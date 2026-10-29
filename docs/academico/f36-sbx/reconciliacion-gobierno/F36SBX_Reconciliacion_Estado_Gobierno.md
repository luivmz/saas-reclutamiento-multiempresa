# F36-SBX — Reconciliación de referencias, estados y controles tras SEG-01 a SEG-04

> **Informe del 29/10/2026**, en la rama `docs/f36-sbx-team-governance-proposal`, creada desde `develop` = `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9`, árbol `82f27c9daf4305cafce6fb23a3b7b9277906b783`. **Solo documenta.** No cambia ningún estado, contrato, validador, evidencia congelada ni documento de gobierno.
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.

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

[`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py) se ejecutó en solo lectura, con `python -I -B`:

| Árbol validado | Rama | Resultado | Fallas |
|---|---|---|---|
| AF5 `4a2b2d7` (checkout principal) | `feature/f36-sbx-authorization-design` | 59 correctas, 0 fallas; gate NO SUPERADO | — |
| Q `061ba68` (worktree temporal) | `docs/f36-sbx-unipersonal-governance-proposal` | 57 correctas, 2 fallas; gate NO SUPERADO | FRZ, porque la rama no está admitida; GATE, porque FG-01 y FG-05 se recalculan distintos de lo declarado |
| `develop` `9dd76c4` (worktree temporal) | `develop` | 56 correctas, 3 fallas; gate NO SUPERADO | Dos de FRZ: 18 archivos fuera del paquete y 5 de runtime. Una de GATE: FG-01 y FG-05, declarados CUMPLE, se recalculan NO CUMPLE |

Los 18 archivos son los de SEG-01 a SEG-04:

- 5 de runtime: `ApplicationController`, `ApplicationPolicy`, `CandidateDocumentPolicy`, `ApplicationStageService` y `JobRequestWorkflow`;
- `docs/assumptions.md` y `docs/defects.md`;
- 5 documentos de `docs/v1.1/security/`;
- 6 archivos de pruebas.

La matriz de H (§9) registra el mismo 57/2 para AF6 y H por el anclaje de rama [R]; esta sesión no lo repitió sobre esas dos ramas.

### 3.2 Estado por sujeto

| Sujeto | Estado declarado | Fuente | Comprobación [H] |
|---|---|---|---|
| F36-SBX | En diseño. AF5 integrada en `develop` y `main` | [`CLAUDE.md`](../../../../CLAUDE.md), [charter](../F36SBX_Charter.md) y el merge `5545694` | Consistente. `CLAUDE.md` todavía la describe como «candidata a auditoría independiente, sin push, merge, tag ni release» (§7) |
| F36-SBX-GATE | No superado. `candidate_commit`, `f37_authorized_ei` y `revocation` nulos. FG-02, FG-03, FG-10 y FG-12 pendientes; los AUTO, declarados CUMPLE | [`f36sbx_gate_state.json`](../gate/f36sbx_gate_state.json) y [gate](../F36SBX_Gate_Sucesor.md) | En `develop`, FG-01 y FG-05 se recalculan NO CUMPLE (§3.3). El resultado sigue NO SUPERADO porque el validador falla cerrado |
| F37-SBX | Bloqueada | Gate y charter | Consistente |
| B-01 | El validador vigente exige que el gobierno declare NO SUPERADO | Gate §9; especificación en `1d5d6aa` | Presente en el código: `rule_gate()` exige NO SUPERADO y `allowed_states()` solo admite ese resultado. El sucesor está especificado, no implementado. D-02b no está emitida |
| H | El candidato final H no existe. `1d5d6aa` es una rama de preparación | Matriz de H §2.1 | No consta ninguna auditoría de H. Ninguna auditoría de AF5 ni de AF6 vale para H |
| Q | Propuesta no vigente, clase B; U-01 a U-05 pendientes | `061ba68` | Veredicto recibido [R]: «APROBADA CON CORRECCIONES DOCUMENTALES PENDIENTES», con 0 BLOCKER, 0 HIGH, 5 MEDIUM, 2 LOW y 2 INFO. El informe no está disponible (§4.1) |
| D-01 a D-09 | Todas no emitidas. D-01 tiene una instrucción operativa (b), sin decisión formal | Matriz de H §7 y Q §10 | Sin cambios. Ninguna consta emitida en Git |
| ADR-005, G0 real y G0-SBX | Propuesta; no aprobada; aprobada con restricciones, solo para F35-SBX | `CLAUDE.md` y `docs/academico/g0-evidence/` | Sin cambios |

### 3.3 Hallazgo: la regla FRZ en `develop` y la revocación del charter

- **Hechos [H].** La regla FRZ (`validate_f36sbx.py`, `rule_frz`) calcula los cambios desde la base `b8892af` y exige que sean solo del paquete, sus herramientas y el gobierno, con «0 cambios de runtime». SEG-01 a SEG-04 cambiaron runtime en `develop` con autorización expresa de Luis y CI en verde. Por eso FG-01 y FG-05 se recalculan NO CUMPLE en `develop`, y no en la rama de AF5. Ningún documento registra una revocación: `revocation` sigue nulo.
- **Texto en conflicto.** El [charter §7](../F36SBX_Charter.md) revoca F36-SBX si «se modifica una superficie congelada de F35-SBX, el runtime o las dependencias», y exige registrar la revocación «en un incremento nuevo». Los documentos de SEG-01 a SEG-04 ya anticipaban la falla de FRZ «por diseño» y proponían validar anclado en su rama.
- **Dos lecturas posibles.**
  1. La cláusula se refiere a cambios hechos por F36-SBX, que es un incremento documental.
  2. La cláusula se aplica a cualquier cambio de runtime en las ramas admitidas.

  Ningún documento decide entre ellas.
- **Consecuencia.** La situación no habilita nada, porque el gate ya estaba NO SUPERADO. Pero el estado AUTO declarado del paquete y su recálculo en `develop` divergen, y la interpretación de §7 queda abierta.
- **[P] Decisión pendiente D-10.** Elegir, en un incremento sucesor auditado, entre:
  - (a) declarar la lectura 1 y anclar la validación de F36-SBX a su rama, o reajustar la base de FRZ para excluir el mantenimiento de seguridad auditado;
  - (b) registrar la revocación y reabrir F36-SBX con una autorización nueva.

  Mientras tanto, nada se corrige ni se reinterpreta.

## 4. Matriz de observaciones anteriores

### 4.1 Auditoría de Q [R]

Solo están disponibles el veredicto y los conteos, recibidos en la petición del 29/10/2026. El informe completo no está en ninguna rama del repositorio (búsqueda en todas las referencias locales y remotas). Tampoco está en las carpetas del proyecto ni en el directorio personal de WSL, donde se buscó en solo lectura.

| Hallazgo | Severidad | Documento afectado | Corrección propuesta | Evidencia necesaria | Estado |
|---|---|---|---|---|---|
| 5 hallazgos | MEDIUM | No disponible | No se propone sin conocer el hallazgo | El informe de Codex sobre `061ba68`, con su manifiesto SHA-256 | **DESCONOCIDO** |
| 2 hallazgos | LOW | No disponible | Ídem | Ídem | **DESCONOCIDO** |
| 2 hallazgos | INFO | No disponible | Ídem | Ídem | **DESCONOCIDO** |

Ninguno se da por resuelto. La propuesta Q2 sustituye la premisa de Q, que era una persona real, pero eso no demuestra que los hallazgos queden sin objeto: hay que contrastarlos uno a uno cuando el informe esté disponible (E-01, §8).

### 4.2 Otras observaciones disponibles [H]

| ID | Severidad | Estado | Dónde consta | Relación con esta reconciliación |
|---|---|---|---|---|
| AF6-L01 y AF6-L02 | LOW | Abiertos: residuos de la guardia de identidad (vocabulario de relleno y homógrafos latinos y armenios) | Mensaje del merge `5545694`; `88fd3d2:docs/academico/f36-sbx/F36SBX_Deuda_Tecnica_AF6.md` | Su corrección es D-05 y toca el validador (D-02b) |
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

**No acreditadas.** No hay en el repositorio ningún sílabo, rúbrica ni norma del curso sobre la composición del equipo, el trabajo individual, el uso de IA, la aprobación de decisiones técnicas o la autorización docente de commits. Que no se encontraran no prueba que no existan: quedan **no acreditadas**.

### 5.2 (b) Reglas internas creadas por el proyecto [H]

| Regla | Fuente | Alcance |
|---|---|---|
| Contratos 1 a 10, incluido el 10: «sin push, merge, release ni tag sin autorización explícita del equipo» | `CLAUDE.md` | Todo el repositorio |
| Gobierno para Codex y flujo multiagente, con un solo escritor por rama | [`AGENTS.md`](../../../../AGENTS.md) y [`multi-agent-workflow.md`](../../../v1.1/multi-agent-workflow.md) | Uso de herramientas |
| Skills del proyecto, por ejemplo `project-guardian` | `.claude/skills/` | Procedimiento de cambio |
| Aprobación de ADR-005 por los tres integrantes | [`F34A_Paquete_Aprobacion_ADR005.md`](../../g0-readiness/F34A_Paquete_Aprobacion_ADR005.md) (línea 106), cumplida en F34C ([acta](../../g0-evidence/F34B_Acta_Aprobacion_ADR005.md)) | G0-14, ya cumplido |
| G0, G0-SBX, SBX-01 a SBX-18 y los gates de F35-SBX | `docs/academico/g0-*` y `evidencia-sbx-*` | Puertas del ciclo inteligente |
| Charter y gate de F36-SBX, con el quórum 3/3 de §8.1 para FG-03, FG-10 y FG-12 | [Charter](../F36SBX_Charter.md) y [gate](../F36SBX_Gate_Sucesor.md) | Solo el paso de F36-SBX a F37-SBX |

El quórum 3/3 reproduce el patrón de F34A y F34C. Es interno: ninguna fuente del curso lo impone.

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
| Reconocimiento docente de un cambio de gobierno | Q lo recomendaba en su lectura (a) y lo exigía en la (b). **Ninguna fuente lo exige** para la lectura (a) |

### 5.5 Cómo se modifican las reglas internas, de forma prospectiva

- **El gate y el validador** cambian mediante «un incremento sucesor auditado que actualice el gobierno y el validador» (gate §9).
- **El gobierno**, según la práctica de F35-SBX-B y Q §3, necesita además la autorización explícita del equipo; el equipo son los tres integrantes declarados.
- **Lo que no cambia:** ninguna enmienda recalifica lo anterior a su adopción, y los registros congelados (F34C, F35-SBX y AF1 a AF6) no se editan; una aclaración solo puede añadirse como anexo fechado.

### 5.6 Brecha: qué significa «equipo» en el contrato 10 [H]

El contrato 10 exige una «autorización explícita del equipo» y no fija quórum. Las integraciones y publicaciones de SEG-01 a SEG-04 se hicieron con la autorización expresa de Luis, registrada en sus mensajes de commit y documentos. Así quedan: **como autorizaciones de Luis, no como aprobaciones 3/3.**

**[P] Decisión pendiente D-11:** definir quién autoriza `push`, `merge`, tags y releases. La propuesta Q2 plantea formalizar esa autoridad en el responsable técnico, con la conformidad expresa de los otros dos integrantes.

## 6. H, B-01 y actividades permitidas

| Actividad | Requisito aplicable | Evidencia disponible | Bloqueo específico | Trabajo permitido mientras tanto | Condición objetiva para continuar |
|---|---|---|---|---|---|
| Desarrollo técnico ordinario del SaaS: defectos, seguridad, refactors y pruebas | Contratos 1 a 10, `project-guardian` y `laravel-saas-quality` | SEG-01 a SEG-04, con RED/GREEN, auditoría y CI | **Ninguno del gate**, que solo decide F37-SBX. Cada cambio de runtime mantiene la falla de FRZ en `develop` (§3.3) | Todo, en ramas `fix/*` o `feature/*` | El flujo normal. La integración y la publicación necesitan una autorización explícita por operación (D-11) |
| Integrar y publicar `develop`, `main`, tags y releases | Contrato 10 | Práctica de SEG: autorización de Luis | La autoridad no está definida (D-11) | Preparar candidatos y auditorías | Autorización explícita por operación; D-11 si se adopta Q2 |
| Mantener la documentación del paquete F36-SBX | Charter: investigar y diseñar | AF6, H y Q en local | Integrarlos exige D-08 | Preparar documentos en ramas propias, sin integrar | D-08 |
| Implementar el sucesor B-01 | Gate §9 y D-02b | Especificación y plan de pruebas (`1d5d6aa`) | D-02b no está emitida; con el contrato vigente, la autoriza el equipo | Afinar la especificación y auditarla como documentación (D-02a) | D-02b auténtica, bajo el modelo vigente en ese momento |
| Corregir AF6-L01 y AF6-L02 | D-05 y D-02b (es código del validador) | Registro de deuda AF6 | D-05 no está emitida | Analizar | D-05 y D-02b |
| Sincronizar `CLAUDE.md`, `PROGRESS.md`, `README.md` y `ACADEMIC_BASELINE.md` | D-07; regla GOV | Deuda inventariada (§7) | D-07 no está emitida, y los documentos están protegidos por GOV | Proponer deltas, como hace este paquete | D-07 dentro de H |
| Resolver FRZ en `develop` y §7 del charter | Charter §7 y FG-05 | Medición 56/3 | D-10 | Validar sobre la rama ancla | D-10 en un sucesor auditado |
| Fijar el candidato H | Matriz de H §2.1 | — | Faltan D-01 formal, D-02b, D-05, D-06 y D-07, y cerrar los cambios materiales | No | Todos los cambios materiales hechos |
| FG-02, auditoría de H | Gate §8.2 y §8.6 | Ninguna: AF6 no sirve para H | H no existe | No | H fijado |
| FG-03, FG-10 y FG-12 | Gate §8.1, 3/3 | Ninguna | Hacen falta los votos reales de los tres integrantes, o una enmienda adoptada, y una FG-02 favorable | Solo borradores de formato | Actos auténticos de cada integrante |
| Iniciar F37-SBX (A o B) | Gate superado | — | F36-SBX-GATE = NO SUPERADO | Nada de EI | El gate superado con el sucesor B-01 |

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
| E-01 | Evidencia | Informe completo de la auditoría de Q, con su manifiesto SHA-256 | Quien lo conserve | No disponible |
| E-02 | Evidencia | Declaración fechada de Luis sobre la composición y los roles reales (R-01 de Q2) | Luis | Pendiente; hay declaraciones recibidas del 28/10/2026 y del 29/10/2026 [R] |
| E-03 | Evidencia | Conformidad expresa y fechada de Fredy y de Anthony, cada uno por su cuenta, o su negativa | Fredy y Anthony | Pendiente |
| E-04 | Evidencia | Auditoría técnica independiente de este paquete | Una sesión de Codex separada | Pendiente |
| E-05 | Evidencia | Autoría de los 6 commits con la identidad «Coronacion Meza Fredy» | Las personas implicadas | Pendiente |
| D-01 a D-09 | Decisión | Las de la matriz de H y Q: candidato, D-02, deuda, uso de AF6, alcance de F37-SBX, sincronización, integración y modelo de gobierno | El equipo, según el modelo vigente | No emitidas |
| T-01 a T-07 | Decisión | Diseño del sucesor B-01 | Ídem | No emitidas |
| F36-M01 a F36-M03 | Decisión | Numeración, EI-09 y ADR sucesor | Ídem | Abiertas |
| D-10 [P] | Decisión | Interpretación de la regla FRZ y de §7 del charter tras SEG (§3.3) | Ídem | Nueva |
| D-11 [P] | Decisión | Quién autoriza `push`, `merge`, tags y releases (§5.6) | Los tres integrantes, al adoptar Q2 | Nueva |
| Q2 | Decisión | Adopción de la propuesta sucesora de Q, por su procedimiento | Ídem | No emitida |
| Decisiones 12 y 13 | Decisión | Promover RF-28, RF-29 y RNF-C al baseline ([scope](../../../v1.1/scope-preliminary.md)) | El equipo | Pendientes |
