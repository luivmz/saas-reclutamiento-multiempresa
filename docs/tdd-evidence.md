# Evidencia de TDD (RED → GREEN → REFACTOR)

Solo se registran ejecuciones reales de `php artisan test` realizadas dentro del contenedor `app` (PostgreSQL `reclutamiento_testing`). Las salidas de las fases 2–4 se observaron en la terminal durante el desarrollo; no se guardaron como archivos.

## Fase 2 — Tenancy, roles y auditoría base

| Paso | Pruebas | Resultado real |
|---|---|---|
| RED | `OrganizationScopeTest`, `AuditLoggerTest`, `RoleMiddlewareTest`, `CandidateRegistrationTest` (14) | 14 fallidas: `Class "App\Models\Organization" not found`, `Class "App\Enums\UserRole" not found`, `Class "App\Models\AuditLog" not found` |
| GREEN (1.er intento) | Suite completa | 1 fallida: la prueba de inmutabilidad asignaba un valor inválido al enum (`ValueError`); era un error de la prueba, se corrigió |
| GREEN | `tests/Feature/Tenancy/OrganizationScopeTest.php`, `tests/Feature/Audit`, `tests/Feature/Auth` | 31 passed, 8 skipped |

## Fase 3 — RF-01 a RF-07

| Paso | Pruebas | Resultado real |
|---|---|---|
| RED | `JobRequestStatusTest`, `WeightingValidatorTest`, `JobRequestWorkflowTest`, `VacancyPublicationTest`, `CrossTenantAccessTest` | Fallidas: `Class "App\Enums\JobRequestStatus" not found`, `Class "App\Services\Evaluation\WeightingValidator" not found`, `Class "App\Models\JobRequest" not found` |
| GREEN (intermedio) | Mismas pruebas | 6 fallidas → corrección de 2 errores de prueba, `withoutVite()` y DEF-03 → 47 passed, 3 fallidas por páginas Inertia inexistentes |
| GREEN | Suite completa tras crear las páginas | 91 passed, 8 skipped |

## Fase 4 — RF-08 a RF-15

| Paso | Pruebas | Resultado real |
|---|---|---|
| RED | `ApplicationStatusTest`, `CandidateProfileTest`, `ApplyToVacancyTest`, `ApplicationReviewTest` | Fallidas: `Class "App\Enums\ApplicationStatus" not found`, `Route [candidate.profile.update] not defined` |
| GREEN (intermedio) | Suite completa | 128 passed, 1 fallida (`Property [application.id] does not exist`) → DEF-05 |
| GREEN | Suite completa | 129 passed, 8 skipped |

## Fase 5 — RF-16 a RF-19

| Paso | Pruebas | Resultado real |
|---|---|---|
| RED (checkpoint `3e66623`, re-ejecutado al retomar) | `tests/Unit/Assessments` (5) + `tests/Feature/Assessments` (18) | **23 failed (0 assertions)**: `Class "App\Services\Assessments\ScoreSheetValidator" not found`, `RouteNotFoundException` |
| GREEN unitario | `tests/Unit/Assessments/ScoreSheetValidatorTest.php` | **5 passed (8 assertions)** |
| GREEN feature (1.er intento) | Unit + Feature de Fase 5 | Proceso PHP terminado prematuramente en `test_assigned_evaluator_records_evaluation_scores` → DEF-06 |
| GREEN feature (2.º intento) | Unit + Feature de Fase 5 | 22 passed, 1 failed: `ModelNotFoundException` en `InterviewTest::test_evaluator_of_another_organization_cannot_access_the_interview` — la prueba construía el payload después de autenticar al evaluador de otra organización (error de la prueba, no del código); se construye antes |
| GREEN | Unit + Feature de Fase 5 | **23 passed (99 assertions)** |
| REFACTOR | Reglas de etapas centralizadas en `AssessmentScheduler::acceptsEvaluation/acceptsInterview`; resumen de sesión compartido en `AssessmentSessionPresenter`; UI de programación y convocatorias | Fase 5: **23 passed (99 assertions)** |
| Regresión | `tests/Feature/Tenancy`, `RoleMiddlewareTest`, `tests/Feature/Applications`, `tests/Feature/Candidates` | **35 passed (146 assertions)** |
| Suite completa | `php artisan test` | **152 passed, 8 skipped, 0 failed (532 assertions)** |

