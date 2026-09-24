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

## Arquitectura (acordada como candidata, implementada así)

- **Laravel es el sistema de registro.** Ninguna decisión ni estado de negocio nace en el servicio de ML.
- **FastAPI es un servicio de inferencia opcional y sin estado**: no accede a la base de datos principal, no conoce el dominio, no escribe en PostgreSQL. Recibe un vector de características ya anonimizado y devuelve un número con su incertidumbre.
- **Contrato versionado** (`/v1/predict`), con esquema de entrada y salida explícito, `model_version` en cada respuesta, timeout corto y *health check*.
- **Fallback obligatorio**: si el servicio no responde, es lento o devuelve algo inválido, Laravel muestra la vista sin la estimación. El proceso de reclutamiento **nunca** depende del modelo.
- **Sin PII cruzando el límite**: solo identificadores internos, conteos, duraciones y fechas relativas.
- La comunicación se simula con `Http::fake()` en todas las pruebas de Laravel.

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

La estimación se presenta como **información operativa**: etiqueta explícita de "estimación", incertidumbre visible, origen del dato y aviso de que no evalúa personas. Nunca cerca del ranking, de la comparación de candidatos ni de la decisión final.
