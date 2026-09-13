import { Form, Head, Link } from '@inertiajs/react';
import { AlertTriangle, Gavel, Lock, Scale, ShieldCheck, UserCheck } from 'lucide-react';
import ApplicationController from '@/actions/App/Http/Controllers/Applications/ApplicationController';
import FinalDecisionController from '@/actions/App/Http/Controllers/Selection/FinalDecisionController';
import SelectionRegistrationController from '@/actions/App/Http/Controllers/Selection/SelectionRegistrationController';
import VacancyClosureController from '@/actions/App/Http/Controllers/Selection/VacancyClosureController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { EmptyState } from '@/components/empty-state';
import { FormField } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { DetailList, PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
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

export default function Comparison({ vacancy, criteria, ranking, rankingError, formula, decision, closedBy, can }: Props) {
    const finalists = ranking.entries.filter((entry) => entry.application_status?.value === 'finalista');

    return (
        <>
            <Head title={`Comparación · ${vacancy.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono">{vacancy.code}</span>
                            <StatusBadge status={vacancy.status} />
                        </>
                    }
                    title={`Comparación de candidatos: ${vacancy.title}`}
                    description="RF-21 y RF-22 · Ranking ponderado y explicable de los candidatos con resultados completos."
                    actions={
                        <Button variant="outline" asChild>
                            <Link href={VacancyController.show(vacancy.id)}>Ver vacante</Link>
                        </Button>
                    }
                />

                <WorkflowAlert />

                <Alert data-cy="human-decision-notice">
                    <ShieldCheck className="text-emerald-600" />
                    <AlertTitle>El ranking es un apoyo para la decisión</AlertTitle>
                    <AlertDescription>
                        El sistema calcula y ordena puntajes, pero no selecciona a ningún candidato. La decisión final la registra un aprobador autorizado (RF-23).
                    </AlertDescription>
                </Alert>

                {rankingError && (
                    <Alert variant="destructive" data-cy="ranking-error">
                        <AlertTriangle />
                        <AlertTitle>No se pudo calcular el ranking</AlertTitle>
                        <AlertDescription>{rankingError}</AlertDescription>
                    </Alert>
                )}

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Scale className="size-5" />
                            Cómo se calcula
                        </CardTitle>
                        <CardDescription data-cy="ranking-formula">{formula}</CardDescription>
                    </CardHeader>
                    <CardContent className="text-muted-foreground space-y-1 text-sm">
                        <p>Si un criterio tiene varios puntajes registrados, se usa su promedio. Solo se incluyen resultados de sesiones realizadas.</p>
                        <p>Los empates comparten la misma posición y no se desempatan automáticamente.</p>
                    </CardContent>
                </Card>

                <Card className="gap-0 overflow-hidden py-0">
                    <CardHeader className="border-b py-4">
                        <CardTitle>Ranking</CardTitle>
                    </CardHeader>
                    {ranking.entries.length === 0 ? (
                        <CardContent className="py-6">
                            <EmptyState title="Sin candidatos con resultados completos" description="El ranking aparecerá cuando existan evaluaciones y entrevistas registradas para todos los criterios." />
                        </CardContent>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm" data-cy="ranking-table">
                                <thead className="bg-muted/50 text-muted-foreground text-left text-xs tracking-wide uppercase">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Posición</th>
                                        <th className="px-4 py-3 font-medium">Candidato</th>
                                        {criteria.map((criterion) => (
                                            <th key={criterion.id} className="px-4 py-3 text-right font-medium">
                                                <span className="block normal-case">{criterion.name}</span>
                                                <span className="font-normal normal-case">
                                                    Pond. {formatNumber(criterion.weight)} · {formatNumber(criterion.min_score)}–{formatNumber(criterion.max_score)}
                                                </span>
                                            </th>
                                        ))}
                                        <th className="px-4 py-3 text-right font-medium">Total (0–100)</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {ranking.entries.map((entry) => (
                                        <tr key={entry.application_id} data-cy="ranking-row" data-position={entry.position}>
                                            <td className="px-4 py-3">
                                                <span className="bg-muted inline-flex size-8 items-center justify-center rounded-full font-semibold">{entry.position}</span>
                                                {entry.tied && (
                                                    <span className="ml-2 rounded-full bg-amber-50 px-2 py-0.5 text-xs text-amber-800 dark:bg-amber-950/60 dark:text-amber-300" data-cy="tie-badge">
                                                        Empate
                                                    </span>
                                                )}
                                            </td>
                                            <td className="px-4 py-3">
                                                <Link href={ApplicationController(entry.application_id)} className="font-medium hover:underline">
                                                    {entry.candidate_name}
                                                </Link>
                                                {entry.application_status && <StatusBadge status={entry.application_status} className="mt-1 block w-fit" />}
                                            </td>
                                            {entry.breakdown.map((item) => (
                                                <td key={item.criterion_id} className="px-4 py-3 text-right tabular-nums">
                                                    <span className="block">{formatNumber(item.average)}</span>
                                                    <span className="text-muted-foreground text-xs">+{formatNumber(item.contribution)} pts</span>
                                                </td>
                                            ))}
                                            <td className="px-4 py-3 text-right text-base font-semibold tabular-nums" data-cy="ranking-total">
                                                {formatNumber(entry.total)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </Card>

                {ranking.incomplete.length > 0 && (
                    <Card data-cy="incomplete-candidates">
                        <CardHeader>
                            <CardTitle>Candidatos sin resultados completos</CardTitle>
                            <CardDescription>No se incluyen en el ranking hasta registrar todos los criterios.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            {ranking.incomplete.map((candidate) => (
                                <div key={candidate.application_id} className="flex flex-wrap items-center justify-between gap-2 rounded-lg border p-3 text-sm">
                                    <Link href={ApplicationController(candidate.application_id)} className="font-medium hover:underline">
                                        {candidate.candidate_name}
                                    </Link>
                                    <span className="text-muted-foreground">Falta: {candidate.missing_criteria.join(', ')}</span>
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                )}

                {can.decide && (
                    <Card data-cy="decision-panel">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Gavel className="size-5" />
                                Decisión final (RF-23)
                            </CardTitle>
                            <CardDescription>
                                Elija al candidato finalista que usted decide seleccionar. Puede apartarse del orden del ranking; en todos los casos debe justificar su decisión.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            {finalists.length === 0 ? (
                                <p className="text-muted-foreground text-sm">No hay candidatos en etapa «Finalista» con resultados completos.</p>
                            ) : (
                                <Form {...FinalDecisionController.form(vacancy.id)} className="space-y-4">
                                    {({ errors, processing }) => (
                                        <>
                                            <fieldset className="space-y-2">
                                                <legend className="mb-2 text-sm font-medium">Candidato elegido</legend>
                                                {finalists.map((entry) => (
                                                    <label key={entry.application_id} className="has-[:checked]:border-primary has-[:checked]:bg-primary/5 flex cursor-pointer items-center gap-3 rounded-lg border p-3 text-sm">
                                                        <input type="radio" name="application_id" value={entry.application_id} data-cy={`decision-candidate-${entry.application_id}`} />
                                                        <span className="flex-1 font-medium">{entry.candidate_name}</span>
                                                        <span className="text-muted-foreground tabular-nums">
                                                            Posición {entry.position} · {formatNumber(entry.total)} pts
                                                        </span>
                                                    </label>
                                                ))}
                                                <InputError message={errors.application_id} />
                                            </fieldset>
                                            <FormField label="Justificación de la decisión" htmlFor="justification" error={errors.justification}>
                                                <Textarea id="justification" name="justification" rows={3} data-cy="decision-justification" />
                                            </FormField>
                                            <label className="flex items-start gap-3 rounded-lg border border-dashed p-3 text-sm">
                                                <input type="checkbox" name="human_confirmation" value="1" className="mt-1" data-cy="decision-human-confirmation" />
                                                <span>Confirmo que tomo esta decisión como responsable autorizado. El ranking es solo información de apoyo.</span>
                                            </label>
                                            <InputError message={errors.human_confirmation} />
                                            <Button type="submit" disabled={processing} data-cy="submit-final-decision">
                                                {processing && <Spinner />}
                                                Registrar decisión final
                                            </Button>
                                        </>
                                    )}
                                </Form>
                            )}
                        </CardContent>
                    </Card>
                )}

                {decision && (
                    <Card data-cy="decision-summary">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <UserCheck className="size-5" />
                                Decisión final registrada
                            </CardTitle>
                            <CardDescription>Tomada por una persona autorizada; el sistema solo la registra.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <DetailList
                                items={[
                                    { label: 'Candidato elegido', value: decision.candidate_name },
                                    { label: 'Posición en el ranking al decidir', value: `${decision.selected_position} de ${decision.ranked_candidates} (${formatNumber(decision.selected_score)} pts)` },
                                    { label: 'Decidido por', value: decision.decided_by },
                                    { label: 'Fecha de decisión', value: formatDateTime(decision.decided_at) },
                                    { label: 'Selección registrada por', value: decision.selection_registered_by ?? 'Pendiente (RR. HH.)' },
                                    { label: 'Fecha de registro de selección', value: formatDateTime(decision.selection_registered_at) },
                                ]}
                            />
                            <p className="bg-muted/60 rounded-md px-3 py-2 text-sm whitespace-pre-line">{decision.justification}</p>
                            {can.registerSelection && (
                                <Form {...SelectionRegistrationController.form(vacancy.id)}>
                                    {({ processing }) => (
                                        <Button type="submit" disabled={processing} data-cy="register-selection">
                                            {processing && <Spinner />}
                                            Registrar selección del candidato (RF-24)
                                        </Button>
                                    )}
                                </Form>
                            )}
                        </CardContent>
                    </Card>
                )}

                {can.close && (
                    <Card data-cy="closure-panel">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Lock className="size-5" />
                                Cerrar convocatoria (RF-25)
                            </CardTitle>
                            <CardDescription>
                                Las demás postulaciones activas pasarán a «No seleccionado» y la vacante no admitirá más cambios.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Form {...VacancyClosureController.form(vacancy.id)} className="space-y-3">
                                {({ errors, processing }) => (
                                    <>
                                        <FormField label="Notas de cierre (opcional)" htmlFor="closure_notes" error={errors.closure_notes}>
                                            <Textarea id="closure_notes" name="closure_notes" rows={2} data-cy="closure-notes" />
                                        </FormField>
                                        <Button type="submit" variant="destructive" disabled={processing} data-cy="close-vacancy">
                                            {processing && <Spinner />}
                                            Cerrar convocatoria
                                        </Button>
                                    </>
                                )}
                            </Form>
                        </CardContent>
                    </Card>
                )}

                {vacancy.status.value === 'cerrada' && (
                    <Card className="bg-muted/30 border-dashed" data-cy="closure-summary">
                        <CardContent className="flex flex-wrap items-center gap-3 text-sm">
                            <Lock className="size-4" />
                            Convocatoria cerrada el {formatDateTime(vacancy.closed_at)}
                            {closedBy && <> por {closedBy}</>}
                            {vacancy.closure_type && <StatusBadge status={vacancy.closure_type} />}
                            {vacancy.closure_notes && <span className="text-muted-foreground">· {vacancy.closure_notes}</span>}
                        </CardContent>
                    </Card>
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
