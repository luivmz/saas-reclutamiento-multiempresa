import { Head } from '@inertiajs/react';
import { ClipboardList } from 'lucide-react';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { EmptyState } from '@/components/empty-state';
import { PageContainer, PageHeader } from '@/components/page';
import {
    VacancyForm,
    initialVacancyData,
} from '@/components/vacancies/vacancy-form';
import type { JobRequestOption } from '@/components/vacancies/vacancy-form';
import type { Presented } from '@/types';

type Props = {
    jobRequests: JobRequestOption[];
    selectedJobRequestId: number | null;
    contractTypes: Presented[];
    stages: Presented[];
    requiredWeightTotal: number | null;
};

export default function CreateVacancy({
    jobRequests,
    selectedJobRequestId,
    contractTypes,
    stages,
    requiredWeightTotal,
}: Props) {
    const selected = jobRequests.find((option) => option.id === selectedJobRequestId);

    return (
        <>
            <Head title="Nueva vacante" />
            <PageContainer className="max-w-4xl">
                <PageHeader
                    title="Nueva vacante"
                    description="RF-05 y RF-06 · Registre el perfil, los criterios de evaluación y la configuración de la convocatoria."
                />
                {jobRequests.length === 0 ? (
                    <EmptyState
                        icon={ClipboardList}
                        title="No hay requerimientos aprobados disponibles"
                        description="Las vacantes se generan a partir de un requerimiento de personal aprobado por Dirección y que aún no tiene vacante."
                    />
                ) : (
                    <VacancyForm
                        mode="create"
                        initial={initialVacancyData(undefined, selected)}
                        jobRequests={jobRequests}
                        contractTypes={contractTypes}
                        stages={stages}
                        requiredWeightTotal={requiredWeightTotal}
                    />
                )}
            </PageContainer>
        </>
    );
}

CreateVacancy.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Nueva', href: VacancyController.create() },
    ],
};
