import { Link } from '@inertiajs/react';
import { SearchX } from 'lucide-react';
import { EmptyState } from '@/components/empty-state';
import { Button } from '@/components/ui/button';
import { home } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

/**
 * Lista de convocatorias sin resultados (DEF-26, lote 3).
 *
 * Son tres casos distintos y cada uno pide algo diferente a quien busca:
 * - la búsqueda o los filtros no coinciden con nada: se dice que es por esos
 *   criterios (no que no haya convocatorias) y se ofrece quitarlos;
 * - no hay ninguna convocatoria publicada: no hay criterio que quitar;
 * - la página pedida está fuera de rango: se vuelve a la primera con los mismos
 *   criterios. No se afirma por qué: solo se sabe que no existe.
 *
 * `total` es el total de la consulta (con búsqueda y filtros), no de la página.
 * `criteria` son los parámetros aplicados, sin la página.
 */
export function JobsEmptyState({
    query,
    total,
    filterCount = 0,
    criteria,
}: {
    query: string;
    total: number;
    filterCount?: number;
    criteria?: Record<string, string>;
}) {
    if (total > 0) {
        const firstPage = criteria ?? (query ? { q: query } : {});

        return (
            <EmptyState
                title="Esta página no tiene convocatorias"
                description="La página indicada en la dirección no existe en esta lista. Las convocatorias empiezan en la primera página."
                action={
                    <Button asChild variant="outline">
                        <Link
                            href={jobsIndex(
                                Object.keys(firstPage).length > 0
                                    ? { query: firstPage }
                                    : undefined,
                            )}
                            data-cy="jobs-first-page"
                        >
                            Ir a la primera página
                        </Link>
                    </Button>
                }
            />
        );
    }

    if (filterCount > 0) {
        return (
            <EmptyState
                icon={SearchX}
                title={
                    query
                        ? `Ninguna convocatoria coincide con «${query}» y los filtros actuales`
                        : 'Ninguna convocatoria coincide con los filtros actuales'
                }
                description="Hay convocatorias publicadas que no cumplen estos criterios. Quite algún filtro o vuelva a ver todas."
                action={
                    <Button asChild>
                        <Link href={jobsIndex()} data-cy="jobs-clear-search">
                            {query
                                ? 'Quitar búsqueda y filtros'
                                : 'Quitar filtros'}
                        </Link>
                    </Button>
                }
            />
        );
    }

    if (query) {
        return (
            <EmptyState
                icon={SearchX}
                title={`Ninguna convocatoria coincide con «${query}»`}
                description="Pruebe con otro puesto o vea todas las convocatorias publicadas."
                action={
                    <Button asChild>
                        <Link href={jobsIndex()} data-cy="jobs-clear-search">
                            Ver todas las convocatorias
                        </Link>
                    </Button>
                }
            />
        );
    }

    return (
        <EmptyState
            title="Todavía no hay convocatorias publicadas"
            description="Cuando una organización publique una convocatoria, aparecerá aquí."
            action={
                <Button asChild variant="outline">
                    <Link href={home()}>Volver al inicio</Link>
                </Button>
            }
        />
    );
}
