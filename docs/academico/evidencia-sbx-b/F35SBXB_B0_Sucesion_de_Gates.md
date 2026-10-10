# F35-SBX-B — B0: sucesión de gates

> Subfase B0 de F35-SBX-B, versión 2 (09/10/2026). La versión 1 se auditó en el commit `66fb20814a048a28f7374fadb8fdad4ba1384778`; esta versión resuelve solo sus dos hallazgos (§5.7). Base: `develop` `8054fedf02f1b91ab6b6baa45c743725166af1a6`, que integra el cierre de F35-SBX-A con su commit E `61f94e23fc30b00a848a4558830b6d65f81dff87`. **Solo documentación**: B0 no crea pipeline, runner, almacenamiento SQLite, fixtures, modelos ni dependencias. Estado: **B0 IMPLEMENTADA, PENDIENTE DE REAUDITORÍA. F35-SBX-B NO INICIADA.**

## 1. Problema

Los validadores de las fases cerradas son *gates de alcance* de su propia fase: comparan el repositorio con su ancla y solo admiten las rutas, ramas y textos de gobierno que esa fase autorizó. El commit E congeló además los artefactos de F35-SBX-A, sin excepciones. Antes de B0 se comprobó con Git real, en clones desechables, que cualquier avance de B los hace fallar:

| Situación | Validadores que fallan | Causa |
|---|---|---|
| Rama nueva sin ningún cambio | `validate_f34b.py`, `validate_f34e.py`, `validate_f35sbx.py` | La excepción de F35-SBX-A para f30/f33/f34 solo vale en su rama, en `develop` o en `main` |
| Carpetas nuevas de B, también en `develop` | Los mismos tres | Rutas fuera de las listas de F34B/F34E y del alcance de F35-SBX-A |
| Registro de «F35-SBX-B INICIADA» en el gobierno | `validate_f30.py`, `validate_f33.py`, `validate_f34.py`, `validate_f34b.py`, `validate_f34e.py`, `validate_f35sbx.py` | Gobierno distinto del texto exacto que admitían |

Adaptar esos validadores reabriría el congelamiento auditado de A (su regla de historia rechaza cualquier commit posterior a E sobre el adaptador). B0 resuelve el conflicto sin modificarlos.

## 2. Decisión: gates históricos anclados y gate sucesor sobre HEAD

| Tipo | Qué es | Dónde se ejecuta | Qué demuestra |
|---|---|---|---|
| **Gate histórico** | `validate_f30.py`, `validate_f33.py`, `validate_f34.py`, `validate_f34b.py`, `validate_f34e.py`, `validate_f35sbx.py`, congelados | En un clon o worktree aislado, sobre su contexto de cierre compatible (§2.1) | Solo que el estado histórico auditado sigue verde |
| **Gate sucesor** | Validador de F35-SBX-B, a implementar en B | Sobre HEAD de la rama de B, de `develop` y de `main` | La validez del estado actual |
| **Validadores vigentes** | `validate.py`, `validate.py --cierre-f29`, `validate_f29.py`, `test_f32_safety.py`, `validate_f34a.py` | Sobre HEAD | Lo que ya comprobaban; si alguno fallara por diseño histórico, su reclasificación exige una decisión documentada |

### 2.1 Contexto de cierre compatible

Los gates de F35-SBX-A dependen del nombre de la rama, y `validate_f34a.py` necesita la referencia `develop`. Por eso un worktree con HEAD separado no basta: la ejecución anclada usa un clon temporal sin remoto, con `main` en el último commit de integración que los dejó verdes (`d63d094fb6f0eb335fee8d1766d33905004a1678`) y `develop` en `8054fedf02f1b91ab6b6baa45c743725166af1a6`, ejecuta los seis gates históricos y borra el clon. Nunca toca las ramas reales.

### 2.2 Principios

- **A.** Un PASS histórico solo demuestra el estado histórico correspondiente.
- **B.** Un PASS histórico nunca prueba que HEAD sea válido.
- **C.** El gate sucesor valida efectivamente HEAD, en todo lo que lista §3.
- **D.** Las excepciones son exactas: rutas o reglas concretas, nunca carpetas completas cuando se pueda evitar.
- **E.** F35-SBX-A permanece congelada: no se modifican `docs/academico/evidencia-sbx/**` ni `docs/academico/tools/f35sbx/**`.
- **F.** Los validadores históricos no son una dependencia mutable de B. Si B reutiliza alguna ayuda suya, primero verifica la integridad del archivo contra E y prefiere lógica propia, pequeña e independiente.

