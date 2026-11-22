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
 *
 * APP-M02: las consultas sucesivas de la ayuda se hacen en la misma página,
 * sin recargarla, también con un envío doble; y se comprueban la consulta en
 * curso, el fallo de red o del servidor y la recuperación.
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
        // APP-M02: cada consulta GET remontaba la página entera. Una marca en el nodo del select comprueba que las
        // consultas sucesivas, sin recargar, conservan el mismo control, la elección y el foco.
        cy.dataCy('aid-criterion').then(($select) => {
            $select[0].dataset.marca = 'app-m02';
        });

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
        // Enter sobre el botón enfocado. En Cypress envía el formulario dos veces seguidas (clic e implícito): dos
        // visitas solapadas, como un doble envío real, que es lo que reproducía el fallo.
        cy.focused().type('{enter}');

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
        cy.dataCy('aid-criterion').should('have.attr', 'data-marca', 'app-m02');
        cy.focused().should('have.attr', 'data-cy', 'aid-submit');

        // F37-UX-02: la fuente recuperada se abre en su tarjeta completa, con la versión vigente, su procedencia y
        // la versión anterior conservada, sin otra visita (la URL no cambia y la página sigue montada).
        cy.location('href').then((antes) => {
            cy.dataCy('aid-results')
                .find('[data-cy="aid-open-source"]')
                .first()
                .click();
            cy.location('href').should('eq', antes);
        });
        cy.focused()
            .should('have.attr', 'data-cy', 'evidence-record')
            .and('have.attr', 'data-destacada', 'true')
            .and('contain', 'evaluación formativa')
            .and('contain', 'Fuente: Documento presentado')
            .within(() => {
                cy.contains('summary', 'Versiones anteriores (1)').click();
                cy.dataCy('evidence-version-provenance').should(
                    'contain',
                    'Fuente: Documento presentado',
                );
            });
        cy.dataCy('aid-criterion').should('have.attr', 'data-marca', 'app-m02');

        // Segunda consulta en la misma página, sin recargar, reenviada con doble clic.
        cy.dataCy('aid-criterion').select('Entrevista personal');
        cy.dataCy('aid-submit').dblclick();
        cy.dataCy('aid-results').should('contain', 'Entrevista personal');
        cy.dataCy('aid-abstained')
            .should('be.visible')
            .and('contain', 'no significa que el criterio no se cumpla');
        cy.dataCy('aid-criterion')
            .should('have.attr', 'data-marca', 'app-m02')
            .find('option:selected')
            .should('have.text', 'Entrevista personal');

        cy.dataCy('search-input').type('TALLER');
        cy.dataCy('search-submit').click();
        cy.dataCy('search-results')
            .find('[data-cy="aid-fragment"]')
            .should('have.length', 1);
        cy.dataCy('aid-criterion').should('have.attr', 'data-marca', 'app-m02');
    });

    it('la ayuda documental indica la consulta en curso, informa un fallo de red y se recupera sin recargar', () => {
        cy.loginAs('hr');
        cy.visit(EVIDENCIAS);
        cy.dataCy('aid-criterion').then(($select) => {
            $select[0].dataset.marca = 'app-m02';
        });

        // Procesamiento: con la respuesta retrasada, la sección y el botón indican la consulta en curso.
        cy.intercept(
            { method: 'GET', pathname: EVIDENCIAS, query: { criterio: '4' } },
            (req) => {
                req.on('response', (res) => {
                    res.setDelay(800);
                });
            },
        ).as('consultaLenta');
        cy.dataCy('aid-criterion').select('Conocimientos pedagógicos');
        cy.dataCy('aid-submit').click();
        cy.dataCy('documentary-aid').should('have.attr', 'aria-busy', 'true');
        cy.dataCy('aid-submit').find('[role="status"]').should('exist');
        cy.wait('@consultaLenta');
        cy.dataCy('aid-results').should('contain', 'Conocimientos pedagógicos');
        cy.dataCy('documentary-aid').should('not.have.attr', 'aria-busy');
        cy.dataCy('aid-submit').find('[role="status"]').should('not.exist');

        // Error de red: aviso propio, sin excepción ni diálogo, y el control sigue usable con la misma elección. El
        // fallo es persistente porque Chromium reintenta por su cuenta un GET cuyo socket se corta.
        cy.intercept(
            { method: 'GET', pathname: EVIDENCIAS, query: { criterio: '6' } },
            { forceNetworkError: true },
        ).as('caidaDeRed');
        cy.dataCy('aid-criterion').select('Entrevista personal');
        cy.dataCy('aid-submit').click();
        cy.wait('@caidaDeRed');
        cy.dataCy('aid-error')
            .should('be.visible')
            .and('contain', 'No se pudo consultar la ayuda documental');
        cy.dataCy('documentary-aid').should('not.have.attr', 'aria-busy');
        cy.dataCy('aid-submit').should('not.be.disabled');
        cy.dataCy('aid-criterion')
            .should('have.attr', 'data-marca', 'app-m02')
            .find('option:selected')
            .should('have.text', 'Entrevista personal');

        // Error del servidor (HTTP 500): el mismo aviso, sin el diálogo de error de Inertia.
        cy.intercept(
            { method: 'GET', pathname: EVIDENCIAS, query: { criterio: '6' } },
            { statusCode: 500, body: 'Error ficticio de prueba' },
        ).as('errorDelServidor');
        cy.dataCy('aid-submit').click();
        cy.wait('@errorDelServidor');
        cy.dataCy('aid-error').should('be.visible');
        cy.get('#inertia-error-dialog').should('not.exist');
        cy.dataCy('documentary-aid').should('not.have.attr', 'aria-busy');

        // Recuperación: con la red y el servidor de vuelta, el mismo envío funciona y retira el aviso. La última
        // interceptación definida se aplica primero y deja pasar la petición al servidor real.
        cy.intercept(
            { method: 'GET', pathname: EVIDENCIAS, query: { criterio: '6' } },
            (req) => req.continue(),
        ).as('recuperada');
        cy.dataCy('aid-submit').click();
        cy.wait('@recuperada').its('response.statusCode').should('eq', 200);
        cy.dataCy('aid-abstained').should('be.visible');
        cy.dataCy('aid-error').should('not.exist');
        cy.dataCy('aid-criterion').should('have.attr', 'data-marca', 'app-m02');
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

    it('un proceso cerrado congela sus evidencias: solo lectura y escritura directa rechazada', () => {
        // «Coordinador(a) de Tutoría» ya está cerrada en los datos demo; su postulación 7 fue seleccionada.
        cy.loginAs('hr');
        cy.visit('/postulaciones/7/evidencias');
        cy.dataCy('evidence-frozen').should('be.visible');
        cy.dataCy('evidence-create').should('not.exist');
        cy.dataCy('documentary-aid').should('be.visible');

        cy.appRequest('POST', '/postulaciones/7/evidencias', {
            type: 'certificado',
            source: 'documento_presentado',
            description: '[SINTÉTICO] Intento directo tras el cierre.',
        }).then((response) => {
            expect(response.status).to.eq(422);
            expect(response.body.errors.workflow[0]).to.contain('congelada');
        });

        // Dirección no escribe ni con el proceso abierto: sigue recibiendo 403, sin el mensaje del cierre.
        cy.loginAs('approver');
        cy.appRequest('POST', '/postulaciones/7/evidencias', {
            type: 'certificado',
            source: 'documento_presentado',
            description: '[SINTÉTICO] Intento de Dirección.',
        })
            .its('status')
            .should('eq', 403);
        cy.loginAs('hrOrgB');
        cy.appRequest('GET', '/postulaciones/7/evidencias')
            .its('status')
            .should('eq', 404);
    });

    it('si el proceso se cierra con la página abierta, el envío muestra el motivo y no registra nada (F37-UX-01)', () => {
        // «Auxiliar de Educación Inicial»: Dirección decide (RF-23, decisión humana de la prueba) y RR. HH. registra la
        // selección; RR. HH. abre las evidencias de una finalista y, sin recargar, cierra el proceso por otra vía.
        cy.loginAs('approver');
        cy.appRequest('POST', '/vacantes/3/decision', {
            application_id: 4,
            justification:
                'Decisión humana ficticia registrada por la prueba E2E-21.',
            human_confirmation: true,
        })
            .its('status')
            .should('eq', 302);
        cy.loginAs('hr');
        cy.appRequest('POST', '/vacantes/3/seleccion')
            .its('status')
            .should('eq', 302);

        cy.visit('/postulaciones/5/evidencias');
        cy.dataCy('evidence-create').should('be.visible');
        cy.dataCy('evidence-type').select('certificado');
        cy.dataCy('evidence-description-input')
            .clear()
            .type('[SINTÉTICO] Constancia ficticia enviada tras el cierre.');

        cy.appRequest('POST', '/vacantes/3/cerrar', {
            closure_notes: 'Cierre ficticio de la prueba E2E-21.',
        })
            .its('status')
            .should('eq', 302);

        cy.dataCy('evidence-submit').click();
        cy.dataCy('workflow-error')
            .should('be.visible')
            .and('contain', 'La convocatoria está cerrada');
        cy.dataCy('evidence-frozen').should('be.visible');
        cy.dataCy('evidence-create').should('not.exist');
        cy.dataCy('evidence-record').should('not.exist');
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

        // En una columna la ayuda queda al final: el atajo de la cabecera la trae a la vista con el foco.
        cy.scrollTo('top');
        cy.dataCy('jump-to-aid').should('be.visible').click();
        cy.focused().should('have.attr', 'data-cy', 'documentary-aid');
        cy.dataCy('aid-criterion').should('be.visible');

        cy.viewport(1280, 800);
        cy.visit(`${EVIDENCIAS}?criterio=4`);
        cy.dataCy('jump-to-aid').should('not.be.visible');
        cy.screenshot('e2e-21-escritorio', { capture: 'fullPage' });
    });
});
