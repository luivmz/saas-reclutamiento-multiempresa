# Pendiente de PowerDesigner — F3 BPMN AS-IS

**Estado: REQUIERE POWERDESIGNER.** Se modela en la **Fase 29**, solo después de que la auditoría **F27C** apruebe el contenido del AS-IS. En la F27B no se abrió PowerDesigner ni se tocó ningún modelo `.oom` o `.pdm`, y los 22 diagramas de la F23 siguen igual.

## Qué debe modelarse

Un diagrama BPMN del **proceso actual (AS-IS preliminar)** de reclutamiento, evaluación y selección de personal del Colegio Andino de Huancayo. Es un modelo de **negocio**, no del software. Va en un modelo **nuevo** (por ejemplo, un BPM de PowerDesigner) o en un paquete propio. **No** se mezcla con el OOM o el PDM de la F23 ni reemplaza AC-01.

Nombre sugerido: «F3 BPMN AS-IS preliminar — Reclutamiento y selección».

## Pools y lanes

| Pool | Lanes | Nota |
|---|---|---|
| Colegio Andino de Huancayo — AS-IS preliminar | Área solicitante · RR. HH. · Dirección · Evaluadores | Actores internos |
| Postulante | — | Externo. Decidir si va como pool de caja negra (solo mensajes) o con sus propios inicio y fin |

No hay lane de «Sistemas»: el AS-IS no identifica ninguna herramienta informática del Colegio.

## Eventos

| ID | Tipo | Lane | Nombre |
|---|---|---|---|
| EI-01 | Inicio | Área solicitante | Necesidad de personal identificada |
| EF-01 | Fin | Dirección | Necesidad no aprobada |
| EF-02 | Fin | RR. HH. | El candidato no continúa |
| EF-03 | Fin | RR. HH. | Resultado comunicado |

## Tareas (con su lane)

| ID | Tarea | Lane |
|---|---|---|
| AS-01 | Identificar la necesidad de personal | Área solicitante |
| AS-02 | Comunicar la necesidad a RR. HH. | Área solicitante |
| AS-03 | Revisar la necesidad | RR. HH. |
| AS-04 | Aprobar o no aprobar la necesidad | Dirección |
| AS-05 | Definir el perfil del puesto | RR. HH. |
| AS-06 | Difundir la convocatoria | RR. HH. |
| AS-07 | Presentar la postulación y el CV | Postulante |
| AS-08 | Recibir y reunir postulaciones y CV | RR. HH. |
| AS-09 | Revisar y preseleccionar candidatos | RR. HH. |
| AS-10 | Coordinar evaluaciones y entrevistas | RR. HH. |
| AS-11 | Realizar evaluaciones y entrevistas | Evaluadores |
| AS-12 | Consolidar resultados y comparar candidatos | RR. HH. |
| AS-13 | Decidir el candidato seleccionado | Dirección |
| AS-14 | Comunicar el resultado | RR. HH. |

## Decisiones

| ID | Compuerta | Lane | Salidas |
|---|---|---|---|
| G-01 | Exclusiva «¿Necesidad aprobada?» | Dirección | Sí → AS-05 · No → EF-01 |
| G-02 | Exclusiva «¿Candidato preseleccionado?» | RR. HH. | Sí → AS-10 · No → EF-02. **Por candidato:** modelar AS-09 a AS-11 como subproceso o tarea de instancia múltiple, o anotarlo |

## Secuencia

EI-01 → AS-01 → AS-02 → AS-03 → AS-04 → G-01 → [Sí] AS-05 → AS-06 → AS-08 (tras AS-07) → AS-09 → G-02 → [Sí] AS-10 → AS-11 → AS-12 → AS-13 → AS-14 → EF-03.

Flujos de mensaje:

- AS-06 → Postulante (convocatoria);
- AS-07 → AS-08 (postulación y CV);
- AS-10 → Postulante (citación);
- AS-11 ↔ Postulante (participación);
- AS-14 → Postulante (resultado).

## Criterio de aceptación

1. **Elementos:** los 14 IDs de tarea, las 2 compuertas y los 4 eventos coinciden **uno a uno** con el Formato 03 aprobado en la F27C. No se añade ninguna actividad, actor ni herramienta.
2. **Lanes:** cada tarea está en el lane indicado.
3. **Anotación visible:** «AS-IS preliminar derivado del análisis del equipo, sujeto a validación institucional».
4. **Modelos existentes:** no se modifica ningún diagrama de la F23 (OOM, PDM ni exportaciones).
5. **Exportación:** PNG y SVG con el mismo nombre que el diagrama, y se reemplaza el borrador en el Formato 03 solo tras una nueva auditoría.
