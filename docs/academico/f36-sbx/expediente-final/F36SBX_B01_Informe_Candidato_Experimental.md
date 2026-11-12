# B-01 · Informe del candidato experimental del sucesor

> **CANDIDATO EXPERIMENTAL — NO ES B-01 IMPLEMENTADO.**
>
> - **Dónde.** Rama local `exp/b01-candidato`, creada el 10/11/2026 desde el commit `55f758e` por autorización operativa de Luis Vila Meza para el desarrollo técnico local.
> - **Lo que falta.** D-02b no está emitida (S v2.2 P-S1 a P-S4), así que **AC-01 no se cumple**. T-01 a T-09 siguen NO EMITIDAS y H no está fijado.
> - **Estados.** Ningún estado formal cambia: F36-SBX = EN DISEÑO, F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.
> - **Publicación.** Sin push, merge, tag ni release.

## 1. Identidad

| Elemento | Valor |
|---|---|
| Especificación | S v2.2, `2b074e419452451b75dc49c9947ada037f3ae300`, blob de S `a7ef013586c811845e5c238ec96fc33dfdeb30c3` |
| Punto de partida (T-09 (a-ii)) | `55f758e013e1852de8c8daa5d6fde95e39b02b0d`; `BASE` sin cambios (`b8892af…`) |
| Trasplante del paquete | `779418b`: `docs/academico/f36-sbx/` de `2b074e4`, 30 rutas |
| Implementación | `c96823a76e3b06a209bcf108196c388ab34e556d`, árbol `7322f12d…` |
| Candidato auditado por Codex (10/11/2026) | `a0f6dd432a50041be2ae3766ef949722c62ab4f7`, árbol `c6cac83d…` |
| Correcciones de esa auditoría | `d83d92434975d0bbf5b92ad4075a759f978d8870`, árbol `c182e699…` |
| Restos de esas correcciones (12/11/2026) | `badb1f5c790e880b24ab6a6bf8f7cf2a4099d476`, árbol `be6c370b…`: último cambio del validador |
| Pruebas y metapruebas (12/11/2026) | `17c7af27c944a328e5bdd2224158a59e054c8af7`, árbol `f260abc4…`: último commit de herramientas; no toca el validador |
| Validador v3 (histórico) | SHA-256 `87ad2f6fed43dd5ae4f0c4baf8721de0a2be71e0efacdb27c8d1f514ea3563ec` |
| Validador del candidato (vigente, `badb1f5`) | SHA-256 `399a3eca8b78cdb5652537a8801ec4dc53a8b7f75ef16810f2246c900377ff3a` |
| Validadores anteriores del candidato | `47d2f47d…` en `a0f6dd4` (el auditado) y `4508e6d6…` en `d83d924` |

## 2. Opciones técnicas aplicadas

Son las de S v2.2. Ninguna está decidida por el equipo.

| Decisión | Opción del candidato |
|---|---|
| T-01 | Espejos E1–E7 de H §5.2, con la reescritura D-07 |
| T-02 | F37-SBX = AUTORIZADA PARA INICIAR solo con R = SUPERADO |
| T-03 | No: F36-SBX sigue EN DISEÑO en la transición |
| T-04 | Una rama nueva, `exp/b01-candidato`. El nombre es provisional |
| T-05 | Formato y delta de §5.8.1 y §5.8.2, con C-R |
| T-06 | No implementado (opcional) |
| T-07 y T-08 | (i): solo la variante 3/3, `gate_version` 3 y esquema v2 |
| T-09 | (a-ii) |

**Reescritura D-07.**

- **Documento del gate.** Tiene una sección «Resultado canónico» con la línea E2. La cabecera ya no afirma el resultado.
- **README del paquete.** Lleva dos viñetas canónicas (E3) y una frase aparte sobre la evidencia pendiente.
- **Gobierno.** En los cuatro documentos, la frase del párrafo de F36 que repetía los dos estados remite ahora a las viñetas (E4–E7).

## 3. Qué cambia en el validador

