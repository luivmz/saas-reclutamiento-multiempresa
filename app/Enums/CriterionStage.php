<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum CriterionStage: string
{
    use HasPresentation;

    case Evaluation = 'evaluacion';
    case Interview = 'entrevista';

    public function label(): string
    {
        return match ($this) {
            self::Evaluation => 'Evaluación',
            self::Interview => 'Entrevista',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Evaluation => 'info',
            self::Interview => 'primary',
        };
    }
}
