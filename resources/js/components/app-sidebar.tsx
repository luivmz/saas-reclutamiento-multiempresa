import { Link, usePage } from '@inertiajs/react';
import AppLogo from '@/components/app-logo';
import { NavMain } from '@/components/nav-main';
import { NavUser } from '@/components/nav-user';
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from '@/components/ui/sidebar';
import { navigationFor } from '@/lib/navigation';
import { dashboard } from '@/routes';

export function AppSidebar() {
    const { auth, notifications } = usePage().props;
    const groups = navigationFor(auth.user?.role, notifications?.unread ?? 0);

    return (
        <Sidebar collapsible="icon" variant="inset">
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton size="lg" asChild>
                            <Link href={dashboard()} prefetch>
                                <AppLogo />
                            </Link>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>

                {/* El rol decide qué puede hacer cada persona en el proceso;
                    tenerlo a la vista evita la pregunta «¿por qué a mí no me
                    aparece este botón?». */}
                {auth.role && (
                    <p
                        className="text-sidebar-foreground/70 border-sidebar-border mx-1 mt-1 rounded-md border border-dashed px-2 py-1 text-xs group-data-[collapsible=icon]:hidden"
                        data-cy="sidebar-role"
                    >
                        Rol:{' '}
                        <span className="text-sidebar-foreground font-medium">
                            {auth.role.label}
                        </span>
                    </p>
                )}
            </SidebarHeader>

            <SidebarContent className="gap-4">
                {groups.map((group) => (
                    <NavMain
                        key={group.label}
                        label={group.label}
                        items={group.items}
                    />
                ))}
            </SidebarContent>

            <SidebarFooter>
                <NavUser />
            </SidebarFooter>
        </Sidebar>
    );
}
