import { Form, Head, Link } from '@inertiajs/react';
import { CalendarClock, MapPin, Search, Users } from 'lucide-react';
import { useRef } from 'react';
import { EmptyState } from '@/components/empty-state';
import { JobHost } from '@/components/job-host/job-host';
import { Pagination } from '@/components/pagination';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { formatDate } from '@/lib/format';
import { index as jobsIndex, show as jobsShow } from '@/routes/jobs';
import type { Paginated, Vacancy } from '@/types';

type Props = {
    vacancies: Paginated<Vacancy>;
    filters: { q: string };
};

export default function JobsIndex({ vacancies, filters }: Props) {
    const listRef = useRef<HTMLDivElement>(null);

    return (
        <>
            <Head title="Empleos disponibles" />

            <section className="border-b">
                <div className="mx-auto max-w-6xl space-y-5 px-4 py-8 sm:px-6 sm:py-12">
                    <h1
                        className="font-serif text-3xl font-semibold tracking-tight md:text-4xl"
                        data-cy="page-title"
                    >
                        Empleos disponibles
                    </h1>
                    <p className="text-muted-foreground max-w-2xl leading-relaxed">
                        Convocatorias vigentes publicadas por las organizaciones
                        de la plataforma. Para postular necesita una cuenta de
                        postulante con perfil y CV.
                    </p>
                    <Form
                        {...jobsIndex.form()}
                        className="grid max-w-xl gap-2 min-[360px]:grid-cols-[minmax(0,1fr)_auto]"
                        role="search"
                    >
                        <Input
                            name="q"
                            defaultValue={filters.q}
                            placeholder="Buscar por puesto…"
                            aria-label="Buscar por puesto"
                            className="max-sm:h-11"
                            data-cy="jobs-search"
                        />
                        <Button
                            type="submit"
                            variant="secondary"
                            className="max-[359px]:justify-self-start max-sm:h-11"
                        >
                            <Search aria-hidden="true" />
                            Buscar
                        </Button>
                    </Form>
                </div>
            </section>

            {/* Desde 1280 px, una columna propia para el anfitrión decorativo: no
                tapa ofertas, búsqueda, paginación ni pie. La columna solo existe
                cuando el anfitrión tiene una presentación visible. */}
            <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 xl:grid-cols-[minmax(0,1fr)_8.5rem] xl:gap-8 xl:has-[[data-cy=job-host]]:grid">
                <div ref={listRef} className="min-w-0 space-y-6">
                    {vacancies.data.length === 0 ? (
                        <EmptyState
                            title="No hay convocatorias vigentes"
                            description={
                                filters.q
                                    ? 'Ninguna convocatoria abierta coincide con esa búsqueda. Pruebe con otro puesto.'
                                    : 'Cuando una organización publique una vacante, aparecerá aquí.'
                            }
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
                                        <h2 className="font-serif text-lg leading-snug font-semibold">
                                            <Link
                                                href={jobsShow(vacancy.id)}
                                                className="after:absolute after:inset-0 hover:underline"
                                                data-cy="job-detail-link"
                                            >
                                                {vacancy.title}
                                            </Link>
                                        </h2>
                                        <p className="text-muted-foreground line-clamp-3 text-sm leading-relaxed">
                                            {vacancy.summary}
                                        </p>
                                    </div>
                                    <dl className="text-muted-foreground space-y-2 border-t px-5 py-4 text-sm [overflow-wrap:anywhere]">
                                        <div className="flex items-center gap-2">
                                            <MapPin
                                                className="size-4 shrink-0"
                                                aria-hidden="true"
                                            />
                                            <dt className="sr-only">
                                                Ubicación
                                            </dt>
                                            <dd>
                                                {vacancy.location},{' '}
                                                {vacancy.contract_type.label}
                                            </dd>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Users
                                                className="size-4 shrink-0"
                                                aria-hidden="true"
                                            />
                                            <dt className="sr-only">Plazas</dt>
                                            <dd>
                                                {vacancy.positions} plaza
                                                {vacancy.positions === 1
                                                    ? ''
                                                    : 's'}
                                            </dd>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <CalendarClock
                                                className="size-4 shrink-0"
                                                aria-hidden="true"
                                            />
                                            <dt className="sr-only">
                                                Cierre de postulaciones
                                            </dt>
                                            <dd>
                                                Postule hasta el{' '}
                                                {formatDate(vacancy.closes_at)}
                                            </dd>
                                        </div>
                                    </dl>
                                </li>
                            ))}
                        </ul>
                    )}
                    <Pagination meta={vacancies.meta} />
                </div>
                {vacancies.data.length > 0 && (
                    <div className="hidden xl:has-[[data-cy=job-host]]:block">
                        <div className="job-host-sticky">
                            <JobHost listRef={listRef} />
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
