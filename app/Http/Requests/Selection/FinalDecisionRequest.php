<?php

namespace App\Http\Requests\Selection;

use App\Models\Vacancy;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class FinalDecisionRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('decide', $this->vacancy());
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        $vacancy = $this->vacancy();

        return [
            'application_id' => [
                'required',
                'integer',
                Rule::exists('applications', 'id')
                    ->where('vacancy_id', $vacancy->id)
                    ->where('organization_id', $vacancy->organization_id),
            ],
            'justification' => ['required', 'string', 'min:20', 'max:2000'],
            'human_confirmation' => ['accepted'],
        ];
    }

    private function vacancy(): Vacancy
    {
        return $this->route('vacancy');
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'application_id' => 'candidato elegido',
            'justification' => 'justificación de la decisión',
            'human_confirmation' => 'confirmación de decisión humana',
        ];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'application_id.exists' => 'El candidato elegido no pertenece a esta vacante.',
            'human_confirmation.accepted' => 'Debe confirmar que la decisión es tomada por usted como responsable autorizado.',
        ];
    }
}
