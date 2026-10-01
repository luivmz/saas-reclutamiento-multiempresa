# F30 — Matriz de evidencia científica

> Documento generado por `docs/academico/tools/f30/f30.py` desde `fuentes.py`, `m_matriz.py` y los datos verificados de `datos/`. No se edita a mano.

**Cómo leer la matriz.** Cada ficha separa cuatro tipos de afirmación:

- **Evidencia científica:** «Resultados relevantes», tomado del resumen publicado del trabajo. Si el trabajo no tiene resumen disponible, se indica y no se dan cifras.
- **Recomendación de los autores:** cuando el resultado es una propuesta o guía, se escribe como tal.
- **Inferencia del equipo:** «Aplicabilidad al caso».
- **Decisión de ingeniería:** «Decisión que respalda». Las decisiones finales están en [F30_Recomendaciones_F33_F40.md](F30_Recomendaciones_F33_F40.md).

**Niveles de evidencia** (sobre el aporte de la fuente a la decisión, no sobre su prestigio):

| Nivel | Significado |
|---|---|
| FUERTE | Metaanálisis, revisión amplia o resultado formal o experimental robusto y replicado |
| MODERADA | Estudio empírico sólido, revisión sistemática o guía ampliamente adoptada, con límites de contexto |
| LIMITADA | Estudio único, caso de aplicación o contexto muy distinto del caso |
| CONFLICTIVA | Resultados que otras fuentes de la matriz contradicen o matizan |
| INSUFICIENTE | No hay datos suficientes para extraer resultados (p. ej., sin resumen disponible) |

## 1. Estrategia de búsqueda

- **Base de búsqueda:** OpenAlex (API pública, 2026-09-30), elegida por indexar Crossref, PubMed, arXiv y repositorios, y por devolver resúmenes; Crossref respondió con límite de tasa (HTTP 429) en búsquedas masivas, por eso se usó solo para verificar.
- **Verificación:** Crossref para cada DOI (metadatos y avisos de retractación, corrección o retirada), DataCite para DOI de arXiv y SSRN, y respuesta HTTP con palabra clave esperada en el título para normas y páginas oficiales (`verificar.py`).
- **Criterio de cribado:** orden por relevancia; 25 primeros resultados de cada consulta como conjunto cribado.
- **Inclusión:** trabajo revisado por pares, metaanálisis, revisión sistemática, norma oficial o trabajo fundacional muy citado; relación directa con un tema A–T; resumen o texto que permita extraer los campos.
- **Exclusión:** sin DOI ni URL verificable, retractado, duplicado, opinión sin método, o tema solo tangencial (p. ej., IA en reclutamiento de pacientes clínicos, que aparece mucho al buscar «recruitment»).
- **Bola de nieve:** trabajos citados por los seleccionados y trabajos fundacionales que la búsqueda por relevancia no devuelve en los 25 primeros (p. ej., metaanálisis de validez de la entrevista).
- **Búsqueda complementaria:** consultas dirigidas a 2021–2025 para cubrir huecos (alucinación de Whisper, sesgo de LLM en contratación, calificación automática de respuestas abiertas, entrevistas multimodales).

### Consultas

| Tema | Nombre | Consulta | Resultados | Cribados | Trabajos seleccionados |
|---|---|---|---|---|---|
| A | AI in recruitment / algorithmic hiring | `algorithmic hiring artificial intelligence recruitment` | 20 662 | 25 | 4 |
| B | Candidate-job fit | `person-job fit candidate job matching` | 40 796 | 25 | 1 |
| C | Competency-based assessment | `competency modeling personnel selection` | 218 279 | 25 | 1 |
| D | Structured interviews | `structured employment interview validity` | 403 463 | 25 | 2 |
| E | CV / resume NLP | `resume parsing natural language processing` | 11 251 | 25 | 2 |
| F | Semantic matching | `semantic matching job postings resumes embeddings` | 717 | 25 | 1 |
| G | Information extraction | `skill extraction job postings information extraction` | 8 129 | 25 | 2 |
| H | Ranking / recommendation | `job recommender system e-recruitment survey` | 261 296 | 25 | 2 |
| I | Multicriteria decision support | `multi-criteria decision making personnel selection` | 193 791 | 25 | 1 |
| J | Explainable AI | `explainable artificial intelligence interpretability survey` | 390 115 | 25 | 1 |
| K | Fairness / algorithmic bias | `algorithmic fairness bias machine learning survey` | 161 027 | 25 | 2 |
| L | Responsible AI | `responsible artificial intelligence governance accountability` | 96 767 | 25 | 1 |
| M | Human-in-the-loop | `human-AI decision making automation bias reliance` | 48 672 | 25 | 3 |
| N | Uncertainty / calibration | `probability calibration classifiers uncertainty` | 75 737 | 25 | 3 |
| O | Model monitoring / drift | `concept drift dataset shift monitoring machine learning` | 32 607 | 25 | 3 |
| P | Auditability | `algorithmic auditing accountability machine learning` | 64 390 | 25 | 2 |
| Q | Recruitment analytics | `human resource analytics people analytics` | 947 321 | 25 | 1 |
| R | Document understanding | `document understanding layout analysis PDF parsing` | 7 801 | 25 | 1 |
| S | Speech-to-text for interviews | `automatic speech recognition robust weak supervision` | 46 793 | 25 | 1 |
| T | Interview transcript evaluation | `automated interview assessment transcripts language` | 28 515 | 25 | 1 |

Además, O03 (L) y O04 (A) son documentos oficiales que aparecieron en el cribado; se cuentan entre las normas y no entre los trabajos.

### Flujo de selección

```
Resultados devueltos por las 20 consultas ........ 3 058 129
Cribados (25 primeros por consulta) ............... 500 registros, 450 DOI únicos
  seleccionados desde el cribado .................. 35
  excluidos del cribado ........................... resto (fuera de tema, sin método, duplicados,
                                                     1 retractado)
Búsqueda complementaria 2021–2025 ................. 9
Bola de nieve y trabajos fundacionales ............ 45
Trabajos científicos en la matriz (S01–S89) ...... 89
Normas y documentos oficiales (O01–O16) ........... 16
Fuentes secundarias de contraste (X01–X02) ........ 2
Total verificado ................................... 107 de 107
```

El cribado fue por título, tipo y revista; la extracción de campos se hizo sobre el resumen publicado (OpenAlex). Los conteos «Resultados» son los que devuelve OpenAlex para la consulta y no equivalen a trabajos pertinentes: solo indican el tamaño del área.

## 2. Resumen de la matriz

Distribución por nivel: FUERTE 19, MODERADA 62, LIMITADA 4, CONFLICTIVA 3, INSUFICIENTE 1.

| ID | Referencia | Tema | Tipo | Revisión por pares | Nivel |
|---|---|---|---|---|---|
| S01 | Raghavan et al. (2020) | A | Artículo de conferencia | Sí | MODERADA |
| S02 | Köchling y Wehner (2020) | A | Artículo de revista | Sí | MODERADA |
| S03 | Hunkenschroer y Luetge (2022) | A | Artículo de revista | Sí | MODERADA |
| S04 | Tambe et al. (2019) | A | Artículo de revista | Sí | MODERADA |
| S05 | Chen (2023) | A | Artículo de revista | Sí | LIMITADA |
| S06 | Langer et al. (2019) | A | Artículo de revista | Sí | MODERADA |
| S07 | Hickman et al. (2022) | T | Artículo de revista | Sí | MODERADA |
| S08 | Barrett et al. (2019) | T | Artículo de revista | Sí | FUERTE |
| S09 | Stark y Hoey (2021) | T | Artículo de conferencia | Sí | MODERADA |
| S10 | Koenecke et al. (2020) | S | Artículo de revista | Sí | MODERADA |
| S11 | Wilson y Caliskan (2024) | E | Artículo de revista | Sí | MODERADA |
| S12 | Schmidt y Hunter (1998) | D | Artículo de revista | Sí | CONFLICTIVA |
| S13 | Sackett et al. (2022) | D | Artículo de revista | Sí | FUERTE |
| S14 | McDaniel et al. (1994) | D | Artículo de revista | Sí | FUERTE |
| S15 | Campion et al. (1997) | D | Artículo de revista | Sí | MODERADA |
| S16 | Levashina et al. (2013) | D | Artículo de revista | Sí | FUERTE |
| S17 | Campion et al. (2011) | C | Artículo de revista | Sí | MODERADA |
| S18 | Sanchez y Levine (2012) | C | Artículo de revista | Sí | MODERADA |
| S19 | Smith y Kendall (1963) | C | Artículo de revista | Sí | MODERADA |
| S20 | Shrout y Fleiss (1979) | C | Artículo de revista | Sí | FUERTE |
| S21 | Koo y Li (2016) | C | Artículo de revista | Sí | FUERTE |
| S22 | Klassen y Kim (2019) | C | Artículo de revista | Sí | FUERTE |
| S23 | Woods et al. (2019) | C | Artículo de revista | Sí | MODERADA |
| S24 | Huffcutt et al. (2001) | D | Artículo de revista | Sí | MODERADA |
| S25 | Zhu et al. (2018) | B | Artículo de revista | Sí | LIMITADA |
| S26 | Qin et al. (2018) | B | Artículo de conferencia | Sí | LIMITADA |
| S27 | Freire y de Castro (2020) | H | Artículo de revista | Sí | MODERADA |
| S28 | Mashayekhi et al. (2024) | H | Artículo de revista | Sí | MODERADA |
| S29 | Zhang et al. (2022) | G | Artículo de conferencia | Sí | MODERADA |
| S30 | Khaouja et al. (2021) | G | Artículo de revista | Sí | MODERADA |
| S31 | Reimers y Gurevych (2019) | F | Artículo de conferencia | Sí | FUERTE |
| S32 | Blodgett et al. (2020) | E | Artículo de conferencia | Sí | MODERADA |
| S33 | Bender y Friedman (2018) | E | Artículo de revista | Sí | MODERADA |
| S34 | Ji et al. (2023) | E | Artículo de revista | Sí | FUERTE |
| S35 | Bender et al. (2021) | E | Artículo de conferencia | Sí | MODERADA |
| S36 | Zheng et al. (2023) | T | Preprint (arXiv) | No (preprint); publicado en NeurIPS 2023 | MODERADA |
| S37 | Xu et al. (2021) | R | Artículo de conferencia | Sí | MODERADA |
| S38 | Radford et al. (2022) | S | Preprint (arXiv) | No (preprint); publicado en ICML 2023 | MODERADA |
| S39 | Saaty (1990) | I | Artículo de revista | Sí | MODERADA |
| S40 | Kelemenis y Askounis (2010) | I | Artículo de revista | Sí | LIMITADA |
| S41 | Mehrabi et al. (2021) | K | Artículo de revista | Sí | MODERADA |
| S42 | Barocas y Selbst (2016) | K | Artículo de revista | Revisión editorial (revista jurídica) | MODERADA |
| S43 | Hardt et al. (2016) | K | Preprint (arXiv) | No (preprint); publicado en NeurIPS 2016 | FUERTE |
| S44 | Kleinberg et al. (2017) | K | Artículo de conferencia | Sí | FUERTE |
| S45 | Chouldechova (2017) | K | Artículo de revista | Sí | FUERTE |
| S46 | Friedler et al. (2019) | K | Artículo de conferencia | Sí | MODERADA |
| S47 | Suresh y Guttag (2021) | K | Artículo de conferencia | Sí | MODERADA |
| S48 | Obermeyer et al. (2019) | K | Artículo de revista | Sí | FUERTE |
| S49 | Bellamy et al. (2019) | K | Artículo de revista | Sí | MODERADA |
| S50 | Holstein et al. (2019) | K | Artículo de conferencia | Sí | MODERADA |
| S51 | Rudin (2019) | J | Artículo de revista | Sí | MODERADA |
| S52 | Ribeiro et al. (2016) | J | Artículo de conferencia | Sí | MODERADA |
| S53 | Lundberg y Lee (2017) | J | Preprint (arXiv) | No (preprint); publicado en NeurIPS 2017 | MODERADA |
| S54 | Wachter et al. (2017) | J | Documento de trabajo (SSRN) | No (documento de trabajo en SSRN); publicado luego en Harvard Journal of Law & Technology | MODERADA |
| S55 | Miller (2019) | J | Artículo de revista | Sí | MODERADA |
| S56 | Bhatt et al. (2020) | J | Artículo de conferencia | Sí | MODERADA |
| S57 | Green y Chen (2019) | M | Artículo de conferencia | Sí | MODERADA |
| S58 | Bansal et al. (2021) | M | Artículo de conferencia | Sí | MODERADA |
| S59 | Vasconcelos et al. (2023) | M | Artículo de revista | Sí | MODERADA |
| S60 | Vaccaro et al. (2024) | M | Artículo de revista | Sí | FUERTE |
| S61 | Alon-Barkat y Busuioc (2022) | M | Artículo de revista | Sí | CONFLICTIVA |
| S62 | Amershi et al. (2019) | M | Artículo de conferencia | Sí | MODERADA |
| S63 | Parasuraman y Manzey (2010) | M | Artículo de revista | Sí | MODERADA |
| S64 | Niculescu-Mizil y Caruana (2005) | N | Artículo de conferencia | Sí | FUERTE |
| S65 | Guo et al. (2017) | N | Preprint (arXiv) | No (preprint); publicado en ICML 2017 | MODERADA |
| S66 | Brier (1950) | N | Artículo de revista | Sí | FUERTE |
| S67 | Silva Filho et al. (2023) | N | Artículo de revista | Sí | MODERADA |
| S68 | Saito y Rehmsmeier (2015) | N | Artículo de revista | Sí | MODERADA |
| S69 | Järvelin y Kekäläinen (2002) | N | Artículo de revista | Sí | FUERTE |
| S70 | Hüllermeier y Waegeman (2021) | N | Artículo de revista | Sí | MODERADA |
| S71 | Mitchell et al. (2019) | P | Artículo de conferencia | Sí | MODERADA |
| S72 | Gebru et al. (2021) | P | Artículo de revista | Sí | MODERADA |
| S73 | Raji et al. (2020) | P | Artículo de conferencia | Sí | MODERADA |
| S74 | Kaufman et al. (2012) | O | Artículo de revista | Sí | FUERTE |
| S75 | Gama et al. (2014) | O | Artículo de revista | Sí | MODERADA |
| S76 | Breck et al. (2017) | O | Artículo de conferencia | Sí | MODERADA |
| S77 | Kreuzberger et al. (2023) | O | Artículo de revista | Sí | MODERADA |
| S78 | Paleyes et al. (2022) | O | Artículo de revista | Sí | MODERADA |
| S79 | Hutchinson et al. (2021) | P | Artículo de conferencia | Sí | MODERADA |
| S80 | Giermindl et al. (2021) | Q | Artículo de revista | Sí | MODERADA |
| S81 | Koenecke et al. (2024) | S | Artículo de conferencia | Sí | MODERADA |
| S82 | Thompson et al. (2023) | T | Artículo de revista | Sí | INSUFICIENTE |
| S83 | Armstrong et al. (2024) | E | Artículo de conferencia | Sí | MODERADA |
| S84 | Wilson et al. (2025) | M | Artículo de revista | Sí | FUERTE |
| S85 | Booth et al. (2021) | T | Artículo de conferencia | Sí | MODERADA |
| S86 | Van Iddekinge et al. (2023) | D | Artículo de revista | Sí | MODERADA |
| S87 | Glazko et al. (2024) | E | Artículo de conferencia | Sí | MODERADA |
| S88 | Bredin (2023) | S | Artículo de conferencia | Sí | MODERADA |
| S89 | Koenig et al. (2023) | C | Artículo de revista | Sí | CONFLICTIVA |

