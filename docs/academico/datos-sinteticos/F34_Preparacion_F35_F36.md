# F34 — Readiness y preparación para F35/F36

> Fase F34, versión 1.1 (04/10/2026), corregida tras la auditoría F34. **F34 no aprueba F35.** Este documento solo fija qué podrían consumir F35 y F36 **si algún día** el equipo aprueba G0.

## Estado de F34

- **F34 = LISTA PARA AUDITORÍA.** Entregables completos (contrato, dataset sintético reproducible, validadores y gobernanza) y hallazgos M01, M02, M03 y LOW de la auditoría corregidos. Solo el equipo puede cerrarla tras su auditoría.
- **F35–F40 = BLOQUEADAS.**
- **G0 = NO APROBADA.** ADR-005 sigue **PROPUESTA**.
- RF-23 sigue siendo humana y RF-29 experimental e informativa. No cambió ningún RF, CU o RNF, ni ADR-001/002, ARQ-01 o el runtime.

## Qué podría consumir F35 (pipeline de evidencia, alcance B)

Solo con G0 aprobada al menos con restricciones (alcance B):

| Artefacto | Uso previsto | Condición |
|---|---|---|
| [`schema.json`](../tools/f34/schema.json) (bloques A, B y C) | Diseño de tablas y validaciones del módulo de evidencia | Las migraciones reales necesitan su propia fase y regresión |
| `vacancies`, `criteria`, `rubric_levels`, `requirements` | Escenarios de prueba de configuración y publicación | Solo datos sintéticos |
| `sessions`, `assessments`, `evidence`, `annotations` | Pruebas de FF-02 (`PROGRAMADA` → registro → `REALIZADA`) y de las anotaciones complementarias | Sin segundo resultado; sin sugerir niveles |
| `expected_alerts` | Oráculo para probar las reglas deterministas de F33 (CAP-01, evidencia faltante, discrepancia, sesión vencida) | Las reglas se implementan aparte; el oráculo no las sustituye |
| [`qa_cases.json`](dataset/qa_casos/qa_cases.json) | Casos negativos para los validadores de F35 | — |
| `analysis_runs` + `analysis_run_events` | Pruebas del registro inmutable con eventos | — |

## Qué podría consumir F36 (ML baseline, alcance E)

Solo con G0 aprobada y **solo sobre el proceso**:

| Artefacto | Uso previsto | Condición |
|---|---|---|
| `process_snapshots` (15 variables RF-29 + `delayed`) | Pruebas de pipeline del proceso | No sustituye ni modifica el dataset y el contrato congelados de RF-29 (`ml-service`) |
| `process_splits` | Partición temporal agrupada con purga por madurez de la etiqueta | Mantener el orden temporal; no usar filas `purgado` ni `censurado` como etiquetadas; `label_known_at` nunca es feature |
| `fairness_sintetico/` | Solo F37: prueba metodológica de separación y agregación | Nunca en features |

## Qué no podrá consumir ninguna fase

- `human_level`, `rubric_points` o `evidence_sufficiency` como etiqueta o feature de un modelo sobre personas.
- `evidence_sufficiency`, `evaluator_disagreement` o sus agregados como features de cualquier modelo: solo QA, análisis del proceso e ICC.
- `grupo_sintetico` como feature.
- Los textos libres como entrada de NLP (alcance C, futuro).
- Cualquier dato real: lo impide la regla de datos de F33/F34.

## Entrada mínima para abrir F35

1. Registro del equipo con G0 aprobada al menos con restricciones (las condiciones están en [ADR-005 §10](../diseno-inteligente/F33_ADR_005_G0.md#10-resultado-g0-en-f33)).
2. `validate_f34.py` en verde sobre la versión del dataset que se vaya a usar.
3. Dataset Card revisado.
