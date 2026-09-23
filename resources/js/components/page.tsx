import type { ComponentProps, ReactNode } from 'react';
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
                'mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8 lg:py-8',
                className,
            )}
        >
            {children}
        </div>
    );
}

/**
 * Encabezado de página.
 *
 * `eyebrow` lleva la identidad del expediente —código y estado—, no una
 * etiqueta decorativa: si no aporta un dato, no se pone.
 */
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
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between lg:gap-8">
            <div className="min-w-0 space-y-2">
                {eyebrow && (
                    <div className="text-muted-foreground flex flex-wrap items-center gap-2 text-sm">
                        {eyebrow}
                    </div>
                )}
                <h1
                    className="font-serif text-2xl leading-tight font-semibold tracking-tight sm:text-3xl"
                    data-cy="page-title"
                >
                    {title}
                </h1>
                {description && (
                    <p className="text-muted-foreground max-w-2xl text-sm leading-relaxed">
                        {description}
                    </p>
                )}
            </div>
            {actions && (
                <div className="flex flex-wrap items-center gap-2 lg:justify-end">
                    {actions}
                </div>
            )}
        </div>
    );
}

/**
 * Pares dato/valor de un expediente.
 *
 * La estructura `<div><dt/><dd/></div>` es la que recorren las pruebas E2E
 * (`cy.contains('dt', …).siblings('dd')`): `dt` y `dd` deben seguir siendo
 * hermanos directos.
 */
export function DetailList({
    items,
    className,
}: {
    items: { label: string; value: ReactNode }[];
    className?: string;
}) {
    return (
        <dl className={cn('grid gap-x-8 gap-y-5 sm:grid-cols-2', className)}>
            {items.map((item) => (
                <div key={item.label} className="min-w-0 space-y-1">
                    <dt className="text-muted-foreground text-xs font-medium">
                        {item.label}
                    </dt>
                    <dd className="text-sm leading-snug break-words">
                        {item.value}
                    </dd>
                </div>
            ))}
        </dl>
    );
}

/**
 * Bloque de contenido con título propio dentro de una página.
 *
 * Reemplaza la repetición de `Card + CardHeader + CardTitle` que estaba
 * copiada en cada módulo, y garantiza que el nivel de encabezado sea `h2`:
 * el lector de pantalla recorre la página como un índice.
 */
export function Section({
    title,
    description,
    actions,
    children,
    className,
    contentClassName,
    ...props
}: {
    title?: ReactNode;
    description?: ReactNode;
    actions?: ReactNode;
    children: ReactNode;
    className?: string;
    contentClassName?: string;
} & Omit<ComponentProps<'section'>, 'title'> &
    Record<`data-${string}`, string | undefined>) {
    return (
        <section
            className={cn(
                'bg-card text-card-foreground rounded-xl border',
                className,
            )}
            {...props}
        >
            {(title || actions) && (
                <div className="flex flex-wrap items-start justify-between gap-3 border-b px-5 py-4">
                    <div className="min-w-0 space-y-1">
                        {title && (
                            <h2 className="font-serif text-base font-semibold">
                                {title}
                            </h2>
                        )}
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
            )}
            <div className={cn('px-5 py-5', contentClassName)}>{children}</div>
        </section>
    );
}
