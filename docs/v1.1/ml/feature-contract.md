# Contrato de features

**Fase 14 · 20 de septiembre de 2026**

Diccionario exhaustivo de las variables candidatas. Ninguna está implementada. Toda feature se calcula **solo con información existente en `checkpoint_at` o antes**; esa regla no admite excepción.

Marcas: **[HECHO]** verificado en código · **[APROBADA]** decisión del equipo · **[PROPUESTA]** sin aprobar · **[PENDIENTE]** requiere decisión · **[LIMITACIÓN]** restricción conocida.

> **[APROBADA] Decisión 9 del equipo, 20 de septiembre de 2026.** Este contrato queda aprobado como **baseline de trabajo** para la Fase 15, con sus cinco categorías intactas: incluidas, condicionadas, de ablation, excluidas y prohibidas. Ninguna variable relacionada con identidad, atributos sensibles, CV, universidad, puntajes, entrevistas o sus resultados, ranking, selección o decisión humana puede incorporarse. Cualquier cambio posterior al contrato requiere una decisión explícita nueva y la actualización de este documento.

## 0. Regla temporal universal

Para toda feature `f` derivada de un evento con marca temporal `t`:

```
se incluye el evento  ⟺  t <= checkpoint_at
```

Ningún conteo, duración, diferencia ni bandera puede depender de un registro posterior. Las features se computan sobre el historial **truncado** en el checkpoint, no sobre el estado final de la fila.

---

## 1. Features incluidas

Formato de cada entrada: ID · nombre canónico · definición · tipo/unidad · dominio · fuente · estado · disponibilidad · faltantes · leakage · ética · decisión.

### ML-FEAT-01 · `elapsed_days_since_publication`

- **Definición:** `días(checkpoint_at − published_at)`, en `America/Lima`.
- **Tipo/unidad:** entero, días. **Dominio:** `≥ 0`; se valida `> 0` porque el checkpoint es posterior al cierre de postulaciones.
- **Fuente:** **[HECHO]** `vacancies.published_at`, timestamp escrito al publicar (`app/Services/Vacancies/VacancyService.php:104`).
- **Estado:** derivable. **Disponible en:** publicación, muy anterior al checkpoint.
- **Faltantes:** imposible por elegibilidad (la vacante debe estar publicada).
- **Leakage:** ninguno; ambos extremos son anteriores o iguales al checkpoint.
- **Ética:** operacional, sin relación con personas.
- **Decisión:** **incluir**.

### ML-FEAT-02 · `days_remaining_to_target`

- **Definición:** `días(target_completion_at − checkpoint_at)`.
- **Tipo/unidad:** entero, días. **Dominio:** `> 0` por elegibilidad.
- **Fuente:** **[APROBADA]** `ML-DECISION-01` quedó resuelta el 20/09/2026. En el **dataset sintético** se deriva de `target_completion_at`, que el generador produce como **variable operacional explícita** fijada antes de la publicación. **[PENDIENTE]** En Laravel no existe fuente todavía: depende de `GAP-01`. **`job_requests.required_by` queda descartado como origen.**
- **Estado:** **incluida para el experimento sintético**; no computable en producción hasta resolver `GAP-01`.
- **Leakage:** ninguno si el plazo es inmutable y previo a la publicación. **[LIMITACIÓN]** Si el plazo pudiera ajustarse durante el proceso, esta feature filtraría información del desenlace y quedaría prohibida. El generador debe garantizar la inmutabilidad, y una validación del dataset lo comprueba.
- **Ética:** operacional.
- **Decisión:** **incluir**. Es la única feature del núcleo que **no** tiene equivalente en el sistema actual, y ese hecho debe declararse en toda conclusión: el modelo entrenado con ella no es desplegable hasta que `GAP-01` se resuelva.

### ML-FEAT-03 · `application_window_days`

- **Definición:** `días(closes_at − opens_at)`. Regla de respaldo cuando `opens_at` es nulo: `días(closes_at − fecha(published_at))`.
- **Tipo/unidad:** entero, días. **Dominio:** `≥ 0`.
- **Fuente:** **[HECHO]** `vacancies.opens_at` y `closes_at`, ambas `date` **nullable** (`…000006…:22-23`), con `CHECK (closes_at >= opens_at)` (`…000006…:40`).
- **Estado:** derivable. **Disponible en:** configuración de la vacante.
- **Faltantes:** **[HECHO]** `opens_at` puede ser nulo; la regla de respaldo la hace siempre computable. `closes_at` nulo excluye la vacante por elegibilidad.
- **Leakage:** ninguno.
- **Decisión:** **incluir**, documentando la regla de respaldo en el generador y en el preprocesamiento.

