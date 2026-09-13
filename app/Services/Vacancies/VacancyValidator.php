<?php

namespace App\Services\Vacancies;

use App\Enums\JobRequestStatus;
use App\Models\EvaluationCriterion;
use App\Models\Vacancy;
use App\Services\Evaluation\WeightingValidator;
use Carbon\CarbonInterface;

/**
 * RF-06: checks whether a configured vacancy is complete and consistent enough to be published.
 */
class VacancyValidator
{
    public function __construct(private readonly WeightingValidator $weights) {}

    /**
     * @return list<string>
     */
    public function issues(Vacancy $vacancy, ?CarbonInterface $today = null): array
    {
        $today = ($today ?? now())->startOfDay();
        $vacancy->loadMissing(['profile', 'criteria', 'jobRequest']);
        $issues = [];

        if ($vacancy->jobRequest->status !== JobRequestStatus::Approved) {
            $issues[] = 'El requerimiento de personal asociado no está aprobado.';
        }

        if ($vacancy->profile === null) {
            $issues[] = 'Debe registrar el perfil del puesto.';
        }

        if ($vacancy->positions > $vacancy->jobRequest->headcount) {
            $issues[] = "El número de plazas ({$vacancy->positions}) excede lo aprobado en el requerimiento ({$vacancy->jobRequest->headcount}).";
        }

        if ($vacancy->closes_at === null) {
            $issues[] = 'Debe definir la fecha de cierre de postulaciones.';
        } elseif ($vacancy->closes_at->lt($today)) {
            $issues[] = 'La fecha de cierre de postulaciones ya pasó.';
        }

        $definitions = $vacancy->criteria->map(fn (EvaluationCriterion $criterion) => $criterion->toDefinition())->all();

        return [...$issues, ...$this->weights->validate($definitions)];
    }
}
