<?php

namespace Tests\Feature\Ml;

use App\Enums\InterviewOutcome;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Ml\OperationalRiskFeatureBuilder;
use App\Services\Ml\OperationalRiskFeatures;
use Carbon\CarbonInterface;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

/**
 * Construcción de las 15 features operacionales desde el dominio Laravel.
 *
 * Dos garantías bajo prueba: que los números son los que el contrato define, y
 * que **nada de lo que sale describe a una persona**.
 */
class OperationalRiskFeatureBuilderTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private OperationalRiskFeatureBuilder $builder;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->builder = app(OperationalRiskFeatureBuilder::class);
    }

    private function vacancy(array $attributes = []): Vacancy
    {
        return Vacancy::factory()->for($this->organization)->configured()->create(array_replace([
            'positions' => 2,
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
            'published_at' => now()->subDays(42),
            'target_completion_at' => now()->addDays(20)->setTime(18, 0),
        ], $attributes));
    }

    // -- contrato -----------------------------------------------------------

    public function test_it_produces_exactly_the_fifteen_contract_features(): void
    {
        $features = $this->builder->build($this->vacancy());

        $this->assertCount(15, $features->toPayload());
        $this->assertSame(
            OperationalRiskFeatures::NAMES,
            array_keys($features->toPayload())
        );
    }

    public function test_every_value_is_an_integer(): void
    {
        foreach ($this->builder->build($this->vacancy())->toPayload() as $name => $value) {
            $this->assertIsInt($value, $name);
        }
    }

    public function test_no_identifier_or_personal_attribute_leaves_the_builder(): void
    {
        $payload = $this->builder->build($this->vacancy())->toPayload();
        $serialised = json_encode($payload, JSON_THROW_ON_ERROR);

        foreach ([
            'vacancy_id', 'organization_id', 'candidate_id', 'user_id', 'evaluator_id',
            'email', 'nombre', 'name', 'edad', 'score', 'outcome', 'ranking',
        ] as $forbidden) {
            $this->assertStringNotContainsString($forbidden, $serialised);
        }
    }

    public function test_an_incomplete_feature_set_is_rejected(): void
    {
        $this->expectException(\InvalidArgumentException::class);

        OperationalRiskFeatures::fromArray(['positions_count' => 1]);
    }

    public function test_an_unexpected_feature_is_rejected(): void
    {
        $values = array_fill_keys(OperationalRiskFeatures::NAMES, 1);
        $values['candidate_id'] = 7;

        $this->expectException(\InvalidArgumentException::class);

        OperationalRiskFeatures::fromArray($values);
    }

    // -- valores ------------------------------------------------------------

    public function test_configuration_features_come_from_the_vacancy(): void
    {
        $features = $this->builder->build($this->vacancy(['positions' => 3]));

        $this->assertSame(3, $features->get('positions_count'));
        // La factoría `configured()` crea tres criterios (40/30/30).
        $this->assertSame(3, $features->get('configured_criteria_count'));
        // opens_at −40 d, closes_at −10 d.
        $this->assertSame(30, $features->get('application_window_days'));
        $this->assertSame(42, $features->get('elapsed_days_since_publication'));
    }

    public function test_the_application_window_falls_back_to_the_publication_date(): void
    {
        $features = $this->builder->build($this->vacancy([
            'opens_at' => null,
            'published_at' => now()->subDays(30),
            'closes_at' => now()->subDays(10)->startOfDay(),
        ]));

        $this->assertSame(20, $features->get('application_window_days'));
    }

    public function test_applications_and_stage_moves_are_counted(): void
    {
        $vacancy = $this->vacancy();
        $applications = $this->applications($vacancy, 3);

        // Cada postulación ya trae su transición inicial; se añade un segundo
        // movimiento a dos de ellas.
        foreach (array_slice($applications, 0, 2) as $application) {
            DB::table('application_stage_histories')->insert([
                'organization_id' => $vacancy->organization_id,
                'application_id' => $application->id,
                'from_status' => 'postulado',
                'to_status' => 'preseleccionado',
                'changed_by' => $application->candidate_id,
                'created_at' => now()->subDays(18),
            ]);
        }

        $features = $this->builder->build($vacancy);

        $this->assertSame(3, $features->get('applications_received_count'));
        // 3 transiciones iniciales + 2 movimientos posteriores.
        $this->assertSame(5, $features->get('stage_transition_count'));
    }

    public function test_stage_moves_are_not_broken_down_by_destination(): void
    {
        /* Desagregar por estado destino reintroduciría resultados individuales
           sobre personas. Solo se cuenta el total. */
        $vacancy = $this->vacancy();
        [$application] = $this->applications($vacancy, 1);

        DB::table('application_stage_histories')->insert([
            'organization_id' => $vacancy->organization_id,
            'application_id' => $application->id,
            'from_status' => 'postulado',
            'to_status' => 'descartado',
            'changed_by' => $application->candidate_id,
            'created_at' => now()->subDays(18),
        ]);
        $discarded = $this->builder->build($vacancy)->toPayload();

        DB::table('application_stage_histories')
            ->where('to_status', 'descartado')
            ->update(['to_status' => 'finalista']);

        $this->assertSame($discarded, $this->builder->build($vacancy)->toPayload());
    }

    public function test_sessions_are_counted_as_scheduled_completed_and_overdue(): void
    {
        $vacancy = $this->vacancy();
        [$first, $second, $third] = $this->applications($vacancy, 3);

        // Programada y completada.
        Evaluation::factory()->forApplication($first)->completed()->create([
            'created_at' => now()->subDays(20),
            'scheduled_at' => now()->subDays(18),
            'completed_at' => now()->subDays(17),
        ]);
        // Programada, vencida y sin completar.
        Evaluation::factory()->forApplication($second)->create([
            'created_at' => now()->subDays(20),
            'scheduled_at' => now()->subDays(5),
        ]);
        // Programada para el futuro: ni vencida ni completada.
        Evaluation::factory()->forApplication($third)->create([
            'created_at' => now()->subDays(2),
            'scheduled_at' => now()->addDays(4),
        ]);

        Interview::factory()->forApplication($first)->completed(InterviewOutcome::Recommended)->create([
            'created_at' => now()->subDays(12),
            'scheduled_at' => now()->subDays(10),
            'completed_at' => now()->subDays(9),
        ]);
        Interview::factory()->forApplication($second)->create([
            'created_at' => now()->subDays(12),
            'scheduled_at' => now()->subDays(3),
        ]);

        $features = $this->builder->build($vacancy);

        $this->assertSame(3, $features->get('evaluations_scheduled_count'));
        $this->assertSame(1, $features->get('evaluations_completed_count'));
        $this->assertSame(1, $features->get('evaluations_overdue_pending_count'));
        $this->assertSame(2, $features->get('interviews_scheduled_count'));
        $this->assertSame(1, $features->get('interviews_completed_count'));
        $this->assertSame(1, $features->get('interviews_overdue_pending_count'));
    }

    public function test_the_interview_outcome_is_never_read(): void
    {
        /* `outcome` es un juicio sobre una persona y está prohibido. Dos
           entrevistas con desenlaces opuestos deben producir el mismo vector. */
        $vacancy = $this->vacancy();
        [$first, $second] = $this->applications($vacancy, 2);

        Interview::factory()->forApplication($first)->completed(InterviewOutcome::Recommended)->create([
            'created_at' => now()->subDays(12),
            'scheduled_at' => now()->subDays(10),
            'completed_at' => now()->subDays(9),
        ]);
        $recommended = $this->builder->build($vacancy)->toPayload();

        DB::table('interviews')->update(['outcome' => InterviewOutcome::NotRecommended->value]);

        $this->assertSame($recommended, $this->builder->build($vacancy)->toPayload());
    }

    public function test_nothing_after_the_checkpoint_is_counted(): void
    {
        $vacancy = $this->vacancy();
        $checkpoint = now()->subDays(15);
        $this->applications($vacancy, 2, now()->subDays(20));
        $this->applications($vacancy, 3, now()->subDays(5));

        $features = $this->builder->build($vacancy, $checkpoint);

        $this->assertSame(2, $features->get('applications_received_count'));
    }

    public function test_days_since_last_event_uses_the_latest_closed_list_event(): void
    {
        $vacancy = $this->vacancy(['published_at' => now()->subDays(42)]);
        $this->applications($vacancy, 1, now()->subDays(6));

        $features = $this->builder->build($vacancy);

        $this->assertSame(6, $features->get('days_since_last_operational_event'));
    }

    public function test_without_events_the_last_event_is_the_publication(): void
    {
        $features = $this->builder->build($this->vacancy(['published_at' => now()->subDays(42)]));

        $this->assertSame(42, $features->get('days_since_last_operational_event'));
    }

    public function test_days_remaining_to_target_counts_whole_days(): void
    {
        $features = $this->builder->build($this->vacancy([
            'target_completion_at' => now()->addDays(20)->addHours(3),
        ]));

        $this->assertSame(20, $features->get('days_remaining_to_target'));
    }

    public function test_an_expired_target_is_not_clamped(): void
    {
        /* Recortarlo a uno fabricaría la única feature que justifica la fase.
           El valor sale negativo y quien decide qué hacer es el servicio. */
        $vacancy = $this->vacancy([
            'closes_at' => now()->subDays(40)->startOfDay(),
            'target_completion_at' => now()->subDays(5),
        ]);

        $this->assertLessThan(1, $this->builder->daysRemainingToTarget($vacancy, now()));
    }

    // -- concurrencia y multiempresa ---------------------------------------

    public function test_concurrent_vacancies_exclude_the_vacancy_itself(): void
    {
        $vacancy = $this->vacancy();
        Vacancy::factory()->for($this->organization)->count(2)->create([
            'published_at' => now()->subDays(20),
            'closed_at' => null,
        ]);
        Vacancy::factory()->for($this->organization)->create([
            'published_at' => now()->subDays(30),
            'closed_at' => now()->subDays(25),
        ]);

        $this->assertSame(2, $this->builder->build($vacancy)->get('concurrent_open_vacancies_count'));
    }

    public function test_concurrent_vacancies_ignore_other_organizations(): void
    {
        $vacancy = $this->vacancy();
        $other = Organization::factory()->create();
        Vacancy::factory()->for($other)->count(4)->create([
            'published_at' => now()->subDays(20),
            'closed_at' => null,
        ]);

        $this->assertSame(0, $this->builder->build($vacancy)->get('concurrent_open_vacancies_count'));
    }

    public function test_counts_ignore_rows_belonging_to_another_organization(): void
    {
        /* El scope global de Eloquent no actúa sin sesión iniciada, así que el
           builder filtra por organización en cada consulta. Esta prueba corre
           sin autenticar a propósito. */
        $vacancy = $this->vacancy();
        $this->applications($vacancy, 2);

        $other = Organization::factory()->create();
        $foreign = Vacancy::factory()->for($other)->create([
            'published_at' => now()->subDays(20),
        ]);
        $this->applications($foreign, 5);

        $this->assertNull(auth()->user());
        $this->assertSame(2, $this->builder->build($vacancy)->get('applications_received_count'));
    }

    /**
     * @return list<Application>
     */
    private function applications(Vacancy $vacancy, int $count, ?CarbonInterface $appliedAt = null): array
    {
        $moment = $appliedAt ?? now()->subDays(20);
        $created = [];

        for ($index = 0; $index < $count; $index++) {
            $candidate = User::factory()->candidate()->create();
            $application = Application::factory()->create([
                'organization_id' => $vacancy->organization_id,
                'vacancy_id' => $vacancy->id,
                'candidate_id' => $candidate->id,
                'applied_at' => $moment,
            ]);

            /* La factoría registra la transición inicial `null -> postulado` con
               la marca de tiempo actual. Se alinea con `applied_at` para que la
               cronología del fixture sea coherente: postular y entrar al proceso
               ocurren en el mismo instante. */
            DB::table('application_stage_histories')
                ->where('application_id', $application->id)
                ->update(['created_at' => $moment]);

            $created[] = $application;
        }

        return $created;
    }
}
