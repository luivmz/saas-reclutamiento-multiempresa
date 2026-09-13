<?php

namespace App\Http\Requests\Assessments;

use App\Enums\Modality;
use App\Enums\UserRole;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class ScheduleAssessmentRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('scheduleAssessment', $this->route('application'));
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'evaluator_id' => [
                'required',
                'integer',
                Rule::exists('users', 'id')
                    ->where('organization_id', $this->user()->organization_id)
                    ->where('role', UserRole::Evaluator->value),
            ],
            'modality' => ['required', Rule::enum(Modality::class)],
            'location' => ['required', 'string', 'max:200'],
            'scheduled_at' => ['required', 'date', 'after:now'],
            'duration_minutes' => ['nullable', 'integer', 'min:15', 'max:480'],
            'instructions' => ['nullable', 'string', 'max:2000'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'evaluator_id' => 'evaluador',
            'type' => 'tipo de evaluación',
            'modality' => 'modalidad',
            'location' => 'lugar o enlace',
            'scheduled_at' => 'fecha y hora',
            'duration_minutes' => 'duración',
            'instructions' => 'indicaciones',
        ];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'evaluator_id.exists' => 'Seleccione un evaluador de su organización.',
            'scheduled_at.after' => 'La fecha y hora deben ser posteriores al momento actual.',
        ];
    }
}
