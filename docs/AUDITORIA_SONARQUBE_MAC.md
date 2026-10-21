# AUDITORÍA SONARQUBE EN MAC

## 1. Resumen ejecutivo

Auditoría de solo diagnóstico realizada el **20/10/2026, America/Lima**, sobre el estado observado aproximadamente a las **15:30–15:34**. No se iniciaron servicios, pruebas ni análisis Sonar. Se consultaron archivos locales, versiones, el historial autorizado y recibos de instalación, sin instalar ni configurar herramientas.

**Ya tenemos:** Docker Desktop 4.90.0, Docker CLI 29.7.2, Compose v5.5.1, PHP 8.5.10, Composer 2.10.3, Node activo 20.20.2, npm 10.8.2 y **SonarScanner CLI 8.1.0.6389** en PATH. Homebrew también conserva Node 26.8.2, pero el shell usa la instalación de NVM. El proyecto tiene PHPUnit, suites Unit/Feature, pruebas Cypress/Vitest y herramientas de calidad declaradas en sus locks.

**Actualmente inaccesible:** Docker Engine en el contexto `desktop-linux`; falta su socket. No hay respuesta HTTP en `localhost:9000` ni en `localhost:8000/health`. No se puede afirmar qué contenedores están detenidos o qué imágenes/volúmenes se conservan hasta consultar el Engine. Docker Desktop instalado no equivale a Engine disponible.

**Evidencia anterior encontrada en esta Mac: SÍ.** El historial zsh contiene comandos para crear un contenedor `sonarqube`, usar `sonarqube:lts-community` y `sonarqube:community`, publicar `9000:9000`, iniciar/parar/eliminar el contenedor y ejecutar el scanner con la clave **`saas-reclutamiento-multiempresa`**. Hay credenciales históricas, siempre omitidas o representadas como `********`. La caché `~/.sonar` contiene motores y analizadores PHP/JavaScript. **Esto no demuestra que una ejecución terminara correctamente ni que un Quality Gate fuera aprobado.**

**Falta preparar:** configuración persistente del proyecto, validación de autenticación actual, driver de cobertura en el runtime elegido, reporte Clover válido e importación, y verificación de análisis/dashboard. No existe `sonar-project.properties`, ni reporte de cobertura en el proyecto. PHP host no tiene Xdebug/PCOV; tampoco están instalados por el Dockerfile definido.

Se identifican **8 grupos de pendientes importantes**, enumerados en §13. No hay evidencia que justifique reinstalar Docker, PHP, Composer, Node o el scanner. Tampoco se justifica descargar de nuevo SonarQube sin inventariar primero Docker.

Este reporte amplía el alcance del [reporte anterior](REPORTE_ESTADO_SONARQUBE.md), conservado sin cambios: aquella auditoría del repositorio no consultó el historial del host. Encontrar ahora parámetros históricos fuera del repositorio no convierte esos parámetros en configuración vigente del proyecto.

Convenciones: **AS-IS** = observado hoy; **histórico** = comando/artefacto preexistente, sin atribuir éxito; **TO-BE** = trabajo futuro no ejecutado. La guía original completa no fue proporcionada: la numeración de pasos de §11–§12 es una **numeración operativa reconstruida de los elementos descritos por el usuario**, no una numeración editorial verificada de ese documento.

## 2. Sistema y proyecto

| Dato | Resultado |
|---|---|
| Ruta absoluta | `/Users/luisvilameza/Universidad/Pruebas_Calidad/Project_SaaS/saas-reclutamiento-multiempresa` |
| Proyecto confirmado | `saas-reclutamiento-multiempresa`, nombre final de la ruta actual |
| Arquitectura Mac | `arm64`, obtenida mediante `uname -m` |
| macOS | `27.0.1`, build `26A434`, según `sw_vers` |
| Arquitectura scanner | `aarch64`, según salida del scanner |
| Rama | `main`, conservada |
| HEAD | `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6` |
| Origin fetch/push | `https://github.com/luivmz/saas-reclutamiento-multiempresa.git` |
| Estado inicial | `## main...origin/main` y `?? docs/REPORTE_ESTADO_SONARQUBE.md` |
| Working tree | No limpio: reporte anterior sin rastrear; ningún cambio rastreado/staged encontrado |
| Estado final esperado | Reporte anterior preservado y este reporte nuevo sin rastrear; sin commits |
| Sincronía remota | No comprobada en vivo; no se ejecutó fetch |
| Fase documental vigente | F34E cerrada; handoff macOS publicado; F35-SBX aún no iniciada, según `CLAUDE.md` y `docs/PROGRESS.md` |

Se leyeron `CLAUDE.md`, `project-guardian`, su checklist, `academic-traceability` y las pautas pertinentes de `laravel-saas-quality`, además de contexto v1.1/handoff. La instrucción específica del usuario autoriza esta auditoría en la rama actual y prohíbe cambiarla, hacer commits o editar documentos existentes; prevalece sobre el flujo habitual de rama/commit de la skill. El archivo previo sin rastrear pertenece a la auditoría anterior de esta conversación y se preserva. No se modifican RF, multitenencia, auditoría, decisión humana ni el ML experimental.

## 3. Docker

| Comprobación | Resultado actual | Evidencia |
|---|---|---|
| Docker Desktop instalado | **SÍ** | `/Applications/Docker.app`; cask local `docker-desktop 4.90.0,238679` |
| Docker CLI disponible | **SÍ** | `Docker version 29.7.2, build a7dcaa6` |
| Docker Compose disponible | **SÍ** | `Docker Compose version v5.5.1` |
| Docker Engine disponible | **NO en el contexto consultado** | `docker info --format '{{json .}}'` termina con salida 1; contexto `desktop-linux` |
| Imágenes actuales | ❓ NO SE PUEDE DETERMINAR | Engine inaccesible |
| Contenedores actuales | ❓ NO SE PUEDE DETERMINAR | Engine inaccesible |
| Volúmenes actuales | ❓ NO SE PUEDE DETERMINAR | Engine inaccesible |

