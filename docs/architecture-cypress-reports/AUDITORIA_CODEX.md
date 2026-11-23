# Auditoría Codex

## 1. Alcance

Auditoría independiente del working tree de `chore/sonarqube-macos-setup`, base **41a830ca0674547aa0778d5d0d0b8bc228d62f63**, realizada el **09/11/2026, America/Lima**. Se auditó primero sin editar y después se corrigieron únicamente problemas demostrados. Guía principal: `Guía Práctica INDIVIDUAL de Arquitectura.docx`; referencia secundaria: `Guia desarrollo de pruebas blanca y negra.pdf` (39 páginas escaneadas, revisadas visualmente). Se leyeron las instrucciones de AGENTS/CLAUDE, las skills pertinentes y el estado vigente F34E.

Se revisaron contenido y diffs de:

- **Código funcional recibido:** `routes/web.php`, `app/Providers/AppServiceProvider.php`, `app/Http/Controllers/Reports/RecruitmentReportController.php`, `app/Http/Requests/Reports/RecruitmentReportRequest.php`, `app/Policies/RecruitmentReportPolicy.php`, `app/Services/Reports/RecruitmentReportService.php`, `resources/js/lib/navigation.ts`, `resources/js/lib/reports.ts`, `resources/js/pages/reports/index.tsx`.
- **Pruebas recibidas:** `tests/Feature/Reports/RecruitmentReportTest.php`, `resources/js/lib/reports.test.tsx`, `cypress/e2e/e2e-16-tabla-accesible-movil.cy.js`, `e2e-17-motion-accesible.cy.js`, `e2e-20-reports.cy.js`. Además, e2e-03, configuración, comandos de soporte, protección del reset E2E y contratos de DataTable/sidebar.
- **Seguridad/datos:** OrganizationScope, modelos Application/Vacancy, historial de etapas, enums/roles, autorización y validación; consultas agregadas y opciones. Se contrastaron con pruebas sobre PostgreSQL.
- **Infraestructura/calidad:** Compose, Dockerfile/entrypoint, phpunit.xml, package/composer scripts y locks, configuración Vite Plus, `sonar-project.properties`, workflow de CI y servidor Sonar existente.
- **Documentación:** todos los Markdown de esta práctica, sus dos guías y evidencias, diagrama 17 y referencias a los 16 anteriores; `docs/PROGRESS.md`, `docs/defects.md`, `docs/tdd-evidence.md`, `docs/v1.1/scope-preliminary.md`, histórico Sonar V1/V2 y documentación de ejecución.

Clasificación del estado recibido: implementación funcional de Reportes; pruebas backend/frontend y Cypress; documentación y evidencias; diagrama 17. **No había cambio de configuración Sonar ni dependencias**. Una instantánea de hashes del estado recibido permitió verificar posteriormente qué editó Codex y qué ya venía del implementador.

No se hizo staging, commit, push, merge, rebase, fetch, pull ni cambio de rama. No se generó DOCX/PDF ni se instaló nada. No se inició RF-29 ni F35-SBX. Los secretos se usaron solo en memoria para autenticación; no se incluyen en las evidencias.

## 2. Estado recibido de Claude

| Afirmación recibida | Verificación independiente |
|---|---|
| Línea base PHPUnit 414 passed + 8 skipped | Log histórico recibido existe; no se revirtió código para repetir la línea base |
| Después de Reportes: 426 passed + 8 skipped, 1715 aserciones | Confirmado al recibir y tras corrección mínima; 434 total, 0 fallidas |
| Vitest 54/54, Reportes 6/6 | Confirmado en dos ejecuciones completas |
| Reportes PHPUnit 12/12 | Confirmado, 209 aserciones; incluido también en regresión completa |
| Cypress 21 specs, 94/94 | Confirmado dos veces; final 02:37, 100 %, 0 omitidas |
| Sonar V3: nueva cobertura 85,0 %, global 70,3 %, duplicación 0 y hotspots 0 | Confirmado por API, nuevo scanner y capturas UI reales |
| 52 requisitos, 49 completos y 3 parciales | **Incorrecto el recuento**: la matriz recibida tiene 59 IDs únicos, 56 completos y 3 parciales |
| Falta IDE y UI Sonar | Confirmado al recibir; cerrado con 8 capturas reales (1 IDE y 7 Sonar) |
| PHPStan histórico 91 | El estado recibido daba **105**: 14 nuevos del servicio y 91 históricos; corregidas solo las anotaciones nuevas |
| Reportes reales, seis indicadores, filtros y tenant | Confirmado en código, BD y tres niveles de pruebas, con la precisión de filtros de §8 |

