# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/notifications-audit`

## Fases

| Fase | Estado |
|---|---|
| 0 — Inspección y plan | ✅ Completada (`docs/implementation-plan.md`) |
| 1 — Bootstrap Laravel 13 + React/Inertia + PostgreSQL + Redis (Docker) | ✅ Completada |
| 2 — Tenancy, roles, seguridad base, auditoría base | ✅ Completada |
| 3 — RF-01 a RF-07 | ✅ Completada |
| 4 — RF-08 a RF-15 | ✅ Completada |
| 5 — RF-16 a RF-19 | ✅ Completada e integrada en `develop` (`40eda7d`) |
| 6 — RF-20 a RF-25 | ✅ Completada e integrada en `develop` (`dda4bd0`) |
| 7 — RF-26 y RF-27 | ✅ Completada en `feature/notifications-audit` (**pendiente de revisión; no fusionada en `develop`**) |
| 8 a 12 | ❌ Pendientes |

**RF-01 a RF-27 constituyen la línea base funcional completa** y todos quedan implementados con backend, frontend y pruebas PHPUnit. RF-25 no incluye cierre sin selección (A-30).

## Reglas de negocio vigentes de la Fase 6 (aprobadas)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras registrar la decisión final (y, por tanto, también tras la selección), RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28; el bloqueo aplica desde la decisión).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 7 — lo realizado

- **RF-26:** `ProcessResultNotification`, una sola clase configurable (seleccionado / no seleccionado) sobre `RecruitmentNotification` (canal `database` + `mail` con driver `log`).
  - Se envía solo al cerrar la vacante, al seleccionado y a quienes pasan a «no seleccionado» en ese cierre (A-31).
  - Contenido: vacante, organización y resultado propio. Sin puntajes, ranking, justificaciones ni otros candidatos.
  - Idempotente por la máquina de estados, el bloqueo de fila y `afterCommit` (A-32).
  - Auditoría `proceso.resultado_notificado`, solo con conteos.
- **RF-27 (existía):** `audit_logs`, `AuditLogger` con eliminación de claves sensibles, `AuditLog` inmutable a nivel de Eloquent, scope por organización, y auditoría de las acciones de negocio desde el requerimiento hasta el cierre.
- **RF-27 (completado):**
  - Vista `audit/index` de solo lectura para Aprobador / Dirección, filtrada por organización, paginada, con lo más reciente primero, filtro por acción y resumen seguro por lista blanca (A-33).
  - Trigger PostgreSQL de solo inserción (DEF-07, A-34).
  - Eliminación ampliada de `cookie`, `authorization` y `api_key` (DEF-08).
  - Prueba de trazabilidad completa del flujo con organización, actor y entidad.
- **Supuestos:** A-31 a A-34. **Defectos:** DEF-07, DEF-08.

## Pruebas ejecutadas (resultados reales)

- Fase 7: 19 pruebas nuevas; GREEN **19 passed (238 assertions)**.
- Regresión: notificaciones 53 passed; auditoría 15 passed; cross-tenant 16 passed.
- Suite completa PHPUnit: **230 pruebas: 222 passed, 8 skipped, 0 failed (1017 assertions)**.
- `npm run build`: OK. `npx tsc --noEmit`: 0 errores.
- Cypress: **no configurado aún**. No hay cobertura medida.
- **Pendiente de validación manual en navegador:** UI de las Fases 5, 6 y 7 (`assessments/*`, sesiones en el expediente, convocatorias del postulante, `selection/comparison`, `audit/index`).

Detalle en `docs/tdd-evidence.md`.

## Migraciones de la Fase 7

- `2026_09_13_000012_make_audit_logs_append_only.php` (función y trigger `audit_logs_append_only`)

## Git

- Rama: `feature/notifications-audit` (creada desde `develop` en `dda4bd0`).
- Sin push. **No fusionar en `develop` hasta la revisión del equipo.**

## Siguiente tarea exacta para retomar

1. Revisión de la Fase 7; si se aprueba, merge `--no-ff` de `feature/notifications-audit` a `develop`.
2. Fase 8 (frontend integral): validación manual de la UI de las Fases 5–7 y ajustes de navegación y experiencia.
3. Luego: seeders de demostración, Cypress (E2E-01 a E2E-10), métricas, documentación final e informe.
