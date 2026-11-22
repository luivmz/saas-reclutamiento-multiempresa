<?php

namespace Tests\Feature\Evidence;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evidence\EvidenceService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * EXPERIMENTAL (exp/evidencias-ml02, F37-UX-03). Where the evidence flow is entered: the application file (HR,
 * Direction) and the assigned session (evaluator). The link follows the flag and the policy; with the flag off no
 * entry point shows it and the eight routes answer 404 without inserting anything.
 */
class EvidenceEntryPointsTest extends TestCase
{
    use RefreshDatabase;

    private User $hr;

    private User $director;

    private User $evaluator;

    private Application $application;

    private Evaluation $evaluation;

    private EvaluationCriterion $criterion;

    protected function setUp(): void
    {
        parent::setUp();
        config()->set('experimental.evidencias', true);

        $org = Organization::factory()->create();
        $this->hr = User::factory()->hr($org)->create();
        $this->director = User::factory()->approver($org)->create();
        $this->evaluator = User::factory()->evaluator($org)->create();

        $vacancy = Vacancy::factory()->published()->state(['organization_id' => $org->id])->create();
        $this->criterion = EvaluationCriterion::factory()->state(['vacancy_id' => $vacancy->id, 'position' => 0])->create();
        $this->application = Application::factory()->state(['vacancy_id' => $vacancy->id])->create();
        $this->evaluation = Evaluation::factory()->forApplication($this->application)->assignedTo($this->evaluator)->state(['scheduled_by' => $this->hr->id])->create();
    }

    public function test_hr_and_direction_find_the_evidence_link_in_the_application_file(): void
    {
        foreach ([$this->hr, $this->director] as $user) {
            $this->actingAs($user)->get(route('applications.show', $this->application))
                ->assertOk()
                ->assertInertia(fn (AssertableInertia $page) => $page
                    ->component('applications/show')
                    ->where('can.viewEvidence', true));
        }
    }

    public function test_the_assigned_evaluator_finds_it_in_their_session(): void
    {
        $this->actingAs($this->evaluator)->get(route('evaluations.show', $this->evaluation))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('assessments/show')
                ->where('can.viewEvidence', true));
    }

    public function test_with_the_flag_off_no_entry_point_shows_it_and_every_route_answers_404(): void
    {
        $this->actingAs($this->hr);
        $item = app(EvidenceService::class)->register($this->hr, $this->application, EvidenceType::Certificate, EvidenceSource::SubmittedDocument, '[SINTÉTICO] Constancia ficticia previa.');
        config()->set('experimental.evidencias', false);
        $rows = [EvidenceItem::query()->count(), EvidenceEvent::query()->count()];

        $this->actingAs($this->hr)->get(route('applications.show', $this->application))
            ->assertInertia(fn (AssertableInertia $page) => $page->where('can.viewEvidence', false));
        $this->actingAs($this->evaluator)->get(route('evaluations.show', $this->evaluation))
            ->assertInertia(fn (AssertableInertia $page) => $page->where('can.viewEvidence', false));

        $this->actingAs($this->hr);
        foreach ([
            $this->get(route('applications.evidence.index', $this->application)),
            $this->get(route('applications.evidence.history', $this->application)),
            $this->post(route('applications.evidence.store', $this->application), ['type' => 'certificado', 'source' => 'documento_presentado', 'description' => '[SINTÉTICO] x']),
            $this->post(route('evidence.link', $item), ['criterion_id' => $this->criterion->id]),
            $this->delete(route('evidence.unlink', [$item, $this->criterion->id])),
            $this->post(route('evidence.review', $item)),
            $this->post(route('evidence.correct', $item), ['source' => 'documento_presentado', 'description' => '[SINTÉTICO] x']),
            $this->post(route('evidence.withdraw', $item), ['reason' => '[SINTÉTICO] x']),
        ] as $response) {
            $response->assertNotFound();
        }

        $this->assertSame($rows, [EvidenceItem::query()->count(), EvidenceEvent::query()->count()]);
    }
}
