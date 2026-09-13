<?php

namespace App\Http\Controllers\Selection;

use App\Enums\VacancyStatus;
use App\Http\Controllers\Controller;
use App\Http\Presenters\RankingPresenter;
use App\Http\Resources\VacancyResource;
use App\Models\Application;
use App\Models\EvaluationCriterion;
use App\Models\SelectionDecision;
use App\Models\Vacancy;
use App\Services\Ranking\InvalidRankingInput;
use App\Services\Ranking\RankingResult;
use App\Services\Ranking\VacancyRankingBuilder;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-21 and RF-22: ranking and comparison as decision support, plus the entry points for RF-23 to RF-25.
 */
class VacancyComparisonController extends Controller
{
    public function __invoke(Request $request, Vacancy $vacancy, VacancyRankingBuilder $builder, RankingPresenter $presenter): Response
    {
        Gate::authorize('viewRanking', $vacancy);

        try {
            $result = $builder->forVacancy($vacancy);
            $rankingError = null;
        } catch (InvalidRankingInput $exception) {
            $result = new RankingResult([], []);
            $rankingError = $exception->getMessage();
        }

        $vacancy->load(['criteria', 'closer:id,name']);
        $applications = Application::query()->where('vacancy_id', $vacancy->id)->get(['id', 'organization_id', 'vacancy_id', 'status'])->keyBy('id');
        $decision = SelectionDecision::query()
            ->where('vacancy_id', $vacancy->id)
            ->with(['selectedApplication:id,organization_id,candidate_id', 'selectedApplication.candidate:id,name', 'decider:id,name', 'selectionRegistrar:id,name'])
            ->first();

        $user = $request->user();
        $isPublished = $vacancy->status === VacancyStatus::Published;

        return Inertia::render('selection/comparison', [
            'vacancy' => new VacancyResource($vacancy),
            'criteria' => $vacancy->criteria->map(fn (EvaluationCriterion $criterion) => [
                'id' => $criterion->id,
                'name' => $criterion->name,
                'stage' => $criterion->stage->present(),
                'weight' => $criterion->weight,
                'min_score' => $criterion->min_score,
                'max_score' => $criterion->max_score,
            ])->values(),
            'ranking' => $presenter->present($result, $applications),
            'rankingError' => $rankingError,
            'formula' => RankingPresenter::FORMULA,
            'decision' => $decision === null ? null : [
                'application_id' => $decision->selected_application_id,
                'candidate_name' => $decision->selectedApplication->candidate->name,
                'justification' => $decision->justification,
                'selected_position' => $decision->selected_position,
                'selected_score' => $decision->selected_score,
                'ranked_candidates' => $decision->ranked_candidates,
                'decided_by' => $decision->decider->name,
                'decided_at' => $decision->decided_at->toIso8601String(),
                'selection_registered_by' => $decision->selectionRegistrar?->name,
                'selection_registered_at' => $decision->selection_registered_at?->toIso8601String(),
            ],
            'closedBy' => $vacancy->closer?->name,
            'can' => [
                'decide' => $user->can('decide', $vacancy) && $isPublished && $decision === null && $rankingError === null,
                'registerSelection' => $user->can('registerSelection', $vacancy) && $isPublished && $decision !== null && ! $decision->isSelectionRegistered(),
                'close' => $user->can('close', $vacancy) && $isPublished && $decision !== null && $decision->isSelectionRegistered(),
            ],
        ]);
    }
}
