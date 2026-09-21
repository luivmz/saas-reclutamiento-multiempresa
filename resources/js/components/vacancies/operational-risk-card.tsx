import { useEffect, useState } from 'react';
import { Activity, Info } from 'lucide-react';

import { Badge } from '@/components/ui/badge';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { formatDateTime } from '@/lib/format';

/**
 * Riesgo operacional del **proceso** de una vacante (Fase 16).
 *
 * Lo que esta tarjeta no hace, y no debe hacer nunca: no ordena candidatos, no
 * puntúa personas, no recomienda contratar ni descartar y no dispara ninguna
 * acción. Es una señal para que alguien mire el proceso; la decisión final es
 * humana (RF-23).
 *
 * El tono es deliberadamente neutro. La tasa de alerta del modelo es alta
 * —73.5 % en el conjunto de prueba—, así que presentar la señal como una
 * alarma crítica sería desproporcionado respecto de lo que mide.
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

export function OperationalRiskCard({ vacancyId }: Props) {
    const [risk, setRisk] = useState<RiskPayload | null>(null);
    const [failed, setFailed] = useState(false);

    useEffect(() => {
        let cancelled = false;

        fetch(`/vacantes/${vacancyId}/riesgo-operacional`, {
            headers: { Accept: 'application/json' },
        })
            .then((response) => (response.ok ? response.json() : Promise.reject(response.status)))
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
        <Card data-cy="operational-risk-panel">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Activity className="size-5" />
                    Riesgo operacional del proceso
                </CardTitle>
                <CardDescription>
                    Estimación experimental sobre el <strong>proceso</strong>, no sobre las personas
                    postulantes. No es una decisión ni una recomendación.
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
                {failed && (
                    <p className="text-muted-foreground" data-cy="operational-risk-failed">
                        No se pudo consultar la estimación. Los indicadores descriptivos del proceso
                        siguen vigentes.
                    </p>
                )}

                {!failed && risk === null && (
                    <p className="text-muted-foreground">Consultando…</p>
                )}

                {risk !== null && (
                    <>
                        <div className="flex flex-wrap items-center gap-2">
                            <Badge variant={predictive ? 'default' : 'secondary'} data-cy="operational-risk-availability">
                                {risk.label}
                            </Badge>
                            <Badge variant="outline">Experimental</Badge>
                            {predictive && risk.risk_flag !== null && (
                                <Badge
                                    variant={risk.risk_flag ? 'outline' : 'secondary'}
                                    data-cy="operational-risk-flag"
                                >
                                    {risk.risk_flag ? 'Señal de riesgo para revisión' : 'Sin señal de riesgo'}
                                </Badge>
                            )}
                        </div>

                        {predictive && risk.risk_percentage !== null && (
                            <p data-cy="operational-risk-score">
                                <span className="text-2xl font-semibold tabular-nums">
                                    {risk.risk_percentage.toLocaleString('es-PE', {
                                        minimumFractionDigits: 1,
                                        maximumFractionDigits: 1,
                                    })}
                                    %
                                </span>{' '}
                                <span className="text-muted-foreground">
                                    riesgo estimado de retraso del proceso
                                </span>
                            </p>
                        )}

                        <p className="text-muted-foreground" data-cy="operational-risk-message">
                            {risk.message}
                        </p>

                        <p className="text-muted-foreground flex items-start gap-2 text-xs">
                            <Info className="mt-0.5 size-4 shrink-0" />
                            <span>
                                Modelo entrenado con datos sintéticos y validado solo en ese entorno.
                                La decisión final corresponde al Aprobador/Dirección, con
                                justificación explícita.
                                {risk.checked_at && ` · Consultado ${formatDateTime(risk.checked_at)}`}
                            </span>
                        </p>
                    </>
                )}
            </CardContent>
        </Card>
    );
}
