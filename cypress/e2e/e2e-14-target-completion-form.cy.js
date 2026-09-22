import { appDate } from '../support/dates';

const inDays = (days) => appDate(days);

/**
 * GAP-01 en el navegador: capturar el plazo objetivo del proceso.
 *
 * La Fase 16 creó `vacancies.target_completion_at` y el campo del formulario,
 * pero hasta aquí nadie había comprobado que un navegador real puede
 * rellenarlo. Un `datetime-local` es precisamente el tipo de control que se
 * comporta distinto fuera de las pruebas de servidor.
 */
describe('E2E-14 · RR. HH. captura el plazo objetivo del proceso (GAP-01)', () => {
    beforeEach(() => {
        cy.resetDatabase();
        cy.fixture('demo').as('demo');
    });

    it('registra el plazo objetivo al configurar una vacante en borrador', function () {
        const { id } = this.demo.vacancies.draft;
        const closesAt = inDays(20);
        const target = `${inDays(50)}T18:00`;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}/editar`);

        cy.dataCy('vacancy-closes-at').clear().type(closesAt);
        cy.dataCy('vacancy-target-completion-at').should('be.enabled').clear().type(target);
        cy.dataCy('vacancy-target-completion-at').should('have.value', target);

        cy.dataCy('save-vacancy').click();

        cy.location('pathname').should('eq', `/vacantes/${id}`);
        // El detalle muestra el plazo ya persistido: el <dd> hermano del
        // <dt> con la etiqueta no puede ser el guion de "sin valor".
        cy.contains('dt', 'Plazo objetivo del proceso')
            .should('be.visible')
            .siblings('dd')
            .should('not.contain', '—')
            .and('not.be.empty');

        // Y al volver al formulario, el valor sigue ahí.
        cy.visit(`/vacantes/${id}/editar`);
        cy.dataCy('vacancy-target-completion-at').should('have.value', target);
    });

    it('el navegador impide enviar un plazo anterior al cierre', function () {
        /* El campo lleva `min` derivado de `closes_at`, así que un plazo
           anterior queda invalido antes de salir del navegador y el formulario
           no se envía. La regla equivalente del servidor -- `after:closes_at` y
           el CHECK de la tabla -- se cubre en `TargetCompletionTest`; aquí
           interesa que el usuario no llegue siquiera a enviarlo. */
        const { id } = this.demo.vacancies.draft;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}/editar`);

        cy.dataCy('vacancy-closes-at').clear().type(inDays(30));
        cy.dataCy('vacancy-target-completion-at').clear().type(`${inDays(10)}T12:00`);

        cy.dataCy('vacancy-target-completion-at').should(($input) => {
            expect($input[0].min, 'min derivado del cierre').to.not.equal('');
            expect($input[0].checkValidity(), 'el campo queda invalido').to.be.false;
        });

        cy.dataCy('save-vacancy').click();

        // Sigue en el formulario: no hubo envío.
        cy.location('pathname').should('eq', `/vacantes/${id}/editar`);

        // Y el plazo no se guardó.
        cy.visit(`/vacantes/${id}`);
        cy.contains('dt', 'Plazo objetivo del proceso').siblings('dd').should('contain', '—');
    });

    it('el plazo es opcional: la vacante se guarda y publica sin él', function () {
        const { id } = this.demo.vacancies.draft;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}/editar`);
        cy.dataCy('vacancy-target-completion-at').should('have.value', '');
        cy.dataCy('save-vacancy').click();

        cy.location('pathname').should('eq', `/vacantes/${id}`);
        cy.dataCy('validation-ok').should('be.visible');
    });

    it('deja de poder editarse una vez publicada la vacante', function () {
        const { id } = this.demo.vacancies.draft;
        const target = `${inDays(60)}T17:00`;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}/editar`);
        cy.dataCy('vacancy-closes-at').clear().type(inDays(20));
        cy.dataCy('vacancy-target-completion-at').clear().type(target);
        cy.dataCy('save-vacancy').click();

        cy.location('pathname').should('eq', `/vacantes/${id}`);
        cy.dataCy('publish-vacancy').click();
        cy.dataCy('status-badge').first().should('contain', 'Publicada');

        /* Publicada, la configuración se cierra: el enlace de edición
           desaparece y entrar a mano redirige. Es lo que impide que el plazo
           se corra durante el proceso, que es lo que haría inutilizable a
           ML-FEAT-02. */
        cy.dataCy('edit-vacancy').should('not.exist');
        cy.visit(`/vacantes/${id}/editar`);
        cy.location('pathname').should('eq', `/vacantes/${id}`);
    });
});
