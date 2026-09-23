import { Head, router } from '@inertiajs/react';
import { ShieldCheck } from 'lucide-react';
import AuditLogController from '@/actions/App/Http/Controllers/Audit/AuditLogController';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { NativeSelect } from '@/components/form-controls';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Label } from '@/components/ui/label';
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
                    description="Acciones críticas del proceso de reclutamiento de su organización (RF-27). Los registros son de solo lectura: ni siquiera la plataforma puede modificarlos."
                />

                <div className="w-full max-w-sm space-y-2">
                    <Label htmlFor="audit-action">Acción</Label>
                    <NativeSelect
                        id="audit-action"
                        options={actions}
                        placeholder="Todas las acciones"
                        value={filters.accion ?? ''}
                        onChange={(event) => filter(event.target.value)}
                        data-cy="audit-action-filter"
                    />
                </div>

                {logs.data.length === 0 ? (
                    <EmptyState
                        icon={ShieldCheck}
                        title="No hay registros para mostrar"
                        description={
                            filters.accion
                                ? 'Todavía no se ha registrado ninguna acción de ese tipo.'
                                : 'Las acciones críticas del proceso aparecerán aquí a medida que ocurran.'
                        }
                    />
                ) : (
                    <DataTable
                        caption="Acciones críticas registradas en su organización"
                        data-cy="audit-table"
                        rows={logs.data}
                        rowKey={(row) => row.id}
                        rowAttributes={(row) => ({
                            'data-cy': 'audit-row',
                            'data-action': row.action.value,
                            className: 'md:align-top',
                        })}
                        columns={[
                            {
                                key: 'created',
                                header: 'Fecha y hora',
                                className:
                                    'text-muted-foreground whitespace-nowrap',
                                cell: (row) => formatDateTime(row.created_at),
                            },
                            {
                                key: 'actor',
                                header: 'Actor',
                                className: 'font-medium',
                                cell: (row) => row.actor,
                            },
                            {
                                key: 'action',
                                header: 'Acción',
                                cell: (row) => (
                                    <StatusBadge status={row.action} />
                                ),
                            },
                            {
                                key: 'entity',
                                header: 'Entidad',
                                className: 'whitespace-nowrap',
                                cell: (row) => (
                                    <>
                                        {row.entity.label}{' '}
                                        <span className="text-muted-foreground font-mono text-xs">
                                            #{row.entity.id}
                                        </span>
                                    </>
                                ),
                            },
                            {
                                key: 'details',
                                header: 'Detalle',
                                cell: (row) =>
                                    row.details.length === 0 ? (
                                        <span className="text-muted-foreground">
                                            —
                                        </span>
                                    ) : (
                                        <dl className="grid gap-0.5">
                                            {row.details.map((detail) => (
                                                <div
                                                    key={detail.label}
                                                    className="flex gap-1.5"
                                                >
                                                    <dt className="text-muted-foreground whitespace-nowrap">
                                                        {detail.label}:
                                                    </dt>
                                                    <dd>{detail.value}</dd>
                                                </div>
                                            ))}
                                        </dl>
                                    ),
                            },
                        ]}
                    />
                )}

                <Pagination meta={logs.meta} />
            </PageContainer>
        </>
    );
}

AuditIndex.layout = {
    breadcrumbs: [{ title: 'Auditoría', href: AuditLogController.index() }],
};
