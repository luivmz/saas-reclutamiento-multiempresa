<?php

namespace Tests\Feature\Applications;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\ApplicationStageChangedNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

class ApplicationReviewTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private User $hr;

    private Vacancy $vacancy;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
    }

    public function test_rf12_hr_lists_applications_of_a_vacancy(): void
    {
        Application::factory()->for($this->vacancy)->count(3)->create();

        $this->actingAs($this->hr)
            ->get(route('vacancies.applications.index', $this->vacancy))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('applications/index')
                ->has('applications.data', 3));
    }

    public function test_rf12_hr_reviews_the_application_file(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();

        $this->actingAs($this->hr)
            ->get(route('applications.show', $application))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('applications/show')
                ->where('application.id', $application->id)
                ->has('application.candidate.profile')
                ->has('history', 1));
    }

    public function test_rf13_rf15_hr_shortlists_and_the_candidate_is_notified(): void
    {
        Notification::fake();
        $application = Application::factory()->for($this->vacancy)->create();

        $this->actingAs($this->hr)
            ->post(route('applications.shortlist', $application), ['comment' => 'Cumple el perfil requerido.'])
            ->assertSessionHasNoErrors();

        $application->refresh();
        $this->assertSame(ApplicationStatus::Shortlisted, $application->status);

        $history = $application->stageHistories()->latest('id')->first();
        $this->assertSame(ApplicationStatus::Submitted, $history->from_status);
        $this->assertSame(ApplicationStatus::Shortlisted, $history->to_status);
        $this->assertSame($this->hr->id, $history->changed_by);
        $this->assertSame('Cumple el perfil requerido.', $history->comment);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::ApplicationStageChanged)->exists());

        Notification::assertSentTo($application->candidate, ApplicationStageChangedNotification::class);
    }

    public function test_rf13_discard_requires_a_reason(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();

        $this->actingAs($this->hr)
            ->post(route('applications.discard', $application), ['comment' => ''])
            ->assertSessionHasErrors('comment');
        $this->assertSame(ApplicationStatus::Submitted, $application->fresh()->status);

        $this->actingAs($this->hr)
            ->post(route('applications.discard', $application), ['comment' => 'No acredita la formación requerida.'])
            ->assertSessionHasNoErrors();
        $this->assertSame(ApplicationStatus::Discarded, $application->fresh()->status);
    }

    public function test_rf14_hr_moves_application_to_an_allowed_stage(): void
    {
        $application = Application::factory()->for($this->vacancy)->shortlisted()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.stage', $application), ['status' => 'en_evaluacion'])
            ->assertSessionHasNoErrors();

        $this->assertSame(ApplicationStatus::Evaluation, $application->fresh()->status);
    }

    public function test_rf14_invalid_stage_transition_is_rejected(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();

        $this->actingAs($this->hr)
            ->post(route('applications.stage', $application), ['status' => 'finalista'])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(ApplicationStatus::Submitted, $application->fresh()->status);
    }

    public function test_rf14_selection_outcomes_cannot_be_assigned_manually(): void
    {
        $application = Application::factory()->for($this->vacancy)->finalist()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.stage', $application), ['status' => 'seleccionado'])
            ->assertSessionHasErrors('status');

        $this->assertSame(ApplicationStatus::Finalist, $application->fresh()->status);
    }

    public function test_stage_changes_are_blocked_when_the_vacancy_is_closed(): void
    {
        $closed = Vacancy::factory()->for($this->organization)->configured()->closed()->create();
        $application = Application::factory()->for($closed)->create();

        $this->actingAs($this->hr)
            ->post(route('applications.shortlist', $application))
            ->assertSessionHasErrors('workflow');

        $this->assertSame(ApplicationStatus::Submitted, $application->fresh()->status);
    }

    public function test_only_hr_can_change_stages(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();

        $this->actingAs(User::factory()->approver($this->organization)->create())->post(route('applications.shortlist', $application))->assertForbidden();
        $this->actingAs(User::factory()->evaluator($this->organization)->create())->post(route('applications.shortlist', $application))->assertForbidden();
        $this->actingAs($application->candidate)->post(route('applications.shortlist', $application))->assertForbidden();

        $this->assertSame(ApplicationStatus::Submitted, $application->fresh()->status);
    }

    public function test_candidate_only_sees_own_applications(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();
        Application::factory()->for($this->vacancy)->create();

        $this->actingAs($application->candidate)
            ->get(route('candidate.applications.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page->component('candidate/applications/index')->has('applications.data', 1));

        $this->actingAs($application->candidate)->get(route('candidate.applications.show', $application))->assertOk();
        $this->actingAs(User::factory()->candidate()->create())->get(route('candidate.applications.show', $application))->assertForbidden();
    }
}
