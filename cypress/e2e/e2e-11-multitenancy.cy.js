// Complements the main tenant-isolation coverage in PHPUnit (CrossTenantAccessTest, OrganizationScopeTest):
// here only the most visible cases are checked through the real UI and HTTP stack.
const denied = (status) => expect([403, 404]).to.include(status);

describe('Multitenancy · aislamiento entre organizaciones', () => {
    before(() => cy.resetDatabase());

    beforeEach(() => cy.fixture('demo').as('demo'));

    it('RR. HH. de la organización B solo ve sus vacantes y no accede a recursos de A', function () {
        const { published, ranking } = this.demo.vacancies;

        cy.loginAs('hrOrgB');
        cy.visit('/vacantes');
        cy.dataCy('vacancy-row').should('have.length', 1).and('contain', this.demo.vacancies.orgB.title);
        cy.dataCy('vacancies-table').should('not.contain', published.title).and('not.contain', ranking.title);

        cy.request({ url: `/vacantes/${published.id}`, failOnStatusCode: false }).its('status').then(denied);
        cy.request({ url: `/postulaciones/${this.demo.applications.submitted.id}`, failOnStatusCode: false }).its('status').then(denied);
        cy.request({ url: `/requerimientos/${this.demo.requests.validated.id}`, failOnStatusCode: false }).its('status').then(denied);
    });

    it('RR. HH. de la organización A no ve la vacante de B', function () {
        cy.loginAs('hr');
        cy.visit('/vacantes');
        cy.dataCy('vacancies-table').should('not.contain', this.demo.vacancies.orgB.title);
        cy.request({ url: `/vacantes/${this.demo.vacancies.orgB.id}`, failOnStatusCode: false }).its('status').then(denied);
    });

    it('la auditoría de cada organización no muestra registros de la otra', () => {
        cy.loginAs('approverOrgB');
        cy.visit('/auditoria');
        cy.dataCy('audit-row').should('have.length.at.least', 1);
        cy.dataCy('audit-table').should('contain', 'Ana Torres (demo B)').and('not.contain', 'Luis Paredes (demo)');

        cy.loginAs('approver');
        cy.visit('/auditoria');
        cy.dataCy('audit-table').should('contain', 'Luis Paredes (demo)').and('not.contain', 'Ana Torres (demo B)');
    });

    it('rechaza acciones sobre identificadores de otra organización', function () {
        const application = this.demo.applications.submitted;

        cy.loginAs('hrOrgB');
        cy.visit('/dashboard');
        cy.appRequest('POST', `/postulaciones/${application.id}/preseleccionar`).its('status').then(denied);
        cy.appRequest('POST', `/vacantes/${this.demo.vacancies.ranking.id}/cerrar`).its('status').then(denied);

        cy.loginAs('approverOrgB');
        cy.visit('/dashboard');
        cy.appRequest('POST', `/vacantes/${this.demo.vacancies.ranking.id}/decision`, {
            application_id: this.demo.applications.rankingFirst.id,
            justification: 'Intento desde otra organización.',
            human_confirmation: true,
        })
            .its('status')
            .then(denied);

        cy.loginAs('hr');
        cy.visit(`/postulaciones/${application.id}`);
        cy.dataCy('status-badge').first().should('contain', 'Postulación registrada');
        cy.visit(`/vacantes/${this.demo.vacancies.ranking.id}/comparacion`);
        cy.dataCy('decision-summary').should('not.exist');
    });
});
