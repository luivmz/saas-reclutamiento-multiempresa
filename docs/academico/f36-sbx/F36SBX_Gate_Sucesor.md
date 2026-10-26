# F36-SBX — Gate sucesor (F36-SBX-GATE) y plan de entrada a F37-SBX

> Fase F36-SBX, versión 2 (26/10/2026). Corrige AF1-M01 de la primera auditoría ([corrección AF1](F36SBX_Correccion_AF1.md)). Candidata a una segunda auditoría independiente. **Resultado vigente: F36-SBX-GATE = NO SUPERADO. F37-SBX = BLOQUEADA.**

## 1. Nombre y propósito

**F36-SBX-GATE** decide una sola cosa: si **F37-SBX** puede comenzar. Lleva el nombre de la fase que lo define, como G0-SBX nació en F34E. Así no se confunde con la G0 real ni con un «G1» de producto.

| Propiedad | Cómo se garantiza |
|---|---|
| Sintético únicamente | FG-07: el contrato de evidencia solo admite `source_type = synthetic` |
| Verificable | Los criterios automáticos los recalcula [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py), que no se fía del valor declarado. La evidencia de equipo se valida por su contenido (sección 8), no por su existencia |
| Reproducible | Biblioteca estándar, sin red, sin reloj en la decisión y con entradas versionadas en Git. El vínculo con el candidato se deriva de Git (sección 9) |
| Fail-closed | Un estado desconocido, una evidencia ausente, vacía, de otro commit o mal formada, o un JSON inválido producen NO SUPERADO |
| Revocable | FG-14 y la sección 5 |
| Independiente de la G0 real | Ningún criterio depende de G0-02, G0-03 o G0-12, y ninguno los da por resueltos |
| No autoriza producción, datos reales ni selección automática | FG-13: `authorizes` es exactamente `["F37-SBX"]`, y la lista `cannot_authorize` es cerrada y obligatoria |

## 2. Estados

| Estado | Significado |
|---|---|
| **NO SUPERADO** | Algún criterio no está en CUMPLE (o en NO APLICA, cuando se admite). F37-SBX bloqueada |
| **SUPERADO** | Todos los criterios están en CUMPLE, o FG-12 en NO APLICA cuando se admite. F37-SBX puede comenzar, solo con las EI autorizadas en FG-03 |
| **REVOCADO** | Hay un evento de revocación registrado. F37-SBX bloqueada o detenida |

Ningún validador «aprueba» por sí solo. SUPERADO exige FG-02 y FG-03, que son actos humanos registrados. El validador comprueba que su evidencia existe, que es del candidato correcto y que dice lo que el criterio exige.

## 3. Criterios

| ID | Criterio | Tipo | Evidencia exigida | Estado vigente |
|---|---|---|---|---|
| FG-01 | El paquete F36-SBX está íntegro: pasan todas las reglas de contenido de `validate_f36sbx.py` (STR, LNK, GOV, SEM, CAP, CTR, THR, EVA, FRZ, DEP y PII) | AUTO | Ejecución del validador | CUMPLE |
| FG-02 | Auditoría independiente del paquete F36-SBX con 0 BLOCKER, 0 HIGH y 0 MEDIUM que requiera corrección abiertos | EQUIPO | `gate/evidencia/FG-02.json` con el formato 8.2 y el informe de auditoría que cita | PENDIENTE |
| FG-03 | Autorización explícita de F37-SBX por el equipo: registro fechado, aprobación individual de los tres integrantes, lista cerrada de EI autorizadas y confirmación de la numeración (F36-M01) | EQUIPO | `gate/evidencia/FG-03.json` con el formato 8.3 | PENDIENTE |
| FG-04 | Los estados de gobierno siguen intactos en `CLAUDE.md`, `README.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md` | AUTO | Regla GOV | CUMPLE |
| FG-05 | F35-SBX congelada, el runtime y las dependencias no cambian desde la base | AUTO | Regla FRZ | CUMPLE |
| FG-06 | La matriz de capacidades es coherente con F33, está fijada y bloquea todo lo prohibido | AUTO | Regla CAP | CUMPLE |
| FG-07 | El contrato de evidencia es válido, cerrado y solo sintético, y su ejemplo de conformidad cumple REL-01..REL-12 | AUTO | Regla CTR | CUMPLE |
| FG-08 | Cada amenaza TEI tiene control y comportamiento fail-closed | AUTO | Regla THR | CUMPLE |
| FG-09 | El plan de evaluación cubre cada EI ALLOWED o CONDITIONAL y declara que no hay resultados | AUTO | Regla EVA | CUMPLE |
| FG-10 | Registro de dependencias del candidato, también para declarar que no hay ninguna nueva: versión exacta, propósito, licencia, origen, revisión de la cadena de suministro, EI relacionadas y aprobación | EQUIPO | `gate/evidencia/FG-10.json` con el formato 8.4. Nunca es NO APLICA | PENDIENTE |
| FG-11 | No hay scoring, ranking, recomendación ni selección automática, y RF-23 sigue humana | AUTO | Reglas CAP y SEM | CUMPLE |
| FG-12 | ADR sucesor APROBADO para toda EI CONDITIONAL de alcance C autorizada, y decisión explícita del equipo sobre EI-09 | EQUIPO | `gate/evidencia/FG-12.json` con el formato 8.5. NO APLICA solo si FG-03 no autoriza ninguna EI CONDITIONAL | PENDIENTE |
| FG-13 | El gate solo autoriza F37-SBX y declara todo lo que no puede autorizar | AUTO | Regla GATE | CUMPLE |
| FG-14 | No hay ningún evento de revocación registrado | AUTO | Regla GATE | CUMPLE |

