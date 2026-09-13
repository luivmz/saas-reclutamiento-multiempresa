# Plan de implementación

Proyecto: **Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal** — caso Colegio Andino de Huancayo.
Universidad Continental · Pruebas y Calidad de Software · NRC 28607 · Docente: Dr. Maglioni Arana Caparachin.
Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony, Vila Meza Luis Antonio.

## 1. Resultado de la Fase 0 (inspección real, 2026-09-12)

| Elemento | Resultado |
|---|---|
| Carpeta del proyecto | Vacía (solo `.claude/`) |
| Git | No inicializado |
| PHP local | 8.2.12 (XAMPP) — **no apto** para Laravel 13 (requiere PHP ≥ 8.3) |
| Composer local | 2.10.2 (usa el PHP de XAMPP) |
| Node / npm locales | 20.16.0 / 10.8.1 — por debajo de lo requerido por Vite 7 (Node ≥ 20.19) |
| Docker / Compose | 27.4.0 / v2.31.0 (Docker Desktop, se inició durante la inspección) |
| Puertos ocupados | 3306 (MySQL de XAMPP; no se usa) |
| Packagist | `laravel/framework` v13.31.0 y `laravel/react-starter-kit` disponibles |

**Decisión:** toda la cadena de herramientas (PHP 8.4, Composer, Node 22) se ejecuta en contenedores Docker. No se usa XAMPP ni MySQL.

## 2. Documentación disponible

Se buscó en la carpeta del proyecto y en `D:\Personal\Courses\PruebasCalidadSoftware` (recursivo).

| Documento solicitado | ¿Encontrado? |
|---|---|
| F4 — Identificación de problemas | No |
| F5 — Modelo BPM TO-BE | No |
| F6 — Requerimientos funcionales | No (los 27 RF se toman del enunciado entregado al equipo) |
| Práctica 08 — Casos de uso | No |
| Plan de pruebas | No |
| Plantilla de proyecto final | No (se usa la lista de 14 capítulos del enunciado) |
| Diagramas UML (PowerDesigner `.oom`) | **Sí** — 4 diagramas |

Contenido extraído de los diagramas UML:

1. **Despliegue**: Cliente → Internet/HTTPS → Servidor Web/Aplicación → PostgreSQL, Redis, S3, Queue Worker.
2. **Secuencia de postulación (RF-10/11)**: Postulante → React → Laravel 13/Inertia 3 → Policy → PostgreSQL. Pasos: consultar vacante, validar usuario y permisos, **consultar estado de vacante**, **verificar postulación existente**, registrar, confirmar.
3. **Secuencia de evaluación (RF-19)**: Evaluador selecciona candidato, consulta evaluación, registra puntajes y observaciones, Policy valida permiso, se guarda entrevista y resultado.
4. **Secuencia de selección (RF-24/25/27)**: RR. HH. consulta resultados y ranking, confirma selección, Policy valida, verifica estado de convocatoria, registra seleccionado, actualiza estado de postulación, cierra convocatoria, registra auditoría.

Toda regla no derivable de estas fuentes se registra en `docs/assumptions.md`.

## 3. Arquitectura

Monolito modular Laravel 13 + Inertia + React/TypeScript (starter kit oficial), PostgreSQL 17, Redis 7.
Organización por dominio dentro de las convenciones de Laravel:

- `app/Enums` — estados y roles.
- `app/Models` — modelos Eloquent con scope de organización (`BelongsToOrganization`).
- `app/Actions/<Módulo>` — casos de uso de negocio (una clase por operación).
- `app/Services` — servicios de dominio (`RankingService`, `WeightingValidator`, `AuditLogger`, `StateMachine` de los enums).
- `app/Policies` — autorización por rol + organización.
- `app/Http/Requests/<Módulo>` — validación server-side.
- `app/Http/Controllers/<Módulo>` — controladores delgados.
- `app/Notifications` — canal `database` (+ `mail` con driver `log`).
- `resources/js/pages/<módulo>` — páginas Inertia.

## 4. Fases

| Fase | Contenido | Commit esperado |
|---|---|---|
| 1 | Bootstrap Laravel 13 + React/Inertia + PostgreSQL + Redis en Docker | `chore: bootstrap Laravel application` / `chore: add Docker environment` |
| 2 | Organizaciones, roles, tenancy, Policies base, auditoría base | `feat: add organizations and tenant isolation` |
| 3 | RF-01..RF-07 | `feat: implement personnel request workflow`, `feat: implement vacancies` |
| 4 | RF-08..RF-15 | `feat: implement candidate applications` |
| 5 | RF-16..RF-19 | `feat: implement evaluations and interviews` |
| 6 | RF-20..RF-25 | `feat: add candidate ranking`, `feat: implement final selection and closure` |
| 7 | RF-26, RF-27 | `feat: add notifications and audit trail` |
| 8 | Frontend completo | incluido en cada fase |
| 9 | PHPUnit + Cypress | `test: ...` |
| 10 | Docker (app, queue, postgres, redis) | `chore: add Docker environment` |
| 11 | Documentación e informe final | `docs: ...` |
| 12 | QA final: tests, build, Cypress, `docker compose up` | — |

Ramas: `main` (estable), `develop` (integración), `feature/*` por fase, merge `--no-ff` a `develop` y de `develop` a `main` al cierre.

## 5. Riesgos identificados

- Ausencia de F5/F6/CU: transiciones de estado basadas en supuestos documentados.
- Bind mount de Windows en Docker es lento para `vendor/` y `node_modules/`: se aceptan tiempos mayores.
- Cypress se ejecuta con la imagen oficial `cypress/included` para no depender del Node local.
