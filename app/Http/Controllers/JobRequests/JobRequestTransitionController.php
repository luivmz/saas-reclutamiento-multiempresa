<?php

namespace App\Http\Controllers\JobRequests;

use App\Enums\JobRequestDecision;
use App\Http\Controllers\Controller;
use App\Http\Requests\JobRequests\DecideJobRequestRequest;
use App\Http\Requests\JobRequests\ObserveJobRequestRequest;
use App\Http\Support\Toast;
use App\Models\JobRequest;
use App\Services\JobRequests\JobRequestWorkflow;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class JobRequestTransitionController extends Controller
{
    public function __construct(private readonly JobRequestWorkflow $workflow) {}

    public function submit(Request $request, JobRequest $jobRequest): RedirectResponse
    {
        Gate::authorize('submit', $jobRequest);

        $this->workflow->submit($jobRequest, $request->user());
        Toast::success('Requerimiento enviado a RR. HH. para su validación.');

        return back();
    }

    public function observe(ObserveJobRequestRequest $request, JobRequest $jobRequest): RedirectResponse
    {
        $this->workflow->observe($jobRequest, $request->user(), $request->validated('comment'));
        Toast::success('Requerimiento observado y devuelto al área solicitante.');

        return back();
    }

    public function validate(Request $request, JobRequest $jobRequest): RedirectResponse
    {
        Gate::authorize('review', $jobRequest);

        $this->workflow->validate($jobRequest, $request->user());
        Toast::success('Requerimiento validado y remitido al aprobador.');

        return back();
    }

    public function decide(DecideJobRequestRequest $request, JobRequest $jobRequest): RedirectResponse
    {
        $comment = $request->validated('comment');

        match ($request->decision()) {
            JobRequestDecision::Approve => $this->workflow->approve($jobRequest, $request->user(), $comment),
            JobRequestDecision::Reject => $this->workflow->reject($jobRequest, $request->user(), (string) $comment),
        };

        Toast::success($request->decision() === JobRequestDecision::Approve ? 'Requerimiento aprobado.' : 'Requerimiento rechazado. Se notificó al área solicitante.');

        return back();
    }
}
