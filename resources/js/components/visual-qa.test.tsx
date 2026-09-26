import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import InputError from '@/components/input-error';
import { SkipLink } from '@/components/skip-link';
import TwoFactorRecoveryCodes from '@/components/two-factor-recovery-codes';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import AuthSimpleLayout from '@/layouts/auth/auth-simple-layout';
import { preferredScrollBehavior } from '@/lib/motion';

/**
 * Los defectos que encontró la Fase 21, fijados para que no vuelvan.
 *
 * Cada prueba corresponde a un hallazgo de `docs/v1.1/phase-21-visual-qa.md`.
 * El contraste real se mide en el navegador (`cypress/e2e/e2e-19-*`); aquí se
 * fija la decisión que lo produce: qué token lleva cada texto.
 */
describe('Fase 21 · correcciones de QA visual y accesibilidad', () => {
    test('la alerta destructiva escribe con el tono de peligro, no con el color que va sobre el relleno', () => {
        const markup = renderToStaticMarkup(
            <Alert variant="destructive">
                <AlertTitle>Requerimiento rechazado</AlertTitle>
                <AlertDescription>Motivo ficticio</AlertDescription>
            </Alert>,
        );

        expect(markup).toContain('text-tone-danger-foreground');
        // `--destructive-foreground` es casi blanco desde la Fase 18: como
        // texto sobre la tarjeta clara quedaba a ~1:1 y el motivo no se leía.
        expect(markup).not.toContain('text-destructive-foreground');
        // El motivo del rechazo no se atenúa: a 80 % bajaba a 4.87:1.
        expect(markup).not.toMatch(/text-tone-danger-foreground\/\d+/);
    });

    test('el error de un campo usa el tono de peligro como texto', () => {
        const markup = renderToStaticMarkup(
            <InputError message="Campo obligatorio" />,
        );

        expect(markup).toContain('text-tone-danger-foreground');
        expect(markup).not.toMatch(/(^|\s|")text-destructive(\s|")/);
    });

    test('el enlace de salto conserva su relleno al recibir el foco', () => {
        const markup = renderToStaticMarkup(<SkipLink />);

        // `not-sr-only` pone `padding: 0` y, como variante, gana a un `px-4`
        // base: el relleno tiene que ir también como variante de foco.
        expect(markup).toContain('focus:not-sr-only');
        expect(markup).toContain('focus:px-4');
        expect(markup).toContain('focus:py-2');
    });

    test('las pantallas de acceso tienen un contenido principal', () => {
        const markup = renderToStaticMarkup(
            <AuthSimpleLayout title="Iniciar sesión" description="Acceso">
                <form />
            </AuthSimpleLayout>,
        );

        expect(markup.match(/<main[\s>]/g)).toHaveLength(1);
        expect(markup).toMatch(
            /<main[^>]*>[\s\S]*<form><\/form>[\s\S]*<\/main>/,
        );
    });

    test('los códigos plegados no dejan una franja visible', () => {
        const markup = renderToStaticMarkup(
            <TwoFactorRecoveryCodes
                recoveryCodesList={['codigo-ficticio-1']}
                fetchRecoveryCodes={() => Promise.resolve()}
                errors={[]}
            />,
        );

        // El relleno superior iba en el elemento de la fila `0fr`, que no se
        // recorta: el plegado dejaba 12 px de la lista a la vista.
        expect(markup).toMatch(
            /grid-rows-\[0fr\][^>]*>\s*<div class="min-h-0">\s*<div class="space-y-3 pt-3"/,
        );
        // Los botones pueden saltar de línea en la columna angosta.
        expect(markup).toContain('sm:flex-wrap');
    });

    test('con movimiento reducido el desplazamiento es inmediato', () => {
        const ventana = (reduce: boolean) => ({
            matchMedia: (query: string) =>
                ({
                    matches:
                        reduce && query === '(prefers-reduced-motion: reduce)',
                }) as MediaQueryList,
        });

        expect(preferredScrollBehavior(ventana(true))).toBe('auto');
        expect(preferredScrollBehavior(ventana(false))).toBe('smooth');
        // Sin `window` (render en servidor) no se pide animación.
        expect(preferredScrollBehavior(undefined)).toBe('auto');
    });
});
