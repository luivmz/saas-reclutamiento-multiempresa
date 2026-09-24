# Progreso del proyecto

Última actualización: 2026-09-24 (Fase 24, pendiente de auditoría).

> El 24/09/2026 la cabecera pasó de «2026-09-23 (hotfix documental de la Fase 21)» a la Fase 23, y ese mismo día, de la Fase 23 a la Fase 24. Hasta el 23/09/2026 decía «Última actualización: 2026-09-13 · Rama actual: `release/qa-final`», que era el estado al cerrar la Fase 12. Las secciones de v1.0 que siguen a la tabla de v1.1 se conservan tal como se escribieron.

## Estado de v1.1

`main` sigue siendo la v1.0 académica (`4563c69`, tag `v1.0.0-academic` en `9a946c2`) y no contiene v1.1. `develop` = `origin/develop` = `8211851` *(hasta la Fase 24: `2621bee`)*.

| Fase | Contenido | Estado | Merge en `develop` | Detalle |
|---|---|---|---|---|
| 13 | Gobierno de v1.1 | ✅ Integrada | `95c5b8b` | `docs/v1.1/phase-13-master-plan.md` |
| 14 | Definición del experimento de ML | ✅ Integrada | `5957fd4` | `docs/v1.1/phase-14-ml-definition.md` |
| 14.5 | Gobierno multiagente | ✅ Integrada | `d02cbc9` | `docs/v1.1/multi-agent-workflow.md` |
| 15 | Servicio ML: datos sintéticos, entrenamiento, FastAPI experimental | ✅ Integrada | `485f0e1` | `docs/v1.1/phase-15-closeout.md` |
| 16 | Integración Laravel ↔ FastAPI (GAP-01 resuelto técnicamente) | ✅ Integrada | `e3e7540` | `docs/v1.1/phase-16-laravel-ml-integration.md` |
| 17 | Validación ML y regresión integral | ✅ Integrada | `0d2ce42` | `docs/v1.1/phase-17-ml-validation.md` |
| 18 | Rediseño del frontend | ✅ Integrada | `11832ac` | `docs/v1.1/phase-18-frontend-redesign.md` |
| 19 | Animaciones y microinteracciones | ✅ Integrada | `67a88a6` | `docs/v1.1/phase-19-animations.md` |
| 20 | Experiencia 3D con CSS 3D (solo portada) | ✅ Cerrada e integrada | `a316c07` | `docs/v1.1/phase-20-3d-experience.md` |
| 21 | QA visual, accesibilidad y responsive | ✅ Cerrada e integrada | `aced6da` | `docs/v1.1/phase-21-visual-qa.md` |
| 22 | Especificación UML del AS-IS | ✅ Integrada | `2621bee` | `docs/v1.1/phase-22-uml-update.md` |
| 23 | Formalización en PowerDesigner | ✅ Integrada | `8211851` | `docs/v1.1/phase-23-powerdesigner.md` |
| 24 | Documentación académica final: Formato 09 v1.1 | 🟡 Implementada en `feature/phase-24-academic-documentation`, pendiente de auditoría | — | `docs/v1.1/phase-24-academic-documentation.md` |
| 25 | QA global final | ⬜ No iniciada | — | — |
| 26 | GitHub, *release* y cierre de v1.1 | ⬜ No iniciada | — | — |

**RF-29** está implementado e integrado **experimentalmente**: validado técnicamente con datos sintéticos, no validado institucionalmente ni autorizado para producción; no selecciona ni descarta a nadie y no cambia RF-23. RF-28, RF-29 y los RNF nuevos (incluido RNF-C) siguen siendo **candidatos** (`docs/v1.1/scope-preliminary.md`, decisión 11 y preguntas 12–13).

Las entradas por fase de v1.1 que siguen al final de este documento empiezan en la Fase 18; las Fases 13 a 17 se documentaron en sus propios archivos, enlazados en la tabla.

## Fases (v1.0)

| Fase | Estado |
|---|---|
| 0 a 10 | ✅ Completadas e integradas en `develop` |
| 11 — Documentación final | ✅ Integrada en `develop` (`904ce72`, merge `--no-ff` de `49b7f33`) |
| 12 — QA final y auditoría de entrega | ✅ Completada en `release/qa-final` (**pendiente de revisión humana**) — veredicto: **APTO PARA PUBLICACIÓN** |
| Cierre Git + publicación en GitHub | ❌ Pendiente, bajo revisión humana |

