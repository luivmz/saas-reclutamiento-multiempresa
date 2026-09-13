<?php

namespace App\Http\Controllers\Candidates;

use App\Enums\VacancyStatus;
use App\Http\Controllers\Controller;
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
    public function __invoke(Request $request, int $vacancy, ApplicationService $applications): RedirectResponse
    {
        Gate::authorize('apply', Application::class);

        $model = Vacancy::query()
            ->withoutGlobalScope(OrganizationScope::class)
            ->where('status', '!=', VacancyStatus::Draft)
            ->findOrFail($vacancy);

        $application = $applications->apply($request->user(), $model);
        Toast::success('Postulación registrada. La confirmación está en sus notificaciones.');

        return to_route('candidate.applications.show', $application);
    }
}
