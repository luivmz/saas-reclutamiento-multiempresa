import { usePage } from '@inertiajs/react';
import type { ReactNode } from 'react';
import AppLayout from '@/layouts/app-layout';
import PublicLayout from '@/layouts/public-layout';

/**
 * Marco de las páginas de error de una visita interna (DEF-28).
 *
 * Con sesión, el error aparece dentro del panel, con su navegación; sin
 * sesión, dentro del sitio público. Si la ruta no existe, el servidor no
 * comparte la sesión: se usa el marco público, que no la necesita.
 */
export default function ErrorLayout({ children }: { children: ReactNode }) {
    const { auth } = usePage().props;

    return auth?.user ? (
        <AppLayout>{children}</AppLayout>
    ) : (
        <PublicLayout>{children}</PublicLayout>
    );
}
