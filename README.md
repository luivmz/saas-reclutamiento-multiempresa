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
| Línea académica post-release F27–F34C | `docs/academico/ACADEMIC_BASELINE.md` · `docs/academico/auditoria-global/README.md` · `docs/academico/diseno-inteligente/README.md` · `docs/academico/datos-sinteticos/README.md` · `docs/academico/g0-readiness/README.md` · `docs/academico/g0-evidence/README.md` |
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
- **v1.1 académica (publicada):** el tag `v1.1.0-academic` conserva el cierre técnico `634f354`; F0–F26 están cerradas. F27–F34B están cerradas e integradas como documentación académica post-release, sin cambios productivos; F34 conserva exclusivamente datos sintéticos. El cierre F34C y el estado vigente de G0 se registran a continuación y en `docs/PROGRESS.md` y `docs/academico/ACADEMIC_BASELINE.md`. Los entregables de fases anteriores conservan su fotografía histórica; no se crean nuevos tags ni releases.
- **Requisitos:** RF-01 a RF-27 son la línea base. RF-28 (candidato, no implementado), RF-29 (experimental) y RNF-C (propuesta) **no** forman parte de ella. Estado por fase: `docs/PROGRESS.md`.
- **F34C CERRADA** tras auditoría final **PASS**, sin cambios productivos. **G0-14 = CUMPLIDO; G0-09 = CUMPLIDO; ADR-005 canónico = PROPUESTA; aprobación interna del equipo = REGISTRADA; G0 = NO APROBADA. G0-02 = PENDIENTE EXTERNO; G0-03 = PENDIENTE EXTERNO; G0-12 = PENDIENTE EXTERNO; F35–F40 = BLOQUEADAS; datos reales PROHIBIDOS.** Hay cuatro adjuntos reales de tres integrantes: se documentan la copia histórica/restaurada de Luis y su confirmación adicional; no se confunden con aprobación jurídica, de privacidad ni institucional. RF-23 sigue humana; RF-29 experimental/informativa y RF-CAND fuera del baseline. Commits A `723001c13e193adace00650cf2c9296468483448` y B `c79fc24597ee0037978c9453df1eb762caf9497e`. Base preintegración: `develop` `619e1b217bf437376618b3eabd95d5013dba2f33`, `main` `b4d4d62456d437d313436eeffb4049f7d513d2cb`. Publicación autorizada con gates CI de develop/main; hashes de integración y resultados finales en Git/GitHub, sin anticiparlos. Sin nuevos tags ni releases.
- **Histórico F34B:** cerrada con cero evidencias externas reales en su entrega original; ese conteo no describe el estado actual tras F34C. Ningún formulario vacío ni control sintético en memoria equivale a aprobación.
