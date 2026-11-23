import { useEffect, useRef, useState } from 'react';
import { latestIntersecting } from '@/lib/intersection';
import { useSceneCapability } from './use-scene-capability';

type ScrollVideoMedia = {
    video: string;
    poster: string;
    still?: string;
    frames: number;
    fps: number;
};

export const SCHOOL_MEDIA = {
    video: '/media/portada/portada-colegio.mp4',
    poster: '/media/portada/portada-colegio.webp',
    frames: 156,
    fps: 24,
} satisfies ScrollVideoMedia;

export const FOLDER_MEDIA = {
    video: '/media/portada/portada-carpeta.mp4',
    poster: '/media/portada/portada-carpeta-poster.webp',
    still: '/media/portada/portada-carpeta-abierta.webp',
    frames: 51,
    fps: 24,
} satisfies ScrollVideoMedia;

export function scrollProgress(distance: number, travel: number): number {
    return travel > 0 ? Math.min(1, Math.max(0, distance / travel)) : 0;
}

export function frameForProgress(progress: number, frames: number): number {
    return Math.round(Math.min(1, Math.max(0, progress)) * (frames - 1));
}

/** El instante central del fotograma: ningún redondeo muestra el vecino. */
export function timeForFrame(frame: number, fps: number): number {
    return (frame + 0.5) / fps;
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
export function createFrameSeeker(video: SeekableVideo, fps: number) {
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
        video.currentTime = timeForFrame(wanted, fps);
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

/** Capa decorativa compartida. El contenedor del recorrido conserva el scroll nativo. */
export function ScrollVideo({ media }: { media: ScrollVideoMedia }) {
    const rootRef = useRef<HTMLDivElement>(null);
    const videoRef = useRef<HTMLVideoElement>(null);
    const { mode, reason } = useSceneCapability();
    const [visible, setVisible] = useState(false);
    const [seen, setSeen] = useState(false);
    useEffect(() => {
        const section = rootRef.current?.closest('[data-video-track]');
        if (!section) return;
        const observer = new IntersectionObserver((entries) => {
            const inside = latestIntersecting(entries);
            if (inside !== null) setVisible(inside);
            if (inside) setSeen(true);
        });
        observer.observe(section);
        return () => observer.disconnect();
    }, []);
    const [videoFailed, setVideoFailed] = useState(false);
    const [stillFailed, setStillFailed] = useState(false);
    const [source, setSource] = useState<string | null>(null);
    const [ready, setReady] = useState(false);

    let kind: Kind = 'pending';
    if (reason !== 'server') {
        if (mode !== 'scene' || videoFailed) {
            kind = 'still';
        } else if (seen) {
            kind = 'video';
        }
    }

    // El clip se descarga entero y se sirve desde memoria: así se
    // puede buscar cualquier fotograma aunque el servidor no atienda
    // peticiones parciales (`php artisan serve` no lo hace). Solo en modo
    // vídeo; si no llega, queda la imagen fija.
    useEffect(() => {
        if (kind !== 'video') {
            return;
        }

        const controller = new AbortController();
        let url: string | null = null;

        fetch(media.video, { signal: controller.signal })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                return response.blob();
            })
            .then((blob) => {
                if (controller.signal.aborted) return;
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
    }, [kind, media.video]);

    useEffect(() => {
        const root = rootRef.current;
        const video = videoRef.current;

        if (kind !== 'video' || !visible || !source || !root || !video) {
            return;
        }

        const track = root.closest('[data-video-track]');
        if (!track) return;
        const stage = root.closest<HTMLElement>('[data-video-stage]') ?? root;
        const seeker = createFrameSeeker(video, media.fps);
        let frame = 0;

        const update = () => {
            frame = 0;
            const box = track.getBoundingClientRect();
            const stickyTop =
                Number.parseFloat(getComputedStyle(stage).top) || 0;
            const travel = Math.min(
                box.height - stage.clientHeight,
                window.innerHeight * 0.6,
            );
            const target = frameForProgress(
                scrollProgress(stickyTop - box.top, travel),
                media.frames,
            );

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
    }, [kind, media, source, visible]);

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
            className="scroll-video pointer-events-none select-none"
            data-cy="hero-video"
            data-mode={kind}
            data-reason={videoFailed ? 'video-error' : reason}
            data-state={state}
        >
            {kind === 'video' ? (
                <video
                    ref={videoRef}
                    className="absolute inset-0 size-full"
                    src={source ?? undefined}
                    poster={media.poster}
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
                    className="absolute inset-0 size-full"
                    src={media.still ?? media.poster}
                    alt=""
                    decoding="async"
                    onError={() => setStillFailed(true)}
                />
            ) : null}
        </div>
    );
}
