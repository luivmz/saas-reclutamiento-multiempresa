# F35-SBX-B — B2: contrato de verificación

> Incremento B2 de F35-SBX-B: versión 2.1 del contrato (11/10/2026), implementada el 12/10/2026. Estado: **B2 = IMPLEMENTADA / CANDIDATA A AUDITORÍA INDEPENDIENTE**.
>
> - Define las pruebas y el gate sucesor que cumple la implementación de B2. Desde el 12/10/2026 son ejecutables, y la evidencia de la implementación está en §5.
> - La versión 2 alinea el contrato con las correcciones B2-M01..B2-M05 y fija Q1–Q9 (§4).
> - La versión 2.1 completa M05 y Q1 tras la reauditoría de `eaac212`: la transición de gobierno de B2 es única y monotónica (§2.3, P25 y P33). La reauditoría final focal de esta versión dio el veredicto «B2-DESIGN APROBADO PARA IMPLEMENTACIÓN».
> - El diseño que se verifica está en [F35SBXB_B2_Diseno_Almacen.md](F35SBXB_B2_Diseno_Almacen.md).
> - El código de la implementación es de desarrollo y NO AUDITADO (Q6): un PASS del gate no equivale a confianza ni a cierre.

## 1. Matriz de pruebas

Cada prueba vive dentro del gate de B2, como en A y en B1, sin `tests/` productivos. Usa el almacén cargado desde los bytes que el gate ya verificó (§2.4), las filas autorizadas de F34 y los fixtures de A.

- **Por la API.** La mayoría de las pruebas usan solo la API.
- **Por la vía interna.** Las que dicen «vía interna» actúan desde el arnés adversarial del gate, sin pasar por la API, para comprobar las defensas adicionales del motor. Esa vía no forma parte de la API.
- **Fallo cerrado.** Una prueba que no se pueda ejecutar cuenta como fallo.

