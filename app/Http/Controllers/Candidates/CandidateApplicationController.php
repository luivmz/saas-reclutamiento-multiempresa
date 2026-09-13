<?php

namespace App\Http\Controllers\Candidates;

use App\Http\Controllers\Controller;
use App\Http\Resources\ApplicationResource;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\Evaluation;
use App\Models\Interview;
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

        $application->load([...$this->vacancyRelations(), 'stageHistories', 'evaluations', 'interviews']);

        return Inertia::render('candidate/applications/show', [
            'application' => new ApplicationResource($application),
            'timeline' => $application->stageHistories->sortBy('id')->values()->map(fn (ApplicationStageHistory $history) => [
                'id' => $history->id,
                'to' => $history->to_status->present(),
                'created_at' => $history->created_at->toIso8601String(),
            ]),
            // RF-17: convocations only; scores, observations and outcomes are never exposed to the candidate (A-21).
            'convocations' => $application->evaluations
                ->map(fn (Evaluation $evaluation) => $this->convocation($evaluation, 'evaluacion', $evaluation->type->label()))
                ->concat($application->interviews->map(fn (Interview $interview) => $this->convocation($interview, 'entrevista', 'Entrevista personal')))
                ->sortBy('scheduled_at')
                ->values(),
        ]);
    }

    /**
     * @return array<string, mixed>
     */
    private function convocation(Evaluation|Interview $session, string $kind, string $title): array
    {
        return [
            'key' => $kind.'-'.$session->id,
            'title' => $title,
            'scheduled_at' => $session->scheduled_at->toIso8601String(),
            'duration_minutes' => $session->duration_minutes,
            'modality' => $session->modality->label(),
            'location' => $session->location,
            'instructions' => $session->instructions,
            'status' => $session->status->present(),
        ];
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
