# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `release/qa-final`

## Fases

| Fase | Estado |
|---|---|
| 0 a 10 | ✅ Completadas e integradas en `develop` |
| 11 — Documentación final | ✅ Integrada en `develop` (`904ce72`, merge `--no-ff` de `49b7f33`) |
| 12 — QA final y auditoría de entrega | ✅ Completada en `release/qa-final` (**pendiente de revisión humana**) — veredicto: **APTO PARA PUBLICACIÓN** |
| Cierre Git + publicación en GitHub | ❌ Pendiente, bajo revisión humana |

**RF-01 a RF-27 constituyen la línea base funcional completa.** La Fase 12 no cambió código, configuración, reglas de negocio ni RF: solo documentación.

## Reglas de negocio vigentes (aprobadas; sin cambios)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras la decisión final, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 12 — resultados reales del QA final

| Verificación | Resultado |
|---|---|
| RF-01 a RF-27 | 27/27 ✅ (rutas, código, Policies, páginas, PHPUnit y Cypress verificados) |
| PHPUnit | 244 pruebas · 236 passed · **0 failed** · 8 skipped · 1074 assertions · 32,25 s |
| Cypress | 14 specs · 43/43 · **0 failed** · 0 skipped · 03:32 · Electron 136 |
| `npm run build` | Correcto |
| `npx tsc --noEmit` | 0 errores |
| Migraciones | 17 aplicadas, 0 pendientes (normal y E2E) |
| Datos demo | 2 organizaciones, 16 usuarios `.test`, 7 CV PDF ficticios |
| Smoke | `/health` 200 (base de datos y Redis ok), `/login` 200, `/empleos` 200, `/dashboard` → login sin sesión, `/__e2e/reset` 404 en el entorno normal |
| *Healthchecks* | `app`, `queue`, `postgres`, `redis`, `app-e2e` y `queue-e2e` *healthy* |
| Secretos | Ninguno versionado (`.env`, `.env.e2e`, logs, *dumps*, CV privados: 0) |
| Defectos nuevos | Ninguno |

## Documentos creados o actualizados en la Fase 12

- `docs/final-report/diagram-reports/01` a `09`: informes escritos de los diagramas (sin recrear gráficos ni editar los `.oom`).
- `docs/final-report/delivery-checklist.md` (con «GitHub publicado» sin marcar).
- `docs/final-report/qa-final-report.md` (veredicto y justificación).
- Resultados del QA final en los capítulos 12 y 13 y en `docs/testing/cypress-e2e.md`.
- Referencias con fecha de consulta (13 de septiembre de 2026).
- Enlaces a los informes de diagramas en `evidence-index.md` y en los capítulos 6 y 14.
- Estado del README.

## Pendientes (equipo)

1. Anexar los BPMN AS-IS y TO-BE originales y los documentos previos de casos de uso.
2. Seleccionar o recapturar las capturas del informe, incluidas Cypress y Docker.
3. Actualizar gráficamente los diagramas de selección y despliegue (opcional).

## Git

- Rama: `release/qa-final` (desde `develop` en `904ce72`). Ramas `main`, `develop` y `feature/*` preservadas.
- Sin remoto, sin push, sin *tag*, sin merge a `main`.

## Siguiente paso (bajo revisión humana)

Cierre Git y publicación en GitHub:
1. Integrar `release/qa-final` en `develop` y luego en `main`.
2. Crear el *tag* de versión.
3. Crear el remoto y hacer `push`.

## Publicación (completada)

Repositorio publicado en https://github.com/luivmz/saas-reclutamiento-multiempresa: `main` (rama por defecto), `develop`, `release/qa-final` y las 10 ramas `feature/*`, más el tag `v1.0.0-academic` (`9a946c2`).

## Post-publicación — Corrección CI GitHub Actions

- **Problema:** el workflow heredado `.github/workflows/tests.yml` fallaba en GitHub Actions durante `composer install`.
- **Causa:** usaba PHP 8.3, mientras Symfony 8.1 (bloqueado en `composer.lock`) requiere PHP ≥ 8.4.1. Además, ejecutaba comandos del *starter kit* (`composer setup`, `composer ci:check`: PHPStan, Pint, *lint*) ajenos a la validación del proyecto. Por separado, `composer.lock` tenía un `content-hash` desincronizado desde el *bootstrap*.
- **Solución:**
  - Workflow con PHP 8.4, Node 22.23.2 y PostgreSQL 17.11.
  - Pasos: `composer install`, `npm ci`, `npm run build`, `npx tsc --noEmit` y `php artisan test`, con variables ficticias de CI y sin Redis (no requerido).
  - `composer update --lock`: solo cambió el `content-hash`, sin variar versiones.
  - Rama `fix/github-actions-ci`, commit `05e6fb1`; merges `c83f232` (`main`) y `7b1b7ef` (`develop`).
- **Workflow verde:** ejecuciones `34787563815` (rama de corrección), `34787861775` (`main`) y `34787885835` (`develop`), todas **success**.
- **Sin cambios funcionales:** no cambiaron RF, reglas, código de la aplicación ni Docker. El tag `v1.0.0-academic` se conserva.
- **Detalle:** `docs/final-report/post-publication-ci-fix.md`.
