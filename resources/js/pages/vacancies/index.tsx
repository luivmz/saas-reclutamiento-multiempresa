import { Head, Link, router } from '@inertiajs/react';
import { Briefcase, Plus } from 'lucide-react';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { EmptyState } from '@/components/empty-state';
import { FilterChips } from '@/components/filter-chips';
import { PageContainer, PageHeader } from '@/components/page';
import { Pagination } from '@/components/pagination';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { formatDate } from '@/lib/format';
import type { Paginated, Presented, Vacancy } from '@/types';

type Props = {
    vacancies: Paginated<Vacancy>;
    filters: { estado: string | null };
    statuses: Presented[];
    can: { create: boolean };
};

export default function VacanciesIndex({ vacancies, filters, statuses, can }: Props) {
    const filter = (estado: string | null) =>
        router.get(
            VacancyController.index.url({ query: estado ? { estado } : {} }),
            {},
            { preserveState: true, replace: true },
        );

    return (
        <>
            <Head title="Vacantes" />
            <PageContainer>
                <PageHeader
                    title="Vacantes"
                    description="Perfil, criterios, validación, publicación y cierre de convocatorias."
                    actions={
                        can.create && (
                            <Button asChild data-cy="new-vacancy">
                                <Link href={VacancyController.create()}>
                                    <Plus />
                                    Nueva vacante
                                </Link>
                            </Button>
                        )
                    }
                />

                <FilterChips options={statuses} value={filters.estado} onChange={filter} allLabel="Todas" />

                {vacancies.data.length === 0 ? (
                    <EmptyState
                        icon={Briefcase}
                        title="No hay vacantes para mostrar"
                        description="Genere una vacante a partir de un requerimiento aprobado."
                    />
                ) : (
                    <Card className="gap-0 overflow-hidden py-0">
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm" data-cy="vacancies-table">
                                <thead className="bg-muted/50 text-muted-foreground text-left text-xs tracking-wide uppercase">
                                    <tr>
                                        <th className="px-4 py-3 font-medium">Código</th>
                                        <th className="px-4 py-3 font-medium">Vacante</th>
                                        <th className="px-4 py-3 font-medium">Requerimiento</th>
                                        <th className="px-4 py-3 text-center font-medium">Plazas</th>
                                        <th className="px-4 py-3 font-medium">Cierre</th>
                                        <th className="px-4 py-3 font-medium">Estado</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y">
                                    {vacancies.data.map((vacancy) => (
                                        <tr key={vacancy.id} className="hover:bg-muted/40" data-cy="vacancy-row" data-code={vacancy.code}>
                                            <td className="px-4 py-3 font-mono text-xs">
                                                <Link href={VacancyController.show(vacancy.id)} className="font-medium hover:underline" data-cy="vacancy-link">
                                                    {vacancy.code}
                                                </Link>
                                            </td>
                                            <td className="px-4 py-3 font-medium">{vacancy.title}</td>
                                            <td className="text-muted-foreground px-4 py-3 font-mono text-xs">{vacancy.job_request?.code}</td>
                                            <td className="px-4 py-3 text-center">{vacancy.positions}</td>
                                            <td className="text-muted-foreground px-4 py-3 whitespace-nowrap">{formatDate(vacancy.closes_at)}</td>
                                            <td className="px-4 py-3">
                                                <StatusBadge status={vacancy.status} />
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                )}

                <Pagination meta={vacancies.meta} />
            </PageContainer>
        </>
    );
}

VacanciesIndex.layout = {
    breadcrumbs: [{ title: 'Vacantes', href: VacancyController.index() }],
};
