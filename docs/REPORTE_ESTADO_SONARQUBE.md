# REPORTE DE ESTADO – SaaS Reclutamiento Multiempresa

## 1. Resumen ejecutivo

Auditoría local realizada el **13/10/2026, aproximadamente 19:10–19:17, America/Lima**, sobre `main`, HEAD `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6`. Ruta absoluta: `/Users/luisvilameza/Universidad/Pruebas_Calidad/Project_SaaS/saas-reclutamiento-multiempresa`.

El proyecto contiene un SaaS académico v1.1 con Docker, PHPUnit, Cypress, pruebas de componentes Vitest, TypeScript, PHPStan/Larastan y Pint configurados. El frontend usa Vite Plus con Oxlint/Oxfmt; **no se encontraron ESLint ni Prettier como herramientas instalables/configuradas del proyecto**. Las dependencias están resueltas en los locks; no se instalaron ni actualizaron.

El último trabajo publicado que muestra Git es el **handoff macOS posterior a F34E**, del 05/10/2026. `CLAUDE.md` y `docs/PROGRESS.md` declaran F34E cerrada, F35-SBX habilitada pero aún no iniciada, y fases productivas bloqueadas. Esta auditoría no inicia una fase funcional ni cambia RF-01 a RF-27, la decisión humana RF-23 o el carácter experimental de RF-29.

La evidencia QA detallada más reciente localizada es la de **F29F, 30/09/2026**, sobre `bc44303d307004de494c4e03f3186ee190118c4c`: PHPUnit 411 aprobadas, 8 omitidas, 0 fallidas y 1498 aserciones; Cypress 20 specs y 85/85; Vitest 42/42; pytest 533; build y TypeScript con salida 0. Pint terminó con salida 1 y 8 problemas de estilo; `vp check` con salida 1 y 226 archivos con formato pendiente. **Son resultados archivados, no ejecuciones de esta sesión.** La comparación Git entre ese commit y HEAD no mostró cambios en los directorios runtime, pruebas, locks, Docker y configuraciones de calidad inspeccionados.

**Estado operativo actual:** Docker Desktop existe en `/Applications/Docker.app`, pero el daemon no está disponible en el socket configurado; `/health` no responde. No se puede comprobar contenedores, imágenes descargadas, volúmenes, bases, Redis o colas. Hay `.env` y assets compilados; falta `.env.e2e`, `vendor/autoload.php` y `node_modules/.bin/vp` en el checkout. Los volúmenes Docker podrían contener dependencias, pero no se pueden consultar con el daemon inaccesible.

**SonarQube no es reproducible desde este repositorio en su estado actual.** No se encontró servidor/configuración de proyecto, URL, project key, token, Compose específico, script de análisis ni evidencia de un análisis anterior. Sí existe **SonarScanner CLI 8.1.0.6389 instalado en el host**, que responde a `--version` e indica `Project root configuration file: NONE`. Esto acredita la instalación del cliente, no un servidor ni un análisis completado. La experiencia anterior recordada por el usuario podría haber usado una configuración externa u otro equipo: no se puede reconstruir con la evidencia disponible.

Se identifican **10 grupos de problemas o pendientes importantes**, priorizados en §11. El proyecto tiene evidencia histórica sólida de pruebas funcionales, pero **no está listo todavía para repetir una demostración completa de SonarQube**.

Convenciones: **AS-IS** = archivos/salidas observados; **implementado** = presente en código, con evidencia histórica cuando se indique; **TO-BE** = pasos pendientes, no ejecutados. Una configuración existente no equivale a funcionamiento comprobado hoy.

## 2. Git

| Dato | Resultado AS-IS |
|---|---|
| Rama | `main`; se conservó por prohibición expresa de cambiar ramas |
| HEAD | `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6` |
| `origin/main` local | Mismo hash que HEAD; sin fetch ni comprobación remota en vivo |
| Origin fetch/push | `https://github.com/luivmz/saas-reclutamiento-multiempresa.git` |
| `git status -sb` inicial | `## main...origin/main` |
| Archivos rastreados modificados/staged iniciales | Ninguno |
| Archivos no rastreados, no ignorados, iniciales | Ninguno |
| Working tree inicial | Limpio |
| Working tree al entregar | Este reporte nuevo sin rastrear; sin commit |
| Git del host | `2.54.0 (Apple Git-157)` |

La regla habitual de `project-guardian` exige una rama de trabajo y commit al cerrar cambios. Para **esta auditoría** prevalece la autorización específica del usuario: permanecer en la rama actual, crear únicamente este reporte y no hacer commits. Tampoco se modifica documentación de fase ni matrices existentes.

Últimos 10 commits, todos fechados 05/10/2026:

```text
b67f644 merge: publish macOS handoff after F34E
36660ae merge: add macOS handoff after F34E
3a74e4a chore(docs): add macOS handoff after F34E
853d423 merge: publish F34E restricted synthetic authorization
ac6aed2 merge: close F34E restricted synthetic authorization
b7ca88d docs(governance): close F34E and enable synthetic F35-SBX only
c016a75 docs(academic): define restricted synthetic G0-SBX gate for F34E
0ea5e63 test(academic): harden post-phase and G0-SBX validation for F34E
9e0fc92 merge: integrate F34D academic closure
8a7e4ba merge: close F34D G0-12 institutional validation
```

Commits relevantes reconstruidos con `git log --all` y consultas por rutas:

| Tema | Evidencia Git |
|---|---|
| SonarQube / SonarScanner / SonarCloud | Sin coincidencias específicas en mensajes; sin coincidencias de `SonarQube`, `sonar-scanner`, `SONAR_TOKEN`, `sonar.projectKey` en cambios textuales consultados |
| Validadores académicos recientes | `0ea5e63` 05/10; `f68aef5` 05/10; `723001c` 04/10 |
| QA real F29F | `a5051d0` 30/09: registro de ejecución; `744d79f` 30/09: resumen QA, defectos y métricas |
| Plan/casos de pruebas | `84c1228` y `7d22c64`, 30/09 |
| QA global v1.1 | `bb94dd0` 24/09; prueba cross-tenant `9867ac1` 24/09 |
| Docker | `ccf05d1` 13/09: imágenes fijadas, aislamiento E2E y fechas |
| Cypress | `9edb0cd` 13/09: scaffold E2E; ampliaciones posteriores en `cypress/` |
| CI | `05e6fb1` 13/09: alineación con PHP 8.4; `9414dc3` documenta corrección |
| Cobertura | Consultas por mensaje encuentran documentación/trazabilidad; no se localizó implementación de Clover/LCOV o integración Sonar |

