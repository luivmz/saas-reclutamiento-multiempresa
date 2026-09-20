# Fase 15B — Entrenamiento y evaluación científica

**Fecha:** 20 de septiembre de 2026
**Rama:** `feature/phase-15-ml-service` · **Base 15A:** `583a021`
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría científica posterior)
**Alcance:** solo 15B. No hay FastAPI, endpoints, Docker de ML ni integración con Laravel.

> **Científicamente aceptable no equivale a desplegable.** `GAP-01` sigue abierto: `target_completion_at` no existe en Laravel, RF-29 continúa siendo candidato y no se autoriza ninguna integración.

---

## 1. Dataset

Fuente única: el generador de 15A. **No se creó ningún dataset paralelo.**

| Campo | Valor |
|---|---|
| Filas generadas / model-ready | 6 000 / **5 533** |
| Censurados | 467 (7.78 %), excluidos del supervisado |
| Prevalencia global | 0.326586 |
| `config_fingerprint` | `4107a60ede323da2bc834128e449628f8c05a797ccf623cbfdfc3b93408b72df` |
| `model_ready_fingerprint` | `d94fe60d941be87580c71c3a72155b59a0b3a38071ad619ecd986bf607f1b2ae` |
| Semilla | `20260920` |

Sin oversampling, undersampling, SMOTE ni reetiquetado. `class_weight` se comparó como hiperparámetro (`None` frente a `balanced`) y se decidió con validation.

## 2. Partición temporal 70/15/15

Ordenada por `checkpoint_at`. **Los empates de timestamp se resuelven de forma determinista por `vacancy_id`**, de modo que un mismo instante puede aparecer a ambos lados de una frontera: el corte es por posición tras un orden determinista, **no por desigualdad estricta de tiempo fila a fila**, y el resultado no afirma lo contrario. No hay fuga demostrada por esta causa y el diseño no se modificó.

| Partición | n | Prevalencia | Orgs | Desde | Hasta |
|---|---|---|---|---|---|
| Train | 3 873 | 0.3036 | 6 | 2023-01-18 | 2025-08-07 |
| Validation | 830 | 0.3795 | 6 | 2025-08-07 | 2026-02-04 |
| Test | 830 | 0.3807 | 6 | 2026-02-04 | 2026-08-22 |

La prevalencia sube de train a validation/test: es el drift moderado que el generador introduce a propósito y que justifica el split temporal.

**Censura contextual por ventana** (sobre el dataset completo, antes de excluir): train 0.0740, validation 0.0872, test 0.0863. Comparables, con un ligero aumento hacia el final del periodo.

## 3. Conjunto de prueba sellado

`SealedTestSet` es una **garantía de protocolo de software**, no una barrera criptográfica ni una prueba histórica. Entrega sus filas solo cuando recibe un `ExperimentFreeze` que:

1. es del tipo del dominio — un objeto cualquiera con `is_frozen=True` **no** sirve;
2. declara la versión de contrato vigente;
3. **fue persistido y recargado desde disco** (`source_path` no nulo);
4. conserva su integridad: el contenido coincide con `freeze_fingerprint`;
5. corresponde a **este** dataset y a **esta** partición (`dataset_fingerprint` y `split_signature`);
6. está completo: features, modelo, umbral y regla presentes.

Cualquier fallo lanza `SealedTestSetError`.

**Validación del `source_path`.** Declarar una ruta no prueba nada: se exige que **exista**, que sea un **archivo regular**, que pueda **cargarse** y que el registro recargado tenga **la misma huella**. Un objeto construido en memoria con `source_path="archivo-que-no-existe.json"` no abre el test.

**Enlace a la configuración.** Además del dataset y la partición, el freeze debe corresponder al `config_fingerprint` del generador. Un protocolo internamente íntegro pero de otra configuración se rechaza.

**Contenido científico efectivo.** No basta con que la clave exista: `threshold_selection`, `calibration_decision`, `validation_metrics`, `validation_baselines`, `ablation_conclusions`, `verdict_rule` y `known_limitations` deben tener contenido; `validation_metrics` debe incluir la métrica primaria, y el umbral debe estar en el rango (0, 1).

