# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/frontend-integral`

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
| 7 — RF-26 y RF-27 | ✅ Completada e integrada en `develop` (`cd092d1`) |
| 8 — Frontend integral y validación en navegador | ✅ Completada en `feature/frontend-integral` (**pendiente de revisión; no fusionada en `develop`**) |
| 9 a 12 | ❌ Pendientes |

**RF-01 a RF-27 constituyen la línea base funcional completa.** Todos quedan implementados con backend, frontend y pruebas PHPUnit, y se validaron por la interfaz en navegador. RF-25 no incluye cierre sin selección (A-30).

## Reglas de negocio vigentes de la Fase 6 (aprobadas; sin cambios en la Fase 8)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras registrar la decisión final (y, por tanto, también tras la selección), RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 8 — lo realizado

- **Integración:** merge `--no-ff` de la Fase 7 en `develop` (`cd092d1`) y rama `feature/frontend-integral`.
- **Datos de demostración:**
  - `DemoSeeder` construye los datos con los servicios reales (flujos, auditoría y notificaciones auténticos).
  - Carga dos organizaciones, todos los roles y postulantes ficticios.
  - Cubre los escenarios de cada estado: requerimientos, vacante en borrador y publicada, ranking pendiente de decisión y proceso cerrado.
  - Documentado en `docs/demo-users.md`.
- **Validación real en navegador:**
  - Cypress 15.3.0 (Electron) en Docker, usado como conductor del navegador.
  - Recorrido visual por rol a 1280, 820 y 390 px: 10/10 casos, 49 capturas.
  - Flujo integral de 12 pasos, desde el requerimiento hasta la auditoría: 12/12.
  - Detalle en `docs/manual-smoke-test.md`.
- **Defectos corregidos:**
  - DEF-09: zona horaria de las fechas en el frontend.
  - DEF-10: etiquetas y fechas legibles en el detalle de la auditoría.
  - DEF-11: iniciales de avatar.
- **Revisión integral:**
  - Navegación por rol correcta.
  - Estados vacíos, errores de flujo (`workflow`) y *toasts* de éxito consistentes.
  - Formularios con etiquetas asociadas.
  - Tablas con desplazamiento horizontal en móvil.
  - `data-cy` estables ya presentes en todos los puntos críticos del flujo (no hubo que agregar).
- **Sin cambios** en reglas de negocio, RF ni roles.

## Pruebas ejecutadas (resultados reales)

- Pruebas nuevas de la Fase 8:
  - `AppTimezoneTest`: 2 pruebas.
  - `AuditLogViewTest::test_rf27_details_show_readable_labels_and_local_dates_instead_of_raw_values`: 1 prueba.
  - RED observado: 3 failed. GREEN: 9 passed junto con `AuditLogViewTest`.
- Suite completa PHPUnit: **233 pruebas: 225 passed, 8 skipped, 0 failed (1045 assertions)**.
- `npm run build`: OK. `npx tsc --noEmit`: 0 errores.
- Navegador: recorrido visual 10/10; flujo integral 12/12.
- Cypress como suite E2E versionada: **no configurado aún**. No hay cobertura medida.

Detalle en `docs/tdd-evidence.md`.

## Git

- Rama: `feature/frontend-integral` (creada desde `develop` en `cd092d1`).
- Sin push. **No fusionar en `develop` hasta la revisión del equipo.**

## Siguiente tarea exacta para retomar

1. Revisión de la Fase 8; si se aprueba, merge `--no-ff` de `feature/frontend-integral` a `develop`.
2. Fase 9 según el plan maestro (no iniciada).