| ID | Qué demuestra | Procedimiento | Resultado esperado | Regla | Origen |
|---|---|---|---|---|---|
| P01 | El almacén usa `:memory:` | `preflight_report`; análisis estático de `connect` | `database_list` sin ruta; `connect` solo con la constante `':memory:'` | STA, DYN | DH-B07 |
| P02 | FK activas | `preflight_report` (`foreign_keys` releído en el preflight interno); vía interna: inserción con FK rota | `1`; la inserción falla y activa el cierre excepcional | DYN | B0 §5.4 |
| P03 | El tenant A no ve los datos del tenant B | Dos almacenes, ORG-S1 y ORG-S2, con datos distintos; listar desde cada uno | Cada uno devuelve solo lo suyo; ningún identificador del otro tenant | DYN, ISO | DH-B08; TSBB-02 |
| P04 | Conexiones independientes | Comparar las conexiones internas de dos almacenes; purgar uno y consultar el otro | Objetos distintos, cada uno con su propia base | DYN, ISO | Q3 |
| P05 | Tenant obligatorio y coherente | Abrir sin tenant o con uno inválido; evidencia cuya fila F34 es de otra organización | `E-TENANT`; `E-ORIGEN`. Por la vía interna, el trigger rechaza una fila de otra organización | DYN, ISO | DH-B08 |
| P06 | Valores siempre como parámetros | AST: cada `execute` recibe una entrada del catálogo y una tupla | Ninguna concatenación ni formato en SQL | STA | B0 §5.4 |
| P07 | `ATTACH` no expuesto | AST: ni `ATTACH` ni `DETACH` en el catálogo; vía interna: `ATTACH` | Ausentes de la API; por la vía interna, el límite de bases adjuntas y el autorizador lo niegan | STA, DYN | B0 §5.4 |
| P08 | Ningún archivo SQLite en lo observable | `database_list`; recorrido del repositorio y de un directorio de trabajo temporal antes y después de la batería | Sin archivos nuevos (`.db`, `-journal`, `-wal` ni otro). Garantía acotada a esas ubicaciones: no prueba la ausencia de temporales del sistema operativo ni de memoria paginada | DYN | TSBB-08; Q4 |
| P09 | `pipeline_run` inmutable | Segundo `create_run`; vía interna: `UPDATE` y `DELETE` del principal | `E-CICLO`; por la vía interna, triggers y autorizador lo rechazan. Un único principal, sin cambios | DYN | F33 §6 |
| P10 | Eventos de solo inserción | Evento fuera de orden o tras un estado terminal; vía interna: `UPDATE`, `DELETE` y `seq` no contiguo | `E-CICLO`; por la vía interna, rechazo. La secuencia sigue intacta | DYN | TSBB-04 y TSBB-05 |
| P11 | Orden determinista | Insertar y listar; dos ejecuciones del mismo guion | Listas en orden de `seq` u ordinal; `snapshot()` idéntico byte a byte | STA, DYN, DET | TSBB-12 |
| P12 | La purga cierra la conexión y solo informa hechos | `purge` en `abierto`, `activo` y `finalizado`; vía interna: fallo inyectado al leer los conteos | Comprobante con `connection = CLOSED` (o `CONNECTION_ABORTED`), `file_backed = false` y `post_close_check`. Con el fallo inyectado, la conexión se cierra igual y los conteos quedan `no_disponible` | DYN, PUR | DH-B06; §9 del diseño |
| P13 | La conexión purgada es inutilizable | Cualquier operación de la API, y una consulta interna, tras `purge` | `E-PURGADO`; la consulta interna lanza `ProgrammingError` | DYN, PUR | B0 §5.3 |
| P14 | El tenant B sigue funcionando tras purgar A | Purgar ORG-S1 y operar con ORG-S2 | ORG-S2 intacto y operativo | DYN, ISO | DH-B08 |
| P15 | Entrada sintética autorizada admitida | Las evidencias de los fixtures de A, desde sus filas F34 | Se registran; `content_hash` y `hash_before` coinciden con los de A (nivel 1 de DH-B05) | DYN, DAT | DH-B05 |
| P16 | Dato real o prohibido rechazado | Variantes con un correo, un DNI, una URL, base64, marcado, sin marcador o con `evidence_kind = cv` | `E-ORIGEN` (el contenido no es el de su fila) o `E-PROHIBIDO`; cierre excepcional. Las heurísticas de PII son defensa adicional, no la garantía | DYN, DAT | TSBB-01 y TSBB-13 |
| P17 | Sin puntaje, recomendación ni selección | Esquema y API sin esos campos; carga útil con `score` o `selected` | Columnas ausentes; `E-CONTRATO` | STA, DYN, CAP | Contratos 2 y 4 |
| P18 | Sin alcance C | Esquema sin OCR, *parsing*, embeddings ni búsqueda semántica; `evidence_kind = documento` | Ausentes; `E-ORIGEN` o `E-PROHIBIDO` | STA, DYN, CAP | SBX-17 |
| P19 | Sin dependencias nuevas | AST de los módulos de B2; archivos de dependencias del proyecto | Solo la lista de §2.2; `sqlite3` solo en el almacén; archivos de dependencias sin cambios | DEP, FSY | TSBB-09 |
| P20 | Sin runtime productivo | Delta y superficies del runtime; referencias a `app/`, `database/`, `routes/`, `.env`, PostgreSQL o Redis | Sin cambios ni referencias | SCP, FSY, STA | SBX-15 y SBX-16 |
| P21 | Un fallo de escritura falla cerrado | Vía interna: `sqlite3.Error` inyectado en cada escritura; fallo en `create_run`; fallo del `ROLLBACK`; fallo al registrar `fallido` | `ROLLBACK` sin evidencia parcial. `FAILED_EVENT_COMMITTED` solo si `fallido` se confirmó; si no, `FAILED_EVENT_UNAVAILABLE` (siempre en el fallo de `create_run`). Conexión cerrada (`CONNECTION_ABORTED`) en todos los casos y objeto `bloqueado` | DYN | DH-B10; B2-M02 |
| P22 | Identidad determinista | Mismo tenant y semilla dos veces; otra semilla; otro tenant con la misma semilla; mismo identificador con otro `clock_start`; instante anterior a `clock_start` | Mismo escenario, mismos identificadores, hashes y comprobante. Otra semilla u otro tenant, otro espacio de nombres. Mismo identificador con otro principal, rechazo. Instante inválido, `E-CONTRATO`. Sin reloj del sistema (AST) | STA, DYN, DET | B0 §5.2; B2-M03 |
| P23 | Ninguna conexión compartida entre tenants | AST: sin conexión ni almacén a nivel de módulo; en ejecución, cada almacén con su conexión | Ninguna variable global de conexión ni registro por organización | STA, ISO | Q3 |
| P24 | La purga no es un `DELETE` | AST: sin `DELETE` en el catálogo ni en `purge`; tras purgar, conexión cerrada | Sin `DELETE`; conexión cerrada | STA, PUR | DH-B06 |
| P25 | B1 sigue íntegra y el gobierno cambia una sola vez | Regla B1F (§2.3) sobre la historia real | A) Conjunto auditado de B1 íntegro desde `8e94a60`. B) Conjunto del cierre íntegro desde `3d9b783`. C) El padre de la transición de gobierno de B2 tiene el blob histórico de B1. D) La transición tiene el blob nuevo de B2. E) Todos los descendientes relevantes conservan el blob nuevo. F) Cualquier tercer blob falla | B1F | B2-M05; Q1 |
| P26 | Las políticas de conflicto no rompen la solo inserción | **A) API y catálogo:** AST del catálogo y de la API; vía interna, una sentencia `OR IGNORE` sometida a la postcondición del almacén. **B) Motor**, vía interna: `INSERT OR REPLACE`, `REPLACE INTO`, `INSERT OR IGNORE`, `DO NOTHING` y `DO UPDATE` sobre filas existentes | **A)** Ninguna de esas formas en el catálogo; ningún parámetro de la API las permite; la postcondición `rowcount == 1` falla cerrada. **B)** Se registra el comportamiento real: `OR REPLACE`, `REPLACE` y `DO UPDATE` fallan; `OR IGNORE` y `DO NOTHING` no fallan ni cambian nada (`rowcount = 0`). Ninguna fila cambia ni desaparece. El motor no se presenta como la garantía | STA, DYN | B2-M01 |
| P27 | El autorizador niega lo que el catálogo no usa | Vía interna, tras abrir: `PRAGMA foreign_keys = OFF`, `DROP TRIGGER`, `CREATE TABLE`, `load_extension`, `random()`, `datetime('now')` | Todo se niega en el motor (defensa adicional) | DYN | DH-B2-04 |
| P28 | Esquema cerrado e igual al contrato | `preflight_report` (`table_info` del preflight interno) y DDL del catálogo frente a la lista independiente del gate | Igualdad exacta de tablas, columnas, tipos y restricciones; sin ninguna API de `PRAGMA` | STA, DYN, DAT | Doble llave; TSBB-10 |
| P29 | Relaciones y hashes desde la entrada autorizada | Para cada evidencia, recalcular desde su fila F34 `T1(evidence_text)`, `hash_before` y `content_hash`; comprobar evidencia ↔ fuente ↔ fila F34 ↔ procedencia ↔ revisión; recalcular las cadenas; proyectar frente al oráculo de A; alterar un eslabón | Todo coincide con la entrada autorizada, no solo consigo mismo; nivel 1 frente a A igual; la alteración se detecta | DYN | DH-B05; TSBB-03; B2-M04 |
| P30 | Ciclo de vida completo | Cada operación en cada estado de §6.1 del diseño, incluido `bloqueado`; vía interna: fallo del `ROLLBACK` | Lo no permitido falla con `E-CICLO`, `E-BLOQUEADO` o `E-PURGADO`. Tras un cierre excepcional solo queda `diagnostic`, y la conexión está cerrada aunque el `ROLLBACK` haya fallado | DYN | DH-B10; B2-M02 |
| P31 | Metadatos válidos con contenido ajeno se rechazan | Evidencia con `origin_record_id`, criterio, tipo, procedencia y hashes coherentes entre sí, pero con el texto de otra fila F34, o un texto alterado tras T1 | `E-ORIGEN`; ninguna fila persistida; cierre excepcional | DYN, DAT | B2-M04 |
| P32 | Modificar y restaurar un artefacto del cierre se detecta | Clon desechable: un commit modifica el manifiesto de B1-FREEZE y otro lo restaura | B1F falla por historia | B1F | B2-M05 |
| P33 | El gobierno no vuelve atrás tras su transición | Clon desechable: la secuencia de commits blob histórico → blob nuevo de B2 → blob histórico → blob nuevo de B2 en `CLAUDE.md` y `docs/PROGRESS.md` | B1F falla, aunque HEAD termine en el blob nuevo: un descendiente de la transición vuelve al blob histórico y hay una segunda introducción del blob nuevo. Demuestra que el gate lee la ascendencia y no solo el blob final | B1F | B2-M05; Q1 |

