# F35-SBX-B — B2: gate sucesor vigente tras B2-FREEZE (corrección de AF-M01)

> **Estado: gate sucesor vigente = IMPLEMENTADO / CANDIDATO A REAUDITORÍA.** Fecha: 14/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`.
>
> - **B2-FREEZE = IMPLEMENTADO / CORREGIDO / PENDIENTE DE REAUDITORÍA FOCAL.** La auditoría independiente sobre `9961d2d65ed51a17c14aae5db0edb7d71c622c22` encontró un hallazgo MEDIUM (AF-M01) y ninguno BLOCKER ni HIGH. AF-M01 se corrige con esta capa sucesora, sin tocar el freeze auditado.
> - **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / APROBADA PARA FREEZE.**
>
> Las secciones 1 a 4 registran la interpretación contractual y el diseño, escritos antes de implementar la corrección (commit RED `5ddf7cca633c1e2b1cb3a0ff2dc5b7b8dfe589f8`). La sección 5 añade los resultados.

## 1. Hallazgo AF-M01 y reproducción

La auditoría confirmó el freeze en todo lo que protege: conjunto congelado, manifiesto, objetos, historia, merges y artefactos. Pero señaló que su documento (§8) presenta al validador del freeze como gate sobre HEAD, y ese validador solo protege su conjunto congelado. El resultado anclado del gate de B2 (119/0 sobre el candidato) más el freeze (10/0) no sustituyen la evaluación material que el gate de B2 hace sobre el estado actual.

Reproducción independiente, previa a cualquier cambio. Se usó un clon limpio sin remoto de `9961d2d`, en la rama de B2, con un LF añadido al final de `docs/academico/datos-sinteticos/dataset/evidence.csv` en el árbol de trabajo:

| Validador sobre ese estado | Resultado |
|---|---|
| `validate_f35sbxb2_freeze.py` (el freeze, aislado) | **10/0**: lo aprueba |
| `validate_f35sbxb2.py` (gate de B2) | **59/60**, con los incumplimientos materiales del cuadro siguiente |

| Regla del gate de B2 | Incumplimiento |
|---|---|
| SBX | SBX-08, SBX-09 y SBX-16 incumplidos (clase B) |
| FSY | Bytes de `evidence.csv` distintos de la base autorizada |
| PRE | `E-ORIGEN`: SHA-256 de origen distinto del manifiesto F34 |
| DYN, ISO, PUR y DAT | No llegan a ejecutarse (falla cerrado) |
| SCP | 13 violaciones: las doce del freeze más `evidence.csv` |

Variantes equivalentes sobre el origen sintético, también con el freeze en 10/0:

| Variante | Gate de B2 |
|---|---|
| Solo el SHA-256 de `evidence.csv` en el manifiesto F34 | 58/61: SBX (SBX-08, SBX-09 y SBX-16), FSY, STA (`F34_INPUTS` distinto del manifiesto F34) y DYN, DET, ISO, PUR y DAT no evaluados |
| CSV y manifiesto alterados de forma coherente entre sí | Las mismas reglas |

La sucesión declarada en B2-FREEZE habría aprobado los tres estados.

## 2. Qué exige la sucesión de gates

Fuentes:

- [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md): §2, §2.2, §3 y DH-B13 (§3.1);
- el gate de [B1](../evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md) y [B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md);
- el [contrato de B2](../evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md) (§2.1 y §2.2);
- [B2-FREEZE](../evidencia-sbx-b2-freeze/F35SBXB_B2_Freeze.md) (§8).

Puntos que deciden la interpretación:

- **B0 §2.2, principios A y B.** «Un PASS histórico solo demuestra el estado histórico correspondiente» y «nunca prueba que HEAD sea válido».
- **B0 §2.2, principio C.** «El gate sucesor valida efectivamente HEAD, en todo lo que lista §3». §3 incluye los criterios SBX recalculados, el dataset y su procedencia por SHA-256, la integridad de A, el árbol, el índice, los artefactos ignorados, los enlaces y los flags.
- **DH-B13, punto 6.** Una falla de alcance (clase A) «no demuestra por sí sola una revocación sustantiva, pero no se ignora: obliga a ejecutar la evaluación sucesora completa sobre HEAD».
- **DH-B13, punto 7.** «La sucesión no reduce ni reinterpreta los criterios: solo sucede el mecanismo de verificación».
- **B1-FREEZE.** Su validador sobre HEAD ejecutaba, además de su integridad, todas las reglas del gate de B1 cargado desde bytes verificados, con el alcance ampliado exactamente a sus tres archivos. B2-FREEZE dejó fuera esa parte.

**Conclusión.** Conservar la evaluación material vigente significa que el gate válido sobre HEAD ejecuta, sobre el estado actual, todas las comprobaciones del gate sucesor congelado de B2, con su código verificado y sin reinterpretarlas:

- las 19 reglas, de CTX a GOV;
- P01..P36, las historias F01..F21 y los negativos NB2 y PB2.

La única comprobación que no puede pasar es SCP, porque es de clase A: el gate congelado no reconoce la evolución autorizada de rutas. Esa falla no se ignora ni se oculta. Se sustituye por un alcance exacto del sucesor (principio D: rutas concretas) y se exige que SCP falle solo por esas rutas. El resultado anclado sobre el candidato y la integridad del freeze siguen siendo necesarios, pero no bastan.

**Causa raíz.** B2-FREEZE trató el resultado anclado de B2 más su propio validador como sucesión completa. Por eso ninguna regla vigente evaluaba sobre HEAD lo que el gate de B2 dejó de poder evaluar legítimamente.

## 3. Diseño de la corrección

Una capa sucesora nueva, separada del freeze y con su propia ancla. El nombre sigue el término normativo de B0 («gate sucesor sobre HEAD») y el patrón `<incremento>_<papel>` de `f35sbxb2_freeze`.

| Ruta | Contenido |
|---|---|
| `docs/academico/tools/f35sbxb2_sucesor/validate_f35sbxb2_sucesor.py` | Gate sucesor vigente sobre HEAD |
| `docs/academico/tools/f35sbxb2_sucesor/test_f35sbxb2_sucesor.py` | Batería AF01..AF14 |
| `docs/academico/evidencia-sbx-b2-sucesor/F35SBXB_B2_Sucesor.md` | Este documento |

| Gate | Papel | Dónde se ejecuta |
|---|---|---|
| Gate de B2 (`validate_f35sbxb2.py`), histórico | Acredita el candidato: 119/0 | Anclado sobre `2472fd6`, en un clon temporal sin remoto |
| Validador del freeze (`validate_f35sbxb2_freeze.py`) | Integridad del candidato y de la capa del freeze | Sobre HEAD |
| Gate sucesor (`validate_f35sbxb2_sucesor.py`), vigente | Compone los dos anteriores y la evaluación material vigente | Sobre HEAD de la rama de B2, `develop` y `main` |

Reglas del gate sucesor:

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. Git sin variables `GIT_*` heredadas, sobre el repositorio del validador, con historia completa y sin injertos ni objetos de reemplazo |
| ANC | Anclas registradas: el candidato `2472fd6…` y el freeze `9961d2d…` son commits íntegros (objetos verificados); el freeze desciende del candidato y HEAD del freeze |
| HIS | El gate de B2, con los bytes del candidato, ejecutado anclado sobre `2472fd6` en un clon temporal sin remoto: código 0, ninguna falla y la transición de gobierno derivada igual a la registrada (`12c1c36`) |
| CON | La capa del freeze tiene en HEAD, el índice y el disco los blobs de `9961d2d`. Su validador, verificado antes de ejecutarlo, termina con código 0 y sin fallas, y deriva como candidato `2472fd6` y como commit de freeze exactamente `9961d2d` |
| MAT | El gate de B2 se verifica byte a byte contra el candidato y se ejecuta sin cambios sobre HEAD. Toda comprobación pasa salvo SCP, y SCP solo falla por clase A: cada ruta enumerada del sucesor en el árbol de HEAD, el árbol de trabajo y el índice, y nada más. El total de comprobaciones coincide con el de la ejecución histórica |
| ALC | Alcance exacto del sucesor frente al candidato. HEAD, el índice y el árbol de trabajo añaden exactamente las rutas enumeradas (la capa del freeze y esta capa), no hay archivos sin seguimiento, y las rutas de esta capa están confirmadas, son regulares y no tienen archivos extra en el disco |
| DEP | Esta capa solo importa la biblioteca estándar autorizada y no ejecuta código dinámico |

**Por qué SCP no se debilita.**

- El gate de B2 se ejecuta intacto, como proceso propio y con sus bytes aprobados, y sigue informando SCP en falla (118/1 sobre HEAD limpio).
- Ninguna constante suya se modifica en memoria, ningún archivo se excluye de su ejecución y su resultado no se convierte en 119/0.
- El gate sucesor solo clasifica esa falla, y exige a la vez dos cosas: que el alcance real sea exactamente el enumerado (ALC) y que SCP no tenga ninguna violación ajena a él (MAT).
- Cualquier otro cambio, como el de `evidence.csv`, aparece como violación ajena y además hace fallar las reglas materiales.

**Raíz de confianza de la capa del freeze (LOW de la auditoría).** El gate sucesor registra el hash exacto del freeze (`9961d2d…`), que ya existe. No hay autorreferencia: es el patrón con que B2 registró su transición de gobierno. Además, verifica los bytes del validador del freeze contra ese commit antes de ejecutarlo y exige que el freeze derivado coincida con el registrado. Así, un PASS aislado del freeze sobre otra historia (un ancla derivada distinta con los mismos bytes) ya no basta.

**Fallo cerrado.** Hacen fallar el gate:

- un candidato o un freeze ausentes, o una ascendencia que no corresponde;
- un validador del freeze o un gate de B2 distintos de sus blobs, que entonces no se ejecutan;
- una salida incompleta, un código de salida inesperado o una línea no reconocida;
- un error de Git, un repositorio superficial, injertos u objetos de reemplazo;
- cualquier error al crear o borrar el clon temporal.

**Qué no cambia.**

- El almacén, el gate de B2 y los cuatro archivos de B2-FREEZE conservan sus bytes.
- `9961d2d` sigue siendo el freeze auditado que recibió AF-M01.
- `CLAUDE.md` y `docs/PROGRESS.md` siguen congelados con el blob de B2. La actualización de gobierno sigue pendiente de un incremento sucesor autorizado.

## 4. Pruebas

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, y ejecuta el gate sucesor con `python -I`. Pasa si fallan exactamente las reglas esperadas. En los casos materiales, además, la línea INFO de MAT tiene que nombrar las reglas del gate de B2 que detectan el incumplimiento.

| Caso | Escenario | Resultado esperado |
|---|---|---|
| AF01 | HEAD con el freeze intacto y estado material válido | PASS |
| AF02 | LF añadido a `evidence.csv` | FAIL en MAT y ALC; MAT nombra SBX, FSY y PRE |
| AF03 | Origen sintético alterado: (a) solo el SHA-256 en el manifiesto F34; (b) CSV y manifiesto coherentes entre sí | FAIL en MAT y ALC; MAT nombra SBX, FSY y STA |
| AF04 | Artefacto congelado de B2: (a) almacén alterado y confirmado; (b) gate de B2 alterado en el disco | (a) FAIL en CON y ALC; (b) FAIL en CON, MAT y ALC, y el gate alterado no se ejecuta |
| AF05 | Capa del freeze: (a) validador alterado y confirmado; (b) manifiesto alterado en el disco | FAIL en CON en ambas |
| AF06 | Modificar → restaurar un archivo congelado | FAIL en CON |
| AF07 | Merge `--no-ff` de la rama de B2 en `develop` (`72e86c5`) y de `develop` en `main` (`3fdfdce`) | PASS en ambos |
| AF08 | Rama lateral que altera y restaura un archivo congelado, integrada con merge `--no-ff` | FAIL en CON |
| AF09 | Estado limpio: el gate de B2 sobre HEAD sigue en 118/1, solo con SCP | PASS del sucesor, sin exigir 119/0 sobre HEAD |
| AF10 | El candidato se sigue acreditando: HIS informa código 0 y ninguna falla sobre `2472fd6`, con el mismo total que MAT | PASS |
| AF11 | Freeze reconstruido con los mismos bytes en otra historia, de modo que el validador del freeze lo aprueba con otra ancla | FAIL en ANC y CON |
| AF12 | `evidence.csv` alterado y `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` apuntando a un clon limpio | FAIL en MAT y ALC; MAT nombra SBX, FSY y PRE |
| AF13 | Clon superficial | FAIL cerrado en ENT, ANC, HIS, CON, MAT y ALC |
| AF14 | Artefacto ignorado en `public/build/`, invisible para `git status` y para ALC | FAIL solo en MAT; MAT nombra FSY |

AF11 a AF14 cubren propiedades que AF01..AF10 no ejercitan:

- **AF11:** el ancla registrada del freeze, que es el LOW.
- **AF12:** el saneamiento del entorno de los subgates, porque el gate de B2 no descarta `GIT_*` por sí mismo.
- **AF13:** el fallo cerrado ante una historia truncada.
- **AF14:** lo que solo la evaluación material detecta. Se añadió después del primer GREEN, al comprobar que AF02, AF03 y AF12 también los detecta ALC (cualquier cambio versionado sale del alcance). Un artefacto ignorado en una superficie del runtime no lo ven ni ALC ni el freeze, y FSY del gate de B2 sí. Es la clase de los artefactos preexistentes del checkout del equipo.

## 5. Resultados

### 5.1 RED y GREEN

| Commit | Contenido | Resultado |
|---|---|---|
| `5ddf7cca633c1e2b1cb3a0ff2dc5b7b8dfe589f8` | Batería AF01..AF13 y este diseño (RED) | 0 casos correctos y 13 fallas, con 17 ejecuciones: el gate sucesor no existía |
| `20146d0ea8df0ad5f2b9bb0515f22a3954e560f3` | Gate sucesor y AF14 (GREEN) | 14 casos correctos y 0 fallas, con 18 ejecuciones del gate sucesor. Se midió sobre un commit desechable con su mismo árbol (`1132689fc651f305c4cab46e10effe44e1bc8776`) |

La primera implementación pasó AF01..AF13 al primer intento, sin endurecimiento. AF14 se añadió después, por la razón de §4.

Esta evidencia es un commit posterior y su hash se consulta en Git.

### 5.2 Detección material

Salida del gate sucesor (línea INFO de MAT y reglas en falla) sobre el commit desechable del GREEN:

| Caso | Gate de B2 sobre ese HEAD | Reglas del sucesor en falla |
|---|---|---|
| AF02 | 59/60. Reglas DAT, DYN, FSY, ISO, PRE, PUR, SBX y SCP, y 52 casos. SCP con 22 violaciones frente a las 21 del alcance | MAT; ALC (`evidence.csv` modificado) |
| AF03 (a) y (b) | 58/61. Reglas DAT, DET, DYN, FSY, ISO, PUR, SBX, SCP y STA, y 52 casos. SCP con 22 y 23 violaciones | MAT; ALC (el manifiesto F34, y en (b) también `evidence.csv`) |
| AF04 (a) | 118/1, solo SCP: añadir un comentario al almacén no es material para el gate | CON (el freeze falla en HIS, ARB, IDX y DSK); ALC |
| AF04 (b) | No se ejecuta: el gate alterado no coincide con su blob `c2b625a` | CON, MAT y ALC |
| AF11 | 118/1, solo SCP | ANC (el freeze registrado no es ancestro de HEAD); CON (el freeze deriva `ed1d8d6…`, no el registrado: «ancla no autenticada») |
| AF12 | 59/60, igual que AF02: las variables `GIT_*` hostiles se descartan | MAT; ALC |
| AF14 | 117/2: FSY («código generado y no versionado») y SCP (21, todas del alcance) | Solo MAT |
| AF09 | El gate de B2 ejecutado directamente da 118/1, solo SCP | Ninguna: el sucesor pasa con 7/0 |

### 5.3 Controles de mutación

La batería se ejecutó contra un gate sucesor debilitado a propósito, en clones desechables:

| Mutación | Casos que la detectan |
|---|---|
| Sin evaluación material, que es el defecto de AF-M01 | AF02, AF03 (las dos sondas) y AF12, que pierden MAT; AF14, que pasa a PASS |
| CON sin comparar el freeze derivado con el registrado, que es el LOW | AF11, que solo falla en ANC |
| Subgates que heredan `GIT_*` | AF12: falla en ENT, HIS y MAT en lugar de MAT y ALC. Con esas variables, incluso ALC miraba el clon limpio |

### 5.4 Validación en clon limpio

Los resultados se obtuvieron en clones limpios sin remoto, sobre un commit desechable con el mismo árbol que este commit. Su repetición sobre el commit real se registra en el reporte de entrega.

| Comprobación | Resultado |
|---|---|
| `validate_f35sbxb2_sucesor.py` | 7/0, en unos 40 segundos |
| `test_f35sbxb2_sucesor.py` | 14/0, con 18 ejecuciones del gate sucesor, en unos 11 minutos |
| `validate_f35sbxb2_freeze.py` sobre HEAD y anclado sobre `9961d2d` | 10/0 en ambos, con el freeze derivado `9961d2d` |
| `test_f35sbxb2_freeze.py` | 27/0, con 33 ejecuciones del validador |
| Gate de B2 anclado sobre `2472fd6` | 119/0, con la transición derivada igual a la registrada (`12c1c36`) |
| Gate de B2 sobre HEAD | 118/1: solo SCP, con 21 violaciones (las siete rutas del sucesor en tres planos). Anclado sobre `9961d2d`, también 118/1, con las doce del freeze |
| Gate de B1 anclado sobre `8e94a60` y B1-FREEZE anclado sobre `3d9b783` | 159/0, con los 18 SBX en PASS, y 14/0, con SBX 18/18 |
| Gate de B1 y validador de B1-FREEZE sobre HEAD | 105/54 y 0/2. Fallan las mismas reglas que sobre el candidato (clase A desde la transición de gobierno), solo con más rutas y commits listados |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py`, `test_f32_safety.py`, `validate_f33.py`, `validate_f34.py` y `validate_f34a.py` | 225/0, OK, 451/0, 403/0 y 108/0 |
| `validate_f34e.py` sobre `2472fd6`, `9961d2d` y HEAD | 247/1 en los tres, con SBX 18/18 sobre HEAD. Es la falla histórica de la regla GIT. Su lista de rutas no autorizadas por DH-02 pasa de 12 a 16 con el freeze y a 19 con esta capa, sin que desaparezca ninguna, y el resto del mensaje es idéntico |
| Enlaces relativos | 1120, 0 rotos |
| MANIFEST y evidencias | 61 hashes y 0 discrepancias; 0 discrepancias en las evidencias |
| `git diff --check` frente a `2472fd6` y a `9961d2d` | Limpio |
| Delta frente al candidato | Exactamente las siete rutas enumeradas (A) |

