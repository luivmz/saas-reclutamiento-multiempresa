/**
 * Panel de riesgo operacional en el navegador.
 *
 * El entorno E2E corre sin servicio ML —`ML_SERVICE_ENABLED=false` por
 * omisión—, así que lo que se valida aquí es lo que un usuario ve cuando no
 * hay predicción: **el panel aparece, explica por qué y no inventa nada**. Es
 * el camino que más veces recorrerá alguien real, porque el servicio es
 * experimental y puede estar apagado.
 *
 * El camino predictivo se cubre en las pruebas de integración de Laravel y en
 * el smoke con FastAPI levantado; reproducirlo aquí exigiría un servicio Python
 * dentro de la infraestructura de E2E, que es alcance de otra fase.
 */
describe('E2E-15 · Panel de riesgo operacional (RF-29, experimental)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('muestra el panel en una vacante publicada, sin inventar una estimación', function () {
        const { id } = this.demo.vacancies.published;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);

        cy.dataCy('operational-risk-panel').should('be.visible');
        cy.dataCy('operational-risk-availability').should('be.visible');

        // Sin predicción no hay porcentaje: nada de un 0 % que se leería como
        // "riesgo nulo".
        cy.dataCy('operational-risk-score').should('not.exist');
        cy.dataCy('operational-risk-message').should('not.be.empty');
    });

    it('declara su naturaleza experimental y que no decide nada', function () {
        const { id } = this.demo.vacancies.published;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);

        cy.dataCy('operational-risk-panel').within(() => {
            cy.contains('Experimental').should('be.visible');
            cy.contains('Riesgo operacional del proceso').should('be.visible');
            cy.contains('no sobre las personas postulantes').should('be.visible');
            cy.contains('decisión final corresponde al Aprobador').should('be.visible');
        });
    });

    it('nunca habla de candidatos, ranking ni recomendaciones', function () {
        const { id } = this.demo.vacancies.published;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);

        cy.dataCy('operational-risk-panel')
            .invoke('text')
            .then((text) => {
                const lowered = text.toLowerCase();
                [
                    'ranking',
                    'mejor candidato',
                    'recomendamos',
                    'debe contratar',
                    'debe descartar',
                    'puntaje del postulante',
                ].forEach((forbidden) => {
                    expect(lowered, `texto prohibido: ${forbidden}`).not.to.contain(forbidden);
                });
            });
    });

    it('evita lenguaje alarmista pese a la tasa de alerta alta', function () {
        const { id } = this.demo.vacancies.published;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);

        cy.dataCy('operational-risk-panel')
            .invoke('text')
            .then((text) => {
                const upper = text.toUpperCase();
                ['ALERTA CRÍTICA', 'RIESGO SEVERO', 'URGENTE', 'PELIGRO'].forEach((word) => {
                    expect(upper, `tono alarmista: ${word}`).not.to.contain(word);
                });
            });
    });

    it('no aparece en una vacante en borrador', function () {
        const { id } = this.demo.vacancies.draft;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);

        // Sin publicar no hay proceso que estimar.
        cy.dataCy('validation-panel').should('be.visible');
        cy.dataCy('operational-risk-panel').should('not.exist');
    });

    it('el Aprobador también lo ve', function () {
        const { id } = this.demo.vacancies.published;

        cy.loginAs('approver');
        cy.visit(`/vacantes/${id}`);

        cy.dataCy('operational-risk-panel').should('be.visible');
    });

    it('un postulante no puede consultar el riesgo por la ruta directa', function () {
        const { id } = this.demo.vacancies.published;

        cy.loginAs('candidate');
        cy.request({
            url: `/vacantes/${id}/riesgo-operacional`,
            failOnStatusCode: false,
        })
            .its('status')
            .should('eq', 403);
    });

    it('una organización no alcanza el riesgo de otra', function () {
        const foreign = this.demo.vacancies.orgB.id;

        cy.loginAs('hr');
        cy.request({
            url: `/vacantes/${foreign}/riesgo-operacional`,
            failOnStatusCode: false,
        })
            .its('status')
            .should('eq', 404);
    });
});
