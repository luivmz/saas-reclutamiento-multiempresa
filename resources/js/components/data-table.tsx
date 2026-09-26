import { useId, type HTMLAttributes, type Key, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

/**
 * Tabla de expedientes.
 *
 * Existía la misma tabla copiada en requerimientos, vacantes, postulaciones,
 * auditoría y ranking: mismas clases, mismos errores. Aquí se resuelven una
 * sola vez, y con un solo DOM en todos los anchos.
 *
 * **Por qué la semántica está escrita a mano.** En pantallas angostas la fila
 * se apila como ficha, y apilarla exige `display: block` y `display: flex`
 * sobre `tbody`, `tr` y `td`. Cambiar el `display` de los elementos de una
 * tabla destruye sus roles implícitos: el navegador deja de exponerla como
 * tabla y la convierte en bloques sueltos. Por eso:
 *
 * - cada elemento declara su rol (`table`, `rowgroup`, `row`, `columnheader`,
 *   `cell`), que en escritorio solo repite lo nativo y en móvil lo restituye;
 * - el encabezado **no se oculta con `display: none`** —eso lo borraría del
 *   árbol de accesibilidad—, sino que se recorta visualmente y sigue
 *   existiendo;
 * - cada celda apunta a su encabezado con `headers`, una relación explícita
 *   que no depende de que el algoritmo nativo de tablas siga vigente.
 *
 * La etiqueta que se ve delante del valor en móvil es texto real y no
 * contenido generado por CSS, y va con `aria-hidden` porque la asociación
 * `headers` ya entrega ese dato a la tecnología asistiva: mostrarlo dos veces
 * haría que se oyera el encabezado repetido.
 */

export type Column<Row> = {
    /** Identificador estable de la columna. */
    key: string;
    /** Encabezado visible. */
    header: ReactNode;
    /**
     * Etiqueta en texto plano que precede al valor cuando la fila se apila.
     * Por omisión se usa `header`, que sirve cuando es una cadena. Una cadena
     * vacía deja la celda sin etiqueta, para columnas de acciones.
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

function labelOf<Row>(column: Column<Row>): string | undefined {
    if (column.label !== undefined) {
        return column.label || undefined;
    }

    return typeof column.header === 'string' ? column.header : undefined;
}

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
    // `useId` puede traer caracteres que no sirven como identificador HTML
    // limpio; lo que importa es que sea único por tabla montada, para que dos
    // tablas en la misma página no compartan los ids de sus encabezados.
    const scope = `dt${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
    const headerId = (key: string) => `${scope}-${key}`;

    return (
        <div
            className={cn(
                'bg-card overflow-x-auto rounded-xl md:border',
                className,
            )}
        >
            <table role="table" className="block w-full text-sm md:table" {...props}>
                <caption className="sr-only">{caption}</caption>
                <thead
                    role="rowgroup"
                    className="text-muted-foreground sr-only text-left text-xs md:not-sr-only md:table-header-group"
                >
                    <tr role="row">
                        {columns.map((column) => (
                            <th
                                key={column.key}
                                id={headerId(column.key)}
                                role="columnheader"
                                scope="col"
                                className={cn(
                                    'bg-surface border-b px-4 py-3 font-medium whitespace-nowrap md:sticky md:top-0 md:z-10',
                                    alignment[column.align ?? 'start'],
                                    column.headerClassName,
                                )}
                            >
                                {column.header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody
                    role="rowgroup"
                    className="block space-y-3 md:table-row-group md:space-y-0 md:divide-y"
                >
                    {rows.map((row) => {
                        const { className: rowClassName, ...attributes } =
                            rowAttributes?.(row) ?? {};

                        return (
                            <tr
                                key={rowKey(row)}
                                role="row"
                                {...attributes}
                                className={cn(
                                    'bg-card md:hover:bg-surface/60 block rounded-xl border p-4 md:table-row md:rounded-none md:border-0 md:p-0 md:transition-colors',
                                    rowClassName,
                                )}
                            >
                                {columns.map((column) => {
                                    const label = labelOf(column);

                                    return (
                                        <td
                                            key={column.key}
                                            role="cell"
                                            headers={headerId(column.key)}
                                            className={cn(
                                                'flex items-baseline gap-3 py-1 md:table-cell md:px-4 md:py-3',
                                                alignment[
                                                    column.align ?? 'start'
                                                ],
                                                column.className,
                                            )}
                                        >
                                            {label && (
                                                <span
                                                    aria-hidden="true"
                                                    className="text-muted-foreground w-28 shrink-0 text-xs md:hidden"
                                                >
                                                    {label}
                                                </span>
                                            )}
                                            <span className="min-w-0 flex-1 md:contents">
                                                {column.cell(row)}
                                            </span>
                                        </td>
                                    );
                                })}
                            </tr>
                        );
                    })}
                </tbody>
                {footer}
            </table>
        </div>
    );
}
