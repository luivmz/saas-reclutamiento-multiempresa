import { Form, Head } from '@inertiajs/react';
import { FileText, Lock } from 'lucide-react';
import AssessmentAssignmentController from '@/actions/App/Http/Controllers/Assessments/AssessmentAssignmentController';
import EvaluationController from '@/actions/App/Http/Controllers/Assessments/EvaluationController';
import InterviewController from '@/actions/App/Http/Controllers/Assessments/InterviewController';
import { FormField, NativeSelect } from '@/components/form-controls';
import InputError from '@/components/input-error';
import {
    DetailList,
    PageContainer,
    PageHeader,
    Section,
} from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime, formatNumber } from '@/lib/format';
import type { AssessmentSummary, DocumentSummary, Presented } from '@/types';

type Props = {
    session: AssessmentSummary;
    application: {
        id: number;
        code: string;
        vacancy: { code: string; title: string };
        candidate: {
            name: string;
            professional_title: string | null;
            years_of_experience: number | null;
            education_level: string | null;
        };
        cv: DocumentSummary | null;
    };
    criteria: {
        id: number;
        name: string;
        weight: number;
        min_score: number;
        max_score: number;
    }[];
    results: { criterion_id: number; score: number; comment: string | null }[];
    outcomes: Presented[];
    can: { record: boolean };
};

