<?php

namespace Tests\Unit\Evaluation;

use App\Enums\CriterionStage;
use App\Services\Evaluation\CriterionDefinition;
use App\Services\Evaluation\WeightingValidator;
use PHPUnit\Framework\TestCase;

class WeightingValidatorTest extends TestCase
{
    private function criterion(string $name, float $weight, float $min = 0, float $max = 20, CriterionStage $stage = CriterionStage::Evaluation): CriterionDefinition
    {
        return new CriterionDefinition($name, $stage, $weight, $min, $max);
    }

    public function test_valid_configuration_has_no_issues(): void
    {
        $validator = new WeightingValidator(requiredTotal: 100);

        $issues = $validator->validate([
            $this->criterion('Conocimientos', 40),
            $this->criterion('Clase modelo', 30),
            $this->criterion('Entrevista', 30, stage: CriterionStage::Interview),
        ]);

        $this->assertSame([], $issues);
    }

    public function test_empty_configuration_is_invalid(): void
    {
        $this->assertNotEmpty((new WeightingValidator(100))->validate([]));
    }

    public function test_weight_must_be_greater_than_zero(): void
    {
        $issues = (new WeightingValidator(null))->validate([
            $this->criterion('A', 0),
            $this->criterion('B', -5),
        ]);

        $this->assertCount(2, $issues);
    }

    public function test_score_range_must_be_consistent(): void
    {
        $issues = (new WeightingValidator(null))->validate([
            $this->criterion('Rango invertido', 50, min: 20, max: 10),
            $this->criterion('Rango vacío', 25, min: 10, max: 10),
            $this->criterion('Mínimo negativo', 25, min: -1, max: 10),
        ]);

        $this->assertCount(3, $issues);
    }

    public function test_criterion_names_must_be_unique_ignoring_case_and_spaces(): void
    {
        $issues = (new WeightingValidator(null))->validate([
            $this->criterion('Entrevista', 50),
            $this->criterion('  entrevista ', 50),
        ]);

        $this->assertCount(1, $issues);
    }

    public function test_weights_must_add_up_to_required_total_when_configured(): void
    {
        $issues = (new WeightingValidator(100))->validate([
            $this->criterion('A', 50),
            $this->criterion('B', 40),
        ]);

        $this->assertCount(1, $issues);
        $this->assertStringContainsString('90', $issues[0]);
    }

    public function test_total_comparison_tolerates_decimal_rounding(): void
    {
        $issues = (new WeightingValidator(100))->validate([
            $this->criterion('A', 33.33),
            $this->criterion('B', 33.33),
            $this->criterion('C', 33.34),
        ]);

        $this->assertSame([], $issues);
    }

    public function test_total_rule_can_be_disabled_by_configuration(): void
    {
        $issues = (new WeightingValidator(null))->validate([
            $this->criterion('A', 50),
            $this->criterion('B', 40),
        ]);

        $this->assertSame([], $issues);
    }
}