Error observado:

```text
failed to connect to the docker API at unix:///Users/luisvilameza/.docker/run/docker.sock
dial unix /Users/luisvilameza/.docker/run/docker.sock: connect: no such file or directory
```

El JSON del comando incluye contadores vacíos/cero sin datos de servidor cuando falla la conexión: **no se interpretaron como inventario de cero imágenes o cero contenedores**. No se abrió Docker Desktop ni se cambió de contexto.

Por la condición impuesta por el usuario, al no haber Engine disponible **no se ejecutaron** `docker ps`, `docker ps -a`, `docker images`, `docker volume ls`, `docker inspect sonarqube` ni `docker logs --tail 50 sonarqube`. Tampoco se consultó PHP dentro de `app`: no se acreditó un servicio ya existente y activo.

Puerto 9000:

- `lsof -nP -iTCP:9000 -sTCP:LISTEN`: sin salida, código 1; no se observó nombre de proceso ni PID.
- `curl -I --max-time 5 http://localhost:9000`: salida 7, no se pudo conectar.
- Clasificación: **puerto 9000 libre en la comprobación local, sin listener visible**. No hay evidencia de ocupación por SonarQube ni por otro proceso en ese momento; repetir antes de una operación futura.

Proyecto funcionando hoy: `curl --fail --max-time 5 http://localhost:8000/health` también termina con salida 7. No se arrancó la aplicación para corregirlo.

Compose existente: solo se localizó `docker-compose.yml` como archivo operativo Compose. Define `app`, `queue`, `postgres`, `redis` y, bajo perfil `e2e`, `app-e2e`, `queue-e2e`, `cypress`. PostgreSQL `17.11-alpine`, Redis `7.4.11-alpine`; app usa `reclutamiento-php:dev`. No contiene SonarQube ni scanner. `docs/academico/qa-final/evidencias/03-compose-config.log` es evidencia histórica, no otro Compose operativo.

Advertencia derivada de código real: el entrypoint instala dependencias si faltan, puede crear entorno/clave/assets y ejecuta `php artisan migrate --force` en cada arranque. Por eso **no se ejecutó `docker compose up` como diagnóstico**. La existencia de una receta de arranque no autoriza esas escrituras durante esta auditoría.

## 4. SonarQube Server

| Elemento | Evidencia histórica/local | Estado actual |
|---|---|---|
| Imagen `sonarqube:lts-community` | Comando de historial, líneas 821–824 | ❓ NO SE PUEDE DETERMINAR si sigue descargada |
| Imagen `sonarqube:community` | Comandos de historial, líneas 926–929 y 936–939 | ❓ NO SE PUEDE DETERMINAR si sigue descargada |
| Contenedor `sonarqube` | `docker run --name sonarqube`, `start`, `stop`, `rm` en historial | ❓ NO SE PUEDE DETERMINAR si existe actualmente |
| Publicación `9000:9000` | Presente en los tres comandos `run` reconstruidos | Sin servicio HTTP respondiendo hoy |
| `sonarqube_data` | Sin referencias en historial inspeccionado ni Compose | ❓ NO SE PUEDE DETERMINAR su existencia actual |
| `sonarqube_logs` | Sin referencias en historial inspeccionado ni Compose | ❓ NO SE PUEDE DETERMINAR su existencia actual |
| `sonarqube_extensions` | Sin referencias en historial inspeccionado ni Compose | ❓ NO SE PUEDE DETERMINAR su existencia actual |
| Montajes del contenedor | Los `run` históricos encontrados no contienen `-v`, `--volume` ni `--mount` | Montajes actuales, incluidos posibles anónimos, desconocidos |
| Estado/health actual | Sin inspect/logs actuales por falta de Engine | ❓ NO SE PUEDE DETERMINAR |
| Fecha de creación del contenedor | Historial sin timestamps por comando | ❓ NO SE PUEDE DETERMINAR |
| Política de reinicio | No se inspeccionó contenedor | ❓ NO SE PUEDE DETERMINAR |
| Dashboard `http://localhost:9000` | URL encontrada en historial | HTTP no disponible hoy; acceso previo a UI no acreditado |
| Versión del servidor | Sin respuesta/inspect actual | ❓ NO SE PUEDE DETERMINAR |

Hay evidencia de comandos históricos de eliminación del contenedor. No debe inferirse que hoy existe un contenedor simplemente detenido, ni que sus datos sobreviven. Tampoco debe inferirse que los tres volúmenes nombrados están ausentes: sin Engine no se pueden clasificar honestamente como «existe/no existe».

El nombre de un motor en caché incluye `9.9.8.100196`, pero **eso no determina la versión del servidor actual** ni demuestra a qué instancia pertenecía. `community` y `lts-community` son referencias históricas distintas; no se sustituyeron imágenes ni se verificaron manifiestos ARM mediante red.

## 5. SonarScanner CLI

| Dato | Resultado verificado |
|---|---|
| Instalado | **SÍ** |
| Disponible en PATH | **SÍ**, `which sonar-scanner` devuelve ruta |
| Ruta pública | `/opt/homebrew/bin/sonar-scanner` |
| Ruta resuelta | `/opt/homebrew/Cellar/sonar-scanner/8.1.0.6389/bin/sonar-scanner` |
| Versión | `SonarScanner CLI 8.1.0.6389` |
| Host identificado por scanner | `Mac OS X 27.0.1 aarch64` |
| Configuración global indicada | `/opt/homebrew/Cellar/sonar-scanner/8.1.0.6389/libexec/conf/sonar-scanner.properties` |
| Propiedades activas globales | **0**: archivo con comentarios/líneas vacías, sin asignaciones activas |
| Configuración raíz de proyecto | `Project root configuration file: NONE` |
| Instalación Homebrew | Fórmula `sonar-scanner`, recibo `arm64`, `homebrew/core`, instalación solicitada |
| Fecha del recibo scanner | `2026-10-07T02:21:25Z` (06/10/2026 21:21:25 en Lima) |
| `~/.sonar/` | Existe: subdirectorios `_tmp`, `cache`, `js` |
| Variables `SONAR*` del proceso | Ninguna encontrada |

