# Fase 21 — QA visual, accesibilidad, responsive y pulido final

**Fecha:** 23 de septiembre de 2026
**Rama:** `feature/phase-21-visual-qa` · **Base:** `a316c07` (cierre de la Fase 20)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **de auditoría y corrección**, no de rediseño. No añade funciones, no cambia reglas de negocio, RF, rutas, contratos de API, modelos, Policies, migraciones ni el servicio ML. RF-23 sigue siendo una decisión humana y RF-29 sigue siendo experimental. La interfaz de v1.1 queda documentada en cuatro fases, cada una en su documento: **F18 = diseño**, **F19 = movimiento**, **F20 = profundidad 3D** y **F21 = QA visual y accesibilidad** (este).

---

## 1. Objetivo

Mirar el frontend consolidado tras tres fases seguidas de cambios visuales como lo vería alguien que llega por primera vez: en anchos que nadie había probado, en oscuro, con teclado, con movimiento reducido y en los estados que no aparecen al cargar una página (errores, vacíos, rechazos, 2FA). Corregir lo que esté roto, justificar lo que se acepta y cerrar las observaciones que las Fases 18 a 20 dejaron abiertas.

## 2. Baseline

| | |
|---|---|
| Rama base | `develop` = `origin/develop` = `a316c0796237926cd8786983c7fed8259aa5fdce`, árbol limpio |
| Laravel | 408 pasadas + 8 omitidas |
| Python (`ml-service`) | 532 pasadas |
| Pruebas de componente | 36 |
| Cypress | 19 specs / 77 pruebas |
| Desbordes horizontales (`phase-18-overflow`) | 0 a 1440, 1280, 768 y 390 px |

## 3. Skills aplicados

`project-guardian` (alcance, contratos, cuándo detenerse), `reviewing-a11y` (guía de revisión de página y de código, WCAG 2.2), `frontend-design` (criterio visual, sin rediseñar), `animate` (política de movimiento de la Fase 19), `recruitment-3d-experience` (revisión de la escena y actualización de su estado) y `laravel-saas-quality` (regresión del backend, que no se tocó).

## 4. Páginas auditadas

**35 rutas y las sesiones de evaluación** de los seis perfiles de demostración, más dos estados provocados:

| Perfil | Rutas |
|---|---|
| Público | `/`, `/empleos`, `/empleos/2`, `/login`, `/register`, `/forgot-password`, `/reset-password/…` |
| RR. HH. | panel, requerimientos (lista y detalle), vacantes (lista, crear, detalle ×2, editar), postulaciones de una vacante, expediente, comparación, notificaciones, perfil, **seguridad**, apariencia, confirmar contraseña |
| Solicitante | panel, crear requerimiento; **requerimiento rechazado** y **formulario con errores** (provocados) |
| Aprobador | auditoría, comparación, requerimiento |
| Evaluador | mis evaluaciones y **cada sesión de evaluación asignada** |
| Postulante con postulación | perfil, mis postulaciones, detalle, vacante pública |
| Postulante nuevo | perfil incompleto, mis postulaciones vacía |

`/settings/security` **no se había auditado nunca**: el *middleware* de confirmación de contraseña redirigía y las pruebas anteriores medían en realidad la pantalla de confirmación. Ahora se confirma la contraseña antes de entrar.

Herramientas: `cypress/visual/phase-21-a11y-audit.cy.js` (auditoría del DOM, ver §15), `phase-21-responsive.cy.js`, `phase-21-visual.cy.js` (capturas), `phase-21-teclado.cy.js` (recorrido con Tab), `phase-21-2fa.cy.js` y `phase-21-sidebar.cy.js`. Ninguna forma parte de la suite: se ejecutan con `--config "specPattern=cypress/visual/**/*.cy.js"`.

## 5. Viewports

| Ancho | Por qué | Cómo |
|---|---|---|
| 1440 · 1280 · 768 · 390 | Los de la Fase 18 | `phase-18-overflow.cy.js`, sin cambios |
| **1024** | Umbral en que la portada pasa a dos columnas y aparece la escena 3D; columna angosta de la configuración | Desborde en todas las rutas + capturas |
| **320** | Mínimo de WCAG 1.4.10 (*Reflow*) | Desborde en todas las rutas + capturas |
| 390 | Tamaño de objetivos táctiles (WCAG 2.5.8) | Auditoría del DOM |

