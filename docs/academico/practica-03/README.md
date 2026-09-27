# Práctica 03 — Formato 03: Diagrama BPM del proceso actual (AS-IS)

Entregable de la Práctica 03 (Fase 27B): modelado BPMN del proceso actual analizado en el [Formato 02](../practica-02/README.md).

**Estado: BPMN AS-IS PRELIMINAR derivado del análisis del equipo.** No es un modelo validado por la institución ni el modelo formal de PowerDesigner.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F3_Diagrama_BPM_ASIS_Colegio_Andino.docx`](F3_Diagrama_BPM_ASIS_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 03 |
| [`F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf`](F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F3_Diagrama_BPM_ASIS_Colegio_Andino.md`](F3_Diagrama_BPM_ASIS_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`diagramas/draft/`](diagramas/draft/) | **Borrador** BPMN en carriles verticales, en dos partes unidas por el enlace A |
| [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) | Especificación para modelarlo formalmente en PowerDesigner (Fase 29) |
| [`evidencias/`](evidencias/README.md) | Evidencias del repositorio con su ruta y su SHA-256 |

## Especificación BPMN (resumen)

| Elemento | Contenido |
|---|---|
| Pools | «Colegio Andino de Huancayo — AS-IS preliminar» y «Postulante (externo)» |
| Lanes | Área solicitante, RR. HH., Dirección y Evaluadores |
| Evento de inicio | EI-01 «Necesidad de personal identificada» |
| Tareas | AS-01 a AS-14, las mismas del Formato 02 |
| Compuertas exclusivas | G-01 «¿Necesidad aprobada?» y G-02 «¿Preseleccionado?», que se evalúa por candidato |
| Eventos de fin | EF-01 «Necesidad no aprobada», EF-02 «El candidato no continúa» y EF-03 «Resultado comunicado» |
| Flujos de mensaje | Convocatoria, postulación y CV, citación, participación y resultado |

La descripción paso a paso y la lista de validación están en el formato.

## ¿Requiere PowerDesigner?

**Sí, para la versión formal.** La guía admite cualquier herramienta BPMN, pero el proyecto formaliza sus modelos en PowerDesigner. El borrador PNG solo sirve para revisar el contenido.

- **Cuándo se modela:** en la Fase 29, después de que la auditoría F27C apruebe el AS-IS.
- **Qué se modela:** está en [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md).
- **Estado de PowerDesigner en esta fase:** no se abrió y no se modificó ningún modelo.

## Limitaciones

- **Base del modelo:** hereda todas las limitaciones del AS-IS preliminar del Formato 02.
- **Validación:** la lista de validación del formato es interna del equipo; falta la validación institucional.
- **Pool del Postulante:** el borrador lo dibuja con tareas y eventos, pero sin sus eventos de inicio y fin propios. En PowerDesigner se decidirá si se modela como pool de caja negra.
