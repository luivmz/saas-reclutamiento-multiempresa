# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/ranking-selection-closure`

## Fases

| Fase | Estado |
|---|---|
| 0 — Inspección y plan | ✅ Completada (`docs/implementation-plan.md`) |
| 1 — Bootstrap Laravel 13 + React/Inertia + PostgreSQL + Redis (Docker) | ✅ Completada |
| 2 — Tenancy, roles, seguridad base, auditoría base | ✅ Completada |
| 3 — RF-01 a RF-07 | ✅ Completada |
| 4 — RF-08 a RF-15 | ✅ Completada |
| 5 — RF-16 a RF-19 | ✅ Completada e integrada en `develop` (merge `40eda7d`) |
| 6 — RF-20 a RF-25 | ✅ Completada en `feature/ranking-selection-closure` (**pendiente de revisión; no fusionada en `develop`**) |
| 7 a 12 | ❌ Pendientes |

## Fase 6 — lo realizado

- **RF-20:** reutiliza `WeightingValidator` y `ScoreSheetValidator` (sin duplicarlos).
  - `RankingService` rechaza configuración de pesos inválida, puntajes fuera de rango, criterios ajenos a la vacante y postulaciones duplicadas.
  - La comparación muestra el error en lugar de un ranking.
- **RF-21:** `RankingService`, servicio de dominio puro y determinista, sin persistencia ni efectos sobre estados.
  - Fórmula normalizada por rango y ponderación (A-24).
  - Candidatos incompletos listados aparte (A-25).
  - Empates marcados y no desempatados (A-26).
  - `VacancyRankingBuilder` usa solo postulaciones de la vacante y de su organización, sin descartados y con resultados de sesiones realizadas (A-23).
- **RF-22:** página `selection/comparison` con criterios, ponderaciones, promedios, aportes por criterio, total, posición y empates, más la fórmula visible y el aviso de decisión humana.
- **RF-23:** `FinalDecisionService`.
  - Solo el Aprobador registra la decisión, con confirmación humana explícita y justificación.
  - Exige un candidato finalista con resultados completos; puede elegir a alguien que no sea el primero.
  - Una única decisión, inmutable y auditada.
  - **No cambia estados.**
- **RF-24:** `SelectionRegistrationService` (RR. HH.) aplica la decisión: finalista → seleccionado, con historial y auditoría.
  - Un índice único parcial en PostgreSQL impide un segundo seleccionado.
  - Tras la decisión se bloquean cambios manuales de etapa (A-28).
- **RF-25:** `VacancyClosureService` (RR. HH.) cierra con selección registrada.
  - Las postulaciones activas restantes pasan a `no_seleccionado`.
  - Registra fecha, responsable, tipo de cierre, notas y auditoría.
  - Cierre sin selección **no implementado** (sin TO-BE, A-30).
  - Una vacante cerrada bloquea postulación, programación, resultados, decisión, selección y nuevo cierre.
- **Supuestos:** A-23 a A-30. **Defectos de producto:** ninguno nuevo (los errores encontrados eran de diseño de pruebas; ver `docs/tdd-evidence.md`).

## Estado de RF

| Estado | RF |
|---|---|
| ✅ Implementado (backend + frontend + PHPUnit) | RF-01 a RF-25 (RF-25 sin cierre «desierta», A-30) |
| ⚠️ Parcial | RF-27 (auditoría activa en RF-01 a RF-25; falta vista de consulta) |
| ❌ Pendiente | RF-26 |

## Pruebas ejecutadas (resultados reales)

- Fase 6: 51 pruebas nuevas; RED por bloque y GREEN final de `tests/Unit/Ranking`, `tests/Unit/Enums`, `tests/Feature/Selection`: **78 passed (273 assertions)**.
- Regresión relacionada (tenancy, roles, postulaciones, evaluaciones, vacantes): **57 passed (268 assertions)**.
- Suite completa PHPUnit: **211 pruebas: 203 passed, 8 skipped, 0 failed (779 assertions)**.
- `npm run build`: OK. `npx tsc --noEmit`: 0 errores.
- Cypress: **no configurado aún**. No hay cobertura medida.
- **Pendiente de validación manual en navegador:** UI de las Fases 5 y 6 (`assessments/*`, panel de sesiones en el expediente, convocatorias del postulante, `selection/comparison`). Se revisará en la fase de validación integral/frontend.

Detalle en `docs/tdd-evidence.md`.

## Migraciones de la Fase 6

- `2026_09_13_000011_create_selection_decisions_table.php` (`selection_decisions` e índice único parcial `applications_one_selected_per_vacancy`)

## Git

- Rama: `feature/ranking-selection-closure` (creada desde `develop` en `40eda7d`).
- Sin push. **No fusionar en `develop` hasta la revisión del equipo.**

## Siguiente tarea exacta para retomar

1. Revisión de la Fase 6 por el equipo; si se aprueba, merge `--no-ff` de `feature/ranking-selection-closure` a `develop`.
2. Fase 7: RF-26 (notificar resultado y cierre al postulante) y cierre de RF-27 (vista de consulta de auditoría).
3. Posteriormente: seeders de demostración, Cypress (E2E-01 a E2E-10) y validación manual de la UI de las Fases 5 y 6.
