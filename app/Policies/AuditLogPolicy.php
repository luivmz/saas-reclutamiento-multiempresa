<?php

namespace App\Policies;

use App\Enums\UserRole;
use App\Models\User;

/**
 * RF-27: only Direction (Approver) of the organization consults the audit trail (docs/assumptions.md A-33).
 * There are intentionally no update or delete abilities: audit records are append-only.
 */
class AuditLogPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->hasRole(UserRole::Approver) && $user->organization_id !== null;
    }
}
