# Fase 15A — Base Python y generador de dataset sintético

**Fecha:** 20 de septiembre de 2026
**Rama:** `feature/phase-15-ml-service`, creada desde `develop` en `d02cbc9`
**Writer principal:** Claude Code · **Reviewer:** Codex (modo lectura)
**Alcance:** solo 15A. No se entrenó ningún modelo, no existe FastAPI ni integración con Laravel.

> **Corrección posterior a la auditoría de Codex (20/09/2026).** Se resolvieron un hallazgo HIGH y cuatro MEDIUM. **Todas las cifras de este documento son las de la regeneración posterior a esas correcciones**; las del commit `d72bd82` quedaron obsoletas y no se conservan. Detalle en la sección 12.

---

## 1. Qué se implementó

| Entregable | Estado |
|---|---|
| Estructura del componente Python (`ml-service/`) | **Implementado** |
| Dependencias mínimas y fijadas | **Implementado** |
| Configuración reproducible (`SyntheticConfig`) | **Implementado** |
| Generador sintético *event-first* | **Implementado** |
| Validaciones del dataset (20 aprobadas) | **Implementado** |
| Manifiesto de linaje por exportación | **Implementado** |
| Suite de pruebas | **182 pruebas, 97 % de cobertura** |
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
├── tests/                      6 archivos, 182 pruebas
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

El orden implementado, que es el aprobado. Tras la auditoría, **el orden del código coincide con el conceptual**: todo lo que determina el plazo objetivo se sortea en `plan_process()`, en el momento de la solicitud.

1. Solicitud del requerimiento: `plan_process()` fija adelanto de publicación, desfase de apertura, ventana de postulaciones, holgura del plazo, plazas, criterios y etapas.
2. **`target_completion_at` se fija aquí**, antes de la publicación, y es inmutable.
3. Publicación → apertura de postulaciones → cierre.
4. `checkpoint_at` = inicio del día siguiente al cierre, `America/Lima`.
5. Eventos operacionales hasta el checkpoint, **incluido el historial inicial de cada postulación**.
6. **Corte**: features derivadas solo del historial truncado.
7. Continuación estocástica: el tiempo restante depende del backlog observable, de los latentes y de ruido irreducible.
8. Cierre real y, solo entonces, `delayed = closed_at > target_completion_at`.

**La etiqueta nunca se calcula desde el vector de features.** Una prueba lo verifica directamente: añadir eventos posteriores al checkpoint no altera ninguna feature.

### Historial de etapas

Se reproduce la semántica verificada en el dominio:

- `ApplicationService::apply()` crea **un** `ApplicationStageHistory` inicial (`null → postulado`) en el mismo instante que `applied_at` (`app/Services/Applications/ApplicationService.php:60-67`), y `tests/Feature/Applications/ApplyToVacancyTest.php:51` afirma que tras postular existe exactamente 1 fila;
- `ApplicationStageService::transition()` crea **uno** por cada cambio posterior (`app/Services/Applications/ApplicationStageService.php:71`).

El generador emite esos eventos explícitamente: historial inicial en `applied_at`, transición a preselección, transición a evaluación y transición a entrevista. **No se suma un contador**: `stage_transition_count` sigue siendo el recuento de eventos truncado en el checkpoint.

### Factores latentes

`operational_capacity`, `coordination_friction`, `workload_pressure`, `random_shock` y `period_effect`. Existen solo en memoria. Una prueba comprueba que **ninguno** aparece en el frame exportado.

`workload_pressure` se sortea como factor propio por (organización, mes) y **no** como recuento de filas de la celda. Fue una corrección deliberada: al derivarlo del recuento, su varianza dependía de `rows` y la prevalencia se movía entre 0.415 (1 500 filas) y 0.381 (6 000). Ahora la prevalencia es una propiedad de la simulación, no del tamaño de muestra.

Los perfiles de organización se normalizan a media geométrica 1. Con solo 4–8 organizaciones, la media muestral de un sorteo lognormal se desplaza según la seed y arrastraba la prevalencia global: el rango entre seeds era 0.21–0.36 y ahora es 0.30–0.36.

### Distribuciones

Lognormal y Gamma para duraciones positivas y asimétricas; binomial negativa para el volumen de postulaciones (sobredispersión); Poisson truncada para sesiones; efectos aleatorios de media cero por organización y periodo; shocks raros (p ≈ 0.035) con impacto grande. **No son estadísticas del Colegio Andino de Huancayo: son supuestos sintéticos académicos.**

## 6. Features implementadas

15 columnas model-ready: las 14 del núcleo más `days_remaining_to_target`.