Se ejecutó únicamente `sonar-scanner --version`, nunca un análisis. La salida de versión no imprime la versión Java. Inspección del launcher: usa `JAVA_HOME` si existe, o el OpenJDK de Homebrew en `/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home`; no había `JAVA_HOME` en el entorno del proceso. El launcher interno tiene `use_embedded_jre=false`. La consulta directa `.../bin/java -version` devuelve **OpenJDK 27, Homebrew, 64-Bit Server VM**. Esto verifica el Java local seleccionado por ese launcher, no la compatibilidad de una futura ejecución con un servidor concreto.

Se revisaron únicamente referencias Sonar en `.zshrc` y `.zprofile` existentes: ninguna. No se modificaron archivos de shell ni configuración global. La caché no es una configuración autenticada de proyecto.

## 6. Configuración Sonar del proyecto

Se inventariaron archivos ocultos/ignorados fuera de `.git` y dependencias, y se buscaron las propiedades, variables y términos Sonar solicitados. El reporte anterior se separó de los resultados para evitar confundir menciones documentales con configuración ejecutable. **No se encontraron coincidencias Sonar en los restantes archivos textuales del proyecto inspeccionados.**

| Propiedad/archivo | Proyecto actual | Evidencia histórica de esta Mac |
|---|---|---|
| `sonar-project.properties` | No existe | No se encontró comando que demuestre su creación |
| `sonar.projectKey` | Sin configuración persistente | `saas-reclutamiento-multiempresa`, repetido en cuatro invocaciones del scanner |
| `sonar.projectName` | Sin configurar | No encontrado |
| `sonar.projectVersion` | Sin configurar | No encontrado |
| `sonar.sources` | Sin configurar | `app,resources/js,routes` |
| `sonar.tests` | Sin configurar | `tests` |
| `sonar.exclusions` | Sin configurar | Lista reproducida debajo |
| `sonar.test.inclusions` | Sin configurar | No encontrado |
| `sonar.php.coverage.reportPaths` | Sin configurar | No encontrado |
| `sonar.sourceEncoding` | Sin configurar | No encontrado |
| `sonar.host.url` | Sin configurar | `http://localhost:9000`, histórico; HTTP actual falla |
| `SONAR_HOST_URL` | No encontrada en proceso/archivos de entorno del proyecto | Host transmitido como propiedad `-Dsonar.host.url` |
| Token/autenticación | Sin variable Sonar vigente encontrada | Argumentos `sonar.token=********` y `sonar.login=********` |
| `.scannerwork` / `report-task.txt` | No localizados en el proyecto | Sin registro final de tarea localizado |

Exclusiones históricas recuperadas:

```text
vendor/**,node_modules/**,public/build/**,storage/**,bootstrap/cache/**,docs/**,database/**,cypress/**,ml-service/**
```

El alcance anterior incluía PHP de `app`/`routes` y React/TypeScript de `resources/js` en un mismo proyecto; indicaba `tests` para pruebas PHP y excluía Cypress. No incluía cobertura ni todas las carpetas del monolito como fuentes. Es un **alcance histórico**, pendiente de confirmar como el deseado; no se lo presenta como un análisis completado o una configuración guardada.

Revisión de `composer.json`, `package.json`, `.github/workflows/tests.yml`, Docker, docs y rutas de scripts: sin script Sonar/cobertura preparado. No se localizaron Makefile, script de scanner, Compose Sonar separado ni configuración SonarCloud. El workflow ejecuta build/TypeScript/PHPUnit y declara `coverage: none`; no ejecuta Sonar.

`.env` existe, `.env.e2e` no existe. No hay claves `SONAR*` en `.env`, `.env.example` o `.env.e2e.example`. No se imprimieron secretos de esos archivos. La presencia de tokens históricos en Terminal **no verifica vigencia, permisos o existencia actual del proyecto en la UI**. No se recuperaron para utilizarlos ni se rotaron.

## 7. PHP, Composer, Node y npm

| Herramienta | Versión | Ruta | Estado |
|---|---|---|---|
| PHP host | `8.5.10` | `/opt/homebrew/bin/php` | ✅ YA ESTÁ; binario Mach-O arm64 |
| Composer host | `2.10.3` | `/opt/homebrew/bin/composer` | ✅ YA ESTÁ; ejecuta PHP 8.5.10 |
| Node activo | `20.20.2` | `/Users/luisvilameza/.nvm/versions/node/v20.20.2/bin/node` | ✅ YA ESTÁ; `process.arch=arm64` |
| npm activo | `10.8.2` | `/Users/luisvilameza/.nvm/versions/node/v20.20.2/bin/npm` | ✅ YA ESTÁ |
| Node conservado en Brew | `26.8.2` | `/opt/homebrew/Cellar/node/26.8.2` | ✅ YA ESTÁ como instalación adicional; no es el Node activo |
| Java OpenJDK | `27` | `/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home/bin/java` | ✅ YA ESTÁ; versión consultada |

No se ejecutaron scripts Composer/npm. `composer --version` fue la única ejecución Composer; no se instaló ni actualizó nada. Arquitectura Composer: recibo Homebrew arm64 y ejecución con PHP arm64; no se atribuye a Composer un binario nativo independiente.

Versiones reales del proyecto:

| Tecnología | Requisito / versión resuelta | Fuente |
|---|---|---|
| PHP declarado | `^8.3` | `composer.json` |
| PHP efectivo por dependencia bloqueada | `>=8.4.1` en `symfony/http-kernel v8.1.6` | `composer.lock` |
| Laravel | Requiere `^13.17`, resuelto `v13.31.0` | Composer/lock |
| Inertia Laravel | `v3.3.4` | Composer lock |
| PHPUnit | `12.5.35` | Composer lock |
| PHPStan / Larastan | `2.2.14` / `v3.12.0` | Composer lock |
| Laravel Pint | `v1.32.1` | Composer lock |
| React | `19.3.0` | npm lock |
| Inertia React | `3.7.1` | npm lock |
| TypeScript | `5.9.3` | npm lock |
| Vite / Vite Plus | `8.3.0` / `0.3.0` | npm lock |
| Vitest | `4.1.11` | npm lock |
| Cypress | Imagen `cypress/included:15.3.0`, script UI `cypress@15.3.0` | Compose/package.json; no dependencia npm del SaaS |
| ESLint / Prettier | No encontrados como paquetes/configuración del proyecto | Manifiestos, lock e inventario |
| Oxlint / Oxfmt | `1.79.0` / `0.64.0` | npm lock; bloques lint/fmt en `vite.config.ts` |

