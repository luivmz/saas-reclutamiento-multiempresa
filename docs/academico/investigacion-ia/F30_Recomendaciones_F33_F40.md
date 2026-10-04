# F30 — Recomendaciones y decisiones para F33–F40

> Fase F30, versión 1 (30/09/2026), auditada e integrada. F30 investiga y propone; F33–F40 implementarán después, si el equipo lo autoriza. Las decisiones de este documento son **propuestas de ingeniería** respaldadas por la [matriz de evidencia](F30_Matriz_Evidencia_Cientifica.md). Ninguna está aprobada hasta que el equipo la registre.

## 1. Conclusión

La evidencia reunida respalda un motor que **estructura, documenta y verifica la evidencia** con la que los evaluadores humanos califican:

- rúbricas BARS y entrevista estructurada [S13, S14, S15, S19];
- procedencia de cada nivel asignado;
- acuerdo entre evaluadores [S20, S21];
- explicaciones verificables [S55, S59].

**No** respalda scoring, sugerencia de niveles ni recomendación de candidatos **para este caso, con los datos, el gobierno y las garantías actuales**:

- seguimiento acrítico de IA sesgada [S84];
- bajo rendimiento de los equipos humano-IA en decisiones [S60];
- explicaciones que aumentan la aceptación ciega [S58];
- sesgos de embeddings y LLM [S11, S83, S87];
- datos pequeños [S04] y validez predictiva baja en docentes [S22].

La evidencia a favor de la calificación automática [S89] se mantiene como **evidencia en tensión**: muestra implementaciones a escala, en organizaciones con grandes volúmenes de calificaciones humanas que el caso no tiene. No se descarta para el futuro; se descarta para este caso en las condiciones actuales.

**Regla central de todo el diseño:** RECOMENDACIÓN DEL SISTEMA ≠ DECISIÓN FINAL DE CONTRATACIÓN. En este motor, una «recomendación del sistema» se refiere al **proceso** y a la **evidencia**, por ejemplo «falta evidencia para el criterio X» o «los evaluadores discrepan en Y». Nunca se refiere a la persona. La decisión final es del Aprobador / Dirección, con confirmación explícita y justificación (RF-23, ADR-002).

## 2. Puerta G0

**Regla G0.** F33 formula y aprueba ADR-005, que constituye la puerta G0. F34 puede avanzar en paralelo **solo con datos sintéticos** y sin scoring ni recomendación de personas. F35–F40 **no comienzan sin G0 aprobado**.

G0 queda aprobada cuando se cumplen todas estas condiciones:

| Condición G0 | Evidencia de cumplimiento | Motivo |
|---|---|---|
| G0-1 Nuevo ADR (ADR-005) que defina qué puede hacer el motor y que **ratifique o enmiende** ADR-001 de forma explícita | ADR aprobado por el equipo | La visión de «recomendar» choca con ADR-001, el contrato 4 y OUT-04/05/11 ([gobernanza §4.2](F30_Explainability_Fairness_Gobernanza.md#42-conflicto-de-gobierno-con-el-proyecto-actual-hallazgo-crítico)) |
| G0-2 Revisión del contrato 4 de CLAUDE.md, solo si el ADR lo enmienda | Cambio registrado y autorizado | El contrato prohíbe que el ML evalúe personas |
| G0-3 Evaluación de impacto previa (riesgo alto) | Documento con revisión jurídica y contraste de los artículos citados con la publicación oficial | DS 115-2025-PCM, arts. 24.1 e) (corroborado) y 30 [O13] |
| G0-4 Análisis de datos personales | Base legal, finalidad, minimización y retención documentadas | Ley 29733 [O15] y DS 016-2024-JUS [O09] |
| G0-5 Requisitos nuevos como **candidatos** (desde RF-32), sin tocar RF-01 a RF-27 | Entradas en `docs/v1.1/scope-preliminary.md` o su sucesor | Contrato 1; la decisión 11 no promueve por implementar |
| G0-6 Autorización explícita de dependencias nuevas | Lista aprobada con versión, licencia y auditoría OSV | Skill `project-guardian`; [herramientas](F30_Analisis_Herramientas_Skills.md) |

## 3. Tabla de decisiones

| ID | DECISIÓN | EVIDENCIA | ALTERNATIVAS | RIESGO | RECOMENDACIÓN | FASE |
|---|---|---|---|---|---|---|
| D-01 | Puerta de gobierno G0 antes de implementar | [O13, O09, S84, S60]; ADR-001 | Implementar y regularizar después | Incumplimiento normativo; contradicción con contratos vigentes | **Adoptar la regla G0**: F33 aprueba ADR-005; F34 solo con datos sintéticos; F35–F40 no comienzan sin G0 aprobado | F33 |
| D-02 | Alcance del motor: asistencia sobre proceso y evidencia, sin puntuar ni recomendar personas | [S58, S60, S84, S11, S83, S87, S22]; tensión con [S89] | Sugerir nivel por criterio; recomendar candidato | Anclaje y discriminación; incumplir ADR-001 | **Solo proceso y evidencia**. Sugerir niveles queda fuera hasta que haya validación local con datos suficientes (hoy no existen) | F33 |
| D-03 | Criterios desde el análisis del puesto, con competencias versionadas | [S17, S18, S24, O14] | Criterios libres por vacante (hoy) | Criterios irrelevantes o sesgados | **Catálogo de competencias** con `criteria_version`; para docentes, derivado del MBDD y validado por el colegio | F33 |
| D-04 | Entrevista estructurada con rúbricas BARS | [S13, S14, S15, S16, S19] | Entrevista libre; puntaje sin anclas | Baja fiabilidad y validez | **Adoptar**: mismas preguntas por vacante, BARS por criterio, `rubric_version` | F33 |
| D-05 | Cadena de procedencia: pregunta → respuesta → evidencia → criterio → nivel → justificación → confianza | [S55, S70, S71, S73] | Puntaje sin evidencia (hoy) | Decisiones no explicables ni auditables | **Adoptar** como modelo de datos del motor | F33, F38 |
| D-06 | Verificaciones del proceso con reglas deterministas | [S51, S62] | ML para detectar inconsistencias | Opacidad innecesaria | **Reglas**: evidencia faltante, nivel sin justificación, discrepancia entre evaluadores, pregunta omitida, rúbrica cambiada | F35 |
| D-07 | Acuerdo entre evaluadores con ICC | [S20, S21] | Un solo evaluador | Calificación no fiable | **Doble calificación** en los criterios de mayor peso; ICC con forma e intervalo | F35, F39 |
| D-08 | Mantener el ranking RF-21 (suma ponderada) | [S39, S40, S51]; A-24, A-26 | TOPSIS u otro MCDM; ranking por ML | Opacidad; pérdida de trazabilidad | **Mantener** la suma ponderada; AHP opcional solo para justificar pesos; desglose por criterio en F40 | F33, F40 |
| D-09 | Dataset sintético primero, con linaje y dataset card | [S72, S74, S79, S33] | Datos reales anonimizados | PII; fuga de información | **Sintético** con semilla, SHA-256, card y particiones por convocatoria | F34 |
| D-10 | No recolectar atributos sensibles | [O09, S44, S46]; contrato 7 | Recolectar para auditar equidad | Riesgo legal; muestras pequeñas sin poder estadístico | **No recolectar**; simular atributos en datos sintéticos si F37 prueba métodos | F34, F37 |
| D-11 | Etiquetas: nunca usar «contratado» como idoneidad | [S42, S48, S01] | Aprender de decisiones históricas | Sesgo por etiqueta *proxy* | **Prohibido** en la dataset card y en las pruebas | F34, F36 |
| D-12 | Pipeline de evidencia: CV digital con extracción de texto; sin OCR por defecto | [S37] | Docling, Tika u OCR | Complejidad y dependencias | **pypdf/pdfplumber/python-docx en sandbox**; OCR solo si aparecen escaneados | F35 |
| D-13 | Localizar fragmentos de evidencia con similitud semántica | [S31, S11] | No usar NLP; puntuar por similitud | Sesgo por nombre y género si se usa como puntaje | **Evaluar en sandbox** solo como localizador, mostrado después de la calificación humana, sin nombre en la entrada | F35 |
| D-14 | Audio: por defecto, no grabar | [S13, S15, S06] | Grabar y transcribir siempre | Datos personales; errores de STT | **No grabar**; solo si F33 demuestra necesidad y pasa G0 | F33 |
| D-15 | Si se graba: solo audio, STT local, revisión humana, sin biometría | [S38, S81, S10, S88, S85, O13] | Vídeo; STT en la nube; diarización por voz | Alucinaciones, sesgo por variedad de habla, biometría | **Whisper local en sandbox**, revisión contra el audio, WER por grupo, segmentación manual | F35 |
| D-16 | Prohibir la inferencia de emociones, personalidad, prosodia y rasgos faciales | [S07, S08, S09, S85, O01, O13] | Análisis multimodal | Evidencia insuficiente, mixta y no generalizable para este uso; riesgo alto o prohibición | **Prohibido** en ADR-005 y en pruebas de regresión | F33 |
| D-17 | LLM fuera de toda evaluación de personas | [S34, S36, S83, S87] | LLM como juez o resumidor | Alucinación y sesgo | **Prohibido** para evaluar; Ollama en sandbox solo para tareas sin personas | F33 |
| D-18 | ML solo sobre el proceso (como RF-29) | [S51, S04]; ADR-001, ADR-004 | Modelo de idoneidad | Contradice contratos y evidencia | Si F36 necesita un modelo, **interpretable** (regresión logística o EBM) y sobre el proceso | F36 |
| D-19 | Calibración y métricas apropiadas si hay probabilidades | [S64, S66, S67, S68] | Exactitud y ROC | Confianza engañosa | PR-AUC, Brier y curva de calibración; sin «confianza» sin calibrar | F36, F39 |
| D-20 | Explicaciones contrastivas y verificables para humanos; SHAP solo interno | [S51, S52, S55, S56, S58, S59] | SHAP o LIME para usuarios | Aceptación acrítica | **Justificación BARS contrastiva** con enlace a la evidencia | F37, F40 |
| D-21 | Equidad del procedimiento primero; revisión estadística agregada con base legal | [S44, S45, S46, O11, S14, S19] | Una métrica de equidad por vacante | Conclusiones espurias con n pequeño | **Controles de procedimiento** + revisión agregada cuando sea legal y estadísticamente posible | F37, F39 |
| D-22 | Diseño contra el sesgo de automatización | [S84, S60, S63, S57, S61] | Mostrar la sugerencia junto a la calificación | Anclaje | El evaluador **califica antes** de ver ayudas; se registra `suggestion_seen_before_scoring` y el desacuerdo | F38, F40 |
| D-23 | Integración Laravel ↔ ML asíncrona, idempotente y con *fallback* | [S76, S77, S78]; patrón de RF-29 | Llamada síncrona en la página | Caídas; duplicados | Cola Redis, `Idempotency-Key`, timeouts, reintentos, circuit breaker | F38 |
| D-24 | Versionado de cada ejecución | [S71, S72, S79] | Solo la versión del modelo | Resultados no reproducibles | `model_version`, `rubric_version`, `criteria_version`, `input_snapshot_hash` | F38 |
| D-25 | Auditoría sin PII ni entradas completas | [O09, S73]; contrato 6 | Guardar la entrada completa | Exposición de datos | Registro de `analysis_run` sin texto de entrada, con hash; `AuditLogger` de solo inserción | F38 |
| D-26 | Multiempresa en todo el motor | Contrato 5 | Modelos compartidos entre organizaciones | Filtración entre organizaciones | `organization_id` permanece en Laravel (datos, Policies, auditoría); no se envía al servicio ML *stateless* salvo justificación explícita: viajan identificadores técnicos pseudónimos mínimos; ningún modelo mezcla organizaciones; pruebas cross-tenant | F38 |
| D-27 | Evaluación con métricas por tarea, no por persona | [S20, S10, S29, S68, S69] | Una exactitud global | Métricas sin verdad de terreno | Tabla de métricas de [modelos §6](F30_Analisis_Modelos_y_Tecnicas.md#6-métricas-por-tarea); NDCG solo con relevancia válida | F39 |
| D-28 | Auditoría interna antes de cualquier piloto | [S73, S76] | Piloto directo | Daños no detectados | **Auditoría interna** con model card, dataset card y las 28 pruebas como lista | F39 |
| D-29 | Panel: desglose del ranking, evidencia y alertas de proceso; sin «recomendado» | [S62, S55]; RF-22, RF-23 | Insignia de «mejor candidato» | Anclaje | El panel muestra **criterios, evidencia, acuerdo y faltantes**; la decisión sigue en RF-23 | F40 |
| D-30 | Herramientas: adopción controlada | [Herramientas](F30_Analisis_Herramientas_Skills.md) | Instalar a demanda | Cadena de suministro y licencias | Solo RECOMENDADO o EVALUAR EN SANDBOX tras G0-6; EVITAR PyMuPDF, LIME, pyannote.audio y Zotero MCP | F33–F40 |

## 4. Plan por fase

| Fase | Objetivo | Entrada | Salida mínima | Decisiones |
|---|---|---|---|---|
| **F33 Diseño funcional** | Definir qué hace y qué no hace el motor; formular y aprobar G0 | F30 auditada | ADR-005 aprobado (G0); requisitos candidatos (RF-32+); modelo de competencias, rúbricas y cadena de procedencia; casos de uso TO-BE; evaluación de impacto iniciada | D-01–D-05, D-08, D-14, D-16, D-17 |
| **F34 Dataset y gobernanza** | Datos sintéticos gobernados | F30 auditada; en paralelo a F33, solo con datos sintéticos y sin scoring ni recomendación de personas | Generador con semilla; dataset card; linaje SHA-256; particiones; registro; regla «sin atributos sensibles» | D-09–D-11 |
| **F35 Pipeline de evidencia** | Capturar y verificar la evidencia | G0 aprobado | Reglas de proceso; doble calificación con ICC; extracción de texto de CV en sandbox; localizador de fragmentos y STT solo si G0 los aprueba | D-06, D-07, D-12, D-13, D-15 |
| **F36 ML baseline** | Solo si se justifica, un modelo interpretable sobre el proceso | F34 y G0 aprobado | Model card; métricas calibradas; comparación con reglas; decisión de usarlo o no | D-18, D-19 |
| **F37 XAI y equidad** | Explicaciones y controles de equidad | G0 aprobado; F35 (y F36 si existe) | Explicaciones BARS contrastivas; controles de procedimiento; método de revisión agregada probado con datos sintéticos | D-20, D-21 |
| **F38 Integración Laravel ↔ ML** | Integrar sin romper contratos | G0 aprobado; F35–F37 | Cola, idempotencia, *fallback*, versionado, auditoría, multiempresa, pruebas cross-tenant, regresión completa | D-22–D-26 |
| **F39 Evaluación** | Medir con honestidad | G0 aprobado; F38 | Métricas por tarea; auditoría interna; informe de límites | D-27, D-28 |
| **F40 Panel** | Mostrar evidencia, no veredictos | F38–F39 | Desglose del ranking, evidencia, acuerdo y faltantes; accesibilidad; sin insignias de candidato | D-29 |

## 5. Decisiones pendientes del equipo

1. ¿Se ratifica ADR-001 tal como está (recomendación de F30) o se enmienda? Si se enmienda, ¿con qué límites exactos?
2. ¿El motor incluirá grabación de audio o solo notas del evaluador?
3. ¿Qué vacantes cubre: solo docentes o también personal administrativo?
4. ¿Quién valida el catálogo de competencias en el colegio y con qué periodicidad?
5. ¿El Colegio Andino es una institución pública o privada? Cambia las obligaciones del DS 115-2025-PCM (arts. 28 y 31).
6. ¿Quién firma la evaluación de impacto y quién hace la revisión jurídica?

## 6. Qué no se debe hacer en F33–F40 (resumen)

- Puntuar, sugerir niveles, ordenar por ML o recomendar candidatos.
- Inferir emociones, personalidad, «ajuste cultural», rasgos faciales, prosodia o acento.
- Usar LLM para evaluar, resumir o comparar candidatos.
- Entrenar con decisiones de contratación pasadas como etiqueta.
- Recolectar atributos sensibles sin el análisis de necesidad, consentimiento, base legal, finalidad y seguridad.
- Usar datos reales o PII.
- Instalar herramientas sin autorización.
- Modificar RF-01 a RF-27, la decisión humana de RF-23, la multiempresa o la auditoría de solo inserción.