`evaluations_pending_count` e `interviews_pending_count` se generan como **auxiliares** para validar la identidad `pending = scheduled − completed`, pero quedan fuera de X por colinealidad exacta.

`ABLATION_REQUIRED_IN_15B` declara en código las features cuya contribución 15B **debe** comparar entrenando con y sin ellas: `concurrent_open_vacancies_count`, `configured_stage_count` y `elapsed_days_since_publication`. La lista viaja también en el manifiesto.

**Ninguna variable prohibida está presente.** El guardián `is_forbidden_column` pasó de comparar **subcadenas** a comparar **tokens completos**, separando por guiones, guiones bajos, puntos y límites de camelCase, con plural simple. Bloquea `evaluation_score`, `final_result`, `total_duration_days`, `candidateEmail` o `candidate.email`; y deja pasar nombres operacionales legítimos como `filename`, `coverage_ratio` y `management_latency`, que una búsqueda de subcadenas bloquearía por contener «name» o «age».

## 7. Censura

Un proceso estancado nunca cierra, porque cerrar exige decisión y selección humanas. Esos procesos:

- se marcan `observation_status = "censored"`;
- tienen `delayed = NA`, **nunca** 0 ni 1;
- quedan fuera del conjunto supervisado;
- se contabilizan en el manifiesto y se distinguen los estancados de los que exceden la ventana observacional.

**La censura es informativa por diseño.** `stall_probability()` construye la probabilidad en escala logit alrededor de `stall_rate` y la hace depender de la fricción de coordinación, la presión de carga, la capacidad operativa, el shock y los días sin actividad. Queda acotada a `[0.005, 0.60]`: nunca es determinista y siempre hay solapamiento entre censurados y completados.

El manifiesto incorpora `censoring_mechanism` y `censoring_comparison`, con las diferencias de medias estandarizadas (SMD) entre ambos grupos. **Es una decisión de simulación académica, no una observación institucional**, y 15B debe usarla para evaluar el sesgo de selección.

La tasa base se configura con `stall_rate`, y una prueba verifica que subirla aumenta la proporción censurada.

## 8. Validación local del dataset de referencia

Configuración aprobada (6 000 filas, seed `20260920`, 6 organizaciones, 42 meses):

| Métrica | Valor medido |
|---|---|
| Filas generadas | 6 000 |
| Filas model-ready | 5 533 |
| Censurados | 467 (7.78 %) — 465 estancados, 2 por ventana |
| **Prevalencia** | **0.3266** (banda objetivo 0.25–0.40) |
| `config_fingerprint` | `4107a60ede323da2bc834128e449628f8c05a797ccf623cbfdfc3b93408b72df` |
| `dataset_fingerprint` (full) | `be7906347a0a6fb0b44b6be103b7f30ae64d4201983b592a70e0c17ba9ad76e1` |
| `model_ready_fingerprint` | `d94fe60d941be87580c71c3a72155b59a0b3a38071ad619ecd986bf607f1b2ae` |
| Validación completa | `dataset valido`, sin issues ni warnings |

### Robustez multiseed (3 000 filas)

| Seed | Prevalencia | Censura |
|---|---|---|
| 20260920 | 0.3153 | 0.0687 |
| 1 | 0.3054 | 0.0810 |
| 7 | 0.2921 | 0.0790 |
| 42 | 0.3302 | 0.0753 |
| 123 | 0.3085 | 0.0783 |
| 999 | 0.3000 | 0.0823 |
| 2026 | 0.3066 | 0.0770 |

Las siete quedan dentro de la banda 0.25–0.40. **No se filtró ninguna seed ni se ajustó ningún parámetro para forzar el resultado.**

### Comprobaciones científicas

| Propiedad | Resultado |
|---|---|
| Determinismo (misma seed ⇒ mismo hash) | ✅ |
| Seed distinta ⇒ dataset distinto | ✅ |
| Correlación máxima feature–target | **0.3915** (`days_remaining_to_target`), lejos del umbral de sospecha 0.92 |
| Drift temporal por tercios | prevalencia **0.2829 → 0.3200 → 0.3769** |
| `stage_transition_count` | media 18.00, mediana 13, min 0, max 221; **0 filas** con menos historiales que postulaciones; ratio medio 1.633 por postulación |
| `elapsed` vs `application_window` | Pearson 0.9716, Spearman 0.9620; identidad exacta en **37.93 %** de las filas (era 100 %), 10 valores distintos de la diferencia |
| `concurrent_open_vacancies_count` vs tiempo | Pearson **0.6846**, Spearman **0.7082**; media anual 48.1 → 76.7 → 107.1 → 136.7 |
| `concurrent_open_vacancies_count` vs target | Pearson **0.1535** |
| `concurrent_open_vacancies_count` vs censura acumulada | Pearson **0.6854** |
| Censurados vs completados (mayor \|SMD\|) | **0.2298** en `days_since_last_operational_event`; siguen `interviews_scheduled_count` (−0.1677) y `concurrent_open_vacancies_count` (+0.1304) |