## Fase 6 — RF-20 a RF-25

Pruebas nuevas de la fase: **51** (`RankingServiceTest` 14, `RankingComparisonTest` 8, `FinalDecisionTest` 10, `SelectionRegistrationTest` 7, `VacancyClosureTest` 5, 6 casos nuevos en `ApplicationStatusTest` y 1 en `CrossTenantAccessTest`).

| Bloque | Paso | Pruebas | Resultado real |
|---|---|---|---|
| A + B (RF-20, RF-21) | RED | `tests/Unit/Ranking/RankingServiceTest.php` (14) | Fallidas: `Class "App\Services\Ranking\RankingService" not found`, `Class "App\Services\Ranking\CandidateScores" not found` |
| A (RF-20) | RED | `CrossTenantAccessTest::test_rf20_hr_of_other_organization_cannot_modify_vacancy_criteria` | 1 failed: la respuesta sí era 404, pero la prueba leía los criterios con el usuario de la organización B autenticado (el scope de tenant devolvía vacío). Error de diseño de la prueba; se corrigió para leer sin scope |
| A + B | GREEN | `tests/Unit/Ranking` + prueba cross-tenant | **14 passed (32 assertions)** y **1 passed (3 assertions)** |
| C (RF-21, RF-22) | RED | `tests/Feature/Selection/RankingComparisonTest.php` | **8 failed (0 assertions)**: `Route [vacancies.comparison] not defined` |
| C | GREEN | `tests/Unit/Ranking` + `RankingComparisonTest` | **22 passed (113 assertions)** |
| C | REFACTOR | `EvaluationCriterion::definitionsFor()` con etapa opcional (sin duplicar consultas); limpieza de una asignación sobrante en `RankingPresenter` | Sin cambios de resultado |
| D (RF-23) | RED | `tests/Feature/Selection/FinalDecisionTest.php` | **10 failed (0 assertions)** |
| D | GREEN | `FinalDecisionTest` + `RankingComparisonTest` | **18 passed (123 assertions)** |
| E (RF-24) | RED | `tests/Feature/Selection/SelectionRegistrationTest.php` | **7 failed (7 assertions)**: `Route [vacancies.selection.store] not defined` (las 7 aserciones corresponden al registro previo de la decisión, que ya funcionaba) |
| E | GREEN | `SelectionRegistrationTest` + regresión `ApplicationReviewTest` | **17 passed (95 assertions)** |
| F (RF-25) | RED | `VacancyClosureTest` + `ApplicationStatusTest` | **9 failed, 17 passed (29 assertions)**: `Route [vacancies.close] not defined` (5) y 4 transiciones hacia `no_seleccionado` no permitidas |
| F | GREEN | `tests/Unit/Ranking`, `tests/Unit/Enums`, `tests/Feature/Selection` | **78 passed (273 assertions)** |
| Regresión | — | `tests/Feature/Tenancy`, `RoleMiddlewareTest`, `tests/Feature/Applications`, `tests/Feature/Assessments`, `tests/Feature/Vacancies` | **57 passed (268 assertions)** |
| Suite completa | — | `php artisan test` | **211 pruebas: 203 passed, 8 skipped, 0 failed (779 assertions)** |

Evidencia específica de que el ranking no selecciona: `RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate` calcula el ranking (servicio y dos vistas) y verifica que no cambian estados, historiales, decisiones ni auditoría de selección; `FinalDecisionTest::test_rf23_approver_records_the_final_decision_for_a_ranked_finalist` verifica que incluso la decisión humana no cambia el estado hasta RF-24.

