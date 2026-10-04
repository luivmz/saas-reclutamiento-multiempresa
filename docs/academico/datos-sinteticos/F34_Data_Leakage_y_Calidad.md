# F34 — Data leakage y calidad de datos

> Fase F34, versión 1.1 (04/10/2026), corregida tras la auditoría F34 (hallazgos M01, M02, M03 y LOW). Reglas automáticas de calidad y de leakage, implementadas en [`validate_f34.py`](../tools/f34/validate_f34.py) con solo biblioteca estándar. Pandera y Great Expectations no están instalados, y F34 no añade dependencias.

## 1. Reglas de calidad

| ID | Regla | Qué comprueba |
|---|---|---|
| DQ-01 | Cabeceras | Las columnas de cada CSV coinciden con `schema.json`, en el mismo orden |
| DQ-02 | Tipos | Enteros, fechas ISO (`YYYY-MM-DD`), instantes ISO (`YYYY-MM-DDTHH:MM:SS`) y booleanos `true`/`false` válidos |
| DQ-03 | Nulos | Ningún campo obligatorio vacío (p. ej., justificación: E-04 de F33) |
| DQ-04 | Restricciones | Enumeraciones, rangos (nivel 1–4, peso 1–100…) y patrones (tokens, prefijo `[SINTÉTICO]`) |
| DQ-05 | Claves | Clave primaria única por tabla |
| DQ-06 | Integridad referencial | Toda clave foránea existe en su tabla de referencia |
| DQ-07 | Linaje | `synthetic_record_id` único en todo el dataset; `source_type = synthetic` |
| DQ-08 | Duplicados | La misma fila de contenido con otra clave sustituta |
| CON-01 | Pesos | Suman 100 por vacante (A-06) |
| CON-02 | Fechas | Publicación < checkpoint ≤ plazo; postulación dentro de la ventana; sesión programada antes de su fecha; realizada en o después de su fecha |
| CON-03 | Rúbrica | El puntaje corresponde al nivel según la rúbrica publicada |
| CON-04 | FF-02 | Valoraciones solo en sesiones `realizada`; un resultado por sesión y criterio (sin segundo resultado); todos los criterios de la etapa; misma fecha y evaluador que la sesión |
| CON-05 | Evidencia | `vinculada` ⇒ valoración coherente; `borrador` ⇒ sesión `programada` y sin valoración |
| CON-06 | Suficiencia | Sin evidencia vinculada ⇒ `insuficiente` (valor imposible en caso contrario) |
| CON-07 | Anotaciones | Posteriores al resultado (son complementarias) |
| CON-08 | Eventos de análisis | Secuencia 1..n sin huecos ni repeticiones (no se sobrescribe el historial); empieza en `pendiente` y termina en un estado terminal |
| CON-09 | Estructura | Criterios de ambas etapas por vacante; 4 niveles por rúbrica |
| CON-10 | Versiones | Las valoraciones y criterios usan la versión congelada de la vacante (E-06) |
| CON-11 | Unicidad de postulación | Una postulación por persona y vacante (RF-10) |
| CON-12 | Ventana observacional | Ningún hecho registrado después de `observation_end` (`2026-09-30T23:59:59`); solo los plazos y fechas programadas pueden ser futuros |
| PII-01 | Columnas sensibles | Ningún nombre de columna con tokens de identidad o atributos sensibles |
| PII-02 | Patrones de PII | Ningún correo, URL, número con forma de DNI o teléfono en los valores |
| PII-03 | Grupo separado | `grupo_sintetico` solo en su archivo separado |
| AL-01 | Alertas | Las alertas esperadas coinciden con un recálculo **independiente** de las cuatro reglas deterministas |
| MF-01/02 | Manifiesto | Hash SHA-256 y filas de cada archivo; versiones, semilla, `observation_end`, semántica temporal, algoritmo de hash, exclusiones, `source = synthetic` y la advertencia |
| RP-01/02 | Reproducibilidad | Dos regeneraciones con la misma semilla son idénticas byte a byte; otra semilla produce otro dataset |

