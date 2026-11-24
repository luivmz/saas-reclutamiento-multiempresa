import { CalendarX2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export const DEADLINE_PASSED_LABEL = 'Plazo de postulación vencido';

/**
 * Marca de una vacante publicada cuyo plazo de postulación ya venció (DEF-27).
 *
 * Acompaña al estado formal, no lo reemplaza: la vacante sigue «Publicada»
 * hasta que se cierre el proceso. El dato viene del servidor
 * (`application_deadline_passed`), con la misma regla de fechas que decide si
 * se aceptan postulaciones. Usa el tono de advertencia de los estados y un
 * icono, para no depender solo del color.
 */
export function DeadlinePassedBadge({ className }: { className?: string }) {
    return (
        <span
            data-cy="deadline-passed"
            className={cn(
                'bg-tone-warning text-tone-warning-foreground ring-tone-warning-edge inline-flex max-w-full items-center gap-1.5 rounded-md px-2 py-0.5 text-xs font-medium whitespace-normal ring-1 ring-inset',
                className,
            )}
        >
            <CalendarX2 className="size-3.5 shrink-0" aria-hidden="true" />
            {DEADLINE_PASSED_LABEL}
        </span>
    );
}
