# F35-SBX-B — B3: pipeline determinista de evidencia sintética

> **Estado: B3 IMPLEMENTADA: pipeline determinista de doce pasos, gate sucesor y transición de gobierno. Candidato a auditoría independiente.** Fecha: 19/10/2026. Rama `feature/f35-sbx-b3-deterministic-pipeline`, desde `develop` = `ca36875938eca035c97205921ec5f9633381c571`.
>
> - **B2 = CERRADA**, exclusivamente en el alcance académico y sintético de F35-SBX. **F35-SBX-B = INICIADA** y **F35-SBX = HABILITADA**, sin cerrar.
> - B3 completa el alcance canónico pendiente de F35-SBX-B: la ejecución determinista del pipeline sintético de doce pasos que fijaron F35-SBX-A, B0 y B2. B3 no es ML, no abre ninguna fase posterior y no amplía el alcance autorizado.
> - Este incremento no se autoaprueba: lo decide la auditoría independiente sobre su ancla.
>
> Las secciones 1 a 5 registran la reconstrucción, el contrato y el diseño, escritos antes de la transición de gobierno, del pipeline y del gate (commit RED). El commit que completa la capa solo los corrige donde la implementación o la medición lo exigieron, con su causa en §6.2. La sección 6 registra los resultados.

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

El pipeline no calcula puntajes ni sugiere ni ordena ni selecciona ni descarta personas; no usa datos reales, OCR, extracción automática de documentos, embeddings ni búsqueda semántica; y no infiere rasgos de ninguna persona. Tampoco toca la aplicación Laravel ni React, el runtime, `tests/`, las dependencias, la CI, el dataset F34, los artefactos de A ni ninguna capa congelada. Sin endpoints ni migraciones. CAP-33 y CAP-34 siguen fuera.

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
| B0, B1 y B2 cerrados; la aprobación de B3 en su auditoría independiente y su integración con CI en verde | Gobierno; protocolo de cada incremento |
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

Escenarios del oráculo: semilla y `clock_start` de cada fixture de A (`ORG-S1`, `ORG-S2` y `ORG-S3`, con `clock_start` `2026-10-07T09:00:00`). El paso que corre en la posición `k` usa el instante lógico `clock_start` + `k` minutos: un paso reordenado no rompe el reloj, y lo rechaza la conformidad.

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

El gate ejecuta el pipeline tres veces, en procesos nuevos, y exige los mismos bytes. PT02 lo repite dentro de un proceso, con almacenes nuevos.

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
| ENT | Intérprete aislado; sin variables de Git que redirijan el repositorio; historia completa, sin injertos ni objetos de reemplazo; el repositorio, a no más de tres niveles de clones compartidos, para que los gates anclados anidados no superen el límite de alternates de Git |
| CTX | Rama de B3, `develop` o `main`, y `ca36875` como ancestro de HEAD |
| ANC | Anclas de §1.1 íntegras y en cadena, con la transición de B3; los merges `eb02c2d`, `04895aa` y `ca36875` con sus padres y árboles; los blobs de gobierno registrados de las cinco etapas |
| HIS | El gate de R2-A, con los bytes de su blob en `ad193f9`, anclado sobre `ad193f9` en un clon temporal sin remoto y con sus alternates aplanados: 14/0, FRZ en `ad193f9` y GOV en `ddefb7d` |
| R2A | El mismo gate sobre HEAD: su salida es la que da su propia lógica, cargada de los bytes verificados de su blob, sobre el estado observado, con recuentos, violaciones visibles y líneas INFO; y solo falla por su clase A (§4.13) |
| MAT | El gate de B2, verificado contra el candidato, sobre HEAD: solo su clase A exacta, con DEP limitado al pipeline y SBX-01..SBX-18 en verde |
| INT | Integridad de las capas congeladas, de A a R2-A, desde sus anclas, en cada commit, el índice y el disco |
| FLG | Ningún flag en el índice |
| GOV | Transición única y monotónica en cinco etapas (§4.14) |
| SEM | Semántica del gobierno y de este documento, con las piezas verificadas del gate de B1 (§4.15) |
| ALC | Alcance exacto frente a `ca36875` en HEAD, el índice y el árbol de trabajo; sin archivos sin seguimiento; carpetas de la capa exactas |
| FRZ | Nivel B: un único commit posterior a `ca36875` completa la capa; desde él, nada de la capa cambia |
| DEP | Biblioteca estándar autorizada por archivo; la única ejecución dinámica de cada archivo es su carga verificada (el almacén en el pipeline; los gates de B1 y de R2-A en el gate); ningún `.py` fuera del pipeline y de B2 nombra el almacén |
| PIP | Pipeline completo: código 0, informe canónico con esquema cerrado, entradas verificadas, filas con los campos del contrato de A y tres runs `completado` |
| DET | Dos ejecuciones más, en procesos nuevos: los mismos bytes |
| CNF | Conformidad de nivel 1 y nivel 2 recalculada por el gate, desde los fixtures de A en su ancla y `evidence.csv`, leídos como objetos Git verificados |
| PUR | Comprobantes verificados, `E-PURGADO` tras la purga y ningún archivo nuevo, ni en el árbol de trabajo ni en el temporal exclusivo, nuevo y vacío, con el que corren el pipeline y sus pruebas |
| TSB | Las pruebas del pipeline, exactamente PT01..PT30 en verde |
| FAL | Fallo inyectado en cada paso de `ORG-S1`: `fallido`, código 1, sin tablas y bytes repetibles |

