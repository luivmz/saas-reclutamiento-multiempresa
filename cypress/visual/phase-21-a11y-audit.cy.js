/**
 * Auditoría de accesibilidad sobre el DOM real. NO forma parte de la suite E2E.
 *
 * No hay axe-core ni lector de pantalla en el entorno, y la fase no autoriza
 * instalarlos. Esto es un equivalente acotado, escrito sobre la
 * infraestructura Cypress que ya existe: comprueba de forma mecánica las
 * reglas de mayor valor en cada página, rol y tema, y escribe los hallazgos
 * en `cypress/results/phase-21-a11y.json`. No falla por hallazgos: los
 * registra para clasificarlos.
 *
 * Reglas:
 * - ids duplicados;
 * - controles sin nombre accesible (y los que solo se nombran por placeholder);
 * - referencias ARIA rotas (`aria-labelledby`, `aria-describedby`, `for`,
 *   `headers`; `aria-controls` solo si el control está expandido, como axe);
 * - saltos en la jerarquía de encabezados y número de `h1`;
 * - un único `main`; varios `nav` sin nombre que los distinga;
 * - elementos enfocables dentro de `aria-hidden` sin `inert`;
 * - `tabindex` positivo;
 * - imágenes sin alternativa;
 * - contraste WCAG 1.4.3 calculado sobre colores renderizados;
 * - objetivos táctiles menores de 24 × 24 px (WCAG 2.5.8), con su vecino
 *   más próximo para evaluar la excepción de espaciado.
 *
 * Los colores del sistema son `oklch()`, y Chrome devuelve el color calculado
 * tal cual: por eso cada color se resuelve pintándolo en un lienzo de 1 × 1 y
 * leyendo el píxel en sRGB, y las capas con transparencia se componen hacia
 * arriba hasta encontrar un fondo opaco.
 */

const RESULTADOS = 'cypress/results/phase-21-a11y.json';

