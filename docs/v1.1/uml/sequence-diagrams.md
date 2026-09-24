# SEQ-01 a SEQ-08 · Diagramas de secuencia

| | |
|---|---|
| **Objetivo** | Mostrar cómo ocurren, paso a paso, los ocho flujos críticos del sistema |
| **Alcance** | Un diagrama por flujo, con *lifelines* significativas. Sin detalles del *framework* (resolución de rutas, sesión, CSRF, *model binding*) |
| **Fuente de verdad** | Controladores, Form Requests (`authorize()`), Policies y servicios citados en cada secuencia |
| **Borradores textuales** | `puml/seq-01-…` a `puml/seq-08-…` |

## Convenciones comunes

**Lifelines**: Actor · UI (página Inertia) · Controlador · Policy · Servicio · Modelo/BD (PostgreSQL) · Auditoría (`AuditLogger`) · Notificación (cola Redis) · servicio externo cuando aplica.

**Patrón transaccional** que comparten todas las secuencias de escritura, y que cada diagrama muestra una vez como fragmento `critical`:

1. La autorización ocurre **antes** del servicio: `Gate::authorize(...)` en el controlador o `FormRequest::authorize()` → Policy (rol **y** organización).
2. El servicio abre `DB::transaction`, bloquea la fila con `lockForUpdate()` y comprueba la transición con el enum (`canTransitionTo`).
3. Una regla de negocio incumplida lanza `BusinessRuleException` → mensaje en español y redirección atrás, sin 500. Va como fragmento `alt`.
4. `AuditLogger::record(...)` dentro de la misma transacción.
5. Las notificaciones son `ShouldQueue` + `afterCommit`: se encolan en Redis y **solo se despachan si la transacción confirma**. El trabajador de cola las entrega por `database` y `mail` (*log* en desarrollo).
6. Respuesta: redirección con *toast* (escrituras) o `Inertia::render` (lecturas).

**RF-27** está presente en todas las escrituras (paso 4). Se dibuja el mensaje `record()` en cada secuencia, sin detallar su interior.

---

## SEQ-01 · Registrar postulación (RF-10, RF-11)

`puml/seq-01-apply.puml`

| # | De → A | Mensaje |
|---|---|---|
| 1 | Postulante → UI `jobs/show` | Pulsa «Postular» |
| 2 | UI → `ApplyController` | `POST empleos/{vacancy}/postular` |
| 3 | `ApplyController` → `ApplicationPolicy` | `apply(user)` → solo `postulante` |
| 4 | `ApplyController` → `ApplicationService` | `apply(candidate, vacancy)` |
| 5 | `ApplicationService` → BD | `Vacancy` con `lockForUpdate()` (sin *global scope*: el postulante es global) |
| 6 | `alt` | Vacante no abierta · perfil incompleto · sin CV · postulación duplicada → `BusinessRuleException` |
| 7 | `ApplicationService` → BD | Crea `Application` (`postulado`, CV más reciente, `organization_id` de la vacante) y el primer `ApplicationStageHistory` |
| 8 | `ApplicationService` → `AuditLogger` | `record(ApplicationSubmitted)` |
| 9 | BD | *Commit*. `UNIQUE (vacancy_id, candidate_id)` protege además de la carrera → misma excepción de duplicado |
| 10 | `ApplicationService` → Notificación | `ApplicationReceivedNotification` al postulante (**RF-11**) |
| 11 | `ApplyController` → UI | Redirección + *toast* «Postulación registrada» |

## SEQ-02 · Aprobar o rechazar requerimiento (RF-03, RF-04)

`puml/seq-02-decide-job-request.puml`

| # | De → A | Mensaje |
|---|---|---|
| 1 | Aprobador → UI `job-requests/show` | Elige aprobar o rechazar; comentario obligatorio al rechazar |
| 2 | UI → `JobRequestTransitionController` | `POST requerimientos/{id}/decision` |
| 3 | `DecideJobRequestRequest` → `JobRequestPolicy` | `decide()` → `aprobador` de la misma organización |
| 4 | Controlador → `JobRequestWorkflow` | `approve(...)` o `reject(...)` según `JobRequestDecision` |
| 5 | `JobRequestWorkflow` → BD | `JobRequest` con `lockForUpdate()`; `validado` → `aprobado` \| `rechazado` |
| 6 | `alt` | Transición no permitida → excepción |
| 7 | `JobRequestWorkflow` → BD | Actualiza estado, `decided_by`, `decided_at`, `decision_comment`; añade `JobRequestStatusHistory` |
| 8 | `JobRequestWorkflow` → `AuditLogger` | `record(JobRequestApproved \| JobRequestRejected)` |
| 9 | `opt [rechazo]` → Notificación | `JobRequestRejectedNotification` al **solicitante** (**RF-04**) |
| 10 | Controlador → UI | Redirección + *toast* |

