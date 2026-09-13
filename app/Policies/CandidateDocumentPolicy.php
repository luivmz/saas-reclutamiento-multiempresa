<?php

namespace App\Policies;

use App\Enums\UserRole;
use App\Models\Application;
use App\Models\CandidateDocument;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\User;
use Illuminate\Database\Eloquent\Builder;

class CandidateDocumentPolicy
{
    public function download(User $user, CandidateDocument $document): bool
    {
        $ownerId = $document->profile->user_id;

        if ($user->id === $ownerId) {
            return true;
        }

        if ($user->organization_id === null) {
            return false;
        }

        if ($user->hasRole(UserRole::HumanResources, UserRole::Approver)) {
            return Application::query()
                ->withoutGlobalScopes()
                ->where('candidate_id', $ownerId)
                ->where('organization_id', $user->organization_id)
                ->exists();
        }

        if ($user->hasRole(UserRole::Evaluator)) {
            return $this->isAssignedToCandidate(Evaluation::query(), $user, $ownerId)
                || $this->isAssignedToCandidate(Interview::query(), $user, $ownerId);
        }

        return false;
    }

    /**
     * @param  Builder<Evaluation>|Builder<Interview>  $sessions
     */
    private function isAssignedToCandidate(Builder $sessions, User $evaluator, int $candidateId): bool
    {
        return $sessions
            ->withoutGlobalScopes()
            ->where('evaluator_id', $evaluator->id)
            ->where('organization_id', $evaluator->organization_id)
            ->whereIn('application_id', Application::query()->withoutGlobalScopes()->where('candidate_id', $candidateId)->select('id'))
            ->exists();
    }
}
