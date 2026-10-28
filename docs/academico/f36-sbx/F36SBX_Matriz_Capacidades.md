# F36-SBX — Matriz de capacidades ALLOWED / CONDITIONAL / BLOCKED

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. **En F36-SBX no se implementa ninguna capacidad.** La clase indica solo si una capacidad podría pedirse para **F37-SBX**, y siempre exclusivamente con datos sintéticos.

## Clases

| Clase | Significado | Qué hace falta para usarla en F37-SBX |
|---|---|---|
| **ALLOWED** | Determinista, de alcance B, sin dependencias nuevas, con texto registrado o introducido por una persona sintética | F36-SBX-GATE SUPERADO y la capacidad incluida en la autorización del equipo (FG-03) |
| **CONDITIONAL** | Alcance C, o frontera B/C sin resolver | Lo mismo que ALLOWED, más su condición: ADR sucesor APROBADO por el equipo (FG-12) o confirmación escrita de la frontera (F36-M02) |
| **BLOCKED** | Contradice ADR-001, ADR-002, el contrato 4, una prohibición de F34E o una CAP BLOQUEADA de F33, o no es proporcional | No puede pedirse en F37-SBX. Una autorización sandbox sucesora no tiene autoridad para habilitarla |

**Reglas de coherencia con F33.** Las verifica [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py), regla CAP:

1. Una fila que cita una CAP **BLOQUEADA** en la [matriz F33](../diseno-inteligente/F33_Matriz_Capacidades_y_Restricciones.md) es BLOCKED.
2. Una fila que cita una CAP **FUTURA** no puede ser ALLOWED.
3. Una fila de alcance C no puede ser ALLOWED.
4. La clase y el alcance de cada EI están fijados en el validador. Reclasificar una EI, por ejemplo EI-09, exige un incremento auditado.
5. Una capacidad ALLOWED no puede nombrar técnicas de alcance C ni bloqueadas: embeddings, búsqueda semántica, OCR, LLM, PDF, DOCX, NER, extracción, transformers, Whisper, STT o audio.

F36-SBX nunca relaja una clasificación de F33.

## Matriz

