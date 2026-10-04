# F33 — Flujos funcionales

> Fase F33, versión 1 (04/10/2026), **pendiente de auditoría**. Flujos de **diseño**: no existen en el código. Los códigos de error E-xx están en el [diseño funcional §12](F33_Diseno_Funcional_Motor_Inteligente.md#12-errores-y-excepciones). **G0 = NO APROBADA**: ninguno de estos flujos se implementa hasta que el equipo apruebe G0 (al menos CON RESTRICCIONES para FF-01 a FF-06).

![Flujo funcional](diagramas/F33-01_flujo_funcional.png)

*Figura 1. Visión general del flujo. Reproducible con `docs/academico/tools/f33/diagramas.py`.*

## Resumen

| Flujo | Nombre | Alcance | G0 requerida | Base actual |
|---|---|---|---|---|
| FF-01 | Configurar vacante, competencias y rúbrica | B | CON RESTRICCIONES | RF-05, RF-06, RF-20 · CU-04, CU-05, CU-16 |
| FF-02 | Registrar evidencia y valoración humana (`PROGRAMADA` → registro → `REALIZADA`) | B | CON RESTRICCIONES | RF-19 · CU-15 · `AssessmentResultRecorder` |
| FF-03 | Entrevista estructurada | B | CON RESTRICCIONES | RF-18, RF-19 · CU-14, CU-15 |
| FF-04 | Verificar el proceso (alertas e ICC) | B | CON RESTRICCIONES | — (nuevo) |
| FF-05 | Comparación estructurada y apoyo explicable | B | CON RESTRICCIONES | RF-21, RF-22 · CU-17 |
| FF-06 | Decisión final humana | Existente | No cambia | RF-23 a RF-25 · CU-18 a CU-20 |
| FF-07 | Asistencia documental | C | **APROBADA + ADR adicional** | — (futuro) |
| FF-08 | Fallo del servicio y fallback | C | **APROBADA** | Patrón de RF-29 |

## FF-01 — Configurar vacante, competencias y rúbrica

- **Actor:** RR. HH.
- **Precondiciones:**
  - vacante en `borrador` (A-07);
  - catálogo de competencias publicado para la organización;
  - usuario con rol RR. HH. de la misma organización.
- **Pasos:**
  1. Elegir las competencias del catálogo (versión vigente).
  2. Definir los criterios con método de evaluación, rango y peso; validar la suma (A-06).
  3. Asociar a cada criterio una rúbrica BARS publicada y preguntas estructuradas.
  4. Validar la configuración completa (RF-06 + reglas nuevas).
  5. Publicar: congela `criteria_version` y `rubric_version` (A-07).
- **Postcondiciones:** la vacante está publicada con versiones congeladas y queda la auditoría de la publicación.
- **Errores:**
  - E-01 (rúbrica incompleta);
  - E-02 (criterio sin rúbrica o sin preguntas);
  - E-05 (otra organización).
- **Excepciones:** si cambia el catálogo de competencias después de publicar, no afecta a la vacante, que conserva su versión.
- **Límites:** el sistema no propone competencias ni pesos a partir de datos de candidatos.

## FF-02 — Registrar evidencia y valoración humana

- **Actor:** evaluador asignado (Policy `recordResult`: solo el evaluador asignado a la sesión).
- **Base vigente:** `app/Services/Assessments/AssessmentResultRecorder.php` (RF-19, A-19). El diseño **conserva** su comportamiento y solo añade evidencia, nivel, justificación y suficiencia al mismo registro.
- **Precondiciones:**
  - sesión (evaluación o entrevista) en estado **`PROGRAMADA`** (`AssessmentStatus::Scheduled`); si no lo está, se rechaza con «Los resultados de esta sesión ya fueron registrados»;
  - evaluador asignado, de la misma organización;
  - vacante no cerrada.
- **Pasos:**
  1. Revisar el CV privado y los documentos (lectura humana; descarga por Policy, C15).
  2. Preparar en borrador las evidencias de cada criterio con su fuente (texto que la persona cita o introduce).
  3. Por criterio, elegir el nivel BARS, escribir la justificación contrastiva («por qué este nivel y no el siguiente») y marcar la suficiencia de la evidencia.
  4. **Registrar el resultado** en una sola transacción con bloqueo, como hoy:
     - validar todos los criterios de la etapa (`ScoreSheetValidator`, RF-20);
     - insertar **un resultado por criterio**, con el puntaje derivado del nivel de forma determinista (restricción única sesión–criterio);
     - vincular las evidencias, que pasan a inmutables.
  5. En la misma transacción, la sesión pasa a **`REALIZADA`** (`AssessmentStatus::Completed`, `completed_at`) y se audita (`EvaluationResultRecorded` o `InterviewResultRecorded`).
- **Secuencia:** `PROGRAMADA` → registro del resultado → `REALIZADA`.
- **Postcondiciones:**
  - resultado **vigente, único e inmutable** por sesión y criterio (A-19);
  - el ranking solo usa sesiones `REALIZADA` (A-23);
  - se crea el `analysis_run` de verificación (FF-04).
- **Errores:**
  - E-03 (evidencia sin fuente);
  - E-04 (sin justificación);
  - E-05 (evaluador no asignado);
  - E-13 (segundo resultado sobre una sesión `REALIZADA`: rechazado).
- **Después del registro: ANOTACIONES COMPLEMENTARIAS.**
  - No existe «corrección de puntaje»: **no se crea un segundo resultado** ni se edita el registrado.
  - Si hace falta un complemento (una aclaración o una fuente adicional), se registra como **anotación complementaria**: entidad aparte, de solo inserción y auditada, con autor, fecha y motivo.
  - Una anotación complementaria **no modifica** el puntaje, el nivel, la justificación ni la valoración registrados, y se muestra diferenciada del resultado.
- **Límites:**
  - **ninguna ayuda del sistema se muestra antes del paso 4** (E-12);
  - el sistema no sugiere niveles;
  - con la vacante cerrada no se registran resultados (A-19).

## FF-03 — Entrevista estructurada

- **Actor:** evaluador (entrevistador).
- **Precondiciones:** entrevista programada (RF-18) y preguntas de la vacante publicadas.
- **Pasos:**
  1. Formular a todos los postulantes las mismas preguntas, en el mismo orden.
  2. Registrar la respuesta como **notas del evaluador** (por defecto no se graba).
  3. Seguir la cadena de FF-02: respuesta → evidencia → criterio → nivel → justificación → suficiencia.
- **Postcondiciones:** valoración por pregunta y criterio con procedencia.
- **Errores:** E-08 (pregunta no formulada a todos).
- **Variante futura (audio, solo con G0 APROBADA):**
  1. Solo con datos ficticios en este proyecto. Con personas reales se aplica la regla de datos de ADR-005 §6.10; el consentimiento por sí solo no basta.
  2. Grabación de solo audio.
  3. STT local.
  4. Revisión humana contra el audio.
  5. Texto revisado como respuesta.
  6. Borrado del audio al vencer el plazo de retención.
- **Límites:**
  - sin prosodia, acento, emociones, rostro, vídeo ni biometría;
  - sin análisis automático de la transcripción para sugerir niveles.

## FF-04 — Verificar el proceso

- **Actor:** sistema (reglas deterministas). Revisa: evaluador o RR. HH.
- **Disparadores:** se registra un resultado o una anotación complementaria, se publica una vacante o se va a mostrar la comparación.
- **Pasos:**
  1. Crear un `analysis_run` inmutable con `rules_version`, versiones congeladas e `input_snapshot_hash`, y su evento `en_proceso`.
  2. Aplicar las reglas:
     - evidencia faltante por criterio;
     - nivel sin justificación;
     - requisito obligatorio no evidenciado (CAP-01);
     - discrepancia entre evaluadores mayor a un nivel (E-07);
     - pregunta omitida (E-08);
     - versión distinta (E-06).
  3. Calcular el ICC en los criterios de doble calificación (dos sesiones con evaluadores distintos sobre los mismos criterios; A-23 ya promedia varios puntajes de un criterio).
  4. Registrar las alertas abiertas y añadir el evento `completado` en `analysis_run_events`.
- **Postcondiciones:** las alertas quedan visibles para RR. HH., el evaluador y el aprobador.
- **Excepciones:** descartar una alerta exige motivo y usuario (`human_override`).
- **Límites:**
  - las alertas **no cambian puntajes, estados ni el ranking**;
  - no hablan de la persona («candidato débil»), solo del proceso («falta evidencia en el criterio X»).

## FF-05 — Comparación estructurada y apoyo explicable

- **Actores:** RR. HH. y Aprobador / Dirección.
- **Precondiciones:** valoraciones registradas; configuración válida (RF-20).
- **Pasos:**
  1. Calcular RF-21 como hoy (A-24), sin desempate automático (A-26).
  2. Mostrar el desglose por criterio, con:
     - el nivel humano;
     - la justificación;
     - las evidencias enlazadas;
     - la suficiencia;
     - las alertas abiertas;
     - el ICC donde aplique.
- **Postcondiciones:** ninguna. La vista es de solo lectura y no escribe estado (ADR-002).
- **Límites:**
  - sin insignias de «recomendado», «mejor candidato» ni semáforos sobre personas;
  - el riesgo RF-29 se muestra lejos de la comparación (OUT-11).

## FF-06 — Decisión final humana (sin cambios)

- **Actor:** Aprobador / Dirección.
- **Pasos:** los mismos de RF-23 a RF-25. El análisis **no** figura como causa de la decisión ni se guarda en el registro de la decisión.
- **Límites:** ADR-002 sin cambios. Ninguna ruta automática (evento, job o servicio) puede cambiar la selección.

## FF-07 — Asistencia documental (FUTURA, alternativa C)

- **Estado:** no habilitado. Requiere G0 APROBADA y un ADR que enmiende de forma acotada ADR-001 (datos del servicio).
- **Precondición clave:** la valoración del evaluador para ese criterio ya está registrada (FF-02, paso 4).
- **Pasos:**
  1. Laravel crea un `analysis_run` (inmutable) con un token pseudónimo, añade el evento `pendiente` y encola el job con `Idempotency-Key`.
  2. El servicio recibe texto minimizado y devuelve **referencias a fragmentos** con `model_version` y `schema_version`.
  3. Laravel valida el esquema: E-11 si trae puntajes, niveles o campos no previstos.
  4. **Revisión y confirmación humana:** el evaluador, después de registrar su resultado, revisa los fragmentos como sugerencias **pendientes**, todavía no visibles como ayuda, y confirma o rechaza cada uno.
  5. **Ayuda visible:** solo los fragmentos confirmados se muestran al evaluador y al aprobador, como **anotaciones complementarias** diferenciadas del resultado. Nunca cambian el resultado registrado.
- **Secuencia:** localizador → revisión y confirmación humana → ayuda visible.
- **Postcondiciones:** quedan registrados los fragmentos confirmados o rechazados (`human_override`) y los eventos de la ejecución.
- **Límites:**
  - no hay similitud visible;
  - no hay búsqueda entre candidatos;
  - no hay resumen de la persona.

## FF-08 — Fallo del servicio y fallback (FUTURO)

- **Disparadores:** timeout, error 5xx, circuito abierto o respuesta inválida.
- **Pasos:**
  1. Reintentos acotados solo ante errores transitorios.
  2. Al agotarlos, se añade el evento `fallido` o `expirado` en `analysis_run_events`.
  3. Se registra el error (sin PII).
  4. El flujo FF-02 a FF-06 continúa sin ayuda.
- **Límites:** la falta de ayuda nunca bloquea una evaluación ni una decisión (patrón de RF-29).
