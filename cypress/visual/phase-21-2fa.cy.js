/**
 * Flujo visual de la verificación en dos pasos. NO forma parte de la suite E2E.
 *
 * Hasta la Fase 21 nadie había visto los códigos de recuperación: los
 * usuarios de demostración no tienen 2FA. Aquí se activa de verdad, con un
 * código TOTP calculado en la propia prueba, sobre una cuenta que ninguna
 * suite usa, y la base se restablece al terminar para que el 2FA no se filtre
 * a otras pruebas.
 *
 * `crypto.subtle` no existe en un origen que no es seguro (`http://app-e2e`),
 * así que SHA-1 y HMAC van escritos a mano. No es código de producción: solo
 * genera el código que escribiría una persona con su aplicación.
 */
const CUENTA = 'postulante2@correo.test';

// Clave obtenida al activar el 2FA en la primera prueba; la segunda la
// necesita para superar el desafío de inicio de sesión.
let secreto = null;

function sha1(bytes) {
    const ml = bytes.length * 8;
    const len = (((bytes.length + 8) >> 6) + 1) * 64;
    const m = new Uint8Array(len);

    m.set(bytes);
    m[bytes.length] = 0x80;

    const dv = new DataView(m.buffer);

    dv.setUint32(len - 4, ml >>> 0);
    dv.setUint32(len - 8, Math.floor(ml / 2 ** 32));

    let [a0, b0, c0, d0, e0] = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0];
    const w = new Uint32Array(80);
    const rotl = (x, n) => (x << n) | (x >>> (32 - n));

    for (let i = 0; i < len; i += 64) {
        for (let t = 0; t < 16; t++) w[t] = dv.getUint32(i + t * 4);
        for (let t = 16; t < 80; t++) w[t] = rotl(w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16], 1);

        let [a, b, c, d, e] = [a0, b0, c0, d0, e0];

        for (let t = 0; t < 80; t++) {
            const [f, k] =
                t < 20
                    ? [(b & c) | (~b & d), 0x5a827999]
                    : t < 40
                      ? [b ^ c ^ d, 0x6ed9eba1]
                      : t < 60
                        ? [(b & c) | (b & d) | (c & d), 0x8f1bbcdc]
                        : [b ^ c ^ d, 0xca62c1d6];
            const tmp = (rotl(a, 5) + f + e + k + w[t]) >>> 0;

            [e, d, c, b, a] = [d, c, rotl(b, 30) >>> 0, a, tmp];
        }

        [a0, b0, c0, d0, e0] = [(a0 + a) >>> 0, (b0 + b) >>> 0, (c0 + c) >>> 0, (d0 + d) >>> 0, (e0 + e) >>> 0];
    }

    const out = new Uint8Array(20);
    const ov = new DataView(out.buffer);

    [a0, b0, c0, d0, e0].forEach((h, i) => ov.setUint32(i * 4, h));

    return out;
}

function hmacSha1(key, msg) {
    const k = new Uint8Array(64);

    k.set(key.length > 64 ? sha1(key) : key);

    const ipad = k.map((x) => x ^ 0x36);
    const opad = k.map((x) => x ^ 0x5c);
    const inner = sha1(new Uint8Array([...ipad, ...msg]));

    return sha1(new Uint8Array([...opad, ...inner]));
}

function totp(secret, desfase = 0) {
    const abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    const bits = secret
        .replace(/[\s=]/g, '')
        .toUpperCase()
        .split('')
        .map((c) => abc.indexOf(c).toString(2).padStart(5, '0'))
        .join('');
    const key = new Uint8Array(Math.floor(bits.length / 8)).map((_, i) =>
        parseInt(bits.slice(i * 8, i * 8 + 8), 2),
    );
    // Fortify acepta el paso anterior y el siguiente, y rechaza reutilizar un
    // código: el desfase permite dar un código distinto al ya usado.
    const contador = Math.floor(Date.now() / 1000 / 30) + desfase;
    const msg = new Uint8Array(8);

    new DataView(msg.buffer).setUint32(4, contador);

    const h = hmacSha1(key, msg);
    const o = h[19] & 0xf;
    const codigo =
        (((h[o] & 0x7f) << 24) | (h[o + 1] << 16) | (h[o + 2] << 8) | h[o + 3]) % 1e6;

    return String(codigo).padStart(6, '0');
}

function reducido(activo) {
    return Cypress.automation('remote:debugger:protocol', {
        command: 'Emulation.setEmulatedMedia',
        params: {
            features: activo ? [{ name: 'prefers-reduced-motion', value: 'reduce' }] : [],
        },
    });
}

/**
 * Pulsación real, enviada por el protocolo del navegador: es el navegador, y
 * no Cypress, quien decide qué hace la tecla sobre el elemento enfocado.
 * `cy.type('{enter}')` no reproduce la activación nativa de un botón.
 */
function teclaReal(tecla) {
    const codigos = { Enter: 13, ' ': 32 };
    const base = {
        key: tecla,
        code: tecla === ' ' ? 'Space' : tecla,
        windowsVirtualKeyCode: codigos[tecla],
        nativeVirtualKeyCode: codigos[tecla],
    };

    return Cypress.automation('remote:debugger:protocol', {
        command: 'Input.dispatchKeyEvent',
        params: { ...base, type: 'keyDown', text: tecla === 'Enter' ? '\r' : ' ' },
    }).then(() =>
        Cypress.automation('remote:debugger:protocol', {
            command: 'Input.dispatchKeyEvent',
            params: { ...base, type: 'keyUp' },
        }),
    );
}

