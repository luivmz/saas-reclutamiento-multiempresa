# Fase 14 — Definición formal del experimento de ML operacional

**Fecha:** 20 de septiembre de 2026
**Rama:** `feature/phase-14-ml-definition`, creada desde `develop` en `95c5b8b`
**Naturaleza:** exclusivamente documental. **No se implementó ML, servicio, dataset, modelo ni integración.**

Índice ejecutivo de la fase. El detalle vive en los documentos enlazados; aquí está lo que hay que saber para decidir.

---

## 1. Objetivo

Fijar, antes de escribir una línea de código, el problema, la unidad de análisis, el checkpoint, el target, las features, el dataset, la partición, las métricas, los límites éticos y la compuerta de entrada a la Fase 15 — de modo que una fase posterior no pueda improvisar ninguna de esas decisiones.

## 2. Evidencia inspeccionada

**[HECHO]** Verificado en esta sesión contra el código, no contra la memoria:

| Área | Evidencia |
|---|---|
| Esquema del dominio | Migraciones de `job_requests`, `vacancies`, `applications`, `evaluations`, `interviews`, `selection_decisions` y auditoría |
| Máquinas de estado | `app/Enums/VacancyStatus.php`, `app/Enums/ApplicationStatus.php` |
| Servicios | `VacancyService`, `VacancyClosureService` |
| Validación | `JobRequestFormRequest`, `VacancyFormRequest` |
| Reglas de negocio | `docs/assumptions.md` (A-22, A-30, A-31, A-32) |
| Requerimientos | `docs/rf-implementation-matrix.md` (RF-01 a RF-27) |
| Gobierno | `CLAUDE.md`, `docs/v1.1/*`, ADR-001 a ADR-003, skills del proyecto |

### Hechos que condicionan el diseño

1. `vacancies.closes_at` y `opens_at` son columnas **`date`** nullable (`…000006…:22-23`); `closes_at` se rotula «cierre de postulaciones» (`VacancyFormRequest.php:91`). El checkpoint queda definido sin ambigüedad horaria.
2. `vacancies.closed_at` es un `timestamp` escrito una sola vez al cerrar (`VacancyClosureService.php:71`).
3. `job_requests.required_by` es `date` nullable, validado `after_or_equal:today` y rotulado «fecha requerida». **No hay evidencia de que signifique plazo de cierre del proceso.**
4. `VacancyStatus` solo tiene `borrador`, `publicada`, `cerrada`: **no existe una etapa de vacante**.
5. `evaluation_criteria.stage` admite solo dos valores por `CHECK` (`…000006…:72`), así que `configured_stage_count` ∈ {0,1,2}.
6. A-22 excluye del MVP cancelar y reprogramar sesiones: las reprogramaciones **no** son una feature disponible.
7. Una vacante solo se cierra tras decisión y selección humanas; A-30 documenta que el cierre desierto no se usa. **Los procesos atascados nunca producen `closed_at`.**

## 3. Divergencias respecto del baseline del prompt

Registradas porque la evidencia prevalece sobre la instrucción factual:

| Divergencia | Observado |
|---|---|
| El prompt anticipaba `PROMPT_FASE_13_CLAUDE_CODE.md` sin rastrear, con SHA-256 `BE4F08…` | **El archivo ya no existe en el repositorio.** El árbol estaba limpio al iniciar la fase; el preflight pasó sin bloqueo. No fue eliminado por esta sesión |
| El prompt describía `closes_at` sin precisar el tipo | Es `date`, no `timestamp`: refuerza la reproducibilidad del checkpoint |
| El prompt sugería `configured_stage_count` como ablation | Se mantiene como ablation, documentando que su cardinalidad máxima es 3 |

**Evolución del estado, sin reescribir el pasado:** `CLAUDE.md` afirma que `main` y `develop` tienen el mismo contenido; tras integrar la Fase 13 solo en `develop` ya no es literalmente cierto. `docs/v1.1/phase-13-master-plan.md` registra permisos locales amplios como hallazgo histórico; hoy `.claude/settings.local.json` usa 21 reglas de lectura, 41 en `ask` y 19 en `deny`. **Ninguno de los dos documentos se modificó**; ambas evoluciones quedan anotadas aquí y en `documentation-update-map.md`.

## 4. Decisiones del equipo — 20 de septiembre de 2026

Doce decisiones formalizadas. Este es el registro de referencia; los documentos temáticos las citan por número.

