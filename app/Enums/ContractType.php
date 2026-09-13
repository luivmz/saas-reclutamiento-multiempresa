<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum ContractType: string
{
    use HasPresentation;

    case FullTime = 'tiempo_completo';
    case PartTime = 'tiempo_parcial';
    case Hourly = 'por_horas';
    case FixedTerm = 'plazo_fijo';

    public function label(): string
    {
        return match ($this) {
            self::FullTime => 'Tiempo completo',
            self::PartTime => 'Tiempo parcial',
            self::Hourly => 'Por horas',
            self::FixedTerm => 'Plazo fijo',
        };
    }

    public function tone(): string
    {
        return 'neutral';
    }
}