function foto(nombre) {
    cy.window().then(
        (win) =>
            new Cypress.Promise((resolve) => {
                const finitas = win.document
                    .getAnimations()
                    .filter((a) => a.effect?.getTiming().iterations !== Infinity);

                Promise.all(finitas.map((a) => a.finished)).then(resolve, resolve);
            }),
    );
    cy.screenshot(nombre, { capture: 'viewport', overwrite: true });
}

function entrar(tema = 'light') {
    cy.visit('/login', {
        onBeforeLoad: (win) => win.localStorage.setItem('appearance', tema),
    });
    cy.dataCy('login-email').type(CUENTA);
    cy.dataCy('login-password').type(Cypress.env('DEMO_PASSWORD'), { log: false });
    cy.dataCy('login-submit').click();
    cy.location('pathname').should('match', /^\/(dashboard|two-factor-challenge)$/);
    cy.location('pathname').then((ruta) => {
        if (ruta === '/two-factor-challenge') {
            foto(`05-2fa-desafio-${tema}`);
            cy.get('input[name=code]').type(totp(secreto, 1));
            cy.contains('button', 'Continuar').click();
        }
    });
    cy.location('pathname').should('eq', '/dashboard');
}

function confirmarContrasena() {
    cy.visit('/user/confirm-password');
    cy.get('input[name=password]').type(Cypress.env('DEMO_PASSWORD'), { log: false });
    cy.get('[data-test=confirm-password-button]').click();
    cy.location('pathname').should('not.eq', '/user/confirm-password');
}

describe('Fase 21 · verificación en dos pasos', () => {
    before(() => cy.resetDatabase());
    after(() => cy.resetDatabase());
    afterEach(() => reducido(false));

    it('se activa, muestra los códigos y responde al teclado', () => {
        cy.viewport(1024, 800);
        entrar();
        confirmarContrasena();
        cy.visit('/settings/security');

        cy.contains('button', 'Activar la verificación en dos pasos').click();
        cy.get('[role=dialog]').should('be.visible');
        cy.get('[role=dialog] input[readonly]')
            .invoke('val')
            .should('match', /^[A-Z2-7]{16,}$/);
        foto('01-2fa-configurar');

        cy.get('[role=dialog] input[readonly]').invoke('val').then((clave) => {
            secreto = String(clave);
            cy.contains('[role=dialog] button', 'Continuar').click();
            cy.get('[role=dialog] input[name=code]').type(totp(String(clave)));
            cy.contains('[role=dialog] button', 'Confirmar').click();
        });
        cy.get('[role=dialog]').should('not.exist');

        // Plegados: el contenedor existe pero está oculto a la tecnología
        // asistiva y no ocupa altura.
        cy.contains('button', 'Ver los códigos')
            .should('have.attr', 'aria-expanded', 'false')
            .as('alternar');
        cy.get('#recovery-codes-section')
            .should('have.attr', 'aria-hidden', 'true')
            .invoke('outerHeight')
            .should('be.lessThan', 2);
        cy.get('@alternar').scrollIntoView({ offset: { top: -240, left: 0 } });
        foto('02-2fa-plegado');

        // Con teclado: el botón se alcanza, Enter despliega y Enter pliega.
        cy.get('@alternar').focus();
        cy.focused().should('have.attr', 'aria-controls', 'recovery-codes-section');
        cy.then(() => teclaReal('Enter'));
        cy.contains('button', 'Ocultar los códigos').should('have.attr', 'aria-expanded', 'true');
        cy.get('#recovery-codes-section')
            .should('have.attr', 'aria-hidden', 'false')
            .find('[role=listitem]')
            .should('have.length.at.least', 8);
        // Los dos botones caben dentro de la tarjeta: en la columna angosta de
        // la configuración, el segundo se desbordaba sin permitir el salto.
        cy.contains('button', 'Generar códigos nuevos').then(($b) => {
            const tarjeta = $b[0].closest('section').getBoundingClientRect();

            expect($b[0].getBoundingClientRect().right).to.be.at.most(tarjeta.right);
        });
        foto('03-2fa-desplegado');

        // Espacio también activa un botón nativo.
        cy.contains('button', 'Ocultar los códigos').focus();
        cy.then(() => teclaReal(' '));
        cy.contains('button', 'Ver los códigos').should('have.attr', 'aria-expanded', 'false');
    });

    it('en oscuro, a 390 px y con movimiento reducido', () => {
        reducido(true);
        cy.viewport(390, 844);
        entrar('dark');
        confirmarContrasena();
        cy.visit('/settings/security');

        // Solo se espía la lista que desplaza el componente: Cypress usa
        // `scrollIntoView` para sus propios clics y no hay que tocarlo.
        cy.get('[role=list][aria-label="Códigos de recuperación"]').then(($lista) => {
            cy.stub($lista[0], 'scrollIntoView').as('desplazar');
        });
        // A 390 px Cypress desplaza el botón al borde superior, bajo la
        // cabecera fija; una persona no desplaza así.
        cy.contains('button', 'Ver los códigos').click({ scrollBehavior: 'center' });
        cy.get('#recovery-codes-section [role=listitem]').should('have.length.at.least', 8);

        // Con movimiento reducido el salto es inmediato, no animado.
        cy.get('@desplazar').should('have.been.calledWithMatch', { behavior: 'auto' });
        cy.document().then((doc) => {
            expect(doc.documentElement.scrollWidth - doc.documentElement.clientWidth).to.be.lessThan(2);
        });
        foto('04-2fa-oscuro-390-reducido');
    });
});
