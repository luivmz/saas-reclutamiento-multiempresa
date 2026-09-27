# Práctica 03 — Formato 03: Diagrama BPM del proceso actual (AS-IS)

Entregable de la Práctica 03: modelado BPMN del proceso actual analizado en el [Formato 02](../practica-02/README.md). Lo elaboró la F27B y la F27D corrigió su especificación tras la auditoría F27C.

**Estado: BPMN AS-IS PRELIMINAR derivado del análisis del equipo.** No es un modelo validado por la institución ni el modelo formal de PowerDesigner.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F3_Diagrama_BPM_ASIS_Colegio_Andino.docx`](F3_Diagrama_BPM_ASIS_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 03 |
| [`F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf`](F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F3_Diagrama_BPM_ASIS_Colegio_Andino.md`](F3_Diagrama_BPM_ASIS_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`diagramas/draft/`](diagramas/draft/) | **Borrador** BPMN en carriles verticales, en dos partes unidas por el enlace A |
| [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) | Especificación cerrada para modelarlo en PowerDesigner (**READY FOR POWERDESIGNER**, Fase 29) |
| [`evidencias/`](evidencias/README.md) | Evidencias del repositorio con su ruta y su SHA-256 |

## Especificación BPMN (resumen)

| Elemento | Contenido |
|---|---|
| Pools | «Colegio Andino de Huancayo — AS-IS preliminar» (caja blanca) y «Postulante», participante visible con comportamiento mínimo: EP-01 → AS-07 → EP-02 |
| Lanes | Área solicitante, RR. HH., Dirección y Evaluadores |
| Tareas | AS-01 a AS-14. AS-08 es una tarea de recepción |
| Subproceso | **SP-01 «Evaluar al candidato»**, de instancia múltiple paralela (una instancia por candidato), con AS-09 a AS-11 |
| Compuertas exclusivas | G-01 «¿Necesidad aprobada?» y G-02 «¿Candidato preseleccionado?» (dentro de SP-01) |
| Eventos | EI-01, EF-01 y EF-03 del proceso; SI-01, EF-02 y EF-04 de SP-01; EP-01 y EP-02 del Postulante |
| Mensajes | MF-01 a MF-04, unidireccionales, con origen, destino y elemento receptor |

El **glosario** de nombres oficiales está en el formato y en [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md). Cada ID tiene un solo nombre en todos los artefactos. Por ejemplo, G-02 es siempre «¿Candidato preseleccionado?» y EF-02 es siempre «El candidato no continúa».

## Correcciones de la F27D

| Hallazgo | Corrección |
|---|---|
| H-01 | Pool del Postulante definido de una sola forma; SP-01 de instancia múltiple sin opciones abiertas; mensajes en una lista cerrada y unidireccional; eventos enumerados |
| H-02 | AS-06 → AS-08 es un flujo de secuencia y AS-08 es una tarea de recepción. El punto «todas las actividades están conectadas» del checklist ya es verdadero |
| H-13 | Glosario único. Se retiraron las variantes «¿Preseleccionado?» y los eventos intermedios del Postulante |

## Limitaciones

- **Base del modelo:** hereda las limitaciones del AS-IS preliminar del Formato 02.
- **Tipos de actor:** el de los evaluadores y el del postulante son **supuestos de modelado**.
- **Validación:** la validación del formato es interna del equipo; falta la validación institucional.
