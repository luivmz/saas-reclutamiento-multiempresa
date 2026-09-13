<?php

namespace App\Services\Assessments;

use App\Enums\AssessmentStatus;
use App\Enums\AuditAction;
use App\Enums\CriterionStage;
use App\Enums\InterviewOutcome;
use App\Exceptions\BusinessRuleException;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvaluationResult;
use App\Models\Interview;
use App\Models\InterviewResult;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

/**
 * RF-19 (interview result) and evaluation results, validated with ScoreSheetValidator (RF-20).
 */
class AssessmentResultRecorder
{
    public function __construct(
        private readonly ScoreSheetValidator $validator,
        private readonly AuditLogger $audit,
    ) {}

    /**
     * @param  array<int, array{score: mixed, comment?: string|null}>  $scores
     */
    public function recordEvaluation(Evaluation $evaluation, User $evaluator, array $scores, ?string $observations): Evaluation
    {
        return DB::transaction(function () use ($evaluation, $evaluator, $scores, $observations): Evaluation {
            $locked = Evaluation::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($evaluation->getKey());
            $definitions = $this->guardAndValidate($locked, CriterionStage::Evaluation, $scores);

            foreach (array_keys($definitions) as $criterionId) {
                $result = new EvaluationResult;
                $result->forceFill([
                    'organization_id' => $locked->organization_id,
                    'evaluation_id' => $locked->id,
                    'evaluation_criterion_id' => $criterionId,
                    'score' => (float) $scores[$criterionId]['score'],
                    'comment' => $scores[$criterionId]['comment'] ?? null,
                ])->save();
            }

            $locked->forceFill([
                'status' => AssessmentStatus::Completed,
                'completed_at' => now(),
                'observations' => $observations,
            ])->save();

            $this->audit->record(AuditAction::EvaluationResultRecorded, $locked, ['criteria' => count($definitions)], $evaluator);

            return $locked;
        });
    }

    /**
     * @param  array<int, array{score: mixed, comment?: string|null}>  $scores
     */
    public function recordInterview(Interview $interview, User $evaluator, array $scores, InterviewOutcome $outcome, string $observations): Interview
    {
        return DB::transaction(function () use ($interview, $evaluator, $scores, $outcome, $observations): Interview {
            $locked = Interview::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($interview->getKey());
            $definitions = $this->guardAndValidate($locked, CriterionStage::Interview, $scores);

            foreach (array_keys($definitions) as $criterionId) {
                $result = new InterviewResult;
                $result->forceFill([
                    'organization_id' => $locked->organization_id,
                    'interview_id' => $locked->id,
                    'evaluation_criterion_id' => $criterionId,
                    'score' => (float) $scores[$criterionId]['score'],
                    'comment' => $scores[$criterionId]['comment'] ?? null,
                ])->save();
            }

            $locked->forceFill([
                'status' => AssessmentStatus::Completed,
                'outcome' => $outcome,
                'completed_at' => now(),
                'observations' => $observations,
            ])->save();

            $this->audit->record(AuditAction::InterviewResultRecorded, $locked, [
                'criteria' => count($definitions),
                'outcome' => $outcome->value,
            ], $evaluator);

            return $locked;
        });
    }

    /**
     * @param  array<int, array{score: mixed, comment?: string|null}>  $scores
     * @return array<int, \App\Services\Evaluation\CriterionDefinition>
     */
    private function guardAndValidate(Evaluation|Interview $session, CriterionStage $stage, array $scores): array
    {
        if ($session->status !== AssessmentStatus::Scheduled) {
            throw new BusinessRuleException('Los resultados de esta sesión ya fueron registrados.');
        }

        $application = Application::query()->withoutGlobalScopes()->findOrFail($session->application_id);
        $vacancy = Vacancy::query()->withoutGlobalScopes()->findOrFail($application->vacancy_id);

        if ($vacancy->isClosed()) {
            throw new BusinessRuleException('La convocatoria está cerrada; no se pueden registrar resultados.');
        }

        $definitions = EvaluationCriterion::definitionsFor($vacancy->id, $stage);
        $errors = $this->validator->validate($definitions, array_map(fn (array $entry) => $entry['score'] ?? null, $scores));

        if ($errors !== []) {
            throw ValidationException::withMessages(
                collect($errors)->mapWithKeys(fn (string $message, int $id) => ["scores.{$id}.score" => $message])->all(),
            );
        }

        return $definitions;
    }
}