Las capturas por encima de 1280 px las recorta la ventana del navegador sin interfaz; 1440 se valida por DOM.

## 6. Claro y oscuro

Cada ruta se auditó en claro y en oscuro a 1280 px, con contraste medido (§15). El modo oscuro tenía los dos defectos de contraste de rojo como texto y como relleno (A2, A3). Tras corregirlos, **0 fallas de contraste en ambos temas**. Revisión visual adicional en oscuro a 320, 390, 1024 y 1280 px: expediente, empleos, auditoría, seguridad, mis postulaciones vacía, diálogo de eliminación y riesgo operacional.

## 7. Teclado

- **Recorrido con Tab** real (teclas enviadas por el protocolo del navegador, no simuladas por Cypress), 40 pulsaciones en cada una de nueve pantallas públicas e internas: ver resultado en §19. Cada pantalla se recorre recién cargada en su propia prueba: con varias visitas en la misma prueba, las teclas se perdían en las páginas públicas (artefacto del arnés, comprobado aparte; en la aplicación el foco avanza con normalidad).
- **2FA**: el botón que despliega los códigos de recuperación se alcanza con Tab y se activa con **Enter** y con **Espacio**, con pulsaciones reales; `aria-expanded` y `aria-controls` se actualizan.
- **Menús y navegación móvil**: los cubre `e2e-17-motion-accesible.cy.js` (apertura con teclado, cierre con Escape y devolución del foco), sin cambios.
- **Sin `tabindex` positivo** y **sin elementos enfocables dentro de contenedores `aria-hidden`** en ninguna de las rutas.

## 8. Foco

- El foco visible es el anillo único de la Fase 18. En el recorrido con Tab se comprobó en cada parada que el elemento enfocado tiene contorno o anillo.
- **Defecto V2 (bajo)**: el enlace «Saltar al contenido» perdía su relleno al enfocarse. `focus:not-sr-only` fija `padding: 0` y, como variante, ganaba al `px-4 py-2` base: el enlace medía 22 px de alto, por debajo de los 24 px de WCAG 2.5.8. Corregido moviendo el relleno a la variante de foco: 20 px de línea más 8 px arriba y abajo. E2E-19 exige 24 px o más.
- El foco vuelve al disparador al cerrar el menú de usuario y la navegación móvil (`e2e-17`, sin regresión).

## 9. Lector de pantalla

**No verificado con un lector real.** No hay NVDA en el equipo y la fase prohíbe instalar software sin autorización. En su lugar, la auditoría del DOM comprueba lo que un lector necesita encontrar:

- **nombre accesible** en todo control (botones, enlaces, campos, casillas de Radix con su rol);
- **referencias válidas** en `aria-labelledby`, `aria-describedby`, `aria-controls` y `headers`;
- **jerarquía de encabezados** sin saltos;
- **un único `main`** por pantalla y navegación marcada;
- **ningún id duplicado**;
- **imágenes con `alt`** y capas decorativas con `aria-hidden` e `inert`.

Resultado: cero hallazgos en todas estas reglas tras corregir A1 (§16). La prueba con NVDA y VoiceOver pasa a las Fases 24/25.

## 10. Movimiento reducido

- La política de la Fase 19 (se conservan color y opacidad, se elimina el desplazamiento) se revisó en portada, panel, tabla, formulario con errores y 2FA.
- **Observación heredada resuelta**: `scrollIntoView({ behavior: 'smooth' })` en los códigos de recuperación **pasaba por encima** de la política, porque `scroll-behavior: auto` solo gobierna el desplazamiento que decide el CSS. Nueva función `preferredScrollBehavior()` en `resources/js/lib/motion.ts`: devuelve `auto` con movimiento reducido. Verificado en el navegador con movimiento reducido emulado (el desplazamiento se pide con `behavior: 'auto'`).
- La escena 3D queda en póster con movimiento reducido (captura 20).

## 11. Responsive