- **Resultado R.** Se deriva de la evidencia. Una `revocation` con el formato cerrado da REVOCADO, que prevalece. Una mal formada, con fecha anterior a H, con evidencia inexistente en H o sin `candidate_commit` falla cerrado: NO SUPERADO y una falla.
- **Espejos.** La comprobación de `:2877` («el gobierno exige NO SUPERADO») se sustituye por `mirror_errors`: E1–E7 declaran exactamente R y el estado derivado de F37-SBX, una vez por sujeto en su ámbito, y cualquier diferencia falla en los dos sentidos.
- **Gobierno.** `required_state(R)` sustituye a la lista fija. SEM admite el vocabulario cerrado en las líneas canónicas y solo los estados históricos fuera de ellas.
- **Después de H.**
  - X2 se compara campo a campo con el blob de H.
  - X3–X5 se comparan línea a línea (`canonical_only`).
  - X1-R y X2-R solo se admiten con las cuatro condiciones de C-R.
  - La identidad de H (H §5.6) se comprueba siempre.
- **Ramas.** `BRANCHES` admite `exp/b01-candidato`.
- **Módulos locales.** `test_f36sbx_b01` pasa a ser un módulo local admitido por DEP.
- **Correcciones posteriores a la auditoría.** Las de `d83d924` y `badb1f5` están en la §10: permanencia de la revocación, formato, ámbito de los espejos, determinación versionada y vínculo de la evidencia EQUIPO.

## 4. RED y GREEN

Los logs completos están fuera de Git, en `experimental-20261110/evidencias/b01/`.

| Paso | Resultado |
|---|---|
| RED (AC-02): `test_f36sbx_b01.py` contra el validador v3, antes de cambiarlo | **14 fallas**: S-T01, S-T02, AC-09, H-5.4, H-5.3b, S-T17, S-T11, H-5.6, S-T18, S-T18c, S-T20a, S-T20b, S-T21c y S-T21d. Las demás pruebas ya pasaban con v3 por otros motivos (por ejemplo, FRZ por la rama) |
| Validador v3 sobre la rama trasplantada | 57/2: la rama no está admitida y FG-01/FG-05 se recalculan |
| GREEN: validador del candidato sobre la rama | **59/0**, R = NO SUPERADO declarado y recalculado (AC-04) |
| `test_f36sbx_b01.py` | **36/0**, con S-T02b y S-T02c añadidos para que la ablación del «falla cerrado» se pueda detectar |
| `test_f36sbx.py` (memoria) | **547/0**. Se adaptaron 7 casos que codificaban v3: M09, M12, G06 y la simulación de Git de los controles positivos. Se añadieron M09b y G06b |
| `test_f36sbx_git.py` (Git real) | **113/0**, 2 omitidos (enlaces simbólicos sin privilegio en Windows, como en la línea base). `sync_package` copia también los documentos de gobierno |
| Sondas desde el árbol del candidato (S-T22) | `sondas_t09`, `sonda_revocacion` y `sonda_trasplante`: código 0, 0 discrepancias |

Estas cifras son las de `c96823a`. Las de las correcciones están en la §10.3, y sus logs en `experimental-20261110/evidencias/correcciones-20261111/` y `correcciones-20261112/`.

## 5. Criterios de aceptación

| ID | Estado | Evidencia o falta |
|---|---|---|
| AC-01 | **No cumplido** | D-02b no emitida; P-S1 (D-10) pendiente |
| AC-02 | Cumplido para la batería nueva | RED de §4 y, para las correcciones, de §10.3, cada uno antes de su arreglo. El plan de pruebas de H (`1d5d6aa`) no se portó entero: sus casos están representados en S-T01 a S-T22 y en la batería adaptada |
| AC-03 | Cumplido para las metapruebas focales B-01 | GREEN de las cuatro baterías sobre `badb1f5` y `17c7af2`. Metapruebas focales B-01 en §6: las 21 ablaciones quedan detectadas por casos pertinentes. La corrida completa de todas las metapruebas no se ejecutó |
| AC-04 | Cumplido | 60/0 en la rama, R = NO SUPERADO; S-T11 en un clon |
| AC-05 | Cumplido | `git diff --name-only 55f758e HEAD` dentro del perímetro; incluye `sondas-b01/` (S-T22a); sondas ejecutadas desde el árbol |
| AC-06 | Cumplido | S-T15 |
| AC-07 | Cumplido con el nombre provisional | S-T13, S-T14 y S-T17 |
| AC-08 | Cumplido para el candidato | Inventario explícito en la §12: el hash vigente consta en el único documento operativo que lo cita, y las citas de v3 se conservan como históricas |
| AC-09 | Cumplido | AC-09a a AC-09d, M09 y B01-M03 (excepción de SEM por ubicación) |
| AC-10 | Cumplido en clones | S-T01 a S-T03, S-T02b, S-T02c y S-T18 a S-T21 sobre el validador nuevo, más la permanencia (B01-H01, N01 y N02), el formato (M01, M02 y N03), la determinación versionada (M04) y SUPERADO → REVOCADO (DS-B01-3d y 3e) |
| AC-11 | Cumplido | `gate/evidencia/` no existe en la rama |
| AC-12 | Cumplido | S-T09 y S-T10 |
| AC-13 | Registrado | §7 |
| AC-14 | Cumplido | DEP: solo biblioteca estándar |

