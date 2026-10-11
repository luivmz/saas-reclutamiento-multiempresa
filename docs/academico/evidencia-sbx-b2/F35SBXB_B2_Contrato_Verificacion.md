# F35-SBX-B — B2: contrato de verificación

> Incremento B2 de F35-SBX-B, versión 1 de diseño (11/10/2026). Estado: **B2 = DISEÑADA / PENDIENTE DE AUDITORÍA DE DISEÑO**. Define las pruebas y el gate sucesor que la implementación de B2 tendrá que cumplir. Nada de esto es ejecutable todavía. El diseño que se verifica está en [F35SBXB_B2_Diseno_Almacen.md](F35SBXB_B2_Diseno_Almacen.md).

## 1. Matriz de pruebas

Cada prueba vivirá dentro del gate de B2, como en A y en B1, sin `tests/` productivos. Usará el almacén cargado desde los bytes que el gate ya verificó (§2.4) y fixtures pequeños derivados de los de A. Una prueba que no se pueda ejecutar cuenta como fallo.

| ID | Qué demuestra | Procedimiento | Resultado esperado | Regla | Origen |
|---|---|---|---|---|---|
| P01 | El almacén usa `:memory:` | `PRAGMA database_list` del almacén abierto; análisis estático de `connect` | Solo `main` (y `temp`) sin ruta; `connect` solo con la constante `':memory:'` | STA, DYN | DH-B07 |
| P02 | FK activas | `PRAGMA foreign_keys` tras abrir; insertar una evidencia con fuente inexistente | `1`; la inserción falla con `E-SQLITE` | DYN | B0 §5.4 |
| P03 | El tenant A no ve los datos del tenant B | Dos almacenes, ORG-S1 y ORG-S2, con datos distintos; listar desde cada uno | Cada uno devuelve solo lo suyo; ningún identificador del otro tenant | DYN, ISO | DH-B08; TSBB-02 |
| P04 | Conexiones independientes | Comparar las conexiones internas de dos almacenes; purgar uno y consultar el otro | Objetos distintos, cada uno con su propia base | DYN, ISO | DH-B2-02 |
| P05 | Tenant obligatorio antes de escribir | Abrir sin tenant o con uno inválido; escribir una fila con otra organización | `E-TENANT` en la API, y también en el trigger cuando se omite la API | DYN, ISO | DH-B08 |
| P06 | Valores siempre como parámetros | AST: cada `execute` recibe una entrada del catálogo y una tupla; escribir un texto sintético con comillas y `;` | Ninguna concatenación ni formato en SQL; el texto se guarda literal y no ejecuta nada | STA, DYN | B0 §5.4 |
| P07 | `ATTACH` no expuesto | AST: ni `ATTACH` ni `DETACH` en el catálogo; en ejecución, `ATTACH` por la vía interna | Ausentes; si se intenta, falla por el límite de bases adjuntas y por el autorizador | STA, DYN | B0 §5.4 |
| P08 | No se crea ningún archivo SQLite | Recorrer el repositorio y un directorio de trabajo temporal antes y después de toda la batería | Ningún archivo nuevo (`.db`, `-journal`, `-wal` ni otro) | DYN | TSBB-08 |
| P09 | `pipeline_run` inmutable | `UPDATE` y `DELETE` sobre el principal por la vía interna; segundo `create_run` | Fallan; un único principal, sin cambios | DYN | F33 §6 |
| P10 | Eventos de solo inserción | `UPDATE` y `DELETE` sobre `pipeline_event`; evento con `seq` no contiguo; evento después de un estado terminal | Todo falla; la secuencia sigue intacta | DYN | TSBB-04 y TSBB-05 |
| P11 | Orden determinista | Insertar en un orden y listar; dos ejecuciones del mismo guion | Listas en orden de `seq` u ordinal; `snapshot()` idéntico byte a byte | STA, DYN, DET | TSBB-12 |
| P12 | La purga cierra la conexión | `purge` en estado activo y en estado finalizado | Comprobante con `post_close_check = ProgrammingError` y `file_backed = false`; estado `purgado` | DYN, PUR | DH-B06 |
| P13 | La conexión purgada es inutilizable | Cualquier operación de la API, y una consulta interna, tras `purge` | `E-PURGADO`; la consulta interna lanza `ProgrammingError` | DYN, PUR | B0 §5.3 |
| P14 | El tenant B sigue funcionando tras purgar A | Purgar ORG-S1 y operar con ORG-S2 | ORG-S2 intacto y operativo | DYN, ISO | DH-B08 |
| P15 | Entrada sintética admitida | Las evidencias de los fixtures de A, con sus marcadores | Se registran; `content_hash` coincide con el de A (nivel 1 de DH-B05) | DYN, DAT | DH-B05 |
| P16 | Dato real o prohibido rechazado | Variantes con un correo, un DNI, un teléfono, una URL, base64, `cv`, sin marcador o con marcado | `E-PROHIBIDO` y run `fallido` | DYN, DAT | TSBB-01 y TSBB-13 |
| P17 | Sin puntaje, recomendación ni selección | Esquema y API sin esos campos; una carga útil con `score` o `selected` | Columnas ausentes; `E-CONTRATO` | STA, DYN, CAP | Contratos 2 y 4 |
| P18 | Sin alcance C | Esquema sin OCR, *parsing*, embeddings ni búsqueda semántica; `evidence_kind = documento` | Ausentes; `E-PROHIBIDO` | STA, DYN, CAP | SBX-17 |
| P19 | Sin dependencias nuevas | AST de los módulos de B2; archivos de dependencias del proyecto | Solo la biblioteca estándar autorizada; `sqlite3` solo en el almacén; archivos de dependencias sin cambios | DEP, FSY | TSBB-09 |
| P20 | Sin runtime productivo | Delta y superficies del runtime; referencias a `app/`, `database/`, `routes/`, `.env`, PostgreSQL o Redis | Sin cambios ni referencias | SCP, FSY, STA | SBX-15 y SBX-16 |
| P21 | Un error de SQLite falla cerrado | Inyectar un `sqlite3.Error` en cada escritura | `E-SQLITE`, run `fallido` y ningún resultado parcial | DYN | DH-B10; TSBB-11 |
| P22 | Identificadores y tiempo deterministas | Dos almacenes con el mismo guion; un instante anterior a `clock_start` o al previo | Mismos identificadores, hashes y comprobante; el instante inválido da `E-CONTRATO`; sin reloj del sistema (AST) | STA, DYN, DET | B0 §5.2 |
| P23 | Ninguna conexión compartida entre tenants | AST: sin conexión ni almacén a nivel de módulo; en ejecución, cada almacén tiene su conexión | Ninguna variable global de conexión ni registro por organización | STA, ISO | DH-B2-02 |
| P24 | La purga no es un `DELETE` | AST: sin `DELETE` en el catálogo ni en `purge`; tras purgar, la conexión está cerrada | Sin `DELETE`; conexión cerrada | STA, PUR | DH-B06 |
| P25 | B1-FREEZE sigue íntegro | Regla B1F (§2.3) sobre HEAD | B1 idéntica al ancla y al cierre | B1F | B1-FREEZE |
| P26 | `REPLACE`, `OR IGNORE` y `ON CONFLICT` no eluden la solo inserción | Por la vía interna, `INSERT OR REPLACE`, `REPLACE INTO`, `INSERT OR IGNORE` y un *upsert* sobre filas existentes | Todos fallan; ninguna fila cambia ni desaparece; `recursive_triggers = 1` | STA, DYN | §16 del diseño: la inspección mostró la elusión |
| P27 | El autorizador niega lo que el catálogo no usa | Tras abrir: `PRAGMA foreign_keys = OFF`, `DROP TRIGGER`, `CREATE TABLE`, `load_extension`, `random()`, `datetime('now')` | Todo se niega en el motor | DYN | DH-B2-04: defensa en profundidad frente a un error del catálogo |
| P28 | Esquema cerrado e igual al contrato | Comparar `PRAGMA table_info` y el DDL con la lista independiente del gate | Igualdad exacta de tablas, columnas, tipos y restricciones | STA, DYN, DAT | Doble llave, como en A; TSBB-10 |
| P29 | Cadenas íntegras | Recalcular `event_hash`, `audit_hash` y `provenance_hash`; alterar un eslabón | Coinciden; la alteración se detecta | DYN | DH-B05, nivel 2; TSBB-03 |
| P30 | Ciclo de vida completo | Cada operación de la API en cada estado de la tabla del diseño (§6) | Lo no permitido falla con `E-CICLO` o `E-PURGADO`; tras `fallido`, sin resultado parcial | DYN | DH-B10 |

