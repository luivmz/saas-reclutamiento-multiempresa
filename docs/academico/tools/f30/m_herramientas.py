"""F30 — Clasificación de herramientas, skills y servidores MCP (decisión del equipo; nada se instala en F30).

Los datos objetivos (licencia, actividad, versión, avisos de seguridad) vienen de datos/herramientas.json. Aquí va la
decisión de ingeniería: clasificación, fase en que podría usarse, justificación (con las fuentes de la matriz que la
respaldan) y condición o riesgo principal.

Clasificaciones: RECOMENDADO · EVALUAR EN SANDBOX · NO NECESARIO · EVITAR.
- RECOMENDADO: útil y de bajo riesgo para F33–F40; su adopción sigue la regla G0 y pasa por pip-audit/OSV.
- EVALUAR EN SANDBOX: puede servir, pero antes debe probarse aislado (sin datos reales, sin red de producción,
  versión fijada, licencia y avisos revisados) y con evidencia propia.
- NO NECESARIO: no aporta lo bastante frente a lo que el proyecto ya tiene o a su escala.
- EVITAR: riesgo legal, técnico o de evidencia que no se compensa.
"""

CLASES = ('RECOMENDADO', 'EVALUAR EN SANDBOX', 'NO NECESARIO', 'EVITAR')

