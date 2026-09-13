# Matriz de implementación de RF

Estado al checkpoint del 2026-09-13 (rama `feature/evaluations-interviews`). Solo información verificada. "Test" se refiere a PHPUnit; Cypress aún no está configurado.

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
| RF-10 | Registrar postulación | `ApplicationService::apply` | Panel de postulación en `jobs/show` | `ApplyToVacancyTest` | Implementado |
| RF-11 | Confirmar postulación | `ApplicationReceivedNotification` | `candidate/applications/*`, `notifications/index` | `ApplyToVacancyTest` | Implementado |
| RF-12 | Consultar y revisar postulaciones | `VacancyApplicationController`, `ApplicationController` | `applications/index`, `applications/show` | `ApplicationReviewTest` | Implementado |
| RF-13 | Registrar preselección o descarte | `ApplicationStageService::shortlist/discard` | `applications/show` | `ApplicationReviewTest` | Implementado |
| RF-14 | Gestionar cambio de etapa | `ApplicationStageService::moveTo` + `ApplicationStatus` | `applications/show` | `ApplicationReviewTest`, `ApplicationStatusTest` | Implementado |
| RF-15 | Notificar cambio de etapa | `ApplicationStageChangedNotification` | `notifications/index` | `ApplicationReviewTest` | Implementado |
| RF-16 | Programar evaluación | — | — | `EvaluationTest` (RED) | Pendiente |
| RF-17 | Generar convocatoria de evaluación | — | — | `EvaluationTest` (RED) | Pendiente |
| RF-18 | Programar entrevista | — | — | `InterviewTest` (RED) | Pendiente |
| RF-19 | Registrar entrevista y resultado | — | — | `InterviewTest` (RED) | Pendiente |
| RF-20 | Validar rangos y ponderaciones | `WeightingValidator` (configuración/publicación) | Suma de ponderaciones en `vacancy-form` | `WeightingValidatorTest`, `VacancyPublicationTest`; `ScoreSheetValidatorTest` (RED) | Parcial |
| RF-21 | Calcular ranking configurable | — | — | — | Pendiente |
| RF-22 | Presentar comparación de candidatos | — | — | — | Pendiente |
| RF-23 | Registrar decisión final de selección | — | — | — | Pendiente |
| RF-24 | Registrar selección del candidato | — | — | — | Pendiente |
| RF-25 | Cerrar vacante o convocatoria | — | — | — | Pendiente |
| RF-26 | Notificar resultado y cierre | — | — | — | Pendiente |
| RF-27 | Generar registro de auditoría | `AuditLogger`, `audit_logs` (usado en RF-01 a RF-15) | Sin vista de consulta | `AuditLoggerTest` y aserciones de auditoría en pruebas de flujo | Parcial |
