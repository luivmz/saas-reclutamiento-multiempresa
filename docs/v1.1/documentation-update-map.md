# Mapa de actualización documental para v1.1

Este documento **señala** qué documentación habría que revisar si v1.1 avanza. En la Fase 13 **no se modificó ningún documento histórico**: la regla es marcar la divergencia aquí, nunca reescribir el pasado en silencio.

Alcance de la revisión realizada: se inventariaron los 40 documentos existentes y se verificó su presencia y estructura. **No** se hizo una relectura línea por línea de cada uno en busca de contradicciones; lo que sigue distingue lo verificado de lo que queda por verificar.

## 1. Divergencias verificadas

| Documento | Sección | Divergencia | Acción propuesta |
|---|---|---|---|
| `docs/PROGRESS.md` | Estado general | Describe el proyecto cerrado en la Fase 12 más la corrección de CI. La Fase 13 abre v1.1 y no está reflejada. | Añadir la Fase 13 como entrada nueva al final, sin alterar las anteriores |
| `docs/final-report/delivery-checklist.md` · `qa-final-report.md` | Cierre | Declaran el cierre de v1.0. Siguen siendo correctos **para v1.0**. | No tocar. v1.1 tendrá sus propios documentos de cierre |
| `README.md` | Estado del proyecto | No menciona `CLAUDE.md` ni las skills del proyecto | Añadir un enlace breve cuando v1.1 se apruebe |

### Divergencias registradas por la Fase 14 (20/09/2026)

Ninguno de estos documentos se modificó. Se anota la evolución, no se corrige el pasado.

| Documento | Qué dice | Qué es cierto ahora | Acción propuesta |
|---|---|---|---|
| `CLAUDE.md` § Estado actual | «`main` y `develop` tienen el mismo contenido» | Dejó de ser literalmente cierto al integrar la Fase 13 solo en `develop` (`95c5b8b` frente a `4563c69` en `main`). `main` sigue siendo la v1.0 publicada, que es lo correcto | Revisar la frase cuando v1.1 se integre en `main`; no antes. ~~Pendiente~~ **Corregida en el hotfix documental de la Fase 21 (23/09/2026)**, antes de lo previsto: ver la sección de ese hotfix |
| `docs/v1.1/phase-13-master-plan.md` §6 | Registra permisos locales amplios como hallazgo, incluido `PowerShell(Remove-Item *)` | El hallazgo **se resolvió** el 20/09/2026: `.claude/settings.local.json` pasó a 21 reglas de solo lectura en `allow`, 41 en `ask` y 19 en `deny`. El archivo no se versiona | Ninguna. El plan de la Fase 13 es un documento histórico y conserva el hallazgo tal como se observó |
| Baseline del prompt de la Fase 14 | Anticipaba `PROMPT_FASE_13_CLAUDE_CODE.md` sin rastrear | El archivo ya no existe en el repositorio; el árbol estaba limpio al iniciar la fase | Ninguna. Registrado en `phase-14-ml-definition.md` §3 |
| `docs/v1.1/ml-feasibility.md` (Fase 13) | Planteaba el servicio de riesgo como estudio abierto, con el plazo objetivo sin resolver | La Fase 14 lo especificó y el equipo aprobó doce decisiones; `ML-DECISION-01` quedó resuelta y apareció `GAP-01` | Ya actualizado con una nota de evolución al inicio; el cuerpo del estudio se conserva |
| `docs/v1.1/scope-preliminary.md` (Fase 13) | Listaba seis decisiones pendientes | Tres se resolvieron el 20/09/2026; quedan tres nuevas, incluida `GAP-01` | Ya actualizado; las resueltas se tacharon en lugar de borrarse |

### Divergencias registradas por la Fase 20 (23/09/2026)

