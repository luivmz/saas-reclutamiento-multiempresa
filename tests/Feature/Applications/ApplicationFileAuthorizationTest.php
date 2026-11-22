<?php

namespace Tests\Feature\Applications;

use App\Enums\ApplicationStatus;
use App\Enums\CriterionStage;
use App\Enums\InterviewOutcome;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvaluationResult;
use App\Models\Interview;
use App\Models\InterviewResult;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Testing\TestResponse;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * SEG-01: the internal application file (RF-12, `applications.show`) is for HR and Direction of the
 * vacancy's organization. The candidate follows their own application only through `mis-postulaciones`,
 * which shows convocations and never scores, observations or interview outcomes (A-21).
 *
 * All fixture data is fictitious. The SEG01-* markers make any leak of internal text detectable in the
 * HTTP response.
 */
class ApplicationFileAuthorizationTest extends TestCase
{
    use RefreshDatabase;

    private const INTERNAL_MARKERS = [
        'SEG01-HISTORY-COMMENT',
        'SEG01-EVALUATION-OBSERVATIONS',
        'SEG01-EVALUATION-RESULT-COMMENT',
        'SEG01-INTERVIEW-OBSERVATIONS',
        'SEG01-INTERVIEW-RESULT-COMMENT',
        'SEG01 Evaluador Ficticio',
        'SEG01 RRHH Ficticio',
    ];

    private Organization $organization;

    private User $hr;

    private User $evaluator;

    private User $owner;

    private Application $application;

    private Evaluation $evaluation;

    private Interview $interview;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create(['name' => 'SEG01 RRHH Ficticio']);
        $this->evaluator = User::factory()->evaluator($this->organization)->create(['name' => 'SEG01 Evaluador Ficticio']);
        $this->owner = User::factory()->candidate()->create();

        $vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->application = Application::factory()->for($vacancy)->forCandidate($this->owner)->inInterview()->create();

        (new ApplicationStageHistory)->forceFill([
            'organization_id' => $this->organization->id,
            'application_id' => $this->application->id,
            'from_status' => ApplicationStatus::Submitted,
            'to_status' => ApplicationStatus::Shortlisted,
            'changed_by' => $this->hr->id,
            'comment' => 'SEG01-HISTORY-COMMENT',
        ])->save();

        $evaluationCriterion = EvaluationCriterion::factory()->create(['vacancy_id' => $vacancy->id, 'stage' => CriterionStage::Evaluation]);
        $interviewCriterion = EvaluationCriterion::factory()->create(['vacancy_id' => $vacancy->id, 'stage' => CriterionStage::Interview]);

        $this->evaluation = Evaluation::factory()->forApplication($this->application)->assignedTo($this->evaluator)->completed()
            ->create(['observations' => 'SEG01-EVALUATION-OBSERVATIONS']);
        (new EvaluationResult)->forceFill([
            'organization_id' => $this->organization->id,
            'evaluation_id' => $this->evaluation->id,
            'evaluation_criterion_id' => $evaluationCriterion->id,
            'score' => 17.5,
            'comment' => 'SEG01-EVALUATION-RESULT-COMMENT',
        ])->save();

