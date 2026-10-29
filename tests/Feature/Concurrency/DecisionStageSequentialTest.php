<?php

namespace Tests\Feature\Concurrency;

use App\Enums\ApplicationStatus;
use App\Models\Application;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Testing\TestResponse;
use PHPUnit\Framework\Attributes\Group;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

/**
 * SEG-02 sequential controls (A-28) through real HTTP requests: when one operation finishes before the other
 * starts, the rules already hold. The concurrent cases are in DecisionStageConcurrencyTest.
 */
#[Group('seg02')]
class DecisionStageSequentialTest extends TestCase
{
    use BuildsRankingScenario, RefreshDatabase;

    private User $hr;

    private User $approver;

    private Vacancy $vacancy;

    private Application $chosen;

    private Application $other;

    protected function setUp(): void
    {
        parent::setUp();

        $organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($organization)->create();
        $this->approver = User::factory()->approver($organization)->create();
        $this->vacancy = Vacancy::factory()->for($organization)->configured()->published()->create();
        $this->chosen = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->other = $this->candidateWithScores($this->vacancy, 20, 10, 19);
    }

    public function test_seg02_s1_discard_requested_after_the_decision_is_rejected(): void
    {
        $this->decide($this->chosen)->assertSessionHasNoErrors();

        $this->actingAs($this->hr)
            ->post(route('applications.discard', $this->chosen), ['comment' => 'Descarte ficticio posterior a la decisión.'])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(ApplicationStatus::Finalist, $this->chosen->fresh()->status);
        $this->assertSame($this->chosen->id, SelectionDecision::query()->sole()->selected_application_id);
    }

    public function test_seg02_s1b_manual_change_of_another_application_after_the_decision_is_rejected(): void
    {
        $this->decide($this->chosen)->assertSessionHasNoErrors();

        $this->actingAs($this->hr)
            ->post(route('applications.discard', $this->other), ['comment' => 'Descarte ficticio posterior a la decisión.'])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(ApplicationStatus::Finalist, $this->other->fresh()->status);
    }

    public function test_seg02_s2_decision_requested_after_a_discard_is_rejected(): void
    {
        $this->actingAs($this->hr)
            ->post(route('applications.discard', $this->chosen), ['comment' => 'Descarte ficticio previo a la decisión.'])
            ->assertSessionHasNoErrors();

        $this->decide($this->chosen)->assertSessionHasErrors();

        $this->assertSame(ApplicationStatus::Discarded, $this->chosen->fresh()->status);
        $this->assertSame(0, SelectionDecision::query()->count());
    }

    private function decide(Application $application): TestResponse
    {
        return $this->actingAs($this->approver)->post(route('vacancies.decision.store', $this->vacancy), [
            'application_id' => $application->id,
            'justification' => 'Decisión ficticia registrada para la prueba secuencial de SEG-02.',
            'human_confirmation' => '1',
        ]);
    }
}
