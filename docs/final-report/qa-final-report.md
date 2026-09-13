# Informe de QA final (Fase 12)

## Datos de la verificación

| Campo | Valor |
|---|---|
| Fecha | 2026-09-13 |
| Rama | `release/qa-final` (creada desde `develop` en `904ce72`, merge de la Fase 11) |
| Commit auditado | `904ce72`, más el commit de QA de esta fase (solo documentación) |
| Entorno | Windows 11 + Docker 27.4.0 (Compose 2.31); servicios `app`, `queue`, `postgres` 17.11, `redis` 7.4.11, `app-e2e`, `queue-e2e`; Cypress 15.3.0 (Electron 136) |
| Identidad Git | `user.name` y `user.email` configurados (no modificados) |
| Alcance | Funcionalidad, RF, pruebas, frontend, multiempresa, autorización, decisión humana, Docker, datos, secretos, documentación, diagramas, Git |

## 1. Requerimientos funcionales (RF-01 a RF-27)

Verificación directa sobre rutas (`route:list`: 92 rutas; las 33 asociadas a RF existen), controladores, servicios, Policies, modelos, páginas React, PHPUnit y Cypress.

| RF | Estado | RF | Estado | RF | Estado |
|---|---|---|---|---|---|
| RF-01 | ✅ | RF-10 | ✅ | RF-19 | ✅ |
| RF-02 | ✅ | RF-11 | ✅ | RF-20 | ✅ |
| RF-03 | ✅ | RF-12 | ✅ | RF-21 | ✅ |
| RF-04 | ✅ | RF-13 | ✅ | RF-22 | ✅ |
| RF-05 | ✅ | RF-14 | ✅ | RF-23 | ✅ |
| RF-06 | ✅ | RF-15 | ✅ | RF-24 | ✅ |
| RF-07 | ✅ | RF-16 | ✅ | RF-25 | ✅ |
| RF-08 | ✅ | RF-17 | ✅ | RF-26 | ✅ |
| RF-09 | ✅ | RF-18 | ✅ | RF-27 | ✅ |

**Resultado:** 27/27 implementados, sin RF adicionales. Cada RF tiene backend, prueba PHPUnit y, cuando corresponde, interfaz.

**Observaciones:**
- RF-25 implementa solo el cierre con selección, conforme a la línea base (A-30).
- RF-04 (notificación de rechazo) y RF-17 (contenido de la convocatoria) verifican parte de su comportamiento solo en PHPUnit; en Cypress se ejercen los flujos que los disparan.
- Ninguno es parcial respecto a la línea base.

## 2. PHPUnit

| Métrica | Resultado |
|---|---|
| Total | 244 |
| Superadas | 236 |
| Fallidas | **0** |
| Omitidas | 8 (*starter kit*: funciones de Fortify desactivadas, A-01) |
| Aserciones | 1074 |
| Duración | 32,25 s |

## 3. Cypress (entorno E2E aislado)

| Métrica | Resultado |
|---|---|
| Specs | 14 |
| Tests | 43 |
| Superados | 43 |
| Fallidos | **0** |
| Omitidos | 0 |
| Navegador | Electron 136 (*headless*) |
| Duración | 03:32 (sin reintentos) |

## 4. Build y TypeScript

- `npm run build`: correcto (19,90 s).
- `npx tsc --noEmit`: 0 errores.

## 5. Docker y *healthchecks*

`docker compose --profile e2e ps`: `app`, `queue`, `postgres`, `redis`, `app-e2e` y `queue-e2e` en estado **healthy**. La instalación reproducible desde un clon limpio se validó en la Fase 10 ([capítulo 10](10-dockerizacion.md)): arranque en 87 s, migraciones, *seed*, *smoke*, PHPUnit y Cypress en verde. En esta fase no hubo cambios de configuración Docker.

## 6. Migraciones

`php artisan migrate:status`: **17 aplicadas, 0 pendientes**, tanto en el entorno normal (`reclutamiento`) como en el E2E (`reclutamiento_e2e`). No se destruyó la base de desarrollo.

## 7. *Seed* y datos demo

