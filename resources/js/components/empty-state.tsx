import type { LucideIcon } from 'lucide-react';
import { Inbox } from 'lucide-react';
import type { ReactNode } from 'react';

export function EmptyState({
    title,
    description,
    icon: Icon = Inbox,
    action,
}: {
    title: string;
    description?: string;
    icon?: LucideIcon;
    action?: ReactNode;
}) {
    return (
        <div
            className="flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed px-6 py-12 text-center"
            data-cy="empty-state"
        >
            <div className="bg-muted text-muted-foreground flex size-11 items-center justify-center rounded-full">
                <Icon className="size-5" />
            </div>
            <div className="space-y-1">
                <p className="font-medium">{title}</p>
                {description && (
                    <p className="text-muted-foreground max-w-md text-sm">
                        {description}
                    </p>
                )}
            </div>
            {action}
        </div>
    );
}
