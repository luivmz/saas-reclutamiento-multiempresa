# BORRADOR — PENDIENTE DE DECISIÓN

## D-10 · Vigencia del charter de F36-SBX tras SEG-01 a SEG-04

> **BORRADOR — PENDIENTE DE DECISIÓN.** Preparado el 07/11/2026 por una sesión de Claude Code a pedido de Luis Vila Meza, fuera de Git. No es un acto de ningún integrante, no determina nada y no registra una revocación ni una autorización. Ningún estado cambia: F36-SBX = EN DISEÑO, F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA, alcance C = BLOQUEADO, datos reales = PROHIBIDOS.
>
> **Referencia de adopción:** RR-001, commit `5036393f11b30855d3b3b28154e2d6a4f94c0bd5` (árbol `214ce447e8f46e8582de5b39c38b55ce3aa29f82`), que adopta Q2 en la versión V `8b1f068b5ac2039139ab5756096c147c11c9fcb2` (árbol `b5b81718680762f9585e4dae969ca44e69114865`) con fecha efectiva 07/11/2026 12:41:15 −05:00. RR-001 §5 deja D-10 para su propia decisión. Adoptar Q2 no resuelve D-10.

Marcas: **[H]** hecho verificado en esta sesión con Git o con los registros citados; **[R]** medición o afirmación tomada de un documento, no repetida aquí; **[P]** propuesta.

---

## 1. Pregunta que hay que resolver

¿Los cambios de runtime de SEG-01 a SEG-04 en `develop` constituyen el supuesto del charter §7 («se modifica […] el runtime […]») que revoca F36-SBX y su gate? Si es así, ¿desde cuándo y con qué efecto? En cualquier caso, ¿qué se registra y qué autorización o enmienda, solo hacia adelante, conviene emitir?

D-10 no consiste en elegir qué pasó. Los hechos están fijados (§3 y §4). Hay que **determinar con fundamentos** el ámbito de la cláusula y si el supuesto se produjo. Después se **registra** el resultado de forma declarativa y, por separado, se decide si hace falta **una autorización o una enmienda con efecto hacia adelante**.

## 2. Fuentes

| ID | Fuente | Qué aporta |
|---|---|---|
| F1 | `5036393:docs/academico/f36-sbx/F36SBX_Charter.md` §1, §2 y §7 | Qué autoriza el charter y la cláusula de revocación |
| F2 | `5036393:docs/academico/f36-sbx/F36SBX_Gate_Sucesor.md` §2, §3 (FG-05 y FG-14), §4 y §5 | Estado REVOCADO, cómo se registra y criterios AUTO |
| F3 | `5036393:docs/academico/f36-sbx/gate/f36sbx_gate_state.json` | `revocation = null`, `declared_result = "NO SUPERADO"`, base `b8892af` |
| F4 | `5036393:docs/academico/tools/f36sbx/validate_f36sbx.py`, `rule_frz` (l. 2144–2177), `RUNTIME_PREFIXES`, `DEPENDENCY_FILES` y `F35_FROZEN` (l. 356–362), `allowed_states` (l. 1283–1300) y decisión del gate (l. 2723–2877) | Lo que mide FRZ y los estados que admite el validador v3 |
| F5 | `4a2b2d7:docs/academico/f36-sbx/README.md`, l. 49, «Anclaje». Introducida en `06e933e` el 26/10/2026 11:59:28 −05:00 | Lo que el paquete previó, antes de SEG, para cambios ajenos posteriores en `develop` o `main` |
| F6 | `5036393:docs/academico/f36-sbx/reconciliacion-gobierno/F36SBX_Reconciliacion_Estado_Gobierno.md` §3.1, §3.3 y §8 | Mediciones del validador y planteamiento de D-10 en cinco puntos |
| F7 | `5036393:docs/academico/f36-sbx/reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md` (V) §4, §9.5 y §11 | Niveles de decisión, entrada en vigor y evidencias que no se reinterpretan |
| F8 | `5036393:docs/academico/f36-sbx/adopcion-q2/RR-001_Adopcion_Q2.md` §4 y §5 | Facultades delegadas utilizables: ninguna. D-10 sigue pendiente |
| F9 | `5036393:docs/academico/f36-sbx/adopcion-q2/G_Continuidad.md` §2 | Formulación de D-10 que revisó Codex |
| F10 | `git log` y `git diff 5545694..9dd76c4` | Cronología y archivos de SEG |
| F11 | `9dd76c4:docs/v1.1/security/SEG-01…SEG-04` y `SEG-01-02-integracion-local.md` | Alcance de cada SEG y lo que declararon sobre FRZ |
| F12 | Transcripciones locales de Claude Code, fuera de Git: `0be29a7a-19c6-41d8-b61d-0054731cdcf7.jsonl` (SHA-256 `f4d5e16e…81eb45b`) y `b1f82d09-0c4a-4c13-8c4c-52abeed8701f.jsonl` (SHA-256 `893a3402…82229c0`), en `C:/Users/Vila/.claude/projects/D--Universidad-…-multiempresa/` | Momento y texto de las autorizaciones operativas de SEG |

