# F29E — Matriz de trazabilidad RF → CU → CP → prueba automatizada → evidencia

> Generada por `f29e.py`, igual que el catálogo ([`F29E_Casos_de_Prueba.md`](F29E_Casos_de_Prueba.md)). Los CU se derivan de los RF con la tabla del Formato 08. Las columnas de pruebas y evidencia remiten a archivos reales.

## Cobertura de RF-01 a RF-27

| RF | Requerimiento | CU | CP automatizados aprobados | Todos los CP | Pruebas automatizadas | Evidencia |
|---|---|---|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | CU-01 | CP-001, CP-002, CP-079, CP-090 | CP-001, CP-002, CP-079, CP-090 | `cypress/e2e/e2e-02-register-job-request.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/JobRequests/JobRequestWorkflowTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-02 | Validar y corregir requerimiento | CU-02 | CP-002, CP-003, CP-079, CP-090 | CP-002, CP-003, CP-079, CP-090 | `cypress/e2e/e2e-02-register-job-request.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/JobRequests/JobRequestWorkflowTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-03 | Registrar aprobación o rechazo del requerimiento | CU-03 | CP-002, CP-004, CP-005, CP-080, CP-090 | CP-002, CP-004, CP-005, CP-080, CP-090 | `cypress/e2e/e2e-03-approve-job-request.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/JobRequests/JobRequestWorkflowTest.php`<br>`tests/Feature/Tenancy/CrossTenantAccessTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-04 | Notificar rechazo del requerimiento | CU-03 | CP-002, CP-006, CP-080 | CP-002, CP-006, CP-080 | `cypress/e2e/e2e-03-approve-job-request.cy.js`<br>`tests/Feature/JobRequests/JobRequestWorkflowTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-05 | Registrar perfil y criterios del puesto | CU-04 | CP-007, CP-008, CP-009, CP-081, CP-090 | CP-007, CP-008, CP-009, CP-081, CP-090 | `cypress/e2e/e2e-04-configure-publish-vacancy.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Vacancies/VacancyPublicationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-06 | Configurar y validar vacante | CU-05 | CP-007, CP-009, CP-010, CP-081 | CP-007, CP-009, CP-010, CP-081 | `cypress/e2e/e2e-04-configure-publish-vacancy.cy.js`<br>`tests/Feature/Vacancies/VacancyPublicationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-07 | Publicar vacante | CU-06 | CP-009, CP-011, CP-081, CP-090 | CP-009, CP-011, CP-081, CP-090 | `cypress/e2e/e2e-04-configure-publish-vacancy.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Vacancies/VacancyPublicationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-08 | Gestionar cuenta y acceso del postulante | CU-07 | CP-012, CP-013, CP-078, CP-082 | CP-012, CP-013, CP-078, CP-082 | `cypress/e2e/e2e-01-login.cy.js`<br>`cypress/e2e/e2e-05-candidate-apply.cy.js`<br>`tests/Feature/Auth/AuthenticationTest.php`<br>`tests/Feature/Auth/CandidateRegistrationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-09 | Gestionar perfil y CV del postulante | CU-08 | CP-014, CP-015, CP-082, CP-090 | CP-014, CP-015, CP-082, CP-090 | `cypress/e2e/e2e-05-candidate-apply.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Candidates/CandidateProfileTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-10 | Registrar postulación | CU-09 | CP-016, CP-017, CP-018, CP-082, CP-089, CP-090 | CP-016, CP-017, CP-018, CP-082, CP-089, CP-090 | `cypress/e2e/e2e-05-candidate-apply.cy.js`<br>`cypress/e2e/e2e-12-negative-rules.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Applications/ApplyToVacancyTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-11 | Confirmar postulación al postulante | CU-09 | CP-016, CP-017, CP-082 | CP-016, CP-017, CP-082 | `cypress/e2e/e2e-05-candidate-apply.cy.js`<br>`tests/Feature/Applications/ApplyToVacancyTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-12 | Consultar y revisar postulaciones | CU-10 | CP-019, CP-020, CP-083 | CP-019, CP-020, CP-083 | `cypress/e2e/e2e-06-shortlist-candidate.cy.js`<br>`tests/Feature/Applications/ApplicationReviewTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-13 | Registrar preselección o descarte | CU-11 | CP-020, CP-021, CP-022, CP-083 | CP-020, CP-021, CP-022, CP-083 | `cypress/e2e/e2e-06-shortlist-candidate.cy.js`<br>`tests/Feature/Applications/ApplicationReviewTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-14 | Gestionar cambio de etapa de la postulación | CU-12 | CP-020, CP-023, CP-024, CP-083, CP-090 | CP-020, CP-023, CP-024, CP-083, CP-090 | `cypress/e2e/e2e-06-shortlist-candidate.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Applications/ApplicationReviewTest.php`<br>`tests/Unit/Enums/ApplicationStatusTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-15 | Notificar cambio de etapa al candidato | CU-12 | CP-020, CP-021, CP-083 | CP-020, CP-021, CP-083 | `cypress/e2e/e2e-06-shortlist-candidate.cy.js`<br>`tests/Feature/Applications/ApplicationReviewTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-16 | Programar evaluación | CU-13 | CP-025, CP-026, CP-027, CP-090 | CP-025, CP-026, CP-027, CP-090 | `cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Assessments/EvaluationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-17 | Generar convocatoria de evaluación | CU-13 | CP-025, CP-027, CP-028, CP-090 | CP-025, CP-027, CP-028, CP-090 | `cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Assessments/EvaluationTest.php`<br>`tests/Feature/Assessments/InterviewTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-18 | Programar entrevista | CU-14 | CP-028, CP-029, CP-090 | CP-028, CP-029, CP-090 | `cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Assessments/InterviewTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-19 | Registrar entrevista y su resultado | CU-15 | CP-027, CP-028, CP-030, CP-084, CP-090 | CP-027, CP-028, CP-030, CP-084, CP-090 | `cypress/e2e/e2e-07-evaluator-records-results.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Assessments/EvaluationTest.php`<br>`tests/Feature/Assessments/InterviewTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-20 | Validar rangos y ponderaciones | CU-16 | CP-005, CP-027, CP-028, CP-031, CP-032, CP-033, CP-034, CP-035, CP-036, CP-037, CP-081, CP-084 | CP-005, CP-027, CP-028, CP-031, CP-032, CP-033, CP-034, CP-035, CP-036, CP-037, CP-081, CP-084 | `cypress/e2e/e2e-04-configure-publish-vacancy.cy.js`<br>`cypress/e2e/e2e-07-evaluator-records-results.cy.js`<br>`tests/Feature/Assessments/EvaluationTest.php`<br>`tests/Feature/Assessments/InterviewTest.php`<br>`tests/Feature/Selection/RankingComparisonTest.php`<br>`tests/Feature/Tenancy/CrossTenantAccessTest.php`<br>`tests/Unit/Assessments/ScoreSheetValidatorTest.php`<br>`tests/Unit/Evaluation/WeightingValidatorTest.php`<br>`tests/Unit/Ranking/RankingServiceTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-21 | Calcular ranking configurable | CU-17 | CP-038, CP-039, CP-040, CP-085, CP-090 | CP-038, CP-039, CP-040, CP-085, CP-090 | `cypress/e2e/e2e-08-comparison-ranking.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Selection/RankingComparisonTest.php`<br>`tests/Unit/Ranking/RankingServiceTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-22 | Presentar comparación de candidatos | CU-17 | CP-038, CP-041, CP-085 | CP-038, CP-041, CP-085 | `cypress/e2e/e2e-08-comparison-ranking.cy.js`<br>`tests/Feature/Selection/RankingComparisonTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-23 | Registrar decisión final de selección | CU-18 | CP-042, CP-043, CP-086, CP-089, CP-090 | CP-042, CP-043, CP-086, CP-089, CP-090 | `cypress/e2e/e2e-09-human-final-decision.cy.js`<br>`cypress/e2e/e2e-12-negative-rules.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Selection/FinalDecisionTest.php`<br>`tests/Feature/Selection/RankingComparisonTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-24 | Registrar selección del candidato | CU-19 | CP-044, CP-087, CP-089, CP-090 | CP-044, CP-087, CP-089, CP-090 | `cypress/e2e/e2e-10-selection-and-closure.cy.js`<br>`cypress/e2e/e2e-12-negative-rules.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Selection/SelectionRegistrationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-25 | Cerrar vacante o convocatoria | CU-20 | CP-024, CP-045, CP-087, CP-089, CP-090 | CP-024, CP-045, CP-087, CP-089, CP-090 | `cypress/e2e/e2e-10-selection-and-closure.cy.js`<br>`cypress/e2e/e2e-12-negative-rules.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Selection/VacancyClosureTest.php`<br>`tests/Unit/Enums/ApplicationStatusTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-26 | Notificar resultado y cierre al postulante | CU-20 | CP-046, CP-047, CP-087, CP-090 | CP-046, CP-047, CP-087, CP-090 | `cypress/e2e/e2e-10-selection-and-closure.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Notifications/ProcessResultNotificationTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |
| RF-27 | Generar registro de auditoría | — | CP-046, CP-048, CP-049, CP-050, CP-051, CP-088, CP-090 | CP-046, CP-048, CP-049, CP-050, CP-051, CP-088, CP-090 | `cypress/e2e/e2e-11-multitenancy.cy.js`<br>`cypress/e2e/e2e-13-full-recruitment-flow.cy.js`<br>`tests/Feature/Audit/AuditLogViewTest.php`<br>`tests/Feature/Audit/AuditLoggerTest.php`<br>`tests/Feature/Audit/AuditTrailTest.php`<br>`tests/Feature/Notifications/ProcessResultNotificationTest.php`<br>`tests/Feature/Tenancy/OrganizationScopeTest.php` | docs/academico/qa-final/evidencias/04-phpunit.log<br>docs/academico/qa-final/evidencias/09-cypress.log<br>docs/academico/qa-final/evidencias/phpunit-junit.xml |