Hay archivos **ignorados**: `.env`, `.claude/settings.local.json`, `.phpunit.result.cache`, `public/build/`, bindings Wayfinder, cachés de Laravel, logs, `storage/app/private/cvs/` y `vendor/`, entre otros. No son modificaciones rastreadas. No se inspeccionó el contenido de CV ni se certificó su origen; para la exposición deben usarse únicamente fixtures ficticios. Los artefactos ignorados no prueban una ejecución actual.

## 3. Stack y versiones

Versiones del lock distinguidas de requisitos declarados y runtimes del host. Docker no se inició para medir versiones actuales de contenedores.

| Tecnología | Versión | Fuente |
|---|---|---|
| Laravel | `v13.31.0`; requisito `^13.17` | `composer.lock`, `composer.json` |
| PHP requerido declarado | `^8.3` | `composer.json` |
| PHP requerido por dependencia Symfony | `>=8.4.1` para `symfony/http-kernel v8.1.6` | `composer.lock`; PHP 8.3 no satisface ese paquete bloqueado |
| PHP Docker esperado | `8.4.25` | `docker/php/Dockerfile`, evidencia histórica `02-entorno.log` |
| PHP host | `8.5.10` | `php --version` |
| Composer Docker esperado / host | `2.10.3` / `2.10.3` | Dockerfile / `composer --version` |
| Node Docker/CI esperado | `22.23.2` | Dockerfile, `.github/workflows/tests.yml` |
| Node host | `20.20.2` | `node --version`; distinto del runtime probado, satisface el rango Node 20 de Vite Plus |
| npm Docker documentado | `10.9.8`, no fijado independientemente ni medido hoy | `docs/docker.md`; Dockerfile copia npm desde la imagen Node |
| npm host | `10.8.2` | `npm --version` |
| React / React DOM | `19.3.0` / `19.3.0`; requisito `^19.2.0` | `package-lock.json`, `package.json` |
| TypeScript | `5.9.3`; requisito `^5.7.2` | Locks/manifiesto npm |
| Inertia Laravel | `v3.3.4`; requisito `^3.0` | Locks/manifiesto Composer |
| Inertia React / Vite | `3.7.1` / `3.7.1` | `package-lock.json` |
| Tailwind CSS | `4.3.3` | `package-lock.json` |
| PostgreSQL | Imagen `17.11-alpine`; servidor actual no medido | `docker-compose.yml` |
| Redis | Imagen `7.4.11-alpine`; servidor actual no medido | `docker-compose.yml` |
| phpredis | `6.3.0` esperado | Dockerfile |
| PHPUnit | `12.5.35`; requisito `^12.5.23` | Locks/manifiesto Composer |
| Cypress | `15.3.0`; Electron 136 documentado históricamente | Compose, scripts npm, `docs/testing/cypress-e2e.md`; no dependencia npm del SaaS |
| PHPStan | `2.2.14` | `composer.lock` |
| Larastan | `v3.12.0`; requisito `^3.9` | Locks/manifiesto Composer |
| Laravel Pint | `v1.32.1`; requisito `^1.27` | Locks/manifiesto Composer |
| ESLint | No encontrado en lock/manifiesto/configuración | Inventario de archivos y paquetes npm |
| Prettier | No encontrado en lock/manifiesto/configuración | Inventario de archivos y paquetes npm |
| Vite | `8.3.0`; requisito `^8.0.0` | Locks/manifiesto npm |
| Vite Plus | `0.3.0` fijado | `package.json`, lock y `vite.config.ts` |
| Oxlint / Oxfmt | `1.79.0` / `0.64.0` | `package-lock.json`; calidad mediante Vite Plus |
| Vitest | `4.1.11` | `package-lock.json`; seis archivos `.test.tsx` |
| Python ML requerido | `>=3.12`; runtime actual no verificado | `ml-service/pyproject.toml` |
| pytest / pytest-cov | `8.3.3` / `5.0.0` declarados | Extras dev de `ml-service/pyproject.toml`; instalación actual no verificada |
| FastAPI / scikit-learn | `0.115.6` / `1.9.1` declarados | `ml-service/pyproject.toml` |
| Docker CLI / Compose host | `29.7.2` / `v5.5.1` | `docker --version`, `docker compose version` |
| SonarScanner host | `8.1.0.6389` | `sonar-scanner --version` |
| SonarQube servidor | No determinable | Sin servidor/configuración/evidencia local del proyecto |
| Arquitectura host | `arm64`; scanner informa `aarch64`, macOS `26.6.2` | `uname -m`, salida scanner |

Vite Plus exige Node `^20.19.0 || ^22.18.0 || >=24.11.0`; Vite `^20.19.0 || >=22.12.0`. No existe versión mínima propia en un campo `engines` del `package.json` leído ni archivo de versión Node localizado.

## 4. Docker y servicios

`docker compose --profile e2e config --format json` se resolvió correctamente. Se imprimieron únicamente campos operativos y nombres de variables; se omitieron valores de secretos. `docker compose ps -a` y `docker ps -a` terminaron con salida 1:

```text
failed to connect to the docker API at unix:///Users/luisvilameza/.docker/run/docker.sock
connect: no such file or directory
```

Docker Desktop está instalado; su daemon **no está disponible en el contexto configurado**. No se abrió ni forzó su inicio. Esto impide saber si existen contenedores detenidos de SonarQube fuera del Compose.

| Servicio | Imagen | Puerto | Estado | Propósito |
|---|---|---|---|---|
| `app` | `reclutamiento-php:dev`, build `docker/php/Dockerfile` | Host `8000` → `8000`, todas las interfaces por defecto | ⚠️ Configurado; runtime no consultable | Laravel y assets React compilados |
| `queue` | `reclutamiento-php:dev` | Sin puerto publicado | ⚠️ Configurado; runtime no consultable | Worker Redis de notificaciones |
| `postgres` | `postgres:17.11-alpine` | `127.0.0.1:5432` → `5432` | ⚠️ Configurado; runtime no consultable | Persistencia y bases aisladas de pruebas |
| `redis` | `redis:7.4.11-alpine` | `127.0.0.1:6379` → `6379` | ⚠️ Configurado; runtime no consultable | Sesiones, caché y colas |
| `app-e2e` | `reclutamiento-php:dev` | `127.0.0.1:8001` → `8000` | ⚠️ Perfil `e2e`; falta `.env.e2e` | Laravel aislado para Cypress |
| `queue-e2e` | `reclutamiento-php:dev` | Sin puerto publicado | ⚠️ Perfil `e2e`; runtime no consultable | Cola aislada E2E |
| `cypress` | `cypress/included:15.3.0` | Sin puerto publicado | ⚠️ Perfil `e2e`; no ejecutado | Electron headless, `http://app-e2e:8000` |

