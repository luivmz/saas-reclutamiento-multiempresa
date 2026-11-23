# Resultados SonarQube – SaaS Reclutamiento Multiempresa

## 1. Fecha y entorno

✅ PASSED — Ejecución real en macOS el **20/10/2026**, America/Lima. Análisis enviado a las 16:01:32 y procesado a las 16:01:36 (21:01 UTC). Docker Desktop local, Linux arm64 en contenedores, datos ficticios. Rama `chore/sonarqube-macos-setup`; sin commit, push, merge o cambios funcionales.

Se preservaron el contenedor Sonar anterior, sus cuatro volúmenes anónimos y el otro proyecto existente. El SaaS no existía en esta instancia: consultas autenticadas de componente/análisis devolvieron 404 e inventario de proyectos no encontró equivalentes. Se creó únicamente el proyecto autorizado `saas-reclutamiento-multiempresa`, nombre `SaaS Reclutamiento Multiempresa`.

App/PostgreSQL/Redis/queue healthy; `/health` database/redis ok. La base principal `reclutamiento` conservó los conteos observados antes/después de pruebas: 2 organizaciones, 16 usuarios, 5 vacantes y 111 registros de auditoría. No se ejecutó reset de la base principal. La comparación de conteos no pretende ser un hash completo de todos los datos.

## 2. Commit analizado

✅ PASSED — SCM revision comunicada por el scanner: `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6`. Se analizaron los archivos presentes en el working tree, incluidos ajustes locales no commiteados de preparación. No se modificaron `app/`, `resources/`, `routes/`, `database/` ni `tests/`; tampoco locks/manifiestos o Compose. La documentación nueva queda fuera del alcance Sonar.

Task ID: `75d37311-1e13-4f14-bbe9-c77ba6fefde6`. Analysis ID: `0cd5eb83-5a78-42ae-8289-78af6dc0cf90`. Project Key comprobada en tarea y API: `saas-reclutamiento-multiempresa`.

## 3. Versiones

✅ PASSED — Versiones medidas, salvo donde se indica fuente de lock:

| Componente                            | Versión                                                            |
| ------------------------------------- | ------------------------------------------------------------------ |
| macOS                                 | 27.0.1, build 26A434                                               |
| Arquitectura Mac / imagen PHP / Sonar | arm64 / arm64 / arm64                                              |
| Docker Engine/CLI                     | 29.7.2                                                             |
| Docker Compose                        | v5.5.1                                                             |
| SonarQube Community                   | 26.10.0.133078, estado UP                                          |
| SonarScanner CLI                      | 8.1.0.6389                                                         |
| Java launcher host / motor scanner    | OpenJDK Homebrew 27 / Java 21.0.12.1 Eclipse Adoptium provisionado |
| PHP Docker                            | 8.4.25                                                             |
| PCOV                                  | 1.0.12, desactivado salvo comando coverage                         |
| Laravel                               | 13.31.0                                                            |
| Composer Docker                       | 2.10.3                                                             |
| Node / npm Docker                     | 22.23.2 / 10.9.8                                                   |
| PHPUnit                               | 12.5.35                                                            |
| PHPStan / Larastan                    | 2.2.14 / 3.12.0, versiones lock                                    |
| Pint                                  | 1.32.1, versión lock                                               |
| TypeScript                            | 5.9.3, versión lock                                                |
| Vite / Vite Plus                      | 8.3.0 / 0.3.0                                                      |
| Vitest                                | 4.1.11                                                             |
| Oxlint / Oxfmt                        | 1.79.0 / 0.64.0, versiones lock                                    |

## 4. PHPUnit

✅ PASSED — Baseline `docker compose exec -T app php artisan test`, salida **0**: **411 passed, 8 skipped, 0 failed, 1498 assertions**, duración reportada **10.32 s**. Total: **419** casos.

✅ PASSED — Segunda ejecución con cobertura: **419 tests, 1498 assertions, 8 skipped**, salida **0**, duración de pruebas **12.367 s**, memoria **97 MB**. Las omitidas dependen de la verificación de correo Fortify desactivada, como en la evidencia histórica. No se cambió esa configuración.

Evidencias: `storage/logs/sonarqube-phpunit-baseline.log`, `sonarqube-coverage.log`. PostgreSQL de pruebas: `reclutamiento_testing`; no la base demo. Mensajes ML de fallos simulados forman parte de los casos de prueba, no son una caída del servicio productivo.

## 5. PHPStan / Larastan

❌ FAILED — `docker compose exec -T app composer types:check`, salida **1**, **91 errores**; duración de proceso **3.413 s**. Nivel 7, configuración existente. No se corrigieron.

