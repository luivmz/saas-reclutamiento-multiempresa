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
import {
    DetailList,
    PageContainer,
    PageHeader,
    Section,
} from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { CriteriaTable } from '@/components/vacancies/criteria-table';
import { OperationalRiskCard } from '@/components/vacancies/operational-risk-card';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
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
                            <span className="font-mono text-xs">
                                {vacancy.code}
                            </span>
                            <StatusBadge status={vacancy.status} />
                        </>
                    }
                    title={vacancy.title}
                    description={`${vacancy.location}. ${vacancy.contract_type.label}, ${vacancy.positions} plaza${vacancy.positions === 1 ? '' : 's'}.`}
                    actions={
                        <>
                            {can.update && (
                                <Button variant="outline" asChild>
                                    <Link
                                        href={VacancyController.edit(
                                            vacancy.id,
                                        )}
                                        data-cy="edit-vacancy"
                                    >
                                        <Pencil aria-hidden="true" />
                                        Configurar
                                    </Link>
                                </Button>
                            )}
                            {!isDraft && (
                                <>
                                    <Button variant="outline" asChild>
                                        <Link
                                            href={VacancyApplicationController(
                                                vacancy.id,
                                            )}
                                            data-cy="vacancy-applications"
                                        >
                                            <Users aria-hidden="true" />
                                            Postulaciones (
                                            {vacancy.applications_count ?? 0})
                                        </Link>
                                    </Button>
                                    <Button variant="outline" asChild>
                                        <Link
                                            href={VacancyComparisonController(
                                                vacancy.id,
                                            )}
                                            data-cy="vacancy-comparison"
                                        >
                                            <Scale aria-hidden="true" />
                                            Comparación y ranking
                                        </Link>
                                    </Button>
                                </>
                            )}
                            {vacancy.status.value === 'publicada' && (
                                <Button variant="outline" asChild>
                                    <Link
                                        href={jobsShow(vacancy.id)}
                                        data-cy="public-vacancy-link"
                                    >
                                        <ExternalLink aria-hidden="true" />
                                        Ver en portal
                                    </Link>
                                </Button>
                            )}
                            {can.publish && (
                                <Form
                                    {...VacancyPublicationController.form(
                                        vacancy.id,
                                    )}
                                >
                                    {({ processing }) => (
                                        <Button
                                            type="submit"
                                            disabled={
                                                processing ||
                                                !validation.publishable
                                            }
                                            data-cy="publish-vacancy"
                                        >
                                            <Rocket aria-hidden="true" />
                                            Publicar vacante
                                        </Button>
                                    )}
                                </Form>
                            )}
                        </>
                    }
                />

                <WorkflowAlert />

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <div className="min-w-0 space-y-6 lg:col-span-2">
                        <Section title="Convocatoria">
                            <div className="space-y-6">
                                <p className="text-sm leading-relaxed whitespace-pre-line">
                                    {vacancy.summary}
                                </p>
                                <DetailList
                                    items={[
                                        {
                                            label: 'Requerimiento de origen',
                                            value: vacancy.job_request ? (
                                                <Link
                                                    href={JobRequestController.show(
                                                        vacancy.job_request.id,
                                                    )}
                                                    className="font-mono hover:underline"
                                                >
                                                    {vacancy.job_request.code}
                                                </Link>
                                            ) : (
                                                '—'
                                            ),
                                        },
                                        {
                                            label: 'Área',
                                            value:
                                                vacancy.job_request?.area ??
                                                '—',
                                        },
                                        {
                                            label: 'Inicio de postulaciones',
                                            value: formatDate(vacancy.opens_at),
                                        },
                                        {
                                            label: 'Cierre de postulaciones',
                                            value: formatDate(
                                                vacancy.closes_at,
                                            ),
                                        },
                                        {
                                            label: 'Plazo objetivo del proceso',
                                            value: formatDateTime(
                                                vacancy.target_completion_at,
                                            ),
                                        },
                                        {
                                            label: 'Publicada',
                                            value: formatDateTime(
                                                vacancy.published_at,
                                            ),
                                        },
                                        {
                                            label: 'Cerrada',
                                            value: formatDateTime(
                                                vacancy.closed_at,
                                            ),
                                        },
                                    ]}
                                />
                            </div>
                        </Section>

                        <Section
                            title="Perfil del puesto"
                            description="Requisitos con los que se evaluará a quienes postulen (RF-05)."
                        >
                            {vacancy.profile ? (
                                <DetailList
                                    items={[
                                        {
                                            label: 'Formación académica',
                                            value: vacancy.profile.education,
                                        },
                                        {
                                            label: 'Experiencia',
                                            value: vacancy.profile.experience,
                                        },
                                        {
                                            label: 'Funciones',
                                            value: (
                                                <span className="whitespace-pre-line">
                                                    {vacancy.profile.functions}
                                                </span>
                                            ),
                                        },
                                        {
                                            label: 'Competencias',
                                            value: (
                                                <span className="whitespace-pre-line">
                                                    {
                                                        vacancy.profile
                                                            .competencies
                                                    }
                                                </span>
                                            ),
                                        },
                                    ]}
                                />
                            ) : (
                                <p className="text-muted-foreground text-sm">
                                    El perfil todavía no está registrado.
                                </p>
                            )}
                        </Section>

                        <Section
                            title="Criterios y ponderaciones"
                            description="Base del cálculo del ranking (RF-20 y RF-21)."
                        >
                            <CriteriaTable criteria={vacancy.criteria ?? []} />
                        </Section>
                    </div>

                    <div className="min-w-0 space-y-6">
                        {!isDraft && (
                            <OperationalRiskCard vacancyId={vacancy.id} />
                        )}

                        {isDraft && (
                            <Section
                                title="Validación de la vacante"
                                description="Revisión automática previa a la publicación (RF-06)."
                                data-cy="validation-panel"
                            >
                                {validation.issues.length === 0 ? (
                                    <p
                                        className="text-tone-success-foreground flex items-start gap-2 text-sm"
                                        data-cy="validation-ok"
                                    >
                                        <CheckCircle2
                                            className="mt-0.5 size-4 shrink-0"
                                            aria-hidden="true"
                                        />
                                        La vacante cumple las validaciones y
                                        puede publicarse.
                                    </p>
                                ) : (
                                    <ul
                                        className="space-y-2.5"
                                        data-cy="validation-issues"
                                    >
                                        {validation.issues.map((issue) => (
                                            <li
                                                key={issue}
                                                className="text-tone-danger-foreground flex items-start gap-2 text-sm"
                                            >
                                                <XCircle
                                                    className="mt-0.5 size-4 shrink-0"
                                                    aria-hidden="true"
                                                />
                                                {issue}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </Section>
                        )}

                        {isDraft && validation.issues.length === 0 && (
                            <p className="text-muted-foreground flex items-start gap-2 px-1 text-xs leading-relaxed">
                                <ListChecks
                                    className="mt-0.5 size-4 shrink-0"
                                    aria-hidden="true"
                                />
                                Publicar la convocatoria la hace visible en el
                                portal público y habilita las postulaciones.
                            </p>
                        )}

                        {vacancy.closure_type && (
                            <Section title="Cierre">
                                <div className="space-y-3 text-sm">
                                    <StatusBadge
                                        status={vacancy.closure_type}
                                    />
                                    {vacancy.closure_notes && (
                                        <p className="leading-relaxed">
                                            {vacancy.closure_notes}
                                        </p>
                                    )}
                                </div>
                            </Section>
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