        $this->interview = Interview::factory()->forApplication($this->application)->assignedTo($this->evaluator)
            ->completed(InterviewOutcome::NotRecommended)
            ->create(['observations' => 'SEG01-INTERVIEW-OBSERVATIONS']);
        (new InterviewResult)->forceFill([
            'organization_id' => $this->organization->id,
            'interview_id' => $this->interview->id,
            'evaluation_criterion_id' => $interviewCriterion->id,
            'score' => 9.0,
            'comment' => 'SEG01-INTERVIEW-RESULT-COMMENT',
        ])->save();
    }

    public function test_rf12_seg01_candidate_owner_cannot_open_the_internal_application_file(): void
    {
        $response = $this->actingAs($this->owner)->get(route('applications.show', $this->application));

        $this->assertNoInternalData($response);
        $response->assertForbidden();
    }

    public function test_rf12_seg01_another_candidate_cannot_open_the_internal_application_file(): void
    {
        $response = $this->actingAs(User::factory()->candidate()->create())->get(route('applications.show', $this->application));

        $this->assertNoInternalData($response);
        $response->assertForbidden();
    }

    public function test_rf12_seg01_hr_and_approver_of_the_organization_keep_the_internal_file(): void
    {
        $approver = User::factory()->approver($this->organization)->create();

        foreach ([$this->hr, $approver] as $staff) {
            $this->actingAs($staff)
                ->get(route('applications.show', $this->application))
                ->assertOk()
                ->assertInertia(fn (AssertableInertia $page) => $page
                    ->component('applications/show')
                    ->where('application.id', $this->application->id)
                    ->has('application.candidate')
                    ->where('history.1.comment', 'SEG01-HISTORY-COMMENT')
                    ->where('assessments.evaluations.0.observations', 'SEG01-EVALUATION-OBSERVATIONS')
                    ->where('assessments.evaluations.0.results.0.comment', 'SEG01-EVALUATION-RESULT-COMMENT')
                    ->where('assessments.interviews.0.observations', 'SEG01-INTERVIEW-OBSERVATIONS')
                    ->has('assessments.interviews.0.outcome'));
        }
    }

    public function test_rf12_seg01_staff_of_another_organization_receives_no_data(): void
    {
        $other = Organization::factory()->create();

        foreach ([User::factory()->hr($other)->create(), User::factory()->approver($other)->create()] as $staff) {
            $response = $this->actingAs($staff)->get(route('applications.show', $this->application));

            $this->assertNoInternalData($response);
            $response->assertNotFound();
        }
    }

    public function test_rf12_seg01_requester_and_evaluator_get_no_internal_file(): void
    {
        foreach ([User::factory()->requester($this->organization)->create(), $this->evaluator] as $user) {
            $response = $this->actingAs($user)->get(route('applications.show', $this->application));

            $this->assertNoInternalData($response, $user);
            $response->assertForbidden();
        }
    }

    public function test_rf19_seg01_assigned_evaluator_keeps_their_session_pages(): void
    {
        $this->actingAs($this->evaluator)->get(route('evaluations.show', $this->evaluation))
            ->assertOk()->assertInertia(fn (AssertableInertia $page) => $page->component('assessments/show'));
        $this->actingAs($this->evaluator)->get(route('interviews.show', $this->interview))
            ->assertOk()->assertInertia(fn (AssertableInertia $page) => $page->component('assessments/show'));
    }

    public function test_rf11_rf17_seg01_candidate_keeps_their_own_application_and_convocations_only(): void
    {
        $this->assertTrue($this->owner->can('view', $this->application), 'The candidate keeps viewing their own application.');

        $this->actingAs($this->owner)->get(route('candidate.applications.index'))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page->component('candidate/applications/index')->has('applications.data', 1));

        $response = $this->actingAs($this->owner)->get(route('candidate.applications.show', $this->application));

        $response->assertOk()->assertInertia(fn (AssertableInertia $page) => $page
            ->component('candidate/applications/show')
            ->where('application.id', $this->application->id)
            ->missing('application.candidate')
            ->missing('history')
            ->missing('assessments')
            ->has('convocations', 2)
            ->has('convocations.0', fn (AssertableInertia $convocation) => $convocation
                ->hasAll(['key', 'title', 'scheduled_at', 'duration_minutes', 'modality', 'location', 'instructions', 'status'])
                ->missing('observations')
                ->missing('outcome')
                ->missing('results')
                ->missing('evaluator')));
        $this->assertNoInternalData($response);
    }

    public function test_seg01_guest_is_sent_to_login(): void
    {
        $this->get(route('applications.show', $this->application))->assertRedirect(route('login'));
    }

    /**
     * No internal marker reaches the response. The acting user's own name is not a leak: shared props may show it.
     */
    private function assertNoInternalData(TestResponse $response, ?User $actor = null): void
    {
        foreach (self::INTERNAL_MARKERS as $marker) {
            if ($actor !== null && $marker === $actor->name) {
                continue;
            }
            $response->assertDontSee($marker, false);
        }
    }
}
