import type { HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

/**
 * Error de un campo.
 *
 * Va con `role="alert"` para que se anuncie en cuanto aparece tras enviar el
 * formulario. El color es el tono de peligro como texto, no el rojo de relleno
 * de los botones: ese rojo se calibra para llevar blanco encima y como texto
 * sobre una tarjeta oscura quedaba en 4.06:1 (Fase 21).
 *
 * Entra con una aparicion corta y un desplazamiento minimo, lo justo para que
 * el ojo registre que ahi hay algo nuevo sin que el campo de arriba parezca
 * saltar. Nada de sacudidas: un formulario que tiembla castiga a quien se
 * equivoco.
 */
export default function InputError({
    message,
    className = '',
    ...props
}: HTMLAttributes<HTMLParagraphElement> & { message?: string }) {
    return message ? (
        <p
            role="alert"
            {...props}
            className={cn(
                'text-tone-danger-foreground animate-in fade-in-0 slide-in-from-top-1 text-sm duration-150 ease-out',
                className,
            )}
        >
            {message}
        </p>
    ) : null;
}
