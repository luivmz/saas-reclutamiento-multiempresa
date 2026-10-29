<?php

namespace Tests\Feature\Audit;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Enums\JobRequestStatus;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\JobRequestRejectedNotification;
use BackedEnum;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * SEG-04: the free-text comments of stage changes (RF-13, RF-14) and of job request transitions (RF-02 to RF-04)
 * belong to their functional history, not to the append-only audit metadata (RF-27). The audit event keeps the
 * actor, the organization, the action, the entity and the states before and after.
 *
 * Every comment is fictitious. The SEG04MARCA marker makes any copy detectable in audit_logs.metadata and in the
 * HTTP responses.
 */
class AuditMetadataMinimizationTest extends TestCase
{
    use RefreshDatabase;

    private const MARKER = 'SEG04MARCA';

    private Organization $organization;

    private User $hr;

    private User $approver;

    private User $requester;

    private Vacancy $vacancy;

    protected function setUp(): void
    {
        parent::setUp();

        Notification::fake();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->approver = User::factory()->approver($this->organization)->create();
        $this->requester = User::factory()->requester($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
    }

    public function test_rf13_rf14_rf27_seg04_stage_change_comments_stay_in_the_history_and_out_of_audit_metadata(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();
        $discarded = Application::factory()->for($this->vacancy)->create();

        $this->actingAs($this->hr)
            ->post(route('applications.shortlist', $application), ['comment' => $this->comment('PRESELECCION')])
            ->assertSessionHasNoErrors();
        $this->actingAs($this->hr)
            ->post(route('applications.stage', $application), ['status' => ApplicationStatus::Evaluation->value, 'comment' => $this->comment('ETAPA')])
            ->assertSessionHasNoErrors();
        $this->actingAs($this->hr)
            ->post(route('applications.discard', $discarded), ['comment' => $this->comment('DESCARTE')])
            ->assertSessionHasNoErrors();

        // The legitimate place of each comment: the stage history of the internal file (RF-12).
        $this->assertSame(
            [null, $this->comment('PRESELECCION'), $this->comment('ETAPA')],
            $application->stageHistories()->orderBy('id')->pluck('comment')->all(),
        );
        $this->assertSame($this->comment('DESCARTE'), $discarded->stageHistories()->latest('id')->value('comment'));

        $this->assertStateOnlyEvents(AuditAction::ApplicationStageChanged, $application, $this->hr, [
            [ApplicationStatus::Submitted, ApplicationStatus::Shortlisted],
            [ApplicationStatus::Shortlisted, ApplicationStatus::Evaluation],
        ]);
        $this->assertStateOnlyEvents(AuditAction::ApplicationStageChanged, $discarded, $this->hr, [
            [ApplicationStatus::Submitted, ApplicationStatus::Discarded],
        ]);
        $this->assertMarkerNeverStoredInAuditMetadata();
    }

    public function test_rf02_rf04_rf27_seg04_job_request_comments_stay_in_the_request_and_out_of_audit_metadata(): void
    {
        $observed = JobRequest::factory()->requestedBy($this->requester)->create();
        $approved = JobRequest::factory()->requestedBy($this->requester)->validated()->create();
        $rejected = JobRequest::factory()->requestedBy($this->requester)->validated()->create();

        $this->actingAs($this->requester)->post(route('job-requests.submit', $observed))->assertSessionHasNoErrors();
        $this->actingAs($this->hr)
            ->post(route('job-requests.observe', $observed), ['comment' => $this->comment('OBSERVACION')])
            ->assertSessionHasNoErrors();
        $this->actingAs($this->approver)
            ->post(route('job-requests.decide', $approved), ['decision' => 'aprobar', 'comment' => $this->comment('APROBACION')])
            ->assertSessionHasNoErrors();
        $this->actingAs($this->approver)
            ->post(route('job-requests.decide', $rejected), ['decision' => 'rechazar', 'comment' => $this->comment('RECHAZO')])
            ->assertSessionHasNoErrors();

        // The legitimate places of each comment: the request itself, its status history and the rejection notice.
        $this->assertSame($this->comment('OBSERVACION'), $observed->fresh()->observation);
        $this->assertSame($this->comment('APROBACION'), $approved->fresh()->decision_comment);
        $this->assertSame($this->comment('RECHAZO'), $rejected->fresh()->decision_comment);
        $this->assertSame([null, $this->comment('OBSERVACION')], $observed->statusHistories()->orderBy('id')->pluck('comment')->all());
        $this->assertSame([$this->comment('APROBACION')], $approved->statusHistories()->pluck('comment')->all());
        $this->assertSame([$this->comment('RECHAZO')], $rejected->statusHistories()->pluck('comment')->all());
        Notification::assertSentTo($this->requester, JobRequestRejectedNotification::class);

        $this->assertStateOnlyEvents(AuditAction::JobRequestSubmitted, $observed, $this->requester, [[JobRequestStatus::Draft, JobRequestStatus::Submitted]]);
        $this->assertStateOnlyEvents(AuditAction::JobRequestObserved, $observed, $this->hr, [[JobRequestStatus::Submitted, JobRequestStatus::Observed]]);
        $this->assertStateOnlyEvents(AuditAction::JobRequestApproved, $approved, $this->approver, [[JobRequestStatus::Validated, JobRequestStatus::Approved]]);
        $this->assertStateOnlyEvents(AuditAction::JobRequestRejected, $rejected, $this->approver, [[JobRequestStatus::Validated, JobRequestStatus::Rejected]]);
        $this->assertMarkerNeverStoredInAuditMetadata();
    }

    public function test_rf27_seg04_audit_trail_view_never_returned_the_comments(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();
        $jobRequest = JobRequest::factory()->requestedBy($this->requester)->submitted()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.shortlist', $application), ['comment' => $this->comment('PRESELECCION')])
            ->assertSessionHasNoErrors();
        $this->actingAs($this->hr)
            ->post(route('job-requests.observe', $jobRequest), ['comment' => $this->comment('OBSERVACION')])
            ->assertSessionHasNoErrors();

        // A-33: Direction reads a whitelisted summary, without raw metadata, IP address or free texts.
        $this->actingAs($this->approver)
            ->get(route('audit.index'))
            ->assertOk()
            ->assertDontSee(self::MARKER, false)
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('audit/index')
                ->has('logs.data', 2)
                ->where('logs.data', fn ($logs) => collect($logs)->every(fn ($log) => ! array_key_exists('metadata', $log)
                    && ! array_key_exists('ip_address', $log)
                    && collect($log['details'])->pluck('label')->all() === ['Estado anterior', 'Estado nuevo'])));

        // Only Direction audits, and only its own organization.
        $this->actingAs($this->hr)->get(route('audit.index'))->assertForbidden();
        $this->actingAs(User::factory()->approver(Organization::factory()->create())->create())
            ->get(route('audit.index'))
            ->assertOk()
            ->assertDontSee(self::MARKER, false)
            ->assertInertia(fn (AssertableInertia $page) => $page->has('logs.data', 0));
    }

