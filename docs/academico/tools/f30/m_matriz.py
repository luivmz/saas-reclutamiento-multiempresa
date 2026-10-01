"""F30 — Matriz de evidencia científica: campos analíticos por fuente.

Los metadatos bibliográficos (autores, año, revista o conferencia, DOI/URL, tipo) NO se escriben aquí: el generador
los toma de datos/verificacion_fuentes.json (Crossref, DataCite o HTTP). Aquí solo va el análisis, escrito a partir del
resumen publicado de cada trabajo (OpenAlex) o, cuando no hay resumen disponible, con una descripción general sin cifras
marcada con «(sin resumen disponible; descripción general)».

Campos: revision · objetivo · datos · tecnica · variables · metricas · resultados · limitaciones · sesgo ·
aplicabilidad · decision · confianza (FUERTE, MODERADA, LIMITADA, CONFLICTIVA, INSUFICIENTE).
"""

NIVELES = ('FUERTE', 'MODERADA', 'LIMITADA', 'CONFLICTIVA', 'INSUFICIENTE')
SI, PRE = 'Sí', 'No (preprint)'
SR = '(sin resumen disponible; descripción general)'


def M(revision, objetivo, datos, tecnica, variables, metricas, resultados, limitaciones, sesgo, aplicabilidad,
      decision, confianza):
    assert confianza in NIVELES, confianza
    return dict(revision=revision, objetivo=objetivo, datos=datos, tecnica=tecnica, variables=variables,
                metricas=metricas, resultados=resultados, limitaciones=limitaciones, sesgo=sesgo,
                aplicabilidad=aplicabilidad, decision=decision, confianza=confianza)


