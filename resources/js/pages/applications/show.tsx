import { Form, Head, Link } from '@inertiajs/react';
import { CheckCircle2, FileText, Lock, UserX } from 'lucide-react';
import ApplicationStageController from '@/actions/App/Http/Controllers/Applications/ApplicationStageController';
import VacancyApplicationController from '@/actions/App/Http/Controllers/Applications/VacancyApplicationController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { FormField, NativeSelect } from '@/components/form-controls';
import { DetailList, PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { StatusTimeline } from '@/components/status-timeline';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime, formatFileSize } from '@/lib/format';
import { AssessmentPanel } from '@/components/assessments/assessment-panel';
import type { SchedulingOptions } from '@/components/assessments/assessment-panel';
import type { AssessmentSummary, JobApplication, Presented, StatusHistoryEntry } from '@/types';

type Props = {
    application: JobApplication;
    history: StatusHistoryEntry[];
    stageOptions: Presented[];
    assessments: { evaluations: AssessmentSummary[]; interviews: AssessmentSummary[] };
    scheduling: SchedulingOptions;
    can: { changeStage: boolean; scheduleEvaluation: boolean; scheduleInterview: boolean };
};

export default function ApplicationShow({ application, history, stageOptions, assessments, scheduling, can }: Props) {
    const profile = application.candidate?.profile;
    const canShortlist = stageOptions.some((option) => option.value === 'preseleccionado');
    const canDiscard = stageOptions.some((option) => option.value === 'descartado');
    const otherStages = stageOptions.filter(
        (option) => option.value !== 'preseleccionado' && option.value !== 'descartado',
    );

    return (
        <>
            <Head title={`Expediente ${application.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono">{application.code}</span>
                            <StatusBadge status={application.status} />
                        </>
                    }
                    title={application.candidate?.name ?? 'Candidato'}
                    description={
                        <>
                            Postulación a{' '}
                            {application.vacancy && (
                                <Link href={VacancyController.show(application.vacancy.id)} className="font-medium hover:underline">
                                    {application.vacancy.code} · {application.vacancy.title}
                                </Link>
                            )}
                        </>
                    }
                    actions={
                        application.vacancy && (
                            <Button variant="outline" asChild>
                                <Link href={VacancyApplicationController(application.vacancy.id)}>
                                    Volver a postulaciones
                                </Link>
                            </Button>
                        )
                    }
                />

                <WorkflowAlert />

                <div className="grid gap-6 lg:grid-cols-3">
                    <div className="space-y-6 lg:col-span-2">
                        <Card>
                            <CardHeader>
                                <CardTitle>Datos del candidato</CardTitle>
                                <CardDescription>RF-12 · Expediente de la postulación.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <DetailList
                                    items={[
                                        { label: 'Correo', value: application.candidate?.email ?? '—' },
                                        { label: 'Teléfono', value: profile?.phone ?? '—' },
                                        { label: 'Ciudad', value: profile?.city ?? '—' },
                                        { label: 'Nivel educativo', value: profile?.education_level?.label ?? '—' },
                                        { label: 'Título u ocupación', value: profile?.professional_title ?? '—' },
                                        { label: 'Experiencia', value: profile?.years_of_experience !== null && profile?.years_of_experience !== undefined ? `${profile.years_of_experience} años` : '—' },
                                        { label: 'Postuló', value: formatDateTime(application.applied_at) },
                                        { label: 'Última actualización', value: formatDateTime(application.stage_changed_at) },
                                    ]}
                                />
                                {profile?.summary && (
                                    <div className="space-y-1">
                                        <p className="text-muted-foreground text-xs font-medium tracking-wide uppercase">Resumen profesional</p>
                                        <p className="text-sm whitespace-pre-line">{profile.summary}</p>
                                    </div>
                                )}
                                {application.cv ? (
                                    <a href={application.cv.download_url} className="hover:bg-accent flex items-center gap-3 rounded-lg border p-3 text-sm" data-cy="application-cv">
                                        <FileText className="text-muted-foreground size-5" />
                                        <span>
                                            <span className="block font-medium">CV adjunto a la postulación</span>
                                            <span className="text-muted-foreground text-xs">
                                                {application.cv.original_name} · {formatFileSize(application.cv.size_bytes)}
                                            </span>
                                        </span>
                                    </a>
                                ) : (
                                    <p className="text-muted-foreground text-sm">Sin CV adjunto.</p>
                                )}
                            </CardContent>
                        </Card>

                        {can.changeStage ? (
                            <Card data-cy="stage-panel">
                                <CardHeader>
                                    <CardTitle>Seguimiento de la postulación</CardTitle>
                                    <CardDescription>
                                        RF-13 y RF-14 · Cada cambio queda registrado y se notifica al candidato (RF-15).
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="grid gap-4 md:grid-cols-2">
                                    {canShortlist && (
                                        <Form {...ApplicationStageController.shortlist.form(application.id)} className="space-y-3 rounded-lg border p-4">
                                            {({ errors, processing }) => (
                                                <>
                                                    <p className="flex items-center gap-2 font-medium">
                                                        <CheckCircle2 className="size-4 text-emerald-600" />
                                                        Preseleccionar
                                                    </p>
                                                    <FormField label="Observación (opcional)" htmlFor="shortlist-comment" error={errors.comment}>
                                                        <Input id="shortlist-comment" name="comment" data-cy="shortlist-comment" />
                                                    </FormField>
                                                    <Button type="submit" disabled={processing} data-cy="shortlist-application">
                                                        Preseleccionar
                                                    </Button>
                                                </>
                                            )}
                                        </Form>
                                    )}
                                    {canDiscard && (
                                        <Form {...ApplicationStageController.discard.form(application.id)} className="space-y-3 rounded-lg border p-4">
                                            {({ errors, processing }) => (
                                                <>
                                                    <p className="flex items-center gap-2 font-medium">
                                                        <UserX className="size-4 text-rose-600" />
                                                        Descartar
                                                    </p>
                                                    <FormField label="Motivo (obligatorio, uso interno)" htmlFor="discard-comment" error={errors.comment}>
                                                        <Textarea id="discard-comment" name="comment" rows={2} data-cy="discard-comment" />
                                                    </FormField>
                                                    <Button type="submit" variant="destructive" disabled={processing} data-cy="discard-application">
                                                        Descartar
                                                    </Button>
                                                </>
                                            )}
                                        </Form>
                                    )}
                                    {otherStages.length > 0 && (
                                        <Form {...ApplicationStageController.change.form(application.id)} className="space-y-3 rounded-lg border p-4 md:col-span-2">
                                            {({ errors, processing }) => (
                                                <>
                                                    <p className="font-medium">Cambiar de etapa</p>
                                                    <div className="grid gap-3 md:grid-cols-[1fr_2fr_auto] md:items-end">
                                                        <FormField label="Nueva etapa" htmlFor="stage-status" error={errors.status}>
                                                            <NativeSelect id="stage-status" name="status" options={otherStages} data-cy="stage-select" />
                                                        </FormField>
                                                        <FormField label="Observación (opcional)" htmlFor="stage-comment" error={errors.comment}>
                                                            <Input id="stage-comment" name="comment" data-cy="stage-comment" />
                                                        </FormField>
                                                        <Button type="submit" disabled={processing} data-cy="change-stage">
                                                            Actualizar etapa
                                                        </Button>
                                                    </div>
                                                </>
                                            )}
                                        </Form>
                                    )}
                                </CardContent>
                            </Card>
                        ) : (
                            <Card className="bg-muted/30 border-dashed">
                                <CardContent className="text-muted-foreground flex items-center gap-3 text-sm">
                                    <Lock className="size-4" />
                                    No hay acciones de seguimiento disponibles para esta postulación.
                                </CardContent>
                            </Card>
                        )}

                        <AssessmentPanel
                            applicationId={application.id}
                            evaluations={assessments.evaluations}
                            interviews={assessments.interviews}
                            scheduling={scheduling}
                            can={{ scheduleEvaluation: can.scheduleEvaluation, scheduleInterview: can.scheduleInterview }}
                        />
                    </div>

                    <Card className="h-fit">
                        <CardHeader>
                            <CardTitle>Historial de etapas</CardTitle>
                            <CardDescription>Estado anterior, nuevo, usuario, fecha y observación.</CardDescription>
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

ApplicationShow.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Expediente', href: VacancyController.index() },
    ],
};
