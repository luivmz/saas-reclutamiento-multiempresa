describe('E2E-10 · RR. HH. registra la selección y cierra el proceso (RF-24 a RF-26)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('registra la selección decidida por Dirección, cierra la convocatoria y notifica el resultado', function () {
        const vacancy = this.demo.vacancies.ranking;
        const { rankingFirst, rankingSecond } = this.demo.applications;

        // Precondition through the UI: the approver's human decision.
        cy.loginAs('approver');
        cy.visit(`/vacantes/${vacancy.id}/comparacion`);
        cy.get(`[data-cy=decision-candidate-${rankingFirst.id}]`).check();
        cy.dataCy('decision-justification').type('Mayor puntaje y desempeño consistente (E2E).');
        cy.dataCy('decision-human-confirmation').check();
        cy.dataCy('submit-final-decision').click();
        cy.dataCy('decision-summary').should('contain', rankingFirst.candidate);

        cy.loginAs('hr');
        cy.visit(`/vacantes/${vacancy.id}/comparacion`);
        cy.dataCy('decision-summary').should('contain', 'Pendiente (RR. HH.)');
        cy.dataCy('register-selection').click();

        cy.dataCy('decision-summary').should('not.contain', 'Pendiente (RR. HH.)');
        cy.contains('[data-cy=ranking-row]', rankingFirst.candidate).should('contain', 'Seleccionado');
        cy.contains('[data-cy=ranking-row]', rankingSecond.candidate).should('contain', 'Finalista');
        cy.dataCy('register-selection').should('not.exist');

        cy.dataCy('closure-notes').type('Proceso concluido (E2E).');
        cy.dataCy('close-vacancy').click();

        cy.dataCy('closure-summary').should('contain', 'Cerrada con selección');
        cy.dataCy('status-badge').first().should('contain', 'Cerrada');
        cy.dataCy('closure-panel').should('not.exist');
        cy.contains('[data-cy=ranking-row]', rankingSecond.candidate).should('contain', 'No seleccionado');

        // RF-26: each candidate receives only their own result, after the closure.
        cy.waitForQueue();
        cy.loginAs('candidateRankingFirst');
        cy.visit('/notificaciones');
        cy.dataCy('notification-item').first().should('contain', vacancy.title).and('contain', 'seleccionado(a)');

        cy.loginAs('candidateRankingSecond');
        cy.visit('/notificaciones');
        cy.dataCy('notification-item').first().should('contain', vacancy.title).and('contain', 'no seleccionado');
    });
});
