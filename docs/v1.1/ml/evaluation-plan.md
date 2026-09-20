# Plan de evaluación

**Fase 14 · 20 de septiembre de 2026**

**[LIMITACIÓN] Ninguna métrica de este documento ha sido medida.** Todo valor aparece como `PENDIENTE DE MEDICIÓN`. Este plan define cómo se medirá, no qué resultó.

> **[APROBADA] Decisiones 5, 6, 7, 8, 10 y 12 del equipo, 20 de septiembre de 2026.** Quedan aprobados el split temporal 70/15/15, el conjunto de modelos, Average Precision como métrica primaria con sus secundarias, la **política** de umbrales (sin cifras), el tratamiento de la censura y la totalidad de los criterios de no-go.

---

## 1. Partición temporal

**[APROBADA] `ML-SPLIT-01`** *(decisión 5)* — Bloques temporales **70 / 15 / 15** ordenados por `checkpoint_at`:

| Bloque | Proporción | Uso |
|---|---|---|
| Train | 70 % más antiguo | Ajuste de preprocesamiento, entrenamiento, validación cruzada temporal de ventana expansiva para hiperparámetros, fijación del baseline operacional |
| Validation | 15 % siguiente | Selección final del modelo, calibración y elección de umbrales |
| Test | 15 % más reciente | **Se usa una sola vez**, para la conclusión final |

Empates de `checkpoint_at` se resuelven de forma determinista por un ID de metadatos, nunca al azar.

### Por qué no un split aleatorio estratificado

Un split aleatorio mezclaría periodos y ocultaría el drift que el generador introduce a propósito. Además dejaría pasar fuga temporal: un proceso de 2027 podría entrenar un modelo evaluado sobre 2026. La comparación honesta es contra el futuro, no contra una muestra intercalada.

### Por qué 70/15/15 y no 80/20

Con 80/20 no queda un conjunto independiente para **calibrar** y **elegir umbrales**. Hacer esas dos cosas sobre test lo contaminaría y convertiría la métrica final en una estimación optimista. Tres bloques permiten entrenar, decidir y luego medir una sola vez.

### Reglas de aislamiento

1. Un proceso nunca aparece en más de un conjunto.
2. Si una v2 introdujera varios checkpoints por proceso, se agrupa por `vacancy_id` **antes** de dividir.
3. Ninguna transformación aprende de validation ni de test: imputación, escalado y codificación se ajustan solo con train.
4. `organization_id` se usa para auditar la distribución, jamás como feature.
5. Se reporta la prevalencia por bloque, pero **no** se reordena el tiempo para igualarla.

---

## 2. Baselines

Son tres cosas distintas y no deben confundirse.

### 2.1 Baseline trivial · `ML-BASE-01`

- `DummyClassifier(strategy="most_frequent")` para accuracy y balanced accuracy.
- Predictor constante igual a la prevalencia de **train** para las métricas probabilísticas: fija el Average Precision de no-skill y el Brier de referencia.

### 2.2 Baseline operacional · `ML-BASE-02`

**[PROPUESTA]** Regla transparente basada en dos señales de backlog:

```
alerta  ⟺  (evaluations_overdue_pending_count + interviews_overdue_pending_count) ≥ k
           ó  days_since_last_operational_event ≥ d
```

`k` y `d` se estiman **solo con train** y se **congelan antes** de tocar validation o test. La regla no se ajusta mirando resultados posteriores; hacerlo la convertiría en un modelo disfrazado de baseline.

### 2.3 Primer modelo ML · `ML-MODEL-01`

**Logistic Regression** con preprocesamiento reproducible. Es el primer modelo, no un baseline. **Es la opción preferida si su desempeño cae dentro de la incertidumbre de modelos más complejos**, por explicabilidad, estabilidad y sencillez de despliegue.

### 2.4 Comparación mínima

**[APROBADA]** *(decisión 6)*

| Modelo | Estado | Restricción |
|---|---|---|
| Dummy / predictor de prevalencia | Aprobado | Baseline trivial obligatorio |
| Baseline operacional sencillo | Aprobado | Umbrales estimados y congelados en train |
| Logistic Regression | Aprobado — **primer modelo** | Escalado ajustado en train; regularización con pocos valores justificados |
| Decision Tree | Aprobado — comparación | Profundidad regularizada y mínimo de muestras por hoja |
| Random Forest | Aprobado — comparación | Número de árboles y profundidad acotados |
| HistGradientBoosting | **Opcional y condicionado** | Solo con justificación experimental explícita y mejora estable |

**Prohibidos:** deep learning, redes neuronales, LLM, AutoML y ensembles innecesarios. Sin búsqueda masiva de hiperparámetros: pocos valores justificados, seed fija y reproducibilidad por encima de la última décima de métrica.

