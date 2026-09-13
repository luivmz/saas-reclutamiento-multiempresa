# Docker y portabilidad

El proyecto se ejecuta completo con Docker Compose. No necesita XAMPP, Apache, MySQL, PHP, Composer, PostgreSQL ni Redis instalados en la PC.

## 1. Arquitectura de contenedores

Monolito modular Laravel 13 + Inertia/React. No hay microservicios ni un contenedor de frontend separado: Vite compila los assets dentro del contenedor `app`.

| Servicio | Imagen | Función | Puerto en el host | Healthcheck |
|---|---|---|---|---|
| `app` | `reclutamiento-php:dev` (`docker/php/Dockerfile`) | Laravel (`php artisan serve`). Al iniciar instala dependencias si faltan, genera `APP_KEY`, compila assets y migra. | `${APP_PORT:-8000}` | `GET /health` responde 200 solo si PostgreSQL y Redis están accesibles |
| `queue` | `reclutamiento-php:dev` | Worker de colas (notificaciones) con la misma configuración que `app` | — | El proceso `queue:work` está vivo y `queue:monitor redis:default` alcanza Redis |
| `postgres` | `postgres:17.11-alpine` | Base de datos (`reclutamiento`, y `reclutamiento_testing` para PHPUnit) | `127.0.0.1:${FORWARD_DB_PORT:-5432}` | `pg_isready` |
| `redis` | `redis:7.4.11-alpine` | Sesiones, caché y colas | `127.0.0.1:${FORWARD_REDIS_PORT:-6379}` | `redis-cli ping` |
| `app-e2e` *(perfil `e2e`)* | `reclutamiento-php:dev` | Aplicación aislada para Cypress (`APP_ENV=e2e`, lee `.env.e2e`) | `127.0.0.1:${E2E_APP_PORT:-8001}` | `GET /health` |
| `queue-e2e` *(perfil `e2e`)* | `reclutamiento-php:dev` | Worker del entorno E2E | — | Igual que `queue` |
| `cypress` *(perfil `e2e`)* | `cypress/included:15.3.0` | Ejecuta la suite E2E contra `http://app-e2e:8000` | — | — |

Orden de arranque:
- `postgres` y `redis` (healthy) → `app` (healthy) → `queue`.
- Con el perfil E2E: `app` (healthy) → `app-e2e` (healthy) → `queue-e2e` (healthy) → `cypress`.

Todos los servicios de larga duración usan `restart: unless-stopped`. El worker usa `--max-time=3600`: termina cada hora y Docker lo reinicia, lo que evita procesos con código antiguo.

Volúmenes con nombre: `pgdata`, `redisdata`, `vendor` y `node_modules`. El código fuente se monta desde el repositorio.

### Versiones fijadas

| Componente | Versión |
|---|---|
| PHP | 8.4.25 (`php:8.4.25-cli-bookworm`, Debian 12) |
| Composer | 2.10.3 |
| Node / npm | 22.23.2 / 10.9.8 |
| Extensión phpredis | 6.3.0 |
| PostgreSQL | 17.11 (alpine) |
| Redis | 7.4.11 (alpine) |
| Cypress / navegador | 15.3.0 / Electron 136 |

Las versiones del `Dockerfile` son `ARG` (`PHP_VERSION`, `NODE_VERSION`, `COMPOSER_VERSION`, `PHPREDIS_VERSION`).

## 2. Requisitos

- Docker Desktop (Windows/macOS) o Docker Engine (Linux) con **Docker Compose ≥ 2.24**. Este proyecto se validó con Docker 27.4.0 y Compose 2.31.
- Git. El repositorio fuerza finales de línea LF (`.gitattributes`), por lo que los scripts `.sh` funcionan también en clones hechos en Windows.
- Opcional: Node/npm en el host, solo para usar los atajos `npm run ...` (los comandos Docker equivalentes se indican abajo) y para `cy:open`.
- Puertos libres en el host: 8000 (app), 5432 y 6379 (solo loopback) y 8001 (app-e2e). Todos son configurables en `.env`.

## 3. Variables de entorno

