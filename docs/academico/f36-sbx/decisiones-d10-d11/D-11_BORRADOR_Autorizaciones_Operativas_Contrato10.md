# BORRADOR — PENDIENTE DE DECISIÓN

## D-11 · Autorizaciones operativas del contrato 10: procedimiento colegiado hacia adelante

> **BORRADOR — PENDIENTE DE DECISIÓN.** Preparado el 07/11/2026 por una sesión de Claude Code a pedido de Luis Vila Meza, fuera de Git. No es un acto de ningún integrante, no adopta ningún procedimiento y no autoriza ninguna operación. Ningún estado cambia.
>
> **Referencia de adopción:** RR-001, commit `5036393f11b30855d3b3b28154e2d6a4f94c0bd5`, que adopta Q2 en la versión V `8b1f068b5ac2039139ab5756096c147c11c9fcb2` (árbol `b5b81718680762f9585e4dae969ca44e69114865`), con efecto desde el 07/11/2026. **Facultades delegadas utilizables: ninguna.** DF-02 está acreditada y DF-03 queda **PENDIENTE DE ACREDITAR SU TEXTO ÍNTEGRO** (RR-001 §2 y §4). Este borrador no presume la intersección ni la anticipa.

Marcas: **[H]** hecho verificado en esta sesión; **[R]** tomado de un documento, no repetido aquí; **[P]** propuesta.

---

## 1. Qué hay que decidir

El contrato 10 (`CLAUDE.md`) dice: «Sin `push`, `merge`, release ni tag sin autorización explícita del equipo». No fija quórum, formato ni lugar de la evidencia. Con Q2 adoptada (V §4 N3 y §10):

- Luis decide en representación del equipo **solo** las operaciones de N3 cubiertas por delegaciones vigentes de Fredy **y** de Anthony;
- todo lo demás va al **mecanismo colegiado**, que V nombra pero no define.

D-11 tiene que definir ese mecanismo: qué operación concreta se autoriza, quién la autoriza, qué rama, commit o versión abarca y dónde se conserva la evidencia. Rige solo hacia adelante.

## 2. Fuentes

| ID | Fuente | Qué aporta |
|---|---|---|
| F1 | `CLAUDE.md`, contratos 9 y 10 | Texto del contrato 10 e inmutabilidad de `v1.0.0-academic` |
| F2 | `AGENTS.md`, «Git y supply chain» | Prohíbe rebase de historia publicada, `reset --hard`, force push y borrado de ramas o tags |
| F3 | `5036393:…/reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md` (V) §3, §4, §7, §8, §9.4–§9.6, §10 y §11 | Roles, N3, registros (RA, RD, RR), aplicación al gate, delegación por intersección y no reinterpretación |
| F4 | `5036393:…/reconciliacion-gobierno/F36SBX_Reconciliacion_Estado_Gobierno.md` §5.6 y §6 | Planteamiento de D-11: autorización operativa frente a representación del equipo |
| F5 | `5036393:…/adopcion-q2/D1_BORRADOR_DF-02_Fredy_Coronacion.md` §2 y `README.md` (Q2AD-M01 y Q2AD-M02) | Catálogo delegable: GIT-2 a GIT-5, B01-1, GATE-1 y GATE-2. Lo que no está en la lista «conserva la autorización del contrato 10» |
| F6 | `5036393:…/adopcion-q2/RR-001_Adopcion_Q2.md` §2, §4 y §5 | Estado de las DF y fecha efectiva |
| F7 | `5036393:…/adopcion-q2/G_Continuidad.md` §2 | D-11 con Q2 adoptada: opción (b) para lo cubierto y (a) para el resto |
| F8 | `5036393:…/F36SBX_Gate_Sucesor.md` §8.1 y §9; `gate/f36sbx_gate_state.json` | Quórum 3/3 del gate v3 para FG-03, FG-10 y FG-12 |
| F9 | Mensajes de `b69c6c3`, `f5b7c59`, `2e53786`, `2546297` y `9dd76c4`; `9dd76c4:docs/v1.1/security/SEG-01-02-integracion-local.md` §1 | Registro de las autorizaciones de SEG en el repositorio |
| F10 | Transcripciones locales `0be29a7a-….jsonl` (SHA-256 `f4d5e16e…81eb45b`) y `b1f82d09-….jsonl` (SHA-256 `893a3402…82229c0`), fuera de Git | Texto y hora de las autorizaciones de Luis |

