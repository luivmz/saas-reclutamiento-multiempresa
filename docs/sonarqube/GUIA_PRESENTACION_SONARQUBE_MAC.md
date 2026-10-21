# Guía de presentación SonarQube en Mac

Guion de **5–8 minutos**, basado exclusivamente en la ejecución del **20/10/2026**. [Resultados completos](RESULTADOS_SONARQUBE_MAC.md) · [Operación y cobertura reproducible](README.md). No presentar la evidencia histórica de Windows como ejecución de esta Mac.

## Antes de presentar

Abrir Docker Desktop y el dashboard del proyecto; iniciar sesión manualmente si se solicita. Mantener token/contraseña fuera de pantalla, terminal, docs y logs. Dejar accesibles el archivo raíz `sonar-project.properties`, `coverage.xml`, `storage/logs/sonarqube-scan.log` y el reporte de resultados. No abrir el archivo local de autenticación durante la exposición.

SonarQube y el SaaS se dejaron activos. Los comandos de arranque de abajo se usan si se detuvieron. El primer análisis tarda unos segundos, pero el tiempo puede cambiar: para un guion de duración fija conviene mostrar los logs ya obtenidos y hacer la reejecución antes de entrar a clase.

## Guion de 5–8 minutos

| Tiempo    | Pantalla/acción                                      | Explicación y dato real                                                                                                                                                                                                                       |
| --------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0:00–0:35 | Docker Desktop y contenedor `sonarqube`; `docker ps` | Se preservó la instancia anterior, imagen arm64. SonarQube Community 26.10.0.133078; servidor local en puerto 9000. No se borraron sus volúmenes.                                                                                             |
| 0:35–0:55 | `http://localhost:9000`, proyecto correcto           | Key `saas-reclutamiento-multiempresa`; nombre `SaaS Reclutamiento Multiempresa`. No confundir con el otro proyecto existente.                                                                                                                 |
| 0:55–1:30 | `sonar-project.properties`                           | Fuentes PHP/React/rutas juntas; pruebas PHP `tests`; exclusiones históricas; versión académica 1.1; no contiene autenticación.                                                                                                                |
| 1:30–2:05 | Log PHPUnit o ejecución breve                        | 411 aprobadas, 8 omitidas, 0 fallidas, 1498 aserciones. Las omitidas dependen de una función Fortify desactivada.                                                                                                                             |
| 2:05–2:45 | `coverage.xml`, primeras líneas y resumen            | PHPUnit genera Clover real con PCOV 1.0.12. PCOV se activa solo en el comando; 151 archivos y 2499/2777 sentencias cubiertas. No es JUnit. Rutas relativas permiten importarlo desde el host.                                                 |
| 2:45–3:20 | Versión y log SonarScanner                           | CLI 8.1.0.6389; mostrar `EXECUTION SUCCESS`, revisión analizada y URL. Token solo por entorno, fuera de pantalla. El servidor también confirmó tarea SUCCESS.                                                                                 |
| 3:20–4:00 | Overview / Quality Gate                              | Estado real OK. Explicar límite: primer análisis devolvió lista de condiciones evaluadas vacía; el gate Sonar way define umbrales de código nuevo. No significa que el código global supere 80 % de cobertura.                                |
| 4:00–4:45 | Issues                                               | 5 abiertos MAJOR: 3 Code Smells y 2 vulnerabilidades reportadas; 0 Bugs tradicionales. Abrir un hallazgo de carga de CV o sidebar y explicar que requiere revisión, sin corregirlo en vivo.                                                   |
| 4:45–5:15 | Security Hotspots                                    | 0 hotspots. Un hotspot es un punto que requiere revisión de seguridad, no automáticamente una vulnerabilidad; es distinto de los 2 hallazgos tipados como vulnerabilidad.                                                                     |
| 5:15–6:15 | Measures / Coverage / Duplications                   | Global 66.5 %, `app` 89.6 %, frontend y rutas 0 % por ausencia de reporte propio; no se excluyeron para elevar el porcentaje. Duplicación 0.0 %, 19495 líneas de código.                                                                      |
| 6:15–6:50 | Measures / Complexity / Debt                         | Complejidad ciclomática 2047, cognitiva 687, deuda tradicional estimada 30 min. Los valores MQR usan otra clasificación; no mezclar sus conteos/estimaciones.                                                                                 |
| 6:50–7:30 | Reporte de calidad                                   | PHPStan: 91 errores; Pint: 8 problemas; check global: 297 archivos con formato pendiente antes de estos docs; Oxlint: 5 warnings. TypeScript/build/Vitest pasaron. La preparación no escondió ni corrigió esa deuda.                          |
| 7:30–8:00 | Cierre                                               | Sonar complementa PHPUnit/Cypress, no ejecuta ni reemplaza sus pruebas. La cobertura exige un reporte real previo. Esta Mac ejecutó PHPUnit/Vitest; Cypress hoy quedó NO EJECUTADO. La decisión final sobre contratación sigue siendo humana. |

