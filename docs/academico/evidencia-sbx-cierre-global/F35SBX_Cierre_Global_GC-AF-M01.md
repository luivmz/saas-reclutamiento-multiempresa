# F35-SBX — Cierre global: corrección GC-AF-M01

> **Estado: CORRECCIÓN REAUDITADA — CONFIRMADA PARA LOS ARCHIVOS QUE GIT IGNORA; LA COMPLETA GC-AF-M02.** Fecha: 25/10/2026. Rama `chore/f35-sbx-global-closure`.
>
> - Registra la corrección del único hallazgo bloqueante de la auditoría independiente del candidato `9f73494033155b3e9d448cc5210b5acfbd59c475`: GC-AF-M01 (MEDIUM). El candidato auditado se conserva como ancestro visible y no se reescribe.
> - La reauditoría focal de su commit, `5c9b04b30e7dd0d882c3a5eec4169d0217f73a17`, confirmó que FSY rechaza los archivos ignorados, excluidos o con los bytes cambiados. También encontró GC-AF-M02 (MEDIUM): una excepción de B1 cuya enumeración falla terminaba certificada. Este registro se conserva como el de su momento. El [registro de GC-AF-M02](F35SBX_Cierre_Global_GC-AF-M02.md) precisa lo que aquí se dice de los errores de lectura y de las uniones.
> - Forma parte de la capa del cierre global, junto con el [documento principal](F35SBX_Cierre_Global.md), y lo valida el mismo gate. No cambia ningún estado de gobierno: la propuesta sigue siendo F35-SBX CERRADA Y CONGELADA solo en su alcance académico y sintético.

## 1. Hallazgo

| Campo | Valor |
|---|---|
| ID y nivel | GC-AF-M01, MEDIUM bloqueante |
| Candidato auditado | `9f73494033155b3e9d448cc5210b5acfbd59c475`, con el gate en 12/0 y la batería en 35/35 sobre un clon limpio |
| Hallazgo | El gate seguía dando 12/0 con un archivo físico de runtime oculto para Git por `.git/info/exclude`, y con un artefacto bajo `public/build/` que ignora `.gitignore`. El gate congelado de B2 rechaza los dos casos en su regla FSY |
| Impacto | El gate podía certificar la integridad material de un checkout con runtime adicional no autorizado |

## 2. Reproducción

En un clon desechable del candidato auditado, con el gate global y, como control, el gate congelado de B2:

| Estado | Gate global | FSY del gate de B2 |
|---|---|---|
| Limpio | 12/0 | Sin falla |
| `app/ignorado.php`, oculto por `.git/info/exclude` | 12/0: falso PASS | Falla: archivo fuera de la base autorizada «aunque Git lo ignore» |
| `public/build/assets/fixture.js`, ignorado por `.gitignore` | 12/0: falso PASS | Falla: código generado y no versionado |

Contra el gate del candidato auditado, los ocho casos nuevos de la batería (§6) también dan PASS: el defecto afecta a toda la clase de estados, no solo a esos nombres.

Con la corrección, sobre un commit desechable con el árbol del GREEN de la corrección, los dos estados del auditor y dos variantes de otro nombre, otra extensión y otra profundidad fallan en FSY, como en el FSY de B2:

| Estado | Gate global | FSY del gate de B2 |
|---|---|---|
| Limpio | 13/0 | Sin falla |
| `app/ignorado.php`, oculto por `.git/info/exclude` | FSY: fuera del inventario autorizado | Falla: fuera de la base autorizada |
| `public/build/assets/fixture.js`, ignorado por `.gitignore` | FSY: código generado | Falla: código generado |
| `app/Support/Otra/Mas/Profunda/registro.inc`, vacío y excluido | FSY: fuera del inventario autorizado | Falla: fuera de la base autorizada |
| `public/build/chunks/x/estilos.css`, ignorado por `.gitignore` | FSY: código generado | Falla: código generado |

Sobre HEAD, el gate congelado de B2 conserva en todos los estados sus siete fallas históricas de clase A (DH-B13); en los cuatro estados con un archivo extra añade la de FSY. Al deshacerlos, el gate global vuelve a dar 13/0.

## 3. Causa raíz

El gate verificaba la integridad de B por la identidad de la historia integrada y por INT, que recorre en el disco solo las carpetas de A y de B. No repetía el recorrido físico de las superficies materiales que B1 exige a la sucesión: FSY (B1, §8.3 y B1.3; TSBB-07 de B0, «artefactos ocultos: archivo extra, ignorado o enlace»).

Ninguna otra regla lo cubría:

