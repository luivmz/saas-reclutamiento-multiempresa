<?php

namespace App\Http\Controllers\Assessments;

use App\Enums\AssessmentStatus;
use App\Enums\CriterionStage;
use App\Http\Controllers\Controller;
use App\Models\Evaluation;
use App\Models\Interview;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

/**
 * Evaluations and interviews assigned to the authenticated evaluator.
 */
class AssessmentAssignmentController extends Controller
{
    private const RELATIONS = [
        'application:id,organization_id,vacancy_id,candidate_id',
        'application.candidate:id,name',
        'application.vacancy:id,organization_id,code,title',
    ];

    public function __invoke(Request $request): Response
    {
        $evaluatorId = $request->user()->id;

        $evaluations = Evaluation::query()->where('evaluator_id', $evaluatorId)->with(self::RELATIONS)->get()
            ->map(fn (Evaluation $evaluation) => $this->row($evaluation, CriterionStage::Evaluation, $evaluation->type->label(), route('evaluations.show', $evaluation, absolute: false)));

        $interviews = Interview::query()->where('evaluator_id', $evaluatorId)->with(self::RELATIONS)->get()
            ->map(fn (Interview $interview) => $this->row($interview, CriterionStage::Interview, 'Entrevista personal', route('interviews.show', $interview, absolute: false)));

        $assignments = $evaluations->concat($interviews)
            ->sortBy(fn (array $row) => [$row['status']['value'] === AssessmentStatus::Completed->value ? 1 : 0, $row['scheduled_at']])
            ->values();

        return Inertia::render('assessments/index', ['assignments' => $assignments]);
    }

    /**
     * @return array<string, mixed>
     */
    private function row(Evaluation|Interview $session, CriterionStage $kind, string $title, string $url): array
    {
        return [
            'key' => $kind->value.'-'.$session->id,
            'id' => $session->id,
            'kind' => $kind->present(),
            'title' => $title,
            'candidate' => $session->application->candidate->name,
            'vacancy' => $session->application->vacancy->code.' · '.$session->application->vacancy->title,
            'scheduled_at' => $session->scheduled_at->toIso8601String(),
            'modality' => $session->modality->label(),
            'location' => $session->location,
            'status' => $session->status->present(),
            'url' => $url,
        ];
    }
}
