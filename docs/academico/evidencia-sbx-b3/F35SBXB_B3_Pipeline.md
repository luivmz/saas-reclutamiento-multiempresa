# F35-SBX-B — B3: pipeline determinista de evidencia sintética

> **Estado: B3 EN CONSTRUCCIÓN: contrato, diseño y baterías en RED, sin pipeline, gate ni transición de gobierno.** Fecha: 19/10/2026. Rama `feature/f35-sbx-b3-deterministic-pipeline`, desde `develop` = `ca36875938eca035c97205921ec5f9633381c571`.
>
> - **B2 = CERRADA**, exclusivamente en el alcance académico y sintético de F35-SBX. **F35-SBX-B = INICIADA** y **F35-SBX = HABILITADA**, sin cerrar.
> - B3 completa el alcance canónico pendiente de F35-SBX-B: la ejecución determinista del pipeline sintético de doce pasos que fijaron F35-SBX-A, B0 y B2. B3 no es ML, no abre ninguna fase posterior y no amplía el alcance autorizado.
> - Este incremento no se autoaprueba: lo decide la auditoría independiente sobre su ancla.
>
> Las secciones 1 a 5 registran la reconstrucción, el contrato y el diseño, escritos antes de la transición de gobierno, del pipeline y del gate (commit RED). La sección 6 añadirá los resultados.

## 1. Punto de partida verificado

### 1.1 Anclas

| Ancla | Commit | Qué es |
|---|---|---|
| F35-SBX-A, commit E | `61f94e23fc30b00a848a4558830b6d65f81dff87` | Contrato, fixtures, manifest y validador de A, congelados |
| B1 | `8e94a60274fe39ebda3e9961bc58036b389dfc00` | Ancla auditada de B1 |
| B1-FREEZE | `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` | Cierre de B1 |
| Candidato de B2 | `2472fd6fadfc0634ec68cbcb76cfc9fbfe105194` | Almacén efímero reauditado |
| B2-FREEZE, sucesor y B2-SUCCESSOR-FREEZE | `9961d2d65ed51a17c14aae5db0edb7d71c622c22`, `9d6fb157bb818574217e3675da1849e8d1010962` y `89694244b81b0bd84dbe6ae5d04b5c7a198bafef` | Capas de B2 |
| B2-GOVERNMENT-CLOSURE | `363273ead5794ea7a2dba74c011a0efd6d59e906` | Cierre de gobierno de B2 |
| Transición del cierre formal (R2-A) | `ddefb7dae00a7b57eb32c1046de634c0be2805de` | Blob del cierre de gobierno → blob del cierre formal |
| R2-A | `ad193f9565bf23246fadb9f85fc0ceddf8ddf698` | Ancla aprobada del registro del cierre formal de B2. Árbol `6ce03dc475d6430e4c199489a9d8cf4399bbef81` |

### 1.2 Integración de R2-A

| Hecho | Valor | Cómo se verificó |
|---|---|---|
| Rama publicada | `origin/chore/f35-sbx-b2-r2a-final-closure` = `ad193f9` | `git ls-remote` |
| Merge en `develop` | `ca36875938eca035c97205921ec5f9633381c571`, con padres `04895aa` y `ad193f9` | Objetos Git; `origin/develop` = `ca36875` |
| Merge en `main` | `8a00505c8a8adc6ebd125f3b30d3cf97dc03b475`, con padres `d5a4b4e` y `ca36875` | Objetos Git; `origin/main` = `8a00505` |
| Árboles | `ad193f9`, `ca36875` y `8a00505` tienen el árbol `6ce03dc4` | `git rev-parse <commit>^{tree}` |
| CI de `develop` | Workflow `tests`, run 62, id `39187931915`, `completed` / `success` | API pública de GitHub |
| CI de `main` | Workflow `tests`, run 63, id `39188344295`, `completed` / `success` | API pública de GitHub |

### 1.3 Qué falta

La evaluación de cierre de F35-SBX (19/10/2026) concluyó que F35-SBX-B no puede cerrarse: su objetivo, la ejecución determinista del pipeline, no existe. El gobierno integrado lo dice («sin pipeline funcional ni ML»), y lo confirman las fuentes de §2.1. B3 es ese pipeline y nada más.

## 2. Reconstrucción desde las fuentes canónicas

### 2.1 Fuentes

