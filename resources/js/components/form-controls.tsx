import {
    Children,
    cloneElement,
    isValidElement,
    type ComponentProps,
    type ReactElement,
    type ReactNode,
} from 'react';
import InputError from '@/components/input-error';
import { Label } from '@/components/ui/label';
import { cn } from '@/lib/utils';
import type { Presented } from '@/types';

/**
 * Une los `aria-describedby` que ya trae el control con los de la ayuda y el
 * error, en ese orden y sin repetir.
 *
 * Sustituir el valor propio del control en lugar de sumarlo dejaba mudo lo que
 * el campo ya describía; quedarse con el propio dejaba mudo el error.
 */
function mergeDescribedBy(
    ...values: (string | undefined)[]
): string | undefined {
    const tokens = values
        .filter((value): value is string => typeof value === 'string')
        .flatMap((value) => value.split(/\s+/))
        .filter(Boolean);

    return tokens.length > 0 ? [...new Set(tokens)].join(' ') : undefined;
}

/**
 * Campo de formulario: etiqueta, control, ayuda y error.
 *
 * El campo se encarga de la parte que ningún módulo recordaba repetir: la
 * ayuda y el mensaje de error quedan asociados al control mediante
 * `aria-describedby`, y un control con error queda marcado con
 * `aria-invalid`. Así el error se oye al llegar al campo, no solo se ve
 * debajo.
 */
export function FormField({
    label,
    htmlFor,
    error,
    hint,
    required = false,
    children,
    className,
}: {
    label: string;
    htmlFor: string;
    error?: string;
    hint?: ReactNode;
    required?: boolean;
    children: ReactNode;
    className?: string;
}) {
    const hintId = hint ? `${htmlFor}-hint` : undefined;
    const errorId = error ? `${htmlFor}-error` : undefined;

    const control = Children.map(children, (child) => {
        if (!isValidElement(child)) {
            return child;
        }

        const element = child as ReactElement<Record<string, unknown>>;
        const own = element.props['aria-describedby'];

        return cloneElement(element, {
            'aria-describedby': mergeDescribedBy(
                typeof own === 'string' ? own : undefined,
                hintId,
                errorId,
            ),
            // Un control con error es inválido, diga lo que diga el llamador:
            // dejar `aria-invalid={false}` junto a un mensaje de error le
            // contaría al lector de pantalla lo contrario de lo que se ve.
            'aria-invalid': error ? true : element.props['aria-invalid'],
        });
    });

    return (
        <div className={cn('grid content-start gap-2', className)}>
            <Label htmlFor={htmlFor}>
                {label}
                {required && (
                    <span className="text-muted-foreground ml-1 text-xs font-normal">
                        (obligatorio)
                    </span>
                )}
            </Label>
            {control}
            {hint && (
                <p id={hintId} className="text-muted-foreground text-xs">
                    {hint}
                </p>
            )}
            <InputError id={errorId} message={error} />
        </div>
    );
}

export function NativeSelect({
    options,
    placeholder,
    className,
    ...props
}: ComponentProps<'select'> & {
    options: Pick<Presented, 'value' | 'label'>[];
    placeholder?: string;
}) {
    return (
        <select
            className={cn(
                'border-input focus-visible:border-ring focus-visible:ring-ring/50 dark:bg-input/30 aria-invalid:border-destructive aria-invalid:ring-destructive/20 h-9 w-full rounded-md border bg-transparent px-3 text-sm shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:opacity-50',
                className,
            )}
            {...props}
        >
            {placeholder !== undefined && (
                <option value="">{placeholder}</option>
            )}
            {options.map((option) => (
                <option key={option.value} value={option.value}>
                    {option.label}
                </option>
            ))}
        </select>
    );
}
