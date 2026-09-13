<?php

namespace App\Services\JobRequests;

use App\Enums\AuditAction;
use App\Enums\JobRequestStatus;
use App\Exceptions\BusinessRuleException;
use App\Exceptions\InvalidStateTransition;
use App\Models\JobRequest;
use App\Models\JobRequestStatusHistory;
use App\Models\User;
use App\Notifications\JobRequestRejectedNotification;
use App\Services\Audit\AuditLogger;
use App\Services\Support\SequentialCodeGenerator;
use Closure;
use Illuminate\Support\Facades\DB;

/**
 * RF-01 to RF-04: lifecycle of a personnel request.
 */
class JobRequestWorkflow
{
    public function __construct(
        private readonly AuditLogger $audit,
        private readonly SequentialCodeGenerator $codes,
    ) {}

    /**
     * @param  array<string, mixed>  $data
     */
    public function register(User $requester, array $data): JobRequest
    {
        return DB::transaction(function () use ($requester, $data): JobRequest {
            $jobRequest = new JobRequest($data);
            $jobRequest->organization_id = $requester->organization_id;
            $jobRequest->requested_by = $requester->id;
            $jobRequest->code = $this->codes->next(JobRequest::class, 'REQ', $requester->organization_id);
            $jobRequest->status = JobRequestStatus::Draft;
            $jobRequest->save();

            $this->recordHistory($jobRequest, null, JobRequestStatus::Draft, $requester, null);
            $this->audit->record(AuditAction::JobRequestCreated, $jobRequest, ['code' => $jobRequest->code], $requester);

            return $jobRequest;
        });
    }

    /**
     * @param  array<string, mixed>  $data
     */
    public function correct(JobRequest $jobRequest, User $requester, array $data): JobRequest
    {
        if (! $jobRequest->status->isEditable()) {
            throw new BusinessRuleException('Solo se puede modificar un requerimiento en borrador u observado.');
        }

        return DB::transaction(function () use ($jobRequest, $requester, $data): JobRequest {
            $jobRequest->fill($data);
            $changedFields = array_keys($jobRequest->getDirty());
            $jobRequest->save();

            $this->audit->record(AuditAction::JobRequestUpdated, $jobRequest, ['fields' => $changedFields], $requester);

            return $jobRequest;
        });
    }

    public function submit(JobRequest $jobRequest, User $requester): JobRequest
    {
        return $this->transition($jobRequest, JobRequestStatus::Submitted, $requester, null, AuditAction::JobRequestSubmitted,
            function (JobRequest $locked): void {
                $locked->submitted_at = now();
            });
    }

    public function observe(JobRequest $jobRequest, User $hr, string $comment): JobRequest
    {
        return $this->transition($jobRequest, JobRequestStatus::Observed, $hr, $comment, AuditAction::JobRequestObserved,
            function (JobRequest $locked) use ($comment): void {
                $locked->observation = $comment;
            });
    }

    public function validate(JobRequest $jobRequest, User $hr, ?string $comment = null): JobRequest
    {
        return $this->transition($jobRequest, JobRequestStatus::Validated, $hr, $comment, AuditAction::JobRequestValidated,
            function (JobRequest $locked) use ($hr): void {
                $locked->validated_by = $hr->id;
                $locked->validated_at = now();
                $locked->observation = null;
            });
    }

    public function approve(JobRequest $jobRequest, User $approver, ?string $comment = null): JobRequest
    {
        return $this->transition($jobRequest, JobRequestStatus::Approved, $approver, $comment, AuditAction::JobRequestApproved,
            $this->decision($approver, $comment));
    }

    public function reject(JobRequest $jobRequest, User $approver, string $comment): JobRequest
    {
        $rejected = $this->transition($jobRequest, JobRequestStatus::Rejected, $approver, $comment, AuditAction::JobRequestRejected,
            $this->decision($approver, $comment));

        $rejected->requester->notify(new JobRequestRejectedNotification($rejected));

        return $rejected;
    }

    /**
     * @return Closure(JobRequest): void
     */
    private function decision(User $approver, ?string $comment): Closure
    {
        return function (JobRequest $locked) use ($approver, $comment): void {
            $locked->decided_by = $approver->id;
            $locked->decided_at = now();
            $locked->decision_comment = $comment;
        };
    }

    /**
     * @param  Closure(JobRequest): void  $apply
     */
    private function transition(JobRequest $jobRequest, JobRequestStatus $target, User $actor, ?string $comment, AuditAction $action, Closure $apply): JobRequest
    {
        return DB::transaction(function () use ($jobRequest, $target, $actor, $comment, $action, $apply): JobRequest {
            $locked = JobRequest::query()->lockForUpdate()->findOrFail($jobRequest->getKey());
            $from = $locked->status;

            if (! $from->canTransitionTo($target)) {
                throw InvalidStateTransition::between('el requerimiento', $from->label(), $target->label());
            }

            $locked->status = $target;
            $apply($locked);
            $locked->save();

            $this->recordHistory($locked, $from, $target, $actor, $comment);
            $this->audit->record($action, $locked, array_filter([
                'from' => $from->value,
                'to' => $target->value,
                'comment' => $comment,
            ]), $actor);

            return $locked;
        });
    }

    private function recordHistory(JobRequest $jobRequest, ?JobRequestStatus $from, JobRequestStatus $to, User $actor, ?string $comment): void
    {
        $history = new JobRequestStatusHistory;
        $history->forceFill([
            'organization_id' => $jobRequest->organization_id,
            'job_request_id' => $jobRequest->id,
            'from_status' => $from,
            'to_status' => $to,
            'changed_by' => $actor->id,
            'comment' => $comment,
        ])->save();
    }
}
