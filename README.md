# Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal

**Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo**

| | |
|---|---|
| Universidad | Universidad Continental |
| Facultad | Facultad de Ingeniería |
| Escuela | Ingeniería de Sistemas e Informática |
| Curso | Pruebas y Calidad de Software (NRC 28607) |
| Docente | Dr. Maglioni Arana Caparachin |
| Integrantes | Coronacion Meza Fredy · Peña Arroyo Anthony · Vila Meza Luis Antonio |

> El sistema calcula puntajes y rankings como **apoyo**, pero **nunca selecciona automáticamente al candidato**: la decisión final la registra el Aprobador/Dirección, con justificación (RF-23).

> **Versión v1.1 (académica).** Prototipo académico con datos ficticios; **no es un sistema productivo**. Añade un servicio **experimental** de riesgo operacional (RF-29) que estima el riesgo de demora del **proceso** de una vacante: no evalúa, puntúa, ordena, selecciona ni descarta personas y no interviene en el ranking ni en la decisión humana. Notas de la versión: [`docs/v1.1/release-notes-v1.1.md`](docs/v1.1/release-notes-v1.1.md) · [`CHANGELOG.md`](CHANGELOG.md).

## Arquitectura

- **Estilo:** monolito modular SaaS multiempresa, sin microservicios.
- **Aislamiento entre organizaciones:** `organization_id` con *scope* global y **Policies** que verifican rol y organización en el backend.
- **Base de datos:** PostgreSQL con restricciones de integridad y auditoría de solo inserción.
- **Redis:** sesiones, caché y colas; un worker procesa las notificaciones.
- **Riesgo operacional (v1.1, experimental):** servicio FastAPI **fuera de Docker Compose** (`ml-service/`), llamado por HTTP interno con token solo si `ML_SERVICE_ENABLED=true`. Sin servicio, la aplicación funciona igual.

Detalle en `docs/final-report/07-arquitectura-tecnologica.md`.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Laravel 13.31 · PHP 8.4.25 · Fortify |
| Frontend | React 19 · TypeScript 5.9 · Inertia 3 · Tailwind CSS 4 (shadcn/ui) · Vite 8 |
| Datos | PostgreSQL 17.11 · Redis 7.4.11 |
| ML experimental (v1.1) | Python 3.12 · scikit-learn 1.9.1 · FastAPI 0.115.6 · pytest |
| Pruebas | PHPUnit 12.5 · Vitest 4.1 · Cypress 15.3.0 (Electron 136) · pytest |
| Entorno | Docker Compose · Git |

No usa XAMPP ni MySQL. No implementa despliegue en la nube, R2/S3, Sentry, Meilisearch, IA en la nube ni RLS. El único componente de ML es el servicio local y experimental de riesgo operacional (RF-29).

## Instalación con Docker

Requisitos: Docker Desktop o Docker Engine con Compose ≥ 2.24, y Git.

```powershell
copy .env.example .env                                              # opcional; ajuste puertos si están ocupados
docker compose up -d --build --wait                                 # primera vez: instala dependencias, compila y migra
docker compose exec app php artisan migrate:fresh --seed --force    # datos demo ficticios
```

Abra http://localhost:8000. Guía completa (entorno E2E, reset y solución de problemas): **`docs/docker.md`**.

## Usuarios de demostración (ficticios)

Contraseña de todos: `password` (solo para desarrollo y demostración). Lista completa y escenarios: `docs/demo-users.md`.

| Rol | Correo |
|---|---|
| Área solicitante | `solicitante@andino.test` |
| Recursos Humanos | `rrhh@andino.test` |
| Aprobador / Dirección | `direccion@andino.test` |
| Evaluador | `evaluador@andino.test` |
| Postulante | `postulante5@correo.test` · `postulante.nuevo@correo.test` (sin perfil) |
| Otra organización (aislamiento) | `rrhh@demob.test` · `direccion@demob.test` |

## Pruebas

| Tipo | Comando | Último resultado (QA global, Fase 25) |
|---|---|---|
| PHPUnit (unitarias + *feature*) | `docker compose exec app php artisan test` | 411 superadas, 8 omitidas, 0 fallidas (1498 aserciones) |
| Componentes (Vitest) | `docker compose exec app npx vp test --run` | 42/42 |
| Servicio ML (pytest) | `cd ml-service` · `.venv/Scripts/python.exe -m pytest` | 533 superadas |
| Cypress E2E (entorno aislado) | `npm run cy:run` | 20 specs, 85/85 |
| *Build* y tipos | `docker compose exec app npm run build` · `docker compose exec app npx tsc --noEmit` | Correcto · 0 errores |