### Baseline descriptivo

Regla, con sus parámetros explícitos **k = 1** y **d = 10**:

```
alerta  ⟺  (evaluations_overdue_pending_count + interviews_overdue_pending_count) >= 1
           ó  days_since_last_operational_event >= 10
```

Resultado sobre el dataset de referencia: **precision 0.4172, recall 0.3597**, 1 558 alertas, frente a una prevalencia de 0.3266. Hay señal, pero muy lejos de una etiqueta determinista.

**Esta regla no es todavía el baseline operacional formal de 15B**: allí sus umbrales deberán estimarse solo con train y congelarse antes de validation y test.

**El dataset generado no se versionó.** Está en `ml-service/artifacts/`, ignorado por Git junto con sus manifiestos.

## 9. Pruebas

| Archivo | Pruebas | Cubre |
|---|---|---|
| `test_dataset_schema.py` | 93 | Contrato de columnas, guardián tokenizado, latentes, tipos, unicidad, validadores negativos |
| `test_generator_reproducibility.py` | 22 | Determinismo, huellas por modo, manifiesto persistido, configuración inválida |
| `test_dataset_distributions.py` | 21 | Prevalencia, invariantes de conteo, drift, multiempresa, CLI |
| `test_dataset_no_leakage.py` | 20 | Eventos posteriores, correlaciones, solapamiento, censura informativa |
| `test_dataset_temporal_integrity.py` | 15 | Orden cronológico, checkpoint, plazo inmutable, zona horaria, colinealidad |
| `test_stage_history_semantics.py` | 11 | Semántica del historial de etapas (HIGH-01) |

**182 pruebas, 97 % de cobertura**, 0 fallos y 0 warnings. Cobertura por módulo: `timeline.py` 100 %, `distributions.py` 100 %, `schema.py` 96 %, `generator.py` 96 %, `validators.py` 95 %, `config.py` 91 %.

Incluyen pruebas negativas que corrompen el dataset a propósito y exigen que cada validador se dispare: un guardián que nunca falla no está demostrado.

## 10. Qué NO se implementó

Pipeline de scikit-learn, Logistic Regression, Decision Tree, Random Forest, split train/validation/test, calibración, métricas, selección de modelo, `joblib`/`pickle`, FastAPI, `/health`, `/v1/predict`, Docker del ML, integración HTTP con Laravel, UI React y la implementación de RF-28/RF-29. Todo ello pertenece a 15B, 15C y 16.

**No se modificó** Laravel, React, Docker, CI, Composer ni NPM. El único archivo del proyecto tocado fuera de `ml-service/` y `docs/v1.1/` es `.gitignore`, con reglas acotadas a `ml-service/`.

## 11. Riesgos y observaciones

| # | Observación |
|---|---|
| 1 | **`GAP-01` sigue abierta.** `target_completion_at` no existe en Laravel; `days_remaining_to_target` no es computable en producción. El modelo no será desplegable aunque 15B tenga éxito |
| 2 | **`concurrent_open_vacancies_count` correlaciona 0.685 con el calendario y 0.685 con la censura acumulada**, por los procesos estancados que permanecen abiertos. Es fiel al dominio (no existe cancelación, A-22) y produce el drift buscado. Decisión: **KEEP + ABLATION obligatoria en 15B** |
| 3 | **`elapsed_days_since_publication` sigue casi colineal con `application_window_days`** (Pearson 0.972) pese a eliminarse la identidad exacta. Es estructural al checkpoint aprobado. Decisión: **KEEP + ABLATION obligatoria en 15B** |
| 4 | **Prevalencia calibrada estructuralmente** ajustando coeficientes del proceso. Es una decisión de simulación documentada, no una estadística institucional |
| 5 | **La censura es informativa por diseño**, no MCAR. Los censurados son casi todos estancados (465 de 467): la ventana de seguimiento de 9 meses es generosa. 15B debe **evaluar** el sesgo de selección con las SMD del manifiesto, no solo declararlo |
| 6 | Las pruebas usan 2 500 filas por velocidad; el entregable académico son 6 000 |

## 12. Correcciones de la auditoría de Codex

