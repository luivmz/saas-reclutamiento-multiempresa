<?php

namespace Tests\Feature\Ml;

use App\Services\Ml\MlRiskClient;
use App\Services\Ml\OperationalRiskFeatures;
use App\Services\Ml\RiskAvailability;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * Cliente HTTP hacia el servicio de riesgo.
 *
 * Todo lo que puede salir mal aquí tiene que terminar en un `RiskAssessment`
 * sin predicción, nunca en una excepción que suba: el reclutamiento no puede
 * depender de que el servicio esté sano.
 *
 * Y una garantía que va más allá de la disponibilidad: **que el servicio
 * responda 200 no basta**. Si la huella del experimento o el umbral no son los
 * que el equipo auditó, la respuesta se descarta.
 */
class MlRiskClientTest extends TestCase
{
    private const FINGERPRINT = '9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2';

    private const THRESHOLD = 0.1679418172266036;

    private const MODEL_VERSION = 'phase-15b-20260920-6000';

    protected function setUp(): void
    {
        parent::setUp();

        config()->set('ml.enabled', true);
        config()->set('ml.base_url', 'http://ml-service.test');
        config()->set('ml.retries', 0);
        config()->set('ml.internal_token', null);
        config()->set('ml.expected_freeze_fingerprint', self::FINGERPRINT);
        config()->set('ml.expected_threshold', self::THRESHOLD);
        config()->set('ml.expected_model_version', self::MODEL_VERSION);
    }

    private function features(): OperationalRiskFeatures
    {
        return OperationalRiskFeatures::fromArray(array_fill_keys(OperationalRiskFeatures::NAMES, 3));
    }

    /**
     * @param  array<string, mixed>  $overrides
     * @return array<string, mixed>
     */
    private function validBody(array $overrides = []): array
    {
        return array_replace([
            'risk_score' => 0.42,
            'risk_flag' => true,
            'threshold' => self::THRESHOLD,
            'model_version' => self::MODEL_VERSION,
            'freeze_fingerprint' => self::FINGERPRINT,
            'status' => 'experimental',
        ], $overrides);
    }

    private function client(): MlRiskClient
    {
        return app(MlRiskClient::class);
    }

    // -- camino feliz -------------------------------------------------------

