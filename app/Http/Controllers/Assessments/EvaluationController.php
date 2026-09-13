<?php

namespace App\Http\Controllers\Assessments;

use App\Http\Controllers\Controller;
use App\Http\Presenters\AssessmentSessionPresenter;
use App\Http\Requests\Assessments\RecordEvaluationResultRequest;
use App\Http\Support\Toast;
use App\Models\Evaluation;
use App\Services\Assessments\AssessmentResultRecorder;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

class EvaluationController extends Controller
{
    public function show(Request $request, Evaluation $evaluation, AssessmentSessionPresenter $presenter): Response
    {
        Gate::authorize('view', $evaluation);

        return Inertia::render('assessments/show', $presenter->present($evaluation, $request->user()));
    }

    public function recordResult(RecordEvaluationResultRequest $request, Evaluation $evaluation, AssessmentResultRecorder $recorder): RedirectResponse
    {
        $recorder->recordEvaluation($evaluation, $request->user(), $request->scores(), $request->validated('observations'));
        Toast::success('Resultados de la evaluación registrados.');

        return back();
    }
}
