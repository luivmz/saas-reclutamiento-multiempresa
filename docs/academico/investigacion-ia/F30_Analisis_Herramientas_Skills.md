# F30 — Análisis de herramientas, skills y servidores MCP

> Datos generados por `docs/academico/tools/f30/f30.py` desde `datos/herramientas.json` (consultas a la API de GitHub, PyPI, npm y OSV con `herramientas.py`) y la clasificación de `m_herramientas.py`. **En F30 no se instaló nada**: ni paquetes, ni skills, ni servidores MCP.

## 1. Método

- **Datos objetivos por herramienta:** existencia y propietario del repositorio, licencia, archivado, última actividad, estrellas; versión y fecha en el registro del paquete; avisos de seguridad en OSV, tanto el total histórico como los que afectan a la última versión publicada.
- **Clasificación:** RECOMENDADO, EVALUAR EN SANDBOX, NO NECESARIO o EVITAR, según necesidad real en F33–F40, evidencia de la matriz, licencia, mantenimiento, avisos y superficie de ataque.
- **Un aviso histórico no es una vulnerabilidad actual:** indica cuánta superficie de ataque ha tenido el proyecto (p. ej., lectores de PDF frente a archivos malformados). Lo que bloquea es un aviso en la versión que se instalaría.
- **Skills y MCP locales:** inventario de solo lectura de `.claude/skills/`, `~/.claude/skills`, plugins y conectores visibles en la sesión, revisando archivos, scripts, *hooks*, `allowed-tools` e instrucciones.

## 2. Resultado

Herramientas evaluadas: 49. RECOMENDADO: 6, EVALUAR EN SANDBOX: 15, NO NECESARIO: 24, EVITAR: 4.

- **RECOMENDADO:** scikit-learn, Fairlearn, nbstripout, pip-audit, OSV-Scanner, Zotero.
- **EVALUAR EN SANDBOX:** InterpretML (EBM), SHAP, AIF360, Pandera, spaCy, sentence-transformers, Microsoft Presidio, Whisper (OpenAI), faster-whisper, whisper.cpp, FFmpeg, pypdf, pdfplumber, python-docx, Ollama.
- **NO NECESARIO:** XGBoost, LightGBM, CatBoost, MLflow, DVC, Evidently, Great Expectations, Hugging Face Transformers, pgvector, FAISS, Qdrant, Vosk, Apache Tika, Docling, Unstructured, Tesseract OCR, JupyterLab, Mermaid, Better BibTeX for Zotero, MCP Reference Servers (fetch, filesystem, git), GitHub MCP Server, Hugging Face MCP Server, arXiv MCP Server, Context7 MCP.
- **EVITAR:** LIME, pyannote.audio, PyMuPDF, Zotero MCP.

## 3. Comparación por necesidad

### Modelo base (si F36 lo justifica)

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| scikit-learn | RECOMENDADO | F36, F37, F39 | Ya es la base de RF-29; trae modelos interpretables (regresión logística, árboles poco profundos), calibración y métricas [S51, S64, S67] | Fijar versión; ningún modelo puntúa personas sin la puerta G0 |
| InterpretML (EBM) | EVALUAR EN SANDBOX | F36 | Modelos aditivos interpretables (*glassbox*), alineados con preferir modelos interpretables a explicaciones post hoc [S51] | Solo si F36 confirma que se necesita un modelo y no bastan reglas |
| XGBoost | NO NECESARIO | — | Con datos pequeños, un modelo de *boosting* no compensa su menor interpretabilidad en una decisión de alto impacto [S04, S51] | Reconsiderar solo con datos y G0 |
| LightGBM | NO NECESARIO | — | Igual que XGBoost [S04, S51] | Igual que XGBoost |
| CatBoost | NO NECESARIO | — | Igual que XGBoost [S04, S51] | Igual que XGBoost |

### Explicabilidad

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| SHAP | EVALUAR EN SANDBOX | F37 | Atribuciones útiles para depurar internamente [S53]; la evidencia muestra que las explicaciones sirven sobre todo a ingenieros [S56] y pueden aumentar la aceptación acrítica [S58] | Nunca como explicación para el evaluador o el postulante |
| LIME | EVITAR | — | Explicaciones locales aproximadas e inestables [S52]; el repositorio no registra actividad desde julio de 2024 (ver datos) | Mantenimiento detenido |
| InterpretML (EBM) | EVALUAR EN SANDBOX | F36 | Modelos aditivos interpretables (*glassbox*), alineados con preferir modelos interpretables a explicaciones post hoc [S51] | Solo si F36 confirma que se necesita un modelo y no bastan reglas |

