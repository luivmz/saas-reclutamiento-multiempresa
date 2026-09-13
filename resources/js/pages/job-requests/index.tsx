import { Head, Link, router } from '@inertiajs/react';
import { ClipboardList, FilePlus2 } from 'lucide-react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import { EmptyState } from '@/components/empty-state';
import { FilterChips } from '@/components/filter-chips';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
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
                    description="Registro, validación, aprobación y trazabilidad de requerimientos (RF-01 a RF-04)."
                    actions={
                        can.create && (
                            <Button asChild data-cy="new-job-request">
                                <Link href={JobRequestController.create()}>
                                    <FilePlus2 />
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
                        description="Cuando existan requerimientos en este estado aparecerán aquí."
                    />
                ) : (
                    <Card className="gap-0 overflow-hidden py-0">
                        <div className="overflow-x-auto">
                            <table
                                className="w-full text-sm"
                                data-cy="job-requests-table"
                            >
                                <thead className="bg-muted/50 text-muted-foreground text-left text-xs tracking-wide uppercase">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Código</th>
                                        <th className="px-4 py-3 font-medium">Puesto</th>
                                        <th className="px-4 py-3 font-medium">Área</th>
                                        <th className="px-4 py-3 text-center font-medium">Plazas</th>
                                        <th className="px-4 py-3 font-medium">Solicitante</th>
                                        <th className="px-4 py-3 font-medium">Estado</th>
                                        <th className="px-4 py-3 font-medium">Registrado</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {jobRequests.data.map((jobRequest) => (
                                        <tr
                                            key={jobRequest.id}
                                            className="hover:bg-muted/40"
                                            data-cy="job-request-row"
                                            data-code={jobRequest.code}
                                        >
                                            <td className="px-4 py-3 font-mono text-xs">
                                                <Link
                                                    href={JobRequestController.show(jobRequest.id)}
                                                    className="font-medium hover:underline"
                                                    data-cy="job-request-link"
                                                >
                                                    {jobRequest.code}
                                                </Link>
                                            </td>
                                            <td className="px-4 py-3 font-medium">
                                                {jobRequest.position_title}
                                            </td>
                                            <td className="text-muted-foreground px-4 py-3">
                                                {jobRequest.area}
                                            </td>
                                            <td className="px-4 py-3 text-center">
                                                {jobRequest.headcount}
                                            </td>
                                            <td className="text-muted-foreground px-4 py-3">
                                                {jobRequest.requester?.name}
                                            </td>
                                            <td className="px-4 py-3">
                                                <StatusBadge status={jobRequest.status} />
                                            </td>
                                            <td className="text-muted-foreground px-4 py-3 whitespace-nowrap">
                                                {formatDate(jobRequest.created_at)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </Card>
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
