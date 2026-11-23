import { Head, router } from '@inertiajs/react';
import { ChartColumnBig, ShieldCheck } from 'lucide-react';
import { useState, type FormEvent } from 'react';
import RecruitmentReportController from '@/actions/App/Http/Controllers/Reports/RecruitmentReportController';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { FormField, NativeSelect } from '@/components/form-controls';
import { PageContainer, PageHeader, Section } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { formatDate } from '@/lib/format';
import {
    barRatio,
    formatNumber,
    formatWeek,
    plural,
    reportQuery,
} from '@/lib/reports';
import { cn } from '@/lib/utils';
import type { Presented } from '@/types';

/**
 * RF-28 (candidato): reportes operativos del proceso de reclutamiento.
 *
 * Todo lo que se ve aquí llega calculado por el servidor a partir de los
 * registros de la organización (postulaciones, historial de etapas y
 * vacantes). La página no inventa ni completa valores: si no hay datos,
 * muestra cero o «—». Son indicadores del **proceso**; no evalúan personas.
 */

type Indicators = {
    applications: number;
    published_vacancies: number;
    vacancies_with_applications: number;
    average_per_vacancy: number | null;
    reached_shortlist: number;
    shortlist_rate: number | null;
    in_assessment: number;
    average_days_to_shortlist: number | null;
};

type StatusCount = Presented & { count: number };

type WeekCount = { week_start: string; count: number };

type VacancyRow = {
    id: number;
    code: string;
    title: string;
    status: Presented;
    applications: number;
    reached_shortlist: number;
    shortlist_rate: number | null;
    in_assessment: number;
};

type Filters = {
    desde: string;
    hasta: string;
    vacante: string | null;
    estado: string | null;
};

type Props = {
    indicators: Indicators;
    by_status: StatusCount[];
    by_week: WeekCount[];
    by_vacancy: VacancyRow[];
    filters: Filters;
    vacancies: { value: string; label: string }[];
    statuses: Presented[];
    errors?: Partial<Record<keyof Filters, string>>;
};