**Deriva sintética (informativa).** El validador informa el PSI entre train y test de tres variables, sin fallar. El efecto de periodo del generador la produce a propósito: sirve para que F36 practique su detección.

### 1.1 Integridad contextual (M03)

Una clave foránea válida no basta: la fila referida debe pertenecer a la **misma organización y vacante**. Estas reglas detectan cruces entre tenants y entre vacantes.

| ID | Qué comprueba |
|---|---|
| CTX-01 | La organización de la postulación es la de su vacante |
| CTX-02 | El requisito verificado pertenece a la vacante de la postulación |
| CTX-03 | La competencia del criterio es de la organización de la vacante; la rúbrica usa la versión de la vacante del criterio |
| CTX-04 | La sesión apunta a la vacante de su postulación; el evaluador es de la organización de la vacante |
| CTX-05 | El resultado tiene la postulación de su sesión y un criterio de la misma vacante y etapa |
| CTX-06 | La evidencia tiene la postulación y el autor de su sesión, y un criterio de la misma vacante |
| CTX-07 | La anotación complementaria la firma un evaluador de la organización de la vacante |
| CTX-08 | El evento de proceso tiene la organización de su vacante y su referencia (postulación o sesión) es de esa vacante |
| CTX-09 | Snapshots y ejecuciones de análisis tienen la organización y las versiones de su vacante |
| CTX-10 | Las alertas esperadas referencian postulaciones y criterios de su vacante; los grupos sintéticos, personas existentes |

## 2. Semántica temporal RF-29 (M02)

El snapshot reproduce **exactamente** el contrato congelado de RF-29 (`docs/v1.1/ml/feature-contract.md`, ADR-004 y `OperationalRiskFeatureBuilder`), sin modificarlo:

| Aspecto | Regla aplicada |
|---|---|
| Granularidad | Instantes con segundo, zona `America/Lima` sin desplazamiento (`YYYY-MM-DDTHH:MM:SS`); `closes_at` es una fecha |
| Checkpoint | Inicio del día siguiente a `closes_at` (`closes_at + 1 día, 00:00:00`), ADR-004 |
| Inclusión | Un hecho cuenta si su instante cumple **`t <= checkpoint_at`** (postulaciones, sesiones creadas y realizadas, cambios de etapa, último evento) |
| Vencidas | Sesión creada con `t <= checkpoint_at`, `scheduled_for < checkpoint_at` y sin completar a esa hora |
| Vacante abierta | Misma organización, otra vacante, `published_at <= checkpoint_at` y (`closed_at` nulo o `closed_at > checkpoint_at`) |
| Días completos | `floor(segundos / 86 400)`, como `wholeDays` de Laravel; la ventana cuenta desde el inicio del día de publicación |
| Cambios de etapa | Incluyen el historial inicial creado al registrar la postulación (`ApplicationService`) |
| Empates | Un hecho **exactamente** en el checkpoint cuenta; una sesión programada exactamente en el checkpoint **no** está vencida. El dataset contiene 100 eventos en el checkpoint, 38 sesiones programadas para ese instante y 11 publicaciones a las 00:00, para que cualquier cambio de `<=` a `<` (o al revés) sea detectable |

`validate_f34.py` recalcula las 15 variables con una implementación independiente (`recompute`) y exige **0 diferencias** (LK-02). LK-11 recalcula además con `<` y comprueba que el resultado difiere y que existen empates en los tres límites: si alguien volviera a `< checkpoint`, LK-02 fallaría (caso QA-26). Además se mutó el propio generador (`<` en la inclusión, `published_at < at` y `closed_at >= at` en vacantes abiertas, `scheduled_for <= at` en vencidas): LK-02 detectó las cuatro mutaciones, y LK-10 detectó el generador sin purga.

## 3. Madurez de las etiquetas (M01)

La etiqueta `delayed` se conoce cuando la vacante cierra: **`label_known_at = closed_at`** (equivale a `target_available_at` / `outcome_known_at`). Una fila de una partición no puede depender de hechos posteriores al inicio de la siguiente. Se resolvió con **purga** (opción A):