## 3. Requisitos del gate sucesor

A implementar en B, antes de cualquier pipeline. Todo estado Git o de sistema de archivos desconocido falla cerrado.

| Requisito | Comprobación |
|---|---|
| Alcance cerrado de B | Delta respecto de la base de B igual a la lista exacta de rutas autorizadas, sin subconjuntos ni superconjuntos |
| Invariantes vigentes | Los trece estados de gobierno, RF-01..RF-27, RF-23 humana y RF-29 experimental, sin cambios |
| Criterios SBX-01..SBX-18 | Recalculados uno por uno sobre HEAD según DH-B13 (§3.1), no deducidos del texto del gobierno |
| Dataset y provenance | `evidence.csv` de F34 y fixtures de A verificados por SHA-256 contra sus manifests y contra E |
| Integridad de A respecto de E | Bytes reales de `evidencia-sbx/**`, `tools/f35sbx/**` y de los cinco validadores históricos adaptados idénticos a sus blobs en E, sin archivos extra |
| Rutas nuevas de B | Solo las autorizadas en §6, con tipo y contenido de texto comprobados |
| Ciclo de vida de B | Textos exactos de apertura y cierre de B sobre su base, sin otro cambio de gobierno |
| Árbol, índice y archivos sin seguimiento | Comparados con la base y con E; renombrados como eliminación más alta |
| Bytes reales | Blob-id calculado sobre el archivo real, sin depender de `git diff` |
| Artefactos ocultos o ignorados | Recorrido del sistema de archivos; `.git/info/exclude` no oculta nada |
| Enlaces simbólicos y objetos especiales | Rechazados en rutas protegidas y nuevas |
| Flags del índice | Solo `H` en `git ls-files -v`: assume-unchanged (`h`), skip-worktree (`S`) y ambos (`s`) fallan |
| Historia y ascendencia | E como ancestro de HEAD y B0 integrada antes que B, identificadas por la historia y no por hashes futuros; historia completa sin simplificar |

### 3.1 DH-B13 — Sucesión normativa de la verificación G0-SBX

1. F34E, su matriz de criterios y `validate_f34e.py` permanecen congelados y no se modifican.
2. Los gates históricos anclados siguen acreditando únicamente sus estados históricos.
3. A partir de B, el gate sucesor sobre HEAD **recalcula individualmente** SBX-01 a SBX-18 con las comprobaciones materiales de la [matriz de criterios](../g0-sandbox/F34E_Matriz_Criterios_G0_SBX.md) (dataset, PII, árbol de archivos, `schema.json`, matriz de trazabilidad, decisión G0, runtime). No basta con comprobar las declaraciones textuales del gobierno.
4. Cada criterio produce como mínimo: ID, estado PASS o FAIL, fuente o evidencia, comprobación aplicada y, si falla, el motivo.
5. Un FAIL sustantivo, un criterio no evaluable, una evidencia ausente, un error de lectura o un estado Git o de sistema de archivos desconocido hacen fallar el gate (fail-closed).
6. Se distinguen dos clases de fallo:
   - **A) Fallo histórico o de alcance:** el validador congelado no reconoce una evolución autorizada de rutas o de ciclo de vida. No demuestra por sí solo una revocación sustantiva, pero no se ignora: obliga a ejecutar la evaluación sucesora completa sobre HEAD.
   - **B) Incumplimiento sustantivo:** uno o más de SBX-01..SBX-18 dejan de cumplirse. Aplica la regla de revocación y bloqueo de la [autorización de F35-SBX](../g0-sandbox/F34E_Autorizacion_F35_SBX.md).
7. La sucesión no reduce ni reinterpreta los criterios: solo sucede el **mecanismo** de verificación cuando el gate congelado ya no puede representar legítimamente la nueva fase.
8. G0-SBX sigue dependiendo del cumplimiento material de SBX-01..SBX-18. DH-B13 no declara ninguna aprobación nueva ni cambia el significado de G0-SBX.
9. Durante B0, mientras no existe el gate ejecutable de B, la comprobación transitoria se limita a esta documentación más una verificación directa y auditable de los 18 criterios (§8). No es un sustituto permanente.
10. Antes de cualquier implementación funcional de B, el gate sucesor tiene que existir o formar parte del primer incremento controlado de B, según la decisión final auditada.