| Archivo | Uso | ¿Versionado? |
|---|---|---|
| `.env.example` | Plantilla del entorno de desarrollo y demostración | Sí (sin secretos reales; `DB_PASSWORD=secret` es un valor de desarrollo) |
| `.env` | Entorno de `app` y `queue`. Si no existe, el entrypoint lo crea desde `.env.example` y genera `APP_KEY`. | **No** |
| `.env.e2e.example` | Plantilla del entorno E2E aislado | Sí |
| `.env.e2e` | Entorno de `app-e2e`, `queue-e2e` y `cypress`. Lo crea `npm run e2e:setup` con `APP_KEY` y `E2E_TOKEN` aleatorios (no se muestran). | **No** |

Variables principales:
- **Aplicación:** `APP_URL`, `APP_PORT`, `APP_TIMEZONE=America/Lima`, `APP_LOCALE=es`.
- **PostgreSQL:** `DB_HOST=postgres`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `FORWARD_DB_PORT`.
- **Redis:** `REDIS_HOST=redis`, `FORWARD_REDIS_PORT`.
- **Colas, sesiones y caché:** `QUEUE_CONNECTION=redis`, `SESSION_DRIVER=redis`, `CACHE_STORE=redis`.
- **Correo:** `MAIL_MAILER=log` (los correos se escriben en el log).
- **CV:** `CV_MAX_KB`.
- **E2E:** `E2E_ENABLED`, `E2E_TOKEN`, `E2E_DATABASE`, `E2E_APP_PORT`.

Si cambia `DB_USERNAME` o `DB_PASSWORD` en `.env`, replique el cambio en `.env.e2e`.

## 4. Instalación desde cero

Desde la raíz del repositorio:

```powershell
# 1. (Opcional) Crear .env y ajustar puertos si 8000/5432/6379 están ocupados.
#    Si no existe, el contenedor app lo crea desde .env.example.
copy .env.example .env          # Linux/macOS: cp .env.example .env

# 2. Construir la imagen y levantar los servicios.
#    La primera vez tarda varios minutos: composer install, npm ci, npm run build, key:generate y migraciones.
docker compose up -d --build --wait

# 3. Cargar los datos de demostración (borra y recrea la base de desarrollo).
docker compose exec app php artisan migrate:fresh --seed --force      # o: npm run demo:reset

# 4. Abrir http://localhost:8000. Usuarios y contraseñas ficticios: docs/demo-users.md
```

Comprobación rápida:

```powershell
docker compose ps                         # app, postgres, redis y queue en estado (healthy)
curl http://localhost:8000/health         # {"status":"ok",...}
```

## 5. Operación diaria

| Acción | Comando |
|---|---|
| Iniciar | `docker compose up -d --wait` |
| Detener (conserva datos) | `docker compose stop` o `docker compose down` |
| Detener y **borrar datos** (volúmenes del proyecto) | `docker compose down -v` (se pierden la base, Redis, `vendor` y `node_modules`; se recrean al volver a iniciar) |
| Reconstruir la imagen | `docker compose build` y luego `docker compose up -d --wait` |
| Estado | `docker compose ps` |
| Logs | `docker compose logs -f app` · `docker compose logs -f queue` |
| Migraciones | `docker compose exec app php artisan migrate` |
| Datos demo | `docker compose exec app php artisan migrate:fresh --seed --force` |
| Reiniciar el worker (tras cambiar código de jobs o notificaciones) | `docker compose restart queue` |
| Artisan / Composer / npm | `docker compose exec app php artisan ...` · `docker compose exec app composer ...` · `docker compose exec app npm ...` |

### Assets (Vite)

- **Ejecución demostrable (por defecto):** la app sirve los assets compilados de `public/build`. El entrypoint los compila si no existen. Tras cambiar el frontend: `docker compose exec app npm run build`.
- **Desarrollo con recarga en caliente:** el HMR de Vite **no está configurado** dentro de Docker (se necesitaría exponer 5173 y configurar `server.hmr`). Se recompila con `npm run build`; es suficiente para este MVP.

### Storage

- Los CV se guardan en el disco privado local `storage/app/private`, montado desde el repositorio e ignorado por Git. No se descargan por URL pública, así que no hace falta `storage:link`.
- El entrypoint crea los directorios de `storage/` y `bootstrap/cache` si faltan.

## 6. Pruebas

### PHPUnit

```powershell
docker compose exec app php artisan test
```

