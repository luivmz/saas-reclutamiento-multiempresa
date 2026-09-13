<?php

namespace App\Http\Requests\Applications;

use App\Enums\ApplicationStatus;
use Illuminate\Validation\Rule;

class ChangeApplicationStageRequest extends StageCommentRequest
{
    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            ...parent::rules(),
            'status' => ['required', Rule::in(array_map(fn (ApplicationStatus $status) => $status->value, ApplicationStatus::manualTargets()))],
        ];
    }

    public function target(): ApplicationStatus
    {
        return ApplicationStatus::from($this->validated('status'));
    }
}