Incluye accesos a propiedades indefinidas de tipos unión en factories, por ejemplo `database/factories/InterviewFactory.php:23`, según la salida. Estos archivos no se modificaron en la preparación. Evidencia completa saneada: `storage/logs/sonarqube-phpstan.log`.

## 6. Pint

❌ FAILED — `docker compose exec -T app vendor/bin/pint --test`, salida **1**, **256 archivos, 8 problemas de estilo**, duración de proceso **4.645 s**. Coinciden con la deuda histórica registrada; no se ejecutó corrector.

- `app/Models/Vacancy.php`
- `app/Providers/AppServiceProvider.php`
- `app/Services/Assessments/AssessmentResultRecorder.php`
- `bootstrap/app.php`
- `database/seeders/DemoSeeder.php`
- `routes/web.php`
- `tests/Feature/Audit/AuditLoggerTest.php`
- `tests/Feature/Tenancy/CrossTenantAccessTest.php`

Evidencia: `storage/logs/sonarqube-pint.log`.

## 7. TypeScript

✅ PASSED — `docker compose exec -T app npm run types:check`, salida **0**, sin errores; duración de proceso **3.494 s**. npm mostró aviso de una nueva versión disponible; no se actualizó.

✅ PASSED — Build adicional `npm run build`, salida **0**; duración reportada **3.22 s**. Avisos informativos de plugins/fuentes se conservan en el log, sin instalar paquetes opcionales.

Evidencias: `storage/logs/sonarqube-typescript.log`, `sonarqube-build.log`.

## 8. Vite Plus / Oxlint / Oxfmt

❌ FAILED — `docker compose exec -T app npm run check`, salida **1**, formato pendiente en **297 archivos**, duración de proceso **3.531 s**. Esta medición se hizo antes de crear los tres documentos de `docs/sonarqube/`; incluye los reportes de auditoría anteriores, preservados sin cambios. No se reformateó código ni documentación histórica.

⚠️ WARNING — Repetición final después de crear y formatear únicamente los tres documentos nuevos: **297 archivos**, salida **1**, duración de proceso **2.962 s**. El formato de los tres documentos nuevos pasó su check acotado; el fallo global permanece en los archivos anteriores. Evidencia: `storage/logs/sonarqube-vp-check-final.log`.

❌ FAILED — Comprobación independiente `docker compose exec -T app npx vp lint`, salida **1**: **5 warnings, 0 errors**, **145 archivos, 111 reglas**, **425 ms** reportados. La configuración `denyWarnings` convierte avisos en salida no exitosa. Se ejecutó porque el check conjunto se detenía en formato y no acreditaba el paso de lint. No se usó `--fix`.

No es ESLint/Prettier: las herramientas reales son Oxlint/Oxfmt mediante Vite Plus. Evidencias: `storage/logs/sonarqube-vp-check.log`, `sonarqube-oxlint.log`. Los documentos nuevos pueden formatearse de forma acotada; eso no resuelve el fallo global.

## 9. Vitest

✅ PASSED — `docker compose exec -T app npx vp test --run`, salida **0**: **6 archivos, 42 pruebas aprobadas, 0 fallidas**, duración reportada **810 ms** (3.907 s incluyendo proceso Docker). Evidencia: `storage/logs/sonarqube-vitest.log`.

## 10. Cypress

⏭️ NO EJECUTADO — Requiere entorno E2E destructivo aislado. `.env.e2e` no existe; setup genera clave/token y la suite utiliza reset con migraciones de recreación en E2E. Se omitió para esta preparación; no bloquea el análisis Sonar.

La evidencia histórica 85/85 no se atribuye a hoy. No se ejecutó ningún reset de `reclutamiento`, no se generó token E2E y no se modificó código de pruebas.

## 11. Cobertura Clover

✅ PASSED — Se generó `coverage.xml` mediante PHPUnit 12 con PCOV activado exclusivamente en ese proceso. XML validado con raíz `coverage`, proyecto y métricas Clover: **151 archivos, 2777 sentencias, 2499 cubiertas** (aproximadamente 90.0 % de sentencias de ese reporte).

Las rutas originales `/var/www/html/app/...` se normalizaron a `app/...` para el scanner del host. Se comprobaron existencia de los archivos y conservación de métricas; copia original en `storage/logs/sonarqube-coverage-docker.xml`. No se alteraron contadores ni se excluyó código propio para elevar cobertura.

`coverage.xml` es artefacto local ignorado por Git; puede entregarse por separado. No contiene datos de casos de prueba ni credenciales, solo rutas y métricas de código. La colección se restringe al source `app/` ya declarado por PHPUnit. No hay LCOV frontend.

## 12. SonarScanner

