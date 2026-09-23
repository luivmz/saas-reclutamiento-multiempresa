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
| `CLAUDE.md` § Estado actual | «`main` y `develop` tienen el mismo contenido» | Dejó de ser literalmente cierto al integrar la Fase 13 solo en `develop` (`95c5b8b` frente a `4563c69` en `main`). `main` sigue siendo la v1.0 publicada, que es lo correcto | Revisar la frase cuando v1.1 se integre en `main`; no antes |
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
