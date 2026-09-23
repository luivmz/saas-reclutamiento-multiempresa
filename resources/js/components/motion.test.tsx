import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { DataTable } from '@/components/data-table';
import InputError from '@/components/input-error';
import TwoFactorRecoveryCodes from '@/components/two-factor-recovery-codes';
import { Button } from '@/components/ui/button';

/**
 * Las decisiones de movimiento de la Fase 19, escritas como prueba.
 *
 * No se mide ninguna duración exacta: lo que se fija son las decisiones que
 * costaría recuperar si alguien las deshiciera sin darse cuenta —qué se mueve,
 * qué no debe moverse nunca, y con qué propiedades—.
 */
describe('Las decisiones de movimiento', () => {
    test('el botón responde a la pulsación y anima solo propiedades baratas', () => {
        const markup = renderToStaticMarkup(<Button>Guardar</Button>);

        expect(markup).toContain('active:scale-[0.98]');
        expect(markup).toContain('transition-[color,box-shadow,transform]');
        // `transition-all` animaría cualquier propiedad que cambie, incluidas
        // las que obligan a recalcular el diseño.
        expect(markup).not.toContain('transition-all');
    });

    test('un botón deshabilitado no cede al pulsarlo', () => {
        const markup = renderToStaticMarkup(<Button disabled>Guardar</Button>);

        expect(markup).toContain('disabled:active:scale-100');
    });

    test('el error de un campo entra atenuándose, nunca sacudiéndose', () => {
        const markup = renderToStaticMarkup(
            <InputError message="Debe indicar un motivo" />,
        );

        expect(markup).toContain('animate-in');
        expect(markup).toContain('fade-in-0');
        // Un formulario que tiembla castiga a quien se equivocó.
        expect(markup).not.toMatch(/shake|animate-bounce|animate-pulse/);
        // El anuncio no depende de la animación.
        expect(markup).toContain('role="alert"');
    });

    test('las filas de la tabla no entran animadas: los datos no se mueven', () => {
        const markup = renderToStaticMarkup(
            <DataTable<{ id: number; code: string }>
                caption="Vacantes"
                rows={[
                    { id: 1, code: 'VAC-001' },
                    { id: 2, code: 'VAC-002' },
                ]}
                rowKey={(row) => row.id}
                columns={[
                    { key: 'code', header: 'Código', cell: (row) => row.code },
                ]}
            />,
        );

        expect(markup).not.toContain('animate-in');
        expect(markup).not.toContain('slide-in');
        // El único movimiento admitido en una fila es el resalte al pasar el
        // puntero, y solo en escritorio.
        expect(markup).toContain('md:hover:bg-surface/60');
        expect(markup).toContain('md:transition-colors');
    });

    test('los códigos de recuperación se pliegan con una altura que sí anima', () => {
        const markup = renderToStaticMarkup(
            <TwoFactorRecoveryCodes
                recoveryCodesList={[]}
                fetchRecoveryCodes={() => Promise.resolve()}
                errors={[]}
            />,
        );

        // `height: auto` no es interpolable: la transición anterior no animaba
        // nada y la altura saltaba de golpe.
        expect(markup).toContain('grid-rows-[0fr]');
        expect(markup).toContain('transition-[grid-template-rows,opacity]');
        expect(markup).not.toContain('transition-all');
    });
});
