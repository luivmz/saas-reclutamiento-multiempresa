# Capítulo 8. Desarrollo

El desarrollo se organizó en fases de trabajo, cada una en una rama `feature/*` fusionada en `develop` con `--no-ff`. Para el informe se agrupan en **9 iteraciones**. Hashes, cifras y defectos provienen de Git, `docs/tdd-evidence.md`, `docs/defects.md` y `docs/PROGRESS.md`.

La Fase 0 (inspección y plan) no generó commits: su resultado es `docs/implementation-plan.md`.

## Resumen

| Iteración | Fase(s) | Rama | Commits → merge en `develop` | RF | PHPUnit al cierre |
|---|---|---|---|---|---|
| 1. Bootstrap + auth + multiempresa | 1–2 | `main`, `feature/tenancy-roles` | `e87ef39` (bootstrap en `main`), `3c28f28` → `d696032` | Base (RF-08 parcial) | 31 passed, 8 skipped (fase) |
| 2. Requerimientos + vacantes | 3 | `feature/job-requests-vacancies` | `7ccb619` → `5ab6e22` | RF-01 a RF-07 | 91 passed, 8 skipped |
| 3. Postulantes + postulaciones | 4 | `feature/candidates-applications` | `215cdbe` → `f20f0b6` | RF-08 a RF-15 | 129 passed, 8 skipped |
| 4. Evaluaciones + entrevistas | 5 | `feature/evaluations-interviews` | `3e66623` (RED), `06cf5c4` → `40eda7d` | RF-16 a RF-19 | 152 passed, 8 skipped (532 assertions) |
| 5. Ranking + selección + cierre | 6 | `feature/ranking-selection-closure` | `7a65bee` → `dda4bd0` | RF-20 a RF-25 | 211: 203 passed, 8 skipped (779) |
| 6. Notificaciones + auditoría | 7 | `feature/notifications-audit` | `9de66ce` → `cd092d1` | RF-26, RF-27 | 230: 222 passed, 8 skipped (1017) |
| 7. Frontend integral | 8 | `feature/frontend-integral` | `ed11ecc` → `6d47e46` | Validación de RF-01 a RF-27 en la interfaz | 233: 225 passed, 8 skipped (1045) |
| 8. Cypress E2E | 9 | `feature/cypress-e2e` | `9edb0cd`, `a77c916` → `e0c8825` | Automatización E2E | 240: 232 passed, 8 skipped (1064) |
| 9. Docker / portabilidad | 10 | `feature/docker-portability` | `ccf05d1`, `ff524e6` → `02c2505` | Portabilidad | 244: 236 passed, 8 skipped (1074) |

Las 8 pruebas omitidas pertenecen al *starter kit* y cubren funciones de Fortify desactivadas (p. ej., verificación de correo, A-01).

## Iteración 1: Bootstrap, autenticación y multiempresa

- **Objetivo:** base ejecutable en Docker con autenticación, roles, aislamiento por organización y auditoría base.
- **Funcionalidades:**
  - Laravel 13 con el *starter kit* React/Inertia sobre PostgreSQL y Redis, y `/health`.
  - Modelo `Organization`, roles (`UserRole`), *trait* `BelongsToOrganization` con `OrganizationScope`, middleware `role`.
  - Registro de postulante con cuenta global y `AuditLogger`.
- **Pruebas:** RED de 14 fallidas (clases inexistentes) → GREEN con `OrganizationScopeTest`, `AuditLoggerTest`, `RoleMiddlewareTest` y `CandidateRegistrationTest`: 31 passed, 8 skipped.
- **Defectos:**
  - DEF-01 (crítico para el arranque): contenedor `unhealthy` porque `artisan serve` recargaba `.env`.
  - DEF-02 (crítico): PHPUnit usaba la base de desarrollo.
- **Resultado:** entorno estable y aislamiento multiempresa verificado.