P26 a P30 se añaden con justificación propia. P26 cubre una elusión real observada en la inspección. P27 y P28 convierten en comprobaciones del motor dos controles que, si no, quedarían solo en el código. P29 verifica la integridad nativa que B0 exige. P30 hace verificable la tabla del ciclo de vida.

## 2. Gate sucesor de B2

### 2.1 Sucesión

| Etapa | Gate sobre HEAD | Evidencia histórica anclada |
|---|---|---|
| B1 auditada | `validate_f35sbxb.py` | — |
| B1-FREEZE | `validate_f35sbxb_freeze.py` | Gate de B1 sobre `8e94a60` |
| B2 (diseño, ahora) | Sin gate ejecutable propio. La regla FRZ del validador de B1-FREEZE acredita la integridad de B1; sus reglas de rama y alcance fallan por diseño en la rama de B2 (§3) | Gate de B1 sobre `8e94a60` y validador del cierre sobre `3d9b783` |
| B2 (implementación) | `validate_f35sbxb2.py`, en la rama de B2, `develop` y `main` | Igual |

Los gates anteriores no se modifican. Sobre HEAD de B2 fallan por su alcance fijo (clase A de B0), y por eso no se usan como gate de HEAD. Se ejecutan anclados, en un clon limpio sin remoto, como evidencia del estado histórico que acreditan. Ese procedimiento es parte de la auditoría, no del gate.

