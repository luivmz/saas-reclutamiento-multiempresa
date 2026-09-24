# Fase 23 — Formalización en PowerDesigner

**Fecha:** 24 de septiembre de 2026
**Rama:** `feature/phase-23-powerdesigner` · **Base:** `2621bee` (cierre de la Fase 22)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **documental y de modelado**. Crea los modelos nativos de PowerDesigner y sus exportaciones a partir de la especificación de la Fase 22. No cambia código, pruebas, dependencias, rutas, modelos de Laravel, Policies, migraciones ni el servicio ML. RF-23 sigue siendo una decisión humana, RF-28 un candidato no implementado y RF-29 un servicio experimental.

---

## 1. Objetivo

Formalizar en PowerDesigner los 19 diagramas UML especificados en la Fase 22 ([`uml/`](uml/)) y el modelo físico real, como modelos nativos (`.oom`, `.pdm`) versionados y exportados, sin reinterpretar la arquitectura: lo que no está en la especificación de F22 no se dibuja.

## 2. Baseline

| | |
|---|---|
| `develop` = `origin/develop` | `2621beeaec53b2482c4b260a05fe0292a7ad0088` (*merge: close phase 22 uml update*), árbol limpio, `git diff --check` limpio |
| `main` | `4563c69` (v1.0 académica), sin cambios |
| `v1.0.0-academic` | `9a946c2`, intacto |
| Fuente de F22 | `docs/v1.1/uml/`, sin cambios desde `4219c11` (*hotfix* de auditoría de F22) |
| Esquema real | `pg_dump --schema-only` de la base `reclutamiento` de `develop` (PostgreSQL 17.11) |

## 3. Rama

`feature/phase-23-powerdesigner`, creada desde `develop` en `2621bee`. Todo el trabajo está en `docs/v1.1/powerdesigner/` y en este documento, más la actualización de estado de `docs/PROGRESS.md`, `docs/v1.1/documentation-update-map.md`, `CLAUDE.md` y el bloque de estado de `docs/v1.1/scope-preliminary.md`. Sin `push`, `merge`, *tag* ni *release*.

La fase se hizo en dos sesiones. La primera construyó el PDM y el OOM estructural y se detuvo, a pedido del equipo, en un *checkpoint* seguro sin commits. La segunda reanudó desde ese estado sin reconstruir nada. Revisó los ajustes estructurales, generó las secuencias, actividades y estados sobre el mismo OOM, cerró la documentación e hizo los commits.

## 4. Skills

| Skill | Uso |
|---|---|
| `project-guardian` | Rama, alcance (solo `docs/`), contratos (RF-23 humano, RF-29 experimental, sin datos reales ni secretos), cuándo detenerse |
| `powerdesigner-uml` | Nada que no exista en el código; nombres técnicos idénticos; `<<propuesto v1.1>>` para RF-28; validar conteos tras importar; registrar versión, pasos, validación y ajustes. **Observación:** su texto dice que en «esta fase» no se generan `.oom`/`.pdm` y que PowerDesigner «no se automatiza desde este entorno»; es de la Fase 22 y contradice el encargo de F23 (§12, O-02) |
| `academic-traceability` | Trazabilidad RF → diagrama (§11); sin reescribir los documentos de v1.0 |

## 5. PowerDesigner usado

- **SAP PowerDesigner 16.6.1.5066** (versión que devuelve la propia aplicación), instalado en el equipo del equipo; no se instaló ni actualizó software.
- **Automatización por COM** (`PowerDesigner.Application`), la misma interfaz que usan los scripts de ejemplo de la instalación, desde PowerShell 5.1. Modo *batch* (`InteractiveMode = 0`) durante cada script, restaurado al terminar; el modelo se guarda antes de cerrarse. Los modelos los crea y guarda PowerDesigner: no se escribió ningún `.oom` ni `.pdm` a mano.
- **Modelo orientado a objetos (OOM)** con lenguaje objeto *Analysis* y **modelo físico (PDM)** con el DBMS *PostgreSQL 9.x*, el más reciente que trae la versión 16.6.
- Reproducibilidad: cada diagrama sale de un script versionado en `powerdesigner/scripts/`; los de comportamiento se pueden regenerar sin duplicar nada (ver [`powerdesigner/README.md`](powerdesigner/README.md)).

