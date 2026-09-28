# Pendiente de PowerDesigner — F3 BPMN AS-IS

**Actualización F29 (27/09/2026): FORMALIZED / DONE**, pendiente de la auditoría F29. Diagrama «F3 - BPMN AS-IS» en [`F29_BPM_Academico.bpm`](../powerdesigner/models/F29_BPM_Academico.bpm) (paquete F3); exportaciones [PNG](../powerdesigner/exports/F3_BPMN_ASIS.png) y [SVG](../powerdesigner/exports/F3_BPMN_ASIS.svg); verificación en [`F29_VALIDATION.md`](../powerdesigner/F29_VALIDATION.md). El estado anterior se conserva a continuación.

**Estado: READY FOR POWERDESIGNER.** Especificación cerrada en la F27D, que resolvió los hallazgos H-01, H-02 y H-13 de la auditoría F27C. Se modela en la **Fase 29**. En las F27B y F27D no se abrió PowerDesigner ni se tocó ningún `.oom` o `.pdm`, y las 22 vistas de la F23 siguen igual.

Esta especificación permite construir el modelo **sin reinterpretar nada**. Si algo del modelo no está aquí, no se agrega.

## Qué debe modelarse

Un diagrama BPMN **nuevo** del proceso actual (AS-IS preliminar) de reclutamiento, evaluación y selección del Colegio Andino de Huancayo. Es un modelo de negocio, no del software: no se mezcla con el OOM o el PDM de la F23 ni reemplaza AC-01.

Nombre: «F3 BPMN AS-IS preliminar — Reclutamiento y selección».

## Glosario (nombre oficial único de cada elemento)

| ID | Tipo | Nombre oficial |
|---|---|---|
| EI-01 | Evento de inicio (pool Colegio) | Necesidad de personal identificada |
| G-01 | Compuerta exclusiva | ¿Necesidad aprobada? |
| EF-01 | Evento de fin del proceso | Necesidad no aprobada |
| SP-01 | Subproceso expandido de instancia múltiple **paralela** (una instancia por candidato) | Evaluar al candidato |
| SI-01 | Evento de inicio de SP-01 | Candidato a evaluar |
| G-02 | Compuerta exclusiva (dentro de SP-01) | ¿Candidato preseleccionado? |
| EF-02 | Evento de fin de SP-01 | El candidato no continúa |
| EF-04 | Evento de fin de SP-01 | Candidato evaluado |
| EF-03 | Evento de fin del proceso | Resultado comunicado |
| EP-01 | Evento de inicio de mensaje (pool Postulante) | Convocatoria recibida |
| EP-02 | Evento de fin (pool Postulante) | Postulación presentada |

**No hay otros eventos.** En particular, no hay eventos intermedios de mensaje en el pool del Postulante: ver «Pools».

## Pools y lanes

| Pool | Lanes | Definición |
|---|---|---|
| Colegio Andino de Huancayo — AS-IS preliminar | Área solicitante · RR. HH. · Dirección · Evaluadores | Caja blanca |
| **Postulante** | — | **Participante visible (caja blanca) con comportamiento mínimo:** EP-01 → AS-07 → EP-02. **No** es un pool de caja negra. MF-03 y MF-04 llegan al **borde del pool**, sin evento receptor interno, porque el AS-IS no documenta cómo reacciona el postulante |

No hay lane de «Sistemas»: el AS-IS no identifica ninguna herramienta informática del Colegio.

## Tareas