1. Las vacantes con cierre observado se ordenan por checkpoint y se asignan 50 % train, 30 % validation y 20 % test.
2. Con `inicio(validation)` y `inicio(test)` como el primer checkpoint de cada partición, una fila de train con `label_known_at >= inicio(validation)` o una de validation con `label_known_at >= inicio(test)` se **purga** (`split = purgado`, motivo `etiqueta_no_madura_antes_de_validation` o `..._test`). No se reasigna a otra partición.
3. Las vacantes sin cierre observado al final de la ventana (`observation_end`) quedan **censuradas** (`observation_status = censored`, `delayed` vacío, `split = censurado`): no se etiquetan ni se usan, como en RF-29.

LK-10 comprueba que `label_known_at` coincide con el cierre observado, que ninguna etiqueta de train o validation madura después del inicio de la siguiente partición, que no hay sobrepurga y que ninguna partición queda vacía. `label_known_at` vive solo en `process_splits`: **nunca** es una feature (LK-08).

## 4. Hash canónico de entrada (LOW)

`analysis_runs.input_snapshot_hash` usa el algoritmo **`f34-input-sha256-v1`** (también en la columna `input_hash_algorithm` y en el manifiesto):

- SHA-256 de un JSON canónico: claves ordenadas, separadores `,` y `:` sin espacios, UTF-8 sin escapar.
- Contenido: algoritmo, vacante, `criteria_version`, `rubric_version`, `rules_version`, y por cada valoración (`assessment_id`, sesión, criterio, `human_level`, `rubric_points`, `evidence_sufficiency`, justificación) y cada evidencia vinculada (`evidence_id`, valoración, criterio, tipo, referencia, texto), ordenadas por ID.
- Determinista y sin tokens de persona ni de evaluador; todo el contenido es sintético.
- Cambiar el contenido canónico exige una versión nueva del algoritmo (`f34-input-sha256-v2`), nunca reutilizar el nombre.

LN-01 recalcula el hash de forma independiente: un texto o una justificación modificados después del análisis se detectan (QA-41, QA-42).

## 5. Particiones

- **Proceso (`process_snapshots`):** partición **temporal agrupada por vacante**, ordenada por checkpoint, con purga por madurez de la etiqueta (§3). De 120 vacantes: 47 train, 16 validation, 23 test, 29 purgadas y 5 censuradas. Cada partición contiene ambas clases. Una vacante pertenece a una sola partición, y un split aleatorio se descartó porque mezclaría periodos (leakage temporal). La semilla fija el orden de generación; el orden de la partición lo fija el checkpoint, no el azar.
- **Evidencia y valoraciones humanas:** **sin partición.** No hay ningún modelo autorizado sobre estos datos (F33). Si algún día se aprobara un uso experimental del proceso sobre ellos, la partición debería agruparse por vacante **y** por persona, para que la misma persona sintética no aparezca en dos conjuntos.

## 6. Matriz de leakage

