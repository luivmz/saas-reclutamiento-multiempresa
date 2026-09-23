/**
 * Captura de los estados que el movimiento toca. NO forma parte de la suite E2E.
 *
 * Una animación no se ve en una imagen fija, pero sí se ve si rompió algo:
 * un panel abierto a medias, un menú con el origen equivocado, un overlay
 * demasiado oscuro. Estas capturas sirven para eso.
 */
function shoot(name) {
    cy.wait(500);
    cy.screenshot(name, { capture: 'viewport', overwrite: true });
}

describe('Fase 19 · captura de estados con movimiento', () => {
    before(() => cy.resetDatabase());

    it('menús y diálogos en claro', () => {
        cy.loginAs('hr');
        cy.viewport(1280, 720);

        cy.visit('/vacantes');
        cy.dataCy('appearance-toggle').click();
        shoot('01-menu-tema');
        cy.get('body').type('{esc}');

        cy.get('[data-test="sidebar-menu-button"]').click();
        shoot('02-menu-usuario');
        cy.get('body').type('{esc}');

        cy.visit('/settings/profile');
        cy.get('[data-test="delete-user-button"]').click();
        shoot('03-dialogo-eliminar');
    });

    it('navegación móvil abierta', () => {
        cy.loginAs('hr');
        cy.viewport(390, 720);
        cy.visit('/vacantes');
        cy.get('[data-sidebar="trigger"]').click();
        shoot('04-navegacion-movil');
    });

    it('menús y diálogos en oscuro', () => {
        cy.loginAs('hr');
        cy.viewport(1280, 720);
        cy.visit('/vacantes', {
            onBeforeLoad(win) {
                win.localStorage.setItem('appearance', 'dark');
            },
        });

        cy.get('[data-test="sidebar-menu-button"]').click();
        shoot('05-menu-usuario-oscuro');
        cy.get('body').type('{esc}');

        cy.visit('/settings/profile');
        cy.get('[data-test="delete-user-button"]').click();
        shoot('06-dialogo-oscuro');
    });

    it('riesgo operacional y formulario con error', () => {
        cy.loginAs('hr');
        cy.viewport(1280, 720);
        cy.visit('/vacantes/2', {
            onBeforeLoad(win) {
                win.localStorage.setItem('appearance', 'light');
            },
        });
        shoot('07-riesgo-operacional');

        cy.loginAs('requester');
        cy.visit('/requerimientos/crear');
        cy.dataCy('save-job-request').click();
        shoot('08-formulario-con-errores');
    });
});
