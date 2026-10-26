# F36-SBX — Charter de autorización, investigación y diseño

> Fase F36-SBX, versión 1 (26/10/2026), en la rama `feature/f36-sbx-authorization-design`, desde `main` = `b8892af39a6492d8dd44a36290604efc602380cd`. **Candidata a auditoría independiente.** Solo documentación, gobierno y validadores documentales.

## 1. Qué es este incremento

F36-SBX es la autorización sucesora **separada** que exigían el cierre global de F35-SBX y F34E: «ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza» ([cierre global](../evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md), [autorización F34E §1](../g0-sandbox/F34E_Autorizacion_F35_SBX.md#1-estados)).

| Aspecto | Valor |
|---|---|
| Origen | Instrucción del equipo del 26/10/2026 para preparar F36-SBX como incremento de autorización, investigación y diseño. La transcribe la sesión de trabajo de esa fecha; no hay un adjunto firmado |
| Autoriza | Solo **investigar y diseñar**: matriz de capacidades, contrato de evidencia, threat model, plan de evaluación y gate sucesor. También los validadores documentales de este paquete y sus pruebas |
| No autoriza | Implementar ML, NLP, embeddings, OCR, parsing automático, búsqueda semántica ni un LLM. Tampoco endpoints, migraciones, UI, integración productiva, dependencias nuevas, datos reales ni el inicio de F37-SBX |
| Estado | **F36-SBX = EN DISEÑO**: solo documental, candidata a auditoría independiente |
| Fase siguiente | **F37-SBX = BLOQUEADA** mientras el [F36-SBX-GATE](F36SBX_Gate_Sucesor.md) siga NO SUPERADO |

Este charter no es una aprobación jurídica, de privacidad ni institucional, ni una aprobación de ADR-005. No cambia ningún estado de la G0 real.

## 2. Estados de gobierno que el charter preserva

Se verificaron sobre `b8892af` antes de abrir la rama. F36-SBX no modifica ninguno:

| Estado | Valor |
|---|---|
| G0 real | NO APROBADA |
| G0-02, G0-03 y G0-12 | PENDIENTE EXTERNO |
| G0-09 y G0-14 | CUMPLIDO |
| G0-SBX | APROBADA CON RESTRICCIONES; su alcance sigue siendo solo F35-SBX |
| ADR-005 | PROPUESTA |
| F35 productiva | BLOQUEADA |
| F35-SBX | CERRADA Y CONGELADA; F36-SBX no toca ninguna de sus superficies |
| F36–F40 productivas | BLOQUEADAS |
| Alcance C | BLOQUEADO |
| Datos reales | PROHIBIDOS |
| RF-23 | Decisión final humana del Aprobador o Dirección |
| RF-29 | Experimental, informativo y sobre el proceso |
| GC-AF-L01 | LOW, ABIERTO / DIFERIDO, no bloqueante ([registro](../TECHNICAL_DEBT.md)) |

## 3. Problema académico que se estudia

> ¿Qué ayudas computacionales **sobre la evidencia** de un expediente sintético pueden facilitar el trabajo de un evaluador humano (organizar, localizar y trazar evidencia frente a criterios explícitos), sin puntuar, ordenar, recomendar ni seleccionar personas? ¿Cómo se demostraría, solo con datos sintéticos, que una ayuda es fiel a su fuente, se abstiene cuando no hay evidencia y no introduce un ranking encubierto?

La pregunta parte de la cadena de procedencia de F30 (pregunta → respuesta → evidencia → criterio → nivel humano → justificación; [F30 §4](../investigacion-ia/F30_Analisis_Modelos_y_Tecnicas.md#4-cadena-de-procedencia-de-la-evidencia)). Ataca el eslabón «evidencia», que hoy se registra a mano. El nivel lo sigue asignando una persona (CAP-05).

### 3.1 Visión funcional y su tratamiento

| Elemento de la visión | Tratamiento en F36-SBX |
|---|---|
| Organizar evidencia | ALLOWED para diseño (EI-01) |
| Localizar evidencia relevante | Léxica: CONDITIONAL de alcance B (EI-09). Semántica: CONDITIONAL de alcance C (EI-10) |
| Resumir evidencia | **BLOCKED** (EI-13). Un resumen de la evidencia de un postulante es un resumen del candidato (CAP-11 y CAP-23 de F33) |
| Contrastar evidencia con criterios | La trazabilidad del enlace humano, ALLOWED (EI-03). El veredicto automático «cumple o no cumple», **BLOCKED** (EI-14) |
| Mostrar por qué una evidencia se relaciona con un criterio | ALLOWED como trazabilidad de cita, fuente y versión (EI-03, CAP-29) |
| Comparar candidatos de forma controlada | El desglose por criterio, sin orden ni insignias, ALLOWED (EI-04, CAP-13). La similitud entre candidatos, **BLOCKED** (EI-18, CAP-10) |

El detalle completo está en la [matriz de capacidades](F36SBX_Matriz_Capacidades.md).

## 4. Prohibiciones duras

Rigen en F36-SBX y en cualquier F37-SBX, aunque el gate se supere. Se suman a las [prohibiciones de F34E](../g0-sandbox/F34E_Prohibiciones.md), sin reemplazarlas:

1. Datos reales de candidatos, CV reales y PII real.
2. Audio o vídeo real de candidatos.
3. Biometría, reconocimiento facial e identificación por voz.
4. Inferir emociones, personalidad, honestidad, inteligencia, estrés o nerviosismo.
5. Cualquier inferencia desde rostro, gestos, voz, prosodia o acento.
6. Selección automática y decisión automática de contratación.
7. Modificar o sustituir RF-23.
8. Scoring, ranking o recomendación de candidatos. Solo una autorización sandbox futura, separada y explícita podría siquiera plantearlo, y este charter no la anticipa.
9. Alimentar producción, crear endpoints productivos o migraciones productivas.
10. Procesar datos reales.

**Observaciones humanas.** Una observación escrita por una persona sintética puede estudiarse como evidencia, con procedencia explícita (`author_kind = human_synthetic`). El sistema nunca la reinterpreta como inferencia propia ni como inferencia biométrica. Si una observación sintética describe conducta («explicó con un ejemplo concreto…»), es un texto de su autor. No es una medición del sistema.

## 5. Divergencia con el mapa F33

En el [mapa F33](../diseno-inteligente/F33_Mapa_F34_F40.md), «F36» designa el **ML baseline del proceso** (CAP-26). F36-SBX usa el número siguiente de la secuencia sandbox para otro objeto: la autorización y el diseño de la inteligencia sobre evidencia.

- El mapa F33 no se reescribe y la F36 productiva («ML baseline») sigue BLOQUEADA.
- F36-SBX no es la F36 del mapa y no habilita el ML del proceso ni cambia el contrato congelado de RF-29.
- Las capacidades que estudia F36-SBX, como CAP-07, CAP-08, CAP-09 y CAP-20, figuran en F33 en las filas de F35, F37 y F39. Se citan siempre por su CAP-xx, no por la fase del mapa.
- Hallazgo F36-M01 ([informe](F36SBX_Investigacion_Diseno.md#9-hallazgos-de-diseño)): el equipo debe confirmar esta numeración o elegir otra antes de F37-SBX.

## 6. Relación con las puertas existentes

| Puerta | Qué decide | Efecto de F36-SBX |
|---|---|---|
| G0 real (ADR-005 §9) | F35–F40 productivas | Ninguno. Sigue NO APROBADA |
| G0-SBX (F34E) | F35-SBX | Ninguno. Su significado histórico no cambia: autorizó F35-SBX y nada más |
| Gates de F35-SBX (B1, B2, B3, cierre terminal y cierre global) | Integridad de F35-SBX | Ninguno. Están congelados y fallan sobre un HEAD posterior por diseño (DG-02) |
| **F36-SBX-GATE** (nuevo) | Si F37-SBX puede comenzar | Lo define este paquete; hoy el resultado es **NO SUPERADO** |

## 7. Revocación

Si ocurre cualquiera de estos hechos, F36-SBX queda REVOCADA y su gate pasa a REVOCADO:

- aparece un dato real o PII real en cualquier artefacto F36-SBX;
- un artefacto F36-SBX afirma o habilita algo que la sección 4 prohíbe;
- se modifica una superficie congelada de F35-SBX, el runtime o las dependencias;
- el equipo retira la autorización.

La revocación se registra en un incremento nuevo y no reescribe este charter. Con F36-SBX revocada, F37-SBX no puede comenzar.

## 8. Artefactos

| Artefacto | Objetivo |
|---|---|
| [Matriz de capacidades](F36SBX_Matriz_Capacidades.md) | Clasifica cada capacidad como ALLOWED, CONDITIONAL o BLOCKED, con su CAP-xx y su alcance |
| [Investigación y diseño](F36SBX_Investigacion_Diseno.md) | Tareas, enfoques, viabilidad de hardware, arquitectura conceptual y propuesta de ADR sucesor |
| [Contrato de evidencia](F36SBX_Contrato_Evidencia.md) y [`f36sbx_evidence_contract.json`](contrato/f36sbx_evidence_contract.json) | Tipos de evidencia sintética, procedencia, marcadores, particiones y fuga |
| [Threat model](F36SBX_Threat_Model.md) | Amenazas TEI-01..TEI-22 con controles fail-closed |
| [Plan de evaluación](F36SBX_Plan_Evaluacion.md) | Métricas por tarea, oráculos y umbrales declarados antes de medir. Sin resultados |
| [Gate sucesor](F36SBX_Gate_Sucesor.md) y [`f36sbx_gate_state.json`](gate/f36sbx_gate_state.json) | Criterios FG-01..FG-14, regla PASS/FAIL y plan de entrada a F37-SBX |
| [Trazabilidad](F36SBX_Trazabilidad.md) | Relación con F30, F33, F34, F35, los RF y las amenazas anteriores |
| [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) y [`test_f36sbx.py`](../tools/f36sbx/test_f36sbx.py) | Validador fail-closed del paquete y sus pruebas negativas y mutantes |
