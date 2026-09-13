# Capítulo 6. Diseño del sistema

## 6.1 Arquitectura conceptual

Monolito modular SaaS multiempresa. El detalle tecnológico está en el [capítulo 7](07-arquitectura-tecnologica.md).

```mermaid
flowchart LR
    U[Usuarios por rol<br/>navegador] -->|HTTPS local / HTTP| W[React + Inertia<br/>páginas por módulo]
    W --> L[Laravel 13<br/>rutas, Form Requests, Policies]
    L --> S[Servicios de dominio<br/>requerimientos, vacantes, postulaciones,<br/>evaluaciones, ranking, selección, auditoría]
    S --> DB[(PostgreSQL 17<br/>datos por organization_id)]
    S --> R[(Redis 7<br/>sesiones, caché, colas)]
    R --> Q[Worker de colas<br/>notificaciones]
    Q --> DB
    S --> F[(Disco privado<br/>CV en PDF)]
```

## 6.2 Casos de uso

El catálogo CU-01 a CU-13 y su relación con los RF están en el [capítulo 4, sección 4.4](04-requerimientos.md#44-casos-de-uso).

## 6.3 Modelo de dominio (clases)

Modelos Eloquent reales (`app/Models`). Los que tienen `organization_id` usan el *trait* `BelongsToOrganization`.

```mermaid
classDiagram
    class Organization
    class User {
      role: solicitante|rrhh|aprobador|evaluador|postulante
    }
    class JobRequest {
      status: JobRequestStatus
    }
    class JobRequestStatusHistory
    class Vacancy {
      status: VacancyStatus
      closure_type
    }
    class JobProfile
    class EvaluationCriterion {
      stage: evaluacion|entrevista
      weight, min_score, max_score
    }
    class CandidateProfile
    class CandidateDocument
    class Application {
      status: ApplicationStatus
    }
    class ApplicationStageHistory
    class Evaluation
    class EvaluationResult
    class Interview {
      outcome: InterviewOutcome
    }
    class InterviewResult
    class SelectionDecision {
      justification
      selected_position, selected_score
    }
    class AuditLog

    Organization "1" --> "*" User : personal
    Organization "1" --> "*" JobRequest
    User "1" --> "*" JobRequest : solicita
    JobRequest "1" --> "*" JobRequestStatusHistory
    JobRequest "1" --> "0..1" Vacancy
    Vacancy "1" --> "1" JobProfile
    Vacancy "1" --> "*" EvaluationCriterion
    Vacancy "1" --> "*" Application
    Vacancy "1" --> "0..1" SelectionDecision
    User "1" --> "0..1" CandidateProfile : postulante
    CandidateProfile "1" --> "*" CandidateDocument
    Application "*" --> "1" User : postulante
    Application "*" --> "0..1" CandidateDocument : CV usado
    Application "1" --> "*" ApplicationStageHistory
    Application "1" --> "*" Evaluation
    Application "1" --> "*" Interview
    Evaluation "1" --> "*" EvaluationResult
    Interview "1" --> "*" InterviewResult
    EvaluationResult "*" --> "1" EvaluationCriterion
    InterviewResult "*" --> "1" EvaluationCriterion
    SelectionDecision "*" --> "1" Application : elegida
    Organization "1" --> "*" AuditLog
```

Servicios de dominio principales:
- `JobRequestWorkflow`
- `VacancyService` y `VacancyValidator`
- `CandidateProfileService`
- `ApplicationService` y `ApplicationStageService`
- `AssessmentScheduler`, `AssessmentResultRecorder` y `ScoreSheetValidator`
- `WeightingValidator`
- `RankingService` (puro) y `VacancyRankingBuilder`
- `FinalDecisionService`, `SelectionRegistrationService` y `VacancyClosureService`
- `AuditLogger`

## 6.4 Estados principales

```mermaid
stateDiagram-v2
    direction LR
    [*] --> borrador
    borrador --> enviado
    enviado --> observado
    observado --> enviado
    enviado --> validado
    validado --> aprobado
    validado --> rechazado
    aprobado --> [*]
    rechazado --> [*]
```

*Requerimiento de personal (`JobRequestStatus`, A-05).*

```mermaid
stateDiagram-v2
    direction LR
    [*] --> postulado
    postulado --> preseleccionado
    preseleccionado --> en_evaluacion
    preseleccionado --> en_entrevista
    en_evaluacion --> en_entrevista
    en_evaluacion --> finalista
    en_entrevista --> finalista
    finalista --> seleccionado: RF-24 (tras decisión humana)
    postulado --> descartado
    preseleccionado --> descartado
    en_evaluacion --> descartado
    en_entrevista --> descartado
    finalista --> descartado
    postulado --> no_seleccionado: RF-25 (al cerrar)
    preseleccionado --> no_seleccionado: RF-25
    en_evaluacion --> no_seleccionado: RF-25
    en_entrevista --> no_seleccionado: RF-25
    finalista --> no_seleccionado: RF-25
```

*Postulación (`ApplicationStatus`, A-13 y A-30). `seleccionado` y `no_seleccionado` no pueden asignarse manualmente.*

## 6.5 Secuencias principales

### Diagramas UML disponibles y correspondencia con la implementación

Los diagramas del equipo están fuera del repositorio, en la carpeta del curso: `Diagramas/PD/*.oom` (PowerDesigner). Se revisaron frente al código final.

| Diagrama | Contenido | Correspondencia con la implementación |
|---|---|---|
| `SaaS Reclutamiento - Diagramas UML.oom` | Secuencia de postulación: Postulante → React → Laravel 13/Inertia 3 → Policy → PostgreSQL (consultar vacante, validar permisos, consultar estado de la vacante, verificar postulación existente, registrar, confirmar) | **Coincide** con `ApplyController` + `ApplicationService::apply` (RF-10, RF-11) |
| `secuencioaEvaluacion.oom` | Secuencia de evaluación: el evaluador registra puntajes y observaciones, la Policy valida el permiso y se guarda el resultado | **Coincide en lo esencial** con `EvaluationController`/`InterviewController` + `AssessmentResultRecorder` (RF-19). La implementación separa evaluación y entrevista y valida rangos (`ScoreSheetValidator`). |
| `seleccionl_3.oom` | Secuencia de selección: **RR. HH.** consulta el ranking, confirma la selección, se registra el seleccionado, se actualiza la postulación, se cierra la convocatoria y se audita, **en un único paso** | **Difiere**. La implementación final separa: (1) la **decisión humana del Aprobador/Dirección** (RF-23), (2) el registro de la selección por RR. HH. (RF-24) y (3) el cierre por RR. HH. (RF-25), seguido de las notificaciones (RF-26). Se recomienda actualizar el diagrama. |
| `deploydiagrama.oom` | Despliegue: Cliente → Internet/HTTPS → Servidor Web/Aplicación → PostgreSQL, Redis, **S3**, Queue Worker | **Difiere parcialmente.** No hay S3: los CV se guardan en disco local privado. HTTPS no está configurado en el entorno local de Docker. El despliegue real está en el [capítulo 10](10-dockerizacion.md). |

### Secuencia implementada: decisión humana, selección y cierre

```mermaid
sequenceDiagram
    actor D as Aprobador/Dirección
    actor H as RR. HH.
    participant UI as React/Inertia
    participant L as Laravel (Policy + Service)
    participant DB as PostgreSQL
    participant Q as Cola (Redis) + worker
    H->>UI: Consultar comparación
    UI->>L: GET /vacantes/{id}/comparacion
    L->>DB: Resultados realizados de la vacante
    L-->>UI: Ranking explicable (apoyo, sin seleccionar)
    D->>UI: Elegir finalista + justificación + confirmación humana
    UI->>L: POST /vacantes/{id}/decision
    L->>L: VacancyPolicy::decide (solo aprobador de la organización)
    L->>DB: selection_decisions (no cambia estados) + auditoría
    H->>UI: Registrar selección
    UI->>L: POST /vacantes/{id}/seleccion
    L->>DB: finalista → seleccionado (índice único parcial) + auditoría
    H->>UI: Cerrar convocatoria
    UI->>L: POST /vacantes/{id}/cerrar
    L->>DB: bloqueo de fila, vacante cerrada, activas → no_seleccionado + auditoría
    L->>Q: ProcessResultNotification (afterCommit)
    Q->>DB: notificación a cada postulante
```

## 6.6 Interfaz de usuario

Páginas Inertia/React reales (`resources/js/pages`), agrupadas por rol:

| Rol | Páginas |
|---|---|
| Público | `welcome`, `jobs/index`, `jobs/show`, `auth/login`, `auth/register` |
| Área solicitante | `dashboard`, `job-requests/index`, `create`, `edit`, `show` |
| RR. HH. | `job-requests/*`, `vacancies/index`, `create`, `edit`, `show`, `applications/index`, `show` (con evaluaciones y entrevistas), `selection/comparison` |
| Aprobador / Dirección | `job-requests/show` (decisión), `vacancies/*`, `selection/comparison` (decisión final), `audit/index` |
| Evaluador | `assessments/index`, `assessments/show` (hoja de puntajes) |
| Postulante | `candidate/profile`, `candidate/applications/index`, `show` (etapas y convocatorias), `jobs/show` (postular) |
| Todos | `notifications/index`, `settings/*` |

Comunes: interfaz en español (`es-PE`), menú lateral según el rol, insignias de estado, `data-cy` estables para E2E y diseño adaptable. La validación visual está en `docs/manual-smoke-test.md`.

## 6.7 Modelo de datos

17 migraciones; esquema PostgreSQL 17. Tablas del dominio:

```mermaid
erDiagram
    organizations ||--o{ users : "personal (postulante sin organización)"
    organizations ||--o{ job_requests : ""
    users ||--o{ job_requests : "requested_by"
    job_requests ||--o{ job_request_status_histories : ""
    job_requests ||--o| vacancies : "job_request_id único"
    vacancies ||--|| job_profiles : ""
    vacancies ||--o{ evaluation_criteria : ""
    vacancies ||--o{ applications : ""
    vacancies ||--o| selection_decisions : "vacancy_id único"
    users ||--o| candidate_profiles : ""
    candidate_profiles ||--o{ candidate_documents : ""
    users ||--o{ applications : "candidate_id"
    candidate_documents ||--o{ applications : "CV usado"
    applications ||--o{ application_stage_histories : ""
    applications ||--o{ evaluations : ""
    applications ||--o{ interviews : ""
    evaluations ||--o{ evaluation_results : ""
    interviews ||--o{ interview_results : ""
    evaluation_criteria ||--o{ evaluation_results : ""
    evaluation_criteria ||--o{ interview_results : ""
    applications ||--o{ selection_decisions : "selected_application_id"
    organizations ||--o{ audit_logs : ""
    users ||--o{ audit_logs : "user_id (null al eliminar)"
    users ||--o{ notifications : "notifiable"
```

**Integridad aplicada en la base de datos:**
- `CHECK` de estados válidos en requerimientos, vacantes, postulaciones, evaluaciones y entrevistas.
- Coherencia rol ↔ organización en `users`.
- Plazas ≥ 1, fechas coherentes, rangos y ponderaciones de criterios, puntajes no negativos.
- Duración de sesiones entre 15 y 480 minutos.
- Coherencia del cierre, de la finalización de sesiones y del registro de la selección.
- Postulación única por vacante y postulante.
- Una decisión por vacante.
- Índice único parcial `applications_one_selected_per_vacancy`.
- *Trigger* `audit_logs_append_only`.

Tablas de apoyo del framework: `cache`, `jobs`, `sessions`, `password_reset_tokens` y `passkeys` (*starter kit*).
