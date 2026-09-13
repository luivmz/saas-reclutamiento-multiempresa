<?php

namespace App\Http\Controllers\Selection;

use App\Http\Controllers\Controller;
use App\Http\Requests\Selection\FinalDecisionRequest;
use App\Http\Support\Toast;
use App\Models\Vacancy;
use App\Services\Selection\FinalDecisionService;
use Illuminate\Http\RedirectResponse;

class FinalDecisionController extends Controller
{
    public function __invoke(FinalDecisionRequest $request, Vacancy $vacancy, FinalDecisionService $decisions): RedirectResponse
    {
        $decisions->decide(
            $vacancy,
            $request->user(),
            (int) $request->validated('application_id'),
            $request->validated('justification'),
        );

        Toast::success('Decisión final registrada. RR. HH. debe registrar la selección del candidato.');

        return back();
    }
}