### 2.2 Reglas

Ubicación: `docs/academico/tools/f35sbxb2/validate_f35sbxb2.py`. Solo biblioteca estándar, sin red y aislado (`python -I`, al que se relanza solo). Cualquier error o estado no evaluable falla cerrado.

| ID | Comprueba | Cómo |
|---|---|---|
| CTX | Contexto | Rama `feature/f35-sbx-b2-ephemeral-store`, `develop` o `main`. Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. E, el cierre de B0, el ancla de B1, el cierre de B1 y la base de B2 (`72e86c5`) son ancestros de HEAD. Historia no superficial |
| B1F | B1-FREEZE histórico válido | Ver §2.3 |
| AIN, B0F, HST | A idéntica a E, B0 idéntico a su cierre e historia de A sin commits que la toquen | Reglas del gate de B1, cargado desde bytes verificados contra el ancla (principio F de B0) |
| SBX | SBX-01..SBX-18 recalculados sobre HEAD | Maquinaria DH-B13 del gate de B1, con su inventario y su verificación previa a la ejecución, cargada desde bytes verificados |
| SCP | Delta exacto de B2 | Árbol de HEAD, árbol de trabajo, índice y archivos sin seguimiento frente a `72e86c5`: exactamente la lista de §2.5, con su estado |
| FSY | Runtime, dataset y evidencia intactos | Superficies byte a byte iguales a la base, como en B1, y carpetas de B2 con su lista exacta. Sin enlaces, archivos ignorados extra ni `__pycache__` no derivable |
| FLG | Índice sin flags | Solo `H` en `git ls-files -v` |
| DEP | Solo biblioteca estándar | AST de los módulos de B2: `sqlite3`, `hashlib`, `json`, `re` y `unicodedata` en el almacén; en el gate, las del gate de B1. `sqlite3` solo en `sbxb_store.py`. Sin importaciones dinámicas |
| STA | Almacén correcto antes de ejecutarlo | AST y catálogo; ver §2.4 |
| DYN | Pruebas P01..P30 | Ejecución en proceso, desde bytes verificados, con la guarda de §2.4 |
| DET | Determinismo | P11 y P22: dos ejecuciones del mismo guion dan `snapshot()` y comprobantes idénticos byte a byte |
| ISO | Aislamiento por tenant | P03, P04, P05, P14 y P23 |
| PUR | Semántica de purga | P12, P13 y P24 |
| DAT | Solo datos sintéticos | P15, P16 y P28, más el vocabulario prohibido en el esquema y en la API |
| CAP | Sin capacidades prohibidas | P17 y P18, más CNT sobre los documentos de B2 con las reglas semánticas de B1 |
| GOV | Gobierno | Los trece estados exactos. Si se aprueba DH-B2-07, `CLAUDE.md` y `docs/PROGRESS.md` deben ser el contenido del ancla más exactamente el bloque de gobierno autorizado de B2, sin ningún otro cambio |

| Requisito del encargo | Reglas |
|---|---|
| B1-FREEZE histórico válido | B1F |
| Delta de B2 exacto | SCP |
| Solo biblioteca estándar y sin dependencias nuevas | DEP y FSY |
| `sqlite3` solo `:memory:` y sin archivos de base de datos | STA, DYN (P01, P08) |
| Sin runtime productivo, endpoints, migraciones, PostgreSQL ni Redis | SCP, FSY, STA (P20) |
| Sin `ATTACH` | STA, DYN (P07, P27) |
| Sin alcance C, scoring, recomendación ni selección | CAP y DAT |
| Solo sintético | DAT |
| Aislamiento por tenant | ISO |
| Semántica de purga | PUR |
| Determinismo | DET |
| Fallo cerrado | Todas; P21 y P30 |

