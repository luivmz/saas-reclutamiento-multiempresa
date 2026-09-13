<?php

namespace App\Policies;

use App\Models\Evaluation;
use App\Models\User;
use App\Policies\Concerns\AuthorizesAssessmentSessions;

class EvaluationPolicy
{
    use AuthorizesAssessmentSessions;

    public function view(User $user, Evaluation $evaluation): bool
    {
        return $this->canViewSession($user, $evaluation);
    }

    public function recordResult(User $user, Evaluation $evaluation): bool
    {
        return $this->isAssignedEvaluator($user, $evaluation);
    }
}
