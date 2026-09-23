import { Eye, EyeOff } from 'lucide-react';
import type { ComponentProps, Ref } from 'react';
import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

/**
 * Campo de contraseña con conmutador de visibilidad.
 *
 * El botón estaba fuera del orden de tabulación (`tabIndex={-1}`), heredado
 * del kit de inicio: quien no usa ratón no podía comprobar lo que había
 * escrito. Ahora es un `<button>` normal, alcanzable con Tab y activable con
 * Enter o Espacio como cualquier botón nativo.
 *
 * El estado se anuncia por el nombre accesible, que cambia entre «Mostrar la
 * contraseña» y «Ocultar la contraseña». No se añade además `aria-pressed`:
 * duplicar la información haría que el lector de pantalla dijera dos veces lo
 * mismo, con dos vocabularios distintos.
 */
export default function PasswordInput({
    className,
    ref,
    ...props
}: Omit<ComponentProps<'input'>, 'type'> & { ref?: Ref<HTMLInputElement> }) {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="relative">
            <Input
                type={showPassword ? 'text' : 'password'}
                className={cn('pr-10', className)}
                ref={ref}
                {...props}
            />
            <button
                type="button"
                onClick={() => setShowPassword((prev) => !prev)}
                className="text-muted-foreground hover:text-foreground absolute inset-y-0 right-0 flex items-center rounded-r-md px-3"
                aria-label={
                    showPassword
                        ? 'Ocultar la contraseña'
                        : 'Mostrar la contraseña'
                }
                aria-controls={props.id}
                data-cy="toggle-password-visibility"
            >
                {showPassword ? (
                    <EyeOff className="size-4" aria-hidden="true" />
                ) : (
                    <Eye className="size-4" aria-hidden="true" />
                )}
            </button>
        </div>
    );
}
