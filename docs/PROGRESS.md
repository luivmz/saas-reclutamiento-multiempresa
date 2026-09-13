# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/docker-portability`

## Fases

| Fase | Estado |
|---|---|
| 0 a 8 | ✅ Completadas e integradas en `develop` |
| 9 — Suite E2E Cypress | ✅ Integrada en `develop` (`e0c8825`, merge `--no-ff` de `a77c916`) |
| 10 — Docker y portabilidad | ✅ Completada en `feature/docker-portability` (**pendiente de revisión; no fusionada en `develop`**) |
| 11 a 12 | ❌ Pendientes |

**RF-01 a RF-27 constituyen la línea base funcional completa.** La Fase 10 no cambió reglas de negocio ni RF.

## Reglas de negocio vigentes de la Fase 6 (aprobadas; sin cambios)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras la decisión final, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 10 — lo realizado

- **Integración de la Fase 9:** merge en `develop` (`e0c8825`). Verificación posterior: PHPUnit 240 (232 passed, 8 skipped) y `tsc` sin errores.
- **Imágenes fijadas:** PHP 8.4.25 (bookworm), Composer 2.10.3, Node 22.23.2 (npm 10.9.8), phpredis 6.3.0, PostgreSQL 17.11-alpine, Redis 7.4.11-alpine y Cypress 15.3.0. Las versiones del `Dockerfile` son `ARG`.
- **Compose:**
  - `restart: unless-stopped` en los servicios de larga duración.
  - Healthcheck del worker: proceso `queue:work` vivo y `queue:monitor` contra Redis. El worker usa `--max-time=3600`.
  - PostgreSQL, Redis y `app-e2e` publicados solo en `127.0.0.1`.
  - Anclas YAML compartidas (`x-php` y los healthchecks).
- **Entorno E2E aislado (DEF-13, A-35):**
  - Servicios `app-e2e` y `queue-e2e` en el perfil `e2e`, con `APP_ENV=e2e`, lo que hace que Laravel cargue `.env.e2e`.
  - Base `reclutamiento_e2e`, Redis DB 2 y 3, y token propio.
  - El entorno normal mantiene `E2E_ENABLED=false`.
  - El reset rechaza cualquier base distinta de `E2E_DATABASE` (409, comando fallido o excepción del servicio).
  - `init-e2e-env.sh` y `npm run e2e:setup` generan `.env.e2e` con `APP_KEY` y token aleatorios.
  - Script `docker/postgres/init/02-create-e2e-db.sql`.
- **Fechas E2E (DEF-12):** helper `cypress/support/dates.js` (`appDate`) en `America/Lima`, spec de soporte `e2e-00-app-dates.cy.js`, y E2E-04 y E2E-13 actualizados.
- **Entrypoint:** usa `.env` o `.env.e2e` según `APP_ENV`, crea los directorios de `storage/` y mantiene la instalación idempotente (Composer, npm, build, clave y migraciones).
- **Configuración:**
  - `.env.example` completado y ordenado, sin secretos; incluye `E2E_DATABASE` y `E2E_APP_PORT`.
  - Nuevo `.env.e2e.example`.
  - `.env.e2e` agregado a `.gitignore`.
  - `.dockerignore` ampliado.
  - Scripts npm `demo:reset`, `e2e:setup`, `e2e:up`, `e2e:reset`, `cy:run` y `cy:open`.
- **Documentación:**
  - Nuevos: `docs/docker.md` y `README.md`.
  - Actualizados: `docs/testing/cypress-e2e.md`, `docs/rf-implementation-matrix.md`, `docs/defects.md` (DEF-12 y DEF-13) y `docs/assumptions.md` (A-35 y A-36).
- **Rutas personales:** no hay rutas de Windows en la configuración versionada (la única coincidencia, `.claude/settings.local.json`, está ignorada). `.gitattributes` fuerza LF.

## Pruebas ejecutadas (resultados reales)

| Verificación | Resultado |
|---|---|
| `E2eSupportTest` + `E2eEnvironmentTest` | RED: 4 failed y 7 passed → GREEN: **11 passed (29 assertions)** |
| Instalación limpia: `up --build --wait` | Exit 0 en 87 s; 4 servicios healthy; `.env` creado por el entrypoint |
| Instalación limpia: migraciones y seed | 17 migraciones, 0 pendientes; seed con 2 organizaciones, 16 usuarios, 11 requerimientos, 5 vacantes y 10 postulaciones |
| Instalación limpia: smoke | `/health` 200, `/login` 200, `/empleos` 200; `/__e2e/reset` 404 en el entorno normal |
| Instalación limpia: PHPUnit | 244 pruebas: 236 passed, 8 skipped, 0 failed |
| Instalación limpia: Cypress | 14 specs · 43/43 · 03:26 |
| Entorno principal: PHPUnit completo | **244 pruebas: 236 passed, 8 skipped, 0 failed (1074 assertions)** |
| Entorno principal: `npm run build` | OK |
| Entorno principal: `npx tsc --noEmit` | 0 errores |
| Entorno principal: Cypress completo (`npm run cy:run`) | **14 specs · 43 tests · 43 passed · 0 failed · 0 skipped · 03:34** · Electron 136 |
| Aislamiento de datos | La base de desarrollo no cambió tras las suites en ambos entornos |

## Seguridad

- `.env` y `.env.e2e` no están versionados (verificado con `git ls-files` y `git check-ignore`).
- Ningún archivo versionado contiene el token E2E (verificado con `git grep`, sin mostrar el valor).
- `.env.example` y `.env.e2e.example` no contienen secretos; `DB_PASSWORD=secret` es un valor de desarrollo.

## Git

- Rama: `feature/docker-portability` (desde `develop` en `e0c8825`).
- Commits: `ccf05d1` (configuración Docker y E2E) y el commit final de documentación.
- Sin push. **No fusionar en `develop` hasta la revisión del equipo.**

## Pendientes reales

- El HMR de Vite no está configurado dentro de Docker; tras cambios del frontend se usa `npm run build`.
- La imagen es de desarrollo y demostración (`php artisan serve`, `root`, `APP_DEBUG=true`); no hay imagen de producción (A-36).
- Los CV de las pruebas E2E comparten `storage/app/private` con el entorno normal (A-35).
- En volúmenes de PostgreSQL anteriores a la Fase 10, `reclutamiento_e2e` debe crearse una vez a mano (documentado).
- `cy:open` sigue sin ejecutarse y solo se probó Electron.

## Siguiente tarea exacta para retomar

1. Revisión de la Fase 10; si se aprueba, merge `--no-ff` de `feature/docker-portability` a `develop`.
2. Fase 11 según el plan maestro (no iniciada).