## 3. Autorizaciones históricas de Luis para SEG [H]

Horas en America/Lima. Todas constan como **autorizaciones operativas de Luis**, una por operación (F4 §5.6; V §11).

| Operación | Resultado | Autorización | Hora | Constancia |
|---|---|---|---|---|
| Rama de integración local y merges de SEG-01 y SEG-02 | `b69c6c3`, `f5b7c59` y `4dd1bac` en `fix/seg-01-02-integration` | Prompt de Luis: «Luis autorizó expresamente…»; excluye push y merge en `develop` o `main` | 28/10 ≈19:05 | F10 (`0be29a7a`); `SEG-01-02-integracion-local.md` §1 |
| Merge local en `develop` | `2e53786` | Prompt de Luis: «Luis ya autorizó expresamente este destino […] No hagas push ni modifiques main» | 28/10 ≈21:03 | F10 (`0be29a7a`); mensaje de `2e53786` |
| Push de `develop` | `5545694..2e53786`; CI 40804808195 `success` | Prompt de Luis: «Publica exclusivamente develop […] Luis ya autorizó expresamente esta operación» | 28/10 ≈21:09 | F10 (`0be29a7a`) |
| Merge local de SEG-03 en `develop` | `2546297` | «Luis autoriza expresamente el merge descrito aquí y su commit. Esta autorización NO incluye push…» | 29/10 ≈09:39 | F10 (`b1f82d09`) |
| Push de `develop` | `2e53786..2546297`; CI 40904841417 `success` | Respuesta a la pregunta de confirmación: «Sí, Luis autoriza el push» | 29/10 10:45:22 | F10 (`b1f82d09`) |
| Merge de SEG-04 en `develop` y push | `9dd76c4`; `2546297..9dd76c4`; CI 40923175235 `success` | «Yo, Luis Vila Meza, autorizo expresamente integrar SEG-04 en develop […], publicar exclusivamente develop y verificar la CI […] No autorizo cambios en main, otras ramas, tags, releases…» | 29/10 12:36:02 | F10 (`b1f82d09`) |

**Lo que se mantiene.**

- **Resultado técnico.** Las auditorías de Codex, la conservación del árbol auditado en cada merge y la CI en verde respaldan el resultado técnico de SEG-01 a SEG-04.
- **Autorización del equipo.** Solo queda documentada en la medida en que consten actos que la acrediten. Constan actos de Luis, uno por operación. No consta ningún acto de Fredy ni de Anthony, ni una delegación anterior al 07/11. Por eso, la autorización del equipo conforme al contrato 10 no está acreditada para estas operaciones, y este borrador no la afirma ni la descarta más allá de esa evidencia.
- **Sin reinterpretación.** No se reinterpretan, no se ratifican con fecha anterior y no se fabrican votos (V §9.5 y §11).

**Discrepancia textual que conviene registrar, sin reescribir nada.**

- Los mensajes de `b69c6c3` y `f5b7c59` dicen «Local integration authorized by the team», y el de `2e53786`, «Local merge into develop authorized by the team».
- La constancia (F10) muestra autorizaciones de Luis, y la reconciliación las califica así.
- `2e53786` está publicado: su mensaje no se cambia. La precisión puede añadirse como anexo fechado en un incremento documental autorizado.
- Los merges `2546297` y `9dd76c4` no tienen cuerpo. Su autorización solo consta en F10, fuera del repositorio.

**Otras referencias históricas, tal como constan.** La integración de AF5 (`5545694` y `55f758e`, 27/10) se hizo con la instrucción operativa (b) de D-01, que no es una decisión formal (F4 §3.2; V §11). El commit RR-001 (`5036393`) es local, sin merge ni push.

## 4. Reglas aplicables por operación

La última columna dice qué rige mientras no haya facultades delegadas utilizables, es decir, hoy.

