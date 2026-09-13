<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum AssessmentStatus: string
{
    use HasPresentation;

    case Scheduled = 'programada';
    case Completed = 'realizada';

    public function label(): string
    {
        return match ($this) {
            self::Scheduled => 'Programada',
            self::Completed => 'Realizada',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Scheduled => 'warning',
            self::Completed => 'success',
        };
    }
}
