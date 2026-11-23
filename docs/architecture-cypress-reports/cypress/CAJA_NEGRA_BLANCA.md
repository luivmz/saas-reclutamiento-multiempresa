# Caja negra y caja blanca en el SaaS de reclutamiento

> Marco conceptual tomado de la *Guía desarrollo de pruebas blanca y negra*, usada **solo como referencia**: definiciones y la idea de ficha por prueba. No se copian su caso de estudio, sus tablas ni sus capturas; las fichas de abajo se rediseñaron para este proyecto.

- **Caja negra.** Se observa el sistema desde fuera: entradas por la interfaz o HTTP, salidas visibles y códigos de estado, sin mirar el código. En este proyecto la cumplen los escenarios **Cypress**, que manejan la aplicación real en un navegador ([`ESCENARIOS_CYPRESS.md`](ESCENARIOS_CYPRESS.md)).
- **Caja blanca.** Las pruebas se diseñan a partir del código: se recorren caminos, condiciones y ramas internas con entradas elegidas para ejercer cada una. Aquí lo hacen las pruebas **PHPUnit** (unitarias y Feature sobre PostgreSQL real) y **Vitest** (utilidades TS). La cobertura Clover de PHPUnit, importada en SonarQube, mide qué líneas de `app/` ejecutaron.

Cypress **no** se usa como caja blanca: no conoce ni inspecciona las ramas del código.

## 1. Fichas de caja negra (Cypress)

Ficha adaptada: *entrada → salida observable*, con el **canal** por el que fluye el dato (formulario, pantalla, HTTP) y la **estructura** que viaja.

| Ficha | Entrada | Canal | Estructura que viaja | Salida esperada / observada | Spec |
|---|---|---|---|---|---|
| CN-01 Inicio de sesión válido | correo y contraseña demo de RR. HH. | Formulario `/login` | `email`, `password` (sesión, cookie) | Redirige a `/dashboard` y muestra el menú del rol | `e2e-01-login` |
| CN-02 Credenciales inválidas | correo válido y contraseña incorrecta | Formulario `/login` | `email`, `password` | Mensaje de error, permanece en `/login`, `/dashboard` responde 302 | `e2e-01-login` |
| CN-03 Registro con campos vacíos | formulario de requerimiento vacío | Formulario | campos obligatorios | Errores de validación; no se crea el registro | `e2e-02-register-job-request` |
| CN-04 Reporte con filtro por vacante | `vacante=3` | Formulario de filtros → `GET /reportes` | `desde`, `hasta`, `vacante`, `estado` | KPI de postulaciones = 3; finalistas = 3; 1 fila en la tabla | `e2e-20-reports` |
| CN-05 Reporte de otra organización | RR. HH. de B pide `?vacante=<id de A>` | URL | parámetro `vacante` | Redirige a `/reportes`, muestra el error de validación y solo datos de B | `e2e-20-reports` |
| CN-06 Rol sin permiso | evaluador pide `/reportes` | HTTP | sesión | 403 y sin entrada de menú | `e2e-20-reports` |

## 2. Fichas de caja blanca (PHPUnit y Vitest)

Ficha adaptada: *camino interno → condición → dato de prueba → resultado*.

### 2.1 Módulo de reportes (`RecruitmentReportService` y `RecruitmentReportRequest`)

