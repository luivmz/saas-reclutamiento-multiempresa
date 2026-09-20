---
name: ml-risk-service
description: Marco de diseño del servicio de riesgo operacional del proceso de reclutamiento (candidato v1.1, aún NO implementado). Úsala al discutir, diseñar o evaluar machine learning, modelos predictivos, un servicio FastAPI de inferencia, datasets sintéticos o métricas de modelo para este proyecto. Define qué puede predecir el modelo, qué tiene prohibido predecir y qué evidencia exige antes de existir.
---

# Servicio de riesgo operacional (diseño, no implementación)

**Estado: candidato. No implementes nada todavía.** Esta skill fija el marco para que, si el equipo lo aprueba, el servicio nazca correcto. Mientras la Fase 13 esté vigente, su uso es exclusivamente de diseño y documentación en `docs/v1.1/ml-feasibility.md`.

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

## Arquitectura acordada como candidata

- **Laravel es el sistema de registro.** Ninguna decisión ni estado de negocio nace en el servicio de ML.
- **FastAPI es un servicio de inferencia opcional y sin estado**: no accede a la base de datos principal, no conoce el dominio, no escribe en PostgreSQL. Recibe un vector de características ya anonimizado y devuelve un número con su incertidumbre.
- **Contrato versionado** (`/v1/predict`), con esquema de entrada y salida explícito, `model_version` en cada respuesta, timeout corto y *health check*.
- **Fallback obligatorio**: si el servicio no responde, es lento o devuelve algo inválido, Laravel muestra la vista sin la estimación. El proceso de reclutamiento **nunca** depende del modelo.
- **Sin PII cruzando el límite**: solo identificadores internos, conteos, duraciones y fechas relativas.
- La comunicación se simula con `Http::fake()` en todas las pruebas de Laravel.

## Datos y evidencia exigidas antes de aprobar

Los detalles del protocolo están en [EVALUATION.md](EVALUATION.md). En resumen:

1. **Dataset sintético, rotulado como tal** en el propio archivo, en la documentación y en la interfaz. Nunca datos reales de personas.
2. **Prevención de fuga**: ninguna característica posterior al hecho que se predice; partición temporal, no aleatoria; el mismo proceso nunca aparece en entrenamiento y prueba.
3. **Línea base honesta** (media histórica o regla simple). Si el modelo no la supera con claridad, no hay modelo.
4. **Métricas reportadas con intervalo**: MAE y RMSE para regresión; AUC-PR, *precision*/*recall* y **calibración** (Brier, diagrama de confiabilidad) para clasificación.
5. **Model card**: propósito, datos, límites, métricas, usos prohibidos y responsable.
6. **Pruebas `pytest`** del contrato, del preprocesamiento y de los casos borde; nada de red en las pruebas.
7. **Criterios de no-go** explícitos: si se cumplen, el servicio no se implementa y v1.1 se entrega sin él.

## En la interfaz

Cuando exista, la estimación se presenta como **información operativa**: etiqueta explícita de "estimación", incertidumbre visible, origen del dato y aviso de que no evalúa personas. Nunca cerca del ranking, de la comparación de candidatos ni de la decisión final.