**Resultado vigente: NO SUPERADO,** porque FG-02, FG-03, FG-10 y FG-12 están PENDIENTES y no hay evidencia registrada. Se registra en [`f36sbx_gate_state.json`](gate/f36sbx_gate_state.json), y el validador recalcula el resultado y exige que coincida con el declarado aquí y en el JSON.

## 4. Regla de decisión

```
si revocation != null                                     → REVOCADO
si un estado no es uno de los admitidos para su criterio
   (AUTO: CUMPLE o NO CUMPLE; EQUIPO: CUMPLE, PENDIENTE
   o NO CUMPLE; NO APLICA solo en FG-12)                  → NO SUPERADO  (fail-closed)
si un AUTO declarado difiere del recalculado              → NO SUPERADO  (y la regla GATE falla)
si un EQUIPO en CUMPLE no tiene evidencia válida según
   la sección 8, o la evidencia no es del candidato
   declarado según la sección 9                           → NO SUPERADO  (y la regla GATE falla)
si FG-12 está en NO APLICA y FG-03 no está en CUMPLE, o
   la autorización incluye alguna EI CONDITIONAL          → NO SUPERADO
si la autorización incluye una EI BLOCKED o una EI que
   no está en la matriz                                   → NO SUPERADO
si todos los criterios están en CUMPLE (o FG-12 en
   NO APLICA cuando se admite), con candidato declarado   → SUPERADO
en cualquier otro caso                                    → NO SUPERADO
```

## 5. Revocación

