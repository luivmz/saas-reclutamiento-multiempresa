<?php

namespace App\Http\Requests\Assessments;

use App\Enums\CriterionStage;
use App\Models\Evaluation;

class RecordEvaluationResultRequest extends RecordScoresRequest
{
    protected function assessmentSession(): Evaluation
    {
        return $this->route('evaluation');
    }

    protected function stage(): CriterionStage
    {
        return CriterionStage::Evaluation;
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            ...parent::rules(),
            'observations' => ['nullable', 'string', 'max:2000'],
        ];
    }
}