- **Reproducibilidad:** `DemoSeeder` se ejecuta en cada reset E2E (`migrate:fresh --seed`), y los 14 specs pasaron sobre esos datos.
- **Base de desarrollo** (sin re-sembrar):
  - organizaciones «Colegio Andino de Huancayo (Demo)» y «Organización Demo B»;
  - 16 usuarios, **0 correos fuera de dominios `.test`**;
  - los 8 usuarios del guion de demostración presentes;
  - 7 CV, todos PDF ficticios.
- **Datos personales:** el esquema no contiene DNI ni fecha de nacimiento (A-15). No hay datos personales reales.

## 8. Prueba de humo

| Comprobación | Resultado |
|---|---|
| `GET /health` | 200 · `{"status":"ok","checks":{"database":"ok","redis":"ok"}}`: aplicación, PostgreSQL y Redis disponibles |
| `GET /login` | 200 |
| `GET /empleos` | 200 |
| Ruta autenticada `/dashboard` sin sesión | 302 → `/login` (guardia activa); acceso autenticado verificado en E2E-01 (5 roles) |
| Worker de colas | `queue` *healthy*; `queue:monitor redis:default` sin trabajos atascados |
| `POST /__e2e/reset` en el entorno normal | 404 |
| `app-e2e`: `/health` y reset sin token | 200 y 403 |

## 9. Multiempresa

Implementación: `organization_id` + `OrganizationScope` + Policies (`sharesOrganizationWith`). **No hay RLS de PostgreSQL** (mejora futura).

| Aspecto | Evidencia |
|---|---|
| A no lee B | `OrganizationScopeTest`, `CrossTenantAccessTest`, E2E-11 (listados e IDs ajenos → 403/404) |
| A no modifica B | `CrossTenantAccessTest::test_rf20_hr_of_other_organization_cannot_modify_vacancy_criteria`, E2E-11 (preselección, cierre y decisión sobre IDs ajenos rechazados sin efecto) |
| Auditoría aislada | `test_rf27_organization_never_sees_audit_logs_of_another_organization`, E2E-11 |
| Postulaciones y ranking aislados | `test_rf21_application_of_another_tenant_is_never_ranked_even_if_linked_to_the_vacancy` |
| Evaluaciones y entrevistas aisladas | `InterviewTest::test_evaluator_of_another_organization_cannot_access_the_interview`; `test_rf16_evaluator_must_be_an_evaluator_of_the_same_organization` |
| Decisiones aisladas | `test_rf23_candidate_of_another_tenant_is_rejected`, `test_rf23_approver_of_another_organization_cannot_decide`, `test_rf24_hr_of_another_organization_cannot_register_the_selection`, `test_rf25_hr_of_another_organization_cannot_close_the_vacancy` |
| Notificaciones aisladas | `test_rf26_closing_a_vacancy_of_another_organization_does_not_notify_this_organization_candidates` |

## 10. Autorización

Roles existentes: `solicitante`, `rrhh`, `aprobador`, `evaluador`, `postulante`. No existen otros.

| Verificación | Evidencia |
|---|---|
| Acceso válido por rol y menú correcto | E2E-01 (5 roles), `RoleMiddlewareTest` |
| 403 en pantallas de otros roles | E2E-12: solicitante → `/auditoria` y `/vacantes`; postulante → `/requerimientos` y `/mis-evaluaciones`; evaluador → `/auditoria` |
| 403 en acciones no permitidas | E2E-12: RR. HH. y evaluador → `POST /vacantes/{id}/decision`; PHPUnit: `test_rf16_only_hr_can_schedule_evaluations`, `test_rf23_only_the_approver_can_record_the_decision`, `test_rf24_only_hr_can_register_the_selection`, `test_rf25_only_hr_can_close_the_vacancy`, `test_rf27_unauthorized_roles_cannot_view_the_audit_trail`, `test_rf09_staff_cannot_use_candidate_profile_routes` |

## 11. Regla crítica de decisión humana