### Equidad

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| Fairlearn | RECOMENDADO | F37, F39 | Métricas desagregadas por grupo y comparación de tasas de selección, de licencia MIT y con dependencias moderadas [S41, S46] | Las métricas exigen datos de grupo con base legal y consentimiento (F34) [O09, O13] |
| AIF360 | EVALUAR EN SANDBOX | F37 | Catálogo amplio de métricas y mitigaciones [S49] | Más pesado que Fairlearn; solo si F37 necesita una métrica que Fairlearn no tiene |

### Registro de modelos y experimentos

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| MLflow | NO NECESARIO | — | A la escala del caso, un registro de modelos con `model_version`, hash y model card versionados en Git basta [S71, S77]; MLflow añade un servidor con muchos avisos de seguridad históricos (ver datos) | Superficie de ataque de un servidor adicional |

### Versionado y validación de datos

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| DVC | NO NECESARIO | — | Los conjuntos sintéticos son pequeños; manifiesto SHA-256 y dataset card en Git cubren el linaje [S72, S79] | Reconsiderar si un conjunto supera lo razonable para Git |
| Pandera | EVALUAR EN SANDBOX | F34 | Validación de esquema de los conjuntos (tipos, rangos, columnas prohibidas como nombre o DNI) [S72, S74] | Fijar versión |
| Great Expectations | NO NECESARIO | — | Cubre lo mismo que Pandera con más dependencias | — |

### Monitoreo y deriva

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| Evidently | NO NECESARIO | — | Con pocas convocatorias al año, la deriva se revisa con reportes simples por convocatoria [S75] | Reconsiderar con volumen |

### Texto, entidades y anonimización

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| spaCy | EVALUAR EN SANDBOX | F34, F35 | Reconocimiento de entidades para anonimizar y segmentar texto en español [S33] | Medir errores de anonimización con texto ficticio antes de usarlo |
| Microsoft Presidio | EVALUAR EN SANDBOX | F34 | Detección y anonimización de datos personales en texto [O09] | Sus reconocedores por defecto están orientados al inglés: medir en español. El repositorio ya no pertenece a la organización microsoft (GitHub lo redirige): verificar quién publica el paquete |
| Hugging Face Transformers | NO NECESARIO | — | Solo entraría como dependencia de otra herramienta; muchos avisos históricos y carga de pesos de modelos de terceros (ver datos) | Pesos en formatos ejecutables (pickle): solo *safetensors* y repositorios fijados |

### Similitud semántica y búsqueda vectorial

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| sentence-transformers | EVALUAR EN SANDBOX | F35 | Embeddings para localizar fragmentos de evidencia relacionados con un criterio [S31] | Nunca como puntuación de candidatos: los embeddings reproducen sesgos de nombre y género [S11] |
| pgvector | NO NECESARIO | — | F33–F40 no necesitan búsqueda vectorial persistente; si llegara a necesitarse, pgvector usa el PostgreSQL ya existente en lugar de un servicio nuevo | Decisión diferida |
| FAISS | NO NECESARIO | — | Igual que pgvector; además añade una dependencia nativa | — |
| Qdrant | NO NECESARIO | — | Servicio adicional sin necesidad demostrada | Infraestructura nueva |

### Voz a texto y diarización

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| Whisper (OpenAI) | EVALUAR EN SANDBOX | F35 | Transcripción local robusta y multilingüe [S38] | Alucina frases en una parte pequeña de los casos [S81] y el error varía por hablante [S10]: toda transcripción se revisa contra el audio |
| faster-whisper | EVALUAR EN SANDBOX | F35 | El mismo modelo Whisper con inferencia más eficiente | Mismos riesgos que Whisper [S10, S81] |
| whisper.cpp | EVALUAR EN SANDBOX | F35 | Whisper en C/C++ sin Python, útil en equipos modestos | Mismos riesgos que Whisper [S10, S81] |
| Vosk | NO NECESARIO | — | La matriz no reúne evidencia de su exactitud en español; Whisper ya cubre la necesidad | Alternativa solo si Whisper no fuera viable |
| pyannote.audio | EVITAR | — | La diarización usa embeddings de voz [S88], que son datos biométricos; para separar entrevistador y postulante bastan canales separados o marcas manuales [O09, O13] | Dato biométrico; modelos con acceso condicionado en Hugging Face |
| FFmpeg | EVALUAR EN SANDBOX | F35 | Conversión y normalización de audio antes de transcribir | Solo con la puerta del audio aprobada; LGPL con componentes GPL opcionales: compilar sin ellos |

