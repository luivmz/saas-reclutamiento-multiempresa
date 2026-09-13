# Capítulo 11. Estrategia de pruebas

## 11.1 Enfoque general

Pirámide de pruebas con TDD en el backend y automatización E2E en la cima:

| Nivel | Herramienta | Cantidad real | Propósito |
|---|---|---|---|
| Unitarias | PHPUnit (`tests/Unit`) | 6 clases, 34 métodos, **62 casos** (con *data providers*), 85 aserciones | Reglas puras: máquinas de estado, ponderaciones, hojas de puntaje, ranking |
| *Feature* / integración | PHPUnit (`tests/Feature`) sobre PostgreSQL `reclutamiento_testing` | 33 clases, 182 métodos: **174 superadas + 8 omitidas**, 989 aserciones | Flujos HTTP completos: validación, Policies, servicios, base de datos, notificaciones, auditoría |
| E2E | Cypress 15.3.0 (`cypress/e2e`) | **14 specs, 43 tests** | Recorridos reales en navegador por rol, aislamiento multiempresa, casos negativos y flujo integral |
| Manual | Navegador (`docs/manual-smoke-test.md`) | Recorrido visual 10/10 (49 capturas) y flujo 12/12 | Validación visual y de experiencia (Fase 8) |
| Instalación / *smoke* | Docker (`docs/docker.md`) | Clon limpio: arranque, migraciones, *seed*, HTTP, PHPUnit y Cypress | Portabilidad (Fase 10) |

Las 8 pruebas omitidas pertenecen al *starter kit* de Laravel (funciones de Fortify desactivadas, como la verificación de correo; A-01). **La cobertura porcentual de código no se midió.**

## 11.2 TDD: RED → GREEN → REFACTOR

Cada bloque funcional se desarrolló así:

1. Escribir la prueba que expresa el RF o la regla.
2. Ejecutarla y **observar el fallo** (RED).
3. Implementar lo mínimo para que pase (GREEN).
4. Refactorizar manteniendo la suite en verde (REFACTOR).
5. Ejecutar la regresión completa.

Evidencia real por fase en `docs/tdd-evidence.md`. Ejemplos:

| Fase | RED | GREEN |
|---|---|---|
| 5 (RF-16 a RF-19) | Checkpoint `3e66623`: **23 failed** (clases y rutas inexistentes) | **23 passed (99 assertions)**; REFACTOR sin cambios de resultado |
| 6 (RF-23) | `FinalDecisionTest`: **10 failed** | **18 passed (123 assertions)** con `RankingComparisonTest` |
| 7 (RF-27) | 10 failed: la auditoría podía modificarse (DEF-07) y había claves sensibles almacenadas (DEF-08) | **19 passed (238 assertions)** |
| 10 (DEF-13) | 4 failed: el reset no verificaba la base activa | **11 passed (29 assertions)** |

Los errores de diseño de las propias pruebas (por ejemplo, aserciones autenticadas con el usuario de otra organización o regex demasiado amplias) también se registraron en `tdd-evidence.md`, sin maquillar resultados.

## 11.3 Pruebas unitarias

| Clase | Qué verifica |
|---|---|
| `Unit/Enums/JobRequestStatusTest`, `ApplicationStatusTest` | Transiciones permitidas y prohibidas de las máquinas de estado |
| `Unit/Evaluation/WeightingValidatorTest` | Suma de ponderaciones configurable, pesos y rangos inválidos |
| `Unit/Assessments/ScoreSheetValidatorTest` | Puntajes completos y dentro del rango de cada criterio |
| `Unit/Ranking/RankingServiceTest` (14) | Normalización ponderada, orden, influencia de los pesos, empates marcados, extremos 0/100, promedios, candidatos incompletos, determinismo y rechazo de entradas inválidas |

## 11.4 Pruebas *feature* e integración

