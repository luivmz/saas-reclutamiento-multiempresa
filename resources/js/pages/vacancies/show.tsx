import { Form, Head, Link } from '@inertiajs/react';
import {
    CheckCircle2,
    ExternalLink,
    ListChecks,
    Pencil,
    Rocket,
    Scale,
    Users,
    XCircle,
} from 'lucide-react';
import VacancyApplicationController from '@/actions/App/Http/Controllers/Applications/VacancyApplicationController';
import VacancyComparisonController from '@/actions/App/Http/Controllers/Selection/VacancyComparisonController';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import VacancyPublicationController from '@/actions/App/Http/Controllers/Vacancies/VacancyPublicationController';
import { DetailList, PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { CriteriaTable } from '@/components/vacancies/criteria-table';
import { OperationalRiskCard } from '@/components/vacancies/operational-risk-card';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { formatDate, formatDateTime } from '@/lib/format';
import { show as jobsShow } from '@/routes/jobs';
import type { Vacancy } from '@/types';

type Props = {
    vacancy: Vacancy;
    validation: { publishable: boolean; issues: string[] };
    can: { update: boolean; publish: boolean };
};

export default function ShowVacancy({ vacancy, validation, can }: Props) {
    const isDraft = vacancy.status.value === 'borrador';

    return (
        <>
            <Head title={`Vacante ${vacancy.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono">{vacancy.code}</span>
                            <StatusBadge status={vacancy.status} />
                        </>
                    }
                    title={vacancy.title}
                    description={`${vacancy.location} · ${vacancy.contract_type.label} · ${vacancy.positions} plaza(s)`}
                    actions={
                        <>
                            {can.update && (
                                <Button variant="outline" asChild>
                                    <Link href={VacancyController.edit(vacancy.id)} data-cy="edit-vacancy">
                                        <Pencil />
                                        Configurar
                                    </Link>
                                </Button>
                            )}
                            {can.publish && (
                                <Form {...VacancyPublicationController.form(vacancy.id)}>
                                    {({ processing }) => (
                                        <Button
                                            type="submit"
                                            disabled={processing || !validation.publishable}
                                            data-cy="publish-vacancy"
                                        >
                                            <Rocket />
                                            Publicar vacante
                                        </Button>
                                    )}
                                </Form>
                            )}
                            {!isDraft && (
                                <Button variant="outline" asChild>
                                    <Link href={VacancyComparisonController(vacancy.id)} data-cy="vacancy-comparison">
                                        <Scale />
                                        Comparación y ranking
                                    </Link>
                                </Button>
                            )}
                            {!isDraft && (
                                <Button variant="outline" asChild>
                                    <Link href={VacancyApplicationController(vacancy.id)} data-cy="vacancy-applications">
                                        <Users />
                                        Postulaciones ({vacancy.applications_count ?? 0})
                                    </Link>
                                </Button>
                            )}
                            {vacancy.status.value === 'publicada' && (
                                <Button variant="outline" asChild>
                                    <Link href={jobsShow(vacancy.id)} data-cy="public-vacancy-link">
                                        <ExternalLink />
                                        Ver en portal
                                    </Link>
                                </Button>
                            )}
                        </>
                    }
                />

                <WorkflowAlert />

                <div className="grid gap-6 lg:grid-cols-3">
                    <div className="space-y-6 lg:col-span-2">
                        <Card>
                            <CardHeader>
                                <CardTitle>Convocatoria</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <p className="text-sm whitespace-pre-line">{vacancy.summary}</p>
                                <DetailList
                                    items={[
                                        {
                                            label: 'Requerimiento',
                                            value: vacancy.job_request ? (
                                                <Link href={JobRequestController.show(vacancy.job_request.id)} className="font-mono hover:underline">
                                                    {vacancy.job_request.code}
                                                </Link>
                                            ) : (
                                                '—'
                                            ),
                                        },
                                        { label: 'Área', value: vacancy.job_request?.area ?? '—' },
                                        { label: 'Inicio de postulaciones', value: formatDate(vacancy.opens_at) },
                                        { label: 'Cierre de postulaciones', value: formatDate(vacancy.closes_at) },
                                        { label: 'Plazo objetivo del proceso', value: formatDateTime(vacancy.target_completion_at) },
                                        { label: 'Publicada', value: formatDateTime(vacancy.published_at) },
                                        { label: 'Cerrada', value: formatDateTime(vacancy.closed_at) },
                                    ]}
                                />
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Perfil del puesto</CardTitle>
                                <CardDescription>RF-05</CardDescription>
                            </CardHeader>
                            <CardContent>
                                {vacancy.profile ? (
                                    <DetailList
                                        items={[
                                            { label: 'Formación académica', value: vacancy.profile.education },
                                            { label: 'Experiencia', value: vacancy.profile.experience },
                                            { label: 'Funciones', value: <span className="whitespace-pre-line">{vacancy.profile.functions}</span> },
                                            { label: 'Competencias', value: <span className="whitespace-pre-line">{vacancy.profile.competencies}</span> },
                                        ]}
                                    />
                                ) : (
                                    <p className="text-muted-foreground text-sm">Perfil no registrado.</p>
                                )}
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader>
                                <CardTitle>Criterios y ponderaciones</CardTitle>
                                <CardDescription>
                                    RF-20 · Base del cálculo del ranking (RF-21).
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <CriteriaTable criteria={vacancy.criteria ?? []} />
                            </CardContent>
                        </Card>
                    </div>

                    <div className="space-y-6">
                        {!isDraft && <OperationalRiskCard vacancyId={vacancy.id} />}

                        {isDraft && (
                            <Card data-cy="validation-panel">
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <ListChecks className="size-5" />
                                        Validación de la vacante
                                    </CardTitle>
                                    <CardDescription>
                                        RF-06 · Revisión automática previa a la publicación.
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    {validation.issues.length === 0 ? (
                                        <p className="flex items-start gap-2 text-sm text-emerald-700 dark:text-emerald-400" data-cy="validation-ok">
                                            <CheckCircle2 className="mt-0.5 size-4 shrink-0" />
                                            La vacante cumple las validaciones y puede publicarse.
                                        </p>
                                    ) : (
                                        <ul className="space-y-2" data-cy="validation-issues">
                                            {validation.issues.map((issue) => (
                                                <li key={issue} className="flex items-start gap-2 text-sm text-rose-700 dark:text-rose-400">
                                                    <XCircle className="mt-0.5 size-4 shrink-0" />
                                                    {issue}
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </CardContent>
                            </Card>
                        )}
                        {vacancy.closure_type && (
                            <Card>
                                <CardHeader>
                                    <CardTitle>Cierre</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-2 text-sm">
                                    <StatusBadge status={vacancy.closure_type} />
                                    {vacancy.closure_notes && <p>{vacancy.closure_notes}</p>}
                                </CardContent>
                            </Card>
                        )}
                    </div>
                </div>
            </PageContainer>
        </>
    );
}

ShowVacancy.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Detalle', href: VacancyController.index() },
    ],
};
