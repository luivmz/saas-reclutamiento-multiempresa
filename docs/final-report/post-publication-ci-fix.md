# Corrección post-publicación del CI (GitHub Actions)

**Clasificación:** incidencia de configuración de integración continua post-publicación. No es un defecto funcional ni un RF nuevo. La línea base RF-01 a RF-27 no cambió.

## 1. Contexto

- El repositorio ya estaba publicado en https://github.com/luivmz/saas-reclutamiento-multiempresa, con el tag académico `v1.0.0-academic` en `9a946c2`.
- El QA final (Fase 12) estaba aprobado con veredicto «APTO PARA PUBLICACIÓN» ([qa-final-report.md](qa-final-report.md)).
- El repositorio incluía un workflow heredado del *starter kit* de Laravel, `.github/workflows/tests.yml`, que no se había adaptado al proyecto. GitHub lo ejecutó al publicar `main`.

## 2. Problema detectado

GitHub Actions fallaba en el workflow `tests` durante la instalación de dependencias de Composer, antes de ejecutar cualquier prueba.

## 3. Causa raíz

1. **Versión de PHP incompatible.** El workflow usaba PHP 8.3 (el runner tenía 8.3.33), pero `composer.lock` fija Symfony 8.1, que requiere PHP ≥ 8.4.1. El proyecto está validado en Docker con PHP 8.4.25.
2. **Comandos heredados que no representaban la estrategia del proyecto:**
   - `composer setup` ejecutaba `npm install`, `key:generate` y migraciones contra la base configurada en `.env`, no contra una base de pruebas.
   - `composer ci:check` ejecutaba `npm run check` (*lint* de vite-plus), `phpstan analyse` (Larastan) y `pint --test`. Ninguno formaba parte de la validación aprobada.
   - No había servicio PostgreSQL: el proyecto no usa SQLite ni MySQL para pruebas.
3. **Aviso de *lock* desincronizado** (independiente de lo anterior). `composer validate` informaba que `composer.lock` no estaba al día con `composer.json`. El desfase venía del *bootstrap* (`e87ef39`), es decir, de los archivos originales del *starter kit*. En la instalación solo generaba una advertencia; no era la causa del fallo.

## 4. Impacto

| Ámbito | ¿Afectado? |
|---|---|
| Funcionalidad (RF-01 a RF-27) | No |
| Entorno Docker validado | No |
| PHPUnit local (Docker) | No |
| Cypress E2E | No |
| Datos, seguridad, multiempresa | No |
| Integración continua en GitHub | **Sí**: el workflow fallaba en rojo |

## 5. Corrección aplicada (`.github/workflows/tests.yml`)

| Aspecto | Antes | Después |
|---|---|---|
| PHP | 8.3 | **8.4** (`shivammathur/setup-php`, mismo SHA fijado) |
| Extensiones PHP | Por defecto | `mbstring, dom, fileinfo, intl, bcmath, zip, pdo_pgsql, pgsql`, derivadas de `composer check-platform-reqs` y del `Dockerfile` |
| Node | 22 | **22.23.2** (igual que Docker), con caché de npm |
| Base de datos | Ninguna | Servicio **PostgreSQL 17.11-alpine** (`reclutamiento_testing`) con *healthcheck* |
| Redis | — | **No se agrega**: PHPUnit pasa con Redis inalcanzable porque `phpunit.xml` fuerza caché y sesión en memoria y cola síncrona |
| Variables de entorno | — | Solo valores ficticios de CI: `APP_ENV=testing`, `APP_DEBUG=false`, `APP_TIMEZONE=America/Lima`, conexión `pgsql` a `127.0.0.1` con usuario `reclutamiento` y contraseña `ci-testing-only` |
| Pasos | `composer setup`, `composer ci:check` | `composer install` (desde el *lock*), `cp .env.example .env` + `php artisan key:generate`, `npm ci`, `npm run build`, `npx tsc --noEmit`, `php artisan test` |
| Disparadores | *push* a `main`, *pull request* | *push* a `main`, `develop`, `release/**` y `fix/**`; *pull request*; ejecución manual |

`npm run build` se ejecuta antes de `tsc` porque genera los tipos de rutas de Wayfinder que TypeScript necesita.

Cypress no se incluye en el CI: está validado mediante Docker (`docs/testing/cypress-e2e.md`) y su incorporación queda como mejora futura.

## 6. Composer lock

- **Diagnóstico:** `composer validate` terminaba con exit 2 («The lock file is not up to date»). `composer update --lock --dry-run` respondió «Nothing to modify in lock file», y `composer install --dry-run`, «Nothing to install, update or remove».
- **Corrección:** `composer update --lock`, que solo recalcula el hash del *lock* sin resolver ni actualizar paquetes. El único cambio en `composer.lock` fue la línea `content-hash` (`d0a5f283…` → `a89a9d0f…`).
- **Después:** `composer validate` terminó con exit 0 («./composer.json is valid») y `composer install --dry-run` volvió a responder «Nothing to install, update or remove».
- **No hubo** *upgrade* ni *downgrade* de dependencias, ni cambios en `composer.json`.

## 7. Evidencia

| Evidencia | Valor |
|---|---|
| Rama de corrección | `fix/github-actions-ci` (desde `main` `9a946c2`) |
| Commit de corrección | `05e6fb1` · `fix: align GitHub Actions with PHP 8.4 project runtime` (archivos: `.github/workflows/tests.yml`, `composer.lock`) |
| Actions en la rama de corrección | Ejecución `34787563815` · **success** · 64 s · 0 anotaciones · https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/34787563815 |
| Merge en `main` | `c83f232` · `merge: align GitHub Actions with PHP 8.4 runtime` |
| Actions en `main` | Ejecución `34787861775` · **success** · https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/34787861775 |
| Merge en `develop` | `7b1b7ef` · `merge: sync GitHub Actions CI fix into develop` |
| Actions en `develop` | Ejecución `34787885835` · **success** · https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/34787885835 |
| Pasos del job `ci` (las 3 ejecuciones) | Setup PHP 8.4, Setup Node 22, `composer install`, preparación del entorno, `npm ci`, *build*, TypeScript y PHPUnit: todos **success** |
| PHPUnit local (Docker, PHP 8.4.25) | 244 pruebas · 236 superadas · 0 fallidas · 8 omitidas · 1074 aserciones · 32,19 s |
| PHPUnit con Redis inalcanzable (local) | 244 pruebas · 236 superadas · 8 omitidas · 1074 aserciones |
| *Build* local | Correcto (19,81 s) |
| TypeScript local | 0 errores |

El detalle numérico de PHPUnit dentro de GitHub Actions no se transcribe: leer los logs de la ejecución requiere autenticación. El paso figura como **success** en la API pública.

## 8. Resultado

CI corregido y validado: el workflow `tests` refleja el entorno real del proyecto y pasa en verde en `fix/github-actions-ci`, `main` y `develop`.

- El tag `v1.0.0-academic` (`9a946c2`) **no se modificó**: representa el release académico original, y esta corrección es posterior.
- No hubo cambios funcionales, en RF ni en reglas de negocio.

## 9. Clasificación

**Incidencia de configuración de integración continua post-publicación.**
- No se registra como defecto funcional (DEF-xx) porque no afectó a la aplicación.
- No se registra como requerimiento nuevo.