## 6. Metapruebas

`meta_f36sbx.py` incluye la batería B-01 y diez ablaciones nuevas:

- las funciones `revocation_errors`, `mirror_errors`, `mirror_lines`, `required_state`, `derived_states`, `identity_errors_h`, `delta_errors_h` y `canonical_only`;
- la degradación de una revocación no vinculada;
- la rama de H en `BRANCHES`.

**Sin resultado sobre `c96823a`.** La ejecución focal (`meta_f36sbx.py ablaciones B-01`) la detuvo el sistema por falta de memoria (0,7 GB libres de 16) antes de imprimir nada.

**Ablaciones nuevas.** Las correcciones (`d83d924` y `badb1f5`) añadieron once, con lo que las B-01 son 21:

- `real_instant`, `without_mirror_lines`, `revocation_history` y `determination_committed`;
- la comprobación de tipo de `ground` y la de permanencia (`if not kept`);
- el árbol de H en la regla de decisión y en la historia;
- la historia leída solo por el estado;
- `mirror_line_numbers` y los límites del desfase.

**Resultado.**

- **Sobre `badb1f5`.** Línea base sin fallas; 19 de 21 ablaciones detectadas por casos pertinentes. Dos sobrevivían:
  - **B01-M03.** La regresión ponía la afirmación fuera del espejo como texto, no con la forma de la viñeta canónica.
  - **Permanencia.** La aguja `if not kept:` no coincidía con nada, porque las metapruebas comparan solo la condición.
- **Sobre `17c7af2`.** Corrige las dos: B01-M03b falla con el validador de `a0f6dd4`, y la aguja pasa a ser `not kept`. La repetición focal de esas dos ablaciones da 2 de 2 detectadas (B01-M03b en sus 4 variantes; B01-H01a a B01-H01d, B01-N01b y B01-N02b), con la línea base sin fallas.

Las otras 19 no se repitieron: el validador es el mismo, y la batería solo ganó los cuatro casos de B01-M03b, así que su detección no puede disminuir.

La corrida completa de las metapruebas, fuera de las focales B-01, no se ejecutó.

## 7. Integración en `develop` (AC-13, I-14)

Si H se integrara en `develop`, FRZ fallaría allí por diseño, porque `develop` contiene los cambios de runtime de SEG respecto de `b8892af`.

S-T14 lo reproduce con el validador nuevo: una rama con el nombre de H cortada desde `develop` da FRZ «fuera de alcance» y «cambios de runtime» con los archivos de `app/` de SEG, y FG-01 y FG-05 en NO CUMPLE. No es una regresión: el resultado R se lee anclado en la rama de H. Cualquier integración exige la autorización del contrato 10.

## 8. Diferencias pendientes con S v2.2

| ID | Diferencia | Tratamiento en el candidato |
|---|---|---|
| DS-B01-1 | X2-R no incluye `candidate_commit`. Una revocación registrada sin evidencia previa no dice qué commit es H, y el validador solo identifica H por `candidate_commit` | Falla cerrado: una revocación exige `candidate_commit` = H (la transición de nulo a H que X2 ya admite). Aclaración propuesta en la §11 (P-01) |
| DS-B01-2 | Con una revocación válida y vinculada, una falla ajena (por ejemplo, un archivo sin citar en `gate/evidencia/`) hace fallar el validador, pero deja R = REVOCADO (I-11). S §3 dice que R se fuerza a NO SUPERADO ante cualquier falla previa de GATE | Se aplica I-11, también a la permanencia de B01-H01. Decisión pendiente, con sus dos opciones y su efecto en las pruebas, en la §11 (P-02) |
| DS-B01-3 | No había control positivo SUPERADO con la evidencia completa de FG-02, FG-03, FG-10 y FG-12 en un clon (S-T05) | **Cubierto desde `d83d924`** con Git real: DS-B01-3a a DS-B01-3e (§10). Son registros sintéticos de un clon desechable, no actos del equipo |
| DS-B01-4 | La variante RD (T-08 (ii)) y T-06 | No implementadas, conforme a la propuesta de S |
| DS-B01-5 | La cabecera de `docs/PROGRESS.md` conserva una foto fechada («F36-SBX-GATE NO SUPERADO») fuera del bloque de estado | No es una afirmación «sujeto = estado». Queda como dato histórico |

