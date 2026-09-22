# Fase 18 — Rediseño frontend integral

**Fecha:** 21 de septiembre de 2026
**Rama:** `feature/phase-18-frontend-redesign` · **Base:** `0d2ce42` (cierre de la Fase 17)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **exclusivamente de interfaz**. No cambia reglas de negocio, rutas, contratos de API, modelos, Policies, el servicio ML ni ninguna decisión científica de las Fases 14 a 17. RF-01 a RF-27 conservan su número y su significado; RF-29 sigue siendo experimental y la decisión final sigue siendo humana (RF-23).

---

## 1. Objetivo

La aplicación funcionaba y estaba probada, pero se veía como lo que era: el kit de inicio de Laravel con pantallas añadidas encima. El objetivo de esta fase es darle una identidad propia, coherente con lo que el producto hace, y cerrar la deuda visual y de accesibilidad acumulada en trece fases de trabajo funcional.

El criterio de diseño es uno solo y se deriva del dominio: **el producto es un expediente**. Un requerimiento avanza por etapas, deja rastro de quién hizo qué y cuándo, y termina en una decisión que firma una persona. Todo lo demás —tipografía, color, estructura— se subordina a eso.

## 2. Auditoría visual previa

Inventario de lo que se encontró antes de tocar nada (111 archivos `.tsx` en `resources/js`):

| Hallazgo | Dónde | Consecuencia |
|---|---|---|
| Tokens de color del kit de inicio, escala de grises pura | `resources/css/app.css` | Ninguna identidad; `--destructive-foreground` era idéntico a `--destructive` |
| Módulo de configuración íntegramente en inglés | `layouts/settings/`, `pages/settings/`, `delete-user`, passkeys, 2FA | Parecía otra aplicación |
| La misma tabla copiada cinco veces | requerimientos, vacantes, postulaciones, auditoría, ranking | Sin `scope="col"`, sin `<caption>`, y en móvil solo arrastre horizontal |
| `StatusBadge` con colores sueltos de Tailwind | `components/status-badge.tsx` | El mismo estado podía verse distinto según el módulo |
| `tabIndex` positivos (1…6) | `auth/login`, `auth/register` | Rompen el orden natural del foco |
| Sin enlace de salto al contenido | todos los *layouts* | Diez enlaces de barra lateral antes de llegar a la tabla, en cada página |
| Sin indicación de página actual salvo por color | `nav-main`, `filter-chips`, `pagination` | Invisible para un lector de pantalla |
| Cambio de tema solo dentro de Configuración | `settings/appearance` | Inalcanzable desde donde se trabaja |
| Código muerto del kit de inicio | 5 archivos | Deuda visual que nadie mantenía |
| Cadenas unidas con punto medio (`A · B · C`) | vacantes, postulaciones, evaluaciones | Ilegible y sin estructura |

## 3. Sistema de diseño

### Tipografía

Superfamilia **IBM Plex**, servida desde el propio dominio (se descarga en el *build*, no en tiempo de ejecución):

| Rol | Familia | Pesos |
|---|---|---|
| Títulos de página y de sección | IBM Plex Serif | 600 |
| Interfaz y cuerpo | IBM Plex Sans | 400, 500, 600 |
| Códigos, fechas y cifras comparables | IBM Plex Mono | 400, 500 |

La elección no es estética por sí sola: un sistema de expedientes se lee mejor con una familia de documento, y el mono separa de un vistazo lo que es identificador (`REQ-2026-0042`) de lo que es prosa.

### Color

Seis tonos de estado (`--tone-*`), cada uno con fondo, texto y borde, definidos una vez en `resources/css/app.css` y usados por todos los componentes. La marca es un **petróleo institucional** que funciona además como tono «en curso»: reutilizarlo es deliberado.

La barra lateral es oscura también en modo claro. El contenido queda como una hoja apoyada sobre un escritorio, lo que separa el marco de navegación del expediente que se está leyendo.

