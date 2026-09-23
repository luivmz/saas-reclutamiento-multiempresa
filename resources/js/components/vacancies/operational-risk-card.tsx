import { useEffect, useState } from 'react';
import { Activity, Info } from 'lucide-react';

import { Section } from '@/components/page';
import { Skeleton } from '@/components/ui/skeleton';
import { formatDateTime } from '@/lib/format';
import { cn } from '@/lib/utils';

/**
 * Riesgo operacional del **proceso** de una vacante (Fase 16).
 *
 * Lo que esta tarjeta no hace, y no debe hacer nunca: no ordena candidatos, no
 * puntúa personas, no recomienda contratar ni descartar y no dispara ninguna
 * acción. Es una señal para que alguien mire el proceso; la decisión final es
 * humana (RF-23).
 *
 * El tono es deliberadamente neutro, y el rediseño de la Fase 18 lo sostiene:
 * la cifra se muestra en el tono informativo, nunca en el de peligro. La tasa
 * de alerta del modelo es alta —73.5 % en el conjunto de prueba—, así que
 * pintarla de rojo sería desproporcionado respecto de lo que mide.
 */

type RiskPayload = {
    availability: 'predictive_available' | 'descriptive_only' | 'unavailable';
    reason: string;
    risk_score: number | null;
    risk_percentage: number | null;
    risk_flag: boolean | null;
    threshold: number | null;
    model_version: string | null;
    freeze_fingerprint: string | null;
    checked_at: string;
    is_experimental: boolean;
    message: string;
    label: string;
};

type Props = {
    vacancyId: number;
};

const chip =
    'inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset';

export function OperationalRiskCard({ vacancyId }: Props) {
    const [risk, setRisk] = useState<RiskPayload | null>(null);
    const [failed, setFailed] = useState(false);

    useEffect(() => {
        let cancelled = false;

        fetch(`/vacantes/${vacancyId}/riesgo-operacional`, {
            headers: { Accept: 'application/json' },
        })
            .then((response) =>
                response.ok ? response.json() : Promise.reject(response.status),
            )
            .then((data: { risk: RiskPayload }) => {
                if (!cancelled) {
                    setRisk(data.risk);
                }
            })
            .catch(() => {
                if (!cancelled) {
                    setFailed(true);
                }
            });

        return () => {
            cancelled = true;
        };
    }, [vacancyId]);

    const predictive = risk?.availability === 'predictive_available';

    return (
        <Section
            data-cy="operational-risk-panel"
            title={
                <span className="flex items-center gap-2">
                    <Activity className="size-4" aria-hidden="true" />
                    Riesgo operacional del proceso
                </span>
            }
            description="Estimación experimental sobre el proceso, no sobre las personas postulantes. No es una decisión ni una recomendación."
        >
            <div className="space-y-4 text-sm" aria-live="polite">
                {failed && (
                    <p
                        className="text-muted-foreground"
                        data-cy="operational-risk-failed"
                    >
                        No se pudo consultar la estimación. Los indicadores
                        descriptivos del proceso siguen vigentes.
                    </p>
                )}

                {!failed && risk === null && (
                    <div className="space-y-3">
                        <Skeleton className="h-5 w-40" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-3/4" />
                        <span className="sr-only">
                            Consultando la estimación…
                        </span>
                    </div>
                )}

                {risk !== null && (
                    <div className="animate-in fade-in-0 space-y-4 duration-200 ease-out">
                        <div className="flex flex-wrap items-center gap-2">
                            <span
                                className={cn(
                                    chip,
                                    predictive
                                        ? 'bg-tone-primary text-tone-primary-foreground ring-tone-primary-edge'
                                        : 'bg-tone-neutral text-tone-neutral-foreground ring-tone-neutral-edge',
                                )}
                                data-cy="operational-risk-availability"
                            >
                                {risk.label}
                            </span>
                            <span
                                className={cn(
                                    chip,
                                    'bg-tone-warning text-tone-warning-foreground ring-tone-warning-edge',
                                )}
                            >
                                Experimental
                            </span>
                            {predictive && risk.risk_flag !== null && (
                                <span
                                    className={cn(
                                        chip,
                                        risk.risk_flag
                                            ? 'bg-tone-info text-tone-info-foreground ring-tone-info-edge'
                                            : 'bg-tone-neutral text-tone-neutral-foreground ring-tone-neutral-edge',
                                    )}
                                    data-cy="operational-risk-flag"
                                >
                                    {risk.risk_flag
                                        ? 'Señal de riesgo para revisión'
                                        : 'Sin señal de riesgo'}
                                </span>
                            )}
                        </div>

                        {predictive && risk.risk_percentage !== null && (
                            <p data-cy="operational-risk-score">
                                <span className="font-mono text-3xl leading-none font-medium tabular-nums">
                                    {risk.risk_percentage.toLocaleString(
                                        'es-PE',
                                        {
                                            minimumFractionDigits: 1,
                                            maximumFractionDigits: 1,
                                        },
                                    )}
                                    %
                                </span>
                                <span className="text-muted-foreground mt-1.5 block text-xs leading-relaxed">
                                    riesgo estimado de retraso del proceso
                                </span>
                            </p>
                        )}

                        <p
                            className="text-muted-foreground leading-relaxed"
                            data-cy="operational-risk-message"
                        >
                            {risk.message}
                        </p>

                        <p className="text-muted-foreground flex items-start gap-2 border-t pt-4 text-xs leading-relaxed">
                            <Info
                                className="mt-0.5 size-4 shrink-0"
                                aria-hidden="true"
                            />
                            <span>
                                Modelo entrenado con datos sintéticos y validado
                                solo en ese entorno. La decisión final
                                corresponde al Aprobador/Dirección, con
                                justificación explícita.
                                {risk.checked_at &&
                                    ` Consultado el ${formatDateTime(risk.checked_at)}`}
                            </span>
                        </p>
                    </div>
                )}
            </div>
        </Section>
    );
}
