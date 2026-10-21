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
        return [
            // A-12: la configuración puede reducir, pero no ampliar, el máximo de 5 MB.
            'cv' => ['required', 'file', 'mimes:pdf', 'mimetypes:application/pdf', 'max:5120', 'max:'.(int) config('recruitment.cv.max_kb')],
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
