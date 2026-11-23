# Resultados V2 preliminares – SonarQube

## 1. Alcance y conclusión

Práctica local del 20/10/2026, macOS Apple Silicon, rama `chore/sonarqube-macos-setup`.
V1 se documentó y validó **antes de modificar código**. V2 corrigió los cinco hallazgos seleccionados y se analizó en la misma instancia y Project Key, sin cambiar reglas, exclusiones, perfiles ni Quality Gate.

**Resultado del análisis V2 inicial: 5/5 Issues originales FIXED, 0 Issues abiertos, pero Quality Gate ERROR.** La condición incumplida era cobertura de código nuevo: **1.7 % < 80 %**. La cobertura global bajó de 66.5 % a **65.6 %**. No se ocultó ese resultado ni se modificó el alcance en aquel análisis.

Este reporte es preliminar porque faltan las capturas manuales V2 y su posterior informe comparativo. No se generó Word V2. No se afirma preparación para producción.

**Continuación de cobertura (20/10/2026, 21:00–21:02 America/Lima):** API consultada nuevamente; Gate ERROR y 1.7 % confirmados. El diagnóstico detallado de la sección 15 identifica **58 líneas de tests TS clasificadas como fuentes entre las 60 nuevas a cubrir**. Se requiere autorización explícita para corregir su clasificación antes de intentar cerrar el Gate mediante cobertura legítima. No se instaló un provider, no se cambiaron propiedades Sonar y no se lanzó otro análisis en esta continuación.

**Estado vigente después de la autorización y reclasificación (20/10/2026, 21:07–21:08 America/Lima): Quality Gate OK, New Code Coverage 50.0 %, 0 Issues y cinco originales FIXED.** Ocho tests TS se clasifican como UTS. Quedan 11 líneas nuevas productivas, de las cuales 2 son elegibles y 1 tiene cobertura importada. El Gate ignora la condición de cobertura por cambios pequeños (`ignoredConditions=true`, ajuste heredado existente); **NO se alcanzó 80 %**. Coverage global 69.5 %, app/ 89.6 %. LCOV sigue pendiente para `sidebar.tsx:621`. Detalles en sección 16; no se modificó código ni se instaló nada.

## 2. Congelación de V1

- [Markdown V1](../v1/REPORTE_EVIDENCIAS_V1_SONARQUBE.md): conservado íntegro.
- 30 PNG V1: mismos nombres, tamaños y SHA-256 anteriores; no se editaron, renombraron ni copiaron a V2.
- [Word V1](../v1/INFORME_EVIDENCIAS_V1_SONARQUBE.docx): creado adicionalmente, **47 páginas verificadas en Microsoft Word**, 30 imágenes originales embebidas, 30 pies de figura numerados. Revisión visual completa, sin conversión a PDF.
- Se cotejaron hashes de las imágenes embebidas con los PNG originales. Se mantuvo su proporción; cada captura dispone de página horizontal propia y explicación.
- SHA-256 del Markdown V1: `4b313ee461095bd82139611aa6c98217af36214d8b41cee2281b032a1a81de54`.
- SHA-256 del Word V1: `4ac17c04324703a8573994533c2fe82ac31b041e7de0aa72a289f4c9f5e2ddd0`.

Se preservaron los dos reportes de auditoría anteriores, `RESULTADOS_SONARQUBE_MAC.md`, `README.md` y `GUIA_PRESENTACION_SONARQUBE_MAC.md`. Sus cifras siguen describiendo V1, no se reescriben como V2.

## 3. Entorno e identidad del análisis

| Dato | Verificado |
|---|---|
| Entorno | macOS Apple Silicon / arm64; Docker Engine aarch64 |
| Docker Engine | 29.7.2 |
| Servicios | app, postgres, redis y queue healthy al inicio; `/health`: database y redis OK |
| SonarQube | Community 26.10.0.133078, estado UP, instalación existente preservada |
| Scanner | CLI 8.1.0.6389; motor Java 21.0.12.1 Eclipse Adoptium |
| PHP / PCOV | PHP 8.4.25; PCOV 1.0.12, desactivado por defecto |
| Node Docker / PHPUnit | Node 22.23.2; PHPUnit 12.5.35 |
| Project Key | `saas-reclutamiento-multiempresa` |
| Project Name / versión | SaaS Reclutamiento Multiempresa / 1.1, sin cambio |
| URL | `http://localhost:9000` |
| Revisión SCM | `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6` |
| Análisis V1 | `0cd5eb83-5a78-42ae-8289-78af6dc0cf90`, 20/10/2026 16:01:25 America/Lima |
| Análisis V2 | `fad88726-7762-4095-bbe0-7239f78be6ac`, 20/10/2026 20:35:44 America/Lima |
| Tarea V2 | `37e3acef-aa70-4fdc-98cb-3d5808ca573f` |
| Procesamiento | SUCCESS, finalizado 20:35:55 America/Lima, 2050 ms |

**V2 analiza cambios locales sin commit.** El mismo SHA que V1 identifica el commit base, no significa que el contenido analizado sea idéntico. Hay 9 archivos sin blame completo por cambios locales/nuevos; esta advertencia limita atribución SCM y debe mencionarse en la exposición. No se hizo commit para eliminarla.

## 4. Cambios controlados y trazabilidad

No se añadieron dependencias al SaaS ni se modificó configuración Sonar/Docker en esta etapa.