## 9. Lo que no hace este candidato

- No registra evidencia, votos, decisiones ni estados.
- No fija H.
- No autoriza F37-SBX.
- No cambia el contrato de evidencia v4, la G0 real, ADR-005, el alcance C, RF-23 ni RF-29.

## 10. Hallazgos de la auditoría del 10/11/2026 y sus correcciones

Codex auditó `a0f6dd4` (informe con SHA-256 `713d4d7d555b0e3e2d5347d9c68e4cd4c17e362df8ea24c9b215acfe68f0711c`, fuera del repositorio). `d83d924` corrigió sus hallazgos. El 12/11/2026, al contrastar esas correcciones con S v2.2 y con la especificación de H (`1d5d6aa`), se encontraron cuatro restos (B01-N01 a B01-N04), que corrige `badb1f5`. Las metapruebas focales sobre `badb1f5` dejaron dos ablaciones sin detectar, que `17c7af2` vuelve a armar sin tocar el validador. Cada prueba nueva se vio fallar antes de su corrección.

### 10.1 Tabla de hallazgos

| ID | Hallazgo | Corrección | Commit | Pruebas |
|---|---|---|---|---|
| B01-H01 (HIGH) | Una revocación válida se retiraba en un commit posterior, con el mismo H, y el validador volvía a dar NO SUPERADO sin fallas | La historia de la rama posterior a la base registra cada revocación válida. El árbol validado tiene que conservar la primera tal cual: mismo evento y misma determinación. Si no, falla y R queda en REVOCADO (I-11). Si la historia no se puede leer, falla cerrado | `d83d924`; completada en `badb1f5` (N01 y N02) | B01-H01a a B01-H01d, DS-B01-3e, B01-N01b y B01-N02b |
| B01-M01 | Un instante imposible (`2026-99-99T99:99:99+99:99`) valía como `effective_from` | Fecha, hora y desfase se interpretan con la biblioteca estándar | `d83d924`; completada en `badb1f5` (N03) | B01-M01, B01-M01b (instante válido anterior al registro) y B01-M01g |
| B01-M02 | Un `ground` compuesto (`[]`, `{}`) interrumpía el validador con `TypeError` | Las cinco claves se comprueban por tipo antes de usarlas: diagnóstico y NO SUPERADO | `d83d924` | B01-M02 (lista, objeto, número y nulo), B01-M02g y B01-M02h |
| B01-M03 | La excepción de SEM se aplicaba por valor: la misma afirmación fuera del espejo pasaba | Solo se exceptúan las líneas canónicas dentro del ámbito de su espejo | `d83d924` | B01-M03 en README y gate, con SUPERADO y con REVOCADO; B01-M03b, con la forma exacta de la viñeta canónica fuera del espejo (`17c7af2`) |
| B01-M04 | Valía una determinación sin versionar | La determinación tiene que ser un blob `100644` de HEAD, sin cambios en el árbol de trabajo (S:118) | `d83d924` | B01-M04a (sin seguimiento), B01-M04b (solo en el índice) y S-T18 (versionada) |
| B01-L01 | La prosa del gate repetía el resultado. El README enumeraba tres ramas | La prosa remite a la línea canónica. El README cita la rama experimental y remite a este informe | `d83d924` | Validador 60/0 (LNK, SEM); inventario de la §12 |
| DS-B01-3 | No había un control SUPERADO integral con Git real | Control sintético completo. Corrección del vínculo de la evidencia EQUIPO (ver la nota) | `d83d924` | DS-B01-3a a DS-B01-3e |
| B01-N01 | Una revocación válida cuya evidencia es una ruta de H (S §5.8.1) daba NO SUPERADO con una falla, y su retirada pasaba limpia | La regla de decisión y la historia juzgan la revocación con el árbol de su H | `badb1f5` | B01-N01a (caso legítimo) y B01-N01b |
| B01-N02 | Una revocación completada por un commit que solo añade la determinación escapaba de la historia, que solo seguía el estado | La historia sigue las dos rutas del registro | `badb1f5` | B01-N02a (caso legítimo) y B01-N02b |
| B01-N03 | Se admitían desfases como `+00:99` | Desfase de RFC 3339: horas de 00 a 23 y minutos de 00 a 59 | `badb1f5` | B01-N03, B01-N03b (`+14:00` y `-00:00` se admiten) y B01-N03g |
| B01-N04 | X3–X5 admitían una línea con forma canónica cambiada fuera del ámbito de su espejo. En un documento de gobierno, fuera de su bloque de estado, SEM no mira, así que una afirmación REVOCADO o SUPERADO podía aparecer ahí después de H | Toda línea cambiada tiene que estar dentro del ámbito del espejo en los dos textos | `badb1f5` | B01-N04a, B01-N04b, B01-N04c y B01-N04d (caso legítimo) |