| Fuente | Qué fija para B3 |
|---|---|
| [Criterios de A](../evidencia-sbx/F35SBX_Criterios_Cierre_y_Revocacion.md), §4 | B ejecuta un pipeline con solo la biblioteca estándar, que recorre los doce pasos sobre los fixtures de A, con SQLite en memoria y triggers de solo inserción, auditoría encadenada, purga verificada, doble ejecución para demostrar determinismo y un informe con hashes y conteos; sin runtime, sin `tests/` y sin dependencias nuevas. CAP-33 y CAP-34 quedan para una autorización aparte |
| [Arquitectura de A](../evidencia-sbx/F35SBX_Arquitectura.md) | Los fixtures son un oráculo declarativo (`run_kind = oraculo_sbx_a`) para que B lo reproduzca. El flujo de doce pasos, los siete estados del camino y la asignación a B de la tabla en memoria, la solo inserción, `fallido` y `purgado`, y «el informe de cada run» |
| [Contratos](../evidencia-sbx/F35SBX_Contratos_Datos.md), [provenance](../evidencia-sbx/F35SBX_Provenance.md), [revisión simulada](../evidencia-sbx/F35SBX_Revision_Humana_Simulada.md) y [aislamiento](../evidencia-sbx/F35SBX_Aislamiento_y_Almacenamiento.md) de A | Campos, marcadores synthetic-only, hash de contenido, cadenas, regla de selección determinista, T1, revisión solo de integridad y procedencia, aislamiento por tenant, y la purga «se implementa en F35-SBX-B» |
| [`validate_f35sbx.py`](../tools/f35sbx/validate_f35sbx.py), congelado en E | La semántica exacta de cada comprobación de A (MAN, SCH, SYN, PII, MED, PER, CAP, HSH, PRV, ORI, ISO, RUN, REV, STO) y las funciones `canon`, `normalize_text`, `content_hash` y `chain_hash` |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md) | DH-B04 a DH-B13; §5.2, conformidad en dos niveles; §5.3, purga; §5.4, SQLite; §5.5, TSBB-01..TSBB-13; §6, `sbxb_pipeline.py` pendiente |
| [B1](../evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md), §5 | El cierre de B congela el gate y los artefactos de B; después, cada fase aporta su gate sucesor sobre HEAD |
| [Diseño de B2](../evidencia-sbx-b2/F35SBXB_B2_Diseno_Almacen.md) y [`sbxb_store.py`](../tools/f35sbxb2/sbxb_store.py) | La API interna del almacén, el ciclo de vida, la identidad `SBB*`, la purga con comprobante y, en §1 y §10, que el pipeline y el double-run completo son de fases posteriores de F35-SBX-B |
| [Sucesor de B2](../evidencia-sbx-b2-sucesor/F35SBXB_B2_Sucesor.md), §2 (AF-M01) | El gate válido sobre HEAD ejecuta, sobre el estado actual, el gate vigente congelado con su código verificado y clasifica con exactitud su falla de clase A |
| [R2-A](../evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md) | El gate vigente sobre HEAD, el blob de gobierno del cierre formal y la cadena monotónica de cuatro etapas |

### 2.2 Los doce pasos

Reconstruidos de la arquitectura de A (§3), con sus comprobaciones en `validate_f35sbx.py` y su ejecución en B sobre la API de B2:

| Paso | Qué hace (A) | Entrada | Salida en B3 | Comprobaciones de A que reproduce |
|---|---|---|---|---|
| 1 | Fixture sintético verificado contra el manifest | Bytes del fixture del tenant y manifest de A | Auditoría `fixture_verificado` | MAN: SHA-256 y tamaño del manifest, JSON sin claves duplicadas, cabecera del fixture |
| 2 | Validación del esquema cerrado | Fixture y contrato `f35sbx-contract-1.0.0` | Evento `validando` y auditoría `esquema_validado` | SCH y CON: subconjunto cerrado de JSON Schema del contrato publicado |
| 3 | Validación synthetic-only: seis marcadores | Registros del fixture | Auditoría `sintetico_verificado` | SYN, PII, MED, PER y CAP |
| 4 | Cálculo del hash de contenido | Filas F34 de origen | Auditoría `hash_calculado` | HSH y ORI: `hash_before` sobre el texto F34, `content_hash` sobre T1, selección determinista |
| 5 | Registro de provenance | Evidencia calculada y revisión declarada | Fuente, evidencia, revisión y procedencia (`append_evidence`), evento `registrado` y auditoría `provenance_registrada` | PRV |
| 6 | Transformación T1 | Lo persistido | Evento `transformado` | HSH (`hash_before`, `hash_after`) |
| 7 | Validación del tenant | Lo persistido y el tenant | Auditoría `tenant_validado` | ISO |
| 8 | Revisión humana simulada | Revisiones persistidas | Eventos `en_revision` y `revisado`, auditoría `revision_simulada_registrada` | REV |
| 9 | Resultado experimental | Evidencias persistidas | `validation_status` de cada evidencia | SCH |
| 10 | Auditoría experimental encadenada | Auditoría persistida | Cadena verificada eslabón por eslabón | RUN y HSH |
| 11 | Cierre e inmutabilidad del run | Run activo | Evento `completado` y auditoría `ejecucion_cerrada`; instantánea de las ocho tablas | HSH (cadenas) |
| 12 | Purga o retención | Almacén cerrado | Comprobante de purga (§2.5) | STO |

Los siete estados del camino son `pendiente`, `validando`, `registrado`, `transformado`, `en_revision`, `revisado` y `completado`; `pendiente` lo crea `create_run`. Las ocho acciones de auditoría siguen el orden del oráculo: `fixture_verificado`, `esquema_validado`, `sintetico_verificado`, `hash_calculado`, `provenance_registrada`, `tenant_validado`, `revision_simulada_registrada` y `ejecucion_cerrada`.

### 2.3 Provenance, hashes y conteos

- **Selección determinista:** las dos primeras filas de `evidence.csv` del tenant con `state = vinculada`, `source_type = synthetic` y `source_type_ev` en `formulario`, `nota_entrevista` o `prueba`, ordenadas por `evidence_id` (provenance de A, §3).
- **Hash de contenido** `f35sbx-content-sha256-v1`: SHA-256 del JSON canónico con `algorithm`, `synthetic_organization_id`, `origin_record_id`, `criterion_ref`, `evidence_kind` y `text`. `hash_before` usa el texto F34 original y `content_hash` = `hash_after`, el texto tras T1.
- **T1:** Unicode NFC y espacios colapsados; pura, determinista e idempotente.
- **Cadenas:** eventos, procedencia y auditoría guardan el hash del anterior (el primero, 64 ceros) y su propio hash, calculado sin ese campo.
- **Conteos por tenant:** dos evidencias, dos fuentes, dos procedencias, dos revisiones, siete eventos y ocho entradas de auditoría.

