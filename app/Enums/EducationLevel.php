<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum EducationLevel: string
{
    use HasPresentation;

    case Secondary = 'secundaria';
    case Technical = 'tecnico';
    case Bachelor = 'bachiller';
    case Graduate = 'titulado';
    case Master = 'maestria';
    case Doctorate = 'doctorado';

    public function label(): string
    {
        return match ($this) {
            self::Secondary => 'Secundaria completa',
            self::Technical => 'Técnico',
            self::Bachelor => 'Bachiller universitario',
            self::Graduate => 'Título profesional',
            self::Master => 'Maestría',
            self::Doctorate => 'Doctorado',
        };
    }

    public function tone(): string
    {
        return 'neutral';
    }
}
