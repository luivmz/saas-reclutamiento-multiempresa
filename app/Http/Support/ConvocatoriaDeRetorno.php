<?php

namespace App\Http\Support;

use App\Models\Scopes\OrganizationScope;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Http\Request;

/**
 * Convocatoria a la que vuelve un postulante después de crear su cuenta, iniciar sesión o completar su perfil.
 *
 * Solo se guarda el identificador numérico de una vacante publicada (nunca una URL), así que el destino es
 * siempre /empleos/{id}: no hay forma de dirigir la redirección fuera de la aplicación. La intención vive en
 * la sesión, caduca a las dos horas, se descarta al entrar al acceso o al registro sin indicarla, al postular
 * y al cerrar sesión, y solo se aplica a postulantes. Volver a la convocatoria es una navegación GET: nunca
 * postula por nadie. La autorización de postular sigue en el servidor (ApplyController y su Policy).
 */
final class ConvocatoriaDeRetorno
{
    public const PARAMETRO = 'convocatoria';

    private const CLAVE = 'postulacion.retorno';

    private const VIGENCIA_SEGUNDOS = 7200;

    /**
     * Toma la convocatoria del parámetro de la petición, si es válida, y la guarda.
     *
     * Sin parámetro: en el acceso y el registro se descarta la intención anterior (el visitante eligió otro
     * camino); en el perfil se conserva la que ya había.
     */
    public function capturar(Request $request, bool $olvidarSinParametro = true): ?Vacancy
    {
        $crudo = $this->valorCrudo($request);

        if ($crudo === false) {
            if ($olvidarSinParametro) {
                $this->olvidar($request);
            }

            return null;
        }

        $vacante = $this->publicada($this->identificador($crudo));

        if ($vacante === null) {
            $this->olvidar($request);

            return null;
        }

        $request->session()->put(self::CLAVE, ['id' => $vacante->id, 'at' => now()->getTimestamp()]);

        return $vacante;
    }

    /**
     * Estado de la intención guardada: null si no hay, o si caducó; `disponible` false si la vacante dejó de
     * estar publicada (no se revela su título).
     *
     * @return array{disponible: bool, vacante: Vacancy|null}|null
     */
    public function estado(Request $request): ?array
    {
        $guardado = $request->session()->get(self::CLAVE);

        if (! is_array($guardado) || ! is_int($guardado['id'] ?? null) || ! is_int($guardado['at'] ?? null)) {
            $this->olvidar($request);

            return null;
        }

        if (now()->getTimestamp() - $guardado['at'] > self::VIGENCIA_SEGUNDOS) {
            $this->olvidar($request);

            return null;
        }

        $vacante = $this->publicada($guardado['id']);

        return ['disponible' => $vacante !== null, 'vacante' => $vacante];
    }

    /**
     * Antes de la respuesta de acceso o registro: a un postulante con una convocatoria vigente lo devuelve a
     * ella mediante la URL «intended» que ya respetan Fortify y Passkeys. Si la convocatoria dejó de estar
     * publicada, lo lleva al listado y lo avisa. A otros roles no les cambia nada.
     */
    public function prepararDestino(Request $request): void
    {
        $user = $request->user();
        $estado = $this->estado($request);

        if ($estado === null) {
            return;
        }

        if (! $user instanceof User || ! $user->isCandidate()) {
            $this->olvidar($request);

            return;
        }

        if ($estado['disponible']) {
            $request->session()->put('url.intended', route('jobs.show', $estado['vacante']->id));

            return;
        }

        $this->olvidar($request);
        $request->session()->put('url.intended', route('jobs.index'));
        Toast::error('La convocatoria que estaba viendo ya no está disponible.');
    }

    public function olvidar(Request $request): void
    {
        $request->session()->forget(self::CLAVE);
    }

    /**
     * El valor tal como llegó en la dirección. No se lee de `$request->query()` porque el middleware global
     * TrimStrings ya lo recortó: «7%0A», «7%00» o un espacio de ancho cero delante pasarían por «7».
     * Devuelve false si el parámetro no está.
     */
    private function valorCrudo(Request $request): mixed
    {
        parse_str((string) $request->server->get('QUERY_STRING', ''), $consulta);

        return array_key_exists(self::PARAMETRO, $consulta) ? $consulta[self::PARAMETRO] : false;
    }

    /**
     * Solo dígitos, sin ceros a la izquierda ni signos: «7». Cualquier otra forma (URL, «//», «7abc», «-1»,
     * espacios, codificaciones) se rechaza.
     */
    private function identificador(mixed $valor): ?int
    {
        if (! is_string($valor) || preg_match('/\A[1-9][0-9]{0,9}\z/', $valor) !== 1) {
            return null;
        }

        $id = (int) $valor;

        return $id <= 2147483647 ? $id : null;
    }

    private function publicada(?int $id): ?Vacancy
    {
        return $id === null ? null : Vacancy::query()
            ->withoutGlobalScope(OrganizationScope::class)
            ->published()
            ->find($id);
    }
}