## 3. Cronología verificada [H]

Horas en America/Lima (−05:00). Los commits llevan su fecha de autor. Las autorizaciones proceden de F12, con las horas UTC del registro convertidas.

| Fecha y hora | Hecho | Referencia |
|---|---|---|
| 26/10/2026 | Se abre F36-SBX desde `main` = `b8892af` por instrucción del equipo, transcrita por la sesión y sin adjunto firmado | F1 §1 |
| 26/10/2026 11:59:28 | El README del paquete añade la regla de «Anclaje»: con cambios ajenos a F36-SBX en `develop` o `main`, FRZ falla por diseño y se valida anclado en la rama | `06e933e`, F5 |
| 27/10/2026 17:30:45 | AF5 queda fijado | `4a2b2d7` |
| 27/10/2026 19:56:43 y 19:58:23 | AF5 se integra en `develop` y en `main` | `5545694` y `55f758e`. El árbol de `55f758e` es `01dc59a`, el mismo que el de AF5 |
| 27/10/2026 20:12–21:42 | AF6, H preliminar y Q, en ramas locales | `20527db`…`88fd3d2`, `a5a8166`…`1d5d6aa`, `d5c59d9`…`061ba68` |
| 28/10/2026 11:09:23 | Primer cambio de runtime de SEG (SEG-01), en la rama `fix/seg-01-internal-application-authorization`, sin integrar | `e1f1f1a` |
| 28/10/2026 14:51:30 | SEG-02, en su rama `fix/*` | `4c89a95` |
| 28/10/2026 ≈19:05 | Luis autoriza la integración local de SEG-01 y SEG-02 en una rama de integración | F12, sesión `0be29a7a`; `SEG-01-02-integracion-local.md` §1 |
| 28/10/2026 19:07–19:23 | Merges en `fix/seg-01-02-integration` y documento de integración | `b69c6c3`, `f5b7c59` y `4dd1bac` |
| 28/10/2026 ≈21:03 | Luis autoriza el merge local en `develop` | F12, sesión `0be29a7a` |
| **28/10/2026 21:05:26** | **El runtime cambia por primera vez en `develop`** | **`2e53786`** (padres `5545694` y `4dd1bac`) |
| 28/10/2026 ≈21:09 | Luis autoriza el push de `develop` | F12, sesión `0be29a7a` |
| 28/10/2026, antes de las 21:10:46 | `develop` se publica en `2e53786`. CI `tests`, ejecución 40804808195, `success` | F12 |
| 28/10/2026 21:34:07 | SEG-03, en su rama `fix/*` | `afa6282` |
| 29/10/2026 ≈09:39 | Luis autoriza el merge local de SEG-03 | F12, sesión `b1f82d09` |
| 29/10/2026 09:44:31 | Merge de SEG-03 en `develop` | `2546297` |
| 29/10/2026 10:45:22 | Luis responde «Sí, Luis autoriza el push» | F12, sesión `b1f82d09` |
| 29/10/2026 10:45:49 | Push `2e53786..2546297`. CI 40904841417, `success` | F12 |
| 29/10/2026 11:24:42 | SEG-04, en su rama `fix/*` | `74bcdf5` |
| 29/10/2026 12:36:02 | Luis autoriza el merge, el push exclusivo de `develop` y la verificación de su CI | F12, sesión `b1f82d09` |
| 29/10/2026 12:37:10 | Merge de SEG-04 en `develop`, después publicado. CI 40923175235, `success` | `9dd76c4` |
| 29/10/2026 13:16 | La reconciliación identifica D-10 | `d32873b`, F6 §3.3 |
| 31/10/2026 10:47:41 | Versión V de Q2 | `8b1f068` |
| 07/11/2026 12:41:15 | RR-001 registra la adopción de Q2 y deja D-10 pendiente | `5036393` |

