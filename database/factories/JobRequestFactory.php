<?php

namespace Database\Factories;

use App\Enums\ContractType;
use App\Enums\JobRequestStatus;
use App\Enums\UserRole;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<JobRequest>
 */
class JobRequestFactory extends Factory
{
    public function definition(): array
    {
        return [
            'organization_id' => Organization::factory(),
            'requested_by' => fn (array $attributes) => User::factory()->state([
                'role' => UserRole::Requester,
                'organization_id' => $attributes['organization_id'],
            ]),
            'code' => 'REQ-'.now()->year.'-'.fake()->unique()->numerify('####'),
            'position_title' => fake()->randomElement(['Docente de Matemática', 'Docente de Comunicación', 'Auxiliar de Educación', 'Psicólogo(a) Escolar']),
            'area' => fake()->randomElement(['Coordinación Académica', 'Dirección de Nivel Inicial', 'Departamento de Tutoría']),
            'headcount' => 1,
            'contract_type' => ContractType::FullTime,
            'justification' => 'Necesidad ficticia generada para pruebas del sistema de reclutamiento.',
            'required_by' => now()->addMonth(),
            'status' => JobRequestStatus::Draft,
        ];
    }

    public function requestedBy(User $requester): static
    {
        return $this->state(fn () => [
            'requested_by' => $requester->id,
            'organization_id' => $requester->organization_id,
        ]);
    }

    public function submitted(): static
    {
        return $this->state(fn () => ['status' => JobRequestStatus::Submitted, 'submitted_at' => now()]);
    }

    public function observed(): static
    {
        return $this->state(fn () => [
            'status' => JobRequestStatus::Observed,
            'submitted_at' => now(),
            'observation' => 'Observación ficticia de RR. HH.',
        ]);
    }

    public function validated(): static
    {
        return $this->state(fn () => [
            'status' => JobRequestStatus::Validated,
            'submitted_at' => now(),
            'validated_at' => now(),
        ]);
    }

    public function approved(): static
    {
        return $this->state(fn () => [
            'status' => JobRequestStatus::Approved,
            'submitted_at' => now(),
            'validated_at' => now(),
            'decided_at' => now(),
        ]);
    }
}
