<?php

namespace App\Notifications;

use App\Enums\CriterionStage;
use Carbon\CarbonInterface;

/**
 * RF-17: convocation sent to the candidate when an evaluation or interview is scheduled.
 */
class AssessmentConvocationNotification extends RecruitmentNotification
{
    public function __construct(
        public readonly CriterionStage $kind,
        public readonly int $applicationId,
        public readonly string $vacancyTitle,
        public readonly string $sessionLabel,
        public readonly CarbonInterface $scheduledAt,
        public readonly string $modalityLabel,
        public readonly string $location,
        public readonly ?int $durationMinutes = null,
        public readonly ?string $instructions = null,
    ) {
        parent::__construct();
    }

    public function kind(): string
    {
        return 'convocatoria_'.$this->kind->value;
    }

    public function title(): string
    {
        return $this->kind === CriterionStage::Evaluation ? 'Convocatoria a evaluación' : 'Convocatoria a entrevista';
    }

    public function message(): string
    {
        $parts = [
            "Ha sido convocado(a) a {$this->sessionLabel} del proceso «{$this->vacancyTitle}» el ".$this->scheduledAt->locale('es')->isoFormat('dddd D [de] MMMM [de] YYYY, HH:mm').'.',
            "Modalidad: {$this->modalityLabel}. Lugar o enlace: {$this->location}.",
        ];

        if ($this->durationMinutes !== null) {
            $parts[] = "Duración estimada: {$this->durationMinutes} minutos.";
        }

        if ($this->instructions !== null && $this->instructions !== '') {
            $parts[] = "Indicaciones: {$this->instructions}";
        }

        return implode(' ', $parts);
    }

    public function url(): ?string
    {
        return route('candidate.applications.show', $this->applicationId, absolute: false);
    }
}
