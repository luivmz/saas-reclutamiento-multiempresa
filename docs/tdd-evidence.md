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

Los 8 skipped corresponden a pruebas del starter kit para funciones de Fortify desactivadas (verificación de correo, etc.).
