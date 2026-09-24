# Trazabilidad UML ↔ RF ↔ código ↔ pruebas

**Fase 22 · base `aced6da`.** Une cada requerimiento con los elementos UML que lo representan, la clase, el código que lo implementa y la prueba que lo respalda. Las rutas y nombres se verificaron en el repositorio; la columna de pruebas cita archivos existentes en `tests/`, `ml-service/tests/` y `cypress/e2e/`. Complementa, sin sustituir, [`docs/rf-implementation-matrix.md`](../../rf-implementation-matrix.md) y [`docs/final-report/traceability-master.md`](../../final-report/traceability-master.md), que siguen siendo la matriz de v1.0.

Abreviaturas UML: UC = caso de uso ([`use-cases.md`](use-cases.md)), CL = clase ([`class-model.md`](class-model.md)), SEQ ([`sequence-diagrams.md`](sequence-diagrams.md)), AC ([`activity-diagrams.md`](activity-diagrams.md)), ST ([`state-diagrams.md`](state-diagrams.md)), CO ([`component-model.md`](component-model.md)).

## 1. Matriz

| RF | Elementos UML | Clase(s) | Ruta · controlador · servicio | Pruebas (PHPUnit · Cypress) |
|---|---|---|---|---|
| RF-01 | UC-RF01 · AC-01 #1 · ST-01 | `JobRequest` | `job-requests.store` · `JobRequestController` · `JobRequestWorkflow::register` | `JobRequestWorkflowTest` · E2E-02 |
| RF-02 | UC-RF02 · AC-01 #2 · ST-01 | `JobRequest`, `JobRequestStatusHistory` | `job-requests.submit/observe/validate/update` · `JobRequestTransitionController` · `submit`, `observe`, `validate`, `correct` | `JobRequestWorkflowTest`, `Unit/Enums/JobRequestStatusTest` · E2E-02 |
| RF-03 | UC-RF03 · SEQ-02 · ST-01 | `JobRequest` | `job-requests.decide` · `JobRequestTransitionController::decide` · `approve`, `reject` | `JobRequestWorkflowTest`, `CrossTenantAccessTest` · E2E-03 |
| RF-04 | UC-RF04 (`<<extend>>`) · SEQ-02 | — (notificación) | `JobRequestRejectedNotification` | `JobRequestWorkflowTest::test_rf04_rejection_notifies_the_requester` · E2E-03 |
| RF-05 | UC-RF05 · AC-01 #4 · ST-02 | `Vacancy`, `JobProfile`, `EvaluationCriterion` | `vacancies.store/update` · `VacancyController` · `VacancyService::create/update` | `VacancyPublicationTest` · E2E-04 |
| RF-06 | UC-RF06 · AC-01 #5 | `Vacancy` (`target_completion_at` desde F16) | `VacancyValidator` | `VacancyPublicationTest`, `Ml/TargetCompletionTest` · E2E-04, E2E-14 |
| RF-07 | UC-RF07 (actor: **RR. HH.**; la consulta pública va como nota) · ST-02 | `Vacancy` | `vacancies.publish` · `VacancyPublicationController` · `VacancyService::publish`; `jobs.index/show` · `PublicVacancyController` | `VacancyPublicationTest` · E2E-04 |
| RF-08 | UC-RF08 | `User` (`postulante`) | Fortify `register` · `CreateNewUser` | `Auth/CandidateRegistrationTest`, `Auth/AuthenticationTest`, `Auth/RoleMiddlewareTest` · E2E-01, E2E-05 |
| RF-09 | UC-RF09 | `CandidateProfile`, `CandidateDocument` | `candidate.profile.update`, `candidate.cv.store` · `CandidateProfileService` | `Candidates/CandidateProfileTest` · E2E-05 |
| RF-10 | UC-RF10 · SEQ-01 · ST-03 | `Application`, `ApplicationStageHistory` | `jobs.apply` · `ApplyController` · `ApplicationService::apply` | `Applications/ApplyToVacancyTest`, `Selection/VacancyClosureTest` · E2E-05, E2E-12 |
| RF-11 | UC-RF11 (`<<include>>`) · SEQ-01 | — (notificación) | `ApplicationReceivedNotification` | `ApplyToVacancyTest` · E2E-05 |
| RF-12 | UC-RF12 | `Application` | `vacancies.applications.index`, `applications.show` · `VacancyApplicationController`, `ApplicationController` | `Applications/ApplicationReviewTest` · E2E-06 |
| RF-13 | UC-RF13 · SEQ-03 · ST-03 | `Application` | `applications.shortlist/discard` · `ApplicationStageService::shortlist/discard` | `ApplicationReviewTest`, `SelectionRegistrationTest` · E2E-06 |
| RF-14 | UC-RF14 · SEQ-03 · ST-03 | `Application`, `ApplicationStageHistory` | `applications.stage` · `ApplicationStageService::moveTo` | `ApplicationReviewTest`, `Unit/Enums/ApplicationStatusTest` · E2E-06 |
| RF-15 | UC-RF15 (`<<include>>`) · SEQ-03 | — (notificación) | `ApplicationStageChangedNotification` | `ApplicationReviewTest` · E2E-06 |
| RF-16 | UC-RF16 · SEQ-04 · ST-04 · CL-01 asociaciones 24 (`evaluator`) y 36 (`scheduler`) | `Evaluation` (`scheduled_by` = quien programó; `evaluator_id` = evaluador asignado) | `applications.evaluations.store` · `AssessmentScheduleController::evaluation` · `AssessmentScheduler::scheduleEvaluation` | `Assessments/EvaluationTest` |
| RF-17 | UC-RF17 (`<<include>>`) · SEQ-04, SEQ-05 | — (notificaciones) | `AssessmentConvocationNotification`, `AssessmentAssignedNotification` | `EvaluationTest`, `Assessments/InterviewTest` |
| RF-18 | UC-RF18 · SEQ-05 · ST-04 · CL-01 asociaciones 25 (`evaluator`) y 37 (`scheduler`) | `Interview` (`scheduled_by` = quien programó; `evaluator_id` = evaluador asignado) | `applications.interviews.store` · `AssessmentScheduler::scheduleInterview` | `InterviewTest`, `VacancyClosureTest` |
| RF-19 | UC-RF19 · SEQ-05 · ST-04 | `EvaluationResult`, `InterviewResult` | `evaluations.results.store`, `interviews.results.store` · `AssessmentResultRecorder` | `InterviewTest`, `EvaluationTest` · E2E-07 |
| RF-20 | UC-RF20 · SEQ-05, SEQ-06 | `EvaluationCriterion` | `WeightingValidator`, `ScoreSheetValidator`, `RankingService` | `Unit/Evaluation/WeightingValidatorTest`, `Unit/Assessments/ScoreSheetValidatorTest`, `Unit/Ranking/RankingServiceTest` · E2E-04, E2E-07 |
| RF-21 | UC-RF21 · SEQ-06 · CO «Cálculo de ranking» | — (no persistente) | `VacancyRankingBuilder`, `RankingService` | `RankingServiceTest`, `Selection/RankingComparisonTest` · E2E-08 |
| RF-22 | UC-RF22 · SEQ-06 | — | `vacancies.comparison` · `VacancyComparisonController` · `RankingPresenter` | `RankingComparisonTest` · E2E-08 |
| RF-23 | UC-RF23 `<<human decision>>` · SEQ-07 · AC-01 #17 | `SelectionDecision` | `vacancies.decision.store` · `FinalDecisionController` · `FinalDecisionService`, `FinalDecisionRequest` | `Selection/FinalDecisionTest`, `RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate` · E2E-09, E2E-12 |
| RF-24 | UC-RF24 · ST-03 | `SelectionDecision`, `Application` | `vacancies.selection.store` · `SelectionRegistrationService` | `Selection/SelectionRegistrationTest` · E2E-10, E2E-12 |
| RF-25 | UC-RF25 · ST-02, ST-03 | `Vacancy`, `Application` | `vacancies.close` · `VacancyClosureController` · `VacancyClosureService` | `VacancyClosureTest`, `ApplicationStatusTest` · E2E-10, E2E-12 |
| RF-26 | UC-RF26 (`<<include>>`) | — (notificación) | `ProcessResultNotification` | `Notifications/ProcessResultNotificationTest` · E2E-10 |
| RF-27 | UC-RF27 · nota transversal en UC-01, SEQ y AC-01 · CO «Auditoría» | `AuditLog` | `AuditLogger::record`; `audit.index` · `AuditLogController` | `Audit/AuditLoggerTest`, `Audit/AuditLogViewTest`, `Audit/AuditTrailTest` · E2E-11 |
| RF-28 | UC-RF28 `<<propuesto v1.1>>` | — | **No implementado** | — |
| RF-29 | UC-RF29 `<<experimental>>` · SEQ-08 · AC-02 · CO «Riesgo operacional» + «Servicio de inferencia» · DE-01 | `Vacancy` (`target_completion_at`); nada persistente propio | `vacancies.operational-risk` · `VacancyOperationalRiskController` · `OperationalRiskService`, `OperationalRiskFeatureBuilder`, `MlRiskClient`; FastAPI `POST /v1/predict` | `tests/Feature/Ml/*` (8 archivos, incluido `MlCrossTenantValidationTest`); `ml-service/tests/test_api_service.py`, `test_api_security.py`, `test_freeze_contract.py` · E2E-15 |

