# Inventario arquitectónico AS-IS

**Fase 22 · 23/09/2026 · base `develop` = `aced6da`.** Todo lo que sigue se leyó en el código de esta revisión, no en documentación previa. Es la fuente de los diagramas de esta carpeta: si un diagrama contradice este inventario, el diagrama está mal.

Marcas: **[AS-IS]** implementado y probado · **[EXP]** implementado como experimental · **[CAND]** candidato o propuesta, no implementado · **[DEUDA]** restricción o deuda conocida.

---

## 1. Actores

Los roles son exactamente los cinco de `app/Enums/UserRole.php`, replicados en el `CHECK users_role_valid`. **No existe** administrador del SaaS, administrador de organización, superusuario ni un rol «Entrevistador».

| Actor | Rol (`users.role`) | Organización | Responsabilidad | RF |
|---|---|---|---|---|
| Área solicitante | `solicitante` | Obligatoria | Registra, corrige y envía sus propios requerimientos | RF-01, RF-02 |
| Recursos Humanos | `rrhh` | Obligatoria | Valida u observa requerimientos; configura y publica vacantes; revisa postulaciones y cambia etapas; programa evaluaciones y entrevistas; registra la selección y cierra | RF-02, RF-05–RF-07, RF-12–RF-18, RF-20–RF-22, RF-24, RF-25, RF-29 |
| Aprobador / Dirección | `aprobador` | Obligatoria | Aprueba o rechaza requerimientos; consulta postulaciones y ranking; **registra la decisión final humana**; consulta la auditoría | RF-03, RF-12, RF-21, RF-22, RF-23, RF-27, RF-29 |
| Evaluador | `evaluador` | Obligatoria | Registra los resultados de las evaluaciones **y de las entrevistas** que tiene asignadas | RF-19, RF-20 |
| Postulante | `postulante` | **Ninguna** (cuenta global) | Crea su cuenta, mantiene perfil y CV, postula y consulta sus postulaciones | RF-08–RF-11 |
| Servicio de riesgo operacional | — (sistema externo) | — | Actor secundario **técnico** de RF-29: recibe features operacionales y devuelve una estimación | RF-29 [EXP] |

Precisiones verificadas:

- **Entrevistador**: no es un rol. La entrevista tiene `evaluator_id` y la registra el Evaluador asignado (`InterviewPolicy::recordResult` → `isAssignedEvaluator`).
- **Visitante sin sesión**: consulta la portada y las vacantes publicadas (`/`, `/empleos`, `/empleos/{id}`) y puede registrarse. No es un rol: en UML se trata como el Postulante antes de autenticarse (RF-07 consulta pública, RF-08 registro).
- `CHECK users_role_organization`: el postulante tiene `organization_id` nulo; el personal, obligatorio.
- Las cuentas de personal no se autorregistran: `CreateNewUser` (Fortify) crea solo postulantes. El personal existe por *seeders*.

## 2. Módulos del monolito

Laravel es un **monolito modular por carpetas**, no por paquetes: cada módulo reparte sus piezas entre `Http/Controllers/<Módulo>`, `Http/Requests/<Módulo>`, `Services/<Módulo>` y los modelos compartidos.

| Módulo | Controladores | Servicios | RF |
|---|---|---|---|
| Requerimientos | `JobRequests/JobRequestController`, `JobRequestTransitionController` | `JobRequestWorkflow` | RF-01–RF-04 |
| Vacantes | `Vacancies/VacancyController`, `VacancyPublicationController`, `PublicVacancyController` | `VacancyService`, `VacancyValidator` | RF-05–RF-07 |
| Postulantes | `Candidates/ApplyController`, `CandidateProfileController`, `CandidateCvController`, `CandidateApplicationController`, `Documents/CandidateDocumentDownloadController` | `CandidateProfileService`, `ApplicationService` | RF-08–RF-11 |
| Postulaciones | `Applications/VacancyApplicationController`, `ApplicationController`, `ApplicationStageController` | `ApplicationStageService` | RF-12–RF-15 |
| Evaluaciones y entrevistas | `Assessments/AssessmentScheduleController`, `AssessmentAssignmentController`, `EvaluationController`, `InterviewController` | `AssessmentScheduler`, `AssessmentResultRecorder`, `ScoreSheetValidator` | RF-16–RF-19 |
| Ranking y selección | `Selection/VacancyComparisonController`, `FinalDecisionController`, `SelectionRegistrationController`, `VacancyClosureController` | `WeightingValidator`, `RankingService`, `VacancyRankingBuilder`, `FinalDecisionService`, `SelectionRegistrationService`, `VacancyClosureService` | RF-20–RF-26 |
| Auditoría | `Audit/AuditLogController` | `AuditLogger` | RF-27 |
| Notificaciones | `NotificationController` | 6 notificaciones sobre `RecruitmentNotification` | RF-04, RF-11, RF-15, RF-17, RF-26 |
| Riesgo operacional [EXP] | `Vacancies/VacancyOperationalRiskController` | `OperationalRiskService`, `OperationalRiskFeatureBuilder`, `MlRiskClient` | RF-29 |
| Cuenta y acceso | Fortify, `Settings/*` | `CreateNewUser`, `ResetUserPassword` | RF-08 |
| Transversal | — | `SequentialCodeGenerator`, `OrganizationScope`, `BelongsToOrganization`, `EnsureUserHasRole` | — |

