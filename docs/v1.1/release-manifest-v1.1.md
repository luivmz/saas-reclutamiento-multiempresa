# Manifiesto de release — v1.1 académica

| | |
|---|---|
| Versión | **v1.1** (académica) |
| Etiqueta propuesta | `v1.1.0-academic`, anotada. **No creada**: pendiente de auditoría y autorización |
| Rama de cierre | `feature/phase-26-release-closeout` |
| Baseline pre-F26 (merge F25 en `develop`) | `2b97fe36d25fd3911bc2e4e1e24c6ab16200179a` |
| Árbol del baseline `develop` pre-F26 | `f945b8d123f419d7e038962a8a92c99008e950e0`. Solo identifica el baseline; **no** es el árbol final del release |
| HEAD de la rama F26 | El último commit de `feature/phase-26-release-closeout`. Un documento no puede contener el hash del commit que lo introduce; se lee con `git rev-parse feature/phase-26-release-closeout` |
| `FINAL_DEVELOP_MERGE_COMMIT` | Por resolver en el cierre: merge `--no-ff` de F26 en `develop` |
| `FINAL_MAIN_MERGE_COMMIT` | Por resolver en el cierre: merge `--no-ff` de `develop` en `main`, con el CI de `develop` en verde |
| `FINAL_RELEASE_TREE` | Se valida dinámicamente en el cierre: `git rev-parse develop^{tree}` debe ser igual a `git rev-parse main^{tree}`. No hay hash fijo |
| `TAG_TARGET` | `FINAL_MAIN_MERGE_COMMIT`, solo después del CI de `main` en verde y de la igualdad de árboles |
| `main` = `origin/main` | `4563c696ba08fd6d2a689af733020d849edebad2` (v1.0), sin cambios |
| Etiqueta de la v1.0 | `v1.0.0-academic` → `9a946c202ef7473230e8efa371ace13479ab889c`, sin cambios |

Secuencia obligatoria de cierre, con la etiqueta solo después del CI verde de `main`: [`phase-26-release-closeout.md`](phase-26-release-closeout.md) §15.

## Artefactos clave con hash

SHA-256 del **contenido confirmado en Git** (`git show <rev>:<ruta> | sha256sum`), reproducible desde cualquier *checkout*. Tamaño en bytes del blob.

| Artefacto | SHA-256 | Bytes |
|---|---|---|
| `docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.pdf` | `a0ffc2917bfd790365c64a0d14460dd3e1b2050fca9702dcd6b48d98312068af` | 2 099 904 |
| `docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx` | `ee288eb237dfd26af10820784b146ffeb8d93df02e40c6e0741b1546430627a5` | 2 576 008 |
| `docs/v1.1/powerdesigner/models/saas-recruitment-v1.1-oom.oom` | `5aed557ce928c2560b46ea9fd2347225224e79fa4bc572ec2e896edcf12705d1` | 1 154 409 |
| `docs/v1.1/powerdesigner/models/saas-recruitment-v1.1-pdm.pdm` | `950565fb84d8f8715a1d943716f4140e972756a86c067163436ba80622a1e23c` | 411 539 |
| `docs/v1.1/powerdesigner/models/source/schema-postgresql.sql` | `3cdcf68820ddedb77c954b5467f06282afd4650afc133c73061edb4a3c5efb7e` | 58 831 |

Originales del Formato 09, sin modificar. Coinciden con el SHA-256 registrado en la Fase 24:

| Original | SHA-256 |
|---|---|
| `GUÍA PRÁCTICA 09.docx` | `89d3f2783941b11aa7be0ccba7450cec5b6a821c480e528ac23d20e7e6c37c6d` |
| `Formato 09 Alcance del proyecto software.docx` | `1fe92a08110c9e4cad18644fa01d3baf38cba807a6db054c1a7276a69c0cfc63` |
| `F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx` | `1bb2fd17fbeea600f9fa6a36a2ceb4ed1c21b2f2fbba2c57a2ea8f618512a72a` |

Contrato ML congelado: *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2` y *threshold* `0.1679418172266036`. El binario del modelo **no se versiona**: se reconstruye desde el protocolo congelado con `recruitment_ml.serving.build_artifact`.

## Inventario (conteos en la base `2b97fe3`)

| Área | Contenido |
|---|---|
| Laravel | 151 archivos PHP en `app/` (17 modelos, 7 Policies), 18 migraciones y 3 archivos de rutas (93 rutas) |
| Frontend | 136 archivos `.ts`/`.tsx` en `resources/js/`, con 31 páginas Inertia |
| Servicio ML | 32 módulos Python en `ml-service/src/` y 18 archivos de prueba |
| Pruebas | 48 archivos PHPUnit, 18 de pytest, 6 de Vitest y 20 specs Cypress |
| QA | `phase-25-final-qa.md`, `phase-25-qa-matrix.md` y `testing/cypress-e2e.md` (§9) |
| UML (F22) | `docs/v1.1/uml/`: 11 documentos Markdown (especificación, inventario, trazabilidad y handoff) y 19 `.puml` |
| PowerDesigner (F23) | OOM (20 diagramas) y PDM (2), 22 PNG, 22 SVG, scripts, inventario y *checklist* |
| Académico (F24) | 3 originales, DOCX y PDF finales, `README.md`, `source-map.md` y `tools/` |
| Gobierno | `AGENTS.md`, `CLAUDE.md`, `docs/PROGRESS.md`, ADR-001 a ADR-004, 17 documentos de fase de v1.1 (F13 a F25, contando 15A–15C y la matriz de QA de la F25) más el de la F26, `documentation-update-map.md` y `scope-preliminary.md` |
| Release (F26) | `CHANGELOG.md`, `release-notes-v1.1.md`, este manifiesto, `final-acceptance-checklist.md` y `phase-26-release-closeout.md` |

## Resultados de QA (Fase 25, línea base auditada)

| Suite | Resultado |
|---|---|
| PHPUnit | 411 superadas · 8 omitidas · 0 fallidas · 1498 aserciones |
| pytest | 533 superadas |
| Componentes (Vitest) | 42/42 |
| TypeScript | 0 errores |
| *Build* | Correcto (aviso informativo de `fontaine`, ver deuda A-01) |
| Cypress | 20 specs · 85/85 |

La Fase 26 no cambió código ni volvió a ejecutar las suites.

## Deuda aceptada

| Severidad | Abiertos |
|---|---|
| BLOCKER | 0 |
| HIGH | 0 |
| MEDIUM | 0 |
| LOW | 8 |
| INFO | 9 |

Clasificación ítem por ítem (ACCEPTED / DEFERRED / RESOLVED / NOT APPLICABLE): [`phase-26-release-closeout.md`](phase-26-release-closeout.md) §12.

## Documentos finales

- [`../../CHANGELOG.md`](../../CHANGELOG.md) · [`release-notes-v1.1.md`](release-notes-v1.1.md) · [`final-acceptance-checklist.md`](final-acceptance-checklist.md) · [`phase-26-release-closeout.md`](phase-26-release-closeout.md)
- [`phase-25-final-qa.md`](phase-25-final-qa.md) · [`phase-25-qa-matrix.md`](phase-25-qa-matrix.md)
- [`../PROGRESS.md`](../PROGRESS.md) · [`documentation-update-map.md`](documentation-update-map.md) · [`scope-preliminary.md`](scope-preliminary.md)
- [`uml/README.md`](uml/README.md) · [`powerdesigner/README.md`](powerdesigner/README.md) · [`../academico/phase-24/README.md`](../academico/phase-24/README.md)
