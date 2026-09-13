import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';

export function PageContainer({
    children,
    className,
}: {
    children: ReactNode;
    className?: string;
}) {
    return (
        <div
            className={cn(
                'mx-auto flex w-full max-w-6xl flex-col gap-6 p-4 md:p-6',
                className,
            )}
        >
            {children}
        </div>
    );
}

export function PageHeader({
    title,
    description,
    eyebrow,
    actions,
}: {
    title: string;
    description?: ReactNode;
    eyebrow?: ReactNode;
    actions?: ReactNode;
}) {
    return (
        <div className="flex flex-col gap-4 border-b pb-5 sm:flex-row sm:items-end sm:justify-between">
            <div className="min-w-0 space-y-1">
                {eyebrow && (
                    <div className="text-muted-foreground flex flex-wrap items-center gap-2 text-xs font-medium tracking-wide uppercase">
                        {eyebrow}
                    </div>
                )}
                <h1
                    className="text-2xl font-semibold tracking-tight"
                    data-cy="page-title"
                >
                    {title}
                </h1>
                {description && (
                    <p className="text-muted-foreground text-sm">
                        {description}
                    </p>
                )}
            </div>
            {actions && (
                <div className="flex flex-wrap items-center gap-2">
                    {actions}
                </div>
            )}
        </div>
    );
}

export function DetailList({
    items,
    className,
}: {
    items: { label: string; value: ReactNode }[];
    className?: string;
}) {
    return (
        <dl className={cn('grid gap-x-6 gap-y-4 sm:grid-cols-2', className)}>
            {items.map((item) => (
                <div key={item.label} className="min-w-0 space-y-1">
                    <dt className="text-muted-foreground text-xs font-medium tracking-wide uppercase">
                        {item.label}
                    </dt>
                    <dd className="text-sm break-words">{item.value}</dd>
                </div>
            ))}
        </dl>
    );
}
