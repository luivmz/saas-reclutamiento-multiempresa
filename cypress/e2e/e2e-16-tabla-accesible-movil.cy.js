/**
 * La tabla de expedientes sigue siendo una tabla en móvil.
 *
 * En pantallas angostas cada fila se apila como ficha, y apilarla exige
 * cambiar el `display` de `tbody`, `tr` y `td`. Ese cambio borra los roles
 * implícitos de la tabla, así que el componente los declara a mano y asocia
 * cada celda con su encabezado mediante `headers`. Lo que se comprueba aquí
 * es justamente eso —que la semántica sobrevive al apilado— y que el apilado
 * no duplicó filas ni perdió los `data-cy` de los que dependen las demás
 * pruebas.
 *
 * Es verificación de DOM y de estilos calculados, no una prueba con lector de
 * pantalla real.
 */
const MOVIL = [390, 844];
const ESCRITORIO = [1280, 800];

/** Comprueba la semántica de una tabla en el ancho actual. */
function verificarSemantica(tabla) {
    cy.dataCy(tabla).should('have.attr', 'role', 'table');

    // El encabezado se recorta, pero sigue existiendo para la tecnología
    // asistiva: con `display: none` desaparecería del árbol de accesibilidad
    // y `headers` no apuntaría a nada.
    cy.dataCy(tabla)
        .find('thead')
        .should('have.attr', 'role', 'rowgroup')
        .and('not.have.css', 'display', 'none');

    cy.dataCy(tabla)
        .find('thead th')
        .each((th) => {
            expect(th.attr('role')).to.eq('columnheader');
            expect(th.attr('scope')).to.eq('col');
            expect(th.attr('id') ?? '', 'el encabezado necesita id').to.match(
                /\S/,
            );
        });

    cy.dataCy(tabla).then(($tabla) => {
        const ids = [...$tabla[0].querySelectorAll('thead th')].map(
            (th) => th.id,
        );
        const celdas = [...$tabla[0].querySelectorAll('tbody td')];

        expect(celdas.length, 'la tabla tiene celdas').to.be.greaterThan(0);

        celdas.forEach((celda) => {
            expect(celda.getAttribute('role')).to.eq('cell');
            expect(
                ids,
                `headers de la celda «${celda.textContent.trim().slice(0, 30)}»`,
            ).to.include(celda.getAttribute('headers'));
        });
    });
}

/** Ninguna página debe poder arrastrarse en horizontal. */
function sinDesborde() {
    cy.document().then((doc) => {
        const raiz = doc.documentElement;

        expect(
            raiz.scrollWidth - raiz.clientWidth,
            'desborde horizontal',
        ).to.be.lessThan(2);
    });
}

/**
 * Fase 25: la página puede no desbordar y la ficha, aun así, quedar recortada,
 * porque el contenedor de la tabla hace scroll horizontal y absorbe el exceso.
 * En móvil cada ficha tiene que caber entera en el viewport.
 */
function fichasDentroDelViewport(fila) {
    cy.document().then((doc) => {
        const ancho = doc.documentElement.clientWidth;

        cy.dataCy(fila).each(($fila) => {
            const borde = $fila[0].getBoundingClientRect().right;

            expect(
                borde,
                `borde derecho de la ficha «${$fila.text().trim().slice(0, 30)}»`,
            ).to.be.at.most(ancho + 1);
        });
    });
}

/**
 * Recorre una tabla en móvil y en escritorio: la semántica debe ser la misma
 * y el número de filas también, porque el apilado es CSS y no duplica DOM.
 */
function auditar({ rol, ruta, tabla, fila }) {
    cy.loginAs(rol);

    cy.viewport(...ESCRITORIO);
    cy.visit(ruta);
    cy.dataCy(fila).should('have.length.at.least', 1);
    verificarSemantica(tabla);

    cy.dataCy(fila).then(($filas) => {
        const enEscritorio = $filas.length;

        cy.viewport(...MOVIL);
        cy.visit(ruta);
        cy.dataCy(fila).should('have.length', enEscritorio);
        verificarSemantica(tabla);
        sinDesborde();
        fichasDentroDelViewport(fila);
    });
}

describe('E2E-16 · La tabla de expedientes conserva su semántica en móvil', () => {
    before(() => cy.resetDatabase());

    beforeEach(() => cy.fixture('demo').as('demo'));

    it('requerimientos', () =>
        auditar({
            rol: 'hr',
            ruta: '/requerimientos',
            tabla: 'job-requests-table',
            fila: 'job-request-row',
        }));

    it('vacantes', () =>
        auditar({
            rol: 'hr',
            ruta: '/vacantes',
            tabla: 'vacancies-table',
            fila: 'vacancy-row',
        }));

    it('postulaciones de una vacante', function () {
        auditar({
            rol: 'hr',
            ruta: `/vacantes/${this.demo.vacancies.ranking.id}/postulaciones`,
            tabla: 'applications-table',
            fila: 'application-row',
        });
    });

    it('ranking de la comparación', function () {
        auditar({
            rol: 'hr',
            ruta: `/vacantes/${this.demo.vacancies.ranking.id}/comparacion`,
            tabla: 'ranking-table',
            fila: 'ranking-row',
        });
    });

    it('auditoría', () =>
        auditar({
            rol: 'approver',
            ruta: '/auditoria',
            tabla: 'audit-table',
            fila: 'audit-row',
        }));

    it('evaluaciones asignadas', () =>
        auditar({
            rol: 'evaluator',
            ruta: '/mis-evaluaciones',
            tabla: 'assignments-table',
            fila: 'assignment-row',
        }));

    it('en móvil cada celda muestra su etiqueta como texto, no como adorno CSS', function () {
        cy.loginAs('hr');
        cy.viewport(...MOVIL);
        cy.visit('/vacantes');

        cy.dataCy('vacancy-row')
            .first()
            .within(() => {
                // La etiqueta es un nodo real y queda fuera del árbol de
                // accesibilidad: la relación `headers` ya entrega el
                // encabezado, y repetirlo lo haría sonar dos veces.
                cy.contains('span[aria-hidden="true"]', 'Código').should(
                    'be.visible',
                );
            });
    });
});
