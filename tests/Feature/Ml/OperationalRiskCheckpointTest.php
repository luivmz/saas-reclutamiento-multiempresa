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
use Carbon\CarbonInterface;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

/**
 * El checkpoint científico, con fechas explícitas.
 *
 * El experimento de la Fase 15B observó siempre el mismo punto:
 *
 *     checkpoint = inicio del día siguiente a closes_at, en America/Lima
 *
 * Esta suite separa dos cosas que conviene no mezclar:
 *
 * - **Reconstrucción del vector.** Depende solo del checkpoint, así que es
 *   determinista y reproducible para siempre: los eventos posteriores no
 *   existen para el modelo.
 * - **Elegibilidad para inferir.** Depende del momento de la consulta. Que el
 *   vector sea reconstruible no significa que preguntar tenga sentido.
 *
 * Las fechas son fijas (`Carbon::setTestNow`) para que el lector pueda seguir
 * la aritmética sin calcular nada.
 */
class OperationalRiskCheckpointTest extends TestCase
{
    use RefreshDatabase;

    /** Cierre de postulaciones del caso base. */
    private const CLOSES_AT = '2026-06-10';

    /** Checkpoint aprobado: inicio del día siguiente. */
    private const CHECKPOINT = '2026-06-11 00:00:00';

    private Organization $organization;

    private OperationalRiskFeatureBuilder $builder;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->builder = app(OperationalRiskFeatureBuilder::class);

