import { useEffect, useRef, useState } from 'react';
import { latestIntersecting } from '@/lib/intersection';
import { SheetFace, STAGE_SHEETS } from './recruitment-scene-poster';

/**
 * Vacante, evidencias y decisión humana: la carpeta del proceso, en profundidad.
 *
 * Detrás del expediente de la sección «Cómo avanza un proceso», las tres hojas
 * del recorrido esperan apiladas. **Al bajar, la carpeta se abre**: cada hoja se
 * separa hacia su profundidad —la ficha de la vacante al fondo, el legajo de
 * evidencias en medio y la hoja de firma cerca del expediente—. **Al subir, el
 * movimiento retrocede** y vuelven a apilarse. Aparte, el cursor gira apenas la
 * escena y desplaza cada hoja según su profundidad (paralaje), sin tocar lo
 * abierta que está.
 *
 * Tres decisiones sostienen el presupuesto (ADR-003):
 *
 * - **CSS 3D, no WebGL.** Perspectiva y capas de DOM compuestas por la GPU:
 *   sin dependencia, sin contexto que perder y sin bucle de render.
 * - **Movimiento por evento, no por bucle.** Se recalcula, a lo sumo una vez
 *   por cuadro, cuando la página se desplaza o el puntero se mueve, y solo
 *   mientras la escena está a la vista. El cursor, solo con punteros finos.
 * - **Transforms directos sobre los elementos**: ni estado de React ni
 *   variables CSS por cada movimiento. El desplazamiento es el del navegador:
 *   nunca se captura.
 *
 * Todo es decorativo: vive dentro de una capa `aria-hidden` e `inert`, sin
 * foco ni eventos, y ninguna información existe solo aquí.
 */

const REST = { x: 6, y: -9 };
const TILT = { x: 4, y: 7 };

type Placement = { x: number; y: number; z: number; rotate: number };

/** Abierta: dónde reposa cada hoja respecto del expediente, y cuánto la mueve el cursor. */
const OPEN = {
    vacancy: {
        x: -44,
        y: -128,
        z: -170,
        rotate: -3,
        parallax: 18,
        shade: 0.85,
    },
    evidence: {
        x: 80,
        y: -60,
        z: -100,
        rotate: 2.5,
        parallax: 12,
        shade: 0.92,
    },
    decision: { x: 52, y: 70, z: -40, rotate: -1.5, parallax: 7, shade: 0.97 },
} as const;

/** Cerrada: las hojas apiladas detrás del expediente, asomando por arriba como en el póster. */
const CLOSED: Record<keyof typeof OPEN, Placement> = {
    vacancy: { x: 0, y: -27, z: -36, rotate: 0 },
    evidence: { x: 0, y: -18, z: -24, rotate: 0 },
    decision: { x: 0, y: -9, z: -12, rotate: 0 },
};

/**
 * Empieza a abrirse cuando el borde superior de la carpeta pasa el 90 % del
 * alto de la ventana y termina cuando llega al 30 %.
 */
const OPEN_START = 0.9;
const OPEN_SPAN = 0.6;

/** Cuánto está abierta la carpeta, de 0 a 1, según dónde está en la ventana. */
export function folderOpenness(top: number, viewport: number): number {
    if (!(viewport > 0)) {
        return 0;
    }

    const t = Math.min(
        1,
        Math.max(0, (OPEN_START * viewport - top) / (OPEN_SPAN * viewport)),
    );

    // Suavizado en los extremos: arranca y llega sin tirón.
    return t * t * (3 - 2 * t);
}

function mix(from: number, to: number, amount: number): number {
    return from + (to - from) * amount;
}

/** Dos decimales y nunca «-0»: el mismo estado da siempre la misma cadena. */
function n(value: number): string {
    return String(Math.round(value * 100) / 100 + 0);
}

export function groupTransform(open: number, pointerX = 0, pointerY = 0) {
    return `rotateX(${n(mix(0, REST.x, open) - pointerY * TILT.x)}deg) rotateY(${n(mix(0, REST.y, open) + pointerX * TILT.y)}deg)`;
}

export function sheetTransform(
    stage: keyof typeof OPEN,
    open: number,
    pointerX = 0,
    pointerY = 0,
): string {
    const from = CLOSED[stage];
    const to = OPEN[stage];

    // El paralaje no depende de lo abierta que esté: las hojas lejanas se
    // desplazan más, en sentido contrario al cursor.
    const x = mix(from.x, to.x, open) - pointerX * to.parallax;
    const y = mix(from.y, to.y, open) - pointerY * to.parallax;

    return `translate3d(${n(x)}px, ${n(y)}px, ${n(mix(from.z, to.z, open))}px) rotateZ(${n(mix(from.rotate, to.rotate, open))}deg)`;
}

