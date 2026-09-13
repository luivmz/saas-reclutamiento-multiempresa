import {
    Bell,
    Briefcase,
    ClipboardCheck,
    ClipboardList,
    FilePlus2,
    FileUser,
    Globe,
    LayoutGrid,
    Send,
} from 'lucide-react';
import AssessmentAssignmentController from '@/actions/App/Http/Controllers/Assessments/AssessmentAssignmentController';
import CandidateApplicationController from '@/actions/App/Http/Controllers/Candidates/CandidateApplicationController';
import CandidateProfileController from '@/actions/App/Http/Controllers/Candidates/CandidateProfileController';
import JobRequestController from '@/actions/App/Http/Controllers/JobRequests/JobRequestController';
import NotificationController from '@/actions/App/Http/Controllers/NotificationController';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { dashboard } from '@/routes';
import { index as jobsIndex } from '@/routes/jobs';
import type { NavGroup, RoleValue } from '@/types';

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

function general(unread: number): NavGroup {
    return {
        label: 'General',
        items: [
            {
                title: 'Panel',
                href: dashboard(),
                icon: LayoutGrid,
                cy: 'dashboard',
                description: 'Resumen de su actividad.',
            },
            {
                title: 'Notificaciones',
                href: NotificationController.index(),
                icon: Bell,
                cy: 'notifications',
                badge: unread,
                description: 'Avisos del proceso de reclutamiento.',
            },
        ],
    };
}

export function navigationFor(
    role: RoleValue | null | undefined,
    unread = 0,
): NavGroup[] {
    switch (role) {
        case 'solicitante':
            return [
                general(unread),
                {
                    label: 'Requerimientos',
                    items: [
                        {
                            title: 'Mis requerimientos',
                            href: JobRequestController.index(),
                            icon: ClipboardList,
                            cy: 'job-requests',
                            description: 'Consulte el estado y el historial de sus requerimientos.',
                        },
                        {
                            title: 'Nuevo requerimiento',
                            href: JobRequestController.create(),
                            icon: FilePlus2,
                            cy: 'new-job-request',
                            description: 'Registre una necesidad de personal (RF-01).',
                        },
                    ],
                },
                portal,
            ];
        case 'rrhh':
            return [
                general(unread),
                {
                    label: 'Reclutamiento',
                    items: [
                        {
                            title: 'Requerimientos',
                            href: JobRequestController.index(),
                            icon: ClipboardList,
                            cy: 'job-requests',
                            description: 'Valide u observe los requerimientos enviados (RF-02).',
                        },
                        {
                            title: 'Vacantes y postulaciones',
                            href: VacancyController.index(),
                            icon: Briefcase,
                            cy: 'vacancies',
                            description: 'Configure y publique vacantes y revise sus postulaciones (RF-05 a RF-15).',
                        },
                    ],
                },
                portal,
            ];
        case 'aprobador':
            return [
                general(unread),
                {
                    label: 'Dirección',
                    items: [
                        {
                            title: 'Requerimientos',
                            href: JobRequestController.index(),
                            icon: ClipboardList,
                            cy: 'job-requests',
                            description: 'Apruebe o rechace requerimientos validados (RF-03).',
                        },
                        {
                            title: 'Vacantes',
                            href: VacancyController.index(),
                            icon: Briefcase,
                            cy: 'vacancies',
                            description: 'Consulte las vacantes y los procesos en curso.',
                        },
                    ],
                },
                portal,
            ];
        case 'evaluador':
            return [
                general(unread),
                {
                    label: 'Evaluación',
                    items: [
                        {
                            title: 'Mis evaluaciones',
                            href: AssessmentAssignmentController(),
                            icon: ClipboardCheck,
                            cy: 'assessments',
                            description: 'Registre puntajes y observaciones de las sesiones asignadas (RF-19).',
                        },
                    ],
                },
                portal,
            ];
        case 'postulante':
            return [
                general(unread),
                {
                    label: 'Mi postulación',
                    items: [
                        {
                            title: 'Mi perfil y CV',
                            href: CandidateProfileController.edit(),
                            icon: FileUser,
                            cy: 'candidate-profile',
                            description: 'Complete su perfil y cargue su CV (RF-09).',
                        },
                        {
                            title: 'Mis postulaciones',
                            href: CandidateApplicationController.index(),
                            icon: Send,
                            cy: 'my-applications',
                            description: 'Siga la etapa de cada postulación (RF-11, RF-15).',
                        },
                    ],
                },
                portal,
            ];
        default:
            return [portal];
    }
}