---

## 3. Métricas

### 3.1 Primaria

**[APROBADA]** *(decisión 7)* **Average Precision (AP)**, entendida como el resumen de la curva Precision–Recall calculado como media ponderada de las precisiones por incremento de recall — **no** como integración trapezoidal de la curva.

Es primaria porque la clase retrasada puede ser minoritaria, porque accuracy ocultaría el fallo justo en esa clase, porque interesa recuperar procesos riesgosos sin saturar la interfaz de alertas y porque resume el desempeño sin depender de un único umbral.

### 3.2 Secundarias obligatorias

| Métrica | Estado |
|---|---|
| Precision, recall y F1 al umbral operativo | `PENDIENTE DE MEDICIÓN` |
| F2, si se ratifica que el falso negativo pesa más | `PENDIENTE DE MEDICIÓN` |
| Matriz de confusión | `PENDIENTE DE MEDICIÓN` |
| Balanced accuracy | `PENDIENTE DE MEDICIÓN` |
| ROC-AUC, solo como contexto y nunca aislada | `PENDIENTE DE MEDICIÓN` |
| Brier score y **Brier Skill Score** frente al predictor constante | `PENDIENTE DE MEDICIÓN` |
| Curva de calibración / diagrama de confiabilidad | `PENDIENTE DE MEDICIÓN` |
| Prevalencia de clase por bloque | `PENDIENTE DE MEDICIÓN` |
| Métricas por bloque temporal y por organización sintética | `PENDIENTE DE MEDICIÓN` |
| Intervalos bootstrap y comparación **pareada** contra el baseline más fuerte | `PENDIENTE DE MEDICIÓN` |

### 3.3 Costo de los errores

**[PROPUESTA]** Cualitativo, sin cifras inventadas:

- **Falso negativo:** no advertir a tiempo un proceso que terminará fuera de plazo. Es el error más costoso operacionalmente, porque anula el propósito del aviso.
- **Falso positivo:** atención innecesaria y fatiga de alertas. Importa, pero **no afecta ninguna decisión sobre una persona**.

**[APROBADA]** *(decisión 8)* La política de selección de umbral es:

1. el umbral se selecciona **únicamente con validation**;
2. la orientación principal es hacia **recall**;
3. se **controla precision** para evitar fatiga de alertas;
4. el umbral se **congela antes** de tocar test;
5. **test nunca** se usa para escogerlo.

**[PENDIENTE]** Los **valores concretos** de precision y recall se determinan experimentalmente en la Fase 15 y deben quedar documentados con su justificación. **[LIMITACIÓN]** No se define ningún costo monetario ni valor institucional absoluto: con datos sintéticos sería una invención.

---

## 4. Calibración y umbrales

**[LIMITACIÓN]** La probabilidad es una estimación condicionada al generador sintético. No es certeza, ni riesgo institucional validado.

**[PROPUESTA]** Procedimiento, en orden:

1. Medir Brier y curva de calibración del modelo **sin calibrar**.
2. Conservar Logistic Regression sin recalibración si ya resulta adecuada.
3. Probar **sigmoid (Platt)** como primera corrección, usando solo train/validation o predicciones out-of-fold temporales.
4. Usar **isotónica solo** si hay muestra de calibración suficiente y estabilidad demostrada. No es el método por defecto: con pocas muestras sobreajusta.
5. Adoptar la calibración únicamente si mejora Brier y confiabilidad en validation **sin degradar materialmente** la discriminación.
6. **Nunca** calibrar ni elegir método mirando test.

### Umbrales

**[PROPUESTA]** No se fijan categorías por intuición. El procedimiento es:

- `t_high`: el menor umbral que cumple en **validation** la precision mínima fijada experimentalmente.
- `t_medium`: el menor umbral que cumple en **validation** la meta de recall fijada experimentalmente, con `t_medium < t_high`.
- **[PENDIENTE]** Las cifras se determinan en la Fase 15 y se documentan. **No se inventan hoy** (decisión 8).
- Elegidos los umbrales, se **congelan** junto con su versión antes de tocar test.
- **Si no hay metas aprobadas, el prototipo devuelve únicamente probabilidad calibrada y `risk_level` queda `null`.**
- Toda categoría publicada lleva versión de umbrales y rótulo de «estimación sintética».

---

## 5. Interpretabilidad

**[PROPUESTA]** Dos niveles:

- **Global:** coeficientes estandarizados de Logistic Regression **y** *permutation importance* medida en validation/test. La importancia nativa de árboles se usa solo como complemento: está sesgada hacia variables de alta cardinalidad.
- **Local:** para Logistic Regression, contribución de cada feature al logit, traducida a etiquetas operacionales y limitada a los principales factores en cada dirección.

