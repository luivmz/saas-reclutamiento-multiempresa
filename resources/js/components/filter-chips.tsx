import { cn } from '@/lib/utils';

export function FilterChips({
    options,
    value,
    onChange,
    allLabel = 'Todos',
}: {
    options: { value: string; label: string }[];
    value: string | null;
    onChange: (value: string | null) => void;
    allLabel?: string;
}) {
    const chip = (active: boolean) =>
        cn(
            'rounded-full border px-3 py-1 text-xs font-medium transition-colors',
            active
                ? 'border-primary bg-primary text-primary-foreground'
                : 'bg-background hover:bg-accent',
        );

    return (
        <div className="flex flex-wrap gap-2" data-cy="status-filters">
            <button
                type="button"
                className={chip(value === null)}
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
                    onClick={() => onChange(option.value)}
                >
                    {option.label}
                </button>
            ))}
        </div>
    );
}
