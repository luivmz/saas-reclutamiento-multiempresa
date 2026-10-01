# F30 — Explicabilidad, equidad y gobernanza

> Fase F30, versión 1 (30/09/2026), **pendiente de auditoría**. Las citas remiten a la [matriz de evidencia](F30_Matriz_Evidencia_Cientifica.md). Las referencias a normas son un análisis técnico para orientar el diseño y **no constituyen asesoría legal**: la evaluación de impacto la valida una persona con competencia jurídica.

## 1. Explicabilidad (XAI)

### 1.1 Qué dice la evidencia

| Hallazgo | Fuente | Implicación |
|---|---|---|
| En alto impacto conviene un modelo interpretable antes que explicar una caja negra | [S51] | Reglas y suma ponderada antes que modelos opacos |
| LIME y SHAP dan atribuciones locales, aproximadas y a veces inestables | [S52, S53] | Útiles para depurar, no para justificar una decisión sobre una persona |
| En las organizaciones, la explicabilidad la usan sobre todo los ingenieros | [S56] | Hay que diseñar la explicación para el evaluador, el aprobador y el postulante |
| Las personas prefieren explicaciones contrastivas («por qué este nivel y no el siguiente») | [S55] | La justificación del nivel BARS es contrastiva |
| Los contrafactuales explican sin revelar el modelo | [S54] | «Qué evidencia faltaría para el nivel siguiente» |
| Las explicaciones aumentaron la aceptación de la recomendación, correcta o no | [S58] | Una explicación no es un control: puede empeorar la dependencia |
| Las explicaciones reducen la sobredependencia cuando verificarlas cuesta poco | [S59] | Cada explicación cita la evidencia y se verifica con un clic |

### 1.2 Diseño de explicaciones recomendado

| Destinatario | Qué necesita | Forma |
|---|---|---|
| Evaluador | Por qué asigna un nivel y qué evidencia lo respalda | Su propia justificación, con enlace a la evidencia (cadena de procedencia) |
| Aprobador / Dirección | Por qué el ranking queda así y dónde hay dudas | Desglose por criterio de la suma ponderada (A-24), acuerdo entre evaluadores y criterios con evidencia insuficiente |
| Postulante | Qué se evaluó y con qué criterios | Criterios y procedimiento antes de evaluar [S86]; si lo pide, explicación comprensible de los criterios [O13 art. 25.3] |
| Auditor | Qué versión de criterios, rúbrica y modelo se usó | `criteria_version`, `rubric_version`, `model_version` e `input_snapshot_hash` |

Los valores SHAP, la «importancia de características» y las probabilidades sin calibrar **no se muestran** a evaluadores ni postulantes [S56, S58, S65].

## 2. Equidad (*fairness*)

### 2.1 Métricas posibles y sus límites

| Métrica | Qué mide | Límite principal | Fuente |
|---|---|---|---|
| Razón de tasas de selección (regla de los cuatro quintos) | Si un grupo es seleccionado con menos del 80 % de la tasa del más favorecido | Es un indicio, no una prueba. Con pocos postulantes por vacante la razón es inestable y no concluye nada | [O11] |
| Paridad demográfica | Igual tasa de resultado positivo por grupo | Ignora diferencias legítimas; choca con otras definiciones | [S41, S44] |
| Igualdad de oportunidades / de probabilidades | Iguales tasas de acierto entre quienes «merecen» el resultado | Requiere una etiqueta válida de idoneidad, que no existe | [S43] |
| Calibración por grupo | Una misma puntuación significa lo mismo en cada grupo | Incompatible con el equilibrio de errores si las tasas base difieren | [S44, S45] |
| Acuerdo entre evaluadores por grupo | Si el ICC es menor con ciertos postulantes | Requiere el atributo de grupo y muestras suficientes | [S20, S21] |
| WER por grupo de hablantes | Si la transcripción es peor para ciertos hablantes | Requiere un piloto con audio consentido o ficticio | [S10] |

**Límites generales:**

- no pueden cumplirse todas las definiciones a la vez [S44, S45];
- los resultados varían con el preprocesamiento y la partición [S46];
- la etiqueta puede ser un *proxy* sesgado [S48];
- el sesgo entra en cualquier etapa del ciclo de vida [S47];
- medir equidad por grupo **exige datos sensibles**, que tienen su propio riesgo legal (sección 4.3).

