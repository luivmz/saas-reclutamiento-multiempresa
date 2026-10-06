# Continuidad macOS después de F34E

Preparado sobre main publicado `853d423de03879f755371a2535ba8896009ae2a5`, posterior a F34E. Rama de este handoff: `chore/macos-handoff-f34e`, creada desde main por autorización expresa. Es una receta de traslado, no la ejecución de F35-SBX ni una certificación de funcionamiento en una Mac.

## Estado vigente F34E

F34E CERRADA. La siguiente fase de trabajo prevista es F35-SBX, pero no se inicia durante este handoff.

- G0 real = NO APROBADA
- G0-09 = CUMPLIDO
- G0-14 = CUMPLIDO
- G0-02 = PENDIENTE EXTERNO
- G0-03 = PENDIENTE EXTERNO
- G0-12 = PENDIENTE EXTERNO
- ADR-005 = PROPUESTA
- G0-SBX = APROBADA CON RESTRICCIONES
- F35 productiva = BLOQUEADA
- F35-SBX = HABILITADA
- F36–F40 = BLOQUEADAS
- Alcance C = BLOQUEADO
- Datos reales = PROHIBIDOS

SBX-01..SBX-18 CUMPLE. Aprobación interna del equipo REGISTRADA, sin aprobación jurídica, de privacidad ni validación institucional. F35-SBX exclusivamente sintético. F35-SBX AÚN NO INICIADA. RF-23 sigue humana; RF-29 sigue experimental/informativa. Sin scoring, recomendación ni selección automática; sin CV, documentos, audio ni vídeo reales. Sin integración productiva ni migración automática de resultados SBX a producción. RF-21 vigente conserva su cálculo determinista a partir de puntajes humanos; el baseline RF/CU/RNF no cambia.

## Referencias y fotografías de cierre

- F34E A: `0ea5e63bb84db717bcc5f2a94c3c93572d5b863e`.
- F34E B: `c016a75401eb127aa11cd9185423e2866b0fc936`.
- F34E C: `b7ca88da7ba38a4ab98ccd7f7dcbe9d82a7e1c00`.
- Merge develop F34E: `ac6aed2a35282ddd9b502a647e37ee00a0a4cd98`; [CI tests success, run 37410817124](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/37410817124).
- Merge main F34E: `853d423de03879f755371a2535ba8896009ae2a5`; [CI tests success, run 37411235227](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/37411235227).
- El hash de main citado arriba es la base de este documento, no un hash futuro del merge de handoff. Consultar `git rev-parse origin/main` después de clonar para conocer la revisión más reciente.
- Stash histórico `1b861837355e1fdbdea8b758bcd25c0604143f63` eliminado por autorización después de verificar los nueve artefactos F34E publicados y comparar su contenido. Contenía versiones preliminares ya sustituidas, F34D integrado y un caché Python; no trabajo fuente único pendiente. No se aplicó el stash sobre main.

Fuentes operativas: [Compose](../../../docker-compose.yml), [Dockerfile PHP](../../../docker/php/Dockerfile), [entrypoint](../../../docker/php/entrypoint.sh), [composer.json](../../../composer.json), [composer.lock](../../../composer.lock), [package.json](../../../package.json), [package-lock.json](../../../package-lock.json), [entorno de ejemplo](../../../.env.example), [PHPUnit](../../../phpunit.xml), [Docker](../../docker.md) y [Cypress](../../testing/cypress-e2e.md).

El [handoff académico anterior](../MAC_HANDOFF.md) y los registros antiguos conservan su valor histórico. Para este traslado se usa esta receta: no ejecutar por rutina comandos de reset demo, regeneración ML ni regeneración documental de esos antecedentes.

## Herramientas y versiones constatadas en el repositorio

| Herramienta | Versión / requisito | Fuente y uso |
|---|---|---|
| Git | Disponible en host; sin versión mínima fijada aquí | Clonar y verificar refs; conservar ramas históricas |
| Docker Desktop + Compose | Compose al menos 2.24, según `docs/docker.md` | Opción recomendada; el compose usa `env_file.required` |
| PHP | 8.4.25 en Docker; `composer.json` permite `^8.3` | Runtime validado del proyecto: PHP 8.4 |
| Composer | 2.10.3 en Docker | Instalación desde `composer.lock`, no `composer update` |
| Node | 22.23.2 en Docker/CI | Compatible con los motores de Vite y vite-plus del lock |
| npm | Incluido en la imagen Node; verificar `npm --version` | `docs/docker.md` registra 10.9.8; no se fija independientemente en `package.json` |
| PostgreSQL | `postgres:17.11-alpine` | Persistencia principal; init crea la BD separada de PHPUnit |
| Redis | `redis:7.4.11-alpine`, phpredis 6.3.0 | Sesiones, caché y cola |
| Frontend | React 19, TypeScript, Inertia, Tailwind/shadcn, Vite 8 | Versiones resueltas en `package-lock.json`; monolito modular |
| Cypress | `cypress/included:15.3.0`, Electron | Perfil E2E aislado; navegador web en host para la UI normal |
| Python | 3.12 o superior recomendado | Validadores académicos; no iniciar el servicio ML |

