describe('E2E-08 · RR. HH. consulta la comparación y el ranking (RF-21, RF-22)', () => {
    before(() => cy.resetDatabase());

    beforeEach(() => cy.fixture('demo').as('demo'));

    it('muestra el ranking ponderado y explicable sin seleccionar a nadie', function () {
        const vacancy = this.demo.vacancies.ranking;
        const { rankingFirst, rankingSecond, rankingThird } = this.demo.applications;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${vacancy.id}`);
        cy.dataCy('vacancy-comparison').click();

        cy.location('pathname').should('eq', `/vacantes/${vacancy.id}/comparacion`);
        cy.dataCy('human-decision-notice').should('be.visible');
        cy.dataCy('ranking-formula').should('contain', 'ponderación');
        cy.dataCy('ranking-row').should('have.length', 3);

        [rankingFirst, rankingSecond, rankingThird].forEach((entry, index) => {
            cy.dataCy('ranking-row')
                .eq(index)
                .should('have.attr', 'data-position', String(index + 1))
                .and('contain', entry.candidate)
                .and('contain', 'Finalista')
                .find('[data-cy=ranking-total]')
                .should('have.text', entry.total);
        });

        // The ranking is decision support only: HR cannot decide and nothing has been selected.
        cy.dataCy('decision-panel').should('not.exist');
        cy.dataCy('decision-summary').should('not.exist');
        cy.dataCy('ranking-table').should('not.contain', 'Seleccionado');
    });
});
