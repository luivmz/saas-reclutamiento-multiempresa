<?php

namespace App\Notifications;

use App\Enums\ApplicationStatus;
use App\Models\Application;
use InvalidArgumentException;

/**
 * RF-26: final result sent to each candidate when the vacancy is closed. It only carries the vacancy title,
 * the organization and the candidate's own outcome — never scores, ranking, justifications or other candidates.
 */
class ProcessResultNotification extends RecruitmentNotification
{
    public function __construct(
        public readonly Application $application,
        public readonly ApplicationStatus $result,
        public readonly string $vacancyTitle,
        public readonly string $organizationName,
    ) {
        if ($result !== ApplicationStatus::Selected && $result !== ApplicationStatus::NotSelected) {
            throw new InvalidArgumentException('The final result must be selected or not selected.');
        }

        parent::__construct();
    }

    public function kind(): string
    {
        return $this->isSelected() ? 'resultado_seleccionado' : 'resultado_no_seleccionado';
    }

    public function title(): string
    {
        return $this->isSelected() ? 'Resultado del proceso: seleccionado(a)' : 'Resultado del proceso de selección';
    }

    public function message(): string
    {
        return $this->isSelected()
            ? "Ha sido seleccionado(a) en la convocatoria «{$this->vacancyTitle}» de {$this->organizationName}. La convocatoria ha concluido; el área de Recursos Humanos se comunicará con usted para los siguientes pasos."
            : "La convocatoria «{$this->vacancyTitle}» de {$this->organizationName} ha concluido. Agradecemos su participación; en esta oportunidad no ha sido seleccionado(a).";
    }

    public function url(): ?string
    {
        return route('candidate.applications.show', $this->application, absolute: false);
    }

    private function isSelected(): bool
    {
        return $this->result === ApplicationStatus::Selected;
    }
}
