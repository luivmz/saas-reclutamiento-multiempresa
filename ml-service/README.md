# ml-service — generador sintético y experimento de ML (Fases 15A y 15B)

Componente Python del experimento académico de **riesgo operacional de retraso** de un proceso de selección. Implementa lo aprobado en la Fase 14 y **nada más**.

> Los datos sintéticos permiten demostrar metodología, entrenamiento, integración y evaluación técnica. **No demuestran validez predictiva real sobre procesos del Colegio Andino de Huancayo ni autorizan uso institucional.**

## Qué hay aquí y qué no

| Implementado (15A + 15B) | No implementado todavía |
|---|---|
| Estructura del paquete y configuración reproducible | FastAPI, `/v1/predict`, `/health` (15C) |
| Generador sintético *event-first* (15A) | Docker del ML (15C) |
| Contrato de columnas y validaciones | Cliente Laravel y contrato HTTP (15C/16) |
| Entrenamiento, evaluación y ablations (15B) | Persistencia de artefactos de modelo |
| Suite de pruebas (264) | Despliegue: bloqueado mientras `GAP-01` siga abierto |
| CLI de generación y CLI de experimento | |

El modelo analiza **el proceso**, nunca a una persona. No puntúa, ordena, recomienda ni descarta postulantes.

## Instalación

Entorno virtual local, aislado y no versionado:

```bash
cd ml-service
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev]"   # Windows
# .venv/bin/python -m pip install -e ".[dev]"         # macOS / Linux
```

Requiere Python ≥ 3.12. Dependencias fijadas: `numpy==2.1.3`, `pandas==2.2.3`, `pydantic==2.9.2`, `tzdata==2024.2`, `scikit-learn==1.9.1`, `scipy==1.18.1`, `joblib==1.6.0`; desarrollo: `pytest==8.3.3`, `pytest-cov==5.0.0`.

`tzdata` no es opcional en Windows: sin ella `zoneinfo` no resuelve `America/Lima`, y toda la cronología depende de esa zona.

## Uso

```bash
.venv/Scripts/python.exe -m recruitment_ml.synthetic.generator \
    --rows 6000 --seed 20260920 --organizations 6 --months 42 \
    --output artifacts/synthetic-v1.csv
```

Opciones: `--rows`, `--seed`, `--organizations`, `--months`, `--output`, `--model-ready` (exporta solo las filas etiquetadas).

Cada exportación escribe además `<output>.manifest.json` con su linaje. **La huella anunciada es siempre la del frame realmente escrito**: en modo `model-ready` el hash corresponde a las filas etiquetadas, no al dataset completo. El manifiesto incluye ambas (`dataset_fingerprint` del modo exportado y `full_dataset_fingerprint` / `model_ready_fingerprint`), y `generated_at` queda fuera de toda huella para que la parte científica sea reproducible.

**La salida nunca se versiona.** `artifacts/` y todo `*.csv`, `*.parquet`, `*.pkl`, `*.joblib` dentro de `ml-service/` están en `.gitignore`.

Desde Python:

```python
from recruitment_ml.config import SyntheticConfig
from recruitment_ml.synthetic.generator import build_dataset
from recruitment_ml.synthetic.validators import validate_dataset

dataset = build_dataset(SyntheticConfig(rows=6000))
print(validate_dataset(dataset))       # "dataset valido"
X = dataset.feature_matrix()           # solo features model-ready
y = dataset.model_ready()["delayed"]   # sin censurados
```

## Experimento de entrenamiento (15B)

```bash
.venv/Scripts/python.exe -m recruitment_ml.training.experiment \
    --rows 6000 --seed 20260920 \
    --output-dir artifacts/phase-15b --evidence-dir ../docs/v1.1/ml
```

Opciones: `--rows`, `--seed`, `--output-dir` (artefactos completos, ignorados por Git), `--evidence-dir` (evidencia reducida y versionable), `--skip-optional-model`.

El orden es estricto y lo impone el código: dataset → split temporal → selección con train/validation → umbral con validation → calibración con train → ablations → **freeze** → apertura del test **una sola vez** → veredicto. `SealedTestSet` lanza `SealedTestSetError` si se intenta abrir el conjunto de prueba sin un `ExperimentFreeze`.

Resultado de referencia: **Logistic Regression**, AP test **0.769** frente a 0.381 del dummy y 0.425 del baseline operacional, **PREDICTIVE GO** con limitaciones. Detalle en [`docs/v1.1/phase-15b-training-evaluation.md`](../docs/v1.1/phase-15b-training-evaluation.md).

## Estructura

```
ml-service/
├── pyproject.toml              dependencias fijadas y configuración de pytest
├── src/recruitment_ml/
│   ├── config.py               SyntheticConfig: toda constante vive aquí
│   ├── schema.py               contrato de columnas y prohibiciones
│   ├── synthetic/              generación del dataset (15A)
│   │   ├── distributions.py    familias de distribución con su justificación
│   │   ├── timeline.py         simulación event-first de un proceso
│   │   ├── generator.py        orquestación, manifiesto y CLI
│   │   └── validators.py       las 20 validaciones aprobadas
│   └── training/               entrenamiento y evaluación (15B)
│       ├── split.py            partición temporal y conjunto sellado
│       ├── preprocessing.py    conjuntos de features y matrices
│       ├── baselines.py        dummy y regla operacional
│       ├── models.py           familias y rejillas de hiperparámetros
│       ├── evaluation.py       métricas y calibración observada
│       ├── thresholds.py       regla de umbral relativa al baseline
│       ├── calibration.py      calibración ajustada solo con train
│       ├── ablation.py         las tres ablations obligatorias
│       └── experiment.py       orquestación, freeze y CLI
├── tests/                      264 pruebas
└── artifacts/                  salida local, ignorada por Git
```

