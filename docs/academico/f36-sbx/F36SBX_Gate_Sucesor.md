# F36-SBX — Gate sucesor (F36-SBX-GATE) y plan de entrada a F37-SBX

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. **Resultado vigente: F36-SBX-GATE = NO SUPERADO. F37-SBX = BLOQUEADA.**

## 1. Nombre y propósito

**F36-SBX-GATE** decide una sola cosa: si **F37-SBX** puede comenzar. Lleva el nombre de la fase que lo define, como G0-SBX nació en F34E. Así no se confunde con la G0 real ni con un «G1» de producto.

| Propiedad | Cómo se garantiza |
|---|---|
| Sintético únicamente | FG-07: el contrato de evidencia solo admite `source_type = synthetic` |
| Verificable | Los criterios automáticos los recalcula [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) y no se fía del valor declarado |
| Reproducible | Biblioteca estándar, sin red, sin reloj en la decisión y con entradas versionadas en Git |
| Fail-closed | Un estado desconocido, una evidencia ausente o un JSON inválido producen NO SUPERADO |
| Revocable | FG-14 y la sección 5 |
| Independiente de la G0 real | Ningún criterio depende de G0-02, G0-03 o G0-12, y ninguno los da por resueltos |
| No autoriza producción, datos reales ni selección automática | FG-13: `authorizes` es exactamente `["F37-SBX"]`, y la lista `cannot_authorize` es cerrada y obligatoria |

## 2. Estados

| Estado | Significado |
|---|---|
| **NO SUPERADO** | Algún criterio no está en CUMPLE (o en NO APLICA, cuando se admite). F37-SBX bloqueada |
| **SUPERADO** | Todos los criterios están en CUMPLE, o en NO APLICA cuando se admite. F37-SBX puede comenzar, solo con las EI autorizadas en FG-03 |
| **REVOCADO** | Hay un evento de revocación registrado. F37-SBX bloqueada o detenida |

Ningún validador «aprueba» por sí solo. SUPERADO exige FG-02 y FG-03, que son actos humanos registrados. El validador solo comprueba que existen y que son coherentes.

## 3. Criterios

| ID | Criterio | Tipo | Evidencia exigida | Estado vigente |
|---|---|---|---|---|
| FG-01 | El paquete F36-SBX está íntegro: pasan todas las reglas de contenido de `validate_f36sbx.py` (STR, LNK, GOV, SEM, CAP, CTR, THR, EVA, FRZ, DEP y PII) | AUTO | Ejecución del validador | CUMPLE |
| FG-02 | Auditoría independiente del paquete F36-SBX con 0 BLOCKER, 0 HIGH y 0 MEDIUM abiertos | EQUIPO | Veredicto archivado en `gate/evidencia/`, con el commit auditado | PENDIENTE |
| FG-03 | Autorización explícita de F37-SBX por el equipo: registro fechado, quórum de los tres integrantes, lista cerrada de EI autorizadas y confirmación de la numeración (F36-M01) | EQUIPO | Registro archivado en `gate/evidencia/` | PENDIENTE |
| FG-04 | Los estados de gobierno siguen intactos en `CLAUDE.md`, `README.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md` | AUTO | Regla GOV | CUMPLE |
| FG-05 | F35-SBX congelada, el runtime y las dependencias no cambian desde la base | AUTO | Regla FRZ | CUMPLE |
| FG-06 | La matriz de capacidades es coherente con F33 y bloquea todo lo prohibido | AUTO | Regla CAP | CUMPLE |
| FG-07 | El contrato de evidencia es válido, cerrado y solo sintético | AUTO | Regla CTR | CUMPLE |
| FG-08 | Cada amenaza TEI tiene control y comportamiento fail-closed | AUTO | Regla THR | CUMPLE |
| FG-09 | El plan de evaluación cubre cada EI ALLOWED o CONDITIONAL y declara que no hay resultados | AUTO | Regla EVA | CUMPLE |
| FG-10 | Registro de dependencias (versión, licencia, OSV y hash) para toda EI autorizada que las necesite | EQUIPO | Registro en `gate/evidencia/`. NO APLICA solo si FG-03 no autoriza ninguna EI CONDITIONAL | PENDIENTE |
| FG-11 | No hay scoring, ranking, recomendación ni selección automática, y RF-23 sigue humana | AUTO | Reglas CAP y SEM | CUMPLE |
| FG-12 | ADR sucesor APROBADO para toda EI CONDITIONAL de alcance C autorizada, y confirmación escrita de F36-M02 si se autoriza EI-09 | EQUIPO | Registro en `gate/evidencia/`. NO APLICA solo si FG-03 no autoriza ninguna EI CONDITIONAL | PENDIENTE |
| FG-13 | El gate solo autoriza F37-SBX y declara todo lo que no puede autorizar | AUTO | Regla GATE | CUMPLE |
| FG-14 | No hay ningún evento de revocación registrado | AUTO | Regla GATE | CUMPLE |

**Resultado vigente: NO SUPERADO,** porque FG-02, FG-03, FG-10 y FG-12 están PENDIENTES. Se registra en [`f36sbx_gate_state.json`](gate/f36sbx_gate_state.json), y el validador recalcula el resultado y exige que coincida con el declarado aquí y en el JSON.

## 4. Regla de decisión

```
si revocation != null                                → REVOCADO
si algún criterio tiene un estado fuera de
   {CUMPLE, PENDIENTE, NO CUMPLE, NO APLICA}         → NO SUPERADO  (fail-closed)
si un AUTO declarado difiere del recalculado         → NO SUPERADO  (y la regla GATE falla)
si un EQUIPO en CUMPLE no tiene evidencia existente  → NO SUPERADO
si NO APLICA aparece fuera de FG-10 y FG-12, o con
   FG-03 sin CUMPLE, o con alguna EI CONDITIONAL
   en la autorización                                → NO SUPERADO
si la autorización de FG-03 incluye una EI BLOCKED
   o una EI que no está en la matriz                 → NO SUPERADO
si todos los criterios están en CUMPLE o NO APLICA   → SUPERADO
en cualquier otro caso                               → NO SUPERADO
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
| **F37-SBX-B** (subconjunto de C, solo sintético) | EI-08, EI-10, EI-11, EI-12 y EI-24 | F37-SBX-A cerrada. ADR sucesor APROBADO (FG-12). Dependencias registradas (FG-10) | Lo mismo que A, más la auditoría contrafactual y la comparación con BM25 |

**Primer paso concreto, cuando el equipo lo decida:** auditar este paquete (FG-02) y, si la auditoría pasa, registrar la autorización de FG-03 con la lista de EI de F37-SBX-A. Nada de F37-SBX se implementa antes.

**Salida de F37-SBX.** Nada migra a producción. Siguen rigiendo SAL-01 a SAL-05 de [F34E](../g0-sandbox/F34E_Autorizacion_F35_SBX.md#3-criterios-de-salida-de-sbx-a-trabajo-real) y la regla de datos de ADR-005 §6.10.