P26 a P30 se justifican así:

- P26 separa la frontera primaria del comportamiento del motor.
- P27 y P28 convierten en comprobaciones dos controles que, si no, quedarían solo en el código.
- P29 ancla la integridad a la entrada autorizada.
- P30 hace verificable la tabla del ciclo de vida.

P31 y P32 son los dos negativos materiales que pidió la primera auditoría; P33, el que pidió la reauditoría. P32 protege los artefactos del cierre de B1-FREEZE; P33, la monotonía de la transición de gobierno.

## 2. Gate sucesor de B2

### 2.1 Sucesión

| Etapa | Gate sobre HEAD | Evidencia histórica anclada |
|---|---|---|
| B1 auditada | `validate_f35sbxb.py` | — |
| B1-FREEZE | `validate_f35sbxb_freeze.py` | Gate de B1 sobre `8e94a60` |
| B2 (diseño) | Sin gate ejecutable propio. La regla FRZ del validador de B1-FREEZE acredita la integridad del conjunto auditado de B1; sus reglas de rama y alcance fallan por diseño en la rama de B2 (§3) | Gate de B1 sobre `8e94a60` y validador del cierre sobre `3d9b783` |
| B2 (implementación, ahora) | `validate_f35sbxb2.py`, en la rama de B2, `develop` y `main` (§5) | Igual |

Los gates anteriores no se modifican. Sobre HEAD de B2 fallan por su alcance fijo (clase A de B0), así que no se usan como gate de HEAD. Se ejecutan anclados, en un clon limpio sin remoto, como evidencia del estado histórico que acreditan. Ese procedimiento es parte de la auditoría, no del gate.

### 2.2 Reglas

Ubicación: `docs/academico/tools/f35sbxb2/validate_f35sbxb2.py`. Solo biblioteca estándar, sin red, aislado (`python -I`, al que se relanza solo) y con fallo cerrado ante cualquier error o estado no evaluable.

| ID | Comprueba | Cómo |
|---|---|---|
| CTX | Contexto | Rama `feature/f35-sbx-b2-ephemeral-store`, `develop` o `main`. Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. E, el cierre de B0, el ancla de B1, el cierre de B1 y la base de B2 (`72e86c5`) son ancestros de HEAD. Historia no superficial |
| B1F | B1 histórica íntegra | §2.3 |
| AIN, B0F, HST | A idéntica a E; B0 idéntico a su cierre; ningún commit que toque A | Reglas del gate de B1, cargado desde bytes verificados contra el ancla, sin releer el archivo (principio F de B0 y Q5) |
| SBX | SBX-01..SBX-18 recalculados sobre HEAD | Maquinaria DH-B13 del gate de B1, con su inventario transitivo verificado antes de ejecutar nada |
| SCP | Delta exacto de B2 | Árbol de HEAD, árbol de trabajo, índice y archivos sin seguimiento frente a `72e86c5`: exactamente la lista enumerada de §2.5, con su estado. No hay excepción general (Q2) |
| FSY | Runtime, dataset y evidencia intactos | Superficies byte a byte iguales a la base, como en B1, y carpetas de B2 con su lista exacta. Sin enlaces, archivos ignorados extra ni `__pycache__` no derivable |
| FLG | Índice sin flags | Solo `H` en `git ls-files -v` |
| DEP | Solo biblioteca estándar | Almacén: `sqlite3`, `csv`, `hashlib`, `json`, `re`, `unicodedata` y `os`, este último solo con `os.path.join`, `os.path.dirname` y `os.path.abspath`. Gate: las del gate de B1. `sqlite3` solo en `sbxb_store.py`. Sin importaciones dinámicas |
| PRE | Entorno compatible | Los requisitos del preflight (§4.3 del diseño): SQLite 3.37 o posterior realmente cargado, API presentes y PRAGMA efectivos. Si no se cumplen, falla cerrado antes de DYN |
| STA | Almacén correcto antes de ejecutarlo | AST y catálogo (§2.4) |
| DYN | Pruebas P01..P33 | Ejecución en proceso desde bytes verificados, con la guarda de §2.4 |
| DET | Determinismo | P11 y P22 |
| ISO | Aislamiento por tenant | P03, P04, P05, P14 y P23 |
| PUR | Semántica de purga | P12, P13 y P24 |
| DAT | Solo contenido sintético autorizado | P15, P16, P28, P29 y P31 |
| CAP | Sin capacidades prohibidas | P17 y P18, más CNT sobre los documentos de B2 con las reglas semánticas de B1 |
| GOV | Gobierno | Los trece estados exactos y la transición única de gobierno de B2 (§2.3) |

| Requisito del encargo | Reglas |
|---|---|
| B1-FREEZE histórico válido | B1F |
| Delta de B2 exacto | SCP |
| Solo biblioteca estándar y sin dependencias nuevas | DEP y FSY |
| `sqlite3` solo `:memory:` y sin archivos de base de datos | STA, PRE, DYN (P01, P08) |
| Sin runtime productivo, endpoints, migraciones, PostgreSQL ni Redis | SCP, FSY y STA (P20) |
| Sin `ATTACH` | STA y DYN (P07, P27) |
| Sin alcance C, scoring, recomendación ni selección | CAP y DAT |
| Solo sintético | DAT |
| Aislamiento por tenant | ISO |
| Semántica de purga | PUR |
| Determinismo | DET |
| Fallo cerrado | Todas; P21 y P30 |

### 2.3 B1F: B1 sigue íntegra

