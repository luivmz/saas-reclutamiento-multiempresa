# Preparación de F36 · B-01

> **PREPARACIÓN — B-01 NO ESTÁ IMPLEMENTADO.** Rama local `feature/continuacion-f36-f40`, 09/11/2026. F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA. Esta carpeta no modifica `validate_f36sbx.py`, no registra evidencia y no decide T-01 a T-09: la implementación exige D-10 determinada y D-02b emitida ([S, §2 y §11](../f36-sbx/expediente-final/F36SBX_B01_Especificacion_S.md)).

| Pieza | Archivo | Estado |
|---|---|---|
| Especificación S, versión 2.1 | [`F36SBX_B01_Especificacion_S.md`](../f36-sbx/expediente-final/F36SBX_B01_Especificacion_S.md) | CANDIDATA A AUDITORÍA |
| Sondas V-1 a V-7, S-T04 y S-T11 a S-T17, en un clon temporal | [`sondas_t09.py`](sondas_t09.py) | Ejecutadas el 09/11/2026: 18 conformes, 0 discrepancias |

```
python -I -B docs/academico/preparacion-f36-b01/sondas_t09.py
python -I -B docs/academico/preparacion-f36-b01/sondas_t09.py --solo S-T11
```

El script sale con código 1 si alguna sonda no da lo esperado. Clona el repositorio en un directorio temporal, prueba allí y borra el clon; el resultado se interpreta en [S, §5.9.4](../f36-sbx/expediente-final/F36SBX_B01_Especificacion_S.md#594-sondas-ejecutables-09112026).
