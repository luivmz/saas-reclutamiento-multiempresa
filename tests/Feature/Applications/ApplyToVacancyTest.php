<?php

namespace Tests\Feature\Applications;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\CandidateProfile;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\ApplicationReceivedNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ApplyToVacancyTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private Vacancy $vacancy;

    private User $candidate;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->candidate = User::factory()->candidate()->has(CandidateProfile::factory()->withCv(), 'candidateProfile')->create();
    }

    public function test_rf10_rf11_candidate_applies_and_receives_confirmation(): void
    {
        Notification::fake();

        $this->actingAs($this->candidate)
            ->post(route('jobs.apply', $this->vacancy))
            ->assertSessionHasNoErrors()
            ->assertRedirect();

        $application = Application::query()->withoutGlobalScopes()->sole();
        $this->assertSame(ApplicationStatus::Submitted, $application->status);
        $this->assertSame($this->organization->id, $application->organization_id);
        $this->assertSame($this->candidate->id, $application->candidate_id);
        $this->assertSame($this->candidate->candidateProfile->documents()->latest('id')->value('id'), $application->candidate_document_id);
        $this->assertSame(1, $application->stageHistories()->withoutGlobalScopes()->count());
        $this->assertTrue(AuditLog::query()->withoutGlobalScopes()
            ->where('action', AuditAction::ApplicationSubmitted)
            ->where('organization_id', $this->organization->id)
            ->exists());

        Notification::assertSentTo($this->candidate, ApplicationReceivedNotification::class);
    }

    public function test_rf10_duplicate_application_is_rejected(): void
    {
        Application::factory()->for($this->vacancy)->forCandidate($this->candidate)->create();

        $this->actingAs($this->candidate)
            ->post(route('jobs.apply', $this->vacancy))
            ->assertSessionHasErrors('workflow');

        $this->assertSame(1, Application::query()->withoutGlobalScopes()->count());
    }

    public function test_rf10_cannot_apply_to_closed_or_expired_vacancy(): void
    {
        $closed = Vacancy::factory()->for($this->organization)->configured()->closed()->create();
        $expired = Vacancy::factory()->for($this->organization)->configured()->published()->create([
            'opens_at' => now()->subDays(20),
            'closes_at' => now()->subDay(),
        ]);

        $this->actingAs($this->candidate)->post(route('jobs.apply', $closed))->assertSessionHasErrors('workflow');
        $this->actingAs($this->candidate)->post(route('jobs.apply', $expired))->assertSessionHasErrors('workflow');

        $this->assertSame(0, Application::query()->withoutGlobalScopes()->count());
    }

    public function test_rf10_draft_vacancy_is_not_available(): void
    {
        $draft = Vacancy::factory()->for($this->organization)->configured()->create();

        $this->actingAs($this->candidate)->post(route('jobs.apply', $draft))->assertNotFound();
    }

    public function test_rf10_incomplete_profile_or_missing_cv_blocks_application(): void
    {
        $withoutProfile = User::factory()->candidate()->create();
        $withoutCv = User::factory()->candidate()->has(CandidateProfile::factory(), 'candidateProfile')->create();

        $this->actingAs($withoutProfile)->post(route('jobs.apply', $this->vacancy))->assertSessionHasErrors('workflow');
        $this->actingAs($withoutCv)->post(route('jobs.apply', $this->vacancy))->assertSessionHasErrors('workflow');

        $this->assertSame(0, Application::query()->withoutGlobalScopes()->count());
    }

    public function test_staff_users_cannot_apply(): void
    {
        $this->actingAs(User::factory()->hr($this->organization)->create())
            ->post(route('jobs.apply', $this->vacancy))
            ->assertForbidden();
    }
}