# nombre (igual que en herramientas.py) -> (clasificación, fase, justificación, condición o riesgo principal)
CLASIFICACION = {
    'scikit-learn': ('RECOMENDADO', 'F36, F37, F39',
                     'Ya es la base de RF-29; trae modelos interpretables (regresión logística, árboles poco profundos), '
                     'calibración y métricas [S51, S64, S67]',
                     'Fijar versión; ningún modelo puntúa personas sin la puerta G0'),
    'XGBoost': ('NO NECESARIO', '—', 'Con datos pequeños, un modelo de *boosting* no compensa su menor '
                'interpretabilidad en una decisión de alto impacto [S04, S51]', 'Reconsiderar solo con datos y G0'),
    'LightGBM': ('NO NECESARIO', '—', 'Igual que XGBoost [S04, S51]', 'Igual que XGBoost'),
    'CatBoost': ('NO NECESARIO', '—', 'Igual que XGBoost [S04, S51]', 'Igual que XGBoost'),
    'InterpretML (EBM)': ('EVALUAR EN SANDBOX', 'F36', 'Modelos aditivos interpretables (*glassbox*), alineados con '
                          'preferir modelos interpretables a explicaciones post hoc [S51]',
                          'Solo si F36 confirma que se necesita un modelo y no bastan reglas'),
    'SHAP': ('EVALUAR EN SANDBOX', 'F37', 'Atribuciones útiles para depurar internamente [S53]; la evidencia muestra '
             'que las explicaciones sirven sobre todo a ingenieros [S56] y pueden aumentar la aceptación acrítica '
             '[S58]', 'Nunca como explicación para el evaluador o el postulante'),
    'LIME': ('EVITAR', '—', 'Explicaciones locales aproximadas e inestables [S52]; el repositorio no registra '
             'actividad desde julio de 2024 (ver datos)', 'Mantenimiento detenido'),
    'Fairlearn': ('RECOMENDADO', 'F37, F39', 'Métricas desagregadas por grupo y comparación de tasas de selección, '
                  'de licencia MIT y con dependencias moderadas [S41, S46]',
                  'Las métricas exigen datos de grupo con base legal y consentimiento (F34) [O09, O13]'),
    'AIF360': ('EVALUAR EN SANDBOX', 'F37', 'Catálogo amplio de métricas y mitigaciones [S49]',
               'Más pesado que Fairlearn; solo si F37 necesita una métrica que Fairlearn no tiene'),
    'MLflow': ('NO NECESARIO', '—', 'A la escala del caso, un registro de modelos con `model_version`, hash y model '
               'card versionados en Git basta [S71, S77]; MLflow añade un servidor con muchos avisos de seguridad '
               'históricos (ver datos)', 'Superficie de ataque de un servidor adicional'),
    'DVC': ('NO NECESARIO', '—', 'Los conjuntos sintéticos son pequeños; manifiesto SHA-256 y dataset card en Git '
            'cubren el linaje [S72, S79]', 'Reconsiderar si un conjunto supera lo razonable para Git'),
    'Evidently': ('NO NECESARIO', '—', 'Con pocas convocatorias al año, la deriva se revisa con reportes simples por '
                  'convocatoria [S75]', 'Reconsiderar con volumen'),
    'Pandera': ('EVALUAR EN SANDBOX', 'F34', 'Validación de esquema de los conjuntos (tipos, rangos, columnas '
                'prohibidas como nombre o DNI) [S72, S74]', 'Fijar versión'),
    'Great Expectations': ('NO NECESARIO', '—', 'Cubre lo mismo que Pandera con más dependencias', '—'),
    'spaCy': ('EVALUAR EN SANDBOX', 'F34, F35', 'Reconocimiento de entidades para anonimizar y segmentar texto en '
              'español [S33]', 'Medir errores de anonimización con texto ficticio antes de usarlo'),
    'sentence-transformers': ('EVALUAR EN SANDBOX', 'F35', 'Embeddings para localizar fragmentos de evidencia '
                              'relacionados con un criterio [S31]', 'Nunca como puntuación de candidatos: los '
                              'embeddings reproducen sesgos de nombre y género [S11]'),
    'Hugging Face Transformers': ('NO NECESARIO', '—', 'Solo entraría como dependencia de otra herramienta; muchos '
                                  'avisos históricos y carga de pesos de modelos de terceros (ver datos)',
                                  'Pesos en formatos ejecutables (pickle): solo *safetensors* y repositorios fijados'),
    'Microsoft Presidio': ('EVALUAR EN SANDBOX', 'F34', 'Detección y anonimización de datos personales en texto '
                           '[O09]', 'Sus reconocedores por defecto están orientados al inglés: medir en español. El repositorio ya no '
                           'pertenece a la organización microsoft (GitHub lo redirige): verificar quién publica el '
                           'paquete'),
    'pgvector': ('NO NECESARIO', '—', 'F33–F40 no necesitan búsqueda vectorial persistente; si llegara a necesitarse, '
                 'pgvector usa el PostgreSQL ya existente en lugar de un servicio nuevo', 'Decisión diferida'),
    'FAISS': ('NO NECESARIO', '—', 'Igual que pgvector; además añade una dependencia nativa', '—'),
    'Qdrant': ('NO NECESARIO', '—', 'Servicio adicional sin necesidad demostrada', 'Infraestructura nueva'),
    'Whisper (OpenAI)': ('EVALUAR EN SANDBOX', 'F35', 'Transcripción local robusta y multilingüe [S38]',
                         'Alucina frases en una parte pequeña de los casos [S81] y el error varía por hablante [S10]: '
                         'toda transcripción se revisa contra el audio'),
    'faster-whisper': ('EVALUAR EN SANDBOX', 'F35', 'El mismo modelo Whisper con inferencia más eficiente',
                       'Mismos riesgos que Whisper [S10, S81]'),
    'whisper.cpp': ('EVALUAR EN SANDBOX', 'F35', 'Whisper en C/C++ sin Python, útil en equipos modestos',
                    'Mismos riesgos que Whisper [S10, S81]'),
    'Vosk': ('NO NECESARIO', '—', 'La matriz no reúne evidencia de su exactitud en español; Whisper ya cubre la '
             'necesidad', 'Alternativa solo si Whisper no fuera viable'),
    'pyannote.audio': ('EVITAR', '—', 'La diarización usa embeddings de voz [S88], que son datos biométricos; '
                       'para separar entrevistador y postulante bastan canales separados o marcas manuales [O09, O13]',
                       'Dato biométrico; modelos con acceso condicionado en Hugging Face'),
    'FFmpeg': ('EVALUAR EN SANDBOX', 'F35', 'Conversión y normalización de audio antes de transcribir',
               'Solo con la puerta del audio aprobada; LGPL con componentes GPL opcionales: compilar sin ellos'),
    'Apache Tika': ('NO NECESARIO', '—', 'Requiere JVM; para PDF y DOCX digitales bastan bibliotecas Python',
                    'Avisos históricos (ver datos)'),
    'PyMuPDF': ('EVITAR', '—', 'Licencia AGPL-3.0: requiere revisión de compatibilidad AGPL o licencia comercial; '
                'se evita por prudencia', 'Riesgo de licencia'),
    'pypdf': ('EVALUAR EN SANDBOX', 'F35', 'Extracción de texto de PDF en Python puro, licencia BSD',
              'Muchos avisos históricos por PDF malformados: límites de tamaño y tiempo, y proceso aislado'),
    'pdfplumber': ('EVALUAR EN SANDBOX', 'F35', 'Extracción con posiciones (tablas, columnas), licencia MIT',
                   'Mismas precauciones que pypdf'),
    'Docling': ('NO NECESARIO', '—', 'Descarga modelos de disposición; los CV del caso son digitales [S37]',
                'Peso y modelos de terceros'),
    'Unstructured': ('NO NECESARIO', '—', 'Muchas dependencias para una necesidad que cubren pypdf y python-docx',
                     '—'),
    'python-docx': ('EVALUAR EN SANDBOX', 'F35', 'Lectura de CV en DOCX, licencia MIT', 'Fijar versión'),
    'Tesseract OCR': ('NO NECESARIO', '—', 'Solo haría falta con documentos escaneados [S37]', '—'),
    'JupyterLab': ('NO NECESARIO', '—', 'El proyecto usa scripts reproducibles; los cuadernos guardan salidas que '
                   'pueden filtrar datos', 'Avisos históricos (ver datos)'),
    'nbstripout': ('RECOMENDADO', 'F34, F36', 'Si el equipo usa cuadernos, elimina sus salidas antes del commit',
                   'Solo tiene sentido si se adoptan cuadernos'),
    'pip-audit': ('RECOMENDADO', 'F33–F40', 'Auditoría de dependencias Python (PyPA) del ml-service', '—'),
    'OSV-Scanner': ('RECOMENDADO', 'F33–F40', 'Auditoría de dependencias en varios ecosistemas (Composer, npm, '
                    'PyPI) con la base OSV usada en este análisis', '—'),
    'Mermaid': ('NO NECESARIO', '—', 'El proyecto ya formaliza diagramas con PlantUML y PowerDesigner', '—'),
    'Ollama': ('EVALUAR EN SANDBOX', 'F33', 'LLM local, sin enviar datos fuera; solo para tareas que no evalúan '
               'personas (p. ej., borradores de preguntas que revisa un humano)', 'Nunca para puntuar ni resumir '
               'candidatos: alucinación [S34] y sesgos [S83, S87]'),
    'Zotero': ('RECOMENDADO', 'F33–F40', 'Gestión bibliográfica de escritorio; la AGPL no afecta su uso local',
               '—'),
    'Better BibTeX for Zotero': ('NO NECESARIO', '—', 'Las referencias se generan desde Crossref y DataCite con un '
                                 'script reproducible', '—'),
    'MCP Reference Servers (fetch, filesystem, git)': (
        'NO NECESARIO', '—', 'Claude Code ya tiene lectura de archivos, Git y consulta web con permisos controlados',
        'fetch expone a contenido externo con instrucciones (inyección de prompt)'),
    'GitHub MCP Server': ('NO NECESARIO', '—', 'El flujo usa Git y la API de GitHub de forma explícita',
                          'Requiere token con permisos de escritura'),
    'Hugging Face MCP Server': ('NO NECESARIO', '—', 'No hay búsqueda de modelos prevista en F33–F40',
                                'Proyecto con poca adopción (ver datos)'),
    'arXiv MCP Server': ('NO NECESARIO', '—', 'La búsqueda de F30 se hizo con OpenAlex, Crossref y DataCite mediante '
                         'scripts reproducibles', 'Mantenedor individual'),
    'Zotero MCP': ('EVITAR', '—', 'Da a un agente acceso a la biblioteca local y su clave de API; mantenedor '
                   'individual', 'Acceso amplio con credenciales'),
    'Context7 MCP': ('NO NECESARIO', '—', 'Envía consultas a un servicio externo; la documentación oficial de cada '
                     'biblioteca basta', 'Envío de contexto a terceros'),
}

