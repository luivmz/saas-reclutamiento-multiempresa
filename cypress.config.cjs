// Cypress E2E suite configuration. See docs/testing/cypress-e2e.md and docs/docker.md.
const fs = require('fs');
const path = require('path');

// Token for the guarded /__e2e/* endpoints of the isolated E2E app: CYPRESS_E2E_TOKEN or E2E_TOKEN (Docker, from
// .env.e2e) or, for `cypress open` on the host, E2E_TOKEN read from .env.e2e.
function tokenFromEnvFile(file) {
    try {
        const line = fs
            .readFileSync(path.join(__dirname, file), 'utf8')
            .split(/\r?\n/)
            .find((entry) => entry.startsWith('E2E_TOKEN='));

        return line ? line.slice('E2E_TOKEN='.length).trim() : '';
    } catch {
        return '';
    }
}

module.exports = {
    e2e: {
        // app-e2e published on the host; overridden by CYPRESS_baseUrl (http://app-e2e:8000 inside Docker Compose).
        baseUrl: 'http://localhost:8001',
        specPattern: 'cypress/e2e/**/*.cy.js',
        supportFile: 'cypress/support/e2e.js',
        fixturesFolder: 'cypress/fixtures',
        screenshotsFolder: 'cypress/screenshots',
        videosFolder: 'cypress/videos',
        screenshotOnRunFailure: true,
        video: false,
        testIsolation: true,
        viewportWidth: 1280,
        viewportHeight: 800,
        defaultCommandTimeout: 10000,
        pageLoadTimeout: 60000,
        // No automatic retries: an intermittent failure must be investigated, not hidden.
        retries: { runMode: 0, openMode: 0 },
        env: {
            APP_TIMEZONE: 'America/Lima',
            DEMO_PASSWORD: 'password',
            E2E_TOKEN: process.env.CYPRESS_E2E_TOKEN || process.env.E2E_TOKEN || tokenFromEnvFile('.env.e2e'),
        },
    },
};