### Componentes reutilizables nuevos

| Componente | Sustituye a |
|---|---|
| `components/data-table.tsx` | Cinco tablas copiadas. Encabezado fijo, `<caption>`, semántica accesible declarada y apilado en ficha por debajo de 768 px, con un solo DOM (ver §4) |
| `components/page.tsx` → `Section` | La repetición de `Card + CardHeader + CardTitle` en cada módulo; fija el nivel `h2` |
| `components/choice.tsx` | Los `<input type="radio">` sueltos y con estilo distinto en cada formulario de decisión |
| `components/skip-link.tsx` | No existía |
| `components/appearance-toggle.tsx` | El tema solo era alcanzable desde Configuración |

## 4. Accesibilidad

Correcciones aplicadas, referidas a WCAG 2.2:

| Criterio | Corrección |
|---|---|
| 1.3.1 Información y relaciones | `<caption>`, `scope="col"`, roles explícitos y relación `headers`/`id` en todas las tablas (ver más abajo); `dt`/`dd` reales en los resúmenes; `fieldset`/`legend` en los formularios de decisión y de puntajes |
| 2.4.1 Evitar bloques | Enlace «Saltar al contenido» en el *shell* y en el sitio público |
| 2.4.3 Orden del foco | Eliminados todos los `tabIndex` positivos, y el conmutador de visibilidad de la contraseña deja de estar excluido con `tabIndex={-1}`: ahora se alcanza con Tab y se activa con Enter o Espacio |
| 2.4.7 Foco visible | Un único anillo de foco (`:focus-visible`) definido en la capa base, visible sobre fondo claro y sobre la barra lateral oscura |
| 1.4.1 Uso del color | La opción elegida cambia de color **y** de grosor de borde; los badges de estado llevan un punto además del fondo; la página actual se marca con `aria-current` |
| 4.1.2 Nombre, rol, valor | `aria-pressed` en los filtros de estado y en las pestañas de tema de Configuración; `menuitemradio` con `aria-checked` en el selector de tema de la barra superior, que es un grupo de opciones excluyentes; `aria-current="page"` en navegación y paginación; `aria-describedby` y `aria-invalid` conectados automáticamente por `FormField` |
| 3.3.1 Identificación de errores | `role="alert"` en los mensajes de campo |
| 2.3.3 Animación por interacción | `prefers-reduced-motion` respetado globalmente |

### La tabla sigue siendo una tabla en móvil

Apilar una fila como ficha exige `display: block` y `display: flex` sobre `tbody`, `tr` y `td`, y cambiar el `display` de los elementos de una tabla **destruye sus roles implícitos**: el navegador deja de exponerla como tabla. Ocultar además el encabezado con `display: none` lo borraría del árbol de accesibilidad. Por eso `DataTable`:

- declara los roles a mano (`table`, `rowgroup`, `row`, `columnheader`, `cell`), que en escritorio solo repiten lo nativo y en móvil lo restituyen;
- recorta el encabezado visualmente en vez de ocultarlo, de modo que sigue existiendo;
- asocia cada celda con su columna mediante `headers`/`id`, una relación explícita que no depende del algoritmo nativo de tablas;
- muestra la etiqueta de cada valor como texto real —no como contenido generado por CSS— y la marca `aria-hidden`, porque la relación `headers` ya entrega ese dato y repetirlo haría que se oyera el encabezado dos veces.

Todo ello con **un solo DOM**: las filas son los mismos elementos, con los mismos `data-cy`, en cualquier ancho.

Nada de esto se declara como auditoría de accesibilidad completa, ni como prueba con lector de pantalla real: es la corrección de los defectos encontrados en la revisión de código de esta fase, verificada sobre el DOM y los estilos calculados.

## 5. Responsive

Verificado con una prueba real, no a ojo. `cypress/visual/phase-18-overflow.cy.js` recorre **24 páginas en 1440, 1280, 768 y 390 px** y falla si `scrollWidth` supera a `clientWidth`. Resultado: **sin desbordamiento horizontal en ninguna combinación**.

