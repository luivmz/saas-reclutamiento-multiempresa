<?php

namespace App\Policies;

use App\Enums\UserRole;
use App\Models\Application;
use App\Models\CandidateDocument;
use App\Models\User;

class CandidateDocumentPolicy
{
    public function download(User $user, CandidateDocument $document): bool
    {
        $ownerId = $document->profile->user_id;

        if ($user->id === $ownerId) {
            return true;
        }

        if ($user->organization_id === null || ! $user->hasRole(UserRole::HumanResources, UserRole::Approver)) {
            return false;
        }

        return Application::query()
            ->withoutGlobalScopes()
            ->where('candidate_id', $ownerId)
            ->where('organization_id', $user->organization_id)
            ->exists();
    }
}