- **Defecto V1 (medio, WCAG 1.4.10)**: a 320 px la cabecera pública se desbordaba **47 px** en horizontal: el logotipo y las cuatro acciones no cabían en una única fila de altura fija (`h-16`). Ahora la cabecera permite una segunda fila (`flex-wrap`, `min-h-16`); a 1024 px y más sigue siendo una sola fila (capturas 04 y 19).
- **Defecto V3 (bajo)**: en la columna angosta de la configuración a 1024 px, el segundo botón de los códigos de recuperación se salía de la tarjeta. Ahora los botones pueden saltar de línea.
- Tras las correcciones, **0 px de desborde** en las 35 rutas y las sesiones de evaluación a 1024 y 320 px, y 0 en la matriz de la Fase 18.

## 12. DataTable

Sin cambios de código. La auditoría confirma la semántica de la Fase 18 en todas las tablas: roles explícitos, `headers`/`id` válidos, encabezado para lectores de pantalla en móvil y ningún id duplicado. Las filas siguen sin animación de entrada (Fase 19). `e2e-16-tabla-accesible-movil.cy.js` sigue verde.

## 13. 2FA

**Observación heredada resuelta: el flujo visual de la verificación en dos pasos no lo había visto nadie**, porque ningún usuario de demostración la tiene activa. Se activó de verdad (`phase-21-2fa.cy.js`), con un código TOTP calculado en la propia prueba, sobre una cuenta ficticia que ninguna suite usa y restableciendo la base antes y después. Se recorrieron: configuración con QR y clave, confirmación con código, códigos plegados y desplegados, botones de la tarjeta (sin regenerar códigos), desafío de inicio de sesión, oscuro, 390 px y movimiento reducido. Encontró dos defectos:

- **Regresión de la Fase 19 (media)**: plegados, los códigos dejaban a la vista **una franja de 12 px** de la lista. El relleno superior estaba en el elemento de la fila `0fr`, que no se recorta. Se movió dentro del elemento recortado: plegado mide **menos de 2 px** y queda `aria-hidden`.
- **V3**: el desborde de botones descrito en §11.

Las capturas con QR, clave o códigos de recuperación **no se versionan**, aunque la cuenta sea ficticia: son secretos por su forma. En el repositorio solo quedan la pantalla plegada y el desafío.

## 14. 3D

- La escena de la Fase 20 se revisó junto con el resto de las pantallas, como pedía su §23. **Se mantiene como está**: se lee como profundidad y no compite con el expediente. No se amplió a ninguna otra superficie.
- Póster con movimiento reducido, a menos de 1024 px y en oscuro: correcto (capturas 19, 20 y las de la Fase 20).
- A 1024 px la escena aparece y la portada no se desborda.
- `e2e-18-profundidad-portada.cy.js` y las 13 pruebas de componente de `experience-3d/` siguen verdes.

## 15. Contraste

La auditoría calcula el contraste de cada texto visible contra el fondo opaco que tiene detrás: los colores oklch se convierten a sRGB con un lienzo de 1×1 —tal como los pinta el navegador— y las capas semitransparentes se componen. Se espera a que terminen las animaciones de entrada antes de medir (un primer falso positivo en la tarjeta de riesgo era su aparición a medio camino).

**Los estados de error no aparecen al cargar una página**, así que la auditoría los provoca: requerimiento rechazado y formulario enviado vacío. Así aparecieron los defectos más graves de la fase:

| Rol del rojo | Antes | Después (medido en la página real) |
|---|---|---|
| Alerta destructiva, claro (título y motivo) | **≈ 1:1** | 7.25:1 |
| Alerta destructiva, oscuro | 7.10:1 | 10.54:1 |
| Error de campo, claro | ≥ 4.5:1 | 7.69:1 |
| Error de campo, oscuro | 4.06:1 | 9.65:1 |
| Botón destructivo (blanco sobre rojo), claro | 5.49:1 | 5.49:1 (sin cambio) |
| Botón destructivo (blanco sobre rojo), oscuro | 4.14:1 | 5.13:1 |
| Borde de campo inválido sobre tarjeta, oscuro (WCAG 1.4.11, mínimo 3:1) | — | 3.27:1 |

Tras las correcciones: **0 fallas de contraste** en las 35 rutas, en claro y en oscuro, incluidos los estados provocados.

## 16. Defectos encontrados y corregidos