Tres defectos reales salieron de ahí y se corrigieron:

1. la barra pública no admitía sus tres acciones a 390 px (etiqueta abreviada en pantallas angostas);
2. la ficha del expediente de la portada forzaba dos columnas sin permitir salto;
3. los detalles de tres columnas no dejaban encoger la columna ancha (faltaba `min-w-0` en los ítems de *grid*), de modo que la tabla de criterios empujaba la página.

## 6. Evidencia visual

Capturas reales tomadas con la aplicación corriendo en el entorno E2E aislado, por rol y por ancho, en `docs/v1.1/phase-18-screenshots/`:

| Captura | Qué muestra |
|---|---|
| `01-portada-desktop.png` | Portada pública: el expediente como argumento |
| `04-login-desktop.png` | Acceso, con el panel institucional |
| `06-panel-rrhh-desktop.png` | Panel de RR. HH. |
| `09-vacantes-desktop.png` | Listado con el nuevo `DataTable` |
| `11-vacante-publicada-desktop.png` | Detalle de vacante con el panel de riesgo operacional |
| `15-comparacion-ranking-desktop.png` | Ranking ponderado y explicable (RF-21, RF-22) |
| `07-requerimientos-movil.png` | La misma tabla apilada en ficha a 390 px |
| `24-vacantes-oscuro-1280.png` | Modo oscuro |

Las especificaciones de captura y de desbordamiento viven en `cypress/visual/` y **no forman parte de la suite E2E**: `specPattern` solo recoge `cypress/e2e/**`. La comprobación de semántica accesible de la tabla en móvil sí forma parte de la suite, en `cypress/e2e/e2e-16-tabla-accesible-movil.cy.js`. Para ejecutar las de `cypress/visual/`:

```
npm run e2e:setup
docker compose --profile e2e run --rm cypress \
  --spec "cypress/visual/phase-18-overflow.cy.js" \
  --config "specPattern=cypress/visual/**/*.cy.js"
```

## 7. RF-29 en la interfaz

El panel de riesgo operacional se rediseñó **sin tocar su lógica ni su contrato**. Lo que cambió:

- la cifra usa el tono informativo, nunca el de peligro: con una tasa de alerta del 73.5 % en el conjunto de prueba, pintarla de rojo sería desproporcionado;
- mientras se consulta se muestra un esqueleto y la región es `aria-live`, en lugar de un «Consultando…» que el lector de pantalla no anunciaba;
- se conservan literalmente los textos que las pruebas E2E verifican: «Experimental», «Riesgo operacional del proceso», «no sobre las personas postulantes» y «decisión final corresponde al Aprobador».

Sigue sin ordenar candidatos, sin puntuar personas, sin recomendar y sin disparar ninguna acción.

## 8. Alcance ampliado, declarado

Dos cosas se hicieron por encima del enunciado literal y se declaran aquí:

1. **Traducción del módulo de configuración al español** (perfil, seguridad, apariencia, eliminación de cuenta, claves de acceso y verificación en dos pasos). Era la única zona en inglés; rediseñarla sin traducirla habría dejado la incoherencia más visible que antes.
2. **Eliminación de cinco archivos muertos del kit de inicio**: `components/app-header.tsx`, `components/heading.tsx`, `layouts/app/app-header-layout.tsx`, `layouts/auth/auth-card-layout.tsx` y `layouts/auth/auth-split-layout.tsx`. Ninguno era alcanzable desde ninguna ruta y todos llevaban estilos fuera del sistema nuevo.

## 9. Regresión

Ejecutada de verdad, sobre el código final de la rama:

| Suite | Resultado |
|---|---|
| `php artisan test` | **408 pasadas, 8 omitidas** (las omitidas son las de verificación de correo de Fortify, deshabilitada en `tests/TestCase.php`) |
| `pytest` (ml-service) | **532 pasadas** |
| `npx tsc --noEmit` | sin errores |
| `npm run build` | correcto |
| `npm run cy:run` | **17 specs, 61 pruebas, 61 pasadas** |
| `npx vp test --run` | **18 pruebas de componente, 18 pasadas** |
| `vp fmt --check` y `vp lint` sobre los archivos de la fase | 0 advertencias, 0 errores |
| `git diff --check` | limpio |
| `php artisan route:list` | sin cambios |

### Lo que no está verde y no lo dejó esta fase

`./vendor/bin/pint --test` reporta cuatro archivos con problemas de formato: `database/seeders/DemoSeeder.php`, `routes/web.php`, `tests/Feature/Audit/AuditLoggerTest.php` y `tests/Feature/Tenancy/CrossTenantAccessTest.php`. **Ninguno está en el diff de esta fase** (la Fase 18 toca un solo archivo PHP, `resources/views/app.blade.php`, que Pint acepta). Lo mismo ocurre con `npm run check` sobre el repositorio completo: señala 152 archivos, la mayoría documentos Markdown y código anterior nunca formateado. Corregirlos sería salir del alcance declarado; queda anotado para que el equipo decida.

## 10. Invariantes preservados

- RF-01 a RF-27 sin renumerar ni reinterpretar.
- Ninguna decisión automática: el ranking calcula, ordena y compara; la decisión la registra una persona con justificación (RF-23 a RF-25).
- Multiempresa, Policies, roles y pruebas cross-tenant intactos: no se tocó ningún controlador, modelo, Policy ni migración.
- Auditoría de solo inserción intacta.
- Solo datos ficticios en capturas y en textos de ejemplo.
- Sin secretos versionados.
- `v1.0.0-academic` (`9a946c2`) intacto.
- Sin `push`, `merge`, *tag* ni *release*.
- Todos los `data-cy` conservados; ninguna prueba E2E modificada.

## 11. Fuera de alcance

No se hizo, por corresponder a fases posteriores o a decisiones no aprobadas: animaciones avanzadas (Fase 19), 3D (Fase 20), cambios de lógica de negocio, de rutas, de contratos de API o del servicio ML, y nuevas dependencias de producción.

## 12. Correcciones posteriores a la auditoría de Codex

| Hallazgo | Corrección |
|---|---|
| MEDIUM · `DataTable` perdía la semántica de tabla en móvil | Roles declarados, encabezado recortado en vez de oculto, relación `headers`/`id` por celda y etiqueta como texto real (§4). Verificado en las cinco tablas migradas por `cypress/e2e/e2e-16-tabla-accesible-movil.cy.js` y por pruebas de componente |
| LOW · `FormField` sustituía el `aria-describedby` del control | Ahora combina el propio del control, el de la ayuda y el del error, sin repetir y en ese orden; un error fuerza `aria-invalid="true"` aunque el llamador pase `false` |
| LOW heredado · el conmutador de contraseña estaba fuera del orden de tabulación | `tabIndex={-1}` eliminado; se alcanza con Tab, se activa con Enter o Espacio, hereda el foco visible global y declara `aria-controls` |
| LOW · salto de encabezados en el panel de evaluaciones | `h4` pasa a `h3` bajo el `h2` de la sección; la jerarquía queda h1 → h2 → h3 en toda la aplicación |
| LOW · la documentación atribuía `aria-pressed` al selector de tema | El selector de la barra superior pasa a `menuitemradio` con `aria-checked`, que es el rol correcto para opciones excluyentes, y la tabla de §4 distingue ahora los dos controles |

Pruebas añadidas por estas correcciones: 18 de componente (`vp test`, con `react-dom/server`, sin dependencias nuevas) y 6 de navegador (`e2e-16`). La línea base de Cypress pasa de 16 specs / 55 pruebas a **17 specs / 61 pruebas**.
