# Fase 15A — Base Python y generador de dataset sintético

**Fecha:** 20 de septiembre de 2026
**Rama:** `feature/phase-15-ml-service`, creada desde `develop` en `d02cbc9`
**Writer principal:** Claude Code · **Reviewer:** Codex (modo lectura)
**Alcance:** solo 15A. No se entrenó ningún modelo, no existe FastAPI ni integración con Laravel.

---

## 1. Qué se implementó

| Entregable | Estado |
|---|---|
| Estructura del componente Python (`ml-service/`) | **Implementado** |
| Dependencias mínimas y fijadas | **Implementado** |
| Configuración reproducible (`SyntheticConfig`) | **Implementado** |
| Generador sintético *event-first* | **Implementado** |
| Validaciones del dataset (20 aprobadas) | **Implementado** |
| Suite de pruebas | **116 pruebas, 95 % de cobertura** |
| Documentación técnica | Este documento y `ml-service/README.md` |

## 2. Estructura

```
ml-service/
├── pyproject.toml
├── README.md
├── src/recruitment_ml/
│   ├── __init__.py
│   ├── config.py               SyntheticConfig, seed, versiones, perfil académico
│   ├── schema.py               contrato de columnas, prohibiciones, latentes
│   ├── data/__init__.py        reservado para 15B
│   └── synthetic/
│       ├── __init__.py         reexportación perezosa
│       ├── distributions.py    familias de distribución justificadas
│       ├── timeline.py         simulación event-first de un proceso
│       ├── generator.py        orquestación, manifiesto de linaje y CLI
│       └── validators.py       las 20 validaciones
├── tests/                      5 archivos, 116 pruebas
└── artifacts/.gitkeep          salida local, ignorada por Git
```

## 3. Entorno y dependencias

Python **3.12.5**, entorno virtual local en `ml-service/.venv` (no versionado). No se modificó el Python global ni el `PATH`.

| Paquete | Versión | Por qué |
|---|---|---|
| `numpy` | 2.1.3 | Generador aleatorio reproducible y distribuciones |
| `pandas` | 2.2.3 | Frame del dataset y tipos nullable |
| `pydantic` | 2.9.2 | Configuración inmutable y validada |
| `tzdata` | 2024.2 | Sin ella `zoneinfo` no resuelve `America/Lima` en Windows |
| `pytest` | 8.3.3 | Pruebas |
| `pytest-cov` | 5.0.0 | Cobertura |

**scikit-learn no se instaló**: 15A no lo necesita y añadirlo antes de tiempo sería una dependencia sin uso.

## 4. Configuración del generador

`SyntheticConfig` centraliza todo parámetro; no hay constantes mágicas dispersas. Valores por defecto, que son los aprobados en la Fase 14:

| Parámetro | Valor | Origen |
|---|---|---|
| `seed` | `20260920` | Decisión 4 |
| `rows` | 6 000 | Decisión 4 (rango 5 000–10 000) |
| `organizations` | 6 | Decisión 4 (rango 4–8) |
| `months` | 42 | Decisión 4 (mínimo 36) |
| `prevalence_min` / `max` | 0.25 / 0.40 | Decisión 4 |
| `stall_rate` | 0.06 | Tasa de censura configurable (decisión 10) |
| `drift_strength` | 0.30 | Drift temporal moderado |
| `delay_pressure` | 1.0 | Palanca estructural de calibración |
| `observation_tail_months` | 9 | Ventana de seguimiento |
| `null_opens_at_rate` | 0.12 | Ejercita la regla de respaldo de `application_window_days` |

**Desviación menor justificada:** `rows` admite 50–50 000 en el modelo, no 5 000–10 000, para que la suite de pruebas corra en segundos. El perfil académico aprobado se comprueba aparte con `validate_academic_profile()`, y tanto la CLI como el manifiesto **advierten** cuando la configuración se sale de él.

## 5. Generación *event-first*

El orden implementado, que es el aprobado:

