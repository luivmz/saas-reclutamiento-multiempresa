# Resultados SonarQube: análisis V3 (práctica individual)

> Actividad 4 de la guía. El análisis **V3** se ejecutó el 09/11/2026 sobre el **working tree** de la rama `chore/sonarqube-macos-setup`: HEAD `41a830c` más los cambios **sin commit** de esta práctica. El historial V1/V2 del 20/10/2026 **se conserva sin cambios** en [`docs/sonarqube/`](../../sonarqube/) y aquí solo se compara.

## 1. Configuración (sin cambios)

| Elemento | Valor | Fuente |
|---|---|---|
| Servidor | SonarQube Community Build **26.10.0.133078**, contenedor existente `sonarqube` (`localhost:9000`, H2 embebido de evaluación), estado `UP` | `GET /api/system/status` |
| Scanner | SonarScanner CLI **8.1.0.6389** (Homebrew, macOS arm64) | `sonar-scanner --version` |
| Proyecto | key `saas-reclutamiento-multiempresa`, nombre «SaaS Reclutamiento Multiempresa», versión 1.1 | `sonar-project.properties` |
| Fuentes / pruebas | `sonar.sources=app,resources/js,routes`; `sonar.tests=tests,resources/js`; `sonar.test.inclusions=tests/**,resources/js/**/*.test.tsx` | idem |
| Exclusiones | `vendor`, `node_modules`, `public/build`, `storage`, `bootstrap/cache`, `docs`, `database`, `cypress`, `ml-service` | idem |
| Cobertura | Clover de PHPUnit (`sonar.php.coverage.reportPaths=coverage.xml`) generado con PCOV 1.0.12. **Sin LCOV de frontend** | idem |
| Quality Gate | **Sonar way** (predeterminado), sin modificar | API |
| Período de código nuevo | `PREVIOUS_VERSION`, desde el 2026-10-20T21:01:25Z (primer análisis de la versión 1.1) | API |
| Autenticación | Token local en `storage/app/private/.sonar-token` (ignorado por Git), pasado como `SONAR_TOKEN` en el entorno del proceso y retirado con `unset`. **No aparece** en logs ni documentos | procedimiento de [`docs/sonarqube/README.md`](../../sonarqube/README.md) |

No se tocaron `sonar-project.properties`, perfiles, reglas, umbrales ni exclusiones. El archivo de pruebas nuevo `resources/js/lib/reports.test.tsx` usa la extensión `.test.tsx` precisamente para que la regla de inclusión existente lo clasifique como prueba y no como fuente.

## 2. Ejecución recibida de Claude (preservada)

| Paso | Comando | Resultado |
|---|---|---|
| Cobertura | `docker compose exec -T app php -d pcov.enabled=1 vendor/bin/phpunit --coverage-clover coverage.xml --colors=never` | 434 pruebas, 1715 aserciones, 8 omitidas, salida 0 |
| Normalización Clover | comando PHP documentado en `docs/sonarqube/README.md` | `files=155 statements=2945 covered=2666` (≈ 90,5 % de sentencias de `app/`) |
| Análisis | `sonar-scanner` | **EXECUTION SUCCESS**, 348 archivos indexados, Clover importado, total 11,99 s |
| Procesamiento | `GET /api/ce/task` | **SUCCESS**, 2 353 ms; task `af93f5e8-a58e-450a-bc7a-11fcac0862e9`; analysis `009b62ce-7f69-4c84-b5cf-1f8a0f257bec`; SCM revision `41a830c…` |

Advertencia del servidor (1): *Missing blame information for 11 files*. Es esperable porque esos archivos son nuevos o están modificados **sin commit**, así que Git no tiene autoría para ellos. No impidió el análisis, pero el cálculo de «código nuevo» de esos archivos se basa en la comparación con el análisis anterior y no en fechas de commit.

Evidencias: [`sonar-scanner-v3.log`](../evidencias/sonarqube/sonar-scanner-v3.log), [`sonar-api-v3.json`](../evidencias/sonarqube/sonar-api-v3.json), [`sonar-api-antes-v3.json`](../evidencias/sonarqube/sonar-api-antes-v3.json), [`phpunit-coverage-v3-resumen.log`](../evidencias/sonarqube/phpunit-coverage-v3-resumen.log) y la [captura de la salida real](../evidencias/sonarqube/SONAR_V3_resultados_terminal_api.png).

## 3. Métricas V3 (API, sin redondeos propios)

