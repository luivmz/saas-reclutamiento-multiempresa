import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    folderOpenness,
    sheetTransform,
} from '@/components/experience-3d/recruitment-scene';
import { STAGE_SHEETS } from '@/components/experience-3d/recruitment-scene-poster';
import { Reveal } from '@/components/reveal';

/**
 * Incremento visual de la portada. Lo que no depende del navegador: el
 * contenido se ve antes de montar (y sin JavaScript), y la escena dibuja las
 * tres etapas que cuenta el expediente, y la carpeta del proceso se abre según
 * el desplazamiento. El ocultamiento al desplazarse y el paralaje se prueban
 * en `e2e-22` y `e2e-23`.
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

describe('Carpeta del proceso: se abre al bajar y se cierra al subir', () => {
    test('cerrada antes de entrar, abierta al llegar al tercio superior, y monótona entre medias', () => {
        const viewport = 800;

        expect(folderOpenness(viewport, viewport)).toBe(0);
        expect(folderOpenness(0.9 * viewport, viewport)).toBe(0);
        expect(folderOpenness(0.3 * viewport, viewport)).toBe(1);
        expect(folderOpenness(-400, viewport)).toBe(1);

        let previous = -1;

        for (let top = viewport; top >= 0; top -= 20) {
            const open = folderOpenness(top, viewport);

            expect(open).toBeGreaterThanOrEqual(previous);
            previous = open;
        }
    });

    test('cerrada, las hojas se apilan detrás del expediente; abierta, se separan en profundidad', () => {
        expect(sheetTransform('vacancy', 0)).toBe(
            'translate3d(0px, -27px, -36px) rotateZ(0deg)',
        );
        expect(sheetTransform('vacancy', 1)).toBe(
            'translate3d(-44px, -128px, -170px) rotateZ(-3deg)',
        );
        expect(sheetTransform('decision', 1)).toBe(
            'translate3d(52px, 70px, -40px) rotateZ(-1.5deg)',
        );
    });

    test('el paralaje del cursor es independiente de lo abierta que esté', () => {
        const xy = (transform: string) =>
            /translate3d\((-?[\d.]+)px, (-?[\d.]+)px/
                .exec(transform)!
                .slice(1)
                .map(Number);
        const offset = (open: number) => {
            const [restX, restY] = xy(sheetTransform('vacancy', open));
            const [movedX, movedY] = xy(sheetTransform('vacancy', open, 1, 1));

            return [movedX - restX, movedY - restY];
        };

        expect(offset(0)).toEqual(offset(1));
        expect(offset(0.5)).toEqual(offset(1));
        expect(offset(1)).toEqual([-18, -18]);
    });
});
