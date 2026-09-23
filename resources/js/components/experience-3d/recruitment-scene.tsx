import { useEffect, useRef, useState } from 'react';
import { SheetFace, STAGE_SHEETS } from './recruitment-scene-poster';

/**
 * El archivo detrás del expediente, en profundidad.
 *
 * La portada muestra un expediente. Detrás, las hojas de otros expedientes se
 * alejan en perspectiva, cada una con el tono de su etapa: el que se ve es uno
 * entre muchos, guardado y trazable. Es lo único que el diseño plano sugería
 * sin poder hacerlo espacial.
 *
 * Tres decisiones sostienen el presupuesto:
 *
 * - **CSS 3D, no WebGL.** Perspectiva y capas de DOM compuestas por la GPU:
 *   sin dependencia, sin contexto que perder y sin bucle de render. Un
 *   navegador sin WebGL la muestra igual.
 * - **Movimiento por evento, no por bucle.** Nada se redibuja mientras nadie
 *   mueve el puntero, así que no hay nada que pausar al ocultar la pestaña o
 *   salir del viewport. La escucha del puntero, además, solo existe mientras
 *   la escena está a la vista y solo con punteros finos.
 * - **Transforms directos sobre el elemento.** Nada de variables CSS en el
 *   padre ni estado de React por cada movimiento: un solo `transform` en el
 *   grupo, a lo sumo una vez por cuadro.
 *
 * Todo el archivo es decorativo: vive dentro de una capa `aria-hidden` e
 * `inert`, sin foco ni eventos, y ninguna información existe solo aquí.
 */

const REST = { x: 8, y: -6 };
const TILT = { x: 3, y: 5 };

function groupTransform(pointerX = 0, pointerY = 0): string {
    return `rotateX(${REST.x - pointerY * TILT.x}deg) rotateY(${REST.y + pointerX * TILT.y}deg)`;
}

function clamp(value: number): number {
    return Math.max(-1, Math.min(1, value));
}

export default function RecruitmentScene() {
    const rootRef = useRef<HTMLDivElement>(null);
    const groupRef = useRef<HTMLDivElement>(null);
    const [ready, setReady] = useState(false);

    // La única entrada: al primer cuadro tras montar, las hojas se abren en
    // abanico desde detrás del expediente. Son transiciones, no keyframes, de
    // modo que se pueden interrumpir.
    useEffect(() => {
        const frame = requestAnimationFrame(() => setReady(true));

        return () => cancelAnimationFrame(frame);
    }, []);

    useEffect(() => {
        const root = rootRef.current;
        const group = groupRef.current;

        if (!root || !group) {
            return;
        }

        // En pantallas táctiles el «hover» es un toque en falso: sin punteros
        // finos, la escena queda quieta en su orientación de reposo.
        if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
            return;
        }

        let frame = 0;
        let pointer: { x: number; y: number } | null = null;
        let listening = false;

        const apply = () => {
            frame = 0;
            group.style.transform = groupTransform(pointer?.x, pointer?.y);
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

        const observer = new IntersectionObserver(([entry]) =>
            listen(entry.isIntersecting),
        );

        observer.observe(root);

        return () => {
            observer.disconnect();
            listen(false);
            cancelAnimationFrame(frame);
        };
    }, []);

    return (
        <div
            ref={rootRef}
            className="absolute inset-0"
            style={{ perspective: '1400px', perspectiveOrigin: '50% 0%' }}
            data-cy="recruitment-scene"
            data-ready={ready}
        >
            <div
                ref={groupRef}
                className="absolute inset-0"
                style={{
                    transformStyle: 'preserve-3d',
                    transform: groupTransform(),
                    transition: 'transform 300ms var(--ease-out)',
                    willChange: 'transform',
                }}
            >
                {STAGE_SHEETS.map((sheet, index) => {
                    // Del fondo (4) al más cercano al expediente (1).
                    const depth = STAGE_SHEETS.length - index;
                    // Se abre primero la hoja más cercana: el abanico nace
                    // del expediente hacia el fondo.
                    const delay = (depth - 1) * 40;

                    return (
                        <div
                            key={sheet.stage}
                            className="bg-card absolute inset-0 rounded-xl border"
                            style={{
                                backfaceVisibility: 'hidden',
                                opacity: ready ? 1 - depth * 0.14 : 0,
                                transform: ready
                                    ? `translate3d(0, ${-depth * 15}px, ${-depth * 48}px)`
                                    : 'translate3d(0, 0, 0)',
                                transition: `transform 480ms var(--ease-out) ${delay}ms, opacity 320ms var(--ease-out) ${delay}ms`,
                            }}
                        >
                            <SheetFace edge={sheet.edge} />
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
