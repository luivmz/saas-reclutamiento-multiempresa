import { Head } from '@inertiajs/react';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { PageContainer, PageHeader } from '@/components/page';
import {
    VacancyForm,
    initialVacancyData,
} from '@/components/vacancies/vacancy-form';
import { WorkflowAlert } from '@/components/workflow-alert';
import type { Presented, Vacancy } from '@/types';

type Props = {
    vacancy: Vacancy;
    contractTypes: Presented[];
    stages: Presented[];
    requiredWeightTotal: number | null;
};

export default function EditVacancy({
    vacancy,
    contractTypes,
    stages,
    requiredWeightTotal,
}: Props) {
    return (
        <>
            <Head title={`Configurar ${vacancy.code}`} />
            <PageContainer className="max-w-4xl">
                <PageHeader
                    eyebrow={<span className="font-mono">{vacancy.code}</span>}
                    title="Configurar vacante"
                    description={`Requerimiento ${vacancy.job_request?.code ?? ''} · ${vacancy.job_request?.area ?? ''}`}
                />
                <WorkflowAlert />
                <VacancyForm
                    mode="edit"
                    vacancyId={vacancy.id}
                    initial={initialVacancyData(vacancy)}
                    contractTypes={contractTypes}
                    stages={stages}
                    requiredWeightTotal={requiredWeightTotal}
                />
            </PageContainer>
        </>
    );
}

EditVacancy.layout = {
    breadcrumbs: [
        { title: 'Vacantes', href: VacancyController.index() },
        { title: 'Configurar', href: VacancyController.index() },
    ],
};
