<?php

namespace App\Services\Assessments;

use App\Enums\ApplicationStatus;
use App\Enums\AssessmentStatus;
use App\Enums\AuditAction;
use App\Enums\CriterionStage;
use App\Enums\UserRole;
use App\Exceptions\BusinessRuleException;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\Interview;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\AssessmentAssignedNotification;
use App\Notifications\AssessmentConvocationNotification;
use App\Services\Applications\ApplicationStageService;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;

/**
 * RF-16 (evaluation), RF-17 (convocation) and RF-18 (interview). See docs/assumptions.md A-16 to A-18.
 */
class AssessmentScheduler
{
    private const EVALUATION_STAGES = [ApplicationStatus::Shortlisted, ApplicationStatus::Evaluation];

    private const INTERVIEW_STAGES = [ApplicationStatus::Shortlisted, ApplicationStatus::Evaluation, ApplicationStatus::Interview];

    public function __construct(
        private readonly ApplicationStageService $stages,
        private readonly AuditLogger $audit,
    ) {}

    public static function acceptsEvaluation(ApplicationStatus $status): bool
    {
        return in_array($status, self::EVALUATION_STAGES, true);
    }

    public static function acceptsInterview(ApplicationStatus $status): bool
    {
        return in_array($status, self::INTERVIEW_STAGES, true);
    }

    /**
     * @param  array<string, mixed>  $data
     */
    public function scheduleEvaluation(Application $application, User $hr, array $data): Evaluation
    {
        [$evaluation, $locked, $vacancy] = DB::transaction(function () use ($application, $hr, $data): array {
            [$locked, $vacancy] = $this->lockForScheduling($application, CriterionStage::Evaluation);

            if (! self::acceptsEvaluation($locked->status)) {
                throw new BusinessRuleException('Solo se pueden programar evaluaciones para postulaciones preseleccionadas o en evaluación.');
            }

            $evaluation = new Evaluation;
            $evaluation->forceFill([...$this->sessionAttributes($locked, $hr, $data), 'type' => $data['type']])->save();

            $this->advanceStage($locked, ApplicationStatus::Evaluation, $hr, 'Evaluación programada.');

            $this->audit->record(AuditAction::EvaluationScheduled, $evaluation, [
                'type' => $evaluation->type->value,
                'scheduled_at' => $evaluation->scheduled_at->toIso8601String(),
                'evaluator_id' => $evaluation->evaluator_id,
            ], $hr);

            return [$evaluation, $locked, $vacancy];
        });

        $this->sendConvocation(CriterionStage::Evaluation, $evaluation, "la evaluación «{$evaluation->type->label()}»", $locked, $vacancy);

        return $evaluation;
    }

    /**
     * @param  array<string, mixed>  $data
     */
    public function scheduleInterview(Application $application, User $hr, array $data): Interview
    {
        [$interview, $locked, $vacancy] = DB::transaction(function () use ($application, $hr, $data): array {
            [$locked, $vacancy] = $this->lockForScheduling($application, CriterionStage::Interview);

            if (! self::acceptsInterview($locked->status)) {
                throw new BusinessRuleException('Solo se pueden programar entrevistas para postulaciones preseleccionadas, en evaluación o en entrevista.');
            }

            $interview = new Interview;
            $interview->forceFill($this->sessionAttributes($locked, $hr, $data))->save();

            $this->advanceStage($locked, ApplicationStatus::Interview, $hr, 'Entrevista programada.');

            $this->audit->record(AuditAction::InterviewScheduled, $interview, [
                'scheduled_at' => $interview->scheduled_at->toIso8601String(),
                'evaluator_id' => $interview->evaluator_id,
            ], $hr);

            return [$interview, $locked, $vacancy];
        });

        $this->sendConvocation(CriterionStage::Interview, $interview, 'la entrevista personal', $locked, $vacancy);

        return $interview;
    }

    /**
     * @return array{Application, Vacancy}
     */
    private function lockForScheduling(Application $application, CriterionStage $stage): array
    {
        $locked = Application::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($application->getKey());
        $vacancy = Vacancy::query()->withoutGlobalScopes()->findOrFail($locked->vacancy_id);

        if ($vacancy->isClosed()) {
            throw new BusinessRuleException('La convocatoria está cerrada; no se pueden programar evaluaciones ni entrevistas.');
        }

        if (EvaluationCriterion::definitionsFor($vacancy->id, $stage) === []) {
            throw new BusinessRuleException("La vacante no tiene criterios de la etapa «{$stage->label()}» configurados.");
        }

        return [$locked, $vacancy];
    }

    /**
     * @param  array<string, mixed>  $data
     * @return array<string, mixed>
     */
    private function sessionAttributes(Application $application, User $hr, array $data): array
    {
        $evaluatorId = (int) $data['evaluator_id'];

        $validEvaluator = User::query()
            ->whereKey($evaluatorId)
            ->where('organization_id', $application->organization_id)
            ->where('role', UserRole::Evaluator)
            ->exists();

        if (! $validEvaluator) {
            throw new BusinessRuleException('El evaluador seleccionado no pertenece a esta organización.', 'evaluator_id');
        }

        return [
            'organization_id' => $application->organization_id,
            'application_id' => $application->id,
            'evaluator_id' => $evaluatorId,
            'scheduled_by' => $hr->id,
            'modality' => $data['modality'],
            'location' => $data['location'],
            'scheduled_at' => $data['scheduled_at'],
            'duration_minutes' => $data['duration_minutes'] ?? null,
            'instructions' => $data['instructions'] ?? null,
            'status' => AssessmentStatus::Scheduled,
            'invitation_sent_at' => now(),
        ];
    }

    private function advanceStage(Application $application, ApplicationStatus $target, User $hr, string $comment): void
    {
        if ($application->status !== $target) {
            $this->stages->transition($application, $target, $hr, $comment, notify: false);
        }
    }

    private function sendConvocation(CriterionStage $kind, Evaluation|Interview $session, string $sessionLabel, Application $application, Vacancy $vacancy): void
    {
        $candidate = User::query()->findOrFail($application->candidate_id);
        $evaluator = User::query()->findOrFail($session->evaluator_id);

        $candidate->notify(new AssessmentConvocationNotification(
            kind: $kind,
            applicationId: $application->id,
            vacancyTitle: $vacancy->title,
            sessionLabel: $sessionLabel,
            scheduledAt: $session->scheduled_at,
            modalityLabel: $session->modality->label(),
            location: $session->location,
            durationMinutes: $session->duration_minutes,
            instructions: $session->instructions,
        ));

        $evaluator->notify(new AssessmentAssignedNotification(
            kind: $kind,
            sessionId: $session->id,
            candidateName: $candidate->name,
            vacancyTitle: $vacancy->title,
            scheduledAt: $session->scheduled_at,
        ));
    }
}
