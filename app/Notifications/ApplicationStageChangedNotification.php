<?php

namespace App\Notifications;

use App\Enums\ApplicationStatus;
use App\Models\Application;

/**
 * RF-15. Internal HR comments are intentionally not included (docs/assumptions.md A-14).
 */
class ApplicationStageChangedNotification extends RecruitmentNotification
{
    public function __construct(
        public readonly Application $application,
        public readonly string $vacancyTitle,
        public readonly ApplicationStatus $status,
    ) {
        parent::__construct();
    }

    public function kind(): string
    {
        return 'postulacion_etapa';
    }

    public function title(): string
    {
        return 'Actualización de su postulación';
    }

    public function message(): string
    {
        if ($this->status === ApplicationStatus::Discarded) {
            return "Le informamos que su postulación a «{$this->vacancyTitle}» no continuará en el proceso de selección. Agradecemos su interés.";
        }

        return "Su postulación a «{$this->vacancyTitle}» avanzó a la etapa: {$this->status->label()}.";
    }

    public function url(): ?string
    {
        return route('candidate.applications.show', $this->application, absolute: false);
    }
}
