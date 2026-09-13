<?php

namespace App\Notifications;

use App\Models\Application;

/**
 * RF-11.
 */
class ApplicationReceivedNotification extends RecruitmentNotification
{
    public function __construct(
        public readonly Application $application,
        public readonly string $vacancyTitle,
        public readonly string $organizationName,
    ) {
        parent::__construct();
    }

    public function kind(): string
    {
        return 'postulacion_registrada';
    }

    public function title(): string
    {
        return 'Postulación registrada';
    }

    public function message(): string
    {
        return "Registramos su postulación a «{$this->vacancyTitle}» de {$this->organizationName}. Código de seguimiento: {$this->application->trackingCode()}.";
    }

    public function url(): ?string
    {
        return route('candidate.applications.show', $this->application, absolute: false);
    }
}
