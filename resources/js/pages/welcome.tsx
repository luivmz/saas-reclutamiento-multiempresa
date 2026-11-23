import { Head, Link, usePage } from '@inertiajs/react';
import {
    Activity,
    ArrowRight,
    BriefcaseBusiness,
    ClipboardList,
    FileStack,
    GraduationCap,
    Scale,
    ShieldCheck,
    Signature,
    type LucideIcon,
} from 'lucide-react';
import {
    SCHOOL_MEDIA,
    ScrollVideo,
} from '@/components/experience-3d/hero-folder-video';
import { RecruitmentDepth } from '@/components/experience-3d/recruitment-depth';
import { Reveal } from '@/components/reveal';
import { Button } from '@/components/ui/button';
import { dashboard, login } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

type RecordEntry = {
    icon: LucideIcon;
    title: string;
    status: string;
    detail: string;
    when: string;
    tone: string;
    iconTone: string;
};

const record: RecordEntry[] = [
    {
        icon: BriefcaseBusiness,
        title: 'Vacante',
        status: 'Convocatoria publicada',
        detail: 'Jefatura de RR. HH. · 3 criterios ponderados',
        when: '09 mar 2026',
        tone: 'bg-tone-primary text-tone-primary-foreground ring-tone-primary-edge',
        iconTone: 'bg-tone-primary text-tone-primary-foreground',
    },
    {
        icon: FileStack,
        title: 'Evidencias',
        status: 'Versión 2 · la anterior se conserva',
        detail: 'RR. HH. y evaluación asignada · fuente declarada',
        when: '18 mar 2026',
        tone: 'bg-tone-info text-tone-info-foreground ring-tone-info-edge',
        iconTone: 'bg-tone-info text-tone-info-foreground',
    },
    {
        icon: Signature,
        title: 'Decisión humana',
        status: 'Firmada por Dirección',
        detail: 'Dirección General · con justificación',
        when: '27 mar 2026',
        tone: 'bg-tone-success text-tone-success-foreground ring-tone-success-edge',
        iconTone: 'bg-tone-success text-tone-success-foreground',
    },
];

/** Lo mismo que muestran las hojas de la escena, dicho en texto. */
const pillars = [
    { icon: BriefcaseBusiness, text: 'Vacantes con criterios ponderados' },
    { icon: FileStack, text: 'Evidencias con versión y fuente' },
    { icon: Signature, text: 'Decisión humana justificada' },
];

const steps: { icon: LucideIcon; title: string; text: string }[] = [
    {
        icon: ClipboardList,
        title: 'Requerimiento',
        text: 'El área solicitante registra la necesidad, RR. HH. la valida y Dirección la aprueba o la observa.',
    },
    {
        icon: BriefcaseBusiness,
        title: 'Vacante',
        text: 'RR. HH. define el perfil, los criterios y sus ponderaciones, y publica la convocatoria.',
    },
    {
        icon: Scale,
        title: 'Evaluación',
        text: 'Evaluaciones y entrevistas con puntajes trazables, y un ranking ponderado que muestra su propio cálculo.',
    },
    {
        icon: Signature,
        title: 'Decisión',
        text: 'Una persona autorizada elige, justifica y registra. El sistema no selecciona por nadie.',
    },
];

/**
 * Quién interviene. Son los roles reales del producto (RF-01 a RF-27), no
 * personas: así se presenta el recorrido sin exponer cuentas ni contraseñas.
 */
const roles = [
    {
        role: 'Área solicitante',
        does: 'Registra la necesidad de personal y responde a las observaciones.',
    },
    {
        role: 'Recursos Humanos',
        does: 'Valida el requerimiento, configura la vacante y sus criterios, y gestiona postulaciones y evaluaciones.',
    },
    {
        role: 'Evaluación',
        does: 'Registra puntajes y observaciones de las evaluaciones y entrevistas que tiene asignadas.',
    },
    {
        role: 'Dirección',
        does: 'Aprueba el requerimiento y toma la decisión final, con confirmación y justificación.',
    },
    {
        role: 'Postulante',
        does: 'Completa su perfil, postula y consulta el estado de su postulación.',
    },
];

/** Lo que el producto se niega a hacer, dicho sin letra pequeña. */
const limits = [
    'No selecciona, descarta ni contrata a nadie automáticamente.',
    'No puntúa ni ordena a las personas con inteligencia artificial.',
    'No mezcla datos entre organizaciones: cada una ve solo los suyos.',
    'No permite borrar ni reescribir el registro de auditoría.',
];

