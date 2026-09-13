/**
 * Dates are shown in the application timezone (APP_TIMEZONE, exposed by the root view), not in the browser's,
 * so every user sees the same date and time that server-side notifications mention.
 */
function resolveTimeZone(): string | undefined {
    if (typeof document === 'undefined') {
        return undefined;
    }

    const timeZone = document.querySelector<HTMLMetaElement>('meta[name="app-timezone"]')?.content;

    try {
        return timeZone ? new Intl.DateTimeFormat('es-PE', { timeZone }).resolvedOptions().timeZone : undefined;
    } catch {
        return undefined;
    }
}

const timeZone = resolveTimeZone();

const dateFormatter = new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone,
});

// Calendar dates (YYYY-MM-DD) carry no time: format them as-is, without any timezone shift.
const calendarDateFormatter = new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
});

const dateTimeFormatter = new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone,
});

function isCalendarDate(value: string): boolean {
    return value.length === 10;
}

export function formatDate(value?: string | null): string {
    if (!value) {
        return '—';
    }

    return isCalendarDate(value) ? calendarDateFormatter.format(new Date(`${value}T00:00:00Z`)) : dateFormatter.format(new Date(value));
}

export function formatDateTime(value?: string | null): string {
    return value ? dateTimeFormatter.format(new Date(isCalendarDate(value) ? `${value}T00:00:00Z` : value)) : '—';
}

export function formatFileSize(bytes: number): string {
    if (bytes < 1024) {
        return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
        return `${Math.round(bytes / 1024)} KB`;
    }

    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export function formatNumber(value: number | null | undefined, digits = 2): string {
    if (value === null || value === undefined) {
        return '—';
    }

    return value.toLocaleString('es-PE', {
        minimumFractionDigits: 0,
        maximumFractionDigits: digits,
    });
}
