# F36-SBX — Especificación S del sucesor B-01

> **CANDIDATA A AUDITORÍA — NO IMPLEMENTADA. Versión 2.2** (09/11/2026), en la rama local `feature/continuacion-f36-f40`, desde `f5003c9`. La 2.2 corrige los cuatro hallazgos del dictamen de Codex sobre la 2.1 (blob `8ae8b5bc…`):
>
> - **S-M01:** limita T-09 a la variante (a-ii), como propuesta para decisión (§5.9.3).
> - **S-M02:** cierra el delta de revocación después de H (§5.8.2).
> - **S-M03:** mueve las sondas al paquete (§5.9.5).
> - **S-L01:** separa en §11 el contrato 10, D-11, D-10 y D-02b.
>
> La 2.1 añadió las sondas ejecutables de §5.9.4 y corrigió AC-02, que contradecía AC-05. La versión 1 (07/11/2026, `feature/entrega-academica-demo`) se conserva en la historia. La v2 aterriza T-09 con mediciones reales del validador (§5.9), añade criterios de aceptación (§10), pruebas de implementación (§8, S-T11 a S-T17), dependencias de D-10, D-11 y D-02b (§11) y los puntos de auditoría (§12). Revisa la especificación de `1d5d6aa:docs/academico/f36-sbx/preparacion-gate/F36SBX_Especificacion_Sucesor_B01.md` (en adelante, «la especificación de H») según Q2 §8, §10 y §12, adoptada por RR-001 (`5036393`).
>
> **No modifica** `validate_f36sbx.py`, sus pruebas, el estado del gate ni el gobierno. Implementarla exige D-02b, que **no está emitida**: sin facultades delegadas utilizables (RR-001 §4), D-02b solo puede emitirse por el mecanismo colegiado. Estado vigente: F36-SBX = EN DISEÑO, F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA.
>
> Validador de referencia: `validate_f36sbx.py` con SHA-256 `87ad2f6fed43dd5ae4f0c4baf8721de0a2be71e0efacdb27c8d1f514ea3563ec`, idéntico en `4a2b2d7`, `9dd76c4`, `5036393` y `2f6d0e0`. Las referencias `:NNNN` son de ese archivo.

## 0. Qué cambia frente a la especificación de H

| # | Cambio | Motivo |
|---|---|---|
| S-1 | Precondición: **D-10 determinada** antes de D-02b (§2) | Si F36-SBX quedó revocada (D10-2), este gate ya no puede superarse y B-01 no tiene objeto. Si D-10 sigue abierta, no se sabe si la puerta que B-01 habilita está vigente |
| S-2 | Nueva decisión **T-09**: base, anclaje y la regla FRZ después de SEG (§5.9) | Un H que descienda de `develop` contiene los 5 archivos de `app/` y las 6 pruebas de SEG. FRZ falla frente a `b8892af`, FG-01 y FG-05 se recalculan NO CUMPLE, y el gate nunca llegaría a SUPERADO con evidencia válida. La especificación de H no lo trataba, porque es anterior a SEG |
| S-3 | **T-05 cerrado:** formato del evento de revocación y estado REVOCADO en los espejos (§5.8) | D10-2 necesita poder registrarse. El v3 no puede representar REVOCADO (`allowed_states()`, `:1290`) |
| S-4 | **T-08 según Q2:** dos variantes del registro de los criterios EQUIPO (§6) | Q2 §8 y §12. La variante unipersonal de Q (`061ba68`) queda sustituida, no se implementa |
| S-5 | **Orden de los registros** de Q2 §8 (§7) | Corrige el D-02c histórico de `1d5d6aa` (UNI-M04, UNI-M05 y UNI-L02), que hacía depender FG-03 de un gate ya superado |
| S-6 | Se conserva FG-12 en NO APLICA cuando el gate lo admite | Sin cambios de regla; se explicita para que ninguna variante lo pierda |
| S-7 | **T-09 medido** (v2): siete sondas del validador fijan qué base y qué rama admiten un H válido (§5.9.1) | La v1 argumentaba T-09 sin medirlo. Las sondas muestran que todo el expediente posterior a SEG cabe en FRZ sobre `55f758e` |
| S-8 | Invariante **I-14**: el resultado del gate se lee anclado en la rama de H (§4) | Integrar H en `develop` hará fallar FRZ allí por diseño, como en F35-SBX (DG-02); no es una regresión del gate |
| S-9 | Criterios de aceptación, pruebas y dependencias explícitos (§8, §10 y §11) | Para que la implementación tenga un «terminado» auditable y quede claro qué espera a D-10, D-11 o D-02b |
| S-10 | **Una sola variante de T-09 en esta versión:** (a-ii), como propuesta para decisión. (a-i) y (b) quedan como alternativas fuera de alcance, con su matriz (§5.9.3) | S-M01: T-04, AC-05, AC-07 y las pruebas solo eran coherentes con (a-ii) |
| S-11 | **X1 y X2 ampliadas para la revocación:** el delta exacto que se admite después de H (§5.8.2) y su sonda con commits sintéticos (§5.8.3) | S-M02: X1 y X2 de H no admitían el documento de determinación ni el cambio de FG-14, de modo que §5.8 y AC-10 eran inalcanzables después de H |
| S-12 | **Sondas dentro del paquete** (`expediente-final/sondas-b01/`), con una sonda del trasplante (§5.9.5) | S-M03: en `docs/academico/preparacion-f36-b01/` quedaban fuera de AC-05 y un H trasplantado no podía llevarlas |
| S-13 | **§11 separa cuatro requisitos:** la autorización del contrato 10, el procedimiento de D-11, la determinación D-10 y la autorización D-02b | S-L01: la 2.1 hacía depender de D-11 una obligación que el contrato 10 ya impone hoy |

