# F33 — Matriz de capacidades y restricciones

> Fase F33, versión 1 (04/10/2026), **pendiente de auditoría**. Clasifica lo que el motor **podría** hacer según [ADR-005](F33_ADR_005_G0.md) (propuesta). **Ninguna capacidad nueva es implementable hoy: G0 = NO APROBADA.** Solo existen las marcadas como «existente».

**Frontera B/C.** El alcance **B** no usa dependencias nuevas ni extrae automáticamente texto de PDF o DOCX: trabaja solo con texto y evidencia **registrados o introducidos por una persona**, y puede buscar o localizar de forma determinista dentro de ese texto. Pertenece al alcance **C** cualquier parsing o extracción automática de PDF o DOCX, el OCR, la extracción automática de CV o documentos, las dependencias nuevas de comprensión documental y la búsqueda semántica o con embeddings.

**Regla de datos.** F34 trabaja **solo con datos sintéticos**. F33 y G0 **no autorizan datos reales de candidatos**, y el consentimiento por sí solo **no** levanta el contrato 7 ni las restricciones vigentes. Cualquier uso futuro de datos reales exige: (1) autorización explícita del equipo; (2) revisión contractual (contrato 7); (3) revisión jurídica; (4) análisis de privacidad y datos personales; y (5) una aprobación específica posterior, distinta de G0.

## Clasificaciones

| Clasificación | Significado | Cuándo podría implementarse |
|---|---|---|
| **PERMITIDA** | Encaja en el alcance B o ya existe | Con G0 APROBADA CON RESTRICCIONES (o ya existe) |
| **PERMITIDA CON RESTRICCIONES** | Encaja en el alcance B solo si se cumplen las condiciones indicadas | Con G0 CON RESTRICCIONES, más sus condiciones |
| **FUTURA** | Alcance C o posterior; requiere evidencia que hoy no existe | Con G0 APROBADA y un ADR adicional |
| **BLOQUEADA** | Contradice ADR-001, ADR-002, el contrato 4, OUT-04/05/11 o la evidencia | No alcanzable en este ciclo |

## Matriz

