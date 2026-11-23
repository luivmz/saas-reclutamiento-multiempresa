# Resultados de la ejecución de Cypress

> Actividad 3.4. Ejecuciones **reales** del 09/11/2026 con `npm run cy:run` (Cypress 15.3.0, Electron 136 headless, contenedor `cypress/included:15.3.0`) sobre la app aislada `app-e2e` (base `reclutamiento_e2e`). Porcentaje de aprobación = aprobadas ÷ ejecutadas × 100.

## 1. Verificación de la herramienta

`cypress verify` dentro de la imagen oficial: **COMPLETED**. `cypress version`: paquete 15.3.0, binario 15.3.0, Electron 36.8.1, Node incluido 22.18.0 ([log](../evidencias/cypress/cypress-verify-version.log)). Se utilizó el Cypress de la imagen oficial del proyecto; no se necesitó ni se reinstaló una instalación independiente del host.

## 2. Totales

| Ejecución | Momento | Specs | Pruebas | Aprobadas | Fallidas | Pendientes | Omitidas | % aprobación | Duración (Cypress) |
|---|---|---|---|---|---|---|---|---|---|
| **1: suite completa** (con el módulo nuevo y antes de corregir las pruebas) | 09/11/2026 ~21:28 (Lima) | 21 (19 ✔, 2 ✖) | 94 | **87** | **7** | 0 | 0 | **92,55 %** | 02:26 |
| **2: suite completa (final)**, tras corregir DEF-14 y DEF-15 | 09/11/2026 ~21:35–21:44 | 21 (21 ✔) | 94 | **94** | **0** | 0 | 0 | **100 %** | 08:33 (8:52 de reloj, incluida la preparación) |
| Verificación dirigida: e2e-16 + e2e-17 | entre 1 y 2 | 2 | 15 | 15 | 0 | 0 | 0 | 100 % | 00:11 |
| Re-verificación: e2e-03 | después de 2 | 1 | 2 | 2 | 0 | 0 | 0 | 100 % | 00:04 |
| Evidencia del módulo: e2e-20 **sobre el bundle final** (ver nota) | después de 2 | 1 | 9 | 9 | 0 | 0 | 0 | 100 % | 00:13 |

**Nota de trazabilidad del bundle.** Las ejecuciones completas 1 y 2 usaron los assets compilados a las 21:26. Un minuto después, la lógica pura de la página de reportes se movió a `resources/js/lib/reports.ts` para probarla con Vitest, sin cambiar su comportamiento. Para que la evidencia corresponda al código final se recompiló (`npm run build`) y se volvió a ejecutar `e2e-20-reports` sobre el bundle definitivo: 9/9. El resto de specs no carga esa página.

Logs: [ejecución 1](../evidencias/cypress/cypress-ejecucion-1-completa.log) · [ejecución 2](../evidencias/cypress/cypress-ejecucion-2-completa.log) · [e2e-16/17](../evidencias/cypress/cypress-verificacion-e2e16-e2e17.log) · [e2e-03](../evidencias/cypress/cypress-reverificacion-e2e03.log) · [e2e-20](../evidencias/reportes/cypress-e2e20-reportes.log). Capturas del resumen: [ejecución 1](../evidencias/cypress/CYP_ejecucion1_resumen_terminal.png) y [ejecución 2](../evidencias/cypress/CYP_ejecucion2_resumen_terminal.png).

### Detalle por spec (ejecución 2, final)

