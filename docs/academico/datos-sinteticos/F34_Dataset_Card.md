# F34 — Dataset Card: `f34-synth-1.1.0`

> **Este dataset es 100 % sintético. NO representa datos reales del Colegio Andino** ni de ninguna institución o persona. Sus distribuciones son decisiones del generador, no mediciones.

## 1. Propósito

Probar **estructuras, contratos, reglas de calidad y controles de leakage** del futuro módulo inteligente diseñado en F33 (alcance B: evidencia, rúbricas y valoración humana; y alcance E: ML del proceso). Sirve para verificar que los datos cumplen el contrato, no para estimar ni predecir nada sobre personas.

## 2. Alcance

- **Incluye** contexto de vacante, competencias, criterios, rúbricas, requisitos, postulaciones con tokens, sesiones, valoraciones humanas, evidencia, anotaciones complementarias, eventos y snapshots del proceso, ejecuciones de análisis y alertas esperadas.
- **No incluye** CV ni documentos, texto extraído automáticamente, audio o vídeo, embeddings, atributos sensibles reales, decisiones de selección ni scores sobre personas.

## 3. Origen

Generado por [`generate_synthetic.py`](../tools/f34/generate_synthetic.py) con `random.Random` (Mersenne Twister) y semilla fija. **No se deriva de ninguna persona, documento o registro real**: los tokens son secuencias inventadas y los textos libres son plantillas marcadas con `[SINTÉTICO]`.

## 4. Proceso de generación

1. Tres organizaciones sintéticas, cuatro evaluadores con token por organización y un catálogo de 8 competencias genéricas por organización.
2. 120 vacantes con instantes en 2026 (granularidad de segundo, `America/Lima`), de 4 a 6 criterios con pesos enteros que suman 100 y una rúbrica de 4 niveles por criterio.
3. Postulaciones con instante dentro de la ventana de cada vacante. VAC-0007 no tiene ninguna (caso borde). Algunas personas sintéticas postulan a dos vacantes distintas.
4. Sesiones de evaluación y de entrevista, con doble calificación en parte de las evaluaciones (para el ICC).
5. Valoraciones solo en sesiones `realizada`, con el puntaje que corresponde al nivel. Las sesiones `programada` solo tienen borradores de evidencia.
6. Eventos del proceso y cierre simulado. El cierre solo se registra si ocurre antes de `observation_end` (`2026-09-30T23:59:59`); si no, la vacante queda **censurada**. Snapshot de las 15 variables RF-29 con la semántica exacta del contrato: hechos con `t <= checkpoint_at`, incluidos empates deliberados en el checkpoint.
7. Partición temporal con purga por madurez de la etiqueta (`label_known_at`), ejecuciones de análisis con hash canónico de entrada y eventos, y alertas esperadas.
8. Manifiesto con versiones, semilla, hashes SHA-256 y número de filas.

Un factor latente por postulación da coherencia a las valoraciones simuladas. Solo existe en memoria, **no se exporta** (regla LK-09) y no representa la idoneidad real de nadie.

## 5. Variables

El detalle completo está en [`schema.json`](../tools/f34/schema.json): 19 tablas y 179 campos, con tipo, restricciones y rol. La clasificación de variables y etiquetas está en la [matriz de features y labels](F34_Matriz_Features_Labels.md).

## 6. Distribución

| Tabla | Filas | Tabla | Filas |
|---|---|---|---|
| organizations | 3 | sessions | 1651 |
| competencies | 24 | assessments | 3551 |
| vacancies | 120 | evidence | 6309 |
| criteria | 568 | annotations | 166 |
| rubric_levels | 2272 | process_events | 6844 |
| requirements | 253 | process_snapshots | 120 |
| applications | 940 | process_splits | 120 |
| requirement_checks | 2004 | analysis_runs / analysis_run_events | 123 / 369 |
| expected_alerts | 1105 | fairness_sintetico (separado) | 862 |

**Total: 27 404 filas.**

Rasgos principales:

- **Vacantes:** 83 docentes y 37 administrativas.
- **Postulaciones:** 856 activas y 84 descartadas; 67 personas sintéticas postulan a dos vacantes.
- **Sesiones:** 889 evaluaciones y 578 entrevistas realizadas; 91 evaluaciones y 93 entrevistas programadas.
- **Niveles humanos:** aproximadamente uniformes (858 / 894 / 849 / 950 para los niveles 1 a 4).
- **Suficiencia de la evidencia:** 2019 suficiente, 1240 parcial y 292 insuficiente.
- **Doble calificación:** 261 pares de evaluadores.
- **Etiqueta del proceso `delayed`:** 40 vacantes con 1 y 75 con 0; 5 censuradas sin etiqueta.
- **Partición:** 47 train (11 con 1), 16 validation (6 con 1), 23 test (7 con 1), 29 purgadas y 5 censuradas.
- **Alertas esperadas:**
  - 622 requisitos no evidenciados;
  - 292 casos de evidencia faltante;
  - 171 sesiones vencidas;
  - 20 discrepancias entre evaluadores.
- **Datos faltantes controlados:**
  - `years_experience_declared`, 9,4 % vacío;
  - `declared_met`, 5,8 % vacío.