| Afirmación | Código | Pruebas | Interfaz | Documentación |
|---|---|---|---|---|
| El ranking calcula, ordena y compara | `RankingService` (puro), `VacancyComparisonController` | `RankingServiceTest` (14), `RankingComparisonTest` | `selection/comparison` (fórmula, desglose, posición) | Capítulos 3, 6 y 7 |
| El ranking NO selecciona | `RankingService` no escribe en la base de datos | `test_rf23_calculating_the_ranking_never_selects_a_candidate`, E2E-08 | Aviso «El ranking es un apoyo…» | Capítulos 1, 3, 4 y 12; README |
| Decide el Aprobador/Dirección | `VacancyPolicy::decide` | `test_rf23_only_the_approver_can_record_the_decision`, E2E-12 | Panel de decisión solo visible para el aprobador | Capítulo 4 (RF-23, A-27) |
| Requiere acción humana explícita | `FinalDecisionRequest` (confirmación + justificación) | `test_rf23_explicit_human_confirmation_and_justification_are_required`, E2E-09 | Casilla de confirmación y justificación | Capítulo 4, sección 4.5 |
| Puede elegir a alguien distinto del n.º 1 | `FinalDecisionService` | `test_rf23_approver_may_choose_a_candidate_who_is_not_first_in_the_ranking`, E2E-09 (elige al 2.º) | Radios para todos los finalistas | Capítulos 3 y 4 |
| La selección ocurre después | `SelectionRegistrationService` exige decisión | `test_rf24_selection_requires_a_recorded_human_decision`, E2E-10 | «Registrar selección» tras la decisión | Informe 08 |
| El cierre ocurre después | `VacancyClosureService` exige selección | `test_rf25_closure_without_a_registered_selection_is_rejected`, E2E-10 | «Cerrar convocatoria» tras la selección | Informe 08 |

**Resultado:** código, pruebas, interfaz y documentación coinciden. El único artefacto discrepante es el diagrama UML preliminar de selección (sección 15), clasificado como preliminar.

## 12. Auditoría

- `AuditLogger` elimina claves sensibles.
- *Trigger* `audit_logs_append_only` (DEF-07).
- Vista `audit/index` de solo lectura para el Aprobador/Dirección, con lista blanca de detalles.
- Pruebas: `AuditTrailTest` (5), `AuditLogViewTest` (7), `AuditLoggerTest`.
- E2E-13 verifica las acciones de decisión, selección, cierre y notificación en la auditoría.

## 13. Archivos subidos (CV)

- Solo PDF de hasta 5 MB, en disco privado `storage/app/private` con nombre UUID; descarga autorizada por `CandidateDocumentPolicy` (A-12).
- Pruebas: `test_rf09_cv_is_stored_privately_with_a_safe_generated_name` y `test_rf09_cv_rejects_invalid_type_and_oversized_files`; E2E-05 (carga real).
- **Ningún CV está versionado:** `storage/app/private/*` está ignorado por Git.

## 14. Secretos

| Verificación | Resultado |
|---|---|
| `.env`, `.env.e2e` versionados | No (0 archivos; ignorados por `.gitignore` y `.dockerignore`) |
| Logs, *dumps*, *backups*, claves `.pem`/`.key`, `auth.json` versionados | No (0). Los únicos `.sql` versionados son los scripts de creación de bases, sin datos |
| CV privados, capturas y resultados de Cypress versionados | No (0) |
| Búsqueda de `password`/`token`/`secret`/`api_key` con valor (valores enmascarados) | 3 coincidencias, ninguna secreta: nombre de variable en `cypress.config.cjs`, token ficticio de `E2eSupportTest` y token de ejemplo del *starter kit* en `PasswordResetTest` |
| Asignaciones en `.env.example` y `.env.e2e.example` | Valores de desarrollo o nulos (`DB_PASSWORD=secret`, `REDIS_PASSWORD=null`, `MAIL_PASSWORD=null`, `E2E_TOKEN=` vacío) |
| Secretos en la documentación | No (sin `APP_KEY`, tokens ni contraseñas reales) |

