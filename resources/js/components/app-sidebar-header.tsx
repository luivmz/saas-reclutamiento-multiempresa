import { Link, usePage } from '@inertiajs/react';
import { Bell } from 'lucide-react';
import NotificationController from '@/actions/App/Http/Controllers/NotificationController';
import { AppearanceToggle } from '@/components/appearance-toggle';
import { Breadcrumbs } from '@/components/breadcrumbs';
import { Button } from '@/components/ui/button';
import { SidebarTrigger } from '@/components/ui/sidebar';
import type { BreadcrumbItem as BreadcrumbItemType } from '@/types';

/**
 * Barra superior del área de trabajo.
 *
 * Llevaba solo el botón de la barra lateral y las migas. Ahora sostiene
 * también lo que uno necesita desde cualquier página sin perder el contexto:
 * los avisos pendientes y el tema.
 */
export function AppSidebarHeader({
    breadcrumbs = [],
}: {
    breadcrumbs?: BreadcrumbItemType[];
}) {
    const { notifications } = usePage().props;
    const unread = notifications?.unread ?? 0;

    return (
        <header className="bg-background/85 border-border/70 sticky top-0 z-20 flex h-14 shrink-0 items-center gap-2 rounded-t-xl border-b px-3 backdrop-blur sm:px-4">
            <SidebarTrigger className="-ml-1" />
            <div className="min-w-0 flex-1">
                <Breadcrumbs breadcrumbs={breadcrumbs} />
            </div>
            <div className="flex items-center gap-1">
                <Button
                    variant="ghost"
                    size="icon"
                    className="relative size-8"
                    asChild
                >
                    <Link
                        href={NotificationController.index()}
                        data-cy="header-notifications"
                    >
                        <Bell className="size-4" aria-hidden="true" />
                        {unread > 0 && (
                            <span className="bg-primary ring-background absolute top-1 right-1 size-2 rounded-full ring-2" />
                        )}
                        <span className="sr-only">
                            {unread > 0
                                ? `Notificaciones, ${unread} sin leer`
                                : 'Notificaciones'}
                        </span>
                    </Link>
                </Button>
                <AppearanceToggle />
            </div>
        </header>
    );
}
