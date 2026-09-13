import { Link, useForm } from '@inertiajs/react';
import { Plus, Trash2 } from 'lucide-react';
import type { FormEvent } from 'react';
import VacancyController from '@/actions/App/Http/Controllers/Vacancies/VacancyController';
import { FormField, NativeSelect } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatNumber } from '@/lib/format';
import { cn } from '@/lib/utils';
import type { Presented, Vacancy } from '@/types';

export type JobRequestOption = {
    id: number;
    code: string;
    position_title: string;
    area: string;
    headcount: number;
    contract_type: string;
};

type CriterionInput = {
    name: string;
    stage: string;
    weight: string;
    min_score: string;
    max_score: string;
};

type ProfileInput = {
    education: string;
    experience: string;
    functions: string;
    competencies: string;
};

export type VacancyFormData = {
    job_request_id: string;
    title: string;
    summary: string;
    location: string;
    contract_type: string;
    positions: string;
    opens_at: string;
    closes_at: string;
    profile: ProfileInput;
    criteria: CriterionInput[];
};

const suggestedCriteria: CriterionInput[] = [
    { name: 'Conocimientos pedagógicos', stage: 'evaluacion', weight: '40', min_score: '0', max_score: '20' },
    { name: 'Clase modelo', stage: 'evaluacion', weight: '30', min_score: '0', max_score: '20' },
    { name: 'Entrevista personal', stage: 'entrevista', weight: '30', min_score: '0', max_score: '20' },
];

export function initialVacancyData(
    vacancy?: Vacancy,
    jobRequest?: JobRequestOption,
): VacancyFormData {
    if (vacancy) {
        return {
            job_request_id: String(vacancy.job_request?.id ?? ''),
            title: vacancy.title,
            summary: vacancy.summary,
            location: vacancy.location,
            contract_type: vacancy.contract_type.value,
            positions: String(vacancy.positions),
            opens_at: vacancy.opens_at ?? '',
            closes_at: vacancy.closes_at ?? '',
            profile: {
                education: vacancy.profile?.education ?? '',
                experience: vacancy.profile?.experience ?? '',
                functions: vacancy.profile?.functions ?? '',
                competencies: vacancy.profile?.competencies ?? '',
            },
            criteria: (vacancy.criteria ?? []).map((criterion) => ({
                name: criterion.name,
                stage: criterion.stage.value,
                weight: String(criterion.weight),
                min_score: String(criterion.min_score),
                max_score: String(criterion.max_score),
            })),
        };
    }

    return {
        job_request_id: jobRequest ? String(jobRequest.id) : '',
        title: jobRequest?.position_title ?? '',
        summary: '',
        location: 'Huancayo, Junín',
        contract_type: jobRequest?.contract_type ?? '',
        positions: jobRequest ? String(jobRequest.headcount) : '1',
        opens_at: '',
        closes_at: '',
        profile: { education: '', experience: '', functions: '', competencies: '' },
        criteria: suggestedCriteria,
    };
}

type Props = {
    mode: 'create' | 'edit';
    vacancyId?: number;
    initial: VacancyFormData;
    jobRequests?: JobRequestOption[];
    contractTypes: Presented[];
    stages: Presented[];
    requiredWeightTotal: number | null;
};

