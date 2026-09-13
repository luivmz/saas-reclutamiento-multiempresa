import { cn } from '@/lib/utils';
import type { Presented, Tone } from '@/types';

const toneClasses: Record<Tone, string> = {
    neutral: 'bg-muted text-muted-foreground ring-border',
    info: 'bg-sky-50 text-sky-800 ring-sky-200 dark:bg-sky-950/60 dark:text-sky-300 dark:ring-sky-900',
    primary:
        'bg-indigo-50 text-indigo-800 ring-indigo-200 dark:bg-indigo-950/60 dark:text-indigo-300 dark:ring-indigo-900',
    success:
        'bg-emerald-50 text-emerald-800 ring-emerald-200 dark:bg-emerald-950/60 dark:text-emerald-300 dark:ring-emerald-900',
    warning:
        'bg-amber-50 text-amber-900 ring-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:ring-amber-900',
    danger: 'bg-rose-50 text-rose-800 ring-rose-200 dark:bg-rose-950/60 dark:text-rose-300 dark:ring-rose-900',
};

export function StatusBadge({
    status,
    className,
}: {
    status: Presented;
    className?: string;
}) {
    return (
        <span
            data-cy="status-badge"
            data-status={status.value}
            className={cn(
                'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap ring-1 ring-inset',
                toneClasses[status.tone],
                className,
            )}
        >
            {status.label}
        </span>
    );
}