## 3. Fichas de evidencia

### S01 — Raghavan et al. (2020)

| Campo | Contenido |
|---|---|
| Referencia | Raghavan, M., Barocas, S., Kleinberg, J. y Levy, K. (2020). Mitigating bias in algorithmic hiring. *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3351095.3372828 |
| Año | 2020 |
| Autores | Raghavan, M., Barocas, S., Kleinberg, J. y Levy, K. |
| Revista o conferencia | Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3351095.3372828 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | A · búsqueda A |
| Avisos de Crossref | ninguno |
| Objetivo | Analizar afirmaciones y prácticas de proveedores de evaluaciones algorítmicas de preempleo |
| Datos o población | Información pública de proveedores comerciales |
| Técnica | Análisis documental técnico y jurídico |
| Variables o características | Datos usados, objetivo de predicción, validación, des-sesgo declarado |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Las decisiones sobre datos y objetivo de predicción crean riesgos; el des-sesgo técnico interactúa de forma compleja con la ley antidiscriminación |
| Limitaciones | Solo lo que los proveedores publican; contexto EE. UU. |
| Riesgos de sesgo | Objetivos de predicción basados en decisiones históricas heredan sesgo |
| Aplicabilidad al caso (inferencia del equipo) | Directa: advierte sobre elegir «etiquetas» de contratación pasada |
| Decisión que respalda (decisión de ingeniería) | No entrenar con decisiones históricas como etiqueta; documentar validación y sesgo |
| Nivel de confianza | MODERADA |

### S02 — Köchling y Wehner (2020)

| Campo | Contenido |
|---|---|
| Referencia | Köchling, A. y Wehner, M. C. (2020). Discriminated by an algorithm: a systematic review of discrimination and fairness by algorithmic decision-making in the context of HR recruitment and HR development. *Business Research*. https://doi.org/10.1007/s40685-020-00134-w |
| Año | 2020 |
| Autores | Köchling, A. y Wehner, M. C. |
| Revista o conferencia | Business Research |
| DOI / URL | https://doi.org/10.1007/s40685-020-00134-w |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | A · búsqueda A |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar la literatura sobre discriminación y equidad en decisiones algorítmicas de RR. HH. |
| Datos o población | 36 artículos (2014–2020) |
| Técnica | Revisión sistemática |
| Variables o características | Aplicaciones en reclutamiento y desarrollo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | El conocimiento sobre discriminación implícita en RR. HH. es aún escaso; identifica riesgos y vacíos |
| Limitaciones | Corpus pequeño y temprano |
| Riesgos de sesgo | Riesgo de discriminación implícita y percepción de injusticia |
| Aplicabilidad al caso (inferencia del equipo) | Alta para el marco de riesgos |
| Decisión que respalda (decisión de ingeniería) | Tratar la equidad como requisito de diseño, no como añadido |
| Nivel de confianza | MODERADA |

### S03 — Hunkenschroer y Luetge (2022)

| Campo | Contenido |
|---|---|
| Referencia | Hunkenschroer, A. L. y Luetge, C. (2022). Ethics of AI-Enabled Recruiting and Selection: A Review and Research Agenda. *Journal of Business Ethics*. https://doi.org/10.1007/s10551-022-05049-6 |
| Año | 2022 |
| Autores | Hunkenschroer, A. L. y Luetge, C. |
| Revista o conferencia | Journal of Business Ethics |
| DOI / URL | https://doi.org/10.1007/s10551-022-05049-6 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | A · búsqueda F |
| Avisos de Crossref | ninguno |
| Objetivo | Mapear oportunidades, riesgos y ambigüedades éticas de la IA en reclutamiento |
| Datos o población | 51 artículos |
| Técnica | Revisión sistemática |
| Variables o características | Etapas: anuncios, cribado de CV, entrevistas en vídeo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Identifica riesgos éticos (incluido el análisis facial en vídeo) y medidas de mitigación |
| Limitaciones | Literatura emergente; pocos estudios empíricos |
| Riesgos de sesgo | Opacidad, discriminación, privacidad |
| Aplicabilidad al caso (inferencia del equipo) | Alta: cubre las mismas etapas que la visión F33–F40 |
| Decisión que respalda (decisión de ingeniería) | Excluir análisis facial; priorizar transparencia |
| Nivel de confianza | MODERADA |

### S04 — Tambe et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Tambe, P., Cappelli, P. y Yakubovich, V. (2019). Artificial Intelligence in Human Resources Management: Challenges and a Path Forward. *California Management Review*. https://doi.org/10.1177/0008125619867910 |
| Año | 2019 |
| Autores | Tambe, P., Cappelli, P. y Yakubovich, V. |
| Revista o conferencia | California Management Review |
| DOI / URL | https://doi.org/10.1177/0008125619867910 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | A · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Identificar retos del uso de ciencia de datos en RR. HH. |
| Datos o población | Ensayo conceptual con casos |
| Técnica | Análisis conceptual |
| Variables o características | Complejidad de fenómenos de RR. HH., datos pequeños, rendición de cuentas |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Propone razonamiento causal, aleatorización y participación de los empleados |
| Limitaciones | Sin datos empíricos propios |
| Riesgos de sesgo | Conjuntos pequeños y etiquetas débiles |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: un colegio genera pocos procesos por año |
| Decisión que respalda (decisión de ingeniería) | Asumir datos pequeños: reglas y rúbricas antes que ML |
| Nivel de confianza | MODERADA |

### S05 — Chen (2023)

| Campo | Contenido |
|---|---|
| Referencia | Chen, Z. (2023). Ethics and discrimination in artificial intelligence-enabled recruitment practices. *Humanities and Social Sciences Communications*. https://doi.org/10.1057/s41599-023-02079-x |
| Año | 2023 |
| Autores | Chen, Z. |
| Revista o conferencia | Humanities and Social Sciences Communications |
| DOI / URL | https://doi.org/10.1057/s41599-023-02079-x |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | A · búsqueda A |
| Avisos de Crossref | ninguno |
| Objetivo | Estudiar la discriminación algorítmica en reclutamiento y sus soluciones |
| Datos o población | Revisión de literatura y encuesta |
| Técnica | Revisión + teoría fundamentada |
| Variables o características | Género, raza, rasgos de personalidad |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | El sesgo proviene de datos limitados y del diseño; recomienda medidas técnicas y de gobernanza |
| Limitaciones | Método mixto con muestra no detallada en el resumen |
| Riesgos de sesgo | Datos históricos sesgados |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Combinar controles técnicos con gobernanza interna y supervisión externa |
| Nivel de confianza | LIMITADA |

### S06 — Langer et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Langer, M., König, C. J. y Papathanasiou, M. (2019). Highly automated job interviews: Acceptance under the influence of stakes. *International Journal of Selection and Assessment*. https://doi.org/10.1111/ijsa.12246 |
| Año | 2019 |
| Autores | Langer, M., König, C. J. y Papathanasiou, M. |
| Revista o conferencia | International Journal of Selection and Assessment |
| DOI / URL | https://doi.org/10.1111/ijsa.12246 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | A · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Medir la reacción de las personas a entrevistas altamente automatizadas |
| Datos o población | N = 123; experimento 2 × 2 preregistrado |
| Técnica | Experimento con viñetas en vídeo |
| Variables o características | Automatización (alta / videoconferencia) × consecuencias (selección / formación) |
| Métricas | Aceptación, presencia social, equidad percibida, controlabilidad |
| Resultados relevantes (evidencia) | La entrevista automatizada redujo la aceptación por menor presencia social y equidad percibida; en alto riesgo generó ambigüedad |
| Limitaciones | Observadores, no postulantes reales |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta: la entrevista del colegio debe seguir siendo humana |
| Decisión que respalda (decisión de ingeniería) | No automatizar la conducción de la entrevista |
| Nivel de confianza | MODERADA |

### S07 — Hickman et al. (2022)

| Campo | Contenido |
|---|---|
| Referencia | Hickman, L., Bosch, N., Ng, V., Saef, R., Tay, L. y Woo, S. E. (2022). Automated video interview personality assessments: Reliability, validity, and generalizability investigations. *Journal of Applied Psychology*. https://doi.org/10.1037/apl0000695 |
| Año | 2022 |
| Autores | Hickman, L., Bosch, N., Ng, V., Saef, R., Tay, L. y Woo, S. E. |
| Revista o conferencia | Journal of Applied Psychology |
| DOI / URL | https://doi.org/10.1037/apl0000695 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | T · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Evaluar fiabilidad y validez de evaluaciones de personalidad por entrevista en vídeo automatizada |
| Datos o población | Varias muestras (resumen parcial en OpenAlex) |
| Técnica | Modelos de ML sobre entrevistas en vídeo |
| Variables o características | Rasgos de personalidad (autoinforme vs. informe del entrevistador) |
| Métricas | Fiabilidad, validez convergente y discriminante, generalización |
| Resultados relevantes (evidencia) | Evidencia escasa de validez cuando se entrenan con autoinformes; mixta con informes del entrevistador |
| Limitaciones | Contextos de laboratorio y académicos |
| Riesgos de sesgo | Constructo psicológico inferido |
| Aplicabilidad al caso (inferencia del equipo) | Directa: sustenta no inferir personalidad |
| Decisión que respalda (decisión de ingeniería) | Prohibir puntuaciones de personalidad desde vídeo |
| Nivel de confianza | MODERADA |

### S08 — Barrett et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Barrett, L. F., Adolphs, R., Marsella, S., Martinez, A. M. y Pollak, S. D. (2019). Emotional Expressions Reconsidered: Challenges to Inferring Emotion From Human Facial Movements. *Psychological Science in the Public Interest*. https://doi.org/10.1177/1529100619832930 |
| Año | 2019 |
| Autores | Barrett, L. F., Adolphs, R., Marsella, S., Martinez, A. M. y Pollak, S. D. |
| Revista o conferencia | Psychological Science in the Public Interest |
| DOI / URL | https://doi.org/10.1177/1529100619832930 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | T · bola de nieve |
| Avisos de Crossref | correction |
| Objetivo | Examinar si la emoción puede inferirse de los movimientos faciales |
| Datos o población | Revisión de la evidencia científica sobre 6 categorías emocionales |
| Técnica | Revisión crítica amplia |
| Variables o características | Configuraciones faciales y emoción |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | La expresión de emociones varía mucho entre culturas, situaciones y personas; una misma configuración facial expresa varias emociones o algo distinto de una emoción |
| Limitaciones | Se centra en 6 emociones básicas |
| Riesgos de sesgo | Inferencias poco generalizables entre culturas |
| Aplicabilidad al caso (inferencia del equipo) | Directa: la evidencia no respalda que el reconocimiento de emociones en entrevistas sea fiable ni generalizable para un uso de alto impacto |
| Decisión que respalda (decisión de ingeniería) | Prohibir inferir emociones o estados desde rostro o voz |
| Nivel de confianza | FUERTE |

### S09 — Stark y Hoey (2021)

| Campo | Contenido |
|---|---|
| Referencia | Stark, L. y Hoey, J. (2021). The Ethics of Emotion in Artificial Intelligence Systems. *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3442188.3445939 |
| Año | 2021 |
| Autores | Stark, L. y Hoey, J. |
| Revista o conferencia | Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3442188.3445939 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | T · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Analizar los modelos conceptuales y datos proxy del reconocimiento automático de emociones |
| Datos o población | Análisis conceptual |
| Técnica | Taxonomía crítica |
| Variables o características | Modelos de emoción, datos proxy |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | No debe asumirse que estos sistemas producen una «verdad de terreno» sobre emociones |
| Limitaciones | Conceptual |
| Riesgos de sesgo | Proxies culturalmente sesgados |
| Aplicabilidad al caso (inferencia del equipo) | Directa |
| Decisión que respalda (decisión de ingeniería) | Misma decisión que S08 |
| Nivel de confianza | MODERADA |

### S10 — Koenecke et al. (2020)

| Campo | Contenido |
|---|---|
| Referencia | Koenecke, A., Nam, A., Lake, E., Nudell, J., Quartey, M., Mengesha, Z. et al. (2020). Racial disparities in automated speech recognition. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.1915768117 |
| Año | 2020 |
| Autores | Koenecke, A., Nam, A., Lake, E., Nudell, J., Quartey, M., Mengesha, Z. et al. |
| Revista o conferencia | Proceedings of the National Academy of Sciences |
| DOI / URL | https://doi.org/10.1073/pnas.1915768117 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | S · búsqueda T |
| Avisos de Crossref | ninguno |
| Objetivo | Medir disparidades raciales en reconocimiento automático del habla |
| Datos o población | 5 sistemas comerciales; entrevistas estructuradas con 42 hablantes blancos y 73 negros; 19,8 h |
| Técnica | Auditoría comparativa |
| Variables o características | Raza del hablante; frases idénticas |
| Métricas | WER |
| Resultados relevantes (evidencia) | WER promedio 0,35 en hablantes negros frente a 0,19 en blancos; la brecha se atribuye a los modelos acústicos |
| Limitaciones | Inglés de EE. UU.; sistemas de 2019 |
| Riesgos de sesgo | Disparidad por variedad dialectal |
| Aplicabilidad al caso (inferencia del equipo) | Alta: el STT puede degradar la evidencia de ciertos hablantes (p. ej., variedades del español andino) |
| Decisión que respalda (decisión de ingeniería) | Medir WER por variedad de habla antes de usar STT; revisión humana de transcripciones |
| Nivel de confianza | MODERADA |

### S11 — Wilson y Caliskan (2024)

| Campo | Contenido |
|---|---|
| Referencia | Wilson, K. y Caliskan, A. (2024). Gender, Race, and Intersectional Bias in Resume Screening via Language Model Retrieval. *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1609/aies.v7i1.31748 |
| Año | 2024 |
| Autores | Wilson, K. y Caliskan, A. |
| Revista o conferencia | Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society |
| DOI / URL | https://doi.org/10.1609/aies.v7i1.31748 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | E · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Auditar sesgos de modelos de embeddings en cribado de CV |
| Datos o población | >500 CV públicos, 500 descripciones de puesto, 9 ocupaciones |
| Técnica | Auditoría por recuperación (Massive Text Embeddings) |
| Variables o características | Nombres asociados a raza y género |
| Métricas | Tasa de preferencia por grupo |
| Resultados relevantes (evidencia) | Preferencia por nombres asociados a personas blancas en 85,1 % de los casos; hombres negros desfavorecidos hasta en el 100 % de los casos |
| Limitaciones | Nombres como proxy; EE. UU. |
| Riesgos de sesgo | Embeddings reproducen sesgos sociales |
| Aplicabilidad al caso (inferencia del equipo) | Directa para matching semántico |
| Decisión que respalda (decisión de ingeniería) | No usar similitud de embeddings como puntuación de candidatos sin auditoría; ocultar nombres |
| Nivel de confianza | MODERADA |

### S12 — Schmidt y Hunter (1998)