1. Solicitud del requerimiento y configuración de la vacante.
2. **`target_completion_at` se fija aquí**, antes de la publicación, y es inmutable.
3. Publicación → ventana de postulaciones → cierre.
4. `checkpoint_at` = inicio del día siguiente al cierre, `America/Lima`.
5. Eventos operacionales hasta el checkpoint.
6. **Corte**: features derivadas solo del historial truncado.
7. Continuación estocástica: el tiempo restante depende del backlog observable, de los latentes y de ruido irreducible.
8. Cierre real y, solo entonces, `delayed = closed_at > target_completion_at`.

**La etiqueta nunca se calcula desde el vector de features.** Una prueba lo verifica directamente: añadir eventos posteriores al checkpoint no altera ninguna feature.

### Factores latentes

`operational_capacity`, `coordination_friction`, `workload_pressure`, `random_shock` y `period_effect`. Existen solo en memoria. Una prueba comprueba que **ninguno** aparece en el frame exportado.

`workload_pressure` se sortea como factor propio por (organización, mes) y **no** como recuento de filas de la celda. Fue una corrección deliberada: al derivarlo del recuento, su varianza dependía de `rows` y la prevalencia se movía entre 0.415 (1 500 filas) y 0.381 (6 000). Ahora la prevalencia es una propiedad de la simulación, no del tamaño de muestra.

Los perfiles de organización se normalizan a media geométrica 1. Con solo 4–8 organizaciones, la media muestral de un sorteo lognormal se desplaza según la seed y arrastraba la prevalencia global: el rango entre seeds era 0.21–0.36 y ahora es 0.30–0.36.

### Distribuciones

Lognormal y Gamma para duraciones positivas y asimétricas; binomial negativa para el volumen de postulaciones (sobredispersión); Poisson truncada para sesiones; efectos aleatorios de media cero por organización y periodo; shocks raros (p ≈ 0.035) con impacto grande. **No son estadísticas del Colegio Andino de Huancayo: son supuestos sintéticos académicos.**

## 6. Features implementadas

15 columnas model-ready: las 14 del núcleo más `days_remaining_to_target`.

`evaluations_pending_count` e `interviews_pending_count` se generan como **auxiliares** para validar la identidad `pending = scheduled − completed`, pero quedan fuera de X por colinealidad exacta. `configured_stage_count` queda como **ablation**.

**Ninguna variable prohibida está presente.** El guardián `is_forbidden_column` comprueba por nombre exacto y por fragmento. Durante la implementación detectó un hueco real: `evaluation_score` no era bloqueada porque `score` figuraba solo como nombre exacto. Se añadieron como fragmentos `score`, `puntaje`, `rank`, `outcome`, `closed`, `closure`, `justification` y `observation`.

## 7. Censura

Un proceso estancado nunca cierra, porque cerrar exige decisión y selección humanas. Esos procesos:

- se marcan `observation_status = "censored"`;
- tienen `delayed = NA`, **nunca** 0 ni 1;
- quedan fuera del conjunto supervisado;
- se contabilizan en el manifiesto y se distinguen los estancados de los que exceden la ventana observacional.

La tasa se configura con `stall_rate`, y una prueba verifica que subirla aumenta la proporción censurada.

## 8. Validación local del dataset de referencia

Configuración aprobada (6 000 filas, seed `20260920`, 6 organizaciones, 42 meses):

| Métrica | Valor medido |
|---|---|
| Filas generadas | 6 000 |
| Filas model-ready | 5 630 |
| Censurados | 370 (6.17 %) — 367 estancados, 3 por ventana |
| **Prevalencia** | **0.3362** (banda objetivo 0.25–0.40) |
| `config_fingerprint` | `4107a60ede323da2bc834128e449628f8c05a797ccf623cbfdfc3b93408b72df` |
| `dataset_fingerprint` | `6c67fa85e62d15e3f2b702909a5c12748ab3d41527d25593428544069be8e789` |
| Validación completa | `dataset valido`, sin issues ni warnings |

Robustez comprobada: prevalencia 0.32–0.38 entre tamaños de 300 a 10 000 filas, y 0.297–0.357 entre siete seeds distintas.

### Comprobaciones científicas