Lo que no cambia de la especificación de H se mantiene en su redacción. Esto incluye el comportamiento verificado (§2 de H), las superficies protegidas (§3 de H), las invariantes I-1 a I-10 (§4 de H), los espejos E1–E7 y su requisito previo (§5.2 de H), el vocabulario cerrado (§5.3), `REQUIRED_STATE(R)` (§5.4), las excepciones X3–X5 (§5.5), la identidad de H (§5.6), la sustitución de `:2877` (§5.7) y los riesgos (§8 de H). X1 y X2 se conservan y §5.8.2 las amplía solo para la revocación. Aquí se resumen solo para que S se audite sin abrir otro commit.

## 1. Propósito y límites

Con el validador vigente, el gate **no puede** pasar a SUPERADO aunque toda la evidencia sea auténtica: `rule_gate()` exige NO SUPERADO (`:2877`), `allowed_states()` solo admite ese resultado (`:1290`) y el vínculo invalida cualquier cambio posterior al candidato fuera de la evidencia y de la columna Estado (`binding_errors()`, `:2293`, y `doc_status_only()`, `:2275`).

B-01 hace que el validador reconozca SUPERADO o REVOCADO **solo** cuando el contrato lo produce, recalculándolo desde la evidencia, y que todas las fuentes que declaran el estado lo reflejen igual.

B-01 **no** registra evidencia, no decide EI ni dependencias, no aprueba ADR, no implementa capacidades de F37-SBX, no cambia el contrato de evidencia v4 y no toca la G0 real, ADR-005, los datos reales, el alcance C, RF-23 ni RF-29.

## 2. Precondiciones de D-02b

| ID | Precondición | Estado al 07/11/2026 |
|---|---|---|
| P-S1 | D-10 determinada (D10-1, o D10-3 con una autorización nueva hacia adelante que cubra B-01). Con D10-2, B-01 no procede: haría falta un gate nuevo | Pendiente. Borrador en `decisiones-d10-d11/` |
| P-S2 | S auditada sobre un commit fijo, sin BLOCKER, HIGH ni MEDIUM que exija corrección | Pendiente. Esta versión es la candidata |
| P-S3 | T-01 a T-09 decididas, o delegadas expresamente a la implementación dentro de las opciones de S | No emitidas |
| P-S4 | Quién emite D-02b: con DF-02 y DF-03 vigentes que incluyan B01-1, un RD de Luis anclado a S, a su informe y a RR-001; sin ellas, el mecanismo colegiado | Sin facultades delegadas utilizables: mecanismo colegiado |

## 3. Resultado derivado y espejos (resumen de H §5.1–§5.7)

- **R** es `evaluate_gate()` (`:2722`) sobre el estado y la evidencia, forzado a NO SUPERADO ante cualquier falla previa de la regla GATE. Vale NO SUPERADO, SUPERADO o REVOCADO.
- **Espejos cerrados:**
  - E1, `declared_result`;
  - E2, una línea canónica del gate;
  - E3, dos viñetas del README del paquete;
  - E4–E7, dos viñetas en cada documento de gobierno.

  Fuera de ellos, solo se admiten los estados históricos.
- **Antes de H**, cada espejo debe tener una sola afirmación por sujeto. Hoy los cuatro documentos de gobierno repiten el estado en el párrafo de F36 (D-07).
- **`:2877` se sustituye** por «E1–E7 declaran exactamente R». Cualquier diferencia, en cualquier sentido, es una falla.
- **Después de H** solo cambian X1–X5, comprobadas línea a línea. X2 se compara campo a campo con el blob de H. Con una revocación, X1 y X2 admiten además el delta cerrado de §5.8.2, y nada más.

## 4. Invariantes que S añade

| ID | Invariante |
|---|---|
| I-11 | R = REVOCADO prevalece sobre cualquier otro resultado y no se deshace en el mismo gate. Para continuar, haría falta un gate nuevo con su autorización |
| I-12 | La base y el perímetro de FRZ no se mueven para «regularizar» hechos anteriores. Cualquier cambio de anclaje es prospectivo, explícito (T-09) y posterior a D-10 |
| I-13 | La variante del registro (3/3 o RD) se fija en el estado del gate de H y no cambia después de H |
| I-14 | El resultado R vale anclado en la rama de H, sobre su árbol. Validar después de integrar H en otra rama que contenga cambios fuera de FRZ (por ejemplo, `develop` con SEG) falla por diseño y no altera R ni constituye una regresión |

## 5. Puntos nuevos o cerrados

### 5.8 Revocación (T-05, cerrado)

#### 5.8.1 Formato

`revocation` pasa de «nulo o cualquier objeto» a un formato cerrado:

```json
{
  "revocation": {
    "date": "AAAA-MM-DD",
    "effective_from": "AAAA-MM-DDThh:mm:ss-05:00",
    "ground": "charter_7_1 | charter_7_2 | charter_7_3 | charter_7_4 | gate_5_tei21 | gate_5_retirada",
    "determination": "docs/academico/f36-sbx/gate/evidencia/REVOCACION_DETERMINACION.md",
    "evidence": ["SHA-256 o rutas que ya existen en H"]
  }
}
```

Las claves son exactamente esas cinco:

- `date` es la fecha del registro, con formato `AAAA-MM-DD`, y no puede ser anterior a la fecha del commit H.
- `effective_from` es un instante con desfase horario. Puede ser anterior a la fecha del registro, porque el registro es declarativo (D-10 §5.4); el validador no lo juzga.
- `determination` es exactamente la ruta fija de §5.8.2.
- `evidence` es una lista no vacía. Cada entrada es un SHA-256 en minúsculas o una ruta que ya existe en el árbol de H, sin añadir otra.

Con `revocation` válido:

- R = REVOCADO;
- F37-SBX = BLOQUEADA en todos los espejos;
- `allowed_states()` admite REVOCADO **solo** en los espejos.

Con `revocation` mal formado, falla cerrado: NO SUPERADO y una falla.

#### 5.8.2 Delta permitido después de H

Las excepciones X1 y X2 de H (§5.5 de H) no admitían ni el documento de determinación ni el cambio de FG-14, que la regla GATE recalcula NO CUMPLE en cuanto `revocation` deja de ser nulo (`:2805`). Sin esta ampliación, una revocación registrada después de H fallaría el vínculo (`binding_errors()`, `:2293`) y AC-10 sería inalcanzable. S amplía X1 y X2 así, y solo así:

| ID | Ruta | Qué puede cambiar | Comprobación |
|---|---|---|---|
| X1 | `gate/evidencia/` | Lo de H: `FG-02.json`, `FG-03.json`, `FG-10.json` y `FG-12.json`, más el informe que cita FG-02 | Vigente (regla GATE y AF5) |
| **X1-R** | `docs/academico/f36-sbx/gate/evidencia/REVOCACION_DETERMINACION.md` | Se **añade** el documento de determinación. Es un blob regular `100644`, versionado en el commit validado, ausente en H y citado exactamente por `revocation.determination` | **Nueva**. Solo con la condición C-R |
| X2 | `gate/f36sbx_gate_state.json` | Lo de H: `candidate_commit`, el `status` y la `evidence` de FG-02, FG-03, FG-10 y FG-12, `f37_authorized_ei`, `declared_result` y `revocation` | Campo a campo con el blob de H |
| **X2-R** | `gate/f36sbx_gate_state.json` | Tres campos, con estas transiciones exactas: `revocation` de nulo a un evento válido (§5.8.1); `criteria[FG-14].status` de CUMPLE a NO CUMPLE; `declared_result` a REVOCADO | **Nueva**, campo a campo. Solo con la condición C-R |
| X3 | `F36SBX_Gate_Sucesor.md` | Sin cambios de regla: la celda Estado de FG-14 pasa de CUMPLE a NO CUMPLE dentro de la columna Estado, y la línea E2 declara REVOCADO | `doc_status_only()` generalizada (H §5.5) |
| X4 y X5 | README del paquete y los cuatro documentos de gobierno | Sin cambios de regla: sus líneas canónicas declaran REVOCADO y F37-SBX = BLOQUEADA | Ídem |

**Condición C-R.** X1-R y X2-R se habilitan solo si se cumplen las cuatro condiciones:

1. `revocation` es nulo en el blob de H.
2. `revocation` es un evento válido según §5.8.1 en el árbol validado.
3. El documento existe en la ruta fija y es exactamente el que cita `determination`.
4. Las tres transiciones de X2-R se dan juntas.

Si falta cualquiera de ellas, la ruta de X1-R y los tres campos de X2-R son cambios materiales posteriores a H y fallan como cualquier otro.

**Lo que no se relaja.** Ningún otro campo, criterio ni ruta del paquete o de las herramientas puede cambiar. Tampoco un segundo archivo en `gate/evidencia/`, una clave adicional en `revocation`, el FG-14 sin revocación, ni una determinación sin evento o en otra ruta. Se mantienen la identidad de H (H §5.6), el vínculo con su commit y las herramientas iguales a H. REVOCADO prevalece y no se deshace (I-11).

**Revocación después de SUPERADO.** El delta admitido es la unión de lo que X1 y X2 ya admiten para SUPERADO con X1-R y X2-R. Ninguno de los dos deltas amplía al otro: para pasar de SUPERADO a REVOCADO cambian exactamente los mismos tres campos y la misma ruta.

#### 5.8.3 Sonda de la especificación

[`sonda_revocacion.py`](sondas-b01/sonda_revocacion.py) prueba que esta definición separa el delta permitido de los demás. La prueba se hace en un clon desechable, con un H sintético desde `55f758e` y un commit sucesor por caso. La sonda codifica §5.8.2 como definición de referencia; no ejecuta ni modifica el validador.

| Caso | Delta frente al H sintético | Resultado del 09/11/2026 |
|---|---|---|
| S-T18 | Exactamente el de §5.8.2: determinación, los tres campos y la celda de FG-14 | Admitido |
| S-T19 | S-T18 más un archivo en `gate/evidencia/`, o más un archivo del paquete | Rechazado: «ruta fuera del delta» (2 casos) |
| S-T20 | S-T18 más `f37_authorized_ei` cambiado, FG-13 en NO CUMPLE o una clave adicional en `revocation` | Rechazado: «campo fuera del delta» o «claves distintas» (3 casos) |
| S-T21 | FG-14 en NO CUMPLE sin revocación; la determinación sin evento; o un evento que cita otra ruta | Rechazado (3 casos) |

La sonda dio 9 conformes y 0 discrepancias. Dos ablaciones de la definición de referencia, hechas sobre copias fuera del repositorio, la hacen fallar con código 1:
- **Sin la comprobación de rutas:** 3 discrepancias (S-T19 ×2 y S-T21 con la determinación).
- **Con cualquier campo admitido:** 3 discrepancias (S-T20 ×2 y S-T21 con FG-14). **No es la validación funcional de AC-10**: esa corresponde a la implementación de B-01, con su RED y su GREEN (S-T01 a S-T03 y S-T18 a S-T21 sobre el validador nuevo). Las líneas canónicas E2 a E7 quedan fuera de la sonda, porque su texto depende de T-01 y D-07. Tampoco cubre la revocación posterior a SUPERADO.

### 5.9 Base, anclaje y FRZ después de SEG (T-09, nuevo)

**Hecho.** SEG-01 a SEG-04 cambiaron 5 archivos de `app/` y 6 de `tests/` en `develop` (`2e53786`, `2546297` y `9dd76c4`). Un H que descienda de `develop` hereda esos cambios frente a `b8892af`, y FRZ falla en dos comprobaciones. En `develop` solo cuentan las rutas de SEG. En las ramas de la entrega y de su continuación se suman además sus cambios de producto, que alargan esas dos listas sin añadir comprobaciones fallidas. Esas ramas dan 55/4 por esa razón y por el anclaje de rama (V-7).

#### 5.9.1 Mediciones (08/11/2026)

El validador de referencia (SHA-256 `87ad2f6f…`) se ejecutó con `python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py` en worktrees temporales, que se eliminaron al terminar. Para leer una rama admitida se hizo checkout de las ramas locales existentes `main` y `develop`, sin mover ninguna ref. Los cambios de H se superpusieron solo en el árbol de trabajo, con `git checkout <commit> -- <ruta>`, que el validador cuenta como cambio (FRZ compara la base con el índice, más lo modificado y lo no versionado). No se creó ningún commit.

