/** E2E-23 · Los vídeos de la portada y el detalle público. */
const VIDEO = 'portada-colegio.mp4';
const JOB_VIDEO = 'portada-carpeta.mp4';
const FPS = 24;

function reducido(activo) {
    return Cypress.automation('remote:debugger:protocol', {
        command: 'Emulation.setEmulatedMedia',
        params: {
            features: activo
                ? [{ name: 'prefers-reduced-motion', value: 'reduce' }]
                : [],
        },
    });
}

function videoPedido(win, video = VIDEO) {
    return win.performance
        .getEntriesByType('resource')
        .some((recurso) => recurso.name.includes(video));
}

/** Cuenta las búsquedas, las que llegan con otra en curso y las reproducciones. */
function vigilarVideo(win) {
    const proto = win.HTMLMediaElement.prototype;
    const original = Object.getOwnPropertyDescriptor(proto, 'currentTime');
    const play = proto.play;

    win.__video = { busquedas: 0, solapadas: 0, reproducciones: 0 };
    Object.defineProperty(proto, 'currentTime', {
        configurable: true,
        get() {
            return original.get.call(this);
        },
        set(valor) {
            win.__video.busquedas++;

            if (this.seeking) {
                win.__video.solapadas++;
            }

            original.set.call(this, valor);
        },
    });
    proto.play = function () {
        win.__video.reproducciones++;

        return play.call(this);
    };
}

function sinDesborde() {
    cy.document().then((doc) => {
        expect(
            doc.documentElement.scrollWidth - doc.documentElement.clientWidth,
        ).to.be.lessThan(2);
    });
}

function portadaUtilizable() {
    cy.get('h1').should('be.visible');
    cy.dataCy('cta-jobs').should('be.visible').and('have.attr', 'href');
    cy.dataCy('cta-login').should('be.visible');
}

function desplazar(y) {
    cy.window().then((win) => win.scrollTo(0, y));
}

/** Espera a que el vídeo muestre el fotograma pedido y devuelve ese fotograma. */
function fotogramaAsentado() {
    return cy
        .dataCy('hero-video')
        .find('video')
        .should(($video) => {
            const video = $video[0];
            const pedido = Number(
                $video.closest('[data-cy="hero-video"]').attr('data-frame'),
            );

            const layer = video.parentElement;
            const win = layer.ownerDocument.defaultView;
            const box = layer
                .closest('[data-video-track]')
                .getBoundingClientRect();
            const stage = layer.closest('[data-video-stage]') ?? layer;
            const stickyTop = Number.parseFloat(
                win.getComputedStyle(stage).top,
            );
            const travel = Math.min(
                box.height - stage.clientHeight,
                win.innerHeight * 0.6,
            );
            const frameCount = Math.round(video.duration * FPS);
            const progress = Math.max(
                0,
                Math.min(1, (stickyTop - box.top) / travel),
            );
            expect(pedido, 'fotograma de la posición actual').to.eq(
                Math.round(progress * (frameCount - 1)),
            );
            expect(video.seeking, 'sin búsqueda en curso').to.eq(false);
            expect(
                Math.abs(video.currentTime - (pedido + 0.5) / FPS),
                'muestra el fotograma pedido',
            ).to.be.lessThan(0.01);
        })
        .then(($video) =>
            Number($video.closest('[data-cy="hero-video"]').attr('data-frame')),
        );
}

function imagenFija(razon) {
    cy.dataCy('hero-video')
        .should('have.attr', 'data-mode', 'still')
        .and('have.attr', 'data-reason', razon);
    cy.dataCy('hero-video').find('video').should('not.exist');
    cy.dataCy('hero-video')
        .find('img')
        .should(($img) =>
            expect($img[0].naturalWidth, 'imagen cargada').to.be.greaterThan(0),
        );
}

// Posición relativa al comienzo y al final de la apertura.
function recorrer(progreso) {
    cy.dataCy('hero-video')
        .should(($layer) => {
            const layer = $layer[0];
            const track = layer.closest('[data-video-track]');
            if (track.getBoundingClientRect().bottom <= 0) {
                track.scrollIntoView();
            }
            expect(layer.dataset.state).to.eq('ready');
        })
        .then(($layer) => {
            const layer = $layer[0];
            const win = layer.ownerDocument.defaultView;
            const box = layer
                .closest('[data-video-track]')
                .getBoundingClientRect();
            const stage = layer.closest('[data-video-stage]') ?? layer;
            const stickyTop = Number.parseFloat(
                win.getComputedStyle(stage).top,
            );
            const travel = Math.min(
                box.height - stage.clientHeight,
                win.innerHeight * 0.6,
            );
            win.scrollTo(
                0,
                Math.ceil(
                    win.scrollY + box.top - stickyTop + travel * progreso,
                ),
            );
        });
}