Usa la base `reclutamiento_testing`, creada por `docker/postgres/init/01-create-testing-db.sql`, con variables forzadas en `phpunit.xml`: caché y sesión en memoria, cola síncrona y `E2E_ENABLED=false`.

### Cypress (entorno E2E aislado)

```powershell
npm run cy:run                                          # suite completa
npm run cy:run -- --spec "cypress/e2e/e2e-10-*.cy.js"   # un spec
npm run cy:open                                         # modo interactivo en el host (http://localhost:8001)
```

`cy:run` equivale a:

```powershell
docker compose run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh   # crea .env.e2e si falta
docker compose --profile e2e run --rm cypress                                      # levanta app-e2e y queue-e2e y ejecuta
```

Al terminar, los servicios E2E pueden detenerse con `docker compose --profile e2e stop app-e2e queue-e2e`.

Detalle de specs y resultados en `docs/testing/cypress-e2e.md`.

## 7. Estrategia normal vs E2E

| Aspecto | Normal (`app`, `queue`) | E2E (`app-e2e`, `queue-e2e`, `cypress`) |
|---|---|---|
| Activación | `docker compose up` | Perfil `e2e` (`--profile e2e`) |
| Archivo de entorno | `.env` | `.env.e2e` (`APP_ENV=e2e`) |
| Base de datos | `reclutamiento` (demo/desarrollo) | `reclutamiento_e2e` |
| Redis | DB 0 (sesiones y cola), DB 1 (caché) | DB 2 (sesiones y cola), DB 3 (caché), prefijos propios |
| Endpoints `/__e2e/*` | Inertes (`E2E_ENABLED=false`, responden 404) | Activos con `X-E2E-Token` |
| Reset destructivo | **Rechazado** | Permitido solo si la base activa es `E2E_DATABASE` |

Protecciones del reset (`e2e:reset`, `POST /__e2e/reset`), cubiertas por `E2eSupportTest` y `E2eEnvironmentTest`:

1. Responde 404 si `E2E_ENABLED` no está activo o el entorno es producción.
2. Responde 403 sin el token correcto.
3. Responde 409, o el comando falla, si la base activa no es exactamente `E2E_DATABASE`.
4. `E2eEnvironment::reset()` vuelve a verificar la base antes de ejecutar `migrate:fresh`.

## 8. Reset controlado

| Qué | Comando | Efecto |
|---|---|---|
| Datos demo de desarrollo | `npm run demo:reset` | `migrate:fresh --seed` en `reclutamiento` |
| Datos del entorno E2E | `npm run e2e:reset` | `e2e:reset` en `app-e2e` (`reclutamiento_e2e`) |
| Todo desde cero | `docker compose --profile e2e down -v` y luego `docker compose up -d --build --wait` | Borra los volúmenes **del proyecto** |

## 9. Seguridad

- `.env` y `.env.e2e` están en `.gitignore` y en `.dockerignore`; nunca se copian a la imagen.
- `.env.example` y `.env.e2e.example` no contienen tokens ni claves reales.
- PostgreSQL, Redis y `app-e2e` solo se publican en `127.0.0.1`.
- `app` se publica en todas las interfaces para poder mostrar la demo en la red local. Para restringirlo: `APP_PORT=127.0.0.1:8000`.
- La imagen es de **desarrollo y demostración**: `php artisan serve`, procesos como `root` y `APP_DEBUG=true`. No es una imagen de producción (A-36).

## 10. Solución de problemas

