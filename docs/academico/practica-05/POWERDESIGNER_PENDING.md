# Pendiente de PowerDesigner — F5 BPMN TO-BE

**Estado: REQUIERE POWERDESIGNER.** Se modela en la **Fase 29**, después de que la auditoría **F27C** apruebe el TO-BE. En la F27B no se abrió PowerDesigner ni se modificó ningún `.oom` o `.pdm`, ni ninguna exportación de la F23.

## Qué debe modelarse

El **BPMN del proceso TO-BE propuesto**, de la guía de la Práctica 05 y del Formato 05. Es un modelo de negocio, **distinto** de AC-01 (diagrama de actividad UML del software implementado, F23), que se conserva sin cambios.

Nombre sugerido: «F5 BPMN TO-BE propuesto — Reclutamiento y selección».

## Pools y lanes

| Pool | Lanes |
|---|---|
| Organización cliente (Colegio) con la plataforma — TO-BE propuesto | Área solicitante · RR. HH. · Aprobador / Dirección · Evaluador · Plataforma SaaS (sistema) |
| Postulante | Externo, comunicado por flujos de mensaje |

## Eventos

| ID | Tipo | Lane | Nombre |
|---|---|---|---|
| EI | Inicio | Área solicitante | Necesidad de personal identificada |
| EFA | Fin | Plataforma | Requerimiento rechazado |
| EFD | Fin | RR. HH. | Postulación descartada |
| EFE | Fin | Plataforma | Convocatoria cerrada con selección |
| SP, MP1 a MP4 | Mensaje (pool del Postulante) | Postulante | Vacante publicada, confirmación, aviso de etapa, convocatoria y resultado recibidos |
| A, B | Enlace | RR. HH. | Solo si el diagrama se divide en páginas |

## Tareas

TB-01 a TB-30, con el lane indicado en la tabla «Descripción de actividades» del Formato 05. Las tareas del sistema van en el lane de la plataforma: TB-06, TB-09, TB-14, TB-17, TB-19, TB-22, TB-24, TB-25, TB-29 y TB-30.

- **TB-26** lleva la anotación **«decisión humana (RF-23)»**.
- **TB-30** es transversal. Se recomienda modelarla como almacén de datos «Auditoría» con asociaciones desde las tareas críticas, o anotarla.

## Decisiones

| ID | Compuerta | Lane | Salidas |
|---|---|---|---|
| GA1 | ¿Requerimiento conforme? | RR. HH. | Observado → TB-04 → TB-02 · Validado → TB-05 |
| GA2 | ¿Aprobado? | Aprobador / Dirección | No → TB-06 → EFA · Sí → TB-07 |
| GB1 | ¿Configuración válida? | Plataforma | No → TB-08 · Sí → TB-10 |
| GD1 | ¿Preseleccionado? | RR. HH. | No → EFD · Sí → GD2 |
| GD2 | ¿Qué sesión se programa? | RR. HH. | Evaluación → TB-18 · Entrevista → TB-20 |
| GD3 | ¿Otra sesión? | RR. HH. | Sí → GD2 · No → TB-23 |

## Secuencia principal

TB-01 → TB-02 → TB-03 → GA1 → TB-05 → GA2 → TB-07 → TB-08 → TB-09 → GB1 → TB-10 → (el Postulante TB-11 → TB-12 → TB-13, por mensaje) → TB-14 → TB-15 → TB-16 → TB-17 → GD1 → GD2 → TB-18 o TB-20 → TB-19 → TB-21 → TB-22 → GD3 → TB-23 → TB-24 → TB-25 → TB-26 → TB-27 → TB-28 → TB-29 → EFE.

## Propuesta futura

**TB-F1 «Cerrar sin selección»** va con estilo diferenciado (gris o discontinuo) y la anotación «propuesta futura, no implementada (A-30)». No se conecta al flujo principal como si fuera un camino vigente.

## Criterio de aceptación

1. **Elementos:** los IDs TB-01 a TB-30 y TB-F1, las compuertas y los eventos coinciden uno a uno con el Formato 05 aprobado en la F27C.
2. **Decisión final:** está en el lane del **Aprobador / Dirección**. Ninguna tarea del sistema decide, selecciona ni descarta.
3. **RF-29:** no aparece en el TO-BE base.
4. **Modelos existentes:** AC-01 y demás diagramas de la F23 se conservan sin cambios.
5. **Exportación:** PNG y SVG, y el Formato 05 se actualiza solo después de una nueva auditoría.