| Regla / contrato | Archivo de implementación | Cambio mínimo | Prueba / alcance |
|---|---|---|---|
| php:S5693 · RF-09 / A-12 | `app/Http/Requests/Candidates/CandidateCvRequest.php` | Añade un máximo literal de 5120 KB además del límite configurable existente; la configuración puede restringir, no ampliar, el máximo aprobado de 5 MB. Conserva PDF, MIME, autorización y almacenamiento privado. | `CandidateProfileTest`: borde exacto, configuración excesiva y límite menor; regresiones de autorización y acceso cross-tenant existentes. |
| typescript:S2245 · placeholder UI | `resources/js/components/ui/sidebar.tsx` | Sustituye Math.random por ancho decorativo fijo de 70 %, dentro del rango anterior 50–89 %. No había uso criptográfico: solo apariencia del skeleton. | Nuevo `sidebar-skeleton.test.tsx`: determinismo SSR, icono opcional y atributos. |
| typescript:S6843 · semántica de tabla | `resources/js/components/data-table.tsx` | Retira únicamente `role="cell"` redundante de `td`; conserva tabla, filas, encabezados, `headers`, clases, enlaces y data-cy. No convierte la tabla en un grid. | `data-table.test.tsx`: celdas nativas, relaciones de encabezados, enlace de acción y estructura; 8 pruebas. |
| typescript:S8786 · test decorativo ADR-003 | `resources/js/components/experience-3d/experience-3d.test.tsx` | Sustituye la regex para quitar etiquetas por split/indexOf/slice/join, sobre el markup controlado del póster. No es un sanitizador HTML general. | Se conserva la aserción de texto vacío y número de hojas; 13 pruebas del archivo. No cambia producción 3D. |
| typescript:S6671 · RF-29 experimental | `resources/js/components/vacancies/operational-risk-card.tsx` | Rechaza con `new Error` cuyo mensaje conserva el status HTTP, en lugar de rechazar con un número. Catch y cancelación mantienen la degradación previa. | Nuevo `operational-risk-card.test.tsx`: HTTP fallido, respuesta correcta y cancelación; fetch simulado, sin red real. |

La restricción de 5 MB ya estaba aprobada en [A-12](../../../assumptions.md); no se inventó ni amplió un límite de negocio. PHP limita upload a 6M y post a 8M, según la configuración existente: no se cambió en V2. Se observó un fallo real del test al permitir 5121 KB cuando la configuración se subía a 8192 KB, antes de agregar el tope fijo.

