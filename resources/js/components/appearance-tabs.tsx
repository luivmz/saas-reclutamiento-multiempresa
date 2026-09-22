import type { LucideIcon } from 'lucide-react';
import { Monitor, Moon, Sun } from 'lucide-react';
import type { HTMLAttributes } from 'react';
import type { Appearance } from '@/hooks/use-appearance';
import { useAppearance } from '@/hooks/use-appearance';
import { cn } from '@/lib/utils';

/**
 * Selector de tema.
 *
 * Es un grupo de botones que alternan una vista, así que cada uno declara con
 * `aria-pressed` si está aplicado; antes solo el color lo decía.
 */
export default function AppearanceToggleTab({
    className = '',
    ...props
}: HTMLAttributes<HTMLDivElement>) {
    const { appearance, updateAppearance } = useAppearance();

    const tabs: { value: Appearance; icon: LucideIcon; label: string }[] = [
        { value: 'light', icon: Sun, label: 'Claro' },
        { value: 'dark', icon: Moon, label: 'Oscuro' },
        { value: 'system', icon: Monitor, label: 'Según el sistema' },
    ];

    return (
        <div
            className={cn(
                'bg-surface inline-flex flex-wrap gap-1 rounded-lg p-1',
                className,
            )}
            role="group"
            aria-label="Tema de la interfaz"
            {...props}
        >
            {tabs.map(({ value, icon: Icon, label }) => (
                <button
                    key={value}
                    type="button"
                    onClick={() => updateAppearance(value)}
                    aria-pressed={appearance === value}
                    className={cn(
                        'flex items-center gap-1.5 rounded-md px-3.5 py-1.5 text-sm transition-colors',
                        appearance === value
                            ? 'bg-card text-foreground font-medium shadow-xs'
                            : 'text-muted-foreground hover:text-foreground',
                    )}
                >
                    <Icon className="size-4" aria-hidden="true" />
                    {label}
                </button>
            ))}
        </div>
    );
}
