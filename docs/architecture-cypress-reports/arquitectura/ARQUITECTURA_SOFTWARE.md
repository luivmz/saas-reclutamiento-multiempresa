# Arquitectura de software

> Actividad 1 de la *Guía Práctica INDIVIDUAL de Arquitectura*. Describe la arquitectura **real** del repositorio en la rama `chore/sonarqube-macos-setup` (HEAD `41a830c` más el working tree de esta práctica, 09/11/2026). Cada afirmación remite a un archivo verificable.

## 1. Tipo de arquitectura

| Rasgo | Valor real | Evidencia |
|---|---|---|
| Estilo principal | **Monolito modular** en Laravel 13: un solo despliegue (`app`) con módulos por dominio en `app/Http/Controllers/*`, `app/Services/*`, `app/Policies/*` | `routes/web.php`, árbol `app/` |
| Modelo de interacción | **Cliente–servidor**: navegador ↔ servidor HTTP Laravel | `docker-compose.yml` (servicio `app`, puerto 8000) |
| Integración frontend/backend | **Integrados mediante Inertia 3**: el servidor responde *props* JSON y el cliente React las renderiza; no hay una API REST pública separada | `Inertia::render(...)` en los controladores; `resources/js/app.tsx` |
| Producto | **SaaS multiempresa** con aislamiento lógico por `organization_id` en una base de datos compartida | `app/Models/Concerns/BelongsToOrganization.php`, `app/Models/Scopes/OrganizationScope.php` |
| Procesamiento asíncrono | Worker de colas (`queue`) para notificaciones, sobre Redis | `docker-compose.yml` (servicio `queue`), `app/Notifications/RecruitmentNotification.php` |
| Servicio periférico opcional | Microservicio experimental FastAPI (RF-29) **fuera** de Compose, consultado por HTTP solo si `ML_SERVICE_ENABLED=true` | `app/Services/Ml/MlRiskClient.php`, `ml-service/` |

No es una arquitectura de microservicios: el negocio completo (requerimientos → vacantes → postulaciones → evaluación → comparación → decisión humana → cierre → auditoría → reportes) vive en un único proceso Laravel. El servicio ML es un componente auxiliar, desactivado por defecto (`ML_SERVICE_ENABLED=false` en el `.env` local), y la aplicación funciona igual sin él.

## 2. Capas y componentes principales

Todo el backend sigue la cadena obligatoria del proyecto (skill `laravel-saas-quality`):

```
Ruta (+ middleware auth/role) → Form Request (autorización y validación) → Controller delgado → Service → Model/Enum → PostgreSQL
                                                                              ↘ AuditLogger (append-only)
                                                                              ↘ Notification (cola Redis)
```

| Capa | Componentes reales | Responsabilidad |
|---|---|---|
| Presentación (cliente) | `resources/js/pages/**` (React 19 + TypeScript), `layouts/`, `components/` (DataTable, Section, StatusBadge…) | Renderizar las páginas Inertia, formularios y tablas accesibles |
| Contrato cliente–servidor | Inertia 3 + Wayfinder (`resources/js/actions`, `routes` generados) | Tipar rutas/acciones del servidor en TypeScript |
| Entrada HTTP | `routes/web.php`, `routes/settings.php`, middleware `auth`, `role:`, `HandleInertiaRequests` | Enrutar en español (`/vacantes`, `/reportes`) y compartir datos de sesión |
| Validación | `app/Http/Requests/**` | Validar en servidor con mensajes en español |
| Autorización | `app/Policies/**` + `Gate::define('viewRecruitmentReports')` | Rol **y** organización para cada acción |
| Aplicación/dominio | `app/Services/**` (JobRequestWorkflow, VacancyService, ApplicationStageService, AssessmentScheduler, RankingService, FinalDecisionService, VacancyClosureService, **RecruitmentReportService**) | Reglas de negocio, transiciones, transacciones |
| Modelo | `app/Models/**`, `app/Enums/**` (estados con `allowedTransitions()`) | Relaciones, casts y máquinas de estado |
| Persistencia | PostgreSQL 17 (`database/migrations`, `CHECK`, FK, trigger append-only) | Integridad de datos |
| Transversales | `AuditLogger`, notificaciones, Fortify (2FA, passkeys) | Auditoría, avisos, seguridad de acceso |

## 3. Módulos funcionales y responsabilidades

