<?php

namespace App\Services\Evaluation;

/**
 * RF-20: validates score ranges and weights of a vacancy's evaluation criteria.
 */
final class WeightingValidator
{
    private const TOLERANCE = 0.01;

    public function __construct(private readonly ?float $requiredTotal) {}

    public function requiredTotal(): ?float
    {
        return $this->requiredTotal;
    }

    /**
     * @param  iterable<CriterionDefinition>  $criteria
     * @return list<string>
     */
    public function validate(iterable $criteria): array
    {
        $issues = [];
        $seenNames = [];
        $total = 0.0;
        $count = 0;

        foreach ($criteria as $criterion) {
            $count++;
            $name = trim($criterion->name);

            if ($criterion->weight <= 0) {
                $issues[] = "El criterio «{$name}» debe tener una ponderación mayor que 0.";
            }

            if ($criterion->minScore < 0) {
                $issues[] = "El puntaje mínimo de «{$name}» no puede ser negativo.";
            } elseif ($criterion->maxScore <= $criterion->minScore) {
                $issues[] = "El rango de «{$name}» es inválido: el puntaje máximo debe ser mayor que el mínimo.";
            }

            $key = mb_strtolower($name);
            if (isset($seenNames[$key])) {
                $issues[] = "El criterio «{$name}» está duplicado.";
            }
            $seenNames[$key] = true;

            $total += $criterion->weight;
        }

        if ($count === 0) {
            return ['Debe configurar al menos un criterio de evaluación con su ponderación.'];
        }

        if ($this->requiredTotal !== null && abs($total - $this->requiredTotal) > self::TOLERANCE) {
            $issues[] = sprintf(
                'La suma de ponderaciones es %s y debe ser %s.',
                self::format($total),
                self::format($this->requiredTotal),
            );
        }

        return $issues;
    }

    private static function format(float $value): string
    {
        return rtrim(rtrim(number_format($value, 2, '.', ''), '0'), '.');
    }
}
