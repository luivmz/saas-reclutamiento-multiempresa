---
name: ml-risk-service
description: Marco del servicio de riesgo operacional del proceso de reclutamiento (RF-29, implementado en develop como experimental en las Fases 15 a 17; candidato, no validado para producción). Úsala al discutir, diseñar o evaluar machine learning, modelos predictivos, un servicio FastAPI de inferencia, datasets sintéticos o métricas de modelo para este proyecto. Define qué puede predecir el modelo, qué tiene prohibido predecir y qué evidencia exige antes de existir.
---

# Servicio de riesgo operacional

**Estado: implementado en `develop` como experimental.** Las Fases 15 a 17 lo construyeron dentro de este marco: `ml-service/` (dataset sintético, entrenamiento y servicio FastAPI con `/health`, `/v1/model-info` y `/v1/predict`), la integración Laravel ↔ FastAPI con `vacancies.target_completion_at` y la tarjeta de riesgo operacional. RF-29 está **validado técnicamente con datos sintéticos, no validado institucionalmente ni autorizado para producción**, y sigue siendo **candidato** (decisión 11). Detalle: [`phase-15-closeout.md`](../../../docs/v1.1/phase-15-closeout.md), [`phase-16-laravel-ml-integration.md`](../../../docs/v1.1/phase-16-laravel-ml-integration.md) y [`phase-17-ml-validation.md`](../../../docs/v1.1/phase-17-ml-validation.md).