### 2.4 Conformidad con el oráculo (B0 §5.2)

- **Nivel 1, proyección semántica A↔B.** Igualdad exacta por tenant, emparejando cada evidencia por su clave natural (`synthetic_organization_id`, `origin_record_id`): los campos de evidencia, fuente, procedencia estructural y revisión de B0 §5.2, la secuencia de `state` y `error_code` de los eventos con `seq` contiguo, la secuencia de `action` de la auditoría y los conteos. Quedan fuera los identificadores, los instantes y las cadenas cuyo preimage los incluye.
- **Nivel 2, integridad nativa de B.** Las cadenas propias de B, con sus identificadores `SBB*`, se verifican eslabón por eslabón con el algoritmo de A, son reproducibles entre ejecuciones y no tienen por qué coincidir con las de A.

### 2.5 Purga (B0 §5.3 y diseño de B2, §9)

1. Almacenamiento exclusivamente `:memory:`.
2. Cierre explícito de la conexión.
3. Comprobación de que la conexión ya no se puede usar.
4. Comprobación de que no se creó ningún archivo SQLite ni temporal persistente.
5. Un comprobante mínimo de finalización y purga en el informe.

La purga no es un borrado seguro de memoria: la base deja de ser alcanzable por la API y por la conexión, y nada más se afirma.

### 2.6 Determinismo

Informe en JSON canónico (UTF-8, LF, claves ordenadas), con el reloj lógico del run y sin rutas absolutas, hora real ni diferencias de plataforma. Identificadores de B derivados solo del tenant, la semilla y los ordinales del reloj lógico. Dos ejecuciones dan los mismos bytes (B0 §5.2; TSBB-12; diseño de B2, §10).

### 2.7 TSBB-01 a TSBB-13 (B0 §5.5)

| ID | Amenaza | Control | Prueba negativa |
|---|---|---|---|
| TSBB-01 | Contaminación con datos reales | Entradas con SHA-256 verificado; reglas synthetic-only | Entrada alterada o con un dato personal: run `fallido` |
| TSBB-02 | Fuga entre tenants | Una conexión y un run por tenant; tenant validado antes de escribir | Fila de otro tenant: FAIL |
| TSBB-03 | Provenance manipulada | Cadena recalculada contra la proyección del oráculo | Eslabón alterado: run `fallido` |
| TSBB-04 | Mutabilidad de la evidencia | Solo inserción | Reescritura de una fila protegida: error y run `fallido` |
| TSBB-05 | Replay | Run único y eventos contiguos | Evento reinsertado o run repetido: FAIL |
| TSBB-06 | Path traversal | Rutas fijas y normalizadas | Ruta con `..` o absoluta: FAIL |
| TSBB-07 | Artefactos ocultos | Delta exacto y recorrido del sistema de archivos | Archivo extra, ignorado o enlace: FAIL |
| TSBB-08 | Persistencia SQLite accidental | Solo `:memory:`, sin archivos antes ni después | Archivo `.db` o temporal: FAIL |
| TSBB-09 | Dependencia del runtime productivo | Solo biblioteca estándar autorizada, sin referencias al runtime | Importación o referencia prohibida: FAIL |
| TSBB-10 | Salida leída como puntaje o sugerencia | Esquema cerrado del informe y vocabulario prohibido | Campo de puntaje, orden o sugerencia: FAIL |
| TSBB-11 | Fail-open | Toda excepción lleva a `fallido` y a código distinto de cero | Error inyectado en cada paso: FAIL controlado |
| TSBB-12 | No determinismo | Reloj lógico, orden explícito, JSON canónico | Dos ejecuciones con informes distintos: FAIL |
| TSBB-13 | Contenido activo | Texto plano sin marcado ni caracteres de control | Marcado HTML en el texto: FAIL |

### 2.8 Fallo cerrado (DH-B10)

Cualquier error, excepción o estado desconocido deja el run en `fallido`, sin resultado parcial, y el proceso con código de salida distinto de cero. Que el evento `fallido` exista en la base se informa con exactitud, no se supone (diseño de B2, §6.2).

### 2.9 Discrepancias encontradas, no materiales

| Observación | Por qué no es una contradicción | Tratamiento en B3 |
|---|---|---|
| Los instantes del oráculo no intercalan eventos y auditoría en el orden de los pasos | B0 §5.2 deja los instantes fuera del nivel 1 | B3 usa su propio reloj lógico, un minuto por paso |
| La API de B2 persiste la revisión declarada junto con su evidencia | Es la decisión Q7 de B2, auditada: fuente, evidencia, revisión y procedencia en una transacción | El paso 5 la persiste; el paso 8 la verifica y registra sus eventos y su auditoría |
| El almacén solo admite el texto ya transformado | Q7 y §11 de B2: el contenido persistido es T1 de su fila F34 | T1 se calcula en el paso 4; el paso 6 la verifica sobre lo persistido |
| `validation_status` admite `rechazado`, pero todo fallo lleva el run a `fallido` | DH-B10 y A (arquitectura, §3): sin resultado parcial | B3 nunca persiste un resultado parcial; el camino del oráculo es `valido` |
| B0 §6 nombraba `tools/f35sbxb/` | B2 fijó carpetas exactas propias (Q2), auditadas | B3 usa `tools/f35sbxb3/` y `evidencia-sbx-b3/` |

## 3. Contrato de B3

### 3.1 Alcance

