/**
 * E2E-21 · Evidencias ficticias y ayuda documental ML-02 (EXPERIMENTAL).
 *
 * Solo en la rama local `exp/evidencias-ml02`, con EXPERIMENTAL_EVIDENCIAS=true
 * en `.env.e2e`. No es la integración formal en el SaaS (EI-23 sigue BLOCKED).
 *
 * Recorre el flujo sobre los datos demo, en la postulación POS-00003 de
 * «Docente de Comunicación - Secundaria», cuya evaluación está asignada a
 * evaluador@andino.test: llegada desde el expediente, estado vacío, error de
 * validación, registro, enlace, revisión, corrección con versión nueva, la
 * ayuda documental con fuentes y su abstención, el evaluador asignado,
 * Dirección en solo lectura, otra organización, teclado y móvil.
 */
const POSTULACION = 3;
const EVIDENCIAS = `/postulaciones/${POSTULACION}/evidencias`;
const MOVIL = [390, 844];

describe('E2E-21 · Evidencias y ayuda documental ML-02 (experimental)', () => {
    before(() => {
        cy.resetDatabase();
    });

    it('RR. HH. llega desde el expediente y ve el aviso experimental y el estado vacío', () => {
        cy.loginAs('hr');
        cy.visit(`/postulaciones/${POSTULACION}`);
        cy.dataCy('open-evidence').click();

        cy.location('pathname').should('eq', EVIDENCIAS);
        cy.contains('h1', 'Evidencias de la postulación');
        cy.contains('Docente de Comunicación - Secundaria');
        cy.dataCy('experimental-notice').should('be.visible');
        cy.dataCy('evidence-list').within(() => {
            cy.dataCy('empty-state').should('be.visible');
        });
    });

    it('rechaza un texto sin el marcador [SINTÉTICO] y no registra nada', () => {
        cy.loginAs('hr');
        cy.visit(EVIDENCIAS);

        cy.dataCy('evidence-type').select('certificado');
        cy.dataCy('evidence-source').should(
            'have.text',
            'Documento presentado',
        );
        cy.dataCy('evidence-description-input')
            .clear()
            .type('Texto sin marcador');
        cy.dataCy('evidence-submit').click();

        cy.contains('El texto debe empezar por [SINTÉTICO]').should(
            'be.visible',
        );
        cy.dataCy('evidence-description-input').should(
            'have.attr',
            'aria-invalid',
            'true',
        );
        cy.dataCy('evidence-record').should('not.exist');
    });

    it('registra, enlaza, revisa y corrige con una versión nueva sin borrar la anterior', () => {
        cy.loginAs('hr');
        cy.visit(EVIDENCIAS);

        cy.dataCy('evidence-type').select('certificado');
        cy.dataCy('evidence-description-input')
            .clear()
            .type(
                '[SINTÉTICO] Constancia ficticia de un taller de conocimientos pedagógicos.',
            );
        cy.dataCy('evidence-submit').click();

        cy.dataCy('evidence-record').should('have.length', 1);
        cy.dataCy('evidence-state').should('contain', 'Registrada');

        cy.dataCy('evidence-link-criterion').select(
            'Conocimientos pedagógicos',
        );
        cy.dataCy('evidence-link').click();
        cy.dataCy('evidence-links').should(
            'contain',
            'Conocimientos pedagógicos',
        );

        cy.dataCy('evidence-review').click();
        cy.dataCy('evidence-state').should('contain', 'Revisada');

        cy.contains('summary', 'Corregir con una versión nueva').click();
        cy.dataCy('evidence-correct-description')
            .clear()
            .type(
                '[SINTÉTICO] Constancia ficticia de un taller de conocimientos pedagógicos y de evaluación formativa.',
            );
        cy.dataCy('evidence-correct').click();

        cy.dataCy('evidence-record')
            .should('have.length', 1)
            .and('contain', 'versión 2');
        cy.dataCy('evidence-state').should('contain', 'Registrada');
        cy.dataCy('evidence-links').should(
            'contain',
            'Conocimientos pedagógicos',
        );
        cy.dataCy('evidence-versions').should(
            'contain',
            'Versiones anteriores (1)',
        );
    });

    it('la ayuda documental muestra fragmentos con su fuente, se usa con teclado y se abstiene sin palabras compartidas', () => {
        cy.loginAs('hr');
        cy.visit(EVIDENCIAS);

        cy.dataCy('aid-criterion').focus().select('Conocimientos pedagógicos');
        cy.press(Cypress.Keyboard.Keys.TAB);
        cy.focused()
            .should('have.attr', 'data-cy', 'aid-submit')
            .then(($button) => {
                const estilo = getComputedStyle($button[0]);

                expect(
                    estilo.outlineStyle !== 'none' ||
                        estilo.boxShadow !== 'none',
                    'el botón enfocado muestra el foco',
                ).to.equal(true);
            });
        cy.focused().click();

        cy.location('search').should('contain', 'criterio=');
        cy.dataCy('aid-results').within(() => {
            cy.dataCy('aid-fragment').should('have.length', 1);
            cy.get('mark').should('have.length.at.least', 1);
            cy.contains('Fuente declarada: Documento presentado');
            cy.contains('versión 2');
        });
        cy.dataCy('documentary-aid').should(
            'contain',
            'No usa modelos entrenados',
        );

        cy.visit(EVIDENCIAS);
        cy.dataCy('aid-criterion').select('Entrevista personal');
        cy.dataCy('aid-submit').click();
        cy.dataCy('aid-abstained')
            .should('be.visible')
            .and('contain', 'no significa que el criterio no se cumpla');

        cy.dataCy('search-input').type('TALLER');
        cy.dataCy('search-submit').click();
        cy.dataCy('search-results')
            .find('[data-cy="aid-fragment"]')
            .should('have.length', 1);
    });

    it('el evaluador asignado registra su observación desde su sesión y no ve el historial', () => {
        cy.loginAs('evaluator');
        cy.visit('/mis-evaluaciones');
        cy.dataCy('open-assignment').first().click();
        cy.dataCy('open-evidence').click();
        cy.location('pathname').should('eq', EVIDENCIAS);

        cy.dataCy('evidence-type')
            .find('option')
            .should('have.length', 1)
            .and('have.value', 'observacion');
        cy.dataCy('evidence-source').should('have.text', 'Sesión asignada');
        cy.dataCy('evidence-description-input')
            .clear()
            .type(
                '[SINTÉTICO] Inició la clase modelo presentando los objetivos.',
            );
        cy.dataCy('evidence-submit').click();
        cy.dataCy('evidence-record').should('have.length', 2);

        cy.dataCy('evidence-history-link').should('not.exist');
        cy.appRequest('GET', `${EVIDENCIAS}/historial`)
            .its('status')
            .should('eq', 403);
    });

    it('Dirección solo consulta y ve el historial; otra organización recibe 404', () => {
        cy.loginAs('approver');
        cy.visit(EVIDENCIAS);
        cy.dataCy('evidence-create').should('not.exist');
        cy.dataCy('evidence-review').should('not.exist');
        cy.dataCy('evidence-history-link').click();
        cy.dataCy('evidence-history-entry').should('have.length.at.least', 5);
        cy.dataCy('evidence-history').should(
            'not.contain',
            'Constancia ficticia',
        );

        cy.loginAs('hrOrgB');
        cy.appRequest('GET', EVIDENCIAS).its('status').should('eq', 404);
    });

    it('en móvil no hay desplazamiento horizontal y las acciones siguen visibles', () => {
        cy.viewport(...MOVIL);
        cy.loginAs('hr');
        cy.visit(`${EVIDENCIAS}?criterio=4`);

        cy.dataCy('evidence-record').first().should('be.visible');
        cy.dataCy('aid-results').should('be.visible');
        cy.document().then((doc) => {
            expect(
                doc.documentElement.scrollWidth,
                'ancho del documento',
            ).to.be.at.most(MOVIL[0]);
        });
        cy.screenshot('e2e-21-movil', { capture: 'fullPage' });

        cy.viewport(1280, 800);
        cy.visit(`${EVIDENCIAS}?criterio=4`);
        cy.screenshot('e2e-21-escritorio', { capture: 'fullPage' });
    });
});