### 4.13 Clase A prevista

Sobre un HEAD válido de B3, dos gates congelados fallan, y deben fallar:

- **Gate de B2:** CTX (solo en la rama), B1F (los commits nuevos), SCP (las cinco rutas nuevas en tres planos: 66), DYN (P25), GOV (contenido distinto y «b2 cerrada») y DEP, con una sola violación, la del pipeline. SBX pasa.
- **Gate de R2-A:**
  - CTX solo en la rama;
  - GCL con las notas del cierre de gobierno que solo explica B3: su CTX en la rama, su MAT con DEP y con SCP 66, y su ALC con las rutas de B3;
  - MAT con DEP y SCP 66;
  - GOV con la regla 3 en los commits de B3, los que no están en la historia de `ca36875`, más las seis del estado efectivo;
  - SEM, porque el cierre de B2 ya no dice «sin pipeline funcional ni ML» y la cabecera añade B3;
  - ALC con las rutas de B3.

  SUC, HIS, INT, FLG, FRZ, DEP y ANC pasan.

El gate de B3 calcula cada salida prevista con la lógica del propio gate congelado, cargada de los bytes verificados de su blob, exige que la observada coincida en recuentos, violaciones visibles y líneas INFO, y la clasifica con reglas propias: una falla fuera de la clase A, o una clase A distinta de la prevista, hace fallar R2A o MAT. En GCL, la predicción omite la nota de SUC: su ausencia la garantiza el SUC de R2-A en verde, que la clasificación exige, porque el ALC de B2-SUCCESSOR-FREEZE nombra siempre la capa de R2-A, ajena al alcance del cierre de gobierno. Lo que esas fallas enmascaran lo reponen las reglas propias: ALC, INT, GOV, SEM y DEP. Los valores medidos están en §6.4.

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
| CB06 | Vuelta al gobierno del cierre formal | GOV, SEM, ALC y R2A |
| CB07 | Intento de declarar B3 «CERRADA» | GOV y SEM |
| CB08 | Historia reconstruida con el mismo contenido | GOV (transición distinta de la registrada); FRZ informa otra ancla |
| CB09 | Transición que también cambia otra ruta | GOV |
| CB10 | Transición hecha en un merge | GOV |
| CB11 | Transición repartida en dos commits | GOV |
| CB12 | Gate de R2-A alterado y confirmado | INT, ALC y R2A |
| CB13 | Almacén de B2 alterado y confirmado | INT, ALC, R2A y las seis del pipeline |
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
| CB34 | Intento de declarar G0 real aprobada | GOV, SEM, MAT y R2A |
| CB35 | Intento de quitar las restricciones de G0-SBX | GOV, SEM, MAT y R2A |
| CB36 | Intento de aprobar ADR-005 | GOV, SEM, MAT y R2A |
| CB37 | Intento de desbloquear F36–F40 | GOV, SEM, MAT y R2A |
| CB38 | Intento de habilitar el alcance C | GOV, SEM, MAT y R2A |
| CB39 | Intento de admitir datos reales | GOV, SEM, MAT y R2A |
| CB40 | Intento de habilitar puntajes y selección automática de personas | GOV, SEM, MAT y R2A |
| CB41 | Intento de declarar «F35-SBX-B CERRADA» | GOV, SEM, MAT y R2A |
| CB42 | Intento de declarar «F35-SBX = CERRADA» | GOV, SEM, MAT y R2A |
| CB43 | Clon superficial | Todas salvo FLG y DEP (fallo cerrado) |
| CB44 | `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` hacia un clon limpio | ENT |
| CB45 | skip-worktree en `CLAUDE.md` con un cambio que `git status` no ve | GOV, FLG, MAT y R2A |
| CB46 | HEAD separado | CTX, MAT y R2A |
| CB47 | B3 sin el merge de integración de R2-A (`ca36875`) | CTX, GOV y FRZ |