| Campo | Contenido |
|---|---|
| Referencia | Schmidt, F. L. y Hunter, J. E. (1998). The validity and utility of selection methods in personnel psychology: Practical and theoretical implications of 85 years of research findings. *Psychological Bulletin*. https://doi.org/10.1037/0033-2909.124.2.262 |
| Año | 1998 |
| Autores | Schmidt, F. L. y Hunter, J. E. |
| Revista o conferencia | Psychological Bulletin |
| DOI / URL | https://doi.org/10.1037/0033-2909.124.2.262 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Resumir 85 años de investigación sobre validez de métodos de selección |
| Datos o población | Metaanálisis de 19 métodos |
| Técnica | Síntesis metaanalítica |
| Variables o características | Métodos de selección y desempeño |
| Métricas | Validez de criterio |
| Resultados relevantes (evidencia) | Las combinaciones de capacidad cognitiva con muestra de trabajo, prueba de integridad o entrevista estructurada tuvieron las mayores validez (≈ 0,63–0,65) |
| Limitaciones | Correcciones de rango revisadas después por S13 |
| Riesgos de sesgo | Sobreestimación por correcciones |
| Aplicabilidad al caso (inferencia del equipo) | Media: contexto histórico |
| Decisión que respalda (decisión de ingeniería) | Usar con la revisión de S13 |
| Nivel de confianza | CONFLICTIVA |

### S13 — Sackett et al. (2022)

| Campo | Contenido |
|---|---|
| Referencia | Sackett, P. R., Zhang, C., Berry, C. M. y Lievens, F. (2022). Revisiting meta-analytic estimates of validity in personnel selection: Addressing systematic overcorrection for restriction of range. *Journal of Applied Psychology*. https://doi.org/10.1037/apl0000994 |
| Año | 2022 |
| Autores | Sackett, P. R., Zhang, C., Berry, C. M. y Lievens, F. |
| Revista o conferencia | Journal of Applied Psychology |
| DOI / URL | https://doi.org/10.1037/apl0000994 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar estimaciones metaanalíticas de validez en selección |
| Datos o población | Reanálisis de metaanálisis previos |
| Técnica | Revisión de correcciones por restricción de rango |
| Variables o características | Métodos de selección |
| Métricas | Validez de criterio |
| Resultados relevantes (evidencia) | Validez sobreestimada antes en 0,10–0,20; la entrevista estructurada queda en el primer lugar |
| Limitaciones | Sigue dependiendo de estudios primarios |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: sustenta la entrevista estructurada como método central |
| Decisión que respalda (decisión de ingeniería) | Basar la evaluación en entrevista estructurada con rúbrica |
| Nivel de confianza | FUERTE |

### S14 — McDaniel et al. (1994)

| Campo | Contenido |
|---|---|
| Referencia | McDaniel, M. A., Whetzel, D. L., Schmidt, F. L. y Maurer, S. D. (1994). The validity of employment interviews: A comprehensive review and meta-analysis. *Journal of Applied Psychology*. https://doi.org/10.1037/0021-9010.79.4.599 |
| Año | 1994 |
| Autores | McDaniel, M. A., Whetzel, D. L., Schmidt, F. L. y Maurer, S. D. |
| Revista o conferencia | Journal of Applied Psychology |
| DOI / URL | https://doi.org/10.1037/0021-9010.79.4.599 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · búsqueda D |
| Avisos de Crossref | ninguno |
| Objetivo | Metaanalizar la validez de la entrevista de empleo |
| Datos o población | 245 coeficientes; 86 311 personas |
| Técnica | Metaanálisis |
| Variables o características | Contenido, estructura, formato, criterio |
| Métricas | Validez |
| Resultados relevantes (evidencia) | La entrevista estructurada supera a la no estructurada; las situacionales superan a las psicológicas |
| Limitaciones | Datos antiguos |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Preguntas situacionales y de conducta pasada, no psicológicas |
| Nivel de confianza | FUERTE |

### S15 — Campion et al. (1997)

| Campo | Contenido |
|---|---|
| Referencia | Campion, M. A., Palmer, D. K. y Campion, J. E. (1997). A REVIEW OF STRUCTURE IN THE SELECTION INTERVIEW. *Personnel Psychology*. https://doi.org/10.1111/j.1744-6570.1997.tb00709.x |
| Año | 1997 |
| Autores | Campion, M. A., Palmer, D. K. y Campion, J. E. |
| Revista o conferencia | Personnel Psychology |
| DOI / URL | https://doi.org/10.1111/j.1744-6570.1997.tb00709.x |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Describir y evaluar los componentes de la estructura de una entrevista |
| Datos o población | Revisión de literatura |
| Técnica | Revisión narrativa |
| Variables o características | 15 componentes de estructura |
| Métricas | Fiabilidad, validez, reacciones |
| Resultados relevantes (evidencia) | La estructura mejora las propiedades psicométricas; identifica 15 componentes |
| Limitaciones | Narrativa |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: guía para la rúbrica de entrevista |
| Decisión que respalda (decisión de ingeniería) | Mismas preguntas, escalas ancladas y calificación por pregunta |
| Nivel de confianza | MODERADA |

### S16 — Levashina et al. (2013)

| Campo | Contenido |
|---|---|
| Referencia | Levashina, J., Hartwell, C. J., Morgeson, F. P. y Campion, M. A. (2013). The Structured Employment Interview: Narrative and Quantitative Review of the Research Literature. *Personnel Psychology*. https://doi.org/10.1111/peps.12052 |
| Año | 2013 |
| Autores | Levashina, J., Hartwell, C. J., Morgeson, F. P. y Campion, M. A. |
| Revista o conferencia | Personnel Psychology |
| DOI / URL | https://doi.org/10.1111/peps.12052 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar 20 años de investigación sobre entrevista estructurada |
| Datos o población | Revisión narrativa y metaanalítica |
| Técnica | Revisión mixta |
| Variables o características | Sesgo, gestión de impresiones, escalas, preguntas |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Mucho se sabe; 12 proposiciones y 19 preguntas abiertas |
| Limitaciones | Preguntas no resueltas |
| Riesgos de sesgo | Gestión de impresiones |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Escalas de calificación ancladas y sondeo controlado |
| Nivel de confianza | FUERTE |

### S17 — Campion et al. (2011)

| Campo | Contenido |
|---|---|
| Referencia | Campion, M. A., Fink, A. A., Ruggeberg, B. J., Carr, L., Phillips, G. M. y Odman, R. B. (2011). DOING COMPETENCIES WELL: BEST PRACTICES IN COMPETENCY MODELING. *Personnel Psychology*. https://doi.org/10.1111/j.1744-6570.2010.01207.x |
| Año | 2011 |
| Autores | Campion, M. A., Fink, A. A., Ruggeberg, B. J., Carr, L., Phillips, G. M. y Odman, R. B. |
| Revista o conferencia | Personnel Psychology |
| DOI / URL | https://doi.org/10.1111/j.1744-6570.2010.01207.x |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer buenas prácticas de modelado por competencias |
| Datos o población | Experiencia aplicada y académica |
| Técnica | Revisión de prácticas |
| Variables o características | Análisis, organización y uso de competencias |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | 20 buenas prácticas; diferencia y complementariedad con el análisis de puestos |
| Limitaciones | Recomendaciones de expertos |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: base de criterios por vacante |
| Decisión que respalda (decisión de ingeniería) | Competencias derivadas de análisis del puesto |
| Nivel de confianza | MODERADA |

### S18 — Sanchez y Levine (2012)

| Campo | Contenido |
|---|---|
| Referencia | Sanchez, J. I. y Levine, E. L. (2012). The Rise and Fall of Job Analysis and the Future of Work Analysis. *Annual Review of Psychology*. https://doi.org/10.1146/annurev-psych-120710-100401 |
| Año | 2012 |
| Autores | Sanchez, J. I. y Levine, E. L. |
| Revista o conferencia | Annual Review of Psychology |
| DOI / URL | https://doi.org/10.1146/annurev-psych-120710-100401 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar la evolución del análisis de puestos y el modelado de competencias |
| Datos o población | Revisión |
| Técnica | Revisión narrativa |
| Variables o características | Actividades, atributos, contexto de trabajo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Propone nuevas formas de análisis del trabajo y una agenda para competencias |
| Limitaciones | Narrativa |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Hacer análisis del puesto antes de definir criterios |
| Nivel de confianza | MODERADA |

### S19 — Smith y Kendall (1963)

| Campo | Contenido |
|---|---|
| Referencia | Smith, P. C. y Kendall, L. M. (1963). Retranslation of expectations: An approach to the construction of unambiguous anchors for rating scales. *Journal of Applied Psychology*. https://doi.org/10.1037/h0047060 |
| Año | 1963 |
| Autores | Smith, P. C. y Kendall, L. M. |
| Revista o conferencia | Journal of Applied Psychology |
| DOI / URL | https://doi.org/10.1037/h0047060 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer escalas de calificación ancladas en conducta (BARS) (sin resumen disponible; descripción general) |
| Datos o población | Desarrollo de escalas |
| Técnica | Retraducción de expectativas |
| Variables o características | Anclas conductuales |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Método para escalas con anclas conductuales no ambiguas |
| Limitaciones | Antiguo |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Usar anclas conductuales por nivel en cada criterio |
| Nivel de confianza | MODERADA |

### S20 — Shrout y Fleiss (1979)

| Campo | Contenido |
|---|---|
| Referencia | Shrout, P. E. y Fleiss, J. L. (1979). Intraclass correlations: Uses in assessing rater reliability. *Psychological Bulletin*. https://doi.org/10.1037/0033-2909.86.2.420 |
| Año | 1979 |
| Autores | Shrout, P. E. y Fleiss, J. L. |
| Revista o conferencia | Psychological Bulletin |
| DOI / URL | https://doi.org/10.1037/0033-2909.86.2.420 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Guiar la elección del coeficiente de correlación intraclase |
| Datos o población | Metodológico |
| Técnica | Estadística |
| Variables o características | n objetos calificados por k jueces |
| Métricas | ICC |
| Resultados relevantes (evidencia) | Seis formas de ICC según el modelo y el uso |
| Limitaciones | Metodológico |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta: fiabilidad entre evaluadores |
| Decisión que respalda (decisión de ingeniería) | Medir acuerdo entre evaluadores con ICC |
| Nivel de confianza | FUERTE |

### S21 — Koo y Li (2016)

| Campo | Contenido |
|---|---|
| Referencia | Koo, T. K. y Li, M. Y. (2016). A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. *Journal of Chiropractic Medicine*. https://doi.org/10.1016/j.jcm.2016.02.012 |
| Año | 2016 |
| Autores | Koo, T. K. y Li, M. Y. |
| Revista o conferencia | Journal of Chiropractic Medicine |
| DOI / URL | https://doi.org/10.1016/j.jcm.2016.02.012 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · bola de nieve |
| Avisos de Crossref | erratum |
| Objetivo | Guía de selección y reporte del ICC |
| Datos o población | Metodológico |
| Técnica | Estadística |
| Variables o características | Formas de ICC |
| Métricas | ICC e IC 95 % |
| Resultados relevantes (evidencia) | Hay 10 formas de ICC; debe reportarse modelo, tipo y definición |
| Limitaciones | Tiene una errata registrada en Crossref |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Reportar el ICC con su forma e intervalo |
| Nivel de confianza | FUERTE |

### S22 — Klassen y Kim (2019)

| Campo | Contenido |
|---|---|
| Referencia | Klassen, R. M. y Kim, L. E. (2019). Selecting teachers and prospective teachers: A meta-analysis. *Educational Research Review*. https://doi.org/10.1016/j.edurev.2018.12.003 |
| Año | 2019 |
| Autores | Klassen, R. M. y Kim, L. E. |
| Revista o conferencia | Educational Research Review |
| DOI / URL | https://doi.org/10.1016/j.edurev.2018.12.003 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Metaanalizar la validez predictiva de la selección de docentes |
| Datos o población | 32 estudios en condiciones reales |
| Técnica | Metaanálisis |
| Variables o características | Predictores académicos y no académicos |
| Métricas | Correlación con eficacia docente |
| Resultados relevantes (evidencia) | Efecto global pequeño pero significativo (r = 0,12) |
| Limitaciones | Medidas de eficacia heterogéneas |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: caso docente |
| Decisión que respalda (decisión de ingeniería) | Ser prudente con la capacidad predictiva en docentes; apoyo, no predicción |
| Nivel de confianza | FUERTE |

### S23 — Woods et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Woods, S. A., Ahmed, S., Nikolaou, I., Costa, A. C. y Anderson, N. R. (2019). Personnel selection in the digital age: a review of validity and applicant reactions, and future research challenges. *European Journal of Work and Organizational Psychology*. https://doi.org/10.1080/1359432x.2019.1681401 |
| Año | 2019 |
| Autores | Woods, S. A., Ahmed, S., Nikolaou, I., Costa, A. C. y Anderson, N. R. |
| Revista o conferencia | European Journal of Work and Organizational Psychology |
| DOI / URL | https://doi.org/10.1080/1359432x.2019.1681401 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · búsqueda C |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar procedimientos de selección digitales |
| Datos o población | Revisión focalizada |
| Técnica | Revisión |
| Variables o características | Aplicaciones en línea, pruebas, entrevistas digitales, gamificación, redes sociales |
| Métricas | Validez y reacciones |
| Resultados relevantes (evidencia) | Base de evidencia desigual; agenda de investigación |
| Limitaciones | Evidencia limitada |
| Riesgos de sesgo | Uso de redes sociales |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | No usar redes sociales del postulante |
| Nivel de confianza | MODERADA |

### S24 — Huffcutt et al. (2001)

| Campo | Contenido |
|---|---|
| Referencia | Huffcutt, A. I., Conway, J. M., Roth, P. L. y Stone, N. J. (2001). Identification and meta-analytic assessment of psychological constructs measured in employment interviews. *Journal of Applied Psychology*. https://doi.org/10.1037/0021-9010.86.5.897 |
| Año | 2001 |
| Autores | Huffcutt, A. I., Conway, J. M., Roth, P. L. y Stone, N. J. |
| Revista o conferencia | Journal of Applied Psychology |
| DOI / URL | https://doi.org/10.1037/0021-9010.86.5.897 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · búsqueda D |
| Avisos de Crossref | ninguno |
| Objetivo | Identificar qué constructos mide la entrevista |
| Datos o población | 338 calificaciones de 47 estudios |
| Técnica | Metaanálisis |
| Variables o características | Taxonomía de 7 constructos |
| Métricas | Frecuencia y validez |
| Resultados relevantes (evidencia) | La mayor validez de la entrevista estructurada se explica en parte por medir constructos más ligados al desempeño |
| Limitaciones | Datos de estudios publicados |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Definir qué competencia mide cada pregunta |
| Nivel de confianza | MODERADA |

### S25 — Zhu et al. (2018)

