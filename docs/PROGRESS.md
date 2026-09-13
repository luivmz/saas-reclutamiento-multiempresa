# Progreso del proyecto (checkpoint)

Fecha del checkpoint: 2026-09-13 · Rama actual: `feature/evaluations-interviews`

## Fases

| Fase | Estado |
|---|---|
| 0 — Inspección y plan | ✅ Completada (`docs/implementation-plan.md`) |
| 1 — Bootstrap Laravel 13 + React/Inertia + PostgreSQL + Redis (Docker) | ✅ Completada |
| 2 — Tenancy, roles, seguridad base, auditoría base | ✅ Completada |
| 3 — RF-01 a RF-07 | ✅ Completada |
| 4 — RF-08 a RF-15 | ✅ Completada |
| 5 — RF-16 a RF-19 | ⚠️ Iniciada: solo pruebas RED y configuración de zona horaria |
| 6 a 12 | ❌ Pendientes |

## Estado exacto de la Fase 5

**Hecho (sin commit previo, incluido en el commit de checkpoint):**
- Pruebas RED escritas (sintaxis verificada con `php -l`):
  - `tests/Unit/Assessments/ScoreSheetValidatorTest.php` (5 pruebas)
  - `tests/Feature/Assessments/EvaluationTest.php` (11 pruebas: RF-16, RF-17, RF-20, registro de resultados, asignaciones del evaluador, descarga de CV por evaluador)
  - `tests/Feature/Assessments/InterviewTest.php` (7 pruebas: RF-18, RF-19, RF-20, cierre, acceso cruzado)
- `config/app.php`: `timezone` ahora usa `APP_TIMEZONE` (por defecto `America/Lima`); variable añadida a `.env.example` (y al `.env` local, no versionado).

**Resultado real de estas pruebas:** fallan (RED esperado) con `Class "App\Services\Assessments\ScoreSheetValidator" not found` y `Route [applications.evaluations.store] not defined`.

**Falta (no iniciado):**
- Enums: `AssessmentStatus` (Scheduled/Completed/…), `EvaluationType`, `Modality`, `InterviewOutcome`.
- Migraciones: `evaluations`, `evaluation_results`, `interviews`, `interview_results`.
- Modelos y factories: `Evaluation`, `EvaluationResult`, `Interview`, `InterviewResult` (factories con `forApplication()` y `assignedTo()`).
- Servicios: `Assessments\ScoreSheetValidator`, `EvaluationService`, `InterviewService`.
- Notificaciones: `AssessmentConvocationNotification`, `AssessmentAssignedNotification`.
- Policies, Form Requests, controladores y rutas: `applications.evaluations.store`, `applications.interviews.store`, `assessments.index`, `evaluations.show`, `evaluations.results.store`, `interviews.show`, `interviews.results.store`.
- `CandidateDocumentPolicy`: permitir descarga al evaluador asignado.
- Frontend: `assessments/index`, `assessments/show`, secciones de programación en `applications/show`, convocatorias en la vista del postulante.

## Estado de RF

| Estado | RF |
|---|---|
| ✅ Implementado (backend + frontend + PHPUnit) | RF-01, RF-02, RF-03, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-10, RF-11, RF-12, RF-13, RF-14, RF-15 |
| ⚠️ Parcial | RF-20 (validación de pesos/rangos de criterios al configurar y publicar; falta validar puntajes al registrar resultados), RF-27 (`audit_logs` + `AuditLogger` usado en RF-01 a RF-15; falta vista de consulta y eventos de fases 5–7) |
| ❌ Pendiente | RF-16, RF-17, RF-18, RF-19, RF-21, RF-22, RF-23, RF-24, RF-25, RF-26 |

## Pruebas ejecutadas (resultados reales)

- Última suite completa PHPUnit (commit `215cdbe`, Fase 4): **129 passed, 8 skipped, 0 failed** (433 aserciones). Los 8 skipped son pruebas del starter kit para funciones de Fortify desactivadas.
- `npm run build`: OK. `tsc --noEmit`: 0 errores (Fase 4).
- Pruebas de la Fase 5: RED (fallan por clases/rutas inexistentes), como se espera antes de implementar.
- Cypress: **no configurado aún**. No hay cobertura medida.

## Cambios realizados en esta sesión

- Proyecto generado con `laravel/react-starter-kit` (dev-main: Laravel 13.31, Inertia 3, Fortify, PHPUnit 12).
- Entorno Docker: `app` (PHP 8.4 + Node 22), `queue`, `postgres:17`, `redis:7`; endpoint `/health`.
- Multitenencia por `organization_id` (scope global + Policies), roles con *check constraints*.
- Auditoría inmutable con eliminación de datos sensibles.
- Flujo de requerimientos (RF-01..04), vacantes con perfil, criterios y validación de publicación (RF-05..07), portal público.
- Perfil de postulante, CV PDF privado, postulación, expediente, preselección/descarte/cambio de etapa y centro de notificaciones (RF-08..15).
- UI en español; traducciones `lang/es`.
- Documentación: `docs/implementation-plan.md`, `docs/assumptions.md` (A-01..A-15), `docs/defects.md` (DEF-01..DEF-05).

## Archivos importantes

- Backend: `app/Services/**`, `app/Policies/**`, `app/Http/Controllers/**`, `app/Http/Requests/**`, `app/Models/**`, `app/Enums/**`, `routes/web.php`, `database/migrations/2026_09_13_*`.
- Frontend: `resources/js/pages/**`, `resources/js/components/**`, `resources/js/lib/navigation.ts`.
- Infraestructura: `docker-compose.yml`, `docker/php/Dockerfile`, `docker/php/entrypoint.sh`, `phpunit.xml`.

## Git

- Rama actual: `feature/evaluations-interviews` (creada desde `develop`).
- Último commit antes del checkpoint: `f20f0b6` (merge de la Fase 4 en `develop`).
- Commit de checkpoint: `test: add RED tests for evaluations and interviews (checkpoint)` sobre la rama actual. **Contiene pruebas que fallan intencionalmente (RED)**: no fusionar en `develop` hasta completar la Fase 5.
- Sin push.

## Siguiente tarea exacta para retomar

1. `docker compose up -d` y confirmar `http://localhost:8000/health`.
2. En la rama `feature/evaluations-interviews`, implementar `app/Services/Assessments/ScoreSheetValidator.php` para que pase `tests/Unit/Assessments/ScoreSheetValidatorTest.php` (API: `validate(array<int, CriterionDefinition> $criteria, array<int, float|int> $scores): array<int, string>`, errores indexados por id de criterio, mensaje «... entre {min} y {max}»).
3. Implementar enums, migraciones, modelos/factories, servicios, policies, requests, controladores y rutas listados arriba hasta que pasen `tests/Feature/Assessments`.
4. `docker compose exec -T app php artisan test` completo, `npm run build`, `npx tsc --noEmit`; commit `feat: implement evaluations and interviews` y merge `--no-ff` a `develop`.
5. Continuar con la Fase 6 (RF-20 a RF-25: `RankingService`, comparación, decisión humana, selección y cierre).
