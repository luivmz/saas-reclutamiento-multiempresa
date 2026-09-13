<?php

namespace App\Http\Requests\Applications;

class DiscardApplicationRequest extends StageCommentRequest
{
    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'comment' => ['required', 'string', 'min:5', 'max:1000'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return ['comment.required' => 'Debe indicar el motivo del descarte.'];
    }
}
