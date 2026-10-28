# F36-SBX — Matriz de preparación del gate (FG-02, FG-03, FG-10 y FG-12)

> Documento de trabajo del 27/10/2026, en la rama `docs/f36-sbx-gate-preparacion-af6`, desde `main` = `55f758e013e1852de8c8daa5d6fde95e39b02b0d`. **No registra evidencia, no cambia ningún estado y no autoriza nada.** Analiza qué exige el contrato vigente para cada criterio EQUIPO pendiente y qué acción humana falta. Fuentes normativas: [gate sucesor](../F36SBX_Gate_Sucesor.md), [estado del gate](../gate/f36sbx_gate_state.json), [esquema de la evidencia de equipo](../gate/f36sbx_team_evidence_schema.json) (`f36sbx-team-evidence/v2`) y [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py). Si este documento difiere de esas fuentes, mandan ellas.

**Estado vigente, sin cambios:** F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; FG-02, FG-03, FG-10 y FG-12 en PENDIENTE, con `evidence = null`; `candidate_commit = null`; `f37_authorized_ei = null`; F37-SBX = BLOQUEADA.

## 1. Categorías de evidencia que no son equivalentes

| Categoría | Qué es | Ejemplos en F36-SBX | Qué puede satisfacer |
|---|---|---|---|
| Evidencia técnica | Resultado reproducible de herramientas y auditorías | El validador (59/0), las baterías, la [sexta auditoría](../F36SBX_Auditoria_AF6.md) y las CI | Los criterios AUTO (FG-01, FG-04..FG-09, FG-11, FG-13 y FG-14). Para FG-02 es la **materia** del informe, no el registro |
| Evidencia académica sintética | Datos y autorizaciones fabricados a propósito para probar el oracle | Fixtures en memoria y en clones desechables de las baterías y de la auditoría | Nada. Nunca se escribe en `gate/evidencia/` |
| Aprobación humana del equipo | Acto fechado de los tres integrantes, con su voto individual | Los registros de FG-03, FG-10 y FG-12, con `approvals` 3/3 | FG-03, FG-10 y FG-12, solo con el formato del gate |
| Autorización institucional externa | Decisión de un tercero con autoridad (jurídica, de privacidad, institucional) | G0-02, G0-03 y G0-12 (PENDIENTE EXTERNO) | Ningún criterio del F36-SBX-GATE: el gate es independiente de la G0 real y no la da por resuelta |
| Autorización para ejecutar capacidades experimentales | Decisión del equipo sobre qué EI puede construir F37-SBX | `authorized_ei` de FG-03, el ADR sucesor de FG-12 y las dependencias de FG-10 | El inicio de F37-SBX con esas EI y nada más. No autoriza producción, datos reales ni alcance C del producto |

## 2. Bloqueos estructurales previos a cualquier registro

Antes de analizar cada criterio, tres hechos del contrato vigente condicionan el plan.