`main` no recibió nada de SEG y sigue en `55f758e` [H].

## 4. Ámbito y cambios concretos de SEG [H]

`git diff --stat 5545694 9dd76c4`: 18 archivos, 2776 inserciones y 20 eliminaciones.

| Grupo | Archivos | SEG y commit | Cambio |
|---|---|---|---|
| Runtime funcional, en `app/` (5) | `Http/Controllers/Applications/ApplicationController.php` y `Policies/ApplicationPolicy.php` | SEG-01, `e1f1f1a` | El expediente interno se autoriza con `viewFile`, que lo restringe a RR. HH. y Aprobadores de la organización (DEF-14) |
| | `Services/Applications/ApplicationStageService.php` | SEG-02, `4c89a95`; SEG-04, `74bcdf5` | Los cambios manuales de etapa se serializan con la decisión final, mediante un bloqueo de la vacante (DEF-15). Además, el comentario libre ya no se copia a los metadatos de auditoría (DEF-17) |
| | `Policies/CandidateDocumentPolicy.php` | SEG-03, `afa6282` | La descarga del CV se liga al documento presentado en una postulación autorizada (DEF-16, A-37) |
| | `Services/JobRequests/JobRequestWorkflow.php` | SEG-04, `74bcdf5` | Metadatos de auditoría reducidos a `from` y `to` (DEF-17, A-38) |
| Pruebas (6) | En `tests/Feature/`: pruebas de autorización del expediente y del CV, de concurrencia (con su *worker*) y de minimización de auditoría | SEG-01 a SEG-04 | Pruebas RED/GREEN. El validador las cuenta como runtime, porque `RUNTIME_PREFIXES` incluye `tests/` |
| Documentación (7) | `docs/assumptions.md`, `docs/defects.md` y 5 documentos de `docs/v1.1/security/` | SEG-01 a SEG-04 | DEF-14 a DEF-17, A-37 y A-38, y la evidencia de cada SEG |
| Archivos de dependencias | **0** de `DEPENDENCY_FILES` | — | — |
| Superficies congeladas de F35-SBX, G0 y antecedentes | **0** de `F35_FROZEN` | — | — |
| Paquete y herramientas de F36-SBX | **0** en `docs/academico/f36-sbx/` y `docs/academico/tools/f36sbx/` | — | — |

Del charter §7, solo puede estar en juego la tercera viñeta, y solo en su parte «el runtime». No hay datos reales, ni nada que la sección 4 prohíba, ni cambios de F35-SBX o de dependencias, ni una retirada de la autorización por el equipo.

## 5. Las cinco cosas que hay que distinguir

### 5.1 Resultado registrado del gate [H], [R]

- **Lo registrado.** El estado registrado es `declared_result = "NO SUPERADO"` y `revocation = null`, y FG-14 está declarado CUMPLE (F3).
- **Lo que mide FG-14.** Que no haya ningún evento de revocación **registrado**. No interpreta el supuesto material (F6 §3.1).
- **Mediciones [R].** Son de F6 §3.1 y no se repitieron en esta sesión:
  - AF5 anclado en su rama: 59/0;
  - `develop` `9dd76c4`: 56/3, con las dos comprobaciones de contenido de FRZ en falla (18 rutas externas y 11 entradas de runtime), y FG-01 y FG-05 recalculados NO CUMPLE.
