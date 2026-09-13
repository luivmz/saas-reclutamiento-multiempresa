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
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

class FinalDecisionTest extends TestCase
{
    use BuildsRankingScenario, RefreshDatabase;

    private Organization $organization;

    private User $approver;

    private Vacancy $vacancy;

    private Application $first;

    private Application $second;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->approver = User::factory()->approver($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->first = $this->candidateWithScores($this->vacancy, 18, 16, 17);  // 85.5
        $this->second = $this->candidateWithScores($this->vacancy, 20, 10, 19); // 83.5
    }

    /**
     * @return array<string, mixed>
     */
    private function payload(Application $application, array $overrides = []): array
    {
        return array_merge([
            'application_id' => $application->id,
            'justification' => 'Se elige al candidato por su desempeño en la clase modelo y la entrevista.',
            'human_confirmation' => '1',
        ], $overrides);
    }

    public function test_rf23_approver_records_the_final_decision_for_a_ranked_finalist(): void
    {
        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->first))
            ->assertSessionHasNoErrors();

        $decision = SelectionDecision::query()->sole();
        $this->assertSame($this->first->id, $decision->selected_application_id);
        $this->assertSame($this->approver->id, $decision->decided_by);
        $this->assertNotNull($decision->decided_at);
        $this->assertSame(1, $decision->selected_position);
        $this->assertEqualsWithDelta(85.5, $decision->selected_score, 0.001);
        $this->assertSame(2, $decision->ranked_candidates);
        $this->assertStringContainsString('clase modelo', $decision->justification);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::SelectionDecisionRecorded)->where('auditable_id', $decision->id)->exists());

        $this->assertSame(ApplicationStatus::Finalist, $this->first->fresh()->status, 'The decision alone must not change the application status (RF-24 does).');
        $this->assertSame(0, Application::query()->withoutGlobalScopes()->where('status', ApplicationStatus::Selected)->count());
    }

    public function test_rf23_approver_may_choose_a_candidate_who_is_not_first_in_the_ranking(): void
    {
        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->second))
            ->assertSessionHasNoErrors();

        $decision = SelectionDecision::query()->sole();
        $this->assertSame($this->second->id, $decision->selected_application_id);
        $this->assertSame(2, $decision->selected_position);
    }

    public function test_rf23_explicit_human_confirmation_and_justification_are_required(): void
    {
        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->first, ['human_confirmation' => null, 'justification' => '']))
            ->assertSessionHasErrors(['human_confirmation', 'justification']);

        $this->assertSame(0, SelectionDecision::query()->count());
    }

    public function test_rf23_candidate_of_another_vacancy_is_rejected(): void
    {
        $otherVacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $outsider = $this->candidateWithScores($otherVacancy, 20, 20, 20);

        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($outsider))
            ->assertSessionHasErrors('application_id');

        $this->assertSame(0, SelectionDecision::query()->count());
    }

    public function test_rf23_candidate_of_another_tenant_is_rejected(): void
    {
        $foreignVacancy = Vacancy::factory()->for(Organization::factory()->create())->configured()->published()->create();
        $foreign = $this->candidateWithScores($foreignVacancy, 20, 20, 20);

        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($foreign))
            ->assertSessionHasErrors('application_id');

        $this->assertSame(0, SelectionDecision::query()->withoutGlobalScopes()->count());
    }

    public function test_rf23_non_finalist_or_incompletely_evaluated_candidates_are_rejected(): void
    {
        $notFinalist = $this->candidateWithScores($this->vacancy, 19, 19, 19, ApplicationStatus::Interview);
        $incomplete = $this->candidateWithScores($this->vacancy, 19, 19, null);

        $this->actingAs($this->approver)->post(route('vacancies.decision.store', $this->vacancy), $this->payload($notFinalist))->assertSessionHasErrors('workflow');
        $this->actingAs($this->approver)->post(route('vacancies.decision.store', $this->vacancy), $this->payload($incomplete))->assertSessionHasErrors('workflow');

        $this->assertSame(0, SelectionDecision::query()->count());
    }

    public function test_rf23_recorded_decision_cannot_be_replaced(): void
    {
        $this->actingAs($this->approver)->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->first))->assertSessionHasNoErrors();

        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->second))
            ->assertSessionHasErrors('workflow');

        $this->assertSame($this->first->id, SelectionDecision::query()->sole()->selected_application_id);
    }

    public function test_rf23_only_the_approver_can_record_the_decision(): void
    {
        foreach ([
            User::factory()->hr($this->organization)->create(),
            User::factory()->evaluator($this->organization)->create(),
            User::factory()->requester($this->organization)->create(),
        ] as $user) {
            $this->actingAs($user)->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->first))->assertForbidden();
        }

        $this->assertSame(0, SelectionDecision::query()->withoutGlobalScopes()->count());
    }

    public function test_rf23_approver_of_another_organization_cannot_decide(): void
    {
        $this->actingAs(User::factory()->approver(Organization::factory()->create())->create())
            ->post(route('vacancies.decision.store', $this->vacancy), $this->payload($this->first))
            ->assertNotFound();

        $this->assertSame(0, SelectionDecision::query()->withoutGlobalScopes()->count());
    }

    public function test_rf23_decision_is_rejected_for_a_closed_vacancy(): void
    {
        $closed = Vacancy::factory()->for($this->organization)->configured()->closed()->create();
        $finalist = $this->candidateWithScores($closed, 18, 18, 18);

        $this->actingAs($this->approver)
            ->post(route('vacancies.decision.store', $closed), $this->payload($finalist))
            ->assertSessionHasErrors('workflow');

        $this->assertSame(0, SelectionDecision::query()->count());
    }
}