Para S6843, [W3C ARIA in HTML: td](https://www.w3.org/TR/html-aria/#el-td) define el rol implícito cell bajo table y desaconseja repetirlo. La tabla no tenía handlers ni foco añadido en td: el hallazgo no prueba por sí solo una barrera explotable. La modificación elimina la redundancia sin quitar los enlaces nativos ni sus encabezados. **Pendiente revisión manual con lector de pantalla y teclado en móvil/escritorio**: las pruebas SSR no equivalen a una auditoría de accesibilidad del navegador.

Las reglas de [SonarSource S5693](https://rules.sonarsource.com/php/RSPEC-5693/) y la descripción de la regla instalada se consultaron para contrastar el límite; no se cambió el umbral de Sonar. RF-01 a RF-27 conservan significado, RF-23 mantiene decisión humana, RF-29 sigue experimental/informativa; sin modificaciones a Policies, organization_id, auditoría, rutas o base principal.

## 5. Validación por hallazgo

Los tests nuevos se justificaron por el cambio de límite/contrato de error o por la estabilidad/semántica de la UI. No se relajaron pruebas para aceptar fallos funcionales.

| Issue | RED observado antes del cambio | GREEN focalizado después |
|---|---|---|
| php:S5693 | 1 failed / 2 passed, 6 assertions: 5121 KB se aceptaba con configuración 8192. | 9 passed, 35 assertions, 0.39 s en CandidateProfileTest; Pint focalizado: 2 archivos PASS. |
| typescript:S2245 | 1 failed / 1 passed: el skeleton no producía ancho determinista. | 2 passed; TypeScript exit 0. |
| typescript:S6843 | 1 failed / 7 passed: td sobrescribía su rol nativo. | 8 passed; TypeScript exit 0. Se adaptó la aserción del rol explícito al contrato nativo, manteniendo validación de headers y enlaces. |
| typescript:S8786 | Sin RED nuevo: refactor de una aserción existente, no nueva funcionalidad. | 13 passed en el archivo de experiencia 3D, conservando las aserciones originales. |
| typescript:S6671 | 1 failed / 2 passed: Promise.reject recibía 503 en vez de Error. | 3 passed; TypeScript exit 0. El efecto se prueba con hooks simulados, no como test de navegador. |

## 6. Regresión general V2

| Herramienta | Resultado real de esta sesión | Código de salida / observación |
|---|---|---|
| PHPUnit baseline | ✅ PASSED: **414 passed, 8 skipped, 0 failed, 1506 assertions**, total 422; 8.55 s | 0; base forzada `reclutamiento_testing`, config cache ausente antes de ejecutar |
| PHPUnit + PCOV | ✅ PASSED: 422 tests, 8 skipped, 1506 assertions; 11.576 s; Clover generado | 0; 414 no omitidos, sin fallos |
| TypeScript `npm run types:check` | ✅ PASSED | 0; tsc --noEmit |
| Vitest completo | ✅ PASSED: **48/48, 8 archivos**, 762 ms | 0; V1 tenía 42 pruebas y 6 archivos |
| Build `npm run build` | ✅ PASSED: 2375 módulos, build 2.32 s | 0; warning opcional fontaine, no se instaló |
| PHPStan / Larastan `composer types:check` | ❌ FAILED: **91 errores** | 1; deuda histórica, no se corrigió masivamente |
| Pint `vendor/bin/pint --test` | ❌ FAILED: **8 problemas en 256 archivos** | 1; no se ejecutó Pint correctivo |
| Vite Plus `npm run check` | ❌ FAILED: **298 archivos con formato pendiente** | 1, ejecución antes de crear los documentos V2; V1 documentó 297, el conjunto documental cambió |
| Oxlint `vp check --no-fmt` | ⚠️ WARNING: **0 errors, 5 warnings, 147 archivos** | 1 por denyWarnings; mismos 5 hallazgos Cypress históricos |
| Oxlint focalizado | ✅ PASSED: 6 archivos editados/añadidos revisados, sin warnings ni errores | 0; carpeta UI se mantiene excluida por configuración histórica |
| Nuevos tests + data-table.test | ✅ PASSED: 3 archivos con formato y lint correctos | 0; solo ajustes manuales del formato recién introducido |
| Cypress | ⏭️ NO EJECUTADO | `.env.e2e` ausente; no se generaron tokens ni se reinició entorno E2E |

Los 8 fallos Pint siguen en `app/Models/Vacancy.php`, `app/Providers/AppServiceProvider.php`, `app/Services/Assessments/AssessmentResultRecorder.php`, `bootstrap/app.php`, `database/seeders/DemoSeeder.php`, `routes/web.php`, `tests/Feature/Audit/AuditLoggerTest.php` y `tests/Feature/Tenancy/CrossTenantAccessTest.php`. No están en los archivos PHP cambiados para Sonar.

El total de formato no equivale a un número de defectos funcionales, ni los errores PHPStan/Pint se suman a los Issues Sonar. El check global corta en formato; por eso se consultó Oxlint por separado. No se ejecutó check:fix ni formatter correctivo global.

## 7. Clover e importación de cobertura

Se siguió el procedimiento ya verificado del [README original](../../README.md), sin modificarlo:

```sh
docker compose exec -T app php -d pcov.enabled=1 vendor/bin/phpunit --coverage-clover coverage.xml --colors=never
```

Después se ejecutó exactamente la normalización DOM documentada: rutas de file/@name desde `/var/www/html/app/...` a `app/...`, validando que cada archivo exista. Resultado: **151 archivos, 2777 sentencias, 2499 cubiertas**. El XML tiene raíz coverage y project Clover, no es JUnit.

Original Docker guardado en `storage/logs/sonarqube-coverage-docker.xml`; copia del Clover anterior preservada en `storage/logs/sonarqube-v1-coverage-before-v2.xml`. El artefacto raíz y logs siguen ignorados por Git.

El scanner registró `Importing .../coverage.xml` y la API devuelve cobertura de app **89.6 %**. La importación sí funcionó; Sonar no generó cobertura. La falta de un reporte de ejecución PHPUnit (`sonar.php.tests.reportPath`) es una información separada, no un fallo de importación Clover.

| Alcance | V1 a cubrir / sin cubrir | V2 a cubrir / sin cubrir | V1 Coverage | V2 Coverage |
|---|---|---|---|---|
| Global | 4379 / 1469 | 4434 / 1524 | 66.5 % | **65.6 %** |
| app/ | 3249 / 339 | 3249 / 339 | 89.6 % | **89.6 %** |
| resources/js | 1073 / 1073 | 1128 / 1128 | 0.0 % | **0.0 %** |
| routes | 57 / 57 | 57 / 57 | 0.0 % | **0.0 %** |

Se conserva el alcance `app,resources/js,routes`, con `sonar.tests=tests`. Por tanto los `.test.tsx` dentro de resources/js siguen clasificados como fuentes, como en V1. Agregar pruebas frontend incrementó en 55 las líneas globales a cubrir, sin LCOV: las líneas cubiertas globales permanecen 2910. Esto explica la disminución de **0.9 puntos porcentuales**, no una pérdida de cobertura PHP. No se excluyeron tests o código propio para ocultarlo.

## 8. Scanner y procesamiento

- ✅ Scanner exit 0, `EXECUTION SUCCESS`, tiempo total 11.123 s.
- ✅ Tarea CE SUCCESS, Project Key correcto, análisis V2 distinto del V1.
- ✅ Historial conserva los dos análisis.
- Log local sin credencial: `storage/logs/sonarqube-v2-scan.log`.
- Instantánea V1 obtenida antes de enviar V2: `storage/logs/sonarqube-v1-api-before-v2.json`.
- Resultados API V2: `storage/logs/sonarqube-v2-api.json` y `storage/logs/sonarqube-v2-new-code.json`.
- Avisos no fatales: falta de blame para 9 archivos locales y advertencia de reflexión de Java/Gson del launcher. No se cambiaron flags de Java para ocultarlos.

La credencial se leyó únicamente en memoria desde el archivo privado autorizado, se pasó por entorno al proceso scanner y no se incluyó en argumentos, documentación ni logs. No se reutilizó historial. El entorno del proceso auxiliar se limpió al finalizar.

## 9. Quality Gate: mejora de Issues, pero Gate fallido

**Sonar way: ERROR.** V1 era OK con `conditions: []`; V2 sí evalúa condiciones de código nuevo. La API indica período PREVIOUS_VERSION con referencia al análisis V1, manteniendo projectVersion 1.1.

| Condición realmente devuelta en V2 | Actual | Umbral | Estado |
|---|---|---|---|
| new_coverage | 1.7 % | >= 80 % | ERROR |
| new_duplicated_lines_density | 0.0 % | <= 3 % | OK |
| new_violations | 0 | 0 | OK |

La API reporta **60 líneas nuevas a cubrir y 59 sin cubrir**: 1/60 = 1.7 % redondeado. Desglose verificado:

| Archivo | Nuevas a cubrir | Nuevas sin cubrir |
|---|---|---|
| CandidateCvRequest.php | 1 | 0 |
| data-table.test.tsx | 11 | 11 |
| experience-3d.test.tsx | 1 | 1 |
| operational-risk-card.test.tsx | 35 | 35 |
| sidebar-skeleton.test.tsx | 11 | 11 |
| sidebar.tsx | 1 | 1 |

Sonar identifica 178 líneas nuevas en total, distintas de las 60 ejecutables a cubrir. El PHP nuevo tiene 100 %; TypeScript no aporta reporte. Se deja constancia del Gate fallido: **cero Issues no equivale a Gate aprobado**. La condición de hotspots revisados no aparece entre las condiciones devueltas; no se inventa una evaluación al 100 % cuando el total es cero.

Una futura fase podría instrumentar cobertura frontend real y revisar explícitamente la clasificación de tests con una nueva línea base comparable. Eso **no se implementó** aquí. No se propone cambiar el Gate para que esta versión pase artificialmente.

## 10. Comparación Antes vs Después

Valores obtenidos de la API instalada; ratings numéricos 1=A, 3=C.

| Métrica | V1 Antes | V2 Después | Variación |
|---|---|---|---|
| Quality Gate | OK, sin condiciones evaluadas | ERROR, new_coverage | No aprobado en V2; contextos distintos |
| Security tradicional | C | A | Mejora |
| Reliability tradicional | A | A | Sin cambio |
| Maintainability tradicional | A | A | Sin cambio |
| Security MQR | 2 Issues / C | 0 / A | -2 |
| Reliability MQR | 3 Issues / C | 0 / A | -3 |
| Maintainability MQR | 1 Issue / A | 0 / A | -1 impacto, no un Issue adicional |
| Coverage global | 66.5 % | 65.6 % | **-0.9 pp** |
| Coverage app/ | 89.6 % | 89.6 % | 0.0 pp |
| Coverage resources/js | 0.0 % | 0.0 % | Sin reporte LCOV |
| Coverage routes | 0.0 % | 0.0 % | Sin reporte importado |
| Duplicación | 0.0 % | 0.0 % | 0.0 pp |
| Issues abiertos | 5 | 0 | -5 |
| Vulnerabilities | 2 | 0 | -2 |
| Code Smells | 3 | 0 | -3 |
| Bugs | 0 | 0 | 0 |
| Security Hotspots | 0 | 0 | 0 |
| Cyclomatic Complexity | 2047 | 2067 | **+20** |
| Cognitive Complexity | 687 | 689 | **+2** |
| Technical Debt tradicional | 30 min | 0 min | -30 min estimados |
| Deuda Maintainability MQR | 5 min | 0 min | -5 min estimados |
| Lines of Code (ncloc) | 19495 | 19597 | **+102** |

La complejidad agregada aumentó: se añadió código de pruebas dentro del alcance de fuentes. No se presenta como una mejora ni como prueba de mayor complejidad del negocio. Los minutos de deuda son estimaciones Sonar, no tiempo real invertido.

Security Hotspot no equivale automáticamente a Vulnerability. La búsqueda V2 devuelve 0 hotspots; pendientes 0 y revisados 0, sin atribuir un porcentaje de revisión no devuelto.

## 11. Verificación explícita de los cinco Issues

Se consultaron sus IDs originales, no solo el total global. Todos siguen recuperables en historial, con status CLOSED, issueStatus FIXED y resolution FIXED. No se cerraron manualmente ni se marcaron False Positive/Accepted.

| Regla | ID original | V1 | V2 | Clasificación solicitada |
|---|---|---|---|---|
| php:S5693 | b5c887a2-2ac3-439b-8a22-c3a9023d5c3e | OPEN | CLOSED / FIXED | RESUELTO |
| typescript:S2245 | 6fce6299-f9af-4975-a5b1-5b7481b15809 | OPEN | CLOSED / FIXED | RESUELTO |
| typescript:S6843 | 1ddb8eca-b699-4e59-a7e8-a4ffc0433ce2 | OPEN | CLOSED / FIXED | RESUELTO |
| typescript:S8786 | 2fd88a22-9d7b-4851-a848-ead901106d67 | OPEN | CLOSED / FIXED | RESUELTO |
| typescript:S6671 | 0911fd6d-79b0-48b8-a5e8-edb9e14bf243 | OPEN | CLOSED / FIXED | RESUELTO |

## 12. Pendientes y límites

1. Tomar manualmente las capturas V2 de [README_CAPTURAS_V2.md](README_CAPTURAS_V2.md), incluyendo el Gate ERROR y la condición de cobertura 1.7 %. No repetir un análisis antes de capturar esta versión.
2. Revisar teclado/lector de pantalla de DataTable en móvil y escritorio. SSR y TypeScript no certifican accesibilidad del navegador.
3. Cobertura frontend real y tratamiento formal de tests como tests: propuesta posterior, sin cambiar el alcance en esta comparación.
4. Deuda histórica: 91 PHPStan, 8 Pint, formato global y 5 warnings Oxlint. Requiere autorización separada para corregirse.
5. Cypress aislado y reproducible queda pendiente; no se toca la base `reclutamiento`.
6. Los cambios locales requieren revisión humana; commit/publicación NO autorizados. El warning SCM persistirá mientras no exista blame de esos cambios.

## 13. Archivos y preservación

Modificados en esta etapa: CandidateCvRequest.php, CandidateProfileTest.php, data-table.tsx, data-table.test.tsx, experience-3d.test.tsx, ui/sidebar.tsx, vacancies/operational-risk-card.tsx y `docs/PROGRESS.md` (registro de trazabilidad).

Nuevos: sidebar-skeleton.test.tsx, vacancies/operational-risk-card.test.tsx, Word V1 y los dos Markdown de esta carpeta V2. Artefactos locales ignorados: Clover y evidencias API/logs citadas.

`.gitignore`, Dockerfile y php.ini **ya estaban modificados antes de esta tarea** por la preparación anterior y se preservaron. `sonar-project.properties`, reportes de auditoría y documentación V1 también eran WIP previo. No se mezclan esos cambios anteriores con las correcciones V2.

No hubo cambios a migraciones, Policies, dependencias del SaaS, secretos, base principal, contenedores ni volúmenes Sonar. Para crear el DOCX se utilizó python-docx 1.2.0 exclusivamente en un entorno virtual temporal fuera del repositorio; no se añadió al proyecto. No se ejecutó git add, commit, push, merge ni limpieza destructiva. La validación final no implica árbol limpio porque el usuario pidió revisar todo sin commit.

Validación final: **41 archivos protegidos cotejados por SHA-256, 0 alteraciones**, enlaces locales sin roturas, patrones de credenciales no encontrados en las líneas añadidas del diff, tests nuevos, documentos V2, Clover y log del scanner. DOCX abre correctamente, sus 30 imágenes coinciden con los originales y no son vínculos externos. `coverage.xml`, `.scannerwork` y la credencial privada no están rastreados. `git diff --check` sin errores. Segunda comprobación final: Vitest **48/48, 8 archivos, 677 ms** y TypeScript exit 0. No se repitió el scanner porque desde su ejecución solo cambió documentación excluida del análisis.

## 14. Checklist de entrega preliminar

- [x] V1: 30 imágenes, Markdown y Word adicional validados antes de cambiar código.
- [x] Misma rama, Project Key, servidor, alcance y versión de análisis.
- [x] Correcciones pequeñas con pruebas focalizadas y regresión general.
- [x] Clover válido, rutas normalizadas y cobertura importada.
- [x] Scanner EXECUTION SUCCESS y tarea CE SUCCESS.
- [x] Estados de los 5 IDs originales comprobados como FIXED.
- [x] Gate ERROR y empeoramiento de cobertura/complexity documentados.
- [x] Deuda PHPStan/Pint/formato preservada sin corrección masiva.
- [ ] Capturas manuales V2.
- [ ] Verificación manual de accesibilidad de DataTable.
- [ ] Informe Word comparativo V2, después de recibir capturas.

**Siguiente paso de la entrega inicial:** tomar las capturas V2 manualmente. Esta indicación queda suspendida por el encargo posterior de estabilizar la cobertura; las capturas siguen pendientes hasta resolver la sección 15. No se continúa con deuda masiva.

## 15. Continuación: diagnóstico real de New Code Coverage

### 15.1. Evidencia y período vigente

Consulta de solo lectura el **20/10/2026 a las 21:00:36 y 21:01:51 America/Lima** (21/10/2026 02:00:36 y 02:01:51 UTC). Servidor 26.10.0.133078 UP; rama obligatoria conservada. Los servicios app, postgres, redis y queue están healthy. No se volvió a ejecutar scanner.

Se consultaron las API reales:

- `/api/new_code_periods/show?project=saas-reclutamiento-multiempresa`
- `/api/project_analyses/search?project=saas-reclutamiento-multiempresa&ps=2`
- `/api/qualitygates/project_status?projectKey=saas-reclutamiento-multiempresa`
- `/api/measures/component` y `/api/measures/component_tree`, con métricas de código nuevo y qualifiers FIL/UTS.
- `/api/sources/lines`, para contrastar `isNew` y `lineHits` línea por línea.
- `/api/issues/search`, por los cinco IDs originales y por Issues sin resolver.

Instantáneas locales ignoradas, sin credenciales: `storage/logs/sonarqube-v2-coverage-diagnosis.json` y `storage/logs/sonarqube-v2-coverage-context.json`. La credencial privada solo se leyó para autenticar peticiones, sin imprimirla ni guardarla en estas evidencias.

Definición: **PREVIOUS_VERSION, inherited=true**. El Gate devuelve fecha de referencia **2026-10-20T21:01:25+0000**, coincidente con V1 (`0cd5eb83-5a78-42ae-8289-78af6dc0cf90`). El último análisis sigue siendo V2 `fad88726-7762-4095-bbe0-7239f78be6ac`, versión 1.1; no se alteró el período, la versión ni la referencia. Ambos análisis se realizaron sobre WIP con el mismo SHA base; esto limita atribución SCM, pero no invalida los conteos de líneas devueltos por la API.

| Medida devuelta por Sonar | Valor |
|---|---|
| Líneas nuevas totales (`new_lines`) | 178 |
| Nuevas líneas a cubrir (`new_lines_to_cover`) | 60 |
| Nuevas líneas sin cubrir (`new_uncovered_lines`) | 59 |
| Nuevas líneas cubiertas, por diferencia | 1 |
| Nuevas condiciones a cubrir / sin cubrir | 0 / 0 |
| New Code Coverage | **1.7 %**, redondeo de 1/60 |
| Quality Gate | **ERROR**, exclusivamente condición de cobertura <80 % |

No se confunden las 178 líneas nuevas totales con las 60 elegibles para cobertura. Tampoco se interpreta `lineHits=0` como prueba de que un test jamás se ejecutó: significa que este análisis no tiene cobertura importada para esa línea.

### 15.2. Archivos nuevos/modificados y distribución PHP/TS

Los nombres siguientes son relativos a la raíz. «Cubiertas/sin cubrir» corresponde únicamente a líneas nuevas elegibles de la API, no a todas las líneas físicas.

| Archivo | Lenguaje / clasificación Sonar | Líneas nuevas totales | Nuevas a cubrir | Cubiertas | Sin cubrir | Reporte disponible/importado |
|---|---|---:|---:|---:|---:|---|
| `app/Http/Requests/Candidates/CandidateCvRequest.php` | PHP / FIL (fuente) | 2 | 1 | 1 | 0 | Clover PHP importado; línea 21 con lineHits=1 |
| `resources/js/components/ui/sidebar.tsx` | TSX / FIL (fuente) | 2 | 1 | 0 | 1 | Sin LCOV; línea 621 |
| `resources/js/components/data-table.tsx` | TSX / FIL (fuente) | 4 | 0 | 0 | 0 | Sin LCOV; líneas nuevas 14, 16–18 no elegibles en este análisis; retirada de un atributo no añade línea a cubrir |
| `resources/js/components/vacancies/operational-risk-card.tsx` | TSX / FIL (fuente) | 3 | 0 | 0 | 0 | Sin LCOV; líneas 56–58 marcadas nuevas pero sin lineHits/denominador nuevo en este análisis |
| `resources/js/components/data-table.test.tsx` | TSX **test clasificado FIL** | 18 | 11 | 0 | 11 | Sin LCOV; assertions/registro de tests contados como fuente |
| `resources/js/components/experience-3d/experience-3d.test.tsx` | TSX **test clasificado FIL** | 5 | 1 | 0 | 1 | Sin LCOV; línea 162 |
| `resources/js/components/sidebar-skeleton.test.tsx` | TSX **test clasificado FIL** | 24 | 11 | 0 | 11 | Sin LCOV; assertions/registro de tests contados como fuente |
| `resources/js/components/vacancies/operational-risk-card.test.tsx` | TSX **test clasificado FIL** | 84 | 35 | 0 | 35 | Sin LCOV; mocks/assertions contados como fuente |
| `tests/Feature/Candidates/CandidateProfileTest.php` | PHP / UTS (**test**) | 36 | No aplica | No aplica | No aplica | Correctamente fuera del denominador productivo; su ejecución aporta a Clover de app/ |
| **Total** | Fuentes y tests | **178** | **60** | **1** | **59** | No hay líneas nuevas elegibles en routes/ |

Distribución del problema:

- **A. PHP nuevo sin pruebas:** 0 líneas nuevas elegibles sin cubrir; el cambio de validación ya tiene pruebas de límites y su línea nueva está cubierta.
- **B. React/TypeScript sin reporte importado:** 59 sin cubrir; **58 están en tests**, 1 en producción (`sidebar.tsx:621`). No equivale a 59 líneas productivas sin pruebas.
- **C. routes/:** 0 líneas nuevas a cubrir; mantiene 57 líneas globales sin cobertura, pero no causa este 1.7 % nuevo.
- **D. New Code:** usa la referencia V1 heredada; no es un umbral modificado ni un período inventado. El problema principal es la combinación de clasificación histórica y ausencia de LCOV, no evidencia de que haga falta bajar el umbral o reiniciar la referencia.

Las pruebas previas de SSR y del efecto asíncrono sí ejercitan comportamiento de los componentes, según las ejecuciones de la sección 6; su éxito no es por sí mismo un reporte de cobertura importable. Hasta generar LCOV no se atribuyen porcentajes de ejecución frontend.

### 15.3. Lista exacta de las 59 líneas nuevas sin cobertura importada

Verificada con `isNew=true` y `lineHits=0` en `/api/sources/lines`, concordante con las métricas por archivo:

| Archivo | Líneas nuevas sin cubrir | Cantidad |
|---|---|---:|
| `resources/js/components/data-table.test.tsx` | 51, 53, 55, 56, 57, 58, 59, 61, 66, 67, 73 | 11 |
| `resources/js/components/experience-3d/experience-3d.test.tsx` | 162 | 1 |
| `resources/js/components/sidebar-skeleton.test.tsx` | 5, 6, 7, 8, 10, 11, 12, 15, 16, 20, 21 | 11 |
| `resources/js/components/vacancies/operational-risk-card.test.tsx` | 5, 11, 14, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 36, 37, 39, 42, 43, 44, 49, 50, 51, 59, 60, 62, 65, 68, 69, 74, 75, 76, 78, 80, 81 | 35 |
| `resources/js/components/ui/sidebar.tsx` | 621 | 1 |

La línea nueva cubierta es `app/Http/Requests/Candidates/CandidateCvRequest.php:21`. Las líneas sin `lineHits` no se etiquetan como «cubiertas» o «sin cubrir»: no forman parte de las 60 elegibles devueltas.

### 15.4. Soporte frontend AS-IS y solución propuesta TO-BE

Verificado en package.json, package-lock.json, pnpm-workspace.yaml, vite.config.ts y dependencias dentro del contenedor:

- Package manager utilizado: **npm**, con package-lock.json. La presencia de pnpm-workspace.yaml no sustituye ese lock ni autoriza cambiar de gestor.
- Vite Plus **0.3.0**, Vitest **4.1.11** instalado como dependencia de Vite Plus; no se actualizaron a las versiones de la documentación web actual.
- No están instalados `@vitest/coverage-v8` ni `@vitest/coverage-istanbul`; las entradas del lock son **peerDependencies opcionales**, no paquetes instalados. Vite Plus no trae un provider de cobertura en sus dependencias instaladas.
- `vp test --help --coverage` devuelve soporte para `--coverage.provider`, `--coverage.reporter`, `--coverage.reportsDirectory` e `--coverage.include`. No se ejecutó un comando que pudiera ofrecer instalación automática.
- El código instalado de Vitest, `node_modules/vitest/dist/chunks/coverage.DM_a_rWm.js`, añade `resolved.include` a `resolved.coverage.exclude` como exclusión fija de los archivos de prueba. No se intentó instrumentarlos como producción ni anular esa protección.
- La [documentación Vitest sobre providers](https://vitest.dev/guide/coverage.html) confirma que V8 es opcional; [reporters](https://vitest.dev/config/coverage.html#coverage-reporter) admite LCOV. La versión del provider debe alinearse con el Vitest **4.1.11 realmente instalado**, no con el «latest».
- La [documentación SonarQube Community Build de JS/TS](https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/test-coverage/javascript-typescript-test-coverage) confirma `sonar.javascript.lcov.reportPaths` para ambos lenguajes. No se añadió esa propiedad sin tener un reporte real.

**TO-BE, no ejecutado:** revisar origen/licencia/integridad y compatibilidad de `@vitest/coverage-v8@4.1.11`, añadirlo como devDependency fija con npm si procede, configurar cobertura real sobre el frontend productivo sin clasificar tests como producción, generar LCOV y añadir únicamente su ruta real a la propiedad JS/TS. Ejecutar las pruebas existentes antes de decidir qué pruebas adicionales hacen falta. No se justifica agregar pruebas PHP solo para aumentar una métrica cuya línea PHP nueva ya está cubierta.

### 15.5. Conflicto de instrucciones y checkpoint necesario

El encargo prohíbe cambiar `sonar.sources`, `sonar.tests` y `sonar.test.inclusions` para ocultar el problema, y a la vez exige no incluir tests como código productivo. **El estado actual ya los clasifica como productivos:** `sonar.sources=app,resources/js,routes`, `sonar.tests=tests`, `sonar.test.inclusions=tests/**`. No se puede corregir esa clasificación con solo añadir la propiedad LCOV.

Con las 60 líneas y 0 condiciones actualmente contabilizadas, aun importando cobertura de la línea productiva TS que falta, serían **2/60 = 3.3 %**, si se mantiene ese denominador. No es una predicción de un scanner futuro: LCOV puede cambiar el detalle de líneas/condiciones. Sí demuestra por qué no corresponde prometer el 80 % conservando 58 líneas de tests exigidas como producción y sin instrumentarlas como tal.

La [distinción oficial de fuentes y tests](https://docs.sonarsource.com/sonarqube-community-build/project-administration/adjusting-analysis/setting-analysis-scope/setting-initial-scope.md) evita que las métricas productivas incluyan tests. Clasificarlos correctamente **no sería excluir código productivo**, pero sí cambiaría la configuración de alcance respecto a V1 y requiere autorización explícita antes de implementarse. También debe documentarse ese cambio metodológico en la comparación; no atribuir la mejora de reclasificación a pruebas nuevas.

**Decisión pendiente del usuario:** autorizar la clasificación de los `.test.tsx` de resources/js como tests Sonar, conservando `sonar.sources` y todo el código productivo, mediante un ajuste mínimo de `sonar.tests`/`sonar.test.inclusions`. No se propone `sonar.coverage.exclusions`, rebajar Gate, cambiar período o versión, mover tests para esconderlos, ni cerrar Issues manualmente.

### 15.6. Estado al detener esta continuación

| Elemento | Resultado |
|---|---|
| Nuevas pruebas añadidas en esta continuación | **0**, pendiente de resolver clasificación y medir LCOV |
| Coverage PHP app/ | **89.6 %**, confirmado otra vez por API |
| Coverage frontend importada | **0.0 %** en Sonar; LCOV aún no disponible |
| New Code Coverage / Gate | **1.7 % / ERROR**, sin maquillaje |
| Coverage global | **65.6 %** |
| Issues / Vulnerabilities / Code Smells / Bugs / Hotspots | **0 / 0 / 0 / 0 / 0**, nueva consulta API |
| Duplicación | **0.0 %** |
| Cinco Issues originales | **5/5 CLOSED / FIXED**, comprobados de nuevo por ID |
| PHPUnit / TypeScript / Vitest / Build | **NO REEJECUTADOS en esta continuación**; últimos resultados verificados siguen en sección 6 (414 passed, 8 skipped, 0 failed, 1506 assertions; TypeScript PASS; 48/48 Vitest; build PASS) |
| Scanner / PCOV / Clover / LCOV | No se ejecutó scanner ni se regeneró cobertura; se conserva la V2 actual |
| Archivos modificados en esta continuación | Este reporte y `docs/PROGRESS.md`, únicamente documentación; JSON de diagnóstico ignorados |
| V1 y correcciones V2 | Preservadas; sin cambios productivos, configuración ni dependencias |

No se realizaron suites generales porque no se cambió código ni configuración y existe una decisión de alcance previa indispensable. Se evita repetir análisis sin resolver su causa. Las capturas V2 finales y el informe comparativo continúan pendientes de estabilizar la metodología y el Gate. Sin git add, commit, push o merge.

## 16. Reclasificación de tests autorizada y nuevo análisis

### 16.1. Cambio mínimo aplicado

El usuario autorizó explícitamente clasificar tests TypeScript como TESTS, manteniendo código productivo, Gate, umbral, evidencias y correcciones. Se cambiaron **solo dos propiedades** de `sonar-project.properties`, además de comentarios explicativos:

```diff
-sonar.tests=tests
-sonar.test.inclusions=tests/**
+sonar.tests=tests,resources/js
+sonar.test.inclusions=tests/**,resources/js/**/*.test.tsx
```

`sonar.sources=app,resources/js,routes` continúa idéntico. También permanecen idénticos `sonar.exclusions`, Project Key, nombre, versión 1.1, encoding y ruta Clover. No se añadió `sonar.coverage.exclusions`, NOSONAR, exclusión de código productivo ni una propiedad de LCOV sin reporte real.

La [documentación oficial de patrones de inclusión](https://docs.sonarsource.com/sonarqube-community-build/project-administration/adjusting-analysis/setting-analysis-scope/excluding-files-based-on-patterns.md) establece que las inclusiones de tests se aplican automáticamente como exclusiones de fuentes para evitar doble indexación. El log confirma exactamente ese comportamiento para `tests/**` y `resources/js/**/*.test.tsx`. **No hizo falta añadir exclusiones manuales.** Los archivos de prueba siguen analizados, ahora como UTS, no desaparecen del proyecto.

Validación estática: se comprobaron las propiedades esperadas y los ocho archivos que coinciden con el patrón, todos con declaraciones de tests reales. Validación efectiva: scanner exit 0 sin solapamiento y API devuelve UTS para los ocho:

| Archivo bajo `resources/js/components/` | Clasificación antes | Después |
|---|---|---|
| `data-table.test.tsx` | FIL | UTS |
| `experience-3d/experience-3d.test.tsx` | FIL | UTS |
| `form-controls.test.tsx` | FIL | UTS |
| `motion.test.tsx` | FIL | UTS |
| `vacancies/operational-risk-card.test.tsx` | FIL | UTS |
| `password-input.test.tsx` | FIL | UTS |
| `sidebar-skeleton.test.tsx` | FIL | UTS |
| `visual-qa.test.tsx` | FIL | UTS |

### 16.2. Ejecución y evidencia

Se reutilizó el Clover existente: XML validado con DOM, raíz coverage y **151 archivos con rutas relativas app/ existentes**. No se regeneró ni se alteró su contenido, porque no cambió ningún archivo de producción o test desde la ejecución verificada. No se ejecutó PHPUnit, Vitest, TypeScript ni build otra vez en esta etapa exclusivamente de clasificación; sus últimos resultados están en sección 6 y no se presentan como nuevas ejecuciones.

- Scanner **EXECUTION SUCCESS**, exit **0**, 11.052 s; análisis 9.609 s.
- Análisis: `4506671a-dad3-4e66-ab77-94317e92ff9b`, **20/10/2026 21:07:16 America/Lima**.
- Tarea CE: `4166629d-a5f2-4adc-929a-82863108ef5b`, **SUCCESS**, finalizada 21:07:25, 1232 ms.
- Mismo proyecto `saas-reclutamiento-multiempresa`, versión 1.1 y commit base `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6` con WIP sin commit. Continúa el aviso de 9 archivos sin blame completo; no se hizo commit para ocultarlo.
- API consultada después del procesamiento a las **21:08:01 America/Lima**; configuración heredada comprobada a las 21:08:42.
- Evidencias locales ignoradas: `storage/logs/sonarqube-v2-tests-classified-before.json`, `sonarqube-v2-tests-classified-scan.log`, `sonarqube-v2-tests-classified-task.json`, `sonarqube-v2-tests-classified-after.json` y `sonarqube-v2-tests-classified-small-changes.json` (estos cuatro últimos también dentro de storage/logs/).
- Autenticación solo en memoria/entorno del proceso, desde el archivo privado autorizado; sin credenciales en argumentos, properties, docs o logs. No se reutilizó historial.

### 16.3. New Code productivo real

El período sigue siendo **PREVIOUS_VERSION heredado**, fecha de referencia V1 `2026-10-20T21:01:25+0000`. La medida de proyecto `new_lines=178` incluye líneas nuevas de tests; por eso no se usa ese total como equivalente a código productivo.

La API por qualifier da **11 líneas nuevas de fuentes FIL** y **167 de tests UTS** (131 TS y 36 PHP). De las 11 productivas, solo **2** forman parte del denominador actual de cobertura:

| Archivo productivo | Líneas nuevas totales | Nuevas a cubrir | Cubiertas | Sin cubrir |
|---|---:|---:|---:|---:|
| `app/Http/Requests/Candidates/CandidateCvRequest.php` | 2 | 1 | 1 | 0 |
| `resources/js/components/data-table.tsx` | 4 | 0 | 0 | 0 |
| `resources/js/components/vacancies/operational-risk-card.tsx` | 3 | 0 | 0 | 0 |
| `resources/js/components/ui/sidebar.tsx` | 2 | 1 | 0 | 1 |
| **Total productivo** | **11** | **2** | **1** | **1** |

New Code Coverage: **1/2 = 50.0 %**. Las 58 líneas elegibles de tests que distorsionaban la métrica ya no se exigen como cobertura productiva. No se escribió una sola prueba adicional para obtener este cambio: es una **corrección de clasificación**, no una mejora de ejecución ni aumento de cobertura real.

### 16.4. Quality Gate OK y límite que debe explicarse

La respuesta real de `/api/qualitygates/project_status` es:

```json
{
  "status": "OK",
  "ignoredConditions": true,
  "coverageCondition": {
    "metricKey": "new_coverage",
    "status": "OK",
    "actualValue": "50.0",
    "errorThreshold": "80"
  }
}
```

El JSON anterior es un extracto reorganizado para lectura; los campos originales completos están en la instantánea after. No significa que 50 sea mayor o igual que 80.

Se consultó, sin modificar, `/api/settings/values?component=saas-reclutamiento-multiempresa&keys=sonar.qualitygate.ignoreSmallChanges`: devuelve **value=true, inherited=true**. La excepción existente de cambios pequeños ignora la condición de cobertura cuando hay menos de 20 líneas nuevas a cubrir, según la [documentación Community Build de Quality Gates](https://docs.sonarsource.com/sonarqube-community-build/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates). Aquí hay 2. El Gate sigue siendo **Sonar way**, umbral 80, misma asignación antes/después; no se modificó ningún ajuste de servidor o Gate.

**Conclusión prudente:** se obtuvo Gate OK mediante clasificación correcta y comportamiento preexistente de Sonar, pero **todavía NO se obtuvo New Code Coverage >=80 %**. No se debe presentar el Gate como certificación de cobertura suficiente. Para demostrar cobertura real de la línea TS pendiente hace falta generar e importar LCOV, conservando PCOV/Clover para PHP.

### 16.5. Línea productiva pendiente y siguiente trabajo, no ejecutado

Única línea nueva productiva con `isNew=true` y `lineHits=0`:

**`resources/js/components/ui/sidebar.tsx:621`**, dentro de `SidebarMenuSkeleton`:

```tsx
const skeletonStyle = { "--skeleton-width": "70%" } as React.CSSProperties
```

Es la asignación del ancho decorativo determinista que corrigió S2245, no una nueva vulnerabilidad. El test existente `resources/js/components/sidebar-skeleton.test.tsx` renderiza ese componente y verifica el ancho 70 %, determinismo SSR, icono opcional y atributos. La falta de cobertura importada **no prueba que falte una prueba funcional**: actualmente falta provider/reporte LCOV. No se modificó esta línea ni se añadieron tests artificiales.

Antes de modificar nada más queda documentado el diagnóstico: **sí sigue haciendo falta cobertura frontend real/importada** para completar el objetivo >=80 %, aunque el Gate ya aparezca OK. La próxima etapa debe revisar/añadir el provider compatible con Vitest 4.1.11, medir primero las pruebas existentes y solo después decidir si hacen falta nuevas assertions o casos. No se instaló ninguna dependencia ni se añadió la propiedad JS/TS de cobertura durante esta reclasificación.

### 16.6. Comparación y estados finales de esta etapa

| Indicador | V1 histórica | V2 inicial, tests como fuentes | V2 reclasificada actual |
|---|---|---|---|
| Quality Gate | OK, sin condiciones evaluadas | ERROR | **OK, condición de coverage ignorada por cambio pequeño** |
| New Code Coverage | No evaluado en primer análisis | 1.7 % (1/60) | **50.0 % (1/2)** |
| Overall Coverage | 66.5 % | 65.6 % | **69.5 %** |
| Coverage app/ | 89.6 % | 89.6 % | **89.6 %** |
| Coverage resources/js | 0.0 % | 0.0 % | **0.0 %, sin LCOV** |
| Coverage routes/ | 0.0 % | 0.0 % | **0.0 %** |
| Líneas globales a cubrir / sin cubrir | 4379 / 1469 | 4434 / 1524 | **4189 / 1279** |
| Issues abiertos | 5 | 0 | **0** |
| Vulnerabilities / Code Smells / Bugs | 2 / 3 / 0 | 0 / 0 / 0 | **0 / 0 / 0** |
| Security Hotspots | 0 | 0 | **0** |
| Duplicación | 0.0 % | 0.0 % | **0.0 %** |

Las líneas globales cubiertas permanecen **2910**. Se retiraron del denominador de producción **245 líneas de los ocho tests TS**, no 245 líneas de aplicación; la mejora 65.6→69.5 es metodológica, no cobertura nueva obtenida. La comparación con V1 debe declarar expresamente la clasificación diferente y conservar sus métricas originales, no reescribirlas.

Los cinco IDs de la sección 11 se consultaron nuevamente, no solo el total de Issues:

| Regla original | Estado después de reclasificar |
|---|---|
| php:S5693 | CLOSED / FIXED |
| typescript:S2245 | CLOSED / FIXED |
| typescript:S6843 | CLOSED / FIXED |
| typescript:S8786 | CLOSED / FIXED |
| typescript:S6671 | CLOSED / FIXED |

Se conservaron V1, pruebas y cinco correcciones sin tocar código funcional. Cambios de esta etapa limitados a `sonar-project.properties`, este reporte y `docs/PROGRESS.md`; artefactos locales ignorados aparte. No se generaron capturas V2 ni Word V2. Sin git add, commit, push o merge.
