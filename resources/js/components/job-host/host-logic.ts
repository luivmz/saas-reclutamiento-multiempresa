/**
 * Lógica del anfitrión de /empleos, sin DOM: qué zona señalar, por qué
 * fotogramas pasar para llegar a ella, cuándo puede reaccionar otra vez y
 * cuánto inclinarse hacia el cursor. Se prueba sin navegador.
 *
 * El clip de señalar (`anfitrion-senala.webm`, 97 fotogramas) es un gesto
 * pregrabado: el apuntador sube, baja y vuelve al reposo. Medida la punta del
 * apuntador fotograma a fotograma:
 *
 * | Fotogramas | Pose |
 * |---|---|
 * | 0–9 y 87–96 | reposo (el 96 es casi idéntico al 0) |
 * | 21–36 | arriba |
 * | ~48 y ~78 | a media altura |
 * | 54–66 | abajo, con la mirada baja |
 *
 * No hay articulación independiente de ojos ni brazo: el anfitrión elige el
 * fotograma cuya pose apunta hacia la zona de la oferta activa.
 */
export type Zone = 'up' | 'mid' | 'down';

export const CLIP_FPS = 24;
/** Fotogramas del clip de señalar. El último (96) cierra el ciclo con el 0. */
export const POINT_FRAMES = 97;
const CYCLE = POINT_FRAMES - 1;

export const ZONE_FRAMES: Record<Zone | 'rest', readonly number[]> = {
    up: [27],
    mid: [48, 78],
    down: [60],
    rest: [0],
};

/** La mano que sujeta el apuntador está a esta altura del personaje (fracción desde arriba). */
const HAND = 0.3;

/**
 * Zona de una oferta respecto del anfitrión: comparada con la altura de su
 * mano, en fracciones de la altura del personaje.
 */
export function zoneFor(
    targetCenterY: number,
    hostTop: number,
    hostHeight: number,
): Zone {
    if (!(hostHeight > 0)) {
        return 'mid';
    }

    const offset = (targetCenterY - (hostTop + HAND * hostHeight)) / hostHeight;

    if (offset < -0.25) {
        return 'up';
    }

    return offset > 0.45 ? 'down' : 'mid';
}

function wrap(frame: number): number {
    return ((frame % CYCLE) + CYCLE) % CYCLE;
}

/** Distancia con signo de `from` a `to` por el camino más corto del ciclo. */
export function cyclicDelta(from: number, to: number): number {
    const forward = wrap(to - from);

    return forward <= CYCLE / 2 ? forward : forward - CYCLE;
}

/** De los fotogramas candidatos, el más cercano a `from` siguiendo el ciclo. */
export function nearestGoal(
    from: number,
    candidates: readonly number[],
): number {
    return candidates.reduce((best, candidate) =>
        Math.abs(cyclicDelta(from, candidate)) <
        Math.abs(cyclicDelta(from, best))
            ? candidate
            : best,
    );
}

/** Un paso (un fotograma) de `from` hacia `goal`; si ya está, devuelve `from`. */
export function stepToward(from: number, goal: number): number {
    const delta = cyclicDelta(from, goal);

    return delta === 0 ? wrap(from) : wrap(from + Math.sign(delta));
}

/** El instante central de un fotograma: ningún redondeo muestra el vecino. */
export function timeForFrame(frame: number): number {
    return (wrap(frame) + 0.5) / CLIP_FPS;
}

/** Si puede volver a reaccionar con interés: como mucho una vez cada `cooldownMs`. */
export function canReact(
    now: number,
    lastReaction: number | null,
    cooldownMs: number,
): boolean {
    return lastReaction === null || now - lastReaction >= cooldownMs;
}

/** Índice del rectángulo cuyo centro está más cerca del centro de la ventana, o -1. */
export function nearestToCenter(
    rects: readonly Pick<DOMRect, 'top' | 'bottom'>[],
    viewportHeight: number,
): number {
    const center = viewportHeight / 2;
    let best = -1;
    let bestDistance = Infinity;

    rects.forEach((rect, index) => {
        if (rect.bottom <= 0 || rect.top >= viewportHeight) {
            return;
        }

        const distance = Math.abs((rect.top + rect.bottom) / 2 - center);

        if (distance < bestDistance) {
            best = index;
            bestDistance = distance;
        }
    });

    return best;
}

/** Inclinación pequeña del contenedor hacia el cursor, en grados, acotada. */
export function tiltFor(
    pointerX: number,
    pointerY: number,
    host: Pick<DOMRect, 'left' | 'top' | 'width' | 'height'>,
): { rotateX: number; rotateY: number } {
    const clamp = (value: number) => Math.max(-1, Math.min(1, value));
    const x = clamp((pointerX - (host.left + host.width / 2)) / 600);
    const y = clamp((pointerY - (host.top + host.height / 2)) / 500);

    return {
        rotateY: Math.round(x * 7 * 100) / 100 + 0,
        rotateX: Math.round(-y * 4 * 100) / 100 + 0,
    };
}
