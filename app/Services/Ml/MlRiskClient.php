<?php

namespace App\Services\Ml;

use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Throwable;

/**
 * Cliente HTTP hacia el servicio de riesgo operacional.
 *
 * Dos principios:
 *
 * - **El servicio nunca rompe el reclutamiento.** Cualquier fallo -- caída,
 *   timeout, 4xx, 5xx, JSON ilegible, contrato incompatible -- se traduce a un
 *   `RiskAssessment` sin predicción. Este cliente no lanza excepciones hacia
 *   arriba.
 * - **No se confía en la respuesta.** Que el servicio conteste 200 no
 *   significa que esté sirviendo el modelo que el equipo auditó. La huella del
 *   experimento y el umbral se comprueban contra los valores aprobados en la
 *   Fase 15B, y una discrepancia descarta la respuesta.
 */
class MlRiskClient
{
    /**
     * Motivos de descarte, para registro y para la vista. Son categorías, no
     * mensajes del servicio: nunca se propaga texto ajeno al usuario.
     */
    public const REASON_DISABLED = 'service_disabled';

    public const REASON_CONNECTION = 'connection_failed';

    public const REASON_TIMEOUT = 'timeout';

    public const REASON_MODEL_UNAVAILABLE = 'model_unavailable';

    public const REASON_REJECTED_PAYLOAD = 'payload_rejected';

    public const REASON_SERVER_ERROR = 'server_error';

    public const REASON_INVALID_JSON = 'invalid_json';

    public const REASON_INCOMPATIBLE = 'incompatible_contract';

    public function __construct(private readonly ?string $baseUrl = null) {}

    public function predict(OperationalRiskFeatures $features): RiskAssessment
    {
        if (! (bool) config('ml.enabled')) {
            return RiskAssessment::descriptive(self::REASON_DISABLED);
        }

        $startedAt = microtime(true);

        try {
            $response = $this->request()->post('/v1/predict', $features->toPayload());
        } catch (ConnectionException $exception) {
            // Distinguir timeout de "no hay nadie escuchando" ayuda a
            // diagnosticar sin tener que leer la excepción completa.
            $reason = str_contains(strtolower($exception->getMessage()), 'timed out')
                ? self::REASON_TIMEOUT
                : self::REASON_CONNECTION;

            $this->log($reason, null, $startedAt);

            return RiskAssessment::unavailable($reason);
        } catch (Throwable $exception) {
            $this->log(self::REASON_CONNECTION, null, $startedAt, $exception::class);

            return RiskAssessment::unavailable(self::REASON_CONNECTION);
        }

        return $this->interpret($response, $startedAt);
    }

    /**
     * Estado del servicio, para diagnóstico. No influye en el flujo.
     *
     * @return array{reachable: bool, model_ready: bool}
     */
    public function health(): array
    {
        if (! (bool) config('ml.enabled')) {
            return ['reachable' => false, 'model_ready' => false];
        }

        try {
            $response = $this->request()->get('/health');
        } catch (Throwable) {
            return ['reachable' => false, 'model_ready' => false];
        }

        if (! $response->successful()) {
            return ['reachable' => true, 'model_ready' => false];
        }

        return [
            'reachable' => true,
            'model_ready' => (bool) $response->json('model_ready', false),
        ];
    }

    private function request(): PendingRequest
    {
        $request = Http::baseUrl($this->baseUrl ?? (string) config('ml.base_url'))
            ->connectTimeout((float) config('ml.connect_timeout'))
            ->timeout((float) config('ml.timeout'))
            ->acceptJson()
            ->asJson();

        $token = config('ml.internal_token');
        if (is_string($token) && $token !== '') {
            $request = $request->withHeaders(['X-Internal-Token' => $token]);
        }

        $retries = max(0, (int) config('ml.retries'));
        if ($retries > 0) {
            // Un reintento como máximo y solo ante fallos de conexión: un 422
            // o un 503 no mejoran por repetirlos, y reintentarlos solo añade
            // latencia al usuario y carga a un servicio que ya está mal.
            $request = $request->retry(
                $retries + 1,
                max(0, (int) config('ml.retry_delay_ms')),
                fn (Throwable $exception): bool => $exception instanceof ConnectionException,
                throw: false,
            );
        }

        return $request;
    }

