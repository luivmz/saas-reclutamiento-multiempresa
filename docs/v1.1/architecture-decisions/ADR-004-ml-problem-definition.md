# ADR-004 — Definición del problema de ML operacional

- **Estado:** **ACEPTADA** — aprobada por el equipo el 20 de septiembre de 2026 (decisiones 1, 2, 3 y 12 de la Fase 14).
- **Fecha:** 20 de septiembre de 2026
- **Contexto:** Fase 14, definición formal del experimento de v1.1
- **Alcance de la aceptación:** aprueba el **problema, la unidad, el checkpoint, la definición conceptual del target y el fallback descriptivo**. **No** autoriza implementación en Laravel: la materialización de `target_completion_at` queda condicionada a `GAP-01`.

## Contexto

v1.1 explora incorporar machine learning operacional. ADR-001 ya fijó *qué ámbito* es admisible —el proceso, nunca las personas— y ADR-002 ratificó que la decisión final es humana. Falta la decisión de ingeniería: **qué problema concreto se formula, sobre qué unidad, en qué instante y contra qué verdad**, de modo que una fase posterior no pueda improvisarlo.

El proyecto no dispone de datos reales y no debe obtenerlos, así que cualquier experimento será sobre datos sintéticos. Eso condiciona qué tipo de afirmación es honesta al final.

## Decisión

### 1. Problema

Clasificación binaria supervisada del **riesgo de que un proceso de selección cierre después de su plazo operacional objetivo**, como prototipo académico con datos sintéticos.

### 2. Unidad de análisis

Un snapshot único de una vacante elegible. Máximo una observación por `vacancy_id`. No es un candidato, ni una postulación, ni una entrevista. Los identificadores son metadatos de linaje, nunca features.

### 3. Checkpoint

`checkpoint_at` = inicio del día inmediatamente posterior a `vacancies.closes_at`, en `America/Lima`. Es un evento de negocio real, único y fechado, y `closes_at` es una columna `date`, lo que hace la definición reproducible sin ambigüedad horaria.

### 4. Target

`delayed = 1` si `vacancies.closed_at > target_completion_at`, `0` en caso contrario. El plazo debe ser conocido e inmutable antes del checkpoint.

### 5. Fallback descriptivo

Si la semántica del plazo objetivo no se aprueba, se emite **NO-GO predictivo** y el trabajo se reorienta al panel descriptivo (RF-28 candidato). Esa degradación es un resultado válido del proyecto, no un fracaso.

## Alternativas consideradas

1. **Regresión de duración restante.** Rechazada para v1: con datos sintéticos, un error medio en días se leería como una capacidad real que no existe, y la censura de los procesos no cerrados obligaría a rellenar valores con sesgo.
2. **Panel descriptivo sin predicción.** No rechazada: es el fallback obligatorio y sigue siendo la opción por defecto si falla la compuerta.
3. **Riesgo de atasco por etapa.** Diferida: el dominio no modela una etapa única de vacante — `VacancyStatus` solo tiene `borrador`, `publicada` y `cerrada` (`app/Enums/VacancyStatus.php:11-13`) — y obligaría a otra unidad de análisis.
4. **Clasificación binaria (elegida).** Permite expresar probabilidad y calibración, evita evaluar personas, es demostrable metodológicamente con datos sintéticos, cabe en Logistic Regression / Decision Tree / Random Forest y ofrece una regla de no-go clara.

No se eligió por sofisticación, sino porque es la afirmación más pequeña que sigue siendo útil.

## Resolución de `ML-DECISION-01`

La condición que mantenía este ADR en estado propuesto quedó resuelta el 20 de septiembre de 2026.

**Lo verificado.** El único campo actual parecido a un plazo es `job_requests.required_by`: `date` nullable (`database/migrations/2026_09_13_000005_create_job_requests_table.php:22`), validado como fecha futura al registrar el requerimiento (`app/Http/Requests/JobRequests/JobRequestFormRequest.php:33`) y rotulado «fecha requerida» (`:48`). El repositorio **no** demuestra que signifique la fecha límite para cerrar el proceso de selección.

**Lo decidido.**

1. **Se rechaza** reinterpretar `job_requests.required_by` como `target_completion_at`. El campo **conserva su significado histórico y actual**, y RF-01 no se modifica ni se reinterpreta.
2. **Se aprueba conceptualmente la necesidad** de un plazo operacional explícito, `target_completion_at`, que represente de forma inequívoca la fecha/hora objetivo máxima para completar el proceso de selección.
3. **Su implementación queda fuera de esta fase.** No se crea campo, migración, requisito ni código. La brecha se registra como **`GAP-01`** y se resuelve en la fase de integración correspondiente.
4. **El dataset sintético de la Fase 15 modela `target_completion_at` como variable operacional explícita**, lo que permite ejecutar el experimento científico sin esperar a la integración en Laravel.

**Consecuencia sobre los gates.** La aprobación separa dos compuertas que antes estaban fundidas: el **gate científico**, que ya puede abrirse porque el dataset sintético provee el plazo, y el **gate de integración Laravel**, que sigue bloqueado por `GAP-01`. Detalle en [`phase-14-ml-definition.md` §8](../phase-14-ml-definition.md).

## Consecuencias

**Positivas.** El problema, la unidad, el instante y la verdad quedan fijados antes de escribir una línea de código, de modo que la Fase 15 no puede improvisarlos. La frontera ética de ADR-001 se mantiene intacta: el sujeto de la predicción es un flujo de trabajo. Existe una salida honesta y preparada si la premisa falla.

**Negativas.** El alcance es menos vistoso que un recomendador de candidatos, y con datos sintéticos las métricas demostrarán método, no eficacia. Ambas cosas se declaran abiertamente.

**Coste asumido conscientemente.** Al rechazar la reutilización de `required_by`, el experimento de la Fase 15 se ejecuta sobre un plazo que **solo existe en el dataset sintético**. Eso es metodológicamente correcto —evita un target tautológico construido sobre un campo cuyo significado nadie ha confirmado— pero implica que, aunque el modelo funcione, **no podrá integrarse en Laravel hasta resolver `GAP-01`**. El equipo acepta esa separación en lugar de forzar una equivalencia que no está demostrada.

**Limitación estructural detectada.** Una vacante solo puede cerrarse después de registrar la decisión final y la selección humanas (`app/Services/Selection/VacancyClosureService.php:44-46`), y A-30 documenta que el cierre desierto no se implementa. Un proceso atascado nunca produce `closed_at`, por lo que los procesos censurados se excluyen y la muestra queda sesgada hacia los que terminaron. Esta limitación debe acompañar a toda conclusión del experimento.

## Aplicación

[`problem-definition.md`](../ml/problem-definition.md) · [`feature-contract.md`](../ml/feature-contract.md) · [`evaluation-plan.md`](../ml/evaluation-plan.md) · skill `ml-risk-service`. Relacionada con [ADR-001](ADR-001-ml-boundary.md) y [ADR-002](ADR-002-human-oversight.md).
