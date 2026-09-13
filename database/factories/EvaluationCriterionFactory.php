<?php

namespace Database\Factories;

use App\Enums\CriterionStage;
use App\Models\EvaluationCriterion;
use App\Models\Vacancy;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<EvaluationCriterion>
 */
class EvaluationCriterionFactory extends Factory
{
    public function definition(): array
    {
        return [
            'organization_id' => fn (array $attributes) => Vacancy::query()->withoutGlobalScopes()->findOrFail($attributes['vacancy_id'])->organization_id,
            'vacancy_id' => Vacancy::factory(),
            'name' => 'Criterio '.fake()->unique()->numberBetween(1, 99999),
            'stage' => CriterionStage::Evaluation,
            'weight' => 50,
            'min_score' => 0,
            'max_score' => 20,
            'position' => 0,
        ];
    }
}
