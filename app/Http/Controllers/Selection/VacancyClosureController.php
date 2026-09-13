<?php

namespace App\Http\Controllers\Selection;

use App\Http\Controllers\Controller;
use App\Http\Requests\Selection\CloseVacancyRequest;
use App\Http\Support\Toast;
use App\Models\Vacancy;
use App\Services\Selection\VacancyClosureService;
use Illuminate\Http\RedirectResponse;

class VacancyClosureController extends Controller
{
    public function __invoke(CloseVacancyRequest $request, Vacancy $vacancy, VacancyClosureService $closures): RedirectResponse
    {
        $closures->close($vacancy, $request->user(), $request->validated('closure_notes'));
        Toast::success('Convocatoria cerrada. Las demás postulaciones activas quedaron como «No seleccionado».');

        return back();
    }
}
