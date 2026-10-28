# F36-SBX — Matriz de preparación del gate (FG-02, FG-03, FG-10 y FG-12)

> Documento de trabajo del 27/10/2026, creado en la rama `docs/f36-sbx-gate-preparacion-af6`, desde `main` = `55f758e013e1852de8c8daa5d6fde95e39b02b0d`, y actualizado en `feature/f36-sbx-gate-transition-h` con las observaciones DOC-AF6-L01, DOC-AF6-L02 y DOC-AF6-I01 de su auditoría documental (sección 10). **No registra evidencia, no cambia ningún estado y no autoriza nada.** Analiza qué exige el contrato vigente para cada criterio EQUIPO pendiente y qué acción humana falta. Fuentes normativas: [gate sucesor](../F36SBX_Gate_Sucesor.md), [estado del gate](../gate/f36sbx_gate_state.json), [esquema de la evidencia de equipo](../gate/f36sbx_team_evidence_schema.json) (`f36sbx-team-evidence/v2`) y [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py). Si este documento difiere de esas fuentes, mandan ellas.

**Estado vigente, sin cambios:** F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; FG-02, FG-03, FG-10 y FG-12 en PENDIENTE, con `evidence = null`; `candidate_commit = null`; `f37_authorized_ei = null`; F37-SBX = BLOQUEADA.

## 1. Categorías de evidencia que no son equivalentes

| Categoría | Qué es | Ejemplos en F36-SBX | Qué puede satisfacer |
|---|---|---|---|
| Evidencia técnica | Resultado reproducible de herramientas y auditorías | El validador (59/0), las baterías, la [sexta auditoría](../F36SBX_Auditoria_AF6.md) y las CI | Los criterios AUTO (FG-01, FG-04..FG-09, FG-11, FG-13 y FG-14). Para FG-02 es la **materia** del informe, no el registro |
| Evidencia académica sintética | Datos y autorizaciones fabricados a propósito para probar el oracle | Fixtures en memoria y en clones desechables de las baterías y de la auditoría | Nada. Nunca se escribe en `gate/evidencia/` |
| Aprobación humana del equipo | Acto fechado de los tres integrantes, con su voto individual | Los registros de FG-03 y FG-10, y el de FG-12 cuando está en CUMPLE, con `approvals` 3/3 | FG-03, FG-10 y FG-12, solo con el formato del gate |
| Autorización institucional externa | Decisión de un tercero con autoridad (jurídica, de privacidad, institucional) | G0-02, G0-03 y G0-12 (PENDIENTE EXTERNO) | Ningún criterio del F36-SBX-GATE: el gate es independiente de la G0 real y no la da por resuelta |
| Autorización para ejecutar capacidades experimentales | Decisión del equipo sobre qué EI puede construir F37-SBX | `authorized_ei` de FG-03, el ADR sucesor de FG-12 y las dependencias de FG-10 | El inicio de F37-SBX con esas EI y nada más. No autoriza producción, datos reales ni alcance C del producto |

## 2. Bloqueos estructurales previos a cualquier registro

Antes de analizar cada criterio, tres hechos del contrato vigente condicionan el plan.