| Operación | Fuente vigente | ¿Está en N3 de V? | ¿Es delegable? (F5) | Hoy |
|---|---|---|---|---|
| Merge en `develop` y push de `develop` | Contrato 10; V N3 | Sí | GIT-2 | Colegiado |
| Merge en `main` | Contrato 10; V N3 | Sí | GIT-3, solo el merge | Colegiado |
| Push de `main` | Contrato 10 | No: V no lo enumera (Q2AD-M01) | No | Colegiado |
| Push de ramas de trabajo (`feature/*`, `fix/*`, `docs/*`, `chore/*`) | Contrato 10 | No (GIT-1 retirado) | No | Colegiado (ver P-04) |
| Merge en ramas de trabajo o de integración local, como `fix/seg-01-02-integration` | Contrato 10, texto vigente («merge», sin calificar) | No: V lo deja fuera de N3, y N1 no lo nombra | No | **Colegiado.** Se aplica el texto vigente hasta que el equipo apruebe una aclaración (P-03) |
| Tag nuevo | Contrato 10; contrato 9 para `v1.0.0-academic` | Sí | GIT-4, solo tags nuevos | Colegiado. Mover, borrar o reutilizar tags está prohibido y fuera de este procedimiento |
| Release nueva | Contrato 10; V N3 | Sí | GIT-5 | Colegiado |
| Force push, rebase de historia publicada, borrado de ramas o tags | `AGENTS.md` | — | — | **Prohibido.** Este procedimiento no lo puede autorizar |
| D-02b, autorización para implementar el sucesor B-01 | V §8: «autorización explícita según el gobierno aplicable». No es una operación del contrato 10 | — | B01-1, solo con una S auditada | Colegiado. Además exige S auditada, que todavía no existe |
| FG-03, FG-10 y FG-12 | Gate v3 §8.1: votos 3/3 de las identidades exactas, esquema `f36sbx-team-evidence/v2` | — | GATE-1 y GATE-2, solo con un sucesor `gate_version` 4 | **Gate v3, sin cambios.** D-11 no lo sustituye ni lo modifica. FG-12 puede quedar en NO APLICA, sin archivo ni votos propios, cuando el gate lo admite: FG-03 en CUMPLE sin ninguna EI CONDITIONAL autorizada (gate §3 y §4; V §8) |
| ADR sucesor, alcance C, EI-09 (F36-M02) y N5 | ADR-005; V §4; Q2AD-M02 | — | No delegables | Fuera de D-11 |

Dos reglas se mantienen siempre. Una autorización del contrato 10 no autoriza nada del gate, y viceversa. Que una operación exija autorización del contrato 10 no la vuelve delegable.

## 5. Procedimiento propuesto [P]

### 5.1 Principios

1. **Hacia adelante.** Rige desde la fecha de su registro de adopción. No recalifica nada anterior (V §9.5).
2. **Por operación concreta.** Cada autorización identifica el repositorio, el commit y el árbol de origen, la ref de destino, el estado remoto esperado y el tipo de operación. Una autorización «general» de publicar no existe, salvo la autorización permanente acotada que el equipo elija en P-04.
3. **Actos propios.** Cada integrante emite su acto por su canal. Ninguna sesión de IA emite, transcribe por su cuenta ni presume un acto. El silencio no autoriza, y ningún plazo lo convierte en autorización.
4. **Dos caminos, nunca a la vez para la misma operación.**
   - **(b) Delegado:** un RD de Luis que cita RR-001, DF-02 y DF-03 vigentes en su fecha y una operación de la intersección. Hoy no está disponible. Solo puede empezar cuando estén vigentes a la vez RR-001 y las dos delegaciones (§5.3).
   - **(a) Colegiado:** para todo lo demás.

### 5.2 Camino colegiado

| Paso | Qué | Quién | Evidencia |
|---|---|---|---|
| 1. Solicitud **SO-NNN** | Un texto con los campos de la plantilla del Anexo A | Luis la emite, y Claude Code puede redactarla | Correo institucional de Luis a Fredy y Anthony, con la SO en el cuerpo o adjunta, y su SHA-256 |
| 2. Actos **RA-NNN** (V §7) | Cada integrante responde por su canal propio: «Autorizo SO-NNN tal como está descrita», citando el commit de origen. Puede poner condiciones, pero solo si se cumplen sin cambiar la SO; si la cambian, hace falta una SO nueva | Luis, Fredy y Anthony, cada uno el suyo | Los `.eml` originales, **fuera de Git** |
| 3. Registro colegiado **RC-NNN** | Transcribe la SO y los actos (titular, fecha, canal y SHA-256 del `.eml`) y comprueba el quórum elegido en P-01 | Claude Code puede redactarlo y Luis lo confirma. Se versiona en el commit de la operación o antes | Ubicación según P-02 |
| 4. Comprobación previa | Comprobar el commit, el árbol, el remoto esperado, la ausencia de conflictos y la CI exigida. Cualquier diferencia detiene la operación | La sesión que ejecuta | Salida conservada en la carpeta del expediente |
| 5. Ejecución | Solo lo enumerado en la SO. El mensaje del merge cita «RC-NNN» | La sesión que ejecuta, por instrucción de Luis | El commit y el push |
| 6. Cierre | Hash resultante, `old..new` del push y CI (ID y resultado). Se añade al expediente y, si procede, en el siguiente incremento documental, sin hashes autorreferenciales | Ídem | Expediente y SHA256SUMS |

