# F30 — Estado del arte de la IA en reclutamiento y selección

> Fase F30, versión 1 (30/09/2026), **pendiente de auditoría**. Investigación documental: no implementa nada. Cada afirmación cita su fuente con el identificador de la [matriz de evidencia](F30_Matriz_Evidencia_Cientifica.md) ([S01]–[S89] trabajos científicos, [O01]–[O14] normas y documentos oficiales, [X01]–[X02] fuentes secundarias). Las referencias completas están en [REFERENCIAS.md](REFERENCIAS.md).

**Convención de este documento.** Se distinguen cuatro tipos de afirmación:

- **Evidencia:** lo que reporta una fuente, con su cita.
- **Recomendación de autores:** una guía o propuesta de la fuente, también citada.
- **Inferencia:** lo que el equipo deduce para el caso del Colegio Andino, marcado como tal.
- **Decisión:** las decisiones de ingeniería, que están en [F30_Recomendaciones_F33_F40.md](F30_Recomendaciones_F33_F40.md).

## 1. Resumen ejecutivo

1. **Lo que funciona en selección no es la IA, es la estructura.** La entrevista estructurada es el procedimiento con mayor validez en la revisión metaanalítica más reciente [S13] y supera a la no estructurada [S14]. Sus componentes conocidos (mismas preguntas, escalas ancladas, calificación por pregunta) [S15, S16] y las escalas ancladas en conducta [S19] son la base más sólida para un «motor» de evaluación.
2. **En docentes la predicción es débil.** Un metaanálisis de selección de docentes encontró una relación pequeña, aunque significativa, entre los métodos de selección y la eficacia docente posterior (r = 0,12) [S22]. *Inferencia:* ningún sistema puede prometer predecir al «mejor docente»; puede ordenar y documentar mejor la evidencia.
3. **La IA aplicada a personas hereda y amplifica sesgos.**
   - Los embeddings usados para cribar CV prefirieron nombres asociados a personas blancas en el 85,1 % de los casos [S11].
   - Los LLM reprodujeron estereotipos de raza y género [S83] y de discapacidad [S87].
   - El reconocimiento de voz comete casi el doble de errores con hablantes negros que con blancos (WER 0,35 frente a 0,19) [S10] y a veces inventa frases [S81].
4. **El «humano en el circuito» no basta por sí solo.**
   - En un experimento de contratación con 528 personas, los participantes siguieron recomendaciones sesgadas de una IA hasta en el 90 % de los casos, incluso cuando la consideraban de baja calidad [S84].
   - En promedio, las combinaciones humano + IA rinden peor que el mejor de los dos por separado, sobre todo en tareas de decisión [S60].
   - Las explicaciones aumentaron la aceptación de la recomendación fuera correcta o no [S58].
5. **La evidencia disponible para inferir emociones o personalidad desde rostro o vídeo es insuficiente, mixta y no suficientemente fiable ni generalizable para un uso de alto impacto como la selección** [S07, S08, S09]. En entrevistas en vídeo, añadir rasgos visuales y paraverbales apenas mejora la exactitud y aumenta el sesgo [S85]. La Ley de IA de la UE prohíbe inferir emociones en el trabajo y en la educación (art. 5) [O01]. El reglamento peruano lo clasifica como uso de riesgo alto [O13].
6. **El marco legal peruano ya clasifica este caso.** El DS 115-2025-PCM [O13] considera de riesgo alto los sistemas de IA usados para determinar la selección, evaluación, contratación o cese de postulantes (art. 24.1 e), corroborado). Según la lectura de F30, también les exige transparencia, explicación, supervisión humana, evaluación de impacto previa al desarrollo y registro; esos artículos (24, 30 y 31, entre otros) se contrastan con la publicación oficial antes de producir efectos jurídicos. Los datos de postulantes están protegidos por la Ley 29733 [O15] y su reglamento [O09].
7. **Hay evidencia en tensión.**
   - Seis sistemas operativos de ML calificaron respuestas abiertas de selección con exactitud y fiabilidad comparables a las de jueces humanos y con poco o ningún impacto adverso [S89].
   - Esos sistemas operan en organizaciones con grandes volúmenes de datos de calificación humana; el caso del colegio no tiene ese volumen [S04].
   - La evidencia sobre cómo las personas usan esas sugerencias es preocupante [S84, S60].
   - Esta tensión se registra como CONFLICTIVA y no se resuelve a favor de la automatización.