- Un pipeline Python, solo con la biblioteca estándar, que recorre los doce pasos sobre los fixtures de A para `ORG-S1`, `ORG-S2` y `ORG-S3`, con el almacén de B2 sin modificarlo.
- Un informe canónico por ejecución, la doble ejecución, la conformidad en dos niveles, la purga con comprobante, los negativos TSBB y el fallo inyectado en cada paso.
- El gate sucesor de B3 sobre HEAD y su batería.
- Una única transición de gobierno que registra a B3 implementada (§4.11).

### 3.2 Exclusiones

El pipeline no calcula puntajes ni sugiere, ordena, selecciona ni descarta personas; no usa datos reales, OCR, extracción automática de documentos, embeddings ni búsqueda semántica; y no infiere rasgos de ninguna persona. Tampoco toca la aplicación Laravel ni React, el runtime, `tests/`, las dependencias, la CI, el dataset F34, los artefactos de A ni ninguna capa congelada. Sin endpoints ni migraciones. CAP-33 y CAP-34 siguen fuera.

### 3.3 Invariantes

1. Estados de gobierno sin cambios: G0 real = NO APROBADA; G0-02, G0-03 y G0-12 = PENDIENTE EXTERNO; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; F35 productiva, F36–F40 y alcance C = BLOQUEADOS; datos reales = PROHIBIDOS.
2. RF-23 sigue siendo decisión final humana y RF-29 sigue experimental e informativo. El baseline RF-01 a RF-27 no cambia.
3. F35-SBX-B sigue INICIADA y F35-SBX sigue HABILITADA. B3 no registra el cierre de ninguna de las dos.
4. Las capas congeladas, de A a R2-A, conservan sus bytes y su historia.
5. SQLite solo `:memory:`, dentro del almacén de B2.

### 3.4 Delta permitido frente a `ca36875`

| Ruta | Estado | Contenido |
|---|---|---|
| `docs/academico/evidencia-sbx-b3/F35SBXB_B3_Pipeline.md` | A | Este documento |
| `docs/academico/tools/f35sbxb3/sbxb_pipeline.py` | A | Pipeline |
| `docs/academico/tools/f35sbxb3/test_sbxb_pipeline.py` | A | Pruebas del pipeline PT01..PT30 |
| `docs/academico/tools/f35sbxb3/validate_f35sbxb3.py` | A | Gate sucesor sobre HEAD |
| `docs/academico/tools/f35sbxb3/test_f35sbxb3.py` | A | Batería del gate CB01..CB47 |
| `CLAUDE.md`, `docs/PROGRESS.md` | M | Solo mediante la transición de §4.11 |

### 3.5 Criterios de cierre de B3

B3 queda aceptado como candidato si se cumple todo:

- el pipeline completa los tres runs con conformidad de nivel 1 y nivel 2, y dos ejecuciones dan el mismo informe byte a byte;
- cada paso con fallo inyectado termina en `fallido`, sin resultado parcial y con un diagnóstico determinista;
- las pruebas del pipeline dan 30/30 y la batería del gate 47/47;
- el gate de B3 da todo en verde sobre la rama y sobre los merges `--no-ff` en `develop` y `main`;
- los gates anclados siguen en verde y los congelados sobre HEAD fallan solo por la clase A prevista (§4.13);
- `validate.py`, `--cierre-f29`, F29, F32, F33, F34 y F34A siguen en verde, F34E en su 247/1 histórico, y enlaces, MANIFEST, evidencias y `git diff --check` sin discrepancias.

### 3.6 Criterios derivados para el cierre posterior de F35-SBX-B

Derivados solo de los contratos existentes, para el incremento terminal que el equipo autorice después de B3:

| Criterio | Fuente |
|---|---|
| B0, B1 y B2 cerrados; B3 aprobado e integrado con CI en verde | Gobierno; protocolo de cada incremento |
| Pipeline de doce pasos, conformidad en dos niveles, doble ejecución, informe con hashes y conteos, y purga verificada | Criterios de A, §4; B0 §5.2 y §5.3 |
| TSBB-01..TSBB-13 con su prueba negativa | B0 §5.5 |
| Congelamiento de B: un commit fija el gate y los artefactos de B | B1 §5 |
| Registro del cierre en el gobierno con su propia transición y su gate sucesor | B0 §3, «ciclo de vida de B»; DH-B13 |
| Registro del cierre en `ACADEMIC_BASELINE.md` | B0 §5.6; B1 §3 |
| G0-SBX vigente, sin ningún hecho de revocación REV-01..REV-14 | Criterios de A, §3 |

B3 no aplica ninguno de los tres últimos: es el incremento posterior el que lo hace.

### 3.7 Amenazas propias de B3

| Amenaza | Qué la rechaza | Casos |
|---|---|---|
| Un paso alterado, omitido o reordenado | Conformidad de nivel 1 recalculada por el gate (CNF) y pruebas del pipeline | PT04, CB16, CB17, CB18 |
| Fixture manipulado | Paso 1, integridad de A (INT) y gate de B2 (MAT) | PT08, CB15 |
| Provenance, hash o conteo incorrectos | Conformidad de nivel 1 y nivel 2 | PT05, PT11, CB19, CB21 |
| Tenant o escenario cruzados | Pasos 1, 2 y 7, almacén y conformidad | PT09, PT10, CB22, CB23 |
| Informe no determinista o doble ejecución divergente | DET, FAL y PT02, PT03 | PT18, CB24 |
| Purga falsa | PUR y la observación en el proceso de PT06 | PT15, CB25 |
| Cadena de auditoría alterada | Nivel 2 | PT05, PT11, CB20 |
| Resultado parcial presentado como completo | FAL y PT19..PT30 | CB26 |
| Capacidad prohibida en el informe o en el código | Esquema cerrado del informe (PIP), DEP y SEM | PT17, CB27, CB28 |
| Cambio de gobierno no autorizado | GOV y SEM | CB04..CB11, CB34..CB42 |

