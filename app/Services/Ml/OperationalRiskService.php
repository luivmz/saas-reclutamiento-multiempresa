<?php

namespace App\Services\Ml;

use App\Models\Vacancy;
use Carbon\CarbonInterface;
use Illuminate\Support\Carbon;

/**
 * Coordina la estimación de riesgo operacional de una vacante.
 *
 * Orden: calcular el checkpoint → comprobar que el proceso está dentro de la
 * ventana válida → construir features **en el checkpoint** → llamar al
 * servicio → devolver un resultado validado. El controlador no habla HTTP ni
 * conoce features.
 *
 * El checkpoint no es «ahora»
 * ---------------------------
 * El experimento de la Fase 15B observó **siempre** el mismo instante:
 * `start_of_day(closes_at + 1 día)` en `America/Lima`
 * (`ml-service/src/recruitment_ml/synthetic/timeline.py:279`). Todas las
 * features del dataset se derivaron del historial truncado ahí, y la
 * especificación lo fija como invariante: «cero eventos posteriores al
 * checkpoint incorporados a cualquier feature».
 *
 * Inferir con `now()` produciría un vector que el modelo nunca vio -- más
 * postulaciones, más sesiones, más días transcurridos -- y devolvería un
 * número con apariencia de rigor. Aquí se usa el checkpoint aprobado y nada
 * más, así que **el vector de una vacante es fijo y reproducible**: consultar
 * dos veces con días de diferencia da exactamente el mismo resultado.
 *
 * La ventana de consulta
 * ----------------------
 * Que el vector sea fijo no significa que preguntar tenga sentido siempre:
 *
 * - **antes del checkpoint** el proceso todavía no llegó al punto observado;
 * - **con la vacante cerrada** el desenlace ya se conoce, y presentar una
 *   «estimación» de algo resuelto sería engañoso;
 * - **pasado el plazo objetivo** la pregunta «¿se retrasará?» ya tiene
 *   respuesta en el calendario, no en un modelo.
 */
class OperationalRiskService
{
    public const REASON_NOT_PUBLISHED = 'vacancy_not_published';

    public const REASON_MISSING_CLOSE = 'missing_application_close';

    public const REASON_MISSING_TARGET = 'missing_target_completion_at';

    public const REASON_CHECKPOINT_NOT_REACHED = 'checkpoint_not_reached';

    public const REASON_VACANCY_CLOSED = 'vacancy_already_closed';

    public const REASON_TARGET_BEFORE_CHECKPOINT = 'target_before_checkpoint';

    public const REASON_QUERY_AFTER_TARGET = 'query_after_target';

    public function __construct(
        private readonly OperationalRiskFeatureBuilder $features,
        private readonly MlRiskClient $client,
    ) {}

    /**
     * @param  CarbonInterface|null  $now  Momento de la consulta; por omisión, ahora.
     */
    public function assess(Vacancy $vacancy, ?CarbonInterface $now = null): RiskAssessment
    {
        $now = $this->inProjectTimezone($now ?? Carbon::now());

        $outOfScope = $this->outOfScopeReason($vacancy, $now);
        if ($outOfScope !== null) {
            return RiskAssessment::descriptive($outOfScope);
        }

        // El vector se construye en el checkpoint aprobado, no en `$now`.
        return $this->client->predict(
            $this->features->build($vacancy, $this->checkpointFor($vacancy))
        );
    }

    /**
     * Checkpoint aprobado: inicio del día siguiente al cierre de postulaciones.
     *
     * `null` si la vacante no tiene fecha de cierre, en cuyo caso no existe
     * punto de observación y no hay nada que estimar.
     */
    public function checkpointFor(Vacancy $vacancy): ?CarbonInterface
    {
        if ($vacancy->closes_at === null) {
            return null;
        }

        return $this->inProjectTimezone($vacancy->closes_at)
            ->addDay()
            ->startOfDay();
    }

