<?php

namespace App\Policies;

use App\Enums\UserRole;
use App\Models\Application;
use App\Models\User;
use App\Models\Vacancy;

class ApplicationPolicy
{
    public function viewAnyForVacancy(User $user, Vacancy $vacancy): bool
    {
        return $user->hasRole(UserRole::HumanResources, UserRole::Approver) && $user->sharesOrganizationWith($vacancy);
    }

    public function view(User $user, Application $application): bool
    {
        if ($user->isCandidate()) {
            return $application->candidate_id === $user->id;
        }

        return $user->hasRole(UserRole::HumanResources, UserRole::Approver) && $user->sharesOrganizationWith($application);
    }

    public function apply(User $user): bool
    {
        return $user->isCandidate();
    }

    public function changeStage(User $user, Application $application): bool
    {
        return $user->hasRole(UserRole::HumanResources) && $user->sharesOrganizationWith($application);
    }

    public function scheduleAssessment(User $user, Application $application): bool
    {
        return $user->hasRole(UserRole::HumanResources) && $user->sharesOrganizationWith($application);
    }
}