Scripts de calidad identificados, **no ejecutados**:

- Composer `types:check`: `phpstan analyse`, nivel 7 en `phpstan.neon`.
- Composer `lint:check`: `pint --parallel --test`; `lint` aplica cambios y no es diagnóstico.
- Composer `test`: limpia configuración, ejecuta Pint check, PHPStan y luego Artisan test; no equivale a solo PHPUnit.
- npm `check`: `vp check`; `check:fix` aplica cambios.
- npm `types:check`: `tsc --noEmit`; npm `build`: `vp build`.
- Componentes: comando documentado `npx vp test --run`.
- npm `cy:run` / `cy:open`: preparan entorno E2E; pueden generar token y reiniciar datos E2E durante la suite. UI puede descargar Cypress.

Dockerfile: PHP **8.4.25**, Composer **2.10.3**, Node **22.23.2**, phpredis **6.3.0**. Instala `pdo_pgsql`, `pgsql`, `zip`, `intl`, `bcmath`, `pcntl`, `opcache` y Redis; configuración PHP local en `docker/php/php.ini`. **No instala Xdebug ni PCOV**. No se construyó la imagen. El Node host activo satisface el rango Node 20 de Vite Plus (`^20.19.0`), aunque difiere de la versión Docker/CI probada.

Faltan `vendor/autoload.php`, `vendor/bin/phpunit` y `node_modules/.bin/vp` en el checkout. El proyecto monta dependencias en volúmenes Docker: no se puede saber si esos volúmenes ya las contienen con el Engine inaccesible. Esto no es una indicación automática de reinstalarlas en el host.

## 8. PHPUnit y cobertura

`phpunit.xml` existe; `phpunit.xml.dist` no existe. Contiene testsuites **Unit** (`tests/Unit`) y **Feature** (`tests/Feature`); source incluye **`app`**. Bootstrap: `vendor/autoload.php`. Fuerza `APP_ENV=testing`, PostgreSQL y `DB_DATABASE=reclutamiento_testing`, caché/sesión array, cola sync, correo array, E2E desactivado. Los scripts PostgreSQL de init crean las bases testing/E2E únicamente al inicializar un volumen nuevo; su existencia actual no se verificó.

| Elemento | Resultado |
|---|---|
| Xdebug HOST | ❌ no instalado en el PHP activo: `php --ri xdebug` → `Extension 'xdebug' not present.` |
| PCOV HOST | ❌ no instalado en el PHP activo: `php --ri pcov` → `Extension 'pcov' not present.` |
| `php -m` filtrado | Sin coincidencias Xdebug/PCOV |
| Xdebug DOCKER, definición | ❌ no instalado por el Dockerfile/configuración del proyecto |
| PCOV DOCKER, definición | ❌ no instalado por el Dockerfile/configuración del proyecto |
| Xdebug/PCOV contenedor real | ❓ NO SE PUEDE DETERMINAR; no se consultó PHP de un app activo |
| Cobertura PHPUnit | Source definido, pero sin sección de salidas/reportes y sin receta Clover/XML encontrada |
| `coverage.xml` / `clover.xml` / `lcov.info` | Ninguno localizado fuera de dependencias; no hay fecha ni contenido que validar |
| Carpeta `coverage/` | No localizada en el inventario fuera de dependencias |
| JUnit PHP/pytest | Sí, evidencias históricas en `docs/academico/qa-final/evidencias/`; son resultados de pruebas, no cobertura |
| Cobertura frontend | Sin LCOV ni instrumentación configurada encontrada; Oxlint/Oxfmt no generan cobertura |
| CI | `coverage: none`; no genera ni importa reporte Sonar |
| Cobertura Python | `pytest-cov` declarado y `[tool.coverage.run]` en `ml-service/pyproject.toml`; no es cobertura PHP ni evidencia de Clover |

**¿Podemos generar actualmente un `coverage.xml` listo para Sonar? ❌ No, falta driver/configuración.** En el runtime host comprobado no hay Xdebug/PCOV ni dependencias PHPUnit utilizables del checkout. En el runtime Docker definido tampoco hay driver; no se pudo inspeccionar una imagen/contenedor real. Además, hay que fijar una receta de generación Clover, su ruta y su importación Sonar, y tener lista una BD testing descartable. No se instaló driver ni se generó reporte.

Basta **una alternativa adecuada de driver** en el runtime elegido; no son obligatorios ambos Xdebug y PCOV ni instalar en host y Docker a la vez. No se inventa el nombre de un reporte válido: llamar a un archivo `coverage.xml` no acredita que contenga Clover.

La evidencia F29F del 30/09/2026 documenta PHPUnit **411 aprobadas, 8 omitidas, 0 fallidas**, Cypress **85/85**, Vitest **42/42** y pytest **533**, en otro entorno. No se repitieron hoy. `--log-junit` registra resultados; **no sustituye a `--coverage-clover`**. No se encontró receta de este último ni `sonar.php.coverage.reportPaths`.

## 9. Evidencia histórica de SonarQube en esta Mac

Se leyó solo el historial autorizado `~/.zsh_history`, filtrando eventos Sonar/puerto/volúmenes. Las líneas continuadas con barra inversa se agruparon antes de extraer propiedades. No se ejecutó ningún comando recuperado. Se emitieron resúmenes permitidos y credenciales enmascaradas, sin volcar historial completo ni comandos ajenos.