| Sonda | Árbol | Rama que lee el validador | Resultado | Fallas |
|---|---|---|---|---|
| V-1 | `main` = `55f758e`, árbol `01dc59a8…`, idéntico al de AF5 `4a2b2d7` | `main` | **59/0** | — |
| V-2 | `develop` = `9dd76c4`, con SEG | `develop` | 56/3 | FRZ por alcance (44 cambios, entre ellos `app/`); FRZ por runtime; GATE, por FG-01 y FG-05 |
| V-3 | V-1 más los cambios de la H preliminar `1d5d6aa` (14 rutas, todas del paquete) | `main` | **59/0** | — |
| V-4 | V-2 más el paquete de `1d5d6aa` | `develop` | 56/3 | Las mismas tres de V-2 (52 cambios) |
| V-5 | V-1 más **todo** `docs/academico/f36-sbx/` de `f5003c9`: Q2, RR-001, D-10, D-11, S v1, conclusiones y prototipo de ML-02 | `main` | **59/0** | — |
| V-6 | `55f758e` y `1d5d6aa` en HEAD desacoplado | `HEAD` | 57/2 | FRZ, por rama no admitida; GATE, por FG-01 y FG-05 |
| V-7 | `f5003c9`, base de esta rama, con el nombre `feature/continuacion-f36-f40`. Desde la 2.2 se mide sobre ese commit fijo, para que la sonda no dependa del árbol desde el que se ejecuta | la rama | 55/4 | Rama no admitida, FRZ por alcance, FRZ por runtime y GATE (FG-01 y FG-05) |

**Hechos estructurales:**

- El subárbol `docs/academico/f36-sbx` es idéntico en `55f758e` y en `9dd76c4` (`41433246…`), y también lo es `docs/academico/tools/f36sbx` (`0bcdb843…`).
- Los cuatro archivos de gobierno (`GOV_FILES`, `:58`) son iguales en ambos commits.
- Los 12 commits de `9dd76c4..2f6d0e0`, de la reconciliación tras SEG a los borradores de D-10 y D-11, cambian 19 rutas, todas dentro del paquete.
- `b8892af` es ancestro de `main` y de `develop`. Ninguna de las dos ramas desciende de la otra: `55f758e` es el merge de AF5 en `main` y no contiene SEG.
- `BRANCHES` (`:38`) admite exactamente `feature/f36-sbx-authorization-design`, `develop` y `main`. La primera está en `4a2b2d7`, con el mismo árbol que `55f758e`.

#### 5.9.2 Efecto sobre la selección de H

1. **Mientras `BASE = b8892af` y FRZ no cambie, H no puede descender de `develop`.** V-2 y V-4 muestran que FRZ falla por SEG, sea cual sea el contenido de H, y R queda NO SUPERADO aun con evidencia auténtica (S-T04).
2. **H puede construirse sobre `55f758e` como trasplante del paquete.** V-5 muestra que el expediente completo posterior a SEG cabe en FRZ, y que no hay conflicto: el subárbol de partida es el mismo en las dos ramas. El trasplante consiste en llevar `docs/academico/f36-sbx/` del candidato de diseño auditado y los cambios del validador (`tools/f36sbx`), nada más. **No se llevan** los cambios de producto, como los de esta rama o los de SEG.
3. **La rama de H tiene que estar admitida.** Esta versión especifica una sola manera: **(a-ii)**, crear una rama nueva desde el commit `55f758e` y admitirla en `BRANCHES` dentro de B-01 (T-04). Es reversible, no mueve ninguna rama existente y aísla H. Las demás maneras medidas o consideradas quedan fuera de esta versión (§5.9.3):
   - **(a-i)** fijaría H en `feature/f36-sbx-authorization-design`, moviendo la rama que ancla AF5 y que usa el checkout principal;
   - **(a-iii)** exigiría integrar H en `main` antes de validarlo, que es una operación del contrato 10.
4. **Ventana temporal.** Si SEG llega a `main` antes de fijar H, `main` deja de servir como base, porque daría lo mismo que V-2. Por eso (a-ii) parte del **commit** `55f758e` y no de la ref móvil `main`.
5. **Después de H.** Integrar H en `develop` hará fallar FRZ allí por diseño (I-14), como hoy en `develop` y como en F35-SBX (DG-02).

#### 5.9.3 Variante admitida en esta versión y alternativas

**S v2.2 especifica una sola variante: T-09 (a-ii), como propuesta para decisión.** No está aprobada ni emitida: T-09 y T-04 siguen NO EMITIDAS (§9) y las decide D-02b por el mecanismo de P-S4. T-04, AC-05, AC-06, AC-07 y las pruebas de §8 están escritos solo para (a-ii).

(a-i) y (b) son alternativas **fuera del alcance** de esta versión. Si el equipo prefiriera una de ellas, haría falta una versión nueva de S con su propia base, sus ramas, sus criterios y sus pruebas, y una auditoría nueva. Esta versión no las prepara ni las descarta como decisión.

| Variante | `BASE` | Punto de partida de H | `BRANCHES` | Criterios y pruebas aplicables | Estado en S v2.2 |
|---|---|---|---|---|---|
| **(a-ii)** | `b8892af`, sin cambios | Commit `55f758e`, con el paquete y el validador trasplantados | Las tres vigentes y **una** rama nueva de H (T-04) | AC-01 a AC-14; S-T01 a S-T15 y S-T17 a S-T22 | **Única variante especificada.** Propuesta para decisión, NO EMITIDA |
| (a-i) | `b8892af` | `4a2b2d7`, en `feature/f36-sbx-authorization-design`, que ya está admitida | Las tres vigentes, sin T-04 | No aplican AC-07, S-T13, S-T14 ni S-T17 en su forma actual. AC-05 se mediría sobre otro punto de partida | Fuera del alcance. Mueve la rama que ancla AF5 |
| (b) | Un commit posterior a SEG, por ejemplo `9dd76c4` | Un descendiente de esa base | Sin determinar | Cambiarían AC-05, AC-06 y S-T15. S-T16 muestra que en la línea de `main` falla «la base es ancestro de HEAD». Exigiría D10-1 | Fuera del alcance. Cambia FG-05 hacia adelante |