Los logs del implementador y las capturas históricas se preservaron. Sus corridas no se presentan como ejecutadas por Codex. Las salidas independientes están en [`evidencias/codex/`](evidencias/codex/).

## 3. Hallazgos

**Balance de la auditoría:** 0 CRÍTICOS, 0 ALTOS, 3 MEDIOS, 4 BAJOS y 4 INFORMATIVOS. Dos MEDIOS se corrigieron/cerraron; el tercero es deuda histórica explícitamente diferida. No se encontraron fugas tenant ni regresiones funcionales reproducibles.

| ID | Severidad | Área | Hallazgo | Evidencia | Acción |
|---|---|---|---|---|---|
| AUD-01 | MEDIO | Tipado PHP | El servicio nuevo introducía 14 errores PHPStan por tipos invariantes de Collection, objetos agregados y arrays; total real recibido 105, no 91 | `evidencias/codex/phpstan-received.log`, diff de PHPDoc | **CORREGIDO**: alias ReportRow y contratos veraces; servicio 0 errores, proyecto 91 históricos |
| AUD-02 | MEDIO | Evidencias académicas | IDE y capturas UI Sonar obligatorios faltaban, dejando 3 requisitos parciales | Matriz/manifiesto recibidos; nuevas capturas | **CERRADO**: ARQ-TECH-09 y SONAR-05/08 con capturas nativas reales |
| AUD-03 | MEDIO | Deuda heredada | PHPStan global 91 errores, Pint 8 archivos y formato global fallan; Sonar no los sustituye | Logs finales PHPStan/Pint; `lint-received.log` (342 archivos al recibir) y Oxlint 5 warnings | **DIFERIDO** al alcance autorizado; no masificar fixes ni declarar esos checks aprobados |
| AUD-04 | BAJO | Trazabilidad | Recuento reportado 52 no coincide con 59 IDs de la matriz | Conteo por secciones/IDs, matriz final | **CORREGIDO DOCUMENTALMENTE**: 59/59 con evidencia, sin eliminar ni inventar IDs |
| AUD-05 | BAJO | Diagnóstico E2E | La documentación atribuía la demora de 324 s a contención sin telemetría causal | Reporte Cypress recibido y nuevas corridas | **CORREGIDO DOCUMENTALMENTE**: hipótesis no confirmada; no reproducida en dos suites |
| AUD-06 | BAJO | Definición de indicadores | Algunas frases decían que todos los filtros afectan a todos los KPI. La etapa no aplica al conteo de vacantes publicadas | Service y Request; tabla de fórmulas | **CORREGIDO DOCUMENTALMENTE** sin alterar la definición del KPI ni las pruebas |
| AUD-07 | BAJO | Preservación Sonar | Se proponía migrar H2 a PostgreSQL como bajo riesgo; la UI advierte que H2 no soporta migración a otro motor | SONAR-UI-04/06/07, propuesta M-6 recibida | **CORREGIDO DOCUMENTALMENTE**: planificar instancia futura y preservación, sin migrar ni recrear nada |
| AUD-08 | INFORMATIVO | Alcance de seguridad | Community Build advierte análisis limitado; Hotspots está deprecado en esta versión | SONAR-UI-06/07 y API | Advertencia incorporada: 0 detectados no certifica ausencia de vulnerabilidades |
| AUD-09 | INFORMATIVO | Git | Referencias distintas: main local 8a00505 y origin/main b8892af | `git rev-parse` de ambas refs | Documentado; **no modificado ni sincronizado**, no fetch/pull |
| AUD-10 | INFORMATIVO | Instrumentación | Un intento de PHPUnit concurrente con build falló por CSS transitoriamente ausente del manifiesto | `phpunit-final.log` vs `phpunit-final-sequential.log` | Repetido secuencialmente: 426 passed; Clover y Cypress posteriores verdes; sin parche de producción |
| AUD-11 | INFORMATIVO | Runtime/herramientas | Scanner avisa de reflexión Java y ausencia de blame en 11 archivos sin commit; build conserva aviso opcional de fontaine | `sonar-scanner-codex.log`, `frontend-final.log` | No bloquea ejecución; no se cambió Java, dependencias ni configuración para ocultarlo |

