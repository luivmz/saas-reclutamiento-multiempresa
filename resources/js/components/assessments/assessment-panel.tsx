import { Form } from '@inertiajs/react';
import { CalendarPlus, MapPin, User } from 'lucide-react';
import AssessmentScheduleController from '@/actions/App/Http/Controllers/Assessments/AssessmentScheduleController';
import { FormField, NativeSelect } from '@/components/form-controls';
import { Section } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime, formatNumber } from '@/lib/format';
import type { AssessmentSummary, Presented } from '@/types';

export type SchedulingOptions = {
    evaluators: { value: string; label: string }[];
    evaluationTypes: Presented[];
    modalities: Presented[];
} | null;

/**
 * Una sesión de evaluación o entrevista.
 *
 * Los datos logísticos —cuándo, dónde, con quién— se leen como una ficha de
 * citación, no como una cadena de fragmentos separados por puntos medios.
 */
function SessionItem({ session }: { session: AssessmentSummary }) {
    return (
        <article
            className="space-y-3 rounded-lg border p-4"
            data-cy="assessment-item"
            data-kind={session.kind.value}
            data-status={session.status.value}
        >
            <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="font-medium">{session.title}</h3>
                <StatusBadge status={session.status} />
            </div>

            <dl className="text-muted-foreground grid gap-1.5 text-sm">
                <div className="flex items-center gap-2">
                    <CalendarPlus
                        className="size-3.5 shrink-0"
                        aria-hidden="true"
                    />
                    <dt className="sr-only">Fecha y hora</dt>
                    <dd>{formatDateTime(session.scheduled_at)}</dd>
                </div>
                <div className="flex items-center gap-2">
                    <MapPin className="size-3.5 shrink-0" aria-hidden="true" />
                    <dt className="sr-only">Modalidad y lugar</dt>
                    <dd>
                        {session.modality.label}, {session.location}
                    </dd>
                </div>
                <div className="flex items-center gap-2">
                    <User className="size-3.5 shrink-0" aria-hidden="true" />
                    <dt className="sr-only">Evaluador</dt>
                    <dd>{session.evaluator}</dd>
                </div>
            </dl>

            {session.results && session.results.length > 0 && (
                <table className="w-full border-t text-sm">
                    <caption className="sr-only">
                        Puntajes registrados en la sesión
                    </caption>
                    <tbody className="divide-y">
                        {session.results.map((result) => (
                            <tr key={result.criterion}>
                                <th
                                    scope="row"
                                    className="py-1.5 text-left font-normal"
                                >
                                    {result.criterion}
                                </th>
                                <td className="py-1.5 text-right font-mono tabular-nums">
                                    {formatNumber(result.score)} /{' '}
                                    {formatNumber(result.max_score)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {session.outcome && (
                <p className="flex flex-wrap items-center gap-2 text-sm">
                    Resultado: <StatusBadge status={session.outcome} />
                </p>
            )}

            {session.observations && (
                <p className="bg-surface rounded-md px-3 py-2 text-sm leading-relaxed">
                    {session.observations}
                </p>
            )}
        </article>
    );
}

function ScheduleForm({
    kind,
    applicationId,
    options,
}: {
    kind: 'evaluacion' | 'entrevista';
    applicationId: number;
    options: NonNullable<SchedulingOptions>;
}) {
    const action =
        kind === 'evaluacion'
            ? AssessmentScheduleController.evaluation.form(applicationId)
            : AssessmentScheduleController.interview.form(applicationId);

    if (options.evaluators.length === 0) {
        return (
            <p className="text-muted-foreground text-sm">
                No hay evaluadores registrados en la organización.
            </p>
        );
    }

    return (
        <Form
            {...action}
            resetOnSuccess
            options={{ preserveScroll: true }}
            className="grid gap-4 rounded-lg border border-dashed p-4 md:grid-cols-2"
            data-cy={`schedule-${kind}-form`}
        >
            {({ errors, processing }) => (
                <>
                    <p className="text-sm font-medium md:col-span-2">
                        {kind === 'evaluacion'
                            ? 'Programar una evaluación'
                            : 'Programar una entrevista'}
                    </p>
                    <FormField
                        label="Evaluador responsable"
                        htmlFor={`${kind}-evaluator`}
                        error={errors.evaluator_id}
                    >
                        <NativeSelect
                            id={`${kind}-evaluator`}
                            name="evaluator_id"
                            options={options.evaluators}
                            placeholder="Seleccione…"
                            data-cy={`${kind}-evaluator`}
                        />
                    </FormField>
                    {kind === 'evaluacion' && (
                        <FormField
                            label="Tipo de evaluación"
                            htmlFor="evaluation-type"
                            error={errors.type}
                        >
                            <NativeSelect
                                id="evaluation-type"
                                name="type"
                                options={options.evaluationTypes}
                                placeholder="Seleccione…"
                                data-cy="evaluacion-type"
                            />
                        </FormField>
                    )}
                    <FormField
                        label="Fecha y hora"
                        htmlFor={`${kind}-scheduled-at`}
                        error={errors.scheduled_at}
                    >
                        <Input
                            id={`${kind}-scheduled-at`}
                            name="scheduled_at"
                            type="datetime-local"
                            data-cy={`${kind}-scheduled-at`}
                        />
                    </FormField>
                    <FormField
                        label="Duración en minutos"
                        htmlFor={`${kind}-duration`}
                        error={errors.duration_minutes}
                        hint="Opcional. Entre 15 y 480 minutos."
                    >
                        <Input
                            id={`${kind}-duration`}
                            name="duration_minutes"
                            type="number"
                            min={15}
                            max={480}
                            data-cy={`${kind}-duration`}
                        />
                    </FormField>
                    <FormField
                        label="Modalidad"
                        htmlFor={`${kind}-modality`}
                        error={errors.modality}
                    >
                        <NativeSelect
                            id={`${kind}-modality`}
                            name="modality"
                            options={options.modalities}
                            placeholder="Seleccione…"
                            data-cy={`${kind}-modality`}
                        />
                    </FormField>
                    <FormField
                        label="Lugar o enlace"
                        htmlFor={`${kind}-location`}
                        error={errors.location}
                    >
                        <Input
                            id={`${kind}-location`}
                            name="location"
                            maxLength={200}
                            data-cy={`${kind}-location`}
                        />
                    </FormField>
                    <FormField
                        label="Indicaciones para el candidato"
                        htmlFor={`${kind}-instructions`}
                        error={errors.instructions}
                        hint="Se incluyen en la convocatoria que recibe el candidato (RF-17)."
                        className="md:col-span-2"
                    >
                        <Textarea
                            id={`${kind}-instructions`}
                            name="instructions"
                            rows={2}
                            data-cy={`${kind}-instructions`}
                        />
                    </FormField>
                    <div className="md:col-span-2">
                        <Button
                            type="submit"
                            disabled={processing}
                            data-cy={`schedule-${kind}`}
                        >
                            {processing ? (
                                <Spinner />
                            ) : (
                                <CalendarPlus aria-hidden="true" />
                            )}
                            {kind === 'evaluacion'
                                ? 'Programar evaluación'
                                : 'Programar entrevista'}
                        </Button>
                    </div>
                </>
            )}
        </Form>
    );
}

export function AssessmentPanel({
    applicationId,
    evaluations,
    interviews,
    scheduling,
    can,
}: {
    applicationId: number;
    evaluations: AssessmentSummary[];
    interviews: AssessmentSummary[];
    scheduling: SchedulingOptions;
    can: { scheduleEvaluation: boolean; scheduleInterview: boolean };
}) {
    return (
        <>
            <Section
                title="Evaluaciones"
                description="Programar la evaluación genera la convocatoria para el candidato y para el evaluador (RF-16 y RF-17)."
                data-cy="evaluations-panel"
            >
                <div className="space-y-3">
                    {evaluations.length === 0 && (
                        <p className="text-muted-foreground text-sm">
                            Todavía no hay evaluaciones programadas.
                        </p>
                    )}
                    {evaluations.map((evaluation) => (
                        <SessionItem key={evaluation.id} session={evaluation} />
                    ))}
                    {can.scheduleEvaluation && scheduling && (
                        <ScheduleForm
                            kind="evaluacion"
                            applicationId={applicationId}
                            options={scheduling}
                        />
                    )}
                </div>
            </Section>

            <Section
                title="Entrevistas"
                description="El evaluador asignado registra puntajes, resultado y observaciones (RF-18 y RF-19)."
                data-cy="interviews-panel"
            >
                <div className="space-y-3">
                    {interviews.length === 0 && (
                        <p className="text-muted-foreground text-sm">
                            Todavía no hay entrevistas programadas.
                        </p>
                    )}
                    {interviews.map((interview) => (
                        <SessionItem key={interview.id} session={interview} />
                    ))}
                    {can.scheduleInterview && scheduling && (
                        <ScheduleForm
                            kind="entrevista"
                            applicationId={applicationId}
                            options={scheduling}
                        />
                    )}
                </div>
            </Section>
        </>
    );
}
