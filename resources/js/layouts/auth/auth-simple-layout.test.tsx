import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import AuthSimpleLayout from '@/layouts/auth/auth-simple-layout';

/**
 * DEF-29: el panel de acceso y registro, que también ven los postulantes,
 * mostraba «(RF-23)». El mensaje se mantiene; el código, no.
 */
describe('Acceso y registro · panel institucional', () => {
    test('explica la decisión humana sin mostrar códigos de requisito', () => {
        const markup = renderToStaticMarkup(
            <AuthSimpleLayout title="Cree su cuenta" description="Registro">
                <form />
            </AuthSimpleLayout>,
        );

        expect(markup).toContain(
            'seleccionar es un acto humano con justificación',
        );
        expect(markup).not.toMatch(/RF-\d+/);
    });
});
