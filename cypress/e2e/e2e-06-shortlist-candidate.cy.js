describe('E2E-06 · RR. HH. preselecciona a un candidato (RF-12 a RF-15)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('revisa la postulación, la preselecciona y el postulante es notificado', function () {
        const vacancy = this.demo.vacancies.published;
        const application = this.demo.applications.submitted;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${vacancy.id}/postulaciones`);
        cy.contains('[data-cy=application-row]', application.candidate).find('[data-cy=application-link]').click();

        cy.location('pathname').should('eq', `/postulaciones/${application.id}`);
        cy.dataCy('status-badge').first().should('contain', 'Postulación registrada');
        cy.dataCy('application-cv').should('be.visible');
        cy.dataCy('shortlist-comment').type('Cumple el perfil (E2E).');
        cy.dataCy('shortlist-application').click();

        cy.dataCy('status-badge').first().should('contain', 'Preseleccionado');
        cy.dataCy('status-timeline').should('contain', 'Preseleccionado');
        cy.dataCy('shortlist-application').should('not.exist');

        cy.waitForQueue();
        cy.loginAs('candidateSubmitted');
        cy.visit('/notificaciones');
        cy.dataCy('notification-item').first().should('contain', vacancy.title).and('contain', 'Preseleccionado');
    });

    it('no descarta una postulación sin indicar el motivo', function () {
        const application = this.demo.applications.submitted;

        cy.loginAs('hr');
        cy.visit(`/postulaciones/${application.id}`);
        cy.dataCy('discard-application').click();

        cy.dataCy('stage-panel').should('be.visible');
        cy.dataCy('status-badge').first().should('contain', 'Postulación registrada');
    });
});
