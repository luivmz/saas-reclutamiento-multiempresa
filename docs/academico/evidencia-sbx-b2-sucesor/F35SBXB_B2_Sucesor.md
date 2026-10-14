# F35-SBX-B — B2: gate sucesor vigente tras B2-FREEZE (corrección de AF-M01)

> **Estado: gate sucesor EN CORRECCIÓN: diseño y pruebas en RED, sin validador.** Fecha: 14/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`.
>
> - **B2-FREEZE = IMPLEMENTADO / AUDITADO CON HALLAZGOS / NO APROBADO PARA INTEGRACIÓN.** La auditoría independiente sobre `9961d2d65ed51a17c14aae5db0edb7d71c622c22` encontró un hallazgo MEDIUM (AF-M01) y ninguno BLOCKER ni HIGH.
> - **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / APROBADA PARA FREEZE.**
>
> Este documento registra la interpretación contractual y el diseño de la corrección antes de implementarla. Los resultados se añaden cuando existan.

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
| `docs/academico/tools/f35sbxb2_sucesor/test_f35sbxb2_sucesor.py` | Batería AF01..AF13 |
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

AF11 a AF13 cubren propiedades que AF01..AF10 no ejercitan: el ancla registrada del freeze, que es el LOW; el saneamiento del entorno de los subgates, porque el gate de B2 no descarta `GIT_*` por sí mismo; y el fallo cerrado ante una historia truncada.

## 5. Resultados

Pendientes: se registrarán tras la implementación.
