<?php

namespace App\Services\Ranking;

final readonly class IncompleteCandidate
{
    /**
     * @param  list<string>  $missingCriteria
     */
    public function __construct(
        public int $applicationId,
        public string $candidateName,
        public array $missingCriteria,
    ) {}
}