**Lo que `describe()` ya no expone.** Antes de revelar, devuelve solo `n`, organizaciones y el periodo, con `labels_disclosed: false`. **No informa de la prevalencia ni del número de positivos**: documentar el tamaño de la partición es legítimo, conocer su distribución de clases antes de congelar el protocolo no lo es. Tras el reveal, sí los incluye.

Las filas viven en un atributo con *name mangling*, no en un campo público. **Esto reduce las rutas accidentales de acceso; no las hace imposibles.** Quien tenga acceso al proceso puede leer el atributo privado, y no se afirma lo contrario.

**`test_reveal_count` cuenta las aperturas de esta instancia en esta ejecución.** No es un registro histórico y **no demuestra** cuántas veces se observó el conjunto de prueba a lo largo del proyecto. El resultado lo declara explícitamente en `test_reveal_count_scope`.

## 4. Modelos y configuraciones

**22 configuraciones** evaluadas en validation (18 sin el modelo opcional). Sin AutoML ni búsqueda masiva.

| Familia | Rejilla | Configs |
|---|---|---|
| Logistic Regression | `C ∈ {0.1, 1, 10}` × `class_weight ∈ {None, balanced}` | 6 |
| Decision Tree | `max_depth ∈ {3,5,8}` × `min_samples_leaf ∈ {20,50}` | 6 |
| Random Forest | `max_depth ∈ {6,10,None}` × `min_samples_leaf ∈ {5,20}`, 300 árboles | 6 |
| HistGradientBoosting (opcional) | `max_depth ∈ {3,6}` × `learning_rate ∈ {0.05,0.1}` | 4 |

Se incluyó HistGradientBoosting porque viene en scikit-learn, no añade dependencias y ofrece una referencia no lineal más fuerte que el bosque.

**Mejor por familia (AP en validation):**

| Familia | AP | Configuración |
|---|---|---|
| **Logistic Regression** | **0.7574** | `C=10.0, class_weight=None` |
| HistGradientBoosting | 0.7466 | `max_depth=3, lr=0.05` |
| Random Forest | 0.7314 | `max_depth=10, min_samples_leaf=5` |
| Decision Tree | 0.6914 | `max_depth=5, min_samples_leaf=50` |

La regresión logística gana **de forma directa**: es a la vez la más simple y la de mayor AP, así que la regla de preferencia por simplicidad (margen 0.005) no tuvo que activarse.

## 5. Baselines

| Baseline | AP validation | AP test | Precision test | Recall test | Tasa de alerta test |
|---|---|---|---|---|---|
| Dummy (prior) | 0.3795 | 0.3807 | 0.3807 | 1.000 | 1.000 |
| Regla operacional (k=1, d=10) | 0.4037 | 0.4252 | 0.4959 | 0.3861 | 0.2964 |

La AP del dummy coincide con la prevalencia, que es exactamente la referencia de no-skill. Los parámetros de la regla operacional se mantuvieron **fijos**: optimizarlos la habría convertido en un modelo encubierto.

## 6. Regla de umbral

La Fase 14 prohibió fijar un umbral arbitrario y **no aprobó ninguna cifra** de precision o recall. La regla es por tanto **relativa**, anclada en el baseline, y se aplica **solo sobre validation**:

1. referencia = precision y recall del baseline operacional en validation;
2. elegibles = umbrales que **no empeoran ninguno de los dos ejes**;
3. entre los elegibles, el de **mayor F2** (β=2 pondera el recall cuatro veces más);
4. desempate por mayor recall y luego por umbral menor;
5. si ninguno domina al baseline, mayor F2 sobre toda la curva, marcado con `floor_satisfied=false`.

| Campo | Valor |
|---|---|
| **Umbral seleccionado (valor exacto)** | **`0.1679418172266036`** |
| Suelo de precision / recall | 0.4500 / 0.342857 |
| Umbrales elegibles | 554 de 830 |
| Precision / Recall / F2 en validation | 0.5169 / 0.9206 / 0.7963 |
| `floor_satisfied` | `true` |

