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
import { ApplicationRequirements } from '@/components/jobs/application-requirements';
import { Reveal } from '@/components/reveal';
import { Button } from '@/components/ui/button';
import { dashboard, login, register } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';
import type { ApplicationRequirements as Requirements } from '@/types';

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

/**
 * Lo que encuentra quien postula. Siguen las tres hojas de la escena —vacante,
 * expediente y decisión—, dichas desde el lado del postulante.
 */
const pillars = [
    { icon: BriefcaseBusiness, text: 'Perfil y criterios de cada puesto' },
    { icon: FileStack, text: 'Postulación y seguimiento en línea' },
    { icon: Signature, text: 'Decisión final de una persona' },
];

/** Cómo postular, en el orden real del sistema. */
const applySteps: { title: string; text: string }[] = [
    {
        title: 'Elija una convocatoria',
        text: 'Revise el perfil del puesto, los criterios de evaluación y la fecha de cierre.',
    },
    {
        title: 'Cree su cuenta de postulante',
        text: 'Con su nombre, un correo y una contraseña. Si ya tiene cuenta, inicie sesión.',
    },
    {
        title: 'Complete su perfil y cargue su CV',
        text: 'Desde Mi perfil, con los datos que se indican en «Qué tener listo».',
    },
    {
        title: 'Postule y siga su avance',
        text: 'Postule desde la convocatoria. La etapa se consulta en Mis postulaciones y los cambios llegan a Notificaciones.',
    },
];

/** «Hoy hay 3 convocatorias…»: cuenta solo las que aceptan postulaciones. */
function openVacanciesText(count: number): string {
    if (count === 0) {
        return 'Hoy no hay convocatorias recibiendo postulaciones.';
    }

    return count === 1
        ? 'Hoy hay 1 convocatoria recibiendo postulaciones.'
        : `Hoy hay ${count} convocatorias recibiendo postulaciones.`;
}

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

