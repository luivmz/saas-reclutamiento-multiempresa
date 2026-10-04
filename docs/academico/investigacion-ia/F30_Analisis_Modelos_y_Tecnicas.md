# F30 — Análisis de modelos y técnicas para el motor de reclutamiento

> Fase F30, versión 1 (30/09/2026), auditada e integrada. Es un diseño conceptual: no hay código, endpoints, migraciones ni modelos. Las citas remiten a la [matriz de evidencia](F30_Matriz_Evidencia_Cientifica.md). Lo que no lleva cita es **decisión o inferencia del equipo** y se presenta como tal.

## 1. Punto de partida: lo que el sistema ya hace

| Pieza actual | Qué hace | Qué no hace |
|---|---|---|
| Criterios y ponderaciones por vacante (RF-05, RF-20; A-06) | RR. HH. define criterios, rangos y pesos; la suma se valida | No deriva criterios de un análisis del puesto documentado |
| Resultados de evaluación (RF-19; A-19) | El evaluador asignado registra un puntaje por criterio, una vez | No guarda la evidencia ni la justificación de cada puntaje |
| Ranking (RF-21, RF-22; A-23, A-24, A-26) | Suma ponderada normalizada de 0 a 100, sin desempate automático | No muestra el porqué de cada puntaje ni el acuerdo entre evaluadores |
| Decisión final (RF-23; ADR-002) | Humana, con justificación y auditoría de solo inserción | — |
| RF-29 (experimental) | Estima el riesgo de demora del **proceso** | No evalúa personas (ADR-001, ADR-004) |

*Inferencia:* el hueco no es de «inteligencia» sino de **estructura y trazabilidad de la evidencia**. Hoy un puntaje es un número sin procedencia; la evidencia de RR. HH. [S13, S15, S19] indica que la calidad de la selección depende justamente de esa estructura.

## 2. Comparación de enfoques

| Enfoque | Datos que necesita | Explicabilidad | Riesgo de sesgo | Evidencia para el caso | Encaje con los contratos del proyecto | Veredicto |
|---|---|---|---|---|---|---|
| **Reglas y rúbricas** (BARS, completitud, consistencia) | Ninguno histórico; criterios definidos por expertos | Total: cada regla es legible | Bajo, controlable en la rúbrica | FUERTE para estructura [S13, S14, S15, S19] | Total | **Base del motor** |
| **MCDM** (suma ponderada actual; AHP para pesos) | Juicio experto | Alta | El de los pesos | MODERADA para AHP [S39]; LIMITADA para TOPSIS [S40] | Total: ya es RF-21 | Mantener la suma ponderada; AHP opcional para justificar pesos |
| **ML interpretable** (regresión logística, EBM, árboles poco profundos) | Etiquetas válidas y suficientes, que el caso no tiene | Alta [S51] | Por etiqueta y *proxy* [S42, S48] | Sin datos válidos para personas [S04, S22] | Prohibido sobre personas (ADR-001); permitido sobre el proceso (RF-29) | Solo sobre el **proceso** |
| **NLP clásico y embeddings** (NER, similitud) | Modelos preentrenados más datos de validación locales | Media: la similitud es un número opaco | Alto: sesgo por nombre y género [S11, S32] | MODERADA para recuperar [S31]; en contra para puntuar [S11] | Solo como **localizador de evidencia** con confirmación humana; requiere G0 | Evaluar en sandbox |
| **LLM** (generación, juez, resumen) | Ninguno para usarlo; mucho para validarlo | Baja; alucina [S34] | Alto [S83, S87]; sesgos de juez [S36] | En contra para evaluar personas | Incompatible para evaluar; posible solo en tareas sin personas | Evitar en la evaluación |

**Conclusión (inferencia del equipo):** reglas, rúbricas y la suma ponderada actual cubren lo que la evidencia respalda. El ML interpretable se limita al proceso. NLP y embeddings solo pueden **localizar** evidencia con confirmación humana. Los LLM quedan fuera de toda evaluación de personas.

## 3. Criterios de vacante y competencias

### 3.1 Proceso recomendado

La cadena sigue la evidencia de RR. HH. [S17, S18, S19, S24]:

```
Análisis del puesto ─► Competencias ─► Criterios evaluables ─► Indicadores conductuales
        ─► Niveles BARS (descriptor por nivel) ─► Preguntas estructuradas por criterio
        ─► Pesos justificados (directos o AHP) ─► Versión congelada al publicar la vacante
```