En CB25 el comprobante falsificado es coherente con el informe: solo lo delatan la observación en el proceso (PT06, dentro de TSB) y el congelamiento del código (FRZ y ALC). Si un conjunto resulta distinto al medirlo en GREEN, se corrige con su causa registrada en §6, como en las capas anteriores.

## 6. Resultados

### 6.1 Commits

| Commit | Padre | Contenido | Resultado |
|---|---|---|---|
| `831ebd5abc4f89de88a059896433b52b30df31d4` | `ca36875` | Contrato y diseño (§1 a §5) y las baterías PT01..PT30 y CB01..CB47 (RED) | Pruebas del pipeline 0/30, sin pipeline. Batería del gate 0/47, con 29 ejecuciones: el gate no existía, y 19 casos ni siquiera podían prepararse |
| `fa5664a0a3660519744a32b320822ecc396b1619` | `831ebd5` | Transición de gobierno (§4.11): solo `CLAUDE.md` y `docs/PROGRESS.md`, con los blobs `8e908661b96a557d078d0036a41e319b2a3bb76c` y `4146a9d331f2d3f6240aedd599eb0238c578f761` | `B3_TRANSITION`, registrada en el gate del commit siguiente |
| El que completa la capa (este) | `fa5664a` | Pipeline, gate, correcciones de §6.2 y estos resultados (GREEN) | Gate 19/0; pruebas del pipeline 30/30; batería 47/47 |

Ese tercer commit es el ancla de nivel B de B3: lo informa la línea INFO de FRZ, y su hash no se guarda en ningún archivo.

### 6.2 GREEN y correcciones

Los resultados se midieron en clones temporales sin remoto. La batería, los controles de mutación y la regresión, sobre commits desechables cuyo árbol solo difiere del de este commit en esta sección 6; el gate, las pruebas del pipeline y las comprobaciones que dependen de los documentos, también sobre uno con el árbol exacto de este commit.

