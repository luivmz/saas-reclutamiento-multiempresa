/**
 * Medición de la portada, antes y después de la Fase 20. NO forma parte de la
 * suite E2E.
 *
 * Presupuestos de `recruitment-3d-experience/BUDGETS.md`: la línea base se
 * mide antes de tocar nada y el resultado se compara contra ella. Se toman
 * cinco cargas y se informa la mediana, porque una sola carga en un
 * contenedor mide sobre todo el ruido del contenedor.
 *
 * LCP no se informa: Chromium no lo reporta dentro del iframe en que Cypress
 * carga la aplicación, y un cero no es una medición.
 */
const RONDAS = 5;

function mediana(valores) {
    const orden = [...valores].sort((a, b) => a - b);

    return orden[Math.floor(orden.length / 2)];
}

describe('Fase 20 · medición de la portada', () => {
    it('registra carga, bytes, primer cuadro de la escena y cuadros por segundo', () => {
        const muestras = [];

        Cypress._.times(RONDAS, () => {
            cy.viewport(1280, 800);
            cy.visit('/', {
                onBeforeLoad(win) {
                    // Momento en que la escena termina de abrirse, medido
                    // desde el inicio de la navegación.
                    win.__escenaLista = null;
                    new win.MutationObserver(() => {
                        if (
                            win.__escenaLista === null &&
                            win.document.querySelector(
                                '[data-cy="recruitment-scene"][data-ready="true"]',
                            )
                        ) {
                            win.__escenaLista = win.performance.now();
                        }
                    }).observe(win.document, {
                        subtree: true,
                        childList: true,
                        attributes: true,
                        attributeFilter: ['data-ready'],
                    });
                },
            });
            cy.get('h1').should('be.visible');
            cy.window().its('document.readyState').should('eq', 'complete');
            cy.get('body').then(($body) => {
                if (
                    $body.find(
                        '[data-cy="recruitment-depth"][data-mode="scene"]',
                    ).length
                ) {
                    cy.dataCy('recruitment-scene').should(
                        'have.attr',
                        'data-ready',
                        'true',
                    );
                }
            });

            // Cuadros por segundo durante un segundo de puntero en movimiento
            // sobre la portada: el caso más caro que la escena admite.
            cy.window()
                .then(
                    (win) =>
                        new Cypress.Promise((resolve) => {
                            let cuadros = 0;
                            let inicio = null;
                            const paso = (t) => {
                                inicio ??= t;
                                cuadros += 1;
                                win.dispatchEvent(
                                    new win.PointerEvent('pointermove', {
                                        clientX: 200 + ((t - inicio) % 900),
                                        clientY: 300 + Math.sin(t / 120) * 150,
                                    }),
                                );

                                if (t - inicio < 1000) {
                                    win.requestAnimationFrame(paso);
                                } else {
                                    resolve((cuadros * 1000) / (t - inicio));
                                }
                            };

                            win.requestAnimationFrame(paso);
                        }),
                )
                .then((fps) => {
                    cy.window().then((win) => {
                        const nav =
                            win.performance.getEntriesByType('navigation')[0];
                        const js = win.performance
                            .getEntriesByType('resource')
                            .filter((r) => r.name.endsWith('.js'));

                        muestras.push({
                            dcl: nav.domContentLoadedEventEnd,
                            load: nav.loadEventEnd,
                            jsCount: js.length,
                            jsBytes: js.reduce(
                                (s, r) => s + (r.decodedBodySize || 0),
                                0,
                            ),
                            escena: js.some((r) =>
                                r.name.includes('recruitment-scene'),
                            ),
                            escenaLista: win.__escenaLista,
                            fps,
                        });
                    });
                });
        });

        cy.then(() => {
            const conEscena = muestras.filter((m) => m.escenaLista !== null);
            const resumen = {
                dclMs: Math.round(mediana(muestras.map((m) => m.dcl))),
                loadMs: Math.round(mediana(muestras.map((m) => m.load))),
                jsArchivos: mediana(muestras.map((m) => m.jsCount)),
                jsKB: Math.round(
                    mediana(muestras.map((m) => m.jsBytes)) / 1024,
                ),
                escenaCargada: muestras.every((m) => m.escena),
                escenaListaMs: conEscena.length
                    ? Math.round(mediana(conEscena.map((m) => m.escenaLista)))
                    : null,
                fps: Math.round(mediana(muestras.map((m) => m.fps))),
            };

            cy.writeFile('cypress/results/phase-20-perf.json', resumen);
        });
    });
});
