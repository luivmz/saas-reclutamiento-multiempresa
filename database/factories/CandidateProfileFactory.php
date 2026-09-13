<?php

namespace Database\Factories;

use App\Enums\EducationLevel;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<CandidateProfile>
 */
class CandidateProfileFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory()->candidate(),
            'phone' => '9'.fake()->numerify('########'),
            'city' => fake()->randomElement(['Huancayo', 'El Tambo', 'Chilca', 'Concepción']),
            'education_level' => EducationLevel::Graduate,
            'professional_title' => 'Licenciado(a) en Educación',
            'years_of_experience' => fake()->numberBetween(1, 15),
            'summary' => 'Perfil profesional ficticio generado para pruebas.',
        ];
    }

    public function withCv(): static
    {
        return $this->afterCreating(function (CandidateProfile $profile): void {
            CandidateDocument::factory()->create(['candidate_profile_id' => $profile->id]);
        });
    }
}