export function VacancyForm({
    mode,
    vacancyId,
    initial,
    jobRequests = [],
    contractTypes,
    stages,
    requiredWeightTotal,
}: Props) {
    const form = useForm<VacancyFormData>(initial);
    const errors = form.errors as Record<string, string | undefined>;
    const totalWeight = form.data.criteria.reduce(
        (sum, criterion) => sum + (Number.parseFloat(criterion.weight) || 0),
        0,
    );
    const weightOk =
        requiredWeightTotal === null ||
        Math.abs(totalWeight - requiredWeightTotal) <= 0.01;

    const submit = (event: FormEvent) => {
        event.preventDefault();

        if (mode === 'create') {
            form.post(VacancyController.store.url());
        } else if (vacancyId !== undefined) {
            form.put(VacancyController.update.url(vacancyId));
        }
    };

    const setField = (field: Exclude<keyof VacancyFormData, 'profile' | 'criteria'>, value: string) =>
        form.setData(field, value);

    const setProfile = (field: keyof ProfileInput, value: string) =>
        form.setData('profile', { ...form.data.profile, [field]: value });

    const setCriterion = (index: number, field: keyof CriterionInput, value: string) =>
        form.setData(
            'criteria',
            form.data.criteria.map((criterion, i) =>
                i === index ? { ...criterion, [field]: value } : criterion,
            ),
        );

    const selectJobRequest = (id: string) => {
        const jobRequest = jobRequests.find((option) => String(option.id) === id);
        form.setData({
            ...form.data,
            job_request_id: id,
            title: jobRequest?.position_title ?? form.data.title,
            contract_type: jobRequest?.contract_type ?? form.data.contract_type,
            positions: jobRequest ? String(jobRequest.headcount) : form.data.positions,
        });
    };

    return (
        <form onSubmit={submit} className="space-y-6" data-cy="vacancy-form">
            <Card>
                <CardHeader>
                    <CardTitle>Datos de la convocatoria</CardTitle>
                    <CardDescription>
                        RF-06 · Configuración pública de la vacante.
                    </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-5 md:grid-cols-2">
                    {mode === 'create' && (
                        <FormField
                            label="Requerimiento aprobado"
                            htmlFor="job_request_id"
                            error={errors.job_request_id}
                            className="md:col-span-2"
                        >
                            <NativeSelect
                                id="job_request_id"
                                value={form.data.job_request_id}
                                onChange={(event) => selectJobRequest(event.target.value)}
                                placeholder="Seleccione un requerimiento…"
                                options={jobRequests.map((jobRequest) => ({
                                    value: String(jobRequest.id),
                                    label: `${jobRequest.code} · ${jobRequest.position_title} (${jobRequest.headcount} plaza/s)`,
                                }))}
                                data-cy="vacancy-job-request"
                            />
                        </FormField>
                    )}
                    <FormField label="Título" htmlFor="title" error={errors.title} className="md:col-span-2">
                        <Input id="title" value={form.data.title} onChange={(e) => setField('title', e.target.value)} data-cy="vacancy-title" />
                    </FormField>
                    <FormField label="Descripción pública" htmlFor="summary" error={errors.summary} className="md:col-span-2">
                        <Textarea id="summary" rows={4} value={form.data.summary} onChange={(e) => setField('summary', e.target.value)} data-cy="vacancy-summary" />
                    </FormField>
                    <FormField label="Lugar de trabajo" htmlFor="location" error={errors.location}>
                        <Input id="location" value={form.data.location} onChange={(e) => setField('location', e.target.value)} data-cy="vacancy-location" />
                    </FormField>
                    <FormField label="Tipo de contrato" htmlFor="contract_type" error={errors.contract_type}>
                        <NativeSelect id="contract_type" value={form.data.contract_type} onChange={(e) => setField('contract_type', e.target.value)} options={contractTypes} placeholder="Seleccione…" data-cy="vacancy-contract-type" />
                    </FormField>
                    <FormField label="Plazas" htmlFor="positions" error={errors.positions}>
                        <Input id="positions" type="number" min={1} max={50} value={form.data.positions} onChange={(e) => setField('positions', e.target.value)} data-cy="vacancy-positions" />
                    </FormField>
                    <div className="grid gap-5 sm:grid-cols-2">
                        <FormField label="Inicio de postulaciones" htmlFor="opens_at" error={errors.opens_at}>
                            <Input id="opens_at" type="date" value={form.data.opens_at} onChange={(e) => setField('opens_at', e.target.value)} data-cy="vacancy-opens-at" />
                        </FormField>
                        <FormField label="Cierre de postulaciones" htmlFor="closes_at" error={errors.closes_at}>
                            <Input id="closes_at" type="date" value={form.data.closes_at} onChange={(e) => setField('closes_at', e.target.value)} data-cy="vacancy-closes-at" />
                        </FormField>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Perfil del puesto</CardTitle>
                    <CardDescription>RF-05 · Requisitos y funciones del puesto.</CardDescription>
                </CardHeader>
                <CardContent className="grid gap-5 md:grid-cols-2">
                    <FormField label="Formación académica" htmlFor="profile-education" error={errors['profile.education']}>
                        <Input id="profile-education" value={form.data.profile.education} onChange={(e) => setProfile('education', e.target.value)} data-cy="profile-education" />
                    </FormField>
                    <FormField label="Experiencia" htmlFor="profile-experience" error={errors['profile.experience']}>
                        <Input id="profile-experience" value={form.data.profile.experience} onChange={(e) => setProfile('experience', e.target.value)} data-cy="profile-experience" />
                    </FormField>
                    <FormField label="Funciones" htmlFor="profile-functions" error={errors['profile.functions']}>
                        <Textarea id="profile-functions" rows={4} value={form.data.profile.functions} onChange={(e) => setProfile('functions', e.target.value)} data-cy="profile-functions" />
                    </FormField>
                    <FormField label="Competencias" htmlFor="profile-competencies" error={errors['profile.competencies']}>
                        <Textarea id="profile-competencies" rows={4} value={form.data.profile.competencies} onChange={(e) => setProfile('competencies', e.target.value)} data-cy="profile-competencies" />
                    </FormField>
                </CardContent>
            </Card>

            <Card>
                <CardHeader className="flex flex-row flex-wrap items-start justify-between gap-3">
                    <div className="space-y-1.5">
                        <CardTitle>Criterios de evaluación y ponderaciones</CardTitle>
                        <CardDescription>
                            RF-05 y RF-20 · Cada criterio se califica en su rango y aporta
                            según su ponderación al puntaje del ranking.
                        </CardDescription>
                    </div>
                    <span
                        data-cy="weight-total"
                        className={cn(
                            'rounded-full px-3 py-1 text-xs font-semibold',
                            weightOk
                                ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300'
                                : 'bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300',
                        )}
                    >
                        Suma: {formatNumber(totalWeight)}
                        {requiredWeightTotal !== null && ` / ${formatNumber(requiredWeightTotal)}`}
                    </span>
                </CardHeader>
                <CardContent className="space-y-3">
                    <InputError message={errors.criteria} />
                    <div className="text-muted-foreground hidden grid-cols-[2fr_1fr_0.8fr_0.8fr_0.8fr_auto] gap-2 px-1 text-xs font-medium md:grid">
                        <span>Criterio</span>
                        <span>Etapa</span>
                        <span>Ponderación</span>
                        <span>Mínimo</span>
                        <span>Máximo</span>
                        <span className="w-9" />
                    </div>
                    {form.data.criteria.map((criterion, index) => (
                        <div key={index} className="rounded-lg border p-3 md:border-0 md:p-0" data-cy="criterion-row">
                            <div className="grid gap-2 md:grid-cols-[2fr_1fr_0.8fr_0.8fr_0.8fr_auto]">
                                <Input aria-label="Nombre del criterio" placeholder="Nombre del criterio" value={criterion.name} onChange={(e) => setCriterion(index, 'name', e.target.value)} data-cy={`criterion-name-${index}`} />
                                <NativeSelect aria-label="Etapa" value={criterion.stage} onChange={(e) => setCriterion(index, 'stage', e.target.value)} options={stages} data-cy={`criterion-stage-${index}`} />
                                <Input aria-label="Ponderación" type="number" step="0.01" min="0" value={criterion.weight} onChange={(e) => setCriterion(index, 'weight', e.target.value)} data-cy={`criterion-weight-${index}`} />
                                <Input aria-label="Puntaje mínimo" type="number" step="0.01" min="0" value={criterion.min_score} onChange={(e) => setCriterion(index, 'min_score', e.target.value)} data-cy={`criterion-min-${index}`} />
                                <Input aria-label="Puntaje máximo" type="number" step="0.01" min="0" value={criterion.max_score} onChange={(e) => setCriterion(index, 'max_score', e.target.value)} data-cy={`criterion-max-${index}`} />
                                <Button
                                    type="button"
                                    variant="ghost"
                                    size="icon"
                                    aria-label="Quitar criterio"
                                    onClick={() => form.setData('criteria', form.data.criteria.filter((_, i) => i !== index))}
                                    data-cy={`remove-criterion-${index}`}
                                >
                                    <Trash2 />
                                </Button>
                            </div>
                            {['name', 'stage', 'weight', 'min_score', 'max_score'].map((field) => (
                                <InputError key={field} message={errors[`criteria.${index}.${field}`]} />
                            ))}
                        </div>
                    ))}
                    <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => form.setData('criteria', [...form.data.criteria, { name: '', stage: 'evaluacion', weight: '', min_score: '0', max_score: '20' }])}
                        data-cy="add-criterion"
                    >
                        <Plus />
                        Agregar criterio
                    </Button>
                    {requiredWeightTotal !== null && (
                        <p className="text-muted-foreground text-xs">
                            Regla configurada: las ponderaciones deben sumar {formatNumber(requiredWeightTotal)}.
                            La vacante puede guardarse como borrador, pero no podrá publicarse si
                            la configuración es inválida.
                        </p>
                    )}
                </CardContent>
            </Card>

            <div className="flex justify-end gap-2">
                <Button variant="outline" asChild>
                    <Link href={vacancyId ? VacancyController.show(vacancyId) : VacancyController.index()}>
                        Cancelar
                    </Link>
                </Button>
                <Button type="submit" disabled={form.processing} data-cy="save-vacancy">
                    {form.processing && <Spinner />}
                    {mode === 'create' ? 'Registrar vacante' : 'Guardar configuración'}
                </Button>
            </div>
        </form>
    );
}