## 4. Decisiones humanas de B

| Decisión | Resultado |
|---|---|
| DH-B01 | Sucesión de gates: gates históricos anclados más gate sucesor sobre HEAD (§2) |
| DH-B02 | Los gates históricos solo aportan evidencia complementaria del estado histórico (principios A y B) |
| DH-B03 | B usa rutas nuevas, separadas de A: `docs/academico/tools/f35sbxb/` y `docs/academico/evidencia-sbx-b/`. Sustituye la ubicación `tools/f35sbx/` que preveía §4 de los criterios de A, incompatible con el congelamiento de E |
| DH-B04 | Gate sucesor obligatorio sobre HEAD antes de cualquier implementación funcional (§3) |
| DH-B05 | Conformidad con el oráculo de A en dos niveles: proyección semántica A↔B e integridad nativa de B, nunca igualdad del informe completo ni de cadenas que dependen del run (§5.2) |
| DH-B06 | Purga definida de forma verificable y sin prometer borrado físico de memoria (§5.3) |
| DH-B07 | SQLite solo `:memory:`, con la configuración de §5.4 |
| DH-B08 | Aislamiento por tenant: una conexión y un run por organización sintética, tenant validado antes de escribir |
| DH-B09 | Integridad de A respecto de E en cada ejecución del gate sucesor |
| DH-B10 | Fail-closed: cualquier error, excepción o estado desconocido deja el run en `fallido`, sin resultado parcial, y el gate con código de salida distinto de cero |
| DH-B11 | Todas las restricciones de G0 real, G0-SBX y sus prohibiciones siguen vigentes |
| DH-B12 | B no autoriza ML, CAP-33, CAP-34, F36–F40 ni ninguna fase posterior |
| DH-B13 | Sucesión normativa de la verificación G0-SBX: el gate sucesor recalcula SBX-01..SBX-18 sobre HEAD (§3.1) |

## 5. Hallazgos de la auditoría del plan

### 5.1 B0-M01: los gates históricos no validan HEAD

Resuelto por DH-B01, DH-B02 y DH-B04: el gate sucesor sobre HEAD es obligatorio y los gates históricos son solo evidencia complementaria. DH-B13 (§3.1) añade la sucesión normativa de la verificación de G0-SBX.

### 5.2 B0-M02: conformidad con el oráculo en dos niveles

El informe de B no se compara byte a byte con los fixtures de A. En A, `event_hash`, `audit_hash` y `provenance_hash` se calculan sobre el objeto completo menos su propio campo, y ese objeto incluye `pipeline_run_id`, los identificadores de objeto y los instantes. Con otro run, esas cadenas cambian necesariamente. En cambio, `content_hash`, `hash_before` y `hash_after` usan el preimage cerrado del contrato (`hash_definition.canonical_fields`: `algorithm`, `criterion_ref`, `evidence_kind`, `origin_record_id`, `synthetic_organization_id`, `text`), que no contiene ningún identificador del run. Los hashes criptográficos ya calculados no se normalizan.

**Nivel 1 — Proyección semántica A↔B.** Igualdad exacta, por tenant, emparejando cada evidencia por su clave natural (`synthetic_organization_id`, `origin_record_id`) y no por identificadores de objeto:

| Objeto | Campos comparados |
|---|---|
| Evidencia | `synthetic_organization_id`, `criterion_ref`, `evidence_kind`, `text_synthetic` (tras T1), `hash_algorithm`, `content_hash`, `validation_status`, `review_status`, `source_type`, `environment` |
| Fuente | `origin_dataset_version`, `origin_file`, `origin_file_sha256`, `origin_record_id`, `source_type`, `synthetic_organization_id` |
| Provenance (estructural) | `provenance_kind`, `transformation_id`, `transformation_version`, `hash_before`, `hash_after`, la relación evidencia ↔ fuente ↔ origen F34 y el orden de la cadena |
| Revisión simulada | `review_scope`, `review_status`, `reviewer_type`, `scripted`, `simulation_actor` |
| Eventos | Secuencia ordenada de `state` y `error_code` del camino del oráculo, con `seq` contiguo |
| Auditoría | Secuencia ordenada de `action` |
| Conteos | Evidencias, fuentes, provenance, revisiones, eventos y entradas de auditoría por tenant |

