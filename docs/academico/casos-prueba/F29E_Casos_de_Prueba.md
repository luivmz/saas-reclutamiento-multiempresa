# F29E — Casos de prueba

> Generado por `docs/academico/tools/f27b/f29e.py` desde el código de pruebas, la matriz maestra y la evidencia de la F29F: `python docs/academico/tools/f27b/build.py f29e`. No se edita a mano.

## Resumen

| Suite | CP | Ejecuciones | Aprobadas | Fallidas | Omitidas |
|---|---|---|---|---|---|
| PHPUnit | 76 | 419 | 411 | 0 | 8 |
| Cypress | 20 | 85 | 85 | 0 | 0 |
| Vitest | 6 | 42 | 42 | 0 | 0 |
| pytest | 18 | 533 | 533 | 0 | 0 |
| Estática | 3 | 3 | 3 | 0 | 0 |
| CI | 1 | 1 | 1 | 0 | 0 |
| Manual | 4 | 0 | 0 | 0 | 0 |
| **Total** | **128** | 1083 | 1075 | 0 | 8 |

**Criterios del catálogo:**

- **Tipo:**
  - unitaria (`tests/Unit`);
  - integración / funcional (`tests/Feature` de negocio);
  - seguridad básica (autenticación, roles, soporte E2E, rutas);
  - multitenencia;
  - UI / E2E (Cypress);
  - UI / componentes (Vitest);
  - ML experimental (pytest, `tests/Feature/Ml` y E2E-14/15);
  - estática / build;
  - regresión / CI;
  - aceptación;
  - no funcional.
- **Prioridad:**
  - Alta: seguridad, multitenencia, CI o RF de decisión, cierre y auditoría (RF-03, RF-21 a RF-25 y RF-27).
  - Media: el resto de RF, las unitarias, el ML y la regresión.
  - Baja: componentes visuales y accesibilidad.
- **Automatización:** `AUTOMATIZADA` solo si existe la prueba en el repositorio. En otro caso, `MANUAL / NO AUTOMATIZADO`.
- **Estado:** sale de la ejecución F29F. Un caso manual sin ejecución queda `NO EJECUTADO`, con su razón.

## Catálogo

### CP-001 — Registrar requerimiento de personal

| Campo | Valor |
|---|---|
| RF relacionado | RF-01 |
| CU relacionado | CU-01 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar requerimiento de personal» con 2 prueba(s) automatizada(s) de `JobRequestWorkflowTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf01_requester_registers_a_job_request`: requester registers a job request<br>2. `test_rf01_required_fields_are_validated`: required fields are validated |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/JobRequests/JobRequestWorkflowTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=JobRequestWorkflowTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-002 — Reglas complementarias de JobRequestWorkflowTest (RF-01, RF-02, RF-03, RF-04)

