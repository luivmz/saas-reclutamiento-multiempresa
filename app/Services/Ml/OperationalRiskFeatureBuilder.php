<?php

namespace App\Services\Ml;

use App\Models\Vacancy;
use Carbon\CarbonInterface;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\DB;

/**
 * Construye las 15 features operacionales de una vacante, en Laravel.
 *
 * Implementa `docs/v1.1/ml/feature-contract.md` con las fuentes reales del
 * dominio. Tres reglas gobiernan todo el archivo:
 *
 * 1. **Truncado al checkpoint.** Ningún conteo mira más allá del instante de
 *    observación. Es lo que impide que la feature contenga información del
 *    desenlace.
 * 2. **Scoping explícito por organización.** `OrganizationScope` ya filtra
 *    cuando hay un usuario autenticado, pero este servicio puede ejecutarse en
 *    consola o en cola, donde `Auth` está vacío y el scope global no hace
 *    nada. Cada consulta repite el filtro a propósito: la multiempresa no
 *    puede depender de que exista sesión.
 * 3. **Cero datos de personas.** Se cuentan eventos, nunca sus protagonistas
 *    ni sus resultados. `interviews.outcome`, `evaluation_results.score`,
 *    `evaluator_id` y `candidate_id` no se leen aquí y no pueden leerse.
 */
class OperationalRiskFeatureBuilder
{
    /**
     * Construye el vector para una vacante en un instante de observación.
     *
     * @param  CarbonInterface|null  $checkpoint  Instante de observación; por omisión, ahora.
     */
    public function build(Vacancy $vacancy, ?CarbonInterface $checkpoint = null): OperationalRiskFeatures
    {
        $at = Carbon::instance(($checkpoint ?? Carbon::now())->toDateTime())
            ->setTimezone(config('app.timezone'));

        $applicationIds = $this->applicationIds($vacancy, $at);

        return OperationalRiskFeatures::fromArray([
            // ML-FEAT-01
            'elapsed_days_since_publication' => $this->elapsedDaysSincePublication($vacancy, $at),
            // ML-FEAT-03
            'application_window_days' => $this->applicationWindowDays($vacancy),
            // ML-FEAT-04
            'positions_count' => (int) $vacancy->positions,
            // ML-FEAT-05
            'applications_received_count' => count($applicationIds),
            // ML-FEAT-06
            'configured_criteria_count' => $this->criteriaCount($vacancy),
            // ML-FEAT-08, 09, 11
            'evaluations_scheduled_count' => $this->scheduledCount('evaluations', $vacancy, $applicationIds, $at),
            'evaluations_completed_count' => $this->completedCount('evaluations', $vacancy, $applicationIds, $at),
            'evaluations_overdue_pending_count' => $this->overduePendingCount('evaluations', $vacancy, $applicationIds, $at),
            // ML-FEAT-12, 13, 15
            'interviews_scheduled_count' => $this->scheduledCount('interviews', $vacancy, $applicationIds, $at),
            'interviews_completed_count' => $this->completedCount('interviews', $vacancy, $applicationIds, $at),
            'interviews_overdue_pending_count' => $this->overduePendingCount('interviews', $vacancy, $applicationIds, $at),
            // ML-FEAT-16
            'stage_transition_count' => $this->stageTransitionCount($vacancy, $applicationIds, $at),
            // ML-FEAT-17
            'days_since_last_operational_event' => $this->daysSinceLastEvent($vacancy, $applicationIds, $at),
            // ML-FEAT-18
            'concurrent_open_vacancies_count' => $this->concurrentOpenVacancies($vacancy, $at),
            // ML-FEAT-02 (GAP-01)
            'days_remaining_to_target' => $this->daysRemainingToTarget($vacancy, $at),
        ]);
    }

    /**
     * Días completos entre el plazo objetivo y el checkpoint.
     *
     * Puede salir cero o negativo cuando el plazo ya venció. **No se recorta
     * a uno**: el contrato del servicio exige un valor positivo, y quien
     * decide si la vacante está dentro del dominio del modelo es
     * `OperationalRiskDomain`, no este cálculo. Falsear el número aquí
     * fabricaría exactamente la feature que justifica toda la fase.
     */
    public function daysRemainingToTarget(Vacancy $vacancy, CarbonInterface $at): int
    {
        if ($vacancy->target_completion_at === null) {
            return 0;
        }

        return $this->wholeDays($at, $vacancy->target_completion_at);
    }

