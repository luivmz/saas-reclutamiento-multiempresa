<?php

namespace App\Http\Controllers\Selection;

use App\Http\Controllers\Controller;
use App\Http\Support\Toast;
use App\Models\Vacancy;
use App\Services\Selection\SelectionRegistrationService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class SelectionRegistrationController extends Controller
{
    public function __invoke(Request $request, Vacancy $vacancy, SelectionRegistrationService $selections): RedirectResponse
    {
        Gate::authorize('registerSelection', $vacancy);

        $selections->register($vacancy, $request->user());
        Toast::success('Selección registrada: la postulación elegida quedó como «Seleccionado».');

        return back();
    }
}
