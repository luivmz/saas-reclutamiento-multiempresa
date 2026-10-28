# F36-SBX — Corrección AF5 (quinta auditoría independiente)

> Fase F36-SBX, corrección focal del 27/10/2026, en la rama `feature/f36-sbx-authorization-design`, sobre el candidato auditado `8ae203ce46374aa542ef3e9dc6106dac809e9ab1`. Candidata a una **sexta auditoría independiente**. **AF5-M01 y AF5-L01 corregidos por implementación, pendientes de sexta auditoría independiente.** Este documento no los declara cerrados: los cierra, o no, esa auditoría.

## 1. Identidad y base del candidato

| Dato | Valor |
|---|---|
| Rama | `feature/f36-sbx-authorization-design` |
| Candidato auditado (AF4) | `8ae203ce46374aa542ef3e9dc6106dac809e9ab1`, árbol `8f8469a1cf9fb95ef67185cf8069b2183cae2943`, padre `d27eedd6ea3c74124ad8997d28dbd06796a80dee` |
| Base | `main` = `b8892af39a6492d8dd44a36290604efc602380cd`, ancestro del candidato |
| Commits AF5 | `7188e67` (validador), `d24a55b` (pruebas), `466264d` (metapruebas), `f266ebc` y `b2876fc` (pruebas añadidas tras la ejecución focal) y el commit de esta documentación |

El HEAD, el árbol y el padre del candidato AF5 se consultan en Git: este documento forma parte de ese commit y no puede citarlo.

**Continuidad.** Una sesión anterior empezó AF5 y se interrumpió por un límite de uso, con cambios sin confirmar en el validador, la batería y la metaprueba. Esos cambios se conservaron: se copiaron íntegros a un worktree aislado, se verificaron (59/0 y 510/0) y son la base de esta corrección. La sesión anterior había probado 28 negativos y 39 nombres plausibles de forma ad hoc; esas listas no se guardaron, así que se reconstruyeron, se ampliaron y ahora forman parte de la batería (sección 6).

## 2. Hallazgos recibidos

La quinta auditoría independiente del candidato `8ae203c` concluyó **no aprobado para integración**, con 0 BLOCKER, 0 HIGH, 1 MEDIUM correctivo y 1 LOW residual. Este registro transcribe lo comunicado; el informe de la auditoría no forma parte del repositorio.

| ID | Severidad | Hallazgo |
|---|---|---|
| AF5-M01 | MEDIUM | Contenido normativo externo no vinculado al candidato Git. En un clon Linux (WSL) se versionó el plan de evaluación como enlace simbólico a un archivo externo, en un candidato con un ADR regular y evidencia sintética de FG-03 y FG-12. Al modificar solo el archivo externo, el validador seguía dando 58/0 y exit 0 |
| AF5-L01 | LOW | Se aceptaban identidades genéricas compuestas como `tbdplaceholder`, `placeholderxx` o `auditorfictionn` |

## 3. Causas raíz

**AF5-M01.** El validador leía las entradas normativas con `Path.read_text()`, que sigue los enlaces. Git, en cambio, guarda un enlace como un blob de modo `120000` cuyo contenido es la **ruta** del destino. La integridad (AF4-M01) comparaba el índice con esa ruta (`os.readlink`), que no cambia, mientras las reglas consumían el Markdown del destino externo, que sí cambia. Se comparaban unos bytes y se consumían otros. Además, ninguna regla exigía que una entrada normativa fuera, en el commit candidato, un blob regular.

**AF5-L01.** La regla de concatenación de AF4 solo reconocía uniones de piezas fuertes de cuatro letras o más. Un marcador corto («tbd»), un relleno pegado a una pieza («xx», «n» repetida) o una palabra de ficción en inglés («fiction») dejaban la palabra sin cubrir, así que contaba como distintiva.

## 4. Soluciones implementadas

### 4.1 AF5-M01: entradas normativas regulares y ligadas al candidato

