<?php

namespace App\Services\Ranking;

use App\Services\Assessments\ScoreSheetValidator;
use App\Services\Evaluation\CriterionDefinition;
use App\Services\Evaluation\WeightingValidator;

/**
 * RF-21: deterministic, explainable weighted ranking (formula in docs/assumptions.md A-24).
 * Pure domain service: no persistence and no state changes. It orders candidates; it never selects one (RF-23 is human).
 */
final class RankingService
{
    private const PRECISION = 4;

    public function __construct(
        private readonly WeightingValidator $weights,
        private readonly ScoreSheetValidator $sheets,
    ) {}

    /**
     * @param  array<int, CriterionDefinition>  $criteria  keyed by criterion id
     * @param  list<CandidateScores>  $candidates
     */
    public function rank(array $criteria, array $candidates): RankingResult
    {
        $this->assertValidConfiguration($criteria);

        $totalWeight = array_sum(array_map(fn (CriterionDefinition $criterion) => $criterion->weight, $criteria));
        $scored = [];
        $incomplete = [];
        $seen = [];

        foreach ($candidates as $candidate) {
            if (isset($seen[$candidate->applicationId])) {
                throw InvalidRankingInput::because("la postulación {$candidate->applicationId} aparece más de una vez.");
            }
            $seen[$candidate->applicationId] = true;

            $this->assertValidScores($criteria, $candidate);

            $missing = $this->missingCriteria($criteria, $candidate);
            if ($missing !== []) {
                $incomplete[] = new IncompleteCandidate($candidate->applicationId, $candidate->candidateName, $missing);

                continue;
            }

            [$total, $breakdown] = $this->score($criteria, $candidate, $totalWeight);
            $scored[] = ['candidate' => $candidate, 'total' => $total, 'breakdown' => $breakdown];
        }

        usort($scored, fn (array $a, array $b) => [$b['total'], $a['candidate']->applicationId] <=> [$a['total'], $b['candidate']->applicationId]);
        usort($incomplete, fn (IncompleteCandidate $a, IncompleteCandidate $b) => $a->applicationId <=> $b->applicationId);

        return new RankingResult($this->assignPositions($scored), $incomplete);
    }

    /**
     * @param  array<int, CriterionDefinition>  $criteria
     */
    private function assertValidConfiguration(array $criteria): void
    {
        if ($criteria === []) {
            throw InvalidRankingInput::because('la vacante no tiene criterios de evaluación configurados.');
        }

        $issues = $this->weights->validate(array_values($criteria));

        if ($issues !== []) {
            throw InvalidRankingInput::because(implode(' ', $issues));
        }
    }

    /**
     * @param  array<int, CriterionDefinition>  $criteria
     */
    private function assertValidScores(array $criteria, CandidateScores $candidate): void
    {
        foreach ($candidate->scoresByCriterion as $criterionId => $scores) {
            if (! isset($criteria[$criterionId])) {
                throw InvalidRankingInput::because("la postulación {$candidate->applicationId} tiene puntajes de un criterio que no pertenece a la vacante.");
            }

            foreach ($scores as $score) {
                $errors = $this->sheets->validate([$criterionId => $criteria[$criterionId]], [$criterionId => $score]);

                if ($errors !== []) {
                    throw InvalidRankingInput::because($errors[$criterionId]);
                }
            }
        }
    }

    /**
     * @param  array<int, CriterionDefinition>  $criteria
     * @return list<string>
     */
    private function missingCriteria(array $criteria, CandidateScores $candidate): array
    {
        $missing = [];

        foreach ($criteria as $criterionId => $criterion) {
            if (($candidate->scoresByCriterion[$criterionId] ?? []) === []) {
                $missing[] = $criterion->name;
            }
        }

        return $missing;
    }

    /**
     * @param  array<int, CriterionDefinition>  $criteria
     * @return array{float, list<CriterionBreakdown>}
     */
    private function score(array $criteria, CandidateScores $candidate, float $totalWeight): array
    {
        $total = 0.0;
        $breakdown = [];

        foreach ($criteria as $criterionId => $criterion) {
            $scores = $candidate->scoresByCriterion[$criterionId];
            $average = array_sum($scores) / count($scores);
            $normalized = ($average - $criterion->minScore) / ($criterion->maxScore - $criterion->minScore);
            $contribution = $normalized * $criterion->weight / $totalWeight * 100;

            $breakdown[] = new CriterionBreakdown($criterionId, $criterion->name, $criterion->weight, $average, $normalized, $contribution);
            $total += $contribution;
        }

        return [round($total, self::PRECISION), $breakdown];
    }

    /**
     * Competition ranking (1, 2, 2, 4). Ties are flagged, not broken: the tied order follows the application id only for a stable display.
     *
     * @param  list<array{candidate: CandidateScores, total: float, breakdown: list<CriterionBreakdown>}>  $scored
     * @return list<RankedCandidate>
     */
    private function assignPositions(array $scored): array
    {
        $occurrences = array_count_values(array_map(fn (array $row) => (string) $row['total'], $scored));
        $entries = [];
        $position = 0;
        $previousTotal = null;

        foreach ($scored as $index => $row) {
            if ($row['total'] !== $previousTotal) {
                $position = $index + 1;
                $previousTotal = $row['total'];
            }

            $entries[] = new RankedCandidate(
                position: $position,
                applicationId: $row['candidate']->applicationId,
                candidateName: $row['candidate']->candidateName,
                total: $row['total'],
                tied: $occurrences[(string) $row['total']] > 1,
                breakdown: $row['breakdown'],
            );
        }

        return $entries;
    }
}
