# F35-SBX-B — B2: diseño del almacén efímero sintético

> Incremento B2 de F35-SBX-B: versión 2.1 del diseño (11/10/2026), implementada y corregida tras la auditoría de la implementación el 12/10/2026. Estado: **B2 = IMPLEMENTADA / CORREGIDA / PENDIENTE DE REAUDITORÍA FOCAL**.
>
> - La versión 1 (`ae25e8c60c538ce2336fadd98489de8eee9e0983`) recibió el veredicto «B2-DESIGN APROBADO CON CORRECCIONES PREVIAS», sin hallazgos BLOCKER ni HIGH.
> - Esta versión resuelve sus cinco MEDIUM (B2-M01..B2-M05, §0) y fija las decisiones Q1–Q9 ([contrato, §4](F35SBXB_B2_Contrato_Verificacion.md#4-decisiones-q1q9)).
> - La versión 2.1 completa M05 y Q1 tras la reauditoría de `eaac212`: la transición de gobierno es única y monotónica. Su reauditoría final focal dio el veredicto «B2-DESIGN APROBADO PARA IMPLEMENTACIÓN».
>
> La implementación sigue este diseño sin cambios: el almacén es [`sbxb_store.py`](../tools/f35sbxb2/sbxb_store.py) y el gate sucesor, [`validate_f35sbxb2.py`](../tools/f35sbxb2/validate_f35sbxb2.py). Su evidencia y sus observaciones están en el [contrato, §5](F35SBXB_B2_Contrato_Verificacion.md#5-implementación-12102026). La auditoría de la implementación encontró tres hallazgos (H01, M01 y M02); su corrección precisa tres puntos sin cambiar el diseño: la propiedad del hilo (§6.1), el bloqueo previo y el comprobante falible (§6.2 y §9) y el código `E-HILO` (§13). Está en el [contrato, §6](F35SBXB_B2_Contrato_Verificacion.md#6-corrección-post-auditoría-de-la-implementación). El código es de desarrollo y NO AUDITADO (Q6). Rama `feature/f35-sbx-b2-ephemeral-store`, creada desde `develop` `72e86c5838984ea873d6dd56c179d94217b27317`.

## 0. Correcciones de la versión 2

| Hallazgo | Corrección | Dónde |
|---|---|---|
| B2-M01. `INSERT OR IGNORE` y `ON CONFLICT DO NOTHING` no fallan, y el autorizador no las distingue | La frontera primaria es la API cerrada con el catálogo fijo. Triggers, autorizador y la postcondición de una fila son defensa adicional | §4, §16 |
| B2-M02. `fallido` no siempre se puede persistir | Tres planos separados: estado persistido, estado del objeto y estado de la conexión. Cierre excepcional con diagnóstico que distingue el evento confirmado del no disponible | §6, §9 |
| B2-M03. Identificadores fijos que colisionan entre escenarios | Espacio de nombres `<org>-<semilla>`, alineado con B0 §5.2 | §10 |
| B2-M04. Afirmación de que no hay dónde guardar datos sensibles | Garantía acotada: antes de persistir, el contenido debe corresponder a su fila F34 autorizada, transformada solo por T1 | §11 |
| B2-M05. Frontera histórica de B1 reducida al cierre | Dos conjuntos con sus anclas, el auditado desde `8e94a60` y el del cierre desde `3d9b783`. Una única transición monotónica de gobierno, de `HISTORICAL_B1_BLOB` a `B2_GOVERNANCE_BLOB`, sin vuelta atrás en sus descendientes (versión 2.1) | [Contrato, §2.3](F35SBXB_B2_Contrato_Verificacion.md#23-b1f-b1-sigue-íntegra) |

## 1. Qué es B2 y de dónde sale

B2 define el almacén donde las fases posteriores de F35-SBX-B ejecutarán el pipeline sintético. Es un módulo Python interno y experimental que guarda los objetos de un run en una base SQLite `:memory:` propia de cada organización sintética y de cada escenario. La base se destruye cerrando la conexión.

B2 no inventa un dominio: deriva todo de contratos ya auditados.

| Fuente | Qué fija para B2 |
|---|---|
| [Contrato de A](../evidencia-sbx/contrato/f35sbx_contract.json), congelado en E | Entidades del run, campos, enumeraciones, patrones, el hash de contenido `f35sbx-content-sha256-v1` y las cadenas con génesis de 64 ceros. La [arquitectura de A](../evidencia-sbx/F35SBX_Arquitectura.md#2-componentes) asigna a B la tabla en memoria, la solo inserción con triggers y los estados reservados `fallido` y `purgado` |
| [`validate_f35sbx.py`](../tools/f35sbx/validate_f35sbx.py), congelado en E | La definición exacta de T1 (`normalize_text`), del JSON canónico (`canon`), del hash de contenido (`content_hash`) y de las cadenas (`chain_hash`) |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md) | DH-B05 (conformidad en dos niveles con el oráculo de A), DH-B06 (purga verificable), DH-B07 (solo `:memory:`), DH-B08 (una conexión y un run por organización) y DH-B10 (fallo cerrado). También §5.2 (identificadores de B), §5.4 (configuración de SQLite) y §5.5 (TSBB-01..TSBB-13) |
| [F33 §6](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#6-estados) y [F34](../datos-sinteticos/F34_Modelo_de_Datos.md) | `analysis_run` como registro principal inmutable y `analysis_run_events` de solo inserción, con el estado vigente en el último evento. El dataset `f34-synth-1.1.0` y su manifiesto |
| [Alcance autorizado de G0-SBX](../g0-sandbox/F34E_Alcance_Autorizado.md) y [prohibiciones](../g0-sandbox/F34E_Prohibiciones.md) | Almacenamiento experimental aislado, fuera de la base productiva y sin acceso desde el runtime; ningún resultado alimenta el runtime ni el servicio de RF-29 |
| [B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md) | B1 histórica y congelada; B2 aporta su propio gate sucesor |

## 2. Arquitectura

```
contexto de tenant (ORG-S1..S3) + semilla del escenario
        |
        v
open_tenant_store(tenant) ──> TenantRunStore      (un objeto por tenant y escenario; sin registro global)
        |   1. origen autorizado: lee los 4 CSV fijos de F34 y verifica su SHA-256 contra el contrato
        |   2. conexión sqlite3 privada a ':memory:'                       (nunca expuesta)
        |   3. preflight: versiones, API y PRAGMA efectivos; esquema fijo verificado
        |   4. política de ejecución: autorizador por lista blanca
        v
create_run / append_event / append_evidence / append_audit / read_* / snapshot
        |   solo sentencias del catálogo cerrado del módulo, con parámetros
        v
purge(store) o cierre excepcional ──> conexión cerrada + comprobante o diagnóstico en memoria
```

- **Ubicación:** `docs/academico/tools/f35sbxb2/sbxb_store.py`. El nombre viene de B0 §6; la carpeta es una ruta exacta de B2 (Q2).
- **Dependencias:** solo la biblioteca estándar: `sqlite3`, `csv`, `hashlib`, `json`, `re`, `unicodedata`, `os.path` (solo para componer las rutas fijas) y `threading` (solo `get_ident`, para la propiedad del hilo que pide M01). `sqlite3` solo se importa en este módulo (B0 §6).
- **Frontera de E/S:**
  - Lee únicamente, en binario y sin escribir, cuatro archivos fijos del dataset F34: `evidence.csv`, `criteria.csv`, `vacancies.csv` y `applications.csv`, cada uno con el SHA-256 del contrato (§11).
  - No escribe archivos ni usa red, variables de entorno ni nada del runtime, y no se registra en ningún punto del proyecto.
- **Frontera de confianza (Q3):** B2 garantiza el aislamiento entre almacenes y el cumplimiento del contrato sobre lo que recibe. No autentica ni autoriza al llamador: quien tenga la referencia a un almacén puede operarlo. El llamador es código del pipeline de B, auditado; no es un usuario externo.

## 3. Aislamiento por tenant

**Decisión (Q3): 1 tenant, 1 run o escenario y 1 conexión a la constante literal `':memory:'`** (DH-B08). El filtro por `organization_id` en una base compartida no es la barrera.

| Criterio | Base compartida filtrada por organización | Una conexión `:memory:` por tenant y escenario |
|---|---|---|
| Fuga entre tenants | Un `WHERE` olvidado o una FK cruzada basta | Imposible por la API: cada base es privada de su conexión |
| Purga de un tenant | Exigiría `DELETE`, contrario a DH-B06 | Cerrar su conexión destruye solo su base |
| Fallo de un tenant | Puede dejar la base común en estado incierto | No afecta a los demás |
| Coste | Un esquema | Un esquema pequeño por almacén |
| Consultas entre tenants | Posibles (riesgo) | No existen: el informe agrega por tenant en Python |

Selección del almacén:

1. **Contexto del tenant.** El llamador construye el contexto con el `SyntheticTenantContext` de A: organización `ORG-S1..S3`, `tenant_kind` y `simulation_actor` del mismo tenant. Se valida antes de crear nada.
2. **Almacén.** `open_tenant_store(tenant)` devuelve un objeto ligado a ese tenant. No existe un registro global indexado por organización ni una función que entregue otro almacén. Ningún campo de una fila elige conexión.
3. **Validación de la operación.** Cada escritura exige que el tenant de la fila coincida con el del almacén y con el de su fila F34 de origen (§11).
4. **SQL.** Solo sentencias del catálogo cerrado, con los valores como parámetros.
5. **Resultado.** Copias en `dict` o `tuple`, nunca cursores ni filas ligadas a la conexión.

`tenant_context` es una fila única e inmutable del almacén. Sirve como metadato y como defensa adicional: un trigger estático compara la organización de cada fila con ella.

## 4. Frontera SQL y endurecimiento de SQLite

### 4.1 Frontera primaria: API cerrada y catálogo fijo

La defensa principal no está en SQLite, sino en el módulo:

- **El llamador no aporta SQL.** Tampoco fragmentos SQL, nombres de tabla ni de columna, ni política de conflicto. No puede pedir `REPLACE`, `INSERT OR REPLACE`, `OR IGNORE` ni *upsert* (`DO UPDATE` o `DO NOTHING`).
- **El catálogo es del módulo.** Es un conjunto cerrado de sentencias constantes, propiedad del módulo. Las escrituras son siempre `INSERT` simple: ante un conflicto, SQLite lanza `IntegrityError` y el almacén falla cerrado (§6.2).
- **Lo prohibido no existe.** `REPLACE`, `INSERT OR REPLACE`, `OR IGNORE`, `ON CONFLICT ... DO UPDATE`, `ON CONFLICT ... DO NOTHING`, `UPDATE`, `DELETE`, `ATTACH`, `DETACH` y `PRAGMA` de escritura no forman parte del catálogo de ejecución, así que son inalcanzables desde la API.
- **Postcondición.** Cada `INSERT` del catálogo debe afectar exactamente una fila (`rowcount == 1`). Si no, el almacén falla cerrado. Es una comprobación de una línea, no un filtro de SQL.

### 4.2 Defensa adicional en el motor

No es la garantía principal. La inspección de §16 muestra sus límites: el autorizador observa acciones, no la sentencia completa, y ve un `INSERT OR IGNORE` o un `DO NOTHING` igual que un `INSERT` legítimo.

| Control | Cómo | Origen |
|---|---|---|
| Solo memoria | `sqlite3.connect(':memory:', isolation_level=None)` con la constante literal, sin `uri=True` ni cadenas del llamador | DH-B07 |
| Solo inserción | Triggers `BEFORE UPDATE` y `BEFORE DELETE` con `RAISE(ABORT)` en las ocho tablas, y `recursive_triggers = ON` para que el borrado implícito de `REPLACE` también los dispare | B0 §5.4; §16 |
| Sin `ATTACH` | `setlimit(SQLITE_LIMIT_ATTACHED, 0)` | B0 §5.4 |
| Autorizador por lista blanca | Se instala tras el preflight (§4.3). Admite `INSERT`, `SELECT`, `READ` y `TRANSACTION` sobre las tablas del esquema, el `PRAGMA database_list` de lectura y las funciones `raise`, `glob` y `length`. Niega `UPDATE`, `DELETE`, DDL, cualquier otro `PRAGMA`, `ATTACH`, `DETACH` y las funciones de fecha, aleatorias o de extensión | Defensa en profundidad |
| Sin extensiones | Nunca se llama a `enable_load_extension`; el autorizador niega `load_extension` | Nuevo |
| Sin caché compartida | Ninguna URI ni `cache=shared` | Nuevo |
| Sin exportación | Ni `backup`, `serialize`, `deserialize` ni `iterdump` | B0 §5.4 |
| `executescript` | Solo para el DDL constante del catálogo, durante el preflight | Nuevo |

### 4.3 Preflight y verificación del esquema (Q4)

Dentro de `open_tenant_store`, antes de instalar el autorizador de ejecución, hay una fase interna con un conjunto cerrado y enumerado de comprobaciones. No existe ninguna API de `PRAGMA` para el llamador, y fuera de esta fase el único `PRAGMA` disponible es la lectura de `database_list` que usan la purga y el cierre excepcional.

| Requisito | Comprobación | Si no se cumple |
|---|---|---|
| SQLite 3.37.0 o posterior (tablas `STRICT`) | `sqlite3.sqlite_version` realmente cargada, no la del sistema operativo | `E-PREFLIGHT` |
| API de Python necesarias | `Connection.setlimit`, `Connection.set_authorizer`, `sqlite3.SQLITE_LIMIT_ATTACHED` y las constantes del autorizador presentes; se comprueba la API, no se supone por la versión de Python (3.11 o posterior para `setlimit`) | `E-PREFLIGHT` |
| `PRAGMA foreign_keys = ON` | Releído: `1` | `E-PREFLIGHT` |
| `PRAGMA recursive_triggers = ON` | Releído: `1` | `E-PREFLIGHT` |
| `PRAGMA temp_store = MEMORY` | Releído: `2` | `E-PREFLIGHT` |
| `PRAGMA trusted_schema = OFF` | Releído: `0` | `E-PREFLIGHT` |
| `journal_mode` compatible con memoria | Releído: `memory` | `E-PREFLIGHT` |
| Base sin archivo | `PRAGMA database_list`: solo bases sin ruta | `E-PREFLIGHT` |
| Límite de bases adjuntas | `getlimit(SQLITE_LIMIT_ATTACHED) == 0` | `E-PREFLIGHT` |
| Esquema | DDL constante ejecutado y `PRAGMA table_info` de cada tabla del catálogo igual a la lista del contrato | `E-PREFLIGHT` |

No hay respaldo silencioso: si algo falta, el almacén no se abre y la conexión se cierra. Los resultados quedan en un informe de preflight de solo lectura en el objeto, que usan P02 y P28.

La ausencia de archivos observada (P08) se limita a lo observable: `PRAGMA database_list`, el repositorio y el directorio de trabajo. No demuestra la ausencia física universal de temporales del sistema operativo ni de memoria paginada a disco.

## 5. Esquema mínimo

Ocho tablas `STRICT`: las entidades del contrato de A que viven en un run. No se reproduce el dominio del SaaS (vacantes, postulaciones, sesiones ni valoraciones). Los nombres derivan de las entidades de A, no de las tablas productivas, para no sugerir una equivalencia con la base del proyecto.

| Tabla | Entidad de A | Equivalente de diseño (F33/F34) | Filas por almacén |
|---|---|---|---|
| `tenant_context` | `SyntheticTenantContext` | Organización sintética | Exactamente 1 |
| `pipeline_run` | `SyntheticPipelineRun` | `analysis_run`: registro principal inmutable | 0 o 1 |
| `pipeline_event` | `SyntheticPipelineEvent` | `analysis_run_events`: solo inserción | Hasta 7 |
| `evidence_source` | `SyntheticEvidenceSource` | Fila de origen F34 | Una por evidencia |
| `evidence_record` | `SyntheticEvidenceRecord` | `evidence`, sin token de persona | Una por fila F34 autorizada, como máximo |
| `evidence_provenance` | `SyntheticEvidenceProvenance` | Procedencia (F33 §7) | Una por evidencia |
| `simulated_review` | `SyntheticHumanReview` | Revisión humana simulada (DH-05 de A) | Una por evidencia |
| `audit_entry` | `SyntheticAuditEntry` | Auditoría experimental, separada de `audit_logs` | Hasta 8 |

Los límites salen de los contratos de entrada, no de un número propio (Q9):

- **Eventos:** como máximo 7, los estados del camino de A. `purgado` queda fuera de la base.
- **Auditoría:** como máximo 8, las acciones de A.
- **Evidencias:** cada fila F34 autorizada se usa como mucho una vez por run (`UNIQUE` sobre `origin_record_id`). Su número lo limita el origen autorizado del tenant.

Las columnas son exactamente los campos de cada entidad de A, con sus constantes y enumeraciones. Solo cambian los valores propios de B:

| Campo | En A | En B2 |
|---|---|---|
| Prefijos de identificador | `SBXR`, `SBXV`, `SBXS`, `SBXE`, `SBXP`, `SBXH`, `SBXA` | `SBBR`, `SBBV`, `SBBS`, `SBBE`, `SBBP`, `SBBH`, `SBBA` (B0 §5.2) |
| Forma del identificador | `<prefijo>-<org>-<ordinal>` | `<prefijo>-<org>-<semilla de 10 dígitos>[-<ordinal>]` (§10) |
| `run_kind` | `oraculo_sbx_a` | `ejecucion_sbx_b` |
| `pipeline_version` | `f35sbx-design-0` | `f35sbxb-0` |
| `contract_version` | `f35sbx-contract-1.0.0` | `f35sbxb-contract-1.0.0` |
| Estados de evento | Siete del oráculo, más `fallido` y `purgado` reservados | Los siete más `fallido`. `purgado` vive en el comprobante externo (§9), porque la base ya no existe |

Los estados de evento son los del contrato de A, que B implementa, no los de `analysis_run_events` de F34 (`en_proceso`, `expirado` o `invalidado`). La equivalencia con F33 y F34 es de invariantes (principal inmutable y eventos de solo inserción), no de valores.

Restricciones en el motor, todas estáticas y del DDL constante:

- **Tipos y claves.** Tipos `TEXT` e `INTEGER`, `NOT NULL` en todo, clave primaria en cada identificador, `UNIQUE` en `origin_record_id`, y FK hacia `pipeline_run` y entre evidencia, fuente, revisión y procedencia.
- **Valores.** `CHECK` de constantes y enumeraciones, `GLOB` de identificadores e instantes, y longitud máxima de `text_synthetic`.
- **Solo inserción y tenant.** Los triggers de §4.2, más el trigger de tenant contra `tenant_context` y el de un único `pipeline_run`.
- **Eventos.** Triggers que exigen `seq` contiguo desde 1, que el primer evento sea `pendiente`, que `prev_event_hash` sea el `event_hash` anterior (o 64 ceros) y ningún evento después de `completado` o `fallido`.
- **Cadenas.** Las de provenance y auditoría, enlazadas igual.

El esquema no define columnas de puntaje, ranking, recomendación, selección, tokens de persona, media ni variables de RF-29. Esa ausencia de columnas no basta como garantía: `text_synthetic` es `TEXT` y podría contener cualquier texto. La garantía sobre el contenido es la correspondencia con el origen autorizado (§11).

## 6. Ciclo de vida y fallo cerrado

### 6.1 Tres planos de estado

| Plano | Qué es | Valores |
|---|---|---|
| Estado lógico persistido | Lo que está confirmado en la base `:memory:` mientras vive la conexión | Principal inmutable y eventos de solo inserción; el estado del run es el último evento confirmado (F33 §6) |
| Estado del objeto Python | Qué operaciones admite el almacén | `abierto`, `activo`, `finalizado`, `bloqueado` y `purgado` |
| Estado de la conexión | Si la base sigue siendo utilizable | `abierta`, `contaminada` (tras un fallo de escritura; no se reutiliza) y `cerrada` |

`bloqueado` existe solo en el objeto. No es una columna ni un evento: el principal no tiene ningún estado mutable.

| Estado del objeto | Se entra con | Conexión |
|---|---|---|
| `abierto` | `open_tenant_store`: origen autorizado, preflight, esquema, autorizador y fila `tenant_context` | `abierta` |
| `activo` | `create_run`: principal y evento `pendiente` en una transacción | `abierta` |
| `finalizado` | Evento terminal confirmado: `completado`, o `fallido` pedido por el pipeline con `append_event` | `abierta` |
| `bloqueado` | Cualquier fallo de una escritura o del preflight (§6.2) | `cerrada`, o cierre no verificado |
| `purgado` | `purge` | `cerrada` |

| Operación | `abierto` | `activo` | `finalizado` (`completado`) | `finalizado` (`fallido`) | `bloqueado` | `purgado` |
|---|---|---|---|---|---|---|
| `create_run` | Sí | No | No | No | No | No |
| `append_event`, `append_evidence`, `append_audit` | No | Sí, con transición válida | No | No | No | No |
| `read_run`, `list_events`, `current_state` | No | Sí | Sí | Sí | No | No |
| `list_evidence`, `list_audit`, `snapshot` | No | Sí | Sí | No: sin resultado parcial (DH-B10) | No | No |
| `preflight_report` | Sí | Sí | Sí | Sí | Sí | Sí |
| `diagnostic` | No | No | No | No | Sí | No |
| `purge` | Sí | Sí, como cierre excepcional (§6.2) | Sí | Sí | No | No |

Fuera de la tabla, la operación falla con `E-CICLO`; en `bloqueado`, con `E-BLOQUEADO`; en `purgado`, con `E-PURGADO`. Las transiciones del run siguen el camino de A (`pendiente` → `validando` → `registrado` → `transformado` → `en_revision` → `revisado` → `completado`), y desde cualquier estado no terminal se puede pasar a `fallido`.

**Propiedad del hilo (corrección de M01).** El almacén pertenece al hilo que lo abre. Toda operación que usa la conexión comprueba, después del ciclo de vida y antes de tocar SQLite, que se llama desde ese hilo; si no, falla con `E-HILO`, no cambia el estado y no declara ningún cierre, de modo que el propietario puede purgar después. `preflight_report` y `diagnostic` no usan la conexión y se admiten desde cualquier hilo. La restricción de hilo de SQLite (`check_same_thread`) se mantiene.

### 6.2 Cierre excepcional

Si falla una escritura (validación, contrato, origen, postcondición o `sqlite3.Error`), o si `purge` llega con el run todavía activo:

0. **Bloqueo (corrección de M02).** Antes de tocar la conexión, el objeto pasa a `bloqueado`: ningún fallo posterior lo devuelve a un estado utilizable.
1. **`ROLLBACK`** de la unidad actual. Si falla, la conexión queda `contaminada` y se salta al paso 4.
2. **Evento `fallido`, solo si es válido.** Se intenta registrar únicamente si el principal existe y está confirmado, el último evento no es terminal y el rollback terminó bien. Se hace en su propia transacción, con su código (`E-ABORTADO` cuando lo pide `purge`). Si se confirma, se relee para el diagnóstico.
3. **Diagnóstico.** Se reúnen los hechos observables: conteos, último `event_hash` y `PRAGMA database_list`. Lo que no se pueda leer queda como `no_disponible`; nunca se rellena. Un fallo inesperado en los pasos 1 a 3 no interrumpe el cierre.
4. **Cierre en `finally`.** La conexión se cierra siempre, aunque hayan fallado el rollback, el evento, el diagnóstico o el comprobante. Después, y solo desde el hilo propietario, se comprueba que una consulta lanza `ProgrammingError`.
5. **Estado final.** El diagnóstico se construye como una operación falible (corrección de M02). Si su construcción falla, se degrada a un mínimo veraz:
   - conserva los hechos ya establecidos (tipo de cierre, código del fallo original, evento fallido y estado de la conexión) y lo disponible del run y del tenant;
   - deja `no_disponible` en lo demás;
   - añade la causa en `receipt_error`;
   - calcula el hash solo si puede.

   El objeto queda en `bloqueado` y el diagnóstico en memoria, accesible con `diagnostic(store)`. Si el cierre lo pidió `purge`, el objeto pasa a `purgado` y el diagnóstico es su comprobante (§9). El llamador recibe siempre `SbxbStoreError` con el código del fallo original.

| Campo del diagnóstico | Valores |
|---|---|
| `failed_event` | `FAILED_EVENT_COMMITTED`, con el evento releído y su `event_hash`, o `FAILED_EVENT_UNAVAILABLE`, sin afirmar que exista |
| `connection` | `CONNECTION_ABORTED`, cerrada y comprobada, o `CLOSE_UNVERIFIED` si no se pudo comprobar el cierre |
| `error_code` | Código del fallo original |
| `observed` | Conteos y hashes leídos, o `no_disponible` |

Ejemplos:

- **Falla `create_run`.** No hay principal, y la FK impide el evento. El diagnóstico dice `FAILED_EVENT_UNAVAILABLE` y `CONNECTION_ABORTED`.
- **Falla `append_evidence` con el run activo.** Las cuatro filas se deshacen. Si `fallido` se confirma, el diagnóstico dice `FAILED_EVENT_COMMITTED`; si no, `FAILED_EVENT_UNAVAILABLE`.

DH-B10 se cumple en el informe. El resultado del run es fallido, nunca completado, sin resultado parcial y con el gate en código distinto de cero. Que el evento `fallido` exista dentro de la base se informa con exactitud, no se supone.

## 7. `pipeline_run`: principal inmutable

- Una sola fila por almacén. La crea `create_run` con la semilla y el `clock_start` del escenario, y el almacén completa las constantes.
- La identidad, el tenant, la versión del dataset de origen, las versiones de contrato y pipeline, el algoritmo de hash, la semilla y `clock_start` no cambian. No existe ninguna sentencia `UPDATE`, y el trigger y el autorizador la rechazarían.
- El estado vigente no es una columna del principal, sino el último evento confirmado. Si `create_run` falla, no hay principal ni eventos (§6.2).

## 8. Eventos de solo inserción

- **Valores que asigna el almacén.** `append_event` recibe `state`, `at`, `error_code` y, opcionalmente, una acción de auditoría. El almacén asigna `seq` (el siguiente), `event_id`, `prev_event_hash` y `event_hash`, este último con `chain_hash` de A: SHA-256 del JSON canónico del objeto sin su propio campo de hash.
- **Atomicidad (Q7).** Si se indica una acción de auditoría que acredita esa transición, el evento y su `audit_entry` se insertan en la misma transacción. Si falla uno, se deshacen los dos.
- **Orden.** Por `seq` (`ORDER BY seq`); nunca por `rowid` ni por un orden de inserción implícito.
- **Tiempo.** `at` es un instante lógico del escenario (`YYYY-MM-DDTHH:MM:SS`, sin zona), no anterior a `clock_start` ni al evento previo. El almacén nunca lee el reloj del sistema.
- **Sin `UPDATE` ni `DELETE`.** Un reintento requiere un almacén nuevo; la base nunca se reescribe.
- **Auditoría.** `audit_entry` sigue las mismas reglas de cadena, con las acciones del enum de A.

## 9. Purga y comprobante

La purga es la frontera de destrucción lógica del almacén (DH-B06, B0 §5.3):

1. **Run activo.** Si el run sigue activo, se aplica el cierre excepcional de §6.2 con `E-ABORTADO`.
2. **Hechos para el comprobante.** Si no, el objeto pasa a `bloqueado` antes de tocar la conexión (corrección de M02), y se leen conteos por tabla, último `event_hash` y `PRAGMA database_list`. Lo que no se pueda leer queda `no_disponible`.
3. **Cierre en `finally`.** La conexión se cierra aunque haya fallado el paso 2.
4. **Comprobación.** Desde el hilo propietario, una consulta sobre la conexión cerrada debe lanzar `sqlite3.ProgrammingError` (corrección de M01: en ese hilo solo puede deberse al cierre). Si no la lanza, el comprobante lo dice (`CLOSE_UNVERIFIED`) y la purga termina con error.
5. **Referencia.** El almacén descarta la conexión y pasa a `purgado`. Después, cualquier llamada falla con `E-PURGADO`.

El comprobante se construye como en el paso 5 de §6.2: si su construcción falla, la purga se completa igual con el comprobante mínimo veraz, con su causa en `receipt_error`.

El comprobante es un objeto Python en memoria (`dict`): no es un archivo, no va a otra base ni a ninguna persistencia productiva. Representa el estado `purgado` de A, encadenado al último evento, y solo contiene hechos observados:

| Campo | Contenido |
|---|---|
| `closure_kind` | `purga` o `aborto` |
| `pipeline_run_id`, `synthetic_organization_id` | Run y tenant del almacén (`sin_run` si se purgó en `abierto`) |
| `final_state` | `completado`, `fallido` o `no_disponible` |
| `failed_event` | Como en §6.2, si hubo cierre excepcional |
| `last_event_hash` | Enlace con la cadena destruida, o `no_disponible` |
| `counts` | Filas por tabla al cerrar, o `no_disponible` |
| `file_backed` | `false` según `PRAGMA database_list`, o `no_disponible` |
| `connection` | `CONNECTION_ABORTED`, `CLOSED` o `CLOSE_UNVERIFIED` |
| `receipt_hash` | SHA-256 del JSON canónico del comprobante sin este campo |

La purga nunca es `DELETE FROM` sobre la misma conexión viva. No hay archivo que borrar. B2 no afirma borrado seguro de RAM, borrado criptográfico ni ninguna garantía física sobre la memoria: solo que la base deja de ser alcanzable por la API y por la conexión.

## 10. Identidad y determinismo

**Identidad (alineada con B0 §5.2).** Los identificadores de B se derivan solo del tenant, de la semilla y de ordinales del reloj lógico del run, con prefijos `SBB*` distintos de los de A, y nunca copian el identificador de A.

| Objeto | Forma | Ejemplo con `ORG-S1` y semilla `20261008` |
|---|---|---|
| Espacio de nombres del run | `<org>-<semilla con 10 dígitos>` | `ORG-S1-0020261008` |
| Run | `SBBR-<espacio>` | `SBBR-ORG-S1-0020261008` |
| Evento | `SBBV-<espacio>-<seq:02>` | `SBBV-ORG-S1-0020261008-01` |
| Auditoría | `SBBA-<espacio>-<seq:02>` | `SBBA-ORG-S1-0020261008-01` |
| Fuente, evidencia, procedencia y revisión | `SBBS`, `SBBE`, `SBBP` y `SBBH` con `-<espacio>-<ordinal de la evidencia:06>` | `SBBE-ORG-S1-0020261008-000001` |

- **Mismo escenario, misma identidad.** El mismo tenant con la misma semilla da exactamente los mismos identificadores.
- **Escenarios distintos, identidades distintas.** Otra semilla u otro tenant dan otro espacio de nombres.
- **Una semilla, un escenario.** Dentro del contrato, una semilla identifica un único escenario de un tenant. El principal guarda sus parámetros (`seed`, `clock_start`, versión del dataset y versiones de contrato). Si dos runs con el mismo identificador tienen principales distintos, se viola el contrato y el gate lo rechaza (P22).
- **Valores prohibidos.** Nunca `rowid`, `uuid`, `random` ni `secrets`.
- **Diferencia con F33.** F33 §7 prevé un `analysis_run_id` UUID aleatorio para el runtime productivo. En el sandbox rige B0 §5.2, que exige identificadores deterministas. No es una contradicción: son ámbitos distintos.

**Determinismo.** Dos ejecuciones del mismo escenario deben dar el mismo resultado lógico, byte a byte en `snapshot()` y en el comprobante:

- **Tiempo.** Solo instantes lógicos del escenario. Ni `datetime.now`, ni `time.time`, ni `CURRENT_TIMESTAMP`; el autorizador niega además las funciones de fecha y aleatorias.
- **Orden.** Todas las lecturas con `ORDER BY` explícito por `seq` o por ordinal.
- **Serialización.** JSON canónico de A (`canon`: claves ordenadas, sin espacios, UTF-8 sin escapar), sin rutas, locale ni zona horaria.

El double-run completo es de una fase posterior; B2 solo garantiza que el almacén no lo impide.

## 11. Contrato sintético y procedencia

La garantía de B2 está acotada: **solo persiste evidencia que satisface el contrato sintético verificable de A y F34.** No afirma detectar toda la PII ni impedir cualquier contenido en una columna `TEXT`. Afirma que el contenido persistido es, exactamente, una fila autorizada de F34 transformada solo por T1.

**Origen autorizado.** Al abrir el almacén, el módulo lee en binario los cuatro CSV de F34 en sus rutas fijas. Exige su SHA-256 exacto, el del manifiesto de `f34-synth-1.1.0`:

| Archivo | SHA-256 |
|---|---|
| `datos-sinteticos/dataset/evidence.csv` | `ec6aef1b297a2f5688800d883df5a681c7c4a8070af406e9532cfd785b4b0563` |
| `datos-sinteticos/dataset/criteria.csv` | `65898a8d9c8c431bfff48a84859647f5c69c9299485cf02e2d27ddfb52f5ee12` |
| `datos-sinteticos/dataset/vacancies.csv` | `04def2e4f115c921586ba46c603c552c3a583344d54a67d69f75ca5c64f00b7a` |
| `datos-sinteticos/dataset/applications.csv` | `15a9a125a11e6c9d14e6d5d239c1c10685786785db7ca02747c0b0230cd5ba82` |

Con ellos construye en memoria el índice del tenant: las filas con `state = vinculada`, `source_type = synthetic`, `source_type_ev` en `formulario`, `nota_entrevista` o `prueba`, y cuya organización es la del tenant. La organización se comprueba por el criterio y por la postulación, con `criteria.csv`, `vacancies.csv` y `applications.csv`, como hace A. El índice no guarda tokens de persona.

**Antes de persistir una evidencia**, `append_evidence` exige, en este orden:

1. `origin_record_id` (`SYN-NNNNNN`) presente en el índice del tenant. Así se comprueban la referencia F34, el origen permitido y el tenant coherente.
2. `origin_file_sha256` igual a la constante de `evidence.csv`. El almacén pone `origin_file` y `origin_dataset_version` desde el contrato; el llamador no los aporta.
3. `criterion_ref` y `evidence_kind` iguales al `criterion_id` y al `source_type_ev` de esa fila.
4. Los seis marcadores synthetic-only de A.
5. `text_synthetic` igual, carácter a carácter, a `T1(evidence_text)`, con T1 exactamente como `normalize_text` de A.
6. `hash_before` igual a `content_hash` sobre el texto original, y `content_hash` (`hash_after`) igual a `content_hash` sobre el texto transformado, con la función de A.

Unos metadatos y una procedencia válidos no bastan: si el texto no es el de su fila de origen, la evidencia se rechaza (`E-ORIGEN`, P31).

**Defensa adicional.** Los detectores de PII de A §5 (correos, URL, números de 8 u 11 dígitos, teléfonos, data URI y base64) siguen aplicándose al texto. Es una heurística, no una detección universal.

**Revisión simulada.** Solo admite `integridad_y_procedencia` con `conforme` u `observado` (DH-05 de A): nunca juzga a la persona sintética.

**Lo que el contrato excluye.** Personas o datos reales, CV, documentos, audio, vídeo, biometría, rostro, voz, inferencias de emoción, personalidad, honestidad, inteligencia, estrés o salud, datos sensibles, puntajes, rankings, recomendaciones, selecciones, OCR, *parsing*, embeddings y búsqueda semántica. Quedan excluidos porque B2 solo acepta contenido de origen F34 autorizado: el dataset sintético que validan F34 y SBX-01..SBX-04. No los excluye la ausencia de columnas.

**RF-23** no se toca: ninguna tabla tiene decisión, selección ni contratación.

## 12. RF-29

RF-29 sigue experimental, solo sobre el proceso y no productivo. B2 no almacena nada de RF-29:

- ni snapshots de proceso, ni variables del contrato RF-29;
- ni etiquetas de demora, ni salidas de modelo, ni puntajes de riesgo.

Por eso no hay selección de candidatos, PII ni identificadores de candidato, ni sustitución del ranking, y el puntaje no se persiste. Ningún dato del almacén alimenta `ml-service/` ni el runtime (F34E). Guardar evidencia de RF-29 en el sandbox requeriría una autorización nueva.

## 13. API interna

Módulo `sbxb_store.py`, API Python interna y experimental. No es una API HTTP.

| Función | Entrada | Salida | Invariantes y errores |
|---|---|---|---|
| `open_tenant_store(tenant)` | `dict` con los 4 campos de `SyntheticTenantContext` | `TenantRunStore` en `abierto` | Origen autorizado, preflight, esquema y autorizador verificados. `E-TENANT`, `E-CONTRATO`, `E-ORIGEN`, `E-PREFLIGHT` |
| `create_run(store, seed, clock_start)` | Entero de 0 a 2147483647; instante lógico | `dict` del principal, con el evento `pendiente` creado | Una vez por almacén; identidad de §10. `E-CICLO`, `E-CONTRATO` |
| `append_event(store, state, at, error_code='', audit_action=None)` | Estado del enum, instante lógico, código `E-[A-Z]{2,12}` solo con `fallido` y acción de auditoría opcional | `dict` del evento (y de su auditoría) con `seq`, identificadores y hashes asignados | Transición válida, instante monótono, atómico con la auditoría. `E-CICLO`, `E-CONTRATO` |
| `append_evidence(store, evidence)` | `origin_record_id`, `origin_file_sha256`, `criterion_ref`, `evidence_kind`, `text_synthetic`, `hash_before`, `content_hash`, `validation_status`, `review_status` y sus instantes | `dict` con fuente, evidencia, revisión simulada y procedencia, con identificadores y cadena asignados | Comprobaciones de §11; cuatro filas en una transacción, en orden FK. `E-ORIGEN`, `E-PROHIBIDO`, `E-CONTRATO`, `E-HASH`, `E-CICLO` |
| `append_audit(store, action, at)` | Acción del enum de A e instante lógico | `dict` de la entrada con identificador y cadena | `E-CICLO`, `E-CONTRATO` |
| `read_run(store)` | — | `dict` del principal | Según §6.1 |
| `list_events(store)`, `list_audit(store)`, `list_evidence(store)` | — | `tuple` de `dict`, en orden de `seq` u ordinal | Según §6.1 |
| `current_state(store)` | — | Estado del último evento confirmado | — |
| `snapshot(store)` | — | `bytes` del JSON canónico de las ocho tablas | Solo `activo` o `finalizado` (`completado`) |
| `preflight_report(store)` | — | `dict` de solo lectura con los hechos del preflight | Sin acceso a `PRAGMA` |
| `diagnostic(store)` | — | `dict` del cierre excepcional | Solo en `bloqueado` |
| `purge(store)` | — | `dict` del comprobante (§9) | Una vez. `E-PURGADO` si se repite |

- **Errores.** Una sola excepción, `SbxbStoreError(code, message)`. Los códigos cumplen el patrón de A `^E-[A-Z]{2,12}$`: `E-TENANT`, `E-CICLO`, `E-CONTRATO`, `E-ORIGEN`, `E-PROHIBIDO`, `E-HASH`, `E-SQLITE`, `E-PREFLIGHT`, `E-ABORTADO`, `E-BLOQUEADO`, `E-PURGADO` y, desde la corrección de M01, `E-HILO`: operación desde un hilo distinto del propietario, sin tocar SQLite ni cambiar el estado (§6.1).
- **Fallo cerrado.** Un `sqlite3.Error` nunca se ignora: se convierte en `E-SQLITE` y activa el cierre excepcional (§6.2).
- **Encapsulamiento.** El objeto no expone la conexión, los cursores, el catálogo ni el índice de origen. Los nombres internos no son API y el gate prohíbe usarlos fuera del módulo.

## 14. Modelo de fallos

| Caso | Detección | Resultado |
|---|---|---|
| Tenant equivocado o ajeno en una fila | API, índice de origen y trigger de `tenant_context` | `E-TENANT` o `E-ORIGEN`; cierre excepcional |
| Contenido que no corresponde a su fila F34 | Comparación con `T1` del origen y recálculo de hashes | `E-ORIGEN`; cierre excepcional |
| Origen F34 alterado | SHA-256 de los cuatro CSV | `E-ORIGEN`; el almacén no se abre |
| Entorno SQLite o Python incompatible | Preflight | `E-PREFLIGHT`; el almacén no se abre |
| Operación sin tenant o sin almacén | No existe API sin almacén ligado a un tenant | No hay escritura posible |
| FK inválida o conflicto de clave | `foreign_keys = ON`; `INSERT` simple | `E-SQLITE`; cierre excepcional |
| Inserción que no afecta una fila | Postcondición `rowcount == 1` | `E-SQLITE`; cierre excepcional |
| Fallo al crear el principal | Ídem | `FAILED_EVENT_UNAVAILABLE`; conexión abortada |
| Escritura tras `completado`, `fallido`, bloqueo o purga | Ciclo de vida y trigger de terminal | `E-CICLO`, `E-BLOQUEADO` o `E-PURGADO` |
| Carga útil con campos de más, de menos o patrones inválidos | Validación cerrada | `E-CONTRATO`; cierre excepcional |
| Dato con marcador ausente, marcado o PII detectada | Validación synthetic-only y heurísticas | `E-PROHIBIDO`; cierre excepcional |
| `ATTACH`, extensión, `PRAGMA` o DDL | Inalcanzables por el catálogo; límite y autorizador como defensa adicional | — |
| Fallo del rollback, del evento `fallido` o del comprobante | Cierre en `finally` | Diagnóstico con `no_disponible`; conexión cerrada |
| Persistencia en disco | `PRAGMA database_list` y el gate (P08) | Purga con error; gate FAIL |

## 15. Decisiones

| ID | Decisión | Estado tras la auditoría de diseño |
|---|---|---|
| DH-B2-01 | Rutas exactas `docs/academico/evidencia-sbx-b2/` y `docs/academico/tools/f35sbxb2/`, enumeradas por el gate y sin excepción general a SCP ni a FSY | Q2: APROBADA |
| DH-B2-02 | 1 tenant, 1 run o escenario y 1 conexión literal `:memory:` por almacén | Q3: MODIFICADA Y RESUELTA |
| DH-B2-03 | Esquema de ocho tablas derivado de A, con la equivalencia con `analysis_run` y `analysis_run_events` documentada | Sin observaciones |
| DH-B2-04 | API cerrada y catálogo fijo como frontera primaria; triggers, autorizador, límites y postcondición como defensa adicional; preflight sin respaldo silencioso | B2-M01, Q4 y Q5 |
| DH-B2-05 | `purgado` vive en el comprobante en memoria, encadenado al último evento y solo con hechos observados | Sin observaciones; precisado por B2-M02 |
| DH-B2-06 | Identidad `<org>-<semilla>` con ordinales del run (B0 §5.2) | B2-M03 |
| DH-B2-07 | El registro de B1 cerrada y del estado de B2 en `CLAUDE.md` y `docs/PROGRESS.md` lo hará el incremento ejecutable del gate de B2, en una única transición monotónica y auditada `HISTORICAL_B1_BLOB` → `B2_GOVERNANCE_BLOB` | Q1: MODIFICADA Y RESUELTA |

Las decisiones Q1–Q9 completas están en el [contrato de verificación, §4](F35SBXB_B2_Contrato_Verificacion.md#4-decisiones-q1q9).

## 16. Observaciones de la inspección

Comprobaciones exploratorias hechas el 11/10/2026 con Python 3.12.5 y SQLite 3.45.3, en una carpeta temporal fuera del repositorio. No son pruebas del almacén: justifican los controles de §4.

| Sentencia sobre una fila existente protegida por triggers, con `recursive_triggers = ON` | Resultado | Acciones que vio el autorizador |
|---|---|---|
| `INSERT` simple | `IntegrityError` por la clave única | `INSERT` |
| `INSERT OR REPLACE` | `IntegrityError` del trigger de borrado | `INSERT`, `SELECT` |
| `INSERT OR IGNORE` | Sin error, `rowcount = 0`, fila intacta | `INSERT`, `READ`, `SELECT` |
| `ON CONFLICT ... DO NOTHING` | Sin error, `rowcount = 0`, fila intacta | `INSERT`, `READ`, `SELECT` |
| `ON CONFLICT ... DO UPDATE` | `IntegrityError` del trigger de modificación | `INSERT`, `READ`, `SELECT`, `UPDATE` |

Otras observaciones de la inspección:

- **Sin `recursive_triggers`**, `INSERT OR REPLACE` y `REPLACE INTO` sustituyeron la fila protegida. Por eso `recursive_triggers = ON` se exige en el preflight.
- **`INSERT OR IGNORE` y `DO NOTHING`** no los distingue el autorizador ni los rechaza el motor: son silenciosos. Por eso la frontera es el catálogo, con la postcondición de una fila como defensa adicional, sin ningún trigger especial.
- **Con `setlimit(SQLITE_LIMIT_ATTACHED, 0)`**, `ATTACH` falló.
- **El autorizador por lista blanca** negó `UPDATE`, `DELETE`, `PRAGMA` de escritura, `DROP TRIGGER`, `CREATE TABLE`, `ATTACH`, `load_extension` y `sqlite_version()`.
- **Tras `close()`**, `execute` lanzó `ProgrammingError`.
- **Ninguna operación** creó archivos en la carpeta de trabajo.

La implementación añadió tres observaciones sobre el autorizador y el motor, sin cambiar el diseño: las lecturas de un `EXISTS` dentro de un trigger, las funciones de los `CHECK` y el resultado de `DO UPDATE` con y sin autorizador (O1–O3 del [contrato, §5.6](F35SBXB_B2_Contrato_Verificacion.md#56-observaciones-de-la-implementación)).
