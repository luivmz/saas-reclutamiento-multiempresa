/**
 * E2E-20 · El recorrido del guion de exposición, sobre los datos demo.
 *
 * Recorre, en el orden en que se presenta, lo que `docs/entrega-final/guion-demo.md`
 * enseña en vivo: la portada, la vacante con su panel de riesgo operacional
 * (ML-01, experimental), el ranking con su cálculo, la decisión humana de
 * Dirección (RF-23) y su huella en la auditoría. Si este spec pasa, el guion se
 * puede seguir paso a paso sin sorpresas.
 *
 * El entorno E2E corre sin el servicio ML, así que el panel muestra su modo sin
 * predicción. La predicción en vivo se demuestra con FastAPI levantado (guion,
 * paso 3) y la cubre `DemoSeederOperationalRiskScenarioTest`.
 */

/** Contraste WCAG del texto de un elemento contra el fondo opaco que tiene detrás (como en E2E-19). */
function contraste(el) {
    const win = el.ownerDocument.defaultView;
    const lienzo = el.ownerDocument.createElement('canvas');

    lienzo.width = lienzo.height = 1;

    const ctx = lienzo.getContext('2d', { willReadFrequently: true });
    const rgba = (css) => {
        ctx.clearRect(0, 0, 1, 1);
        ctx.fillStyle = css;
        ctx.fillRect(0, 0, 1, 1);

        const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;

        return [r, g, b, a / 255];
    };
    const sobre = (arriba, abajo) => [0, 1, 2].map((i) => arriba[i] * arriba[3] + abajo[i] * (1 - arriba[3])).concat(1);
    const luminancia = (c) => {
        const [r, g, b] = c.slice(0, 3).map((v) => {
            const s = v / 255;

            return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
        });

        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };

    const capas = [];

    for (let n = el; n; n = n.parentElement) {
        const c = rgba(win.getComputedStyle(n).backgroundColor);

        if (c[3] > 0) capas.push(c);
        if (c[3] >= 1) break;
    }

    const fondo = capas.reduceRight((abajo, arriba) => sobre(arriba, abajo), [255, 255, 255, 1]);
    const texto = sobre(rgba(win.getComputedStyle(el).color), fondo);
    const [l1, l2] = [luminancia(texto), luminancia(fondo)].sort((p, q) => q - p);

    return (l1 + 0.05) / (l2 + 0.05);
}

function sinAnimaciones() {
    cy.window().then(
        (win) =>
            new Cypress.Promise((resolve) => {
                const finitas = win.document.getAnimations().filter((a) => a.effect?.getTiming().iterations !== Infinity);

                Promise.all(finitas.map((a) => a.finished)).then(resolve, resolve);
            }),
    );
}