**El umbral se persiste con toda su precisión.** Una versión redondeada a seis decimales (`0.167942`) cambia la clasificación de observaciones en la frontera y las métricas dejan de reproducirse. El freeze guarda el `float` exacto en `threshold`; `threshold_display` existe solo para lectura humana y **nunca** debe usarse para inferir.

### Por qué la regla cambió durante la fase

La primera versión solo ponía un suelo de precision y después maximizaba recall. Esa formulación converge al umbral más bajo admisible: en validation producía una **tasa de alerta del 81.4 %**. El plan de evaluación aprobado advierte expresamente contra la fatiga de alertas, así que un punto que marca casi todos los procesos no es útil aunque cumpla la restricción.

La regla se corrigió a «dominar al baseline en ambos ejes y después maximizar F2», que conserva la orientación al recall sin degenerar. La tasa de alerta bajó a 67.6 % en validation.

### Contaminación procedimental menor

La corrección se decidió a partir de una observación **de validation** (la tasa de alerta). Pero una primera ejecución completa ya había impreso la AP de test antes de cerrar la versión final de la regla.

Se clasifica como **MINOR PROCEDURAL CONTAMINATION** y queda registrada en las limitaciones conocidas del propio freeze.

AP es invariante al umbral y ninguna métrica de test dependiente de él se inspeccionó antes de la corrección. **No se encontró evidencia de un efecto material sobre la selección del modelo ni sobre el punto de operación, aunque no puede descartarse una influencia indirecta.**

Aun así, **este conjunto no puede describirse como *pristine holdout* ni como *never seen holdout***. Se denomina **holdout de evaluación final con contaminación procedimental menor documentada**.

## 7. Calibración

Ajustada con `CalibratedClassifierCV(method='sigmoid', cv=5)` **solo sobre train**, nunca con validation ni test.

| Métrica | Sin calibrar | Calibrado |
|---|---|---|
| Brier | 0.161408 | 0.161148 |
| ECE | 0.025874 | 0.027528 |
| AP | 0.757382 | 0.758120 |

**Decisión: no se adopta la calibración.** La regla exige mejorar Brier **y** ECE sin perder más de 0.01 de AP; aquí el ECE empeora. El modelo sin calibrar ya está bien calibrado (ECE 0.026 en validation, 0.041 en test).

**Nota para fases futuras.** La calibración se evaluó con `StratifiedKFold` aleatorio dentro de train. Como fue rechazada, no forma parte del modelo final y no se reentrenó nada por este motivo. Si alguna fase posterior la reconsidera, sería preferible usar **folds temporales** en lugar de validación cruzada aleatoria, para no mezclar periodos dentro del ajuste.

## 8. Freeze: protocolo previo al test

El orden lo impone el código, no una convención: **el protocolo se escribe en disco, se recarga y se verifica antes de que exista ningún número de test.**

```
selección con train/validation
  → construir freeze  → persist_freeze(ruta)   ← el artefacto ya existe en disco
  → load_freeze(ruta) → verificar integridad
  → sealed_test.reveal(freeze_recargado)       ← recién aquí se abre el test
  → evaluar test → artefacto de resultados separado
```

El freeze que abre el conjunto de prueba es **el recargado desde disco**, de modo que el artefacto versionado es literalmente el que autorizó la revelación.

### Contenido del protocolo

`docs/v1.1/ml/phase-15b-experiment-freeze.json` — huella `ec8e89cd408b8f5d4256a840b2455ee3034a41ad682e9dd2077f328aa6a72253`:

`schema_version` · `experiment_id` · `seed` · `dataset_fingerprint` · `config_fingerprint` · `split_signature` · `split_definition` · `feature_set` y `features` (15) · `excluded_features` · `ablation_feature_sets` · `preprocessing` · `model_family` y `model_params` · **`threshold` exacto** y `threshold_rule` · `threshold_selection` · `calibration_decision` · `validation_metrics` · `validation_baselines` · `ablation_conclusions` · `verdict_rule` · **`known_limitations`** · `frozen_at` · `freeze_fingerprint`.

