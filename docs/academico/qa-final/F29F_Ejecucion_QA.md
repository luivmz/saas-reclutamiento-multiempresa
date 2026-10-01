# F29F — Ejecución QA final

> Generado por `docs/academico/tools/f27b/f29f.py` a partir de la evidencia versionada en [`evidencias/`](evidencias/): `python docs/academico/tools/f27b/build.py f29f`. Cada cifra sale de la salida real de la herramienta; no se usaron resultados históricos.

## Qué se probó

| Dato | Valor |
|---|---|
| Fecha | 30/09/2026 (de 2026-09-30 10:53:03 -0500 a 2026-09-30 11:02:12 -0500, más las repeticiones y mediciones indicadas) |
| Commit probado | `bc44303d307004de494c4e03f3186ee190118c4c` (`develop`, F29C integrada); árbol limpio al iniciar |
| Plan aplicado | [F29D](../plan-pruebas/README.md), criterios CA-01 a CA-07 |
| Casos de prueba | [F29E](../casos-prueba/README.md): 128 CP |
| Docker | Docker 29.7.2 · Compose v5.5.1 |
| Contenedor `app` | PHP 8.4.25 · Node v22.23.2 |
| Servicios | PostgreSQL 17.11 · Redis 7.4.11; `app`, `app-e2e`, `postgres`, `queue`, `queue-e2e` y `redis` healthy |
| Servicio ML | Python 3.12.5 (`ml-service/.venv`) |
| Equipo | AMD Ryzen 9 5900X, 31,9 GB de RAM, Windows 11 Pro; Docker Desktop con 24 CPU y 16,7 GB |

## Resultados por herramienta

| Registro | Herramienta | Comando | Aprobadas / resultado | Fallidas | Omitidas | Aserciones | Duración | Código de salida |
|---|---|---|---|---|---|---|---|---|
| [`04-phpunit`](evidencias/04-phpunit.log) | PHPUnit (1.ª ejecución) | `docker compose exec -T app php artisan test` | 411 | 0 | 8 | 1498 | 53.11s | 0 |
| [`04b-phpunit-junit`](evidencias/04b-phpunit-junit.log) | PHPUnit (2.ª ejecución, con JUnit) | `docker compose exec -T app php artisan test --log-junit …` | 411 | 0 | 8 | 1498 | 43.27s | 0 |
| [`05-tsc`](evidencias/05-tsc.log) | TypeScript | `docker compose exec -T app npx tsc --noEmit` | — | 0 errores | — | — | — | 0 |
| [`06-build`](evidencias/06-build.log) | Build del frontend (Vite) | `docker compose exec -T app npm run build` | 2375 módulos | 0 | — | — | 33.80s | 0 |
| [`07-vitest`](evidencias/07-vitest.log) | Vitest (componentes) | `docker compose exec -T app npx vp test --run` | 42 | 0 | 0 | — | 1.39s | 0 |
| [`08-pytest`](evidencias/08-pytest.log) | pytest (1.ª ejecución) | `cd ml-service && .venv/Scripts/python.exe -m pytest -q` | sin conteo (resumen suprimido por -q duplicado) | — | — | — | — | 0 |
| [`08b-pytest`](evidencias/08b-pytest.log) | pytest (2.ª ejecución, con resumen) | `cd ml-service && .venv/Scripts/python.exe -m pytest --junitxml=…` | 533 | 0 | 0 | — | 66.19s | 0 |
| [`09-cypress`](evidencias/09-cypress.log) | Cypress E2E (20 specs) | `npm run cy:run` | 85 | 0 | 0 | — | 05:31 | 0 |
| [`03-compose-config`](evidencias/03-compose-config.log) | Configuración de Docker Compose | `docker compose config --quiet` | válida | — | — | — | — | 0 |
| [`11-pint`](evidencias/11-pint.log) | Estilo PHP (Pint, medición) | `docker compose exec -T app vendor/bin/pint --test` | 256 archivos | 8 avisos de estilo | — | — | — | 1 |
| [`12-vp-check`](evidencias/12-vp-check.log) | Formato (vp check, medición) | `docker compose exec -T app npx vp check` | — | 226 archivos con formato pendiente | — | — | — | 1 |