| Id | Severidad | Dónde | Causa | Corrección |
|---|---|---|---|---|
| **A4** | **Alta** | Alertas destructivas en claro: rechazo de requerimiento (RF-04), error de flujo, error de ranking, `AlertError` | La Fase 18 cambió `--destructive-foreground` a casi blanco —el color que va *sobre* el relleno rojo— y la variante de alerta lo usaba como color de texto sobre la tarjeta clara. El motivo del rechazo no se leía | `ui/alert.tsx`: texto con `--tone-danger-foreground` (7.25:1 en claro), el tono de peligro para texto; el motivo ya no se atenúa al 80 % |
| **A2** | Media | Botón destructivo, oscuro | `--destructive` con L = 0.612: blanco encima a 4.14:1 | `app.css`: L = 0.56 → 5.13:1; el borde inválido queda en 3.27:1 |
| **A3** | Media (latente) | Error de campo, oscuro | Rojo de relleno usado como texto: 4.06:1 | `input-error.tsx`: `text-tone-danger-foreground` → 9.65:1 |
| **A1** | Media | Inicio de sesión, registro, recuperar y restablecer contraseña, confirmar contraseña | El diseño de acceso no tenía `main`: un lector de pantalla no tenía a dónde saltar | `auth-simple-layout.tsx`: la columna del formulario es `main` |
| **V1** | Media | Cabecera pública a 320 px | Fila única de altura fija: +47 px de desborde (WCAG 1.4.10) | `public-layout.tsx`: `flex-wrap` y `min-h-16` |
| **F19-R** | Media | Códigos de recuperación plegados | Relleno fuera del elemento recortado de la fila `0fr`: franja de 12 px visible | `two-factor-recovery-codes.tsx`: relleno dentro de `min-h-0` |
| **V2** | Baja | Enlace de salto enfocado | `not-sr-only` anulaba el relleno: 22 px de alto | `skip-link.tsx`: `focus:px-4 focus:py-2` |
| **V3** | Baja | Botones de 2FA a 1024 px | Fila sin salto de línea en columna angosta | `two-factor-recovery-codes.tsx`: `sm:flex-wrap` |
| **M1** | Heredada | Desplazamiento a los códigos | `behavior: 'smooth'` explícito ignoraba el movimiento reducido | `lib/motion.ts` + uso en el componente |

Ningún defecto obligó a tocar backend, rutas ni contratos.

## 17. Defectos y observaciones aceptados

| Observación | Decisión | Evidencia |
|---|---|---|
| 27 objetivos de menos de 24 px a 390 px | **Aceptados**: todos cumplen WCAG 2.5.8 por la **excepción de espaciado** (un círculo de 24 px centrado en cada uno no toca a otro objetivo) | Auditoría del DOM, 0 hallazgos fuera de la excepción |
| Barra lateral: anima `width`/`left`/`right` (kit de inicio) | **Deuda aceptada** | 10 aperturas y cierres, 271 cuadros: mediana, p95 y máximo 16.7 ms, **0 cuadros de 50 ms o más**. Los desplazamientos de diseño ocurren solo tras un clic del usuario y el CLS los excluye con entrada de confianza; el 1.74 medido sale de que los clics de Cypress no son de confianza. Advertencia: el contenedor no es un equipo modesto |
| Lector de pantalla real | **Pasa a F24/F25** | §9 |
| Rendimiento y LCP indicativos | **Pasa a F24/F25** | El entorno es un contenedor; LCP no se reporta dentro del iframe de Cypress |
| `axe-core` no disponible | Sustituido por la auditoría del DOM | No es dependencia del proyecto y la fase no añade dependencias |
| Deuda de Pint / `composer check` | Fuera de alcance | La fase no toca PHP |
| CSS +0.11 kB gzip de la Fase 20 | Aceptado | Las cifras de la Fase 20 son históricamente correctas; las actuales, en §19 |
| Navegador interactivo de Codex no disponible en auditorías previas | Informativo | Las capturas de esta fase son la evidencia visual |

## 18. Gobierno

