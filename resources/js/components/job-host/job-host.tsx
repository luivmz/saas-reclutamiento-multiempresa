import { useEffect, useRef, useState, type RefObject } from 'react';
import { REDUCED_MOTION_QUERY } from '@/components/experience-3d/use-scene-capability';
import { latestIntersecting } from '@/lib/intersection';
import {
    canReact,
    nearestGoal,
    nearestToCenter,
    stepToward,
    tiltFor,
    timeForFrame,
    ZONE_FRAMES,
    zoneFor,
    type Zone,
} from './host-logic';

/**
 * Anfitrión del listado público de empleos.
 *
 * Un personaje ilustrado acompaña la exploración de las ofertas desde la
 * derecha. **Es decorativo**: `aria-hidden`, `inert` y sin eventos de puntero;
 * ninguna información ni acción depende de él, y su sonrisa invita a explorar,
 * no recomienda ni valora ninguna oferta.
 *
 * - **Reposo:** su pose neutral (póster transparente).
 * - **Interés:** al entrar con el cursor en una oferta, o al llevarle el foco
 *   del teclado, reproduce una vez la reacción de interés (como mucho cada
 *   8 s), y después señala.
 * - **Señalar:** recorre el clip de señalar, fotograma a fotograma, hasta la
 *   pose que apunta hacia la zona (arriba, media altura o abajo) de la oferta
 *   activa. Sin oferta activa, mientras se desplaza la página, señala la más
 *   cercana al centro. La última oferta manda; nada se reinicia por pasar
 *   deprisa entre tarjetas.
 * - **Seguimiento:** el contenedor se inclina unos grados hacia el cursor. El
 *   personaje no se desplaza por la pantalla ni se deforma.
 * - **Vuelta al reposo:** sin oferta activa, recorre el clip hasta el reposo y
 *   funde al póster.
 *
 * **Carga.** Solo en escritorio de 1280 px o más. Los clips (WebM VP9 con
 * transparencia) se descargan la primera vez que el anfitrión se ve, y solo
 * con puntero fino, sin movimiento reducido, sin ahorro de datos, en un equipo
 * no modesto y en un navegador que muestre su transparencia. En otro caso
 * queda el póster. Si falla un clip, se prescinde de él; si falla el póster,
 * el anfitrión desaparece y el listado sigue igual.
 */
export const HOST_MEDIA = {
    poster: '/media/anfitrion/anfitrion-reposo.webp',
    interest: '/media/anfitrion/anfitrion-interes.webm',
    point: '/media/anfitrion/anfitrion-senala.webm',
} as const;

/** Desde este ancho hay sitio para el anfitrión junto a las ofertas. */
export const HOST_MIN_WIDTH = 1280;
const WIDE_QUERY = `(min-width: ${HOST_MIN_WIDTH}px)`;
const FINE_POINTER_QUERY = '(hover: hover) and (pointer: fine)';
const INTEREST_COOLDOWN_MS = 8000;
const IDLE_MS = 900;
const SCROLL_IDLE_MS = 1400;
/** Un desplazamiento cuenta como exploración si una entrada del usuario lo precedió en este margen. */
const USER_SCROLL_MS = 1000;
const STEP_MS = 1000 / 30;
/** De vuelta al reposo, el gesto recorre el clip más deprisa. */
const RETURN_STEP_MS = 1000 / 48;

export type HostMode = 'off' | 'static' | 'animated';
type Clip = 'rest' | 'interest' | 'point';

/** Las URL de los clips ya descargados se comparten entre visitas a la página. */
const clipCache = new Map<string, Promise<string>>();

function loadClip(url: string): Promise<string> {
    let pending = clipCache.get(url);

    if (!pending) {
        pending = fetch(url)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                return response.blob();
            })
            .then((blob) => URL.createObjectURL(blob));
        pending.catch(() => clipCache.delete(url));
        clipCache.set(url, pending);
    }

    return pending;
}

