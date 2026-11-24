/**
 * E2E-27 · Lote 2 de UX: portada para postulantes, requisitos antes del
 * registro, cabecera pública en móvil y continuidad de la convocatoria.
 *
 * Crear la cuenta, iniciar sesión o completar el perfil devuelven a la
 * convocatoria de la que se venía. Solo se admite el identificador de una
 * convocatoria publicada; volver nunca postula por nadie.
 */
const entrarConFormulario = (email) => {
    cy.dataCy('login-email').type(email);
    cy.dataCy('login-password').type(Cypress.env('DEMO_PASSWORD'), {
        log: false,
    });
    cy.dataCy('login-submit').click();
};

describe('E2E-27 · Continuidad de la convocatoria y portada para postulantes', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
        cy.fixture('users').as('users');
    });

    it('acceso → convocatoria → perfil y CV → vuelta a la convocatoria, sin postular por nadie', function () {
        const vacancy = this.demo.vacancies.published;

        cy.visit(`/empleos/${vacancy.id}`);
        cy.dataCy('application-requirements').should(
            'contain',
            'PDF de hasta 5 MB',
        );
        cy.dataCy('apply-login').click();

        cy.location('search').should('eq', `?convocatoria=${vacancy.id}`);
        cy.dataCy('return-notice').should('contain', vacancy.title);
        entrarConFormulario(this.users.candidateNew);

        cy.location('pathname').should('eq', `/empleos/${vacancy.id}`);
        cy.dataCy('complete-profile').click();

        cy.location('pathname').should('eq', '/mi-perfil');
        cy.dataCy('profile-return').should('contain', vacancy.title);
        cy.dataCy('return-to-vacancy').should('not.exist');

        cy.dataCy('profile-phone').type('900000099');
        cy.dataCy('profile-city').type('Huancayo');
        cy.dataCy('profile-education-level').select(2);
        cy.dataCy('profile-years').type('3');
        cy.dataCy('profile-title').type('Licenciada en Educación Secundaria');
        cy.dataCy('save-profile').click();
        cy.dataCy('no-cv').should('be.visible');
        cy.dataCy('cv-input').selectFile('cypress/fixtures/cv-ficticio.pdf');
        cy.dataCy('upload-cv').click();
        cy.dataCy('profile-complete').should('be.visible');

        cy.dataCy('return-to-vacancy').click();
        cy.location('pathname').should('eq', `/empleos/${vacancy.id}`);
        // Volver no postula: la decisión sigue siendo de la persona.
        cy.dataCy('apply-button').should('be.visible');
        cy.dataCy('view-my-application').should('not.exist');

        cy.dataCy('apply-button').click();
        cy.idFromPath(/^\/mis-postulaciones\/(\d+)$/);
        cy.dataCy('tracking-notifications').should(
            'have.attr',
            'href',
            '/notificaciones',
        );
        cy.dataCy('convocations-empty').should('contain', 'No es un error');

        // Tras postular, el perfil ya no ofrece volver.
        cy.visit('/mi-perfil');
        cy.dataCy('profile-return').should('not.exist');
    });

    it('el registro desde una convocatoria anuncia los requisitos y vuelve a ella', function () {
        const vacancy = this.demo.vacancies.published;

        cy.visit(`/empleos/${vacancy.id}`);
        cy.dataCy('apply-register').click();

        cy.location('search').should('eq', `?convocatoria=${vacancy.id}`);
        cy.dataCy('return-notice').should('contain', vacancy.title);
        cy.dataCy('application-requirements')
            .should('contain', 'teléfono')
            .and('contain', 'PDF de hasta 5 MB');

        cy.dataCy('register-name').type('Postulante Retorno (ficticia)');
        cy.dataCy('register-email').type('retorno.e2e@correo.test');
        cy.dataCy('register-password').type('Contrasena-Ficticia-27');
        cy.dataCy('register-password-confirmation').type(
            'Contrasena-Ficticia-27',
        );
        cy.dataCy('register-submit').click();

        cy.location('pathname').should('eq', `/empleos/${vacancy.id}`);
        cy.dataCy('complete-profile')
            .should('have.attr', 'href')
            .and('include', `convocatoria=${vacancy.id}`);
    });

    [
        '//sitio-externo.test',
        'https://sitio-externo.test/empleos/2',
        '/empleos/2',
        '2abc',
    ].forEach((destino) => {
        it(`ignora el destino no permitido «${destino}»`, function () {
            cy.visit(`/login?convocatoria=${encodeURIComponent(destino)}`);
            cy.dataCy('return-notice').should('not.exist');
            entrarConFormulario(this.users.candidateNew);
            cy.location('href').should(
                'eq',
                `${Cypress.config('baseUrl')}/dashboard`,
            );
        });
    });

    it('una convocatoria cerrada no se ofrece como destino', function () {
        cy.visit(`/login?convocatoria=${this.demo.vacancies.closed.id}`);
        cy.dataCy('return-notice').should('not.exist');
        entrarConFormulario(this.users.candidateNew);
        cy.location('pathname').should('eq', '/dashboard');
    });

    it('otros roles conservan su navegación', function () {
        cy.visit(`/login?convocatoria=${this.demo.vacancies.published.id}`);
        cy.dataCy('return-notice').should('be.visible');
        entrarConFormulario(this.users.hr);
        cy.location('pathname').should('eq', '/dashboard');
    });

    it('la portada cuenta solo las convocatorias que aceptan postulaciones y anuncia los requisitos', () => {
        cy.visit('/');
        cy.dataCy('open-vacancies-count')
            .invoke('text')
            .should(
                'match',
                /^Hoy (hay \d+ convocatorias? recibiendo postulaciones|no hay convocatorias recibiendo postulaciones)\.$/,
            );
        cy.dataCy('cta-jobs').should('contain', 'Ver convocatorias');
        cy.dataCy('landing-requirements').should(
            'contain',
            'PDF de hasta 5 MB',
        );
        // El contenido institucional sigue, después de cómo postular.
        cy.dataCy('landing-apply').then(($apply) => {
            cy.dataCy('landing-roles').then(($roles) => {
                expect(
                    $apply[0].compareDocumentPosition($roles[0]) &
                        Node.DOCUMENT_POSITION_FOLLOWING,
                ).to.be.greaterThan(0);
            });
        });
        cy.dataCy('landing-ml-note').should('contain', 'experimental');
    });

    [320, 390].forEach((ancho) => {
        it(`a ${ancho} px la cabecera pública se lee completa, no desborda y se recorre con el teclado`, () => {
            cy.viewport(ancho, 800);
            cy.visit('/empleos');

            cy.dataCy('nav-public-jobs').should(
                'have.attr',
                'aria-current',
                'page',
            );
            cy.dataCy('nav-login')
                .should('be.visible')
                .and('have.text', 'Iniciar sesión');
            cy.dataCy('nav-register').should('be.visible');
            cy.document().then((doc) => {
                expect(
                    doc.documentElement.scrollWidth,
                    'sin desborde horizontal',
                ).to.be.at.most(ancho);
            });
            ['nav-public-jobs', 'nav-login', 'nav-register'].forEach((item) => {
                cy.dataCy(item).then(($el) => {
                    expect(
                        $el[0].getBoundingClientRect().height,
                        `${item} táctil`,
                    ).to.be.at.least(44);
                });
            });

            cy.dataCy('nav-home').focus();
            ['nav-public-jobs', 'nav-login', 'nav-register'].forEach((item) => {
                cy.press(Cypress.Keyboard.Keys.TAB);
                cy.focused()
                    .should('have.attr', 'data-cy', item)
                    .then(($a) => {
                        const estilo = getComputedStyle($a[0]);
                        expect(
                            estilo.outlineStyle !== 'none' ||
                                estilo.boxShadow !== 'none',
                            'foco visible',
                        ).to.eq(true);
                    });
            });
        });
    });
});
