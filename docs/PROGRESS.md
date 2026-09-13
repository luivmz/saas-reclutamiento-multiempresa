# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/evaluations-interviews`

## Fases

| Fase | Estado |
|---|---|
| 0 — Inspección y plan | ✅ Completada (`docs/implementation-plan.md`) |
| 1 — Bootstrap Laravel 13 + React/Inertia + PostgreSQL + Redis (Docker) | ✅ Completada |
| 2 — Tenancy, roles, seguridad base, auditoría base | ✅ Completada |
| 3 — RF-01 a RF-07 | ✅ Completada |
| 4 — RF-08 a RF-15 | ✅ Completada |
| 5 — RF-16 a RF-19 | ✅ Completada (commit de cierre en `feature/evaluations-interviews`, pendiente de merge a `develop`) |
| 6 a 12 | ❌ Pendientes |

## Fase 5 — lo realizado

- **Validación de puntajes:** `app/Services/Assessments/ScoreSheetValidator.php` (puro, testeable; rangos, puntajes faltantes o no numéricos, criterios ajenos a la etapa).
- **Programación (RF-16, RF-18):** `AssessmentScheduler`
  - Evaluador de la misma organización, fecha futura y etapas permitidas.
  - Avance automático de la postulación a `en_evaluacion` / `en_entrevista`.
  - Auditoría `evaluacion.programada` / `entrevista.programada`.
- **Convocatoria (RF-17):** `AssessmentConvocationNotification` al postulante y `AssessmentAssignedNotification` al evaluador (canal `database` + `mail` con driver `log`); `invitation_sent_at`.
- **Registro de resultados (RF-19):** `AssessmentResultRecorder`
  - Solo el evaluador asignado registra, una única vez, con todos los criterios de la etapa dentro de su rango.
  - La entrevista exige resultado y observaciones.
  - El registro se bloquea si la vacante está cerrada.
  - Auditoría `*.resultado_registrado`.
- **Autorización:** `EvaluationPolicy`, `InterviewPolicy`, `ApplicationPolicy::scheduleAssessment` y `CandidateDocumentPolicy` (el evaluador asignado puede descargar el CV).
- **Frontend:**
  - `assessments/index` («Mis evaluaciones» del evaluador) y `assessments/show` (hoja de puntajes).
  - Panel de programación y resultados en `applications/show`.
  - Convocatorias en `candidate/applications/show`, sin puntajes.
  - Menú del rol evaluador.
- **Supuestos:** A-16 a A-22. **Defectos:** DEF-06.

## Estado de RF

| Estado | RF |
|---|---|
| ✅ Implementado (backend + frontend + PHPUnit) | RF-01 a RF-19 |
| ⚠️ Parcial | RF-20 (pesos al configurar/publicar y rangos de puntajes al registrar; falta su uso previo al ranking), RF-27 (auditoría activa en RF-01 a RF-19; falta vista de consulta y eventos de fases 6–7) |
| ❌ Pendiente | RF-21, RF-22, RF-23, RF-24, RF-25, RF-26 |

## Pruebas ejecutadas (resultados reales)

- Fase 5: RED inicial **23 failed (0 assertions)** → GREEN **23 passed (99 assertions)**.
- Autorización / cross-tenant / aplicaciones / postulantes: **35 passed (146 assertions)**.
- Suite completa PHPUnit: **160 pruebas: 152 passed, 8 skipped, 0 failed (532 assertions)**.
- `npm run build`: OK. `npx tsc --noEmit`: 0 errores.
- Cypress: **no configurado aún**. No hay cobertura medida.
- La UI nueva **no se verificó en un navegador** en esta sesión (solo build, tipos y pruebas de backend con aserciones Inertia).

Detalle en `docs/tdd-evidence.md`.

## Migraciones de la Fase 5

- `2026_09_13_000009_create_evaluations_table.php` (`evaluations`, `evaluation_results`)
- `2026_09_13_000010_create_interviews_table.php` (`interviews`, `interview_results`)

## Git

- Rama: `feature/evaluations-interviews`.
- Commits de la Fase 5: `3e66623` (pruebas RED, checkpoint) y el commit `feat: implement evaluations and interviews`.
- Sin push. Pendiente: merge `--no-ff` a `develop`.

## Siguiente tarea exacta para retomar

1. `docker compose up -d` y confirmar `http://localhost:8000/health`.
2. Merge de `feature/evaluations-interviews` a `develop` y crear `feature/ranking-selection`.
3. Fase 6 (RF-20 a RF-25), empezando por pruebas RED de `RankingService`:
   - Ranking determinista, explicable y sin efectos sobre estados.
   - Normalización por rango y ponderación.
   - Empates y candidatos con resultados incompletos.
   - No se selecciona automáticamente.