- **Análisis del puesto:** tareas, contexto y requisitos. Lo hacen RR. HH. y la Dirección, y queda documentado.
- **Competencias:** se toman de un catálogo versionado (`criteria_version`). Para docentes, se derivan del MBDD [O14] y las valida el colegio.
- **Criterio evaluable:** cada criterio dice qué método lo evalúa (CV, entrevista, clase demostrativa) y con qué evidencia.
- **Niveles BARS:** cuatro o cinco niveles con conducta observable por nivel, versionados (`rubric_version`) [S19].
- **Preguntas:** situacionales o de conducta pasada, iguales para todos los postulantes de la vacante [S14, S15].
- **Pesos:** la regla actual de suma 100 (A-06) se mantiene; AHP es opcional para documentar la justificación [S39].
- **Congelamiento:** como hoy (A-07), los criterios no cambian después de publicar; la versión queda ligada a cada evaluación.

### 3.2 Ejemplo ilustrativo: vacante docente

> **Ilustrativo y no adoptado.** Sirve para mostrar la forma; el contenido lo define y valida el colegio en F33. Las competencias se inspiran en los dominios del Marco de Buen Desempeño Docente [O14] y no reproducen su redacción oficial. Los datos son ficticios.

| Criterio (ejemplo) | Dominio MBDD de referencia | Método | Evidencia esperada | Peso (ejemplo) |
|---|---|---|---|---|
| Planificación de la enseñanza | Preparación para el aprendizaje | Entrevista estructurada + muestra de sesión | Describe cómo diseña una sesión a partir de un propósito de aprendizaje | 25 |
| Conducción del aprendizaje en aula | Enseñanza para el aprendizaje | Clase demostrativa observada con rúbrica | Conductas observadas durante la clase | 30 |
| Evaluación formativa | Enseñanza para el aprendizaje | Entrevista estructurada | Ejemplo concreto de retroalimentación a un estudiante | 20 |
| Trabajo con familias y comunidad | Participación en la gestión escolar | Entrevista estructurada | Situación pasada de coordinación con familias | 10 |
| Desarrollo profesional | Profesionalidad e identidad docente | CV + entrevista | Formación y reflexión sobre su práctica | 15 |

Ejemplo de rúbrica BARS para «Evaluación formativa» (ilustrativo):

| Nivel | Descriptor conductual |
|---|---|
| 1 — Insuficiente | No describe ninguna práctica de retroalimentación o solo menciona calificar |
| 2 — En inicio | Menciona la retroalimentación en general, sin ejemplo concreto |
| 3 — Logrado | Da un ejemplo concreto: qué observó, qué retroalimentó y cómo respondió el estudiante |
| 4 — Destacado | Da un ejemplo concreto y explica cómo ajustó su enseñanza a partir de lo observado |

Quedan **fuera** de los criterios: edad, sexo, estado civil, apariencia, acento, lugar de origen, religión, discapacidad y cualquier otro atributo protegido o su *proxy* (ADR-001). También quedan fuera la «personalidad» y el «ajuste cultural» [S07, S08].

## 4. Cadena de procedencia de la evidencia

Es el núcleo del motor. Cada nivel asignado debe poder recorrerse hacia atrás hasta lo que dijo o presentó el postulante.

```
Pregunta ─► Respuesta ─► Evidencia ─► Competencia/criterio ─► Nivel ─► Justificación ─► Confianza
 (versión)   (fuente)     (fragmento)   (criteria_version)     (BARS)    (texto humano)    (explícita)
```

| Eslabón | Qué es | Quién lo produce | Regla |
|---|---|---|---|
| Pregunta | Ítem de la guía de entrevista, con id y `rubric_version` | RR. HH. | Igual para todos los postulantes de la vacante |
| Respuesta | Notas del evaluador o fragmento de transcripción revisada | Evaluador (o STT revisado por humano) | Una transcripción sin revisar no es respuesta válida [S81] |
| Evidencia | Fragmento concreto: cita textual, sección del CV o conducta observada | Evaluador; el sistema solo puede **sugerir** fragmentos | Toda evidencia apunta a su fuente (documento, minuto, línea) |
| Criterio | Criterio y competencia a los que se asigna la evidencia | Evaluador | Debe existir en la `criteria_version` congelada |
| Nivel | Nivel BARS elegido | **Solo el evaluador humano** | Sin nivel sugerido por el sistema (ADR-001) [S58, S84] |
| Justificación | Por qué esa evidencia corresponde a ese nivel y no al siguiente | Evaluador | Contrastiva [S55]; obligatoria |
| Confianza | Suficiencia de la evidencia: suficiente, parcial o insuficiente | Evaluador; el sistema señala la ausencia de evidencia | Incertidumbre epistémica explícita [S70]; no es una probabilidad |