function auditar(win, { contraste = true, objetivos = false } = {}) {
    const doc = win.document;
    const hallazgos = [];
    const add = (regla, el, detalle = '') =>
        hallazgos.push({ regla, el: describir(el), detalle });

    function describir(el) {
        if (!el || !el.tagName) {
            return String(el);
        }

        const cy = el.getAttribute('data-cy');
        const id = el.id ? `#${el.id}` : '';
        const texto = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);

        return `${el.tagName.toLowerCase()}${id}${cy ? `[cy=${cy}]` : ''} «${texto}»`;
    }

    function oculto(el) {
        for (let n = el; n && n !== doc.body; n = n.parentElement) {
            if (n.getAttribute('aria-hidden') === 'true' || n.hasAttribute('inert')) {
                return true;
            }

            const s = win.getComputedStyle(n);

            if (s.display === 'none' || s.visibility === 'hidden') {
                return true;
            }
        }

        const box = el.getBoundingClientRect();

        return box.width === 0 && box.height === 0;
    }

    function visualmenteOculto(el) {
        // `sr-only`: 1 × 1 px recortado. Existe para la tecnología asistiva.
        const s = win.getComputedStyle(el);
        const recortado =
            s.clipPath === 'inset(50%)' || s.clip === 'rect(0px, 0px, 0px, 0px)';

        return (
            recortado ||
            (s.position === 'absolute' &&
                parseFloat(s.width) <= 1 &&
                parseFloat(s.height) <= 1)
        );
    }

    function textoDe(id) {
        const el = doc.getElementById(id);

        return el ? el.textContent.trim() : '';
    }

    function nombre(el) {
        const labelledby = el.getAttribute('aria-labelledby');

        if (labelledby) {
            const t = labelledby.split(/\s+/).map(textoDe).join(' ').trim();

            if (t) return t;
        }

        const label = el.getAttribute('aria-label');

        if (label && label.trim()) return label.trim();

        if (el.id) {
            const lbl = doc.querySelector(`label[for="${CSS.escape(el.id)}"]`);

            if (lbl && lbl.textContent.trim()) return lbl.textContent.trim();
        }

        const envolvente = el.closest('label');

        if (envolvente && envolvente.textContent.trim()) return envolvente.textContent.trim();

        if (['BUTTON', 'A'].includes(el.tagName) || el.getAttribute('role')) {
            const t = el.textContent.trim();

            if (t) return t;

            const img = el.querySelector('img[alt]');

            if (img && img.alt.trim()) return img.alt.trim();
        }

        if (el.getAttribute('title')) return el.getAttribute('title');

        return '';
    }

    // --- ids duplicados ------------------------------------------------------
    const vistos = new Map();

    doc.querySelectorAll('[id]').forEach((el) => {
        vistos.set(el.id, (vistos.get(el.id) || 0) + 1);
    });
    vistos.forEach((n, id) => {
        if (n > 1 && id) add('id-duplicado', doc.getElementById(id), `${n} veces`);
    });

    // --- controles sin nombre ----------------------------------------------
    const controles = doc.querySelectorAll(
        'button, a[href], input:not([type=hidden]), select, textarea, [role=button], [role=link], [role=menuitem], [role=menuitemradio], [role=tab], [role=checkbox], [role=radio], [role=switch], [role=combobox]',
    );

    controles.forEach((el) => {
        if (oculto(el)) return;

        const n = nombre(el);

        if (!n) {
            if (el.getAttribute('placeholder')) {
                add('nombre-solo-placeholder', el, el.getAttribute('placeholder'));
            } else {
                add('control-sin-nombre', el);
            }
        }
    });

    // --- referencias ARIA -----------------------------------------------------
    [
        ['aria-labelledby', false],
        ['aria-describedby', false],
        ['aria-controls', true],
        ['headers', false],
    ].forEach(([attr, soloExpandido]) => {
        doc.querySelectorAll(`[${attr}]`).forEach((el) => {
            if (soloExpandido && el.getAttribute('aria-expanded') !== 'true') return;

            el.getAttribute(attr)
                .split(/\s+/)
                .filter(Boolean)
                .forEach((id) => {
                    if (!doc.getElementById(id)) add('idref-roto', el, `${attr}=${id}`);
                });
        });
    });

    doc.querySelectorAll('label[for]').forEach((el) => {
        if (!doc.getElementById(el.getAttribute('for'))) {
            add('idref-roto', el, `for=${el.getAttribute('for')}`);
        }
    });

    // --- encabezados -----------------------------------------------------------
    const encabezados = [...doc.querySelectorAll('h1, h2, h3, h4, h5, h6')].filter(
        (h) => !oculto(h),
    );
    const h1 = encabezados.filter((h) => h.tagName === 'H1').length;

    if (h1 !== 1) add('h1-distinto-de-uno', doc.body, `${h1} h1`);

    let previo = 0;

    encabezados.forEach((h) => {
        const nivel = Number(h.tagName[1]);

        if (previo && nivel > previo + 1) add('salto-de-encabezado', h, `h${previo} → h${nivel}`);

        previo = nivel;
    });

    // --- landmarks -------------------------------------------------------------
    const mains = [...doc.querySelectorAll('main, [role=main]')];

    if (mains.length !== 1) add('main-distinto-de-uno', doc.body, `${mains.length} main`);

    const navs = [...doc.querySelectorAll('nav, [role=navigation]')].filter((n) => !oculto(n));

    if (navs.length > 1) {
        const nombres = navs.map((n) => n.getAttribute('aria-label') || textoDe(n.getAttribute('aria-labelledby') || ''));

        navs.forEach((n, i) => {
            if (!nombres[i]) add('nav-sin-nombre', n, `${navs.length} nav en la página`);
        });

        const repetidos = nombres.filter((x, i) => x && nombres.indexOf(x) !== i);

        repetidos.forEach((x) => add('nav-nombre-repetido', doc.body, x));
    }

    // --- enfocables ocultos y tabindex positivo -------------------------------
    const enfocables =
        'a[href], button:not([disabled]), input:not([disabled]):not([type=hidden]), select:not([disabled]), textarea:not([disabled]), [tabindex]';

    doc.querySelectorAll('[aria-hidden=true]').forEach((cont) => {
        if (cont.closest('[inert]')) return;

        cont.querySelectorAll(enfocables).forEach((el) => {
            if (el.getAttribute('tabindex') === '-1') return;

            add('enfocable-en-aria-hidden', el);
        });
    });

    doc.querySelectorAll('[tabindex]').forEach((el) => {
        if (Number(el.getAttribute('tabindex')) > 0) add('tabindex-positivo', el, el.getAttribute('tabindex'));
    });

    // --- imágenes -------------------------------------------------------------
    doc.querySelectorAll('img').forEach((img) => {
        if (!oculto(img) && !img.hasAttribute('alt')) add('img-sin-alt', img);
    });

    // --- contraste -------------------------------------------------------------
    if (contraste) {
        const lienzo = doc.createElement('canvas');

        lienzo.width = lienzo.height = 1;

        const ctx = lienzo.getContext('2d', { willReadFrequently: true });

        const rgba = (css) => {
            ctx.clearRect(0, 0, 1, 1);
            ctx.fillStyle = '#000';
            ctx.fillStyle = css;
            ctx.fillRect(0, 0, 1, 1);

            const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;

            return [r, g, b, a / 255];
        };

        const sobre = (arriba, abajo) => {
            const a = arriba[3];

            return [
                arriba[0] * a + abajo[0] * (1 - a),
                arriba[1] * a + abajo[1] * (1 - a),
                arriba[2] * a + abajo[2] * (1 - a),
                1,
            ];
        };

        const luminancia = ([r, g, b]) => {
            const c = [r, g, b].map((v) => {
                const s = v / 255;

                return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
            });

            return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
        };

        const razon = (x, y) => {
            const [l1, l2] = [luminancia(x), luminancia(y)].sort((p, q) => q - p);

            return (l1 + 0.05) / (l2 + 0.05);
        };

        const fondo = (el) => {
            const capas = [];
            let imagen = false;

            for (let n = el; n; n = n.parentElement) {
                const s = win.getComputedStyle(n);

                if (s.backgroundImage && s.backgroundImage !== 'none') imagen = true;

                const c = rgba(s.backgroundColor);

                if (c[3] > 0) capas.push(c);
                if (c[3] >= 1) break;
            }

            let base = [255, 255, 255, 1];

            if (!capas.length || capas[capas.length - 1][3] < 1) {
                base = rgba(win.getComputedStyle(doc.documentElement).backgroundColor);
                if (base[3] < 1) base = [255, 255, 255, 1];
            }

            return { color: capas.reverse().reduce((acc, c) => sobre(c, acc), base), imagen };
        };

        const opacidad = (el) => {
            let o = 1;

            for (let n = el; n; n = n.parentElement) o *= parseFloat(win.getComputedStyle(n).opacity);

            return o;
        };

        const revisados = new Set();
        const recorrido = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);

        for (let t = recorrido.nextNode(); t; t = recorrido.nextNode()) {
            const el = t.parentElement;

            if (!el || revisados.has(el) || !t.textContent.trim()) continue;

            revisados.add(el);

            if (oculto(el) || visualmenteOculto(el)) continue;
            // WCAG 1.4.3 no aplica a controles deshabilitados.
            if (el.closest(':disabled, [aria-disabled=true]')) continue;

            const s = win.getComputedStyle(el);
            const { color: bg, imagen } = fondo(el);

            if (imagen) continue;

            const texto = sobre([...rgba(s.color).slice(0, 3), rgba(s.color)[3] * opacidad(el)], bg);
            const r = razon(texto, bg);
            const size = parseFloat(s.fontSize);
            const grande = size >= 24 || (size >= 18.66 && Number(s.fontWeight) >= 700);
            const minimo = grande ? 3 : 4.5;

            if (r < minimo) {
                add('contraste', el, `${r.toFixed(2)}:1 (mín. ${minimo}) · ${size}px`);
            }
        }
    }

    // --- tamaño de objetivos ---------------------------------------------------
    if (objetivos) {
        const blancos = [
            ...doc.querySelectorAll(
                'button, a[href], input[type=checkbox], input[type=radio], [role=button], [role=checkbox], [role=switch], [role=tab], [role=menuitem]',
            ),
        ].filter((el) => !oculto(el) && !visualmenteOculto(el));

        const cajas = blancos.map((el) => ({ el, b: el.getBoundingClientRect() }));

        cajas.forEach(({ el, b }) => {
            if (b.width >= 24 && b.height >= 24) return;
            // Enlaces dentro de una frase: exentos (WCAG 2.5.8, «inline»).
            if (el.tagName === 'A' && win.getComputedStyle(el).display === 'inline') return;
            // Casillas con etiqueta asociada: la etiqueta también activa el control.
            const rolDeCasilla = el.getAttribute('role') || el.type || '';

            if (/^(checkbox|radio|switch)$/.test(rolDeCasilla) && nombre(el)) return;

            const cx = b.left + b.width / 2;
            const cy = b.top + b.height / 2;
            let vecino = Infinity;

            cajas.forEach((o) => {
                if (o.el === el || o.el.contains(el) || el.contains(o.el)) return;

                const dx = Math.max(o.b.left - cx, 0, cx - o.b.right);
                const dy = Math.max(o.b.top - cy, 0, cy - o.b.bottom);

                vecino = Math.min(vecino, Math.hypot(dx, dy));
            });

            add(
                'objetivo-pequeño',
                el,
                `${Math.round(b.width)}×${Math.round(b.height)} px; vecino a ${Math.round(vecino)} px${vecino >= 12 ? ' (cumple por espaciado)' : ''}`,
            );
        });
    }

    return hallazgos;
}

