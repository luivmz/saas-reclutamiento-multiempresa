import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { STAGE_SHEETS } from '@/components/experience-3d/recruitment-scene-poster';
import { Reveal } from '@/components/reveal';

/**
 * Incremento visual de la portada. Lo que no depende del navegador: el
 * contenido se ve antes de montar (y sin JavaScript), y la escena dibuja las
 * tres etapas que cuenta el expediente. El ocultamiento al desplazarse y el
 * paralaje se prueban en `e2e-22`.
 */
describe('Reveal', () => {
    test('antes de montar el contenido es visible: estado estático, sin retardo', () => {
        const markup = renderToStaticMarkup(
            <Reveal delay={120} data-cy="bloque">
                Contenido
            </Reveal>,
        );

        expect(markup).toContain('data-reveal="static"');
        expect(markup).not.toContain('transition-delay');
        expect(markup).toContain('data-cy="bloque"');
        expect(markup).toContain('Contenido');
    });
});

describe('Hojas de la escena', () => {
    test('son las tres etapas del expediente, en este orden', () => {
        expect(STAGE_SHEETS.map((sheet) => sheet.stage)).toEqual([
            'vacancy',
            'evidence',
            'decision',
        ]);
    });
});