**RF-01 a RF-27 constituyen la línea base funcional completa.** La Fase 12 no cambió código, configuración, reglas de negocio ni RF: solo documentación.

## Reglas de negocio vigentes (aprobadas; sin cambios)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras la decisión final, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 12 — resultados reales del QA final

| Verificación | Resultado |
|---|---|
| RF-01 a RF-27 | 27/27 ✅ (rutas, código, Policies, páginas, PHPUnit y Cypress verificados) |
| PHPUnit | 244 pruebas · 236 passed · **0 failed** · 8 skipped · 1074 assertions · 32,25 s |
| Cypress | 14 specs · 43/43 · **0 failed** · 0 skipped · 03:32 · Electron 136 |
| `npm run build` | Correcto |
| `npx tsc --noEmit` | 0 errores |
| Migraciones | 17 aplicadas, 0 pendientes (normal y E2E) |
| Datos demo | 2 organizaciones, 16 usuarios `.test`, 7 CV PDF ficticios |
| Smoke | `/health` 200 (base de datos y Redis ok), `/login` 200, `/empleos` 200, `/dashboard` → login sin sesión, `/__e2e/reset` 404 en el entorno normal |
| *Healthchecks* | `app`, `queue`, `postgres`, `redis`, `app-e2e` y `queue-e2e` *healthy* |
| Secretos | Ninguno versionado (`.env`, `.env.e2e`, logs, *dumps*, CV privados: 0) |
| Defectos nuevos | Ninguno |

## Documentos creados o actualizados en la Fase 12

- `docs/final-report/diagram-reports/01` a `09`: informes escritos de los diagramas (sin recrear gráficos ni editar los `.oom`).
- `docs/final-report/delivery-checklist.md` (con «GitHub publicado» sin marcar).
- `docs/final-report/qa-final-report.md` (veredicto y justificación).
- Resultados del QA final en los capítulos 12 y 13 y en `docs/testing/cypress-e2e.md`.
- Referencias con fecha de consulta (13 de septiembre de 2026).
- Enlaces a los informes de diagramas en `evidence-index.md` y en los capítulos 6 y 14.
- Estado del README.

## Pendientes (equipo)

1. Anexar los BPMN AS-IS y TO-BE originales y los documentos previos de casos de uso.
2. Seleccionar o recapturar las capturas del informe, incluidas Cypress y Docker.
3. Actualizar gráficamente los diagramas de selección y despliegue (opcional).

## Git

- Rama: `release/qa-final` (desde `develop` en `904ce72`). Ramas `main`, `develop` y `feature/*` preservadas.
- Sin remoto, sin push, sin *tag*, sin merge a `main`.

## Siguiente paso (bajo revisión humana)

Cierre Git y publicación en GitHub:
1. Integrar `release/qa-final` en `develop` y luego en `main`.
2. Crear el *tag* de versión.
3. Crear el remoto y hacer `push`.

## Publicación (completada)

Repositorio publicado en https://github.com/luivmz/saas-reclutamiento-multiempresa: `main` (rama por defecto), `develop`, `release/qa-final` y las 10 ramas `feature/*`, más el tag `v1.0.0-academic` (`9a946c2`).

## Post-publicación — Corrección CI GitHub Actions

- **Problema:** el workflow heredado `.github/workflows/tests.yml` fallaba en GitHub Actions durante `composer install`.
- **Causa:** usaba PHP 8.3, mientras Symfony 8.1 (bloqueado en `composer.lock`) requiere PHP ≥ 8.4.1. Además, ejecutaba comandos del *starter kit* (`composer setup`, `composer ci:check`: PHPStan, Pint, *lint*) ajenos a la validación del proyecto. Por separado, `composer.lock` tenía un `content-hash` desincronizado desde el *bootstrap*.
- **Solución:**
  - Workflow con PHP 8.4, Node 22.23.2 y PostgreSQL 17.11.
  - Pasos: `composer install`, `npm ci`, `npm run build`, `npx tsc --noEmit` y `php artisan test`, con variables ficticias de CI y sin Redis (no requerido).
  - `composer update --lock`: solo cambió el `content-hash`, sin variar versiones.
  - Rama `fix/github-actions-ci`, commit `05e6fb1`; merges `c83f232` (`main`) y `7b1b7ef` (`develop`).
