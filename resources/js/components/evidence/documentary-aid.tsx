import { Form } from '@inertiajs/react';
import { Search, SearchX, WifiOff } from 'lucide-react';
import { useState } from 'react';
import ApplicationEvidenceController from '@/actions/App/Http/Controllers/Evidence/ApplicationEvidenceController';
import { EvidenceFragmentCard } from '@/components/evidence/evidence-fragment';
import { FormField, NativeSelect } from '@/components/form-controls';
import { Section } from '@/components/page';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import type {
    DocumentaryAidResult,
    EvidenceSearchResult,
    Presented,
} from '@/types';

/**
 * Ayuda documental ML-02 (experimental): fragmentos de las evidencias
 * vigentes de UNA postulación por criterio, con su fuente, y una búsqueda
 * exacta. Ordena fragmentos para una consulta; nunca ordena, puntúa ni
 * recomienda personas.
 */
export function DocumentaryAid({
    applicationId,
    criteria,
    aid,
    search,
    filters,
}: {
    applicationId: number;
    criteria: Presented[];
    aid: DocumentaryAidResult | null;
    search: EvidenceSearchResult | null;
    filters: { criterio: number | null; buscar: string | null };
}) {
    const route = ApplicationEvidenceController.index(applicationId);
    const [busy, setBusy] = useState<AidForm | null>(null);
    const [failed, setFailed] = useState<AidForm | null>(null);

    /**
     * APP-M02. Las dos consultas son GET a esta misma página. Con la opción por defecto de Inertia para GET
     * (preserveState: false), cada respuesta remontaba la página entera: el foco caía al cuerpo, el desplazamiento
     * volvía arriba y, con dos envíos solapados (doble clic o Enter), la segunda respuesta sustituía el select
     * mientras se elegía otro criterio, perdiendo la elección. Ahora la página se conserva montada y la sección
     * indica la consulta en curso y el fallo de red o del servidor, con un aviso propio y el control usable.
     */
    const visit = (form: AidForm) => ({
        onStart: () => {
            setFailed(null);
            setBusy(form);
        },
        onFinish: () => setBusy(null),
        options: {
            preserveState: true,
            preserveScroll: true,
            onNetworkError: () => {
                setFailed(form);

                return false;
            },
            onHttpException: () => {
                setFailed(form);

                return false;
            },
        },
    });

    return (
        <Section
            title="Ayuda documental"
            description="ML-02 experimental. Muestra qué fragmentos de las evidencias vigentes comparten palabras con un criterio. No evalúa a nadie."
            className="h-fit"
            aria-busy={busy !== null || undefined}
            data-cy="documentary-aid"
        >
            <div className="space-y-6">
                <Form
                    action={route.url}
                    method="get"
                    className="space-y-3"
                    {...visit('aid')}
                    data-cy="aid-form"
                >
                    <FormField
                        label="Criterio de la vacante"
                        htmlFor="criterio"
                    >
                        <NativeSelect
                            id="criterio"
                            name="criterio"
                            options={criteria}
                            placeholder="Seleccione un criterio…"
                            defaultValue={
                                filters.criterio ? String(filters.criterio) : ''
                            }
                            required
                            data-cy="aid-criterion"
                        />
                    </FormField>
                    <Button
                        type="submit"
                        variant="outline"
                        className="w-full"
                        disabled={criteria.length === 0}
                        data-cy="aid-submit"
                    >
                        {busy === 'aid' ? (
                            <Spinner aria-label="Consultando la ayuda documental" />
                        ) : (
                            <Search aria-hidden="true" />
                        )}
                        Ver fragmentos
                    </Button>
                </Form>

                {failed === 'aid' && <FailedQuery data-cy="aid-error" />}

                {criteria.length === 0 && (
                    <p className="text-muted-foreground text-sm">
                        La vacante no tiene criterios configurados.
                    </p>
                )}

                {aid && (
                    <div
                        className="space-y-3"
                        aria-live="polite"
                        data-cy="aid-results"
                    >
                        <h3 className="text-sm font-semibold">
                            Fragmentos para «{aid.criterion.name}»
                        </h3>
                        {aid.abstained ? (
                            <div
                                className="text-muted-foreground flex gap-3 rounded-lg border border-dashed p-3 text-sm"
                                data-cy="aid-abstained"
                            >
                                <SearchX
                                    className="mt-0.5 size-4 shrink-0"
                                    aria-hidden="true"
                                />
                                <p>
                                    Ninguna evidencia vigente comparte palabras
                                    con este criterio. Eso no significa que el
                                    criterio no se cumpla: la ayuda solo compara
                                    palabras.
                                </p>
                            </div>
                        ) : (
                            <ol className="space-y-2">
                                {aid.results.map((fragment, index) => (
                                    <li key={fragment.id}>
                                        <EvidenceFragmentCard
                                            fragment={fragment}
                                            rank={index + 1}
                                        />
                                    </li>
                                ))}
                            </ol>
                        )}
                        <p className="text-muted-foreground text-xs leading-relaxed">
                            Método: recuperación léxica BM25 ({aid.method}),
                            hasta {aid.k} fragmentos de esta postulación,
                            ordenados por palabras compartidas con el criterio.
                            Términos buscados:{' '}
                            {aid.query_terms.length > 0
                                ? aid.query_terms.join(', ')
                                : 'ninguno'}
                            . No usa modelos entrenados ni datos de otros
                            postulantes, y no alimenta el ranking ni la
                            decisión, que corresponde a Dirección (RF-23).
                        </p>
                    </div>
                )}

                <Form
                    action={route.url}
                    method="get"
                    className="space-y-3 border-t pt-4"
                    {...visit('search')}
                    data-cy="search-form"
                >
                    <FormField
                        label="Buscar en las evidencias"
                        htmlFor="buscar"
                        hint="Búsqueda exacta, sin distinguir mayúsculas ni tildes."
                    >
                        <Input
                            id="buscar"
                            name="buscar"
                            type="search"
                            maxLength={120}
                            defaultValue={filters.buscar ?? ''}
                            required
                            data-cy="search-input"
                        />
                    </FormField>
                    <Button
                        type="submit"
                        variant="outline"
                        className="w-full"
                        data-cy="search-submit"
                    >
                        {busy === 'search' ? (
                            <Spinner aria-label="Buscando en las evidencias" />
                        ) : (
                            <Search aria-hidden="true" />
                        )}
                        Buscar
                    </Button>
                </Form>

                {failed === 'search' && <FailedQuery data-cy="search-error" />}

                {search && (
                    <div
                        className="space-y-2"
                        aria-live="polite"
                        data-cy="search-results"
                    >
                        <h3 className="text-sm font-semibold">
                            Resultados para «{search.query}»
                        </h3>
                        {search.results.length === 0 ? (
                            <p className="text-muted-foreground text-sm">
                                Sin coincidencias en las evidencias vigentes.
                            </p>
                        ) : (
                            search.results.map((fragment) => (
                                <EvidenceFragmentCard
                                    key={fragment.id}
                                    fragment={fragment}
                                />
                            ))
                        )}
                    </div>
                )}
            </div>
        </Section>
    );
}

type AidForm = 'aid' | 'search';

function FailedQuery({ 'data-cy': dataCy }: { 'data-cy': string }) {
    return (
        <Alert variant="destructive" data-cy={dataCy}>
            <WifiOff aria-hidden="true" />
            <AlertDescription>
                No se pudo consultar la ayuda documental. Las evidencias
                registradas no cambiaron; vuelva a intentarlo.
            </AlertDescription>
        </Alert>
    );
}