### 2.2 Recomendación: equidad del procedimiento antes que equidad estadística

*Inferencia del equipo:* en el caso hay pocos postulantes por vacante y no hay base legal para recoger atributos sensibles. Por eso la equidad se controla primero en el **procedimiento**, donde la evidencia es más sólida:

1. **Mismas preguntas y misma rúbrica** para todos los postulantes de una vacante [S14, S15].
2. **Anclas conductuales** que reducen la ambigüedad de la calificación [S19].
3. **CV minimizado para el evaluador:** sin foto, edad, estado civil ni dirección. El nombre se oculta en la etapa de revisión documental cuando sea viable. *Inferencia* desde [S11]: hay sesgo por nombre en sistemas, y el sesgo humano es plausible.
4. **Calificación independiente** de dos evaluadores en los criterios de mayor peso, con ICC y revisión de discrepancias [S20, S21].
5. **Criterios excluidos:** acento, fluidez, apariencia, «ajuste cultural» y personalidad [S07, S10, S85].
6. **Revisión agregada de impacto adverso** solo cuando existan base legal, datos y muestra suficiente, a lo largo de varias convocatorias y nunca por vacante individual [O11, S46].

## 3. Supervisión humana y sesgo de automatización

### 3.1 Evidencia

- Las personas siguieron recomendaciones raciales sesgadas de una IA hasta en el 90 % de los casos, incluso cuando la juzgaban de baja calidad. Sin IA, o con IA sin sesgo, seleccionaron por igual a ambos grupos [S84].
- Las combinaciones humano + IA rindieron en promedio peor que el mejor de los dos (g = −0,23), con pérdidas en tareas de decisión [S60].
- Al usar evaluaciones de riesgo algorítmicas, las personas mostraron interacciones dispares por raza [S57].
- La complacencia y el sesgo de automatización producen errores de omisión y de comisión, en novatos y en expertos [S63].
- **En tensión:** en tres experimentos no se encontró sesgo de automatización general, pero sí adherencia selectiva a consejos alineados con estereotipos [S61].
- ADR-002 ya rechazó la preselección automática con confirmación posterior por el sesgo de anclaje.

### 3.2 Medidas de diseño

| Medida | Contra qué protege | Fuente |
|---|---|---|
| El sistema **no recomienda candidatos** ni sugiere niveles | Anclaje y seguimiento de IA sesgada | [S84, S58]; ADR-001 |
| El evaluador califica **antes** de ver cualquier ayuda del sistema | Anclaje | [S84, S63] |
| Las «recomendaciones» del sistema se refieren al **proceso** (falta evidencia, discrepancia, pregunta omitida) | Confundir ayuda con decisión | [S62]; ADR-001 |
| Justificación obligatoria en cada nivel y en la decisión final | Aprobación pasiva | [S55]; RF-23 |
| Registrar si se aceptó o descartó cada fragmento sugerido | Detectar aceptación acrítica | [S58] |
| Capacitación del evaluador sobre los límites del sistema | Exceso de confianza | [O13 art. 28.11] |
| Capacidad de detener, corregir o invalidar cualquier salida | Supervisión efectiva | [O13 art. 28.11, O01 art. 14] |

**Regla central:** RECOMENDACIÓN DEL SISTEMA ≠ DECISIÓN FINAL DE CONTRATACIÓN. La decisión final es humana, con confirmación explícita y justificación (RF-23, ADR-002). Ninguna salida del motor se registra como causa de la decisión.

## 4. Gobernanza

### 4.1 Marco regulatorio aplicable al caso