No existe servicio SonarQube ni SonarScanner en Compose, ni otro Compose localizado en el proyecto. El ML experimental corre fuera de Compose y está desactivado en `.env` (`ML_SERVICE_ENABLED=false`).

Red implícita: `default`, nombre resuelto `reclutamiento_default`; sin redes adicionales declaradas. Volúmenes: `reclutamiento_pgdata`, `reclutamiento_redisdata`, `reclutamiento_vendor`, `reclutamiento_node_modules`. Código montado en `/var/www/html`; dependencias en volúmenes; SQL de init montado read-only en PostgreSQL. Cypress monta `cypress/` y su configuración, esta última read-only.

Dependencias y healthchecks:

- PostgreSQL y Redis healthy → `app` healthy → `queue`.
- `app` healthy → `app-e2e` healthy → `queue-e2e`; Cypress espera ambos E2E healthy.
- App: `curl -fsS http://localhost:8000/health`, intervalo 10 s, timeout 5 s, 30 intentos, arranque 240 s.
- PostgreSQL: `pg_isready`, intervalo 5 s, timeout 5 s, 20 intentos.
- Redis: `redis-cli ping`, intervalo 5 s, timeout 3 s, 20 intentos.
- Queue: proceso `queue:work` en PID 1 y `php artisan queue:monitor redis:default --max=1000000`; intervalo 30 s, timeout 15 s, 5 intentos, arranque 30 s. Worker: 3 intentos, sleep 1 s, `--max-time=3600`, restart `unless-stopped`.

Variables operativas verificadas en `.env`: `APP_ENV=local`, `APP_URL=http://localhost:8000`, `APP_PORT=8000`, zona `America/Lima`, `DB_CONNECTION=pgsql`, `DB_HOST=postgres`, `DB_PORT=5432`, `DB_DATABASE=reclutamiento`, `REDIS_HOST=redis`, `REDIS_PORT=6379`, sesión/caché/cola Redis, `SEED_ON_BOOT=false`. `APP_KEY=********` y `DB_PASSWORD=********` están no vacíos; su validez no se comprobó. Contraseñas Redis/correo y token ML vacíos/null. No se encontraron variables Sonar en los archivos de entorno inspeccionados ni en el entorno del proceso.

**Efectos reales del arranque:** `docker/php/entrypoint.sh` crea `.env` si falta, instala Composer/npm si faltan dependencias, genera APP_KEY si falta, compila si falta el manifest, crea directorios y ejecuta **`php artisan migrate --force` en cada arranque**. `up` no es read-only. No se ejecutó en esta auditoría y no se debe presentar como comando sin escrituras. Los scripts SQL de init crean `reclutamiento_testing` y `reclutamiento_e2e` solo al inicializar un volumen PostgreSQL nuevo.

Prueba HTTP actual: `curl --fail --max-time 5 http://localhost:8000/health` terminó con **salida 7, conexión rechazada**. `lsof` no mostró listeners en 8000, 8001, 5432 o 6379 y terminó con salida 1. No se observó un conflicto de puertos en esa consulta; debe repetirse antes del ensayo. `/health` está implementado en `HealthController`: consulta SQL `select 1` y ping Redis; retorna 200 si ambos pasan y 503 si falla alguno. No certifica que el worker procese trabajos. `/up` es la ruta de salud Laravel adicional configurada.

## 5. Pruebas configuradas

| Suite | Configuración / archivos | Descubrimiento estático | Evidencia histórica |
|---|---|---|---|
| PHPUnit Unit | `phpunit.xml`, `tests/Unit/` | 6 archivos `*Test.php` | Parte de 419 casos totales F29F |
| PHPUnit Feature | `phpunit.xml`, `tests/Feature/` | 42 archivos `*Test.php` | Parte de 411 aprobadas + 8 omitidas |
| Integración backend | Dentro de Feature: tenancy, auditoría, colas, ML HTTP y flujos | No existe testsuite separada `Integration` en XML | Evidencia PHPUnit F29F |
| Cypress E2E | `cypress.config.cjs`, `cypress/e2e/**/*.cy.js` | 20 specs | 85 aprobadas, 0 fallidas, 05:31 en F29F |
| Cypress visual exploratorio | `cypress/visual/` | 11 specs fuera del patrón E2E por defecto | Ejecuciones por fase en docs v1.1; no se ejecutan con la suite ordinaria |
| Vitest componentes | `resources/js/**/*.test.tsx`, Vite Plus | 6 archivos | 42 aprobadas |
| Cypress component testing | Sin bloque `component` configurado | No localizado | No determinable como suite disponible |
| pytest ML | `ml-service/tests/`, `pyproject.toml` | 18 archivos `test_*.py` | 533 aprobadas |

Los conteos de archivos son inventario estático, no conteos de pruebas descubiertas por el runner. PHPUnit usa PostgreSQL real `reclutamiento_testing`, forzado en XML; caché/sesión `array`, cola `sync`, correo `array`, E2E desactivado. Pruebas Feature usan `RefreshDatabase`; no son inspección de solo lectura y necesitan una base descartable. Las 8 omitidas históricas dependen de verificación de correo Fortify desactivada, no son fallos.

Comando backend respaldado por README y registros: `docker compose exec app php artisan test`. Selección por clase documentada, por ejemplo `docker compose exec app php artisan test --filter=JobRequestWorkflowTest` y `--filter=CrossTenantAccessTest`. Para Unit/Feature se derivan los comandos de §9 de los nombres exactos del XML; no existe script separado para cada suite ni se verificó `--help` con un runner disponible hoy.

`composer test` **no equivale a ejecutar solo PHPUnit**: hace `config:clear`, Pint check, PHPStan y luego Artisan test. Con los fallos de estilo históricos podría detenerse antes de PHPUnit. No se ejecutó.

