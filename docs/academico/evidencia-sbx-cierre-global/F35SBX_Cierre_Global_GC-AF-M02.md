# F35-SBX — Cierre global: corrección GC-AF-M02

> **Estado: CORRECCIÓN IMPLEMENTADA / VALIDADA LOCALMENTE / CANDIDATA A REAUDITORÍA FOCAL.** Fecha: 25/10/2026. Rama `chore/f35-sbx-global-closure`.
>
> - Registra la corrección de GC-AF-M02 (MEDIUM), el hallazgo bloqueante de la reauditoría focal del candidato `5c9b04b30e7dd0d882c3a5eec4169d0217f73a17`, y la de GC-FIX-L01 (LOW), que la misma reauditoría registró. El candidato reauditado se conserva como ancestro visible y no se reescribe.
> - Forma parte de la capa del cierre global, junto con el [documento principal](F35SBX_Cierre_Global.md) y el [registro de GC-AF-M01](F35SBX_Cierre_Global_GC-AF-M01.md), y lo valida el mismo gate. No cambia ningún estado de gobierno: la propuesta sigue siendo F35-SBX CERRADA Y CONGELADA solo en su alcance académico y sintético.

## 1. Hallazgos

| Campo | GC-AF-M02 | GC-FIX-L01 |
|---|---|---|
| Nivel | MEDIUM, bloqueante | LOW |
| Hallazgo | Con la enumeración de `cypress/results` denegada por una ACL de NTFS (solo `ListDirectory`), el gate daba 13/0 con un archivo no autorizado dentro, legible por su ruta. Con la ACL restaurada, FSY lo rechazaba | Los recorridos heredados podían enumerar el destino externo de una unión antes de que FSY la rechazara |
| Impacto | Una superficie o una excepción que no se pudo recorrer terminaba certificada | Lectura fuera del checkout durante la verificación |

## 2. Reproducción

Sobre clones desechables, con el gate del candidato reauditado y con el corregido. El corregido se midió sobre un commit desechable con el árbol del GREEN de GC-AF-M02.