## Generación *event-first*

El orden no es negociable: **la etiqueta nunca se calcula a partir del vector de features.**

1. Solicitud del requerimiento y configuración de la vacante.
2. **`target_completion_at` se fija aquí**, antes de publicar, y no vuelve a tocarse.
3. Publicación, ventana de postulaciones y cierre.
4. `checkpoint_at` = inicio del día siguiente al cierre, en `America/Lima`.
5. Eventos operacionales hasta el checkpoint: postulaciones, preselecciones, evaluaciones, entrevistas, transiciones.
6. **Corte**: las features se derivan solo del historial truncado en el checkpoint.
7. Continuación estocástica posterior: el tiempo restante depende del backlog observable, de los factores latentes y de un ruido irreducible.
8. Cierre real y, **solo entonces**, `delayed = closed_at > target_completion_at`.

Los factores latentes (`operational_capacity`, `coordination_friction`, `workload_pressure`, `random_shock`, `period_effect`) existen solo en memoria y **nunca se exportan**. Son la causa común que hace que features y desenlace covaríen sin que el target sea una función de las features.

### Historial de etapas

Se modela la semántica real, verificada en el código: `ApplicationService::apply()` crea **un** `ApplicationStageHistory` inicial (`null → postulado`) en el mismo instante que `applied_at`, y `ApplicationStageService::transition()` crea **uno** por cada cambio posterior. Por eso toda postulación anterior al checkpoint aporta al menos un evento, y `stage_transition_count` nunca puede ser menor que `applications_received_count`.

## Features

15 columnas model-ready: las 14 del núcleo del contrato más `days_remaining_to_target`.

`evaluations_pending_count` e `interviews_pending_count` se generan como **auxiliares** para validar la identidad `pending = scheduled − completed`, pero quedan fuera de X por ser colinealidad exacta.

`ABLATION_REQUIRED_IN_15B` declara las features que 15B **debe** comparar entrenando con y sin ellas: `concurrent_open_vacancies_count` (crece con el calendario), `configured_stage_count` (cardinalidad máxima 2) y `elapsed_days_since_publication` (casi colineal con la ventana por construcción del checkpoint).

Las variables prohibidas están en `schema.py` y las comprueba `is_forbidden_column`, **por token completo y no por subcadena**: `evaluation_score` queda bloqueada por el token `score`, mientras `coverage_ratio`, `management_latency` y `filename` pasan, porque una búsqueda de subcadenas los bloquearía por contener «age» o «name».

## Censura

Un proceso estancado **nunca cierra**, porque cerrar exige decisión y selección humanas. Esos procesos se marcan `observation_status = "censored"`, su etiqueta queda `NA` y **no entran** en el conjunto supervisado. No se les asigna `0` ni `1` bajo ninguna circunstancia.

La censura es **informativa por diseño**: la probabilidad de estancamiento se construye en escala logit alrededor de `stall_rate` y depende de la fricción de coordinación, la presión de carga, la capacidad operativa, el shock y los días sin actividad. Está acotada a `[0.005, 0.60]`, de modo que nunca es determinista y siempre existe solapamiento entre censurados y completados. **Es una decisión de simulación académica, no una observación institucional.**

El manifiesto reporta `censored_total`, `censored_stalled`, `censored_observation_window`, `censoring_ratio`, `censoring_mechanism` y `censoring_comparison`, esta última con las diferencias de medias estandarizadas (SMD) entre censurados y completados.

## Pruebas

```bash
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pytest --cov=recruitment_ml --cov-report=term-missing
```

264 pruebas, 97 % de cobertura.

## Limitaciones conocidas

1. **Los datos son sintéticos.** Un buen resultado demostraría que el método es correcto, no que funcionaría en la institución del caso de estudio.
2. **`target_completion_at` no existe en Laravel.** Está aprobado conceptualmente; su implementación es `GAP-01`. Mientras siga abierta, `days_remaining_to_target` no es computable en producción y **el modelo no es desplegable** aunque el experimento tenga éxito.
3. **`concurrent_open_vacancies_count` crece con el calendario** (Pearson 0.685, Spearman 0.708 frente al tiempo en el dataset de referencia), en buena parte porque los procesos estancados permanecen abiertos indefinidamente: su correlación con la censura acumulada es 0.685. Es fiel al dominio real, donde no existe cancelación (A-22), y produce el drift buscado, pero **15B debe comparar el modelo con y sin esta feature**.
4. **`elapsed_days_since_publication` y `application_window_days` quedan casi colineales** (Pearson 0.972). La identidad exacta universal se eliminó generando un desfase entre publicación y apertura de postulaciones, pero la redundancia residual es estructural: el checkpoint se define como `closes_at + 1`. Donde `opens_at` es nulo la identidad es definicional, por la propia regla de respaldo del contrato.
5. **Las distribuciones son supuestos académicos**, no estadísticas observadas de ninguna institución.
6. **La prevalencia está calibrada estructuralmente**, ajustando el proceso y nunca filtrando etiquetas ni remuestreando.
7. **La censura es informativa por diseño**, no MCAR. 15B debe evaluar el sesgo de selección, no solo declararlo.
