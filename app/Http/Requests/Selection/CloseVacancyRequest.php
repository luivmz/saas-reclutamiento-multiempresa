<?php

namespace App\Http\Requests\Selection;

use Illuminate\Foundation\Http\FormRequest;

class CloseVacancyRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('close', $this->route('vacancy'));
    }

    /**
     * @return array<string, list<string>>
     */
    public function rules(): array
    {
        return [
            'closure_notes' => ['nullable', 'string', 'max:1000'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return ['closure_notes' => 'notas de cierre'];
    }
}