### Documentos (PDF, DOCX, OCR)

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| pypdf | EVALUAR EN SANDBOX | F35 | Extracción de texto de PDF en Python puro, licencia BSD | Muchos avisos históricos por PDF malformados: límites de tamaño y tiempo, y proceso aislado |
| pdfplumber | EVALUAR EN SANDBOX | F35 | Extracción con posiciones (tablas, columnas), licencia MIT | Mismas precauciones que pypdf |
| python-docx | EVALUAR EN SANDBOX | F35 | Lectura de CV en DOCX, licencia MIT | Fijar versión |
| PyMuPDF | EVITAR | — | Licencia AGPL-3.0: requiere revisión de compatibilidad AGPL o licencia comercial; se evita por prudencia | Riesgo de licencia |
| Docling | NO NECESARIO | — | Descarga modelos de disposición; los CV del caso son digitales [S37] | Peso y modelos de terceros |
| Unstructured | NO NECESARIO | — | Muchas dependencias para una necesidad que cubren pypdf y python-docx | — |
| Apache Tika | NO NECESARIO | — | Requiere JVM; para PDF y DOCX digitales bastan bibliotecas Python | Avisos históricos (ver datos) |
| Tesseract OCR | NO NECESARIO | — | Solo haría falta con documentos escaneados [S37] | — |

### Cuadernos y reproducibilidad

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| JupyterLab | NO NECESARIO | — | El proyecto usa scripts reproducibles; los cuadernos guardan salidas que pueden filtrar datos | Avisos históricos (ver datos) |
| nbstripout | RECOMENDADO | F34, F36 | Si el equipo usa cuadernos, elimina sus salidas antes del commit | Solo tiene sentido si se adoptan cuadernos |

### Seguridad de dependencias

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| pip-audit | RECOMENDADO | F33–F40 | Auditoría de dependencias Python (PyPA) del ml-service | — |
| OSV-Scanner | RECOMENDADO | F33–F40 | Auditoría de dependencias en varios ecosistemas (Composer, npm, PyPI) con la base OSV usada en este análisis | — |

### LLM local

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| Ollama | EVALUAR EN SANDBOX | F33 | LLM local, sin enviar datos fuera; solo para tareas que no evalúan personas (p. ej., borradores de preguntas que revisa un humano) | Nunca para puntuar ni resumir candidatos: alucinación [S34] y sesgos [S83, S87] |

### Bibliografía y diagramas

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| Zotero | RECOMENDADO | F33–F40 | Gestión bibliográfica de escritorio; la AGPL no afecta su uso local | — |
| Better BibTeX for Zotero | NO NECESARIO | — | Las referencias se generan desde Crossref y DataCite con un script reproducible | — |
| Mermaid | NO NECESARIO | — | El proyecto ya formaliza diagramas con PlantUML y PowerDesigner | — |

### Servidores MCP

| Herramienta | Clasificación | Fase | Justificación | Condición o riesgo |
|---|---|---|---|---|
| MCP Reference Servers (fetch, filesystem, git) | NO NECESARIO | — | Claude Code ya tiene lectura de archivos, Git y consulta web con permisos controlados | fetch expone a contenido externo con instrucciones (inyección de prompt) |
| GitHub MCP Server | NO NECESARIO | — | El flujo usa Git y la API de GitHub de forma explícita | Requiere token con permisos de escritura |
| Hugging Face MCP Server | NO NECESARIO | — | No hay búsqueda de modelos prevista en F33–F40 | Proyecto con poca adopción (ver datos) |
| arXiv MCP Server | NO NECESARIO | — | La búsqueda de F30 se hizo con OpenAlex, Crossref y DataCite mediante scripts reproducibles | Mantenedor individual |
| Zotero MCP | EVITAR | — | Da a un agente acceso a la biblioteca local y su clave de API; mantenedor individual | Acceso amplio con credenciales |
| Context7 MCP | NO NECESARIO | — | Envía consultas a un servicio externo; la documentación oficial de cada biblioteca basta | Envío de contexto a terceros |

