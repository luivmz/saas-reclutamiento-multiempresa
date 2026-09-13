import { Link } from '@inertiajs/react';
import { cn } from '@/lib/utils';
import type { Paginated } from '@/types';

export function Pagination({ meta }: { meta: Paginated<unknown>['meta'] }) {
    if (meta.last_page <= 1) {
        return null;
    }

    const lastIndex = meta.links.length - 1;

    return (
        <nav
            className="flex flex-col items-center justify-between gap-3 text-sm sm:flex-row"
            aria-label="Paginación"
        >
            <p className="text-muted-foreground">
                Mostrando {meta.from}–{meta.to} de {meta.total}
            </p>
            <div className="flex flex-wrap items-center gap-1">
                {meta.links.map((link, index) => {
                    const label =
                        index === 0
                            ? '‹ Anterior'
                            : index === lastIndex
                              ? 'Siguiente ›'
                              : link.label;

                    return link.url ? (
                        <Link
                            key={index}
                            href={link.url}
                            preserveScroll
                            className={cn(
                                'hover:bg-accent rounded-md border px-3 py-1.5',
                                link.active &&
                                    'bg-primary text-primary-foreground hover:bg-primary',
                            )}
                        >
                            {label}
                        </Link>
                    ) : (
                        <span
                            key={index}
                            className="text-muted-foreground rounded-md border px-3 py-1.5 opacity-50"
                        >
                            {label}
                        </span>
                    );
                })}
            </div>
        </nav>
    );
}
