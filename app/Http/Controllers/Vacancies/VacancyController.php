<?php

namespace App\Http\Controllers\Vacancies;

use App\Enums\ContractType;
use App\Enums\CriterionStage;
use App\Enums\JobRequestStatus;
use App\Enums\VacancyStatus;
use App\Http\Controllers\Controller;
use App\Http\Requests\Vacancies\VacancyFormRequest;
use App\Http\Resources\VacancyResource;
use App\Http\Support\Toast;
use App\Models\JobRequest;
use App\Models\Vacancy;
use App\Services\Evaluation\WeightingValidator;
use App\Services\Vacancies\VacancyService;
use App\Services\Vacancies\VacancyValidator;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

class VacancyController extends Controller
{
    public function __construct(
        private readonly VacancyService $vacancies,
        private readonly WeightingValidator $weights,
    ) {}

    public function index(Request $request): Response
    {
        Gate::authorize('viewAny', Vacancy::class);

        $status = VacancyStatus::tryFrom((string) $request->query('estado'));

        $vacancies = Vacancy::query()
            ->with('jobRequest:id,code,area,headcount')
            ->withCount('applications')
            ->when($status, fn ($query) => $query->where('status', $status))
            ->latest()
            ->paginate(15)
            ->withQueryString();

        return Inertia::render('vacancies/index', [
            'vacancies' => VacancyResource::collection($vacancies),
            'filters' => ['estado' => $status?->value],
            'statuses' => VacancyStatus::options(),
            'can' => ['create' => $request->user()->can('create', Vacancy::class)],
        ]);
    }

    public function create(Request $request): Response
    {
        Gate::authorize('create', Vacancy::class);

        return Inertia::render('vacancies/create', [
            ...$this->formOptions(),
            'jobRequests' => JobRequest::query()
                ->where('status', JobRequestStatus::Approved)
                ->whereDoesntHave('vacancy')
                ->orderBy('code')
                ->get(['id', 'code', 'position_title', 'area', 'headcount', 'contract_type'])
                ->map(fn (JobRequest $jobRequest) => [
                    'id' => $jobRequest->id,
                    'code' => $jobRequest->code,
                    'position_title' => $jobRequest->position_title,
                    'area' => $jobRequest->area,
                    'headcount' => $jobRequest->headcount,
                    'contract_type' => $jobRequest->contract_type->value,
                ]),
            'selectedJobRequestId' => $request->integer('requerimiento') ?: null,
        ]);
    }

    public function store(VacancyFormRequest $request): RedirectResponse
    {
        $jobRequest = JobRequest::query()->findOrFail($request->validated('job_request_id'));

        $vacancy = $this->vacancies->create(
            $request->user(),
            $jobRequest,
            $request->vacancyAttributes(),
            $request->profileAttributes(),
            $request->criteriaAttributes(),
        );

        Toast::success("Vacante {$vacancy->code} registrada como borrador.");

        return to_route('vacancies.show', $vacancy);
    }

    public function show(Request $request, Vacancy $vacancy, VacancyValidator $validator): Response
    {
        Gate::authorize('view', $vacancy);

        $vacancy->load(['jobRequest:id,code,area,headcount,status', 'profile', 'criteria'])->loadCount('applications');
        $issues = $vacancy->status === VacancyStatus::Draft ? $validator->issues($vacancy) : [];

        return Inertia::render('vacancies/show', [
            'vacancy' => new VacancyResource($vacancy),
            'validation' => [
                'publishable' => $vacancy->status === VacancyStatus::Draft && $issues === [],
                'issues' => $issues,
            ],
            'can' => [
                'update' => $request->user()->can('update', $vacancy) && $vacancy->status === VacancyStatus::Draft,
                'publish' => $request->user()->can('publish', $vacancy) && $vacancy->status === VacancyStatus::Draft,
            ],
        ]);
    }

    public function edit(Vacancy $vacancy): Response|RedirectResponse
    {
        Gate::authorize('update', $vacancy);

        if ($vacancy->status !== VacancyStatus::Draft) {
            Toast::error('Solo se puede configurar una vacante en borrador.');

            return to_route('vacancies.show', $vacancy);
        }

        $vacancy->load(['jobRequest:id,code,position_title,area,headcount', 'profile', 'criteria']);

        return Inertia::render('vacancies/edit', [
            ...$this->formOptions(),
            'vacancy' => new VacancyResource($vacancy),
        ]);
    }

    public function update(VacancyFormRequest $request, Vacancy $vacancy): RedirectResponse
    {
        $this->vacancies->update(
            $vacancy,
            $request->user(),
            $request->vacancyAttributes(),
            $request->profileAttributes(),
            $request->criteriaAttributes(),
        );

        Toast::success('Configuración de la vacante guardada.');

        return to_route('vacancies.show', $vacancy);
    }

    /**
     * @return array<string, mixed>
     */
    private function formOptions(): array
    {
        return [
            'contractTypes' => ContractType::options(),
            'stages' => CriterionStage::options(),
            'requiredWeightTotal' => $this->weights->requiredTotal(),
        ];
    }
}