| # | Capacidad | Clasificación | Condiciones o motivo | Evidencia o norma | Fase |
|---|---|---|---|---|---|
| CAP-01 | Validación de requisitos obligatorios | **PERMITIDA CON RESTRICCIONES** | Comprobación **determinista** de lo declarado o adjuntado frente a los requisitos de la vacante. Produce una alerta «requisito no evidenciado» para RR. HH. **Nunca descarta automáticamente** (RF-13 sigue siendo humano; ADR-001 prohíbe filtrar). Sin interpretar texto libre con IA | ADR-001, ADR-002, RF-13 | F35 |
| CAP-02 | Rúbricas BARS versionadas | **PERMITIDA** | Publicadas = inmutables; validadas con el colegio | [S19, S15] | F35 |
| CAP-03 | Ponderaciones | **PERMITIDA** (existente) | Regla A-06 sin cambios; AHP solo para documentar la justificación de los pesos | RF-20, A-06, [S39] | — |
| CAP-04 | Evidencia por competencia o criterio (registro humano con procedencia) | **PERMITIDA** | Cita mínima, fuente y criterio; justificación obligatoria | [S71, S73], RF-19 | F35 |
| CAP-05 | Nivel observado por criterio | **PERMITIDA solo como acción humana** | El sistema no sugiere niveles; el humano califica antes de ver cualquier ayuda | ADR-001, [S84] | F35 |
| CAP-06 | Extracción manual estructurada (formulario del evaluador) | **PERMITIDA** | El evaluador transcribe o cita | — | F35 |
| CAP-07 | Extracción automática de datos de CV o documentos: parsing de PDF o DOCX, OCR | **FUTURA** | Alcance C: requiere G0 APROBADA, un ADR adicional y dependencias de comprensión documental autorizadas (p. ej., pypdf o pdfplumber evaluados en sandbox en F30). Solo para localizar evidencia; nunca para filtrar o puntuar | [S37], F30 herramientas | F35 (si G0 APROBADA) |
| CAP-08 | Búsqueda léxica determinista dentro del texto ya registrado o introducido por una persona en **una** postulación (evidencias, notas, justificaciones), iniciada por el evaluador | **PERMITIDA CON RESTRICCIONES** | Alcance B: sin dependencias nuevas y sin parsing de PDF o DOCX; no ordena candidatos ni busca entre postulaciones | ADR-005 (frontera B/C) | F35 |
| CAP-09 | Búsqueda semántica (embeddings) | **FUTURA** | Solo como localizador de fragmentos tras la calificación; sin puntaje visible ni búsqueda entre candidatos; con auditoría de sesgo previa | [S31, S11] | F35/F37 (si G0 APROBADA) |
| CAP-10 | Búsqueda o ordenamiento de candidatos por similitud con el perfil | **BLOQUEADA** | Equivale a ordenar o preseleccionar personas | ADR-001, [S11] | — |
| CAP-11 | Resumen automático de un candidato (LLM u otro) | **BLOQUEADA** | Alucinación y sesgo; condiciona la decisión | [S34, S83, S87] | — |
| CAP-12 | Resumen del estado del **proceso** (conteos, pendientes, alertas) | **PERMITIDA** | Sin datos personales; relación con el candidato RF-28 | RF-28 (cand.) | F40 |
| CAP-13 | Comparación estructurada (desglose por criterio y evidencia) | **PERMITIDA** | Extiende RF-22 sin insignias de «recomendado» | RF-22, ADR-002 | F40 |
| CAP-14 | Ranking actual RF-21 | **PERMITIDA** (existente) | Sin cambios; ninguna salida de ML lo alimenta; empates sin desempate automático | RF-21, A-24, A-26 | — |
| CAP-15 | Scoring inteligente de candidatos | **BLOQUEADA** | ADR-001 (alternativas 1 y 2 rechazadas), contrato 4, OUT-04/05 | [S84, S60, S58] | — |
| CAP-16 | Recomendación de candidatos | **BLOQUEADA** | Ídem; anclaje y sesgo transmitido | [S84, S57] | — |
| CAP-17 | Preselección, descarte o selección automática | **BLOQUEADA** | ADR-002: ninguna ruta automática | ADR-002, OUT-04 | — |
| CAP-18 | Análisis de entrevistas por contenido, hecho por el evaluador con preguntas estructuradas | **PERMITIDA** | Cadena pregunta → respuesta → evidencia → nivel humano | [S13, S14] | F35 |
| CAP-19 | Análisis automático de transcripciones para sugerir niveles | **BLOQUEADA** | Es scoring de personas | ADR-001, [S36] | — |
| CAP-20 | Localizar evidencia en transcripciones revisadas | **FUTURA** | Igual que CAP-09; solo sobre texto revisado por un humano | [S81] | — |
| CAP-21 | Inferencias desde rostro, voz o apariencia (personalidad, honestidad, inteligencia, estrés, estabilidad emocional, liderazgo, salud mental, idoneidad), prosodia, acento, emociones, biometría | **BLOQUEADA (prohibida sin excepción)** | Evidencia insuficiente y no fiable para alto impacto; prohibición o riesgo alto normativo | [S07, S08, S09, S85, S88], O01 art. 5, O13 | — |
| CAP-22 | Embeddings como puntaje o representación de candidatos | **BLOQUEADA** | Sesgo por nombre y género | [S11] | — |
| CAP-23 | LLM para evaluar, resumir o comparar personas | **BLOQUEADA** | Ídem CAP-11 | [S34, S36, S83, S87] | — |
| CAP-24 | LLM local para tareas **sin personas** (p. ej., borradores de preguntas que revisa un humano) | **FUTURA** | Herramienta en sandbox (F30: Ollama); dependencia autorizada; nunca con datos de postulantes | F30 herramientas | — |
| CAP-25 | ML supervisado sobre personas (idoneidad, desempeño, permanencia) | **BLOQUEADA** | Sin etiquetas válidas; sesgo de *proxy*; ADR-001 | [S42, S48, S04, S22] | — |
| CAP-26 | ML sobre el **proceso** (RF-29 y extensiones) | **PERMITIDA CON RESTRICCIONES** (existente) | Experimental e informativo; 15 contadores sin IDs ni PII; lejos del ranking y de la decisión (OUT-11) | ADR-001, ADR-004 | F36 |
| CAP-27 | Grabación de audio y transcripción | **FUTURA** | Por defecto no se graba. Requiere necesidad y G0 APROBADA; en este proyecto, solo datos ficticios; con personas reales, la regla de datos (el consentimiento por sí solo no basta). Además: STT local, revisión humana contra el audio y medición del error por grupo | [S38, S81, S10] | F35 (si G0 APROBADA) |
| CAP-28 | Vídeo | **BLOQUEADA** | No aporta y aumenta el sesgo | [S85] | — |
| CAP-29 | Explicabilidad basada en evidencia, reglas y versiones | **PERMITIDA** | Justificación contrastiva; enlace a la evidencia | [S55, S59] | F37 |
| CAP-30 | SHAP o LIME como explicación para el usuario | **BLOQUEADA** | Usados para depurar, no para justificar decisiones | [S52, S56, S58] | — |
| CAP-31 | Controles de equidad del procedimiento (mismas preguntas, BARS, CV minimizado, doble calificación) | **PERMITIDA** | — | [S14, S19, S20] | F35/F37 |
| CAP-32 | Métricas estadísticas de equidad sobre datos reales | **FUTURA** | Fuera de G0: exige los cinco requisitos de la regla de datos, además de muestra suficiente y agregación por convocatoria. Hoy solo se prueba el método con datos sintéticos (F37) | [S44, S45, S46], O11 | F37 |
| CAP-33 | Acuerdo entre evaluadores (ICC) | **PERMITIDA** | Métrica del proceso, no de la persona | [S20, S21] | F35/F39 |
| CAP-34 | Alertas deterministas de proceso | **PERMITIDA** | Nunca hablan de la persona | [S62] | F35 |
| CAP-35 | Recolección de atributos sensibles | **BLOQUEADA** | No recolectar (F30 D-10) | O15, O09 | — |
| CAP-36 | Entrenar, evaluar o probar con datos reales de candidatos | **BLOQUEADA** | Contrato 7. F33 y G0 no lo autorizan y el consentimiento por sí solo no lo habilita; solo una aprobación específica posterior con los cinco requisitos de la regla de datos | `CLAUDE.md` | — |
| CAP-37 | Comunicar al postulante salidas del motor (alertas, puntajes) | **BLOQUEADA** | A-31: el postulante solo recibe su resultado final | A-31 | — |

## Resumen

| Clasificación | Capacidades |
|---|---|
| PERMITIDA | CAP-02, 03, 04, 05 (solo humana), 06, 12, 13, 14, 18, 29, 31, 33, 34 |
| PERMITIDA CON RESTRICCIONES | CAP-01, 08, 26 |
| FUTURA | CAP-07, 09, 20, 24, 27, 32 |
| BLOQUEADA | CAP-10, 11, 15, 16, 17, 19, 21, 22, 23, 25, 28, 30, 35, 36, 37 |

Todas las fuentes [Sxx] y [Oxx] remiten a la [matriz de evidencia de F30](../investigacion-ia/F30_Matriz_Evidencia_Cientifica.md).
