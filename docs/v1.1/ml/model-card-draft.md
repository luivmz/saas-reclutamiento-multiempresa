# Model card — EXPERIMENTAL

**Estado: `experimental`.** El modelo existe y fue evaluado en la Fase 15B sobre **datos exclusivamente sintéticos**. Las métricas de este documento provienen de una ejecución real y reproducible, no de metas ni ejemplos.

> **Científicamente aceptable no equivale a desplegable.** `GAP-01` sigue abierto y el modelo **no puede integrarse ni desplegarse**.

---

## Identificación

| Campo | Valor |
|---|---|
| Nombre | `process-delay-risk` |
| Versión del modelo | `0.1.0-experimental` (Fase 15B) |
| Estado | **`experimental`** — evaluado y aceptado científicamente, **no desplegable** |
| Fecha de esta versión | 20 de septiembre de 2026 |
| Propietario académico | Equipo del proyecto: Coronacion Meza Fredy, Peña Arroyo Anthony, Vila Meza Luis Antonio |
| Curso | Pruebas y Calidad de Software, NRC 28607, Universidad Continental |
| Docente | Dr. Maglioni Arana Caparachin |
| Revisión y aprobación | Auditoría científica de Codex **pendiente** |
| Evidencia | [`phase-15b-experiment-freeze.json`](phase-15b-experiment-freeze.json) · [`phase-15b-results-summary.json`](phase-15b-results-summary.json) · [`../phase-15b-training-evaluation.md`](../phase-15b-training-evaluation.md) |

## Propósito

Estimar, con fines **académicos y experimentales**, la probabilidad de que un proceso de selección cierre después de su plazo operacional objetivo, a partir de señales operacionales agregadas disponibles en un checkpoint fijo.

**No** evalúa, puntúa, ordena ni clasifica personas. **No** interviene en ninguna decisión sobre candidatos.

## Unidad de análisis y checkpoint

- **Unidad:** un snapshot único de una vacante elegible. Máximo una observación por `vacancy_id`.
- **Checkpoint:** inicio del día inmediatamente posterior a `vacancies.closes_at`, en `America/Lima`.
- Detalle y justificación: [`problem-definition.md` §3](problem-definition.md).

## Target

```
delayed = 1  si  vacancies.closed_at >  target_completion_at
delayed = 0  si  vacancies.closed_at <= target_completion_at
```

**Aprobado conceptualmente** el 20/09/2026 (decisión 3). `ML-DECISION-01` quedó resuelta: `job_requests.required_by` **no** se reinterpreta y se aprueba la necesidad de un plazo operacional explícito.

**PENDIENTE para despliegue — `GAP-01`.** `target_completion_at` **no existe en Laravel**. El experimento lo obtiene del dataset sintético, que lo modela como variable operacional explícita. El modelo resultante **no es integrable** hasta que la brecha se resuelva en una fase posterior.

## Datos

| Campo | Valor |
|---|---|
| Origen | **Sintético**, generado a partir de la estructura del proceso |
| Versión | `synthetic-v1` *(no generado)* |
| Volumen | 6 000 observaciones propuestas |
| Periodo simulado | ≥ 36 meses |
| Organizaciones | 4 – 8, totalmente ficticias |
| Seed | `20260920` |
| Datos reales o PII | **Ninguno.** No se obtienen ni se usan |
| Hash del dataset | `PENDIENTE DE MEDICIÓN` |

## Features

- **Incluidas:** 14 del conjunto núcleo, más `days_remaining_to_target` condicionada a la aprobación del target. Lista completa con definiciones: [`feature-contract.md` §1](feature-contract.md).
- **Excluidas en v1:** 7 candidatas documentadas con su motivo ([§2](feature-contract.md)).
- **Prohibidas:** identidad, atributos sensibles, proxies socioeconómicos, contenido textual, puntajes, resultados de entrevista, ranking, decisión, identificadores y todo dato posterior al checkpoint ([§3](feature-contract.md)).

## Partición

Bloques temporales 70 / 15 / 15 ordenados por `checkpoint_at`, con desempate determinista por `vacancy_id`. **Test se abrió exactamente una vez**, tras el freeze.

| Partición | n | Prevalencia | Periodo |
|---|---|---|---|
| Train | 3 873 | 0.3036 | 2023-01-18 → 2025-08-07 |
| Validation | 830 | 0.3795 | 2025-08-07 → 2026-02-04 |
| Test | 830 | 0.3807 | 2026-02-04 → 2026-08-22 |

