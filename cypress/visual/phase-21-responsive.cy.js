/**
 * Desbordamiento horizontal en los anchos que la Fase 18 no cubría. NO forma
 * parte de la suite E2E.
 *
 * La Fase 18 midió 1440, 1280, 768 y 390 px. Aquí se añaden 1024 —el umbral en
 * que la portada pasa a dos columnas y aparece la escena de la Fase 20— y 320,
 * el teléfono más angosto que todavía se usa. También entran las páginas que
 * aquella lista no alcanzaba: seguridad (detrás de `RequirePassword`), las
 * sesiones de evaluación y los estados vacíos de un postulante nuevo.
 */
const ANCHOS = [1024, 320];

const PAGINAS = [
    { rol: null, rutas: ['/', '/empleos', '/empleos/2', '/login', '/register', '/forgot-password', '/reset-password/token-ficticio?email=nadie%40ejemplo.test'] },
    {
        rol: 'hr',
        confirmar: true,
        rutas: ['/dashboard', '/requerimientos', '/requerimientos/4', '/vacantes', '/vacantes/crear', '/vacantes/1', '/vacantes/2', '/vacantes/1/editar', '/vacantes/3/postulaciones', '/postulaciones/4', '/vacantes/3/comparacion', '/notificaciones', '/settings/profile', '/settings/security', '/settings/appearance', '/user/confirm-password'],
    },
    { rol: 'requester', rutas: ['/requerimientos/crear'] },
    { rol: 'approver', rutas: ['/auditoria', '/vacantes/3/comparacion'] },
    { rol: 'evaluator', rutas: ['/mis-evaluaciones'], asignaciones: true },
    { rol: 'candidateSubmitted', rutas: ['/mi-perfil', '/mis-postulaciones', '/mis-postulaciones/1'] },
    { rol: 'candidateNew', rutas: ['/mi-perfil', '/mis-postulaciones'] },
];

function sinDesborde(ruta, ancho) {
    cy.viewport(ancho, 800);
    cy.visit(ruta);
    cy.get('h1, [data-cy=page-title]').should('exist');
    cy.document().then((doc) => {
        const raiz = doc.documentElement;
        const exceso = raiz.scrollWidth - raiz.clientWidth;
        let detalle = '';

        if (exceso > 1) {
            detalle = [...doc.querySelectorAll('body *')]
                .map((el) => ({ el, r: el.getBoundingClientRect().right }))
                .filter((x) => x.r > raiz.clientWidth + 1)
                .sort((a, b) => b.r - a.r)
                .slice(0, 3)
                .map((x) => `${x.el.tagName.toLowerCase()}.${String(x.el.className).slice(0, 80)} @${Math.round(x.r)}`)
                .join(' || ');
        }

        expect(exceso, `desborde en ${ruta} a ${ancho}px ${detalle}`).to.be.lessThan(2);
    });
}

describe('Fase 21 · desbordamiento a 1024 y 320 px', () => {
    before(() => cy.resetDatabase());

    PAGINAS.forEach(({ rol, confirmar, rutas, asignaciones }) => {
        it(rol || 'público', () => {
            if (rol) cy.loginAs(rol);

            if (confirmar) {
                cy.visit('/user/confirm-password');
                cy.get('input[name=password]').type(Cypress.env('DEMO_PASSWORD'), { log: false });
                cy.get('[data-test=confirm-password-button]').click();
                cy.location('pathname').should('not.eq', '/user/confirm-password');
            }

            ANCHOS.forEach((ancho) => rutas.forEach((ruta) => sinDesborde(ruta, ancho)));

            if (asignaciones) {
                cy.visit('/mis-evaluaciones');
                cy.get('[data-cy=open-assignment]').then(($a) => {
                    [...new Set([...$a].map((a) => new URL(a.href).pathname))].forEach((ruta) =>
                        ANCHOS.forEach((ancho) => sinDesborde(ruta, ancho)),
                    );
                });
            }
        });
    });
});
