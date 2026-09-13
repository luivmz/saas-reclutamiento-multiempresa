<?php

namespace App\Http\Controllers\Assessments;

use App\Http\Controllers\Controller;
use App\Http\Presenters\AssessmentSessionPresenter;
use App\Http\Requests\Assessments\RecordInterviewResultRequest;
use App\Http\Support\Toast;
use App\Models\Interview;
use App\Services\Assessments\AssessmentResultRecorder;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

class InterviewController extends Controller
{
    public function show(Request $request, Interview $interview, AssessmentSessionPresenter $presenter): Response
    {
        Gate::authorize('view', $interview);

        return Inertia::render('assessments/show', $presenter->present($interview, $request->user()));
    }

    public function recordResult(RecordInterviewResultRequest $request, Interview $interview, AssessmentResultRecorder $recorder): RedirectResponse
    {
        $recorder->recordInterview($interview, $request->user(), $request->scores(), $request->outcome(), $request->validated('observations'));
        Toast::success('Entrevista y resultado registrados.');

        return back();
    }
}
