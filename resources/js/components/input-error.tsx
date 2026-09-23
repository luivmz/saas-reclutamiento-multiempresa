import type { HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

/**
 * Error de un campo.
 *
 * Va con `role="alert"` para que se anuncie en cuanto aparece tras enviar el
 * formulario, y usa el token `destructive` en lugar de un rojo suelto de la
 * paleta.
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
            className={cn('text-destructive text-sm', className)}
        >
            {message}
        </p>
    ) : null;
}
