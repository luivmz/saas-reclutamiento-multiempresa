import { Head, Link } from '@inertiajs/react';
import { Briefcase } from 'lucide-react';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
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
                    description="Seguimiento de sus postulaciones y de la etapa en que se encuentra cada una."
                    actions={
                        <Button variant="outline" asChild>
                            <Link href={jobsIndex()}>
                                <Briefcase aria-hidden="true" />
                                Buscar empleos
                            </Link>
                        </Button>
                    }
                />
                {applications.data.length === 0 ? (
                    <EmptyState
                        icon={Briefcase}
                        title="Todavía no tiene postulaciones"
                        description="Explore las convocatorias vigentes y postule a las que se ajusten a su perfil."
                        action={
                            <Button asChild>
                                <Link href={jobsIndex()}>Ver empleos</Link>
                            </Button>
                        }
                    />
                ) : (
                    <ul
                        className="bg-card divide-y overflow-hidden rounded-xl border"
                        data-cy="my-applications"
                    >
                        {applications.data.map((application) => (
                            <li key={application.id}>
                                <Link
                                    href={CandidateApplicationController.show(
                                        application.id,
                                    )}
                                    className="hover:bg-surface flex flex-col gap-3 px-5 py-4 transition-colors sm:flex-row sm:items-center sm:justify-between"
                                    data-cy="my-application-row"
                                >
                                    <span className="min-w-0 space-y-1">
                                        <span className="block font-medium">
                                            {application.vacancy?.title}
                                        </span>
                                        <span className="text-muted-foreground block text-xs">
                                            {application.vacancy?.organization}
                                        </span>
                                        <span className="text-muted-foreground block text-xs">
                                            <span className="font-mono">
                                                {application.code}
                                            </span>
                                            , postuló el{' '}
                                            {formatDate(application.applied_at)}
                                        </span>
                                    </span>
                                    <StatusBadge status={application.status} />
                                </Link>
                            </li>
                        ))}
                    </ul>
                )}
                <Pagination meta={applications.meta} />
            </PageContainer>
        </>
    );
}

MyApplications.layout = {
    breadcrumbs: [
        {
            title: 'Mis postulaciones',
            href: CandidateApplicationController.index(),
        },
    ],
};
