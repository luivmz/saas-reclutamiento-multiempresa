# SaaS Reclutamiento Multiempresa — contexto del proyecto

Plataforma SaaS multiempresa para reclutamiento, evaluación y selección de personal. Caso de estudio: Colegio Andino de Huancayo. Proyecto académico de la Universidad Continental, curso Pruebas y Calidad de Software, NRC 28607, docente Dr. Maglioni Arana Caparachin. Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio.

Stack real: Laravel 13 (PHP 8.4) + React 19 + TypeScript + Inertia 3 + Tailwind 4, PostgreSQL 17, Redis 7, PHPUnit, Cypress 15 y Docker Compose. En `develop` (v1.1) se suma el servicio experimental `ml-service/`: Python, scikit-learn y FastAPI, con `pytest`.

## Antes de cambiar cualquier cosa

**Usa la skill `project-guardian`.** Define el procedimiento obligatorio: qué leer primero, en qué rama trabajar, qué pruebas exigir y cuándo detenerse. Las demás skills del proyecto se apoyan en ella:

| Skill | Cuándo |
|---|---|
| `project-guardian` | Siempre, antes de editar o planificar |
| `laravel-saas-quality` | Backend Laravel: controladores, servicios, Policies, migraciones, pruebas |
| `academic-traceability` | Documentación, trazabilidad RF y entregables del curso |
| `powerdesigner-uml` | Diagramas UML/PlantUML derivados del código real |
| `ml-risk-service` | Servicio de riesgo operacional (RF-29): **implementado en `develop` como experimental** (Fases 15–17); marco, fronteras y evidencia exigida |
| `recruitment-3d-experience` | 3D público y progresivo: **implementado y acotado** a la portada con CSS 3D (Fase 20); condiciones para ampliarlo |

Skills externas instaladas (ver `PROVENANCE.md` de cada una): `frontend-design`, `animate` y `reviewing-a11y`.

## Contratos inviolables

1. **RF-01 a RF-27 conservan su número y su significado.** No se renumeran, eliminan ni reinterpretan.
2. **El sistema nunca selecciona, descarta ni contrata automáticamente.** El ranking calcula, ordena y compara; nada más.
3. **La decisión final pertenece al Aprobador/Dirección**, con confirmación humana explícita y justificación (RF-23).
4. **El ML es informativo y operacional**, sobre el proceso, nunca evaluando, puntuando ni clasificando personas. Vale para el servicio actual (RF-29) y para cualquier ML futuro.
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
| Planificación y fases de v1.1 (F13–F23) | `docs/v1.1/` — cada fase en su `phase-*.md` |
| Modelos PowerDesigner de v1.1 (OOM, PDM y exportaciones) | `docs/v1.1/powerdesigner/` |
| Divergencias documentales entre v1.0 y v1.1 | `docs/v1.1/documentation-update-map.md` |
| Candidatos RF-28+, RNF y decisiones pendientes | `docs/v1.1/scope-preliminary.md` |

## Comandos habituales

Laravel y el frontend corren en Docker; no hay PHP ni Node locales del proyecto. El servicio ML es la excepción (ver abajo).

```
docker compose up -d --wait                                   # levantar
docker compose exec app php artisan test                      # PHPUnit (v1.0: 244 pruebas; develop: 408 + 8 omitidas)
docker compose exec app npm run build                         # compilar frontend
docker compose exec app npx tsc --noEmit                      # tipos
docker compose exec app npx vp test --run                     # pruebas de componente (develop)
npm run cy:run                                                # Cypress (entorno E2E aislado)
docker compose exec app php artisan migrate:fresh --seed --force   # datos demo
```

El servicio ML **no** corre en Docker Compose: se ejecuta desde `ml-service/` con su entorno virtual (`cd ml-service` y `.venv/Scripts/python.exe -m pytest`; el servidor, con `uvicorn` en el puerto 8008). Laravel solo lo llama si `ML_SERVICE_ENABLED=true`, y sin servicio la página funciona igual. Detalle en `docs/v1.1/phase-16-laravel-ml-integration.md`.

## Estado actual

