<?php

namespace Tests\Feature\Evidence;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Enums\VacancyClosureType;
use App\Enums\VacancyStatus;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evidence\EvidenceService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Testing\TestResponse;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * EXPERIMENTAL (exp/evidencias-ml02, F37-UX-01). The process closes while a writer still has the evidence page open:
 * the form posts after the closure. The write is refused without inserting anything (R-08), and the writer gets back
 * to the page with an understandable message instead of a bare 403. Whoever could not write with the process open
 * keeps getting 403/404: the message never widens who learns anything about the application.
 */
class EvidenceClosedProcessTest extends TestCase
{
    use RefreshDatabase;

    private Organization $org;

    private User $hr;

    private User $evaluator;

    private Vacancy $vacancy;

    private Application $application;

    private EvaluationCriterion $criterion;

    private EvidenceItem $certificate;

    private EvidenceItem $observation;

    protected function setUp(): void
    {
        parent::setUp();
        config()->set('experimental.evidencias', true);

        $this->org = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->org)->create();
        $this->evaluator = User::factory()->evaluator($this->org)->create();

        $this->vacancy = Vacancy::factory()->published()->state(['organization_id' => $this->org->id])->create();
        $this->criterion = EvaluationCriterion::factory()->state(['vacancy_id' => $this->vacancy->id, 'name' => 'Planificación', 'position' => 0])->create();
        $this->application = Application::factory()->state(['vacancy_id' => $this->vacancy->id])->create();
        Evaluation::factory()->forApplication($this->application)->assignedTo($this->evaluator)->state(['scheduled_by' => $this->hr->id])->create();

        $service = app(EvidenceService::class);
        $this->actingAs($this->hr);
        $this->certificate = $service->register($this->hr, $this->application, EvidenceType::Certificate, EvidenceSource::SubmittedDocument, '[SINTÉTICO] Constancia ficticia de planificación.');
        $this->actingAs($this->evaluator);
        $this->observation = $service->register($this->evaluator, $this->application, EvidenceType::Observation, EvidenceSource::AssignedSession, '[SINTÉTICO] Observación ficticia de la sesión.');

        // The closure lands after the writer loaded the page (status written directly: the closure flow itself is
        // covered by VacancyClosureService and EvidenceClosureConcurrencyTest).
        DB::table('vacancies')->where('id', $this->vacancy->id)->update([
            'status' => VacancyStatus::Closed->value,
            'closed_at' => now(),
            'closure_type' => VacancyClosureType::Deserted->value,
        ]);
    }

    public function test_hr_writes_after_the_closure_come_back_with_the_closure_message_and_insert_nothing(): void
    {
        $page = route('applications.evidence.index', $this->application);
        $rows = $this->rows();

        foreach ($this->writes($this->certificate) as $label => $send) {
            $response = $send($this->actingAs($this->hr)->from($page));

            $response->assertRedirect($page);
            $response->assertSessionHasErrors(['workflow' => EvidenceService::CLOSED_MESSAGE]);
            $this->assertSame($rows, $this->rows(), "{$label}: una escritura tras el cierre no debe insertar filas");
        }
    }

    public function test_the_assigned_evaluator_gets_the_same_message_on_their_own_observation(): void
    {
        $page = route('applications.evidence.index', $this->application);
        $rows = $this->rows();

        $this->actingAs($this->evaluator)->from($page)
            ->post(route('applications.evidence.store', $this->application), $this->observationBody())
            ->assertRedirect($page)
            ->assertSessionHasErrors(['workflow' => EvidenceService::CLOSED_MESSAGE]);
        $this->actingAs($this->evaluator)->from($page)
            ->post(route('evidence.correct', $this->observation), ['source' => 'sesion_asignada', 'description' => '[SINTÉTICO] Corrección ficticia.'])
            ->assertRedirect($page)
            ->assertSessionHasErrors(['workflow' => EvidenceService::CLOSED_MESSAGE]);

        $this->assertSame($rows, $this->rows());
    }

    public function test_who_could_not_write_with_the_process_open_still_gets_403_or_404(): void
    {
        $rows = $this->rows();
        $other = Organization::factory()->create();
        $outsiders = [
            'dirección' => [User::factory()->approver($this->org)->create(), 403],
            'evaluador no asignado' => [User::factory()->evaluator($this->org)->create(), 403],
            'solicitante' => [User::factory()->requester($this->org)->create(), 403],
            'RR. HH. de otra organización' => [User::factory()->hr($other)->create(), 404],
        ];

        foreach ($outsiders as $label => [$user, $status]) {
            $response = $this->actingAs($user)->post(route('applications.evidence.store', $this->application), $this->observationBody());
            $this->assertSame($status, $response->getStatusCode(), "{$label}: registrar");
            $response->assertSessionMissing('errors');

            $response = $this->actingAs($user)->post(route('evidence.review', $this->certificate));
            $this->assertSame($status, $response->getStatusCode(), "{$label}: revisar");
        }

        $this->assertSame($rows, $this->rows());
    }

    public function test_the_page_of_a_closed_process_is_read_only_for_every_writer(): void
    {
        foreach ([$this->hr, $this->evaluator] as $user) {
            $this->actingAs($user)->get(route('applications.evidence.index', $this->application))
                ->assertOk()
                ->assertInertia(fn (AssertableInertia $page) => $page
                    ->where('application.vacancy.closed', true)
                    ->where('can.create', false)
                    ->has('records', 2)
                    ->where('records.0.can', ['link' => false, 'review' => false, 'correct' => false, 'withdraw' => false])
                    ->where('records.1.can', ['link' => false, 'review' => false, 'correct' => false, 'withdraw' => false]));
        }
    }

    /**
     * @return array<string, callable(self): TestResponse>
     */
    private function writes(EvidenceItem $item): array
    {
        return [
            'registrar' => fn (self $t) => $t->post(route('applications.evidence.store', $this->application), [
                'type' => 'certificado', 'source' => 'documento_presentado', 'description' => '[SINTÉTICO] Otra constancia ficticia.',
            ]),
            'enlazar' => fn (self $t) => $t->post(route('evidence.link', $item), ['criterion_id' => $this->criterion->id]),
            'revisar' => fn (self $t) => $t->post(route('evidence.review', $item)),
            'corregir' => fn (self $t) => $t->post(route('evidence.correct', $item), ['source' => 'documento_presentado', 'description' => '[SINTÉTICO] Corrección ficticia.']),
            'retirar' => fn (self $t) => $t->post(route('evidence.withdraw', $item), ['reason' => '[SINTÉTICO] Motivo ficticio.']),
        ];
    }

    /**
     * @return array<string, string>
     */
    private function observationBody(): array
    {
        return ['type' => 'observacion', 'source' => 'sesion_asignada', 'description' => '[SINTÉTICO] Observación ficticia nueva.'];
    }

    /**
     * @return list<int>
     */
    private function rows(): array
    {
        return [
            EvidenceItem::query()->withoutGlobalScopes()->count(),
            EvidenceEvent::query()->withoutGlobalScopes()->count(),
            AuditLog::query()->withoutGlobalScopes()->count(),
        ];
    }
}
