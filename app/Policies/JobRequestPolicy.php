<?php

namespace App\Policies;

use App\Enums\JobRequestStatus;
use App\Enums\UserRole;
use App\Models\JobRequest;
use App\Models\User;

class JobRequestPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->hasRole(UserRole::Requester, UserRole::HumanResources, UserRole::Approver);
    }

    public function view(User $user, JobRequest $jobRequest): bool
    {
        if (! $user->sharesOrganizationWith($jobRequest)) {
            return false;
        }

        if ($user->hasRole(UserRole::HumanResources, UserRole::Approver)) {
            return $jobRequest->status !== JobRequestStatus::Draft;
        }

        return $this->isOwner($user, $jobRequest);
    }

    public function create(User $user): bool
    {
        return $user->hasRole(UserRole::Requester);
    }

    public function update(User $user, JobRequest $jobRequest): bool
    {
        return $this->isOwner($user, $jobRequest);
    }

    public function submit(User $user, JobRequest $jobRequest): bool
    {
        return $this->isOwner($user, $jobRequest);
    }

    public function review(User $user, JobRequest $jobRequest): bool
    {
        return $user->hasRole(UserRole::HumanResources) && $user->sharesOrganizationWith($jobRequest);
    }

    public function decide(User $user, JobRequest $jobRequest): bool
    {
        return $user->hasRole(UserRole::Approver) && $user->sharesOrganizationWith($jobRequest);
    }

    private function isOwner(User $user, JobRequest $jobRequest): bool
    {
        return $user->hasRole(UserRole::Requester)
            && $user->sharesOrganizationWith($jobRequest)
            && $jobRequest->requested_by === $user->id;
    }
}