**Lo que el sistema puede verificar y decir** (recomendaciones sobre el proceso, no sobre la persona):

- falta evidencia para un criterio;
- hay un nivel sin justificación;
- dos evaluadores difieren en más de un nivel;
- una pregunta no se hizo a todos los postulantes;
- se cambió la rúbrica después de publicar la vacante.

*Decisión de ingeniería propuesta:* estas verificaciones son **reglas deterministas**, no ML.

## 5. Pipeline seguro de audio y vídeo

**Recomendación base: no grabar.** La entrevista estructurada con notas del evaluador ya captura la evidencia necesaria [S13, S15]. La grabación solo se justifica si F33 demuestra una necesidad concreta (p. ej., revisión por un segundo evaluador) y pasa la puerta G0.

Si se aprueba, el pipeline se limita a esto:

```
Consentimiento informado específico ─► Grabación de solo audio (vídeo: no) ─► Almacenamiento cifrado, con plazo de retención
  ─► STT local (sin enviar audio a terceros) ─► Revisión humana de la transcripción contra el audio
  ─► Segmentación por pregunta (marcas manuales del evaluador, sin huella de voz)
  ─► [Opcional, sandbox] sugerencia de fragmentos por criterio ─► Confirmación humana
  ─► Calificación humana con BARS ─► Eliminación del audio al vencer el plazo
```

| Paso | Control | Fuente |
|---|---|---|
| Consentimiento | Específico para grabar y transcribir; con alternativa sin grabación y sin penalización | [O09, O13] |
| Solo audio | Añadir vídeo apenas mejora la exactitud y aumenta el sesgo | [S85] |
| STT local | Whisper o una variante, con versión fijada | [S38] |
| Revisión humana | Contra el audio: corrige alucinaciones y errores | [S81] |
| Medición por variedad de habla | WER por grupo de hablantes en un piloto con voces ficticias o consentidas | [S10] |
| Segmentación | Por marcas manuales o canales separados; **sin diarización biométrica** | [S88, O09] |
| Retención | Plazo definido y borrado verificable | [O09] |

**Prohibido en cualquier versión:**

- emociones, estados de ánimo, estrés o «nerviosismo» [S08, S09, O01, O13];
- personalidad o rasgos [S07];
- expresiones faciales, mirada o gestos [S08, S85];
- prosodia, tono, fluidez, acento o velocidad del habla [S10, S85];
- huellas de voz o identificación biométrica [S88, O13];
- calificación automática del contenido [S84, S89 en tensión].

## 6. Métricas por tarea

| Tarea | Métrica | Por qué | Fuente |
|---|---|---|---|
| Acuerdo entre evaluadores | ICC (forma declarada, intervalo del 95 %) | Fiabilidad de la calificación humana | [S20, S21] |
| Completitud de la evidencia | Porcentaje de criterios con evidencia y justificación | Calidad del proceso | Decisión de ingeniería |
| Transcripción (si se aprueba) | WER global y **por grupo de hablantes**; tasa de alucinación detectada en la revisión | Errores desiguales y frases inventadas | [S10, S81] |
| Sugerencia de fragmentos (si se aprueba) | Precisión, exhaustividad y F1 por tramo frente a la anotación humana | Mide la localización, no al postulante | [S29, S30] |
| Modelo del proceso (RF-29) | PR-AUC, Brier y calibración | Clases desbalanceadas y probabilidades | [S64, S66, S68] |
| Ranking | Estabilidad ante cambios de pesos (análisis de sensibilidad) | Transparencia del orden | Decisión de ingeniería |
| NDCG | Solo si existe un juicio de relevancia válido, que hoy no existe | Evitar métricas sin verdad de terreno | [S69] |
| Equidad | Tasas de selección por grupo (cuatro quintos como indicio) **solo con datos legales y muestra suficiente** | Impacto adverso | [O11, S44, S46] |
| Supervisión humana | Tasa de desacuerdo con la sugerencia de fragmentos; tiempo de revisión | Detectar aceptación acrítica | [S58, S84] |