## Iteración 2: Requerimientos de personal y vacantes (RF-01 a RF-07)

- **Objetivo:** flujo completo del requerimiento y creación y publicación de vacantes.
- **Funcionalidades:**
  - `JobRequestWorkflow` (registrar, enviar, observar, corregir, validar, aprobar, rechazar) con historial y notificación de rechazo.
  - `VacancyService` y `VacancyValidator`, con perfil y criterios ponderados (`WeightingValidator`, A-06).
  - Portal público de empleos.
- **Pruebas:** `JobRequestStatusTest`, `WeightingValidatorTest`, `JobRequestWorkflowTest`, `VacancyPublicationTest` y `CrossTenantAccessTest`: 91 passed, 8 skipped.
- **Defectos:**
  - DEF-03: asignación masiva en `JobProfile`.
  - DEF-04: *build* roto por rutas de verificación de correo que ya no existían.
- **Resultado:** RF-01 a RF-07 implementados con interfaz y pruebas.

## Iteración 3: Postulantes y postulaciones (RF-08 a RF-15)

- **Objetivo:** ciclo del postulante y revisión de postulaciones por RR. HH.
- **Funcionalidades:**
  - Perfil y CV privado (PDF de hasta 5 MB).
  - Postulación única con perfil completo, confirmación con código y expediente.
  - Preselección, descarte con motivo y cambio de etapa (`ApplicationStatus`), con notificaciones de etapa.
- **Pruebas:** `ApplicationStatusTest`, `CandidateProfileTest`, `ApplyToVacancyTest` y `ApplicationReviewTest`: 129 passed, 8 skipped.
- **Defectos:** DEF-05, props de Inertia envueltas en `data` (detectado por prueba).
- **Resultado:** RF-08 a RF-15 implementados.

## Iteración 4: Evaluaciones y entrevistas (RF-16 a RF-19)

- **Objetivo:** programar sesiones con convocatoria y registrar resultados.
- **Funcionalidades:**
  - `AssessmentScheduler` (evaluador de la misma organización, fecha futura, avance automático de etapa, A-16).
  - Convocatorias al postulante y al evaluador.
  - `ScoreSheetValidator` y `AssessmentResultRecorder` (una sola vez; resultado de entrevista obligatorio).
  - Vistas del evaluador.
- **Pruebas:** checkpoint RED `3e66623` con **23 failed** → GREEN **23 passed (99 assertions)** → REFACTOR sin cambios de resultado. Suite: **152 passed, 8 skipped (532 assertions)**.
- **Defectos:** DEF-06 (crítico), un método `session()` que sobrescribía el de `Request` y terminaba el proceso PHP.
- **Resultado:** RF-16 a RF-19 implementados.

## Iteración 5: Ranking, decisión humana, selección y cierre (RF-20 a RF-25)

- **Objetivo:** ranking explicable como apoyo y cadena decisión → selección → cierre con la regla crítica de no selección automática.
- **Funcionalidades:**
  - `RankingService` puro (normalización ponderada, empates marcados, candidatos incompletos) y comparación.
  - `FinalDecisionService` (solo Aprobador/Dirección, con confirmación y justificación).
  - `SelectionRegistrationService` (índice único parcial) y `VacancyClosureService` (cierre con selección, las demás postulaciones a `no_seleccionado`).
- **Pruebas:**
  - 51 pruebas nuevas por bloques A–F, cada una con RED observado (p. ej., `FinalDecisionTest` 10 failed → GREEN).
  - `RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate` demuestra que calcular el ranking no cambia estados, decisiones ni auditoría.
  - Suite: **211 pruebas: 203 passed, 8 skipped (779 assertions)**.
- **Defectos:** errores de diseño de pruebas corregidos y documentados en `tdd-evidence.md`; sin defectos de producto registrados.
- **Resultado:** RF-20 a RF-25 implementados, con reglas aprobadas A-23 a A-30.