**Lotes.** Una SO puede enumerar una secuencia cerrada, como en SEG-04: un merge `--no-ff` con un mensaje exacto, el push de ese hash y la verificación de la CI. Cada paso se enumera y se detiene si falla.

**Caducidad.** Una SO se usa una vez. Caduca si cambia la base o el remoto esperado, o si pasa el plazo que fije la propia SO.

### 5.3 Camino delegado (cuando exista)

**Cuándo empieza.** Una facultad delegada empieza cuando están vigentes a la vez RR-001, DF-02 y DF-03, es decir, en la última de estas fechas:

- la fecha efectiva de RR-001, el 07/11/2026;
- el inicio de DF-02, que su texto fija en la fecha del RR o la de su emisión, la posterior;
- el inicio de DF-03, una vez acreditado su texto íntegro, y nunca antes de esa acreditación.

Nunca rige antes. Solo pasa la intersección de las dos listas.

Cada uso exige un **RD-NNN**: fecha real, nivel N3, la operación del catálogo, el commit y el árbol, la cita de RR-001, DF-02 y DF-03, el informe y la CI. La revocación de una DF elimina la facultad desde su fecha (V §9.6).

### 5.4 Relación con el gate

FG-03, FG-10 y FG-12 siguen el gate v3: los registros `gate/evidencia/FG-0x.json` con los `approvals` de las tres identidades exactas, según §8. La excepción es FG-12 en NO APLICA, que el gate admite sin archivo ni votos propios cuando FG-03 está en CUMPLE y no autoriza ninguna EI CONDITIONAL. D-11 no crea un atajo. Un acto RA del contrato 10 no sirve como voto del gate, ni al revés. GATE-1 y GATE-2 solo existirán con un sucesor `gate_version` 4 auditado y adoptado.

## 6. Decisiones exactas que el equipo tendría que tomar

D-11 cambia el mecanismo de autorización, así que se adopta con un acto propio de **cada uno de los tres** integrantes sobre la misma versión fijada de este documento (F4 §8: «Los tres integrantes»). Puntos:

| ID | Pregunta | Opciones | Recomendación del preparador, no vinculante |
|---|---|---|---|
| P-01 | Quórum del mecanismo colegiado | **(i)** 3/3: los tres autorizan. **(ii)** Dos autorizaciones RA más un acto expreso del tercero, que debe constar antes de ejecutar (ver la nota de P-01) | (i). Es coherente con la adopción de Q2, con F34C y con el gate. (ii) solo es legítima si los tres la adoptan aquí |
| P-02 | Dónde se versiona el RC | **(i)** En el documento del incremento, como hasta ahora los RD. **(ii)** En una carpeta común, por ejemplo `docs/academico/gobierno/autorizaciones/RC-NNN.md` | (ii). Es más fácil de auditar y de enlazar desde el mensaje del merge |
| P-03 | Merges en ramas de trabajo o de integración local | El contrato 10 vigente ya exige, para estos merges como para cualquier otro, la autorización explícita del equipo. Esa exigencia no depende de D-11. Lo que D-11 añadiría es el formato: una vez adoptado, la autorización se tramitaría con SO, RA y RC. Hasta su adopción, se sigue exigiendo la autorización explícita del equipo del contrato 10, sin ese formato. La única pregunta es si se aprueba una aclaración hacia adelante: **(i)** no, y se mantiene el texto vigente; **(ii)** sí, y pasan a N1 siempre que no toquen `develop` ni `main` | Decisión del equipo. (ii) reduce fricción, pero solo rige desde su adopción por los tres, y se refleja en el delta de `CLAUDE.md`. Hasta entonces, cada merge de este tipo necesita la autorización explícita del equipo |
| P-04 | Push de ramas de trabajo | **(i)** Una SO por push. **(ii)** Una autorización colegiada permanente y acotada (un RC) para push sin force de ramas de trabajo, con una fecha de fin y sin `develop`, `main`, tags ni releases | (ii), con fecha de fin. Sigue siendo un acto 3/3, no una delegación |
| P-05 | Constancia de las autorizaciones históricas de SEG | **(i)** Ninguna nueva: se reconocen tal como constan. **(ii)** Una «toma de conocimiento» fechada hoy, sin ratificación retroactiva | (i), y añadir en un incremento documental la precisión sobre los mensajes «by the team» (§3) |
| P-06 | Canal admitido para SO y RA | El correo institucional propio de cada integrante, con el `.eml` conservado. Otros canales, solo con la evidencia original | El correo institucional. Una captura sola no basta (lección del expediente del 03/11) |

