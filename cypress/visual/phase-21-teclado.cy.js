/**
 * Recorrido con Tab por las pantallas principales. NO forma parte de la suite.
 *
 * Las teclas se envían por el protocolo del navegador, no con `cy.type`: así
 * es el navegador quien mueve el foco, como con una persona. En cada parada se
 * anota qué recibió el foco y si el indicador se ve (contorno o anillo). El
 * resultado queda en `cypress/results/phase-21-teclado.json`.
 */
const RESULTADOS = 'cypress/results/phase-21-teclado.json';
const PARADAS = 40;

function tab() {
    const base = { key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9 };

    return Cypress.automation('remote:debugger:protocol', {
        command: 'Input.dispatchKeyEvent',
        params: { ...base, type: 'keyDown' },
    }).then(() =>
        Cypress.automation('remote:debugger:protocol', {
            command: 'Input.dispatchKeyEvent',
            params: { ...base, type: 'keyUp' },
        }),
    );
}

function parada(win) {
    const el = win.document.activeElement;

    if (!el || el === win.document.body) return { el: 'body' };

    const s = win.getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const contorno = s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0;
    const anillo = s.boxShadow && s.boxShadow !== 'none';

    return {
        el: `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}`,
        nombre: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 40),
        visible: r.width > 0 && r.height > 0,
        indicador: Boolean(contorno || anillo),
        oculto: Boolean(el.closest('[aria-hidden=true], [inert]')),
    };
}

const PAGINAS = [
    { rol: null, rutas: ['/', '/login', '/empleos'] },
    { rol: 'hr', rutas: ['/dashboard', '/vacantes', '/vacantes/3/comparacion', '/settings/appearance'] },
    { rol: 'evaluator', rutas: ['/mis-evaluaciones'] },
    { rol: 'candidateSubmitted', rutas: ['/mis-postulaciones'] },
];

describe('Fase 21 · recorrido con teclado', () => {
    const informe = [];

    before(() => cy.resetDatabase());
    after(() => cy.writeFile(RESULTADOS, informe));

    // Una prueba por ruta: con varias visitas en la misma prueba, las teclas
    // enviadas por el protocolo se perdían en las páginas públicas y el
    // recorrido quedaba en `body`. Cada página se recorre recién cargada.
    PAGINAS.forEach(({ rol, rutas }) => {
        rutas.forEach((ruta) => {
            it(`teclado · ${rol || 'público'} · ${ruta}`, () => {
                if (rol) cy.loginAs(rol);

                cy.viewport(1280, 900);
                cy.visit(ruta);
                cy.get('h1').should('exist');
                // El primer evento de teclado tras abrir el navegador puede
                // perderse mientras el protocolo se conecta: se descarta.
                cy.window().then((win) => win.focus());

                const paradas = [];

                for (let i = 0; i < PARADAS; i++) {
                    cy.then(() => tab());
                    cy.window().then((win) => paradas.push(parada(win)));
                }

                cy.then(() => {
                    informe.push({
                        rol: rol || 'público',
                        ruta,
                        inicio: paradas.slice(0, 4).map((p) => `${p.el} ${p.nombre ?? ''}`.trim()),
                        enBody: paradas.filter((p) => p.el === 'body').length,
                        sinIndicador: paradas.filter((p) => p.el !== 'body' && !p.indicador),
                        invisibles: paradas.filter((p) => p.el !== 'body' && !p.visible),
                        enOculto: paradas.filter((p) => p.oculto),
                    });
                });
            });
        });
    });
});