| Métrica | Resultado | Interpretación |
|---|---|---|
| **Quality Gate** | **OK (Passed)**, condiciones **evaluadas** (`ignoredConditions=false`) | Cumple las tres condiciones de Sonar way sobre código nuevo |
| ↳ New Coverage | **85,0 %** (220 líneas a cubrir, 33 sin cubrir) ≥ 80 % | Cumple; ver §5 para su composición |
| ↳ New Duplicated Lines | 0,0 % ≤ 3 % | Cumple |
| ↳ New Violations (issues nuevos) | 0 | Cumple |
| **Bugs** | **0** (Reliability Rating A) | Sin defectos probables detectados |
| **Vulnerabilities** | **0** (Security Rating A) | Sin problemas de seguridad detectados por las reglas |
| **Code Smells** | **0** (Maintainability Rating A, deuda 0 min) | Sin problemas de mantenibilidad abiertos |
| Issues abiertos (total) | 0 | Tampoco hay issues MQR de seguridad, fiabilidad o mantenibilidad |
| **Security Hotspots** | **0** (`security_hotspots_reviewed` sin valor) | No hay puntos para revisar; no se afirma «100 % revisados» |
| **Coverage (global)** | **70,3 %** (4 407 líneas a cubrir, 1 311 sin cubrir) | Promedio de backend cubierto y frontend sin reporte |
| ↳ `app/` | **90,1 %** (3 436 / 340 sin cubrir) | Backend bien ejercitado por PHPUnit |
| ↳ `resources/js/` | **0,0 %** (913 sin cubrir) | Sin LCOV: Vitest corre, pero su cobertura no se importa |
| ↳ `routes/` | 0,0 % (58) | Archivos de rutas no instrumentados por Clover |
| **Duplicated Lines** | **0,0 %** | Sin duplicación |
| Tamaño | 19 856 ncloc | +878 frente a V2 (18 978) |
| Complejidad | ciclomática 2 064 · cognitiva 712 | Agregados, sin umbral |

## 4. Comparación con las mediciones anteriores

| Métrica | V1 (20/10, inicial) | V2 final (20/10, 21:07 Lima) | **V3 (09/11, esta práctica)** |
|---|---|---|---|
| Quality Gate | OK, `conditions: []` (sin evaluar) | **OK por Small Changes**: `ignoredConditions=true`, New Coverage **50,0 %** (1/2 líneas), **no 80 %** | **OK con las condiciones evaluadas**: New Coverage **85,0 %** (187/220), `ignoredConditions=false` |
| Issues abiertos | 5 | 0 | 0 |
| Bugs / Vulnerabilities / Code Smells | 0 / 2 / 3 | 0 / 0 / 0 | 0 / 0 / 0 |
| Hotspots | 0 | 0 | 0 |
| Coverage global | 66,5 % | 69,5 % | **70,3 %** |
| Coverage `app/` | 89,6 % | 89,6 % | **90,1 %** |
| Duplicación | 0,0 % | 0,0 % | 0,0 % |
| ncloc | 19 495 | 18 978 | 19 856 |

**La advertencia histórica se verificó y sigue siendo cierta para V2:** la API, consultada antes de V3 ([`sonar-api-antes-v3.json`](../evidencias/sonarqube/sonar-api-antes-v3.json)), devolvió para el análisis `4506671a…` (21/10/2026 02:07 UTC) Gate OK con `ignoredConditions=true` y New Coverage 50,0 %. **Ese resultado histórico no se reemplaza.** V3 es una medición nueva y distinta: ahora el código nuevo supera el umbral de «cambio pequeño» (220 líneas a cubrir), así que la condición de cobertura **sí se evaluó** y se cumplió con 85,0 %.

## 5. Interpretación (preguntas 4.3 de la guía)

**¿Qué resultado obtuvo el Quality Gate?** OK, y por primera vez con las tres condiciones de código nuevo evaluadas y cumplidas. La guía no exige un Gate aprobado; lo importante es entender por qué pasa.

**¿Por qué pasa la cobertura nueva y qué oculta?** El 85,0 % es un promedio de líneas nuevas que mezcla dos realidades:

| Archivo nuevo o modificado | Líneas nuevas a cubrir | Sin cubrir | Cobertura nueva |
|---|---|---|---|
| `app/Services/Reports/RecruitmentReportService.php` | 113 | 0 | 100 % |
| `app/Http/Requests/Reports/RecruitmentReportRequest.php` | 54 | 1 | 98,1 % |
| `app/Http/Controllers/Reports/RecruitmentReportController.php` | 16 | 0 | 100 % |
| `app/Policies/RecruitmentReportPolicy.php` | 3 | 0 | 100 % |
| `app/Providers/AppServiceProvider.php` | 1 | 0 | 100 % |
| `app/Http/Requests/Candidates/CandidateCvRequest.php` (cambio V2) | 1 | 0 | 100 % |
| `resources/js/pages/reports/index.tsx` | 20 | 20 | 0 % |
| `resources/js/lib/reports.ts` | 9 | 9 | 0 % |
| `resources/js/lib/navigation.ts` | 1 | 1 | 0 % |
| `resources/js/components/ui/sidebar.tsx` (cambio V2) | 1 | 1 | 0 % |
| `routes/web.php` | 1 | 1 | 0 % |