Fuera del dominio y fuera de UML: `HealthController` (`/health`, *healthcheck* de Docker) y `Testing/*` + `E2eEnvironment` (rutas `__e2e`, inertes salvo en el entorno E2E).

## 3. Entidades persistentes

17 modelos Eloquent en `app/Models`. **13 llevan `BelongsToOrganization`** (global scope `OrganizationScope` + `organization_id` asignado al crear); 4 no.

| Modelo | Tabla | Tenant | Estado (enum) |
|---|---|---|---|
| `Organization` | `organizations` | Raíz | — |
| `User` | `users` | `organization_id` **nulo para postulantes** | `role: UserRole` |
| `JobRequest` | `job_requests` | Sí | `JobRequestStatus` |
| `JobRequestStatusHistory` | `job_request_status_histories` | Sí | — |
| `Vacancy` | `vacancies` | Sí | `VacancyStatus`, `VacancyClosureType` |
| `JobProfile` | `job_profiles` | Sí | — |
| `EvaluationCriterion` | `evaluation_criteria` | Sí | `stage: CriterionStage` |
| `CandidateProfile` | `candidate_profiles` | **No** (global) | — |
| `CandidateDocument` | `candidate_documents` | **No** (global) | `type: DocumentType` |
| `Application` | `applications` | Sí | `ApplicationStatus` |
| `ApplicationStageHistory` | `application_stage_histories` | Sí | — |
| `Evaluation` | `evaluations` | Sí | `AssessmentStatus`, `EvaluationType` |
| `EvaluationResult` | `evaluation_results` | Sí | — |
| `Interview` | `interviews` | Sí | `AssessmentStatus`, `InterviewOutcome` |
| `InterviewResult` | `interview_results` | Sí | — |
| `SelectionDecision` | `selection_decisions` | Sí | — |
| `AuditLog` | `audit_logs` | Sí (nulo para acciones de cuentas globales) | `action: AuditAction` |

Tablas del *framework* que no son dominio: `sessions`, `cache`, `jobs`, `failed_jobs`, `password_reset_tokens`, `passkeys` y `notifications` (canal `database`, polimórfica sobre `User`).

**No se persiste**: el ranking (se calcula en memoria en cada consulta; solo su instantánea queda en `SelectionDecision`) ni la estimación de riesgo operacional (se calcula en cada consulta y solo deja una línea en el *log* de la aplicación).

## 4. Máquinas de estado

Definidas con `allowedTransitions()` en el enum y replicadas en `CHECK` de PostgreSQL.

| Enum | Estados | Transiciones |
|---|---|---|
| `JobRequestStatus` | `borrador`, `enviado`, `observado`, `validado`, `aprobado`, `rechazado` | borrador→enviado; enviado→observado \| validado; observado→enviado; validado→aprobado \| rechazado |
| `VacancyStatus` | `borrador`, `publicada`, `cerrada` | borrador→publicada→cerrada |
| `ApplicationStatus` | `postulado`, `preseleccionado`, `en_evaluacion`, `en_entrevista`, `finalista`, `seleccionado`, `no_seleccionado`, `descartado` | Ver [`state-diagrams.md`](state-diagrams.md) |
| `AssessmentStatus` | `programada`, `realizada` | programada→realizada (sin enum de transiciones; lo impone el `CHECK` de coherencia con `completed_at`) |

## 5. Servicios transversales y almacenamiento

| Elemento | Implementación real |
|---|---|
| Auditoría | `AuditLogger::record()` desde cada servicio; 23 acciones en `AuditAction`; `audit_logs` de **solo inserción** por el *trigger* `audit_logs_append_only` |
| Notificaciones | 6 clases sobre `RecruitmentNotification` (`ShouldQueue`, `afterCommit`); canales `database` y `mail`; en desarrollo `MAIL_MAILER=log`: **no hay proveedor de correo** |
| Cola | Redis (`QUEUE_CONNECTION=redis`), consumida por el contenedor `queue` (`queue:work redis`) |
| Sesión y caché | Redis |
| CV | Disco `local` de Laravel = `storage/app/private`; descarga solo por `CandidateDocumentPolicy::download`. **No hay S3 ni almacenamiento en la nube** |
| Concurrencia | `DB::transaction` + `lockForUpdate()` en todas las transiciones de estado |
| Errores de negocio | `BusinessRuleException` (mensaje en español, nunca 500) |

