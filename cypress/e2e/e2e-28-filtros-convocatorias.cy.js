describe('RF-07 · Filtros del listado público de convocatorias', () => {
    before(() => cy.resetDatabase());

    it('combina puesto y tres filtros, restaura los controles y permite quitarlos', () => {
        cy.viewport(1440, 900);
        cy.visit('/empleos?page=9');
        cy.dataCy('jobs-first-page').should('be.visible');
        cy.dataCy('jobs-filter-organizacion')
            .find('option')
            .contains('Colegio Andino')
            .then(($option) => {
                cy.dataCy('jobs-filter-organizacion').select($option.val());
            });
        cy.dataCy('jobs-filter-ubicacion').select('Huancayo, Junín');
        cy.dataCy('jobs-filter-contrato').select('tiempo_completo');
        cy.dataCy('jobs-search').type('Comunicación{enter}');
        cy.dataCy('jobs-result-count').should('have.text', '1 convocatoria');
        cy.location('search').then((search) => {
            const params = new URLSearchParams(search);
            expect(params.has('page')).to.eq(false);
            expect(params.get('organizacion')).to.match(/^\d+$/);
            expect(params.get('q')).to.eq('Comunicación');
            expect(params.get('ubicacion')).to.eq('Huancayo, Junín');
            expect(params.get('contrato')).to.eq('tiempo_completo');
        });
        cy.reload();
        cy.dataCy('jobs-search').should('have.value', 'Comunicación');
        cy.dataCy('jobs-filter-ubicacion').should(
            'have.value',
            'Huancayo, Junín',
        );
        cy.dataCy('jobs-criterion').should('have.length', 4);
        cy.dataCy('job-card')
            .should('have.length', 1)
            .within(() => {
                cy.contains('h2', 'Docente de Comunicación');
                [
                    'Ubicación',
                    'Tipo de contrato',
                    'Plazas',
                    'Cierre de postulaciones',
                ].forEach((label) => cy.contains('dt', label));
            });
        cy.get('[data-key="contrato"]').click();
        cy.dataCy('jobs-filter-contrato').should('have.value', '');
        cy.go('back');
        cy.dataCy('jobs-filter-contrato').should(
            'have.value',
            'tiempo_completo',
        );
        cy.go('forward');
        cy.dataCy('jobs-filter-contrato').should('have.value', '');
        cy.dataCy('jobs-clear-filters').click();
        cy.dataCy('jobs-criterion').should('have.length', 1);
        cy.dataCy('jobs-search').should('have.value', 'Comunicación');
        cy.get('[data-key="q"]').click();
        cy.location('search').should('eq', '');
        cy.dataCy('jobs-criterion').should('not.exist');
    });

    it('permite operar a 320 px por teclado y limpiar una consulta sin coincidencias', () => {
        cy.viewport(320, 640);
        cy.visit('/empleos?q=astronauta&contrato=tiempo_completo');
        cy.dataCy('jobs-result-count').should('have.attr', 'role', 'status');
        cy.dataCy('jobs-result-count').should('have.text', '0 convocatorias');
        cy.contains(
            'Ninguna convocatoria coincide con «astronauta» y los filtros actuales',
        );
        cy.dataCy('jobs-search').focus();
        cy.press(Cypress.Keyboard.Keys.TAB);
        cy.dataCy('jobs-filters-toggle').should('be.focused');
        cy.press(Cypress.Keyboard.Keys.SPACE);
        cy.dataCy('jobs-filters-toggle').should(
            'have.attr',
            'aria-expanded',
            'true',
        );
        cy.press(Cypress.Keyboard.Keys.TAB);
        cy.dataCy('jobs-filter-organizacion').should('be.focused');
        cy.get('label[for="jobs-organizacion"]').should('be.visible');
        cy.dataCy('jobs-filter-contrato').should(
            'have.value',
            'tiempo_completo',
        );
        cy.document().then(({ documentElement: root }) =>
            expect(root.scrollWidth).to.eq(root.clientWidth),
        );
        cy.dataCy('jobs-clear-all').click();
        cy.location('search').should('eq', '');
        cy.dataCy('jobs-search').should('have.value', '');
        cy.dataCy('job-card').should('have.length.greaterThan', 0);
    });

    it('un parámetro inválido devuelve al listado con aviso y la página fuera de rango conserva el filtro', () => {
        cy.visit('/empleos?ubicacion%5B%5D=x');
        cy.dataCy('jobs-validation').should('have.attr', 'role', 'alert');
        cy.dataCy('jobs-validation').should(
            'contain.text',
            'La ubicación indicada no es válida.',
        );
        cy.location('search').should('eq', '');
        cy.visit('/empleos?contrato=tiempo_completo&page=9');
        cy.dataCy('jobs-first-page').click();
        cy.location('search').should('eq', '?contrato=tiempo_completo');
        cy.dataCy('deadline-passed').should('be.visible');
    });
});