Frontend: `docker compose exec app npx vp test --run`; no existe `npm test` en scripts. Cypress headless: `npm run cy:run`; UI: `npm run cy:open`. La UI usa `npx --yes cypress@15.3.0 open --e2e --config-file cypress.config.cjs` y puede descargar Cypress; no se ejecutó ni se instaló nada.

**Restricción de esta auditoría:** `cy:run`/`cy:open` llaman primero a `e2e:setup`; al faltar `.env.e2e`, este script genera APP_KEY y E2E_TOKEN. Además, Cypress llama a `/__e2e/reset`, cuyo código ejecuta `migrate:fresh --seed` en `reclutamiento_e2e`, limpia caché y cola. Esto está verificado en `cypress/support/commands.js` y `app/Services/Testing/E2eEnvironment.php`. Los comandos existen, pero **no son compatibles con las prohibiciones actuales de generar tokens y reiniciar bases**. Se inventarían resultados si se calificara esa suite como verificada hoy.

Descubrimiento seguro ejecutado: `npm run` enumeró los scripts sin lanzar pruebas. No se ejecutó Artisan porque falta `vendor/autoload.php` y Docker no está disponible; no se ejecutaron suites completas, cobertura, build ni analizadores.

## 6. SonarQube

| Aspecto solicitado | Hallazgo AS-IS |
|---|---|
| `sonar-project.properties` | No localizado, incluidos archivos ignorados/ocultos del proyecto fuera de dependencias y `.git` |
| Project key / project name | No determinables |
| URL / puerto del servidor | No encontrados; no se presupone un puerto por defecto |
| SonarQube local o Docker | No hay configuración en el proyecto; daemon inaccesible impide inventariar contenedores externos |
| Compose específico / SonarCloud | No localizados |
| Scanner local instalado | `/opt/homebrew/bin/sonar-scanner`, CLI `8.1.0.6389`; `--version` salida 0 |
| Scanner por Docker | No hay comando, imagen ni servicio encontrado |
| Scripts npm / Composer | Ninguno para Sonar |
| Uso anterior de token | No acreditado; no se encontró `SONAR_TOKEN`/`sonar.token` configurado en el proyecto |
| Token existente/vencido/permisos | No verificable; no se generó, recuperó ni validó token |
| Carpetas analizadas | No determinables |
| Exclusiones vendor/node_modules/docs/Cypress | No hay exclusiones Sonar verificables; `.gitignore`/`.dockerignore` no equivalen a `sonar.exclusions` |
| Tests incluidos/excluidos | Sin configuración `sonar.tests` ni evidencia de tratamiento |
| Análisis conjunto Laravel + React | No acreditado |
| Clover/LCOV consumidos y rutas esperadas | No hay propiedades ni rutas Sonar encontradas |
| `.scannerwork` / `report-task.txt` / resultados previos | No localizados en el proyecto |
| Dashboard / Quality Gate / métricas | No verificables sin URL/proyecto/servidor |

Salida pertinente del cliente:

```text
Scanner configuration file: /opt/homebrew/Cellar/sonar-scanner/8.1.0.6389/libexec/conf/sonar-scanner.properties
Project root configuration file: NONE
SonarScanner CLI 8.1.0.6389
Mac OS X 26.6.2 aarch64
```

Se ejecutó **solo `--version`**: no scanner de análisis, conexión autenticada ni publicación. La ruta de configuración global indicada por el programa no se editó ni se utilizó como evidencia de una configuración de este proyecto.

Método de búsqueda reproducible aplicado: inventario `rg --files --hidden --no-ignore` por nombres Sonar/cobertura/Compose; búsquedas textuales de SonarQube, SonarScanner, SonarCloud, propiedades/variables, Clover, LCOV, Xdebug y PCOV; revisión de manifiestos, Docker, XML PHPUnit, README, docs y workflow; `git log --all` por mensajes y `-G` por cambios. Se excluyeron `.git`, dependencias `vendor/`, `node_modules/` y `.venv`, binarios/modelos y documentos binarios. Los archivos de entorno se examinaron por claves y se enmascararon secretos. JUnit se identificó por nombre y evidencias asociadas; no es cobertura. No se consultó historial de shell fuera del repositorio ni GitHub/Sonar en vivo. La ausencia encontrada es **local al alcance auditado**, no prueba de que Sonar nunca se haya ejecutado en otro entorno.

## 7. Cobertura y análisis estático

| Herramienta | Configuración y alcance | Comando real / situación |
|---|---|---|
| Cobertura PHP | PHPUnit declara `<source>` con `app/`; no ruta/formato de salida de cobertura | Sin comando de generación encontrado; no se generó |
| Xdebug/PCOV Docker | Dockerfile instala extensiones PostgreSQL, zip, intl, bcmath, pcntl, opcache y Redis; no Xdebug/PCOV | Falta driver en la imagen definida; runtime actual no inspeccionable |
| Cobertura CI | Workflow fija `coverage: none` | CI no genera cobertura ni la envía a Sonar |
| JUnit PHPUnit | `docs/academico/qa-final/evidencias/phpunit-junit.xml` | Comando archivado: `docker compose exec -T app php artisan test --log-junit storage/logs/f29f-phpunit-junit.xml`; escribe reporte de resultados, **no cobertura** |
| Clover/LCOV/coverage.xml | Ningún artefacto localizado en el checkout auditado | No hay porcentaje/ruta de importación Sonar verificable |
| Cobertura React/Cypress | Sin instrumentación ni plugin/provider en lock | No `@cypress/code-coverage`, `@vitest/coverage-v8`, `@vitest/coverage-istanbul`, `babel-plugin-istanbul`, `istanbul-lib-instrument` ni `nyc` en lock; sin LCOV |
| Cobertura ML | `pytest-cov==5.0.0` declarado; `[tool.coverage.run]` con `source=[recruitment_ml]`, `branch=true` | Configuración Python independiente; sin comando/artefacto de cobertura Sonar encontrado |
| PHPStan/Larastan | `phpstan.neon`, nivel 7; app, bootstrap/app.php, config, database, routes; extensiones Larastan/Carbon | Script Composer `types:check` → `phpstan analyse`; no resultado actual ni registro de ejecución localizado en QA F29F |
| Pint | `pint.json`, preset Laravel | `composer lint:check` → `pint --parallel --test`; medición documentada `vendor/bin/pint --test`, falló históricamente |
| Oxlint/Oxfmt | Bloques `lint` y `fmt` de `vite.config.ts` | `npm run check` → `vp check`; histórico terminó en errores de formato, no acredita una pasada completa de lint |
| ESLint | No configuración/dependencia/script encontrado | No hay `npm run lint` ni comando ESLint verificable |
| TypeScript | `tsconfig.json`: strict, noImplicitAny, noEmit, bundler, alias `@/*`; incluye resources/js TS/TSX | `npm run types:check` → `tsc --noEmit`; también `npx tsc --noEmit` documentado |
| Prettier | No dependencia/configuración/script encontrado | No hay `npm run format`; Oxfmt es la herramienta de formato configurada |

