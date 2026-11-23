<?php

namespace App\Services\Reports;

use App\Enums\ApplicationStatus;
use App\Enums\VacancyStatus;
use App\Models\Application;
use App\Models\Vacancy;
use Carbon\CarbonImmutable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

/**
 * RF-28 (candidato): indicadores operativos del proceso de reclutamiento.
 *
 * Todo se calcula a partir de registros almacenados (postulaciones, su
 * historial de etapas y vacantes) y **siempre** dentro de una organización:
 * además del scope global de `BelongsToOrganization`, cada consulta filtra
 * explícitamente por `organization_id`.
 *
 * Los indicadores describen el **proceso** (volumen, avance y tiempos); no
 * puntúan, ordenan ni clasifican personas, y no devuelven nombres, correos ni
 * puntajes. Indicadores, gráficos y tabla salen del mismo conjunto filtrado,
 * de modo que nunca se contradicen entre sí.
 *
 * @phpstan-type ReportRow object{vacancy_id: int, status: ApplicationStatus, applied_at: CarbonImmutable, shortlisted_at: CarbonImmutable|null, reached_shortlist: bool}&\stdClass
 */
final class RecruitmentReportService
{
    /**
     * Etapas a las que solo se llega habiendo pasado por la preselección.
     *
     * @var list<ApplicationStatus>
     */
    private const AFTER_SHORTLIST = [
        ApplicationStatus::Shortlisted,
        ApplicationStatus::Evaluation,
        ApplicationStatus::Interview,
        ApplicationStatus::Finalist,
        ApplicationStatus::Selected,
    ];

    /**
     * @var list<ApplicationStatus>
     */
    private const IN_ASSESSMENT = [
        ApplicationStatus::Evaluation,
        ApplicationStatus::Interview,
    ];

    /**
     * @return array{
     *     indicators: array<string, int|float|null>,
     *     by_status: list<array{value: string, label: string, tone: string, count: int}>,
     *     by_week: list<array{week_start: string, count: int}>,
     *     by_vacancy: array<int, array<string, mixed>>
     * }
     */
    public function generate(
        int $organizationId,
        CarbonImmutable $from,
        CarbonImmutable $to,
        ?int $vacancyId = null,
        ?ApplicationStatus $status = null,
    ): array {
        $rows = $this->applicationRows($organizationId, $from, $to, $vacancyId, $status);

        return [
            'indicators' => $this->indicators($rows, $this->publishedVacancies($organizationId, $from, $to, $vacancyId)),
            'by_status' => $this->byStatus($rows),
            'by_week' => $this->byWeek($rows, $from, $to),
            'by_vacancy' => $this->byVacancy($rows, $organizationId),
        ];
    }

    /**
     * Vacantes que pueden filtrarse: publicadas o cerradas de la organización.
     *
     * @return array<int, array{value: string, label: string}>
     */
    public function vacancyOptions(int $organizationId): array
    {
        return Vacancy::query()
            ->where('organization_id', $organizationId)
            ->whereNot('status', VacancyStatus::Draft)
            ->orderByDesc('published_at')
            ->orderByDesc('id')
            ->get(['id', 'code', 'title'])
            ->map(fn (Vacancy $vacancy) => [
                'value' => (string) $vacancy->id,
                'label' => "{$vacancy->code} · {$vacancy->title}",
            ])
            ->values()
            ->all();
    }

    /**
     * Una fila por postulación filtrada, sin datos personales.
     *
     * @return Collection<int, ReportRow>
     */
    private function applicationRows(int $organizationId, CarbonImmutable $from, CarbonImmutable $to, ?int $vacancyId, ?ApplicationStatus $status): Collection
    {
        $firstShortlist = DB::table('application_stage_histories')
            ->selectRaw('min(application_stage_histories.created_at)')
            ->whereColumn('application_stage_histories.application_id', 'applications.id')
            ->where('application_stage_histories.organization_id', $organizationId)
            ->where('application_stage_histories.to_status', ApplicationStatus::Shortlisted->value);

        return Application::query()
            ->where('applications.organization_id', $organizationId)
            ->whereBetween('applications.applied_at', [$from, $to])
            ->when($vacancyId, fn (Builder $query) => $query->where('applications.vacancy_id', $vacancyId))
            ->when($status, fn (Builder $query) => $query->where('applications.status', $status))
            ->toBase()
            ->select(['applications.vacancy_id', 'applications.status', 'applications.applied_at'])
            ->selectSub($firstShortlist, 'shortlisted_at')
            ->get()
            ->map(function (object $row): object {
                $state = ApplicationStatus::from($row->status);
                $shortlistedAt = $row->shortlisted_at === null ? null : CarbonImmutable::parse($row->shortlisted_at);

                return (object) [
                    'vacancy_id' => (int) $row->vacancy_id,
                    'status' => $state,
                    'applied_at' => CarbonImmutable::parse($row->applied_at),
                    'shortlisted_at' => $shortlistedAt,
                    'reached_shortlist' => $shortlistedAt !== null || in_array($state, self::AFTER_SHORTLIST, true),
                ];
            });
    }