    /**
     * Motivo por el que no se estima, o `null` si la consulta es válida.
     */
    public function outOfScopeReason(Vacancy $vacancy, ?CarbonInterface $now = null): ?string
    {
        $now = $this->inProjectTimezone($now ?? Carbon::now());

        if ($vacancy->published_at === null) {
            return self::REASON_NOT_PUBLISHED;
        }

        $checkpoint = $this->checkpointFor($vacancy);
        if ($checkpoint === null) {
            return self::REASON_MISSING_CLOSE;
        }

        // GAP-01: sin plazo objetivo no hay ML-FEAT-02, y no se inventa.
        if ($vacancy->target_completion_at === null) {
            return self::REASON_MISSING_TARGET;
        }

        if ($now->lt($checkpoint)) {
            return self::REASON_CHECKPOINT_NOT_REACHED;
        }

        // Desenlace conocido: estimar ahora sería presentar como pronóstico
        // algo que ya ocurrió.
        if ($vacancy->closed_at !== null) {
            return self::REASON_VACANCY_CLOSED;
        }

        /* El contrato del servicio exige `days_remaining_to_target >= 1` en el
           checkpoint, y el valor **no se recorta**: un plazo que no sobrevive
           al punto de observación describe un proceso que el modelo nunca vio,
           porque el dataset solo contiene plazos posteriores al checkpoint. */
        if ($this->features->daysRemainingToTarget($vacancy, $checkpoint) < 1) {
            return self::REASON_TARGET_BEFORE_CHECKPOINT;
        }

        // Consulta tardía: pasado el plazo, la pregunta ya la responde el
        // calendario.
        if ($now->gt($this->inProjectTimezone($vacancy->target_completion_at))) {
            return self::REASON_QUERY_AFTER_TARGET;
        }

        return null;
    }

    /**
     * Texto en español para la interfaz. Tono neutro a propósito: la tasa de
     * alerta del modelo es alta (73.5 % en test) y presentar la señal como
     * alarma crítica sería desproporcionado.
     */
    public function explain(RiskAssessment $assessment): string
    {
        return match (true) {
            $assessment->isPredictive() => $assessment->flag
                ? 'Señal de riesgo para revisión. Conviene revisar el avance del proceso; no es una decisión ni una alarma.'
                : 'Sin señal de riesgo en este momento. El proceso avanza dentro de lo esperado por el modelo.',
            $assessment->reason === self::REASON_MISSING_TARGET => 'Sin plazo objetivo configurado: registra la fecha límite del proceso para habilitar la estimación.',
            $assessment->reason === self::REASON_MISSING_CLOSE => 'Sin fecha de cierre de postulaciones no hay punto de observación para estimar.',
            $assessment->reason === self::REASON_CHECKPOINT_NOT_REACHED => 'El modelo observa el proceso el día siguiente al cierre de postulaciones. Todavía no se alcanzó ese punto.',
            $assessment->reason === self::REASON_VACANCY_CLOSED => 'La vacante ya está cerrada: el desenlace se conoce y no se estima riesgo.',
            $assessment->reason === self::REASON_TARGET_BEFORE_CHECKPOINT => 'El plazo objetivo no supera el punto de observación del modelo, así que queda fuera de lo que puede estimar.',
            $assessment->reason === self::REASON_QUERY_AFTER_TARGET => 'El plazo objetivo ya venció. A estas alturas el avance del proceso se comprueba, no se estima.',
            $assessment->reason === self::REASON_NOT_PUBLISHED => 'La vacante aún no se publica: no hay proceso que estimar.',
            $assessment->reason === MlRiskClient::REASON_DISABLED => 'La estimación de riesgo está desactivada en este entorno.',
            $assessment->availability === RiskAvailability::Unavailable => 'El servicio de estimación no está disponible. Los indicadores descriptivos del proceso siguen vigentes.',
            default => 'Solo hay información descriptiva del proceso.',
        };
    }

    private function inProjectTimezone(CarbonInterface $moment): Carbon
    {
        return Carbon::instance($moment->toDateTime())->setTimezone(config('app.timezone'));
    }
}
