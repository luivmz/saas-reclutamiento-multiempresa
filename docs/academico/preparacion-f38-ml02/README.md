# Preparación de F38 · ML-02

> **PREPARACIÓN — SIN MÉTODO, SIN ENTRENAMIENTO Y SIN PROCESAR EVIDENCIA.** Rama local `feature/continuacion-f36-f40`, 08/11/2026. F37-SBX y F38-SBX = BLOQUEADAS; EI-22 y EI-23 = BLOCKED. La decisión de selección sigue siendo de Dirección (RF-23).

| Pieza | Archivo | Estado |
|---|---|---|
| Conjunto, resultados esperados, métricas, protocolo y especificación de entrenamiento | [`F38_Conjunto_Evaluacion_ML02.md`](F38_Conjunto_Evaluacion_ML02.md) | PREPARADO |
| Conjunto sintético con `dev` y `test` sellado | [`conjunto/ml02_casos_sinteticos.json`](conjunto/ml02_casos_sinteticos.json) | PREPARADO |
| Salidas de referencia escritas a mano (perfecta y degradada) | [`conjunto/salidas_de_referencia/`](conjunto/salidas_de_referencia/) | PREPARADAS |
| Arnés de evaluación, sin método | [`evaluacion/f38_evaluar.py`](evaluacion/f38_evaluar.py) | IMPLEMENTADO fuera del SaaS |
| Pruebas del arnés (28) | [`evaluacion/test_f38_evaluar.py`](evaluacion/test_f38_evaluar.py) | Ejecutadas: 28/28 |

Prototipo navegable y plan previos: [`../f36-sbx/prototipo-ml02/`](../f36-sbx/prototipo-ml02/README.md).
