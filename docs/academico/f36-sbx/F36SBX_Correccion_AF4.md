# F36-SBX — Corrección AF4 (cuarta auditoría independiente)

> Fase F36-SBX, corrección focal del 27/10/2026, en la rama `feature/f36-sbx-authorization-design`, sobre el candidato auditado `57efbfce6a76437510782e22fc7bb9f50184bfa2`. Candidata a una **quinta auditoría independiente**. **AF4-M01, AF4-M02 y AF4-L01 corregidos por implementación, pendientes de quinta auditoría independiente.** Este documento no los declara cerrados: los cierra, o no, esa auditoría.

## 1. Veredicto recibido

La cuarta auditoría independiente del candidato `57efbfc` concluyó **no aprobado para integración**, con 0 BLOCKER, 0 HIGH, 2 MEDIUM correctivos y 1 LOW. Este registro transcribe lo comunicado; el informe de la auditoría no forma parte del repositorio.

| ID | Severidad | Hallazgo |
|---|---|---|
| AF4-M01 | MEDIUM | Las marcas del índice ocultaban modificaciones posteriores. Con un ADR versionado y modificado, marcado `assume-unchanged` o `skip-worktree`, el validador daba 56/0 y exit 0, y también con una ruta productiva modificada y marcada. Sin las marcas, la sustitución fallaba |
| AF4-M02 | MEDIUM | `refs/replace` falseaba la pertenencia al `candidate_commit`. Con una ref de reemplazo creada solo en un clon, un candidato sin ADR parecía contenerlo y el validador daba 56/0, aunque `git --no-replace-objects cat-file -e <candidato>:<ADR>` devolvía 128 |
| AF4-L01 | LOW | Seguían aceptándose identidades genéricas compuestas, como «Auditor placeholder», «auditor sin nombre» o «revisor desconocido». Las variantes simples ya se rechazaban |

## 2. Reproducción independiente sobre `57efbfc`

Antes de cambiar nada se reprodujeron los hallazgos sin depender de los archivos de la auditoría:

- AF4-M01 y AF4-M02, con Git real, en un clon local desechable del HEAD exacto y con evidencia sintética de FG-03 y FG-12;
- AF4-L01, en memoria.

Las seis variantes materiales fueron falsos PASS.

| # | Ataque | En `57efbfc` | En este candidato |
|---|---|---|---|
| 1 | Control positivo: ADR versionado en el candidato | 56/0 | 58/0 (AF4-M01-1) |
| 2 | ADR modificado, sin marcas | Falla (54/2) | Falla (AF4-M01-2) |
| 3 | ADR modificado y marcado `assume-unchanged` | Falso PASS (56/0) | Falla (AF4-M01-3) |
| 4 | ADR modificado y marcado `skip-worktree` | Falso PASS (56/0) | Falla (AF4-M01-4) |
| 5 | `routes/web.php` modificado y marcado `assume-unchanged` | Falso PASS (56/0) | Falla (AF4-M01-5) |
| 6 | `routes/web.php` modificado y marcado `skip-worktree` | Falso PASS (56/0) | Falla (reproducción; en la batería, AF4-M01-6 con `composer.json` y AF4-M01-A6) |
| 7 | `refs/replace`: el commit anterior al candidato, sin ADR, sustituido por uno con ADR, y evidencia que cita el SHA original | Falso PASS (56/0); `git --no-replace-objects cat-file -e` = 128 | Falla (AF4-M02-2) |
| 8 | Auditor «Auditor placeholder», «auditor sin nombre» o «revisor desconocido» | Válido | Falla (AF4-L01-01..03) |

## 3. Corrección de AF4-M01: integridad del árbol de trabajo sin marcas ni caché