### ML-FEAT-04 · `positions_count`

- **Definición:** número de plazas de la vacante.
- **Tipo/unidad:** entero, plazas. **Dominio:** `≥ 1`.
- **Fuente:** **[HECHO]** `vacancies.positions`, `unsignedSmallInteger` con `CHECK (positions >= 1)` (`…000006…:21` y `:39`).
- **Estado:** existente. **Disponible en:** configuración.
- **Leakage:** ninguno. **Ética:** operacional.
- **Decisión:** **incluir**; su utilidad se comprueba, no se asume.

### ML-FEAT-05 · `applications_received_count`

- **Definición:** `count(applications donde vacancy_id = V y applied_at <= checkpoint_at)`.
- **Tipo/unidad:** entero, postulaciones. **Dominio:** `≥ 0`.
- **Fuente:** **[HECHO]** `applications.applied_at`, timestamp obligatorio (`…000008…:19`).
- **Estado:** derivable. **Leakage:** controlado por la regla temporal.
- **Ética:** **agregado puro**. No entra ningún atributo, identidad ni resultado de candidato.
- **Decisión:** **incluir**.

### ML-FEAT-06 · `configured_criteria_count`

- **Definición:** `count(evaluation_criteria donde vacancy_id = V)`.
- **Tipo/unidad:** entero. **Dominio:** `≥ 0`.
- **Fuente:** **[HECHO]** tabla `evaluation_criteria` (`…000006…:55-68`), con unicidad `(vacancy_id, name)`.
- **Estado:** existente. **Leakage:** ninguno: mide complejidad de configuración, no contenido ni puntajes.
- **Ética:** no incluye pesos, rangos ni resultados.
- **Decisión:** **incluir**.

### ML-FEAT-07 · `configured_stage_count`

- **Definición:** número de valores distintos de `stage` entre los criterios de la vacante.
- **Tipo/unidad:** entero. **Dominio:** **[HECHO]** `{0, 1, 2}` — el `CHECK` del esquema solo admite `'evaluacion'` y `'entrevista'` (`…000006…:72`).
- **Estado:** derivable, pero de cardinalidad mínima.
- **[LIMITACIÓN]** Con tres valores posibles y fuerte correlación con ML-FEAT-06, su aporte informativo esperado es muy bajo.
- **Decisión:** **ablation candidate**, fuera del conjunto núcleo. Se prueba, no se asume.

### ML-FEAT-08 · `evaluations_scheduled_count`

- **Definición:** `count(evaluations de postulaciones de V con created_at <= checkpoint_at)`.
- **Fuente:** **[HECHO]** tabla `evaluations` (`…000009…:12-33`).
- **Leakage:** se cuenta el acto de programar, no su resultado. **Ética:** ningún puntaje.
- **Decisión:** **incluir**.

### ML-FEAT-09 · `evaluations_completed_count`

- **Definición:** `count(evaluations con completed_at <= checkpoint_at)`.
- **Fuente:** **[HECHO]** `evaluations.completed_at`, con `CHECK ((status='realizada') = (completed_at IS NOT NULL))` (`…000009…:39`), lo que hace la señal inequívoca.
- **Leakage:** es un evento contemporáneo, no un outcome. **Ética:** **nunca** se leen `evaluation_results.score` ni `observations`.
- **Decisión:** **incluir**.

### ML-FEAT-10 · `evaluations_pending_count`

- **Definición:** `ML-FEAT-08 − ML-FEAT-09`.
- **[LIMITACIÓN] Colinealidad perfecta.** Es una combinación lineal exacta de dos features ya incluidas. En Logistic Regression eso produce coeficientes inestables y una interpretación global engañosa.
- **Decisión:** **incluir en el dataset** por legibilidad operacional, pero **excluir de `X`** cuando el modelo sea lineal, o eliminar una de las tres. La decisión se documenta en el preprocesamiento, no se deja al azar.