**Multiempresa** (transversal): CL-01 `<<tenant scoped>>` · `BelongsToOrganization`, `OrganizationScope`, Policies · `Tenancy/CrossTenantAccessTest`, `Tenancy/OrganizationScopeTest`, `Ml/MlCrossTenantValidationTest` · E2E-11.

## 2. Roles y permisos (según Policies y *middleware*)

«Misma org.» = la Policy exige además `sharesOrganizationWith`. Leído de `app/Policies/*` y `routes/web.php`, no deducido del nombre del actor.

| Acción | Solicitante | RR. HH. | Aprobador | Evaluador | Postulante | Fuente |
|---|---|---|---|---|---|---|
| Ver requerimientos | Propios | No borradores, misma org. | No borradores, misma org. | — | — | `JobRequestPolicy::view` |
| Registrar, corregir, enviar (RF-01/02) | Dueño | — | — | — | — | `create`, `update`, `submit` |
| Observar o validar (RF-02) | — | Misma org. | — | — | — | `review` |
| Aprobar o rechazar (RF-03) | — | — | Misma org. | — | — | `decide` |
| Consultar vacantes publicadas (efecto de RF-07, no el caso «Publicar») | Sí | Sí | Sí | Sí | Sí, **también sin sesión** | Rutas públicas `jobs.index`, `jobs.show` (fuera del grupo `auth`) |
| Ver vacantes internas | — | Misma org. | Misma org. | — | — | `VacancyPolicy::view` |
| Crear, configurar, publicar (RF-05–07) | — | Misma org. | — | — | — | `create`, `update`, `publish` |
| Ver postulaciones (RF-12) | — | Misma org. | Misma org. | — | Las propias | `ApplicationPolicy::view`, `viewAnyForVacancy` |
| Postular (RF-10) | — | — | — | — | Sí | `apply` |
| Perfil y CV (RF-09) | — | — | — | — | Propios | *middleware* `role:postulante` |
| Cambiar etapa (RF-13/14) | — | Misma org. | — | — | — | `changeStage` |
| Programar sesiones (RF-16/18) | — | Misma org. | — | — | — | `scheduleAssessment` |
| Ver sesión | — | Misma org. | Misma org. | Asignado | — | `canViewSession` |
| Registrar resultados (RF-19) | — | — | — | **Asignado**, misma org. | — | `recordResult` |
| Ranking y comparación (RF-21/22) | — | Misma org. | Misma org. | — | — | `viewRanking` |
| **Decisión final (RF-23)** | — | — | **Misma org.** | — | — | `VacancyPolicy::decide` |
| Registrar selección y cerrar (RF-24/25) | — | Misma org. | — | — | — | `registerSelection`, `close` |
| Riesgo operacional (RF-29) | — | Misma org. | Misma org. | — | — | `viewOperationalRisk` |
| Auditoría (RF-27) | — | — | Con organización | — | — | `AuditLogPolicy::viewAny` |
| Descargar CV | — | Si el postulante postuló en su org. | Si el postulante postuló en su org. | Si tiene sesión asignada con él | El suyo | `CandidateDocumentPolicy::download` |
| Mis evaluaciones | — | — | — | Sí | — | *middleware* `role:evaluador` |

## 3. Discrepancias encontradas en el cruce con el código

| # | Hallazgo | Tratamiento |
|---|---|---|
| D-01 | El catálogo describe RF-28 como fallback descriptivo; lo implementado en `descriptive_only` es solo un mensaje de la tarjeta de RF-29, no el panel agregado de RF-28 | RF-28 como **candidato no implementado** en UC-01 |
| D-02 | RF-17 se llama «convocatoria de evaluación», pero la implementación convoca también a entrevistas | UC-RF18 también incluye UC-RF17; nota en el caso |
| D-03 | `VacancyClosureType::Deserted` existe sin flujo | Nota en CL-01 y ST-02; no se dibuja transición |
| D-04 | La descripción OpenAPI de `days_remaining_to_target` sigue diciendo que Laravel no puede producirla | Deuda de texto en `ml-service`; GAP-01 se modela **resuelto** |
| D-05 | El diagrama de casos de uso de v1.0 atribuye RF-20 al Evaluador | En v1.1 RF-20 es un caso del sistema incluido por RF-06, RF-19 y RF-21 |
| D-06 | El despliegue original de v1.0 incluía S3 | No se modela: los CV van al disco local privado |
