// E2E-20 · Reportes de reclutamiento (RF-28, candidato).
//
// Valores esperados derivados de DemoSeeder (docs/demo-users.md) tras /__e2e/reset. Organización A
// (Colegio Andino demo): 9 postulaciones en 3 vacantes publicadas hoy. Etapas actuales: 1 postulación
// registrada, 1 preseleccionada, 1 en evaluación, 3 finalistas, 1 seleccionada y 2 no seleccionadas;
// 8 pasaron por la preselección. Organización Demo B: 1 postulación registrada en 1 vacante.
// Las pruebas exhaustivas de cálculo y aislamiento están en tests/Feature/Reports/RecruitmentReportTest.php.

const kpi = (name) => cy.dataCy(`kpi-${name}`);

const statusCount = (status) => cy.get(`[data-cy=chart-status-row][data-status=${status}]`);

describe('E2E-20 · Reportes de reclutamiento (RF-28, candidato)', () => {
    before(() => cy.resetDatabase());

    beforeEach(() => cy.fixture('demo').as('demo'));

    it('RR. HH. abre Reportes desde el menú y ve indicadores calculados desde la base de datos', function () {
        cy.loginAs('hr');
        cy.visit('/dashboard');
        cy.dataCy('nav-reports').should('be.visible').click();

        cy.location('pathname').should('eq', '/reportes');
        cy.dataCy('page-title').should('contain', 'Reportes de reclutamiento');

        kpi('applications').should('have.attr', 'data-value', '9');
        kpi('published-vacancies').should('have.attr', 'data-value', '3');
        kpi('average-per-vacancy').should('have.attr', 'data-value', '3');
        kpi('reached-shortlist').should('have.attr', 'data-value', '8').and('contain', '88.9 %');
        kpi('in-assessment').should('have.attr', 'data-value', '1');

        statusCount('postulado').should('have.attr', 'data-count', '1');
        statusCount('finalista').should('have.attr', 'data-count', '3');
        statusCount('no_seleccionado').should('have.attr', 'data-count', '2');

        cy.dataCy('chart-week-column').filter('[data-count="9"]').should('have.length', 1);
        cy.dataCy('report-vacancy-row').should('have.length', 3);
        cy.dataCy('report-by-vacancy')
            .should('contain', this.demo.vacancies.published.title)
            .and('contain', this.demo.vacancies.ranking.title)
            .and('contain', this.demo.vacancies.closed.title)
            .and('not.contain', this.demo.vacancies.orgB.title)
            .and('not.contain', this.demo.vacancies.draft.title);

        cy.screenshot('E2E-20-01-reportes-rrhh-organizacion-a', { capture: 'fullPage' });
    });

    it('el filtro por vacante recalcula indicadores, gráficos y tabla', function () {
        const ranking = this.demo.vacancies.ranking;

        cy.loginAs('hr');
        cy.visit('/reportes');
        cy.dataCy('report-filter-vacante').select(String(ranking.id));
        cy.dataCy('report-filter-apply').click();

        cy.location('search').should('contain', `vacante=${ranking.id}`);
        kpi('applications').should('have.attr', 'data-value', '3');
        kpi('published-vacancies').should('have.attr', 'data-value', '1');
        statusCount('finalista').should('have.attr', 'data-count', '3');
        statusCount('postulado').should('have.attr', 'data-count', '0');
        cy.dataCy('report-vacancy-row').should('have.length', 1).and('have.attr', 'data-code');
        cy.dataCy('report-by-vacancy').should('contain', ranking.title);

        cy.screenshot('E2E-20-02-filtro-por-vacante', { capture: 'fullPage' });
    });

    it('el filtro por etapa actual limita el conjunto analizado', () => {
        cy.loginAs('hr');
        cy.visit('/reportes');
        cy.dataCy('report-filter-estado').select('no_seleccionado');
        cy.dataCy('report-filter-apply').click();

        cy.location('search').should('contain', 'estado=no_seleccionado');
        kpi('applications').should('have.attr', 'data-value', '2');
        kpi('reached-shortlist').should('have.attr', 'data-value', '2');
        statusCount('no_seleccionado').should('have.attr', 'data-count', '2');
        statusCount('finalista').should('have.attr', 'data-count', '0');
    });

    it('un período sin registros muestra cero y un estado vacío, sin datos de ejemplo', () => {
        cy.loginAs('hr');
        cy.visit('/reportes');
        cy.dataCy('report-filter-desde').clear().type('2025-01-01');
        cy.dataCy('report-filter-hasta').clear().type('2025-01-31');
        cy.dataCy('report-filter-apply').click();

        cy.location('search').should('contain', 'desde=2025-01-01').and('contain', 'hasta=2025-01-31');
        kpi('applications').should('have.attr', 'data-value', '0');
        kpi('reached-shortlist').should('contain', '—');
        cy.dataCy('empty-state').should('be.visible');
        cy.dataCy('chart-by-status').should('not.exist');

        cy.dataCy('report-filter-clear').click();
        cy.location('search').should('eq', '');
        kpi('applications').should('have.attr', 'data-value', '9');
    });

    it('refleja al instante una preselección registrada en el sistema', function () {
        const application = this.demo.applications.submitted;

        cy.loginAs('hr');
        cy.visit('/reportes');
        kpi('reached-shortlist').should('have.attr', 'data-value', '8');

        cy.visit(`/postulaciones/${application.id}`);
        cy.dataCy('shortlist-comment').type('Cumple el perfil (E2E reportes).');
        cy.dataCy('shortlist-application').click();
        cy.dataCy('status-badge').first().should('contain', 'Preseleccionado');

        cy.visit('/reportes');
        kpi('reached-shortlist').should('have.attr', 'data-value', '9').and('contain', '100 %');
        statusCount('postulado').should('have.attr', 'data-count', '0');
        statusCount('preseleccionado').should('have.attr', 'data-count', '2');
    });

    it('la organización B solo ve sus propios indicadores', function () {
        cy.loginAs('hrOrgB');
        cy.visit('/reportes');

        kpi('applications').should('have.attr', 'data-value', '1');
        kpi('published-vacancies').should('have.attr', 'data-value', '1');
        cy.dataCy('report-vacancy-row').should('have.length', 1);
        cy.dataCy('report-by-vacancy')
            .should('contain', this.demo.vacancies.orgB.title)
            .and('not.contain', this.demo.vacancies.published.title);
        cy.dataCy('report-filter-vacante')
            .find('option')
            .should('have.length', 2)
            .and('not.contain', this.demo.vacancies.ranking.title);

        cy.screenshot('E2E-20-06-reportes-organizacion-b', { capture: 'fullPage' });
    });

    it('rechaza filtrar por una vacante de otra organización sin filtrar sus datos', function () {
        cy.loginAs('hrOrgB');
        cy.visit(`/reportes?vacante=${this.demo.vacancies.ranking.id}`);

        cy.location('pathname').should('eq', '/reportes');
        cy.location('search').should('eq', '');
        cy.contains('La vacante seleccionada no está disponible en su organización.').should('be.visible');
        kpi('applications').should('have.attr', 'data-value', '1');
        cy.dataCy('report-by-vacancy').should('not.contain', this.demo.vacancies.ranking.title);
    });

    it('los roles sin permiso no acceden ni ven el menú de reportes', () => {
        ['requester', 'evaluator', 'candidate'].forEach((role) => {
            cy.loginAs(role);
            cy.visit('/dashboard');
            cy.dataCy('nav-reports').should('not.exist');
            cy.request({ url: '/reportes', failOnStatusCode: false }).its('status').should('eq', 403);
        });
    });

    it('el aprobador también lo consulta, y en móvil la página no se desborda', () => {
        cy.viewport(390, 844);
        cy.loginAs('approver');
        cy.visit('/reportes');

        kpi('applications').should('have.attr', 'data-value', '9');
        cy.dataCy('report-vacancy-table').should('be.visible');
        cy.document().then((doc) => {
            expect(doc.documentElement.scrollWidth, 'sin desplazamiento horizontal').to.be.at.most(390);
        });

        cy.screenshot('E2E-20-09-reportes-aprobador-movil', { capture: 'fullPage' });
    });
});