- **Lo que FRZ no decide.** FRZ mide un perímetro técnico frente a `b8892af` en la rama validada. Su falla en `develop` es un indicio del hecho, no la determinación de D-10.

### 5.2 El supuesto material: dos lecturas

**Lectura A, literal amplia.** Cualquier modificación del runtime del repositorio posterior al charter revoca F36-SBX.

**Lectura B, sistemática.** La tercera viñeta se refiere a modificaciones hechas por F36-SBX o dentro de ella, en su rama, su paquete o su incremento. El mantenimiento del SaaS en incrementos propios queda fuera.

| Elemento | Favorece | Peso y límite |
|---|---|---|
| El texto de §7, tercera viñeta, no tiene sujeto y no excepciona el mantenimiento | A | Es el argumento más fuerte de A. Las viñetas 1 y 2 dicen «en cualquier artefacto F36-SBX» y «un artefacto F36-SBX»; la 3 no lo dice. Eso puede leerse como amplitud deliberada (A) o como elipsis del mismo sujeto (B) |
| FG-05, «el runtime y las dependencias no cambian desde la base», medido en la rama que se valida | A, débil | Describe una comprobación técnica, no el ámbito material de la autorización |
| Charter §1: autoriza solo investigar y diseñar, y «no autoriza» endpoints, migraciones, UI ni dependencias | B | La cláusula protege los límites de lo que F36-SBX puede hacer |
| Charter §2, fila de F35-SBX: «F36-SBX no toca ninguna de sus superficies» | B | El sujeto de las restricciones es F36-SBX |
| README, «Anclaje» (F5): escrito el 26/10, antes de SEG, y parte del paquete auditado hasta AF5 | B, el elemento más fuerte de B | Prevé expresamente «cambios ajenos a F36-SBX» en `develop` o `main` y les asigna una consecuencia: FRZ falla por diseño y se valida anclado. No menciona la revocación. **Límite:** habla de FRZ, no de §7 |
| Precedente DG-02 de F35-SBX: los gates congelados fallan sobre un HEAD posterior por diseño | B | Práctica del proyecto: un HEAD posterior ajeno no invalida la puerta anterior |
| Documentos SEG (F11): «Un rechazo FRZ […] es esperable por diseño»; «se valida anclado en su rama» | B, débil | Lectura contemporánea de la sesión que implementó SEG, no un acto del equipo |
| Finalidad: el sandbox se protege de su propio desbordamiento hacia producción | B | Con A, cualquier corrección de seguridad del SaaS revocaría el diseño sandbox. Sería un resultado posible pero oneroso, y ningún texto lo justifica |
| F6 §3.3, punto 1: «La cláusula […] no rige el mantenimiento del SaaS ni la validez técnica de SEG» | Neutro | Delimita el efecto (SEG sigue válido con A o con B), no si el supuesto se produjo |

### 5.3 Posible efecto histórico de la cláusula

- **Con la lectura B.** El supuesto no se produjo. F36-SBX siguió autorizada sin interrupción, y las mediciones históricas se conservan tal cual (AF5 59/0; `develop` 56/3).
- **Con la lectura A.** La cláusula prevé un efecto automático: «F36-SBX queda REVOCADA y su gate pasa a REVOCADO», sin otra votación (F6 §3.3, punto 3). Habría que fijar el instante T:
  - **Candidato principal:** 28/10/2026 21:05:26, `2e53786`, el primer cambio de runtime en `develop`, la rama de integración del producto.
  - **Alternativas que el equipo tendría que descartar con fundamentos:** el commit en la rama `fix/*` (`e1f1f1a`, 11:09:23), que no estaba integrado, y la publicación (antes de las 21:10:46).
- **Efectos con la lectura A, si se determina así:**
  - AF5, AF6, H y Q son anteriores a T, así que no les afecta.
  - Q2 y su adopción son actos de gobierno del equipo, con su propio procedimiento (V §9 y RR-001). No dependen de la autorización de F36-SBX y no se deshacen.
  - El trabajo documental de F36-SBX posterior a T no tendría cobertura del charter como trabajo de F36-SBX. Tal como está hoy, eso incluye la reconciliación, el roadmap y la preparación de B-01, si la hubiera. No se borra ni se reescribe: se califica.
  - F37-SBX no podría comenzar por este gate. Haría falta una autorización nueva y un gate sucesor.
  - SEG no se ve afectado en ningún caso.