- **Empates en el checkpoint:** 100 eventos exactamente en el checkpoint (52 sesiones creadas y 48 cambios de etapa), 38 sesiones programadas para el instante del checkpoint y 11 vacantes publicadas a las 00:00.

## 7. Limitaciones

- **Sin validez externa.** Las distribuciones son arbitrarias. Ningún resultado obtenido con este dataset dice algo sobre el Colegio Andino ni sobre candidatos reales.
- **Ceros estructurales.** Las entrevistas se programan desde el checkpoint, por eso `interviews_scheduled_count`, `interviews_completed_count` y `interviews_overdue_pending_count` valen 0 en el checkpoint.
- **Tamaño pequeño.** 120 vacantes (86 etiquetadas tras la purga) bastan para probar estructuras, no para entrenar ni evaluar modelos con rigor estadístico.
- **Textos de plantilla.** Los textos libres no sirven para probar NLP, que de todos modos está fuera del alcance B.

## 8. Sesgos simulados

- **Efecto de periodo.** Las vacantes publicadas más tarde tienen más demora: produce deriva deliberada entre particiones, medida con PSI en el validador.
- **Grupo sintético.** `grupo_sintetico` se asigna al azar, sin relación con ninguna variable. Sirve para probar que un pipeline de equidad separa y agrega correctamente; no simula discriminación real.
- **Ningún sesgo** reproduce patrones históricos de contratación, porque no se usan etiquetas de contratación.

## 9. Usos permitidos

- Probar el contrato de datos, los validadores y las reglas deterministas de F33 (alertas, ICC, completitud).
- Probar pipelines de **proceso** (alcance E), con datos sintéticos y en el marco de G0.
- Probar que un pipeline de equidad mantiene separado el atributo de grupo.
- Docencia y documentación académica.

## 10. Usos prohibidos

- Entrenar o evaluar modelos que puntúen, ordenen, recomienden, filtren o descarten **personas**.
- Presentarlo como evidencia de eficacia, validez predictiva o equidad del sistema.
- Usar `human_level`, `rubric_points` o `delayed` como etiqueta de idoneidad personal.
- Usar `evidence_sufficiency`, `evaluator_disagreement` o sus agregados como features de ML: solo sirven para QA, análisis del proceso e ICC.
- Usar las vacantes purgadas o censuradas como filas etiquetadas.
- Mezclarlo con datos reales o completarlo con información de personas reales.
- Usar `grupo_sintetico` como feature o para cualquier decisión.

## 11. Privacidad

No contiene PII ni datos personales: los validadores PII-01 a PII-03 lo comprueban (columnas, patrones de correo, DNI, teléfono y URL, y atributos separados). El consentimiento no autoriza datos reales en F34; la gobernanza completa está en [F34_Gobernanza_Privacidad.md](F34_Gobernanza_Privacidad.md).

## 12. Riesgos

| Riesgo | Mitigación |
|---|---|
| Tomar el dataset como representativo | Advertencia en el card, en el manifiesto y en el README |
| Reutilizarlo para scoring de personas | Usos prohibidos; el contrato no tiene campos de score sobre personas |
| Leakage al pasar a F36 | Reglas LK-01 a LK-11, purga por madurez de la etiqueta y partición temporal agrupada |
| Que se le añadan datos reales | Regla de datos de F33/F34 y validador PII |
| Cruces entre organizaciones o vacantes | Reglas CTX-01 a CTX-10 |

## 13. Versionado

| Elemento | Valor |
|---|---|
| `dataset_version` | `f34-synth-1.1.0` |
| `generator_version` | `f34-gen-1.1.0` |
| `schema_version` | `f34-schema-1.1.0` |
| `feature_set_version` | `f34-fs-1.0.0` |
| `rules_version` | `f33-rules-design-0` |
| `generated_at` | `2026-10-04T00:00:00-05:00` (fecha lógica fija) |
| `seed` | `20261004` |
| `observation_end` | `2026-09-30T23:59:59` |
| `input_hash_algorithm` | `f34-input-sha256-v1` |

Las versiones de rúbrica y criterios por vacante (`RV-VAC-xxxx-1`, `CV-VAC-xxxx-1`) están en el [manifiesto](dataset/manifest.json). Cualquier cambio del generador o del contrato sube la versión correspondiente. La versión 1.1.0 corrige los hallazgos de la auditoría F34 (madurez de etiquetas, semántica RF-29, integridad contextual y hash canónico); la 1.0.0 queda reemplazada.

## 14. Reproducibilidad

`python docs/academico/tools/f34/generate_synthetic.py` produce exactamente los mismos archivos con la misma semilla. El validador lo comprueba en cada ejecución:

- genera dos veces en carpetas temporales y compara los SHA-256 con el manifiesto;
- verifica que otra semilla produce otro dataset.

Se probó con Python 3.12 y solo biblioteca estándar.

## 15. Mantenimiento

- **Responsable:** el equipo del proyecto.
- **Cuándo regenerar:** solo al cambiar el contrato o el generador, siempre con una versión nueva y el validador F34 en verde.
- **Revisión:** este card se revisa en cada fase que consuma el dataset (F35/F36) y antes de cualquier reutilización académica.