Quedan **fuera** del nivel 1: `pipeline_run_id`, `run_kind`, `pipeline_version`, `seed` y `clock_start` cuando son propios de la ejecución; los identificadores de objeto asignados por el run (`synthetic_id`, `source_id`, `provenance_id`, `review_id`, `event_id`, `audit_id`, `target_ref`); los instantes (`at`, `created_at`, `recorded_at`, `reviewed_at`); las cadenas cuyo preimage incluye identificadores o instantes del run (`event_hash`/`prev_event_hash`, `audit_hash`/`prev_audit_hash`, `provenance_hash`/`prev_provenance_hash`); los estados propios de B (`fallido`, `purgado`), los fallos inyectados, el comprobante de purga, las rutas y los metadatos de plataforma.

**Nivel 2 — Integridad nativa de B.** B calcula sus propias cadenas con sus identificadores reales, con el mismo algoritmo de A (SHA-256 del JSON canónico del objeto sin su propio campo de hash y génesis de 64 ceros):

- se verifican internamente, eslabón por eslabón, y cualquier alteración las rompe;
- son reproducibles bajo el contrato de determinismo de B: dos ejecuciones dan los mismos bytes;
- no tienen por qué coincidir con las cadenas de A, porque incorporan otro run.

Los identificadores de B se derivan de forma estable solo del tenant, la semilla y el ordinal del reloj lógico, con un prefijo distinto del de A. Nunca se copia el `pipeline_run_id` de A para obtener el mismo hash. La regla exacta de identificadores y la lista definitiva de campos de cada nivel se congelan en el contrato de B antes de implementar, sin contradecir esta sección.

Para el determinismo, el informe usa JSON canónico en UTF-8, finales de línea LF, orden estable de claves y filas y el reloj lógico del run. No depende de rutas absolutas, de la hora real ni de diferencias entre Windows y macOS.

### 5.3 B0-M03: purga

La purga de B no es un borrado seguro de memoria ni una sanitización física de la RAM. Consiste en:

1. Almacenamiento exclusivamente SQLite `:memory:`.
2. Cierre explícito de cursores y conexiones.
3. Comprobación de que esas conexiones ya no se pueden usar.
4. Comprobación de que B no creó ningún archivo SQLite ni temporal persistente.
5. Un comprobante externo mínimo de finalización y purga en el informe.

La evidencia es de solo inserción durante toda la ejecución. El almacenamiento efímero se destruye cerrando la base `:memory:`, nunca con `DELETE` sobre tablas protegidas.

### 5.4 B0-M04: configuración de SQLite

- `PRAGMA foreign_keys = ON`, verificado tras activarlo.
- `temp_store` en memoria, verificado.
- Solo SQL fijo o parametrizado.
- `ATTACH`, exportación y persistencia prohibidos.
- Triggers que no se pueden modificar ni desactivar desde el pipeline.
- Una conexión y un run por tenant; tenant validado antes de cualquier escritura.

SQLite `:memory:` no es una frontera de seguridad frente a SQL arbitrario: la protección viene de que el pipeline solo ejecuta SQL fijo.

### 5.5 B0-L01: modelo de amenazas de B

