# F34B — Aceptación del modelo de amenazas (G0-09)

> Fase F34B, versión 1 (04/10/2026). Registro para que el equipo revise y acepte el [modelo de amenazas de F34A](../g0-readiness/F34A_Modelo_de_Amenazas.md) (STRIDE, 25 amenazas). **Estado: PENDIENTE.** El modelo existe; falta su aceptación registrada.

## 1. Qué se revisa

- Que los activos, actores y fronteras de confianza describen el módulo del alcance B.
- Que las 25 amenazas, incluidas la fuga cross-tenant (T-10), la exfiltración (T-11), los logs con PII (T-13) y el XSS persistente (T-25), tienen mitigación y riesgo residual razonables.
- Que los riesgos residuales medios (T-01, T-10, T-11 y T-14) se aceptan como condición para F35/F38, con pruebas obligatorias.

## 2. Registro

Valores de **Decisión:** `PENDIENTE`, `ACEPTA`, `ACEPTA CON OBSERVACIONES`, `RECHAZA`. **Estado:** `PENDIENTE` o `REGISTRADO`. **Rol:** `Integrante del equipo`, exactamente tres filas. **Identidad:** tres personas distintas de la lista de integrantes del proyecto (`CLAUDE.md`), cada una exactamente una vez.

| Responsable | Rol | Fecha | Decisión | Evidencia adjunta/referencia | Observaciones | Estado |
|---|---|---|---|---|---|---|
| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |
| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |
| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |

## 3. Regla de resultado

- G0-09 pasa a CUMPLIDO si las tres filas están `REGISTRADO` con `ACEPTA` o `ACEPTA CON OBSERVACIONES` y adjunto existente. Las observaciones se convierten en tareas de F35/F38, no en cambios del modelo de F34A.
- Con `RECHAZA`, G0-09 queda RECHAZADO hasta un modelo de amenazas revisado en una fase nueva.
- En cualquier otro caso, G0-09 sigue PARCIAL (modelo elaborado, aceptación pendiente).