Cada ataque al pipeline de la batería desactiva también las comprobaciones propias del pipeline que lo detendrían, para que lo que se pruebe sea el rechazo del gate.

## 4. Diseño

### 4.1 Archivos y commits

- **Base y rama:** `develop` integrado `ca36875`, rama `feature/f35-sbx-b3-deterministic-pipeline`, en un worktree hermano del checkout del equipo.
- **Commits:**
  1. **RED.** Este documento y las dos baterías; sin pipeline ni gate, las dos fallan enteras.
  2. **Transición de gobierno.** Un solo padre; cambia exactamente `CLAUDE.md` y `docs/PROGRESS.md` (§4.11).
  3. **GREEN.** El pipeline, el gate, que registra la transición (ya existe: sin autorreferencia), y los resultados de §6. Es el commit que completa la capa.

### 4.2 API de B2 utilizada

| Función | Uso en B3 |
|---|---|
| `open_tenant_store(tenant)` | Un almacén por tenant y escenario |
| `create_run(store, seed, clock_start)` | Principal inmutable y evento `pendiente` |
| `append_event(store, state, at, error_code, audit_action)` | Estados del camino, atómicos con su auditoría; `fallido` con su código |
| `append_audit(store, action, at)` | Acciones de auditoría sin evento propio |
| `append_evidence(store, evidence)` | Fuente, evidencia, revisión y procedencia en una transacción |
| `list_events`, `list_audit`, `list_evidence`, `read_run`, `current_state` | Verificaciones de los pasos 6 a 10 |
| `snapshot(store)` | Las ocho tablas en JSON canónico, tras el cierre |
| `purge(store)` y `diagnostic(store)` | Comprobante de purga o diagnóstico del cierre excepcional |

Nada más: el pipeline no abre conexiones ni emite SQL. `sqlite3` solo lo importa el almacén.

### 4.3 Carga verificada del almacén

El pipeline lee los bytes de `sbxb_store.py`, exige su SHA-256 registrado (el blob `09ac588eb442d80f5270e641cb98cdfe0169166c` del candidato de B2) y los ejecuta como módulo desde esos bytes, sin `__pycache__` ni ruta de importación. Es la única ejecución dinámica del pipeline. Al nombrar el almacén, el gate de B2, congelado, falla en DEP: es la clase A prevista de B3 (§4.13), que el diseño de B2 anticipaba («el llamador es código del pipeline de B, auditado»). No se oculta el nombre ni se carga por otra vía.

### 4.4 Ejecución por tenant

Escenarios del oráculo: semilla y `clock_start` de cada fixture de A (`ORG-S1`, `ORG-S2` y `ORG-S3`, con `clock_start` `2026-10-07T09:00:00`). El paso `k` usa el instante lógico `clock_start` + `k` minutos.

| Paso | Llamadas al almacén |
|---|---|
| Apertura | `open_tenant_store` con el contexto del tenant del contrato; `create_run` (`pendiente`) |
| 1 | `append_audit(fixture_verificado)` |
| 2 | `append_event(validando, esquema_validado)` |
| 3 | `append_audit(sintetico_verificado)` |
| 4 | `append_audit(hash_calculado)` |
| 5 | `append_evidence` por evidencia; `append_event(registrado, provenance_registrada)` |
| 6 | `append_event(transformado)` |
| 7 | `append_audit(tenant_validado)` |
| 8 | `append_event(en_revision)`; `append_event(revisado, revision_simulada_registrada)` |
| 9 y 10 | Solo lecturas y verificación |
| 11 | `append_event(completado, ejecucion_cerrada)`; `snapshot` |
| 12 | `purge`; una llamada posterior debe fallar con `E-PURGADO` |

Instantes de cada evidencia: `created_at` y `recorded_at` = instante del paso 5; `reviewed_at` = instante del paso 8.

### 4.5 Informe canónico

Un único objeto JSON canónico, en UTF-8 y con LF final, por la salida estándar. No escribe archivos. Esquema cerrado `f35sbxb3-report-1.0.0`:

- `report_version`, `result` (`completado` o `fallido`), `pipeline_version`, `contract_version`, `run_kind`, `environment` y `source_type`, tomados del almacén;
- `inputs`: versión del dataset y SHA-256 del manifest F34, de `evidence.csv`, del manifest y del contrato de A, de cada fixture y del almacén;
- `runs`, solo si el resultado es `completado`: por tenant, el escenario, el estado final, los doce pasos con su instante, las ocho tablas, sus conteos, el resultado de la conformidad de nivel 1 y nivel 2, el comprobante de purga y el resultado de la llamada posterior a la purga;
- `failure`, solo si es `fallido`: tenant, paso, código, mensaje fijo y el comprobante o diagnóstico del almacén. Sin tablas ni ningún resultado parcial.

Código de salida 0 si el resultado es `completado`; 1 si es `fallido`; 2 si la invocación no es válida.

### 4.6 Doble ejecución

El gate ejecuta el pipeline dos veces, en procesos nuevos, y exige los mismos bytes. PT02 lo repite dentro de un proceso, con almacenes nuevos.

### 4.7 Comprobante de purga

El del almacén (diseño de B2, §9): `closure_kind = purga`, `final_state = completado`, `connection = CLOSED`, `post_close_check = ProgrammingError`, `file_backed = false`, conteos iguales a los de la instantánea, `last_event_hash` igual al hash del evento `completado` y `receipt_hash` recalculable. Tras la purga, `list_events` debe fallar con `E-PURGADO`.

