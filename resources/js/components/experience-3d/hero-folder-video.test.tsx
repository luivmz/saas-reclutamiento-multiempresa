import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    CLIP_FPS,
    CLIP_FRAMES,
    createFrameSeeker,
    frameForProgress,
    heroProgress,
    HeroFolderVideo,
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
    test('0 arriba del todo, 1 tras desplazar el 60 % de la portada, sin salirse', () => {
        expect(heroProgress(0, 800)).toBe(0);
        expect(heroProgress(120, 800)).toBe(0);
        expect(heroProgress(-240, 800)).toBeCloseTo(0.5);
        expect(heroProgress(-480, 800)).toBe(1);
        expect(heroProgress(-5000, 800)).toBe(1);
        expect(heroProgress(-100, 0)).toBe(0);
    });

    test('cada progreso cae en un fotograma del clip, y cada fotograma en su centro', () => {
        expect(frameForProgress(0)).toBe(0);
        expect(frameForProgress(1)).toBe(CLIP_FRAMES - 1);
        expect(frameForProgress(-1)).toBe(0);
        expect(frameForProgress(2)).toBe(CLIP_FRAMES - 1);

        for (let frame = 0; frame < CLIP_FRAMES; frame++) {
            const time = timeForFrame(frame);

            expect(time).toBeGreaterThan(frame / CLIP_FPS);
            expect(time).toBeLessThan((frame + 1) / CLIP_FPS);
        }
    });
});

describe('Búsquedas sin solaparse', () => {
    test('sin metadatos no busca; al llegar, aplica solo el último fotograma pedido', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video);

        seeker.request(3);
        seeker.request(9);
        expect(video.sets).toEqual([]);

        video.loadMetadata();
        expect(video.sets).toEqual([timeForFrame(9)]);
        seeker.dispose();
    });

    test('mientras busca, guarda solo la última posición y la aplica al terminar', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video);

        video.loadMetadata();
        seeker.request(5);
        seeker.request(12);
        seeker.request(20);
        seeker.request(31);
        expect(video.sets).toEqual([timeForFrame(5)]);

        video.finishSeek();
        expect(video.sets).toEqual([timeForFrame(5), timeForFrame(31)]);

        // Hacia atrás también: retroceder al subir es otra búsqueda más.
        video.finishSeek();
        seeker.request(2);
        expect(video.sets.at(-1)).toBe(timeForFrame(2));
        expect(video.overlapping).toBe(0);
        seeker.dispose();
    });

    test('no repite la búsqueda del fotograma que ya pidió', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video);

        video.loadMetadata();
        seeker.request(7);
        video.finishSeek();
        seeker.request(7);
        seeker.request(7);
        expect(video.sets).toEqual([timeForFrame(7)]);
        seeker.dispose();
    });

    test('tras retirarlo, ningún evento posterior vuelve a buscar', () => {
        const video = new FakeVideo();
        const seeker = createFrameSeeker(video);

        video.loadMetadata();
        seeker.request(4);
        seeker.request(8);
        seeker.dispose();
        video.finishSeek();
        video.loadMetadata();
        expect(video.sets).toEqual([timeForFrame(4)]);
    });
});

describe('Antes de decidir', () => {
    test('el panel es decorativo y no pide ni el vídeo ni la imagen', () => {
        const markup = renderToStaticMarkup(<HeroFolderVideo />);

        expect(markup).toContain('data-cy="hero-video"');
        expect(markup).toContain('aria-hidden="true"');
        expect(markup).toContain('inert');
        expect(markup).toContain('data-mode="pending"');
        expect(markup).not.toContain('<video');
        expect(markup).not.toContain('<img');
    });
});