- ALC usa `git ls-files --others --exclude-standard`, que no muestra lo que Git ignora;
- SBX-15 solo busca referencias textuales al sandbox en el runtime;
- SBX-16 compara árboles de Git con la base de F34D.

Tampoco bastaba con quitar `--exclude-standard`. Git no lista los archivos de una carpeta `.git` anidada (GC41), sigue las uniones de directorio como carpetas (GC42) y no ve un byte cambiado con el mismo tamaño y la fecha restaurada (GC43). Solo un recorrido físico, comparado con un inventario verificado, ve los tres.

El defecto está en el gate sucesor, no en las capas congeladas: el gate de B2 lo detecta.

## 4. Superficies y contrato

Se usan las superficies y las excepciones que B1 fijó y B2 heredó, sin ampliarlas ni reducirlas:

| Elemento | Contenido | Fuente |
|---|---|---|
| Superficies recorridas | `app/`, `routes/`, `database/`, `config/`, `resources/`, `bootstrap/`, `public/`, `lang/`, `tests/`, `cypress/`, `docker/`, `.github/`, `ml-service/src/`, `ml-service/tests/`, `ml-service/pyproject.toml`, `artisan`, `composer.json`, `composer.lock`, `package.json`, `package-lock.json`, `docker-compose.yml`, `.dockerignore`, `phpunit.xml`, `vite.config.ts`, `docs/academico/datos-sinteticos/`, `docs/academico/g0-sandbox/` y `docs/academico/g0-evidence/` | B1, §8.3; `RUNTIME_SURFACES` del gate de B1 |
| Fuera del recorrido | `vendor/`, `node_modules/`, `storage/`, `.git/`, `ml-service/.venv/` y `ml-service/artifacts/`, que no alteran el código versionado ni el dataset | B1, §8.3 |
| Excepciones de metadatos | `cypress/results` (solo `.json` y `.log`) y los archivos de metadatos de `ml-service/src/recruitment_ml.egg-info`, con su patrón de nombre | B1, §10.3 |
| Código generado | `public/build/`, `public/hot`, `resources/js/actions/`, `resources/js/routes/`, `resources/js/wayfinder/` y `bootstrap/cache/`: no se certifican por nombre ni extensión y fallan cerrados | B1.3 |
| Bytecode | Solo los `.pyc` derivables de su fuente hermana con el intérprete actual, en las cachés de `ml-service/src/` y `ml-service/tests/` | B1.3 |
| Enlaces | Un enlace simbólico falla en el recorrido de B1. Las uniones de directorio de Windows, que ese recorrido sigue como carpetas, se buscan aparte y fallan igual | TSBB-07 de B0: archivo extra, ignorado o enlace, FAIL |

Las carpetas de A, las de B y las de esta capa ya se recorren en el disco con INT y ALC, y las cuatro rutas de gobierno con GOV.

## 5. Diseño de la corrección

- **Una regla nueva, FSY,** en el gate del cierre global, que pasa a tener 13 reglas.
- **Recorrido físico.** Recorre el sistema de archivos real con las piezas del gate de B1, cargadas de los bytes verificados de su blob en `8e94a60`: el recorrido, sus excepciones, el código generado y los `.pyc` derivables. No depende de `git status`, de `git ls-files`, de `--exclude-standard` ni del contenido de los archivos: un archivo extra falla aunque esté vacío, oculto o anidado, con cualquier nombre o extensión. Las uniones de directorio, que Python no trata como enlaces simbólicos, se buscan aparte y sin seguirlas.
- **Inventario autorizado.** Es el árbol de esas superficies en `f082b41`, leído de objetos verificados. Debe coincidir con el de HEAD y con el de la base `430f3f5` de B1, y coincide: no hubo ningún cambio entre ellas. Ni `.gitignore` ni `.git/info/exclude` deciden qué archivo físico es legítimo.
- **Fallos.** Un archivo extra, uno generado, uno ausente, un enlace, una unión de directorio o unos bytes distintos de su blob en el inventario hacen fallar FSY, que falla cerrado ante cualquier error de lectura.
- **Excepciones.** Solo las de B1: los metadatos de `cypress/results` y de `recruitment_ml.egg-info`, con su patrón, y los `.pyc` derivables de su fuente con el intérprete que ejecuta el gate.
- **La capa.** Este registro es su cuarto archivo, así que la capa se completa en el commit GREEN de la corrección, que FRZ informa. `9f73494` queda en la historia como candidato auditado y no aprobado.
- **Lo que no cambia.** Ninguna capa congelada, ni el runtime, el dataset, el CI ni el gobierno.

## 6. Pruebas

