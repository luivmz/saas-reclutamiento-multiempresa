<?php

namespace App\Services\Ranking;

final readonly class CandidateScores
{
    /**
     * @param  array<int, list<float|int>>  $scoresByCriterion  recorded scores keyed by criterion id
     */
    public function __construct(
        public int $applicationId,
        public string $candidateName,
        public array $scoresByCriterion,
    ) {}
}