| Fuente | Hallazgo | Límite de la evidencia |
|---|---|---|
| zsh líneas 821–824 | `docker run`, nombre `sonarqube`, imagen `sonarqube:lts-community`, puerto `9000:9000` | Comando registrado; no contiene salida ni código de retorno |
| zsh 826 | Consulta `docker logs` de SonarQube | No conserva esos logs |
| zsh 827–828 | Instalación histórica `brew install sonar-scanner` y consulta de versión | No ejecutadas hoy; recibo actual confirma instalación |
| zsh 829–835 | Scanner del SaaS: key, fuentes, tests, host, token y exclusiones | Token `********`; sin prueba de finalización |
| zsh 836–842 | Segunda invocación, autenticación `sonar.login=********` y exclusiones | No demuestra que esa variante funcionara |
| zsh 843–848 | Otra invocación del scanner del SaaS con autenticación | Sin resultado/Quality Gate archivado |
| zsh 853–859 | Cuarta invocación del SaaS con exclusiones y `sonar.login=********` | No existe archivo de propiedades equivalente en el repo |
| zsh 870–871 | Comandos históricos `docker stop` y `docker rm` de `sonarqube` | No se atribuye su ejecución ni eliminación actual sin inventario |
| zsh 926–929 | `docker run` de `sonarqube:community`, nombre `sonarqube`, `9000:9000` | Sin flags de volúmenes nombrados |
| zsh 932 | `docker start sonarqube` | Evidencia de intento anterior de arranque, no de disponibilidad actual |
| zsh 934–939 | `stop`/`rm` seguidos de otro `run` de `sonarqube:community` | Estado persistido actual desconocido |
| zsh 941 | Nueva consulta `docker logs` | Sin salida archivada |
| zsh 943–947 | Scanner para **otro proyecto**, con token | No atribuir ese análisis al SaaS; credencial omitida |
| Docker hoy | Engine inaccesible | No confirma conservación de imagen/contenedor/volúmenes |
| Homebrew local | Fórmula scanner y recibo arm64 de 06/10 en Lima | Confirma instalación, no servidor |
| `~/.sonar/cache` | 26 archivos relevantes jar/log/properties encontrados en recorrido de hasta tres niveles; muestra incluye analizadores PHP y JavaScript | Artefactos de uso previo; no una transacción de análisis completa |

No se encontraron comandos explícitos **`docker pull sonarqube...`**, **`docker volume create` de Sonar** ni referencias a `sonarqube_data`, `sonarqube_logs` o `sonarqube_extensions` en el historial inspeccionado. `docker run` puede obtener una imagen ausente, pero **no se infiere que una descarga ocurriera o terminara** solo por el comando.

Ejemplos de parámetros históricos recuperados, **solo evidencia, no receta para ejecutar hoy**:

```text
sonar.projectKey=saas-reclutamiento-multiempresa
sonar.sources=app,resources/js,routes
sonar.tests=tests
sonar.host.url=http://localhost:9000
sonar.token=********
sonar.login=********
```

Los eventos zsh relacionados no contienen timestamps extendidos por comando. El archivo fue modificado por última vez `2026-10-14T13:17:28.317Z`; esa fecha no fecha cada comando. La caché incluye `sonar-scanner-engine-shaded-9.9.8.100196-all.jar` con mtime `2026-10-07T02:22:31.297Z`, y analizadores PHP/JavaScript con mtime alrededor de `2026-10-14T02:26:33Z`. Estos tiempos de archivos pueden reflejar descarga/copia; no se usan para inventar fechas o resultados de análisis específicos.

Homebrew administrado localmente:

```text
composer       2.10.3
node           26.8.2
openjdk        27
php            8.5.10
sonar-scanner  8.1.0.6389
docker-desktop 4.90.0,238679
```

La primera consulta `brew list --versions`, con autoactualización/analytics desactivados, intentó obtener metadatos API de Homebrew y falló por DNS (`Could not resolve host: formulae.brew.sh`). No instaló/actualizó paquetes. La consulta se completó **sin API**, añadiendo `HOMEBREW_NO_INSTALL_FROM_API=1`; se contrastó con recibos locales de Cellar y Caskroom. No se ejecutó `brew info` para evitar otra consulta remota innecesaria. El fallo DNS de esta sesión no demuestra ausencia permanente de Internet. No se elevaron permisos para descargar metadatos.

Conclusión histórica: **SÍ hay evidencia de instalación y uso/intentos de SonarQube en esta Mac**, incluidos parámetros del SaaS. **El éxito del análisis, acceso al dashboard y estado del Quality Gate previos son ❓ NO SE PUEDE DETERMINAR.** No se recuperó una captura o resultado final que lo pruebe.

## 10. Comparación con la guía

Estados usados exactamente: ✅ YA ESTÁ; ⚠️ EXISTE PERO FALTA VERIFICAR; ❌ FALTA; ❓ NO SE PUEDE DETERMINAR. «Falta» puede referirse a configuración o disponibilidad, no implica necesariamente instalar. Un registro histórico no acredita estado vigente. Las filas opcionales no se convierten en obligaciones nuevas.