| Módulo | RF | Controladores / servicios | Roles |
|---|---|---|---|
| Requerimientos de personal | RF-01 a RF-04 | `JobRequestController`, `JobRequestTransitionController`, `JobRequestWorkflow` | Solicitante, RR. HH., Aprobador |
| Vacantes y publicación | RF-05 a RF-07 | `VacancyController`, `VacancyPublicationController`, `VacancyService` | RR. HH. (Aprobador consulta) |
| Portal público y postulación | RF-08 a RF-11 | `PublicVacancyController`, `ApplyController`, `CandidateProfileController`, `CandidateCvController` | Postulante |
| Postulaciones y etapas | RF-12 a RF-15 | `VacancyApplicationController`, `ApplicationStageController`, `ApplicationStageService` | RR. HH. |
| Evaluación y entrevista | RF-16 a RF-20 | `AssessmentScheduleController`, `EvaluationController`, `InterviewController` | RR. HH., Evaluador |
| Comparación y ranking | RF-21, RF-22 | `VacancyComparisonController`, `RankingService` | RR. HH., Aprobador |
| Decisión humana, selección y cierre | RF-23 a RF-26 | `FinalDecisionController`, `SelectionRegistrationController`, `VacancyClosureController` | Aprobador decide; RR. HH. registra y cierra |
| Auditoría | RF-27 | `AuditLogController`, `AuditLogger` | Aprobador |
| Riesgo operacional (experimental) | RF-29 (candidato) | `VacancyOperationalRiskController`, `OperationalRiskService` | RR. HH., Aprobador |
| **Reportes de reclutamiento (nuevo)** | **RF-28 (candidato)** | **`RecruitmentReportController`, `RecruitmentReportService`** | **RR. HH., Aprobador** |

RF-28 ya figuraba en [`docs/v1.1/scope-preliminary.md`](../../v1.1/scope-preliminary.md) como «Panel operativo de seguimiento de convocatorias: etapas, tiempos y cuellos de botella, sin datos de personas». Esta práctica lo **implementa**, pero implementarlo **no** lo promueve al baseline (decisión 11): RF-01 a RF-27 no cambian. El detalle del módulo está en [`../reportes/MODULO_REPORTES.md`](../reportes/MODULO_REPORTES.md).

Fuera de alcance por diseño: contratación, planillas, evaluación de desempeño y eliminación de registros de negocio (las rutas `resource` se declaran `->except('destroy')` para preservar la trazabilidad y la auditoría).

## 4. Comunicación entre componentes (flujo UI → backend → BD)

1. El navegador solicita una URL (`GET /reportes?desde=…`). En navegación interna, Inertia envía la petición por XHR con la cabecera `X-Inertia`.
2. Laravel resuelve la ruta y aplica el middleware `auth` (sesión en Redis).
3. En Reportes, el Form Request llama primero al Gate desde `authorize()` (rol + organización), antes de validar y de invocar el controlador. La ubicación de una Policy puede variar en otros flujos. Una autorización rechazada responde 403; una validación inválida redirige con errores.
4. El controlador delega en un servicio; el servicio consulta los modelos Eloquent, sobre los que actúa `OrganizationScope`.
5. PostgreSQL ejecuta la consulta; el servicio arma un arreglo de datos.
6. `Inertia::render('pagina', props)` devuelve JSON (XHR) o HTML con el JSON embebido (primera carga); React actualiza la vista.
7. Las acciones críticas escriben además en `audit_logs` y encolan notificaciones en Redis, que procesa el worker `queue`.

## 5. Multitenencia y aislamiento por organización

- **Modelo de datos**: toda entidad de negocio lleva `organization_id` con FK (`organizations`). El postulante es global (`organization_id = null`).
- **Scope global**: `BelongsToOrganization` registra `OrganizationScope`, que añade `where organization_id = <org del usuario>` a toda consulta de un usuario de personal, y asigna la organización al crear registros.
- **Policies**: comparan rol **y** organización (`$user->sharesOrganizationWith($model)`).
- **Validaciones**: las referencias cruzadas usan `Rule::exists(...)->where('organization_id', …)`. Así, una vacante de otra organización no se puede usar ni como filtro de reportes.
- **Defensa en profundidad del módulo de reportes**: además del scope, cada consulta del `RecruitmentReportService` filtra explícitamente `organization_id`, incluida la subconsulta sobre `application_stage_histories`.
- **Pruebas cross-tenant**: `tests/Feature/Tenancy/*`, `tests/Feature/Reports/RecruitmentReportTest.php` (`test_rf28_reports_never_include_records_of_another_organization`, `test_rf28_vacancy_of_another_organization_cannot_be_used_as_filter`) y Cypress `e2e-11-multitenancy`, `e2e-20-reports`.

