# Manifiesto de evidencias

Todas las evidencias se generaron el **09/11/2026** (America/Lima) sobre el working tree de `chore/sonarqube-macos-setup` (base `41a830c`, sin commit). Son salidas reales de comandos y capturas reales de la aplicación. **No contienen** tokens, contraseñas, cookies ni el contenido de `.env`/`.env.e2e`: se verificaron con una búsqueda de patrones de secretos, sin coincidencias. Los logs se copiaron desde `storage/logs/practica-arq/` (ignorado por Git) sin códigos de color ANSI ni líneas de ruido `dbus`.

Rutas relativas a `docs/architecture-cypress-reports/`.

## Arquitectura y tecnología

| ID | Actividad | Descripción | Archivo | Fecha | Resultado |
|---|---|---|---|---|---|
| EV-ARQ-01 | 1.2 | Diagrama nuevo del módulo de reportes (editable, SVG y PNG) | `arquitectura/diagramas/17_MODULO_REPORTES_COMPONENTES.drawio` · `.svg` · `.png` | 09/11/2026 | XML válido; revisado visualmente, sin cruces de texto |
| EV-ARQ-02 | 1.2 / 2.2 | Diagramas reutilizados 01, 02, 06, 11 y 16 | `docs/metologia/diagramas/` (ver `arquitectura/DIAGRAMAS_REFERENCIA.md`) | 03/11/2026 | Sin cambios; vigencia del 06 y del 11 anotada |
| EV-TEC-01 | 2.1 / 2.3 | Versiones medidas (host y contenedores), estado de los servicios y `/health` | `evidencias/tecnologia/versiones-entorno.log` | 09/11/2026 21:42 | Todos los servicios healthy; `/health` OK |
| EV-TEC-02 | 2.3 | PHPUnit, línea base previa a los cambios | `evidencias/tecnologia/phpunit-linea-base.log` | 09/11/2026 | 414 passed, 8 skipped, 0 failed |
| EV-TEC-03 | 2.3 | PHPUnit final | `evidencias/tecnologia/phpunit-final.log` | 09/11/2026 | 426 passed, 8 skipped, 0 failed (1715 aserciones) |
| EV-TEC-04 | 2.3 | Vitest final | `evidencias/tecnologia/vitest-final.log` | 09/11/2026 | 9 archivos, 54 pruebas aprobadas |
| EV-TEC-05 | 2.3 | Build de producción del frontend | `evidencias/tecnologia/npm-build.log` | 09/11/2026 | `✓ built` |
| EV-TEC-06 | 2.3 | TypeScript (`tsc --noEmit`) | `evidencias/tecnologia/tsc.log` | 09/11/2026 | 0 errores |

## Cypress

| ID | Actividad | Descripción | Archivo | Fecha | Resultado |
|---|---|---|---|---|---|
| EV-CYP-01 | 3.1 | `cypress verify` y `cypress version` en la imagen oficial | `evidencias/cypress/cypress-verify-version.log` | 09/11/2026 | COMPLETED; 15.3.0 |
| EV-CYP-02 | 3.4 | Ejecución completa 1 | `evidencias/cypress/cypress-ejecucion-1-completa.log` | 09/11/2026 | 94 pruebas: 87 ✔ / 7 ✖ (92,55 %) |
| EV-CYP-03 | 3.4 | Captura del resumen de la ejecución 1 (salida real renderizada) | `evidencias/cypress/CYP_ejecucion1_resumen_terminal.png` | 09/11/2026 | idem |
| EV-CYP-04 | 3.4 | Verificación de las correcciones DEF-14 y DEF-15 | `evidencias/cypress/cypress-verificacion-e2e16-e2e17.log` | 09/11/2026 | 15/15 |
| EV-CYP-05 | 3.4 | Ejecución completa 2 (final) | `evidencias/cypress/cypress-ejecucion-2-completa.log` | 09/11/2026 | 94/94 (100 %), 21 specs, 08:33 |
| EV-CYP-06 | 3.4 | Captura del resumen de la ejecución 2 (salida real renderizada) | `evidencias/cypress/CYP_ejecucion2_resumen_terminal.png` | 09/11/2026 | idem |
| EV-CYP-07 | 3.4 | Re-verificación de la duración atípica de e2e-03 | `evidencias/cypress/cypress-reverificacion-e2e03.log` | 09/11/2026 | 2/2 en 4 s |