**Contrato científico congelado.** No se modifica sin una fase y una decisión del equipo: *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`, *threshold* `0.1679418172266036`, Logistic Regression `C=10`, `class_weight=None`, `StandardScaler`, sin calibración.

Las reglas de abajo siguen vigentes para el servicio actual y para cualquier cambio o modelo futuro.

> Historia: hasta la Fase 21 esta skill decía «Estado: candidato. No implementes nada todavía» y limitaba su uso al diseño durante la Fase 13. Se actualizó en el hotfix documental de la Fase 21 (23/09/2026) para reflejar lo implementado; las fronteras y la evidencia exigida no cambiaron.

## La frontera, primero

El modelo predice **el comportamiento del proceso**, nunca a las personas.

**Puede estimar:**

- riesgo de **demora** de una convocatoria respecto de su fecha objetivo;
- probabilidad de que una etapa se **atasque** (evaluaciones sin programar, entrevistas sin resultado);
- **carga de trabajo** esperada por organización o por etapa;
- volumen de postulaciones esperado para una vacante.

**Tiene prohibido, sin excepción:**

- puntuar, ordenar, recomendar, filtrar, preseleccionar o descartar postulantes;
- predecir desempeño, idoneidad, permanencia, personalidad o "ajuste cultural";
- usar atributos sensibles o sus aproximaciones: nombre, sexo, edad, fecha de nacimiento, DNI, dirección, foto, nacionalidad, estado civil, discapacidad, religión, afiliación, universidad, texto libre del CV;
- alimentar, alterar o reordenar el ranking de RF-20 a RF-22;
- intervenir en la decisión final de RF-23 a RF-25.

Si una propuesta necesita cruzar esa frontera, la respuesta es no. Documenta la petición en `docs/v1.1/scope-preliminary.md` como descartada y explica por qué.

## Arquitectura implementada

- **Laravel es el sistema de registro.** Ninguna decisión ni estado de negocio nace en el servicio de ML.
- **FastAPI es un servicio de inferencia opcional y sin estado**: no accede a la base de datos principal, no conoce el dominio, no escribe en PostgreSQL, no guarda peticiones ni predicciones. Laravel calcula las features (`app/Services/Ml/OperationalRiskFeatureBuilder.php`) y el servicio solo devuelve la estimación.
- **Endpoints** (`ml-service/src/recruitment_ml/api/`): `GET /health` (abierto), `GET /v1/model-info` y `POST /v1/predict`, estos dos con la cabecera `X-Internal-Token`; sin token configurado en el servicio, `/v1/*` responde 503.
- **Fallback obligatorio**: timeout corto (`config/ml.php`), y si el servicio está deshabilitado (`ML_SERVICE_ENABLED=false`, valor por defecto), no responde, es lento o devuelve algo inválido, la vista se muestra sin la estimación. El proceso de reclutamiento **nunca** depende del modelo.
- Las pruebas de Laravel no llaman al servicio real: simulan el HTTP con `Http::fake()` o trabajan con el servicio deshabilitado.

## Contrato de `/v1/predict` (fuente: `schemas.py`)

**Petición — `PredictionRequest`.** Exactamente **15 features operacionales** de un proceso de vacante en su *checkpoint*, todas **enteras**, con `extra="forbid"` y `strict=True`: un campo de más, una cadena o un decimal se rechazan con 422. El servicio comprueba al arrancar que el esquema coincide con el contrato de features entrenado.

`elapsed_days_since_publication`, `application_window_days`, `positions_count`, `applications_received_count`, `configured_criteria_count`, `evaluations_scheduled_count`, `evaluations_completed_count`, `evaluations_overdue_pending_count`, `interviews_scheduled_count`, `interviews_completed_count`, `interviews_overdue_pending_count`, `stage_transition_count`, `days_since_last_operational_event`, `concurrent_open_vacancies_count`, `days_remaining_to_target`.

**Nada más cruza el límite**: ningún identificador —ni `candidate_id`, ni `vacancy_id`, ni `organization_id`—, ninguna PII, ningún atributo sensible, ningún texto libre y ningún resultado del proceso. `extra="forbid"` hace de esa regla una frontera efectiva, no una recomendación.

**Respuesta — `PredictionResponse`** (también con `extra="forbid"`), exactamente estos seis campos:

| Campo | Qué es |
|---|---|
| `risk_score` | Probabilidad estimada de retraso operacional **del proceso**, en [0, 1]. No evalúa, puntúa ni clasifica personas |
| `risk_flag` | `risk_score >= threshold`. Señal para revisión humana: no es decisión, recomendación, descarte ni ranking |
| `threshold` | Umbral congelado: `0.1679418172266036` |
| `model_version` | Identificador del experimento que produjo el modelo |
| `freeze_fingerprint` | Huella del protocolo congelado: `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2` |
| `status` | Estado del servicio: experimental, no desplegable |

**No hay un campo de incertidumbre** ni intervalo por predicción: el modelo es una regresión logística **sin calibración** y el contrato no lo expone. Laravel (`MlRiskClient`) valida además la respuesta antes de usarla —tipos, rango, `risk_flag` coherente con el umbral, y que `threshold` y `freeze_fingerprint` sean los congelados—; cualquier discrepancia la descarta.

## Datos y evidencia exigidas (cumplidas para el experimento; exigibles a cualquier modelo nuevo)

Los detalles del protocolo están en [EVALUATION.md](EVALUATION.md). En resumen:

1. **Dataset sintético, rotulado como tal** en el propio archivo, en la documentación y en la interfaz. Nunca datos reales de personas.
2. **Prevención de fuga**: ninguna característica posterior al hecho que se predice; partición temporal, no aleatoria; el mismo proceso nunca aparece en entrenamiento y prueba.
3. **Línea base honesta** (media histórica o regla simple). Si el modelo no la supera con claridad, no hay modelo.
4. **Métricas reportadas con intervalo**: MAE y RMSE para regresión; AUC-PR, *precision*/*recall* y **calibración** (Brier, diagrama de confiabilidad) para clasificación.
5. **Model card**: propósito, datos, límites, métricas, usos prohibidos y responsable.
6. **Pruebas `pytest`** del contrato, del preprocesamiento y de los casos borde; nada de red en las pruebas.
7. **Criterios de no-go** explícitos: si se cumplen, el servicio no se implementa y v1.1 se entrega sin él.

## En la interfaz

Lo implementado es la tarjeta «Riesgo operacional del proceso» (`resources/js/components/vacancies/operational-risk-card.tsx`), solo en el detalle de la vacante: nunca cerca del ranking, de la comparación de candidatos ni de la decisión final. Tiene tres estados: `predictive_available` (el porcentaje de `risk_score` y la señal de `risk_flag`), `descriptive_only` («Solo información descriptiva», por ejemplo sin plazo objetivo) y `unavailable`. Siempre lleva la etiqueta **Experimental**, dice que estima el proceso y no a las personas, que el modelo se entrenó con datos sintéticos y que la decisión final corresponde al Aprobador/Dirección (RF-23). **No muestra una incertidumbre**, porque el contrato no la tiene; cualquier modelo futuro que la exponga debe mostrarla.

> Historia: hasta el hotfix final de la Fase 21 (23/09/2026) esta sección y la de arquitectura conservaban el diseño candidato de la Fase 13 —«devuelve un número con su incertidumbre», «incertidumbre visible», «solo identificadores internos, conteos, duraciones y fechas relativas»—, que no coincide con el contrato implementado. Se reescribieron a partir de `schemas.py` y del código de Laravel.