export default function ReportsIndex({
    indicators,
    by_status,
    by_week,
    by_vacancy,
    filters,
    vacancies,
    statuses,
    errors = {},
}: Props) {
    const [form, setForm] = useState({
        desde: filters.desde,
        hasta: filters.hasta,
        vacante: filters.vacante ?? '',
        estado: filters.estado ?? '',
    });

    const apply = (event: FormEvent) => {
        event.preventDefault();

        const query = reportQuery(form);

        router.get(
            RecruitmentReportController.url({ query }),
            {},
            { preserveState: false, preserveScroll: true },
        );
    };

    const clear = () =>
        router.get(
            RecruitmentReportController.url(),
            {},
            { preserveState: false },
        );

    const period = `${formatDate(filters.desde)} – ${formatDate(filters.hasta)}`;

    return (
        <>
            <Head title="Reportes" />
            <PageContainer>
                <PageHeader
                    title="Reportes de reclutamiento"
                    description="Indicadores del proceso de su organización calculados a partir de los registros almacenados: postulaciones, historial de etapas y vacantes. Los filtros afectan a los indicadores, los gráficos y la tabla."
                />

                <form
                    onSubmit={apply}
                    className="bg-card grid gap-4 rounded-xl border p-5 sm:grid-cols-2 lg:grid-cols-[repeat(4,minmax(0,1fr))_auto] lg:items-end"
                    aria-label="Filtros del reporte"
                    data-cy="report-filters"
                >
                    <FormField
                        label="Desde"
                        htmlFor="report-desde"
                        error={errors.desde}
                    >
                        <Input
                            id="report-desde"
                            type="date"
                            value={form.desde}
                            max={form.hasta || undefined}
                            onChange={(event) =>
                                setForm({ ...form, desde: event.target.value })
                            }
                            data-cy="report-filter-desde"
                        />
                    </FormField>
                    <FormField
                        label="Hasta"
                        htmlFor="report-hasta"
                        error={errors.hasta}
                    >
                        <Input
                            id="report-hasta"
                            type="date"
                            value={form.hasta}
                            min={form.desde || undefined}
                            onChange={(event) =>
                                setForm({ ...form, hasta: event.target.value })
                            }
                            data-cy="report-filter-hasta"
                        />
                    </FormField>
                    <FormField
                        label="Vacante"
                        htmlFor="report-vacante"
                        error={errors.vacante}
                    >
                        <NativeSelect
                            id="report-vacante"
                            options={vacancies}
                            placeholder="Todas las vacantes"
                            value={form.vacante}
                            onChange={(event) =>
                                setForm({
                                    ...form,
                                    vacante: event.target.value,
                                })
                            }
                            data-cy="report-filter-vacante"
                        />
                    </FormField>
                    <FormField
                        label="Etapa actual"
                        htmlFor="report-estado"
                        error={errors.estado}
                    >
                        <NativeSelect
                            id="report-estado"
                            options={statuses}
                            placeholder="Todas las etapas"
                            value={form.estado}
                            onChange={(event) =>
                                setForm({ ...form, estado: event.target.value })
                            }
                            data-cy="report-filter-estado"
                        />
                    </FormField>
                    <div className="flex gap-2 sm:col-span-2 lg:col-span-1">
                        <Button type="submit" data-cy="report-filter-apply">
                            Aplicar
                        </Button>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={clear}
                            data-cy="report-filter-clear"
                        >
                            Limpiar
                        </Button>
                    </div>
                </form>

                <p
                    className="text-muted-foreground text-sm"
                    data-cy="report-period"
                >
                    Período consultado:{' '}
                    <span className="text-foreground font-medium">
                        {period}
                    </span>
                    {' · '}postulaciones registradas en esas fechas.
                </p>

                <dl
                    className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3"
                    data-cy="report-indicators"
                >
                    <Kpi
                        cy="kpi-applications"
                        label="Postulaciones recibidas"
                        value={formatNumber(indicators.applications)}
                        raw={indicators.applications}
                        hint={`En ${plural(indicators.vacancies_with_applications, 'vacante', 'vacantes')}.`}
                    />
                    <Kpi
                        cy="kpi-published-vacancies"
                        label="Vacantes publicadas en el período"
                        value={formatNumber(indicators.published_vacancies)}
                        raw={indicators.published_vacancies}
                        hint="Convocatorias cuya fecha de publicación cae en el período."
                    />
                    <Kpi
                        cy="kpi-average-per-vacancy"
                        label="Promedio de postulaciones por vacante"
                        value={formatNumber(indicators.average_per_vacancy)}
                        raw={indicators.average_per_vacancy}
                        hint="Sobre las vacantes que recibieron postulaciones."
                    />
                    <Kpi
                        cy="kpi-reached-shortlist"
                        label="Llegaron a la preselección"
                        value={formatNumber(indicators.reached_shortlist)}
                        raw={indicators.reached_shortlist}
                        hint={`Tasa de preselección: ${formatNumber(indicators.shortlist_rate, ' %')}.`}
                    />
                    <Kpi
                        cy="kpi-in-assessment"
                        label="En evaluación o entrevista"
                        value={formatNumber(indicators.in_assessment)}
                        raw={indicators.in_assessment}
                        hint="Postulaciones cuya etapa actual es evaluación o entrevista."
                    />
                    <Kpi
                        cy="kpi-days-to-shortlist"
                        label="Tiempo promedio hasta la preselección"
                        value={formatNumber(
                            indicators.average_days_to_shortlist,
                            ' días',
                        )}
                        raw={indicators.average_days_to_shortlist}
                        hint="Desde la postulación hasta su preselección registrada."
                    />
                </dl>

                {indicators.applications === 0 ? (
                    <EmptyState
                        icon={ChartColumnBig}
                        title="No hay postulaciones para estos filtros"
                        description="Amplíe el período o quite filtros. Los reportes se calculan sobre los registros reales de su organización; no se muestran datos de ejemplo."
                    />
                ) : (
                    <>
                        <div className="grid gap-6 lg:grid-cols-2">
                            <Section
                                title="Postulaciones por etapa actual"
                                description="Distribución del período según la etapa en que se encuentra cada postulación."
                                data-cy="chart-by-status"
                            >
                                <StatusBars rows={by_status} />
                            </Section>
                            <Section
                                title="Postulaciones por semana"
                                description="Semanas de lunes a domingo; las semanas sin registros valen cero."
                                data-cy="chart-by-week"
                            >
                                <WeekColumns weeks={by_week} />
                            </Section>
                        </div>

                        <Section
                            title="Detalle por vacante"
                            description="Vacantes ordenadas por cantidad de postulaciones en el período."
                            contentClassName="p-0 md:p-0"
                            data-cy="report-by-vacancy"
                        >
                            <VacancyTable rows={by_vacancy} />
                        </Section>
                    </>
                )}

                <aside className="bg-surface text-surface-foreground flex gap-3 rounded-xl border border-dashed px-5 py-4 text-sm leading-relaxed">
                    <ShieldCheck
                        className="text-primary mt-0.5 size-5 shrink-0"
                        aria-hidden="true"
                    />
                    <p>
                        Son indicadores agregados del{' '}
                        <strong className="font-medium">proceso</strong>: no
                        muestran nombres ni puntajes y no evalúan, ordenan ni
                        descartan personas. La decisión final de selección la
                        registra siempre una persona autorizada (RF-23).
                    </p>
                </aside>
            </PageContainer>
        </>
    );
}