### Lo que el freeze NO contiene

**Ningún resultado de test.** El campo `contains_test_results` lo declara explícitamente y una prueba verifica que ninguna clave del protocolo aloje métricas medidas sobre el test.

### La huella

Se calcula sobre el protocolo **excluyendo `frozen_at` y la propia huella**. Así es reproducible entre ejecuciones —dos corridas con la misma configuración producen la misma huella— y a la vez detecta cualquier alteración: cambiar el modelo, el umbral o las features rompe la verificación, y un archivo manipulado es rechazado al cargarse.

## 8bis. Resultados post-test, en artefacto separado

`docs/v1.1/ml/phase-15b-test-results.json` contiene las métricas de test, los baselines, el análisis por organización, la estabilidad temporal, el veredicto y las limitaciones. **Referencia `freeze_fingerprint`**: la dependencia va de resultados a protocolo, nunca al revés.

## 9. Resultado final en test

Evaluado **una vez en esta ejecución corregida**, con todo congelado. `test_reveal_count` es un contador local de la instancia actual, **no evidencia histórica absoluta**.

| Métrica | Validation | **Test** |
|---|---|---|
| **Average Precision** | 0.757382 | **0.769082** |
| ROC-AUC | 0.826100 | 0.833922 |
| Precision | 0.516934 | 0.483607 |
| Recall | 0.920635 | 0.933544 |
| F1 | 0.662100 | 0.637149 |
| F2 | 0.796266 | 0.787086 |
| Balanced accuracy | 0.697211 | 0.660352 |
| Brier | 0.161408 | 0.159213 |
| Brier Skill Score | 0.330926 | 0.341319 |
| ECE / MCE | 0.025874 / — | 0.041313 / 0.113893 |
| Tasa de alerta | 0.675904 | 0.734940 |
| Matriz de confusión | — | tp 295, fp 315, fn 21, tn 199 |

**Diferencia validation → test: AP +0.0117.** No hay degradación; el modelo mejora ligeramente.

## 10. Ablations

Con la configuración seleccionada, sin reajustar hiperparámetros, evaluadas en validation.

| Conjunto | n features | AP | Δ vs core | Recall | Precision | ECE |
|---|---|---|---|---|---|---|
| `core` | 15 | 0.7574 | — | 0.9206 | 0.5169 | 0.0259 |
| `core + configured_stage_count` | 16 | 0.7570 | **−0.0004** | 0.9175 | 0.5115 | 0.0320 |
| `core − elapsed_days_since_publication` | 14 | 0.7572 | **−0.0002** | 0.9143 | 0.5106 | 0.0253 |
| `core − concurrent_open_vacancies_count` | 14 | 0.7474 | **−0.0100** | 0.8889 | 0.5395 | 0.0518 |

**Lectura:**

- **`concurrent_open_vacancies_count`**: quitarla cambia AP en **−0.0100** (−1.32 % relativo: 0.7574 → 0.7474). Se reporta de forma **puramente descriptiva**, con magnitud absoluta y relativa: el código **ya no aplica ningún corte rígido** para clasificar la dependencia como «pequeña» o «apreciable», porque la Fase 14 no preregistró ningún umbral y cualquier categoría sería una heurística inventada a posteriori. **No es criterio de gate.** Sigue siendo la feature con mayor efecto y la que más conviene vigilar por su correlación con el calendario.
- **`elapsed_days_since_publication`**: quitarla no degrada nada (−0.0002). **El modelo no depende de ella**, lo que resuelve la preocupación por su colinealidad con `application_window_days` (Pearson 0.972): su peso es intercambiable, no imprescindible.
- **`configured_stage_count`**: añadirla no mejora (−0.0004). **Se mantiene fuera del núcleo.**

## 11. Estabilidad temporal

| Partición | AP | ROC-AUC | Recall | Precision | Brier | Prevalencia |
|---|---|---|---|---|---|---|
| Train | 0.6988 | 0.8299 | 0.8912 | 0.4437 | 0.1467 | 0.3036 |
| Validation | 0.7574 | 0.8261 | 0.9206 | 0.5169 | 0.1614 | 0.3795 |
| Test | 0.7691 | 0.8339 | 0.9335 | 0.4836 | 0.1592 | 0.3807 |

