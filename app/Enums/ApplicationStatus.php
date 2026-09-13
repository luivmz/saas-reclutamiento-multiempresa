<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum ApplicationStatus: string
{
    use HasPresentation;

    case Submitted = 'postulado';
    case Shortlisted = 'preseleccionado';
    case Evaluation = 'en_evaluacion';
    case Interview = 'en_entrevista';
    case Finalist = 'finalista';
    case Selected = 'seleccionado';
    case NotSelected = 'no_seleccionado';
    case Discarded = 'descartado';

    /**
     * @return list<self>
     */
    public function allowedTransitions(): array
    {
        return match ($this) {
            self::Submitted => [self::Shortlisted, self::Discarded],
            self::Shortlisted => [self::Evaluation, self::Interview, self::Discarded],
            self::Evaluation => [self::Interview, self::Finalist, self::Discarded],
            self::Interview => [self::Finalist, self::Discarded],
            self::Finalist => [self::Selected, self::NotSelected, self::Discarded],
            self::Selected, self::NotSelected, self::Discarded => [],
        };
    }

    public function canTransitionTo(self $target): bool
    {
        return in_array($target, $this->allowedTransitions(), true);
    }

    /**
     * Stages HR may assign directly (RF-13/RF-14). Selection outcomes only come from RF-24 and RF-25.
     *
     * @return list<self>
     */
    public static function manualTargets(): array
    {
        return [self::Shortlisted, self::Evaluation, self::Interview, self::Finalist, self::Discarded];
    }

    public function isManualTarget(): bool
    {
        return in_array($this, self::manualTargets(), true);
    }

    public function isTerminal(): bool
    {
        return $this->allowedTransitions() === [];
    }

    public function label(): string
    {
        return match ($this) {
            self::Submitted => 'Postulación registrada',
            self::Shortlisted => 'Preseleccionado',
            self::Evaluation => 'En evaluación',
            self::Interview => 'En entrevista',
            self::Finalist => 'Finalista',
            self::Selected => 'Seleccionado',
            self::NotSelected => 'No seleccionado',
            self::Discarded => 'Descartado',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Submitted => 'info',
            self::Shortlisted, self::Finalist => 'primary',
            self::Evaluation, self::Interview => 'warning',
            self::Selected => 'success',
            self::NotSelected => 'neutral',
            self::Discarded => 'danger',
        };
    }
}