**Integración continua** (evidencia: [`ci-github-actions.json`](evidencias/ci-github-actions.json), respuesta de la API de GitHub):

| Rama | Commit | Resultado | Ejecución |
|---|---|---|---|
| CI develop | `bc44303` | success | https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/36736500405 |
| CI main | `60ebcb2` | sin ejecución | — |

## Evaluación de los criterios de aceptación del plan

| Criterio | Descripción | Resultado | Evidencia |
|---|---|---|---|
| CA-01 | PHPUnit sin fallos; solo las 8 omitidas del starter kit | **CUMPLE** | 411 aprobadas, 0 fallidas, 8 omitidas (verificación de correo desactivada en Fortify) |
| CA-02 | Cypress: 20 specs, 0 fallidos, sin reintentos | **CUMPLE** | 85/85 en 20 specs |
| CA-03 | Vitest y pytest sin fallos | **CUMPLE** | Vitest 42/42; pytest 533 aprobadas, 0 fallidas |
| CA-04 | TypeScript y build sin errores | **CUMPLE** | tsc y build con código de salida 0 |
| CA-05 | CI en verde en develop | **CUMPLE** | develop: success; main: sin ejecución (pendiente de ejecución manual) |
| CA-06 | Cada RF-01 a RF-27 con un CP automatizado aprobado | **CUMPLE** | 27 de 27 RF |
| CA-07 | Ningún defecto de severidad Alta abierto | **CUMPLE** | Registro unificado de la F29G (v1.0 y v1.1): 0 defectos Críticos o Altos abiertos |

**Dictamen:** se cumplen los siete criterios de aceptación. No hubo pruebas fallidas, así que no fue necesario clasificar fallos como regresión, flaky, ambiente, dependencia externa o documental. Las observaciones siguientes sí se clasifican.

## Observaciones clasificadas

| ID | Clasificación | Descripción | Estado |
|---|---|---|---|
| OBS-F29F-01 | Procedimiento | La primera ejecución de pytest usó `-q` y el `pyproject.toml` ya fija `addopts = "-q"`: con `-qq`, pytest no imprimió el resumen de conteos, aunque terminó con código 0. Se repitió sin el `-q` extra (08b), con 533 aprobadas. No es un defecto del software; se conservan las dos ejecuciones. | Documentado |
| OBS-F29F-02 | Repetición | PHPUnit se ejecutó dos veces: la segunda, con `--log-junit`, para el detalle por clase que usa la matriz CP → resultado. Los conteos coinciden (411/0/8, 1498 aserciones); solo cambia la duración. | Documentado |
| OBS-F29F-03 | No aplicable | Las 8 pruebas omitidas de PHPUnit (`EmailVerificationTest`, `VerificationNotificationTest`) dependen de `Features::emailVerification()`, desactivada en Fortify. No son fallos. | Aceptado |
| OBS-F29F-04 | Dependencia externa (CI) | El merge F29C en `main` (`60ebcb2`) no generó ejecución de GitHub Actions: el push terminó con un error del cliente aunque la rama se actualizó. `main` tiene el mismo árbol que `develop` (`bc44303`), cuya CI pasó. Deuda: **CI main F29C pendiente de ejecución manual** (`workflow_dispatch`). | Abierto |
| OBS-F29F-05 | Deuda de estilo | Pint informa 8 avisos de estilo en 256 archivos PHP. `vp check` informa formato pendiente en 226 archivos: 188 Markdown y 35 de código o configuración. Es F25-L03, solo de formato, y la CI no lo verifica. No se corrige en la F29F porque cambiaría código fuera del alcance autorizado. | Abierto (LOW) |
| OBS-F29F-06 | Entorno | La documentación de la F29D a la F29H se escribió mientras corrían las suites: al final, `git status` mostraba solo archivos de `docs/academico/`. El runtime probado es exactamente `bc44303`: el árbol estaba limpio al empezar (01-git). | Documentado |

## Matriz CP → resultado