- **Workflow verde:** ejecuciones `34787563815` (rama de corrección), `34787861775` (`main`) y `34787885835` (`develop`), todas **success**.
- **Sin cambios funcionales:** no cambiaron RF, reglas, código de la aplicación ni Docker. El tag `v1.0.0-academic` se conserva.
- **Detalle:** `docs/final-report/post-publication-ci-fix.md`.

## v1.1 — Fase 18: rediseño frontend integral

- **Rama:** `feature/phase-18-frontend-redesign`, desde `develop` en `0d2ce42` (cierre de la Fase 17).
- **Alcance:** solo interfaz. Sistema de diseño propio (tipografía IBM Plex, tokens de estado, barra lateral oscura), `DataTable` y `Section` reutilizables, accesibilidad (enlace de salto, foco visible único, `aria-current`/`aria-pressed`, tablas con `scope` y `caption`), responsive verificado a 1440/1280/768/390 px, modo oscuro y traducción al español del módulo de configuración.
- **Sin cambios** en reglas de negocio, RF, rutas, contratos de API, modelos, Policies, migraciones ni servicio ML. RF-29 sigue siendo experimental y la decisión final sigue siendo humana (RF-23).
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 18 pruebas de componente (`vp test`) · `tsc` sin errores · `npm run build` correcto · Cypress 17 specs / 61 pruebas, 61 pasadas.
- **Detalle y evidencia:** `docs/v1.1/phase-18-frontend-redesign.md` y `docs/v1.1/phase-18-screenshots/`.
- **Sin `push`, `merge`, *tag* ni *release*.**

## v1.1 — Fase 19: animaciones y microinteracciones

- **Rama:** `feature/phase-19-animations`, desde `develop` en `11832ac` (cierre de la Fase 18).
- **Alcance:** solo movimiento. Sistema de tres curvas y una escala de duración declarado con los tokens que Tailwind ya usa; corrección del movimiento heredado del kit de inicio (curvas lineales, `transition-all`, 500 ms de apertura, menús creciendo desde el centro); respuesta del botón a la pulsación; entrada de errores de formulario y del resultado de riesgo operacional. **Sin biblioteca de motion nueva.**
- **Se anima poco a propósito:** sin transiciones entre páginas, sin entrada animada de filas de tabla, sin contadores y sin badges que laten.
- **`prefers-reduced-motion` implementado y probado:** se conservan color y opacidad, se elimina todo desplazamiento, el spinner sigue girando y el esqueleto deja de latir.
- **Defecto de accesibilidad encontrado y corregido:** al cerrar la navegación móvil el foco se perdía en `body`; ahora vuelve al botón que la abrió.
- **Sin cambios** en reglas de negocio, RF, rutas, contratos de API, modelos, Policies, migraciones ni servicio ML.
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 23 pruebas de componente · `tsc` sin errores · `npm run build` correcto · Cypress 18 specs / 69 pruebas · 0 desbordes horizontales.
- **Detalle:** `docs/v1.1/phase-19-animations.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**

## v1.1 — Fase 20: experiencia 3D contextual

- **Rama:** `feature/phase-20-3d-experience`, desde `develop` en `67a88a6` (cierre de la Fase 19).
- **Alcance:** una sola superficie, la portada pública. Detrás del expediente de la portada, una pila de hojas en perspectiva, cada una con el tono de su etapa. Decorativa, opcional y sin información propia (ADR-003).
- **Tecnología:** CSS 3D (perspectiva y capas de DOM), **sin WebGL y sin dependencias nuevas**. `package.json` no cambia.
- **Presupuesto:** *bundle* inicial JS **+0 KB**; la escena va en su propio fragmento diferido (1.26 kB gzip) que solo se descarga en escritorio, sin movimiento reducido ni ahorro de datos, y al entrar en el viewport. 61 FPS con el puntero en movimiento; escena lista en ≈ 500 ms.
- **Fallback:** póster estático con la misma idea en plano, visible al instante; queda con movimiento reducido, en móvil, con ahorro de datos, en equipos modestos o si el fragmento falla. Sin WebGL la escena se muestra igual.
- **Gobierno:** ADR-003 y RNF-C seguían «pendiente de decisión»; se anotaron sin reescribir su historia. La promoción formal de RNF-C sigue siendo decisión del equipo.
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 36 pruebas de componente · `tsc` sin errores · `npm run build` correcto · Cypress 19 specs / 77 pruebas · 0 desbordes horizontales.
- **Detalle:** `docs/v1.1/phase-20-3d-experience.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**

