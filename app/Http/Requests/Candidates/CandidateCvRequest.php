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
