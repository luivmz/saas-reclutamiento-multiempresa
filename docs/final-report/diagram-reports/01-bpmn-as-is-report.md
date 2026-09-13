# Informe del diagrama BPMN AS-IS

## 1. Propósito

El BPMN AS-IS debe representar cómo se realiza hoy el reclutamiento, la evaluación y la selección de personal en el caso de estudio (Colegio Andino de Huancayo), antes de la plataforma. Sirve de base para identificar los problemas P1 a P5 y justificar el proceso TO-BE.

**Disponibilidad:** el BPMN AS-IS forma parte de la documentación académica previa, pero **no se encuentra versionado en el repositorio actual**. Tampoco se encontró en la carpeta del curso revisada (`Diagramas/PD` solo contiene diagramas UML de PowerDesigner). Este informe no reconstruye ni sustituye ese diagrama.

## 2. Elementos principales

Sin el archivo original no pueden enumerarse con certeza sus carriles, actividades ni compuertas. La única descripción disponible del AS-IS en el repositorio es textual y preliminar ([capítulo 3, sección 3.1](../03-procesos-negocio.md#31-proceso-as-is-preliminar-pendiente-de-validación)). Enumera actividades a nivel macro:
- detectar la necesidad;
- revisar y aprobar;
- definir el perfil y difundir;
- recibir postulaciones;
- preseleccionar;
- coordinar evaluaciones y entrevistas;
- consolidar resultados;
- decidir y comunicar.

Participantes mencionados: Área solicitante, RR. HH., Dirección, evaluadores y postulantes.

No se agregan actividades nuevas.

## 3. Relación con requerimientos

El AS-IS no se implementa: justifica los requerimientos. Cada problema derivado del AS-IS se relaciona con los RF que lo atienden ([capítulo 2, sección 2.3](../02-contexto-problema.md#23-relación-problema--solución-implementada)):

| Problema | RF |
|---|---|
| P1 Información distribuida | RF-01, RF-05, RF-06, RF-09, RF-10, RF-12 |
| P2 Seguimiento manual | RF-02, RF-03, RF-13, RF-14, RF-24, RF-25 |
| P3 Evaluaciones heterogéneas | RF-05, RF-16 a RF-22 |
| P4 Comunicación manual | RF-04, RF-11, RF-15, RF-17, RF-26 |
| P5 Indicadores limitados | RF-21, RF-22, RF-23, RF-27 |

## 4. Relación con implementación

No aplica de forma directa. La implementación (RF-01 a RF-27) corresponde al TO-BE ([02-bpmn-to-be-report.md](02-bpmn-to-be-report.md)).

## 5. Consistencias

- Los cinco problemas usados en el informe (P1 a P5) son los definidos por el equipo en su análisis previo.
- La descripción textual del capítulo 3 no contradice esos problemas y los mantiene rotulados como preliminares.

## 6. Diferencias detectadas

No pueden evaluarse sin el diagrama original. Queda un riesgo: que la descripción textual resumida no refleje con exactitud los carriles o el nivel de detalle del BPMN del equipo.

## 7. Limitaciones

- Diagrama original no versionado ni localizado en la carpeta del curso.
- **El AS-IS es preliminar** y está pendiente de validación con RR. HH./Administración del colegio.
- No hay documentación institucional verificada (tiempos, canales, formatos, responsables reales). **No debe tratarse como hecho institucional final.**

## 8. Estado para entrega

**Evidencia externa pendiente**, con AS-IS preliminar.

## 9. Recomendación

1. Anexar el BPMN AS-IS original del equipo (imagen o exportación) al informe final y, si procede, versionarlo en `docs/`.
2. Validarlo con RR. HH./Administración, o conservar el rótulo «preliminar» en todas sus menciones.
3. Contrastar la descripción del capítulo 3 con el diagrama y ajustar el texto si hay diferencias.