Por año: train 2023 → 2025 con AP 0.694 → 0.695 → 0.713; validation 2025 → 2026 con 0.753 → 0.786; test (íntegramente 2026) 0.769.

La AP sube con el tiempo porque la prevalencia también sube. **No hay degradación temporal** y el ROC-AUC, que es insensible a la prevalencia, se mantiene estable en 0.83.

## 12. Análisis por organización

`organization_id` **nunca entra en X**; se usa solo como metadato de evaluación. Las organizaciones son ficticias y no describen ninguna institución real.

| Org (test) | n | Prevalencia | AP | Recall | Precision |
|---|---|---|---|---|---|
| 1 | 67 | 0.2388 | 0.4762 | 0.6250 | 0.2564 |
| 2 | 144 | 0.3819 | 0.8038 | 0.9636 | 0.5300 |
| 3 | 137 | 0.2920 | 0.6994 | 0.9250 | 0.4205 |
| 4 | 180 | 0.2889 | 0.7820 | 0.9808 | 0.3750 |
| 5 | 93 | 0.5269 | 0.8141 | 0.8776 | 0.6515 |
| 6 | 209 | 0.4976 | 0.8405 | 0.9712 | 0.5580 |

La organización 1 es claramente la peor (AP 0.476 con n=67 y prevalencia 0.239). Con 67 casos la estimación es ruidosa y **no debe sobreinterpretarse**, pero es la mayor heterogeneidad observada y merece seguimiento.

## 13. Censura

Los censurados se excluyen del supervisado y **nunca reciben etiqueta imputada**. La censura es **informativa por diseño** (15A): mayor \|SMD\| 0.2298 en `days_since_last_operational_event`.

**Limitación:** el conjunto supervisado está sesgado hacia procesos que terminaron. Toda conclusión debe acompañarse de ese sesgo.

## 14. Importancia de features

Coeficientes estandarizados de la regresión logística, **descriptivos, no causales**:

| Feature | Coef. |
|---|---|
| `applications_received_count` | +2.6905 |
| `stage_transition_count` | −2.3842 |
| `days_remaining_to_target` | −1.4215 |
| `evaluations_scheduled_count` | +0.5170 |
| `evaluations_completed_count` | −0.3815 |
| `evaluations_overdue_pending_count` | +0.3080 |
| `concurrent_open_vacancies_count` | +0.2467 |

Intercepto −1.2317.

**Advertencia obligatoria:** `applications_received_count` y `stage_transition_count` tienen coeficientes grandes y de signo opuesto porque están fuertemente correlacionados por construcción — cada postulación genera su historial inicial, así que el par funciona como una diferencia («transiciones más allá de las iniciales»). Lo mismo ocurre, en menor escala, con `elapsed_days_since_publication` y `application_window_days`. **El reparto de peso entre features colineales es inestable y no debe leerse como importancia relativa real.**

## 15. Veredicto

Criterios fijados **antes** de abrir el test, todos comparativos:

Criterios comparativos, todos anclados en un baseline y **fijados en el freeze antes de abrir el test**:

| Criterio | Resultado |
|---|---|
| AP(test) por encima de la del dummy | ✅ 0.7691 > 0.3807 |
| AP(test) por encima de la del baseline operacional | ✅ 0.7691 > 0.4252 |
| Brier Skill Score(test) positivo | ✅ 0.3413 |
| Margen sobre el baseline preservado | ✅ 0.3439 en test frente a 0.3537 en validation |
| Persisten limitaciones conocidas | ✅ sí → el veredicto **no** puede ser GO a secas |

### **PREDICTIVE GO WITH LIMITATIONS**

El modelo supera con holgura a ambos baselines, está razonablemente calibrado y es estable en el tiempo. **Las limitaciones conocidas, registradas en el freeze antes de ver el test, degradan el veredicto de GO a GO CON LIMITACIONES**; no es un matiz de redacción, es la regla `limitations_downgrade_the_verdict` del protocolo.

