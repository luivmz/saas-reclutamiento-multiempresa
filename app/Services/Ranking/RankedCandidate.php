<?php

namespace App\Services\Ranking;

final readonly class RankedCandidate
{
    /**
     * @param  list<CriterionBreakdown>  $breakdown
     */
    public function __construct(
        public int $position,
        public int $applicationId,
        public string $candidateName,
        public float $total,
        public bool $tied,
        public array $breakdown,
    ) {}
}
