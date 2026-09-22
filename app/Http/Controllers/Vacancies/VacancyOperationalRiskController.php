<?php

namespace App\Http\Controllers\Vacancies;

use App\Http\Controllers\Controller;
use App\Models\Vacancy;
use App\Services\Ml\OperationalRiskService;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Gate;

/**
 * Riesgo operacional de un proceso de vacante (Fase 16).
 *
 * Delgado a propósito: autoriza, delega y serializa. Ni HTTP hacia el servicio
 * ni cálculo de features viven aquí.
 *
 * Siempre responde 200. Que el servicio esté caído es un estado del panel, no
 * un error de esta petición: el flujo de reclutamiento no depende de él.
 */
class VacancyOperationalRiskController extends Controller
{
    public function __construct(private readonly OperationalRiskService $risk) {}

    public function __invoke(Vacancy $vacancy): JsonResponse
    {
        Gate::authorize('viewOperationalRisk', $vacancy);

        $assessment = $this->risk->assess($vacancy);

        return response()->json([
            'risk' => [
                ...$assessment->toArray(),
                'message' => $this->risk->explain($assessment),
                'label' => $assessment->availability->label(),
            ],
        ]);
    }
}