| Ficha | Camino / condición del código | Dato de prueba elegido para ejercerla | Resultado esperado | Prueba |
|---|---|---|---|---|
| CB-01 | `reached_shortlist = shortlisted_at !== null \|\| status ∈ AFTER_SHORTLIST`: **rama 1** (hay historial) | Postulación **descartada** después de haber sido preseleccionada (historial con `to_status = preseleccionado`) | Cuenta como preseleccionada (aunque su etapa actual sea `descartado`) | `test_rf28_indicators_are_calculated_from_stored_records` |
| CB-02 | Misma condición, **rama 2** (sin historial, etapa posterior) | Postulación `en_evaluacion` sin registro de historial | Cuenta como preseleccionada | idem |
| CB-03 | Misma condición, **ambas falsas** | Postulación `postulado` | No cuenta | idem y `test_rf28_vacancy_and_status_filters_narrow_every_section` |
| CB-04 | `rate()`: `total > 0 ? round(…) : null` | Organización sin postulaciones | `shortlist_rate = null`, `average_per_vacancy = null` (la UI muestra «—») | `test_rf28_empty_organization_shows_zeros_instead_of_errors` |
| CB-05 | `rate()` con total > 0 y parte 0 | Julio 2026: 1 postulación sin preselección | `shortlist_rate = 0`, `average_days_to_shortlist = null` | `test_rf28_period_filter_changes_indicators_charts_and_table` |
| CB-06 | `byWeek()`: bucle semanal desde el lunes de `desde` y relleno con ceros | Período 12/08–09/11/2026 | Primera semana `2026-08-10`, última `2026-11-09`, suma = 5 | `test_rf28_charts_and_table_group_the_same_filtered_records` |
| CB-07 | `period()`: valores por defecto (hoy − 89 días, hoy) | Petición sin parámetros, reloj fijado en 09/11/2026 | `desde = 2026-08-12`, `hasta = 2026-11-09` | `test_rf28_hr_and_approver_open_the_reports_module` |
| CB-08 | `after()`: rango > 731 días | 2024-01-01 a 2026-11-09 | Error en `desde` | `test_rf28_filters_are_validated` |
| CB-09 | Regla `hasta after_or_equal:desde`, `date_format`, `Rule::enum` | Rango invertido, `desde=ayer`, `estado=contratado` | Error en `hasta`, `desde` y `estado` respectivamente | idem |
| CB-10 | `Rule::exists(vacancies)->where(organization_id)->whereNot(borrador)` | Id de una vacante de la organización B | Error de validación en `vacante`; redirige a `reports.index` | `test_rf28_vacancy_of_another_organization_cannot_be_used_as_filter` |
| CB-11 | `where('applications.organization_id', $org)` + `OrganizationScope` | Postulaciones de A y B en el mismo período | A ve 6; B ve 3 y su propia vacante | `test_rf28_reports_never_include_records_of_another_organization` |
| CB-12 | `RecruitmentReportPolicy::view`: `organization_id !== null && rol ∈ {rrhh, aprobador}` | Invitado, solicitante, evaluador y postulante | 302 a login y 403, respectivamente | `test_rf28_unauthorized_roles_cannot_open_the_reports_module` |
| CB-13 | `reportQuery()` (TS): filtra valores vacíos o en blanco | `vacante: ''`, `desde: ' '` | Se omiten de la URL | `reports.test.tsx` |
| CB-14 | `barRatio()` (TS): ramas `value <= 0`, `max <= 0` y tope en 1 | `(0,10)`, `(5,0)`, `(12,10)` | 0, 0, 1 | `reports.test.tsx` |

### 2.2 Caminos internos ya cubiertos por la suite existente (referencia)

| Ficha | Código | Condición interna | Prueba |
|---|---|---|---|
| CB-15 | `ApplicationStatus::allowedTransitions()` | Cada par origen→destino permitido o prohibido (máquina de estados) | `tests/Unit/Enums/ApplicationStatusTest::test_transition_rules` (proveedor de datos) |
| CB-16 | `ApplicationStatus::manualTargets()` | Seleccionado/no seleccionado nunca se asignan a mano (RF-23 humana) | `ApplicationStatusTest::test_selection_outcomes_are_not_manual_targets` |
| CB-17 | Policies con `sharesOrganizationWith` | Rol correcto pero de otra organización → denegado | `tests/Feature/Tenancy/CrossTenantAccessTest` (7 casos) |
| CB-18 | `OrganizationScope::apply` | Usuario de personal → `where organization_id`; postulante → sin scope | `tests/Feature/Tenancy/OrganizationScopeTest` |
| CB-19 | Trigger `audit_logs_append_only` | `UPDATE`/`DELETE` rechazados en la base de datos | `AuditTrailTest::test_rf27_audit_logs_are_append_only_at_database_level` |
| CB-20 | `RankingService` | Ponderación, candidatos incompletos y desempates | `tests/Unit/Ranking/RankingServiceTest` |

**Medición de caja blanca.** En el análisis SonarQube V3 de esta práctica, la cobertura Clover de PHPUnit sobre `app/` y la de los archivos nuevos del módulo se reportan en [`../sonarqube/RESULTADOS_SONARQUBE.md`](../sonarqube/RESULTADOS_SONARQUBE.md).