## 6. Modelos creados

| Archivo | Tipo | Contenido |
|---|---|---|
| `powerdesigner/models/saas-recruitment-v1.1-oom.oom` | OOM | «SaaS Reclutamiento v1.1 - UML AS-IS»: 20 diagramas. 27 clases (17 del dominio + 10 enumeraciones), 37 asociaciones, 6 actores, 29 casos de uso, 20 componentes, 3 interfaces, 6 nodos, 9 artefactos, 40 objetos de secuencia, 125 mensajes, 20 fragmentos, 36 actividades, 10 decisiones, 58 flujos, 6 unidades organizativas, 19 estados, 37 transiciones, 23 eventos |
| `powerdesigner/models/saas-recruitment-v1.1-pdm.pdm` | PDM | «SaaS Reclutamiento v1.1 - Modelo fisico»: 27 tablas, 258 columnas, 48 FK, 43 claves, 31 índices, 1 *trigger* (`audit_logs_append_only`), 32 CHECK; 2 diagramas |
| `powerdesigner/models/source/schema-postgresql.sql` | SQL | Esquema real preparado para el lector PG9 (sin datos ni credenciales), fuente de la ingeniería inversa |

Organización del OOM: CL-01 en el paquete `App\Models`, CL-01b en `App\Enums`, PK-01 en `Módulos del monolito` (con sus 10 subpaquetes), cada diagrama de estados en su paquete `ST-01` … `ST-04`, y el resto en la raíz. Sin diagramas vacíos, sin objetos de prueba.

## 7. Diagramas

22 diagramas: los 19 de F22, la vista auxiliar CL-01b y los dos físicos. Inventario completo, con conteos y RF: [`powerdesigner/inventory.md`](powerdesigner/inventory.md).

| Grupo | Diagramas |
|---|---|
| Físico | PDM-01 Esquema completo · PDM-02 Tablas de dominio |
| Estructura | CL-01 Clases del dominio · CL-01b Enumeraciones · UC-01 Casos de uso · PK-01 Paquetes · CO-01 Componentes · DE-01 Despliegue |
| Interacción | SEQ-01 Registrar postulación · SEQ-02 Aprobar o rechazar requerimiento · SEQ-03 Cambiar etapa · SEQ-04 Programar evaluación · SEQ-05 Entrevista · SEQ-06 Ranking y comparación · SEQ-07 Decisión final `<<human decision>>` · SEQ-08 Riesgo operacional `<<experimental>>` |
| Actividad | AC-01 Proceso de reclutamiento AS-IS · AC-02 Riesgo operacional `<<experimental>>` |
| Estados | ST-01 Requerimiento · ST-02 Vacante · ST-03 Postulación · ST-04 Evaluación y entrevista |

## 8. Rutas

```
docs/v1.1/powerdesigner/
├── README.md             cómo abrir, cómo regenerar, reglas
├── inventory.md          inventario de los 22 diagramas
├── f22-checklist.md      correspondencia F22 ↔ PowerDesigner
├── models/               .oom, .pdm y source/schema-postgresql.sql
├── exports/              PNG y SVG de cada diagrama (+ *_svg_Files/ que enlazan los SVG)
└── scripts/              01–09, seqlib, flowlib, pdlib, pdm/, tools/
```

Las exportaciones se llaman como el diagrama (`SEQ-07-decision-final.png`, `ST-03-estados-postulacion.svg`…). No se versionan modelos de prueba ni copias de respaldo de PowerDesigner.

## 9. Validación visual

Cada diagrama se exportó a PNG y se **revisó a ojo** después de cada cambio; los problemas encontrados se corrigieron en el script y se regeneró el diagrama, sin copias:

- **Secuencias**: mensajes cada uno en su fila y en el orden de F22; separador del `else` bajo el último mensaje del primer operando; fragmentos anidados cerrando dentro del que los contiene; espacio antes y después de cada fragmento para que guardas y rótulos no se pisen; lifelines recolocadas sobre la rejilla (PowerDesigner movía alguna al adjuntar los mensajes) y ensanchadas para que el nombre quepa; estereotipos largos (`<<external service, experimental>>`) con caja propia; rótulos de automensajes a la derecha del bucle; marco de la interacción que abarca las notas.
- **Actividades**: carriles sin solaparse, rutas ortogonales, bucles por fuera (observación del requerimiento, reconfiguración de la vacante, más sesiones), fines de flujo ⊗ en los descartes, rombos del tamaño de su condición.
- **Estados**: transiciones horizontales hacia `descartado` y `no_seleccionado`, carriles laterales para las transiciones que saltan un estado, rótulos junto a su origen sin tapar estados ni líneas.
- **Estructura** (primera sesión y reanudación): nombres de vínculos visibles donde F22 los rotula, sin nombres automáticos; rutas rectas en DE-01.

