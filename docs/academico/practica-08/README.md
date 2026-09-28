# Práctica 08 — Formato 08: Diagrama de casos de uso

Entregable de la Práctica 08 (Fase 27B): actores y casos de uso de la línea base RF-01 a RF-27. Consolida las tres vistas que ya existían, **sin destruir ninguna**.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F8_Diagrama_Casos_de_Uso_Colegio_Andino.docx`](F8_Diagrama_Casos_de_Uso_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 08 |
| [`F8_Diagrama_Casos_de_Uso_Colegio_Andino.pdf`](F8_Diagrama_Casos_de_Uso_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F8_Diagrama_Casos_de_Uso_Colegio_Andino.md`](F8_Diagrama_Casos_de_Uso_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`diagramas/draft/`](diagramas/draft/) | **Borrador** del diagrama académico con los 5 actores y los 20 CU — **DRAFT / SUPERSEDED BY F29 FORMAL EXPORT** |
| [`../powerdesigner/exports/F8_Casos_de_Uso_Academicos.png`](../powerdesigner/exports/F8_Casos_de_Uso_Academicos.png) · [SVG](../powerdesigner/exports/F8_Casos_de_Uso_Academicos.svg) | **Exportación formal de PowerDesigner (F29)**, diagrama «F8 - Casos de Uso Academicos» |
| [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) | Adaptación formal de la vista académica (Fase 29) |
| [`evidencias/`](evidencias/README.md) | Evidencias, incluida una copia del antecedente del anexo B del F9 v1.0 |

## Las tres vistas

| Vista | Fuente | Casos | Uso |
|---|---|---|---|
| A. CU académicos | F9 (tablas 5 y 8) | CU-01 a CU-20 | Vista del curso (Formatos 08 y 09) |
| B. CU agrupados | Informe v1.0, capítulo 4 §4.4 | CU-01 a CU-13 | Historia de la v1.0 |
| C. UC-RF técnicos | [`docs/v1.1/uml/use-cases.md`](../../v1.1/uml/use-cases.md) y UC-01 de PowerDesigner | UC-RF01 a UC-RF29 | Trazabilidad técnica: un caso por RF |

El formato incluye la **matriz de correspondencia** CU académico ↔ CU agrupado ↔ UC-RF ↔ actor ↔ RF ↔ alcance (bloque IN del F9), y conserva la tabla de los 13 CU agrupados. No se renumera ninguna vista.

## Actores

| ID | Actor |
|---|---|
| ACT-01 | Área solicitante |
| ACT-02 | Recursos Humanos |
| ACT-03 | Aprobador / Dirección (decisión final humana) |
| ACT-04 | Postulante |
| ACT-05 | Evaluador |

El Sistema **no** es un actor. No hay superadministrador ni facturación.

## Decisión del equipo sobre los casos de uso (F27D)

| ID | Decisión |
|---|---|
| D-CU-01 | Los **20 casos de uso académicos** (CU-01 a CU-20) quedan **aprobados**. No se amplía el catálogo |
| D-CU-02 | CU-18 se renombra a **«Registrar decisión final humana»**. RF-23 conserva su ID. Alias histórico: «Registrar decisión final» |
| D-CU-03 | **CU-21 «Consultar auditoría»: DIFERIDO.** No forma parte del catálogo de esta versión |
| D-CU-04 | La consulta de auditoría es una **capacidad técnica vinculada a RF-27** |

**Nota técnica.** Consulta de auditoría vinculada a RF-27 y ACT-03; cubierta por la vista técnica UC-RF27 y fuera del catálogo académico CU-01..CU-20 de esta versión.

En la trazabilidad, RF-23 va solo a CU-18 → UC-RF23 (bloque IN-07). RF-27 es transversal → UC-RF27 (bloque IN-08) y no se mezcla con RF-23.

## Observaciones

| ID | Observación |
|---|---|
| O-F8-01 | **Nombres de los CU. Resuelto:** el equipo aprobó los 20 CU y el nuevo nombre de CU-18 (D-CU-01 y D-CU-02) |
| O-F8-02 | **Consulta de auditoría. Resuelto como DIFERIDO:** CU-21 no se crea (D-CU-03 y D-CU-04) |
| O-F8-03 | **CU-16.** Es un caso incluido, sin actor directo. En UML es válido |
| O-F8-04 | **CU-10.** Además de RR. HH., se asocia al Aprobador, igual que en la implementación (UC-RF12). El F9 publicado no se modifica |
| O-F8-05 | **Entrevista.** También envía la convocatoria de RF-17 |
| O-F8-06 | **Antecedente superado.** El diagrama de CU del F9 v1.0 (anexo B) tenía actores fuera del alcance; se conserva solo como evidencia |
| O-F8-07 | **Extensiones.** RF-28 y RF-29 no están en los 20 CU; solo aparecen en la vista técnica UC-RF |

## ¿Requiere PowerDesigner?

Para una **adaptación formal** de la vista académica, sí. Está **lista para PowerDesigner** ([`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md)) y se hará en la Fase 29. **UC-01 de la F23 no se modifica**: se usa como referencia técnica en el formato.

## Formalización F29

La vista se formalizó en PowerDesigner en la F29: diagrama «F8 - Casos de Uso Academicos» del modelo [`F29_UML_Academico.oom`](../powerdesigner/models/F29_UML_Academico.oom), paquete F8, con exportaciones [PNG](../powerdesigner/exports/F8_Casos_de_Uso_Academicos.png) y [SVG](../powerdesigner/exports/F8_Casos_de_Uso_Academicos.svg). Validación en [`F29_VALIDATION.md`](../powerdesigner/F29_VALIDATION.md) y trazabilidad por elemento en [`F29-powerdesigner-traceability.md`](../trazabilidad/F29-powerdesigner-traceability.md).

El borrador de [`diagramas/draft/`](diagramas/draft/) queda como **DRAFT / SUPERSEDED BY F29 FORMAL EXPORT**. El DOCX y el PDF del Formato siguen con el borrador: se sustituyen solo después de la auditoría F29 (criterio de aceptación de [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md)).