✅ PASSED — CLI **8.1.0.6389**, salida **0**, **`EXECUTION SUCCESS`**, total reportado **10.805 s**. Archivo raíz persistente leído correctamente, token transmitido por entorno, sin argumentos de autenticación ni credenciales en configuración. Log saneado: `storage/logs/sonarqube-scan.log`. Se indexaron **338 archivos**, con perfiles **Sonar way core** para PHP y TypeScript; **108 archivos** quedaron fuera por reglas SCM. No se cambiaron perfiles ni reglas para este resultado.

✅ PASSED — Procesamiento servidor **SUCCESS**, ejecutado a `2026-10-20T21:01:36+0000`, **1870 ms**, `warningCount=0`. Project Key coincide exactamente. Task/analysis IDs en §2.

⚠️ WARNING — Java host mostró aviso de mutación reflexiva de campos finales por la biblioteca del scanner. No impidió ejecución y no se alteraron flags/Java para silenciarlo. La importación Clover consta en el log sin errores de resolución de rutas.

## 13. Quality Gate

✅ PASSED — API `api/qualitygates/project_status`, consultada por **analysisId**, devolvió **`OK`**. Gate asociado: **Sonar way**, predeterminado.

⚠️ WARNING — Este primer análisis devuelve **`conditions: []`**. El gate existe y su definición tiene condiciones sobre **código nuevo**, pero no hay condiciones evaluadas en esta respuesta. No presentar el `OK` como prueba de que el código global tenga cobertura ≥80 % o cero problemas de seguridad.

Definición consultada, sin modificarla:

| Métrica sobre código nuevo       | Umbral de error |
| -------------------------------- | --------------- |
| `new_violations`                 | >0              |
| `new_coverage`                   | <80 %           |
| `new_duplicated_lines_density`   | >3 %            |
| `new_security_hotspots_reviewed` | <100 %          |

## 14. Security

⚠️ WARNING — **2 vulnerabilidades reportadas**, Security Rating tradicional **3.0 (C)**. MQR: `software_quality_security_issues=2`, rating **3.0 (C)**. Son hallazgos del analizador pendientes de revisión humana; no se corrigieron ni se marcaron aceptados.

Reglas: `php:S5693` (límite de carga de CV) y `typescript:S2245` (generador pseudoaleatorio en sidebar). Ver detalle en §19.

## 15. Reliability

⚠️ WARNING — Métricas tradicionales: **0 Bugs**, Reliability Rating **1.0 (A)**. Métricas MQR: **3 incidencias con impacto Reliability**, rating **3.0 (C)**. No son conteos intercambiables: las reglas pueden atribuir impacto Reliability a incidencias tipadas tradicionalmente como Code Smell.

## 16. Maintainability

⚠️ WARNING — Métricas tradicionales: **3 Code Smells**, Maintainability Rating **1.0 (A)**. MQR: **1 incidencia con impacto Maintainability**, rating **1.0 (A)**. No sumar los conteos MQR para calcular Issues únicos: una incidencia puede tener más de un impacto.

## 17. Coverage

✅ PASSED — Importación real confirmada por log y API. **Coverage global = 66.5 %**, Line Coverage **66.5 %**; **4379 líneas a cubrir, 1469 sin cubrir**.

| Alcance Sonar  | Coverage   | Líneas a cubrir | Sin cubrir |
| -------------- | ---------- | --------------- | ---------- |
| `app`          | **89.6 %** | 3249            | 339        |
| `resources/js` | **0.0 %**  | 1073            | 1073       |
| `routes`       | **0.0 %**  | 57              | 57         |
| Global         | **66.5 %** | 4379            | 1469       |

⚠️ WARNING — PHP Clover incluye `app/`; frontend/rutas permanecen en Sonar sin reporte propio. Se mantuvo ese denominador histórico. La cobertura de sentencias Clover y las líneas ejecutables que calcula Sonar son medidas distintas; por ello el aproximadamente 90.0 % de Clover no sustituye a 89.6 % de `app` ni a 66.5 % global. La API no devolvió `branch_coverage`/condiciones cubiertas para esta consulta: no se inventa cobertura de ramas.

## 18. Duplicación

✅ PASSED — `duplicated_lines_density = 0.0 %`. No se cambiaron umbrales ni exclusiones de duplicación. Tamaño analizado: **19495 líneas de código** (`ncloc`), según API.

## 19. Issues

⚠️ WARNING — **5 Issues no resueltos**, todos `OPEN`, severidad tradicional **MAJOR**. Distribución: **3 CODE_SMELL, 2 VULNERABILITY, 0 BUG**. Facetas de impacto: 5 MEDIUM y 1 LOW; estos son impactos y pueden contarse varias veces por Issue.

