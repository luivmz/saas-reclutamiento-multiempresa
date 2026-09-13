<?php

namespace App\Http\Controllers\Vacancies;

use App\Http\Controllers\Controller;
use App\Http\Support\Toast;
use App\Models\Vacancy;
use App\Services\Vacancies\VacancyService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class VacancyPublicationController extends Controller
{
    public function __invoke(Request $request, Vacancy $vacancy, VacancyService $vacancies): RedirectResponse
    {
        Gate::authorize('publish', $vacancy);

        $published = $vacancies->publish($vacancy, $request->user());
        Toast::success("Vacante {$published->code} publicada. Ya es visible en el portal de empleos.");

        return back();
    }
}
