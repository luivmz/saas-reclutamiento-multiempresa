# Suite E2E con Cypress (Fase 9)

Suite formal, versionada y reproducible de pruebas end-to-end. **Complementa** a PHPUnit (unitarias, feature, autorización y aislamiento multiempresa) y no lo reemplaza.

## 1. Versión y navegador

| Elemento | Valor |
|---|---|
| Cypress | **15.3.0** (imagen oficial `cypress/included:15.3.0`) |
| Navegador | **Electron 136 (headless)** |
| Ejecución | Servicio `cypress` de Docker Compose (perfil `e2e`) contra el entorno aislado `http://app-e2e:8000` (desde la Fase 10; ver `docs/docker.md`) |
| Reintentos | Ninguno (`retries: 0`): un fallo intermitente se investiga, no se oculta |
| Aislamiento | `testIsolation: true` (cookies y almacenamiento limpios entre tests) |
| Evidencia | Capturas solo en fallos (`cypress/screenshots`, ignorado por Git); sin video |
| Viewport | 1280×800 |

## 2. Instalación y configuración

No se agregan dependencias npm a la aplicación: Cypress se ejecuta desde su imagen oficial.

| Archivo | Propósito |
|---|---|
| `cypress.config.cjs` | Configuración. `baseUrl` por defecto `http://localhost:8001` (`app-e2e` publicado en el host), sobrescrita por `CYPRESS_baseUrl=http://app-e2e:8000` en Docker. El token se lee de `CYPRESS_E2E_TOKEN` o `E2E_TOKEN` (inyectado desde `.env.e2e`) o, para `cypress open` en el host, desde `.env.e2e`. Zona horaria de fechas: `APP_TIMEZONE=America/Lima`. |
| `docker-compose.yml` → servicios `app-e2e`, `queue-e2e`, `cypress` (perfil `e2e`) | Entorno aislado con `APP_ENV=e2e`. `cypress` usa la imagen fijada, `entrypoint` `cypress run --browser electron` (admite `--spec`), `env_file: .env.e2e` y depende de `app-e2e` y `queue-e2e` (healthy). |
| `package.json` | Scripts `e2e:setup`, `e2e:up`, `e2e:reset`, `cy:run` y `cy:open`. |
| `config/e2e.php` | `E2E_ENABLED` (por defecto `false`), `E2E_TOKEN` y `E2E_DATABASE` (por defecto `reclutamiento_e2e`). |

### Variables necesarias (solo en `.env.e2e`, nunca versionado)

`npm run e2e:setup` crea `.env.e2e` desde `.env.e2e.example` con `APP_KEY` y `E2E_TOKEN` aleatorios, sin mostrarlos:

```dotenv
APP_ENV=e2e
DB_DATABASE=reclutamiento_e2e
E2E_ENABLED=true
E2E_TOKEN=<generado>
E2E_DATABASE=reclutamiento_e2e
```

El entorno normal (`.env`) mantiene `E2E_ENABLED=false`, por lo que ahí los endpoints responden 404. La contraseña de los usuarios demo (`password`, ficticia, ver `docs/demo-users.md`) está en la configuración de Cypress como `DEMO_PASSWORD`.

## 3. Preparación y reset de datos

Cada spec empieza desde un **estado conocido** que genera `DemoSeeder` (`docs/demo-users.md`), en la base aislada `reclutamiento_e2e`.

- **`php artisan e2e:reset`** (`npm run e2e:reset`) ejecuta `migrate:fresh --seed`, vacía la cola y limpia la caché (incluidos los contadores de intentos de login). En producción se niega a ejecutarse.
- **`POST /__e2e/reset`** es el mismo reset expuesto para Cypress (`cy.resetDatabase()`).
- **`GET /__e2e/queue`** devuelve los trabajos pendientes en la cola, para `cy.waitForQueue()`.

Seguridad de los endpoints (`EnsureE2eSupportEnabled` y `E2eEnvironment`, cubiertas por `tests/Feature/Testing/E2eSupportTest.php` y `E2eEnvironmentTest.php`, 11 pruebas):

- Responden **404** si `E2E_ENABLED` está desactivado o el entorno es producción.
- Responden **403** sin cabecera `X-E2E-Token` o con un token incorrecto (comparación con `hash_equals`).
- El reset responde **409** (o el comando falla, o el servicio lanza una excepción) si la base activa no es exactamente `E2E_DATABASE` (DEF-13).
- Se registran fuera del grupo `web`, por lo que no usan sesión ni CSRF.

Desde la Fase 10 el reset **ya no afecta** la base de desarrollo y demostración (`reclutamiento`): la suite usa `app-e2e` con `reclutamiento_e2e` y bases Redis propias (DB 2 y 3).

