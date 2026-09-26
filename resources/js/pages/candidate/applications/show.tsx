import { Head, Link } from '@inertiajs/react';
import { ExternalLink } from 'lucide-react';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import {
    DetailList,
    PageContainer,
    PageHeader,
    Section,
} from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { formatDateTime } from '@/lib/format';
import { show as jobsShow } from '@/routes/jobs';
import type { JobApplication, Presented } from '@/types';

type TimelineEntry = { id: number; to: Presented; created_at: string };

type Convocation = {
    key: string;
    title: string;
    scheduled_at: string;
    duration_minutes: number | null;
    modality: string;
    location: string;
    instructions: string | null;
    status: Presented;
};

export default function MyApplicationShow({
    application,
    timeline,
    convocations,
}: {
    application: JobApplication;
    timeline: TimelineEntry[];
    convocations: Convocation[];
}) {
    return (
        <>
            <Head title={`Postulación ${application.code}`} />
            <PageContainer className="max-w-4xl">
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono text-xs">
                                {application.code}
                            </span>
                            <StatusBadge status={application.status} />
                        </>
                    }
                    title={application.vacancy?.title ?? 'Postulación'}
                    description={application.vacancy?.organization ?? undefined}
                    actions={
                        application.vacancy?.status.value === 'publicada' && (
                            <Button variant="outline" asChild>
                                <Link href={jobsShow(application.vacancy.id)}>
                                    <ExternalLink aria-hidden="true" />
                                    Ver convocatoria
                                </Link>
                            </Button>
                        )
                    }
                />

                <div className="grid min-w-0 gap-6 md:grid-cols-2">
                    <Section
                        title="Estado actual"
                        description="Le avisaremos por notificación en cada cambio de etapa."
                    >
                        <DetailList
                            className="sm:grid-cols-1"
                            items={[
                                {
                                    label: 'Etapa',
                                    value: (
                                        <StatusBadge
                                            status={application.status}
                                        />
                                    ),
                                },
                                {
                                    label: 'Fecha de postulación',
                                    value: formatDateTime(
                                        application.applied_at,
                                    ),
                                },
                                {
                                    label: 'Última actualización',
                                    value: formatDateTime(
                                        application.stage_changed_at,
                                    ),
                                },
                            ]}
                        />
                    </Section>

                    <Section title="Seguimiento">
                        <ol
                            className="space-y-5 border-l pl-5"
                            data-cy="candidate-timeline"
                        >
                            {timeline.map((entry) => (
                                <li key={entry.id} className="relative">
                                    <span
                                        aria-hidden="true"
                                        className="bg-primary ring-card absolute top-1.5 -left-[25px] size-2.5 rounded-full ring-4"
                                    />
                                    <StatusBadge status={entry.to} />
                                    <p className="text-muted-foreground mt-1.5 text-xs">
                                        {formatDateTime(entry.created_at)}
                                    </p>
                                </li>
                            ))}
                        </ol>
                    </Section>
                </div>

                <Section
                    title="Convocatorias"
                    description="Evaluaciones y entrevistas a las que ha sido convocado."
                    data-cy="candidate-convocations"
                >
                    <div className="space-y-3">
                        {convocations.length === 0 ? (
                            <p className="text-muted-foreground text-sm">
                                Todavía no tiene convocatorias para esta
                                postulación.
                            </p>
                        ) : (
                            convocations.map((convocation) => (
                                <article
                                    key={convocation.key}
                                    className="space-y-2 rounded-lg border p-4 text-sm"
                                    data-cy="convocation-item"
                                >
                                    <div className="flex flex-wrap items-center justify-between gap-2">
                                        <h3 className="font-medium">
                                            {convocation.title}
                                        </h3>
                                        <StatusBadge
                                            status={convocation.status}
                                        />
                                    </div>
                                    <p>
                                        {formatDateTime(
                                            convocation.scheduled_at,
                                        )}
                                        {convocation.duration_minutes
                                            ? `, ${convocation.duration_minutes} minutos`
                                            : ''}
                                    </p>
                                    <p className="text-muted-foreground">
                                        {convocation.modality},{' '}
                                        {convocation.location}
                                    </p>
                                    {convocation.instructions && (
                                        <p className="bg-surface rounded-md px-3 py-2 leading-relaxed">
                                            {convocation.instructions}
                                        </p>
                                    )}
                                </article>
                            ))
                        )}
                    </div>
                </Section>
            </PageContainer>
        </>
    );
}

MyApplicationShow.layout = {
    breadcrumbs: [
        {
            title: 'Mis postulaciones',
            href: CandidateApplicationController.index(),
        },
        { title: 'Detalle', href: CandidateApplicationController.index() },
    ],
};
