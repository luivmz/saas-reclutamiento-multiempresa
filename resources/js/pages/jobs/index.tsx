import { Head, Link } from '@inertiajs/react';
import { ArrowRight } from 'lucide-react';
import { useRef, useState } from 'react';
import { JobHost } from '@/components/job-host/job-host';
import { JobsEmptyState } from '@/components/jobs/jobs-empty-state';
import { JobsFilters } from '@/components/jobs/jobs-filters';
import { Pagination } from '@/components/pagination';
import { DeadlinePassedBadge } from '@/components/vacancies/deadline-passed-badge';
import { formatDate } from '@/lib/format';
import {
    activeFilterCount,
    criteriaQuery,
    vacancyCount,
} from '@/lib/job-filters';
import { show as jobsShow } from '@/routes/jobs';
import type {
    JobCriteria,
    JobFilterOptions,
    Paginated,
    Vacancy,
} from '@/types';

type Props = {
    vacancies: Paginated<Vacancy>;
    filters: JobCriteria;
    options: JobFilterOptions;
    errors: Partial<Record<keyof JobCriteria | 'page', string>>;
};

export default function JobsIndex({
    vacancies,
    filters,
    options,
    errors,
}: Props) {
    const listRef = useRef<HTMLDivElement>(null);

    const [loading, setLoading] = useState(false);
    const messages = Object.values(errors);

    return (
        <>
            <Head title="Convocatorias" />

            <section className="border-b">
                <div className="mx-auto max-w-6xl space-y-5 px-4 py-8 sm:px-6 sm:py-12">
                    <h1
                        className="font-serif text-3xl font-semibold tracking-tight md:text-4xl"
                        data-cy="page-title"
                    >
                        Convocatorias
                    </h1>
                    <p className="text-muted-foreground max-w-2xl leading-relaxed">
                        Ofertas de empleo publicadas por las organizaciones de
                        la plataforma. Para postular necesita una cuenta con
                        perfil de postulante y CV.
                    </p>
                    {messages.length > 0 && (
                        <div
                            role="alert"
                            className="rounded-lg border border-amber-500 px-4 py-3 text-sm"
                            data-cy="jobs-validation"
                        >
                            <p className="font-medium">
                                Se muestran todas las convocatorias.
                            </p>
                            <ul>
                                {messages.map((message) => (
                                    <li key={message}>{message}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    <JobsFilters
                        criteria={filters}
                        options={options}
                        processing={loading}
                        onLoadingChange={setLoading}
                    />
                </div>
            </section>

            {/* Desde 1280 px, una columna propia para el anfitrión decorativo: no
                tapa ofertas, búsqueda, paginación ni pie. La columna solo existe
                cuando el anfitrión tiene una presentación visible. */}
            <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 xl:grid-cols-[minmax(0,1fr)_8.5rem] xl:gap-8 xl:has-[[data-cy=job-host]]:grid">
                <div
                    ref={listRef}
                    className="min-w-0 space-y-6 [overflow-wrap:anywhere]"
                >
                    <p
                        role="status"
                        aria-atomic="true"
                        className="text-sm font-medium"
                        data-cy="jobs-result-count"
                    >
                        {loading
                            ? 'Buscando convocatorias…'
                            : vacancyCount(vacancies.meta.total)}
                    </p>
                    {vacancies.data.length === 0 ? (
                        <JobsEmptyState
                            query={
                                options.organizaciones.length ? filters.q : ''
                            }
                            filterCount={activeFilterCount(filters)}
                            criteria={criteriaQuery(filters)}
                            total={vacancies.meta.total}
                        />
                    ) : (
                        <ul
                            className="grid gap-4 md:grid-cols-2 lg:grid-cols-3"
                            data-cy="jobs-list"
                        >
                            {vacancies.data.map((vacancy) => (
                                <li
                                    key={vacancy.id}
                                    className="bg-card hover:border-primary/50 focus-within:border-primary/50 relative flex flex-col rounded-xl border transition-colors"
                                    data-cy="job-card"
                                    data-code={vacancy.code}
                                >
                                    <div className="flex-1 space-y-3 p-5 [overflow-wrap:anywhere]">
                                        <p className="text-muted-foreground text-xs">
                                            {vacancy.organization?.name}
                                        </p>
                                        {vacancy.application_deadline_passed && (
                                            <DeadlinePassedBadge />
                                        )}
                                        <h2 className="font-serif text-lg leading-snug font-semibold">
                                            <Link
                                                href={jobsShow(vacancy.id)}
                                                className="focus-visible:after:ring-ring after:absolute after:inset-0 after:rounded-xl hover:underline focus-visible:after:ring-2"
                                                data-cy="job-detail-link"
                                            >
                                                {vacancy.title}
                                            </Link>
                                        </h2>
                                        <p className="text-muted-foreground line-clamp-2 text-sm leading-relaxed">
                                            {vacancy.summary}
                                        </p>
                                    </div>
                                    <dl className="grid grid-cols-2 gap-x-3 gap-y-3 border-t px-5 py-4 text-sm [overflow-wrap:anywhere]">
                                        <div>
                                            <dt className="text-muted-foreground text-xs">
                                                Ubicación
                                            </dt>
                                            <dd>{vacancy.location}</dd>
                                        </div>
                                        <div>
                                            <dt className="text-muted-foreground text-xs">
                                                Tipo de contrato
                                            </dt>
                                            <dd>
                                                {vacancy.contract_type.label}
                                            </dd>
                                        </div>
                                        <div>
                                            <dt className="text-muted-foreground text-xs">
                                                Plazas
                                            </dt>
                                            <dd>{vacancy.positions}</dd>
                                        </div>
                                        <div>
                                            <dt className="text-muted-foreground text-xs">
                                                Cierre de postulaciones
                                            </dt>
                                            <dd>
                                                {formatDate(vacancy.closes_at)}
                                            </dd>
                                        </div>
                                    </dl>
                                    <span
                                        aria-hidden="true"
                                        className="text-primary flex items-center gap-2 px-5 pb-4 text-sm font-medium"
                                    >
                                        Ver detalle{' '}
                                        <ArrowRight className="size-4" />
                                    </span>
                                </li>
                            ))}
                        </ul>
                    )}
                    {vacancies.data.length > 0 && (
                        <Pagination meta={vacancies.meta} />
                    )}
                </div>
                {vacancies.data.length > 0 && (
                    <div className="hidden xl:has-[[data-cy=job-host]]:block">
                        <div className="job-host-sticky">
                            <JobHost
                                key={JSON.stringify(filters)}
                                listRef={listRef}
                            />
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