- **Comprobación semántica previa de este documento.** Antes de ejecutar el gate, las mismas piezas que usa SEM encontraron en el documento del commit RED tres afirmaciones positivas, cuatro declaraciones contradictorias y un estado de B3 distinto de implementada. Eran falsos positivos de redacción: en §3.2 las comas cortaban la negación de una enumeración, las filas CB34..CB42 describían cada ataque como una declaración y §3.6 pedía la aprobación de B3. Se reescribieron sin tocar SEM, con la convención de R2-A («Intento de …») y la negación sin comas, y la comprobación dio 0 en las tres.
- **Pipeline.** El paso que corre en la posición `k` usa el instante de esa posición (§4.4). Con un instante fijo por paso, el ataque que reordena dos pasos (CB17) fallaba en el almacén por un instante no monótono y no llegaba a la conformidad que ese caso prueba. El paso 11 llama a `level1` con los dos argumentos de su interfaz pública, la que usan las pruebas y los ataques de la batería.
- **Revisión del gate contra la batería, antes de ejecutarla.** El almacén se deriva del árbol de HEAD, porque en el clon superficial de CB43 no está la base y DEP tiene que pasar. Los `.py` rastreados se filtran por su sufijo, porque con `--literal-pathspecs` un patrón no se expande. La regla 3 de R2-A es de clase A en los commits que no están en la historia de `ca36875` (CB47 monta B3 sobre `ad193f9`). Y PUR compara cada comprobante con el tenant que declara su run (CB22).
- **Primera ejecución del gate sobre un HEAD simulado: 16/3.** HIS exigía que, sobre su propio HEAD, el cierre de gobierno no fallara, cuando el gate de R2-A exige que falle exactamente en lo previsto. INT tomaba por inesperadas las subcarpetas `contrato/` y `fixtures/` de la capa A. Y SEM vio el documento anterior a la reescritura. Con HIS como el gate de R2-A y una subcarpeta admitida si contiene archivos de su capa, el gate dio 19/0.
- **Autoauditoría (§6.8), antes de la batería.** El pipeline y sus pruebas corren con un temporal exclusivo, nuevo y vacío, que PUR exige vacío al terminar (TSBB-08 también fuera del repositorio). CNF comprueba además el principal del run y el contexto del tenant, y el nivel 2, que los instantes sean monótonos y no anteriores al reloj lógico. DET ejecuta el pipeline dos veces más, no una, para que un informe que dependa del PID no coincida por azar (CB24). Una ejecución de la batería que probaba el gate anterior a estos cambios se detuvo a los 20 minutos, sin ningún caso terminado.
- **Primera batería completa: 1/47 (48 ejecuciones del gate en seis tandas, unas dos horas).** Todos los casos, salvo CB43, fallaron además en HIS, y CB06 en R2A. CB13 no falló en MAT. Ninguno de los tres era una regresión de B3:
  - **HIS.** Git no sigue más de seis niveles de alternates, y cada gate anclado clona con objetos compartidos. La batería se ejecutó desde un clon compartido, así que el caso quedaba a tres niveles; el clon anclado de HIS sumaba uno y la cadena congelada que anida el gate de R2-A, tres más. El gate de R2-A anclado a esa profundidad dio 13/1 (el cierre de gobierno anclado no acreditaba B2-SUCCESSOR-FREEZE); un nivel más arriba, 14/0. Era el hallazgo H5 (§6.8), corregido en RED → GREEN: el clon de HIS aplana sus alternates, que listan directamente cada almacén de la cadena, y ENT exige no más de tres niveles bajo el repositorio, el máximo con el que la cadena anidada del gate de R2-A sobre HEAD cabe en el límite. Una cadena de clones compartidos fallaba en el séptimo nivel y, aplanando el cuarto, leyó los siete; CB01 y CB03, desde el mismo clon compartido, pasaron.
  - **CB06.** El gate de R2-A también rechaza la vuelta al blob del cierre formal, por su regla 4: un segundo commit lo reintroduce fuera de su transición. Es una detección correcta que la expectativa de RED no había previsto: CB06 espera ahora GOV, SEM, ALC y R2A.
  - **CB13.** El gate de B2 no comprueba los bytes de su propio almacén, cosa que hace B2-FREEZE, así que MAT pasa. La alteración la detectan INT («capa B2»), R2A y las seis reglas del pipeline: CB13 espera ahora INT, ALC, R2A y las seis del pipeline.
- **Batería completa con el gate corregido: 47/47,** sin otras expectativas de RED corregidas que las de CB06 y CB13, desde un clon compartido como el de la primera batería y en dos tandas: la primera terminó 17 casos (CB01..CB13 y CB15..CB18, con CB02 en `develop` y en `main`) antes de un corte de la sesión, y la segunda, los 30 restantes (CB14 y CB19..CB47) en seis tandas paralelas. En total, 48 ejecuciones del gate, todas sobre el mismo árbol.

### 6.3 Pipeline

| Medida | Resultado |
|---|---|
| Informe | 38 372 bytes, SHA-256 `7efc00ee307c932955f2f3cc10b56dc08c14cd408c1fc7b43f612a712d174967`, resultado `completado`. Los mismos bytes en el proceso (PT02), en procesos nuevos (PT03 y DET) y en cada clon |
| Runs | `SBBR-ORG-S1-0020261008`, `SBBR-ORG-S2-0020261009` y `SBBR-ORG-S3-0020261010`: los doce pasos; 1, 1, 7, 2, 2, 2, 2 y 8 filas en las ocho tablas; nivel 1 conforme y nivel 2 íntegro, recalculados por el gate |
| Purga | Tres comprobantes `purga` con `completado`, `CLOSED`, `ProgrammingError` y `file_backed` falso, y `E-PURGADO` en la llamada posterior. Ningún archivo nuevo en el árbol de trabajo ni en el temporal exclusivo |
| Fallo inyectado | En cada paso 1..12 de `ORG-S1`: `fallido` con `E-INYECTADO`, código 1, sin tablas y los mismos bytes en dos procesos. El almacén queda purgado, con `final_state` `fallido` en los pasos 1..11 y `completado` en el 12, cuyo run ya había terminado |
| Pruebas | `test_sbxb_pipeline.py`: 30/30 |