| Propiedad | Resultado |
|---|---|
| Determinismo (misma seed ⇒ mismo hash) | ✅ |
| Seed distinta ⇒ dataset distinto | ✅ |
| Correlación máxima feature–target | 0.41 (`days_remaining_to_target`), lejos del umbral de sospecha 0.92 |
| Solapamiento de clases | 98.8 % de las filas viven en perfiles donde ocurren ambos desenlaces |
| Drift temporal | prevalencia 0.278 → 0.347 → 0.384 entre tercios temporales |
| Regla operacional simple | precision 0.405, recall 0.390 frente a prevalencia 0.336 — hay señal, no determinismo |

**El dataset generado no se versionó.** Está en `ml-service/artifacts/`, ignorado por Git.

## 9. Pruebas

| Archivo | Cubre |
|---|---|
| `test_generator_reproducibility.py` | Determinismo, hashes, manifiesto, configuración inválida |
| `test_dataset_schema.py` | Contrato de columnas, prohibidas, latentes, tipos, unicidad |
| `test_dataset_temporal_integrity.py` | Orden cronológico, checkpoint, plazo inmutable, zona horaria |
| `test_dataset_no_leakage.py` | Eventos posteriores, correlaciones, solapamiento, censura |
| `test_dataset_distributions.py` | Prevalencia, invariantes de conteo, drift, multiempresa, CLI |

**116 pruebas, 95 % de cobertura.** Incluyen pruebas negativas que corrompen el dataset a propósito y exigen que cada validador se dispare: un guardián que nunca falla no está demostrado.

## 10. Qué NO se implementó

Pipeline de scikit-learn, Logistic Regression, Decision Tree, Random Forest, split train/validation/test, calibración, métricas, selección de modelo, `joblib`/`pickle`, FastAPI, `/health`, `/v1/predict`, Docker del ML, integración HTTP con Laravel, UI React y la implementación de RF-28/RF-29. Todo ello pertenece a 15B, 15C y 16.

**No se modificó** Laravel, React, Docker, CI, Composer ni NPM. El único archivo del proyecto tocado fuera de `ml-service/` y `docs/v1.1/` es `.gitignore`, con reglas acotadas a `ml-service/`.

## 11. Riesgos y observaciones

| # | Observación |
|---|---|
| 1 | **`GAP-01` sigue abierta.** `target_completion_at` no existe en Laravel; `days_remaining_to_target` no es computable en producción. El modelo no será desplegable aunque 15B tenga éxito |
| 2 | **`concurrent_open_vacancies_count` correlaciona 0.64 con el calendario** por la acumulación de procesos estancados. Es fiel al dominio (no existe cancelación, A-22) y produce drift intencionado, pero 15B debe vigilar que el modelo no aprenda solo el paso del tiempo |
| 3 | **Prevalencia calibrada estructuralmente** ajustando coeficientes del proceso. Es una decisión de simulación documentada, no una estadística institucional |
| 4 | Los censurados son casi todos estancados (367 de 370): la ventana de seguimiento de 9 meses es generosa. 15B debe reportar el sesgo de selección, no solo declararlo |
| 5 | Las pruebas usan 2 500 filas por velocidad; el entregable académico son 6 000 |

## 12. Handoff a 15B

Lo que 15B recibe listo: dataset reproducible por seed y hash, contrato de features aplicado y verificado, censura resuelta, manifiesto de linaje y suite de validaciones reutilizable.

Lo que 15B debe hacer: split temporal 70/15/15 por `checkpoint_at`, baseline trivial y baseline operacional, Logistic Regression como primer modelo, comparación con Decision Tree y Random Forest, Average Precision como métrica primaria, calibración, umbrales fijados solo en validation, y evaluación del impacto de la censura.

**15B requiere autorización explícita** antes de instalar scikit-learn y escribir el pipeline de entrenamiento.

## Enlaces

- [`ml-service/README.md`](../../ml-service/README.md)
- [Definición del problema](ml/problem-definition.md) · [Contrato de features](ml/feature-contract.md) · [Especificación del dataset](ml/dataset-specification.md) · [Plan de evaluación](ml/evaluation-plan.md)
- [ADR-004](architecture-decisions/ADR-004-ml-problem-definition.md) · [Índice de la Fase 14](phase-14-ml-definition.md)
