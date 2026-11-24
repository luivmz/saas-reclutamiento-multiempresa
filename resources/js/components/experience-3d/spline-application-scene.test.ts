import {
    afterEach,
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from 'vite-plus/test';

const runtime = vi.hoisted(() => {
    type Listener = (event: { target?: { name?: string } }) => void;

    class FakeApplication {
        static instances: FakeApplication[] = [];
        static nextLoad: () => Promise<void> = async () => {};
        static drawsOnRequest = true;

        canvas: EventTarget;
        options: Record<string, unknown>;
        variables: Record<string, number> = { applicationStep: 1 };
        listeners = new Map<string, Listener>();
        load = vi.fn(() => FakeApplication.nextLoad());
        setBackgroundColor = vi.fn();
        play = vi.fn();
        stop = vi.fn();
        dispose = vi.fn();
        requestRender = vi.fn(() => {
            if (FakeApplication.drawsOnRequest) {
                this.canvas.dispatchEvent(new Event('rendered'));
            }
        });
        setVariable = vi.fn((name: string, value: number) => {
            this.variables[name] = value;
        });
        getVariable = vi.fn((name: string) => this.variables[name]);
        addEventListener = vi.fn((name: string, listener: Listener) => {
            this.listeners.set(name, listener);
        });
        removeEventListener = vi.fn((name: string) => {
            this.listeners.delete(name);
        });

        constructor(canvas: EventTarget, options: Record<string, unknown>) {
            this.canvas = canvas;
            this.options = options;
            FakeApplication.instances.push(this);
        }

        click(name: string) {
            this.listeners.get('mouseDown')?.({ target: { name } });
        }
    }

    return { FakeApplication };
});

vi.mock('@splinetool/runtime', () => ({
    Application: runtime.FakeApplication,
}));

const { APPLICATION_SCENE_URL, loadSplineApplicationScene } =
    await import('./spline-application-scene');
const { FakeApplication } = runtime;

function canvas() {
    return new EventTarget() as HTMLCanvasElement;
}

beforeEach(() => {
    FakeApplication.instances = [];
    FakeApplication.nextLoad = async () => {};
    FakeApplication.drawsOnRequest = true;
    vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => {
        callback(0);
        return 1;
    });
    vi.stubGlobal('cancelAnimationFrame', () => {});
});

afterEach(() => vi.unstubAllGlobals());

describe('Adaptador de Spline para «Cómo postular»', () => {
    it('carga el export propio con WebGL y fondo transparente, y resuelve tras el primer cuadro', async () => {
        FakeApplication.drawsOnRequest = false;
        const target = canvas();
        const signal = new AbortController().signal;
        let resolved = false;
        const pending = loadSplineApplicationScene(
            target,
            signal,
            vi.fn(),
        ).then((scene) => {
            resolved = true;
            return scene;
        });
        await vi.waitFor(() =>
            expect(
                FakeApplication.instances[0]?.requestRender,
            ).toHaveBeenCalled(),
        );
        const app = FakeApplication.instances[0];

        expect(app.options).toMatchObject({
            renderer: 'webgl',
            htmlContentMode: 'none',
            renderMode: 'auto',
        });
        expect(app.load).toHaveBeenCalledWith(
            APPLICATION_SCENE_URL,
            { applicationStep: 1 },
            { signal },
        );
        expect(APPLICATION_SCENE_URL).toBe(
            '/spline/proceso-postulacion-eaa9e57f.splinecode',
        );
        expect(app.setBackgroundColor).toHaveBeenCalledWith('transparent');
        await Promise.resolve();
        expect(resolved).toBe(false);

        target.dispatchEvent(new Event('rendered'));
        await pending;
        expect(resolved).toBe(true);
    });

    it('traduce el paso a applicationStep y la reproducción a play y stop', async () => {
        const scene = await loadSplineApplicationScene(
            canvas(),
            new AbortController().signal,
            vi.fn(),
        );
        const app = FakeApplication.instances[0];

        scene.setStep(3);
        scene.setPlaying(true);
        scene.setPlaying(false);

        expect(app.setVariable).toHaveBeenCalledWith('applicationStep', 3);
        expect(app.play).toHaveBeenCalledTimes(1);
        expect(app.stop).toHaveBeenCalledTimes(1);
    });

    it('notifica el valor de la variable solo tras pulsar una flecha', async () => {
        const onStep = vi.fn();
        await loadSplineApplicationScene(
            canvas(),
            new AbortController().signal,
            onStep,
        );
        const app = FakeApplication.instances[0];

        app.variables.applicationStep = 2;
        app.click('Siguiente');
        app.click('Tarjeta 1');
        app.variables.applicationStep = 1;
        app.click('Anterior');

        expect(onStep.mock.calls).toEqual([[2], [1]]);
    });

    it('libera el runtime y no notifica tras desmontar', async () => {
        const onStep = vi.fn();
        const scene = await loadSplineApplicationScene(
            canvas(),
            new AbortController().signal,
            onStep,
        );
        const app = FakeApplication.instances[0];

        scene.dispose();
        scene.dispose();
        app.click('Siguiente');

        expect(app.dispose).toHaveBeenCalledTimes(1);
        expect(app.removeEventListener).toHaveBeenCalledWith(
            'mouseDown',
            expect.any(Function),
        );
        expect(onStep).not.toHaveBeenCalled();
    });

    it('libera el runtime y rechaza si se aborta durante la carga', async () => {
        let finish!: () => void;
        FakeApplication.nextLoad = () =>
            new Promise<void>((resolve) => {
                finish = resolve;
            });
        const abort = new AbortController();
        const pending = loadSplineApplicationScene(
            canvas(),
            abort.signal,
            vi.fn(),
        );
        await vi.waitFor(() =>
            expect(FakeApplication.instances[0]?.load).toHaveBeenCalled(),
        );

        abort.abort();
        finish();

        await expect(pending).rejects.toMatchObject({ name: 'AbortError' });
        expect(FakeApplication.instances[0].dispose).toHaveBeenCalledTimes(1);
    });

    it('libera el runtime y propaga el error si el export no se puede decodificar', async () => {
        FakeApplication.nextLoad = async () => {
            throw new Error('archivo dañado');
        };

        await expect(
            loadSplineApplicationScene(
                canvas(),
                new AbortController().signal,
                vi.fn(),
            ),
        ).rejects.toThrow('archivo dañado');
        expect(FakeApplication.instances[0].dispose).toHaveBeenCalledTimes(1);
    });

    it('no crea el runtime si la carga ya estaba cancelada', async () => {
        const abort = new AbortController();
        abort.abort();

        await expect(
            loadSplineApplicationScene(canvas(), abort.signal, vi.fn()),
        ).rejects.toMatchObject({ name: 'AbortError' });
        expect(FakeApplication.instances).toHaveLength(0);
    });
});
