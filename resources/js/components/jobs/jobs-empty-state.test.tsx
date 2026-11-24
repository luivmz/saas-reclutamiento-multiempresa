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
        expect(markup).toMatch(/href="\/empleos\?q=docente"/);
    });

    test('el término se muestra como texto, sin interpretar HTML', () => {
        const markup = renderToStaticMarkup(
            <JobsEmptyState query="<b>x</b>" total={0} />,
        );

        expect(markup).not.toContain('<b>x</b>');
        expect(markup).toContain('&lt;b&gt;x&lt;/b&gt;');
    });
});