Ninguna métrica de esta tabla puntúa a un postulante. Todas miden la calidad del proceso o de una herramienta.

## 7. Arquitectura futura (conceptual)

Extiende el patrón de RF-29 (Laravel ↔ FastAPI con *fallback*, ver `docs/v1.1/phase-16-laravel-ml-integration.md`) y los principios de MLOps y despliegue [S76, S77, S78]:

```
Laravel (dominio, Policies, organization_id, auditoría)
   │  1. crea analysis_run (estado: pendiente) e input_snapshot_hash
   │  2. encola un trabajo (cola Redis existente)
   ▼
Worker Laravel ──REST──► ml-service (FastAPI, sin estado de negocio)
   │   Idempotency-Key = analysis_run_id     • timeout de conexión y lectura
   │   reintentos con espera exponencial      • circuit breaker con fallback
   ▼
Resultado validado por esquema ─► se guarda como SUGERENCIA (nunca como nivel ni decisión)
   ▼
Interfaz del evaluador: muestra la sugerencia DESPUÉS de su calificación independiente
```

| Requisito | Diseño |
|---|---|
| REST | Contrato versionado (`/v2/...`), validación de esquema en ambos extremos, autenticación interna como en RF-29 |
| Asíncrono | Trabajos en cola; la interfaz nunca espera al servicio ML |
| Idempotencia | `analysis_run_id` como clave; repetir una petición no duplica resultados |
| Timeouts y reintentos | Límites explícitos; reintentos acotados con espera exponencial; sin reintento ante errores de validación |
| Circuit breaker | Tras N fallos se abre el circuito y la página sigue funcionando sin la sugerencia, como RF-29 |
| Versionado | `model_version`, `rubric_version`, `criteria_version` e `input_snapshot_hash` en cada ejecución |
| Multiempresa | `organization_id` permanece preferentemente en Laravel, que aplica Policies y scope global. **No se envía al servicio ML *stateless* salvo justificación explícita**; en su lugar viajan identificadores técnicos pseudónimos mínimos (p. ej., `analysis_run_id` o un token por ejecución). Ningún modelo se entrena ni consulta con datos de otra organización |
| Privacidad | El servicio ML recibe texto minimizado, sin nombre, DNI, correo ni foto, y solo identificadores pseudónimos; no persiste entradas |

## 8. Modelo de auditoría de una ejecución

Registro por cada `analysis_run`. La auditoría crítica sigue en `AuditLogger` (solo inserción).

| Campo | Persistir | Motivo o cuidado |
|---|---|---|
| `analysis_run_id` | Sí | Clave e idempotencia |
| `organization_id`, `vacancy_id`, `application_id` | Sí, solo en Laravel | Multiempresa y trazabilidad; no viajan al servicio ML salvo justificación explícita |
| `criteria_version`, `rubric_version` | Sí | Reproducibilidad del marco de evaluación |
| `model_version` (y hash del artefacto) | Sí | Qué modelo o regla produjo la sugerencia |
| `input_snapshot_hash` | Sí | Probar qué entrada se usó **sin guardar la entrada** |
| Texto de entrada completo | **No** | PII; se reconstruye desde la fuente con su hash si hace falta |
| `evidence_refs` | Sí | Ids y posiciones de los fragmentos, no el texto |
| `suggestion` | Sí, si existe | Solo fragmentos sugeridos por criterio; **nunca nivel ni puntaje** |
| `human_level`, `human_justification`, `evidence_sufficiency` | Sí | Eslabones humanos de la cadena |
| `reviewer_id`, `reviewed_at` | Sí | Quién y cuándo |
| `suggestion_seen_before_scoring` | Sí | Debe ser falso: control del sesgo de anclaje [S84] |
| `human_disagreement` | Sí | Si el humano descartó la sugerencia; monitorea la aceptación acrítica [S58] |
| `latency_ms`, `status`, `error_code` | Sí | Operación |
| `final_decision` | **No en este registro** | La decisión vive en RF-23 y su auditoría; el análisis nunca la referencia como causa |
| Audio, transcripción no revisada, embeddings | **No** | Datos personales o biométricos sin necesidad de conservarse |
| Atributos sensibles (sexo, edad, discapacidad…) | **No** | Solo en un estudio de equidad separado, con base legal (ver gobernanza) |
