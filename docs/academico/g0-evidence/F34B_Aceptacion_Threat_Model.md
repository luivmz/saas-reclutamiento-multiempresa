# F34B — Aceptación del modelo de amenazas (G0-09)

> Fase F34B, versión 1 (04/10/2026); **actualizada en F34C** con evidencia real y corregida tras la auditoría F34C. Registro para que el equipo revise y acepte el [modelo de amenazas de F34A](../g0-readiness/F34A_Modelo_de_Amenazas.md) (STRIDE, 25 amenazas). **Estado: REGISTRADA (F34C).** Los tres integrantes registraron `ACEPTA` con evidencia adjunta y verificada. La aceptación es del **equipo**: no sustituye las pruebas de cada mitigación en F35/F38.

## 1. Qué se revisa

- Que los activos, actores y fronteras de confianza describen el módulo del alcance B.
- Que las 25 amenazas, incluidas la fuga cross-tenant (T-10), la exfiltración (T-11), los logs con PII (T-13) y el XSS persistente (T-25), tienen mitigación y riesgo residual razonables.
- Que los riesgos residuales medios (T-01, T-10, T-11 y T-14) se aceptan como condición para F35/F38, con pruebas obligatorias.

## 2. Registro

Valores de **Decisión:** `PENDIENTE`, `ACEPTA`, `ACEPTA CON OBSERVACIONES`, `RECHAZA`. **Estado:** `PENDIENTE` o `REGISTRADO`. **Rol:** `Integrante del equipo`, exactamente tres filas. **Identidad:** tres personas distintas de la lista de integrantes del proyecto (`CLAUDE.md`), cada una exactamente una vez.

| Responsable | Rol | Fecha | Decisión | Evidencia adjunta/referencia | Observaciones | Estado |
|---|---|---|---|---|---|---|
| Coronacion Meza Fredy | Integrante del equipo | 2026-10-04 | ACEPTA | [captura](adjuntos/G0-ADR005-ThreatModel_Fredy_Coronacion_2026-10-04.png) | Integrante: «Ninguna». Verificación: [acta §5](F34B_Acta_Aprobacion_ADR005.md#5-verificación-de-evidencias-f34c) | REGISTRADO |
| Peña Arroyo Anthony | Integrante del equipo | 2026-10-04 | ACEPTA | [captura](adjuntos/G0-ADR005-ThreatModel_Anthony_Pena_2026-10-04.png) | Integrante: «Ninguna». Verificación: [acta §5](F34B_Acta_Aprobacion_ADR005.md#5-verificación-de-evidencias-f34c) | REGISTRADO |
| Vila Meza Luis Antonio | Integrante del equipo | 2026-10-04 | ACEPTA | [original](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04_original.png) · [confirmación](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png) | Integrante: «Ninguna». Verificación: [acta §5](F34B_Acta_Aprobacion_ADR005.md#5-verificación-de-evidencias-f34c) | REGISTRADO |

## 3. Regla de resultado

- G0-09 pasa a CUMPLIDO si las tres filas están `REGISTRADO` con `ACEPTA` o `ACEPTA CON OBSERVACIONES` y adjunto existente. Las observaciones se convierten en tareas de F35/F38, no en cambios del modelo de F34A.
- Con `RECHAZA`, G0-09 queda RECHAZADO hasta un modelo de amenazas revisado en una fase nueva.
- En cualquier otro caso, G0-09 sigue PARCIAL (modelo elaborado, aceptación pendiente).

**Resultado F34C:** G0-09 = CUMPLIDO. Las pruebas de las mitigaciones, con prioridad para T-10, T-11, T-14, T-17 y T-25, siguen siendo obligatorias si alguna vez se habilita F35/F38.
