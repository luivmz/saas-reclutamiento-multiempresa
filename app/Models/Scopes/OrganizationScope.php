<?php

namespace App\Models\Scopes;

use App\Models\User;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;
use Illuminate\Support\Facades\Auth;

/**
 * Restricts tenant-owned models to the organization of the authenticated staff user.
 * Candidates and guests are not scoped here: their access is limited explicitly by policies and queries.
 */
class OrganizationScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $user = Auth::user();

        if ($user instanceof User && $user->organization_id !== null) {
            $builder->where($model->qualifyColumn('organization_id'), $user->organization_id);
        }
    }
}
