describe('E2E-03 · El aprobador decide un requerimiento validado (RF-03, RF-04)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('aprueba el requerimiento validado por RR. HH.', function () {
        const { id } = this.demo.requests.validated;

        cy.loginAs('approver');
        cy.visit(`/requerimientos/${id}`);
        cy.dataCy('status-badge').first().should('contain', 'Validado por RR. HH.');
        cy.dataCy('decision-approve').check();
        cy.dataCy('decision-comment').type('Plaza presupuestada para el periodo (validación E2E).');
        cy.dataCy('submit-decision').click();

        cy.dataCy('status-badge').first().should('contain', 'Aprobado');
        cy.dataCy('decision-panel').should('not.exist');
        cy.dataCy('status-timeline').should('contain', 'Aprobado');
    });

    it('no permite rechazar sin indicar el motivo', function () {
        const { id } = this.demo.requests.validated;

        cy.loginAs('approver');
        cy.visit(`/requerimientos/${id}`);
        cy.dataCy('decision-reject').check();
        cy.dataCy('submit-decision').click();

        cy.dataCy('decision-panel').should('contain', 'motivo');
        cy.dataCy('status-badge').first().should('contain', 'Validado por RR. HH.');
    });
});
