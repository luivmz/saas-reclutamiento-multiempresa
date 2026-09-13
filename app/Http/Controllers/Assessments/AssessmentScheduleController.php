<?php

namespace App\Http\Controllers\Assessments;

use App\Http\Controllers\Controller;
use App\Http\Requests\Assessments\ScheduleAssessmentRequest;
use App\Http\Requests\Assessments\ScheduleEvaluationRequest;
use App\Http\Support\Toast;
use App\Models\Application;
use App\Services\Assessments\AssessmentScheduler;
use Illuminate\Http\RedirectResponse;

class AssessmentScheduleController extends Controller
{
    public function __construct(private readonly AssessmentScheduler $scheduler) {}

    public function evaluation(ScheduleEvaluationRequest $request, Application $application): RedirectResponse
    {
        $this->scheduler->scheduleEvaluation($application, $request->user(), $request->validated());
        Toast::success('Evaluación programada. Se envió la convocatoria al candidato y al evaluador.');

        return back();
    }

    public function interview(ScheduleAssessmentRequest $request, Application $application): RedirectResponse
    {
        $this->scheduler->scheduleInterview($application, $request->user(), $request->validated());
        Toast::success('Entrevista programada. Se envió la convocatoria al candidato y al evaluador.');

        return back();
    }
}
