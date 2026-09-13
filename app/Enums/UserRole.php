<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum UserRole: string
{
    use HasPresentation;

    case Requester = 'solicitante';
    case HumanResources = 'rrhh';
    case Approver = 'aprobador';
    case Evaluator = 'evaluador';
    case Candidate = 'postulante';

    public function label(): string
    {
        return match ($this) {
            self::Requester => 'Área solicitante',
            self::HumanResources => 'Recursos Humanos',
            self::Approver => 'Aprobador / Dirección',
            self::Evaluator => 'Evaluador',
            self::Candidate => 'Postulante',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Requester => 'info',
            self::HumanResources => 'primary',
            self::Approver => 'warning',
            self::Evaluator => 'success',
            self::Candidate => 'neutral',
        };
    }

    public function isStaff(): bool
    {
        return $this !== self::Candidate;
    }
}