Cubren los 27 RF con peticiones HTTP reales, Policies, Form Requests, servicios, base de datos PostgreSQL, notificaciones (`Notification::fake`/cola síncrona) y auditoría. 106 métodos se nombran `test_rfNN_*` para trazar la prueba al RF (ver [traceability-master.md](traceability-master.md)).

Pruebas clave de la regla crítica:
- `RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate`: calcular y consultar el ranking no cambia estados, historiales, decisiones ni auditoría.
- `FinalDecisionTest::test_rf23_approver_may_choose_a_candidate_who_is_not_first_in_the_ranking`.
- `FinalDecisionTest::test_rf23_explicit_human_confirmation_and_justification_are_required`.
- `FinalDecisionTest::test_rf23_only_the_approver_can_record_the_decision`.

## 11.5 Autorización

- `Auth/RoleMiddlewareTest`: acceso por rol a las rutas.
- Pruebas por RF del tipo «solo X puede…» o «otro rol no puede…» (`test_rf16_only_hr_can_schedule_evaluations`, `test_rf24_only_hr_can_register_the_selection`, `test_rf25_only_hr_can_close_the_vacancy`, `test_rf27_unauthorized_roles_cannot_view_the_audit_trail`, `test_rf09_staff_cannot_use_candidate_profile_routes`, etc.).
- `Testing/E2eSupportTest` y `E2eEnvironmentTest`: endpoints E2E inertes sin habilitación, en producción, sin token o fuera de la base E2E.

## 11.6 Aislamiento multiempresa (*cross-tenant*)

- `Tenancy/OrganizationScopeTest` (4): *scope* global por organización.
- `Tenancy/CrossTenantAccessTest` (7): acceso y modificación de recursos de otra organización rechazados.
- Pruebas por RF con organización ajena: `test_rf23_candidate_of_another_tenant_is_rejected`, `test_rf23_approver_of_another_organization_cannot_decide`, `test_rf24_hr_of_another_organization_cannot_register_the_selection`, `test_rf25_hr_of_another_organization_cannot_close_the_vacancy`, `test_rf21_application_of_another_tenant_is_never_ranked_even_if_linked_to_the_vacancy`, `test_rf26_closing_a_vacancy_of_another_organization_does_not_notify_this_organization_candidates`, `test_rf27_organization_never_sees_audit_logs_of_another_organization`.
- Regresión *cross-tenant* de la Fase 7: **16 passed (65 assertions)**.
- En E2E, `e2e-11-multitenancy` verifica listados, IDs ajenos y auditoría. La cobertura principal se mantiene en PHPUnit.

## 11.7 Regresión

Al cierre de cada fase se ejecutó la suite completa (`php artisan test`), `npm run build` y `npx tsc --noEmit`. La evolución real está en el [capítulo 8](08-desarrollo.md) y en el [capítulo 13](13-metricas-calidad.md).

## 11.8 E2E

- 14 specs y 43 tests en un entorno aislado.
- Reset protegido y datos ficticios reproducibles (`DemoSeeder`).
- Selectores `data-cy`, sin esperas arbitrarias ni reintentos automáticos.

Detalle en el [capítulo 12](12-automatizacion-pruebas.md).

## 11.9 Gestión de defectos

Procedimiento: reproducir → escribir una prueba que falle (cuando es automatizable) → corregir → registrar en `docs/defects.md`. Hay 13 defectos registrados y los 13 están cerrados (resumen en el [capítulo 13](13-metricas-calidad.md)).

## 11.10 Fuera del alcance de las pruebas

No se ejecutaron:
- pruebas de carga o rendimiento (k6);
- pruebas dinámicas de seguridad (OWASP ZAP);
- análisis estático (PHPStan/Larastan);
- pruebas unitarias de frontend (Vitest);
- auditoría automática de accesibilidad;
- medición de cobertura de código.

Quedan como recomendaciones ([capítulo 14](14-implementacion-monitoreo.md)).
