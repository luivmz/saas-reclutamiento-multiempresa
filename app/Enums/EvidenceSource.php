<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

/**
 * Experimental (F37 flow): where a person says the evidence comes from. Only internal sources of the process;
 * never a URL or an external source (R-09).
 */
enum EvidenceSource: string
{
    use HasPresentation;

    case SubmittedDocument = 'documento_presentado';
    case AssignedSession = 'sesion_asignada';

    public function label(): string
    {
        return match ($this) {
            self::SubmittedDocument => 'Documento presentado',
            self::AssignedSession => 'Sesión asignada',
        };
    }

    public function tone(): string
    {
        return 'neutral';
    }
}
