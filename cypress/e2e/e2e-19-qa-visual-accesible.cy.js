/**
 * Lo que encontró la QA visual de la Fase 21, protegido en el navegador.
 *
 * Los defectos de contraste solo existían en el navegador: un token correcto
 * en el lugar equivocado no falla ni en TypeScript ni en una prueba de
 * componente. Aquí se mide el color que de verdad se pinta, y se comprueban la
 * reflow a 320 px, el `main` de las pantallas de acceso y el tamaño del enlace
 * de salto. Detalle en `docs/v1.1/phase-21-visual-qa.md`.
 */

/**
 * Contraste WCAG entre el color de un elemento y el fondo opaco que tiene
 * detrás. Los colores del sistema son oklch: un lienzo de 1×1 los convierte a
 * sRGB tal como los pinta el navegador.
 */
function contraste(el, colorTexto) {
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
    const sobre = (arriba, abajo) =>
        [0, 1, 2].map((i) => arriba[i] * arriba[3] + abajo[i] * (1 - arriba[3])).concat(1);
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
    const texto = sobre(rgba(colorTexto ?? win.getComputedStyle(el).color), fondo);
    const [l1, l2] = [luminancia(texto), luminancia(fondo)].sort((p, q) => q - p);

    return (l1 + 0.05) / (l2 + 0.05);
}

/** Espera a que terminen las entradas animadas antes de medir colores. */
function sinAnimaciones() {
    cy.window().then(
        (win) =>
            new Cypress.Promise((resolve) => {
                const finitas = win.document
                    .getAnimations()
                    .filter((a) => a.effect?.getTiming().iterations !== Infinity);

                Promise.all(finitas.map((a) => a.finished)).then(resolve, resolve);
            }),
    );
}

function visitar(ruta, tema = 'light') {
    cy.visit(ruta, {
        onBeforeLoad: (win) => win.localStorage.setItem('appearance', tema),
    });
}

describe('E2E-19 · QA visual y accesibilidad de la Fase 21', () => {
    before(() => cy.resetDatabase());

    it('las páginas públicas no se desbordan a 320 px (WCAG 1.4.10)', () => {
        cy.viewport(320, 640);

        ['/', '/empleos', '/login'].forEach((ruta) => {
            visitar(ruta);
            cy.get('main').should('be.visible');
            cy.document().then((doc) => {
                const { scrollWidth, clientWidth } = doc.documentElement;

                expect(scrollWidth - clientWidth, `desborde en ${ruta}`).to.be.lessThan(2);
            });
        });
    });

    it('cada pantalla de acceso tiene un único contenido principal', () => {
        ['/login', '/register', '/forgot-password'].forEach((ruta) => {
            visitar(ruta);
            cy.get('main').should('have.length', 1).find('form').should('exist');
        });
    });

    it('el enlace de salto enfocado mide al menos 24 px de alto (WCAG 2.5.8)', () => {
        visitar('/');
        cy.get('a[href="#contenido-principal"]')
            .focus()
            .should('be.visible')
            .invoke('outerHeight')
            .should('be.at.least', 24);
    });

    ['light', 'dark'].forEach((tema) => {
        it(`la alerta de rechazo se lee en ${tema} (WCAG 1.4.3)`, () => {
            cy.loginAs('requester');
            visitar('/requerimientos?estado=rechazado', tema);
            cy.dataCy('job-request-link').first().click();
            cy.dataCy('rejection-alert').should('be.visible');
            sinAnimaciones();

            cy.dataCy('rejection-alert').then(($alerta) => {
                ['alert-title', 'alert-description'].forEach((slot) => {
                    const el = $alerta[0].querySelector(`[data-slot=${slot}]`);

                    expect(contraste(el), `${slot} en ${tema}`).to.be.at.least(4.5);
                });
            });
        });

        it(`el error de un campo y el botón destructivo se leen en ${tema}`, () => {
            cy.loginAs('requester');
            visitar('/requerimientos/crear', tema);
            cy.dataCy('save-job-request').click();
            cy.get('p[role=alert]').should('have.length.at.least', 1);
            sinAnimaciones();

            cy.get('p[role=alert]').each(($error) => {
                expect(contraste($error[0]), `error en ${tema}`).to.be.at.least(4.5);
            });

            // El botón destructivo (`bg-destructive text-white`) no aparece en
            // esta pantalla: se mide el mismo par de colores con una muestra.
            cy.document().then((doc) => {
                const muestra = doc.createElement('button');

                muestra.className = 'bg-destructive text-white';
                doc.querySelector('main').appendChild(muestra);

                expect(contraste(muestra), `botón destructivo en ${tema}`).to.be.at.least(4.5);
                muestra.remove();
            });
        });
    });
});