### Colas y notificaciones

Las notificaciones son `ShouldQueue` y las procesa el servicio `queue-e2e` (worker Redis del entorno aislado), del que depende el servicio `cypress`. Antes de afirmar sobre notificaciones, los specs llaman a `cy.waitForQueue()`. Este comando consulta el tamaño real de la cola cada 250 ms, hasta 40 veces, y falla con un mensaje explícito si no se vacía. No hay esperas fijas.

## 4. Estructura

```text
cypress.config.cjs
cypress/
├── e2e/                      14 specs (*.cy.js): e2e-00 de soporte y E2E-01 a E2E-13
├── fixtures/
│   ├── users.json            correos de usuarios demo por rol (ficticios)
│   ├── demo.json             IDs y nombres que genera DemoSeeder
│   └── cv-ficticio.pdf       CV PDF ficticio para la carga
└── support/
    ├── e2e.js
    ├── commands.js           comandos personalizados
    └── dates.js              appDate(): fechas en la zona horaria de la aplicación (DEF-12)
```

Comandos personalizados (solo los que evitan duplicación):

| Comando | Uso |
|---|---|
| `cy.dataCy(name)` | Selecciona por `data-cy` |
| `cy.resetDatabase()` | Reset al estado conocido |
| `cy.loginAs(role)` | Login real por formulario, una vez por rol, con `cy.session` |
| `cy.waitForQueue()` | Espera por estado real de la cola |
| `cy.appRequest(method, url, body)` | Petición autenticada con CSRF y `Accept: application/json`, para los negativos |
| `cy.idFromPath(regex)` | Obtiene el ID de la URL tras una redirección |

Reglas seguidas:
- Solo selectores `data-cy` o atributos de datos (`data-kind`, `data-status`, `data-action`, `data-position`).
- Sin clases de Tailwind y sin `cy.wait` arbitrarios.
- Se espera a URL, elementos visibles, estado de la interfaz y cola vacía.

## 5. Specs y propósito

| ID | Spec | Propósito | RF | Tests |
|---|---|---|---|---|
| Soporte | `e2e-00-app-dates.cy.js` | Verifica `appDate()`: con un instante fijo de las 21:30 en Lima (ya día siguiente en UTC), las fechas usadas por los specs siguen `America/Lima`. No accede a la aplicación. | DEF-12 | 3 |
| E2E-01 | `e2e-01-login.cy.js` | Login real de los 5 roles, con menú visible y oculto según el rol. Negativo: credenciales inválidas. | RF-08 y roles | 6 |
| E2E-02 | `e2e-02-register-job-request.cy.js` | El área solicitante registra y envía un requerimiento. Negativo: formulario vacío que no crea registros. | RF-01, RF-02 | 2 |
| E2E-03 | `e2e-03-approve-job-request.cy.js` | El aprobador aprueba un requerimiento validado. Negativo: rechazo sin motivo. | RF-03, RF-04 | 2 |
| E2E-04 | `e2e-04-configure-publish-vacancy.cy.js` | RR. HH. genera la vacante desde un requerimiento aprobado, la valida y la publica, y la vacante aparece en el portal. Negativo: ponderaciones que no suman 100, botón deshabilitado y publicación directa rechazada (422). | RF-05 a RF-07, RF-20 | 2 |
| E2E-05 | `e2e-05-candidate-apply.cy.js` | El postulante completa su perfil, carga su CV, postula y recibe la confirmación. | RF-08 a RF-11 | 1 |
| E2E-06 | `e2e-06-shortlist-candidate.cy.js` | RR. HH. revisa y preselecciona, y el postulante es notificado. Negativo: descarte sin motivo. | RF-12 a RF-15 | 2 |
| E2E-07 | `e2e-07-evaluator-records-results.cy.js` | El evaluador registra puntajes; un puntaje fuera de rango no se envía. | RF-19, RF-20 | 1 |
| E2E-08 | `e2e-08-comparison-ranking.cy.js` | RR. HH. consulta el ranking ponderado (orden, totales 85.5 / 83.5 / 68.5, fórmula y aviso). **El ranking no selecciona:** no hay decisión, RR. HH. no puede decidir y nadie queda como «Seleccionado». | RF-21, RF-22 | 1 |
| E2E-09 | `e2e-09-human-final-decision.cy.js` | La decisión exige justificación y confirmación humana. El aprobador elige al **segundo** del ranking y los estados de las postulaciones no cambian. | RF-23 | 2 |
| E2E-10 | `e2e-10-selection-and-closure.cy.js` | Tras la decisión humana, RR. HH. registra la selección y cierra la convocatoria. Los demás quedan como «No seleccionado» y cada candidato recibe su propio resultado. | RF-24 a RF-26 | 1 |
| E2E-11 | `e2e-11-multitenancy.cy.js` | La organización B no ve ni accede a vacantes, postulaciones ni requerimientos de A, y viceversa. La auditoría no se cruza. Las acciones sobre IDs ajenos se rechazan (403/404) sin efectos. | Multiempresa, RF-27 | 4 |
| E2E-12 | `e2e-12-negative-rules.cy.js` | Rol sin permiso (403); postulación a vacante cerrada (404 en el portal, 422 al postular); decisión por RR. HH. o evaluador (403); selección y cierre después del cierre (422). | RF-10, RF-23 a RF-25 | 4 |
| E2E-13 | `e2e-13-full-recruitment-flow.cy.js` | Flujo integral: requerimiento → aprobación → vacante → publicación → postulación → preselección → evaluación → entrevista → ranking (sin decisión automática) → decisión humana → selección → cierre → notificación → auditoría. | RF-01 a RF-27 | 12 |

