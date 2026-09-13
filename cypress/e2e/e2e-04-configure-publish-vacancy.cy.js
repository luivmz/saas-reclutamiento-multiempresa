import { appDate } from '../support/dates';

const today = () => appDate(0);
const inDays = (days) => appDate(days);

describe('E2E-04 · RR. HH. configura y publica una vacante (RF-05 a RF-07)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('genera la vacante desde un requerimiento aprobado, la valida y la publica', function () {
        const request = this.demo.requests.approvedWithoutVacancy;
        const title = 'Docente de Religión - Secundaria (E2E)';

        cy.loginAs('hr');
        cy.visit(`/requerimientos/${request.id}`);
        cy.dataCy('create-vacancy-from-request').click();

        cy.dataCy('vacancy-form').should('be.visible');
        cy.dataCy('vacancy-job-request').should('have.value', String(request.id));
        cy.dataCy('vacancy-title').clear().type(title);
        cy.dataCy('vacancy-summary').clear().type('Convocatoria ficticia creada por la suite E2E.');
        cy.dataCy('vacancy-contract-type').select(1);
        cy.dataCy('vacancy-opens-at').clear().type(today());
        cy.dataCy('vacancy-closes-at').clear().type(inDays(30));
        cy.dataCy('profile-education').clear().type('Título profesional en Educación Religiosa');
        cy.dataCy('profile-experience').clear().type('Mínimo 2 años');
        cy.dataCy('profile-functions').clear().type('Desarrollar sesiones de educación religiosa.');
        cy.dataCy('profile-competencies').clear().type('Comunicación y trabajo en equipo.');
        cy.dataCy('criterion-row').should('have.length.at.least', 1);
        cy.dataCy('weight-total').should('contain', '100');
        cy.dataCy('save-vacancy').click();

        cy.idFromPath(/^\/vacantes\/(\d+)$/).then((vacancyId) => {
            cy.dataCy('status-badge').first().should('contain', 'Borrador');
            cy.dataCy('validation-ok').should('be.visible');
            cy.dataCy('publish-vacancy').click();
            cy.dataCy('status-badge').first().should('contain', 'Publicada');

            cy.visit('/empleos');
            cy.dataCy('job-card').should('contain', title);
            cy.visit(`/empleos/${vacancyId}`);
            cy.dataCy('page-title').should('contain', title);
        });
    });

    it('impide publicar si las ponderaciones no suman 100', function () {
        const { id } = this.demo.vacancies.draft;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}/editar`);
        cy.dataCy('criterion-row').first().find('input[type=number]').first().clear().type('10');
        cy.dataCy('weight-total').should('not.contain', '100 / 100');
        cy.dataCy('save-vacancy').click();

        cy.location('pathname').should('eq', `/vacantes/${id}`);
        cy.dataCy('validation-issues').should('be.visible');
        cy.dataCy('publish-vacancy').should('be.disabled');

        // The server also rejects a direct publication attempt (RF-06/RF-20), not only the disabled button.
        cy.appRequest('POST', `/vacantes/${id}/publicar`).its('status').should('eq', 422);
        cy.reload();
        cy.dataCy('status-badge').first().should('contain', 'Borrador');
    });
});
