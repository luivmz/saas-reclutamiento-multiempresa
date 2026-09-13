import { Head, Link } from '@inertiajs/react';
import { ExternalLink } from 'lucide-react';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import { DetailList, PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { formatDateTime } from '@/lib/format';
import { show as jobsShow } from '@/routes/jobs';
import type { JobApplication, Presented } from '@/types';

type TimelineEntry = { id: number; to: Presented; created_at: string };

export default function MyApplicationShow({
    application,
    timeline,
}: {
    application: JobApplication;
    timeline: TimelineEntry[];
}) {
    return (
        <>
            <Head title={`Postulación ${application.code}`} />
            <PageContainer className="max-w-4xl">
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono">{application.code}</span>
                            <StatusBadge status={application.status} />
                        </>
                    }
                    title={application.vacancy?.title ?? 'Postulación'}
                    description={application.vacancy?.organization ?? undefined}
                    actions={
                        application.vacancy?.status.value === 'publicada' && (
                            <Button variant="outline" asChild>
                                <Link href={jobsShow(application.vacancy.id)}>
                                    <ExternalLink />
                                    Ver convocatoria
                                </Link>
                            </Button>
                        )
                    }
                />
                <div className="grid gap-6 md:grid-cols-2">
                    <Card>
                        <CardHeader>
                            <CardTitle>Estado actual</CardTitle>
                            <CardDescription>
                                Le notificaremos cada cambio de etapa.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <DetailList
                                className="sm:grid-cols-1"
                                items={[
                                    { label: 'Etapa', value: <StatusBadge status={application.status} /> },
                                    { label: 'Fecha de postulación', value: formatDateTime(application.applied_at) },
                                    { label: 'Última actualización', value: formatDateTime(application.stage_changed_at) },
                                ]}
                            />
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader>
                            <CardTitle>Seguimiento</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <ol className="space-y-4 border-l pl-5" data-cy="candidate-timeline">
                                {timeline.map((entry) => (
                                    <li key={entry.id} className="relative">
                                        <span className="bg-primary absolute top-1.5 -left-[25px] size-2.5 rounded-full" />
                                        <StatusBadge status={entry.to} />
                                        <p className="text-muted-foreground mt-1 text-xs">
                                            {formatDateTime(entry.created_at)}
                                        </p>
                                    </li>
                                ))}
                            </ol>
                        </CardContent>
                    </Card>
                </div>
            </PageContainer>
        </>
    );
}

MyApplicationShow.layout = {
    breadcrumbs: [
        { title: 'Mis postulaciones', href: CandidateApplicationController.index() },
        { title: 'Detalle', href: CandidateApplicationController.index() },
    ],
};
