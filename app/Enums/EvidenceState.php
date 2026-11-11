<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

/**
 * Experimental (F37 flow): state of one evidence version. It is never stored: it is derived from the
 * append-only versions and events (R-04).
 */
enum EvidenceState: string
{
    use HasPresentation;

    case Registered = 'registrada';
    case Reviewed = 'revisada';
    case Superseded = 'sustituida';
    case Withdrawn = 'retirada';

    public function label(): string
    {
        return match ($this) {
            self::Registered => 'Registrada',
            self::Reviewed => 'Revisada por RR. HH.',
            self::Superseded => 'Sustituida por una versión nueva',
            self::Withdrawn => 'Retirada',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Registered => 'info',
            self::Reviewed => 'success',
            self::Superseded => 'neutral',
            self::Withdrawn => 'warning',
        };
    }

    public function isCurrent(): bool
    {
        return $this === self::Registered || $this === self::Reviewed;
    }
}
