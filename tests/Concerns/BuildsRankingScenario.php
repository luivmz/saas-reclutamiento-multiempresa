<?php

namespace Tests\Concerns;

use App\Enums\ApplicationStatus;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvaluationResult;
use App\Models\Interview;
use App\Models\InterviewResult;
use App\Models\Vacancy;

/**
 * Builds applications with completed sessions for vacancies created with VacancyFactory::configured()
 * (criteria 0–20: «Conocimientos pedagógicos» 40, «Clase modelo» 30, «Entrevista personal» 30).
 */
trait BuildsRankingScenario
{
    protected function candidateWithScores(
        Vacancy $vacancy,
        ?float $knowledge,
        ?float $modelClass,
        ?float $interview,
        ApplicationStatus $status = ApplicationStatus::Finalist,
    ): Application {
        $application = Application::factory()->for($vacancy)->state(['status' => $status])->create();
        $criteria = EvaluationCriterion::query()->withoutGlobalScopes()->where('vacancy_id', $vacancy->id)->orderBy('position')->get();

        if ($knowledge !== null || $modelClass !== null) {
            $evaluation = Evaluation::factory()->forApplication($application)->completed()->create();

            foreach ([[$criteria[0], $knowledge], [$criteria[1], $modelClass]] as [$criterion, $score]) {
                if ($score !== null) {
                    (new EvaluationResult)->forceFill([
                        'organization_id' => $application->organization_id,
                        'evaluation_id' => $evaluation->id,
                        'evaluation_criterion_id' => $criterion->id,
                        'score' => $score,
                    ])->save();
                }
            }
        }

        if ($interview !== null) {
            $session = Interview::factory()->forApplication($application)->completed()->create();

            (new InterviewResult)->forceFill([
                'organization_id' => $application->organization_id,
                'interview_id' => $session->id,
                'evaluation_criterion_id' => $criteria[2]->id,
                'score' => $interview,
            ])->save();
        }

        return $application;
    }
}