Revoca el gate, aunque ya esté SUPERADO, cualquier hecho de la [sección 7 del charter](F36SBX_Charter.md#7-revocación). También lo revocan un fallo de reproducibilidad en F37-SBX (TEI-21) que no se corrija antes de publicar resultados, y la retirada de la autorización por el equipo. La revocación se registra en `revocation` con fecha, motivo y evidencia, en un incremento nuevo.

## 6. Lo que el gate no puede autorizar

Producción y despliegue, datos reales, PII real, audio o vídeo reales, selección o decisión automática, scoring, ranking o recomendación de personas, cambios en RF-23, RF-21 o RF-29, la G0 real, el alcance C del producto, nuevos endpoints, migraciones o UI, y las EI BLOCKED.

## 7. Plan de entrada a F37-SBX

F37-SBX se divide en dos etapas. La B no puede empezar antes de que la A esté cerrada.

| Etapa | Contenido | Requisitos de entrada | Salida mínima para auditar |
|---|---|---|---|
| **F37-SBX-A** (alcance B) | Generador sintético v1 según el contrato, guardia de entrada, EI-01 a EI-07 y EI-09 si se confirma F36-M02, arnés de evaluación (M-01 a M-08, M-11, M-12 y R-01 a R-05) | F36-SBX-GATE SUPERADO. Las EI pedidas están en la autorización de FG-03. Sin dependencias nuevas | Preregistro, `test` sellado, RED y GREEN, resultados reproducibles con manifiesto y un gate sucesor propio |
| **F37-SBX-B** (subconjunto de C, solo sintético) | EI-08, EI-10, EI-11, EI-12 y EI-24 | F37-SBX-A cerrada. ADR sucesor APROBADO (FG-12). Dependencias registradas y aprobadas (FG-10) | Lo mismo que A, más la auditoría contrafactual y la comparación con BM25 |

**Primer paso concreto, cuando el equipo lo decida:** auditar este paquete (FG-02) y, si la auditoría pasa, registrar la autorización de FG-03 con la lista de EI de F37-SBX-A. Nada de F37-SBX se implementa antes.

**Salida de F37-SBX.** Nada migra a producción. Siguen rigiendo SAL-01 a SAL-05 de [F34E](../g0-sandbox/F34E_Autorizacion_F35_SBX.md#3-criterios-de-salida-de-sbx-a-trabajo-real) y la regla de datos de ADR-005 §6.10.

## 8. Formato de la evidencia de equipo

### 8.1 Reglas comunes

El esquema cerrado es [`f36sbx_team_evidence_schema.json`](gate/f36sbx_team_evidence_schema.json) (`f36sbx-team-evidence/v1`), fijado por su SHA-256 canónico. Cada criterio tiene un único archivo JSON en una ruta fija: `gate/evidencia/FG-02.json`, `FG-03.json`, `FG-10.json` y `FG-12.json`. El estado del gate lo cita solo cuando el criterio está en CUMPLE.

| Campo común | Regla |
|---|---|
| `schema` | Exactamente `f36sbx-team-evidence/v1` |
| `criterion_id` | El criterio del archivo |
| `gate_id`, `gate_version` | `F36-SBX-GATE` y `2`; otro gate u otra versión es evidencia de otro contexto |
| `candidate_commit` | El commit auditado, igual al `candidate_commit` del estado del gate (sección 9) |
| `record_id` | `F36SBX-<criterio>-NNN` |
| `recorded_at` | Fecha `AAAA-MM-DD` válida, no anterior a la del commit candidato |

Son JSON estrictos: sin claves duplicadas y con exactamente los campos del esquema. Un archivo vacío, un texto genérico o un campo adicional invalidan la evidencia. En `gate/evidencia/` no puede haber archivos sin citar ni enlaces simbólicos.

**Aprobaciones (FG-03, FG-10 y FG-12).** `approvals` es una lista de exactamente tres objetos `{member, vote, date}`, uno por integrante: `Coronacion Meza Fredy`, `Peña Arroyo Anthony` y `Vila Meza Luis Antonio`. La identidad se compara exacta, sin coincidencias aproximadas, y debe coincidir con los integrantes que declara `CLAUDE.md`. Cada voto tiene que ser `APRUEBA` y `quorum` debe valer `3/3`. Una persona duplicada, dos de tres, un voto `RECHAZA` o `SE_ABSTIENE` o una fecha fuera del registro invalidan la evidencia.

### 8.2 FG-02 — auditoría independiente

| Campo | Regla |
|---|---|
| `auditor` | `{name, kind, independent_of_candidate}`: un nombre inequívoco (no vale «auditor», «N/A» ni similares), un tipo cerrado (`docente`, `integrante_no_autor`, `sesion_de_auditoria_independiente` o `revisor_academico_externo`) y `independent_of_candidate = true` |
| `audit_report` | `{path, sha256}`: un `.md` dentro de `gate/evidencia/`, con ese SHA-256 y el commit candidato completo en su texto |
| `verdict` | `APROBADO_PARA_INTEGRACION` o `APROBADO_CON_OBSERVACIONES`. `NO_APROBADO_PARA_INTEGRACION` no cumple |
| `findings_open` | Enteros no negativos `blocker`, `high`, `medium_requiring_fix`, `medium_accepted` y `low`; los tres primeros deben ser 0 |

### 8.3 FG-03 — autorización explícita

| Campo | Regla |
|---|---|
| `decision` | `AUTORIZA_INICIO_F37_SBX`; `NO_AUTORIZA` no cumple |
| `authorized_ei` | Lista no vacía, sin repetidos, de EI de la matriz en ALLOWED o CONDITIONAL. Debe ser igual a `f37_authorized_ei` del estado del gate. Una EI BLOCKED, una desconocida o una autorización genérica sin lista no cumplen |
| `numbering_f36_m01` | `CONFIRMADA` |
| `approvals`, `quorum` | 3/3 (sección 8.1) |

### 8.4 FG-10 — dependencias

| Campo | Regla |
|---|---|
| `new_dependencies` | Booleano. Con `false`, `dependencies` es `[]` y no se puede haber autorizado EI-10, EI-11 ni EI-12, que son las únicas que justifican dependencias nuevas |
| `dependencies` | Cada dependencia tiene exactamente `name`, `version` (fijada con `==`), `purpose`, `license` (Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, MIT, MPL-2.0 o PSF-2.0), `source = pypi`, `source_url` canónica, `supply_chain_review` (fecha de consulta OSV, 0 vulnerabilidades abiertas, SHA-256 del artefacto y un integrante como revisor), `related_ei` (EI autorizadas en FG-03 de entre EI-10, EI-11 y EI-12) y `approval_status = APROBADA` |
| `approvals`, `quorum` | 3/3 |

FG-10 exige una FG-03 válida. Cada EI autorizada que necesite dependencias debe quedar cubierta por al menos una dependencia aprobada. F36-SBX no propone ninguna dependencia concreta.

### 8.5 FG-12 — ADR sucesor y EI-09

| Campo | Regla |
|---|---|
| `successor_adr` | `null` si FG-03 no autoriza ninguna EI CONDITIONAL de alcance C. Si no, `{id, path, sha256, status, relation_to_adr005, scope}`: un id entre ADR-006 y ADR-099, un `.md` bajo `docs/` con ese SHA-256 que nombra su id, F36-SBX y ADR-005, `status = APROBADO` (un ADR `PROPUESTO` no basta), `relation_to_adr005 = EXCEPCION_SANDBOX_SINTETICA_ADR005_6_4` y `scope = ALCANCE_C_SOLO_SINTETICO` |
| `covered_ei` | EI CONDITIONAL de alcance C (EI-08, EI-10, EI-11, EI-12 y EI-24) que el ADR cubre; deben incluir todas las autorizadas. Una EI BLOCKED, ALLOWED o desconocida no cumple |
| `ei09_decision` | `CABE_EN_ALCANCE_B`, `NO_CABE_EN_ALCANCE_B` o `SIN_DECISION`. Si FG-03 autoriza EI-09, debe ser `CABE_EN_ALCANCE_B` |
| `approvals`, `quorum` | 3/3 |

FG-12 exige una FG-03 válida. F36-SBX no aprueba ningún ADR sucesor ni decide sobre EI-09 (F36-M02 y F36-M03 siguen abiertos).

## 9. Vínculo con el candidato auditado

`candidate_commit` del estado del gate es `null` mientras no haya evidencia. Cuando el equipo registre evidencia, valdrá el commit que se auditó, y todas las evidencias deben citar ese mismo commit. El validador lo deriva de Git, de forma reproducible:

1. Es un commit del repositorio, con 40 caracteres hexadecimales.
2. Desciende de la base `b8892af` y es ancestro del HEAD que se valida (o es el propio HEAD).
3. Entre ese commit y el árbol de trabajo solo cambian las rutas de registro: `gate/evidencia/`, `gate/f36sbx_gate_state.json` y, en este documento, únicamente la columna Estado de la tabla FG.

Así, una auditoría de otro commit no sirve. Tampoco sirve la de un commit anterior si después cambió cualquier otra parte del paquete: lo auditado tiene que ser exactamente lo que se registra. Esta versión del validador exige además que el gobierno siga declarando NO SUPERADO. Declarar el gate SUPERADO necesita un incremento sucesor auditado que actualice el gobierno y el validador. Mientras tanto, la función de decisión se prueba con controles positivos en memoria, que nunca se escriben en el repositorio.
