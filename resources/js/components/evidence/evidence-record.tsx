import { Form } from '@inertiajs/react';
import {
    Archive,
    CalendarClock,
    FileInput,
    History,
    Link2,
    Link2Off,
    PencilLine,
    UserRound,
} from 'lucide-react';
import EvidenceItemController from '@/actions/App/Http/Controllers/Evidence/EvidenceItemController';
import { FormField, NativeSelect } from '@/components/form-controls';
import InputError from '@/components/input-error';
import { StatusBadge } from '@/components/status-badge';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { Textarea } from '@/components/ui/textarea';
import { formatDateTime } from '@/lib/format';
import type { EvidenceRecord, Presented, RegistrableType } from '@/types';

/** Ancla de la tarjeta de una evidencia; la ayuda documental enlaza a ella. */
export function evidenceAnchor(id: number): string {
    return `evidence-${id}`;
}

/**
 * Una evidencia con su versión vigente, sus enlaces, sus versiones
 * anteriores y las acciones que el usuario puede hacer. Nada se borra:
 * corregir crea una versión nueva y retirar deja la evidencia en el
 * historial.
 */
export function EvidenceRecordCard({
    record,
    criteria,
    registrableTypes,
}: {
    record: EvidenceRecord;
    criteria: Presented[];
    registrableTypes: RegistrableType[];
}) {
    const linkable = criteria.filter(
        (criterion) =>
            !record.links.some((link) => String(link.id) === criterion.value),
    );
    const correctionTypes = registrableTypes.filter(
        (type) => type.source.value === record.source.value,
    );
    const previous = record.versions.slice(0, -1).reverse();

    return (
        <article
            id={evidenceAnchor(record.id)}
            tabIndex={-1}
            className="bg-card target:ring-ring/60 focus-visible:ring-ring/60 data-[destacada=true]:ring-ring/60 scroll-mt-24 space-y-4 rounded-xl border p-4 outline-none target:ring-[3px] focus-visible:ring-[3px] data-[destacada=true]:ring-[3px]"
            data-cy="evidence-record"
            aria-labelledby={`evidence-${record.id}-title`}
        >
            <header className="flex flex-wrap items-start justify-between gap-2">
                <div className="space-y-1.5">
                    <h3
                        id={`evidence-${record.id}-title`}
                        className="flex flex-wrap items-center gap-2 text-sm font-semibold"
                    >
                        <span className="font-mono text-base">
                            {record.code}
                        </span>
                        <span className="bg-tone-primary text-tone-primary-foreground ring-tone-primary-edge rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset">
                            versión {record.version}
                        </span>
                    </h3>
                    <Provenance
                        author={record.author}
                        createdAt={record.created_at}
                        source={record.source.label}
                    />
                </div>
                <div className="flex flex-wrap gap-2">
                    <StatusBadge status={record.type} />
                    <span data-cy="evidence-state">
                        <StatusBadge status={record.state} />
                    </span>
                </div>
            </header>

            <p
                className="border-primary/40 border-l-2 pl-3 text-sm leading-relaxed"
                data-cy="evidence-description"
            >
                {record.description}
            </p>

            {record.withdrawal_reason && (
                <p className="text-muted-foreground text-xs">
                    Motivo del retiro: {record.withdrawal_reason}
                </p>
            )}

            <div className="space-y-2">
                <p className="text-muted-foreground text-xs font-medium">
                    Criterios enlazados
                </p>
                {record.links.length === 0 ? (
                    <p className="text-muted-foreground text-xs">
                        Sin enlaces vigentes.
                    </p>
                ) : (
                    <ul
                        className="flex flex-wrap gap-2"
                        data-cy="evidence-links"
                    >
                        {record.links.map((link) => (
                            <li
                                key={link.id}
                                className="bg-surface flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs"
                            >
                                <Link2 className="size-3" aria-hidden="true" />
                                {link.name}
                                {record.can.link && (
                                    <Form
                                        {...EvidenceItemController.unlink.form({
                                            evidence: record.id,
                                            criterion: link.id,
                                        })}
                                    >
                                        {({ processing }) => (
                                            <button
                                                type="submit"
                                                className="text-muted-foreground hover:text-foreground focus-visible:ring-ring/50 ml-1 rounded-full outline-none focus-visible:ring-[3px]"
                                                disabled={processing}
                                                aria-label={`Retirar el enlace con ${link.name}`}
                                                data-cy="evidence-unlink"
                                            >
                                                <Link2Off
                                                    className="size-3"
                                                    aria-hidden="true"
                                                />
                                            </button>
                                        )}
                                    </Form>
                                )}
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {(record.can.link || record.can.review) && (
                <div className="flex flex-wrap items-end gap-3 border-t pt-4">
                    {record.can.link && linkable.length > 0 && (
                        <Form
                            {...EvidenceItemController.link.form(record.id)}
                            className="flex flex-wrap items-end gap-2"
                        >
                            {({ errors, processing }) => (
                                <>
                                    <FormField
                                        label="Enlazar con un criterio"
                                        htmlFor={`link-${record.id}`}
                                        error={errors.criterion_id}
                                        className="min-w-48"
                                    >
                                        <NativeSelect
                                            id={`link-${record.id}`}
                                            name="criterion_id"
                                            options={linkable}
                                            placeholder="Seleccione…"
                                            required
                                            data-cy="evidence-link-criterion"
                                        />
                                    </FormField>
                                    <Button
                                        type="submit"
                                        variant="outline"
                                        disabled={processing}
                                        data-cy="evidence-link"
                                    >
                                        {processing && <Spinner />}
                                        Enlazar
                                    </Button>
                                </>
                            )}
                        </Form>
                    )}
                    {record.can.review && (
                        <Form
                            {...EvidenceItemController.review.form(record.id)}
                        >
                            {({ errors, processing }) => (
                                <>
                                    <Button
                                        type="submit"
                                        variant="outline"
                                        disabled={processing}
                                        data-cy="evidence-review"
                                    >
                                        {processing && <Spinner />}
                                        Marcar como revisada
                                    </Button>
                                    <InputError message={errors.evidence} />
                                </>
                            )}
                        </Form>
                    )}
                </div>
            )}

            {record.can.correct && (
                <details className="group rounded-lg border p-3">
                    <summary className="flex cursor-pointer items-center gap-2 text-sm font-medium">
                        <PencilLine
                            className="text-primary size-4"
                            aria-hidden="true"
                        />
                        Corregir con una versión nueva
                    </summary>
                    <Form
                        {...EvidenceItemController.correct.form(record.id)}
                        className="mt-3 space-y-3"
                        data-cy="evidence-correct-form"
                    >
                        {({ errors, processing }) => (
                            <>
                                {correctionTypes.length > 1 && (
                                    <FormField
                                        label="Tipo"
                                        htmlFor={`correct-type-${record.id}`}
                                        error={errors.type}
                                    >
                                        <NativeSelect
                                            id={`correct-type-${record.id}`}
                                            name="type"
                                            options={correctionTypes}
                                            defaultValue={record.type.value}
                                        />
                                    </FormField>
                                )}
                                <input
                                    type="hidden"
                                    name="source"
                                    value={record.source.value}
                                />
                                <FormField
                                    label="Descripción corregida"
                                    htmlFor={`correct-description-${record.id}`}
                                    error={errors.description ?? errors.source}
                                    hint="La versión anterior se conserva y queda sustituida."
                                    required
                                >
                                    <Textarea
                                        id={`correct-description-${record.id}`}
                                        name="description"
                                        rows={3}
                                        maxLength={2000}
                                        defaultValue={record.description}
                                        data-cy="evidence-correct-description"
                                    />
                                </FormField>
                                <InputError message={errors.evidence} />
                                <Button
                                    type="submit"
                                    disabled={processing}
                                    data-cy="evidence-correct"
                                >
                                    {processing && <Spinner />}
                                    Registrar versión nueva
                                </Button>
                            </>
                        )}
                    </Form>
                </details>
            )}

            {record.can.withdraw && (
                <details className="rounded-lg border p-3">
                    <summary className="flex cursor-pointer items-center gap-2 text-sm font-medium">
                        <Archive
                            className="text-tone-danger-foreground size-4"
                            aria-hidden="true"
                        />
                        Retirar evidencia
                    </summary>
                    <Form
                        {...EvidenceItemController.withdraw.form(record.id)}
                        className="mt-3 space-y-3"
                        data-cy="evidence-withdraw-form"
                    >
                        {({ errors, processing }) => (
                            <>
                                <FormField
                                    label="Motivo"
                                    htmlFor={`withdraw-reason-${record.id}`}
                                    error={errors.reason}
                                    hint="Empiece por [SINTÉTICO]. La evidencia sigue en el historial."
                                    required
                                >
                                    <Textarea
                                        id={`withdraw-reason-${record.id}`}
                                        name="reason"
                                        rows={2}
                                        maxLength={500}
                                        defaultValue="[SINTÉTICO] "
                                        data-cy="evidence-withdraw-reason"
                                    />
                                </FormField>
                                <InputError message={errors.evidence} />
                                <Button
                                    type="submit"
                                    variant="destructive"
                                    disabled={processing}
                                    data-cy="evidence-withdraw"
                                >
                                    {processing && <Spinner />}
                                    Retirar
                                </Button>
                            </>
                        )}
                    </Form>
                </details>
            )}

            {previous.length > 0 && (
                <details
                    className="rounded-lg border p-3"
                    data-cy="evidence-versions"
                >
                    <summary className="flex cursor-pointer items-center gap-2 text-sm font-medium">
                        <History className="size-4" aria-hidden="true" />
                        Versiones anteriores ({previous.length})
                    </summary>
                    <p className="text-muted-foreground mt-2 text-xs">
                        Se conservan sin cambios: cada corrección añadió una
                        versión nueva encima.
                    </p>
                    <ol className="border-border mt-3 ml-1.5 space-y-4 border-l-2">
                        {previous.map((version) => (
                            <li
                                key={version.id}
                                className="relative space-y-1.5 pl-4 text-sm"
                            >
                                <span
                                    aria-hidden="true"
                                    className="bg-card border-muted-foreground/50 absolute top-1 -left-[7px] size-3 rounded-full border-2"
                                />
                                <p className="flex flex-wrap items-center gap-2 text-xs">
                                    <span className="font-mono font-medium">
                                        {version.code}
                                    </span>
                                    <span className="text-muted-foreground">
                                        versión {version.version}
                                    </span>
                                    <StatusBadge status={version.state} />
                                </p>
                                <Provenance
                                    author={version.author}
                                    createdAt={version.created_at}
                                    source={version.source.label}
                                    data-cy="evidence-version-provenance"
                                />
                                <p className="text-muted-foreground leading-relaxed">
                                    {version.description}
                                </p>
                            </li>
                        ))}
                    </ol>
                </details>
            )}
        </article>
    );
}

/**
 * Procedencia de una versión: quién la registró, cuándo y de qué fuente dice
 * venir. Es la misma línea en la versión vigente y en las anteriores, para que
 * se reconozca de un vistazo.
 */
function Provenance({
    author,
    createdAt,
    source,
    'data-cy': dataCy,
}: {
    author: { name: string; role: string } | null;
    createdAt: string;
    source: string;
    'data-cy'?: string;
}) {
    return (
        <p
            className="text-muted-foreground flex flex-wrap items-center gap-x-3 gap-y-1 text-xs"
            data-cy={dataCy}
        >
            <span className="inline-flex items-center gap-1">
                <UserRound className="size-3.5" aria-hidden="true" />
                {author
                    ? `${author.name} (${author.role})`
                    : 'Autor no disponible'}
            </span>
            <span className="inline-flex items-center gap-1">
                <CalendarClock className="size-3.5" aria-hidden="true" />
                {formatDateTime(createdAt)}
            </span>
            <span className="inline-flex items-center gap-1">
                <FileInput className="size-3.5" aria-hidden="true" />
                Fuente: {source}
            </span>
        </p>
    );
}
