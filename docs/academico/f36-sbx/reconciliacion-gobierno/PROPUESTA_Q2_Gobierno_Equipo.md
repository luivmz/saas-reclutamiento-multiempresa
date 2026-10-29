# PROPUESTA — NO VIGENTE — PENDIENTE DE ADOPCIÓN

## Q2 — Gobierno académico de tres integrantes con un responsable técnico (sucesora de Q)

> **PROPUESTA — NO VIGENTE — PENDIENTE DE ADOPCIÓN.** Documento del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`, creada desde `develop` = `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9`.
>
> **No modifica** `AGENTS.md`, `CLAUDE.md`, las skills, el contrato, el esquema ni el validador de F36-SBX, ni ningún estado o evidencia. Mientras no se adopte por el procedimiento de la sección 9, rigen las reglas vigentes: F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA y el quórum 3/3 del gate. Los hechos citados están verificados en el [informe de reconciliación](F36SBX_Reconciliacion_Estado_Gobierno.md).

## 1. Relación con Q

Q es la propuesta `061ba68:docs/academico/f36-sbx/preparacion-gate/F36SBX_Propuesta_Gobierno_Unipersonal.md`. Respondía a la declaración del 27/10/2026 de que el proyecto lo desarrolla una sola persona real, y distinguía dos lecturas sin elegir entre ellas:

- **(a)** tres integrantes reales, de los que solo uno desarrolla;
- **(b)** una sola persona real.

Las declaraciones posteriores, recibidas en las peticiones del 28/10/2026 (SEG-01 y SEG-02) y del 29/10/2026, dicen lo siguiente [R]:

- el equipo tiene tres integrantes reales: Luis Vila Meza, Fredy Coronacion y Anthony Peña;
- Luis es el único desarrollador técnico y toma las decisiones ordinarias de programación.

Eso corresponde a la lectura (a), así que el modelo unipersonal deja de ser el adecuado. **Q2 sustituye a Q como propuesta.** Q no se adoptó, se conserva como registro y no se edita.

Q2 reutiliza de Q:

- el registro de decisiones con fecha real;
- la separación entre la auditoría técnica y la decisión humana;
- la prohibición de presentar una IA como persona;
- la adopción prospectiva, sin efecto retroactivo.

| Tema | Q | Q2 |
|---|---|---|
| Composición | Una persona real, o una lectura sin determinar | Tres integrantes reales; uno es el responsable técnico |
| Quórum 3/3 del gate | «Imposible de cumplir con autenticidad» en la lectura (b) | Posible solo si los tres actúan de verdad. Q2 no lo simula ni lo da por cumplido |
| Fredy y Anthony | Integrantes «no activos» | Integrantes académicos, sin contribuciones, firmas ni aprobaciones técnicas atribuidas |
| Autoridad para enmendar | La conformidad de los otros dos (a) o el docente (b) | La conformidad expresa de Fredy y de Anthony. El docente, solo si una fuente lo exige o el equipo decide consultarle |
| Decisiones técnicas ordinarias | Del responsable, dentro del modelo unipersonal | Del responsable técnico, sin quórum, como ya ocurre |
| Expediente para el docente | Imprescindible en la lectura (b) | No es condición de Q2, porque ninguna fuente lo exige. Es opcional |

## 2. Hechos de partida

- **[H] Equipo declarado ante el curso:** Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio. En este documento, Fredy Coronacion, Anthony Peña y Luis Vila Meza son la forma corta de esos mismos nombres.
- **[H] Autoría Git.** Tienen como autor a «Luis Vila Meza»:
  - los 32 commits de F36-SBX hasta AF5;
  - los 8 de AF6, H y Q;
  - los 20 de SEG-01 a SEG-04.

  Seis commits del 20/10/2026 figuran con la identidad «Coronacion Meza Fredy». Solo están en `origin/codex/mejoras-sonarqube`, sin integrar, y Git declara la identidad, no la autentica.
- **[H] Sin norma externa.** No consta ninguna norma del curso sobre la composición del equipo, el uso de IA ni la aprobación de decisiones técnicas: está no acreditada (reconciliación §5.1).
- **[H] Origen del 3/3.** El quórum 3/3 de F36-SBX es interno: nace en F34A, se cumplió en F34C y lo hereda el gate §8.1.
- **[H] Práctica reciente.** Las integraciones y publicaciones de SEG-01 a SEG-04 se hicieron con la autorización expresa de Luis, por operación.

## 3. Roles

| Rol | Quién | Puede | No puede |
|---|---|---|---|
| Responsable técnico de desarrollo | Luis Vila Meza | Decidir en N1 a N3 (sección 4), proponer cambios de gobierno, registrar sus decisiones y aceptar o rechazar hallazgos, siempre con justificación | Auditarse a sí mismo; decidir en N4 por los otros dos; decidir en N5 |
| Integrantes académicos | Fredy Coronacion y Anthony Peña | Participar en N4 con actos propios: aprobar, rechazar, abstenerse, delegar o revocar | Ser sustituidos por otra persona, un dispositivo o una IA. Que se les atribuyan contribuciones técnicas, firmas o aprobaciones que no hicieron |
| Claude Code | Sesiones de implementación | Diseñar, implementar, probar, documentar y preparar borradores | Decidir, aprobar, votar, auditar su propio trabajo o registrar actos humanos que no ocurrieron |
| Codex | Sesiones de revisión separadas | Auditar de forma técnica y diferenciada, con informe, veredicto y manifiesto | Decidir o votar; presentarse como integrante, docente o revisor humano |
| ChatGPT | Coordinación | Redactar planes y prompts y ordenar el trabajo | Decidir: sus propuestas valen cuando Luis las asume |
| Docente | Autoridad académica externa | Evaluar los entregables; reconocer o no lo que se le consulte | — (sus permisos no se presumen) |

## 4. Niveles de decisión

| Nivel | Qué cubre | Quién decide | Requisitos previos | Registro |
|---|---|---|---|---|
| **N1** Técnica ordinaria | Diseño e implementación, pruebas, commits, ramas `feature/*`, `fix/*`, `docs/*` y `chore/*`, worktrees, refactors, priorización de la deuda técnica, y aceptar o rechazar sugerencias de una IA | Luis | Contratos 1 a 10 y la regresión de `project-guardian` | El commit y el documento del incremento |
| **N2** Cambio con revisión diferenciada | Seguridad, autorización y multiempresa; la auditoría (`AuditLogger` y su trigger); el modelo de datos y las migraciones; el ML (RF-29) y su contrato; validadores y gates; dependencias; CI; documentos de gobierno | Luis, después de la revisión | Una auditoría técnica de Codex sobre el commit exacto, sin BLOCKER, HIGH ni MEDIUM que exija corrección abiertos, y con los LOW y los INFO registrados | Un RD que cita el informe y su hash |
| **N3** Integración y publicación | Merge a `develop`, push de `develop`, merge a `main`, tags y releases | Luis, si D-11 se resuelve así | El candidato auditado (N2 si aplica), el árbol idéntico al auditado y una autorización explícita por operación. Después del push, la CI en verde | Mensaje del merge y un RD |
| **N4** Académica del equipo | Adoptar o cambiar este modelo. Las declaraciones ante el curso (composición, contribuciones y uso de IA). Presentar un entregable o una release como trabajo del equipo. Los criterios de equipo de F36-SBX mientras rija el 3/3 | Los tres integrantes, cada uno con un acto propio, o quien reciba una delegación expresa de cada uno, con un alcance definido | Que cada integrante tenga información suficiente antes de actuar | RA con la evidencia de cada acto |
| **N5** Externa | G0-02, G0-03 y G0-12; las aprobaciones jurídicas, de privacidad o institucionales; los datos reales; producción; el alcance C del producto | Nadie del equipo: queda fuera de su autoridad | — | Solo se registra lo recibido, con su evidencia |

**N1 no necesita autorización del docente ni de los otros integrantes:** ninguna fuente lo exige. **N3**, mientras D-11 no se resuelva, sigue necesitando una autorización explícita por operación, como en SEG-01 a SEG-04. **En N4**, una delegación no se presume ni se amplía: tiene un alcance y una fecha, y es revocable. Aprobar un ADR sucesor que excepcione ADR-005, o cualquier decisión de alcance C, **no es delegable**: ADR-005 lo revisaron los tres integrantes (F34C).

## 5. Revisión técnica diferenciada

1. **Sesión separada.** La sesión que audita no es la que implementó ni la que preparó lo auditado.
2. **Identidad.** Examina un commit fijo, con su SHA y su árbol, y lo declara en el informe.
3. **Método propio.** Usa sus propias pruebas, además de las oficiales.
4. **Evidencia.** Un informe con su manifiesto SHA-256. Si se versiona, basta un resumen con los hashes.
5. **Límites declarados.** Un mismo operador humano orquesta las sesiones, y las auditorías se ejecutaron en el mismo PC Windows y su WSL. Que los proveedores sean distintos reduce los errores correlacionados, pero no los elimina, y no hay independencia institucional.
6. **Registro.** Luis comprueba la sesión, el manifiesto y el commit, y registra su decisión sobre cada hallazgo, en RD o en RX.
7. **Uso de IA declarado.**
   - Los commits llevan las líneas `Co-Authored-By`.
   - Los documentos dicen que implementa Claude Code y revisa Codex.
   - Cómo se declara la asistencia de IA en los entregables académicos lo decide el equipo (N4).

Una revisión de IA nunca es una aprobación humana, un voto ni una validación externa. La auditoría de Q2 (E-04) la hace una sesión que no redactó Q2.

## 6. Validaciones externas

Solo donde corresponde: en N5, y donde una fuente del curso lo exija. No se pide autorización del docente para commits, pruebas ni decisiones técnicas ordinarias, porque ninguna fuente aplicable lo exige.

La consulta al docente es **opcional**, por ejemplo para un reconocimiento externo de la delegación o de la declaración de contribuciones (N4). Si el equipo la hace, la respuesta se conserva tal como se recibió, con su fecha y su hash.

## 7. Registros

| Registro | ID | Campos | Quién lo escribe | Regla |
|---|---|---|---|---|
| Decisiones del responsable técnico | RD-NNN | Fecha real, nivel (N1 a N3), alcance (rama, commit y árbol), decisión y evidencia (informe, hash y CI) | Luis, o la sesión que transcribe literalmente una decisión expresa suya, citando el canal y la fecha | Nunca anterior a la evidencia que cita; no se retrofecha |
| Discrepancias | RX-NNN | Hallazgo o propuesta; su fuente (auditoría, IA o integrante); la postura de Luis, el motivo, el riesgo que se acepta y el seguimiento | Luis | Ningún hallazgo se descarta en silencio |
| Excepciones | RE-NNN | La regla exceptuada, el motivo, el alcance, la duración y el control compensatorio | Luis (N1 a N3) o los tres integrantes (N4) | No se exceptúan los contratos 1 a 10 ni las prohibiciones duras del charter |
| Actos de los integrantes | RA-NNN | El integrante, el acto (aprueba, rechaza, se abstiene, delega o revoca), el alcance, la fecha, el canal y la evidencia con su SHA-256 | Cada integrante emite su acto; el registro solo lo transcribe y conserva | Nadie registra un acto en nombre de otro. Un mensaje o una captura se conserva con su hash, como en F34C |

Hasta la adopción, los RD siguen viviendo en el documento de cada incremento, como en SEG-01 a SEG-04. El índice de registros se crearía en el incremento de la sección 9.

## 8. Aplicación a F36-SBX

| Camino | Condición | FG-03, FG-10 y FG-12 | D-02b (sucesor B-01) |
|---|---|---|---|
| **Contrato vigente** (sin adoptar Q2, o sin delegación) | El gate v3 tal como está | Tres votos reales de las tres identidades exactas, cada uno emitido por su titular | Autorización explícita del equipo, con el 3/3 como práctica |
| **Q2 con delegación** | Q2 adoptada y RA de Fredy y de Anthony que cubran el criterio | Un contrato sucesor (`gate_version` 4 y esquema v3) sustituye los `approvals` 3/3 por un RD de Luis que cita los RA y una FG-02 favorable sobre H. Las fechas van en orden: adopción, informe de FG-02 y decisión. El ADR y el alcance C quedan fuera de la delegación | Un RD de Luis posterior a una auditoría de la especificación, si la delegación cubre D-02 |
| **Ninguno** | Ni votos ni delegación | Sin registro | Sin autorización |

En el tercer caso, el gate sigue NO SUPERADO y F37-SBX sigue bloqueada. Es el resultado correcto de un contrato que falla cerrado.

Valen en los tres caminos:

- **FG-02.** El auditor puede ser una sesión de Codex del tipo `sesion_de_auditoria_independiente`, nunca presentada como persona. Fredy o Anthony podrían figurar como `integrante_no_autor` solo si hacen de verdad una auditoría técnica; no se presume.
- **FG-10.** El revisor de la cadena de suministro puede ser Luis, que es un integrante.
- **Ninguna aprobación se simula.**

## 9. Adopción: procedimiento, autoridad y entrada en vigor

1. **P1 (E-04).** Auditoría técnica independiente de Q2, sin BLOCKER, HIGH ni MEDIUM que exija corrección abiertos.
2. **P2 (R-01).** Declaración fechada de Luis sobre la composición y los roles (plantilla, sección 13).
3. **P3 (C-01 y C-02).** Conformidad expresa y fechada de Fredy y de Anthony, cada uno por su propio canal, con el alcance de delegación que acepte: total, parcial o ninguno. Se conserva con su SHA-256.
4. **P4. Registro de adopción.** La autoridad son los tres integrantes, cada uno con su acto. Q2 entra en vigor en la fecha del último acto exigido, solo hacia adelante. Si Fredy o Anthony no da su conformidad, Q2 no se adopta. N1 sigue como hoy, porque ninguna regla lo restringe. D-11 sigue abierta, y el equipo puede, si quiere, consultar al docente.
5. **P5. Incrementos sucesores auditados** que apliquen los deltas de la sección 12:
   - la parte del gate, dentro de H, con D-02b bajo el modelo adoptado;
   - la de `AGENTS.md`, `CLAUDE.md` y las skills, en su propio incremento.

## 10. Transición desde las reglas anteriores

| Regla o documento | Hoy | Con Q2 adoptada |
|---|---|---|
| Q (`061ba68`) | Propuesta no vigente | Sustituida como propuesta; se conserva |
| Contrato 10 | «Del equipo», sin quórum. En la práctica, autorización de Luis por operación | N3 de Luis, por delegación expresa (D-11) |
| Gate de F36-SBX v3, con quórum 3/3 | En vigor | En vigor hasta que un sucesor auditado lo cambie (`gate_version` 4) |
| D-02 (sucesor B-01) | No emitida; la autoriza el equipo | Un RD de Luis tras auditoría, si la delegación la cubre |
| D-09 (modelo de gobierno) | No emitida | Resuelta por la adopción de Q2, o por mantener el 3/3 |
| U-01 a U-05 de Q | Pendientes | U-01 pasa a R-01; U-02, a C-01 y C-02; U-03, a E-04 (la auditoría de Q2); U-04, a P4. U-05 no aplica en la lectura (a) |
| `AGENTS.md`, `CLAUDE.md` y skills | Sin cambios | Deltas de la sección 12, en un incremento propio |

## 11. Evidencias que no se reinterpretan

- **Las capturas de F34C (G0-09 y G0-14).** Son la aprobación de los tres integrantes tal como se registró. La lectura (a) conserva su sentido. No se fechan de nuevo, no se reatribuyen y no se editan.
- **La respuesta de G0-12.** Sigue sin evidencia archivada y con una identidad no verificable.
- **Las auditorías de AF1 a AF6, DOC-AF6, SEG-01 a SEG-04 y Q.** Son revisiones técnicas de sesiones de IA, nunca aprobaciones humanas.
- **Las integraciones y publicaciones de SEG-01 a SEG-04.** Son autorizaciones de Luis, ni votos del equipo ni un 3/3.
- **La integración de AF5 (`5545694` y `55f758e`)** y la instrucción operativa (b) de D-01, que no es una decisión formal. Quedan tal como constan.
- **La autoría Git, tal como consta.** Los 6 commits con la identidad de Fredy no se reatribuyen sin una declaración de las personas implicadas (E-05).
- **Lo publicado y congelado.** Los tags `v1.0.0-academic` y `v1.1.0-academic` y sus informes, la evidencia congelada de F35-SBX y las ejecuciones de CI.

## 12. Deltas propuestos, sin aplicar

| Documento | Delta propuesto | Procedimiento |
|---|---|---|
| [`AGENTS.md`](../../../../AGENTS.md), línea 76 | «ChatGPT: coordinación, planes y borradores de prompts; las decisiones son de Luis, responsable técnico» | Incremento propio auditado, tras P4 |
| [`multi-agent-workflow.md`](../../../v1.1/multi-agent-workflow.md), línea 81 | El mismo cambio en la tabla de roles | Ídem |
| [`CLAUDE.md`](../../../../CLAUDE.md) | Conservar literal la línea `Integrantes: …`, que la regla GOV exige (`CLAUDE_MEMBERS`, `validate_f36sbx.py:82`). Añadir: «Luis Vila Meza es el responsable técnico de desarrollo; Fredy Coronacion y Anthony Peña, integrantes académicos». En el contrato 10: «autorización explícita del responsable técnico, por operación (N3)». Sincronizar el bloque de estado (D-07) | Los protege la regla GOV, así que entra en el sucesor de H (D-07) |
| `.claude/skills/project-guardian/SKILL.md`, §6 | «`push`, `merge`, release o tag: autorización explícita del responsable técnico (N3)» | `AGENTS.md` exige una fase y una autorización para modificar skills; incremento propio |
| Gate de F36-SBX, §8.1 a §8.5, y esquema `f36sbx-team-evidence` | `gate_version` 4 y esquema v3: los `approvals` 3/3 pasan a ser un RD con los RA de la delegación, en orden de fechas; ADR y alcance C, no delegables | Sucesor B-01 (D-02b) dentro de H, auditado |
| `validate_f36sbx.py` | `MEMBERS` (`:81`), `CLAUDE_MEMBERS` (`:82`), `approval_errors()` (`:2367`), el revisor de FG-10 (`:2566`) y la regla GATE (B-01, `:2877`) | Ídem, con RED y GREEN |
| Borrador D-02 (`1d5d6aa`) | Añadir la variante de Q2 junto a la del contrato vigente | Al integrar la preparación (D-08) |

## 13. Plantillas sin firmar

**R-01. Declaración del responsable técnico.** La completa y fecha Luis, con su propio acto.

| Campo | Valor |
|---|---|
| Composición real del equipo | PENDIENTE |
| Rol de cada integrante en el desarrollo | PENDIENTE |
| Uso de los entornos de trabajo (PC principal, PC secundario y macOS) | PENDIENTE |
| Uso de IA: Claude Code implementa, Codex revisa y ChatGPT coordina | PENDIENTE |
| Fecha y canal | PENDIENTE |

**C-01 y C-02. Conformidad de cada integrante académico.** Una por persona y emitida por ella.

| Campo | Fredy Coronacion | Anthony Peña |
|---|---|---|
| Conformidad con Q2 (sí, no o parcial) | PENDIENTE | PENDIENTE |
| Alcance de la delegación en Luis (N3, N4 delegable, ninguno) | PENDIENTE | PENDIENTE |
| Fecha y canal | PENDIENTE | PENDIENTE |
| Evidencia y su SHA-256 | PENDIENTE | PENDIENTE |

Sin firmas. Ninguna de estas plantillas es evidencia mientras su titular no la emita.

## 14. Lo que Q2 no hace

- No se adopta ni se declara aprobada.
- No modifica contratos, validadores, estados, evidencias ni documentos de gobierno.
- No crea votos, firmas, delegaciones ni identidades.
- No afirma requisitos del curso ni permisos del docente.
- No reinterpreta la historia.
- No autoriza F37-SBX, datos reales, el alcance C, scoring, ranking, recomendación ni selección automática.
