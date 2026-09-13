<?php

namespace App\Http\Requests\Vacancies;

use App\Enums\ContractType;
use App\Enums\CriterionStage;
use App\Models\Vacancy;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class VacancyFormRequest extends FormRequest
{
    public function authorize(): bool
    {
        $vacancy = $this->route('vacancy');

        return $vacancy instanceof Vacancy
            ? $this->user()->can('update', $vacancy)
            : $this->user()->can('create', Vacancy::class);
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        $isUpdate = $this->route('vacancy') instanceof Vacancy;

        return [
            'job_request_id' => $isUpdate
                ? ['exclude']
                : ['required', 'integer', Rule::exists('job_requests', 'id')->where('organization_id', $this->user()->organization_id)],
            'title' => ['required', 'string', 'max:150'],
            'summary' => ['required', 'string', 'max:3000'],
            'location' => ['required', 'string', 'max:120'],
            'contract_type' => ['required', Rule::enum(ContractType::class)],
            'positions' => ['required', 'integer', 'min:1', 'max:50'],
            'opens_at' => ['nullable', 'date'],
            'closes_at' => ['nullable', 'date', 'after_or_equal:opens_at'],
            'profile' => ['required', 'array'],
            'profile.education' => ['required', 'string', 'max:200'],
            'profile.experience' => ['required', 'string', 'max:200'],
            'profile.functions' => ['required', 'string', 'max:3000'],
            'profile.competencies' => ['required', 'string', 'max:3000'],
            'criteria' => ['present', 'array', 'max:12'],
            'criteria.*.name' => ['required', 'string', 'max:120', 'distinct:ignore_case'],
            'criteria.*.stage' => ['required', Rule::enum(CriterionStage::class)],
            'criteria.*.weight' => ['required', 'numeric', 'gt:0', 'max:100'],
            'criteria.*.min_score' => ['required', 'numeric', 'min:0', 'max:1000'],
            'criteria.*.max_score' => ['required', 'numeric', 'gt:criteria.*.min_score', 'max:1000'],
        ];
    }

    /**
     * @return array<string, mixed>
     */
    public function vacancyAttributes(): array
    {
        return $this->safe()->only(['title', 'summary', 'location', 'contract_type', 'positions', 'opens_at', 'closes_at']);
    }

    /**
     * @return array<string, string>
     */
    public function profileAttributes(): array
    {
        return $this->validated('profile');
    }

    /**
     * @return list<array<string, mixed>>
     */
    public function criteriaAttributes(): array
    {
        return array_values($this->validated('criteria', []));
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'job_request_id' => 'requerimiento aprobado',
            'title' => 'título',
            'summary' => 'descripción',
            'location' => 'lugar de trabajo',
            'contract_type' => 'tipo de contrato',
            'positions' => 'plazas',
            'opens_at' => 'inicio de postulaciones',
            'closes_at' => 'cierre de postulaciones',
            'profile.education' => 'formación académica',
            'profile.experience' => 'experiencia',
            'profile.functions' => 'funciones',
            'profile.competencies' => 'competencias',
            'criteria.*.name' => 'nombre del criterio',
            'criteria.*.stage' => 'etapa del criterio',
            'criteria.*.weight' => 'ponderación',
            'criteria.*.min_score' => 'puntaje mínimo',
            'criteria.*.max_score' => 'puntaje máximo',
        ];
    }
}
