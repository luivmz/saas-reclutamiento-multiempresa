# Definición del problema de ML operacional

**Fase 14 · 20 de septiembre de 2026 · rama `feature/phase-14-ml-definition`**

Este documento define *qué* se va a predecir, *sobre qué unidad*, *en qué instante* y *contra qué verdad*. Nada de lo aquí descrito está implementado.

## Taxonomía usada

| Marca | Significado |
|---|---|
| **[HECHO]** | Verificado en código, esquema, prueba o Git, con cita `ruta:línea` |
| **[APROBADA]** | Decisión explícita del equipo, con fecha registrada |
| **[PROPUESTA]** | Diseño recomendado, aún sin aprobación del equipo |
| **[PENDIENTE]** | Requiere decisión explícita del equipo o del dueño del dominio |
| **[LIMITACIÓN]** | Restricción de datos, validez, arquitectura o alcance |

> **Decisiones del equipo del 20 de septiembre de 2026.** El problema, la unidad, el checkpoint y la definición conceptual del target quedaron **aprobados**. `ML-DECISION-01` quedó **resuelta** en los términos de la sección 4.2. El registro completo de las doce decisiones está en [`phase-14-ml-definition.md` §4](../phase-14-ml-definition.md).

---

## 1. Alternativas comparadas

| # | Alternativa | Claridad del target | Riesgo principal | Utilidad operacional | Veredicto |
|---|---|---|---|---|---|
| A | **Clasificación binaria de retraso** | Alta: un umbral y una comparación de fechas | Depende por completo de que exista un plazo objetivo con semántica aprobada | Alta: permite avisar antes de que el plazo venza | **Recomendada**, condicionada |
| B | Regresión de duración restante | Baja: exige una duración "verdadera" y sufre censura en procesos no cerrados | Falsa precisión — con datos sintéticos un MAE en días se leería como una capacidad real que no existe | Media | **Descartada** para v1 |
| C | Panel descriptivo sin predicción | No aplica: no hay target | Ninguno relevante | Media, pero honesta y segura | **Fallback obligatorio** si A no supera su compuerta |
| D | Riesgo de atasco por etapa | Baja en este dominio | **[HECHO]** El dominio no modela una etapa única de vacante: `VacancyStatus` solo tiene `borrador`, `publicada` y `cerrada` (`app/Enums/VacancyStatus.php:11-13`); las etapas pertenecen a cada postulación (`app/Enums/ApplicationStatus.php:25-32`) | Alta si existiera la entidad | **Diferida** a una fase futura |

### Por qué A y no B

Con un dataset sintético, una regresión produciría un error medio en días que parecería una medición del proceso real del Colegio Andino. No lo sería. La clasificación binaria permite hablar de *probabilidad calibrada de un evento operacional definido*, que es una afirmación mucho más defendible y evaluable. B además arrastra censura: los procesos aún abiertos no tienen duración observada, y rellenarla introduciría sesgo.

### Por qué C sigue vivo

**[APROBADA]** C sigue siendo el **fallback obligatorio**. Si el experimento no supera su compuerta —no bate al baseline, presenta fuga no resoluble, descalibración grave o resultados artificialmente fáciles—, **no se presentará como predictor válido** y el trabajo se reorienta al panel descriptivo (RF-28 candidato). Esa degradación es un resultado válido, no un fracaso: un panel que muestra tiempos y cuellos de botella reales vale más que un predictor sin verdad definida.

---

## 2. Problema recomendado

**[APROBADA] `ML-PROBLEM-01`** *(decisión 1 del equipo, 20/09/2026)* — Clasificación binaria supervisada del riesgo operacional de que un proceso de selección **cierre después de su plazo operacional objetivo**, estimada en un checkpoint fijo, entrenada y evaluada exclusivamente sobre datos sintéticos, con fines académicos y sin validez institucional. **La unidad es siempre una vacante/proceso, nunca una persona.**

El modelo analiza **el proceso**, nunca a las personas. No puntúa, ordena, recomienda ni descarta postulantes, no alimenta el ranking de RF-20 a RF-22 y no interviene en la decisión de RF-23 a RF-25.

---

## 3. Unidad de análisis y checkpoint

### 3.1 Unidad

**[APROBADA] `ML-UNIT-01`** *(decisión 2, 20/09/2026)* — Una observación es **un snapshot único de una vacante elegible en un checkpoint operacional definido**. Máximo una fila por `vacancy_id` en la primera versión.