## Fase 7 — RF-26 y RF-27

Pruebas nuevas de la fase: **19** (`ProcessResultNotificationTest` 8, `AuditTrailTest` 5, `AuditLogViewTest` 6).

| Bloque | Paso | Pruebas | Resultado real |
|---|---|---|---|
| A + B + C (RF-26) | RED | `tests/Feature/Notifications/ProcessResultNotificationTest.php` | **6 failed, 2 passed (37 assertions)**: no se enviaba ninguna notificación de resultado y `Undefined constant App\Enums\AuditAction::ProcessResultNotified`. Las 2 que pasaron (`no_final_result_is_sent_before_the_vacancy_is_closed`, `only_candidates_of_the_closed_vacancy_are_notified`) solo contienen aserciones negativas y pasaban porque aún no se notificaba nada; se conservan como guardas de regresión |
| D + E + F (RF-27) | RED | `tests/Feature/Audit/AuditTrailTest.php`, `tests/Feature/Audit/AuditLogViewTest.php` | **10 failed, 1 passed**: `Undefined constant …ProcessResultNotified`; `DB::table('audit_logs')->update()/delete()` no lanzaba excepción (DEF-07); `cookie`/`authorization`/`api_key` se almacenaban (DEF-08); no existía ruta de consulta; `Route [audit.index] not defined` (6). Pasó `deleting_a_user_keeps_the_audit_record_without_the_actor_reference` (comportamiento previo de la FK `nullOnDelete`) |
| Todos | GREEN (1.er intento) | Notificaciones + auditoría + `VacancyClosureTest` | **2 failed, 26 passed (246 assertions)**, ambos errores de diseño de las pruebas nuevas: (1) el patrón `/justificaci/` coincidía con una observación legítima de RR. HH. («Precisar la justificación.»); se reemplazó por el texto exacto de la justificación de la decisión; (2) `assertSame` sobre metadatos `jsonb` fallaba por el orden de claves que reordena PostgreSQL; se usa `assertEquals` más `assertArrayNotHasKey` por cada clave sensible |
| Todos | GREEN | `ProcessResultNotificationTest`, `AuditTrailTest`, `AuditLogViewTest` | **19 passed (238 assertions)** |
| Regresión | — | Pruebas que usan notificaciones (`tests/Feature/Notifications`, `JobRequests`, `Applications`, `Assessments`) | **53 passed (300 assertions)** |
| Regresión | — | `tests/Feature/Audit` (incluye `AuditLoggerTest`) | **15 passed (184 assertions)** |
| Regresión | — | Pruebas cross-tenant (`--filter` por organización ajena/foránea en toda la suite) | **16 passed (65 assertions)** |
| Suite completa | — | `php artisan test` | **230 pruebas: 222 passed, 8 skipped, 0 failed (1017 assertions)** |

Los 8 skipped corresponden a pruebas del starter kit para funciones de Fortify desactivadas (verificación de correo, etc.).

## Fase 8 — Frontend integral

Los defectos se detectaron en la validación en navegador (`docs/manual-smoke-test.md`). En cada uno: reproducción en capturas, prueba en RED, corrección y GREEN.

Pruebas nuevas de la fase: **3**.

