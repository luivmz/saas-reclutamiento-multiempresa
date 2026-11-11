<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

/**
 * Experimental (F37 flow, exp/evidencias-ml02): the type a person declares for a fictitious evidence record.
 * The system never infers it from the content.
 */
enum EvidenceType: string
{
    use HasPresentation;

    case Cv = 'cv';
    case Certificate = 'certificado';
    case ReviewedTranscript = 'transcripcion_revisada';
    case Observation = 'observacion';

    public function label(): string
    {
        return match ($this) {
            self::Cv => 'CV presentado',
            self::Certificate => 'Certificado',
            self::ReviewedTranscript => 'Transcripción revisada',
            self::Observation => 'Observación del evaluador',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Observation => 'success',
            self::ReviewedTranscript => 'info',
            default => 'neutral',
        };
    }

    /**
     * R-09: each type has exactly one admissible declared source.
     */
    public function source(): EvidenceSource
    {
        return match ($this) {
            self::Cv, self::Certificate => EvidenceSource::SubmittedDocument,
            self::ReviewedTranscript, self::Observation => EvidenceSource::AssignedSession,
        };
    }

    /**
     * Types each role may register (F37 §4). Anything else is denied.
     *
     * @return list<self>
     */
    public static function registrableBy(UserRole $role): array
    {
        return match ($role) {
            UserRole::HumanResources => [self::Cv, self::Certificate, self::ReviewedTranscript],
            UserRole::Evaluator => [self::Observation],
            default => [],
        };
    }
}
