describe('E2E-29 · Cómo postular en la portada', () => {
    it('explica los cuatro pasos y mantiene convocatoria, requisitos y registro como enlaces y contenido HTML', () => {
        cy.viewport(1440, 900);
        cy.visit('/');
        const excerpts = [
            'criterios de evaluación y la fecha de cierre',
            'Si ya tiene cuenta, inicie sesión',
            'Cargue allí su CV',
            'Mis postulaciones y los cambios en Notificaciones',
        ];

        cy.dataCy('apply-step').should('have.length', 4);
        excerpts.forEach((text, index) => {
            cy.dataCy('apply-step')
                .eq(index)
                .click()
                .should('have.attr', 'aria-pressed', 'true');
            cy.get('[data-cy=apply-step][aria-pressed=true]').should(
                'have.length',
                1,
            );
            cy.dataCy('apply-description').should(
                'have.attr',
                'role',
                'status',
            );
            cy.dataCy('apply-description').should('contain.text', text);
            cy.dataCy('apply-poster')
                .children()
                .eq(index)
                .should('have.attr', 'data-active', 'true');
            cy.location('pathname').should('eq', '/');
        });

        cy.dataCy('landing-requirements').should(
            'contain.text',
            'PDF de hasta 5 MB',
        );
        cy.dataCy('landing-register').should('have.attr', 'href', '/register');
        cy.dataCy('apply-jobs').click();
        cy.location('pathname').should('eq', '/empleos');
        cy.dataCy('jobs-filters').should('be.visible');
    });

    it('pide la escena solo cerca de la sección y, si el export falla, deja el respaldo sincronizado', () => {
        cy.intercept('GET', '/spline/*.splinecode', {
            forceNetworkError: true,
        }).as('export');
        cy.viewport(1440, 900);
        cy.visit('/', {
            onBeforeLoad(win) {
                // Equipo capaz: la escena intenta cargar en lugar del póster.
                Object.defineProperty(win.navigator, 'hardwareConcurrency', {
                    value: 8,
                });
                Object.defineProperty(win.navigator, 'deviceMemory', {
                    value: 8,
                });
            },
        });
        cy.dataCy('apply-step').should('have.length', 4);
        cy.get('@export.all').should('have.length', 0);

        cy.dataCy('apply-illustration').scrollIntoView();
        cy.wait('@export');
        cy.dataCy('apply-illustration').find('canvas').should('not.exist');
        cy.dataCy('apply-poster').should('be.visible');
        cy.dataCy('apply-step').eq(2).click();
        cy.dataCy('apply-poster')
            .children()
            .eq(2)
            .should('have.attr', 'data-active', 'true');
        cy.dataCy('apply-description').should(
            'contain.text',
            'Cargue allí su CV',
        );
    });

    it('mantiene el recorrido con teclado y la alternativa estática a 320 px con movimiento reducido', () => {
        cy.viewport(320, 740);
        cy.visit('/', {
            onBeforeLoad(win) {
                const match = win.matchMedia.bind(win);
                cy.stub(win, 'matchMedia').callsFake((query) =>
                    query === '(prefers-reduced-motion: reduce)'
                        ? {
                              ...match(query),
                              matches: true,
                              addEventListener() {},
                              removeEventListener() {},
                          }
                        : match(query),
                );
            },
        });
        cy.dataCy('apply-step').first().focus();
        cy.press(Cypress.Keyboard.Keys.TAB);
        cy.dataCy('apply-step').eq(1).should('be.focused');
        cy.press(Cypress.Keyboard.Keys.SPACE);
        cy.dataCy('apply-step')
            .eq(1)
            .should('have.attr', 'aria-pressed', 'true');
        cy.dataCy('apply-description').should('contain.text', 'Regístrese');
        cy.dataCy('apply-illustration').should(
            'have.attr',
            'aria-hidden',
            'true',
        );
        cy.dataCy('apply-illustration').find('canvas').should('not.exist');
        cy.document().then(({ documentElement }) => {
            expect(documentElement.scrollWidth).to.eq(
                documentElement.clientWidth,
            );
        });
    });
});
