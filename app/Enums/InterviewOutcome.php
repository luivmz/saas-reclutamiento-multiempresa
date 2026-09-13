<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum InterviewOutcome: string
{
    use HasPresentation;

    case Recommended = 'recomendado';
    case RecommendedWithReservations = 'recomendado_con_reservas';
    case NotRecommended = 'no_recomendado';

    public function label(): string
    {
        return match ($this) {
            self::Recommended => 'Recomendado',
            self::RecommendedWithReservations => 'Recomendado con reservas',
            self::NotRecommended => 'No recomendado',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Recommended => 'success',
            self::RecommendedWithReservations => 'warning',
            self::NotRecommended => 'danger',
        };
    }
}