describe('E2E-20 · Recorrido del guion de demostración', () => {
    before(() => cy.resetDatabase());
    beforeEach(() => cy.fixture('demo').as('demo'));

    ['light', 'dark'].forEach((tema) => {
        it(`paso 1: la portada explica roles, límites y ML-01, legible en tema ${tema} (WCAG 1.4.3)`, () => {
            cy.visit('/', { onBeforeLoad: (win) => win.localStorage.setItem('appearance', tema) });
            sinAnimaciones();

            cy.dataCy('landing-roles').within(() => {
                cy.get('h2').should('contain', 'Quién interviene');
                cy.get('li').should('have.length', 5);
            });
            cy.dataCy('landing-limits').should('contain', 'No selecciona, descarta ni contrata');
            cy.dataCy('landing-ml-note').should('contain', 'nunca a las personas postulantes').and('contain', 'experimental');

            cy.get('[data-cy=landing-roles] p, [data-cy=landing-limits] p, [data-cy=landing-limits] li, [data-cy=landing-ml-note] p').each(($el) => {
                expect(contraste($el[0]), $el.text().slice(0, 40)).to.be.at.least(4.5);
            });
        });
    });

    it('paso 1: la portada no se desborda a 320 px y conserva un único h1', () => {
        cy.viewport(320, 640);
        cy.visit('/');
        cy.get('h1').should('have.length', 1);
        cy.document().then((doc) => {
            expect(doc.documentElement.scrollWidth - doc.documentElement.clientWidth).to.be.lessThan(2);
        });
    });

    it('paso 2: RR. HH. abre la vacante del escenario de riesgo y el panel no inventa una estimación', function () {
        const { id, title } = this.demo.vacancies.riskScenario;

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);
        cy.contains('h1', title).should('be.visible');
        cy.dataCy('operational-risk-panel').within(() => {
            cy.contains('Experimental').should('be.visible');
            cy.contains('no sobre las personas postulantes').should('be.visible');
        });
        cy.dataCy('operational-risk-score').should('not.exist');
    });

    it('paso 2b: con una estimación disponible, el panel muestra la cifra, el modelo y el umbral, sin hablar de personas', function () {
        const { id } = this.demo.vacancies.riskScenario;

        // Respuesta copiada de la verificación en vivo con FastAPI del 07/11/2026 (informe de entrega, §3).
        // Se simula en el navegador porque el entorno E2E no levanta el servicio Python (E2E-15).
        cy.intercept('GET', `/vacantes/${id}/riesgo-operacional`, {
            risk: {
                availability: 'predictive_available',
                reason: 'ok',
                risk_score: 0.13081671445096835,
                risk_percentage: 13.1,
                risk_flag: false,
                threshold: 0.1679418172266036,
                model_version: 'phase-15b-20260920-6000',
                freeze_fingerprint: '9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2',
                checked_at: '2026-11-07T17:29:12-05:00',
                is_experimental: true,
                measures: 'proceso',
                decision_is_human: true,
                message: 'Sin señal de riesgo en este momento. El proceso avanza dentro de lo esperado por el modelo.',
                label: 'Estimación disponible',
            },
        }).as('riesgo');

        cy.loginAs('hr');
        cy.visit(`/vacantes/${id}`);
        cy.wait('@riesgo');

        cy.dataCy('operational-risk-score').invoke('text').should('match', /13[.,]1\s*%/);
        cy.dataCy('operational-risk-flag').should('contain', 'Sin señal de riesgo');
        cy.dataCy('operational-risk-model')
            .should('contain', 'phase-15b-20260920-6000')
            .and('contain', 'freeze 9ee1843')
            .invoke('text')
            .should('match', /16[.,]8\s*%/);
        cy.dataCy('operational-risk-panel')
            .invoke('text')
            .then((text) => {
                // Misma lista que E2E-15, ahora también con una estimación en pantalla.
                ['ranking', 'mejor candidato', 'recomendamos', 'debe contratar', 'debe descartar', 'puntaje del postulante'].forEach((palabra) => {
                    expect(text.toLowerCase(), palabra).not.to.contain(palabra);
                });
            });
    });

    it('paso 3: el ranking muestra su cálculo y la decisión sigue pendiente', function () {
        cy.loginAs('hr');
        cy.visit(`/vacantes/${this.demo.vacancies.ranking.id}/comparacion`);
        cy.dataCy('ranking-row').should('have.length', 3);
        cy.dataCy('ranking-row').first().should('contain', this.demo.applications.rankingFirst.total);
        cy.dataCy('decision-panel').should('not.exist');
    });

    it('paso 4: Dirección decide con justificación y confirmación, y la auditoría lo registra', function () {
        const chosen = this.demo.applications.rankingSecond;

        cy.loginAs('approver');
        cy.visit(`/vacantes/${this.demo.vacancies.ranking.id}/comparacion`);
        cy.get(`[data-cy=decision-candidate-${chosen.id}]`).check();
        cy.dataCy('decision-justification').type('Mejor desempeño en la clase modelo; decisión de la demostración académica.');
        cy.dataCy('decision-human-confirmation').check();
        cy.dataCy('submit-final-decision').click();
        cy.dataCy('decision-summary').should('contain', chosen.candidate);

        cy.visit('/auditoria');
        cy.dataCy('audit-row').first().should('have.attr', 'data-action', 'seleccion.decision_registrada');
    });
});