| Elemento | Requerido | Estado actual | Evidencia | Acción pendiente |
|---|---|---|---|---|
| Docker Desktop | Sí para ruta Docker Mac | ✅ YA ESTÁ | App y cask 4.90.0 | Activarlo manualmente después de esta auditoría |
| Docker CLI | Sí | ✅ YA ESTÁ | 29.7.2 | Ninguna instalación |
| Docker Compose | Sí para SaaS | ✅ YA ESTÁ | v5.5.1 | Verificar runtime cuando Engine responda |
| Docker Engine | Sí para inventario/servidor Docker | ❌ FALTA | Socket inexistente; info salida 1 | Recuperar disponibilidad, sin reinstalar por defecto |
| PHP | Sí para pruebas PHP; host opcional con Docker | ✅ YA ESTÁ | Host 8.5.10 | Elegir runtime de pruebas/coverage |
| Composer | Sí para dependencias PHP; host opcional con Docker | ✅ YA ESTÁ | Host 2.10.3 | Verificar dependencias existentes al recuperar Docker |
| Node.js | Sí para frontend | ✅ YA ESTÁ | Activo 20.20.2, arm64 | Mantener referencia Docker 22.23.2 para reproducibilidad |
| npm | Sí para frontend | ✅ YA ESTÁ | 10.8.2 activo | Ninguna instalación inmediata |
| Proyecto funcionando | Sí para demo funcional/pruebas | ❌ FALTA | `/health` sin conexión | Verificar/activar en otra sesión sin migraciones no autorizadas |
| Imagen sonarqube:community | Según guía; puede estar ya descargada | ❓ NO SE PUEDE DETERMINAR | Run histórico; Engine inaccesible | Inventariar imágenes antes de pull |
| Contenedor sonarqube | Sí para ruta descrita | ❓ NO SE PUEDE DETERMINAR | Run/start/rm históricos | Inventariar antes de crear/iniciar |
| Puerto 9000 | Disponible para publicación | ✅ YA ESTÁ | Sin listener visible; curl conexión rechazada | Repetir control antes de usarlo |
| sonarqube_data | Persistencia prevista por guía | ❓ NO SE PUEDE DETERMINAR | Sin inventario Engine | Listar volúmenes; no crearlo todavía |
| sonarqube_logs | Persistencia prevista por guía | ❓ NO SE PUEDE DETERMINAR | Sin inventario Engine | Igual |
| sonarqube_extensions | Persistencia prevista por guía | ❓ NO SE PUEDE DETERMINAR | Sin inventario Engine | Igual |
| Servidor SonarQube | Sí para analizar | ❓ NO SE PUEDE DETERMINAR | Sin servicio en 9000; instalación conservada desconocida | Verificar contenedor/imagen antes de operar |
| Dashboard localhost:9000 | Sí para exposición | ❌ FALTA | Endpoint no accesible hoy | Verificar cuando servidor esté disponible |
| SonarScanner CLI | Sí para ruta CLI | ✅ YA ESTÁ | Versión 8.1.0.6389 | No reinstalar |
| SonarScanner en PATH | Sí | ✅ YA ESTÁ | `which sonar-scanner` | Ninguna |
| sonar-project.properties | Sí para receta persistente solicitada | ❌ FALTA | Archivo ausente | Crear solo en fase posterior autorizada |
| sonar.projectKey | Identidad obligatoria del análisis | ⚠️ EXISTE PERO FALTA VERIFICAR | Histórico `saas-reclutamiento-multiempresa` | Confirmar proyecto servidor y persistir |
| sonar.projectName | Nombre solicitado por guía; puede depender de UI/default | ❌ FALTA | Sin valor encontrado | Confirmar nombre; no inventarlo |
| sonar.projectVersion | Metadato opcional solicitado | ❌ FALTA | Sin valor encontrado | Decidir valor o documentar omisión |
| sonar.sources | Alcance fuente | ⚠️ EXISTE PERO FALTA VERIFICAR | Histórico app,resources/js,routes | Confirmar alcance deseado |
| sonar.tests | Alcance pruebas | ⚠️ EXISTE PERO FALTA VERIFICAR | Histórico tests | Confirmar separación y pruebas frontend |
| sonar.exclusions | Acotar análisis | ⚠️ EXISTE PERO FALTA VERIFICAR | Lista histórica en §6 | Revisar y persistir |
| sonar.test.inclusions | Condicional según layout | ❌ FALTA | Sin configuración | Decidir si es necesario; no inventar patrones |
| sonar.php.coverage.reportPaths | Sí para importar Clover PHP | ❌ FALTA | Sin propiedad/reporte | Fijar tras generar reporte real |
| sonar.sourceEncoding | Declaración solicitada por guía | ❌ FALTA | No encontrada | Confirmar codificación antes de configurar |
| SONAR_HOST_URL / host URL | Conexión al servidor | ⚠️ EXISTE PERO FALTA VERIFICAR | Host histórico `http://localhost:9000`; sin env vigente | Verificar instancia actual y persistencia segura |
| Token Sonar | Autenticación cuando la instancia la exige | ⚠️ EXISTE PERO FALTA VERIFICAR | Credenciales históricas `********` | Verificar vigencia/permisos en sesión posterior; sin generar hoy |
| PHPUnit | Sí para pruebas/cobertura PHP | ⚠️ EXISTE PERO FALTA VERIFICAR | Lock 12.5.35 y XML; sin binario checkout | Verificar runtime/dependencias Docker |
| Xdebug host | Alternativa de driver, no obligatorio junto a PCOV | ❌ FALTA | `php --ri xdebug` no presente | Solo instalar si se elige esta alternativa/runtime |
| PCOV host | Alternativa de driver | ❌ FALTA | `php --ri pcov` no presente | Igual; basta un driver apropiado |
| Xdebug Docker | Alternativa de driver en definición | ❌ FALTA | Dockerfile no lo instala | Runtime real desconocido; preparar si se elige |
| PCOV Docker | Alternativa de driver en definición | ❌ FALTA | Dockerfile no lo instala | Igual; no instalar ambos por rutina |
| coverage.xml | Salida prevista si se decide ese nombre/formato | ❌ FALTA | No localizado | Generar reporte real en fase posterior |
| Clover | Formato para cobertura PHP Sonar | ❌ FALTA | Sin receta/artefacto | Preparar driver/generación/ruta |
| Sonar analysis previo | Evidencia para reconstruir demo | ⚠️ EXISTE PERO FALTA VERIFICAR | Cuatro invocaciones del SaaS y caché | Éxito/finalización no determinados |
| Dashboard previo | Evidencia de exposición anterior | ❓ NO SE PUEDE DETERMINAR | Sin captura/resultado final | Consultar instancia original recuperada |
| Quality Gate previo | Evidencia de calidad Sonar | ❓ NO SE PUEDE DETERMINAR | Sin gate/resultados archivados | No afirmar aprobado/rechazado |

## 11. Pasos de la guía ya cumplidos

