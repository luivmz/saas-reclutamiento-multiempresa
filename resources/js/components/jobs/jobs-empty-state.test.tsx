import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { JobsEmptyState } from '@/components/jobs/jobs-empty-state';

/**
 * DEF-26: el listado decía «No hay convocatorias vigentes» también cuando una
 * búsqueda no encontraba nada, y no ofrecía cómo quitar el filtro.
 */
describe('Empleos · estados vacíos', () => {
    test('una búsqueda sin coincidencias nombra el término y ofrece ver todas', () => {
        const markup = renderToStaticMarkup(
            <JobsEmptyState query="astronauta" total={0} />,
        );

        expect(markup).toContain(
            'Ninguna convocatoria coincide con «astronauta»',
        );
        expect(markup).toContain('Ver todas las convocatorias');
        expect(markup).toMatch(/href="\/empleos"/);
        expect(markup).not.toContain('No hay convocatorias vigentes');
    });

    test('sin ofertas publicadas no habla de búsquedas ni ofrece quitar un filtro', () => {
        const markup = renderToStaticMarkup(
            <JobsEmptyState query="" total={0} />,
        );

        expect(markup).toContain('Todavía no hay convocatorias publicadas');
        expect(markup).not.toContain('Ver todas las convocatorias');
        expect(markup).not.toMatch(/búsqueda/i);
    });

    test('una página vacía de una lista con ofertas lleva a la primera página sin perder la búsqueda', () => {
        const markup = renderToStaticMarkup(
            <JobsEmptyState query="docente" total={14} />,
        );

        expect(markup).toContain('Esta página no tiene convocatorias');
        // Solo se sabe que la página no existe; no se supone que la lista cambió.
        expect(markup).not.toMatch(/cambi/i);
        expect(markup).toMatch(/href="\/empleos\?q=docente"/);
    });

    test.each([
        [
            '',
            'Ninguna convocatoria coincide con los filtros actuales',
            'Quitar filtros',
        ],
        [
            'docente',
            'Ninguna convocatoria coincide con «docente» y los filtros actuales',
            'Quitar búsqueda y filtros',
        ],
    ])(
        'distingue una combinación sin coincidencias con el puesto «%s»',
        (query, title, action) => {
            const markup = renderToStaticMarkup(
                <JobsEmptyState query={query} total={0} filterCount={2} />,
            );
            expect(markup).toContain(title);
            expect(markup).toContain(action);
            expect(markup).toContain('href="/empleos"');
        },
    );

    test('la salida de página fuera de rango conserva todos los criterios', () => {
        const markup = renderToStaticMarkup(
            <JobsEmptyState
                query="aula"
                total={14}
                criteria={{
                    q: 'aula',
                    organizacion: '2',
                    ubicacion: 'Lima',
                    contrato: 'por_horas',
                }}
            />,
        );
        expect(markup).toContain(
            'q=aula&amp;organizacion=2&amp;ubicacion=Lima&amp;contrato=por_horas',
        );
        expect(markup).not.toContain('page=');
    });

    test('el término se muestra como texto, sin interpretar HTML', () => {
        const markup = renderToStaticMarkup(
            <JobsEmptyState query="<b>x</b>" total={0} />,
        );

        expect(markup).not.toContain('<b>x</b>');
        expect(markup).toContain('&lt;b&gt;x&lt;/b&gt;');
    });
});