| Hallazgo | Corrección |
|---|---|
| **HIGH-01** · `stage_transition_count` no incluía el historial inicial | Se modela explícitamente el evento `null → postulado` que `ApplicationService::apply()` crea en `applied_at`, y las transiciones a preselección, evaluación y entrevista como eventos propios. Sigue siendo event-first: **no** se suma un contador. Resultado: **0 filas** con menos historiales que postulaciones (antes, gran proporción) |
| **MEDIUM-01** · La CLI anunciaba la huella del dataset completo al exportar `--model-ready` | La huella anunciada corresponde siempre al frame exportado. Se añaden `model_ready_fingerprint`, `dataset_mode`, `rows_exported` y un manifiesto persistido `<output>.manifest.json`. `generated_at` queda fuera de toda huella reproducible |
| **MEDIUM-02** · `elapsed = window + 1` en el 100 % de las filas | Se genera un desfase realista entre publicación y apertura de postulaciones (`opening_offset_days`). La identidad universal desaparece: ahora se cumple en el 37.93 %, y donde `opens_at` es nulo es definicional por la regla de respaldo del contrato. La correlación residual (0.972) es estructural y se marca para ablation |
| **MEDIUM-03** · Censura casi MCAR | `stall_probability()` construye la probabilidad en escala logit alrededor de `stall_rate`, dependiente de fricción, presión, capacidad, shock e inactividad, acotada a `[0.005, 0.60]`. El manifiesto incorpora `censoring_mechanism` y `censoring_comparison` con SMD |
| **MEDIUM-04** · Concurrencia y drift | Se mantiene **KEEP + ABLATION**; cifras recalculadas y documentadas; obligación declarada en código (`ABLATION_REQUIRED_IN_15B`) y en el manifiesto |
| **LOW** · Guardián por subcadenas | `is_forbidden_column` pasa a **tokenización** con separadores y camelCase, con plural simple. Bloquea `evaluation_score`, `final_result`, `candidateEmail`, `total_duration_days`; permite `filename`, `coverage_ratio`, `management_latency` |
| **LOW** · Ramas de validadores sin cubrir | Pruebas negativas nuevas: manifiesto no sintético, manifiesto incompleto, estado de observación inválido, NaN contractual, dtype de target, columna ausente, `positions_count` imposible, etapas fuera de rango |
| **LOW** · Baseline descriptivo sin parámetros | Documentado con `k = 1`, `d = 10` y su fórmula; cifras recalculadas (precision 0.4172, recall 0.3597) |
| **§13** · Orden event-first del target | El plazo se sortea ahora en `plan_process()`, en el momento de la solicitud, antes de publicar y antes de cualquier evento operacional. El orden del código coincide con el conceptual |

## 13. Handoff a 15B

Lo que 15B recibe listo: dataset reproducible por seed y hash, huellas separadas para el dataset completo y el model-ready, manifiesto de linaje persistido por exportación, contrato de features aplicado y verificado, semántica del historial de etapas fiel al dominio, censura informativa con sus SMD, y una suite de validaciones reutilizable.

Lo que 15B debe hacer: split temporal 70/15/15 por `checkpoint_at`, baseline trivial y baseline operacional, Logistic Regression como primer modelo, comparación con Decision Tree y Random Forest, Average Precision como métrica primaria, calibración y umbrales fijados solo en validation.

**Obligaciones explícitas que 15B no puede omitir:**

1. **Ablation de `ABLATION_REQUIRED_IN_15B`**: entrenar y comparar con y sin `concurrent_open_vacancies_count`, `configured_stage_count` y `elapsed_days_since_publication`. Sin esa comparación no puede afirmarse que el modelo aprende señal operacional y no el paso del calendario.
2. **Evaluar el impacto de la censura**, no solo declararlo: usar `censoring_comparison` del manifiesto y reportar el sesgo de selección en las conclusiones.
3. **Tratar la multicolinealidad** entre `elapsed_days_since_publication` y `application_window_days` (Pearson 0.972) con regularización o eliminando una de las dos, y justificar la elección.
4. **No convertir el baseline descriptivo de la sección 8 en baseline formal sin recalibrarlo**: sus umbrales `k` y `d` deben estimarse solo con train y congelarse antes de validation y test.

**15B requiere autorización explícita** antes de instalar scikit-learn y escribir el pipeline de entrenamiento.

## Enlaces

- [`ml-service/README.md`](../../ml-service/README.md)
- [Definición del problema](ml/problem-definition.md) · [Contrato de features](ml/feature-contract.md) · [Especificación del dataset](ml/dataset-specification.md) · [Plan de evaluación](ml/evaluation-plan.md)
- [ADR-004](architecture-decisions/ADR-004-ml-problem-definition.md) · [Índice de la Fase 14](phase-14-ml-definition.md)
