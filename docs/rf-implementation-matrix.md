# Matriz de implementación de RF

Estado al cierre de la Fase 8 (2026-09-13, rama `feature/frontend-integral`). Solo información verificada. "Test" se refiere a PHPUnit; la suite E2E de Cypress aún no está configurada.

**Validación en navegador (Fase 8):** RF-01 a RF-27 se recorrieron por la interfaz con los roles reales en un flujo integral de 12 pasos (12/12 OK) y en un recorrido visual por rol (10/10 OK, 49 capturas). Ver `docs/manual-smoke-test.md`. Las correcciones de interfaz afectan la presentación de fechas (DEF-09), el detalle de RF-27 (DEF-10) y los avatares (DEF-11), sin cambios en reglas de negocio.

| RF | Nombre | Backend | Frontend | Test | Estado |
|---|---|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | `JobRequestWorkflow::register` | `job-requests/create` | `JobRequestWorkflowTest` | Implementado |
| RF-02 | Validar y corregir requerimiento | `observe`, `validate`, `correct`, `submit` | `job-requests/show`, `edit` | `JobRequestWorkflowTest` | Implementado |
| RF-03 | Registrar aprobación o rechazo | `approve`, `reject` | Panel de decisión en `job-requests/show` | `JobRequestWorkflowTest`, `CrossTenantAccessTest` | Implementado |
| RF-04 | Notificar rechazo | `JobRequestRejectedNotification` | `notifications/index` | `test_rf04_rejection_notifies_the_requester` | Implementado |
| RF-05 | Registrar perfil y criterios | `VacancyService::create/update` | `vacancies/create`, `edit` | `VacancyPublicationTest` | Implementado |
| RF-06 | Configurar y validar vacante | `VacancyValidator` | Checklist en `vacancies/show` | `VacancyPublicationTest` | Implementado |
| RF-07 | Publicar vacante | `VacancyService::publish`, `PublicVacancyController` | `vacancies/show`, `jobs/index`, `jobs/show` | `VacancyPublicationTest` | Implementado |
| RF-08 | Gestionar cuenta y acceso del postulante | Fortify + `CreateNewUser` (rol postulante) | `auth/register`, `auth/login` | `CandidateRegistrationTest`, `AuthenticationTest` | Implementado |
| RF-09 | Gestionar perfil y CV | `CandidateProfileService` | `candidate/profile` | `CandidateProfileTest` | Implementado |
| RF-10 | Registrar postulación | `ApplicationService::apply` | Panel de postulación en `jobs/show` | `ApplyToVacancyTest`, `VacancyClosureTest` (postular tras cierre) | Implementado |
| RF-11 | Confirmar postulación | `ApplicationReceivedNotification` | `candidate/applications/*`, `notifications/index` | `ApplyToVacancyTest` | Implementado |
| RF-12 | Consultar y revisar postulaciones | `VacancyApplicationController`, `ApplicationController` | `applications/index`, `applications/show` | `ApplicationReviewTest` | Implementado |
| RF-13 | Registrar preselección o descarte | `ApplicationStageService::shortlist/discard` (bloqueado tras la decisión final, A-28) | `applications/show` | `ApplicationReviewTest`, `SelectionRegistrationTest` | Implementado |
| RF-14 | Gestionar cambio de etapa | `ApplicationStageService::moveTo` + `ApplicationStatus` | `applications/show` | `ApplicationReviewTest`, `ApplicationStatusTest` | Implementado |
| RF-15 | Notificar cambio de etapa | `ApplicationStageChangedNotification` | `notifications/index` | `ApplicationReviewTest` | Implementado |
| RF-16 | Programar evaluación | `AssessmentScheduler::scheduleEvaluation` | Panel «Evaluaciones» en `applications/show` | `EvaluationTest` | Implementado |
| RF-17 | Generar convocatoria de evaluación | `AssessmentConvocationNotification`, `AssessmentAssignedNotification` | `notifications/index`, «Convocatorias» en `candidate/applications/show` | `EvaluationTest`, `InterviewTest` | Implementado |
| RF-18 | Programar entrevista | `AssessmentScheduler::scheduleInterview` | Panel «Entrevistas» en `applications/show` | `InterviewTest`, `VacancyClosureTest` (bloqueo tras cierre) | Implementado |
| RF-19 | Registrar entrevista y resultado | `AssessmentResultRecorder` | `assessments/index`, `assessments/show` | `InterviewTest`, `EvaluationTest` | Implementado |
| RF-20 | Validar rangos y ponderaciones | `WeightingValidator` (configuración, publicación y entrada del ranking), `ScoreSheetValidator` (registro de resultados y puntajes usados en el ranking), `RankingService` rechaza configuración inválida, puntajes fuera de rango y criterios ajenos a la vacante | Suma de ponderaciones en `vacancy-form`; rangos en `assessments/show`; error de configuración en `selection/comparison` | `WeightingValidatorTest`, `ScoreSheetValidatorTest`, `RankingServiceTest` (`rf20_*`), `RankingComparisonTest::test_rf20_…`, `CrossTenantAccessTest::test_rf20_…` | Implementado |
| RF-21 | Calcular ranking configurable | `RankingService` (puro, determinista, explicable; empates marcados), `VacancyRankingBuilder` (misma vacante y organización) | `selection/comparison` | `RankingServiceTest`, `RankingComparisonTest` | Implementado |
| RF-22 | Presentar comparación de candidatos | `VacancyComparisonController`, `RankingPresenter` | `selection/comparison` (criterios, ponderaciones, promedios, aportes, total, posición); enlace en `vacancies/show` | `RankingComparisonTest` | Implementado |
| RF-23 | Registrar decisión final de selección | `FinalDecisionService`, `FinalDecisionRequest` (confirmación humana y justificación), `VacancyPolicy::decide` | Panel «Decisión final» y resumen en `selection/comparison` | `FinalDecisionTest`, `RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate` | Implementado |
| RF-24 | Registrar selección del candidato | `SelectionRegistrationService`, `VacancyPolicy::registerSelection`, índice único parcial `applications_one_selected_per_vacancy` | Botón «Registrar selección» en `selection/comparison` | `SelectionRegistrationTest` | Implementado |
| RF-25 | Cerrar vacante o convocatoria | `VacancyClosureService`, `CloseVacancyRequest`, `VacancyPolicy::close` (cierre con selección; sin selección no implementado, A-30) | Panel «Cerrar convocatoria» y resumen de cierre en `selection/comparison` | `VacancyClosureTest`, `ApplicationStatusTest` | Implementado (cierre sin selección no disponible por falta de TO-BE) |
| RF-26 | Notificar resultado y cierre | `ProcessResultNotification` (database + mail log) enviada por `VacancyClosureService` solo al cerrar; auditoría `proceso.resultado_notificado` | `notifications/index` del postulante | `ProcessResultNotificationTest` | Implementado |
| RF-27 | Generar registro de auditoría | `AuditLogger` (redacción ampliada), `audit_logs` de solo inserción (trigger PostgreSQL), 23 acciones de negocio auditadas, `AuditLogPolicy`, `AuditLogController`, `AuditLogResource` (resumen seguro con etiquetas legibles y fechas locales, DEF-10) | `audit/index` (Aprobador / Dirección) | `AuditLoggerTest`, `AuditTrailTest`, `AuditLogViewTest`, `OrganizationScopeTest` | Implementado |

**RF-01 a RF-27 constituyen la línea base funcional completa del proyecto.** No se han agregado RF fuera de esta línea base.
