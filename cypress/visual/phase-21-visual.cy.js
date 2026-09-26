/**
 * Matriz de capturas de la Fase 21. NO forma parte de la suite E2E.
 *
 * Cubre lo que las fases anteriores no miraron: 320 y 1024 px, el modo oscuro
 * en móvil, estados vacíos y de error, la página de seguridad y el enlace de
 * salto con el foco puesto. Las capturas por encima de 1280 px las recorta la
 * ventana del navegador sin interfaz, así que 1440 se valida por DOM.
 */
function tema(valor) {
    return {
        onBeforeLoad(win) {
            win.localStorage.setItem('appearance', valor);
        },
    };
}

function asentar() {
    cy.window().then(
        (win) =>
            new Cypress.Promise((resolve) => {
                const finitas = win.document
                    .getAnimations()
                    .filter((a) => a.effect?.getTiming().iterations !== Infinity);

                Promise.all(finitas.map((a) => a.finished)).then(resolve, resolve);
            }),
    );
}

function foto(nombre, captura = 'viewport') {
    asentar();
    cy.screenshot(nombre, { capture: captura, overwrite: true });
}

function confirmarContrasena() {
    cy.visit('/user/confirm-password');
    cy.get('input[name=password]').type(Cypress.env('DEMO_PASSWORD'), { log: false });
    cy.get('[data-test=confirm-password-button]').click();
    cy.location('pathname').should('not.eq', '/user/confirm-password');
}

describe('Fase 21 · matriz visual', () => {
    before(() => cy.resetDatabase());

    it('público a 320 y 1024, claro y oscuro', () => {
        cy.viewport(320, 700);
        cy.visit('/', tema('light'));
        foto('01-portada-320');
        cy.visit('/empleos', tema('dark'));
        foto('02-empleos-oscuro-320');
        cy.visit('/login', tema('light'));
        foto('03-login-320');

        cy.viewport(1024, 720);
        cy.visit('/', tema('dark'));
        cy.dataCy('recruitment-depth').should('have.attr', 'data-mode', 'scene');
        foto('04-portada-oscuro-1024');
        cy.visit('/register', tema('light'));
        foto('05-registro-1024');
    });

    it('enlace de salto con el foco', () => {
        cy.loginAs('hr');
        cy.viewport(1280, 720);
        cy.visit('/vacantes', tema('light'));
        cy.get('a[href="#contenido-principal"]').focus();
        foto('06-salto-al-contenido');
    });

    it('interno a 320: tabla, formulario con errores y navegación', () => {
        cy.loginAs('hr');
        cy.viewport(320, 700);
        cy.visit('/vacantes', tema('light'));
        foto('07-vacantes-320');
        cy.visit('/postulaciones/4', tema('dark'));
        foto('08-expediente-oscuro-320');
        cy.get('[data-sidebar="trigger"]').click();
        foto('09-navegacion-movil-320');

        cy.loginAs('requester');
        cy.visit('/requerimientos/crear', tema('light'));
        cy.dataCy('save-job-request').click();
        cy.get('[role=alert]').should('exist');
        foto('10-formulario-errores-320');
    });

    it('interno a 1024: comparación, auditoría y seguridad', () => {
        cy.loginAs('approver');
        cy.viewport(1024, 720);
        cy.visit('/vacantes/3/comparacion', tema('light'));
        foto('11-comparacion-1024');
        cy.visit('/auditoria', tema('dark'));
        foto('12-auditoria-oscuro-1024');

        cy.loginAs('hr');
        confirmarContrasena();
        cy.visit('/settings/security', tema('light'));
        foto('13-seguridad-1024', 'fullPage');
        cy.visit('/settings/security', tema('dark'));
        foto('14-seguridad-oscuro-1024', 'fullPage');
    });

    it('evaluador y postulante: sesión, vacíos e incompletos', () => {
        cy.loginAs('evaluator');
        cy.viewport(390, 844);
        cy.visit('/mis-evaluaciones', tema('light'));
        cy.get('[data-cy=open-assignment]').first().click();
        cy.dataCy('score-sheet').should('exist');
        foto('15-sesion-evaluacion-390');

        cy.loginAs('candidateNew');
        cy.visit('/mis-postulaciones', tema('dark'));
        foto('16-vacio-oscuro-390');
        cy.visit('/mi-perfil', tema('light'));
        foto('17-perfil-incompleto-390');
    });

    it('lo que la matriz de la Fase 18 ya cubría, visto de nuevo tras F19 y F20', () => {
        // 720 px de alto: con más, la ventana sin interfaz escala la página y
        // la captura muestra las barras de desplazamiento del propio Cypress.
        cy.viewport(1280, 720);
        cy.visit('/', tema('light'));
        cy.dataCy('recruitment-scene').should('have.attr', 'data-ready', 'true');
        foto('19-portada-escena-1280');

        cy.then(() =>
            Cypress.automation('remote:debugger:protocol', {
                command: 'Emulation.setEmulatedMedia',
                params: { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] },
            }),
        );
        cy.visit('/', tema('dark'));
        cy.dataCy('recruitment-depth').should('have.attr', 'data-reason', 'reduced-motion');
        foto('20-portada-reducido-oscuro-1280');
        cy.then(() =>
            Cypress.automation('remote:debugger:protocol', {
                command: 'Emulation.setEmulatedMedia',
                params: { features: [] },
            }),
        );

        cy.loginAs('hr');
        cy.visit('/dashboard', tema('light'));
        cy.document().then((doc) => {
            expect(doc.documentElement.scrollWidth - doc.documentElement.clientWidth).to.be.lessThan(2);
        });
        foto('21-panel-rrhh-1280');
        cy.visit('/vacantes/3', tema('dark'));
        cy.dataCy('operational-risk-message').should('exist');
        cy.dataCy('operational-risk-panel').scrollIntoView({ offset: { top: -120, left: 0 } });
        foto('22-riesgo-operacional-oscuro-1280');
        cy.visit('/settings/appearance', tema('light'));
        foto('23-apariencia-1280');
        cy.visit('/settings/profile', tema('dark'));
        cy.contains('button', 'Eliminar mi cuenta').click();
        cy.get('[role=dialog]').should('be.visible');
        foto('24-dialogo-oscuro-1280');

        cy.loginAs('requester');
        cy.viewport(1024, 720);
        cy.visit('/requerimientos?estado=rechazado', tema('light'));
        cy.dataCy('job-request-link').first().click();
        cy.dataCy('rejection-alert').scrollIntoView({ offset: { top: -120, left: 0 } });
        foto('25-alerta-rechazo-1024');
    });

    it('botones destructivos en oscuro', () => {
        cy.loginAs('hr');
        cy.viewport(1024, 720);
        cy.visit('/settings/profile', tema('dark'));
        cy.contains('button', 'Eliminar mi cuenta').scrollIntoView();
        foto('18-destructivo-oscuro');
    });
});
