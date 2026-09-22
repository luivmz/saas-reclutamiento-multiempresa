import type { LucideIcon } from 'lucide-react';
import { Inbox } from 'lucide-react';
import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';

/**
 * Pantalla vacía.
 *
 * Una lista sin datos no es un error: explica por qué está vacía y, cuando
 * hay algo que hacer, ofrece la acción. Nunca se disculpa.
 */
export function EmptyState({
    title,
    description,
    icon: Icon = Inbox,
    action,
    className,
}: {
    title: string;
    description?: string;
    icon?: LucideIcon;
    action?: ReactNode;
    className?: string;
}) {
    return (
        <div
            className={cn(
                'bg-card flex flex-col items-center justify-center gap-4 rounded-xl border border-dashed px-6 py-14 text-center',
                className,
            )}
            data-cy="empty-state"
        >
            <div className="bg-surface text-muted-foreground flex size-12 items-center justify-center rounded-full">
                <Icon className="size-5" aria-hidden="true" />
            </div>
            <div className="space-y-1.5">
                <p className="font-serif text-base font-semibold">{title}</p>
                {description && (
                    <p className="text-muted-foreground mx-auto max-w-md text-sm leading-relaxed">
                        {description}
                    </p>
                )}
            </div>
            {action}
        </div>
    );
}