**Total: 14 specs y 43 tests** desde la Fase 10 (en la Fase 9 eran 13 specs y 40 tests, sin `e2e-00`).

### Decisiones de diseño

- **Reset por spec o por test.** Los specs que modifican datos seedeados hacen reset en `beforeEach`. Los de solo lectura, o con tests que no interfieren entre sí (E2E-01, E2E-08, E2E-11, E2E-12), lo hacen una vez en `before`.
- **E2E-13 en un único spec ordenado.** El proceso es secuencial por naturaleza: cada `it` es un traspaso entre roles y pasa IDs al siguiente. Dividirlo duplicaría toda la preparación. Se acepta que un fallo detenga los pasos siguientes, porque el fallo indica exactamente dónde se rompió el flujo.
- **Multiempresa.** La cobertura principal sigue en PHPUnit (`CrossTenantAccessTest`, `OrganizationScopeTest`). E2E-11 solo verifica los casos más visibles de extremo a extremo.
- **Negativos.** Se usan peticiones HTTP autenticadas (`cy.appRequest`) para comprobar el rechazo del servidor y la interfaz para comprobar que la acción no se ofrece. Las matrices exhaustivas de autorización siguen en PHPUnit.

## 6. Comandos

```powershell
# Requisito: Docker Desktop en ejecución. cy:run crea .env.e2e si falta y levanta app-e2e y queue-e2e.
npm run cy:run                              # suite completa (headless, Electron, en Docker)
npm run cy:run -- --spec "cypress/e2e/e2e-10-*.cy.js"   # un spec
npm run e2e:setup                           # solo crear .env.e2e (APP_KEY y E2E_TOKEN aleatorios)
npm run e2e:up                              # solo levantar app-e2e y queue-e2e
npm run e2e:reset                           # reset manual de la base E2E (reclutamiento_e2e)
npm run cy:open                             # Cypress interactivo en el host (npx cypress@15.3.0)
```

Sin npm en el host: `docker compose run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh` y luego `docker compose --profile e2e run --rm cypress`.

Para `cy:open`, el host necesita Node y descarga el binario de Cypress la primera vez. Apunta a `http://localhost:8001` (`app-e2e`) y lee el token desde `.env.e2e`. **`cy:open` no se ejecutó durante la Fase 9** (solo se usó `cy:run` en Docker).

## 7. Resultados reales

### Ejecuciones durante el desarrollo

| Ejecución | Specs | Tests | Passed | Failed | Causa y corrección |
|---|---|---|---|---|---|
| E2E-01 a E2E-05 | 5 | 13 | 12 | 1 | E2E-04, negativo: el test esperaba que el botón «Publicar» no existiera. La aplicación lo muestra **deshabilitado** (`disabled` si la validación falla), lo que es correcto. El test ahora afirma `be.disabled` y además verifica que el servidor rechaza la publicación directa (422). |
| E2E-04, E2E-06 a E2E-10 | 6 | 9 | 8 | 1 | E2E-10: el test buscaba el texto «no seleccionado» en la notificación. El texto real de RF-26 es «…en esta oportunidad **no ha sido seleccionado(a)**». Se corrigió la aserción; la aplicación es correcta. |
| E2E-10 (reejecución) | 1 | 1 | 1 | 0 | — |
| E2E-11 a E2E-13 | 3 | 20 | 20 | 0 | — |

### Suite completa: primera corrida

Cypress 15.3.0 · Electron 136 (headless) · **13 specs · 40 tests · 40 passed · 0 failed · 0 pending · 0 skipped · 04:01**

### Suite completa: segunda corrida (estabilidad)

Cypress 15.3.0 · Electron 136 (headless) · **13 specs · 40 tests · 40 passed · 0 failed · 0 pending · 0 skipped · 03:56**

