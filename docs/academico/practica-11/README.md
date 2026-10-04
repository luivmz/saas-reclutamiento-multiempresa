# Práctica 11 — Formato 11: Arquitectura del sistema

Arquitectura conceptual del sistema. La carpeta contiene dos versiones del entregable:

| Versión | Entregable | Estado |
|---|---|---|
| **Definitiva** (fase F11-R, 29/09/2026) | [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_Colegio_Andino.docx) · [PDF](F11_Arquitectura_del_Sistema_Colegio_Andino.pdf) · [espejo `.md`](F11_Arquitectura_del_Sistema_Colegio_Andino.md) | Regularizada sobre la **plantilla oficial del Formato 11**, recibida después de la F28. Misma arquitectura. Pendiente de auditoría. Registro: [`F11R_REGULARIZACION.md`](F11R_REGULARIZACION.md) |
| **Histórica** (Fases 28 y 29) | [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) · [PDF](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) | Adaptación académica hecha cuando el Formato 11 oficial no estaba disponible. Válida en esas condiciones y **conservada sin cambios**. El resto de este README la describe tal como se entregó |

**Equivalencia de identificadores.** La versión definitiva usa CMP-01 a CMP-17, que exige el formato oficial. Equivalen uno a uno a los identificadores históricos C01 a C17, que conservan `COMPONENTS.md`, `RELATIONSHIPS.md` y el diagrama ARQ-01. Las relaciones R-01 a R-20 no cambian.

## Versión histórica: adaptación académica (Fase 28)

Entregable de la Fase 28: la arquitectura conceptual del sistema.

> **Documento adaptado académicamente a partir de la Guía de Práctica N.° 11, porque durante la F28 la institución no había proporcionado el Formato 11 oficial.** La versión adaptada no es una plantilla oficial ni pretende serlo. La plantilla oficial se incorporó al repositorio el 29/09/2026 y es la base de la versión definitiva (F11-R).

**Estado:** versión 1.1 (28/09/2026). Integra la vista formal ARQ-01 de PowerDesigner (F29 y F29B); la versión 1.0 se auditó en la F28. La validación es estructural, académica e interna del equipo: **no hay aprobación institucional**.

## Fuentes

| Tipo | Fuente |
|---|---|
| Normativa | [`GUIA_PRACTICA_11.docx`](../00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx). Exigencias: revisar el alcance, analizar los casos de uso, identificar los componentes, definir sus relaciones, representar la arquitectura conceptual y validarla |
| Académica | F2 a F9 ([`practica-02`](../practica-02/README.md) a [`practica-09`](../practica-09/F9_POST_RELEASE_ADDENDUM.md)), [`ACADEMIC_BASELINE.md`](../ACADEMIC_BASELINE.md) y [`trazabilidad/F2-F9-traceability.md`](../trazabilidad/F2-F9-traceability.md) |
| Técnica (referencia, sin modificar) | CO-01 y PK-01 ([`component-model.md`](../../v1.1/uml/component-model.md)), DE-01, UC-01, SEQ-07 y SEQ-08 (`docs/v1.1/uml/`); exportaciones de la F23; [capítulo 7](../../final-report/07-arquitectura-tecnologica.md) |
| Diseño visual | Paquete del F9 v1.1 (portada, cabecera, pie y estilos), usado en memoria. **El F9 no se modifica** |

## Artefactos

