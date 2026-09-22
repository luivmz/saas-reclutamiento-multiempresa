import { Head, Link, router } from '@inertiajs/react';
import { ClipboardList, FilePlus2 } from 'lucide-react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { FilterChips } from '@/components/filter-chips';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { formatDate } from '@/lib/format';
import type { JobRequest, Paginated, Presented } from '@/types';

type Props = {
    jobRequests: Paginated<JobRequest>;
    filters: { estado: string | null };
    statuses: Presented[];
    can: { create: boolean };
};

export default function JobRequestsIndex({
    jobRequests,
    filters,
    statuses,
    can,
}: Props) {
    const filter = (estado: string | null) =>
        router.get(
            JobRequestController.index.url({
                query: estado ? { estado } : {},
            }),
            {},
            { preserveState: true, replace: true },
        );

    return (
        <>
            <Head title="Requerimientos de personal" />
            <PageContainer>
                <PageHeader
                    title="Requerimientos de personal"
                    description="Registro, validación, aprobación y trazabilidad de las necesidades de personal (RF-01 a RF-04)."
                    actions={
                        can.create && (
                            <Button asChild data-cy="new-job-request">
                                <Link href={JobRequestController.create()}>
                                    <FilePlus2 aria-hidden="true" />
                                    Nuevo requerimiento
                                </Link>
                            </Button>
                        )
                    }
                />

                <FilterChips
                    options={statuses}
                    value={filters.estado}
                    onChange={filter}
                />

                {jobRequests.data.length === 0 ? (
                    <EmptyState
                        icon={ClipboardList}
                        title="No hay requerimientos para mostrar"
                        description={
                            filters.estado
                                ? 'Ningún requerimiento está en ese estado. Quite el filtro para ver todos.'
                                : 'Cuando un área registre una necesidad de personal, aparecerá aquí.'
                        }
                    />
                ) : (
                    <DataTable
                        caption="Requerimientos de personal de su organización"
                        data-cy="job-requests-table"
                        rows={jobRequests.data}
                        rowKey={(row) => row.id}
                        rowAttributes={(row) => ({
                            'data-cy': 'job-request-row',
                            'data-code': row.code,
                        })}
                        columns={[
                            {
                                key: 'code',
                                header: 'Código',
                                className: 'font-mono text-xs',
                                cell: (row) => (
                                    <Link
                                        href={JobRequestController.show(row.id)}
                                        className="font-medium hover:underline"
                                        data-cy="job-request-link"
                                    >
                                        {row.code}
                                    </Link>
                                ),
                            },
                            {
                                key: 'position',
                                header: 'Puesto',
                                className: 'font-medium',
                                cell: (row) => row.position_title,
                            },
                            {
                                key: 'area',
                                header: 'Área',
                                className: 'text-muted-foreground',
                                cell: (row) => row.area,
                            },
                            {
                                key: 'headcount',
                                header: 'Plazas',
                                align: 'center',
                                cell: (row) => row.headcount,
                            },
                            {
                                key: 'requester',
                                header: 'Solicitante',
                                className: 'text-muted-foreground',
                                cell: (row) => row.requester?.name ?? '—',
                            },
                            {
                                key: 'status',
                                header: 'Estado',
                                cell: (row) => (
                                    <StatusBadge status={row.status} />
                                ),
                            },
                            {
                                key: 'created',
                                header: 'Registrado',
                                className:
                                    'text-muted-foreground whitespace-nowrap',
                                cell: (row) => formatDate(row.created_at),
                            },
                        ]}
                    />
                )}

                <Pagination meta={jobRequests.meta} />
            </PageContainer>
        </>
    );
}

JobRequestsIndex.layout = {
    breadcrumbs: [
        { title: 'Requerimientos', href: JobRequestController.index() },
    ],
};
