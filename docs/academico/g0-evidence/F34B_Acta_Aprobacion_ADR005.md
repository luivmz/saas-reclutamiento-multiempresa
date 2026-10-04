# F34B — Acta de aprobación de ADR-005 (G0-14)

> Fase F34B, versión 1 (04/10/2026). Acta para que el equipo registre su decisión sobre [ADR-005](../diseno-inteligente/F33_ADR_005_G0.md), con el [paquete de aprobación de F34A](../g0-readiness/F34A_Paquete_Aprobacion_ADR005.md) como base. **Estado: PENDIENTE.** **ADR-005 = PROPUESTA.** No hay firmas ni evidencia adjunta.

## 1. Qué se decide

Si el equipo aprueba la **alternativa B** de ADR-005 (reglas, rúbricas y procedencia; nivel asignado siempre por una persona; decisión final humana), con E mantenida, C como futura, D rechazada y A como estado por defecto. Aprobar ADR-005 cierra **solo G0-14**; no aprueba G0.

## 2. Valores admitidos

- **Decisión:** `PENDIENTE`, `APRUEBA`, `APRUEBA CON OBSERVACIONES`, `RECHAZA`.
- **Estado:** `PENDIENTE` (sin evidencia) o `REGISTRADO` (con evidencia adjunta en [`adjuntos/`](adjuntos/README.md)).
- **Rol:** `Integrante del equipo` (exactamente tres filas) o `Docente del curso (consultivo, opcional)` (como máximo una).
- **Identidad:** cada fila de integrante corresponde a una persona distinta de la lista de integrantes del proyecto (`CLAUDE.md`), y cada integrante aparece **exactamente una vez**. La fila del docente es de otra persona y **no sustituye** a ningún integrante.

## 3. Registro

| Responsable | Rol | Fecha | Decisión | Evidencia adjunta/referencia | Observaciones | Estado |
|---|---|---|---|---|---|---|
| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |
| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |
| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |
| — | Docente del curso (consultivo, opcional) | — | PENDIENTE | — | — | PENDIENTE |

## 4. Regla de resultado

- **ADR-005 APROBADA:** las tres filas de integrantes en `APRUEBA` o `APRUEBA CON OBSERVACIONES`, cada una con fecha, estado `REGISTRADO` y un adjunto existente. La fila del docente es consultiva y no cuenta para el quórum.
- **ADR-005 RECHAZADA:** cualquier integrante en `RECHAZA` con evidencia; el proyecto vuelve a la alternativa A.
- **En cualquier otro caso:** ADR-005 sigue PROPUESTA y G0-14 sigue PENDIENTE EXTERNO.
- Una aprobación registrada aquí se publica después en un commit de gobierno propio; esta acta no modifica el texto del ADR.
