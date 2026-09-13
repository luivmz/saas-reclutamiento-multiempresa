<?php

namespace Tests\Unit\Ranking;

use App\Enums\CriterionStage;
use App\Services\Assessments\ScoreSheetValidator;
use App\Services\Evaluation\CriterionDefinition;
use App\Services\Evaluation\WeightingValidator;
use App\Services\Ranking\CandidateScores;
use App\Services\Ranking\InvalidRankingInput;
use App\Services\Ranking\RankedCandidate;
use App\Services\Ranking\RankingService;
use PHPUnit\Framework\TestCase;

class RankingServiceTest extends TestCase
{
    private function service(?float $requiredTotal = 100): RankingService
    {
        return new RankingService(new WeightingValidator($requiredTotal), new ScoreSheetValidator);
    }

    /**
     * Criterion 1: 0–20, criterion 2: 0–10.
     *
     * @return array<int, CriterionDefinition>
     */
    private function criteria(float $weightA = 60, float $weightB = 40): array
    {
        return [
            1 => new CriterionDefinition('Conocimientos', CriterionStage::Evaluation, $weightA, 0, 20),
            2 => new CriterionDefinition('Entrevista', CriterionStage::Interview, $weightB, 0, 10),
        ];
    }

    /**
     * @param  float|list<float>  $a
     * @param  float|list<float>  $b
     */
    private function candidate(int $applicationId, float|array $a, float|array $b): CandidateScores
    {
        return new CandidateScores($applicationId, "Candidato {$applicationId}", [1 => (array) $a, 2 => (array) $b]);
    }

    /**
     * @param  list<RankedCandidate>  $entries
     * @return list<int>
     */
    private function ids(array $entries): array
    {
        return array_map(fn (RankedCandidate $entry) => $entry->applicationId, $entries);
    }

    public function test_rf21_single_candidate_total_is_the_weighted_normalized_sum(): void
    {
        $result = $this->service()->rank($this->criteria(), [$this->candidate(10, 15, 5)]);

        $this->assertCount(1, $result->entries);
        $entry = $result->entries[0];
        $this->assertSame(1, $entry->position);
        $this->assertSame(10, $entry->applicationId);
        $this->assertFalse($entry->tied);
        $this->assertEqualsWithDelta(65.0, $entry->total, 0.0001);

        $this->assertSame(1, $entry->breakdown[0]->criterionId);
        $this->assertEqualsWithDelta(15.0, $entry->breakdown[0]->average, 0.0001);
        $this->assertEqualsWithDelta(0.75, $entry->breakdown[0]->normalized, 0.0001);
        $this->assertEqualsWithDelta(45.0, $entry->breakdown[0]->contribution, 0.0001);
        $this->assertEqualsWithDelta(20.0, $entry->breakdown[1]->contribution, 0.0001);
    }

    public function test_rf21_candidates_are_ordered_by_total_descending(): void
    {
        $result = $this->service()->rank($this->criteria(), [
            $this->candidate(1, 10, 5),
            $this->candidate(2, 20, 10),
            $this->candidate(3, 15, 2),
        ]);

        $this->assertSame([2, 3, 1], $this->ids($result->entries));
        $this->assertSame([1, 2, 3], array_map(fn (RankedCandidate $entry) => $entry->position, $result->entries));
    }

    public function test_rf21_weights_change_the_order(): void
    {
        $candidates = [$this->candidate(1, 20, 0), $this->candidate(2, 0, 10)];

        $this->assertSame([1, 2], $this->ids($this->service()->rank($this->criteria(60, 40), $candidates)->entries));
        $this->assertSame([2, 1], $this->ids($this->service()->rank($this->criteria(30, 70), $candidates)->entries));
    }

    public function test_rf21_ties_share_the_position_and_are_flagged_without_being_broken(): void
    {
        $result = $this->service()->rank($this->criteria(), [
            $this->candidate(5, 10, 5),
            $this->candidate(3, 10, 5),
            $this->candidate(9, 20, 10),
        ]);

        $this->assertSame([9, 3, 5], $this->ids($result->entries));
        $this->assertSame([1, 2, 2], array_map(fn (RankedCandidate $entry) => $entry->position, $result->entries));
        $this->assertSame([false, true, true], array_map(fn (RankedCandidate $entry) => $entry->tied, $result->entries));
    }