| Spec | Tests | 1.ª corrida | 2.ª corrida |
|---|---|---|---|
| e2e-01-login | 6 | 6/6 · 00:15 | 6/6 · 00:15 |
| e2e-02-register-job-request | 2 | 2/2 · 00:19 | 2/2 · 00:18 |
| e2e-03-approve-job-request | 2 | 2/2 · 00:15 | 2/2 · 00:15 |
| e2e-04-configure-publish-vacancy | 2 | 2/2 · 00:23 | 2/2 · 00:21 |
| e2e-05-candidate-apply | 1 | 1/1 · 00:12 | 1/1 · 00:12 |
| e2e-06-shortlist-candidate | 2 | 2/2 · 00:18 | 2/2 · 00:18 |
| e2e-07-evaluator-records-results | 1 | 1/1 · 00:10 | 1/1 · 00:09 |
| e2e-08-comparison-ranking | 1 | 1/1 · 00:08 | 1/1 · 00:08 |
| e2e-09-human-final-decision | 2 | 2/2 · 00:15 | 2/2 · 00:15 |
| e2e-10-selection-and-closure | 1 | 1/1 · 00:17 | 1/1 · 00:17 |
| e2e-11-multitenancy | 4 | 4/4 · 00:17 | 4/4 · 00:17 |
| e2e-12-negative-rules | 4 | 4/4 · 00:21 | 4/4 · 00:20 |
| e2e-13-full-recruitment-flow | 12 | 12/12 · 00:46 | 12/12 · 00:46 |

Las dos corridas completas pasaron sin reintentos: no se observó flakiness.

### Fase 10: entorno E2E aislado

| Corrida | Entorno | Specs | Tests | Passed | Failed | Skipped | Duración |
|---|---|---|---|---|---|---|---|
| Instalación limpia | Clon nuevo del repositorio, volúmenes nuevos (`-p reclutamiento-clean`) | 14 | 43 | 43 | 0 | 0 | 03:26 |
| Entorno principal | `app-e2e` y `queue-e2e` junto al entorno de desarrollo | 14 | 43 | 43 | 0 | 0 | 03:34 |

Ambas corridas usaron Cypress 15.3.0 y Electron 136 headless, sin reintentos.

**QA final (Fase 12, 2026-09-13):** suite completa en el entorno principal: 14 specs · 43/43 · 0 failed · 0 skipped · 03:32 · Electron 136. `e2e-00-app-dates` (3 tests) se agregó en esta fase.

**Aislamiento verificado con datos:**
- En la instalación limpia, la base de desarrollo conservó el seed intacto (11 requerimientos, 5 vacantes) mientras la E2E recibió los datos de las pruebas.
- En el entorno principal, la base de desarrollo tenía 12 requerimientos, 6 vacantes y 16 usuarios antes de la suite y los mismos valores después.

### Defectos

- **Defectos reales de la aplicación encontrados por la suite: ninguno.**
- **Tests corregidos por expectativas erróneas:** E2E-04 (negativo) y E2E-10 (texto de RF-26), descritos arriba.
- **Ajuste de diseño antes de la primera ejecución:** el negativo de E2E-02 dependía del texto del mensaje de validación y se cambió por una verificación de estado (el número de requerimientos no cambia).
- **Soporte agregado a la interfaz:** atributo `data-status` en la fila de asignaciones del evaluador (`assessments/index.tsx`), para seleccionar sesiones programadas sin depender de textos.

## 8. Limitaciones conocidas

- **Resueltas en la Fase 10:**
  - La base compartida con desarrollo (DEF-13): ahora hay entorno aislado `app-e2e` con `reclutamiento_e2e`.
  - Las fechas en UTC (DEF-12): ahora se usa `appDate()` en `America/Lima`.
- **Almacenamiento compartido:** los CV que se cargan en las pruebas se guardan en el mismo `storage/app/private` que el entorno normal (nombres UUID, sin colisiones), y el reset no los borra (A-35).
- **Un solo navegador:** solo se ejecutó Electron 136; Chrome, Firefox y Edge no se probaron.
- **Worker obligatorio:** las aserciones de notificaciones requieren `queue-e2e` en ejecución (dependencia declarada del servicio `cypress`).
- **Rango de puntajes:** en E2E-07 lo impide la validación nativa del navegador (`max`). El rechazo en el servidor está cubierto por PHPUnit (`ScoreSheetValidatorTest`).
- **Duración:** cada reset tarda unos 6 s, por lo que la suite completa dura unos 4 min en serie.
- **Ruido en logs:** los mensajes `dbus` de Electron dentro del contenedor no afectan los resultados.
- **Alcance:** sin métricas de cobertura E2E ni integración continua (fuera del alcance de la Fase 9).
