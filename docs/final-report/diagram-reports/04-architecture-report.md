# Informe de arquitectura

## 1. Propósito

Describir la arquitectura lógica de la plataforma: capas, módulos, componentes y cómo se garantizan multiempresa, autorización, colas y auditoría.

**Disponibilidad:** no hay un diagrama de arquitectura lógica original en el repositorio ni en la carpeta del curso. Existe el diagrama de despliegue (`deploydiagrama.oom`), analizado en [09-deployment-report.md](09-deployment-report.md). La arquitectura se describe por escrito a partir del código y del [capítulo 7](../07-arquitectura-tecnologica.md).

## 2. Elementos principales

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| Interfaz | React 19 + TypeScript + Tailwind 4 (shadcn/ui) | Páginas por módulo y rol (`resources/js/pages`) |
| Puente SPA | Inertia 3 | Renderiza páginas React desde controladores Laravel sin API REST separada |
| Aplicación | Laravel 13 (PHP 8.4) | Rutas, Form Requests, Policies, controladores delgados |
| Dominio | Servicios y *enums* | Reglas de negocio y máquinas de estado por módulo |
| Persistencia | PostgreSQL 17 | Datos por `organization_id`, integridad declarativa, auditoría de solo inserción |
| Sesiones, caché y colas | Redis 7 | Sesiones, caché y cola de notificaciones |
| Worker | `php artisan queue:work` | Entrega de notificaciones (base de datos + correo con *driver* `log`) |
| Archivos | Disco local privado | CV en PDF con nombre UUID |
| Ejecución | Docker Compose | Entorno reproducible (normal y E2E) |

**Módulos del monolito** (`app/Http/Controllers/<Módulo>`, `app/Services/<Módulo>`):
- `JobRequests`
- `Vacancies`
- `Candidates`
- `Applications`
- `Assessments`
- `Ranking`/`Evaluation`
- `Selection`
- `Audit`
- `Notifications`
- `Testing` (soporte E2E protegido)

## 3. Relación con requerimientos

- La arquitectura soporta RF-01 a RF-27 y los RNF de seguridad, aislamiento, trazabilidad, mantenibilidad y portabilidad ([capítulo 4, sección 4.3](../04-requerimientos.md#43-requerimientos-no-funcionales)).
- **Multiempresa:** transversal a todos los RF de personal.
- **Colas:** RF-04, RF-11, RF-15, RF-17 y RF-26.
- **Auditoría:** RF-27.

## 4. Relación con implementación

- **Monolito modular:** una aplicación Laravel; los módulos comparten modelo de datos y transacciones.
- **Multiempresa:**
  - *Trait* `BelongsToOrganization` con `OrganizationScope` (*scope* global y asignación de `organization_id`).
  - Policies que verifican rol y organización (`sharesOrganizationWith`).
  - El postulante tiene cuenta global (A-04).
- **Autorización:** 7 Policies (`JobRequest`, `Vacancy`, `Application`, `Evaluation`, `Interview`, `CandidateDocument`, `AuditLog`) y middleware `role`.
- **Colas:** `RecruitmentNotification` (`ShouldQueue`, `afterCommit`); servicio Docker `queue` con *healthcheck*.
- **Auditoría:** `AuditLogger` (claves sensibles eliminadas), tabla `audit_logs` con *trigger* `audit_logs_append_only` y vista `audit/index` (solo Aprobador/Dirección).
- **Decisión humana:** `RankingService` puro (no escribe); la decisión solo entra por `FinalDecisionService` con `VacancyPolicy::decide`.

## 5. Consistencias

- Laravel 13, React/Inertia, PostgreSQL 17, Redis 7, Docker y el worker de colas existen y están en uso.
- El aislamiento multiempresa se verifica en PHPUnit (`CrossTenantAccessTest`, `OrganizationScopeTest` y pruebas por RF) y en E2E-11.

## 6. Diferencias detectadas

Sin diagrama lógico original no hay diferencias gráficas que reportar. Frente a descripciones previas del despliegue:
- **S3:** no existe; se usa almacenamiento local privado.
- **HTTPS:** no está configurado en el entorno local.

## 7. Limitaciones

**Implementado:** todo lo descrito en las secciones 2 y 4.

**Mejoras futuras (no implementadas):**
- RLS de PostgreSQL;
- CI/CD;
- almacenamiento en la nube (S3/R2);
- monitoreo de errores (Sentry);
- búsqueda (Meilisearch);
- IA;
- microservicios o Kubernetes;
- imagen de producción.

## 8. Estado para entrega

**Vigente** (descripción escrita basada en el código).

## 9. Recomendación

Si se requiere una figura para el informe, elaborarla a partir de este texto y del capítulo 7. Mantener separadas la arquitectura implementada y las mejoras futuras.
