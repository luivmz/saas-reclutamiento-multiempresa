import type { JobCriteria, JobFilterOptions } from '@/types';

export type CriterionKey = keyof JobCriteria;

/** Los tres filtros, en el orden de los controles. La búsqueda va aparte. */
export const FILTER_KEYS = ['organizacion', 'ubicacion', 'contrato'] as const;

export const CRITERION_LABELS: Record<CriterionKey, string> = {
    q: 'Puesto',
    organizacion: 'Organización',
    ubicacion: 'Ubicación',
    contrato: 'Tipo de contrato',
};

/**
 * Parámetros de la dirección para unos criterios: solo los que tienen valor,
 * así un filtro en «Todas» no deja `?organizacion=` vacío en la URL. Sin
 * `page`: cambiar los criterios siempre vuelve a la primera página.
 */
export function criteriaQuery(
    criteria: Partial<Record<CriterionKey, string | number | null>>,
): Record<string, string> {
    const query: Record<string, string> = {};

    for (const key of ['q', ...FILTER_KEYS] as CriterionKey[]) {
        const value = criteria[key];
        const text =
            value === null || value === undefined ? '' : String(value).trim();

        if (text !== '') {
            query[key] = text;
        }
    }

    return query;
}

/** Los mismos criterios sin uno de ellos (para quitarlo desde su etiqueta). */
export function withoutCriterion(
    criteria: JobCriteria,
    key: CriterionKey,
): Record<string, string> {
    return criteriaQuery({ ...criteria, [key]: null });
}

/** Solo la búsqueda: lo que deja «Limpiar filtros». */
export function searchOnly(criteria: JobCriteria): Record<string, string> {
    return criteriaQuery({ q: criteria.q });
}

export function activeFilterCount(criteria: JobCriteria): number {
    return FILTER_KEYS.filter((key) => criteria[key] !== null).length;
}

/**
 * Criterios activos con el texto que ve la persona: el nombre de la
 * organización o del contrato, no su identificador.
 */
export function activeCriteria(
    criteria: JobCriteria,
    options: JobFilterOptions,
): { key: CriterionKey; label: string; value: string }[] {
    const labelOf = (
        list: { value: string; label: string }[],
        value: string | number | null,
    ) =>
        list.find((option) => option.value === String(value))?.label ??
        String(value);

    const active: { key: CriterionKey; label: string; value: string }[] = [];

    if (criteria.q !== '') {
        active.push({ key: 'q', label: CRITERION_LABELS.q, value: criteria.q });
    }

    if (criteria.organizacion !== null) {
        active.push({
            key: 'organizacion',
            label: CRITERION_LABELS.organizacion,
            value: labelOf(options.organizaciones, criteria.organizacion),
        });
    }

    if (criteria.ubicacion !== null) {
        active.push({
            key: 'ubicacion',
            label: CRITERION_LABELS.ubicacion,
            value: criteria.ubicacion,
        });
    }

    if (criteria.contrato !== null) {
        active.push({
            key: 'contrato',
            label: CRITERION_LABELS.contrato,
            value: labelOf(options.contratos, criteria.contrato),
        });
    }

    return active;
}

/** «1 convocatoria», «12 convocatorias». */
export function vacancyCount(total: number): string {
    return total === 1 ? '1 convocatoria' : `${total} convocatorias`;
}
