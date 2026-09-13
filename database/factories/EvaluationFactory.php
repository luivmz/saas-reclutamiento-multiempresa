<?php

namespace Database\Factories;

use App\Enums\AssessmentStatus;
use App\Enums\EvaluationType;
use App\Enums\Modality;
use App\Enums\UserRole;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Evaluation>
 */
class EvaluationFactory extends Factory
{
    public function definition(): array
    {
        return [
            'application_id' => Application::factory()->inEvaluation(),
            'organization_id' => fn (array $attributes) => Application::query()->withoutGlobalScopes()->findOrFail($attributes['application_id'])->organization_id,
            'evaluator_id' => fn (array $attributes) => User::factory()->state(['role' => UserRole::Evaluator, 'organization_id' => $attributes['organization_id']]),
            'scheduled_by' => fn (array $attributes) => User::factory()->state(['role' => UserRole::HumanResources, 'organization_id' => $attributes['organization_id']]),
            'type' => EvaluationType::Knowledge,
            'modality' => Modality::InPerson,
            'location' => 'Aula de demostración',
            'scheduled_at' => now()->addDays(2),
            'duration_minutes' => 60,
            'instructions' => null,
            'status' => AssessmentStatus::Scheduled,
            'invitation_sent_at' => now(),
        ];
    }

    public function forApplication(Application $application): static
    {
        return $this->state(fn () => [
            'application_id' => $application->id,
            'organization_id' => $application->organization_id,
        ]);
    }

    public function assignedTo(User $evaluator): static
    {
        return $this->state(fn () => ['evaluator_id' => $evaluator->id]);
    }

    public function completed(): static
    {
        return $this->state(fn () => ['status' => AssessmentStatus::Completed, 'completed_at' => now()]);
    }
}
