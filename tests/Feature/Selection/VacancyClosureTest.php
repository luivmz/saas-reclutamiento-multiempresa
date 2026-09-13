<?php

namespace Tests\Feature\Selection;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Enums\VacancyClosureType;
use App\Enums\VacancyStatus;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\CandidateProfile;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

class VacancyClosureTest extends TestCase
{
    use BuildsRankingScenario, RefreshDatabase;

    private Organization $organization;

    private User $hr;

    private User $approver;

    private Vacancy $vacancy;

    private Application $chosen;

    private Application $otherFinalist;

    private Application $inEvaluation;

    private Application $discarded;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->approver = User::factory()->approver($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->chosen = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->otherFinalist = $this->candidateWithScores($this->vacancy, 20, 10, 19);
        $this->inEvaluation = $this->candidateWithScores($this->vacancy, 12, null, null, ApplicationStatus::Evaluation);
        $this->discarded = $this->candidateWithScores($this->vacancy, null, null, null, ApplicationStatus::Discarded);
    }

    private function recordDecision(): void
    {
        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), [
                'application_id' => $this->chosen->id,
                'justification' => 'Decisión humana registrada para la prueba de cierre.',
                'human_confirmation' => '1',
            ])
            ->assertSessionHasNoErrors();
    }

    private function recordDecisionAndSelection(): void
    {
        $this->recordDecision();
        $this->actingAs($this->hr)->post(route('vacancies.selection.store', $this->vacancy))->assertSessionHasNoErrors();
    }

    public function test_rf25_hr_closes_the_vacancy_after_the_selection_is_registered(): void
    {
        $this->recordDecisionAndSelection();

        $this->actingAs($this->hr)
            ->post(route('vacancies.close', $this->vacancy), ['closure_notes' => 'Proceso concluido con selección.'])
            ->assertSessionHasNoErrors();

        $vacancy = $this->vacancy->fresh();
        $this->assertSame(VacancyStatus::Closed, $vacancy->status);
        $this->assertSame(VacancyClosureType::WithSelection, $vacancy->closure_type);
        $this->assertSame($this->hr->id, $vacancy->closed_by);
        $this->assertNotNull($vacancy->closed_at);
        $this->assertSame('Proceso concluido con selección.', $vacancy->closure_notes);

        $this->assertSame(ApplicationStatus::Selected, $this->chosen->fresh()->status);
        $this->assertSame(ApplicationStatus::NotSelected, $this->otherFinalist->fresh()->status);
        $this->assertSame(ApplicationStatus::NotSelected, $this->inEvaluation->fresh()->status);
        $this->assertSame(ApplicationStatus::Discarded, $this->discarded->fresh()->status);

        $history = $this->otherFinalist->stageHistories()->latest('id')->first();
        $this->assertSame(ApplicationStatus::NotSelected, $history->to_status);
        $this->assertSame($this->hr->id, $history->changed_by);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::VacancyClosed)->where('auditable_id', $this->vacancy->id)->exists());
    }

    public function test_rf25_closure_without_a_registered_selection_is_rejected(): void
    {
        $this->actingAs($this->hr)->post(route('vacancies.close', $this->vacancy))->assertSessionHasErrors('workflow');

        $this->recordDecision();
        $this->actingAs($this->hr)->post(route('vacancies.close', $this->vacancy))->assertSessionHasErrors('workflow');

        $this->assertSame(VacancyStatus::Published, $this->vacancy->fresh()->status);
        $this->assertSame(ApplicationStatus::Finalist, $this->otherFinalist->fresh()->status);
    }

    public function test_rf25_only_hr_can_close_the_vacancy(): void
    {
        $this->recordDecisionAndSelection();

        $this->actingAs($this->approver)->post(route('vacancies.close', $this->vacancy))->assertForbidden();
        $this->actingAs(User::factory()->evaluator($this->organization)->create())->post(route('vacancies.close', $this->vacancy))->assertForbidden();

        $this->assertSame(VacancyStatus::Published, $this->vacancy->fresh()->status);
    }

    public function test_rf25_hr_of_another_organization_cannot_close_the_vacancy(): void
    {
        $this->recordDecisionAndSelection();

        $this->actingAs(User::factory()->hr(Organization::factory()->create())->create())
            ->post(route('vacancies.close', $this->vacancy))
            ->assertNotFound();

        $this->assertSame(VacancyStatus::Published, $this->vacancy->fresh()->status);
    }

    public function test_rf25_closed_vacancy_rejects_incompatible_operations(): void
    {
        $this->recordDecisionAndSelection();
        $this->actingAs($this->hr)->post(route('vacancies.close', $this->vacancy))->assertSessionHasNoErrors();

        $newCandidate = User::factory()->candidate()->has(CandidateProfile::factory()->withCv(), 'candidateProfile')->create();
        $this->actingAs($newCandidate)->post(route('jobs.apply', $this->vacancy))->assertSessionHasErrors('workflow');

        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), [
                'application_id' => $this->otherFinalist->id,
                'justification' => 'Intento de modificar la decisión después del cierre.',
                'human_confirmation' => '1',
            ])
            ->assertSessionHasErrors('workflow');

        $this->actingAs($this->hr)->post(route('vacancies.selection.store', $this->vacancy))->assertSessionHasErrors('workflow');
        $this->actingAs($this->hr)->post(route('vacancies.close', $this->vacancy))->assertSessionHasErrors('workflow');

        $this->actingAs($this->hr)
            ->post(route('applications.interviews.store', $this->otherFinalist), [
                'evaluator_id' => User::factory()->evaluator($this->organization)->create()->id,
                'modality' => 'presencial',
                'location' => 'Sala de reuniones',
                'scheduled_at' => now()->addDay()->format('Y-m-d H:i'),
            ])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(ApplicationStatus::Selected, $this->chosen->fresh()->status);
        $this->assertSame(ApplicationStatus::NotSelected, $this->otherFinalist->fresh()->status);
        $this->assertSame(1, Application::query()->withoutGlobalScopes()->where('vacancy_id', $this->vacancy->id)->where('status', ApplicationStatus::Selected)->count());
        $this->assertSame(4, Application::query()->withoutGlobalScopes()->where('vacancy_id', $this->vacancy->id)->count());
    }
}
