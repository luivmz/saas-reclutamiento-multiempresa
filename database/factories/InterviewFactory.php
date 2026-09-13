<?php

namespace Database\Factories;

use App\Enums\AssessmentStatus;
use App\Enums\InterviewOutcome;
use App\Enums\Modality;
use App\Enums\UserRole;
use App\Models\Application;
use App\Models\Interview;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Interview>
 */
class InterviewFactory extends Factory
{
    public function definition(): array
    {
        return [
            'application_id' => Application::factory()->inInterview(),
            'organization_id' => fn (array $attributes) => Application::query()->withoutGlobalScopes()->findOrFail($attributes['application_id'])->organization_id,
            'evaluator_id' => fn (array $attributes) => User::factory()->state(['role' => UserRole::Evaluator, 'organization_id' => $attributes['organization_id']]),
            'scheduled_by' => fn (array $attributes) => User::factory()->state(['role' => UserRole::HumanResources, 'organization_id' => $attributes['organization_id']]),
            'modality' => Modality::InPerson,
            'location' => 'Oficina de RR. HH. (demo)',
            'scheduled_at' => now()->addDays(3),
            'duration_minutes' => 30,
            'instructions' => null,
            'status' => AssessmentStatus::Scheduled,
            'outcome' => null,
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

    public function completed(InterviewOutcome $outcome = InterviewOutcome::Recommended): static
    {
        return $this->state(fn () => [
            'status' => AssessmentStatus::Completed,
            'outcome' => $outcome,
            'completed_at' => now(),
            'observations' => 'Entrevista ficticia registrada.',
        ]);
    }
}