B1F protege dos conjuntos, cada uno desde su ancla. No reduce la frontera histórica de B1 al cierre.

**A) Conjunto auditado de B1**, con ancla `8e94a60274fe39ebda3e9961bc58036b389dfc00`. Son las cinco rutas que B1 cambió respecto de su base: `CLAUDE.md`, `docs/PROGRESS.md`, `evidencia-sbx-b/README.md`, `evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md` y `tools/f35sbxb/validate_f35sbxb.py`.

- **Valores protegidos.** Modo, tipo y blob de cada ruta, tomados del árbol del ancla.
- **Historia.** En cada commit de `git rev-list --ancestry-path 8e94a60..HEAD`, merges incluidos, cada ruta tiene un blob admitido. Así se detectan modificar y restaurar, renombrar, eliminar y los cambios de modo o de tipo. Los merges legítimos pasan, como en B1-FREEZE.
- **Blobs admitidos.** Para las tres rutas que no son de gobierno, solo el blob del ancla. Para `CLAUDE.md` y `docs/PROGRESS.md`, los de la transición monotónica de gobierno, que dependen de la ascendencia de cada commit (ver «Transición de gobierno de B2»).
- **Estado efectivo.** En el árbol de HEAD, en el índice (etapa 0, sin flags) y en el disco (archivo regular, sin enlaces, con sus bytes), el blob admitido vigente.

**B) Conjunto del cierre de B1-FREEZE**, con referencia `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`. Son los tres archivos que introdujo el cierre: `validate_f35sbxb_freeze.py`, `b1_freeze_manifest.json` y `F35SBXB_B1_Freeze.md`.

- **Valores protegidos.** Modo, tipo y blob exactos del commit de cierre.
- **Historia.** Desde su introducción: en cada commit de `git rev-list --ancestry-path 3d9b783..HEAD`, el mismo blob. Antes del cierre no existían, así que su protección empieza ahí. Modificar y restaurar se detecta (P32), igual que eliminar, renombrar y cambiar el modo o el tipo.
- **Estado efectivo.** Árbol de HEAD, índice y disco iguales al cierre.

**C) Carpetas.** Las de B1 (`evidencia-sbx-b/`, `tools/f35sbxb/`) y las de B1-FREEZE (`evidencia-sbx-b-freeze/`, `tools/f35sbxb_freeze/`) con su contenido exacto.

**Transición de gobierno de B2 (DH-B2-07, Q1).** Para `CLAUDE.md` y `docs/PROGRESS.md` se distinguen tres cosas:

| Concepto | Qué es |
|---|---|
| `HISTORICAL_B1_BLOB` | Blob de cada ruta en el ancla `8e94a60`. Es la historia válida de B1 y nunca se presenta como incorrecta |
| `B2_GOVERNANCE_BLOB` | Blob nuevo autorizado por B2. El delta es una lista cerrada de reemplazos literales (bloque antiguo → bloque nuevo) sobre el contenido del ancla, cada bloque antiguo presente exactamente una vez; está enumerado en §5.2. El gate calcula los bytes esperados aplicándolos al blob histórico |
| `B2_GOVERNANCE_TRANSITION` | Commit que introduce, en las dos rutas a la vez, el paso `HISTORICAL_B1_BLOB` → `B2_GOVERNANCE_BLOB`. Se registra en §5.2 y en el gate después de que exista, nunca en el propio commit |

La transición se identifica sin hashes inventados:

- **Derivación.** El gate la deriva de la historia: es el único commit de `git rev-list --ancestry-path 8e94a60..HEAD` que contiene el blob nuevo en las dos rutas sin que ninguno de sus padres lo contenga.
- **Registro posterior.** Cuando exista, el contrato o el cierre del incremento sucesor la registrará explícitamente, después de que exista, nunca en el propio commit. Desde entonces el gate exige que la transición derivada coincida con la registrada.

Para cada commit `C` de `git rev-list --ancestry-path 8e94a60..HEAD`, merges incluidos:

1. **Antes de la transición, o si `C` no desciende de ella**, `C` contiene `HISTORICAL_B1_BLOB`. Una rama legítima creada antes de la transición puede seguir con el blob histórico mientras no desciende de la transición. Nunca puede tener un tercer blob.
2. **En la transición**, que debe ser un commit con un solo padre, el padre contiene `HISTORICAL_B1_BLOB` y el commit contiene `B2_GOVERNANCE_BLOB` en las dos rutas. En esas rutas el único cambio es ese.
3. **En todo descendiente de la transición**, determinado con `git merge-base --is-ancestor`, `C` contiene `B2_GOVERNANCE_BLOB`. Un merge `--no-ff` legítimo, como el de la rama de B2 en `develop` y el de `develop` en `main`, desciende de la transición y lleva el blob nuevo: pasa. Un merge que reintroduce el blob histórico en su resultado falla.
4. **Introducción única.** Ningún otro commit puede introducir el blob nuevo, es decir, contenerlo sin que lo contenga alguno de sus padres. La secuencia histórico → nuevo → histórico → nuevo falla dos veces: por el descendiente que vuelve al blob histórico (regla 3) y por la segunda introducción (regla 4). También fallan modificar y restaurar, y cualquier tercer blob, aunque HEAD termine en el blob nuevo (P33).

No existe ninguna regla que acepte indistintamente el blob histórico o el nuevo en un commit intermedio. Lo que vale en cada commit depende solo de su ascendencia respecto de la transición. Una transición de gobierno distinta en el futuro solo podrá autorizarla otro incremento sucesor, con su propio contrato y su propia ancla.

El contenido histórico de B1 sigue siendo verificable: es el blob de `8e94a60` en Git, no se reescribe, y es la entrada de la función que da el blob nuevo. Quedan separadas tres cosas: la historia válida de B1, la transición autorizada de B2 y el estado posterior obligatorio de B2.

Desde la transición, el validador de B1-FREEZE falla en FRZ sobre HEAD, como prevé su propio documento (§4 del cierre), y pasa a ejecutarse anclado sobre `3d9b783`.

### 2.4 Almacén: verificación antes de ejecutar

Antes de importar cualquier módulo de B2, el gate lo analiza por AST sobre los bytes leídos:

