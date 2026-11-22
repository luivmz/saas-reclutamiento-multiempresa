import { useEffect, useRef, useState } from 'react';
import { useSceneCapability } from './use-scene-capability';

/**
 * La carpeta de la portada, en vídeo: se abre al bajar y se cierra al subir.
 *
 * El clip (generado con Higgsfield, sin texto, personas ni logotipos) son los
 * 51 fotogramas en que una carpeta pasa de cerrada a abierta. **No se
 * reproduce**: el desplazamiento de la página elige el fotograma. Lo que
 * garantiza este componente:
 *
 * 1. **Es decorativo**: `aria-hidden`, `inert`, sin controles ni foco. Todo lo
 *    que la portada dice está en el texto de al lado.
 * 2. **Solo se descarga cuando se usa**: escritorio de 1024 px o más, sin
 *    movimiento reducido, sin ahorro de datos ni equipo modesto
 *    (`useSceneCapability`, la misma regla que la escena de ADR-003). En los
 *    demás casos queda una imagen fija de la carpeta abierta y, si también
 *    falla, el fondo CSS del panel. Antes de decidir no se pide nada. El clip
 *    se descarga una vez y se sirve desde memoria (blob), para poder buscar
 *    cualquier fotograma aunque el servidor no atienda peticiones parciales.
 * 3. **El desplazamiento es el del navegador**: no se captura ni se suaviza el
 *    scroll; el vídeo solo busca fotogramas, a lo sumo una vez por cuadro.
 * 4. **Una búsqueda cada vez**: sin metadatos no se busca; mientras el vídeo
 *    busca, la posición siguiente espera y solo se aplica la última
 *    (`createFrameSeeker`).
 * 5. **Si el vídeo falla**, queda la imagen fija; si el movimiento reducido o
 *    el ancho cambian con la página abierta, también, y se retiran las
 *    escuchas.
 */
export const HERO_MEDIA = {
    video: '/media/portada/portada-carpeta.mp4',
    poster: '/media/portada/portada-carpeta-poster.webp',
    still: '/media/portada/portada-carpeta-abierta.webp',
} as const;

/** Fotogramas del clip (de cerrada a abierta) y su cadencia. */
export const CLIP_FRAMES = 51;
export const CLIP_FPS = 24;

/** Fracción de la altura de la portada que hay que desplazar para abrirla del todo. */
const OPEN_DISTANCE = 0.6;

/** 0 con la portada arriba del todo; 1 tras desplazar el 60 % de su altura. */
export function heroProgress(top: number, height: number): number {
    if (!(height > 0)) {
        return 0;
    }

    return Math.min(1, Math.max(0, -top / (height * OPEN_DISTANCE)));
}

export function frameForProgress(progress: number): number {
    return Math.round(Math.min(1, Math.max(0, progress)) * (CLIP_FRAMES - 1));
}

/** El instante central del fotograma: ningún redondeo muestra el vecino. */
export function timeForFrame(frame: number): number {
    return (frame + 0.5) / CLIP_FPS;
}

/** HTMLMediaElement.HAVE_METADATA, sin depender del DOM en las pruebas. */
const HAVE_METADATA = 1;

export type SeekableVideo = Pick<
    HTMLVideoElement,
    'currentTime' | 'seeking' | 'readyState'
> &
    Pick<EventTarget, 'addEventListener' | 'removeEventListener'>;

/**
 * Cola de una sola plaza para buscar fotogramas sin solapar búsquedas.
 *
 * - Sin metadatos no busca: espera a `loadedmetadata`.
 * - Mientras el vídeo busca (`seeking`), guarda solo el último fotograma
 *   pedido y lo aplica al terminar (`seeked`).
 * - No repite la búsqueda del fotograma que ya pidió.
 */
export function createFrameSeeker(video: SeekableVideo) {
    let wanted: number | null = null;
    let requested: number | null = null;
    let disposed = false;

    const pump = () => {
        if (
            disposed ||
            wanted === null ||
            wanted === requested ||
            video.readyState < HAVE_METADATA ||
            video.seeking
        ) {
            return;
        }

        requested = wanted;
        video.currentTime = timeForFrame(wanted);
    };

    video.addEventListener('loadedmetadata', pump);
    video.addEventListener('seeked', pump);

    return {
        request(frame: number) {
            wanted = frame;
            pump();
        },
        dispose() {
            disposed = true;
            video.removeEventListener('loadedmetadata', pump);
            video.removeEventListener('seeked', pump);
        },
    };
}