MATRIZ = {
    # ------------------------------------------------------------------ A. IA en reclutamiento y ética
    'S01': M(SI, 'Analizar afirmaciones y prácticas de proveedores de evaluaciones algorítmicas de preempleo',
             'Información pública de proveedores comerciales', 'Análisis documental técnico y jurídico',
             'Datos usados, objetivo de predicción, validación, des-sesgo declarado', 'Cualitativo',
             'Las decisiones sobre datos y objetivo de predicción crean riesgos; el des-sesgo técnico interactúa de forma '
             'compleja con la ley antidiscriminación', 'Solo lo que los proveedores publican; contexto EE. UU.',
             'Objetivos de predicción basados en decisiones históricas heredan sesgo',
             'Directa: advierte sobre elegir «etiquetas» de contratación pasada',
             'No entrenar con decisiones históricas como etiqueta; documentar validación y sesgo', 'MODERADA'),
    'S02': M(SI, 'Revisar la literatura sobre discriminación y equidad en decisiones algorítmicas de RR. HH.',
             '36 artículos (2014–2020)', 'Revisión sistemática', 'Aplicaciones en reclutamiento y desarrollo',
             'Cualitativo', 'El conocimiento sobre discriminación implícita en RR. HH. es aún escaso; identifica riesgos '
             'y vacíos', 'Corpus pequeño y temprano', 'Riesgo de discriminación implícita y percepción de injusticia',
             'Alta para el marco de riesgos', 'Tratar la equidad como requisito de diseño, no como añadido', 'MODERADA'),
    'S03': M(SI, 'Mapear oportunidades, riesgos y ambigüedades éticas de la IA en reclutamiento',
             '51 artículos', 'Revisión sistemática', 'Etapas: anuncios, cribado de CV, entrevistas en vídeo',
             'Cualitativo', 'Identifica riesgos éticos (incluido el análisis facial en vídeo) y medidas de mitigación',
             'Literatura emergente; pocos estudios empíricos', 'Opacidad, discriminación, privacidad',
             'Alta: cubre las mismas etapas que la visión F33–F40', 'Excluir análisis facial; priorizar transparencia',
             'MODERADA'),
    'S04': M(SI, 'Identificar retos del uso de ciencia de datos en RR. HH.', 'Ensayo conceptual con casos',
             'Análisis conceptual', 'Complejidad de fenómenos de RR. HH., datos pequeños, rendición de cuentas',
             'Cualitativo', 'Propone razonamiento causal, aleatorización y participación de los empleados',
             'Sin datos empíricos propios', 'Conjuntos pequeños y etiquetas débiles',
             'Muy alta: un colegio genera pocos procesos por año', 'Asumir datos pequeños: reglas y rúbricas antes que ML',
             'MODERADA'),
    'S05': M(SI, 'Estudiar la discriminación algorítmica en reclutamiento y sus soluciones',
             'Revisión de literatura y encuesta', 'Revisión + teoría fundamentada',
             'Género, raza, rasgos de personalidad', 'Cualitativo',
             'El sesgo proviene de datos limitados y del diseño; recomienda medidas técnicas y de gobernanza',
             'Método mixto con muestra no detallada en el resumen', 'Datos históricos sesgados',
             'Media', 'Combinar controles técnicos con gobernanza interna y supervisión externa', 'LIMITADA'),
    'S06': M(SI, 'Medir la reacción de las personas a entrevistas altamente automatizadas',
             'N = 123; experimento 2 × 2 preregistrado', 'Experimento con viñetas en vídeo',
             'Automatización (alta / videoconferencia) × consecuencias (selección / formación)',
             'Aceptación, presencia social, equidad percibida, controlabilidad',
             'La entrevista automatizada redujo la aceptación por menor presencia social y equidad percibida; en alto riesgo '
             'generó ambigüedad', 'Observadores, no postulantes reales', 'No aplica',
             'Alta: la entrevista del colegio debe seguir siendo humana', 'No automatizar la conducción de la entrevista',
             'MODERADA'),
    'S07': M(SI, 'Evaluar fiabilidad y validez de evaluaciones de personalidad por entrevista en vídeo automatizada',
             'Varias muestras (resumen parcial en OpenAlex)', 'Modelos de ML sobre entrevistas en vídeo',
             'Rasgos de personalidad (autoinforme vs. informe del entrevistador)', 'Fiabilidad, validez convergente y '
             'discriminante, generalización', 'Evidencia escasa de validez cuando se entrenan con autoinformes; mixta con '
             'informes del entrevistador', 'Contextos de laboratorio y académicos', 'Constructo psicológico inferido',
             'Directa: sustenta no inferir personalidad', 'Prohibir puntuaciones de personalidad desde vídeo', 'MODERADA'),
    'S08': M(SI, 'Examinar si la emoción puede inferirse de los movimientos faciales',
             'Revisión de la evidencia científica sobre 6 categorías emocionales', 'Revisión crítica amplia',
             'Configuraciones faciales y emoción', 'Cualitativo',
             'La expresión de emociones varía mucho entre culturas, situaciones y personas; una misma configuración facial '
             'expresa varias emociones o algo distinto de una emoción', 'Se centra en 6 emociones básicas',
             'Inferencias poco generalizables entre culturas', 'Directa: la evidencia no respalda que el reconocimiento de emociones en entrevistas sea fiable ni '
             'generalizable para un uso de alto impacto',
             'Prohibir inferir emociones o estados desde rostro o voz', 'FUERTE'),
    'S09': M(SI, 'Analizar los modelos conceptuales y datos proxy del reconocimiento automático de emociones',
             'Análisis conceptual', 'Taxonomía crítica', 'Modelos de emoción, datos proxy', 'Cualitativo',
             'No debe asumirse que estos sistemas producen una «verdad de terreno» sobre emociones', 'Conceptual',
             'Proxies culturalmente sesgados', 'Directa', 'Misma decisión que S08', 'MODERADA'),
    'S10': M(SI, 'Medir disparidades raciales en reconocimiento automático del habla',
             '5 sistemas comerciales; entrevistas estructuradas con 42 hablantes blancos y 73 negros; 19,8 h', 'Auditoría comparativa',
             'Raza del hablante; frases idénticas', 'WER',
             'WER promedio 0,35 en hablantes negros frente a 0,19 en blancos; la brecha se atribuye a los modelos '
             'acústicos', 'Inglés de EE. UU.; sistemas de 2019', 'Disparidad por variedad dialectal',
             'Alta: el STT puede degradar la evidencia de ciertos hablantes (p. ej., variedades del español andino)',
             'Medir WER por variedad de habla antes de usar STT; revisión humana de transcripciones', 'MODERADA'),
    'S11': M(SI, 'Auditar sesgos de modelos de embeddings en cribado de CV', '>500 CV públicos, 500 descripciones de '
             'puesto, 9 ocupaciones', 'Auditoría por recuperación (Massive Text Embeddings)', 'Nombres asociados a raza y '
             'género', 'Tasa de preferencia por grupo', 'Preferencia por nombres asociados a personas blancas en 85,1 % '
             'de los casos; hombres negros desfavorecidos hasta en el 100 % de los casos', 'Nombres como proxy; EE. UU.',
             'Embeddings reproducen sesgos sociales', 'Directa para matching semántico',
             'No usar similitud de embeddings como puntuación de candidatos sin auditoría; ocultar nombres', 'MODERADA'),
    # ------------------------------------------------------------------ C/D. Selección de personal
    'S12': M(SI, 'Resumir 85 años de investigación sobre validez de métodos de selección', 'Metaanálisis de 19 métodos',
             'Síntesis metaanalítica', 'Métodos de selección y desempeño', 'Validez de criterio',
             'Las combinaciones de capacidad cognitiva con muestra de trabajo, prueba de integridad o entrevista '
             'estructurada tuvieron las mayores validez (≈ 0,63–0,65)', 'Correcciones de rango revisadas después por S13',
             'Sobreestimación por correcciones', 'Media: contexto histórico', 'Usar con la revisión de S13', 'CONFLICTIVA'),
    'S13': M(SI, 'Revisar estimaciones metaanalíticas de validez en selección', 'Reanálisis de metaanálisis previos',
             'Revisión de correcciones por restricción de rango', 'Métodos de selección', 'Validez de criterio',
             'Validez sobreestimada antes en 0,10–0,20; la entrevista estructurada queda en el primer lugar',
             'Sigue dependiendo de estudios primarios', 'No aplica',
             'Muy alta: sustenta la entrevista estructurada como método central', 'Basar la evaluación en entrevista '
             'estructurada con rúbrica', 'FUERTE'),
    'S14': M(SI, 'Metaanalizar la validez de la entrevista de empleo', '245 coeficientes; 86 311 personas',
             'Metaanálisis', 'Contenido, estructura, formato, criterio', 'Validez',
             'La entrevista estructurada supera a la no estructurada; las situacionales superan a las psicológicas',
             'Datos antiguos', 'No aplica', 'Alta', 'Preguntas situacionales y de conducta pasada, no psicológicas', 'FUERTE'),
    'S15': M(SI, 'Describir y evaluar los componentes de la estructura de una entrevista', 'Revisión de literatura',
             'Revisión narrativa', '15 componentes de estructura', 'Fiabilidad, validez, reacciones',
             'La estructura mejora las propiedades psicométricas; identifica 15 componentes',
             'Narrativa', 'No aplica', 'Muy alta: guía para la rúbrica de entrevista',
             'Mismas preguntas, escalas ancladas y calificación por pregunta', 'MODERADA'),
    'S16': M(SI, 'Revisar 20 años de investigación sobre entrevista estructurada', 'Revisión narrativa y metaanalítica',
             'Revisión mixta', 'Sesgo, gestión de impresiones, escalas, preguntas', 'Varias',
             'Mucho se sabe; 12 proposiciones y 19 preguntas abiertas', 'Preguntas no resueltas', 'Gestión de impresiones',
             'Alta', 'Escalas de calificación ancladas y sondeo controlado', 'FUERTE'),
    'S17': M(SI, 'Proponer buenas prácticas de modelado por competencias', 'Experiencia aplicada y académica',
             'Revisión de prácticas', 'Análisis, organización y uso de competencias', 'Cualitativo',
             '20 buenas prácticas; diferencia y complementariedad con el análisis de puestos', 'Recomendaciones de expertos',
             'No aplica', 'Muy alta: base de criterios por vacante', 'Competencias derivadas de análisis del puesto',
             'MODERADA'),
    'S18': M(SI, 'Revisar la evolución del análisis de puestos y el modelado de competencias', 'Revisión',
             'Revisión narrativa', 'Actividades, atributos, contexto de trabajo', 'Cualitativo',
             'Propone nuevas formas de análisis del trabajo y una agenda para competencias', 'Narrativa', 'No aplica',
             'Alta', 'Hacer análisis del puesto antes de definir criterios', 'MODERADA'),
    'S19': M(SI, 'Proponer escalas de calificación ancladas en conducta (BARS) ' + SR, 'Desarrollo de escalas',
             'Retraducción de expectativas', 'Anclas conductuales', 'Cualitativo',
             'Método para escalas con anclas conductuales no ambiguas', 'Antiguo', 'No aplica', 'Alta',
             'Usar anclas conductuales por nivel en cada criterio', 'MODERADA'),
    'S20': M(SI, 'Guiar la elección del coeficiente de correlación intraclase', 'Metodológico', 'Estadística',
             'n objetos calificados por k jueces', 'ICC', 'Seis formas de ICC según el modelo y el uso',
             'Metodológico', 'No aplica', 'Alta: fiabilidad entre evaluadores', 'Medir acuerdo entre evaluadores con ICC',
             'FUERTE'),
    'S21': M(SI, 'Guía de selección y reporte del ICC', 'Metodológico', 'Estadística', 'Formas de ICC', 'ICC e IC 95 %',
             'Hay 10 formas de ICC; debe reportarse modelo, tipo y definición', 'Tiene una errata registrada en Crossref',
             'No aplica', 'Alta', 'Reportar el ICC con su forma e intervalo', 'FUERTE'),
    'S22': M(SI, 'Metaanalizar la validez predictiva de la selección de docentes', '32 estudios en condiciones reales',
             'Metaanálisis', 'Predictores académicos y no académicos', 'Correlación con eficacia docente',
             'Efecto global pequeño pero significativo (r = 0,12)', 'Medidas de eficacia heterogéneas', 'No aplica',
             'Muy alta: caso docente', 'Ser prudente con la capacidad predictiva en docentes; apoyo, no predicción',
             'FUERTE'),
    'S23': M(SI, 'Revisar procedimientos de selección digitales', 'Revisión focalizada', 'Revisión',
             'Aplicaciones en línea, pruebas, entrevistas digitales, gamificación, redes sociales',
             'Validez y reacciones', 'Base de evidencia desigual; agenda de investigación', 'Evidencia limitada',
             'Uso de redes sociales', 'Media', 'No usar redes sociales del postulante', 'MODERADA'),
    'S24': M(SI, 'Identificar qué constructos mide la entrevista', '338 calificaciones de 47 estudios', 'Metaanálisis',
             'Taxonomía de 7 constructos', 'Frecuencia y validez', 'La mayor validez de la entrevista estructurada se '
             'explica en parte por medir constructos más ligados al desempeño', 'Datos de estudios publicados',
             'No aplica', 'Alta', 'Definir qué competencia mide cada pregunta', 'MODERADA'),
    # ------------------------------------------------------------------ B/E/F/G/H. Matching, NLP, recomendación
    'S25': M(SI, 'Modelar el ajuste persona-puesto con redes neuronales', 'Postulaciones históricas',
             'CNN bipartita (PJFNN)', 'Texto de requisitos y de experiencia', 'Precisión de ajuste',
             'Estima el ajuste e identifica qué requisitos cumple el candidato', 'Requiere grandes datos históricos',
             'Aprende de decisiones pasadas', 'Baja: no hay volumen de datos en el caso', 'Descartar deep learning de '
             'matching para el caso', 'LIMITADA'),
    'S26': M(SI, 'Ajuste persona-puesto consciente de habilidades con mejor interpretación', 'Postulaciones históricas',
             'Red neuronal con atención (APJFNN)', 'Representaciones de requisitos y experiencia', 'Precisión',
             'Mejora la interpretación del ajuste frente a modelos previos', 'Datos de una plataforma',
             'Etiquetas de decisiones pasadas', 'Baja por datos', 'Igual que S25', 'LIMITADA'),
    'S27': M(SI, 'Revisión sistemática de recomendadores de e-recruitment ' + SR, 'Literatura', 'Revisión sistemática',
             'Enfoques de recomendación', 'Varias', 'Panorama de técnicas y retos', 'Ver la publicación', 'Varios',
             'Media', 'Contexto para F40', 'MODERADA'),
    'S28': M(SI, 'Identificar retos de los recomendadores de e-recruitment', 'Literatura', 'Revisión por retos',
             'Retos: datos, bidireccionalidad, equidad, explicabilidad', 'Varias',
             'Organiza la literatura por retos prácticos', 'Revisión', 'Equidad e impacto en carreras', 'Media',
             'Tratar equidad y explicación como requisitos del ranking', 'MODERADA'),
    'S29': M(SI, 'Extraer habilidades duras y blandas de avisos de empleo ' + SR, 'Corpus anotado de avisos en inglés',
             'Etiquetado de secuencias con modelos tipo BERT', 'Tramos de habilidad', 'F1 por tramo',
             'Conjunto de datos y referencias para extracción de habilidades', 'Inglés; avisos, no CV',
             'Anotación subjetiva de habilidades blandas', 'Media: la extracción en español requiere datos propios',
             'Extracción de habilidades como sugerencia revisada por humanos', 'MODERADA'),
    'S30': M(SI, 'Revisar la identificación de habilidades en avisos de empleo', '108 artículos', 'Revisión sistemática',
             'Bases de habilidades, métodos, granularidad', 'Varias', 'Clasifica métodos y aplicaciones; retos abiertos',
             'Avisos, no CV', 'Taxonomías no neutrales', 'Media', 'Usar una taxonomía explícita (p. ej., ESCO) si se '
             'extraen habilidades', 'MODERADA'),
    'S31': M(SI, 'Obtener embeddings de oraciones eficientes ' + SR, 'Corpus de similitud y NLI',
             'Redes siamesas sobre BERT (SBERT)', 'Pares de oraciones', 'Correlación con similitud humana',
             'Embeddings comparables por coseno con mucho menor costo que comparar con BERT completo',
             'Similitud general, no ajuste laboral', 'Hereda sesgos del preentrenamiento (ver S11)', 'Media',
             'Similitud semántica solo para encontrar evidencia, no para puntuar', 'FUERTE'),
    'S32': M(SI, 'Revisar críticamente cómo se estudia el «sesgo» en NLP', '146 artículos', 'Revisión crítica',
             'Motivaciones y técnicas de medición del sesgo', 'Cualitativo',
             'Motivaciones vagas y técnicas poco alineadas con ellas; propone tres recomendaciones', 'Revisión',
             'Sesgo social en lenguaje', 'Alta', 'Definir qué daño se mide y a quién afecta antes de medir sesgo',
             'MODERADA'),
    'S33': M(SI, 'Proponer «data statements» para NLP', 'Propuesta', 'Práctica de documentación',
             'Población, variedad lingüística, anotadores', 'Cualitativo', 'Documentar datos mejora generalización y '
             'reduce exclusión', 'Propuesta normativa', 'Variedades lingüísticas', 'Alta (español andino)',
             'Documentar variedad de habla y texto en el dataset card', 'MODERADA'),
    'S34': M(SI, 'Revisar la alucinación en generación de lenguaje', 'Literatura', 'Revisión', 'Tareas de generación',
             'Métricas de alucinación', 'La generación neuronal es propensa a alucinar; métodos de medición y mitigación',
             'Previa a los LLM más recientes', 'Información falsa', 'Muy alta para resúmenes y explicaciones con LLM',
             'Toda salida de LLM debe citar la evidencia de origen y validarse', 'FUERTE'),
    'S35': M(SI, 'Analizar riesgos de modelos de lenguaje muy grandes', 'Ensayo crítico', 'Análisis',
             'Datos, costo, sesgo', 'Cualitativo', 'Recomienda documentar datos y evaluar riesgos antes de desarrollar',
             'Posicionamiento', 'Sesgos del corpus web', 'Media', 'Evaluar riesgos antes de adoptar LLM', 'MODERADA'),
    'S36': M(PRE + '; publicado en NeurIPS 2023', 'Evaluar el uso de LLM como jueces', 'MT-Bench y Chatbot Arena',
             'LLM como evaluador', 'Preguntas abiertas', 'Acuerdo con preferencias humanas',
             'Acuerdo superior al 80 % con preferencias humanas; sesgos de posición, verbosidad y autopromoción',
             'Tareas de chat, no evaluación de personas', 'Sesgos del juez', 'Media',
             'No usar LLM como juez de candidatos; como mucho, ayuda para revisar consistencia de rúbricas', 'MODERADA'),
    'S37': M(SI, 'Preentrenamiento multimodal para comprender documentos ' + SR, 'Documentos escaneados y digitales',
             'Transformer de texto, disposición e imagen (LayoutLMv2)', 'Texto, posición, imagen', 'Exactitud en tareas',
             'Mejora tareas de comprensión de documentos visualmente ricos', 'Costo computacional',
             'No relevante', 'Baja: los CV del caso son digitales', 'OCR/disposición solo si hay escaneados', 'MODERADA'),
    'S38': M(PRE + '; publicado en ICML 2023', 'Reconocimiento de voz robusto con supervisión débil',
             '680 000 h de audio multilingüe', 'Transformer codificador-decodificador (Whisper)', 'Audio',
             'WER', 'Generaliza bien en cero disparos y se acerca a la robustez humana', 'Evaluación en benchmarks',
             'Rendimiento desigual por idioma y variedad', 'Alta: candidato STT local', 'Evaluar Whisper con audio '
             'propio y revisión humana', 'MODERADA'),
    # ------------------------------------------------------------------ I. Multicriterio
    'S39': M(SI, 'Presentar el proceso analítico jerárquico (AHP) ' + SR, 'Método', 'AHP',
             'Comparaciones por pares de criterios', 'Razón de consistencia', 'Método para derivar pesos de criterios',
             'Sensible a la elicitación', 'Pesos subjetivos', 'Alta: pesos por vacante', 'Derivar pesos con método '
             'explícito y registrado', 'MODERADA'),
    'S40': M(SI, 'Aplicar TOPSIS a la selección de personal ' + SR, 'Caso de aplicación', 'TOPSIS', 'Criterios '
             'ponderados', 'Ordenamiento', 'Enfoque multicriterio para ordenar candidatos', 'Caso único',
             'Pesos subjetivos', 'Media: el ranking actual ya es una suma ponderada (RF-21)', 'Mantener la suma '
             'ponderada transparente; MCDM complejo no aporta evidencia adicional', 'LIMITADA'),
    # ------------------------------------------------------------------ K. Equidad
    'S41': M(SI, 'Revisar sesgo y equidad en ML', 'Literatura', 'Revisión', 'Fuentes de sesgo, definiciones',
             'Varias', 'Taxonomía de sesgos y definiciones de equidad', 'Revisión', 'Varios', 'Alta',
             'Catálogo de sesgos para el análisis de riesgos', 'MODERADA'),
    'S42': M('Revisión editorial (revista jurídica)', 'Analizar el impacto dispar de la minería de datos',
             'Análisis jurídico', 'Análisis', 'Datos históricos', 'Cualitativo',
             'Los algoritmos heredan prejuicios de decisiones previas y patrones de exclusión', 'Derecho de EE. UU.',
             'Sesgo histórico', 'Alta', 'No usar decisiones históricas de contratación como verdad', 'MODERADA'),
    'S43': M(PRE + '; publicado en NeurIPS 2016', 'Definir igualdad de oportunidades en aprendizaje supervisado',
             'Teórico con caso', 'Post-procesamiento', 'Predictor, objetivo, atributo protegido', 'Tasas de error por grupo',
             'Define igualdad de oportunidades/probabilidades y cómo ajustarlas; límites de las medidas «oblivious»',
             'Requiere el atributo protegido y una etiqueta confiable', 'Etiqueta sesgada', 'Media',
             'Las métricas de equidad requieren etiquetas válidas que el caso no tiene', 'FUERTE'),
    'S44': M(SI, 'Formalizar compromisos entre condiciones de equidad', 'Teórico', 'Demostración',
             'Calibración y equilibrio de errores', 'Formal', 'Salvo casos especiales, no pueden cumplirse a la vez',
             'Teórico', 'No aplica', 'Alta', 'Elegir y justificar una métrica de equidad; no prometer todas', 'FUERTE'),
    'S45': M(SI, 'Estudiar criterios de equidad en instrumentos de riesgo', 'Teórico con datos de reincidencia',
             'Análisis formal y empírico', 'Tasas base por grupo', 'Error por grupo',
             'Los criterios no pueden satisfacerse a la vez si las tasas base difieren', 'Dominio penal', 'Tasas base',
             'Alta', 'Igual que S44', 'FUERTE'),
    'S46': M(SI, 'Comparar intervenciones para mejorar la equidad', 'Varios conjuntos de datos', 'Benchmark',
             'Algoritmos de equidad', 'Equidad y exactitud', 'Resultados sensibles al preprocesamiento y a la partición',
             'Datasets de referencia', 'Inestabilidad de métricas', 'Media', 'Reportar variabilidad, no un solo número',
             'MODERADA'),
    'S47': M(SI, 'Identificar fuentes de daño en el ciclo de vida del ML', 'Marco conceptual', 'Taxonomía',
             '7 fuentes de daño', 'Cualitativo', 'Sesgos histórico, de representación, de medición, etc.',
             'Conceptual', 'Todos', 'Muy alta', 'Usar las 7 fuentes como lista de riesgos de F34', 'MODERADA'),
    'S48': M(SI, 'Medir sesgo racial en un algoritmo de salud', 'Algoritmo comercial; millones de pacientes',
             'Auditoría', 'Costo de salud como proxy', 'Tasa de derivación',
             'Usar el costo como proxy de la necesidad creó sesgo racial; corregirlo eleva la ayuda a pacientes negros '
             'de 17,7 % a 46,5 %', 'Dominio de salud', 'Sesgo de proxy de la etiqueta', 'Alta por analogía',
             'Revisar qué representa la etiqueta (p. ej., «contratado» ≠ «idóneo»)', 'FUERTE'),
    'S49': M(SI, 'Presentar el toolkit AI Fairness 360', 'Software', 'Biblioteca', 'Métricas y mitigaciones',
             'Métricas de equidad', 'Toolkit Apache 2.0 con métricas, explicaciones y mitigaciones', 'Herramienta',
             'No aplica', 'Media', 'Candidato de herramienta (ver análisis de herramientas)', 'MODERADA'),
    'S50': M(SI, 'Identificar necesidades de practicantes para ML más justo', '35 entrevistas y 267 encuestados',
             'Entrevistas y encuesta', 'Retos de equipos de producto', 'Cualitativo',
             'Desajuste entre retos reales y soluciones de investigación', 'Empresas de tecnología', 'No aplica',
             'Media', 'Planificar recolección de datos de auditoría desde el diseño', 'MODERADA'),
    # ------------------------------------------------------------------ J. Explicabilidad
    'S51': M(SI, 'Argumentar contra explicar cajas negras en decisiones de alto impacto ' + SR, 'Ensayo',
             'Análisis', 'Modelos interpretables', 'Cualitativo',
             'Recomienda modelos interpretables en lugar de explicaciones post hoc en alto impacto', 'Posición',
             'No aplica', 'Muy alta: selección es alto impacto', 'Preferir modelos/reglas interpretables', 'MODERADA'),
    'S52': M(SI, 'Explicar predicciones de cualquier clasificador (LIME)', 'Experimentos con usuarios', 'LIME',
             'Explicaciones locales', 'Confianza del usuario', 'Explicaciones locales ayudan a evaluar la confianza',
             'Explicaciones aproximadas e inestables', 'No aplica', 'Baja', 'No usar LIME como explicación al '
             'usuario final', 'MODERADA'),
    'S53': M(PRE + '; publicado en NeurIPS 2017', 'Unificar métodos de atribución (SHAP)', 'Teórico y experimentos',
             'Valores de Shapley', 'Importancia por característica', 'Consistencia', 'Marco unificado de importancia '
             'aditiva', 'Asume independencia en algunas variantes; costo', 'No aplica', 'Media',
             'SHAP solo para depuración interna si hubiera modelo', 'MODERADA'),
    'S54': M('No (documento de trabajo en SSRN); publicado luego en Harvard Journal of Law & Technology', 'Proponer explicaciones contrafactuales ' + SR,
             'Análisis jurídico-técnico', 'Contrafactuales', 'Cambios mínimos', 'Cualitativo',
             'Explicar qué cambio mínimo alteraría el resultado sin abrir la caja negra', 'Puede sugerir cambios '
             'no accionables', 'Atributos protegidos', 'Media', 'Explicar por criterios y evidencia faltante', 'MODERADA'),
    'S55': M(SI, 'Aportar la perspectiva de ciencias sociales sobre explicaciones ' + SR, 'Revisión', 'Revisión',
             'Explicaciones contrastivas y sociales', 'Cualitativo',
             'Las personas prefieren explicaciones contrastivas, selectivas y sociales', 'Revisión', 'No aplica',
             'Alta', 'Explicar «por qué este nivel y no otro» con evidencia', 'MODERADA'),
    'S56': M(SI, 'Estudiar cómo se usa la explicabilidad en organizaciones', 'Entrevistas en organizaciones',
             'Estudio cualitativo', 'Usos de explicaciones', 'Cualitativo',
             'La mayoría de despliegues sirven a ingenieros para depurar, no a los afectados', 'Muestra limitada',
             'No aplica', 'Alta', 'Diseñar explicaciones para el evaluador humano y el postulante', 'MODERADA'),
    # ------------------------------------------------------------------ M. Humano en el circuito
    'S57': M(SI, 'Estudiar cómo las personas usan evaluaciones de riesgo', 'Experimento en línea',
             'Experimento controlado', 'Predicciones de riesgo', 'Exactitud y disparidad',
             'Las personas rindieron menos que el algoritmo, no evaluaron bien su exactitud y mostraron «interacciones '
             'dispares» por raza', 'Participantes en línea', 'Disparidad en la interacción', 'Muy alta',
             'Evaluar el sistema socio-técnico completo, no solo el modelo', 'MODERADA'),
    'S58': M(SI, 'Medir si las explicaciones producen desempeño complementario', 'Estudios con usuarios en 3 datasets',
             'Experimentos mixtos', 'Explicaciones de IA', 'Exactitud del equipo',
             'Las explicaciones no aumentaron el desempeño complementario; aumentaron la aceptación de la recomendación '
             'sea correcta o no', 'Tareas de laboratorio', 'Sobredependencia', 'Muy alta',
             'Una explicación no garantiza control humano; evitar recomendar un candidato', 'MODERADA'),
    'S59': M(SI, 'Explicar cuándo las explicaciones reducen la sobredependencia', 'Experimentos',
             'Marco costo-beneficio', 'Costo de verificar la explicación', 'Sobredependencia',
             'Hay escenarios en que las explicaciones sí reducen la sobredependencia, si verificarlas cuesta poco',
             'Tareas controladas', 'Sobredependencia', 'Alta', 'Explicaciones fáciles de verificar contra evidencia '
             'citada', 'MODERADA'),
    'S60': M(SI, 'Metaanalizar cuándo humano + IA supera a cada uno', '106 experimentos; 370 tamaños de efecto',
             'Metaanálisis preregistrado', 'Tipo de tarea y desempeño relativo', 'g de Hedges',
             'En promedio la combinación rindió peor que el mejor de los dos (g = −0,23); pérdidas en tareas de '
             'decisión', 'Posible sesgo de publicación', 'No aplica', 'Muy alta',
             'No asumir que la recomendación de IA mejora la decisión de selección', 'FUERTE'),
    'S61': M(SI, 'Medir sesgo de automatización y adherencia selectiva en el sector público', '3 experimentos '
             '(N = 605, 904, 1345)', 'Experimentos', 'Fuente del consejo y estereotipos', 'Adherencia',
             'No se encontró sesgo de automatización; sí adherencia selectiva a consejos alineados con estereotipos en '
             'el estudio 2', 'Países Bajos', 'Estereotipos', 'Alta', 'Vigilar adherencia selectiva, no solo '
             'sobredependencia', 'CONFLICTIVA'),
    'S62': M(SI, 'Proponer guías de interacción humano-IA', 'Evaluación con 49 profesionales y 20 productos',
             'Diseño validado', '18 guías', 'Cumplimiento', '18 guías validadas para interacción con IA',
             'Productos de consumo', 'No aplica', 'Alta para F40', 'Mostrar qué hace y qué no hace el sistema; '
             'permitir corregirlo', 'MODERADA'),
    'S63': M(SI, 'Integrar la evidencia sobre complacencia y sesgo de automatización', 'Revisión de estudios',
             'Revisión y modelo teórico', 'Carga de tareas, atención', 'Cualitativo',
             'El sesgo de automatización produce errores de omisión y comisión; afecta a novatos y expertos',
             'Automatización en general', 'No aplica', 'Alta', 'Diseñar para revisión activa, no aprobación pasiva',
             'MODERADA'),
    'S84': M(SI, 'Medir el efecto de recomendaciones sesgadas de IA en decisiones humanas de contratación',
             'N = 528; 1526 escenarios; 16 ocupaciones', 'Experimento de cribado con IA simulada',
             'Preferencias raciales de la IA, IAT, alfabetización en IA', 'Tasa de selección por grupo',
             'Sin IA o con IA sin sesgo, las personas seleccionaron por igual; con IA sesgada la siguieron hasta en el '
             '90 % de los casos, incluso juzgándola de baja calidad', 'IA simulada; EE. UU.',
             'Sesgo transmitido a la persona', 'Muy alta: cuestiona el «humano en el circuito» como salvaguarda',
             'No mostrar recomendación de candidato junto a la decisión (refuerza ADR-001)', 'FUERTE'),
    # ------------------------------------------------------------------ N. Calibración y métricas
    'S64': M(SI, 'Comparar la calidad probabilística de distintos algoritmos', 'Varios datasets', 'Experimentos',
             'Probabilidades predichas', 'Calibración', 'Algunos modelos distorsionan probabilidades; Platt e isotónica '
             'las corrigen', 'Datasets clásicos', 'No aplica', 'Media', 'Calibrar y verificar probabilidades si se '
             'reportan', 'FUERTE'),
    'S65': M(PRE + '; publicado en ICML 2017', 'Estudiar la calibración de redes modernas', 'Imagen y texto',
             'Experimentos', 'Profundidad, regularización', 'ECE', 'Las redes modernas están mal calibradas; el escalado '
             'de temperatura ayuda', 'Redes profundas', 'No aplica', 'Baja', 'No reportar «confianza» sin calibrarla',
             'MODERADA'),
    'S66': M(SI, 'Proponer la verificación de pronósticos probabilísticos (puntaje de Brier) ' + SR, 'Método',
             'Estadística', 'Pronósticos probabilísticos', 'Puntaje de Brier', 'Medida de exactitud probabilística',
             'Antiguo', 'No aplica', 'Media', 'Usar Brier si se reportan probabilidades', 'FUERTE'),
    'S67': M(SI, 'Revisar la calibración de clasificadores', 'Revisión', 'Tutorial y revisión',
             'Métodos de calibración', 'Varias', 'Introducción y panorama de principios y práctica', 'Revisión',
             'No aplica', 'Media', 'Guía para F39', 'MODERADA'),
    'S68': M(SI, 'Comparar curvas ROC y PR en datos desbalanceados', 'Simulación y estudios', 'Análisis',
             'Desbalance de clases', 'ROC, PR', 'Las curvas PR son más informativas que ROC con desbalance',
             'Bioinformática', 'No aplica', 'Media', 'Preferir PR-AUC con clases desbalanceadas', 'MODERADA'),
    'S69': M(SI, 'Proponer medidas de ganancia acumulada (DCG/NDCG)', 'Experimentos de recuperación', 'Métricas',
             'Relevancia graduada', 'DCG, NDCG', 'Medidas para evaluar rankings con relevancia graduada',
             'Recuperación de información', 'No aplica', 'Media', 'NDCG solo si existe un juicio de relevancia válido',
             'FUERTE'),
    'S70': M(SI, 'Introducir incertidumbre aleatoria y epistémica', 'Revisión', 'Tutorial', 'Tipos de incertidumbre',
             'Varias', 'Distingue incertidumbre aleatoria y epistémica y sus métodos', 'Revisión', 'No aplica', 'Alta',
             'Representar «evidencia insuficiente» como incertidumbre epistémica explícita', 'MODERADA'),
    # ------------------------------------------------------------------ O/P/L. Gobernanza y MLOps
    'S71': M(SI, 'Proponer model cards', 'Propuesta con ejemplos', 'Documentación', 'Uso previsto, métricas por '
             'grupo', 'Cualitativo', 'Documentación estándar de modelos con evaluación por subgrupo', 'Propuesta',
             'No aplica', 'Alta (ya usada en RF-29)', 'Exigir model card en F36', 'MODERADA'),
    'S72': M(SI, 'Proponer datasheets for datasets', 'Propuesta', 'Documentación', 'Motivación, composición, '
             'recolección', 'Cualitativo', 'Documentación estándar de conjuntos de datos', 'Propuesta', 'No aplica',
             'Alta', 'Exigir dataset card en F34', 'MODERADA'),
    'S73': M(SI, 'Proponer un marco de auditoría algorítmica interna', 'Marco', 'Proceso de auditoría',
             'Artefactos de auditoría', 'Cualitativo', 'Auditoría interna de extremo a extremo antes del despliegue',
             'Marco', 'No aplica', 'Alta', 'Auditoría interna documentada antes de F39', 'MODERADA'),
    'S74': M(SI, 'Formalizar la fuga de datos (leakage)', 'Casos y competencias', 'Análisis', 'Información del '
             'objetivo', 'Cualitativo', 'Taxonomía de fugas y cómo evitarlas', 'Casos', 'No aplica', 'Alta',
             'Particiones temporales y por proceso (ya aplicado en RF-29)', 'FUERTE'),
    'S75': M(SI, 'Revisar la adaptación a la deriva de concepto', 'Revisión', 'Revisión', 'Deriva', 'Varias',
             'Categoriza estrategias y evaluación', 'Aprendizaje en línea', 'No aplica', 'Media',
             'Monitorear deriva entre convocatorias', 'MODERADA'),
    'S76': M(SI, 'Proponer pruebas de preparación para producción de ML', 'Experiencia industrial', 'Rúbrica',
             '28 pruebas y monitoreo', 'Puntaje', '28 pruebas concretas para reducir deuda técnica', 'Experiencia de una '
             'empresa', 'No aplica', 'Alta', 'Usar la rúbrica como lista de F38–F39', 'MODERADA'),
    'S77': M(SI, 'Definir MLOps', 'Revisión, herramientas y entrevistas', 'Métodos mixtos', 'Prácticas y roles',
             'Cualitativo', 'Definición y arquitectura de MLOps', 'Revisión', 'No aplica', 'Media',
             'Versionado y registro mínimos, no una plataforma completa', 'MODERADA'),
    'S78': M(SI, 'Revisar retos de desplegar ML', 'Casos publicados', 'Revisión', 'Etapas de despliegue',
             'Cualitativo', 'Hay problemas en cada etapa del despliegue', 'Reportes publicados', 'No aplica', 'Media',
             'Planificar despliegue y monitoreo desde F33', 'MODERADA'),
    'S79': M(SI, 'Proponer rendición de cuentas para datasets', 'Marco', 'Ingeniería de software', 'Ciclo de vida del '
             'dataset', 'Cualitativo', 'Marco de transparencia para el desarrollo de datasets', 'Marco', 'No aplica',
             'Alta', 'Requisitos y revisiones del dataset como artefactos versionados', 'MODERADA'),
    'S80': M(SI, 'Revisar los riesgos de la analítica de personas', 'Revisión teórica', 'Revisión', 'Riesgos',
             'Cualitativo', 'Identifica peligros para organizaciones y empleados', 'Teórico', 'Vigilancia, '
             'discriminación', 'Alta', 'Minimizar datos y propósito limitado', 'MODERADA'),
    # ------------------------------------------------------------------ Complementos 2021–2025
    'S81': M(SI, 'Medir alucinaciones de Whisper', 'Audio de hablantes con afasia y control', 'Auditoría',
             'Duración no vocal', 'Tasa de alucinación', 'Cerca del 1 % de transcripciones contenía frases '
             'inventadas; el 38 % de ellas con daños explícitos; más frecuentes con pausas largas', 'Versión 2023',
             'Afecta más a ciertos hablantes', 'Muy alta: una transcripción puede inventar «evidencia»',
             'Toda transcripción se revisa contra el audio antes de usarse como evidencia', 'MODERADA'),
    'S82': M(SI, 'Evaluar algoritmos para calificar respuestas abiertas en selección ' + SR, 'Respuestas de '
             'evaluaciones de selección', 'Deep learning', 'Texto de respuestas', 'Acuerdo con calificadores humanos',
             'Ver la publicación (resumen no disponible)', 'Ver la publicación', 'Sesgo de los calificadores de '
             'entrenamiento', 'Media', 'Solo como antecedente; no adoptar calificación automática', 'INSUFICIENTE'),
    'S83': M(SI, 'Auditar sesgos de GPT-3.5 en contratación', '32 nombres, 10 ocupaciones, 3 tareas',
             'Auditoría por nombres', 'Raza y género', 'Puntuaciones', 'El modelo refleja sesgos estereotípicos al '
             'evaluar y al generar CV', 'Un modelo y versión', 'Estereotipos', 'Alta',
             'No pedir a un LLM que puntúe candidatos', 'MODERADA'),
    'S85': M(SI, 'Analizar sesgo y equidad en entrevistas en vídeo multimodales', '733 participantes; anotadores '
             'entrenados', 'Modelos interpretables multimodales', 'Rasgos verbales, paraverbales, visuales',
             'Exactitud, sesgo, equidad', 'Combinar modalidades apenas mejora la exactitud y aumenta el sesgo; lo verbal '
             'solo rinde casi igual', 'Contratación simulada', 'Rasgos visuales y paraverbales',
             'Muy alta', 'Usar solo el contenido verbal; excluir rasgos visuales y paraverbales', 'MODERADA'),
    'S86': M(SI, 'Revisar decisiones de diseño de selección (validez, diversidad, experiencia)', 'Revisión',
             'Revisión', 'Desarrollo, administración y puntuación (incluida IA)', 'Cualitativo',
             'Sintetiza efectos de decisiones de diseño sobre validez, diversidad y experiencia del postulante',
             'Revisión', 'Impacto adverso', 'Alta', 'Explicar el procedimiento al postulante antes de evaluar',
             'MODERADA'),
    'S87': M(SI, 'Auditar sesgo por discapacidad en cribado de CV con GPT-4', 'Pares de CV con y sin méritos '
             'relacionados con discapacidad', 'Auditoría', 'Méritos asociados a discapacidad', 'Ranking',
             'GPT-4 mostró prejuicio contra CV con méritos relacionados con discapacidad', 'Un modelo', 'Capacitismo',
             'Alta', 'No usar LLM para ordenar CV', 'MODERADA'),
    'S88': M(SI, 'Describir el pipeline de diarización de pyannote.audio 2.1 ' + SR, 'Benchmarks de diarización',
             'Segmentación y embeddings de hablante', 'Audio', 'DER', 'Pipeline y receta de diarización',
             'Benchmarks', 'Usa embeddings de voz (dato biométrico)', 'Media',
             'Preferir canales separados o segmentación manual antes que huellas de voz', 'MODERADA'),
    'S89': M(SI, 'Presentar seis casos de ML para puntuar respuestas en selección operativa', 'Seis sistemas '
             'operativos en organizaciones', 'ML sobre respuestas escritas y orales', 'Texto de respuestas',
             'Exactitud, fiabilidad, impacto adverso', 'El ML calificó respuestas tan exacta y fiablemente como jueces '
             'humanos, con poco o ningún impacto adverso', 'Grandes volúmenes de datos de organizaciones grandes',
             'Depende de los calificadores humanos de referencia', 'Media: el caso no tiene ese volumen de datos',
             'Posible a futuro solo con validación local; en tensión con S84', 'CONFLICTIVA'),
}

