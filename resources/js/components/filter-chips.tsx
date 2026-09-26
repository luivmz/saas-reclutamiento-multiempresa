import { cn } from '@/lib/utils';

/**
 * Filtro por estado.
 *
 * Son botones que alternan una vista, no enlaces: `aria-pressed` dice cuál
 * está aplicado, y el grupo se anuncia con su propósito. Antes el único
 * indicio de la opción activa era el color.
 */
export function FilterChips({
    options,
    value,
    onChange,
    allLabel = 'Todos',
    label = 'Filtrar por estado',
}: {
    options: { value: string; label: string }[];
    value: string | null;
    onChange: (value: string | null) => void;
    allLabel?: string;
    label?: string;
}) {
    const chip = (active: boolean) =>
        cn(
            'rounded-full border px-3 py-1.5 text-xs font-medium transition-colors',
            active
                ? 'border-primary bg-primary text-primary-foreground'
                : 'bg-card text-muted-foreground hover:border-input hover:text-foreground',
        );

    return (
        <div
            className="flex flex-wrap gap-2"
            role="group"
            aria-label={label}
            data-cy="status-filters"
        >
            <button
                type="button"
                className={chip(value === null)}
                aria-pressed={value === null}
                onClick={() => onChange(null)}
            >
                {allLabel}
            </button>
            {options.map((option) => (
                <button
                    key={option.value}
                    type="button"
                    data-cy={`filter-${option.value}`}
                    className={chip(value === option.value)}
                    aria-pressed={value === option.value}
                    onClick={() => onChange(option.value)}
                >
                    {option.label}
                </button>
            ))}
        </div>
    );
}
