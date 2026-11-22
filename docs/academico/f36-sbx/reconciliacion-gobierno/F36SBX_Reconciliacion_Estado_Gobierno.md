# F36-SBX — Reconciliación de referencias, estados y controles tras SEG-01 a SEG-04

> **Informe del 29/10/2026**, en la rama `docs/f36-sbx-team-governance-proposal`, creada desde `develop` = `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9`, árbol `82f27c9daf4305cafce6fb23a3b7b9277906b783`. **Solo documenta.** No cambia ningún estado, contrato, validador, evidencia congelada ni documento de gobierno.
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.
>
> **Versión corregida** el 29/10/2026, tras la auditoría documental de Codex sobre `729babb4a5584a4bc119fe61e59c101147e7acd5`, con veredicto CORRECCIONES REQUERIDAS (5 MEDIUM y 2 LOW). Recoge las correcciones de Q2-M01, Q2-M03, Q2-M04, Q2-M05 y Q2-L01. La matriz completa está en la respuesta a la auditoría de esta misma carpeta.

Cada afirmación lleva su naturaleza:

- **[H]** es un hecho comprobado en esta sesión con Git, `ls-remote` o el validador.
- **[R]** es una afirmación recibida que aquí no se puede verificar.
- **[P]** es una propuesta.

La propuesta sucesora de Q y el roadmap están en documentos aparte de esta misma carpeta, enlazados desde su README.

## 1. Base verificada [H]

| Referencia | Valor |
|---|---|
| `develop` local, `origin/develop` y el remoto real (`ls-remote`) | `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9`, árbol `82f27c9daf4305cafce6fb23a3b7b9277906b783`, padres `25462977dd5d…` y `484c20452b2a…` (merge de SEG-04) |
| CI de ese commit | `tests`, ejecución 40923175235, `success`. Ejecuta build, TypeScript y PHPUnit (444 aprobadas y 8 omisiones de Fortify preexistentes); no ejecuta Cypress |
| `main` local, `origin/main` y el remoto real | `55f758e013e1852de8c8daa5d6fde95e39b02b0d`, árbol `01dc59a80eed0e9f7c26143f6787010fcefb406c`, padres `b8892af39a64…` y `55456943059e…` |
| Stash protegido | `6a42795dd19646eef212da85c5d9ad7661874321`, árbol `8bfb140debe3…`. Presente y sin aplicar |
| Checkout principal | `feature/f36-sbx-authorization-design` @ `4a2b2d7`, limpio, sin operaciones Git en curso |

## 2. Referencias reconciliadas [H]

### 2.1 Identidad

| Ref | Commit completo | Árbol | Padre | Fecha | Rama local | En el remoto |
|---|---|---|---|---|---|---|
| AF5 | `4a2b2d7e78d162dc59e099325e3603407dcfb5fc` | `01dc59a80eed0e9f7c26143f6787010fcefb406c` | `b2876fca59deaaa3f3f06f65d7c92bc143d0f865` | 27/10/2026 | `feature/f36-sbx-authorization-design` | Sí: la misma rama, y es ancestro de `origin/develop` y `origin/main` |
| AF6 | `88fd3d2ee8b863bd8487001a45f50177c073e15a` | `765c2d4874e8f1e7e0cd937f306ca92c3b9a494c` | `af9b05ed7b220c831a2f18c61b425a96ae1d1cee` | 27/10/2026 | `docs/f36-sbx-gate-preparacion-af6` | No |
| H preliminar | `1d5d6aa5c56ef682433b8a20854b5a0cfa78513d` | `f62a6748b830115b13edeadb594caf72c08b8666` | `2627ee94da3880e8e30dc32ef1202615f2c82279` | 27/10/2026 | `feature/f36-sbx-gate-transition-h` | No |
| Q | `061ba68a082173ed679f03151efa7191444ca8a7` | `7b3879e102025ce9191c66629c1a6b250931f945` | `d5c59d969cbe8c4317c6aef81de54525891640e8` | 27/10/2026 | `docs/f36-sbx-unipersonal-governance-proposal` | No |

Que AF6, H y Q no estén en el remoto no significa que no existan. Están completos en este clon, que no es superficial. Los 32 commits de F36-SBX hasta AF5 (`b8892af..4a2b2d7`) y los 8 de AF6, H y Q tienen como autor Git a «Luis Vila Meza».

### 2.2 Cadena e integración

```
develop: 87ef831 ──┬── 5545694  merge de AF5 (padres 87ef831 y 4a2b2d7)
                   └── 4a2b2d7  AF5
main:    b8892af ──┬── 55f758e  merge de develop 5545694 (árbol 01dc59a, el de AF5)
                   └── 5545694
AF6:     55f758e → 20527db → af9b05e → 88fd3d2
H:       88fd3d2 → a5a8166 → 2627ee9 → 1d5d6aa
Q:       1d5d6aa → d5c59d9 → 061ba68
develop: 5545694 → SEG-01, SEG-02, SEG-03 y SEG-04 (20 commits) → 9dd76c4
```

Commits completos de los tramos:

