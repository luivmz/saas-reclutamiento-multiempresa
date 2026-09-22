import type { HTMLAttributes, Key, ReactNode } from 'react';
import { cn } from '@/lib/utils';

/**
 * Tabla de expedientes.
 *
 * Existía la misma tabla copiada en requerimientos, vacantes, postulaciones,
 * auditoría y ranking: mismas clases, mismos errores. Aquí se resuelven una
 * sola vez tres cosas que faltaban en todas:
 *
 * - `scope="col"` y `<caption>`, para que un lector de pantalla anuncie a qué
 *   columna pertenece cada celda y qué contiene la tabla;
 * - un encabezado que se queda fijo al desplazar tablas largas;
 * - en pantallas angostas, cada fila se apila como una ficha con su etiqueta
 *   delante, en lugar de obligar a arrastrar la tabla en horizontal.
 *
 * El apilado es puramente CSS y conserva un solo DOM: las filas siguen siendo
 * los mismos elementos con los mismos `data-cy` en cualquier ancho.
 */

export type Column<Row> = {
    /** Identificador estable de la columna. */
    key: string;
    /** Encabezado visible. */
    header: ReactNode;
    /**
     * Etiqueta en texto plano que precede al valor cuando la fila se apila.
     * Por omisión se usa `header`, que sirve cuando es una cadena.
     */
    label?: string;
    cell: (row: Row) => ReactNode;
    align?: 'start' | 'center' | 'end';
    className?: string;
    headerClassName?: string;
};

type Props<Row> = {
    /** Qué contiene la tabla. Se anuncia al lector de pantalla. */
    caption: string;
    columns: Column<Row>[];
    rows: Row[];
    rowKey: (row: Row) => Key;
    /** Atributos por fila: `data-cy`, `data-code`, etc. */
    rowAttributes?: (
        row: Row,
    ) => HTMLAttributes<HTMLTableRowElement> &
        Record<`data-${string}`, string | number | undefined>;
    /** Pie de tabla, por ejemplo un total. */
    footer?: ReactNode;
    className?: string;
} & Record<`data-${string}`, string | undefined>;

const alignment = {
    start: 'md:text-left',
    center: 'md:text-center',
    end: 'md:text-right',
} as const;

export function DataTable<Row>({
    caption,
    columns,
    rows,
    rowKey,
    rowAttributes,
    footer,
    className,
    ...props
}: Props<Row>) {
    return (
        <div
            className={cn(
                'bg-card overflow-x-auto rounded-xl md:border',
                className,
            )}
        >
            <table className="w-full text-sm" {...props}>
                <caption className="sr-only">{caption}</caption>
                <thead className="bg-surface text-muted-foreground sticky top-0 z-10 hidden text-left text-xs md:table-header-group">
                    <tr>
                        {columns.map((column) => (
                            <th
                                key={column.key}
                                scope="col"
                                className={cn(
                                    'border-b px-4 py-3 font-medium whitespace-nowrap',
                                    alignment[column.align ?? 'start'],
                                    column.headerClassName,
                                )}
                            >
                                {column.header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="block space-y-3 md:table-row-group md:space-y-0 md:divide-y">
                    {rows.map((row) => {
                        const { className: rowClassName, ...attributes } =
                            rowAttributes?.(row) ?? {};

                        return (
                            <tr
                                key={rowKey(row)}
                                {...attributes}
                                className={cn(
                                    'bg-card md:hover:bg-surface/60 block rounded-xl border p-4 md:table-row md:rounded-none md:border-0 md:p-0 md:transition-colors',
                                    rowClassName,
                                )}
                            >
                                {columns.map((column) => (
                                    <td
                                        key={column.key}
                                        data-label={
                                            column.label ??
                                            (typeof column.header === 'string'
                                                ? column.header
                                                : undefined)
                                        }
                                        className={cn(
                                            'before:text-muted-foreground flex items-baseline gap-3 py-1 before:w-28 before:shrink-0 before:text-xs before:content-[attr(data-label)] md:table-cell md:px-4 md:py-3 md:before:content-none',
                                            alignment[column.align ?? 'start'],
                                            column.className,
                                        )}
                                    >
                                        {column.cell(row)}
                                    </td>
                                ))}
                            </tr>
                        );
                    })}
                </tbody>
                {footer}
            </table>
        </div>
    );
}