## 4. Datos verificados por herramienta

Consulta del 2026-09-30 (cada herramienta registra su fecha en `datos/herramientas.json`).

| Herramienta | Repositorio | Licencia (GitHub) | Última actividad | Estrellas | Archivado | Versión | Avisos OSV históricos | Avisos en última versión | Clasificación |
|---|---|---|---|---|---|---|---|---|---|
| scikit-learn | scikit-learn/scikit-learn | BSD-3-Clause | 2026-09-30 | 67435 | no | 1.9.1 | 6 | 0 | RECOMENDADO |
| XGBoost | dmlc/xgboost | Apache-2.0 | 2026-09-30 | 28809 | no | 3.4.1 | 0 | 0 | NO NECESARIO |
| LightGBM | lightgbm-org/LightGBM (transferido) | MIT | 2026-09-29 | 18824 | no | 4.7.0 | 2 | 0 | NO NECESARIO |
| CatBoost | catboost/catboost | Apache-2.0 | 2026-09-30 | 9128 | no | 1.2.10 | 0 | 0 | NO NECESARIO |
| InterpretML (EBM) | interpretml/interpret | MIT | 2026-09-28 | 6949 | no | 0.7.8 | 0 | 0 | EVALUAR EN SANDBOX |
| SHAP | shap/shap | MIT | 2026-09-30 | 25787 | no | 0.52.0 | 0 | 0 | EVALUAR EN SANDBOX |
| LIME | marcotcr/lime | BSD-2-Clause | 2024-07-25 | 12163 | no | 0.2.0.1 | 0 | 0 | EVITAR |
| Fairlearn | fairlearn/fairlearn | MIT | 2026-09-30 | 2289 | no | 0.14.0 | 0 | 0 | RECOMENDADO |
| AIF360 | Trusted-AI/AIF360 | Apache-2.0 | 2026-06-15 | 2872 | no | 0.6.1 | 0 | 0 | EVALUAR EN SANDBOX |
| MLflow | mlflow/mlflow | Apache-2.0 | 2026-10-01 | 28205 | no | 3.16.1 | 162 | 0 | NO NECESARIO |
| DVC | treeverse/dvc (transferido) | Apache-2.0 | 2026-09-28 | 15892 | no | 3.67.1 | 0 | 0 | NO NECESARIO |
| Evidently | evidentlyai/evidently | Apache-2.0 | 2026-09-29 | 7951 | no | 0.7.23 | 0 | 0 | NO NECESARIO |
| Pandera | unionai-oss/pandera | MIT | 2026-09-26 | 4471 | no | 0.33.1 | 0 | 0 | EVALUAR EN SANDBOX |
| Great Expectations | fivetran/great_expectations (transferido) | Apache-2.0 | 2026-09-30 | 11851 | no | 1.23.2 | 0 | 0 | NO NECESARIO |
| spaCy | explosion/spaCy | MIT | 2026-09-30 | 33931 | no | 3.8.16 | 0 | 0 | EVALUAR EN SANDBOX |
| sentence-transformers | huggingface/sentence-transformers (transferido) | Apache-2.0 | 2026-09-24 | 19138 | no | 6.1.0 | 1 | 0 | EVALUAR EN SANDBOX |
| Hugging Face Transformers | huggingface/transformers | Apache-2.0 | 2026-10-01 | 166874 | no | 5.18.0 | 55 | 0 | NO NECESARIO |
| Microsoft Presidio | data-privacy-stack/presidio (transferido) | MIT | 2026-09-29 | 11119 | no | 2.2.364 | 0 | 0 | EVALUAR EN SANDBOX |
| pgvector | pgvector/pgvector | NOASSERTION | 2026-09-30 | 23202 | no | — | — | — | NO NECESARIO |
| FAISS | facebookresearch/faiss | MIT | 2026-09-29 | 41003 | no | 1.15.1 | 0 | 0 | NO NECESARIO |
| Qdrant | qdrant/qdrant | Apache-2.0 | 2026-09-30 | 34892 | no | 1.19.1 | 2 | 0 | NO NECESARIO |
| Whisper (OpenAI) | openai/whisper | MIT | 2026-08-31 | 109815 | no | 20250625 | 0 | 0 | EVALUAR EN SANDBOX |
| faster-whisper | SYSTRAN/faster-whisper | MIT | 2026-09-30 | 25653 | no | 1.2.1 | 0 | 0 | EVALUAR EN SANDBOX |
| whisper.cpp | ggml-org/whisper.cpp | MIT | 2026-09-28 | 54050 | no | — | — | — | EVALUAR EN SANDBOX |
| Vosk | alphacep/vosk-api | Apache-2.0 | 2026-08-09 | 15158 | no | 0.3.45 | 0 | 0 | NO NECESARIO |
| pyannote.audio | pyannote/pyannote-audio | MIT | 2026-09-24 | 10606 | no | 4.0.7 | 0 | 0 | EVITAR |
| FFmpeg | FFmpeg/FFmpeg | NOASSERTION | 2026-10-01 | 64673 | no | — | — | — | EVALUAR EN SANDBOX |
| Apache Tika | apache/tika | Apache-2.0 | 2026-09-30 | 4082 | no | — | 13 | — | NO NECESARIO |
| PyMuPDF | pymupdf/PyMuPDF | AGPL-3.0 | 2026-09-30 | 10812 | no | 1.28.2 | 2 | 0 | EVITAR |
| pypdf | py-pdf/pypdf | NOASSERTION | 2026-09-30 | 10241 | no | 6.19.0 | 85 | 0 | EVALUAR EN SANDBOX |
| pdfplumber | jsvine/pdfplumber | MIT | 2026-08-06 | 10786 | no | 0.11.10 | 0 | 0 | EVALUAR EN SANDBOX |
| Docling | docling-project/docling | MIT | 2026-09-30 | 68237 | no | 2.131.0 | 16 | 0 | NO NECESARIO |
| Unstructured | Unstructured-IO/unstructured | Apache-2.0 | 2026-09-30 | 15520 | no | 0.27.10 | 6 | 0 | NO NECESARIO |
| python-docx | python-openxml/python-docx | MIT | 2026-08-01 | 5731 | no | 1.2.0 | 2 | 0 | EVALUAR EN SANDBOX |
| Tesseract OCR | tesseract-ocr/tesseract | Apache-2.0 | 2026-09-28 | 76776 | no | — | — | — | NO NECESARIO |
| JupyterLab | jupyterlab/jupyterlab | BSD-3-Clause | 2026-09-30 | 15328 | no | 4.6.4 | 26 | 0 | NO NECESARIO |
| nbstripout | kynan/nbstripout | NOASSERTION | 2026-04-11 | 1484 | no | 0.9.1 | 0 | 0 | RECOMENDADO |
| pip-audit | pypa/pip-audit | Apache-2.0 | 2026-09-26 | 1375 | no | 2.10.1 | 0 | 0 | RECOMENDADO |
| OSV-Scanner | google/osv-scanner | Apache-2.0 | 2026-10-01 | 11126 | no | — | — | — | RECOMENDADO |
| Mermaid | mermaid-js/mermaid | MIT | 2026-09-30 | 90493 | no | 12.0.0 | 16 | 0 | NO NECESARIO |
| Ollama | ollama/ollama | MIT | 2026-09-30 | 181981 | no | — | — | — | EVALUAR EN SANDBOX |
| Zotero | zotero/zotero | NOASSERTION | 2026-09-30 | 15447 | no | — | — | — | RECOMENDADO |
| Better BibTeX for Zotero | retorquere/zotero-better-bibtex | MIT | 2026-09-30 | 7178 | no | — | — | — | NO NECESARIO |
| MCP Reference Servers (fetch, filesystem, git) | modelcontextprotocol/servers | NOASSERTION | 2026-10-01 | 90835 | no | — | — | — | NO NECESARIO |
| GitHub MCP Server | github/github-mcp-server | MIT | 2026-09-30 | 33308 | no | — | — | — | NO NECESARIO |
| Hugging Face MCP Server | huggingface/hf-mcp-server | MIT | 2026-09-29 | 301 | no | — | — | — | NO NECESARIO |
| arXiv MCP Server | blazickjp/arxiv-mcp-server | Apache-2.0 | 2026-09-30 | 3183 | no | 0.7.3 | 0 | 0 | NO NECESARIO |
| Zotero MCP | 54yyyu/zotero-mcp | MIT | 2026-09-30 | 5205 | no | 0.3.1 | 0 | 0 | EVITAR |
| Context7 MCP | upstash/context7 | MIT | 2026-09-30 | 62568 | no | 4.1.1 | 0 | 0 | NO NECESARIO |

