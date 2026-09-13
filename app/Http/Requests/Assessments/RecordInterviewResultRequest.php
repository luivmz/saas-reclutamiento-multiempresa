<?php

namespace App\Http\Requests\Assessments;

use App\Enums\CriterionStage;
use App\Enums\InterviewOutcome;
use App\Models\Interview;
use Illuminate\Validation\Rule;

class RecordInterviewResultRequest extends RecordScoresRequest
{
    protected function assessmentSession(): Interview
    {
        return $this->route('interview');
    }

    protected function stage(): CriterionStage
    {
        return CriterionStage::Interview;
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            ...parent::rules(),
            'outcome' => ['required', Rule::enum(InterviewOutcome::class)],
            'observations' => ['required', 'string', 'min:10', 'max:2000'],
        ];
    }

    public function outcome(): InterviewOutcome
    {
        return InterviewOutcome::from($this->validated('outcome'));
    }
}
