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

    public function viewRanking(User $user, Vacancy $vacancy): bool
    {
        return $this->view($user, $vacancy);
    }

    /**
     * Riesgo operacional del proceso (Fase 16).
     *
     * Mismo alcance que ver la vacante: RR. HH. y Aprobador de la **misma**
     * organización. Un postulante nunca lo ve, y no porque se le oculte una
     * puntuación suya -- el modelo no puntúa personas --, sino porque es
     * información de gestión interna del proceso.
     */
    public function viewOperationalRisk(User $user, Vacancy $vacancy): bool
    {
        return $this->view($user, $vacancy);
    }

    public function decide(User $user, Vacancy $vacancy): bool
    {
        return $user->hasRole(UserRole::Approver) && $user->sharesOrganizationWith($vacancy);
    }

    public function registerSelection(User $user, Vacancy $vacancy): bool
    {
        return $this->manages($user, $vacancy);
    }

    public function close(User $user, Vacancy $vacancy): bool
    {
        return $this->manages($user, $vacancy);
    }

    private function manages(User $user, Vacancy $vacancy): bool
    {
        return $user->hasRole(UserRole::HumanResources) && $user->sharesOrganizationWith($vacancy);
    }
}