    // -- ML-FEAT-01 y 03 ----------------------------------------------------

    private function elapsedDaysSincePublication(Vacancy $vacancy, CarbonInterface $at): int
    {
        if ($vacancy->published_at === null) {
            return 0;
        }

        return max(0, $this->wholeDays($vacancy->published_at, $at));
    }

    /**
     * `días(closes_at − opens_at)`, con la regla de respaldo del contrato:
     * si `opens_at` es nulo se usa la fecha de publicación.
     */
    private function applicationWindowDays(Vacancy $vacancy): int
    {
        if ($vacancy->closes_at === null) {
            return 0;
        }

        $start = $vacancy->opens_at ?? $vacancy->published_at?->copy()->startOfDay();

        if ($start === null) {
            return 0;
        }

        return max(0, $this->wholeDays($start, $vacancy->closes_at));
    }

    // -- conteos ------------------------------------------------------------

    /**
     * Identificadores de las postulaciones recibidas hasta el checkpoint.
     *
     * Son identificadores internos usados solo para agregar; ninguno sale
     * hacia el servicio ni hacia la vista.
     *
     * @return list<int>
     */
    private function applicationIds(Vacancy $vacancy, CarbonInterface $at): array
    {
        return DB::table('applications')
            ->where('organization_id', $vacancy->organization_id)
            ->where('vacancy_id', $vacancy->getKey())
            ->where('applied_at', '<=', $at)
            ->pluck('id')
            ->map(static fn ($id): int => (int) $id)
            ->all();
    }

    private function criteriaCount(Vacancy $vacancy): int
    {
        return DB::table('evaluation_criteria')
            ->where('organization_id', $vacancy->organization_id)
            ->where('vacancy_id', $vacancy->getKey())
            ->count();
    }

    /**
     * `count(sesiones creadas hasta el checkpoint)`. Se cuenta el acto de
     * programar, nunca su resultado.
     *
     * @param  list<int>  $applicationIds
     */
    private function scheduledCount(string $table, Vacancy $vacancy, array $applicationIds, CarbonInterface $at): int
    {
        if ($applicationIds === []) {
            return 0;
        }

        return DB::table($table)
            ->where('organization_id', $vacancy->organization_id)
            ->whereIn('application_id', $applicationIds)
            ->where('created_at', '<=', $at)
            ->count();
    }

    /**
     * @param  list<int>  $applicationIds
     */
    private function completedCount(string $table, Vacancy $vacancy, array $applicationIds, CarbonInterface $at): int
    {
        if ($applicationIds === []) {
            return 0;
        }

        return DB::table($table)
            ->where('organization_id', $vacancy->organization_id)
            ->whereIn('application_id', $applicationIds)
            ->whereNotNull('completed_at')
            ->where('completed_at', '<=', $at)
            ->count();
    }

    /**
     * Backlog vencido: programado antes del checkpoint y todavía sin completar
     * en ese instante.
     *
     * @param  list<int>  $applicationIds
     */
    private function overduePendingCount(string $table, Vacancy $vacancy, array $applicationIds, CarbonInterface $at): int
    {
        if ($applicationIds === []) {
            return 0;
        }

        return DB::table($table)
            ->where('organization_id', $vacancy->organization_id)
            ->whereIn('application_id', $applicationIds)
            ->where('created_at', '<=', $at)
            ->where('scheduled_at', '<', $at)
            ->where(function ($query) use ($at): void {
                $query->whereNull('completed_at')->orWhere('completed_at', '>', $at);
            })
            ->count();
    }