- **Conexión.** `sqlite3.connect` aparece una sola vez, con la constante `':memory:'` y sin `uri`.
- **Métodos prohibidos.** Ni `backup`, `serialize`, `deserialize`, `iterdump`, `enable_load_extension` ni `load_extension`.
- **Sentencias.** Cada `execute` y `executemany` recibe como primer argumento una entrada del catálogo (un nombre o un subíndice con clave literal), nunca una expresión. `executescript` solo recibe la constante del DDL, en el preflight.
- **Catálogo de ejecución.** Sin `REPLACE`, `OR REPLACE`, `OR IGNORE`, `ON CONFLICT`, `UPDATE`, `DELETE`, `ATTACH`, `DETACH` ni `PRAGMA`, salvo la lectura de `database_list`. Los `PRAGMA` del preflight son una lista enumerada aparte. Toda escritura comprueba `rowcount == 1`. El DDL coincide con el esquema que el gate construye por su cuenta (doble llave, P28).
- **Lectura de archivos.** `open` solo con las cuatro rutas fijas de F34 en modo `rb`; ninguna escritura de archivos.
- **Importaciones.** Ni `time`, `datetime`, `random`, `uuid`, `secrets`, `socket`, `urllib`, `http` ni `subprocess`. De `os`, solo `os.path.join`, `os.path.dirname` y `os.path.abspath`.
- **Referencias.** Ninguna a `app/`, `database/`, `routes/`, `artisan`, `.env`, `pgsql`, `postgres` ni `redis`.
- **API.** Ninguna función acepta SQL, fragmentos, nombres de tabla ni política de conflicto, y no existe una API de `PRAGMA`. Ningún nombre interno del almacén se usa fuera de él.
- **Estado del módulo.** Ninguna conexión ni almacén a nivel de módulo.

Solo si todo pasa, el gate ejecuta el módulo desde esos mismos bytes en memoria. Lo hace con una guarda como la de B1.4, que solo admite la biblioteca estándar y ese módulo, y dentro de un directorio de trabajo temporal recorrido antes y después (P08).

**Arranque y confianza (Q6).**

- **Durante el desarrollo de B2.** Las pruebas se hacen en ciclos RED/GREEN, con temporales aislados. El código de B2 es explícitamente NO AUDITADO, y un PASS de desarrollo no equivale a confianza ni a cierre.
- **Antes del cierre.** Se fija el commit que se propone cerrar, que pasa por auditoría independiente, correcciones y freeze. Tras el cierre, el sucesor compara el código de B2 con su commit de cierre.

### 2.5 Delta autorizado de B2 respecto de `72e86c5`

Rutas exactas del incremento sucesor; no hay excepción general a SCP ni a FSY (Q2).

| Ruta | Estado | Cuándo |
|---|---|---|
| `docs/academico/evidencia-sbx-b2/README.md` | A | Diseño |
| `docs/academico/evidencia-sbx-b2/F35SBXB_B2_Diseno_Almacen.md` | A | Diseño |
| `docs/academico/evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md` | A | Diseño |
| `docs/academico/tools/f35sbxb2/sbxb_store.py` | A | Implementación |
| `docs/academico/tools/f35sbxb2/validate_f35sbxb2.py` | A | Implementación (gate y casos P01..P33) |
| `CLAUDE.md`, `docs/PROGRESS.md` | M | Implementación, solo mediante la transición única y monotónica de §2.3 (Q1) |

Nada más: ni runtime, ni CI, ni dataset, ni A, ni B0, ni B1 o B1-FREEZE, ni `ACADEMIC_BASELINE.md`.

### 2.6 Qué se reutiliza del gate de B1 (Q5)

La combinación es mínima:

- **Ayudas históricas.** Las necesarias (AIN, B0F, HST, la maquinaria SBX y la semántica de afirmaciones) se cargan desde bytes verificados, con su inventario transitivo comprobado antes de ejecutar nada.
- **Reglas propias de B2.** Alcance, gobierno, almacén, dinámica, determinismo, aislamiento, purga y datos.
- **El gate de B1 no se copia ni se modifica.** Sus valores fijos (alcance, archivos de B, estados de B1) siguen siendo los de B1.

## 3. Verificación de las sesiones de diseño

**Versión 1 (`ae25e8c`).** Validación en un clon limpio sin remoto:

| Comprobación | Resultado |
|---|---|
| Validador de B1-FREEZE sobre HEAD de B2 | FRZ sin violaciones: el conjunto congelado, su historia, el índice, el disco y las carpetas de B1 siguen idénticos. SBX-01..SBX-18 en 18/18 PASS. Solo fallan CTX (la rama de B2 no está entre las tres ramas fijas de B1) y SCP (los documentos de B2 quedan fuera del alcance fijo): fallas de alcance histórico, clase A de B0 |
| Gate de B1 sobre HEAD de B2 | 157/2: solo fallan CTX y SCP, por las mismas causas |
| Regresión mínima | `validate.py` y `--cierre-f29`: 0 fallas; `validate_f29.py`: 225/0; `test_f32_safety.py`: OK; `validate_f34a.py`: 108/0 |
| Enlaces, MANIFEST y evidencias | 1094 enlaces, 0 rotos; 0 discrepancias |
| Alcance | Delta frente a `72e86c5`: exactamente los tres documentos (A). Cero archivos tocados en runtime, dependencias, CI, dataset, `ACADEMIC_BASELINE.md`, A, B0, B1, B1-FREEZE y gobierno |
| `git diff --check` | Limpio |

**Versión 2.**

Validación en un clon limpio sin remoto, con los tres documentos corregidos confirmados sobre `ae25e8c` (el mismo contenido de los commits de la corrección):

