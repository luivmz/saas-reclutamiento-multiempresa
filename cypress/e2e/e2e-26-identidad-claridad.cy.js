/**
 * Fase 1 de identidad y claridad (DEF-24 a DEF-29), comprobada en el navegador.
 *
 * Lo que una prueba de servidor no ve: el color real de los iconos, el
 * contraste calculado del título del menú móvil en ambos temas, que quitar la
 * búsqueda vacíe de verdad el campo, que la vacante vencida conserve su estado
 * formal y que las páginas de error ofrezcan una salida según la sesión sin
 * cambiar los códigos HTTP ni las respuestas JSON.
 */

/** Contraste WCAG entre el color de un elemento y el primer fondo opaco detrás de él. */
function contraste(el) {
    const win = el.ownerDocument.defaultView;
    const ctx = el.ownerDocument.createElement('canvas').getContext('2d');
    const rgb = (color) => {
        ctx.clearRect(0, 0, 1, 1);
        ctx.fillStyle = color;
        ctx.fillRect(0, 0, 1, 1);

        return [...ctx.getImageData(0, 0, 1, 1).data].slice(0, 3);
    };
    const lum = (c) => {
        const [r, g, b] = c.map((x) => {
            const v = x / 255;

            return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
        });

        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    let fondo = el;
    let bg = win.getComputedStyle(fondo).backgroundColor;
    while (fondo && /rgba\(.*,\s*0\)$|transparent/.test(bg)) {
        fondo = fondo.parentElement;
        bg = win.getComputedStyle(fondo).backgroundColor;
    }
    const a = lum(rgb(win.getComputedStyle(el).color));
    const b = lum(rgb(bg));

    return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

describe('E2E-26 · Identidad y claridad de la interfaz', () => {
    before(() => cy.resetDatabase());

    it('los iconos del navegador muestran la marca de la plataforma y no la de Laravel', () => {
        cy.request('/favicon.svg').then(({ body }) => {
            expect(body).not.to.match(/#FF2D20/i);
            expect(body).to.contain('<title>SaaS Reclutamiento</title>');
        });
        cy.visit('/login');
        cy.window().then((win) =>
            Promise.all(
                ['/favicon.ico', '/apple-touch-icon.png'].map(
                    (src) =>
                        new Promise((resolve, reject) => {
                            const img = new win.Image();
                            img.onload = () => {
                                const canvas =
                                    win.document.createElement('canvas');
                                canvas.width = canvas.height = 32;
                                const ctx = canvas.getContext('2d');
                                ctx.drawImage(img, 0, 0, 32, 32);
                                resolve([
                                    src,
                                    [...ctx.getImageData(3, 16, 1, 1).data],
                                ]);
                            };
                            img.onerror = reject;
                            img.src = `${src}?v=${Date.now()}`;
                        }),
                ),
            ).then((pixeles) => {
                pixeles.forEach(([src, [r, g, b, alfa]]) => {
                    expect(
                        alfa,
                        `${src} opaco en el borde de la baldosa`,
                    ).to.be.greaterThan(200);
                    expect(r, `${src} sin el rojo de Laravel`).to.be.lessThan(
                        80,
                    );
                    expect(
                        b,
                        `${src} en el petróleo de la marca`,
                    ).to.be.greaterThan(r);
                    expect(
                        g,
                        `${src} en el petróleo de la marca`,
                    ).to.be.greaterThan(r);
                });
            }),
        );
    });

    it('el título «Navegación» del menú móvil se lee en claro y en oscuro y conserva nombre y foco', () => {
        cy.loginAs('hr');
        cy.viewport(390, 844);

        ['light', 'dark'].forEach((tema) => {
            cy.visit('/dashboard', {
                onBeforeLoad: (win) =>
                    win.localStorage.setItem('appearance', tema),
            });
            cy.get('[data-sidebar="trigger"]').click();
            cy.get('[data-mobile="true"] h2')
                .should('be.visible')
                .and('have.text', 'Navegación')
                .then(($h) => {
                    expect(
                        contraste($h[0]),
                        `contraste en tema ${tema}`,
                    ).to.be.at.least(4.5);
                });
            // El panel sigue nombrado por su título y el foco queda dentro.
            cy.get('[data-mobile="true"]')
                .invoke('attr', 'aria-labelledby')
                .then((id) =>
                    cy.get(`[id="${id}"]`).should('have.text', 'Navegación'),
                );
            cy.focused().closest('[data-mobile="true"]').should('exist');
            cy.get('body').type('{esc}');
            cy.get('[data-mobile="true"]').should('not.exist');
            cy.focused().should('have.attr', 'data-sidebar', 'trigger');
        });
    });

    it('una búsqueda sin coincidencias nombra el término y «Ver todas las convocatorias» quita el filtro', () => {
        cy.visit('/empleos?q=astronauta');
        cy.dataCy('empty-state')
            .should(
                'contain.text',
                'Ninguna convocatoria coincide con «astronauta»',
            )
            .and('not.contain.text', 'No hay convocatorias vigentes');
        cy.dataCy('jobs-search').should('have.value', 'astronauta');

        cy.dataCy('jobs-clear-search').click();
        cy.location('pathname').should('eq', '/empleos');
        cy.location('search').should('eq', '');
        cy.dataCy('jobs-search').should('have.value', '');
        cy.dataCy('job-card').should('have.length.greaterThan', 0);
    });

    it('una página vacía de una lista con ofertas no dice que no existan ofertas', () => {
        cy.visit('/empleos?page=99');
        cy.dataCy('empty-state')
            .should('contain.text', 'Esta página no tiene convocatorias')
            .and('not.contain.text', 'Todavía no hay convocatorias publicadas');

        cy.dataCy('jobs-first-page').click();
        cy.location('search').should('eq', '');
        cy.dataCy('job-card').should('have.length.greaterThan', 0);
    });

    it('la vacante con el plazo vencido lo muestra y conserva su estado formal «Publicada»', () => {
        cy.visit('/empleos');
        cy.dataCy('deadline-passed').should('have.length', 1);
        cy.dataCy('deadline-passed')
            .closest('[data-cy="job-card"]')
            .should('contain.text', 'Plazo de postulación vencido')
            .find('[data-cy="job-detail-link"]')
            .click();

        cy.dataCy('apply-panel').within(() => {
            cy.dataCy('status-badge').should('contain.text', 'Publicada');
            cy.dataCy('deadline-passed').should('be.visible');
            cy.contains('El plazo de postulación venció el').should(
                'be.visible',
            );
        });

        cy.loginAs('hr');
        cy.visit('/vacantes');
        cy.dataCy('deadline-passed').should('have.length', 1);
    });

    it('las páginas de error hablan español, conservan su código y ofrecen una salida según la sesión', () => {
        cy.request({ url: '/empleos/999999', failOnStatusCode: false })
            .its('status')
            .should('eq', 404);
        cy.visit('/empleos/999999', { failOnStatusCode: false });
        cy.get('html').should('have.attr', 'lang', 'es');
        cy.get('h1').should('have.text', 'No encontramos esta página');
        cy.contains('a', 'Ver empleos disponibles').should(
            'have.attr',
            'href',
            '/empleos',
        );
        cy.contains('a', 'Iniciar sesión').focus();
        cy.focused().should('have.attr', 'href', '/login');

        // Sin cabecera Sec-Fetch-Site ni token (cliente fuera del navegador): 419.
        cy.request({
            method: 'POST',
            url: '/login',
            failOnStatusCode: false,
        }).then((r) => {
            expect(r.status).to.eq(419);
            expect(r.body).to.contain('La página expiró');
        });
        cy.request({
            method: 'POST',
            url: '/login',
            failOnStatusCode: false,
            headers: { Accept: 'application/json' },
        }).then((r) => {
            expect(r.status).to.eq(419);
            expect(r.headers['content-type']).to.contain('application/json');
        });

        cy.loginAs('hr');
        cy.visit('/auditoria', { failOnStatusCode: false });
        cy.get('h1').should(
            'have.text',
            'No tiene permiso para ver esta página',
        );
        cy.contains('a', 'Ir a mi panel').should(
            'have.attr',
            'href',
            '/dashboard',
        );
        cy.get('body').should(
            'not.contain.text',
            'This action is unauthorized',
        );
        cy.appRequest('GET', '/auditoria').then((r) => {
            expect(r.status).to.eq(403);
            expect(r.headers['content-type']).to.contain('application/json');
        });
    });

    it('el 419 depende del origen: Laravel acepta mismo origen sin token y exige token a mismo sitio y otro sitio', () => {
        // PreventRequestForgery (Laravel 13) acepta Sec-Fetch-Site: same-origin; same-site solo si se
        // habilita allowSameSite(), que esta aplicación no usa. Sin token, todo lo demás recibe 419.
        const enviar = (secFetchSite) =>
            cy.request({
                method: 'POST',
                url: '/login',
                failOnStatusCode: false,
                followRedirect: false,
                headers: secFetchSite ? { 'Sec-Fetch-Site': secFetchSite } : {},
            });

        enviar('same-origin').its('status').should('not.eq', 419);
        enviar('same-site').its('status').should('eq', 419);
        enviar('cross-site').its('status').should('eq', 419);
        enviar('none').its('status').should('eq', 419);
        enviar(null).its('status').should('eq', 419);
    });

    it('una visita interna hacia un 403 o un 404 muestra la página de error sin el modal de Inertia', () => {
        cy.loginAs('hr');

        [
            ['/auditoria', 'No tiene permiso para ver esta página'],
            ['/empleos/999999', 'No encontramos esta página'],
        ].forEach(([destino, encabezado]) => {
            // La visita real de Inertia (al pulsar «Notificaciones») se desvía hacia la ruta de error.
            cy.intercept(
                {
                    method: 'GET',
                    pathname: '/notificaciones',
                    headers: { 'x-inertia': 'true' },
                },
                (req) => {
                    req.url = req.url.replace('/notificaciones', destino);
                },
            ).as('visita');
            cy.visit('/dashboard');
            cy.dataCy('quick-links').find('a[href$="/notificaciones"]').click();
            cy.wait('@visita')
                .its('response.statusCode')
                .should('eq', destino === '/auditoria' ? 403 : 404);

            cy.location('pathname').should('eq', destino);
            cy.dataCy('http-error').find('h1').should('have.text', encabezado);
            cy.contains('a', 'Ir a mi panel').should(
                'have.attr',
                'href',
                '/dashboard',
            );
            cy.get('dialog, iframe').should('not.exist');
        });
    });

    it('acceso y registro explican la decisión humana sin códigos de requisito', () => {
        cy.visit('/register');
        cy.contains('seleccionar es un acto humano con justificación').should(
            'be.visible',
        );
        cy.get('body')
            .invoke('text')
            .should('not.match', /RF-\d+/);
    });

    it('el postulante no ve códigos RF y la auditoría muestra etiquetas legibles', () => {
        cy.loginAs('candidateNew');
        cy.visit('/dashboard');
        cy.dataCy('quick-links').should('be.visible');
        cy.get('body')
            .invoke('text')
            .should('not.match', /RF-\d+/);
        // La trazabilidad sigue en el marcado, no en el texto.
        cy.get('[data-rf="RF-09"]').should('exist');
        cy.visit('/mi-perfil');
        cy.get('h1').should('be.visible');
        cy.get('body')
            .invoke('text')
            .should('not.match', /RF-\d+/);

        cy.loginAs('approver');
        cy.visit('/auditoria');
        cy.get('main')
            .should('not.contain.text', 'evidence_item')
            .and('contain.text', 'Evidencia');
    });
});
