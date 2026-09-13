<?php

namespace App\Http\Controllers\Audit;

use App\Enums\AuditAction;
use App\Http\Controllers\Controller;
use App\Http\Resources\AuditLogResource;
use App\Models\AuditLog;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-27: read-only audit trail of the user's organization.
 */
class AuditLogController extends Controller
{
    public function index(Request $request): Response
    {
        Gate::authorize('viewAny', AuditLog::class);

        $action = AuditAction::tryFrom((string) $request->query('accion'));

        $logs = AuditLog::query()
            ->where('organization_id', $request->user()->organization_id)
            ->when($action, fn ($query) => $query->where('action', $action))
            ->with('user:id,name')
            ->orderByDesc('created_at')
            ->orderByDesc('id')
            ->paginate(25)
            ->withQueryString();

        return Inertia::render('audit/index', [
            'logs' => AuditLogResource::collection($logs),
            'actions' => AuditAction::options(),
            'filters' => ['accion' => $action?->value],
        ]);
    }
}