export default function AssessmentSession({
    session,
    application,
    criteria,
    results,
    outcomes,
    can,
}: Props) {
    const isInterview = session.kind.value === 'entrevista';
    const action = isInterview
        ? InterviewController.recordResult.form(session.id)
        : EvaluationController.recordResult.form(session.id);
    const resultFor = (criterionId: number) =>
        results.find((result) => result.criterion_id === criterionId);

    return (
        <>
            <Head title={`${session.title} de ${application.candidate.name}`} />
            <PageContainer className="max-w-5xl">
                <PageHeader
                    eyebrow={
                        <>
                            <StatusBadge status={session.kind} />
                            <StatusBadge status={session.status} />
                        </>
                    }
                    title={`${session.title}: ${application.candidate.name}`}
                    description={`Vacante ${application.vacancy.title} (${application.vacancy.code}). Postulación ${application.code}.`}
                />

                <WorkflowAlert />

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <div className="min-w-0 lg:col-span-2">
                        <Section
                            title={
                                isInterview
                                    ? 'Registro de la entrevista'
                                    : 'Registro de resultados'
                            }
                            description="Cada puntaje debe estar dentro del rango de su criterio (RF-20). Una vez registrado no se puede modificar."
                            data-cy="score-sheet"
                        >
                            {can.record ? (
                                <Form {...action} className="space-y-5">
                                    {({ errors, processing }) => (
                                        <>
                                            {criteria.map((criterion) => (
                                                <fieldset
                                                    key={criterion.id}
                                                    className="grid gap-3 rounded-lg border p-4 md:grid-cols-[2fr_1fr_2fr]"
                                                    data-cy="score-row"
                                                >
                                                    <legend className="sr-only">
                                                        {criterion.name}
                                                    </legend>
                                                    <div>
                                                        <p className="font-medium">
                                                            {criterion.name}
                                                        </p>
                                                        <p className="text-muted-foreground text-xs leading-relaxed">
                                                            Escala{' '}
                                                            {formatNumber(
                                                                criterion.min_score,
                                                            )}
                                                            –
                                                            {formatNumber(
                                                                criterion.max_score,
                                                            )}
                                                            , ponderación{' '}
                                                            {formatNumber(
                                                                criterion.weight,
                                                            )}
                                                        </p>
                                                    </div>
                                                    <div className="space-y-1.5">
                                                        <Input
                                                            type="number"
                                                            step="0.01"
                                                            min={
                                                                criterion.min_score
                                                            }
                                                            max={
                                                                criterion.max_score
                                                            }
                                                            name={`scores[${criterion.id}][score]`}
                                                            aria-label={`Puntaje de ${criterion.name}`}
                                                            aria-invalid={
                                                                errors[
                                                                    `scores.${criterion.id}.score`
                                                                ]
                                                                    ? true
                                                                    : undefined
                                                            }
                                                            data-cy={`score-${criterion.id}`}
                                                        />
                                                        <InputError
                                                            message={
                                                                errors[
                                                                    `scores.${criterion.id}.score`
                                                                ]
                                                            }
                                                        />
                                                    </div>
                                                    <Input
                                                        name={`scores[${criterion.id}][comment]`}
                                                        placeholder="Comentario (opcional)"
                                                        aria-label={`Comentario de ${criterion.name}`}
                                                        data-cy={`score-comment-${criterion.id}`}
                                                    />
                                                </fieldset>
                                            ))}

                                            <InputError
                                                message={errors.scores}
                                            />

                                            {isInterview && (
                                                <FormField
                                                    label="Resultado de la entrevista"
                                                    htmlFor="outcome"
                                                    error={errors.outcome}
                                                    required
                                                >
                                                    <NativeSelect
                                                        id="outcome"
                                                        name="outcome"
                                                        options={outcomes}
                                                        placeholder="Seleccione…"
                                                        data-cy="interview-outcome"
                                                    />
                                                </FormField>
                                            )}

                                            <FormField
                                                label={
                                                    isInterview
                                                        ? 'Observaciones de la entrevista'
                                                        : 'Observaciones (opcional)'
                                                }
                                                htmlFor="observations"
                                                error={errors.observations}
                                            >
                                                <Textarea
                                                    id="observations"
                                                    name="observations"
                                                    rows={4}
                                                    data-cy="session-observations"
                                                />
                                            </FormField>

                                            <div className="flex justify-end">
                                                <Button
                                                    type="submit"
                                                    disabled={processing}
                                                    data-cy="record-results"
                                                >
                                                    {processing && <Spinner />}
                                                    Registrar resultados
                                                </Button>
                                            </div>
                                        </>
                                    )}
                                </Form>
                            ) : (
                                <div className="space-y-4">
                                    {results.length === 0 ? (
                                        <p className="text-muted-foreground flex items-center gap-2 text-sm">
                                            <Lock
                                                className="size-4"
                                                aria-hidden="true"
                                            />
                                            No hay resultados registrados y
                                            usted no puede registrarlos en esta
                                            sesión.
                                        </p>
                                    ) : (
                                        <table
                                            className="w-full text-sm"
                                            data-cy="recorded-results"
                                        >
                                            <caption className="sr-only">
                                                Puntajes registrados en la
                                                sesión
                                            </caption>
                                            <thead className="text-muted-foreground border-b text-left text-xs">
                                                <tr>
                                                    <th
                                                        scope="col"
                                                        className="py-2 font-medium"
                                                    >
                                                        Criterio
                                                    </th>
                                                    <th
                                                        scope="col"
                                                        className="py-2 text-right font-medium"
                                                    >
                                                        Puntaje
                                                    </th>
                                                    <th
                                                        scope="col"
                                                        className="py-2 pl-4 font-medium"
                                                    >
                                                        Comentario
                                                    </th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y">
                                                {criteria.map((criterion) => (
                                                    <tr key={criterion.id}>
                                                        <th
                                                            scope="row"
                                                            className="py-2 text-left font-normal"
                                                        >
                                                            {criterion.name}
                                                        </th>
                                                        <td className="py-2 text-right font-mono tabular-nums">
                                                            {formatNumber(
                                                                resultFor(
                                                                    criterion.id,
                                                                )?.score,
                                                            )}{' '}
                                                            /{' '}
                                                            {formatNumber(
                                                                criterion.max_score,
                                                            )}
                                                        </td>
                                                        <td className="text-muted-foreground py-2 pl-4">
                                                            {resultFor(
                                                                criterion.id,
                                                            )?.comment ?? '—'}
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    )}
                                    {session.outcome && (
                                        <p className="flex flex-wrap items-center gap-2 text-sm">
                                            Resultado:{' '}
                                            <StatusBadge
                                                status={session.outcome}
                                            />
                                        </p>
                                    )}
                                    {session.observations && (
                                        <p className="bg-surface rounded-md px-3 py-2 text-sm leading-relaxed whitespace-pre-line">
                                            {session.observations}
                                        </p>
                                    )}
                                </div>
                            )}
                        </Section>
                    </div>

                    <div className="min-w-0 space-y-6">
                        <Section title="Convocatoria">
                            <DetailList
                                className="sm:grid-cols-1"
                                items={[
                                    {
                                        label: 'Fecha y hora',
                                        value: formatDateTime(
                                            session.scheduled_at,
                                        ),
                                    },
                                    {
                                        label: 'Duración',
                                        value: session.duration_minutes
                                            ? `${session.duration_minutes} minutos`
                                            : '—',
                                    },
                                    {
                                        label: 'Modalidad',
                                        value: session.modality.label,
                                    },
                                    {
                                        label: 'Lugar o enlace',
                                        value: session.location,
                                    },
                                    {
                                        label: 'Indicaciones',
                                        value: session.instructions ?? '—',
                                    },
                                    {
                                        label: 'Registrada',
                                        value: formatDateTime(
                                            session.completed_at,
                                        ),
                                    },
                                ]}
                            />
                        </Section>

                        <Section title="Candidato">
                            <div className="space-y-4">
                                <DetailList
                                    className="sm:grid-cols-1"
                                    items={[
                                        {
                                            label: 'Título u ocupación',
                                            value:
                                                application.candidate
                                                    .professional_title ?? '—',
                                        },
                                        {
                                            label: 'Nivel educativo',
                                            value:
                                                application.candidate
                                                    .education_level ?? '—',
                                        },
                                        {
                                            label: 'Experiencia',
                                            value:
                                                application.candidate
                                                    .years_of_experience !==
                                                null
                                                    ? `${application.candidate.years_of_experience} años`
                                                    : '—',
                                        },
                                    ]}
                                />
                                {application.cv && (
                                    <a
                                        href={application.cv.download_url}
                                        className="hover:bg-surface flex items-center gap-2 rounded-lg border p-3 text-sm transition-colors"
                                        data-cy="session-cv"
                                    >
                                        <FileText
                                            className="text-muted-foreground size-4"
                                            aria-hidden="true"
                                        />
                                        Descargar CV
                                    </a>
                                )}
                            </div>
                        </Section>
                    </div>
                </div>
            </PageContainer>
        </>
    );
}

AssessmentSession.layout = {
    breadcrumbs: [
        { title: 'Mis evaluaciones', href: AssessmentAssignmentController() },
        { title: 'Sesión', href: AssessmentAssignmentController() },
    ],
};
