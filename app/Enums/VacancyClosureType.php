<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum VacancyClosureType: string
{
    use HasPresentation;

    case WithSelection = 'con_seleccion';
    case Deserted = 'desierta';

    public function label(): string
    {
        return match ($this) {
            self::WithSelection => 'Cerrada con selección',
            self::Deserted => 'Cerrada sin selección (desierta)',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::WithSelection => 'success',
            self::Deserted => 'warning',
        };
    }
}