## 4. Correcciones realizadas

### Corrección de tipado, sin alterar comportamiento

Único archivo de software editado por Codex: **`app/Services/Reports/RecruitmentReportService.php`**. Cambios exclusivamente en comentarios PHPDoc:

- Alias local `ReportRow` con campos agregados `vacancy_id`, `status`, `applied_at`, `shortlisted_at` y `reached_shortlist`, objeto mutable compatible con `stdClass`.
- Tipos Collection coherentes en el productor y sus consumidores.
- Contratos de arrays con claves enteras según la inferencia real de Laravel/PHPStan.

Se comparó el contenido ejecutable con la copia recibida, quitando comentarios/espacios: **idéntico**. Ninguna instrucción, consulta, fórmula, permiso o filtro cambió. No se añadieron ignores, baseline nuevo, dependencias ni supresiones. PHPStan dirigido al servicio terminó sin errores; global 105 → 91.

### Correcciones documentales y evidencias

Se aclararon los filtros de KPI, límites de seguridad/H2, carácter no demostrado de la causa de e2e-03, procedencia histórica de resultados, conteo de requisitos y estado de captura del IDE. Se actualizaron README, arquitectura tecnológica, módulo/impacto, resultados Cypress/Sonar, matrices, manifiesto, informe técnico Markdown, PROGRESS y nota de reauditoría DEF-14/15. Se añadió este informe y la evidencia independiente. Los registros históricos no se borraron ni se convirtieron en resultados actuales.

## 5. Arquitectura

**VERIFICADA:** monolito modular Laravel **13.31.0**, React **19.3.0**, Inertia React **3.7.1** / Laravel **3.3.4**, TypeScript **5.9.3**, PostgreSQL **17.11**, Redis **7.4.11**. Docker **29.7.2**, Compose **v5.5.1**, macOS **27.2 arm64**. PHP **8.4.25**, Node **22.23.2**, npm **10.9.8**, PHPUnit **12.5.35**, PCOV **1.0.12**, Vitest **4.1.11**. Las versiones se contrastaron con comandos y locks, no solo con documentos antiguos.

Reportes sigue ruta → Request (autoriza antes de validar) → controlador → servicio de lectura → modelos/consultas → PostgreSQL → props Inertia → React. Sin API BI, tablas, migraciones o biblioteca de gráficos nueva. Dos gráficos HTML/CSS y DataTable consumen props reales.

**RF-28:** candidato implementado localmente para esta práctica; no constituye promoción de RF-01–27 ni aprobación institucional. **RF-29:** servicio propio FastAPI, experimental, opcional, fuera del Compose y `ml.enabled=false` verificado. No se levantó; las pruebas usan dobles cuando corresponde. No hay recomendación ni selección automática de personas.

El diagrama **17_MODULO_REPORTES_COMPONENTES.drawio** ya existía: XML válido `mxfile → diagram → mxGraphModel`, una página, 26 mxCell, elementos editables; SVG y PNG presentes y revisados visualmente. No fue necesario recrearlo. Los 16 diagramas anteriores permanecieron sin cambios. La apertura nativa en diagrams.net del conjunto sigue siendo una revisión humana recomendable, no una validación inventada.

## 6. Cypress

Binario y paquete **15.3.0**, Electron **36.8.1 / Chromium 136**, Node incluido **22.18.0**. `cypress verify` **COMPLETED**, sin reinstalación. Configuración: `testIsolation`, retries 0, soporte propio y selectores data-cy. Suite formal de 21 specs, con pruebas de acceso, reglas, flujo, roles, tenant, UI y Reportes.

| Corrida independiente | Specs | Tests | Passed | Failed | Skipped/Pending | % | Duración Cypress |
|---|---|---|---|---|---|---|---|
| Estado recibido | 21 | 94 | 94 | 0 | 0 | 100 % | 02:46 |
| **Final tras corrección mínima** | **21** | **94** | **94** | **0** | **0** | **100 %** | **02:37** |

Reloj final con preparación: **175,770 s**. Comando final: `docker compose --profile e2e run --rm --no-deps cypress`, con app-e2e y queue-e2e saludables previamente. Se verificó **APP_ENV=e2e, E2E_DATABASE=reclutamiento_e2e y conexión activa a esa misma BD**; el reset solo operó sobre esa base descartable. No se reinició ni borró la base principal.

