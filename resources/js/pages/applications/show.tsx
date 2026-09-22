import { Form, Head, Link } from '@inertiajs/react';
import { CheckCircle2, FileText, Lock, UserX } from 'lucide-react';
import ApplicationStageController from '@/actions/App/Http/Controllers/Applications/ApplicationStageController';
import VacancyApplicationController from '@/actions/App/Http/Controllers/Applications/VacancyApplicationController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { FormField, NativeSelect } from '@/components/form-controls';
import {
    DetailList,
    PageContainer,
    PageHeader,
    Section,
} from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { StatusTimeline } from '@/components/status-timeline';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime, formatFileSize } from '@/lib/format';
import { AssessmentPanel } from '@/components/assessments/assessment-panel';
import type { SchedulingOptions } from '@/components/assessments/assessment-panel';
import type {
    AssessmentSummary,
    JobApplication,
    Presented,
    StatusHistoryEntry,
} from '@/types';

type Props = {
    application: JobApplication;
    history: StatusHistoryEntry[];
    stageOptions: Presented[];
    assessments: {
        evaluations: AssessmentSummary[];
        interviews: AssessmentSummary[];
    };
    scheduling: SchedulingOptions;
    can: {
        changeStage: boolean;
        scheduleEvaluation: boolean;
        scheduleInterview: boolean;
    };
};

