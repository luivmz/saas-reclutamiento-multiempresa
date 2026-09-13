import { FormField, NativeSelect } from '@/components/form-controls';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import type { JobRequest, Presented } from '@/types';

export function JobRequestFields({
    contractTypes,
    defaults,
    errors,
}: {
    contractTypes: Presented[];
    defaults?: JobRequest;
    errors: Record<string, string>;
}) {
    return (
        <div className="grid gap-5 md:grid-cols-2">
            <FormField
                label="Puesto requerido"
                htmlFor="position_title"
                error={errors.position_title}
                className="md:col-span-2"
            >
                <Input
                    id="position_title"
                    name="position_title"
                    defaultValue={defaults?.position_title}
                    maxLength={150}
                    placeholder="Ej. Docente de Matemática - Secundaria"
                    data-cy="position_title"
                />
            </FormField>

            <FormField label="Área solicitante" htmlFor="area" error={errors.area}>
                <Input
                    id="area"
                    name="area"
                    defaultValue={defaults?.area}
                    maxLength={120}
                    placeholder="Ej. Coordinación Académica"
                    data-cy="area"
                />
            </FormField>

            <FormField
                label="Número de plazas"
                htmlFor="headcount"
                error={errors.headcount}
            >
                <Input
                    id="headcount"
                    name="headcount"
                    type="number"
                    min={1}
                    max={50}
                    defaultValue={defaults?.headcount ?? 1}
                    data-cy="headcount"
                />
            </FormField>

            <FormField
                label="Tipo de contrato"
                htmlFor="contract_type"
                error={errors.contract_type}
            >
                <NativeSelect
                    id="contract_type"
                    name="contract_type"
                    options={contractTypes}
                    placeholder="Seleccione…"
                    defaultValue={defaults?.contract_type.value ?? ''}
                    data-cy="contract_type"
                />
            </FormField>

            <FormField
                label="Fecha en que se requiere"
                htmlFor="required_by"
                error={errors.required_by}
                hint="Opcional."
            >
                <Input
                    id="required_by"
                    name="required_by"
                    type="date"
                    defaultValue={defaults?.required_by ?? ''}
                    data-cy="required_by"
                />
            </FormField>

            <FormField
                label="Justificación"
                htmlFor="justification"
                error={errors.justification}
                hint="Explique por qué se necesita la plaza (mínimo 20 caracteres)."
                className="md:col-span-2"
            >
                <Textarea
                    id="justification"
                    name="justification"
                    rows={5}
                    defaultValue={defaults?.justification}
                    data-cy="justification"
                />
            </FormField>
        </div>
    );
}
