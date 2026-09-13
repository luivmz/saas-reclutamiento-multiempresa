import { Link, usePage } from '@inertiajs/react';
import type { ReactNode } from 'react';
import AppLogoIcon from '@/components/app-logo-icon';
import { Button } from '@/components/ui/button';
import { dashboard, home, login, register } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

export default function PublicLayout({ children }: { children: ReactNode }) {
    const { auth, name } = usePage().props;

    return (
        <div className="bg-muted/30 flex min-h-screen flex-col">
            <header className="bg-background/95 sticky top-0 z-20 border-b backdrop-blur">
                <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 md:px-6">
                    <Link href={home()} className="flex items-center gap-2">
                        <span className="bg-primary text-primary-foreground flex size-8 items-center justify-center rounded-md">
                            <AppLogoIcon className="size-5 fill-current" />
                        </span>
                        <span className="hidden font-semibold sm:inline">
                            {name}
                        </span>
                    </Link>
                    <nav className="flex items-center gap-1 text-sm sm:gap-2">
                        <Button variant="ghost" size="sm" asChild>
                            <Link href={jobsIndex()} data-cy="nav-public-jobs">
                                Empleos
                            </Link>
                        </Button>
                        {auth?.user ? (
                            <Button size="sm" asChild>
                                <Link href={dashboard()} data-cy="nav-dashboard">
                                    Ir a mi panel
                                </Link>
                            </Button>
                        ) : (
                            <>
                                <Button variant="ghost" size="sm" asChild>
                                    <Link href={login()} data-cy="nav-login">
                                        Iniciar sesión
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
                    </nav>
                </div>
            </header>
            <main className="flex-1">{children}</main>
            <footer className="bg-background border-t">
                <div className="text-muted-foreground mx-auto flex max-w-6xl flex-col gap-1 px-4 py-6 text-xs md:px-6">
                    <span>
                        Proyecto académico · Universidad Continental · Pruebas y
                        Calidad de Software (NRC 28607)
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
