<?php

namespace App\Http\Requests\Candidates;

use App\Enums\EducationLevel;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class CandidateProfileRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->isCandidate();
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'phone' => ['required', 'string', 'regex:/^[0-9+\s-]{6,20}$/'],
            'city' => ['required', 'string', 'max:80'],
            'education_level' => ['required', Rule::enum(EducationLevel::class)],
            'professional_title' => ['required', 'string', 'max:150'],
            'years_of_experience' => ['required', 'integer', 'min:0', 'max:60'],
            'summary' => ['nullable', 'string', 'max:2000'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'phone' => 'teléfono',
            'city' => 'ciudad',
            'education_level' => 'nivel educativo',
            'professional_title' => 'título u ocupación',
            'years_of_experience' => 'años de experiencia',
            'summary' => 'resumen profesional',
        ];
    }
}
