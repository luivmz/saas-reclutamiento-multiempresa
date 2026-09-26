/**
 * El movimiento no puede costarle nada a quien no lo quiere o no lo usa.
 *
 * Aquí se comprueban las tres cosas que una animación puede romper y que no
 * se ven en una captura: que el teclado siga llevando y devolviendo el foco,
 * que `prefers-reduced-motion` deje de desplazar cosas sin dejar la interfaz
 * inservible, y que la tabla de expedientes conserve la semántica que fijó la
 * Fase 18 también con el movimiento reducido.
 *
 * No se mide ninguna duración exacta: se comprueba que la curva y la política
 * aplicadas son las del sistema, no las del navegador.
 */

/** Emula `prefers-reduced-motion: reduce` en el navegador de la prueba. */
function conMovimientoReducido() {
    return Cypress.automation('remote:debugger:protocol', {
        command: 'Emulation.setEmulatedMedia',
        params: {
            features: [{ name: 'prefers-reduced-motion', value: 'reduce' }],
        },
    });
}

/** Devuelve el navegador a su configuración normal. */
function sinEmulacion() {
    return Cypress.automation('remote:debugger:protocol', {
        command: 'Emulation.setEmulatedMedia',
        params: { features: [] },
    });
}

describe('E2E-17 · El movimiento respeta el teclado y a quien lo reduce', () => {
    before(() => cy.resetDatabase());

    afterEach(() => sinEmulacion());

    it('el menú de usuario se abre con teclado y devuelve el foco al cerrarse', () => {
        cy.loginAs('hr');
        cy.visit('/vacantes');

        cy.get('[data-test="sidebar-menu-button"]').focus().type('{enter}');
        cy.get('[role="menu"]').should('be.visible');

        cy.focused().type('{esc}');
        cy.get('[role="menu"]').should('not.exist');
        // Radix devuelve el foco al disparador: sin eso, quien navega con
        // teclado queda al principio de la página tras cada menú.
        cy.focused().should('have.attr', 'data-test', 'sidebar-menu-button');
    });

    it('la navegación móvil se abre, se cierra con Escape y devuelve el foco', () => {
        cy.loginAs('hr');
        cy.viewport(390, 844);
        cy.visit('/vacantes');

        cy.get('[data-sidebar="trigger"]').click();
        cy.get('[data-mobile="true"]').should('be.visible');
        cy.dataCy('nav-vacancies').should('be.visible');

        cy.get('[data-mobile="true"]').type('{esc}');
        cy.get('[data-mobile="true"]').should('not.exist');
        // El panel se abre por estado y no por un disparador de Radix, asi que
        // la devolucion del foco es nuestra: sin ella se termina en `body`.
        cy.focused().should('have.attr', 'data-sidebar', 'trigger');
    });

    it('el diálogo de eliminar la cuenta atrapa y devuelve el foco', () => {
        cy.loginAs('hr');
        cy.visit('/settings/profile');

        cy.get('[data-test="delete-user-button"]').click();
        cy.get('[role="dialog"]').should('be.visible');
        cy.get('[role="dialog"]').within(() => {
            cy.contains('¿Confirma que desea eliminar su cuenta?').should(
                'be.visible',
            );
        });

        cy.get('body').type('{esc}');
        cy.get('[role="dialog"]').should('not.exist');
        cy.focused().should('have.attr', 'data-test', 'delete-user-button');
    });

    it('usa la curva del sistema y no la del navegador', () => {
        cy.loginAs('hr');
        cy.visit('/vacantes');

        // `ease-out` está redefinido en los tokens: si alguien volviera a la
        // curva incorporada, esta comprobación lo dice.
        cy.dataCy('vacancy-row')
            .first()
            .should('have.css', 'transition-timing-function')
            .and('include', 'cubic-bezier(0.23, 1, 0.32, 1)');
    });

    it('con movimiento reducido no se desplaza nada y la interfaz sigue usable', () => {
        cy.loginAs('hr');
        conMovimientoReducido();
        cy.visit('/vacantes');

        // La política deja pasar color y opacidad, y quita el resto: si
        // `transform` siguiera en la lista, el movimiento seguiría ahí.
        cy.dataCy('vacancy-row')
            .first()
            .then(($fila) => {
                const propiedades = getComputedStyle(
                    $fila[0],
                ).transitionProperty;

                expect(propiedades).to.include('opacity');
                expect(propiedades).not.to.include('transform');
            });

        // Y la interfaz sigue respondiendo: el menú abre y cierra igual.
        cy.get('[data-test="sidebar-menu-button"]').click();
        cy.get('[role="menu"]').should('be.visible');
        cy.get('body').type('{esc}');
        cy.get('[role="menu"]').should('not.exist');
    });

    it('con movimiento reducido el esqueleto deja de latir y el spinner sigue girando', () => {
        cy.loginAs('hr');
        conMovimientoReducido();
        cy.visit('/vacantes');

        cy.document().then((doc) => {
            const prueba = doc.createElement('div');
            prueba.className = 'animate-pulse';
            const spinner = doc.createElement('div');
            spinner.className = 'animate-spin';
            doc.body.append(prueba, spinner);

            // El latido es adorno; el giro es información sobre una espera.
            expect(getComputedStyle(prueba).animationName).to.eq('none');
            expect(getComputedStyle(spinner).animationName).to.eq('spin');

            prueba.remove();
            spinner.remove();
        });
    });

    it('con movimiento reducido la tabla conserva su semántica accesible', () => {
        cy.loginAs('hr');
        conMovimientoReducido();
        cy.viewport(390, 844);
        cy.visit('/vacantes');

        cy.dataCy('vacancies-table').should('have.attr', 'role', 'table');
        cy.dataCy('vacancies-table')
            .find('thead')
            .should('not.have.css', 'display', 'none');
        cy.dataCy('vacancy-row').should('have.length.at.least', 1);

        cy.dataCy('vacancies-table').then(($tabla) => {
            const ids = [...$tabla[0].querySelectorAll('thead th')].map(
                (th) => th.id,
            );

            [...$tabla[0].querySelectorAll('tbody td')].forEach((celda) => {
                expect(ids).to.include(celda.getAttribute('headers'));
            });
        });

        cy.document().then((doc) => {
            const raiz = doc.documentElement;

            expect(raiz.scrollWidth - raiz.clientWidth).to.be.lessThan(2);
        });
    });

    it('el panel de riesgo aparece con una atenuación, sin latido ni alarma', () => {
        cy.loginAs('hr');
        cy.visit('/vacantes/2');

        cy.dataCy('operational-risk-panel')
            .should('be.visible')
            .within(() => {
                // Entra atenuándose, nunca desplazándose ni repitiendo: es una
                // señal para revisión humana, no una alerta.
                cy.get('.animate-in')
                    .should('have.class', 'fade-in-0')
                    .and('not.have.class', 'animate-pulse');
                cy.get('[class*="slide-in"]').should('not.exist');
                cy.get('[class*="animate-bounce"]').should('not.exist');
            });
    });
});