    private function interpret(Response $response, float $startedAt): RiskAssessment
    {
        $status = $response->status();

        if ($status === 503) {
            $this->log(self::REASON_MODEL_UNAVAILABLE, $status, $startedAt);

            return RiskAssessment::unavailable(self::REASON_MODEL_UNAVAILABLE);
        }

        if ($status === 422) {
            // El servicio rechazó el payload: el error está de este lado, en el
            // feature builder. Se registra como incidencia propia.
            $this->log(self::REASON_REJECTED_PAYLOAD, $status, $startedAt);

            return RiskAssessment::unavailable(self::REASON_REJECTED_PAYLOAD);
        }

        if (! $response->successful()) {
            $this->log(self::REASON_SERVER_ERROR, $status, $startedAt);

            return RiskAssessment::unavailable(self::REASON_SERVER_ERROR);
        }

        try {
            $body = $response->json();
        } catch (Throwable) {
            $body = null;
        }

        if (! is_array($body)) {
            $this->log(self::REASON_INVALID_JSON, $status, $startedAt);

            return RiskAssessment::unavailable(self::REASON_INVALID_JSON);
        }

        $problem = $this->contractViolation($body);
        if ($problem !== null) {
            $this->log(self::REASON_INCOMPATIBLE, $status, $startedAt, $problem);

            return RiskAssessment::unavailable(self::REASON_INCOMPATIBLE);
        }

        $this->log('ok', $status, $startedAt);

        return RiskAssessment::predictive(
            score: (float) $body['risk_score'],
            flag: (bool) $body['risk_flag'],
            threshold: (float) $body['threshold'],
            modelVersion: (string) $body['model_version'],
            freezeFingerprint: (string) $body['freeze_fingerprint'],
        );
    }

    /**
     * Comprueba que la respuesta describe el experimento aprobado.
     *
     * Devuelve la categoría del problema, o `null` si la respuesta es válida.
     *
     * **Todo se valida antes de castear.** `(float) ['a']` vale 1.0 y
     * `(string) 42` vale "42": castear primero convertiría una respuesta
     * absurda en una cifra plausible, que es justo lo que no puede pasar con
     * un número que se va a mostrar a alguien.
     *
     * @param  array<mixed>  $body
     */
    private function contractViolation(array $body): ?string
    {
        foreach (['risk_score', 'risk_flag', 'threshold', 'model_version', 'freeze_fingerprint', 'status'] as $key) {
            if (! array_key_exists($key, $body)) {
                return "missing:{$key}";
            }
        }

        // -- tipos --------------------------------------------------------

        if (! is_int($body['risk_score']) && ! is_float($body['risk_score'])) {
            return 'score_not_numeric';
        }

        $score = (float) $body['risk_score'];
        if (! is_finite($score) || $score < 0.0 || $score > 1.0) {
            return 'score_out_of_range';
        }

        if (! is_bool($body['risk_flag'])) {
            return 'flag_not_boolean';
        }

        if (! is_int($body['threshold']) && ! is_float($body['threshold'])) {
            return 'threshold_not_numeric';
        }
        if (! is_finite((float) $body['threshold'])) {
            return 'threshold_not_finite';
        }

        foreach (['model_version', 'freeze_fingerprint', 'status'] as $key) {
            if (! is_string($body[$key])) {
                return "{$key}_not_string";
            }
            if (trim($body[$key]) === '') {
                return "{$key}_empty";
            }
        }

        // -- identidad del experimento -------------------------------------

        // El umbral debe ser el exacto de la Fase 15B. Se compara con una
        // tolerancia mínima porque viaja por JSON, no porque se admita otro.
        $expectedThreshold = (float) config('ml.expected_threshold');
        if (abs((float) $body['threshold'] - $expectedThreshold) > 1e-12) {
            return 'threshold_mismatch';
        }

        $expectedFingerprint = (string) config('ml.expected_freeze_fingerprint');
        if (! hash_equals($expectedFingerprint, $body['freeze_fingerprint'])) {
            return 'fingerprint_mismatch';
        }

        $expectedVersion = (string) config('ml.expected_model_version');
        if ($expectedVersion !== '' && ! hash_equals($expectedVersion, $body['model_version'])) {
            return 'model_version_mismatch';
        }

        // La respuesta debe seguir declarándose experimental. Si algún día deja
        // de hacerlo, es que el servicio cambió de contrato sin avisar.
        if ($body['status'] !== 'experimental') {
            return 'status_not_experimental';
        }

        // Coherencia interna: la bandera es el umbral aplicado al score.
        if ($body['risk_flag'] !== ($score >= (float) $body['threshold'])) {
            return 'flag_inconsistent_with_threshold';
        }

        return null;
    }

    /**
     * Registro sin PII.
     *
     * Se guardan categoría, estado HTTP y duración. **No** se registran el
     * payload, la respuesta completa ni el token: lo primero contiene el
     * estado operativo de una vacante concreta, y lo último es un secreto.
     */
    private function log(string $outcome, ?int $status, float $startedAt, ?string $detail = null): void
    {
        $context = [
            'outcome' => $outcome,
            'status' => $status,
            'duration_ms' => (int) round((microtime(true) - $startedAt) * 1000),
        ];

        if ($detail !== null) {
            $context['detail'] = $detail;
        }

        if ($outcome === 'ok') {
            Log::debug('ml.risk.predict', $context);

            return;
        }

        Log::warning('ml.risk.predict', $context);
    }
}
