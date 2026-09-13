# Informe del diagrama BPMN TO-BE

## 1. Propósito

El BPMN TO-BE representa el proceso de reclutamiento, evaluación y selección **propuesto por el proyecto**, con la plataforma como soporte. Es la base de diseño de la línea base RF-01 a RF-27.

**Disponibilidad:**
- El BPMN TO-BE original forma parte de la documentación académica previa del equipo, pero **no se encuentra versionado en el repositorio actual** ni en la carpeta del curso revisada (`Diagramas/PD` solo contiene diagramas UML).
- La documentación del repositorio **no registra un número de actividades** del BPMN TO-BE. En particular, no aparece la referencia a 44 actividades, por lo que ese dato no puede contrastarse aquí.
- Al no disponer del BPMN, varias reglas se fijaron como supuestos explícitos (A-05, A-13 y A-16 en `docs/assumptions.md`).

El [capítulo 3](../03-procesos-negocio.md#33-proceso-to-be-propuesto) incluye un **diagrama de flujo derivado de la implementación**. **No es el BPMN original** ni debe presentarse como tal.

## 2. Elementos principales

**TO-BE documentado por escrito** (capítulo 3), organizado en cinco subprocesos:

| Subproceso | Actividades | Actores |
|---|---|---|
| A. Requerimiento de personal | Registrar → enviar → validar u observar (corrección y reenvío) → aprobar o rechazar con motivo | Área solicitante, RR. HH., Aprobador/Dirección |
| B. Convocatoria | Crear vacante desde requerimiento aprobado → perfil y criterios ponderados → validación → publicar | RR. HH. |
| C. Postulación | Cuenta → perfil y CV → postular → confirmación | Postulante |
| D. Evaluación | Revisar expediente → preseleccionar/descartar → programar evaluación y entrevista (convocatoria) → registrar puntajes y resultado → finalista | RR. HH., Evaluador |
| E. Selección y cierre | Ranking y comparación → **decisión final humana** → registrar selección → cerrar → notificar resultados → auditar | Sistema (cálculo), Aprobador/Dirección, RR. HH. |

## 3. Relación con requerimientos

| Elemento TO-BE | RF |
|---|---|
| Requerimientos de personal | RF-01 a RF-04 |
| Vacantes | RF-05 a RF-07, RF-20 |
| Postulaciones | RF-08 a RF-15 |
| Evaluaciones | RF-16, RF-17, RF-19, RF-20 |
| Entrevistas | RF-18, RF-19, RF-20 |
| Ranking y comparación | RF-21, RF-22 |
| Decisión | RF-23 |
| Selección | RF-24 |
| Cierre y resultado | RF-25, RF-26 |
| Auditoría | RF-27 |

## 4. Relación con implementación

| Elemento TO-BE | Implementación |
|---|---|
| Flujo del requerimiento | `JobRequestWorkflow`; estados `borrador → enviado → (observado → enviado) → validado → aprobado \| rechazado` |
| Vacantes | `VacancyService`, `VacancyValidator`, `WeightingValidator`; estados `borrador → publicada → cerrada` |
| Postulaciones | `ApplicationService`, `ApplicationStageService`; etapas de `ApplicationStatus` con historial |
| Evaluaciones y entrevistas | `AssessmentScheduler` (convocatorias), `AssessmentResultRecorder`, `ScoreSheetValidator` |
| Ranking | `RankingService` (puro, no selecciona) |
| Decisión | `FinalDecisionService` (solo Aprobador/Dirección; confirmación y justificación; no cambia estados) |
| Selección y cierre | `SelectionRegistrationService`, `VacancyClosureService` (con selección; demás a `no_seleccionado`) |
| Notificaciones | `app/Notifications/*` en cola |
| Auditoría | `AuditLogger`, `audit_logs` de solo inserción, `audit/index` |

Verificación: PHPUnit (244 pruebas, 0 fallidas) y Cypress E2E-13 (flujo integral de 12 pasos).

## 5. Consistencias

- La descripción escrita del TO-BE, los 27 RF, los supuestos aprobados y el código coinciden entre sí.
- El flujo integral está automatizado de extremo a extremo (E2E-13).
- La regla crítica («el sistema no selecciona; decide el Aprobador/Dirección») está presente en la documentación, el código y las pruebas.

## 6. Diferencias detectadas

- **Con el BPMN original:** no pueden determinarse sin el archivo. Puntos a revisar al anexarlo:
  - número y nombre de las actividades;
  - quién toma la decisión final;
  - si contempla el cierre sin selección, que no está implementado (A-30);
  - posibles indicadores de gestión (P5), que no están implementados.
- **Con el diagrama UML de selección:** existe una diferencia conocida, documentada en [08-selection-sequence-report.md](08-selection-sequence-report.md).

## 7. Limitaciones

- BPMN original no versionado; número de actividades no verificable desde el repositorio.
- El TO-BE es una **propuesta del proyecto**: su adopción en el Colegio Andino no está validada institucionalmente.
- El diagrama de flujo del capítulo 3 es derivado y no reemplaza al BPMN.

## 8. Estado para entrega

**Evidencia externa pendiente**, con TO-BE propuesto documentado por escrito y verificado contra la implementación.

## 9. Recomendación

1. Anexar el BPMN TO-BE original. Si registra un número de actividades (p. ej., 44), conservarlo tal como está y contrastar cada actividad con la tabla de la sección 4.
2. Donde el BPMN difiera de la implementación, indicar que la versión vigente es la línea base RF-01 a RF-27 y las pruebas automatizadas, o actualizar el BPMN en una futura versión.
3. Mantener el rótulo «TO-BE propuesto» en todas sus menciones.
