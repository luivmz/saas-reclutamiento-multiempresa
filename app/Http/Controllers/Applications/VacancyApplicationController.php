<?php

namespace App\Http\Controllers\Applications;

use App\Enums\ApplicationStatus;
use App\Http\Controllers\Controller;
use App\Http\Resources\ApplicationResource;
use App\Http\Resources\VacancyResource;
use App\Models\Application;
use App\Models\Vacancy;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-12: list and filter the applications of a vacancy.
 */
class VacancyApplicationController extends Controller
{
    public function __invoke(Request $request, Vacancy $vacancy): Response
    {
        Gate::authorize('viewAnyForVacancy', [Application::class, $vacancy]);

        $status = ApplicationStatus::tryFrom((string) $request->query('estado'));

        $applications = $vacancy->applications()
            ->with(['candidate:id,name,email', 'candidate.candidateProfile'])
            ->when($status, fn ($query) => $query->where('status', $status))
            ->orderBy('applied_at')
            ->paginate(20)
            ->withQueryString();

        $counts = $vacancy->applications()
            ->toBase()
            ->selectRaw('status, count(*) as total')
            ->groupBy('status')
            ->pluck('total', 'status');

        return Inertia::render('applications/index', [
            'vacancy' => new VacancyResource($vacancy),
            'applications' => ApplicationResource::collection($applications),
            'statuses' => array_map(fn (ApplicationStatus $case) => [
                ...$case->present(),
                'count' => (int) ($counts[$case->value] ?? 0),
            ], ApplicationStatus::cases()),
            'filters' => ['estado' => $status?->value],
        ]);
    }
}
