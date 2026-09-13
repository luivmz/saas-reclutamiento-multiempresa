describe('E2E-09 · El aprobador registra la decisión final humana (RF-23)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('exige justificación y confirmación humana antes de registrar la decisión', function () {
        const vacancy = this.demo.vacancies.ranking;
        const chosen = this.demo.applications.rankingSecond;

        cy.loginAs('approver');
        cy.visit(`/vacantes/${vacancy.id}/comparacion`);
        cy.dataCy('decision-panel').should('be.visible');
        cy.get(`[data-cy=decision-candidate-${chosen.id}]`).check();
        cy.dataCy('submit-final-decision').click();

        cy.dataCy('decision-panel').should('be.visible');
        cy.dataCy('decision-summary').should('not.exist');
    });

    it('registra la decisión eligiendo a un candidato que no es el primero del ranking', function () {
        const vacancy = this.demo.vacancies.ranking;
        const chosen = this.demo.applications.rankingSecond;

        cy.loginAs('approver');
        cy.visit(`/vacantes/${vacancy.id}/comparacion`);
        cy.dataCy('ranking-row').first().should('not.contain', chosen.candidate);

        cy.get(`[data-cy=decision-candidate-${chosen.id}]`).check();
        cy.dataCy('decision-justification').type('Mejor desempeño en la entrevista y experiencia en el nivel inicial (E2E).');
        cy.dataCy('decision-human-confirmation').check();
        cy.dataCy('submit-final-decision').click();

        cy.dataCy('decision-summary')
            .should('contain', chosen.candidate)
            .and('contain', '2 de 3')
            .and('contain', 'Pendiente (RR. HH.)');
        cy.dataCy('decision-panel').should('not.exist');

        // Registering the decision does not change any application status (approved rule 1).
        cy.dataCy('ranking-row').each(($row) => cy.wrap($row).should('contain', 'Finalista'));
    });
});
