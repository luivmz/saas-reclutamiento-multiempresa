export type ApplicationStep = 1 | 2 | 3 | 4;

/** Contrato entre la portada y el futuro adaptador del runtime de Spline. */
export type ApplicationScene = {
    setStep: (step: ApplicationStep) => void;
    setPlaying: (playing: boolean) => void;
    dispose: () => void;
};

export type LoadApplicationScene = (
    canvas: HTMLCanvasElement,
    signal: AbortSignal,
    onStepChange: (value: unknown) => void,
) => Promise<ApplicationScene>;

export type SceneStatus = 'loading' | 'ready' | 'error';

const LOAD_TIMEOUT_MS = 8_000;

/** Retiene la última selección incluso si cambia durante la carga. */
export function startApplicationScene(
    canvas: HTMLCanvasElement,
    load: LoadApplicationScene,
    onStatus: (status: SceneStatus) => void,
    onStepChange?: (step: ApplicationStep) => void,
) {
    const abort = new AbortController();
    let scene: ApplicationScene | undefined;
    let step: ApplicationStep = 1;
    let playing = false;

    const dispose = () => {
        abort.abort();
        clearTimeout(timeout);
        canvas.removeEventListener('webglcontextlost', fail);
        scene?.dispose();
        scene = undefined;
    };

    const fail = () => {
        if (!abort.signal.aborted) {
            dispose();
            onStatus('error');
        }
    };

    const timeout = setTimeout(fail, LOAD_TIMEOUT_MS);
    canvas.addEventListener('webglcontextlost', fail);
    onStatus('loading');

    void (async () => {
        try {
            const loaded = await load(canvas, abort.signal, (value) => {
                if (
                    !scene ||
                    !playing ||
                    abort.signal.aborted ||
                    value === step
                ) {
                    return;
                }
                if (value === 1 || value === 2 || value === 3 || value === 4) {
                    step = value;
                    onStepChange?.(value);
                }
            });
            if (abort.signal.aborted) {
                loaded.dispose();
                return;
            }

            scene = loaded;
            clearTimeout(timeout);
            scene.setStep(step);
            scene.setPlaying(playing);
            onStatus('ready');
        } catch {
            fail();
        }
    })();

    return {
        setStep(next: ApplicationStep) {
            if (next === step) {
                return;
            }
            step = next;
            try {
                scene?.setStep(step);
            } catch {
                fail();
            }
        },
        setPlaying(next: boolean) {
            playing = next;
            try {
                scene?.setPlaying(playing);
            } catch {
                fail();
            }
        },
        dispose,
    };
}