describe('E2E-23 · Portada: la carpeta en vídeo y la carpeta del proceso', () => {
    afterEach(() => reducido(false));

    it('el vídeo avanza al bajar y retrocede al subir, sin reproducirse solo ni solapar búsquedas', () => {
        cy.viewport(1280, 800);
        cy.visit('/', { onBeforeLoad: vigilarVideo });
        recorrer(0);

        cy.dataCy('hero-video')
            .should('have.attr', 'data-mode', 'video')
            .and('have.attr', 'data-state', 'ready');
        fotogramaAsentado().should('eq', 0);
        cy.screenshot('e2e23-video-1-arriba', { capture: 'viewport' });

        const vistos = [];

        [0.25, 0.5, 1].forEach((y, paso) => {
            recorrer(y);
            fotogramaAsentado().then((fotograma) => vistos.push(fotograma));
            cy.screenshot(`e2e23-video-${paso + 2}-bajando-${y}`, {
                capture: 'viewport',
            });
        });
        [0.5, 0].forEach((y, paso) => {
            recorrer(y);
            fotogramaAsentado().then((fotograma) => vistos.push(fotograma));
            cy.screenshot(`e2e23-video-${paso + 5}-subiendo-${y}`, {
                capture: 'viewport',
            });
        });

        cy.then(() => {
            const [a, b, c, d, e] = vistos;

            expect(a, 'baja').to.be.greaterThan(0);
            expect(b, 'sigue bajando').to.be.greaterThan(a);
            expect(c, 'abierta del todo').to.eq(155);
            expect(d, 'al subir retrocede').to.be.lessThan(c);
            expect(d, 'mismo sitio, mismo fotograma').to.eq(b);
            expect(e, 'arriba, cerrada').to.eq(0);
        });
        cy.window().then((win) => {
            expect(win.__video.busquedas, 'hubo búsquedas').to.be.greaterThan(
                0,
            );
            expect(win.__video.solapadas, 'búsquedas solapadas').to.eq(0);
            expect(win.__video.reproducciones, 'reproducciones').to.eq(0);
        });
        cy.dataCy('hero-video')
            .find('video')
            .should(($video) => expect($video[0].paused).to.eq(true));
        portadaUtilizable();
        sinDesborde();
    });

    it('si el vídeo no llega, queda la imagen fija y la portada sigue entera', () => {
        cy.intercept('GET', `**/${VIDEO}`, { statusCode: 404, body: '' });
        cy.viewport(1280, 800);
        cy.visit('/');

        imagenFija('video-error');
        portadaUtilizable();
        cy.screenshot('e2e23-video-fallido', { capture: 'viewport' });
    });

    it('con movimiento reducido al cargar: imagen fija y el vídeo no se pide', () => {
        reducido(true);
        cy.viewport(1280, 800);
        cy.visit('/');

        imagenFija('reduced-motion');
        cy.window().then((win) =>
            expect(videoPedido(win), 'vídeo pedido').to.eq(false),
        );
        portadaUtilizable();
    });

    it('si el movimiento reducido se activa con la página abierta, el vídeo cede a la imagen fija', () => {
        cy.viewport(1280, 800);
        cy.visit('/');
        recorrer(0);
        cy.dataCy('hero-video')
            .should('have.attr', 'data-mode', 'video')
            .and('have.attr', 'data-state', 'ready');

        // En la cola de Cypress: se activa con la página ya abierta.
        cy.then(() => reducido(true));
        imagenFija('reduced-motion');
        desplazar(300);
        desplazar(0);
        portadaUtilizable();
    });

    [
        [390, 844],
        [320, 640],
    ].forEach(([ancho, alto]) => {
        it(`a ${ancho} px: imagen fija, sin pedir el vídeo y sin desbordar`, () => {
            cy.viewport(ancho, alto);
            cy.visit('/');

            imagenFija('small-viewport');
            cy.window().then((win) =>
                expect(videoPedido(win), 'vídeo pedido').to.eq(false),
            );
            portadaUtilizable();
            sinDesborde();
            cy.screenshot(`e2e23-movil-${ancho}`, { capture: 'viewport' });
            cy.dataCy('landing-folder').scrollIntoView();
            cy.dataCy('recruitment-depth').should(
                'have.attr',
                'data-mode',
                'poster',
            );
            cy.contains('REQ-2026-0042').should('be.visible');
            sinDesborde();
            cy.screenshot(`e2e23-movil-${ancho}-carpeta`, {
                capture: 'viewport',
            });
        });
    });

    ['light', 'dark'].forEach((tema) => {
        it(`en tema ${tema === 'light' ? 'claro' : 'oscuro'}, el texto y los accesos se leen igual`, () => {
            cy.viewport(1280, 800);
            cy.visit('/', {
                onBeforeLoad(win) {
                    win.localStorage.setItem('appearance', tema);
                },
            });

            cy.get('html').should(
                tema === 'dark' ? 'have.class' : 'not.have.class',
                'dark',
            );

            portadaUtilizable();
            cy.screenshot(`e2e23-tema-${tema}-portada`, {
                capture: 'viewport',
            });
            recorrer(1);
            fotogramaAsentado().should('eq', 155);
            cy.get('.school-stage').should(($stage) => {
                expect($stage[0].getBoundingClientRect().top).to.be.closeTo(
                    Number.parseFloat(
                        $stage[0].ownerDocument.defaultView.getComputedStyle(
                            $stage[0],
                        ).top,
                    ),
                    1,
                );
            });
            cy.dataCy('landing-folder').scrollIntoView();
            cy.dataCy('recruitment-scene').should(
                'have.attr',
                'data-ready',
                'true',
            );
            cy.screenshot(`e2e23-tema-${tema}-carpeta`, {
                capture: 'viewport',
            });
        });
    });

    it('la escena recupera el progreso tras salir, recargar y volver de empleos', () => {
        cy.viewport(1280, 800);
        cy.visit('/');
        recorrer(0.5);
        fotogramaAsentado().should('eq', 78);
        cy.reload();
        recorrer(0.5);
        fotogramaAsentado().should('eq', 78);
        cy.dataCy('landing-roles').scrollIntoView();
        recorrer(0.25);
        fotogramaAsentado().should('eq', 39);
        cy.dataCy('cta-jobs').click();
        cy.location('pathname').should('eq', '/empleos');
        cy.go('back');
        recorrer(0);
        fotogramaAsentado().should('eq', 0);
    });

    it('la carpeta del proceso con movimiento reducido: estática y legible', () => {
        reducido(true);
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.dataCy('landing-folder').scrollIntoView();
        cy.dataCy('recruitment-depth')
            .should('have.attr', 'data-mode', 'poster')
            .and('have.attr', 'data-reason', 'reduced-motion');
        cy.dataCy('recruitment-scene').should('not.exist');
        cy.contains('REQ-2026-0042').should('be.visible');
        cy.screenshot('e2e23-carpeta-movimiento-reducido', {
            capture: 'viewport',
        });
    });
    ['light', 'dark'].forEach((tema, index) => {
        it(`en una oferta distinta en tema ${tema}, la carpeta acompaña al contenido`, () => {
            cy.viewport(1280, 800);
            cy.visit('/empleos', {
                onBeforeLoad(win) {
                    vigilarVideo(win);
                    win.localStorage.setItem('appearance', tema);
                },
            });
            cy.dataCy('job-detail-link')
                .eq(index)
                .then(($link) => {
                    const nombre = $link.text().trim();
                    cy.wrap($link).click();
                    cy.dataCy('page-title').should('have.text', nombre);
                });
            cy.dataCy('hero-video')
                .should('have.css', 'opacity', '0.2')
                .and('have.attr', 'inert');
            cy.dataCy('hero-video')
                .find('video')
                .should('not.have.attr', 'controls');
            cy.contains('La convocatoria').should('be.visible');
            cy.contains('Perfil del puesto').should('be.visible');
            cy.contains('Criterios de evaluación').should('be.visible');
            cy.contains('REQ-2026-0042').should('not.exist');
            recorrer(0);
            fotogramaAsentado().should('eq', 0);
            cy.screenshot(`oferta-${tema}-inicio`, { capture: 'viewport' });
            recorrer(1);
            fotogramaAsentado().should('eq', 50);
            cy.screenshot(`oferta-${tema}-apertura`, { capture: 'viewport' });
            recorrer(0);
            fotogramaAsentado().should('eq', 0);
            cy.dataCy('apply-login')
                .focus()
                .should('be.focused')
                .and('have.attr', 'href', '/login');
            cy.dataCy('apply-register').should('be.visible');
            cy.window().then((win) => {
                expect(win.__video.solapadas).to.eq(0);
                expect(win.__video.reproducciones).to.eq(0);
                expect(videoPedido(win, JOB_VIDEO)).to.eq(true);
                expect(videoPedido(win)).to.eq(false);
            });
            cy.then(() => reducido(true));
            imagenFija('reduced-motion');
            cy.dataCy('hero-video').should(
                'not.have.css',
                'position',
                'sticky',
            );
        });
    });

    it('el detalle conserva sus acciones en móvil y ante un fallo del vídeo', () => {
        cy.viewport(320, 640);
        cy.visit('/empleos');
        cy.dataCy('job-detail-link').first().click();
        imagenFija('small-viewport');
        sinDesborde();
        cy.window().then((win) =>
            expect(videoPedido(win, JOB_VIDEO)).to.eq(false),
        );
        cy.dataCy('apply-register').scrollIntoView().should('be.visible');
        cy.screenshot('oferta-320-acciones', { capture: 'viewport' });
        cy.intercept('GET', `**/${JOB_VIDEO}`, { statusCode: 404, body: '' });
        cy.viewport(1280, 800);
        cy.reload();
        imagenFija('video-error');
        cy.dataCy('apply-login').should('be.visible');
    });
});