Estado de cada caso de prueba de la F29E según esta ejecución (detalle y pasos en [`F29E_Casos_de_Prueba.md`](../casos-prueba/F29E_Casos_de_Prueba.md)).

| CP | Título | Suite | Ejecuciones | Aprobadas | Fallidas | Omitidas | Estado |
|---|---|---|---|---|---|---|---|
| CP-001 | Registrar requerimiento de personal | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-002 | Reglas complementarias de JobRequestWorkflowTest (RF-01, RF-02, RF-03, RF-04) | PHPUnit | 4 | 4 | 0 | 0 | APROBADO |
| CP-003 | Validar y corregir requerimiento | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-004 | Registrar aprobación o rechazo del requerimiento | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-005 | Reglas complementarias de CrossTenantAccessTest (RF-03, RF-20) | PHPUnit | 6 | 6 | 0 | 0 | APROBADO |
| CP-006 | Notificar rechazo del requerimiento | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-007 | Registrar perfil y criterios del puesto / Configurar y validar vacante | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-008 | Registrar perfil y criterios del puesto | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-009 | Reglas complementarias de VacancyPublicationTest (RF-05, RF-06, RF-07) | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-010 | Configurar y validar vacante | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-011 | Publicar vacante | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-012 | Reglas complementarias de AuthenticationTest (RF-08) | PHPUnit | 6 | 6 | 0 | 0 | APROBADO |
| CP-013 | Reglas complementarias de CandidateRegistrationTest (RF-08) | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-014 | Reglas complementarias de CandidateProfileTest (RF-09) | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-015 | Gestionar perfil y CV del postulante | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-016 | Registrar postulación / Confirmar postulación al postulante | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-017 | Reglas complementarias de ApplyToVacancyTest (RF-10, RF-11) | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-018 | Registrar postulación | PHPUnit | 4 | 4 | 0 | 0 | APROBADO |
| CP-019 | Consultar y revisar postulaciones | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-020 | Reglas complementarias de ApplicationReviewTest (RF-12, RF-13, RF-14, RF-15) | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-021 | Registrar preselección o descarte / Notificar cambio de etapa al candidato | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-022 | Registrar preselección o descarte | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-023 | Gestionar cambio de etapa de la postulación | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-024 | Reglas complementarias de ApplicationStatusTest (RF-14, RF-25) | PHPUnit | 21 | 21 | 0 | 0 | APROBADO |
| CP-025 | Programar evaluación / Generar convocatoria de evaluación | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-026 | Programar evaluación | PHPUnit | 4 | 4 | 0 | 0 | APROBADO |
| CP-027 | Reglas complementarias de EvaluationTest (RF-16, RF-17, RF-19, RF-20) | PHPUnit | 6 | 6 | 0 | 0 | APROBADO |
| CP-028 | Reglas complementarias de InterviewTest (RF-17, RF-18, RF-19, RF-20) | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-029 | Programar entrevista | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-030 | Registrar entrevista y su resultado | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-031 | Validar rangos y ponderaciones | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-032 | Validar rangos y ponderaciones | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-033 | Validar rangos y ponderaciones | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-034 | Validar rangos y ponderaciones | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-035 | Reglas complementarias de ScoreSheetValidatorTest (RF-20) | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-036 | Reglas complementarias de WeightingValidatorTest (RF-20) | PHPUnit | 8 | 8 | 0 | 0 | APROBADO |
| CP-037 | Validar rangos y ponderaciones | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-038 | Calcular ranking configurable / Presentar comparación de candidatos | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-039 | Calcular ranking configurable | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-040 | Calcular ranking configurable | PHPUnit | 9 | 9 | 0 | 0 | APROBADO |
| CP-041 | Presentar comparación de candidatos | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-042 | Registrar decisión final de selección | PHPUnit | 10 | 10 | 0 | 0 | APROBADO |
| CP-043 | Registrar decisión final de selección | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-044 | Registrar selección del candidato | PHPUnit | 7 | 7 | 0 | 0 | APROBADO |
| CP-045 | Cerrar vacante o convocatoria | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-046 | Notificar resultado y cierre al postulante / Generar registro de auditoría | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-047 | Notificar resultado y cierre al postulante | PHPUnit | 7 | 7 | 0 | 0 | APROBADO |
| CP-048 | Generar registro de auditoría | PHPUnit | 7 | 7 | 0 | 0 | APROBADO |
| CP-049 | Reglas complementarias de AuditLoggerTest (RF-27) | PHPUnit | 4 | 4 | 0 | 0 | APROBADO |
| CP-050 | Generar registro de auditoría | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-051 | Reglas complementarias de OrganizationScopeTest (RF-27) | PHPUnit | 4 | 4 | 0 | 0 | APROBADO |
| CP-052 | Transversal — DashboardTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-053 | RF-29 (EXPERIMENTAL / PROPUESTO) — MlCrossTenantValidationTest | PHPUnit | 10 | 10 | 0 | 0 | APROBADO |
| CP-054 | RF-29 (EXPERIMENTAL / PROPUESTO) — MlRiskClientTest | PHPUnit | 64 | 64 | 0 | 0 | APROBADO |
| CP-055 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskAuthorizationTest | PHPUnit | 11 | 11 | 0 | 0 | APROBADO |
| CP-056 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskCheckpointTest | PHPUnit | 21 | 21 | 0 | 0 | APROBADO |
| CP-057 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskFeatureBuilderTest | PHPUnit | 19 | 19 | 0 | 0 | APROBADO |
| CP-058 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskServiceTest | PHPUnit | 19 | 19 | 0 | 0 | APROBADO |
| CP-059 | RF-29 (EXPERIMENTAL / PROPUESTO) — TargetCompletionTest | PHPUnit | 16 | 16 | 0 | 0 | APROBADO |
| CP-060 | RF-29 (EXPERIMENTAL / PROPUESTO) — VacancyOperationalRiskRouteTest | PHPUnit | 12 | 12 | 0 | 0 | APROBADO |
| CP-061 | Prueba de humo del starter kit — ExampleTest | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-062 | Regresión de DEF-09 (zona horaria) — AppTimezoneTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-063 | Prueba de humo del starter kit — ExampleTest | PHPUnit | 1 | 1 | 0 | 0 | APROBADO |
| CP-064 | RNF-01 — EmailVerificationTest | PHPUnit | 6 | 0 | 0 | 6 | OMITIDO (función del starter kit desactivada) |
| CP-065 | RNF-01 — PasswordConfirmationTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-066 | RNF-01 — PasswordResetTest | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-067 | RNF-01 — RegistrationTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-068 | RNF-01 — RoleMiddlewareTest | PHPUnit | 3 | 3 | 0 | 0 | APROBADO |
| CP-069 | RNF-01 — TwoFactorChallengeTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-070 | RNF-01 — VerificationNotificationTest | PHPUnit | 2 | 0 | 0 | 2 | OMITIDO (función del starter kit desactivada) |
| CP-071 | RNF-01 — NumericRouteParametersTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-072 | RNF-01 — ProfileUpdateTest | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-073 | RNF-01 — SecurityTest | PHPUnit | 5 | 5 | 0 | 0 | APROBADO |
| CP-074 | RNF-01; regresión de DEF-13 — E2eEnvironmentTest | PHPUnit | 2 | 2 | 0 | 0 | APROBADO |
| CP-075 | RNF-01; regresión de DEF-13 — E2eSupportTest | PHPUnit | 9 | 9 | 0 | 0 | APROBADO |
| CP-076 | Transversal — JobRequestStatusTest | PHPUnit | 13 | 13 | 0 | 0 | APROBADO |
| CP-077 | E2E-00 · Soporte · fechas en la zona horaria de la aplicación | Cypress | 3 | 3 | 0 | 0 | APROBADO |
| CP-078 | E2E-01 · E2E-01 · Inicio de sesión por rol | Cypress | 6 | 6 | 0 | 0 | APROBADO |
| CP-079 | E2E-02 · E2E-02 · El área solicitante registra un requerimiento (RF-01) | Cypress | 2 | 2 | 0 | 0 | APROBADO |
| CP-080 | E2E-03 · E2E-03 · El aprobador decide un requerimiento validado (RF-03, RF-04) | Cypress | 2 | 2 | 0 | 0 | APROBADO |
| CP-081 | E2E-04 · E2E-04 · RR. HH. configura y publica una vacante (RF-05 a RF-07) | Cypress | 2 | 2 | 0 | 0 | APROBADO |
| CP-082 | E2E-05 · E2E-05 · El postulante completa su perfil y postula (RF-08 a RF-11) | Cypress | 1 | 1 | 0 | 0 | APROBADO |
| CP-083 | E2E-06 · E2E-06 · RR. HH. preselecciona a un candidato (RF-12 a RF-15) | Cypress | 2 | 2 | 0 | 0 | APROBADO |
| CP-084 | E2E-07 · E2E-07 · El evaluador registra resultados (RF-19, RF-20) | Cypress | 1 | 1 | 0 | 0 | APROBADO |
| CP-085 | E2E-08 · E2E-08 · RR. HH. consulta la comparación y el ranking (RF-21, RF-22) | Cypress | 1 | 1 | 0 | 0 | APROBADO |
| CP-086 | E2E-09 · E2E-09 · El aprobador registra la decisión final humana (RF-23) | Cypress | 2 | 2 | 0 | 0 | APROBADO |
| CP-087 | E2E-10 · E2E-10 · RR. HH. registra la selección y cierra el proceso (RF-24 a RF-26) | Cypress | 1 | 1 | 0 | 0 | APROBADO |
| CP-088 | E2E-11 · Multitenancy · aislamiento entre organizaciones | Cypress | 4 | 4 | 0 | 0 | APROBADO |
| CP-089 | E2E-12 · Negativos · permisos y reglas del proceso | Cypress | 4 | 4 | 0 | 0 | APROBADO |
| CP-090 | E2E-13 · Flujo integral · de requerimiento a auditoría | Cypress | 12 | 12 | 0 | 0 | APROBADO |
| CP-091 | E2E-14 · E2E-14 · RR. HH. captura el plazo objetivo del proceso (GAP-01) | Cypress | 4 | 4 | 0 | 0 | APROBADO |
| CP-092 | E2E-15 · E2E-15 · Panel de riesgo operacional (RF-29, experimental) | Cypress | 8 | 8 | 0 | 0 | APROBADO |
| CP-093 | E2E-16 · E2E-16 · La tabla de expedientes conserva su semántica en móvil | Cypress | 7 | 7 | 0 | 0 | APROBADO |
| CP-094 | E2E-17 · E2E-17 · El movimiento respeta el teclado y a quien lo reduce | Cypress | 8 | 8 | 0 | 0 | APROBADO |
| CP-095 | E2E-18 · E2E-18 · La profundidad de la portada es opcional y nunca estorba | Cypress | 8 | 8 | 0 | 0 | APROBADO |
| CP-096 | E2E-19 · E2E-19 · QA visual y accesibilidad de la Fase 21 | Cypress | 7 | 7 | 0 | 0 | APROBADO |
| CP-097 | Componente de interfaz «data-table» | Vitest | 7 | 7 | 0 | 0 | APROBADO |
| CP-098 | Componente de interfaz «experience-3d» | Vitest | 13 | 13 | 0 | 0 | APROBADO |
| CP-099 | Componente de interfaz «form-controls» | Vitest | 8 | 8 | 0 | 0 | APROBADO |
| CP-100 | Componente de interfaz «motion» | Vitest | 5 | 5 | 0 | 0 | APROBADO |
| CP-101 | Componente de interfaz «password-input» | Vitest | 3 | 3 | 0 | 0 | APROBADO |
| CP-102 | Componente de interfaz «visual-qa» | Vitest | 6 | 6 | 0 | 0 | APROBADO |
| CP-103 | Servicio ML: ablation | pytest | 9 | 9 | 0 | 0 | APROBADO |
| CP-104 | Servicio ML: api security | pytest | 24 | 24 | 0 | 0 | APROBADO |
| CP-105 | Servicio ML: api service | pytest | 56 | 56 | 0 | 0 | APROBADO |
| CP-106 | Servicio ML: dataset distributions | pytest | 21 | 21 | 0 | 0 | APROBADO |
| CP-107 | Servicio ML: dataset no leakage | pytest | 20 | 20 | 0 | 0 | APROBADO |
| CP-108 | Servicio ML: dataset schema | pytest | 93 | 93 | 0 | 0 | APROBADO |
| CP-109 | Servicio ML: dataset temporal integrity | pytest | 15 | 15 | 0 | 0 | APROBADO |
| CP-110 | Servicio ML: experiment freeze | pytest | 14 | 14 | 0 | 0 | APROBADO |
| CP-111 | Servicio ML: freeze contract | pytest | 113 | 113 | 0 | 0 | APROBADO |
| CP-112 | Servicio ML: generator reproducibility | pytest | 22 | 22 | 0 | 0 | APROBADO |
| CP-113 | Servicio ML: metrics | pytest | 10 | 10 | 0 | 0 | APROBADO |
| CP-114 | Servicio ML: model reproducibility | pytest | 13 | 13 | 0 | 0 | APROBADO |
| CP-115 | Servicio ML: serving artifact | pytest | 57 | 57 | 0 | 0 | APROBADO |
| CP-116 | Servicio ML: serving cli | pytest | 8 | 8 | 0 | 0 | APROBADO |
| CP-117 | Servicio ML: stage history semantics | pytest | 11 | 11 | 0 | 0 | APROBADO |
| CP-118 | Servicio ML: temporal split | pytest | 20 | 20 | 0 | 0 | APROBADO |
| CP-119 | Servicio ML: threshold selection | pytest | 10 | 10 | 0 | 0 | APROBADO |
| CP-120 | Servicio ML: training no leakage | pytest | 17 | 17 | 0 | 0 | APROBADO |
| CP-121 | Tipos de TypeScript del frontend | Estática | 1 | 1 | 0 | 0 | APROBADO |
| CP-122 | Compilación del frontend | Estática | 1 | 1 | 0 | 0 | APROBADO |
| CP-123 | Configuración de Docker Compose | Estática | 1 | 1 | 0 | 0 | APROBADO |
| CP-124 | Integración continua (GitHub Actions `tests`) | CI | 1 | 1 | 0 | 0 | APROBADO en develop (bc44303); main (60ebcb2): sin ejecución — pendiente de ejecución manual |
| CP-125 | Recorrido visual por rol en navegador | Manual | 0 | 0 | 0 | 0 | EJECUTADO EN LA FASE 8 (13/09/2026): 10/10; no repetido en la F29F |
| CP-126 | Aceptación por el usuario institucional (RR. HH. / Dirección del Colegio) | Manual | 0 | 0 | 0 | 0 | NO EJECUTADO: sin validación institucional (fuera de alcance) |
| CP-127 | Rendimiento y carga | Manual | 0 | 0 | 0 | 0 | NO EJECUTADO: sin herramienta de carga ni SLA (RNF-06 NO VERIFICADO) |
| CP-128 | Disponibilidad y recuperación | Manual | 0 | 0 | 0 | 0 | NO EJECUTADO: sin entorno de producción (RNF-07 NO VERIFICADO) |
| **Total** | | | **1083** | **1075** | **0** | **8** | |

## Evidencia

- **Registros:** `evidencias/*.log`, uno por paso. Cada uno trae el comando, la hora de inicio y de fin, la salida completa y el código de salida.
- **Saneamiento:** se quitaron los códigos de color ANSI y se reemplazaron el nombre del equipo y la ruta temporal del job. Ningún resultado se alteró, y los registros no contienen secretos: `.env.e2e` nunca se imprime.
- **Resumen de la primera ronda:** `evidencias/00-resumen.tsv`.
- **Detalle por prueba:** `evidencias/phpunit-junit.xml` (419 casos) y `evidencias/pytest-junit.xml` (533).
- **Integración continua:** `evidencias/ci-github-actions.json`.
