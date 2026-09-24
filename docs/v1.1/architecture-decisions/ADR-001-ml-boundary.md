# ADR-001 — Frontera del machine learning

- **Estado:** aceptada como restricción de diseño (la existencia del servicio sigue pendiente de decisión)
- **Fecha:** 19 de septiembre de 2026
- **Contexto:** Fase 13, planificación de v1.1

> **Nota de evolución (hotfix final de la Fase 21, 23/09/2026).** La decisión sigue vigente y no se reescribe. Lo que cambió: el servicio **existe** como experimento (Fases 15 a 17) y se construyó dentro de esta frontera. Una diferencia con el texto de abajo: la respuesta implementada **no incluye incertidumbre** —devuelve `risk_score`, `risk_flag`, `threshold`, `model_version`, `freeze_fingerprint` y `status`— y recibe 15 features operacionales enteras, sin identificadores ni PII. El contrato vigente está en la skill `ml-risk-service` y en `ml-service/src/recruitment_ml/api/schemas.py`.

## Contexto

Se propone incorporar un componente de machine learning a la plataforma. El sistema gestiona procesos de reclutamiento: cualquier modelo mal encuadrado terminaría, directa o indirectamente, influyendo en decisiones sobre personas. El proyecto además no dispone de datos reales y no debe obtenerlos.

## Decisión

El machine learning en esta plataforma predice **el comportamiento del proceso**, nunca a las personas.

**Ámbito permitido:** riesgo de demora de una convocatoria, probabilidad de que una etapa se atasque, carga de trabajo esperada y volumen de postulaciones previsto. La unidad de análisis es la convocatoria o la etapa.

**Prohibido sin excepción:** puntuar, ordenar, recomendar, filtrar, preseleccionar o descartar postulantes; predecir desempeño, idoneidad, permanencia, personalidad o "ajuste cultural"; usar atributos sensibles o sus aproximaciones; alimentar o alterar el ranking de RF-20 a RF-22; intervenir en la decisión de RF-23 a RF-25.

**Arquitectura:** Laravel es el sistema de registro. El servicio de inferencia, si existe, es opcional, sin estado, sin acceso a la base de datos principal y sin conocimiento del dominio; recibe características anonimizadas y devuelve un valor con su incertidumbre. Laravel funciona completo si el servicio no responde.

**Datos:** únicamente sintéticos y rotulados como tales.

## Alternativas consideradas

1. **Modelo de recomendación de candidatos.** Rechazada: contradice el contrato de no decisión automática, introduce riesgo de discriminación y no es defendible éticamente en un contexto educativo.
2. **Puntuación asistida "solo como sugerencia".** Rechazada: una sugerencia visible junto al ranking condiciona la decisión humana; el efecto práctico es el mismo que decidir.
3. **Sin machine learning.** Sigue siendo una opción válida y es el resultado por defecto si no se superan los criterios de no-go.

## Consecuencias

**Positivas:** el proyecto puede demostrar competencia en ML sin comprometer a las personas del caso de estudio; la frontera es explicable y defendible en la sustentación; el sistema no adquiere dependencia operativa del modelo.

**Negativas:** el ámbito permitido es menos vistoso que una recomendación de candidatos, y con datos sintéticos las métricas demuestran método, no eficacia real. Ambas cosas se declaran abiertamente en el informe.

**Aplicación:** la skill `ml-risk-service` y el estudio `../ml-feasibility.md`. Relacionada con [ADR-002](ADR-002-human-oversight.md).
