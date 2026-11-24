import type {
    ApplicationScene,
    ApplicationStep,
    LoadApplicationScene,
} from './application-scene-session';

/**
 * Export del carrusel «Cómo postular» publicado desde Spline el 24/11/2026 y
 * servido desde el propio dominio. El nombre lleva el prefijo de su SHA-256
 * (eaa9e57f…): al sustituir el export cambia el archivo y su referencia.
 */
export const APPLICATION_SCENE_URL =
    '/spline/proceso-postulacion-eaa9e57f.splinecode';

/** Carpeta donde el build deja `bevel.wasm` (plugin `spline-runtime-wasm`). */
const RUNTIME_WASM_PATH = `${import.meta.env.BASE_URL}spline-runtime`;

const STEP_VARIABLE = 'applicationStep';
const ARROWS = new Set(['Siguiente', 'Anterior']);

type SplineRuntime = typeof import('@splinetool/runtime');

function aborted(): DOMException {
    return new DOMException('La carga de la escena se canceló.', 'AbortError');
}

/**
 * Adaptador real del contrato `LoadApplicationScene` para el runtime de Spline.
 *
 * - Dibuja en el canvas que entrega la portada, con WebGL y fondo transparente,
 *   para que se vea el fondo de la sección en ambos temas.
 * - Resuelve cuando el runtime confirma el primer cuadro dibujado.
 * - `setStep` asigna `applicationStep`; las flechas de la escena notifican el
 *   valor resultante, que la sesión valida antes de cambiar la selección HTML.
 * - Libera el runtime (y su contexto WebGL) al abortar o al desmontar.
 *
 * Elegir un paso solo cambia la ilustración: no registra postulaciones ni
 * ejecuta acciones de negocio.
 */
export const loadSplineApplicationScene: LoadApplicationScene = async (
    canvas,
    signal,
    onStepChange,
) => {
    if (signal.aborted) {
        throw aborted();
    }

    const runtime: SplineRuntime = await import('@splinetool/runtime');
    if (signal.aborted) {
        throw aborted();
    }

    const app = new runtime.Application(canvas, {
        renderMode: 'auto',
        renderer: 'webgl',
        htmlContentMode: 'none',
        wasmPath: import.meta.env.DEV ? undefined : RUNTIME_WASM_PATH,
    });

    let disposed = false;
    let frame = 0;

    const onMouseDown = (event: { target?: { name?: string } }) => {
        if (!ARROWS.has(event.target?.name ?? '')) {
            return;
        }
        // La acción SetVariable de la flecha termina en el mismo ciclo del
        // evento; se lee el valor en el cuadro siguiente.
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
            if (!disposed) {
                onStepChange(app.getVariable(STEP_VARIABLE));
            }
        });
    };

    const dispose = () => {
        if (disposed) {
            return;
        }
        disposed = true;
        cancelAnimationFrame(frame);
        signal.removeEventListener('abort', dispose);
        app.removeEventListener('mouseDown', onMouseDown);
        app.dispose();
    };

    signal.addEventListener('abort', dispose, { once: true });

    try {
        await app.load(
            APPLICATION_SCENE_URL,
            { [STEP_VARIABLE]: 1 },
            { signal },
        );
        if (signal.aborted) {
            throw aborted();
        }

        app.setBackgroundColor('transparent');
        app.addEventListener('mouseDown', onMouseDown);

        await new Promise<void>((resolve, reject) => {
            const rendered = () => {
                cleanup();
                resolve();
            };
            const cancel = () => {
                cleanup();
                reject(aborted());
            };
            const cleanup = () => {
                canvas.removeEventListener('rendered', rendered);
                signal.removeEventListener('abort', cancel);
            };
            canvas.addEventListener('rendered', rendered);
            signal.addEventListener('abort', cancel, { once: true });
            app.requestRender();
        });
    } catch (issue) {
        dispose();
        throw issue;
    }

    const scene: ApplicationScene = {
        setStep(step: ApplicationStep) {
            app.setVariable(STEP_VARIABLE, step);
        },
        setPlaying(playing: boolean) {
            if (playing) {
                app.play();
            } else {
                app.stop();
            }
        },
        dispose,
    };

    return scene;
};