function Kpi({
    label,
    value,
    raw,
    hint,
    cy,
}: {
    label: string;
    value: string;
    raw: number | null;
    hint: string;
    cy: string;
}) {
    return (
        <div
            className="bg-card flex flex-col gap-1 rounded-xl border px-5 py-4"
            data-cy={cy}
            data-value={raw ?? ''}
        >
            <dt className="text-muted-foreground text-sm">{label}</dt>
            <dd className="font-serif text-3xl leading-tight font-semibold tabular-nums">
                {value}
            </dd>
            <dd className="text-muted-foreground text-xs leading-relaxed">
                {hint}
            </dd>
        </div>
    );
}

/**
 * Barras horizontales de una sola serie: el color es uno solo (la identidad la
 * da la etiqueta, no el tono), el valor va al final de la barra y la escala
 * empieza en cero.
 */
function StatusBars({ rows }: { rows: StatusCount[] }) {
    const max = Math.max(1, ...rows.map((row) => row.count));

    return (
        <ul className="space-y-3">
            {rows.map((row) => (
                <li
                    key={row.value}
                    className="grid grid-cols-[minmax(7rem,9rem)_1fr] items-center gap-3 text-sm"
                    data-cy="chart-status-row"
                    data-status={row.value}
                    data-count={row.count}
                    title={`${row.label}: ${plural(row.count, 'postulación', 'postulaciones')}`}
                >
                    <span className="text-muted-foreground truncate">
                        {row.label}
                    </span>
                    <span className="flex items-center gap-2">
                        <span
                            className="bg-primary h-4 rounded-r-sm"
                            style={{
                                width:
                                    row.count === 0
                                        ? 0
                                        : `max(4px, ${barRatio(row.count, max) * 85}%)`,
                            }}
                            aria-hidden="true"
                        />
                        <span className="tabular-nums">
                            {formatNumber(row.count)}
                        </span>
                    </span>
                </li>
            ))}
        </ul>
    );
}

/**
 * Columnas por semana. Las columnas no llenan su franja (máx. 24 px), crecen
 * desde una línea base común y muestran el valor al pasar el cursor o al
 * enfocarlas con el teclado. Una tabla oculta repite los datos para lectores
 * de pantalla.
 */