**[LIMITACIÓN]** Los coeficientes **no** son causalidad. No se introduce SHAP: solo se justificaría en una fase posterior si un modelo no lineal aprobado necesitara explicaciones locales y el costo aportara valor demostrable.

La interfaz futura dirá «Factores operacionales asociados a la estimación de riesgo». Nunca «motivos por los que un candidato no es apto». Ningún factor puede nombrar personas, puntajes, universidad, CV, resultado de entrevista, ranking ni decisión humana.

---

## 6. Criterios de aceptación del futuro experimento

**[PROPUESTA]** El experimento será aceptable para continuar **como prototipo técnico** solo si se cumplen **todos**:

1. El pipeline es reproducible por seed, configuración y versiones registradas.
2. El esquema y las invariantes del dataset pasan.
3. No se detecta fuga tras una revisión explícita y documentada.
4. Train, validation y test son temporales e independientes.
5. El modelo supera al baseline trivial **y** al baseline operacional en **AP sobre test**.
6. El intervalo bootstrap **pareado** de la diferencia de AP frente al baseline más fuerte respalda una mejora positiva — o se documenta honestamente que **no es concluyente**.
7. El modelo no compra AP a costa de un recall inaceptable en el umbral fijado en validation.
8. El Brier Skill Score es positivo frente al predictor constante y la confiabilidad no muestra descalibración grave.
9. El resultado es estable por periodo y no depende de una sola organización sintética.
10. Se elige la opción **más simple** dentro de la incertidumbre estadística.
11. Inferencia y preprocesamiento son deterministas y el contrato tolera los casos borde.
12. Todas las pruebas especificadas pasan realmente.

**[LIMITACIÓN]** No se fija ninguna cifra absoluta de AP, F1 o recall como «calidad institucional». Con datos sintéticos sería arbitraria. Los criterios son **relativos** (contra baseline), de **estabilidad** y de **calibración**, que sí son defendibles.

---

## 7. Criterios de NO-GO

**[APROBADA]** *(decisión 12: se mantienen todos los criterios)* Se declara **NO-GO predictivo** si ocurre cualquiera:

1. Se pierde la definición inequívoca y estable del plazo objetivo — resuelta conceptualmente por la decisión 3, pero **no implementada**: si `GAP-01` no se resuelve, el modelo no es desplegable aunque el experimento tenga éxito.
2. El target resulta tautológico o artificial.
3. El generador hace la etiqueta casi determinista.
4. Existe fuga estructural que no puede eliminarse.
5. El modelo no supera de forma estable al baseline más fuerte.
6. La señal depende de variables personales o prohibidas.
7. Las métricas varían severamente por periodo u organización sintética.
8. La probabilidad está gravemente descalibrada.
9. La explicación induce a evaluar personas.
10. El costo académico pone en riesgo entregables obligatorios.

### Dos desenlaces distintos

- **NO-GO para presentar un predictor válido o desplegable.** El sistema no incorpora la estimación.
- **Prototipo experimental no validado.** Puede conservarse como demostración metodológica **si se rotula y se aísla correctamente**, sin presentarse como capacidad del producto.

**[APROBADA]** *(decisión 12)* Si el experimento no supera el baseline, presenta fuga no resoluble, descalibración grave o resultados artificialmente fáciles, **no se presentará como predictor válido** y el fallback es el enfoque descriptivo.

Un NO-GO conduce al panel descriptivo (RF-28 candidato) y **no cancela el trabajo académico**: un no-go bien demostrado es un resultado publicable y más honesto que un predictor artificialmente exitoso.

---

## 8. Censura

**[APROBADA]** *(decisión 10)* Se mantiene como **[LIMITACIÓN]** permanente del experimento:

> Los procesos sin `closed_at` al final de la ventana observacional están **censurados** y **no deben etiquetarse arbitrariamente**.

La Fase 15 debe conservar esta limitación y **evaluar su impacto**, no solo declararla: reportar cuántos procesos se excluyeron, qué proporción representan y si sus features difieren sistemáticamente de las de los incluidos. **[HECHO]** La censura es estructural, no accidental: una vacante solo puede cerrarse tras registrar la decisión final y la selección humanas (`app/Services/Selection/VacancyClosureService.php:44-46`), y A-30 documenta que el cierre desierto no se implementa, de modo que un proceso atascado **nunca** produce `closed_at`.

Si la comparación revela una diferencia material, toda conclusión del experimento debe declararla como sesgo de selección.

## Enlaces

- [Definición del problema](problem-definition.md) · [Contrato de features](feature-contract.md) · [Dataset](dataset-specification.md) · [Model card](model-card-draft.md) · [Índice de la Fase 14](../phase-14-ml-definition.md)