**Nota sobre el vínculo de la evidencia EQUIPO (`d83d924`).** Ese vínculo comparaba el documento del gate con `doc_status_only()`, que rechaza cualquier cambio de la línea E2. SUPERADO cambia E2, así que la evidencia de FG-02, FG-03 y FG-10 nunca podía vincularse y DS-B01-3a era inalcanzable. Ahora aplica `canonical_only()`, que son X3–X5 de H §5.5, y no repite el delta, que se comprueba una vez para el candidato. No relaja nada: X3–X5 es exactamente lo que H §5.5 admite.

### 10.2 Límites

- **Historia local.** La permanencia se lee en la historia local de la rama, desde la base. Si alguien reescribe esa historia y quita los commits del registro, con un rebase o un reset, el validador solo no lo detecta. Lo protegen el anclaje en la rama de H, la auditoría y el contrato 10, que no permite `push` ni `force` sin autorización.
- **Controles positivos.** Los de SUPERADO y REVOCADO son sintéticos. Solo existen en clones desechables (AC-11) y no son actos del equipo.
- **Omisiones.** Dos casos de enlaces simbólicos (AF5-M01-G06 y G07) se omiten en Windows por falta de privilegio, como en la línea base. No cuentan como correctos.

### 10.3 Ejecuciones

Los logs completos están fuera de Git, en `experimental-20261110/evidencias/`, en la ruta indicada.

| Ejecución | Código | Resultado | Log |
|---|---|---|---|
| RED de las correcciones del 10/11 | `a0f6dd4` más las pruebas nuevas | `test_f36sbx_b01` 39/18 | `correcciones-20261111/b01/01-red-auditoria.log` |
| GREEN de `d83d924` | `d83d924` | B-01 57/0; memoria 547/0; Git real 113/0 con 2 omitidos; validador 60/0 | `correcciones-20261111/b01/03-*.log` |
| RED de los restos | `d83d924` más las pruebas nuevas | 60/8: B01-N01a, N01b, N02b, N03, N03g, N04a, N04b y N04c | `correcciones-20261112/b01/01-red-restos.log` |
| GREEN de los restos | El árbol de `badb1f5`, antes del commit | 68/0 | `correcciones-20261112/b01/02-green-restos.log` |
| RED de todo el delta frente al candidato auditado | Pruebas de `badb1f5` con el validador de `a0f6dd4`, en un clon desechable | 42/26: cada falla es un hallazgo de esta tabla | `correcciones-20261112/b01/04-red-delta-a0f6dd4.log` |
| Batería completa, árbol limpio | `badb1f5` | Validador 60/0 con R = NO SUPERADO; B-01 68/0; memoria 547/0; Git real 113/0 con 2 omitidos; tres sondas sin discrepancias | `correcciones-20261112/b01/10-bateria-badb1f5/` |
| Metapruebas focales B-01 | `badb1f5` | Línea base sin fallas; 19 de 21 detectadas, 2 supervivientes (§6). Una primera ejecución se interrumpió a mano y se descarta (`…/10-bateria-badb1f5/08-meta-ablaciones-B-01.INTERRUMPIDA.log`) | `correcciones-20261112/b01/11-meta-badb1f5/` |
| RED de B01-M03b | Pruebas de `17c7af2` con el validador de `a0f6dd4`, en un clon desechable | Las 4 variantes de B01-M03b fallan (42/30) | `correcciones-20261112/b01/05-red-m03b-a0f6dd4.log` |
| Batería completa y las dos ablaciones vueltas a armar | `17c7af2` | validador 60/0; B-01 72/0; memoria 547/0; Git real 113/0 con 2 omitidos; tres sondas sin discrepancias; ablaciones: 2 de 2 detectadas (B01-M03b en sus 4 variantes; B01-H01a a B01-H01d, B01-N01b y B01-N02b) | `correcciones-20261112/b01/12-bateria-17c7af2/` |

