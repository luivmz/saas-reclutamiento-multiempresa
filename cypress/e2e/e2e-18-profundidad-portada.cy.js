/**
 * La profundidad de la portada es un adorno que puede no cargar (ADR-003).
 *
 * Lo que se comprueba aquí es lo que no se puede simular fuera de un
 * navegador: que la escena vive en un fragmento aparte y solo se descarga
 * cuando procede, que si ese fragmento falla la portada sigue entera, y que
 * con movimiento reducido, en móvil, con un equipo modesto o sin WebGL la
 * página funciona igual. En todos los casos la portada tiene que poder usarse
 * sin mirar la escena.
 *
 * Para saber si el fragmento se descargó se usa la API de Resource Timing, que
 * registra también lo servido desde caché: una interceptación de red no lo
 * vería.
 */
const ESCENA = 'recruitment-scene';

function reducido(activo) {
    return Cypress.automation('remote:debugger:protocol', {
        command: 'Emulation.setEmulatedMedia',
        params: {
            features: activo
                ? [{ name: 'prefers-reduced-motion', value: 'reduce' }]
                : [],
        },
    });
}

/** Si el navegador pidió el fragmento de la escena en este documento. */
function escenaDescargada(win) {
    return win.performance
        .getEntriesByType('resource')
        .some((recurso) => recurso.name.includes(ESCENA));
}

/** La portada se puede usar sin la escena: título y llamadas a la acción. */
function portadaUtilizable() {
    cy.get('h1').should('be.visible');
    cy.dataCy('cta-jobs').should('be.visible').and('have.attr', 'href');
    cy.dataCy('cta-login').should('be.visible');
}

function sinDesborde() {
    cy.document().then((doc) => {
        const raiz = doc.documentElement;

        expect(raiz.scrollWidth - raiz.clientWidth).to.be.lessThan(2);
    });
}

describe('E2E-18 · La profundidad de la portada es opcional y nunca estorba', () => {
    afterEach(() => reducido(false));

    // Va primero: el fragmento todavía no está en la caché del navegador, así
    // que la interceptación lo alcanza con seguridad.
    it('si el fragmento de la escena falla, queda el póster y la portada sigue entera', () => {
        cy.intercept('GET', `**/${ESCENA}-*.js`, {
            statusCode: 500,
            body: '',
        }).as('fragmento');

        cy.viewport(1280, 800);
        cy.visit('/');

        cy.wait('@fragmento');
        cy.dataCy('recruitment-poster').should('exist');
        cy.dataCy('recruitment-scene').should('not.exist');
        portadaUtilizable();
    });

    it('en escritorio la escena se monta desde su propio fragmento', () => {
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.dataCy('recruitment-depth').should(
            'have.attr',
            'data-mode',
            'scene',
        );
        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );
        cy.window().then((win) => {
            expect(escenaDescargada(win), 'fragmento diferido').to.eq(true);
        });
        portadaUtilizable();
    });

    it('no descarga la escena hasta que entra en el viewport', () => {
        // Ventana ancha pero muy baja: la tarjeta queda por debajo del borde.
        cy.viewport(1280, 130);
        cy.visit('/');

        cy.dataCy('recruitment-depth').should(
            'have.attr',
            'data-mode',
            'scene',
        );
        cy.dataCy('recruitment-poster').should('exist');
        cy.window().then((win) => {
            expect(escenaDescargada(win), 'antes de verse').to.eq(false);
        });

        cy.dataCy('recruitment-depth').scrollIntoView();
        cy.dataCy('recruitment-scene').should('exist');
        cy.window().then((win) => {
            expect(escenaDescargada(win), 'al verse').to.eq(true);
        });
    });

    it('con movimiento reducido: póster, sin descargar la escena', () => {
        reducido(true);
        cy.viewport(1280, 800);
        cy.visit('/');

        cy.dataCy('recruitment-depth')
            .should('have.attr', 'data-mode', 'poster')
            .and('have.attr', 'data-reason', 'reduced-motion');
        cy.dataCy('recruitment-scene').should('not.exist');
        cy.window().then((win) => {
            expect(escenaDescargada(win)).to.eq(false);
        });
        portadaUtilizable();
    });

    it('en móvil: póster, sin descargar la escena y sin desbordar', () => {
        cy.viewport(390, 844);
        cy.visit('/');

        cy.dataCy('recruitment-depth')
            .should('have.attr', 'data-mode', 'poster')
            .and('have.attr', 'data-reason', 'small-viewport');
        cy.window().then((win) => {
            expect(escenaDescargada(win)).to.eq(false);
        });
        portadaUtilizable();
        sinDesborde();
    });

    it('en un equipo modesto: póster', () => {
        cy.viewport(1280, 800);
        cy.visit('/', {
            onBeforeLoad(win) {
                Object.defineProperty(win.navigator, 'hardwareConcurrency', {
                    value: 2,
                });
            },
        });

        cy.dataCy('recruitment-depth')
            .should('have.attr', 'data-mode', 'poster')
            .and('have.attr', 'data-reason', 'low-end');
        portadaUtilizable();
    });

    it('sin WebGL la escena se muestra igual: no depende de él', () => {
        cy.viewport(1280, 800);
        cy.visit('/', {
            onBeforeLoad(win) {
                delete win.WebGLRenderingContext;
                delete win.WebGL2RenderingContext;
                const original = win.HTMLCanvasElement.prototype.getContext;
                win.HTMLCanvasElement.prototype.getContext = function (
                    tipo,
                    ...resto
                ) {
                    return String(tipo).startsWith('webgl')
                        ? null
                        : original.call(this, tipo, ...resto);
                };
            },
        });

        cy.dataCy('recruitment-scene').should(
            'have.attr',
            'data-ready',
            'true',
        );
        cy.get('canvas').should('not.exist');
        portadaUtilizable();
    });

    it('es decorativa: oculta, inerte y fuera del orden de tabulación', () => {
        cy.viewport(1280, 800);
        cy.visit('/');

        // `have.attr` con un solo argumento cambia el sujeto al valor del
        // atributo, así que cada comprobación va en su propia cadena.
        cy.dataCy('recruitment-depth')
            .should('have.attr', 'aria-hidden', 'true')
            .and('have.css', 'pointer-events', 'none');
        cy.dataCy('recruitment-depth').should('have.attr', 'inert');
        cy.dataCy('recruitment-depth')
            .find('a, button, input, [tabindex]')
            .should('not.exist');

        // El texto del expediente queda por delante de la escena, sobre su
        // propio fondo sólido: se lee igual con escena o sin ella.
        cy.contains('REQ-2026-0042')
            .closest('.z-10')
            .should('have.css', 'z-index', '10');
    });
});