function clamp(value: number): number {
    return Math.max(-1, Math.min(1, value));
}

export default function RecruitmentScene() {
    const rootRef = useRef<HTMLDivElement>(null);
    const groupRef = useRef<HTMLDivElement>(null);
    const sheetRefs = useRef<(HTMLDivElement | null)[]>([]);
    const [ready, setReady] = useState(false);

    useEffect(() => {
        const root = rootRef.current;
        const group = groupRef.current;

        if (!root || !group) {
            return;
        }

        const finePointer = window.matchMedia(
            '(hover: hover) and (pointer: fine)',
        ).matches;
        let frame = 0;
        let pointer: { x: number; y: number } | null = null;
        let visible = false;

        const apply = () => {
            frame = 0;
            const open = folderOpenness(
                root.getBoundingClientRect().top,
                window.innerHeight,
            );

            // Observable para las pruebas: lo abierta que está la carpeta.
            root.dataset.open = open.toFixed(2);
            group.style.transform = groupTransform(
                open,
                pointer?.x,
                pointer?.y,
            );
            STAGE_SHEETS.forEach((sheet, index) => {
                const element = sheetRefs.current[index];

                if (element) {
                    element.style.transform = sheetTransform(
                        sheet.stage,
                        open,
                        pointer?.x,
                        pointer?.y,
                    );
                }
            });
        };

        const schedule = () => {
            if (!frame) {
                frame = requestAnimationFrame(apply);
            }
        };

        const onMove = (event: PointerEvent) => {
            const box = root.getBoundingClientRect();

            pointer = {
                x: clamp(
                    (event.clientX - (box.left + box.width / 2)) / box.width,
                ),
                y: clamp(
                    (event.clientY - (box.top + box.height / 2)) / box.height,
                ),
            };
            schedule();
        };

        const onLeave = () => {
            pointer = null;
            schedule();
        };

        const watch = (on: boolean) => {
            if (on === visible) {
                return;
            }

            visible = on;
            const method = on ? 'addEventListener' : 'removeEventListener';

            window[method]('scroll', schedule, { passive: true });
            window[method]('resize', schedule);

            if (finePointer) {
                // Observable para las pruebas: si la escena escucha el puntero.
                root.dataset.pointer = on ? 'listening' : 'idle';
                window[method]('pointermove', onMove as EventListener, {
                    passive: true,
                });
                document.documentElement[method]('pointerleave', onLeave);

                if (!on) {
                    pointer = null;
                }
            }
        };

        // Primera posición sin transición: la que corresponde a donde ya está
        // la página. Después, las transiciones suavizan los saltos de la rueda.
        apply();
        const first = requestAnimationFrame(() => setReady(true));
        // El estado más reciente del aviso, no el primero (DEF-19).
        const observer = new IntersectionObserver((entries) => {
            const visibleNow = latestIntersecting(entries);

            if (visibleNow !== null) {
                watch(visibleNow);
            }

            schedule();
        });

        observer.observe(root);

        return () => {
            observer.disconnect();
            watch(false);
            cancelAnimationFrame(frame);
            cancelAnimationFrame(first);
        };
    }, []);

    return (
        <div
            ref={rootRef}
            className="absolute inset-0"
            style={{ perspective: '1200px', perspectiveOrigin: '50% 30%' }}
            data-cy="recruitment-scene"
            data-ready={ready}
        >
            <div
                ref={groupRef}
                className="absolute inset-0"
                style={{
                    transformStyle: 'preserve-3d',
                    transform: groupTransform(0),
                    transition: ready
                        ? 'transform 260ms var(--ease-out)'
                        : undefined,
                    willChange: 'transform',
                }}
            >
                {STAGE_SHEETS.map((sheet, index) => (
                    <div
                        key={sheet.stage}
                        data-sheet={sheet.stage}
                        ref={(element) => {
                            sheetRefs.current[index] = element;
                        }}
                        className="bg-card absolute inset-0 overflow-hidden rounded-xl border shadow-[0_32px_64px_-28px_oklch(0.25_0.04_220/0.45)]"
                        style={{
                            backfaceVisibility: 'hidden',
                            opacity: OPEN[sheet.stage].shade,
                            transform: sheetTransform(sheet.stage, 0),
                            transition: ready
                                ? 'transform 260ms var(--ease-out)'
                                : undefined,
                        }}
                    >
                        <SheetFace edge={sheet.edge} kind={sheet.stage} />
                    </div>
                ))}
            </div>
        </div>
    );
}