        config()->set('ml.enabled', true);
        config()->set('ml.base_url', 'http://ml-service.test');
        config()->set('ml.retries', 0);
    }

    protected function tearDown(): void
    {
        Carbon::setTestNow();

        parent::tearDown();
    }

    private function service(): OperationalRiskService
    {
        return app(OperationalRiskService::class);
    }

    private function vacancy(array $attributes = []): Vacancy
    {
        return Vacancy::factory()->for($this->organization)->configured()->create(array_replace([
            'opens_at' => '2026-05-11',
            'closes_at' => self::CLOSES_AT,
            'published_at' => '2026-05-09 09:00:00',
            'target_completion_at' => '2026-07-15 18:00:00',
            'positions' => 2,
        ], $attributes));
    }

    private function applicationAt(Vacancy $vacancy, string $moment): Application
    {
        $application = Application::factory()->create([
            'organization_id' => $vacancy->organization_id,
            'vacancy_id' => $vacancy->id,
            'candidate_id' => User::factory()->candidate()->create()->id,
            'applied_at' => $moment,
        ]);

        // La factoría registra la transición inicial con la hora actual; se
        // alinea con la postulación para que la cronología sea coherente.
        DB::table('application_stage_histories')
            ->where('application_id', $application->id)
            ->update(['created_at' => $moment]);

        return $application;
    }

    private function checkpoint(Vacancy $vacancy): CarbonInterface
    {
        return $this->service()->checkpointFor($vacancy);
    }

    // -- el instante ---------------------------------------------------------

    public function test_the_checkpoint_is_the_start_of_the_day_after_the_close(): void
    {
        $checkpoint = $this->checkpoint($this->vacancy());

        $this->assertSame(self::CHECKPOINT, $checkpoint->toDateTimeString());
        $this->assertSame('America/Lima', $checkpoint->timezoneName);
        $this->assertSame(0, $checkpoint->hour + $checkpoint->minute + $checkpoint->second);
    }

    // -- reconstrucción del vector ------------------------------------------

    public function test_only_events_up_to_the_checkpoint_enter_the_vector(): void
    {
        $vacancy = $this->vacancy();

        // Tres momentos, deliberadamente alrededor de la frontera.
        $this->applicationAt($vacancy, '2026-06-05 10:00:00');   // antes
        $this->applicationAt($vacancy, self::CHECKPOINT);        // justo en el checkpoint
        $this->applicationAt($vacancy, '2026-06-11 00:00:01');   // un segundo después
        $this->applicationAt($vacancy, '2026-06-20 12:00:00');   // días después

        $features = $this->builder->build($vacancy, $this->checkpoint($vacancy));

        /* El contrato usa `applied_at <= checkpoint`, así que el evento que cae
           exactamente en el checkpoint entra y el de un segundo después no. */
        $this->assertSame(2, $features->get('applications_received_count'));
        $this->assertSame(2, $features->get('stage_transition_count'));
    }

    public function test_sessions_respect_the_same_boundary(): void
    {
        $vacancy = $this->vacancy();
        [$first, $second] = [
            $this->applicationAt($vacancy, '2026-06-01 09:00:00'),
            $this->applicationAt($vacancy, '2026-06-02 09:00:00'),
        ];

        // Creada antes y completada antes: cuenta en ambas.
        Evaluation::factory()->forApplication($first)->completed()->create([
            'created_at' => '2026-06-03 09:00:00',
            'scheduled_at' => '2026-06-05 09:00:00',
            'completed_at' => '2026-06-06 09:00:00',
        ]);
        // Creada antes, completada DESPUÉS del checkpoint: cuenta como
        // programada y vencida, nunca como completada.
        Evaluation::factory()->forApplication($second)->completed()->create([
            'created_at' => '2026-06-04 09:00:00',
            'scheduled_at' => '2026-06-07 09:00:00',
            'completed_at' => '2026-06-15 09:00:00',
        ]);
        // Creada después del checkpoint: no existe para el modelo.
        Interview::factory()->forApplication($first)->create([
            'created_at' => '2026-06-14 09:00:00',
            'scheduled_at' => '2026-06-18 09:00:00',
        ]);

        $features = $this->builder->build($vacancy, $this->checkpoint($vacancy));

        $this->assertSame(2, $features->get('evaluations_scheduled_count'));
        $this->assertSame(1, $features->get('evaluations_completed_count'));
        $this->assertSame(1, $features->get('evaluations_overdue_pending_count'));
        $this->assertSame(0, $features->get('interviews_scheduled_count'));
    }

    public function test_the_vector_is_identical_whenever_it_is_rebuilt(): void
    {
        /* La reconstrucción no depende de cuándo se pregunte. Es lo que hace
           auditable una predicción meses después. */
        $vacancy = $this->vacancy();
        $this->applicationAt($vacancy, '2026-06-05 10:00:00');

        Carbon::setTestNow('2026-06-11 08:00:00');
        $atCheckpoint = $this->builder->build($vacancy, $this->checkpoint($vacancy))->toPayload();

        $this->applicationAt($vacancy, '2026-06-25 10:00:00');
        Carbon::setTestNow('2026-09-30 08:00:00');
        $monthsLater = $this->builder->build($vacancy->fresh(), $this->checkpoint($vacancy))->toPayload();

        $this->assertSame($atCheckpoint, $monthsLater);
        $this->assertSame(1, $monthsLater['applications_received_count']);
    }

    public function test_days_remaining_is_measured_from_the_checkpoint(): void
    {
        // 2026-06-11 → 2026-07-15: 34 días completos.
        $features = $this->builder->build($this->vacancy(), $this->checkpoint($this->vacancy()));

        $this->assertSame(34, $features->get('days_remaining_to_target'));
    }

    // -- ML-FEAT-18: vacantes concurrentes ----------------------------------

    public function test_concurrent_open_vacancies_is_reconstructed_at_the_checkpoint(): void
    {
        /* Caso histórico explícito. El conteo es el estado **en el checkpoint**,
           no el estado actual de la tabla. */
        $target = $this->vacancy();

        // B: abierta antes del checkpoint y cerrada después → contaba entonces.
        Vacancy::factory()->for($this->organization)->create([
            'published_at' => '2026-05-01 09:00:00',
            'closed_at' => '2026-06-20 09:00:00',
            'opens_at' => '2026-05-01',
            'closes_at' => '2026-06-15',
        ]);
        // C: cerrada antes del checkpoint → no contaba.
        Vacancy::factory()->for($this->organization)->create([
            'published_at' => '2026-04-01 09:00:00',
            'closed_at' => '2026-05-20 09:00:00',
            'opens_at' => '2026-04-01',
            'closes_at' => '2026-05-15',
        ]);
        // D: publicada después del checkpoint → todavía no existía.
        Vacancy::factory()->for($this->organization)->create([
            'published_at' => '2026-06-25 09:00:00',
            'closed_at' => null,
            'opens_at' => '2026-06-25',
            'closes_at' => '2026-07-25',
        ]);
        // E: abierta antes y todavía abierta → contaba.
        Vacancy::factory()->for($this->organization)->create([
            'published_at' => '2026-05-05 09:00:00',
            'closed_at' => null,
            'opens_at' => '2026-05-05',
            'closes_at' => '2026-06-30',
        ]);

        $features = $this->builder->build($target, $this->checkpoint($target));

        // Solo B y E. La propia vacante nunca se cuenta.
        $this->assertSame(2, $features->get('concurrent_open_vacancies_count'));
    }

    // -- ML-FEAT-17: último evento operacional ------------------------------

    public function test_the_last_operational_event_uses_the_closed_list(): void
    {
        $vacancy = $this->vacancy();
        $application = $this->applicationAt($vacancy, '2026-06-02 09:00:00');

        // Evento permitido más reciente antes del checkpoint: 2026-06-08.
        Evaluation::factory()->forApplication($application)->completed()->create([
            'created_at' => '2026-06-04 09:00:00',
            'scheduled_at' => '2026-06-06 09:00:00',
            'completed_at' => '2026-06-08 09:00:00',
        ]);

        $features = $this->builder->build($vacancy, $this->checkpoint($vacancy));

        // 2026-06-08 → 2026-06-11: 2 días completos y 15 horas.
        $this->assertSame(2, $features->get('days_since_last_operational_event'));
    }

    public function test_an_event_after_the_checkpoint_does_not_become_the_latest(): void
    {
        $vacancy = $this->vacancy();
        $application = $this->applicationAt($vacancy, '2026-06-02 09:00:00');
        Evaluation::factory()->forApplication($application)->completed()->create([
            'created_at' => '2026-06-04 09:00:00',
            'scheduled_at' => '2026-06-06 09:00:00',
            'completed_at' => '2026-06-08 09:00:00',
        ]);
        $before = $this->builder->build($vacancy, $this->checkpoint($vacancy))->toPayload();

        // Actividad posterior: no puede mover el máximo.
        $this->applicationAt($vacancy, '2026-06-30 09:00:00');

        $this->assertSame(
            $before,
            $this->builder->build($vacancy->fresh(), $this->checkpoint($vacancy))->toPayload()
        );
    }

    public function test_a_column_outside_the_closed_list_does_not_affect_the_feature(): void
    {
        /* `invitation_sent_at` es un timestamp real de la tabla y **no** está en
           la lista cerrada del contrato. Moverlo no puede cambiar nada. */
        $vacancy = $this->vacancy();
        $application = $this->applicationAt($vacancy, '2026-06-02 09:00:00');
        Evaluation::factory()->forApplication($application)->create([
            'created_at' => '2026-06-04 09:00:00',
            'scheduled_at' => '2026-06-06 09:00:00',
            'invitation_sent_at' => '2026-06-04 09:00:00',
        ]);
        $before = $this->builder->build($vacancy, $this->checkpoint($vacancy))->toPayload();

        DB::table('evaluations')->update(['invitation_sent_at' => '2026-06-10 23:00:00']);

        $this->assertSame(
            $before,
            $this->builder->build($vacancy->fresh(), $this->checkpoint($vacancy))->toPayload()
        );
    }

    public function test_without_events_the_fallback_is_the_publication(): void
    {
        // Publicada 2026-05-09 → checkpoint 2026-06-11: 32 días.
        $features = $this->builder->build($this->vacancy(), $this->checkpoint($this->vacancy()));

        $this->assertSame(32, $features->get('days_since_last_operational_event'));
    }

    // -- elegibilidad: distinta de la reconstrucción ------------------------

    public function test_reconstruction_and_eligibility_are_separate_questions(): void
    {
        /* El vector se reconstruye siempre; la decisión de mostrar una
           predicción depende del momento de la consulta. */
        $vacancy = $this->vacancy();
        $this->applicationAt($vacancy, '2026-06-05 10:00:00');

        // Vector reconstruible en cualquier momento.
        Carbon::setTestNow('2026-12-31 10:00:00');
        $vector = $this->builder->build($vacancy, $this->checkpoint($vacancy))->toPayload();
        $this->assertSame(1, $vector['applications_received_count']);

        // Pero a esa altura el plazo ya venció: no se estima.
        Http::fake();
        $assessment = $this->service()->assess($vacancy);

        $this->assertSame(OperationalRiskService::REASON_QUERY_AFTER_TARGET, $assessment->reason);
        $this->assertNull($assessment->score);
        Http::assertNothingSent();
    }

    public function test_at_the_checkpoint_the_query_is_eligible(): void
    {
        Carbon::setTestNow('2026-06-11 09:00:00');
        Http::fake(['*/v1/predict' => Http::response([
            'risk_score' => 0.42,
            'risk_flag' => true,
            'threshold' => (float) config('ml.expected_threshold'),
            'model_version' => (string) config('ml.expected_model_version'),
            'freeze_fingerprint' => (string) config('ml.expected_freeze_fingerprint'),
            'status' => 'experimental',
        ])]);

        $assessment = $this->service()->assess($this->vacancy());

        $this->assertTrue($assessment->isPredictive());
    }

    public function test_a_second_before_the_checkpoint_the_query_is_not_eligible(): void
    {
        Carbon::setTestNow('2026-06-10 23:59:59');
        Http::fake();

        $assessment = $this->service()->assess($this->vacancy());

        $this->assertSame(OperationalRiskService::REASON_CHECKPOINT_NOT_REACHED, $assessment->reason);
        Http::assertNothingSent();
    }

    public function test_a_closed_vacancy_is_not_eligible_even_inside_the_window(): void
    {
        Carbon::setTestNow('2026-06-20 09:00:00');
        Http::fake();

        $vacancy = $this->vacancy(['closed_at' => '2026-06-18 09:00:00']);

        $this->assertSame(
            OperationalRiskService::REASON_VACANCY_CLOSED,
            $this->service()->assess($vacancy)->reason
        );
        Http::assertNothingSent();
    }

    public function test_a_target_that_does_not_survive_the_checkpoint_is_not_eligible(): void
    {
        Carbon::setTestNow('2026-06-11 09:00:00');
        Http::fake();

        // El plazo cae el mismo día del checkpoint: quedan 0 días completos.
        $vacancy = $this->vacancy(['target_completion_at' => '2026-06-11 20:00:00']);

        $this->assertSame(
            OperationalRiskService::REASON_TARGET_BEFORE_CHECKPOINT,
            $this->service()->assess($vacancy)->reason
        );
        Http::assertNothingSent();
    }
}
