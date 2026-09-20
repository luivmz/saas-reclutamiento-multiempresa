# Mapa de actualización documental para v1.1

Este documento **señala** qué documentación habría que revisar si v1.1 avanza. En la Fase 13 **no se modificó ningún documento histórico**: la regla es marcar la divergencia aquí, nunca reescribir el pasado en silencio.

Alcance de la revisión realizada: se inventariaron los 40 documentos existentes y se verificó su presencia y estructura. **No** se hizo una relectura línea por línea de cada uno en busca de contradicciones; lo que sigue distingue lo verificado de lo que queda por verificar.

## 1. Divergencias verificadas

| Documento | Sección | Divergencia | Acción propuesta |
|---|---|---|---|
| `docs/PROGRESS.md` | Estado general | Describe el proyecto cerrado en la Fase 12 más la corrección de CI. La Fase 13 abre v1.1 y no está reflejada. | Añadir la Fase 13 como entrada nueva al final, sin alterar las anteriores |
| `docs/final-report/delivery-checklist.md` · `qa-final-report.md` | Cierre | Declaran el cierre de v1.0. Siguen siendo correctos **para v1.0**. | No tocar. v1.1 tendrá sus propios documentos de cierre |
| `README.md` | Estado del proyecto | No menciona `CLAUDE.md` ni las skills del proyecto | Añadir un enlace breve cuando v1.1 se apruebe |

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
