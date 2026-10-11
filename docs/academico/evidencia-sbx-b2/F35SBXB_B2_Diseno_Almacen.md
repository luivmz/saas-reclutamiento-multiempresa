# F35-SBX-B — B2: diseño del almacén efímero sintético

> Incremento B2 de F35-SBX-B, versión 1 de diseño (11/10/2026). Estado: **B2 = DISEÑADA / PENDIENTE DE AUDITORÍA DE DISEÑO**. Este documento es un contrato de diseño: no hay almacén, runtime SQLite, pruebas ejecutables ni gate implementados. Rama `feature/f35-sbx-b2-ephemeral-store`, creada desde `develop` `72e86c5838984ea873d6dd56c179d94217b27317`.

## 1. Qué es B2 y de dónde sale

B2 define el almacén donde las fases posteriores de F35-SBX-B ejecutarán el pipeline sintético. Es un módulo Python interno y experimental que guarda los objetos de un run en una base SQLite `:memory:` propia de cada organización sintética, y la destruye cerrando la conexión.

B2 no inventa un dominio: deriva todo de contratos ya auditados.

| Fuente | Qué fija para B2 |
|---|---|
| [Contrato de A](../evidencia-sbx/contrato/f35sbx_contract.json), congelado en E | Las entidades del run, sus campos, enumeraciones, patrones, el hash de contenido `f35sbx-content-sha256-v1` y las cadenas con génesis de 64 ceros. La [arquitectura de A](../evidencia-sbx/F35SBX_Arquitectura.md#2-componentes) ya asigna a B la tabla en memoria, la solo inserción con triggers y los estados reservados `fallido` y `purgado` |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md) | DH-B05 (conformidad en dos niveles con el oráculo de A), DH-B06 (purga verificable), DH-B07 (solo `:memory:`), DH-B08 (una conexión y un run por organización), DH-B10 (fallo cerrado a `fallido`), §5.2 (identificadores propios de B), §5.4 (configuración de SQLite) y §5.5 (amenazas TSBB-01..TSBB-13) |
| [F33 §6](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#6-estados) y [F34](../datos-sinteticos/F34_Modelo_de_Datos.md) | `analysis_run` como registro principal inmutable y `analysis_run_events` de solo inserción, con el estado vigente en el último evento |
| [Alcance autorizado de G0-SBX](../g0-sandbox/F34E_Alcance_Autorizado.md) y [prohibiciones](../g0-sandbox/F34E_Prohibiciones.md) | Almacenamiento experimental aislado, fuera de la base productiva y sin acceso desde el runtime; ningún resultado alimenta el runtime ni el servicio de RF-29 |
| [B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md) | B1 histórica y congelada; B2 aporta su propio gate sucesor |

## 2. Arquitectura

```
contexto de tenant (ORG-S1..S3, validado)
        |
        v
open_tenant_store(tenant) ──> TenantRunStore      (un objeto por tenant y run; sin registro global)
        |                        |
        |                        +-- conexión sqlite3 privada a ':memory:'  (nunca expuesta)
        |                        +-- esquema fijo verificado + autorizador por lista blanca
        |                        +-- catálogo cerrado de sentencias SQL con parámetros
        v
create_run / append_event / append_evidence / append_audit / read_* / snapshot
        |
        v
purge(store) ──> cierre de la conexión + comprobante de purga (fuera del almacén)
```

- **Ubicación propuesta:** `docs/academico/tools/f35sbxb2/sbxb_store.py`. El nombre `sbxb_store.py` viene de B0 §6. La carpeta es nueva porque `tools/f35sbxb/` está congelada con contenido exacto en B1-FREEZE (DH-B2-01, §15).
- **Dependencias:** solo la biblioteca estándar: `sqlite3`, `hashlib`, `json`, `re` y `unicodedata`. `sqlite3` solo se importa en ese módulo, como exige B0 §6.
- **Frontera:** el módulo no abre archivos, no usa red, no lee variables de entorno, no importa nada del runtime y no se registra en ningún punto del proyecto.

## 3. Aislamiento por tenant

**Decisión: una conexión SQLite `:memory:` independiente por tenant y por run** (DH-B08). El filtro por `organization_id` en una base compartida no es la barrera.

| Criterio | Base compartida filtrada por organización | Una conexión `:memory:` por tenant |
|---|---|---|
| Fuga entre tenants | Un `WHERE` olvidado o una FK cruzada basta | Imposible por la API: cada base es privada de su conexión |
| Purga de un tenant | Exigiría `DELETE`, contrario a DH-B06 | Cerrar su conexión destruye solo su base |
| Fallo de un tenant | Puede dejar la base común en estado incierto | No afecta a los demás |
| Coste | Un esquema | Un esquema pequeño por tenant |
| Consultas entre tenants | Posibles (riesgo) | No existen: el informe agrega por tenant en Python |

Selección del almacén:

1. **Contexto del tenant.** El llamador construye el contexto con el `SyntheticTenantContext` de A: organización `ORG-S1..S3`, `tenant_kind` y `simulation_actor` del mismo tenant. Se valida antes de crear nada.
2. **Almacén.** `open_tenant_store(tenant)` devuelve un objeto ligado a ese tenant. No existe un registro global indexado por organización ni una función que entregue otro almacén. El tenant de una fila nunca elige conexión, porque la conexión ya está fijada en el objeto.
3. **Validación de la operación.** Cada escritura exige que el tenant de la fila coincida con el del almacén. Además, un trigger estático compara la organización de cada fila con la fila única `tenant_context` y rechaza la diferencia en el propio motor.
4. **SQL.** Solo sentencias del catálogo cerrado, con los valores como parámetros.
5. **Resultado.** Copias en `dict` o `tuple`, nunca cursores ni filas ligadas a la conexión.

## 4. Endurecimiento de SQLite

| Control | Cómo | Origen |
|---|---|---|
| Solo memoria | `sqlite3.connect(':memory:', isolation_level=None)` con la constante literal, sin `uri=True` ni cadenas del llamador | DH-B07 |
| Sin archivo | Antes de cerrar, `PRAGMA database_list` debe mostrar solo `main` (y `temp`) sin ruta | B0 §5.3 |
| FK | `PRAGMA foreign_keys = ON`, verificado leyéndolo | B0 §5.4 |
| Temporales | `PRAGMA temp_store = MEMORY`, verificado | B0 §5.4 |
| Esquema no confiable | `PRAGMA trusted_schema = OFF`, verificado | Nuevo |
| REPLACE bajo control | `PRAGMA recursive_triggers = ON`, verificado. Sin él, `INSERT OR REPLACE` sustituye filas protegidas sin disparar el trigger de borrado | Nuevo (§16) |
| Sin ATTACH | `setlimit(SQLITE_LIMIT_ATTACHED, 0)` y el autorizador niegan `ATTACH` y `DETACH` | B0 §5.4 |
| Sin extensiones | Nunca se llama a `enable_load_extension`; el autorizador niega la función `load_extension` | Nuevo |
| Sin caché compartida | Ninguna URI ni `cache=shared`; en Python 3.12 `enable_shared_cache` ya no existe | Nuevo |
| SQL fijo | Catálogo cerrado de sentencias; `execute` solo recibe una entrada del catálogo y una tupla de parámetros. Sin concatenación, f-strings, `%` ni `format` en SQL | B0 §5.4 |
| Sin `executescript` externo | Solo para el DDL fijo del catálogo, antes de instalar el autorizador | Nuevo |
| Sentencias prohibidas | Ni `OR REPLACE`, `REPLACE INTO`, `OR IGNORE`, `ON CONFLICT`, `UPDATE` ni `DELETE` en el catálogo de escritura | Nuevo |
| Autorizador por lista blanca | Tras crear y verificar el esquema: solo `INSERT`, `SELECT`, `READ`, `TRANSACTION`, el `PRAGMA database_list` y las funciones `raise`, `glob` y `length`. Todo lo demás se niega en el motor (`UPDATE`, `DELETE`, DDL, `PRAGMA` de escritura, `ATTACH`, funciones de fecha, aleatorias o de extensión) | Nuevo |
| Triggers fijos | Definidos solo en el DDL del catálogo; el autorizador impide crearlos, borrarlos o desactivarlos después | B0 §5.4 |
| Sin exportación | Ni `backup`, `serialize`, `deserialize` ni `iterdump` | B0 §5.4 |
| Versión | SQLite 3.37 o posterior, por las tablas `STRICT`; si no, falla cerrado | Nuevo |

SQLite `:memory:` no es una frontera de seguridad frente a SQL arbitrario (B0 §5.4). La protección es el catálogo fijo; el autorizador, los triggers y los límites son defensa en profundidad.

## 5. Esquema mínimo

Ocho tablas `STRICT`. Son las entidades del contrato de A que viven en un run; no se reproduce el dominio del SaaS (vacantes, postulaciones, sesiones ni valoraciones). Los nombres derivan de las entidades de A, no de las tablas productivas, para no sugerir una equivalencia con la base del proyecto.

| Tabla | Entidad de A | Equivalente de diseño (F33/F34) | Filas por almacén |
|---|---|---|---|
| `tenant_context` | `SyntheticTenantContext` | Organización sintética | Exactamente 1 |
| `pipeline_run` | `SyntheticPipelineRun` | `analysis_run`: registro principal inmutable | 0 o 1 |
| `pipeline_event` | `SyntheticPipelineEvent` | `analysis_run_events`: solo inserción | Hasta 7 |
| `evidence_source` | `SyntheticEvidenceSource` | Fila de origen F34 | Hasta 100 |
| `evidence_record` | `SyntheticEvidenceRecord` | `evidence`, sin token de persona | Hasta 100 |
| `evidence_provenance` | `SyntheticEvidenceProvenance` | Procedencia (F33 §7) | Hasta 100 |
| `simulated_review` | `SyntheticHumanReview` | Revisión humana simulada (DH-05 de A) | Hasta 100 |
| `audit_entry` | `SyntheticAuditEntry` | Auditoría experimental, separada de `audit_logs` | Hasta 8 |

Los máximos de eventos y de auditoría salen de A: siete estados en el camino del run (`purgado` queda fuera de la base) y ocho acciones de auditoría. El tope de 100 evidencias por run es un límite de recursos que propone B2 (A usa dos por tenant).

Las columnas son exactamente los campos de cada entidad de A, con sus constantes y enumeraciones. Solo cambian los valores propios de B:

| Campo | En A | En B2 |
|---|---|---|
| Prefijos de identificador | `SBXR`, `SBXV`, `SBXS`, `SBXE`, `SBXP`, `SBXH`, `SBXA` | `SBBR`, `SBBV`, `SBBS`, `SBBE`, `SBBP`, `SBBH`, `SBBA` (B0 §5.2) |
| `run_kind` | `oraculo_sbx_a` | `ejecucion_sbx_b` |
| `pipeline_version` | `f35sbx-design-0` | `f35sbxb-0` |
| `contract_version` | `f35sbx-contract-1.0.0` | `f35sbxb-contract-1.0.0` |
| Estados de evento | Siete del oráculo, más `fallido` y `purgado` reservados | Los siete más `fallido`. `purgado` vive en el comprobante externo (§9), porque la base ya no existe |

Restricciones en el motor, todas estáticas y del DDL fijo:

- **Tipos y claves.** Tipos `TEXT` e `INTEGER`, `NOT NULL` en todo, clave primaria en cada identificador y FK hacia `pipeline_run` y entre evidencia, fuente, revisión y procedencia.
- **Valores.** `CHECK` de constantes y enumeraciones, `GLOB` de identificadores e instantes, y longitud máxima de `text_synthetic`.
- **Solo inserción.** Triggers `BEFORE UPDATE` y `BEFORE DELETE` con `RAISE(ABORT)` en las ocho tablas.
- **Tenant.** Trigger `BEFORE INSERT` que rechaza una `synthetic_organization_id` distinta de la de `tenant_context`.
- **Run único.** Trigger que rechaza una segunda fila en `pipeline_run`.
- **Eventos.** Triggers que exigen `seq` contiguo desde 1, que el primer evento sea `pendiente`, que `prev_event_hash` sea el `event_hash` anterior (o 64 ceros) y ningún evento después de `completado` o `fallido`.
- **Cadenas.** Las de provenance y auditoría, enlazadas igual.

No hay columnas de puntaje, ranking, recomendación, selección, tokens de persona, texto de CV, media ni variables de RF-29. El esquema es cerrado: el gate lo compara con la lista independiente del contrato (doble llave) y con `PRAGMA table_info` en ejecución.

## 6. Ciclo de vida

Estados del almacén, alineados con los de A y F33. Los del run son eventos; los del almacén, del objeto:

| Estado del almacén | Se entra con | Run |
|---|---|---|
| `abierto` | `open_tenant_store`: conexión, PRAGMA verificados, esquema verificado, autorizador y fila `tenant_context` | Sin run |
| `activo` | `create_run`: principal y evento `pendiente` en una transacción | Último evento no terminal |
| `finalizado` | Evento `completado` o `fallido` | Terminal |
| `purgado` | `purge` | Destruido; comprobante externo |

| Operación | `abierto` | `activo` | `finalizado` (`completado`) | `finalizado` (`fallido`) | `purgado` |
|---|---|---|---|---|---|
| `create_run` | Sí | No | No | No | No |
| `append_event` | No | Sí, con transición válida | No | No | No |
| `append_evidence`, `append_audit` | No | Sí | No | No | No |
| `read_run`, `list_events`, `current_state` | No | Sí | Sí | Sí | No |
| `list_evidence`, `list_audit`, `snapshot` | No | Sí | Sí | No: sin resultado parcial (DH-B10) | No |
| `purge` | Sí | Sí, tras registrar `fallido` con `E-ABORTADO` | Sí | Sí | No |

Cualquier operación fuera de la tabla falla con `E-CICLO`; después de `purge`, con `E-PURGADO`. Las transiciones del run siguen el camino de A (`pendiente` → `validando` → `registrado` → `transformado` → `en_revision` → `revisado` → `completado`), y desde cualquier estado no terminal se puede pasar a `fallido`.

## 7. `pipeline_run`: principal inmutable

- Una sola fila por almacén. La crea `create_run` con la semilla y el `clock_start` del escenario, y el almacén completa las constantes.
- La identidad, el tenant, la versión del dataset de origen, las versiones de contrato y pipeline, el algoritmo de hash, la semilla y `clock_start` no cambian. No existe ninguna sentencia `UPDATE`; el trigger y el autorizador la rechazarían.
- El estado vigente no es una columna del principal: es el último evento (F33 §6).

## 8. Eventos de solo inserción

- **Valores que asigna el almacén.** `append_event` recibe solo `state`, `at` y `error_code`. El almacén asigna `seq` (el siguiente), `event_id` (`SBBV-<org>-0001-<seq:02>`), `prev_event_hash` y `event_hash`, este último con el algoritmo de A: SHA-256 del JSON canónico del objeto sin su propio campo de hash.
- **Orden.** Por `seq` (`ORDER BY seq`); nunca por `rowid` ni por orden de inserción implícito.
- **Tiempo.** `at` es un instante lógico del escenario (`YYYY-MM-DDTHH:MM:SS`, sin zona), no anterior a `clock_start` ni al evento previo. El almacén nunca lee el reloj del sistema.
- **Sin `UPDATE` ni `DELETE`.** Un reintento añade eventos o requiere un almacén nuevo; no reescribe.
- **Auditoría.** La entrada `audit_entry` sigue las mismas reglas, con sus acciones del enum de A.

## 9. Purga

La purga es la frontera de destrucción lógica del almacén (DH-B06, B0 §5.3):

1. **Run activo.** Si el run sigue activo, se registra `fallido` con `E-ABORTADO`.
2. **Comprobante.** Se lee lo necesario para el comprobante: conteos por tabla, último `event_hash` y `PRAGMA database_list`, que debe mostrar bases sin archivo.
3. **Cierre.** Se cierra la conexión; el almacén no conserva cursores abiertos.
4. **Comprobación.** Una consulta trivial sobre la conexión cerrada debe lanzar `sqlite3.ProgrammingError`; si no la lanza, la purga falla cerrada.
5. **Referencia.** El almacén descarta la conexión y pasa a `purgado`. Cualquier llamada posterior falla con `E-PURGADO`.
6. **Comprobante externo.** Se devuelve el estado `purgado` de A, encadenado al último evento:

| Campo del comprobante | Contenido |
|---|---|
| `pipeline_run_id`, `synthetic_organization_id` | Run y tenant del almacén |
| `final_state` | `completado` o `fallido` (o `sin_run` si se purgó en `abierto`) |
| `last_event_hash` | Enlace con la cadena de eventos destruida |
| `counts` | Filas por tabla en el momento del cierre |
| `file_backed` | `false`, según `PRAGMA database_list` |
| `post_close_check` | `ProgrammingError` |
| `receipt_hash` | SHA-256 del JSON canónico del comprobante sin este campo |

La purga nunca es `DELETE FROM` sobre la misma conexión viva. No hay archivo que borrar. B2 no afirma borrado seguro de RAM, borrado criptográfico ni ninguna garantía física sobre la memoria: solo que la base deja de ser alcanzable por la API y por la conexión.

## 10. Determinismo

Dos ejecuciones del mismo escenario sintético deben dar el mismo resultado lógico, byte a byte en `snapshot()` y en el comprobante:

- **Identificadores.** Se derivan solo del tenant y de ordinales del run (B0 §5.2), con los prefijos `SBB*`:
  - el run es `SBBR-<org>-0001`, porque hay uno por almacén;
  - los eventos y la auditoría usan `seq`;
  - la evidencia, su fuente, su revisión y su procedencia comparten el ordinal de la evidencia, de 6 dígitos.
- **Valores prohibidos.** Nunca `rowid`, `uuid`, `random` ni `secrets`.
- **Tiempo.** Solo instantes lógicos del escenario. Ni `datetime.now`, ni `time.time`, ni `CURRENT_TIMESTAMP`. El autorizador niega las funciones de fecha y aleatorias.
- **Orden.** Todas las lecturas con `ORDER BY` explícito por la clave del ordinal.
- **Serialización.** JSON canónico (claves ordenadas, sin espacios, UTF-8 sin escapar), igual que A. Sin rutas, locale ni zona horaria.
- **Texto.** `text_synthetic` debe estar ya normalizado en NFC; la transformación T1 es del pipeline. El almacén solo lo comprueba.

El double-run completo pertenece a una fase posterior. B2 solo garantiza que el almacén no lo impide.

## 11. Restricciones de datos

| Admitido | Rechazado |
|---|---|
| Objetos de las ocho entidades, con exactamente sus campos | Cualquier campo adicional o ausente (`E-CONTRATO`) |
| `text_synthetic` con `[SINTÉTICO] `, sin `<`, `>` ni caracteres de control, de 400 caracteres como máximo y en NFC | Texto sin el marcador, con marcado, controles o fuera de NFC (`E-PROHIBIDO`) |
| `evidence_kind` en `formulario`, `nota_entrevista` o `prueba` | `cv`, `documento` o cualquier otro (alcance C) |
| Origen fijo: el `evidence.csv` de F34, con su SHA-256 | Otra ruta, incluidos los adjuntos de `g0-evidence` |
| Los seis marcadores synthetic-only de A en cada evidencia | Uno ausente (`E-PROHIBIDO`) |

- **PII.** El texto pasa los detectores de A §5: correos, URL, números de 8 u 11 dígitos, teléfonos, data URI y bloques base64. Una coincidencia falla.
- **Datos sensibles y capacidades.** El esquema no tiene dónde guardar personas reales, CV, documentos, audio, vídeo, biometría, rostro, voz, ni inferencias de emoción, personalidad, honestidad, inteligencia, estrés o salud. Tampoco datos sensibles (religión, orientación sexual, raza o etnia, afiliación política), puntajes, rankings, recomendaciones, selecciones, OCR, *parsing*, embeddings ni búsqueda semántica.
- **Revisión simulada.** Solo admite `integridad_y_procedencia` con `conforme` u `observado` (DH-05 de A): nunca juzga a la persona sintética.
- **RF-23** no se toca: ninguna tabla tiene decisión, selección ni contratación.

## 12. RF-29

RF-29 sigue experimental, solo sobre el proceso y no productivo. B2 no almacena nada de RF-29:

- ni snapshots de proceso, ni variables del contrato RF-29;
- ni etiquetas de demora, ni salidas de modelo, ni puntajes de riesgo.

Por eso no hay selección de candidatos, PII ni identificadores de candidato, ni sustitución del ranking, y el puntaje no se persiste. Ningún dato del almacén alimenta `ml-service/` ni el runtime (F34E). Guardar evidencia de RF-29 en el sandbox requeriría una autorización nueva.

## 13. API interna

Módulo `sbxb_store.py`, API Python interna y experimental. No es una API HTTP.

| Función | Entrada | Salida | Invariantes y errores |
|---|---|---|---|
| `open_tenant_store(tenant)` | `dict` con los 4 campos de `SyntheticTenantContext` | `TenantRunStore` en `abierto` | Tenant `ORG-S1..S3` coherente; PRAGMA, esquema y autorizador verificados. `E-TENANT`, `E-CONTRATO`, `E-SQLITE` |
| `create_run(store, seed, clock_start)` | Entero de 0 a 2147483647; instante lógico | `dict` del principal, con el evento `pendiente` creado | Una vez por almacén. `E-CICLO`, `E-CONTRATO` |
| `append_event(store, state, at, error_code='')` | Estado del enum, instante lógico y código `E-[A-Z]{2,12}` solo con `fallido` | `dict` del evento con `seq`, id y hashes asignados | Transición válida, instante monótono. `E-CICLO`, `E-CONTRATO` |
| `append_evidence(store, evidence)` | Contenido de una evidencia: `origin_file_sha256`, `origin_record_id`, `criterion_ref`, `evidence_kind`, `text_synthetic`, `hash_before`, `validation_status`, `review_status` y sus instantes | `dict` con fuente, evidencia, revisión simulada y procedencia, con ids, `content_hash` y cadena asignados | Inserta las cuatro filas en una transacción, en orden FK. Recalcula `content_hash` con `f35sbx-content-sha256-v1`. `E-PROHIBIDO`, `E-CONTRATO`, `E-HASH`, `E-CICLO` |
| `append_audit(store, action, at)` | Acción del enum de A e instante lógico | `dict` de la entrada con id y cadena | `E-CICLO`, `E-CONTRATO` |
| `read_run(store)` | — | `dict` del principal | `E-CICLO`, `E-PURGADO` |
| `list_events(store)`, `list_audit(store)`, `list_evidence(store)` | — | `tuple` de `dict`, en orden por `seq` u ordinal | Según la tabla de §6 |
| `current_state(store)` | — | Estado del último evento | — |
| `snapshot(store)` | — | `bytes` del JSON canónico de las ocho tablas | Solo `activo` o `completado` |
| `purge(store)` | — | `dict` del comprobante (§9) | Una vez. `E-PURGADO` si se repite |

- **Errores.** Una sola excepción, `SbxbStoreError(code, message)`. Los códigos cumplen el patrón de A `^E-[A-Z]{2,12}$`: `E-TENANT`, `E-CICLO`, `E-CONTRATO`, `E-PROHIBIDO`, `E-HASH`, `E-SQLITE`, `E-ABORTADO` y `E-PURGADO`.
- **Fallo cerrado.** Cualquier error en una escritura deja el run en `fallido` con su código (DH-B10). Si la base no admite ni ese evento, el almacén pasa a `fallido` en el objeto y solo admite `purge`. Un `sqlite3.Error` nunca se ignora: se convierte en `E-SQLITE`.
- **Encapsulamiento.** El objeto no expone la conexión, los cursores ni el catálogo. Los nombres internos no son API y el gate prohíbe usarlos fuera del módulo.

## 14. Modelo de fallos

| Caso | Detección | Resultado |
|---|---|---|
| Tenant equivocado o ajeno en una fila | API y trigger `tenant_context` | `E-TENANT`; run `fallido` |
| Operación sin tenant o sin almacén | No existe API sin almacén ligado a un tenant | No hay escritura posible |
| Conexión cerrada o almacén purgado | Estado `purgado`; `ProgrammingError` | `E-PURGADO` |
| FK inválida | `foreign_keys = ON` | `E-SQLITE`; run `fallido` |
| Escritura después de `completado`, `fallido` o la purga | Ciclo de vida y trigger de terminal | `E-CICLO` o `E-PURGADO` |
| Carga útil con campos de más, de menos o patrones inválidos | Validación cerrada | `E-CONTRATO`; run `fallido` |
| Dato prohibido (sin marcador, PII, tipo `cv`, marcado) | Validación synthetic-only | `E-PROHIBIDO`; run `fallido` |
| Hash de contenido distinto del recalculado | Recálculo | `E-HASH`; run `fallido` |
| Modificar o borrar una fila | Autorizador y triggers; `recursive_triggers` para `REPLACE` | `E-SQLITE`; run `fallido` |
| `ATTACH`, extensión, PRAGMA o DDL después del esquema | Límite de bases adjuntas y autorizador | `E-SQLITE`; run `fallido` |
| Cualquier `sqlite3.Error` | Envoltura obligatoria | `E-SQLITE`; run `fallido` |
| Persistencia en disco | `PRAGMA database_list` y el gate (sin archivos antes ni después) | Purga fallida; gate FAIL |

## 15. Decisiones propuestas

Son propuestas que el equipo debe aprobar en la auditoría de diseño. Ninguna está aprobada todavía.

| ID | Propuesta |
|---|---|
| DH-B2-01 | Rutas nuevas `docs/academico/evidencia-sbx-b2/` y `docs/academico/tools/f35sbxb2/`. DH-B03 no cambia para B1; las carpetas de B1 siguen congeladas |
| DH-B2-02 | Una conexión `:memory:` por tenant y por run, como concreción de DH-B08 |
| DH-B2-03 | Esquema de ocho tablas derivado de A, con nombres de entidad de A y la equivalencia con `analysis_run`/`analysis_run_events` documentada |
| DH-B2-04 | Controles adicionales sobre B0 §5.4: `recursive_triggers`, `trusted_schema = OFF`, límite de bases adjuntas en 0, autorizador por lista blanca y prohibición de `OR REPLACE`, `OR IGNORE` y `ON CONFLICT` |
| DH-B2-05 | `purgado` vive en el comprobante externo, encadenado al último evento |
| DH-B2-06 | Identificadores `SBB*` derivados del tenant y de ordinales, con el run fijo en `0001` porque hay uno por almacén |
| DH-B2-07 | El registro de B1 cerrada y de B2 en `CLAUDE.md` y `docs/PROGRESS.md` se hace en el incremento que introduce el gate de B2, con su regla de gobierno, no en este diseño |

## 16. Observaciones de la inspección

Comprobaciones exploratorias hechas el 11/10/2026 con Python 3.12.5 y SQLite 3.45.3, en una carpeta temporal fuera del repositorio. No son pruebas del almacén: justifican los controles de §4.

| Observación | Consecuencia en el diseño |
|---|---|
| `INSERT OR REPLACE` y `REPLACE INTO` sustituyeron una fila protegida por triggers `BEFORE UPDATE` y `BEFORE DELETE`. Con `recursive_triggers = ON`, el trigger la rechazó | `recursive_triggers = ON` verificado y `REPLACE` fuera del catálogo |
| `INSERT OR IGNORE` descartó la fila en silencio | Prohibido: rompe el fallo cerrado |
| `ON CONFLICT ... DO UPDATE` sí disparó el trigger de modificación | Fuera del catálogo igualmente |
| Con `setlimit(SQLITE_LIMIT_ATTACHED, 0)`, `ATTACH` falló | Límite obligatorio |
| El autorizador por lista blanca negó `UPDATE`, `DELETE`, `PRAGMA` de escritura, `DROP TRIGGER`, `CREATE TABLE`, `ATTACH`, `load_extension` y `sqlite_version()`, y permitió `INSERT`, `SELECT` y las transacciones | Autorizador tras verificar el esquema |
| Tras `close()`, `execute` lanzó `ProgrammingError` | Base de la comprobación de purga |
| Ninguna operación creó archivos en la carpeta de trabajo | Base de P08 |
