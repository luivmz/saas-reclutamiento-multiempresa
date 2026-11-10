# Preparación de F37 · Evidencias

> **PREPARACIÓN — NO IMPLEMENTADA EN EL SAAS.** Rama local `feature/continuacion-f36-f40`, 08/11/2026. F37-SBX = BLOQUEADA; F36-SBX-GATE = NO SUPERADO. Sin cambios en `app/`, `database/`, `resources/` ni `routes/`.

| Pieza | Archivo | Estado |
|---|---|---|
| Especificación del flujo mínimo, permisos, aislamiento y huecos de integración | [`F37_Flujo_Minimo_Evidencias.md`](F37_Flujo_Minimo_Evidencias.md) | PREPARADA |
| Ejemplos ficticios: 2 organizaciones, 5 roles, 38 escenarios | [`ejemplos/f37_ejemplos_ficticios.json`](ejemplos/f37_ejemplos_ficticios.json) | PREPARADOS |
| Prototipo separado, en memoria, solo biblioteca estándar | [`prototipo/f37_flujo_evidencias.py`](prototipo/f37_flujo_evidencias.py) | PROTOTIPO, sin ninguna EI |
| Pruebas del prototipo (23) | [`prototipo/test_f37_flujo_evidencias.py`](prototipo/test_f37_flujo_evidencias.py) | Ejecutadas: 23/23 |

```
python -I -B docs/academico/preparacion-f37-evidencias/prototipo/f37_flujo_evidencias.py
python -I -B -m unittest discover -s docs/academico/preparacion-f37-evidencias/prototipo -v
```

Lo pendiente y su requisito exacto están en la [especificación, §8](F37_Flujo_Minimo_Evidencias.md#8-qué-existe-y-qué-falta-para-integrarlo).