## SEQ-03 · Cambiar etapa y notificar (RF-13, RF-14, RF-15)

`puml/seq-03-change-stage.puml`

| # | De → A | Mensaje |
|---|---|---|
| 1 | RR. HH. → UI `applications/show` | Preselecciona, descarta (comentario obligatorio) o elige etapa destino |
| 2 | UI → `ApplicationStageController` | `POST postulaciones/{id}/preseleccionar` \| `descartar` \| `etapa` |
| 3 | Form Request → `ApplicationPolicy` | `changeStage()` → `rrhh` de la misma organización |
| 4 | Controlador → `ApplicationStageService` | `shortlist` \| `discard` \| `moveTo(target)` |
| 5 | `alt` | Destino `seleccionado`/`no_seleccionado` (solo RF-24/RF-25) · decisión final ya registrada (A-28) · vacante cerrada · transición inválida → excepción |
| 6 | Servicio → BD | `Application` con `lockForUpdate()`; nuevo estado, `stage_changed_at`; `ApplicationStageHistory` con autor y comentario |
| 7 | Servicio → `AuditLogger` | `record(ApplicationStageChanged)` |
| 8 | Servicio → Notificación | `ApplicationStageChangedNotification` al postulante (**RF-15**) |
| 9 | Controlador → UI | Redirección + *toast* «Se notificó al candidato» |

## SEQ-04 · Programar evaluación (RF-16, RF-17)

`puml/seq-04-schedule-evaluation.puml`

| # | De → A | Mensaje |
|---|---|---|
| 1 | RR. HH. → UI `applications/show` | Tipo, modalidad, lugar, fecha, duración, evaluador |
| 2 | UI → `AssessmentScheduleController` | `POST postulaciones/{id}/evaluaciones` |
| 3 | `ScheduleEvaluationRequest` → `ApplicationPolicy` | `scheduleAssessment()` → `rrhh` de la misma organización |
| 4 | Controlador → `AssessmentScheduler` | `scheduleEvaluation(application, hr, data)` |
| 5 | Scheduler → BD | `Application` con `lockForUpdate()` |
| 6 | `alt` | Vacante cerrada · sin criterios de etapa `evaluacion` · postulación no preseleccionada ni en evaluación · evaluador de otra organización o sin rol `evaluador` → excepción |
| 7 | Scheduler → BD | Crea `Evaluation` (`programada`, `invitation_sent_at`) |
| 8 | Scheduler → `ApplicationStageService` | `transition(..., en_evaluacion, notify: false)` si aún no estaba ahí |
| 9 | Scheduler → `AuditLogger` | `record(EvaluationScheduled)` |
| 10 | Scheduler → Notificación | `AssessmentConvocationNotification` al postulante (**RF-17**) y `AssessmentAssignedNotification` al evaluador |
| 11 | Controlador → UI | Redirección + *toast* |

## SEQ-05 · Programar y registrar entrevista (RF-18, RF-19)

`puml/seq-05-interview.puml`. Dos tramos en el mismo diagrama, separados por un fragmento `ref`/divisor.

**Tramo A — programar (RR. HH.)**: igual que SEQ-04 con `POST postulaciones/{id}/entrevistas`, `ScheduleAssessmentRequest`, criterios de etapa `entrevista`, postulación en `preseleccionado`, `en_evaluacion` o `en_entrevista`, creación de `Interview` y avance a `en_entrevista`. Convocatoria al postulante y aviso al evaluador (RF-17).

**Tramo B — registrar resultado (Evaluador)**:

