# Viabilidad del servicio de riesgo operacional

**Estado: estudio de viabilidad. No se ha implementado nada, no se ha entrenado ningún modelo y no existe ningún dataset.** Este documento describe qué tendría que ser cierto para que el servicio exista.

> **Actualización del 20 de septiembre de 2026 (Fase 14).** Este estudio sigue vigente y no se reescribe. La Fase 14 lo llevó de estudio de viabilidad a **especificación formal aprobada**: el equipo tomó doce decisiones que fijan problema, unidad, checkpoint, target, dataset, partición, modelos, métrica, política de umbrales, features, censura y criterios de no-go. Punto de entrada: [`phase-14-ml-definition.md`](phase-14-ml-definition.md).
>
> **Conclusión operativa:** el experimento **puede** ejecutarse sobre datos sintéticos, pero `job_requests.required_by` **no** se reinterpreta como plazo objetivo. La necesidad de un `target_completion_at` explícito queda aprobada conceptualmente y su implementación registrada como `GAP-01`. Eso separa dos compuertas: el **gate científico**, cumplido salvo la autorización para crear código Python, y el **gate de integración Laravel**, **bloqueado** hasta resolver `GAP-01`.

## 1. Qué se propone predecir

El **comportamiento del proceso de reclutamiento**, cuya unidad de análisis es la convocatoria o la etapa, nunca el postulante:

- riesgo de que una convocatoria supere su fecha objetivo;
- probabilidad de que una etapa quede atascada;
- carga de trabajo esperada por organización o etapa.

## 2. Qué está prohibido predecir

Puntuar, ordenar, recomendar, filtrar, preseleccionar o descartar postulantes; estimar desempeño, idoneidad, permanencia, personalidad o "ajuste cultural"; usar atributos sensibles o sus aproximaciones (nombre, sexo, edad, DNI, dirección, foto, nacionalidad, estado civil, discapacidad, universidad, texto libre del CV); alimentar o alterar el ranking de RF-20 a RF-22; intervenir en la decisión de RF-23 a RF-25.

Esta frontera es una decisión de arquitectura registrada en [ADR-001](architecture-decisions/ADR-001-ml-boundary.md) y no se renegocia por conveniencia técnica.

## 3. Arquitectura propuesta

```
React/Inertia ──► Laravel (sistema de registro, PostgreSQL)
                      │  HTTP, timeout corto, sin PII
                      ▼
                 FastAPI /v1/predict  (sin estado, sin base de datos, sin dominio)
                      │
                      ▼
                 {valor, incertidumbre, model_version}
```

- Laravel decide qué mostrar y qué guardar; el servicio solo calcula.
- Si el servicio falla, es lento o responde algo inválido, la pantalla se muestra **sin** la estimación. El proceso nunca depende del modelo.
- Solo cruzan el límite conteos, duraciones, fechas relativas y estados. Nunca datos de una persona.
- Contrato versionado, `health check` y `model_version` en cada respuesta.

## 4. Datos

No existen datos reales y **no deben obtenerse**. El estudio usaría un dataset **sintético** generado a partir de la estructura real del proceso, rotulado como ficticio en el archivo, en la documentación y en cualquier pantalla que muestre resultados derivados.

Consecuencia honesta que el informe debe declarar: con datos sintéticos, un buen resultado demuestra que el método es correcto, **no** que el modelo funcionaría en el Colegio Andino.

## 5. Evidencia mínima antes de aprobar

Protocolo completo en `.claude/skills/ml-risk-service/EVALUATION.md`. Resumen:

1. Partición **temporal** (nunca aleatoria) y prevención explícita de fuga de información.
2. **Línea base** simple (media histórica o regla fija) contra la cual comparar.
3. Métricas reportadas con incertidumbre: MAE/RMSE en regresión; AUC-PR, *precision*/*recall* y **calibración** (Brier, diagrama de confiabilidad) en clasificación.
4. **Model card** con propósito, datos, límites y usos prohibidos.
5. Pruebas `pytest` del contrato y del preprocesamiento, sin red.
6. En Laravel, `Http::fake()` cubriendo respuesta válida, inválida, timeout y servicio caído.

## 6. Criterios de no-go

El servicio **no se implementa** si se cumple cualquiera:

1. el modelo no supera la línea base en la partición temporal;
2. hay fuga de información que no puede eliminarse;
3. el dataset sintético no representa razonablemente el proceso;
4. la calibración es mala y la estimación induciría a error;
5. el esfuerzo pone en riesgo los entregables académicos de v1.1;
6. alguna característica necesaria obligaría a cruzar la frontera de la sección 2.

Un no-go es un resultado válido y publicable. Se documenta aquí con su evidencia y v1.1 se entrega sin el servicio.

## 7. Presentación en la interfaz, si llegara a existir

Etiqueta explícita de "estimación", incertidumbre visible, origen del dato, aviso de que no evalúa personas, y ubicación lejos del ranking, de la comparación de candidatos y de la decisión final.

## 8. Estado actual

| Elemento | Estado al 20 de septiembre de 2026 |
|---|---|
| Decisión de explorar el servicio | **Aprobada** (decisión 1) |
| Especificación formal del experimento | **Existe y está aprobada** — ver [`phase-14-ml-definition.md`](phase-14-ml-definition.md) |
| Semántica del plazo objetivo (`ML-DECISION-01`) | **Resuelta** — `required_by` descartado; `target_completion_at` aprobado conceptualmente |
| Implementación del plazo (`GAP-01`) | **Abierta — bloquea la integración, no el experimento** |
| Autorización para código Python y dependencias | **Pendiente** — única condición que falta del gate científico |
| Dataset | No existe |
| Modelo | No existe |
| Servicio FastAPI | No existe |
| Cliente en Laravel | No existe |
| Dependencias añadidas | Ninguna |

### Dónde continúa este estudio

| Tema | Documento de la Fase 14 |
|---|---|
| Problema, unidad, checkpoint, target, fuga | [`ml/problem-definition.md`](ml/problem-definition.md) |
| Features incluidas, excluidas y prohibidas | [`ml/feature-contract.md`](ml/feature-contract.md) |
| Dataset sintético reproducible | [`ml/dataset-specification.md`](ml/dataset-specification.md) |
| Split, baselines, métricas, aceptación y no-go | [`ml/evaluation-plan.md`](ml/evaluation-plan.md) |
| Ética y supervisión humana | [`ml/ethics-and-human-oversight.md`](ml/ethics-and-human-oversight.md) |
| Borrador de model card | [`ml/model-card-draft.md`](ml/model-card-draft.md) |
| Contrato conceptual de API | [`ml/api-contract-draft.md`](ml/api-contract-draft.md) |
| Decisión de arquitectura | [`architecture-decisions/ADR-004-ml-problem-definition.md`](architecture-decisions/ADR-004-ml-problem-definition.md) |