- **AF6:** `20527db301dc2cccb329433ea534520c4a2a82e7`, `af9b05ed7b220c831a2f18c61b425a96ae1d1cee` y `88fd3d2…`.
- **H:** `a5a81661200fc6daffcad356946808370d66691e`, `2627ee94da3880e8e30dc32ef1202615f2c82279` y `1d5d6aa…`.
- **Q:** `d5c59d969cbe8c4317c6aef81de54525891640e8` y `061ba68…`.

| Ref | Base | Solo en la ref | Solo en `develop` | Documentos | Estado declarado | ¿Integrada? |
|---|---|---|---|---|---|---|
| AF5 | Rama desde `b8892af` | 0 | — | Paquete F36-SBX y sus herramientas, en su versión AF5 | F36-SBX en diseño, gate no superado, F37-SBX bloqueada. El merge `5545694` cita la sexta auditoría: 0 BLOCKER, 0 HIGH, 0 MEDIUM; AF6-L01 y AF6-L02 LOW abiertos | **Sí**, en `develop` (`5545694`) y en `main` (`55f758e`) |
| AF6 | `main` `55f758e`; base común con `develop`: `5545694` | 4 (`55f758e` y sus 3 commits) | 20 | 11 archivos (+501/−6), todos en `docs/academico/f36-sbx/`: registro y deuda AF6, y `preparacion-gate/` (matriz, borradores de acta y de lista de comprobación) | Preparación: no registra evidencia ni cambia estados. Auditoría documental de Codex registrada en la matriz de H §10 [R] | No |
| H preliminar | AF6 | 7 | 20 | 10 archivos (+493/−59), en `docs/academico/f36-sbx/`: especificación y plan de pruebas de B-01, borrador D-02 y actualización de la matriz | «Preparación H lista; implementación de B-01 pendiente de la autorización D-02.» B-01 sin implementar y H sin congelar. **No consta ninguna auditoría de H** | No |
| Q | H preliminar | 9 | 20 | 7 archivos (+302/−3): `F36SBX_Propuesta_Gobierno_Unipersonal.md`, `BORRADOR_Expediente_Adecuacion_Unipersonal.md` y ajustes de D-02, B-01, la matriz, el README y la trazabilidad | «PROPUESTA — NO VIGENTE — PENDIENTE DE AUTORIZACIÓN», clase B, con U-01 a U-05 pendientes | No |

**Solapamiento.** Desde `5545694`, `develop` cambió 18 archivos, todos de SEG-01 a SEG-04 y todos fuera de `docs/academico/f36-sbx/`. AF6, H y Q solo cambian archivos dentro de esa carpeta, así que no hay conflicto textual entre los dos lados. Integrarlos sigue necesitando la decisión D-08, y no arreglaría la regla FRZ en `develop` (§3.3).

El contenido de AF6, H y Q se cita aquí por commit y ruta, por ejemplo `061ba68:docs/academico/f36-sbx/preparacion-gate/F36SBX_Propuesta_Gobierno_Unipersonal.md`. Esta rama no los integra ni los copia.

## 3. Estado real de Q, H, B-01 y los gates

### 3.1 Mediciones del validador [H]