Exclusiones Vite Plus para lint: `vendor/**`, `node_modules/**`, `public/**`, `bootstrap/ssr/**`, `tailwind.config.js`, bindings `resources/js/actions/**`, `routes/**`, `wayfinder/**` y `resources/js/components/ui/*`. Configuración `denyWarnings=true`, `typeAware=true`. Formato: ancho 80, indentación 4, comilla simple, punto y coma, orden Tailwind; excluye `.github/**`, `composer.json`, UI base y vistas de correo. **No son exclusiones de SonarQube.**

Pint, evidencia F29F: 8 problemas en `app/Models/Vacancy.php`, `app/Providers/AppServiceProvider.php`, `app/Services/Assessments/AssessmentResultRecorder.php`, `bootstrap/app.php`, `database/seeders/DemoSeeder.php`, `routes/web.php`, `tests/Feature/Audit/AuditLoggerTest.php` y `tests/Feature/Tenancy/CrossTenantAccessTest.php`. `vp check`: 226 archivos con formato pendiente en el registro histórico. No se corrigieron ni se volvieron a medir; un reporte Markdown nuevo podría afectar el conteo futuro.

No confundir **27/27 RF con pruebas aprobadas** (cobertura funcional/trazabilidad) con cobertura de líneas o ramas. `README.md`, F29G y F32 declaran esta última **NO MEDIDA**. No se asigna un porcentaje inventado.

Workflow `.github/workflows/tests.yml`: un job `ci`, Ubuntu, PostgreSQL 17.11; instala desde locks, prepara entorno CI ficticio, build, TypeScript y PHPUnit. No ejecuta Sonar, Cypress, PHPStan, Pint, Vite Plus check ni cobertura. Hay `workflow_dispatch`; referencias a CI success de F34E en el handoff son documentación archivada, no estado GitHub comprobado en esta sesión.

## 8. Estado para la exposición

Leyenda: ✅ configurado/acreditado en el alcance indicado; ⚠️ configurado, pendiente de ejecución actual; ❌ falta configuración o hay problema comprobado; ❓ evidencia insuficiente. Ningún ✅ de configuración certifica una suite pasada hoy.

| Componente | Estado | Evidencia | Acción pendiente |
|---|---|---|---|
| Git | ✅ | Árbol inicial limpio, HEAD y ref local origin/main iguales | Mantener reporte sin commit; sincronía remota no verificada |
| Docker | ❌ | CLI/Compose disponibles; socket inexistente | Abrir Docker Desktop manualmente y consultar estado |
| Aplicación Laravel | ⚠️ | Código/configuración presentes; `/health` conexión rechazada | Levantar en sesión posterior y revisar destino/efectos del entrypoint |
| React | ⚠️ | Lock y 98 entradas manifest, 0 assets referenciados faltantes | Verificar render real; no basta el manifest |
| PostgreSQL | ⚠️ | Compose y SQL init | Verificar healthy, volúmenes y bases existentes |
| Redis | ⚠️ | Compose y configuración local | Verificar healthy y ping |
| Queue | ⚠️ | Worker/healthcheck definidos | Verificar salud y procesamiento de notificaciones |
| PHPUnit | ⚠️ | XML, F29F 411 aprobadas + 8 omitidas | Ejecutar en BD testing descartable; dependencias actuales sin verificar |
| Tests Unit | ⚠️ | 6 archivos, testsuite Unit | Ejecutar selección Unit |
| Tests Feature | ⚠️ | 42 archivos, testsuite Feature | Ejecutar y mantener cross-tenant/decisión humana |
| Cypress | ⚠️ | 20 specs, histórico 85/85 | Resolver `.env.e2e`, ARM y permisos de reset/generación fuera de esta auditoría |
| Vitest | ⚠️ | 6 archivos, histórico 42/42 | Repetir con dependencias disponibles |
| pytest ML | ⚠️ | 18 archivos, histórico 533 | Comprobar entorno Mac si se incluye en la exposición; ML opcional |
| PHPStan/Larastan | ⚠️ | Lock, nivel 7 y script | Ejecutar; sin resultado comprobado |
| Pint | ❌ | F29F salida 1, 8 problemas | Medir otra vez y explicar deuda; no corregido |
| ESLint | ❌ | No configuración/script/paquete | Explicar herramienta real Oxlint; no prometer ESLint |
| TypeScript | ⚠️ | Script y F29F salida 0 | Repetir `types:check` |
| Prettier | ❌ | No configuración/script/paquete | Explicar herramienta real Oxfmt |
| Vite Plus check | ❌ | F29F salida 1, 226 archivos | Repetir check y registrar salida; no afirmar lint aprobado |
| Cobertura backend | ❌ | Sin driver definido/reporte; CI none | Preparación futura de driver/reportes con alcance autorizado |
| Cobertura frontend | ❌ | Sin instrumentación/provider ni LCOV | Preparación futura si se exige mostrar porcentaje |
| SonarQube | ❓ | No configuración de servidor; Docker inaccesible | Recuperar servidor/Compose/URL anteriores |
| SonarScanner CLI | ✅ | `--version` salida 0, 8.1.0.6389 | Recuperar configuración de análisis del proyecto |
| Integración scanner/proyecto | ❌ | Configuración raíz NONE; sin key/script | Recuperar receta antes de analizar |
| Dashboard SonarQube | ❓ | Sin URL/key/análisis archivado | Identificar y comprobar dashboard real |
| Documentación | ✅ | README, Docker, Cypress, F25/F29F, métricas, handoff | Presentar versiones/fechas correctas y distinguir historia |
| Preparación para exposición | ❌ | Aplicación inaccesible, Sonar no reproducible | Resolver los pendientes de §11 y realizar ensayo completo |