/** Si el navegador muestra la transparencia de un WebM VP9 (Safari no). */
function supportsAlphaWebm(win: Window): boolean {
    const ua = win.navigator.userAgent;
    const safari =
        /Safari\//.test(ua) &&
        !/Chrome|Chromium|CriOS|Edg|Firefox|Android/.test(ua);

    return (
        !safari &&
        win.document
            .createElement('video')
            .canPlayType('video/webm; codecs="vp9"') !== ''
    );
}

export function detectHostMode(win: Window | undefined): {
    mode: HostMode;
    reason: string;
} {
    if (!win) {
        return { mode: 'off', reason: 'server' };
    }

    if (!win.matchMedia(WIDE_QUERY).matches) {
        return { mode: 'off', reason: 'narrow' };
    }

    const nav = win.navigator as Navigator & {
        connection?: { saveData?: boolean };
        deviceMemory?: number;
    };

    if (win.matchMedia(REDUCED_MOTION_QUERY).matches) {
        return { mode: 'static', reason: 'reduced-motion' };
    }

    if (!win.matchMedia(FINE_POINTER_QUERY).matches) {
        return { mode: 'static', reason: 'coarse-pointer' };
    }

    if (nav.connection?.saveData) {
        return { mode: 'static', reason: 'save-data' };
    }

    if ((nav.hardwareConcurrency ?? 8) <= 2 || (nav.deviceMemory ?? 8) <= 2) {
        return { mode: 'static', reason: 'low-end' };
    }

    if (!supportsAlphaWebm(win)) {
        return { mode: 'static', reason: 'no-alpha-video' };
    }

    return { mode: 'animated', reason: 'ok' };
}

function useHostMode() {
    const [state, setState] = useState<{ mode: HostMode; reason: string }>({
        mode: 'off',
        reason: 'server',
    });

    useEffect(() => {
        const update = () => setState(detectHostMode(window));
        const queries = [
            WIDE_QUERY,
            REDUCED_MOTION_QUERY,
            FINE_POINTER_QUERY,
        ].map((query) => window.matchMedia(query));

        update();
        queries.forEach((query) => query.addEventListener('change', update));

        return () =>
            queries.forEach((query) =>
                query.removeEventListener('change', update),
            );
    }, []);

    return state;
}

type Props = {
    /** El contenedor de las ofertas: el anfitrión escucha dentro de él. */
    listRef: RefObject<HTMLElement | null>;
    /** Selector de cada oferta dentro de la lista. */
    itemSelector?: string;
    className?: string;
};