Las variantes medidas que no se proponen se mantienen como **descartadas**, con su motivo:

| Variante | Motivo |
|---|---|
| (a-iii): validar H en `main` | Exige una operación del contrato 10 (integrar H) antes de validarlo |
| (c): excluir de FRZ el mantenimiento fuera del paquete | Debilita TEI-22 y convierte una cuestión de D-10 en una excepción de código |
| (d): H desde `develop` sin cambiar FRZ ni la base | Inviable: R nunca llega a SUPERADO (V-2 y V-4) |

**Por qué (a-ii).** FRZ pasa sin mover la base (V-1, V-3 y V-5, y S-T11). Es coherente con la regla «Anclaje» del README del paquete (`06e933e`, 26/10/2026) y con I-12. Es reversible, no exige determinar D-10 para elegir la base y no toca ninguna rama existente. Es una justificación técnica, no una decisión del equipo.

#### 5.9.4 Sondas ejecutables (09/11/2026)

[`sondas_t09.py`](sondas-b01/sondas_t09.py) repite V-1 a V-7 y observa hoy lo que FRZ haría en S-T04 y S-T11 a S-T17. Clona en un directorio temporal, no mueve ninguna ref y borra el clon. No modifica el validador: las sondas con la rama «admitida» añaden el nombre a `BRANCHES` solo en memoria, en el proceso de la sonda, sobre el código del clon. El nombre `feature/f36-sbx-h-sonda` es de prueba: la rama real de H es T-04, NO EMITIDA.

| Sonda | Montaje | Resultado | Fallas |
|---|---|---|---|
| V-1 a V-7, S-T04 | Las de §5.9.1 | Iguales a §5.9.1; S-T04 = V-2 | — |
| S-T15 | `BASE` | `b8892af` | — |
| S-T17 | `BRANCHES` hoy | Las tres ramas vigentes | — |
| S-T11, RED | Rama de H desde `55f758e`, con `docs/academico/f36-sbx/` de `f5003c9`, **sin** admitir | 57/2 | Rama no admitida; GATE (FG-01 y FG-05) |
| **S-T11** | Lo mismo, con la rama admitida | **59/0**, R = NO SUPERADO | — |
| S-T12 | S-T11 más un archivo en `app/`, en `tests/` o `composer.json` (tres sondas) | 56/3 cada una | FRZ por alcance, FRZ por runtime y GATE |
| S-T13 | El árbol de S-T11, con otra rama no admitida | 57/2 | Rama; GATE |
| S-T14 | Rama con el nombre admitido, cortada desde `develop` | 56/3 | FRZ por alcance, FRZ por runtime y GATE |
| S-T16 | `main` con `BASE = 9dd76c4` | 53/6 | «La base es ancestro de HEAD», FRZ por alcance y por runtime, GATE, identidad de la base y la invariante de evidencia «el candidato desciende de la base» |

**Qué acredita la sonda de T-09:**
- Con el validador v3 y la rama admitida solo en memoria, FRZ acepta un árbol que parte de `55f758e` y lleva el paquete completo (S-T11). Admitir la rama es el único cambio que FRZ necesita para ese árbol.
- FRZ rechaza ese mismo árbol con una ruta de producto o de dependencias (S-T12), con otra rama (S-T13) o si parte de `develop` (S-T14).
- S-T16 es evidencia de por qué (b) queda fuera de alcance; no es una prueba de la implementación.

**Qué no acredita:**
- Que H vaya a superar el gate. R sigue en NO SUPERADO, porque falta la evidencia de FG-02, FG-03, FG-10 y FG-12, y el v3 ni siquiera puede representar SUPERADO.
- Nada de la lógica nueva de B-01. S-T01 a S-T03, S-T05 a S-T10 y S-T18 a S-T21 sobre el validador nuevo no se pueden observar hasta implementarla.

**Queda por verificar sobre el futuro H**, una vez fijado:
- **Árbol y rama:** S-T11 a S-T14, con la rama real de T-04 en `BRANCHES` del validador nuevo y no en memoria, y con el árbol real de H y no con el paquete de `f5003c9`.
- **Constantes:** que `BASE` sigue igual (AC-06) y que `BRANCHES` admite exactamente esa rama (AC-07).
- **Inventario y ejecución:** que el inventario de H cabe en AC-05 y que las sondas se ejecutan desde el árbol de H (S-T22).
- **Validación anclada:** la validación anclada en la rama de H (I-14).

#### 5.9.5 Ubicación de las sondas y trasplante (09/11/2026)

Las sondas están en [`sondas-b01/`](sondas-b01/README.md), dentro de `docs/academico/f36-sbx/`, es decir, dentro del perímetro de AC-05. Hasta la 2.1 estaban en `docs/academico/preparacion-f36-b01/`, fuera del paquete: un H trasplantado según (a-ii) no podía llevarlas sin salir de AC-05. Ninguna sonda depende ya de la rama desde la que se ejecuta: V-7 se mide sobre el commit fijo `f5003c9`.

[`sonda_trasplante.py`](sondas-b01/sonda_trasplante.py) comprueba esa ubicación en un árbol aislado. En un clon temporal crea un H de prueba desde `55f758e`, con `docs/academico/f36-sbx/` de la revisión indicada, y hace un commit sintético. Sobre ese árbol comprueba cuatro cosas:

| ID | Comprobación |
|---|---|
| T-1 | `git diff --name-only 55f758e <H de prueba>` cabe en AC-05 e incluye los cuatro archivos de `sondas-b01/` |
| T-2 | Los enlaces relativos de S y del README de las sondas resuelven en ese árbol y no salen del paquete |
| T-3 | El validador del clon, con la rama de prueba admitida solo en memoria, da 0 fallas y R = NO SUPERADO |
| T-4 | `sondas_t09.py` y `sonda_revocacion.py`, lanzados desde ese árbol, salen con código 0 |

Es la sonda de S-T22. El H de prueba es sintético y desaparece con el clon; no fija H.