Conteos: cada diagrama se recorrió por COM y sus elementos se compararon con la fuente de F22 (inventario y [`f22-checklist.md`](powerdesigner/f22-checklist.md)). Resultado: **sin diferencias de contenido**; 125 mensajes y 20 fragmentos (igual que los `.puml`), 37 transiciones, 19 estados. PDM: 27 tablas y 48 FK, igual que el esquema.

Archivos tal como quedan en Git: `.gitattributes` normaliza a LF los `.oom`, `.pdm` y `.svg` (son XML). Se extrajeron las versiones confirmadas y se abrieron en PowerDesigner: 20 diagramas y 125 mensajes en el OOM, y 27 tablas, 48 referencias y 2 diagramas en el PDM.

Quedan detalles cosméticos que no cambian datos (inventario, «Observaciones cosméticas»).

**Sin suites funcionales**: la fase no toca código ni pruebas; no se ejecutaron PHPUnit, Vitest, pytest ni Cypress.

## 10. Diferencias justificadas

Detalle y motivo de cada una en [`powerdesigner/f22-checklist.md`](powerdesigner/f22-checklist.md). **Ninguna diferencia de contenido sin justificar.** Resumen:

- **Por la herramienta**:
  - nombres únicos (objetos de secuencia reutilizados, actividades repetidas con su estado real o su RF, cada diagrama de estados en su paquete);
  - dependencias sin rótulo con un espacio por nombre;
  - carriles de AC-01 y contenedores de DE-01 como marcos gráficos;
  - artefactos sin `/` ni `:`;
  - DBMS PG9, con los CHECK restituidos como conjunción y el `WHERE` del índice parcial en un comentario.
- **Por la notación**:
  - transiciones `evento [guarda] / efecto`, con el paréntesis de actor y RF junto al evento;
  - separadores de tramo de SEQ-05 como notas;
  - actor «RR. HH. / Aprobador» de SEQ-06 y SEQ-08 como «Recursos Humanos», con una nota del Aprobador;
  - notas de los dos niveles en AC-01.
- **Por legibilidad**:
  - enumeraciones en la vista auxiliar CL-01b;
  - fila 2 de CL-01 como dos asociaciones y una nota, y fila 35 como nota;
  - estados finales altos en ST-03.

## 11. Trazabilidad

| RF | Diagramas de PowerDesigner |
|---|---|
| RF-01 a RF-04 | UC-01, PK-01, CO-01, CL-01, PDM, SEQ-02, AC-01, ST-01 |
| RF-05 a RF-07 | UC-01, PK-01, CO-01, CL-01, PDM, AC-01, ST-02 |
| RF-08 a RF-11 | UC-01, PK-01, CL-01, PDM, SEQ-01, AC-01, ST-03 (RF-10) |
| RF-12 a RF-15 | UC-01, PK-01, CL-01, PDM, SEQ-03, AC-01, ST-03 |
| RF-16 a RF-20 | UC-01, PK-01, CL-01, PDM, SEQ-04, SEQ-05, SEQ-06 (RF-20), AC-01, ST-03, ST-04 |
| RF-21, RF-22 | UC-01, PK-01, CO-01, SEQ-06, AC-01 (solo postulaciones no descartadas) |
| **RF-23** | UC-01 (`<<human decision>>`), CL-01 (`SelectionDecision`), SEQ-07 `<<human decision>>`, AC-01 (actividad `<<human decision>>` del Aprobador). La persona decide y justifica; puede no ser la primera; ningún mensaje al ML |
| RF-24 a RF-26 | UC-01, PK-01, CL-01, PDM (índice parcial), AC-01, ST-02, ST-03 |
| RF-27 | UC-01, PK-01, CO-01, CL-01 (`AuditLog`), PDM (*trigger* de solo inserción), lifeline `AuditLogger` en las secuencias, nota transversal en AC-01 |
| **RF-28** | UC-01: UC-RF28 `<<propuesto v1.1>>` **sin asociaciones**, con nota de candidato no implementado. En ningún otro diagrama |
| **RF-29** | UC-01, PK-01, CO-01, DE-01, CL-01/PDM (`target_completion_at`), SEQ-08 y AC-02, siempre `<<experimental>>`. Estima el **proceso**; 15 features sin IDs ni PII; sin incertidumbre; sin relación con ranking, comparación ni decisión |