### ML-FEAT-11 · `evaluations_overdue_pending_count`

- **Definición:** `count(evaluations con scheduled_at < checkpoint_at y sin completed_at <= checkpoint_at)`.
- **Fuente:** **[HECHO]** `evaluations.scheduled_at` es obligatorio (`…000009…:21`).
- **Leakage:** ninguno: mide backlog vencido en el instante del checkpoint, no el futuro.
- **Decisión:** **incluir**. Es una de las señales operacionales más plausibles.

### ML-FEAT-12 a ML-FEAT-15 · entrevistas

Espejo exacto de ML-FEAT-08 a ML-FEAT-11 sobre la tabla `interviews`:

| ID | Nombre | Nota |
|---|---|---|
| ML-FEAT-12 | `interviews_scheduled_count` | **[HECHO]** `interviews.scheduled_at` obligatorio (`…000010…:20`) |
| ML-FEAT-13 | `interviews_completed_count` | **[HECHO]** `CHECK` liga `status='realizada'` con `completed_at` **y** `outcome` no nulos (`…000010…:38`) |
| ML-FEAT-14 | `interviews_pending_count` | Misma advertencia de colinealidad que ML-FEAT-10 |
| ML-FEAT-15 | `interviews_overdue_pending_count` | Backlog vencido contemporáneo |

**Ética:** **[HECHO]** `interviews.outcome` (`recomendado`, `recomendado_con_reservas`, `no_recomendado`, `…000010…:37`) es un juicio sobre una persona y está **prohibido**. Solo se cuenta la existencia del evento completado, nunca su valor.

### ML-FEAT-16 · `stage_transition_count`

- **Definición:** `count(application_stage_histories de postulaciones de V con created_at <= checkpoint_at)`.
- **Fuente:** **[HECHO]** tabla `application_stage_histories` con `created_at useCurrent()` e índice `(application_id, created_at)` (`…000008…:31-42`).
- **[LIMITACIÓN]** Es un agregado de movimientos de personas. Se admite porque mide *ritmo del proceso*, no *calidad de nadie*, pero **no** se desagrega por estado destino: eso reintroduciría resultados individuales.
- **Decisión:** **incluir con cautela**, solo como conteo total.

### ML-FEAT-17 · `days_since_last_operational_event`

- **Definición:** `días(checkpoint_at − max(t))` donde `t` recorre, **solo hasta el checkpoint**: `published_at`, `applications.applied_at`, `evaluations.created_at`, `evaluations.completed_at`, `interviews.created_at`, `interviews.completed_at` y `application_stage_histories.created_at`.
- **Tipo/unidad:** entero, días. **Dominio:** `≥ 0`.
- **Faltantes:** si no hay ningún evento posterior a la publicación, el máximo es `published_at`; nunca queda indefinida.
- **Leakage:** ninguno, por construcción del máximo truncado.
- **Decisión:** **incluir**. La lista de eventos es cerrada y debe versionarse con el contrato.

### ML-FEAT-18 · `concurrent_open_vacancies_count`

- **Definición:** número de vacantes de la misma organización publicadas y no cerradas en `checkpoint_at`, excluyendo la propia.
- **Fuente:** **[HECHO]** reconstruible con `vacancies.published_at`, `closed_at` y `organization_id` (`…000006…:14, 27, 29`).
- **[LIMITACIÓN]** Usa `organization_id` para **agrupar**, jamás como señal: el identificador no entra en `X`.
- **Leakage:** se reconstruye al checkpoint, no con el estado actual de la tabla.
- **Decisión:** **incluir**. Captura carga organizacional, que es la hipótesis operacional más defendible.

---

## 2. Features evaluadas y excluidas en v1