| Síntoma | Causa y solución |
|---|---|
| `port is already allocated` | Otro programa usa el puerto. Cambie `APP_PORT`, `FORWARD_DB_PORT`, `FORWARD_REDIS_PORT` o `E2E_APP_PORT` en `.env`. |
| `app` tarda en quedar `healthy` la primera vez | Está ejecutando `composer install`, `npm ci` y `npm run build`. Siga el avance con `docker compose logs -f app`. El healthcheck espera hasta 240 s de arranque. |
| La página carga sin estilos o con error de `manifest.json` | Faltan assets: `docker compose exec app npm run build`. |
| `app-e2e` no arranca: `database "reclutamiento_e2e" does not exist` | El volumen de PostgreSQL es anterior a la Fase 10 (los scripts de inicio solo corren al crearlo). Ejecute una vez: `docker compose exec postgres psql -U reclutamiento -d reclutamiento -c "CREATE DATABASE reclutamiento_e2e"`. |
| Cypress falla con 403 en `/__e2e/reset` | Falta `.env.e2e` o el token: `npm run e2e:setup` (para rotar el token, borre `.env.e2e` y repita). |
| `/__e2e/reset` responde 409 | La base activa no es la E2E. Revise `DB_DATABASE` y `E2E_DATABASE` en `.env.e2e`. |
| Notificaciones que no aparecen | El worker no está activo: `docker compose ps queue` y `docker compose logs queue`. |
| `exec ... entrypoint.sh: not found` o `\r` en scripts | Clon con finales CRLF de una versión antigua: `git add --renormalize .` o vuelva a clonar (`.gitattributes` fuerza LF). |
| Archivos de `storage/` propiedad de `root` (Linux) | Los contenedores de desarrollo corren como `root`: `sudo chown -R $USER storage bootstrap/cache`. |
| Mensajes `dbus` en la salida de Cypress | Ruido de Electron dentro del contenedor, sin efecto. |

## 11. Validación de portabilidad (Fase 10, 2026-09-13)

**Instalación desde cero:**
- Se hizo un `git clone` limpio de la rama `feature/docker-portability` (commit `ccf05d1`) en una carpeta temporal, sin `.env`, `vendor/` ni `node_modules/`.
- Se levantó como otro proyecto de Compose (`-p reclutamiento-clean`), con volúmenes nuevos y otros puertos (8100, 55432, 56379 y 8101), sin tocar el entorno principal.
- Al terminar se eliminaron sus volúmenes (`down -v`) y la carpeta.

| Paso | Resultado real |
|---|---|
| `docker compose up -d --build --wait` | Exit 0 en **87 s**; `app`, `postgres`, `redis` y `queue` en estado **healthy** |
| `.env` | Creado por el entrypoint desde `.env.example`, con `APP_KEY` generada |
| Scripts de inicio de PostgreSQL | Bases `reclutamiento`, `reclutamiento_e2e` y `reclutamiento_testing` creadas |
| Migraciones | 17 ejecutadas, 0 pendientes |
| `migrate:fresh --seed` | Exit 0: 2 organizaciones, 16 usuarios, 11 requerimientos, 5 vacantes, 10 postulaciones y 110 registros de auditoría |
| Smoke HTTP | `/health` 200 (`{"status":"ok","checks":{"database":"ok","redis":"ok"}}`), `/login` 200, `/empleos` 200 con la vacante demo visible |
| `POST /__e2e/reset` en el entorno normal | 404 (inerte) |
| PHPUnit | **244 pruebas: 236 passed, 8 skipped, 0 failed (1074 assertions)**, en 36 s |
| `init-e2e-env.sh` (`e2e:setup`) | Exit 0; `.env.e2e` creado |
| Cypress (perfil `e2e`, contra `app-e2e`) | **14 specs · 43 tests · 43 passed · 0 failed · 03:26** · Electron 136 · `app-e2e` y `queue-e2e` healthy |
| Aislamiento de datos | Tras la suite, la base `reclutamiento` conservaba el seed intacto (11 requerimientos, 5 vacantes); los datos de las pruebas quedaron solo en `reclutamiento_e2e` (12 requerimientos, 6 vacantes) |

**Entorno principal**, tras recrearlo con el nuevo `docker-compose.yml` e imágenes fijadas:
- Los cuatro servicios quedaron healthy, incluido `queue` con su nuevo healthcheck.
- PostgreSQL y Redis se publican en `127.0.0.1`.
- `POST /__e2e/reset` responde 404.
- La base `reclutamiento_e2e` se creó manualmente, porque el volumen existente es anterior a la Fase 10 (ver solución de problemas).
- Resultados:

  | Verificación | Resultado real |
  |---|---|
  | PHPUnit | 244 pruebas: 236 passed, 8 skipped, 0 failed (1074 assertions) |
  | `npm run build` | OK |
  | `npx tsc --noEmit` | 0 errores |
  | `npm run cy:run` | 14 specs · 43/43 · 03:34 |
  | Aislamiento | La base de desarrollo tenía 12 requerimientos, 6 vacantes y 16 usuarios antes de la suite y los mismos valores después |
