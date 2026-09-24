# ST-01 a ST-04 · Diagramas de estados

| | |
|---|---|
| **Objetivo** | Representar las máquinas de estado que el código define explícitamente |
| **Alcance** | `JobRequest`, `Vacancy`, `Application` y las sesiones (`Evaluation`/`Interview`). Solo transiciones que existen en `allowedTransitions()` o en un `CHECK` |
| **Fuente de verdad** | `app/Enums/JobRequestStatus.php`, `VacancyStatus.php`, `ApplicationStatus.php`, `AssessmentStatus.php`; `CHECK` de las migraciones; servicios que disparan cada transición |
| **Borradores textuales** | `puml/st-01-…` a `puml/st-04-…` |

Cada transición indica **disparador** (método del servicio), **actor** y **RF**. Una transición que el enum permite pero que ningún servicio usa se marca así.

## ST-01 · Requerimiento (`JobRequestStatus`)

| Desde | Hacia | Disparador | Actor | RF |
|---|---|---|---|---|
| ● | `borrador` | `JobRequestWorkflow::register` | Área solicitante | RF-01 |
| `borrador` | `enviado` | `submit` | Área solicitante (dueño) | RF-01/RF-02 |
| `enviado` | `observado` | `observe` (comentario obligatorio) | RR. HH. | RF-02 |
| `observado` | `enviado` | `submit` tras `correct` | Área solicitante (dueño) | RF-02 |
| `enviado` | `validado` | `validate` | RR. HH. | RF-02 |
| `validado` | `aprobado` | `approve` | Aprobador | RF-03 |
| `validado` | `rechazado` | `reject` (motivo obligatorio) / efecto: notificación | Aprobador | RF-03, RF-04 |

`aprobado` y `rechazado` son finales. Editable solo en `borrador` y `observado` (`isEditable()`); editar no cambia el estado. Desde `aprobado` RR. HH. puede crear **una** vacante (restricción de `Vacancy`, no un estado del requerimiento).

## ST-02 · Vacante (`VacancyStatus`)

| Desde | Hacia | Disparador | Actor | Guarda | RF |
|---|---|---|---|---|---|
| ● | `borrador` | `VacancyService::create` | RR. HH. | Requerimiento `aprobado` y sin vacante | RF-05, RF-06 |
| `borrador` | `publicada` | `VacancyService::publish` | RR. HH. | `VacancyValidator` sin observaciones | RF-07 |
| `publicada` | `cerrada` | `VacancyClosureService::close` | RR. HH. | Decisión final (RF-23) **y** selección (RF-24) registradas → `closure_type = con_seleccion` | RF-25 |

`cerrada` es final. La configuración solo se edita en `borrador`. `CHECK vacancies_closure_consistent` exige `closed_at` y `closure_type` al cerrar. **`desierta` existe en `VacancyClosureType` pero ningún servicio lo usa** (A-30): no se dibuja como transición; va como nota.

## ST-03 · Postulación (`ApplicationStatus`)

| Desde | Hacia | Disparador | Actor | RF |
|---|---|---|---|---|
| ● | `postulado` | `ApplicationService::apply` | Postulante | RF-10 |
| `postulado` | `preseleccionado` | `shortlist` | RR. HH. | RF-13 |
| `postulado`, `preseleccionado`, `en_evaluacion`, `en_entrevista`, `finalista` | `descartado` | `discard` (comentario obligatorio) | RR. HH. | RF-13 |
| `preseleccionado` | `en_evaluacion` | `moveTo` **o** automático al programar evaluación | RR. HH. | RF-14, RF-16 |
| `preseleccionado`, `en_evaluacion` | `en_entrevista` | `moveTo` **o** automático al programar entrevista | RR. HH. | RF-14, RF-18 |
| `en_evaluacion`, `en_entrevista` | `finalista` | `moveTo` | RR. HH. | RF-14 |
| `finalista` | `seleccionado` | `SelectionRegistrationService::register` | RR. HH. (tras la decisión del Aprobador) | RF-24 |
| `postulado` … `finalista` (no finales) | `no_seleccionado` | `VacancyClosureService::close` para las activas que no son la elegida | RR. HH. | RF-25 |

Finales: `seleccionado`, `no_seleccionado`, `descartado`.

Guardas que van como notas:

- **Destinos manuales** (`manualTargets()`): `preseleccionado`, `en_evaluacion`, `en_entrevista`, `finalista`, `descartado`. `seleccionado` y `no_seleccionado` **solo** por RF-24 y RF-25.
- **Tras la decisión final** (RF-23) no se admiten cambios manuales en esa vacante (A-28).
- **Vacante cerrada**: ningún cambio.
- **Como mucho una `seleccionado` por vacante** (índice parcial).
- Cada transición deja `ApplicationStageHistory`, se audita y, salvo las automáticas y la de RF-24, notifica al postulante (RF-15). El cierre notifica por RF-26.
- La decisión final (RF-23) **no** es una transición de la postulación: la elegida sigue en `finalista` hasta RF-24.

## ST-04 · Sesión de evaluación o entrevista (`AssessmentStatus`)

| Desde | Hacia | Disparador | Actor | RF |
|---|---|---|---|---|
| ● | `programada` | `AssessmentScheduler::scheduleEvaluation` / `scheduleInterview` | RR. HH. | RF-16, RF-18 |
| `programada` | `realizada` | `AssessmentResultRecorder::recordEvaluation` / `recordInterview` | Evaluador asignado | RF-19 |

`realizada` es final (los resultados no se vuelven a registrar). No hay cancelación ni reprogramación implementadas. Diagrama pequeño; F23 puede integrarlo como nota de CL-01 si prefiere no dibujarlo aparte.

## Instrucciones para F23

1. Un *Statechart Diagram* por entidad, con los estados con su valor real (`en_evaluacion`, no «En evaluación»; la etiqueta visible puede ir como alias).
2. Transiciones etiquetadas `disparador [guarda] / efecto`.
3. Notas de las guardas de ST-03 y de `desierta` en ST-02.
