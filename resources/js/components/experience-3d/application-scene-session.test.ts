import { afterEach, describe, expect, it, vi } from 'vite-plus/test';
import {
    startApplicationScene,
    type ApplicationScene,
} from './application-scene-session';

function fixture() {
    const canvas = new EventTarget() as HTMLCanvasElement;
    const status = vi.fn();
    const scene = { setStep: vi.fn(), setPlaying: vi.fn(), dispose: vi.fn() };
    return { canvas, status, scene };
}

afterEach(() => vi.useRealTimers());

describe('Sesión del futuro adaptador de escena de postulación', () => {
    it('acepta flechas visibles, evita el eco y descarta eventos de una sesión vencida', async () => {
        const { canvas, status, scene } = fixture();
        const onStep = vi.fn();
        let notify!: (value: unknown) => void;
        const session = startApplicationScene(
            canvas,
            async (_canvas, _signal, changed) => {
                notify = changed;
                notify(2);
                return scene;
            },
            status,
            onStep,
        );
        await Promise.resolve();
        notify(2);
        session.setPlaying(true);
        notify(3);
        session.setStep(3);
        notify(3);
        notify(5);
        notify('2');
        session.setStep(4);
        notify(4);
        session.dispose();
        notify(2);
        expect(onStep.mock.calls).toEqual([[3]]);
        expect(scene.setStep.mock.calls).toEqual([[1], [4]]);
    });

    it('aplica la última selección disponible tras cargar y pausa al salir', async () => {
        const { canvas, status, scene } = fixture();
        const load = vi.fn(async () => scene);
        const session = startApplicationScene(canvas, load, status);

        session.setStep(2);
        session.setStep(4);
        expect(status).toHaveBeenLastCalledWith('loading');
        await Promise.resolve();

        expect(scene.setStep.mock.calls).toEqual([[4]]);
        expect(scene.setPlaying).toHaveBeenLastCalledWith(false);
        expect(status).toHaveBeenLastCalledWith('ready');
        session.setPlaying(true);
        session.setStep(3);
        session.setPlaying(false);
        expect(scene.setPlaying.mock.calls).toEqual([[false], [true], [false]]);
        expect(scene.setStep).toHaveBeenLastCalledWith(3);
        session.dispose();
        expect(scene.dispose).toHaveBeenCalledOnce();
    });

    it('informa del error de descarga sin dejar una sesión activa', async () => {
        const { canvas, status } = fixture();
        const load = vi.fn(async () => {
            throw new Error('Recurso no disponible');
        });
        startApplicationScene(canvas, load, status);
        await Promise.resolve();

        expect(status.mock.calls).toEqual([['loading'], ['error']]);
        expect(load.mock.calls).toHaveLength(1);
    });

    it('agota la espera y libera un resultado que llegó después', async () => {
        vi.useFakeTimers();
        const { canvas, status, scene } = fixture();
        let finish!: (loaded: ApplicationScene) => void;
        const load = vi.fn(
            () =>
                new Promise<ApplicationScene>((resolve) => {
                    finish = resolve;
                }),
        );
        startApplicationScene(canvas, load, status);
        await vi.advanceTimersByTimeAsync(8_000);
        expect(status).toHaveBeenLastCalledWith('error');
        finish(scene);
        await Promise.resolve();

        expect(scene.dispose).toHaveBeenCalledOnce();
        expect(scene.setStep).not.toHaveBeenCalled();
        expect(status).not.toHaveBeenCalledWith('ready');
    });

    it('libera el recurso al desmontar durante la carga sin anunciar error', async () => {
        const { canvas, status, scene } = fixture();
        const load = vi.fn(
            async (_canvas: HTMLCanvasElement, _signal: AbortSignal) => scene,
        );
        const session = startApplicationScene(canvas, load, status);
        session.dispose();
        await Promise.resolve();

        expect(load.mock.calls[0][1].aborted).toBe(true);
        expect(scene.dispose).toHaveBeenCalledOnce();
        expect(status.mock.calls).toEqual([['loading']]);
    });

    it('libera la sesión y conserva el respaldo al perder el contexto gráfico', async () => {
        const { canvas, status, scene } = fixture();
        startApplicationScene(canvas, async () => scene, status);
        await Promise.resolve();
        canvas.dispatchEvent(new Event('webglcontextlost'));

        expect(scene.dispose).toHaveBeenCalledOnce();
        expect(status.mock.calls).toEqual([['loading'], ['ready'], ['error']]);
    });
});
