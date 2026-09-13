# Capítulo 7. Arquitectura tecnológica

## 7.1 Stack real

Versiones leídas de `composer.lock`, del árbol `npm ls` y de los contenedores en ejecución (Fase 10/11).

| Capa | Tecnología | Versión |
|---|---|---|
| Lenguaje backend | PHP | 8.4.25 (imagen `php:8.4.25-cli-bookworm`) |
| Framework backend | Laravel | 13.31.0 |
| Autenticación | Laravel Fortify | 1.39.0 |
| Puente SPA | Inertia (`inertiajs/inertia-laravel` / `@inertiajs/react`) | 3.3.4 / 3.7.1 |
| Rutas tipadas | Laravel Wayfinder | 0.1.21 |
| Frontend | React / React DOM | 19.3.0 |
| Lenguaje frontend | TypeScript | 5.9.3 |
| Estilos | Tailwind CSS (componentes shadcn/ui) | 4.3.3 |
| Empaquetado | Vite / vite-plus | 8.3.0 / 0.3.0 |
| Base de datos | PostgreSQL | 17.11 (alpine) |
| Sesiones, caché y colas | Redis (extensión phpredis 6.3.0) | 7.4.11 (alpine) |
| Contenedores | Docker Compose | Validado con Docker 27.4.0 y Compose 2.31 |
| Pruebas backend | PHPUnit | 12.5.35 |
| Pruebas E2E | Cypress (navegador Electron 136) | 15.3.0 |
| Control de versiones | Git | Repositorio local |
| Herramientas en la imagen | Composer / Node / npm | 2.10.3 / 22.23.2 / 10.9.8 |

**No implementado** (no existe en el código):
- Cloudflare R2 o S3: los CV usan disco local privado.
- Meilisearch, IA o recomendaciones automáticas.
- Kubernetes y microservicios.
- Facturación.
- Sentry.
- RLS de PostgreSQL.
- CI/CD.

## 7.2 Estilo arquitectónico: monolito modular SaaS multiempresa

Una sola aplicación Laravel organizada por dominios. Las páginas React se sirven mediante Inertia, sin una API REST separada. Los dominios son:
- requerimientos;
- vacantes;
- postulantes;
- postulaciones;
- evaluaciones;
- ranking;
- selección;
- notificaciones;
- auditoría.

| Carpeta | Responsabilidad |
|---|---|
| `app/Http/Controllers/<Módulo>` | Controladores delgados: autorizan, delegan en un servicio y responden con Inertia o redirección |
| `app/Http/Requests` | Validación en el servidor (Form Requests) |
| `app/Policies` | Autorización por rol y organización |
| `app/Services/<Módulo>` | Reglas de negocio y transacciones (p. ej., `FinalDecisionService`, `RankingService`) |
| `app/Enums` | Estados, transiciones permitidas, roles y etiquetas (`HasPresentation`) |
| `app/Models` | Eloquent; `BelongsToOrganization` en las entidades de una organización |
| `app/Notifications` | Notificaciones en cola (base de datos + correo con *driver* `log`) |
| `resources/js/pages/<módulo>` | Páginas Inertia/React |
| `database/migrations` | Esquema PostgreSQL con restricciones de integridad |

## 7.3 Multiempresa (tenancy)

- **`organization_id`:** las entidades de negocio (requerimientos, vacantes, criterios, postulaciones, sesiones, resultados, decisiones, historiales y auditoría) tienen `organization_id` no nulo, salvo la auditoría de cuentas globales.
- **Scope global:** el *trait* `BelongsToOrganization` aplica `OrganizationScope`, que limita las consultas a la organización del usuario autenticado cuando este pertenece a una. Además, completa `organization_id` al crear.
- **Autorización en el backend:** además del *scope*, cada Policy comprueba el rol y que el usuario comparta organización con el recurso (`sharesOrganizationWith`). Un identificador ajeno responde 403 o 404 y no produce efectos (`CrossTenantAccessTest`, E2E-11).
- **Postulante global:** la cuenta del postulante no pertenece a ninguna organización (A-04). Una organización solo ve sus datos a través de postulaciones a **sus** vacantes.
- **RLS:** PostgreSQL Row Level Security **no está implementado**. El aislamiento se aplica en la capa de aplicación; RLS queda como recomendación de defensa en profundidad.

