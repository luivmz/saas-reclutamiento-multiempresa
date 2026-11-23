/**
 * E2E-24 · Anfitrión del listado público de empleos.
 *
 * Un personaje decorativo acompaña la exploración de las ofertas desde la
 * derecha. Lo que se comprueba aquí:
 *
 * - reposo, interés al entrar en una oferta (cursor o teclado), señalar hacia
 *   la oferta activa y vuelta al reposo, con la oferta activa resaltada;
 * - pasar deprisa entre tarjetas no acumula reproducciones ni búsquedas;
 * - al desplazarse, atiende a la oferta más cercana al centro;
 * - es decorativo: oculto al lector de pantalla, inerte, sin tapar nada;
 * - póster estático con movimiento reducido (al cargar y con la página
 *   abierta) y sin puntero fino, sin descargar los clips;
 * - sin anfitrión ni descargas en anchos estrechos, sin desbordar;
 * - si falla un clip o el póster, el listado sigue igual;
 * - búsqueda, ida a una oferta y regreso.
 *
 * Electron sin pantalla no tiene ratón: donde hace falta se declara un puntero
 * fino, como en un escritorio. Los gestos son clips pregrabados: se comprueba
 * qué clip y qué zona elige, no la anatomía del personaje.
 *
 * Las capturas van al final de cada prueba: en Electron, después de
 * `cy.screenshot`, requestAnimationFrame baja a cerca de un cuadro por segundo
 * y el recorrido del gesto se ralentiza (en Chrome no ocurre).
 */
const CLIPS = ['anfitrion-interes.webm', 'anfitrion-senala.webm'];

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

/** Declara si hay un puntero fino con hover (ratón) o no (pantalla táctil). */
function punteroFino(win, hay) {
    const original = win.matchMedia.bind(win);

    win.matchMedia = (query) =>
        query.includes('hover: hover')
            ? {
                  matches: hay,
                  media: query,
                  addEventListener() {},
                  removeEventListener() {},
              }
            : original(query);
}

/** Cuenta reproducciones y búsquedas, y las que llegan con otra búsqueda en curso. */
function vigilar(win) {
    const proto = win.HTMLMediaElement.prototype;
    const original = Object.getOwnPropertyDescriptor(proto, 'currentTime');
    const play = proto.play;

    win.__anfitrion = { reproducciones: 0, busquedas: 0, solapadas: 0 };
    Object.defineProperty(proto, 'currentTime', {
        configurable: true,
        get() {
            return original.get.call(this);
        },
        set(valor) {
            win.__anfitrion.busquedas++;

            if (this.seeking) {
                win.__anfitrion.solapadas++;
            }

            original.set.call(this, valor);
        },
    });
    proto.play = function () {
        win.__anfitrion.reproducciones++;

        return play.call(this);
    };
}

function escritorio(win) {
    vigilar(win);
    punteroFino(win, true);
}

function pedidos(win, nombres) {
    return win.performance
        .getEntriesByType('resource')
        .filter((recurso) => nombres.some((n) => recurso.name.includes(n)))
        .map((recurso) => recurso.name.split('/').pop());
}

function sinDesborde() {
    cy.document().then((doc) => {
        expect(
            doc.documentElement.scrollWidth - doc.documentElement.clientWidth,
        ).to.be.lessThan(2);
    });
}

function anfitrionListo() {
    cy.dataCy('job-host')
        .should('have.attr', 'data-mode', 'animated')
        .and('have.attr', 'data-state', 'ready')
        .and('have.attr', 'data-clip', 'rest');
    // Los dos clips con su primer fotograma decodificado.
    cy.dataCy('job-host')
        .find('video')
        .should('have.length', 2)
        .each(($video) =>
            cy
                .wrap($video)
                .should(($v) => expect($v[0].readyState).to.be.at.least(2)),
        );
}

/**
 * El cursor entra en una oferta, sin que Cypress desplace antes la página: un
 * desplazamiento haría de esa oferta el objetivo «por scroll», que no reacciona.
 */
function entrar(indice) {
    cy.dataCy('job-card')
        .eq(indice)
        .trigger('pointerover', { scrollBehavior: false });
}