No es un candidato, ni una postulación, ni una entrevista, ni una fila por persona. `vacancy_id`, `organization_id`, `checkpoint_at` y la versión del dataset se conservan **como metadatos de linaje**, fuera de la matriz `X`.

### 3.2 Checkpoint

**[APROBADA] `ML-CHECKPOINT-01`** *(decisión 2, 20/09/2026)*

```
checkpoint_at = inicio del día inmediatamente posterior a vacancies.closes_at,
                en zona America/Lima
```

**[HECHO]** Esta definición es reproducible sin ambigüedad porque `vacancies.closes_at` es una columna `date`, no un timestamp (`database/migrations/2026_09_13_000006_create_vacancies_table.php:23`, casteada en `app/Models/Vacancy.php:58`). No hay hora que normalizar: el checkpoint es el comienzo del día siguiente a esa fecha.

**[HECHO]** `closes_at` es el cierre de **postulaciones**, no del proceso: su etiqueta en el formulario es literalmente «cierre de postulaciones» (`app/Http/Requests/Vacancies/VacancyFormRequest.php:91`) y la aceptación de postulaciones se corta con `closes_at >= hoy` (`app/Models/Vacancy.php:78`).

#### Comparación con alternativas de checkpoint

| Alternativa | Problema |
|---|---|
| 25 % o 50 % del plazo | Circular: usa el plazo objetivo para definir el instante en que se predice contra ese mismo plazo |
| N días tras la publicación | Arbitrario, y puede caer antes o después del cierre de postulaciones según la vacante |
| Checkpoints periódicos | Genera varias filas por vacante, correlación intra-proceso y riesgo de fuga entre particiones. Posible en una v2 con agrupación por `vacancy_id` |
| Entrada a etapa | **[HECHO]** No existe una etapa de vacante que disparar (`app/Enums/VacancyStatus.php:11-13`) |
| **Cierre de postulaciones (recomendado)** | Es un evento de negocio real, único, fechado y anterior al desenlace |

### 3.3 Elegibilidad

**[PROPUESTA]** Una vacante genera observación solo si, al checkpoint:

1. está publicada y `published_at` es conocido — **[HECHO]** se escribe al publicar (`app/Services/Vacancies/VacancyService.php:104`);
2. `closes_at` no es nulo — **[HECHO]** la columna es nullable (`…000006…:23`);
3. no estaba cerrada todavía (`closed_at` nulo o posterior al checkpoint);
4. el plazo objetivo estaba fijado en o antes de la publicación y no cambió después;
5. `target_completion_at > checkpoint_at`, para que sea una predicción y no una alerta de mora ya consumada;
6. existe un `closed_at` observable dentro de la ventana de seguimiento, necesario para construir la etiqueta.

**[LIMITACIÓN]** Los procesos aún abiertos al final de la ventana observacional están **censurados**. No se les asigna etiqueta arbitraria: se excluyen del primer experimento. La exclusión sesga la muestra hacia procesos que sí terminaron, y ese sesgo debe declararse en toda conclusión.

---

## 4. Target y la decisión pendiente que lo condiciona

### 4.1 Definición conceptual

**[APROBADA] `ML-TARGET-01`** *(decisión 3, 20/09/2026 — aprobación **conceptual**)*

```
target_completion_at = fecha/hora objetivo máxima para completar el proceso de selección,
                       conocida e inmutable antes del checkpoint
actual_completion_at = vacancies.closed_at

delayed = 1  si actual_completion_at >  target_completion_at
delayed = 0  si actual_completion_at <= target_completion_at
```

**[HECHO]** `vacancies.closed_at` es un `timestamp` nullable (`…000006…:29`) y se escribe una sola vez, al cerrar realmente la convocatoria (`app/Services/Selection/VacancyClosureService.php:71`).

**[PROPUESTA]** Normalización temporal: si el plazo es una fecha sin hora, `target_completion_at` es el **final de ese día en `America/Lima`** (23:59:59.999999), convertido a UTC solo para intercambio entre servicios. Nunca se comparan fechas locales contra instantes UTC sin convertir.

### 4.2 `ML-DECISION-01` — resuelta el 20 de septiembre de 2026

**[APROBADA]** El equipo decidió:

1. **`job_requests.required_by` NO se reinterpreta** como `target_completion_at`. Conserva su significado histórico y actual; RF-01 no se modifica.
2. **Se aprueba conceptualmente la necesidad** de un plazo operacional explícito, `target_completion_at`, que represente de forma inequívoca la fecha/hora objetivo máxima para completar el proceso de selección.
3. **No se implementa en la Fase 14:** sin campo, sin migración, sin RF nuevo, sin cambios en Laravel. La brecha queda registrada como **`GAP-01`** en [`requirements-and-traceability-plan.md` §3](requirements-and-traceability-plan.md) y se resuelve en la fase de integración.
4. **El dataset sintético de la Fase 15 modela `target_completion_at` como variable operacional explícita**, generada antes de la publicación e inmutable. Eso permite ejecutar el experimento sin esperar a la integración.

**[LIMITACIÓN]** La consecuencia es una separación real entre ciencia e integración: el modelo podrá entrenarse y evaluarse, pero **no podrá conectarse a Laravel hasta que `GAP-01` se resuelva**, porque hoy el sistema no registra ese plazo en ninguna parte. Es el precio de no forzar una equivalencia no demostrada, y se asume conscientemente.

#### Lo verificado sobre `required_by`

Se conserva como evidencia del análisis que condujo a la decisión:

| Aspecto | Evidencia |
|---|---|
| Existe y es `date` nullable | `database/migrations/2026_09_13_000005_create_job_requests_table.php:22` |
| Se valida como fecha futura al registrar el requerimiento | `app/Http/Requests/JobRequests/JobRequestFormRequest.php:33` — `['nullable','date','after_or_equal:today']` |
| Se rotula «fecha requerida» | `app/Http/Requests/JobRequests/JobRequestFormRequest.php:48` y `resources/js/pages/job-requests/show.tsx:293` |
| Se captura antes de la validación y de la aprobación | Es campo del formulario del requerimiento (`app/Models/JobRequest.php:40`) |

**[LIMITACIÓN]** Nada en el código, en las pruebas ni en `docs/assumptions.md` demuestra que «fecha requerida» signifique «fecha límite para cerrar el proceso de selección». Podría significar la fecha en que se necesita a la persona incorporada, que no es lo mismo. Ese fue el motivo del rechazo: **el equipo optó por la salida 2 de las tres que estaban sobre la mesa** (definir un plazo explícito) en lugar de reinterpretar un campo existente.

**[APROBADA]** Restricciones que siguen vigentes sobre el target:

- **No** se usa `vacancies.closes_at` como target: solo cierra postulaciones.
- **No** se fabrica el plazo con una fórmula derivada de las mismas features: produciría un target tautológico.
- El plazo debe estar fijado **antes de la publicación** y no cambiar después, también en el generador sintético.

---

## 5. Riesgos de fuga de información identificados

| # | Riesgo | Mitigación especificada |
|---|---|---|
| L1 | Usar `closed_at`, `closure_type`, duración total o estado final como feature | Prohibidos explícitamente en `feature-contract.md` §3 |
| L2 | Contar eventos posteriores al checkpoint | Toda feature lleva la regla `timestamp <= checkpoint_at` en su definición |
| L3 | **Censura estructural**: **[HECHO]** una vacante solo puede cerrarse después de registrar decisión y selección humana (`VacancyClosureService.php:44-46`), y A-30 documenta que el cierre desierto no se implementa. Un proceso atascado **nunca** produce `closed_at` | Se excluyen los censurados y se declara el sesgo; se documenta como limitación de validez |
| L4 | Plazo objetivo modificado después del checkpoint | Elegibilidad exige plazo inmutable fijado antes de publicar |
| L5 | Features compuestas que reconstruyen el target | `progress_score` y el porcentaje de etapas completadas quedan excluidos |
| L6 | Identificadores memorizables (`vacancy_id`, `organization_id`, IDs secuenciales) | Solo metadatos de linaje, nunca columnas de `X` |
| L7 | Generador sintético que hace la etiqueta casi determinista | El diseño *event-first* de `dataset-specification.md` §2 y la revisión de exactitud sospechosa |

---

## 6. Qué queda fuera, explícitamente

**[LIMITACIÓN]** El modelo no estima idoneidad, desempeño, permanencia, personalidad ni ajuste cultural de ninguna persona. No usa ni aproxima atributos sensibles. Los detalles y la lista completa de variables prohibidas están en `ethics-and-human-oversight.md` y `feature-contract.md` §3.

---

## Enlaces

- [Contrato de features](feature-contract.md)
- [Especificación del dataset sintético](dataset-specification.md)
- [Plan de evaluación](evaluation-plan.md)
- [Ética y supervisión humana](ethics-and-human-oversight.md)
- [ADR-004](../architecture-decisions/ADR-004-ml-problem-definition.md)
- [Índice de la Fase 14](../phase-14-ml-definition.md)