## Iteración 6: Notificaciones y auditoría (RF-26, RF-27)

- **Objetivo:** notificar el resultado final y completar una auditoría inmutable y consultable.
- **Funcionalidades:**
  - `ProcessResultNotification` (solo al cerrar, sin puntajes ni datos de terceros; A-31, A-32).
  - Vista de auditoría para Dirección con resumen seguro (A-33).
  - *Trigger* de solo inserción (A-34) y eliminación ampliada de claves sensibles.
- **Pruebas:** RED 6 failed + 10 failed → GREEN **19 passed (238 assertions)**; regresión cross-tenant de 16 passed. Suite: **230 pruebas: 222 passed, 8 skipped (1017 assertions)**.
- **Defectos:**
  - DEF-07: la auditoría podía modificarse con consultas masivas.
  - DEF-08: la eliminación de claves sensibles era incompleta.
- **Resultado:** línea base RF-01 a RF-27 completa.

## Iteración 7: Frontend integral

- **Objetivo:** validar toda la interfaz en navegador por rol y consolidar datos demo reproducibles.
- **Funcionalidades:** `DemoSeeder` construido con los servicios reales, revisión visual de navegación, estados, formularios y diseño adaptable, y atributos `data-cy`.
- **Pruebas:**
  - Recorrido visual 10/10 con 49 capturas y flujo integral manual 12/12 (`docs/manual-smoke-test.md`).
  - Pruebas nuevas `AppTimezoneTest` y de auditoría legible.
  - Suite: **233 pruebas: 225 passed, 8 skipped (1045 assertions)**.
- **Defectos:**
  - DEF-09: zona horaria del navegador.
  - DEF-10: auditoría con valores internos.
  - DEF-11: iniciales de avatar.
- **Resultado:** interfaz validada sin cambios en las reglas de negocio.

## Iteración 8: Suite E2E con Cypress

- **Objetivo:** automatizar E2E-01 a E2E-10, multiempresa, casos negativos y flujo integral.
- **Funcionalidades:**
  - Cypress 15.3.0 en Docker con comandos de soporte y *fixtures*.
  - Reset protegido por `E2E_ENABLED`, token y bloqueo en producción, con pruebas `E2eSupportTest`.
- **Pruebas:**
  - 13 specs y 40 tests: **40/40 en dos corridas completas** (04:01 y 03:56).
  - PHPUnit: **240 pruebas: 232 passed, 8 skipped (1064 assertions)**.
- **Defectos:** ninguno de la aplicación. Se corrigieron 2 tests con expectativas erróneas: E2E-04 (botón deshabilitado, no oculto) y E2E-10 (texto de RF-26).
- **Resultado:** suite E2E estable.

## Iteración 9: Docker y portabilidad

- **Objetivo:** que el proyecto funcione desde cero en otra PC.
- **Funcionalidades:**
  - Imágenes y versiones fijadas, políticas de reinicio, *healthcheck* del worker y puertos de base de datos y Redis solo en `127.0.0.1`.
  - Entorno E2E aislado (`app-e2e`, `queue-e2e`, `.env.e2e`, `reclutamiento_e2e`).
  - Fechas E2E en `America/Lima`, `docs/docker.md` y README.
- **Pruebas:**
  - `E2eSupportTest` + `E2eEnvironmentTest`: RED 4 failed → GREEN **11 passed**.
  - Instalación limpia en un clon: arranque en 87 s, 17 migraciones, *seed*, *smoke*, PHPUnit 244 (236 passed) y Cypress 43/43.
  - Entorno principal: PHPUnit **244 pruebas: 236 passed, 8 skipped (1074 assertions)**, *build*, `tsc` y Cypress **14 specs, 43/43**.
- **Defectos:**
  - DEF-12: fechas UTC en E2E.
  - DEF-13: el reset E2E afectaba la base de desarrollo.
- **Resultado:** instalación reproducible validada y base E2E aislada.