### 2.3 B1F: B1 sigue íntegra

1. **Archivos del cierre.** El validador, el manifiesto y el documento de B1-FREEZE son idénticos a sus blobs en `3d9b783`.
2. **Artefactos inmutables de B1.** El gate de B1, el documento de B1 y el README de `evidencia-sbx-b/` son idénticos a sus blobs en el ancla `8e94a60` en el árbol de HEAD, en el índice y en el disco. Además, en cada commit de `git rev-list --ancestry-path 3d9b783..HEAD`, es decir, la misma regla de contenido del cierre de B1, que deja pasar los merges legítimos.
3. **Gobierno.** `CLAUDE.md` y `docs/PROGRESS.md` deben ser idénticos al ancla mientras no se apruebe DH-B2-07. Con DH-B2-07, deben ser el ancla más exactamente el bloque autorizado de B2, comprobado por GOV.
4. **Carpetas.** Las de B1 y de B1-FREEZE con su contenido exacto, como en el cierre.

Mientras el gobierno no cambie, el gate puede delegar los puntos 2 a 4 en la regla FRZ del validador de B1-FREEZE, cargado desde sus bytes verificados contra `3d9b783`.

### 2.4 Almacén: verificación estática antes de ejecutar

Antes de importar cualquier módulo de B2, el gate lo analiza por AST sobre los bytes leídos:

- **Conexión.** `sqlite3.connect` aparece una sola vez, con la constante `':memory:'` y sin `uri`.
- **Métodos prohibidos.** Ni `backup`, `serialize`, `deserialize`, `iterdump`, `enable_load_extension` ni `load_extension`.
- **Sentencias.** Cada `execute` y `executemany` recibe como primer argumento una entrada del catálogo (un nombre o un subíndice con clave literal), nunca una expresión. `executescript` solo recibe la constante del DDL.
- **Catálogo.** Sin `OR REPLACE`, `REPLACE INTO`, `OR IGNORE`, `ON CONFLICT`, `UPDATE`, `DELETE`, `ATTACH`, `DETACH` ni `PRAGMA` fuera de la lista de configuración. El DDL coincide con el esquema que el gate construye por su cuenta (doble llave, P28).
- **Importaciones.** Ni `time`, `datetime`, `random`, `uuid`, `secrets`, `os`, `socket`, `urllib`, `http` ni `subprocess`.
- **Referencias.** Ninguna a `app/`, `database/`, `routes/`, `artisan`, `.env`, `pgsql`, `postgres` ni `redis`.
- **Estado del módulo.** Ninguna conexión ni almacén a nivel de módulo, y ningún nombre interno del almacén usado fuera de él.

Solo si todo pasa, el gate ejecuta el módulo desde esos mismos bytes en memoria. Lo hace con una guarda como la de B1.4, que solo admite la biblioteca estándar y ese módulo, y dentro de un directorio de trabajo temporal recorrido antes y después (P08).

Mientras B2 está en desarrollo, su código no tiene una referencia externa contra la que compararse. Lo acredita la auditoría, igual que el gate de B1 en su etapa de desarrollo. Tras el cierre de B2, el sucesor lo comparará con el commit de cierre.

### 2.5 Delta autorizado de B2 respecto de `72e86c5`

| Ruta | Estado | Cuándo |
|---|---|---|
| `docs/academico/evidencia-sbx-b2/README.md` | A | Diseño (esta sesión) |
| `docs/academico/evidencia-sbx-b2/F35SBXB_B2_Diseno_Almacen.md` | A | Diseño |
| `docs/academico/evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md` | A | Diseño |
| `docs/academico/tools/f35sbxb2/sbxb_store.py` | A | Implementación |
| `docs/academico/tools/f35sbxb2/validate_f35sbxb2.py` | A | Implementación (gate y casos P01..P30) |
| `CLAUDE.md`, `docs/PROGRESS.md` | M | Implementación, solo si se aprueba DH-B2-07 |

Nada más: ni runtime, ni CI, ni dataset, ni A, ni B0, ni B1 o B1-FREEZE, ni `ACADEMIC_BASELINE.md`.

### 2.6 Qué no se copia del gate de B1