Para cinco minutos, resumir las dos últimas filas de medidas y mostrar los checks en una tabla, conservando la explicación del gate y de la cobertura parcial. No anunciar que el sistema está libre de vulnerabilidades o listo para producción.

# ARRANQUE RÁPIDO EN MAC

Desde la raíz del repositorio, en zsh. Los comandos de arranque/health, generación, normalización y entorno de autenticación fueron verificados. Ejecutar en orden; si falla una etapa, revisar su salida antes del scanner. Esperar `UP` en la API de Sonar tras iniciarlo.

```sh
open -a Docker
docker start sonarqube
docker compose up -d --wait
docker compose ps
curl -fsS http://localhost:9000/api/system/status
curl -fsS http://localhost:8000/health

docker compose exec -T app php artisan test
docker compose exec -T app php -d pcov.enabled=1 vendor/bin/phpunit --coverage-clover coverage.xml --colors=never
docker compose exec -T app php -r '$r = new DOMDocument(); if (!$r->load("coverage.xml") || $r->documentElement->tagName !== "coverage") { exit(1); } if (!copy("coverage.xml", "storage/logs/sonarqube-coverage-docker.xml")) { exit(1); } $n = 0; foreach ($r->getElementsByTagName("file") as $f) { $p = $f->getAttribute("name"); $prefix = getcwd()."/"; if (!str_starts_with($p, $prefix)) { fwrite(STDERR, "Unexpected Clover path\n"); exit(1); } $relative = substr($p, strlen($prefix)); if (!is_file($relative)) { exit(1); } $f->setAttribute("name", $relative); $n++; } if (!$r->save("coverage.xml")) { exit(1); } $x = new DOMXPath($r); $m = $x->query("/coverage/project/metrics")->item(0); echo "Clover normalized files=".$n." statements=".$m->getAttribute("statements")." covered=".$m->getAttribute("coveredstatements").PHP_EOL;'

export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN="$(< storage/app/private/.sonar-token)"
sonar-scanner
unset SONAR_TOKEN
open 'http://localhost:9000/dashboard?id=saas-reclutamiento-multiempresa'
```

No mostrar ni imprimir la variable de autenticación; no activar debug. Este bloque lee el token local proporcionado por el usuario sin incluir su valor en historial. Si ya no es válido, detenerse en autenticación. `EXECUTION SUCCESS` acredita envío; revisar también la finalización del procesamiento en la instancia antes de mostrar resultados nuevos.

El comando de cobertura escribe solamente el artefacto generado y la base testing; el arranque del SaaS puede aplicar migraciones normales. No ejecutar la receta contra una base externa/productiva. Si no cambió la imagen no hace falta reconstruirla cada día.

## Controles adicionales antes de entrar a clase

```sh
docker compose exec -T app composer types:check
docker compose exec -T app vendor/bin/pint --test
docker compose exec -T app npm run types:check
docker compose exec -T app npm run check
docker compose exec -T app npx vp lint
docker compose exec -T app npx vp test --run
```

Los fallos de PHPStan/Pint/Vite Plus son resultados esperados de esta línea base y deben explicarse, no borrarse mediante correctores automáticos. No ejecutar Cypress por rutina: su entorno aislado requiere preparación y reset separados.

## Al terminar

Parada segura documentada, no ejecutada al cerrar la preparación:

```sh
docker compose down
docker stop sonarqube
```

No añadir `-v`, no eliminar `sonarqube`, no borrar volúmenes, no ejecutar prune ni recrear la base principal. Conservar los logs, Clover y token privado para la repetición autorizada; estos artefactos no se añaden a Git. No se realizó commit ni push: los cambios están pendientes de revisión manual.