### 6.4 Clase A observada sobre HEAD

Medida en la rama y comparada con la base `ca36875` (`develop`), en clones limpios sin remoto:

| Gate congelado sobre HEAD | Resultado (base) | Fallas |
|---|---|---|
| R2-A | 8/6 (14/0) | La clase A de §4.13, exacta: CTX 1, la rama; GCL 4, las notas del cierre de gobierno por la rama, por el DEP del pipeline, por SCP 66 y por las rutas de B3; MAT 2, CTX y DEP materiales y SCP 66 frente a 51; GOV 8, la regla 3 en `fa5664a` y en el commit que completa la capa y las seis del estado efectivo; SEM 3, la declaración del cierre de B2 en cada ruta y la cabecera; ALC 3, las rutas de B3 en cada plano |
| B2-GOVERNMENT-CLOSURE | 7/6 (8/5) | CTX 1, solo la rama; SUC 1, MAT 3 (2), GOV 10 (9), SEM 3 y ALC 3, como sobre la base salvo la regla material del pipeline en MAT y los commits y las rutas de B3 en GOV y ALC |
| B2-SUCCESSOR-FREEZE | 10/2 (10/2) | VIG 5 y ALC 3, como sobre la base |
| Sucesor | 4/3 (4/3) | CON 1, MAT 2 y ALC 3, como sobre la base |
| B2-FREEZE | 6/4 (6/4) | HIS 10 (7: los tres commits de B3), ARB 1, IDX 1 y DSK 2, solo por `CLAUDE.md` y `docs/PROGRESS.md` |
| B2 | 112/7 (114/5) | CTX 1, solo la rama; B1F 16 (13: los tres commits de B3); SCP 66 (51: las cinco rutas de B3 en tres planos); DEP 1, el pipeline; DYN 1 (P25); GOV 3, como sobre la base. SBX en verde |
| B1 | 105/54 (106/53) | CTX 1, solo la rama; GOV 1 y los 51 casos PB, idénticos a los de la base; SCP 90 (75: las cinco rutas de B3 en tres planos) |
| B1-FREEZE | 0/2 (0/2) | FRZ 31 (28: los tres commits de B3) y B1, como sobre la base |
| F35-SBX-A | Termina con `StopIteration` (igual sobre la base) | Su autoprueba de mutaciones busca la frase canónica del ciclo de vida de A, que el gobierno vigente ya no tiene literal, y termina con `StopIteration` sobre HEAD y sobre `ca36875`. No depende de B3: anclado en su commit E y con su rama da 846/0 (§6.6) |

En `develop` y `main` CTX pasa: sobre los merges `--no-ff` (CB02 y la regresión), el gate de R2-A da 9/5 y el de B2, 113/6, con las mismas reglas de clase A sin CTX. R2A clasifica exactamente la primera fila y MAT la sexta; las demás se reponen con INT, GOV y SEM (§4.13).

### 6.5 Controles de mutación

La batería se ejecutó contra gates debilitados a propósito, en commits desechables, con el caso que debe detectar cada mutación:

| Mutación del gate | Caso | Resultado |
|---|---|---|
| CNF sin efecto | CB16 | Detectada: CB16 deja de fallar en CNF |
| DET sin comparar las ejecuciones | CB24 | Detectada: deja de fallar en DET |
| FAL sin efecto | CB26 | Detectada: deja de fallar en FAL |
| TSB sin efecto | CB25 | Detectada: la purga falsa ya solo falla en ALC y FRZ |
| PUR sin efecto | CB22 | Detectada: deja de fallar en PUR |
| PIP sin esquema ni entradas | CB27 | Detectada: deja de fallar en PIP |
| R2A sin la clasificación de clase A | CB30, CB46 y CB34 | CB30 no la detecta: ahí el gate de R2-A falla también en SUC, fuera de la clase A, y basta la comparación exacta. CB46 y CB34 sí: R2-A falla solo en reglas de clase A con contenido ajeno (CTX con «HEAD separado» y SEM con un estado sobredeclarado), y los dos dejan de fallar en R2A |
| MAT acepta cualquier salida del gate de B2 | CB31 | Detectada: deja de fallar en MAT |
| GOV sin comparar la transición derivada con la registrada | CB08 | Detectada: CB08 pasa a PASS |
| SEM sin la declaración ni el ciclo de vida de B3 | CB07 | Detectada: deja de fallar en SEM |
| INT sin la capa A | CB15 | Detectada: deja de fallar en INT |
| Sin FRZ | CB28 | Detectada: deja de fallar en FRZ |
| DEP sin buscar el nombre del almacén | CB29 | Detectada: deja de fallar en DEP |
| Sin ALC | CB33 | Detectada: deja de fallar en ALC |
| CTX sin exigir `ca36875` | CB47 | Detectada: deja de fallar en CTX |

Las quince mutaciones se detectan, con 17 ejecuciones del gate. Dos tandas anteriores de estos controles no ejecutaron ningún caso: la lista de casos tenía fin de línea CRLF y la batería no reconocía sus identificadores. No se cuentan.

### 6.6 Validación

