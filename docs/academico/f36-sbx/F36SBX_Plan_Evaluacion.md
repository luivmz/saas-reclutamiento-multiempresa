# F36-SBX — Plan de evaluación

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. **No hay resultados:** F36-SBX no ejecuta ningún método. Este plan fija qué se mediría en F37-SBX, contra qué oráculo y con qué umbral, todo declarado **antes** de medir.

## 1. Reglas generales

1. **Preregistro.** Antes de ejecutar nada en F37-SBX se registran en el repositorio la métrica, el oráculo, el umbral de aceptación y el manifiesto sellado de `test`. Si se cambia algo después, la evaluación se invalida (TEI-08).
2. **Lo que se mide es el método,** contra un oráculo sintético. Nunca a una persona. Ninguna métrica se presenta como validez predictiva sobre candidatos.
3. **Comparación obligatoria con la línea base** más simple de la escalera (reglas → BM25 → semántico; [informe §4](F36SBX_Investigacion_Diseno.md#4-comparación-de-enfoques)).
4. **Intervalos de confianza** (bootstrap por vacante, unidad de partición) para toda métrica de proporción.
5. **Desglose por estrato** de solapamiento léxico (`alto`, `medio`, `nulo`) en toda métrica de recuperación.
6. **Sin resultados inventados.** Todo número publicado sale de una ejecución reproducible con su manifiesto.

## 2. Métricas por capacidad

| ID | Capacidad | Métrica | Oráculo | Umbral de aceptación propuesto |
|---|---|---|---|---|
| M-01 | EI-01, EI-06 | Exactitud de la organización por metadatos (coincidencia exacta) | Metadatos declarados | 100 %: es determinista. Cualquier diferencia es un defecto |
| M-02 | EI-02 | Precisión y exhaustividad de las alertas | `expected_alerts` de F34 | 100 % sobre el oráculo, con casos negativos de QA |
| M-03 | EI-03 | Tasa de enlaces íntegros (la cita existe, la fuente y la versión coinciden) | Enlaces sintéticos con fallos sembrados | Detecta el 100 % de los fallos sembrados, sin falsos positivos |
| M-04 | EI-04 | Invariancia del orden: el desglose no cambia al permutar los valores de las postulaciones | Permutaciones | Orden idéntico en todas las permutaciones |
| M-05 | EI-05 | Exhaustividad de la guardia de PII | PII ficticia sembrada y evidente | 100 % de los casos sembrados rechazados |
| M-06 | EI-07 | Coincidencia exacta de la búsqueda | Consultas con respuesta conocida | 100 % |
| M-07 | EI-09, EI-10 | Recall@k, Precision@k, MRR y nDCG@k por estrato | `relevance_annotation`, con acuerdo medido | Se fija en el preregistro. EI-10 solo se acepta si supera a BM25 en el estrato `medio` o en el `nulo` por un margen declarado |
| M-08 | EI-09, EI-10 | Calidad de la abstención: cobertura frente a riesgo y tasa de abstención correcta en casos sin evidencia | Casos sin evidencia relevante | Abstención correcta en todos los casos sin evidencia del conjunto sellado, o el umbral declarado |
| M-09 | EI-08, EI-12 | Precisión, exhaustividad y F1 por campo o entidad; coincidencia exacta | Campos y entidades anotados | Se fija en el preregistro. Toda entidad de persona detectada es un defecto bloqueante |
| M-10 | EI-11 | Fidelidad de extracción: distancia de edición normalizada entre el texto extraído y el `cv_document` de origen | `rendered_from` | Se fija en el preregistro, por formato |
| M-11 | Toda salida | Atribución de evidencia: proporción de salidas cuyo texto coincide byte a byte con la fuente en sus offsets | Fuente canónica | 100 %. Cualquier fallo es un defecto (TEI-09 y TEI-10) |
| M-12 | Toda salida | Fidelidad: ausencia de texto generado | Esquema de salida | 0 campos de texto libre producidos por el método |
| M-13 | EI-24 | Diferencia de Recall@k entre variantes contrafactuales, y tasa de pares con salida distinta | `counterfactual_pair` | Se fija en el preregistro. No se generaliza a personas |

## 3. Robustez, recursos y reproducibilidad

| ID | Métrica | Cómo |
|---|---|---|
| R-01 | Robustez adversarial: cambio de M-07 y M-08 ante los `adversarial_case` | Por tipo de ataque, frente al mismo caso sin ataque |
| R-02 | Latencia por consulta (mediana y p95) | En la PC declarada, en CPU, con hilos fijos |
| R-03 | Pico de memoria por ejecución | Medido por proceso, con el límite de WSL2 declarado |
| R-04 | Reproducibilidad | Dos ejecuciones con hash de salida idéntico |
| R-05 | Inyección (TEI-03) | El formato y la ruta de salida no cambian ante ninguna instrucción incrustada |

## 4. Equidad

Solo con EI-24 y solo con marcadores sintéticos contrafactuales. Se justifica porque [S11] documenta sesgos por nombre y género en la recuperación con embeddings. No se calculan métricas de equidad sobre personas ni con atributos reales (CAP-32), y un resultado sintético no permite afirmar que el método sea justo con personas reales.

## 5. Qué no se mide

- Ninguna métrica de «calidad del candidato», idoneidad o probabilidad de contratación.
- Ninguna correlación entre las salidas y RF-21, RF-23 o RF-29.
- Ningún resultado de LLM, OCR o audio, que están BLOCKED.

## 6. Resultados

**No hay resultados.** F36-SBX no ejecutó ningún método ni generó ningún corpus.