| Comprobación | Resultado |
|---|---|
| Validador de B1-FREEZE sobre HEAD de B2 | FRZ sin violaciones; SBX-01..SBX-18 en 18/18 PASS. Solo fallan CTX y SCP, como en la versión 1 |
| Gate de B1 sobre HEAD de B2 | 157/2: solo fallan CTX y SCP |
| Regresión mínima | `validate.py` y `--cierre-f29`: 0 fallas; `validate_f29.py`: 225/0; `test_f32_safety.py`: OK; `validate_f34a.py`: 108/0 |
| Enlaces, MANIFEST y evidencias | 1098 enlaces, 0 rotos (incluidos los anclajes nuevos entre los dos documentos); 0 discrepancias |
| Alcance | Delta frente a `72e86c5`: exactamente los tres documentos de B2 (A). Cero archivos tocados en runtime, dependencias, CI, dataset, `ACADEMIC_BASELINE.md`, A, B0, B1, B1-FREEZE y gobierno |
| `git diff --check` | Limpio |
| Inspección de SQLite (§16 del diseño) | Ampliada con `DO NOTHING` y las acciones que ve el autorizador, en una carpeta temporal fuera del repositorio, sin archivos creados |

## 4. Decisiones Q1–Q9

Decisiones fijadas por la auditoría independiente del diseño (versión 1).

| # | Pregunta | Decisión | Estado | Dónde |
|---|---|---|---|---|
| Q1 | Registro en el gobierno del cierre de B1 y del estado de B2 | El gobierno se actualizará únicamente en el incremento ejecutable del gate de B2, mediante una transición explícita y monotónica `HISTORICAL_B1_BLOB` → `B2_GOVERNANCE_BLOB`. El commit concreto se identificará cuando exista. Desde ese commit, ningún descendiente relevante de B2 puede volver al blob histórico ni tener otro. La evidencia histórica de B1 sigue verificable en sus anclas. Esta corrección documental no toca el gobierno | MODIFICADA Y RESUELTA | §2.3; P25 y P33; diseño §15 |
| Q2 | Rutas de B2 | `docs/academico/evidencia-sbx-b2/` y `docs/academico/tools/f35sbxb2/`, rutas exactas enumeradas por el gate; no son una excepción general a SCP ni a FSY | APROBADA | §2.5 |
| Q3 | Almacén y run | 1 tenant, 1 run o escenario y 1 conexión literal `:memory:`. Identidad alineada con B0. `tenant_context` es metadato inmutable y defensa adicional. Tener la referencia a un almacén es una frontera de confianza separada: B2 garantiza el aislamiento entre almacenes, no la autenticación ni la autorización del llamador | MODIFICADA Y RESUELTA | Diseño §2, §3 y §10 |
| Q4 | Requisitos de SQLite y Python | Preflight sin respaldo silencioso: SQLite 3.37 o posterior realmente cargado, API comprobadas directamente y no por versión, y `foreign_keys`, `recursive_triggers`, `temp_store`, `journal_mode` y el límite de bases adjuntas efectivos. Si algo no se cumple, falla cerrado. La ausencia de archivos observados no prueba la ausencia física de temporales ni de memoria paginada | MODIFICADA Y RESUELTA | Diseño §4.3; P08 |
| Q5 | Reutilización del gate de B1 | Combinación mínima: ayudas históricas desde bytes verificados, inventario transitivo previo a la ejecución y reglas propias de B2 | APROBADA | §2.6 |
| Q6 | Arranque | Durante el desarrollo, RED/GREEN, temporales aislados y código NO AUDITADO. Antes del cierre, commit propuesto, auditoría independiente, correcciones y freeze. Un PASS de desarrollo no es confianza ni cierre | APROBADA | §2.4 |
| Q7 | Evidencia atómica | Las filas de una misma operación lógica (fuente, evidencia, procedencia, marcadores, revisión simulada y, cuando la acredita, la auditoría o el evento asociado) forman una unidad. Si falla un elemento, `ROLLBACK` completo y ninguna evidencia parcial | APROBADA | Diseño §8 y §13 |
| Q8 | `fallido` | `pipeline_run` es inmutable. `fallido` es un evento de solo inserción únicamente si se confirmó. Si no, no se inventa: objeto `bloqueado`, conexión abortada y cerrada, y diagnóstico en memoria. Ninguna columna de estado mutable | MODIFICADA Y RESUELTA | Diseño §6.2; P21 y P30 |
| Q9 | Límite de recursos | Se elimina el tope numérico de 100, que no aportaba valor. Los límites salen de las entradas autorizadas: 7 estados y 8 acciones de A, y cada fila F34 autorizada a lo sumo una vez por run. No hay parámetro del llamador | MODIFICADA Y RESUELTA | Diseño §5 |

## 5. Implementación (12/10/2026)

Estado: **B2 = IMPLEMENTADA / CANDIDATA A AUDITORÍA INDEPENDIENTE**. La implementación sigue la versión 2.1 sin cambios de diseño. No se declara cerrada, integrada ni productiva, y nada de este incremento se ha publicado: la auditoría independiente, la integración y la publicación requieren autorización explícita del equipo.

### 5.1 Commits y resultados

Rama `feature/f35-sbx-b2-ephemeral-store`, desde el diseño 2.1 (`24e4ed911ca1580c5d4afeace0e97e3f515f10e8`). Ciclo RED → GREEN → refactorización → validación, en commits pequeños:

| Commit | Contenido | Resultado del gate |
|---|---|---|
| `8244bb93b214d1f87fa87f5c9fe409057fa64a64` | Gate con STA, DEP, PRE y el arnés de P01..P31, sin almacén | RED: 0 correctas, 34 fallas, código 1 (falla cerrado: almacén ausente) |
| `05c8e72c0381e60b26927b0650f425c7e89ea542` | Almacén [`sbxb_store.py`](../tools/f35sbxb2/sbxb_store.py) | GREEN: 38 correctas, 0 fallas |
| `5532eb6fb32eee639e0219c527ba25c548077d08` | P26 con y sin autorizador, `E-HASH` en P29 y NB2-01..NB2-17 | 55 correctas, 0 fallas |
| `29080755c475fad86d92b667906d7475c11b56d1` | Reglas de repositorio del [gate](../tools/f35sbxb2/validate_f35sbxb2.py), B1F con P25, P32 y P33, y NB2-18..NB2-28 | 101 correctas, 0 fallas en un clon limpio sin remoto |
| `8750e7df5d16db3c6ad89401441f40dbb4cde892` | Esta documentación de la implementación | 100 correctas y 1 falla en el árbol de trabajo local: solo FSY, por la observación O6 |
| `12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa` | Transición de gobierno (§5.2) | 101 correctas, 0 fallas en un clon limpio sin remoto, con la transición derivada de la historia |