**Nota de trazabilidad (Fase 9):** un token E2E local, no versionado, se imprimió una vez en la terminal durante una prueba manual. Se rotó de inmediato y, desde la Fase 10, el token se genera en `.env.e2e`. No afecta al repositorio.

## 15. Documentación e informes de diagramas

- **Estructura:** 14 capítulos, README, `docs/docker.md`, `docs/testing/cypress-e2e.md`, matriz maestra, índice de evidencias, resumen técnico, guion de demo, checklist y este informe.
- **Enlaces:** 0 enlaces relativos rotos (validación de la Fase 11; nuevos enlaces revisados en esta fase).
- **Datos académicos:** NRC 28607, docente e integrantes coinciden en README, capítulo 1 y la interfaz pública. No hay NRC incorrectos en la documentación vigente.
- **Stack:** MySQL, Pest, Playwright, R2/S3, Meilisearch, microservicios, RLS, IA, Sentry y Kubernetes solo aparecen como no implementados o como trabajo futuro.
- **Referencias:** con fecha de consulta 13 de septiembre de 2026; sin DOI ni autores inventados.

**Informes escritos de diagramas** (`docs/final-report/diagram-reports/`):

| Informe | Artefacto original | Estado para entrega |
|---|---|---|
| 01 BPMN AS-IS | No versionado | Evidencia externa pendiente (AS-IS preliminar) |
| 02 BPMN TO-BE | No versionado | Evidencia externa pendiente (TO-BE propuesto documentado por escrito) |
| 03 Casos de uso | No versionado | Vigente con observaciones (catálogo derivado) |
| 04 Arquitectura | Sin diagrama lógico original | Vigente (descripción escrita) |
| 05 Modelo de clases | Sin diagrama de clases original | Vigente (descripción escrita) |
| 06 Secuencia de postulación | `SaaS Reclutamiento - Diagramas UML.oom` | Vigente con observaciones |
| 07 Secuencia de evaluación | `secuencioaEvaluacion.oom` | Vigente con observaciones |
| 08 Secuencia de selección | `seleccionl_3.oom` | **Preliminar / pendiente de actualización gráfica** (RR. HH. selecciona y cierra en un paso; la implementación separa ranking → comparación → decisión del Aprobador → selección → cierre) |
| 09 Despliegue | `deploydiagrama.oom` | Vigente con observaciones (S3 y HTTPS no implementados; falta el perfil E2E) |

No se editaron los `.oom` ni se generaron BPMN nuevos.

## 16. Defectos

`docs/defects.md`: DEF-01 a DEF-13, todos reales (detectados por pruebas, *build*, *healthcheck*, navegador o revisión) y **cerrados**. El estado coincide con el código: las pruebas asociadas pasan en esta corrida. Severidades coherentes (crítica: 2, alta: 5, media: 4, baja: 2). **El QA final no encontró defectos nuevos.**

## 17. Evidencias visuales recomendadas para el informe

No se versionan capturas automáticamente. Hay capturas locales de la Fase 8 (`storage/app/smoke/`, no versionadas). Se recomienda capturarlas de nuevo tras `migrate:fresh --seed` para el informe final:

| Evidencia | Captura local disponible | Acción |
|---|---|---|
| Login | `guest-04-login.png` | Reutilizar o recapturar |
| Requerimiento | `req-02-list.png`, `dir-02-request-decision.png` | Reutilizar o recapturar |
| Vacante | `hr-06-vacancy-draft.png`, `hr-05-vacancy-create.png` | Reutilizar o recapturar |
| Postulación | `new-02-job-complete-profile.png`, `flow-05-applied.png` | Reutilizar o recapturar |
| Evaluación | `eva-03-evaluation-pending.png` | Reutilizar o recapturar |
| Entrevista | `eva-04-interview-completed.png` | Reutilizar o recapturar |
| Ranking | `hr-13-comparison-pending.png` | Reutilizar o recapturar |
| Decisión | `dir-03-comparison-decision.png`, `flow-09-final-decision.png` | Reutilizar o recapturar |
| Auditoría | `dir-04-audit.png`, `flow-12-audit.png` | Reutilizar o recapturar |
| Cypress | No disponible (la suite solo captura en fallos) | **Capturar a mano** la tabla «Run Finished» de `npm run cy:run` |
| Docker | No disponible | **Capturar a mano** `docker compose ps` y `curl http://localhost:8000/health` |