    public function test_rf02_rf12_seg04_authorized_history_keeps_the_comment_and_the_candidate_never_sees_it(): void
    {
        $application = Application::factory()->for($this->vacancy)->create();
        $jobRequest = JobRequest::factory()->requestedBy($this->requester)->submitted()->create();

        $this->actingAs($this->hr)
            ->post(route('applications.shortlist', $application), ['comment' => $this->comment('PRESELECCION')])
            ->assertSessionHasNoErrors();
        $this->actingAs($this->hr)
            ->post(route('job-requests.observe', $jobRequest), ['comment' => $this->comment('OBSERVACION')])
            ->assertSessionHasNoErrors();

        foreach ([$this->hr, $this->approver] as $staff) {
            $this->actingAs($staff)
                ->get(route('applications.show', $application))
                ->assertOk()
                ->assertInertia(fn (AssertableInertia $page) => $page->where('history.1.comment', $this->comment('PRESELECCION')));
        }

        // The requester needs the observation to correct the request (RF-02).
        $this->actingAs($this->requester)
            ->get(route('job-requests.show', $jobRequest))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('jobRequest.observation', $this->comment('OBSERVACION'))
                ->where('history.0.comment', $this->comment('OBSERVACION')));

        // A-21: the candidate follows the application without internal comments.
        $this->actingAs($application->candidate)
            ->get(route('candidate.applications.show', $application))
            ->assertOk()
            ->assertDontSee(self::MARKER, false);

        // Staff of another organization receives nothing.
        $other = Organization::factory()->create();
        $this->actingAs(User::factory()->hr($other)->create())
            ->get(route('applications.show', $application))
            ->assertNotFound()
            ->assertDontSee(self::MARKER, false);
        $this->actingAs(User::factory()->approver($other)->create())
            ->get(route('job-requests.show', $jobRequest))
            ->assertNotFound()
            ->assertDontSee(self::MARKER, false);
    }

    private function comment(string $tag): string
    {
        return self::MARKER."-{$tag}: motivo ficticio con un DNI inventado 00000000 y un dato de salud inventado.";
    }

    /**
     * Each event of the subject keeps actor, organization and entity, and exactly the states before and after.
     *
     * @param  list<array{0: BackedEnum, 1: BackedEnum}>  $transitions
     */
    private function assertStateOnlyEvents(AuditAction $action, Model $subject, User $actor, array $transitions): void
    {
        $logs = AuditLog::query()->withoutGlobalScopes()
            ->where('action', $action)
            ->where('auditable_type', $subject->getMorphClass())
            ->where('auditable_id', $subject->getKey())
            ->orderBy('id')
            ->get();

        $this->assertCount(count($transitions), $logs);

        foreach ($logs as $index => $log) {
            [$from, $to] = $transitions[$index];

            $this->assertSame($actor->id, $log->user_id);
            $this->assertSame($this->organization->id, $log->organization_id);
            $this->assertEquals(
                ['from' => $from->value, 'to' => $to->value],
                $log->metadata,
                "{$action->value} stored more than the states in audit_logs.metadata.",
            );
        }
    }

    private function assertMarkerNeverStoredInAuditMetadata(): void
    {
        $this->assertSame(
            0,
            AuditLog::query()->withoutGlobalScopes()->whereRaw('metadata::text like ?', ['%'.self::MARKER.'%'])->count(),
            'A synthetic comment reached audit_logs.metadata.',
        );
    }
}
