# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/cypress-e2e` (checkpoint parcial de Fase 9)

## Fases

| Fase | Estado |
|---|---|
| 0 a 7 | ✅ Completadas e integradas en `develop` |
| 8 — Frontend integral y validación en navegador | ✅ Integrada en `develop` (`6d47e46`, merge `--no-ff` de `ed11ecc`) |
| 9 — Suite E2E Cypress | 🟡 **En curso (checkpoint parcial, detenida por límite de sesión)** |
| 10 a 12 | ❌ Pendientes |

**RF-01 a RF-27 constituyen la línea base funcional completa.** Sin cambios de reglas de negocio en la Fase 9.

## Reglas de negocio vigentes de la Fase 6 (aprobadas; sin cambios)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras la decisión final, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 9 — estado exacto del checkpoint

### Paso 0 (completado)

- Punto de control verificado: rama `feature/frontend-integral`, commit `ed11ecc`, árbol limpio.
- Merge `--no-ff` en `develop` (`6d47e46`), sin conflictos y sin push.
- Verificación posterior: PHPUnit con 233 pruebas (225 passed, 8 skipped, 1045 assertions); `tsc` sin errores.
- Rama `feature/cypress-e2e` creada desde `develop`.

### Infraestructura creada (en el commit de checkpoint)

- **Restablecimiento de datos:**
  - Comando `php artisan e2e:reset` (`app/Console/Commands/E2eResetCommand.php`): ejecuta `migrate:fresh --seed`, vacía la cola y la caché, y rechaza la ejecución en producción.
  - Servicio `App\Services\Testing\E2eEnvironment`.
- **Endpoints de apoyo:**
  - `POST /__e2e/reset` y `GET /__e2e/queue`, fuera del grupo `web`.
  - Protegidos por el middleware `EnsureE2eSupportEnabled`: responden 404 si están desactivados o en producción, y 403 sin el token `X-E2E-Token`.
  - Configuración en `config/e2e.php`, con `E2E_ENABLED` y `E2E_TOKEN`. En `.env.example` quedan desactivados y sin token; el token solo existe en el `.env` local, no versionado.
- **Pruebas PHPUnit:**
  - `tests/Feature/Testing/E2eSupportTest.php`: RED con 5 failed y 2 passed; GREEN con **7 passed (19 assertions)**.
  - `phpunit.xml` fuerza `E2E_ENABLED=false`.
- **Cypress:**
  - `cypress.config.cjs`: `baseUrl` por configuración o `CYPRESS_baseUrl`, viewport de 1280×800, capturas solo en fallos, sin video, `testIsolation` activo y sin reintentos.
  - Token leído de `CYPRESS_E2E_TOKEN` o del `.env` local.
- **Soporte:** `cypress/support/commands.js` con los comandos `dataCy`, `resetDatabase`, `loginAs` (`cy.session`), `waitForQueue` (consulta el tamaño real de la cola), `appRequest` (con CSRF) e `idFromPath`.
- **Fixtures:** `users.json` (correos demo ficticios; la contraseña demo sale de la configuración), `demo.json` (IDs del `DemoSeeder`) y `cv-ficticio.pdf`.
- **npm:** scripts `e2e:reset`, `cy:run` (`docker compose --profile e2e run --rm cypress`) y `cy:open` (`npx cypress@15.3.0 open`).
- **Docker (ajuste mínimo):** el servicio `cypress` (`cypress/included:15.3.0`, Electron) ahora tiene:
  - un `entrypoint` que admite `--spec`;
  - la variable `CYPRESS_E2E_TOKEN: ${E2E_TOKEN:-}`;
  - dependencia de `queue`.
- **Frontend:** `data-status` en la fila de asignaciones del evaluador (`assessments/index.tsx`).
- **`.gitignore`:** agrega `cypress/results`; `cypress/screenshots` y `cypress/videos` ya estaban ignorados.

### Estado de los E2E