## 6. Integración ML [EXP]

| Tramo | Real |
|---|---|
| Consulta | `GET vacantes/{vacancy}/riesgo-operacional` → JSON; la pide `OperationalRiskCard` después de cargar el detalle de la vacante |
| Autorización | `VacancyPolicy::viewOperationalRisk` = RR. HH. o Aprobador **de la misma organización** |
| Elegibilidad | `OperationalRiskService::outOfScopeReason`: 7 motivos → `descriptive_only` **sin llamar al servicio** |
| Checkpoint | Día siguiente a `closes_at`, inicio del día, zona horaria del proyecto |
| Features | `OperationalRiskFeatureBuilder` → 15 enteros operacionales |
| Cliente | `MlRiskClient`: `POST /v1/predict`, cabecera `X-Internal-Token`, timeout de conexión 1 s y total 3 s, 1 reintento; valida la respuesta |
| Servicio | FastAPI (`ml-service/src/recruitment_ml/api`), **fuera de Docker Compose**: proceso local con `uvicorn` en el puerto 8008, alcanzado desde el contenedor por `host.docker.internal` |
| Modelo | Artefacto `.joblib` + metadatos en `ml-service/artifacts/` (no versionado); al cargar se verifican SHA-256, *freeze* y versiones de librerías |
| Desactivado | `ML_SERVICE_ENABLED=false` por defecto → `descriptive_only` / `service_disabled` |

**Petición** (`PredictionRequest`, `extra="forbid"`, `strict=True`): exactamente estas 15 features enteras, sin identificadores ni PII:
`elapsed_days_since_publication`, `application_window_days`, `positions_count`, `applications_received_count`, `configured_criteria_count`, `evaluations_scheduled_count`, `evaluations_completed_count`, `evaluations_overdue_pending_count`, `interviews_scheduled_count`, `interviews_completed_count`, `interviews_overdue_pending_count`, `stage_transition_count`, `days_since_last_operational_event`, `concurrent_open_vacancies_count`, `days_remaining_to_target`.

**Respuesta** (`PredictionResponse`, `extra="forbid"`): `risk_score`, `risk_flag`, `threshold`, `model_version`, `freeze_fingerprint`, `status`. **Sin campo de incertidumbre.** Contrato científico congelado: *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`, *threshold* `0.1679418172266036`.

**Estados en la interfaz** (`RiskAvailability`): `predictive_available`, `descriptive_only`, `unavailable`.

## 7. Despliegue real (`docker-compose.yml`)

| Servicio | Imagen | Función |
|---|---|---|
| `app` | `reclutamiento-php:dev` (PHP 8.4, Node 22) | Laravel con `php artisan serve` en 8000; al arrancar ejecuta `composer install`, `npm ci`, `npm run build` y `migrate` |
| `queue` | `reclutamiento-php:dev` | `queue:work redis --tries=3` |
| `postgres` | `postgres:17.11-alpine` | Bases `reclutamiento`, `reclutamiento_testing`, `reclutamiento_e2e` |
| `redis` | `redis:7.4.11-alpine` | Sesiones, caché y colas |
| `app-e2e`, `queue-e2e`, `cypress` | perfil `e2e` | Entorno de pruebas aislado; no es parte del sistema en operación |

El frontend **no es un servidor aparte**: Vite compila React/TypeScript a `public/build` y Laravel lo sirve; Inertia entrega cada página desde el mismo proceso.

## 8. Frontend

React 19 + TypeScript + Inertia 3 + Tailwind 4. 31 páginas en `resources/js/pages` agrupadas por módulo (`job-requests`, `vacancies`, `applications`, `assessments`, `selection`, `audit`, `candidate`, `jobs`, `notifications`, `settings`, `auth`, `dashboard`, `welcome`). Componentes compartidos: `DataTable`, `Section`, `StatusBadge`, `StatusTimeline`, `WorkflowAlert`, formularios y `ui/*` (shadcn/Radix). La experiencia 3D de la Fase 20 es **presentación en la portada**, no un componente arquitectónico.

## 9. No implementado (fuera del UML AS-IS)

Administrador del SaaS o de organización · facturación y planes · *Talent Pool* · Meilisearch · IA en la nube · Kubernetes · proveedores cloud · PostgreSQL RLS · base de datos por tenant · S3 o almacenamiento en la nube · proveedor de correo real · WebGL / Three.js · ML en producción · microservicios generales · **RF-28** (panel operativo agregado) · cierre de vacante **desierta** (el valor `desierta` existe en `VacancyClosureType`, pero RF-25 solo implementa el cierre con selección, A-30).
