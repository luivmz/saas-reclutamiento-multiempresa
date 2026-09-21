<?php

namespace Tests\Feature\Ml;

use App\Models\Organization;
use App\Models\Vacancy;
use App\Services\Ml\MlRiskClient;
use App\Services\Ml\OperationalRiskService;
use App\Services\Ml\RiskAvailability;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

/**
 * Coordinación de la estimación de riesgo.
 *
 * Aquí se comprueba lo que decide **no** preguntar. El experimento observó
 * siempre el mismo instante —el día siguiente al cierre de postulaciones—, así
 * que preguntar en otro punto sería extrapolar y devolver un número con
 * apariencia de rigor que no tiene.
 */
class OperationalRiskServiceTest extends TestCase
{
    use RefreshDatabase;

    private const FINGERPRINT = '9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2';

    private const THRESHOLD = 0.1679418172266036;

    private Organization $organization;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        config()->set('ml.enabled', true);
        config()->set('ml.base_url', 'http://ml-service.test');
        config()->set('ml.retries', 0);
        config()->set('ml.expected_freeze_fingerprint', self::FINGERPRINT);
        config()->set('ml.expected_threshold', self::THRESHOLD);
    }

    private function service(): OperationalRiskService
    {
        return app(OperationalRiskService::class);
    }

    /**
     * Vacante dentro del alcance: publicada, ventana cerrada y plazo vigente.
     */
    private function assessableVacancy(array $attributes = []): Vacancy
    {
        return Vacancy::factory()->for($this->organization)->configured()->create(array_replace([
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
            'published_at' => now()->subDays(42),
            'target_completion_at' => now()->addDays(20)->setTime(18, 0),
        ], $attributes));
    }

    private function fakeSuccess(float $score = 0.42): void
    {
        Http::fake(['*/v1/predict' => Http::response([
            'risk_score' => $score,
            'risk_flag' => $score >= self::THRESHOLD,
            'threshold' => self::THRESHOLD,
            'model_version' => 'phase-15b-20260920-6000',
            'freeze_fingerprint' => self::FINGERPRINT,
            'status' => 'experimental',
        ])]);
    }

    // -- camino predictivo --------------------------------------------------

    public function test_an_assessable_vacancy_gets_a_prediction(): void
    {
        $this->fakeSuccess();

        $assessment = $this->service()->assess($this->assessableVacancy());

        $this->assertSame(RiskAvailability::PredictiveAvailable, $assessment->availability);
        $this->assertSame(0.42, $assessment->score);
        $this->assertTrue($assessment->flag);
        $this->assertSame(42.0, $assessment->scoreAsPercentage());
    }

    public function test_the_assessment_declares_what_it_is_and_is_not(): void
    {
        $this->fakeSuccess();

        $payload = $this->service()->assess($this->assessableVacancy())->toArray();

        $this->assertTrue($payload['is_experimental']);
        $this->assertSame('proceso', $payload['measures']);
        $this->assertTrue($payload['decision_is_human']);
    }

    public function test_a_low_score_produces_no_flag(): void
    {
        $this->fakeSuccess(0.05);

        $assessment = $this->service()->assess($this->assessableVacancy());

        $this->assertFalse($assessment->flag);
        $this->assertStringContainsString('Sin señal de riesgo', $this->service()->explain($assessment));
    }

    public function test_the_flag_message_stays_neutral(): void
    {
        /* La tasa de alerta del modelo es alta: presentar la señal como alarma
           crítica sería desproporcionado. */
        $this->fakeSuccess(0.9);

        $message = $this->service()->explain($this->service()->assess($this->assessableVacancy()));

        $this->assertStringContainsString('para revisión', $message);
        foreach (['ALERTA CRÍTICA', 'RIESGO SEVERO', 'descartar', 'contratar'] as $forbidden) {
            $this->assertStringNotContainsStringIgnoringCase($forbidden, $message);
        }
    }

    // -- fuera del alcance --------------------------------------------------

    public function test_without_a_target_there_is_no_prediction(): void
    {
        Http::fake();

        $assessment = $this->service()->assess($this->assessableVacancy(['target_completion_at' => null]));

        $this->assertSame(RiskAvailability::DescriptiveOnly, $assessment->availability);
        $this->assertSame(OperationalRiskService::REASON_MISSING_TARGET, $assessment->reason);
        $this->assertNull($assessment->score);
        Http::assertNothingSent();
    }

    public function test_an_expired_target_falls_back_instead_of_extrapolating(): void
    {
        Http::fake();

        $vacancy = $this->assessableVacancy([
            'closes_at' => now()->subDays(40)->startOfDay(),
            'target_completion_at' => now()->subDays(5),
        ]);

        $assessment = $this->service()->assess($vacancy);

        $this->assertSame(OperationalRiskService::REASON_TARGET_REACHED, $assessment->reason);
        Http::assertNothingSent();
    }

    public function test_an_open_application_window_falls_back(): void
    {
        /* El modelo observa el proceso tras el cierre; antes, el vector cae
           fuera de lo que vio en entrenamiento. */
        Http::fake();

        $vacancy = $this->assessableVacancy([
            'closes_at' => now()->addDays(5)->startOfDay(),
            'target_completion_at' => now()->addDays(40),
        ]);

        $assessment = $this->service()->assess($vacancy);

        $this->assertSame(OperationalRiskService::REASON_WINDOW_OPEN, $assessment->reason);
        Http::assertNothingSent();
    }

    public function test_an_unpublished_vacancy_falls_back(): void
    {
        Http::fake();

        $vacancy = Vacancy::factory()->for($this->organization)->configured()->create([
            'published_at' => null,
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
        ]);

        $this->assertSame(
            OperationalRiskService::REASON_NOT_PUBLISHED,
            $this->service()->assess($vacancy)->reason
        );
        Http::assertNothingSent();
    }

    // -- servicio caído -----------------------------------------------------

    public function test_a_dead_service_does_not_break_the_flow(): void
    {
        Http::fake(fn () => throw new ConnectionException('Connection refused'));

        $assessment = $this->service()->assess($this->assessableVacancy());

        $this->assertSame(RiskAvailability::Unavailable, $assessment->availability);
        $this->assertNull($assessment->score);
        $this->assertNull($assessment->flag);
        $this->assertStringContainsString('no está disponible', $this->service()->explain($assessment));
    }

    public function test_no_score_is_invented_when_there_is_no_prediction(): void
    {
        /* Un cero se leería como "riesgo nulo", que es una afirmación que nadie
           ha medido. */
        Http::fake(fn () => throw new ConnectionException('Connection refused'));

        foreach ([
            $this->service()->assess($this->assessableVacancy()),
            $this->service()->assess($this->assessableVacancy(['target_completion_at' => null])),
        ] as $assessment) {
            $this->assertNull($assessment->score);
            $this->assertNull($assessment->scoreAsPercentage());
            $this->assertNull($assessment->flag);
            $this->assertNull($assessment->threshold);
        }
    }

    public function test_an_incompatible_response_falls_back(): void
    {
        Http::fake(['*/v1/predict' => Http::response([
            'risk_score' => 0.42,
            'risk_flag' => true,
            'threshold' => self::THRESHOLD,
            'model_version' => 'otro-experimento',
            'freeze_fingerprint' => str_repeat('a', 64),
            'status' => 'experimental',
        ])]);

        $assessment = $this->service()->assess($this->assessableVacancy());

        $this->assertSame(RiskAvailability::Unavailable, $assessment->availability);
        $this->assertSame(MlRiskClient::REASON_INCOMPATIBLE, $assessment->reason);
    }

    public function test_a_disabled_integration_returns_the_descriptive_panel(): void
    {
        config()->set('ml.enabled', false);
        Http::fake();

        $assessment = $this->service()->assess($this->assessableVacancy());

        $this->assertSame(RiskAvailability::DescriptiveOnly, $assessment->availability);
        $this->assertStringContainsString('desactivada', $this->service()->explain($assessment));
    }
}
