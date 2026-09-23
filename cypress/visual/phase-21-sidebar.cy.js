/**
 * ¿La barra lateral de escritorio produce saltos o tirones al plegarse?
 * NO forma parte de la suite E2E.
 *
 * La Fase 19 la dejó animando `width`, `left` y `right`, que obligan a
 * recalcular el diseño. Antes de reescribirla se mide: intervalos entre
 * cuadros durante el pliegue y desplazamientos de diseño registrados.
 */
describe('Fase 21 · barra lateral de escritorio', () => {
    it('mide diez pliegues', () => {
        cy.loginAs('hr');
        cy.viewport(1280, 800);
        cy.visit('/vacantes', {
            onBeforeLoad(win) {
                win.__cambios = [];
                new win.PerformanceObserver((l) => {
                    l.getEntries().forEach((e) =>
                        win.__cambios.push({ valor: e.value, conEntrada: e.hadRecentInput }),
                    );
                }).observe({ type: 'layout-shift', buffered: false });
            },
        });
        cy.dataCy('vacancy-row').should('exist');

        const intervalos = [];

        Cypress._.times(10, () => {
            cy.window().then((win) => {
                let previo = null;
                let activo = true;
                const paso = (t) => {
                    if (previo !== null) intervalos.push(t - previo);
                    previo = t;
                    if (activo) win.requestAnimationFrame(paso);
                };

                win.requestAnimationFrame(paso);
                win.setTimeout(() => (activo = false), 450);
            });
            cy.get('[data-sidebar="trigger"]').click();
            cy.get('[data-state]').should('exist');
            cy.window().then((win) => new Cypress.Promise((r) => win.setTimeout(r, 500)));
        });

        cy.window().then((win) => {
            const orden = [...intervalos].sort((a, b) => a - b);
            const p = (q) => orden[Math.floor((orden.length - 1) * q)];

            cy.writeFile('cypress/results/phase-21-sidebar.json', {
                cuadros: intervalos.length,
                medianaMs: Number(p(0.5).toFixed(1)),
                p95Ms: Number(p(0.95).toFixed(1)),
                maxMs: Number(orden[orden.length - 1].toFixed(1)),
                cuadrosDe50msOMas: intervalos.filter((i) => i >= 50).length,
                desplazamientos: win.__cambios.length,
                clsSinEntrada: win.__cambios
                    .filter((c) => !c.conEntrada)
                    .reduce((s, c) => s + c.valor, 0),
            });
        });
    });
});
