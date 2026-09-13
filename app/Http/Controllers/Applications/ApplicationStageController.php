<?php

namespace App\Http\Controllers\Applications;

use App\Http\Controllers\Controller;
use App\Http\Requests\Applications\ChangeApplicationStageRequest;
use App\Http\Requests\Applications\DiscardApplicationRequest;
use App\Http\Requests\Applications\StageCommentRequest;
use App\Http\Support\Toast;
use App\Models\Application;
use App\Services\Applications\ApplicationStageService;
use Illuminate\Http\RedirectResponse;

class ApplicationStageController extends Controller
{
    public function __construct(private readonly ApplicationStageService $stages) {}

    public function shortlist(StageCommentRequest $request, Application $application): RedirectResponse
    {
        $this->stages->shortlist($application, $request->user(), $request->validated('comment'));
        Toast::success('Postulación preseleccionada. Se notificó al candidato.');

        return back();
    }

    public function discard(DiscardApplicationRequest $request, Application $application): RedirectResponse
    {
        $this->stages->discard($application, $request->user(), $request->validated('comment'));
        Toast::success('Postulación descartada. Se notificó al candidato.');

        return back();
    }

    public function change(ChangeApplicationStageRequest $request, Application $application): RedirectResponse
    {
        $target = $request->target();
        $this->stages->moveTo($application, $target, $request->user(), $request->validated('comment'));
        Toast::success("Etapa actualizada a «{$target->label()}». Se notificó al candidato.");

        return back();
    }
}