| Norma | Qué exige o prohíbe (relevante) | Consecuencia para F33–F40 |
|---|---|---|
| DS 115-2025-PCM, art. 24.1 e) [O13] (corroborado) | Riesgo alto: sistemas de IA que **determinan** procesos de selección, evaluación, contratación y cese de trabajadores o postulantes | El motor, aunque solo asista, entra en esta zona; se trata como riesgo alto por prudencia |
| DS 115-2025-PCM, art. 24.1 b) [O13] | Riesgo alto: evaluar a niños, niñas y adolescentes en educación, salvo función complementaria | No aplica a docentes; prohíbe extender el motor a estudiantes sin nueva evaluación |
| DS 115-2025-PCM, art. 24.1, final del inciso i) [O13] | Riesgo alto: inferir emociones de una persona en entornos de trabajo y centros educativos | Excluido del diseño (además, la evidencia sobre su fiabilidad es insuficiente y mixta [S08]) |
| DS 115-2025-PCM, art. 23 [O13] | Uso indebido (prohibido): inferir origen racial o étnico, opiniones y otros datos sensibles a partir de datos biométricos | Sin biometría ni inferencia de atributos sensibles |
| DS 115-2025-PCM, art. 25 [O13] | Transparencia algorítmica; si el sistema toma decisiones que afectan derechos, explicación comprensible a los afectados | Explicaciones por criterio y evidencia (sección 1.2) |
| DS 115-2025-PCM, art. 28.11 [O13] | Entidades públicas: supervisión humana capacitada y capaz de detener, corregir o invalidar | Si el colegio es privado no es obligatorio; se adopta como buena práctica |
| DS 115-2025-PCM, art. 30 [O13] | Evaluación de impacto **previa** al desarrollo o implementación de un sistema de riesgo alto | Condición de G0 (aprobada en F33), antes de F35–F40 |
| DS 115-2025-PCM, art. 31.1 [O13] | Sector privado: registro actualizado de principios de funcionamiento y fuentes de datos | Registro de modelos y datasets (F34, F36) |
| Ley 29733 [O15] y DS 016-2024-JUS [O09] | Protección de datos personales: consentimiento, finalidad, proporcionalidad, seguridad; datos sensibles | Gobernanza del dataset (sección 4.3) |
| RGPD, art. 22 [O02] (referencia) | Derecho a no ser objeto de decisiones basadas únicamente en tratamiento automatizado | Coincide con RF-23: la decisión final es humana |
| Ley de IA de la UE [O01, X01] (referencia) | Prohíbe el reconocimiento de emociones en el trabajo y la educación; reclutamiento de alto riesgo; supervisión humana consciente del sesgo de automatización | Estándar comparado de diseño |
| Reglamento (UE) 2026/1744 [O16] (referencia) | Aplaza al 2/12/2027 los requisitos de alto riesgo para los sistemas del Anexo III; no cambia la prohibición del art. 5.1.f | Calendario oficial de la UE; sustituye a la fuente secundaria [X02] |
| NIST AI RMF y SP 1270 [O03, O04]; ISO/IEC 42001 y 23894 [O05, O06] | Gestión de riesgos y sesgos | Estructura de la evaluación de impacto |

**Vigencia del DS 115-2025-PCM:** entra en vigor a los 90 días hábiles de su publicación (9/9/2025), salvo algunas disposiciones que rigen desde el día siguiente. La fecha exacta de vigencia se confirma en la evaluación de impacto.

**Alcance de la lectura del DS 115-2025-PCM:** el art. 24.1 e) está corroborado. Los arts. 24, 30 y 31 —y los demás citados en esta tabla— se leyeron en una copia no oficial de la publicación y **requieren contraste artículo por artículo con la publicación normativa oficial antes de producir efectos jurídicos**.

### 4.2 Conflicto de gobierno con el proyecto actual (hallazgo crítico)

La visión de un «motor inteligente» que **recomiende** choca con decisiones vigentes del proyecto:

| Decisión vigente | Texto | Choque con la visión |
|---|---|---|
| Contrato 4 (CLAUDE.md) | El ML es informativo y operacional, sobre el proceso, nunca evaluando, puntuando ni clasificando personas | Cualquier puntuación o nivel sugerido por ML sobre un postulante |
| ADR-001 | Prohíbe «puntuar, ordenar, recomendar, filtrar, preseleccionar o descartar postulantes; predecir desempeño, idoneidad…» | Recomendación de candidatos |
| ADR-001, alternativas rechazadas | Rechazó el «modelo de recomendación de candidatos» y la «puntuación asistida solo como sugerencia» | Sugerir niveles o puntajes |
| Alcance F9 | OUT-04 (selección automática por IA o ML), OUT-05 (inferencia de idoneidad), OUT-11 (uso decisorio de RF-29) | Todo uso del ML en la selección |

