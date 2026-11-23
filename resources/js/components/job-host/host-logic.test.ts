import { describe, expect, test } from 'vitest';
import {
    canReact,
    CLIP_FPS,
    cyclicDelta,
    nearestGoal,
    nearestToCenter,
    POINT_FRAMES,
    stepToward,
    tiltFor,
    timeForFrame,
    ZONE_FRAMES,
    zoneFor,
} from './host-logic';

/**
 * El anfitrión de /empleos, sin navegador: zonas, recorrido por el clip de
 * señalar, frecuencia de reacciones, oferta más cercana al centro e
 * inclinación. El comportamiento real se prueba en `e2e-24`.
 */
describe('Zona de la oferta respecto del anfitrión', () => {
    // Personaje de 260 px con su parte superior en 300: la mano está a 378.
    test('arriba, a media altura o abajo, comparada con la altura de la mano', () => {
        expect(zoneFor(250, 300, 260)).toBe('up');
        expect(zoneFor(380, 300, 260)).toBe('mid');
        expect(zoneFor(480, 300, 260)).toBe('mid');
        expect(zoneFor(520, 300, 260)).toBe('down');
        expect(zoneFor(380, 300, 0)).toBe('mid');
    });
});

describe('Recorrido por el clip de señalar', () => {
    test('el ciclo une el último fotograma con el primero', () => {
        expect(cyclicDelta(0, 27)).toBe(27);
        expect(cyclicDelta(90, 0)).toBe(6);
        expect(cyclicDelta(0, 60)).toBe(-36);
        expect(cyclicDelta(60, 60)).toBe(0);
    });

    test('elige el fotograma de la zona más cercano: a media altura hay dos', () => {
        expect(nearestGoal(30, ZONE_FRAMES.mid)).toBe(48);
        expect(nearestGoal(70, ZONE_FRAMES.mid)).toBe(78);
        expect(nearestGoal(5, ZONE_FRAMES.mid)).toBe(78);
    });

    test('avanza o retrocede un fotograma por paso y se detiene en la meta', () => {
        expect(stepToward(0, 27)).toBe(1);
        expect(stepToward(60, 48)).toBe(59);
        expect(stepToward(0, 60)).toBe(95);
        expect(stepToward(95, 0)).toBe(0);
        expect(stepToward(27, 27)).toBe(27);

        let frame = 0;
        let steps = 0;

        while (frame !== 60 && steps < 200) {
            frame = stepToward(frame, 60);
            steps++;
        }

        // Del reposo a «abajo» por el camino corto: hacia atrás desde el final (rest → 78 → 60).
        expect(steps).toBe(36);
    });

    test('cada fotograma cae en su propio intervalo de tiempo', () => {
        for (let frame = 0; frame < POINT_FRAMES - 1; frame++) {
            const time = timeForFrame(frame);

            expect(time).toBeGreaterThan(frame / CLIP_FPS);
            expect(time).toBeLessThan((frame + 1) / CLIP_FPS);
        }
    });
});

describe('Frecuencia de la reacción de interés', () => {
    test('una vez y después, solo pasado el intervalo', () => {
        expect(canReact(1000, null, 8000)).toBe(true);
        expect(canReact(5000, 1000, 8000)).toBe(false);
        expect(canReact(9000, 1000, 8000)).toBe(true);
    });
});

describe('Oferta más cercana al centro durante el desplazamiento', () => {
    test('ignora las que están fuera de la ventana', () => {
        const rects = [
            { top: -300, bottom: -10 },
            { top: 100, bottom: 360 },
            { top: 380, bottom: 640 },
            { top: 900, bottom: 1160 },
        ];

        expect(nearestToCenter(rects, 800)).toBe(2);
        expect(nearestToCenter(rects.slice(0, 1), 800)).toBe(-1);
    });
});

describe('Inclinación hacia el cursor', () => {
    test('pequeña, en el sentido del cursor y acotada', () => {
        const host = { left: 1000, top: 300, width: 132, height: 260 };

        expect(tiltFor(1066, 430, host)).toEqual({ rotateX: 0, rotateY: 0 });
        expect(tiltFor(466, 430, host).rotateY).toBeLessThan(0);
        expect(tiltFor(-5000, -5000, host)).toEqual({
            rotateX: 4,
            rotateY: -7,
        });
    });
});