**Causa raíz.** El alcance (regla FRZ) y el vínculo con el candidato ([gate, sección 9](F36SBX_Gate_Sucesor.md#9-vínculo-con-el-candidato-auditado)) se calculaban con `git diff --name-only <commit>` y `git ls-files --others`. `git diff` no lee los archivos marcados `assume-unchanged` o `skip-worktree`, sino que da por buena su entrada del índice. Tampoco relee un archivo cuyo stat coincide con el guardado, y aplica los filtros locales. Así, una vista local del índice decidía si una superficie protegida había cambiado.

**Corrección.**

1. `worktree_state()` lee el índice con `git ls-files -s -v`: marcas, etapas, modos y objetos. Calcula el identificador de objeto de cada archivo versionado del árbol de trabajo **a partir de sus bytes**: no usa el stat guardado, no atiende a las marcas y no ejecuta filtros.
   - Solo tolera la conversión LF→CRLF completa de un checkout (`core.autocrlf`, `eol=crlf`). Cualquier otra diferencia, aunque sea de un solo fin de línea, es un cambio.
   - Compara también el bit de ejecución donde Git lo compara: con `core.fileMode` y fuera de Windows.
2. `changed_since(commit)` une tres vistas independientes de las marcas:
   - el árbol del commit frente al índice (objetos);
   - el árbol de trabajo frente al índice (bytes);
   - los archivos sin versionar que Git no ignora.

   Alimenta la regla FRZ y el vínculo con el candidato.
3. **Falla cerrado**, en FRZ y en el vínculo con el candidato, ante:
   - cualquier marca `assume-unchanged` o `skip-worktree`, aunque el archivo esté intacto;
   - entradas sin fusionar, submódulos o modos no verificables y entradas cuyo objeto no existe;
   - archivos versionados ilegibles o un índice ilegible;
   - operaciones de Git en curso: fusión, cherry-pick, revert, rebase, am y bisect.
4. **El validador no cambia el checkout.** No retira marcas ni escribe el índice. Ya no ejecuta `git diff`, que con su refresco automático reescribía el índice: W18 y AF4-M01-A13 lo comprueban.

**Pruebas con Git real** ([`test_f36sbx_git.py`](../tools/f36sbx/test_f36sbx_git.py)):

- **Exigidas por la auditoría:**
  - AF4-M01-1: ADR normal, control positivo;
  - AF4-M01-2: ADR modificado sin marcas;
  - AF4-M01-3 y AF4-M01-4: ADR modificado y marcado `assume-unchanged` o `skip-worktree`;
  - AF4-M01-5: `routes/web.php` modificado y marcado `assume-unchanged`;
  - AF4-M01-6: `composer.json` modificado y marcado `skip-worktree`;
  - AF4-M01-7: entradas sin fusionar.
- **Ataques propios:**
  - A1: fusión en curso; A2: índice ilegible; A3: marca sin cambio;
  - A4: matriz del paquete modificada y marcada `skip-worktree`;
  - A5: cambio del mismo tamaño con la fecha restaurada, sin marcas;
  - A6: `skip-worktree` y archivo borrado;
  - A7: filtro *clean* local que oculta el cambio a Git;
  - A10: un solo fin de línea CRLF;
  - A11: documento del paquete sacado del índice e ignorado localmente;
  - A12: evidencia registrada en un commit y cambiada con `assume-unchanged`;
  - A13: el validador no escribe el índice.
- **Controles positivos:** A8 (marcas puestas y retiradas) y A9 (conversión CRLF completa).
- **Unitarias:** W01..W19.

En los casos con marca, filtro o stat engañado, `git status` sin opciones no muestra el cambio (consta en el detalle de cada caso), y aun así el validador falla.

## 4. Corrección de AF4-M02: objetos reales, sin `refs/replace`

**Causa raíz.** Git sustituye de forma transparente todo objeto que tenga una ref en `refs/replace/`. Las consultas normativas del validador (`cat-file`, `ls-tree`, `merge-base`, `show` y `diff`) observaban el objeto sustituto. Así, un commit sin ADR podía «contenerlo», y también cambiar de padres o de fecha. Proteger solo `git_blob()` no habría bastado.

**Corrección.**

1. **Una sola vía hacia Git.** `git_run()` es la única llamada a `subprocess` del validador; AF4-10 lo comprueba sobre el código.
   - Antepone `--no-replace-objects`, `--no-optional-locks`, `-c core.commitGraph=false`, `-c core.fsmonitor=false` y `-c core.untrackedCache=false`.
   - Usa un entorno sin ninguna variable `GIT_*` heredada (`GIT_DIR`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_REPLACE_REF_BASE`…), con `GIT_NO_REPLACE_OBJECTS=1` y `GIT_OPTIONAL_LOCKS=0`.
2. **El commit es el real.** `git_commit()` lee el commit y comprueba que el SHA-1 de sus bytes es el SHA citado. Una etiqueta que apunta a un commit, y que Git desreferencia, no es un commit. La fecha es la del committer en su propia zona horaria, como `%cs`.
3. **Todo se lee de objetos reales:** ancestros, árbol, blobs, documentos de la base y del candidato, y cambios.
4. **Falla cerrado si hay `refs/replace`.** No cambian lo que lee el validador, pero sí lo que ve quien revisa con Git sin opciones, y esa ambigüedad no se acepta. Lo mismo vale para los injertos (`info/grafts`), que Git aplica incluso con `--no-replace-objects`.
5. Un error de Git sigue siendo un fallo cerrado. Un objeto real que no se puede resolver no es un commit, ni un blob, ni un ancestro.

**Pruebas con Git real:**

- **Exigidas por la auditoría:**
  - AF4-M02-1: control positivo;
  - AF4-M02-2: la reproducción, una ref que introduce un ADR ausente;
  - AF4-M02-3 y AF4-M02-3b: una ref que altera un commit o un blob que ya existen;
  - AF4-M02-4a..4c: las funciones de commit, ancestros, fecha, cambios, documento del gate y blob frente a sustitutos;
  - AF4-M02-5: un SHA inexistente con una ref de reemplazo a su nombre.
- **Ataques propios:**
  - A1: injertos;
  - A2: ref ajena al candidato;
  - A3: entorno hostil, control positivo;
  - A4: control positivo tras retirar refs e injertos.
- **Unitarias:** RP01..RP07, incluida la paridad de la fecha con `%cs` en tres zonas horarias.

En cada caso, Git sin opciones ve el objeto sustituto (consta en el detalle) y el validador ve el real.

## 5. Corrección de AF4-L01: identidades genéricas compuestas

**Causa raíz.** El rechazo comparaba la identidad entera con una lista de marcadores, o exigía que todas sus palabras fueran genéricas. Un marcador («placeholder», «desconocido») junto a un rol escapaba a las dos reglas.

**Corrección.** Una identidad tiene que contener al menos una palabra distintiva. Primero se normaliza: mayúsculas, tildes, formas de compatibilidad NFKD (como las letras de ancho completo) y camelCase. Después se clasifica cada palabra. **No es distintiva** si es:

- un número o una inicial;
- un rol o un tratamiento;
- una palabra funcional;
- un marcador de hueco o de identidad ausente o ficticia;
- un relleno de una letra repetida;
- una palabra con dígitos en lugar de letras, como «pl4ceh0lder»;
- una unión sin separadores de roles y marcadores, como «auditorplaceholder».

Además, una palabra que mezcla letras latinas con cirílicas o griegas (un homógrafo) se rechaza. No es una lista de cadenas, sino una regla de composición sobre un vocabulario de palabras sin valor identificativo. Los nombres legítimos que solo contienen alguna de esas palabras siguen siendo válidos: «Ezio Auditore», «Nil Puig», «Ana Test» o «Revisor externo Pérez».

**Pruebas** ([`test_f36sbx.py`](../tools/f36sbx/test_f36sbx.py)):

- AF4-L01-01..03: las tres reproducciones, también registradas en el repositorio;
- AF4-L01-04..29: variantes y ataques propios, entre ellos AF4-L01-28, un homógrafo cirílico;
- AF4-L01-P1 y AF4-L01-P2: controles positivos.

P-07 cambia un control: «Revisora Externa Ficticia», dos roles y un marcador sin nombre propio, pasa a rechazarse (AF4-L01-25). P-07 usa ahora «Revisora Externa Ficticia Quispe».

**Límite.** Sigue siendo una validación estructural de una identidad declarada, no una autenticación.

## 6. Revisión del oracle y hallazgos propios

Se revisaron todos los helpers Git del validador:

| Pieza | Antes | Ahora |
|---|---|---|
| `git()`, `git_bytes()` y `git_ignored()` | `subprocess` directo, con la vista habitual de Git | `git_run()` |
| Existencia y tipo del candidato | `cat-file -t` | `git_commit()`: el objeto real, con su SHA-1 verificado |
| Fecha del candidato | `show -s --format=%cs` | El committer del objeto real |
| Ancestros | `merge-base` | `merge-base` sobre objetos reales y sin grafo de commits; los injertos se rechazan |
| Cambios posteriores a la base y al candidato | `git diff --name-only` y `ls-files --others` | `changed_since()` |
| ADR y documento del gate del candidato | `git_blob()` | `git_blob()` por `git_run()` |
| Gobierno de la base | `git show BASE:ruta` | `git_blob()` del objeto real |

La revisión encontró además cinco defectos, corregidos en AF4. Los numera este documento, no la auditoría:

| ID | Severidad | Defecto | Corrección y pruebas |
|---|---|---|---|
| AF4-PR01 | MEDIUM | Una entrada normativa sacada del índice e ignorada localmente se leía del árbol de trabajo sin figurar en ningún cambio. Podía ser un documento del paquete, del gobierno, una herramienta o una fuente F34. El validador validaba así un paquete que ningún commit contiene | FRZ exige que Git no ignore ninguna entrada leída del árbol de trabajo (AF4-06..08 y AF4-M01-A11) |
| AF4-PR02 | MEDIUM | Los injertos (`info/grafts`) cambian los ancestros incluso con `--no-replace-objects` | Fallo cerrado (RP07 y AF4-M02-A1) |
| AF4-PR03 | MEDIUM | Sin ninguna marca, un cambio del mismo tamaño con la fecha restaurada, o un filtro *clean* local, ocultaban el cambio a `git diff` | Integridad por bytes (W06, AF4-M01-A5 y AF4-M01-A7) |
| AF4-PR04 | LOW | Las variables `GIT_*` del entorno, como `GIT_DIR` o `GIT_INDEX_FILE`, podían dirigir el validador a otro repositorio o a otro índice | Entorno saneado (AF4-11, W16 y AF4-M02-A3) |
| AF4-PR05 | LOW | `git diff` reescribía el índice con su refresco automático, así que el validador no era de solo lectura | Sin `git diff` (W18 y AF4-M01-A13) |

## 7. Pruebas y metapruebas

| Herramienta | Resultado | Cambio |
|---|---|---|
| `validate_f36sbx.py` | 58/0 | Dos comprobaciones FRZ nuevas: estado Git fiable y entradas versionables |
| `test_f36sbx.py` | 510/0 | 43 casos nuevos |
| `test_f36sbx_git.py` | 89/0 | 58 casos nuevos |

[`meta_f36sbx.py`](../tools/f36sbx/meta_f36sbx.py) suma 24 ablaciones de código y 10 de función. Las piezas de la vista de Git solo se prueban contra la batería con Git real, que es la única que las ejercita. El nuevo filtro `meta_f36sbx.py ablaciones <subcadena,…>` permite ejecuciones focales.

### 7.1 Ejecución focal de ablaciones

PENDIENTE: se registra al terminar la ejecución.

## 8. Límites

- **Fin de línea.** Solo se tolera la conversión CRLF completa de un checkout. Un archivo con finales mixtos es un cambio, aunque Git lo normalizaría al añadirlo.
- **Reglas de exclusión locales.** `.git/info/exclude` y `core.excludesFile` siguen decidiendo qué es un archivo sin versionar. Un archivo ignorado que no es entrada normativa no cuenta como cambio: ningún commit lo contiene sin forzarlo y el validador no lo lee.
- **Almacén de objetos.** Su integridad se presume, y la comprueba `git fsck`. El validador verifica el SHA-1 de los commits y de los blobs que lee, pero no el de los árboles. Un objeto falsificado en el almacén local y una colisión de SHA-1 quedan fuera de este oracle.
- **Defensa en profundidad sin prueba dedicada.** El grafo de commits, fsmonitor, la caché de archivos sin versionar y los bloqueos opcionales se desactivan sin una prueba propia. Ninguna orden del validador depende de ellos para decidir; W18 y AF4-M01-A13 comprueban que no escribe el índice.
- **Identidad.** La regla depende de un vocabulario. Una identidad formada solo por palabras de ese vocabulario se rechaza aunque fuera el nombre real de alguien. El validador no autentica, no comprueba independencia y no lee la prosa.

## 9. No regresión

Siguen pasando, sin cambios de criterio:

- AF3-M02, contexto canónico y REL-15: AF3-12..AF3-25, P-12..P-14 y C52..C54;
- AF3-M01, el ADR es el blob del candidato: AF3-01..AF3-11, U01..U18 y G01..G11, ahora sobre Git endurecido;
- AF3-L01: AF3-26..AF3-35 y P-08; P-07, con el cambio de la sección 5;
- AF2-M01, coherencia estructurada: AF2-01..AF2-12 y D01..D46;
- AF2-M02, hashes, sello y provenance: AF2-13..AF2-24, H01..H12 y P-01..P-04;
- AF2-M03, aislamiento entre tenants: AF2-25..AF2-30, X01..X10, P-05 y P-06;
- AF2-L01, cierre y completitud del ejemplo: AF2-31..AF2-33 y L01..L05.

El contrato (v4), el ejemplo de conformidad, el esquema de la evidencia de equipo (v2) y el formato de la evidencia no cambian.

## 10. Lo que no cambia

- **F36-SBX:** F36-SBX = EN DISEÑO y F36-SBX-GATE = NO SUPERADO. FG-02, FG-03, FG-10 y FG-12 siguen pendientes y sin evidencia registrada: la evidencia sintética de las pruebas solo existe en memoria o en clones desechables. F37-SBX = BLOQUEADA.
- **Gobierno:** G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; Alcance C = BLOQUEADO; Datos reales = PROHIBIDOS.
- **Decisiones:** RF-23 sigue siendo la decisión final humana y RF-29 sigue experimental e informativa.
- **Alcance:** no hay ML, NLP productivo, embeddings, OCR, parsing, LLM, endpoints, migraciones, UI ni dependencias nuevas. F35-SBX, F34, G0, el runtime y el gobierno global no cambian.