Numeración operativa adoptada para este informe, por no disponer de la guía original numerada:

| Paso operativo | Contenido | Resultado |
|---|---|---|
| 1 | Docker Desktop/CLI/Compose instalados y Engine disponible | ⚠️ Parcial: herramientas instaladas; Engine inaccesible |
| 2 | PHP/Composer y Node/npm cuando se usan | ✅ Cumplido en instalación del host; versiones diferenciadas de Docker |
| 3 | Imagen, contenedor y persistencia SonarQube | ⚠️ Evidencia histórica parcial; estado actual no determinable |
| 4 | Servidor/dashboard accesible en el puerto acordado | ❌ Pendiente hoy; no responde 9000 |
| 5 | SonarScanner CLI y PATH | ✅ Cumplido, versión 8.1.0.6389 |
| 6 | Proyecto/key/configuración persistente y alcance | ⚠️ Parámetros históricos recuperados; archivo/proyecto actual sin verificar |
| 7 | Autenticación válida | ⚠️ Token histórico encontrado; vigencia/permisos desconocidos |
| 8 | PHPUnit utilizable y cobertura Clover | ❌ Pendiente driver/reporte y verificación de runtime/dependencias |
| 9 | Análisis finalizado e importación de cobertura | ❌ Pendiente de comprobación actual; éxito anterior desconocido |
| 10 | Dashboard, Quality Gate, Issues, Hotspots y Measures listos | ❌ Pendiente para exposición actual; resultados anteriores desconocidos |

No hace falta repetir instalación del paso 2 ni del scanner del paso 5. El paso 3 **no puede declararse cumplido solo por el historial**. No se inventa un «paso de descarga pendiente» hasta conocer el inventario Docker actual.

## 12. Paso exacto desde donde continuar

**Debemos continuar desde el paso 1: activar manualmente Docker Desktop ya instalado y volver a comprobar la disponibilidad de Docker Engine.**

Ese es el primer punto incompleto de la secuencia operativa definida en §11. Después, la continuación inmediata es un inventario de solo lectura para decidir si el servidor existente se recupera o si realmente faltan imagen/contenedor/volúmenes. **No corresponde todavía descargar imágenes, crear volúmenes/contenedor o ejecutar el scanner.**

El número de página/paso equivalente en la guía original es **❓ NO SE PUEDE DETERMINAR** sin su numeración. El «paso 1» de este informe significa disponibilidad de Docker, no reinstalación.

## 13. Elementos faltantes

Ocho grupos importantes de pendientes, contabilizados una vez cada uno:

1. Engine accesible e inventario actual de imágenes/contenedor/volúmenes.
2. Runtime/dependencias del SaaS y PHPUnit utilizables, con bases de pruebas verificadas.
3. Configuración persistente Sonar e identidad/alcance confirmados.
4. Autenticación vigente y autorizada, sin secretos en archivos versionados.
5. Un driver de cobertura en el runtime elegido.
6. Clover válido y ruta de importación Sonar verificada.
7. Análisis del SaaS finalizado, ligado a la revisión correcta y con alcance comprobado.
8. Dashboard/Quality Gate/Issues/Hotspots/Measures actuales preparados para la exposición.

### Falta instalar

- **Un driver de cobertura PHP adecuado al runtime elegido**, si ese runtime coincide con el host comprobado o con la imagen definida. Elegir Xdebug o PCOV con versión/compatibilidad revisadas; no instalar ambos en ambos entornos.
- No falta instalar Docker Desktop/CLI/Compose, PHP, Composer, Node/npm o SonarScanner: su presencia se verificó.
- Dependencias del proyecto, imagen Sonar y volúmenes Docker: necesidad de instalación/descarga/creación **no determinable todavía**; no confundir ausencia del binario en el checkout con ausencia del volumen de dependencias.

### Falta crear

- `sonar-project.properties`, ausente, en una fase posterior autorizada.
- Reporte de cobertura Clover: actualmente no existe. Nombre/ruta definitivos pendientes de decisión y generación verificable.
- Proyecto UI, contenedor, imagen y volúmenes: no se acredita que falten; **verificar antes de crear**. No se propone un project name nuevo ni crear tokens por rutina.

### Falta configurar

- Identidad persistente, fuentes/tests/exclusiones y metadatos que correspondan. La key histórica ya está recuperada, pero su correspondencia con la instancia vigente no está comprobada.
- Host/autenticación segura; revisar token histórico sin publicarlo ni asumir que sigue vigente.
- Driver y receta de cobertura; conectar `sonar.php.coverage.reportPaths` con un archivo Clover validado.
- Alcance PHP/React deseado: confirmar si se preservan las exclusiones históricas, especialmente database, Cypress y ML. No ampliar ni reducir silenciosamente.

### Falta verificar

- Recursos Docker conservados, montajes/persistencia, arquitectura, versión y estado real del servidor.
- Dependencias en volúmenes y existencia de la base `reclutamiento_testing`; no ejecutar migraciones para comprobarlas.
- Acceso a la UI y proyecto correcto, permisos de autenticación, finalización de análisis y medidas reales.
- Compatibilidad Apple Silicon/imagen cuando se identifique la imagen conservada; no se consultó manifiesto remoto ni se forzó emulación.
- Los fallos de Pint/check documentados históricamente y las suites no se reejecutaron; no son evidencia Sonar actual ni cobertura.

## 14. Plan para completar SonarQube

**TO-BE. No ejecutado.** Contiene solo trabajo pendiente y verificaciones necesarias para decidirlo. No se reinstalan herramientas ya presentes. Los pasos mutantes requieren una sesión operativa posterior expresamente autorizada; esta auditoría termina con el reporte.

1. **Activar Docker Desktop manualmente**, sin comando automático. Comprobar después `docker info`. Si sigue fallando, diagnosticar ese error antes de continuar; no cambiar contexto/configuración a ciegas.
2. **Inventariar recursos, solo si Engine responde:**

   ```sh
   docker ps
   docker ps -a
   docker images
   docker volume ls
   ```

   Identificar ambas etiquetas históricas Sonar, contenedor `sonarqube` y los tres volúmenes nombrados. Si el contenedor existe, consultar entonces `docker inspect sonarqube` y `docker logs --tail 50 sonarqube`, filtrando secretos antes de mostrar salida. No arrancarlo como parte de este inventario.