| ID | Amenaza | Control | Prueba negativa | Resultado esperado |
|---|---|---|---|---|
| TSBB-01 | Contaminación con datos reales | Entradas solo con SHA-256 verificado contra E y el manifest de F34; reglas synthetic-only | Entrada alterada o con PII | FAIL; run `fallido` |
| TSBB-02 | Fuga entre tenants | Conexión y run por tenant; tenant validado antes de escribir | Fila de otro tenant | FAIL |
| TSBB-03 | Provenance manipulada | Cadena recalculada contra la proyección del oráculo | Eslabón alterado | FAIL; run `fallido` |
| TSBB-04 | Mutabilidad de la evidencia | Triggers que rechazan `UPDATE` y `DELETE` | `UPDATE` o `DELETE` sobre una tabla protegida | Error; run `fallido` |
| TSBB-05 | Replay | Identificador de run único y eventos contiguos | Evento reinsertado o run repetido | FAIL |
| TSBB-06 | Path traversal | Rutas fijas y normalizadas | Ruta con `..` o absoluta | FAIL |
| TSBB-07 | Artefactos ocultos | Delta exacto y recorrido del sistema de archivos | Archivo extra, ignorado o enlace | FAIL |
| TSBB-08 | Persistencia SQLite accidental | Solo `:memory:`; sin archivos antes ni después | Archivo `.db` o temporal creado | FAIL |
| TSBB-09 | Dependencia del runtime productivo | Solo biblioteca estándar autorizada; sin referencias a `app/`, `routes/`, `database/`, `storage/` ni `.env` | Importación o referencia prohibida | FAIL |
| TSBB-10 | Salida leída como scoring o recomendación | Esquema cerrado del informe; vocabulario prohibido | Campo de puntaje, orden o recomendación | FAIL |
| TSBB-11 | Fail-open | Toda excepción lleva a `fallido` y a código distinto de cero | Error inyectado en cada paso | FAIL controlado |
| TSBB-12 | No determinismo | Reloj lógico, orden explícito, JSON canónico | Dos ejecuciones con informes distintos | FAIL |
| TSBB-13 | Contenido activo o XSS | Texto plano sin marcado ni caracteres de control | Marcado HTML o script en el texto | FAIL |

### 5.6 B0-L02: estado documental de F35-SBX-A

Git confirma que F35-SBX-A, incluido su commit E, está integrada en `develop` y en `main`. B0 corrige solo la frase vigente que la daba como pendiente de publicación, en `CLAUDE.md` y `docs/PROGRESS.md`. `docs/academico/ACADEMIC_BASELINE.md` registra cierres de fase, conserva su texto del cierre de A y no cambia en B0. Los resultados de CI y los hashes de los merges se consultan en Git y GitHub.

### 5.7 Auditoría de B0 (versión 1)

La auditoría independiente del commit `66fb20814a048a28f7374fadb8fdad4ba1384778` concluyó «B0 NO APROBADA PARA INTEGRACIÓN» y autorizó corregir solo dos hallazgos documentales:

| Hallazgo | Severidad | Resolución |
|---|---|---|
| Sucesión normativa incompleta: B0 no exigía recalcular SBX-01..SBX-18 sobre HEAD | BLOCKER | DH-B13 (§3.1), nueva fila en §3 y verificación transitoria de los 18 criterios (§8) |
| Proyección de cadenas ambigua: las cadenas de A incluyen `pipeline_run_id` | MEDIUM | Dos niveles de comparación con campos exactos (§5.2) y DH-B05 actualizada |

## 6. Rutas de B

Autorizadas conceptualmente para la implementación; en B0 solo existe esta documentación.

| Ruta | Contenido admitido | Regla |
|---|---|---|
| `docs/academico/evidencia-sbx-b/` | Markdown y JSON de texto | Lista exacta de archivos, que fija el alcance de B |
| `docs/academico/tools/f35sbxb/` | Python con biblioteca estándar autorizada | Lista exacta de archivos; `sqlite3` solo aquí |

Pendiente para la implementación y fuera de B0: `sbxb_pipeline.py`, `sbxb_store.py`, el runtime SQLite, fixtures nuevos, modelos de ML y dependencias nuevas.

## 7. Gobierno y límites

- G0 real = NO APROBADA
- ADR-005 = PROPUESTA
- G0-SBX = APROBADA CON RESTRICCIONES
- F35 productiva = BLOQUEADA
- F35-SBX = HABILITADA, solo sandbox sintético
- F35-SBX-A = CERRADA E INTEGRADA
- F35-SBX-B = NO INICIADA hasta que B0 se reaudite y se autorice B
- F36–F40 = BLOQUEADAS
- Alcance C = BLOQUEADO
- Datos reales = PROHIBIDOS

B0 no cambia RF-01..RF-27, no modifica RF-23 y no habilita ranking, recomendación, scoring ni selección automática.

## 8. Validación de B0

