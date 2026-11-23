/**
 * E2E-23 · Portada: la carpeta en vídeo y la carpeta del proceso.
 *
 * Lo que solo un navegador puede comprobar:
 *
 * - el vídeo de la portada no se reproduce solo: avanza al bajar y retrocede
 *   al subir, una búsqueda cada vez;
 * - si el vídeo no llega, con movimiento reducido (al cargar o con la página
 *   abierta), en móvil o a 320 px, queda la imagen fija y no se pide el vídeo;
 * - el progreso se recupera al salir de la escena, recargar o volver de empleos;
 * - el texto y los accesos no dependen de nada de lo anterior, en los dos temas.
 *
 * Las capturas (`cy.screenshot`) son la evidencia visual del avance y del
 * retroceso; las aserciones no dependen de ellas.
 */
const VIDEO = 'portada-carpeta.mp4';
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

function videoPedido(win) {
    return win.performance
        .getEntriesByType('resource')
        .some((recurso) => recurso.name.includes(VIDEO));
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

            const portada = $video
                .closest('section')[0]
                .getBoundingClientRect();
            const progreso = Math.min(
                1,
                Math.max(
                    0,
                    (0.3 * video.ownerDocument.defaultView.innerHeight -
                        portada.top) /
                        (video.ownerDocument.defaultView.innerHeight * 0.6),
                ),
            );

            expect(
                pedido,
                'el fotograma que corresponde al desplazamiento',
            ).to.eq(Math.round(progreso * 50));
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
    cy.dataCy('landing-process').then(($section) => {
        const win = $section[0].ownerDocument.defaultView;
        const top = $section[0].getBoundingClientRect().top + win.scrollY;
        win.scrollTo(0, top + (0.6 * progreso - 0.3) * win.innerHeight);
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
            expect(c, 'abierta del todo').to.eq(50);
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

        recorrer(0.5);
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
            fotogramaAsentado().should('eq', 50);
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
        fotogramaAsentado().should('eq', 25);
        cy.reload();
        recorrer(0.5);
        fotogramaAsentado().should('eq', 25);
        cy.dataCy('landing-roles').scrollIntoView();
        recorrer(0.25);
        fotogramaAsentado().should('eq', 13);
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
});
