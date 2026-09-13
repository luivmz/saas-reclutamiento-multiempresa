<?php

namespace Tests\Feature\Selection;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

class SelectionRegistrationTest extends TestCase
{
    use BuildsRankingScenario, RefreshDatabase;

    private Organization $organization;

    private User $hr;

    private User $approver;

    private Vacancy $vacancy;

    private Application $chosen;

    private Application $other;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->approver = User::factory()->approver($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->chosen = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->other = $this->candidateWithScores($this->vacancy, 20, 10, 19);
    }

    private function recordDecision(Application $application): void
    {
        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), [
                'application_id' => $application->id,
                'justification' => 'Decisión humana registrada para la prueba de selección.',
                'human_confirmation' => '1',
            ])
            ->assertSessionHasNoErrors();
    }

    public function test_rf24_hr_registers_the_selection_after_the_human_decision(): void
    {
        $this->recordDecision($this->chosen);

        $this->actingAs($this->hr)->post(route('vacancies.selection.store', $this->vacancy))->assertSessionHasNoErrors();

        $this->assertSame(ApplicationStatus::Selected, $this->chosen->fresh()->status);
        $this->assertSame(ApplicationStatus::Finalist, $this->other->fresh()->status);

        $history = $this->chosen->stageHistories()->latest('id')->first();
        $this->assertSame(ApplicationStatus::Finalist, $history->from_status);
        $this->assertSame(ApplicationStatus::Selected, $history->to_status);
        $this->assertSame($this->hr->id, $history->changed_by);

        $decision = SelectionDecision::query()->sole();
        $this->assertSame($this->hr->id, $decision->selection_registered_by);
        $this->assertNotNull($decision->selection_registered_at);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::CandidateSelected)->where('auditable_id', $this->chosen->id)->exists());
    }

    public function test_rf24_selection_requires_a_recorded_human_decision(): void
    {
        $this->actingAs($this->hr)
            ->post(route('vacancies.selection.store', $this->vacancy))
            ->assertSessionHasErrors('workflow');

        $this->assertSame(0, Application::query()->withoutGlobalScopes()->where('status', ApplicationStatus::Selected)->count());
    }

    public function test_rf24_selection_cannot_be_registered_twice(): void
    {
        $this->recordDecision($this->chosen);
        $this->actingAs($this->hr)->post(route('vacancies.selection.store', $this->vacancy))->assertSessionHasNoErrors();

        $this->actingAs($this->hr)
            ->post(route('vacancies.selection.store', $this->vacancy))
            ->assertSessionHasErrors('workflow');

        $this->assertSame(1, Application::query()->withoutGlobalScopes()->where('status', ApplicationStatus::Selected)->count());
    }

    public function test_rf24_only_hr_can_register_the_selection(): void
    {
        $this->recordDecision($this->chosen);

        $this->actingAs($this->approver)->post(route('vacancies.selection.store', $this->vacancy))->assertForbidden();
        $this->actingAs(User::factory()->evaluator($this->organization)->create())->post(route('vacancies.selection.store', $this->vacancy))->assertForbidden();

        $this->assertSame(ApplicationStatus::Finalist, $this->chosen->fresh()->status);
    }

    public function test_rf24_hr_of_another_organization_cannot_register_the_selection(): void
    {
        $this->recordDecision($this->chosen);

        $this->actingAs(User::factory()->hr(Organization::factory()->create())->create())
            ->post(route('vacancies.selection.store', $this->vacancy))
            ->assertNotFound();

        $this->assertSame(ApplicationStatus::Finalist, $this->chosen->fresh()->status);
    }

    public function test_rf24_manual_stage_changes_are_blocked_after_the_final_decision(): void
    {
        $this->recordDecision($this->chosen);

        $this->actingAs($this->hr)
            ->post(route('applications.discard', $this->chosen), ['comment' => 'Intento de descartar tras la decisión.'])
            ->assertSessionHasErrors('workflow');
        $this->actingAs($this->hr)
            ->post(route('applications.discard', $this->other), ['comment' => 'Intento de descartar tras la decisión.'])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(ApplicationStatus::Finalist, $this->chosen->fresh()->status);
        $this->assertSame(ApplicationStatus::Finalist, $this->other->fresh()->status);
    }

    public function test_rf24_database_prevents_two_selected_candidates_in_the_same_vacancy(): void
    {
        $this->recordDecision($this->chosen);
        $this->actingAs($this->hr)->post(route('vacancies.selection.store', $this->vacancy))->assertSessionHasNoErrors();

        $this->expectException(QueryException::class);

        Application::query()->withoutGlobalScopes()->whereKey($this->other->id)->update(['status' => ApplicationStatus::Selected->value]);
    }
}
