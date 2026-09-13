<?php

namespace Tests\Feature\Selection;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Ranking\VacancyRankingBuilder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Inertia\Testing\AssertableInertia;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

class RankingComparisonTest extends TestCase
{
    use BuildsRankingScenario, RefreshDatabase;

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

    public function test_rf21_rf22_hr_views_the_comparison_ordered_by_weighted_total(): void
    {
        $a = $this->candidateWithScores($this->vacancy, 18, 16, 17); // 36 + 24 + 25.5 = 85.5
        $b = $this->candidateWithScores($this->vacancy, 14, 15, 12); // 28 + 22.5 + 18 = 68.5
        $c = $this->candidateWithScores($this->vacancy, 20, 10, 19); // 40 + 15 + 28.5 = 83.5

        $this->actingAs($this->hr)
            ->get(route('vacancies.comparison', $this->vacancy))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('selection/comparison')
                ->has('criteria', 3)
                ->where('rankingError', null)
                ->has('ranking.entries', 3)
                ->where('ranking.entries.0.application_id', $a->id)
                ->where('ranking.entries.0.position', 1)
                ->where('ranking.entries.0.total', 85.5)
                ->has('ranking.entries.0.breakdown', 3)
                ->where('ranking.entries.1.application_id', $c->id)
                ->where('ranking.entries.1.total', 83.5)
                ->where('ranking.entries.2.application_id', $b->id)
                ->where('ranking.entries.2.total', 68.5));
    }

    public function test_rf22_approver_can_view_the_comparison_but_other_roles_cannot(): void
    {
        $this->candidateWithScores($this->vacancy, 18, 16, 17);

        $this->actingAs(User::factory()->approver($this->organization)->create())->get(route('vacancies.comparison', $this->vacancy))->assertOk();
        $this->actingAs(User::factory()->evaluator($this->organization)->create())->get(route('vacancies.comparison', $this->vacancy))->assertForbidden();
        $this->actingAs(User::factory()->requester($this->organization)->create())->get(route('vacancies.comparison', $this->vacancy))->assertForbidden();
        $this->actingAs(User::factory()->candidate()->create())->get(route('vacancies.comparison', $this->vacancy))->assertForbidden();
    }

    public function test_rf23_calculating_the_ranking_never_selects_a_candidate(): void
    {
        $applications = collect([
            $this->candidateWithScores($this->vacancy, 20, 20, 20),
            $this->candidateWithScores($this->vacancy, 10, 10, 10),
            $this->candidateWithScores($this->vacancy, 15, 12, 18, ApplicationStatus::Interview),
        ]);
        $statusesBefore = $applications->mapWithKeys(fn (Application $application) => [$application->id => $application->fresh()->status])->all();
        $historiesBefore = ApplicationStageHistory::query()->withoutGlobalScopes()->count();

        app(VacancyRankingBuilder::class)->forVacancy($this->vacancy);
        $this->actingAs($this->hr)->get(route('vacancies.comparison', $this->vacancy))->assertOk();
        $this->actingAs(User::factory()->approver($this->organization)->create())->get(route('vacancies.comparison', $this->vacancy))->assertOk();

        $statusesAfter = $applications->mapWithKeys(fn (Application $application) => [$application->id => $application->fresh()->status])->all();
        $this->assertSame($statusesBefore, $statusesAfter);
        $this->assertSame(0, Application::query()->withoutGlobalScopes()->where('status', ApplicationStatus::Selected)->count());
        $this->assertSame(0, SelectionDecision::query()->withoutGlobalScopes()->count());
        $this->assertSame($historiesBefore, ApplicationStageHistory::query()->withoutGlobalScopes()->count());
        $this->assertFalse(AuditLog::query()->withoutGlobalScopes()->whereIn('action', [AuditAction::CandidateSelected, AuditAction::SelectionDecisionRecorded])->exists());
        $this->assertTrue($this->vacancy->fresh()->status->value === 'publicada');
    }

    public function test_rf21_discarded_and_other_vacancy_applications_are_not_ranked(): void
    {
        $eligible = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->candidateWithScores($this->vacancy, 20, 20, 20, ApplicationStatus::Discarded);
        $otherVacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->candidateWithScores($otherVacancy, 20, 20, 20);

        $this->actingAs($this->hr)
            ->get(route('vacancies.comparison', $this->vacancy))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->has('ranking.entries', 1)
                ->where('ranking.entries.0.application_id', $eligible->id)
                ->has('ranking.incomplete', 0));
    }

    public function test_rf21_application_of_another_tenant_is_never_ranked_even_if_linked_to_the_vacancy(): void
    {
        $eligible = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $foreignVacancy = Vacancy::factory()->for(Organization::factory()->create())->configured()->published()->create();
        $foreign = $this->candidateWithScores($foreignVacancy, 20, 20, 20);
        $foreign->forceFill(['vacancy_id' => $this->vacancy->id])->save();

        $result = app(VacancyRankingBuilder::class)->forVacancy($this->vacancy);

        $this->assertSame([$eligible->id], array_map(fn ($entry) => $entry->applicationId, $result->entries));
        $this->assertSame([], $result->incomplete);
    }

    public function test_rf21_candidates_without_complete_results_are_listed_as_incomplete(): void
    {
        $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $pending = $this->candidateWithScores($this->vacancy, 15, 12, null, ApplicationStatus::Evaluation);

        $this->actingAs($this->hr)
            ->get(route('vacancies.comparison', $this->vacancy))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->has('ranking.entries', 1)
                ->has('ranking.incomplete', 1)
                ->where('ranking.incomplete.0.application_id', $pending->id)
                ->where('ranking.incomplete.0.missing_criteria', ['Entrevista personal']));
    }

    public function test_rf20_invalid_weight_configuration_is_reported_instead_of_a_ranking(): void
    {
        $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->vacancy->criteria()->first()->update(['weight' => 5]);

        $this->actingAs($this->hr)
            ->get(route('vacancies.comparison', $this->vacancy))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->whereNot('rankingError', null)
                ->has('ranking.entries', 0));
    }

    public function test_rf22_hr_of_other_organization_cannot_view_the_comparison(): void
    {
        $this->candidateWithScores($this->vacancy, 18, 16, 17);

        $this->actingAs(User::factory()->hr(Organization::factory()->create())->create())
            ->get(route('vacancies.comparison', $this->vacancy))
            ->assertNotFound();
    }
}
