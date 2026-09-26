import { ArrowRight } from 'lucide-react';
import { StatusBadge } from '@/components/status-badge';
import { formatDateTime } from '@/lib/format';
import type { StatusHistoryEntry } from '@/types';

/**
 * Historial de estados de un expediente.
 *
 * Es la prueba de la trazabilidad: qué cambió, quién lo hizo y cuándo. Por eso
 * el autor y la fecha nunca se recortan, aunque el panel sea estrecho.
 */
export function StatusTimeline({ entries }: { entries: StatusHistoryEntry[] }) {
    if (entries.length === 0) {
        return (
            <p className="text-muted-foreground text-sm">
                Todavía no hay movimientos registrados.
            </p>
        );
    }

    return (
        <ol
            className="relative space-y-6 border-l pl-5"
            data-cy="status-timeline"
        >
            {entries.map((entry) => (
                <li key={entry.id} className="relative">
                    <span
                        aria-hidden="true"
                        className="bg-primary ring-card absolute top-1.5 -left-[25px] size-2.5 rounded-full ring-4"
                    />
                    <div className="flex flex-wrap items-center gap-2">
                        {entry.from && (
                            <>
                                <StatusBadge status={entry.from} />
                                <ArrowRight
                                    className="text-muted-foreground size-3"
                                    aria-hidden="true"
                                />
                            </>
                        )}
                        <StatusBadge status={entry.to} />
                    </div>
                    <p className="text-muted-foreground mt-1.5 text-xs">
                        {entry.author}, {formatDateTime(entry.created_at)}
                    </p>
                    {entry.comment && (
                        <p className="bg-surface mt-2 rounded-md px-3 py-2 text-sm leading-relaxed">
                            {entry.comment}
                        </p>
                    )}
                </li>
            ))}
        </ol>
    );
}
