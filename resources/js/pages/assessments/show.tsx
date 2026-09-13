import { Form, Head } from '@inertiajs/react';
import { FileText, Lock } from 'lucide-react';
import AssessmentAssignmentController from '@/actions/App/Http/Controllers/Assessments/AssessmentAssignmentController';
import EvaluationController from '@/actions/App/Http/Controllers/Assessments/EvaluationController';
import InterviewController from '@/actions/App/Http/Controllers/Assessments/InterviewController';
import { FormField, NativeSelect } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { DetailList, PageContainer, PageHeader } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
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
    criteria: { id: number; name: string; weight: number; min_score: number; max_score: number }[];
    results: { criterion_id: number; score: number; comment: string | null }[];
    outcomes: Presented[];
    can: { record: boolean };
};

export default function AssessmentSession({ session, application, criteria, results, outcomes, can }: Props) {
    const isInterview = session.kind.value === 'entrevista';
    const action = isInterview
        ? InterviewController.recordResult.form(session.id)
        : EvaluationController.recordResult.form(session.id);
    const resultFor = (criterionId: number) => results.find((result) => result.criterion_id === criterionId);

    return (
        <>
            <Head title={`${session.title} · ${application.candidate.name}`} />
            <PageContainer className="max-w-5xl">
                <PageHeader
                    eyebrow={
                        <>
                            <StatusBadge status={session.kind} />
                            <StatusBadge status={session.status} />
                        </>
                    }
                    title={`${session.title}: ${application.candidate.name}`}
                    description={`${application.vacancy.code} · ${application.vacancy.title} · Postulación ${application.code}`}
                />

                <WorkflowAlert />

                <div className="grid gap-6 lg:grid-cols-3">
                    <div className="space-y-6 lg:col-span-2">
                        <Card data-cy="score-sheet">
                            <CardHeader>
                                <CardTitle>{isInterview ? 'Registro de la entrevista' : 'Registro de resultados'}</CardTitle>
                                <CardDescription>
                                    Cada puntaje debe estar dentro del rango del criterio (RF-20). Una vez registrado no se puede modificar.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                {can.record ? (
                                    <Form {...action} className="space-y-5">
                                        {({ errors, processing }) => (
                                            <>
                                                {criteria.map((criterion) => (
                                                    <div key={criterion.id} className="grid gap-3 rounded-lg border p-4 md:grid-cols-[2fr_1fr_2fr]" data-cy="score-row">
                                                        <div>
                                                            <p className="font-medium">{criterion.name}</p>
                                                            <p className="text-muted-foreground text-xs">
                                                                Rango {formatNumber(criterion.min_score)} – {formatNumber(criterion.max_score)} · Ponderación {formatNumber(criterion.weight)}
                                                            </p>
                                                        </div>
                                                        <div>
                                                            <Input
                                                                type="number"
                                                                step="0.01"
                                                                min={criterion.min_score}
                                                                max={criterion.max_score}
                                                                name={`scores[${criterion.id}][score]`}
                                                                aria-label={`Puntaje de ${criterion.name}`}
                                                                data-cy={`score-${criterion.id}`}
                                                            />
                                                            <InputError message={errors[`scores.${criterion.id}.score`]} />
                                                        </div>
                                                        <Input
                                                            name={`scores[${criterion.id}][comment]`}
                                                            placeholder="Comentario (opcional)"
                                                            aria-label={`Comentario de ${criterion.name}`}
                                                            data-cy={`score-comment-${criterion.id}`}
                                                        />
                                                    </div>
                                                ))}
                                                <InputError message={errors.scores} />
                                                {isInterview && (
                                                    <FormField label="Resultado de la entrevista" htmlFor="outcome" error={errors.outcome}>
                                                        <NativeSelect id="outcome" name="outcome" options={outcomes} placeholder="Seleccione…" data-cy="interview-outcome" />
                                                    </FormField>
                                                )}
                                                <FormField
                                                    label={isInterview ? 'Observaciones de la entrevista' : 'Observaciones (opcional)'}
                                                    htmlFor="observations"
                                                    error={errors.observations}
                                                >
                                                    <Textarea id="observations" name="observations" rows={4} data-cy="session-observations" />
                                                </FormField>
                                                <div className="flex justify-end">
                                                    <Button type="submit" disabled={processing} data-cy="record-results">
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
                                                <Lock className="size-4" />
                                                No hay resultados registrados y usted no puede registrarlos en esta sesión.
                                            </p>
                                        ) : (
                                            <table className="w-full text-sm" data-cy="recorded-results">
                                                <thead className="text-muted-foreground border-b text-left text-xs uppercase">
                                                    <tr>
                                                        <th className="py-2 font-medium">Criterio</th>
                                                        <th className="py-2 text-right font-medium">Puntaje</th>
                                                        <th className="py-2 pl-4 font-medium">Comentario</th>
                                                    </tr>
                                                </thead>
                                                <tbody className="divide-y">
                                                    {criteria.map((criterion) => (
                                                        <tr key={criterion.id}>
                                                            <td className="py-2">{criterion.name}</td>
                                                            <td className="py-2 text-right tabular-nums">
                                                                {formatNumber(resultFor(criterion.id)?.score)} / {formatNumber(criterion.max_score)}
                                                            </td>
                                                            <td className="text-muted-foreground py-2 pl-4">{resultFor(criterion.id)?.comment ?? '—'}</td>
                                                        </tr>
                                                    ))}
                                                </tbody>
                                            </table>
                                        )}
                                        {session.outcome && (
                                            <p className="flex items-center gap-2 text-sm">
                                                Resultado: <StatusBadge status={session.outcome} />
                                            </p>
                                        )}
                                        {session.observations && <p className="text-sm whitespace-pre-line">{session.observations}</p>}
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>

                    <div className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Convocatoria</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <DetailList
                                    className="sm:grid-cols-1"
                                    items={[
                                        { label: 'Fecha y hora', value: formatDateTime(session.scheduled_at) },
                                        { label: 'Duración', value: session.duration_minutes ? `${session.duration_minutes} min` : '—' },
                                        { label: 'Modalidad', value: session.modality.label },
                                        { label: 'Lugar o enlace', value: session.location },
                                        { label: 'Indicaciones', value: session.instructions ?? '—' },
                                        { label: 'Registrada', value: formatDateTime(session.completed_at) },
                                    ]}
                                />
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader>
                                <CardTitle>Candidato</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <DetailList
                                    className="sm:grid-cols-1"
                                    items={[
                                        { label: 'Título u ocupación', value: application.candidate.professional_title ?? '—' },
                                        { label: 'Nivel educativo', value: application.candidate.education_level ?? '—' },
                                        { label: 'Experiencia', value: application.candidate.years_of_experience !== null ? `${application.candidate.years_of_experience} años` : '—' },
                                    ]}
                                />
                                {application.cv && (
                                    <a href={application.cv.download_url} className="hover:bg-accent flex items-center gap-2 rounded-lg border p-3 text-sm" data-cy="session-cv">
                                        <FileText className="text-muted-foreground size-4" />
                                        Descargar CV
                                    </a>
                                )}
                            </CardContent>
                        </Card>
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
