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
| Validador v3 (histórico) | SHA-256 `87ad2f6fed43dd5ae4f0c4baf8721de0a2be71e0efacdb27c8d1f514ea3563ec` |
| Validador del candidato | SHA-256 `47d2f47d413f607b6947d4ce994847a3563921513d6f953ccd55fb8848e6b928` |

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

## 5. Criterios de aceptación

| ID | Estado | Evidencia o falta |
|---|---|---|
| AC-01 | **No cumplido** | D-02b no emitida; P-S1 (D-10) pendiente |
| AC-02 | Cumplido para la batería nueva | RED de §4. El plan de pruebas de H (`1d5d6aa`) no se portó entero: sus casos están representados en S-T01 a S-T22 y en la batería adaptada |
| AC-03 | **Parcial** | GREEN de las tres baterías. Metapruebas declaradas, pero **sin ejecutar**: la ejecución se detuvo por falta de memoria (§6) |
| AC-04 | Cumplido | 59/0 en la rama; S-T11 en un clon |
| AC-05 | Cumplido | `git diff --name-only 55f758e HEAD` dentro del perímetro; incluye `sondas-b01/` (S-T22a); sondas ejecutadas desde el árbol |
| AC-06 | Cumplido | S-T15 |
| AC-07 | Cumplido con el nombre provisional | S-T13, S-T14 y S-T17 |
| AC-08 | Parcial | El SHA-256 nuevo consta aquí. S y las conclusiones citan v3 como el validador de sus mediciones (histórico). Falta decidir si algún otro documento debe citar el nuevo |
| AC-09 | Cumplido | AC-09a a AC-09d y M09 |
| AC-10 | Cumplido en clones | S-T01 a S-T03, S-T02b, S-T02c y S-T18 a S-T21 sobre el validador nuevo |
| AC-11 | Cumplido | `gate/evidencia/` no existe en la rama |
| AC-12 | Cumplido | S-T09 y S-T10 |
| AC-13 | Registrado | §7 |
| AC-14 | Cumplido | DEP: solo biblioteca estándar |

## 6. Metapruebas

`meta_f36sbx.py` incluye la batería B-01 y diez ablaciones nuevas:

- las funciones `revocation_errors`, `mirror_errors`, `mirror_lines`, `required_state`, `derived_states`, `identity_errors_h`, `delta_errors_h` y `canonical_only`;
- la degradación de una revocación no vinculada;
- la rama de H en `BRANCHES`.

**Sin resultado.** La ejecución focal (`meta_f36sbx.py ablaciones B-01`) sobre `c96823a` la detuvo el sistema por falta de memoria (0,7 GB libres de 16) antes de imprimir nada. Tampoco se ejecutó la corrida completa. Repetirlas es un paso pendiente (AC-03).

## 7. Integración en `develop` (AC-13, I-14)

Si H se integrara en `develop`, FRZ fallaría allí por diseño, porque `develop` contiene los cambios de runtime de SEG respecto de `b8892af`.

S-T14 lo reproduce con el validador nuevo: una rama con el nombre de H cortada desde `develop` da FRZ «fuera de alcance» y «cambios de runtime» con los archivos de `app/` de SEG, y FG-01 y FG-05 en NO CUMPLE. No es una regresión: el resultado R se lee anclado en la rama de H. Cualquier integración exige la autorización del contrato 10.

## 8. Diferencias pendientes con S v2.2

| ID | Diferencia | Tratamiento en el candidato |
|---|---|---|
| DS-B01-1 | X2-R no incluye `candidate_commit`. Una revocación registrada sin evidencia previa no dice qué commit es H, y el validador solo identifica H por `candidate_commit` | Falla cerrado: una revocación exige `candidate_commit` = H (la transición de nulo a H que X2 ya admite). Hay que aclararlo en S |
| DS-B01-2 | Con una revocación válida y vinculada, una falla ajena (por ejemplo, un archivo sin citar en `gate/evidencia/`) hace fallar el validador, pero deja R = REVOCADO (I-11). S §3 dice que R se fuerza a NO SUPERADO ante cualquier falla previa de GATE | Se aplica I-11. Hay que decidir cuál prevalece |
| DS-B01-3 | No hay control positivo SUPERADO con la evidencia completa de FG-02, FG-03, FG-10 y FG-12 en un clon (S-T05) | SUPERADO se cubre en memoria (evaluate_gate, espejos y REQUIRED_STATE). Falta el control con Git real |
| DS-B01-4 | La variante RD (T-08 (ii)) y T-06 | No implementadas, conforme a la propuesta de S |
| DS-B01-5 | La cabecera de `docs/PROGRESS.md` conserva una foto fechada («F36-SBX-GATE NO SUPERADO») fuera del bloque de estado | No es una afirmación «sujeto = estado». Queda como dato histórico |

## 9. Lo que no hace este candidato

- No registra evidencia, votos, decisiones ni estados.
- No fija H.
- No autoriza F37-SBX.
- No cambia el contrato de evidencia v4, la G0 real, ADR-005, el alcance C, RF-23 ni RF-29.
