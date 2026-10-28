# F36-SBX — Especificación del sucesor B-01 (transición del F36-SBX-GATE)

> Especificación de diseño del 27/10/2026, en la rama `feature/f36-sbx-gate-transition-h`. **No está implementada:** este incremento no modifica [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py), sus pruebas ni el gobierno. Implementarla requiere la autorización D-02 del equipo, que **no está emitida** ([borrador](BORRADOR_Autorizacion_D02.md)). Mientras tanto, F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA. Las referencias `validate_f36sbx.py:NNNN` son del validador integrado (`4a2b2d7`, SHA-256 del archivo `87ad2f6f…`).

## 1. Propósito y límites

B-01 resuelve un solo problema: con el validador vigente, el gate **no puede** pasar a SUPERADO aunque toda la evidencia sea auténtica y válida ([matriz, B-01](F36SBX_Matriz_Preparacion_Gate.md#2-bloqueos-estructurales-previos-a-cualquier-registro)).

El sucesor debe permitir que el validador reconozca ese resultado **solo** cuando el contrato se cumple, recalculándolo siempre a partir de la evidencia. Debe mantener, además, la coherencia de todas las fuentes que declaran el estado.

B-01 **no**:

- registra evidencia;
- decide EI ni dependencias;
- aprueba ADR;
- implementa ninguna capacidad de F37-SBX;
- cambia el contrato de evidencia (v4) ni el esquema de evidencia de equipo (v2);
- toca la G0 real, ADR-005, los datos reales, el alcance C del producto, RF-23 ni RF-29.

## 2. Comportamiento actual verificado

| Pieza | Comportamiento | Efecto sobre una transición legítima |
|---|---|---|
| `evaluate_gate()` (`:2722`) | Calcula SUPERADO si todos los criterios están en CUMPLE (o FG-12 en NO APLICA cuando se admite), con evidencia válida, candidato y lista de EI | Correcto: es la regla de decisión del gate §4 |
| `rule_gate()` (`:2766`), comprobación final (`:2877`) | Exige que el resultado sea NO SUPERADO | Un resultado SUPERADO legítimo siempre falla |
| `rule_gate()`, frase del resultado (`:2874`–`:2876`) | Exige «F36-SBX-GATE = resultado» en el gate y en el README del paquete | Con SUPERADO, esos dos documentos tendrían que cambiar después del candidato |
| `binding_errors()` (`:2293`) y `doc_status_only()` (`:2275`) | Después del candidato solo admiten `gate/evidencia/`, el JSON del estado y la columna Estado de la tabla FG | Cualquier otro cambio, también el de esa frase o el de un espejo del gobierno, invalida el candidato |
| `REQUIRED_STATE` (`:76`) y `rule_gov()` (`:1257`) | Los cuatro documentos de gobierno tienen exactamente 16 líneas de estado, entre ellas la del gate en NO SUPERADO y la de F37-SBX en BLOQUEADA, y conservan las de la base | El gobierno no puede reflejar un resultado distinto |
| `allowed_states()` (`:1283`) | Solo admite NO SUPERADO para el gate, y solo estados bloqueados para F37-SBX y las fases posteriores | Cualquier afirmación del resultado nuevo falla en SEM |
| `FORBIDDEN_CLAIMS` (`:85`) | Prohíbe cualquier afirmación de habilitación, autorización o inicio de F37-SBX | Igual |
| `BRANCHES` (`:38`) | Solo admite `feature/f36-sbx-authorization-design`, `develop` y `main` | Una rama nueva da 57/2 por diseño |

**Quitar solo la comprobación de `:2877` no basta ni es seguro.** Con evidencia válida, el resultado sería SUPERADO. La frase del gate y del README tendría que cambiar después del candidato, y entonces el vínculo fallaría y el resultado se forzaría a NO SUPERADO. Si no cambiara, el gobierno seguiría declarando NO SUPERADO junto a un gate SUPERADO.

Ninguna prueba existente registra los cuatro criterios en una fotografía del repositorio. La comprobación de `:2877`, por tanto, no la observa hoy ningún caso; el resultado de su ablación está en el [plan de pruebas](F36SBX_Plan_Pruebas_Sucesor_B01.md#1-situación-de-partida). Los controles positivos E00 y E00b de la batería en memoria prueban solo la función de decisión.

## 3. Superficies protegidas que el sucesor debe conservar

| Superficie | Dónde | Protección vigente |
|---|---|---|
| Ramas admitidas | `BRANCHES` | Fallo FRZ en otra rama (decisión T-04) |
| Paquete | `PKG_FILES`: 14 documentos y 4 JSON | STR, LNK, SEM y vínculo con el candidato |
| Contrato de evidencia y esquema de equipo | `CONTRACT_SHA256` y `TEAM_SCHEMA_SHA256` | SHA-256 de su JSON canónico |
| Herramientas | `docs/academico/tools/f36sbx/` | FRZ y vínculo: no cambian después del candidato |
| Gobierno | `GOV_FILES`: `CLAUDE.md`, `README.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md` | GOV (`REQUIRED_STATE` y estados de la base) y SEM |
| Fuentes de F33 y F34 | `F33_MATRIX` y `UPSTREAM_FILES` (5 archivos) | Lectura normativa (AF5) y FRZ |
| Antecedentes congelados | `F35_FROZEN`, 7 prefijos, incluido `docs/academico/TECHNICAL_DEBT.md` | FRZ |
| Runtime y dependencias | `RUNTIME_PREFIXES` (12) y `DEPENDENCY_FILES` (7) | FRZ y DEP |
| Integridad de Git | AF4 y AF5: objetos reales, índice por bytes, archivos regulares, sin enlaces ni redirecciones | FRZ y vínculo |

El sucesor no puede relajar ninguna. Solo añade las excepciones posteriores al candidato de la sección 5.5, cerradas y comprobadas línea a línea.

## 4. Invariantes del diseño

| ID | Invariante |
|---|---|
| I-1 | Falla cerrado: cualquier situación no prevista da NO SUPERADO y una falla del validador |
| I-2 | El resultado se **deriva** de la evidencia validada por `evaluate_gate()`. Ningún espejo, ni el JSON del estado, puede imponerlo: declarar un resultado distinto del derivado es una falla, en los dos sentidos |
| I-3 | Una sola derivación: todos los espejos se comparan con el mismo resultado R |
| I-4 | Lista cerrada de espejos (sección 5.2): fuera de ella, nada puede afirmar el resultado nuevo |
| I-5 | Después de H solo cambian las rutas y las líneas de la sección 5.5, comprobadas línea a línea |
| I-6 | Sin modos de excepción: ni argumentos de línea de órdenes, ni variables de entorno, ni archivos de configuración que alteren la decisión. Hoy `main()` no lee argumentos y el único acceso al entorno es `git_env()`; se conserva así y se prueba |
| I-7 | Identidad exacta de H: toda evidencia cita el mismo `candidate_commit`, y el estado del gate en H no contiene evidencia, ni candidato, ni un resultado distinto de NO SUPERADO |
| I-8 | Sin capacidades nuevas: B-01 no añade código de F37-SBX, dependencias ni rutas de runtime |
| I-9 | Los documentos históricos no cambian; fuera de los espejos solo se admiten los estados históricos (NO SUPERADO y BLOQUEADA) |
| I-10 | Una evidencia sintética nunca es auténtica, pero el validador no puede distinguirlas por estructura: lo impide el procedimiento (sección 8), no el código |

## 5. Política de transición

### 5.1 Resultado derivado

R es el valor de `evaluate_gate()` sobre el estado y la evidencia, forzado a NO SUPERADO si falla cualquier comprobación previa de la regla GATE (lo que ya hacen `:2857`–`:2859`). R vale NO SUPERADO, SUPERADO o REVOCADO.

Del resultado se derivan dos valores:

- el estado del gate, que es R;
- el estado de F37-SBX: con R en SUPERADO, el estado de habilitación que fije la decisión T-02; con R en NO SUPERADO o REVOCADO, BLOQUEADA.

### 5.2 Espejos cerrados

| ID | Fuente | Lugar exacto | Hoy |
|---|---|---|---|
| E1 | `gate/f36sbx_gate_state.json` | `declared_result` | NO SUPERADO |
| E2 | `F36SBX_Gate_Sucesor.md` | Una única línea canónica de resultado, en una sección propia que el sucesor crea | Cabecera (línea 3), que además describe la versión |
| E3 | `README.md` del paquete | Las viñetas del gate y de F37-SBX de la sección «Estado» | Líneas 8 y 9 |
| E4–E7 | `CLAUDE.md`, `README.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md` | Las viñetas del gate y de F37-SBX del bloque «Estado vigente» | Una viñeta por sujeto, **más** un párrafo del mismo bloque que vuelve a afirmar los dos estados |

**Requisito previo a H** (parte de D-07): en cada espejo debe quedar **exactamente una** afirmación por sujeto derivado dentro de su ámbito. Hoy los cuatro documentos de gobierno repiten los dos estados en el párrafo de F36, y el gate los afirma en una cabecera que mezcla la versión con el resultado. Antes de H, esos textos se reescriben para remitir a la viñeta, sin afirmar el estado. Así, la transición posterior cambia solo líneas canónicas.

### 5.3 Vocabulario cerrado

| Sujeto | En un espejo | Fuera de los espejos |
|---|---|---|
| F36-SBX-GATE | El valor derivado R: NO SUPERADO, SUPERADO o REVOCADO | Solo NO SUPERADO (afirmaciones históricas) |
| F37-SBX | El valor derivado: BLOQUEADA o el estado de habilitación de T-02 | Solo BLOQUEADA |
| F36-SBX | EN DISEÑO, salvo lo que decida T-03 | EN DISEÑO |

`allowed_states()` y `FORBIDDEN_CLAIMS` pasan a depender de R y del ámbito. Fuera de los espejos se mantienen como hoy, y la regla que prohíbe afirmar la habilitación de F37-SBX sigue vigente. La única excepción es la línea canónica de un espejo cuando R está en SUPERADO.

### 5.4 Estado de gobierno dependiente de R

`REQUIRED_STATE` pasa a ser una función de R, `REQUIRED_STATE(R)`: las 14 líneas que no dependen del gate, más la línea del gate con R y la de F37-SBX con su valor derivado. `rule_gov()` sigue exigiendo exactamente esas líneas, una vez cada una, y sigue conservando las líneas de la base `b8892af`.

### 5.5 Excepciones del vínculo después de H

Entre H y el árbol validado **solo** pueden cambiar:

| ID | Ruta | Qué puede cambiar | Comprobación |
|---|---|---|---|
| X1 | `gate/evidencia/` | Solo `FG-02.json`, `FG-03.json`, `FG-10.json` y `FG-12.json`, más el informe que cita FG-02; archivos regulares, citados y versionables | Vigente (regla GATE y AF5) |
| X2 | `gate/f36sbx_gate_state.json` | Solo `candidate_commit` (de nulo a H), el `status` y la `evidence` de FG-02, FG-03, FG-10 y FG-12, `f37_authorized_ei`, `declared_result` y `revocation` (de nulo a un evento). Todo lo demás, igual que en el blob de H | **Nueva**: comparación campo a campo con el blob de H |
| X3 | `F36SBX_Gate_Sucesor.md` | La columna Estado de la tabla FG y la línea canónica E2 | `doc_status_only()` generalizada a «solo líneas canónicas» |
| X4 | `README.md` del paquete | Las dos líneas canónicas de E3 | **Nueva**, misma función |
| X5 | Los cuatro documentos de gobierno | Las dos líneas canónicas de E4–E7 | **Nueva**, misma función |

La función generalizada exige el mismo número de líneas. Toda línea distinta tiene que ser, antes, la línea canónica del valor que tenía en H y, después, la del valor derivado de R. Cualquier otra diferencia es un cambio material posterior a H y falla.

### 5.6 Identidad del candidato H

- **Sin evidencia dentro de H.** En el blob de H, el estado del gate tiene `candidate_commit` nulo, FG-02, FG-03, FG-10 y FG-12 en PENDIENTE, `declared_result` en NO SUPERADO, `f37_authorized_ei` nulo y `revocation` nulo, y `gate/evidencia/` no existe. Esto impide un candidato que ya traiga evidencia o espejos adelantados.
- **Vínculo vigente.** Toda evidencia cita el `candidate_commit` del estado (vigente). Se mantienen el commit real con su SHA-1 verificado, la descendencia de la base, el ancestro de HEAD, la fiabilidad del estado de Git y las entradas normativas regulares.
- **Herramientas de H.** El validador que decide es el de H, porque las herramientas no pueden cambiar después de H. Quien valida comprueba además, con Git, que `docs/academico/tools/f36sbx/` no difiere de H (sección 8).

### 5.7 Sustitución de la comprobación de `:2877`

La comprobación «el gobierno de esta versión exige NO SUPERADO» se sustituye por «los espejos E1–E7 declaran exactamente el resultado derivado R». La frase actual del gate y del README (`:2874`) pasa a ser un caso de esa comprobación.

| Situación | Resultado del CLI |
|---|---|
| R en NO SUPERADO y espejos en NO SUPERADO, como hoy | 0 fallas |
| R en SUPERADO y espejos en SUPERADO, con el vínculo íntegro | 0 fallas |
| Cualquier diferencia entre R y un espejo, en cualquier sentido | Falla |

### 5.8 Revocación

Con `revocation` distinto de nulo, R pasa a REVOCADO y F37-SBX a BLOQUEADA en todos los espejos. Hoy `revocation` no tiene formato cerrado; T-05 decide si el sucesor lo cierra (fecha, motivo y ruta de evidencia) o lo deja para un incremento propio.

### 5.9 Ramas

B-01 no cambia `BRANCHES` para esconder el 57/2. Si H y los registros posteriores han de validarse en una rama nueva, añadirla es una decisión explícita (T-04), con su prueba, y nunca un patrón genérico.

## 6. Requisitos de los criterios EQUIPO que B-01 conserva sin relajar

| Criterio | Requisito que no cambia |
|---|---|
| FG-02 | Informe canónico del auditor elegible sobre H, en `gate/evidencia/`. Registro coherente con su bloque. Independencia declarada y verificada por personas. Veredicto aprobatorio con 0 BLOCKER, 0 HIGH y 0 MEDIUM que exija corrección, y los LOW abiertos declarados tal cual. **Sin quórum 3/3 propio** |
| FG-03 | `AUTORIZA_INICIO_F37_SBX`. Lista cerrada de EI ALLOWED o CONDITIONAL, idéntica a `f37_authorized_ei`, en el mismo orden. Numeración F36-M01 confirmada. Tres votos `APRUEBA` de las tres identidades exactas, sin duplicados, y quórum 3/3 |
| FG-10 | Siempre se registra, con 3/3, aunque no haya dependencias. Nunca NO APLICA. Con dependencias, contrato completo de versión, licencia, origen, revisión OSV real y hash del artefacto real |
| FG-12 | NO APLICA solo si FG-03 no autoriza ninguna EI CONDITIONAL; entonces no existe `FG-12.json` ni hay votos propios. En CUMPLE, 3/3, con la decisión sobre EI-09 y, si hay alcance C, el ADR sucesor APROBADO dentro de H |

**Refuerzo opcional (T-06).** Para un auditor `integrante_no_autor`, comparar su identidad con los autores Git de los commits entre la base y H. Requiere una tabla de correspondencia entre nombres y autores en el gobierno. Git no autentica, solo declara, así que no sustituye la verificación humana.

## 7. Plan de implementación, si se autoriza D-02

1. **RED.** Escribir antes las pruebas del [plan](F36SBX_Plan_Pruebas_Sucesor_B01.md) y observarlas fallar con el validador vigente.
2. **Validador.**
   - Función `derived_mirrors(R)`.
   - `REQUIRED_STATE(R)`, y `allowed_states()` y `FORBIDDEN_CLAIMS` dependientes del ámbito y de R.
   - Generalizar `doc_status_only()` a líneas canónicas.
   - Comprobación X2, campo a campo, del JSON del estado frente al blob de H.
   - Comprobación de H sin evidencia (5.6).
   - Sustituir la comprobación de `:2877` (5.7).
   - Añadir a `PKG_DOCS` los documentos nuevos del paquete, para que SEM y LNK los lean.
3. **Documentos normativos antes de H.**
   - La sección del resultado canónico en el gate.
   - La reescritura de los párrafos que duplican estados (D-07).
   - La documentación del sucesor.
   - La trazabilidad.
4. **Batería, metapruebas y regresión** de la sección 4 del plan.
5. **Congelación de H** solo cuando no quede ningún cambio material previsto (ver la [secuencia](F36SBX_Matriz_Preparacion_Gate.md#21-secuencia-hacia-el-candidato-h)).

## 8. Riesgos y límites que el diseño no elimina

- **Autenticidad.** El validador comprueba estructura, coherencia y vínculo Git. No autentica personas, firmas, votos ni sesiones: lo hace el procedimiento de la [lista de comprobación](BORRADOR_Checklist_Evidencias_y_Verificacion.md#2-procedimiento-de-verificación).
- **Autoconfianza del validador.** El validador que se ejecuta comprueba que las herramientas no cambiaron después de H, pero un validador alterado podría no comprobarlo. Por eso quien valida ejecuta también `git diff --quiet <H> HEAD -- docs/academico/tools/f36sbx` y solo acepta un árbol sin diferencias.
- **Fixtures sintéticos.** Los controles positivos pueden producir evidencia que pasa el validador. Por eso solo se crean en memoria o en clones desechables, y siempre sobre un candidato sintético creado en el clon, nunca sobre H.
- **Anclaje posterior.** Tras la transición, cualquier cambio posterior en la rama que valida, fuera de las excepciones, hace fallar el vínculo por diseño, como DG-02 en F35-SBX. La validación se ancla entonces en la rama del registro.
- **Ramas.** Mientras T-04 no se decida, el validador seguirá dando 57/2 en las ramas no admitidas, y el contenido se comprueba en clones con una rama admitida.

## 9. Decisiones de diseño pendientes del equipo

| ID | Decisión | Recomendación técnica, no vinculante | Estado |
|---|---|---|---|
| T-01 | Lista final de espejos (E1–E7) y reescritura previa de los textos que duplican estados | Aceptar la lista de la sección 5.2 | NO EMITIDA |
| T-02 | Estado de F37-SBX cuando el gate esté en SUPERADO | Un único estado de habilitación, sin enumerar EI en el gobierno: las EI viven en `f37_authorized_ei`. Ejemplo de redacción: «AUTORIZADA PARA INICIAR» | NO EMITIDA |
| T-03 | Si la transición cambia también el estado de F36-SBX | No. Su cierre sería un incremento propio | NO EMITIDA |
| T-04 | Rama en la que se fija H y se registran las evidencias | Validar en `develop` tras integrar H con autorización explícita, o admitir de forma explícita una sola rama nueva | NO EMITIDA |
| T-05 | Formato cerrado del evento de revocación | Cerrarlo en B-01 (fecha, motivo y ruta de evidencia) | NO EMITIDA |
| T-06 | Refuerzo de independencia para `integrante_no_autor` | Opcional; no sustituye la verificación humana | NO EMITIDA |
| T-07 | Versión del gate y del esquema de evidencia | Conservar `gate_version = 3` y el esquema v2: B-01 no cambia el formato de la evidencia | NO EMITIDA |
