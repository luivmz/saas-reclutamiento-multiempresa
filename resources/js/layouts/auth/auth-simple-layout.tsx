import { Link } from '@inertiajs/react';
import { FileCheck2, Landmark, UserCheck } from 'lucide-react';
import AppLogoIcon from '@/components/app-logo-icon';
import { home } from '@/routes';
import type { AuthLayoutProps } from '@/types';

/**
 * Acceso a la plataforma.
 *
 * A la izquierda, lo único que hay que hacer: entrar. A la derecha, de quién
 * es el sistema y bajo qué regla trabaja —la decisión final es de una
 * persona—, más el aviso de que todo lo que se verá dentro es ficticio. En
 * pantallas angostas el panel institucional desaparece: no compite con el
 * formulario.
 */
const claims = [
    {
        icon: FileCheck2,
        title: 'Un expediente por requerimiento',
        text: 'Cada solicitud de personal deja registro de quién la validó, quién la aprobó y cuándo.',
    },
    {
        icon: UserCheck,
        title: 'La decisión la firma una persona',
        text: 'El sistema calcula y ordena puntajes; seleccionar es un acto humano con justificación (RF-23).',
    },
    {
        icon: Landmark,
        title: 'Cada organización ve lo suyo',
        text: 'Los procesos de una institución no son visibles para ninguna otra.',
    },
];

export default function AuthSimpleLayout({
    children,
    title,
    description,
}: AuthLayoutProps) {
    return (
        <div className="bg-background min-h-svh lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(0,1.05fr)]">
            {/* El formulario es el contenido principal: sin `main`, un lector
                de pantalla no tenía a dónde saltar en estas cinco pantallas. */}
            <main className="flex min-h-svh flex-col justify-center px-6 py-10 sm:px-10 lg:min-h-0 lg:px-14">
                <div className="mx-auto w-full max-w-sm space-y-8">
                    <div className="space-y-6">
                        <Link
                            href={home()}
                            className="inline-flex items-center gap-2.5"
                        >
                            <span className="bg-primary text-primary-foreground flex size-9 items-center justify-center rounded-md">
                                <AppLogoIcon className="size-5 fill-current" />
                            </span>
                            <span className="font-serif text-base font-semibold">
                                Volver al inicio
                            </span>
                        </Link>

                        <div className="space-y-2">
                            <h1 className="font-serif text-2xl font-semibold tracking-tight">
                                {title}
                            </h1>
                            {description && (
                                <p className="text-muted-foreground text-sm leading-relaxed">
                                    {description}
                                </p>
                            )}
                        </div>
                    </div>

                    {children}
                </div>
            </main>

            <aside className="bg-sidebar text-sidebar-foreground hidden flex-col justify-between px-14 py-14 lg:flex">
                <div className="space-y-10">
                    <p className="text-sidebar-foreground/70 text-sm">
                        Colegio Andino de Huancayo — entorno de demostración
                    </p>
                    <h2 className="font-serif text-3xl leading-tight font-semibold">
                        Reclutamiento, evaluación y selección con rastro
                        completo
                    </h2>
                    <ul className="space-y-6">
                        {claims.map((claim) => (
                            <li key={claim.title} className="flex gap-4">
                                <claim.icon
                                    className="text-sidebar-primary mt-0.5 size-5 shrink-0"
                                    aria-hidden="true"
                                />
                                <div className="space-y-1">
                                    <p className="text-sm font-medium">
                                        {claim.title}
                                    </p>
                                    <p className="text-sidebar-foreground/70 text-sm leading-relaxed">
                                        {claim.text}
                                    </p>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
                <p className="text-sidebar-foreground/60 border-sidebar-border border-t pt-6 text-xs leading-relaxed">
                    Proyecto académico de la Universidad Continental. Todos los
                    datos de este entorno son ficticios.
                </p>
            </aside>
        </div>
    );
}