Resultado de la v1.0 (Fase 12): 244 pruebas PHPUnit (236 superadas, 8 omitidas) y 14 specs Cypress (43/43). Detalle de la v1.1: [`docs/v1.1/phase-25-final-qa.md`](docs/v1.1/phase-25-final-qa.md).

La cobertura porcentual de código no se ha medido.

## Comandos útiles

| Acción | Comando |
|---|---|
| Estado y salud | `docker compose ps` · `curl http://localhost:8000/health` |
| Logs | `docker compose logs -f app` · `docker compose logs -f queue` |
| Reiniciar datos demo | `npm run demo:reset` |
| Entorno E2E | `npm run e2e:setup` · `npm run e2e:up` · `npm run e2e:reset` · `npm run cy:open` |
| Detener | `docker compose down` (con `-v` también borra los datos) |

## Estructura

```text
app/                  Backend: Controllers, Requests, Policies, Services, Enums, Models, Notifications
database/             Migraciones (PostgreSQL) y DemoSeeder
resources/js/         Frontend React/TypeScript (páginas Inertia por módulo)
tests/                PHPUnit: Unit y Feature
cypress/              Suite E2E (specs, soporte, fixtures)
ml-service/           Servicio experimental de riesgo operacional (Python, FastAPI; v1.1)
docker/               Dockerfile, entrypoint y scripts de PostgreSQL
docs/                 Documentación técnica y del informe final
```

## Documentación

| Tema | Documento |
|---|---|
| Informe final (14 capítulos) | `docs/final-report/01-informacion-general.md` … `14-implementacion-monitoreo.md` |
| Matriz maestra RF-01 a RF-27 | `docs/final-report/traceability-master.md` |
| Índice de evidencias | `docs/final-report/evidence-index.md` |
| Resumen técnico y guion de demo | `docs/final-report/technical-summary.md` · `docs/final-report/demo-script.md` |
| Progreso | `docs/PROGRESS.md` |
| Docker | `docs/docker.md` |
| Suite E2E | `docs/testing/cypress-e2e.md` |
| TDD, defectos y supuestos | `docs/tdd-evidence.md` · `docs/defects.md` · `docs/assumptions.md` |
| v1.1: fases, cierre y *release* | `docs/v1.1/` · `docs/v1.1/phase-26-release-closeout.md` · `docs/v1.1/release-notes-v1.1.md` |
| v1.1: UML y PowerDesigner | `docs/v1.1/uml/` · `docs/v1.1/powerdesigner/` |
| v1.1: Formato 09 | `docs/academico/phase-24/` |
| Divergencias entre v1.0 y v1.1 | `docs/v1.1/documentation-update-map.md` |

## Seguridad

- Autorización en el backend con Policies y aislamiento multiempresa probado (PHPUnit y E2E).
- Validación en el servidor, protección CSRF y límite de intentos de inicio de sesión.
- CV en disco privado con descarga autorizada.
- Auditoría inmutable sin datos sensibles.
- Endpoints de soporte E2E inertes fuera del entorno aislado y nunca en producción.
- `.env` y `.env.e2e` no se versionan; los archivos `.example` no contienen secretos.

Todos los datos son ficticios. No se afirma cumplimiento legal ni certificación.

## Estado

- **v1.0 académica (publicada):** Fases 0 a 12, RF-01 a RF-27; rama `main` y tag `v1.0.0-academic`. Veredicto de la Fase 12: **APTO PARA PUBLICACIÓN** (`docs/final-report/qa-final-report.md`).
- **v1.1 académica (en cierre):** Fases 13 a 25 cerradas en `develop` (ML experimental, integración Laravel ↔ FastAPI, rediseño, *motion*, CSS 3D, QA visual, UML, PowerDesigner, Formato 09 y QA global). La Fase 26 prepara el cierre y el *release* (`docs/v1.1/phase-26-release-closeout.md`); la etiqueta propuesta es `v1.1.0-academic`, pendiente de auditoría.
- **Requisitos:** RF-01 a RF-27 son la línea base. RF-28 (candidato, no implementado), RF-29 (experimental) y RNF-C (propuesta) **no** forman parte de ella. Estado por fase: `docs/PROGRESS.md`.
