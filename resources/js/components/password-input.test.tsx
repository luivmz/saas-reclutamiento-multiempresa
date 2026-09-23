import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import PasswordInput from '@/components/password-input';

/**
 * El conmutador de visibilidad venía del kit de inicio con `tabIndex={-1}`:
 * quien navega con teclado no podía comprobar lo que había escrito.
 */
describe('PasswordInput y el conmutador de visibilidad', () => {
    test('el botón está en el orden de tabulación', () => {
        const markup = renderToStaticMarkup(<PasswordInput id="password" />);
        const button = markup.match(/<button[^>]*>/)?.[0] ?? '';

        expect(button).not.toContain('tabindex="-1"');
        expect(button).toContain('type="button"');
    });

    test('tiene nombre accesible y dice qué campo controla', () => {
        const markup = renderToStaticMarkup(<PasswordInput id="password" />);

        expect(markup).toContain('aria-label="Mostrar la contraseña"');
        expect(markup).toContain('aria-controls="password"');
    });

    test('el campo nace oculto y el icono es decorativo', () => {
        const markup = renderToStaticMarkup(<PasswordInput id="password" />);

        expect(markup).toContain('type="password"');
        expect(markup).toContain('aria-hidden="true"');
    });
});
