import { useEffect, useRef, useState } from 'react';
import { latestIntersecting } from '@/lib/intersection';
import { SheetFace, STAGE_SHEETS } from './recruitment-scene-poster';

/**
 * Vacante, evidencias y decisión humana, en profundidad.
 *
 * Detrás del expediente de la portada, las tres hojas del recorrido flotan a
 * distintas distancias: la ficha de la vacante al fondo, el legajo de
 * evidencias en medio y la hoja de firma cerca del expediente. Al mover el
 * cursor, la escena gira apenas y cada hoja se desplaza según su profundidad
 * (paralaje), como si se mirara una mesa de trabajo desde otro ángulo.
 *
 * Tres decisiones sostienen el presupuesto (ADR-003):
 *
 * - **CSS 3D, no WebGL.** Perspectiva y capas de DOM compuestas por la GPU:
 *   sin dependencia, sin contexto que perder y sin bucle de render. Un
 *   navegador sin WebGL la muestra igual.
 * - **Movimiento por evento, no por bucle.** Nada se redibuja mientras nadie
 *   mueve el puntero. La escucha solo existe mientras la escena está a la vista
 *   y solo con punteros finos: en pantallas táctiles queda en reposo.
 * - **Transforms directos sobre los elementos**, a lo sumo una vez por cuadro:
 *   ni estado de React ni variables CSS por cada movimiento.
 *
 * Todo es decorativo: vive dentro de una capa `aria-hidden` e `inert`, sin
 * foco ni eventos, y ninguna información existe solo aquí.
 */

const REST = { x: 6, y: -9 };
const TILT = { x: 4, y: 7 };

/** Dónde reposa cada hoja respecto del expediente, y cuánto la mueve el cursor. */
const PLACEMENT = {
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

function groupTransform(pointerX = 0, pointerY = 0): string {
    return `rotateX(${REST.x - pointerY * TILT.x}deg) rotateY(${REST.y + pointerX * TILT.y}deg)`;
}

function sheetTransform(
    stage: keyof typeof PLACEMENT,
    pointerX = 0,
    pointerY = 0,
): string {
    const p = PLACEMENT[stage];

    // Las hojas lejanas se desplazan más en sentido contrario al cursor.
    return `translate3d(${p.x - pointerX * p.parallax}px, ${p.y - pointerY * p.parallax}px, ${p.z}px) rotateZ(${p.rotate}deg)`;
}

function clamp(value: number): number {
    return Math.max(-1, Math.min(1, value));
}

export default function RecruitmentScene() {
    const rootRef = useRef<HTMLDivElement>(null);
    const groupRef = useRef<HTMLDivElement>(null);
    const sheetRefs = useRef<(HTMLDivElement | null)[]>([]);
    const [ready, setReady] = useState(false);

    // La única entrada: al primer cuadro tras montar, las hojas se abren desde
    // detrás del expediente hacia su sitio. Son transiciones, no keyframes, de
    // modo que se pueden interrumpir.
    useEffect(() => {
        const frame = requestAnimationFrame(() => setReady(true));

        return () => cancelAnimationFrame(frame);
    }, []);

    useEffect(() => {
        const root = rootRef.current;
        const group = groupRef.current;

        if (!root || !group || !ready) {
            return;
        }

        if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
            return;
        }

        let frame = 0;
        let pointer: { x: number; y: number } | null = null;
        let listening = false;

        const apply = () => {
            frame = 0;
            group.style.transform = groupTransform(pointer?.x, pointer?.y);
            STAGE_SHEETS.forEach((sheet, index) => {
                const element = sheetRefs.current[index];

                if (element) {
                    // Tras la entrada, el cursor responde sin el retardo
                    // escalonado de la apertura.
                    element.style.transition =
                        'transform 400ms var(--ease-out), opacity 450ms var(--ease-out)';
                    element.style.transform = sheetTransform(
                        sheet.stage,
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

        const listen = (on: boolean) => {
            if (on === listening) {
                return;
            }

            listening = on;
            // Observable para las pruebas: si la escena escucha el puntero.
            root.dataset.pointer = on ? 'listening' : 'idle';

            if (on) {
                window.addEventListener('pointermove', onMove, {
                    passive: true,
                });
                document.documentElement.addEventListener(
                    'pointerleave',
                    onLeave,
                );
            } else {
                window.removeEventListener('pointermove', onMove);
                document.documentElement.removeEventListener(
                    'pointerleave',
                    onLeave,
                );
                onLeave();
            }
        };

        const observer = new IntersectionObserver((entries) => {
            const visible = latestIntersecting(entries);
            if (visible !== null) listen(visible);
        });

        observer.observe(root);

        return () => {
            observer.disconnect();
            listen(false);
            cancelAnimationFrame(frame);
        };
    }, [ready]);

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
                    transform: groupTransform(),
                    transition: 'transform 400ms var(--ease-out)',
                    willChange: 'transform',
                }}
            >
                {STAGE_SHEETS.map((sheet, index) => {
                    const placement = PLACEMENT[sheet.stage];
                    // Se abre primero la hoja más cercana al expediente.
                    const delay = (STAGE_SHEETS.length - 1 - index) * 70;

                    return (
                        <div
                            key={sheet.stage}
                            data-sheet={sheet.stage}
                            ref={(element) => {
                                sheetRefs.current[index] = element;
                            }}
                            className="bg-card absolute inset-0 overflow-hidden rounded-xl border shadow-[0_32px_64px_-28px_oklch(0.25_0.04_220/0.45)]"
                            style={{
                                backfaceVisibility: 'hidden',
                                opacity: ready ? placement.shade : 0,
                                transform: ready
                                    ? sheetTransform(sheet.stage)
                                    : 'translate3d(0, 0, -20px)',
                                transition: ready
                                    ? `transform 700ms var(--ease-out) ${delay}ms, opacity 450ms var(--ease-out) ${delay}ms`
                                    : undefined,
                            }}
                        >
                            <SheetFace edge={sheet.edge} kind={sheet.stage} />
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