    private function publishedVacancies(int $organizationId, CarbonImmutable $from, CarbonImmutable $to, ?int $vacancyId): int
    {
        return Vacancy::query()
            ->where('organization_id', $organizationId)
            ->whereNot('status', VacancyStatus::Draft)
            ->whereBetween('published_at', [$from, $to])
            ->when($vacancyId, fn (Builder $query) => $query->whereKey($vacancyId))
            ->count();
    }

    /**
     * @param  Collection<int, ReportRow>  $rows
     * @return array<string, int|float|null>
     */
    private function indicators(Collection $rows, int $publishedVacancies): array
    {
        $applications = $rows->count();
        $vacancies = $rows->pluck('vacancy_id')->unique()->count();
        $reached = $rows->where('reached_shortlist', true)->count();

        $days = $rows
            ->filter(fn (object $row) => $row->shortlisted_at !== null)
            ->map(fn (object $row) => max(0, $row->applied_at->diffInSeconds($row->shortlisted_at)) / 86400);

        return [
            'applications' => $applications,
            'published_vacancies' => $publishedVacancies,
            'vacancies_with_applications' => $vacancies,
            'average_per_vacancy' => $vacancies > 0 ? round($applications / $vacancies, 1) : null,
            'reached_shortlist' => $reached,
            'shortlist_rate' => $this->rate($reached, $applications),
            'in_assessment' => $rows->filter(fn (object $row) => in_array($row->status, self::IN_ASSESSMENT, true))->count(),
            'average_days_to_shortlist' => $days->isEmpty() ? null : round($days->avg(), 1),
        ];
    }

    /**
     * @param  Collection<int, ReportRow>  $rows
     * @return list<array{value: string, label: string, tone: string, count: int}>
     */
    private function byStatus(Collection $rows): array
    {
        $counts = $rows->countBy(fn (object $row) => $row->status->value);

        return array_map(fn (ApplicationStatus $case) => [
            ...$case->present(),
            'count' => (int) ($counts[$case->value] ?? 0),
        ], ApplicationStatus::cases());
    }

    /**
     * Postulaciones por semana (lunes a domingo); las semanas sin registros valen cero.
     *
     * @param  Collection<int, ReportRow>  $rows
     * @return list<array{week_start: string, count: int}>
     */
    private function byWeek(Collection $rows, CarbonImmutable $from, CarbonImmutable $to): array
    {
        $counts = $rows->countBy(fn (object $row) => $row->applied_at->startOfWeek()->toDateString());
        $weeks = [];

        for ($week = $from->startOfWeek(); $week->lessThanOrEqualTo($to); $week = $week->addWeek()) {
            $key = $week->toDateString();
            $weeks[] = ['week_start' => $key, 'count' => (int) ($counts[$key] ?? 0)];
        }

        return $weeks;
    }

    /**
     * @param  Collection<int, ReportRow>  $rows
     * @return array<int, array<string, mixed>>
     */
    private function byVacancy(Collection $rows, int $organizationId): array
    {
        $groups = $rows->groupBy('vacancy_id');

        if ($groups->isEmpty()) {
            return [];
        }

        $vacancies = Vacancy::query()
            ->where('organization_id', $organizationId)
            ->whereKey($groups->keys()->all())
            ->get(['id', 'code', 'title', 'status'])
            ->keyBy('id');

        return $groups
            ->map(function (Collection $group, int $vacancyId) use ($vacancies): array {
                /** @var Vacancy $vacancy */
                $vacancy = $vacancies[$vacancyId];
                $reached = $group->where('reached_shortlist', true)->count();

                return [
                    'id' => $vacancy->id,
                    'code' => $vacancy->code,
                    'title' => $vacancy->title,
                    'status' => $vacancy->status->present(),
                    'applications' => $group->count(),
                    'reached_shortlist' => $reached,
                    'shortlist_rate' => $this->rate($reached, $group->count()),
                    'in_assessment' => $group->filter(fn (object $row) => in_array($row->status, self::IN_ASSESSMENT, true))->count(),
                ];
            })
            ->sortBy([['applications', 'desc'], ['code', 'asc']])
            ->values()
            ->all();
    }

    private function rate(int $part, int $total): ?float
    {
        return $total > 0 ? round($part * 100 / $total, 1) : null;
    }
}
