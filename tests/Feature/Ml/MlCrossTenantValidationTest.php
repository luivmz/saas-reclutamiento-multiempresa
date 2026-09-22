<?php

namespace Tests\Feature\Ml;

use App\Models\Application;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Ml\OperationalRiskFeatureBuilder;
use App\Services\Ml\OperationalRiskService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

/**
 * Multiempresa, en modo adversarial.
 *
 * Dos organizaciones con datos equivalentes y nombres deliberadamente
 * parecidos. Se comprueba que **nada** de la organización B puede influir en el
 * vector, en la ruta ni en la respuesta de la organización A.
 *
 * Una fuga cross-tenant aquí no es un defecto menor: el modelo pasaría a medir
 * un proceso con datos de otra institución.
 */
class MlCrossTenantValidationTest extends TestCase
{
    use RefreshDatabase;

    private Organization $orgA;

    private Organization $orgB;

    private User $hrA;

    private User $hrB;

    private Vacancy $vacancyA;

    private Vacancy $vacancyB;

    private OperationalRiskFeatureBuilder $builder;

    protected function setUp(): void
    {
        parent::setUp();

        config()->set('ml.enabled', true);
        config()->set('ml.base_url', 'http://ml-service.test');
        config()->set('ml.retries', 0);

        $this->builder = app(OperationalRiskFeatureBuilder::class);

        $this->orgA = Organization::factory()->create(['name' => 'Colegio Ficticio A']);
        $this->orgB = Organization::factory()->create(['name' => 'Colegio Ficticio B']);
        $this->hrA = User::factory()->hr($this->orgA)->create();
        $this->hrB = User::factory()->hr($this->orgB)->create();

        $this->vacancyA = $this->populatedVacancy($this->orgA, 3);
        $this->vacancyB = $this->populatedVacancy($this->orgB, 7);
    }

    /**
     * Vacante con postulaciones, transiciones, evaluaciones y entrevistas.
     */
    private function populatedVacancy(Organization $organization, int $applications): Vacancy
    {
        $vacancy = Vacancy::factory()->for($organization)->configured()->create([
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
            'published_at' => now()->subDays(42),
            'target_completion_at' => now()->addDays(25)->setTime(18, 0),
            'positions' => 2,
        ]);

        for ($index = 0; $index < $applications; $index++) {
            $application = Application::factory()->create([
                'organization_id' => $organization->id,
                'vacancy_id' => $vacancy->id,
                'candidate_id' => User::factory()->candidate()->create()->id,
                'applied_at' => now()->subDays(25),
            ]);
            DB::table('application_stage_histories')
                ->where('application_id', $application->id)
                ->update(['created_at' => now()->subDays(25)]);

            Evaluation::factory()->forApplication($application)->create([
                'created_at' => now()->subDays(22),
                'scheduled_at' => now()->subDays(20),
            ]);
            Interview::factory()->forApplication($application)->create([
                'created_at' => now()->subDays(18),
                'scheduled_at' => now()->subDays(16),
            ]);
        }

        return $vacancy;
    }

    private function checkpoint(Vacancy $vacancy)
    {
        return app(OperationalRiskService::class)->checkpointFor($vacancy);
    }

    private function vector(Vacancy $vacancy): array
    {
        return $this->builder->build($vacancy, $this->checkpoint($vacancy))->toPayload();
    }

    // -- el vector de A no ve a B -------------------------------------------

    public function test_each_organization_gets_its_own_counts(): void
    {
        $this->assertSame(3, $this->vector($this->vacancyA)['applications_received_count']);
        $this->assertSame(7, $this->vector($this->vacancyB)['applications_received_count']);
    }

    public function test_adding_data_to_b_does_not_move_the_vector_of_a(): void
    {
        $before = $this->vector($this->vacancyA);

        // Mucha actividad en B, incluida una vacante concurrente.
        $this->populatedVacancy($this->orgB, 12);
        for ($index = 0; $index < 15; $index++) {
            $application = Application::factory()->create([
                'organization_id' => $this->orgB->id,
                'vacancy_id' => $this->vacancyB->id,
                'candidate_id' => User::factory()->candidate()->create()->id,
                'applied_at' => now()->subDays(25),
            ]);
            Evaluation::factory()->forApplication($application)->create([
                'created_at' => now()->subDays(22),
                'scheduled_at' => now()->subDays(20),
            ]);
        }

        $this->assertSame($before, $this->vector($this->vacancyA->fresh()));
    }

