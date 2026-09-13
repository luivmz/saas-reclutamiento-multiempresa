<?php

namespace App\Http\Requests\Applications;

use Illuminate\Foundation\Http\FormRequest;

class StageCommentRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('changeStage', $this->route('application'));
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'comment' => ['nullable', 'string', 'max:1000'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return ['comment' => 'observación', 'status' => 'etapa'];
    }
}