### 5.4 Registro declarativo

Sea cual sea la determinación, se registra en un incremento nuevo, sin reescribir el charter (F1 §7, F2 §5). El registro documenta el hecho; no lo crea ni lo elimina.

- **Con la lectura B.** Un documento fechado de **determinación de no activación**, con sus fundamentos. `revocation` sigue en `null`, ahora respaldado por una determinación.
- **Con la lectura A.** Un documento fechado de **determinación de activación** con T, el motivo y la evidencia.
  - **Limitación técnica [H]:** el validador v3 solo admite `F36-SBX = EN DISEÑO` y `F36-SBX-GATE = NO SUPERADO` (`allowed_states`, l. 1288–1290), y exige NO SUPERADO en el gobierno (l. 2877). Un `revocation` no nulo calcula REVOCADO (l. 2727–2728), que entraría en conflicto con esas reglas.
  - **Consecuencia:** registrar la revocación en `f36sbx_gate_state.json` y en las líneas de estado de `CLAUDE.md`, `PROGRESS.md`, `README.md` y `ACADEMIC_BASELINE.md` exige antes un incremento sucesor del validador y del gobierno, auditado (N2 de Q2).
  - **Mientras tanto:** el documento fechado deja constancia de la determinación, y el JSON no se altera a mano.

### 5.5 Autorización nueva o enmienda, solo hacia adelante [P]

Son actos distintos de la determinación y nunca la sustituyen:

- **Autorización nueva** (Anexo 2). Hace falta si se determina A y el equipo quiere continuar F36-SBX. También es posible con D-10 abierta, «sin perjuicio» de la determinación, para que el trabajo futuro tenga cobertura cierta. No regulariza nada anterior.
- **Enmienda aclaratoria de §7** (Anexo 3). Es opcional con cualquier resultado. Rige desde su fecha, se añade como anexo fechado y no recalifica lo anterior (F6 §5.5).
- **Un anclaje o una base nuevos** (por ejemplo, un H creado desde `develop` con SEG) no regularizan hechos anteriores.

## 6. Qué respaldan los documentos y qué incertidumbre queda

**Lo que acreditan sin duda [H]:**

- SEG-01 a SEG-04 modificaron cinco archivos de runtime funcional (y seis de pruebas) en `develop` entre el 28/10/2026 21:05:26 y el 29/10/2026 12:37:10, después de abrirse el charter;
- no tocaron dependencias, F35-SBX ni el paquete F36-SBX;
- `main` no cambió;
- no hay ninguna revocación registrada ni una retirada de la autorización.

**Lo que respaldan con peso preponderante, pero no concluyente.** Los elementos sistemáticos favorecen la lectura B, sobre todo la regla de «Anclaje», escrita antes de SEG dentro del mismo paquete auditado, junto con §1, §2, DG-02 y la finalidad. A tiene a su favor el texto literal de §7 y la falta de una excepción escrita.

**Incertidumbre que queda:**

1. No hay constancia de lo que los tres integrantes entendieron por §7 el 26/10: el charter nace de una instrucción transcrita, sin adjunto firmado.
2. La regla de «Anclaje» trata de FRZ, no de §7.
3. Con A, falta fijar T.
4. Con A, falta calificar el trabajo de F36-SBX posterior a T.

Por eso, ni la sesión que prepara ni la que revisa pueden cerrar D-10. Es una determinación del equipo sobre su propio charter. No figura en el catálogo de facultades delegables (GIT-2 a GIT-5, B01-1, GATE-1 y GATE-2) y, sin facultades delegadas utilizables (F8 §4), corresponde al **mecanismo colegiado**: un acto propio de cada integrante.

## 7. Decisión exacta que el equipo tendría que tomar

