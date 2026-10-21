<?php

namespace App\Http\Requests\Candidates;

use Illuminate\Foundation\Http\FormRequest;

class CandidateCvRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->isCandidate();
    }

    /**
     * @return array<string, list<string>>
     */
    public function rules(): array
    {
        // Limite por archivo: 5120 KB por defecto, ademas de exigir PDF.
        // Revision de la alerta y prueba de frontera: docs/v1.1/sonarqube/revision-v1.md.
        return [
            'cv' => ['required', 'file', 'mimes:pdf', 'mimetypes:application/pdf', 'max:'.(int) config('recruitment.cv.max_kb')],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return ['cv' => 'CV'];
    }
}