| Archivo | Contenido |
|---|---|
| [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_Colegio_Andino.docx) · [PDF](F11_Arquitectura_del_Sistema_Colegio_Andino.pdf) · [`.md`](F11_Arquitectura_del_Sistema_Colegio_Andino.md) | **Entregable definitivo (F11-R)**, sobre la plantilla oficial: 8 secciones oficiales |
| [`F11R_REGULARIZACION.md`](F11R_REGULARIZACION.md) | Registro de la regularización: matriz de correspondencia, CMP ↔ C, R-01 a R-20, diferencias y fuentes con SHA-256 |
| [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) | **Entregable histórico** (F28 y F29): portada con la nota de adaptación y 14 secciones |
| [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.md`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`COMPONENTS.md`](COMPONENTS.md) | 17 componentes: responsabilidad, RF, CU, actores, estado y fuente. Incluye las exclusiones y las capas |
| [`RELATIONSHIPS.md`](RELATIONSHIPS.md) | 20 relaciones: tipo, información, dependencia, RF/CU y observación. Incluye el flujo de información y el de RF-29 aparte |
| [`VALIDATION.md`](VALIDATION.md) | Matriz de validación (A–H), validación de componentes y de relaciones |
| [`F28_VALIDATION.md`](F28_VALIDATION.md) | Exigencias de la Guía 11 frente a la evidencia |
| [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) | Especificación de la vista ARQ-01 para la F29 (**FORMALIZED / INTEGRATED / DONE**) |
| [`ARQ01_Arquitectura_Conceptual_PowerDesigner.png`](../powerdesigner/evidencias/capturas/ARQ01_Arquitectura_Conceptual_PowerDesigner.png) | Captura real de PowerDesigner de la vista ARQ-01 |
| [`diagramas/draft/`](diagramas/draft/) | Borrador del diagrama conceptual (PNG) — **DRAFT / SUPERSEDED BY F29 FORMAL EXPORT** |
| [`../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png`](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png) · [SVG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.svg) | **Exportación formal de PowerDesigner (F29)**, diagrama «ARQ-01 - Arquitectura Conceptual» |
| [`evidencias/`](evidencias/README.md) | Manifiesto de evidencias: archivo, ruta, SHA-256 y uso |

Trazabilidad componente → RF → CU → RNF → alcance → artefacto: [`../trazabilidad/F11-architecture-traceability.md`](../trazabilidad/F11-architecture-traceability.md).

## Estructura del documento

1. Datos generales (incluye la correspondencia con la Guía 11)
2. Contexto y alcance arquitectónico
3. Casos de uso que condicionan la arquitectura
4. Componentes principales
5. Responsabilidades
6. Relaciones entre componentes
7. Flujo de información (con el de RF-29 aparte)
8. Arquitectura conceptual (con la técnica de referencia)
9. Decisiones arquitectónicas y relación RNF → decisiones
10. Validación
11. Limitaciones y observaciones
12. Conclusiones
13. Evidencias
14. Trazabilidad

## Decisiones de modelado verificadas con evidencia

| Decisión | Motivo |
|---|---|
| **17 componentes**, dentro del rango de 12 a 18 | Se validó la propuesta del encargo componente por componente |
| «Gestión de organizaciones» pasa a **C03 Autorización y contexto multiempresa** (transversal) | No hay gestión de organizaciones en el código |
| **Evaluaciones y entrevistas en un solo componente** (C08) | Es un solo módulo, con programación y registro compartidos |
| **Decisión final humana (C10) separada de selección y cierre (C11)** | Deja visible la frontera de RF-23 |
| **Reportes / panel operativo no es un componente** | RF-28 es un candidato no implementado (X-01) |
| **C17 (RF-29) es experimental y opcional**, sin relación con el ranking, la decisión ni la selección | Frontera del ML (ADR-001) |

## Limitaciones

- **Formato:** es una adaptación académica, porque en la F28 no se disponía del Formato 11 oficial. Se incorporó el 29/09/2026 y la F11-R regularizó el entregable sobre él.
- **Punto de partida:** el AS-IS (F2 a F4) es preliminar.
- **RNF no verificados:** RNF-06 (rendimiento) y RNF-07 (disponibilidad y recuperabilidad).
- **H-14:** RESUELTA en F31 mediante la conservación de la referencia oficial de cabecera del F4.
- **F28-L01:** NO APLICA. La revisión visual de F31 confirma que el F11 adaptado histórico sí dibuja su encabezado y «Asignatura»; la omisión era propia del extractor usado en F28. El artefacto histórico no se modifica.
- **RF-28:** no implementado.
- **RF-29:** experimental.
- **Aprobación:** no hay aprobación institucional.
- **Diagrama:** el DOCX y el PDF definitivo usan la vista formal ARQ-01 de la F29 (ver «Formalización F29»). F29-L02 quedó RESUELTA en F31 mediante offsets de rótulos persistidos y reexportados; el adaptado histórico conserva la exportación que le correspondía. Hasta el 28/09/2026 se usaba el borrador.

## Relación con la F29 (estado al cierre de la F28)

La vista ARQ-01 está especificada en [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) y figura en la [lista de trabajo de PowerDesigner](../POWERDESIGNER_WORKLIST.md) como READY FOR POWERDESIGNER, condicionada a la auditoría de la F28. PowerDesigner no se abrió en esta fase.

## Formalización F29

La vista se formalizó en PowerDesigner en la F29: diagrama «ARQ-01 - Arquitectura Conceptual» del modelo [`F29_UML_Academico.oom`](../powerdesigner/models/F29_UML_Academico.oom), paquete ARQ01, con exportaciones [PNG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png) y [SVG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.svg). Validación en [`F29_VALIDATION.md`](../powerdesigner/F29_VALIDATION.md) y trazabilidad por elemento en [`F29-powerdesigner-traceability.md`](../trazabilidad/F29-powerdesigner-traceability.md).

**Integración posterior a la F29 (28/09/2026): FORMALIZED / INTEGRATED / DONE.** Tras las auditorías F29 y F29B, el DOCX y el PDF del Formato usan la exportación formal como diagrama principal (figura 1: vista ARQ-01 completa en página horizontal; figuras 2 y 3: ampliaciones de sus dos mitades). Criterio de aceptación de [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) cumplido. Capturas reales de PowerDesigner: [`ARQ01_Arquitectura_Conceptual_PowerDesigner.png`](../powerdesigner/evidencias/capturas/ARQ01_Arquitectura_Conceptual_PowerDesigner.png). Las fuentes, con su SHA-256, están en [`evidencias/`](evidencias/README.md). El borrador de [`diagramas/draft/`](diagramas/draft/) se conserva como antecedente: **DRAFT / SUPERSEDED BY F29 FORMAL EXPORT**.
