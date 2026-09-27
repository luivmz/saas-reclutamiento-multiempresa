# Práctica 05 — Formato 05: Modelo BPM mejorado (TO-BE)

Entregable de la Práctica 05 (Fase 27B): proceso mejorado de reclutamiento, evaluación y selección.

**Estado: TO-BE PROPUESTO**, soportado por el **software implementado** v1.1. Su adopción en el Colegio no está validada. La única actividad no implementada es **TB-F1**, marcada como propuesta futura.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F5_Modelo_BPM_TOBE_Colegio_Andino.docx`](F5_Modelo_BPM_TOBE_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 05 |
| [`F5_Modelo_BPM_TOBE_Colegio_Andino.pdf`](F5_Modelo_BPM_TOBE_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F5_Modelo_BPM_TOBE_Colegio_Andino.md`](F5_Modelo_BPM_TOBE_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`diagramas/draft/`](diagramas/draft/) | **Borrador** BPMN TO-BE en tres partes: requerimiento y convocatoria; postulación y evaluación; selección y cierre |
| [`POWERDESIGNER_PENDING.md`](POWERDESIGNER_PENDING.md) | Especificación para modelarlo formalmente en PowerDesigner (Fase 29) |
| [`evidencias/`](evidencias/README.md) | Evidencias, incluida una copia sin modificar del TO-BE original del equipo (anexo A del F9 v1.0) |

## TO-BE

- **30 actividades (TB-01 a TB-30)** en cinco subprocesos, que son los de [`03-procesos-negocio.md`](../../final-report/03-procesos-negocio.md) §3.3, más una transversal (TB-30, auditoría).
- **Propuesta futura:** TB-F1.
- **Carriles:**
  - pool de la organización con Área solicitante, RR. HH., Aprobador / Dirección, Evaluador y Plataforma SaaS (sistema);
  - pool externo del Postulante, comunicado por mensajes.

**Matriz problema → solución → actividad TO-BE → RF:**

| Problema | Solución | Actividades TO-BE | RF |
|---|---|---|---|
| P1 | S-01 Registro único por convocatoria | TB-01, TB-07, TB-08, TB-12, TB-13, TB-15 | RF-01, RF-05, RF-06, RF-09, RF-10, RF-12 |
| P2 | S-02 Estados e historial | TB-02 a TB-05, TB-16, TB-23, TB-27, TB-28 | RF-02, RF-03, RF-13, RF-14, RF-24, RF-25 |
| P3 | S-03 Criterios ponderados, validación y ranking explicable | TB-07, TB-09, TB-18 a TB-22, TB-24, TB-25 | RF-05, RF-16 a RF-22 |
| P4 | S-04 Notificaciones automáticas | TB-06, TB-14, TB-17, TB-19, TB-29 | RF-04, RF-11, RF-15, RF-17, RF-26 |
| P5 | S-05 Comparación y auditoría (**parcial**) | TB-24, TB-25, TB-26, TB-30 | RF-21, RF-22, RF-23, RF-27 |

Coincide con [`02-contexto-problema.md`](../../final-report/02-contexto-problema.md) §2.3. Los 27 RF de la línea base tienen al menos una actividad TO-BE (ver [F6](../practica-06/README.md)).

## Correcciones conceptuales

| ID | Corrección |
|---|---|
| C-01 | La **decisión final es humana** y la registra el **Aprobador / Dirección** (TB-26, RF-23). RR. HH. solo aplica la decisión (TB-27) y cierra (TB-28). |
| C-02 | **«Cerrar sin selección»:** el TO-BE original del equipo lo incluía, pero no está implementado (A-30). Queda como **propuesta futura** (TB-F1), fuera del flujo principal y dibujada en gris. |
| C-03 | **Ranking (TB-24):** calcula, ordena y compara; **no selecciona ni cambia estados**. |
| C-04 | **RF-29 (riesgo operacional, experimental):** no forma parte del TO-BE base. |
| C-05 | **Indicadores de gestión (P5):** no se dan por resueltos, porque RF-28 es un candidato no implementado. |

## ¿Requiere PowerDesigner?

**Sí, para la versión formal**, en la Fase 29 y después de la auditoría F27C. En esta fase no se abrió PowerDesigner. El diagrama de actividad AC-01 de la F23 describe el software implementado y **no** se reemplaza.
