<?php

namespace App\Http\Presenters;

use App\Enums\AssessmentStatus;
use App\Enums\CriterionStage;
use App\Enums\InterviewOutcome;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvaluationResult;
use App\Models\Interview;
use App\Models\InterviewResult;
use App\Models\User;

/**
 * Props for evaluation/interview sessions, shared by the evaluator page and the HR application file.
 */
class AssessmentSessionPresenter
{
    /**
     * Evaluator session page (RF-19).
     *
     * @return array<string, mixed>
     */
    public function present(Evaluation|Interview $session, User $viewer): array
    {
        $session->load([
            'application.vacancy:id,organization_id,code,title,status',
            'application.candidate:id,name',
            'application.candidate.candidateProfile',
            'application.cvDocument',
            'results',
        ]);

        $kind = $this->kind($session);
        $application = $session->application;
        $profile = $application->candidate->candidateProfile;

        return [
            'session' => $this->base($session),
            'application' => [
                'id' => $application->id,
                'code' => $application->trackingCode(),
                'vacancy' => ['code' => $application->vacancy->code, 'title' => $application->vacancy->title],
                'candidate' => [
                    'name' => $application->candidate->name,
                    'professional_title' => $profile?->professional_title,
                    'years_of_experience' => $profile?->years_of_experience,
                    'education_level' => $profile?->education_level?->label(),
                ],
                'cv' => $application->cvDocument?->toSummary(),
            ],
            'criteria' => EvaluationCriterion::query()
                ->where('vacancy_id', $application->vacancy_id)
                ->where('stage', $kind)
                ->orderBy('position')
                ->orderBy('id')
                ->get()
                ->map(fn (EvaluationCriterion $criterion) => [
                    'id' => $criterion->id,
                    'name' => $criterion->name,
                    'weight' => $criterion->weight,
                    'min_score' => $criterion->min_score,
                    'max_score' => $criterion->max_score,
                ])
                ->values(),
            'results' => $session->results->map(fn (EvaluationResult|InterviewResult $result) => [
                'criterion_id' => $result->evaluation_criterion_id,
                'score' => $result->score,
                'comment' => $result->comment,
            ])->values(),
            'outcomes' => $kind === CriterionStage::Interview ? InterviewOutcome::options() : [],
            'can' => [
                'record' => $viewer->can('recordResult', $session)
                    && $session->status === AssessmentStatus::Scheduled
                    && ! $application->vacancy->isClosed(),
            ],
        ];
    }

    /**
     * Session summary with evaluator and results for the HR application file. Requires evaluator and results.criterion loaded.
     *
     * @return array<string, mixed>
     */
    public function summary(Evaluation|Interview $session): array
    {
        return [
            ...$this->base($session),
            'evaluator' => $session->evaluator->name,
            'results' => $session->results->map(fn (EvaluationResult|InterviewResult $result) => [
                'criterion' => $result->criterion->name,
                'score' => $result->score,
                'max_score' => $result->criterion->max_score,
                'comment' => $result->comment,
            ])->values(),
        ];
    }

    /**
     * @return array<string, mixed>
     */
    private function base(Evaluation|Interview $session): array
    {
        return [
            'id' => $session->id,
            'kind' => $this->kind($session)->present(),
            'title' => $session instanceof Evaluation ? $session->type->label() : 'Entrevista personal',
            'status' => $session->status->present(),
            'scheduled_at' => $session->scheduled_at->toIso8601String(),
            'duration_minutes' => $session->duration_minutes,
            'modality' => $session->modality->present(),
            'location' => $session->location,
            'instructions' => $session->instructions,
            'observations' => $session->observations,
            'outcome' => $session instanceof Interview ? $session->outcome?->present() : null,
            'completed_at' => $session->completed_at?->toIso8601String(),
        ];
    }

    private function kind(Evaluation|Interview $session): CriterionStage
    {
        return $session instanceof Evaluation ? CriterionStage::Evaluation : CriterionStage::Interview;
    }
}