| Regla              | Archivo/línea reportada                                            | Tipo tradicional | Hallazgo resumido                                    |
| ------------------ | ------------------------------------------------------------------ | ---------------- | ---------------------------------------------------- |
| `typescript:S8786` | `resources/js/components/experience-3d/experience-3d.test.tsx:162` | CODE_SMELL       | Regex con posible coste superlineal por backtracking |
| `typescript:S6843` | `resources/js/components/data-table.tsx:149`                       | CODE_SMELL       | Rol no interactivo en elemento interactivo           |
| `typescript:S6671` | `resources/js/components/vacancies/operational-risk-card.tsx:56`   | CODE_SMELL       | Rechazo Promise que no es Error                      |
| `php:S5693`        | `app/Http/Requests/Candidates/CandidateCvRequest.php:20`           | VULNERABILITY    | Revisar seguridad del límite de tamaño de carga      |
| `typescript:S2245` | `resources/js/components/ui/sidebar.tsx:624`                       | VULNERABILITY    | Revisar uso seguro de generador pseudoaleatorio      |

No se modificaron fuentes ni se resolvieron Issues automáticamente. Sonar analiza los `.test.tsx` dentro de `resources/js` como fuente porque se conservó el alcance histórico; `tests/` se clasifica aparte como pruebas PHP.

## 20. Security Hotspots

✅ PASSED — API de Hotspots: **0 total, 0 pendientes, 0 revisados**. La métrica porcentual `security_hotspots_reviewed` no fue devuelta; no se la presenta como 100 % por defecto.

Un **Security Hotspot no equivale automáticamente a una vulnerabilidad**. Aquí hay cero hotspots y dos vulnerabilidades reportadas: son categorías diferentes.

## 21. Complexity

⚠️ WARNING — Complejidad ciclomática **2047**; complejidad cognitiva **687**. Son agregados de la línea base, no umbrales aprobados ni medidas de rendimiento. No se aplicó refactorización.

## 22. Technical Debt

⚠️ WARNING — `sqale_index = 30` minutos estimados de remediación tradicional. La métrica MQR `software_quality_maintainability_remediation_effort = 5` minutos corresponde al impacto Maintainability. No son tiempo real trabajado ni una promesa de esfuerzo; no se suman entre sí.

## 23. Evidencias para exposición

✅ PASSED — Dashboard: [SaaS Reclutamiento Multiempresa](http://localhost:9000/dashboard?id=saas-reclutamiento-multiempresa). Navegación de exposición en [la guía](GUIA_PRESENTACION_SONARQUBE_MAC.md); operación/repetición en [README](README.md).

Evidencia local ignorada por Git:

- `storage/logs/sonarqube-scan.log`: `EXECUTION SUCCESS`, revisión e importación Clover.
- `storage/logs/sonarqube-resultados-api.json`: tarea, Gate, medidas, directorios, Issues y Hotspots saneados.
- `storage/logs/sonarqube-checks.json`: códigos/duraciones/salidas de los controles.
- `storage/logs/sonarqube-*.log`: salidas de cada control.
- `coverage.xml`: Clover de rutas relativas; original Docker en `storage/logs/sonarqube-coverage-docker.xml`.
- `.scannerwork/report-task.txt`: identificadores locales de tarea; no versionado.

No se copiaron tokens a evidencia. La autenticación local se conserva exclusivamente donde la proporcionó el usuario y en memoria de los procesos autorizados. Se preservaron sin cambios los dos reportes previos de auditoría.

### Checklist para exposición

- [x] Docker Desktop abierto y Engine accesible.
- [x] SonarQube running y `localhost:9000` accesible.
- [x] SaaS, PostgreSQL, Redis y queue healthy.
- [x] PHPUnit ejecutado; 8 omitidas explicadas.
- [x] `coverage.xml` generado y Clover validado.
- [x] PHPStan ejecutado — FAILED, 91 errores documentados.
- [x] Pint check ejecutado — FAILED, 8 problemas documentados.
- [x] TypeScript ejecutado — PASSED.
- [x] Vite Plus check ejecutado — FAILED, formato pendiente documentado.
- [x] Oxlint independiente ejecutado — FAILED por 5 warnings.
- [x] Vitest ejecutado — 42 PASSED.
- [x] SonarScanner SUCCESS.
- [x] Análisis procesado SUCCESS para la key correcta.
- [x] Quality Gate consultado — OK, sin condiciones evaluadas en la respuesta inicial.
- [x] Issues, Hotspots y Measures preparados con cifras reales.
- [x] Coverage importada y visible por API: 66.5 % global.
- [x] Token no visible en configuración, evidencia ni Git diff.
- [ ] Revisar visualmente en el navegador autenticado las pantallas preparadas.
- [ ] Dejar la terminal de exposición limpia y con los logs seleccionados.

Marcar «ejecutado» no significa «aprobado». Cypress no se incluye como aprobado: **NO EJECUTADO** hoy. El gate OK tampoco oculta las deudas actuales de PHPStan, estilo y cobertura frontend.