**Nota de P-01, opción (ii).** El tercero tiene que emitir, por su canal propio y antes de la ejecución, un acto expreso que cite la SO-NNN y su commit de origen. Puede ser de uno de estos tipos:

- **autorización**, y entonces el resultado es 3/3;
- **abstención expresa:** «Me abstengo respecto de SO-NNN y no me opongo a su ejecución»;
- **no oposición expresa:** «No autorizo SO-NNN, pero no me opongo a que se ejecute con las otras dos autorizaciones».

Tres reglas completan la opción:

- **Sin ese acto,** la operación no está autorizada. El silencio, la falta de respuesta o el vencimiento de un plazo no lo sustituyen.
- **Si el tercero se opone de forma expresa,** la operación no está autorizada.
- **El acto del tercero se conserva** igual que los RA, con su `.eml` fuera de Git y su SHA-256 en el RC.

Luis cuenta como uno de los tres, así que con esta opción, una vez emitido el acto expreso del tercero, basta la autorización de Luis y de un integrante más.

**Fuera de D-11.**

- DF-03 sigue pendiente: si Anthony acredita su texto íntegro, se registra por su propio procedimiento, con efecto desde su fecha.
- Los deltas de Q2 §12 al contrato 10 en `CLAUDE.md` y a `project-guardian` §6 se aplican después, en un incremento propio y auditado.

## 7. Evidencia que falta

| # | Evidencia | De quién |
|---|---|---|
| 1 | Revisión diferenciada de Codex sobre la versión fijada de este borrador | Sesión de Codex separada |
| 2 | Tres actos de adopción de D-11, con las opciones de P-01 a P-06 elegidas, sobre la misma versión | Luis, Fredy y Anthony |
| 3 | Para usar el camino (b): el texto íntegro de DF-03, acreditado | Anthony, si lo decide |
| 4 | Hash conservado de las transcripciones F10 en el expediente que se cree. Son registros locales que pueden crecer, así que se fija una copia | Luis |

---

## Anexo A. Plantilla SO-NNN (sin emitir)

```
SO-NNN — Solicitud de autorización colegiada (contrato 10)
Repositorio: https://github.com/luivmz/saas-reclutamiento-multiempresa.git
Operación(es), en orden: [p. ej. 1) merge --no-ff de <commit> en develop con el mensaje "<exacto>"; 2) push de <hash> a refs/heads/develop, sin force; 3) verificar la CI "tests"]
Origen: commit <40 hex>, árbol <40 hex>, rama <nombre>
Destino: <ref>; valor remoto esperado antes: <40 hex>; tipo: fast-forward | --no-ff
Árbol esperado tras el merge: <40 hex> (debe coincidir con el auditado)
Auditoría: <carpeta>, <informe>, SHA-256 <…>, veredicto <…>
Exclusiones: main | otras ramas | tags | releases | force | [otras]
Caducidad: un solo uso; caduca si cambia la base o el remoto, o el <fecha>
Se detiene si: cambia la base, hay conflictos, el árbol difiere o la CI falla
```

## Anexo B. Plantilla de acto RA (sin emitir)

> «Yo, [nombre], autorizo la solicitud SO-NNN tal como está descrita (origen `<commit>`, destino `<ref>`). [Sin condiciones | Condiciones: …]. No autorizo ninguna otra operación.»

## Anexo C. Plantilla RC-NNN (sin emitir)

| Campo | Valor |
|---|---|
| SO | SO-NNN, SHA-256 |
| Actos | Titular, fecha y hora, canal, SHA-256 del `.eml` (uno por integrante) |
| Quórum | Según P-01: cumplido o no cumplido |
| Camino | Colegiado (a). Ninguna facultad delegada utilizada |
| Ejecución | Hash resultante, `old..new`, CI (ID y resultado); se completa al cerrar |