Cada integrante emite su propio acto, por su canal propio, citando la misma versión fijada de este documento (commit y árbol, cuando se versione tras la revisión de Codex). Mientras D-11 no fije otro procedimiento, tres actos conformes con la misma opción satisfacen cualquier lectura de «del equipo». El silencio no cuenta.

**Decisión principal (elegir una):**

| Opción | Contenido | Qué se registra después |
|---|---|---|
| **D10-1. No activación** | Se determina, con los fundamentos de §5.2, que la tercera viñeta de §7 se refiere a modificaciones hechas por F36-SBX o dentro de ella, y que SEG-01 a SEG-04, incrementos de mantenimiento propios y ajenos al paquete, no constituyen el supuesto | Documento de determinación fechado (Anexo 1, texto A). `revocation` sigue en `null`. Sin cambios de estado |
| **D10-2. Activación** | Se determina que SEG-01 a SEG-04 constituyen el supuesto, con T = 28/10/2026 21:05:26 (`2e53786`) u otro T fundado | Documento de determinación fechado (Anexo 1, texto B). Después, un incremento sucesor auditado del validador y del gobierno para registrar `revocation` y los estados. Si se quiere continuar, una autorización nueva (Anexo 2, variante D10-2) |
| **D10-3. Mantener abierta** | No se determina todavía | Ningún registro nuevo. El estado registrado sigue NO SUPERADO y F37-SBX, BLOQUEADA. La pregunta histórica queda sin respuesta: el registro no dice si el gate siguió vigente o quedó revocado el 28/10. Opcionalmente, una autorización nueva «sin perjuicio» (Anexo 2, variante D10-3) para cubrir el trabajo futuro |

**Qué estado rige con cada opción.** Las tres opciones no producen el mismo estado:

| | D10-1 | D10-2 | D10-3 |
|---|---|---|---|
| Situación del gate según la determinación del equipo | Vigente, NO SUPERADO | **REVOCADO desde T** | Sin determinar |
| Lo que muestra `f36sbx_gate_state.json` (v3) | `revocation = null`, NO SUPERADO; coincide con la determinación | `revocation = null`, NO SUPERADO **hasta el incremento sucesor**. No expresa la determinación: el v3 no puede representar REVOCADO (§5.4) | `revocation = null`, NO SUPERADO |
| F37-SBX | BLOQUEADA hasta superar este gate | BLOQUEADA. Este gate ya no puede superarse: haría falta un gate nuevo o un sucesor | BLOQUEADA |

Con D10-2, mientras no exista el incremento sucesor, lo que rige es la determinación documentada. El JSON v3 queda como un registro técnico desfasado, que se señala en el documento de determinación y no se corrige a mano. Ningún validador ni criterio puede leer en ese `null` que el gate siga vigente.

**Decisión accesoria, independiente:** si se emite la enmienda aclaratoria de §7 (Anexo 3), con efecto desde su fecha.

**Recomendación del preparador.** No vincula a nadie. D10-1 con la enmienda del Anexo 3: es la lectura mejor respaldada, y la enmienda elimina la ambigüedad para el futuro sin tocar el pasado. Si algún integrante no comparte la lectura B, lo coherente es D10-3 con la autorización «sin perjuicio», no forzar D10-1.

## 8. Evidencia que falta

| # | Evidencia | De quién | Necesaria para |
|---|---|---|---|
| 1 | Revisión diferenciada de Codex sobre la versión fijada de este borrador | Sesión de Codex separada | Cualquier opción |
| 2 | Tres actos individuales con la opción elegida, citando esa versión | Luis, Fredy y Anthony, cada uno por su canal | Cualquier opción |
| 3 | Si existe, cualquier constancia del 26/10 sobre lo que el equipo quiso decir en §7 (mensajes o notas), conservada sin alterar | Quien la tenga | Reduce la incertidumbre 1; no es obligatoria |
| 4 | Una nueva ejecución del validador en solo lectura sobre AF5 anclado y sobre `develop` `9dd76c4`, para actualizar las mediciones [R] de §5.1 | Claude Code o Codex | Que la determinación cite mediciones de su fecha |
| 5 | Con D10-2: un incremento sucesor auditado del validador y del gobierno que admita REVOCADO | Luis (N2), con auditoría de Codex | Registrar `revocation` |

