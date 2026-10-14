# F35-SBX-B — B2-FREEZE: congelación del candidato B2

> **Estado: B2-FREEZE = IMPLEMENTADO / CANDIDATO A AUDITORÍA INDEPENDIENTE.** Fecha: 13/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`.
>
> **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / APROBADA PARA FREEZE.** La reauditoría independiente final del candidato dio el veredicto «B2-IMPLEMENTATION REAUDITADA Y APROBADA PARA FREEZE»: H01, M01 y M02 resueltos y ningún hallazgo nuevo BLOCKER, HIGH ni MEDIUM. Resultados independientes informados: gate sucesor de B2 119/0, B1 anclada 159/0, B1-FREEZE 14/0, SBX 18/18, `git diff --check` limpio y F34E 247/1 (falla histórica).
>
> Este freeze protege el candidato aprobado sin modificarlo. No cierra, no integra ni publica B2: falta la auditoría independiente del freeze.

## 1. Candidato y referencias

| Referencia | Commit | Qué identifica |
|---|---|---|
| Ancla auditada de B1 | `8e94a60274fe39ebda3e9961bc58036b389dfc00` | B1 aprobada |
| Cierre de B1-FREEZE | `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` | El cierre de B1 ([B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md)) |
| Base de B2 | `72e86c5838984ea873d6dd56c179d94217b27317` | `develop` al crear la rama de B2 |
| Transición de gobierno de B2 | `12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa` | El único paso del blob histórico de B1 al blob de B2 en `CLAUDE.md` y `docs/PROGRESS.md` |
| `B2_CANDIDATE` | `2472fd6fadfc0634ec68cbcb76cfc9fbfe105194` | El contenido de B2 reauditado y aprobado para freeze. Raíz del nivel A |
| Pruebas del freeze en RED | `253145bdf6cd210f845bb11af945350fe08bedd8` | La batería de pruebas, antes de que existiera el validador |
| Commit de freeze | Se consulta en Git | El commit que completa la capa del freeze. Raíz del nivel B |
| Merge futuro en `develop` | No existe | Requiere autorización explícita del equipo |
| Merge futuro en `main` | No existe | Requiere autorización explícita del equipo |

El candidato, el commit de freeze y los dos merges futuros son commits distintos. El candidato no cambia, y el validador lo acredita aunque HEAD avance. Ningún archivo registra el hash del commit de freeze, porque sería autorreferencial: Git lo identifica como el commit que completa la capa (§7).

## 2. Conjunto congelado

El conjunto se deriva de Git y se contrasta con el contrato de B2. Son las rutas que B2 cambió respecto de su base (`git diff-tree -r --no-renames --name-status 72e86c5 2472fd6`). El validador comprueba en cada ejecución que coinciden con el alcance del [contrato, §2.5](../evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md), tal como lo fija el gate aprobado (`SCOPE2`). Esas constantes se leen por AST del blob del candidato, sin ejecutar el gate.

| Ruta | Frente a la base | Modo | Blob en el candidato | SHA-256 | Bytes |
|---|---|---|---|---|---|
| `CLAUDE.md` | M | 100644 | `74cc4a71c56918678e0a70c7f59a3f060d87b6a0` | `5bb44a43e521047d254a282f5f98b247f902ece6631d8fd5baf45c7003c440fe` | 20331 |
| `docs/PROGRESS.md` | M | 100644 | `07889bf8c82990651539a6e4b8a1098b4bd2d35a` | `cb57d277c275b8dd5192e87b30844855d03af2ee92e5c12e211d6d07a44e5fe7` | 34977 |
| `docs/academico/evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md` | A | 100644 | `54b527262cf71842d482f6c1374772a42444d2b1` | `1916a223a2d51837782f0cb8571ebb050291721a46174a9f0626ca4377b60d92` | 54474 |
| `docs/academico/evidencia-sbx-b2/F35SBXB_B2_Diseno_Almacen.md` | A | 100644 | `fb4315e20438cf1925b25867bb05e87f91b295fb` | `cf913639166c8c5015af706f5aafb28231420dcd0b2e91e288e297094ea1cf3f` | 41248 |
| `docs/academico/evidencia-sbx-b2/README.md` | A | 100644 | `21318f49fdf42627a24aa294be52a4691d36c099` | `651aa026499aa50f3d90846e829e63fb44b81b99ca8638ae606c0c99a223aa6d` | 5593 |
| `docs/academico/tools/f35sbxb2/sbxb_store.py` | A | 100644 | `09ac588eb442d80f5270e641cb98cdfe0169166c` | `0f96ed8f305d649bf906970e6b3baa179df95f373a172887e25cba2a7beb8663` | 65742 |
| `docs/academico/tools/f35sbxb2/validate_f35sbxb2.py` | A | 100644 | `c2b625a5764b6c29391b0f8eb366f6d6716e20bc` | `403b0ab06189bae334ecf3c8e811cdee611ca0cf194d7ecd98c77fd57111808b` | 158289 |

Todas son blobs regulares. La tabla reproduce el [manifiesto](../tools/f35sbxb2_freeze/b2_freeze_manifest.json), que el validador vuelve a derivar del candidato en cada ejecución.

**Inclusiones.**

- **Almacén y gate.** Son la implementación auditada. Congelar sus bytes mantiene válido para HEAD el resultado anclado del gate (119/0).
- **Los tres documentos de B2.** Definen lo que se auditó: diseño, contrato (P01..P36, Q1–Q9 y la corrección de §6) e índice.
- **`CLAUDE.md` y `docs/PROGRESS.md`.** Forman parte del delta auditado de B2, con el blob de gobierno que introdujo la transición `12c1c36`. La regla monotónica de B2 ya exige ese blob en todos los descendientes de la transición, así que congelarlo no añade una restricción nueva. Lo que cambia es que ahora la hace cumplir también este validador sobre HEAD (§9).

**Exclusiones.**

- **B1 y B1-FREEZE.** Sus conjuntos y carpetas siguen protegidos por sus propios validadores, que se ejecutan anclados. B2-FREEZE no sustituye ni reinterpreta el cierre de B1.
- **A, B0, el runtime, el dataset y el resto del repositorio.** Quedan fuera del delta de B2; incluirlos sería congelar el repositorio arbitrariamente.
- **La capa del freeze.** Tiene su propio nivel de protección, con otra ancla (§7).

**Superficies reservadas.** Son las carpetas que B2 creó: `docs/academico/evidencia-sbx-b2/` y `docs/academico/tools/f35sbxb2/`. Se derivan del delta (carpetas de las rutas añadidas que no existían en la base) y solo contienen el conjunto congelado. En la historia, en HEAD, en el índice y en el disco deben tener exactamente ese contenido, sin archivos extra, ni siquiera ignorados.

## 3. Arquitectura

| Archivo | Contenido |
|---|---|
| [`validate_f35sbxb2_freeze.py`](../tools/f35sbxb2_freeze/validate_f35sbxb2_freeze.py) | Validador: integridad Git de solo lectura y fallo cerrado. Biblioteca estándar; `subprocess` solo para Git |
| [`b2_freeze_manifest.json`](../tools/f35sbxb2_freeze/b2_freeze_manifest.json) | Manifiesto declarativo: candidato, base, anclas previas, conjunto congelado (ruta, estado, tipo, modo, blob, SHA-256 y tamaño), superficies reservadas y capa del freeze. Determinista y sin marcas de tiempo |
| [`test_f35sbxb2_freeze.py`](../tools/f35sbxb2_freeze/test_f35sbxb2_freeze.py) | Batería de 27 casos en clones desechables fuera del repositorio |
| `F35SBXB_B2_Freeze.md` | Este documento |

Uso, desde la raíz del repositorio:

- `python -I docs/academico/tools/f35sbxb2_freeze/validate_f35sbxb2_freeze.py`, que tarda menos de un segundo;
- `python -I docs/academico/tools/f35sbxb2_freeze/test_f35sbxb2_freeze.py`, que tarda alrededor de un minuto y medio.

Los dos se relanzan aislados si se invocan sin `-I`.

**Dos niveles.**

- **Nivel A** protege el candidato, con ancla `2472fd6`.
- **Nivel B** protege la capa del freeze, con ancla en el commit que la completa.

**Raíz de confianza.** La fuente de verdad del nivel A es el commit candidato, cuyo hash está fijado en el validador, y sus objetos Git. El manifiesto no lo es: es la serialización canónica de lo que se deriva del candidato y se compara byte a byte (MAN). Cada objeto que el validador lee (commits, árboles y blobs) se pide a `git cat-file --batch` con `--no-replace-objects`. Solo se acepta si el SHA-1 de su tipo, tamaño y contenido coincide con el identificador pedido: es el identificador que calcula Git, sin criptografía propia. El SHA-256 del manifiesto es un dato adicional de cada blob. La historia se recorre sobre esos commits verificados, sin `rev-list`, injertos ni objetos de reemplazo.

**Qué no hace.** No ejecuta el almacén ni el gate de B2, no abre SQLite, no usa la red y no escribe nada. Las variables `GIT_*` heredadas se descartan, para que el entorno no pueda redirigir el repositorio, el índice ni los objetos.

## 4. Reglas del validador

| ID | Nivel | Comprueba |
|---|---|---|
| ENT | A | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. Git sobre el repositorio del validador, con historia completa y sin injertos ni objetos de reemplazo |
| CAN | A | Candidato íntegro y ancestro de HEAD; base de B2 y anclas previas como ancestros del candidato; delta de Git igual al alcance del contrato; cada ruta, un blob regular 100644 cuyo estado frente a la base confirman los objetos |
| MAN | A | Manifiesto igual, byte a byte, a la serialización canónica de lo que se deriva del candidato |
| HIS | A | En cada commit posterior al candidato que lleva a HEAD, merges incluidos, rutas congeladas y superficies reservadas iguales al candidato |
| ARB | A | Árbol de HEAD igual al candidato |
| IDX | A | Índice con una entrada en etapa 0 por archivo, con el modo y el blob del candidato, y nada más en las superficies |
| FLG | A | Ningún flag en el índice de todo el repositorio: ni assume-unchanged, ni skip-worktree, ni conflictos |
| DSK | A | Disco: archivos regulares, sin enlaces ni uniones en la ruta, con los bytes del candidato y, en POSIX, sin bit de ejecución. Superficies con su contenido exacto, incluidos archivos ignorados, ocultos y `__pycache__` |
| FRZ | B | Un único commit posterior al candidato completa la capa y HEAD desciende de él. Desde él, cada commit, HEAD, el índice y el disco tienen exactamente los archivos de la capa |
| DEP | B | Los archivos Python de la capa solo importan la biblioteca estándar autorizada (`ast`, `hashlib`, `json`, `os`, `subprocess` y `sys`) y no ejecutan código dinámico |

Cada regla se evalúa por separado. Si no puede evaluarse (falta un objeto, la historia está incompleta o Git falla), falla cerrada con el motivo.

## 5. Historia y merges

La historia protegida son los commits que descienden del candidato y son ancestros de HEAD, lo mismo que daría `git rev-list --ancestry-path 2472fd6..HEAD`. Esa lista incluye los merges y se calcula sobre commits verificados. En cada uno de esos commits, las siete rutas y las dos superficies deben ser idénticas al candidato en modo, tipo y blob.

- **Modificar y restaurar, eliminar y restaurar, renombrar y restaurar, cambiar el modo y restaurar.** El commit intermedio desciende del candidato y difiere, así que el validador falla aunque HEAD termine con los bytes correctos (F03 a F06).
- **Merge legítimo.** Un merge `--no-ff` de la rama de B2 en `develop`, o de `develop` en `main`, lleva el contenido del candidato. Su otro padre no desciende del candidato y no entra en la lista. El merge pasa, y también los commits posteriores ajenos al conjunto (F15).
- **Historia lateral.** Una rama que altera y restaura una ruta congelada e integra después un merge con resultado correcto falla. Sus commits descienden del candidato y forman parte de la historia protegida (F16).
- **Historia que no corresponde.** Falla un HEAD que no desciende del candidato, aunque tenga sus bytes (F18). También falla un candidato sustituido con `git replace` (F19): el validador lee el candidato verdadero y, además, rechaza los objetos de reemplazo. Un clon superficial, en el que faltan los objetos de la historia, falla cerrado (F20).

## 6. Árbol, índice, flags y disco

Cada plano se compara por separado con el candidato, de modo que la regla que falla indica dónde está el cambio:

- **Cambio confirmado.** Fallan HIS, ARB, IDX y DSK (F02).
- **Solo en el árbol de trabajo.** Falla DSK (F07).
- **Solo en el índice.** Falla IDX (F08).
- **Cambios invisibles para `git status`.** Con assume-unchanged o skip-worktree fallan FLG y DSK (F09 y F10). Un archivo ignorado dentro de una superficie reservada hace fallar DSK (F13).
- **Objeto inesperado.** Un gitlink en el índice hace fallar IDX. Un enlace simbólico en el disco hace fallar DSK aunque entregue los bytes correctos (F17).
- **Entorno de Git hostil.** `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` apuntan a un clon limpio, de modo que Git no ve el cambio. El validador las descarta y falla en IDX (F21).

El validador no depende de `git status`: lee el índice con `git ls-files` y los bytes del disco directamente. Los artefactos ignorados del checkout del equipo (`public/build/` y `.pyc` de pytest) están fuera de las superficies de este freeze. El gate de B2 sigue fallando en FSY por ellos, igual que antes del freeze, y el checkout no se limpia para obtener un PASS.

## 7. Nivel B: autointegridad sin autorreferencia

La capa del freeze son cuatro archivos en dos carpetas propias: `tools/f35sbxb2_freeze/` (validador, manifiesto y batería) y `evidencia-sbx-b2-freeze/` (este documento).

- **Ancla derivada.** El commit de freeze es el único commit posterior al candidato que contiene la capa completa sin que la contenga ninguno de sus padres. Ningún archivo guarda su hash. Si la capa se completa en más de un commit, el validador falla. Ocurre, por ejemplo, con una capa alternativa en una rama lateral integrada con un merge que conserva la original (B05).
- **Inmutabilidad.** Desde ese commit, cada descendiente que lleva a HEAD, HEAD, el índice y el disco deben tener exactamente los archivos de la capa. Fallan modificar y confirmar el validador (B01), modificar el manifiesto en el disco (B02), modificar la evidencia solo en el índice (B03) y modificar y restaurar el validador (B04). Los merges posteriores que conservan la capa pasan (F15).
- **Límite.** Un validador modificado podría informar cualquier cosa sobre sí mismo. Por eso B01 ejecuta la copia de confianza, con los bytes del commit de freeze, y detecta la modificación en la historia y en el índice. La copia modificada falla además en DEP, porque importa `sqlite3`.
- **Confianza.** Ningún validador puede acreditarse a sí mismo. La confianza en el nivel B la aporta el registro externo del commit de freeze: la auditoría lo anota y el incremento sucesor lo registra después de que exista, como hizo B2 con su transición de gobierno.

## 8. Sucesión de gates

| Etapa | Gate sobre HEAD | Evidencia histórica anclada |
|---|---|---|
| B2 corregida (candidato `2472fd6`) | `validate_f35sbxb2.py` | Gate de B1 sobre `8e94a60` y validador de B1-FREEZE sobre `3d9b783` |
| B2-FREEZE (ahora) | `validate_f35sbxb2_freeze.py`, en la rama de B2, `develop` y `main` | Gate de B2 sobre `2472fd6`, gate de B1 sobre `8e94a60` y B1-FREEZE sobre `3d9b783` |
| Integración futura (`--no-ff`) | El mismo validador: los merges legítimos pasan (F15) | Igual |
| Incremento sucesor autorizado | Su propio gate, que registra el commit de freeze | Este validador, anclado sobre el commit de freeze |

El gate de B2 no se modifica. Sobre un HEAD posterior al candidato da 118/1: solo falla SCP, por los cuatro archivos de la capa, que quedan fuera de su delta fijo (doce violaciones: cada archivo en el árbol de HEAD, el árbol de trabajo y el índice). Es la falla de alcance histórico prevista por B0 (clase A), y no se corrige debilitando el gate. Anclado sobre el candidato, en un clon limpio, da 119/0.

El gate de B1 y el validador de B1-FREEZE fallan sobre HEAD en las mismas reglas que sobre el candidato (clase A desde la transición de gobierno). Solo crece la lista de rutas y commits: el gate de B1 da 105/54 en los dos, y el validador de B1-FREEZE 0/2.

Si un incremento posterior autorizado cambia una ruta congelada (por ejemplo, el gobierno), este validador fallará sobre ese HEAD, y debe fallar. Ese incremento aportará su propio gate sucesor y ejecutará este validador anclado sobre el commit de freeze.

## 9. Gobierno

El contrato de B2 (§2.3) solo admite una transición de gobierno, la de `12c1c36`: «Una transición de gobierno distinta en el futuro solo podrá autorizarla otro incremento sucesor, con su propio contrato y su propia ancla». Por eso este freeze no modifica `CLAUDE.md` ni `docs/PROGRESS.md`, que conservan el blob de B2 y la propiedad monotónica auditada:

> **Actualización de gobierno pendiente de incremento sucesor autorizado.**

Mientras tanto, el gobierno sigue describiendo B2 como implementada y candidata a auditoría independiente, como advirtió el riesgo R4 de la corrección de B2. El estado vigente de B2 y de este freeze se registra en este documento.

Los estados de gobierno no cambian:

- G0 real = NO APROBADA y ADR-005 = PROPUESTA;
- G0-SBX = APROBADA CON RESTRICCIONES;
- F35 productiva = BLOQUEADA y F36–F40 = BLOQUEADAS;
- Alcance C = BLOQUEADO y datos reales = PROHIBIDOS.

B2-FREEZE no introduce capacidades. No añade SQLite, red, ML, OCR, embeddings ni búsqueda semántica, y no persiste RF-29. Tampoco hay puntaje, recomendación ni selección automática, ni datos de candidatos: todo es sintético. RF-23 sigue siendo una decisión humana y RF-01..RF-27 no cambian.

## 10. Pruebas

**RED.** La batería se confirmó antes que el validador (`253145b`). Sobre ese commit dio 0 casos correctos y 24 fallas: el validador, el manifiesto y la evidencia no existían.

**GREEN.** La implementación mínima pasó los 24 casos en el primer intento.

**Casos añadidos.** Después se añadieron tres casos, cada uno por una propiedad material que ningún caso anterior ejercitaba:

- **F20.** Una historia truncada, como la de un checkout de CI con `--depth 1`, no puede ocultar un modificar y restaurar.
- **F21.** El entorno no puede redirigir el veredicto.
- **B05.** El ancla del nivel B es única.

**Controles de mutación.** Se ejecutó la batería contra un validador debilitado a propósito, en un clon desechable:

- sin el saneamiento de `GIT_*`, F21 falla;
- con la historia reducida a HEAD, fallan F03 a F06 y F16.

No hizo falta ningún endurecimiento: ningún caso material mostró una brecha.

| Caso | Escenario | Reglas en falla esperadas y observadas |
|---|---|---|
| F01 | Candidato intacto con la capa del freeze | Ninguna (PASS) |
| F02 | Archivo congelado modificado y confirmado | HIS, ARB, IDX, DSK |
| F03 | Modificar → restaurar | HIS |
| F04 | Eliminar → restaurar | HIS |
| F05 | Renombrar → restaurar | HIS |
| F06 | Cambio de modo → restauración | HIS |
| F07 | Modificación solo en el árbol de trabajo | DSK |
| F08 | Modificación solo en el índice | IDX |
| F09 | assume-unchanged con un cambio que `git status` no ve | FLG, DSK |
| F10 | skip-worktree con un cambio que `git status` no ve | FLG, DSK |
| F11 | Manifiesto que excluye una ruta congelada | MAN, FRZ |
| F12 | Blob, SHA-256 o tamaño incorrectos en el manifiesto (tres sondas) | MAN, FRZ en cada una |
| F13 | Archivo ignorado en una superficie reservada | DSK |
| F14 | Manifiesto reanclado al padre del candidato | MAN, FRZ |
| F15 | Merges `--no-ff` en `develop` y `main`, y un commit posterior (tres ejecuciones) | Ninguna (PASS) en las tres |
| F16 | Rama lateral que altera y restaura, integrada con un merge | HIS |
| F17 | Gitlink en el índice; enlace simbólico en el disco | IDX; DSK |
| F18 | Historia reescrita: el candidato no es ancestro de HEAD | CAN, HIS, FRZ |
| F19 | Candidato sustituido con `git replace` para ocultar una alteración | ENT, HIS, ARB, IDX, DSK |
| F20 | Clon superficial | ENT, CAN, MAN, HIS, ARB, IDX, DSK, FRZ (fallo cerrado) |
| F21 | `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` apuntan a un clon limpio | IDX |
| R01 | Archivo congelado y manifiesto alterados de forma coherente | MAN, HIS, ARB, IDX, DSK, FRZ |
| B01 | Validador del freeze modificado y confirmado | FRZ (copia de confianza); FRZ, DEP (copia modificada) |
| B02 | Manifiesto del freeze modificado en el disco | MAN, FRZ |
| B03 | Evidencia del freeze modificada solo en el índice | FRZ |
| B04 | Modificar → restaurar el validador del freeze | FRZ |
| B05 | Segunda capa del freeze en una rama lateral, integrada con un merge que conserva la original | FRZ |

Resultado: 27 casos correctos y 0 fallas, con 33 ejecuciones del validador. R01 demuestra que el manifiesto no puede acreditar una alteración, aunque coincida con el archivo alterado. Fallan las reglas que comparan con el candidato (HIS, ARB, IDX y DSK), además de MAN y FRZ.

## 11. Validación en clon limpio

Los resultados de esta sección se obtuvieron en clones limpios sin remoto, sobre un commit desechable con el mismo árbol que el commit de freeze. Su repetición sobre el commit de freeze real se registra en el reporte de entrega.

| Comprobación | Resultado |
|---|---|
| `validate_f35sbxb2_freeze.py` | 10/0 |
| `test_f35sbxb2_freeze.py` | 27/0, con 33 ejecuciones del validador |
| Gate de B2 anclado sobre `2472fd6` | 119/0, con la transición derivada igual a la registrada (`12c1c36`) |
| Gate de B2 sobre HEAD | 118/1: solo SCP, por la capa del freeze (§8) |
| Gate de B1 anclado sobre `8e94a60` | 159/0, con SBX-01..SBX-18 en PASS |
| Validador de B1-FREEZE anclado sobre `3d9b783` | 14/0, con SBX-01..SBX-18 en 18/18 PASS |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py` | 225/0 |
| `test_f32_safety.py` | OK |
| `validate_f33.py` | 451/0 |
| `validate_f34.py` | 403/0 |
| `validate_f34a.py` | 108/0 |
| `validate_f34e.py` | 247/1, con los criterios SBX en 18/18 |
| Enlaces relativos | 1115, 0 rotos |
| MANIFEST y evidencias de las prácticas | 61 hashes y 0 discrepancias; 0 discrepancias en las evidencias |
| `git diff --check 2472fd6..HEAD` | Limpio |
| Delta frente al candidato | Exactamente los cuatro archivos de la capa (A) |

