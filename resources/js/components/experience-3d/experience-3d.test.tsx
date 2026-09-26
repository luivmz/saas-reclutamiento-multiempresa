import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import { RecruitmentDepth } from './recruitment-depth';
import {
    RecruitmentScenePoster,
    STAGE_SHEETS,
} from './recruitment-scene-poster';
import {
    detectSceneCapability,
    REDUCED_MOTION_QUERY,
    WIDE_VIEWPORT_QUERY,
} from './use-scene-capability';

/**
 * La capa de profundidad de la portada (ADR-003) es un adorno que puede no
 * cargar. Estas pruebas fijan cuándo no carga y qué garantiza cuando no lo
 * hace. No se prueba nada del navegador que no se pueda simular: el montaje
 * diferido, el fallo del fragmento y la escena real se prueban en `e2e-18`.
 */
type Options = {
    reduced?: boolean;
    wide?: boolean;
    saveData?: boolean;
    cores?: number;
    memory?: number;
    preserve3d?: boolean;
};

function fakeWindow({
    reduced = false,
    wide = true,
    saveData = false,
    cores = 8,
    memory,
    preserve3d = true,
}: Options = {}) {
    return {
        matchMedia: (query: string) =>
            ({
                matches:
                    query === REDUCED_MOTION_QUERY
                        ? reduced
                        : query === WIDE_VIEWPORT_QUERY
                          ? wide
                          : false,
            }) as MediaQueryList,
        navigator: {
            hardwareConcurrency: cores,
            deviceMemory: memory,
            connection: { saveData },
        },
        CSS: {
            supports: (property: string, value: string) =>
                preserve3d &&
                property === 'transform-style' &&
                value === 'preserve-3d',
        },
    };
}

describe('Cuándo la escena cede su sitio al póster', () => {
    test('con todo a favor, escena', () => {
        expect(detectSceneCapability(fakeWindow())).toEqual({ mode: 'scene' });
    });

    test('sin ventana —antes de montar—, póster', () => {
        expect(detectSceneCapability(undefined)).toEqual({
            mode: 'poster',
            reason: 'server',
        });
    });

    test('movimiento reducido: póster, y no hay nada que lo anule', () => {
        // Aunque el resto del equipo pueda con todo, lo que la persona pidió
        // manda. No se reduce la velocidad: se quita la escena.
        expect(detectSceneCapability(fakeWindow({ reduced: true }))).toEqual({
            mode: 'poster',
            reason: 'reduced-motion',
        });
    });

    test('ahorro de datos: póster, y el fragmento no se descarga', () => {
        expect(detectSceneCapability(fakeWindow({ saveData: true }))).toEqual({
            mode: 'poster',
            reason: 'save-data',
        });
    });

    test('pantalla angosta: póster, para no competir con el contenido', () => {
        expect(detectSceneCapability(fakeWindow({ wide: false }))).toEqual({
            mode: 'poster',
            reason: 'small-viewport',
        });
    });

    test('equipo modesto, por núcleos o por memoria: póster', () => {
        expect(detectSceneCapability(fakeWindow({ cores: 2 })).reason).toBe(
            'low-end',
        );
        expect(detectSceneCapability(fakeWindow({ memory: 2 })).reason).toBe(
            'low-end',
        );
    });

    test('sin composición en perspectiva: póster', () => {
        expect(
            detectSceneCapability(fakeWindow({ preserve3d: false })),
        ).toEqual({ mode: 'poster', reason: 'no-3d-support' });
    });

    test('la ausencia de WebGL no importa: la escena no lo usa', () => {
        // La ventana de prueba no tiene `WebGLRenderingContext` ni canvas: si
        // el detector lo consultara, esto daría póster.
        const win = fakeWindow();

        expect('WebGLRenderingContext' in win).toBe(false);
        expect(detectSceneCapability(win).mode).toBe('scene');
    });
});

describe('Lo que la capa garantiza a cualquiera', () => {
    test('lo primero que se pinta es el póster, nunca la escena', () => {
        const markup = renderToStaticMarkup(<RecruitmentDepth />);

        expect(markup).toContain('data-cy="recruitment-poster"');
        expect(markup).not.toContain('data-cy="recruitment-scene"');
    });

    test('es decorativa: oculta a la tecnología asistiva, inerte y sin eventos', () => {
        const markup = renderToStaticMarkup(<RecruitmentDepth />);
        const capa =
            markup.match(/<div[^>]*data-cy="recruitment-depth"[^>]*>/)?.[0] ??
            '';

        expect(capa).toContain('aria-hidden="true"');
        expect(capa).toContain('inert');
        expect(capa).toContain('pointer-events-none');
    });

    test('no tiene nada que pueda recibir el foco ni un lienzo WebGL', () => {
        const markup = renderToStaticMarkup(<RecruitmentDepth />);

        expect(markup).not.toMatch(
            /<(a|button|input|select|textarea|canvas)\b/,
        );
        expect(markup).not.toContain('tabindex');
    });

    test('ocupa la caja de la tarjeta: cambiar póster por escena no mueve la página', () => {
        const markup = renderToStaticMarkup(<RecruitmentDepth />);
        const capa =
            markup.match(/<div[^>]*data-cy="recruitment-depth"[^>]*>/)?.[0] ??
            '';

        // Absoluta dentro de la caja de la tarjeta: no aporta altura ni ancho
        // al flujo, así que el cambio no produce desplazamiento de diseño.
        expect(capa).toContain('absolute inset-0');
    });

    test('el póster no contiene información que solo esté ahí', () => {
        const markup = renderToStaticMarkup(<RecruitmentScenePoster />);
        const texto = markup.replace(/<[^>]+>/g, '').trim();

        // Ni etapas, ni nombres, ni cifras: todo lo que la portada dice está
        // en el expediente de al lado.
        expect(texto).toBe('');
        expect(markup.match(/rounded-xl border/g)).toHaveLength(
            STAGE_SHEETS.length,
        );
    });
});
