# Práctica 06 — Formato 06: Requerimientos funcionales

Entregable de la Práctica 06 (Fase 27B): los **27 requerimientos funcionales de la línea base** (RF-01 a RF-27), con sus fichas y su trazabilidad con el TO-BE.

**Estado: SOFTWARE IMPLEMENTADO.** Los 27 RF están implementados y trazados a código y pruebas en la v1.1 ([`traceability-master.md`](../../final-report/traceability-master.md); QA de la F25).

## Contenido

| Archivo | Qué es |
|---|---|
| [`F6_Requerimientos_Funcionales_Colegio_Andino.docx`](F6_Requerimientos_Funcionales_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 06 |
| [`F6_Requerimientos_Funcionales_Colegio_Andino.pdf`](F6_Requerimientos_Funcionales_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F6_Requerimientos_Funcionales_Colegio_Andino.md`](F6_Requerimientos_Funcionales_Colegio_Andino.md) | Espejo en Markdown del mismo contenido |
| [`evidencias/`](evidencias/README.md) | Evidencias del repositorio con su ruta y su SHA-256 |

## Qué contiene

- **Lista de los 27 RF** con nombre canónico, descripción («El sistema debe…»), actor, entradas, salidas y prioridad. La prioridad es una **priorización analítica del equipo**: Alta si el RF está en el camino principal del proceso; Media si es una notificación derivada.
- **27 fichas** con los campos de la plantilla:
  - descripción, actor principal y precondiciones;
  - flujo principal y flujos alternativos;
  - postcondiciones;
  - además, la actividad TO-BE y la evidencia de implementación (clases de prueba y specs E2E).

  Las entradas vienen de los Form Requests reales (`app/Http/Requests`) y las reglas, de [`assumptions.md`](../../assumptions.md).
- **Trazabilidad TO-BE → RF:** las 30 actividades TB-01 a TB-30 del [Formato 05](../practica-05/README.md). TB-F1 es una propuesta futura sin RF.
- **Extensiones posteriores al baseline**, en una sección **aparte**, fuera de la tabla principal:
  - **RF-28:** candidato descriptivo, no implementado;
  - **RF-29:** experimental, solo sobre el proceso, no productivo. No evalúa candidatos, no decide y no modifica el ranking.

## Nombres abreviados

Los IDs no cambian. El formato muestra el **nombre canónico** y, si existe, el **alias histórico**:

| Documento | Rótulos distintos del canónico |
|---|---|
| F9 (v1.0 y v1.1) | 13: 11 abreviaturas y 2 variantes (RF-19 y RF-23) |
| Informe v1.0, capítulo 4 | 8 |

La Fase 24 había registrado «seis rótulos abreviados» (observación L-02). La comparación completa de la F27B encuentra las 13 diferencias y las resuelve todas. El F9 publicado no se modifica.

## Reglas que el formato mantiene

- **RF-23:** la decisión final es humana y la registra el **Aprobador / Dirección**, con confirmación y justificación. RR. HH. no decide.
- **RF-21 y RF-22:** calculan, ordenan y comparan; **no seleccionan ni cambian estados**.
- **RF-25:** solo cierra **con selección**. El cierre sin selección está fuera de la línea base (A-30).
