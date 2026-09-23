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

## v1.1 — Fase 18: rediseño frontend integral

- **Rama:** `feature/phase-18-frontend-redesign`, desde `develop` en `0d2ce42` (cierre de la Fase 17).
- **Alcance:** solo interfaz. Sistema de diseño propio (tipografía IBM Plex, tokens de estado, barra lateral oscura), `DataTable` y `Section` reutilizables, accesibilidad (enlace de salto, foco visible único, `aria-current`/`aria-pressed`, tablas con `scope` y `caption`), responsive verificado a 1440/1280/768/390 px, modo oscuro y traducción al español del módulo de configuración.
- **Sin cambios** en reglas de negocio, RF, rutas, contratos de API, modelos, Policies, migraciones ni servicio ML. RF-29 sigue siendo experimental y la decisión final sigue siendo humana (RF-23).
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 18 pruebas de componente (`vp test`) · `tsc` sin errores · `npm run build` correcto · Cypress 17 specs / 61 pruebas, 61 pasadas.
- **Detalle y evidencia:** `docs/v1.1/phase-18-frontend-redesign.md` y `docs/v1.1/phase-18-screenshots/`.
- **Sin `push`, `merge`, *tag* ni *release*.**

## v1.1 — Fase 19: animaciones y microinteracciones

- **Rama:** `feature/phase-19-animations`, desde `develop` en `11832ac` (cierre de la Fase 18).
- **Alcance:** solo movimiento. Sistema de tres curvas y una escala de duración declarado con los tokens que Tailwind ya usa; corrección del movimiento heredado del kit de inicio (curvas lineales, `transition-all`, 500 ms de apertura, menús creciendo desde el centro); respuesta del botón a la pulsación; entrada de errores de formulario y del resultado de riesgo operacional. **Sin biblioteca de motion nueva.**
- **Se anima poco a propósito:** sin transiciones entre páginas, sin entrada animada de filas de tabla, sin contadores y sin badges que laten.
- **`prefers-reduced-motion` implementado y probado:** se conservan color y opacidad, se elimina todo desplazamiento, el spinner sigue girando y el esqueleto deja de latir.
- **Defecto de accesibilidad encontrado y corregido:** al cerrar la navegación móvil el foco se perdía en `body`; ahora vuelve al botón que la abrió.
- **Sin cambios** en reglas de negocio, RF, rutas, contratos de API, modelos, Policies, migraciones ni servicio ML.
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 23 pruebas de componente · `tsc` sin errores · `npm run build` correcto · Cypress 18 specs / 69 pruebas · 0 desbordes horizontales.
- **Detalle:** `docs/v1.1/phase-19-animations.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**

## v1.1 — Fase 20: experiencia 3D contextual

- **Rama:** `feature/phase-20-3d-experience`, desde `develop` en `67a88a6` (cierre de la Fase 19).
- **Alcance:** una sola superficie, la portada pública. Detrás del expediente de la portada, una pila de hojas en perspectiva, cada una con el tono de su etapa. Decorativa, opcional y sin información propia (ADR-003).
- **Tecnología:** CSS 3D (perspectiva y capas de DOM), **sin WebGL y sin dependencias nuevas**. `package.json` no cambia.
- **Presupuesto:** *bundle* inicial JS **+0 KB**; la escena va en su propio fragmento diferido (1.26 kB gzip) que solo se descarga en escritorio, sin movimiento reducido ni ahorro de datos, y al entrar en el viewport. 61 FPS con el puntero en movimiento; escena lista en ≈ 500 ms.
- **Fallback:** póster estático con la misma idea en plano, visible al instante; queda con movimiento reducido, en móvil, con ahorro de datos, en equipos modestos o si el fragmento falla. Sin WebGL la escena se muestra igual.
- **Gobierno:** ADR-003 y RNF-C seguían «pendiente de decisión»; se anotaron sin reescribir su historia. La promoción formal de RNF-C sigue siendo decisión del equipo.
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 36 pruebas de componente · `tsc` sin errores · `npm run build` correcto · Cypress 19 specs / 77 pruebas · 0 desbordes horizontales.
- **Detalle:** `docs/v1.1/phase-20-3d-experience.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**