«—» en avisos: la herramienta no se publica en un ecosistema que OSV indexe con ese nombre (p. ej., binarios o extensiones); no significa cero avisos. «NOASSERTION» o «Other»: GitHub no reconoce la licencia automáticamente; se revisa el archivo de licencia antes de adoptar.

## 5. Skills, plugins y conectores del entorno local

Inventario de solo lectura del 30/09/2026. Las skills del proyecto son Markdown sin scripts, *hooks* ni acceso de red; las tres externas tienen `PROVENANCE.md` con origen, commit fijado, licencia y auditoría. No hay *hooks* configurados en `.claude/settings.local.json` ni en la configuración de usuario.

| Skill o plugin | Origen | Contenido | Clasificación | Uso o motivo |
|---|---|---|---|---|
| project-guardian | Proyecto (propia) | Solo Markdown | RECOMENDADO | Obligatoria antes de cualquier cambio |
| academic-traceability | Proyecto (propia) | Solo Markdown | RECOMENDADO | Trazabilidad de F33–F40 |
| laravel-saas-quality | Proyecto (propia) | Solo Markdown | RECOMENDADO | F38 (integración Laravel) |
| ml-risk-service | Proyecto (propia) | Solo Markdown | RECOMENDADO | Marco de RF-29; F33 debe ampliarla o crear una nueva skill para el motor, sin mezclar ambos |
| powerdesigner-uml | Proyecto (propia) | Solo Markdown | RECOMENDADO | Diagramas TO-BE del motor |
| recruitment-3d-experience | Proyecto (propia) | Solo Markdown | NO NECESARIO | Sin relación con el motor |
| frontend-design | Externa (Anthropic), con PROVENANCE.md | Solo Markdown, Apache 2.0 | RECOMENDADO | F40 (panel) |
| animate | Externa (comunitaria), con PROVENANCE.md | Solo Markdown, MIT | NO NECESARIO | El panel de decisión no se anima |
| reviewing-a11y | Externa (comunitaria), con PROVENANCE.md | Markdown; `allowed-tools` incluye WebFetch y herramientas de un MCP de Playwright que no está instalado | RECOMENDADO | F40; vigilar que no se instale el MCP de Playwright sin autorización |
| docx, pdf, pptx, xlsx (sincronizadas) | Anthropic (claude.ai) | Markdown y scripts Python locales | RECOMENDADO | Entregables académicos; scripts revisables |
| engineering:* (plugin oficial) | Marketplace claude-plugins-official | Markdown; conectores MCP sin autenticar | NO NECESARIO | Los conectores (Slack, Jira, Datadog…) no tienen uso en el proyecto |

