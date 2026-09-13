<?php

namespace App\Http\Controllers\JobRequests;

use App\Enums\ContractType;
use App\Enums\JobRequestStatus;
use App\Enums\UserRole;
use App\Http\Controllers\Controller;
use App\Http\Requests\JobRequests\JobRequestFormRequest;
use App\Http\Resources\JobRequestResource;
use App\Http\Support\Toast;
use App\Models\JobRequest;
use App\Models\JobRequestStatusHistory;
use App\Models\Vacancy;
use App\Services\JobRequests\JobRequestWorkflow;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

class JobRequestController extends Controller
{
    public function __construct(private readonly JobRequestWorkflow $workflow) {}

    public function index(Request $request): Response
    {
        Gate::authorize('viewAny', JobRequest::class);

        $user = $request->user();
        $status = JobRequestStatus::tryFrom((string) $request->query('estado'));

        $jobRequests = JobRequest::query()
            ->with('requester:id,name')
            ->when(
                $user->hasRole(UserRole::Requester),
                fn ($query) => $query->where('requested_by', $user->id),
                fn ($query) => $query->where('status', '!=', JobRequestStatus::Draft),
            )
            ->when($status, fn ($query) => $query->where('status', $status))
            ->latest()
            ->paginate(15)
            ->withQueryString();

        return Inertia::render('job-requests/index', [
            'jobRequests' => JobRequestResource::collection($jobRequests),
            'filters' => ['estado' => $status?->value],
            'statuses' => JobRequestStatus::options(),
            'can' => ['create' => $user->can('create', JobRequest::class)],
        ]);
    }

    public function create(): Response
    {
        Gate::authorize('create', JobRequest::class);

        return Inertia::render('job-requests/create', [
            'contractTypes' => ContractType::options(),
        ]);
    }

    public function store(JobRequestFormRequest $request): RedirectResponse
    {
        $jobRequest = $this->workflow->register($request->user(), $request->validated());

        Toast::success("Requerimiento {$jobRequest->code} registrado como borrador.");

        return to_route('job-requests.show', $jobRequest);
    }

    public function show(Request $request, JobRequest $jobRequest): Response
    {
        Gate::authorize('view', $jobRequest);

        $jobRequest->load(['requester:id,name', 'vacancy:id,job_request_id,code,status', 'statusHistories.author:id,name']);
        $user = $request->user();
        $status = $jobRequest->status;

        return Inertia::render('job-requests/show', [
            'jobRequest' => new JobRequestResource($jobRequest),
            'history' => $jobRequest->statusHistories->sortBy('id')->values()->map(fn (JobRequestStatusHistory $history) => [
                'id' => $history->id,
                'from' => $history->from_status?->present(),
                'to' => $history->to_status->present(),
                'author' => $history->author->name,
                'comment' => $history->comment,
                'created_at' => $history->created_at->toIso8601String(),
            ]),
            'can' => [
                'update' => $user->can('update', $jobRequest) && $status->isEditable(),
                'submit' => $user->can('submit', $jobRequest) && $status->canTransitionTo(JobRequestStatus::Submitted),
                'review' => $user->can('review', $jobRequest) && $status === JobRequestStatus::Submitted,
                'decide' => $user->can('decide', $jobRequest) && $status === JobRequestStatus::Validated,
                'createVacancy' => $user->can('create', Vacancy::class) && $status === JobRequestStatus::Approved && $jobRequest->vacancy === null,
            ],
        ]);
    }

    public function edit(JobRequest $jobRequest): Response|RedirectResponse
    {
        Gate::authorize('update', $jobRequest);

        if (! $jobRequest->status->isEditable()) {
            Toast::error('Solo se puede modificar un requerimiento en borrador u observado.');

            return to_route('job-requests.show', $jobRequest);
        }

        return Inertia::render('job-requests/edit', [
            'jobRequest' => new JobRequestResource($jobRequest),
            'contractTypes' => ContractType::options(),
        ]);
    }

    public function update(JobRequestFormRequest $request, JobRequest $jobRequest): RedirectResponse
    {
        $this->workflow->correct($jobRequest, $request->user(), $request->validated());

        Toast::success('Requerimiento actualizado.');

        return to_route('job-requests.show', $jobRequest);
    }
}
