# Informe del diagrama de secuencia de evaluación y entrevista

## 1. Propósito

Representar cómo el evaluador consulta una sesión asignada y registra puntajes, resultado y observaciones.

**Artefacto original:** `Diagramas/PD/secuencioaEvaluacion.oom` (PowerDesigner, carpeta del curso, fuera del repositorio). No se modificó.

## 2. Elementos principales

**Líneas de vida del diagrama original:** Evaluador (actor), React, Laravel, Policy, PostgreSQL.

**Mensajes del diagrama original:**
1. Seleccionar candidato → Solicitar detalle de evaluación → Consultar evaluación y candidato → Retornar datos → Mostrar formulario de evaluación.
2. Registrar puntajes y observaciones → Enviar evaluación → Validar permiso de entrevista → Evaluador autorizado.
3. Guardar entrevista → Guardar resultado de evaluación → Confirmar registro → Confirmar entrevista registrada → Mostrar confirmación.

## 3. Relación con requerimientos

- RF-16 (programar evaluación) y RF-18 (programar entrevista), como precondición.
- RF-17 (convocatoria).
- RF-19 (registrar entrevista y resultado).
- RF-20 (validar rangos).

## 4. Relación con implementación

| Paso | Implementación real |
|---|---|
| Actor y entrada | Evaluador autenticado; `GET /mis-evaluaciones` (`AssessmentAssignmentController`, middleware `role:evaluador`) → `GET /evaluaciones/{id}` o `/entrevistas/{id}` |
| Validación de permisos | `EvaluationPolicy` / `InterviewPolicy` (`AuthorizesAssessmentSessions`): solo el evaluador asignado de la misma organización |
| Validaciones de negocio | `RecordScoresRequest` / `RecordInterviewResultRequest` + `ScoreSheetValidator`: puntaje para **todos** los criterios de la etapa y dentro de su rango (RF-20). La entrevista exige resultado y observaciones (A-20). Registro único, bloqueado si la vacante está cerrada (A-19) |
| Servicio | `AssessmentResultRecorder::recordEvaluation` / `recordInterview` |
| Persistencia | `evaluation_results` / `interview_results` (una fila por criterio, `UNIQUE`); sesión en estado `realizada` con `completed_at` |
| Notificación | No se notifica al postulante (A-21: no ve puntajes). La convocatoria previa (RF-17) la envía `AssessmentScheduler` al programar |
| Auditoría | `evaluacion.resultado_registrado` / `entrevista.resultado_registrado` (solo número de criterios y resultado, sin comentarios) |

**Pruebas:**
- PHPUnit: `EvaluationTest` (11), `InterviewTest` (7), `ScoreSheetValidatorTest` (unitaria).
- Cypress: E2E-07 y E2E-13 (evaluación y entrevista).

## 5. Consistencias

- El actor, los participantes y la secuencia básica (consultar, validar el permiso con Policy, guardar el resultado, confirmar) coinciden con la implementación.
- La validación de autorización del evaluador existe y está probada.

## 6. Diferencias detectadas

- El diagrama **mezcla evaluación y entrevista** en una sola secuencia («Validar permiso de entrevista», «Guardar entrevista» y «Guardar resultado de evaluación» en el mismo flujo). La implementación las separa en dos entidades, rutas, Policies y registros, cada una con sus criterios de etapa (`evaluacion` / `entrevista`).
- El diagrama no muestra la validación de rangos ni la obligatoriedad de todos los criterios (`ScoreSheetValidator`).
- El diagrama no muestra la auditoría ni el bloqueo por vacante cerrada.

## 7. Limitaciones

El artefacto está fuera del repositorio; su nombre de archivo tiene una errata («secuencioa»). Es una versión preliminar anterior a la separación evaluación/entrevista.

## 8. Estado para entrega

**Vigente con observaciones.**

## 9. Recomendación

En una futura versión gráfica:
- separar la secuencia de evaluación y la de entrevista (o usar fragmentos alternativos);
- incluir la validación de rangos (RF-20) y la auditoría;
- corregir el nombre del archivo.
