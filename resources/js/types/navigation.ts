import type { InertiaLinkProps } from '@inertiajs/react';
import type { LucideIcon } from 'lucide-react';

export type BreadcrumbItem = {
    title: string;
    href: NonNullable<InertiaLinkProps['href']>;
};

export type NavItem = {
    title: string;
    href: NonNullable<InertiaLinkProps['href']>;
    icon?: LucideIcon | null;
    isActive?: boolean;
    cy?: string;
    description?: string;
    badge?: number;
    /** Requisitos que cubre la entrada, para la trazabilidad; no se muestran en pantallas de postulante. */
    rf?: string[];
};

export type NavGroup = {
    label: string;
    items: NavItem[];
};
