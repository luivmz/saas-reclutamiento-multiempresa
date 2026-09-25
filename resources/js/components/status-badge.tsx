import { cn } from '@/lib/utils';
import type { Presented, Tone } from '@/types';

/**
 * Estado de una entidad, con el vocabulario de color definido en `app.css`.
 *
 * Los tonos vienen de tokens (`--tone-*`) y no de la paleta de Tailwind: así el
 * mismo estado se ve igual en una tabla, en una línea de tiempo y en el
 * encabezado de una página, y el modo oscuro se resuelve en un solo sitio.
 */
const toneClasses: Record<Tone, string> = {
    neutral:
        'bg-tone-neutral text-tone-neutral-foreground ring-tone-neutral-edge',
    info: 'bg-tone-info text-tone-info-foreground ring-tone-info-edge',
    primary:
        'bg-tone-primary text-tone-primary-foreground ring-tone-primary-edge',
    success:
        'bg-tone-success text-tone-success-foreground ring-tone-success-edge',
    warning:
        'bg-tone-warning text-tone-warning-foreground ring-tone-warning-edge',
    danger: 'bg-tone-danger text-tone-danger-foreground ring-tone-danger-edge',
};

export function StatusBadge({
    status,
    className,
}: {
    status: Presented;
    className?: string;
}) {
    return (
        <span
            data-cy="status-badge"
            data-status={status.value}
            className={cn(
                'inline-flex max-w-full items-center gap-1.5 rounded-md px-2 py-0.5 text-xs font-medium whitespace-normal ring-1 ring-inset md:whitespace-nowrap',
                toneClasses[status.tone],
                className,
            )}
        >
            {/* Un punto del mismo tono: quien no distingue los colores sigue
                viendo un marcador de estado, y el badge no depende solo del
                fondo para leerse como tal. */}
            <span
                aria-hidden="true"
                className="size-1.5 shrink-0 rounded-full bg-current opacity-70"
            />
            {status.label}
        </span>
    );
}
