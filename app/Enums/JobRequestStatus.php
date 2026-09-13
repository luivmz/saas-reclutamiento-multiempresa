<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum JobRequestStatus: string
{
    use HasPresentation;

    case Draft = 'borrador';
    case Submitted = 'enviado';
    case Observed = 'observado';
    case Validated = 'validado';
    case Approved = 'aprobado';
    case Rejected = 'rechazado';

    /**
     * @return list<self>
     */
    public function allowedTransitions(): array
    {
        return match ($this) {
            self::Draft => [self::Submitted],
            self::Submitted => [self::Observed, self::Validated],
            self::Observed => [self::Submitted],
            self::Validated => [self::Approved, self::Rejected],
            self::Approved, self::Rejected => [],
        };
    }

    public function canTransitionTo(self $target): bool
    {
        return in_array($target, $this->allowedTransitions(), true);
    }

    public function isEditable(): bool
    {
        return $this === self::Draft || $this === self::Observed;
    }

    public function label(): string
    {
        return match ($this) {
            self::Draft => 'Borrador',
            self::Submitted => 'Enviado a RR. HH.',
            self::Observed => 'Observado',
            self::Validated => 'Validado por RR. HH.',
            self::Approved => 'Aprobado',
            self::Rejected => 'Rechazado',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Draft => 'neutral',
            self::Submitted => 'info',
            self::Observed => 'warning',
            self::Validated => 'primary',
            self::Approved => 'success',
            self::Rejected => 'danger',
        };
    }
}
