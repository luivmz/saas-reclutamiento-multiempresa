<?php

namespace App\Services\Evaluation;

use App\Enums\CriterionStage;

final readonly class CriterionDefinition
{
    public function __construct(
        public string $name,
        public CriterionStage $stage,
        public float $weight,
        public float $minScore,
        public float $maxScore,
    ) {}
}
