import { Monitor, Moon, Sun } from 'lucide-react';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import type { Appearance } from '@/hooks/use-appearance';
import { useAppearance } from '@/hooks/use-appearance';

/**
 * Cambio de tema desde la barra superior.
 *
 * El tema ya existía, pero solo se podía cambiar entrando a Configuración →
 * Apariencia. Quien trabaja de noche con tablas largas no debería tener que
 * salir de la página para bajar el brillo.
 */
const options: { value: Appearance; icon: typeof Sun; label: string }[] = [
    { value: 'light', icon: Sun, label: 'Claro' },
    { value: 'dark', icon: Moon, label: 'Oscuro' },
    { value: 'system', icon: Monitor, label: 'Según el sistema' },
];

export function AppearanceToggle() {
    const { appearance, resolvedAppearance, updateAppearance } =
        useAppearance();
    const Icon = resolvedAppearance === 'dark' ? Moon : Sun;

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button
                    variant="ghost"
                    size="icon"
                    className="size-8"
                    data-cy="appearance-toggle"
                >
                    <Icon className="size-4" aria-hidden="true" />
                    <span className="sr-only">Cambiar tema</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="min-w-44">
                {options.map((option) => (
                    <DropdownMenuItem
                        key={option.value}
                        onSelect={() => updateAppearance(option.value)}
                        className="cursor-pointer"
                        data-active={appearance === option.value}
                    >
                        <option.icon className="size-4" aria-hidden="true" />
                        {option.label}
                        {appearance === option.value && (
                            <span className="text-muted-foreground ml-auto text-xs">
                                Activo
                            </span>
                        )}
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
