import { Form, Head, Link, usePage } from '@inertiajs/react';
import { ArrowLeft, Building2, CalendarClock, MapPin, Users } from 'lucide-react';
import ApplyController from '@/actions/App/Http/Controllers/Candidates/ApplyController';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import CandidateProfileController from '@/actions/App/Http/Controllers/Candidates/CandidateProfileController';
import { StatusBadge } from '@/components/status-badge';
import { CriteriaTable } from '@/components/vacancies/criteria-table';
import { WorkflowAlert } from '@/components/workflow-alert';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
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

export default function JobShow({ vacancy, candidate }: { vacancy: Vacancy; candidate: CandidateContext }) {
    const { auth } = usePage().props;

    return (
        <>
            <Head title={vacancy.title} />
            <div className="mx-auto max-w-6xl space-y-6 px-4 py-8 md:px-6">
                <Link href={jobsIndex()} className="text-muted-foreground inline-flex items-center gap-1 text-sm hover:underline">
                    <ArrowLeft className="size-4" />
                    Volver a empleos
                </Link>
                <WorkflowAlert />
                <div className="grid gap-6 lg:grid-cols-3">
                    <div className="space-y-6 lg:col-span-2">
                        <Card>
                            <CardHeader className="gap-2">
                                <CardDescription className="flex items-center gap-1.5">
                                    <Building2 className="size-4" />
                                    {vacancy.organization?.name}
                                </CardDescription>
                                <CardTitle className="text-2xl" data-cy="page-title">{vacancy.title}</CardTitle>
                                <p className="text-muted-foreground font-mono text-xs">{vacancy.code}</p>
                            </CardHeader>
                            <CardContent className="space-y-6 text-sm">
                                <p className="whitespace-pre-line">{vacancy.summary}</p>
                                {vacancy.profile && (
                                    <div className="grid gap-5 sm:grid-cols-2">
                                        <section className="space-y-1">
                                            <h3 className="font-semibold">Formación académica</h3>
                                            <p className="text-muted-foreground">{vacancy.profile.education}</p>
                                        </section>
                                        <section className="space-y-1">
                                            <h3 className="font-semibold">Experiencia</h3>
                                            <p className="text-muted-foreground">{vacancy.profile.experience}</p>
                                        </section>
                                        <section className="space-y-1">
                                            <h3 className="font-semibold">Funciones</h3>
                                            <p className="text-muted-foreground whitespace-pre-line">{vacancy.profile.functions}</p>
                                        </section>
                                        <section className="space-y-1">
                                            <h3 className="font-semibold">Competencias</h3>
                                            <p className="text-muted-foreground whitespace-pre-line">{vacancy.profile.competencies}</p>
                                        </section>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader>
                                <CardTitle>Criterios de evaluación</CardTitle>
                                <CardDescription>Criterios y ponderaciones con los que se evaluará a los candidatos.</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <CriteriaTable criteria={vacancy.criteria ?? []} />
                            </CardContent>
                        </Card>
                    </div>
                    <Card className="h-fit" data-cy="apply-panel">
                        <CardHeader>
                            <CardTitle>Resumen</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4 text-sm">
                            <StatusBadge status={vacancy.status} />
                            <p className="flex items-center gap-2"><MapPin className="text-muted-foreground size-4" />{vacancy.location}</p>
                            <p className="flex items-center gap-2"><Users className="text-muted-foreground size-4" />{vacancy.positions} plaza(s) · {vacancy.contract_type.label}</p>
                            <p className="flex items-center gap-2"><CalendarClock className="text-muted-foreground size-4" />Postulaciones hasta el {formatDate(vacancy.closes_at)}</p>

                            {!auth?.user && (
                                <div className="space-y-2 border-t pt-4">
                                    <p className="text-muted-foreground">Para postular necesita una cuenta de postulante.</p>
                                    <Button asChild className="w-full">
                                        <Link href={register()} data-cy="apply-register">Crear cuenta</Link>
                                    </Button>
                                    <Button asChild variant="outline" className="w-full">
                                        <Link href={login()} data-cy="apply-login">Ya tengo cuenta</Link>
                                    </Button>
                                </div>
                            )}

                            {candidate && (
                                <div className="space-y-3 border-t pt-4" data-cy="candidate-apply">
                                    {candidate.application ? (
                                        <>
                                            <p>Ya postuló a esta convocatoria.</p>
                                            <StatusBadge status={candidate.application.status} />
                                            <Button asChild variant="outline" className="w-full">
                                                <Link href={CandidateApplicationController.show(candidate.application.id)} data-cy="view-my-application">
                                                    Ver mi postulación
                                                </Link>
                                            </Button>
                                        </>
                                    ) : !vacancy.accepts_applications ? (
                                        <p className="text-muted-foreground" data-cy="vacancy-not-accepting">
                                            La convocatoria no está recibiendo postulaciones.
                                        </p>
                                    ) : !(candidate.profileComplete && candidate.hasCv) ? (
                                        <>
                                            <p className="text-muted-foreground">Complete su perfil y cargue su CV para postular.</p>
                                            <Button asChild className="w-full">
                                                <Link href={CandidateProfileController.edit()} data-cy="complete-profile">Completar perfil</Link>
                                            </Button>
                                        </>
                                    ) : (
                                        <Form {...ApplyController.form(vacancy.id)}>
                                            {({ processing }) => (
                                                <Button type="submit" className="w-full" disabled={processing} data-cy="apply-button">
                                                    {processing && <Spinner />}
                                                    Postular a esta vacante
                                                </Button>
                                            )}
                                        </Form>
                                    )}
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </>
    );
}
