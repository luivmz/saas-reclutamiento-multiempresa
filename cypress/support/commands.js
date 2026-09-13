const e2eHeaders = () => ({ 'X-E2E-Token': Cypress.env('E2E_TOKEN') });

// Element by its stable data-cy attribute.
Cypress.Commands.add('dataCy', (name) => cy.get(`[data-cy="${name}"]`));

// Restores the known DemoSeeder state (fresh schema, no pending jobs, no cached rate limits).
Cypress.Commands.add('resetDatabase', () => {
    cy.request({ method: 'POST', url: '/__e2e/reset', headers: e2eHeaders(), timeout: 120000 })
        .its('body.reset')
        .should('eq', true);
});

// Signs in through the real login form once per role and restores the session afterwards.
Cypress.Commands.add('loginAs', (role) => {
    cy.fixture('users').then((users) => {
        const email = users[role];

        if (!email) {
            throw new Error(`Unknown demo role "${role}"`);
        }

        cy.session(
            ['demo-user', role],
            () => {
                cy.visit('/login');
                cy.dataCy('login-email').type(email);
                cy.dataCy('login-password').type(Cypress.env('DEMO_PASSWORD'), { log: false });
                cy.dataCy('login-submit').click();
                cy.location('pathname').should('eq', '/dashboard');
            },
            {
                validate() {
                    cy.request({ url: '/dashboard', followRedirect: false }).its('status').should('eq', 200);
                },
            },
        );
    });
});

// Waits until the queue worker has delivered every pending job (e.g. notifications), polling the real queue size.
Cypress.Commands.add('waitForQueue', (attempts = 40) => {
    cy.request({ url: '/__e2e/queue', headers: e2eHeaders(), log: false })
        .its('body.pending', { log: false })
        .then((pending) => {
            if (pending === 0) {
                return;
            }

            if (attempts <= 0) {
                throw new Error(`The queue still has ${pending} pending job(s); is the "queue" service running?`);
            }

            // Short poll interval between two real state checks, not a fixed wait for the UI.
            cy.wait(250, { log: false });
            cy.waitForQueue(attempts - 1);
        });
});

// Sends a request as the signed-in user (CSRF header included) and yields the raw response, for negative checks.
Cypress.Commands.add('appRequest', (method, url, body = {}) => {
    cy.getCookie('XSRF-TOKEN').then((cookie) =>
        cy.request({
            method,
            url,
            body,
            failOnStatusCode: false,
            followRedirect: false,
            headers: {
                Accept: 'application/json',
                'X-XSRF-TOKEN': cookie ? decodeURIComponent(cookie.value) : '',
            },
        }),
    );
});

// Pathname id captured after a redirect, e.g. idFromPath(/^\/vacantes\/(\d+)$/).
Cypress.Commands.add('idFromPath', (pattern) =>
    cy
        .location('pathname')
        .should('match', pattern)
        .then((pathname) => Number(pathname.match(pattern)[1])),
);