## 18. Guion de demostración

`demo-script.md` usa escenarios del `DemoSeeder` que la suite Cypress ejercita en esta misma corrida:
- aprobación del requerimiento validado (E2E-03);
- publicación de la vacante en borrador (E2E-04);
- postulación del postulante nuevo (E2E-05);
- evaluación pendiente de Claudia Vilca (E2E-07);
- ranking 85.5 / 83.5 / 68.5 (E2E-08);
- decisión eligiendo al 2.º (E2E-09);
- selección y cierre (E2E-10).

Duración estimada: unos 11 minutos (8 minutos omitiendo los pasos opcionales). Requiere `migrate:fresh --seed` previo, como indica el guion.

## 19. Git

- **Ramas preservadas:**
  - `main` (`e87ef39`);
  - `develop` (`904ce72`);
  - `release/qa-final`;
  - 11 ramas `feature/*`: `tenancy-roles`, `job-requests-vacancies`, `candidates-applications`, `evaluations-interviews`, `ranking-selection-closure`, `notifications-audit`, `frontend-integral`, `cypress-e2e`, `docker-portability`, `final-documentation`.
- **Historia:** cada fase se fusionó en `develop` con `--no-ff`.
- **Estado remoto:** sin remoto, sin `push`, sin *tag* y sin merge a `main`.

## 20. Riesgos

| Riesgo | Impacto | Tratamiento |
|---|---|---|
| BPMN AS-IS/TO-BE y documentos previos (casos de uso, análisis) no están en el repositorio | Anexos A, B y C incompletos en el informe académico | El equipo debe anexarlos; los informes escritos 01–03 lo declaran |
| Diagrama UML de selección preliminar, discrepante con la implementación | Confusión si se presenta sin contexto | Informe 08 lo clasifica como preliminar y remite a RF-21 a RF-25 y a las pruebas |
| Sin hechos institucionales verificados del colegio | El docente podría pedir sustento | Toda la documentación rotula el AS-IS como preliminar y el TO-BE como propuesto |
| Métricas no medidas (cobertura, rendimiento, DAST) | Evaluación de calidad incompleta en esas dimensiones | Declaradas explícitamente como no medidas; recomendaciones en el capítulo 14 |
| Imagen Docker de desarrollo | No apta para producción | Declarado (A-36); fuera de alcance |
| La demo depende del estado de los datos | Demo fallida si no se re-siembra | Paso de preparación y plan B en el guion |

## 21. Pendientes

1. Anexar los BPMN AS-IS y TO-BE y los documentos previos de casos de uso (equipo).
2. Seleccionar o recapturar las capturas del informe, incluidas Cypress y Docker (equipo).
3. Actualizar gráficamente los diagramas de selección y despliegue (opcional, futura versión).
4. Cierre Git y publicación en GitHub: merge a `main`, *tag* y `push`, **bajo revisión humana**.

## Veredicto

# APTO PARA PUBLICACIÓN

**Justificación.** Se cumplen todas las condiciones obligatorias del QA final con evidencia real de esta corrida:

- RF-01 a RF-27 implementados y probados (27/27, sin RF extra);
- PHPUnit **0 fallidas** (244 pruebas, 236 superadas);
- Cypress **0 fallidos** (43/43);
- *build* correcto y TypeScript sin errores;
- migraciones al día;
- datos demo ficticios y reproducibles;
- servicios *healthy* y *smoke test* correcto;
- aislamiento multiempresa y autorización verificados;
- regla de decisión humana coherente en código, pruebas, interfaz y documentación;
- **ningún secreto versionado**.

Los pendientes identificados son **evidencias académicas externas** (BPMN originales, casos de uso previos, capturas) y mejoras futuras declaradas. No afectan a la integridad, seguridad ni reproducibilidad del repositorio. Deben completarse en el informe académico antes de la entrega formal.