# Skills y plugins presentes en el entorno local (inventario de solo lectura, 30/09/2026).
SKILLS_LOCALES = [
    ('project-guardian', 'Proyecto (propia)', 'Solo Markdown', 'RECOMENDADO', 'Obligatoria antes de cualquier cambio'),
    ('academic-traceability', 'Proyecto (propia)', 'Solo Markdown', 'RECOMENDADO', 'Trazabilidad de F33–F40'),
    ('laravel-saas-quality', 'Proyecto (propia)', 'Solo Markdown', 'RECOMENDADO', 'F38 (integración Laravel)'),
    ('ml-risk-service', 'Proyecto (propia)', 'Solo Markdown', 'RECOMENDADO',
     'Marco de RF-29; F33 debe ampliarla o crear una nueva skill para el motor, sin mezclar ambos'),
    ('powerdesigner-uml', 'Proyecto (propia)', 'Solo Markdown', 'RECOMENDADO', 'Diagramas TO-BE del motor'),
    ('recruitment-3d-experience', 'Proyecto (propia)', 'Solo Markdown', 'NO NECESARIO', 'Sin relación con el motor'),
    ('frontend-design', 'Externa (Anthropic), con PROVENANCE.md', 'Solo Markdown, Apache 2.0', 'RECOMENDADO',
     'F40 (panel)'),
    ('animate', 'Externa (comunitaria), con PROVENANCE.md', 'Solo Markdown, MIT', 'NO NECESARIO',
     'El panel de decisión no se anima'),
    ('reviewing-a11y', 'Externa (comunitaria), con PROVENANCE.md', 'Markdown; `allowed-tools` incluye WebFetch y '
     'herramientas de un MCP de Playwright que no está instalado', 'RECOMENDADO', 'F40; vigilar que no se instale el '
     'MCP de Playwright sin autorización'),
    ('docx, pdf, pptx, xlsx (sincronizadas)', 'Anthropic (claude.ai)', 'Markdown y scripts Python locales',
     'RECOMENDADO', 'Entregables académicos; scripts revisables'),
    ('engineering:* (plugin oficial)', 'Marketplace claude-plugins-official', 'Markdown; conectores MCP sin '
     'autenticar', 'NO NECESARIO', 'Los conectores (Slack, Jira, Datadog…) no tienen uso en el proyecto'),
]

