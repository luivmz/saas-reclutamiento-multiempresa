# F30 — Investigación científica y tecnológica para el motor inteligente de reclutamiento

Investigación documental para decidir **qué puede y qué no debe hacer** un futuro motor inteligente de reclutamiento en el SaaS (caso Colegio Andino de Huancayo), antes de que F33–F40 implementen algo.

**Estado:** versión 1 (30/09/2026), **pendiente de auditoría**. F30 **no implementa nada**: no hay modelos, embeddings, base vectorial, parsing, transcripción, scoring, endpoints, migraciones ni interfaz. Tampoco se instaló ninguna herramienta, skill ni servidor MCP.

## Conclusión en una línea

La evidencia respalda un motor que **estructura y verifica la evidencia** que usan los evaluadores humanos (entrevista estructurada, rúbricas BARS, procedencia, acuerdo entre evaluadores). **No respalda scoring ni recomendación de candidatos para este caso, con los datos, el gobierno y las garantías actuales**; la calificación automática a escala existe [S89], pero en organizaciones con volúmenes de datos que el caso no tiene, y se registra como evidencia en tensión. La visión de «recomendar» choca con ADR-001 y el contrato 4, y el DS 115-2025-PCM clasifica este uso como de **riesgo alto** (art. 24.1 e). Por eso rige una puerta de gobierno:

**Regla G0.** F33 formula y aprueba ADR-005, que constituye la puerta G0. F34 puede avanzar en paralelo **solo con datos sintéticos** y sin scoring ni recomendación de personas. F35–F40 **no comienzan sin G0 aprobado**.

**RECOMENDACIÓN DEL SISTEMA ≠ DECISIÓN FINAL DE CONTRATACIÓN** (RF-23: la decisión es humana).

## Documentos

| Archivo | Contenido | Origen |
|---|---|---|
| [F30_Estado_del_Arte_IA_Reclutamiento.md](F30_Estado_del_Arte_IA_Reclutamiento.md) | Estado del arte por tema (A–T), perspectiva de RR. HH., prácticas recomendadas y a evitar | Redactado |
| [F30_Matriz_Evidencia_Cientifica.md](F30_Matriz_Evidencia_Cientifica.md) | Estrategia de búsqueda, flujo de selección y 89 fichas con 20 campos y nivel de evidencia; normas | Generado |
| [F30_Analisis_Modelos_y_Tecnicas.md](F30_Analisis_Modelos_y_Tecnicas.md) | Reglas, MCDM, ML, NLP y LLM comparados; criterios y competencias (ejemplo docente ilustrativo); cadena de procedencia; pipeline de audio; métricas; arquitectura; modelo de auditoría | Redactado |
| [F30_Explainability_Fairness_Gobernanza.md](F30_Explainability_Fairness_Gobernanza.md) | Explicabilidad, métricas de equidad y sus límites, sesgo de automatización, marco legal, conflicto con ADR-001, gobernanza del dataset | Redactado |
| [F30_Analisis_Herramientas_Skills.md](F30_Analisis_Herramientas_Skills.md) | 49 herramientas y MCP con datos verificados y clasificación; skills locales; señales de cadena de suministro | Generado |
| [F30_Recomendaciones_F33_F40.md](F30_Recomendaciones_F33_F40.md) | Puerta G0, 30 decisiones (DECISIÓN / EVIDENCIA / ALTERNATIVAS / RIESGO / RECOMENDACIÓN / FASE) y plan por fase | Redactado |
| [REFERENCIAS.md](REFERENCIAS.md) | 107 referencias: trabajos desde metadatos de Crossref y DataCite; normas desde su fuente oficial | Generado |
| [F30_Investigacion_IA_Reclutamiento.docx](F30_Investigacion_IA_Reclutamiento.docx) · [PDF](F30_Investigacion_IA_Reclutamiento.pdf) | Consolidado de los documentos anteriores | Generado |
| [`datos/`](datos/) | `busqueda_openalex.json`, `verificacion_fuentes.json`, `herramientas.json` | Generado por los scripts |

## Fuentes en cifras

- **Búsqueda:** 20 consultas en OpenAlex, una por tema A–T, con 500 registros cribados (25 por consulta).
- **Trabajos científicos:** 89, de los cuales 35 vienen del cribado, 9 de una búsqueda complementaria 2021–2025 y 45 de bola de nieve y trabajos fundacionales.
- **Normas y documentos oficiales:** 16. **Fuentes secundarias de contraste:** 2.
- **Verificación:** las 107 fuentes están verificadas en Crossref, DataCite o por HTTP con palabra clave en el título; las normas de la UE, en el texto oficial del Diario Oficial.
- **Avisos y exclusiones:** un artículo retractado del cribado quedó excluido. Dos fuentes tienen avisos menores, una corrección (S08) y una errata (S21).

## Cómo se reproduce

Desde la raíz del repositorio, con Python 3.12 y sin dependencias externas (solo biblioteca estándar y red):

```
python docs/academico/tools/f30/busqueda.py                       # búsqueda OpenAlex → datos/busqueda_openalex.json
python docs/academico/tools/f30/verificar.py [--abstracts DIR]    # verificación → datos/verificacion_fuentes.json
python docs/academico/tools/f30/herramientas.py [--completar]     # GitHub, PyPI, npm y OSV → datos/herramientas.json
python docs/academico/tools/f30/f30.py                            # matriz, referencias, herramientas y DOCX
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/investigacion-ia/F30_Investigacion_IA_Reclutamiento.docx
python docs/academico/tools/f30/validate_f30.py                   # validación de F30
```

- Los resúmenes de OpenAlex se descargan a una carpeta temporal (`--abstracts`) solo para la lectura del equipo. **No se versionan**, por derechos de autor.
- Las consultas a APIs públicas devuelven datos que cambian con el tiempo (citas, versiones, avisos). Cada JSON registra su fecha.

## Límites

- La extracción se hizo sobre resúmenes, no sobre el texto completo. Si no hay resumen disponible, la matriz lo indica y no da cifras.
- El análisis normativo es técnico y **no es asesoría legal**.
- Algunos datos de herramientas dependen de la API de GitHub sin autenticación, limitada a 60 consultas por hora. Si faltan, el documento lo dice.
- El calendario de la Ley de IA de la UE se cita desde la fuente oficial, el Reglamento (UE) 2026/1744 [O16]: los requisitos de alto riesgo del Anexo III se aplican desde el 2/12/2027. X02 queda solo como contexto.
- DS 115-2025-PCM [O13]: el art. 24.1 e) está corroborado; los arts. 24, 30 y 31 (y los demás citados) requieren contraste artículo por artículo con la publicación normativa oficial antes de producir efectos jurídicos.
- El ejemplo de criterios docentes es **ilustrativo** y no está adoptado.

## Siguiente paso

Auditoría de F30 por el equipo y, si se aprueba, apertura de F33. **Regla G0.** F33 formula y aprueba ADR-005, que constituye la puerta G0. F34 puede avanzar en paralelo **solo con datos sintéticos** y sin scoring ni recomendación de personas. F35–F40 **no comienzan sin G0 aprobado**.