**B-01. Esta versión del validador exige que el gobierno declare NO SUPERADO.** La regla GATE comprueba que el resultado sea NO SUPERADO y que lo declaren el gate, su JSON y el gobierno. El [gate §9](../F36SBX_Gate_Sucesor.md#9-vínculo-con-el-candidato-auditado) lo dice expresamente: «declarar el gate SUPERADO necesita un incremento sucesor auditado que actualice el gobierno y el validador». Así que, aunque los cuatro criterios tuvieran evidencia auténtica, F36-SBX-GATE no podría pasar a SUPERADO sin ese incremento sucesor (decisión D-02). La [especificación del sucesor B-01](F36SBX_Especificacion_Sucesor_B01.md) detalla por qué no basta con retirar una comprobación.

**B-02. El candidato del gate solo admite cambios en las rutas de registro.** Entre `candidate_commit` y el árbol que se valida solo pueden cambiar `gate/evidencia/`, `gate/f36sbx_gate_state.json` y la columna Estado de la tabla FG del gate (gate §9). El árbol de `main` (`55f758e`) es idéntico al del candidato auditado `4a2b2d7`, pero esta preparación y el sucesor cambian el paquete, las herramientas y el gobierno. Por eso **`4a2b2d7` no puede ser el candidato del gate si se incorporan**. La auditoría documental lo reprodujo: con el puntero en `4a2b2d7`, el validador pasa de 59/0 a 58/1 en cuanto aparecen estos documentos, sea cual sea el orden de registro.

**B-03. El formato de FG-02 exige un informe dentro de `gate/evidencia/`.** El informe AF6 no tiene las secciones ni el bloque canónico del gate §8.6, y no está en el repositorio. Si el equipo lo redactara de nuevo con ese formato en nombre del auditor, sería un documento del equipo y no del auditor: un riesgo de evidencia no auténtica (decisión D-04).

### 2.1 Secuencia hacia el candidato H

Con la estrategia D-01 (b), un candidato final nuevo H, el único orden que conserva FG-02 es este:

1. **Autorizar los cambios normativos:** el sucesor B-01 (D-02), la deuda AF6 (D-05), el registro de deuda (D-03), el alcance de F37-SBX en lo que afecte a H (D-06) y la sincronización del gobierno (D-07).
2. **Incorporar** esta preparación AF6 y el sucesor.
3. **Completar todos los cambios materiales necesarios:** el validador sucesor, sus pruebas, el gobierno sincronizado, la documentación y, si se autoriza alguna EI CONDITIONAL de alcance C, el ADR sucesor aprobado.
4. **Fijar el candidato final H:** un commit real, con su SHA y su árbol. Desde ese momento, cualquier corrección material produce otro candidato, que exige otra auditoría. Nada de amend, rebase ni sustitución silenciosa.
5. **Auditar H de forma independiente.** El auditor elegible emite su informe canónico sobre H.
6. **Obtener las decisiones y la evidencia auténticas referidas a H:** FG-02, FG-03, FG-10 y FG-12 citan H.
7. **Registrar después de H únicamente** los cambios que permite el contrato sucesor auditado.
8. **Validar** el árbol de registro con el validador de H y cerrar el gate si corresponde. Integrar solo con autorización explícita.

**Una auditoría de AF5 no puede reutilizarse como auditoría de H.** Ni la sexta auditoría (sobre `4a2b2d7`) ni la auditoría documental de esta preparación (sobre `88fd3d2`) examinaron H. Cambiar el SHA de su informe, o apoyarse en que dos árboles coinciden, no las convierte en una auditoría de H. Siguen valiendo como antecedentes técnicos e históricos.

## 3. Análisis por criterio

### 3.1 FG-02 — auditoría independiente

| Punto | Análisis |
|---|---|
| 1. Definición contractual | «Auditoría independiente del paquete F36-SBX con 0 BLOCKER, 0 HIGH y 0 MEDIUM que requiera corrección abiertos» (gate §3). Tipo EQUIPO |
| 2. Estado actual | PENDIENTE, `evidence = null`. Hay una auditoría técnica favorable (AF6) sobre `4a2b2d7`, sin registrar, que no sirve para H (sección 2.1) |
| 3. Evidencia auténtica requerida | `gate/evidencia/FG-02.json` con `auditor {name, kind, independent_of_candidate}`, `audit_report {path, sha256}`, `verdict` y `findings_open {blocker, high, medium_requiring_fix, medium_accepted, low}` (gate §8.2), más el informe `.md` citado |
| 4. Autoridad | El auditor emite el informe y su veredicto. Puede ser una persona (`docente`, `integrante_no_autor` o `revisor_academico_externo`) o una sesión automatizada de tipo `sesion_de_auditoria_independiente`, distinta de la sesión que implementó o preparó el candidato. Las personas del equipo verifican la procedencia, el alcance y la independencia, y registran el criterio. FG-02 no tiene quórum 3/3 propio |
| 5. Formato y ubicación | JSON estricto con exactamente los campos del esquema. El informe es un `.md` dentro de `gate/evidencia/`, en UTF-8 NFC, con un título de nivel 1, las secciones «Alcance», «Hallazgos» y «Conclusión», al menos 200 letras fuera del bloque y un único bloque `f36sbx-audit-metadata` (`f36sbx-audit-report/v1`) coherente con el registro |
| 6. Commit, hashes y procedencia | `candidate_commit` del registro y del bloque igual al del estado del gate. SHA-256 del informe entero. `recorded_at` no anterior a la fecha del candidato. `report_date` entre esa fecha y `recorded_at`. El informe no puede cambiar después del registro |
| 7. Dependencias | Ninguna contractual con otros FG. Depende de la decisión D-01 (qué commit es el candidato) |
| 8. Riesgos de aceptación inválida | (a) Tratar el informe AF6 como registro por su mera existencia, o como auditoría de H. (b) Un informe redactado por el equipo en nombre del auditor. (c) Un auditor que no es independiente: los 32 commits de F36-SBX hasta AF5 tienen como autor Git a «Luis Vila Meza», que no puede figurar como `integrante_no_autor` de ese candidato. Claude y Codex no son integrantes, docentes ni revisores externos humanos: como mucho, una sesión de auditoría independiente, y nunca la sesión implementadora. (d) Registrar contra un candidato después del cual cambia algo fuera de las rutas de registro: el vínculo falla. (e) La identidad del auditor: la guardia estructural tiene los residuos AF6-L01 y AF6-L02, así que la identidad la verifica una persona |
| 9. Acción humana pendiente | Decidir D-01 y D-04. Una vez fijado H, obtener del auditor elegible un informe sobre H con el formato del gate. El auditor, no el equipo, decide si el veredicto es `APROBADO_PARA_INTEGRACION` o `APROBADO_CON_OBSERVACIONES`. Registrar `findings_open` con los LOW que sigan abiertos. Verificar la identidad o la sesión del auditor |
| 10. Condición objetiva | El validador, con el registro y el informe en `gate/evidencia/` y FG-02 en CUMPLE, no da ningún error para FG-02 (regla GATE), y una persona del equipo ha verificado la identidad o la sesión del auditor y la autoría del informe |

### 3.2 FG-03 — autorización explícita de F37-SBX

| Punto | Análisis |
|---|---|
| 1. Definición contractual | «Autorización explícita de F37-SBX por el equipo: registro fechado, aprobación individual de los tres integrantes, lista cerrada de EI autorizadas y confirmación de la numeración (F36-M01)» |
| 2. Estado actual | PENDIENTE. `f37_authorized_ei = null`. F36-M01 sin confirmar |
| 3. Evidencia auténtica requerida | `gate/evidencia/FG-03.json` con `decision`, `authorized_ei`, `numbering_f36_m01`, `approvals` y `quorum` (gate §8.3) |
| 4. Autoridad | Los tres integrantes declarados en `CLAUDE.md` y en el esquema: `Coronacion Meza Fredy`, `Peña Arroyo Anthony` y `Vila Meza Luis Antonio`. Ningún otro rol ni ninguna sesión automatizada puede sustituirlos |
| 5. Formato y ubicación | JSON estricto en `gate/evidencia/FG-03.json`. `authorized_ei`, la lista no vacía y sin repetidos de EI ALLOWED o CONDITIONAL de la matriz, tiene que ser **igual** a `f37_authorized_ei` del estado del gate, también en el orden |
| 6. Commit, hashes y procedencia | `candidate_commit` igual al del estado. Cada aprobación `{member, vote, date}` con la fecha dentro del registro. `quorum` igual a `3/3`. La procedencia del voto (que cada persona votó de verdad) **no la comprueba el validador**: ver el [procedimiento de verificación](BORRADOR_Checklist_Evidencias_y_Verificacion.md) |
| 7. Dependencias | FG-10 y FG-12 exigen una FG-03 válida. Si `authorized_ei` contiene una EI CONDITIONAL, FG-12 no puede quedar en NO APLICA. EI-09 es CONDITIONAL de alcance B, y autorizarla exige `ei09_decision = CABE_EN_ALCANCE_B` en FG-12 |
| 8. Riesgos de aceptación inválida | Una autorización genérica sin lista. Una EI BLOCKED o desconocida. Votos registrados por una sola persona en nombre de las otras. Fechas inventadas. Confundir la autorización del sandbox con una autorización de producción o de datos reales, que el gate no puede dar (FG-13) |
| 9. Acción humana pendiente | Reunión del equipo. Confirmar o cambiar la numeración F36-M01. Decidir la lista cerrada de EI para F37-SBX-A (y si incluye EI-09, F36-M02). Votar individualmente. La decisión puede ser negativa (`NO_AUTORIZA`) o restrictiva (una lista corta) |
| 10. Condición objetiva | Un registro con `decision = AUTORIZA_INICIO_F37_SBX`, `numbering_f36_m01 = CONFIRMADA`, tres votos `APRUEBA` de las tres identidades exactas y `authorized_ei` igual al estado, sin errores del validador, y con la procedencia de cada voto verificada por el procedimiento acordado |

### 3.3 FG-10 — dependencias

| Punto | Análisis |
|---|---|
| 1. Definición contractual | «Registro de dependencias del candidato, también para declarar que no hay ninguna nueva: versión exacta, propósito, licencia, origen, revisión de la cadena de suministro, EI relacionadas y aprobación». **Nunca es NO APLICA** |
| 2. Estado actual | PENDIENTE. F36-SBX no propone ninguna dependencia: el validador y sus baterías solo usan la biblioteca estándar |
| 3. Evidencia auténtica requerida | `gate/evidencia/FG-10.json` con `new_dependencies`, `dependencies`, `approvals` y `quorum` (gate §8.4) |
| 4. Autoridad | Los tres integrantes, 3/3, también si no hay dependencias. El revisor de la cadena de suministro de cada dependencia tiene que ser un integrante |
| 5. Formato y ubicación | Con `new_dependencies = false`: `dependencies = []`. Con `true`: cada dependencia con `name`, `version` fijada con `==`, `purpose`, `license` de la lista cerrada (Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, MIT, MPL-2.0 o PSF-2.0), `source = pypi`, `source_url` canónica, `supply_chain_review` (consulta OSV fechada, 0 vulnerabilidades abiertas, SHA-256 del artefacto y revisor), `related_ei` y `approval_status = APROBADA` |
| 6. Commit, hashes y procedencia | `candidate_commit` igual al del estado. Los SHA-256 de los artefactos se calculan sobre los artefactos reales descargados: nunca se inventan |
| 7. Dependencias | Exige una FG-03 válida. `new_dependencies = false` es incompatible con autorizar EI-10, EI-11 o EI-12. Cada EI autorizada que necesite dependencias debe quedar cubierta por una dependencia aprobada |
| 8. Riesgos de aceptación inválida | Declarar `false` y autorizar EI-10..EI-12. Una revisión OSV sin fecha o sin hacer. Un hash copiado de otra versión. Una licencia fuera de la lista |
| 9. Acción humana pendiente | Decidir, junto con FG-03, si F37-SBX-A necesita dependencias (el plan dice que no: «sin dependencias nuevas»). Si no, registrar `new_dependencies = false` con 3/3. Si las necesita, hacer la revisión real de cada una |
| 10. Condición objetiva | Un registro sin errores del validador y coherente con la lista de FG-03, con la revisión de cada dependencia hecha y fechada por un integrante |

### 3.4 FG-12 — ADR sucesor y EI-09

| Punto | Análisis |
|---|---|
| 1. Definición contractual | «ADR sucesor APROBADO para toda EI CONDITIONAL de alcance C autorizada, y decisión explícita del equipo sobre EI-09». NO APLICA **solo** si FG-03 no autoriza ninguna EI CONDITIONAL |
| 2. Estado actual | PENDIENTE. No existe ningún ADR sucesor (F36-M03) y no hay decisión sobre EI-09 (F36-M02). ADR-005 = PROPUESTA |
| 3. Evidencia auténtica requerida | **Depende del estado:** (a) en CUMPLE, `gate/evidencia/FG-12.json` con `successor_adr`, `covered_ei`, `ei09_decision`, `approvals` y `quorum` (gate §8.5) y, si hay alcance C autorizado, el ADR `.md`; (b) en NO APLICA, **ningún archivo ni votos propios**: `evidence` sigue nulo, y un `FG-12.json` presente haría fallar la regla GATE como evidencia sin citar |
| 4. Autoridad | En CUMPLE, los tres integrantes, 3/3, para el registro y para aprobar el ADR. En NO APLICA, ninguna votación propia: su condición la fija FG-03, que sí lleva sus votos. Un ADR sucesor que excepciona ADR-005 §6.4 en el sandbox no sustituye a la G0 real ni a ninguna autorización institucional |
| 5. Formato y ubicación | `successor_adr` es nulo si FG-03 no autoriza ninguna EI CONDITIONAL de alcance C. Si no, es `{id, path, sha256, status, relation_to_adr005, scope}`, con un id entre ADR-006 y ADR-099 y un ADR `.md` bajo `docs/` **que forma parte del commit candidato** y no cambia después. Ese ADR lleva el bloque `f36sbx-adr-metadata`, el estado APROBADO, la relación `EXCEPCION_SANDBOX_SINTETICA_ADR005_6_4` y el alcance `ALCANCE_C_SOLO_SINTETICO` |
| 6. Commit, hashes y procedencia | El ADR se lee del blob `candidate_commit:path` (AF3-M01, sin `refs/replace`). Su SHA-256 se calcula sobre esos bytes. Su `decided_on` no es posterior al commit candidato |
| 7. Dependencias | Exige una FG-03 válida. **El ADR tiene que estar dentro del candidato**: si se autoriza alguna EI CONDITIONAL de alcance C, el ADR se escribe y se aprueba **antes** de fijar H (D-06) |
| 8. Riesgos de aceptación inválida | Un ADR PROPUESTO tratado como aprobado. Un ADR añadido después del candidato. Poner FG-12 en NO APLICA y autorizar EI-09 u otra EI CONDITIONAL. Fabricar un `FG-12.json` o una votación para rellenar un NO APLICA. Confundir una excepción del sandbox con el alcance C del producto, que sigue BLOQUEADO |
| 9. Acción humana pendiente | Decidir F36-M02: si EI-09 cabe en el alcance B. Decidir si F37-SBX-B entra en esta autorización: el plan la deja para después de cerrar F37-SBX-A. Si entra, redactar y votar el ADR sucesor antes de H. Si FG-03 solo autoriza EI ALLOWED, FG-12 queda en NO APLICA, sin archivo ni votos |
| 10. Condición objetiva | Una de dos: (a) FG-12 en NO APLICA, con FG-03 en CUMPLE, sin ninguna EI CONDITIONAL autorizada y sin `FG-12.json`; o (b) FG-12 en CUMPLE con un registro 3/3 sin errores del validador, con el ADR APROBADO en H si hay alcance C, y con `ei09_decision = CABE_EN_ALCANCE_B` si se autoriza EI-09 |

## 4. Matriz de seguimiento

| Criterio | Pendiente porque | Evidencia que falta | Interviene | Verificación de autenticidad | Decisiones negativas o restrictivas posibles | No automatizable | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
| FG-02 | Nadie ha registrado una auditoría con el formato del gate; el candidato H no existe todavía | Informe del auditor elegible sobre H, con el formato 8.6, en `gate/evidencia/`, y su registro | Auditor independiente (persona o sesión elegible); el equipo verifica y registra | Autoría del informe confirmada por el auditor; SHA-256 del informe; identidad o sesión del auditor revisada por una persona | `NO_APROBADO_PARA_INTEGRACION`; hallazgos que exijan corrección; decidir que el auditor no es independiente | La verificación de procedencia e independencia y el registro | POR DESIGNAR | PENDIENTE |
| FG-03 | No hay decisión del equipo ni lista de EI | Registro con decisión, lista cerrada, numeración y 3 votos | Los tres integrantes | Voto individual de cada persona por el canal acordado; acta firmada fuera del repositorio | `NO_AUTORIZA`; `RECHAZA`; `SE_ABSTIENE`; una lista de EI más corta; `numbering_f36_m01 = NO_CONFIRMADA` | La deliberación, el voto y la elección de EI | POR DESIGNAR | PENDIENTE |
| FG-10 | Depende de FG-03; nadie ha declarado las dependencias | Registro `new_dependencies` con 3 votos y, si hay dependencias, revisión OSV real | Los tres integrantes; un integrante revisor por dependencia | Fecha de la consulta OSV y SHA-256 de artefactos reales, comprobables por un tercero | Una dependencia RECHAZADA o PROPUESTA; no autorizar las EI que la necesitan | La revisión de la cadena de suministro y el voto | POR DESIGNAR | PENDIENTE |
| FG-12 | Depende de FG-03; no hay ADR sucesor ni decisión sobre EI-09 | NO APLICA (sin archivo ni votos propios, solo si no hay EI CONDITIONAL), o registro 3/3 con `ei09_decision` y, si hay alcance C, el ADR dentro de H | Los tres integrantes, si está en CUMPLE | ADR versionado dentro de H; votos individuales | ADR RECHAZADO; `NO_CABE_EN_ALCANCE_B`; `SIN_DECISION` (que impide autorizar EI-09) | Redactar y aprobar el ADR; decidir sobre EI-09 | POR DESIGNAR | PENDIENTE |
| Incremento sucesor (B-01) | El validador vigente exige NO SUPERADO; D-02 no está emitida | Autorización D-02 y, después, la implementación según la [especificación](F36SBX_Especificacion_Sucesor_B01.md), con su auditoría dentro de la de H | El equipo autoriza; una sesión implementadora desarrolla; un auditor independiente revisa | Autorización auténtica del equipo; auditoría de H | No autorizarlo: el gate sigue NO SUPERADO | La autorización | POR DESIGNAR | NO EMITIDA |

## 5. Lo que impide iniciar F37-SBX

F37-SBX = BLOQUEADA mientras se cumpla **cualquiera** de estas condiciones:

1. Cualquiera de FG-02, FG-03, FG-10 o FG-12 no está en CUMPLE (o FG-12 en NO APLICA cuando se admite).
2. `candidate_commit` es nulo, o hay cambios fuera de las rutas de registro entre él y el árbol validado.
3. `f37_authorized_ei` es nulo o difiere de `authorized_ei` de FG-03.
4. El validador vigente exige NO SUPERADO (B-01) y no se ha integrado el incremento sucesor auditado.
5. Hay un evento de revocación (FG-14), o la regla GATE falla por cualquier otro motivo.
6. Para F37-SBX-B, además: F37-SBX-A no está cerrada, o no hay un ADR sucesor APROBADO dentro del candidato.

Ninguna de estas condiciones se resuelve con la evidencia técnica sola. Aunque se resolvieran todas, seguirían sin autorizarse la producción, los datos reales, la G0 real, el alcance C del producto, el scoring y la selección automática (FG-13).

## 6. Qué puede hacer cada actor

El proceso del gate combina tres tipos de acto que no se sustituyen entre sí:

| Acto | Quién puede realizarlo | Ejemplos |
|---|---|---|
| Informe técnico de auditoría | Un auditor elegible: una persona (`docente`, `integrante_no_autor` o `revisor_academico_externo`) o una sesión automatizada de tipo `sesion_de_auditoria_independiente`, distinta de la sesión que implementó o preparó lo auditado | El informe canónico de FG-02 sobre H, con su veredicto y sus recuentos |
| Verificación humana | Las personas del equipo | Comprobar la procedencia, el alcance y la independencia del informe y de la sesión; verificar identidades; revisar la cadena de suministro de una dependencia; registrar los criterios |
| Decisiones, votos y firmas | Solo las personas autorizadas: los tres integrantes, según el criterio | Las decisiones de FG-03, FG-10 y FG-12 en CUMPLE, y las autorizaciones D-01 a D-08 y T-01 a T-07 |

**Una sesión automatizada puede emitir un informe técnico de auditoría** si es independiente de lo auditado: el esquema contempla ese tipo de auditor. Su elegibilidad no se presume por el nombre de la herramienta ni por declarar `independent_of_candidate = true`. La comprueban personas.

**Una sesión automatizada no puede:**

- auditar su propio trabajo;
- votar, firmar ni decidir en nombre de los integrantes;
- registrar como auténtico un acto humano que no ha ocurrido;
- presentarse como integrante, docente o revisor externo humano.

La sesión que prepara este paquete puede preparar formatos, comprobar coherencia y ejecutar el validador.

También son actos humanos, que nadie puede automatizar:

- la elección de EI;
- la redacción y aprobación de un ADR sucesor;
- cualquier autorización institucional externa (G0-02, G0-03 y G0-12), que el gate no toca.

## 7. Decisiones que requieren intervención humana

| ID | Decisión | Opciones | Consecuencias y análisis | Estado |
|---|---|---|---|---|
| D-01 | Qué commit será el candidato del gate | (a) `4a2b2d7`; (b) un candidato final nuevo H, posterior a esta preparación y al sucesor | (a) impide incorporar esta preparación o el sucesor sin perder el candidato (B-02). (b) exige la secuencia de la sección 2.1 y una auditoría nueva de H. **El solicitante dio el 27/10/2026 la instrucción operativa de seguir la opción (b). No es una decisión formal del equipo** | Instrucción operativa (b); decisión formal NO EMITIDA |
| D-02 | Autorizar el incremento sucesor B-01 y su alcance antes de editar código | Autorizarlo con las opciones T-01 a T-07; o no hacerlo | Sin D-02 no se edita el validador ni el gobierno normativo. El contrato no fija un quórum; la práctica del proyecto exige una autorización explícita del equipo para un sucesor de gobierno. [Borrador](BORRADOR_Autorizacion_D02.md) | NO EMITIDA |
| D-03 | Dónde registrar la deuda AF6-L01 y AF6-L02 | (a) Mantenerla en el paquete ([deuda AF6](../F36SBX_Deuda_Tecnica_AF6.md)); (b) replicarla en `docs/academico/TECHNICAL_DEBT.md`; (c) un registro de deuda propio de F36-SBX dentro del paquete | `TECHNICAL_DEBT.md` no solo queda fuera del alcance de FRZ: el validador lo declara antecedente congelado (`F35_FROZEN`). Replicarla ahí rompe FRZ en esta rama y en `develop` y `main`, y quitarlo de `F35_FROZEN` debilitaría una congelación de F35. **Recomendación técnica:** (a) mientras F36-SBX esté abierta, y replicarla en el registro general en un incremento autorizado posterior al cierre de F36-SBX, cuando su validador quede anclado en su rama | NO EMITIDA |
| D-04 | Uso del informe AF6 para FG-02 | (a) Pedir al auditor un informe con el formato del gate; (b) encargar una auditoría nueva; (c) no usarlo | Con D-01 (b), el informe AF6 no sirve para H: FG-02 exige una auditoría de H (sección 2.1). Queda como antecedente técnico | NO EMITIDA |
| D-05 | Qué hacer con AF6-L01 y AF6-L02 | (a) Corregirlos en el incremento de H, antes de fijarlo; (b) registrar FG-02 con los dos LOW en `findings_open.low` | **Recomendación técnica: (a).** El sucesor convierte al validador en una pieza capaz de dar por superado un gate que habilita autorizaciones reales; su guardia de identidad debe estar en su mejor estado. Como H exige una auditoría nueva de todos modos, corregirlos antes no añade ninguna auditoría. Exige RED, GREEN y la autorización del equipo, como toda deuda; la verificación humana de identidades sigue siendo obligatoria. Hasta que se implementen y prueben, **siguen abiertos** | NO EMITIDA |
| D-06 | Alcance de F37-SBX | Lista cerrada de EI, inclusión de EI-09 (F36-M02), numeración (F36-M01), dependencias y si F37-SBX-B entra ahora | Determina FG-03, FG-10 y FG-12. **Orden:** si se autorizará alguna EI CONDITIONAL de alcance C, su ADR sucesor tiene que aprobarse e incorporarse **antes de fijar H**. La lista concreta de EI ALLOWED, EI-09, la numeración y las dependencias se votan en FG-03, FG-10 y FG-12, después de auditar H. Nadie elige EI en nombre del equipo | NO EMITIDA |
| D-07 | Sincronizar `CLAUDE.md`, `docs/PROGRESS.md`, `README.md` y `ACADEMIC_BASELINE.md` | Actualizar el estado vigente antes de fijar H; o dejarlo para después | `CLAUDE.md` aún describe F36-SBX como «candidata a auditoría independiente, sin push, merge, tag ni release», aunque AF5 ya está integrada. Los cuatro documentos repiten el resultado del gate y el estado de F37-SBX en un párrafo de su bloque de estado vigente, además de en las viñetas, y el sucesor necesita una sola afirmación por sujeto (especificación, §5.2). Como son normativos y están protegidos por la regla GOV, la sincronización debe entrar en H, distinguiendo el estado vigente de las fotografías históricas, y necesita autorización | NO EMITIDA |
| D-08 | Integración de la preparación AF6 | Integrarla como parte de H, tras auditar H; o integrarla antes, con su propia autorización | La instrucción operativa es no integrar todavía. Integrarla exige una autorización explícita del equipo (`CLAUDE.md`, contrato 10) | NO EMITIDA |

Las decisiones de diseño del sucesor, T-01 a T-07, están en la [especificación](F36SBX_Especificacion_Sucesor_B01.md#9-decisiones-de-diseño-pendientes-del-equipo).

## 8. Borradores y documentos de preparación

Ninguno es evidencia, ninguno está firmado y ninguno está en `gate/evidencia/`:

- [Acta de revisión técnica y registro de decisiones](BORRADOR_Acta_Revision_y_Decisiones.md): acta, matriz de EI propuesta y registro de decisiones y abstenciones.
- [Lista de comprobación de evidencias y procedimiento de verificación](BORRADOR_Checklist_Evidencias_y_Verificacion.md): lista por criterio, procedimiento de verificación de identidad, votos y procedencia, y condiciones de bloqueo.
- [Autorización D-02](BORRADOR_Autorizacion_D02.md): qué autorizaría el equipo, qué no y en qué condiciones.
- [Especificación del sucesor B-01](F36SBX_Especificacion_Sucesor_B01.md) y su [plan de pruebas](F36SBX_Plan_Pruebas_Sucesor_B01.md): diseño sin implementar.

## 9. Validación de las ramas de preparación

El validador solo admite las ramas `feature/f36-sbx-authorization-design`, `develop` y `main`. En `docs/f36-sbx-gate-preparacion-af6` y en `feature/f36-sbx-gate-transition-h` da **57/2**: FRZ falla por la rama, y GATE falla porque FG-01 y FG-05 se recalculan en NO CUMPLE. Es el anclaje por diseño, no un defecto del contenido:

- la base `55f758e`, sin ningún cambio, da el mismo 57/2 con el nombre de una rama no admitida;
- el contenido de cada rama, validado en un clon desechable con la rama local llamada `develop`, da 59/0, y la batería en memoria, 545/0.

Los documentos nuevos (este, sus borradores y los registros AF6) no están en `PKG_DOCS`, así que las reglas SEM y LNK del validador no los leen. Se comprobaron aparte con las mismas funciones del validador (afirmaciones prohibidas, estados admitidos, enlaces y anclas, caracteres invisibles y NFC). Incluirlos en `PKG_DOCS` cambiaría el código del validador y forma parte del sucesor.

## 10. Auditoría documental de esta preparación

Codex auditó la preparación sobre `88fd3d2ee8b863bd8487001a45f50177c073e15a` el 27/10/2026 («PREPARACIÓN DOCUMENTAL AF6 APROBADA PARA INTEGRACIÓN»). Su condición: no integrarla mientras se conserve `4a2b2d7` como candidato de FG-02. Sus hallazgos y su tratamiento en este documento:

| ID | Severidad | Hallazgo | Tratamiento |
|---|---|---|---|
| DOC-AF6-L01 | LOW | Faltaba explicitar que, después del sucesor, hay que fijar y auditar un candidato nuevo H | Sección 2.1, B-02 y D-01 |
| DOC-AF6-L02 | LOW | Redacción demasiado absoluta sobre si un agente puede emitir un informe técnico de auditoría | Sección 6 y punto 4 de FG-02 |
| DOC-AF6-I01 | INFO | Los votos de FG-12 solo se exigen con FG-12 en CUMPLE | Sección 3.4, matriz de seguimiento y lista de comprobación |

El informe se conserva fuera del repositorio, en el directorio de la sesión de auditoría (`AF6-Documental-Audit/`). Sus SHA-256:

- `Informe_Preparacion_Documental_AF6.md`: `d13e78673c0e195b6edbdebdbffc39512dc9b148db9164b7d2ad0489f28b8f2c`;
- `findings.json`: `a208833c0c6f865b27af713979924a40d40757161976c1bd0a86f2c4de41377d`;
- `SHA256SUMS.txt`: `d98429e40e1f11fa42bf4b171cea094114b572f2b23bab497f0e6cfaebd4f130`.

Esa auditoría no es evidencia de FG-02 ni de ningún criterio, y no examinó H.