| Campo | Valor |
|---|---|
| RF relacionado | RF-01, RF-02, RF-03, RF-04 |
| CU relacionado | CU-01, CU-02, CU-03 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de JobRequestWorkflowTest (RF-01, RF-02, RF-03, RF-04)» con 4 prueba(s) automatizada(s) de `JobRequestWorkflowTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_invalid_transition_is_rejected_and_state_is_kept`: invalid transition is rejected and state is kept<br>2. `test_submitted_request_cannot_be_edited`: submitted request cannot be edited<br>3. `test_roles_without_permission_are_forbidden`: roles without permission are forbidden<br>4. `test_requester_only_lists_own_requests_and_cannot_view_others`: requester only lists own requests and cannot view others |
| Resultado esperado | Las 4 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/JobRequests/JobRequestWorkflowTest.php (4 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=JobRequestWorkflowTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-003 — Validar y corregir requerimiento

| Campo | Valor |
|---|---|
| RF relacionado | RF-02 |
| CU relacionado | CU-02 |
| Referencia transversal | — |
| Objetivo | Verificar «Validar y corregir requerimiento» con 2 prueba(s) automatizada(s) de `JobRequestWorkflowTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf02_hr_observes_and_requester_corrects_and_resubmits`: hr observes and requester corrects and resubmits<br>2. `test_rf02_observation_requires_a_comment`: observation requires a comment |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/JobRequests/JobRequestWorkflowTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=JobRequestWorkflowTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-004 — Registrar aprobación o rechazo del requerimiento

| Campo | Valor |
|---|---|
| RF relacionado | RF-03 |
| CU relacionado | CU-03 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar aprobación o rechazo del requerimiento» con 1 prueba(s) automatizada(s) de `JobRequestWorkflowTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf03_hr_validates_and_approver_approves`: hr validates and approver approves |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/JobRequests/JobRequestWorkflowTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=JobRequestWorkflowTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-005 — Reglas complementarias de CrossTenantAccessTest (RF-03, RF-20)

| Campo | Valor |
|---|---|
| RF relacionado | RF-03, RF-20 |
| CU relacionado | CU-03, CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de CrossTenantAccessTest (RF-03, RF-20)» con 6 prueba(s) automatizada(s) de `CrossTenantAccessTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_hr_of_other_organization_cannot_view_or_review_job_requests`: hr of other organization cannot view or review job requests<br>2. `test_approver_of_other_organization_cannot_decide_job_requests`: approver of other organization cannot decide job requests<br>3. `test_job_request_listing_only_contains_own_organization`: job request listing only contains own organization<br>4. `test_hr_of_other_organization_cannot_view_edit_or_publish_vacancies`: hr of other organization cannot view edit or publish vacancies<br>5. `test_hr_of_other_organization_cannot_list_view_or_move_applications`: hr of other organization cannot list view or move applications<br>6. `test_hr_cannot_create_vacancy_from_another_organization_request`: hr cannot create vacancy from another organization request |
| Resultado esperado | Las 6 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Multitenencia |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Tenancy/CrossTenantAccessTest.php (6 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=CrossTenantAccessTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (6/6 aprobadas) |

### CP-006 — Notificar rechazo del requerimiento

| Campo | Valor |
|---|---|
| RF relacionado | RF-04 |
| CU relacionado | CU-03 |
| Referencia transversal | — |
| Objetivo | Verificar «Notificar rechazo del requerimiento» con 2 prueba(s) automatizada(s) de `JobRequestWorkflowTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf04_rejection_notifies_the_requester`: rejection notifies the requester<br>2. `test_rf04_rejection_requires_a_comment`: rejection requires a comment |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/JobRequests/JobRequestWorkflowTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=JobRequestWorkflowTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-007 — Registrar perfil y criterios del puesto / Configurar y validar vacante

| Campo | Valor |
|---|---|
| RF relacionado | RF-05, RF-06 |
| CU relacionado | CU-04, CU-05 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar perfil y criterios del puesto / Configurar y validar vacante» con 1 prueba(s) automatizada(s) de `VacancyPublicationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf05_rf06_hr_creates_vacancy_with_profile_and_criteria_from_approved_request`: hr creates vacancy with profile and criteria from approved request |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Vacancies/VacancyPublicationTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyPublicationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-008 — Registrar perfil y criterios del puesto

| Campo | Valor |
|---|---|
| RF relacionado | RF-05 |
| CU relacionado | CU-04 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar perfil y criterios del puesto» con 1 prueba(s) automatizada(s) de `VacancyPublicationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf05_vacancy_cannot_be_created_from_a_request_that_is_not_approved`: vacancy cannot be created from a request that is not approved |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Vacancies/VacancyPublicationTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyPublicationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-009 — Reglas complementarias de VacancyPublicationTest (RF-05, RF-06, RF-07)

| Campo | Valor |
|---|---|
| RF relacionado | RF-05, RF-06, RF-07 |
| CU relacionado | CU-04, CU-05, CU-06 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de VacancyPublicationTest (RF-05, RF-06, RF-07)» con 3 prueba(s) automatizada(s) de `VacancyPublicationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_draft_vacancies_are_not_public`: draft vacancies are not public<br>2. `test_published_vacancy_configuration_cannot_be_modified`: published vacancy configuration cannot be modified<br>3. `test_non_hr_roles_cannot_manage_vacancies`: non hr roles cannot manage vacancies |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Vacancies/VacancyPublicationTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyPublicationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-010 — Configurar y validar vacante

| Campo | Valor |
|---|---|
| RF relacionado | RF-06 |
| CU relacionado | CU-05 |
| Referencia transversal | — |
| Objetivo | Verificar «Configurar y validar vacante» con 1 prueba(s) automatizada(s) de `VacancyPublicationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf06_validation_report_lists_issues_of_an_invalid_vacancy`: validation report lists issues of an invalid vacancy |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Vacancies/VacancyPublicationTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyPublicationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-011 — Publicar vacante

| Campo | Valor |
|---|---|
| RF relacionado | RF-07 |
| CU relacionado | CU-06 |
| Referencia transversal | — |
| Objetivo | Verificar «Publicar vacante» con 3 prueba(s) automatizada(s) de `VacancyPublicationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf07_hr_publishes_a_valid_vacancy_and_it_becomes_public`: hr publishes a valid vacancy and it becomes public<br>2. `test_rf07_invalid_weights_prevent_publication`: invalid weights prevent publication<br>3. `test_rf07_vacancy_without_criteria_or_with_expired_deadline_cannot_be_published`: vacancy without criteria or with expired deadline cannot be published |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Vacancies/VacancyPublicationTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyPublicationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-012 — Reglas complementarias de AuthenticationTest (RF-08)

| Campo | Valor |
|---|---|
| RF relacionado | RF-08 |
| CU relacionado | CU-07 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de AuthenticationTest (RF-08)» con 6 prueba(s) automatizada(s) de `AuthenticationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_login_screen_can_be_rendered`: login screen can be rendered<br>2. `test_users_can_authenticate_using_the_login_screen`: users can authenticate using the login screen<br>3. `test_users_with_two_factor_enabled_are_redirected_to_two_factor_challenge`: users with two factor enabled are redirected to two factor challenge<br>4. `test_users_can_not_authenticate_with_invalid_password`: users can not authenticate with invalid password<br>5. `test_users_can_logout`: users can logout<br>6. `test_users_are_rate_limited`: users are rate limited |
| Resultado esperado | Las 6 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/AuthenticationTest.php (6 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=AuthenticationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (6/6 aprobadas) |

### CP-013 — Reglas complementarias de CandidateRegistrationTest (RF-08)

| Campo | Valor |
|---|---|
| RF relacionado | RF-08 |
| CU relacionado | CU-07 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de CandidateRegistrationTest (RF-08)» con 3 prueba(s) automatizada(s) de `CandidateRegistrationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_self_registration_creates_a_candidate_account_without_organization`: self registration creates a candidate account without organization<br>2. `test_self_registration_cannot_escalate_role_or_organization`: self registration cannot escalate role or organization<br>3. `test_registration_is_audited_without_password`: registration is audited without password |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/CandidateRegistrationTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=CandidateRegistrationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-014 — Reglas complementarias de CandidateProfileTest (RF-09)

| Campo | Valor |
|---|---|
| RF relacionado | RF-09 |
| CU relacionado | CU-08 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de CandidateProfileTest (RF-09)» con 1 prueba(s) automatizada(s) de `CandidateProfileTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_cv_download_is_restricted_to_owner_and_organizations_where_candidate_applied`: cv download is restricted to owner and organizations where candidate applied |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Candidates/CandidateProfileTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=CandidateProfileTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-015 — Gestionar perfil y CV del postulante

| Campo | Valor |
|---|---|
| RF relacionado | RF-09 |
| CU relacionado | CU-08 |
| Referencia transversal | — |
| Objetivo | Verificar «Gestionar perfil y CV del postulante» con 5 prueba(s) automatizada(s) de `CandidateProfileTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf09_candidate_updates_profile`: candidate updates profile<br>2. `test_rf09_profile_fields_are_validated`: profile fields are validated<br>3. `test_rf09_cv_is_stored_privately_with_a_safe_generated_name`: cv is stored privately with a safe generated name<br>4. `test_rf09_cv_rejects_invalid_type_and_oversized_files`: cv rejects invalid type and oversized files<br>5. `test_rf09_staff_cannot_use_candidate_profile_routes`: staff cannot use candidate profile routes |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Candidates/CandidateProfileTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=CandidateProfileTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-016 — Registrar postulación / Confirmar postulación al postulante

| Campo | Valor |
|---|---|
| RF relacionado | RF-10, RF-11 |
| CU relacionado | CU-09 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar postulación / Confirmar postulación al postulante» con 1 prueba(s) automatizada(s) de `ApplyToVacancyTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf10_rf11_candidate_applies_and_receives_confirmation`: candidate applies and receives confirmation |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplyToVacancyTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplyToVacancyTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-017 — Reglas complementarias de ApplyToVacancyTest (RF-10, RF-11)

| Campo | Valor |
|---|---|
| RF relacionado | RF-10, RF-11 |
| CU relacionado | CU-09 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de ApplyToVacancyTest (RF-10, RF-11)» con 1 prueba(s) automatizada(s) de `ApplyToVacancyTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_staff_users_cannot_apply`: staff users cannot apply |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplyToVacancyTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplyToVacancyTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-018 — Registrar postulación

| Campo | Valor |
|---|---|
| RF relacionado | RF-10 |
| CU relacionado | CU-09 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar postulación» con 4 prueba(s) automatizada(s) de `ApplyToVacancyTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf10_duplicate_application_is_rejected`: duplicate application is rejected<br>2. `test_rf10_cannot_apply_to_closed_or_expired_vacancy`: cannot apply to closed or expired vacancy<br>3. `test_rf10_draft_vacancy_is_not_available`: draft vacancy is not available<br>4. `test_rf10_incomplete_profile_or_missing_cv_blocks_application`: incomplete profile or missing cv blocks application |
| Resultado esperado | Las 4 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplyToVacancyTest.php (4 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplyToVacancyTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-019 — Consultar y revisar postulaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-12 |
| CU relacionado | CU-10 |
| Referencia transversal | — |
| Objetivo | Verificar «Consultar y revisar postulaciones» con 2 prueba(s) automatizada(s) de `ApplicationReviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf12_hr_lists_applications_of_a_vacancy`: hr lists applications of a vacancy<br>2. `test_rf12_hr_reviews_the_application_file`: hr reviews the application file |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplicationReviewTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplicationReviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-020 — Reglas complementarias de ApplicationReviewTest (RF-12, RF-13, RF-14, RF-15)

| Campo | Valor |
|---|---|
| RF relacionado | RF-12, RF-13, RF-14, RF-15 |
| CU relacionado | CU-10, CU-11, CU-12 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de ApplicationReviewTest (RF-12, RF-13, RF-14, RF-15)» con 3 prueba(s) automatizada(s) de `ApplicationReviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_stage_changes_are_blocked_when_the_vacancy_is_closed`: stage changes are blocked when the vacancy is closed<br>2. `test_only_hr_can_change_stages`: only hr can change stages<br>3. `test_candidate_only_sees_own_applications`: candidate only sees own applications |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplicationReviewTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplicationReviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-021 — Registrar preselección o descarte / Notificar cambio de etapa al candidato

| Campo | Valor |
|---|---|
| RF relacionado | RF-13, RF-15 |
| CU relacionado | CU-11, CU-12 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar preselección o descarte / Notificar cambio de etapa al candidato» con 1 prueba(s) automatizada(s) de `ApplicationReviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf13_rf15_hr_shortlists_and_the_candidate_is_notified`: hr shortlists and the candidate is notified |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplicationReviewTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplicationReviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-022 — Registrar preselección o descarte

| Campo | Valor |
|---|---|
| RF relacionado | RF-13 |
| CU relacionado | CU-11 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar preselección o descarte» con 1 prueba(s) automatizada(s) de `ApplicationReviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf13_discard_requires_a_reason`: discard requires a reason |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplicationReviewTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplicationReviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-023 — Gestionar cambio de etapa de la postulación

| Campo | Valor |
|---|---|
| RF relacionado | RF-14 |
| CU relacionado | CU-12 |
| Referencia transversal | — |
| Objetivo | Verificar «Gestionar cambio de etapa de la postulación» con 3 prueba(s) automatizada(s) de `ApplicationReviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf14_hr_moves_application_to_an_allowed_stage`: hr moves application to an allowed stage<br>2. `test_rf14_invalid_stage_transition_is_rejected`: invalid stage transition is rejected<br>3. `test_rf14_selection_outcomes_cannot_be_assigned_manually`: selection outcomes cannot be assigned manually |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Applications/ApplicationReviewTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplicationReviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-024 — Reglas complementarias de ApplicationStatusTest (RF-14, RF-25)

| Campo | Valor |
|---|---|
| RF relacionado | RF-14, RF-25 |
| CU relacionado | CU-12, CU-20 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de ApplicationStatusTest (RF-14, RF-25)» con 3 prueba(s) automatizada(s) de `ApplicationStatusTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_transition_rules`: transition rules<br>2. `test_selection_outcomes_are_not_manual_targets`: selection outcomes are not manual targets<br>3. `test_terminal_statuses`: terminal statuses |
| Resultado esperado | Las 21 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Unitaria |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/Enums/ApplicationStatusTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ApplicationStatusTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (21/21 aprobadas) |

### CP-025 — Programar evaluación / Generar convocatoria de evaluación

| Campo | Valor |
|---|---|
| RF relacionado | RF-16, RF-17 |
| CU relacionado | CU-13 |
| Referencia transversal | — |
| Objetivo | Verificar «Programar evaluación / Generar convocatoria de evaluación» con 1 prueba(s) automatizada(s) de `EvaluationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf16_rf17_hr_schedules_evaluation_and_convocation_is_sent`: hr schedules evaluation and convocation is sent |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/EvaluationTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=EvaluationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-026 — Programar evaluación

| Campo | Valor |
|---|---|
| RF relacionado | RF-16 |
| CU relacionado | CU-13 |
| Referencia transversal | — |
| Objetivo | Verificar «Programar evaluación» con 4 prueba(s) automatizada(s) de `EvaluationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf16_evaluator_must_be_an_evaluator_of_the_same_organization`: evaluator must be an evaluator of the same organization<br>2. `test_rf16_evaluation_cannot_be_scheduled_in_the_past`: evaluation cannot be scheduled in the past<br>3. `test_rf16_only_shortlisted_or_in_evaluation_applications_can_be_evaluated`: only shortlisted or in evaluation applications can be evaluated<br>4. `test_rf16_only_hr_can_schedule_evaluations`: only hr can schedule evaluations |
| Resultado esperado | Las 4 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/EvaluationTest.php (4 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=EvaluationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-027 — Reglas complementarias de EvaluationTest (RF-16, RF-17, RF-19, RF-20)

| Campo | Valor |
|---|---|
| RF relacionado | RF-16, RF-17, RF-19, RF-20 |
| CU relacionado | CU-13, CU-15, CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de EvaluationTest (RF-16, RF-17, RF-19, RF-20)» con 6 prueba(s) automatizada(s) de `EvaluationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_assigned_evaluator_records_evaluation_scores`: assigned evaluator records evaluation scores<br>2. `test_actors_of_another_organization_cannot_schedule_view_or_record_evaluations`: actors of another organization cannot schedule view or record evaluations<br>3. `test_only_the_assigned_evaluator_can_record_results`: only the assigned evaluator can record results<br>4. `test_results_cannot_be_recorded_twice`: results cannot be recorded twice<br>5. `test_evaluator_only_lists_and_views_own_assignments`: evaluator only lists and views own assignments<br>6. `test_assigned_evaluator_can_download_the_candidate_cv`: assigned evaluator can download the candidate cv |
| Resultado esperado | Las 6 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/EvaluationTest.php (6 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=EvaluationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (6/6 aprobadas) |

### CP-028 — Reglas complementarias de InterviewTest (RF-17, RF-18, RF-19, RF-20)

| Campo | Valor |
|---|---|
| RF relacionado | RF-17, RF-18, RF-19, RF-20 |
| CU relacionado | CU-13, CU-14, CU-15, CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de InterviewTest (RF-17, RF-18, RF-19, RF-20)» con 2 prueba(s) automatizada(s) de `InterviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_results_are_blocked_once_the_vacancy_is_closed`: results are blocked once the vacancy is closed<br>2. `test_evaluator_of_another_organization_cannot_access_the_interview`: evaluator of another organization cannot access the interview |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/InterviewTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=InterviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-029 — Programar entrevista

| Campo | Valor |
|---|---|
| RF relacionado | RF-18 |
| CU relacionado | CU-14 |
| Referencia transversal | — |
| Objetivo | Verificar «Programar entrevista» con 2 prueba(s) automatizada(s) de `InterviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf18_hr_schedules_interview_and_notifies_candidate_and_interviewer`: hr schedules interview and notifies candidate and interviewer<br>2. `test_rf18_submitted_application_cannot_be_interviewed`: submitted application cannot be interviewed |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/InterviewTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=InterviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-030 — Registrar entrevista y su resultado

| Campo | Valor |
|---|---|
| RF relacionado | RF-19 |
| CU relacionado | CU-15 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar entrevista y su resultado» con 2 prueba(s) automatizada(s) de `InterviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf19_assigned_evaluator_records_interview_and_result`: assigned evaluator records interview and result<br>2. `test_rf19_outcome_and_observations_are_required`: outcome and observations are required |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/InterviewTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=InterviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-031 — Validar rangos y ponderaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Validar rangos y ponderaciones» con 1 prueba(s) automatizada(s) de `EvaluationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf20_out_of_range_or_missing_scores_are_rejected`: out of range or missing scores are rejected |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/EvaluationTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=EvaluationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-032 — Validar rangos y ponderaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Validar rangos y ponderaciones» con 1 prueba(s) automatizada(s) de `InterviewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf20_interview_score_out_of_range_is_rejected`: interview score out of range is rejected |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Assessments/InterviewTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=InterviewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-033 — Validar rangos y ponderaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Validar rangos y ponderaciones» con 1 prueba(s) automatizada(s) de `RankingComparisonTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf20_invalid_weight_configuration_is_reported_instead_of_a_ranking`: invalid weight configuration is reported instead of a ranking |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/RankingComparisonTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingComparisonTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-034 — Validar rangos y ponderaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Validar rangos y ponderaciones» con 1 prueba(s) automatizada(s) de `CrossTenantAccessTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf20_hr_of_other_organization_cannot_modify_vacancy_criteria`: hr of other organization cannot modify vacancy criteria |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Multitenencia |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Tenancy/CrossTenantAccessTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=CrossTenantAccessTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-035 — Reglas complementarias de ScoreSheetValidatorTest (RF-20)

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de ScoreSheetValidatorTest (RF-20)» con 5 prueba(s) automatizada(s) de `ScoreSheetValidatorTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_complete_sheet_within_ranges_has_no_errors`: complete sheet within ranges has no errors<br>2. `test_boundary_values_are_accepted`: boundary values are accepted<br>3. `test_missing_scores_are_reported_per_criterion`: missing scores are reported per criterion<br>4. `test_scores_outside_the_range_are_reported`: scores outside the range are reported<br>5. `test_scores_for_unknown_criteria_are_rejected`: scores for unknown criteria are rejected |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Unitaria |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/Assessments/ScoreSheetValidatorTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ScoreSheetValidatorTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-036 — Reglas complementarias de WeightingValidatorTest (RF-20)

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de WeightingValidatorTest (RF-20)» con 8 prueba(s) automatizada(s) de `WeightingValidatorTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_valid_configuration_has_no_issues`: valid configuration has no issues<br>2. `test_empty_configuration_is_invalid`: empty configuration is invalid<br>3. `test_weight_must_be_greater_than_zero`: weight must be greater than zero<br>4. `test_score_range_must_be_consistent`: score range must be consistent<br>5. `test_criterion_names_must_be_unique_ignoring_case_and_spaces`: criterion names must be unique ignoring case and spaces<br>6. `test_weights_must_add_up_to_required_total_when_configured`: weights must add up to required total when configured<br>7. `test_total_comparison_tolerates_decimal_rounding`: total comparison tolerates decimal rounding<br>8. `test_total_rule_can_be_disabled_by_configuration`: total rule can be disabled by configuration |
| Resultado esperado | Las 8 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Unitaria |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/Evaluation/WeightingValidatorTest.php (8 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=WeightingValidatorTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (8/8 aprobadas) |

### CP-037 — Validar rangos y ponderaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-20 |
| CU relacionado | CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar «Validar rangos y ponderaciones» con 5 prueba(s) automatizada(s) de `RankingServiceTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf20_weights_need_not_add_up_to_100_when_the_rule_is_disabled`: weights need not add up to 100 when the rule is disabled<br>2. `test_rf20_invalid_weight_configuration_is_rejected`: invalid weight configuration is rejected<br>3. `test_rf20_score_outside_the_configured_range_is_rejected`: score outside the configured range is rejected<br>4. `test_rf20_scores_for_criteria_outside_the_vacancy_are_rejected`: scores for criteria outside the vacancy are rejected<br>5. `test_rf20_empty_criteria_are_rejected`: empty criteria are rejected |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Unitaria |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/Ranking/RankingServiceTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingServiceTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-038 — Calcular ranking configurable / Presentar comparación de candidatos

| Campo | Valor |
|---|---|
| RF relacionado | RF-21, RF-22 |
| CU relacionado | CU-17 |
| Referencia transversal | — |
| Objetivo | Verificar «Calcular ranking configurable / Presentar comparación de candidatos» con 1 prueba(s) automatizada(s) de `RankingComparisonTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf21_rf22_hr_views_the_comparison_ordered_by_weighted_total`: hr views the comparison ordered by weighted total |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/RankingComparisonTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingComparisonTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-039 — Calcular ranking configurable

| Campo | Valor |
|---|---|
| RF relacionado | RF-21 |
| CU relacionado | CU-17 |
| Referencia transversal | — |
| Objetivo | Verificar «Calcular ranking configurable» con 3 prueba(s) automatizada(s) de `RankingComparisonTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf21_discarded_and_other_vacancy_applications_are_not_ranked`: discarded and other vacancy applications are not ranked<br>2. `test_rf21_application_of_another_tenant_is_never_ranked_even_if_linked_to_the_vacancy`: application of another tenant is never ranked even if linked to the vacancy<br>3. `test_rf21_candidates_without_complete_results_are_listed_as_incomplete`: candidates without complete results are listed as incomplete |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/RankingComparisonTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingComparisonTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-040 — Calcular ranking configurable

| Campo | Valor |
|---|---|
| RF relacionado | RF-21 |
| CU relacionado | CU-17 |
| Referencia transversal | — |
| Objetivo | Verificar «Calcular ranking configurable» con 9 prueba(s) automatizada(s) de `RankingServiceTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf21_single_candidate_total_is_the_weighted_normalized_sum`: single candidate total is the weighted normalized sum<br>2. `test_rf21_candidates_are_ordered_by_total_descending`: candidates are ordered by total descending<br>3. `test_rf21_weights_change_the_order`: weights change the order<br>4. `test_rf21_ties_share_the_position_and_are_flagged_without_being_broken`: ties share the position and are flagged without being broken<br>5. `test_rf21_minimum_and_maximum_scores_produce_0_and_100`: minimum and maximum scores produce 0 and 100<br>6. `test_rf21_multiple_scores_for_a_criterion_are_averaged`: multiple scores for a criterion are averaged<br>7. `test_rf21_candidates_with_missing_criteria_are_reported_as_incomplete_and_not_ranked`: candidates with missing criteria are reported as incomplete and not ranked<br>8. `test_rf21_result_is_deterministic_regardless_of_input_order`: result is deterministic regardless of input order<br>9. `test_rf21_duplicate_applications_are_rejected`: duplicate applications are rejected |
| Resultado esperado | Las 9 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Unitaria |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/Ranking/RankingServiceTest.php (9 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingServiceTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (9/9 aprobadas) |

### CP-041 — Presentar comparación de candidatos

| Campo | Valor |
|---|---|
| RF relacionado | RF-22 |
| CU relacionado | CU-17 |
| Referencia transversal | — |
| Objetivo | Verificar «Presentar comparación de candidatos» con 2 prueba(s) automatizada(s) de `RankingComparisonTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf22_approver_can_view_the_comparison_but_other_roles_cannot`: approver can view the comparison but other roles cannot<br>2. `test_rf22_hr_of_other_organization_cannot_view_the_comparison`: hr of other organization cannot view the comparison |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/RankingComparisonTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingComparisonTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-042 — Registrar decisión final de selección

| Campo | Valor |
|---|---|
| RF relacionado | RF-23 |
| CU relacionado | CU-18 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar decisión final de selección» con 10 prueba(s) automatizada(s) de `FinalDecisionTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf23_approver_records_the_final_decision_for_a_ranked_finalist`: approver records the final decision for a ranked finalist<br>2. `test_rf23_approver_may_choose_a_candidate_who_is_not_first_in_the_ranking`: approver may choose a candidate who is not first in the ranking<br>3. `test_rf23_explicit_human_confirmation_and_justification_are_required`: explicit human confirmation and justification are required<br>4. `test_rf23_candidate_of_another_vacancy_is_rejected`: candidate of another vacancy is rejected<br>5. `test_rf23_candidate_of_another_tenant_is_rejected`: candidate of another tenant is rejected<br>6. `test_rf23_non_finalist_or_incompletely_evaluated_candidates_are_rejected`: non finalist or incompletely evaluated candidates are rejected<br>7. `test_rf23_recorded_decision_cannot_be_replaced`: recorded decision cannot be replaced<br>8. `test_rf23_only_the_approver_can_record_the_decision`: only the approver can record the decision<br>9. `test_rf23_approver_of_another_organization_cannot_decide`: approver of another organization cannot decide<br>10. `test_rf23_decision_is_rejected_for_a_closed_vacancy`: decision is rejected for a closed vacancy |
| Resultado esperado | Las 10 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/FinalDecisionTest.php (10 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=FinalDecisionTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (10/10 aprobadas) |

### CP-043 — Registrar decisión final de selección

| Campo | Valor |
|---|---|
| RF relacionado | RF-23 |
| CU relacionado | CU-18 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar decisión final de selección» con 1 prueba(s) automatizada(s) de `RankingComparisonTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf23_calculating_the_ranking_never_selects_a_candidate`: calculating the ranking never selects a candidate |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/RankingComparisonTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RankingComparisonTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-044 — Registrar selección del candidato

| Campo | Valor |
|---|---|
| RF relacionado | RF-24 |
| CU relacionado | CU-19 |
| Referencia transversal | — |
| Objetivo | Verificar «Registrar selección del candidato» con 7 prueba(s) automatizada(s) de `SelectionRegistrationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf24_hr_registers_the_selection_after_the_human_decision`: hr registers the selection after the human decision<br>2. `test_rf24_selection_requires_a_recorded_human_decision`: selection requires a recorded human decision<br>3. `test_rf24_selection_cannot_be_registered_twice`: selection cannot be registered twice<br>4. `test_rf24_only_hr_can_register_the_selection`: only hr can register the selection<br>5. `test_rf24_hr_of_another_organization_cannot_register_the_selection`: hr of another organization cannot register the selection<br>6. `test_rf24_manual_stage_changes_are_blocked_after_the_final_decision`: manual stage changes are blocked after the final decision<br>7. `test_rf24_database_prevents_two_selected_candidates_in_the_same_vacancy`: database prevents two selected candidates in the same vacancy |
| Resultado esperado | Las 7 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/SelectionRegistrationTest.php (7 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=SelectionRegistrationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (7/7 aprobadas) |

### CP-045 — Cerrar vacante o convocatoria

| Campo | Valor |
|---|---|
| RF relacionado | RF-25 |
| CU relacionado | CU-20 |
| Referencia transversal | — |
| Objetivo | Verificar «Cerrar vacante o convocatoria» con 5 prueba(s) automatizada(s) de `VacancyClosureTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf25_hr_closes_the_vacancy_after_the_selection_is_registered`: hr closes the vacancy after the selection is registered<br>2. `test_rf25_closure_without_a_registered_selection_is_rejected`: closure without a registered selection is rejected<br>3. `test_rf25_only_hr_can_close_the_vacancy`: only hr can close the vacancy<br>4. `test_rf25_hr_of_another_organization_cannot_close_the_vacancy`: hr of another organization cannot close the vacancy<br>5. `test_rf25_closed_vacancy_rejects_incompatible_operations`: closed vacancy rejects incompatible operations |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Selection/VacancyClosureTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyClosureTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-046 — Notificar resultado y cierre al postulante / Generar registro de auditoría

| Campo | Valor |
|---|---|
| RF relacionado | RF-26, RF-27 |
| CU relacionado | CU-20 |
| Referencia transversal | — |
| Objetivo | Verificar «Notificar resultado y cierre al postulante / Generar registro de auditoría» con 1 prueba(s) automatizada(s) de `ProcessResultNotificationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf26_rf27_result_notifications_are_audited_without_personal_data`: result notifications are audited without personal data |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Notifications/ProcessResultNotificationTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ProcessResultNotificationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-047 — Notificar resultado y cierre al postulante

| Campo | Valor |
|---|---|
| RF relacionado | RF-26 |
| CU relacionado | CU-20 |
| Referencia transversal | — |
| Objetivo | Verificar «Notificar resultado y cierre al postulante» con 7 prueba(s) automatizada(s) de `ProcessResultNotificationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf26_selected_candidate_receives_the_result_when_the_vacancy_closes`: selected candidate receives the result when the vacancy closes<br>2. `test_rf26_not_selected_candidates_receive_the_result_when_the_vacancy_closes`: not selected candidates receive the result when the vacancy closes<br>3. `test_rf26_no_final_result_is_sent_before_the_vacancy_is_closed`: no final result is sent before the vacancy is closed<br>4. `test_rf26_only_candidates_of_the_closed_vacancy_are_notified`: only candidates of the closed vacancy are notified<br>5. `test_rf26_closing_a_vacancy_of_another_organization_does_not_notify_this_organization_candidates`: closing a vacancy of another organization does not notify this organization candidates<br>6. `test_rf26_result_notification_does_not_expose_scores_ranking_or_internal_notes`: result notification does not expose scores ranking or internal notes<br>7. `test_rf26_final_result_is_not_sent_twice_when_closure_is_repeated`: final result is not sent twice when closure is repeated |
| Resultado esperado | Las 7 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Notifications/ProcessResultNotificationTest.php (7 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ProcessResultNotificationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (7/7 aprobadas) |

### CP-048 — Generar registro de auditoría

| Campo | Valor |
|---|---|
| RF relacionado | RF-27 |
| CU relacionado | — |
| Referencia transversal | — |
| Objetivo | Verificar «Generar registro de auditoría» con 7 prueba(s) automatizada(s) de `AuditLogViewTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf27_approver_views_the_organization_audit_trail_latest_first`: approver views the organization audit trail latest first<br>2. `test_rf27_unauthorized_roles_cannot_view_the_audit_trail`: unauthorized roles cannot view the audit trail<br>3. `test_rf27_organization_never_sees_audit_logs_of_another_organization`: organization never sees audit logs of another organization<br>4. `test_rf27_logs_without_organization_are_not_listed`: logs without organization are not listed<br>5. `test_rf27_audit_trail_can_be_filtered_by_action`: audit trail can be filtered by action<br>6. `test_rf27_details_show_readable_labels_and_local_dates_instead_of_raw_values`: details show readable labels and local dates instead of raw values<br>7. `test_rf27_view_shows_only_a_safe_summary`: view shows only a safe summary |
| Resultado esperado | Las 7 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Audit/AuditLogViewTest.php (7 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=AuditLogViewTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (7/7 aprobadas) |

### CP-049 — Reglas complementarias de AuditLoggerTest (RF-27)

| Campo | Valor |
|---|---|
| RF relacionado | RF-27 |
| CU relacionado | — |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de AuditLoggerTest (RF-27)» con 4 prueba(s) automatizada(s) de `AuditLoggerTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_records_actor_action_entity_and_organization`: records actor action entity and organization<br>2. `test_sensitive_metadata_is_never_stored`: sensitive metadata is never stored<br>3. `test_audit_logs_cannot_be_updated`: audit logs cannot be updated<br>4. `test_audit_logs_cannot_be_deleted`: audit logs cannot be deleted |
| Resultado esperado | Las 4 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Audit/AuditLoggerTest.php (4 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=AuditLoggerTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-050 — Generar registro de auditoría

| Campo | Valor |
|---|---|
| RF relacionado | RF-27 |
| CU relacionado | — |
| Referencia transversal | — |
| Objetivo | Verificar «Generar registro de auditoría» con 5 prueba(s) automatizada(s) de `AuditTrailTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_rf27_full_process_generates_an_audit_trail_with_tenant_actor_and_entity`: full process generates an audit trail with tenant actor and entity<br>2. `test_rf27_audit_logs_are_append_only_at_database_level`: audit logs are append only at database level<br>3. `test_rf27_deleting_a_user_keeps_the_audit_record_without_the_actor_reference`: deleting a user keeps the audit record without the actor reference<br>4. `test_rf27_sensitive_values_are_never_stored_in_metadata`: sensitive values are never stored in metadata<br>5. `test_rf27_audit_trail_is_exposed_read_only`: audit trail is exposed read only |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Audit/AuditTrailTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=AuditTrailTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-051 — Reglas complementarias de OrganizationScopeTest (RF-27)

| Campo | Valor |
|---|---|
| RF relacionado | RF-27 |
| CU relacionado | — |
| Referencia transversal | — |
| Objetivo | Verificar «Reglas complementarias de OrganizationScopeTest (RF-27)» con 4 prueba(s) automatizada(s) de `OrganizationScopeTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_staff_user_only_sees_records_of_own_organization`: staff user only sees records of own organization<br>2. `test_scope_is_not_applied_without_authenticated_staff_user`: scope is not applied without authenticated staff user<br>3. `test_database_rejects_staff_user_without_organization`: database rejects staff user without organization<br>4. `test_database_rejects_candidate_linked_to_an_organization`: database rejects candidate linked to an organization |
| Resultado esperado | Las 4 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Multitenencia |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Tenancy/OrganizationScopeTest.php (4 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=OrganizationScopeTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-052 — Transversal — DashboardTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Transversal |
| Objetivo | Verificar Transversal con 2 prueba(s) automatizada(s) de `DashboardTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_guests_are_redirected_to_the_login_page`: guests are redirected to the login page<br>2. `test_authenticated_users_can_visit_the_dashboard`: authenticated users can visit the dashboard |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Integración / funcional |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/DashboardTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=DashboardTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-053 — RF-29 (EXPERIMENTAL / PROPUESTO) — MlCrossTenantValidationTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 10 prueba(s) automatizada(s) de `MlCrossTenantValidationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_each_organization_gets_its_own_counts`: each organization gets its own counts<br>2. `test_adding_data_to_b_does_not_move_the_vector_of_a`: adding data to b does not move the vector of a<br>3. `test_concurrent_vacancies_never_count_another_organization`: concurrent vacancies never count another organization<br>4. `test_there_is_no_leakage_without_a_session`: there is no leakage without a session<br>5. `test_the_vector_of_a_is_unchanged_when_b_is_wiped`: the vector of a is unchanged when b is wiped<br>6. `test_hr_of_a_cannot_reach_the_vacancy_of_b`: hr of a cannot reach the vacancy of b<br>7. `test_the_denial_does_not_reveal_whether_the_vacancy_exists`: the denial does not reveal whether the vacancy exists<br>8. `test_each_organization_sees_only_its_own_risk`: each organization sees only its own risk<br>9. `test_the_payload_sent_for_a_carries_only_its_own_counts`: the payload sent for a carries only its own counts<br>10. `test_the_policy_denies_across_organizations`: the policy denies across organizations |
| Resultado esperado | Las 10 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/MlCrossTenantValidationTest.php (10 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=MlCrossTenantValidationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (10/10 aprobadas) |

### CP-054 — RF-29 (EXPERIMENTAL / PROPUESTO) — MlRiskClientTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 34 prueba(s) automatizada(s) de `MlRiskClientTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_a_valid_response_produces_a_prediction`: a valid response produces a prediction<br>2. `test_it_sends_only_the_fifteen_features`: it sends only the fifteen features<br>3. `test_it_attaches_the_internal_token_when_configured`: it attaches the internal token when configured<br>4. `test_it_sends_no_token_header_when_none_is_configured`: it sends no token header when none is configured<br>5. `test_a_disabled_service_never_calls_out`: a disabled service never calls out<br>6. `test_a_connection_failure_falls_back`: a connection failure falls back<br>7. `test_a_timeout_is_reported_as_such`: a timeout is reported as such<br>8. `test_a_503_means_the_model_is_unavailable`: a 503 means the model is unavailable<br>9. `test_a_422_means_our_payload_was_wrong`: a 422 means our payload was wrong<br>10. `test_a_401_falls_back_without_breaking`: a 401 falls back without breaking<br>11. `test_a_500_falls_back`: a 500 falls back<br>12. `test_invalid_json_falls_back`: invalid json falls back<br>13. `test_a_wrong_freeze_fingerprint_is_rejected`: a wrong freeze fingerprint is rejected<br>14. `test_a_wrong_threshold_is_rejected`: a wrong threshold is rejected<br>15. `test_a_rounded_threshold_is_rejected`: a rounded threshold is rejected<br>16. `test_an_invalid_score_is_rejected`: an invalid score is rejected<br>17. `test_a_non_boolean_flag_is_rejected`: a non boolean flag is rejected<br>18. `test_a_flag_inconsistent_with_the_threshold_is_rejected`: a flag inconsistent with the threshold is rejected<br>19. `test_a_response_that_stops_declaring_itself_experimental_is_rejected`: a response that stops declaring itself experimental is rejected<br>20. `test_a_missing_key_is_rejected`: a missing key is rejected<br>21. `test_an_empty_model_version_is_rejected`: an empty model version is rejected<br>22. `test_a_blank_model_version_is_rejected`: a blank model version is rejected<br>23. `test_a_different_model_version_is_rejected`: a different model version is rejected<br>24. `test_a_non_string_model_version_is_rejected`: a non string model version is rejected<br>25. `test_a_non_string_fingerprint_is_rejected`: a non string fingerprint is rejected<br>26. `test_a_non_string_status_is_rejected`: a non string status is rejected<br>27. `test_a_non_numeric_score_is_rejected`: a non numeric score is rejected<br>28. `test_a_non_numeric_threshold_is_rejected`: a non numeric threshold is rejected<br>29. `test_a_missing_status_is_rejected`: a missing status is rejected<br>30. `test_the_valid_response_is_still_accepted`: the valid response is still accepted<br>31. `test_a_transient_failure_is_retried_once`: a transient failure is retried once<br>32. `test_an_error_response_is_not_retried`: an error response is not retried<br>33. `test_health_reports_the_service_state`: health reports the service state<br>34. `test_health_survives_a_dead_service`: health survives a dead service |
| Resultado esperado | Las 64 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/MlRiskClientTest.php (34 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=MlRiskClientTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (64/64 aprobadas) |

### CP-055 — RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskAuthorizationTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 9 prueba(s) automatizada(s) de `OperationalRiskAuthorizationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_human_resources_is_authorised`: human resources is authorised<br>2. `test_the_approver_is_authorised`: the approver is authorised<br>3. `test_other_roles_are_denied`: other roles are denied<br>4. `test_a_guest_is_denied`: a guest is denied<br>5. `test_a_candidate_with_an_application_is_still_denied`: a candidate with an application is still denied<br>6. `test_an_evaluator_assigned_to_the_process_is_still_denied`: an evaluator assigned to the process is still denied<br>7. `test_the_route_and_the_policy_agree_for_every_role`: the route and the policy agree for every role<br>8. `test_the_denial_leaks_nothing_about_the_process`: the denial leaks nothing about the process<br>9. `test_every_role_in_the_system_is_covered_by_this_suite`: every role in the system is covered by this suite |
| Resultado esperado | Las 11 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/OperationalRiskAuthorizationTest.php (9 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=OperationalRiskAuthorizationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (11/11 aprobadas) |

### CP-056 — RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskCheckpointTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 21 prueba(s) automatizada(s) de `OperationalRiskCheckpointTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_the_checkpoint_is_the_start_of_the_day_after_the_close`: the checkpoint is the start of the day after the close<br>2. `test_only_events_up_to_the_checkpoint_enter_the_vector`: only events up to the checkpoint enter the vector<br>3. `test_sessions_respect_the_same_boundary`: sessions respect the same boundary<br>4. `test_the_vector_is_identical_whenever_it_is_rebuilt`: the vector is identical whenever it is rebuilt<br>5. `test_days_remaining_is_measured_from_the_checkpoint`: days remaining is measured from the checkpoint<br>6. `test_concurrent_open_vacancies_is_reconstructed_at_the_checkpoint`: concurrent open vacancies is reconstructed at the checkpoint<br>7. `test_the_last_operational_event_uses_the_closed_list`: the last operational event uses the closed list<br>8. `test_an_event_after_the_checkpoint_does_not_become_the_latest`: an event after the checkpoint does not become the latest<br>9. `test_a_column_outside_the_closed_list_does_not_affect_the_feature`: a column outside the closed list does not affect the feature<br>10. `test_without_events_the_fallback_is_the_publication`: without events the fallback is the publication<br>11. `test_the_query_window_spans_from_the_checkpoint_to_the_target`: the query window spans from the checkpoint to the target<br>12. `test_a_query_days_after_the_checkpoint_still_predicts`: a query days after the checkpoint still predicts<br>13. `test_events_after_the_checkpoint_do_not_alter_a_later_query`: events after the checkpoint do not alter a later query<br>14. `test_a_late_query_means_outside_the_window_not_after_the_checkpoint_day`: a late query means outside the window not after the checkpoint day<br>15. `test_a_query_after_the_target_falls_back`: a query after the target falls back<br>16. `test_closing_the_vacancy_ends_the_window_before_the_target`: closing the vacancy ends the window before the target<br>17. `test_reconstruction_and_eligibility_are_separate_questions`: reconstruction and eligibility are separate questions<br>18. `test_at_the_checkpoint_the_query_is_eligible`: at the checkpoint the query is eligible<br>19. `test_a_second_before_the_checkpoint_the_query_is_not_eligible`: a second before the checkpoint the query is not eligible<br>20. `test_a_closed_vacancy_is_not_eligible_even_inside_the_window`: a closed vacancy is not eligible even inside the window<br>21. `test_a_target_that_does_not_survive_the_checkpoint_is_not_eligible`: a target that does not survive the checkpoint is not eligible |
| Resultado esperado | Las 21 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/OperationalRiskCheckpointTest.php (21 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=OperationalRiskCheckpointTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (21/21 aprobadas) |

### CP-057 — RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskFeatureBuilderTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 19 prueba(s) automatizada(s) de `OperationalRiskFeatureBuilderTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_it_produces_exactly_the_fifteen_contract_features`: it produces exactly the fifteen contract features<br>2. `test_every_value_is_an_integer`: every value is an integer<br>3. `test_no_identifier_or_personal_attribute_leaves_the_builder`: no identifier or personal attribute leaves the builder<br>4. `test_an_incomplete_feature_set_is_rejected`: an incomplete feature set is rejected<br>5. `test_an_unexpected_feature_is_rejected`: an unexpected feature is rejected<br>6. `test_configuration_features_come_from_the_vacancy`: configuration features come from the vacancy<br>7. `test_the_application_window_falls_back_to_the_publication_date`: the application window falls back to the publication date<br>8. `test_applications_and_stage_moves_are_counted`: applications and stage moves are counted<br>9. `test_stage_moves_are_not_broken_down_by_destination`: stage moves are not broken down by destination<br>10. `test_sessions_are_counted_as_scheduled_completed_and_overdue`: sessions are counted as scheduled completed and overdue<br>11. `test_the_interview_outcome_is_never_read`: the interview outcome is never read<br>12. `test_nothing_after_the_checkpoint_is_counted`: nothing after the checkpoint is counted<br>13. `test_days_since_last_event_uses_the_latest_closed_list_event`: days since last event uses the latest closed list event<br>14. `test_without_events_the_last_event_is_the_publication`: without events the last event is the publication<br>15. `test_days_remaining_to_target_counts_whole_days`: days remaining to target counts whole days<br>16. `test_an_expired_target_is_not_clamped`: an expired target is not clamped<br>17. `test_concurrent_vacancies_exclude_the_vacancy_itself`: concurrent vacancies exclude the vacancy itself<br>18. `test_concurrent_vacancies_ignore_other_organizations`: concurrent vacancies ignore other organizations<br>19. `test_counts_ignore_rows_belonging_to_another_organization`: counts ignore rows belonging to another organization |
| Resultado esperado | Las 19 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/OperationalRiskFeatureBuilderTest.php (19 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=OperationalRiskFeatureBuilderTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (19/19 aprobadas) |

### CP-058 — RF-29 (EXPERIMENTAL / PROPUESTO) — OperationalRiskServiceTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 19 prueba(s) automatizada(s) de `OperationalRiskServiceTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_an_assessable_vacancy_gets_a_prediction`: an assessable vacancy gets a prediction<br>2. `test_the_assessment_declares_what_it_is_and_is_not`: the assessment declares what it is and is not<br>3. `test_a_low_score_produces_no_flag`: a low score produces no flag<br>4. `test_the_flag_message_stays_neutral`: the flag message stays neutral<br>5. `test_without_a_target_there_is_no_prediction`: without a target there is no prediction<br>6. `test_an_expired_target_falls_back_instead_of_extrapolating`: an expired target falls back instead of extrapolating<br>7. `test_before_the_checkpoint_there_is_no_prediction`: before the checkpoint there is no prediction<br>8. `test_the_checkpoint_is_the_day_after_the_application_close`: the checkpoint is the day after the application close<br>9. `test_a_vacancy_without_a_close_date_has_no_checkpoint`: a vacancy without a close date has no checkpoint<br>10. `test_events_after_the_checkpoint_do_not_change_the_vector`: events after the checkpoint do not change the vector<br>11. `test_the_eligible_case_sends_the_fifteen_features`: the eligible case sends the fifteen features<br>12. `test_a_closed_vacancy_gets_no_late_prediction`: a closed vacancy gets no late prediction<br>13. `test_a_late_query_gets_no_prediction`: a late query gets no prediction<br>14. `test_a_target_that_does_not_survive_the_checkpoint_is_out_of_scope`: a target that does not survive the checkpoint is out of scope<br>15. `test_an_unpublished_vacancy_falls_back`: an unpublished vacancy falls back<br>16. `test_a_dead_service_does_not_break_the_flow`: a dead service does not break the flow<br>17. `test_no_score_is_invented_when_there_is_no_prediction`: no score is invented when there is no prediction<br>18. `test_an_incompatible_response_falls_back`: an incompatible response falls back<br>19. `test_a_disabled_integration_returns_the_descriptive_panel`: a disabled integration returns the descriptive panel |
| Resultado esperado | Las 19 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/OperationalRiskServiceTest.php (19 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=OperationalRiskServiceTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (19/19 aprobadas) |

### CP-059 — RF-29 (EXPERIMENTAL / PROPUESTO) — TargetCompletionTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 16 prueba(s) automatizada(s) de `TargetCompletionTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_the_column_exists_and_is_nullable`: the column exists and is nullable<br>2. `test_the_value_is_cast_to_a_datetime`: the value is cast to a datetime<br>3. `test_the_database_rejects_a_target_before_the_application_close`: the database rejects a target before the application close<br>4. `test_existing_vacancies_keep_working_without_a_target`: existing vacancies keep working without a target<br>5. `test_hr_can_register_a_target_completion_date`: hr can register a target completion date<br>6. `test_the_target_must_be_after_the_application_close`: the target must be after the application close<br>7. `test_the_target_is_optional`: the target is optional<br>8. `test_the_target_cannot_be_changed_once_published`: the target cannot be changed once published<br>9. `test_the_model_reports_when_the_target_is_editable`: the model reports when the target is editable<br>10. `test_the_target_is_recorded_in_the_audit_trail`: the target is recorded in the audit trail<br>11. `test_the_edit_form_receives_the_current_target`: the edit form receives the current target<br>12. `test_the_edit_form_receives_null_when_there_is_no_target`: the edit form receives null when there is no target<br>13. `test_the_detail_view_exposes_the_target`: the detail view exposes the target<br>14. `test_the_form_component_offers_the_field`: the form component offers the field<br>15. `test_an_update_in_draft_can_change_the_target`: an update in draft can change the target<br>16. `test_hr_cannot_set_a_target_on_another_organizations_vacancy`: hr cannot set a target on another organizations vacancy |
| Resultado esperado | Las 16 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/TargetCompletionTest.php (16 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=TargetCompletionTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (16/16 aprobadas) |

### CP-060 — RF-29 (EXPERIMENTAL / PROPUESTO) — VacancyOperationalRiskRouteTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar RF-29 (EXPERIMENTAL / PROPUESTO) con 12 prueba(s) automatizada(s) de `VacancyOperationalRiskRouteTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_hr_can_query_the_operational_risk`: hr can query the operational risk<br>2. `test_the_approver_can_query_it`: the approver can query it<br>3. `test_a_candidate_cannot_query_it`: a candidate cannot query it<br>4. `test_an_evaluator_cannot_query_it`: an evaluator cannot query it<br>5. `test_a_guest_cannot_query_it`: a guest cannot query it<br>6. `test_hr_cannot_query_another_organizations_vacancy`: hr cannot query another organizations vacancy<br>7. `test_the_policy_denies_a_foreign_vacancy_even_without_the_global_scope`: the policy denies a foreign vacancy even without the global scope<br>8. `test_the_response_declares_the_experimental_nature`: the response declares the experimental nature<br>9. `test_the_response_never_mentions_candidates_or_decisions`: the response never mentions candidates or decisions<br>10. `test_a_dead_service_still_returns_a_usable_panel`: a dead service still returns a usable panel<br>11. `test_a_vacancy_without_a_target_returns_the_descriptive_panel`: a vacancy without a target returns the descriptive panel<br>12. `test_the_response_leaks_no_paths_or_traces`: the response leaks no paths or traces |
| Resultado esperado | Las 12 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Ml/VacancyOperationalRiskRouteTest.php (12 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VacancyOperationalRiskRouteTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (12/12 aprobadas) |

### CP-061 — Prueba de humo del starter kit — ExampleTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Prueba de humo del starter kit |
| Objetivo | Verificar Prueba de humo del starter kit con 1 prueba(s) automatizada(s) de `ExampleTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_returns_a_successful_response`: returns a successful response |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Regresión |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/ExampleTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ExampleTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-062 — Regresión de DEF-09 (zona horaria) — AppTimezoneTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Regresión de DEF-09 (zona horaria) |
| Objetivo | Verificar Regresión de DEF-09 (zona horaria) con 2 prueba(s) automatizada(s) de `AppTimezoneTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_root_view_exposes_the_application_timezone_for_date_formatting`: root view exposes the application timezone for date formatting<br>2. `test_public_pages_also_expose_the_application_timezone`: public pages also expose the application timezone |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Regresión |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Frontend/AppTimezoneTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=AppTimezoneTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-063 — Prueba de humo del starter kit — ExampleTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Prueba de humo del starter kit |
| Objetivo | Verificar Prueba de humo del starter kit con 1 prueba(s) automatizada(s) de `ExampleTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_that_true_is_true`: that true is true |
| Resultado esperado | Las 1 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Regresión |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/ExampleTest.php (1 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ExampleTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-064 — RNF-01 — EmailVerificationTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 6 prueba(s) automatizada(s) de `EmailVerificationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_email_verification_screen_can_be_rendered`: email verification screen can be rendered<br>2. `test_email_can_be_verified`: email can be verified<br>3. `test_email_is_not_verified_with_invalid_hash`: email is not verified with invalid hash<br>4. `test_email_is_not_verified_with_invalid_user_id`: email is not verified with invalid user id<br>5. `test_verified_user_is_redirected_to_dashboard_from_verification_prompt`: verified user is redirected to dashboard from verification prompt<br>6. `test_already_verified_user_visiting_verification_link_is_redirected_without_firing_event_again`: already verified user visiting verification link is redirected without firing event again |
| Resultado esperado | Las 6 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/EmailVerificationTest.php (6 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=EmailVerificationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **OMITIDO (función del starter kit desactivada)** (0/6 aprobadas, 6 omitidas) |

### CP-065 — RNF-01 — PasswordConfirmationTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 2 prueba(s) automatizada(s) de `PasswordConfirmationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_confirm_password_screen_can_be_rendered`: confirm password screen can be rendered<br>2. `test_password_confirmation_requires_authentication`: password confirmation requires authentication |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/PasswordConfirmationTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=PasswordConfirmationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-066 — RNF-01 — PasswordResetTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 5 prueba(s) automatizada(s) de `PasswordResetTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_reset_password_link_screen_can_be_rendered`: reset password link screen can be rendered<br>2. `test_reset_password_link_can_be_requested`: reset password link can be requested<br>3. `test_reset_password_screen_can_be_rendered`: reset password screen can be rendered<br>4. `test_password_can_be_reset_with_valid_token`: password can be reset with valid token<br>5. `test_password_cannot_be_reset_with_invalid_token`: password cannot be reset with invalid token |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/PasswordResetTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=PasswordResetTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-067 — RNF-01 — RegistrationTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 2 prueba(s) automatizada(s) de `RegistrationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_registration_screen_can_be_rendered`: registration screen can be rendered<br>2. `test_new_users_can_register`: new users can register |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/RegistrationTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RegistrationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-068 — RNF-01 — RoleMiddlewareTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 3 prueba(s) automatizada(s) de `RoleMiddlewareTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_guest_is_redirected_to_login`: guest is redirected to login<br>2. `test_user_without_allowed_role_is_forbidden`: user without allowed role is forbidden<br>3. `test_user_with_allowed_role_passes`: user with allowed role passes |
| Resultado esperado | Las 3 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/RoleMiddlewareTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=RoleMiddlewareTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-069 — RNF-01 — TwoFactorChallengeTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 2 prueba(s) automatizada(s) de `TwoFactorChallengeTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_two_factor_challenge_redirects_to_login_when_not_authenticated`: two factor challenge redirects to login when not authenticated<br>2. `test_two_factor_challenge_can_be_rendered`: two factor challenge can be rendered |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/TwoFactorChallengeTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=TwoFactorChallengeTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-070 — RNF-01 — VerificationNotificationTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 2 prueba(s) automatizada(s) de `VerificationNotificationTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_sends_verification_notification`: sends verification notification<br>2. `test_does_not_send_verification_notification_if_email_is_verified`: does not send verification notification if email is verified |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Auth/VerificationNotificationTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=VerificationNotificationTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **OMITIDO (función del starter kit desactivada)** (0/2 aprobadas, 2 omitidas) |

### CP-071 — RNF-01 — NumericRouteParametersTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 2 prueba(s) automatizada(s) de `NumericRouteParametersTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_non_numeric_identifiers_respond_not_found_instead_of_a_server_error`: non numeric identifiers respond not found instead of a server error<br>2. `test_the_localized_create_route_still_works`: the localized create route still works |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Routing/NumericRouteParametersTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=NumericRouteParametersTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-072 — RNF-01 — ProfileUpdateTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 5 prueba(s) automatizada(s) de `ProfileUpdateTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_profile_page_is_displayed`: profile page is displayed<br>2. `test_profile_information_can_be_updated`: profile information can be updated<br>3. `test_email_verification_status_is_unchanged_when_the_email_address_is_unchanged`: email verification status is unchanged when the email address is unchanged<br>4. `test_user_can_delete_their_account`: user can delete their account<br>5. `test_correct_password_must_be_provided_to_delete_account`: correct password must be provided to delete account |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Settings/ProfileUpdateTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=ProfileUpdateTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-073 — RNF-01 — SecurityTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar RNF-01 con 5 prueba(s) automatizada(s) de `SecurityTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_security_page_is_displayed`: security page is displayed<br>2. `test_security_page_requires_password_confirmation_when_enabled`: security page requires password confirmation when enabled<br>3. `test_security_page_renders_without_two_factor_when_feature_is_disabled`: security page renders without two factor when feature is disabled<br>4. `test_password_can_be_updated`: password can be updated<br>5. `test_correct_password_must_be_provided_to_update_password`: correct password must be provided to update password |
| Resultado esperado | Las 5 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Settings/SecurityTest.php (5 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=SecurityTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-074 — RNF-01; regresión de DEF-13 — E2eEnvironmentTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01; regresión de DEF-13 |
| Objetivo | Verificar RNF-01; regresión de DEF-13 con 2 prueba(s) automatizada(s) de `E2eEnvironmentTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_detects_whether_the_active_database_is_the_configured_e2e_database`: detects whether the active database is the configured e2e database<br>2. `test_reset_never_touches_a_database_that_is_not_the_e2e_database`: reset never touches a database that is not the e2e database |
| Resultado esperado | Las 2 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Testing/E2eEnvironmentTest.php (2 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=E2eEnvironmentTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-075 — RNF-01; regresión de DEF-13 — E2eSupportTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-01; regresión de DEF-13 |
| Objetivo | Verificar RNF-01; regresión de DEF-13 con 9 prueba(s) automatizada(s) de `E2eSupportTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_endpoints_do_not_exist_when_e2e_support_is_disabled`: endpoints do not exist when e2e support is disabled<br>2. `test_endpoints_do_not_exist_in_production_even_if_enabled`: endpoints do not exist in production even if enabled<br>3. `test_enabled_endpoints_reject_a_missing_or_wrong_token`: enabled endpoints reject a missing or wrong token<br>4. `test_reset_endpoint_restores_the_known_demo_state`: reset endpoint restores the known demo state<br>5. `test_reset_endpoint_refuses_when_the_active_database_is_not_the_e2e_database`: reset endpoint refuses when the active database is not the e2e database<br>6. `test_queue_endpoint_reports_pending_jobs`: queue endpoint reports pending jobs<br>7. `test_reset_command_runs_against_the_e2e_database`: reset command runs against the e2e database<br>8. `test_reset_command_refuses_a_database_that_is_not_the_e2e_database`: reset command refuses a database that is not the e2e database<br>9. `test_reset_command_refuses_to_run_in_production`: reset command refuses to run in production |
| Resultado esperado | Las 9 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Feature/Testing/E2eSupportTest.php (9 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=E2eSupportTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (9/9 aprobadas) |

### CP-076 — Transversal — JobRequestStatusTest

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Transversal |
| Objetivo | Verificar Transversal con 3 prueba(s) automatizada(s) de `JobRequestStatusTest`. |
| Precondiciones | Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus datos con fábricas y `RefreshDatabase` |
| Datos | Ficticios: organizaciones, usuarios por rol y registros creados por fábricas |
| Pasos | 1. `test_transition_rules`: transition rules<br>2. `test_only_draft_and_observed_requests_are_editable`: only draft and observed requests are editable<br>3. `test_approved_and_rejected_are_terminal`: approved and rejected are terminal |
| Resultado esperado | Las 13 ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos. |
| Tipo de prueba | Unitaria |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `tests/Unit/Enums/JobRequestStatusTest.php (3 métodos)` |
| Comando | `docker compose exec app php artisan test --filter=JobRequestStatusTest` |
| Evidencia | docs/academico/qa-final/evidencias/04-phpunit.log; docs/academico/qa-final/evidencias/phpunit-junit.xml |
| Estado (F29F) | **APROBADO** (13/13 aprobadas) |

### CP-077 — E2E-00 · Soporte · fechas en la zona horaria de la aplicación

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Regresión de DEF-12 (fechas en la zona horaria de la aplicación) |
| Objetivo | Verificar en navegador el comportamiento de «Soporte · fechas en la zona horaria de la aplicación». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: usa la fecha de Lima aunque en UTC ya sea el día siguiente<br>2. it: coincide con UTC durante el día en Lima<br>3. it: usa America/Lima por defecto |
| Resultado esperado | Los 3 tests del spec pasan sin reintentos. |
| Tipo de prueba | Regresión |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-00-app-dates.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-00-app-dates.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-078 — E2E-01 · E2E-01 · Inicio de sesión por rol

| Campo | Valor |
|---|---|
| RF relacionado | RF-08 |
| CU relacionado | CU-07 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-01 · Inicio de sesión por rol». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: ${label}: inicia sesión y ve solo el menú de su rol<br>2. it: rechaza credenciales inválidas sin iniciar sesión<br>3. (algunas pruebas se generan en bucle: el total ejecutado es mayor que los `it` del código) |
| Resultado esperado | Los 6 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-01-login.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-01-login.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (6/6 aprobadas) |

### CP-079 — E2E-02 · E2E-02 · El área solicitante registra un requerimiento (RF-01)

| Campo | Valor |
|---|---|
| RF relacionado | RF-01, RF-02 |
| CU relacionado | CU-01, CU-02 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-02 · El área solicitante registra un requerimiento (RF-01)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: registra el requerimiento y lo envía a RR. HH.<br>2. it: no registra un requerimiento con datos obligatorios vacíos |
| Resultado esperado | Los 2 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-02-register-job-request.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-02-register-job-request.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-080 — E2E-03 · E2E-03 · El aprobador decide un requerimiento validado (RF-03, RF-04)

| Campo | Valor |
|---|---|
| RF relacionado | RF-03, RF-04 |
| CU relacionado | CU-03 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-03 · El aprobador decide un requerimiento validado (RF-03, RF-04)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: aprueba el requerimiento validado por RR. HH.<br>2. it: no permite rechazar sin indicar el motivo |
| Resultado esperado | Los 2 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-03-approve-job-request.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-03-approve-job-request.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-081 — E2E-04 · E2E-04 · RR. HH. configura y publica una vacante (RF-05 a RF-07)

| Campo | Valor |
|---|---|
| RF relacionado | RF-05, RF-06, RF-07, RF-20 |
| CU relacionado | CU-04, CU-05, CU-06, CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-04 · RR. HH. configura y publica una vacante (RF-05 a RF-07)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: genera la vacante desde un requerimiento aprobado, la valida y la publica<br>2. it: impide publicar si las ponderaciones no suman 100 |
| Resultado esperado | Los 2 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-04-configure-publish-vacancy.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-04-configure-publish-vacancy.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-082 — E2E-05 · E2E-05 · El postulante completa su perfil y postula (RF-08 a RF-11)

| Campo | Valor |
|---|---|
| RF relacionado | RF-08, RF-09, RF-10, RF-11 |
| CU relacionado | CU-07, CU-08, CU-09 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-05 · El postulante completa su perfil y postula (RF-08 a RF-11)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: completa perfil, carga su CV, postula y recibe la confirmación |
| Resultado esperado | Los 1 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-05-candidate-apply.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-05-candidate-apply.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-083 — E2E-06 · E2E-06 · RR. HH. preselecciona a un candidato (RF-12 a RF-15)

| Campo | Valor |
|---|---|
| RF relacionado | RF-12, RF-13, RF-14, RF-15 |
| CU relacionado | CU-10, CU-11, CU-12 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-06 · RR. HH. preselecciona a un candidato (RF-12 a RF-15)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: revisa la postulación, la preselecciona y el postulante es notificado<br>2. it: no descarta una postulación sin indicar el motivo |
| Resultado esperado | Los 2 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-06-shortlist-candidate.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-06-shortlist-candidate.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-084 — E2E-07 · E2E-07 · El evaluador registra resultados (RF-19, RF-20)

| Campo | Valor |
|---|---|
| RF relacionado | RF-19, RF-20 |
| CU relacionado | CU-15, CU-16 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-07 · El evaluador registra resultados (RF-19, RF-20)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: registra los puntajes de la evaluación asignada dentro del rango de cada criterio |
| Resultado esperado | Los 1 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-07-evaluator-records-results.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-07-evaluator-records-results.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-085 — E2E-08 · E2E-08 · RR. HH. consulta la comparación y el ranking (RF-21, RF-22)

| Campo | Valor |
|---|---|
| RF relacionado | RF-21, RF-22 |
| CU relacionado | CU-17 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-08 · RR. HH. consulta la comparación y el ranking (RF-21, RF-22)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: muestra el ranking ponderado y explicable sin seleccionar a nadie |
| Resultado esperado | Los 1 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-08-comparison-ranking.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-08-comparison-ranking.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-086 — E2E-09 · E2E-09 · El aprobador registra la decisión final humana (RF-23)

| Campo | Valor |
|---|---|
| RF relacionado | RF-23 |
| CU relacionado | CU-18 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-09 · El aprobador registra la decisión final humana (RF-23)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: exige justificación y confirmación humana antes de registrar la decisión<br>2. it: registra la decisión eligiendo a un candidato que no es el primero del ranking |
| Resultado esperado | Los 2 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-09-human-final-decision.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-09-human-final-decision.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (2/2 aprobadas) |

### CP-087 — E2E-10 · E2E-10 · RR. HH. registra la selección y cierra el proceso (RF-24 a RF-26)

| Campo | Valor |
|---|---|
| RF relacionado | RF-24, RF-25, RF-26 |
| CU relacionado | CU-19, CU-20 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «E2E-10 · RR. HH. registra la selección y cierra el proceso (RF-24 a RF-26)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: registra la selección decidida por Dirección, cierra la convocatoria y notifica el resultado |
| Resultado esperado | Los 1 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-10-selection-and-closure.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-10-selection-and-closure.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-088 — E2E-11 · Multitenancy · aislamiento entre organizaciones

| Campo | Valor |
|---|---|
| RF relacionado | RF-27 |
| CU relacionado | — |
| Referencia transversal | RNF-02 |
| Objetivo | Verificar en navegador el comportamiento de «Multitenancy · aislamiento entre organizaciones». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: RR. HH. de la organización B solo ve sus vacantes y no accede a recursos de A<br>2. it: RR. HH. de la organización A no ve la vacante de B<br>3. it: la auditoría de cada organización no muestra registros de la otra<br>4. it: rechaza acciones sobre identificadores de otra organización |
| Resultado esperado | Los 4 tests del spec pasan sin reintentos. |
| Tipo de prueba | Multitenencia |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-11-multitenancy.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-11-multitenancy.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-089 — E2E-12 · Negativos · permisos y reglas del proceso

| Campo | Valor |
|---|---|
| RF relacionado | RF-10, RF-23, RF-24, RF-25 |
| CU relacionado | CU-09, CU-18, CU-19, CU-20 |
| Referencia transversal | RNF-01 |
| Objetivo | Verificar en navegador el comportamiento de «Negativos · permisos y reglas del proceso». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: un rol sin permiso no accede a pantallas de otros roles<br>2. it: no se puede postular a una vacante cerrada<br>3. it: solo el aprobador puede registrar la decisión final<br>4. it: no se puede registrar una selección después del cierre |
| Resultado esperado | Los 4 tests del spec pasan sin reintentos. |
| Tipo de prueba | Seguridad básica |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-12-negative-rules.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-12-negative-rules.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-090 — E2E-13 · Flujo integral · de requerimiento a auditoría

| Campo | Valor |
|---|---|
| RF relacionado | RF-01, RF-02, RF-03, RF-05, RF-07, RF-09, RF-10, RF-14, RF-16, RF-17, RF-18, RF-19, RF-21, RF-23, RF-24, RF-25, RF-26, RF-27 |
| CU relacionado | CU-01, CU-02, CU-03, CU-04, CU-06, CU-08, CU-09, CU-12, CU-13, CU-14, CU-15, CU-17, CU-18, CU-19, CU-20 |
| Referencia transversal | — |
| Objetivo | Verificar en navegador el comportamiento de «Flujo integral · de requerimiento a auditoría». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: 01 el área solicitante registra y envía el requerimiento<br>2. it: 02 RR. HH. valida el requerimiento<br>3. it: 03 el aprobador aprueba el requerimiento<br>4. it: 04 RR. HH. genera, valida y publica la vacante<br>5. it: 05 el postulante completa su perfil, carga su CV y postula<br>6. it: 06 RR. HH. preselecciona y programa evaluación y entrevista<br>7. it: 07 el evaluador registra la evaluación y la entrevista<br>8. it: 08 RR. HH. pasa la postulación a finalista y consulta el ranking<br>9. it: 09 el aprobador registra la decisión final humana<br>10. it: 10 RR. HH. registra la selección y cierra la convocatoria<br>11. it: 11 el postulante ve el resultado y su notificación<br>12. it: 12 el aprobador consulta la auditoría del proceso |
| Resultado esperado | Los 12 tests del spec pasan sin reintentos. |
| Tipo de prueba | Aceptación (flujo completo) |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-13-full-recruitment-flow.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-13-full-recruitment-flow.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (12/12 aprobadas) |

### CP-091 — E2E-14 · E2E-14 · RR. HH. captura el plazo objetivo del proceso (GAP-01)

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar en navegador el comportamiento de «E2E-14 · RR. HH. captura el plazo objetivo del proceso (GAP-01)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: registra el plazo objetivo al configurar una vacante en borrador<br>2. it: el navegador impide enviar un plazo anterior al cierre<br>3. it: el plazo es opcional: la vacante se guarda y publica sin él<br>4. it: deja de poder editarse una vez publicada la vacante |
| Resultado esperado | Los 4 tests del spec pasan sin reintentos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-14-target-completion-form.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-14-target-completion-form.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (4/4 aprobadas) |

### CP-092 — E2E-15 · E2E-15 · Panel de riesgo operacional (RF-29, experimental)

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar en navegador el comportamiento de «E2E-15 · Panel de riesgo operacional (RF-29, experimental)». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: muestra el panel en una vacante publicada, sin inventar una estimación<br>2. it: declara su naturaleza experimental y que no decide nada<br>3. it: nunca habla de candidatos, ranking ni recomendaciones<br>4. it: evita lenguaje alarmista pese a la tasa de alerta alta<br>5. it: no aparece en una vacante en borrador<br>6. it: el Aprobador también lo ve<br>7. it: un postulante no puede consultar el riesgo por la ruta directa<br>8. it: una organización no alcanza el riesgo de otra |
| Resultado esperado | Los 8 tests del spec pasan sin reintentos. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-15-operational-risk-panel.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-15-operational-risk-panel.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (8/8 aprobadas) |

### CP-093 — E2E-16 · E2E-16 · La tabla de expedientes conserva su semántica en móvil

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad y accesibilidad) |
| Objetivo | Verificar en navegador el comportamiento de «E2E-16 · La tabla de expedientes conserva su semántica en móvil». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: requerimientos<br>2. it: vacantes<br>3. it: postulaciones de una vacante<br>4. it: ranking de la comparación<br>5. it: auditoría<br>6. it: evaluaciones asignadas<br>7. it: en móvil cada celda muestra su etiqueta como texto, no como adorno CSS |
| Resultado esperado | Los 7 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E (accesibilidad) |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-16-tabla-accesible-movil.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-16-tabla-accesible-movil.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (7/7 aprobadas) |

### CP-094 — E2E-17 · E2E-17 · El movimiento respeta el teclado y a quien lo reduce

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad y accesibilidad) |
| Objetivo | Verificar en navegador el comportamiento de «E2E-17 · El movimiento respeta el teclado y a quien lo reduce». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: el menú de usuario se abre con teclado y devuelve el foco al cerrarse<br>2. it: la navegación móvil se abre, se cierra con Escape y devuelve el foco<br>3. it: el diálogo de eliminar la cuenta atrapa y devuelve el foco<br>4. it: usa la curva del sistema y no la del navegador<br>5. it: con movimiento reducido no se desplaza nada y la interfaz sigue usable<br>6. it: con movimiento reducido el esqueleto deja de latir y el spinner sigue girando<br>7. it: con movimiento reducido la tabla conserva su semántica accesible<br>8. it: el panel de riesgo aparece con una atenuación, sin latido ni alarma |
| Resultado esperado | Los 8 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E (accesibilidad) |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-17-motion-accesible.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-17-motion-accesible.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (8/8 aprobadas) |

### CP-095 — E2E-18 · E2E-18 · La profundidad de la portada es opcional y nunca estorba

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad y accesibilidad) |
| Objetivo | Verificar en navegador el comportamiento de «E2E-18 · La profundidad de la portada es opcional y nunca estorba». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: si el fragmento de la escena falla, queda el póster y la portada sigue entera<br>2. it: en escritorio la escena se monta desde su propio fragmento<br>3. it: no descarga la escena hasta que entra en el viewport<br>4. it: con movimiento reducido: póster, sin descargar la escena<br>5. it: en móvil: póster, sin descargar la escena y sin desbordar<br>6. it: en un equipo modesto: póster<br>7. it: sin WebGL la escena se muestra igual: no depende de él<br>8. it: es decorativa: oculta, inerte y fuera del orden de tabulación |
| Resultado esperado | Los 8 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E (accesibilidad) |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-18-profundidad-portada.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-18-profundidad-portada.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (8/8 aprobadas) |

### CP-096 — E2E-19 · E2E-19 · QA visual y accesibilidad de la Fase 21

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad y accesibilidad) |
| Objetivo | Verificar en navegador el comportamiento de «E2E-19 · QA visual y accesibilidad de la Fase 21». |
| Precondiciones | Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba (`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800) |
| Datos | Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress |
| Pasos | 1. it: las páginas públicas no se desbordan a 320 px (WCAG 1.4.10)<br>2. it: cada pantalla de acceso tiene un único contenido principal<br>3. it: el enlace de salto enfocado mide al menos 24 px de alto (WCAG 2.5.8)<br>4. it: la alerta de rechazo se lee en ${tema} (WCAG 1.4.3)<br>5. it: el error de un campo y el botón destructivo se leen en ${tema}<br>6. (algunas pruebas se generan en bucle: el total ejecutado es mayor que los `it` del código) |
| Resultado esperado | Los 7 tests del spec pasan sin reintentos. |
| Tipo de prueba | UI / E2E (accesibilidad) |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `cypress/e2e/e2e-19-qa-visual-accesible.cy.js` |
| Comando | `npm run cy:run -- --spec cypress/e2e/e2e-19-qa-visual-accesible.cy.js` |
| Evidencia | docs/academico/qa-final/evidencias/09-cypress.log |
| Estado (F29F) | **APROBADO** (7/7 aprobadas) |

### CP-097 — Componente de interfaz «data-table»

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad) |
| Objetivo | Verificar el componente «data-table» de forma aislada (renderizado, accesibilidad y estados). |
| Precondiciones | Contenedor `app` healthy; entorno de pruebas de Vitest |
| Datos | Propiedades ficticias del componente |
| Pasos | 1. test: declara los roles de tabla, para que sobrevivan al display:block<br>2. test: el encabezado se recorta visualmente, nunca con display:none<br>3. test: cada celda apunta con headers a un encabezado que existe<br>4. test: dos tablas en la misma página no comparten los ids<br>5. test: hay una sola fila por registro y conserva sus data-cy<br>6. test: la etiqueta de móvil es texto real y no se anuncia dos veces<br>7. test: el pie de tabla se conserva cuando se entrega |
| Resultado esperado | Las 7 pruebas del archivo pasan. |
| Tipo de prueba | UI / componentes |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `resources/js/components/data-table.test.tsx` |
| Comando | `docker compose exec app npx vp test --run` |
| Evidencia | docs/academico/qa-final/evidencias/07-vitest.log |
| Estado (F29F) | **APROBADO** (7/7 aprobadas) |

### CP-098 — Componente de interfaz «experience-3d»

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad) |
| Objetivo | Verificar el componente «experience-3d» de forma aislada (renderizado, accesibilidad y estados). |
| Precondiciones | Contenedor `app` healthy; entorno de pruebas de Vitest |
| Datos | Propiedades ficticias del componente |
| Pasos | 1. test: con todo a favor, escena<br>2. test: sin ventana —antes de montar—, póster<br>3. test: movimiento reducido: póster, y no hay nada que lo anule<br>4. test: ahorro de datos: póster, y el fragmento no se descarga<br>5. test: pantalla angosta: póster, para no competir con el contenido<br>6. test: equipo modesto, por núcleos o por memoria: póster<br>7. test: sin composición en perspectiva: póster<br>8. test: la ausencia de WebGL no importa: la escena no lo usa<br>9. test: lo primero que se pinta es el póster, nunca la escena<br>10. test: es decorativa: oculta a la tecnología asistiva, inerte y sin eventos<br>11. test: no tiene nada que pueda recibir el foco ni un lienzo WebGL<br>12. test: ocupa la caja de la tarjeta: cambiar póster por escena no mueve la página<br>13. test: el póster no contiene información que solo esté ahí |
| Resultado esperado | Las 13 pruebas del archivo pasan. |
| Tipo de prueba | UI / componentes |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `resources/js/components/experience-3d/experience-3d.test.tsx` |
| Comando | `docker compose exec app npx vp test --run` |
| Evidencia | docs/academico/qa-final/evidencias/07-vitest.log |
| Estado (F29F) | **APROBADO** (13/13 aprobadas) |

### CP-099 — Componente de interfaz «form-controls»

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad) |
| Objetivo | Verificar el componente «form-controls» de forma aislada (renderizado, accesibilidad y estados). |
| Precondiciones | Contenedor `app` healthy; entorno de pruebas de Vitest |
| Datos | Propiedades ficticias del componente |
| Pasos | 1. test: A · conserva el aria-describedby que ya traía el control<br>2. test: B · añade la ayuda<br>3. test: C · añade el error y marca el control como inválido<br>4. test: D · combina los tres sin duplicar ni perder el orden<br>5. test: E · un error gana a un aria-invalid={false} del llamador<br>6. test: E-bis · sin error se respeta el aria-invalid del llamador<br>7. test: F · funciona igual con select y con textarea<br>8. test: sin ayuda ni error no inventa una descripción |
| Resultado esperado | Las 8 pruebas del archivo pasan. |
| Tipo de prueba | UI / componentes |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `resources/js/components/form-controls.test.tsx` |
| Comando | `docker compose exec app npx vp test --run` |
| Evidencia | docs/academico/qa-final/evidencias/07-vitest.log |
| Estado (F29F) | **APROBADO** (8/8 aprobadas) |

### CP-100 — Componente de interfaz «motion»

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad) |
| Objetivo | Verificar el componente «motion» de forma aislada (renderizado, accesibilidad y estados). |
| Precondiciones | Contenedor `app` healthy; entorno de pruebas de Vitest |
| Datos | Propiedades ficticias del componente |
| Pasos | 1. test: el botón responde a la pulsación y anima solo propiedades baratas<br>2. test: un botón deshabilitado no cede al pulsarlo<br>3. test: el error de un campo entra atenuándose, nunca sacudiéndose<br>4. test: las filas de la tabla no entran animadas: los datos no se mueven<br>5. test: los códigos de recuperación se pliegan con una altura que sí anima |
| Resultado esperado | Las 5 pruebas del archivo pasan. |
| Tipo de prueba | UI / componentes |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `resources/js/components/motion.test.tsx` |
| Comando | `docker compose exec app npx vp test --run` |
| Evidencia | docs/academico/qa-final/evidencias/07-vitest.log |
| Estado (F29F) | **APROBADO** (5/5 aprobadas) |

### CP-101 — Componente de interfaz «password-input»

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad) |
| Objetivo | Verificar el componente «password-input» de forma aislada (renderizado, accesibilidad y estados). |
| Precondiciones | Contenedor `app` healthy; entorno de pruebas de Vitest |
| Datos | Propiedades ficticias del componente |
| Pasos | 1. test: el botón está en el orden de tabulación<br>2. test: tiene nombre accesible y dice qué campo controla<br>3. test: el campo nace oculto y el icono es decorativo |
| Resultado esperado | Las 3 pruebas del archivo pasan. |
| Tipo de prueba | UI / componentes |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `resources/js/components/password-input.test.tsx` |
| Comando | `docker compose exec app npx vp test --run` |
| Evidencia | docs/academico/qa-final/evidencias/07-vitest.log |
| Estado (F29F) | **APROBADO** (3/3 aprobadas) |

### CP-102 — Componente de interfaz «visual-qa»

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 (usabilidad) |
| Objetivo | Verificar el componente «visual-qa» de forma aislada (renderizado, accesibilidad y estados). |
| Precondiciones | Contenedor `app` healthy; entorno de pruebas de Vitest |
| Datos | Propiedades ficticias del componente |
| Pasos | 1. test: la alerta destructiva escribe con el tono de peligro, no con el color que va sobre el relleno<br>2. test: el error de un campo usa el tono de peligro como texto<br>3. test: el enlace de salto conserva su relleno al recibir el foco<br>4. test: las pantallas de acceso tienen un contenido principal<br>5. test: los códigos plegados no dejan una franja visible<br>6. test: con movimiento reducido el desplazamiento es inmediato |
| Resultado esperado | Las 6 pruebas del archivo pasan. |
| Tipo de prueba | UI / componentes |
| Prioridad | Baja |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `resources/js/components/visual-qa.test.tsx` |
| Comando | `docker compose exec app npx vp test --run` |
| Evidencia | docs/academico/qa-final/evidencias/07-vitest.log |
| Estado (F29F) | **APROBADO** (6/6 aprobadas) |

### CP-103 — Servicio ML: ablation

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «ablation» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_the_four_mandatory_feature_sets_are_compared`<br>2. `test_each_ablation_removes_or_adds_exactly_one_feature`<br>3. `test_every_feature_flagged_by_the_15a_audit_is_covered`<br>4. `test_ablations_are_evaluated_on_validation`<br>5. `test_hyperparameters_are_not_retuned_per_feature_set`<br>6. `test_every_set_reports_the_comparable_metrics`<br>7. `test_deltas_are_measured_against_the_core_set`<br>8. `test_interpretation_covers_the_three_audited_features`<br>9. `test_experiment_reports_the_ablation_table` |
| Resultado esperado | Las 9 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_ablation.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_ablation.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (9/9 aprobadas) |

### CP-104 — Servicio ML: api security

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «api security» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_the_token_comes_only_from_the_environment`<br>2. `test_a_blank_token_disables_authentication`<br>3. `test_the_token_is_exactly_what_the_environment_says`<br>4. `test_the_module_reads_the_token_from_the_environment`<br>5. `test_predict_requires_the_token`<br>6. `test_model_info_requires_the_token`<br>7. `test_a_wrong_token_is_rejected`<br>8. `test_the_correct_token_is_accepted`<br>9. `test_model_info_with_the_token_is_accepted`<br>10. `test_the_rejection_does_not_echo_the_token`<br>11. `test_health_stays_open`<br>12. `test_without_a_configured_token_the_model_routes_are_closed`<br>13. `test_a_token_in_the_header_does_not_open_an_unconfigured_service`<br>14. `test_the_closed_response_reveals_no_configuration_detail`<br>15. `test_health_still_answers_without_a_configured_token`<br>16. `test_a_blank_token_also_closes_the_service`<br>17. `test_openapi_documents_the_protected_routes` |
| Resultado esperado | Las 24 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_api_security.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_api_security.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (24/24 aprobadas) |

### CP-105 — Servicio ML: api service

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «api service» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_health_reports_a_live_service_with_a_ready_model`<br>2. `test_health_separates_process_from_model`<br>3. `test_health_leaks_no_paths_or_traces`<br>4. `test_model_info_describes_the_frozen_experiment`<br>5. `test_model_info_states_the_verdict_and_the_limits`<br>6. `test_model_info_reports_gap_01_as_technically_resolved`<br>7. `test_the_openapi_description_does_not_claim_production_readiness`<br>8. `test_model_info_explains_what_the_score_is_not`<br>9. `test_model_info_exposes_no_training_data_or_paths`<br>10. `test_model_info_is_unavailable_without_a_model`<br>11. `test_predict_returns_a_probability_and_a_flag`<br>12. `test_predict_reports_the_exact_frozen_threshold`<br>13. `test_predict_identifies_the_model_that_answered`<br>14. `test_predict_is_deterministic`<br>15. `test_the_json_field_order_does_not_change_the_answer`<br>16. `test_a_different_process_gets_a_different_score`<br>17. `test_an_unknown_field_is_rejected`<br>18. `test_identifiers_are_rejected`<br>19. `test_personal_and_outcome_attributes_are_rejected`<br>20. `test_a_missing_field_is_rejected`<br>21. `test_an_empty_payload_is_rejected`<br>22. `test_a_wrong_type_is_rejected`<br>23. `test_a_decimal_count_is_rejected`<br>24. `test_nan_and_infinity_are_rejected`<br>25. `test_a_vacancy_without_positions_is_rejected`<br>26. `test_a_zero_elapsed_since_publication_is_rejected`<br>27. `test_a_negative_count_is_rejected`<br>28. `test_a_non_positive_days_remaining_is_rejected`<br>29. `test_an_impossible_day_count_is_rejected`<br>30. `test_malformed_json_is_rejected`<br>31. `test_predict_without_a_model_returns_503`<br>32. `test_the_unavailable_response_leaks_nothing`<br>33. `test_an_incompatible_artifact_keeps_the_service_unready`<br>34. `test_an_inference_failure_is_reported_without_a_trace`<br>35. `test_the_request_schema_matches_the_feature_contract`<br>36. `test_openapi_documents_the_endpoints_with_a_fictional_example`<br>37. `test_the_days_remaining_field_does_not_claim_gap_01_is_open`<br>38. `test_the_documentation_states_that_it_is_not_deployable`<br>39. `test_no_cors_headers_are_emitted` |
| Resultado esperado | Las 56 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_api_service.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_api_service.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (56/56 aprobadas) |

### CP-106 — Servicio ML: dataset distributions

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «dataset distributions» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_prevalence_sits_inside_the_simulated_band`<br>2. `test_prevalence_is_not_an_artifact_of_the_sample_size`<br>3. `test_prevalence_emerges_from_the_process_not_from_resampling`<br>4. `test_count_invariants_hold`<br>5. `test_pending_is_exactly_scheduled_minus_completed`<br>6. `test_application_counts_are_overdispersed`<br>7. `test_durations_are_right_skewed`<br>8. `test_temporal_drift_is_present_and_moderate`<br>9. `test_several_fictitious_organizations_are_present`<br>10. `test_no_organization_determines_the_target`<br>11. `test_extreme_cases_are_represented`<br>12. `test_zero_application_processes_exist`<br>13. `test_censoring_rate_is_configurable`<br>14. `test_full_validation_suite_passes`<br>15. `test_count_invariant_guard_detects_a_broken_identity`<br>16. `test_count_invariant_guard_detects_more_completed_than_scheduled`<br>17. `test_prevalence_guard_detects_an_out_of_band_dataset`<br>18. `test_extreme_case_guard_reports_a_missing_scenario`<br>19. `test_cli_generates_a_dataset_and_prints_its_lineage`<br>20. `test_cli_can_export_only_labelled_rows` |
| Resultado esperado | Las 21 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_dataset_distributions.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_dataset_distributions.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (21/21 aprobadas) |

### CP-107 — Servicio ML: dataset no leakage

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «dataset no leakage» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_events_after_the_checkpoint_do_not_change_any_feature`<br>2. `test_sessions_completed_after_the_checkpoint_are_not_counted_as_completed`<br>3. `test_no_feature_correlates_suspiciously_with_the_target`<br>4. `test_the_strongest_signal_is_informative_but_far_from_deterministic`<br>5. `test_similar_processes_can_end_differently`<br>6. `test_censored_processes_never_receive_a_label`<br>7. `test_completed_processes_always_receive_a_label`<br>8. `test_model_ready_excludes_every_censored_process`<br>9. `test_censoring_statistics_are_reported`<br>10. `test_target_is_derived_only_from_the_final_closure`<br>11. `test_leakage_guard_detects_a_target_revealing_column`<br>12. `test_censoring_guard_detects_a_labelled_censored_row`<br>13. `test_censoring_guard_detects_an_unlabelled_completed_row`<br>14. `test_stall_probability_depends_on_operational_conditions`<br>15. `test_stall_probability_rises_with_inactivity`<br>16. `test_stall_probability_is_never_deterministic`<br>17. `test_censored_and_completed_differ_without_separating_perfectly`<br>18. `test_censored_and_completed_overlap_in_the_feature_space`<br>19. `test_censoring_is_reproducible`<br>20. `test_censoring_ratio_stays_in_a_reasonable_range` |
| Resultado esperado | Las 20 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_dataset_no_leakage.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_dataset_no_leakage.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (20/20 aprobadas) |

### CP-108 — Servicio ML: dataset schema

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «dataset schema» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_columns_match_the_contract_exactly`<br>2. `test_no_forbidden_column_is_present`<br>3. `test_no_latent_factor_is_exported`<br>4. `test_known_offenders_are_detected`<br>5. `test_legitimate_operational_names_are_allowed`<br>6. `test_tokenizer_splits_names_consistently`<br>7. `test_contract_columns_are_not_flagged`<br>8. `test_identifiers_exist_only_as_metadata`<br>9. `test_linear_combination_columns_are_not_model_ready`<br>10. `test_ablation_feature_is_not_model_ready`<br>11. `test_model_ready_features_are_the_approved_set`<br>12. `test_dtypes_follow_the_contract`<br>13. `test_no_nan_where_the_contract_forbids_it`<br>14. `test_one_row_per_process`<br>15. `test_observation_status_has_only_the_two_expected_values`<br>16. `test_feature_matrix_exposes_only_model_ready_columns`<br>17. `test_validator_detects_a_forbidden_column`<br>18. `test_validator_detects_an_exported_latent_factor`<br>19. `test_validator_detects_a_wrong_dtype`<br>20. `test_validator_detects_duplicated_processes`<br>21. `test_validator_detects_negative_counts`<br>22. `test_validator_detects_a_non_positive_remaining_horizon`<br>23. `test_validator_detects_a_missing_column`<br>24. `test_validator_detects_a_wrong_target_dtype`<br>25. `test_validator_detects_nan_in_a_contractual_column`<br>26. `test_validator_detects_an_impossible_position_count`<br>27. `test_validator_detects_too_many_configured_stages`<br>28. `test_validator_detects_an_invalid_observation_status`<br>29. `test_validator_reports_a_manifest_that_does_not_declare_synthetic_data`<br>30. `test_validator_reports_an_incomplete_manifest`<br>31. `test_ablation_obligations_are_declared_for_15b` |
| Resultado esperado | Las 93 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_dataset_schema.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_dataset_schema.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (93/93 aprobadas) |

### CP-109 — Servicio ML: dataset temporal integrity

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «dataset temporal integrity» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_chronological_order_holds`<br>2. `test_checkpoint_is_the_start_of_the_day_after_applications_close`<br>3. `test_all_timestamps_are_lima_aware`<br>4. `test_target_is_fixed_before_publication_and_after_the_checkpoint`<br>5. `test_target_resolves_to_the_end_of_its_day`<br>6. `test_target_is_immutable_across_the_simulation`<br>7. `test_closure_happens_after_the_checkpoint`<br>8. `test_stalled_processes_never_close`<br>9. `test_elapsed_and_remaining_days_are_strictly_positive`<br>10. `test_checkpoints_are_parseable_and_carry_an_offset`<br>11. `test_application_window_falls_back_to_publication_when_opens_at_is_null`<br>12. `test_applications_can_open_after_publication`<br>13. `test_elapsed_is_not_universally_window_plus_one`<br>14. `test_the_residual_identity_is_explained_by_the_fallback_rule`<br>15. `test_elapsed_and_window_remain_correlated_without_being_identical` |
| Resultado esperado | Las 15 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_dataset_temporal_integrity.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_dataset_temporal_integrity.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (15/15 aprobadas) |

### CP-110 — Servicio ML: experiment freeze

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «experiment freeze» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_freeze_records_everything_needed_to_reproduce`<br>2. `test_freeze_metrics_come_from_validation_not_test`<br>3. `test_the_test_set_is_opened_exactly_once`<br>4. `test_a_sealed_test_set_refuses_an_unfrozen_record`<br>5. `test_a_persisted_freeze_opens_the_test_set`<br>6. `test_the_threshold_used_on_test_is_the_frozen_one`<br>7. `test_verdict_criteria_are_comparative_not_invented`<br>8. `test_verdict_is_one_of_the_three_allowed_outcomes`<br>9. `test_verdict_evidence_supports_the_decision`<br>10. `test_deployment_is_never_declared_while_gap_01_is_open`<br>11. `test_censoring_limitation_travels_with_the_result`<br>12. `test_organization_id_is_metadata_only`<br>13. `test_cli_runs_and_writes_evidence`<br>14. `test_cli_can_skip_the_optional_model` |
| Resultado esperado | Las 14 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_experiment_freeze.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_experiment_freeze.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (14/14 aprobadas) |

### CP-111 — Servicio ML: freeze contract

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «freeze contract» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_freeze_declares_the_full_protocol`<br>2. `test_freeze_contains_no_test_results`<br>3. `test_freeze_fingerprint_is_reproducible_and_excludes_timestamps`<br>4. `test_tampering_with_the_protocol_breaks_the_fingerprint`<br>5. `test_a_tampered_file_is_rejected_on_load`<br>6. `test_reveal_rejects_an_arbitrary_object_claiming_to_be_frozen`<br>7. `test_reveal_rejects_a_freeze_that_was_never_persisted`<br>8. `test_reveal_rejects_a_freeze_from_another_dataset`<br>9. `test_reveal_rejects_a_freeze_from_another_split`<br>10. `test_incomplete_freeze_is_rejected`<br>11. `test_incompatible_schema_version_is_rejected`<br>12. `test_predictions_can_be_rebuilt_from_the_persisted_freeze`<br>13. `test_a_rounded_threshold_can_change_a_classification`<br>14. `test_persisted_threshold_keeps_full_precision`<br>15. `test_reported_test_threshold_is_the_exact_frozen_one`<br>16. `test_test_results_reference_the_freeze`<br>17. `test_cli_writes_freeze_and_results_as_separate_artefacts`<br>18. `test_the_persisted_freeze_is_the_one_that_opened_the_test`<br>19. `test_an_aligned_and_persisted_freeze_is_accepted`<br>20. `test_reveal_rejects_a_wrong_config_fingerprint`<br>21. `test_reveal_rejects_a_nonexistent_source_path`<br>22. `test_reveal_rejects_a_source_path_pointing_to_a_directory`<br>23. `test_reveal_rejects_a_source_path_holding_a_different_freeze`<br>24. `test_reveal_rejects_a_tampered_source_file`<br>25. `test_reveal_rejects_an_empty_scientific_section`<br>26. `test_reveal_rejects_validation_metrics_without_the_primary_metric`<br>27. `test_reveal_rejects_an_empty_scalar_field`<br>28. `test_reveal_rejects_an_out_of_range_threshold`<br>29. `test_reveal_rejects_a_placeholder_threshold_selection`<br>30. `test_reveal_rejects_a_threshold_selection_without_the_threshold`<br>31. `test_reveal_rejects_a_threshold_selection_with_a_different_threshold`<br>32. `test_reveal_rejects_a_threshold_chosen_on_test`<br>33. `test_reveal_rejects_a_threshold_selection_without_a_rule`<br>34. `test_reveal_rejects_a_placeholder_calibration_decision`<br>35. `test_reveal_rejects_an_incomplete_calibration_decision`<br>36. `test_reveal_rejects_a_calibration_fitted_outside_train`<br>37. `test_the_official_freeze_does_not_adopt_calibration`<br>38. `test_reveal_rejects_a_placeholder_validation_metrics`<br>39. `test_reveal_rejects_validation_metrics_with_only_the_primary_metric`<br>40. `test_reveal_rejects_validation_metrics_missing_a_metric`<br>41. `test_reveal_rejects_a_nan_validation_metric`<br>42. `test_reveal_rejects_validation_metrics_computed_with_another_threshold`<br>43. `test_reveal_rejects_a_broken_confusion_matrix`<br>44. `test_reveal_rejects_placeholder_validation_baselines`<br>45. `test_reveal_rejects_validation_baselines_missing_one`<br>46. `test_reveal_rejects_a_baseline_without_its_metrics`<br>47. `test_reveal_rejects_placeholder_ablation_conclusions`<br>48. `test_reveal_rejects_ablation_conclusions_missing_a_required_feature`<br>49. `test_reveal_rejects_an_ablation_reading_without_a_number`<br>50. `test_reveal_rejects_a_placeholder_verdict_rule`<br>51. `test_reveal_rejects_a_verdict_rule_missing_a_criterion`<br>52. `test_the_official_verdict_rule_blocks_deployment_while_gap_01_is_open`<br>53. `test_reveal_rejects_blank_known_limitations`<br>54. `test_reveal_rejects_known_limitations_missing_a_key_topic`<br>55. `test_the_official_freeze_covers_every_required_limitation`<br>56. `test_the_official_freeze_still_passes_every_section_validator`<br>57. `test_validate_freeze_for_split_requires_the_config_fingerprint`<br>58. `test_validate_freeze_for_split_rejects_an_invalid_config_fingerprint`<br>59. `test_reveal_rejects_a_threshold_selection_without_validation_as_source`<br>60. `test_reveal_rejects_a_freeze_that_adopts_calibration`<br>61. `test_no_calibration_method_rescues_an_adopting_freeze`<br>62. `test_reveal_rejects_a_calibration_decision_incoherent_with_the_pipeline`<br>63. `test_reveal_rejects_a_section_that_is_not_an_object`<br>64. `test_reveal_rejects_a_metric_that_is_not_numeric`<br>65. `test_reveal_rejects_known_limitations_that_are_not_a_list`<br>66. `test_reveal_rejects_a_freeze_without_model_params`<br>67. `test_an_unfrozen_record_is_rejected`<br>68. `test_a_stale_fingerprint_is_rejected`<br>69. `test_reveal_rejects_an_infinite_validation_metric`<br>70. `test_reveal_rejects_a_non_string_limitation`<br>71. `test_reveal_rejects_a_freeze_without_the_concurrency_proxy_limitation` |
| Resultado esperado | Las 113 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_freeze_contract.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_freeze_contract.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (113/113 aprobadas) |

### CP-112 — Servicio ML: generator reproducibility

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «generator reproducibility» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_same_seed_and_config_produce_identical_dataset`<br>2. `test_different_seed_produces_different_dataset`<br>3. `test_changing_a_structural_parameter_changes_the_dataset`<br>4. `test_output_path_does_not_change_the_config_fingerprint`<br>5. `test_dataset_fingerprint_detects_any_content_change`<br>6. `test_manifest_records_the_lineage_required_by_phase_14`<br>7. `test_manifest_flags_configurations_outside_the_approved_profile`<br>8. `test_invalid_row_counts_are_rejected`<br>9. `test_inverted_prevalence_band_is_rejected`<br>10. `test_config_is_immutable`<br>11. `test_unknown_config_field_is_rejected`<br>12. `test_lazy_reexport_exposes_the_public_api`<br>13. `test_lazy_reexport_rejects_unknown_attributes`<br>14. `test_each_export_mode_has_its_own_fingerprint`<br>15. `test_unknown_export_mode_is_rejected`<br>16. `test_export_manifest_describes_the_exported_frame`<br>17. `test_generation_timestamp_is_excluded_from_every_fingerprint`<br>18. `test_cli_announces_the_fingerprint_of_the_written_file`<br>19. `test_cli_persists_a_manifest_next_to_the_dataset` |
| Resultado esperado | Las 22 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_generator_reproducibility.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_generator_reproducibility.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (22/22 aprobadas) |

### CP-113 — Servicio ML: metrics

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «metrics» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_perfect_separation_yields_perfect_metrics`<br>2. `test_confusion_matrix_matches_the_threshold`<br>3. `test_f2_weights_recall_more_than_f1`<br>4. `test_brier_skill_score_is_zero_for_the_reference_predictor`<br>5. `test_brier_skill_score_is_positive_when_the_model_beats_the_reference`<br>6. `test_average_precision_of_a_random_score_approaches_prevalence`<br>7. `test_calibration_report_detects_a_well_calibrated_score`<br>8. `test_calibration_report_detects_a_badly_calibrated_score`<br>9. `test_group_metrics_skip_groups_that_are_too_small`<br>10. `test_group_metrics_skip_single_class_groups` |
| Resultado esperado | Las 10 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_metrics.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_metrics.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (10/10 aprobadas) |

### CP-114 — Servicio ML: model reproducibility

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «model reproducibility» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_every_family_is_deterministic`<br>2. `test_seed_is_the_approved_one`<br>3. `test_unknown_family_is_rejected`<br>4. `test_grid_stays_small_and_reviewable`<br>5. `test_forbidden_model_families_are_absent`<br>6. `test_only_logistic_regression_is_scaled`<br>7. `test_dummy_baseline_returns_the_train_prevalence`<br>8. `test_operational_rule_is_deterministic`<br>9. `test_whole_experiment_is_reproducible`<br>10. `test_a_different_seed_changes_the_experiment` |
| Resultado esperado | Las 13 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_model_reproducibility.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_model_reproducibility.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (13/13 aprobadas) |

### CP-115 — Servicio ML: serving artifact

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «serving artifact» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_the_artifact_is_derived_from_the_frozen_protocol`<br>2. `test_the_artifact_and_its_metadata_are_written`<br>3. `test_the_artifact_is_fitted_only_on_train`<br>4. `test_metadata_records_the_library_versions`<br>5. `test_building_with_the_wrong_row_count_is_rejected`<br>6. `test_building_from_a_tampered_freeze_is_rejected`<br>7. `test_metadata_round_trips_through_disk`<br>8. `test_metadata_keeps_the_exact_threshold`<br>9. `test_metadata_with_unknown_fields_is_rejected`<br>10. `test_incomplete_metadata_is_rejected`<br>11. `test_service_metadata_states_the_limits`<br>12. `test_service_metadata_exposes_no_local_paths`<br>13. `test_a_valid_artifact_loads`<br>14. `test_a_missing_artifact_is_reported`<br>15. `test_an_artifact_without_metadata_is_rejected`<br>16. `test_an_artifact_that_does_not_match_the_freeze_is_rejected`<br>17. `test_altered_hyperparameters_are_rejected`<br>18. `test_a_threshold_mismatch_is_rejected`<br>19. `test_a_feature_order_mismatch_is_rejected`<br>20. `test_altered_library_versions_are_rejected`<br>21. `test_a_wrong_digest_is_rejected`<br>22. `test_metadata_without_a_digest_is_rejected`<br>23. `test_a_freeze_that_is_not_the_approved_one_is_rejected`<br>24. `test_a_substituted_estimator_with_predict_proba_is_rejected`<br>25. `test_a_pipeline_with_another_scaler_is_rejected`<br>26. `test_a_pipeline_with_other_hyperparameters_is_rejected`<br>27. `test_a_pipeline_fitted_on_other_features_is_rejected`<br>28. `test_a_pipeline_fitted_on_a_different_feature_order_is_rejected`<br>29. `test_an_unfitted_pipeline_is_rejected`<br>30. `test_a_pipeline_with_only_the_scaler_fitted_is_rejected`<br>31. `test_a_pipeline_with_only_the_final_estimator_fitted_is_rejected`<br>32. `test_the_official_artifact_is_fully_fitted`<br>33. `test_a_partially_fitted_artifact_never_reports_a_ready_model`<br>34. `test_the_official_artifact_passes_the_structural_check`<br>35. `test_an_incompatible_schema_version_is_rejected`<br>36. `test_a_corrupted_artifact_is_rejected`<br>37. `test_an_unreadable_binary_with_a_matching_digest_is_rejected`<br>38. `test_an_object_that_is_not_a_pipeline_is_rejected`<br>39. `test_unreadable_metadata_is_rejected`<br>40. `test_a_missing_freeze_is_reported`<br>41. `test_a_tampered_freeze_blocks_the_load`<br>42. `test_prediction_is_deterministic`<br>43. `test_prediction_survives_a_reload`<br>44. `test_the_json_order_does_not_change_the_prediction`<br>45. `test_the_frame_is_built_in_the_frozen_order`<br>46. `test_missing_features_are_reported`<br>47. `test_the_score_is_a_probability`<br>48. `test_the_flag_uses_the_exact_threshold`<br>49. `test_a_pipeline_fitted_without_feature_names_is_rejected` |
| Resultado esperado | Las 57 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_serving_artifact.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_serving_artifact.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (57/57 aprobadas) |

### CP-116 — Servicio ML: serving cli

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «serving cli» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_the_cli_builds_the_artifact`<br>2. `test_the_cli_fails_cleanly_on_a_wrong_row_count`<br>3. `test_the_schema_guard_accepts_the_current_contract`<br>4. `test_the_schema_guard_detects_a_divergence`<br>5. `test_the_builder_rejects_a_freeze_that_is_not_the_approved_one`<br>6. `test_the_builder_records_the_binary_digest`<br>7. `test_an_inference_failure_is_wrapped`<br>8. `test_metadata_read_rejects_a_file_with_missing_fields` |
| Resultado esperado | Las 8 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_serving_cli.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_serving_cli.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (8/8 aprobadas) |

### CP-117 — Servicio ML: stage history semantics

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «stage history semantics» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_a_single_application_produces_at_least_one_history_entry`<br>2. `test_every_application_before_the_checkpoint_contributes_its_initial_history`<br>3. `test_applications_after_the_checkpoint_do_not_count`<br>4. `test_additional_transitions_add_to_the_initial_history`<br>5. `test_transitions_after_the_checkpoint_are_excluded`<br>6. `test_a_process_without_applications_has_no_stage_history`<br>7. `test_stage_transitions_never_fall_below_applications`<br>8. `test_processes_without_applications_report_no_transitions`<br>9. `test_transitions_exceed_applications_when_the_process_advances`<br>10. `test_counts_are_non_negative` |
| Resultado esperado | Las 11 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_stage_history_semantics.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_stage_history_semantics.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (11/11 aprobadas) |

### CP-118 — Servicio ML: temporal split

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «temporal split» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_partitions_respect_the_approved_ratios`<br>2. `test_train_precedes_validation_precedes_test`<br>3. `test_no_process_appears_in_two_partitions`<br>4. `test_every_labelled_row_lands_in_exactly_one_partition`<br>5. `test_censored_processes_never_enter_the_split`<br>6. `test_split_is_deterministic`<br>7. `test_ordering_is_by_checkpoint_with_a_deterministic_tie_break`<br>8. `test_summary_reports_what_the_documentation_needs`<br>9. `test_test_labels_are_not_disclosed_before_the_reveal`<br>10. `test_boundary_note_does_not_claim_strict_inequality`<br>11. `test_reveal_count_is_scoped_to_the_current_run`<br>12. `test_an_unlabelled_frame_is_rejected`<br>13. `test_the_split_cannot_be_built_without_a_config_fingerprint`<br>14. `test_an_empty_config_fingerprint_is_rejected`<br>15. `test_an_empty_dataset_fingerprint_is_rejected`<br>16. `test_a_malformed_fingerprint_is_rejected`<br>17. `test_a_sealed_test_set_cannot_be_built_without_a_valid_config` |
| Resultado esperado | Las 20 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_temporal_split.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_temporal_split.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (20/20 aprobadas) |

### CP-119 — Servicio ML: threshold selection

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «threshold selection» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_selected_point_dominates_the_operational_baseline`<br>2. `test_rule_does_not_degenerate_into_alerting_on_everything`<br>3. `test_selection_maximises_f2_within_the_eligible_region`<br>4. `test_fallback_is_flagged_when_no_threshold_dominates`<br>5. `test_selection_is_deterministic`<br>6. `test_decision_records_the_rule_and_its_provenance`<br>7. `test_precision_recall_table_is_small_and_ordered`<br>8. `test_operational_rule_parameters_are_the_documented_ones`<br>9. `test_operational_rule_matches_its_formula`<br>10. `test_threshold_in_the_experiment_is_selected_on_validation_only` |
| Resultado esperado | Las 10 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_threshold_selection.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_threshold_selection.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (10/10 aprobadas) |

### CP-120 — Servicio ML: training no leakage

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RF-29 (EXPERIMENTAL / PROPUESTO) |
| Objetivo | Verificar «training no leakage» del servicio de riesgo operacional, que no evalúa ni clasifica personas. |
| Precondiciones | Entorno virtual `ml-service/.venv` (Python 3.12.5) |
| Datos | Dataset sintético del experimento; sin PII |
| Pasos | 1. `test_scaler_is_fitted_only_with_train`<br>2. `test_validation_is_only_transformed_never_refitted`<br>3. `test_sealed_test_cannot_be_opened_without_a_freeze`<br>4. `test_describing_the_test_partition_does_not_count_as_opening_it`<br>5. `test_no_feature_set_contains_metadata_or_target`<br>6. `test_no_feature_set_contains_a_forbidden_column`<br>7. `test_identifiers_never_reach_the_matrix`<br>8. `test_raw_timestamps_are_not_used_as_features`<br>9. `test_unknown_feature_set_is_rejected`<br>10. `test_building_the_target_rejects_unlabelled_rows`<br>11. `test_missing_feature_columns_are_reported` |
| Resultado esperado | Las 17 ejecuciones pasan. |
| Tipo de prueba | ML experimental |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `ml-service/tests/test_training_no_leakage.py` |
| Comando | `cd ml-service && .venv/Scripts/python.exe -m pytest tests/test_training_no_leakage.py` |
| Evidencia | docs/academico/qa-final/evidencias/08b-pytest.log; docs/academico/qa-final/evidencias/pytest-junit.xml |
| Estado (F29F) | **APROBADO** (17/17 aprobadas) |

### CP-121 — Tipos de TypeScript del frontend

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-09 (mantenibilidad) |
| Objetivo | Verificar: tipos de typescript del frontend. |
| Precondiciones | Contenedores healthy |
| Datos | No aplica |
| Pasos | 1. Ejecutar `docker compose exec app npx tsc --noEmit` |
| Resultado esperado | 0 errores de tipos |
| Tipo de prueba | Estática / build |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `docker compose exec app npx tsc --noEmit` |
| Comando | `docker compose exec app npx tsc --noEmit` |
| Evidencia | docs/academico/qa-final/evidencias/05-tsc.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-122 — Compilación del frontend

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-09 (mantenibilidad) |
| Objetivo | Verificar: compilación del frontend. |
| Precondiciones | Contenedores healthy |
| Datos | No aplica |
| Pasos | 1. Ejecutar `docker compose exec app npm run build` |
| Resultado esperado | Build terminado sin errores |
| Tipo de prueba | Estática / build |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `docker compose exec app npm run build` |
| Comando | `docker compose exec app npm run build` |
| Evidencia | docs/academico/qa-final/evidencias/06-build.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-123 — Configuración de Docker Compose

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-09 (mantenibilidad) |
| Objetivo | Verificar: configuración de docker compose. |
| Precondiciones | Contenedores healthy |
| Datos | No aplica |
| Pasos | 1. Ejecutar `docker compose config --quiet` |
| Resultado esperado | Configuración válida |
| Tipo de prueba | Estática / build |
| Prioridad | Media |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `docker compose config --quiet` |
| Comando | `docker compose config --quiet` |
| Evidencia | docs/academico/qa-final/evidencias/03-compose-config.log |
| Estado (F29F) | **APROBADO** (1/1 aprobadas) |

### CP-124 — Integración continua (GitHub Actions `tests`)

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-09 |
| Objetivo | Verificar que cada push a `develop` y `main` ejecuta build, TypeScript y PHPUnit en verde. |
| Precondiciones | Push a `develop` o `main` |
| Datos | Los de PHPUnit |
| Pasos | 1. Consultar la ejecución del workflow `tests` del commit probado |
| Resultado esperado | Ejecución `success` |
| Tipo de prueba | Regresión / CI |
| Prioridad | Alta |
| Automatización | AUTOMATIZADA |
| Prueba automática asociada | `.github/workflows/tests.yml` |
| Comando | `GitHub Actions (automático)` |
| Evidencia | docs/academico/qa-final/evidencias/ci-github-actions.json |
| Estado (F29F) | **APROBADO en develop (bc44303); main (60ebcb2): sin ejecución — pendiente de ejecución manual** (1/1 aprobadas) |

### CP-125 — Recorrido visual por rol en navegador

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-05 |
| Objetivo | Recorrer las pantallas de cada rol y detectar errores visibles, HTTP o de JavaScript. |
| Precondiciones | Según el caso |
| Datos | Ficticios |
| Pasos | 1. Procedimiento manual |
| Resultado esperado | Recorrer las pantallas de cada rol y detectar errores visibles, HTTP o de JavaScript. |
| Tipo de prueba | Aceptación (manual) |
| Prioridad | Media |
| Automatización | MANUAL / NO AUTOMATIZADO |
| Prueba automática asociada | — |
| Comando | — |
| Evidencia | docs/manual-smoke-test.md |
| Estado (F29F) | **EJECUTADO EN LA FASE 8 (13/09/2026): 10/10; no repetido en la F29F** (0/0 aprobadas) |

### CP-126 — Aceptación por el usuario institucional (RR. HH. / Dirección del Colegio)

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | Validación institucional |
| Objetivo | Confirmar con el Colegio que el TO-BE y el sistema responden a su proceso real. |
| Precondiciones | Según el caso |
| Datos | Ficticios |
| Pasos | 1. Procedimiento manual |
| Resultado esperado | Confirmar con el Colegio que el TO-BE y el sistema responden a su proceso real. |
| Tipo de prueba | Aceptación (manual) |
| Prioridad | Media |
| Automatización | MANUAL / NO AUTOMATIZADO |
| Prueba automática asociada | — |
| Comando | — |
| Evidencia | — |
| Estado (F29F) | **NO EJECUTADO: sin validación institucional (fuera de alcance)** (0/0 aprobadas) |

### CP-127 — Rendimiento y carga

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-06 |
| Objetivo | Medir tiempos de respuesta con usuarios concurrentes frente a un objetivo definido. |
| Precondiciones | Según el caso |
| Datos | Ficticios |
| Pasos | 1. Procedimiento manual |
| Resultado esperado | Medir tiempos de respuesta con usuarios concurrentes frente a un objetivo definido. |
| Tipo de prueba | No funcional |
| Prioridad | Media |
| Automatización | MANUAL / NO AUTOMATIZADO |
| Prueba automática asociada | — |
| Comando | — |
| Evidencia | — |
| Estado (F29F) | **NO EJECUTADO: sin herramienta de carga ni SLA (RNF-06 NO VERIFICADO)** (0/0 aprobadas) |

### CP-128 — Disponibilidad y recuperación

| Campo | Valor |
|---|---|
| RF relacionado | — |
| CU relacionado | — |
| Referencia transversal | RNF-07 |
| Objetivo | Verificar la continuidad del servicio y la restauración desde respaldos. |
| Precondiciones | Según el caso |
| Datos | Ficticios |
| Pasos | 1. Procedimiento manual |
| Resultado esperado | Verificar la continuidad del servicio y la restauración desde respaldos. |
| Tipo de prueba | No funcional |
| Prioridad | Media |
| Automatización | MANUAL / NO AUTOMATIZADO |
| Prueba automática asociada | — |
| Comando | — |
| Evidencia | — |
| Estado (F29F) | **NO EJECUTADO: sin entorno de producción (RNF-07 NO VERIFICADO)** (0/0 aprobadas) |