La interfaz de v1.1 quedó documentada en tres fases separadas, cada una en su documento, sin que ninguna reescriba a la anterior: **Fase 18 = diseño** ([`phase-18-frontend-redesign.md`](phase-18-frontend-redesign.md)), **Fase 19 = movimiento** ([`phase-19-animations.md`](phase-19-animations.md)) y **Fase 20 = profundidad 3D** ([`phase-20-3d-experience.md`](phase-20-3d-experience.md)).

| Documento | Qué decía | Qué es cierto ahora | Acción tomada |
|---|---|---|---|
| `architecture-decisions/ADR-003-progressive-3d.md` | Estado «propuesta (pendiente de decisión del equipo)» | El equipo encargó la Fase 20 y la experiencia se implementó bajo las condiciones de la ADR, sin dependencias nuevas | Estado tachado, no borrado, y nota de evolución al inicio; el cuerpo se conserva |
| `scope-preliminary.md` · RNF-C | «Pendiente de decisión» | Implementada en la Fase 20; su promoción formal al baseline sigue pendiente | Estado tachado y anotado |
| `scope-preliminary.md` · pregunta 3 | ¿Se autoriza el 3D y sus dependencias? | El 3D se encargó; las dependencias no hicieron falta | Anotada; la parte de dependencias sigue abierta |
| `.claude/skills/recruitment-3d-experience/SKILL.md` | «Estado: candidato. No instales dependencias ni escribas componentes 3D todavía» | Ya hay un componente 3D, sin dependencias | **No se tocó**: es una skill del equipo; actualizar su estado le corresponde a quien la mantiene |

### Divergencias registradas por la Fase 21 (23/09/2026)

La interfaz de v1.1 queda documentada en cuatro fases, cada una en su documento: **F18 = diseño** ([`phase-18-frontend-redesign.md`](phase-18-frontend-redesign.md)), **F19 = movimiento** ([`phase-19-animations.md`](phase-19-animations.md)), **F20 = profundidad 3D** ([`phase-20-3d-experience.md`](phase-20-3d-experience.md)) y **F21 = QA visual y accesibilidad** ([`phase-21-visual-qa.md`](phase-21-visual-qa.md)). La Fase 21 corrige defectos de las anteriores sin reescribir sus documentos: cada corrección se registra en el suyo.

| Documento | Qué decía | Qué es cierto ahora | Acción tomada |
|---|---|---|---|
| `.claude/skills/recruitment-3d-experience/SKILL.md` | «Estado: candidato…» (ver Fase 20) | Implementada y acotada a la portada | **Actualizada**, por encargo explícito de la Fase 21: estado «implementada y acotada», condiciones para ampliarla; el texto anterior se conserva como nota de historia y las reglas no cambian |
| `CLAUDE.md` · tabla de skills | `recruitment-3d-experience`: «aún **no implementado**» | Implementada en la Fase 20 | ~~**No se tocó**: `CLAUDE.md` se revisa cuando v1.1 se integre en `main` (misma regla que su § Estado actual)~~ **Corregida en el hotfix documental de la Fase 21** (ver abajo) |
| `scope-preliminary.md` · preguntas | Doce preguntas | Pregunta 13: ¿pasa RNF-C al baseline? | Añadida como **propuesta pendiente**; no se finge aprobación |
| `phase-18-frontend-redesign.md` | El rojo destructivo y la variante destructiva de alerta como quedaron en la Fase 18 | La alerta destructiva era ilegible en claro (≈ 1:1) y el rojo en oscuro no llegaba a 4.5:1; corregido en la Fase 21 | Sin cambios en el documento de la Fase 18; la corrección y sus cifras están en `phase-21-visual-qa.md` §15–§16 |
| `phase-19-animations.md` | Plegado de los códigos de recuperación con `grid-template-rows` | Dejaba una franja de 12 px visible; `scrollIntoView` suave ignoraba el movimiento reducido. Corregido en la Fase 21 | Sin cambios en el documento de la Fase 19; ver `phase-21-visual-qa.md` §10 y §13 |
| `phase-20-3d-experience.md` §15 | `app-*.css` 99.90 kB | Las cifras actuales, tras la Fase 21, están en `phase-21-visual-qa.md` §19 | Sin cambios: las cifras de la Fase 20 son correctas para su momento |

