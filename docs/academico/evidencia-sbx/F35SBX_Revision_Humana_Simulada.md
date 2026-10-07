# F35-SBX-A — Revisión humana simulada

> Fase F35-SBX-A, versión 1 (07/10/2026). Aplica DH-05: `SyntheticHumanReview` revisa solo la integridad y la procedencia del **artefacto**, nunca a la persona sintética a la que se refiere la evidencia.

## 1. Qué revisa

| Aspecto | Pregunta del revisor simulado |
|---|---|
| Integridad | ¿El texto, los hashes y los enlaces entre evidencia, fuente, provenance y run coinciden con lo registrado? |
| Procedencia | ¿La evidencia procede de la fila F34 declarada y de su tenant? |

`review_scope` tiene un único valor admitido, `integridad_y_procedencia`, sin alias ni valores alternativos, y `review_status` solo admite `conforme` u `observado`. `reviewer_type` es siempre `synthetic_human_simulation`, `simulation_actor` es el rol simulado del tenant (`SIMREV-ORG-S*`) y `scripted = true`: la decisión viene declarada en el fixture.

## 2. Qué nunca evalúa

| Prohibido en la revisión simulada | Consecuencia |
|---|---|
| Aptitud, mérito o idoneidad | Campo o valor evaluativo: FAIL (REV, CAP) |
| Desempeño, personalidad o cualquier inferencia sobre la persona | FAIL |
| Recomendación, selección o ranking de personas | FAIL |
| Estados como «apto», «no apto», «recomendado» o «seleccionado» | Fuera del enum: FAIL |
| Decisión final de contratación | RF-23 sigue humana y fuera de F35-SBX |

## 3. Reglas

- Exactamente una revisión por evidencia; sin revisión, la evidencia no se cierra (caso NS-34).
- El `review_status` de la evidencia es igual al de su revisión.
- La revisión es del mismo tenant y del mismo run que la evidencia.
- El conjunto de campos es cerrado: un campo adicional falla aunque su valor sea inocuo.