| ID | Candidata | Motivo de exclusión |
|---|---|---|
| ML-FEAT-X01 | `current_process_stage` | **[HECHO]** No existe etapa de vacante: `VacancyStatus` es `borrador`/`publicada`/`cerrada` (`app/Enums/VacancyStatus.php:11-13`). Inferir una etapa "actual" agregando estados de postulaciones sería una construcción ad hoc y ambigua |
| ML-FEAT-X02 | porcentaje de etapas completadas | Compuesto ambiguo y potencialmente tautológico; los contadores atómicos ML-FEAT-08 a 15 son más interpretables y auditables |
| ML-FEAT-X03 | cantidad de finalistas | Deriva de resultados sobre personas (`ApplicationStatus::Finalist`) y desviaría la explicación hacia los candidatos. Solo reconsiderable con justificación ética explícita |
| ML-FEAT-X04 | responsables involucrados | **[HECHO]** Se construiría con `evaluator_id`/`scheduled_by` (`…000009…:16-17`), convirtiendo el modelo en una evaluación indirecta de trabajadores. Excluida |
| ML-FEAT-X05 | reprogramaciones o cancelaciones | **[HECHO]** No disponible: A-22 declara fuera del MVP la cancelación y la reprogramación de sesiones (`docs/assumptions.md:28`) |
| ML-FEAT-X06 | `progress_score` u otro compuesto | Puede ocultar fuga y duplica las variables que lo construyen |
| ML-FEAT-X07 | área, cargo, ubicación, tipo de contrato, texto libre | Campos nominales sin derivación operacional reproducible; riesgo de fabricar señal y de actuar como proxy socioeconómico |

---

## 3. Variables prohibidas

**Ninguna de estas puede entrar en `X`, en el dataset model-ready, en la API ni en la explicación.** La prohibición es absoluta y no admite excepción por utilidad predictiva.

**Identidad y datos personales:** nombre, apellidos, DNI, correo, teléfono, dirección, fotografía.

**Atributos demográficos y sensibles:** edad, fecha de nacimiento, sexo, género, nacionalidad, estado civil, raza, etnia, religión, orientación sexual, salud, discapacidad, ideología política, afiliación sindical, biometría.

**Proxies:** universidad o centro de estudios, nivel educativo del candidato, ubicación de residencia, cualquier indicador socioeconómico.

**Contenido:** CV, texto del CV, embeddings, cartas, `evaluations.observations`, `interviews.observations`, `evaluation_results.comment`, `interview_results.comment`, `job_requests.justification`, `selection_decisions.justification`.

**Resultados sobre personas:** `evaluation_results.score`, `interview_results.score`, `interviews.outcome`, ranking, posición, puntaje ponderado, desempates, completitud del ranking, `selection_decisions.selected_score`, `selected_position`, `ranked_candidates`.

**Decisión:** `selection_decisions.*` en su totalidad, identidad del seleccionado, `selected_application_id`, `decided_by`, `decided_at`.

**Identificadores:** `candidate_id`, `user_id`, `evaluator_id`, `scheduled_by`, `changed_by`, `vacancy_id`, `organization_id`, `job_request_id` y cualquier ID secuencial que permita memorizar entidades.

**Futuro respecto del checkpoint:** `vacancies.closed_at`, `closed_by`, `closure_type`, `closure_notes`, `status` final, duración total real, cualquier evento, conteo, resultado o registro de auditoría posterior al checkpoint, y cualquier transformación que revele el target.

**Cualquier señal que convierta el análisis del flujo en una evaluación de personas.**

---

## 4. Resumen

| Conjunto | Cantidad | Estado |
|---|---|---|
| Núcleo (ML-FEAT-01, 03, 04, 05, 06, 08, 09, 11, 12, 13, 15, 16, 17, 18) | 14 | **[APROBADA]** |
| Dependiente de `GAP-01` (ML-FEAT-02) | 1 | **[APROBADA]** para el dataset sintético; no computable en Laravel |
| Derivadas con advertencia de colinealidad (ML-FEAT-10, 14) | 2 | **[APROBADA]** en el dataset, fuera de `X` en modelos lineales |
| Ablation candidate (ML-FEAT-07) | 1 | **[APROBADA]** como ablation |
| Excluidas documentadas (ML-FEAT-X01…X07) | 7 | **[APROBADA]** su exclusión |

**[APROBADA]** El contrato queda aprobado como baseline de trabajo (decisión 9). **[LIMITACIÓN]** De las 15 features utilizables, **14 son computables hoy en Laravel y una no lo es**: `ML-FEAT-02` requiere `GAP-01`.

## Enlaces

- [Definición del problema](problem-definition.md)
- [Especificación del dataset](dataset-specification.md)
- [Ética y supervisión humana](ethics-and-human-oversight.md)
- [Índice de la Fase 14](../phase-14-ml-definition.md)