**B-01. Esta versión del validador exige que el gobierno declare NO SUPERADO.** La regla GATE comprueba que el resultado sea NO SUPERADO y que lo declaren el gate, su JSON y el gobierno. El [gate §9](../F36SBX_Gate_Sucesor.md#9-vínculo-con-el-candidato-auditado) lo dice expresamente: «declarar el gate SUPERADO necesita un incremento sucesor auditado que actualice el gobierno y el validador». Así que, aunque los cuatro criterios tuvieran evidencia auténtica, F36-SBX-GATE no podría pasar a SUPERADO sin ese incremento sucesor (decisión D-02).

**B-02. El candidato del gate solo admite cambios en las rutas de registro.** Entre `candidate_commit` y el árbol que se valida solo pueden cambiar `gate/evidencia/`, `gate/f36sbx_gate_state.json` y la columna Estado de la tabla FG del gate (gate §9). Hoy el árbol de `main` (`55f758e`) es **idéntico** al del candidato auditado `4a2b2d7` (`01dc59a…`).

- Si el equipo quiere registrar la evidencia contra `4a2b2d7`, tiene que hacerlo **antes** de integrar cualquier otro cambio en esa rama.
- Este incremento cambia el paquete. Integrarlo antes invalidaría `4a2b2d7` como candidato y exigiría auditar un candidato nuevo para FG-02 (decisión D-01).

**B-03. El formato de FG-02 exige un informe dentro de `gate/evidencia/`.** El informe AF6 no tiene las secciones ni el bloque canónico del gate §8.6, y no está en el repositorio. Si el equipo lo redactara de nuevo con ese formato en nombre del auditor, sería un documento del equipo y no del auditor: un riesgo de evidencia no auténtica (decisión D-04).

## 3. Análisis por criterio

### 3.1 FG-02 — auditoría independiente

| Punto | Análisis |
|---|---|
| 1. Definición contractual | «Auditoría independiente del paquete F36-SBX con 0 BLOCKER, 0 HIGH y 0 MEDIUM que requiera corrección abiertos» (gate §3). Tipo EQUIPO |
| 2. Estado actual | PENDIENTE, `evidence = null`. Hay una auditoría técnica favorable (AF6) sobre `4a2b2d7`, sin registrar |
| 3. Evidencia auténtica requerida | `gate/evidencia/FG-02.json` con `auditor {name, kind, independent_of_candidate}`, `audit_report {path, sha256}`, `verdict` y `findings_open {blocker, high, medium_requiring_fix, medium_accepted, low}` (gate §8.2), más el informe `.md` citado |
| 4. Autoridad | El auditor emite el informe y su veredicto. El equipo registra el criterio. Tipos de auditor admitidos: `docente`, `integrante_no_autor`, `sesion_de_auditoria_independiente` y `revisor_academico_externo`, con `independent_of_candidate = true` |
| 5. Formato y ubicación | JSON estricto con exactamente los campos del esquema. El informe es un `.md` dentro de `gate/evidencia/`, en UTF-8 NFC, con un título de nivel 1, las secciones «Alcance», «Hallazgos» y «Conclusión», al menos 200 letras fuera del bloque y un único bloque `f36sbx-audit-metadata` (`f36sbx-audit-report/v1`) coherente con el registro |
| 6. Commit, hashes y procedencia | `candidate_commit` del registro y del bloque igual al del estado del gate. SHA-256 del informe entero. `recorded_at` no anterior a la fecha del candidato. `report_date` entre esa fecha y `recorded_at`. El informe no puede cambiar después del registro |
| 7. Dependencias | Ninguna contractual con otros FG. Depende de la decisión D-01 (qué commit es el candidato) |
| 8. Riesgos de aceptación inválida | (a) Tratar el informe AF6 como registro por su mera existencia. (b) Un informe redactado por el equipo en nombre del auditor. (c) Un auditor que no es independiente: los 32 commits de F36-SBX tienen como autor Git a «Luis Vila Meza», que no puede figurar como `integrante_no_autor`. (d) Registrar contra `4a2b2d7` después de integrar otros cambios: el vínculo falla. (e) La identidad del auditor: la guardia estructural tiene los residuos AF6-L01 y AF6-L02, así que la identidad la verifica una persona |
| 9. Acción humana pendiente | Decidir D-01 y D-04. Obtener del auditor un informe con el formato del gate, o una auditoría nueva. Elegir el `verdict` que corresponde al dictamen (el auditor, no el equipo, decide si es `APROBADO_PARA_INTEGRACION` o `APROBADO_CON_OBSERVACIONES`). Registrar `findings_open` con los dos LOW abiertos. Verificar la identidad del auditor |
| 10. Condición objetiva | El validador, con el registro y el informe en `gate/evidencia/` y FG-02 en CUMPLE, no da ningún error para FG-02 (regla GATE), y una persona del equipo ha verificado la identidad del auditor y la autoría del informe |

### 3.2 FG-03 — autorización explícita de F37-SBX

| Punto | Análisis |
|---|---|
| 1. Definición contractual | «Autorización explícita de F37-SBX por el equipo: registro fechado, aprobación individual de los tres integrantes, lista cerrada de EI autorizadas y confirmación de la numeración (F36-M01)» |
| 2. Estado actual | PENDIENTE. `f37_authorized_ei = null`. F36-M01 sin confirmar |
| 3. Evidencia auténtica requerida | `gate/evidencia/FG-03.json` con `decision`, `authorized_ei`, `numbering_f36_m01`, `approvals` y `quorum` (gate §8.3) |
| 4. Autoridad | Los tres integrantes declarados en `CLAUDE.md` y en el esquema: `Coronacion Meza Fredy`, `Peña Arroyo Anthony` y `Vila Meza Luis Antonio`. Ningún otro rol puede sustituirlos |
| 5. Formato y ubicación | JSON estricto en `gate/evidencia/FG-03.json`. `authorized_ei`, la lista no vacía y sin repetidos de EI ALLOWED o CONDITIONAL de la matriz, tiene que ser **igual** a `f37_authorized_ei` del estado del gate |
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
| 4. Autoridad | Los tres integrantes, 3/3. El revisor de la cadena de suministro de cada dependencia tiene que ser un integrante |
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
| 3. Evidencia auténtica requerida | `gate/evidencia/FG-12.json` con `successor_adr`, `covered_ei`, `ei09_decision`, `approvals` y `quorum` (gate §8.5). Si hay alcance C autorizado, además, el ADR `.md` |
| 4. Autoridad | Los tres integrantes, 3/3, para el registro y para aprobar el ADR. Un ADR sucesor que excepciona ADR-005 §6.4 en el sandbox no sustituye a la G0 real ni a ninguna autorización institucional |
| 5. Formato y ubicación | `successor_adr` es nulo si FG-03 no autoriza ninguna EI CONDITIONAL de alcance C. Si no, es `{id, path, sha256, status, relation_to_adr005, scope}`, con un id entre ADR-006 y ADR-099 y un ADR `.md` bajo `docs/` **que forma parte del commit candidato** y no cambia después. Ese ADR lleva el bloque `f36sbx-adr-metadata`, el estado APROBADO, la relación `EXCEPCION_SANDBOX_SINTETICA_ADR005_6_4` y el alcance `ALCANCE_C_SOLO_SINTETICO` |
| 6. Commit, hashes y procedencia | El ADR se lee del blob `candidate_commit:path` (AF3-M01, sin `refs/replace`). Su SHA-256 se calcula sobre esos bytes. Su `decided_on` no es posterior al commit candidato |
| 7. Dependencias | Exige una FG-03 válida. **El ADR tiene que estar dentro del candidato**: si F37-SBX-B se autoriza, el ADR se escribe y se aprueba **antes** de fijar el candidato. Eso afecta a D-01 |
| 8. Riesgos de aceptación inválida | Un ADR PROPUESTO tratado como aprobado. Un ADR añadido después del candidato. Poner FG-12 en NO APLICA y autorizar EI-09 u otra EI CONDITIONAL. Confundir una excepción del sandbox con el alcance C del producto, que sigue BLOQUEADO |
| 9. Acción humana pendiente | Decidir F36-M02: si EI-09 cabe en el alcance B. Decidir si F37-SBX-B entra en esta autorización: el plan la deja para después de cerrar F37-SBX-A. Si entra, redactar y votar el ADR sucesor antes del candidato. Si FG-03 solo autoriza EI ALLOWED, FG-12 puede quedar en NO APLICA |
| 10. Condición objetiva | Una de dos: (a) FG-12 en NO APLICA, con FG-03 en CUMPLE y sin ninguna EI CONDITIONAL autorizada; o (b) un registro sin errores del validador, con el ADR APROBADO en el candidato si hay alcance C, y con `ei09_decision = CABE_EN_ALCANCE_B` si se autoriza EI-09 |

## 4. Matriz de seguimiento

| Criterio | Pendiente porque | Evidencia que falta | Interviene | Verificación de autenticidad | Decisiones negativas o restrictivas posibles | No automatizable | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
| FG-02 | Nadie ha registrado una auditoría con el formato del gate; el candidato del gate no está fijado | Informe del auditor con el formato 8.6 en `gate/evidencia/` y su registro | Auditor independiente; el equipo registra | Autoría del informe confirmada por el auditor; SHA-256 del informe; identidad del auditor revisada por una persona | `NO_APROBADO_PARA_INTEGRACION`; hallazgos que exijan corrección; decidir que el auditor no es independiente | La auditoría, el veredicto y la verificación de la identidad | POR DESIGNAR | PENDIENTE |
| FG-03 | No hay decisión del equipo ni lista de EI | Registro con decisión, lista cerrada, numeración y 3 votos | Los tres integrantes | Voto individual de cada persona por el canal acordado; acta firmada fuera del repositorio | `NO_AUTORIZA`; `RECHAZA`; `SE_ABSTIENE`; una lista de EI más corta; `numbering_f36_m01 = NO_CONFIRMADA` | La deliberación, el voto y la elección de EI | POR DESIGNAR | PENDIENTE |
| FG-10 | Depende de FG-03; nadie ha declarado las dependencias | Registro `new_dependencies` con 3 votos y, si hay dependencias, revisión OSV real | Los tres integrantes; un integrante revisor por dependencia | Fecha de la consulta OSV y SHA-256 de artefactos reales, comprobables por un tercero | Una dependencia RECHAZADA o PROPUESTA; no autorizar las EI que la necesitan | La revisión de la cadena de suministro y el voto | POR DESIGNAR | PENDIENTE |
| FG-12 | Depende de FG-03; no hay ADR sucesor ni decisión sobre EI-09 | NO APLICA justificado, o registro con ADR (si hay alcance C) y `ei09_decision` | Los tres integrantes | ADR versionado dentro del candidato; votos individuales | ADR RECHAZADO; `NO_CABE_EN_ALCANCE_B`; `SIN_DECISION` (que impide autorizar EI-09) | Redactar y aprobar el ADR; decidir sobre EI-09 | POR DESIGNAR | PENDIENTE |
| Incremento sucesor (B-01) | El validador vigente exige NO SUPERADO | Un incremento auditado que actualice el validador y el gobierno | El equipo, con auditoría independiente | Auditoría del incremento | No hacerlo: el gate sigue NO SUPERADO | La decisión y la auditoría | POR DESIGNAR | NO EMITIDA |

## 5. Lo que impide iniciar F37-SBX

F37-SBX = BLOQUEADA mientras se cumpla **cualquiera** de estas condiciones:

1. Cualquiera de FG-02, FG-03, FG-10 o FG-12 no está en CUMPLE (o FG-12 en NO APLICA cuando se admite).
2. `candidate_commit` es nulo, o hay cambios fuera de las rutas de registro entre él y el árbol validado.
3. `f37_authorized_ei` es nulo o difiere de `authorized_ei` de FG-03.
4. El validador vigente exige NO SUPERADO (B-01) y no se ha integrado el incremento sucesor auditado.
5. Hay un evento de revocación (FG-14), o la regla GATE falla por cualquier otro motivo.
6. Para F37-SBX-B, además: F37-SBX-A no está cerrada, o no hay un ADR sucesor APROBADO dentro del candidato.

Ninguna de estas condiciones se resuelve con la evidencia técnica sola. Aunque se resolvieran todas, seguirían sin autorizarse la producción, los datos reales, la G0 real, el alcance C del producto, el scoring y la selección automática (FG-13).

## 6. Acciones que no se pueden automatizar

- La deliberación y el voto de cada integrante, y la elección de EI.
- La auditoría independiente y su veredicto.
- La verificación de que una identidad o un voto corresponden a una persona real: la guardia del validador es estructural (y tiene los residuos [AF6-L01 y AF6-L02](../F36SBX_Deuda_Tecnica_AF6.md)).
- La revisión de la cadena de suministro de una dependencia.
- La redacción y aprobación de un ADR sucesor.
- Cualquier autorización institucional externa (G0-02, G0-03 y G0-12), que el gate no toca.

Un agente puede preparar formatos, comprobar coherencia y ejecutar el validador. No puede emitir, firmar ni completar estos actos.

## 7. Decisiones que requieren intervención humana

| ID | Decisión | Opciones | Consecuencias | Estado |
|---|---|---|---|---|
| D-01 | Qué commit será el candidato del gate | (a) `4a2b2d7`, cuyo árbol es hoy el de `main`; (b) un candidato posterior que incluya esta preparación y, si se decide, la corrección de AF6-L01 y AF6-L02 | (a) exige registrar la evidencia antes de integrar cualquier otro cambio, también este incremento, y obtener un informe de AF6 con el formato del gate. (b) exige una nueva auditoría independiente sobre ese candidato para FG-02 y, si hay alcance C, el ADR dentro de él | NO EMITIDA |
| D-02 | Incremento sucesor que permita declarar SUPERADO | Hacerlo, auditado, cuando la evidencia exista; o no hacerlo | Sin él, el gate no puede pasar a SUPERADO con este validador | NO EMITIDA |
| D-03 | Replicar AF6-L01 y AF6-L02 en `docs/academico/TECHNICAL_DEBT.md` | (a) Ampliar en un incremento auditado el alcance de FRZ; (b) mantenerlos solo en el paquete; (c) replicarlos aceptando un fallo del validador fuera de su rama | (a) cambia el validador. (b) los deja fuera del registro general. (c) hace fallar FRZ en `develop` y `main` | NO EMITIDA |
| D-04 | Uso del informe AF6 para FG-02 | (a) Pedir al auditor un informe con el formato del gate sobre el candidato que se elija; (b) encargar una auditoría nueva; (c) no usarlo | Un informe redactado por el equipo en nombre del auditor no es auténtico. Usarlo exige conservar su evidencia completa (registro AF6 §7) | NO EMITIDA |
| D-05 | Corregir AF6-L01 y AF6-L02 antes de fijar el candidato | Corregir antes; o registrar FG-02 con los dos LOW en `findings_open.low` | Corregir antes implica un candidato nuevo (D-01 b) y otra auditoría | NO EMITIDA |
| D-06 | Alcance de F37-SBX | Lista cerrada de EI, inclusión de EI-09 (F36-M02), numeración (F36-M01) y si F37-SBX-B entra ahora | Determina FG-03, FG-10 y FG-12 | NO EMITIDA |
| D-07 | Sincronizar `CLAUDE.md` y `docs/PROGRESS.md` con la integración de AF5 | Actualizar el estado vigente; o dejarlo hasta el siguiente cierre | `CLAUDE.md` aún describe F36-SBX como «candidata a auditoría independiente, sin push, merge, tag ni release». Cambiarlo toca la regla GOV y exige cuidado con sus líneas de estado | NO EMITIDA |
| D-08 | Integración de este incremento documental | Integrar tras su auditoría; o retenerlo hasta resolver D-01 | Integrarlo cambia el árbol frente a `4a2b2d7` (B-02) | NO EMITIDA |

## 8. Borradores preparados

Ninguno es evidencia, ninguno está firmado y ninguno está en `gate/evidencia/`:

- [Acta de revisión técnica y registro de decisiones](BORRADOR_Acta_Revision_y_Decisiones.md): acta, matriz de EI propuesta y registro de decisiones y abstenciones.
- [Lista de comprobación de evidencias y procedimiento de verificación](BORRADOR_Checklist_Evidencias_y_Verificacion.md): lista por criterio, procedimiento de verificación de identidad, votos y procedencia, y condiciones de bloqueo.

## 9. Validación de esta rama

El validador solo admite las ramas `feature/f36-sbx-authorization-design`, `develop` y `main`. En `docs/f36-sbx-gate-preparacion-af6` da **57/2**: FRZ falla por la rama, y GATE falla porque FG-01 y FG-05 se recalculan en NO CUMPLE. Es el anclaje por diseño, no un defecto del contenido:

- la base `55f758e`, sin ningún cambio, da el mismo 57/2 con el nombre de esta rama;
- el contenido de esta rama, validado en un clon desechable con la rama local llamada `develop`, da 59/0, y la batería en memoria, 545/0.

Los documentos nuevos (este, sus borradores y los registros AF6) no están en `PKG_DOCS`, así que las reglas SEM y LNK del validador no los leen. Se comprobaron aparte con las mismas funciones del validador (afirmaciones prohibidas, estados admitidos, enlaces y anclas, caracteres invisibles y NFC). Incluirlos en `PKG_DOCS` cambiaría el código del validador y queda para un incremento auditado.
