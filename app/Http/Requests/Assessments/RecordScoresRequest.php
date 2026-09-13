<?php

namespace App\Http\Requests\Assessments;

use App\Enums\CriterionStage;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\Interview;
use App\Services\Assessments\ScoreSheetValidator;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Validator;

abstract class RecordScoresRequest extends FormRequest
{
    abstract protected function assessmentSession(): Evaluation|Interview;

    abstract protected function stage(): CriterionStage;

    public function authorize(): bool
    {
        return $this->user()->can('recordResult', $this->assessmentSession());
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'scores' => ['required', 'array'],
            'scores.*' => ['array'],
            'scores.*.score' => ['required', 'numeric'],
            'scores.*.comment' => ['nullable', 'string', 'max:500'],
        ];
    }

    /**
     * @return list<callable(Validator): void>
     */
    public function after(): array
    {
        return [
            function (Validator $validator): void {
                $scores = $this->input('scores');

                if (! is_array($scores)) {
                    return;
                }

                $definitions = EvaluationCriterion::definitionsFor($this->assessmentSession()->application->vacancy_id, $this->stage());
                $values = array_map(fn ($entry) => is_array($entry) ? ($entry['score'] ?? null) : null, $scores);

                foreach (app(ScoreSheetValidator::class)->validate($definitions, $values) as $criterionId => $message) {
                    $key = "scores.{$criterionId}.score";

                    if (! $validator->errors()->has($key)) {
                        $validator->errors()->add($key, $message);
                    }
                }
            },
        ];
    }

    /**
     * @return array<int, array{score: mixed, comment?: string|null}>
     */
    public function scores(): array
    {
        return $this->validated('scores');
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'scores' => 'puntajes',
            'scores.*.score' => 'puntaje',
            'scores.*.comment' => 'comentario',
            'observations' => 'observaciones',
            'outcome' => 'resultado de la entrevista',
        ];
    }
}
