<?php

namespace App\Http\Controllers;

use App\Http\Support\RequisitosPostulacion;
use App\Models\Scopes\OrganizationScope;
use App\Models\Vacancy;
use Inertia\Inertia;
use Inertia\Response;

/**
 * Portada pública. El contador cuenta las convocatorias que hoy aceptan postulaciones, con la misma regla que
 * permite postular (Vacancy::acceptsApplications): publicadas y dentro de su plazo. No incluye borradores,
 * vacantes cerradas ni convocatorias vencidas o que aún no abren.
 */
class HomeController extends Controller
{
    public function __invoke(): Response
    {
        return Inertia::render('welcome', [
            'convocatoriasAbiertas' => Vacancy::query()
                ->withoutGlobalScope(OrganizationScope::class)
                ->acceptingApplications()
                ->count(),
            'requisitos' => RequisitosPostulacion::toArray(),
        ]);
    }
}