| Defecto | Paso | Pruebas | Resultado real |
|---|---|---|---|
| DEF-09, DEF-10 | RED | `tests/Feature/Frontend/AppTimezoneTest.php` (primera versión, que verificaba una prop compartida `timezone`), `AuditLogViewTest::test_rf27_details_show_readable_labels_and_local_dates_instead_of_raw_values` | **3 failed (22 assertions)**: `Property [timezone] does not exist` (2); el detalle de auditoría devolvía `enviado`, `validado`, `con_seleccion`, `clase_modelo` y la fecha ISO en UTC |
| DEF-09 | Rediseño | `AppTimezoneTest` | La zona horaria se expone con `<meta name="app-timezone">` en la vista raíz, en lugar de una prop de Inertia. Así `lib/format.ts` la lee al cargar el módulo, antes del primer render. La prueba se ajustó a ese contrato y siguió en RED hasta agregar la etiqueta. |
| DEF-09, DEF-10 | GREEN | `AppTimezoneTest`, `AuditLogViewTest` | **9 passed (103 assertions)** |
| DEF-11 | — | Sin prueba automatizada (no hay Vitest en el alcance) | Verificado en las capturas posteriores: «EÑ», «RH», «JS», «LP» |
| Regresión | — | `php artisan test` | **233 pruebas: 225 passed, 8 skipped, 0 failed (1045 assertions)** |
| Build | — | `npm run build`, `npx tsc --noEmit` | OK, 0 errores |
| Navegador | — | Recorrido visual por rol / flujo integral | **10/10 (49 capturas) / 12/12** |

## Entrega académica (07/11/2026) — datos demo de ML-01 (DEF-18)

Rama local `feature/entrega-academica-demo`, desde `2f6d0e0`. Solo cambia los datos de demostración; el contrato de RF-29 no cambia.

| Defecto | Paso | Pruebas | Resultado real |
|---|---|---|---|
| DEF-18 | RED | `tests/Feature/Ml/DemoSeederOperationalRiskScenarioTest.php`, antes de cambiar `DemoSeeder` | **2 failed, 1 passed (9 assertions)**: `ModelNotFoundException`, porque no existía ninguna vacante del escenario. La guardia de identificadores de Cypress ya pasaba |
| DEF-18 | GREEN | Ídem, con el escenario al final de `DemoSeeder` | **3 passed (19 assertions)** |
| Regresión | — | `php artisan test`, `npm run build`, `npx tsc --noEmit`, Cypress y `pytest` de `ml-service` | Resultados en [`docs/entrega-final/informe-final.md`](entrega-final/informe-final.md) |

## Continuación (08/11/2026) — cronograma del proceso y prototipos de F37 y F38

Rama local `feature/continuacion-f36-f40`, desde `f5003c9`. El cambio de producto es solo de interfaz: no toca el backend, las migraciones ni los contratos de RF-21, RF-23 y RF-29.

| Cambio | Paso | Pruebas | Resultado real |
|---|---|---|---|
| Cronograma del proceso (`ProcessSchedule`) | RED | `resources/js/components/vacancies/process-schedule.test.tsx`, escrita antes del componente | **1 archivo fallido, 0 pruebas**: `Failed to resolve import "@/components/vacancies/process-schedule"` |
| Ídem | GREEN | Ídem, con el componente y `toCalendarDate`/`calendarToday` en `lib/format.ts` | **11 passed** |
| Plazo sin fecha en un proceso cerrado | RED | Dos pruebas nuevas en el mismo archivo, antes del arreglo | **2 failed, 10 passed**: el plazo sin fecha quedaba marcado como hito en curso, también con la vacante cerrada |
| Ídem | GREEN | Ídem, sin considerar en curso un plazo sin fecha | **12 passed** |
| Regresión de componentes | — | `npx vp test --run` | **7 archivos, 54 passed** |
| Tipos y build | — | `npx tsc --noEmit`, `npm run build` | 0 errores; build correcto |
| Cypress dirigido | — | E2E-20 (12 tests, 5 nuevos del cronograma) y los specs que visitan el detalle de la vacante | Resultados en [`entrega-final/informe-continuacion.md`](entrega-final/informe-continuacion.md) |
| Prototipo de F37 (fuera del SaaS) | — | `docs/academico/preparacion-f37-evidencias/prototipo/test_f37_flujo_evidencias.py` | **19 passed**. No fue TDD: las pruebas se escribieron junto al prototipo. Se verificaron con 6 ablaciones; las 6 fallan. La sexta sobrevivía al principio y obligó a añadir una prueba |
| Arnés de F38 (fuera del SaaS) | — | `docs/academico/preparacion-f38-ml02/evaluacion/test_f38_evaluar.py` | **17 passed**, con los valores de la salida degradada calculados a mano antes de ejecutar. 5 ablaciones; las 5 fallan |