## v1.1 — Fase 21: QA visual, accesibilidad, responsive y pulido final

- **Rama:** `feature/phase-21-visual-qa`, desde `develop` en `a316c07` (cierre de la Fase 20).
- **Alcance:** auditoría y corrección del frontend consolidado tras las Fases 18 a 20, sin rediseño ni funciones nuevas. 35 rutas y las sesiones de evaluación de los seis perfiles, en claro y oscuro, a 1440/1280/1024/768/390/320 px, con teclado, movimiento reducido y estados provocados (rechazo, errores, 2FA real).
- **Defectos corregidos:** alertas destructivas ilegibles en claro (≈ 1:1, **alta**; afectaba al motivo de rechazo de RF-04); rojo destructivo en oscuro por debajo de 4.5:1 como botón y como texto de error; pantallas de acceso sin `main`; cabecera pública desbordada a 320 px (WCAG 1.4.10); franja visible de los códigos de recuperación plegados (regresión de la Fase 19); enlace de salto de 22 px; botones de 2FA fuera de su tarjeta a 1024 px; desplazamiento suave que ignoraba el movimiento reducido.
- **Aceptado con evidencia:** animación de ancho de la barra lateral (0 cuadros de 50 ms o más); 27 objetivos pequeños que cumplen WCAG 2.5.8 por espaciado. **Pasan a F24/F25:** lector de pantalla real y rendimiento en equipo modesto.
- **Gobierno:** RNF-C queda como propuesta (pregunta 13 de `scope-preliminary.md`), no aprobada; skill `recruitment-3d-experience` actualizada a «implementada y acotada»; ~~`CLAUDE.md` sin tocar hasta la integración en `main`~~ *(decisión inicial de la fase, ya no vigente: el hotfix documental del 23/09/2026 corrigió `CLAUDE.md` al estado real a pedido de la auditoría de Codex)*.
- **Sin cambios** en backend, reglas de negocio, RF, rutas, contratos de API, modelos, Policies, migraciones ni servicio ML. No se adelantó la Fase 22.
- **Regresión ejecutada:** Laravel 408 pasadas + 8 omitidas · Python 532 pasadas · 42 pruebas de componente · `tsc` sin errores · `npm run build` correcto · Cypress 20 specs / 84 pruebas · 0 desbordes horizontales.
- **Detalle y evidencia:** `docs/v1.1/phase-21-visual-qa.md` y `docs/v1.1/phase-21-screenshots/`.
- **Auditoría de Codex:** técnicamente en verde; pidió un hotfix documental (`CLAUDE.md` desactualizado, redacción de WebGL en la skill 3D, cifra del CSS). Hecho el 23/09/2026 en la misma rama, solo documentación y skills. La reauditoría pidió un hotfix final (estado vigente en `scope-preliminary.md`, contrato real en la skill `ml-risk-service`, esta entrada), también solo documental. **La fase no está cerrada** hasta la nueva reauditoría.
- **Cierre:** tras la reauditoría, integrada en `develop` con el merge `aced6da`. *(Anotado en la Fase 22.)*
- **Sin `push`, `merge`, *tag* ni *release*.**

## v1.1 — Fase 22: especificación UML del AS-IS