const paginas = [
    { rol: null, rutas: ['/', '/empleos', '/empleos/2', '/login', '/register', '/forgot-password', '/reset-password/token-ficticio?email=nadie%40ejemplo.test'] },
    {
        rol: 'hr',
        rutas: ['/dashboard', '/requerimientos', '/requerimientos/4', '/vacantes', '/vacantes/crear', '/vacantes/1', '/vacantes/2', '/vacantes/1/editar', '/vacantes/3/postulaciones', '/postulaciones/4', '/vacantes/3/comparacion', '/notificaciones', '/settings/profile', '/settings/security', '/settings/appearance', '/user/confirm-password'],
    },
    { rol: 'requester', rutas: ['/dashboard', '/requerimientos/crear'] },
    { rol: 'approver', rutas: ['/auditoria', '/vacantes/3/comparacion', '/requerimientos/4'] },
    { rol: 'evaluator', rutas: ['/mis-evaluaciones'], asignaciones: true },
    { rol: 'candidateSubmitted', rutas: ['/mi-perfil', '/mis-postulaciones', '/mis-postulaciones/1', '/empleos/2'] },
    { rol: 'candidateNew', rutas: ['/mi-perfil', '/mis-postulaciones'] },
];

describe('Fase 21 · auditoría de accesibilidad del DOM', () => {
    const informe = [];

    before(() => cy.resetDatabase());

    after(() => cy.writeFile(RESULTADOS, informe));

    function visitar(ruta, tema, ancho) {
        cy.viewport(ancho, 900);
        cy.visit(ruta, {
            onBeforeLoad(win) {
                win.localStorage.setItem('appearance', tema);
            },
        });
        cy.get('h1, [data-cy=page-title]').should('exist');
        cy.get('html').should(tema === 'dark' ? 'have.class' : 'not.have.class', 'dark');
        // La capa de profundidad y el riesgo operacional terminan de montar.
        cy.get('body').then(($b) => {
            if ($b.find('[data-cy=operational-risk-panel]').length) {
                cy.dataCy('operational-risk-message').should('exist');
            }
        });
    }

    function registrar(rol, ruta, tema, ancho, opciones) {
        cy.window().then(
            (win) =>
                new Cypress.Promise((resolve) => {
                    const finitas = win.document
                        .getAnimations()
                        .filter(
                            (a) => a.effect?.getTiming().iterations !== Infinity,
                        );

                    Promise.all(finitas.map((a) => a.finished)).then(
                        resolve,
                        resolve,
                    );
                }),
        );
        cy.window().then((win) => {
            auditar(win, opciones).forEach((h) =>
                informe.push({ rol: rol || 'público', ruta, tema, ancho, ...h }),
            );
        });
    }

    // Los estados de error no aparecen al cargar una página: hay que
    // provocarlos. Sin esto, la auditoría nunca vio una alerta destructiva ni
    // un campo con error, y por ahí se colaron dos defectos de contraste.
    it('auditoría · estados de error', () => {
        cy.loginAs('requester');

        ['light', 'dark'].forEach((tema) => {
            visitar('/requerimientos?estado=rechazado', tema, 1280);
            cy.dataCy('job-request-link').first().click();
            cy.dataCy('rejection-alert').should('be.visible');
            cy.location('pathname').then((ruta) =>
                registrar('requester', `${ruta} (rechazado)`, tema, 1280, { contraste: true }),
            );

            visitar('/requerimientos/crear', tema, 1280);
            cy.dataCy('save-job-request').click();
            cy.get('[role=alert]').should('have.length.at.least', 1);
            registrar('requester', '/requerimientos/crear (errores)', tema, 1280, { contraste: true });
        });
    });

    paginas.forEach(({ rol, rutas, asignaciones }) => {
        it(`auditoría · ${rol || 'público'}`, () => {
            if (rol) cy.loginAs(rol);

            if (rutas.includes('/settings/security')) {
                cy.visit('/user/confirm-password');
                cy.get('input[name=password]').type(Cypress.env('DEMO_PASSWORD'), {
                    log: false,
                });
                cy.get('[data-test=confirm-password-button]').click();
                cy.location('pathname').should('not.eq', '/user/confirm-password');
            }

            const recorrer = (lista) =>
                lista.forEach((ruta) => {
                    visitar(ruta, 'light', 1280);
                    registrar(rol, ruta, 'light', 1280, { contraste: true });
                    visitar(ruta, 'dark', 1280);
                    registrar(rol, ruta, 'dark', 1280, { contraste: true });
                    visitar(ruta, 'light', 390);
                    registrar(rol, ruta, 'light', 390, { contraste: false, objetivos: true });
                });

            recorrer(rutas);

            if (asignaciones) {
                cy.visit('/mis-evaluaciones');
                cy.get('[data-cy=open-assignment]').then(($a) => {
                    const hrefs = [...new Set([...$a].map((a) => new URL(a.href).pathname))];

                    recorrer(hrefs);
                });
            }
        });
    });
});
