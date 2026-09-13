<?php

namespace App\Notifications;

use App\Enums\CriterionStage;
use Carbon\CarbonInterface;

/**
 * RF-16/RF-18: informs the assigned evaluator.
 */
class AssessmentAssignedNotification extends RecruitmentNotification
{
    public function __construct(
        public readonly CriterionStage $kind,
        public readonly int $sessionId,
        public readonly string $candidateName,
        public readonly string $vacancyTitle,
        public readonly CarbonInterface $scheduledAt,
    ) {
        parent::__construct();
    }

    public function kind(): string
    {
        return 'asignacion_'.$this->kind->value;
    }

    public function title(): string
    {
        return $this->kind === CriterionStage::Evaluation ? 'Nueva evaluación asignada' : 'Nueva entrevista asignada';
    }

    public function message(): string
    {
        return sprintf(
            'Se le asignó %s de %s (%s) para el %s.',
            $this->kind === CriterionStage::Evaluation ? 'la evaluación' : 'la entrevista',
            $this->candidateName,
            $this->vacancyTitle,
            $this->scheduledAt->locale('es')->isoFormat('D [de] MMMM [de] YYYY, HH:mm'),
        );
    }

    public function url(): ?string
    {
        return $this->kind === CriterionStage::Evaluation
            ? route('evaluations.show', $this->sessionId, absolute: false)
            : route('interviews.show', $this->sessionId, absolute: false);
    }
}
