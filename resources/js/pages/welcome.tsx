import { Head, Link, usePage } from '@inertiajs/react';
import { ShieldCheck } from 'lucide-react';
import { RecruitmentDepth } from '@/components/experience-3d/recruitment-depth';
import { Button } from '@/components/ui/button';
import { dashboard, login } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

/**
 * Portada pública.
 *
 * Lo primero que se ve no es una promesa, es un expediente: la cadena de
 * custodia de un requerimiento real del caso de estudio, con quién intervino
 * en cada paso. Es exactamente lo que hace el producto, así que sirve de
 * argumento mejor que cualquier eslogan.
 */
const record = [
    {
        stage: 'Requerimiento registrado',
        actor: 'Coordinación Académica',
        when: '02 mar 2026',
        tone: 'bg-tone-neutral text-tone-neutral-foreground ring-tone-neutral-edge',
    },
    {
        stage: 'Validado por RR. HH.',
        actor: 'Jefatura de Recursos Humanos',
        when: '04 mar 2026',
        tone: 'bg-tone-info text-tone-info-foreground ring-tone-info-edge',
    },
    {
        stage: 'Aprobado por Dirección',
        actor: 'Dirección General',
        when: '06 mar 2026',
        tone: 'bg-tone-success text-tone-success-foreground ring-tone-success-edge',
    },
    {
        stage: 'Convocatoria publicada',
        actor: 'Jefatura de Recursos Humanos',
        when: '09 mar 2026',
        tone: 'bg-tone-primary text-tone-primary-foreground ring-tone-primary-edge',
    },
];

const steps = [
    {
        title: 'Requerimiento',
        text: 'El área solicitante registra la necesidad, RR. HH. la valida y Dirección la aprueba o la observa.',
    },
    {
        title: 'Vacante',
        text: 'RR. HH. define el perfil, los criterios y sus ponderaciones, y publica la convocatoria.',
    },
    {
        title: 'Evaluación',
        text: 'Evaluaciones y entrevistas con puntajes trazables, y un ranking ponderado que muestra su propio cálculo.',
    },
    {
        title: 'Decisión',
        text: 'Una persona autorizada elige, justifica y registra. El sistema no selecciona por nadie.',
    },
];

export default function Welcome() {
    const { auth } = usePage().props;

    return (
        <>
            <Head title="Inicio" />

            <section className="bg-background border-b">
                <div className="mx-auto grid max-w-6xl gap-12 px-4 py-14 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:gap-16 lg:py-20">
                    <div className="space-y-7">
                        <p className="text-muted-foreground text-sm">
                            Caso de estudio: Colegio Andino de Huancayo
                            (demostración con datos ficticios)
                        </p>
                        <h1 className="font-serif text-4xl leading-[1.08] font-semibold tracking-tight md:text-5xl">
                            Todo el proceso de selección, con nombre y fecha en
                            cada paso
                        </h1>
                        <p className="text-muted-foreground max-w-xl text-lg leading-relaxed">
                            Plataforma SaaS multiempresa para reclutar, evaluar
                            y seleccionar personal. Cada requerimiento avanza
                            como un expediente y termina en una decisión que
                            firma una persona.
                        </p>
                        <div className="flex flex-wrap gap-3">
                            <Button size="lg" asChild>
                                <Link href={jobsIndex()} data-cy="cta-jobs">
                                    Ver empleos disponibles
                                </Link>
                            </Button>
                            <Button size="lg" variant="outline" asChild>
                                <Link
                                    href={auth?.user ? dashboard() : login()}
                                    data-cy="cta-login"
                                >
                                    {auth?.user
                                        ? 'Ir a mi panel'
                                        : 'Iniciar sesión'}
                                </Link>
                            </Button>
                        </div>
                    </div>

                    {/* El expediente queda delante, plano y sólido: su texto
                        nunca depende del fondo para leerse. Detrás, la capa de
                        profundidad —decorativa y opcional (ADR-003)—. */}
                    <div className="relative">
                        <RecruitmentDepth />
                        <div className="bg-card relative z-10 rounded-xl border shadow-sm">
                            <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1 border-b px-5 py-4">
                                <p className="font-mono text-sm font-medium">
                                    REQ-2026-0042
                                </p>
                                <p className="text-muted-foreground text-xs">
                                    Docente de Matemática, 2 plazas
                                </p>
                            </div>
                            <ol className="divide-y">
                                {record.map((entry) => (
                                    <li
                                        key={entry.stage}
                                        className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1 px-5 py-3.5"
                                    >
                                        <div className="min-w-0 space-y-0.5">
                                            <span
                                                className={`inline-flex rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${entry.tone}`}
                                            >
                                                {entry.stage}
                                            </span>
                                            <p className="text-muted-foreground text-xs">
                                                {entry.actor}
                                            </p>
                                        </div>
                                        <p className="text-muted-foreground font-mono text-xs">
                                            {entry.when}
                                        </p>
                                    </li>
                                ))}
                            </ol>
                            <p className="text-muted-foreground bg-surface rounded-b-xl px-5 py-3 text-xs">
                                Ejemplo ilustrativo. Los expedientes reales
                                viven dentro de la plataforma.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <section className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
                <h2 className="font-serif text-2xl font-semibold tracking-tight">
                    Cómo avanza un proceso
                </h2>
                <ol className="bg-border mt-8 grid gap-px overflow-hidden rounded-xl border sm:grid-cols-2 lg:grid-cols-4">
                    {steps.map((step, index) => (
                        <li key={step.title} className="bg-card p-5">
                            <p className="text-muted-foreground font-mono text-xs">
                                Paso {index + 1} de {steps.length}
                            </p>
                            <h3 className="mt-2 font-serif text-lg font-semibold">
                                {step.title}
                            </h3>
                            <p className="text-muted-foreground mt-2 text-sm leading-relaxed">
                                {step.text}
                            </p>
                        </li>
                    ))}
                </ol>
            </section>

            <section className="border-t">
                <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-10 sm:flex-row sm:items-start sm:px-6">
                    <ShieldCheck
                        className="text-primary size-6 shrink-0"
                        aria-hidden="true"
                    />
                    <div className="space-y-2">
                        <h2 className="font-serif text-lg font-semibold">
                            Apoyo a la decisión, no reemplazo
                        </h2>
                        <p className="text-muted-foreground max-w-3xl text-sm leading-relaxed">
                            El sistema calcula puntajes ponderados y ordena a
                            los candidatos mostrando cómo obtuvo cada resultado.
                            La selección final la registra siempre una persona
                            autorizada, con su justificación, y queda auditada.
                        </p>
                        <p>
                            <Link
                                href={jobsIndex()}
                                className="text-primary text-sm font-medium underline underline-offset-4"
                            >
                                Ver las convocatorias vigentes
                            </Link>
                        </p>
                    </div>
                </div>
            </section>
        </>
    );
}