| Caso | Escenario | Reglas en falla |
|---|---|---|
| GC36 | Archivo PHP inerte en una carpeta anidada de `app/`, oculto por `.git/info/exclude` | FSY |
| GC37 | Artefacto JavaScript en `public/build/`, ignorado por `.gitignore` | FSY |
| GC38 | Archivo CSV en el dataset sintético, oculto por `.git/info/exclude` | FSY |
| GC39 | Carpeta anidada de `routes/` con un `.gitignore` que la ignora entera, y un archivo vacío | FSY |
| GC40 | `.pyc` no derivable en una caché `__pycache__` ignorada de `ml-service/src` | FSY |
| GC41 | Archivo PHP dentro de una carpeta `.git` anidada de `app/`, que Git no lista nunca | FSY |
| GC42 | Unión de directorio vacía en `app/` hacia una carpeta externa | FSY |
| GC43 | Archivo versionado de `routes/` con un byte cambiado, el mismo tamaño y su fecha restaurada, que `git status` y `git diff` no ven | FSY |
| GC15 y GC16 | Runtime y dataset modificados y confirmados | Ahora también FSY |
| GC24 | Clon superficial | Todas salvo FLG y DEP, ahora también FSY |

GC36..GC40 se añadieron en el commit RED de la corrección, antes de implementar FSY. GC41..GC43 salieron de la autoauditoría de la defensa, antes del commit GREEN, con su RED medido igual.

| Medida | Resultado |
|---|---|
| RED, batería completa sobre el commit RED de la corrección (`395a56e`) | 7 correctos y 33 fallas, con 39 ejecuciones del gate. El gate no tenía FSY, y FRZ falla en todos los casos porque el commit cambia la capa después de `9f73494`: los siete correctos ya esperaban FRZ |
| RED focal: la batería de la corrección contra el gate de `9f73494` | GC36..GC40 dan PASS, que es el falso PASS, y GC15 y GC16 no fallan en FSY (0/7). GC41..GC43 también dan PASS (0/3) |
| Gate, sobre un commit desechable hijo de `395a56e` con el árbol del GREEN de la corrección | 13/0, en unos cinco segundos |
| Batería | 43/43, con 44 ejecuciones del gate en unos cinco minutos |
| Controles de mutación de FSY | 10 de 10 detectados, con el control sin mutar en verde. Cinco son correcciones ingenuas: solo los nombres del auditor, solo un nivel, solo PHP y JavaScript, respetar lo que Git ignora y el listado de Git sin `--exclude-standard`. Detalle en el documento principal, §5.5 |
| Control histórico | En los cuatro estados de §2, el FSY de este gate y el del gate congelado de B2 rechazan el mismo archivo |

### 6.1 Sondas de evasión

Fuera de la batería, sobre el mismo commit desechable y con el gate completo. Cada sonda se deshace sin `git clean` y el clon queda limpio; al final, el gate vuelve a dar 13/0. «Git» es lo que muestra `git status`:

| # | Sonda | Git | Gate |
|---|---|---|---|
| S01 | Reproducción del auditor: `app/ignorado.php`, oculto por `.git/info/exclude` | Ignorado | FSY |
| S02 | Reproducción del auditor: `public/build/assets/fixture.js`, ignorado por `.gitignore` | Ignorado | FSY: código generado |
| S03 | Otro nombre, a cuatro niveles en `config/`, excluido | Ignorado | FSY |
| S04 | Extensión `.tmp` en `resources/`, ignorada por un `core.excludesFile` del repositorio | Ignorado | FSY |
| S05 | Archivo oculto y vacío en `tests/`, excluido | Ignorado | FSY |
| S06 | Carpeta escrita con otra capitalización (`app/Http/controllers/`), excluida en minúsculas | Ignorado | FSY, con la ruta real `app/Http/Controllers/Extra.php` |
| S07 | `.gitignore` local con `*` en `database/factories/` y un archivo nuevo | Ignorados | FSY, con los dos archivos |
| S08..S10 | Generados e ignorados: `public/hot`, `bootstrap/cache/packages.php` y `resources/js/wayfinder/index.ts` | Ignorados | FSY: código generado |
| S11 | Archivo dentro de una carpeta `.git` anidada de `public/` | No lo ve | FSY |
| S12 | Unión de directorio en `app/` hacia una carpeta externa con un archivo, excluida | Ignorada | FSY: la unión y el archivo |
| S13 | Unión de directorio vacía en `resources/` | No la ve | FSY: la unión |
| S14 | Unión que sustituye `app/Policies` por una copia externa idéntica | No la ve | FSY: la unión y los bytes, que no se leen a través de ella |
| S15 y S16 | Enlace simbólico de directorio y de archivo en `app/`, excluidos | Ignorados | FSY: enlace |
| S17 | Unión cíclica de `app/` hacia sí misma, excluida | Ignorada | FSY, con 91 violaciones: termina en unos seis segundos y falla cerrado |
| S18 | Archivo versionado con un byte cambiado, el mismo tamaño y la fecha restaurada, con la configuración de Git por defecto | No lo ve, tampoco `git diff` | FSY: bytes distintos de su blob |
| S19 | Flujo alternativo de NTFS en `app/Models/User.php` | No lo ve | Sin falla (§7, GC-M01-H4) |
| S20 | Archivos en `storage/logs/` y en `vendor/` | Ignorados | Sin falla: fuera de las superficies (B1, §8.3) |
| S21 | Excepción de B1: un `.json` y un `.log` en `cypress/results` | Ignorados | Sin falla |
| S22 | Un `.php` en `cypress/results` | Ignorado | FSY: fuera de la excepción |
| S23 | `.pyc` derivable de su fuente con este intérprete | Ignorado | Sin falla (B1.3) |
| S24 | `.pyc` con la etiqueta de otra versión de Python | Ignorado | FSY: no derivable |
| S25 | Excepción de B1: metadatos de `pip -e` en `recruitment_ml.egg-info` | Ignorados | Sin falla |
| S26 | Un `.py` en `recruitment_ml.egg-info` | Ignorado | FSY: fuera de la excepción |
| S27 | Archivo nuevo visible para Git en `app/` | Sin seguimiento | ALC, FSY y SBX. La sonda esperaba ALC y FSY; también fallan SBX-08, SBX-09 y SBX-16, que exigen la línea base y el runtime sin cambios según Git |
| S28 | Nombre con espacios y «ñ» en `app/Support/`, excluido con un comodín | Ignorado | FSY |

Ningún estado de la clase de GC-AF-M01 da un falso PASS: la única sonda sin falla de las que Git no muestra es el flujo alternativo de NTFS, que no es un archivo de la superficie (GC-M01-H4). Ningún estado legítimo del contrato da un falso FAIL.

## 7. Autoauditoría de la defensa física

| # | Nivel | Hallazgo | Tratamiento |
|---|---|---|---|
| GC-M01-H1 | LOW | El recorrido de B1 sigue las uniones de directorio de Windows como carpetas, así que una unión vacía no le aporta ningún archivo, aunque el contrato trata los enlaces como FAIL | Corregido antes del commit GREEN: FSY busca las uniones aparte, sin seguirlas (GC42 y M23; S12..S14 y S17) |
| GC-M01-H2 | INFO | El mutante M22, en su primera forma, llamaba a `check-ignore` con las opciones de Git del gate (`--literal-pathspecs`), que ese comando no admite, así que no hacía lo que pretendía | Corregido el mutante, la batería lo detecta. No afecta al gate |
| GC-M01-H3 | INFO | La comprobación del árbol de HEAD frente al inventario se solapa con ALC, SBX y la comparación de bytes: M26 sobrevive | Defensa en profundidad: ningún estado depende solo de ella |
| GC-M01-H4 | INFO | Los flujos alternativos de NTFS no se recorren: S19 no falla, y Git tampoco los ve | No son archivos de la superficie, y nada del runtime los carga sin cambiar un archivo del inventario, que FSY sí detecta. Tampoco llegan a la imagen Docker de Linux. El recorrido de B1 trabaja igual |
| GC-M01-H5 | INFO | Una carpeta vacía y no versionada no se señala | No contiene nada que se ejecute o se importe, y Git no la representa; B1 tampoco la señala. Una unión vacía sí se señala (GC42) |
| GC-M01-H6 | INFO | FSY falla en un checkout de trabajo con artefactos de build, cachés de Laravel, `.pyc` de otra versión de Python o metadatos del sistema como `.DS_Store` | Es el contrato de B1 (§8.3 y B1.3): lo que no está en el inventario no se certifica. El gate se ejecuta en un clon limpio, como los gates de B |
| GC-M01-H7 | INFO | Lo que hay fuera de las superficies no se recorre: `vendor/`, `node_modules/`, `storage/`, `ml-service/.venv/` y `ml-service/artifacts/` (S20) | Exclusión contractual de B1, §8.3: no altera el código versionado ni el dataset |

Al cerrar esta corrección no se conocía ningún hallazgo BLOCKER, HIGH ni MEDIUM abierto. La reauditoría focal encontró después GC-AF-M02 (MEDIUM), que se trata en su registro.