| Paquete trasplantado (09/11/2026) | T-1 | T-2 | T-3 | T-4 |
|---|---|---|---|---|
| El de esta versión (`--paquete ARBOL`, mismo contenido que el commit de la 2.2) | Conforme: 30 rutas, todas en AC-05, con los 4 archivos de `sondas-b01/` | Conforme | 59/0, R = NO SUPERADO | Las dos sondas, código 0 |
| Contraprueba con el de `5719ebc` (S v2.1, sondas fuera del paquete) | Falla: faltan los 4 archivos | Falla: S enlaza `../../preparacion-f36-b01/`, que no existe en H | 59/0 | Falla: código 2, no hay sondas que ejecutar |

T-3 da 0 fallas en los dos casos: FRZ no detecta que falten las sondas. Por eso AC-05 exige además S-T22.

## 6. Criterios EQUIPO: dos variantes (T-08 según Q2)

| | Variante 3/3 (vigente) | Variante RD (Q2 con delegación) |
|---|---|---|
| Cuándo | Siempre disponible | Solo con RR-001 vigente y DF-02 y DF-03 vigentes que incluyan GATE-1 (FG-03) o GATE-2 (FG-10). Hoy **no disponible** |
| Formato | `gate_version = 3`, esquema `f36sbx-team-evidence/v2`, `approvals` de las tres identidades exactas (`MEMBERS`, `:81`) | `gate_version = 4`, esquema v3: un `decision_record` en lugar de `approvals`, que cita el RD, RR-001, DF-02 y DF-03 con sus fechas, y una FG-02 favorable sobre H. El RD es posterior a las tres |
| FG-02 | Igual en las dos: informe canónico del auditor elegible sobre H, sin quórum propio |
| FG-03 | 3/3 `APRUEBA`, `AUTORIZA_INICIO_F37_SBX`, lista cerrada de EI idéntica a `f37_authorized_ei` y F36-M01 confirmada | RD bajo GATE-1, con las mismas condiciones de contenido. EI-09 solo con F36-M02 confirmada por actos auténticos. GATE-3 no existe |
| FG-10 | 3/3 siempre, nunca NO APLICA | RD bajo GATE-2, solo para declarar que no hay dependencias nuevas. Con dependencias, 3/3 |
| FG-12 | **NO APLICA** si FG-03 no autoriza ninguna EI CONDITIONAL, sin archivo ni votos. Si no, 3/3 con la decisión sobre EI-09 y, con alcance C, un ADR sucesor APROBADO dentro de H | Igual. El ADR y el alcance C no son delegables |

`approval_errors()` (`:2367`) se conserva para la variante 3/3. La variante RD añade `decision_record_errors()`, con su propio RED/GREEN. Ninguna variante relaja la otra (I-13).

## 7. Orden de los registros (Q2 §8)

1. Auditoría de S.
2. D-10 determinada (P-S1).
3. D-02b, por el mecanismo que corresponda (P-S4).
4. Implementación: RED, validador, documentos normativos previos a H (D-07), batería y metapruebas del plan de `1d5d6aa`, más los casos de §8.
5. H fijado, según T-09.
6. FG-02 favorable sobre H.
7. FG-03, FG-10 y FG-12, referidos a H.
8. Registro permitido por el sucesor.
9. Validación anclada.
10. Inicio de F37-SBX, solo si R = SUPERADO.

FG-03 es una entrada del gate: no puede exigir un gate ya superado.

## 8. Casos de prueba que S añade al plan de `1d5d6aa`

| ID | Caso | Esperado |
|---|---|---|
| S-T01 | `revocation` con el formato de §5.8.1 y la determinación versionada en su ruta fija | R = REVOCADO; espejos en REVOCADO y BLOQUEADA; 0 fallas |
| S-T02 | `revocation` sin `determination`, con `ground` desconocido o con un tipo distinto | NO SUPERADO y una falla |
| S-T03 | `revocation` válido y espejos en NO SUPERADO | Falla (I-2) |
| S-T04 | H descendiente de `develop` con SEG, base `b8892af` | FRZ falla; R = NO SUPERADO aun con evidencia válida |
| S-T05 | H en una rama desde `55f758e`, admitida por T-04, con evidencia válida y sintética en un clon | R = SUPERADO; 0 fallas |
| S-T06 | Variante RD con una DF cuya fecha es posterior al RD | Falla |
| S-T07 | Variante RD con FG-10 y dependencias declaradas | Falla: exige 3/3 |
| S-T08 | Variante fijada en H como 3/3 y evidencia con `decision_record` | Falla (I-13) |
| S-T09 | FG-12 en NO APLICA con FG-03 sin EI CONDITIONAL y sin `FG-12.json` | Admitido |
| S-T10 | FG-12 en NO APLICA con una EI CONDITIONAL autorizada | NO SUPERADO |
| S-T11 | Con T-09 (a-ii): rama de H desde `55f758e`, admitida, con el paquete trasplantado y sin evidencia de criterios EQUIPO | 0 fallas; R = NO SUPERADO. Es V-5 con la rama nueva |
| S-T12 | S-T11 más una ruta bajo `app/`, `tests/` o un archivo de dependencias | FRZ falla por alcance y por runtime; R = NO SUPERADO |
| S-T13 | El mismo árbol que S-T11, con un nombre de rama no admitido o en HEAD desacoplado | FRZ falla por la rama (V-6) |
| S-T14 | Rama con el nombre admitido de H, pero cortada desde `develop` | FRZ falla por alcance y por runtime. El nombre solo no basta |
| S-T15 | Con T-09 (a-ii): `BASE` sigue siendo `b8892af…` | Prueba que fija la constante. Cambiarla queda fuera de esta versión |
| S-T16 | **Sonda de la especificación, no prueba de la implementación:** H en la línea de `main` y `BASE = 9dd76c4` | Falla «la base es ancestro de HEAD». Documenta por qué (b) queda fuera de alcance (§5.9.3) |
| S-T17 | `BRANCHES` | Contiene exactamente las tres ramas vigentes más la de H; ninguna otra pasa |
| S-T18 | Revocación después de H con exactamente el delta de §5.8.2 y la condición C-R | R = REVOCADO; espejos en REVOCADO y BLOQUEADA; 0 fallas |
| S-T19 | S-T18 más una ruta adicional, en `gate/evidencia/` o en cualquier otro lugar del paquete | Falla el vínculo: cambio material posterior a H |
| S-T20 | S-T18 más un campo adicional: otro campo del estado, otro criterio o una clave adicional en `revocation` | Falla el vínculo o el formato de `revocation` |
| S-T21 | FG-14 en NO CUMPLE o el documento de determinación sin un evento válido, o un evento que cita otra ruta | Falla: X1-R y X2-R no se habilitan sin C-R |
| S-T22 | Inventario de H: `git diff --name-only 55f758e <H>` incluye `sondas-b01/`, sus enlaces resuelven y las sondas se ejecutan desde el árbol de H | Cabe en AC-05; las sondas salen con código 0 |