- **Rama:** `feature/phase-22-uml-update`, desde `develop` en `aced6da` (cierre de la Fase 21).
- **Alcance:** solo documentación. Especificación verificable de los diagramas UML del sistema implementado, en `docs/v1.1/uml/`: inventario, casos de uso (RF-01 a RF-29), clases del dominio (17 clases, 37 asociaciones), componentes y paquetes, despliegue, 8 secuencias, 2 actividades, 4 máquinas de estado, matriz de trazabilidad y guía para PowerDesigner. 19 borradores PlantUML, no renderizados.
- **Hallazgos del cruce con el código:** RF-28 es un candidato no implementado (el estado `descriptive_only` de RF-29 no es su panel); el cierre `desierta` no tiene flujo; la descripción OpenAPI de `days_remaining_to_target` quedó obsoleta (GAP-01 está resuelto).
- **Sin cambios** en código, pruebas, dependencias ni servicio ML. **Sin archivos de PowerDesigner**: son de la Fase 23, que no se inició. No se ejecutaron suites funcionales: el cambio es documental.
- **Auditoría de Codex:** tres correcciones de UML (`scheduled_by` en CL-01, descarte terminal en AC-01, UC-RF07 solo de RR. HH.), hechas en la misma rama; pendiente de reauditoría.
- **Detalle:** `docs/v1.1/phase-22-uml-update.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**
- **Cierre:** tras la reauditoría, integrada en `develop` con el merge `2621bee`. *(Anotado en la Fase 23.)*

## v1.1 — Fase 23: formalización en PowerDesigner

- **Rama:** `feature/phase-23-powerdesigner`, desde `develop` en `2621bee` (cierre de la Fase 22).
- **Alcance:** modelos nativos de PowerDesigner 16.6.1.5066 en `docs/v1.1/powerdesigner/`, construidos por su interfaz COM con scripts versionados. OOM con los 19 diagramas de F22 (CL-01, UC-01, PK-01, CO-01, DE-01, SEQ-01 a SEQ-08, AC-01, AC-02, ST-01 a ST-04) más la vista CL-01b; PDM por ingeniería inversa del esquema real (27 tablas, 48 FK, 32 CHECK) con PDM-01 y PDM-02. 22 diagramas exportados en PNG y SVG.
- **Validación:** revisión visual de cada exportación y conteo de elementos contra F22 (125 mensajes, 20 fragmentos, 19 estados, 37 transiciones…), sin diferencias de contenido; las de representación están justificadas en `powerdesigner/f22-checklist.md`. RF-23 humano, RF-28 candidato sin asociaciones, RF-29 experimental. Los modelos, tal como quedan en Git, abren en PowerDesigner.
- **Sin cambios** en código, pruebas, dependencias ni servicio ML; no se ejecutaron suites funcionales. La deuda de texto OpenAPI de GAP-01 (`schemas.py`) se registra, no se corrige.
- **Proceso:** dos sesiones; la primera se detuvo en un *checkpoint* sin commits y la segunda la reanudó sin reconstruir.
- **Detalle:** `docs/v1.1/phase-23-powerdesigner.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**
- **Cierre:** tras la auditoría, integrada en `develop` con el merge `8211851`. *(Anotado en la Fase 24.)*

## v1.1 — Fase 24: documentación académica final (Formato 09)

- **Rama:** `feature/phase-24-academic-documentation`, desde `develop` en `8211851` (cierre de la Fase 23).
- **Alcance:** solo documentación. Formato 09 v1.1 en `docs/academico/phase-24/output/` (DOCX y PDF exportado por Word, 28 páginas), construido a partir del F9 histórico del equipo con la guía y la plantilla oficiales como referencia. Los tres originales se versionaron sin cambios.
- **Correcciones:** NRC 30180 → **28607**; campos oficiales que faltaban (usuarios principales, entorno de uso, módulo/sistema, destino de las salidas, los cuatro criterios de aceptación); afirmaciones de ML obsoletas («Laravel todavía no lo consume», «GAP-01 permanece abierto») reemplazadas por la integración experimental vigente; anexos de casos de uso y de arquitectura con actores y servicios fuera del alcance sustituidos por UC-01 y CO-01 de PowerDesigner, más DE-01, AC-01 y CL-01.
- **Contratos:** RF-01 a RF-27 siguen siendo la línea base oficial; RF-28 (no implementado), RF-29 (experimental) y RNF-C (propuesta) figuran como candidatos, sin promoción; RF-23, decisión humana.
- **Observaciones:** los catálogos de CU (20 académicos, 13 del informe y uno por RF en el UML) y de RNF (10 frente a 11) divergen; se declaran y quedan para decisión del equipo.
- **Validación:** documental y estructural (`tools/validate_f9.py` sin fallos; índice verificado contra el PDF; originales con el mismo SHA-256). **No se ejecutaron suites funcionales**: el QA global es de la Fase 25.
- **Detalle:** `docs/v1.1/phase-24-academic-documentation.md`, `docs/academico/phase-24/README.md` y `source-map.md`.
- **Sin `push`, `merge`, *tag* ni *release*.**
