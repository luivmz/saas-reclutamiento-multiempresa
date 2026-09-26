import { Link } from '@inertiajs/react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Paginated } from '@/types';

/**
 * Paginación de un listado.
 *
 * La página actual se marca con `aria-current`, no solo con color, y los
 * extremos llevan su flecha como icono aparte del texto: quien navega por
 * teclado o con lector de pantalla oye «Anterior», no un carácter suelto.
 */
export function Pagination({ meta }: { meta: Paginated<unknown>['meta'] }) {
    if (meta.last_page <= 1) {
        return null;
    }

    const lastIndex = meta.links.length - 1;
    const base =
        'inline-flex h-8 min-w-8 items-center justify-center gap-1 rounded-md border px-2.5 text-sm';

    return (
        <nav
            className="flex flex-col items-center justify-between gap-3 text-sm sm:flex-row"
            aria-label="Paginación"
        >
            <p className="text-muted-foreground">
                Mostrando {meta.from}–{meta.to} de {meta.total}
            </p>
            <ul className="flex flex-wrap items-center gap-1">
                {meta.links.map((link, index) => {
                    const isFirst = index === 0;
                    const isLast = index === lastIndex;
                    const label = isFirst
                        ? 'Anterior'
                        : isLast
                          ? 'Siguiente'
                          : link.label;

                    return (
                        <li key={index}>
                            {link.url ? (
                                <Link
                                    href={link.url}
                                    preserveScroll
                                    aria-current={
                                        link.active ? 'page' : undefined
                                    }
                                    aria-label={
                                        isFirst || isLast
                                            ? label
                                            : `Página ${link.label}`
                                    }
                                    className={cn(
                                        base,
                                        'bg-card hover:border-input hover:text-foreground transition-colors',
                                        link.active &&
                                            'border-primary bg-primary text-primary-foreground hover:text-primary-foreground',
                                    )}
                                >
                                    {isFirst && (
                                        <ChevronLeft
                                            className="size-4"
                                            aria-hidden="true"
                                        />
                                    )}
                                    {label}
                                    {isLast && (
                                        <ChevronRight
                                            className="size-4"
                                            aria-hidden="true"
                                        />
                                    )}
                                </Link>
                            ) : (
                                <span
                                    className={cn(
                                        base,
                                        'text-muted-foreground border-dashed',
                                    )}
                                >
                                    {isFirst && (
                                        <ChevronLeft
                                            className="size-4"
                                            aria-hidden="true"
                                        />
                                    )}
                                    {label}
                                    {isLast && (
                                        <ChevronRight
                                            className="size-4"
                                            aria-hidden="true"
                                        />
                                    )}
                                </span>
                            )}
                        </li>
                    );
                })}
            </ul>
        </nav>
    );
}
