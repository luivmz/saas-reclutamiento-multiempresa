import { Link, usePage } from '@inertiajs/react';
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

    return (
        <div className="bg-background flex min-h-svh flex-col">
            <SkipLink />
            <header className="bg-background/90 sticky top-0 z-20 border-b backdrop-blur">
                <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
                    <Link
                        href={home()}
                        className="flex items-center gap-2.5"
                        data-cy="nav-home"
                    >
                        <span className="bg-primary text-primary-foreground flex size-8 items-center justify-center rounded-md">
                            <AppLogoIcon className="size-5 fill-current" />
                        </span>
                        <span className="hidden font-serif font-semibold sm:inline">
                            {name}
                        </span>
                    </Link>
                    <nav
                        className="flex items-center gap-0.5 sm:gap-2"
                        aria-label="Navegación principal"
                    >
                        <Button variant="ghost" size="sm" asChild>
                            <Link href={jobsIndex()} data-cy="nav-public-jobs">
                                Empleos
                            </Link>
                        </Button>
                        {auth?.user ? (
                            <Button size="sm" asChild>
                                <Link
                                    href={dashboard()}
                                    data-cy="nav-dashboard"
                                >
                                    Ir a mi panel
                                </Link>
                            </Button>
                        ) : (
                            <>
                                <Button variant="ghost" size="sm" asChild>
                                    <Link href={login()} data-cy="nav-login">
                                        {/* En pantallas angostas la barra no
                                            admite las tres acciones completas;
                                            se acorta la etiqueta antes que
                                            esconder el acceso. */}
                                        <span className="sm:hidden">
                                            Entrar
                                        </span>
                                        <span className="hidden sm:inline">
                                            Iniciar sesión
                                        </span>
                                    </Link>
                                </Button>
                                <Button size="sm" asChild>
                                    <Link
                                        href={register()}
                                        data-cy="nav-register"
                                    >
                                        Crear cuenta
                                    </Link>
                                </Button>
                            </>
                        )}
                        <AppearanceToggle />
                    </nav>
                </div>
            </header>

            <main id={MAIN_CONTENT_ID} tabIndex={-1} className="flex-1">
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