En la ruta Docker no se requieren PHP, Composer, PostgreSQL, Redis ni Node instalados en macOS. Node/npm en host son opcionales para atajos `npm run cy:run` o la apertura gráfica de Cypress. Si se usa Node nativo, 22.23.2 es la referencia probada: el lock exige Node compatible con Vite (`^20.19.0 || >=22.12.0`) y vite-plus (`^20.19.0 || ^22.18.0 || >=24.11.0`); no usar versiones antiguas solo porque existan en Windows.

Apple Silicon: verificar antes de arrancar que Docker puede obtener las imágenes exactas para la arquitectura de la Mac, especialmente Cypress/Electron. No se ha ejecutado este traslado en macOS ni se ha validado aquí el manifiesto ARM de Cypress. Si hay incompatibilidad, detener esa comprobación y registrar el error; no sustituir imágenes ni agregar `platform` silenciosamente. La CI Linux no acredita por sí sola compatibilidad Intel/ARM de macOS.

## Traslado recomendado: clone nuevo

En Terminal de macOS, desde una carpeta de trabajo elegida por el usuario:

```sh
git clone https://github.com/luivmz/saas-reclutamiento-multiempresa.git
cd saas-reclutamiento-multiempresa
git switch main
git fetch origin --tags
git status --short --branch
git rev-parse HEAD origin/main
```

No copiar desde Windows `vendor/`, `node_modules/`, `.venv/`, `__pycache__/`, caches, archivos `.env` privados ni binarios generados. Usar los locks versionados y reinstalar dependencias en el nuevo entorno. Los entregables académicos versionados PDF/DOCX/PNG/SVG sí llegan mediante Git; no son dependencias nativas reutilizadas.

No copiar credenciales Windows, tokens GitHub, configuración global ni CV privados. Cualquier autenticación Git en la Mac se configura por su mecanismo habitual seguro, sin tokens escritos en comandos o documentación.

## Configuración privada antes del primer arranque

Crear `.env` únicamente en el clone nuevo si no existe:

```sh
test -e .env || cp .env.example .env
```

Editar ese archivo local antes de arrancar. No imprimirlo ni versionarlo. Configuración esperada de la ruta Compose:

| Variables | Configuración y precaución |
|---|---|
| `APP_URL`, `APP_PORT` | `http://localhost:8000`, `8000` por defecto; ajustar ambos si el puerto está ocupado |
| `APP_TIMEZONE` | `America/Lima` |
| `APP_KEY` | Se genera localmente en el entrypoint si falta; no reutilizar una clave privada Windows |
| `DB_CONNECTION`, `DB_HOST`, `DB_PORT` | `pgsql`, `postgres`, `5432` dentro de Compose |
| `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` | BD local ficticia `reclutamiento`; elegir credencial local privada, no conservar la contraseña de ejemplo |
| `FORWARD_DB_PORT` | `5432` por defecto, publicado en loopback; no cambia el puerto interno |
| `REDIS_CLIENT`, `REDIS_HOST`, `REDIS_PORT` | `phpredis`, `redis`, `6379` dentro de Compose |
| `REDIS_PASSWORD`, `FORWARD_REDIS_PORT` | Respetar el servidor configurado; la imagen actual no activa contraseña. Puerto host en loopback |
| `QUEUE_CONNECTION`, `SESSION_DRIVER`, `CACHE_STORE` | `redis`; caché DB 1 y sesión/cola DB 0 según ejemplos |
| `MAIL_MAILER` | `log`; no se necesitan credenciales SMTP para la verificación ficticia |
| `FILESYSTEM_DISK` | `local`; CV privados, sin necesidad de `storage:link` |
| `SEED_ON_BOOT` | `false`; no cargar ni resetear datos automáticamente por esta receta |
| `E2E_ENABLED`, `E2E_TOKEN` | Desactivado/token vacío en `.env` normal; el entorno E2E usa archivo y token separados |
| `ML_SERVICE_ENABLED` | `false`; no habilitar ni configurar ML por este handoff |