Guía de exposición existente: `docs/final-report/demo-script.md`, 8–12 minutos. Es **histórica v1.0**, cita 244 pruebas/43 E2E e incluye reset destructivo de demo: no usar ese reset bajo las reglas actuales. La guía E2E conserva secciones v1.0 y añade §9 con 20 specs/85 tests v1.1. Para resultados posteriores usar `docs/academico/qa-final/F29F_Ejecucion_QA.md` y sus logs; para operación Mac usar `docs/academico/handoff/F34E_MACOS_HANDOFF.md`. No se encontró guía previa SonarQube.

Pantallas útiles para el profesor: Docker Desktop con contenedores healthy cuando existan; respuesta real de `/health`; terminal PHPUnit/TypeScript/Vitest y Cypress con fecha de ejecución; aplicación en roles ficticios mostrando aislamiento y decisión humana; documentos F29F/F29G con evidencia. Sonar queda pendiente según §10.

## 9. Comandos exactos para reproducir las pruebas

**Inventario para una sesión posterior, no ejecutado durante esta auditoría.** Todos requieren runtime/dependencias disponibles. Las pruebas escriben en sus bases/cachés/artefactos; no ejecutarlas bajo la autorización actual de solo diagnóstico. Los comandos derivados de nombres de suite se identifican expresamente; no se atribuyen a ejecuciones antiguas.

Backend, comandos documentados:

```sh
docker compose exec app php artisan test
docker compose exec app php artisan test --filter=JobRequestWorkflowTest
docker compose exec app php artisan test --filter=CrossTenantAccessTest
```

Selección Unit/Feature, **derivada del XML** y pendiente de verificar contra el `--help` del runner disponible; no hay atajos específicos en manifiestos:

```sh
docker compose exec app php artisan test --testsuite=Unit
docker compose exec app php artisan test --testsuite=Feature
```

Frontend, documentados:

```sh
docker compose exec -T app npm run types:check
docker compose exec app npx tsc --noEmit
docker compose exec app npx vp test --run
# Build escribe assets y bindings; listado como referencia, no ejecutado:
# docker compose exec app npm run build
```

Cypress, comandos existentes **bloqueados bajo las reglas actuales** por generación de token/reset de BD E2E. La UI también puede descargar un binario. No hay variante completa de esta suite que evite esos efectos en los scripts encontrados:

```sh
# npm run cy:run
# npm run cy:run -- --spec "cypress/e2e/e2e-10-*.cy.js"
# npm run cy:open
```

Calidad PHP, scripts reales ejecutables dentro del servicio `app` cuando esté disponible:

```sh
docker compose exec app composer types:check
docker compose exec app composer lint:check
```

Son la invocación Docker de scripts presentes en Composer: `types:check` ejecuta `phpstan analyse`; `lint:check` ejecuta `pint --parallel --test`. La invocación directa de Pint registrada históricamente es:

```sh
docker compose exec -T app vendor/bin/pint --test
```

Calidad frontend, script real y modo sin corrección:

```sh
docker compose exec app npm run check
```

`check` ejecuta `vp check`; no usar `check:fix`, `composer lint`, `vp check --fix`, `composer setup` ni `composer test` como inspecciones inocuas. No existen scripts `analyse`, `lint` npm, `typecheck` npm, `format`, `npm test` ni scripts Sonar/cobertura en los manifiestos; los nombres correctos de tipos son `types:check` tanto en npm como en Composer, con herramientas diferentes.

Cobertura: **sin comando completo encontrado**, sin driver Docker definido y sin rutas Clover/LCOV establecidas. No se propone una ruta/flag arbitraria. El comando JUnit existente escribe resultados y no resuelve cobertura. pytest histórico usa `.venv/Scripts/python.exe` de Windows; no convertirlo en un comando Mac supuestamente probado.

## 10. Secuencia exacta para volver a demostrar SonarQube

**TO-BE, no ejecutada.** La secuencia solo puede reconstruirse parcialmente. Las etapas bloqueadas se dejan sin comando inventado. Antes de una sesión operativa hay que recuperar configuración externa Sonar y aceptar expresamente los efectos de arranque/pruebas; no se instala ni se genera nada durante esta auditoría.

1. **Abrir Docker Desktop manualmente.** Está instalado en `/Applications/Docker.app`; no hay comando de apertura Mac documentado en el repositorio. Después comprobar `docker --version` y `docker compose version`.
2. **Levantar SaaS**, únicamente en un ensayo posterior con dependencias ya preparadas o instalación autorizada y bases locales ficticias. Revisar `.env` sin imprimir secretos, volúmenes y migraciones pendientes: el entrypoint instala si falta y migra en cada inicio. Comando documentado: `docker compose up -d --wait`. No se usa reset demo ni eliminación de volúmenes. Si las restricciones actuales siguen vigentes, detenerse antes de este paso.
3. **Comprobar servicios:** `docker compose ps`. Deben observarse `app`, `queue`, `postgres`, `redis` healthy. No presumir nombres de contenedor distintos de los servicios encontrados.
4. **Comprobar Laravel:** `curl --fail http://localhost:8000/health`; debe retornar 200 con database/redis ok. Comandos de continuidad encontrados: `docker compose exec -T app php artisan --version` y `docker compose exec -T app php artisan migrate:status`.
5. **Ejecutar PHPUnit**, en sesión que permita escrituras en `reclutamiento_testing`: `docker compose exec app php artisan test`. Registrar resultados reales y explicar las omitidas si siguen presentes.
6. **Generar cobertura backend: BLOQUEADO.** No hay driver Xdebug/PCOV en la imagen definida ni receta de generación/importación en el repositorio. Hace falta una preparación futura aprobada; no inventar Clover ni atribuir cobertura a JUnit.
7. **PHPStan/Larastan:** `docker compose exec app composer types:check`, invocación del script real. Registrar salida, incluso si falla.
8. **Pint en check:** `docker compose exec -T app vendor/bin/pint --test`. Existe fallo histórico; no corregir durante el ensayo diagnóstico.
9. **ESLint: NO CONFIGURADO.** La herramienta real de calidad frontend es `docker compose exec app npm run check` (Vite Plus/Oxlint/Oxfmt). Puede detenerse por formato, como en F29F; mostrar la salida real.
10. **TypeScript:** `docker compose exec -T app npm run types:check`. Opcional de componentes documentado: `docker compose exec app npx vp test --run`.
11. **Cypress: BLOQUEADO bajo las restricciones actuales.** El comando real es `npm run cy:run`, pero hoy faltaría generar token y la suite reinicia la BD E2E mediante `migrate:fresh`. Para otra sesión se debe permitir explícitamente esa operación sobre datos sintéticos descartables y comprobar ARM. UI alternativa existente `npm run cy:open`, con posible descarga, no ejecutada.
12. **Levantar SonarQube: BLOQUEADO.** No se encontró Compose, imagen, servicio ni comando anterior. Recuperar primero la receta del entorno original; no crear un servidor arbitrario.
13. **Comprobar Sonar en navegador: BLOQUEADO.** URL/puerto no determinados; no asumir una dirección. Confirmar versión y estado del servidor real cuando se recupere.
14. **Ejecutar sonar-scanner de análisis: BLOQUEADO.** El cliente existe pero falta project key, servidor, autenticación y alcance. Único comando diagnóstico probado: `sonar-scanner --version`. No constituye análisis ni debe usarse para anunciar éxito.
15. **Verificar finalización: pendiente.** Después de recuperar la receta, comprobar salida del scanner y procesamiento del análisis en el servidor/dashboard del proyecto correcto. No hay identificador de tarea ni archivo de resultados previo localizado para reutilizar.
16. **Abrir dashboard: BLOQUEADO.** No hay URL/key verificable. Confirmar fecha y commit del análisis antes de enseñar métricas; no reutilizar un dashboard de otro proyecto.
17. **Preparar métricas/pantallas:** cuando exista análisis real, mostrar resumen del proyecto y estado de Quality Gate; incidencias de fiabilidad (Bugs/Reliability), seguridad (Vulnerabilities/Security), Security Hotspots y su revisión, mantenibilidad (Code Smells/Maintainability), duplicaciones y líneas de código. Mostrar Coverage solo si hay importación válida, indicando qué lenguajes/directorios cubre; separar código nuevo/global si el dashboard lo distingue. **Los nombres y la disponibilidad dependen de la versión/modo del servidor aún desconocido: ninguna cifra o pantalla Sonar se verificó hoy.** Conviene preparar resumen, condiciones del gate, incidencias, hotspots y medidas, únicamente si están presentes en ese servidor.