type Kind = 'pending' | 'video' | 'still';

export function HeroFolderVideo() {
    const rootRef = useRef<HTMLDivElement>(null);
    const videoRef = useRef<HTMLVideoElement>(null);
    const { mode, reason } = useSceneCapability();
    const [videoFailed, setVideoFailed] = useState(false);
    const [stillFailed, setStillFailed] = useState(false);
    const [source, setSource] = useState<string | null>(null);
    const [ready, setReady] = useState(false);

    const kind: Kind =
        reason === 'server'
            ? 'pending'
            : mode === 'scene' && !videoFailed
              ? 'video'
              : 'still';

    // El clip se descarga entero (700 kB) y se sirve desde memoria: así se
    // puede buscar cualquier fotograma aunque el servidor no atienda
    // peticiones parciales (`php artisan serve` no lo hace). Solo en modo
    // vídeo; si no llega, queda la imagen fija.
    useEffect(() => {
        if (kind !== 'video') {
            return;
        }

        const controller = new AbortController();
        let url: string | null = null;

        fetch(HERO_MEDIA.video, { signal: controller.signal })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                return response.blob();
            })
            .then((blob) => {
                url = URL.createObjectURL(blob);
                setSource(url);
            })
            .catch(() => {
                if (!controller.signal.aborted) {
                    setVideoFailed(true);
                }
            });

        return () => {
            controller.abort();
            setSource(null);
            setReady(false);

            if (url) {
                URL.revokeObjectURL(url);
            }
        };
    }, [kind]);

    useEffect(() => {
        const root = rootRef.current;
        const video = videoRef.current;

        if (kind !== 'video' || !source || !root || !video) {
            return;
        }

        const hero = root.closest('section') ?? root;
        const seeker = createFrameSeeker(video);
        let frame = 0;

        const update = () => {
            frame = 0;
            const box = hero.getBoundingClientRect();
            const target = frameForProgress(heroProgress(box.top, box.height));

            // Observable para las pruebas: el fotograma que pide el desplazamiento.
            root.dataset.frame = String(target);
            seeker.request(target);
        };
        const schedule = () => {
            if (!frame) {
                frame = requestAnimationFrame(update);
            }
        };
        const onData = () => setReady(true);

        if (video.readyState >= 2) {
            setReady(true);
        }

        video.addEventListener('loadeddata', onData);
        window.addEventListener('scroll', schedule, { passive: true });
        window.addEventListener('resize', schedule);
        update();

        return () => {
            cancelAnimationFrame(frame);
            window.removeEventListener('scroll', schedule);
            window.removeEventListener('resize', schedule);
            video.removeEventListener('loadeddata', onData);
            seeker.dispose();
        };
    }, [kind, source]);

    const state =
        kind === 'video'
            ? ready
                ? 'ready'
                : 'loading'
            : kind === 'still' && stillFailed
              ? 'css'
              : kind;

    return (
        <div
            ref={rootRef}
            aria-hidden="true"
            inert
            className="hero-folder relative aspect-[4/3] w-full overflow-hidden rounded-2xl border shadow-[0_28px_56px_-28px_oklch(0.2_0.04_220/0.55)] select-none"
            data-cy="hero-video"
            data-mode={kind}
            data-reason={videoFailed ? 'video-error' : reason}
            data-state={state}
        >
            {kind === 'video' ? (
                <video
                    ref={videoRef}
                    className="absolute inset-0 size-full object-cover object-right"
                    src={source ?? undefined}
                    poster={HERO_MEDIA.poster}
                    muted
                    playsInline
                    preload="auto"
                    disablePictureInPicture
                    disableRemotePlayback
                    tabIndex={-1}
                    onError={() => setVideoFailed(true)}
                />
            ) : null}
            {kind === 'still' && !stillFailed ? (
                <img
                    className="absolute inset-0 size-full object-cover object-right"
                    src={HERO_MEDIA.still}
                    alt=""
                    decoding="async"
                    onError={() => setStillFailed(true)}
                />
            ) : null}
        </div>
    );
}