/**
 * Marca el anfitrión actual y espera a que Inertia lo sustituya por el de la
 * página nueva (cada visita vuelve a montar la página).
 */
function marcarAnfitrion() {
    cy.dataCy('job-host').then(($host) => {
        $host[0].__anterior = true;
    });
}

function anfitrionRemontado() {
    cy.dataCy('job-host').should(($host) => {
        expect($host).to.have.length(1);
        expect($host[0].__anterior, 'anfitrión nuevo').to.eq(undefined);
    });
}

/** Desplazamiento hecho por la persona: la rueda precede al scroll. */
function desplazarComoPersona(y) {
    cy.window().then((win) => {
        win.dispatchEvent(new win.WheelEvent('wheel', { deltaY: 100 }));
        win.scrollTo(0, y);
    });
}

function listado() {
    return cy.dataCy('jobs-list').parent();
}

describe('E2E-24 · Anfitrión del listado de empleos', () => {
    before(() => cy.resetDatabase());

    afterEach(() => reducido(false));

    it('reposo, interés al entrar en una oferta, señala hacia ella y vuelve al reposo', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();
        cy.dataCy('job-host').should('have.attr', 'data-reason', 'ok');
        cy.get('[data-anfitrion]').should('not.exist');

        entrar(0);
        cy.dataCy('job-host').should('have.attr', 'data-clip', 'interest');
        cy.dataCy('job-card')
            .eq(0)
            .should('have.attr', 'data-anfitrion', 'activa')
            .invoke('attr', 'data-code')
            .then((codigo) =>
                cy
                    .dataCy('job-host')
                    .should('have.attr', 'data-target', codigo),
            );

        // Al terminar la reacción (4 s), señala hacia la oferta activa.
        cy.dataCy('job-host', { timeout: 8000 })
            .should('have.attr', 'data-clip', 'point')
            .and(($h) =>
                expect($h.attr('data-zone')).to.be.oneOf(['up', 'mid', 'down']),
            );
        cy.dataCy('job-host').should(($h) =>
            expect(['27', '48', '78', '60']).to.include($h.attr('data-frame')),
        );

        listado().trigger('pointerleave');
        cy.dataCy('job-host', { timeout: 6000 }).should(
            'have.attr',
            'data-clip',
            'rest',
        );
        cy.get('[data-anfitrion]').should('not.exist');
        cy.window().then((win) => {
            expect(win.__anfitrion.reproducciones, 'reproducciones').to.eq(1);
            expect(win.__anfitrion.solapadas, 'búsquedas solapadas').to.eq(0);
        });
        cy.screenshot('e2e24-1-reposo', { capture: 'viewport' });
    });

    it('pasar deprisa entre tarjetas no acumula reacciones: manda la última', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();

        [0, 1, 2, 0, 1, 2, 1].forEach((indice) => {
            entrar(indice);
            cy.wait(40);
        });
        cy.dataCy('job-card')
            .eq(1)
            .should('have.attr', 'data-anfitrion', 'activa');
        cy.get('[data-anfitrion]').should('have.length', 1);
        cy.dataCy('job-host', { timeout: 8000 }).should(
            'have.attr',
            'data-clip',
            'point',
        );
        cy.window().then((win) => {
            expect(win.__anfitrion.reproducciones, 'una sola reacción').to.eq(
                1,
            );
            expect(win.__anfitrion.solapadas, 'búsquedas solapadas').to.eq(0);
        });
    });

    it('el foco por teclado en el enlace de una oferta produce la misma reacción', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();

        cy.dataCy('job-detail-link').eq(1).focus();
        cy.dataCy('job-host').should('have.attr', 'data-clip', 'interest');
        cy.dataCy('job-card')
            .eq(1)
            .should('have.attr', 'data-anfitrion', 'activa');
        cy.screenshot('e2e24-4-foco-teclado', { capture: 'viewport' });

        cy.dataCy('job-detail-link').eq(1).blur();
        cy.dataCy('job-host', { timeout: 6000 }).should(
            'have.attr',
            'data-clip',
            'rest',
        );
        cy.get('[data-anfitrion]').should('not.exist');
    });

    it('al desplazarse atiende a la oferta más cercana al centro, y después reposa', () => {
        cy.viewport(1280, 640);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();

        // Un desplazamiento programático no elige oferta.
        cy.scrollTo(0, 320);
        cy.wait(300);
        cy.dataCy('job-host').should('have.attr', 'data-clip', 'rest');
        cy.scrollTo(0, 0);

        desplazarComoPersona(320);
        cy.dataCy('job-host')
            .should('have.attr', 'data-clip', 'point')
            .and(($h) => expect($h.attr('data-target')).not.to.eq(''));
        cy.get('[data-anfitrion="activa"]').should('have.length', 1);
        desplazarComoPersona(0);
        cy.dataCy('job-host', { timeout: 8000 }).should(
            'have.attr',
            'data-clip',
            'rest',
        );
        cy.get('[data-anfitrion]').should('not.exist');
    });

    it('es decorativo: oculto, inerte, sin tapar ofertas ni enlaces', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();

        cy.dataCy('job-host')
            .should('have.attr', 'aria-hidden', 'true')
            .and('have.css', 'pointer-events', 'none');
        cy.dataCy('job-host').should('have.attr', 'inert');
        cy.dataCy('job-host')
            .find('a, button, input, [tabindex]:not([tabindex="-1"])')
            .should('not.exist');
        cy.dataCy('job-host').then(($host) => {
            const anfitrion = $host[0].getBoundingClientRect();

            cy.dataCy('job-card').each(($card) => {
                const tarjeta = $card[0].getBoundingClientRect();

                expect(
                    tarjeta.right <= anfitrion.left ||
                        tarjeta.left >= anfitrion.right ||
                        tarjeta.bottom <= anfitrion.top ||
                        tarjeta.top >= anfitrion.bottom,
                    'no se solapa con ninguna oferta',
                ).to.eq(true);
            });
        });
        sinDesborde();
    });

    it('con movimiento reducido al cargar: póster y sin descargar los clips', () => {
        reducido(true);
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });

        cy.dataCy('job-host')
            .should('have.attr', 'data-mode', 'static')
            .and('have.attr', 'data-reason', 'reduced-motion');
        cy.dataCy('job-host').find('video').should('not.exist');
        cy.dataCy('job-host')
            .find('img')
            .should(($img) =>
                expect($img[0].naturalWidth).to.be.greaterThan(0),
            );
        entrar(0);
        cy.get('[data-anfitrion]').should('not.exist');
        cy.window().then((win) => expect(pedidos(win, CLIPS)).to.deep.eq([]));
        cy.screenshot('e2e24-7-movimiento-reducido', { capture: 'viewport' });
    });

    it('si el movimiento reducido se activa con la página abierta, vuelve al póster y suelta los clips', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();
        entrar(0);
        cy.dataCy('job-card')
            .eq(0)
            .should('have.attr', 'data-anfitrion', 'activa');

        cy.then(() => reducido(true));
        cy.dataCy('job-host')
            .should('have.attr', 'data-mode', 'static')
            .and('not.have.attr', 'data-clip');
        cy.dataCy('job-host').find('video').should('not.exist');
        cy.get('[data-anfitrion]').should('not.exist');
        cy.dataCy('job-host')
            .find('[data-layer="rest"]')
            .should('have.css', 'opacity', '1');
    });

    it('sin puntero fino (pantalla táctil): póster discreto y sin clips', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', {
            onBeforeLoad: (win) => punteroFino(win, false),
        });

        cy.dataCy('job-host')
            .should('have.attr', 'data-mode', 'static')
            .and('have.attr', 'data-reason', 'coarse-pointer');
        cy.dataCy('job-host').find('video').should('not.exist');
        cy.window().then((win) => expect(pedidos(win, CLIPS)).to.deep.eq([]));
    });

    [
        [320, 640],
        [1024, 768],
    ].forEach(([ancho, alto]) => {
        it(`a ${ancho} px no hay anfitrión ni descargas, y nada desborda`, () => {
            cy.viewport(ancho, alto);
            cy.visit('/empleos', { onBeforeLoad: escritorio });

            cy.dataCy('job-card').should('have.length.at.least', 1);
            cy.dataCy('job-host').should('not.exist');
            cy.window().then((win) =>
                expect(
                    pedidos(win, [...CLIPS, 'anfitrion-reposo.webp']),
                ).to.deep.eq([]),
            );
            sinDesborde();
            cy.screenshot(`e2e24-8-${ancho}`, { capture: 'viewport' });
        });
    });

    it('si falla un clip, prescinde de él; el listado sigue entero', () => {
        cy.intercept('GET', '**/anfitrion-interes.webm', {
            statusCode: 404,
            body: '',
        });
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });

        cy.dataCy('job-host')
            .should('have.attr', 'data-interest-failed', 'true')
            .and('have.attr', 'data-state', 'ready');
        // Sin la reacción, al entrar en una oferta señala directamente.
        entrar(0);
        cy.dataCy('job-host').should('have.attr', 'data-clip', 'point');
        cy.dataCy('job-detail-link').should('have.length.at.least', 1);
        cy.dataCy('jobs-search').should('be.visible');
    });

    it('si falla el póster, el anfitrión desaparece y el listado sigue entero', () => {
        cy.intercept('GET', '**/anfitrion-reposo.webp', {
            statusCode: 404,
            body: '',
        });
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });

        cy.dataCy('job-host').should('not.exist');
        cy.dataCy('job-card').should('have.length.at.least', 1);
        sinDesborde();
    });

    ['light', 'dark'].forEach((tema) => {
        it(`búsqueda, ida a una oferta y regreso, en tema ${tema === 'light' ? 'claro' : 'oscuro'}`, () => {
            cy.viewport(1280, 800);
            cy.visit('/empleos', {
                onBeforeLoad(win) {
                    escritorio(win);
                    win.localStorage.setItem('appearance', tema);
                },
            });
            anfitrionListo();

            marcarAnfitrion();
            cy.dataCy('jobs-search').type('Docente{enter}');
            cy.location('search').should('contain', 'q=Docente');
            cy.dataCy('job-card').should('have.length.at.least', 1);
            // Inertia vuelve a montar la página en cada visita: el anfitrión también.
            anfitrionRemontado();
            anfitrionListo();
            entrar(0);
            cy.dataCy('job-host').should('have.attr', 'data-clip', 'interest');

            cy.dataCy('job-detail-link')
                .first()
                .then(($link) => {
                    const nombre = $link.text().trim();

                    cy.wrap($link).click();
                    cy.dataCy('page-title').should('have.text', nombre);
                });
            cy.dataCy('job-host').should('not.exist');
            cy.go('back');
            cy.location('search').should('contain', 'q=Docente');
            cy.dataCy('job-host').should('have.length', 1);
            cy.get('[data-anfitrion]').should('have.length.at.most', 1);
            anfitrionListo();
            entrar(0);
            cy.get('[data-anfitrion="activa"]').should('have.length', 1);
            cy.dataCy('job-host').should('have.attr', 'data-clip', 'interest');
            cy.screenshot(`e2e24-9-${tema}-regreso`, { capture: 'viewport' });
        });
    });

    // Capturas de cada estado, al final de su propia prueba.
    it('captura: reacción de interés', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();
        entrar(0);
        cy.dataCy('job-host').should('have.attr', 'data-clip', 'interest');
        cy.wait(1000);
        cy.screenshot('e2e24-2-interes', { capture: 'viewport' });
    });

    it('captura: señala hacia una oferta de la fila de abajo', () => {
        cy.viewport(1280, 800);
        cy.visit('/empleos', { onBeforeLoad: escritorio });
        anfitrionListo();
        cy.dataCy('job-card').its('length').should('be.gte', 4);
        cy.dataCy('job-detail-link').eq(3).focus();
        cy.dataCy('job-host', { timeout: 10000 })
            .should('have.attr', 'data-clip', 'point')
            .and('have.attr', 'data-zone', 'down')
            .and('have.attr', 'data-frame', '60');
        cy.screenshot('e2e24-3-senala-abajo', { capture: 'viewport' });
    });
});
