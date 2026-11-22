import { describe, expect, test } from 'vitest';
import { latestIntersecting, someIntersecting } from './intersection';

/**
 * DEF-19. Un aviso de IntersectionObserver trae todas las entradas acumuladas
 * desde el anterior, en orden. Si la página se desplaza justo después de
 * observar, el aviso inicial («fuera») y el siguiente («dentro») pueden llegar
 * juntos: leer solo la primera deja el bloque oculto para siempre.
 */
const entries = (...states: boolean[]) =>
    states.map((isIntersecting) => ({ isIntersecting }));

describe('Lotes de entradas de IntersectionObserver', () => {
    test('«alguna a la vista» no se pierde la entrada que llega en segundo lugar', () => {
        expect(someIntersecting(entries(false, true))).toBe(true);
        expect(someIntersecting(entries(true, false))).toBe(true);
        expect(someIntersecting(entries(false, false))).toBe(false);
        expect(someIntersecting(entries())).toBe(false);
    });

    test('«el estado más reciente» es el de la última entrada', () => {
        expect(latestIntersecting(entries(false, true))).toBe(true);
        expect(latestIntersecting(entries(true, false))).toBe(false);
        expect(latestIntersecting(entries())).toBeNull();
    });
});