### Hotfix documental de la Fase 21 (23/09/2026)

La auditoría de Codex encontró que `CLAUDE.md` —la fuente de contexto común de Claude Code y Codex, que `AGENTS.md` manda leer primero— describía como **estado actual** lo que solo era cierto al abrir v1.1: `main` igual a `develop`, la Fase 13 vigente y ML y 3D sin implementar. Esperar a la integración en `main` dejaba a cualquier agente trabajando sobre un contexto falso, así que se corrigió ya. Mapa de v1.1 tras el hotfix: **F13–F14.5 = gobierno y definición del ML**, **F15 = ML implementado** (datos sintéticos, entrenamiento, FastAPI experimental), **F16 = integración Laravel ↔ FastAPI**, **F17 = validación ML**, **F18 = diseño**, **F19 = movimiento**, **F20 = CSS 3D**, **F21 = QA visual y accesibilidad**.

| Documento | Qué decía | Qué es cierto ahora | Acción tomada |
|---|---|---|---|
| `CLAUDE.md` § Estado actual | `main` y `develop` iguales; Fase 13 solo gobierno; sin ML, FastAPI, rediseño, motion ni 3D | `main` = v1.0 (`4563c69`, tag `9a946c2`); `develop` = `a316c07` integra F13–F20; F21 implementada en su rama, sin integrar; F22 sin iniciar | **Reescrita** separando `main`/v1.0 de `develop`/v1.1; el texto anterior se conserva como nota de historia |
| `CLAUDE.md` · tabla de skills, stack y comandos | ML y 3D «aún no implementado»; PHPUnit 244; «todo corre en Docker» | ML experimental implementado; 3D implementado y acotado; PHPUnit 408 + 8 en `develop`; el servicio ML corre fuera de Docker Compose | Actualizados; el conteo de v1.0 se conserva junto al actual |
| `CLAUDE.md` · contrato 4 | «Cualquier ML **futuro** será informativo…» | Ya existe un ML (RF-29) | Redactado para cubrir el actual y cualquier futuro; el contrato no se relaja |
| `.claude/skills/ml-risk-service/SKILL.md` | «Estado: candidato. No implementes nada todavía» | Implementado en `develop` como experimental; contrato científico congelado | Estado actualizado con nota de historia; fronteras y evidencia exigida sin cambios |
| `.claude/skills/recruitment-3d-experience/SKILL.md` | Primera condición de *fallback*: «el navegador no soporta WebGL» | La escena actual es CSS 3D y **no depende de WebGL** | Separadas las condiciones actuales de las de una escena WebGL futura hipotética; nota de historia |
| `scope-preliminary.md` · RF-29 y preguntas 10 y 11 | RF-29 «bloqueado por `ML-DECISION-01`»; preguntas 10 y 11 pendientes | `ML-DECISION-01` resuelta; F15 ejecutada; `GAP-01` resuelto técnicamente en F16. RF-29 **sigue siendo candidato** | Tachado y anotado, sin borrar |
| `ml-feasibility.md` · `ml/model-card-draft.md` | «No se ha implementado nada»; «`GAP-01` sigue abierto y el modelo no puede integrarse» | Servicio implementado (F15), integrado (F16) y validado en pruebas (F17); experimental; `GAP-01` resuelto técnicamente | Nota de evolución al inicio de cada uno; cuerpo intacto. Los demás borradores de `ml/` llevan fecha «Fase 14» en su cabecera y se leen como historia: no se tocaron |
| `docs/PROGRESS.md` | Cabecera de la Fase 12 (`release/qa-final`); sin entradas F13–F17 | Estado de v1.1 por fase | Añadida una tabla de estado v1.1 al inicio; las secciones de v1.0 se conservan |
| `phase-21-visual-qa.md` §19 | `app-*.css` 99.82 kB / 16.57 kB gzip | 99.86 kB / 16.58 kB gzip en la compilación de `1b3d27d` | Corregido |

