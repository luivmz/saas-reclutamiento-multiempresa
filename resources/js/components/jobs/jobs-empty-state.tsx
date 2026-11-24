import { Link } from '@inertiajs/react';
import { SearchX } from 'lucide-react';
import { EmptyState } from '@/components/empty-state';
import { Button } from '@/components/ui/button';
import { index as jobsIndex } from '@/routes/jobs';

/**
 * Lista de empleos sin resultados (DEF-26).
 *
 * Son tres casos distintos y cada uno pide algo diferente a quien busca:
 * - la búsqueda no coincide con nada: se nombra el término y se ofrece quitarlo;
 * - no hay ninguna convocatoria publicada: no hay filtro que quitar;
 * - la página pedida está fuera de rango (un enlace viejo): se vuelve a la primera.
 *
 * `total` es el total de la consulta (con la búsqueda aplicada), no de la página.
 */
export function JobsEmptyState({
    query,
    total,
}: {
    query: string;
    total: number;
}) {
    if (total > 0) {
        return (
            <EmptyState
                title="Esta página no tiene convocatorias"
                description="La lista cambió desde que se abrió este enlace."
                action={
                    <Button asChild variant="outline">
                        <Link
                            href={jobsIndex(
                                query ? { query: { q: query } } : undefined,
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
        />
    );
}