---

## Anexo 1. Textos de determinación (plantillas sin emitir)

**Texto A (D10-1).** «Yo, [nombre], respecto de D-10 en la versión [commit]/[árbol], determino que la tercera viñeta del §7 del charter de F36-SBX se refiere a modificaciones de superficies congeladas de F35-SBX, del runtime o de las dependencias realizadas por F36-SBX o dentro de ella, y que SEG-01 a SEG-04 (merges `2e53786`, `2546297` y `9dd76c4` en `develop`), incrementos de mantenimiento de seguridad propios, ajenos al paquete y sin cambios de dependencias ni de F35-SBX, no constituyen ese supuesto. F36-SBX no quedó revocada. Esta determinación no modifica el gate, que sigue NO SUPERADO, ni F37-SBX, que sigue BLOQUEADA.»

**Texto B (D10-2).** «Yo, [nombre], respecto de D-10 en la versión [commit]/[árbol], determino que los cambios de runtime de SEG-01 a SEG-04 constituyen el supuesto de la tercera viñeta del §7 del charter de F36-SBX, producido el [T] con [commit]. Desde ese instante, F36-SBX quedó revocada y su gate en REVOCADO, a registrar en un incremento sucesor del validador y del gobierno. Hasta ese registro, `f36sbx_gate_state.json` seguirá mostrando `revocation = null` y NO SUPERADO, que no expresa esta determinación. El resultado técnico de SEG-01 a SEG-04 no se ve afectado. El trabajo anterior a T conserva su calificación.»

## Anexo 2. Autorización nueva, con efecto solo hacia adelante (plantilla sin emitir)

La autorización cubre **trabajo** futuro. No es un estado del gate ni lo modifica, así que cada variante dice por separado qué pasa con el gate anterior.

**Parte común.**

> «Yo, [nombre], autorizo, desde la fecha de este acto y sin efecto sobre ningún hecho anterior, que el trabajo de F36-SBX continúe como incremento solo documental de autorización, investigación y diseño, con el mismo ámbito y las mismas prohibiciones del charter §1 y §4. No autorizo implementar ML, NLP, embeddings, OCR, parsing, búsqueda semántica ni un LLM, ni endpoints, migraciones, UI, dependencias, datos reales o el inicio de F37-SBX. Esta autorización no supera, no restablece ni sustituye ningún gate.»

**Variante D10-2.**

> «Esta autorización no deja sin efecto la revocación determinada el [fecha], con efecto desde [T]. El F36-SBX-GATE anterior sigue REVOCADO según esa determinación, aunque su JSON v3 muestre NO SUPERADO hasta el incremento sucesor. Si se quiere que F37-SBX pueda comenzar, hará falta un gate nuevo o sucesor, definido y auditado en su propio incremento. F37-SBX sigue BLOQUEADA.»

**Variante D10-3.**

> «Se emite sin perjuicio de la determinación pendiente de D-10, que esta autorización no decide. El estado registrado del gate sigue NO SUPERADO, y F37-SBX, BLOQUEADA. Si D-10 se determina después como activación, el gate anterior quedará REVOCADO desde T, y esta autorización solo seguirá cubriendo el trabajo posterior a su fecha.»

Con D10-1 no hace falta una autorización nueva: la autorización original sigue vigente y el gate, NO SUPERADO.

## Anexo 3. Enmienda aclaratoria de §7, con efecto solo hacia adelante (plantilla sin emitir)

> «Desde [fecha], la tercera viñeta del §7 del charter de F36-SBX se entiende así: "se modifica una superficie congelada de F35-SBX, el runtime o las dependencias por F36-SBX o dentro de ella (su rama, su paquete o su incremento)". El mantenimiento del SaaS en incrementos propios, autorizado y auditado, no la activa. Su efecto sobre el validador se gestiona con el anclaje documentado o con un sucesor auditado. Esta aclaración se añade como anexo fechado, no reescribe el charter y no recalifica nada anterior a su fecha.»
