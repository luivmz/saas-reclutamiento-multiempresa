import { ArrowRight } from 'lucide-react';
import { StatusBadge } from '@/components/status-badge';
import { formatDateTime } from '@/lib/format';
import type { StatusHistoryEntry } from '@/types';

export function StatusTimeline({ entries }: { entries: StatusHistoryEntry[] }) {
    if (entries.length === 0) {
        return (
            <p className="text-muted-foreground text-sm">
                Sin movimientos registrados.
            </p>
        );
    }

    return (
        <ol className="relative space-y-5 border-l pl-5" data-cy="status-timeline">
            {entries.map((entry) => (
                <li key={entry.id} className="relative">
                    <span className="bg-primary border-background ring-border absolute top-1.5 -left-[25px] size-2.5 rounded-full border-2 ring-1" />
                    <div className="flex flex-wrap items-center gap-2">
                        {entry.from && (
                            <>
                                <StatusBadge status={entry.from} />
                                <ArrowRight className="text-muted-foreground size-3" />
                            </>
                        )}
                        <StatusBadge status={entry.to} />
                    </div>
                    <p className="text-muted-foreground mt-1 text-xs">
                        {entry.author} · {formatDateTime(entry.created_at)}
                    </p>
                    {entry.comment && (
                        <p className="bg-muted/60 mt-2 rounded-md px-3 py-2 text-sm">
                            {entry.comment}
                        </p>
                    )}
                </li>
            ))}
        </ol>
    );
}
