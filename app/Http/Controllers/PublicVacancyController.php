<?php

namespace App\Http\Controllers;

use App\Http\Resources\VacancyResource;
use App\Models\Scopes\OrganizationScope;
use App\Models\Vacancy;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

/**
 * RF-07: public listing of published vacancies across organizations.
 */
class PublicVacancyController extends Controller
{
    public function index(Request $request): Response
    {
        $search = trim((string) $request->query('q'));

        $vacancies = $this->publishedVacancies()
            ->with('organization:id,name')
            ->when($search !== '', fn (Builder $query) => $query->where('title', 'ilike', '%'.$search.'%'))
            ->orderBy('closes_at')
            ->paginate(12)
            ->withQueryString();

        return Inertia::render('jobs/index', [
            'vacancies' => VacancyResource::collection($vacancies),
            'filters' => ['q' => $search],
        ]);
    }

    public function show(int $vacancy): Response
    {
        $model = $this->publishedVacancies()
            ->with(['organization:id,name', 'profile', 'criteria'])
            ->findOrFail($vacancy);

        return Inertia::render('jobs/show', [
            'vacancy' => new VacancyResource($model),
        ]);
    }

    /**
     * @return Builder<Vacancy>
     */
    private function publishedVacancies(): Builder
    {
        return Vacancy::query()->withoutGlobalScope(OrganizationScope::class)->published();
    }
}