### 4.8 Conformidad de nivel 1 y nivel 2

El pipeline la calcula y la informa, y el gate la recalcula por su cuenta desde el informe y los fixtures de A, sin fiarse del resultado que trae el informe. El nivel 1 recalcula además, desde `evidence.csv`, la selección, T1, `hash_before` y `content_hash`.

### 4.9 Inyección de fallo

`--fallo ORG-SX:N` inyecta un error controlado al empezar el paso `N` (1 a 12) del tenant indicado. El run queda `fallido` con código `E-INYECTADO` si aún está activo, el almacén se purga o cierra, el informe no trae tablas y el proceso termina con código 1. Dos ejecuciones con el mismo fallo dan los mismos bytes.

### 4.10 Negativos TSBB

| ID | Dónde |
|---|---|
| TSBB-01, 02, 03, 04, 05, 06, 08, 10, 11, 12 y 13 | Pruebas del pipeline (§5.1) |
| TSBB-07 | Batería del gate: base SQLite sin seguimiento (CB32) y artefacto ignorado (CB33) en la carpeta de B3 |
| TSBB-09 | Batería del gate: importación no autorizada en el pipeline (CB28) y otro módulo que nombra el almacén (CB29) |

### 4.11 Transición de gobierno

`B3_GOVERNANCE_BLOB` resulta de aplicar al blob del cierre formal (`0f9d516fd129ba83058076e6bffb293e9be1fac1` en `CLAUDE.md` y `60a891fbf7967d4bcc9342ed43b10f1b587540e7` en `docs/PROGRESS.md`) una lista cerrada de reemplazos literales, cada bloque antiguo presente exactamente una vez:

```text
CLAUDE.md y docs/PROGRESS.md, la frase del estado vigente
  antes:   … B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E INTEGRADA, sin pipeline funcional ni ML.
  después: … B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA, sin ML.

CLAUDE.md y docs/PROGRESS.md, la frase de los incrementos (con enlaces relativos a su ruta)
  antes:   …; su cierre formal está registrado en [`evidencia-sbx-b2-cierre-formal`](…).
  después: …; su cierre formal está registrado en [`evidencia-sbx-b2-cierre-formal`](…); su incremento B3 (pipeline determinista de doce pasos sobre el almacén de B2) está IMPLEMENTADO, registrado en [`evidencia-sbx-b3`](…/evidencia-sbx-b3/F35SBXB_B3_Pipeline.md).

docs/PROGRESS.md, cabecera
  antes:   Última actualización: 2026-10-18 (…; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA).
  después: Última actualización: 2026-10-19 (…; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA, B3 IMPLEMENTADA).

docs/PROGRESS.md, nota de historia
  antes:   … El 18/10/2026 pasó a B2 cerrada e integrada, con su cierre de gobierno auditado e integrado y su cierre formal registrado.
  después: … El 18/10/2026 pasó a B2 cerrada e integrada, con su cierre de gobierno auditado e integrado y su cierre formal registrado. El 19/10/2026 pasó a B3 implementada: el pipeline determinista de doce pasos sobre el almacén de B2.
```

El texto no menciona el estado de auditoría de B3, así que sigue siendo cierto después de integrarse. Ningún otro texto cambia. `B3_TRANSITION` es el commit que introduce el blob en las dos rutas a la vez; se registra en el gate en el commit GREEN.

### 4.12 Gate sucesor

`validate_f35sbxb3.py`: solo biblioteca estándar, aislado (`python -I`, al que se relanza solo), con objetos Git verificados y fallo cerrado.

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado; sin variables de Git que redirijan el repositorio; historia completa, sin injertos ni objetos de reemplazo |
| CTX | Rama de B3, `develop` o `main`, y `ca36875` como ancestro de HEAD |
| ANC | Anclas de §1.1 íntegras y en cadena; los merges `eb02c2d`, `04895aa` y `ca36875` con sus padres y árboles; los blobs de gobierno de las cuatro etapas anteriores |
| HIS | El gate de R2-A, con los bytes de su blob en `ad193f9`, anclado sobre `ad193f9` en un clon temporal sin remoto: 14/0, FRZ en `ad193f9` y GOV en `ddefb7d` |
| R2A | El mismo gate sobre HEAD: solo su clase A exacta (§4.13), con recuentos, violaciones visibles y líneas INFO |
| MAT | El gate de B2, verificado contra el candidato, sobre HEAD: solo su clase A exacta, con DEP limitado al pipeline y SBX-01..SBX-18 en verde |
| INT | Integridad de las capas congeladas, de B1 a R2-A, desde sus anclas, en cada commit, el índice y el disco |
| FLG | Ningún flag en el índice |
| GOV | Transición única y monotónica en cinco etapas (§4.14) |
| SEM | Semántica del gobierno y de este documento, con las piezas verificadas del gate de B1 (§4.15) |
| ALC | Alcance exacto frente a `ca36875` en HEAD, el índice y el árbol de trabajo; sin archivos sin seguimiento; carpetas de la capa exactas |
| FRZ | Nivel B: un único commit posterior a `ca36875` completa la capa; desde él, nada de la capa cambia |
| DEP | Biblioteca estándar autorizada por archivo; la única ejecución dinámica de cada archivo es su carga verificada; ningún `.py` fuera del pipeline y de B2 nombra el almacén |
| PIP | Pipeline completo: código 0, informe con esquema cerrado, tres runs `completado` |
| DET | Segunda ejecución en un proceso nuevo: mismos bytes |
| CNF | Conformidad de nivel 1 y nivel 2 recalculada por el gate |
| PUR | Comprobantes verificados, `E-PURGADO` tras la purga y ningún archivo nuevo en el árbol de trabajo |
| TSB | Las pruebas del pipeline, exactamente PT01..PT30 en verde |
| FAL | Fallo inyectado en cada paso de `ORG-S1`: `fallido`, código 1, sin tablas y bytes repetibles |