# Documentos oficiales y normas: campos reducidos (qué establece, obligación relevante, aplicabilidad, decisión).
OFICIALES = {
    'O01': ('Reglamento (UE) 2024/1689 (Ley de IA)', 'Prohíbe inferir emociones en el trabajo y la educación (art. '
            '5.1.f); clasifica como alto riesgo el reclutamiento y la evaluación de candidatos (Anexo III, 4.a); exige '
            'supervisión humana capaz de ignorar o revertir el resultado y consciente del sesgo de automatización '
            '(art. 14). Texto contrastado en el Diario Oficial (Oficina de Publicaciones de la UE)',
            'Referencia comparada (no aplica directamente en Perú)', 'Diseñar como sistema de alto riesgo aunque no '
            'se esté obligado'),
    'O02': ('Reglamento (UE) 2016/679 (RGPD)', 'Derecho a no ser objeto de decisiones exclusivamente automatizadas '
            '(art. 22)', 'Referencia comparada', 'Decisión final siempre humana (ya en RF-23)'),
    'O03': ('NIST AI RMF 1.0', 'Funciones gobernar, mapear, medir y gestionar riesgos de IA', 'Marco voluntario',
            'Estructurar el análisis de riesgos de F34–F39'),
    'O04': ('NIST SP 1270', 'Identificación y gestión de sesgos en IA (sesgos sistémicos, estadísticos y humanos)',
            'Marco voluntario', 'Catálogo de sesgos humanos y sistémicos'),
    'O05': ('ISO/IEC 42001:2023', 'Sistema de gestión de IA', 'Norma de pago; referencia', 'Referencia de gobernanza; '
            'sin certificación'),
    'O06': ('ISO/IEC 23894:2023', 'Gestión de riesgos de IA', 'Norma de pago; referencia', 'Referencia de gestión de '
            'riesgos'),
    'O07': ('Principios de IA de la OCDE', 'Principios de IA confiable', 'Referencia; el DS 115-2025-PCM los cita',
            'Alineación de principios'),
    'O08': ('Recomendación de la UNESCO sobre ética de la IA', 'Principios éticos y supervisión humana', 'Referencia',
            'Alineación de principios'),
    'O09': ('DS 016-2024-JUS (reglamento de la Ley 29733)', 'Protección de datos personales en Perú', 'Aplica al caso',
            'Base legal, consentimiento, minimización y seguridad de datos de postulantes'),
    'O10': ('Ley N.º 31814', 'Promueve el uso de IA en Perú', 'Aplica', 'Marco nacional'),
    'O11': ('29 CFR 1607 (Uniform Guidelines)', 'Regla de los cuatro quintos como indicio de impacto adverso',
            'Referencia de EE. UU.', 'Indicador de impacto adverso solo con datos válidos y suficientes'),
    'O12': ('NYC Local Law 144 (AEDT)', 'Auditorías de sesgo para herramientas automatizadas de empleo',
            'Referencia de EE. UU.', 'Antecedente de auditoría independiente'),
    'O13': ('DS 115-2025-PCM (reglamento de la Ley 31814)', 'Riesgo alto: determinar selección, evaluación, '
            'contratación y cese de postulantes (art. 24.1 e, corroborado). Además, según la lectura de F30 pendiente '
            'de contraste con la publicación oficial: evaluación de NNA en educación (24.1 b); inferir emociones en el '
            'trabajo o centros educativos (24.1, final del inciso i); transparencia y explicación (art. 25); '
            'evaluación de impacto previa (art. 30); registro (art. 31)', 'Aplica al caso (vigente)',
            'Tratar la visión F33–F40 como riesgo alto. Los arts. 24, 30 y 31 se contrastan artículo por artículo con '
            'la publicación normativa oficial antes de producir efectos jurídicos'),
    'O14': ('Marco de Buen Desempeño Docente (MINEDU, RM 0547-2012-ED)', 'Dominios, competencias y desempeños del '
            'buen docente en Perú', 'Aplica al caso docente', 'Fuente candidata de competencias para vacantes docentes, '
            'a validar con el colegio'),
    'O15': ('Ley N.º 29733, Ley de Protección de Datos Personales (2011)', 'Derecho fundamental a la protección de '
            'datos personales: principios de consentimiento, finalidad, proporcionalidad y seguridad; datos sensibles',
            'Aplica al caso (norma primaria; O09 es su reglamento)', 'Base legal, consentimiento, minimización y '
            'seguridad de los datos de postulantes'),
    'O16': ('Reglamento (UE) 2026/1744 (Digital Omnibus on AI)', 'Modifica el Reglamento (UE) 2024/1689: los requisitos '
            'de alto riesgo (cap. III, secciones 1 a 3) se aplican desde el 2/12/2027 a los sistemas del Anexo III y '
            'desde el 2/8/2028 a los del Anexo I; entra en vigor al tercer día de su publicación (DO de 24/7/2026); no '
            'modifica la prohibición del art. 5.1.f', 'Referencia comparada (fuente oficial del calendario)',
            'El calendario de la UE se cita desde esta fuente oficial y no desde X02'),
}