### Revisión del candidato `a9fa344` (09/11/2026)

| Cambio | Paso | Pruebas | Resultado real |
|---|---|---|---|
| Cronograma: plazo no posterior a la publicación y proceso cerrado sin fecha de cierre | RED | Dos pruebas nuevas en `process-schedule.test.tsx`, contra el componente de `a9fa344` | **2 failed, 12 passed**: decía «Sin plazo objetivo» con un plazo registrado y marcaba vencido un proceso cerrado. El arreglo se escribió antes de ejecutarlas; el RED se observó restaurando temporalmente el componente de `a9fa344` |
| Ídem | GREEN | Ídem, con el arreglo | **14 passed**; regresión de componentes **56 passed** |
| Prototipo de F37: R-05 en toda escritura y con camelCase; una sola fuente por tipo | RED | Dos pruebas nuevas | **2 failed** de 21 |
| Ídem | GREEN | Ídem, y 5 escenarios nuevos | **21 passed**; 38/38 escenarios |
| Arnés de F38: semilla, catálogo de tareas, camelCase, valores numéricos, forma de la salida, particiones y `k` en el sello | RED | Ocho pruebas nuevas | **6 failed, 1 error** de 25. La octava, que fija el sello publicado, pasaba: es una guarda |
| Ídem | GREEN | Ídem, con el sello nuevo `fb7e7e13…` | **25 passed** |

### Hallazgos MEDIUM de la auditoría de Codex sobre `138ce29` (09/11/2026)

Las pruebas de regresión se escribieron primero y se ejecutaron contra el código de `138ce29` antes de corregirlo.

| Hallazgo | Paso | Pruebas | Resultado real |
|---|---|---|---|
| CONT-M01 · F37: RR. HH. corregía la observación ajena `EVD-S1-0002` declarando `type='cv'` y `source='documento_presentado'` | RED | `test_rrhh_no_corrige_una_observacion_ajena_aunque_declare_otro_tipo` y `test_el_autor_sigue_corrigiendo_su_observacion` | **1 failed** de 23 (`True is not false : permitido`); la corrección del autor ya pasaba |
| Ídem | GREEN | Ídem: la corrección se autoriza por el tipo y el autor de la evidencia original, antes de los datos de reemplazo | **23 passed**; 38/38 escenarios. La solicitud se deniega, no se crea ningún registro y `EVD-S1-0002` sigue `registrada` |
| CONT-M02 · F38: una raíz JSON `[]`, `null`, cadena o número lanzaba `AttributeError` | RED | `test_una_raiz_que_no_es_objeto_se_rechaza_por_el_punto_de_entrada`, por `main` | **1 error**: `AttributeError: 'list' object has no attribute 'get'` |
| CONT-M03 · F38: `['FRG-004', 'FRG-004', 'FRG-004']` en APP-ML-001 / CRI-01-CLASE pasaba como válida | RED | `test_ids_repetidos_en_una_lista_de_recuperacion_invalidan` y `test_las_metricas_de_recuperacion_validas_quedan_en_cero_uno` | **1 failed** (`True is not false`). Medido antes de corregir: `valid = true`, Recall@3 = 1,667 y nDCG@3 = 1,377 en `dev` |
| CONT-M02 y CONT-M03 | GREEN | Ídem: la raíz se valida antes de `.get()` y una lista de recuperación con IDs repetidos se rechaza antes de calcular métricas | **28 passed**. Sello, semilla, `k` y conjunto sin cambios (`fb7e7e13…`) |

## Práctica individual — Módulo de reportes (RF-28 candidato, 09/11/2026)

