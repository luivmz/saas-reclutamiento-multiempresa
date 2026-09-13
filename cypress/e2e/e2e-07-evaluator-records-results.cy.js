describe('E2E-07 · El evaluador registra resultados (RF-19, RF-20)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('registra los puntajes de la evaluación asignada dentro del rango de cada criterio', function () {
        const evaluation = this.demo.evaluations.pending;

        cy.loginAs('evaluator');
        cy.visit('/mis-evaluaciones');
        cy.get('[data-cy=assignment-row][data-status=programada]')
            .filter(`:contains("${evaluation.candidate}")`)
            .should('have.length', 1)
            .find('[data-cy=open-assignment]')
            .click();

        cy.location('pathname').should('eq', `/evaluaciones/${evaluation.id}`);
        cy.dataCy('score-row').should('have.length', 2);

        // RF-20: a score above the criterion maximum is rejected before anything is recorded.
        cy.dataCy('score-row').first().find('input[type=number]').type('25');
        cy.dataCy('score-row').eq(1).find('input[type=number]').type('15');
        cy.dataCy('record-results').click();
        cy.dataCy('score-row').first().find('input[type=number]').then(($input) => {
            expect($input[0].checkValidity()).to.equal(false);
        });
        cy.dataCy('recorded-results').should('not.exist');

        cy.dataCy('score-row').first().find('input[type=number]').clear().type('17');
        cy.dataCy('session-observations').type('Buen dominio de los contenidos (E2E).');
        cy.dataCy('record-results').click();

        cy.dataCy('recorded-results').should('be.visible').and('contain', '17').and('contain', '15');
        cy.dataCy('record-results').should('not.exist');

        cy.visit('/mis-evaluaciones');
        cy.get('[data-cy=assignment-row][data-status=programada]')
            .filter(`:contains("${evaluation.candidate}")`)
            .should('have.length', 0);
    });
});
