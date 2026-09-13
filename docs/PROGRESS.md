# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/cypress-e2e`

## Fases

| Fase | Estado |
|---|---|
| 0 a 7 | ✅ Completadas e integradas en `develop` |
| 8 — Frontend integral y validación en navegador | ✅ Integrada en `develop` (`6d47e46`) |
| 9 — Suite E2E Cypress | ✅ Completada en `feature/cypress-e2e` (**pendiente de revisión; no fusionada en `develop`**) |
| 10 a 12 | ❌ Pendientes |

**RF-01 a RF-27 constituyen la línea base funcional completa.** La Fase 9 no cambió reglas de negocio ni RF.

## Reglas de negocio vigentes de la Fase 6 (aprobadas; sin cambios)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras la decisión final, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 9 — lo realizado

- **Integración de la Fase 8** en `develop` (`6d47e46`) y creación de `feature/cypress-e2e`. Checkpoint parcial previo: `9edb0cd`.
- **Estado reproducible:**
  - Comando `e2e:reset` y endpoints `POST /__e2e/reset` y `GET /__e2e/queue`.
  - Protegidos por `E2E_ENABLED`, fuera de producción y con token `X-E2E-Token`.
  - Cubiertos por `E2eSupportTest` (7 pruebas).
- **Cypress 15.3.0** en Docker (Electron 136 headless):
  - `cypress.config.cjs`, comandos de soporte y fixtures ficticias.
  - Scripts `cy:run`, `cy:open` y `e2e:reset`.
  - Ajuste mínimo del servicio `cypress` en `docker-compose.yml`.
- **13 specs y 40 tests:**
  - E2E-01 a E2E-10.
  - Multiempresa (E2E-11).
  - Negativos prioritarios (E2E-12).
  - Flujo integral de 14 etapas en 12 pasos (E2E-13).
- **Defectos reales de la aplicación:** ninguno. Se corrigieron dos tests por expectativas erróneas (E2E-04 negativo y E2E-10).
- **Documentación:** `docs/testing/cypress-e2e.md`.

## Pruebas ejecutadas (resultados reales)

| Verificación | Resultado |
|---|---|
| Cypress, suite completa (1.ª corrida) | 13 specs · 40 tests · 40 passed · 0 failed · 0 skipped · 04:01 · Electron 136 |
| Cypress, suite completa (2.ª corrida) | 13 specs · 40 tests · 40 passed · 0 failed · 0 skipped · 03:56 · Electron 136 |
| PHPUnit completo | **240 pruebas: 232 passed, 8 skipped, 0 failed (1064 assertions)** |
| `npm run build` | OK |
| `npx tsc --noEmit` | 0 errores |

Detalle en `docs/testing/cypress-e2e.md`.

## Seguridad

- `.env` no está versionado.
- `.env.example` deja `E2E_ENABLED=false` y `E2E_TOKEN` vacío.
- Ningún archivo versionado contiene el token (verificado con `git grep` sin mostrar el valor).
- Durante una prueba manual el token local se imprimió en una salida de terminal. Se rotó de inmediato y el nuevo valor nunca se mostró.

## Git

- Rama: `feature/cypress-e2e` (desde `develop` en `6d47e46`).
- Sin push. **No fusionar en `develop` hasta la revisión del equipo.**

## Pendientes reales

- Calcular en `America/Lima` las fechas que usan los specs (riesgo no observado entre 19:00 y 24:00 de Lima).
- Base de datos E2E separada de la de demostración (Fase 10, Docker).
- `cy:open` documentado pero no ejecutado; solo se probó Electron.

## Siguiente tarea exacta para retomar

1. Revisión de la Fase 9; si se aprueba, merge `--no-ff` de `feature/cypress-e2e` a `develop`.
2. Fase 10 según el plan maestro (no iniciada).