| ID | Tarea | Pool / lane | Tipo |
|---|---|---|---|
| AS-01 | Identificar la necesidad de personal | Colegio / Área solicitante | Tarea |
| AS-02 | Comunicar la necesidad a RR. HH. | Colegio / Área solicitante | Tarea |
| AS-03 | Revisar la necesidad | Colegio / RR. HH. | Tarea |
| AS-04 | Aprobar o no aprobar la necesidad | Colegio / Dirección | Tarea |
| AS-05 | Definir el perfil del puesto | Colegio / RR. HH. | Tarea |
| AS-06 | Difundir la convocatoria | Colegio / RR. HH. | Tarea (envía MF-01) |
| AS-07 | Presentar la postulación y el CV | Postulante | Tarea (envía MF-02) |
| AS-08 | Recibir y reunir postulaciones y CV | Colegio / RR. HH. | **Tarea de recepción** (recibe MF-02) |
| AS-09 | Revisar el CV y preseleccionar al candidato | Colegio / RR. HH., **dentro de SP-01** | Tarea |
| AS-10 | Coordinar evaluaciones y entrevistas | Colegio / RR. HH., **dentro de SP-01** | Tarea (envía MF-03) |
| AS-11 | Realizar evaluaciones y entrevistas | Colegio / Evaluadores, **dentro de SP-01** | Tarea |
| AS-12 | Consolidar resultados y comparar candidatos | Colegio / RR. HH. | Tarea |
| AS-13 | Decidir el candidato seleccionado | Colegio / Dirección | Tarea |
| AS-14 | Comunicar el resultado | Colegio / RR. HH. | Tarea (envía MF-04) |

## Subproceso

**SP-01 «Evaluar al candidato»** es un subproceso expandido de **instancia múltiple paralela**: una instancia por candidato cuya postulación reunió AS-08.

- **Contenido:** SI-01 → AS-09 → G-02 → [No] EF-02 | [Sí] AS-10 → AS-11 → EF-04.
- **Fin:** SP-01 termina cuando **todas** sus instancias terminaron (por EF-02 o por EF-04).
- **Continuación:** el flujo sigue hacia AS-12.

## Decisiones

| ID | Compuerta | Lane | Salidas |
|---|---|---|---|
| G-01 | ¿Necesidad aprobada? | Dirección | Sí → AS-05 · No → EF-01 |
| G-02 | ¿Candidato preseleccionado? | RR. HH. (dentro de SP-01) | Sí → AS-10 · No → EF-02 |

## Flujos de secuencia (pool Colegio)

EI-01 → AS-01 → AS-02 → AS-03 → AS-04 → G-01 → [Sí] AS-05 → AS-06 → **AS-08** → SP-01 → AS-12 → AS-13 → AS-14 → EF-03. Además, G-01 → [No] EF-01.

**Pool Postulante:** EP-01 → AS-07 → EP-02.

## Flujos de mensaje (lista cerrada, todos unidireccionales)

| ID | Origen | Destino | Elemento receptor | Contenido |
|---|---|---|---|---|
| MF-01 | AS-06 (Colegio, RR. HH.) | Postulante | EP-01 Convocatoria recibida | Convocatoria |
| MF-02 | AS-07 (Postulante) | Colegio, RR. HH. | AS-08 (tarea de recepción) | Postulación y CV |
| MF-03 | AS-10 (Colegio, RR. HH., dentro de SP-01) | Postulante | Borde del pool Postulante | Citación |
| MF-04 | AS-14 (Colegio, RR. HH.) | Postulante | Borde del pool Postulante | Resultado |

No hay mensajes bidireccionales ni otros mensajes.

## Anotaciones obligatorias

- En el pool del Colegio: «AS-IS preliminar derivado del análisis del equipo, sujeto a validación institucional».
- En EF-02: «No está verificado si se informa al candidato que no continúa».

## Criterio de aceptación

1. **Elementos:** coinciden uno a uno con este documento y con el Formato 03:
   - 14 tareas;
   - 1 subproceso de instancia múltiple;
   - 2 compuertas;
   - 6 eventos del Colegio y de SP-01, más 2 del Postulante;
   - 4 mensajes.

   No se agrega ninguna actividad, actor, herramienta ni evento.
2. **Glosario:** cada nombre coincide literalmente con el glosario.
3. **Conexión:** todas las actividades están conectadas y AS-06 → AS-08 es un flujo de secuencia.
4. **Modelos existentes:** no se modifica ningún diagrama de la F23 (OOM, PDM ni exportaciones).
5. **Exportación:** PNG y SVG, y el borrador del Formato 03 se sustituye solo tras una nueva auditoría.
