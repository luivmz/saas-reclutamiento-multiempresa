<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum EvaluationType: string
{
    use HasPresentation;

    case Knowledge = 'conocimientos';
    case ModelClass = 'clase_modelo';
    case Practical = 'practica';
    case Other = 'otra';

    public function label(): string
    {
        return match ($this) {
            self::Knowledge => 'Prueba de conocimientos',
            self::ModelClass => 'Clase modelo',
            self::Practical => 'Prueba práctica',
            self::Other => 'Otra evaluación',
        };
    }

    public function tone(): string
    {
        return 'info';
    }
}
