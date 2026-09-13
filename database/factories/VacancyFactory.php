<?php

namespace Database\Factories;

use App\Enums\ContractType;
use App\Enums\CriterionStage;
use App\Enums\UserRole;
use App\Enums\VacancyStatus;
use App\Models\EvaluationCriterion;
use App\Models\JobProfile;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Vacancy>
 */
class VacancyFactory extends Factory
{
    public function definition(): array
    {
        return [
            'organization_id' => Organization::factory(),
            'job_request_id' => fn (array $attributes) => JobRequest::factory()->approved()->state([
                'organization_id' => $attributes['organization_id'],
            ]),
            'created_by' => fn (array $attributes) => User::factory()->state([
                'role' => UserRole::HumanResources,
                'organization_id' => $attributes['organization_id'],
            ]),
            'code' => 'VAC-'.now()->year.'-'.fake()->unique()->numerify('####'),
            'title' => fake()->randomElement(['Docente de Matemática', 'Docente de Comunicación', 'Auxiliar de Educación Inicial']),
            'summary' => 'Convocatoria ficticia para pruebas del sistema de reclutamiento.',
            'location' => 'Huancayo, Junín',
            'contract_type' => ContractType::FullTime,
            'positions' => 1,
            'opens_at' => now()->startOfDay(),
            'closes_at' => now()->addDays(15)->startOfDay(),
            'status' => VacancyStatus::Draft,
        ];
    }

    /**
     * Adds a complete job profile and a valid criteria set (40/30/30).
     */
    public function configured(): static
    {
        return $this->afterCreating(function (Vacancy $vacancy): void {
            $profile = new JobProfile([
                'education' => 'Licenciatura en Educación',
                'experience' => 'Mínimo 2 años',
                'functions' => 'Funciones ficticias del puesto.',
                'competencies' => 'Competencias ficticias del puesto.',
            ]);
            $profile->organization_id = $vacancy->organization_id;
            $profile->vacancy_id = $vacancy->id;
            $profile->save();

            foreach ([
                ['Conocimientos pedagógicos', CriterionStage::Evaluation, 40],
                ['Clase modelo', CriterionStage::Evaluation, 30],
                ['Entrevista personal', CriterionStage::Interview, 30],
            ] as $position => [$name, $stage, $weight]) {
                EvaluationCriterion::factory()->create([
                    'organization_id' => $vacancy->organization_id,
                    'vacancy_id' => $vacancy->id,
                    'name' => $name,
                    'stage' => $stage,
                    'weight' => $weight,
                    'position' => $position,
                ]);
            }
        });
    }

    public function published(): static
    {
        return $this->state(fn () => ['status' => VacancyStatus::Published, 'published_at' => now()]);
    }
}