- **RNF-C** (experiencia 3D): implementar no promueve un requisito —RF-29 está integrado y sigue siendo candidato por la decisión 11—. Se dejó **propuesta**, no aprobación: pregunta 13 de [`scope-preliminary.md`](scope-preliminary.md), para que el equipo decida RNF-C junto con RF-28 y RF-29.
- **Skill `recruitment-3d-experience`**: actualizada, como pedía la fase, de «candidato, no implementado» a «implementada y acotada». Las reglas de uso no cambiaron; se añadieron las condiciones para *ampliar* el 3D y se conservó el texto anterior como nota de historia.
- ~~**`CLAUDE.md`** sigue diciendo en la tabla de skills que el 3D está «aún no implementado». **No se tocó**: la convención del mapa documental es revisar `CLAUDE.md` cuando v1.1 se integre en `main`.~~ **Corregido en el hotfix documental** (§23): la auditoría de Codex lo marcó como hallazgo medio, porque `CLAUDE.md` es el contexto de partida de los agentes y no puede describir un estado falso. Anotado en [`documentation-update-map.md`](documentation-update-map.md).
- Sin cambios en RF-01 a RF-29, rutas, Policies, permisos, `FormRequest`, FastAPI, `target_completion_at`, *checkpoint*, *freeze* ni umbral.

## 19. Resultados de pruebas

**Nuevas pruebas, solo para defectos reales corregidos:**

- `resources/js/components/visual-qa.test.tsx` — 6 pruebas de componente: token de la alerta destructiva, token del error de campo, relleno del enlace de salto, `main` en acceso, plegado de los códigos y `preferredScrollBehavior` con y sin movimiento reducido.
- `cypress/e2e/e2e-19-qa-visual-accesible.cy.js` — 7 pruebas en el navegador: sin desborde a 320 px en páginas públicas, `main` único en acceso, enlace de salto de 24 px o más, contraste de la alerta de rechazo en claro y oscuro, y contraste del error de campo y del botón destructivo en claro y oscuro.

**RED observado**: revertidas temporalmente las correcciones, fallaron **5 de 7** pruebas de Cypress (la alerta en oscuro y el par claro de error/botón ya cumplían antes) y **4 de 6** de componente (las dos restantes cubren archivos que no se revirtieron). Restauradas, pasan todas.

**Regresión final:**

| Suite | Resultado |
|---|---|
| Laravel | **408 pasadas + 8 omitidas** (igual que la línea base) |
| Python (`ml-service`) | **532 pasadas** |
| Componente (`vp test`) | **42 pasadas** (36 + 6 nuevas) |
| `tsc --noEmit` | Sin errores |
| `npm run build` | Correcto. `app-*.js` 204.31 kB / 59.93 kB gzip (+0.04 kB por `lib/motion.ts`); `app-*.css` **99.86 kB / 16.58 kB gzip** en la compilación de `1b3d27d` (la primera versión de este documento decía 99.82 / 16.57, medido antes de los últimos commits; corregido en el hotfix documental); `recruitment-scene-*.js` 2.51 kB / 1.26 kB gzip, sin cambios |
| Cypress (`cy:run`) | **20 specs / 84 pruebas, 84 pasadas** (19/77 + E2E-19 con 7) |
| `phase-18-overflow` | 5/5, **0 desbordes** a 1440, 1280, 768 y 390 px |
| `phase-21-responsive` (1024 y 320 px) | 7/7, **0 desbordes** |
| Auditoría del DOM | 0 hallazgos salvo los 27 objetivos por espaciado |
| Recorrido con Tab | 9/9 pantallas: la primera parada es «Saltar al contenido» (en `/login`, el campo de correo tiene el foco inicial y Tab pasa al siguiente control); **todas las paradas con indicador de foco visible**, ninguna invisible ni dentro de un contenedor oculto |
| `git diff --check` | Sin errores |

## 20. Capturas

[`phase-21-screenshots/`](phase-21-screenshots/), conjunto curado:

