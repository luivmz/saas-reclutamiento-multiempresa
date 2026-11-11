<?php

namespace App\Policies;

use App\Enums\EvidenceType;
use App\Enums\UserRole;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvidenceItem;
use App\Models\Interview;
use App\Models\User;

/**
 * EXPERIMENTAL (F37 flow, exp/evidencias-ml02). Role matrix of F37 §4 plus R-01 (same organization for actor,
 * application, vacancy and evidence), R-02 (an evaluator acts only on applications with a session assigned to them)
 * and R-08 (a closed vacancy freezes its evidence). Whatever is not listed is denied.
 *
 * Direction only reads: the final decision stays human and theirs (RF-23); evidence never feeds the ranking.
 */
class EvidenceItemPolicy
{
    /** consultar */
    public function viewAny(User $user, Application $application): bool
    {
        if (! $this->sameOrganization($user, $application)) {
            return false;
        }

        return $user->hasRole(UserRole::HumanResources, UserRole::Approver)
            || $this->isAssignedEvaluator($user, $application);
    }

    /** historial */
    public function viewHistory(User $user, Application $application): bool
    {
        return $this->sameOrganization($user, $application)
            && $user->hasRole(UserRole::HumanResources, UserRole::Approver);
    }

    /** registrar */
    public function create(User $user, Application $application): bool
    {
        return $this->canWrite($user, $application)
            && ($user->hasRole(UserRole::HumanResources) || $this->isAssignedEvaluator($user, $application));
    }

    /** enlazar y desenlazar */
    public function link(User $user, EvidenceItem $evidence): bool
    {
        $application = $evidence->application;

        return $this->sameEvidenceOrganization($evidence)
            && $this->canWrite($user, $application)
            && ($user->hasRole(UserRole::HumanResources) || $this->isAssignedEvaluator($user, $application));
    }

    /** revisar */
    public function review(User $user, EvidenceItem $evidence): bool
    {
        return $this->sameEvidenceOrganization($evidence)
            && $this->canWrite($user, $evidence->application)
            && $user->hasRole(UserRole::HumanResources);
    }

    /**
     * corregir: authorized by the original evidence before looking at the replacement data (CONT-M01). An
     * observation is corrected only by its author; an evaluator corrects only their own observations.
     */
    public function correct(User $user, EvidenceItem $evidence): bool
    {
        $application = $evidence->application;

        if (! $this->sameEvidenceOrganization($evidence) || ! $this->canWrite($user, $application)) {
            return false;
        }

        $isAuthor = $evidence->registered_by !== null && $evidence->registered_by === $user->id;

        if ($evidence->type === EvidenceType::Observation && ! $isAuthor) {
            return false;
        }

        return $user->hasRole(UserRole::HumanResources)
            || ($this->isAssignedEvaluator($user, $application) && $isAuthor);
    }

    /** retirar */
    public function withdraw(User $user, EvidenceItem $evidence): bool
    {
        return $this->sameEvidenceOrganization($evidence)
            && $this->canWrite($user, $evidence->application)
            && $user->hasRole(UserRole::HumanResources);
    }

    private function canWrite(User $user, Application $application): bool
    {
        return $this->sameOrganization($user, $application) && ! $application->vacancy->isClosed();
    }

    private function sameOrganization(User $user, Application $application): bool
    {
        return $user->isStaff()
            && $user->sharesOrganizationWith($application)
            && $application->vacancy !== null
            && $application->vacancy->organization_id === $application->organization_id;
    }

    private function sameEvidenceOrganization(EvidenceItem $evidence): bool
    {
        return $evidence->organization_id === $evidence->application->organization_id;
    }

    private function isAssignedEvaluator(User $user, Application $application): bool
    {
        if (! $user->hasRole(UserRole::Evaluator) || ! $user->sharesOrganizationWith($application)) {
            return false;
        }

        $assigned = fn ($query) => $query
            ->where('application_id', $application->id)
            ->where('organization_id', $application->organization_id)
            ->where('evaluator_id', $user->id);

        return $assigned(Evaluation::query())->exists() || $assigned(Interview::query())->exists();
    }
}