### 5.5 Checkout del equipo

Sobre el checkout original, sin limpiar sus artefactos preexistentes:

- **Gate sucesor: 6/1.** Solo falla MAT, porque el gate de B2 falla en FSY por los 20 artefactos ignorados de siempre (`.pyc` de pytest y `public/build`), que es la clase de AF14. HIS, CON, ANC, ALC, ENT y DEP pasan.
- **Validador del freeze: 10/0.**

La certificación se hace en un clon limpio: el gate sucesor no confunde la integridad de Git con la limpieza del sistema de archivos local, pero tampoco la ignora.

### 5.6 Sucesión vigente

| Gate | Papel | Dónde | Resultado en clon limpio |
|---|---|---|---|
| `validate_f35sbxb2_sucesor.py` | Gate sobre HEAD, en la rama de B2, `develop` y `main` | HEAD | 7/0 |
| `validate_f35sbxb2.py` | Gate histórico de B2 (dentro de HIS) | Anclado sobre `2472fd6` | 119/0 |
| `validate_f35sbxb2.py` | Evaluación material (dentro de MAT) | HEAD | 118/1, solo SCP de clase A |
| `validate_f35sbxb2_freeze.py` | Integridad del candidato y del freeze (dentro de CON) | HEAD, y anclado sobre `9961d2d` | 10/0 |
| `validate_f35sbxb.py` y `validate_f35sbxb_freeze.py` | Gates históricos de B1 y B1-FREEZE | Anclados sobre `8e94a60` y `3d9b783` | 159/0 y 14/0 |

