# SonarQube en macOS Apple Silicon

Preparación local académica verificada el 20/10/2026 en la rama `chore/sonarqube-macos-setup`. No es un despliegue productivo. [Resultados medidos](RESULTADOS_SONARQUBE_MAC.md) · [Guion y arranque rápido](GUIA_PRESENTACION_SONARQUBE_MAC.md).

## Arquitectura y versiones verificadas

- macOS 27.0.1, arm64; Docker Desktop/Engine 29.7.2 y Compose v5.5.1.
- SonarQube Community 26.10.0.133078, contenedor existente `sonarqube`, imagen Linux arm64 `sonarqube:community`.
- SonarScanner CLI 8.1.0.6389 de Homebrew; launcher local OpenJDK 27 y motor de análisis con Java 21.0.12.1 Eclipse Adoptium provisionado por el scanner, según el log.
- SaaS en Compose: `app`, `queue`, PostgreSQL 17.11 y Redis 7.4.11. PHP 8.4.25, Laravel 13.31.0, Composer 2.10.3, Node 22.23.2 y npm 10.9.8 dentro de `app`.
- PCOV 1.0.12 compilado nativamente para arm64, cargado y desactivado por defecto. PHP de macOS no se modificó.

Sonar es un contenedor separado del Compose del SaaS. La aplicación sirve React/Inertia compilado en `http://localhost:8000`; Sonar está en `http://localhost:9000`. El proyecto Sonar usa la key `saas-reclutamiento-multiempresa` y el nombre `SaaS Reclutamiento Multiempresa`.

## Preservación de la instancia anterior

Se reutilizó el contenedor `de01957cd314d45dfc2c0ed11b59e91e05df4143776ef5eaf0f83dbf8e91f019`, creado el `2026-10-14T02:17:27.579399471Z`, imagen ID `sha256:2e378f7852b67d43507d3d383ee8fb5a522b8b0f920be9803f74f72952fce8f1`. Política restart: `no`; publica `9000:9000`. No se recreó ni se migraron datos.

Volúmenes anónimos conservados:

| Destino del contenedor      | Nombre/ID del volumen                                              |
| --------------------------- | ------------------------------------------------------------------ |
| `/opt/sonarqube/data`       | `b1537cfa9a0705782e79417257320d5add31739e38fd0af9fde0421eb7fd462c` |
| `/opt/sonarqube/extensions` | `a3d0aee8a48ec96b7cea6851f90bd7a2116de0195fd1d3af9e12370ad8e6cfff` |
| `/opt/sonarqube/logs`       | `31c2891b7781bf5b4b62de5c838c6992fed475aa65d56a1d183d5f60b15bd716` |
| `/opt/sonarqube/temp`       | `52510b34908339d799a67465a2b0f9f84424bb51309554291360f8816e09e72c` |

No existen los volúmenes nombrados `sonarqube_data`, `sonarqube_logs`, `sonarqube_extensions` en el inventario realizado. No se crearon sustitutos: los datos están en los IDs anteriores. La instancia usa H2 embebido y advierte que es solo para evaluación. Antes de cualquier futura recreación/migración se necesita un plan de copia y restauración; esta preparación no realiza esa operación.

La consulta autenticada inicial devolvió 404 para la key del SaaS y el inventario solo tenía otro proyecto sin equivalentes. Se creó el proyecto autorizado del SaaS; el otro proyecto se preservó. No se reutilizaron tokens del historial.

## Arranque diario

Abrir Docker Desktop en macOS. Los comandos de apertura se verificaron durante la preparación:

```sh
open -a Docker
docker info
docker start sonarqube
docker compose up -d --wait
docker compose ps
curl -fsS http://localhost:9000/api/system/status
curl -fsS http://localhost:8000/health
```

Esperar a que Sonar indique `UP`; `docker start` no espera la inicialización. Si hace falta, consultar `docker logs --tail 100 sonarqube`. El SaaS debe mostrar `app`, `queue`, `postgres`, `redis` healthy y `/health` debe devolver database/redis ok.

