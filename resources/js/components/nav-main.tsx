import { Link } from '@inertiajs/react';
import {
    SidebarGroup,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from '@/components/ui/sidebar';
import { useCurrentUrl } from '@/hooks/use-current-url';
import type { NavItem } from '@/types';

export function NavMain({
    items,
    label = 'Plataforma',
}: {
    items: NavItem[];
    label?: string;
}) {
    const { isCurrentUrl } = useCurrentUrl();

    return (
        <SidebarGroup className="px-2 py-0">
            <SidebarGroupLabel className="text-sidebar-foreground/55 text-xs font-medium">
                {label}
            </SidebarGroupLabel>
            <SidebarMenu>
                {items.map((item) => {
                    const isCurrent = isCurrentUrl(item.href);

                    return (
                        <SidebarMenuItem key={item.title}>
                            <SidebarMenuButton
                                asChild
                                isActive={isCurrent}
                                tooltip={{ children: item.title }}
                            >
                                <Link
                                    href={item.href}
                                    prefetch
                                    // La página actual se anuncia, no solo se
                                    // pinta: con `aria-current` el lector de
                                    // pantalla dice dónde está uno.
                                    aria-current={
                                        isCurrent ? 'page' : undefined
                                    }
                                    data-cy={
                                        item.cy ? `nav-${item.cy}` : undefined
                                    }
                                >
                                    {item.icon && <item.icon />}
                                    <span>{item.title}</span>
                                    {item.badge ? (
                                        <span
                                            className="bg-sidebar-primary text-sidebar-primary-foreground ml-auto rounded-full px-1.5 text-[10px] leading-4 font-semibold"
                                            data-cy={`nav-badge-${item.cy}`}
                                        >
                                            {item.badge}
                                            <span className="sr-only">
                                                {' '}
                                                sin leer
                                            </span>
                                        </span>
                                    ) : null}
                                </Link>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    );
                })}
            </SidebarMenu>
        </SidebarGroup>
    );
}
