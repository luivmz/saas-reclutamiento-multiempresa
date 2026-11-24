<?php

namespace App\Http\Controllers;

use App\Enums\ContractType;
use App\Http\Requests\Vacancies\PublicVacancyFilterRequest;
use App\Http\Resources\VacancyResource;
use App\Http\Support\RequisitosPostulacion;
use App\Models\Application;
use App\Models\CandidateProfile;
use App\Models\Organization;
use App\Models\Scopes\OrganizationScope;
use App\Models\User;
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
    /**
     * Búsqueda por puesto y filtros por organización, ubicación y tipo de contrato, combinados con AND. Igual que
     * antes, el listado muestra todas las convocatorias publicadas, también las de plazo vencido (con su
     * distintivo): publicada no equivale a «recibiendo postulaciones».
     */
    public function index(PublicVacancyFilterRequest $request): Response
    {
        $criteria = $request->criteria();

        $vacancies = $this->publishedVacancies()
            ->with('organization:id,name')
            ->when($criteria['q'] !== '', fn (Builder $query) => $query->where('title', 'ilike', '%'.$criteria['q'].'%'))
            ->when($criteria['organizacion'] !== null, fn (Builder $query) => $query->where('organization_id', $criteria['organizacion']))
            ->when($criteria['ubicacion'] !== null, fn (Builder $query) => $query->where('location', $criteria['ubicacion']))
            ->when($criteria['contrato'] !== null, fn (Builder $query) => $query->where('contract_type', $criteria['contrato']))
            ->orderBy('closes_at')
            // Desempate estable: con fechas de cierre iguales, cada página conserva siempre las mismas convocatorias.
            ->orderBy('id')
            ->paginate(12)
            ->withQueryString();

        return Inertia::render('jobs/index', [
            'vacancies' => VacancyResource::collection($vacancies),
            'filters' => $criteria,
            'options' => $this->filterOptions(),
        ]);
    }

    public function show(Request $request, int $vacancy): Response
    {
        $model = $this->publishedVacancies()
            ->with(['organization:id,name', 'profile', 'criteria'])
            ->findOrFail($vacancy);

        return Inertia::render('jobs/show', [
            'vacancy' => new VacancyResource($model),
            'candidate' => $this->candidateContext($request->user(), $model),
            // Requisitos comunes a toda postulación (perfil y CV), distintos de los de esta convocatoria.
            'requisitos' => RequisitosPostulacion::toArray(),
        ]);
    }

    /**
     * @return array<string, mixed>|null
     */
    private function candidateContext(?User $user, Vacancy $vacancy): ?array
    {
        if ($user === null || ! $user->isCandidate()) {
            return null;
        }

        $profile = CandidateProfile::query()->with('latestCv')->where('user_id', $user->id)->first();
        $application = Application::query()
            ->withoutGlobalScopes()
            ->where('vacancy_id', $vacancy->id)
            ->where('candidate_id', $user->id)
            ->first();

        return [
            'profileComplete' => $profile?->isComplete() ?? false,
            'hasCv' => $profile?->latestCv !== null,
            'application' => $application === null ? null : [
                'id' => $application->id,
                'status' => $application->status->present(),
            ],
        ];
    }

    /**
     * Opciones de los filtros, tomadas solo de convocatorias publicadas: lo que no se ve en el listado tampoco
     * aparece como opción. Tres consultas, sin depender del número de convocatorias.
     *
     * @return array<string, array<array{value: string, label: string}>>
     */
    private function filterOptions(): array
    {
        $organizations = Organization::query()
            ->whereIn('id', $this->publishedVacancies()->select('organization_id'))
            ->orderBy('name')
            ->get(['id', 'name'])
            ->map(fn (Organization $organization) => ['value' => (string) $organization->id, 'label' => $organization->name])
            ->all();

        $locations = $this->publishedVacancies()
            ->distinct()
            ->orderBy('location')
            ->pluck('location')
            ->map(fn (string $location) => ['value' => $location, 'label' => $location])
            ->all();

        $present = $this->publishedVacancies()->distinct()->pluck('contract_type')
            ->map(fn (ContractType|string $type) => $type instanceof ContractType ? $type->value : $type)
            ->all();
        $contracts = collect(ContractType::cases())
            ->filter(fn (ContractType $type) => in_array($type->value, $present, true))
            ->map(fn (ContractType $type) => ['value' => $type->value, 'label' => $type->label()])
            ->values()
            ->all();

        return ['organizaciones' => $organizations, 'ubicaciones' => $locations, 'contratos' => $contracts];
    }

    /**
     * @return Builder<Vacancy>
     */
    private function publishedVacancies(): Builder
    {
        return Vacancy::query()->withoutGlobalScope(OrganizationScope::class)->published();
    }
}
