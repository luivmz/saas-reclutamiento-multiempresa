<?php

namespace Tests\Feature\Assessments;

use App\Enums\ApplicationStatus;
use App\Enums\AssessmentStatus;
use App\Enums\AuditAction;
use App\Enums\CriterionStage;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Evaluation;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\AssessmentAssignedNotification;
use App\Notifications\AssessmentConvocationNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

class EvaluationTest extends TestCase
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
    private function schedulePayload(array $overrides = []): array
    {
        return array_merge([
            'evaluator_id' => $this->evaluator->id,
            'type' => 'conocimientos',
            'modality' => 'presencial',
            'location' => 'Aula 204 - Sede central (demo)',
            'scheduled_at' => now()->addDays(3)->setTime(9, 0)->format('Y-m-d H:i'),
            'duration_minutes' => 60,
            'instructions' => 'Presentarse 15 minutos antes con lapicero.',
        ], $overrides);
    }

    /**
     * @return array<int, array{score: float|int, comment?: string}>
     */
    private function evaluationScores(float $knowledge = 16, float $modelClass = 14): array
    {
        $criteria = $this->vacancy->criteria()->where('stage', CriterionStage::Evaluation)->orderBy('position')->get();

        return [
            $criteria[0]->id => ['score' => $knowledge, 'comment' => 'Dominio adecuado.'],
            $criteria[1]->id => ['score' => $modelClass],
        ];
    }

    public function test_rf16_rf17_hr_schedules_evaluation_and_convocation_is_sent(): void
    {
        Notification::fake();
        $application = Application::factory()->for($this->vacancy)->shortlisted()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.evaluations.store', $application), $this->schedulePayload())
            ->assertSessionHasNoErrors();

        $evaluation = Evaluation::query()->sole();
        $this->assertSame(AssessmentStatus::Scheduled, $evaluation->status);
        $this->assertSame($this->evaluator->id, $evaluation->evaluator_id);
        $this->assertNotNull($evaluation->invitation_sent_at);
        $this->assertSame(ApplicationStatus::Evaluation, $application->fresh()->status);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::EvaluationScheduled)->exists());

        Notification::assertSentTo($application->candidate, AssessmentConvocationNotification::class);
        Notification::assertSentTo($this->evaluator, AssessmentAssignedNotification::class);
    }

    public function test_rf16_evaluator_must_be_an_evaluator_of_the_same_organization(): void
    {
        $application = Application::factory()->for($this->vacancy)->shortlisted()->create();
        $foreignEvaluator = User::factory()->evaluator(Organization::factory()->create())->create();

        $this->actingAs($this->hr)
            ->post(route('applications.evaluations.store', $application), $this->schedulePayload(['evaluator_id' => $foreignEvaluator->id]))
            ->assertSessionHasErrors('evaluator_id');

        $this->actingAs($this->hr)
            ->post(route('applications.evaluations.store', $application), $this->schedulePayload(['evaluator_id' => $this->hr->id]))
            ->assertSessionHasErrors('evaluator_id');

        $this->assertSame(0, Evaluation::query()->count());
    }

    public function test_rf16_evaluation_cannot_be_scheduled_in_the_past(): void
    {
        $application = Application::factory()->for($this->vacancy)->shortlisted()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.evaluations.store', $application), $this->schedulePayload(['scheduled_at' => now()->subHour()->format('Y-m-d H:i')]))
            ->assertSessionHasErrors('scheduled_at');
    }

    public function test_rf16_only_shortlisted_or_in_evaluation_applications_can_be_evaluated(): void
    {
        $submitted = Application::factory()->for($this->vacancy)->create();
        $discarded = Application::factory()->for($this->vacancy)->discarded()->create();

        $this->actingAs($this->hr)->post(route('applications.evaluations.store', $submitted), $this->schedulePayload())->assertSessionHasErrors('workflow');
        $this->actingAs($this->hr)->post(route('applications.evaluations.store', $discarded), $this->schedulePayload())->assertSessionHasErrors('workflow');

        $this->assertSame(0, Evaluation::query()->count());
    }

    public function test_rf16_only_hr_can_schedule_evaluations(): void
    {
        $application = Application::factory()->for($this->vacancy)->shortlisted()->create();

        $this->actingAs(User::factory()->approver($this->organization)->create())
            ->post(route('applications.evaluations.store', $application), $this->schedulePayload())
            ->assertForbidden();
        $this->actingAs($this->evaluator)
            ->post(route('applications.evaluations.store', $application), $this->schedulePayload())
            ->assertForbidden();
    }

    public function test_assigned_evaluator_records_evaluation_scores(): void
    {
        $evaluation = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo($this->evaluator)->create();

        $this->actingAs($this->evaluator)
            ->post(route('evaluations.results.store', $evaluation), [
                'scores' => $this->evaluationScores(),
                'observations' => 'Evaluación desarrollada con normalidad.',
            ])
            ->assertSessionHasNoErrors();

        $evaluation->refresh();
        $this->assertSame(AssessmentStatus::Completed, $evaluation->status);
        $this->assertNotNull($evaluation->completed_at);
        $this->assertSame(2, $evaluation->results()->count());
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::EvaluationResultRecorded)->exists());
    }

    public function test_rf20_out_of_range_or_missing_scores_are_rejected(): void
    {
        $evaluation = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo($this->evaluator)->create();
        $scores = $this->evaluationScores(knowledge: 25);
        $firstCriterionId = array_key_first($scores);

        $this->actingAs($this->evaluator)
            ->post(route('evaluations.results.store', $evaluation), ['scores' => $scores])
            ->assertSessionHasErrors("scores.{$firstCriterionId}.score");

        $this->actingAs($this->evaluator)
            ->post(route('evaluations.results.store', $evaluation), ['scores' => array_slice($scores, 1, null, true)])
            ->assertSessionHasErrors("scores.{$firstCriterionId}.score");

        $this->assertSame(AssessmentStatus::Scheduled, $evaluation->fresh()->status);
        $this->assertSame(0, $evaluation->results()->count());
    }

    /**
     * Fase 25 (QA global): caracterización cross-tenant de evaluaciones. RR. HH. y un
     * evaluador de otra organización no pueden programar, ver ni registrar sesiones
     * de esta organización, aunque conozcan el ID.
     */
    public function test_actors_of_another_organization_cannot_schedule_view_or_record_evaluations(): void
    {
        $foreign = Organization::factory()->create();
        $foreignHr = User::factory()->hr($foreign)->create();
        $foreignEvaluator = User::factory()->evaluator($foreign)->create();
        // Antes de autenticar: con un usuario de otra organización el scope oculta los criterios.
        $resultPayload = ['scores' => $this->evaluationScores()];

        $shortlisted = Application::factory()->for($this->vacancy)->shortlisted()->create();
        $schedule = $this->actingAs($foreignHr)
            ->post(route('applications.evaluations.store', $shortlisted), $this->schedulePayload(['evaluator_id' => $foreignEvaluator->id]));
        $this->assertContains($schedule->status(), [403, 404]);
        $this->assertSame(0, Evaluation::query()->withoutGlobalScopes()->count());

        $evaluation = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo($this->evaluator)->create();

        $this->assertContains($this->actingAs($foreignEvaluator)->get(route('evaluations.show', $evaluation))->status(), [403, 404]);
        $this->assertContains($this->actingAs($foreignHr)->get(route('evaluations.show', $evaluation))->status(), [403, 404]);

        $record = $this->actingAs($foreignEvaluator)
            ->post(route('evaluations.results.store', $evaluation), $resultPayload);
        $this->assertContains($record->status(), [403, 404]);
        $this->assertSame(AssessmentStatus::Scheduled, Evaluation::query()->withoutGlobalScopes()->findOrFail($evaluation->id)->status);
    }

    public function test_only_the_assigned_evaluator_can_record_results(): void
    {
        $evaluation = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo($this->evaluator)->create();
        $payload = ['scores' => $this->evaluationScores()];

        $this->actingAs(User::factory()->evaluator($this->organization)->create())->post(route('evaluations.results.store', $evaluation), $payload)->assertForbidden();
        $this->actingAs($this->hr)->post(route('evaluations.results.store', $evaluation), $payload)->assertForbidden();

        $this->assertSame(AssessmentStatus::Scheduled, $evaluation->fresh()->status);
    }

    public function test_results_cannot_be_recorded_twice(): void
    {
        $evaluation = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo($this->evaluator)->create();
        $payload = ['scores' => $this->evaluationScores()];

        $this->actingAs($this->evaluator)->post(route('evaluations.results.store', $evaluation), $payload)->assertSessionHasNoErrors();
        $this->actingAs($this->evaluator)->post(route('evaluations.results.store', $evaluation), $payload)->assertSessionHasErrors('workflow');

        $this->assertSame(2, $evaluation->results()->count());
    }

    public function test_evaluator_only_lists_and_views_own_assignments(): void
    {
        $own = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo($this->evaluator)->create();
        $other = Evaluation::factory()->forApplication(Application::factory()->for($this->vacancy)->inEvaluation()->create())->assignedTo(User::factory()->evaluator($this->organization)->create())->create();

        $this->actingAs($this->evaluator)
            ->get(route('assessments.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page->component('assessments/index')->has('assignments', 1));

        $this->actingAs($this->evaluator)
            ->get(route('evaluations.show', $own))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('assessments/show')
                ->where('session.id', $own->id)
                ->has('criteria', 2));

        $this->actingAs($this->evaluator)->get(route('evaluations.show', $other))->assertForbidden();
    }

    public function test_assigned_evaluator_can_download_the_candidate_cv(): void
    {
        $application = Application::factory()->for($this->vacancy)->inEvaluation()->create();
        Evaluation::factory()->forApplication($application)->assignedTo($this->evaluator)->create();

        $this->actingAs($this->evaluator)->get(route('documents.download', $application->candidate_document_id))->assertOk();
        $this->actingAs(User::factory()->evaluator($this->organization)->create())->get(route('documents.download', $application->candidate_document_id))->assertForbidden();
    }
}
