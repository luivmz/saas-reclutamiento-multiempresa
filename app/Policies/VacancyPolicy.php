<?php

namespace App\Policies;

use App\Enums\UserRole;
use App\Models\User;
use App\Models\Vacancy;

class VacancyPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->hasRole(UserRole::HumanResources, UserRole::Approver);
    }

    public function view(User $user, Vacancy $vacancy): bool
    {
        return $this->viewAny($user) && $user->sharesOrganizationWith($vacancy);
    }

    public function create(User $user): bool
    {
        return $user->hasRole(UserRole::HumanResources);
    }

    public function update(User $user, Vacancy $vacancy): bool
    {
        return $this->manages($user, $vacancy);
    }

    public function publish(User $user, Vacancy $vacancy): bool
    {
        return $this->manages($user, $vacancy);
    }

    private function manages(User $user, Vacancy $vacancy): bool
    {
        return $user->hasRole(UserRole::HumanResources) && $user->sharesOrganizationWith($vacancy);
    }
}
