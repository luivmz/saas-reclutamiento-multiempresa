/**
 * Captura visual de la Fase 18. NO forma parte de la suite E2E.
 *
 * Se ejecuta con `--config specPattern=cypress/visual/**\/*.cy.js` para
 * fotografiar cada módulo en escritorio y en móvil, y se borra al terminar la
 * validación: la suite de regresión sigue siendo de 16 specs.
 */
const DESKTOP = [1280, 720];
const MOBILE = [390, 720];

function shoot(name) {
    cy.wait(350);
    cy.screenshot(name, { capture: 'fullPage', overwrite: true });
}

function visitAndShoot(path, name, sizes = [DESKTOP, MOBILE]) {
    sizes.forEach(([w, h], index) => {
        cy.viewport(w, h);
        cy.visit(path);
        shoot(`${name}-${index === 0 ? 'desktop' : 'movil'}`);
    });
}

describe('Fase 18 · captura visual', () => {
    before(() => cy.resetDatabase());

    it('sitio público y acceso', () => {
        visitAndShoot('/', '01-portada');
        visitAndShoot('/empleos', '02-empleos');
        visitAndShoot('/empleos/2', '03-empleo-detalle');
        visitAndShoot('/login', '04-login');
        visitAndShoot('/register', '05-registro');
    });

    it('RR. HH.', () => {
        cy.loginAs('hr');
        visitAndShoot('/dashboard', '06-panel-rrhh');
        visitAndShoot('/requerimientos', '07-requerimientos');
        visitAndShoot('/requerimientos/4', '08-requerimiento-detalle');
        visitAndShoot('/vacantes', '09-vacantes');
        visitAndShoot('/vacantes/1', '10-vacante-borrador');
        visitAndShoot('/vacantes/2', '11-vacante-publicada');
        visitAndShoot('/vacantes/1/editar', '12-vacante-formulario');
        visitAndShoot('/vacantes/3/postulaciones', '13-postulaciones');
        visitAndShoot('/postulaciones/4', '14-expediente-postulacion');
        visitAndShoot('/vacantes/3/comparacion', '15-comparacion-ranking');
        visitAndShoot('/notificaciones', '16-notificaciones');
        visitAndShoot('/settings/profile', '17-configuracion');
    });

    it('Dirección y evaluador', () => {
        cy.loginAs('approver');
        visitAndShoot('/vacantes/3/comparacion', '18-decision-final');
        visitAndShoot('/auditoria', '19-auditoria');

        cy.loginAs('evaluator');
        visitAndShoot('/mis-evaluaciones', '20-mis-evaluaciones');
    });

    it('postulante', () => {
        cy.loginAs('candidateSubmitted');
        visitAndShoot('/mi-perfil', '21-perfil-postulante');
        visitAndShoot('/mis-postulaciones', '22-mis-postulaciones');
        visitAndShoot('/mis-postulaciones/1', '23-mi-postulacion');
    });

    it('modo oscuro y anchos intermedios', () => {
        cy.loginAs('hr');

        cy.viewport(1280, 800);
        cy.visit('/vacantes', {
            onBeforeLoad(win) {
                win.localStorage.setItem('appearance', 'dark');
            },
        });
        shoot('24-vacantes-oscuro-1280');

        cy.viewport(768, 1024);
        cy.visit('/vacantes/3/comparacion');
        shoot('25-comparacion-tablet');

        cy.viewport(1440, 900);
        cy.visit('/requerimientos', {
            onBeforeLoad(win) {
                win.localStorage.setItem('appearance', 'light');
            },
        });
        shoot('26-requerimientos-claro');
    });
});
