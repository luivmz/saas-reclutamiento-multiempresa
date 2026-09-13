<?php

namespace App\Http\Controllers\Applications;

use App\Enums\ApplicationStatus;
use App\Enums\EvaluationType;
use App\Enums\Modality;
use App\Enums\UserRole;
use App\Http\Controllers\Controller;
use App\Http\Presenters\AssessmentSessionPresenter;
use App\Http\Resources\ApplicationResource;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\User;
use App\Services\Assessments\AssessmentScheduler;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-12: application file (expediente) for HR and Direction, including RF-16 to RF-19 sessions.
 */
class ApplicationController extends Controller
{
    public function __invoke(Request $request, Application $application, AssessmentSessionPresenter $sessions): Response
    {
        Gate::authorize('view', $application);

        $application->load([
            'vacancy:id,organization_id,code,title,status',
            'candidate:id,name,email',
            'candidate.candidateProfile',
            'cvDocument',
            'stageHistories.author:id,name',
            'evaluations' => fn ($query) => $query->orderBy('scheduled_at'),
            'evaluations.evaluator:id,name',
            'evaluations.results.criterion:id,name,max_score',
            'interviews' => fn ($query) => $query->orderBy('scheduled_at'),
            'interviews.evaluator:id,name',
            'interviews.results.criterion:id,name,max_score',
        ]);

        $user = $request->user();
        $status = $application->status;
        $isOpen = ! $application->vacancy->isClosed();
        $canChangeStage = $user->can('changeStage', $application) && $isOpen && ! $status->isTerminal();
        $canSchedule = $user->can('scheduleAssessment', $application) && $isOpen;

        return Inertia::render('applications/show', [
            'application' => new ApplicationResource($application),
            'history' => $application->stageHistories->sortBy('id')->values()
                ->map(fn (ApplicationStageHistory $history) => $history->toTimelineEntry()),
            'stageOptions' => collect(ApplicationStatus::manualTargets())
                ->filter(fn (ApplicationStatus $target) => $status->canTransitionTo($target))
                ->map(fn (ApplicationStatus $target) => $target->present())
                ->values(),
            'assessments' => [
                'evaluations' => $application->evaluations->map(fn (Evaluation $evaluation) => $sessions->summary($evaluation))->values(),
                'interviews' => $application->interviews->map(fn (Interview $interview) => $sessions->summary($interview))->values(),
            ],
            'scheduling' => $canSchedule ? [
                'evaluators' => User::query()
                    ->where('organization_id', $application->organization_id)
                    ->where('role', UserRole::Evaluator)
                    ->orderBy('name')
                    ->get(['id', 'name'])
                    ->map(fn (User $evaluator) => ['value' => (string) $evaluator->id, 'label' => $evaluator->name]),
                'evaluationTypes' => EvaluationType::options(),
                'modalities' => Modality::options(),
            ] : null,
            'can' => [
                'changeStage' => $canChangeStage,
                'scheduleEvaluation' => $canSchedule && AssessmentScheduler::acceptsEvaluation($status),
                'scheduleInterview' => $canSchedule && AssessmentScheduler::acceptsInterview($status),
            ],
        ]);
    }
}
