import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    FOLDER_MEDIA,
    SCHOOL_MEDIA,
    createFrameSeeker,
    frameForProgress,
    scrollProgress,
    ScrollVideo,
    timeForFrame,
} from './hero-folder-video';

/**
 * El vídeo de la carpeta de la portada: lo que no depende del navegador. Las
 * búsquedas se prueban contra un vídeo simulado que cuenta las que se solapan;
 * el desplazamiento real, el fallo de red y el movimiento reducido, en
 * `e2e-23`.
 */
class FakeVideo extends EventTarget {
    readyState = 0;
    seeking = false;
    sets: number[] = [];
    overlapping = 0;
    private time = 0;

    get currentTime() {
        return this.time;
    }

    set currentTime(value: number) {
        if (this.seeking) {
            this.overlapping++;
        }

        this.sets.push(value);
        this.time = value;
        this.seeking = true;
    }

    loadMetadata() {
        this.readyState = 1;
        this.dispatchEvent(new Event('loadedmetadata'));
    }

    finishSeek() {
        this.seeking = false;
        this.dispatchEvent(new Event('seeked'));
    }
}

describe('Progreso y fotogramas', () => {
    test('limita el progreso al recorrido del fondo', () => {
        expect(scrollProgress(-20, 480)).toBe(0);
        expect(scrollProgress(0, 480)).toBe(0);
        expect(scrollProgress(240, 480)).toBe(0.5);
        expect(scrollProgress(480, 480)).toBe(1);
        expect(scrollProgress(5000, 480)).toBe(1);
        expect(scrollProgress(100, 0)).toBe(0);
    });

    test.each([SCHOOL_MEDIA, FOLDER_MEDIA])(
        'elige los fotogramas del clip $video',
        ({ frames, fps }) => {
            expect(frameForProgress(0, frames)).toBe(0);
            expect(frameForProgress(1, frames)).toBe(frames - 1);
            expect(frameForProgress(-1, frames)).toBe(0);
            expect(frameForProgress(2, frames)).toBe(frames - 1);

            for (let frame = 0; frame < frames; frame++) {
                const time = timeForFrame(frame, fps);

                expect(time).toBeGreaterThan(frame / fps);
                expect(time).toBeLessThan((frame + 1) / fps);
            }
        },
    );
});

describe('Búsquedas sin solaparse', () => {
    test('sin metadatos no busca; al llegar, aplica solo el último fotograma pedido', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video, FOLDER_MEDIA.fps);

        seeker.request(3);
        seeker.request(9);
        expect(video.sets).toEqual([]);

        video.loadMetadata();
        expect(video.sets).toEqual([timeForFrame(9, FOLDER_MEDIA.fps)]);
        seeker.dispose();
    });

    test('mientras busca, guarda solo la última posición y la aplica al terminar', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video, FOLDER_MEDIA.fps);

        video.loadMetadata();
        seeker.request(5);
        seeker.request(12);
        seeker.request(20);
        seeker.request(31);
        expect(video.sets).toEqual([timeForFrame(5, FOLDER_MEDIA.fps)]);

        video.finishSeek();
        expect(video.sets).toEqual([
            timeForFrame(5, FOLDER_MEDIA.fps),
            timeForFrame(31, FOLDER_MEDIA.fps),
        ]);

        // Hacia atrás también: retroceder al subir es otra búsqueda más.
        video.finishSeek();
        seeker.request(2);
        expect(video.sets.at(-1)).toBe(timeForFrame(2, FOLDER_MEDIA.fps));
        expect(video.overlapping).toBe(0);
        seeker.dispose();
    });

    test('no repite la búsqueda del fotograma que ya pidió', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video, FOLDER_MEDIA.fps);

        video.loadMetadata();
        seeker.request(7);
        video.finishSeek();
        seeker.request(7);
        seeker.request(7);
        expect(video.sets).toEqual([timeForFrame(7, FOLDER_MEDIA.fps)]);
        seeker.dispose();
    });

    test('tras retirarlo, ningún evento posterior vuelve a buscar', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video, FOLDER_MEDIA.fps);

        video.loadMetadata();
        seeker.request(4);
        seeker.request(8);
        seeker.dispose();
        video.finishSeek();
        video.loadMetadata();
        expect(video.sets).toEqual([timeForFrame(4, FOLDER_MEDIA.fps)]);
    });
});

describe('Antes de decidir', () => {
    test('el panel es decorativo y no pide ni el vídeo ni la imagen', () => {
        const markup = renderToStaticMarkup(
            <ScrollVideo media={SCHOOL_MEDIA} />,
        );

        expect(markup).toContain('data-cy="hero-video"');
        expect(markup).toContain('aria-hidden="true"');
        expect(markup).toContain('inert');
        expect(markup).toContain('data-mode="pending"');
        expect(markup).not.toContain('<video');
        expect(markup).not.toContain('<img');
    });
});