[`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py) se ejecutó en solo lectura, con `python -I -B`, sobre cada rama real, sin cambiar su nombre, su base ni sus reglas:

| Árbol validado | Rama | Correctas/fallas | Gate calculado |
|---|---|---|---|
| AF5 `4a2b2d7` | `feature/f36-sbx-authorization-design` | 59/0 | NO SUPERADO |
| Q `061ba68` | `docs/f36-sbx-unipersonal-governance-proposal` | 57/2 | NO SUPERADO |
| `develop` `9dd76c4` | `develop` | 56/3 | NO SUPERADO |
| Q2 original `729babb` | `docs/f36-sbx-team-governance-proposal` | 55/4 | NO SUPERADO |

La auditoría de Codex sobre `729babb` reprodujo las cuatro cifras en clones aislados, con los nombres de rama reales. El resultado del candidato corregido figura en el README.

| Comprobación | AF5 | Q | `develop` | Q2 original |
|---|---|---|---|---|
| FRZ — rama admitida | Pasa | Falla | Pasa | Falla |
| FRZ — cambios solo en el paquete, sus herramientas y el gobierno | Pasa | Pasa | Falla: 18 rutas externas | Falla: las mismas 18 |
| FRZ — 0 cambios de runtime, producto o dependencias | Pasa | Pasa | Falla: 11 entradas | Falla: las mismas 11 |
| GATE — los AUTO declarados coinciden con los recalculados | Pasa | Falla: FG-01 y FG-05 | Falla: FG-01 y FG-05 | Falla: FG-01 y FG-05 |

- **Las 18 rutas externas al paquete** son las de SEG-01 a SEG-04:
  - 5 archivos de `app/`: `ApplicationController`, `ApplicationPolicy`, `CandidateDocumentPolicy`, `ApplicationStageService` y `JobRequestWorkflow`;
  - `docs/assumptions.md` y `docs/defects.md`;
  - 5 documentos de `docs/v1.1/security/`;
  - 6 archivos de pruebas.
- **Las 11 entradas del chequeo de runtime** son los 5 archivos de `app/` y los 6 de pruebas, porque `RUNTIME_PREFIXES` incluye `tests/`. No son 11 cambios funcionales: los funcionales son los 5 de `app/`.
- **De `develop` a Q2 original solo cambia una comprobación de las 59:** «FRZ — rama admitida». Las cuatro rutas nuevas de Q2 caen dentro del paquete, así que ni la lista externa ni la de runtime crecen. Hay, por tanto, una comprobación adicional fallida por el anclaje de rama, sin rutas externas ni fallas de contenido nuevas.
- **FG-01 y FG-05.** El validador deriva FG-05 de FRZ y FG-01 de todas las reglas AUTO. El estado del gate los declara CUMPLE; cuando FRZ falla, los dos se recalculan NO CUMPLE y la regla GATE falla por la divergencia. La causa de que FRZ falle depende de la rama:
  - en Q, solo la rama;
  - en `develop`, las dos comprobaciones de contenido de FRZ;
  - en Q2 original, las tres.

  FG-14 solo comprueba que no haya un evento de revocación registrado; no interpreta el supuesto material del charter (§3.3).

La matriz de H (§9) registra el mismo 57/2 para AF6 y H por el anclaje de rama [R]; esta sesión no lo repitió sobre esas dos ramas.

### 3.2 Estado por sujeto

| Sujeto | Estado declarado | Fuente | Comprobación [H] |
|---|---|---|---|
| F36-SBX | En diseño. AF5 integrada en `develop` y `main` | [`CLAUDE.md`](../../../../CLAUDE.md), [charter](../F36SBX_Charter.md) y el merge `5545694` | Consistente. `CLAUDE.md` todavía la describe como «candidata a auditoría independiente, sin push, merge, tag ni release» (§7) |
| F36-SBX-GATE | No superado. `candidate_commit`, `f37_authorized_ei` y `revocation` nulos. FG-02, FG-03, FG-10 y FG-12 pendientes; los AUTO, declarados CUMPLE | [`f36sbx_gate_state.json`](../gate/f36sbx_gate_state.json) y [gate](../F36SBX_Gate_Sucesor.md) | El resultado registrado sigue NO SUPERADO. En `develop`, FG-01 y FG-05 se recalculan NO CUMPLE (§3.1). La vigencia material de la autorización de F36-SBX frente a §7 del charter está pendiente de determinarse (D-10, §3.3) |
| F37-SBX | Bloqueada | Gate y charter | Consistente |
| B-01 | El validador vigente exige que el gobierno declare NO SUPERADO | Gate §9; especificación en `1d5d6aa` | Presente en el código: `rule_gate()` exige NO SUPERADO y `allowed_states()` solo admite ese resultado. El sucesor está especificado, no implementado. D-02b no está emitida |
| H | El candidato final H no existe. `1d5d6aa` es una rama de preparación | Matriz de H §2.1 | No consta ninguna auditoría de H. Ninguna auditoría de AF5 ni de AF6 vale para H |
| Q | Propuesta no vigente, clase B; U-01 a U-05 pendientes | `061ba68` | Veredicto de su auditoría: «APROBADA CON CORRECCIONES DOCUMENTALES PENDIENTES», con 0 BLOCKER, 0 HIGH, 5 MEDIUM, 2 LOW y 2 INFO. El informe íntegro está disponible fuera del repositorio (§4.1) |
| D-01 a D-09 | Todas no emitidas. D-01 tiene una instrucción operativa (b), sin decisión formal | Matriz de H §7 y Q §10 | Sin cambios. Ninguna consta emitida en Git |
| ADR-005, G0 real y G0-SBX | Propuesta; no aprobada; aprobada con restricciones, solo para F35-SBX | `CLAUDE.md` y `docs/academico/g0-evidence/` | Sin cambios |

### 3.3 D-10: la cláusula de revocación del charter y la regla FRZ

Hay cinco cosas distintas que no deben confundirse:

1. **Ámbito y periodo de la autorización [H].**
   - **Qué autoriza.** El [charter §1](../F36SBX_Charter.md) autoriza investigar y diseñar F36-SBX, con sus validadores documentales y sus pruebas. Su gate decide una sola cosa: si F37-SBX puede comenzar.
   - **Cuándo.** Se abrió por una instrucción del equipo del 26/10/2026. AF5 quedó fijado el 27/10/2026 (`4a2b2d7`) y ese mismo día se integró en `develop` (`5545694`).
   - **Hasta dónde llega.** La cláusula afecta a esa autorización y a su puerta a F37-SBX. No rige el mantenimiento del SaaS ni la validez técnica de SEG.
2. **Hecho que podría activar la cláusula [H].** El charter §7 revoca F36-SBX, entre otros supuestos, si «se modifica una superficie congelada de F35-SBX, el runtime o las dependencias».
   - **Qué ocurrió.** SEG-01 a SEG-04 modificaron cinco archivos de runtime en `develop` después de abrirse el charter. Los commits son `e1f1f1a`, `4c89a95` y `afa6282`, del 28/10/2026, y `74bcdf5`, del 29/10/2026; se integraron con `2e53786` (28/10/2026), `2546297` y `9dd76c4` (los dos del 29/10/2026).
   - **No hay excepción escrita** para el mantenimiento de seguridad auditado.
   - **Dos lecturas.** En la lectura literal amplia, esos cambios encajan en el tipo de hecho descrito. En una lectura restringida al trabajo hecho bajo F36-SBX quedarían fuera, pero esa restricción habría que documentarla con sus razones.
   - **Lo que FRZ no decide.** La falla de FRZ no resuelve por sí sola esta interpretación: FRZ mide un perímetro técnico desde `b8892af` en la rama que se valida.
3. **Efecto condicional previsto [H].** La cláusula dice: «si ocurre cualquiera de estos hechos, F36-SBX queda REVOCADA y su gate pasa a REVOCADO». Es un efecto condicional: si el supuesto se acredita, no hace falta otra votación para que se produzca.
4. **Registro declarativo [H].** El gate §5 exige registrar la revocación en `revocation`, con fecha, motivo y evidencia, en un incremento nuevo. El registro documenta el hecho; no lo crea ni lo elimina. `revocation = null` solo muestra que no hay ningún evento registrado, no que el supuesto material nunca ocurriera.
5. **Autorización nueva o enmienda, solo hacia adelante [P].**
   - Si se acredita el supuesto, corresponde registrar el hecho y, si el equipo quiere continuar, una autorización nueva con su fecha.
   - Si se documenta una aclaración de ámbito, solo puede regir hacia adelante, y se conservan las mediciones y las anclas históricas (AF5 59/0; `develop` 56/3).

**[P] D-10, reformulada.** Hay que determinar documentalmente el ámbito y el periodo aplicables, y acreditar o descartar el supuesto con sus fundamentos. Según el resultado, se registra el hecho y, si procede, una autorización nueva, o se documenta la aclaración de ámbito con efecto solo prospectivo. D-10 no es una elección sobre qué ocurrió en el pasado, y un anclaje o una base nuevos no regularizan hechos anteriores.

**Lo que este documento no hace:** no revierte SEG, no modifica `f36sbx_gate_state.json`, no registra una revocación y no emite una autorización nueva. El resultado registrado sigue NO SUPERADO y F37-SBX sigue BLOQUEADA.

## 4. Matriz de observaciones anteriores

### 4.1 Auditoría de Q

**Actualización [H].** El informe íntegro está disponible fuera del repositorio, donde Codex lo conserva:

`C:/Users/Vila/.codex/visualizations/2026/10/27/01a17ebf-75df-7883-a55e-3ede1b24ee18/F36-Unipersonal-Audit-061ba68/Informe_Auditoria_Unipersonal_061ba68.md`

Su SHA-256, `a1dbc1d2b3951fbeb83284925ee961987dcafcab2c93c3d8af5cfad1b350a0ab`, coincide con el comunicado y figura en el manifiesto `SHA256SUMS.txt` de esa carpeta.

**Hecho histórico.** La versión `729babb` de este informe decía que solo se conocían los conteos. Era el resultado de una búsqueda acotada:

- en todas las referencias Git;
- en varias carpetas locales, incluida `C:\Users\Vila\.codex`, pero solo hasta cuatro niveles de profundidad;
- en el directorio personal de WSL.

La carpeta de Codex está a seis niveles, así que la búsqueda no la alcanzó. No era imposible recuperar el informe.

**Los nueve hallazgos** (UNI-M01 a UNI-M05, UNI-L01, UNI-L02, UNI-I01 e UNI-I02) y su correspondencia con este candidato están en la respuesta a la auditoría de esta carpeta. **Ninguno se cierra formalmente por sustituir Q**: Q no se modifica, y las correcciones que les corresponden están implementadas en el nuevo candidato, pendientes de la revisión de Codex.

### 4.2 Otras observaciones disponibles [H]

| ID | Severidad | Estado | Dónde consta | Relación con esta reconciliación |
|---|---|---|---|---|
| Q2-M01 a Q2-M05, Q2-L01 y Q2-L02 | MEDIUM y LOW | Corregidos en este candidato, pendientes de revisión | Auditoría de Codex sobre `729babb`, fuera del repositorio | Matriz en la respuesta a la auditoría |
| AF6-L01 y AF6-L02 | LOW | Abiertos: residuos de la guardia de identidad (vocabulario de relleno y homógrafos latinos y armenios) | Mensaje del merge `5545694`; `88fd3d2:docs/academico/f36-sbx/F36SBX_Deuda_Tecnica_AF6.md` | Pueden corregirse en un incremento propio de mantenimiento, con su alcance, autorización, RED/GREEN y revisión (§6). D-05 solo decide su tratamiento si se incluyen en H. No exigen D-02b por ser código Python |
| DOC-AF6-L01, DOC-AF6-L02 y DOC-AF6-I01 | LOW, LOW e INFO | Tratados en la matriz de H §10, sin auditoría posterior | `1d5d6aa` | El tratamiento no está auditado porque H no se auditó |
| GC-AF-L01 | LOW | Abierto y diferido | [`TECHNICAL_DEBT.md`](../../TECHNICAL_DEBT.md) | Ajena a Q2 |
| SEG01-AUD-L01 y SEG02-AUD-I01 | LOW e INFO | Abiertas | Documentos SEG en `docs/v1.1/security/` | Ajenas a Q2 |
| Tratamiento de registros de auditoría anteriores | — | Propuesta separada, no ejecutada | [SEG-04 §9](../../../v1.1/security/SEG-04-minimizacion-metadatos-auditoria.md) | Ajena a Q2 |
| Deuda global de Pint (8 archivos) y PHPStan (91 errores) | — | Equivalente a la base | SEG-04 §7 | Ajena a Q2 |

## 5. Origen y vigencia de los controles

### 5.1 (a) Obligaciones académicas externas demostradas [H]

| Obligación | Fuente | Alcance |
|---|---|---|
| Curso Pruebas y Calidad de Software, NRC 28607, con el docente Dr. Maglioni Arana Caparachin | [`ACADEMIC_BASELINE.md`](../../ACADEMIC_BASELINE.md) y [`CLAUDE.md`](../../../../CLAUDE.md) | Identificación del proyecto ante el curso |
| Equipo declarado ante el curso: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio | Informe final v1.0, prácticas F2 a F11 y F29H | Autoría académica de los entregables. Ninguna regla interna la cambia |
| Guías y formatos oficiales de las prácticas 02 a 09 y 11, y plantilla del informe final | [Inventario de fuentes oficiales](../../00-fuentes-oficiales/inventory.md), con tipo OFICIAL | Contenido y formato de los entregables académicos |
| **Formar equipos de tres estudiantes para el proyecto grupal** | Las nueve guías oficiales (§5.1.1): «Para el desarrollo de la práctica los estudiantes deberán seguir las siguientes indicaciones, formando equipos de 3 estudiantes para la entrega del proyecto grupal al final de la asignatura» | La composición del equipo académico del proyecto grupal |

#### 5.1.1 La instrucción de las nueve guías [H]

La frase citada aparece, con texto idéntico, en el mismo párrafo de `word/document.xml` de las nueve guías de `docs/academico/00-fuentes-oficiales/guias/`. La numeración del párrafo depende del método de extracción: Codex lo cuenta como el 12 del cuerpo. Se comprobó leyendo los blobs de `9dd76c4`, sin abrir Office.

| Guía | SHA-256 |
|---|---|
| `GUIA_PRACTICA_02.docx` | `a089eea421ab4589bdefdd2a68ef8bf3d3ab20cd88a73b18a095fbdb213eb854` |
| `GUIA_PRACTICA_03.docx` | `2651dc652b64e7f3aa9f6849e4af05e6ba37027086b40491cf5ad88685611f13` |
| `GUIA_PRACTICA_04.docx` | `2626f3994c35356495aaa80a9f978324406e90fba628fecb73dc5243f6e21fd7` |
| `GUIA_PRACTICA_05.docx` | `bc22e93eaa98804b36f88b08b4918f46d6fc7d0567346c98837fae1627e5f81a` |
| `GUIA_PRACTICA_06.docx` | `fe458ad4fa41e5517f9584b5b773dcbadebce5a130c35a4c4b7550ec71dba54d` |
| `GUIA_PRACTICA_07.docx` | `5ccbfc5444c377735678b1c8a701131ac99ab98b7720a601becc9bb8ba2b0e4f` |
| `GUIA_PRACTICA_08.docx` | `43013822ad4ab2e108b40cbe2e732d62001fa289d259f148515c281ccd0793a0` |
| `GUIA_PRACTICA_09.docx` | `89d3f2783941b11aa7be0ccba7450cec5b6a821c480e528ac23d20e7e6c37c6d` |
| `GUIA_PRACTICA_11.docx` | `c70f913787f81e250eee843eff197c8efb3ecda32896deb40afaabbfdb9689e7` |

Los nueve hashes coinciden con el [inventario](../../00-fuentes-oficiales/inventory.md) y con las auditorías de Q y de Q2. La copia histórica `docs/academico/phase-24/GUÍA PRÁCTICA 09.docx` tiene el mismo hash que la guía 09. La versión `729babb` de este informe negaba esta instrucción; era un error (Q2-M01, y antes UNI-M02).

**Qué demuestra y qué no.** La instrucción exige que el proyecto grupal lo entreguen equipos de tres estudiantes. El equipo de Luis Vila Meza, Fredy Coronacion y Anthony Peña responde a ella, y Q2 conserva a los tres, así que no hace falta una excepción individual. La instrucción **no** demuestra:

- tres votos por commit;
- una contribución técnica igual de los tres;
- una autorización docente universal;
- el mecanismo 3/3 de FG-03, FG-10 y FG-12.

**Tres cosas distintas:**

1. **La composición académica de tres integrantes** es una obligación externa acreditada por las guías.
2. **El quórum interno para actos concretos** es una regla del proyecto: la aprobación de ADR-005 (F34A) y FG-03, FG-10 y FG-12 de F36-SBX (§5.2).
3. **Las decisiones técnicas ordinarias** se rigen por las reglas vigentes del repositorio (§5.2), y Luis es el único desarrollador técnico [R]. No se encontró ninguna regla externa sobre ellas.

**No acreditadas.** No hay en el repositorio sílabo, rúbrica ni norma del curso sobre:

- el reparto de la contribución técnica;
- el uso de IA;
- la aprobación de decisiones técnicas;
- la autorización docente de commits;
- la aplicabilidad actual de las guías, o eventuales excepciones.

Quedan **no acreditadas**: que no se encontraran no prueba que no existan, y si aparece una fuente aplicable se conserva y se cumple.

### 5.2 (b) Reglas internas creadas por el proyecto [H]

| Regla | Fuente | Alcance |
|---|---|---|
| Contratos 1 a 10, incluido el 10: «sin push, merge, release ni tag sin autorización explícita del equipo» | `CLAUDE.md` | Todo el repositorio |
| Gobierno para Codex y flujo multiagente, con un solo escritor por rama | [`AGENTS.md`](../../../../AGENTS.md) y [`multi-agent-workflow.md`](../../../v1.1/multi-agent-workflow.md) | Uso de herramientas |
| Skills del proyecto, por ejemplo `project-guardian` | `.claude/skills/` | Procedimiento de cambio |
| Aprobación de ADR-005 por los tres integrantes | [`F34A_Paquete_Aprobacion_ADR005.md`](../../g0-readiness/F34A_Paquete_Aprobacion_ADR005.md) (línea 106), cumplida en F34C ([acta](../../g0-evidence/F34B_Acta_Aprobacion_ADR005.md)) | G0-14, ya cumplido |
| G0, G0-SBX, SBX-01 a SBX-18 y los gates de F35-SBX | `docs/academico/g0-*` y `evidencia-sbx-*` | Puertas del ciclo inteligente |
| Charter y gate de F36-SBX, con el quórum 3/3 de §8.1 para FG-03, FG-10 y FG-12 | [Charter](../F36SBX_Charter.md) y [gate](../F36SBX_Gate_Sucesor.md) | Solo el paso de F36-SBX a F37-SBX |

El quórum 3/3 reproduce el patrón de F34A y F34C. Es interno: la instrucción del curso exige equipos de tres estudiantes (§5.1), no tres votos para actos técnicos.

### 5.3 (c) Controles técnicos de seguridad e integridad [H]

Se conservan sin cambios:

- multiempresa con `organization_id`, Policies y pruebas cross-tenant;
- auditoría de solo inserción (trigger `audit_logs_append_only`, A-34), con metadatos minimizados (A-38, SEG-04);
- RF-23 humana;
- solo datos sintéticos;
- ningún secreto versionado;
- el tag `v1.0.0-academic` inmutable;
- CI `tests` obligatoria para publicar;
- los validadores F34B, F35-SBX y F36-SBX, que fallan cerrado;
- las prácticas Git: sin force push ni reescritura de historia publicada;
- las correcciones DEF-14 a DEF-17.

### 5.4 (d) Validaciones externas pendientes [H]

| Validación | Estado |
|---|---|
| G0-02, G0-03 y G0-12 | PENDIENTE EXTERNO. La respuesta de G0-12 quedó sin evidencia archivada (F34D) |
| Fila consultiva del docente en el acta de ADR-005 | Pendiente ([acta](../../g0-evidence/F34B_Acta_Aprobacion_ADR005.md)) |
| Validación institucional de RF-29 | No validada; RF-29 sigue siendo experimental ([F17](../../../v1.1/phase-17-ml-validation.md)) |
| Revisión jurídica y de privacidad para datos reales | No solicitada. Los datos reales siguen prohibidos |
| Reconocimiento docente de un cambio de gobierno interno | **Ninguna fuente lo exige.** Las guías piden equipos de tres estudiantes, y Q2 mantiene a los tres integrantes, así que no hace falta una excepción individual. Q lo recomendaba en su lectura (a) y lo exigía en la (b) |
| Aclarar la discrepancia entre las declaraciones del 27/10/2026 y las del 28 y 29/10/2026 sobre la composición del equipo | Pendiente. Corresponde a la declaración R-01 de Luis (Q2 §2), sin reinterpretar la historia |

### 5.5 Cómo se modifican las reglas internas, de forma prospectiva

- **El gate y el validador** cambian mediante «un incremento sucesor auditado que actualice el gobierno y el validador» (gate §9).
- **El gobierno**, según la práctica de F35-SBX-B y Q §3, necesita además la autorización explícita del equipo; el equipo son los tres integrantes declarados.
- **Lo que no cambia:** ninguna enmienda recalifica lo anterior a su adopción, y los registros congelados (F34C, F35-SBX y AF1 a AF6) no se editan; una aclaración solo puede añadirse como anexo fechado.

### 5.6 D-11: autorización operativa y representación del equipo en el contrato 10 [H]

- **Lo que dice el contrato.** El contrato 10 exige «autorización explícita del equipo» para `push`, `merge`, release o tag. No fija quórum ni un formato numérico por operación.
- **Lo que está acreditado.** Las integraciones y publicaciones de SEG-01 a SEG-04 se hicieron con autorizaciones explícitas de Luis, una por operación, registradas en los mensajes de commit, en los documentos SEG y en la sesión. Son **autorizaciones operativas de Luis**, y así quedan.
- **Lo que no está documentado.** Que esas autorizaciones fueran además una representación del equipo conforme al contrato 10. No hay votos de Fredy ni de Anthony, ni una delegación documentada.
- **Lo que no se deduce.** La brecha no invalida las correcciones SEG, que se auditaron e integraron con la CI en verde. Tampoco obliga a tres votos por commit ni exige revertir nada. No se fabrican delegaciones ni votos con fecha anterior.

**[P] D-11, prospectiva.** Definir quién autoriza cada operación del contrato 10, con qué límites y con qué evidencia. Hay dos opciones legítimas:

- **(a)** un mecanismo colegiado, sin inventar un quórum que el texto no fija;
- **(b)** una delegación en Luis, mediante actos auténticos de Fredy y de Anthony, con fecha real y alcance futuro, como prevé Q2 (§7 y §9).

Lo anterior a esa decisión se reconoce tal como está registrado.

## 6. H, B-01 y actividades permitidas

La columna «Fuente vigente» cita las reglas en vigor hoy. Los niveles N1 a N5 de Q2 son una clasificación propuesta: no crean ni amplían permisos y solo regirían después de su adopción (Q2 §9).

| Actividad | Fuente vigente | Evidencia disponible | Bloqueo específico | Trabajo permitido mientras tanto | Condición objetiva para continuar |
|---|---|---|---|---|---|
| Desarrollo técnico ordinario del SaaS: defectos, seguridad, refactors y pruebas | Contratos 1 a 10 (`CLAUDE.md`), `AGENTS.md`, `project-guardian`, `laravel-saas-quality` y el alcance autorizado de cada incremento | SEG-01 a SEG-04, con RED/GREEN, auditoría y CI | **Ninguno del gate**, que solo decide F37-SBX | Todo, en ramas `fix/*`, `feature/*`, `docs/*` o `chore/*` | Las reglas vigentes |
| Integrar y publicar `develop`, `main`, tags y releases | Contrato 10: autorización explícita del equipo | Las autorizaciones operativas de Luis en SEG (§5.6) | La representación documentada del equipo no está definida (D-11) | Preparar candidatos y auditorías | Autorización explícita por operación conforme al contrato 10. D-11 la precisará hacia adelante |
| Mantener el ML operacional existente (ML-01) sin cambiar su contrato | Skill `ml-risk-service` y documentación de F15 a F17 | Servicio experimental integrado | Ninguno del gate | Correcciones, QA y reconstrucción reproducible del artefacto desde el *freeze* aprobado | Conservar el *freeze*, el umbral y el contrato de variables |
| QA visual, accesibilidad y rendimiento | Skills `frontend-design`, `animate` y `reviewing-a11y`, ADR-003, `data-cy` y Cypress | Fases 18 a 21 | Ninguno del gate | Las pruebas pendientes con lector de pantalla y con un equipo modesto | Las reglas vigentes; ampliar el 3D exige una decisión nueva |
| Mantener la documentación del paquete F36-SBX | Charter §1 | AF6, H y Q en local | Integrarlos exige D-08 | Preparar documentos en ramas propias, sin integrar | D-08 |
| Diseñar el sucesor B-01 y su plan de pruebas | Charter §1, como D-02a | Especificación y plan (`1d5d6aa`) | — | Afinar el diseño y auditarlo como documentación | Implementarlo exige D-02b |
| Implementar el sucesor B-01, que habilita la transición a SUPERADO | Gate §9 | Ídem | D-02b no está emitida | Ninguna implementación | D-02b auténtica y las decisiones de diseño; después, un H nuevo auditado |
| Corregir defectos independientes del validador, como AF6-L01 y AF6-L02 | Charter §1: validadores documentales y sus pruebas | Registro de deuda AF6 | Ninguno de B-01: no exigen D-02b por ser código Python | Un incremento propio de mantenimiento | El alcance y la autorización aplicables, RED/GREEN, un candidato nuevo y su revisión. Si se incluyen en H, D-05 decide su tratamiento |
| Sincronizar hechos documentales sin cambiar estados ni contratos (`CLAUDE.md`, `PROGRESS.md`, `README.md` y `ACADEMIC_BASELINE.md`) | `AGENTS.md` y `academic-traceability` admiten la evolución documental autorizada. La regla GOV comprueba invariantes (las líneas de estado y la de integrantes); no prohíbe toda edición | Deuda inventariada (§7) | Ninguno general | Proponer deltas, como hace este paquete, o hacer un incremento documental autorizado que conserve los invariantes | La autorización del incremento. Dentro de H, D-07 organiza la sincronización. Cambiar estados, contratos o el mecanismo de autorización exige su propio procedimiento |
| Determinar el supuesto de §7 del charter (D-10) | Charter §7 y gate §5 | Mediciones de §3.1 | D-10 sin resolver | Documentar hechos, periodo y ámbito | D-10, con efecto solo prospectivo para cualquier aclaración (§3.3) |
| Fijar el candidato H | Gate §9 y la estrategia H, si se elige | — | Faltan D-01 formal, D-02b y los cambios materiales que se elijan (D-05, D-06 y D-07) | No | Todos los cambios materiales hechos |
| FG-02, auditoría de H | Gate §8.2 y §8.6 | Ninguna: AF6 no sirve para H | H no existe | No | H fijado |
| FG-03, FG-10 y FG-12 | Gate §8.1: 3/3 cuando se registra CUMPLE | Ninguna | Faltan actos auténticos de los tres integrantes, o un contrato sucesor adoptado, y una FG-02 favorable | Solo borradores de formato | Actos auténticos de cada integrante. FG-12 puede quedar en NO APLICA solo según el contrato, sin archivo ni votos propios |
| Ejecutar EI o iniciar F37-SBX (A o B) | Gate y matriz de capacidades | — | F36-SBX-GATE = NO SUPERADO | Nada de EI | El gate superado con el sucesor B-01, la lista de EI y las demás condiciones |

## 7. Deuda documental inventariada [H]

Se inventaría sin corregir; su actualización queda fuera de este incremento:

- **DEF-14, DEF-15, DEF-16 y DEF-17** dicen «pendiente de auditoría» en [`defects.md`](../../../defects.md), aunque las cuatro auditorías fueron favorables y están integradas en `develop`.
- **[`CLAUDE.md`](../../../../CLAUDE.md):**
  - no menciona SEG-01 a SEG-04 en ninguna línea;
  - en la 101 describe F36-SBX como «candidata a auditoría independiente, sin push, merge, tag ni release», cuando AF5 está integrada;
  - su bloque de estado sigue fechado en F34E.
- **[`PROGRESS.md`](../../../PROGRESS.md):** la última actualización es del 26/10/2026, y no registra SEG ni la integración de AF5.
- **[`AGENTS.md`](../../../../AGENTS.md):** la línea 76 atribuye a ChatGPT «arquitectura, prompts y decisiones», y `multi-agent-workflow.md`, en la línea 81, hace lo mismo. El propio flujo reserva al «decisor humano» el alcance, las dependencias, la publicación y los conflictos (línea 89).
- **Commits con la identidad Git «Coronacion Meza Fredy»:** son 6, del 20/10/2026, y solo están en `origin/codex/mejoras-sonarqube`. Git declara la identidad, no la autentica. No se reinterpretan ni se atribuyen sin una declaración de las personas implicadas (E-05).

## 8. Decisiones y evidencias pendientes

| ID | Tipo | Qué | De quién | Estado |
|---|---|---|---|---|
| E-01 | Evidencia | Informe completo de la auditoría de Q | Codex | **Disponible** fuera del repositorio (SHA-256 `a1dbc1d2…`); su correspondencia, en la respuesta a la auditoría |
| E-02 | Evidencia | Declaración fechada de Luis sobre la composición y los roles reales (R-01 de Q2), que aclare también la discrepancia con las declaraciones del 27/10/2026 | Luis | Pendiente. Hay declaraciones recibidas del 28/10/2026 y del 29/10/2026 [R] |
| E-03 | Evidencia | Los actos de conformidad de los tres integrantes con una misma versión fijada de Q2 (CM-01 a CM-03) y, por separado, las delegaciones de Fredy y de Anthony (DF-02 y DF-03), o su negativa | Cada integrante, por su cuenta | Pendiente |
| E-04 | Evidencia | Revisión técnica diferenciada del paquete | Una sesión de Codex separada | Entregada sobre `729babb`, con CORRECCIONES REQUERIDAS; pendiente sobre el candidato corregido |
| RR | Registro | Registro raíz de adopción de una versión fijada de Q2 (Q2 §9) | Se crearía en un incremento posterior, tras los actos de E-03 | No existe |
| E-05 | Evidencia | Autoría de los 6 commits con la identidad «Coronacion Meza Fredy» | Las personas implicadas | Pendiente |
| D-01 a D-09 | Decisión | Las de la matriz de H y Q: candidato, D-02, deuda, uso de AF6, alcance de F37-SBX, sincronización, integración y modelo de gobierno | El equipo, según el modelo vigente | No emitidas |
| T-01 a T-07 | Decisión | Diseño del sucesor B-01 | Ídem | No emitidas |
| F36-M01 a F36-M03 | Decisión | Numeración, EI-09 y ADR sucesor | Ídem | Abiertas |
| D-10 [P] | Decisión | Determinación documental del supuesto de §7 del charter tras SEG, con efecto solo prospectivo para cualquier aclaración (§3.3) | El equipo | Nueva |
| D-11 [P] | Decisión | Autoridad y representación para las operaciones del contrato 10, hacia adelante (§5.6) | Los tres integrantes | Nueva |
| Q2 | Decisión | Adopción de la propuesta sucesora de Q, por su procedimiento | Ídem | No emitida |
| Decisiones 12 y 13 | Decisión | Promover RF-28, RF-29 y RNF-C al baseline ([scope](../../../v1.1/scope-preliminary.md)) | El equipo | Pendientes |
