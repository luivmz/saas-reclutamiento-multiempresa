import { usePage } from '@inertiajs/react';

import AppLogoIcon from '@/components/app-logo-icon';

/**
 * Bloque de marca de la barra lateral.
 *
 * Debajo del nombre del producto va la organización en la que uno está
 * trabajando. En una plataforma multiempresa ese dato no es decorativo: es lo
 * que distingue el expediente propio del de otra institución.
 */
export default function AppLogo() {
    const { name, auth } = usePage().props;

    return (
        <>
            <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-md">
                <AppLogoIcon className="size-5 fill-current" />
            </div>
            <div className="ml-1 grid flex-1 text-left">
                <span className="truncate font-serif text-sm leading-tight font-semibold">
                    {name}
                </span>
                <span
                    className="text-sidebar-foreground/65 truncate text-xs"
                    data-cy="tenant-name"
                >
                    {auth?.organization?.name ?? 'Portal de postulantes'}
                </span>
            </div>
        </>
    );
}