| # | De → A | Mensaje |
|---|---|---|
| 1 | Evaluador → UI `assessments/index` | Abre la sesión asignada (`GET entrevistas/{id}`) |
| 2 | `InterviewController` → `InterviewPolicy` | `view()` / `recordResult()` → **evaluador asignado** (`evaluator_id` = usuario) de la misma organización |
| 3 | Evaluador → UI `assessments/show` | Puntaje por criterio, resultado (`InterviewOutcome`) y observaciones |
| 4 | UI → `InterviewController` | `POST entrevistas/{id}/resultados` |
| 5 | Controlador → `AssessmentResultRecorder` | `recordInterview(interview, evaluator, scores, outcome, observations)` |
| 6 | Recorder → BD | `Interview` con `lockForUpdate()` |
| 7 | `alt` | Resultados ya registrados · vacante cerrada · puntaje fuera de rango o criterio ajeno (`ScoreSheetValidator`, **RF-20**) → excepción |
| 8 | Recorder → BD | Un `InterviewResult` por criterio; `Interview` → `realizada`, `outcome`, `completed_at` |
| 9 | Recorder → `AuditLogger` | `record(InterviewResultRecorded)` |
| 10 | Controlador → UI | Redirección + *toast* |

## SEQ-06 · Calcular ranking y comparar candidatos (RF-20, RF-21, RF-22)

`puml/seq-06-ranking.puml`. **Solo lectura**: no hay transacción de escritura, auditoría ni notificación.

| # | De → A | Mensaje |
|---|---|---|
| 1 | RR. HH. o Aprobador → UI | Abre la comparación de la vacante |
| 2 | UI → `VacancyComparisonController` | `GET vacantes/{id}/comparacion` |
| 3 | Controlador → `VacancyPolicy` | `viewRanking()` → `rrhh` o `aprobador` de la misma organización |
| 4 | Controlador → `VacancyRankingBuilder` | `forVacancy(vacancy)` |
| 5 | Builder → BD | Postulaciones de la vacante **excepto descartadas**; puntajes de sesiones `realizada` (evaluaciones y entrevistas) |
| 6 | Builder → `RankingService` | `rank(criteria, candidates)` |
| 7 | `RankingService` | Valida configuración y puntajes (**RF-20**); calcula promedios por criterio, aporte ponderado y total; marca empates; separa los **incompletos** |
| 8 | `alt` | Configuración o puntajes inválidos → `InvalidRankingInput` → la página muestra el error en lugar del ranking |
| 9 | Controlador → `RankingPresenter` | Presenta criterios, ponderaciones, aportes, total y posición |
| 10 | Controlador → UI `selection/comparison` | `Inertia::render` |

Nota obligatoria: **el ranking no se guarda y no cambia ninguna postulación**. Es soporte a la decisión (`test_rf23_calculating_the_ranking_never_selects_a_candidate`).

## SEQ-07 · Registrar decisión final (RF-23) `<<human decision>>`

`puml/seq-07-final-decision.puml`

| # | De → A | Mensaje |
|---|---|---|
| 1 | Aprobador → UI `selection/comparison` | Elige una postulación **finalista**, escribe la justificación y marca la confirmación de decisión humana |
| 2 | UI → `FinalDecisionController` | `POST vacantes/{id}/decision` |
| 3 | `FinalDecisionRequest` | Valida `application_id`, `justification` (20–2000 caracteres) y `human_confirmation` (`accepted`) |
| 4 | `FinalDecisionRequest` → `VacancyPolicy` | `decide()` → **solo `aprobador`** de la misma organización |
| 5 | Controlador → `FinalDecisionService` | `decide(vacancy, approver, applicationId, justification)` |
| 6 | Servicio → BD | `Vacancy` con `lockForUpdate()` |
| 7 | `alt` | Vacante no publicada o cerrada · decisión ya registrada · postulación ajena · **no finalista** → excepción |
| 8 | Servicio → `VacancyRankingBuilder` | `forVacancy(...)` **solo para la instantánea**; `alt` sin resultados completos → excepción |
| 9 | Servicio → BD | Crea `SelectionDecision`: elegida, decisor, justificación, `selected_position`, `selected_score`, `ranked_candidates`, `decided_at` |
| 10 | Servicio → `AuditLogger` | `record(SelectionDecisionRecorded)` |
| 11 | Controlador → UI | Redirección + *toast* «RR. HH. debe registrar la selección» |