Los controles positivos (S-T01, S-T05, S-T11 con evidencia y S-T18) solo se crean en memoria o en clones desechables, nunca sobre H (H §8). S-T11 a S-T14 y S-T18 a S-T22 necesitan Git real en un repositorio temporal, como la batería AF5 con Git real.

Su montaje y su resultado de hoy están en las sondas: §5.8.3 para S-T18 a S-T21, §5.9.4 para S-T11 a S-T17 y §5.9.5 para S-T22. Las sondas de S-T18 a S-T21 usan la definición de referencia de la sonda, no el validador. Al implementar B-01 se trasladan a la batería, sobre el validador nuevo y con la rama admitida en `BRANCHES`, no en memoria.

## 9. Decisiones de diseño

| ID | Decisión | Propuesta de S para decisión, no vinculante | Estado |
|---|---|---|---|
| T-01 | Lista de espejos E1–E7 y reescritura previa | Aceptar la de H §5.2 | NO EMITIDA |
| T-02 | Estado de F37-SBX con R = SUPERADO | Un único estado de habilitación, por ejemplo «AUTORIZADA PARA INICIAR», sin enumerar EI en el gobierno | NO EMITIDA |
| T-03 | ¿Cambia el estado de F36-SBX en la transición? | No; su cierre sería un incremento propio | NO EMITIDA |
| T-04 | Rama de H y de los registros | Admitir de forma explícita una sola rama de H, creada desde el commit `55f758e`, con S-T13, S-T14 y S-T17. Solo se especifica para T-09 (a-ii) | NO EMITIDA |
| T-05 | Formato de la revocación y su delta después de H | §5.8.1 y §5.8.2 | **Cerrado en S**, pendiente de auditoría |
| T-06 | Refuerzo de independencia de `integrante_no_autor` | Opcional | NO EMITIDA |
| T-07 | Versión del gate y del esquema | `gate_version = 3` y esquema v2 si se elige solo la variante 3/3; 4 y v3 si se implementa también la variante RD | NO EMITIDA |
| T-08 | Variante de registro | Implementar la 3/3 ahora y dejar la RD especificada. Con las DF actuales, la RD no se puede usar | NO EMITIDA |
| T-09 | Base, anclaje y FRZ después de SEG | (a-ii), la única variante de esta versión: una rama de H nueva desde el commit `55f758e`, con el paquete trasplantado y `BASE` sin cambios. (a-i) y (b) quedan fuera de alcance (§5.9.3) | NO EMITIDA |

## 10. Criterios de aceptación de la implementación

B-01 solo se da por implementado si se cumplen todos los criterios. Cada uno se verifica sobre el commit candidato, anclado en la rama de H. Están escritos para T-09 (a-ii), la única variante de esta versión (§5.9.3).

| ID | Criterio | Cómo se verifica |
|---|---|---|
| AC-01 | D-02b emitida por el mecanismo de P-S4, citada en el mensaje del primer commit de la implementación, y P-S1 a P-S3 cumplidas | Las rutas o los SHA-256 de los actos, y la determinación de D-10 |
| AC-02 | RED observado antes de cambiar el validador: S-T01 a S-T15, S-T17 a S-T22 y las pruebas de H fallan donde deben. S-T16 es una sonda de la especificación y no forma parte de la batería | Salida registrada en el informe de la implementación, dentro del paquete. `docs/tdd-evidence.md` queda fuera del perímetro de AC-05 y haría fallar FRZ: se sincroniza después, en un incremento propio |
| AC-03 | GREEN: la batería y las metapruebas (`meta_f36sbx.py`) pasan, con ablaciones del código nuevo que las hagan fallar | Ejecución completa y su recuento |
| AC-04 | Sin evidencia de criterios EQUIPO, el validador da 0 fallas con R = NO SUPERADO declarado y recalculado | S-T11 |
| AC-05 | `git diff --name-only 55f758e <H>` ⊆ `docs/academico/f36-sbx/` ∪ `docs/academico/tools/f36sbx/` ∪ `GOV_FILES`, con H creado desde el commit `55f758e` (T-09 (a-ii)). El inventario incluye `expediente-final/sondas-b01/`, y las sondas se ejecutan desde el árbol de H | Comando y su salida en el informe; S-T22 |
| AC-06 | `BASE` sin cambios (`b8892af…`), como exige (a-ii) | S-T15 |
| AC-07 | `BRANCHES` admite exactamente una rama nueva, la de H, creada desde el commit `55f758e` (T-04 con (a-ii)) | S-T13, S-T14 y S-T17 |
| AC-08 | El SHA-256 nuevo del validador consta en todos los documentos que lo citan, y el de v3 (`87ad2f6f…`) se conserva como histórico | Búsqueda de ambos valores |
| AC-09 | Los espejos E1–E7 tienen una sola afirmación por sujeto antes de H (D-07), y cualquier divergencia con R, en cualquier sentido, falla | Batería de H y S-T03 |
| AC-10 | REVOCADO representable y prevalente. Después de H, el vínculo admite exactamente el delta de §5.8.2 con la condición C-R, y rechaza cualquier ruta o campo adicional | S-T01 a S-T03 (I-11) y S-T18 a S-T21, sobre el validador nuevo |
| AC-11 | Ningún control positivo (SUPERADO o REVOCADO) persiste en el repositorio | Búsqueda en el árbol de H: 0 archivos bajo `gate/evidencia/`, tampoco `REVOCACION_DETERMINACION.md` |
| AC-12 | FG-12 en NO APLICA se conserva | S-T09 y S-T10 |
| AC-13 | El informe registra que, al integrar H en `develop`, FRZ fallará allí por diseño (I-14), con la salida esperada | Sección del informe |
| AC-14 | Sin dependencias nuevas; el validador sigue usando solo la biblioteca estándar | Regla DEP |