| RIESGO | EJEMPLO | CONTROL | VALIDADOR |
|---|---|---|---|
| **Target leakage** | `closed_at` o la duración total en la tabla de features revela `delayed` | Contrato RF-29: columnas prohibidas por nombre y por token; `closed_at` solo existe en los eventos y como `label_known_at` en las particiones | LK-01 (usa `is_forbidden_column` del contrato RF-29, sin modificarlo), LK-08 |
| **Leakage temporal** | Contar sesiones realizadas después del checkpoint | Solo hechos con `t <= checkpoint_at`; checkpoint = inicio del día siguiente a `closes_at` (ADR-004) | LK-02 (recálculo independiente de las 15 variables), LK-03, LK-11 |
| **Madurez de la etiqueta** | Etiqueta de train conocida después del inicio de validation | Purga por `label_known_at`; censura sin cierre observado | LK-10, LK-04, LK-06 |
| **Variables posteriores a la decisión** | Selección, decisión RF-23 o posición en el ranking como feature | No existen en el contrato; datos humanos fuera de la tabla de proceso | LK-01, LK-08 |
| **Features auxiliares** | `evidence_sufficiency`, `evaluator_disagreement` o sus agregados como feature | Solo QA, análisis del proceso e ICC; excluidas en el manifiesto | LK-08 |
| **Etiqueta incoherente** | `delayed` que no coincide con el cierre observado, o censurada con etiqueta | Recalcular la etiqueta y el estado de observación desde los eventos | LK-04 |
| **Cruce de contexto** | Postulación de ORG-S1 marcada como ORG-S2; requisito de otra vacante | Integridad contextual | CTX-01 a CTX-10 |
| **Proxies** | Años de experiencia crudos (edad); grupo sintético como feature | FT-02 solo como umbral; grupo en archivo separado | LK-07, PII-01, PII-03 |
| **Factores latentes** | Exportar el factor interno del generador | Solo en memoria | LK-09 |
| **Duplicados** | La misma evidencia o el mismo evento con otro ID | Fuentes únicas por sesión y criterio; eventos de cambio de etapa con destino | DQ-08, CON-04, CON-11 |
| **Contaminación entre particiones** | La misma vacante en train y test; test anterior a train | Partición temporal agrupada por vacante | LK-06 |
| **Feature set desalineado** | El manifiesto lista otras features que el contrato | Lista única en el generador, el schema y el manifiesto | LK-05 |
| **Entrada de análisis alterada** | Evidencia modificada después del análisis | Hash canónico del contenido | LN-01 |

## 7. Casos intencionales (inconsistencias de prueba)

El dataset versionado está **limpio**. Las inconsistencias viven en [`qa_casos/qa_cases.json`](dataset/qa_casos/qa_cases.json): 45 casos que el validador aplica en memoria sobre una copia, y cada uno debe ser detectado por su regla.

- **QA-01 a QA-20 (versión 1):** nivel 5; segundo resultado como corrección; puntaje que no corresponde a la rúbrica; evidencia huérfana; correo y DNI en textos; `closed_at` en las features; vacante en dos particiones; pesos que no suman 100; valoración sobre una sesión programada; suficiencia imposible; grupo sintético en las features; justificación vacía; anotación anterior al resultado; feature con información futura; columna `gender`; sesión realizada antes de lo programado; eventos de análisis sobrescritos; oráculo de alertas incompleto; nivel humano como feature.
- **QA-21 a QA-25 (M01):** fila purgada devuelta a train y a validation; `label_known_at` falseado; vacante censurada con etiqueta; vacante censurada movida a test.
- **QA-26 y QA-27 (M02):** features recalculadas con `< checkpoint`; checkpoint desplazado a las 23:59:59 de `closes_at`.
- **QA-28 a QA-40 (M03):** APP-00001 cambiada de ORG-S1 a ORG-S2; requisito de otra vacante; competencia de otra organización; evaluador de otra organización; sesión de otra vacante; resultado con criterio de otra vacante; evidencia de otra postulación; anotación firmada por otra organización; evento con otra organización y con referencia de otra vacante; análisis y snapshot con otra organización; alerta con postulación de otra vacante.
- **QA-41 a QA-45 (LOW):** evidencia y justificación modificadas sin recalcular el hash; `evidence_sufficiency` y `evaluator_disagreement` como features; evento posterior a la ventana observacional.

## 8. Casos borde incluidos en el dataset limpio

- VAC-0007, una vacante sin postulaciones.
- Personas sintéticas que postulan a dos vacantes distintas.
- Valoraciones sin evidencia (alerta de evidencia faltante).
- Discrepancias de dos o más niveles entre evaluadores.
- Sesiones programadas y vencidas.
- Requisitos declarados vacíos.
- Ejecuciones de análisis fallidas seguidas de un reintento.
- Hechos exactamente en el checkpoint (empates) y vacantes publicadas a las 00:00.
- Vacantes censuradas y vacantes purgadas por madurez de la etiqueta.
- Ceros estructurales de entrevistas programadas en el checkpoint.