| # | Decisión | Resultado |
|---|---|---|
| 1 | **Problema ML** | **APROBADA.** Clasificación binaria del riesgo operacional de retraso. La unidad es siempre una vacante/proceso, nunca una persona |
| 2 | **Unidad y checkpoint** | **APROBADA.** Snapshot único por vacante elegible; checkpoint = inicio del día posterior a `closes_at`, `America/Lima` |
| 3 | **Target** | **APROBADA conceptualmente.** `delayed` según `closed_at` vs `target_completion_at`. **Rechazado** reinterpretar `job_requests.required_by`. Se aprueba la **necesidad** de un plazo operacional explícito; su implementación es `GAP-01` |
| 4 | **Dataset** | **APROBADA.** Sintético, 6 000 observaciones (rango 5 000–10 000), ≥36 meses, varias organizaciones ficticias, seed `20260920`, *event-first*, target no determinista, datos exclusivamente ficticios |
| 5 | **Split** | **APROBADA.** 70/15/15 con orden temporal por `checkpoint_at` |
| 6 | **Modelos** | **APROBADA.** Dummy/prevalencia, baseline operacional, Logistic Regression (primer modelo), Decision Tree y Random Forest. HistGradientBoosting opcional y condicionado. Sin deep learning, LLM, AutoML ni redes neuronales |
| 7 | **Métrica** | **APROBADA.** Average Precision primaria; recall, precision, F1, F2 cuando corresponda, balanced accuracy, ROC-AUC, matriz de confusión, Brier/BSS y curva de calibración como secundarias |
| 8 | **Umbrales** | **APROBADA la política, sin cifras.** Selección solo con validation, orientación a recall, control de precision, congelado antes de test, test nunca para escoger. Valores concretos: Fase 15, documentados |
| 9 | **Features** | **APROBADA** como baseline de trabajo, con las cinco categorías intactas y la prohibición absoluta de variables personales |
| 10 | **Censura** | **APROBADA como limitación permanente.** Los procesos sin `closed_at` no se etiquetan arbitrariamente; la Fase 15 debe **evaluar su impacto** |
| 11 | **RF** | **APROBADA.** RF-28 candidato descriptivo; RF-29 candidato condicionado; RF-30 y RF-31 fuera del alcance ML. **Ninguno pasa al baseline v1.1** |
| 12 | **NO-GO** | **APROBADA.** Se mantienen todos los criterios. Si el experimento falla, no se presenta como predictor válido y el fallback es el enfoque descriptivo |

### Estado resultante de los identificadores

| ID | Estado |
|---|---|
| `ML-PROBLEM-01`, `ML-UNIT-01`, `ML-CHECKPOINT-01`, `ML-ETHICS-01` | **APROBADA** |
| `ML-TARGET-01` | **APROBADA conceptualmente**; no implementable hasta `GAP-01` |
| `ML-DECISION-01` | **RESUELTA** — ver decisión 3 |
| `ML-SPLIT-01`, `ML-BASE-01/02`, `ML-MODEL-01` | **APROBADA** |
| `ML-FEAT-01…18`, `ML-FEAT-X01…X07` | **APROBADA** como contrato baseline |
| `GAP-01` | **Decisión de diseño aprobada, implementación abierta** |
| ADR-004 | **ACEPTADA** |

Alternativas descartadas: regresión de duración restante (falsa precisión y censura) y riesgo de atasco por etapa (el dominio no modela la etapa). El panel descriptivo **no** se descarta: es el fallback obligatorio.

## 5. Pendientes restantes

| # | Pendiente | Bloquea |
|---|---|---|
| 1 | **`GAP-01`** — implementar el plazo operacional explícito en Laravel: dónde vive, quién lo fija, cuándo, obligatoriedad, inmutabilidad y qué RF lo cubre | **La integración**, no el experimento |
| 2 | **Valores concretos de precision y recall** para `t_high` y `t_medium` | Nada: se determinan experimentalmente en la Fase 15 y se documentan |
| 3 | **Autorización separada** para crear código Python e instalar dependencias | **El inicio de la Fase 15** |
| 4 | **Disposición final de RF-28 y RF-29** como requerimientos del baseline v1.1 | La planificación funcional, no el experimento |
| 5 | **Entregables y fechas** de la próxima evaluación del curso | La priorización general |

## 6. Artefactos de esta fase

| Documento | Contenido |
|---|---|
| [`ml/problem-definition.md`](ml/problem-definition.md) | Alternativas, problema, unidad, checkpoint, target, riesgos de fuga |
| [`ml/feature-contract.md`](ml/feature-contract.md) | 18 features con definición completa, 7 excluidas, lista de prohibidas |
| [`ml/dataset-specification.md`](ml/dataset-specification.md) | Escala, generación *event-first*, distribuciones, validaciones |
| [`ml/evaluation-plan.md`](ml/evaluation-plan.md) | Split, baselines, modelos, métricas, calibración, aceptación y no-go |
| [`ml/ethics-and-human-oversight.md`](ml/ethics-and-human-oversight.md) | Frontera ética, supervisión humana, rotulado, privacidad |
| [`ml/model-card-draft.md`](ml/model-card-draft.md) | Borrador con todo resultado como `PENDIENTE DE MEDICIÓN` |
| [`ml/api-contract-draft.md`](ml/api-contract-draft.md) | Contrato conceptual `POST /v1/predict`, errores y fallback |
| [`ml/requirements-and-traceability-plan.md`](ml/requirements-and-traceability-plan.md) | RF-28 a RF-31, RNF, brecha `GAP-01`, esquema de trazabilidad |
| [`architecture-decisions/ADR-004-ml-problem-definition.md`](architecture-decisions/ADR-004-ml-problem-definition.md) | Decisión duradera, en estado **aceptada** |

