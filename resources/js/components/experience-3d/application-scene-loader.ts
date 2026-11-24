import type { LoadApplicationScene } from './application-scene-session';

/**
 * Cargador estable que la portada entrega a «Cómo postular». El adaptador y el
 * runtime de Spline se descargan solo cuando la escena va a mostrarse; la
 * página no los incluye en su fragmento.
 */
export const loadApplicationScene: LoadApplicationScene = async (
    canvas,
    signal,
    onStepChange,
) => {
    const { loadSplineApplicationScene } =
        await import('./spline-application-scene');
    return loadSplineApplicationScene(canvas, signal, onStepChange);
};
