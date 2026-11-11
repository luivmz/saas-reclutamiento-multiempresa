import { Form, Head, Link } from '@inertiajs/react';
import { FileStack, FlaskConical, History, Lock } from 'lucide-react';
import { useState } from 'react';
import ApplicationController from '@/actions/App/Http/Controllers/Applications/ApplicationController';
import ApplicationEvidenceController from '@/actions/App/Http/Controllers/Evidence/ApplicationEvidenceController';
import { EmptyState } from '@/components/empty-state';
import { DocumentaryAid } from '@/components/evidence/documentary-aid';
import { EvidenceRecordCard } from '@/components/evidence/evidence-record';
import { FormField, NativeSelect } from '@/components/form-controls';
import { PageContainer, PageHeader, Section } from '@/components/page';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { dashboard } from '@/routes';
import type {
    DocumentaryAidResult,
    EvidenceRecord,
    EvidenceSearchResult,
    Presented,
    RegistrableType,
} from '@/types';

type Props = {
    application: {
        id: number;
        code: string;
        vacancy: { id: number; code: string; title: string; closed: boolean };
    };
    records: EvidenceRecord[];
    criteria: Presented[];
    registrableTypes: RegistrableType[];
    aid: DocumentaryAidResult | null;
    search: EvidenceSearchResult | null;
    filters: { criterio: number | null; buscar: string | null };
    can: { create: boolean; viewHistory: boolean; viewFile: boolean };
};