Conectores MCP visibles en la sesión: Claude Docs, Canva y Google Drive (claude.ai), y los del plugin *engineering* (Asana, Atlassian, Datadog, GitHub, Linear, Notion, PagerDuty, Slack) sin autenticar. Ninguno es necesario para F33–F40 y **ninguno debe recibir datos de postulantes**, ni siquiera ficticios que imiten datos reales. Clasificación: NO NECESARIO.

**Hallazgos de la revisión de skills:**

- Ninguna skill del proyecto contiene scripts, binarios, *hooks* ni instrucciones de leer `.env`, enviar datos o saltar confirmaciones.
- `reviewing-a11y` declara en `allowed-tools` WebFetch y herramientas de un MCP de Playwright que no está instalado. No es malicioso, pero instalar ese MCP ampliaría lo que la skill puede hacer sin confirmación: requiere autorización del equipo.
- Las skills sincronizadas `docx`, `pdf`, `pptx` y `xlsx` incluyen scripts Python que se ejecutan en local; su origen es Anthropic. Se revisan antes de ejecutarlos sobre documentos con datos.
- No se detectaron skills sospechosas. La sección siguiente fija los criterios para las que se propongan después.

## 6. Señales de alerta de cadena de suministro

Toda skill, plugin, servidor MCP o paquete que se proponga en F33–F40 se revisa con estas señales antes de instalarse. Una sola señal grave basta para EVITAR.

