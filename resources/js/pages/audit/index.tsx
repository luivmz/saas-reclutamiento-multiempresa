import { Head, router } from '@inertiajs/react';
import { ShieldCheck } from 'lucide-react';
import AuditLogController from '@/actions/App/Http/Controllers/Audit/AuditLogController';
import { EmptyState } from '@/components/empty-state';
import { NativeSelect } from '@/components/form-controls';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Card } from '@/components/ui/card';
import { formatDateTime } from '@/lib/format';
import type { Paginated, Presented } from '@/types';

type AuditEntry = {
    id: number;
    created_at: string;
    actor: string;
    action: Presented;
    entity: { type: string; label: string; id: number };
    details: { label: string; value: string }[];
};

type Props = {
    logs: Paginated<AuditEntry>;
    actions: Presented[];
    filters: { accion: string | null };
};

export default function AuditIndex({ logs, actions, filters }: Props) {
    const filter = (accion: string) =>
        router.get(
            AuditLogController.index.url({ query: accion ? { accion } : {} }),
            {},
            { preserveState: true, replace: true },
        );

    return (
        <>
            <Head title="Auditoría" />
            <PageContainer>
                <PageHeader
                    title="Registro de auditoría"
                    description="RF-27 · Acciones críticas del proceso de reclutamiento de su organización. Los registros son de solo lectura y no pueden modificarse."
                />

                <div className="flex flex-wrap items-end gap-3">
                    <div className="w-full max-w-sm">
                        <label htmlFor="audit-action" className="mb-1 block text-sm font-medium">
                            Acción
                        </label>
                        <NativeSelect
                            id="audit-action"
                            options={actions}
                            placeholder="Todas las acciones"
                            value={filters.accion ?? ''}
                            onChange={(event) => filter(event.target.value)}
                            data-cy="audit-action-filter"
                        />
                    </div>
                </div>

                {logs.data.length === 0 ? (
                    <EmptyState icon={ShieldCheck} title="No hay registros para mostrar" description="Las acciones críticas del proceso aparecerán aquí." />
                ) : (
                    <Card className="gap-0 overflow-hidden py-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm" data-cy="audit-table">
                                <thead className="bg-muted/50 text-muted-foreground text-left text-xs tracking-wide uppercase">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Fecha y hora</th>
                                        <th className="px-4 py-3 font-medium">Actor</th>
                                        <th className="px-4 py-3 font-medium">Acción</th>
                                        <th className="px-4 py-3 font-medium">Entidad</th>
                                        <th className="px-4 py-3 font-medium">Detalle</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {logs.data.map((log) => (
                                        <tr key={log.id} className="align-top" data-cy="audit-row" data-action={log.action.value}>
                                            <td className="text-muted-foreground px-4 py-3 whitespace-nowrap">{formatDateTime(log.created_at)}</td>
                                            <td className="px-4 py-3 font-medium">{log.actor}</td>
                                            <td className="px-4 py-3">
                                                <StatusBadge status={log.action} />
                                            </td>
                                            <td className="px-4 py-3 whitespace-nowrap">
                                                {log.entity.label} <span className="text-muted-foreground font-mono text-xs">#{log.entity.id}</span>
                                            </td>
                                            <td className="px-4 py-3">
                                                {log.details.length === 0 ? (
                                                    <span className="text-muted-foreground">—</span>
                                                ) : (
                                                    <dl className="grid gap-0.5">
                                                        {log.details.map((detail) => (
                                                            <div key={detail.label} className="flex gap-1.5">
                                                                <dt className="text-muted-foreground">{detail.label}:</dt>
                                                                <dd>{detail.value}</dd>
                                                            </div>
                                                        ))}
                                                    </dl>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                )}

                <Pagination meta={logs.meta} />
            </PageContainer>
        </>
    );
}

AuditIndex.layout = {
    breadcrumbs: [{ title: 'Auditoría', href: AuditLogController.index() }],
};