1. **Una sola lectura, sin seguir enlaces.** `read_normative()` lee cada entrada normativa (paquete, gobierno, matriz F33, fuentes F34, herramientas y evidencia) una sola vez:
   - `link_in_path()` recorre todos los componentes de la ruta desde la raíz del repositorio, incluido el último. Ninguno puede redirigir (`redirects()`): ni un enlace simbólico, ni una unión de directorios (junction), ni, en Windows, ningún otro punto de reparse.
   - El último componente tiene que ser un archivo regular. Se abre con `O_NOFOLLOW` donde existe y sin bloquearse ante una FIFO.
   - Después de leer, el descriptor abierto tiene que ser el mismo archivo inspeccionado (`st_dev`, `st_ino`) y la ruta tiene que seguir sin redirecciones. En Windows, que no tiene `O_NOFOLLOW`, un cambio entre la comprobación y la lectura falla cerrado.
   - `walk_normative()` recorre los directorios de herramientas y de evidencia sin entrar en enlaces ni uniones, y deja cada uno con su motivo.
2. **Lo comparado es lo consumido.** `worktree_state()` recibe esos mismos bytes y los compara con el objeto del índice. Una entrada normativa que es un enlace nunca coincide con su blob, aunque la ruta destino sea la del blob.
3. **Modo regular en el índice y en el candidato.** Toda entrada normativa leída tiene que ser:
   - en el índice, una entrada `100644`;
   - en el árbol del commit candidato, un blob `100644`, comprobado sobre el objeto real (`git_facts()`);
   - presente en el candidato, salvo la evidencia, que se registra después.

   La regla FRZ falla si alguna no lo es. El vínculo con el candidato ([gate §9](F36SBX_Gate_Sucesor.md#9-vínculo-con-el-candidato-auditado)) falla cerrado si la vista normativa falta, no es una lista o tiene problemas.
4. **Rutas.** `safe_repo_path()` rechaza además `:`. En Windows, `C:/x` es absoluta aunque no empiece por `/`, y `x.md:flujo` es un flujo alternativo de NTFS. Ya rechazaba `..`, componentes vacíos, barras invertidas e invisibles.
5. **Falla cerrado** ante un objeto ausente, un tipo incompatible (enlace, submódulo, árbol o ejecutable), una entrada ilegible, un árbol del candidato que Git no puede leer y una vista normativa no evaluada.

### 4.2 AF5-L01: composiciones genéricas sin separadores

`concatenated()` aplica una gramática explícita, no una lista de cadenas. Una palabra sin separadores es genérica si se puede cubrir **entera, sin ninguna letra suelta**, de una de estas dos formas:

- **Con al menos una pieza fuerte.** Una pieza fuerte es un rol o un marcador de cuatro letras o más. Se combina con pegamento (conectores, tratamientos, palabras funcionales y el resto del vocabulario de dos o tres letras) y con rellenos: una letra repetida, una «x» o «z» suelta, o una letra que repite la anterior. Así se rechazan `tbdplaceholder`, `placeholderxx`, `auditorfictionn`, `auditorsinnombre` y `drplaceholder`.
- **Solo con marcadores cortos y rellenos de «x» o «z»**, en dos piezas o más y con algún marcador de tres letras: `tbdxx`, `natbd`.

Además:

- una forma colapsada, con cada letra repetida reducida a una, se compara con las piezas fuertes colapsadas igual: `plaaceholder`, `placeholdeerr`;
- las letras latinas que NFKD no descompone se pliegan: `ı` → `i`, `ł` → `l`, `ø` → `o`… (`auditorfıctionn`);
- la frase marcadora se compara también en camelCase: `JaneDoe`;
- el vocabulario suma ficción, provisionalidad y vacío, también en inglés (`fiction`, `temp`, `blank`, `random`…), números en palabras, rellenos de teclado y los nombres de relleno `john doe`, `jane doe` y `juan nadie`.

Los tratamientos y los conectores son pegamento, nunca piezas fuertes, y ninguna pieza de una sola letra cubre nada. Por eso siguen siendo nombres:

- «Lola», que solo es pegamento;
- «Donna», sin pieza fuerte;
- «Nana», con dos marcadores de dos letras;
- «Barr» o «Doerr», un marcador corto más otra letra;
- «Testino», «Testa» o «Auditore», con letras sin cubrir;
- «Donato», donde «doña» es un tratamiento.

## 5. Garantías y limitaciones

**Garantías.**

- Lo que se valida es exactamente lo que el commit candidato fija: bytes de archivos regulares, comparados con su objeto Git, y blobs `100644` en el árbol real del candidato.
- Ningún enlace, unión ni punto de reparse, en ningún componente de la ruta, puede introducir contenido externo.
- Un enlace duro a un archivo externo no rompe la garantía: se validan sus bytes, y cualquier cambio del destino es un cambio respecto al candidato (G02 y G03).

**Limitaciones.**

- **Carrera local.** En Windows no hay `O_NOFOLLOW`. La comprobación posterior de identidad (`st_dev`, `st_ino`) y de la ruta reduce la ventana a un cambio que se deshaga entre esa comprobación y la siguiente lectura. Un atacante con acceso local concurrente al checkout queda fuera del modelo, como en AF4.
- **Puntos de reparse.** Se rechaza cualquiera, también los de un proveedor de archivos en la nube. Un checkout dentro de una carpeta sincronizada puede fallar cerrado por esa razón; se valida fuera de ella.
- **Identidad.** Sigue siendo una validación estructural de una identidad declarada, no una autenticación. Una sola palabra que coincida con un rol más una letra repetida («Stubb») se rechaza. Un nombre completo pasa si alguna de sus palabras es distintiva. La revisión humana de la identidad y de las firmas externas sigue siendo obligatoria.

## 6. Pruebas positivas y negativas

### 6.1 En memoria ([`test_f36sbx.py`](../tools/f36sbx/test_f36sbx.py))

| Casos | Qué comprueban |
|---|---|
| AF5-L01-01..03 | Reproducción de la quinta auditoría (`tbdplaceholder`, `placeholderxx`, `auditorfictionn`), en el registro y en el bloque del informe |
| AF5-L01-04..20 | Variantes: camelCase, tildes, «ı» sin punto, ancho completo, dígitos, letras duplicadas, marcadores cortos, inglés, `JaneDoe`, `John Doe`, tratamiento y rellenos a ambos lados |
| AF5-L01-21 | 58 variantes adversariales más: todas se rechazan |
| AF5-L01-22 | Contraste directo de `concatenated()` |
| AF5-L01-23, AF5-L01-24 | `AuditorE` y `MrX`: rol o tratamiento e inicial en camelCase |
| AF5-L01-P1 | Control positivo: 99 nombres plausibles, entre ellos «Lola», «Ella», «Donna», «Elena», «Anna», «Nana», «Barr», «Testino» y «Donato» |
| AF5-L01-P2 | Control positivo: registro de FG-02 con la auditora «Lola Donato» |
| AF5-M01-01..03 | FRZ falla con una entrada normativa enlazada, con modo `120000` en el índice o sin vista evaluada |
| AF5-M01-04..08 | El vínculo falla con el plan como enlace en el candidato, ausente del candidato, sin vista evaluada o de tipo inesperado, también registrado en el repositorio |
| AF5-M01-09 | Rutas con `..`, absolutas, con unidad o con flujo alternativo: se rechazan sin leerlas |

### 6.2 Con Git real ([`test_f36sbx_git.py`](../tools/f36sbx/test_f36sbx_git.py))

| Caso | Escenario | Resultado esperado |
|---|---|---|
| G01 | Plan regular versionado | Control positivo |
| G02 | Plan como enlace duro a una copia externa idéntica | Control positivo: se validan los bytes |
| G03 | Ese enlace duro, con el destino externo modificado | Falla: el paquete cambió |
| G04 | Directorio del paquete redirigido (junction en Windows, enlace en Linux) a una copia idéntica | Falla: entradas normativas |
| G04b | `read_normative()` rechaza esa ruta antes de leerla, con su motivo | Sin lectura |
| G05, G05b | Lo mismo, con el plan externo modificado; el texto externo no llega a las reglas | Falla; nada consumido |
| G06, G07 | Plan sustituido por un enlace simbólico a una copia externa, idéntica o modificada | Falla (solo con privilegio de enlaces) |
| G08, G09 | Plan sacado del índice, o sacado e ignorado | Falla |
| G10 | Plan sustituido después del candidato | Falla |
| G11 | Bytes consumidos distintos de los protegidos (lectura alterada, simulada) | Falla: lo comparado es lo consumido |
| G12 | Git no puede leer el árbol del candidato (simulado) | Falla cerrado |
| G13 | Entrada del índice del plan con un objeto inexistente | Falla cerrado |
| G14 | La ruta pasa a ser un enlace entre la comprobación y la lectura (simulado) | Falla cerrado |
| G15 | Contraste de `read_normative()` | Bytes, ausente o no regular |
| G16 | Subdirectorio de las herramientas redirigido a código externo | Falla: recorrido |
| G16b | El recorrido no entra en ese subdirectorio y lo registra con su motivo | Una sola entrada |
| **G20, G21** | **Reproducción de la quinta auditoría**: plan versionado como enlace a un archivo externo (modo `120000`), con el objetivo intacto y después modificado solo el archivo externo | **Falla** (antes, 58/0) |
| G22 | Plan versionado como enlace a otro archivo interno | Falla: se exige archivo regular |
| G23 | Plan versionado como submódulo (objeto de tipo commit) | Falla |
| G24 | El plan vuelve a ser regular | Control positivo |
| G25 | Plan ausente del candidato y presente sin versionar | Falla: no pertenece al candidato |
| G26 | Candidato con el plan en `120000` y HEAD posterior regular | Falla: el modo se comprueba en el árbol del candidato |

## 7. Reproducciones con Git real

**Ataque de Codex, en Linux (WSL, Ubuntu 24.04).** Sobre un clon desechable en `/tmp`, el script de reproducción hace lo siguiente:

1. Versiona el plan como enlace simbólico real a un archivo externo, junto a un ADR regular.
2. Registra evidencia sintética de FG-03 y FG-12.
3. Valida con el objetivo intacto, y de nuevo tras modificar solo el archivo externo. `git status` del plan queda vacío.

Se ejecutó con el validador de cada versión:

| Validador | Objetivo intacto | Objetivo externo modificado | Control: archivo regular modificado |
|---|---|---|---|
| AF4 (`8ae203c`) | **58/0, falso PASS** | **58/0, falso PASS** | 56/2, falla |
| AF5 | 55/4: FRZ «entradas normativas» y GATE | 55/4: FRZ «entradas normativas» y GATE | 57/2, falla |

En la batería, G20 y G21 son esa misma reproducción. En Linux, Git crea el enlace simbólico real. En Windows, sin privilegio de enlaces, Git escribe un archivo de texto con la ruta; el modo `120000` del índice y del candidato hace fallar igualmente FRZ y el vínculo.

## 8. Resultados en Windows y en WSL

| Herramienta | Windows 11 (Python 3.12.10) | Linux WSL2, Ubuntu 24.04 (Python 3.12.3, Git 2.43.0) |
|---|---|---|
| `validate_f36sbx.py` | 59/0 (antes 58: suma la comprobación FRZ de entradas normativas) | 59/0 |
| `test_f36sbx.py` | 545/0 (35 casos nuevos) | 545/0 |
| `test_f36sbx_git.py` | 113/0 y **2 omitidos**: G06 y G07 necesitan crear enlaces simbólicos, que este Windows no permite (WinError 1314). Se informan aparte y no cuentan como correctos | 115/0, sin omitidos (26 casos nuevos; en Windows, 113 correctos y 2 omitidos) |

En WSL se ejecutó en un clon local en `/tmp` (sistema de archivos de Linux), con el paquete y las herramientas del candidato.

**Sí se ejecutaron en Windows:** las uniones de directorios (junction), los enlaces duros, los candidatos con modo `120000` (escritos como archivo de texto) y las simulaciones. **Los enlaces simbólicos reales solo se ejecutaron en WSL.**

## 9. Metapruebas y ablaciones

[`meta_f36sbx.py`](../tools/f36sbx/meta_f36sbx.py) suma 18 ablaciones de código y 5 de función para AF5:

- **AF5-M01:**
  - lectura sin enlaces, archivo regular e identidad de lo abierto;
  - componentes que redirigen, en la ruta y en el recorrido;
  - bytes consumidos frente a releídos;
  - modo del índice;
  - entrada requerida y blob regular en el candidato;
  - FRZ y vínculo;
  - funciones `read_normative` (mutante que sigue enlaces), `link_in_path`, `redirects` (sin uniones ni puntos de reparse) y `safe_repo_path` (sin `:`).
- **AF5-L01:** pieza fuerte, pegamento y relleno, marcadores cortos, letras duplicadas, letras alargadas, pliegue latino, frase en camelCase y `filler_piece`.

Se corrigieron dos ablaciones de AF4 cuya firma ya no coincidía (`concatenated` y `changed_since`): habrían contado como excepción y no como detección. Las 119 ablaciones de código tienen una sola coincidencia.

### 9.1 Ejecución focal de ablaciones

**Qué se ejecutó y por qué.** AF5 cambia la lectura normativa, la vista del árbol de trabajo para esas entradas, el vínculo con el candidato y la identidad. No se repitieron las 113 ablaciones históricas completas; se ejecutaron las de AF5 y las de las piezas que dependen de lo cambiado. Todo corrió en Windows, en un clon local aislado (`git clone --shared`) de `466264d`, con línea base sin fallas en memoria y con Git real.

- **P1, AF5** (23 ablaciones): **21 detectadas** por casos pertinentes y **2 supervivientes**, «lectura: enlace en la ruta» y «recorrido: entrada que redirige». No eran agujeros: eran capas de defensa en profundidad enmascaradas por la comprobación posterior a la lectura. Sin la comprobación previa, la redirección se detectaba igual («cambió durante la lectura»); sin la del recorrido, este entraba en la unión y `read_normative` rechazaba cada archivo por su ancestro. El validador seguía fallando, pero ninguna prueba observaba cada capa. `b2876fc` añade G04b (motivo exacto antes de leer) y G16b (el recorrido no entra en el directorio redirigido).
- **P2, piezas dependientes** (31 ablaciones):
  - identidad de AF2, AF3 y AF4-L01;
  - vista del árbol de trabajo de AF4-M01;
  - FRZ y vínculo de AF4;
  - las funciones `binding_errors`, `changed_since`, `git_blob` y `same_blob`;
  - la regla FRZ entera.

  **30 detectadas** y **1 superviviente**, «AF4-L01 · palabra: camelCase». La nueva gramática ya rechaza sin separar las palabras los casos que la cubrían (`AuditorPlaceholder`, `AuditorNN`). Separarlas sigue siendo necesario: `AuditorE` (rol e inicial) y `MrX` solo se rechazan así. `f266ebc` añade AF5-L01-23 y AF5-L01-24.
- **Reejecuciones dirigidas**, con línea base sin fallas:
  - P3, sobre `f266ebc`: las 2 ablaciones de camelCase, 2 de 2 detectadas;
  - P4, sobre `b2876fc`: las 2 supervivientes de P1, 2 de 2 detectadas, por G04b y G16b.

**Total: 53 ablaciones focales distintas** (P1 y P2 comparten la de la frase marcadora en camelCase), **53 detectadas por casos pertinentes y 0 supervivientes**, tras las reejecuciones dirigidas. Después solo cambió la documentación: este documento, la sincronización del paquete y `PKG_DOCS`, un dato y no una comprobación.

## 10. Regresión proporcional

AF5 cambia la lectura de las entradas normativas, la vista del árbol de trabajo para esas entradas, el vínculo con el candidato y la identidad. Se ejecutaron completas:

- la batería en memoria;
- la batería con Git real, en Windows y en Linux;
- la ablación focal de la sección 9, sobre las piezas cambiadas y las que dependen de ellas.

Siguen corregidos, sin cambios de criterio:

- AF4-M01, AF4-M02 y AF4-PR01..PR05: AF4-01..AF4-12, AF4-M01-1..7 y A1..A13, AF4-M02-1..5 y A1..A4, W01..W19 y RP01..RP07;
- AF4-L01: AF4-L01-01..29, P1 y P2;
- AF3-M01, el ADR es el blob del candidato: AF3-01..AF3-11, U01..U18 y G01..G11;
- AF3-M02, contexto canónico y REL-15: AF3-12..AF3-25, P-12..P-14 y C52..C54;
- AF3-L01: AF3-26..AF3-35, P-07 y P-08;
- AF2-M01, coherencia entre registro, informe y ADR: AF2-01..AF2-12 y D01..D46;
- AF2-M02, hashes, sello y provenance: AF2-13..AF2-24, H01..H12 y P-01..P-04;
- AF2-M03, aislamiento entre organizaciones: AF2-25..AF2-30, X01..X10, P-05 y P-06;
- AF2-L01, tipado y completitud del contrato: AF2-31..AF2-33 y L01..L05.

No se repitieron las ablaciones históricas completas, ni `meta_f36sbx.py hojas`. AF5 no toca el contrato, el ejemplo de conformidad, los hashes, el sello ni el aislamiento entre organizaciones, que son lo que ejercitan esas mutaciones. El contrato (v4), el ejemplo, el esquema de la evidencia de equipo (v2) y el formato de la evidencia no cambian.

## 11. Hallazgos propios

| ID | Severidad | Defecto | Corrección y pruebas |
|---|---|---|---|
| AF5-PR01 | LOW | `safe_repo_path()` aceptaba `C:/x`, que en Windows es absoluta, y `x.md:flujo`, un flujo alternativo de NTFS. Ninguna ruta normativa actual lo explotaba: las constantes son fijas y `safe_doc_path()` exige `docs/` | Rechaza `:` (AF5-M01-09) |
| AF5-PR02 | LOW | La regla FRZ de AF5 en curso habría lanzado una excepción con una vista normativa nula, en lugar de fallar cerrado | Falla cerrado (AF5-M01-03) |
| AF5-PR03 | LOW | La gramática en curso de la sesión interrumpida aceptaba `auditorfictionn`, el propio ejemplo de la auditoría, y rechazaba «Testino» y «Donato» por tolerar una letra sin cubrir y tratar los tratamientos como piezas fuertes | Gramática de la sección 4.2 (AF5-L01-03 y AF5-L01-P1) |
| AF5-PR04 | LOW | En la forma colapsada, `xxxx` se reducía a `x` y contaba como pieza fuerte: «Foxx» se rechazaba | Piezas fuertes colapsadas de cuatro letras o más (AF5-L01-P1) |
| AF5-PR05 | LOW | Una unión de directorios u otro punto de reparse de Windows no se detectaba con la comprobación de enlaces simbólicos sola, y la lectura no comprobaba que lo abierto fuera lo inspeccionado | `redirects()` y la comprobación posterior (G04, G05, G14 y G16) |

## 12. Estado de gobierno

- **F36-SBX:** F36-SBX = EN DISEÑO y F36-SBX-GATE = NO SUPERADO. FG-02, FG-03, FG-10 y FG-12 siguen PENDIENTE y sin evidencia registrada: la evidencia sintética de las pruebas solo existe en memoria o en clones desechables. F37-SBX = BLOQUEADA.
- **Gobierno:** G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; Alcance C productivo = BLOQUEADO; Datos reales = PROHIBIDOS.
- **Decisiones:** RF-23 sigue siendo la decisión final humana y RF-29 sigue experimental e informativa.
- **Alcance:** no hay ML, NLP productivo, embeddings, OCR, búsqueda semántica, LLM, scoring, recomendación ni selección automática, endpoints, migraciones, UI ni dependencias nuevas. F35-SBX, F34, G0, el runtime, Docker, CI y el gobierno global no cambian. El delta se limita a `docs/academico/f36-sbx/` y `docs/academico/tools/f36sbx/`.

Un validador en verde no autoriza nada: no es una aprobación del equipo ni supera el F36-SBX-GATE.

## 13. Evidencia reproducible

```sh
python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py
python -I -B docs/academico/tools/f36sbx/test_f36sbx.py
python -I -B docs/academico/tools/f36sbx/test_f36sbx_git.py   # en Windows, G06 y G07 se omiten sin privilegio de enlaces
python -I -B docs/academico/tools/f36sbx/meta_f36sbx.py ablaciones "AF5"
```

En Linux, o en WSL desde un clon local en el sistema de archivos de Linux, las tres primeras órdenes ejecutan también los enlaces simbólicos reales. Todas las pruebas trabajan en directorios temporales desechables, no usan red y comprueban que el repositorio original no cambia (R00 y R01).

## 14. Criterios para la sexta auditoría independiente

1. Reproducir el ataque de la sección 7 en Linux, con un enlace simbólico real, y comprobar que falla con el objetivo intacto y modificado.
2. Intentar otras redirecciones: enlaces en componentes ancestrales, uniones de directorios, enlaces duros, submódulos, árboles, ejecutables, entradas ignoradas o sin versionar, `..`, rutas absolutas o con unidad, y flujos alternativos.
3. Comprobar que ninguna entrada normativa se consume con bytes distintos de los del blob regular `100644` del commit candidato.
4. Intentar nuevas composiciones genéricas sin separadores, y comprobar que los 99 nombres plausibles siguen siendo válidos.
5. Confirmar que AF2, AF3 y AF4 siguen corregidos y que no hay falsos PASS materiales.
6. Confirmar que el gobierno no cambió: F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.
