# BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN

## Preparación del registro raíz de adopción (RR): estructura y requisitos

> **BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN.** Estructura y lista de requisitos del 31/10/2026. **No es un RR**, no crea ninguno y no declara ningún resultado. Q2 sigue sin adoptar.

## 1. Qué será el RR

Según [Q2 §7 y §9](../reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md#9-adopción-versión-conformidad-delegación-y-entrada-en-vigor):

- se crea en un incremento posterior, solo cuando se cumplen las reglas de §9.3;
- transcribe los actos sin alterarlos;
- su fecha nunca es anterior a la del informe de V ni a la del último acto que cita, y no se retrofecha;
- la adopción rige desde su fecha, solo hacia adelante, y cada delegación desde su propia fecha, si es posterior. Nada anterior cambia de calificación.

## 2. Campos, requisitos y datos disponibles hoy

| Campo | Requisito de Q2 | Dato disponible hoy | Estado |
|---|---|---|---|
| Versión V | Commit y árbol del paquete, y ruta de la propuesta (§7 y §9.1) | Commit `8b1f068b5ac2039139ab5756096c147c11c9fcb2`, árbol `b5b81718680762f9585e4dae969ca44e69114865`. Propuesta: `docs/academico/f36-sbx/reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md`, blob `8d83d17bf94b917d9cb654d6aca6d7dd4ff73d3b`, SHA-256 `8829a0380bf7ea118b24d70c070de791bdf8efe4615a8f6a70372d403c0e71d0` | Identificada |
| Informe aplicable | Una revisión diferenciada favorable sobre el mismo commit, sin BLOCKER, HIGH ni MEDIUM que exija corrección abiertos (§9.1). Ubicación, SHA-256, veredicto y recuentos (§7) | «Revisión final acotada Q2 — residuo Q2-M05», de Codex, del 31/10/2026, sobre `8b1f068b5ac2039139ab5756096c147c11c9fcb2`. Veredicto: APROBADA COMO PROPUESTA DOCUMENTAL. Recuentos: Q2-M05 resuelto, seis correcciones conservadas y cero hallazgos nuevos. Detalle de ubicación y hashes en §3 | Disponible y comprobado el 31/10/2026. Se comprueba de nuevo al crear el RR |
| R-01 | Declaración de Luis sobre la composición y los roles (§9.2), con su hash | — | PENDIENTE |
| CM-01, CM-02 y CM-03 | Las tres citan el mismo commit y el mismo árbol de V, y son «conforme», o «conforme con condiciones» acreditadas como cumplidas (§9.3) | — | PENDIENTE |
| DF-02 y DF-03 | Opcionales. Lista cerrada de facultades, límites, inicio, fin o revocabilidad, canal y evidencia (§7) | — | PENDIENTE, opcionales |
| Condiciones y su cumplimiento | Cada condición, con la evidencia de que se cumplió. Una que exige cambiar V no se cumple sobre V (§9.3) | — | PENDIENTE |
| Facultades delegadas efectivas | La intersección de DF-02 y DF-03 vigentes (§9.4), calculada como indica §5 | — | PENDIENTE |
| Fecha del RR | No anterior al informe (31/10/2026) ni al último acto citado. Sin retrofechar (§7 y §9.3) | — | PENDIENTE |
| Resultado | ADOPTADA solo si se cumplen a la vez las tres reglas de §9.3; si no, NO ADOPTADA | — | PENDIENTE |

## 3. Informe favorable: ubicación y comprobación

El informe está fuera del repositorio, donde Codex lo dejó, y no se copia:

`C:/Users/Vila/.codex/visualizations/2026/10/27/01a17ebf-75df-7883-a55e-3ede1b24ee18/F36-Q2-Final-8b1f068/Informe_Revision_Final_Q2_8b1f068.md`

| Comprobación del 31/10/2026 | Resultado |
|---|---|
| SHA-256 del informe | `a797cd09074688bf983df04230b3eb6b089357315e49ffc9c6fb9f5a550df0d3` |
| Manifiesto `SHA256SUMS.txt` de su carpeta | SHA-256 `df705b39436c17cf87d32cc7819aa9c1f81e86551c3a3b1d0279d0ae318f58dc`. Incluye el informe y sus 44 archivos verifican |
| Commit revisado | `8b1f068b5ac2039139ab5756096c147c11c9fcb2`, con árbol `b5b81718680762f9585e4dae969ca44e69114865` y un solo padre, `e5a750ba4a9d9969fe6ee5f1029365f8845ec842` |
| Alcance del dictamen | Aprobar la propuesta no la adopta, no concede facultades, no emite actos humanos, no autoriza integrar ni publicar y no supera ningún gate |

El manifiesto usa finales de línea CRLF. Para verificarlo hay que quitarlos antes; si no, todas las líneas fallan. Desde esa carpeta, en Git Bash: `tr -d '\r' < SHA256SUMS.txt | sha256sum -c --quiet -`.

## 4. Comprobaciones antes de crear el RR

1. **V.** El commit y el árbol resuelven a los objetos esperados, y el SHA-256 de la propuesta coincide.
2. **Informe.** Su SHA-256 y su manifiesto coinciden, examina exactamente V y su veredicto y sus recuentos son los de §3.
3. **Cada acto.** Lo emitió su titular por su propio canal. El original está conservado tal como llegó, con su fecha y el SHA-256 del archivo conservado ([guía de conservación](F_Textos_para_compartir_y_conservacion.md#5-cómo-conservar-cada-respuesta)).
4. **CM.** Las tres citan `8b1f068b5ac2039139ab5756096c147c11c9fcb2` **y** `b5b81718680762f9585e4dae969ca44e69114865`. Una conformidad con otra versión no cuenta.
5. **Condiciones.** Cada una está acreditada con evidencia. Si alguna exige cambiar V, el resultado sobre V es NO ADOPTADA.
6. **Negativas y silencios.** Una negativa, la falta de respuesta o una conformidad solo con una parte de V dan NO ADOPTADA.
7. **Delegaciones.** Se calcula la intersección (§5). Una facultad que no se puede delegar no pasa aunque alguien la escriba.
8. **Fechas.** La del RR es igual o posterior al 31/10/2026 y al último acto. Ninguna delegación empieza antes que el RR.
9. **Resultado.** Se aplica §9.3. La adopción rige desde la fecha del RR, solo hacia adelante.

## 5. Cómo se calcula la intersección

Una facultad pasa a Luis solo si figura en las dos delegaciones vigentes. Para esa facultad rigen los límites de las dos, y solo durante el periodo en que ambas están vigentes.

Ejemplo inventado para ilustrar la regla; no refleja ninguna decisión:

| Facultad | DF-02 del ejemplo | DF-03 del ejemplo | Pasa a Luis |
|---|---|---|---|
| GIT-1 | Sí | No | No |
| GIT-2 | Sí, hasta el 31/12/2026 | Sí, sin fecha de fin | Sí, hasta el 31/12/2026 |
| B01-1 | Sí, con aviso previo | Sí | Sí, con aviso previo |
| GATE-3 | No | Sí | No |

## 6. Lo que el RR no hará

- No cambia el gate vigente (`gate_version` 3), `CLAUDE.md`, `AGENTS.md`, las skills ni el validador. Los deltas de Q2 §12 los aplican incrementos sucesores auditados (Q2 §9.8).
- No determina D-10 ni autoriza B-01 por sí mismo.
- No autoriza F37-SBX ni supera ningún gate.
- No recalifica nada anterior a su fecha.