La matriz completa RF ↔ UML ↔ código ↔ pruebas sigue siendo [`uml/traceability-matrix.md`](uml/traceability-matrix.md); los diagramas de PowerDesigner tienen los mismos ID que allí.

## 12. Observaciones

| # | Observación | Tratamiento |
|---|---|---|
| O-01 | `evaluation_criteria.position` está en el esquema (PDM) y no en los atributos de `EvaluationCriterion` de la especificación de F22 | CL-01 sigue a F22. Anotado para revisar la especificación; no se corrige aquí |
| O-02 | La skill `powerdesigner-uml` (y su `POWERDESIGNER.md`) dice que en «esta fase» no se generan `.oom`/`.pdm` y que PowerDesigner no se automatiza desde este entorno | Texto de la Fase 22. F23 pedía los archivos nativos, y la automatización por COM funcionó y es reproducible. **Decisión del equipo**: actualizar la skill en una fase de gobierno; no se modificó aquí |
| O-03 | La skill pide registrar la importación en `docs/final-report/diagram-reports/` | Los informes de v1.0 no se tocan. El registro de v1.1 es este documento más `powerdesigner/inventory.md` y `f22-checklist.md` |
| O-04 | Modelos de prueba de la primera sesión (`zz_*.oom`, copias de sondeo) | Solo en la carpeta temporal del trabajo de Claude Code, **fuera del repositorio**. No se versionaron ni se borraron: su limpieza espera autorización |
| O-05 | Detalles cosméticos (guarda de `critical`, rótulos cortos de AC-01) | Listados en el inventario; no afectan a los datos |
| O-06 | PowerDesigner quedó abierto en el equipo durante toda la fase, como pidió el equipo | Cada script cierra solo los modelos que abre; `tools/pd-status.ps1` confirma `modelos abiertos: 0` al terminar |

## 13. Deuda OpenAPI

`ml-service/src/recruitment_ml/api/schemas.py` describe el campo `days_remaining_to_target` como algo que Laravel no puede producir (GAP-01). **Es texto obsoleto**: GAP-01 está resuelto técnicamente desde la Fase 16 (`vacancies.target_completion_at`). Se **registra, no se corrige**: está en el runtime ML, fuera del alcance de F23 (`ml-service/**` no se modifica). En los modelos de PowerDesigner GAP-01 figura resuelto: SEQ-08 y AC-02 construyen las 15 features, incluido el plazo, y el PDM tiene `target_completion_at`. Corregirlo corresponde a una fase con permiso sobre `ml-service/`, con su prueba.

## 14. Handoff a la Fase 24

La Fase 24 **no se inició** y su alcance no está definido en la documentación de v1.1 (la Fase 21 solo anota que el lector de pantalla real y el rendimiento en equipo modesto «pasan a F24/F25»). Para quien la defina:

1. **Auditoría de Codex de F23**: abrir los dos modelos en PowerDesigner 16.6; revisar el inventario, la checklist y las exportaciones; regenerar al menos una secuencia con `$env:PD_ONLY` para confirmar que el script reemplaza sin duplicar.
2. **Decisiones pendientes del equipo**: actualizar la skill `powerdesigner-uml` (O-02); revisar `evaluation_criteria.position` en CL-01 (O-01); autorizar la limpieza de los modelos de prueba (O-04); corregir el texto OpenAPI de GAP-01 (§13) en una fase con permiso sobre `ml-service/`.
3. **Uso de los modelos**: son la fuente gráfica de v1.1. Cualquier cambio se hace en su script y se regenera, y se actualiza el inventario.
4. **Sin cambios**: RF-01 a RF-27 con su número y significado; RF-28 candidato; RF-29 experimental; RF-23 humano; multiempresa, Policies y auditoría de solo inserción.