El primer intento de GREEN falló en PRE por la observación O1 de §5.6, que se corrigió antes del commit del almacén. El commit que registra la transición es posterior y se consulta en Git.

### 5.2 Delta y transición de gobierno

| Ruta | `HISTORICAL_B1_BLOB` (ancla `8e94a60`) | `B2_GOVERNANCE_BLOB` (calculado por el gate) |
|---|---|---|
| `CLAUDE.md` | `b7068afbfac6cc2f1f39053dff8face38b894415` | `74cc4a71c56918678e0a70c7f59a3f060d87b6a0` |
| `docs/PROGRESS.md` | `983844fd2477432b2a1ea402aa8b3130678a014a` | `07889bf8c82990651539a6e4b8a1098b4bd2d35a` |

El delta es la constante `GOVERNANCE_DELTA` del gate: dos reemplazos literales en `CLAUDE.md` y cuatro en `docs/PROGRESS.md`, cada bloque antiguo presente exactamente una vez en el blob del ancla. Cambian las líneas 92 y 94 de `CLAUDE.md` y las 3, 5, 25 y 27 de `docs/PROGRESS.md`. Los trece estados de gobierno no cambian, y F35-SBX-B sigue INICIADA. Los bloques nuevos de `docs/PROGRESS.md` difieren de los de `CLAUDE.md` solo en la ruta relativa de los enlaces:

```text
CLAUDE.md, reemplazo 1
  antes:   F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) en desarrollo, sin pipeline funcional, SQLite ni ML.
  después: F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, sin pipeline funcional ni ML.

CLAUDE.md, reemplazo 2
  antes:   F35-SBX-B INICIADA en `feature/f35-sbx-b-deterministic-pipeline`; su incremento B1 (gate sucesor sobre HEAD) se entrega PENDIENTE DE AUDITORÍA.
  después: F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`](docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está IMPLEMENTADO y es CANDIDATO A AUDITORÍA INDEPENDIENTE, en `feature/f35-sbx-b2-ephemeral-store` y registrado en [`evidencia-sbx-b2`](docs/academico/evidencia-sbx-b2/README.md). Su integración y su publicación requieren autorización explícita del equipo.

docs/PROGRESS.md, reemplazo 1
  antes:   Última actualización: 2026-10-09 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA, B1 en desarrollo).
  después: Última actualización: 2026-10-12 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 IMPLEMENTADA Y CANDIDATA A AUDITORÍA INDEPENDIENTE).

docs/PROGRESS.md, reemplazo 2
  antes:   el mismo día, al inicio de F35-SBX-B con B0 cerrada e integrada.
  después: el mismo día, al inicio de F35-SBX-B con B0 cerrada e integrada. El 12/10/2026 pasó de «B1 en desarrollo» a B1 cerrada e integrada y B2 implementada, candidata a auditoría independiente.

docs/PROGRESS.md, reemplazo 3
  antes:   F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) en desarrollo, sin pipeline funcional, SQLite ni ML.
  después: F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, sin pipeline funcional ni ML.

docs/PROGRESS.md, reemplazo 4
  antes:   F35-SBX-B INICIADA en `feature/f35-sbx-b-deterministic-pipeline`; su incremento B1 (gate sucesor sobre HEAD) se entrega PENDIENTE DE AUDITORÍA.
  después: F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`](academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está IMPLEMENTADO y es CANDIDATO A AUDITORÍA INDEPENDIENTE, en `feature/f35-sbx-b2-ephemeral-store` y registrado en [`evidencia-sbx-b2`](academico/evidencia-sbx-b2/README.md). Su integración y su publicación requieren autorización explícita del equipo.
```

`B2_GOVERNANCE_TRANSITION` = `12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa`. Es el commit que introduce los dos blobs nuevos a la vez. Tiene un solo padre, `8750e7df5d16db3c6ad89401441f40dbb4cde892`, que conserva los blobs históricos, y no cambia ninguna otra ruta. Se registró después de existir, en un commit separado. Desde entonces el gate exige que la transición que deriva de la historia coincida con la registrada (NB2-28), y todo descendiente debe conservar los blobs nuevos (regla 3). Además de las reglas 1 a 4 de §2.3, el gate exige que la transición cambie solo las dos rutas de gobierno (historia F15).

### 5.3 Cómo se ejecutan las pruebas

- **Orden.** Gate de B1 desde los bytes de su ancla; `collect()` de B1 sin `__main__` registrado; estado de B2 y B1F sobre la historia real; historias desechables F01–F21; STA; PRE; DYN (P01..P31); negativos NB2.
- **Ejecución del almacén.** Desde los mismos bytes que analizó STA, sin registrarse en `sys.modules`, bajo la guarda de B1.4 y con un directorio de trabajo temporal recorrido antes y después de la batería (P08).
- **Vía interna.** Una conexión envuelta inyecta `sqlite3.Error` en sentencias concretas (P12, P21, P30). El autorizador se retira temporalmente para observar solo los triggers y el límite de bases adjuntas (P07, P09, P10, P26). Las escrituras fuera de la API usan la unidad de escritura del propio almacén (P02, P05, P26).
- **Doble llave.** El gate deriva por su cuenta, desde el contrato de A y las decisiones de B2, el `CREATE TABLE` de cada tabla, los triggers de solo inserción, de tenant y de fila única, el `table_info` y las columnas de cada `INSERT` y `SELECT`. Toma las rutas y el SHA-256 de F34 del manifiesto del dataset.
- **Procedencia (P29).** Recalcula T1, `hash_before` y `content_hash` desde las filas F34 con funciones propias, y verifica las cadenas, las relaciones y la proyección de nivel 1 frente a los fixtures de A en los tres tenants.

### 5.4 Historias desechables de B1F

Cada historia se construye en un repositorio temporal fuera del original, con la configuración de Git aislada y commits creados con plumbing sobre un índice propio. El repositorio real no se modifica.