export default function Welcome({
    convocatoriasAbiertas,
    requisitos,
}: {
    convocatoriasAbiertas: number;
    requisitos: Requirements;
}) {
    const { auth } = usePage().props;

    return (
        <>
            <Head title="Inicio" />

            <section className="school-hero" data-video-track>
                <div className="school-stage" data-video-stage>
                    <ScrollVideo media={SCHOOL_MEDIA} />
                    <div className="school-copy relative mx-auto w-full max-w-6xl px-4 py-7 [overflow-wrap:anywhere] sm:px-6 sm:py-10 lg:py-16">
                        <div className="max-w-[25rem] space-y-6">
                            <p className="bg-card text-muted-foreground inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium shadow-xs">
                                <GraduationCap
                                    className="text-primary size-4 shrink-0"
                                    aria-hidden="true"
                                />
                                Colegio Andino de Huancayo · caso de estudio con
                                datos ficticios
                            </p>
                            <h1 className="font-serif text-[2rem] leading-[1.06] font-semibold tracking-tight min-[360px]:text-4xl md:text-5xl lg:text-[3.35rem]">
                                Revise las convocatorias{' '}
                                <span className="text-teal-200">
                                    y postule en línea
                                </span>
                            </h1>
                            <p className="max-w-xl text-base leading-relaxed text-teal-50/90 sm:text-lg">
                                Cada convocatoria muestra el perfil del puesto,
                                sus criterios de evaluación y su fecha de
                                cierre. Cree su cuenta, complete su perfil con
                                su CV y siga su postulación desde aquí.
                            </p>
                            <p
                                className="flex items-center gap-2 text-sm font-medium text-teal-50"
                                data-cy="open-vacancies-count"
                            >
                                <BriefcaseBusiness
                                    className="size-4 shrink-0 text-teal-200"
                                    aria-hidden="true"
                                />
                                {openVacanciesText(convocatoriasAbiertas)}
                            </p>
                            <div className="flex flex-wrap gap-3 max-sm:[&>a]:h-auto max-sm:[&>a]:min-h-11 max-sm:[&>a]:max-w-full max-sm:[&>a]:text-center max-sm:[&>a]:whitespace-normal">
                                <Button
                                    size="lg"
                                    className="shadow-primary/20 shadow-md"
                                    asChild
                                >
                                    <Link href={jobsIndex()} data-cy="cta-jobs">
                                        Ver convocatorias
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
                aria-labelledby="landing-apply-title"
                data-cy="landing-apply"
            >
                <div className="grid grid-cols-1 gap-10 [overflow-wrap:anywhere] lg:grid-cols-[3fr_2fr]">
                    <div>
                        <h2
                            id="landing-apply-title"
                            className="font-serif text-3xl font-semibold tracking-tight md:text-4xl"
                        >
                            Cómo postular
                        </h2>
                        <ol className="mt-7 grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
                            {applySteps.map((step, index) => (
                                <li
                                    key={step.title}
                                    className="flex items-start gap-3 border-t pt-4"
                                >
                                    <span
                                        className="bg-tone-primary text-tone-primary-foreground flex size-7 shrink-0 items-center justify-center rounded-full text-sm font-semibold"
                                        aria-hidden="true"
                                    >
                                        {index + 1}
                                    </span>
                                    <div>
                                        <h3 className="font-serif text-lg font-semibold">
                                            {step.title}
                                        </h3>
                                        <p className="text-muted-foreground mt-1 text-sm leading-relaxed">
                                            {step.text}
                                        </p>
                                    </div>
                                </li>
                            ))}
                        </ol>
                    </div>
                    <div
                        className="bg-card h-fit space-y-4 rounded-xl border p-5"
                        data-cy="landing-requirements"
                    >
                        <h3 className="font-serif text-xl font-semibold">
                            Qué tener listo
                        </h3>
                        <ApplicationRequirements requirements={requisitos} />
                        <p className="text-muted-foreground border-t pt-4 text-sm leading-relaxed">
                            Cada convocatoria indica además su propio perfil del
                            puesto —formación, experiencia, funciones y
                            competencias— y los criterios con que se evaluará.
                        </p>
                        {!auth?.user && (
                            <p className="flex flex-wrap gap-x-4 gap-y-2 text-sm">
                                <Link
                                    href={register()}
                                    className="text-primary font-medium underline underline-offset-4"
                                    data-cy="landing-register"
                                >
                                    Crear cuenta de postulante
                                </Link>
                            </p>
                        )}
                    </div>
                </div>
            </section>

            <section
                className="bg-surface border-t"
                aria-labelledby="landing-process-title"
                data-cy="landing-process"
            >
                <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:py-16">
                    <div className="grid grid-cols-1 items-center gap-10 [overflow-wrap:anywhere] lg:grid-cols-2">
                        <div>
                            <h2
                                id="landing-process-title"
                                className="font-serif text-3xl font-semibold tracking-tight md:text-4xl"
                            >
                                Cómo avanza un proceso
                            </h2>
                            <p className="text-muted-foreground mt-2 max-w-xl text-sm leading-relaxed">
                                Lo que ocurre del lado de la institución, desde
                                que se pide un puesto hasta la decisión.
                            </p>
                            <ol className="mt-7 grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
                                {steps.map((step) => (
                                    <li
                                        key={step.title}
                                        className="border-t pt-4"
                                    >
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
                                        Ejemplo ilustrativo. Los expedientes
                                        reales viven dentro de la plataforma.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section
                className="border-t"
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
                    <ul className="mt-8 grid grid-cols-1 gap-4 [overflow-wrap:anywhere] sm:grid-cols-2 lg:grid-cols-5">
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

            <section className="bg-surface border-t">
                <div className="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-4 py-14 [overflow-wrap:anywhere] sm:px-6 lg:grid-cols-2">
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
