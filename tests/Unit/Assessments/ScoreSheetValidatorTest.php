<?php

namespace Tests\Unit\Assessments;

use App\Enums\CriterionStage;
use App\Services\Assessments\ScoreSheetValidator;
use App\Services\Evaluation\CriterionDefinition;
use PHPUnit\Framework\TestCase;

class ScoreSheetValidatorTest extends TestCase
{
    /**
     * @return array<int, CriterionDefinition>
     */
    private function criteria(): array
    {
        return [
            10 => new CriterionDefinition('Conocimientos', CriterionStage::Evaluation, 60, 0, 20),
            11 => new CriterionDefinition('Clase modelo', CriterionStage::Evaluation, 40, 5, 10),
        ];
    }

    public function test_complete_sheet_within_ranges_has_no_errors(): void
    {
        $errors = (new ScoreSheetValidator)->validate($this->criteria(), [10 => 15.5, 11 => 7]);

        $this->assertSame([], $errors);
    }

    public function test_boundary_values_are_accepted(): void
    {
        $errors = (new ScoreSheetValidator)->validate($this->criteria(), [10 => 0, 11 => 10]);

        $this->assertSame([], $errors);
    }

    public function test_missing_scores_are_reported_per_criterion(): void
    {
        $errors = (new ScoreSheetValidator)->validate($this->criteria(), [10 => 12]);

        $this->assertSame([11], array_keys($errors));
        $this->assertStringContainsString('Clase modelo', $errors[11]);
    }

    public function test_scores_outside_the_range_are_reported(): void
    {
        $errors = (new ScoreSheetValidator)->validate($this->criteria(), [10 => 20.01, 11 => 4.99]);

        $this->assertSame([10, 11], array_keys($errors));
        $this->assertStringContainsString('entre 0 y 20', $errors[10]);
        $this->assertStringContainsString('entre 5 y 10', $errors[11]);
    }

    public function test_scores_for_unknown_criteria_are_rejected(): void
    {
        $errors = (new ScoreSheetValidator)->validate($this->criteria(), [10 => 10, 11 => 8, 99 => 5]);

        $this->assertSame([99], array_keys($errors));
    }
}
