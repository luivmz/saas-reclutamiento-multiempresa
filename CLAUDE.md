# SaaS Reclutamiento Multiempresa — contexto del proyecto

Plataforma SaaS multiempresa para reclutamiento, evaluación y selección de personal. Caso de estudio: Colegio Andino de Huancayo. Proyecto académico de la Universidad Continental, curso Pruebas y Calidad de Software, NRC 28607, docente Dr. Maglioni Arana Caparachin. Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio.

Stack real: Laravel 13 (PHP 8.4) + React 19 + TypeScript + Inertia 3 + Tailwind 4, PostgreSQL 17, Redis 7, PHPUnit, Cypress 15 y Docker Compose.

## Antes de cambiar cualquier cosa

**Usa la skill `project-guardian`.** Define el procedimiento obligatorio: qué leer primero, en qué rama trabajar, qué pruebas exigir y cuándo detenerse. Las demás skills del proyecto se apoyan en ella:

| Skill | Cuándo |
|---|---|
| `project-guardian` | Siempre, antes de editar o planificar |
| `laravel-saas-quality` | Backend Laravel: controladores, servicios, Policies, migraciones, pruebas |
| `academic-traceability` | Documentación, trazabilidad RF y entregables del curso |
| `powerdesigner-uml` | Diagramas UML/PlantUML derivados del código real |
| `ml-risk-service` | Diseño del servicio de riesgo operacional (aún **no implementado**) |
| `recruitment-3d-experience` | 3D público y progresivo (aún **no implementado**) |

Skills externas instaladas (ver `PROVENANCE.md` de cada una): `frontend-design`, `animate` y `reviewing-a11y`.

## Contratos inviolables

1. **RF-01 a RF-27 conservan su número y su significado.** No se renumeran, eliminan ni reinterpretan.
2. **El sistema nunca selecciona, descarta ni contrata automáticamente.** El ranking calcula, ordena y compara; nada más.
3. **La decisión final pertenece al Aprobador/Dirección**, con confirmación humana explícita y justificación (RF-23).
4. **Cualquier ML futuro será informativo y operacional**, sobre el proceso, nunca evaluando, puntuando ni clasificando personas.
5. **Se preservan la multiempresa (`organization_id`), las Policies, los roles y las pruebas cross-tenant.**
6. **Se preserva la auditoría segura y de solo inserción** (`AuditLogger` + trigger `audit_logs_append_only`).
7. **Solo datos ficticios.** Nunca datos personales reales ni PII.
8. **Nunca se versionan secretos** (`.env`, `.env.e2e`, tokens, claves).
9. **El tag `v1.0.0-academic` (`9a946c2`) no se mueve, borra ni reutiliza**, y la historia de v1.0 no se reescribe.
10. **Sin `push`, `merge`, release ni tag sin autorización explícita del equipo.**

## Documentación fuente

No dupliques estos documentos: enlázalos.

| Tema | Documento |
|---|---|
| Estado por fase | `docs/PROGRESS.md` |
| Trazabilidad RF-01 a RF-27 | `docs/final-report/traceability-master.md` · `docs/rf-implementation-matrix.md` |
| Decisiones de negocio (A-01…A-36) | `docs/assumptions.md` |
| Defectos (DEF-01…DEF-13) | `docs/defects.md` |
| Evidencia TDD | `docs/tdd-evidence.md` |
| Entorno y Docker | `docs/docker.md` |
| Suite E2E | `docs/testing/cypress-e2e.md` |
| Usuarios demo ficticios | `docs/demo-users.md` |
| Informe académico (14 capítulos) e informes de diagramas | `docs/final-report/` |
| Planificación v1.1 | `docs/v1.1/` |

## Comandos habituales

Todo corre en Docker; no hay PHP ni Node locales del proyecto.

```
docker compose up -d --wait                                   # levantar
docker compose exec app php artisan test                      # PHPUnit (244 pruebas)
docker compose exec app npm run build                         # compilar frontend
docker compose exec app npx tsc --noEmit                      # tipos
npm run cy:run                                                # Cypress (entorno E2E aislado)
docker compose exec app php artisan migrate:fresh --seed --force   # datos demo
```

## Estado actual

v1.0 está publicada: `main` y `develop` tienen el mismo contenido y el tag `v1.0.0-academic` marca el release académico. La Fase 13 abre v1.1 y es **solo gobierno y documentación**: no hay ML, FastAPI, rediseño de frontend, motion, 3D ni UML definitivo aprobados. RF-28 y los RNF nuevos existen únicamente como **candidatos** en `docs/v1.1/scope-preliminary.md`.

## Permisos

No amplíes permisos por comodidad. `.claude/settings.local.json` es local y no se versiona; cualquier cambio de permisos, instalación global de skills o ejecución de hooks externos requiere autorización explícita del equipo.
