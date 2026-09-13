// Full process in one ordered scenario: each `it` is a role handoff and passes identifiers to the next one.
// A single reset in `before` is deliberate: the steps are inherently sequential, and splitting them into
// independent specs would duplicate the whole setup. A failure stops at the exact step that broke.
const TITLE = 'Docente de Ciencias - Flujo integral E2E';
const CANDIDATE = 'Gabriela Nueva (ficticia)';
const state = {};

const inDays = (days) => new Date(Date.now() + days * 86400000).toISOString().slice(0, 10);

const recordPendingSession = (kind, score) => {
    cy.visit('/mis-evaluaciones');
    cy.get(`[data-cy=assignment-row][data-kind=${kind}][data-status=programada]`)
        .filter(`:contains("${CANDIDATE}")`)
        .should('have.length', 1)
        .find('[data-cy=open-assignment]')
        .click();
    cy.dataCy('score-row').find('input[type=number]').each(($input) => cy.wrap($input).type(score));

    if (kind === 'entrevista') {
        cy.dataCy('interview-outcome').select(1);
    }

    cy.dataCy('session-observations').type('Desempeño registrado en el flujo integral (dato ficticio).');
    cy.dataCy('record-results').click();
    cy.dataCy('recorded-results').should('be.visible');
};

describe('Flujo integral · de requerimiento a auditoría', () => {
    before(() => cy.resetDatabase());

    it('01 el área solicitante registra y envía el requerimiento', () => {
        cy.loginAs('requester');
        cy.visit('/requerimientos/crear');
        cy.dataCy('position_title').type(TITLE);
        cy.dataCy('area').type('Coordinación Académica');
        cy.dataCy('contract_type').select(1);
        cy.dataCy('justification').type('Ampliación de secciones de ciencias para el siguiente periodo (dato ficticio).');
        cy.dataCy('save-job-request').click();
        cy.idFromPath(/^\/requerimientos\/(\d+)$/).then((id) => (state.request = id));
        cy.dataCy('submit-job-request').click();
        cy.dataCy('status-badge').first().should('contain', 'Enviado a RR. HH.');
    });

    it('02 RR. HH. valida el requerimiento', () => {
        cy.loginAs('hr');
        cy.visit(`/requerimientos/${state.request}`);
        cy.dataCy('validate-job-request').click();
        cy.dataCy('status-badge').first().should('contain', 'Validado por RR. HH.');
    });

    it('03 el aprobador aprueba el requerimiento', () => {
        cy.loginAs('approver');
        cy.visit(`/requerimientos/${state.request}`);
        cy.dataCy('decision-approve').check();
        cy.dataCy('submit-decision').click();
        cy.dataCy('status-badge').first().should('contain', 'Aprobado');
    });

    it('04 RR. HH. genera, valida y publica la vacante', () => {
        cy.loginAs('hr');
        cy.visit(`/requerimientos/${state.request}`);
        cy.dataCy('create-vacancy-from-request').click();
        cy.dataCy('vacancy-title').clear().type(TITLE);
        cy.dataCy('vacancy-summary').clear().type('Convocatoria ficticia del flujo integral E2E.');
        cy.dataCy('vacancy-contract-type').select(1);
        cy.dataCy('vacancy-opens-at').clear().type(inDays(0));
        cy.dataCy('vacancy-closes-at').clear().type(inDays(30));
        cy.dataCy('profile-education').clear().type('Título profesional en Educación, especialidad Ciencias');
        cy.dataCy('profile-experience').clear().type('Mínimo 2 años');
        cy.dataCy('profile-functions').clear().type('Planificar y desarrollar sesiones de ciencias.');
        cy.dataCy('profile-competencies').clear().type('Indagación científica y trabajo en equipo.');
        cy.dataCy('save-vacancy').click();
        cy.idFromPath(/^\/vacantes\/(\d+)$/).then((id) => (state.vacancy = id));
        cy.dataCy('publish-vacancy').click();
        cy.dataCy('status-badge').first().should('contain', 'Publicada');
    });

    it('05 el postulante completa su perfil, carga su CV y postula', () => {
        cy.loginAs('candidateNew');
        cy.visit('/mi-perfil');
        cy.dataCy('profile-phone').type('900000099');
        cy.dataCy('profile-city').type('Huancayo');
        cy.dataCy('profile-education-level').select(2);
        cy.dataCy('profile-years').type('3');
        cy.dataCy('profile-title').type('Licenciada en Educación - Ciencias');
        cy.dataCy('save-profile').click();
        cy.dataCy('cv-input').selectFile('cypress/fixtures/cv-ficticio.pdf');
        cy.dataCy('upload-cv').click();
        cy.dataCy('profile-complete').should('be.visible');

        cy.visit(`/empleos/${state.vacancy}`);
        cy.dataCy('apply-button').click();
        cy.idFromPath(/^\/mis-postulaciones\/(\d+)$/).then((id) => (state.application = id));
    });

    it('06 RR. HH. preselecciona y programa evaluación y entrevista', () => {
        cy.loginAs('hr');
        cy.visit(`/postulaciones/${state.application}`);
        cy.dataCy('shortlist-application').click();
        cy.dataCy('status-badge').first().should('contain', 'Preseleccionado');

        cy.dataCy('evaluacion-evaluator').select('Jorge Salazar (demo)');
        cy.dataCy('evaluacion-type').select('Clase modelo');
        cy.dataCy('evaluacion-scheduled-at').type(`${inDays(2)}T10:00`);
        cy.dataCy('evaluacion-modality').select(1);
        cy.dataCy('evaluacion-location').type('Aula 305 - Sede central (demo)');
        cy.dataCy('schedule-evaluacion').click();
        cy.get('[data-cy=assessment-item][data-kind=evaluacion]').should('have.length', 1);

        cy.dataCy('entrevista-evaluator').select('Jorge Salazar (demo)');
        cy.dataCy('entrevista-scheduled-at').type(`${inDays(3)}T09:30`);
        cy.dataCy('entrevista-modality').select(1);
        cy.dataCy('entrevista-location').type('Sala de reuniones (demo)');
        cy.dataCy('schedule-entrevista').click();
        cy.get('[data-cy=assessment-item][data-kind=entrevista]').should('have.length', 1);
        cy.dataCy('status-badge').first().should('contain', 'En entrevista');
    });

    it('07 el evaluador registra la evaluación y la entrevista', () => {
        cy.loginAs('evaluator');
        recordPendingSession('evaluacion', '19');
        recordPendingSession('entrevista', '18');
    });

    it('08 RR. HH. pasa la postulación a finalista y consulta el ranking', () => {
        cy.loginAs('hr');
        cy.visit(`/postulaciones/${state.application}`);
        cy.dataCy('stage-select').select('Finalista');
        cy.dataCy('change-stage').click();
        cy.dataCy('status-badge').first().should('contain', 'Finalista');

        cy.visit(`/vacantes/${state.vacancy}/comparacion`);
        cy.dataCy('human-decision-notice').should('be.visible');
        cy.dataCy('ranking-row').should('have.length', 1).and('contain', CANDIDATE);
        cy.dataCy('decision-summary').should('not.exist');
    });

    it('09 el aprobador registra la decisión final humana', () => {
        cy.loginAs('approver');
        cy.visit(`/vacantes/${state.vacancy}/comparacion`);
        cy.get(`[data-cy=decision-candidate-${state.application}]`).check();
        cy.dataCy('decision-justification').type('Desempeño sobresaliente en clase modelo y entrevista (E2E).');
        cy.dataCy('decision-human-confirmation').check();
        cy.dataCy('submit-final-decision').click();
        cy.dataCy('decision-summary').should('contain', CANDIDATE);
    });

    it('10 RR. HH. registra la selección y cierra la convocatoria', () => {
        cy.loginAs('hr');
        cy.visit(`/vacantes/${state.vacancy}/comparacion`);
        cy.dataCy('register-selection').click();
        cy.dataCy('decision-summary').should('not.contain', 'Pendiente (RR. HH.)');
        cy.dataCy('close-vacancy').click();
        cy.dataCy('closure-summary').should('contain', 'Cerrada con selección');
    });

    it('11 el postulante ve el resultado y su notificación', () => {
        cy.waitForQueue();
        cy.loginAs('candidateNew');
        cy.visit(`/mis-postulaciones/${state.application}`);
        cy.dataCy('status-badge').first().should('contain', 'Seleccionado');
        cy.visit('/notificaciones');
        cy.dataCy('notification-item').first().should('contain', TITLE).and('contain', 'seleccionado(a)');
    });

    it('12 el aprobador consulta la auditoría del proceso', () => {
        cy.loginAs('approver');
        cy.visit('/auditoria');
        ['vacante.cerrada', 'seleccion.candidato_registrado', 'seleccion.decision_registrada', 'proceso.resultado_notificado'].forEach((action) => {
            cy.get(`[data-cy=audit-row][data-action="${action}"]`).should('have.length.at.least', 1);
        });
        cy.dataCy('audit-row').first().should('contain', 'Vacante');
    });
});
