<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum Modality: string
{
    use HasPresentation;

    case InPerson = 'presencial';
    case Virtual = 'virtual';

    public function label(): string
    {
        return match ($this) {
            self::InPerson => 'Presencial',
            self::Virtual => 'Virtual',
        };
    }

    public function tone(): string
    {
        return 'neutral';
    }
}
