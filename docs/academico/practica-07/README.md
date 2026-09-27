# Práctica 07 — Formato 07: Requerimientos no funcionales

Entregable de la Práctica 07 (Fase 27B): los **10 RNF académicos** (RNF-01 a RNF-10, catálogo del F9) con su criterio, su método de verificación, su **estado real de validación** y su equivalencia con los 11 RNF técnicos del informe v1.0.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F7_Requerimientos_No_Funcionales_Colegio_Andino.docx`](F7_Requerimientos_No_Funcionales_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 07 |
| [`F7_Requerimientos_No_Funcionales_Colegio_Andino.pdf`](F7_Requerimientos_No_Funcionales_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F7_Requerimientos_No_Funcionales_Colegio_Andino.md`](F7_Requerimientos_No_Funcionales_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`evidencias/`](evidencias/README.md) | Evidencias del repositorio con su ruta y su SHA-256 |

## Estado de validación

| RNF | Nombre | Estado |
|---|---|---|
| RNF-01 | Seguridad y control de acceso | VERIFICADO |
| RNF-02 | Multitenencia y aislamiento | VERIFICADO |
| RNF-03 | Trazabilidad y auditoría | VERIFICADO |
| RNF-04 | Privacidad | VERIFICADO |
| RNF-05 | Usabilidad | EVIDENCIA PARCIAL: sin pruebas con usuarios reales ni con un lector de pantalla real |
| RNF-06 | Rendimiento | **NO VERIFICADO**: sin SLA, pruebas de carga ni umbral aprobado. La medición de la F25 es exploratoria |
| RNF-07 | Disponibilidad y recuperabilidad | **NO VERIFICADO**: sin pruebas de respaldo o restauración ni objetivos de disponibilidad |
| RNF-08 | Compatibilidad | EVIDENCIA PARCIAL: solo el motor Chromium (Electron), sin matriz formal de navegadores |
| RNF-09 | Mantenibilidad | EVIDENCIA PARCIAL: estructura y suites verificadas, sin métricas de mantenibilidad |
| RNF-10 | Integridad de datos | VERIFICADO |

Para RNF-06, RNF-07 y RNF-08 el formato da un **criterio propuesto**, no un umbral inventado.

## Equivalencia con el catálogo técnico

La relación **no es 1:1**:

- **RNF-01 y RNF-03** agrupan dos RNF técnicos cada uno.
- **RNF-06, RNF-07 y RNF-08** no tienen equivalente técnico.
- **Portabilidad y localización** (capítulo 4, RNF-09 y RNF-11) no tienen equivalente académico.

Unificar los catálogos es una decisión pendiente del equipo (F24 L-01). Los candidatos RNF-A, RNF-B y **RNF-C** siguen siendo **propuestas**. RNF-C está implementado en la portada (F20), pero no está promovido.