- **Se reutilizan**, verificadas antes de ejecutarse, las reglas cuyo objeto no cambia: AIN, B0F, HST, la maquinaria SBX y la semántica de afirmaciones.
- **Son propios de B2:** el alcance (SCP), las carpetas, los estados de gobierno admitidos para B1 y B2, el objetivo de CNT (los documentos de B2), DEP con `sqlite3` y las reglas del almacén (STA, DYN, DET, ISO, PUR y DAT).
- **El gate de B1 no se modifica.** Sus valores fijos (alcance, archivos de B, estados de B1) siguen siendo los de B1.

## 3. Verificación de esta sesión de diseño

Validación en un clon limpio sin remoto, con los tres documentos confirmados sobre `72e86c5` (el mismo contenido de los commits de esta sesión):

| Comprobación | Resultado |
|---|---|
| Validador de B1-FREEZE sobre HEAD de B2 | FRZ sin violaciones: el conjunto congelado, su historia, el índice, el disco y las carpetas de B1 siguen idénticos. SBX-01..SBX-18 en 18/18 PASS. Solo fallan CTX, porque la rama de B2 no está entre las tres ramas fijas de B1, y SCP, porque los documentos de B2 quedan fuera del alcance fijo. Son fallas de alcance histórico (clase A de B0) |
| Gate de B1 sobre HEAD de B2 | 157/2: solo fallan CTX y SCP, por las mismas causas |
| Regresión mínima | `validate.py` y `--cierre-f29`: 0 fallas; `validate_f29.py`: 225/0; `test_f32_safety.py`: OK; `validate_f34a.py`: 108/0 |
| Enlaces, MANIFEST y evidencias | 1094 enlaces, 0 rotos; 0 discrepancias |
| Alcance | Delta frente a `72e86c5`: exactamente los tres documentos (A). Cero archivos tocados en runtime, dependencias, CI, dataset, `ACADEMIC_BASELINE.md`, A, B0, B1, B1-FREEZE y gobierno |
| `git diff --check` | Limpio |
| Inspección de SQLite (§16 del diseño) | Hecha en una carpeta temporal fuera del repositorio, sin archivos creados |

Las dos fallas de alcance confirman la necesidad del gate propio de B2. Hasta que exista, la integridad de B1 sobre esta rama se lee en la regla FRZ del validador de B1-FREEZE.

## 4. Preguntas abiertas para la auditoría

| # | Pregunta | Propuesta del diseño |
|---|---|---|
| Q1 | ¿Cuándo se registra en el gobierno el cierre de B1 y el estado de B2? Hoy `CLAUDE.md` y `docs/PROGRESS.md` (en `develop` y `main`) todavía dicen que B1 está pendiente de auditoría, porque son parte del conjunto congelado | En el incremento que introduce el gate de B2 (DH-B2-07), con la regla GOV. No en el diseño |
| Q2 | ¿Se aceptan rutas nuevas para B2 frente a DH-B03, que asignaba `tools/f35sbxb/` a todo B? | Sí (DH-B2-01): las carpetas de B1 quedan exactas y FRZ sigue sirviendo |
| Q3 | ¿Un run por almacén, y la semilla fuera de los identificadores? | Sí (DH-B2-02 y DH-B2-06): basta para DH-B08 y para el determinismo. La semilla queda como campo del principal |
| Q4 | ¿Es aceptable exigir SQLite 3.37 o posterior, por `STRICT`? En macOS, la versión depende del Python instalado | Sí, con fallo cerrado si no se cumple y la versión registrada en el informe |
| Q5 | ¿El gate de B2 reutiliza código del gate de B1 cargado desde bytes verificados, o reimplementa esas reglas? | Reutilizar, como prevé el principio F de B0, y solo en las reglas cuyo objeto no cambia |
| Q6 | ¿Es suficiente la verificación estática más la carga desde bytes en memoria para ejecutar el almacén mientras B2 está en desarrollo? | Sí, con la auditoría como acreditación y la comparación con el cierre de B2 después |
| Q7 | ¿Se registra la evidencia como un paquete atómico (fuente, evidencia, revisión y procedencia en una transacción)? | Sí: así las FK son inmediatas. Los instantes lógicos conservan el orden de los pasos de A |
| Q8 | ¿Un fallo solo como evento `fallido` con código, sin acción de auditoría propia, dado que el enum de A no tiene una? | Sí: no se amplía el enum de A |
| Q9 | ¿El tope de 100 evidencias por run? | Límite de recursos propuesto; A usa dos por tenant |
