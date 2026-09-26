# Cierre Fase 15

**Fecha:** 2026-09-21. **Rama de trabajo:** `feature/phase-15-ml-service`. **Commit técnico aprobado:** `41a23cb84632bf8eaf8d66b290a863a35a1e26d3`.

15A (datos sintéticos), 15B (entrenamiento y evaluación), 15C (FastAPI experimental) y 15D (QA) están cerradas. La verificación de cierre ejecutó **506 pruebas**, sin fallos ni avisos, con **98 % de cobertura**.

- **Freeze:** `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`.
- **Modelo:** Logistic Regression (`C=10.0`, `class_weight=None`), `StandardScaler`, sin calibración; seed `20260920`; threshold exacto `0.1679418172266036`.
- **API experimental:** `GET /health`, `GET /v1/model-info`, `POST /v1/predict`.
- **Veredicto científico:** `PREDICTIVE GO WITH LIMITATIONS`. Se demostró metodología con datos sintéticos, **no** validez predictiva institucional. Persisten tasa de alerta alta, heterogeneidad entre organizaciones, censura informativa, colinealidad, posible proxy temporal y contaminación procedimental menor del test.
- **GAP-01 abierto:** Laravel no dispone de `target_completion_at`; por ello no puede calcular `days_remaining_to_target`. No hay integración productiva Laravel ni autorización de despliegue. La Fase 16 queda autorizada para comenzar en una rama nueva desde `develop`, sin dar por cerrado GAP-01.

**Observaciones no bloqueantes heredadas de 15D:** LOW: `test_reveal_count` no figura en `phase-15b-results-summary.json`. INFO: el documento 15B conserva el conteo histórico de pruebas de su cierre; `build_artifact.py` mantiene ramas defensivas sin cobertura; la auditoría 15D no fue completamente independiente; el ejemplo OpenAPI produce un score alto; `F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx` permanece ajeno y fuera de Git. Estas observaciones no cambian el freeze, el modelo ni las métricas.
