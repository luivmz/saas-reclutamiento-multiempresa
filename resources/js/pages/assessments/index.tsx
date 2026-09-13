import { Head, Link } from '@inertiajs/react';
import { CalendarClock, ClipboardCheck } from 'lucide-react';
import AssessmentAssignmentController from '@/actions/App/Http/Controllers/Assessments/AssessmentAssignmentController';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
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
                    description="Sesiones asignadas a usted. Registre los puntajes y observaciones de cada una (RF-19)."
                />
                {assignments.length === 0 ? (
                    <EmptyState
                        icon={ClipboardCheck}
                        title="No tiene sesiones asignadas"
                        description="RR. HH. le asignará evaluaciones y entrevistas cuando programe el proceso."
                    />
                ) : (
                    <Card className="gap-0 overflow-hidden py-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm" data-cy="assignments-table">
                                <thead className="bg-muted/50 text-muted-foreground text-left text-xs tracking-wide uppercase">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Sesión</th>
                                        <th className="px-4 py-3 font-medium">Candidato</th>
                                        <th className="px-4 py-3 font-medium">Vacante</th>
                                        <th className="px-4 py-3 font-medium">Fecha</th>
                                        <th className="px-4 py-3 font-medium">Estado</th>
                                        <th className="px-4 py-3" />
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {assignments.map((assignment) => (
                                        <tr key={assignment.key} className="hover:bg-muted/40" data-cy="assignment-row" data-kind={assignment.kind.value} data-status={assignment.status.value}>
                                            <td className="px-4 py-3">
                                                <p className="font-medium">{assignment.title}</p>
                                                <StatusBadge status={assignment.kind} className="mt-1" />
                                            </td>
                                            <td className="px-4 py-3 font-medium">{assignment.candidate}</td>
                                            <td className="text-muted-foreground px-4 py-3">{assignment.vacancy}</td>
                                            <td className="px-4 py-3 whitespace-nowrap">
                                                <span className="flex items-center gap-1.5">
                                                    <CalendarClock className="text-muted-foreground size-4" />
                                                    {formatDateTime(assignment.scheduled_at)}
                                                </span>
                                                <span className="text-muted-foreground text-xs">
                                                    {assignment.modality} · {assignment.location}
                                                </span>
                                            </td>
                                            <td className="px-4 py-3">
                                                <StatusBadge status={assignment.status} />
                                            </td>
                                            <td className="px-4 py-3 text-right">
                                                <Button variant="outline" size="sm" asChild>
                                                    <Link href={assignment.url} data-cy="open-assignment">
                                                        {assignment.status.value === 'programada' ? 'Registrar resultados' : 'Ver resultados'}
                                                    </Link>
                                                </Button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                )}
            </PageContainer>
        </>
    );
}

AssessmentAssignments.layout = {
    breadcrumbs: [{ title: 'Mis evaluaciones', href: AssessmentAssignmentController() }],
};
