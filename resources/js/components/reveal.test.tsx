import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    folderOpenness,
    sheetTransform,
} from '@/components/experience-3d/recruitment-scene';
import { STAGE_SHEETS } from '@/components/experience-3d/recruitment-scene-poster';
import { Reveal, watchReveal, type RevealState } from '@/components/reveal';

/**
 * Incremento visual de la portada. Lo que no depende del navegador: el
 * contenido se ve antes de montar (y sin JavaScript), el movimiento reducido
 * nunca deja nada oculto (VIS-L01) y la carpeta del proceso se abre según el
 * desplazamiento. La apariencia real con la página montada se prueba en
 * `e2e-22` y `e2e-23`.
 */
describe('Reveal', () => {
    test('antes de montar el contenido es visible: estado estático, sin retardo', () => {
        const markup = renderToStaticMarkup(
            <Reveal delay={120} data-cy="bloque">
                Contenido
            </Reveal>,
        );

        expect(markup).toContain('data-reveal="static"');
        expect(markup).not.toContain('transition-delay');
        expect(markup).toContain('data-cy="bloque"');
        expect(markup).toContain('Contenido');
    });
});

/** Ventana simulada: movimiento reducido conmutable y un observador que se puede disparar. */
function fakeWindow({ reduced = false, top = 2000 } = {}) {
    const listeners = new Set<() => void>();
    const observers: {
        fire: (...isIntersecting: boolean[]) => void;
        disconnected: boolean;
        observed: number;
    }[] = [];
    const motion = {
        matches: reduced,
        addEventListener: (_: string, listener: () => void) =>
            listeners.add(listener),
        removeEventListener: (_: string, listener: () => void) =>
            listeners.delete(listener),
    };

    class Observer {
        record: (typeof observers)[number];

        constructor(
            callback: (entries: { isIntersecting: boolean }[]) => void,
        ) {
            // Un aviso puede traer varias entradas: las que se acumularon desde el anterior.
            this.record = {
                fire: (...states) =>
                    callback(
                        states.map((isIntersecting) => ({ isIntersecting })),
                    ),
                disconnected: false,
                observed: 0,
            };
            observers.push(this.record);
        }

        observe() {
            this.record.observed++;
        }

        disconnect() {
            this.record.disconnected = true;
        }
    }

    const win = {
        innerHeight: 800,
        matchMedia: () => motion as unknown as MediaQueryList,
        IntersectionObserver:
            Observer as unknown as typeof IntersectionObserver,
    };
    const element = {
        getBoundingClientRect: () => ({ top }) as DOMRect,
    } as Element;

    return {
        win,
        element,
        listeners,
        observers,
        setReduced(value: boolean) {
            motion.matches = value;
            [...listeners].forEach((listener) => listener());
        },
    };
}

