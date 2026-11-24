import { describe, expect, test } from 'vitest';
import { navigationFor } from '@/lib/navigation';

/**
 * DEF-29: los textos dirigidos al postulante mostraban códigos de requisito
 * («RF-09», «RF-11, RF-15»). Se retiran de la pantalla y la trazabilidad queda
 * en el atributo `rf` de cada entrada (y en la documentación y las pruebas).
 */
describe('Navegación · textos para el postulante', () => {
    const postulante = navigationFor('postulante').flatMap(
        (group) => group.items,
    );

    test('ninguna descripción del postulante muestra códigos RF', () => {
        for (const item of postulante) {
            expect(item.description ?? '').not.toMatch(/RF-\d+/);
        }
    });

    test('la trazabilidad de cada entrada se conserva fuera del texto', () => {
        expect(
            postulante.find((item) => item.cy === 'candidate-profile')?.rf,
        ).toEqual(['RF-09']);
        expect(
            postulante.find((item) => item.cy === 'my-applications')?.rf,
        ).toEqual(['RF-11', 'RF-15']);
    });

    test('las pantallas del personal conservan sus códigos', () => {
        const rrhh = navigationFor('rrhh').flatMap((group) => group.items);

        expect(
            rrhh.find((item) => item.cy === 'job-requests')?.description,
        ).toContain('RF-02');
    });
});