Mantener una base **nueva, local y descartable**, sin datos reales ni conexión a bases remotas/productivas. El entrypoint ejecuta `php artisan migrate --force` en cada arranque: es una migración con escritura de esquema, no una comprobación read-only. Revisar destino antes de usar `up`. Esta receta no usa `migrate:fresh`, `demo:reset` ni `down -v`.

El puerto de `app` se publica por defecto en todas las interfaces, mientras PostgreSQL, Redis y E2E usan loopback. No exponer el desarrollo con `APP_DEBUG=true` a una red no confiable; usar controles de red locales y mantener datos exclusivamente ficticios. Este handoff no cambia la configuración de despliegue.

## Restauración y arranque soportados

Comprobar herramientas y construir desde fuentes locales:

```sh
git --version
docker --version
docker compose version
python3 --version
docker compose build app
docker compose run --rm --no-deps --entrypoint sh app -lc 'php -v; composer --version; node --version; npm --version'
docker compose up -d --wait
docker compose ps
curl --fail http://localhost:8000/health
```

El entrypoint instala `composer install` si falta `vendor/autoload.php`, ejecuta `npm ci` si faltan herramientas frontend, genera la clave local, compila assets si falta el manifiesto y aplica migraciones. PHP y Node usan volúmenes nuevos de esta Mac, no carpetas copiadas. La conexión PostgreSQL/Redis se verifica también por `/health`.

Comandos explícitos equivalentes de instalación/recompilación, solo si se necesitan dentro de la instalación local:

```sh
docker compose exec -T app composer install --no-interaction --prefer-dist
docker compose exec -T app npm ci
docker compose exec -T app npm run build
```

No usar `composer update` ni `npm install` para cambiar locks durante el traslado. El build descarga fuentes tipográficas según `vite.config.ts`; un error de red es un fallo verificable, no motivo para cambiar dependencias.

Backend: `docker compose up -d --wait` inicia `app`, `queue`, PostgreSQL y Redis. Frontend: `docker compose exec -T app npm run build`, servido por Laravel en el mismo puerto. HMR no está configurado en Compose (5173 no se expone): `npm run dev` dentro de `app` no constituye una receta accesible desde el navegador host. No se agregan puertos/configuración funcional aquí.

Abrir `http://localhost:8000` en el navegador. Para cerrar sin borrar volúmenes: `docker compose stop`. Las cuentas ficticias requieren carga de fixtures/demo en una fase controlada; no es un prerrequisito para `/health` y no se resetea la BD durante este handoff.

## Checklist ejecutable después del traslado

```sh
docker compose exec -T app composer validate --no-check-publish
docker compose exec -T app php artisan --version
docker compose exec -T app php artisan migrate:status
docker compose exec -T postgres sh -lc 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
docker compose exec -T redis redis-cli ping
docker compose exec -T app npm run types:check
docker compose exec -T app npm run build
docker compose exec -T app php artisan test
```

PHPUnit usa `reclutamiento_testing`, forzada en `phpunit.xml`, creada por [init SQL](../../../docker/postgres/init/01-create-testing-db.sql) en el primer arranque de un volumen PostgreSQL nuevo. No apuntar esa suite a una BD con datos valiosos. Registrar resultados reales en la Mac: el CI publicado pasó PHPUnit/TypeScript/build, pero no se atribuye a esta Mac una ejecución todavía inexistente.

Cypress completo, sin Node en el host:

```sh
docker compose run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh
docker compose --profile e2e run --rm cypress
docker compose --profile e2e stop app-e2e queue-e2e
```

`init-e2e-env.sh` se ejecuta **dentro del contenedor Linux**: utiliza `sed -i` GNU y no debe lanzarse directamente en macOS. Crea `.env.e2e` con clave/token nuevos sin mostrarlos. Revisar localmente las credenciales DB si se cambiaron en `.env`. La suite E2E crea/reinicia fixtures en `reclutamiento_e2e`, con protecciones de entorno/base/token; por ello esa BD debe ser exclusivamente descartable y sintética.

La apertura gráfica requiere Node/npm en host y usa la receta ya existente `npm run cy:open`, que obtiene Cypress 15.3.0; no es necesaria para el recorrido Docker anterior. Consultar [configuración Cypress](../../../cypress.config.cjs) y [pruebas E2E](../../testing/cypress-e2e.md).

Validadores académicos, desde la raíz con Python 3.12 o superior:

```sh
python3 -B docs/academico/tools/f33/validate_f33.py
python3 -B docs/academico/tools/f34/validate_f34.py
python3 -B docs/academico/tools/f34a/validate_f34a.py
python3 -B docs/academico/tools/f34b/validate_f34b.py
python3 -B docs/academico/tools/f34e/validate_f34e.py
python3 -B docs/academico/tools/f27b/validate.py
python3 -B docs/academico/tools/f27b/validate.py --cierre-f29
python3 -B docs/academico/tools/f30/validate_f30.py
python3 -B docs/academico/powerdesigner/scripts/validate_f29.py
python3 -B docs/academico/tools/f27b/test_f32_safety.py
git diff --check
git status --short --branch
```

Los validadores F33/F34/F34A/F34B/F34E usan biblioteca estándar Python; F34 verifica reproducibilidad en temporales. `test_f32_safety.py` importa el builder y requiere Pillow disponible para su módulo de diagramas: comprobar `python3 -c 'import PIL'`. Si no existe, registrar ese prerrequisito y preparar un entorno virtual con la revisión/autorización de dependencias aplicable; no ejecutar un instalador automático ni agregar paquetes al proyecto por este handoff. No regenerar PDF/DOCX ni el modelo ML para verificar continuidad.

Mantener el clone limpio para validar alcance. Los validadores post-F34E admiten únicamente los artefactos de cierre/handoff autorizados; no dan permiso genérico a nuevas fases, runtime o evidencias congeladas.

## Auditoría de portabilidad y limitaciones conservadas

| Hallazgo | Clasificación | Tratamiento |
|---|---|---|
| XAMPP / rutas de unidades Windows en planes y reportes antiguos | Documentación histórica, no runtime actual | No ejecutar esas recetas ni reescribir evidencia histórica; usar Compose |
| PowerDesigner `.ps1`, automatización COM y metadatos locales en modelos históricos | Herramientas de edición Windows, no runtime Laravel | Conservar modelos/exportaciones; visualización de PNG/SVG/PDF en Mac, edición formal pendiente de entorno compatible |
| `powerdesigner/scripts/svg2png.py` usa ruta Windows de Edge | Regeneración auxiliar no portable | No ejecutarlo en Mac ni redibujar evidencia; no es requisito para validar modelos guardados |
| `tools/f27b/topdf*.ps1` requiere Word COM | Conversión PDF Windows | No ejecutarlo en macOS; entregables ya versionados. Una conversión nueva exige receta aprobada y revisión visual |
| `init-e2e-env.sh` usa GNU `sed -i` | Necesita contexto Linux | Usar la invocación Compose documentada; no modificar el script |
| Scripts `.sh` versionados sin bit ejecutable | No afecta receta actual | Se invocan con `sh`; no se requiere cambio de permisos |
| Dependencias opcionales Node Windows/Linux | No copiar bindings nativos | `npm ci` dentro del contenedor resuelve plataforma; el lock incluye bindings Darwin para instalación nativa opcional |
| CRLF/LF y separadores | `.gitattributes` fuerza LF; configuración runtime usa rutas relativas/Unix | Clone limpio; comprobar `git ls-files --eol` si una herramienta cambia finales |
| Cypress/Apple Silicon y ejecución real Mac | Pendiente de validación en host destino | No afirmar compatibilidad ARM verificada ni modificar imágenes automáticamente |

La inspección de archivos versionados encontró referencias Windows/PowerShell/XAMPP en 32 archivos, clasificadas en la tabla anterior, y 0 archivos con CRLF en el índice. No encontró ejecutables Windows `.exe/.dll/.msi/.bat/.cmd` ni cachés `.pyc`, `vendor/` o `node_modules/` añadidos al repositorio. Literales Windows usados como datos de pruebas negativas no son rutas de ejecución. No se modifica código productivo ni documentación histórica solo por contener una ruta local.

No se crea `scripts/check-macos-readiness.sh`: la checklist explícita cubre las mismas comprobaciones sin un script adicional ni instalación/escrituras implícitas. Ningún comando de esta receta fue ejecutado aquí contra una Mac o una base de datos.

## Seguridad y continuidad

Conservar el entorno local original de Windows y sus archivos ignorados/no rastreados: no limpieza, stash de ese entorno ni copia de sus secretos. Mantener `.env` y `.env.e2e` ignorados; revisar `git status` antes de cualquier publicación. No imprimir logs completos si contienen datos privados. No eliminar ramas históricas sin autorización expresa.

Solo datos ficticios/sintéticos en la Mac. La siguiente sesión puede preparar una rama específica para F35-SBX con autorización nueva de trabajo y alcance; este handoff no inicia esa fase, no modifica ADR-005 ni satisface los criterios externos pendientes.