    public function test_a_valid_response_produces_a_prediction(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody())]);

        $assessment = $this->client()->predict($this->features());

        $this->assertTrue($assessment->isPredictive());
        $this->assertSame(0.42, $assessment->score);
        $this->assertTrue($assessment->flag);
        $this->assertSame(self::THRESHOLD, $assessment->threshold);
        $this->assertSame('phase-15b-20260920-6000', $assessment->modelVersion);
    }

    public function test_it_sends_only_the_fifteen_features(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody())]);

        $this->client()->predict($this->features());

        Http::assertSent(function (Request $request): bool {
            $payload = $request->data();

            return array_keys($payload) === OperationalRiskFeatures::NAMES
                && count($payload) === 15;
        });
    }

    public function test_it_attaches_the_internal_token_when_configured(): void
    {
        config()->set('ml.internal_token', 'token-de-prueba');
        Http::fake(['*/v1/predict' => Http::response($this->validBody())]);

        $this->client()->predict($this->features());

        Http::assertSent(fn (Request $request): bool => $request->hasHeader('X-Internal-Token', 'token-de-prueba'));
    }

    public function test_it_sends_no_token_header_when_none_is_configured(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody())]);

        $this->client()->predict($this->features());

        Http::assertSent(fn (Request $request): bool => ! $request->hasHeader('X-Internal-Token'));
    }

    // -- interruptor --------------------------------------------------------

    public function test_a_disabled_service_never_calls_out(): void
    {
        config()->set('ml.enabled', false);
        Http::fake();

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(RiskAvailability::DescriptiveOnly, $assessment->availability);
        $this->assertSame(MlRiskClient::REASON_DISABLED, $assessment->reason);
        Http::assertNothingSent();
    }

    // -- fallos de transporte ----------------------------------------------

    public function test_a_connection_failure_falls_back(): void
    {
        Http::fake(fn () => throw new ConnectionException('Connection refused'));

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(RiskAvailability::Unavailable, $assessment->availability);
        $this->assertSame(MlRiskClient::REASON_CONNECTION, $assessment->reason);
        $this->assertNull($assessment->score);
    }

    public function test_a_timeout_is_reported_as_such(): void
    {
        Http::fake(fn () => throw new ConnectionException('cURL error 28: Operation timed out'));

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(MlRiskClient::REASON_TIMEOUT, $assessment->reason);
    }

    // -- respuestas de error ------------------------------------------------

    public function test_a_503_means_the_model_is_unavailable(): void
    {
        Http::fake(['*/v1/predict' => Http::response(['error' => 'model_unavailable'], 503)]);

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(MlRiskClient::REASON_MODEL_UNAVAILABLE, $assessment->reason);
    }

    public function test_a_422_means_our_payload_was_wrong(): void
    {
        Http::fake(['*/v1/predict' => Http::response(['error' => 'validation_error'], 422)]);

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(MlRiskClient::REASON_REJECTED_PAYLOAD, $assessment->reason);
    }

    public function test_a_401_falls_back_without_breaking(): void
    {
        Http::fake(['*/v1/predict' => Http::response(['detail' => 'no autorizado'], 401)]);

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(RiskAvailability::Unavailable, $assessment->availability);
        $this->assertSame(MlRiskClient::REASON_SERVER_ERROR, $assessment->reason);
    }

    public function test_a_500_falls_back(): void
    {
        Http::fake(['*/v1/predict' => Http::response(['error' => 'inference_failed'], 500)]);

        $this->assertSame(MlRiskClient::REASON_SERVER_ERROR, $this->client()->predict($this->features())->reason);
    }

    public function test_invalid_json_falls_back(): void
    {
        Http::fake(['*/v1/predict' => Http::response('esto no es json', 200, ['Content-Type' => 'text/plain'])]);

        $this->assertSame(MlRiskClient::REASON_INVALID_JSON, $this->client()->predict($this->features())->reason);
    }

    // -- validación del contrato -------------------------------------------

    public function test_a_wrong_freeze_fingerprint_is_rejected(): void
    {
        /* El servicio contesta 200 y un número plausible, pero está sirviendo
           otro modelo. Aceptarlo sería presentar como auditado algo que no lo
           está. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['freeze_fingerprint' => str_repeat('0', 64)]))]);

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(RiskAvailability::Unavailable, $assessment->availability);
        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $assessment->reason);
        $this->assertNull($assessment->score);
    }

    public function test_a_wrong_threshold_is_rejected(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody([
            'threshold' => 0.5,
            'risk_flag' => false,
        ]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_a_rounded_threshold_is_rejected(): void
    {
        /* El umbral congelado tiene 16 decimales; su versión redondeada
           clasifica distinto en la frontera. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['threshold' => 0.167942]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    /**
     * @return array<string, array{mixed}>
     */
    public static function invalidScores(): array
    {
        return [
            'negativo' => [-0.1],
            'mayor que uno' => [1.5],
            'texto' => ['alto'],
            'nulo' => [null],
        ];
    }

    #[DataProvider('invalidScores')]
    public function test_an_invalid_score_is_rejected(mixed $score): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['risk_score' => $score]))]);

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $assessment->reason);
        $this->assertNull($assessment->score);
    }

    public function test_a_non_boolean_flag_is_rejected(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['risk_flag' => 'si']))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_a_flag_inconsistent_with_the_threshold_is_rejected(): void
    {
        /* 0.05 está por debajo del umbral, así que la bandera no puede ser
           verdadera: el servicio se estaría contradiciendo. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody([
            'risk_score' => 0.05,
            'risk_flag' => true,
        ]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_a_response_that_stops_declaring_itself_experimental_is_rejected(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['status' => 'production']))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    /**
     * @return array<string, array{string}>
     */
    public static function requiredKeys(): array
    {
        return [
            'risk_score' => ['risk_score'],
            'risk_flag' => ['risk_flag'],
            'threshold' => ['threshold'],
            'model_version' => ['model_version'],
            'freeze_fingerprint' => ['freeze_fingerprint'],
        ];
    }

    #[DataProvider('requiredKeys')]
    public function test_a_missing_key_is_rejected(string $key): void
    {
        $body = $this->validBody();
        unset($body[$key]);
        Http::fake(['*/v1/predict' => Http::response($body)]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    // -- identidad del modelo ----------------------------------------------

    public function test_an_empty_model_version_is_rejected(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['model_version' => '']))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_a_blank_model_version_is_rejected(): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['model_version' => '   ']))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_a_different_model_version_is_rejected(): void
    {
        /* Huella correcta y versión distinta es una respuesta incoherente: el
           servicio estaría diciendo dos cosas a la vez. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody([
            'model_version' => 'phase-15b-20260920-1000',
        ]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    /**
     * @return array<string, array{mixed}>
     */
    public static function nonStringValues(): array
    {
        return [
            'numero' => [42],
            'decimal' => [1.5],
            'booleano' => [true],
            'nulo' => [null],
            'array' => [['phase-15b']],
            'objeto' => [['version' => 'phase-15b']],
        ];
    }

    #[DataProvider('nonStringValues')]
    public function test_a_non_string_model_version_is_rejected(mixed $value): void
    {
        /* Sin comprobar el tipo, `(string) 42` valdría "42" y una respuesta
           absurda se convertiría en una cifra plausible. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['model_version' => $value]))]);

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $assessment->reason);
        $this->assertNull($assessment->score);
        $this->assertNull($assessment->flag);
        $this->assertNull($assessment->threshold);
    }

    #[DataProvider('nonStringValues')]
    public function test_a_non_string_fingerprint_is_rejected(mixed $value): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['freeze_fingerprint' => $value]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    #[DataProvider('nonStringValues')]
    public function test_a_non_string_status_is_rejected(mixed $value): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['status' => $value]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    /**
     * @return array<string, array{mixed}>
     */
    public static function nonNumericValues(): array
    {
        return [
            'texto' => ['0.42'],
            'array' => [[0.42]],
            'objeto' => [['valor' => 0.42]],
            'booleano' => [true],
            'nulo' => [null],
        ];
    }

    #[DataProvider('nonNumericValues')]
    public function test_a_non_numeric_score_is_rejected(mixed $value): void
    {
        /* Una cadena numérica tampoco pasa: el servicio devuelve JSON, y en
           JSON un número es un número. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['risk_score' => $value]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    #[DataProvider('nonNumericValues')]
    public function test_a_non_numeric_threshold_is_rejected(mixed $value): void
    {
        Http::fake(['*/v1/predict' => Http::response($this->validBody(['threshold' => $value]))]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_a_missing_status_is_rejected(): void
    {
        $body = $this->validBody();
        unset($body['status']);
        Http::fake(['*/v1/predict' => Http::response($body)]);

        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $this->client()->predict($this->features())->reason);
    }

    public function test_the_valid_response_is_still_accepted(): void
    {
        /* Control positivo: el endurecimiento no puede rechazarlo todo. */
        Http::fake(['*/v1/predict' => Http::response($this->validBody())]);

        $assessment = $this->client()->predict($this->features());

        $this->assertTrue($assessment->isPredictive());
        $this->assertSame(self::MODEL_VERSION, $assessment->modelVersion);
    }

    // -- reintentos ---------------------------------------------------------

    public function test_a_transient_failure_is_retried_once(): void
    {
        config()->set('ml.retries', 1);
        config()->set('ml.retry_delay_ms', 0);
        $attempts = 0;
        Http::fake(function () use (&$attempts) {
            $attempts++;

            if ($attempts === 1) {
                throw new ConnectionException('Connection refused');
            }

            return Http::response($this->validBody());
        });

        $assessment = $this->client()->predict($this->features());

        $this->assertSame(2, $attempts);
        $this->assertTrue($assessment->isPredictive());
    }

    public function test_an_error_response_is_not_retried(): void
    {
        /* Un 422 o un 503 no mejoran por repetirlos: solo añaden latencia al
           usuario y carga a un servicio que ya está mal. */
        config()->set('ml.retries', 1);
        config()->set('ml.retry_delay_ms', 0);
        $attempts = 0;
        Http::fake(function () use (&$attempts) {
            $attempts++;

            return Http::response(['error' => 'model_unavailable'], 503);
        });

        $this->client()->predict($this->features());

        $this->assertSame(1, $attempts);
    }

    // -- diagnóstico --------------------------------------------------------

    public function test_health_reports_the_service_state(): void
    {
        Http::fake(['*/health' => Http::response(['status' => 'ok', 'model_ready' => true])]);

        $this->assertSame(['reachable' => true, 'model_ready' => true], $this->client()->health());
    }

    public function test_health_survives_a_dead_service(): void
    {
        Http::fake(fn () => throw new ConnectionException('Connection refused'));

        $this->assertSame(['reachable' => false, 'model_ready' => false], $this->client()->health());
    }
}
