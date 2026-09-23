/**
 * Diagnóstico de desbordamiento horizontal. NO forma parte de la suite E2E.
 *
 * Recorre cada página en cuatro anchos y reporta el ancho de desplazamiento
 * frente al ancho visible, más el elemento más ancho encontrado. Un desborde
 * en móvil obliga a arrastrar la página en horizontal, que es el peor defecto
 * responsive que puede tener una tabla.
 */
const WIDTHS = [1440, 1280, 768, 390];

const PUBLIC_PAGES = ['/', '/empleos', '/empleos/2', '/login', '/register'];

const HR_PAGES = [
    '/dashboard',
    '/requerimientos',
    '/requerimientos/4',
    '/vacantes',
    '/vacantes/1',
    '/vacantes/2',
    '/vacantes/1/editar',
    '/vacantes/3/postulaciones',
    '/postulaciones/4',
    '/vacantes/3/comparacion',
    '/notificaciones',
    '/settings/profile',
    '/settings/security',
];

const APPROVER_PAGES = ['/auditoria', '/vacantes/3/comparacion'];
const EVALUATOR_PAGES = ['/mis-evaluaciones'];
const CANDIDATE_PAGES = [
    '/mi-perfil',
    '/mis-postulaciones',
    '/mis-postulaciones/1',
];

function audit(path) {
    WIDTHS.forEach((width) => {
        cy.viewport(width, 800);
        cy.visit(path);
        cy.document().then((doc) => {
            const root = doc.documentElement;
            const overflow = root.scrollWidth - root.clientWidth;
            let detail = '';

            if (overflow > 1) {
                const widest = [...doc.querySelectorAll('body *')]
                    .map((el) => ({
                        el,
                        right: el.getBoundingClientRect().right,
                    }))
                    .filter((item) => item.right > root.clientWidth + 1)
                    .sort((a, b) => b.right - a.right)
                    .slice(0, 3)
                    .map(
                        (item) =>
                            `${item.el.tagName.toLowerCase()}.${String(item.el.className).slice(0, 90)} @${Math.round(item.right)}`,
                    );

                detail = ` | ${widest.join(' || ')}`;
                cy.log(`DESBORDE ${path} @${width}: +${overflow}px${detail}`);
            }

            expect(
                overflow,
                `desborde horizontal en ${path} a ${width}px${detail}`,
            ).to.be.lessThan(2);
        });
    });
}

describe('Fase 18 · desbordamiento horizontal', () => {
    before(() => cy.resetDatabase());

    it('páginas públicas', () => PUBLIC_PAGES.forEach(audit));

    it('RR. HH.', () => {
        cy.loginAs('hr');
        HR_PAGES.forEach(audit);
    });

    it('Dirección', () => {
        cy.loginAs('approver');
        APPROVER_PAGES.forEach(audit);
    });

    it('evaluador', () => {
        cy.loginAs('evaluator');
        EVALUATOR_PAGES.forEach(audit);
    });

    it('postulante', () => {
        cy.loginAs('candidateSubmitted');
        CANDIDATE_PAGES.forEach(audit);
    });
});
