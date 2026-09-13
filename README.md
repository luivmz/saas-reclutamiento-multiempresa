# Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal

Caso de estudio: **Colegio Andino de Huancayo**. Proyecto académico del curso Pruebas y Calidad de Software (NRC 28607) de la Universidad Continental. Docente: Dr. Maglioni Arana Caparachin.

Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio.

> El sistema calcula puntajes y rankings como apoyo, pero **nunca selecciona automáticamente al candidato**: la decisión final la registra una persona autorizada (RF-23).

## Stack

- Laravel 13 (PHP 8.4) como monolito modular multiempresa.
- React 19 + TypeScript + Inertia 3 + Vite + Tailwind 4 (shadcn/ui).
- PostgreSQL 17 y Redis 7 (sesiones, caché y colas).
- PHPUnit y Cypress 15.
- Docker Compose. No se usan XAMPP ni MySQL.

## Puesta en marcha (Docker)

Requisitos: Docker Desktop o Docker Engine con Compose ≥ 2.24, y Git.

```powershell
copy .env.example .env                                              # opcional; ajuste puertos si están ocupados
docker compose up -d --build --wait                                 # primera vez: varios minutos
docker compose exec app php artisan migrate:fresh --seed --force    # datos demo ficticios
```

Abra http://localhost:8000. Usuarios de demostración (contraseña `password`): `docs/demo-users.md`.

| Tarea | Comando |
|---|---|
| Estado y salud | `docker compose ps` · `curl http://localhost:8000/health` |
| PHPUnit | `docker compose exec app php artisan test` |
| Cypress (entorno E2E aislado) | `npm run cy:run` |
| Detener | `docker compose down` |

Guía completa (arquitectura, variables, E2E, reset y solución de problemas): **`docs/docker.md`**.

## Documentación

| Tema | Documento |
|---|---|
| Progreso | `docs/PROGRESS.md` |
| Plan de implementación | `docs/implementation-plan.md` |
| Matriz de RF (RF-01 a RF-27) | `docs/rf-implementation-matrix.md` |
| Supuestos | `docs/assumptions.md` |
| Defectos | `docs/defects.md` |
| Suite E2E | `docs/testing/cypress-e2e.md` |
| Usuarios demo | `docs/demo-users.md` |

Todos los datos del proyecto son ficticios.
