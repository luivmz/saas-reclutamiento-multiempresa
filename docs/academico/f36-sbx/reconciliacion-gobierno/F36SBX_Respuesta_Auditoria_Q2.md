# F36-SBX — Respuesta a la auditoría documental de Q2

> Documento del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`. Responde a la revisión diferenciada de Codex sobre el candidato `729babb4a5584a4bc119fe61e59c101147e7acd5`, con árbol `1a3bba9b073f58145ab879af4bd96df8fefe869b` y base `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9`.
>
> **No cierra ningún hallazgo.** Describe las correcciones implementadas en el candidato nuevo, que siguen pendientes de revisión. No adopta Q2, no emite conformidades humanas y no cambia ningún estado: F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.

## 1. Informes revisados [H]

| Informe | Veredicto | SHA-256 del informe | Manifiesto |
|---|---|---|---|
| Auditoría documental de Q2 sobre `729babb` | CORRECCIONES REQUERIDAS: 0 BLOCKER, 0 HIGH, 5 MEDIUM, 2 LOW y 0 INFO | `24aa7b0ea4e8c8d8c27f3b5ec67cddea356f6cb69dbeb45db907b90c4fbf1ce2` | Figura en el `SHA256SUMS.txt` de su carpeta, cuyo SHA-256 es `71c9bbd0490fd4e8d06f093807fad99e56a371bfdbb884f0fd3dce06c5bff351` |
| Auditoría histórica de Q sobre `061ba68` | APROBADA CON CORRECCIONES DOCUMENTALES PENDIENTES: 0 BLOCKER, 0 HIGH, 5 MEDIUM, 2 LOW y 2 INFO | `a1dbc1d2b3951fbeb83284925ee961987dcafcab2c93c3d8af5cfad1b350a0ab`, igual al comunicado | Figura en el `SHA256SUMS.txt` de su carpeta, cuyo SHA-256 es `69e773b8bb239d66bb6ff17f696be118b1bde1e0263ba7d653ee1d1d7436e767` |

Los dos informes están fuera del repositorio, en `C:/Users/Vila/.codex/visualizations/2026/10/27/01a17ebf-75df-7883-a55e-3ede1b24ee18/`:

- el de Q2, en `F36-Q2-Documental-Audit-729babb/Informe_Auditoria_Documental_Q2_729babb.md`;
- el de Q, en `F36-Unipersonal-Audit-061ba68/Informe_Auditoria_Unipersonal_061ba68.md`.

Se conservan donde Codex los dejó, junto con su evidencia: no se copian al repositorio ni se modifican.

## 2. Matriz de respuesta a Q2-M01 a Q2-L02

| Hallazgo | Corrección implementada | Ubicación | Evidencia | Estado de revisión |
|---|---|---|---|---|
| **Q2-M01**, MEDIUM: se negaba la instrucción académica de formar equipos de tres estudiantes | Se reconoce la instrucción de las nueve guías, con su texto y sus SHA-256. «No acreditadas» se limita a lo que de verdad no se encontró. Se distinguen la composición académica, el quórum interno y las decisiones técnicas ordinarias, y no se exige consulta docente para operaciones ordinarias | Reconciliación §5.1, §5.1.1, §5.2 y §5.4; Q2 §1, §2 y §6 | Los blobs de las nueve guías en `9dd76c4`, con SHA-256 verificados en esta sesión; el inventario oficial; la evidencia de Codex (`official-guides.json`) | Implementada; pendiente de revisión diferenciada |
| **Q2-M02**, MEDIUM: la entrada en vigor no resolvía la conformidad parcial ni fijaba una misma versión | Se adopta una versión exacta V, fijada por commit y árbol, mediante un registro raíz futuro (RR). La conformidad (CM) y la delegación (DF) son actos separados. Hay reglas para versiones distintas, condiciones, conformidad parcial, negativa, silencio, delegación nula o parcial y revocación. Los RD con facultades delegadas citan el RR y las DF vigentes, y no hay referencia circular | Q2 §7, §9 y §13; esta respuesta, §4 | La tabla de escenarios (§4) | Implementada; pendiente |
| **Q2-M03**, MEDIUM: los permisos de hoy se fundaban en N1 y N2, y la autoridad Git quedaba sin resolver | Se separa la fuente vigente de la clasificación propuesta, y N1 a N5 se declaran no vigentes. D-11, prospectiva, distingue la autorización operativa de Luis de la representación documentada del equipo. No se invalida SEG ni se fabrican votos | Reconciliación §5.6 y §6; Q2 §3 y §4; roadmap §4 y §5 | El contrato 10 de `CLAUDE.md` y los mensajes y documentos de SEG | Implementada; pendiente |
| **Q2-M04**, MEDIUM: se extendían condiciones de la estrategia H a todo mantenimiento | D-02b se limita al sucesor que habilita la transición a SUPERADO. Las correcciones independientes del validador van por su propio incremento, y D-05 y D-07 solo valen dentro de la estrategia H. GOV se describe como una comprobación de invariantes. Esta aclaración no autoriza implementar B-01 | Reconciliación §4.2 y §6; Q2 §12; roadmap §5 (R4) | Charter §1, gate §9 y `rule_gov()` | Implementada; pendiente |
| **Q2-M05**, MEDIUM: D-10 mezclaba efecto, registro y enmienda | Reconciliación §3.3 separa cinco cosas: ámbito y periodo, hecho, efecto condicional, registro declarativo y enmienda prospectiva. D-10 pasa a ser una determinación documental, y `revocation = null` y FRZ no deciden por sí solos. No se revierte SEG, no se cambia el JSON y no se emite ninguna revocación ni autorización | Reconciliación §3.2, §3.3 y §6; roadmap §5 (R0 y R5) | Charter §1 y §7, gate §5 y las fechas Git de SEG | Implementada; pendiente |
| **Q2-L01**, LOW: los resultados del validador eran imprecisos | Una tabla por comprobación para AF5, Q, `develop` y Q2 original. Hay una comprobación adicional fallida por el anclaje de rama, sin rutas externas ni fallas de contenido nuevas. Se distinguen las 18 rutas externas de las 11 entradas del chequeo de runtime (5 de `app/` y 6 de pruebas), y se explica la divergencia de FG-01 y FG-05 | Reconciliación §3.1; README | Ejecuciones del validador, en esta sesión y en la auditoría | Implementada; pendiente |
| **Q2-L02**, LOW: se confundía entrenar con abrir un experimento nuevo | Se separan cinco actividades de ML-01. La reconstrucción desde el *freeze* aprobado, con `build_artifact`, no abre un experimento nuevo. Se corrige la línea que atribuía la regeneración al experimento de 15B | Roadmap §2, §5 (R1b) y §7 | `ml-service/README.md`, sección 15C | Implementada; pendiente |

## 3. Informe histórico de Q: correspondencia con este candidato

El informe íntegro de Q ya está disponible (§1). La versión `729babb` lo describía como no disponible porque su búsqueda fue acotada (reconciliación §4.1); eso se conserva como hecho histórico, no como estado actual.

Q se emitió bajo declaraciones humanas distintas de las vigentes, así que sus hallazgos se contrastan con el contexto actual de tres integrantes. **Ninguno se cierra formalmente por sustituir Q:** Q no se modifica.

| Hallazgo de Q | Severidad | Resumen | Tratamiento en este candidato | Estado |
|---|---|---|---|---|
| UNI-M01 | MEDIUM | U-01 seguía abierta y la inferencia histórica excedía la evidencia | Q2 §1 registra las declaraciones del 27/10/2026 y las del 28 y 29/10/2026 como una discrepancia que debe aclarar R-01, sin reinterpretar la historia. R-01 sigue PENDIENTE | Implementado en Q2; pendiente de revisión; no cerrado |
| UNI-M02 | MEDIUM | Se omitía la instrucción de formar equipos de tres estudiantes | Q2-M01 | Ídem |
| UNI-M03 | MEDIUM | Faltaba el vínculo obligatorio con la autoridad que adopta | Q2 §7 y §9: un RR anclado a la versión y al informe, y los RD con facultades delegadas citan el RR y las DF. El docente solo interviene si una fuente lo exige | Ídem |
| UNI-M04 | MEDIUM | El registro de D-02b se confundía con el de H | Q2 §8: D-02b se ancla a la especificación S auditada y al RR; FG-03, FG-10 y FG-12, a H y a su FG-02 | Implementado en Q2. El borrador D-02 de `1d5d6aa` no se modifica (delta en Q2 §12) |
| UNI-M05 | MEDIUM | D-02c era circular | Q2 §8 fija el orden: H, FG-02, las decisiones de FG-03 y siguientes, la validación y, solo con SUPERADO, el inicio efectivo | Ídem |
| UNI-L01 | LOW | D-02 presentaba como exigencia un quórum que solo estaba propuesto | Q2 §4 y §8: el contrato no fija quórum para D-02 ni para cada operación Git. El 3/3 es una práctica, y la conformidad de los tres para adoptar Q2 es una elección de Q2 | Implementado en Q2; pendiente |
| UNI-L02 | LOW | T-08 no se había propagado al plan ni a la especificación | Q2 §12: propagar T-08 y las variantes al integrar la preparación (D-08). No implementado | Delta propuesto; pendiente |
| UNI-I01 | INFO | Los artefactos prueban declaraciones, no personas | Se conserva el límite: Q2 §7 (RA) y §11 | Sin cambio |
| UNI-I02 | INFO | Los resultados reproducidos no aprueban el gate | Se conserva: reconciliación §3.1 y README | Sin cambio |

## 4. Evaluación documental de los escenarios de adopción

Se aplican las reglas de Q2 §9.3 a §9.6 a casos **hipotéticos**: hoy no existe ningún acto. «N3 `develop`» y «N3 `main`» son ejemplos de facultades.

| # | Escenario | Regla aplicada | Resultado | Facultades de Luis después |
|---|---|---|---|---|
| 1 | Los tres son conformes con la misma V, y Fredy y Anthony delegan la misma lista (N3 `develop` y N3 `main`) | 9.3 se cumple; en 9.4, la intersección es esa lista | ADOPTADA | N1 y N2, y N3 para `develop` y `main`, citando el RR y las DF |
| 2 | Fredy es conforme con V1 (commit A) y Anthony con V2 (commit B) | 9.3.1 no se cumple | NO ADOPTADA | Las de hoy |
| 3 | Anthony da una conformidad con condiciones que exigen cambiar §8 de V | 9.3.2: una condición que exige cambiar V no se cumple sobre V | NO ADOPTADA. Hace falta V′, con su revisión y actos nuevos | Las de hoy |
| 4 | Fredy no es conforme | 9.3: no hay tres conformidades | NO ADOPTADA | Las de hoy |
| 5 | Anthony no responde | 9.3: el silencio no cuenta | NO ADOPTADA | Las de hoy |
| 6 | Los tres son conformes con V y no hay delegaciones | 9.3 se cumple; en 9.4, la intersección está vacía | ADOPTADA, sin facultades delegadas | N1 y N2. N3 y los criterios del gate siguen en el mecanismo colegiado |
| 7 | Los tres son conformes con V; Fredy delega N3 `develop` y Anthony, N3 `develop` y N3 `main` | En 9.4, la intersección es N3 `develop` | ADOPTADA | N3 solo para `develop` |
| 8 | Anthony revoca su DF después del RR | 9.4: solo cuentan las DF vigentes; 9.5 y 9.6: la facultad deja de existir desde la revocación y lo anterior no cambia de calificación | Sigue ADOPTADA, sin esa facultad | Los RD anteriores siguen valiendo |

Ninguno de estos casos produce una adopción con versiones distintas, con silencio o con condiciones sin acreditar.

## 5. Cifras corregidas del informe anterior

- **Líneas del candidato.** `729babb` añadía 602 líneas en 4 archivos, no 593. La cifra de 593 se midió antes de completar la tabla de validación del README, que añadió 9 líneas.
- **Fallas del validador.** La frase «no añade ninguna falla» era imprecisa. Lo exacto es que falla una comprobación adicional por el anclaje de rama, sin rutas externas ni fallas de contenido nuevas (reconciliación §3.1).

La validación de este candidato está en el README de esta carpeta.