    public function test_concurrent_vacancies_never_count_another_organization(): void
    {
        Vacancy::factory()->for($this->orgB)->count(6)->create([
            'published_at' => now()->subDays(30),
            'closed_at' => null,
            'opens_at' => now()->subDays(30)->startOfDay(),
            'closes_at' => now()->addDays(10)->startOfDay(),
        ]);

        $this->assertSame(0, $this->vector($this->vacancyA)['concurrent_open_vacancies_count']);
    }

    public function test_there_is_no_leakage_without_a_session(): void
    {
        /* `OrganizationScope` solo actúa con usuario autenticado. El builder
           puede correr en consola o en cola, donde no lo hay: por eso filtra
           por organización en cada consulta. */
        $this->assertNull(auth()->user());

        $this->assertSame(3, $this->vector($this->vacancyA)['applications_received_count']);
        $this->assertSame(7, $this->vector($this->vacancyB)['applications_received_count']);
    }

    public function test_the_vector_of_a_is_unchanged_when_b_is_wiped(): void
    {
        /* La prueba inversa: si el vector de A dependiera de B, borrar B lo
           movería. */
        $before = $this->vector($this->vacancyA);

        DB::table('interviews')->where('organization_id', $this->orgB->id)->delete();
        DB::table('evaluations')->where('organization_id', $this->orgB->id)->delete();
        DB::table('application_stage_histories')->where('organization_id', $this->orgB->id)->delete();
        DB::table('applications')->where('organization_id', $this->orgB->id)->delete();

        $this->assertSame($before, $this->vector($this->vacancyA->fresh()));
    }

    // -- la ruta de A no expone B -------------------------------------------

    public function test_hr_of_a_cannot_reach_the_vacancy_of_b(): void
    {
        Http::fake();

        $this->actingAs($this->hrA)
            ->getJson(route('vacancies.operational-risk', $this->vacancyB))
            ->assertNotFound();

        Http::assertNothingSent();
    }

    public function test_the_denial_does_not_reveal_whether_the_vacancy_exists(): void
    {
        /* Una vacante ajena y un identificador inexistente deben responder
           igual: distinguirlos filtraría qué procesos tiene la otra
           organización. */
        Http::fake();

        $foreign = $this->actingAs($this->hrA)
            ->getJson(route('vacancies.operational-risk', $this->vacancyB));
        $missing = $this->actingAs($this->hrA)
            ->getJson('/vacantes/999999/riesgo-operacional');

        $this->assertSame($foreign->status(), $missing->status());
        $this->assertSame(404, $foreign->status());
    }

    public function test_each_organization_sees_only_its_own_risk(): void
    {
        Http::fake(['*/v1/predict' => Http::response([
            'risk_score' => 0.42,
            'risk_flag' => true,
            'threshold' => (float) config('ml.expected_threshold'),
            'model_version' => (string) config('ml.expected_model_version'),
            'freeze_fingerprint' => (string) config('ml.expected_freeze_fingerprint'),
            'status' => 'experimental',
        ])]);

        $this->actingAs($this->hrA)
            ->getJson(route('vacancies.operational-risk', $this->vacancyA))
            ->assertOk();
        $this->actingAs($this->hrB)
            ->getJson(route('vacancies.operational-risk', $this->vacancyB))
            ->assertOk();
    }

    public function test_the_payload_sent_for_a_carries_only_its_own_counts(): void
    {
        Http::fake(['*/v1/predict' => Http::response([
            'risk_score' => 0.42,
            'risk_flag' => true,
            'threshold' => (float) config('ml.expected_threshold'),
            'model_version' => (string) config('ml.expected_model_version'),
            'freeze_fingerprint' => (string) config('ml.expected_freeze_fingerprint'),
            'status' => 'experimental',
        ])]);

        $this->actingAs($this->hrA)->getJson(route('vacancies.operational-risk', $this->vacancyA));

        Http::assertSent(fn ($request): bool => $request->data()['applications_received_count'] === 3);
    }

    public function test_the_policy_denies_across_organizations(): void
    {
        $this->assertFalse($this->hrA->can('viewOperationalRisk', $this->vacancyB));
        $this->assertFalse($this->hrB->can('viewOperationalRisk', $this->vacancyA));
        $this->assertTrue($this->hrA->can('viewOperationalRisk', $this->vacancyA));
    }
}
