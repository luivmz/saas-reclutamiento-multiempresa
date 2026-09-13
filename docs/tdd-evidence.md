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

Los 8 skipped corresponden a pruebas del starter kit para funciones de Fortify desactivadas (verificación de correo, etc.).