| Campo | Contenido |
|---|---|
| Referencia | Zhu, C., Zhu, H., Xiong, H., Ma, C., Xie, F., Ding, P. et al. (2018). Person-Job Fit. *ACM Transactions on Management Information Systems*. https://doi.org/10.1145/3234465 |
| Año | 2018 |
| Autores | Zhu, C., Zhu, H., Xiong, H., Ma, C., Xie, F., Ding, P. et al. |
| Revista o conferencia | ACM Transactions on Management Information Systems |
| DOI / URL | https://doi.org/10.1145/3234465 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | B · búsqueda B |
| Avisos de Crossref | ninguno |
| Objetivo | Modelar el ajuste persona-puesto con redes neuronales |
| Datos o población | Postulaciones históricas |
| Técnica | CNN bipartita (PJFNN) |
| Variables o características | Texto de requisitos y de experiencia |
| Métricas | Precisión de ajuste |
| Resultados relevantes (evidencia) | Estima el ajuste e identifica qué requisitos cumple el candidato |
| Limitaciones | Requiere grandes datos históricos |
| Riesgos de sesgo | Aprende de decisiones pasadas |
| Aplicabilidad al caso (inferencia del equipo) | Baja: no hay volumen de datos en el caso |
| Decisión que respalda (decisión de ingeniería) | Descartar deep learning de matching para el caso |
| Nivel de confianza | LIMITADA |

### S26 — Qin et al. (2018)

| Campo | Contenido |
|---|---|
| Referencia | Qin, C., Zhu, H., Xu, T., Zhu, C., Jiang, L., Chen, E. et al. (2018). Enhancing Person-Job Fit for Talent Recruitment. *The 41st International ACM SIGIR Conference on Research &amp; Development in Information Retrieval*. https://doi.org/10.1145/3209978.3210025 |
| Año | 2018 |
| Autores | Qin, C., Zhu, H., Xu, T., Zhu, C., Jiang, L., Chen, E. et al. |
| Revista o conferencia | The 41st International ACM SIGIR Conference on Research &amp; Development in Information Retrieval |
| DOI / URL | https://doi.org/10.1145/3209978.3210025 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | B · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Ajuste persona-puesto consciente de habilidades con mejor interpretación |
| Datos o población | Postulaciones históricas |
| Técnica | Red neuronal con atención (APJFNN) |
| Variables o características | Representaciones de requisitos y experiencia |
| Métricas | Precisión |
| Resultados relevantes (evidencia) | Mejora la interpretación del ajuste frente a modelos previos |
| Limitaciones | Datos de una plataforma |
| Riesgos de sesgo | Etiquetas de decisiones pasadas |
| Aplicabilidad al caso (inferencia del equipo) | Baja por datos |
| Decisión que respalda (decisión de ingeniería) | Igual que S25 |
| Nivel de confianza | LIMITADA |

### S27 — Freire y de Castro (2020)

| Campo | Contenido |
|---|---|
| Referencia | Freire, M. N. y de Castro, L. N. (2020). e-Recruitment recommender systems: a systematic review. *Knowledge and Information Systems*. https://doi.org/10.1007/s10115-020-01522-8 |
| Año | 2020 |
| Autores | Freire, M. N. y de Castro, L. N. |
| Revista o conferencia | Knowledge and Information Systems |
| DOI / URL | https://doi.org/10.1007/s10115-020-01522-8 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | H · búsqueda H |
| Avisos de Crossref | ninguno |
| Objetivo | Revisión sistemática de recomendadores de e-recruitment (sin resumen disponible; descripción general) |
| Datos o población | Literatura |
| Técnica | Revisión sistemática |
| Variables o características | Enfoques de recomendación |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Panorama de técnicas y retos |
| Limitaciones | Ver la publicación |
| Riesgos de sesgo | Varios |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Contexto para F40 |
| Nivel de confianza | MODERADA |

### S28 — Mashayekhi et al. (2024)

| Campo | Contenido |
|---|---|
| Referencia | Mashayekhi, Y., Li, N., Kang, B., Lijffijt, J. y De Bie, T. (2024). A Challenge-based Survey of E-recruitment Recommendation Systems. *ACM Computing Surveys*. https://doi.org/10.1145/3659942 |
| Año | 2024 |
| Autores | Mashayekhi, Y., Li, N., Kang, B., Lijffijt, J. y De Bie, T. |
| Revista o conferencia | ACM Computing Surveys |
| DOI / URL | https://doi.org/10.1145/3659942 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | H · búsqueda H |
| Avisos de Crossref | ninguno |
| Objetivo | Identificar retos de los recomendadores de e-recruitment |
| Datos o población | Literatura |
| Técnica | Revisión por retos |
| Variables o características | Retos: datos, bidireccionalidad, equidad, explicabilidad |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Organiza la literatura por retos prácticos |
| Limitaciones | Revisión |
| Riesgos de sesgo | Equidad e impacto en carreras |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Tratar equidad y explicación como requisitos del ranking |
| Nivel de confianza | MODERADA |

### S29 — Zhang et al. (2022)

| Campo | Contenido |
|---|---|
| Referencia | Zhang, M., Jensen, K., Sonniks, S. y Plank, B. (2022). SkillSpan: Hard and Soft Skill Extraction from English Job Postings. *Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*. https://doi.org/10.18653/v1/2022.naacl-main.366 |
| Año | 2022 |
| Autores | Zhang, M., Jensen, K., Sonniks, S. y Plank, B. |
| Revista o conferencia | Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies |
| DOI / URL | https://doi.org/10.18653/v1/2022.naacl-main.366 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | G · búsqueda G |
| Avisos de Crossref | ninguno |
| Objetivo | Extraer habilidades duras y blandas de avisos de empleo (sin resumen disponible; descripción general) |
| Datos o población | Corpus anotado de avisos en inglés |
| Técnica | Etiquetado de secuencias con modelos tipo BERT |
| Variables o características | Tramos de habilidad |
| Métricas | F1 por tramo |
| Resultados relevantes (evidencia) | Conjunto de datos y referencias para extracción de habilidades |
| Limitaciones | Inglés; avisos, no CV |
| Riesgos de sesgo | Anotación subjetiva de habilidades blandas |
| Aplicabilidad al caso (inferencia del equipo) | Media: la extracción en español requiere datos propios |
| Decisión que respalda (decisión de ingeniería) | Extracción de habilidades como sugerencia revisada por humanos |
| Nivel de confianza | MODERADA |

### S30 — Khaouja et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Khaouja, I., Kassou, I. y Ghogho, M. (2021). A Survey on Skill Identification From Online Job Ads. *IEEE Access*. https://doi.org/10.1109/access.2021.3106120 |
| Año | 2021 |
| Autores | Khaouja, I., Kassou, I. y Ghogho, M. |
| Revista o conferencia | IEEE Access |
| DOI / URL | https://doi.org/10.1109/access.2021.3106120 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | G · búsqueda G |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar la identificación de habilidades en avisos de empleo |
| Datos o población | 108 artículos |
| Técnica | Revisión sistemática |
| Variables o características | Bases de habilidades, métodos, granularidad |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Clasifica métodos y aplicaciones; retos abiertos |
| Limitaciones | Avisos, no CV |
| Riesgos de sesgo | Taxonomías no neutrales |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Usar una taxonomía explícita (p. ej., ESCO) si se extraen habilidades |
| Nivel de confianza | MODERADA |

### S31 — Reimers y Gurevych (2019)

| Campo | Contenido |
|---|---|
| Referencia | Reimers, N. y Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*. https://doi.org/10.18653/v1/D19-1410 |
| Año | 2019 |
| Autores | Reimers, N. y Gurevych, I. |
| Revista o conferencia | Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) |
| DOI / URL | https://doi.org/10.18653/v1/D19-1410 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | F · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Obtener embeddings de oraciones eficientes (sin resumen disponible; descripción general) |
| Datos o población | Corpus de similitud y NLI |
| Técnica | Redes siamesas sobre BERT (SBERT) |
| Variables o características | Pares de oraciones |
| Métricas | Correlación con similitud humana |
| Resultados relevantes (evidencia) | Embeddings comparables por coseno con mucho menor costo que comparar con BERT completo |
| Limitaciones | Similitud general, no ajuste laboral |
| Riesgos de sesgo | Hereda sesgos del preentrenamiento (ver S11) |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Similitud semántica solo para encontrar evidencia, no para puntuar |
| Nivel de confianza | FUERTE |

### S32 — Blodgett et al. (2020)

| Campo | Contenido |
|---|---|
| Referencia | Blodgett, S. L., Barocas, S., Daumé III, H. y Wallach, H. (2020). Language (Technology) is Power: A Critical Survey of “Bias” in NLP. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*. https://doi.org/10.18653/v1/2020.acl-main.485 |
| Año | 2020 |
| Autores | Blodgett, S. L., Barocas, S., Daumé III, H. y Wallach, H. |
| Revista o conferencia | Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics |
| DOI / URL | https://doi.org/10.18653/v1/2020.acl-main.485 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | E · búsqueda E |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar críticamente cómo se estudia el «sesgo» en NLP |
| Datos o población | 146 artículos |
| Técnica | Revisión crítica |
| Variables o características | Motivaciones y técnicas de medición del sesgo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Motivaciones vagas y técnicas poco alineadas con ellas; propone tres recomendaciones |
| Limitaciones | Revisión |
| Riesgos de sesgo | Sesgo social en lenguaje |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Definir qué daño se mide y a quién afecta antes de medir sesgo |
| Nivel de confianza | MODERADA |

### S33 — Bender y Friedman (2018)

| Campo | Contenido |
|---|---|
| Referencia | Bender, E. M. y Friedman, B. (2018). Data Statements for Natural Language Processing: Toward Mitigating System Bias and Enabling Better Science. *Transactions of the Association for Computational Linguistics*. https://doi.org/10.1162/tacl_a_00041 |
| Año | 2018 |
| Autores | Bender, E. M. y Friedman, B. |
| Revista o conferencia | Transactions of the Association for Computational Linguistics |
| DOI / URL | https://doi.org/10.1162/tacl_a_00041 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | E · búsqueda E |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer «data statements» para NLP |
| Datos o población | Propuesta |
| Técnica | Práctica de documentación |
| Variables o características | Población, variedad lingüística, anotadores |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Documentar datos mejora generalización y reduce exclusión |
| Limitaciones | Propuesta normativa |
| Riesgos de sesgo | Variedades lingüísticas |
| Aplicabilidad al caso (inferencia del equipo) | Alta (español andino) |
| Decisión que respalda (decisión de ingeniería) | Documentar variedad de habla y texto en el dataset card |
| Nivel de confianza | MODERADA |

### S34 — Ji et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y. et al. (2023). Survey of Hallucination in Natural Language Generation. *ACM Computing Surveys*. https://doi.org/10.1145/3571730 |
| Año | 2023 |
| Autores | Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y. et al. |
| Revista o conferencia | ACM Computing Surveys |
| DOI / URL | https://doi.org/10.1145/3571730 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | E · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar la alucinación en generación de lenguaje |
| Datos o población | Literatura |
| Técnica | Revisión |
| Variables o características | Tareas de generación |
| Métricas | Métricas de alucinación |
| Resultados relevantes (evidencia) | La generación neuronal es propensa a alucinar; métodos de medición y mitigación |
| Limitaciones | Previa a los LLM más recientes |
| Riesgos de sesgo | Información falsa |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta para resúmenes y explicaciones con LLM |
| Decisión que respalda (decisión de ingeniería) | Toda salida de LLM debe citar la evidencia de origen y validarse |
| Nivel de confianza | FUERTE |

### S35 — Bender et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Bender, E. M., Gebru, T., McMillan-Major, A. y Shmitchell, S. (2021). On the Dangers of Stochastic Parrots. *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3442188.3445922 |
| Año | 2021 |
| Autores | Bender, E. M., Gebru, T., McMillan-Major, A. y Shmitchell, S. |
| Revista o conferencia | Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3442188.3445922 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | E · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Analizar riesgos de modelos de lenguaje muy grandes |
| Datos o población | Ensayo crítico |
| Técnica | Análisis |
| Variables o características | Datos, costo, sesgo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Recomienda documentar datos y evaluar riesgos antes de desarrollar |
| Limitaciones | Posicionamiento |
| Riesgos de sesgo | Sesgos del corpus web |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Evaluar riesgos antes de adoptar LLM |
| Nivel de confianza | MODERADA |

### S36 — Zheng et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Zheng, L., Chiang, W. L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y. et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *arXiv*. https://doi.org/10.48550/arXiv.2306.05685 |
| Año | 2023 |
| Autores | Zheng, L., Chiang, W. L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y. et al. |
| Revista o conferencia | arXiv |
| DOI / URL | https://doi.org/10.48550/arXiv.2306.05685 |
| Tipo de publicación | Preprint (arXiv) |
| Revisión por pares | No (preprint); publicado en NeurIPS 2023 |
| Tema y origen | T · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Evaluar el uso de LLM como jueces |
| Datos o población | MT-Bench y Chatbot Arena |
| Técnica | LLM como evaluador |
| Variables o características | Preguntas abiertas |
| Métricas | Acuerdo con preferencias humanas |
| Resultados relevantes (evidencia) | Acuerdo superior al 80 % con preferencias humanas; sesgos de posición, verbosidad y autopromoción |
| Limitaciones | Tareas de chat, no evaluación de personas |
| Riesgos de sesgo | Sesgos del juez |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | No usar LLM como juez de candidatos; como mucho, ayuda para revisar consistencia de rúbricas |
| Nivel de confianza | MODERADA |

### S37 — Xu et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Xu, Y., Xu, Y., Lv, T., Cui, L., Wei, F., Wang, G. et al. (2021). LayoutLMv2: Multi-modal Pre-training for Visually-rich Document Understanding. *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)*. https://doi.org/10.18653/v1/2021.acl-long.201 |
| Año | 2021 |
| Autores | Xu, Y., Xu, Y., Lv, T., Cui, L., Wei, F., Wang, G. et al. |
| Revista o conferencia | Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers) |
| DOI / URL | https://doi.org/10.18653/v1/2021.acl-long.201 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | R · búsqueda R |
| Avisos de Crossref | ninguno |
| Objetivo | Preentrenamiento multimodal para comprender documentos (sin resumen disponible; descripción general) |
| Datos o población | Documentos escaneados y digitales |
| Técnica | Transformer de texto, disposición e imagen (LayoutLMv2) |
| Variables o características | Texto, posición, imagen |
| Métricas | Exactitud en tareas |
| Resultados relevantes (evidencia) | Mejora tareas de comprensión de documentos visualmente ricos |
| Limitaciones | Costo computacional |
| Riesgos de sesgo | No relevante |
| Aplicabilidad al caso (inferencia del equipo) | Baja: los CV del caso son digitales |
| Decisión que respalda (decisión de ingeniería) | OCR/disposición solo si hay escaneados |
| Nivel de confianza | MODERADA |

### S38 — Radford et al. (2022)

| Campo | Contenido |
|---|---|
| Referencia | Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C. y Sutskever, I. (2022). Robust Speech Recognition via Large-Scale Weak Supervision. *arXiv*. https://doi.org/10.48550/arXiv.2212.04356 |
| Año | 2022 |
| Autores | Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C. y Sutskever, I. |
| Revista o conferencia | arXiv |
| DOI / URL | https://doi.org/10.48550/arXiv.2212.04356 |
| Tipo de publicación | Preprint (arXiv) |
| Revisión por pares | No (preprint); publicado en ICML 2023 |
| Tema y origen | S · búsqueda S |
| Avisos de Crossref | ninguno |
| Objetivo | Reconocimiento de voz robusto con supervisión débil |
| Datos o población | 680 000 h de audio multilingüe |
| Técnica | Transformer codificador-decodificador (Whisper) |
| Variables o características | Audio |
| Métricas | WER |
| Resultados relevantes (evidencia) | Generaliza bien en cero disparos y se acerca a la robustez humana |
| Limitaciones | Evaluación en benchmarks |
| Riesgos de sesgo | Rendimiento desigual por idioma y variedad |
| Aplicabilidad al caso (inferencia del equipo) | Alta: candidato STT local |
| Decisión que respalda (decisión de ingeniería) | Evaluar Whisper con audio propio y revisión humana |
| Nivel de confianza | MODERADA |

