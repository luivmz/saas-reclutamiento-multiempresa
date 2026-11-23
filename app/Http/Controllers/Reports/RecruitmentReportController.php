<?php

namespace App\Http\Controllers\Reports;

use App\Enums\ApplicationStatus;
use App\Http\Controllers\Controller;
use App\Http\Requests\Reports\RecruitmentReportRequest;
use App\Services\Reports\RecruitmentReportService;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-28 (candidato): reportes operativos del proceso de reclutamiento.
 *
 * Solo lectura. La autorización (rol RR. HH./Aprobador con organización) y la
 * validación de filtros viven en el Form Request; el cálculo, en el servicio.
 */
class RecruitmentReportController extends Controller
{
    public function __invoke(RecruitmentReportRequest $request, RecruitmentReportService $reports): Response
    {
        $organizationId = (int) $request->user()->organization_id;
        [$from, $to] = $request->period();
        $vacancyId = $request->vacancyId();
        $status = $request->status();

        return Inertia::render('reports/index', [
            ...$reports->generate($organizationId, $from, $to, $vacancyId, $status),
            'filters' => [
                'desde' => $from->toDateString(),
                'hasta' => $to->toDateString(),
                'vacante' => $vacancyId === null ? null : (string) $vacancyId,
                'estado' => $status?->value,
            ],
            'vacancies' => $reports->vacancyOptions($organizationId),
            'statuses' => ApplicationStatus::options(),
        ]);
    }
}
