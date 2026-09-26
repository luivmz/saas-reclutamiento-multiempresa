import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { DataTable } from '@/components/data-table';

/**
 * El apilado en móvil obliga a cambiar el `display` de la tabla, y eso borra
 * sus roles implícitos. Estas pruebas fijan lo que sostiene la semántica
 * cuando eso ocurre: roles explícitos, encabezados que siguen existiendo y la
 * relación `headers` entre cada celda y su columna.
 */
type Row = { id: number; code: string; title: string };

const rows: Row[] = [
    { id: 1, code: 'VAC-001', title: 'Docente de Inglés' },
    { id: 2, code: 'VAC-002', title: 'Auxiliar de Inicial' },
];

function render(extra: Partial<Parameters<typeof DataTable<Row>>[0]> = {}) {
    return renderToStaticMarkup(
        <DataTable<Row>
            caption="Vacantes de su organización"
            data-cy="vacancies-table"
            rows={rows}
            rowKey={(row) => row.id}
            rowAttributes={(row) => ({
                'data-cy': 'vacancy-row',
                'data-code': row.code,
            })}
            columns={[
                { key: 'code', header: 'Código', cell: (row) => row.code },
                { key: 'title', header: 'Vacante', cell: (row) => row.title },
                {
                    key: 'actions',
                    header: <span className="sr-only">Abrir</span>,
                    label: '',
                    cell: () => <a href="/x">Ver</a>,
                },
            ]}
            {...extra}
        />,
    );
}

function headerIds(markup: string): string[] {
    return [...markup.matchAll(/<th[^>]*id="([^"]+)"/g)].map(
        (match) => match[1],
    );
}

describe('DataTable y la semántica que el apilado no debe romper', () => {
    test('declara los roles de tabla, para que sobrevivan al display:block', () => {
        const markup = render();

        expect(markup).toContain('role="table"');
        expect(markup).toContain('role="rowgroup"');
        expect(markup).toContain('role="row"');
        expect(markup).toContain('role="columnheader"');
        expect(markup).toContain('role="cell"');
    });

    test('el encabezado se recorta visualmente, nunca con display:none', () => {
        const markup = render();
        const thead = markup.match(/<thead[^>]*>/)?.[0] ?? '';

        expect(thead).toContain('sr-only');
        expect(thead).not.toMatch(/class="[^"]*\bhidden\b/);
    });

    test('cada celda apunta con headers a un encabezado que existe', () => {
        const markup = render();
        const ids = headerIds(markup);
        const references = [
            ...markup.matchAll(/<td[^>]*headers="([^"]+)"/g),
        ].map((match) => match[1]);

        expect(ids).toHaveLength(3);
        expect(references).toHaveLength(rows.length * 3);
        references.forEach((reference) => expect(ids).toContain(reference));
    });

    test('dos tablas en la misma página no comparten los ids', () => {
        const markup = renderToStaticMarkup(
            <>
                <DataTable<Row>
                    caption="Primera"
                    rows={rows}
                    rowKey={(row) => row.id}
                    columns={[
                        {
                            key: 'code',
                            header: 'Código',
                            cell: (row) => row.code,
                        },
                    ]}
                />
                <DataTable<Row>
                    caption="Segunda"
                    rows={rows}
                    rowKey={(row) => row.id}
                    columns={[
                        {
                            key: 'code',
                            header: 'Código',
                            cell: (row) => row.code,
                        },
                    ]}
                />
            </>,
        );

        const ids = headerIds(markup);

        expect(ids).toHaveLength(2);
        expect(new Set(ids).size).toBe(2);
    });

    test('hay una sola fila por registro y conserva sus data-cy', () => {
        const markup = render();

        expect(markup.match(/<tr/g)).toHaveLength(rows.length + 1);
        expect(markup.match(/data-cy="vacancy-row"/g)).toHaveLength(
            rows.length,
        );
        expect(markup).toContain('data-code="VAC-001"');
        expect(markup).toContain('data-code="VAC-002"');
        expect(markup).toContain('data-cy="vacancies-table"');
    });

    test('la etiqueta de móvil es texto real y no se anuncia dos veces', () => {
        const markup = render();

        // Texto real en el DOM, no contenido generado por CSS.
        expect(markup).not.toContain('content-[attr(data-label)]');
        expect(markup.match(/aria-hidden="true"/g)).toHaveLength(
            // Dos columnas con etiqueta por fila; la de acciones la omite.
            rows.length * 2,
        );
    });

    test('el pie de tabla se conserva cuando se entrega', () => {
        const markup = render({
            footer: (
                <tfoot>
                    <tr>
                        <td data-cy="total">2</td>
                    </tr>
                </tfoot>
            ),
        });

        expect(markup).toContain('data-cy="total"');
    });
});
