import type { LucideIcon } from 'lucide-react';
import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';

/**
 * Opciones de una decisión, presentadas como fichas.
 *
 * Los formularios de decisión —validar o rechazar un requerimiento, elegir al
 * candidato seleccionado— usaban `<input type="radio">` sueltos con estilos
 * distintos en cada página. Aquí la ficha es una sola y el control nativo
 * sigue debajo: el teclado, las flechas y el lector de pantalla funcionan como
 * en cualquier grupo de radios.
 *
 * El borde de la opción elegida cambia de color **y** de grosor: el color solo
 * no basta para quien no lo distingue.
 */

type Tone = 'primary' | 'success' | 'danger';

const toneRing: Record<Tone, string> = {
    primary: 'has-[:checked]:border-primary has-[:checked]:bg-tone-primary/50',
    success:
        'has-[:checked]:border-tone-success-edge has-[:checked]:bg-tone-success/60',
    danger: 'has-[:checked]:border-tone-danger-edge has-[:checked]:bg-tone-danger/60',
};

const toneIcon: Record<Tone, string> = {
    primary: 'text-primary',
    success: 'text-tone-success-foreground',
    danger: 'text-tone-danger-foreground',
};

const base =
    'flex cursor-pointer items-start gap-3 rounded-lg border p-4 text-sm transition-colors has-[:checked]:border-2 has-[:checked]:p-[15px] has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 has-[:focus-visible]:outline-ring';

export function RadioCard({
    name,
    value,
    title,
    description,
    icon: Icon,
    tone = 'primary',
    defaultChecked,
    'data-cy': dataCy,
    trailing,
}: {
    name: string;
    value: string | number;
    title: ReactNode;
    description?: ReactNode;
    icon?: LucideIcon;
    tone?: Tone;
    defaultChecked?: boolean;
    'data-cy'?: string;
    trailing?: ReactNode;
}) {
    return (
        <label className={cn(base, toneRing[tone])}>
            <input
                type="radio"
                name={name}
                value={value}
                defaultChecked={defaultChecked}
                className="mt-1 size-4 shrink-0 accent-current"
                data-cy={dataCy}
            />
            <span className="min-w-0 flex-1">
                <span className="flex items-center gap-2 font-medium">
                    {Icon && (
                        <Icon
                            className={cn('size-4', toneIcon[tone])}
                            aria-hidden="true"
                        />
                    )}
                    {title}
                </span>
                {description && (
                    <span className="text-muted-foreground mt-0.5 block text-xs leading-relaxed">
                        {description}
                    </span>
                )}
            </span>
            {trailing}
        </label>
    );
}

export function CheckCard({
    name,
    value = '1',
    children,
    'data-cy': dataCy,
}: {
    name: string;
    value?: string;
    children: ReactNode;
    'data-cy'?: string;
}) {
    return (
        <label
            className={cn(
                base,
                'has-[:checked]:border-primary border-dashed has-[:checked]:border-solid',
            )}
        >
            <input
                type="checkbox"
                name={name}
                value={value}
                className="mt-0.5 size-4 shrink-0"
                data-cy={dataCy}
            />
            <span className="leading-relaxed">{children}</span>
        </label>
    );
}
