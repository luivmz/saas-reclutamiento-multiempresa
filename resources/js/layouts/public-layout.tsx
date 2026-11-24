import { Link, usePage } from '@inertiajs/react';
import { BriefcaseBusiness } from 'lucide-react';
import type { ReactNode } from 'react';
import AppLogoIcon from '@/components/app-logo-icon';
import { AppearanceToggle } from '@/components/appearance-toggle';
import { MAIN_CONTENT_ID, SkipLink } from '@/components/skip-link';
import { Button } from '@/components/ui/button';
import { dashboard, home, login, register } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

/**
 * Marco del sitio público: portada y bolsa de empleo.
 *
 * Es la única parte de la plataforma que ve alguien que todavía no tiene
 * cuenta, así que el pie repite sin adornos de quién es el proyecto y que los
 * datos son ficticios.
 */
export default function PublicLayout({ children }: { children: ReactNode }) {
    const { auth, name } = usePage().props;
    // Marca «Convocatorias» como página actual en el listado y en cada detalle.
    const onJobs = /^\/empleos(\/|\?|$)/.test(usePage().url);

    return (
        <div className="bg-background flex min-h-svh flex-col">
            <SkipLink />
            <header className="bg-background/90 z-20 border-b backdrop-blur sm:sticky sm:top-0">
                {/* En móvil: identidad y tema arriba; debajo, la navegación en
                    una rejilla de dos columnas con las etiquetas completas.
                    Desde sm, todo en una fila. */}
                <div className="mx-auto flex min-h-16 max-w-6xl flex-wrap items-center justify-between gap-x-4 gap-y-2 px-4 py-2 sm:px-6">
                    <Link
                        href={home()}
                        className="flex min-h-11 min-w-0 flex-1 items-center gap-2.5 sm:flex-none"
                        data-cy="nav-home"
                    >
                        <span className="bg-primary text-primary-foreground flex size-8 shrink-0 items-center justify-center rounded-md">
                            <AppLogoIcon
                                className="size-5 fill-current"
                                aria-hidden="true"
                            />
                        </span>
                        <span className="font-serif font-semibold [overflow-wrap:anywhere]">
                            {name}
                        </span>
                    </Link>
                    <nav
                        className="grid w-full grid-cols-2 gap-2 max-sm:order-last sm:ml-auto sm:flex sm:w-auto sm:items-center"
                        aria-label="Navegación principal"
                        data-cy="public-nav"
                    >
                        <Button
                            variant="ghost"
                            size="sm"
                            className={`max-sm:min-h-11 ${auth?.user ? '' : 'max-sm:col-span-2 max-sm:justify-start'} aria-[current=page]:bg-accent`}
                            asChild
                        >
                            <Link
                                href={jobsIndex()}
                                aria-current={onJobs ? 'page' : undefined}
                                data-cy="nav-public-jobs"
                            >
                                <BriefcaseBusiness aria-hidden="true" />
                                Convocatorias
                            </Link>
                        </Button>
                        {auth?.user ? (
                            <Button
                                size="sm"
                                className="max-sm:min-h-11"
                                asChild
                            >
                                <Link
                                    href={dashboard()}
                                    data-cy="nav-dashboard"
                                >
                                    Ir a mi panel
                                </Link>
                            </Button>
                        ) : (
                            <>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    className="max-sm:min-h-11"
                                    asChild
                                >
                                    <Link href={login()} data-cy="nav-login">
                                        Iniciar sesión
                                    </Link>
                                </Button>
                                <Button
                                    size="sm"
                                    className="max-sm:min-h-11"
                                    asChild
                                >
                                    <Link
                                        href={register()}
                                        data-cy="nav-register"
                                    >
                                        Crear cuenta
                                    </Link>
                                </Button>
                            </>
                        )}
                    </nav>
                    <AppearanceToggle className="shrink-0 max-sm:size-11" />
                </div>
            </header>

            <main
                id={MAIN_CONTENT_ID}
                tabIndex={-1}
                className="flex-1 sm:[&_:focus-visible]:scroll-mt-20"
            >
                {children}
            </main>

            <footer className="bg-surface border-t">
                <div className="text-muted-foreground mx-auto flex max-w-6xl flex-col gap-1.5 px-4 py-8 text-xs leading-relaxed sm:px-6">
                    <span>
                        Proyecto académico de la Universidad Continental, curso
                        Pruebas y Calidad de Software (NRC 28607).
                    </span>
                    <span>
                        Todos los datos mostrados son ficticios y se usan solo
                        con fines de demostración.
                    </span>
                </div>
            </footer>
        </div>
    );
}
