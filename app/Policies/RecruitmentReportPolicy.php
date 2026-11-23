<?php

namespace App\Policies;

use App\Enums\UserRole;
use App\Models\User;

/**
 * RF-28 (candidato): reportes operativos del proceso de reclutamiento.
 *
 * Solo RR. HH. y Aprobador/Dirección de una organización consultan los
 * indicadores, y siempre los de su propia organización: el servicio filtra por
 * `organization_id`. Postulantes, evaluadores y áreas solicitantes no acceden.
 */
class RecruitmentReportPolicy
{
    public function view(User $user): bool
    {
        return $user->organization_id !== null
            && $user->hasRole(UserRole::HumanResources, UserRole::Approver);
    }
}