| ID | Capacidad | Clase | Alcance | CAP F33 | Condiciones o motivo | Etapa propuesta |
|---|---|---|---|---|---|---|
| EI-01 | Organizar la evidencia por tipo, criterio y fuente, a partir de metadatos declarados por una persona | **ALLOWED** | B | CAP-04, CAP-06 | Determinista y sin leer el contenido. No crea campos sobre la persona | F37-SBX-A |
| EI-02 | Alerta de proceso «requisito no evidenciado»: requisitos declarados frente a los requisitos de la vacante | **ALLOWED** | B | CAP-01, CAP-34 | Determinista. Nunca descarta (RF-13 sigue humano) y la alerta habla del proceso, no de la persona | F37-SBX-A |
| EI-03 | Trazabilidad evidencia → criterio: comprobar que cada enlace creado por una persona apunta a una cita existente, con su fuente y su `criteria_version` | **ALLOWED** | B | CAP-04, CAP-29 | Comprueba la integridad del enlace, no su relevancia. El enlace lo crea la persona | F37-SBX-A |
| EI-04 | Desglose estructurado por criterio de las postulaciones sintéticas de una vacante | **ALLOWED** | B | CAP-13 | Orden fijo por identificador sintético, nunca por un valor. Sin totales nuevos ni insignias. No sustituye RF-22 | F37-SBX-A |
| EI-05 | Guardia de entrada: detección determinista de PII (correo, teléfono, DNI, URL) en todo texto sintético | **ALLOWED** | B | — | Patrones de la biblioteca estándar. Ante una coincidencia, falla cerrado: el artefacto no entra | F37-SBX-A |
| EI-06 | Tipo de documento (CV, certificado, transcripción revisada, observación) tomado de metadatos declarados | **ALLOWED** | B | CAP-06 | Sin modelo y sin inspeccionar el contenido | F37-SBX-A |
| EI-07 | Búsqueda léxica exacta, por subcadena o por token normalizado, dentro de **una** postulación, iniciada por el evaluador | **ALLOWED** | B | CAP-08 | Sin dependencias nuevas, sin parsing de PDF o DOCX y sin búsqueda entre postulaciones | F37-SBX-A |
| EI-08 | Extracción estructurada por reglas desde texto sintético nativo, como formación o fechas declaradas | **CONDITIONAL** | C | CAP-07 | Es extracción automática de documentos. Exige un ADR sucesor APROBADO. Solo campos no sensibles; nunca nombre, edad, género ni foto | F37-SBX-B |
| EI-09 | Recuperación léxica ponderada (BM25 o TF-IDF) de fragmentos de una postulación frente al texto de un criterio | **CONDITIONAL** | B | CAP-08 | Ordena fragmentos, no personas. Sin puntaje visible, solo después de la calificación humana y sin agregados por persona. El equipo debe confirmar por escrito que el orden por relevancia cabe en el alcance B (F36-M02) | F37-SBX-A, si se confirma |
| EI-10 | Recuperación semántica de fragmentos de una postulación con embeddings locales | **CONDITIONAL** | C | CAP-09, CAP-20 | ADR sucesor APROBADO. Modelo local fijado por hash, sin puntaje visible y después de la calificación. Exige la auditoría contrafactual de EI-24 | F37-SBX-B |
| EI-11 | Extracción de texto de PDF o DOCX sintéticos nacidos digitales | **CONDITIONAL** | C | CAP-07 | ADR sucesor APROBADO. Dependencia autorizada con versión, licencia y consulta OSV. Proceso aislado, con límites de tamaño, páginas y tiempo | F37-SBX-B |
| EI-12 | NER sobre texto sintético, solo para entidades no personales (institución, título, fecha) | **CONDITIONAL** | C | CAP-07 | Mismas condiciones que EI-08. Modelo local y ninguna entidad de persona. Prioridad baja | F37-SBX-B |
| EI-24 | Métricas de equidad por grupo de EI-09 o EI-10, con marcadores sintéticos contrafactuales | **CONDITIONAL** | C | CAP-32 | Solo sintético y solo para auditar la recuperación. El grupo sintético nunca es feature, y el resultado no se generaliza a personas | F37-SBX-B, con EI-10 |
| EI-13 | Resumen de la evidencia de un postulante, extractivo o generativo | **BLOCKED** | — | CAP-11, CAP-23 | Es un resumen del candidato: alucinación, sesgo y anclaje [S34, S83, S87] | — |
| EI-14 | Veredicto automático «cumple o no cumple», o nivel sugerido frente a un criterio | **BLOCKED** | — | CAP-05, CAP-19 | Sugerir niveles es scoring de personas (ADR-001) | — |
| EI-15 | OCR | **BLOCKED** | C | CAP-07 | No es necesario, porque los documentos sintéticos nacen digitales. Además es una dependencia pesada y las imágenes de documentos elevan el riesgo de PII (proporcionalidad, G0-13) | — |
| EI-16 | LLM sobre evidencia de candidatos: generar, resumir, comparar, juzgar o extraer | **BLOCKED** | — | CAP-11, CAP-23 | D-17 de F30: LLM fuera de la evaluación | — |
| EI-17 | LLM para generar el corpus sintético | **BLOCKED** | — | CAP-24 | Puede reproducir PII memorizada y no es reproducible. El corpus se genera con plantillas y semilla | — |
| EI-18 | Búsqueda, similitud u orden entre candidatos, o búsqueda entre postulaciones | **BLOCKED** | — | CAP-10, CAP-22 | Equivale a preseleccionar u ordenar personas [S11] | — |
| EI-19 | Scoring, ranking, recomendación, preselección, selección automática o «mejor candidato» | **BLOCKED** | — | CAP-15, CAP-16, CAP-17 | Contrato 4, ADR-001, ADR-002 y RF-23 | — |
| EI-20 | Inferencias desde rostro, gestos, voz, prosodia o acento; emociones, personalidad, honestidad, inteligencia, estrés o nerviosismo; biometría | **BLOCKED** | — | CAP-21, CAP-28 | Prohibición sin excepción (ADR-005 §6.7) | — |
| EI-21 | Audio y transcripción automática (STT), también con voz sintética | **BLOCKED** | — | CAP-27 | Necesita una aprobación aparte y no está en el alcance de F37-SBX. Las transcripciones de F37-SBX son texto sintético escrito como «revisado» | — |
| EI-22 | Ajuste fino o entrenamiento de modelos con evidencia | **BLOCKED** | — | CAP-25 | No hay etiquetas válidas y crearía un modelo sobre personas | — |
| EI-23 | Datos reales o integración productiva: endpoints, migraciones, UI o salidas hacia RF-21, RF-23 o RF-29 | **BLOCKED** | — | CAP-14, CAP-36 | Contrato 7 y regla de datos (ADR-005 §6.10) | — |

## Resumen

| Clase | Capacidades |
|---|---|
| ALLOWED | EI-01, EI-02, EI-03, EI-04, EI-05, EI-06, EI-07 |
| CONDITIONAL | EI-08, EI-09, EI-10, EI-11, EI-12, EI-24 |
| BLOCKED | EI-13, EI-14, EI-15, EI-16, EI-17, EI-18, EI-19, EI-20, EI-21, EI-22, EI-23 |

## Alcance C: qué se propone y qué no

- **Hoy no se habilita nada del alcance C.** Las capacidades de alcance C son CONDITIONAL o BLOCKED, y ninguna CONDITIONAL se puede usar sin un ADR sucesor APROBADO por el equipo (FG-12).
- **Subconjunto propuesto para estudio, solo sintético:** EI-11 (extracción de texto de documentos nacidos digitales), EI-08 y EI-12 (extracción estructurada) y EI-10 (localizador semántico), con la auditoría contrafactual EI-24. Se agrupan en una etapa propia, F37-SBX-B, que no puede empezar antes que F37-SBX-A.
- **Se mantienen bloqueados:** el OCR (EI-15), los LLM (EI-16 y EI-17), el audio (EI-21) y toda búsqueda entre candidatos (EI-18).
- Cualquier autorización de un subconjunto de C debe ser **explícita** (lista cerrada de EI), **trazable** (registro fechado del equipo), **revocable** (sección 7 del [charter](F36SBX_Charter.md#7-revocación)) y **separada** de la G0 real. No cambia el estado «Alcance C = BLOQUEADO» del producto.
