import { Head, Link, router } from '@inertiajs/react';
import { Users } from 'lucide-react';
import ApplicationController from '@/actions/App/Http/Controllers/Applications/ApplicationController';
import VacancyApplicationController from '@/actions/App/Http/Controllers/Applications/VacancyApplicationController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { FilterChips } from '@/components/filter-chips';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { formatDate } from '@/lib/format';
import type { JobApplication, Paginated, Presented, Vacancy } from '@/types';

type Props = {
    vacancy: Vacancy;
    applications: Paginated<JobApplication>;
    statuses: (Presented & { count: number })[];
    filters: { estado: string | null };
};

export default function VacancyApplications({
    vacancy,
    applications,
    statuses,
    filters,
}: Props) {
    const filter = (estado: string | null) =>
        router.get(
            VacancyApplicationController.url(vacancy.id, {
                query: estado ? { estado } : {},
            }),
            {},
            { preserveState: true, replace: true },
        );

    return (
        <>
            <Head title={`Postulaciones de ${vacancy.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono text-xs">
                                {vacancy.code}
                            </span>
                            <StatusBadge status={vacancy.status} />
                        </>
                    }
                    title={`Postulaciones: ${vacancy.title}`}
                    description="Consulte y revise las postulaciones recibidas (RF-12)."
                    actions={
                        <Button variant="outline" asChild>
                            <Link href={VacancyController.show(vacancy.id)}>
                                Ver vacante
                            </Link>
                        </Button>
                    }
                />

                <FilterChips
                    options={statuses
                        .filter((status) => status.count > 0)
                        .map((status) => ({
                            value: status.value,
                            label: `${status.label} (${status.count})`,
                        }))}
                    value={filters.estado}
                    onChange={filter}
                    allLabel="Todas"
                    label="Filtrar por etapa"
                />

                {applications.data.length === 0 ? (
                    <EmptyState
                        icon={Users}
                        title="No hay postulaciones para mostrar"
                        description={
                            filters.estado
                                ? 'Ninguna postulación está en esa etapa. Quite el filtro para verlas todas.'
                                : 'Aparecerán aquí en cuanto alguien postule a la convocatoria.'
                        }
                    />
                ) : (
                    <DataTable
                        caption={`Postulaciones recibidas en la vacante ${vacancy.code}`}
                        data-cy="applications-table"
                        rows={applications.data}
                        rowKey={(row) => row.id}
                        rowAttributes={(row) => ({
                            'data-cy': 'application-row',
                            'data-candidate': row.candidate?.email,
                        })}
                        columns={[
                            {
                                key: 'code',
                                header: 'Código',
                                className: 'font-mono text-xs',
                                cell: (row) => row.code,
                            },
                            {
                                key: 'candidate',
                                header: 'Candidato',
                                cell: (row) => (
                                    <>
                                        <span className="block font-medium">
                                            {row.candidate?.name}
                                        </span>
                                        <span className="text-muted-foreground block text-xs">
                                            {row.candidate?.profile
                                                ?.professional_title ?? '—'}
                                        </span>
                                    </>
                                ),
                            },
                            {
                                key: 'experience',
                                header: 'Experiencia',
                                align: 'center',
                                cell: (row) =>
                                    row.candidate?.profile
                                        ?.years_of_experience !== undefined &&
                                    row.candidate?.profile
                                        ?.years_of_experience !== null
                                        ? `${row.candidate.profile.years_of_experience} años`
                                        : '—',
                            },
                            {
                                key: 'city',
                                header: 'Ciudad',
                                className: 'text-muted-foreground',
                                cell: (row) =>
                                    row.candidate?.profile?.city ?? '—',
                            },
                            {
                                key: 'applied',
                                header: 'Postuló',
                                className:
                                    'text-muted-foreground whitespace-nowrap',
                                cell: (row) => formatDate(row.applied_at),
                            },
                            {
                                key: 'status',
                                header: 'Etapa',
                                cell: (row) => (
                                    <StatusBadge status={row.status} />
                                ),
                            },
                            {
                                key: 'actions',
                                header: (
                                    <span className="sr-only">Expediente</span>
                                ),
                                label: '',
                                align: 'end',
                                cell: (row) => (
                                    <Button variant="outline" size="sm" asChild>
                                        <Link
                                            href={ApplicationController(row.id)}
                                            data-cy="application-link"
                                        >
                                            Ver expediente
                                        </Link>
                                    </Button>
                                ),
                            },
                        ]}
                    />
                )}

                <Pagination meta={applications.meta} />
            </PageContainer>
        </>
    );
}

VacancyApplications.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Postulaciones', href: VacancyController.index() },
    ],
};
