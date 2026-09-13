<?php

namespace App\Services\Ranking;

/**
 * Decision-support output only: it carries no selection and never changes application states.
 */
final readonly class RankingResult
{
    /**
     * @param  list<RankedCandidate>  $entries
     * @param  list<IncompleteCandidate>  $incomplete
     */
    public function __construct(
        public array $entries,
        public array $incomplete,
    ) {}

    public function entryFor(int $applicationId): ?RankedCandidate
    {
        foreach ($this->entries as $entry) {
            if ($entry->applicationId === $applicationId) {
                return $entry;
            }
        }

        return null;
    }
}