## Baselines y modelo

**22 configuraciones** evaluadas en validation.

| Rol | Definición | AP validation | AP test |
|---|---|---|---|
| Baseline trivial | `DummyClassifier(strategy='prior')` | 0.3795 | 0.3807 |
| Baseline operacional | Backlog vencido ≥ 1 **o** ≥ 10 días sin actividad (k=1, d=10, fijos) | 0.4037 | 0.4252 |
| **Modelo seleccionado** | **Logistic Regression**, `C=10.0`, `class_weight=None`, con `StandardScaler` | **0.7574** | **0.7691** |
| Comparación | HistGradientBoosting 0.7466 · Random Forest 0.7314 · Decision Tree 0.6914 | — | — |

La regresión logística fue a la vez la más simple y la de mayor AP.

## Métricas

Medidas sobre **test**, con la configuración congelada. Prevalencia de test 0.3807.

| Métrica | Valor |
|---|---|
| **Average Precision (primaria)** | **0.769082** |
| Precision / Recall / F1 al umbral | 0.483607 / 0.933544 / 0.637149 |
| F2 | 0.787086 |
| Matriz de confusión | tp 295, fp 315, fn 21, tn 199 |
| Balanced accuracy | 0.660352 |
| ROC-AUC (contexto) | 0.833922 |
| Brier score | 0.159213 |
| Brier Skill Score | 0.341319 |
| ECE / MCE | 0.041313 / 0.113893 |
| Tasa de alerta | 0.734940 |
| Prevalencia por bloque | train 0.3036 · validation 0.3795 · test 0.3807 |
| AP por organización (test) | 0.476 – 0.840 según organización sintética |
| Intervalo bootstrap pareado vs. baseline | `PENDIENTE DE MEDICIÓN` — no ejecutado en 15B |

## Calibración y umbrales

| Campo | Valor |
|---|---|
| Método evaluado | `sigmoid` con `CalibratedClassifierCV(cv=5)`, ajustado **solo en train** |
| Decisión | **No se adopta**: mejora Brier (0.1614 → 0.1611) pero empeora ECE (0.0259 → 0.0275) |
| Calibración del modelo final | Sin calibrar; ECE 0.0259 en validation y 0.0413 en test |
| Umbral operativo | **0.167942**, elegido **solo con validation** |
| Regla del umbral | Dominar al baseline operacional en precision **y** recall; entre los elegibles, mayor F2; desempate por recall y luego por umbral menor |
| Suelos (del baseline, no inventados) | precision ≥ 0.4500 · recall ≥ 0.342857 |
| `t_high` / `t_medium` | **No definidos**: siguen sin existir metas aprobadas de precision/recall |
| Comportamiento sin metas aprobadas | Devolver solo probabilidad; `risk_level = null` |

## Limitaciones

1. **Los datos son sintéticos.** Un buen resultado demostraría que el método es correcto, no que funcionaría en el Colegio Andino de Huancayo.
2. **Censura estructural.** Una vacante solo se cierra tras decisión y selección humanas, de modo que los procesos atascados nunca producen `closed_at` y quedan excluidos. Eso sesga la muestra hacia procesos que terminaron. La Fase 15 debe **medir** ese sesgo, no solo declararlo (decisión 10).
3. **El plazo objetivo no existe en el sistema.** Está aprobado conceptualmente, pero `GAP-01` sigue abierta: una de las quince features utilizables (`ML-FEAT-02`) **no es computable en Laravel hoy**. El modelo no es desplegable hasta resolverlo.
4. **Alcance temporal.** Una sola observación por proceso, en un único checkpoint.
5. **Sin validación externa.** Ninguna comparación contra datos reales es posible ni está prevista.
6. **Tasa de alerta alta.** En el umbral elegido el modelo marca el **73.5 %** de los procesos de test (recall 0.934, precision 0.484). Es consecuencia directa de una regla recall-oriented y constituye el principal problema de diseño para la interfaz de 15C.
7. **F2 poco discriminante en este régimen.** Un predictor que alerta sobre todo obtiene F2 0.7545 frente al 0.7871 del modelo. La comparación significativa es la AP (0.769 frente a 0.381), no F2.
8. **Heterogeneidad entre organizaciones sintéticas.** AP entre 0.476 (n=67) y 0.840. La organización con peor desempeño tiene pocos casos y su estimación es ruidosa; no debe sobreinterpretarse.
9. **Censura informativa medida.** Mayor \|SMD\| 0.2298 en `days_since_last_operational_event`. La censura contextual por ventana es comparable (train 0.074, validation 0.087, test 0.086).
10. **Coeficientes no interpretables como importancia.** `applications_received_count` (+2.69) y `stage_transition_count` (−2.38) están fuertemente correlacionados por construcción, igual que `elapsed_days_since_publication` y `application_window_days` (Pearson 0.972). El reparto de peso entre features colineales es inestable.
11. **Deriva temporal presente pero no degradante.** La AP sube de train (0.699) a test (0.769) porque la prevalencia también sube; el ROC-AUC se mantiene estable en 0.83.