## 6. Autenticación

Laravel Fortify (`config/fortify.php`): registro, restablecimiento de contraseña, **autenticación en dos pasos** y **passkeys** (`@laravel/passkeys`). Sesiones en Redis (`SESSION_DRIVER=redis`). La verificación de correo está desactivada, y por eso hay 8 pruebas PHPUnit omitidas (comportamiento documentado en los informes previos).

## 7. Autorización

Cinco roles (`app/Enums/UserRole.php`): Área solicitante, Recursos Humanos, Aprobador/Dirección, Evaluador y Postulante. La autorización combina:

- middleware `role:` para pantallas de un solo rol (por ejemplo `role:postulante`);
- Policies por modelo (`VacancyPolicy`, `ApplicationPolicy`, `AuditLogPolicy`…);
- un Gate sin modelo para los reportes: `viewRecruitmentReports` → `RecruitmentReportPolicy::view` (RR. HH. o Aprobador **con** organización).

**Contrato inviolable**: el sistema nunca selecciona, descarta ni contrata automáticamente. El ranking calcula, ordena y compara; la decisión final la registra el Aprobador con justificación (RF-23). Los reportes solo agregan.

## 8. Auditoría

`App\Services\Audit\AuditLogger` registra las acciones críticas con metadatos sin datos sensibles. La tabla `audit_logs` es **append-only** por el trigger `audit_logs_append_only` (migración `make_audit_logs_append_only`). La consulta del módulo de reportes es de solo lectura y no constituye una acción crítica, así que no se audita.

## 9. Datos

PostgreSQL 17.11 en el contenedor `postgres`. Tablas de negocio: `organizations`, `users`, `job_requests` (+ historial), `vacancies`, `job_profiles`, `evaluation_criteria`, `candidate_profiles`, `candidate_documents`, `applications`, `application_stage_histories`, `evaluations`, `interviews` (+ resultados), `selection_decisions`, `audit_logs` y `notifications`. Infraestructura: `jobs`, `cache`, `passkeys`.

Bases separadas por propósito: `reclutamiento` (demo), `reclutamiento_testing` (PHPUnit, forzada en `phpunit.xml`) y `reclutamiento_e2e` (Cypress, reiniciada por `/__e2e/reset`). **Solo datos ficticios** (`DemoSeeder`, factories).

El módulo de reportes lee `applications`, `application_stage_histories` y `vacancies`, sin tablas nuevas y sin migraciones.

## 10. APIs e integraciones externas

| API o servicio | Funcionalidad | Información intercambiada | Justificación | Estado |
|---|---|---|---|---|
| Servicio de riesgo operacional (FastAPI propio, `ml-service/`, puerto 8008) | Estimar el riesgo de demora del **proceso** de una vacante (RF-29) | Envía *features* agregadas del proceso de la vacante; recibe una probabilidad y metadatos del modelo. Nunca datos de personas | Apoyo informativo a la gestión del plazo (GAP-01) | **Experimental y desactivado** por defecto (`ML_SERVICE_ENABLED=false`). Con fallback: sin servicio, la página funciona |

**No hay APIs de terceros** (pagos, geolocalización, mensajería, BI externo). Justificación:

- El proceso termina en la preselección o la selección interna; no hay cobros, logística ni ubicación que geolocalizar.
- Las notificaciones usan los canales `database` y `mail` de Laravel (`RecruitmentNotification::via`), procesados por la cola. En el entorno académico el correo está configurado como `MAIL_MAILER=log`: no se envían mensajes reales, en coherencia con el contrato de «solo datos ficticios». Conectar un proveedor SMTP real sería una decisión de despliegue, no una integración de negocio.
- Los reportes se calculan **dentro** del monolito sobre PostgreSQL. Una herramienta de BI externa duplicaría los datos y obligaría a sacar información del perímetro multiempresa sin una necesidad funcional.

Por eso los componentes internos se comunican por **llamadas en proceso** (controlador → servicio → modelo), **SQL** hacia PostgreSQL, **Redis** para sesión, caché y colas, y **HTTP/JSON (Inertia)** hacia el navegador. Siguiendo la guía, no se agregó una API artificial.

## 11. Diagramas

Ver [`DIAGRAMAS_REFERENCIA.md`](DIAGRAMAS_REFERENCIA.md): se reutilizan `01_ARQUITECTURA_GENERAL_SAAS` y `06_MAPA_MODULOS_SAAS`, y se agrega solo la vista de componentes del módulo nuevo (`17_MODULO_REPORTES_COMPONENTES`).
