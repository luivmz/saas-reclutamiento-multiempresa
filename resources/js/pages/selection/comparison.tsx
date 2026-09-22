import { Form, Head, Link } from '@inertiajs/react';
import {
    AlertTriangle,
    Gavel,
    Lock,
    ShieldCheck,
    UserCheck,
} from 'lucide-react';
import ApplicationController from '@/actions/App/Http/Controllers/Applications/ApplicationController';
import FinalDecisionController from '@/actions/App/Http/Controllers/Selection/FinalDecisionController';
import SelectionRegistrationController from '@/actions/App/Http/Controllers/Selection/SelectionRegistrationController';
import VacancyClosureController from '@/actions/App/Http/Controllers/Selection/VacancyClosureController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { CheckCard, RadioCard } from '@/components/choice';
import { DataTable } from '@/components/data-table';
import { EmptyState } from '@/components/empty-state';
import { FormField } from '@/components/form-controls';
import InputError from '@/components/input-error';
import {
    DetailList,
    PageContainer,
    PageHeader,
    Section,
} from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime, formatNumber } from '@/lib/format';
import type { Presented, Vacancy } from '@/types';

type RankingCriterion = {
    id: number;
    name: string;
    stage: Presented;
    weight: number;
    min_score: number;
    max_score: number;
};

type RankingEntry = {
    position: number;
    application_id: number;
    candidate_name: string;
    application_status: Presented | null;
    total: number;
    tied: boolean;
    breakdown: {
        criterion_id: number;
        name: string;
        weight: number;
        average: number;
        normalized: number;
        contribution: number;
    }[];
};

type IncompleteEntry = {
    application_id: number;
    candidate_name: string;
    application_status: Presented | null;
    missing_criteria: string[];
};

type Decision = {
    application_id: number;
    candidate_name: string;
    justification: string;
    selected_position: number;
    selected_score: number;
    ranked_candidates: number;
    decided_by: string;
    decided_at: string;
    selection_registered_by: string | null;
    selection_registered_at: string | null;
} | null;

type Props = {
    vacancy: Vacancy;
    criteria: RankingCriterion[];
    ranking: { entries: RankingEntry[]; incomplete: IncompleteEntry[] };
    rankingError: string | null;
    formula: string;
    decision: Decision;
    closedBy: string | null;
    can: { decide: boolean; registerSelection: boolean; close: boolean };
};

