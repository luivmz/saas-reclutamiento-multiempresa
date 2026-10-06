# F34E — Decisión G0-SBX

> Fase F34E, versión 1 (04/10/2026), preparada sobre F34D cerrada el 05/10/2026. Aplica la regla de la [definición](F34E_Definicion_G0_SBX.md#4-regla-de-decisión) a la [matriz de criterios](F34E_Matriz_Criterios_G0_SBX.md), verificada por [`validate_f34e.py`](../tools/f34e/validate_f34e.py). Pendiente de auditoría y de registro en commit de gobierno; ningún validador decide por sí solo.

## 1. Resultado

- **G0-SBX = APROBADA CON RESTRICCIONES.** Se cumplen los 18 criterios SBX, todos verificados dentro del repositorio.
- **F35-SBX = HABILITADA**, solo en modo sandbox sintético, dentro del [alcance autorizado](F34E_Alcance_Autorizado.md) y de las [prohibiciones](F34E_Prohibiciones.md).
- **F35 productiva = BLOQUEADA.**
- **F36–F40 = BLOQUEADAS.**
- **G0 real = NO APROBADA.** Pendientes externos: G0-02 (jurídico), G0-03 (privacidad) y G0-12 (necesidad institucional).
- **ADR-005 = PROPUESTA** (estado canónico), con aprobación interna del equipo registrada.
- **Alcance C = BLOQUEADO.**
- **Los datos reales siguen PROHIBIDOS.**
- RF-23 sigue humana, RF-21 no se reemplaza y RF-29 sigue experimental e informativa.
- F34E = LISTA PARA AUDITORÍA.

## 2. Criterios

| Estado | Criterios | Total |
|---|---|---|
| CUMPLE | SBX-01 a SBX-18 | 18 |
| NO CUMPLE | — | 0 |

## 3. Restricciones de la aprobación

- Solo datos 100 % sintéticos; ningún dato, documento, audio ni vídeo real.
- Sin scoring, recomendación, ranking nuevo ni decisión automática sobre personas.
- Aislado del runtime productivo: sin endpoints, migraciones ni dependencias.
- Ningún resultado SBX alimenta producción; la reutilización exige los criterios SAL-01 a SAL-05 de la [autorización de F35-SBX](F34E_Autorizacion_F35_SBX.md#3-criterios-de-salida-de-sbx-a-trabajo-real).

## 4. Revocación

G0-SBX pasa a REVOCADA, y F35-SBX a BLOQUEADA, si `validate_f34e.py` detecta que un criterio SBX deja de cumplirse, si se infringe una prohibición o si el equipo lo decide. La revocación se registra en un documento nuevo; esta decisión no se reescribe.