**F34E.** Su falla es la histórica conocida. Es la misma regla (GIT) con el mismo recuento que sobre el candidato. La única diferencia es la lista de rutas F35-SBX no autorizadas por DH-02, a la que se suman los cuatro archivos de la capa (de 12 a 16), igual que antes se sumaron las rutas de B0, B1, B1-FREEZE y B2. En la sublista recortada del alcance de `validate_f34b.py`, la evidencia de este freeze desplaza por orden alfabético a una ruta de B2.

## 12. Riesgos residuales

| # | Riesgo | Tratamiento |
|---|---|---|
| R1 | El commit de freeze se deriva y no se registra en ningún archivo. Si la rama, que aún no se ha publicado, se reescribiera entera después del candidato, otra capa podría ser la única | La auditoría anota el hash del commit de freeze, y el incremento sucesor lo registra y exige que el derivado coincida |
| R2 | Un validador modificado puede declararse correcto a sí mismo | La confianza viene de ejecutar la copia con los bytes del commit de freeze registrado (B01) |
| R3 | `CLAUDE.md` y `docs/PROGRESS.md` quedan congelados con el blob de B2 | Es deliberado: cualquier cambio de gobierno pasa por un incremento sucesor autorizado (§9) |
| R4 | Los flags se comprueban en todo el repositorio y las superficies son exactas: un checkout disperso o una caché en una superficie hacen fallar el validador | Es deliberado: falla cerrado |
| R5 | Los identificadores de Git del repositorio son SHA-1 | Es el formato de objetos del repositorio. El manifiesto añade el SHA-256 de cada blob y el validador no admite otro formato |
| R6 | F17 necesita que el sistema permita crear enlaces simbólicos (en Windows, el modo de desarrollador). La batería usa clones con objetos compartidos y un temporal fuera del repositorio | Si no los permite, el caso falla cerrado con el motivo |
| R7 | El código que el intérprete ejecuta antes del validador, como el sitio de Python, queda fuera de su alcance | Igual que en B1-FREEZE: `python -I` y fallo si hay `PYTHONPATH`, `PYTHONHOME` o `PYTHONUSERBASE` |

## 13. Próximo paso

Auditoría independiente de B2-FREEZE por otro modelo. Hasta entonces:

- B2 no se declara cerrada, congelada ni integrada;
- no hay push, merge en `develop` ni en `main`, tag ni release;
- la actualización de gobierno queda pendiente de un incremento sucesor autorizado.
