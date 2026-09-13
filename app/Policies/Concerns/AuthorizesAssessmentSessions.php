<?php

namespace App\Policies\Concerns;

use App\Enums\UserRole;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\User;

trait AuthorizesAssessmentSessions
{
    protected function canViewSession(User $user, Evaluation|Interview $session): bool
    {
        if (! $user->sharesOrganizationWith($session)) {
            return false;
        }

        return $user->hasRole(UserRole::HumanResources, UserRole::Approver)
            || $this->isAssignedEvaluator($user, $session);
    }

    protected function isAssignedEvaluator(User $user, Evaluation|Interview $session): bool
    {
        return $user->hasRole(UserRole::Evaluator)
            && $user->sharesOrganizationWith($session)
            && $session->evaluator_id === $user->id;
    }
}