describe('Reveal con movimiento reducido dinámico (VIS-L01)', () => {
    test('lo de abajo se oculta y espera a verse', () => {
        const fake = fakeWindow();
        const states: RevealState[] = [];

        watchReveal(fake.element, fake.win, (state) => states.push(state));
        expect(states).toEqual(['hidden']);
        expect(fake.observers[0].observed).toBe(1);
        expect(fake.listeners.size).toBe(1);
    });

    test('si el movimiento reducido se activa con la página abierta, lo oculto pasa a estático y se retiran las escuchas', () => {
        const fake = fakeWindow();
        const states: RevealState[] = [];

        watchReveal(fake.element, fake.win, (state) => states.push(state));
        fake.setReduced(true);

        expect(states).toEqual(['hidden', 'static']);
        expect(fake.observers[0].disconnected).toBe(true);
        expect(fake.listeners.size).toBe(0);

        // Ningún aviso posterior lo vuelve a tocar: ni el observador ni un
        // nuevo cambio de preferencia.
        fake.observers[0].fire(true);
        fake.setReduced(false);
        fake.setReduced(true);
        expect(states).toEqual(['hidden', 'static']);
    });

    test('al verse entra una vez y se retiran las escuchas', () => {
        const fake = fakeWindow();
        const states: RevealState[] = [];

        watchReveal(fake.element, fake.win, (state) => states.push(state));
        fake.observers[0].fire(false);
        fake.observers[0].fire(true);
        fake.setReduced(true);

        expect(states).toEqual(['hidden', 'shown']);
        expect(fake.observers[0].disconnected).toBe(true);
        expect(fake.listeners.size).toBe(0);
    });

    test('DEF-19: si el aviso inicial (fuera) y el siguiente (dentro) llegan juntos, entra igual', () => {
        const fake = fakeWindow();
        const states: RevealState[] = [];

        watchReveal(fake.element, fake.win, (state) => states.push(state));
        fake.observers[0].fire(false, true);

        expect(states).toEqual(['hidden', 'shown']);
        expect(fake.observers[0].disconnected).toBe(true);
    });

    test('con movimiento reducido al montar, o si ya se ve, no se oculta ni observa', () => {
        for (const fake of [
            fakeWindow({ reduced: true }),
            fakeWindow({ top: 100 }),
        ]) {
            const states: RevealState[] = [];

            watchReveal(fake.element, fake.win, (state) => states.push(state));
            expect(states).toEqual([]);
            expect(fake.observers).toHaveLength(0);
            expect(fake.listeners.size).toBe(0);
        }
    });

    test('al desmontar se desconecta el observador y se retira la escucha', () => {
        const fake = fakeWindow();
        const stop = watchReveal(fake.element, fake.win, () => {});

        stop();
        expect(fake.observers[0].disconnected).toBe(true);
        expect(fake.listeners.size).toBe(0);
    });
});

describe('Hojas de la escena', () => {
    test('son las tres etapas del expediente, en este orden', () => {
        expect(STAGE_SHEETS.map((sheet) => sheet.stage)).toEqual([
            'vacancy',
            'evidence',
            'decision',
        ]);
    });
});

describe('Carpeta del proceso: se abre al bajar y se cierra al subir', () => {
    test('cerrada antes de entrar, abierta al llegar al tercio superior, y monótona entre medias', () => {
        const viewport = 800;

        expect(folderOpenness(viewport, viewport)).toBe(0);
        expect(folderOpenness(0.9 * viewport, viewport)).toBe(0);
        expect(folderOpenness(0.3 * viewport, viewport)).toBe(1);
        expect(folderOpenness(-400, viewport)).toBe(1);

        let previous = -1;

        for (let top = viewport; top >= 0; top -= 20) {
            const open = folderOpenness(top, viewport);

            expect(open).toBeGreaterThanOrEqual(previous);
            previous = open;
        }
    });

    test('cerrada, las hojas se apilan detrás del expediente; abierta, se separan en profundidad', () => {
        expect(sheetTransform('vacancy', 0)).toBe(
            'translate3d(0px, -27px, -36px) rotateZ(0deg)',
        );
        expect(sheetTransform('vacancy', 1)).toBe(
            'translate3d(-44px, -128px, -170px) rotateZ(-3deg)',
        );
        expect(sheetTransform('decision', 1)).toBe(
            'translate3d(52px, 70px, -40px) rotateZ(-1.5deg)',
        );
    });

    test('el paralaje del cursor es independiente de lo abierta que esté', () => {
        const xy = (transform: string) =>
            /translate3d\((-?[\d.]+)px, (-?[\d.]+)px/
                .exec(transform)!
                .slice(1)
                .map(Number);
        const offset = (open: number) => {
            const [restX, restY] = xy(sheetTransform('vacancy', open));
            const [movedX, movedY] = xy(sheetTransform('vacancy', open, 1, 1));

            return [movedX - restX, movedY - restY];
        };

        expect(offset(0)).toEqual(offset(1));
        expect(offset(0.5)).toEqual(offset(1));
        expect(offset(1)).toEqual([-18, -18]);
    });
});