### S39 — Saaty (1990)

| Campo | Contenido |
|---|---|
| Referencia | Saaty, T. L. (1990). How to make a decision: The analytic hierarchy process. *European Journal of Operational Research*. https://doi.org/10.1016/0377-2217(90)90057-I |
| Año | 1990 |
| Autores | Saaty, T. L. |
| Revista o conferencia | European Journal of Operational Research |
| DOI / URL | https://doi.org/10.1016/0377-2217(90)90057-I |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | I · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Presentar el proceso analítico jerárquico (AHP) (sin resumen disponible; descripción general) |
| Datos o población | Método |
| Técnica | AHP |
| Variables o características | Comparaciones por pares de criterios |
| Métricas | Razón de consistencia |
| Resultados relevantes (evidencia) | Método para derivar pesos de criterios |
| Limitaciones | Sensible a la elicitación |
| Riesgos de sesgo | Pesos subjetivos |
| Aplicabilidad al caso (inferencia del equipo) | Alta: pesos por vacante |
| Decisión que respalda (decisión de ingeniería) | Derivar pesos con método explícito y registrado |
| Nivel de confianza | MODERADA |

### S40 — Kelemenis y Askounis (2010)

| Campo | Contenido |
|---|---|
| Referencia | Kelemenis, A. y Askounis, D. (2010). A new TOPSIS-based multi-criteria approach to personnel selection. *Expert Systems with Applications*. https://doi.org/10.1016/j.eswa.2009.12.013 |
| Año | 2010 |
| Autores | Kelemenis, A. y Askounis, D. |
| Revista o conferencia | Expert Systems with Applications |
| DOI / URL | https://doi.org/10.1016/j.eswa.2009.12.013 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | I · búsqueda I |
| Avisos de Crossref | ninguno |
| Objetivo | Aplicar TOPSIS a la selección de personal (sin resumen disponible; descripción general) |
| Datos o población | Caso de aplicación |
| Técnica | TOPSIS |
| Variables o características | Criterios ponderados |
| Métricas | Ordenamiento |
| Resultados relevantes (evidencia) | Enfoque multicriterio para ordenar candidatos |
| Limitaciones | Caso único |
| Riesgos de sesgo | Pesos subjetivos |
| Aplicabilidad al caso (inferencia del equipo) | Media: el ranking actual ya es una suma ponderada (RF-21) |
| Decisión que respalda (decisión de ingeniería) | Mantener la suma ponderada transparente; MCDM complejo no aporta evidencia adicional |
| Nivel de confianza | LIMITADA |

### S41 — Mehrabi et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. y Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3457607 |
| Año | 2021 |
| Autores | Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. y Galstyan, A. |
| Revista o conferencia | ACM Computing Surveys |
| DOI / URL | https://doi.org/10.1145/3457607 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | K · búsqueda K |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar sesgo y equidad en ML |
| Datos o población | Literatura |
| Técnica | Revisión |
| Variables o características | Fuentes de sesgo, definiciones |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Taxonomía de sesgos y definiciones de equidad |
| Limitaciones | Revisión |
| Riesgos de sesgo | Varios |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Catálogo de sesgos para el análisis de riesgos |
| Nivel de confianza | MODERADA |

### S42 — Barocas y Selbst (2016)

| Campo | Contenido |
|---|---|
| Referencia | Barocas, S. y Selbst, A. D. (2016). Big Data's Disparate Impact. *California Law Review*. https://doi.org/10.15779/Z38BG31 |
| Año | 2016 |
| Autores | Barocas, S. y Selbst, A. D. |
| Revista o conferencia | California Law Review |
| DOI / URL | https://doi.org/10.15779/Z38BG31 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Revisión editorial (revista jurídica) |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Analizar el impacto dispar de la minería de datos |
| Datos o población | Análisis jurídico |
| Técnica | Análisis |
| Variables o características | Datos históricos |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Los algoritmos heredan prejuicios de decisiones previas y patrones de exclusión |
| Limitaciones | Derecho de EE. UU. |
| Riesgos de sesgo | Sesgo histórico |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | No usar decisiones históricas de contratación como verdad |
| Nivel de confianza | MODERADA |

### S43 — Hardt et al. (2016)

| Campo | Contenido |
|---|---|
| Referencia | Hardt, M., Price, E. y Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *arXiv*. https://doi.org/10.48550/arXiv.1610.02413 |
| Año | 2016 |
| Autores | Hardt, M., Price, E. y Srebro, N. |
| Revista o conferencia | arXiv |
| DOI / URL | https://doi.org/10.48550/arXiv.1610.02413 |
| Tipo de publicación | Preprint (arXiv) |
| Revisión por pares | No (preprint); publicado en NeurIPS 2016 |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Definir igualdad de oportunidades en aprendizaje supervisado |
| Datos o población | Teórico con caso |
| Técnica | Post-procesamiento |
| Variables o características | Predictor, objetivo, atributo protegido |
| Métricas | Tasas de error por grupo |
| Resultados relevantes (evidencia) | Define igualdad de oportunidades/probabilidades y cómo ajustarlas; límites de las medidas «oblivious» |
| Limitaciones | Requiere el atributo protegido y una etiqueta confiable |
| Riesgos de sesgo | Etiqueta sesgada |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Las métricas de equidad requieren etiquetas válidas que el caso no tiene |
| Nivel de confianza | FUERTE |

### S44 — Kleinberg et al. (2017)

| Campo | Contenido |
|---|---|
| Referencia | Kleinberg, J., Mullainathan, S. y Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Schloss Dagstuhl – Leibniz-Zentrum für Informatik*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 |
| Año | 2017 |
| Autores | Kleinberg, J., Mullainathan, S. y Raghavan, M. |
| Revista o conferencia | Schloss Dagstuhl – Leibniz-Zentrum für Informatik |
| DOI / URL | https://doi.org/10.4230/LIPIcs.ITCS.2017.43 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Formalizar compromisos entre condiciones de equidad |
| Datos o población | Teórico |
| Técnica | Demostración |
| Variables o características | Calibración y equilibrio de errores |
| Métricas | Formal |
| Resultados relevantes (evidencia) | Salvo casos especiales, no pueden cumplirse a la vez |
| Limitaciones | Teórico |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Elegir y justificar una métrica de equidad; no prometer todas |
| Nivel de confianza | FUERTE |

### S45 — Chouldechova (2017)

| Campo | Contenido |
|---|---|
| Referencia | Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*. https://doi.org/10.1089/big.2016.0047 |
| Año | 2017 |
| Autores | Chouldechova, A. |
| Revista o conferencia | Big Data |
| DOI / URL | https://doi.org/10.1089/big.2016.0047 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Estudiar criterios de equidad en instrumentos de riesgo |
| Datos o población | Teórico con datos de reincidencia |
| Técnica | Análisis formal y empírico |
| Variables o características | Tasas base por grupo |
| Métricas | Error por grupo |
| Resultados relevantes (evidencia) | Los criterios no pueden satisfacerse a la vez si las tasas base difieren |
| Limitaciones | Dominio penal |
| Riesgos de sesgo | Tasas base |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Igual que S44 |
| Nivel de confianza | FUERTE |

### S46 — Friedler et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Friedler, S. A., Scheidegger, C., Venkatasubramanian, S., Choudhary, S., Hamilton, E. P. y Roth, D. (2019). A comparative study of fairness-enhancing interventions in machine learning. *Proceedings of the Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3287560.3287589 |
| Año | 2019 |
| Autores | Friedler, S. A., Scheidegger, C., Venkatasubramanian, S., Choudhary, S., Hamilton, E. P. y Roth, D. |
| Revista o conferencia | Proceedings of the Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3287560.3287589 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | K · búsqueda K |
| Avisos de Crossref | ninguno |
| Objetivo | Comparar intervenciones para mejorar la equidad |
| Datos o población | Varios conjuntos de datos |
| Técnica | Benchmark |
| Variables o características | Algoritmos de equidad |
| Métricas | Equidad y exactitud |
| Resultados relevantes (evidencia) | Resultados sensibles al preprocesamiento y a la partición |
| Limitaciones | Datasets de referencia |
| Riesgos de sesgo | Inestabilidad de métricas |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Reportar variabilidad, no un solo número |
| Nivel de confianza | MODERADA |

### S47 — Suresh y Guttag (2021)

| Campo | Contenido |
|---|---|
| Referencia | Suresh, H. y Guttag, J. (2021). A Framework for Understanding Sources of Harm throughout the Machine Learning Life Cycle. *Equity and Access in Algorithms, Mechanisms, and Optimization*. https://doi.org/10.1145/3465416.3483305 |
| Año | 2021 |
| Autores | Suresh, H. y Guttag, J. |
| Revista o conferencia | Equity and Access in Algorithms, Mechanisms, and Optimization |
| DOI / URL | https://doi.org/10.1145/3465416.3483305 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Identificar fuentes de daño en el ciclo de vida del ML |
| Datos o población | Marco conceptual |
| Técnica | Taxonomía |
| Variables o características | 7 fuentes de daño |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Sesgos histórico, de representación, de medición, etc. |
| Limitaciones | Conceptual |
| Riesgos de sesgo | Todos |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta |
| Decisión que respalda (decisión de ingeniería) | Usar las 7 fuentes como lista de riesgos de F34 |
| Nivel de confianza | MODERADA |

### S48 — Obermeyer et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Obermeyer, Z., Powers, B., Vogeli, C. y Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. https://doi.org/10.1126/science.aax2342 |
| Año | 2019 |
| Autores | Obermeyer, Z., Powers, B., Vogeli, C. y Mullainathan, S. |
| Revista o conferencia | Science |
| DOI / URL | https://doi.org/10.1126/science.aax2342 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | K · búsqueda A |
| Avisos de Crossref | ninguno |
| Objetivo | Medir sesgo racial en un algoritmo de salud |
| Datos o población | Algoritmo comercial; millones de pacientes |
| Técnica | Auditoría |
| Variables o características | Costo de salud como proxy |
| Métricas | Tasa de derivación |
| Resultados relevantes (evidencia) | Usar el costo como proxy de la necesidad creó sesgo racial; corregirlo eleva la ayuda a pacientes negros de 17,7 % a 46,5 % |
| Limitaciones | Dominio de salud |
| Riesgos de sesgo | Sesgo de proxy de la etiqueta |
| Aplicabilidad al caso (inferencia del equipo) | Alta por analogía |
| Decisión que respalda (decisión de ingeniería) | Revisar qué representa la etiqueta (p. ej., «contratado» ≠ «idóneo») |
| Nivel de confianza | FUERTE |

### S49 — Bellamy et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Bellamy, R. K. E., Dey, K., Hind, M., Hoffman, S. C., Houde, S., Kannan, K. et al. (2019). AI Fairness 360: An extensible toolkit for detecting and mitigating algorithmic bias. *IBM Journal of Research and Development*. https://doi.org/10.1147/JRD.2019.2942287 |
| Año | 2019 |
| Autores | Bellamy, R. K. E., Dey, K., Hind, M., Hoffman, S. C., Houde, S., Kannan, K. et al. |
| Revista o conferencia | IBM Journal of Research and Development |
| DOI / URL | https://doi.org/10.1147/JRD.2019.2942287 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Presentar el toolkit AI Fairness 360 |
| Datos o población | Software |
| Técnica | Biblioteca |
| Variables o características | Métricas y mitigaciones |
| Métricas | Métricas de equidad |
| Resultados relevantes (evidencia) | Toolkit Apache 2.0 con métricas, explicaciones y mitigaciones |
| Limitaciones | Herramienta |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Candidato de herramienta (ver análisis de herramientas) |
| Nivel de confianza | MODERADA |

### S50 — Holstein et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Holstein, K., Wortman Vaughan, J., Daumé, H., Dudik, M. y Wallach, H. (2019). Improving Fairness in Machine Learning Systems. *Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3290605.3300830 |
| Año | 2019 |
| Autores | Holstein, K., Wortman Vaughan, J., Daumé, H., Dudik, M. y Wallach, H. |
| Revista o conferencia | Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems |
| DOI / URL | https://doi.org/10.1145/3290605.3300830 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | K · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Identificar necesidades de practicantes para ML más justo |
| Datos o población | 35 entrevistas y 267 encuestados |
| Técnica | Entrevistas y encuesta |
| Variables o características | Retos de equipos de producto |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Desajuste entre retos reales y soluciones de investigación |
| Limitaciones | Empresas de tecnología |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Planificar recolección de datos de auditoría desde el diseño |
| Nivel de confianza | MODERADA |

### S51 — Rudin (2019)

| Campo | Contenido |
|---|---|
| Referencia | Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence*. https://doi.org/10.1038/s42256-019-0048-x |
| Año | 2019 |
| Autores | Rudin, C. |
| Revista o conferencia | Nature Machine Intelligence |
| DOI / URL | https://doi.org/10.1038/s42256-019-0048-x |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | J · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Argumentar contra explicar cajas negras en decisiones de alto impacto (sin resumen disponible; descripción general) |
| Datos o población | Ensayo |
| Técnica | Análisis |
| Variables o características | Modelos interpretables |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Recomienda modelos interpretables en lugar de explicaciones post hoc en alto impacto |
| Limitaciones | Posición |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: selección es alto impacto |
| Decisión que respalda (decisión de ingeniería) | Preferir modelos/reglas interpretables |
| Nivel de confianza | MODERADA |

### S52 — Ribeiro et al. (2016)

| Campo | Contenido |
|---|---|
| Referencia | Ribeiro, M. T., Singh, S. y Guestrin, C. (2016). "Why Should I Trust You?". *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/2939672.2939778 |
| Año | 2016 |
| Autores | Ribeiro, M. T., Singh, S. y Guestrin, C. |
| Revista o conferencia | Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining |
| DOI / URL | https://doi.org/10.1145/2939672.2939778 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | J · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Explicar predicciones de cualquier clasificador (LIME) |
| Datos o población | Experimentos con usuarios |
| Técnica | LIME |
| Variables o características | Explicaciones locales |
| Métricas | Confianza del usuario |
| Resultados relevantes (evidencia) | Explicaciones locales ayudan a evaluar la confianza |
| Limitaciones | Explicaciones aproximadas e inestables |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Baja |
| Decisión que respalda (decisión de ingeniería) | No usar LIME como explicación al usuario final |
| Nivel de confianza | MODERADA |

### S53 — Lundberg y Lee (2017)

| Campo | Contenido |
|---|---|
| Referencia | Lundberg, S. y Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. *arXiv*. https://doi.org/10.48550/arXiv.1705.07874 |
| Año | 2017 |
| Autores | Lundberg, S. y Lee, S. I. |
| Revista o conferencia | arXiv |
| DOI / URL | https://doi.org/10.48550/arXiv.1705.07874 |
| Tipo de publicación | Preprint (arXiv) |
| Revisión por pares | No (preprint); publicado en NeurIPS 2017 |
| Tema y origen | J · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Unificar métodos de atribución (SHAP) |
| Datos o población | Teórico y experimentos |
| Técnica | Valores de Shapley |
| Variables o características | Importancia por característica |
| Métricas | Consistencia |
| Resultados relevantes (evidencia) | Marco unificado de importancia aditiva |
| Limitaciones | Asume independencia en algunas variantes; costo |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | SHAP solo para depuración interna si hubiera modelo |
| Nivel de confianza | MODERADA |

