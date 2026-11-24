import { Link, router } from '@inertiajs/react';
import { Search, SlidersHorizontal, X } from 'lucide-react';
import { useState, type FormEvent } from 'react';
import { NativeSelect } from '@/components/form-controls';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Spinner } from '@/components/ui/spinner';
import {
    activeCriteria,
    activeFilterCount,
    criteriaQuery,
    searchOnly,
    withoutCriterion,
} from '@/lib/job-filters';
import { index as jobsIndex } from '@/routes/jobs';
import type { JobCriteria, JobFilterOptions } from '@/types';

const PANEL_ID = 'jobs-filter-panel';

/**
 * Búsqueda por puesto y filtros del listado público.
 *
 * Los filtros se aplican con «Buscar», no al cambiar un desplegable: con el
 * teclado, recorrer las opciones no debe recargar la página (WCAG 3.2.2).
 * Aplicar siempre vuelve a la primera página. En móvil los desplegables
 * quedan tras «Filtros» para no ocupar la primera pantalla; los criterios
 * activos se ven siempre debajo, cada uno con su forma de quitarlo.
 */
export function JobsFilters({
    criteria,
    options,
    processing,
    onLoadingChange,
}: {
    criteria: JobCriteria;
    options: JobFilterOptions;
    processing: boolean;
    onLoadingChange: (loading: boolean) => void;
}) {
    const [open, setOpen] = useState(false);
    const active = activeCriteria(criteria, options);
    const filterCount = activeFilterCount(criteria);
    // Las claves rehacen los controles cuando cambian los criterios aplicados
    // (enlaces, atrás o adelante): nunca muestran un valor que no se aplicó.
    const applied = JSON.stringify(criteria);

    const loading = {
        preserveState: true,
        onStart: () => onLoadingChange(true),
        onFinish: () => onLoadingChange(false),
    };

    const submit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = Object.fromEntries(new FormData(event.currentTarget));

        router.get(
            jobsIndex.url({
                query: criteriaQuery(data as Record<string, string>),
            }),
            {},
            loading,
        );
    };

    return (
        <div className="space-y-3">
            <form
                role="search"
                aria-label="Buscar convocatorias"
                onSubmit={submit}
                className="grid grid-cols-2 gap-3 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,3fr)_auto] lg:items-end"
                data-cy="jobs-filters"
            >
                <div className="col-span-2 grid gap-1.5 lg:col-span-1">
                    <Label htmlFor="jobs-q">Puesto</Label>
                    <Input
                        key={`q-${applied}`}
                        id="jobs-q"
                        name="q"
                        defaultValue={criteria.q}
                        placeholder="Por ejemplo, docente"
                        maxLength={150}
                        className="max-sm:h-11"
                        data-cy="jobs-search"
                    />
                </div>

                <Button
                    type="button"
                    variant="outline"
                    className="h-11 sm:hidden"
                    aria-expanded={open}
                    aria-controls={PANEL_ID}
                    onClick={() => setOpen((value) => !value)}
                    data-cy="jobs-filters-toggle"
                >
                    <SlidersHorizontal aria-hidden="true" />
                    Filtros
                    {filterCount > 0 && (
                        <span className="bg-primary text-primary-foreground rounded-full px-1.5 text-xs">
                            <span className="sr-only">, activos: </span>
                            {filterCount}
                        </span>
                    )}
                </Button>

                <div
                    id={PANEL_ID}
                    className={`col-span-2 gap-3 sm:grid sm:grid-cols-3 lg:col-span-1 ${open ? 'grid' : 'hidden'}`}
                >
                    <div className="grid min-w-0 gap-1.5">
                        <Label htmlFor="jobs-organizacion">Organización</Label>
                        <NativeSelect
                            key={`o-${applied}`}
                            id="jobs-organizacion"
                            name="organizacion"
                            defaultValue={criteria.organizacion ?? ''}
                            placeholder="Todas"
                            options={options.organizaciones}
                            className="max-sm:h-11"
                            data-cy="jobs-filter-organizacion"
                        />
                    </div>
                    <div className="grid min-w-0 gap-1.5">
                        <Label htmlFor="jobs-ubicacion">Ubicación</Label>
                        <NativeSelect
                            key={`u-${applied}`}
                            id="jobs-ubicacion"
                            name="ubicacion"
                            defaultValue={criteria.ubicacion ?? ''}
                            placeholder="Todas"
                            options={options.ubicaciones}
                            className="max-sm:h-11"
                            data-cy="jobs-filter-ubicacion"
                        />
                    </div>
                    <div className="grid min-w-0 gap-1.5">
                        <Label htmlFor="jobs-contrato">Tipo de contrato</Label>
                        <NativeSelect
                            key={`c-${applied}`}
                            id="jobs-contrato"
                            name="contrato"
                            defaultValue={criteria.contrato ?? ''}
                            placeholder="Todos"
                            options={options.contratos}
                            className="max-sm:h-11"
                            data-cy="jobs-filter-contrato"
                        />
                    </div>
                </div>

                <Button
                    type="submit"
                    variant="secondary"
                    disabled={processing}
                    className="h-11 max-sm:col-start-2 sm:h-9 sm:justify-self-start lg:justify-self-auto"
                    data-cy="jobs-submit"
                >
                    {processing ? <Spinner /> : <Search aria-hidden="true" />}
                    Buscar
                </Button>
            </form>

            {active.length > 0 && (
                <div
                    className="flex flex-wrap items-center gap-2 text-sm"
                    data-cy="jobs-active-criteria"
                >
                    <span className="text-muted-foreground">Aplicado:</span>
                    <ul className="contents">
                        {active.map((item) => (
                            <li key={item.key} className="max-w-full">
                                <Link
                                    href={jobsIndex.url({
                                        query: withoutCriterion(
                                            criteria,
                                            item.key,
                                        ),
                                    })}
                                    {...loading}
                                    className="bg-surface hover:border-primary/50 inline-flex min-h-9 max-w-full items-center gap-1.5 rounded-full border px-3 py-1 [overflow-wrap:anywhere] pointer-coarse:min-h-11"
                                    aria-label={`Quitar ${item.label.toLowerCase()}: ${item.value}`}
                                    data-cy="jobs-criterion"
                                    data-key={item.key}
                                >
                                    <span>
                                        <span className="text-muted-foreground">
                                            {item.label}:
                                        </span>{' '}
                                        {item.value}
                                    </span>
                                    <X
                                        className="size-3.5 shrink-0"
                                        aria-hidden="true"
                                    />
                                </Link>
                            </li>
                        ))}
                    </ul>
                    {filterCount > 0 && (
                        <Link
                            href={jobsIndex.url({
                                query: searchOnly(criteria),
                            })}
                            {...loading}
                            className="text-primary inline-flex min-h-9 items-center font-medium underline underline-offset-4 pointer-coarse:min-h-11"
                            data-cy="jobs-clear-filters"
                        >
                            Limpiar filtros
                            {criteria.q !== '' && (
                                <span className="text-muted-foreground ml-1 font-normal no-underline">
                                    (se mantiene la búsqueda)
                                </span>
                            )}
                        </Link>
                    )}
                    {criteria.q !== '' && filterCount > 0 && (
                        <Link
                            href={jobsIndex()}
                            {...loading}
                            className="text-primary inline-flex min-h-9 items-center font-medium underline underline-offset-4 pointer-coarse:min-h-11"
                            data-cy="jobs-clear-all"
                        >
                            Limpiar todo
                        </Link>
                    )}
                </div>
            )}
        </div>
    );
}
