# Sondas de la especificación S (B-01)

> **PREPARACIÓN — B-01 NO ESTÁ IMPLEMENTADO.** Rama local `feature/continuacion-f36-f40`, 09/11/2026. F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA. Estas sondas no modifican `validate_f36sbx.py`, no registran evidencia, no mueven ninguna ref y no deciden T-01 a T-09. La implementación exige D-10 determinada y D-02b emitida ([S, §2 y §11](../F36SBX_B01_Especificacion_S.md)).

La carpeta está dentro del paquete, en el perímetro de AC-05, para que un H trasplantado según T-09 (a-ii) la lleve consigo ([S, §5.9.5](../F36SBX_B01_Especificacion_S.md)). Cada sonda clona el repositorio en un directorio temporal, prueba allí, borra el clon y sale con código 1 si algo no da lo esperado.

| Sonda | Archivo | Qué observa | Sección de S |
|---|---|---|---|
| T-09 | [`sondas_t09.py`](sondas_t09.py) | V-1 a V-7, S-T04, S-T11 a S-T15 y S-T17 con el validador v3, y S-T16 como evidencia de por qué (b) queda fuera de alcance | §5.9.1 y §5.9.4 |
| Revocación | [`sonda_revocacion.py`](sonda_revocacion.py) | Con commits sintéticos, que el delta de §5.8.2 se distingue de otro con una ruta o un campo adicional (S-T18 a S-T21). No es la validación funcional de AC-10 | §5.8.2 y §5.8.3 |
| Trasplante | [`sonda_trasplante.py`](sonda_trasplante.py) | Un H de prueba desde `55f758e` con el paquete trasplantado: inventario dentro de AC-05, enlaces, FRZ con la rama admitida en memoria y ejecución de las otras dos sondas desde ese árbol (S-T22) | §5.9.5 |

```
python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sondas_t09.py
python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sondas_t09.py --solo S-T11
python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sonda_revocacion.py
python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sonda_trasplante.py
python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sonda_trasplante.py --paquete ARBOL
```

`sonda_trasplante.py` trasplanta por defecto el paquete del commit HEAD; con `--paquete ARBOL`, el del árbol de trabajo. La rama `feature/f36-sbx-h-sonda` y los commits que crean las sondas son de prueba y desaparecen con el clon: la rama real de H es T-04, NO EMITIDA.
