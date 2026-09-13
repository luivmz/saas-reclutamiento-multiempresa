<?php

namespace Tests\Feature\Assessments;

use App\Enums\ApplicationStatus;
use App\Enums\AssessmentStatus;
use App\Enums\AuditAction;
use App\Enums\CriterionStage;
use App\Enums\InterviewOutcome;
use App\Enums\VacancyClosureType;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Interview;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\AssessmentAssignedNotification;
use App\Notifications\AssessmentConvocationNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class InterviewTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private User $hr;

    private User $evaluator;

    private Vacancy $vacancy;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->evaluator = User::factory()->evaluator($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
    }

    /**
     * @return array<string, mixed>
     */
    private function resultPayload(float $score = 17): array
    {
        $criterion = $this->vacancy->criteria()->where('stage', CriterionStage::Interview)->sole();

        return [
            'scores' => [$criterion->id => ['score' => $score, 'comment' => 'Comunicación clara.']],
            'outcome' => 'recomendado',
            'observations' => 'Entrevista realizada; candidato con buena disposición.',
        ];
    }

    public function test_rf18_hr_schedules_interview_and_notifies_candidate_and_interviewer(): void
    {
        Notification::fake();
        $application = Application::factory()->for($this->vacancy)->inEvaluation()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.interviews.store', $application), [
                'evaluator_id' => $this->evaluator->id,
                'modality' => 'virtual',
                'location' => 'https://reuniones.example.test/sala-demo',
                'scheduled_at' => now()->addDays(2)->setTime(15, 30)->format('Y-m-d H:i'),
                'duration_minutes' => 30,
            ])
            ->assertSessionHasNoErrors();

        $interview = Interview::query()->sole();
        $this->assertSame(AssessmentStatus::Scheduled, $interview->status);
        $this->assertSame(ApplicationStatus::Interview, $application->fresh()->status);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::InterviewScheduled)->exists());

        Notification::assertSentTo($application->candidate, AssessmentConvocationNotification::class);
        Notification::assertSentTo($this->evaluator, AssessmentAssignedNotification::class);
    }

    public function test_rf18_submitted_application_cannot_be_interviewed(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();

        $this->actingAs($this->hr)
            ->post(route('applications.interviews.store', $application), [
                'evaluator_id' => $this->evaluator->id,
                'modality' => 'presencial',
                'location' => 'Oficina de RR. HH.',
                'scheduled_at' => now()->addDay()->format('Y-m-d H:i'),
            ])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(0, Interview::query()->count());
    }

    public function test_rf19_assigned_evaluator_records_interview_and_result(): void
    {
        $interview = Interview::factory()->forApplication(Application::factory()->for($this->vacancy)->inInterview()->create())->assignedTo($this->evaluator)->create();

        $this->actingAs($this->evaluator)
            ->post(route('interviews.results.store', $interview), $this->resultPayload())
            ->assertSessionHasNoErrors();

        $interview->refresh();
        $this->assertSame(AssessmentStatus::Completed, $interview->status);
        $this->assertSame(InterviewOutcome::Recommended, $interview->outcome);
        $this->assertSame('Entrevista realizada; candidato con buena disposición.', $interview->observations);
        $this->assertSame(1, $interview->results()->count());
        $this->assertEquals(17.0, $interview->results()->sole()->score);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::InterviewResultRecorded)->exists());
    }

    public function test_rf19_outcome_and_observations_are_required(): void
    {
        $interview = Interview::factory()->forApplication(Application::factory()->for($this->vacancy)->inInterview()->create())->assignedTo($this->evaluator)->create();

        $this->actingAs($this->evaluator)
            ->post(route('interviews.results.store', $interview), [...$this->resultPayload(), 'outcome' => '', 'observations' => ''])
            ->assertSessionHasErrors(['outcome', 'observations']);

        $this->assertSame(AssessmentStatus::Scheduled, $interview->fresh()->status);
    }

    public function test_rf20_interview_score_out_of_range_is_rejected(): void
    {
        $interview = Interview::factory()->forApplication(Application::factory()->for($this->vacancy)->inInterview()->create())->assignedTo($this->evaluator)->create();
        $payload = $this->resultPayload(score: -1);
        $criterionId = array_key_first($payload['scores']);

        $this->actingAs($this->evaluator)
            ->post(route('interviews.results.store', $interview), $payload)
            ->assertSessionHasErrors("scores.{$criterionId}.score");

        $this->assertSame(0, $interview->results()->count());
    }

    public function test_results_are_blocked_once_the_vacancy_is_closed(): void
    {
        $closed = Vacancy::factory()->for($this->organization)->configured()->closed(VacancyClosureType::Deserted)->create();
        $this->vacancy = $closed;
        $interview = Interview::factory()->forApplication(Application::factory()->for($closed)->inInterview()->create())->assignedTo($this->evaluator)->create();

        $this->actingAs($this->evaluator)
            ->post(route('interviews.results.store', $interview), $this->resultPayload())
            ->assertSessionHasErrors('workflow');

        $this->assertSame(AssessmentStatus::Scheduled, $interview->fresh()->status);
    }

    public function test_evaluator_of_another_organization_cannot_access_the_interview(): void
    {
        $interview = Interview::factory()->forApplication(Application::factory()->for($this->vacancy)->inInterview()->create())->assignedTo($this->evaluator)->create();
        $foreign = User::factory()->evaluator(Organization::factory()->create())->create();

        $this->actingAs($foreign)->get(route('interviews.show', $interview))->assertNotFound();
        $this->actingAs($foreign)->post(route('interviews.results.store', $interview), $this->resultPayload())->assertNotFound();
    }
}
