import { useEffect, useState } from 'react';

/**
 * Decide si la escena en profundidad de la portada puede mostrarse o si queda
 * el póster estático.
 *
 * El 3D es un adorno que puede no cargar, y este es el único sitio donde se
 * decide. El orden de las comprobaciones es deliberado: primero lo que la
 * persona pidió —movimiento reducido, ahorro de datos—, después lo que el
 * dispositivo puede sostener. En cualquier duda, póster: nunca se paga el
 * 3D a costa de quien no lo quiere o no lo puede mover.
 *
 * La escena no usa WebGL —es CSS 3D sobre capas de DOM—, así que un navegador
 * sin WebGL la muestra igual. Lo que sí se comprueba es que el navegador sepa
 * componer en perspectiva.
 */
export type SceneMode = 'poster' | 'scene';

export type PosterReason =
    | 'server'
    | 'reduced-motion'
    | 'save-data'
    | 'small-viewport'
    | 'low-end'
    | 'no-3d-support';

export type SceneCapability = { mode: SceneMode; reason?: PosterReason };

/** Por debajo de este ancho la portada va a una columna y el 3D competiría con el contenido. */
export const SCENE_MIN_WIDTH = 1024;

export const REDUCED_MOTION_QUERY = '(prefers-reduced-motion: reduce)';
export const WIDE_VIEWPORT_QUERY = `(min-width: ${SCENE_MIN_WIDTH}px)`;

type CapabilityWindow = Pick<Window, 'matchMedia'> & {
    navigator: Pick<Navigator, 'hardwareConcurrency'> & {
        deviceMemory?: number;
        connection?: { saveData?: boolean };
    };
    CSS?: { supports?: (property: string, value: string) => boolean };
};

export function detectSceneCapability(
    win: CapabilityWindow | undefined,
): SceneCapability {
    if (!win) {
        return { mode: 'poster', reason: 'server' };
    }

    if (win.matchMedia(REDUCED_MOTION_QUERY).matches) {
        return { mode: 'poster', reason: 'reduced-motion' };
    }

    if (win.navigator.connection?.saveData) {
        return { mode: 'poster', reason: 'save-data' };
    }

    if (!win.matchMedia(WIDE_VIEWPORT_QUERY).matches) {
        return { mode: 'poster', reason: 'small-viewport' };
    }

    const cores = win.navigator.hardwareConcurrency;
    const memory = win.navigator.deviceMemory;

    if (
        (cores !== undefined && cores <= 2) ||
        (memory !== undefined && memory <= 2)
    ) {
        return { mode: 'poster', reason: 'low-end' };
    }

    if (!win.CSS?.supports?.('transform-style', 'preserve-3d')) {
        return { mode: 'poster', reason: 'no-3d-support' };
    }

    return { mode: 'scene' };
}

/**
 * Versión reactiva: empieza siempre en póster —lo que se ve al instante— y se
 * reevalúa si la persona cambia el movimiento reducido o el ancho de la
 * ventana mientras está en la página.
 */
export function useSceneCapability(): SceneCapability {
    const [capability, setCapability] = useState<SceneCapability>({
        mode: 'poster',
        reason: 'server',
    });

    useEffect(() => {
        const update = () => setCapability(detectSceneCapability(window));
        const queries = [REDUCED_MOTION_QUERY, WIDE_VIEWPORT_QUERY].map(
            (query) => window.matchMedia(query),
        );

        update();
        queries.forEach((query) => query.addEventListener('change', update));

        return () =>
            queries.forEach((query) =>
                query.removeEventListener('change', update),
            );
    }, []);

    return capability;
}
