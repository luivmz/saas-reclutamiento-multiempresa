import { afterEach, describe, expect, test, vi } from 'vitest';
import { OperationalRiskCard } from './operational-risk-card';

// Prueba unitaria del efecto asíncrono, sin navegador ni peticiones reales.
const state = vi.hoisted(() => ({
    effect: undefined as undefined | (() => void | (() => void)),
    setRisk: vi.fn(),
    setFailed: vi.fn(),
}));

vi.mock('react', async (importOriginal) => ({
    ...(await importOriginal<typeof import('react')>()),
    useEffect: (effect: () => void | (() => void)) => {
        state.effect = effect;
    },
    useState: (initial: unknown) => [
        initial,
        initial === null ? state.setRisk : state.setFailed,
    ],
}));

afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    state.setRisk.mockClear();
    state.setFailed.mockClear();
    state.effect = undefined;
});

describe('RF-29 experimental: degradación del indicador operacional', () => {
    test('un HTTP fallido rechaza con Error y conserva el estado de degradación', async () => {
        const request = vi.fn().mockResolvedValue({ ok: false, status: 503 });
        vi.stubGlobal('fetch', request);
        const reject = vi.spyOn(Promise, 'reject');

        OperationalRiskCard({ vacancyId: 7 });
        state.effect?.();

        await vi.waitFor(() =>
            expect(state.setFailed).toHaveBeenCalledWith(true),
        );
        expect(reject).toHaveBeenCalledWith(expect.any(Error));
        expect(state.setRisk).not.toHaveBeenCalled();
        expect(request).toHaveBeenCalledWith('/vacantes/7/riesgo-operacional', {
            headers: { Accept: 'application/json' },
        });
    });

    test('una respuesta correcta conserva el payload sin convertirlo en decisión', async () => {
        const risk = { availability: 'descriptive_only' };
        vi.stubGlobal(
            'fetch',
            vi.fn().mockResolvedValue({
                ok: true,
                json: () => Promise.resolve({ risk }),
            }),
        );

        OperationalRiskCard({ vacancyId: 7 });
        state.effect?.();

        await vi.waitFor(() =>
            expect(state.setRisk).toHaveBeenCalledWith(risk),
        );
        expect(state.setFailed).not.toHaveBeenCalled();
    });

    test('no actualiza estado después de cancelar el efecto', async () => {
        vi.stubGlobal(
            'fetch',
            vi.fn().mockResolvedValue({ ok: false, status: 503 }),
        );

        OperationalRiskCard({ vacancyId: 7 });
        const cleanup = state.effect?.();
        if (typeof cleanup === 'function') cleanup();
        // Deja completar la cadena de microtareas del fetch simulado.
        await new Promise((resolve) => setTimeout(resolve, 0));

        expect(state.setFailed).not.toHaveBeenCalled();
        expect(state.setRisk).not.toHaveBeenCalled();
    });
});
