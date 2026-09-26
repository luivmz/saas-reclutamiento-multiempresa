<?php

namespace App\Services\Ml;

use Illuminate\Support\Carbon;

/**
 * Resultado de consultar el riesgo operacional de un proceso.
 *
 * Es lo único que sale hacia el controlador y la vista. No contiene el payload
 * enviado, ni identificadores de personas, ni nada sobre postulantes.
 *
 * `score` y `flag` son nulos salvo en `PredictiveAvailable`. Esa nulidad es
 * intencionada y debe propagarse hasta la interfaz: cuando no hay estimación,
 * lo honesto es no mostrar ninguna.
 */
final class RiskAssessment
{
    private function __construct(
        public readonly RiskAvailability $availability,
        public readonly ?float $score,
        public readonly ?bool $flag,
        public readonly ?float $threshold,
        public readonly ?string $modelVersion,
        public readonly ?string $freezeFingerprint,
        public readonly string $reason,
        public readonly Carbon $checkedAt,
    ) {}

    public static function predictive(
        float $score,
        bool $flag,
        float $threshold,
        string $modelVersion,
        string $freezeFingerprint,
    ): self {
        return new self(
            availability: RiskAvailability::PredictiveAvailable,
            score: $score,
            flag: $flag,
            threshold: $threshold,
            modelVersion: $modelVersion,
            freezeFingerprint: $freezeFingerprint,
            reason: 'ok',
            checkedAt: Carbon::now(),
        );
    }

    public static function descriptive(string $reason): self
    {
        return self::withoutPrediction(RiskAvailability::DescriptiveOnly, $reason);
    }

    public static function unavailable(string $reason): self
    {
        return self::withoutPrediction(RiskAvailability::Unavailable, $reason);
    }

    private static function withoutPrediction(RiskAvailability $availability, string $reason): self
    {
        return new self(
            availability: $availability,
            score: null,
            flag: null,
            threshold: null,
            modelVersion: null,
            freezeFingerprint: null,
            reason: $reason,
            checkedAt: Carbon::now(),
        );
    }

    public function isPredictive(): bool
    {
        return $this->availability === RiskAvailability::PredictiveAvailable;
    }

    /**
     * Porcentaje para lectura humana. Nulo si no hay estimación.
     */
    public function scoreAsPercentage(): ?float
    {
        return $this->score === null ? null : round($this->score * 100, 1);
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        return [
            'availability' => $this->availability->value,
            'reason' => $this->reason,
            'risk_score' => $this->score,
            'risk_percentage' => $this->scoreAsPercentage(),
            'risk_flag' => $this->flag,
            'threshold' => $this->threshold,
            'model_version' => $this->modelVersion,
            'freeze_fingerprint' => $this->freezeFingerprint,
            'checked_at' => $this->checkedAt->toIso8601String(),
            // Recordatorios que viajan con el dato, no solo en la documentación.
            'is_experimental' => true,
            'measures' => 'proceso',
            'decision_is_human' => true,
        ];
    }
}
