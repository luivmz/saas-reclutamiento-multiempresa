import { Head, Link, router } from '@inertiajs/react';
import { Briefcase, Plus } from 'lucide-react';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { FilterChips } from '@/components/filter-chips';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { formatDate } from '@/lib/format';
import type { Paginated, Presented, Vacancy } from '@/types';

type Props = {
    vacancies: Paginated<Vacancy>;
    filters: { estado: string | null };
    statuses: Presented[];
    can: { create: boolean };
};

export default function VacanciesIndex({
    vacancies,
    filters,
    statuses,
    can,
}: Props) {
    const filter = (estado: string | null) =>
        router.get(
            VacancyController.index.url({ query: estado ? { estado } : {} }),
            {},
            { preserveState: true, replace: true },
        );

    return (
        <>
            <Head title="Vacantes" />
            <PageContainer>
                <PageHeader
                    title="Vacantes"
                    description="Perfil, criterios, validación, publicación y cierre de las convocatorias (RF-05 a RF-15)."
                    actions={
                        can.create && (
                            <Button asChild data-cy="new-vacancy">
                                <Link href={VacancyController.create()}>
                                    <Plus aria-hidden="true" />
                                    Nueva vacante
                                </Link>
                            </Button>
                        )
                    }
                />

                <FilterChips
                    options={statuses}
                    value={filters.estado}
                    onChange={filter}
                    allLabel="Todas"
                />

                {vacancies.data.length === 0 ? (
                    <EmptyState
                        icon={Briefcase}
                        title="No hay vacantes para mostrar"
                        description={
                            filters.estado
                                ? 'Ninguna vacante está en ese estado. Quite el filtro para verlas todas.'
                                : 'Genere una vacante a partir de un requerimiento aprobado.'
                        }
                    />
                ) : (
                    <DataTable
                        caption="Vacantes de su organización"
                        data-cy="vacancies-table"
                        rows={vacancies.data}
                        rowKey={(row) => row.id}
                        rowAttributes={(row) => ({
                            'data-cy': 'vacancy-row',
                            'data-code': row.code,
                        })}
                        columns={[
                            {
                                key: 'code',
                                header: 'Código',
                                className: 'font-mono text-xs',
                                cell: (row) => (
                                    <Link
                                        href={VacancyController.show(row.id)}
                                        className="font-medium hover:underline"
                                        data-cy="vacancy-link"
                                    >
                                        {row.code}
                                    </Link>
                                ),
                            },
                            {
                                key: 'title',
                                header: 'Vacante',
                                className: 'font-medium',
                                cell: (row) => row.title,
                            },
                            {
                                key: 'job-request',
                                header: 'Requerimiento',
                                className:
                                    'text-muted-foreground font-mono text-xs',
                                cell: (row) => row.job_request?.code ?? '—',
                            },
                            {
                                key: 'positions',
                                header: 'Plazas',
                                align: 'center',
                                cell: (row) => row.positions,
                            },
                            {
                                key: 'closes',
                                header: 'Cierre',
                                className:
                                    'text-muted-foreground whitespace-nowrap',
                                cell: (row) => formatDate(row.closes_at),
                            },
                            {
                                key: 'status',
                                header: 'Estado',
                                cell: (row) => (
                                    <StatusBadge status={row.status} />
                                ),
                            },
                        ]}
                    />
                )}

                <Pagination meta={vacancies.meta} />
            </PageContainer>
        </>
    );
}

VacanciesIndex.layout = {
    breadcrumbs: [{ title: 'Vacantes', href: VacancyController.index() }],
};