| Estado | Gate de `5c9b04b` | Gate corregido |
|---|---|---|
| Limpio | 13/0 | 13/0 |
| `cypress/results/registro_material.php`, con la carpeta enumerable | FSY: archivo no autorizado dentro de la excepción | FSY, con el mismo motivo |
| La misma carpeta con la enumeración denegada por una ACL de NTFS (Todos, solo `ListDirectory`). El archivo se lee por su ruta y `git status` está limpio | **13/0, código 0: falso PASS** | FSY y SBX, código 1: «carpeta no enumerable (PermissionError)» |
| ACL restaurada | FSY | FSY |
| `cypress/results/oculto.`, carpeta con punto final creada con el prefijo `\\?\`, con un archivo. Aparece al enumerar su padre, pero su ruta normalizada falla con `FileNotFoundError` | **13/0: falso PASS** | FSY y SBX: «carpeta no enumerable (FileNotFoundError)» |
| Unión de `app/` hacia una carpeta externa con un archivo que nombra `g0-sandbox` | FSY nombra el archivo externo, y SBX-15 falla porque lo leyó | FSY y SBX, sin nombrar el archivo externo: ningún recorrido entra en el destino |

Con la ACL, el gate congelado de B2 tampoco falla en FSY: da 112/7, solo sus siete fallas históricas, con el candidato reauditado y con la corrección. Es el silencio que hereda de B1, y B2 no se modifica.

## 3. Causa raíz

- **Las excepciones.** FSY usaba el recorrido de B1, que omite `cypress/results` y `recruitment_ml.egg-info` y deja su revisión a `exception_problems()`. Esa función recorre con `os.walk` sin `onerror`: un error de enumeración no deja rastro y la excepción queda «limpia».
- **La búsqueda de uniones** del propio gate (`junctions()`) también capturaba `OSError` y seguía.
- **Los recorridos heredados siguen las uniones.** Python no trata las uniones de directorio de Windows como enlaces simbólicos, así que el recorrido de B1 en FSY y el de F34E en SBX-15 entran en su destino antes de que FSY rechace la unión. SBX-15, además, lee el contenido: con una unión hacia una carpeta externa cuyo archivo nombra `g0-sandbox`, el gate reauditado falla en SBX-15 por ese archivo externo. GC-FIX-L01 es, por tanto, una lectura real fuera del checkout, no solo una enumeración.
- **B2.** El gate congelado de B2 hereda el mismo silencio: con la ACL, su FSY tampoco falla. No se modifica, porque es una capa congelada.

## 4. Diseño de la corrección

- **Recorrido físico previo.** Antes de cualquier recorrido heredado, FSY enumera con `os.scandir` todas las carpetas de las superficies de B1, también las excepciones y las cachés de Python. Lee los metadatos de cada entrada sin seguir nada (`lstat` y `DirEntry.stat(follow_symlinks=False)`). Señala sin entrar en ellos los enlaces simbólicos, las uniones de directorio y cualquier otro punto de reanálisis de NTFS. Todo `OSError` al leer metadatos o al enumerar una carpeta es un problema, sea `PermissionError`, `FileNotFoundError` u otro: lo no verificado nunca cuenta como limpio.
- **Nada heredado sobre lo no verificado.** Si ese recorrido encuentra algo, FSY falla con esos problemas y no ejecuta el recorrido de B1 ni su revisión de las excepciones. SBX falla cerrado sin ejecutar `compute_sbx()` de F34E, cuyo SBX-15 recorre y lee el runtime. Así ningún recorrido entra en el destino de una unión (GC-FIX-L01).
- **Lo legítimo no cambia.** Con el recorrido previo limpio, FSY sigue como en GC-AF-M01: las mismas superficies, excepciones de metadatos, `.pyc` derivables e inventario. Una carpeta vacía y los archivos ignorados fuera de las superficies siguen sin fallar.
- **Lecturas.** Un archivo del inventario que no se puede leer falla como antes, y el mensaje dice ahora «bytes físicos ilegibles o distintos».
- **La capa.** Este registro es su quinto archivo, así que la capa se completa en el commit GREEN de GC-AF-M02, que FRZ informa. `5c9b04b` queda en la historia como candidato reauditado y no aprobado.
- **Lo que no cambia.** Ninguna capa congelada (tampoco B1, B2 ni F34E), ni el runtime, el dataset, el CI, las dependencias ni el gobierno. El gate sigue teniendo 13 reglas y solo usa la biblioteca estándar.

## 5. Pruebas

| Caso | Escenario | Reglas en falla |
|---|---|---|
| GC42 (reforzado) | Unión de directorio vacía en `app/` | FSY y, ahora, SBX |
| GC44 | Archivo PHP no autorizado en `cypress/results`, con la enumeración denegada (en Windows, ACL de NTFS; fuera, permisos) y legible por su ruta | FSY y SBX |
| GC45 | `recruitment_ml.egg-info` con la enumeración denegada, aunque solo contenga un `PKG-INFO` | FSY y SBX |
| GC46 | Unión hacia una carpeta externa con un archivo que nombra `g0-sandbox`: ninguna línea FALLA lo nombra | FSY y SBX |
| GC47 | Carpeta de `app/` con la enumeración denegada y un archivo, excluida | FSY y SBX |
| GC48 | Estado legítimo: carpeta vacía, metadatos de Cypress y de `pip -e`, `.pyc` derivable y archivos ignorados fuera de las superficies | Ninguna (PASS) |
| GC49 | Carpeta con punto final en `cypress/results`, con un archivo: en Windows su enumeración falla con `FileNotFoundError`, un error que no es de permisos | FSY y SBX en Windows; FSY fuera de Windows |

Los casos de permisos usan el sistema de archivos real, en Windows y fuera de él, y comprueban antes que la enumeración falla de verdad y que el archivo sigue legible. Si no se reproduce, el caso falla como escenario no reproducido. No hay inyección: el gate se ejecuta aislado (`python -I`) y no tiene ningún punto de entrada para simular errores. El error que no es de permisos (GC49) solo se reproduce en Windows; fuera, el caso comprueba la otra vía.

| Medida | Resultado |
|---|---|
| RED focal: la batería del commit RED de GC-AF-M02 contra el gate de `5c9b04b` | 1 de 7 casos correctos. GC44, GC45 y GC49 dan PASS: el falso PASS. GC42 y GC47 no cierran SBX. En GC46, SBX falla porque SBX-15 leyó el archivo externo. Solo pasa GC48, el positivo |
| Gate, sobre un commit desechable hijo de `59d80f8` con el árbol del GREEN de GC-AF-M02 | 13/0 en unos cinco segundos. El recorrido previo, medido aparte, tarda unos 0,01 s |
| Casos focales: GC01, GC36, GC37, GC40..GC49 | 13/13 en 62 s |
| Batería completa, una sola vez | 49/49, con 50 ejecuciones del gate en 304 s |
| Controles de mutación de la corrección | 7 de 7 detectados (N01..N07), con el control sin mutar en verde. M16 se repitió con su sentencia nueva y también se detecta. Detalle en el documento principal, §5.5 |
| Reproducción del hallazgo | La de §2: el falso PASS de `5c9b04b` pasa a FSY y SBX |

### 5.1 Sondas en Windows

Fuera de la batería, con permisos, rutas y uniones reales de NTFS, sobre el mismo commit desechable y con el gate completo. Cada sonda restaura sus ACL y se deshace sin `git clean`, y el clon queda limpio; al final, el gate vuelve a dar 13/0. «Git» es lo que muestra `git status`, también con `--ignored`.

| # | Sonda | Git | Gate |
|---|---|---|---|
| T01 | Reproducción del auditor: `cypress/results` con la enumeración denegada; el archivo se lee por su ruta | No lo ve | FSY y SBX |
| T02 | La misma carpeta, enumerable | Ignorado | FSY: archivo no autorizado |
| T03..T07 | Enumeración denegada en `recruitment_ml.egg-info`, en una subcarpeta de `cypress/results`, en una carpeta excluida de `routes/`, en la caché `__pycache__` de `ml-service/src` y en una carpeta excluida del dataset | No los ve | FSY y SBX |
| T08 | Enumeración denegada en la carpeta versionada `app/Policies` | No lo ve | FSY y SBX |
| T09 | Lectura denegada en el archivo versionado `routes/web.php` | No lo ve | FSY: bytes ilegibles |
| T10 | Lectura denegada en un metadato legítimo, `cypress/results/run.json` | Ignorado | Sin falla (§6, GC-M02-H3) |
| T11 | Carpeta con punto final en `app/` | No la ve | FSY y SBX: `FileNotFoundError` |
| T12 | Archivo con punto final en `app/` | Sin seguimiento | ALC, FSY y SBX |
| T13 | Ruta de 299 caracteres en `cypress/results` | No la ve | FSY y SBX |
| T14 | Unión de `app/` hacia una carpeta externa con `g0-sandbox` | Ignorada | FSY y SBX, sin nombrar el archivo externo |
| T15 | Unión dentro de `cypress/results` | Ignorada | FSY y SBX |
| T16 | Unión cíclica de `app/` hacia sí misma | Ignorada | FSY y SBX, en 1,1 s |
| T17 | Enlace simbólico de archivo en `recruitment_ml.egg-info` | Ignorado | FSY y SBX |
| T18 | La raíz `lang/` sustituida por una unión hacia una copia idéntica | No la ve | FSY y SBX |
| T19 | Carpeta vacía de `app/` con la enumeración denegada | No la ve | FSY y SBX: no se puede saber que está vacía (§6, GC-M02-H4) |
| T20 | Carpetas sin enumeración fuera de las superficies, en `storage/logs/` y en `vendor/` | No las ve | Sin falla |
| T21 | Estados legítimos: carpeta vacía, metadatos de Cypress y de `pip -e`, `.pyc` derivable e ignorados fuera de las superficies | Ignorados | Sin falla |

Ningún estado que no se pudo verificar da PASS. Ningún estado legítimo, ni ninguna carpeta inaccesible fuera de las superficies, da FAIL. Cuando el recorrido previo encuentra algo, el gate tarda 1,1 s, porque no ejecuta los recorridos heredados ni SBX.

## 6. Autoauditoría

| # | Nivel | Hallazgo | Tratamiento |
|---|---|---|---|
| GC-AF-M02 | MEDIUM | Reauditoría de `5c9b04b`: una superficie o una excepción cuya enumeración falla terminaba certificada | Corregido con el recorrido físico previo, que falla cerrado (GC44, GC45, GC47 y GC49; N01..N04; T01..T08, T11, T13 y T19) |
| GC-FIX-L01 | LOW | Reauditoría de `5c9b04b`: los recorridos heredados entraban en el destino externo de una unión, y SBX-15 llegaba a leerlo | Corregido: el recorrido previo señala la unión sin entrar en ella, y ni los recorridos heredados de FSY ni SBX se ejecutan sobre una superficie sin verificar (GC42 y GC46; N05..N07; T14..T18) |
| GC-M02-H1 | INFO | El gate congelado de B2 calla el mismo error de enumeración: con la ACL, su FSY no falla | Capa congelada: no se modifica. Sobre HEAD decide el gate sucesor, que falla cerrado |
| GC-M02-H2 | INFO | Cualquier unión, enlace o carpeta que no se puede enumerar hace fallar también SBX | Fallo cerrado deliberado: SBX-15 recorrería y leería esa superficie con el código de F34E, que sigue las uniones y calla los errores |
| GC-M02-H3 | INFO | Un metadato legítimo de `cypress/results` con la lectura denegada no falla (T10) | La excepción de B1 se define por nombre y tipo, no por contenido, y nada del runtime lee esos metadatos. Su carpeta sí tiene que poder enumerarse |
| GC-M02-H4 | INFO | Una carpeta vacía que no se puede enumerar falla (T19) | No es un falso FAIL: no se puede saber que está vacía. Una carpeta vacía enumerable no falla (GC48 y T21) |
| GC-M02-H5 | INFO | Entre el recorrido previo y los heredados pasan unos segundos: un permiso cambiado o una unión creada en ese intervalo no se verían | Exige modificar el checkout mientras el gate corre, igual que cambiar un archivo después de ejecutarlo. Queda fuera del modelo de amenazas: el gate certifica un clon limpio |
| GC-M02-H6 | INFO | El error que no es de permisos (GC49) solo se reproduce en Windows; fuera, GC49 comprueba la otra vía | El proyecto y su auditoría trabajan en Windows, y el gate trata igual cualquier `OSError`: N03 lo demuestra |
| GC-M02-H7 | INFO | SBX-15, con el código de F34E, salta en silencio un archivo del runtime que no puede leer (T09) | FSY lo rechaza por sus bytes ilegibles, así que el gate falla. F34E es una capa congelada |
| GC-M02-H8 | INFO | INT detecta las uniones con `os.path.isjunction`, que existe desde Python 3.12; el recorrido previo usa los atributos de NTFS y no depende de la versión | El gate se ejecuta con Python 3.12.5. INT no cambia, porque está acreditada |

No queda ningún hallazgo BLOCKER, HIGH ni MEDIUM abierto.
