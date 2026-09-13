describe('E2E-05 · El postulante completa su perfil y postula (RF-08 a RF-11)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('completa perfil, carga su CV, postula y recibe la confirmación', function () {
        const vacancy = this.demo.vacancies.published;

        cy.loginAs('candidateNew');

        cy.visit(`/empleos/${vacancy.id}`);
        cy.dataCy('complete-profile').click();

        cy.location('pathname').should('eq', '/mi-perfil');
        cy.dataCy('profile-incomplete').should('be.visible');
        cy.dataCy('profile-phone').type('900000099');
        cy.dataCy('profile-city').type('Huancayo');
        cy.dataCy('profile-education-level').select(2);
        cy.dataCy('profile-years').type('3');
        cy.dataCy('profile-title').type('Licenciada en Educación Secundaria');
        cy.dataCy('save-profile').click();
        cy.dataCy('no-cv').should('be.visible');

        cy.dataCy('cv-input').selectFile('cypress/fixtures/cv-ficticio.pdf');
        cy.dataCy('upload-cv').click();
        cy.dataCy('current-cv').should('contain', 'cv-ficticio.pdf');
        cy.dataCy('profile-complete').should('be.visible');

        cy.visit(`/empleos/${vacancy.id}`);
        cy.dataCy('apply-button').click();

        cy.idFromPath(/^\/mis-postulaciones\/(\d+)$/);
        cy.dataCy('page-title').should('contain', vacancy.title);
        cy.dataCy('status-badge').first().should('contain', 'Postulación registrada');

        cy.visit(`/empleos/${vacancy.id}`);
        cy.dataCy('view-my-application').should('be.visible');
        cy.dataCy('apply-button').should('not.exist');

        cy.waitForQueue();
        cy.visit('/notificaciones');
        cy.dataCy('notification-item').first().should('contain', vacancy.title);
    });
});