El backend nuevo está prácticamente cubierto al 100 % por las 12 pruebas Feature (TDD). El frontend nuevo figura con **0 %** aunque `reports.ts` tiene 6 pruebas Vitest que pasan y la página está ejercitada por 9 escenarios Cypress. La causa: **Sonar no recibe cobertura de JavaScript/TypeScript** (no hay LCOV). Si las 31 líneas TS nuevas pesaran más, el Gate fallaría, como ocurrió en V2 inicial (1,7 %).

**¿Qué problemas se identificaron?** Ningún issue abierto (0 bugs, 0 vulnerabilidades, 0 code smells, 0 hotspots). Los problemas reales están **fuera** de las reglas de Sonar:

1. Cobertura de frontend invisible para Sonar (0 % en `resources/js`, 913 líneas).
2. `routes/` sin instrumentar (0 %).
3. Deuda de herramientas complementarias, reejecutada por Codex: PHPStan llegó a 105 errores en el estado recibido (14 nuevos del servicio); tras corregir solo PHPDoc volvió a 91 históricos. Pint mantiene 8 archivos y Oxfmt presenta deuda global. Detalle en [`RESULTADOS_SONARQUBE_MAC.md`](../../sonarqube/RESULTADOS_SONARQUBE_MAC.md).
4. La línea 1 sin cubrir de `RecruitmentReportRequest` es la rama `if (! hasta && from > to) $to = from` (sin `hasta` y con `desde` en el futuro); no tiene prueba específica.
5. La instancia usa H2 embebido (solo evaluación): no es apta para conservar el historial a largo plazo.

**¿Qué componentes concentran más observaciones?** Por cobertura, `resources/js/` (913 líneas sin cubrir según Sonar) y `routes/`. En `app/` quedan 340 líneas sin cubrir (90,1 %). No hay componentes con issues abiertos.

**¿Qué vulnerabilidades se detectaron?** Ninguna en V3. Las dos de V1 (`php:S5693` en `CandidateCvRequest` y `typescript:S2245` en `sidebar.tsx`) siguen cerradas desde V2. El módulo nuevo no introdujo ninguna: solo lee, valida todos los parámetros y no construye SQL con concatenación (subconsulta con *query builder* y parámetros enlazados).

**¿Qué nivel de cobertura se obtuvo?** 70,3 % global, 90,1 % en backend y 85,0 % en código nuevo; el frontend no se mide en Sonar.

## 6. Propuestas de mejora

| # | Mejora | Efecto esperado | Esfuerzo / riesgo |
|---|---|---|---|
| M-1 | Generar LCOV con Vitest (`@vitest/coverage-v8`) e importarlo (`sonar.javascript.lcov.reportPaths`) | Cobertura real de `resources/js` y Gate representativo del frontend | Requiere una **dependencia de desarrollo nueva**: decisión del equipo; no se agregó en esta práctica |
| M-2 | Prueba para la rama de `period()` sin `hasta` y con `desde` futuro | Cubrir la única línea pendiente del módulo | Bajo |
| M-3 | Corregir los 91 errores de PHPStan nivel 7 (principalmente factories) | Tipos más seguros | Medio |
| M-4 | Aplicar Pint y Oxfmt en un commit exclusivo de formato | Eliminar ruido de estilo y diffs futuros | Bajo, pero conviene aislarlo para no mezclarlo con cambios funcionales |
| M-5 | Integrar el scanner en CI (job con servidor Sonar persistente o SonarQube Cloud) | Análisis en cada PR, no solo local | Requiere decidir dónde alojar el servidor y cómo guardar el token como secreto de CI |
| M-6 | Planificar una instancia futura con PostgreSQL, preservando el contenedor y los volúmenes históricos de H2 | Persistencia adecuada fuera de evaluación | Requiere revisión de compatibilidad y preservación: la propia UI advierte que H2 **no soporta migración a otro motor**. No se propone una migración directa de bajo riesgo ni se ejecutó cambio alguno |
| M-7 | Volver a ejecutar Cypress en toda corrección guiada por Sonar | Evita regresiones como DEF-14 | Proceso, sin costo técnico |

## 7. Capturas reales del panel obtenidas por Codex

Se utilizó la sesión ya abierta de Safari para navegar por la UI local. No se ingresaron credenciales, no se generó un token y no se modificaron Gate, perfiles, reglas ni ajustes del proyecto. Se guardaron capturas nativas, sin editar ni recrear su contenido:

