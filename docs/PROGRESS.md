# Progreso del proyecto

Última actualización: 2026-09-13 · Rama actual: `feature/final-documentation`

## Fases

| Fase | Estado |
|---|---|
| 0 a 9 | ✅ Completadas e integradas en `develop` |
| 10 — Docker y portabilidad | ✅ Integrada en `develop` (`02c2505`, merge `--no-ff` de `ff524e6`) |
| 11 — Documentación final | ✅ Completada en `feature/final-documentation` (**pendiente de revisión; no fusionada en `develop`**) |
| 12 — QA final | ❌ Pendiente |

**RF-01 a RF-27 constituyen la línea base funcional completa.** La Fase 11 solo modificó documentación (Markdown): no cambió código, configuración, reglas de negocio ni RF.

## Reglas de negocio vigentes de la Fase 6 (aprobadas; sin cambios)

1. Registrar la decisión final no cambia por sí sola el estado de ninguna postulación.
2. El candidato elegido puede no ser el primero del ranking.
3. La decisión requiere acción humana explícita y justificación.
4. Tras la decisión final, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las demás postulaciones activas pasan a «no seleccionado» al cerrar la vacante, no antes.
6. RF-25 implementa solo el cierre con selección.

## Fase 11 — lo realizado

- **Integración de la Fase 10:** merge en `develop` (`02c2505`).
- **Verificación posterior al merge:** PHPUnit **244 pruebas: 236 passed, 8 skipped, 0 failed**. Por suite: Unit 62 passed (85 assertions) y Feature 174 passed + 8 skipped (989 assertions), 1074 assertions en total.
- **Auditoría documental:**
  - Fuera del repositorio solo existen 4 diagramas UML de PowerDesigner (`Diagramas/PD/*.oom`).
  - No existen BPMN AS-IS/TO-BE, casos de uso ni documentos F4/F5/F6.
  - No se encontró NRC 30180 ni tecnologías inexistentes presentadas como implementadas.
- **Informe final (`docs/final-report/`):** 14 capítulos (`01` a `14`), además de `traceability-master.md`, `evidence-index.md`, `technical-summary.md` y `demo-script.md`.
- **Matriz maestra:** RF-01 a RF-27, con actor, backend, frontend, PHPUnit y Cypress verificados contra el código; clases citadas y 106 métodos `test_rfNN_*` comprobados.
- **Diagramas:** se referenciaron los `.oom` y se documentaron sus discrepancias con la implementación final:
  - la secuencia de selección no separa la decisión humana (RF-23), la selección (RF-24) y el cierre (RF-25);
  - el diagrama de despliegue incluye S3, que no existe.
- **Diagramas nuevos derivados del código** (Mermaid): arquitectura, clases, estados, secuencia de decisión → selección → cierre, ERD y flujo TO-BE implementado. El flujo TO-BE se rotula explícitamente como no-BPMN.
- **Otros archivos:**
  - `README.md` completo: proyecto, universidad, integrantes, arquitectura, stack, instalación, usuarios demo, pruebas, estructura, comandos, documentación, seguridad y estado.
  - Referencia a la matriz maestra en `docs/rf-implementation-matrix.md`.
- **Validación documental:**
  - 0 enlaces relativos rotos y todas las rutas citadas existen.
  - Versiones leídas de `composer.lock`, `npm ls` y contenedores; hashes leídos de `git log`.
  - Sin secretos en la documentación.

## Cifras usadas en la documentación

| Fuente | Cifra |
|---|---|
| PHPUnit | 244 pruebas · 236 passed · 0 failed · 8 skipped · 1074 assertions (Unit 62 / Feature 174 + 8) |
| Cypress | 14 specs · 43 tests · 43/43 (instalación limpia 03:26, entorno principal 03:34); Fase 9: 40/40 ×2 |
| Validación manual | Recorrido visual 10/10 (49 capturas) · flujo 12/12 |
| RF | 27/27 implementados, con PHPUnit y ejercidos por Cypress |
| Defectos | 13 registrados / 13 cerrados (Crítica 2 · Alta 5 · Media 4 · Baja 2) |
| Cobertura de código | No medida |

## Pendientes documentales (antes de la entrega)

1. Anexar los BPMN AS-IS y TO-BE (no están en el repositorio).
2. Contrastar el catálogo de casos de uso derivado con la práctica de casos de uso del equipo.
3. Validar el AS-IS preliminar con RR. HH./Administración, o mantenerlo rotulado como preliminar.
4. Seleccionar las capturas de pantalla para el informe (las actuales son locales y no están versionadas).
5. Completar las fechas de consulta de las referencias.
6. Actualizar o anotar los diagramas UML de selección y despliegue.

## Git

- Rama: `feature/final-documentation` (desde `develop` en `02c2505`).
- Sin push, sin remoto, sin tag. **No fusionar en `develop` hasta la revisión del equipo.**

## Siguiente tarea exacta para retomar

1. Revisión de la Fase 11; si se aprueba, merge `--no-ff` de `feature/final-documentation` a `develop`.
2. Fase 12 (QA final) según el plan maestro, no iniciada. Incluye la integración en `main` y la publicación en GitHub tras la revisión final.
