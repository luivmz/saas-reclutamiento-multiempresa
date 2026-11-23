/**
 * RF-28 (candidato): utilidades puras del módulo de reportes.
 *
 * Se separan de la página para probarlas sin navegador: formato de cifras en
 * español, escala de barras y construcción de la consulta de filtros.
 */

const number = new Intl.NumberFormat('es-PE', { maximumFractionDigits: 1 });

const weekLabel = new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: 'short',
    timeZone: 'UTC',
});

/** Cifra en formato es-PE; `null` (sin datos para calcular) se muestra como «—». */
export function formatNumber(value: number | null, suffix = ''): string {
    return value === null ? '—' : `${number.format(value)}${suffix}`;
}

export function plural(count: number, one: string, many: string): string {
    return `${number.format(count)} ${count === 1 ? one : many}`;
}

/** Fecha de calendario (AAAA-MM-DD) del lunes de la semana, sin desplazamiento horario. */
export function formatWeek(weekStart: string): string {
    return weekLabel.format(new Date(`${weekStart}T00:00:00Z`));
}

/**
 * Proporción de una barra respecto al máximo, de 0 a 1. Un valor cero no
 * dibuja barra; la escala empieza siempre en cero.
 */
export function barRatio(value: number, max: number): number {
    if (value <= 0 || max <= 0) {
        return 0;
    }

    return Math.min(1, value / max);
}

export type ReportFilterForm = {
    desde: string;
    hasta: string;
    vacante: string;
    estado: string;
};

/** Parámetros de consulta: solo los filtros con valor, con los nombres que valida el servidor. */
export function reportQuery(form: ReportFilterForm): Record<string, string> {
    return Object.fromEntries(
        Object.entries(form).filter(([, value]) => value.trim() !== ''),
    );
}