## 7.4 Autorización y seguridad en el backend

- **Policies:** `JobRequestPolicy`, `VacancyPolicy` (incluye `decide`, `registerSelection` y `close`), `ApplicationPolicy`, `EvaluationPolicy`, `InterviewPolicy`, `CandidateDocumentPolicy` y `AuditLogPolicy`.
- **Reglas destacadas:**
  - `decide` exige el rol **aprobador** y la misma organización: RR. HH. no puede registrar la decisión final.
  - La auditoría solo la consulta el aprobador (A-33).
- **Errores de negocio:** `BusinessRuleException` responde como error de validación (clave `workflow`), con aviso en la interfaz, y no se reporta como fallo del sistema.
- **Resto de controles** (CSRF, límite de intentos de inicio de sesión, archivos privados, secretos): [capítulo 5, sección 5.7](05-planificacion-calidad.md#57-seguridad-aplicada).

## 7.5 PostgreSQL

- Base principal `reclutamiento`, base de pruebas `reclutamiento_testing` y base E2E `reclutamiento_e2e`.
- Integridad declarativa: `CHECK` de estados y rangos, `UNIQUE` compuestos, FK con `restrict`/`cascade`/`null` según el caso e índice único parcial (un único `seleccionado` por vacante).
- Metadatos de auditoría en `jsonb` y *trigger* de solo inserción.
- Las pruebas usan PostgreSQL real, no SQLite, para validar restricciones e índices del mismo motor (A-03).

## 7.6 Redis y colas

- **Uso de Redis:** sesiones (`SESSION_DRIVER=redis`), caché (`CACHE_STORE=redis`) y colas (`QUEUE_CONNECTION=redis`).
- **Bases lógicas:**

  | Entorno | Sesiones y cola | Caché |
  |---|---|---|
  | Normal | DB 0 | DB 1 |
  | E2E | DB 2 | DB 3 |

- **Notificaciones:** heredan de `RecruitmentNotification` (`ShouldQueue`, `afterCommit`). Las procesa el servicio `queue` (`php artisan queue:work redis --tries=3 --max-time=3600`), que tiene su propio *healthcheck*.
- Encolar tras el *commit* evita notificar operaciones revertidas y contribuye a la idempotencia del resultado final (A-32).

## 7.7 Auditoría

- **Registro:** `AuditLogger::record(acción, entidad, metadatos, actor)` guarda la organización, el actor, la acción (`AuditAction`, 23 acciones de negocio), la entidad polimórfica (*morph map* obligatorio), los metadatos saneados y la IP.
- **Datos excluidos:** contraseñas, tokens, secretos, cookies, cabeceras de autorización, API keys y contenido de archivos (DEF-08).
- **Inmutabilidad:** *trigger* PostgreSQL `audit_logs_append_only` (DEF-07). Solo se permite poner `user_id` en nulo al eliminar una cuenta (A-34).
- **Consulta:** `audit/index`, de solo lectura, filtrada por organización y con resumen legible mediante lista blanca (A-33, DEF-10).

## 7.8 Decisión humana en la arquitectura

`RankingService` es un servicio puro:
- recibe criterios y puntajes;
- devuelve posiciones, totales, desglose por criterio, empates y candidatos incompletos;
- **no escribe en la base de datos**.

La única ruta que registra una decisión es `POST /vacantes/{id}/decision`: `VacancyPolicy::decide` → `FinalDecisionRequest` (confirmación humana y justificación) → `FinalDecisionService`. Aun así, la decisión **no cambia estados**: la selección la aplica RR. HH. después (RF-24).

## 7.9 Arquitectura de despliegue

Entorno reproducible de desarrollo y demostración con Docker Compose (servicios `app`, `queue`, `postgres`, `redis` y el perfil `e2e`). No hay infraestructura de producción ni en la nube. Detalle en el [capítulo 10](10-dockerizacion.md) y en `docs/docker.md`.
