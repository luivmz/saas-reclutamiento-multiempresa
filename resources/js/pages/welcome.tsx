import { Head, Link, usePage } from '@inertiajs/react';
import {
    ArrowRight,
    BarChart3,
    Briefcase,
    ClipboardCheck,
    ShieldCheck,
    UserCheck,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { dashboard, login } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

const steps = [
    {
        icon: ClipboardCheck,
        title: 'Requerimiento',
        text: 'El área solicitante registra la necesidad; RR. HH. la valida y Dirección la aprueba.',
    },
    {
        icon: Briefcase,
        title: 'Vacante',
        text: 'RR. HH. define el perfil, los criterios y las ponderaciones, y publica la convocatoria.',
    },
    {
        icon: BarChart3,
        title: 'Evaluación',
        text: 'Evaluaciones y entrevistas con puntajes trazables y un ranking configurable y explicable.',
    },
    {
        icon: UserCheck,
        title: 'Decisión humana',
        text: 'Una persona autorizada registra la decisión final; el sistema no selecciona automáticamente.',
    },
];

export default function Welcome() {
    const { auth } = usePage().props;

    return (
        <>
            <Head title="Inicio" />
            <section className="bg-background border-b">
                <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 md:px-6 lg:grid-cols-[1.2fr_1fr] lg:items-center lg:py-24">
                    <div className="space-y-6">
                        <p className="text-muted-foreground text-sm font-medium tracking-wide uppercase">
                            Caso de estudio · Colegio Andino de Huancayo (demo)
                        </p>
                        <h1 className="text-4xl font-semibold tracking-tight text-balance md:text-5xl">
                            Reclutamiento, evaluación y selección de personal en
                            una sola plataforma
                        </h1>
                        <p className="text-muted-foreground max-w-xl text-lg">
                            Plataforma SaaS multiempresa que da trazabilidad a
                            cada paso del proceso, desde el requerimiento hasta
                            el cierre de la convocatoria.
                        </p>
                        <div className="flex flex-wrap gap-3">
                            <Button size="lg" asChild>
                                <Link href={jobsIndex()} data-cy="cta-jobs">
                                    Ver empleos disponibles
                                    <ArrowRight />
                                </Link>
                            </Button>
                            <Button size="lg" variant="outline" asChild>
                                <Link
                                    href={auth?.user ? dashboard() : login()}
                                    data-cy="cta-login"
                                >
                                    {auth?.user ? 'Ir a mi panel' : 'Iniciar sesión'}
                                </Link>
                            </Button>
                        </div>
                    </div>
                    <Card className="bg-muted/40 border-dashed">
                        <CardHeader className="gap-3">
                            <ShieldCheck className="size-8 text-emerald-600" />
                            <CardTitle className="text-lg">
                                Apoyo a la decisión, no reemplazo
                            </CardTitle>
                            <CardDescription className="text-sm leading-relaxed">
                                El sistema calcula puntajes ponderados y ordena a
                                los candidatos mostrando cómo se obtuvo cada
                                resultado. La selección final siempre la
                                registra una persona autorizada, con su
                                justificación y auditoría.
                            </CardDescription>
                        </CardHeader>
                    </Card>
                </div>
            </section>
            <section className="mx-auto max-w-6xl px-4 py-14 md:px-6">
                <h2 className="mb-6 text-xl font-semibold tracking-tight">
                    Cómo funciona el proceso
                </h2>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    {steps.map((step, index) => (
                        <Card key={step.title} className="gap-3">
                            <CardHeader className="gap-3">
                                <div className="flex items-center gap-3">
                                    <span className="bg-primary text-primary-foreground flex size-8 items-center justify-center rounded-full text-sm font-semibold">
                                        {index + 1}
                                    </span>
                                    <step.icon className="text-muted-foreground size-5" />
                                </div>
                                <CardTitle className="text-base">
                                    {step.title}
                                </CardTitle>
                                <CardDescription>{step.text}</CardDescription>
                            </CardHeader>
                        </Card>
                    ))}
                </div>
            </section>
        </>
    );
}
