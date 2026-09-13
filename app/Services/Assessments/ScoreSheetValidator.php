<?php

namespace App\Services\Assessments;

use App\Services\Evaluation\CriterionDefinition;

/**
 * RF-20 applied to RF-16/RF-19 results: every criterion of the stage must have a numeric score inside its range.
 */
final class ScoreSheetValidator
{
    /**
     * @param  array<int, CriterionDefinition>  $criteria  keyed by criterion id
     * @param  array<int|string, mixed>  $scores  keyed by criterion id
     * @return array<int, string> error messages keyed by criterion id
     */
    public function validate(array $criteria, array $scores): array
    {
        $errors = [];

        foreach ($criteria as $id => $criterion) {
            $score = $scores[$id] ?? null;

            if (! is_int($score) && ! is_float($score) && ! (is_string($score) && is_numeric($score))) {
                $errors[$id] = "Debe registrar un puntaje numérico para «{$criterion->name}».";

                continue;
            }

            $value = (float) $score;

            if ($value < $criterion->minScore || $value > $criterion->maxScore) {
                $errors[$id] = sprintf(
                    'El puntaje de «%s» debe estar entre %s y %s.',
                    $criterion->name,
                    self::format($criterion->minScore),
                    self::format($criterion->maxScore),
                );
            }
        }

        foreach (array_keys($scores) as $id) {
            if (! array_key_exists($id, $criteria)) {
                $errors[(int) $id] = 'El criterio indicado no corresponde a esta etapa de evaluación.';
            }
        }

        return $errors;
    }

    private static function format(float $value): string
    {
        return rtrim(rtrim(number_format($value, 2, '.', ''), '0'), '.');
    }
}