### S54 — Wachter et al. (2017)

| Campo | Contenido |
|---|---|
| Referencia | Wachter, S., Mittelstadt, B. y Russell, C. (2017). Counterfactual Explanations Without Opening the Black Box: Automated Decisions and the GDPR. *SSRN Electronic Journal*. https://doi.org/10.2139/ssrn.3063289 |
| Año | 2017 |
| Autores | Wachter, S., Mittelstadt, B. y Russell, C. |
| Revista o conferencia | SSRN Electronic Journal |
| DOI / URL | https://doi.org/10.2139/ssrn.3063289 |
| Tipo de publicación | Documento de trabajo (SSRN) |
| Revisión por pares | No (documento de trabajo en SSRN); publicado luego en Harvard Journal of Law & Technology |
| Tema y origen | J · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer explicaciones contrafactuales (sin resumen disponible; descripción general) |
| Datos o población | Análisis jurídico-técnico |
| Técnica | Contrafactuales |
| Variables o características | Cambios mínimos |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Explicar qué cambio mínimo alteraría el resultado sin abrir la caja negra |
| Limitaciones | Puede sugerir cambios no accionables |
| Riesgos de sesgo | Atributos protegidos |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Explicar por criterios y evidencia faltante |
| Nivel de confianza | MODERADA |

### S55 — Miller (2019)

| Campo | Contenido |
|---|---|
| Referencia | Miller, T. (2019). Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence*. https://doi.org/10.1016/j.artint.2018.07.007 |
| Año | 2019 |
| Autores | Miller, T. |
| Revista o conferencia | Artificial Intelligence |
| DOI / URL | https://doi.org/10.1016/j.artint.2018.07.007 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | J · búsqueda J |
| Avisos de Crossref | ninguno |
| Objetivo | Aportar la perspectiva de ciencias sociales sobre explicaciones (sin resumen disponible; descripción general) |
| Datos o población | Revisión |
| Técnica | Revisión |
| Variables o características | Explicaciones contrastivas y sociales |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Las personas prefieren explicaciones contrastivas, selectivas y sociales |
| Limitaciones | Revisión |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Explicar «por qué este nivel y no otro» con evidencia |
| Nivel de confianza | MODERADA |

### S56 — Bhatt et al. (2020)

| Campo | Contenido |
|---|---|
| Referencia | Bhatt, U., Xiang, A., Sharma, S., Weller, A., Taly, A., Jia, Y. et al. (2020). Explainable machine learning in deployment. *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3351095.3375624 |
| Año | 2020 |
| Autores | Bhatt, U., Xiang, A., Sharma, S., Weller, A., Taly, A., Jia, Y. et al. |
| Revista o conferencia | Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3351095.3375624 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | J · búsqueda P |
| Avisos de Crossref | ninguno |
| Objetivo | Estudiar cómo se usa la explicabilidad en organizaciones |
| Datos o población | Entrevistas en organizaciones |
| Técnica | Estudio cualitativo |
| Variables o características | Usos de explicaciones |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | La mayoría de despliegues sirven a ingenieros para depurar, no a los afectados |
| Limitaciones | Muestra limitada |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Diseñar explicaciones para el evaluador humano y el postulante |
| Nivel de confianza | MODERADA |

### S57 — Green y Chen (2019)

| Campo | Contenido |
|---|---|
| Referencia | Green, B. y Chen, Y. (2019). Disparate Interactions. *Proceedings of the Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3287560.3287563 |
| Año | 2019 |
| Autores | Green, B. y Chen, Y. |
| Revista o conferencia | Proceedings of the Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3287560.3287563 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | M · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Estudiar cómo las personas usan evaluaciones de riesgo |
| Datos o población | Experimento en línea |
| Técnica | Experimento controlado |
| Variables o características | Predicciones de riesgo |
| Métricas | Exactitud y disparidad |
| Resultados relevantes (evidencia) | Las personas rindieron menos que el algoritmo, no evaluaron bien su exactitud y mostraron «interacciones dispares» por raza |
| Limitaciones | Participantes en línea |
| Riesgos de sesgo | Disparidad en la interacción |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta |
| Decisión que respalda (decisión de ingeniería) | Evaluar el sistema socio-técnico completo, no solo el modelo |
| Nivel de confianza | MODERADA |

### S58 — Bansal et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E. et al. (2021). Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance. *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3411764.3445717 |
| Año | 2021 |
| Autores | Bansal, G., Wu, T., Zhou, J., Fok, R., Nushi, B., Kamar, E. et al. |
| Revista o conferencia | Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems |
| DOI / URL | https://doi.org/10.1145/3411764.3445717 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | M · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Medir si las explicaciones producen desempeño complementario |
| Datos o población | Estudios con usuarios en 3 datasets |
| Técnica | Experimentos mixtos |
| Variables o características | Explicaciones de IA |
| Métricas | Exactitud del equipo |
| Resultados relevantes (evidencia) | Las explicaciones no aumentaron el desempeño complementario; aumentaron la aceptación de la recomendación sea correcta o no |
| Limitaciones | Tareas de laboratorio |
| Riesgos de sesgo | Sobredependencia |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta |
| Decisión que respalda (decisión de ingeniería) | Una explicación no garantiza control humano; evitar recomendar un candidato |
| Nivel de confianza | MODERADA |

### S59 — Vasconcelos et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Vasconcelos, H., Jörke, M., Grunde-McLaughlin, M., Gerstenberg, T., Bernstein, M. S. y Krishna, R. (2023). Explanations Can Reduce Overreliance on AI Systems During Decision-Making. *Proceedings of the ACM on Human-Computer Interaction*. https://doi.org/10.1145/3579605 |
| Año | 2023 |
| Autores | Vasconcelos, H., Jörke, M., Grunde-McLaughlin, M., Gerstenberg, T., Bernstein, M. S. y Krishna, R. |
| Revista o conferencia | Proceedings of the ACM on Human-Computer Interaction |
| DOI / URL | https://doi.org/10.1145/3579605 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | M · búsqueda M |
| Avisos de Crossref | ninguno |
| Objetivo | Explicar cuándo las explicaciones reducen la sobredependencia |
| Datos o población | Experimentos |
| Técnica | Marco costo-beneficio |
| Variables o características | Costo de verificar la explicación |
| Métricas | Sobredependencia |
| Resultados relevantes (evidencia) | Hay escenarios en que las explicaciones sí reducen la sobredependencia, si verificarlas cuesta poco |
| Limitaciones | Tareas controladas |
| Riesgos de sesgo | Sobredependencia |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Explicaciones fáciles de verificar contra evidencia citada |
| Nivel de confianza | MODERADA |

### S60 — Vaccaro et al. (2024)

| Campo | Contenido |
|---|---|
| Referencia | Vaccaro, M., Almaatouq, A. y Malone, T. (2024). When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-024-02024-1 |
| Año | 2024 |
| Autores | Vaccaro, M., Almaatouq, A. y Malone, T. |
| Revista o conferencia | Nature Human Behaviour |
| DOI / URL | https://doi.org/10.1038/s41562-024-02024-1 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | M · búsqueda M |
| Avisos de Crossref | ninguno |
| Objetivo | Metaanalizar cuándo humano + IA supera a cada uno |
| Datos o población | 106 experimentos; 370 tamaños de efecto |
| Técnica | Metaanálisis preregistrado |
| Variables o características | Tipo de tarea y desempeño relativo |
| Métricas | g de Hedges |
| Resultados relevantes (evidencia) | En promedio la combinación rindió peor que el mejor de los dos (g = −0,23); pérdidas en tareas de decisión |
| Limitaciones | Posible sesgo de publicación |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta |
| Decisión que respalda (decisión de ingeniería) | No asumir que la recomendación de IA mejora la decisión de selección |
| Nivel de confianza | FUERTE |

### S61 — Alon-Barkat y Busuioc (2022)

| Campo | Contenido |
|---|---|
| Referencia | Alon-Barkat, S. y Busuioc, M. (2022). Human–AI Interactions in Public Sector Decision Making: “Automation Bias” and “Selective Adherence” to Algorithmic Advice. *Journal of Public Administration Research and Theory*. https://doi.org/10.1093/jopart/muac007 |
| Año | 2022 |
| Autores | Alon-Barkat, S. y Busuioc, M. |
| Revista o conferencia | Journal of Public Administration Research and Theory |
| DOI / URL | https://doi.org/10.1093/jopart/muac007 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | M · búsqueda M |
| Avisos de Crossref | ninguno |
| Objetivo | Medir sesgo de automatización y adherencia selectiva en el sector público |
| Datos o población | 3 experimentos (N = 605, 904, 1345) |
| Técnica | Experimentos |
| Variables o características | Fuente del consejo y estereotipos |
| Métricas | Adherencia |
| Resultados relevantes (evidencia) | No se encontró sesgo de automatización; sí adherencia selectiva a consejos alineados con estereotipos en el estudio 2 |
| Limitaciones | Países Bajos |
| Riesgos de sesgo | Estereotipos |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Vigilar adherencia selectiva, no solo sobredependencia |
| Nivel de confianza | CONFLICTIVA |

### S62 — Amershi et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P. et al. (2019). Guidelines for Human-AI Interaction. *Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems*. https://doi.org/10.1145/3290605.3300233 |
| Año | 2019 |
| Autores | Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P. et al. |
| Revista o conferencia | Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems |
| DOI / URL | https://doi.org/10.1145/3290605.3300233 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | M · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer guías de interacción humano-IA |
| Datos o población | Evaluación con 49 profesionales y 20 productos |
| Técnica | Diseño validado |
| Variables o características | 18 guías |
| Métricas | Cumplimiento |
| Resultados relevantes (evidencia) | 18 guías validadas para interacción con IA |
| Limitaciones | Productos de consumo |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta para F40 |
| Decisión que respalda (decisión de ingeniería) | Mostrar qué hace y qué no hace el sistema; permitir corregirlo |
| Nivel de confianza | MODERADA |

### S63 — Parasuraman y Manzey (2010)

| Campo | Contenido |
|---|---|
| Referencia | Parasuraman, R. y Manzey, D. H. (2010). Complacency and Bias in Human Use of Automation: An Attentional Integration. *Human Factors: The Journal of the Human Factors and Ergonomics Society*. https://doi.org/10.1177/0018720810376055 |
| Año | 2010 |
| Autores | Parasuraman, R. y Manzey, D. H. |
| Revista o conferencia | Human Factors: The Journal of the Human Factors and Ergonomics Society |
| DOI / URL | https://doi.org/10.1177/0018720810376055 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | M · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Integrar la evidencia sobre complacencia y sesgo de automatización |
| Datos o población | Revisión de estudios |
| Técnica | Revisión y modelo teórico |
| Variables o características | Carga de tareas, atención |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | El sesgo de automatización produce errores de omisión y comisión; afecta a novatos y expertos |
| Limitaciones | Automatización en general |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Diseñar para revisión activa, no aprobación pasiva |
| Nivel de confianza | MODERADA |

### S64 — Niculescu-Mizil y Caruana (2005)

| Campo | Contenido |
|---|---|
| Referencia | Niculescu-Mizil, A. y Caruana, R. (2005). Predicting good probabilities with supervised learning. *Proceedings of the 22nd international conference on Machine learning - ICML '05*. https://doi.org/10.1145/1102351.1102430 |
| Año | 2005 |
| Autores | Niculescu-Mizil, A. y Caruana, R. |
| Revista o conferencia | Proceedings of the 22nd international conference on Machine learning - ICML '05 |
| DOI / URL | https://doi.org/10.1145/1102351.1102430 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | N · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Comparar la calidad probabilística de distintos algoritmos |
| Datos o población | Varios datasets |
| Técnica | Experimentos |
| Variables o características | Probabilidades predichas |
| Métricas | Calibración |
| Resultados relevantes (evidencia) | Algunos modelos distorsionan probabilidades; Platt e isotónica las corrigen |
| Limitaciones | Datasets clásicos |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Calibrar y verificar probabilidades si se reportan |
| Nivel de confianza | FUERTE |

### S65 — Guo et al. (2017)

| Campo | Contenido |
|---|---|
| Referencia | Guo, C., Pleiss, G., Sun, Y. y Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *arXiv*. https://doi.org/10.48550/arXiv.1706.04599 |
| Año | 2017 |
| Autores | Guo, C., Pleiss, G., Sun, Y. y Weinberger, K. Q. |
| Revista o conferencia | arXiv |
| DOI / URL | https://doi.org/10.48550/arXiv.1706.04599 |
| Tipo de publicación | Preprint (arXiv) |
| Revisión por pares | No (preprint); publicado en ICML 2017 |
| Tema y origen | N · búsqueda N |
| Avisos de Crossref | ninguno |
| Objetivo | Estudiar la calibración de redes modernas |
| Datos o población | Imagen y texto |
| Técnica | Experimentos |
| Variables o características | Profundidad, regularización |
| Métricas | ECE |
| Resultados relevantes (evidencia) | Las redes modernas están mal calibradas; el escalado de temperatura ayuda |
| Limitaciones | Redes profundas |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Baja |
| Decisión que respalda (decisión de ingeniería) | No reportar «confianza» sin calibrarla |
| Nivel de confianza | MODERADA |

### S66 — Brier (1950)

| Campo | Contenido |
|---|---|
| Referencia | Brier, G. W. (1950). VERIFICATION OF FORECASTS EXPRESSED IN TERMS OF PROBABILITY. *Monthly Weather Review*. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 |
| Año | 1950 |
| Autores | Brier, G. W. |
| Revista o conferencia | Monthly Weather Review |
| DOI / URL | https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | N · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer la verificación de pronósticos probabilísticos (puntaje de Brier) (sin resumen disponible; descripción general) |
| Datos o población | Método |
| Técnica | Estadística |
| Variables o características | Pronósticos probabilísticos |
| Métricas | Puntaje de Brier |
| Resultados relevantes (evidencia) | Medida de exactitud probabilística |
| Limitaciones | Antiguo |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Usar Brier si se reportan probabilidades |
| Nivel de confianza | FUERTE |

### S67 — Silva Filho et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Silva Filho, T., Song, H., Perello-Nieto, M., Santos-Rodriguez, R., Kull, M. y Flach, P. (2023). Classifier calibration: a survey on how to assess and improve predicted class probabilities. *Machine Learning*. https://doi.org/10.1007/s10994-023-06336-7 |
| Año | 2023 |
| Autores | Silva Filho, T., Song, H., Perello-Nieto, M., Santos-Rodriguez, R., Kull, M. y Flach, P. |
| Revista o conferencia | Machine Learning |
| DOI / URL | https://doi.org/10.1007/s10994-023-06336-7 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | N · búsqueda N |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar la calibración de clasificadores |
| Datos o población | Revisión |
| Técnica | Tutorial y revisión |
| Variables o características | Métodos de calibración |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Introducción y panorama de principios y práctica |
| Limitaciones | Revisión |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Guía para F39 |
| Nivel de confianza | MODERADA |

### S68 — Saito y Rehmsmeier (2015)

