<?php

namespace App\Http\Requests\Assessments;

use App\Enums\EvaluationType;
use Illuminate\Validation\Rule;

class ScheduleEvaluationRequest extends ScheduleAssessmentRequest
{
    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            ...parent::rules(),
            'type' => ['required', Rule::enum(EvaluationType::class)],
        ];
    }
}
