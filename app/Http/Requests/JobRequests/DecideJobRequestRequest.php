<?php

namespace App\Http\Requests\JobRequests;

use App\Enums\JobRequestDecision;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class DecideJobRequestRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('decide', $this->route('jobRequest'));
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'decision' => ['required', Rule::enum(JobRequestDecision::class)],
            'comment' => ['nullable', 'required_if:decision,'.JobRequestDecision::Reject->value, 'string', 'max:1000'],
        ];
    }

    public function decision(): JobRequestDecision
    {
        return JobRequestDecision::from($this->validated('decision'));
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return ['decision' => 'decisión', 'comment' => 'motivo'];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return ['comment.required_if' => 'Debe indicar el motivo del rechazo.'];
    }
}
