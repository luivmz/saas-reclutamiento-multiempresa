<?php

namespace Tests\Feature\Notifications;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\ProcessResultNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

class ProcessResultNotificationTest extends TestCase
{
    use BuildsRankingScenario, RefreshDatabase;

    private const JUSTIFICATION = 'Justificación interna confidencial de la dirección para la prueba.';

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

        $this->organization = Organization::factory()->create(['name' => 'Colegio Andino (Demo)']);
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->approver = User::factory()->approver($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create(['title' => 'Docente de Matemática']);
        $this->chosen = $this->candidateWithScores($this->vacancy, 18, 16, 17);        // 85.5
        $this->otherFinalist = $this->candidateWithScores($this->vacancy, 20, 10, 19); // 83.5
        $this->inEvaluation = $this->candidateWithScores($this->vacancy, 12, null, null, ApplicationStatus::Evaluation);
        $this->discarded = $this->candidateWithScores($this->vacancy, null, null, null, ApplicationStatus::Discarded);
    }

    private function decideAndSelect(Vacancy $vacancy, Application $chosen, User $approver, User $hr): void
    {
        $this->actingAs($approver)
            ->post(route('vacancies.decision.store', $vacancy), [
                'application_id' => $chosen->id,
                'justification' => self::JUSTIFICATION,
                'human_confirmation' => '1',
            ])
            ->assertSessionHasNoErrors();

        $this->actingAs($hr)->post(route('vacancies.selection.store', $vacancy))->assertSessionHasNoErrors();
    }

    private function close(Vacancy $vacancy, User $hr): void
    {
        $this->actingAs($hr)->post(route('vacancies.close', $vacancy))->assertSessionHasNoErrors();
    }

    public function test_rf26_selected_candidate_receives_the_result_when_the_vacancy_closes(): void
    {
        Notification::fake();
        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);
        $this->close($this->vacancy, $this->hr);

        Notification::assertSentTo(
            $this->chosen->candidate,
            ProcessResultNotification::class,
            fn (ProcessResultNotification $notification) => $notification->result === ApplicationStatus::Selected
                && $notification->application->is($this->chosen),
        );
    }

    public function test_rf26_not_selected_candidates_receive_the_result_when_the_vacancy_closes(): void
    {
        Notification::fake();
        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);
        $this->close($this->vacancy, $this->hr);

        foreach ([$this->otherFinalist, $this->inEvaluation] as $application) {
            Notification::assertSentTo(
                $application->candidate,
                ProcessResultNotification::class,
                fn (ProcessResultNotification $notification) => $notification->result === ApplicationStatus::NotSelected,
            );
        }
    }

    public function test_rf26_no_final_result_is_sent_before_the_vacancy_is_closed(): void
    {
        Notification::fake();
        $this->actingAs($this->hr)->get(route('vacancies.comparison', $this->vacancy))->assertOk();
        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);

        foreach ([$this->chosen, $this->otherFinalist, $this->inEvaluation, $this->discarded] as $application) {
            Notification::assertNotSentTo($application->candidate, ProcessResultNotification::class);
        }
    }

    public function test_rf26_only_candidates_of_the_closed_vacancy_are_notified(): void
    {
        Notification::fake();
        $otherVacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $otherVacancyCandidate = $this->candidateWithScores($otherVacancy, 20, 20, 20);
        $foreignOrganization = Organization::factory()->create();
        $foreignVacancy = Vacancy::factory()->for($foreignOrganization)->configured()->published()->create();
        $foreignCandidate = $this->candidateWithScores($foreignVacancy, 20, 20, 20);

        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);
        $this->close($this->vacancy, $this->hr);

        Notification::assertNotSentTo($this->discarded->candidate, ProcessResultNotification::class);
        Notification::assertNotSentTo($otherVacancyCandidate->candidate, ProcessResultNotification::class);
        Notification::assertNotSentTo($foreignCandidate->candidate, ProcessResultNotification::class);
    }

    public function test_rf26_closing_a_vacancy_of_another_organization_does_not_notify_this_organization_candidates(): void
    {
        Notification::fake();
        $foreignOrganization = Organization::factory()->create();
        $foreignVacancy = Vacancy::factory()->for($foreignOrganization)->configured()->published()->create();
        $foreignChosen = $this->candidateWithScores($foreignVacancy, 19, 19, 19);

        $this->decideAndSelect(
            $foreignVacancy,
            $foreignChosen,
            User::factory()->approver($foreignOrganization)->create(),
            $foreignHr = User::factory()->hr($foreignOrganization)->create(),
        );
        $this->close($foreignVacancy, $foreignHr);

        Notification::assertSentTo($foreignChosen->candidate, ProcessResultNotification::class);
        foreach ([$this->chosen, $this->otherFinalist, $this->inEvaluation, $this->discarded] as $application) {
            Notification::assertNotSentTo($application->candidate, ProcessResultNotification::class);
        }
    }

    public function test_rf26_result_notification_does_not_expose_scores_ranking_or_internal_notes(): void
    {
        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);
        $this->close($this->vacancy, $this->hr);

        foreach ([$this->chosen, $this->otherFinalist] as $application) {
            $stored = $application->candidate->notifications()->where('type', ProcessResultNotification::class)->sole();
            $payload = json_encode($stored->data, JSON_UNESCAPED_UNICODE);

            $this->assertStringContainsString('Docente de Matemática', $payload);
            $this->assertStringContainsString('Colegio Andino (Demo)', $payload);
            $this->assertStringNotContainsString('85.5', $payload);
            $this->assertStringNotContainsString('83.5', $payload);
            $this->assertStringNotContainsString(self::JUSTIFICATION, $payload);
            $this->assertStringNotContainsStringIgnoringCase('puntaje', $payload);
            $this->assertStringNotContainsStringIgnoringCase('ranking', $payload);
            $this->assertStringNotContainsString($this->chosen->is($application) ? $this->otherFinalist->candidate->name : $this->chosen->candidate->name, $payload);
        }
    }

    public function test_rf26_final_result_is_not_sent_twice_when_closure_is_repeated(): void
    {
        Notification::fake();
        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);
        $this->close($this->vacancy, $this->hr);

        $this->actingAs($this->hr)->post(route('vacancies.close', $this->vacancy))->assertSessionHasErrors('workflow');

        Notification::assertSentToTimes($this->chosen->candidate, ProcessResultNotification::class, 1);
        Notification::assertSentToTimes($this->otherFinalist->candidate, ProcessResultNotification::class, 1);
    }

    public function test_rf26_rf27_result_notifications_are_audited_without_personal_data(): void
    {
        Notification::fake();
        $this->decideAndSelect($this->vacancy, $this->chosen, $this->approver, $this->hr);
        $this->close($this->vacancy, $this->hr);

        $log = AuditLog::query()->where('action', AuditAction::ProcessResultNotified)->sole();
        $this->assertSame($this->organization->id, $log->organization_id);
        $this->assertSame($this->hr->id, $log->user_id);
        $this->assertSame('vacancy', $log->auditable_type);
        $this->assertSame($this->vacancy->id, $log->auditable_id);
        $this->assertSame(['selected' => 1, 'not_selected' => 2], $log->metadata);
    }
}