## SonarQube

| ID | Actividad | Descripción | Archivo | Fecha | Resultado |
|---|---|---|---|---|---|
| EV-SON-01 | 4.4 | Estado previo según la API (histórico V2: Small Changes, 50 %) | `evidencias/sonarqube/sonar-api-antes-v3.json` | 09/11/2026 (consulta) | Gate OK, `ignoredConditions=true`, new_coverage 50,0 |
| EV-SON-02 | 4.1 | Resumen de PHPUnit con cobertura (PCOV) | `evidencias/sonarqube/phpunit-coverage-v3-resumen.log` | 09/11/2026 | 434 pruebas, 8 omitidas |
| EV-SON-03 | 4.1 | Log de SonarScanner V3 | `evidencias/sonarqube/sonar-scanner-v3.log` | 09/11/2026 21:45 | EXECUTION SUCCESS |
| EV-SON-04 | 4.2 | Tarea, Gate, medidas, directorios, issues, hotspots, historial y código nuevo por archivo (API) | `evidencias/sonarqube/sonar-api-v3.json` | 09/11/2026 | Gate OK (evaluado); 0/0/0; cobertura 70,3 %; new 85,0 % |
| EV-SON-05 | 4.2 | Captura de la salida real del scanner y de la API (**no** es la UI) | `evidencias/sonarqube/SONAR_V3_resultados_terminal_api.png` | 09/11/2026 | idem |
| EV-SON-06 | 4 | Capturas reales de la UI de Sonar (7 archivos, detalle debajo) | `evidencias/sonarqube/SONAR-UI-*.jpg` | 09/11/2026 | Disponibles; sesión existente, sin exponer credenciales |

## Reportes

| ID | Actividad | Descripción | Archivo | Fecha | Resultado |
|---|---|---|---|---|---|
| EV-REP-01 | 5.2 | RED de TDD: las pruebas del módulo antes de implementarlo | `evidencias/reportes/phpunit-reportes-RED.log` | 09/11/2026 | 12 failed (ruta inexistente) |
| EV-REP-02 | 5.2 | GREEN de las pruebas del módulo | `evidencias/reportes/phpunit-reportes-GREEN.log` | 09/11/2026 | 12 passed (209 aserciones) |
| EV-REP-03 | 5.2 | Cypress e2e-20 (ejecución que produjo las capturas) | `evidencias/reportes/cypress-e2e20-reportes.log` | 09/11/2026 | 9/9 |
| EV-REP-04 | 5.2 | Captura: RR. HH. de la organización A, KPI, gráficos y tabla con datos de la BD | `evidencias/reportes/E2E-20-01-reportes-rrhh-organizacion-a.png` | 09/11/2026 | 9 postulaciones, 88,9 % |
| EV-REP-05 | 5.2 | Captura: filtro por vacante aplicado | `evidencias/reportes/E2E-20-02-filtro-por-vacante.png` | 09/11/2026 | 3 postulaciones, 1 fila |
| EV-REP-06 | 5.2 | Captura: organización B (tenant B) | `evidencias/reportes/E2E-20-06-reportes-organizacion-b.png` | 09/11/2026 | 1 postulación, solo su vacante |
| EV-REP-07 | 5.2 | Captura: Aprobador en móvil (390 px) | `evidencias/reportes/E2E-20-09-reportes-aprobador-movil.png` | 09/11/2026 | Sin desplazamiento horizontal; KPI 9 (tras la preselección del escenario 5) |

Nota sobre las capturas `fullPage` de Cypress: al unir varias pantallas, Cypress repite los elementos fijos (barra lateral y encabezado) en cada tramo. Es un efecto conocido de la captura, no de la aplicación.

## Impacto

