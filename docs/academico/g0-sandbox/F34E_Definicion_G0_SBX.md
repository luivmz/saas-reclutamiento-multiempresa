# F34E — Definición de G0-SBX (puerta de experimentación académica sintética)

> Fase F34E, versión 1 (04/10/2026). Define una puerta **independiente** de la G0 real de [ADR-005 §9](../diseno-inteligente/F33_ADR_005_G0.md#9-puerta-g0). G0-SBX no modifica, sustituye ni reinterpreta la G0 real, que sigue **NO APROBADA** ([decisión G0 vigente](../g0-evidence/F34B_Decision_G0.md)).

## 1. Propósito

Autorizar **trabajo experimental académico** del alcance B de ADR-005 exclusivamente con datos **100 % sintéticos**, sin personas reales y sin ningún impacto sobre candidatos reales, para que el curso pueda avanzar en fases sandbox mientras los pendientes externos de la G0 real siguen abiertos.

## 2. Qué no es G0-SBX

G0-SBX **no sustituye**:

- la G0 real;
- la revisión jurídica (G0-02);
- la revisión de privacidad (G0-03);
- la validación de la necesidad institucional (G0-12).

Tampoco aprueba ADR-005, cuyo estado canónico sigue siendo PROPUESTA, ni autoriza datos reales, despliegue productivo o el alcance C.

## 3. Estados

| Estado | Significado |
|---|---|
| **NO APROBADA** | Al menos un criterio SBX no se cumple o no se puede verificar dentro del repositorio. F35-SBX bloqueada |
| **APROBADA CON RESTRICCIONES** | Los 18 criterios SBX se cumplen y se verifican automáticamente. Habilita solo F35-SBX, dentro de las [prohibiciones](F34E_Prohibiciones.md) |
| **REVOCADA** | Una aprobación anterior queda sin efecto porque un criterio deja de cumplirse o por decisión del equipo. F35-SBX vuelve a estar bloqueada |

## 4. Regla de decisión

- G0-SBX solo puede estar APROBADA CON RESTRICCIONES si **todos** los criterios SBX-01 a SBX-18 están en CUMPLE ([matriz](F34E_Matriz_Criterios_G0_SBX.md)) y [`validate_f34e.py`](../tools/f34e/validate_f34e.py) los verifica.
- **No hay criterios pendientes.** Si un criterio no se puede verificar dentro del repositorio, cuenta como NO CUMPLE y G0-SBX queda NO APROBADA.
- La puerta se reevalúa en cada fase SBX. Si un criterio deja de cumplirse, G0-SBX pasa a REVOCADA y el trabajo SBX se detiene.
- Toda mención usa el sufijo: «G0-SBX APROBADA CON RESTRICCIONES». Nunca se escribe una aprobación de G0 sin el sufijo SBX.

## 5. Ámbito de los datos

«Datos experimentales» son el dataset sintético de F34 ([`datos-sinteticos/`](../datos-sinteticos/README.md)) y cualquier fixture, documento o registro que produzca una fase SBX. Las evidencias de gobierno del equipo ([`g0-evidence/adjuntos/`](../g0-evidence/adjuntos/README.md)) **no** son datos experimentales y nunca se usan como entrada de un experimento.