**e2e-16 (7/7):** el diff sustituye la exigencia de atributo role=cell por comprobación de TD y rol ausente o cell. Mantiene encabezados, asociaciones, filas y overflow. Es consistente con [HTML-ARIA para td](https://www.w3.org/TR/html-aria/#el-td), sin afirmar validación completa con lector de pantalla.

**e2e-17 (8/8):** Escape sobre body evita el clic geométrico en el panel y mantiene cierre y devolución de foco. Contraste con [comportamiento `.type()` de Cypress](https://docs.cypress.io/api/commands/type). No se eliminaron assertions para obtener un falso positivo. Codex no volvió a editar esos specs.

**e2e-20 (9/9):** comprueba seis KPI, filtros, cero datos, actualización BD tras preselección 8 → 9, org B, rechazo de ID ajeno, roles y móvil. No se limita a visitar y leer texto estático.

**e2e-03:** final 2/2 en 4 s; prueba negativa 1251 ms, frente a 1462 ms en la primera corrida Codex. La demora histórica no se reprodujo. Sin retry oculto ni dependencia externa que la explique; su causa sigue no demostrada. No se parcheó un evento aislado.

No se detectaron `.only` ni debugger ejecutable. Sondeo de cola cada 250 ms condicionado y acotado, no pausa fija arbitraria de la suite. Esperas en `cypress/visual/` quedan como deuda auxiliar fuera del patrón formal. Detalle y logs: [`cypress/RESULTADOS_CYPRESS.md`](cypress/RESULTADOS_CYPRESS.md).

## 7. SonarQube

Servidor existente preservado: **Community Build 26.10.0.133078**, contenedor sonarqube, H2, `http://localhost:9000`. SonarScanner **8.1.0.6389**. Token privado leído únicamente para autenticación y entorno del scanner, sin incluirlo en argumentos persistentes, configuración, logs ni Git.

Nueva medición V3 del working tree, **09/11/2026 22:20:19 Lima**, analysis **ff71984c-9177-40eb-b244-0468a15bbdf2**; CE task **96f51c6e-cb3f-435b-b32b-9d28f6ac02a2**. Scanner **EXECUTION SUCCESS**, CE **SUCCESS**. No se modificaron sources/tests/exclusions, Gate, reglas ni umbrales.

| Métrica final | Valor real |
|---|---|
| Quality Gate | **OK**, ignoredConditions **false** |
| Bugs | **0** |
| Vulnerabilities | **0** |
| Code Smells | **0** |
| Issues abiertos | **0** |
| Coverage global | **70,3 %**; 4407 líneas elegibles, 1311 sin cubrir |
| Coverage app/ | **90,1 %**; 3436 elegibles, 340 sin cubrir |
| Coverage resources/js/ | **0,0 %**; 913 sin cubrir, sin LCOV importado |
| Coverage routes/ | **0,0 %**; 58 sin cubrir |
| New Code Coverage | **85,0 %**, 187/220 cubiertas, 33 sin cubrir |
| New Code total textual | **1645 líneas**; recibido 1643, +2 de PHPDoc, sin alterar elegibles |
| Duplicated Lines global / nuevo | **0,0 % / 0,0 %** |
| Security Hotspots | **0**; sin valor de porcentaje revisado, no se afirma 100 % |
| Complexity / Cognitive Complexity | **2064 / 712** |
| Technical Debt tradicional | **0 min** de issues abiertos Sonar |

Sonar way evaluó y cumplió: nueva cobertura ≥80 %, nueva duplicación ≤3 %, nuevos issues=0. La definición New Code es PREVIOUS_VERSION desde **2026-10-20T21:01:25Z**. No es el caso de V2 histórico: V2 fue **OK por Small Changes**, ignoredConditions=true y cobertura nueva **50 %, no 80 %**. V1 y V2 no se reescribieron.

Las cinco reglas originales `php:S5693`, `typescript:S2245`, `typescript:S6843`, `typescript:S8786` y `typescript:S6671` siguen **CLOSED/FIXED**, consultadas individualmente, no deducidas del total.

Clover real regenerado con PCOV; normalización documentada conserva 155 archivos, 2945 sentencias y 2666 cubiertas. Sonar lo importó; su métrica de líneas app/ es 90,1 %, distinta del cociente de sentencias Clover. **No hay LCOV frontend**. El módulo nuevo aporta 187 líneas PHP elegibles (186 cubiertas), el cambio previo de CV 1/1, TS 0/31 y routes 0/1: total **187/220**. No se excluyó código para mejorar el resultado.

Advertencias: UI en MQR mode; Community Build declara alcance limitado de seguridad; H2 solo evaluación y sin migración a otro motor soportada según su aviso. Zero Issues no es certificación de seguridad. Scanner mantiene warning Java y blame faltante en 11 archivos sin commit. Ninguno impidió el análisis. Evidencias: [`sonarqube/RESULTADOS_SONARQUBE.md`](sonarqube/RESULTADOS_SONARQUBE.md) y [`evidencias/codex/sonar-final.json`](evidencias/codex/sonar-final.json).

## 8. Reportes

Se verificaron **seis indicadores desde BD**, sin arrays simulados ni valores hardcodeados:

| Indicador | Fórmula / universo |
|---|---|
| Postulaciones | Count de applications por organization_id, applied_at y filtros |
| Vacantes publicadas | Count de vacancies no borrador, published_at en período y filtro de vacante; **sin filtro de etapa** |
| Promedio por vacante | Postulaciones / vacantes distintas con postulaciones filtradas; null si denominador cero |
| Alcanzaron preselección + tasa | Historial hacia shortlisted o estado actual alcanzable después; tasa sobre postulaciones filtradas |
| En evaluación/entrevista | Count por estado actual evaluation/interview dentro del conjunto filtrado |
| Días a preselección | Promedio de max(0, primera preselección − applied_at) / 86400; null si no hay fecha |

Fechas inclusivas; ventana por defecto 90 días y máximo 731. Validación de fechas, orden, enum y vacante propia no borrador. Los filtros de período/vacante afectan a KPI, gráficos y tabla; etapa limita cinco KPI de postulaciones y ambas visualizaciones/tabla, no el conteo de vacantes publicadas. El texto sobre filtros se ajustó a esta semántica, sin alterar código.

Los dos gráficos usan agrupaciones backend: ocho estados (incluidos ceros) y semanas lunes–domingo con ceros. La tabla agrupa por vacante de la misma organización. El frontend consume props; maneja vacío y null. Verificado tanto con fixtures de prueba como con registros DemoSeeder guardados en PostgreSQL.

Impacto: resultados funcionales medidos separados de beneficios potenciales. No se atribuyen reducciones de tiempo o porcentajes sin estudio. AS-IS sigue preliminar, TO-BE propuesto y RF-23 mantiene decisión humana. RF-28 implementado para esta práctica no cambia el baseline histórico.

## 9. Multitenencia

**Estado: aislamiento verificado en el alcance del módulo; no se encontró fuga.**

1. Gate viewRecruitmentReports: HR o Approver con organization_id. FormRequest autoriza antes de validar.
2. Application/Vacancy aplican OrganizationScope; además, el servicio filtra explícitamente por la organización del usuario autenticado.
3. La subconsulta MIN de primera preselección correlaciona application_id y también organization_id del historial. No mezcla filas de otras organizaciones.
4. La consulta de vacantes publicadas, las opciones y las etiquetas de tabla aplican organization_id. No se aceptan tenant IDs del query string.
5. El filtro exists valida ID + organización + no borrador. Una vacante de B enviada por A se rechaza sin exponer su título o datos.
6. Se revisaron agregaciones, conteos, agrupaciones y toBase sin encontrar un escape de scopes o un join sin acotar.

Pruebas explícitas: `test_rf28_reports_never_include_records_of_another_organization` y `test_rf28_vacancy_of_another_organization_cannot_be_used_as_filter`; además, autorización, opciones y ausencia de PII. Cypress e2e-20 verifica A=9 postulaciones/B=1 y el rechazo de vacante ajena. Ambas organizaciones se crean en la BD de pruebas, no son un supuesto documental.

No se cambió middleware global, Policy, organización ni esquema. Los agregados no contienen nombres, correos, IDs de candidato o puntajes personales. El servicio es de lectura y no escribe auditoría ni decide sobre personas.

## 10. Tests

| Herramienta / alcance | Resultado final real | Evidencia |
|---|---|---|
| PHPUnit completo | **434 total: 426 passed, 8 skipped, 0 failed, 1715 assertions**; 10,57 s reportados por Laravel | `phpunit-final-sequential.log` |
| PHPUnit Reportes | **12/12, 209 assertions**; también incluidos en la suite final | `reports-received.log` y suite final |
| PHPUnit + PCOV/Clover | **434 tests, 8 skipped, 1715 assertions**, exit 0 | `coverage-final.log` |
| Vitest completo | **54/54**, 9 archivos, 0 fallidas | `frontend-final.log` |
| Vitest Reportes | **6/6**, utilidades con assertions de comportamiento | mismo log y `resources/js/lib/reports.test.tsx` |
| TypeScript | **0 errores**, exit 0 | `frontend-final.log` |
| Build | **PASS**, 4,20 s de build, con aviso opcional preexistente de fontaine | `frontend-final.log` |
| PHPStan del servicio corregido | **0 errores** | `phpstan-reports-final.log` |
| PHPStan global | **FAILED: 91 errores históricos**, nivel 7 | `phpstan-final.log` |
| Pint --test | **FAILED: 8 archivos / 261 revisados**, sin corrección automática | `pint-final.log` |
| npm run check | **FAILED por formato**, 342 archivos medidos al recibir; no se presenta como recuento posterior a editar Markdown | `lint-received.log` |
| Oxlint separado | **5 warnings, 0 errores, exit 1** según política de warnings | `oxlint-final.log` |
| Cypress final | **94/94**, 21 specs; 02:37 | `cypress-final.log` |

Comandos backend/frontend usados realmente:

```sh
docker compose exec -T app php artisan test
docker compose exec -T app php artisan test --filter=RecruitmentReportTest
docker compose exec -T app composer types:check
docker compose exec -T app vendor/bin/pint --test
docker compose exec -T app npm run types:check
docker compose exec -T app npx --no-install vp test --run
docker compose exec -T app npm run build
docker compose exec -T app npm run check
docker compose exec -T app npx --no-install vp lint
docker compose exec -T app php -d pcov.enabled=1 vendor/bin/phpunit --coverage-clover coverage.xml --colors=never
```

Se conservó un intento concurrente fallido: PHPUnit iniciado mientras el build reconstruía assets obtuvo **425 passed, 8 skipped y 1 failed** por CSS ausente. La repetición **secuencial** tras acabar build pasó y fue seguida por Clover y Cypress también aprobados. No se borró el log ni se parcheó código para ocultar el fallo de instrumentación. Las ejecuciones finales están asociadas al mismo código ejecutable auditado.

No hubo nuevas pruebas vacías, supresiones ni ajustes de cantidades para reproducir el reporte. La modificación PHPDoc no requirió nuevos tests espejo; se ejecutaron las regresiones exigidas de todos modos.

## 11. Evidencias

Se obtuvieron **7 capturas reales Sonar UI** y **1 captura real de VS Code**, sin modificar imágenes ni fabricar salidas. Se usó Safari nativo con sesión existente; no se imprimió token ni contraseña. Se restauró el zoom temporal de captura. La UI MQR se contrasta con contadores tradicionales de API; no se atribuyen a la imagen métricas no visibles.

- `evidencias/sonarqube/SONAR-UI-01_Proyecto.jpg`
- `evidencias/sonarqube/SONAR-UI-02_Quality_Gate.jpg`
- `evidencias/sonarqube/SONAR-UI-03_Metricas_Globales.jpg`
- `evidencias/sonarqube/SONAR-UI-04_Coverage.jpg`
- `evidencias/sonarqube/SONAR-UI-05_Issues.jpg`
- `evidencias/sonarqube/SONAR-UI-06_Security_Hotspots.jpg`
- `evidencias/sonarqube/SONAR-UI-07_Limitaciones_Seguridad.jpg`
- `evidencias/arquitectura/ARQ-TECH-09_IDE_VSCode.jpg`

Manifiesto final: **32 registros principales, 32 disponibles, 0 pendientes**; 16 imágenes totales en esta fase (8 PNG y 8 JPEG), incluido el diagrama 17. EV-SON-06 agrupa siete archivos y EV-COD-01 agrupa salidas de auditoría; no se confunden registros con número de archivos. Los logs/JSON originales de Claude siguen intactos; las copias API independientes omiten metadatos personales de autor/asignación que no son necesarios para las métricas. Salidas ANSI y ruido dbus se eliminaron de las copias legibles, sin alterar resultados; no son capturas de terminal fabricadas.

La matriz conserva **59 IDs únicos** (5 general, 10 arquitectura SW, 9 tecnológica, 11 Cypress, 8 Sonar, 8 Reportes, 7 Impacto, 1 Informe). Tras cerrar ARQ-TECH-09 y SONAR-05/08: **59 completos, 0 parciales, 0 pendientes** para el artefacto fuente Markdown. No se afirma que exista ya un DOCX/PDF final.

El informe técnico mantiene exactamente sus **10 secciones**: portada, descripción, arquitectura SW, arquitectura tecnológica, Cypress, Sonar, Reportes, impacto, conclusiones y anexos. Se verificaron referencias locales, archivos de imágenes, XML, secretos y diff; resultado reproducible en `evidencias/codex/validacion-final.json`.

## 12. Rúbrica

Estimación conservadora tras las evidencias nuevas, no atribución de nota:

| Categoría | Máximo | Estimación |
|---|---|---|
| Arquitectura de software | 4 | **3** |
| Arquitectura tecnológica | 3 | **3** |
| Cypress | 5 | **5** |
| SonarQube | 4 | **4** |
| Reportes e impacto | 4 | **4** |
| **Total** | **20** | **19/20** |

La reserva en arquitectura corresponde a revisión humana en editor nativo de diagramas y valoración docente de integración opcional demostrada con dobles, no en vivo. No se exige activar ML ni inventar un despliegue. [Matriz detallada](requisitos/MATRIZ_RUBRICA.md). No se recomienda 20/20 automático ni se rebajan umbrales de calidad.

## 13. Riesgos restantes

- **Deuda previa, no saneada:** PHPStan 91, Pint 8 y formato; Oxlint 5 warnings. La fase no tiene todos los checks globales verdes. Requieren autorización y trabajo separado, no refactor masivo durante esta auditoría.
- **Cobertura frontend:** sin LCOV, 0 % importado. Vitest/Cypress aprobados no equivalen a cobertura importada. Falta una rama específica de fecha futura del Request; no afecta el Gate actual, pero debe planificarse.
- **Seguridad/infraestructura:** Community Build limitado y H2 solo evaluación. Cero hallazgos no significa ausencia de vulnerabilidades. No trasladar estos datos a producción ni recrear/migrar el histórico sin un plan validado.
- **Evidencia académica:** AS-IS institucional no validado, beneficios de proceso no medidos, RF-28 no promovido al baseline. DOCX/PDF y revisión humana del diff son pasos posteriores; no se generaron aquí.
- **Git:** main local y origin/main difieren (8a00505 vs b8892af), solo referencias locales leídas. No se resolvió ni se tocó main.
- **Operación:** evitar ejecutar build y pruebas web al mismo tiempo sobre el volumen compartido. La causa de e2e-03 histórico sigue abierta como hipótesis si vuelve a reproducirse.

Al terminar se **detuvieron solo app-e2e y queue-e2e**, sin eliminar contenedores, bases ni volúmenes. Se mantuvieron app, queue, postgres, redis y sonarqube; `/health` final dio database=ok y redis=ok. El contenedor Sonar histórico sigue running. No se ejecutó down -v, prune, migrate:fresh contra la BD principal ni ningún comando destructivo.

## 14. Veredicto

**LISTO PARA CIERRE** técnico de esta práctica y revisión humana local.

No se encontró fuga multiempresa; Reportes obtiene datos reales persistidos; PHPUnit, Vitest, TypeScript, build y Cypress finales pasaron; scanner y procesamiento terminaron SUCCESS; las métricas Sonar están completas y el Gate se evaluó con 85,0 %; las evidencias obligatorias de IDE y Sonar UI están disponibles. La corrección PHPDoc eliminó los errores nuevos del servicio sin modificar su comportamiento.

Este veredicto **no** declara ausencia de deuda global, preparación productiva, aprobación institucional o calificación docente. Los checks estáticos históricos fallidos se dejan expresos, junto con cobertura frontend y revisión documental final. Todos los cambios quedan locales para revisión: **NO git add, NO commit, NO push, NO merge, NO rebase y main NO modificado**.
