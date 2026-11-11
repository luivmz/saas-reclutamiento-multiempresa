import { Head, Link } from '@inertiajs/react';
import { History } from 'lucide-react';
import ApplicationEvidenceController from '@/actions/App/Http/Controllers/Evidence/ApplicationEvidenceController';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader, Section } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { formatDateTime } from '@/lib/format';
import { dashboard } from '@/routes';
import type { EvidenceHistoryEntry } from '@/types';

type Props = {
    application: {
        id: number;
        code: string;
        vacancy: { code: string; title: string };
    };
    entries: EvidenceHistoryEntry[];
};

/**
 * Historial de las evidencias de una postulación, leído de la auditoría de
 * solo inserción. Solo identificadores: nunca el texto de la evidencia.
 */
export default function EvidenceHistory({ application, entries }: Props) {
    return (
        <>
            <Head title={`Historial de evidencias de ${application.code}`} />
            <PageContainer className="max-w-4xl">
                <PageHeader
                    eyebrow={
                        <span className="font-mono text-xs">
                            {application.code}
                        </span>
                    }
                    title="Historial de evidencias"
                    description={`${application.vacancy.title} (${application.vacancy.code}). Registro de solo inserción; muestra identificadores, no el texto.`}
                    actions={
                        <Button variant="outline" asChild>
                            <Link
                                href={ApplicationEvidenceController.index(
                                    application.id,
                                )}
                            >
                                Volver a las evidencias
                            </Link>
                        </Button>
                    }
                />

                <Section title="Eventos" data-cy="evidence-history">
                    {entries.length === 0 ? (
                        <EmptyState
                            icon={History}
                            title="Sin eventos todavía"
                            description="Cada registro, enlace, revisión, corrección o retiro aparecerá aquí."
                        />
                    ) : (
                        <ol className="divide-y">
                            {entries.map((entry) => (
                                <li
                                    key={entry.id}
                                    className="flex flex-col gap-1 py-3 sm:flex-row sm:items-center sm:justify-between"
                                    data-cy="evidence-history-entry"
                                >
                                    <div className="space-y-1">
                                        <p className="flex flex-wrap items-center gap-2 text-sm">
                                            <StatusBadge
                                                status={entry.action}
                                            />
                                            <span className="font-mono">
                                                {entry.evidence}
                                            </span>
                                            {entry.supersedes && (
                                                <span className="text-muted-foreground text-xs">
                                                    sustituye a{' '}
                                                    {entry.supersedes}
                                                </span>
                                            )}
                                        </p>
                                        {entry.criterion && (
                                            <p className="text-muted-foreground text-xs">
                                                Criterio: {entry.criterion}
                                            </p>
                                        )}
                                    </div>
                                    <p className="text-muted-foreground text-xs sm:text-right">
                                        {entry.actor
                                            ? `${entry.actor.name} (${entry.actor.role})`
                                            : 'Usuario no disponible'}
                                        <br />
                                        <time dateTime={entry.created_at}>
                                            {formatDateTime(entry.created_at)}
                                        </time>
                                    </p>
                                </li>
                            ))}
                        </ol>
                    )}
                </Section>
            </PageContainer>
        </>
    );
}

EvidenceHistory.layout = {
    breadcrumbs: [
        { title: 'Panel', href: dashboard() },
        { title: 'Historial de evidencias', href: dashboard() },
    ],
};