| Historia | Qué contiene | Resultado esperado |
|---|---|---|
| F01 | Historia legítima antes de la transición | Pasa, sin transición derivada |
| F02 | Transición legítima y un descendiente | Pasa y deriva la transición |
| F03 | Transición registrada que coincide con la derivada | Pasa |
| F04 | Transición registrada distinta de la derivada | Falla |
| F05 | Manifiesto del cierre modificado y restaurado (P32) | Falla por la historia del conjunto del cierre |
| F06 | Gate de B1 modificado y restaurado | Falla por el conjunto auditado |
| F07 | Documento de B1 eliminado | Falla por el conjunto auditado |
| F08 | Documento de B1 renombrado | Falla por el conjunto auditado |
| F09 | Gate de B1 con cambio de modo | Falla por el conjunto auditado |
| F10 | Histórico, nuevo, histórico y nuevo otra vez (P33) | Falla por las reglas 3 y 4, aunque termine en el blob nuevo |
| F11 | Histórico, nuevo e histórico otra vez | Falla por la regla 3 |
| F12 | Tercer blob en el gobierno | Falla por la regla 1 |
| F13 | Transición hecha en un merge | Falla por la regla 2 |
| F14 | Transición en una sola ruta | Falla por las reglas 1 y 4 |
| F15 | Transición que cambia otras rutas | Falla |
| F16 | Rama previa a la transición fusionada con el blob nuevo | Pasa |
| F17 | Merge que reintroduce el blob histórico | Falla por la regla 3 |
| F18 | Integración `--no-ff` en `develop` y después en `main` | Pasa con la transición registrada |
| F19 | Estado efectivo limpio tras la transición | Pasa |
| F20 | Disco con el blob histórico tras la transición | Falla por el disco |
| F21 | Índice con el flag `skip-worktree` | Falla por el índice |

### 5.5 Negativos NB2

Cada negativo muta en memoria los bytes del almacén o una copia del estado del repositorio, y el gate debe detectarlo. Las mutaciones del almacén las detecta STA en su tema o, si STA no las ve, el caso DYN indicado, ejecutado con los bytes mutados. Las del repositorio las detecta su regla.

| Caso | Regla | Negativo |
|---|---|---|
| NB2-01 | STA | conexión a un archivo con URI |
| NB2-02 | STA | INSERT OR REPLACE en el catálogo |
| NB2-03 | STA | DELETE en el catálogo |
| NB2-04 | DEP | el almacén importa time |
| NB2-05 | STA | inserción sin la postcondición de una fila |
| NB2-06 | STA | SQL construido fuera del catálogo |
| NB2-07 | STA | API que acepta SQL del llamador |
| NB2-08 | STA | columna de puntaje fuera del contrato de A |
| NB2-09 | STA | conexión a nivel de módulo |
| NB2-10 | STA | apertura del origen en modo de escritura |
| NB2-11 | DYN | texto ajeno admitido sin compararlo con T1 de su fila |
| NB2-12 | DYN | autorizador que todo lo admite |
| NB2-13 | DYN | cierre excepcional sin cerrar la conexión |
| NB2-14 | DYN | filas F34 de otra organización en el índice del tenant |
| NB2-15 | DYN | purga sin cerrar la conexión |
| NB2-16 | DYN | evento fallido afirmado sin confirmarlo |
| NB2-17 | DYN | hashes aceptados sin recalcularlos |
| NB2-18 | SCP | archivo del runtime en el delta de B2 |
| NB2-19 | SCP | gobierno eliminado en el árbol de trabajo |
| NB2-20 | FSY | base de datos en archivo junto al almacén |
| NB2-21 | DEP | otro módulo del repositorio usa el almacén |
| NB2-22 | GOV | G0 real declarada APROBADA |
| NB2-23 | GOV | B2 declarada cerrada e integrada en el gobierno |
| NB2-24 | CTX | rama no permitida |
| NB2-25 | CAP | un documento de B2 afirma que el motor recomienda quién continúa |
| NB2-26 | CAP | dato personal en un documento de B2 |
| NB2-27 | GOV | F35-SBX-B declarada cerrada en el gobierno |
| NB2-28 | B1F | transición registrada distinta de la derivada |

Detectores de los negativos DYN: NB2-11 con P31, NB2-12 con P27, NB2-13 con P21, NB2-14 con P05, NB2-15 con P24, NB2-16 con P21, NB2-17 con P29.

### 5.6 Observaciones de la implementación

| # | Observación | Tratamiento |
|---|---|---|
| O1 | Un `EXISTS (SELECT 1 FROM tabla)` de un trigger llega al autorizador como lectura sin columna y con base `None`, no `main` | El autorizador admite `main` o `None` solo para las ocho tablas del esquema; crear tablas, `ATTACH` y `DETACH` siguen denegados |
| O2 | Las funciones de los `CHECK` y de los triggers (`glob` y `length`) no se notifican al autorizador | Su lista de funciones solo afecta a sentencias, y el catálogo no usa funciones |
| O3 | Con el autorizador, `DO UPDATE` falla con `DatabaseError` al preparar; sin él, con `IntegrityError` del trigger. `OR REPLACE` y `REPLACE` fallan por el trigger de borrado; `OR IGNORE` y `DO NOTHING` son silenciosos | P26 registra los dos modos, y la postcondición de una fila falla cerrada ante la forma silenciosa |
| O4 | Sin la comparación con T1 (NB2-11) o sin el filtro de tenant del índice (NB2-14), la evidencia se sigue rechazando, con `E-HASH`: el hash de contenido liga el texto y el tenant | P31 y P05 exigen `E-ORIGEN` y detectan las dos mutaciones |
| O5 | `preflight_report` sigue disponible en `purgado`, según la tabla de §6.1 del diseño, aunque P13 menciona «cualquier operación» | P13 comprueba todas las demás operaciones; el informe es una copia en memoria, sin conexión |
| O6 | En el árbol de trabajo local, FSY falla por artefactos previos (`.pyc` de pytest en `ml-service/tests` y el bundle de Vite), los mismos que ya rechazaba el gate de B1 | La validación de referencia se hace en un clon limpio sin remoto |
| O7 | El gate tarda unos 30 segundos: recálculo de SBX, 21 historias desechables y la batería DYN | Sin efecto en el resultado |
