<?php

namespace App\Http\Controllers\Applications;

use App\Enums\ApplicationStatus;
use App\Http\Controllers\Controller;
use App\Http\Resources\ApplicationResource;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-12: application file (expediente) for HR and Direction.
 */
class ApplicationController extends Controller
{
    public function __invoke(Request $request, Application $application): Response
    {
        Gate::authorize('view', $application);

        $application->load([
            'vacancy:id,organization_id,code,title,status',
            'candidate:id,name,email',
            'candidate.candidateProfile',
            'cvDocument',
            'stageHistories.author:id,name',
        ]);

        $status = $application->status;
        $canChangeStage = $request->user()->can('changeStage', $application)
            && ! $application->vacancy->isClosed()
            && ! $status->isTerminal();

        return Inertia::render('applications/show', [
            'application' => new ApplicationResource($application),
            'history' => $application->stageHistories->sortBy('id')->values()
                ->map(fn (ApplicationStageHistory $history) => $history->toTimelineEntry()),
            'stageOptions' => collect(ApplicationStatus::manualTargets())
                ->filter(fn (ApplicationStatus $target) => $status->canTransitionTo($target))
                ->map(fn (ApplicationStatus $target) => $target->present())
                ->values(),
            'can' => ['changeStage' => $canChangeStage],
        ]);
    }
}