export default function Welcome() {
    const { auth } = usePage().props;

    return (
        <>
            <Head title="Inicio" />

            <section className="school-hero" data-video-track>
                <div className="school-stage" data-video-stage>
                    <ScrollVideo media={SCHOOL_MEDIA} />
                    <div className="school-copy relative mx-auto w-full max-w-6xl px-4 py-7 sm:px-6 sm:py-10 lg:py-16">
                        <div className="max-w-[25rem] space-y-6">
                            <p className="bg-card text-muted-foreground inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium shadow-xs">
                                <GraduationCap
                                    className="text-primary size-4"
                                    aria-hidden="true"
                                />
                                Colegio Andino de Huancayo · caso de estudio con
                                datos ficticios
                            </p>
                            <h1 className="font-serif text-[2rem] leading-[1.06] font-semibold tracking-tight min-[360px]:text-4xl md:text-5xl lg:text-[3.35rem]">
                                Reclutamiento con evidencia,{' '}
                                <span className="text-teal-200">
                                    decisión con nombre propio
                                </span>
                            </h1>
                            <p className="max-w-xl text-base leading-relaxed text-teal-50/90 sm:text-lg">
                                Plataforma multiempresa para publicar vacantes,
                                reunir las evidencias de cada postulación con
                                sus versiones y llegar a una decisión que firma
                                una persona. El sistema ordena y explica; nunca
                                elige por nadie.
                            </p>
                            <div className="flex flex-wrap gap-3">
                                <Button
                                    size="lg"
                                    className="shadow-primary/20 shadow-md"
                                    asChild
                                >
                                    <Link href={jobsIndex()} data-cy="cta-jobs">
                                        Ver empleos disponibles
                                        <ArrowRight aria-hidden="true" />
                                    </Link>
                                </Button>
                                <Button
                                    size="lg"
                                    variant="outline"
                                    className="bg-card text-card-foreground"
                                    asChild
                                >
                                    <Link
                                        href={
                                            auth?.user ? dashboard() : login()
                                        }
                                        data-cy="cta-login"
                                    >
                                        {auth?.user
                                            ? 'Ir a mi panel'
                                            : 'Iniciar sesión'}
                                    </Link>
                                </Button>
                            </div>
                            <ul
                                className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-teal-50/90"
                                data-cy="landing-pillars"
                            >
                                {pillars.map(({ icon: Icon, text }) => (
                                    <li
                                        key={text}
                                        className="flex items-center gap-2"
                                    >
                                        <Icon
                                            className="size-4 shrink-0 text-teal-200"
                                            aria-hidden="true"
                                        />
                                        {text}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            <section
                className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:py-16"
                aria-labelledby="landing-process-title"
                data-cy="landing-process"
            >
                <div className="grid items-center gap-10 lg:grid-cols-2">
                    <div>
                        <h2
                            id="landing-process-title"
                            className="font-serif text-3xl font-semibold tracking-tight md:text-4xl"
                        >
                            Cómo avanza un proceso
                        </h2>
                        <ol className="mt-7 grid gap-x-8 gap-y-6 sm:grid-cols-2">
                            {steps.map((step) => (
                                <li key={step.title} className="border-t pt-4">
                                    <div className="flex items-center gap-3">
                                        <step.icon
                                            aria-hidden="true"
                                            className="text-primary size-4"
                                        />
                                        <h3 className="font-serif text-xl font-semibold">
                                            {step.title}
                                        </h3>
                                    </div>
                                    <p className="text-muted-foreground mt-2 text-sm leading-relaxed">
                                        {step.text}
                                    </p>
                                </li>
                            ))}
                        </ol>
                    </div>
                    {/* El expediente queda delante, plano y sólido: su texto
                        nunca depende del fondo para leerse. Detrás, la capa de
                        profundidad —decorativa y opcional (ADR-003)—. En
                        escritorio, el margen deja sitio para que asomen las
                        hojas de la escena. */}
                    <div className="lg:px-14 lg:py-24">
                        <div className="relative" data-cy="landing-folder">
                            <RecruitmentDepth />
                            <div className="bg-card relative z-10 rounded-xl border shadow-[0_24px_48px_-24px_oklch(0.25_0.04_220/0.35)]">
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
                                            key={entry.title}
                                            className="flex items-start gap-3 px-5 py-4"
                                        >
                                            <span
                                                className={`flex size-9 shrink-0 items-center justify-center rounded-lg ${entry.iconTone}`}
                                            >
                                                <entry.icon
                                                    className="size-4"
                                                    aria-hidden="true"
                                                />
                                            </span>
                                            <div className="min-w-0 flex-1 space-y-1">
                                                <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-0.5">
                                                    <p className="text-sm font-semibold">
                                                        {entry.title}
                                                    </p>
                                                    <p className="text-muted-foreground font-mono text-xs">
                                                        {entry.when}
                                                    </p>
                                                </div>
                                                <span
                                                    className={`inline-flex rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${entry.tone}`}
                                                >
                                                    {entry.status}
                                                </span>
                                                <p className="text-muted-foreground text-xs">
                                                    {entry.detail}
                                                </p>
                                            </div>
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
                </div>
            </section>

            <section
                className="bg-surface border-t"
                aria-labelledby="landing-roles-title"
                data-cy="landing-roles"
            >
                <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
                    <Reveal>
                        <h2
                            id="landing-roles-title"
                            className="font-serif text-2xl font-semibold tracking-tight md:text-3xl"
                        >
                            Quién interviene
                        </h2>
                        <p className="text-muted-foreground mt-2 max-w-2xl text-sm leading-relaxed">
                            Cada rol ve y hace solo lo que le corresponde,
                            dentro de su organización.
                        </p>
                    </Reveal>
                    <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
                        {roles.map((item, index) => (
                            <li key={item.role}>
                                <Reveal
                                    delay={index * 60}
                                    className="bg-card h-full rounded-xl border p-5"
                                >
                                    <h3 className="font-serif text-base font-semibold">
                                        {item.role}
                                    </h3>
                                    <p className="text-muted-foreground mt-2 text-sm leading-relaxed">
                                        {item.does}
                                    </p>
                                </Reveal>
                            </li>
                        ))}
                    </ul>
                </div>
            </section>

            <section className="border-t">
                <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 sm:px-6 lg:grid-cols-2">
                    <Reveal
                        className="flex flex-col gap-4 sm:flex-row sm:items-start"
                        data-cy="landing-limits"
                    >
                        <span className="bg-tone-primary text-tone-primary-foreground flex size-10 shrink-0 items-center justify-center rounded-lg">
                            <ShieldCheck
                                className="size-5"
                                aria-hidden="true"
                            />
                        </span>
                        <div className="space-y-3">
                            <h2 className="font-serif text-lg font-semibold">
                                Apoyo a la decisión, no reemplazo
                            </h2>
                            <p className="text-muted-foreground max-w-3xl text-sm leading-relaxed">
                                El sistema calcula puntajes ponderados y ordena
                                a los candidatos mostrando cómo obtuvo cada
                                resultado. La selección final la registra
                                siempre una persona autorizada, con su
                                justificación, y queda auditada.
                            </p>
                            <ul className="text-muted-foreground list-disc space-y-1 pl-5 text-sm leading-relaxed">
                                {limits.map((limit) => (
                                    <li key={limit}>{limit}</li>
                                ))}
                            </ul>
                            <p>
                                <Link
                                    href={jobsIndex()}
                                    className="text-primary text-sm font-medium underline underline-offset-4"
                                >
                                    Ver las convocatorias vigentes
                                </Link>
                            </p>
                        </div>
                    </Reveal>

                    <Reveal
                        delay={80}
                        className="flex flex-col gap-4 sm:flex-row sm:items-start"
                        data-cy="landing-ml-note"
                    >
                        <span className="bg-tone-primary text-tone-primary-foreground flex size-10 shrink-0 items-center justify-center rounded-lg">
                            <Activity className="size-5" aria-hidden="true" />
                        </span>
                        <div className="space-y-3">
                            <h2 className="font-serif text-lg font-semibold">
                                Riesgo operacional del proceso{' '}
                                <span className="text-muted-foreground font-sans text-sm font-normal">
                                    (experimental)
                                </span>
                            </h2>
                            <p className="text-muted-foreground max-w-3xl text-sm leading-relaxed">
                                Un modelo experimental, entrenado solo con datos
                                sintéticos, estima si un proceso de selección
                                corre riesgo de no cerrar a tiempo. Mide el
                                proceso, nunca a las personas postulantes, y no
                                interviene en el ranking ni en la decisión.
                            </p>
                            <p className="text-muted-foreground max-w-3xl text-sm leading-relaxed">
                                Es opcional: si el servicio no está disponible,
                                la plataforma funciona igual. No está validado
                                institucionalmente ni autorizado para
                                producción.
                            </p>
                        </div>
                    </Reveal>
                </div>
            </section>
        </>
    );
}