export function JobHost({
    listRef,
    itemSelector = '[data-cy="job-card"]',
    className,
}: Props) {
    const { mode, reason } = useHostMode();
    const [posterFailed, setPosterFailed] = useState(false);
    const rootRef = useRef<HTMLDivElement>(null);
    const tiltRef = useRef<HTMLDivElement>(null);
    const interestRef = useRef<HTMLVideoElement>(null);
    const pointRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        const root = rootRef.current;
        const tilt = tiltRef.current;
        const interestVideo = interestRef.current;
        const pointVideo = pointRef.current;
        const list = listRef.current;

        if (
            mode !== 'animated' ||
            !root ||
            !tilt ||
            !interestVideo ||
            !pointVideo ||
            !list
        ) {
            return;
        }

        let disposed = false;
        let visible = false;
        const failed = { interest: false, point: false };
        // Listo = sin fallo y con su primer fotograma decodificado, medido en el
        // momento: no depende del orden en que lleguen los eventos.
        const isReady = (key: 'interest' | 'point') =>
            !failed[key] &&
            (key === 'interest' ? interestVideo : pointVideo).readyState >= 2;
        let clip: Clip = 'rest';
        let target: HTMLElement | null = null;
        let source: 'hover' | 'focus' | 'scroll' | null = null;
        let lastReaction: number | null = null;
        let frame = 0;
        let goal = 0;
        let stepTimer = 0;
        let idleTimer = 0;
        let scrollTimer = 0;
        let tiltFrame = 0;
        let pointer: { x: number; y: number } | null = null;

        const show = (next: Clip) => {
            clip = next;
            root.dataset.clip = next;
        };

        const setTarget = (card: HTMLElement | null, from: typeof source) => {
            if (card === target) {
                source = card ? from : null;

                return;
            }

            target?.removeAttribute('data-anfitrion');
            target = card;
            source = card ? from : null;
            root.dataset.target = card?.dataset.code ?? '';

            if (card) {
                card.setAttribute('data-anfitrion', 'activa');
                window.clearTimeout(idleTimer);
                react();
            } else {
                root.dataset.zone = 'none';

                // Sin oferta activa durante el interés: funde al reposo sin
                // esperar a que el gesto termine.
                if (clip === 'interest') {
                    interestVideo.pause();
                    show('rest');
                }

                schedule();
            }
        };

        /** La zona de la oferta activa, medida ahora (la página puede haberse desplazado). */
        const zone = (): Zone | null => {
            if (!target) {
                return null;
            }

            const host = tilt.getBoundingClientRect();
            const card = target.getBoundingClientRect();

            return zoneFor((card.top + card.bottom) / 2, host.top, host.height);
        };

        const react = () => {
            if (!visible) {
                return;
            }

            const now = performance.now();

            if (
                clip === 'rest' &&
                source !== 'scroll' &&
                isReady('interest') &&
                canReact(now, lastReaction, INTEREST_COOLDOWN_MS)
            ) {
                lastReaction = now;
                show('interest');
                interestVideo.currentTime = 0;
                void interestVideo.play().catch(() => afterInterest());

                return;
            }

            if (clip !== 'interest') {
                startPointing();
            }
        };

        const afterInterest = () => {
            if (disposed || clip !== 'interest') {
                return;
            }

            interestVideo.pause();

            if (target && isReady('point')) {
                startPointing();
            } else {
                show('rest');
            }
        };

        const startPointing = () => {
            if (!isReady('point')) {
                return;
            }

            if (clip !== 'point') {
                frame = 0;
                pointVideo.currentTime = timeForFrame(0);
                show('point');
            }

            schedule();
        };

        // Un único paso pendiente, activo solo mientras queda recorrido. Va a
        // la cadencia del clip (un fotograma cada 1/30 s, o 1/48 s de vuelta al
        // reposo) con un temporizador: no depende de que el navegador pinte, y se
        // detiene con la pestaña oculta o el anfitrión fuera de la vista.
        const schedule = (delay = 0) => {
            if (!stepTimer && !disposed && visible && !document.hidden) {
                stepTimer = window.setTimeout(tick, delay);
            }
        };

        const tick = () => {
            stepTimer = 0;

            if (disposed || clip !== 'point') {
                return;
            }

            const z = zone();

            root.dataset.zone = z ?? 'none';
            goal = nearestGoal(frame, ZONE_FRAMES[z ?? 'rest']);

            if (frame === goal) {
                root.dataset.frame = String(frame);

                if (!z) {
                    // En el reposo: funde al póster.
                    show('rest');
                }

                return;
            }

            // Una búsqueda cada vez: si la anterior no terminó, espera al siguiente paso.
            if (!pointVideo.seeking) {
                frame = stepToward(frame, goal);
                root.dataset.frame = String(frame);
                pointVideo.currentTime = timeForFrame(frame);
            }

            schedule(z ? STEP_MS : RETURN_STEP_MS);
        };

        const cardFrom = (node: EventTarget | null) =>
            node instanceof Element
                ? (node.closest(itemSelector) as HTMLElement | null)
                : null;

        const onOver = (event: PointerEvent) => {
            const card = cardFrom(event.target);

            if (card && list.contains(card)) {
                setTarget(card, 'hover');
            }
        };

        const leaveSoon = () => {
            window.clearTimeout(idleTimer);
            idleTimer = window.setTimeout(() => {
                if (source !== 'focus') {
                    setTarget(null, null);
                }
            }, IDLE_MS);
        };

        const onListLeave = () => {
            if (source === 'hover') {
                leaveSoon();
            }
        };

        const onFocusIn = (event: FocusEvent) => {
            const card = cardFrom(event.target);

            if (card) {
                setTarget(card, 'focus');
            }
        };

        const onFocusOut = (event: FocusEvent) => {
            if (!list.contains(event.relatedTarget as Node | null)) {
                source = 'scroll';
                leaveSoon();
            }
        };

        // Solo el desplazamiento que hace la persona (rueda, gesto táctil,
        // teclado o barra) elige oferta: no la restauración de Inertia al
        // cambiar de página ni un desplazamiento programático.
        let userInputAt = Number.NEGATIVE_INFINITY;
        const onUserInput = () => {
            userInputAt = performance.now();
        };

        const onScroll = () => {
            if (source === 'hover' || source === 'focus') {
                schedule();

                return;
            }

            if (performance.now() - userInputAt > USER_SCROLL_MS) {
                return;
            }

            const cards = Array.from(
                list.querySelectorAll<HTMLElement>(itemSelector),
            );
            const index = nearestToCenter(
                cards.map((card) => card.getBoundingClientRect()),
                window.innerHeight,
            );

            setTarget(index >= 0 ? cards[index] : null, 'scroll');
            window.clearTimeout(scrollTimer);
            scrollTimer = window.setTimeout(() => {
                if (source === 'scroll') {
                    setTarget(null, null);
                }
            }, SCROLL_IDLE_MS);
            schedule();
        };

        const onPointerMove = (event: PointerEvent) => {
            pointer = { x: event.clientX, y: event.clientY };

            if (!tiltFrame) {
                tiltFrame = requestAnimationFrame(() => {
                    tiltFrame = 0;

                    if (!pointer) {
                        return;
                    }

                    const { rotateX, rotateY } = tiltFor(
                        pointer.x,
                        pointer.y,
                        root.getBoundingClientRect(),
                    );

                    tilt.style.transform = `perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                });
            }
        };

        const onPageLeave = () => {
            pointer = null;
            tilt.style.transform = '';
        };

        const pause = () => {
            window.clearTimeout(stepTimer);
            stepTimer = 0;
            interestVideo.pause();
        };

        // Al volver a verse: una reacción de interés que quedó a medias termina
        // (señala o reposa) en lugar de reanudarse.
        const resume = () => {
            if (clip === 'interest') {
                afterInterest();
            }

            schedule();
        };

        const onVisibility = () => {
            if (document.hidden) {
                pause();
            } else if (visible) {
                resume();
            }
        };

        const observer = new IntersectionObserver((entries) => {
            const now = latestIntersecting(entries);

            if (now === null) {
                return;
            }

            visible = now;
            root.dataset.visible = String(now);

            if (now) {
                load();
                resume();
            } else {
                pause();
            }
        });

        let loading = false;
        const urls: string[] = [];
        const load = () => {
            if (loading) {
                return;
            }

            loading = true;
            root.dataset.state = 'loading';

            const attach = (
                url: string,
                video: HTMLVideoElement,
                key: 'interest' | 'point',
            ) =>
                loadClip(url)
                    .then((objectUrl) => {
                        if (disposed) {
                            return;
                        }

                        urls.push(objectUrl);
                        video.src = objectUrl;
                        // Si ya había una oferta activa mientras cargaba, reacciona ahora.
                        video.addEventListener(
                            'loadeddata',
                            () => {
                                if (target && clip === 'rest') {
                                    react();
                                }
                            },
                            { once: true },
                        );
                        video.addEventListener('error', () => {
                            failed[key] = true;
                            root.dataset[`${key}Failed`] = 'true';

                            // Si falla el clip que se está viendo, vuelve el reposo.
                            if (clip === key) {
                                show('rest');
                            }
                        });
                    })
                    .catch(() => {
                        failed[key] = true;
                        root.dataset[`${key}Failed`] = 'true';
                    });

            void Promise.all([
                attach(HOST_MEDIA.interest, interestVideo, 'interest'),
                attach(HOST_MEDIA.point, pointVideo, 'point'),
            ]).then(() => {
                if (!disposed) {
                    root.dataset.state = 'ready';
                }
            });
        };

        interestVideo.addEventListener('ended', afterInterest);
        list.addEventListener('pointerover', onOver);
        list.addEventListener('pointerleave', onListLeave);
        list.addEventListener('focusin', onFocusIn);
        list.addEventListener('focusout', onFocusOut);
        window.addEventListener('scroll', onScroll, { passive: true });
        const inputs = [
            'wheel',
            'touchmove',
            'keydown',
            'pointerdown',
        ] as const;
        inputs.forEach((type) =>
            window.addEventListener(type, onUserInput, { passive: true }),
        );
        window.addEventListener('pointermove', onPointerMove, {
            passive: true,
        });
        document.documentElement.addEventListener('pointerleave', onPageLeave);
        document.addEventListener('visibilitychange', onVisibility);
        observer.observe(root);
        show('rest');
        root.dataset.zone = 'none';

        return () => {
            disposed = true;
            observer.disconnect();
            interestVideo.removeEventListener('ended', afterInterest);
            list.removeEventListener('pointerover', onOver);
            list.removeEventListener('pointerleave', onListLeave);
            list.removeEventListener('focusin', onFocusIn);
            list.removeEventListener('focusout', onFocusOut);
            window.removeEventListener('scroll', onScroll);
            inputs.forEach((type) =>
                window.removeEventListener(type, onUserInput),
            );
            window.removeEventListener('pointermove', onPointerMove);
            document.documentElement.removeEventListener(
                'pointerleave',
                onPageLeave,
            );
            document.removeEventListener('visibilitychange', onVisibility);
            window.clearTimeout(stepTimer);
            cancelAnimationFrame(tiltFrame);
            window.clearTimeout(idleTimer);
            window.clearTimeout(scrollTimer);
            target?.removeAttribute('data-anfitrion');
            interestVideo.pause();
            pointVideo.pause();
            interestVideo.removeAttribute('src');
            pointVideo.removeAttribute('src');
            tilt.style.transform = '';
            delete root.dataset.clip;
            delete root.dataset.zone;
            delete root.dataset.frame;
            delete root.dataset.target;
            delete root.dataset.state;
            delete root.dataset.visible;
        };
    }, [mode, listRef, itemSelector]);

    if (mode === 'off' || posterFailed) {
        return null;
    }

    return (
        <div
            ref={rootRef}
            aria-hidden="true"
            inert
            className={['job-host pointer-events-none select-none', className]
                .filter(Boolean)
                .join(' ')}
            data-cy="job-host"
            data-mode={mode}
            data-reason={reason}
        >
            <div ref={tiltRef} className="job-host-figure">
                <img
                    src={HOST_MEDIA.poster}
                    alt=""
                    decoding="async"
                    className="job-host-layer"
                    data-layer="rest"
                    onError={() => setPosterFailed(true)}
                />
                {mode === 'animated' ? (
                    <>
                        <video
                            ref={interestRef}
                            className="job-host-layer"
                            data-layer="interest"
                            muted
                            playsInline
                            preload="auto"
                            disablePictureInPicture
                            disableRemotePlayback
                            tabIndex={-1}
                        />
                        <video
                            ref={pointRef}
                            className="job-host-layer"
                            data-layer="point"
                            muted
                            playsInline
                            preload="auto"
                            disablePictureInPicture
                            disableRemotePlayback
                            tabIndex={-1}
                        />
                    </>
                ) : null}
            </div>
        </div>
    );
}
