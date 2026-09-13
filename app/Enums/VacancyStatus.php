<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum VacancyStatus: string
{
    use HasPresentation;

    case Draft = 'borrador';
    case Published = 'publicada';
    case Closed = 'cerrada';

    /**
     * @return list<self>
     */
    public function allowedTransitions(): array
    {
        return match ($this) {
            self::Draft => [self::Published],
            self::Published => [self::Closed],
            self::Closed => [],
        };
    }

    public function canTransitionTo(self $target): bool
    {
        return in_array($target, $this->allowedTransitions(), true);
    }

    public function label(): string
    {
        return match ($this) {
            self::Draft => 'Borrador',
            self::Published => 'Publicada',
            self::Closed => 'Cerrada',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Draft => 'neutral',
            self::Published => 'success',
            self::Closed => 'warning',
        };
    }
}
