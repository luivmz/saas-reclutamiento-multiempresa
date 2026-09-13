# Matriz maestra de trazabilidad (RF-01 a RF-27)

Verificada contra el código y las pruebas en la Fase 11 (rama `feature/final-documentation`, base `develop` `02c2505`).

- **PHPUnit:** clases de prueba reales en `tests/`. Los nombres `test_rfNN_*` se listaron con búsqueda en el código.
- **Cypress:** specs reales en `cypress/e2e/` (ver `docs/testing/cypress-e2e.md`).
- **Línea base:** contiene exactamente 27 RF.

| RF | Funcionalidad | Actor | Backend | Frontend | PHPUnit | Cypress | Estado |
|---|---|---|---|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | Área solicitante | `JobRequestController`, `JobRequestWorkflow::register` | `job-requests/create` | `JobRequestWorkflowTest::test_rf01_*` (2) | E2E-02, E2E-13 | Implementado |
| RF-02 | Validar y corregir requerimiento | RR. HH. / Área solicitante | `JobRequestTransitionController` (`submit`, `observe`, `validate`), `JobRequestWorkflow` | `job-requests/show`, `job-requests/edit` | `JobRequestWorkflowTest::test_rf02_*` (2) | E2E-02 (envío), E2E-13 (validación) | Implementado |
| RF-03 | Registrar aprobación o rechazo | Aprobador / Dirección | `JobRequestTransitionController::decide`, `JobRequestWorkflow::approve/reject`, `JobRequestPolicy` | Panel de decisión en `job-requests/show` | `JobRequestWorkflowTest::test_rf03_*`, `CrossTenantAccessTest` | E2E-03, E2E-13 | Implementado |
| RF-04 | Notificar rechazo | Sistema → Área solicitante | `JobRequestRejectedNotification` | `notifications/index`, alerta de rechazo en `job-requests/show` | `JobRequestWorkflowTest::test_rf04_*` (2) | E2E-03 (rechazo sin motivo impedido); la notificación se verifica en PHPUnit | Implementado |
| RF-05 | Registrar perfil y criterios | RR. HH. | `VacancyController`, `VacancyService::create/update` | `vacancies/create`, `vacancies/edit` (`vacancy-form`) | `VacancyPublicationTest::test_rf05_*` (2) | E2E-04, E2E-13 | Implementado |
| RF-06 | Configurar y validar vacante | RR. HH. | `VacancyValidator` | Lista de validación en `vacancies/show` | `VacancyPublicationTest::test_rf05_rf06_*`, `test_rf06_*` | E2E-04 | Implementado |
| RF-07 | Publicar vacante | RR. HH. | `VacancyPublicationController`, `VacancyService::publish`, `PublicVacancyController` | `vacancies/show`, `jobs/index`, `jobs/show` | `VacancyPublicationTest::test_rf07_*` (3) | E2E-04, E2E-13 | Implementado |
| RF-08 | Gestionar cuenta y acceso del postulante | Postulante | Fortify + `CreateNewUser` (rol postulante) | `auth/register`, `auth/login` | `CandidateRegistrationTest` (3), `AuthenticationTest` | E2E-01, E2E-05 | Implementado |
| RF-09 | Gestionar perfil y CV | Postulante | `CandidateProfileController`, `CandidateCvController`, `CandidateProfileService`, `CandidateDocumentPolicy` | `candidate/profile` | `CandidateProfileTest::test_rf09_*` (5) | E2E-05, E2E-13 | Implementado |
| RF-10 | Registrar postulación | Postulante | `ApplyController`, `ApplicationService::apply` | Panel de postulación en `jobs/show` | `ApplyToVacancyTest::test_rf10_*` (5), `VacancyClosureTest` | E2E-05, E2E-12 (vacante cerrada), E2E-13 | Implementado |
| RF-11 | Confirmar postulación | Sistema → Postulante | `ApplicationReceivedNotification` | `candidate/applications/*`, `notifications/index` | `ApplyToVacancyTest::test_rf10_rf11_*` | E2E-05 | Implementado |
| RF-12 | Consultar y revisar postulaciones | RR. HH. | `VacancyApplicationController`, `ApplicationController`, `ApplicationPolicy` | `applications/index`, `applications/show` | `ApplicationReviewTest::test_rf12_*` (2) | E2E-06 | Implementado |
| RF-13 | Registrar preselección o descarte | RR. HH. | `ApplicationStageController` (`shortlist`, `discard`), `ApplicationStageService` | Panel de etapas en `applications/show` | `ApplicationReviewTest::test_rf13_*` (2), `SelectionRegistrationTest::test_rf24_manual_stage_changes_are_blocked_after_the_final_decision` | E2E-06 | Implementado |
| RF-14 | Gestionar cambio de etapa | RR. HH. | `ApplicationStageController::change`, `ApplicationStageService::moveTo`, `ApplicationStatus` | `applications/show` | `ApplicationReviewTest::test_rf14_*` (3), `ApplicationStatusTest` (unitaria) | E2E-06, E2E-13 | Implementado |
| RF-15 | Notificar cambio de etapa | Sistema → Postulante | `ApplicationStageChangedNotification` | `notifications/index`, `candidate/applications/show` | `ApplicationReviewTest::test_rf13_rf15_*` | E2E-06 | Implementado |
| RF-16 | Programar evaluación | RR. HH. | `AssessmentScheduleController::evaluation`, `AssessmentScheduler::scheduleEvaluation`, `EvaluationPolicy` | Panel «Evaluaciones» en `applications/show` | `EvaluationTest::test_rf16_*` (5) | E2E-13 | Implementado |
| RF-17 | Generar convocatoria de evaluación | Sistema → Postulante y Evaluador | `AssessmentConvocationNotification`, `AssessmentAssignedNotification` | `notifications/index`, «Convocatorias» en `candidate/applications/show` | `EvaluationTest::test_rf16_rf17_*`, `InterviewTest::test_rf18_*` | E2E-13 (programación); el contenido de la convocatoria se verifica en PHPUnit | Implementado |
| RF-18 | Programar entrevista | RR. HH. | `AssessmentScheduleController::interview`, `AssessmentScheduler::scheduleInterview`, `InterviewPolicy` | Panel «Entrevistas» en `applications/show` | `InterviewTest::test_rf18_*` (2), `VacancyClosureTest` | E2E-13 | Implementado |
| RF-19 | Registrar entrevista y resultado | Evaluador | `EvaluationController`, `InterviewController`, `AssessmentResultRecorder` | `assessments/index`, `assessments/show` | `InterviewTest::test_rf19_*` (2), `EvaluationTest` | E2E-07, E2E-13 | Implementado |
| RF-20 | Validar rangos y ponderaciones | Sistema (RR. HH. configura) | `WeightingValidator`, `ScoreSheetValidator`, `RankingService` | Suma de ponderaciones en `vacancy-form`, rangos en `assessments/show`, error en `selection/comparison` | `WeightingValidatorTest`, `ScoreSheetValidatorTest` (unitarias), `RankingServiceTest::test_rf20_*` (5), `EvaluationTest::test_rf20_*`, `InterviewTest::test_rf20_*`, `RankingComparisonTest::test_rf20_*`, `CrossTenantAccessTest::test_rf20_*` | E2E-04 (ponderaciones), E2E-07 (rango) | Implementado |
| RF-21 | Calcular ranking configurable | Sistema | `RankingService`, `VacancyRankingBuilder` | `selection/comparison` | `RankingServiceTest::test_rf21_*` (9), `RankingComparisonTest::test_rf21_*` (4) | E2E-08, E2E-13 | Implementado |
| RF-22 | Presentar comparación de candidatos | RR. HH., Aprobador / Dirección | `VacancyComparisonController`, `RankingPresenter`, `VacancyPolicy::viewRanking` | `selection/comparison` | `RankingComparisonTest::test_rf21_rf22_*`, `test_rf22_*` (2) | E2E-08 | Implementado |
| RF-23 | Registrar decisión final de selección (**humana**) | Aprobador / Dirección | `FinalDecisionController`, `FinalDecisionService`, `FinalDecisionRequest`, `VacancyPolicy::decide` | Panel «Decisión final» en `selection/comparison` | `FinalDecisionTest::test_rf23_*` (10), `RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate` | E2E-09, E2E-12 (no autorizado), E2E-13 | Implementado |
| RF-24 | Registrar selección del candidato | RR. HH. | `SelectionRegistrationController`, `SelectionRegistrationService`, índice `applications_one_selected_per_vacancy` | Botón «Registrar selección» en `selection/comparison` | `SelectionRegistrationTest::test_rf24_*` (7) | E2E-10, E2E-12 (tras el cierre), E2E-13 | Implementado |
| RF-25 | Cerrar vacante o convocatoria (con selección; A-30) | RR. HH. | `VacancyClosureController`, `VacancyClosureService`, `CloseVacancyRequest`, `VacancyPolicy::close` | Panel «Cerrar convocatoria» en `selection/comparison` | `VacancyClosureTest::test_rf25_*` (5), `ApplicationStatusTest` | E2E-10, E2E-12, E2E-13 | Implementado (cierre sin selección fuera de la línea base) |
| RF-26 | Notificar resultado y cierre | Sistema → Postulantes | `ProcessResultNotification` (enviada por `VacancyClosureService`) | `notifications/index` | `ProcessResultNotificationTest::test_rf26_*` (8) | E2E-10, E2E-13 | Implementado |
| RF-27 | Generar registro de auditoría | Sistema; consulta: Aprobador / Dirección | `AuditLogger`, `AuditLog`, *trigger* `audit_logs_append_only`, `AuditLogController`, `AuditLogPolicy`, `AuditLogResource` | `audit/index` | `AuditTrailTest::test_rf27_*` (5), `AuditLogViewTest::test_rf27_*` (7), `AuditLoggerTest`, `OrganizationScopeTest` | E2E-11, E2E-13 | Implementado |

## Resumen

| Indicador | Valor |
|---|---|
| RF en la línea base | 27 |
| RF implementados | 27 (100 %) |
| RF con pruebas PHPUnit | 27 (100 %). RF-08 se cubre con `CandidateRegistrationTest`/`AuthenticationTest`; los otros 26 tienen además pruebas nombradas `test_rfNN_*`. |
| RF ejercidos por Cypress | 27 (100 %); al menos E2E-13 recorre el flujo completo. RF-04 y RF-17 verifican parte del comportamiento solo en PHPUnit (indicado en la tabla). |
| Specs E2E | 14 (E2E-01 a E2E-13 + `e2e-00` de soporte), 43 tests |

La columna Cypress indica los specs que ejercen cada RF. Que un RF esté ejercido no equivale a cobertura porcentual, que **no fue medida**.
