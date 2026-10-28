# BORRADOR — NO FIRMADO — SIN AUTORIZACIÓN

## Acta de revisión técnica del equipo y registro de decisiones del F36-SBX-GATE

> **BORRADOR — NO FIRMADO — SIN AUTORIZACIÓN.** Plantilla de trabajo del 27/10/2026, preparada para que el equipo la complete en una reunión real. No contiene ninguna decisión, voto, firma, fecha de aprobación ni identidad nueva. No es evidencia de ningún criterio, y no está en `gate/evidencia/` ni puede llevarse allí tal cual: la evidencia válida es un JSON con el formato del [gate §8](../F36SBX_Gate_Sucesor.md#8-formato-de-la-evidencia-de-equipo). Mientras este documento siga siendo un borrador, F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.

Las celdas con `PENDIENTE`, `NO EMITIDA` o `POR DESIGNAR` se completan solo con hechos reales del día de la reunión.

## 1. Datos de la reunión

| Campo | Valor |
|---|---|
| Fecha de la reunión | PENDIENTE |
| Modalidad y canal | PENDIENTE |
| Asistentes | PENDIENTE: los tres integrantes que declara `CLAUDE.md` deben constar uno por uno, con su presencia confirmada |
| Responsable del acta | POR DESIGNAR |
| Candidato del gate examinado | PENDIENTE: depende de la decisión D-01 de la [matriz](F36SBX_Matriz_Preparacion_Gate.md#7-decisiones-que-requieren-intervención-humana) |
| Árbol del candidato | PENDIENTE |
| Validador ejecutado sobre el candidato | PENDIENTE: resultado real, con su salida |

## 2. Revisión técnica

| Punto | Antecedente disponible | Conclusión del equipo |
|---|---|---|
| Sexta auditoría independiente (AF6) | [Registro AF6](../F36SBX_Auditoria_AF6.md): técnicamente favorable para integración, sobre `4a2b2d7` | NO EMITIDA |
| Hallazgos abiertos AF6-L01 y AF6-L02 | [Deuda técnica AF6](../F36SBX_Deuda_Tecnica_AF6.md) | NO EMITIDA (corregir antes, D-05, o registrarlos en `findings_open.low`) |
| Independencia del auditor de FG-02 | Ver matriz §3.1, punto 8 | NO EMITIDA |
| Formato del informe para FG-02 | El informe AF6 no tiene el formato del gate §8.6 (matriz, B-03) | NO EMITIDA |
| Incremento sucesor que permita SUPERADO | Matriz, B-01 y D-02 | NO EMITIDA |

## 3. Matriz de capacidades propuesta para F37-SBX

Solo pueden autorizarse EI ALLOWED o CONDITIONAL de la [matriz de capacidades](../F36SBX_Matriz_Capacidades.md). Las EI BLOCKED (EI-13 a EI-23) **no se pueden autorizar** y no figuran como opción. Cada fila admite tres decisiones: autorizar, restringir (autorizar con condiciones adicionales del equipo) o rechazar.

| EI | Capacidad (resumen) | Clase y alcance | Etapa del plan | Requisito adicional | Decisión del equipo |
|---|---|---|---|---|---|
| EI-01 | Organizar evidencia por metadatos declarados | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-02 | Alerta de proceso «requisito no evidenciado» | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-03 | Trazabilidad evidencia → criterio | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-04 | Desglose estructurado por criterio | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-05 | Guardia de entrada de PII | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-06 | Tipo de documento por metadatos | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-07 | Búsqueda léxica exacta en una postulación | ALLOWED, B | F37-SBX-A | — | NO EMITIDA |
| EI-09 | Recuperación léxica ponderada de fragmentos | CONDITIONAL, B | F37-SBX-A, si se confirma F36-M02 | En FG-12, `ei09_decision` con el valor `CABE_EN_ALCANCE_B`; impide FG-12 en NO APLICA | NO EMITIDA |
| EI-08 | Extracción estructurada por reglas | CONDITIONAL, C | F37-SBX-B | ADR sucesor APROBADO dentro del candidato (FG-12); F37-SBX-A cerrada | NO EMITIDA |
| EI-10 | Recuperación semántica con embeddings locales | CONDITIONAL, C | F37-SBX-B | ADR sucesor (FG-12) y dependencias aprobadas (FG-10) | NO EMITIDA |
| EI-11 | Extracción de texto de PDF o DOCX sintéticos | CONDITIONAL, C | F37-SBX-B | ADR sucesor (FG-12) y dependencias aprobadas (FG-10) | NO EMITIDA |
| EI-12 | NER solo de entidades no personales | CONDITIONAL, C | F37-SBX-B | ADR sucesor (FG-12) y dependencias aprobadas (FG-10) | NO EMITIDA |
| EI-24 | Métricas de equidad contrafactuales | CONDITIONAL, C | F37-SBX-B | ADR sucesor (FG-12) | NO EMITIDA |

Lista cerrada resultante (`authorized_ei` de FG-03 e idéntica a `f37_authorized_ei` del estado): NO EMITIDA.

## 4. Otras decisiones

| Decisión | Valores que admite el contrato | Decisión del equipo |
|---|---|---|
| Decisión de FG-03 | `AUTORIZA_INICIO_F37_SBX` o `NO_AUTORIZA` | NO EMITIDA |
| Numeración F36-M01 | `CONFIRMADA` o `NO_CONFIRMADA` | NO EMITIDA |
| Frontera de EI-09 (F36-M02) | `CABE_EN_ALCANCE_B`, `NO_CABE_EN_ALCANCE_B` o `SIN_DECISION` | NO EMITIDA |
| Dependencias nuevas (FG-10) | Sí, con cada dependencia revisada, o no | NO EMITIDA |
| ADR sucesor (FG-12, F36-M03) | Solo si se autoriza alguna EI CONDITIONAL de alcance C, y aprobado e incorporado **antes de fijar H** | NO EMITIDA |
| Estado de FG-12 | CUMPLE (con registro y 3 votos) o NO APLICA (sin registro ni votos propios, solo si no hay ninguna EI CONDITIONAL) | NO EMITIDA |
| Candidato del gate (D-01) | Ver matriz §7. Consta la instrucción operativa del solicitante de seguir la opción (b), un candidato final nuevo H | NO EMITIDA |
| Incremento sucesor B-01 (D-02) | Ver el [borrador de autorización D-02](BORRADOR_Autorizacion_D02.md) y las decisiones de diseño T-01 a T-07 | NO EMITIDA |
| Deuda AF6-L01 y AF6-L02 (D-05) | Corregirla en el incremento de H, o registrarla como LOW abiertos | NO EMITIDA |
| Sincronización del gobierno (D-07) | Antes de fijar H, o después | NO EMITIDA |

## 5. Registro de votos y abstenciones

Uno por integrante y por decisión votada. El contrato solo admite `APRUEBA`, `RECHAZA` o `SE_ABSTIENE`; cualquier voto distinto de `APRUEBA` impide que FG-03, FG-10 o FG-12 pasen a CUMPLE. Una abstención o un rechazo también se registran: no se omiten. Si FG-12 queda en NO APLICA, no hay votación de FG-12 que registrar: no se inventa una para completar la tabla.

| Decisión votada | Integrante | Voto | Fecha del voto | Canal de verificación del voto |
|---|---|---|---|---|
| PENDIENTE | Coronacion Meza Fredy | PENDIENTE | PENDIENTE | PENDIENTE |
| PENDIENTE | Peña Arroyo Anthony | PENDIENTE | PENDIENTE | PENDIENTE |
| PENDIENTE | Vila Meza Luis Antonio | PENDIENTE | PENDIENTE | PENDIENTE |

Los nombres son los de los integrantes que ya declara `CLAUDE.md` y que el esquema exige literalmente. No implican ningún voto.

## 6. Cierre del acta

| Campo | Valor |
|---|---|
| Resultado | NO EMITIDA |
| Firmas | Ninguna. Este borrador no se firma. El acta real se firma o se confirma fuera del repositorio, por el procedimiento de la [lista de comprobación](BORRADOR_Checklist_Evidencias_y_Verificacion.md#2-procedimiento-de-verificación) |
| Paso siguiente | PENDIENTE |

**Recordatorio.** Completar esta acta no supera el gate. Con este validador, F36-SBX-GATE solo puede pasar a SUPERADO tras un incremento sucesor auditado (decisión D-02), y ni siquiera entonces autoriza producción, datos reales, la G0 real ni el alcance C del producto.
