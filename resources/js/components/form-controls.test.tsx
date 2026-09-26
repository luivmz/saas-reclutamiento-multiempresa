import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { FormField, NativeSelect } from '@/components/form-controls';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

/**
 * `FormField` es el único sitio donde se conecta la ayuda y el error con el
 * control. Si se equivoca, el error se ve pero no se oye, y eso no se nota
 * mirando la pantalla: hace falta comprobar los atributos.
 */
function describedBy(markup: string): string | null {
    return markup.match(/aria-describedby="([^"]*)"/)?.[1] ?? null;
}

function invalid(markup: string): string | null {
    return markup.match(/aria-invalid="([^"]*)"/)?.[1] ?? null;
}

describe('FormField y la descripción accesible del control', () => {
    test('A · conserva el aria-describedby que ya traía el control', () => {
        const markup = renderToStaticMarkup(
            <FormField label="Puesto" htmlFor="puesto">
                <Input id="puesto" aria-describedby="glosario" />
            </FormField>,
        );

        expect(describedBy(markup)).toBe('glosario');
    });

    test('B · añade la ayuda', () => {
        const markup = renderToStaticMarkup(
            <FormField label="Plazo" htmlFor="plazo" hint="Opcional.">
                <Input id="plazo" />
            </FormField>,
        );

        expect(describedBy(markup)).toBe('plazo-hint');
        expect(markup).toContain('id="plazo-hint"');
    });

    test('C · añade el error y marca el control como inválido', () => {
        const markup = renderToStaticMarkup(
            <FormField label="Plazas" htmlFor="plazas" error="Debe ser 1 o más">
                <Input id="plazas" />
            </FormField>,
        );

        expect(describedBy(markup)).toBe('plazas-error');
        expect(invalid(markup)).toBe('true');
        expect(markup).toContain('id="plazas-error"');
    });

    test('D · combina los tres sin duplicar ni perder el orden', () => {
        const markup = renderToStaticMarkup(
            <FormField
                label="Cierre"
                htmlFor="cierre"
                hint="Posterior a la apertura."
                error="Fecha inválida"
            >
                <Input id="cierre" aria-describedby="glosario cierre-hint" />
            </FormField>,
        );

        expect(describedBy(markup)).toBe('glosario cierre-hint cierre-error');
    });

    test('E · un error gana a un aria-invalid={false} del llamador', () => {
        const markup = renderToStaticMarkup(
            <FormField label="Correo" htmlFor="correo" error="Correo inválido">
                <Input id="correo" aria-invalid={false} />
            </FormField>,
        );

        expect(invalid(markup)).toBe('true');
    });

    test('E-bis · sin error se respeta el aria-invalid del llamador', () => {
        const markup = renderToStaticMarkup(
            <FormField label="Correo" htmlFor="correo">
                <Input id="correo" aria-invalid={false} />
            </FormField>,
        );

        expect(invalid(markup)).toBe('false');
    });

    test('F · funciona igual con select y con textarea', () => {
        const select = renderToStaticMarkup(
            <FormField
                label="Etapa"
                htmlFor="etapa"
                hint="Elija una."
                error="Obligatorio"
            >
                <NativeSelect id="etapa" options={[]} />
            </FormField>,
        );

        const textarea = renderToStaticMarkup(
            <FormField
                label="Justificación"
                htmlFor="justificacion"
                error="Obligatorio"
            >
                <Textarea id="justificacion" />
            </FormField>,
        );

        expect(describedBy(select)).toBe('etapa-hint etapa-error');
        expect(invalid(select)).toBe('true');
        expect(describedBy(textarea)).toBe('justificacion-error');
        expect(invalid(textarea)).toBe('true');
    });

    test('sin ayuda ni error no inventa una descripción', () => {
        const markup = renderToStaticMarkup(
            <FormField label="Ciudad" htmlFor="ciudad">
                <Input id="ciudad" />
            </FormField>,
        );

        expect(describedBy(markup)).toBeNull();
        expect(invalid(markup)).toBeNull();
    });
});
