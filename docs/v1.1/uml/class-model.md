# CL-01 · Modelo de clases del dominio

| | |
|---|---|
| **Objetivo** | Representar las entidades del dominio, sus atributos relevantes, sus asociaciones con multiplicidad verificada y la frontera multiempresa |
| **Alcance** | 17 modelos de dominio de `app/Models` + enums de estado. **Sin** clases del *framework*, controladores ni *getters*. Los servicios van en el diagrama de componentes |
| **Fuente de verdad** | `app/Models/*.php` (relaciones Eloquent), `database/migrations/*` (FK, `UNIQUE`, `CHECK`), `app/Enums/*`, `app/Models/Concerns/BelongsToOrganization.php`, `app/Models/Scopes/OrganizationScope.php` |
| **Borrador textual** | [`puml/cl-01-domain.puml`](puml/cl-01-domain.puml) |
| **RF** | RF-01 a RF-27 y RF-29 (atributo `Vacancy.target_completion_at`) |

## 1. Decisiones de modelado

- **Clase de dominio ≠ tabla.** El diagrama muestra la clase Eloquent con sus atributos de negocio. Las FK no se dibujan como atributos: son asociaciones. Timestamps (`created_at`, `updated_at`) y columnas técnicas (`remember_token`, secretos de 2FA) se omiten. El modelo físico va aparte, para F23 ([§6](#6-nota-para-el-modelo-físico-f23)).
- **Multiplicidad = FK + `UNIQUE` + regla del servicio.** Cuando la base admite más que la regla de negocio, se indica ambas cosas.
- **Multiempresa con estereotipo, no con 13 líneas.** Las 13 clases con `BelongsToOrganization` llevan `<<tenant scoped>>` y el atributo `organization_id`. Solo se dibujan explícitamente las asociaciones con `Organization` de `User`, `JobRequest`, `Vacancy` y `AuditLog`; una nota explica que las demás heredan el mismo aislamiento.
- **Composición** (rombo lleno) solo donde la FK es `cascadeOnDelete` y la parte no tiene sentido sin el todo: historiales, perfil del puesto, criterios, documentos del postulante y resultados por criterio. El resto son asociaciones (`restrictOnDelete` o `nullOnDelete`).
- **Enums** como `<<enumeration>>` con sus valores reales.
- **No se modelan** como clases persistentes el ranking ni la estimación de riesgo: se calculan en cada consulta. Van como `<<value object>>` en un paquete aparte solo si F23 lo necesita; su lugar natural es el diagrama de componentes.

## 2. Clases

`<<T>>` = `<<tenant scoped>>`: lleva `organization_id`, se filtra con `OrganizationScope` para el personal y la Policy compara organización.

| Clase | Atributos relevantes (nombre real) | Notas |
|---|---|---|
| `Organization` | `name`, `slug` (único), `tax_id` (único, opcional), `is_active` | Raíz del tenant |
| `User` | `name`, `email` (único), `role: UserRole`, `organization_id` (nulo si `postulante`) | Personal o postulante. `CHECK users_role_organization` |
| `JobRequest` `<<T>>` | `code` (único por organización), `position_title`, `area`, `headcount` (≥ 1), `contract_type`, `justification`, `required_by`, `status: JobRequestStatus`, `observation`, `submitted_at`, `validated_at`, `decided_at`, `decision_comment` | RF-01–RF-03 |
| `JobRequestStatusHistory` `<<T>>` | `from_status`, `to_status`, `comment`, `created_at` | Historial de solo añadido por servicio |
| `Vacancy` `<<T>>` | `code` (único por organización), `title`, `summary`, `location`, `contract_type`, `positions` (≥ 1), `opens_at`, `closes_at`, **`target_completion_at`** (> `closes_at`, opcional), `status: VacancyStatus`, `published_at`, `closed_at`, `closure_type: VacancyClosureType`, `closure_notes` | `target_completion_at` es de la Fase 16 (GAP-01 resuelto técnicamente) |
| `JobProfile` `<<T>>` | `education`, `experience`, `functions`, `competencies` | RF-05 |
| `EvaluationCriterion` `<<T>>` | `name` (único por vacante), `stage: CriterionStage`, `weight` (> 0), `min_score`, `max_score` (> mínimo) | RF-05, RF-20 |
| `CandidateProfile` | `phone`, `city`, `education_level`, `professional_title`, `years_of_experience`, `summary` | **Global**, sin `organization_id` |
| `CandidateDocument` | `type: DocumentType` (`cv`), `original_name`, `stored_path` (único), `mime_type`, `size_bytes` | **Global**. Archivo en el disco privado `local` |
| `Application` `<<T>>` | `status: ApplicationStatus`, `applied_at`, `stage_changed_at` | Única por (vacante, postulante) |
| `ApplicationStageHistory` `<<T>>` | `from_status`, `to_status`, `comment`, `created_at` | RF-14 |
| `Evaluation` `<<T>>` | `type: EvaluationType`, `modality`, `location`, `scheduled_at`, `duration_minutes` (15–480), `instructions`, `status: AssessmentStatus`, `invitation_sent_at`, `completed_at`, `observations` | RF-16, RF-19 |
| `EvaluationResult` `<<T>>` | `score` (≥ 0), `comment` | Único por (evaluación, criterio) |
| `Interview` `<<T>>` | `modality`, `location`, `scheduled_at`, `duration_minutes`, `instructions`, `status: AssessmentStatus`, `outcome: InterviewOutcome`, `invitation_sent_at`, `completed_at`, `observations` | RF-18, RF-19 |
| `InterviewResult` `<<T>>` | `score` (≥ 0), `comment` | Único por (entrevista, criterio) |
| `SelectionDecision` `<<T>>` `<<human decision>>` | `justification`, `selected_position` (≥ 1), `selected_score` (0–100), `ranked_candidates` (≥ posición), `decided_at`, `selection_registered_at` | Única por vacante e inmutable. Guarda la **instantánea** del ranking al decidir |
| `AuditLog` `<<T>>` `<<append only>>` | `action: AuditAction`, `auditable_type`, `auditable_id`, `metadata` (JSONB, sin datos sensibles), `ip_address`, `created_at` | `organization_id` nulo para acciones de cuentas globales. *Trigger* `audit_logs_append_only`: rechaza `DELETE` y todo `UPDATE`, salvo anular `user_id` al borrar el usuario (FK `nullOnDelete`) |

## 3. Asociaciones y multiplicidades

Leído como *extremo A mult. — mult. extremo B*. Fuente: la relación Eloquent y la FK indicadas.

| # | A | Mult. A | Mult. B | B | Rol / FK | Tipo | Fuente |
|---|---|---|---|---|---|---|---|
| 1 | `Organization` | 0..1 | 0..* | `User` | `users.organization_id` (nulo para postulantes) | Asociación | `User::organization`, `Organization::users` |
| 2 | `Organization` | 1 | 0..* | `JobRequest`, `Vacancy` y demás `<<T>>` | `organization_id` | Asociación (nota) | `BelongsToOrganization::organization` |
| 3 | `Organization` | 0..1 | 0..* | `AuditLog` | `audit_logs.organization_id` nulo | Asociación | migración `audit_logs` |
| 4 | `User` | 1 | 0..* | `JobRequest` | `requested_by` · rol *solicitante* | Asociación | `JobRequest::requester` |
| 5 | `User` | 0..1 | 0..* | `JobRequest` | `validated_by` · rol *validador* | Asociación | `JobRequest::validator` |
| 6 | `User` | 0..1 | 0..* | `JobRequest` | `decided_by` · rol *decisor* | Asociación | `JobRequest::decider` |
| 7 | `JobRequest` | 1 | 0..* | `JobRequestStatusHistory` | `job_request_id` cascade | **Composición** | `JobRequest::statusHistories` |
| 8 | `JobRequestStatusHistory` | 0..* | 1 | `User` | `changed_by` · autor | Asociación | `::author` |
| 9 | `JobRequest` | 1 | 0..1 | `Vacancy` | `vacancies.job_request_id` **UNIQUE**; solo si el requerimiento está aprobado | Asociación | `JobRequest::vacancy`, `Vacancy::jobRequest` |
| 10 | `Vacancy` | 1 | 1 | `JobProfile` | `job_profiles.vacancy_id` UNIQUE cascade. Físicamente 0..1; **1 por regla** (el formulario lo exige y el servicio lo crea) | **Composición** | `Vacancy::profile` |
| 11 | `Vacancy` | 1 | 0..* | `EvaluationCriterion` | `vacancy_id` cascade; nombre único por vacante. Publicar exige criterios válidos | **Composición** | `Vacancy::criteria` |
| 12 | `User` | 1 | 0..* | `Vacancy` | `created_by` · creador | Asociación | `Vacancy::creator` |
| 13 | `User` | 0..1 | 0..* | `Vacancy` | `published_by` · publicador | Asociación | `Vacancy::publisher` |
| 14 | `User` | 0..1 | 0..* | `Vacancy` | `closed_by` · quien cierra | Asociación | `Vacancy::closer` |
| 15 | `Vacancy` | 1 | 0..* | `Application` | `vacancy_id` restrict | Asociación | `Vacancy::applications` |
| 16 | `User` | 1 | 0..* | `Application` | `candidate_id` · postulante; **UNIQUE (vacancy_id, candidate_id)** | Asociación | `Application::candidate`, `User::applications` |
| 17 | `User` | 1 | 0..1 | `CandidateProfile` | `candidate_profiles.user_id` UNIQUE cascade | **Composición** | `User::candidateProfile` |
| 18 | `CandidateProfile` | 1 | 0..* | `CandidateDocument` | `candidate_profile_id` cascade | **Composición** | `CandidateProfile::documents` (`latestCv` = el más reciente) |
| 19 | `Application` | 0..* | 0..1 | `CandidateDocument` | `candidate_document_id` · CV usado al postular | Asociación | `Application::cvDocument` |
| 20 | `Application` | 1 | 0..* | `ApplicationStageHistory` | `application_id` cascade | **Composición** | `Application::stageHistories` |
| 21 | `ApplicationStageHistory` | 0..* | 1 | `User` | `changed_by` · autor | Asociación | `::author` |
| 22 | `Application` | 1 | 0..* | `Evaluation` | `application_id` restrict | Asociación | `Application::evaluations` |
| 23 | `Application` | 1 | 0..* | `Interview` | `application_id` restrict | Asociación | `Application::interviews` |
| 24 | `User` | 1 | 0..* | `Evaluation` | `evaluator_id` · evaluador asignado | Asociación | `Evaluation::evaluator` |
| 25 | `User` | 1 | 0..* | `Interview` | `evaluator_id` · evaluador asignado | Asociación | `Interview::evaluator` |
| 26 | `Evaluation` | 1 | 0..* | `EvaluationResult` | `evaluation_id` cascade | **Composición** | `Evaluation::results` |
| 27 | `Interview` | 1 | 0..* | `InterviewResult` | `interview_id` cascade | **Composición** | `Interview::results` |
| 28 | `EvaluationCriterion` | 1 | 0..* | `EvaluationResult` | `evaluation_criterion_id` restrict; **UNIQUE (evaluation_id, criterion)** | Asociación | `EvaluationResult::criterion` |
| 29 | `EvaluationCriterion` | 1 | 0..* | `InterviewResult` | `evaluation_criterion_id` restrict; **UNIQUE (interview_id, criterion)** | Asociación | `InterviewResult::criterion` |
| 30 | `Vacancy` | 1 | 0..1 | `SelectionDecision` | `selection_decisions.vacancy_id` **UNIQUE** | Asociación | `Vacancy::selectionDecision` |
| 31 | `SelectionDecision` | 0..1 | 1 | `Application` | `selected_application_id` · elegida. 0..1 del lado de la decisión porque hay una sola por vacante | Asociación | `SelectionDecision::selectedApplication` |
| 32 | `User` | 1 | 0..* | `SelectionDecision` | `decided_by` · **Aprobador** | Asociación | `SelectionDecision::decider` |
| 33 | `User` | 0..1 | 0..* | `SelectionDecision` | `selection_registered_by` · RR. HH. | Asociación | `SelectionDecision::selectionRegistrar` |
| 34 | `User` | 0..1 | 0..* | `AuditLog` | `user_id` nullOnDelete · actor | Asociación | `AuditLog::user` |
| 35 | `AuditLog` | 0..* | 1 | *entidad auditada* | `auditable_type` + `auditable_id` (polimórfica) | Dependencia con nota | migración `audit_logs` |
| 36 | `User` | 1 | 0..* | `Evaluation` | `evaluations.scheduled_by` **NOT NULL** restrict · *programador* (RR. HH.) | Asociación | FK de la migración `evaluations` + `AssessmentScheduler::sessionAttributes` (`'scheduled_by' => $hr->id`). **Sin relación Eloquent declarada** |
| 37 | `User` | 1 | 0..* | `Interview` | `interviews.scheduled_by` **NOT NULL** restrict · *programador* (RR. HH.) | Asociación | FK de la migración `interviews` + `AssessmentScheduler::sessionAttributes`. **Sin relación Eloquent declarada** |

**Dos asociaciones distintas entre `User` y cada sesión** (24/36 para `Evaluation`, 25/37 para `Interview`): `evaluator_id` es el **evaluador asignado**, que registra los resultados (RF-19); `scheduled_by` es **quien programó** la sesión, RR. HH. (RF-16, RF-18). Pueden ser personas distintas y se dibujan como dos líneas con su nombre de rol, no como una. Las filas 36 y 37 se añadieron en el *hotfix* de la Fase 22 (auditoría de Codex, MEDIUM-01); se verificó que son las únicas FK a `users` que faltaban.

Restricción adicional que no se ve en una multiplicidad: **índice único parcial `applications_one_selected_per_vacancy`** — como mucho una postulación `seleccionado` por vacante. Va como nota OCL o de texto sobre la asociación 15.

`EvaluationCriterion.stage` separa los criterios de **evaluación** y de **entrevista**: `EvaluationResult` solo usa criterios de etapa `evaluacion` e `InterviewResult` solo de etapa `entrevista`. Lo hace cumplir `ScoreSheetValidator`, no una FK: va como nota.

## 4. Enumeraciones

| Enum | Valores |
|---|---|
| `UserRole` | `solicitante`, `rrhh`, `aprobador`, `evaluador`, `postulante` |
| `JobRequestStatus` | `borrador`, `enviado`, `observado`, `validado`, `aprobado`, `rechazado` |
| `VacancyStatus` | `borrador`, `publicada`, `cerrada` |
| `VacancyClosureType` | `con_seleccion`, `desierta` (**`desierta` sin flujo implementado**, A-30) |
| `ApplicationStatus` | `postulado`, `preseleccionado`, `en_evaluacion`, `en_entrevista`, `finalista`, `seleccionado`, `no_seleccionado`, `descartado` |
| `AssessmentStatus` | `programada`, `realizada` |
| `EvaluationType` | `conocimientos`, `clase_modelo`, `practica`, `otra` |
| `InterviewOutcome` | `recomendado`, `recomendado_con_reservas`, `no_recomendado` |
| `CriterionStage` | `evaluacion`, `entrevista` |
| `DocumentType` | `cv` |
| `AuditAction` | 23 acciones (`usuario.registrado` … `proceso.resultado_notificado`); listarlas en una nota o en el diccionario de F23 |

`ContractType`, `Modality` y `EducationLevel` también existen; son valores de formulario, no de comportamiento, y pueden ir solo como tipo del atributo.

## 5. Multiempresa en este diagrama

- `<<tenant scoped>>` = `use BelongsToOrganization`: *global scope* `OrganizationScope` (filtra por `organization_id` del usuario autenticado cuando lo tiene) y asignación de `organization_id` al crear.
- El aislamiento es **lógico en la aplicación** (scope + Policies que comparan rol **y** organización, `sharesOrganizationWith`). **No hay PostgreSQL RLS ni base de datos por tenant.**
- `User` (postulante), `CandidateProfile` y `CandidateDocument` son **globales**: un postulante puede postular a vacantes de varias organizaciones. El personal ve su CV solo si ese postulante tiene una postulación en su organización (`CandidateDocumentPolicy`).
- Nota del diagrama: *«Las 13 clases `<<tenant scoped>>` pertenecen a exactamente una `Organization` (asociación 2); solo se dibujan explícitamente las de `JobRequest`, `Vacancy`, `User` y `AuditLog`.»*

## 6. Nota para el modelo físico (F23)

El PDM se obtiene por ingeniería inversa del esquema real (procedimiento en `.claude/skills/powerdesigner-uml/POWERDESIGNER.md`), no a partir de este diagrama. Conteo esperado a verificar tras importar: **17 tablas de dominio** (las de §2, con `vacancies`, `job_profiles` y `evaluation_criteria` en la misma migración) más las tablas del *framework* (`users` se comparte). Restricciones que deben aparecer: los `CHECK` de estado y de coherencia de cada tabla, `UNIQUE (organization_id, code)` en `job_requests` y `vacancies`, `UNIQUE (vacancy_id, candidate_id)` en `applications`, el índice parcial `applications_one_selected_per_vacancy`, `vacancies_target_after_close` y el *trigger* `audit_logs_append_only`.

## 7. Contraste con v1.0

Mismas 17 clases que [`05-class-model-report.md`](../../final-report/diagram-reports/05-class-model-report.md). Única diferencia estructural de v1.1: **`Vacancy.target_completion_at`** (Fase 16). No hay clases nuevas de dominio: el ML no persiste nada.

## 8. Instrucciones para F23

1. OOM, *Class Diagram* «CL-01 Dominio AS-IS v1.1», paquete `App\Models`; enums en un paquete `App\Enums`.
2. Crear las 17 clases con los atributos de §2, sin timestamps ni FK como atributos.
3. Trazar las 37 asociaciones de §3 con sus multiplicidades y nombres de rol; composiciones donde se indica. Entre `User` y `Evaluation`/`Interview` van **dos** asociaciones cada una: `evaluator` y `scheduler`.
4. Estereotipos: `<<tenant scoped>>`, `<<human decision>>` (`SelectionDecision`), `<<append only>>` (`AuditLog`).
5. Notas: multiempresa (§5), índice parcial de selección, separación de criterios por etapa, `desierta` sin flujo.