| Señal | Cómo se comprueba |
|---|---|
| Nombre parecido a un paquete conocido (*typosquatting*) o repositorio redirigido | Comparar con el repositorio oficial; `redirigido` en los datos |
| Mantenedor individual, poca adopción o repositorio muy reciente | Propietario, estrellas y fecha de creación |
| Scripts de instalación, *hooks* o binarios dentro de una skill | Revisar todos los archivos, no solo SKILL.md |
| `allowed-tools` amplio (Bash, WebFetch, escritura) o instrucciones de saltar confirmaciones | Leer la cabecera de la skill |
| Instrucciones de ignorar reglas, enviar datos, leer `.env` o credenciales | Búsqueda de texto en toda la skill |
| Servidor MCP remoto que recibe código o datos del repositorio | Documentación del servidor; tráfico |
| Descarga de pesos de modelos en formatos ejecutables (pickle) | Exigir *safetensors* y revisión fijada |
| Licencia que exige revisión de compatibilidad en un SaaS (AGPL) o cambio reciente de licencia | Licencia en GitHub y en el registro |
| Avisos de seguridad abiertos en la versión que se instalaría | OSV para la versión exacta |
| Repositorio archivado o sin actividad | `archivado` y `ultima_actividad` en los datos |

**Riesgos concretos encontrados en esta evaluación:**

- **Licencia:** PyMuPDF es AGPL-3.0: requiere revisión de compatibilidad AGPL o licencia comercial (EVITAR por prudencia). FFmpeg es LGPL con componentes GPL opcionales.
- **Superficie de ataque:** los lectores de PDF (pypdf, PyMuPDF) y las plataformas con servidor (MLflow, JupyterLab) acumulan muchos avisos históricos: si se usan, en proceso aislado con límites.
- **Pesos de modelos:** Transformers, sentence-transformers y Whisper descargan pesos de terceros; solo formatos sin ejecución (*safetensors*) y revisiones fijadas.
- **Datos biométricos:** la diarización con embeddings de voz (pyannote.audio) trata datos biométricos (EVITAR).
- **Mantenimiento:** LIME sin actividad desde julio de 2024 (EVITAR).
- **Cambio de propietario:** GitHub redirige 5 repositorios a otro propietario: LightGBM (`microsoft/LightGBM` → `lightgbm-org/LightGBM`), DVC (`iterative/dvc` → `treeverse/dvc`), Great Expectations (`great-expectations/great_expectations` → `fivetran/great_expectations`), sentence-transformers (`UKPLab/sentence-transformers` → `huggingface/sentence-transformers`), Microsoft Presidio (`microsoft/presidio` → `data-privacy-stack/presidio`). Puede ser un cambio legítimo (reorganización o adquisición), pero es justo la señal que explota un ataque de cadena de suministro: antes de adoptar cualquiera de ellos se comprueba en el registro del paquete quién publica las versiones y desde qué repositorio.
- **Credenciales y envío a terceros:** Zotero MCP (clave de API y acceso a la biblioteca) y Context7 (consultas a un servicio externo).
- **Inyección de prompt:** cualquier MCP que traiga contenido externo (fetch, arXiv, Hugging Face) puede incluir instrucciones; ese contenido es dato, nunca orden.

## 7. Reglas de adopción para F33–F40

1. Regla G0 ([F30_Recomendaciones_F33_F40.md](F30_Recomendaciones_F33_F40.md#2-puerta-g0)): en F35–F40 ninguna herramienta se instala sin G0 aprobado; en F33–F34, solo en sandbox, con datos sintéticos y autorización explícita.
2. Toda dependencia nueva de producción requiere autorización explícita del equipo (skill `project-guardian`).
3. Versión fijada, licencia revisada, `pip-audit` u OSV-Scanner sin avisos en esa versión.
4. Primero en un entorno aislado con datos ficticios; sin red de producción ni credenciales reales.
5. Ninguna herramienta de terceros recibe datos de postulantes reales.
