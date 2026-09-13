<?php

namespace App\Notifications;

use App\Models\JobRequest;

/**
 * RF-04.
 */
class JobRequestRejectedNotification extends RecruitmentNotification
{
    public function __construct(public readonly JobRequest $jobRequest)
    {
        parent::__construct();
    }

    public function kind(): string
    {
        return 'requerimiento_rechazado';
    }

    public function title(): string
    {
        return "Requerimiento {$this->jobRequest->code} rechazado";
    }

    public function message(): string
    {
        return "El requerimiento «{$this->jobRequest->position_title}» fue rechazado. Motivo: {$this->jobRequest->decision_comment}";
    }

    public function url(): ?string
    {
        return route('job-requests.show', $this->jobRequest, absolute: false);
    }
}
