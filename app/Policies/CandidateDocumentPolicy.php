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
    /**
     * A-04, A-11 and A-12 (SEG-03): staff reach a CV only through an application of their organization that presented
     * exactly that document, and an evaluator only through a session assigned to them on such an application. Neither
     * another application of the candidate nor their latest CV stands in for it.
     */
    public function download(User $user, CandidateDocument $document): bool
    {
        $ownerId = $document->profile->user_id;

        if ($user->id === $ownerId) {
            return true;
        }

        if ($user->organization_id === null) {
            return false;
        }

        $presented = Application::query()
            ->withoutGlobalScopes()
            ->where('candidate_id', $ownerId)
            ->where('organization_id', $user->organization_id)
            ->where('candidate_document_id', $document->id);

        if ($user->hasRole(UserRole::HumanResources, UserRole::Approver)) {
            return $presented->exists();
        }

        if ($user->hasRole(UserRole::Evaluator)) {
            return $this->isAssignedTo(Evaluation::query(), $user, $presented)
                || $this->isAssignedTo(Interview::query(), $user, $presented);
        }

        return false;
    }

    /**
     * @param  Builder<Evaluation>|Builder<Interview>  $sessions
     * @param  Builder<Application>  $applications
     */
    private function isAssignedTo(Builder $sessions, User $evaluator, Builder $applications): bool
    {
        return $sessions
            ->withoutGlobalScopes()
            ->where('evaluator_id', $evaluator->id)
            ->where('organization_id', $evaluator->organization_id)
            ->whereIn('application_id', (clone $applications)->select('id'))
            ->exists();
    }
}
