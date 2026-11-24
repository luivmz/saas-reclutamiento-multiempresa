<?php

namespace App\Http\Controllers\Candidates;

use App\Enums\VacancyStatus;
use App\Http\Controllers\Controller;
use App\Http\Support\ConvocatoriaDeRetorno;
use App\Http\Support\Toast;
use App\Models\Application;
use App\Models\Scopes\OrganizationScope;
use App\Models\Vacancy;
use App\Services\Applications\ApplicationService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class ApplyController extends Controller
{
    public function __invoke(Request $request, int $vacancy, ApplicationService $applications, ConvocatoriaDeRetorno $retorno): RedirectResponse
    {
        Gate::authorize('apply', Application::class);

        $model = Vacancy::query()
            ->withoutGlobalScope(OrganizationScope::class)
            ->where('status', '!=', VacancyStatus::Draft)
            ->findOrFail($vacancy);

        $application = $applications->apply($request->user(), $model);
        // La postulación cierra el recorrido: la convocatoria de retorno ya no hace falta.
        $retorno->olvidar($request);
        Toast::success('Postulación registrada. La confirmación está en sus notificaciones.');

        return to_route('candidate.applications.show', $application);
    }
}