### 4.13 Clase A prevista

Sobre un HEAD válido de B3, dos gates congelados fallan, y deben fallar:

- **Gate de B2:** CTX (solo en la rama), B1F (los commits nuevos), SCP (las cinco rutas nuevas en tres planos: 66), DYN (P25), GOV (contenido distinto y «b2 cerrada») y DEP, con una sola violación, la del pipeline. SBX pasa.
- **Gate de R2-A:**
  - CTX solo en la rama;
  - GCL con las notas del cierre de gobierno que solo explica B3: su CTX en la rama, su MAT con DEP y con SCP 66, y su ALC con las rutas de B3;
  - MAT con DEP y SCP 66;
  - GOV con la regla 3 en los commits de B3 que llevan el nuevo blob, más las seis del estado efectivo;
  - SEM, porque el cierre de B2 ya no dice «sin pipeline funcional ni ML» y la cabecera añade B3;
  - ALC con las rutas de B3.

  SUC, HIS, INT, FLG, FRZ, DEP y ANC pasan.

El gate de B3 predice cada falla desde el estado observado, con su recuento y sus violaciones visibles, y exige que no haya ninguna otra. Lo que esas fallas enmascaran lo reponen las reglas propias: ALC, INT, GOV, SEM y DEP. Los valores exactos se miden antes de escribir el gate y se registran en §6.

### 4.14 GOV: cinco etapas

Las cuatro de R2-A (B1, B2, cierre de gobierno y cierre formal) más `B3_GOVERNANCE_BLOB`:

- cada blob lo introduce solo su transición, en las dos rutas a la vez;
- la transición de B3 tiene un solo padre, con el blob del cierre formal, desciende de `ca36875` y cambia exactamente las dos rutas;
- todo descendiente conserva el blob; la transición derivada coincide con la registrada;
- HEAD, el índice y el disco tienen el blob de B3.

### 4.15 SEM

Con las piezas verificadas del gate de B1, en el gobierno de HEAD:

- una única sección «Estado vigente F34E», con los trece estados exactos;
- F35-SBX-B solo INICIADA, y ninguna declaración de cierre de F35-SBX;
- la declaración canónica de B2 cerrada y la de B3 implementada; sin «sin pipeline funcional»;
- B3 solo IMPLEMENTADA: se rechazan «cerrada», «congelada», «integrada», «aprobada», «productiva», «publicada» y «desplegada», y su reapertura;
- ninguna declaración contradictoria ni afirmación positiva de una capacidad prohibida en lo vigente ni en las líneas nuevas frente al blob del cierre formal.

Este documento pasa las mismas comprobaciones: sin datos personales, afirmaciones positivas ni declaraciones contradictorias.

### 4.16 Raíz de confianza y ancla

- **Registradas en el gate:** las anclas de §1.1, los merges, las transiciones de gobierno y, en el commit GREEN, la de B3.
- **Derivada y registrada fuera:** el commit que completa la capa, que informa la línea INFO de FRZ. Es el ancla de B3; ningún archivo guarda su propio hash.
- Los merges en `main` no son ancestros de esta rama: se registran en §1.2 y la batería prueba la integración `--no-ff`.

### 4.17 Lo que no cambia

- Las capas congeladas, de A a R2-A, y sus validadores, que no se ejecutan con constantes alteradas.
- `ACADEMIC_BASELINE.md`, que solo registra cierres.
- Los estados de G0, G0-SBX, ADR-005, F35 productiva, F36–F40, alcance C y datos reales.

## 5. Pruebas

### 5.1 Pruebas del pipeline

`test_sbxb_pipeline.py`: importa el pipeline de su carpeta y ejecuta cada caso en memoria o en un proceso nuevo, sin escribir archivos.

| Caso | Comprueba |
|---|---|
| PT01 | Ejecución completa: código 0, tres runs `completado`, esquema cerrado del informe |
| PT02 | Doble ejecución en un proceso, con almacenes nuevos: mismos bytes |
| PT03 | Doble ejecución en procesos nuevos: mismos bytes |
| PT04 | Nivel 1 igual al oráculo de A en los tres tenants |
| PT05 | Nivel 2: cadenas de eventos, procedencia y auditoría recalculadas |
| PT06 | Comprobantes de purga, y en el propio proceso cada almacén inutilizable (`E-PURGADO`) |
| PT07 | Identificadores `SBB*` del espacio `<org>-<semilla>`, sin ninguno de A |
| PT08 | TSBB-01: fixture alterado, run `fallido` en el paso 1 |
| PT09 | TSBB-01 y TSBB-02: dato personal y fila de otro tenant, rechazados |
| PT10 | TSBB-02: fixture de otro tenant, run `fallido` |
| PT11 | TSBB-03: eslabón de procedencia alterado, nivel 2 en falla |
| PT12 | TSBB-04: reescritura de una evidencia ya registrada, run `fallido` |
| PT13 | TSBB-05: evento repetido y run repetido, rechazados |
| PT14 | TSBB-06: ruta con `..` o absoluta, rechazada |
| PT15 | TSBB-08: comprobante con `file_backed` distinto de `false`, rechazado |
| PT16 | TSBB-13: marcado HTML en el texto, rechazado |
| PT17 | TSBB-10: informe con un campo de puntaje, rechazado por el esquema |
| PT18 | TSBB-12: dos informes distintos, detectados |
| PT19..PT30 | TSBB-11: fallo inyectado en cada paso 1..12, `fallido` sin resultado parcial y repetible |

