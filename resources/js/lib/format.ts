const dateFormatter = new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
});

const dateTimeFormatter = new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
});

function parse(value: string): Date {
    return value.length === 10 ? new Date(`${value}T00:00:00`) : new Date(value);
}

export function formatDate(value?: string | null): string {
    return value ? dateFormatter.format(parse(value)) : '—';
}

export function formatDateTime(value?: string | null): string {
    return value ? dateTimeFormatter.format(parse(value)) : '—';
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