## 11. Qué depende de D-10, D-11 y D-02b

Son cuatro requisitos distintos, y ninguno sustituye a otro (borrador D-11, §4):

- **Contrato 10** (`CLAUDE.md`). Exige **hoy** autorización explícita del equipo para cada `push`, `merge`, release o tag. La obligación existe con D-11 o sin ella.
- **D-11.** Si se adopta, define el procedimiento y el formato de esa autorización. No la crea, no la sustituye y no autoriza ninguna operación. Mientras no se adopte, la autorización se acredita con actos del equipo según el texto vigente del contrato 10.
- **D-10.** Es una determinación sobre la vigencia del charter. No autoriza ni implementar ni publicar.
- **D-02b.** Autoriza implementar B-01 en local. No autoriza ningún `push` ni ningún `merge`, y una autorización del contrato 10 tampoco equivale a D-02b.

| Elemento | D-10 | D-02b | Contrato 10 (hoy) | D-11 (si se adopta) | Otros requisitos |
|---|---|---|---|---|---|
| B-01 en conjunto | **Sí** (P-S1). Con D10-2, B-01 no tiene objeto y haría falta un gate nuevo | **Sí**: la autoriza | No: implementar en local no es una operación del contrato 10 | No | Auditoría de S (P-S2) |
| T-09 (a-ii), elegir la base | No: la base no se mueve | Sí, como decisión | No | No | — |
| T-04, admitir la rama de H | No | Sí | No | No | — |
| Crear la rama local de H e implementar | Sí, a través de B-01 | Sí | No: es trabajo local | No | — |
| Push de H para la auditoría | No | No la sustituye | **Sí**: autorización explícita del equipo para esa operación | Fija el procedimiento y el formato del acto | — |
| Merge de H en `develop` o `main` | No | No la sustituye | **Sí**: autorización explícita del equipo para esa operación | Fija el procedimiento y el formato del acto | Validación anclada antes del merge (I-14) |
| T-05 (REVOCADO) y su delta (§5.8.2) | Solo se usa con D10-2 o con una revocación posterior; el formato no depende de D-10 | Sí | No | No | El documento de determinación (X1-R) |
| T-08, variante RD | No | Sí | No | No | DF-03 con su texto íntegro (hoy pendiente) |
| FG-02 sobre H | No | No | No | No | El informe del auditor elegible sobre H |
| FG-03, FG-10 y FG-12 | No | No | No: un acto del contrato 10 no es un voto del gate | No | Votos 3/3 (gate v3), referidos a H |
| Inicio de F37-SBX | Sí | Sí | No | No | R = SUPERADO anclado en H |

(a-i) y (b) no figuran: quedan fuera del alcance de esta versión (§5.9.3).

**Lo que se puede hacer sin D-10, D-02b ni autorizaciones del contrato 10:**
- auditar S;
- preparar la batería de pruebas RED como borrador fuera del validador;
- repetir las sondas de §5.8.3, §5.9.1, §5.9.4 y §5.9.5, que están en [`sondas-b01/`](sondas-b01/README.md).

## 12. Qué debe auditar Codex en esta versión

1. Que §5.9.1 se pueda reproducir: las siete sondas, con sus resultados y su método (sin mover refs).
2. Que §5.9.2 no afirme más de lo medido. Por ejemplo, V-5 no prueba que H vaya a superar el gate: solo que FRZ admite el trasplante.
3. Que §5.9.3 especifique solo (a-ii), como propuesta para decisión, sin anticipar D-10, D-02b ni T-04, y que (a-i) y (b) consten como alternativas fuera de alcance, no como decisiones.
4. Que S-T11 a S-T22 y AC-01 a AC-14 sean verificables, y que ningún control positivo quede en el repositorio.
5. Que §11 no atribuya a D-11 lo que es de D-02b, del gate o del contrato 10, ni a la inversa.
6. Que ningún pasaje emita un acto, un voto, una delegación o un estado del gate.
7. Que las sondas de `sondas-b01/` no modifiquen el validador ni ninguna ref, que el parche en memoria se limite a `BRANCHES` y `BASE`, y que §5.9.4 no presente S-T11 como prueba de que H superaría el gate.
8. Que AC-02 y AC-05 ya no se contradigan: todo lo que exige la implementación cabe en el perímetro de FRZ.

**Correcciones de la 2.2**, con su evidencia del 09/11/2026:

9. **S-M01.** Que T-04, AC-05, AC-06, AC-07, S-T15, S-T16 y la matriz de §5.9.3 solo se refieran a (a-ii), y que ninguna variante figure como aprobada.
10. **S-M02.**
    - Que X1-R, X2-R y la condición C-R (§5.8.2) sean compatibles con §5.8.1 y AC-10, y que no relajen ninguna otra restricción.
    - Que `sonda_revocacion.py` diera 9 conformes y 0 discrepancias, y que dos ablaciones de su definición de referencia la hicieran fallar.
    - Que la sonda no se presente como validación funcional de AC-10.
11. **S-M03.** Que `sondas-b01/` quede dentro de AC-05 y que `sonda_trasplante.py` diera T-1 a T-4 conformes (§5.9.5). También que `sondas_t09.py` siga dando sus 18 sondas conformes, con V-7 sobre `f5003c9`.
12. **S-L01.** Que §11 distinga la obligación vigente del contrato 10, el procedimiento de D-11, la determinación D-10 y la autorización D-02b.
