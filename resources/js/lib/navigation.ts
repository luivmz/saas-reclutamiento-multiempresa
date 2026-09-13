import {
    Briefcase,
    ClipboardList,
    FilePlus2,
    Globe,
    LayoutGrid,
} from 'lucide-react';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { dashboard } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';
import type { NavGroup, NavItem, RoleValue } from '@/types';

const panel: NavItem = {
    title: 'Panel',
    href: dashboard(),
    icon: LayoutGrid,
    cy: 'dashboard',
    description: 'Resumen de su actividad.',
};

const portal: NavGroup = {
    label: 'Portal',
    items: [
        {
            title: 'Empleos publicados',
            href: jobsIndex(),
            icon: Globe,
            cy: 'jobs',
            description: 'Vacantes publicadas visibles para los postulantes.',
        },
    ],
};

const general: NavGroup = { label: 'General', items: [panel] };

export function navigationFor(role: RoleValue | null | undefined): NavGroup[] {
    switch (role) {
        case 'solicitante':
            return [
                general,
                {
                    label: 'Requerimientos',
                    items: [
                        {
                            title: 'Mis requerimientos',
                            href: JobRequestController.index(),
                            icon: ClipboardList,
                            cy: 'job-requests',
                            description:
                                'Consulte el estado y el historial de sus requerimientos.',
                        },
                        {
                            title: 'Nuevo requerimiento',
                            href: JobRequestController.create(),
                            icon: FilePlus2,
                            cy: 'new-job-request',
                            description:
                                'Registre una necesidad de personal (RF-01).',
                        },
                    ],
                },
                portal,
            ];
        case 'rrhh':
            return [
                general,
                {
                    label: 'Reclutamiento',
                    items: [
                        {
                            title: 'Requerimientos',
                            href: JobRequestController.index(),
                            icon: ClipboardList,
                            cy: 'job-requests',
                            description:
                                'Valide u observe los requerimientos enviados (RF-02).',
                        },
                        {
                            title: 'Vacantes',
                            href: VacancyController.index(),
                            icon: Briefcase,
                            cy: 'vacancies',
                            description:
                                'Configure, valide y publique vacantes (RF-05 a RF-07).',
                        },
                    ],
                },
                portal,
            ];
        case 'aprobador':
            return [
                general,
                {
                    label: 'Dirección',
                    items: [
                        {
                            title: 'Requerimientos',
                            href: JobRequestController.index(),
                            icon: ClipboardList,
                            cy: 'job-requests',
                            description:
                                'Apruebe o rechace requerimientos validados (RF-03).',
                        },
                        {
                            title: 'Vacantes',
                            href: VacancyController.index(),
                            icon: Briefcase,
                            cy: 'vacancies',
                            description:
                                'Consulte las vacantes y los procesos en curso.',
                        },
                    ],
                },
                portal,
            ];
        case 'evaluador':
        case 'postulante':
            return [general, portal];
        default:
            return [portal];
    }
}