Esta tabla supera la de §8 del documento de B2-FREEZE, congelado en `9961d2d`. El validador del freeze sigue vigente, pero como parte de este gate y no como único gate sobre HEAD.

### 5.7 Riesgos residuales

| # | Nivel | Riesgo | Tratamiento |
|---|---|---|---|
| R1 | LOW | Esta capa no se protege a sí misma: ningún archivo puede registrar su propio hash | La reauditoría anota el commit de la corrección, y un incremento posterior lo registra como aquí se registró el freeze |
| R2 | INFO | MAT lee la salida textual del gate de B2, que muestra como mucho tres violaciones por regla | El formato se valida de forma estricta: solo su línea INFO, líneas FALLA y su resumen, coherentes con el código de salida. SCP se clasifica por su recuento, por las entradas mostradas y por el alcance exacto de ALC |
| R3 | INFO | Cada ejecución tarda unos 40 segundos: dos ejecuciones del gate de B2 en paralelo y un clon temporal en TEMP, fuera del repositorio | Es el coste de conservar la evaluación completa |
| R4 | INFO | En el checkout del equipo, MAT falla por FSY (artefactos preexistentes) | Es deliberado; el checkout no se limpia y la certificación es en clon limpio |
| R5 | INFO | Cualquier cambio fuera del alcance enumerado hace fallar este gate, incluido uno legítimo de un incremento futuro | Es una falla de clase A para ese incremento, que aportará su propio gate sucesor |
| R6 | INFO | `CLAUDE.md` y `docs/PROGRESS.md` siguen describiendo B2 como candidata a auditoría | Actualización de gobierno pendiente de un incremento sucesor autorizado |
| R7 | INFO | F34E lista las rutas nuevas entre las no autorizadas por DH-02 | Es la misma regla, con el mismo recuento, como con B0..B2-FREEZE |

### 5.8 Próximo paso

Reauditoría focal de AF-M01 por el mismo auditor independiente. Hasta entonces:

- B2-FREEZE no se aprueba para integración;
- B2 no se declara cerrada, congelada ni integrada;
- no hay push, merge, tag ni release.
