import { Head, Link, usePage } from '@inertiajs/react';
import { Button } from '@/components/ui/button';
import { dashboard, login } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';

/**
 * Error 403 o 404 de una navegación interna (DEF-28).
 *
 * Sin esta página, Inertia abría la respuesta HTML del error en su ventana
 * modal. Los textos y las salidas son los de las vistas Blade de
 * `resources/views/errors`, que siguen atendiendo las cargas completas.
 * Nunca muestra el mensaje de la excepción ni datos del recurso pedido.
 */
const TEXTOS = {
    403: {
        titulo: 'Acceso no permitido',
        encabezado: 'No tiene permiso para ver esta página',
        mensaje:
            'Su cuenta no tiene acceso a esta sección. Si cree que debería tenerlo, consulte con la persona que administra su organización.',
    },
    404: {
        titulo: 'Página no encontrada',
        encabezado: 'No encontramos esta página',
        mensaje:
            'La dirección no existe o su contenido no está disponible para esta cuenta. Revise el enlace o continúe desde aquí.',
    },
} as const;

export default function HttpError({ status }: { status: 403 | 404 }) {
    const { auth } = usePage().props;
    const texto = TEXTOS[status] ?? TEXTOS[404];
    const conSesion = Boolean(auth?.user);

    return (
        <>
            <Head title={texto.titulo} />
            <div className="mx-auto flex w-full max-w-xl flex-1 flex-col justify-center px-4 py-12 sm:px-6">
                <section
                    className="bg-card rounded-xl border p-6 sm:p-7"
                    aria-labelledby="titulo-error"
                    data-cy="http-error"
                    data-status={status}
                >
                    <p className="text-muted-foreground text-sm">
                        Error {status}
                    </p>
                    <h1
                        id="titulo-error"
                        className="mt-1 font-serif text-2xl font-semibold tracking-tight sm:text-3xl"
                    >
                        {texto.encabezado}
                    </h1>
                    <p className="text-muted-foreground mt-3 leading-relaxed">
                        {texto.mensaje}
                    </p>
                    <nav
                        aria-label="Cómo continuar"
                        className="mt-6 flex flex-wrap gap-2.5"
                    >
                        {conSesion ? (
                            <>
                                <Button asChild>
                                    <Link href={dashboard()}>
                                        Ir a mi panel
                                    </Link>
                                </Button>
                                <Button asChild variant="outline">
                                    <Link href={jobsIndex()}>
                                        Ver convocatorias
                                    </Link>
                                </Button>
                            </>
                        ) : (
                            <>
                                <Button asChild>
                                    <Link href={jobsIndex()}>
                                        Ver convocatorias
                                    </Link>
                                </Button>
                                <Button asChild variant="outline">
                                    <Link href={login()}>Iniciar sesión</Link>
                                </Button>
                            </>
                        )}
                    </nav>
                </section>
            </div>
        </>
    );
}
