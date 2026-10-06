# F34E — Relación entre la G0 real y G0-SBX

> Fase F34E, versión 1 (04/10/2026). Son dos puertas **separadas**. G0-SBX no cambia ningún estado de la G0 real.

| Aspecto | G0 real | G0-SBX |
|---|---|---|
| Fuente | [ADR-005 §9](../diseno-inteligente/F33_ADR_005_G0.md#9-puerta-g0) | [Definición F34E](F34E_Definicion_G0_SBX.md) |
| Estado | **G0 real = NO APROBADA** | Ver la [decisión G0-SBX](F34E_Decision_G0_SBX.md) |
| Datos | Ninguno autorizado; los reales exigen además una aprobación específica posterior | Solo sintéticos |
| Habilita | Con APROBADA CON RESTRICCIONES, F35–F40 productivas del alcance B | Como máximo, F35-SBX |
| Evidencia externa | Obligatoria (jurídica, privacidad, institución) | No la exige ni la sustituye |
| ADR-005 | Requiere su aprobación (G0-14) | Requiere la aprobación interna del equipo registrada (SBX-13) |

## Pendientes reales de la G0 real

| Criterio | Estado | Qué falta |
|---|---|---|
| G0-02 | PENDIENTE EXTERNO | Revisión jurídica firmada y evaluación de impacto COMPLETADA o conclusión de NO APLICABILIDAD |
| G0-03 | PENDIENTE EXTERNO | Análisis de privacidad aprobado por el responsable del tratamiento |
| G0-12 | PENDIENTE EXTERNO | Respuesta archivada y vinculación inequívoca con el docente o un representante institucional (F34D: respuesta en texto sin adjunto e identidad no verificable) |

G0-SBX **no resuelve** ninguno de estos pendientes. Sin ellos, la G0 real sigue NO APROBADA y F35–F40 productivas siguen BLOQUEADAS.

## Reglas de redacción

- Se escribe siempre «G0 real» o «G0-SBX», nunca «G0» a secas cuando se habla de un estado.
- La única aprobación que puede aparecer en este paquete es «G0-SBX APROBADA CON RESTRICCIONES».
- `validate_f34e.py` falla si encuentra una aprobación de G0 sin el sufijo SBX.