| ID | Archivo | Evidencia visible |
|---|---|---|
| SONAR-UI-01 | [Proyecto](../evidencias/sonarqube/SONAR-UI-01_Proyecto.jpg) | Nombre, Passed y New Code |
| SONAR-UI-02 | [Quality Gate](../evidencias/sonarqube/SONAR-UI-02_Quality_Gate.jpg) | Cobertura 85,0 % ≥ 80 %, duplicación 0,0 % ≤ 3 %, 0 issues |
| SONAR-UI-03 | [Overall Code](../evidencias/sonarqube/SONAR-UI-03_Metricas_Globales.jpg) | Cobertura global 70,3 %, MQR 0 por calidad y duplicación |
| SONAR-UI-04 | [Coverage](../evidencias/sonarqube/SONAR-UI-04_Coverage.jpg) | Measures, 220 líneas nuevas a cubrir, 33 descubiertas, TS sin reporte |
| SONAR-UI-05 | [Issues](../evidencias/sonarqube/SONAR-UI-05_Issues.jpg) | 0 abiertos, categorías y severidades MQR |
| SONAR-UI-06 | [Security Hotspots](../evidencias/sonarqube/SONAR-UI-06_Security_Hotspots.jpg) | Ninguno para revisar; aviso de deprecación del concepto en esta versión |
| SONAR-UI-07 | [Limitaciones de seguridad](../evidencias/sonarqube/SONAR-UI-07_Limitaciones_Seguridad.jpg) | Community Build declara cobertura limitada de análisis de seguridad; H2 es solo evaluación |

La UI actual es **MQR mode**. Los contadores tradicionales Bugs/Vulnerabilities/Code Smells se obtuvieron de la API y valen 0; no se afirma que esas tres etiquetas aparezcan en la captura de Issues. La cifra `app/` = 90,1 % está en la API por directorio; la captura Coverage muestra global y archivos, no una cifra de directorio inexistente en la imagen.

## 8. Reejecución y contraste independiente de Codex

| Dato | Resultado |
|---|---|
| Fecha del análisis | 09/11/2026 22:20:19 America/Lima (10/11/2026 03:20:19 UTC) |
| Rama / revisión | `chore/sonarqube-macos-setup`, HEAD `41a830ca0674547aa0778d5d0d0b8bc228d62f63` + working tree; no commit de esta fase |
| Scanner | **EXECUTION SUCCESS** |
| CE task | `96f51c6e-cb3f-435b-b32b-9d28f6ac02a2` → **SUCCESS** |
| Analysis ID | `ff71984c-9177-40eb-b244-0468a15bbdf2` |
| Proyecto | `saas-reclutamiento-multiempresa` (mismo proyecto, sin duplicación) |
| Quality Gate | **OK**, `ignoredConditions=false` |
| Condiciones | new_coverage 85,0 ≥ 80; new_duplicated_lines_density 0,0 ≤ 3; new_violations 0 |
| Cobertura nueva | **187/220** líneas cubiertas = **85,0 %**; 33 descubiertas |
| Líneas nuevas totales | 1645; el recibido registraba 1643. Dos líneas de anotación PHPDoc cambiaron el total textual, **no** las 220 elegibles ni el numerador |
| Cobertura global / app / frontend / routes | **70,3 / 90,1 / 0,0 / 0,0 %** |
| Bugs / Vulnerabilities / Code Smells / Issues abiertos / Hotspots | **0 / 0 / 0 / 0 / 0** |
| Duplicación global y nueva | **0,0 / 0,0 %** |
| Complejidad ciclomática / cognitiva | **2064 / 712** |
| Deuda técnica tradicional | **0 min** de Issues abiertos medidos por Sonar; no equivale a ausencia de deuda en otras herramientas |
| Cinco reglas originales | `php:S5693`, `typescript:S2245`, `typescript:S6843`, `typescript:S8786`, `typescript:S6671`: **5/5 CLOSED / FIXED**, comprobados individualmente |

Evidencias independientes: [scanner](../evidencias/codex/sonar-scanner-codex.log), [procesamiento](../evidencias/codex/sonar-task-codex.json), [resumen](../evidencias/codex/sonar-run-codex.json), [API y medidas completas](../evidencias/codex/sonar-final.json), [PCOV/PHPUnit](../evidencias/codex/coverage-final.log). El XML Clover contiene 155 archivos, 2945 sentencias y 2666 cubiertas: esa razón de sentencias no sustituye la métrica de líneas de Sonar (90,1 % en app). Las rutas se normalizaron con el procedimiento existente, sin cambiar la cobertura.

**Límites de seguridad.** Cero hallazgos significa cero detectados por los analizadores disponibles. La UI avisa que Community Build tiene análisis de seguridad limitado (por ejemplo SQL injection y XSS); no demuestra ausencia de vulnerabilidades. La página de Hotspots marca ese concepto como deprecado en esta versión: se mantiene la métrica API solicitada, sin afirmar revisión al 100 % ni inventar un hallazgo. H2 y sus volúmenes históricos se preservaron íntegramente.