Ejecución histórica en el working tree de `chore/sonarqube-macos-setup`, sin commit y pendiente de auditoría. Las pruebas se escribieron antes que la ruta, el Form Request, la Policy, el servicio y la página.

Pruebas nuevas: **12** PHPUnit (`tests/Feature/Reports/RecruitmentReportTest.php`), **6** Vitest (`resources/js/lib/reports.test.tsx`) y **9** Cypress (`cypress/e2e/e2e-20-reports.cy.js`).

| Requisito | Paso | Pruebas | Resultado real |
|---|---|---|---|
| RF-28 (cand.) | Ajuste previo | `RecruitmentReportTest` | Antes de la primera ejecución se corrigió una expectativa de la propia prueba: una postulación `en_evaluacion` sin historial sí alcanzó la preselección (4, no 3) |
| RF-28 (cand.) | RED | `RecruitmentReportTest` | **12 failed (0 assertions)**: `Route [reports.index] not defined` |
| RF-28 (cand.) | Implementación backend | `RecruitmentReportTest` | **8 passed, 4 failed**: la prueba esperaba `75.0` y el JSON serializa los valores enteros como `75`. Se ajustó la expectativa de la prueba; la lógica no cambió |
| RF-28 (cand.) | GREEN (backend) | `RecruitmentReportTest` | **11 passed, 1 failed**: faltaba la página `reports/index` |
| RF-28 (cand.) | GREEN | `RecruitmentReportTest` | **12 passed (209 assertions)** |
| RF-28 (cand.) | GREEN | `reports.test.tsx` (Vitest) | **6 passed** |
| RF-28 (cand.) | E2E | `e2e-20-reports.cy.js` | **9 passed** |
| Regresión | — | `php artisan test` | **434 pruebas: 426 passed, 8 skipped, 0 failed (1715 assertions)** |
| Regresión | — | `npx vp test --run`, `npm run build`, `npx tsc --noEmit` | 54/54; build OK; 0 errores |
| Regresión E2E | — | `npm run cy:run` | Ejecución 1: **87/94** (DEF-20 y DEF-21, registrados originalmente como DEF-14 y DEF-15 en la práctica) → ejecución 2: **94/94** |

## Incremento visual de la presentación (`design/presentacion-higgsfield`, 22/11/2026)

Cada RED se ejecutó contra el código anterior a su corrección; los resultados GREEN, contra `446b8fe`.

| Cambio | Paso | Pruebas | Resultado real |
|---|---|---|---|
| VIS-L01 · movimiento reducido activado con la portada abierta | RED | E2E-22, regresión nueva con `getComputedStyle`, contra el `Reveal` y el CSS de `main` | **1 failed**: «opacidad: expected '0' to equal '1'» |
| Ídem | Ablación | Ídem, con solo la defensa CSS y el JS de `main` | **1 failed** (línea 244): los bloques siguen en estado oculto |
| Ídem | GREEN | Ídem, con `watchReveal` y la defensa CSS | **8 passed** en E2E-22; unitarias de `watchReveal` en verde |
| DEF-19 · lote `[fuera, dentro]` de IntersectionObserver | RED | Prueba unitaria nueva de `watchReveal` y pruebas de `lib/intersection.ts` | **1 failed** (seguía oculto) y el módulo aún no existía |
| Ídem | GREEN | Ídem, con `someIntersecting` y `latestIntersecting` | **83 passed** (11 archivos); E2E-22 **5 de 5** ejecuciones seguidas |
| Vídeo y carpeta del proceso | — | `hero-folder-video.test.tsx` (progreso, fotogramas, búsquedas sin solaparse, nada pedido antes de decidir) y pruebas de la carpeta en `reveal.test.tsx`; E2E-23 | Escritas junto al componente, no antes: no es TDD. E2E-23 **10/10** |

La primera versión de la regresión de VIS-L01 cambiaba la preferencia fuera de la cola de Cypress; sus dos ejecuciones se conservan como inválidas en las evidencias, y la prueba vigente encola los cambios.
