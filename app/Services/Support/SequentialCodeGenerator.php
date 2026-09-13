<?php

namespace App\Services\Support;

use Illuminate\Database\Eloquent\Model;

/**
 * Generates per-organization, per-year codes such as REQ-2026-0001. The unique index on (organization_id, code) backs it.
 */
class SequentialCodeGenerator
{
    /**
     * @param  class-string<Model>  $modelClass
     */
    public function next(string $modelClass, string $prefix, int $organizationId): string
    {
        $pattern = sprintf('%s-%d-', $prefix, now()->year);

        $last = $modelClass::query()
            ->withoutGlobalScopes()
            ->where('organization_id', $organizationId)
            ->where('code', 'like', $pattern.'%')
            ->orderByDesc('code')
            ->lockForUpdate()
            ->value('code');

        $sequence = $last === null ? 1 : ((int) substr($last, strlen($pattern))) + 1;

        return $pattern.str_pad((string) $sequence, 4, '0', STR_PAD_LEFT);
    }
}