3. **Determinar la recuperación que realmente falta.** Si el contenedor/servidor se conserva, revisar su imagen, versión y montajes antes de proponer activación. Si falta, preparar una receta revisable de servidor/persistencia para la arquitectura Mac. Solo en ese caso correspondería descargar/crear los recursos ausentes. No se proporciona un `docker pull`/`volume create`/`run` incondicional: hoy no se sabe qué falta, y no se debe duplicar o perder datos.
4. **Verificar servidor y UI después de su activación autorizada.** La dirección histórica real es `http://localhost:9000`; volver a comprobar puerto/HTTP. Consultar el proyecto con key histórica `saas-reclutamiento-multiempresa`; confirmar si existe, nombre mostrado, versión del servidor y permisos. No crear un proyecto duplicado ni inventar nombre/versión.
5. **Preparar la configuración persistente ausente**, con alcance confirmado y sin token en el archivo. Usar como evidencia los valores de §6; no asumir que una receta antigua completa equivale a la configuración actual deseada. Resolver project name/version, inclusiones/codificación y host a partir de comprobaciones reales, antes de escribir.
6. **Resolver autenticación vigente**, mediante un mecanismo seguro autorizado. El historial demuestra un token anterior, no su vigencia. No crear uno nuevo sin necesidad comprobada ni pegarlo en comandos que queden en historial. No se consulta ni genera durante esta auditoría.
7. **Preparar cobertura en un único runtime elegido.** Comprobar primero dependencias/bases ya existentes; autorizar por separado la extensión/configuración necesaria. Definir generación Clover y ubicación real. No usar `composer test` como diagnóstico inocuo: limpia caché y añade checks. No iniciar `app` sin revisar que su entrypoint migra y puede instalar dependencias.
8. **Ejecutar pruebas y generar Clover en una sesión posterior que permita esas escrituras.** Validar XML, timestamp, cobertura de `app` y rutas de archivos; JUnit no sirve como sustituto. Hasta fijar driver/receta/ruta reales no hay comando de cobertura listo para copiar sin inventar parámetros.
9. **Realizar el análisis Sonar solo después de completar lo anterior.** SonarScanner ya está instalado; confirmar configuración, identidad y autenticación. No se ejecuta aquí. Registrar salida final y tarea de procesamiento, comprobar importación de cobertura y revisión analizada. La receta exacta final depende de los datos pendientes; no se presenta una invocación autenticada incompleta como lista para uso.
10. **Preparar evidencia de exposición:** resumen del proyecto correcto con fecha/revisión; Quality Gate y sus condiciones; Issues; Security Hotspots y revisión; Measures de fiabilidad, seguridad, mantenibilidad, duplicaciones, líneas y cobertura si fue importada realmente. Nombres/pantallas concretas dependen del servidor recuperado. Mostrar resultados reales, sin inventar porcentajes o estado aprobado.

El plan no incluye resets demo/E2E, eliminación de volúmenes, actualizaciones ni instalación automática. No es posible cerrar una receta de servidor/análisis completamente ejecutable antes de conocer los recursos Docker conservados, la instancia y la ruta de cobertura.

## 15. Próximo paso recomendado

**Abrir Docker Desktop manualmente y esperar a que indique que el Engine está disponible.**

Un único próximo paso; **no ejecutado** por esta auditoría. No incluye arrancar SonarQube ni el SaaS por comandos. El estado de contenedores debe revisarse después, antes de cualquier creación/descarga.

## 16. NO MODIFICADO

Durante esta auditoría no se modificó código fuente, configuración, dependencias, bases de datos, contenedores, imágenes, volúmenes, historial Git ni secretos. La única modificación realizada fue la creación de este reporte Markdown.

No se cambió de rama, no se hizo commit/push/reset/checkout, no se arrancó/detuvo/reinició SonarQube, no se crearon archivos de configuración Sonar, no se generaron tokens y no se ejecutaron migraciones, suites, cobertura o análisis scanner. Solo se consultó la versión del scanner. El intento incidental de metadatos Homebrew y su fallo se declaran en §9; no se instalaron/actualizaron paquetes ni se descargaron imágenes Docker. No se modificó el historial Terminal ni la configuración global.

El reporte anterior `docs/REPORTE_ESTADO_SONARQUBE.md` se preservó; su SHA-256 observado antes de escribir este archivo fue `5f6253a1979fca4e7238b10610591c68e3d767ad1938f917950b9c2923b88f23`. Las verificaciones finales se limitan al alcance Git, estructura de este Markdown, enlaces, whitespace y comprobación de que no se copiaron secretos de entorno/historial. No se ejecuta regresión funcional por tratarse exclusivamente de una auditoría documental y por prohibición expresa del usuario.

Fuentes del proyecto: [CLAUDE.md](../CLAUDE.md), [PROGRESS.md](PROGRESS.md), [handoff macOS F34E](academico/handoff/F34E_MACOS_HANDOFF.md), [Compose](../docker-compose.yml), [Dockerfile](../docker/php/Dockerfile), [entrypoint](../docker/php/entrypoint.sh), [Composer](../composer.json), [lock PHP](../composer.lock), [npm](../package.json), [lock npm](../package-lock.json), [PHPUnit](../phpunit.xml), [PHPStan](../phpstan.neon), [Pint](../pint.json), [Vite](../vite.config.ts), [CI](../.github/workflows/tests.yml), [QA F29F histórico](academico/qa-final/F29F_Ejecucion_QA.md) y [métricas históricas](academico/metricas-calidad/README.md). Fuentes del host: comandos/versiones citados, recibos Homebrew locales, launcher/configuración global scanner, inventario acotado de `~/.sonar` e historial zsh filtrado/enmascarado.
