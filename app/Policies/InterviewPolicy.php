<?php

namespace App\Policies;

use App\Models\Interview;
use App\Models\User;
use App\Policies\Concerns\AuthorizesAssessmentSessions;

class InterviewPolicy
{
    use AuthorizesAssessmentSessions;

    public function view(User $user, Interview $interview): bool
    {
        return $this->canViewSession($user, $interview);
    }

    public function recordResult(User $user, Interview $interview): bool
    {
        return $this->isAssignedEvaluator($user, $interview);
    }
}
