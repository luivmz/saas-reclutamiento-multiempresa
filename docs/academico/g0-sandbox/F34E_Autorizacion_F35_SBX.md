# F34E — Autorización de F35-SBX

> Fase F34E, versión 1 (04/10/2026).

## 1. Estados

- **F35 productiva = BLOQUEADA.** Depende de la G0 real, que sigue NO APROBADA.
- **F35-SBX** queda HABILITADA **solo** si G0-SBX está APROBADA CON RESTRICCIONES. Su estado vigente está en la [decisión G0-SBX](F34E_Decision_G0_SBX.md).
- F36–F40 siguen BLOQUEADAS, tanto productivas como en modo sandbox, hasta una autorización explícita propia.

## 2. Condiciones de F35-SBX

1. Solo el [alcance autorizado](F34E_Alcance_Autorizado.md), siempre dentro de las [prohibiciones](F34E_Prohibiciones.md).
2. Todo artefacto de F35-SBX vive en un espacio marcado como sandbox (por ejemplo, `docs/academico/` o carpetas `sbx`), con fixtures `[SINTÉTICO]`.
3. Cada entrega de F35-SBX vuelve a ejecutar `validate_f34e.py`; si algún criterio SBX falla, G0-SBX pasa a REVOCADA y el trabajo se detiene.
4. F35-SBX no modifica RF-01 a RF-27, CU-01 a CU-20 ni los RF candidatos, y no promueve nada al baseline.

## 3. Criterios de salida: de SBX a trabajo real

Nada migra automáticamente de SBX a producción. Reutilizar un artefacto SBX en trabajo real exige **todo** lo siguiente:

| # | Condición |
|---|---|
| SAL-01 | G0 real APROBADA CON RESTRICCIONES, registrada por el equipo con su evidencia |
| SAL-02 | Revisión de privacidad completada (G0-03) |
| SAL-03 | Revisión jurídica completada, con la evaluación de impacto COMPLETADA o la conclusión de NO APLICABILIDAD (G0-02) |
| SAL-04 | Necesidad institucional verificada (G0-12) |
| SAL-05 | Revisión explícita, artefacto por artefacto, de qué piezas SBX pueden reutilizarse, con sus pruebas, cross-tenant y regresión completa |

Incluso con SAL-01 a SAL-05, los datos reales siguen prohibidos hasta una aprobación específica posterior (ADR-005 §6.10).