**Conclusión del estado del arte (inferencia del equipo):** la contribución defendible de la IA en este proyecto es **estructurar, documentar y verificar la evidencia** que usan los evaluadores humanos. Ejemplos: rúbricas, procedencia de cada nivel asignado, completitud y acuerdo entre evaluadores. La evidencia reunida **no respalda predecir, puntuar ni recomendar candidatos para este caso, con los datos, el gobierno y las garantías actuales**; las implementaciones a escala [S89] se registran como evidencia en tensión. Esta conclusión coincide con ADR-001 y con el contrato 4 del proyecto.

## 2. Estrategia y alcance de la revisión

- **Búsqueda y verificación:** veinte consultas en OpenAlex, una por tema A–T, con 500 registros cribados. Se añadieron búsqueda complementaria 2021–2025, bola de nieve y normas oficiales. Todo DOI se verificó en Crossref o DataCite, incluidos sus avisos de retractación. El detalle y el flujo de selección están en la [sección 1 de la matriz](F30_Matriz_Evidencia_Cientifica.md#1-estrategia-de-búsqueda).
- **Resultado:** 89 trabajos científicos, 16 normas o documentos oficiales y 2 fuentes secundarias de contraste, verificados los 107. Se excluyó un artículo retractado que apareció en el cribado.
- **Límite principal:** la extracción se hizo sobre los resúmenes publicados, no sobre el texto completo. Si un trabajo no tiene resumen disponible, la matriz lo indica y no le atribuye cifras.

## 3. Estado del arte por tema

### A. IA en reclutamiento: prácticas, ética y discriminación

- **Evidencia:**
  - Los proveedores de evaluaciones algorítmicas de preempleo eligen objetivos y datos de entrenamiento que pueden incorporar sesgo. Sus técnicas de des-sesgo interactúan de forma compleja con la ley antidiscriminación [S01].
  - Dos revisiones sistemáticas, de 36 y 51 artículos, concluyen que la evidencia empírica es escasa y que los riesgos dominantes son discriminación, opacidad y privacidad [S02, S03].
  - Los datos de RR. HH. son pequeños, las etiquetas débiles y la rendición de cuentas difícil [S04]. La analítica de personas tiene riesgos propios para organizaciones y empleados [S80].
  - La discriminación algorítmica en reclutamiento nace de datos limitados y del diseño; se recomienda combinar medidas técnicas con gobernanza interna y supervisión externa [S05].
- **Evidencia (reacciones de postulantes):** las entrevistas altamente automatizadas reducen la aceptación de los postulantes por menor presencia social y equidad percibida [S06]. Las decisiones de diseño de un procedimiento de selección afectan a la vez su validez, la diversidad y la experiencia del postulante [S86]. La base de evidencia de los procedimientos digitales (pruebas en línea, entrevistas digitales, gamificación, redes sociales) es todavía desigual [S23].
- **Inferencia:** un colegio con pocas convocatorias al año está en el peor escenario para el ML supervisado sobre personas (pocos datos, etiquetas históricas sesgadas, alto impacto).

### B. Ajuste persona-puesto (*person-job fit*)

- **Evidencia:** los modelos neuronales de ajuste persona-puesto aprenden de grandes históricos de postulaciones y decisiones [S25, S26].
- **Inferencia:** en el caso no hay ese histórico. Además, la etiqueta («fue contratado») refleja decisiones pasadas y no idoneidad, con el riesgo de sesgo por etiqueta *proxy* documentado en otros dominios [S42, S48]. Nivel de aplicabilidad: LIMITADA.

### C. Evaluación por competencias y análisis del puesto

- **Recomendación de autores:**
  - Hay 20 buenas prácticas para modelar competencias, que se derivan del análisis del puesto y se organizan para su uso en selección [S17].
  - El análisis del trabajo ha evolucionado hacia modelos que incluyen actividades, atributos y contexto [S18].
  - Las escalas ancladas en conducta (BARS) describen cada nivel con conductas observables [S19].
- **Evidencia:** la validez de la entrevista estructurada se explica en parte porque mide constructos más relacionados con el desempeño [S24].
- **Contexto peruano:** el Marco de Buen Desempeño Docente del MINEDU [O14] organiza dominios, competencias y desempeños del docente. *Inferencia:* es una fuente candidata de competencias para vacantes docentes, que el colegio debe validar.

### D. Entrevistas estructuradas

- **Evidencia:**
  - La entrevista estructurada supera a la no estructurada, y las preguntas situacionales y de conducta superan a las de tipo psicológico [S14].
  - Tras corregir la sobrecorrección por restricción de rango, las validez se reducen entre 0,10 y 0,20, pero la entrevista estructurada queda primera [S13]. Esto matiza las estimaciones clásicas [S12], que por eso se marcan como CONFLICTIVA.
  - La estructura tiene 15 componentes identificados [S15]; la revisión de 20 años confirma sus beneficios y deja preguntas abiertas [S16].
- **Recomendación de autores:** medir la fiabilidad entre evaluadores con el coeficiente de correlación intraclase (ICC), eligiendo la forma adecuada y reportándola con su intervalo [S20, S21].

### E. Procesamiento de CV con NLP

- **Evidencia:**
  - Los modelos de lenguaje y sus embeddings codifican sesgos sociales [S11, S32].
  - Los LLM alucinan contenido [S34] y su escala tiene riesgos documentados [S35].
  - Usados como evaluadores de CV, GPT-3.5 y GPT-4 mostraron sesgos de raza, género y discapacidad [S83, S87].
- **Recomendación de autores:** documentar la variedad lingüística y la población de los datos (*data statements*) [S33]. Definir qué daño se mide antes de medir el «sesgo» [S32].

### F. Similitud semántica

- **Evidencia:** SBERT produce embeddings de oraciones comparables por coseno con un costo bajo [S31]. Ese tipo de similitud, usada para recuperar CV, mostró sesgos fuertes por nombre [S11].
- **Inferencia:** la similitud semántica puede servir para **encontrar** fragmentos de evidencia relacionados con un criterio, nunca para **puntuar** candidatos.

### G. Extracción de información y habilidades

- **Evidencia:** existen conjuntos anotados y modelos para extraer habilidades de avisos de empleo [S29]. Una revisión de 108 artículos clasifica los métodos y sus retos [S30].
- **Límite:** son avisos de empleo en inglés, no CV en español.
- **Inferencia:** la extracción en español necesitaría datos propios y revisión humana.

### H. Ranking y recomendación

- **Evidencia:** las revisiones de recomendadores de empleo identifican retos de datos, bidireccionalidad, equidad y explicabilidad [S27, S28].
- **Contexto del proyecto:** el ranking ya existe (RF-21). Es una suma ponderada normalizada de los puntajes que registran evaluadores humanos ([A-24](../../assumptions.md)), sin desempate automático (A-26).

### I. Decisión multicriterio (MCDM)

- **Evidencia:** AHP deriva pesos de comparaciones por pares con una razón de consistencia [S39]. TOPSIS se ha aplicado a la selección de personal [S40].
- **Inferencia:** el ranking actual ya es un método multicriterio transparente (suma ponderada). AHP puede servir para **justificar los pesos** de una vacante. Reemplazar la suma por TOPSIS u otro método no aporta evidencia de mejor selección y sí añade opacidad.

### J. Explicabilidad (XAI)

- **Recomendación de autores:** en decisiones de alto impacto, usar modelos interpretables en lugar de explicar cajas negras [S51].
- **Evidencia:**
  - LIME y SHAP explican predicciones localmente [S52, S53], pero en las organizaciones se usan sobre todo para que los ingenieros depuren modelos [S56].
  - Las personas prefieren explicaciones contrastivas y selectivas [S55]. Los contrafactuales explican sin abrir el modelo [S54].
  - Las explicaciones pueden aumentar la confianza ciega [S58] o reducirla cuando verificarlas cuesta poco [S59].

Detalle en [F30_Explainability_Fairness_Gobernanza.md](F30_Explainability_Fairness_Gobernanza.md).

### K. Equidad algorítmica

- **Evidencia:**
  - Las definiciones de equidad (calibración por grupo, equilibrio de errores) no pueden cumplirse a la vez si las tasas base difieren [S44, S45].
  - La igualdad de oportunidades exige una etiqueta válida [S43].
  - El sesgo puede entrar por la etiqueta (*proxy*) [S48], por los datos históricos [S42] o en cualquiera de siete puntos del ciclo de vida [S47].
  - Los resultados de las intervenciones de equidad son sensibles al preprocesamiento y a la partición [S46].
  - Hay catálogos y herramientas de métricas [S41, S49]. Los equipos reales tienen necesidades que la investigación no cubre [S50].
- **Normas:** la regla de los cuatro quintos es un indicio de impacto adverso en EE. UU. [O11]. La Ley Local 144 de Nueva York exige auditorías de sesgo para herramientas automatizadas de empleo [O12].

### L. IA responsable y gobernanza

- **Normas y marcos:**
  - NIST AI RMF y NIST SP 1270 estructuran la gestión de riesgos y sesgos [O03, O04].
  - ISO/IEC 42001 y 23894 son normas de gestión [O05, O06].
  - La OCDE y la UNESCO fijan principios [O07, O08].
- **Normas aplicables:** la Ley 31814 y el DS 115-2025-PCM regulan la IA en Perú [O10, O13]. La Ley de IA de la UE clasifica el reclutamiento como alto riesgo y exige supervisión humana efectiva [O01, X01]. El Reglamento (UE) 2026/1744 (Digital Omnibus on AI), publicado en el Diario Oficial el 24/7/2026, aplaza al 2/12/2027 la aplicación de los requisitos de alto riesgo a los sistemas del Anexo III, y no modifica la prohibición de inferir emociones del art. 5.1.f [O16]. El análisis secundario [X02] coincide y queda solo como contexto.

### M. Humano en el circuito y sesgo de automatización

- **Evidencia a favor de la cautela:**
  - Seguimiento de IA sesgada hasta en el 90 % de los casos [S84].
  - Pérdidas de desempeño al combinar humano e IA en tareas de decisión [S60].
  - Interacciones dispares por raza [S57].
  - La complacencia y el sesgo de automatización afectan a novatos y expertos [S63].
- **Evidencia que matiza:** en tres experimentos del sector público no se encontró sesgo de automatización general, pero sí adherencia selectiva a consejos alineados con estereotipos [S61]. Se marca CONFLICTIVA sobre el sesgo general y consistente sobre la adherencia selectiva.
- **Recomendación de autores:** 18 guías de interacción humano-IA [S62], entre ellas dejar claro qué hace el sistema y permitir corregirlo.

### N. Incertidumbre y calibración

- **Evidencia:**
  - Muchos clasificadores entregan probabilidades mal calibradas que pueden corregirse [S64, S65, S67].
  - El puntaje de Brier mide la exactitud probabilística [S66].
  - Con clases desbalanceadas, la curva PR informa más que la ROC [S68].
- **Recomendación de autores:** distinguir la incertidumbre aleatoria de la epistémica [S70].
- **Inferencia:** «evidencia insuficiente» debe representarse de forma explícita y no ocultarse tras un número.

### O. Monitoreo y deriva

- **Evidencia:** la deriva de concepto requiere estrategias de detección y adaptación [S75]. Desplegar ML tiene problemas en cada etapa [S78]. MLOps define prácticas y roles [S77].
- **Recomendación de autores:** 28 pruebas de preparación para producción [S76].

### P. Auditabilidad

- **Recomendación de autores:** documentar modelos con *model cards*, que incluyen evaluación por subgrupo [S71]. Documentar conjuntos de datos con *datasheets* [S72] y con un ciclo de vida auditable [S79]. Hacer una auditoría interna de extremo a extremo antes del despliegue [S73].
- **Evidencia:** la fuga de información del objetivo (*leakage*) invalida evaluaciones y tiene una taxonomía conocida [S74].
- **Contexto del proyecto:** ya tiene auditoría de solo inserción (`AuditLogger` y el trigger `audit_logs_append_only`).

### Q. Analítica de reclutamiento

- **Evidencia:** la analítica de personas tiene riesgos de vigilancia y discriminación [S80] y depende de datos pequeños y difíciles [S04].
- **Exclusión:** el único trabajo del cribado sobre pérdida de decisión humana y pereza en educación está retractado y se excluyó (ver la [matriz, sección 5](F30_Matriz_Evidencia_Cientifica.md#5-avisos-editoriales-y-exclusiones)).

### R. Comprensión de documentos

- **Evidencia:** los modelos multimodales de texto, disposición e imagen mejoran la comprensión de documentos visualmente ricos [S37].
- **Inferencia:** los CV del caso son digitales (PDF o DOCX), así que basta extraer texto. El OCR y los modelos de disposición solo harían falta con documentos escaneados.

### S. Voz a texto

- **Evidencia:**
  - Whisper se entrenó con 680 000 horas de audio multilingüe y generaliza sin ajuste fino [S38].
  - Alrededor del 1 % de sus transcripciones contenía frases inventadas, el 38 % de ellas con contenido dañino, más frecuentes con pausas largas [S81].
  - Los sistemas de reconocimiento de voz tienen errores desiguales por grupo de hablantes [S10].
  - La diarización usa embeddings de voz [S88].
- **Inferencia:** una transcripción no es evidencia hasta que una persona la revisa contra el audio. En el contexto andino deben medirse los errores por variedad de habla antes de usarla.

### T. Evaluación de transcripciones y entrevistas

- **Evidencia:**
  - Las evaluaciones de personalidad desde vídeo entrenadas con autoinformes tienen poca fiabilidad y validez [S07].
  - La evidencia no respalda inferir la emoción a partir de la cara de forma fiable: su expresión varía entre culturas, situaciones y personas [S08, S09].
  - En entrevistas multimodales, el contenido verbal solo rinde casi igual que la combinación y con menos sesgo [S85].
  - Un LLM usado como juez coincide más del 80 % con preferencias humanas en tareas de chat, pero tiene sesgos de posición, verbosidad y autopromoción [S36].
  - La calificación automática de respuestas abiertas puede igualar a jueces humanos con grandes volúmenes de datos [S89]. De otro trabajo del área no hay resumen disponible [S82].
- **Inferencia:** si alguna vez se analizan transcripciones, debe ser **solo el contenido verbal** y para **localizar evidencia**, no para calificar.

## 4. Perspectiva de recursos humanos

| Práctica | Qué dice la evidencia | Implicación para el motor |
|---|---|---|
| Análisis del puesto | Base de criterios válidos; se ha ampliado a análisis del trabajo [S18] | Cada criterio de la vacante se justifica con el análisis del puesto |
| Modelos de competencias | 20 buenas prácticas [S17]; el MBDD como marco docente peruano [O14] | Catálogo de competencias versionado (`criteria_version`) |
| Entrevista estructurada | Mayor validez [S13, S14]; 15 componentes [S15, S16] | Mismas preguntas por vacante, con calificación por pregunta |
| BARS | Anclas conductuales sin ambigüedad [S19] | Rúbrica versionada (`rubric_version`) con descriptor por nivel |
| Fiabilidad entre evaluadores | ICC con forma e intervalo [S20, S21] | Métrica de calidad del proceso, no de la persona |
| Impacto adverso | Cuatro quintos como indicio [O11]; auditorías [O12]; límites formales [S44, S45] | Revisión agregada y legalmente sustentada (ver gobernanza) |
| Reacciones del postulante | Rechazo a la automatización alta [S06]; diseño equilibrado [S86] | Entrevista humana; explicar el procedimiento antes de evaluar |

## 5. Prácticas recomendadas

Las respalda la evidencia; cada una se traduce en decisión en el documento de recomendaciones.

1. Criterios derivados del análisis del puesto y competencias explícitas [S17, S18, O14].
2. Entrevista estructurada con preguntas situacionales y de conducta, y rúbricas BARS [S13, S14, S15, S19].
3. Calificación humana independiente y medición del acuerdo entre evaluadores con ICC [S20, S21].
4. Procedencia de cada nivel asignado: pregunta, respuesta, evidencia, criterio, nivel, justificación y confianza [S71, S73].
5. Reglas y modelos interpretables antes que cajas negras [S51].
6. Explicaciones contrastivas, verificables y para el usuario humano [S55, S56, S59].
7. Diseño contra el sesgo de automatización: el evaluador califica antes de ver cualquier salida del sistema [S60, S63, S84].
8. Documentación de datos y modelos: *datasheets*, *model cards* y *data statements* [S33, S71, S72, S79].
9. Particiones sin fuga de información y pruebas de preparación [S74, S76].
10. Evaluación de impacto antes de desarrollar, transparencia y registro [O13].

## 6. Prácticas a evitar

1. **Recomendar, puntuar o preseleccionar candidatos con IA.** Ver la tensión con [S89] en la sección 1. Fuentes: [S01, S11, S58, S60, S83, S84, S87]; ADR-001.
2. **Inferir emociones, personalidad o «ajuste cultural»** desde rostro, voz o vídeo [S07, S08, S09, S85, O01, O13].
3. **Usar decisiones históricas de contratación como etiqueta de «idoneidad»** [S01, S42, S48].
4. **Usar similitud de embeddings como puntaje** [S11].
5. **Usar un LLM como juez o resumidor de candidatos** [S34, S36, S83, S87].
6. **Usar una transcripción automática sin revisión humana** [S10, S81].
7. **Calificar fluidez, acento o prosodia**. *Inferencia* desde [S10, S85]: penaliza variedades de habla sin relación con el desempeño.
8. **Dar SHAP o LIME al usuario final como «explicación»** [S52, S56, S58].
9. **Prometer equidad con una sola métrica o con muestras pequeñas** [S44, S45, S46].
10. **Entrevistas totalmente automatizadas** [S06].
11. **Revisar redes sociales del postulante**: evidencia desigual y riesgo de usar información ajena al puesto [S23].