Actualizados para enlazar la especificación: [`ml-feasibility.md`](ml-feasibility.md), [`scope-preliminary.md`](scope-preliminary.md), [`documentation-update-map.md`](documentation-update-map.md).

## 7. Validaciones

**[HECHO]** Ejecutadas: preflight Git completo, `git diff --check`, comparación del diff contra la allowlist, verificación de enlaces relativos, comprobación de cada ruta citada, revisión de que RF-01 a RF-27 no cambiaron y de que no se tocó documentación histórica.

**No ejecutado en esta sesión: cambio exclusivamente documental, sin código ni dependencias.** No se corrió `php artisan test`, Cypress, `npm run build` ni `tsc`. Los resultados de v1.0 (244 pruebas PHPUnit, 43 pruebas Cypress) siguen siendo los últimos registrados y **no** se reejecutaron.

## 8. Las dos compuertas

La decisión 3 separó lo que antes era una sola compuerta. **Conviene no confundirlas: la primera está abierta, la segunda no.**

### 8.1 Gate científico — iniciar el experimento en Python

| # | Condición | Estado |
|---|---|---|
| 1 | El equipo aprueba explorar **clasificación binaria** y no otra alternativa | ✅ Decisión 1 |
| 2 | Existe una **definición inequívoca del target**, aunque su fuente sea el dataset sintético | ✅ Decisión 3 |
| 3 | **Unidad y checkpoint** aprobados | ✅ Decisión 2 |
| 4 | **Contrato de features** aprobado, sin variables personales | ✅ Decisión 9 |
| 5 | **Estrategia de dataset**, seed y versionado aprobados | ✅ Decisión 4 |
| 6 | **Split, baselines, métrica primaria, política de umbrales y no-go** aprobados | ✅ Decisiones 5, 6, 7, 8, 12 |
| 7 | Se acepta que **los datos sintéticos no validan uso real** | ✅ Decisión 4 |
| 8 | **RF-29 permanece candidato experimental**; no se asume aprobado | ✅ Decisión 11 |
| 9 | Sin bloqueadores críticos de seguridad, ética, fuga o trazabilidad | ✅ Verificado en esta fase |
| 10 | Fase 14 revisada y árbol limpio | ✅ Revisión favorable del equipo |
| 11 | **Autorización separada** para crear código Python e instalar dependencias | ⛔ **PENDIENTE** |

**Estado: 10 de 11 condiciones cumplidas.** La única que falta es la autorización explícita para escribir código Python e instalar dependencias, que por gobierno del proyecto debe concederse por separado y no se deduce de las decisiones anteriores.

### 8.2 Gate de integración Laravel — conectar el modelo al producto

| # | Condición | Estado |
|---|---|---|
| 1 | **`GAP-01` resuelta**: existe un plazo operacional explícito en el sistema | ⛔ **BLOQUEANTE** |
| 2 | El experimento superó los 12 criterios de aceptación | ⛔ No ejecutado |
| 3 | Umbrales determinados y congelados, con sus cifras documentadas | ⛔ Fase 15 |
| 4 | Contrato de API cerrado y seguridad servicio-a-servicio definida | ⛔ Fase de integración |
| 5 | Fallback implementado y probado con `Http::fake()` | ⛔ Fase de integración |
| 6 | RF-29 aprobado formalmente como requerimiento de v1.1 | ⛔ Decisión 11 lo mantiene candidato |

**Estado: bloqueado.** **[LIMITACIÓN]** Aunque el experimento de la Fase 15 tenga éxito, el modelo **no será desplegable** mientras `GAP-01` siga abierta: `ML-FEAT-02` no es computable en Laravel, de modo que el vector del contrato de API no puede ensamblarse. Es una consecuencia deliberada de no reinterpretar `required_by`, y el equipo la asumió conscientemente.

**Si el experimento falla** (no supera el baseline, fuga no resoluble, descalibración grave o resultados artificialmente fáciles), se aplica la decisión 12: no se presenta como predictor válido y el fallback es el panel descriptivo de RF-28.

## 9. Contratos preservados

RF-01 a RF-27 conservan número, significado y condición de línea base. El sistema sigue sin seleccionar, descartar ni contratar automáticamente. La decisión final sigue siendo humana. Laravel sigue siendo el sistema de registro. `v1.0.0-academic` (`9a946c2`) permanece intacto y la historia publicada no se reescribió.
