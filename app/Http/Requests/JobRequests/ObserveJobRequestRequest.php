<?php

namespace App\Http\Requests\JobRequests;

use Illuminate\Foundation\Http\FormRequest;

class ObserveJobRequestRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('review', $this->route('jobRequest'));
    }

    /**
     * @return array<string, list<string>>
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
    public function attributes(): array
    {
        return ['comment' => 'observación'];
    }
}