Notas obligatorias: la persona elige; **puede no ser la primera del ranking**; la decisión **no cambia el estado de ninguna postulación** (eso lo hacen RF-24 y RF-25); es única e inmutable; **no hay ningún mensaje hacia el servicio de riesgo operacional**.

Continuación (fuera de este diagrama, `ref`): RR. HH. registra la selección (`SelectionRegistrationService`: elegida → `seleccionado`, sin notificar) y cierra la vacante (`VacancyClosureService`: `cerrada` con `con_seleccion`, el resto de las activas → `no_seleccionado`, `ProcessResultNotification` a la seleccionada y a cada postulación que pasa a `no_seleccionado`, **RF-26**; las descartadas antes del cierre ya fueron notificadas por RF-15).

## SEQ-08 · Consultar riesgo operacional (RF-29) `<<experimental>>`

`puml/seq-08-operational-risk.puml`

| # | De → A | Mensaje |
|---|---|---|
| 1 | RR. HH. o Aprobador → UI `vacancies/show` | Abre el detalle de la vacante (la página carga sin esperar al riesgo) |
| 2 | `OperationalRiskCard` → `VacancyOperationalRiskController` | `GET vacantes/{id}/riesgo-operacional` (JSON) |
| 3 | Controlador → `VacancyPolicy` | `viewOperationalRisk()` → `rrhh` o `aprobador` de la misma organización |
| 4 | Controlador → `OperationalRiskService` | `assess(vacancy)` |
| 5 | Servicio | `outOfScopeReason()`: no publicada · sin `closes_at` · sin `target_completion_at` · *checkpoint* no alcanzado · vacante cerrada · plazo antes del *checkpoint* · consulta tras el plazo |
| 6 | `alt [fuera de alcance]` | `RiskAssessment::descriptive(motivo)` → **no se llama al servicio** |
| 7 | Servicio → `OperationalRiskFeatureBuilder` | `build(vacancy, checkpoint)`; *checkpoint* = día siguiente a `closes_at` |
| 8 | Builder → BD | Conteos y días del proceso **hasta el *checkpoint*** → 15 enteros |
| 9 | Servicio → `MlRiskClient` | `predict(features)` |
| 10 | `alt [ML_SERVICE_ENABLED=false]` | `descriptive(service_disabled)` |
| 11 | `MlRiskClient` → FastAPI | `POST /v1/predict`, cabecera `X-Internal-Token`, cuerpo = **solo las 15 features** (sin IDs ni PII) |
| 12 | FastAPI | `security` valida el token (sin token configurado → 503); `PredictionRequest` rechaza campos extra o tipos laxos (422) |
| 13 | FastAPI → *Predictor* | Aplica el modelo congelado (cargado y verificado al arrancar) |
| 14 | FastAPI → `MlRiskClient` | `risk_score`, `risk_flag`, `threshold`, `model_version`, `freeze_fingerprint`, `status` |
| 15 | `MlRiskClient` | Valida: campos, tipos, rango [0, 1], `risk_flag` = (`risk_score` ≥ `threshold`), *threshold* y *freeze* iguales a los congelados |
| 16 | `alt` | Timeout, conexión, 503, 422, 5xx, JSON inválido o contrato incompatible → `unavailable(motivo)` |
| 17 | `MlRiskClient` → Servicio | `RiskAssessment::predictive(...)` |
| 18 | Controlador → UI | JSON: disponibilidad, porcentaje, señal, mensaje explicativo, `is_experimental`, `measures: proceso`, `decision_is_human` |
| 19 | UI | Muestra la tarjeta: «Experimental», porcentaje y señal si es predictivo; solo etiqueta y mensaje si es descriptivo o no disponible |

Notas obligatorias: estima el **proceso**, no a las personas; nada se guarda en la base (solo una línea de *log*); **no hay ningún mensaje hacia el ranking, la comparación ni la decisión**; la respuesta no tiene incertidumbre.

## Instrucciones para F23

1. Un *Sequence Diagram* por flujo, con los nombres `SEQ-0n` y el título de este documento.
2. *Lifelines* de las tablas; fragmentos `alt`/`opt`/`critical` donde se indican.
3. Mensajes con el nombre real del método o de la ruta; no inventar retornos.
4. Notas obligatorias de SEQ-06, SEQ-07 y SEQ-08.
