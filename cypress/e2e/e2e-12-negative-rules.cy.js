// Priority negative scenarios through the real HTTP stack. Invalid login is covered in E2E-01; exhaustive
// authorization matrices stay in PHPUnit.
describe('Negativos · permisos y reglas del proceso', () => {
    before(() => cy.resetDatabase());

    beforeEach(() => cy.fixture('demo').as('demo'));

    it('un rol sin permiso no accede a pantallas de otros roles', () => {
        cy.loginAs('requester');
        cy.request({ url: '/auditoria', failOnStatusCode: false }).its('status').should('eq', 403);
        cy.request({ url: '/vacantes', failOnStatusCode: false }).its('status').should('eq', 403);

        cy.loginAs('candidate');
        cy.request({ url: '/requerimientos', failOnStatusCode: false }).its('status').should('eq', 403);
        cy.request({ url: '/mis-evaluaciones', failOnStatusCode: false }).its('status').should('eq', 403);

        cy.loginAs('evaluator');
        cy.request({ url: '/auditoria', failOnStatusCode: false }).its('status').should('eq', 403);
    });

    it('no se puede postular a una vacante cerrada', function () {
        const closed = this.demo.vacancies.closed;

        cy.loginAs('candidateComplete');
        cy.request({ url: `/empleos/${closed.id}`, failOnStatusCode: false }).its('status').should('eq', 404);

        cy.visit('/mis-postulaciones');
        cy.appRequest('POST', `/empleos/${closed.id}/postular`).then((response) => {
            expect(response.status).to.eq(422);
            expect(response.body.errors).to.have.property('workflow');
        });
        cy.reload();
        cy.dataCy('page-title').should('be.visible');
        cy.get('body').should('not.contain', closed.title);
    });

    it('solo el aprobador puede registrar la decisión final', function () {
        const vacancy = this.demo.vacancies.ranking;
        const body = {
            application_id: this.demo.applications.rankingFirst.id,
            justification: 'Intento de decisión por un rol no autorizado.',
            human_confirmation: true,
        };

        cy.loginAs('hr');
        cy.visit(`/vacantes/${vacancy.id}/comparacion`);
        cy.dataCy('decision-panel').should('not.exist');
        cy.appRequest('POST', `/vacantes/${vacancy.id}/decision`, body).its('status').should('eq', 403);

        cy.loginAs('evaluator');
        cy.visit('/dashboard');
        cy.appRequest('POST', `/vacantes/${vacancy.id}/decision`, body).its('status').should('eq', 403);

        cy.loginAs('approver');
        cy.visit(`/vacantes/${vacancy.id}/comparacion`);
        cy.dataCy('decision-summary').should('not.exist');
    });

    it('no se puede registrar una selección después del cierre', function () {
        const closed = this.demo.vacancies.closed;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${closed.id}/comparacion`);
        cy.dataCy('closure-summary').should('be.visible');
        cy.dataCy('register-selection').should('not.exist');
        cy.dataCy('close-vacancy').should('not.exist');

        cy.appRequest('POST', `/vacantes/${closed.id}/seleccion`).then((response) => {
            expect(response.status).to.eq(422);
            expect(response.body.errors).to.have.property('workflow');
        });
        cy.appRequest('POST', `/vacantes/${closed.id}/cerrar`).its('status').should('eq', 422);
    });
});