## 11. Propuestas técnicas para S (no adoptadas)

Ninguna cambia S. El contrato sigue siendo S v2.2 (blob `a7ef0135…`), y las propuestas son para una S v2.3, que tendría que auditarse antes de servir como contrato de H. El candidato ya aplica la interpretación de cada propuesta. Elegir entre las opciones de P-02 corresponde al equipo, no a quien implementa ni a quien audita.

| ID | Tema | Texto propuesto | Efecto en las pruebas |
|---|---|---|---|
| P-01 (DS-B01-1) | `candidate_commit` en una revocación sin evidencia EQUIPO previa | En §5.8.2: «X2-R se aplica junto con la transición de `candidate_commit` de nulo a H que X2 ya admite. Sin `candidate_commit` = H, la revocación no es vinculable y falla cerrado» | Ninguno en el código. Deja fijados S-T18 a S-T21, que registran `candidate_commit` = H, y el caso de revocación sin él (NO SUPERADO y falla) |
| P-02 (DS-B01-2) | Prioridad entre I-11 y S §3 | **A** (la del candidato): con una revocación válida registrada, en el árbol o en la historia, R = REVOCADO aunque falle otra comprobación de GATE, y el validador falla igualmente. **B:** cualquier falla previa de GATE fuerza NO SUPERADO, también con revocación | **Con A**, DS-B01-2, B01-H01a a B01-H01d, B01-N01b, B01-N02b y DS-B01-3e esperan REVOCADO, como hoy. **Con B**, esos casos esperarían NO SUPERADO, y la permanencia seguiría fallando. En las dos, F37-SBX queda BLOQUEADA: solo cambia qué estado no habilitante declaran los espejos |
| P-03 (B01-H01) | Mecanismo de I-11 | «La permanencia se comprueba en la historia de la rama posterior a la base, en los commits que tocan el estado del gate o la determinación. Una revocación válida frente a su H en cualquiera de ellos tiene que conservarse sin cambios. Si la historia no se puede leer, falla cerrado» | B01-H01a a B01-H01d, B01-N01b, B01-N02b y DS-B01-3e. Con el límite de la §10.2 |
| P-04 (B01-N03) | Formato de `effective_from` | «Instante de RFC 3339 con desfase numérico: horas de 00 a 23 y minutos de 00 a 59» | B01-M01, B01-N03, B01-N03b y B01-N03g |
| P-05 (B01-N04) | Ámbito de X3–X5 | Donde H §5.5 dice «la línea canónica»: «la línea canónica dentro del ámbito de su espejo (E2 a E7); una línea con la misma forma fuera de él es un cambio material» | B01-N04a a B01-N04d |

## 12. Inventario de citas del validador (AC-08)

Búsqueda sobre `badb1f5` más este informe: `git grep -n -e 87ad2f6f -e 47d2f47d -e 4508e6d6 -e 399a3eca`.

| Dónde | Valor | Clase | Tratamiento |
|---|---|---|---|
| S, cabecera (línea 14) | v3 | Histórica: el validador de referencia de las mediciones de S | Se conserva |
| S §5.9.1 (línea 158) | v3 | Histórica: el método de medición | Se conserva |
| S §10, AC-08 (línea 349) | v3 | Normativa: el propio criterio | Se conserva |
| Conclusiones, C-15 (línea 39) | v3 | Histórica, acotada a `4a2b2d7` y `2f6d0e0` | Se conserva. No describe esta rama |
| Este informe, §1 | v3 y los tres del candidato | Operativa (vigente, `399a3eca…`) e histórica (los anteriores) | Actualizado |
| README del paquete, «Validación» | Ninguno: remite a este informe | Instrucción operativa | Remite aquí desde `d83d924` |

Fuera del paquete, `CLAUDE.md`, `README.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md` no citan ningún hash del validador. Para el candidato, AC-08 queda cumplido: el hash vigente consta en el único documento operativo que lo cita, y las citas de v3 se conservan como históricas, sin fingir mediciones nuevas.