| Captura | Qué muestra |
|---|---|
| `01-portada-320` · `03-login-320` · `05-registro-1024` | Público a 320 y 1024 px, cabecera en dos filas a 320 |
| `02-empleos-oscuro-320` · `04-portada-oscuro-1024` | Oscuro en móvil y en el umbral de la escena |
| `06-salto-al-contenido` | Enlace de salto enfocado |
| `07-vacantes-320` · `08-expediente-oscuro-320` · `09-navegacion-movil-320` | Tabla, expediente y navegación móvil a 320 |
| `10-formulario-errores-320` | Errores de campo |
| `11-comparacion-1024` · `12-auditoria-oscuro-1024` | Comparación y auditoría |
| `13-seguridad-1024` · `14-seguridad-oscuro-1024` | Seguridad, antes nunca auditada |
| `15-sesion-evaluacion-390` · `16-vacio-oscuro-390` · `17-perfil-incompleto-390` | Evaluador, estado vacío, perfil incompleto |
| `18-destructivo-oscuro` | Botón destructivo con el rojo corregido |
| `19-portada-escena-1280` · `20-portada-reducido-oscuro-1280` | Escena 3D y póster con movimiento reducido |
| `21-panel-rrhh-1280` · `22-riesgo-operacional-oscuro-1280` | Panel y tarjeta de riesgo operacional |
| `23-apariencia-1280` · `24-dialogo-oscuro-1280` | Selector de tema y diálogo |
| `25-alerta-rechazo-1024` | La alerta de rechazo, legible (A4) |
| `2fa-02-plegado` · `2fa-05-desafio` | 2FA sin secretos a la vista |

## 21. Limitaciones

- **Sin lector de pantalla real** (§9) y sin `axe-core`: la auditoría del DOM cubre las reglas estructurales, no la experiencia de escucha.
- **Navegador sin interfaz**: las capturas son de Electron en el contenedor de Cypress, revisadas una por una. No hubo un navegador interactivo disponible para la revisión manual; la limitación queda registrada.
- **El contraste se mide en texto sobre fondo sólido.** Texto sobre imágenes o degradados se marca y se revisa a ojo; en la aplicación no hay casos relevantes.
- **Medición de rendimiento indicativa**: contenedor, no equipo modesto.
- El recorrido con Tab cubre 40 pulsaciones en nueve pantallas, no todas las rutas; el resto lo cubre la auditoría estática del DOM (§7).

## 22. Para la Fase 22

La interfaz queda cerrada para v1.1: sin defectos visuales de severidad media o alta conocidos. La Fase 22 (UML y PowerDesigner) **no se adelantó**: no hay diagramas nuevos ni cambios arquitectónicos. Lo que la Fase 22 debería tomar de aquí:

- los componentes de interfaz nuevos de v1.1 (`DataTable`, `Section`, capa `experience-3d/`, `lib/motion.ts`) existen en el código y, si el diagrama de componentes del frontend los incluye, deben salir del código real;
- la decisión pendiente sobre RNF-C, RF-28 y RF-29 (pregunta 13), que condiciona qué se marca como `<<propuesto v1.1>>`.

Para las Fases 24/25: lector de pantalla real, medición de rendimiento en un equipo modesto y LCP fuera del iframe de Cypress.

## 23. Hotfix documental (23/09/2026)

La auditoría de Codex dio la fase por **técnicamente en verde** (Laravel 408 + 8, Python 532, 42 pruebas de componente, `tsc`, *build*, Cypress 20 specs / 84, 0 desbordes, 2FA real, auditoría del DOM, teclado y barra lateral) y pidió corregir la documentación antes del cierre. Se corrigió **solo documentación y skills**, sin tocar código, pruebas ni dependencias:

| Hallazgo | Corrección |
|---|---|
| **MEDIUM-01** · `CLAUDE.md` describía como actuales `main` = `develop`, la Fase 13 vigente y ML y 3D sin implementar | `CLAUDE.md` separa `main`/v1.0 de `develop`/v1.1, lista el estado por fase (F21 sin integrar, F22 sin iniciar), documenta el ML experimental con su contrato congelado y el 3D con CSS 3D acotado. La skill `ml-risk-service` se actualizó igual |
| **LOW-01** · La skill 3D ponía «sin WebGL» como condición de *fallback*, como si la escena lo necesitara | La skill distingue la escena actual (CSS 3D, independiente de WebGL) de una escena WebGL futura hipotética |
| **LOW-02** · Cifra del CSS | 99.86 kB / 16.58 kB gzip (§19) |

También se anotaron, sin borrar historia, las entradas desactualizadas de `scope-preliminary.md` (RF-29 y preguntas 10 y 11) y se añadió a `PROGRESS.md` la tabla de estado de v1.1. RF-29 y RNF-C siguen siendo candidatos. **La Fase 21 no está cerrada** hasta que Codex reaudite este hotfix, y la Fase 22 no se inició.