*Verificado con Git el 24/09/2026. Antes de actuar, vuelve a comprobarlo: `git log --oneline -1 main develop` y `docs/PROGRESS.md`.*

### `main` — v1.0 académica (publicada)

- `main` sigue siendo la **v1.0 académica** (`4563c69`) y **no contiene v1.1**. El tag `v1.0.0-academic` apunta a `9a946c2` y no se mueve.
- RF-01 a RF-27 son la línea base v1.0. Sus documentos de cierre (`docs/final-report/`) siguen siendo correctos **para v1.0** y no se reescriben.

### `develop` — v1.1 en curso (integrado hasta la Fase 22)

`develop` = `origin/develop` = `2621bee`. **`main` y `develop` ya no tienen el mismo contenido**: `develop` integra las Fases 13 a 22.

| Fase | Contenido | Estado |
|---|---|---|
| 13 · 14 · 14.5 | Gobierno de v1.1, definición del experimento de ML, flujo multiagente | Integradas |
| 15 | `ml-service/`: dataset sintético, entrenamiento y **servicio FastAPI experimental** (`/health`, `/v1/model-info`, `/v1/predict`) | Integrada |
| 16 | **Integración Laravel ↔ FastAPI**: `vacancies.target_completion_at` (GAP-01 resuelto técnicamente), cliente HTTP con validación y *fallback*, tarjeta de riesgo operacional | Integrada |
| 17 | Validación ML y regresión integral | Integrada |
| 18 · 19 | **Rediseño del frontend** y **motion** (sin biblioteca nueva, con movimiento reducido) | Integradas |
| 20 | **Experiencia 3D con CSS 3D**, solo en la portada pública | Integrada |
| 21 | QA visual, accesibilidad y responsive | Integrada (`aced6da`) |
| 22 | Especificación UML del AS-IS, solo documentación (`docs/v1.1/uml/`) | Integrada (`2621bee`) |
| 23 | Formalización en PowerDesigner: OOM y PDM nativos, 22 diagramas exportados (`docs/v1.1/powerdesigner/`) | **Implementada** en `feature/phase-23-powerdesigner`, pendiente de auditoría. No está en `develop` |
| 24 | Sin alcance definido | **No iniciada** |

**ML (RF-29).** Implementado e integrado **experimentalmente**: validado técnicamente con datos sintéticos, **no** validado institucionalmente ni autorizado para producción. Estima el riesgo de demora del **proceso**; no puntúa, ordena, selecciona ni descarta personas, no toca el ranking y no cambia RF-23. Contrato científico congelado, no se modifica: *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`, *threshold* `0.1679418172266036`, Logistic Regression `C=10`, `class_weight=None`, `StandardScaler`, sin calibración.

**3D.** Una sola superficie —la tarjeta del expediente de la portada pública—, con **CSS 3D** (perspectiva y capas de DOM): sin WebGL, Three.js, React Three Fiber ni Spline, y sin dependencias nuevas. Decorativa, fuera de todo flujo operativo, con póster de respaldo (movimiento reducido, pantallas de menos de 1024 px, ahorro de datos, equipos modestos o fallo del fragmento). **No se amplía sin una nueva decisión del equipo** (ADR-003 y skill `recruitment-3d-experience`).

**Requisitos.** RF-28, RF-29 y los RNF nuevos (RNF-A, RNF-B, RNF-C…) siguen siendo **candidatos** en `docs/v1.1/scope-preliminary.md`: implementar algo no lo promueve al baseline (decisión 11). La promoción de RF-28, RF-29 y RNF-C es una decisión pendiente del equipo (preguntas 12 y 13).

> Historia: hasta el hotfix documental de la Fase 21 esta sección decía que `main` y `develop` tenían el mismo contenido y que la Fase 13 era solo gobierno, sin ML, FastAPI, rediseño, motion ni 3D. Era cierto al abrir v1.1 (19/09/2026); dejó de serlo al integrarse las Fases 13 a 20.

## Permisos

No amplíes permisos por comodidad. `.claude/settings.local.json` es local y no se versiona; cualquier cambio de permisos, instalación global de skills o ejecución de hooks externos requiere autorización explícita del equipo.