| Comprobación | Resultado |
|---|---|
| `validate_f35sbxb3.py` | 19/0 en la rama, en el merge `--no-ff` en `develop` y en el de `develop` en `main`, con el mismo informe. FRZ informa el commit que completa la capa; GOV deriva `fa5664a`, igual a la registrada; HIS da 14/0, con el ancla derivada `ad193f9` y la transición `ddefb7d`; R2A observa 8/6 en la rama y 9/5 en `develop` y `main`, siempre con las reglas previstas; MAT, 112/7 en la rama y 113/6 en `develop` y `main`, con SCP 66 de 66 previstas y SBX en verde |
| `test_sbxb_pipeline.py` | 30/30 |
| `test_f35sbxb3.py` | 47/47 (§6.2) |
| Gates anclados en clones limpios sin remoto | R2-A sobre `ad193f9`: 14/0. B2-GOVERNMENT-CLOSURE sobre `363273e`: 13/0. B2-SUCCESSOR-FREEZE sobre `8969424`: 12/0. Sucesor sobre `9d6fb15`: 7/0. B2-FREEZE sobre `9961d2d`: 10/0. B2 sobre `2472fd6`: 119/0. B1 sobre `8e94a60`: 159/0. B1-FREEZE sobre `3d9b783`: 14/0, con SBX-01..SBX-18 en 18/18. F35-SBX-A sobre su commit E, `61f94e2`, con su rama: 846/0 |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py`, `test_f32_safety.py`, `validate_f33.py` y `validate_f34.py` | 225/0, OK, 451/0 y 403/0 |
| `validate_f34a.py` | 108/0 |
| `validate_f34e.py` | 247/1, igual que sobre `ca36875`: la falla histórica de la regla GIT. Su lista de rutas no autorizadas por DH-02 pasa de 29 a 34, las cinco de esta capa, sin que desaparezca ninguna, y el resto del mensaje no cambia. Criterios SBX: 18/18 |
| Enlaces relativos | 1143 en `docs/academico` y 1547 en todo el repositorio, 0 rotos |
| MANIFEST y evidencias | 61 hashes y 0 discrepancias; 81 hashes de las evidencias de las prácticas 03, 05, 08 y 11, 0 discrepancias |
| `git diff --check` | Limpio frente a `ca36875`, `ad193f9` y `2472fd6` |
| Delta frente a `ca36875` | Exactamente las cinco rutas de la capa (A) y las dos de gobierno (M); ninguna fuera de `docs/academico` |
| Gobierno de HEAD | Los trece estados sin cambios y F35-SBX-B INICIADA; B2 CERRADA y B3 IMPLEMENTADA en las dos rutas, sin «sin pipeline funcional»; RF-23 sigue humana y RF-29, experimental e informativa |

### 6.7 Sucesión vigente

| Gate | Papel | Dónde | Resultado en clon limpio |
|---|---|---|---|
| `validate_f35sbxb3.py` | Gate sobre HEAD, en esta rama, `develop` y `main` | HEAD | 19/0 |
| `validate_f35sbxb2_cierre_formal.py` | R2-A (dentro de HIS y R2A) | Anclado sobre `ad193f9` y HEAD | 14/0 y 8/6 (clase A) |
| `validate_f35sbxb2.py` | Evaluación material (dentro de MAT) | HEAD | 112/7 (clase A) |
| `validate_f35sbxb2_cierre_gobierno.py` | Cierre de gobierno (dentro del gate de R2-A) | Anclado sobre `363273e` y HEAD | 13/0 y 7/6 |
| `validate_f35sbxb2_sucesor_freeze.py`, `validate_f35sbxb2_sucesor.py`, `validate_f35sbxb2_freeze.py` | Capas anteriores de B2 | Anclados sobre `8969424`, `9d6fb15` y `9961d2d` | 12/0, 7/0 y 10/0 |
| `validate_f35sbxb2.py` | Gate histórico de B2 | Anclado sobre `2472fd6` | 119/0 |
| `validate_f35sbxb.py`, `validate_f35sbxb_freeze.py` | Gates históricos de B1 y B1-FREEZE | Anclados sobre `8e94a60` y `3d9b783` | 159/0 y 14/0 |
| `validate_f35sbx.py` | Validador de F35-SBX-A | Anclado sobre su commit E, `61f94e2` | 846/0 |

Esta tabla supera la de §5.6 del registro del cierre formal, congelada en `ad193f9`.

### 6.8 Autoauditoría

Se intentó romper B3 por cada vía de la consigna, con el resultado medido:

| Intento | Qué lo rechaza | Evidencia |
|---|---|---|
| Omitir, reordenar o alterar un paso | CNF (nivel 1: acciones y estados del oráculo) y las pruebas del pipeline | CB16, CB17 y CB18 |
| Manipular el fixture | Paso 1 (SHA-256 del manifest de A), INT de la capa A y el gate de B2 | PT08, PT10 y CB15 |
| Manipular la procedencia o un hash | Nivel 1 recalculado desde `evidence.csv` y nivel 2 eslabón por eslabón | PT11, CB19 y CB20 |
| Alterar un conteo | CNF frente a las tablas y al oráculo; PUR solo frente a las tablas | CB21 |
| Cruzar tenants o escenarios | Pasos 1, 2 y 7, el almacén, PIP, CNF y PUR | PT09, PT10, CB22 y CB23 |
| No determinismo y doble ejecución divergente | DET (tres procesos) y FAL (dos por paso) | PT02, PT03, PT18 y CB24 |
| Purga falsa con un comprobante coherente | La observación en el proceso de PT06 (TSB), y FRZ y ALC sobre el código | CB25 |
| Cadena de auditoría alterada | Nivel 2 | PT05 y CB20 |
| Resultado parcial presentado como completo | FAL, y PIP exige código 0 y los tres runs | CB26 |
| Capacidad prohibida | Esquema cerrado del informe (PIP), DEP y SEM | PT17, CB27, CB28 y CB40 |
| Dejar un archivo en el temporal o en el repositorio (TSBB-08) | PUR: el temporal exclusivo y el árbol de trabajo, antes y después | Dos ataques fuera de la batería, sobre un pipeline alterado en un clon desechable: `rastro.sqlite` en su temporal y `rastro.db` en la carpeta de B3, los dos rechazados por PUR |
| Cambio de gobierno no autorizado | GOV y SEM, y R2A y MAT por sus gates congelados | CB04..CB11 y CB34..CB42 |

| # | Nivel | Hallazgo | Tratamiento |
|---|---|---|---|
| H1 | MEDIUM | TSBB-08 solo se comprobaba dentro del repositorio: un archivo escrito en el temporal del usuario no se habría detectado | Corregido: temporal exclusivo, nuevo y vacío, que PUR exige vacío al terminar |
| H2 | LOW | CNF no comprobaba el principal del run ni el contexto del tenant, y el nivel 2 no comprobaba los instantes | Corregido (§6.2) |
| H3 | LOW | Con una sola ejecución más, un informe dependiente del PID coincidía por azar con probabilidad 1/500 | Corregido: dos ejecuciones más (1/250 000) |
| H4 | LOW | Una purga falsificada con un comprobante coherente solo la ve la observación en el proceso. Causa: el gate ejecuta el pipeline en otro proceso y el comprobante lo informa el propio pipeline. Impacto: un pipeline alterado para forjar un comprobante coherente pasa PUR (CB25) | Aceptado como riesgo residual (R5), sin bloquear la auditoría: lo detectan PT06, dentro de TSB, y FRZ y ALC si el código cambia después del commit que completa la capa. Un pipeline y unas pruebas falseados en ese mismo commit son lo que revisa la auditoría independiente |
| H5 | MEDIUM | Ejecutada desde un clon compartido, como en una auditoría habitual, la batería hacía fallar HIS en todos los casos: el clon anclado de HIS sumaba un nivel de alternates a la cadena congelada y superaba el límite de Git | Corregido en RED → GREEN (§6.2): alternates aplanados en el clon de HIS y ENT con la profundidad admitida |

No quedó ningún hallazgo BLOCKER, HIGH ni MEDIUM abierto.

### 6.9 Riesgos residuales

| # | Nivel | Riesgo | Tratamiento |
|---|---|---|---|
| R1 | INFO | Hasta que la auditoría independiente apruebe B3 y el equipo autorice su integración, el registro de B3 en el gobierno de esta rama no vale: `develop` y `main` siguen diciendo «sin pipeline funcional ni ML» | Es el estado de todo candidato. El texto nuevo no menciona el estado de auditoría de B3, así que sigue siendo cierto después de integrarse |
| R2 | INFO | El ancla de nivel B solo autentica la capa si se registra fuera: una capa reconstruida con los mismos bytes en otra historia informa otra ancla (CB08) | La auditoría anota el commit que informa FRZ |
| R3 | LOW | R2A y MAT solo ven las tres primeras violaciones de cada regla de los gates que ejecutan | Exigen recuentos exactos y predichos y comparan una a una las violaciones visibles. El alcance exacto lo comprueba ALC y la integridad, INT |
| R4 | INFO | La predicción de R2A usa la lógica del propio gate de R2-A: un error común a esa lógica y a su salida no lo revela la comparación | Por eso la clasificación de clase A es propia, y lo enmascarado lo reponen ALC, INT, GOV, SEM y DEP |
| R5 | LOW | El gate no puede observar la memoria del proceso del pipeline: una purga falsificada con un comprobante coherente pasa PUR (CB25) | La detectan PT06, dentro de TSB, y FRZ y ALC sobre el código congelado |
| R6 | INFO | Una ejecución del gate tardó 203 segundos sin otra carga, y unos 25 minutos por caso con doce en paralelo: el gate de R2-A, anclado y sobre HEAD, ejecuta a su vez toda la cadena congelada | Es el coste de conservar completa la evaluación vigente |
| R7 | INFO | El gate exige no más de tres niveles de clones compartidos bajo el repositorio, y la batería, que añade dos, no más de uno: más abajo, la cadena congelada del gate de R2-A sobre HEAD superaría el límite de alternates de Git, y B3 no puede aplanar los clones de los gates congelados | ENT lo informa con su causa. Se ejecutan desde el repositorio o desde un clon compartido de él |
| R8 | INFO | Cualquier cambio fuera de las rutas de B3 hace fallar ALC, MAT y R2A, incluido uno legítimo de un incremento futuro, y cualquier cambio del gobierno hace fallar GOV | Es la clase A de ese incremento, que aportará su propio gate sucesor (DH-B13) |
| R9 | INFO | Los merges en `main` no son ancestros de esta rama, así que el gate no los verifica | Se registraron con Git y con el CI (§1.2), y CB02 prueba la integración `--no-ff` sobre `8a00505` |

### 6.10 Próximo paso

Auditoría independiente de B3, que anota como ancla el commit que informa la línea INFO de FRZ. Hasta entonces:

- B3 no se aprueba ni se integra;
- F35-SBX-B sigue INICIADA y F35-SBX, HABILITADA, y ninguna de las dos se declara cerrada;
- no hay push, merge, tag ni release de este incremento.