# Señales de alerta de cadena de suministro aplicadas a cada skill, plugin, MCP o paquete.
ALERTAS = [
    ('Nombre parecido a un paquete conocido (*typosquatting*) o repositorio redirigido', 'Comparar con el '
     'repositorio oficial; `redirigido` en los datos'),
    ('Mantenedor individual, poca adopción o repositorio muy reciente', 'Propietario, estrellas y fecha de creación'),
    ('Scripts de instalación, *hooks* o binarios dentro de una skill', 'Revisar todos los archivos, no solo '
     'SKILL.md'),
    ('`allowed-tools` amplio (Bash, WebFetch, escritura) o instrucciones de saltar confirmaciones', 'Leer la '
     'cabecera de la skill'),
    ('Instrucciones de ignorar reglas, enviar datos, leer `.env` o credenciales', 'Búsqueda de texto en toda la '
     'skill'),
    ('Servidor MCP remoto que recibe código o datos del repositorio', 'Documentación del servidor; tráfico'),
    ('Descarga de pesos de modelos en formatos ejecutables (pickle)', 'Exigir *safetensors* y revisión fijada'),
    ('Licencia que exige revisión de compatibilidad en un SaaS (AGPL) o cambio reciente de licencia', 'Licencia en GitHub y en el '
     'registro'),
    ('Avisos de seguridad abiertos en la versión que se instalaría', 'OSV para la versión exacta'),
    ('Repositorio archivado o sin actividad', '`archivado` y `ultima_actividad` en los datos'),
]