| Spec | Contenido | Estado real |
|---|---|---|
| `e2e-01-login.cy.js` | E2E-01: login de 5 roles y login inválido | ✅ Completo: 6/6 pasaron |
| `e2e-02-register-job-request.cy.js` | E2E-02, más un negativo de campos vacíos | ✅ Completo: 2/2 |
| `e2e-03-approve-job-request.cy.js` | E2E-03, más un rechazo sin motivo | ✅ Completo: 2/2 |
| `e2e-04-configure-publish-vacancy.cy.js` | E2E-04, más un negativo de ponderaciones distintas de 100 | 🟡 Parcial: el caso principal pasó; el negativo falló por un supuesto erróneo del test (el botón está deshabilitado, no oculto; **no es un defecto**). Ya está corregido, pero **no se verificó** |
| `e2e-05-candidate-apply.cy.js` | E2E-05 (incluye la notificación RF-11) | ✅ Completo: 1/1 |
| `e2e-06-shortlist-candidate.cy.js` | E2E-06, más un descarte sin motivo | 🟡 Escrito, sin resultado verificado |
| `e2e-07-evaluator-records-results.cy.js` | E2E-07 | 🟡 Escrito, sin resultado verificado |
| `e2e-08-comparison-ranking.cy.js` | E2E-08 | 🟡 Escrito, sin resultado verificado |
| `e2e-09-human-final-decision.cy.js` | E2E-09 | 🟡 Escrito, sin resultado verificado |
| `e2e-10-selection-and-closure.cy.js` | E2E-10 (incluye RF-26) | 🟡 Escrito, sin resultado verificado |
| `e2e-11-multitenancy.cy.js` | Aislamiento A/B: listados, auditoría e IDs ajenos | 🟡 Escrito, nunca ejecutado |
| `e2e-12-negative-rules.cy.js` | Rol sin permiso, vacante cerrada, decisión no autorizada, selección tras el cierre | 🟡 Escrito, nunca ejecutado |
| `e2e-13-full-recruitment-flow.cy.js` | Flujo integral de 12 pasos | 🟡 Escrito, nunca ejecutado |

### Pruebas ejecutadas (resultados reales)

- Primera ejecución de E2E-01 a E2E-05 (Electron, Docker): **5 specs, 13 tests, 12 passed, 1 failed, 1 min 34 s**. El fallo fue el negativo de E2E-04 descrito arriba.
- Quedó lanzada en segundo plano una ejecución de E2E-04 y E2E-06 a E2E-10, con log local en `cypress/results/run-04-10.log` (ignorado por Git). **Terminó con código de salida 1 (al menos un fallo o un error de build); el detalle no se revisó antes del checkpoint.**
- PHPUnit completo al inicio de la fase: 233 pruebas (225 passed, 8 skipped). Con `E2eSupportTest` debería llegar a 240, pero **la suite completa no se volvió a ejecutar**.
- `npm run build` se ejecutó al inicio de la última corrida en segundo plano, con resultado no revisado. `tsc`: no se volvió a ejecutar tras el cambio de `data-status`.

### Defectos

- Ningún defecto real nuevo en la Fase 9 hasta este punto.

## Git

- Rama: `feature/cypress-e2e`. Último commit: checkpoint parcial de la Fase 9 (ver `git log -1`).
- Sin push. No fusionar en `develop`.

## Siguiente paso exacto para reanudar

1. Confirmar que `.env` local tiene `E2E_ENABLED=true` y `E2E_TOKEN` (sin imprimirlo), y que `docker compose ps` muestra `app` healthy y `queue` en ejecución.
2. `docker compose exec app npm run build`
3. `npm run cy:run -- --spec "cypress/e2e/e2e-04-*.cy.js,cypress/e2e/e2e-0[6-9]-*.cy.js,cypress/e2e/e2e-10-*.cy.js"`, y corregir según resultados.
4. `npm run cy:run -- --spec "cypress/e2e/e2e-1[1-3]-*.cy.js"`, y corregir según resultados.
5. Suite completa `npm run cy:run` dos veces para comprobar estabilidad.
6. PHPUnit completo, `npm run build`, `npx tsc --noEmit`.
7. Crear `docs/testing/cypress-e2e.md` y actualizar `rf-implementation-matrix.md` (y `defects.md` si aparecen defectos).
8. Commit final de la Fase 9 sin push y reporte de 27 puntos. No avanzar a la Fase 10.
