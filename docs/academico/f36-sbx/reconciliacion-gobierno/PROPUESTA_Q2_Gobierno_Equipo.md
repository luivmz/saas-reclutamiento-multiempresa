# PROPUESTA — NO VIGENTE — PENDIENTE DE ADOPCIÓN

## Q2 — Gobierno académico de tres integrantes con un responsable técnico (sucesora de Q)

> **PROPUESTA — NO VIGENTE — PENDIENTE DE ADOPCIÓN.** Documento del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`, creada desde `develop` = `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9`.
>
> **No modifica** `AGENTS.md`, `CLAUDE.md`, las skills, el contrato, el esquema ni el validador de F36-SBX, ni ningún estado o evidencia. Mientras no se adopte por el procedimiento de la sección 9, rigen las reglas vigentes: F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA y el quórum 3/3 del gate. Los hechos citados están verificados en el [informe de reconciliación](F36SBX_Reconciliacion_Estado_Gobierno.md).
>
> **Versión corregida** tras la auditoría documental de Codex sobre `729babb`. Recoge las correcciones de Q2-M01 a Q2-M04 y las que corresponden a los hallazgos de Q; la matriz está en la respuesta a la auditoría de esta carpeta. La versión que llegue a adoptarse se identificará por su commit y su árbol, no por este texto (sección 9).

## 1. Relación con Q

Q es la propuesta `061ba68:docs/academico/f36-sbx/preparacion-gate/F36SBX_Propuesta_Gobierno_Unipersonal.md`. Distinguía dos lecturas sin elegir entre ellas:

- **(a)** tres integrantes reales, de los que solo uno desarrolla;
- **(b)** una sola persona real.

**Las declaraciones recibidas no coinciden en el tiempo [R]:**

| Fecha | Declaración | Dónde consta |
|---|---|---|
| 27/10/2026 | El proyecto lo desarrolla una sola persona real, y los tres dispositivos son tres entornos de trabajo, no tres integrantes humanos independientes. La auditoría de Q registra además que su encargo presentaba a Fredy Coronacion y Anthony Peña como identificadores de entornos | Q §1.1 e informe de la auditoría de Q (UNI-M01) |
| 28/10/2026 y 29/10/2026 | El equipo tiene tres integrantes reales, Luis Vila Meza, Fredy Coronacion y Anthony Peña. Luis es el único desarrollador técnico y toma las decisiones ordinarias de programación | Peticiones de SEG-01 y SEG-02, y de este incremento |

Q2 parte de la declaración vigente, que corresponde a la lectura (a) de Q, y **no reinterpreta la historia**. La aclaración formal de la discrepancia le corresponde a Luis, en su declaración R-01 (sección 13). Los registros históricos se conservan tal como constan (sección 11).

**Q2 sustituye a Q como propuesta.** Q no se adoptó, se conserva como registro y no se edita. Q2 reutiliza de Q:

- el registro de decisiones con fecha real;
- la separación entre auditoría técnica y decisión humana;
- la prohibición de presentar una IA como persona;
- la adopción prospectiva.

| Tema | Q | Q2 |
|---|---|---|
| Composición | Una persona real, o una lectura sin determinar | Tres integrantes reales, conforme a la instrucción de las guías oficiales de formar equipos de tres estudiantes. Uno es el responsable técnico |
| Quórum 3/3 del gate | «Imposible de cumplir con autenticidad» en la lectura (b) | Posible solo si los tres actúan de verdad. Q2 no lo simula ni lo da por cumplido |
| Fredy y Anthony | Integrantes «no activos» | Integrantes académicos, sin contribuciones, firmas ni aprobaciones técnicas atribuidas |
| Autoridad para adoptar | La conformidad de los otros dos (a) o el docente (b) | Los actos de conformidad de los tres integrantes con una misma versión fijada (sección 9). El docente, solo si una fuente aplicable lo exige o el equipo decide consultarle |
| Delegación | No se distinguía | Separada de la conformidad: cada integrante delega o no, de forma total, parcial o nula (sección 9) |
| Decisiones técnicas ordinarias | Del responsable, dentro del modelo unipersonal | Hoy se rigen por las reglas vigentes del repositorio. Q2 solo las clasifica (N1) y no las amplía |
| Excepción o consulta docente | Imprescindible en la lectura (b) | No hace falta una excepción individual, porque Q2 mantiene a los tres integrantes que piden las guías. La consulta es opcional |

## 2. Hechos de partida

- **[H] Equipo declarado ante el curso:** Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio. En este documento, Fredy Coronacion, Anthony Peña y Luis Vila Meza son la forma corta de esos mismos nombres.
- **[H] Instrucción académica.** Las nueve guías oficiales, de la 02 a la 09 y la 11, indican formar equipos de tres estudiantes para el proyecto grupal. El texto y los SHA-256 están en la [reconciliación, §5.1.1](F36SBX_Reconciliacion_Estado_Gobierno.md#511-la-instrucción-de-las-nueve-guías-h). Hay tres cosas distintas:
  1. **la composición académica de tres integrantes**, una obligación externa acreditada;
  2. **el quórum interno para actos concretos**, como ADR-005 o FG-03, FG-10 y FG-12, que es una regla del proyecto;
  3. **las decisiones técnicas ordinarias**, que se rigen por las reglas vigentes del repositorio y sobre las que no se encontró ninguna norma externa.
- **[H] No acreditadas:**
  - el reparto de la contribución técnica;
  - el uso de IA;
  - la aprobación de decisiones técnicas;
  - la autorización docente de commits;
  - la aplicabilidad actual de las guías.
- **[H] Autoría Git.** Tienen como autor a «Luis Vila Meza» los 32 commits de F36-SBX hasta AF5, los 8 de AF6, H y Q, y los 20 de SEG-01 a SEG-04. Seis commits del 20/10/2026 figuran con la identidad «Coronacion Meza Fredy»; están solo en `origin/codex/mejoras-sonarqube`, sin integrar. Git declara la identidad, no la autentica.
- **[H] Origen del 3/3.** El quórum 3/3 de F36-SBX es interno: nace en F34A, se cumplió en F34C y lo hereda el gate §8.1.
- **[H] Práctica reciente.** SEG-01 a SEG-04 se integraron y publicaron con autorizaciones operativas de Luis, una por operación. No está documentado que fueran una representación del equipo según el contrato 10 (D-11, reconciliación §5.6). Eso no invalida SEG.

## 3. Roles

La tabla describe los roles con Q2 adoptada; hoy rigen las reglas vigentes (sección 4).

| Rol | Quién | Puede | No puede |
|---|---|---|---|
| Responsable técnico de desarrollo | Luis Vila Meza | Las decisiones de N1 y N2. En N3, solo lo que cubran las delegaciones vigentes. Proponer cambios de gobierno y registrar sus decisiones, siempre con justificación | Auditarse a sí mismo; decidir en N4 por los otros dos; decidir en N5 |
| Integrantes académicos | Fredy Coronacion y Anthony Peña | Emitir sus propios actos: conformidad, delegación, aprobación, rechazo, abstención o revocación | Ser sustituidos por otra persona, un dispositivo o una IA. Que se les atribuyan contribuciones técnicas, firmas o aprobaciones que no hicieron |
| Claude Code | Sesiones de implementación | Diseñar, implementar, probar, documentar y preparar borradores | Decidir, aprobar, votar, auditar su propio trabajo o registrar actos humanos que no ocurrieron |
| Codex | Sesiones de revisión separadas | Auditar de forma técnica y diferenciada, con informe, veredicto y manifiesto | Decidir o votar; presentarse como integrante, docente o revisor humano |
| ChatGPT | Coordinación | Redactar planes y prompts y ordenar el trabajo | Decidir: sus propuestas valen cuando Luis las asume |
| Docente | Autoridad académica externa | Evaluar los entregables; reconocer o no lo que se le consulte | — (sus permisos no se presumen) |

## 4. Niveles de decisión: clasificación propuesta

**No es fuente de autoridad actual.** Hoy cada actividad se rige por la fuente vigente de la tercera columna. La cuarta describe lo que regiría después del registro raíz de adopción (sección 9).

| Nivel | Qué cubre | Fuente vigente hoy | Tras la adopción | Registro |
|---|---|---|---|---|
| **N1** Técnica ordinaria | Diseño e implementación, pruebas, commits, ramas `feature/*`, `fix/*`, `docs/*` y `chore/*`, worktrees, refactors, priorización de la deuda técnica, y aceptar o rechazar sugerencias de una IA | `CLAUDE.md`, `AGENTS.md` y las skills (`project-guardian`, `laravel-saas-quality`, `ml-risk-service` y las de frontend), dentro del alcance de cada incremento. Ninguna fuente exige votos ni autorización docente | Igual: decide Luis. Q2 no crea ni amplía estos permisos | El commit y el documento del incremento |
| **N2** Cambio con revisión diferenciada | Seguridad, autorización y multiempresa; la auditoría; el modelo de datos y las migraciones; el ML y su contrato; validadores y gates; dependencias; CI; documentos de gobierno | Las reglas de seguridad y calidad vigentes y las revisiones que exija cada incremento, como las auditorías de SEG. Hoy no rige la tabla completa | Decide Luis, después de una auditoría técnica de Codex sobre el commit exacto, sin BLOCKER, HIGH ni MEDIUM que exija corrección abiertos | Un RD que cita el informe y su hash |
| **N3** Integración y publicación | Merge a `develop`, push de `develop`, merge a `main`, tags y releases | Contrato 10: autorización explícita del equipo. Las autorizaciones operativas de Luis están acreditadas; la representación del equipo no está documentada (D-11) | Decide Luis en representación del equipo, solo con las delegaciones vigentes de Fredy y de Anthony que cubran la operación. Sin ellas, decide el mecanismo colegiado | Mensaje del merge y un RD que cita el RR y las DF |
| **N4** Académica del equipo | Adoptar o cambiar este modelo; las declaraciones ante el curso; presentar un entregable o una release como trabajo del equipo; los criterios de equipo de F36-SBX mientras rija el 3/3 | Las reglas internas específicas (ADR-005; FG-03, FG-10 y FG-12 con 3/3) y la composición de tres que piden las guías | Actos propios de cada integrante, o una delegación expresa con un alcance definido. El ADR y el alcance C no son delegables | RA, CM o DF, con la evidencia de cada acto |
| **N5** Externa | G0-02, G0-03 y G0-12; las aprobaciones jurídicas, de privacidad o institucionales; los datos reales; producción; el alcance C del producto | Las autoridades externas | Igual: fuera de la autoridad del equipo | Solo lo recibido, con su evidencia |

- **La conformidad de los tres para adoptar Q2 es una elección de esta propuesta.** La justifica su efecto sobre las responsabilidades y las declaraciones académicas del equipo. No es una norma universitaria que exija unanimidad para las decisiones técnicas.
- **En N3, autorizar no es lo mismo que representar.** Una autorización de Luis para una operación es una autorización operativa; solo con delegaciones vigentes sería, además, una representación documentada del equipo.
- **Aprobar un ADR sucesor** que excepcione ADR-005, o cualquier decisión de alcance C, no es delegable: ADR-005 lo revisaron los tres integrantes (F34C).

## 5. Revisión técnica diferenciada

1. **Sesión separada.** La sesión que audita no es la que implementó ni la que preparó lo auditado.
2. **Identidad.** Examina un commit fijo, con su SHA y su árbol, y lo declara en el informe.
3. **Método propio.** Usa sus propias pruebas, además de las oficiales.
4. **Evidencia.** Un informe con su manifiesto SHA-256. Si se versiona, basta un resumen con los hashes.
5. **Límites declarados.** Un mismo operador humano orquesta las sesiones, y las auditorías se ejecutaron en el mismo PC Windows y su WSL. Que los proveedores sean distintos reduce los errores correlacionados, pero no los elimina, y no hay independencia institucional.
6. **Registro.** Luis comprueba la sesión, el manifiesto y el commit, y registra su decisión sobre cada hallazgo en un RD o un RX. Una discrepancia registrada no altera el informe del auditor ni las condiciones de un gate.
7. **Uso de IA declarado.**
   - Los commits llevan las líneas `Co-Authored-By`.
   - Los documentos dicen que implementa Claude Code y revisa Codex.
   - Cómo se declara la asistencia de IA en los entregables académicos lo decide el equipo (N4).

Una revisión de IA nunca es una aprobación humana, un voto ni una validación externa.

## 6. Validaciones externas

- **Las guías oficiales** piden equipos de tres estudiantes, y Q2 los mantiene (sección 2).
- **No se pide autorización del docente** para commits, pruebas ni decisiones técnicas ordinarias: ninguna fuente aplicable lo exige.
- **Lo no acreditado** —la aplicabilidad actual de las guías, las reglas de entrega y autoría y el uso de IA— se cumplirá si aparece una fuente aplicable.
- **La consulta al docente es opcional**, por ejemplo para un reconocimiento externo de la delegación o de la declaración de contribuciones (N4). Si se hace, la respuesta se conserva tal como se recibió, con su fecha y su hash.
- **N5 queda fuera de la autoridad del equipo.** Ni tener tres integrantes ni trabajar con datos sintéticos sustituye esas revisiones.

## 7. Registros

| Registro | ID | Campos | Quién lo escribe | Regla |
|---|---|---|---|---|
| Registro raíz de adopción | RR-NNN | La versión (commit y árbol del paquete), el informe aplicable (ubicación, SHA-256, veredicto y recuentos), los actos R-01, CM y DF con sus hashes, las condiciones y su cumplimiento, el alcance efectivo y la fecha | Se crea en un incremento posterior, cuando se cumplen las reglas de la sección 9. Transcribe los actos sin alterarlos | Nunca anterior al informe ni al último acto que cita. No se retrofecha |
| Conformidad con el modelo | CM-NN | El integrante, la versión (commit y árbol), la decisión (conforme, conforme con condiciones o no conforme), las condiciones, la fecha, el canal y la evidencia con su SHA-256 | Cada integrante, también Luis | Una conformidad con otra versión no cuenta |
| Delegación de facultades | DF-NN | Quién delega, las facultades delegadas (lista cerrada), los límites, el inicio, el fin o la revocabilidad, el canal y la evidencia | Fredy y Anthony, cada uno por su cuenta | Es independiente de la conformidad, puede ser total, parcial o nula, y se revoca hacia adelante con otro acto |
| Decisiones del responsable técnico | RD-NNN | Fecha real, nivel, alcance (rama, commit y árbol), decisión y evidencia (informe, hash y CI). Si usa una facultad delegada, cita el RR y las DF vigentes en su fecha | Luis, o la sesión que transcribe literalmente una decisión expresa suya, citando el canal y la fecha | Sin RR y DF vigentes, una facultad delegada no existe. Nunca anterior a la evidencia que cita |
| Discrepancias | RX-NNN | El hallazgo o la propuesta, su fuente, la postura de Luis, el motivo, el riesgo aceptado y el seguimiento | Luis | Ningún hallazgo se descarta en silencio |
| Excepciones | RE-NNN | La regla exceptuada, el motivo, el alcance, la duración y el control compensatorio | Luis (N1 y N2) o los tres integrantes (N4) | No se exceptúan los contratos 1 a 10 ni las prohibiciones duras del charter |
| Otros actos de integrantes | RA-NNN | El integrante, el acto, el alcance, la fecha, el canal y la evidencia con su SHA-256 | Cada integrante emite su acto; el registro solo lo transcribe | Nadie registra un acto en nombre de otro. Un hash conserva bytes, no autentica al emisor: la autenticidad se comprueba por un canal propio del titular |

Hasta la adopción, los RD siguen viviendo en el documento de cada incremento, como en SEG-01 a SEG-04.

## 8. Aplicación a F36-SBX

| Camino | Condición | FG-03, FG-10 y FG-12 | D-02b (sucesor B-01) |
|---|---|---|---|
| **Contrato vigente** (sin adoptar Q2, o sin delegación que lo cubra) | El gate v3 tal como está | Tres votos reales de las tres identidades exactas, cada uno emitido por su titular | Una autorización explícita según el gobierno aplicable. El contrato no fija un quórum para D-02; el 3/3 es una práctica, no un texto normativo |
| **Q2 con delegación** | RR vigente y DF de Fredy y de Anthony que cubran el criterio | Un contrato sucesor (`gate_version` 4 y esquema v3) sustituye los `approvals` 3/3 por un RD de Luis que cita el RR, las DF y una FG-02 favorable sobre H. El ADR y el alcance C quedan fuera de la delegación | Un RD anclado al commit de la especificación S del sucesor, a su informe de auditoría y al RR, con un alcance de implementación limitado |
| **Ninguno** | Ni votos ni delegación | Sin registro | Sin autorización |

En el tercer caso, el gate sigue NO SUPERADO y F37-SBX sigue bloqueada, que es el resultado correcto de un contrato que falla cerrado. Adoptar Q2 no implementa por sí solo `gate_version` 4 ni el esquema v3: el contrato vigente se aplica mientras no se ejecute legítimamente el cambio.

**Orden que conserva cada registro en su objeto:**

1. auditoría de la especificación S;
2. D-02b, si procede;
3. implementación y cambios materiales;
4. H fijado;
5. FG-02 favorable sobre H;
6. decisiones y evidencias de FG-03, FG-10 y FG-12 referidas a H;
7. registro permitido por el sucesor;
8. validación;
9. inicio efectivo de F37-SBX con el procedimiento correspondiente, solo si el resultado es SUPERADO.

**FG-03 es una entrada del gate:** no puede exigir que el gate ya esté superado. Este orden corrige el D-02c histórico de `1d5d6aa`, que aquí no se modifica.

**En los tres caminos:**

- **FG-02.** El auditor puede ser una sesión de Codex del tipo `sesion_de_auditoria_independiente`, nunca presentada como persona. Fredy o Anthony podrían figurar como `integrante_no_autor` solo si hacen de verdad una auditoría técnica; no se presume.
- **FG-10.** El revisor de la cadena de suministro puede ser Luis, que es un integrante.
- **FG-12.** Queda en NO APLICA solo según el contrato, sin archivo ni votos propios.
- **Ninguna aprobación se simula.**

## 9. Adopción: versión, conformidad, delegación y entrada en vigor

**9.1 Versión.** Se adopta una versión exacta V de Q2, identificada por un commit y su árbol en la rama de este paquete. V debe tener una revisión diferenciada favorable sobre ese mismo commit, sin BLOCKER, HIGH ni MEDIUM que exija corrección abiertos.

El texto de V no contiene su propio hash. El RR, que se crea después y en otro commit, cita V, así que no hay referencia circular. Una corrección material de V produce otra versión, que necesita otra revisión y actos nuevos.

**9.2 Actos.**

- R-01 es la declaración de Luis sobre la composición y los roles.
- CM-01, CM-02 y CM-03 son las conformidades de Luis, Fredy y Anthony con V.
- DF-02 y DF-03 son las delegaciones de Fredy y de Anthony en Luis, independientes de las conformidades.

**9.3 Reglas.** Q2 queda ADOPTADA solo si se cumplen todas a la vez:

1. Las tres CM citan el mismo commit y el mismo árbol de V.
2. Las tres son «conforme», o «conforme con condiciones» cuyas condiciones el RR acredita como cumplidas, con su evidencia. Una condición que exige cambiar V no se cumple sobre V: hacen falta una versión nueva, su revisión y actos nuevos.
3. La fecha del RR no es anterior a la del informe de V ni a la del último acto que cita.

Sin las tres conformidades no hay adopción. Ni la negativa ni el silencio cuentan como conformidad, y ningún plazo convierte la falta de respuesta en aceptación.

**9.4 Delegación.** No es condición de la adopción. Una facultad pasa a Luis solo si Fredy y Anthony la delegan los dos, en DF vigentes: lo que pasa es la intersección de sus listas. Con una delegación nula o parcial, el resto de facultades sigue en el mecanismo colegiado del contrato 10 o en el 3/3 del gate.

**9.5 Entrada en vigor.** En la fecha del RR, solo hacia adelante. Cada DF rige desde su propia fecha, si es posterior. Nada anterior cambia de calificación.

**9.6 Escenarios.**

| Escenario | Resultado |
|---|---|
| Los tres son conformes con la misma V | ADOPTADA |
| Las conformidades citan versiones distintas | NO ADOPTADA para ninguna. Hacen falta actos nuevos sobre una misma versión |
| Conformidad con condiciones compatibles, que el RR acredita como cumplidas | ADOPTADA, con esas condiciones registradas |
| Condiciones incompatibles entre sí o con V, o no acreditadas | NO ADOPTADA. Si exigen cambiar V: una versión nueva, su revisión y actos nuevos |
| Conformidad parcial, solo con una parte de V | NO ADOPTADA: el modelo se adopta entero. La parte acordada puede proponerse como una versión nueva |
| Negativa de un integrante | NO ADOPTADA. Sigue el régimen vigente |
| Falta de respuesta | NO ADOPTADA. El silencio no es conformidad |
| Modelo aprobado por los tres, sin delegaciones | ADOPTADA, sin facultades delegadas: N3 y los criterios de equipo del gate siguen en el mecanismo colegiado |
| Delegación parcial: Fredy y Anthony delegan listas distintas | ADOPTADA. Solo pasan a Luis las facultades que delegan los dos |
| Revocación posterior de una delegación | La facultad deja de existir desde la fecha de la revocación. Los RD anteriores conservan su validez |

**9.7 Si no se adopta.** N1 sigue como hoy, porque ninguna regla lo restringe; el contrato 10 conserva su texto y D-11 queda abierta. El equipo puede consultar al docente si quiere.

**9.8 Incrementos sucesores.** Los deltas de la sección 12 los aplican incrementos auditados:

- la parte del gate, dentro de H, con D-02b bajo el modelo adoptado;
- la de `AGENTS.md`, `CLAUDE.md` y las skills, en su propio incremento.

## 10. Transición desde las reglas anteriores

| Regla o documento | Hoy | Con Q2 adoptada |
|---|---|---|
| Q (`061ba68`) | Propuesta no vigente | Sustituida como propuesta; se conserva |
| Contrato 10 | «Del equipo», sin quórum. Autorizaciones operativas de Luis acreditadas; representación del equipo sin documentar | N3 de Luis, solo con las DF vigentes que cubran la operación. Sin ellas, mecanismo colegiado |
| Gate de F36-SBX v3, con quórum 3/3 | En vigor | En vigor hasta que un sucesor auditado lo cambie (`gate_version` 4) |
| D-02 (sucesor B-01) | No emitida | Un RD anclado a la especificación S auditada y al RR, si las DF cubren D-02 |
| D-09 (modelo de gobierno) | No emitida | Resuelta por la adopción de Q2, o por mantener el 3/3 |
| U-01 a U-05 de Q | Pendientes | U-01 pasa a R-01; U-02, a las CM y DF; U-03, a la revisión diferenciada de V (entregada sobre `729babb`, con correcciones requeridas); U-04, al RR. U-05 no aplica, porque Q2 mantiene a los tres integrantes |
| `AGENTS.md`, `CLAUDE.md` y skills | Sin cambios | Deltas de la sección 12, en un incremento propio |

## 11. Evidencias que no se reinterpretan

- **Las capturas de F34C (G0-09 y G0-14).** Son la aprobación de ADR-005 y del threat model tal como se registró. No son conformidades con Q2 ni delegaciones de operaciones Git, y no se fechan de nuevo ni se reatribuyen.
- **La respuesta de G0-12.** Sigue sin evidencia archivada y con una identidad no verificable.
- **Las declaraciones del 27/10/2026.** Se conservan tal como constan en Q y en su auditoría; la discrepancia la aclara R-01.
- **Las auditorías.** AF1 a AF6, DOC-AF6, SEG-01 a SEG-04, la de Q (UNI-M01 a UNI-I02) y la de Q2 (Q2-M01 a Q2-L02) son revisiones técnicas de sesiones de IA, nunca aprobaciones humanas.
- **Las integraciones y publicaciones de SEG-01 a SEG-04.** Son autorizaciones operativas de Luis, ni votos del equipo ni un 3/3.
- **La integración de AF5 (`5545694` y `55f758e`)** y la instrucción operativa (b) de D-01, que no es una decisión formal, quedan tal como constan.
- **La autoría Git, tal como consta.** Los 6 commits con la identidad de Fredy no se reatribuyen sin una declaración de las personas implicadas.
- **Lo publicado y congelado.** Los tags `v1.0.0-academic` y `v1.1.0-academic` y sus informes, la evidencia congelada de F35-SBX y las ejecuciones de CI.

## 12. Deltas propuestos, sin aplicar

| Documento | Delta propuesto | Procedimiento |
|---|---|---|
| [`AGENTS.md`](../../../../AGENTS.md), línea 76 | «ChatGPT: coordinación, planes y borradores de prompts; las decisiones son de Luis, responsable técnico» | Incremento documental propio, auditado, tras el RR |
| [`multi-agent-workflow.md`](../../../v1.1/multi-agent-workflow.md), línea 81 | El mismo cambio en la tabla de roles | Ídem |
| [`CLAUDE.md`](../../../../CLAUDE.md) | Conservar literal la línea `Integrantes: …`, que la regla GOV exige (`CLAUDE_MEMBERS`, `validate_f36sbx.py:82`). Añadir: «Luis Vila Meza es el responsable técnico de desarrollo; Fredy Coronacion y Anthony Peña, integrantes académicos». En el contrato 10, dejar la representación sujeta a las DF vigentes (N3). Sincronizar el bloque de estado | GOV comprueba invariantes, no prohíbe editar: un incremento documental autorizado puede aplicarlo si conserva los invariantes y los estados. Cambiar estados o el mecanismo de autorización exige su propio procedimiento. Dentro de H, D-07 organiza la sincronización |
| `.claude/skills/project-guardian/SKILL.md`, §6 | «`push`, `merge`, release o tag: autorización explícita conforme al contrato 10; con Q2 adoptada, la del responsable técnico dentro de sus delegaciones vigentes» | `AGENTS.md` exige una fase y una autorización para modificar skills; incremento propio |
| Gate de F36-SBX, §8.1 a §8.5, y esquema `f36sbx-team-evidence` | `gate_version` 4 y esquema v3: los `approvals` 3/3 pasan a un RD que cita el RR y las DF, en orden de fechas. ADR y alcance C, no delegables | Sucesor B-01 (D-02b), que habilita la transición, dentro de H y auditado |
| `validate_f36sbx.py` | `MEMBERS` (`:81`), `CLAUDE_MEMBERS` (`:82`), `approval_errors()` (`:2367`), el revisor de FG-10 (`:2566`) y la regla GATE (B-01, `:2877`) | Ídem, con RED y GREEN. Las correcciones independientes del validador, como AF6-L01 y AF6-L02, van por su propio incremento (reconciliación §6) |
| Borrador D-02 y especificación B-01 (`1d5d6aa`) | Añadir la variante de Q2, propagar T-08 al plan de pruebas y corregir D-02b y D-02c según la sección 8 (UNI-M04, UNI-M05 y UNI-L02) | Al integrar la preparación (D-08) |

## 13. Plantillas sin firmar

**R-01. Declaración del responsable técnico.** La completa y fecha Luis, con su propio acto.

| Campo | Valor |
|---|---|
| Composición real del equipo | PENDIENTE |
| Aclaración de la discrepancia con las declaraciones del 27/10/2026 | PENDIENTE |
| Rol de cada integrante en el desarrollo | PENDIENTE |
| Uso de los entornos de trabajo (PC principal, PC secundario y macOS) | PENDIENTE |
| Uso de IA: Claude Code implementa, Codex revisa y ChatGPT coordina | PENDIENTE |
| Fecha y canal | PENDIENTE |

**CM-01 a CM-03. Conformidad con una versión fijada.** Una por integrante y emitida por él.

| Campo | Luis Vila Meza | Fredy Coronacion | Anthony Peña |
|---|---|---|---|
| Versión de Q2: commit y árbol | PENDIENTE | PENDIENTE | PENDIENTE |
| Decisión: conforme, conforme con condiciones o no conforme | PENDIENTE | PENDIENTE | PENDIENTE |
| Condiciones | PENDIENTE | PENDIENTE | PENDIENTE |
| Fecha y canal | PENDIENTE | PENDIENTE | PENDIENTE |
| Evidencia y su SHA-256 | PENDIENTE | PENDIENTE | PENDIENTE |

**DF-02 y DF-03. Delegación en el responsable técnico.** Independiente de la conformidad, y puede ser nula.

| Campo | Fredy Coronacion | Anthony Peña |
|---|---|---|
| Facultades delegadas (lista cerrada) | PENDIENTE | PENDIENTE |
| Límites | PENDIENTE | PENDIENTE |
| Inicio y fin, o revocabilidad | PENDIENTE | PENDIENTE |
| Fecha y canal | PENDIENTE | PENDIENTE |
| Evidencia y su SHA-256 | PENDIENTE | PENDIENTE |

**RR. Registro raíz de adopción.** Es solo su estructura: no se crea hasta que se cumplan las reglas de 9.3.

| Campo | Valor |
|---|---|
| Versión V: commit, árbol y ruta de la propuesta | PENDIENTE |
| Informe aplicable: ubicación, SHA-256, veredicto y recuentos | PENDIENTE |
| R-01, CM-01 a CM-03 y DF-02 y DF-03, con sus hashes | PENDIENTE |
| Condiciones y su cumplimiento | PENDIENTE |
| Facultades delegadas efectivas (intersección) | PENDIENTE |
| Fecha y resultado (ADOPTADA o NO ADOPTADA) | PENDIENTE |

Sin firmas. Ninguna de estas plantillas es evidencia mientras su titular no la emita.

## 14. Lo que Q2 no hace

- No se adopta ni se declara aprobada.
- No modifica contratos, validadores, estados, evidencias ni documentos de gobierno.
- No crea votos, firmas, delegaciones ni identidades.
- No afirma requisitos del curso no acreditados ni permisos del docente.
- No reinterpreta la historia.
- No autoriza F37-SBX, datos reales, el alcance C, scoring, ranking, recomendación ni selección automática.