**Resultado:** 27 de 27 RF con al menos un CP automatizado aprobado. CU cubiertos a través de sus RF: 20 de 20.

## Casos transversales y fuera de la línea base

| CP | Título | Tipo | Referencia | Estado |
|---|---|---|---|---|
| CP-052 | Transversal — DashboardTest | Integración / funcional | Transversal | APROBADO |
| CP-053 | RF-29 (EXPERIMENTAL / PROPUESTO) — MlCrossTenantValidationTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-054 | RF-29 (EXPERIMENTAL / PROPUESTO) — MlRiskClientTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-055 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskAuthorizationTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-056 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskCheckpointTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-057 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskFeatureBuilderTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-058 | RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskServiceTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-059 | RF-29 (EXPERIMENTAL / PROPUESTO) — TargetCompletionTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-060 | RF-29 (EXPERIMENTAL / PROPUESTO) — VacancyOperationalRiskRouteTest | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-061 | Prueba de humo del starter kit — ExampleTest | Regresión | Prueba de humo del starter kit | APROBADO |
| CP-062 | Regresión de DEF-09 (zona horaria) — AppTimezoneTest | Regresión | Regresión de DEF-09 (zona horaria) | APROBADO |
| CP-063 | Prueba de humo del starter kit — ExampleTest | Regresión | Prueba de humo del starter kit | APROBADO |
| CP-064 | RNF-01 — EmailVerificationTest | Seguridad básica | RNF-01 | OMITIDO (función del starter kit desactivada) |
| CP-065 | RNF-01 — PasswordConfirmationTest | Seguridad básica | RNF-01 | APROBADO |
| CP-066 | RNF-01 — PasswordResetTest | Seguridad básica | RNF-01 | APROBADO |
| CP-067 | RNF-01 — RegistrationTest | Seguridad básica | RNF-01 | APROBADO |
| CP-068 | RNF-01 — RoleMiddlewareTest | Seguridad básica | RNF-01 | APROBADO |
| CP-069 | RNF-01 — TwoFactorChallengeTest | Seguridad básica | RNF-01 | APROBADO |
| CP-070 | RNF-01 — VerificationNotificationTest | Seguridad básica | RNF-01 | OMITIDO (función del starter kit desactivada) |
| CP-071 | RNF-01 — NumericRouteParametersTest | Seguridad básica | RNF-01 | APROBADO |
| CP-072 | RNF-01 — ProfileUpdateTest | Seguridad básica | RNF-01 | APROBADO |
| CP-073 | RNF-01 — SecurityTest | Seguridad básica | RNF-01 | APROBADO |
| CP-074 | RNF-01; regresión de DEF-13 — E2eEnvironmentTest | Seguridad básica | RNF-01; regresión de DEF-13 | APROBADO |
| CP-075 | RNF-01; regresión de DEF-13 — E2eSupportTest | Seguridad básica | RNF-01; regresión de DEF-13 | APROBADO |
| CP-076 | Transversal — JobRequestStatusTest | Unitaria | Transversal | APROBADO |
| CP-077 | E2E-00 · Soporte · fechas en la zona horaria de la aplicación | Regresión | Regresión de DEF-12 (fechas en la zona horaria de la aplicación) | APROBADO |
| CP-091 | E2E-14 · E2E-14 · RR. HH. captura el plazo objetivo del proceso (GAP-01) | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-092 | E2E-15 · E2E-15 · Panel de riesgo operacional (RF-29, experimental) | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-093 | E2E-16 · E2E-16 · La tabla de expedientes conserva su semántica en móvil | UI / E2E (accesibilidad) | RNF-05 (usabilidad y accesibilidad) | APROBADO |
| CP-094 | E2E-17 · E2E-17 · El movimiento respeta el teclado y a quien lo reduce | UI / E2E (accesibilidad) | RNF-05 (usabilidad y accesibilidad) | APROBADO |
| CP-095 | E2E-18 · E2E-18 · La profundidad de la portada es opcional y nunca estorba | UI / E2E (accesibilidad) | RNF-05 (usabilidad y accesibilidad) | APROBADO |
| CP-096 | E2E-19 · E2E-19 · QA visual y accesibilidad de la Fase 21 | UI / E2E (accesibilidad) | RNF-05 (usabilidad y accesibilidad) | APROBADO |
| CP-097 | Componente de interfaz «data-table» | UI / componentes | RNF-05 (usabilidad) | APROBADO |
| CP-098 | Componente de interfaz «experience-3d» | UI / componentes | RNF-05 (usabilidad) | APROBADO |
| CP-099 | Componente de interfaz «form-controls» | UI / componentes | RNF-05 (usabilidad) | APROBADO |
| CP-100 | Componente de interfaz «motion» | UI / componentes | RNF-05 (usabilidad) | APROBADO |
| CP-101 | Componente de interfaz «password-input» | UI / componentes | RNF-05 (usabilidad) | APROBADO |
| CP-102 | Componente de interfaz «visual-qa» | UI / componentes | RNF-05 (usabilidad) | APROBADO |
| CP-103 | Servicio ML: ablation | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-104 | Servicio ML: api security | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-105 | Servicio ML: api service | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-106 | Servicio ML: dataset distributions | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-107 | Servicio ML: dataset no leakage | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-108 | Servicio ML: dataset schema | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-109 | Servicio ML: dataset temporal integrity | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-110 | Servicio ML: experiment freeze | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-111 | Servicio ML: freeze contract | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-112 | Servicio ML: generator reproducibility | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-113 | Servicio ML: metrics | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-114 | Servicio ML: model reproducibility | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-115 | Servicio ML: serving artifact | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-116 | Servicio ML: serving cli | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-117 | Servicio ML: stage history semantics | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-118 | Servicio ML: temporal split | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-119 | Servicio ML: threshold selection | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-120 | Servicio ML: training no leakage | ML experimental | RF-29 (EXPERIMENTAL / PROPUESTO) | APROBADO |
| CP-121 | Tipos de TypeScript del frontend | Estática / build | RNF-09 (mantenibilidad) | APROBADO |
| CP-122 | Compilación del frontend | Estática / build | RNF-09 (mantenibilidad) | APROBADO |
| CP-123 | Configuración de Docker Compose | Estática / build | RNF-09 (mantenibilidad) | APROBADO |
| CP-124 | Integración continua (GitHub Actions `tests`) | Regresión / CI | RNF-09 | APROBADO en develop (bc44303); main (60ebcb2): sin ejecución — pendiente de ejecución manual |
| CP-125 | Recorrido visual por rol en navegador | Aceptación (manual) | RNF-05 | EJECUTADO EN LA FASE 8 (13/09/2026): 10/10; no repetido en la F29F |
| CP-126 | Aceptación por el usuario institucional (RR. HH. / Dirección del Colegio) | Aceptación (manual) | Validación institucional | NO EJECUTADO: sin validación institucional (fuera de alcance) |
| CP-127 | Rendimiento y carga | No funcional | RNF-06 | NO EJECUTADO: sin herramienta de carga ni SLA (RNF-06 NO VERIFICADO) |
| CP-128 | Disponibilidad y recuperación | No funcional | RNF-07 | NO EJECUTADO: sin entorno de producción (RNF-07 NO VERIFICADO) |
