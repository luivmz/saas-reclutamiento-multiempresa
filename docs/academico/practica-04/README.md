# Práctica 04 — Formato 04: Identificación de problemas del proceso

Entregable de la Práctica 04 (Fase 27B): problemas del proceso actual (AS-IS preliminar), con su clasificación, sus causas y su ubicación en el BPMN.

**Estado: AS-IS PRELIMINAR.** Los problemas P1 a P5 vienen del análisis previo del equipo. La prioridad es una **priorización analítica del equipo** y las causas son hipótesis. Nada de esto está validado por la institución.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F4_Problemas_del_Proceso_Colegio_Andino.docx`](F4_Problemas_del_Proceso_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 04 |
| [`F4_Problemas_del_Proceso_Colegio_Andino.pdf`](F4_Problemas_del_Proceso_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F4_Problemas_del_Proceso_Colegio_Andino.md`](F4_Problemas_del_Proceso_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`matriz-problemas.md`](matriz-problemas.md) | Matriz consolidada de 11 columnas: actividad, problema, tipo, descripción, impacto, prioridad, causa, descripción de la causa, ubicación y estado de la evidencia |
| [`diagramas/draft/`](diagramas/draft/) | BPMN AS-IS anotado con P1 a P5 sobre cada actividad afectada (borrador) |
| [`evidencias/`](evidencias/README.md) | Evidencias del repositorio con su ruta y su SHA-256 |

## Problemas

| ID | Problema | Actividades AS-IS | Tipo principal | Prioridad (analítica) |
|---|---|---|---|---|
| P1 | Información distribuida | AS-02, AS-05, AS-06, AS-08 | Calidad (sec.: redundancia) | Alta |
| P2 | Seguimiento manual | AS-02, AS-03, AS-04, AS-09 | Control (sec.: tiempo) | Alta |
| P3 | Evaluaciones heterogéneas | AS-11, AS-12 | Calidad (sec.: control) | Alta |
| P4 | Comunicación manual | AS-07, AS-10, AS-14 | Tiempo (sec.: control) | Media |
| P5 | Indicadores limitados | AS-12, AS-13 | Control (sec.: información de gestión) | Media |

Cada problema se asigna a las mismas actividades que ya lo tenían en [`03-procesos-negocio.md`](../../final-report/03-procesos-negocio.md) §3.1. Las observaciones O-01 a O-05 del Formato 02 remiten a las mismas actividades.

## Precauciones

- **Tiempos, costos y frecuencias:** no se inventan. No hay mediciones del AS-IS, así que el impacto se describe sin cuantificarlo.
- **Redundancia:** no se identificaron actividades duplicadas verificadas; P1 la tiene solo como riesgo secundario.
- **P5:** el TO-BE lo atiende **solo en parte**, con la comparación explicable y la auditoría. Los indicadores de gestión corresponden a **RF-28, un candidato no implementado**, y no se presentan como resueltos.