| Campo | Contenido |
|---|---|
| Referencia | Saito, T. y Rehmsmeier, M. (2015). The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. *PLOS ONE*. https://doi.org/10.1371/journal.pone.0118432 |
| Año | 2015 |
| Autores | Saito, T. y Rehmsmeier, M. |
| Revista o conferencia | PLOS ONE |
| DOI / URL | https://doi.org/10.1371/journal.pone.0118432 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | N · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Comparar curvas ROC y PR en datos desbalanceados |
| Datos o población | Simulación y estudios |
| Técnica | Análisis |
| Variables o características | Desbalance de clases |
| Métricas | ROC, PR |
| Resultados relevantes (evidencia) | Las curvas PR son más informativas que ROC con desbalance |
| Limitaciones | Bioinformática |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Preferir PR-AUC con clases desbalanceadas |
| Nivel de confianza | MODERADA |

### S69 — Järvelin y Kekäläinen (2002)

| Campo | Contenido |
|---|---|
| Referencia | Järvelin, K. y Kekäläinen, J. (2002). Cumulated gain-based evaluation of IR techniques. *ACM Transactions on Information Systems*. https://doi.org/10.1145/582415.582418 |
| Año | 2002 |
| Autores | Järvelin, K. y Kekäläinen, J. |
| Revista o conferencia | ACM Transactions on Information Systems |
| DOI / URL | https://doi.org/10.1145/582415.582418 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | N · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer medidas de ganancia acumulada (DCG/NDCG) |
| Datos o población | Experimentos de recuperación |
| Técnica | Métricas |
| Variables o características | Relevancia graduada |
| Métricas | DCG, NDCG |
| Resultados relevantes (evidencia) | Medidas para evaluar rankings con relevancia graduada |
| Limitaciones | Recuperación de información |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | NDCG solo si existe un juicio de relevancia válido |
| Nivel de confianza | FUERTE |

### S70 — Hüllermeier y Waegeman (2021)

| Campo | Contenido |
|---|---|
| Referencia | Hüllermeier, E. y Waegeman, W. (2021). Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods. *Machine Learning*. https://doi.org/10.1007/s10994-021-05946-3 |
| Año | 2021 |
| Autores | Hüllermeier, E. y Waegeman, W. |
| Revista o conferencia | Machine Learning |
| DOI / URL | https://doi.org/10.1007/s10994-021-05946-3 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | N · búsqueda N |
| Avisos de Crossref | ninguno |
| Objetivo | Introducir incertidumbre aleatoria y epistémica |
| Datos o población | Revisión |
| Técnica | Tutorial |
| Variables o características | Tipos de incertidumbre |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Distingue incertidumbre aleatoria y epistémica y sus métodos |
| Limitaciones | Revisión |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Representar «evidencia insuficiente» como incertidumbre epistémica explícita |
| Nivel de confianza | MODERADA |

### S71 — Mitchell et al. (2019)

| Campo | Contenido |
|---|---|
| Referencia | Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B. et al. (2019). Model Cards for Model Reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3287560.3287596 |
| Año | 2019 |
| Autores | Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B. et al. |
| Revista o conferencia | Proceedings of the Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3287560.3287596 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | P · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer model cards |
| Datos o población | Propuesta con ejemplos |
| Técnica | Documentación |
| Variables o características | Uso previsto, métricas por grupo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Documentación estándar de modelos con evaluación por subgrupo |
| Limitaciones | Propuesta |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta (ya usada en RF-29) |
| Decisión que respalda (decisión de ingeniería) | Exigir model card en F36 |
| Nivel de confianza | MODERADA |

### S72 — Gebru et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Iii, H. D. et al. (2021). Datasheets for datasets. *Communications of the ACM*. https://doi.org/10.1145/3458723 |
| Año | 2021 |
| Autores | Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Iii, H. D. et al. |
| Revista o conferencia | Communications of the ACM |
| DOI / URL | https://doi.org/10.1145/3458723 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | P · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer datasheets for datasets |
| Datos o población | Propuesta |
| Técnica | Documentación |
| Variables o características | Motivación, composición, recolección |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Documentación estándar de conjuntos de datos |
| Limitaciones | Propuesta |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Exigir dataset card en F34 |
| Nivel de confianza | MODERADA |

### S73 — Raji et al. (2020)

| Campo | Contenido |
|---|---|
| Referencia | Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B. et al. (2020). Closing the AI accountability gap. *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3351095.3372873 |
| Año | 2020 |
| Autores | Raji, I. D., Smart, A., White, R. N., Mitchell, M., Gebru, T., Hutchinson, B. et al. |
| Revista o conferencia | Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3351095.3372873 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | P · búsqueda L |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer un marco de auditoría algorítmica interna |
| Datos o población | Marco |
| Técnica | Proceso de auditoría |
| Variables o características | Artefactos de auditoría |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Auditoría interna de extremo a extremo antes del despliegue |
| Limitaciones | Marco |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Auditoría interna documentada antes de F39 |
| Nivel de confianza | MODERADA |

### S74 — Kaufman et al. (2012)

| Campo | Contenido |
|---|---|
| Referencia | Kaufman, S., Rosset, S., Perlich, C. y Stitelman, O. (2012). Leakage in data mining. *ACM Transactions on Knowledge Discovery from Data*. https://doi.org/10.1145/2382577.2382579 |
| Año | 2012 |
| Autores | Kaufman, S., Rosset, S., Perlich, C. y Stitelman, O. |
| Revista o conferencia | ACM Transactions on Knowledge Discovery from Data |
| DOI / URL | https://doi.org/10.1145/2382577.2382579 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | O · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Formalizar la fuga de datos (leakage) |
| Datos o población | Casos y competencias |
| Técnica | Análisis |
| Variables o características | Información del objetivo |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Taxonomía de fugas y cómo evitarlas |
| Limitaciones | Casos |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Particiones temporales y por proceso (ya aplicado en RF-29) |
| Nivel de confianza | FUERTE |

### S75 — Gama et al. (2014)

| Campo | Contenido |
|---|---|
| Referencia | Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M. y Bouchachia, A. (2014). A survey on concept drift adaptation. *ACM Computing Surveys*. https://doi.org/10.1145/2523813 |
| Año | 2014 |
| Autores | Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M. y Bouchachia, A. |
| Revista o conferencia | ACM Computing Surveys |
| DOI / URL | https://doi.org/10.1145/2523813 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | O · búsqueda O |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar la adaptación a la deriva de concepto |
| Datos o población | Revisión |
| Técnica | Revisión |
| Variables o características | Deriva |
| Métricas | Varias |
| Resultados relevantes (evidencia) | Categoriza estrategias y evaluación |
| Limitaciones | Aprendizaje en línea |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Monitorear deriva entre convocatorias |
| Nivel de confianza | MODERADA |

### S76 — Breck et al. (2017)

| Campo | Contenido |
|---|---|
| Referencia | Breck, E., Cai, S., Nielsen, E., Salib, M. y Sculley, D. (2017). The ML test score: A rubric for ML production readiness and technical debt reduction. *2017 IEEE International Conference on Big Data (Big Data)*. https://doi.org/10.1109/BigData.2017.8258038 |
| Año | 2017 |
| Autores | Breck, E., Cai, S., Nielsen, E., Salib, M. y Sculley, D. |
| Revista o conferencia | 2017 IEEE International Conference on Big Data (Big Data) |
| DOI / URL | https://doi.org/10.1109/BigData.2017.8258038 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | O · bola de nieve |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer pruebas de preparación para producción de ML |
| Datos o población | Experiencia industrial |
| Técnica | Rúbrica |
| Variables o características | 28 pruebas y monitoreo |
| Métricas | Puntaje |
| Resultados relevantes (evidencia) | 28 pruebas concretas para reducir deuda técnica |
| Limitaciones | Experiencia de una empresa |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Usar la rúbrica como lista de F38–F39 |
| Nivel de confianza | MODERADA |

### S77 — Kreuzberger et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Kreuzberger, D., Kühl, N. y Hirschl, S. (2023). Machine Learning Operations (MLOps): Overview, Definition, and Architecture. *IEEE Access*. https://doi.org/10.1109/access.2023.3262138 |
| Año | 2023 |
| Autores | Kreuzberger, D., Kühl, N. y Hirschl, S. |
| Revista o conferencia | IEEE Access |
| DOI / URL | https://doi.org/10.1109/access.2023.3262138 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | O · búsqueda O |
| Avisos de Crossref | ninguno |
| Objetivo | Definir MLOps |
| Datos o población | Revisión, herramientas y entrevistas |
| Técnica | Métodos mixtos |
| Variables o características | Prácticas y roles |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Definición y arquitectura de MLOps |
| Limitaciones | Revisión |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Versionado y registro mínimos, no una plataforma completa |
| Nivel de confianza | MODERADA |

### S78 — Paleyes et al. (2022)

| Campo | Contenido |
|---|---|
| Referencia | Paleyes, A., Urma, R. G. y Lawrence, N. D. (2022). Challenges in Deploying Machine Learning: A Survey of Case Studies. *ACM Computing Surveys*. https://doi.org/10.1145/3533378 |
| Año | 2022 |
| Autores | Paleyes, A., Urma, R. G. y Lawrence, N. D. |
| Revista o conferencia | ACM Computing Surveys |
| DOI / URL | https://doi.org/10.1145/3533378 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | O · búsqueda O |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar retos de desplegar ML |
| Datos o población | Casos publicados |
| Técnica | Revisión |
| Variables o características | Etapas de despliegue |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Hay problemas en cada etapa del despliegue |
| Limitaciones | Reportes publicados |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Planificar despliegue y monitoreo desde F33 |
| Nivel de confianza | MODERADA |

### S79 — Hutchinson et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Hutchinson, B., Smart, A., Hanna, A., Denton, R., Greer, C., Kjartansson, O. et al. (2021). Towards Accountability for Machine Learning Datasets: Practices from Software Engineering and Infrastructure. *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3442188.3445918 |
| Año | 2021 |
| Autores | Hutchinson, B., Smart, A., Hanna, A., Denton, R., Greer, C., Kjartansson, O. et al. |
| Revista o conferencia | Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3442188.3445918 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | P · búsqueda P |
| Avisos de Crossref | ninguno |
| Objetivo | Proponer rendición de cuentas para datasets |
| Datos o población | Marco |
| Técnica | Ingeniería de software |
| Variables o características | Ciclo de vida del dataset |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Marco de transparencia para el desarrollo de datasets |
| Limitaciones | Marco |
| Riesgos de sesgo | No aplica |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Requisitos y revisiones del dataset como artefactos versionados |
| Nivel de confianza | MODERADA |

### S80 — Giermindl et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Giermindl, L. M., Strich, F., Christ, O., Leicht-Deobald, U. y Redzepi, A. (2021). The dark sides of people analytics: reviewing the perils for organisations and employees. *European Journal of Information Systems*. https://doi.org/10.1080/0960085x.2021.1927213 |
| Año | 2021 |
| Autores | Giermindl, L. M., Strich, F., Christ, O., Leicht-Deobald, U. y Redzepi, A. |
| Revista o conferencia | European Journal of Information Systems |
| DOI / URL | https://doi.org/10.1080/0960085x.2021.1927213 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | Q · búsqueda Q |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar los riesgos de la analítica de personas |
| Datos o población | Revisión teórica |
| Técnica | Revisión |
| Variables o características | Riesgos |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Identifica peligros para organizaciones y empleados |
| Limitaciones | Teórico |
| Riesgos de sesgo | Vigilancia, discriminación |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Minimizar datos y propósito limitado |
| Nivel de confianza | MODERADA |

### S81 — Koenecke et al. (2024)

| Campo | Contenido |
|---|---|
| Referencia | Koenecke, A., Choi, A. S. G., Mei, K. X., Schellmann, H. y Sloane, M. (2024). Careless Whisper: Speech-to-Text Hallucination Harms. *The 2024 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3630106.3658996 |
| Año | 2024 |
| Autores | Koenecke, A., Choi, A. S. G., Mei, K. X., Schellmann, H. y Sloane, M. |
| Revista o conferencia | The 2024 ACM Conference on Fairness, Accountability, and Transparency |
| DOI / URL | https://doi.org/10.1145/3630106.3658996 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | S · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Medir alucinaciones de Whisper |
| Datos o población | Audio de hablantes con afasia y control |
| Técnica | Auditoría |
| Variables o características | Duración no vocal |
| Métricas | Tasa de alucinación |
| Resultados relevantes (evidencia) | Cerca del 1 % de transcripciones contenía frases inventadas; el 38 % de ellas con daños explícitos; más frecuentes con pausas largas |
| Limitaciones | Versión 2023 |
| Riesgos de sesgo | Afecta más a ciertos hablantes |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: una transcripción puede inventar «evidencia» |
| Decisión que respalda (decisión de ingeniería) | Toda transcripción se revisa contra el audio antes de usarse como evidencia |
| Nivel de confianza | MODERADA |

### S82 — Thompson et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Thompson, I., Koenig, N., Mracek, D. L. y Tonidandel, S. (2023). Deep Learning in Employee Selection: Evaluation of Algorithms to Automate the Scoring of Open-Ended Assessments. *Journal of Business and Psychology*. https://doi.org/10.1007/s10869-023-09874-y |
| Año | 2023 |
| Autores | Thompson, I., Koenig, N., Mracek, D. L. y Tonidandel, S. |
| Revista o conferencia | Journal of Business and Psychology |
| DOI / URL | https://doi.org/10.1007/s10869-023-09874-y |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | T · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Evaluar algoritmos para calificar respuestas abiertas en selección (sin resumen disponible; descripción general) |
| Datos o población | Respuestas de evaluaciones de selección |
| Técnica | Deep learning |
| Variables o características | Texto de respuestas |
| Métricas | Acuerdo con calificadores humanos |
| Resultados relevantes (evidencia) | Ver la publicación (resumen no disponible) |
| Limitaciones | Ver la publicación |
| Riesgos de sesgo | Sesgo de los calificadores de entrenamiento |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Solo como antecedente; no adoptar calificación automática |
| Nivel de confianza | INSUFICIENTE |

### S83 — Armstrong et al. (2024)

| Campo | Contenido |
|---|---|
| Referencia | Armstrong, L., Liu, A., MacNeil, S. y Metaxa, D. (2024). The Silicon Ceiling: Auditing GPT’s Race and Gender Biases in Hiring. *Proceedings of the 4th ACM Conference on Equity and Access in Algorithms, Mechanisms, and Optimization*. https://doi.org/10.1145/3689904.3694699 |
| Año | 2024 |
| Autores | Armstrong, L., Liu, A., MacNeil, S. y Metaxa, D. |
| Revista o conferencia | Proceedings of the 4th ACM Conference on Equity and Access in Algorithms, Mechanisms, and Optimization |
| DOI / URL | https://doi.org/10.1145/3689904.3694699 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | E · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Auditar sesgos de GPT-3.5 en contratación |
| Datos o población | 32 nombres, 10 ocupaciones, 3 tareas |
| Técnica | Auditoría por nombres |
| Variables o características | Raza y género |
| Métricas | Puntuaciones |
| Resultados relevantes (evidencia) | El modelo refleja sesgos estereotípicos al evaluar y al generar CV |
| Limitaciones | Un modelo y versión |
| Riesgos de sesgo | Estereotipos |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | No pedir a un LLM que puntúe candidatos |
| Nivel de confianza | MODERADA |