    /**
     * Total de movimientos de etapa, **sin desagregar por estado destino**:
     * desagregarlo reintroduciría resultados individuales sobre personas.
     *
     * @param  list<int>  $applicationIds
     */
    private function stageTransitionCount(Vacancy $vacancy, array $applicationIds, CarbonInterface $at): int
    {
        if ($applicationIds === []) {
            return 0;
        }

        return DB::table('application_stage_histories')
            ->where('organization_id', $vacancy->organization_id)
            ->whereIn('application_id', $applicationIds)
            ->where('created_at', '<=', $at)
            ->count();
    }

    // -- ML-FEAT-17 ---------------------------------------------------------

    /**
     * Días desde el último evento operacional, sobre una lista **cerrada** de
     * eventos: publicación, postulaciones, sesiones creadas o completadas y
     * movimientos de etapa. Si no hay ninguno posterior, el máximo es la
     * publicación, así que nunca queda indefinida.
     *
     * @param  list<int>  $applicationIds
     */
    private function daysSinceLastEvent(Vacancy $vacancy, array $applicationIds, CarbonInterface $at): int
    {
        $candidates = [];

        if ($vacancy->published_at !== null && $vacancy->published_at->lte($at)) {
            $candidates[] = $vacancy->published_at;
        }

        $candidates[] = $this->maxTimestamp('applications', 'applied_at', $vacancy, ['vacancy_id' => $vacancy->getKey()], $at);

        if ($applicationIds !== []) {
            foreach (['evaluations', 'interviews'] as $table) {
                foreach (['created_at', 'completed_at'] as $column) {
                    $candidates[] = $this->maxTimestampIn($table, $column, $vacancy, $applicationIds, $at);
                }
            }
            $candidates[] = $this->maxTimestampIn('application_stage_histories', 'created_at', $vacancy, $applicationIds, $at);
        }

        /** @var list<CarbonInterface> $found */
        $found = array_values(array_filter($candidates));

        if ($found === []) {
            return 0;
        }

        $latest = $found[0];
        foreach ($found as $moment) {
            if ($moment->gt($latest)) {
                $latest = $moment;
            }
        }

        return max(0, $this->wholeDays($latest, $at));
    }

    /**
     * @param  array<string, mixed>  $conditions
     */
    private function maxTimestamp(string $table, string $column, Vacancy $vacancy, array $conditions, CarbonInterface $at): ?Carbon
    {
        $value = DB::table($table)
            ->where('organization_id', $vacancy->organization_id)
            ->where($conditions)
            ->where($column, '<=', $at)
            ->max($column);

        return $value === null ? null : Carbon::parse($value);
    }

    /**
     * @param  list<int>  $applicationIds
     */
    private function maxTimestampIn(string $table, string $column, Vacancy $vacancy, array $applicationIds, CarbonInterface $at): ?Carbon
    {
        $value = DB::table($table)
            ->where('organization_id', $vacancy->organization_id)
            ->whereIn('application_id', $applicationIds)
            ->where($column, '<=', $at)
            ->max($column);

        return $value === null ? null : Carbon::parse($value);
    }

    // -- ML-FEAT-18 ---------------------------------------------------------

    /**
     * Vacantes de la **misma organización** abiertas en el checkpoint, sin
     * contar la propia.
     *
     * `organization_id` agrupa; jamás viaja como señal al modelo.
     */
    private function concurrentOpenVacancies(Vacancy $vacancy, CarbonInterface $at): int
    {
        return DB::table('vacancies')
            ->where('organization_id', $vacancy->organization_id)
            ->where('id', '!=', $vacancy->getKey())
            ->whereNotNull('published_at')
            ->where('published_at', '<=', $at)
            ->where(function ($query) use ($at): void {
                $query->whereNull('closed_at')->orWhere('closed_at', '>', $at);
            })
            ->count();
    }

    // -- utilidades ---------------------------------------------------------

    /**
     * Días completos entre dos instantes, en la zona horaria del proyecto.
     */
    private function wholeDays(CarbonInterface $from, CarbonInterface $to): int
    {
        $timezone = config('app.timezone');

        $start = Carbon::instance($from->toDateTime())->setTimezone($timezone);
        $end = Carbon::instance($to->toDateTime())->setTimezone($timezone);

        return (int) floor($start->diffInDays($end, false));
    }
}
