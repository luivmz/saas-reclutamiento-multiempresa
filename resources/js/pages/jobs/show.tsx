import { Form, Head, Link, usePage } from '@inertiajs/react';
import { ArrowLeft, CalendarClock, MapPin, Users } from 'lucide-react';
import ApplyController from '@/actions/App/Http/Controllers/Candidates/ApplyController';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import CandidateProfileController from '@/actions/App/Http/Controllers/Candidates/CandidateProfileController';
import { Section } from '@/components/page';
import { StatusBadge } from '@/components/status-badge';
import { CriteriaTable } from '@/components/vacancies/criteria-table';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { formatDate } from '@/lib/format';
import { login, register } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';
import type { Presented, Vacancy } from '@/types';

type CandidateContext = {
    profileComplete: boolean;
    hasCv: boolean;
    application: { id: number; status: Presented } | null;
} | null;

export default function JobShow({
    vacancy,
    candidate,
}: {
    vacancy: Vacancy;
    candidate: CandidateContext;
}) {
    const { auth } = usePage().props;

    const facts = [
        { icon: MapPin, label: 'Ubicación', value: vacancy.location },
        {
            icon: Users,
            label: 'Plazas',
            value: `${vacancy.positions} plaza${vacancy.positions === 1 ? '' : 's'}, ${vacancy.contract_type.label}`,
        },
        {
            icon: CalendarClock,
            label: 'Cierre de postulaciones',
            value: formatDate(vacancy.closes_at),
        },
    ];

    return (
        <>
            <Head title={vacancy.title} />
            <div className="mx-auto max-w-6xl space-y-6 px-4 py-8 sm:px-6">
                <Link
                    href={jobsIndex()}
                    className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1.5 text-sm"
                >
                    <ArrowLeft className="size-4" aria-hidden="true" />
                    Volver a empleos
                </Link>

                <WorkflowAlert />

                <header className="space-y-3 border-b pb-6">
                    <p className="text-muted-foreground text-sm">
                        {vacancy.organization?.name}
                    </p>
                    <h1
                        className="font-serif text-3xl font-semibold tracking-tight"
                        data-cy="page-title"
                    >
                        {vacancy.title}
                    </h1>
                    <p className="text-muted-foreground font-mono text-xs">
                        {vacancy.code}
                    </p>
                </header>

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <div className="min-w-0 space-y-6 lg:col-span-2">
                        <Section title="La convocatoria">
                            <p className="text-sm leading-relaxed whitespace-pre-line">
                                {vacancy.summary}
                            </p>
                        </Section>

                        {vacancy.profile && (
                            <Section title="Perfil del puesto">
                                <dl className="grid gap-6 sm:grid-cols-2">
                                    {[
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
                                            value: vacancy.profile.functions,
                                        },
                                        {
                                            label: 'Competencias',
                                            value: vacancy.profile.competencies,
                                        },
                                    ].map((item) => (
                                        <div
                                            key={item.label}
                                            className="space-y-1"
                                        >
                                            <dt className="text-sm font-medium">
                                                {item.label}
                                            </dt>
                                            <dd className="text-muted-foreground text-sm leading-relaxed whitespace-pre-line">
                                                {item.value}
                                            </dd>
                                        </div>
                                    ))}
                                </dl>
                            </Section>
                        )}

                        <Section
                            title="Criterios de evaluación"
                            description="Con estos criterios y estas ponderaciones se evaluará a quienes postulen."
                        >
                            <CriteriaTable criteria={vacancy.criteria ?? []} />
                        </Section>
                    </div>

                    <div
                        className="bg-card h-fit min-w-0 rounded-xl border lg:sticky lg:top-6"
                        data-cy="apply-panel"
                    >
                        <div className="space-y-4 border-b px-5 py-5">
                            <StatusBadge status={vacancy.status} />
                            <dl className="space-y-3 text-sm">
                                {facts.map((fact) => (
                                    <div
                                        key={fact.label}
                                        className="flex items-start gap-2.5"
                                    >
                                        <fact.icon
                                            className="text-muted-foreground mt-0.5 size-4 shrink-0"
                                            aria-hidden="true"
                                        />
                                        <div>
                                            <dt className="text-muted-foreground text-xs">
                                                {fact.label}
                                            </dt>
                                            <dd>{fact.value}</dd>
                                        </div>
                                    </div>
                                ))}
                            </dl>
                        </div>

                        <div className="space-y-3 px-5 py-5">
                            {!auth?.user && (
                                <>
                                    <p className="text-muted-foreground text-sm">
                                        Para postular necesita una cuenta de
                                        postulante.
                                    </p>
                                    <Button asChild className="w-full">
                                        <Link
                                            href={register()}
                                            data-cy="apply-register"
                                        >
                                            Crear cuenta
                                        </Link>
                                    </Button>
                                    <Button
                                        asChild
                                        variant="outline"
                                        className="w-full"
                                    >
                                        <Link
                                            href={login()}
                                            data-cy="apply-login"
                                        >
                                            Ya tengo cuenta
                                        </Link>
                                    </Button>
                                </>
                            )}

                            {candidate && (
                                <div
                                    className="space-y-3"
                                    data-cy="candidate-apply"
                                >
                                    {candidate.application ? (
                                        <>
                                            <p className="text-sm">
                                                Ya postuló a esta convocatoria.
                                            </p>
                                            <StatusBadge
                                                status={
                                                    candidate.application.status
                                                }
                                            />
                                            <Button
                                                asChild
                                                variant="outline"
                                                className="w-full"
                                            >
                                                <Link
                                                    href={CandidateApplicationController.show(
                                                        candidate.application
                                                            .id,
                                                    )}
                                                    data-cy="view-my-application"
                                                >
                                                    Ver mi postulación
                                                </Link>
                                            </Button>
                                        </>
                                    ) : !vacancy.accepts_applications ? (
                                        <p
                                            className="text-muted-foreground text-sm"
                                            data-cy="vacancy-not-accepting"
                                        >
                                            La convocatoria no está recibiendo
                                            postulaciones.
                                        </p>
                                    ) : !(
                                          candidate.profileComplete &&
                                          candidate.hasCv
                                      ) ? (
                                        <>
                                            <p className="text-muted-foreground text-sm">
                                                Complete su perfil y cargue su
                                                CV para postular.
                                            </p>
                                            <Button asChild className="w-full">
                                                <Link
                                                    href={CandidateProfileController.edit()}
                                                    data-cy="complete-profile"
                                                >
                                                    Completar perfil
                                                </Link>
                                            </Button>
                                        </>
                                    ) : (
                                        <Form
                                            {...ApplyController.form(
                                                vacancy.id,
                                            )}
                                        >
                                            {({ processing }) => (
                                                <Button
                                                    type="submit"
                                                    className="w-full"
                                                    disabled={processing}
                                                    data-cy="apply-button"
                                                >
                                                    {processing && <Spinner />}
                                                    Postular a esta vacante
                                                </Button>
                                            )}
                                        </Form>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