export default function Comparison({
    vacancy,
    criteria,
    ranking,
    rankingError,
    formula,
    decision,
    closedBy,
    can,
}: Props) {
    const finalists = ranking.entries.filter(
        (entry) => entry.application_status?.value === 'finalista',
    );

    return (
        <>
            <Head title={`Comparación de ${vacancy.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono text-xs">
                                {vacancy.code}
                            </span>
                            <StatusBadge status={vacancy.status} />
                        </>
                    }
                    title={`Comparación de candidatos: ${vacancy.title}`}
                    description="Ranking ponderado y explicable de los candidatos con resultados completos (RF-21 y RF-22)."
                    actions={
                        <Button variant="outline" asChild>
                            <Link href={VacancyController.show(vacancy.id)}>
                                Ver vacante
                            </Link>
                        </Button>
                    }
                />

                <WorkflowAlert />

                {/* La advertencia que sostiene todo el módulo. Va arriba,
                    antes del ranking, no después: quien llega a esta página
                    debe leerla antes de mirar los puntajes. */}
                <Alert data-cy="human-decision-notice">
                    <ShieldCheck className="text-primary" />
                    <AlertTitle>
                        El ranking es un apoyo para la decisión
                    </AlertTitle>
                    <AlertDescription>
                        El sistema calcula y ordena puntajes, pero no selecciona
                        a ningún candidato. La decisión final la registra un
                        aprobador autorizado (RF-23).
                    </AlertDescription>
                </Alert>

                {rankingError && (
                    <Alert variant="destructive" data-cy="ranking-error">
                        <AlertTriangle />
                        <AlertTitle>No se pudo calcular el ranking</AlertTitle>
                        <AlertDescription>{rankingError}</AlertDescription>
                    </Alert>
                )}

                <Section title="Cómo se calcula">
                    <div className="space-y-3 text-sm leading-relaxed">
                        <p
                            className="bg-surface rounded-md px-3 py-2 font-mono text-xs"
                            data-cy="ranking-formula"
                        >
                            {formula}
                        </p>
                        <p className="text-muted-foreground">
                            Si un criterio tiene varios puntajes registrados, se
                            usa su promedio. Solo se incluyen resultados de
                            sesiones realizadas.
                        </p>
                        <p className="text-muted-foreground">
                            Los empates comparten la misma posición y no se
                            desempatan automáticamente.
                        </p>
                    </div>
                </Section>

                <Section title="Ranking" contentClassName="p-0 md:px-0 md:py-0">
                    {ranking.entries.length === 0 ? (
                        <div className="p-5">
                            <EmptyState
                                title="Sin candidatos con resultados completos"
                                description="El ranking aparecerá cuando existan evaluaciones y entrevistas registradas para todos los criterios."
                                className="border-0"
                            />
                        </div>
                    ) : (
                        <DataTable
                            className="rounded-none border-0 md:border-0"
                            caption={`Ranking ponderado de los candidatos de la vacante ${vacancy.code}`}
                            data-cy="ranking-table"
                            rows={ranking.entries}
                            rowKey={(row) => row.application_id}
                            rowAttributes={(row) => ({
                                'data-cy': 'ranking-row',
                                'data-position': row.position,
                            })}
                            columns={[
                                {
                                    key: 'position',
                                    header: 'Posición',
                                    cell: (row) => (
                                        <span className="flex flex-wrap items-center gap-2">
                                            <span className="bg-surface inline-flex size-8 items-center justify-center rounded-full font-mono font-medium">
                                                {row.position}
                                            </span>
                                            {row.tied && (
                                                <span
                                                    className="bg-tone-warning text-tone-warning-foreground ring-tone-warning-edge rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset"
                                                    data-cy="tie-badge"
                                                >
                                                    Empate
                                                </span>
                                            )}
                                        </span>
                                    ),
                                },
                                {
                                    key: 'candidate',
                                    header: 'Candidato',
                                    cell: (row) => (
                                        <>
                                            <Link
                                                href={ApplicationController(
                                                    row.application_id,
                                                )}
                                                className="font-medium hover:underline"
                                            >
                                                {row.candidate_name}
                                            </Link>
                                            {row.application_status && (
                                                <StatusBadge
                                                    status={
                                                        row.application_status
                                                    }
                                                    className="mt-1.5 flex w-fit"
                                                />
                                            )}
                                        </>
                                    ),
                                },
                                ...criteria.map((criterion, index) => ({
                                    key: `criterion-${criterion.id}`,
                                    label: criterion.name,
                                    align: 'end' as const,
                                    header: (
                                        <span className="block">
                                            <span className="block">
                                                {criterion.name}
                                            </span>
                                            <span className="text-muted-foreground block font-normal">
                                                Ponderación{' '}
                                                {formatNumber(criterion.weight)}
                                                , escala{' '}
                                                {formatNumber(
                                                    criterion.min_score,
                                                )}
                                                –
                                                {formatNumber(
                                                    criterion.max_score,
                                                )}
                                            </span>
                                        </span>
                                    ),
                                    cell: (row: RankingEntry) => {
                                        const item = row.breakdown[index];

                                        if (!item) {
                                            return '—';
                                        }

                                        return (
                                            <span className="tabular-nums">
                                                <span className="block font-mono">
                                                    {formatNumber(item.average)}
                                                </span>
                                                <span className="text-muted-foreground block text-xs">
                                                    aporta{' '}
                                                    {formatNumber(
                                                        item.contribution,
                                                    )}{' '}
                                                    pts
                                                </span>
                                            </span>
                                        );
                                    },
                                })),
                                {
                                    key: 'total',
                                    header: 'Total (0–100)',
                                    align: 'end',
                                    cell: (row) => (
                                        <span
                                            className="font-mono text-base font-medium tabular-nums"
                                            data-cy="ranking-total"
                                        >
                                            {formatNumber(row.total)}
                                        </span>
                                    ),
                                },
                            ]}
                        />
                    )}
                </Section>

                {ranking.incomplete.length > 0 && (
                    <Section
                        title="Candidatos sin resultados completos"
                        description="No entran al ranking hasta que se registren todos los criterios."
                        data-cy="incomplete-candidates"
                    >
                        <ul className="space-y-2">
                            {ranking.incomplete.map((candidate) => (
                                <li
                                    key={candidate.application_id}
                                    className="flex flex-wrap items-center justify-between gap-2 rounded-lg border p-3 text-sm"
                                >
                                    <Link
                                        href={ApplicationController(
                                            candidate.application_id,
                                        )}
                                        className="font-medium hover:underline"
                                    >
                                        {candidate.candidate_name}
                                    </Link>
                                    <span className="text-muted-foreground">
                                        Falta:{' '}
                                        {candidate.missing_criteria.join(', ')}
                                    </span>
                                </li>
                            ))}
                        </ul>
                    </Section>
                )}

                {can.decide && (
                    <Section
                        title={
                            <span className="flex items-center gap-2">
                                <Gavel className="size-4" aria-hidden="true" />
                                Decisión final (RF-23)
                            </span>
                        }
                        description="Elija al candidato finalista que usted decide seleccionar. Puede apartarse del orden del ranking; en todos los casos debe justificar su decisión."
                        data-cy="decision-panel"
                    >
                        {finalists.length === 0 ? (
                            <p className="text-muted-foreground text-sm">
                                No hay candidatos en etapa «Finalista» con
                                resultados completos.
                            </p>
                        ) : (
                            <Form
                                {...FinalDecisionController.form(vacancy.id)}
                                className="space-y-5"
                            >
                                {({ errors, processing }) => (
                                    <>
                                        <fieldset className="space-y-2">
                                            <legend className="mb-2 text-sm font-medium">
                                                Candidato elegido
                                            </legend>
                                            {finalists.map((entry) => (
                                                <RadioCard
                                                    key={entry.application_id}
                                                    name="application_id"
                                                    value={entry.application_id}
                                                    title={entry.candidate_name}
                                                    data-cy={`decision-candidate-${entry.application_id}`}
                                                    trailing={
                                                        <span className="text-muted-foreground shrink-0 font-mono text-xs tabular-nums">
                                                            Posición{' '}
                                                            {entry.position},{' '}
                                                            {formatNumber(
                                                                entry.total,
                                                            )}{' '}
                                                            pts
                                                        </span>
                                                    }
                                                />
                                            ))}
                                            <InputError
                                                message={errors.application_id}
                                            />
                                        </fieldset>

                                        <FormField
                                            label="Justificación de la decisión"
                                            htmlFor="justification"
                                            error={errors.justification}
                                            required
                                        >
                                            <Textarea
                                                id="justification"
                                                name="justification"
                                                rows={3}
                                                data-cy="decision-justification"
                                            />
                                        </FormField>

                                        <div className="space-y-2">
                                            <CheckCard
                                                name="human_confirmation"
                                                data-cy="decision-human-confirmation"
                                            >
                                                Confirmo que tomo esta decisión
                                                como responsable autorizado. El
                                                ranking es solo información de
                                                apoyo.
                                            </CheckCard>
                                            <InputError
                                                message={
                                                    errors.human_confirmation
                                                }
                                            />
                                        </div>

                                        <Button
                                            type="submit"
                                            disabled={processing}
                                            data-cy="submit-final-decision"
                                        >
                                            {processing && <Spinner />}
                                            Registrar decisión final
                                        </Button>
                                    </>
                                )}
                            </Form>
                        )}
                    </Section>
                )}

                {decision && (
                    <Section
                        title={
                            <span className="flex items-center gap-2">
                                <UserCheck
                                    className="size-4"
                                    aria-hidden="true"
                                />
                                Decisión final registrada
                            </span>
                        }
                        description="Tomada por una persona autorizada; el sistema solo la registra."
                        data-cy="decision-summary"
                    >
                        <div className="space-y-5">
                            <DetailList
                                items={[
                                    {
                                        label: 'Candidato elegido',
                                        value: decision.candidate_name,
                                    },
                                    {
                                        label: 'Posición en el ranking al decidir',
                                        value: `${decision.selected_position} de ${decision.ranked_candidates}, con ${formatNumber(decision.selected_score)} pts`,
                                    },
                                    {
                                        label: 'Decidido por',
                                        value: decision.decided_by,
                                    },
                                    {
                                        label: 'Fecha de decisión',
                                        value: formatDateTime(
                                            decision.decided_at,
                                        ),
                                    },
                                    {
                                        label: 'Selección registrada por',
                                        value:
                                            decision.selection_registered_by ??
                                            'Pendiente (RR. HH.)',
                                    },
                                    {
                                        label: 'Fecha de registro de selección',
                                        value: formatDateTime(
                                            decision.selection_registered_at,
                                        ),
                                    },
                                ]}
                            />
                            <blockquote className="bg-surface border-primary rounded-md border-l-2 px-4 py-3 text-sm leading-relaxed whitespace-pre-line">
                                {decision.justification}
                            </blockquote>
                            {can.registerSelection && (
                                <Form
                                    {...SelectionRegistrationController.form(
                                        vacancy.id,
                                    )}
                                >
                                    {({ processing }) => (
                                        <Button
                                            type="submit"
                                            disabled={processing}
                                            data-cy="register-selection"
                                        >
                                            {processing && <Spinner />}
                                            Registrar selección del candidato
                                            (RF-24)
                                        </Button>
                                    )}
                                </Form>
                            )}
                        </div>
                    </Section>
                )}

                {can.close && (
                    <Section
                        title={
                            <span className="flex items-center gap-2">
                                <Lock className="size-4" aria-hidden="true" />
                                Cerrar convocatoria (RF-25)
                            </span>
                        }
                        description="Las demás postulaciones activas pasarán a «No seleccionado» y la vacante no admitirá más cambios."
                        data-cy="closure-panel"
                    >
                        <Form
                            {...VacancyClosureController.form(vacancy.id)}
                            className="space-y-4"
                        >
                            {({ errors, processing }) => (
                                <>
                                    <FormField
                                        label="Notas de cierre (opcional)"
                                        htmlFor="closure_notes"
                                        error={errors.closure_notes}
                                    >
                                        <Textarea
                                            id="closure_notes"
                                            name="closure_notes"
                                            rows={2}
                                            data-cy="closure-notes"
                                        />
                                    </FormField>
                                    <Button
                                        type="submit"
                                        variant="destructive"
                                        disabled={processing}
                                        data-cy="close-vacancy"
                                    >
                                        {processing && <Spinner />}
                                        Cerrar convocatoria
                                    </Button>
                                </>
                            )}
                        </Form>
                    </Section>
                )}

                {vacancy.status.value === 'cerrada' && (
                    <p
                        className="bg-surface text-surface-foreground flex flex-wrap items-center gap-2 rounded-xl border border-dashed px-5 py-4 text-sm"
                        data-cy="closure-summary"
                    >
                        <Lock className="size-4" aria-hidden="true" />
                        Convocatoria cerrada el{' '}
                        {formatDateTime(vacancy.closed_at)}
                        {closedBy && <> por {closedBy}</>}
                        {vacancy.closure_type && (
                            <StatusBadge status={vacancy.closure_type} />
                        )}
                        {vacancy.closure_notes && (
                            <span className="text-muted-foreground">
                                {vacancy.closure_notes}
                            </span>
                        )}
                    </p>
                )}
            </PageContainer>
        </>
    );
}

Comparison.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Comparación', href: VacancyController.index() },
    ],
};
