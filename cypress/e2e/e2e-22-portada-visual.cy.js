/**
 * E2E-22 · Portada del incremento visual: vacante, evidencias y decisión humana en profundidad.
 *
 * Complementa a E2E-18 (que fija cuándo la escena cede al póster) con lo que añade este incremento:
 *
 * - el expediente cuenta en texto las tres etapas que la escena dibuja;
 * - con un puntero fino, las hojas se desplazan según su profundidad (paralaje); sin él, quedan quietas;
 * - el acceso principal se alcanza con el teclado y muestra el foco;
 * - las entradas al desplazarse no ocultan nada con movimiento reducido ni a quien ya lo está viendo;
 * - a 320 px no hay desplazamiento horizontal;
 * - VIS-L01: si el movimiento reducido se activa con la portada abierta, lo
 *   pendiente aparece en su sitio y no vuelve a ocultarse.
 *
 */
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

function sinDesborde() {
    cy.document().then((doc) => {
        expect(
            doc.documentElement.scrollWidth - doc.documentElement.clientWidth,
        ).to.be.lessThan(2);
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

/** Un movimiento del puntero donde la escena escucha: en la ventana. */
function moverCursor(clientX, clientY) {
    cy.window().then((win) =>
        win.dispatchEvent(
            new win.PointerEvent('pointermove', {
                clientX,
                clientY,
                bubbles: true,
            }),
        ),
    );
}

/** La carpeta del proceso a la vista, y dos cuadros para que la escena asiente su posición. */
function irALaCarpeta() {
    cy.dataCy('landing-folder').scrollIntoView();
    cy.window().then(
        (win) =>
            new Cypress.Promise((listo) =>
                win.requestAnimationFrame(() =>
                    win.requestAnimationFrame(listo),
                ),
            ),
    );
}

/** Una hoja de la escena; sus aserciones con callback se reintentan. */
function hoja(etapa) {
    return cy.get(`[data-sheet="${etapa}"]`);
}

function transformDe(etapa) {
    return cy
        .get(`[data-sheet="${etapa}"]`)
        .then(($hoja) => $hoja[0].style.transform);
}

describe('E2E-22 · Portada: profundidad, paralaje y accesos', () => {
    afterEach(() => reducido(false));

    it('el expediente cuenta en texto lo que la escena dibuja: vacante, evidencias y decisión humana', () => {
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.contains('REQ-2026-0042')
            .closest('.z-10')
            .within(() => {
                cy.contains('Vacante').should('be.visible');
                cy.contains('Evidencias').should('be.visible');
                cy.contains('Decisión humana').should('be.visible');
            });
        cy.dataCy('landing-pillars').find('li').should('have.length', 3);
        irALaCarpeta();
        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );
        cy.get('[data-sheet]').should('have.length', 3);
        cy.dataCy('recruitment-depth')
            .find('[data-sheet]')
            .each(($hoja) => {
                expect($hoja.text().trim(), 'las hojas no llevan texto').to.eq(
                    '',
                );
            });
    });

    it('con un puntero fino, las hojas se desplazan según su profundidad y vuelven al reposo', () => {
        cy.viewport(1280, 800);
        // Electron sin pantalla no tiene ratón: se declara un puntero fino, como en un escritorio.
        cy.visit('/', { onBeforeLoad: (win) => punteroFino(win, true) });
        irALaCarpeta();
        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );

        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-pointer',
            'listening',
        );
        irALaCarpeta();
        transformDe('vacancy').then((reposo) => {
            moverCursor(1240, 120);
            hoja('vacancy').should(($h) =>
                expect($h[0].style.transform).not.to.eq(reposo),
            );
            hoja('decision').should(($h) =>
                expect($h[0].style.transform).to.match(/translate3d/),
            );

            cy.document().then((doc) =>
                doc.documentElement.dispatchEvent(
                    new PointerEvent('pointerleave'),
                ),
            );
            hoja('vacancy').should(($h) =>
                expect($h[0].style.transform).to.eq(reposo),
            );
        });

        // Al volver al hero, el CTA sigue sin transformaciones del cursor.
        cy.scrollTo('top');
        cy.dataCy('cta-jobs')
            .should('be.visible')
            .and('not.have.attr', 'style');
    });

    it('en pantallas táctiles (sin puntero fino) la escena queda quieta', () => {
        cy.viewport(1280, 800);
        cy.visit('/', { onBeforeLoad: (win) => punteroFino(win, false) });
        irALaCarpeta();
        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );

        // Sin puntero fino la escena nunca se pone a escuchar.
        cy.dataCy('recruitment-scene').should('not.have.attr', 'data-pointer');
        transformDe('vacancy').then((reposo) => {
            moverCursor(1240, 120);
            // Tiempo de sobra para un cuadro: si hubiera escucha, el transform ya habría cambiado.
            cy.wait(300);
            hoja('vacancy').should(($h) =>
                expect($h[0].style.transform).to.eq(reposo),
            );
        });
        cy.scrollTo('top');
        cy.dataCy('cta-jobs').should('be.visible');
    });

    it('el acceso principal se alcanza con el teclado y muestra el foco', () => {
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.dataCy('cta-jobs').focus();
        cy.focused()
            .should('have.attr', 'data-cy', 'cta-jobs')
            .then(($a) => {
                const estilo = getComputedStyle($a[0]);

                expect(
                    estilo.outlineStyle !== 'none' ||
                        estilo.boxShadow !== 'none',
                    'foco visible',
                ).to.eq(true);
            });
        cy.press(Cypress.Keyboard.Keys.TAB);
        cy.focused().should('have.attr', 'data-cy', 'cta-login');
    });

    it('con movimiento reducido nada queda oculto a la espera de desplazarse', () => {
        reducido(true);
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.get('[data-reveal]').should('have.length.at.least', 5);
        cy.get('[data-reveal="hidden"]').should('not.exist');
        cy.dataCy('landing-ml-note').should('have.css', 'opacity', '1');
    });

    it('VIS-L01: si el movimiento reducido se activa con la portada abierta, lo pendiente aparece sin desplazarse y no vuelve a ocultarse', () => {
        cy.viewport(1280, 800);
        cy.visit('/');

        // Antes: lo de abajo espera oculto y desplazado.
        cy.dataCy('landing-ml-note').should('have.css', 'opacity', '0');
        cy.get('[data-reveal="hidden"]')
            .should('have.length.at.least', 3)
            .then(($pendientes) => {
                const pendientes = $pendientes.toArray();
                const aLaVista = () =>
                    cy.wrap(pendientes).each((bloque) =>
                        cy.wrap(bloque).should(($b) => {
                            const estilo = getComputedStyle($b[0]);

                            expect(estilo.opacity, 'opacidad').to.eq('1');
                            expect(
                                estilo.transform,
                                'sin desplazamiento',
                            ).to.eq('none');
                        }),
                    );

                // Se activa con la página abierta y sin desplazarla: la
                // apariencia real de cada bloque pendiente cambia en su sitio.
                // Va en la cola de Cypress, en orden con las aserciones.
                cy.then(() => reducido(true));
                aLaVista();
                cy.window().its('scrollY').should('eq', 0);
                cy.get('[data-reveal="hidden"]').should('not.exist');

                // Ni al recorrer la página ni al desactivar la preferencia
                // vuelve a ocultarse nada: ya no hay observadores pendientes.
                cy.scrollTo('bottom');
                cy.scrollTo('top');
                cy.then(() => reducido(false));
                cy.scrollTo('bottom');
                aLaVista();
                cy.get('[data-reveal="hidden"]').should('not.exist');
            });
    });

    it('sin movimiento reducido, lo de abajo entra al desplazarse y queda visible', () => {
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.dataCy('landing-ml-note').should(
            'have.attr',
            'data-reveal',
            'hidden',
        );
        cy.dataCy('landing-ml-note').scrollIntoView();
        cy.dataCy('landing-ml-note')
            .should('have.attr', 'data-reveal', 'shown')
            .and('have.css', 'opacity', '1');
    });

    it('a 320 px: póster, un solo h1, acceso principal visible y sin desbordar', () => {
        cy.viewport(320, 640);
        cy.visit('/');

        cy.dataCy('recruitment-depth').should(
            'have.attr',
            'data-mode',
            'poster',
        );
        cy.get('h1').should('have.length', 1);
        cy.dataCy('cta-jobs').scrollIntoView().should('be.visible');
        sinDesborde();
    });
});
