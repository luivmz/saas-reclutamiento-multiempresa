import { Head, Link } from '@inertiajs/react';
import { ClipboardCheck } from 'lucide-react';
import AssessmentAssignmentController from '@/actions/App/Http/Controllers/Assessments/AssessmentAssignmentController';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { formatDateTime } from '@/lib/format';
import type { AssessmentAssignment } from '@/types';

export default function AssessmentAssignments({
    assignments,
}: {
    assignments: AssessmentAssignment[];
}) {
    return (
        <>
            <Head title="Mis evaluaciones" />
            <PageContainer>
                <PageHeader
                    title="Mis evaluaciones y entrevistas"
                    description="Sesiones asignadas a usted. Registre los puntajes y las observaciones de cada una (RF-19)."
                />
                {assignments.length === 0 ? (
                    <EmptyState
                        icon={ClipboardCheck}
                        title="No tiene sesiones asignadas"
                        description="RR. HH. le asignará evaluaciones y entrevistas cuando programe el proceso."
                    />
                ) : (
                    <DataTable
                        caption="Evaluaciones y entrevistas asignadas a usted"
                        data-cy="assignments-table"
                        rows={assignments}
                        rowKey={(row) => row.key}
                        rowAttributes={(row) => ({
                            'data-cy': 'assignment-row',
                            'data-kind': row.kind.value,
                            'data-status': row.status.value,
                        })}
                        columns={[
                            {
                                key: 'session',
                                header: 'Sesión',
                                cell: (row) => (
                                    <>
                                        <span className="block font-medium">
                                            {row.title}
                                        </span>
                                        <StatusBadge
                                            status={row.kind}
                                            className="mt-1.5 flex w-fit"
                                        />
                                    </>
                                ),
                            },
                            {
                                key: 'candidate',
                                header: 'Candidato',
                                className: 'font-medium',
                                cell: (row) => row.candidate,
                            },
                            {
                                key: 'vacancy',
                                header: 'Vacante',
                                className: 'text-muted-foreground',
                                cell: (row) => row.vacancy,
                            },
                            {
                                key: 'schedule',
                                header: 'Fecha',
                                className: 'md:whitespace-nowrap',
                                cell: (row) => (
                                    <>
                                        <span className="block">
                                            {formatDateTime(row.scheduled_at)}
                                        </span>
                                        <span className="text-muted-foreground block text-xs">
                                            {row.modality}, {row.location}
                                        </span>
                                    </>
                                ),
                            },
                            {
                                key: 'status',
                                header: 'Estado',
                                cell: (row) => (
                                    <StatusBadge status={row.status} />
                                ),
                            },
                            {
                                key: 'actions',
                                header: <span className="sr-only">Abrir</span>,
                                label: '',
                                align: 'end',
                                cell: (row) => (
                                    <Button variant="outline" size="sm" asChild>
                                        <Link
                                            href={row.url}
                                            data-cy="open-assignment"
                                        >
                                            {row.status.value === 'programada'
                                                ? 'Registrar resultados'
                                                : 'Ver resultados'}
                                        </Link>
                                    </Button>
                                ),
                            },
                        ]}
                    />
                )}
            </PageContainer>
        </>
    );
}

AssessmentAssignments.layout = {
    breadcrumbs: [
        { title: 'Mis evaluaciones', href: AssessmentAssignmentController() },
    ],
};