Bloque cronológico A–M para la exposición. Líneas comentadas requieren trabajo posterior; las secciones sin receta permanecen explícitamente pendientes. Los comandos de arranque/pruebas **no tienen autorización de ejecución en esta auditoría**.

```sh
# A. Arranque del proyecto — sesión posterior; revisar efectos del entrypoint
# Abrir Docker Desktop manualmente antes de continuar.
# docker compose up -d --wait

# B. Verificación de Docker
docker --version
docker compose version
docker compose ps

# C. Verificación de Laravel
curl --fail http://localhost:8000/health
docker compose exec -T app php artisan --version
docker compose exec -T app php artisan migrate:status

# D. PHPUnit — solo con autorización de escrituras en BD testing descartable
# docker compose exec app php artisan test

# E. Cobertura — BLOQUEADO: sin driver/receta/rutas verificables.

# F. PHPStan — script Composer real, requiere app/dependencias
docker compose exec app composer types:check

# G. Pint — modo check, sin arreglos automáticos
docker compose exec -T app vendor/bin/pint --test

# H. ESLint — no configurado; herramienta real Vite Plus/Oxlint/Oxfmt
docker compose exec app npm run check

# I. TypeScript
docker compose exec -T app npm run types:check
# Componentes (comando documentado):
# docker compose exec app npx vp test --run

# J. Cypress — BLOQUEADO hoy: genera token si falta entorno y reinicia BD E2E
# npm run cy:run
# Alternativa UI existente, puede descargar binario:
# npm run cy:open

# K. SonarQube — BLOQUEADO: sin comando de arranque encontrado.

# L. sonar-scanner — solo disponibilidad; NO ejecuta análisis
sonar-scanner --version
# Análisis: BLOQUEADO hasta recuperar key/URL/auth/configuración.

# M. Apertura dashboard — BLOQUEADO: URL/key no determinados.
```

Esta limitación evita presentar como reproducible una demostración que exigiría configuración nueva y comandos no encontrados. No se generaron tokens ni se recomendó publicarlos en la terminal.

## 11. Posibles problemas antes de la presentación

Diez grupos priorizados; son pendientes operativos/configuracionales, no diez defectos funcionales del SaaS:

1. **Docker no disponible y aplicación inaccesible.** Socket inexistente; `/health` salida 7. Bloquea verificación runtime, suites y cualquier Sonar en Docker. No se inició Docker.
2. **Receta SonarQube ausente.** Sin servidor/URL/key/Compose/script ni resultados previos locales; solo cliente instalado. No se puede reproducir scanner/dashboard/Quality Gate. Token vencido o gate fallando son posibilidades aún no comprobables, no fallos afirmados.
3. **Cobertura backend no preparada.** Sin Xdebug/PCOV en Dockerfile, sin Clover, CI `coverage: none`. No mostrar un porcentaje ni importar JUnit como cobertura.
4. **Cobertura frontend no preparada.** Sin instrumentación Cypress/provider Vitest ni LCOV; las pruebas E2E/componentes no proporcionan automáticamente cobertura Sonar.
5. **Dependencias y datos de Docker sin verificar.** Faltan autoload y ejecutable VP en el host; volúmenes inaccesibles. El manifest tiene 98 entradas sin assets referenciados faltantes, pero no acredita build reproducido. `up` puede instalar y migrar, acciones prohibidas durante esta auditoría. Semilla automática desactivada: no se acreditó que existan usuarios demo en la BD actual. No se midieron permisos de volúmenes/archivos ni vigencia de dependencias contra fuentes externas.
6. **Cypress requiere acciones actualmente prohibidas.** `.env.e2e` ausente; setup genera token/clave; reset ejecuta `migrate:fresh` sobre E2E. No iniciar la suite sin delimitar una sesión posterior y la BD sintética descartable. No lanzar `init-e2e-env.sh` directamente en macOS: usa GNU `sed -i` dentro de Linux.
7. **Deuda de estilo acreditada y herramientas diferentes a las esperadas.** Pint 8 problemas; Vite Plus check 226 archivos en F29F, salida 1. ESLint/Prettier no están configurados; presentar Oxlint/Oxfmt. `composer test` puede detenerse antes de PHPUnit por check de estilo. No confundir este fallo con un bug funcional.
8. **Análisis estático PHP y regresiones actuales pendientes.** PHPStan nivel 7 configurado, sin pasada registrada localizada. PHPUnit/TypeScript/Cypress/Vitest/pytest no se ejecutaron hoy; CI actual no consultada. Los resultados de Windows/Linux no certifican esta Mac.
9. **Portabilidad ARM, acceso a Internet y diferencias de runtime.** Mac arm64; manifiesto ARM de Cypress/Electron no verificado. Host Node 20.20.2 y PHP 8.5.10 difieren del Docker validado Node 22.23.2/PHP 8.4.25. Primer arranque puede necesitar descargar imágenes/dependencias/fuentes Bunny; UI Cypress puede descargar binario. Build histórico avisa falta del paquete opcional `fontaine`; no se instaló. La documentación registra ruido `dbus` de Electron. No se demostró incompatibilidad ni fallo de red actual.
10. **Ensayo/documentación/contexto de demo pendientes.** Guion v1.0 conserva conteos antiguos y resets que no deben ejecutarse. No se comprobó disponibilidad de datos demo, dashboard o navegación. `lsof` no encontró conflictos en 8000/8001/5432/6379 ahora, pero repetir antes de iniciar; no se afirma que PostgreSQL/Redis nativos estén interfiriendo. Puerto Sonar desconocido. Git estaba limpio inicialmente; al terminar queda únicamente este reporte nuevo sin commit por instrucción expresa.

