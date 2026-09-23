/**
 * Captura de la portada con la capa de profundidad. NO forma parte de la
 * suite E2E.
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

function tema(win, valor) {
    win.localStorage.setItem('appearance', valor);
}

describe('Fase 20 · captura de la portada', () => {
    afterEach(() => reducido(false));

    it('escritorio claro con escena', () => {
        cy.viewport(1280, 720);
        cy.visit('/', { onBeforeLoad: (win) => tema(win, 'light') });
        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );
        cy.screenshot('01-escena-claro-1280', {
            capture: 'viewport',
            overwrite: true,
        });
    });

    it('escritorio oscuro con escena', () => {
        cy.viewport(1280, 720);
        cy.visit('/', { onBeforeLoad: (win) => tema(win, 'dark') });
        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );
        cy.screenshot('02-escena-oscuro-1280', {
            capture: 'viewport',
            overwrite: true,
        });
    });

    it('movimiento reducido: póster', () => {
        reducido(true);
        cy.viewport(1280, 720);
        cy.visit('/', { onBeforeLoad: (win) => tema(win, 'light') });
        cy.dataCy('recruitment-poster').should('exist');
        cy.screenshot('03-poster-reducido-1280', {
            capture: 'viewport',
            overwrite: true,
        });
    });

    it('tableta y móvil: póster', () => {
        cy.viewport(768, 1024);
        cy.visit('/', { onBeforeLoad: (win) => tema(win, 'light') });
        cy.dataCy('recruitment-poster').should('exist');
        cy.dataCy('recruitment-depth').scrollIntoView({
            offset: { top: -80, left: 0 },
        });
        cy.screenshot('04-poster-768', {
            capture: 'viewport',
            overwrite: true,
        });

        cy.viewport(390, 844);
        cy.visit('/', { onBeforeLoad: (win) => tema(win, 'dark') });
        cy.dataCy('recruitment-poster').should('exist');
        cy.dataCy('recruitment-depth').scrollIntoView({
            offset: { top: -140, left: 0 },
        });
        cy.screenshot('05-poster-oscuro-390', {
            capture: 'viewport',
            overwrite: true,
        });
    });
});
