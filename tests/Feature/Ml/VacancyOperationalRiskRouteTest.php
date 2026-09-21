<?php

namespace Tests\Feature\Ml;

use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Ml\OperationalRiskService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

/**
 * Ruta de consulta del riesgo operacional.
 *
 * Quién puede verlo, quién no, y qué contiene la respuesta. Lo último importa
 * tanto como lo primero: la respuesta no puede contener nada sobre personas ni
 * parecerse a una decisión.
 */
class VacancyOperationalRiskRouteTest extends TestCase
{
    use RefreshDatabase;

    private const FINGERPRINT = '9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2';

    private const THRESHOLD = 0.1679418172266036;

    private Organization $organization;

    private User $hr;

    private Vacancy $vacancy;

    protected function setUp(): void
    {
        parent::setUp();

        config()->set('ml.enabled', true);
        config()->set('ml.base_url', 'http://ml-service.test');
        config()->set('ml.retries', 0);
        config()->set('ml.expected_freeze_fingerprint', self::FINGERPRINT);
        config()->set('ml.expected_threshold', self::THRESHOLD);

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->create([
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
            'published_at' => now()->subDays(42),
            'target_completion_at' => now()->addDays(20)->setTime(18, 0),
        ]);
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

    private function url(?Vacancy $vacancy = null): string
    {
        return route('vacancies.operational-risk', $vacancy ?? $this->vacancy);
    }

    // -- autorización -------------------------------------------------------

    public function test_hr_can_query_the_operational_risk(): void
    {
        $this->fakeSuccess();

        $this->actingAs($this->hr)
            ->getJson($this->url())
            ->assertOk()
            ->assertJsonPath('risk.availability', 'predictive_available')
            ->assertJsonPath('risk.risk_score', 0.42);
    }

    public function test_the_approver_can_query_it(): void
    {
        $this->fakeSuccess();
        $approver = User::factory()->approver($this->organization)->create();

        $this->actingAs($approver)->getJson($this->url())->assertOk();
    }

    public function test_a_candidate_cannot_query_it(): void
    {
        Http::fake();
        $candidate = User::factory()->candidate()->create();

        $this->actingAs($candidate)->getJson($this->url())->assertForbidden();
        Http::assertNothingSent();
    }

    public function test_an_evaluator_cannot_query_it(): void
    {
        Http::fake();
        $evaluator = User::factory()->evaluator($this->organization)->create();

        $this->actingAs($evaluator)->getJson($this->url())->assertForbidden();
        Http::assertNothingSent();
    }

    public function test_a_guest_cannot_query_it(): void
    {
        Http::fake();

        $this->getJson($this->url())->assertUnauthorized();
        Http::assertNothingSent();
    }

    // -- multiempresa -------------------------------------------------------

    public function test_hr_cannot_query_another_organizations_vacancy(): void
    {
        Http::fake();
        $other = Organization::factory()->create();
        $foreign = Vacancy::factory()->for($other)->configured()->create([
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
            'published_at' => now()->subDays(42),
            'target_completion_at' => now()->addDays(20),
        ]);

        /* El scope global oculta la vacante ajena, así que la vinculación de
           ruta ni siquiera la encuentra: 404 antes de llegar a la policy. */
        $this->actingAs($this->hr)->getJson($this->url($foreign))->assertNotFound();
        Http::assertNothingSent();
    }

    public function test_the_policy_denies_a_foreign_vacancy_even_without_the_global_scope(): void
    {
        /* Defensa en profundidad: aunque alguien resolviera la vacante sin el
           scope, la policy sigue negando. */
        $other = Organization::factory()->create();
        $foreign = Vacancy::factory()->for($other)->create();

        $this->assertFalse($this->hr->can('viewOperationalRisk', $foreign));
    }

    // -- contenido de la respuesta -----------------------------------------

    public function test_the_response_declares_the_experimental_nature(): void
    {
        $this->fakeSuccess();

        $this->actingAs($this->hr)
            ->getJson($this->url())
            ->assertJsonPath('risk.is_experimental', true)
            ->assertJsonPath('risk.measures', 'proceso')
            ->assertJsonPath('risk.decision_is_human', true);
    }

    public function test_the_response_never_mentions_candidates_or_decisions(): void
    {
        $this->fakeSuccess(0.95);

        $body = $this->actingAs($this->hr)->getJson($this->url())->getContent();

        foreach ([
            'candidate', 'candidato', 'postulante', 'ranking', 'seleccion',
            'contratar', 'descartar', 'recomendado', 'email', 'nombre',
        ] as $forbidden) {
            $this->assertStringNotContainsStringIgnoringCase($forbidden, $body);
        }
    }

    public function test_a_dead_service_still_returns_a_usable_panel(): void
    {
        /* Que el servicio esté caído es un estado del panel, no un error de la
           petición: el flujo de reclutamiento no depende de él. */
        Http::fake(fn () => throw new ConnectionException('Connection refused'));

        $this->actingAs($this->hr)
            ->getJson($this->url())
            ->assertOk()
            ->assertJsonPath('risk.availability', 'unavailable')
            ->assertJsonPath('risk.risk_score', null)
            ->assertJsonPath('risk.risk_flag', null);
    }

    public function test_a_vacancy_without_a_target_returns_the_descriptive_panel(): void
    {
        Http::fake();
        $this->vacancy->forceFill(['target_completion_at' => null])->save();

        $this->actingAs($this->hr)
            ->getJson($this->url())
            ->assertOk()
            ->assertJsonPath('risk.availability', 'descriptive_only')
            ->assertJsonPath('risk.reason', OperationalRiskService::REASON_MISSING_TARGET)
            ->assertJsonPath('risk.risk_score', null);
    }

    public function test_the_response_leaks_no_paths_or_traces(): void
    {
        Http::fake(fn () => throw new ConnectionException('Connection refused at http://ml-service.test'));

        $body = $this->actingAs($this->hr)->getJson($this->url())->getContent();

        foreach (['Traceback', 'vendor/', '/var/www', 'ml-service.test', 'Exception'] as $leak) {
            $this->assertStringNotContainsString($leak, $body);
        }
    }
}
