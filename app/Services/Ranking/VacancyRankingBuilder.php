<?php

namespace App\Services\Ranking;

use App\Enums\ApplicationStatus;
use App\Enums\AssessmentStatus;
use App\Models\Application;
use App\Models\EvaluationCriterion;
use App\Models\EvaluationResult;
use App\Models\InterviewResult;
use App\Models\Vacancy;

/**
 * Loads the ranking inputs of a single vacancy. Only applications of that vacancy and of its own organization are
 * considered; discarded applications are excluded and only results of completed sessions count (docs/assumptions.md A-23).
 */
class VacancyRankingBuilder
{
    public function __construct(private readonly RankingService $ranking) {}

    public function forVacancy(Vacancy $vacancy): RankingResult
    {
        $applications = Application::query()
            ->withoutGlobalScopes()
            ->where('vacancy_id', $vacancy->id)
            ->where('organization_id', $vacancy->organization_id)
            ->where('status', '!=', ApplicationStatus::Discarded)
            ->with('candidate:id,name')
            ->orderBy('id')
            ->get();

        $scores = $this->recordedScores($vacancy, $applications->modelKeys());

        $candidates = $applications->map(fn (Application $application) => new CandidateScores(
            $application->id,
            $application->candidate->name,
            $scores[$application->id] ?? [],
        ))->all();

        return $this->ranking->rank(EvaluationCriterion::definitionsFor($vacancy->id), $candidates);
    }

    /**
     * @param  list<int>  $applicationIds
     * @return array<int, array<int, list<float>>> scores keyed by application id and criterion id
     */
    private function recordedScores(Vacancy $vacancy, array $applicationIds): array
    {
        $scores = [];

        $sources = [
            [EvaluationResult::class, 'evaluations', 'evaluation_results', 'evaluation_id'],
            [InterviewResult::class, 'interviews', 'interview_results', 'interview_id'],
        ];

        foreach ($sources as [$model, $sessions, $results, $foreignKey]) {
            $rows = $model::query()
                ->withoutGlobalScopes()
                ->toBase()
                ->join($sessions, "{$sessions}.id", '=', "{$results}.{$foreignKey}")
                ->whereIn("{$sessions}.application_id", $applicationIds)
                ->where("{$sessions}.organization_id", $vacancy->organization_id)
                ->where("{$sessions}.status", AssessmentStatus::Completed->value)
                ->orderBy("{$results}.id")
                ->get(["{$sessions}.application_id", "{$results}.evaluation_criterion_id", "{$results}.score"]);

            foreach ($rows as $row) {
                $scores[(int) $row->application_id][(int) $row->evaluation_criterion_id][] = (float) $row->score;
            }
        }

        return $scores;
    }
}