## Ablations verificadas

| Feature | Efecto al quitarla (ΔAP en validation) | Lectura |
|---|---|---|
| `concurrent_open_vacancies_count` | **−0.0100** | Señal moderada; por debajo de la tolerancia 0.02, no se declara dependencia de proxy temporal |
| `elapsed_days_since_publication` | **−0.0002** | El modelo **no** depende de ella pese a su colinealidad |
| `configured_stage_count` (al añadirla) | **−0.0004** | No aporta; se mantiene fuera del núcleo |

## Usos permitidos

Demostración metodológica académica: diseño de problema, generación reproducible, entrenamiento, evaluación honesta, calibración, integración técnica y documentación de un no-go.

## Usos prohibidos

Evaluar, puntuar, ordenar, recomendar, filtrar o descartar personas. Sustituir o condicionar la decisión del Aprobador/Dirección. Alimentar el ranking de RF-20 a RF-22. Presentarse como capacidad validada del producto. Cualquier uso institucional real.

## Ética y privacidad

Frontera completa en [`ethics-and-human-oversight.md`](ethics-and-human-oversight.md). Ningún atributo sensible ni proxy. Ningún dato personal cruza el límite Laravel ↔ ML.

## Supervisión humana

La decisión final pertenece siempre a una persona identificable, con justificación registrada y auditoría inalterable. El modelo no dispara acciones automáticas.

## Arquitectura y fallback

Laravel es el sistema de registro. El servicio de inferencia es opcional y sin estado. Si falla, es lento o responde algo inválido, la pantalla se muestra sin estimación y el proceso continúa completo. Detalle: [`api-contract-draft.md`](api-contract-draft.md).

## Actualización y retiro

**[PROPUESTA]** El modelo se retira si: cambia la semántica del plazo objetivo, se detecta fuga posterior, el rendimiento se degrada entre periodos, aparece cualquier uso fuera de los permitidos, o el equipo académico concluye el proyecto. No hay reentrenamiento automático.

## Linaje

| Campo | Valor |
|---|---|
| Hash del artefacto | *(no aplica)* — en 15B no se persiste ningún binario de modelo |
| Hash del dataset (model-ready) | `d94fe60d941be87580c71c3a72155b59a0b3a38071ad619ecd986bf607f1b2ae` |
| Hash de la configuración | `4107a60ede323da2bc834128e449628f8c05a797ccf623cbfdfc3b93408b72df` |
| Versión del contrato de features | `feature-contract.md`, Fase 14 |
| Semilla | `20260920` (dataset, split, modelos y calibración) |
| Versiones de librerías | Python 3.12.5 · scikit-learn 1.9.1 · numpy 2.1.3 · pandas 2.2.3 · scipy 1.18.1 · joblib 1.6.0 |
| Reproducibilidad | Dos ejecuciones completas produjeron huellas, freeze, métricas de test y veredicto idénticos |

## Veredicto de la Fase 15B

**PREDICTIVE GO**, con las limitaciones de la sección anterior. Criterios comparativos fijados antes de abrir el test: supera al dummy (0.769 > 0.381), supera al baseline operacional (0.769 > 0.425), Brier Skill Score positivo (0.341), margen preservado (0.344 en test frente a 0.354 en validation) y sin dependencia de proxy temporal.

**Prohibición de despliegue mientras `GAP-01` siga abierto.** `days_remaining_to_target` —tercera feature por peso— no es computable en Laravel, así que el modelo no puede integrarse. RF-29 sigue siendo candidato.