### S84 — Wilson et al. (2025)

| Campo | Contenido |
|---|---|
| Referencia | Wilson, K., Sim, M., Gueorguieva, A. M. y Caliskan, A. (2025). No Thoughts Just AI: Biased LLM Hiring Recommendations Alter Human Decision Making and Limit Human Autonomy. *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1609/aies.v8i3.36749 |
| Año | 2025 |
| Autores | Wilson, K., Sim, M., Gueorguieva, A. M. y Caliskan, A. |
| Revista o conferencia | Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society |
| DOI / URL | https://doi.org/10.1609/aies.v8i3.36749 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | M · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Medir el efecto de recomendaciones sesgadas de IA en decisiones humanas de contratación |
| Datos o población | N = 528; 1526 escenarios; 16 ocupaciones |
| Técnica | Experimento de cribado con IA simulada |
| Variables o características | Preferencias raciales de la IA, IAT, alfabetización en IA |
| Métricas | Tasa de selección por grupo |
| Resultados relevantes (evidencia) | Sin IA o con IA sin sesgo, las personas seleccionaron por igual; con IA sesgada la siguieron hasta en el 90 % de los casos, incluso juzgándola de baja calidad |
| Limitaciones | IA simulada; EE. UU. |
| Riesgos de sesgo | Sesgo transmitido a la persona |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta: cuestiona el «humano en el circuito» como salvaguarda |
| Decisión que respalda (decisión de ingeniería) | No mostrar recomendación de candidato junto a la decisión (refuerza ADR-001) |
| Nivel de confianza | FUERTE |

### S85 — Booth et al. (2021)

| Campo | Contenido |
|---|---|
| Referencia | Booth, B. M., Hickman, L., Subburaj, S. K., Tay, L., Woo, S. E. y D'Mello, S. K. (2021). Bias and Fairness in Multimodal Machine Learning: A Case Study of Automated Video Interviews. *Proceedings of the 2021 International Conference on Multimodal Interaction*. https://doi.org/10.1145/3462244.3479897 |
| Año | 2021 |
| Autores | Booth, B. M., Hickman, L., Subburaj, S. K., Tay, L., Woo, S. E. y D'Mello, S. K. |
| Revista o conferencia | Proceedings of the 2021 International Conference on Multimodal Interaction |
| DOI / URL | https://doi.org/10.1145/3462244.3479897 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | T · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Analizar sesgo y equidad en entrevistas en vídeo multimodales |
| Datos o población | 733 participantes; anotadores entrenados |
| Técnica | Modelos interpretables multimodales |
| Variables o características | Rasgos verbales, paraverbales, visuales |
| Métricas | Exactitud, sesgo, equidad |
| Resultados relevantes (evidencia) | Combinar modalidades apenas mejora la exactitud y aumenta el sesgo; lo verbal solo rinde casi igual |
| Limitaciones | Contratación simulada |
| Riesgos de sesgo | Rasgos visuales y paraverbales |
| Aplicabilidad al caso (inferencia del equipo) | Muy alta |
| Decisión que respalda (decisión de ingeniería) | Usar solo el contenido verbal; excluir rasgos visuales y paraverbales |
| Nivel de confianza | MODERADA |

### S86 — Van Iddekinge et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Van Iddekinge, C. H., Lievens, F. y Sackett, P. R. (2023). Personnel selection: A review of ways to maximize validity, diversity, and the applicant experience. *Personnel Psychology*. https://doi.org/10.1111/peps.12578 |
| Año | 2023 |
| Autores | Van Iddekinge, C. H., Lievens, F. y Sackett, P. R. |
| Revista o conferencia | Personnel Psychology |
| DOI / URL | https://doi.org/10.1111/peps.12578 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | D · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Revisar decisiones de diseño de selección (validez, diversidad, experiencia) |
| Datos o población | Revisión |
| Técnica | Revisión |
| Variables o características | Desarrollo, administración y puntuación (incluida IA) |
| Métricas | Cualitativo |
| Resultados relevantes (evidencia) | Sintetiza efectos de decisiones de diseño sobre validez, diversidad y experiencia del postulante |
| Limitaciones | Revisión |
| Riesgos de sesgo | Impacto adverso |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | Explicar el procedimiento al postulante antes de evaluar |
| Nivel de confianza | MODERADA |

### S87 — Glazko et al. (2024)

| Campo | Contenido |
|---|---|
| Referencia | Glazko, K., Mohammed, Y., Kosa, B., Potluri, V. y Mankoff, J. (2024). Identifying and Improving Disability Bias in GPT-Based Resume Screening. *The 2024 ACM Conference on Fairness Accountability and Transparency*. https://doi.org/10.1145/3630106.3658933 |
| Año | 2024 |
| Autores | Glazko, K., Mohammed, Y., Kosa, B., Potluri, V. y Mankoff, J. |
| Revista o conferencia | The 2024 ACM Conference on Fairness Accountability and Transparency |
| DOI / URL | https://doi.org/10.1145/3630106.3658933 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | E · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Auditar sesgo por discapacidad en cribado de CV con GPT-4 |
| Datos o población | Pares de CV con y sin méritos relacionados con discapacidad |
| Técnica | Auditoría |
| Variables o características | Méritos asociados a discapacidad |
| Métricas | Ranking |
| Resultados relevantes (evidencia) | GPT-4 mostró prejuicio contra CV con méritos relacionados con discapacidad |
| Limitaciones | Un modelo |
| Riesgos de sesgo | Capacitismo |
| Aplicabilidad al caso (inferencia del equipo) | Alta |
| Decisión que respalda (decisión de ingeniería) | No usar LLM para ordenar CV |
| Nivel de confianza | MODERADA |

### S88 — Bredin (2023)

| Campo | Contenido |
|---|---|
| Referencia | Bredin, H. (2023). pyannote.audio 2.1 speaker diarization pipeline: principle, benchmark, and recipe. *INTERSPEECH 2023*. https://doi.org/10.21437/interspeech.2023-105 |
| Año | 2023 |
| Autores | Bredin, H. |
| Revista o conferencia | INTERSPEECH 2023 |
| DOI / URL | https://doi.org/10.21437/interspeech.2023-105 |
| Tipo de publicación | Artículo de conferencia |
| Revisión por pares | Sí |
| Tema y origen | S · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Describir el pipeline de diarización de pyannote.audio 2.1 (sin resumen disponible; descripción general) |
| Datos o población | Benchmarks de diarización |
| Técnica | Segmentación y embeddings de hablante |
| Variables o características | Audio |
| Métricas | DER |
| Resultados relevantes (evidencia) | Pipeline y receta de diarización |
| Limitaciones | Benchmarks |
| Riesgos de sesgo | Usa embeddings de voz (dato biométrico) |
| Aplicabilidad al caso (inferencia del equipo) | Media |
| Decisión que respalda (decisión de ingeniería) | Preferir canales separados o segmentación manual antes que huellas de voz |
| Nivel de confianza | MODERADA |

### S89 — Koenig et al. (2023)

| Campo | Contenido |
|---|---|
| Referencia | Koenig, N., Tonidandel, S., Thompson, I., Albritton, B., Koohifar, F., Yankov, G. et al. (2023). Improving measurement and prediction in personnel selection through the application of machine learning. *Personnel Psychology*. https://doi.org/10.1111/peps.12608 |
| Año | 2023 |
| Autores | Koenig, N., Tonidandel, S., Thompson, I., Albritton, B., Koohifar, F., Yankov, G. et al. |
| Revista o conferencia | Personnel Psychology |
| DOI / URL | https://doi.org/10.1111/peps.12608 |
| Tipo de publicación | Artículo de revista |
| Revisión por pares | Sí |
| Tema y origen | C · búsqueda complementaria |
| Avisos de Crossref | ninguno |
| Objetivo | Presentar seis casos de ML para puntuar respuestas en selección operativa |
| Datos o población | Seis sistemas operativos en organizaciones |
| Técnica | ML sobre respuestas escritas y orales |
| Variables o características | Texto de respuestas |
| Métricas | Exactitud, fiabilidad, impacto adverso |
| Resultados relevantes (evidencia) | El ML calificó respuestas tan exacta y fiablemente como jueces humanos, con poco o ningún impacto adverso |
| Limitaciones | Grandes volúmenes de datos de organizaciones grandes |
| Riesgos de sesgo | Depende de los calificadores humanos de referencia |
| Aplicabilidad al caso (inferencia del equipo) | Media: el caso no tiene ese volumen de datos |
| Decisión que respalda (decisión de ingeniería) | Posible a futuro solo con validación local; en tensión con S84 |
| Nivel de confianza | CONFLICTIVA |

## 4. Normas, documentos oficiales y fuentes secundarias

Para las normas no aplican campos como métricas o población: se registra qué establecen, si aplican al caso y qué decisión motivan. Esto no es asesoría legal: la evaluación de impacto la valida una persona con competencia jurídica.

- **Normas de la UE (O01, O02, O16):** EUR-Lex responde 202 a clientes automáticos; su texto se verificó en la versión oficial del Diario Oficial que sirve la Oficina de Publicaciones de la UE.
- **DS 115-2025-PCM (O13):** la ficha oficial en gob.pe está verificada y el **art. 24.1 e) está corroborado**. El texto de los demás artículos citados (24, incluidos sus incisos b) e i); 23, 25, 28.11, 30 y 31) se leyó en la copia en PDF de la publicación en El Peruano que difunde el portal jurídico LP Derecho. **Requieren contraste artículo por artículo con la publicación normativa oficial antes de producir efectos jurídicos.**

| ID | Documento | Qué establece (relevante) | Aplicabilidad | Decisión que motiva | Verificado |
|---|---|---|---|---|---|
| O01 | Reglamento (UE) 2024/1689 (Ley de IA) | Prohíbe inferir emociones en el trabajo y la educación (art. 5.1.f); clasifica como alto riesgo el reclutamiento y la evaluación de candidatos (Anexo III, 4.a); exige supervisión humana capaz de ignorar o revertir el resultado y consciente del sesgo de automatización (art. 14). Texto contrastado en el Diario Oficial (Oficina de Publicaciones de la UE) | Referencia comparada (no aplica directamente en Perú) | Diseñar como sistema de alto riesgo aunque no se esté obligado | Sí |
| O02 | Reglamento (UE) 2016/679 (RGPD) | Derecho a no ser objeto de decisiones exclusivamente automatizadas (art. 22) | Referencia comparada | Decisión final siempre humana (ya en RF-23) | Sí |
| O03 | NIST AI RMF 1.0 | Funciones gobernar, mapear, medir y gestionar riesgos de IA | Marco voluntario | Estructurar el análisis de riesgos de F34–F39 | Sí |
| O04 | NIST SP 1270 | Identificación y gestión de sesgos en IA (sesgos sistémicos, estadísticos y humanos) | Marco voluntario | Catálogo de sesgos humanos y sistémicos | Sí |
| O05 | ISO/IEC 42001:2023 | Sistema de gestión de IA | Norma de pago; referencia | Referencia de gobernanza; sin certificación | Sí |
| O06 | ISO/IEC 23894:2023 | Gestión de riesgos de IA | Norma de pago; referencia | Referencia de gestión de riesgos | Sí |
| O07 | Principios de IA de la OCDE | Principios de IA confiable | Referencia; el DS 115-2025-PCM los cita | Alineación de principios | Sí |
| O08 | Recomendación de la UNESCO sobre ética de la IA | Principios éticos y supervisión humana | Referencia | Alineación de principios | Sí |
| O09 | DS 016-2024-JUS (reglamento de la Ley 29733) | Protección de datos personales en Perú | Aplica al caso | Base legal, consentimiento, minimización y seguridad de datos de postulantes | Sí |
| O10 | Ley N.º 31814 | Promueve el uso de IA en Perú | Aplica | Marco nacional | Sí |
| O11 | 29 CFR 1607 (Uniform Guidelines) | Regla de los cuatro quintos como indicio de impacto adverso | Referencia de EE. UU. | Indicador de impacto adverso solo con datos válidos y suficientes | Sí |
| O12 | NYC Local Law 144 (AEDT) | Auditorías de sesgo para herramientas automatizadas de empleo | Referencia de EE. UU. | Antecedente de auditoría independiente | Sí |
| O13 | DS 115-2025-PCM (reglamento de la Ley 31814) | Riesgo alto: determinar selección, evaluación, contratación y cese de postulantes (art. 24.1 e, corroborado). Además, según la lectura de F30 pendiente de contraste con la publicación oficial: evaluación de NNA en educación (24.1 b); inferir emociones en el trabajo o centros educativos (24.1, final del inciso i); transparencia y explicación (art. 25); evaluación de impacto previa (art. 30); registro (art. 31) | Aplica al caso (vigente) | Tratar la visión F33–F40 como riesgo alto. Los arts. 24, 30 y 31 se contrastan artículo por artículo con la publicación normativa oficial antes de producir efectos jurídicos | Sí |
| O14 | Marco de Buen Desempeño Docente (MINEDU, RM 0547-2012-ED) | Dominios, competencias y desempeños del buen docente en Perú | Aplica al caso docente | Fuente candidata de competencias para vacantes docentes, a validar con el colegio | Sí |
| O15 | Ley N.º 29733, Ley de Protección de Datos Personales (2011) | Derecho fundamental a la protección de datos personales: principios de consentimiento, finalidad, proporcionalidad y seguridad; datos sensibles | Aplica al caso (norma primaria; O09 es su reglamento) | Base legal, consentimiento, minimización y seguridad de los datos de postulantes | Sí |
| O16 | Reglamento (UE) 2026/1744 (Digital Omnibus on AI) | Modifica el Reglamento (UE) 2024/1689: los requisitos de alto riesgo (cap. III, secciones 1 a 3) se aplican desde el 2/12/2027 a los sistemas del Anexo III y desde el 2/8/2028 a los del Anexo I; entra en vigor al tercer día de su publicación (DO de 24/7/2026); no modifica la prohibición del art. 5.1.f | Referencia comparada (fuente oficial del calendario) | El calendario de la UE se cita desde esta fuente oficial y no desde X02 | Sí |

Fuentes secundarias (solo para contrastar, nunca como única base de una afirmación):

| ID | Página | Uso |
|---|---|---|
| X01 | Annex III: High-Risk AI Systems Referred to in Article 6(2) \| EU Artificial Intelligence Act | Lectura del Anexo III y del art. 5 de la Ley de IA cuando EUR-Lex no entrega el texto a clientes automáticos |
| X02 | EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines and Other Key Changes - Gibson Dunn | Contexto del acuerdo político del Digital Omnibus. **Sustituida** para fechas por la fuente oficial O16 (Reglamento (UE) 2026/1744), con la que coincide en el aplazamiento al 2/12/2027 de las obligaciones del Anexo III |

## 5. Avisos editoriales y exclusiones

Fuentes incluidas con avisos (corrección o errata; ninguna retractada):

| ID | Referencia | Aviso |
|---|---|---|
| S08 | Barrett et al. (2019) | correction |
| S21 | Koo y Li (2016) | erratum |

Fuentes excluidas tras la verificación:

| DOI | Tema | Motivo |
|---|---|---|
| https://doi.org/10.1057/s41599-023-01787-8 | Q | Artículo retractado: Crossref registra una retractación del editor (10.1057/s41599-026-06602-8, 03/02/2026) y el título empieza por «RETRACTED ARTICLE» |
