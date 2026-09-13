<?php

namespace App\Http\Controllers\Candidates;

use App\Http\Controllers\Controller;
use App\Http\Resources\ApplicationResource;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

class CandidateApplicationController extends Controller
{
    public function index(Request $request): Response
    {
        $applications = Application::query()
            ->where('candidate_id', $request->user()->id)
            ->with($this->vacancyRelations())
            ->latest('applied_at')
            ->paginate(10);

        return Inertia::render('candidate/applications/index', [
            'applications' => ApplicationResource::collection($applications),
        ]);
    }

    public function show(Application $application): Response
    {
        Gate::authorize('view', $application);

        $application->load([...$this->vacancyRelations(), 'stageHistories']);

        return Inertia::render('candidate/applications/show', [
            'application' => new ApplicationResource($application),
            'timeline' => $application->stageHistories->sortBy('id')->values()->map(fn (ApplicationStageHistory $history) => [
                'id' => $history->id,
                'to' => $history->to_status->present(),
                'created_at' => $history->created_at->toIso8601String(),
            ]),
        ]);
    }

    /**
     * @return array<string, mixed>
     */
    private function vacancyRelations(): array
    {
        return [
            'vacancy' => fn (BelongsTo $query) => $query->withoutGlobalScopes()->select(['id', 'organization_id', 'code', 'title', 'status']),
            'vacancy.organization:id,name',
        ];
    }
}