function WeekColumns({ weeks }: { weeks: WeekCount[] }) {
    const [active, setActive] = useState<number | null>(null);
    const max = Math.max(1, ...weeks.map((week) => week.count));
    const peak = weeks.reduce(
        (best, week, index) => (week.count > weeks[best].count ? index : best),
        0,
    );
    const labelEvery = Math.max(1, Math.ceil(weeks.length / 6));
    const current = active === null ? null : weeks[active];

    return (
        <div>
            <p
                className="text-muted-foreground mb-3 h-5 text-sm tabular-nums"
                aria-live="polite"
            >
                {current
                    ? `Semana del ${formatWeek(current.week_start)}: ${plural(current.count, 'postulación', 'postulaciones')}`
                    : `Máximo semanal: ${plural(weeks[peak]?.count ?? 0, 'postulación', 'postulaciones')}`}
            </p>
            <div
                className="border-border flex h-40 items-end gap-0.5 border-b"
                onMouseLeave={() => setActive(null)}
                aria-hidden="true"
            >
                {weeks.map((week, index) => (
                    <div
                        key={week.week_start}
                        className="flex h-full min-w-0 flex-1 cursor-default items-end justify-center"
                        onMouseEnter={() => setActive(index)}
                        data-cy="chart-week-column"
                        data-week={week.week_start}
                        data-count={week.count}
                    >
                        <div
                            className={cn(
                                'bg-primary w-full max-w-6 rounded-t-sm transition-opacity',
                                active !== null &&
                                    active !== index &&
                                    'opacity-40',
                            )}
                            style={{
                                height:
                                    week.count === 0
                                        ? 0
                                        : `max(4px, ${barRatio(week.count, max) * 100}%)`,
                            }}
                        />
                    </div>
                ))}
            </div>
            <div
                className="text-muted-foreground mt-2 flex gap-0.5 text-xs"
                aria-hidden="true"
            >
                {weeks.map((week, index) => (
                    <span
                        key={week.week_start}
                        className="min-w-0 flex-1 text-center whitespace-nowrap"
                    >
                        {index % labelEvery === 0
                            ? formatWeek(week.week_start)
                            : ''}
                    </span>
                ))}
            </div>
            <table className="sr-only">
                <caption>Postulaciones por semana</caption>
                <thead>
                    <tr>
                        <th scope="col">Semana que inicia</th>
                        <th scope="col">Postulaciones</th>
                    </tr>
                </thead>
                <tbody>
                    {weeks.map((week) => (
                        <tr key={week.week_start}>
                            <td>{formatDate(week.week_start)}</td>
                            <td>{week.count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function VacancyTable({ rows }: { rows: VacancyRow[] }) {
    const max = Math.max(1, ...rows.map((row) => row.applications));

    return (
        <DataTable
            caption="Postulaciones e indicadores por vacante en el período"
            className="rounded-none md:border-0"
            data-cy="report-vacancy-table"
            rows={rows}
            rowKey={(row) => row.id}
            rowAttributes={(row) => ({
                'data-cy': 'report-vacancy-row',
                'data-code': row.code,
            })}
            columns={[
                {
                    key: 'vacancy',
                    header: 'Vacante',
                    cell: (row) => (
                        <span className="block min-w-0">
                            <span className="block font-medium">
                                {row.title}
                            </span>
                            <span className="text-muted-foreground font-mono text-xs">
                                {row.code}
                            </span>
                        </span>
                    ),
                },
                {
                    key: 'status',
                    header: 'Estado',
                    cell: (row) => <StatusBadge status={row.status} />,
                },
                {
                    key: 'applications',
                    header: 'Postulaciones',
                    cell: (row) => (
                        <span className="flex items-center gap-2">
                            <span
                                className="bg-primary h-3 rounded-r-sm"
                                style={{
                                    width: `${Math.max(4, barRatio(row.applications, max) * 96)}px`,
                                }}
                                aria-hidden="true"
                            />
                            <span
                                className="tabular-nums"
                                data-cy="report-vacancy-applications"
                            >
                                {formatNumber(row.applications)}
                            </span>
                        </span>
                    ),
                },
                {
                    key: 'shortlist',
                    header: 'Preseleccionadas',
                    align: 'end',
                    cell: (row) => (
                        <span className="tabular-nums">
                            {formatNumber(row.reached_shortlist)}
                        </span>
                    ),
                },
                {
                    key: 'rate',
                    header: 'Tasa de preselección',
                    align: 'end',
                    cell: (row) => (
                        <span className="tabular-nums">
                            {formatNumber(row.shortlist_rate, ' %')}
                        </span>
                    ),
                },
                {
                    key: 'assessment',
                    header: 'En evaluación o entrevista',
                    align: 'end',
                    cell: (row) => (
                        <span className="tabular-nums">
                            {formatNumber(row.in_assessment)}
                        </span>
                    ),
                },
            ]}
        />
    );
}

ReportsIndex.layout = {
    breadcrumbs: [{ title: 'Reportes', href: RecruitmentReportController() }],
};