| Spec | Pruebas | Aprobadas | Duración |
|---|---|---|---|
| e2e-00-app-dates | 3 | 3 | 64 ms |
| e2e-01-login | 6 | 6 | 00:07 |
| e2e-02-register-job-request | 2 | 2 | 00:06 |
| e2e-03-approve-job-request | 2 | 2 | 05:27 (ver §3.3) |
| e2e-04-configure-publish-vacancy | 2 | 2 | 00:08 |
| e2e-05-candidate-apply | 1 | 1 | 00:04 |
| e2e-06-shortlist-candidate | 2 | 2 | 00:05 |
| e2e-07-evaluator-records-results | 1 | 1 | 00:03 |
| e2e-08-comparison-ranking | 1 | 1 | 00:02 |
| e2e-09-human-final-decision | 2 | 2 | 00:04 |
| e2e-10-selection-and-closure | 1 | 1 | 00:08 |
| e2e-11-multitenancy | 4 | 4 | 00:06 |
| e2e-12-negative-rules | 4 | 4 | 00:08 |
| e2e-13-full-recruitment-flow | 12 | 12 | 01:11 |
| e2e-14-target-completion-form | 4 | 4 | 00:07 |
| e2e-15-operational-risk-panel | 8 | 8 | 00:10 |
| e2e-16-tabla-accesible-movil | 7 | 7 | 00:06 |
| e2e-17-motion-accesible | 8 | 8 | 00:04 |
| e2e-18-profundidad-portada | 8 | 8 | 00:01 |
| e2e-19-qa-visual-accesible | 7 | 7 | 00:03 |
| **e2e-20-reports (nuevo)** | **9** | **9** | 00:13 |
| **Total** | **94** | **94** | **08:33** |

Antes de esta práctica, la última ejecución documentada de la suite eran **85/85** (histórico); en la sesión Sonar del 20/10 Cypress figuraba como «NO EJECUTADO». Las 94 de hoy son 85 + 9 del spec nuevo.

## 3. Errores encontrados y análisis

### 3.1 DEF-14: `e2e-16` desalineado con `DataTable` (6 fallas, ejecución 1)

- **Síntoma**: `AssertionError: expected null to equal 'cell'` en 6 de las 7 pruebas (requerimientos, vacantes, postulaciones, ranking, auditoría y evaluaciones).
- **Causa**: el commit `a88cd3c` corrigió el hallazgo Sonar `typescript:S6843` y quitó el `role="cell"` explícito de las celdas de `DataTable`, dejando el rol nativo de `<td>`. El spec seguía exigiendo el atributo. Como la suite no se ejecutó en aquella sesión, la incoherencia quedó latente.
- **¿Funcionalidad con problemas?** No. La semántica de tabla se mantiene (`role="table"`, `rowgroup`, `row`, `columnheader`, `headers` por celda); la falla estaba en la **prueba**.
- **Corrección**: la aserción ahora exige que la celda sea `TD` y que no tenga otro rol (`role` ausente o `cell`), conforme al contrato documentado en `data-table.tsx`. Resultado: 7/7.
- **Lección**: una corrección de análisis estático que toca marcado accesible debe volver a pasar por la suite E2E; SonarQube y Cypress se complementan.

### 3.2 DEF-15: `e2e-17` frágil ante una nueva entrada de menú (1 falla, ejecución 1)

- **Síntoma**: «la navegación móvil se abre, se cierra con Escape…» fallaba con `cy.type() failed because it requires a valid typeable element`; la captura mostraba la página `/empleos`.
- **Causa**: `cy.get('[data-mobile="true"]').type('{esc}')` **hace clic en el centro** del panel antes de escribir. Con la nueva entrada «Reportes», ese centro pasó a ser el enlace «Empleos publicados»: la app navegaba y el panel desaparecía. El cambio de contenido es legítimo; la prueba dependía de la geometría.
- **Corrección**: `cy.get('body').type('{esc}')` entrega Escape al elemento enfocado (dentro del panel) sin hacer clic. Se conservan las aserciones de cierre y de devolución del foco. Resultado: 8/8.

### 3.3 Duración atípica en `e2e-03` (sin falla)

En la ejecución 2, «no permite rechazar sin indicar el motivo» **aprobó** pero tardó 324,7 s; en la ejecución 1 la misma prueba tardó segundos, y en una re-ejecución aislada, 1,07 s. No se reprodujo. Coincidió con actividad paralela en el host (comandos `docker compose exec` y renders de Chrome headless para los diagramas), pero **no hay telemetría que demuestre causalidad**. La contención de recursos es una hipótesis, no un diagnóstico confirmado. Si reaparece, deberá investigarse (la configuración `retries: 0` lo haría visible).

### 3.4 Capturas de las fallas de la ejecución 1

