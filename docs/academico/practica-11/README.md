# Práctica 11 — Formato 11: Arquitectura del sistema (adaptación académica)

Entregable de la Fase 28: la arquitectura conceptual del sistema.

> **Documento adaptado académicamente a partir de la Guía de Práctica N.° 11. La institución no proporcionó un Formato 11 oficial.** Ningún archivo de esta carpeta es una plantilla oficial ni pretende serlo.

**Estado:** versión 1.0, lista para auditoría. La validación es estructural, académica e interna del equipo: **no hay aprobación institucional**.

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
| [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) | **Entregable**: portada con la nota de adaptación y 14 secciones |
| [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.md`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`COMPONENTS.md`](COMPONENTS.md) | 17 componentes: responsabilidad, RF, CU, actores, estado y fuente. Incluye las exclusiones y las capas |
| [`RELATIONSHIPS.md`](RELATIONSHIPS.md) | 20 relaciones: tipo, información, dependencia, RF/CU y observación. Incluye el flujo de información y el de RF-29 aparte |
| [`VALIDATION.md`](VALIDATION.md) | Matriz de validación (A–H), validación de componentes y de relaciones |
| [`F28_VALIDATION.md`](F28_VALIDATION.md) | Exigencias de la Guía 11 frente a la evidencia |
| [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) | Especificación de la vista ARQ-01 para la F29 |
| [`diagramas/draft/`](diagramas/draft/) | Borrador del diagrama conceptual (PNG) |
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

- **Formato:** es una adaptación académica; no existe Formato 11 oficial.
- **Punto de partida:** el AS-IS (F2 a F4) es preliminar.
- **RNF no verificados:** RNF-06 (rendimiento) y RNF-07 (disponibilidad y recuperabilidad).
- **H-14:** la cabecera del PDF del F4 queda como LOW para la F31.
- **Cabecera del PDF del F11 (LOW, mismo caso que H-14):** la extracción de texto de Word no devuelve «F11 ADAPTADO | …». El texto del cuerpo, incluido «Formato 11», sí se extrae, y el DOCX contiene la cabecera. Se revisa junto con H-14 en la F31.
- **RF-28:** no implementado.
- **RF-29:** experimental.
- **Aprobación:** no hay aprobación institucional.
- **Diagrama:** es un borrador; la vista formal ARQ-01 se hará en la F29.

## Relación con la F29

La vista ARQ-01 está especificada en [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) y figura en la [lista de trabajo de PowerDesigner](../POWERDESIGNER_WORKLIST.md) como READY FOR POWERDESIGNER, condicionada a la auditoría de la F28. PowerDesigner no se abrió en esta fase.
