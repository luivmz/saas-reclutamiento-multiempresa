import { Form, Head, Link } from '@inertiajs/react';
import { Building2, CalendarClock, MapPin, Search, Users } from 'lucide-react';
import { EmptyState } from '@/components/empty-state';
import { Pagination } from '@/components/pagination';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { formatDate } from '@/lib/format';
import { index as jobsIndex, show as jobsShow } from '@/routes/jobs';
import type { Paginated, Vacancy } from '@/types';

type Props = {
    vacancies: Paginated<Vacancy>;
    filters: { q: string };
};

export default function JobsIndex({ vacancies, filters }: Props) {
    return (
        <>
            <Head title="Empleos disponibles" />
            <section className="bg-background border-b">
                <div className="mx-auto max-w-6xl space-y-4 px-4 py-10 md:px-6">
                    <h1 className="text-3xl font-semibold tracking-tight" data-cy="page-title">
                        Empleos disponibles
                    </h1>
                    <p className="text-muted-foreground">
                        Convocatorias vigentes publicadas por las organizaciones de la plataforma.
                    </p>
                    <Form {...jobsIndex.form()} className="flex max-w-xl gap-2">
                        <Input
                            name="q"
                            defaultValue={filters.q}
                            placeholder="Buscar por puesto…"
                            aria-label="Buscar por puesto"
                            data-cy="jobs-search"
                        />
                        <Button type="submit" variant="secondary">
                            <Search />
                            Buscar
                        </Button>
                    </Form>
                </div>
            </section>
            <div className="mx-auto max-w-6xl space-y-6 px-4 py-8 md:px-6">
                {vacancies.data.length === 0 ? (
                    <EmptyState
                        title="No hay convocatorias vigentes"
                        description="Vuelva a consultar más adelante."
                    />
                ) : (
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3" data-cy="jobs-list">
                        {vacancies.data.map((vacancy) => (
                            <Card key={vacancy.id} className="gap-4" data-cy="job-card" data-code={vacancy.code}>
                                <CardHeader className="gap-2">
                                    <CardDescription className="flex items-center gap-1.5">
                                        <Building2 className="size-3.5" />
                                        {vacancy.organization?.name}
                                    </CardDescription>
                                    <CardTitle className="text-lg leading-snug">{vacancy.title}</CardTitle>
                                </CardHeader>
                                <CardContent className="text-muted-foreground space-y-2 text-sm">
                                    <p className="line-clamp-3">{vacancy.summary}</p>
                                    <p className="flex items-center gap-1.5">
                                        <MapPin className="size-3.5" />
                                        {vacancy.location} · {vacancy.contract_type.label}
                                    </p>
                                    <p className="flex items-center gap-1.5">
                                        <Users className="size-3.5" />
                                        {vacancy.positions} plaza(s)
                                    </p>
                                    <p className="flex items-center gap-1.5">
                                        <CalendarClock className="size-3.5" />
                                        Postula hasta el {formatDate(vacancy.closes_at)}
                                    </p>
                                </CardContent>
                                <CardFooter className="mt-auto">
                                    <Button asChild className="w-full" variant="outline">
                                        <Link href={jobsShow(vacancy.id)} data-cy="job-detail-link">
                                            Ver convocatoria
                                        </Link>
                                    </Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )}
                <Pagination meta={vacancies.meta} />
            </div>
        </>
    );
}