Cypress guardó capturas automáticas de las 7 fallas, pero la opción por defecto `trashAssetsBeforeRuns` vació `cypress/screenshots/` al iniciar las ejecuciones siguientes. Se conservan los **logs completos** con el mensaje y la traza de cada falla; la descripción de la captura de DEF-15 (página `/empleos`) se registró al analizarla.

## 4. Conclusión

La suite final aprueba **94 de 94 (100 %)** en 21 specs. El spec nuevo del módulo de reportes aprueba 9/9 en todas sus ejecuciones. Los dos errores encontrados estaban en **pruebas** existentes (uno por deuda de una corrección Sonar previa y otro por fragilidad ante el nuevo menú), no en funcionalidades de la aplicación; ambos se corrigieron y registraron como DEF-14 y DEF-15 en [`docs/defects.md`](../../defects.md).

## 5. Reauditoría independiente de Codex

Las ejecuciones históricas anteriores se conservan. Se volvió a verificar el binario sin reinstalarlo (`npx --no-install cypress version` y `npx --no-install cypress verify` dentro de la imagen oficial) y se repitió **toda la suite sobre el bundle final**, también después de la corrección PHPDoc del servicio:

| Ejecución Codex | Specs | Total | Aprobadas | Fallidas | Omitidas/pendientes | Aprobación | Duración Cypress | Reloj con preparación |
|---|---|---|---|---|---|---|---|---|
| Estado recibido | 21 | 94 | 94 | 0 | 0 | 100 % | 02:46 | 185,426 s |
| **Regresión final** | **21** | **94** | **94** | **0** | **0** | **100 %** | **02:37** | **175,770 s** |

Comando final real: `docker compose --profile e2e run --rm --no-deps cypress`, con `app-e2e` y `queue-e2e` ya saludables, `.env.e2e` local y BD descartable **reclutamiento_e2e**, nunca `reclutamiento`.

Evidencias: [`cypress-final.log`](../evidencias/codex/cypress-final.log), [metadatos de comando y duración](../evidencias/codex/cypress-final.json), [`cypress-received.log`](../evidencias/codex/cypress-received.log), [`cypress-verify.log`](../evidencias/codex/cypress-verify.log).

### Comprobaciones de los specs críticos

- **e2e-16: 7/7**. Se mantuvieron las comprobaciones de tabla, filas, encabezados, asociaciones `headers`, desbordamiento y celda `TD` sin un rol incompatible. El rol implícito de `td` es válido; comprobar un atributo ausente no sustituye una prueba con lector de pantalla. Referencia: [HTML-ARIA, elemento td](https://www.w3.org/TR/html-aria/#el-td).
- **e2e-17: 8/8**. Enviar Escape a `body` conserva las comprobaciones de cierre y foco y evita el clic geométrico sobre un enlace del panel. La corrección coincide con el comportamiento documentado de [Cypress `.type()`](https://docs.cypress.io/api/commands/type).
- **e2e-20: 9/9**. Verifica KPI contra la BD, filtros, estado vacío, cambio de preselección **8 → 9**, organizaciones A/B, rechazo de vacante ajena, roles y móvil. No se redujo a texto estático.
- **e2e-03: 2/2**, spec completo en 4 s en la regresión final; la prueba negativa tardó **1251 ms** (1462 ms en la primera corrida Codex). Los 324 s históricos **no se reprodujeron** en dos suites nuevas. Sin retries, llamadas externas ni espera fija que explique esa duración. El timeout de 120 s del reset es un límite, no una espera obligatoria.
- Sin `it.only`, `describe.only`, `context.only` ni instrucciones `debugger`. La espera de 250 ms del comando de cola es sondeo de una condición real, con límite. Hay esperas fijas en `cypress/visual/`, **fuera del specPattern de esta suite formal**; quedan como deuda auxiliar, sin reescribir los 21 specs.

Las capturas nuevas del IDE y Sonar provienen de UI nativa. Las dos imágenes históricas de resumen de Cypress son renderizados de salidas reales, no capturas del Cypress Runner; esta diferencia se mantiene explícita.
