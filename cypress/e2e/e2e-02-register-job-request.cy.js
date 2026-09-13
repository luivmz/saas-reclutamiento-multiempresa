describe('E2E-02 · El área solicitante registra un requerimiento (RF-01)', () => {
    beforeEach(() => cy.resetDatabase());

    it('registra el requerimiento y lo envía a RR. HH.', () => {
        const title = 'Docente de Ciencias - Secundaria (E2E)';

        cy.loginAs('requester');
        cy.visit('/requerimientos');
        cy.dataCy('new-job-request').click();

        cy.location('pathname').should('eq', '/requerimientos/crear');
        cy.dataCy('position_title').type(title);
        cy.dataCy('area').type('Coordinación Académica');
        cy.dataCy('headcount').clear().type('2');
        cy.dataCy('contract_type').select(1);
        cy.dataCy('justification').type('Ampliación de secciones de ciencias para el siguiente periodo (dato ficticio).');
        cy.dataCy('save-job-request').click();

        cy.idFromPath(/^\/requerimientos\/(\d+)$/);
        cy.dataCy('page-title').should('contain', title);
        cy.dataCy('status-badge').first().should('contain', 'Borrador');

        cy.dataCy('submit-job-request').click();
        cy.dataCy('status-badge').first().should('contain', 'Enviado a RR. HH.');
        cy.dataCy('submit-job-request').should('not.exist');

        cy.visit('/requerimientos');
        cy.dataCy('job-request-row').first().should('contain', title).and('contain', 'Enviado a RR. HH.');
    });

    it('no registra un requerimiento con datos obligatorios vacíos', () => {
        cy.loginAs('requester');
        cy.visit('/requerimientos');
        cy.dataCy('job-request-row').its('length').then((before) => {
            cy.visit('/requerimientos/crear');
            cy.dataCy('save-job-request').click();
            cy.location('pathname').should('eq', '/requerimientos/crear');
            cy.dataCy('position_title').should('have.value', '');

            cy.visit('/requerimientos');
            cy.dataCy('job-request-row').should('have.length', before);
        });
    });
});
