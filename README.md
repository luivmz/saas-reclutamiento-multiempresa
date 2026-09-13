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

## Arquitectura

- **Estilo:** monolito modular SaaS multiempresa, sin microservicios.
- **Aislamiento entre organizaciones:** `organization_id` con *scope* global y **Policies** que verifican rol y organización en el backend.
- **Base de datos:** PostgreSQL con restricciones de integridad y auditoría de solo inserción.
- **Redis:** sesiones, caché y colas; un worker procesa las notificaciones.

Detalle en `docs/final-report/07-arquitectura-tecnologica.md`.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Laravel 13.31 · PHP 8.4.25 · Fortify |
| Frontend | React 19 · TypeScript 5.9 · Inertia 3 · Tailwind CSS 4 (shadcn/ui) · Vite 8 |
| Datos | PostgreSQL 17.11 · Redis 7.4.11 |
| Pruebas | PHPUnit 12.5 · Cypress 15.3.0 (Electron 136) |
| Entorno | Docker Compose · Git |

No usa XAMPP ni MySQL. No implementa despliegue en la nube, R2/S3, Sentry, Meilisearch, IA ni RLS.

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

| Tipo | Comando | Último resultado |
|---|---|---|
| PHPUnit (unitarias + *feature*) | `docker compose exec app php artisan test` | 244 pruebas: 236 superadas, 8 omitidas, 0 fallidas (1074 aserciones) |
| Cypress E2E (entorno aislado) | `npm run cy:run` | 14 specs, 43/43 |
| *Build* y tipos | `docker compose exec app npm run build` · `docker compose exec app npx tsc --noEmit` | Correcto · 0 errores |

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

## Seguridad

- Autorización en el backend con Policies y aislamiento multiempresa probado (PHPUnit y E2E).
- Validación en el servidor, protección CSRF y límite de intentos de inicio de sesión.
- CV en disco privado con descarga autorizada.
- Auditoría inmutable sin datos sensibles.
- Endpoints de soporte E2E inertes fuera del entorno aislado y nunca en producción.
- `.env` y `.env.e2e` no se versionan; los archivos `.example` no contienen secretos.

Todos los datos son ficticios. No se afirma cumplimiento legal ni certificación.

## Estado

- **Fases completadas:**
  - 0 a 10: implementación de RF-01 a RF-27, frontend, E2E y Docker.
  - 11: documentación final (en revisión).
- **Pendiente:** Fase 12 (QA final, integración en `main` y publicación del repositorio).