export default function EvidenceIndex({
    application,
    records,
    criteria,
    registrableTypes,
    aid,
    search,
    filters,
    can,
}: Props) {
    const [typeValue, setTypeValue] = useState(
        registrableTypes[0]?.value ?? '',
    );
    const selectedType = registrableTypes.find(
        (type) => type.value === typeValue,
    );

    return (
        <>
            <Head title={`Evidencias de ${application.code}`} />
            <PageContainer>
                <PageHeader
                    eyebrow={
                        <>
                            <span className="font-mono text-xs">
                                {application.code}
                            </span>
                            <span className="bg-tone-info text-tone-info-foreground ring-tone-info-edge inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ring-1">
                                <FlaskConical
                                    className="size-3"
                                    aria-hidden="true"
                                />
                                Experimental
                            </span>
                        </>
                    }
                    title="Evidencias de la postulación"
                    description={`${application.vacancy.title} (${application.vacancy.code})`}
                    actions={
                        <div className="flex flex-wrap gap-2">
                            {can.viewHistory && (
                                <Button variant="outline" asChild>
                                    <Link
                                        href={ApplicationEvidenceController.history(
                                            application.id,
                                        )}
                                        data-cy="evidence-history-link"
                                    >
                                        <History aria-hidden="true" />
                                        Historial
                                    </Link>
                                </Button>
                            )}
                            {can.viewFile && (
                                <Button variant="outline" asChild>
                                    <Link
                                        href={ApplicationController(
                                            application.id,
                                        )}
                                    >
                                        Volver al expediente
                                    </Link>
                                </Button>
                            )}
                        </div>
                    }
                />

                <Alert data-cy="experimental-notice">
                    <FlaskConical />
                    <AlertTitle>
                        Entorno experimental con datos ficticios
                    </AlertTitle>
                    <AlertDescription>
                        Este flujo vive solo en la rama local de pruebas y no es
                        la integración formal en el SaaS, que sigue pendiente de
                        la G0 real y de una decisión del equipo. Las evidencias
                        no alimentan el ranking ni la decisión final, que
                        corresponde a Dirección.
                    </AlertDescription>
                </Alert>

                {application.vacancy.closed && (
                    <Alert data-cy="evidence-frozen">
                        <Lock />
                        <AlertTitle>Vacante cerrada</AlertTitle>
                        <AlertDescription>
                            Las evidencias se pueden consultar, pero ya no se
                            pueden registrar ni modificar.
                        </AlertDescription>
                    </Alert>
                )}

                <div className="grid min-w-0 gap-6 lg:grid-cols-3">
                    <div className="min-w-0 space-y-6 lg:col-span-2">
                        <Section
                            title="Evidencias registradas"
                            description="Cada corrección crea una versión nueva y la anterior se conserva. Nada se borra."
                            data-cy="evidence-list"
                        >
                            {records.length === 0 ? (
                                <EmptyState
                                    icon={FileStack}
                                    title="Todavía no hay evidencias"
                                    description={
                                        can.create
                                            ? 'Registre la primera con el formulario de abajo.'
                                            : 'Cuando RR. HH. o un evaluador asignado registren evidencias, aparecerán aquí.'
                                    }
                                />
                            ) : (
                                <div className="space-y-4">
                                    {records.map((record) => (
                                        <EvidenceRecordCard
                                            key={record.id}
                                            record={record}
                                            criteria={criteria}
                                            registrableTypes={registrableTypes}
                                        />
                                    ))}
                                </div>
                            )}
                        </Section>

                        {can.create && registrableTypes.length > 0 && (
                            <Section
                                title="Registrar evidencia"
                                description="Declare el tipo y describa la evidencia. El texto debe empezar por [SINTÉTICO]."
                                data-cy="evidence-create"
                            >
                                <Form
                                    {...ApplicationEvidenceController.store.form(
                                        application.id,
                                    )}
                                    className="space-y-4"
                                    resetOnSuccess={['description']}
                                >
                                    {({ errors, processing }) => (
                                        <>
                                            <div className="grid gap-4 sm:grid-cols-2">
                                                <FormField
                                                    label="Tipo"
                                                    htmlFor="evidence-type"
                                                    error={errors.type}
                                                    required
                                                >
                                                    <NativeSelect
                                                        id="evidence-type"
                                                        name="type"
                                                        options={
                                                            registrableTypes
                                                        }
                                                        value={typeValue}
                                                        onChange={(event) =>
                                                            setTypeValue(
                                                                event.target
                                                                    .value,
                                                            )
                                                        }
                                                        data-cy="evidence-type"
                                                    />
                                                </FormField>
                                                <div className="grid content-start gap-2">
                                                    <span className="text-sm font-medium">
                                                        Fuente
                                                    </span>
                                                    <p
                                                        className="text-muted-foreground flex h-9 items-center text-sm"
                                                        data-cy="evidence-source"
                                                    >
                                                        {selectedType?.source
                                                            .label ?? '—'}
                                                    </p>
                                                    <input
                                                        type="hidden"
                                                        name="source"
                                                        value={
                                                            selectedType?.source
                                                                .value ?? ''
                                                        }
                                                    />
                                                </div>
                                            </div>
                                            <FormField
                                                label="Descripción"
                                                htmlFor="evidence-description"
                                                error={
                                                    errors.description ??
                                                    errors.source ??
                                                    errors.evidence
                                                }
                                                hint="Solo datos ficticios: sin nombres, correos, teléfonos ni enlaces."
                                                required
                                            >
                                                <Textarea
                                                    id="evidence-description"
                                                    name="description"
                                                    rows={3}
                                                    maxLength={2000}
                                                    defaultValue="[SINTÉTICO] "
                                                    data-cy="evidence-description-input"
                                                />
                                            </FormField>
                                            <div className="flex justify-end">
                                                <Button
                                                    type="submit"
                                                    disabled={processing}
                                                    data-cy="evidence-submit"
                                                >
                                                    {processing && <Spinner />}
                                                    Registrar evidencia
                                                </Button>
                                            </div>
                                        </>
                                    )}
                                </Form>
                            </Section>
                        )}
                    </div>

                    <DocumentaryAid
                        applicationId={application.id}
                        criteria={criteria}
                        aid={aid}
                        search={search}
                        filters={filters}
                    />
                </div>
            </PageContainer>
        </>
    );
}

EvidenceIndex.layout = {
    breadcrumbs: [
        { title: 'Panel', href: dashboard() },
        { title: 'Evidencias (experimental)', href: dashboard() },
    ],
};
