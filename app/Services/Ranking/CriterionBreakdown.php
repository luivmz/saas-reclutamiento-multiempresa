<?php

namespace App\Services\Ranking;

/**
 * How one criterion contributes to a candidate's total: contribution = normalized × weight ÷ Σweights × 100.
 */
final readonly class CriterionBreakdown
{
    public function __construct(
        public int $criterionId,
        public string $name,
        public float $weight,
        public float $average,
        public float $normalized,
        public float $contribution,
    ) {}
}
