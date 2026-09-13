describe('E2E-01 · Inicio de sesión por rol', () => {
    const roles = [
        { role: 'requester', label: 'Área solicitante', visible: 'nav-new-job-request', hidden: 'nav-audit' },
        { role: 'hr', label: 'Recursos Humanos', visible: 'nav-vacancies', hidden: 'nav-audit' },
        { role: 'approver', label: 'Aprobador / Dirección', visible: 'nav-audit', hidden: 'nav-new-job-request' },
        { role: 'evaluator', label: 'Evaluador', visible: 'nav-assessments', hidden: 'nav-vacancies' },
        { role: 'candidate', label: 'Postulante', visible: 'nav-my-applications', hidden: 'nav-job-requests' },
    ];

    before(() => cy.resetDatabase());

    const submitLogin = (email, password) => {
        cy.visit('/login');
        cy.dataCy('login-email').type(email);
        cy.dataCy('login-password').type(password, { log: false });
        cy.dataCy('login-submit').click();
    };

    roles.forEach(({ role, label, visible, hidden }) => {
        it(`${label}: inicia sesión y ve solo el menú de su rol`, () => {
            cy.fixture('users').then((users) => submitLogin(users[role], Cypress.env('DEMO_PASSWORD')));

            cy.location('pathname').should('eq', '/dashboard');
            cy.dataCy('page-title').should('be.visible');
            cy.dataCy('status-badge').first().should('contain', label);
            cy.dataCy(visible).should('be.visible');
            cy.dataCy(hidden).should('not.exist');
        });
    });

    it('rechaza credenciales inválidas sin iniciar sesión', () => {
        cy.fixture('users').then((users) => submitLogin(users.hr, 'contraseña-incorrecta'));

        cy.dataCy('login-error').should('be.visible');
        cy.location('pathname').should('eq', '/login');
        cy.request({ url: '/dashboard', followRedirect: false }).its('status').should('eq', 302);
    });
});
