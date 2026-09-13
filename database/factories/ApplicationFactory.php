<?php

namespace Database\Factories;

use App\Enums\ApplicationStatus;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Application>
 */
class ApplicationFactory extends Factory
{
    public function definition(): array
    {
        return [
            'vacancy_id' => Vacancy::factory()->configured()->published(),
            'candidate_id' => User::factory()->candidate()->has(CandidateProfile::factory()->withCv(), 'candidateProfile'),
            'organization_id' => fn (array $attributes) => Vacancy::query()->withoutGlobalScopes()->findOrFail($attributes['vacancy_id'])->organization_id,
            'candidate_document_id' => fn (array $attributes) => CandidateDocument::query()
                ->whereHas('profile', fn ($query) => $query->where('user_id', $attributes['candidate_id']))
                ->latest('id')
                ->value('id'),
            'status' => ApplicationStatus::Submitted,
            'applied_at' => now(),
            'stage_changed_at' => now(),
        ];
    }

    public function configure(): static
    {
        return $this->afterCreating(function (Application $application): void {
            $history = new ApplicationStageHistory;
            $history->forceFill([
                'organization_id' => $application->organization_id,
                'application_id' => $application->id,
                'from_status' => null,
                'to_status' => ApplicationStatus::Submitted,
                'changed_by' => $application->candidate_id,
            ])->save();
        });
    }

    public function forCandidate(User $candidate): static
    {
        return $this->state(fn () => ['candidate_id' => $candidate->id]);
    }

    public function shortlisted(): static
    {
        return $this->state(fn () => ['status' => ApplicationStatus::Shortlisted]);
    }

    public function inEvaluation(): static
    {
        return $this->state(fn () => ['status' => ApplicationStatus::Evaluation]);
    }

    public function inInterview(): static
    {
        return $this->state(fn () => ['status' => ApplicationStatus::Interview]);
    }

    public function finalist(): static
    {
        return $this->state(fn () => ['status' => ApplicationStatus::Finalist]);
    }

    public function discarded(): static
    {
        return $this->state(fn () => ['status' => ApplicationStatus::Discarded]);
    }
}