- **Vigentes sobre HEAD**: `validate.py`, `validate.py --cierre-f29`, `validate_f29.py`, `test_f32_safety.py` y `validate_f34a.py` deben terminar sin fallas.
- **Históricos sobre HEAD**: fallan por diseño, por las causas de §1 (rama, rutas nuevas y gobierno). No se modifican para obtener PASS.
- **Históricos anclados** (§2.1): deben terminar sin fallas en su contexto de cierre.
- **Comprobaciones directas de B0**: delta exacto de B0 respecto de `develop`, integridad de A respecto de E, sin cambios en el runtime ni en las dependencias, sin flags del índice, `git diff --check` limpio y enlaces relativos válidos.

Hasta que exista el gate sucesor, estas comprobaciones directas sustituyen la validación de HEAD solo para B0, que es únicamente documental.

### 8.1 Verificación transitoria de SBX-01..SBX-18 (DH-B13, punto 9)

Recalculados uno por uno sobre HEAD de la rama de B0 el 09/10/2026, con la función `compute_sbx()` de `validate_f34e.py`, ejecutada en modo de solo lectura y sin generar bytecode, después de comprobar que el archivo es idéntico byte a byte a su blob en E. Esa función calcula cada criterio con las comprobaciones materiales de la matriz, independientemente del alcance Git histórico que hace fallar el validador completo sobre HEAD. Es una comprobación transitoria de B0, no un sustituto del gate sucesor.

| ID | Comprobación aplicada | Fuente | Resultado |
|---|---|---|---|
| SBX-01 | Reglas DQ-05 a DQ-07 sin violaciones y `source = synthetic` en el manifiesto | Dataset F34, `validate_f34.py` | PASS |
| SBX-02 | Reglas PII-01 a PII-03 sin violaciones | `validate_f34.py` | PASS |
| SBX-03 | Solo CSV, JSON o Markdown en `datos-sinteticos/` y `g0-sandbox/`; DQ-04 | Árbol de archivos, F34 | PASS |
| SBX-04 | Ningún archivo de audio ni de vídeo en esas carpetas | Árbol de archivos | PASS |
| SBX-05 | Ningún campo de score, ranking ni selección; LK-01 y LK-08 | `schema.json`, F34 | PASS |
| SBX-06 | Ningún campo de recomendación | `schema.json` | PASS |
| SBX-07 | Ningún campo de selección o contratación; RF-23 humana | `schema.json`, matriz de trazabilidad | PASS |
| SBX-08 | Fila RF-23 «humana» y baseline sin cambios frente a la base fija | `traceability-master.md`, Git | PASS |
| SBX-09 | Fila RF-21 presente, sin cambios, y regla RANK de F34A | Matriz de trazabilidad, `validate_f34a.py` | PASS |
| SBX-10 | Reglas CTX-01 a CTX-10 y `organization_token` en el contexto | F34, `schema.json` | PASS |
| SBX-11 | `provenance` en `evidence` y DQ-07 | `schema.json`, F34 | PASS |
| SBX-12 | G0-09 derivado como CUMPLIDO | Registros de F34C, `validate_f34b.py` | PASS |
| SBX-13 | G0-14 CUMPLIDO y ADR-005 canónico PROPUESTA | `validate_f34b.py`, ADR-005 | PASS |
| SBX-14 | `source_type = synthetic`, prefijo `[SINTÉTICO]` y advertencia del manifiesto | F34, `manifest.json` | PASS |
| SBX-15 | Ningún archivo del runtime referencia los datos sintéticos ni G0-SBX | Recorrido del runtime | PASS |
| SBX-16 | Runtime, dependencias, migraciones y baseline sin cambios frente a la base fija | Git | PASS |
| SBX-17 | La decisión G0 vigente declara el alcance C no habilitado | `F34B_Decision_G0.md` | PASS |
| SBX-18 | «G0 = NO APROBADA» y G0-02, G0-03 y G0-12 sin cerrar (PENDIENTE EXTERNO) | `F34B_Decision_G0.md`, `validate_f34b.py` | PASS |

Resultado: 18/18 PASS, sin criterios no evaluables. El validador completo `validate_f34e.py` sobre HEAD da 247 comprobaciones correctas y 1 falla, del tipo A de DH-B13 (alcance Git histórico), que no se ignora: es la que obliga a esta evaluación criterio a criterio.
