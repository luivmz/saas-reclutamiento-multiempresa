<?php

namespace App\Http\Requests\JobRequests;

use App\Enums\ContractType;
use App\Models\JobRequest;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class JobRequestFormRequest extends FormRequest
{
    public function authorize(): bool
    {
        $jobRequest = $this->route('jobRequest');

        return $jobRequest instanceof JobRequest
            ? $this->user()->can('update', $jobRequest)
            : $this->user()->can('create', JobRequest::class);
    }

    /**
     * @return array<string, ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'position_title' => ['required', 'string', 'max:150'],
            'area' => ['required', 'string', 'max:120'],
            'headcount' => ['required', 'integer', 'min:1', 'max:50'],
            'contract_type' => ['required', Rule::enum(ContractType::class)],
            'justification' => ['required', 'string', 'min:20', 'max:2000'],
            'required_by' => ['nullable', 'date', 'after_or_equal:today'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'position_title' => 'puesto requerido',
            'area' => 'área solicitante',
            'headcount' => 'número de plazas',
            'contract_type' => 'tipo de contrato',
            'justification' => 'justificación',
            'required_by' => 'fecha requerida',
        ];
    }
}
