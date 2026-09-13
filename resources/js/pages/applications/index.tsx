import { Head, Link, router } from '@inertiajs/react';
import { Users } from 'lucide-react';
import ApplicationController from '@/actions/App/Http/Controllers/Applications/ApplicationController';
import VacancyApplicationController from '@/actions/App/Http/Controllers/Applications/VacancyApplicationController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { EmptyState } from '@/components/empty-state';
import { FilterChips } from '@/components/filter-chips';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
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
            <Head title={`Postulaciones · ${vacancy.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono">{vacancy.code}</span>
                            <StatusBadge status={vacancy.status} />
                        </>
                    }
                    title={`Postulaciones: ${vacancy.title}`}
                    description="RF-12 · Consulte y revise las postulaciones recibidas."
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
                />

                {applications.data.length === 0 ? (
                    <EmptyState
                        icon={Users}
                        title="No hay postulaciones para mostrar"
                        description="Las postulaciones aparecerán aquí cuando los candidatos postulen a la vacante."
                    />
                ) : (
                    <Card className="gap-0 overflow-hidden py-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm" data-cy="applications-table">
                                <thead className="bg-muted/50 text-muted-foreground text-left text-xs tracking-wide uppercase">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Código</th>
                                        <th className="px-4 py-3 font-medium">Candidato</th>
                                        <th className="px-4 py-3 text-center font-medium">Experiencia</th>
                                        <th className="px-4 py-3 font-medium">Ciudad</th>
                                        <th className="px-4 py-3 font-medium">Postuló</th>
                                        <th className="px-4 py-3 font-medium">Etapa</th>
                                        <th className="px-4 py-3" />
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {applications.data.map((application) => (
                                        <tr
                                            key={application.id}
                                            className="hover:bg-muted/40"
                                            data-cy="application-row"
                                            data-candidate={application.candidate?.email}
                                        >
                                            <td className="px-4 py-3 font-mono text-xs">{application.code}</td>
                                            <td className="px-4 py-3">
                                                <p className="font-medium">{application.candidate?.name}</p>
                                                <p className="text-muted-foreground text-xs">
                                                    {application.candidate?.profile?.professional_title ?? '—'}
                                                </p>
                                            </td>
                                            <td className="px-4 py-3 text-center">
                                                {application.candidate?.profile?.years_of_experience ?? '—'} años
                                            </td>
                                            <td className="text-muted-foreground px-4 py-3">
                                                {application.candidate?.profile?.city ?? '—'}
                                            </td>
                                            <td className="text-muted-foreground px-4 py-3 whitespace-nowrap">
                                                {formatDate(application.applied_at)}
                                            </td>
                                            <td className="px-4 py-3">
                                                <StatusBadge status={application.status} />
                                            </td>
                                            <td className="px-4 py-3 text-right">
                                                <Button variant="outline" size="sm" asChild>
                                                    <Link href={ApplicationController(application.id)} data-cy="application-link">
                                                        Ver expediente
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
