import { Head, Link } from '@inertiajs/react';
import { Briefcase, Building2 } from 'lucide-react';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { formatDate } from '@/lib/format';
import { index as jobsIndex } from '@/routes/jobs';
import type { JobApplication, Paginated } from '@/types';

export default function MyApplications({
    applications,
}: {
    applications: Paginated<JobApplication>;
}) {
    return (
        <>
            <Head title="Mis postulaciones" />
            <PageContainer>
                <PageHeader
                    title="Mis postulaciones"
                    description="Seguimiento de sus postulaciones y de la etapa en que se encuentran."
                    actions={
                        <Button variant="outline" asChild>
                            <Link href={jobsIndex()}>
                                <Briefcase />
                                Buscar empleos
                            </Link>
                        </Button>
                    }
                />
                {applications.data.length === 0 ? (
                    <EmptyState
                        icon={Briefcase}
                        title="Aún no tiene postulaciones"
                        description="Explore las convocatorias vigentes y postule a las que se ajusten a su perfil."
                        action={
                            <Button asChild>
                                <Link href={jobsIndex()}>Ver empleos</Link>
                            </Button>
                        }
                    />
                ) : (
                    <Card className="gap-0 divide-y py-0" data-cy="my-applications">
                        {applications.data.map((application) => (
                            <Link
                                key={application.id}
                                href={CandidateApplicationController.show(application.id)}
                                className="hover:bg-muted/40 flex flex-col gap-2 p-4 sm:flex-row sm:items-center sm:justify-between"
                                data-cy="my-application-row"
                            >
                                <div className="min-w-0 space-y-1">
                                    <p className="font-medium">{application.vacancy?.title}</p>
                                    <p className="text-muted-foreground flex flex-wrap items-center gap-1.5 text-xs">
                                        <Building2 className="size-3.5" />
                                        {application.vacancy?.organization}
                                        <span>·</span>
                                        <span className="font-mono">{application.code}</span>
                                        <span>·</span>
                                        Postuló el {formatDate(application.applied_at)}
                                    </p>
                                </div>
                                <StatusBadge status={application.status} />
                            </Link>
                        ))}
                    </Card>
                )}
                <Pagination meta={applications.meta} />
            </PageContainer>
        </>
    );
}

MyApplications.layout = {
    breadcrumbs: [
        { title: 'Mis postulaciones', href: CandidateApplicationController.index() },
    ],
};