El entrypoint del SaaS instala desde locks si faltan dependencias, compila si falta el manifest y ejecuta migraciones normales con `migrate --force`. Antes de arrancar, verificar localmente que `.env` sigue apuntando a `DB_HOST=postgres`, `DB_DATABASE=reclutamiento`, sin URL externa/productiva. No imprimir sus credenciales. No se usa reset de la base demo. No se detectaron conflictos de puertos 5432/6379/8000 y no se detuvieron servicios Homebrew.

## Imagen PHP con cobertura

Solo al cambiar el Dockerfile/php.ini, reconstruir la imagen compartida:

```sh
docker compose build app
docker compose up -d --wait
docker compose exec -T app php --ri pcov
```

`app` y `queue` comparten `reclutamiento-php:dev`; una construcción de `app` basta. El resultado debe indicar PCOV 1.0.12 y soporte desactivado en uso normal. No instalar otro driver por rutina.

Origen revisado: [PECL PCOV 1.0.12](https://pecl.php.net/package/pcov/1.0.12), licencia PHP, release estable con compatibilidad PHP 8.4. La versión se fija como `ARG PCOV_VERSION=1.0.12` y se compila mediante PECL en la imagen. Es código nativo adicional de desarrollo; se validaron build arm64, carga CLI y ejecución PHPUnit. `pcov.enabled=0` evita activar la recolección normalmente, según la [documentación del proyecto PCOV](https://github.com/krakjoe/pcov). No se añade una dependencia Composer/npm ni se cambia PHP host.

## PHPUnit y Clover real

La base de pruebas es exclusivamente `reclutamiento_testing`, forzada en `phpunit.xml`; las pruebas escriben allí. Antes de repetirlas, confirmar que sigue siendo una base local y descartable. No ejecutar estas suites contra datos importantes.

Baseline sin cobertura:

```sh
docker compose exec -T app php artisan test
```

Generación verificada con PHPUnit 12.5.35; activar PCOV solo en este proceso:

```sh
docker compose exec -T app php -d pcov.enabled=1 vendor/bin/phpunit --coverage-clover coverage.xml --colors=never
```

PHPUnit escribe rutas absolutas del contenedor. El scanner corre en macOS: normalizar únicamente los atributos `file/@name`, conservando una copia original. El siguiente comando fue ejecutado y comprobado:

```sh
docker compose exec -T app php -r '$r = new DOMDocument(); if (!$r->load("coverage.xml") || $r->documentElement->tagName !== "coverage") { exit(1); } if (!copy("coverage.xml", "storage/logs/sonarqube-coverage-docker.xml")) { exit(1); } $n = 0; foreach ($r->getElementsByTagName("file") as $f) { $p = $f->getAttribute("name"); $prefix = getcwd()."/"; if (!str_starts_with($p, $prefix)) { fwrite(STDERR, "Unexpected Clover path\n"); exit(1); } $relative = substr($p, strlen($prefix)); if (!is_file($relative)) { exit(1); } $f->setAttribute("name", $relative); $n++; } if (!$r->save("coverage.xml")) { exit(1); } $x = new DOMXPath($r); $m = $x->query("/coverage/project/metrics")->item(0); echo "Clover normalized files=".$n." statements=".$m->getAttribute("statements")." covered=".$m->getAttribute("coveredstatements").PHP_EOL;'
test -f coverage.xml
head -n 10 coverage.xml
```

La normalización no cambia líneas, contadores ni porcentajes. La ejecución del 20/10 produjo 151 archivos, 2777 sentencias y 2499 cubiertas. `coverage.xml` está ignorado por Git y se conserva localmente como evidencia entregable por separado; también se ignora `.scannerwork/`. **JUnit no es cobertura.**

El `<source>` PHPUnit existente cubre `app/`, no React ni `routes/`. Sonar importa Clover con `sonar.php.coverage.reportPaths=coverage.xml`, conforme a su [documentación PHP](https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/test-coverage/php-test-coverage). La diferencia entre cobertura Clover y global Sonar se explica en el reporte; no se añadieron exclusiones de cobertura para mejorar porcentajes.

## Controles de calidad

```sh
docker compose exec -T app composer types:check
docker compose exec -T app vendor/bin/pint --test
docker compose exec -T app npm run types:check
docker compose exec -T app npm run check
docker compose exec -T app npx vp lint
docker compose exec -T app npx vp test --run
docker compose exec -T app npm run build
```

Consultar los resultados reales: PHPStan/Pint/Vite Plus fallan en esta línea base. `npm run check` se detiene por formato; por eso se ejecutó Oxlint separadamente, sin `--fix`. No ejecutar correctores globales. Cypress se dejó **NO EJECUTADO**, pues falta `.env.e2e` y su preparación/suite genera credenciales y reinicia una BD E2E; no bloquea Sonar. No se lanzó el servicio ML.

## Autenticación y scanner

El usuario proporcionó un token nuevo en `storage/app/private/.sonar-token`, ignorado por Git, para uso local. No mostrarlo ni copiarlo a configuración, docs, logs o historial. Si expira, obtener otro mediante la UI y entregarlo de forma segura; no reutilizar historial ni credenciales por defecto.

En zsh, dentro de la raíz del repositorio, la lectura y exportación segura se verificaron sin imprimir el valor:

```sh
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN="$(< storage/app/private/.sonar-token)"
sonar-scanner
unset SONAR_TOKEN
```

El valor se transmite por entorno; no usar argumentos de autenticación ni modos DEBUG/verbose. Las propiedades del archivo raíz se contrastaron con la [documentación Community](https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/analysis-parameters/parameters-not-settable-in-ui) y la API de la instancia 26.10. No se usa `sonar.login` ni se guarda autenticación en el archivo.

El análisis conserva `sonar.sources=app,resources/js,routes`, `sonar.tests=tests` y las exclusiones históricas. Se explicitan nombre, versión académica 1.1, UTF-8, inclusiones `tests/**` y ruta Clover. Los `.test.tsx` de componentes permanecen bajo el alcance fuente histórico; la línea base incluso contiene una incidencia en uno de ellos. Los bindings generados ignorados por Git se excluyen por el comportamiento SCM predeterminado. No se amplió el alcance a ML, Cypress, database o documentación.

No basta con `EXECUTION SUCCESS`: comprobar la tarea del servidor indicada por `.scannerwork/report-task.txt` y su estado `SUCCESS`. Su key debe ser exactamente la del SaaS. La API disponible se puede consultar en `http://localhost:9000/web_api`; durante la preparación se verificaron autenticación, componentes, procesamiento, medidas, Issues, Hotspots y Quality Gate con el token solo en memoria.

## Dashboard y evidencias

```sh
open 'http://localhost:9000/dashboard?id=saas-reclutamiento-multiempresa'
```

Durante esta preparación los logs de comandos/scanner se capturaron y sanearon antes de escribirlos. Están en `storage/logs/sonarqube-*.log`; snapshots de API y ejecuciones en `sonarqube-resultados-api.json` y `sonarqube-checks.json`, también ignorados. La autenticación no está en ellos. Los logs de una repetición se deben conservar sin secretos y sin activar debug.

El primer análisis devolvió Gate `OK` sin condiciones evaluadas. No significa que toda la aplicación cumpla 80 % de cobertura o que no tenga vulnerabilidades. Revisar medidas globales y código nuevo por separado. Un **Security Hotspot no equivale automáticamente a una vulnerabilidad**; ambos se explican con sus resultados reales en el reporte.

## Apagado seguro

Comandos de parada documentados; no se ejecutaron al cerrar la preparación para dejar la demo disponible:

```sh
docker compose down
docker stop sonarqube
```

`down` sin opciones elimina los contenedores/red del SaaS, conservando sus volúmenes nombrados; no alcanza al contenedor Sonar separado. `docker stop sonarqube` solo lo detiene. **No añadir `-v`, no eliminar el contenedor Sonar, no borrar sus volúmenes, no ejecutar prune ni resetear la base demo.** Los comandos de parada no se presentan como una prueba realizada hoy.