### 5.2 Batería del gate

`test_f35sbxb3.py`: cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta el gate con `python -I`.

Las reglas del pipeline (PIP, DET, CNF, PUR, TSB y FAL) se abrevian como «las seis del pipeline».

| Caso | Escenario | Reglas en falla esperadas |
|---|---|---|
| CB01 | Estado válido; el ancla derivada es el commit que completa la capa | Ninguna |
| CB02 | Merge `--no-ff` en `develop` (`ca36875`) y de `develop` en `main` (`8a00505`) | Ninguna en ambos |
| CB03 | Commit posterior sin cambios de contenido | Ninguna |
| CB04 | Sexto blob de gobierno tras la transición | GOV |
| CB05 | Modificar → restaurar el gobierno tras la transición | GOV |
| CB06 | Vuelta al gobierno del cierre formal | GOV, SEM y ALC |
| CB07 | Gobierno que declara B3 «CERRADA» | GOV y SEM |
| CB08 | Historia reconstruida con el mismo contenido | GOV (transición distinta de la registrada); FRZ informa otra ancla |
| CB09 | Transición que también cambia otra ruta | GOV |
| CB10 | Transición hecha en un merge | GOV |
| CB11 | Transición repartida en dos commits | GOV |
| CB12 | Gate de R2-A alterado y confirmado | INT, ALC y R2A |
| CB13 | Almacén de B2 alterado y confirmado | INT, ALC, MAT, R2A y las seis del pipeline |
| CB14 | Modificar → restaurar el documento del cierre de gobierno | INT y R2A |
| CB15 | Fixture de A alterado en el árbol de trabajo | INT, ALC, MAT, R2A y las seis del pipeline |
| CB16 | Pipeline que omite un paso | ALC, FRZ, CNF y TSB |
| CB17 | Pipeline que reordena dos pasos | ALC, FRZ, CNF y TSB |
| CB18 | Pipeline que altera la auditoría de un paso | ALC, FRZ, CNF y TSB |
| CB19 | Pipeline que informa una procedencia incorrecta | ALC, FRZ, CNF y TSB |
| CB20 | Pipeline que altera la cadena de auditoría | ALC, FRZ, CNF y TSB |
| CB21 | Pipeline que informa un conteo incorrecto | ALC, FRZ, CNF y TSB |
| CB22 | Pipeline que cruza tenants | ALC, FRZ, PIP, CNF, PUR y TSB |
| CB23 | Pipeline que cruza escenarios | ALC, FRZ, CNF y TSB |
| CB24 | Pipeline no determinista | ALC, FRZ, DET, FAL y TSB |
| CB25 | Pipeline con purga falsa y comprobante coherente | ALC, FRZ y TSB |
| CB26 | Pipeline que presenta un resultado parcial como completo | ALC, FRZ, FAL y TSB |
| CB27 | Pipeline con un campo de puntaje en el informe | ALC, FRZ, PIP y TSB |
| CB28 | Pipeline que importa un módulo no autorizado (TSBB-09), confirmado | FRZ y DEP |
| CB29 | Otro módulo del repositorio nombra el almacén (TSBB-09) | ALC, DEP, MAT y R2A |
| CB30 | Dependencia (`composer.json`) modificada y confirmada | ALC, MAT y R2A |
| CB31 | Runtime (`routes/web.php`) modificado y confirmado | ALC, MAT y R2A |
| CB32 | Base SQLite sin seguimiento en la carpeta de B3 (TSBB-07 y TSBB-08) | ALC, FRZ, MAT y R2A |
| CB33 | Artefacto ignorado en la carpeta de B3 (TSBB-07) | ALC y FRZ |
| CB34 | Gobierno que declara G0 real aprobada | GOV, SEM, MAT y R2A |
| CB35 | Gobierno que quita las restricciones de G0-SBX | GOV, SEM, MAT y R2A |
| CB36 | Gobierno que aprueba ADR-005 | GOV, SEM, MAT y R2A |
| CB37 | Gobierno que desbloquea F36–F40 | GOV, SEM, MAT y R2A |
| CB38 | Gobierno que da por habilitado el alcance C | GOV, SEM, MAT y R2A |
| CB39 | Gobierno que admite datos reales | GOV, SEM, MAT y R2A |
| CB40 | Gobierno que admite puntajes y selección automática de personas | GOV, SEM, MAT y R2A |
| CB41 | Gobierno que declara «F35-SBX-B CERRADA» | GOV, SEM, MAT y R2A |
| CB42 | Gobierno que declara «F35-SBX = CERRADA» | GOV, SEM, MAT y R2A |
| CB43 | Clon superficial | Todas salvo FLG y DEP (fallo cerrado) |
| CB44 | `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` hacia un clon limpio | ENT |
| CB45 | skip-worktree en `CLAUDE.md` con un cambio que `git status` no ve | GOV, FLG, MAT y R2A |
| CB46 | HEAD separado | CTX, MAT y R2A |
| CB47 | B3 sin el merge de integración de R2-A (`ca36875`) | CTX, GOV y FRZ |

En CB25 el comprobante falsificado es coherente con el informe: solo lo delatan la observación en el proceso (PT06, dentro de TSB) y el congelamiento del código (FRZ y ALC). Si un conjunto resulta distinto al medirlo en GREEN, se corrige con su causa registrada en §6, como en las capas anteriores.

## 6. Resultados

Pendientes: se registrarán en el commit que completa la capa.