### Limitaciones

1. **Tasa de alerta alta:** 73.5 % en test. Con recall 0.933 y precision 0.484, el punto de operación marca tres de cada cuatro procesos. Es el principal problema de diseño para la interfaz de 15C.
2. **F2 solo mejora modestamente sobre «alertar siempre»:** el dummy obtiene F2 0.7545 frente al 0.7871 del modelo. La comparación significativa es la AP (0.769 vs 0.381), no F2.
3. **Heterogeneidad alta por organización sintética:** AP entre 0.476 y 0.840.
4. **La organización 1 es débil y con muestra pequeña:** AP 0.476 con n=67 y prevalencia 0.239. No debe sobreinterpretarse.
5. **Censura informativa:** sesgo de selección hacia procesos que cerraron.
6. **Datos 100 % sintéticos:** el resultado demuestra método, no validez institucional.
7. **Colinealidad fuerte:** los coeficientes no son interpretables como importancia relativa.
8. **`concurrent_open_vacancies_count` como posible proxy temporal:** correlaciona 0.685 con el calendario; su ablation cuesta 0.0100 de AP.
9. **MINOR PROCEDURAL CONTAMINATION:** la AP de test se observó antes de cerrar la versión final de la regla de umbral (§6).
10. **`GAP-01` abierto** y **sin validez institucional**: el modelo **no es desplegable**.

### **GAP-01 y despliegue**

`target_completion_at` no existe en Laravel, así que `days_remaining_to_target` —la tercera feature por peso— **no es computable en producción**. El modelo **no es desplegable**, RF-29 sigue siendo candidato y no se autoriza integración ni servicio HTTP.

## 16. Reproducibilidad

Semilla `20260920` en dataset, split, modelos y calibración. Dos ejecuciones completas produjeron resultados idénticos: mismas huellas, mismo freeze, mismas métricas de test, mismo veredicto.

`RandomForestClassifier` y `HistGradientBoostingClassifier` llevan `random_state` fijo y se ejecutan con `n_jobs=1` para evitar no determinismo por paralelismo.

## 17. Pruebas

**305 pruebas, 0 fallos, 97 % de cobertura** (las 182 de 15A siguen pasando; 123 de 15B).

| Archivo nuevo | Pruebas | Garantía |
|---|---|---|
| `test_training_no_leakage.py` | 17 | Escalado solo con train, test sellado, sin metadatos ni prohibidas en X |
| `test_experiment_freeze.py` | 14 | Freeze completo, apertura única del test, criterios comparativos |
| `test_model_reproducibility.py` | 13 | Determinismo por familia y del experimento completo |
| `test_metrics.py` | 10 | Métricas contra valores calculados a mano |
| `test_threshold_selection.py` | 10 | Regla relativa, sin degenerar, determinista |
| `test_temporal_split.py` | 9 | Cronología, sin solapamiento, censurados fuera |
| `test_ablation.py` | 9 | Las tres obligaciones de la auditoría cubiertas |
| `test_freeze_contract.py` | 38 | Persistencia previa al reveal, integridad, **enlace a la configuración**, **`source_path` real**, **secciones científicas no vacías**, y reconstrucción de predicciones desde el artefacto |

## 18. Qué NO se implementó

FastAPI, `/health`, `/v1/predict`, uvicorn, servicio HTTP, Docker de ML, cliente Laravel, autenticación servicio-a-servicio y UI. Todo ello pertenece a 15C y 16. Tampoco se persistieron artefactos binarios de modelo: no hacen falta en 15B.

## Enlaces

- [Freeze del experimento](ml/phase-15b-experiment-freeze.json) · [Resumen de resultados](ml/phase-15b-results-summary.json)
- [Model card](ml/model-card-draft.md) · [Plan de evaluación](ml/evaluation-plan.md) · [Contrato de features](ml/feature-contract.md)
- [Fase 15A](phase-15a-synthetic-data.md) · [Fase 14](phase-14-ml-definition.md) · [ADR-004](architecture-decisions/ADR-004-ml-problem-definition.md)