    public function test_rf21_minimum_and_maximum_scores_produce_0_and_100(): void
    {
        $result = $this->service()->rank($this->criteria(), [
            $this->candidate(1, 0, 0),
            $this->candidate(2, 20, 10),
        ]);

        $this->assertEqualsWithDelta(100.0, $result->entries[0]->total, 0.0001);
        $this->assertEqualsWithDelta(0.0, $result->entries[1]->total, 0.0001);
    }

    public function test_rf21_multiple_scores_for_a_criterion_are_averaged(): void
    {
        $result = $this->service()->rank($this->criteria(), [$this->candidate(1, [10, 20], [4, 6])]);

        $this->assertEqualsWithDelta(15.0, $result->entries[0]->breakdown[0]->average, 0.0001);
        $this->assertEqualsWithDelta(65.0, $result->entries[0]->total, 0.0001);
    }

    public function test_rf21_candidates_with_missing_criteria_are_reported_as_incomplete_and_not_ranked(): void
    {
        $result = $this->service()->rank($this->criteria(), [
            new CandidateScores(7, 'Incompleto', [1 => [18.0]]),
            $this->candidate(1, 10, 5),
        ]);

        $this->assertSame([1], $this->ids($result->entries));
        $this->assertCount(1, $result->incomplete);
        $this->assertSame(7, $result->incomplete[0]->applicationId);
        $this->assertSame(['Entrevista'], $result->incomplete[0]->missingCriteria);
    }

    public function test_rf21_result_is_deterministic_regardless_of_input_order(): void
    {
        $candidates = [
            $this->candidate(1, 12, 7),
            $this->candidate(2, 12, 7),
            $this->candidate(3, 19, 3),
            $this->candidate(4, 6, 9),
        ];

        $snapshot = fn (array $entries) => array_map(fn (RankedCandidate $entry) => [$entry->applicationId, $entry->position, round($entry->total, 4), $entry->tied], $entries);

        $this->assertSame(
            $snapshot($this->service()->rank($this->criteria(), $candidates)->entries),
            $snapshot($this->service()->rank($this->criteria(), array_reverse($candidates))->entries),
        );
    }

    public function test_rf20_weights_need_not_add_up_to_100_when_the_rule_is_disabled(): void
    {
        $result = $this->service(requiredTotal: null)->rank($this->criteria(3, 1), [$this->candidate(1, 20, 0)]);

        $this->assertEqualsWithDelta(75.0, $result->entries[0]->total, 0.0001);
    }

    public function test_rf20_invalid_weight_configuration_is_rejected(): void
    {
        $this->expectException(InvalidRankingInput::class);

        $this->service(requiredTotal: 100)->rank($this->criteria(50, 40), [$this->candidate(1, 10, 5)]);
    }

    public function test_rf20_score_outside_the_configured_range_is_rejected(): void
    {
        $this->expectException(InvalidRankingInput::class);

        $this->service()->rank($this->criteria(), [$this->candidate(1, 25, 5)]);
    }

    public function test_rf20_scores_for_criteria_outside_the_vacancy_are_rejected(): void
    {
        $this->expectException(InvalidRankingInput::class);

        $this->service()->rank($this->criteria(), [new CandidateScores(1, 'Ajeno', [1 => [10.0], 2 => [5.0], 99 => [3.0]])]);
    }

    public function test_rf20_empty_criteria_are_rejected(): void
    {
        $this->expectException(InvalidRankingInput::class);

        $this->service()->rank([], [$this->candidate(1, 10, 5)]);
    }

    public function test_rf21_duplicate_applications_are_rejected(): void
    {
        $this->expectException(InvalidRankingInput::class);

        $this->service()->rank($this->criteria(), [$this->candidate(1, 10, 5), $this->candidate(1, 12, 6)]);
    }
}