| ID | Actividad | Descripción | Archivo | Fecha | Resultado |
|---|---|---|---|---|---|
| EV-IMP-01 | 5.3 | Resultados medidos M-1 a M-7, con referencia a EV-REP y a las pruebas | `reportes/IMPACTO_FUNCIONAL.md` §6 | 09/11/2026 | Solo hechos verificados |
| EV-IMP-02 | 5.3 | Fuente del problema y del límite P5 (sin modificar) | `docs/final-report/02-contexto-problema.md` §2.2–2.3 | v1.0 | Referencia |

En la auditoría Codex se creó `evidencias/arquitectura/` para la captura real del IDE. Los diagramas no se duplicaron ni se alteraron los 16 históricos. El impacto sigue sustentado con EV-REP y pruebas, sin captura artificial adicional.

**Totales finales: 32 registros principales, 32 disponibles y 0 pendientes**. EV-SON-06 agrupa 7 capturas UI, sin contarlas otra vez como registros principales. Hay **16 imágenes** en esta fase: 8 PNG recibidos y preservados + 8 JPEG nativos (7 Sonar UI + 1 IDE). Los registros y ficheros son unidades diferentes; EV-COD-01 agrupa las salidas de auditoría.

## Verificación independiente y cierre de las evidencias faltantes

| ID | Actividad | Descripción | Archivo | Fecha | Resultado |
|---|---|---|---|---|---|
| EV-TEC-07 | 2.3 | Captura real de VS Code con estructura del SaaS y servicio de Reportes | `evidencias/arquitectura/ARQ-TECH-09_IDE_VSCode.jpg` | 09/11/2026 | Disponible; cierra ARQ-TECH-09 |
| EV-COD-01 | Todas | Comandos, regresiones, análisis Sonar y validación de integridad independientes | `evidencias/codex/` y `AUDITORIA_CODEX.md` | 09/11/2026 | PHPUnit 426+8, Vitest 54, Cypress 94, Gate OK evaluado; deuda histórica declarada |

### Subinventario EV-SON-06 (capturas nativas, sin edición)

| ID UI | Archivo relativo a evidencias/sonarqube | Contenido visible |
|---|---|---|
| SONAR-UI-01 | `SONAR-UI-01_Proyecto.jpg` | Proyecto, Passed y resumen de código nuevo |
| SONAR-UI-02 | `SONAR-UI-02_Quality_Gate.jpg` | Passed, condición 85,0 % ≥ 80 %, 0 issues, duplicación 0,0 % ≤ 3 % |
| SONAR-UI-03 | `SONAR-UI-03_Metricas_Globales.jpg` | Overall Code, MQR 0 en seguridad/fiabilidad/mantenibilidad, cobertura 70,3 % |
| SONAR-UI-04 | `SONAR-UI-04_Coverage.jpg` | Measures, cobertura global 70,3 %, nueva 85,0 %, 220 líneas y 33 sin cubrir, TS visible sin cobertura |
| SONAR-UI-05 | `SONAR-UI-05_Issues.jpg` | Issues abiertos 0; categorías y severidades en MQR |
| SONAR-UI-06 | `SONAR-UI-06_Security_Hotspots.jpg` | Sin hotspots para revisar y aviso de concepto deprecado en esta versión |
| SONAR-UI-07 | `SONAR-UI-07_Limitaciones_Seguridad.jpg` | Aviso de alcance limitado de seguridad de Community Build y H2 de evaluación |

La UI está en **MQR mode**: no se etiqueta su pantalla como si mostrara los tres contadores tradicionales. Bugs, Vulnerabilities y Code Smells se contrastan con la API (todos 0). Una captura no prueba aquello que no se ve: el 90,1 % de `app/` se sustenta en `evidencias/codex/sonar-final.json`, no en una cifra inventada dentro de una imagen.

Las capturas son reales y locales, tomadas sobre el mismo proyecto después del análisis `ff71984c-9177-40eb-b244-0468a15bbdf2`. No se borró evidencia recibida. Los originales DOCX/PDF de las guías, las capturas V1/V2 y los 16 diagramas anteriores permanecen intactos.

**Formato de captura:** la API nativa entregó JPEG; se usa la extensión `.jpg` correspondiente. Se conservan sus bytes y resolución originales, sin conversión, compresión adicional ni edición. Los PNG recibidos no se modificaron.