export default function ApplicationShow({
    application,
    history,
    stageOptions,
    assessments,
    scheduling,
    can,
}: Props) {
    const profile = application.candidate?.profile;
    const canShortlist = stageOptions.some(
        (option) => option.value === 'preseleccionado',
    );
    const canDiscard = stageOptions.some(
        (option) => option.value === 'descartado',
    );
    const otherStages = stageOptions.filter(
        (option) =>
            option.value !== 'preseleccionado' && option.value !== 'descartado',
    );

    return (
        <>
            <Head title={`Expediente ${application.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono text-xs">
                                {application.code}
                            </span>
                            <StatusBadge status={application.status} />
                        </>
                    }
                    title={application.candidate?.name ?? 'Candidato'}
                    description={
                        application.vacancy ? (
                            <>
                                Postulación a{' '}
                                <Link
                                    href={VacancyController.show(
                                        application.vacancy.id,
                                    )}
                                    className="font-medium hover:underline"
                                >
                                    {application.vacancy.title}
                                </Link>{' '}
                                <span className="font-mono text-xs">
                                    ({application.vacancy.code})
                                </span>
                            </>
                        ) : undefined
                    }
                    actions={
                        application.vacancy && (
                            <Button variant="outline" asChild>
                                <Link
                                    href={VacancyApplicationController(
                                        application.vacancy.id,
                                    )}
                                >
                                    Volver a postulaciones
                                </Link>
                            </Button>
                        )
                    }
                />

                <WorkflowAlert />

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <div className="min-w-0 space-y-6 lg:col-span-2">
                        <Section
                            title="Datos del candidato"
                            description="Expediente de la postulación (RF-12)."
                        >
                            <div className="space-y-6">
                                <DetailList
                                    items={[
                                        {
                                            label: 'Correo',
                                            value:
                                                application.candidate?.email ??
                                                '—',
                                        },
                                        {
                                            label: 'Teléfono',
                                            value: profile?.phone ?? '—',
                                        },
                                        {
                                            label: 'Ciudad',
                                            value: profile?.city ?? '—',
                                        },
                                        {
                                            label: 'Nivel educativo',
                                            value:
                                                profile?.education_level
                                                    ?.label ?? '—',
                                        },
                                        {
                                            label: 'Título u ocupación',
                                            value:
                                                profile?.professional_title ??
                                                '—',
                                        },
                                        {
                                            label: 'Experiencia',
                                            value:
                                                profile?.years_of_experience !==
                                                    null &&
                                                profile?.years_of_experience !==
                                                    undefined
                                                    ? `${profile.years_of_experience} años`
                                                    : '—',
                                        },
                                        {
                                            label: 'Postuló',
                                            value: formatDateTime(
                                                application.applied_at,
                                            ),
                                        },
                                        {
                                            label: 'Última actualización',
                                            value: formatDateTime(
                                                application.stage_changed_at,
                                            ),
                                        },
                                    ]}
                                />

                                {profile?.summary && (
                                    <div className="space-y-1.5 border-t pt-5">
                                        <h3 className="text-sm font-medium">
                                            Resumen profesional
                                        </h3>
                                        <p className="text-muted-foreground text-sm leading-relaxed whitespace-pre-line">
                                            {profile.summary}
                                        </p>
                                    </div>
                                )}

                                {application.cv ? (
                                    <a
                                        href={application.cv.download_url}
                                        className="hover:bg-surface flex items-center gap-3 rounded-lg border p-3 text-sm transition-colors"
                                        data-cy="application-cv"
                                    >
                                        <FileText
                                            className="text-muted-foreground size-5 shrink-0"
                                            aria-hidden="true"
                                        />
                                        <span className="min-w-0">
                                            <span className="block font-medium">
                                                CV adjunto a la postulación
                                            </span>
                                            <span className="text-muted-foreground block truncate text-xs">
                                                {application.cv.original_name} (
                                                {formatFileSize(
                                                    application.cv.size_bytes,
                                                )}
                                                )
                                            </span>
                                        </span>
                                    </a>
                                ) : (
                                    <p className="text-muted-foreground text-sm">
                                        La postulación no tiene CV adjunto.
                                    </p>
                                )}
                            </div>
                        </Section>

                        {can.changeStage ? (
                            <Section
                                title="Seguimiento de la postulación"
                                description="Cada cambio queda registrado y se notifica al candidato (RF-13 a RF-15)."
                                data-cy="stage-panel"
                            >
                                <div className="grid gap-4 md:grid-cols-2">
                                    {canShortlist && (
                                        <Form
                                            {...ApplicationStageController.shortlist.form(
                                                application.id,
                                            )}
                                            className="space-y-3 rounded-lg border p-4"
                                        >
                                            {({ errors, processing }) => (
                                                <>
                                                    <h3 className="flex items-center gap-2 font-medium">
                                                        <CheckCircle2
                                                            className="text-tone-success-foreground size-4"
                                                            aria-hidden="true"
                                                        />
                                                        Preseleccionar
                                                    </h3>
                                                    <FormField
                                                        label="Observación (opcional)"
                                                        htmlFor="shortlist-comment"
                                                        error={errors.comment}
                                                    >
                                                        <Input
                                                            id="shortlist-comment"
                                                            name="comment"
                                                            data-cy="shortlist-comment"
                                                        />
                                                    </FormField>
                                                    <Button
                                                        type="submit"
                                                        disabled={processing}
                                                        data-cy="shortlist-application"
                                                    >
                                                        Preseleccionar
                                                    </Button>
                                                </>
                                            )}
                                        </Form>
                                    )}

                                    {canDiscard && (
                                        <Form
                                            {...ApplicationStageController.discard.form(
                                                application.id,
                                            )}
                                            className="space-y-3 rounded-lg border p-4"
                                        >
                                            {({ errors, processing }) => (
                                                <>
                                                    <h3 className="flex items-center gap-2 font-medium">
                                                        <UserX
                                                            className="text-tone-danger-foreground size-4"
                                                            aria-hidden="true"
                                                        />
                                                        Descartar
                                                    </h3>
                                                    <FormField
                                                        label="Motivo (uso interno)"
                                                        htmlFor="discard-comment"
                                                        error={errors.comment}
                                                        required
                                                    >
                                                        <Textarea
                                                            id="discard-comment"
                                                            name="comment"
                                                            rows={2}
                                                            data-cy="discard-comment"
                                                        />
                                                    </FormField>
                                                    <Button
                                                        type="submit"
                                                        variant="destructive"
                                                        disabled={processing}
                                                        data-cy="discard-application"
                                                    >
                                                        Descartar
                                                    </Button>
                                                </>
                                            )}
                                        </Form>
                                    )}

                                    {otherStages.length > 0 && (
                                        <Form
                                            {...ApplicationStageController.change.form(
                                                application.id,
                                            )}
                                            className="space-y-3 rounded-lg border p-4 md:col-span-2"
                                        >
                                            {({ errors, processing }) => (
                                                <>
                                                    <h3 className="font-medium">
                                                        Cambiar de etapa
                                                    </h3>
                                                    <div className="grid gap-3 md:grid-cols-[1fr_2fr_auto] md:items-end">
                                                        <FormField
                                                            label="Nueva etapa"
                                                            htmlFor="stage-status"
                                                            error={
                                                                errors.status
                                                            }
                                                        >
                                                            <NativeSelect
                                                                id="stage-status"
                                                                name="status"
                                                                options={
                                                                    otherStages
                                                                }
                                                                data-cy="stage-select"
                                                            />
                                                        </FormField>
                                                        <FormField
                                                            label="Observación (opcional)"
                                                            htmlFor="stage-comment"
                                                            error={
                                                                errors.comment
                                                            }
                                                        >
                                                            <Input
                                                                id="stage-comment"
                                                                name="comment"
                                                                data-cy="stage-comment"
                                                            />
                                                        </FormField>
                                                        <Button
                                                            type="submit"
                                                            disabled={
                                                                processing
                                                            }
                                                            data-cy="change-stage"
                                                        >
                                                            Actualizar etapa
                                                        </Button>
                                                    </div>
                                                </>
                                            )}
                                        </Form>
                                    )}
                                </div>
                            </Section>
                        ) : (
                            <p className="bg-surface text-muted-foreground flex items-center gap-3 rounded-xl border border-dashed px-5 py-4 text-sm">
                                <Lock className="size-4" aria-hidden="true" />
                                No hay acciones de seguimiento disponibles para
                                esta postulación.
                            </p>
                        )}

                        <AssessmentPanel
                            applicationId={application.id}
                            evaluations={assessments.evaluations}
                            interviews={assessments.interviews}
                            scheduling={scheduling}
                            can={{
                                scheduleEvaluation: can.scheduleEvaluation,
                                scheduleInterview: can.scheduleInterview,
                            }}
                        />
                    </div>

                    <Section
                        title="Historial de etapas"
                        description="Estado anterior, nuevo, usuario, fecha y observación."
                        className="h-fit"
                    >
                        <StatusTimeline entries={history} />
                    </Section>
                </div>
            </PageContainer>
        </>
    );
}

ApplicationShow.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Expediente', href: VacancyController.index() },
    ],
};