No se ejecutaron auditorías de vulnerabilidades/actualizaciones contra registries ni pruebas de carga. Por tanto no se afirma que dependencias estén desactualizadas, que haya vulnerabilidades detectadas por Sonar o que un Quality Gate esté aprobado/rechazado.

## 12. Checklist final de exposición

- [ ] Docker Desktop abierto y daemon accesible.
- [ ] Destino `.env` local/ficticio y efectos del entrypoint revisados antes de arrancar.
- [ ] SaaS levantado en una sesión posterior autorizada.
- [ ] Aplicación accesible en `http://localhost:8000`.
- [ ] `/health` devuelve 200 y database/redis ok.
- [ ] PostgreSQL healthy; bases demo/testing/E2E necesarias verificadas.
- [ ] Redis healthy.
- [ ] Queue healthy y notificaciones comprobadas.
- [ ] Usuarios/fixtures exclusivamente ficticios listos sin reset de la BD demo.
- [ ] PHPUnit ejecutado, conteos y omitidas registrados con fecha/commit.
- [ ] Unit y Feature verificadas, incluido aislamiento cross-tenant y decisión humana.
- [ ] Cobertura backend generada **solo si se prepara antes la configuración faltante**; mientras tanto declarar NO MEDIDA.
- [ ] Cobertura frontend/LCOV **solo si se prepara instrumentación**; mientras tanto declarar NO MEDIDA.
- [ ] PHPStan/Larastan ejecutado y salida registrada.
- [ ] Pint verificado en modo check y deuda explicada si sigue fallando.
- [ ] Oxlint/Oxfmt mediante Vite Plus check ejecutado; aclarar que ESLint/Prettier no están configurados.
- [ ] TypeScript verificado.
- [ ] Vitest ejecutado.
- [ ] Cypress/ARM y entorno E2E preparados en sesión que permita token y reset de la BD descartable.
- [ ] Cypress ejecutado y resultados listos; UI opcional preparada con antelación.
- [ ] SonarQube original/receta identificados, URL y puerto comprobados.
- [ ] Project key, nombre, fuentes, tests, exclusiones y autenticación Sonar recuperados sin exponer secretos.
- [ ] SonarQube activo.
- [ ] SonarScanner ejecutado para análisis real; `--version` no basta.
- [ ] Procesamiento completado y análisis del commit correcto visible en dashboard.
- [ ] Quality Gate revisado y condiciones explicables.
- [ ] Métricas reales preparadas; cobertura diferenciada de trazabilidad funcional.
- [ ] README, guías Docker/Cypress, F29F/F29G y handoff disponibles.
- [ ] Navegador listo para demo con roles ficticios y pantallas de evidencia.
- [ ] Acceso a imágenes/dependencias/fuentes preparado antes del día de exposición, con autorización de instalación si hace falta.
- [ ] Alcance Git revisado: únicamente reporte nuevo, sin publicación ni correcciones.

## 13. NO MODIFICADO

Durante esta auditoría no se modificó código fuente, configuración existente, dependencias, base de datos, Docker volumes ni historial Git. La única modificación realizada fue la creación de este archivo de reporte.

No se cambió de rama, no se hizo commit/push/merge/tag/fetch, no se inició Docker, no se instalaron herramientas/dependencias, no se ejecutaron suites, cobertura, scanner de análisis, migraciones/reset ni generación de tokens/secretos. Se conservaron archivos ignorados, datos y cachés preexistentes. Los secretos de entorno se resumieron como presencia/ausencia y `********`.

Se aplicaron `project-guardian`, su checklist, `academic-traceability` y las pautas de `laravel-saas-quality` pertinentes a configuración/pruebas. Se distinguió evidencia histórica de verificación actual y no se reescribieron documentos de v1.0/v1.1. No corresponde ejecutar la regresión funcional para este único archivo documental: habría escrito artefactos/datos y requerido Docker/dependencias fuera de la autorización actual. La validación de entrega se limita a estructura, enlaces locales, alcance Git, formato whitespace y ausencia de valores secretos en el reporte.

Fuentes principales consultadas: [CLAUDE.md](../CLAUDE.md), [README.md](../README.md), [PROGRESS.md](PROGRESS.md), [Docker](docker.md), [Cypress](testing/cypress-e2e.md), [QA F29F](academico/qa-final/F29F_Ejecucion_QA.md), [resumen de comandos históricos](academico/qa-final/evidencias/00-resumen.tsv), [métricas F29G](academico/metricas-calidad/F29G_Defectos_y_Metricas.md), [handoff F34E macOS](academico/handoff/F34E_MACOS_HANDOFF.md), [guion histórico](final-report/demo-script.md), [Compose](../docker-compose.yml), [Dockerfile](../docker/php/Dockerfile), [Composer](../composer.json), [npm](../package.json), [PHPUnit](../phpunit.xml), [PHPStan](../phpstan.neon), [Vite](../vite.config.ts) y [CI](../.github/workflows/tests.yml).
