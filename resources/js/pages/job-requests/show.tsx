import { Form, Head, Link } from '@inertiajs/react';
import {
    AlertTriangle,
    Briefcase,
    CheckCircle2,
    Pencil,
    Send,
    XCircle,
} from 'lucide-react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import JobRequestTransitionController from '@/actions/App/Http/Controllers/JobRequests/JobRequestTransitionController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { FormField } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { DetailList, PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { StatusTimeline } from '@/components/status-timeline';
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
import { Textarea } from '@/components/ui/textarea';
import { formatDate, formatDateTime } from '@/lib/format';
import type { JobRequest, StatusHistoryEntry } from '@/types';

type Props = {
    jobRequest: JobRequest;
    history: StatusHistoryEntry[];
    can: {
        update: boolean;
        submit: boolean;
        review: boolean;
        decide: boolean;
        createVacancy: boolean;
    };
};

export default function ShowJobRequest({ jobRequest, history, can }: Props) {
    return (
        <>
            <Head title={`Requerimiento ${jobRequest.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono">{jobRequest.code}</span>
                            <StatusBadge status={jobRequest.status} />
                        </>
                    }
                    title={jobRequest.position_title}
                    description={jobRequest.area}
                    actions={
                        <>
                            {can.update && (
                                <Button variant="outline" asChild>
                                    <Link
                                        href={JobRequestController.edit(jobRequest.id)}
                                        data-cy="edit-job-request"
                                    >
                                        <Pencil />
                                        Corregir
                                    </Link>
                                </Button>
                            )}
                            {can.submit && (
                                <Form
                                    {...JobRequestTransitionController.submit.form(jobRequest.id)}
                                >
                                    {({ processing }) => (
                                        <Button
                                            type="submit"
                                            disabled={processing}
                                            data-cy="submit-job-request"
                                        >
                                            <Send />
                                            Enviar a RR. HH.
                                        </Button>
                                    )}
                                </Form>
                            )}
                            {can.createVacancy && (
                                <Button asChild>
                                    <Link
                                        href={VacancyController.create({
                                            query: { requerimiento: jobRequest.id },
                                        })}
                                        data-cy="create-vacancy-from-request"
                                    >
                                        <Briefcase />
                                        Generar vacante
                                    </Link>
                                </Button>
                            )}
                        </>
                    }
                />

                <WorkflowAlert />

                {jobRequest.status.value === 'observado' && jobRequest.observation && (
                    <Alert data-cy="observation-alert">
                        <AlertTriangle />
                        <AlertTitle>Observación de RR. HH.</AlertTitle>
                        <AlertDescription>{jobRequest.observation}</AlertDescription>
                    </Alert>
                )}

                {jobRequest.status.value === 'rechazado' && (
                    <Alert variant="destructive" data-cy="rejection-alert">
                        <XCircle />
                        <AlertTitle>Requerimiento rechazado</AlertTitle>
                        <AlertDescription>
                            {jobRequest.decision_comment}
                        </AlertDescription>
                    </Alert>
                )}

                <div className="grid gap-6 lg:grid-cols-3">
                    <div className="space-y-6 lg:col-span-2">
                        {can.review && (
                            <Card data-cy="review-panel">
                                <CardHeader>
                                    <CardTitle>Validación de RR. HH.</CardTitle>
                                    <CardDescription>
                                        RF-02 · Verifique la información. Si hay
                                        inconsistencias, observe el requerimiento
                                        para que el área lo corrija.
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="grid gap-4 md:grid-cols-2">
                                    <Form
                                        {...JobRequestTransitionController.observe.form(jobRequest.id)}
                                        resetOnSuccess
                                        className="space-y-3"
                                    >
                                        {({ errors, processing }) => (
                                            <>
                                                <FormField
                                                    label="Observación"
                                                    htmlFor="observe-comment"
                                                    error={errors.comment}
                                                >
                                                    <Textarea
                                                        id="observe-comment"
                                                        name="comment"
                                                        rows={3}
                                                        placeholder="Describa qué debe corregirse"
                                                        data-cy="observe-comment"
                                                    />
                                                </FormField>
                                                <Button
                                                    type="submit"
                                                    variant="outline"
                                                    disabled={processing}
                                                    data-cy="observe-job-request"
                                                >
                                                    <AlertTriangle />
                                                    Observar
                                                </Button>
                                            </>
                                        )}
                                    </Form>
                                    <div className="bg-muted/30 flex flex-col justify-between gap-3 rounded-lg border p-4">
                                        <p className="text-sm">
                                            Si el requerimiento es consistente,
                                            valídelo para remitirlo al aprobador.
                                        </p>
                                        <Form
                                            {...JobRequestTransitionController.validate.form(jobRequest.id)}
                                        >
                                            {({ processing }) => (
                                                <Button
                                                    type="submit"
                                                    disabled={processing}
                                                    data-cy="validate-job-request"
                                                >
                                                    <CheckCircle2 />
                                                    Validar requerimiento
                                                </Button>
                                            )}
                                        </Form>
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {can.decide && (
                            <Card data-cy="decision-panel">
                                <CardHeader>
                                    <CardTitle>Decisión del aprobador</CardTitle>
                                    <CardDescription>
                                        RF-03 · Registre la aprobación o el
                                        rechazo. El rechazo se notifica al área
                                        solicitante (RF-04).
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <Form
                                        {...JobRequestTransitionController.decide.form(jobRequest.id)}
                                        className="space-y-4"
                                    >
                                        {({ errors, processing }) => (
                                            <>
                                                <fieldset className="grid gap-3 sm:grid-cols-2">
                                                    <legend className="sr-only">
                                                        Decisión
                                                    </legend>
                                                    <label className="flex cursor-pointer items-start gap-3 rounded-lg border p-4 has-[:checked]:border-emerald-500 has-[:checked]:bg-emerald-50 dark:has-[:checked]:bg-emerald-950/40">
                                                        <input
                                                            type="radio"
                                                            name="decision"
                                                            value="aprobar"
                                                            defaultChecked
                                                            className="mt-1"
                                                            data-cy="decision-approve"
                                                        />
                                                        <span>
                                                            <span className="flex items-center gap-2 font-medium">
                                                                <CheckCircle2 className="size-4 text-emerald-600" />
                                                                Aprobar
                                                            </span>
                                                            <span className="text-muted-foreground block text-xs">
                                                                Autoriza generar la
                                                                convocatoria.
                                                            </span>
                                                        </span>
                                                    </label>
                                                    <label className="flex cursor-pointer items-start gap-3 rounded-lg border p-4 has-[:checked]:border-rose-500 has-[:checked]:bg-rose-50 dark:has-[:checked]:bg-rose-950/40">
                                                        <input
                                                            type="radio"
                                                            name="decision"
                                                            value="rechazar"
                                                            className="mt-1"
                                                            data-cy="decision-reject"
                                                        />
                                                        <span>
                                                            <span className="flex items-center gap-2 font-medium">
                                                                <XCircle className="size-4 text-rose-600" />
                                                                Rechazar
                                                            </span>
                                                            <span className="text-muted-foreground block text-xs">
                                                                Requiere indicar el
                                                                motivo.
                                                            </span>
                                                        </span>
                                                    </label>
                                                </fieldset>
                                                <InputError message={errors.decision} />
                                                <FormField
                                                    label="Comentario / motivo"
                                                    htmlFor="decision-comment"
                                                    error={errors.comment}
                                                    hint="Obligatorio si rechaza el requerimiento."
                                                >
                                                    <Textarea
                                                        id="decision-comment"
                                                        name="comment"
                                                        rows={3}
                                                        data-cy="decision-comment"
                                                    />
                                                </FormField>
                                                <Button
                                                    type="submit"
                                                    disabled={processing}
                                                    data-cy="submit-decision"
                                                >
                                                    Registrar decisión
                                                </Button>
                                            </>
                                        )}
                                    </Form>
                                </CardContent>
                            </Card>
                        )}

                        <Card>
                            <CardHeader>
                                <CardTitle>Detalle del requerimiento</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <DetailList
                                    items={[
                                        { label: 'Puesto', value: jobRequest.position_title },
                                        { label: 'Área solicitante', value: jobRequest.area },
                                        { label: 'Plazas', value: jobRequest.headcount },
                                        { label: 'Tipo de contrato', value: jobRequest.contract_type.label },
                                        { label: 'Fecha requerida', value: formatDate(jobRequest.required_by) },
                                        { label: 'Solicitante', value: jobRequest.requester?.name ?? '—' },
                                        { label: 'Registrado', value: formatDateTime(jobRequest.created_at) },
                                        { label: 'Enviado a RR. HH.', value: formatDateTime(jobRequest.submitted_at) },
                                        { label: 'Validado', value: formatDateTime(jobRequest.validated_at) },
                                        { label: 'Decidido', value: formatDateTime(jobRequest.decided_at) },
                                    ]}
                                />
                                <div className="space-y-1">
                                    <p className="text-muted-foreground text-xs font-medium tracking-wide uppercase">
                                        Justificación
                                    </p>
                                    <p className="text-sm whitespace-pre-line">
                                        {jobRequest.justification}
                                    </p>
                                </div>
                                {jobRequest.decision_comment &&
                                    jobRequest.status.value === 'aprobado' && (
                                        <div className="space-y-1">
                                            <p className="text-muted-foreground text-xs font-medium tracking-wide uppercase">
                                                Comentario del aprobador
                                            </p>
                                            <p className="text-sm">
                                                {jobRequest.decision_comment}
                                            </p>
                                        </div>
                                    )}
                                {jobRequest.vacancy && (
                                    <div className="flex items-center justify-between rounded-lg border p-3 text-sm">
                                        <span className="flex items-center gap-2">
                                            <Briefcase className="text-muted-foreground size-4" />
                                            Vacante{' '}
                                            <span className="font-mono">
                                                {jobRequest.vacancy.code}
                                            </span>
                                            <StatusBadge status={jobRequest.vacancy.status} />
                                        </span>
                                        <Link
                                            href={VacancyController.show(jobRequest.vacancy.id)}
                                            className="font-medium hover:underline"
                                        >
                                            Ver vacante
                                        </Link>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>

                    <Card className="h-fit">
                        <CardHeader>
                            <CardTitle>Historial de estados</CardTitle>
                            <CardDescription>
                                Trazabilidad de cada cambio con usuario y fecha.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <StatusTimeline entries={history} />
                        </CardContent>
                    </Card>
                </div>
            </PageContainer>
        </>
    );
}

ShowJobRequest.layout = {
    breadcrumbs: [
        { title: 'Requerimientos', href: JobRequestController.index() },
        { title: 'Detalle', href: JobRequestController.index() },
    ],
};