**Sin cambios de decisión:** RF-29 y RNF-C siguen siendo candidatos; la promoción al baseline sigue siendo decisión del equipo (preguntas 12 y 13 de `scope-preliminary.md`).

## 2. Por verificar antes de tocar nada

| Documento | Qué revisar |
|---|---|
| `docs/tdd-evidence.md` | Los conteos de pruebas son por fase y crecen a lo largo del proyecto; confirmar que el conteo final coincide con la última ejecución registrada (244 pruebas) y que ningún conteo intermedio se presenta como final |
| `docs/rf-implementation-matrix.md` · `traceability-master.md` | Confirmar que las rutas de archivo citadas siguen existiendo tras la corrección de CI |
| `docs/docker.md` | Confirmar que las versiones citadas coinciden con los Dockerfiles actuales (PHP 8.4) |
| `docs/final-report/diagram-reports/` | Confirmar que los diagramas descritos siguen correspondiendo al código |
| `.github/workflows/tests.yml` frente a `post-publication-ci-fix.md` | Confirmar que lo documentado coincide con el flujo vigente |

Cada verificación que se ejecute debe anotar aquí su resultado real, incluido "sin divergencias".

## 3. Formato 09

**Entrada de la Fase 14:** existen candidatos revisados (RF-28 a RF-31), una brecha funcional (`GAP-01`, plazo operacional de cierre) y cinco RNF candidatos adicionales con numeración provisional, todos en [`ml/requirements-and-traceability-plan.md`](ml/requirements-and-traceability-plan.md).

**Decisión 11 del 20/09/2026:** ningún RF candidato pasa al baseline de v1.1. El Formato 09 **no se toca todavía**.

**Cuando `GAP-01` se aborde**, el plazo operacional explícito necesitará entrada propia en el Formato 09: no es una columna técnica sino una capacidad funcional nueva, con actor, momento de captura y regla de inmutabilidad. **No se le reserva número de RF por anticipado.**

El Formato 09 se actualiza **solo** cuando el equipo apruebe requerimientos de v1.1. Regla: RF-01 a RF-27 conservan su número y su redacción; los nuevos se agregan al final desde RF-28 y no se renumera nada. Si un candidato de `scope-preliminary.md` se descarta, su número provisional se libera y no se reutiliza en ese mismo ciclo.

## 4. UML

| Diagrama | Acción en v1.1 |
|---|---|
| Casos de uso | Añadir solo los casos de uso aprobados, marcados como v1.1 |
| Clases | Añadir clases nuevas; no redibujar las existentes |
| Secuencia | Un diagrama nuevo por flujo aprobado |
| Componentes | Incorporar el servicio de inferencia **solo si** supera los criterios de `ml-feasibility.md`, y marcado como opcional |
| Despliegue | Reflejar servicios nuevos solo cuando existan en `docker-compose.yml` |
| Modelo de datos | Reflejar migraciones reales, nunca tablas planeadas |

Procedimiento obligatorio: la skill `powerdesigner-uml`. Todo elemento del diagrama debe existir en el código o estar marcado `<<propuesto v1.1>>`.

## 5. PowerDesigner

Los archivos de PowerDesigner de v1.0 **se preservan intactos**. v1.1, si lo requiere, trabajará sobre copias nuevas con nombre versionado y registrará el procedimiento de importación y su validación en el informe de diagramas correspondiente. En la Fase 13 no se generó ni se editó ningún archivo de PowerDesigner.

## 6. Regla de oro

Un documento de v1.0 que contradiga el estado de v1.1 **no se corrige**: se anota en este mapa la diferencia (documento, sección, qué dice, qué es cierto ahora) y se explica en el documento nuevo de v1.1. La historia del proyecto es parte de la evidencia académica.