La evidencia de F30 **respalda esas decisiones** [S58, S60, S84]. Por eso F30 no las cambia: propone la puerta **G0** (ver [recomendaciones](F30_Recomendaciones_F33_F40.md#2-puerta-g0)), en la que el equipo decide de forma explícita y documentada qué puede hacer el motor. **Regla G0.** F33 formula y aprueba ADR-005, que constituye la puerta G0. F34 puede avanzar en paralelo **solo con datos sintéticos** y sin scoring ni recomendación de personas. F35–F40 **no comienzan sin G0 aprobado**. Lo que F30 recomienda —ayuda sobre el **proceso** y la **evidencia**, sin puntuar personas— cabe dentro de ADR-001 si un nuevo ADR lo precisa.

### 4.3 Gobernanza del dataset (F34)

**Principio:** sintético primero. Ningún dato real de postulantes entra al proyecto (contrato 7).

| Tema | Regla | Fuente |
|---|---|---|
| Origen | Datos sintéticos generados con semilla y script versionado, como en RF-29; nunca CV ni entrevistas reales | Contrato 7 |
| Anonimización | Si en el futuro hubiera datos reales: seudonimización en origen, eliminación de identificadores directos y verificación con texto ficticio; se mide el error de la herramienta (p. ej., Presidio o spaCy en español) | [O09, S33] |
| Consentimiento y finalidad | Específicos para investigación o mejora del proceso; separados de la postulación; revocables | [O09] |
| Minimización | Solo los campos que exige el criterio; sin foto, edad, sexo, estado civil ni dirección | [O09]; ADR-001 |
| Linaje | Cada conjunto con id, versión, SHA-256, script generador, semilla y fecha | [S72, S79] |
| Dataset card | Motivación, composición, recolección, preprocesamiento, usos permitidos y prohibidos, variedad lingüística | [S33, S72] |
| Registro | Inventario de conjuntos y modelos con responsable y estado | [O13 art. 31.1, S71] |
| Fuga de información | Particiones por convocatoria y en orden temporal; ningún campo derivado del resultado (p. ej., estado final) como entrada | [S74] |
| Etiquetas | Prohibido usar «contratado» o «seleccionado» como verdad de idoneidad | [S42, S48] |
| Retención y borrado | Plazos definidos; borrado verificable | [O09] |
| Acceso | Por organización (`organization_id`) y rol; nada cruza entre organizaciones | Contrato 5 |

**Atributos sensibles.** No se proponen para recolección. Antes de considerar cualquiera, el equipo debe responder estas cinco preguntas y registrarlas en la evaluación de impacto:

| Pregunta | Ejemplo para «sexo» o «discapacidad» con fines de auditoría de equidad |
|---|---|
| **Necesidad** | ¿Hay un análisis de equidad concreto que no pueda hacerse sin el dato? Con pocos postulantes, la respuesta probable es no (sección 2.1) |
| **Consentimiento** | Voluntario, separado de la postulación, sin efecto en la evaluación y revocable |
| **Base legal** | Tratamiento de datos sensibles según la Ley 29733 [O15] y su reglamento [O09]; validación jurídica |
| **Finalidad** | Solo auditoría agregada de equidad; nunca como entrada de un modelo ni visible para evaluadores |
| **Seguridad** | Almacenamiento separado, acceso restringido, agregación mínima para publicar, borrado |

**Decisión recomendada para F34:** no recolectar atributos sensibles. Si F37 necesitara medir equidad, usará datos sintéticos con atributos simulados para probar el método, y lo declarará como tal.

### 4.4 Evaluación de impacto previa (contenido mínimo)

Estructurada con NIST AI RMF (gobernar, mapear, medir, gestionar) [O03] y el art. 30 del DS 115-2025-PCM [O13]:

1. Finalidad, usuarios y personas afectadas (postulantes, evaluadores, Dirección).
2. Clasificación de riesgo (art. 24.1 e) y justificación.
3. Datos: origen, base legal, minimización, retención (sección 4.3).
4. Riesgos de sesgo humano, sistémico y estadístico [O04, S47] y sus medidas.
5. Supervisión humana y sesgo de automatización (sección 3).
6. Transparencia y explicaciones (sección 1.2).
7. Seguridad y cadena de suministro (ver [herramientas](F30_Analisis_Herramientas_Skills.md)).
8. Monitoreo y criterios de retirada: cuándo se apaga una función.
9. Responsable de la evaluación, revisión jurídica y fecha.
