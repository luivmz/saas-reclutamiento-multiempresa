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
import { RadioCard } from '@/components/choice';
import { FormField } from '@/components/form-controls';
import InputError from '@/components/input-error';
import {
    DetailList,
    PageContainer,
    PageHeader,
    Section,
} from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { StatusTimeline } from '@/components/status-timeline';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
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
                            <span className="font-mono text-xs">
                                {jobRequest.code}
                            </span>
                            <StatusBadge status={jobRequest.status} />
                        </>
                    }
                    title={jobRequest.position_title}
                    description={`Área solicitante: ${jobRequest.area}`}
                    actions={
                        <>
                            {can.update && (
                                <Button variant="outline" asChild>
                                    <Link
                                        href={JobRequestController.edit(
                                            jobRequest.id,
                                        )}
                                        data-cy="edit-job-request"
                                    >
                                        <Pencil aria-hidden="true" />
                                        Corregir
                                    </Link>
                                </Button>
                            )}
                            {can.submit && (
                                <Form
                                    {...JobRequestTransitionController.submit.form(
                                        jobRequest.id,
                                    )}
                                >
                                    {({ processing }) => (
                                        <Button
                                            type="submit"
                                            disabled={processing}
                                            data-cy="submit-job-request"
                                        >
                                            <Send aria-hidden="true" />
                                            Enviar a RR. HH.
                                        </Button>
                                    )}
                                </Form>
                            )}
                            {can.createVacancy && (
                                <Button asChild>
                                    <Link
                                        href={VacancyController.create({
                                            query: {
                                                requerimiento: jobRequest.id,
                                            },
                                        })}
                                        data-cy="create-vacancy-from-request"
                                    >
                                        <Briefcase aria-hidden="true" />
                                        Generar vacante
                                    </Link>
                                </Button>
                            )}
                        </>
                    }
                />

                <WorkflowAlert />

                {jobRequest.status.value === 'observado' &&
                    jobRequest.observation && (
                        <Alert data-cy="observation-alert">
                            <AlertTriangle />
                            <AlertTitle>Observación de RR. HH.</AlertTitle>
                            <AlertDescription>
                                {jobRequest.observation}
                            </AlertDescription>
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

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <div className="min-w-0 space-y-6 lg:col-span-2">
                        {can.review && (
                            <Section
                                title="Validación de RR. HH."
                                description="Verifique la información. Si hay inconsistencias, observe el requerimiento para que el área lo corrija (RF-02)."
                                data-cy="review-panel"
                            >
                                <div className="grid gap-5 md:grid-cols-2">
                                    <Form
                                        {...JobRequestTransitionController.observe.form(
                                            jobRequest.id,
                                        )}
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
                                                    <AlertTriangle aria-hidden="true" />
                                                    Observar
                                                </Button>
                                            </>
                                        )}
                                    </Form>
                                    <div className="bg-surface flex flex-col justify-between gap-3 rounded-lg border p-4">
                                        <p className="text-sm leading-relaxed">
                                            Si el requerimiento es consistente,
                                            valídelo para remitirlo al
                                            aprobador.
                                        </p>
                                        <Form
                                            {...JobRequestTransitionController.validate.form(
                                                jobRequest.id,
                                            )}
                                        >
                                            {({ processing }) => (
                                                <Button
                                                    type="submit"
                                                    disabled={processing}
                                                    data-cy="validate-job-request"
                                                >
                                                    <CheckCircle2 aria-hidden="true" />
                                                    Validar requerimiento
                                                </Button>
                                            )}
                                        </Form>
                                    </div>
                                </div>
                            </Section>
                        )}

                        {can.decide && (
                            <Section
                                title="Decisión del aprobador"
                                description="Registre la aprobación o el rechazo. El rechazo se notifica al área solicitante (RF-03 y RF-04)."
                                data-cy="decision-panel"
                            >
                                <Form
                                    {...JobRequestTransitionController.decide.form(
                                        jobRequest.id,
                                    )}
                                    className="space-y-4"
                                >
                                    {({ errors, processing }) => (
                                        <>
                                            <fieldset className="grid gap-3 sm:grid-cols-2">
                                                <legend className="sr-only">
                                                    Decisión
                                                </legend>
                                                <RadioCard
                                                    name="decision"
                                                    value="aprobar"
                                                    defaultChecked
                                                    tone="success"
                                                    icon={CheckCircle2}
                                                    title="Aprobar"
                                                    description="Autoriza generar la convocatoria."
                                                    data-cy="decision-approve"
                                                />
                                                <RadioCard
                                                    name="decision"
                                                    value="rechazar"
                                                    tone="danger"
                                                    icon={XCircle}
                                                    title="Rechazar"
                                                    description="Requiere indicar el motivo."
                                                    data-cy="decision-reject"
                                                />
                                            </fieldset>
                                            <InputError
                                                message={errors.decision}
                                            />
                                            <FormField
                                                label="Comentario o motivo"
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
                            </Section>
                        )}

                        <Section title="Detalle del requerimiento">
                            <div className="space-y-6">
                                <DetailList
                                    items={[
                                        {
                                            label: 'Puesto',
                                            value: jobRequest.position_title,
                                        },
                                        {
                                            label: 'Área solicitante',
                                            value: jobRequest.area,
                                        },
                                        {
                                            label: 'Plazas',
                                            value: jobRequest.headcount,
                                        },
                                        {
                                            label: 'Tipo de contrato',
                                            value: jobRequest.contract_type
                                                .label,
                                        },
                                        {
                                            label: 'Fecha requerida',
                                            value: formatDate(
                                                jobRequest.required_by,
                                            ),
                                        },
                                        {
                                            label: 'Solicitante',
                                            value:
                                                jobRequest.requester?.name ??
                                                '—',
                                        },
                                        {
                                            label: 'Registrado',
                                            value: formatDateTime(
                                                jobRequest.created_at,
                                            ),
                                        },
                                        {
                                            label: 'Enviado a RR. HH.',
                                            value: formatDateTime(
                                                jobRequest.submitted_at,
                                            ),
                                        },
                                        {
                                            label: 'Validado',
                                            value: formatDateTime(
                                                jobRequest.validated_at,
                                            ),
                                        },
                                        {
                                            label: 'Decidido',
                                            value: formatDateTime(
                                                jobRequest.decided_at,
                                            ),
                                        },
                                    ]}
                                />

                                <div className="space-y-1.5 border-t pt-5">
                                    <h3 className="text-sm font-medium">
                                        Justificación
                                    </h3>
                                    <p className="text-muted-foreground text-sm leading-relaxed whitespace-pre-line">
                                        {jobRequest.justification}
                                    </p>
                                </div>

                                {jobRequest.decision_comment &&
                                    jobRequest.status.value === 'aprobado' && (
                                        <div className="space-y-1.5">
                                            <h3 className="text-sm font-medium">
                                                Comentario del aprobador
                                            </h3>
                                            <p className="text-muted-foreground text-sm leading-relaxed">
                                                {jobRequest.decision_comment}
                                            </p>
                                        </div>
                                    )}

                                {jobRequest.vacancy && (
                                    <div className="bg-surface flex flex-wrap items-center justify-between gap-3 rounded-lg border p-4 text-sm">
                                        <span className="flex flex-wrap items-center gap-2">
                                            <Briefcase
                                                className="text-muted-foreground size-4"
                                                aria-hidden="true"
                                            />
                                            Vacante{' '}
                                            <span className="font-mono">
                                                {jobRequest.vacancy.code}
                                            </span>
                                            <StatusBadge
                                                status={
                                                    jobRequest.vacancy.status
                                                }
                                            />
                                        </span>
                                        <Link
                                            href={VacancyController.show(
                                                jobRequest.vacancy.id,
                                            )}
                                            className="font-medium hover:underline"
                                        >
                                            Ver vacante
                                        </Link>
                                    </div>
                                )}
                            </div>
                        </Section>
                    </div>

                    <Section
                        title="Historial de estados"
                        description="Cada cambio con su autor y su fecha."
                        className="h-fit"
                    >
                        <StatusTimeline entries={history} />
                    </Section>
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
