# Capítulo 2. Contexto y problema

## 2.1 Contexto

El Colegio Andino de Huancayo es el caso de estudio del proyecto. Sobre él **no hay documentación institucional verificada en el repositorio**: no se incluyen estadísticas de contratación, número de postulantes, herramientas actuales ni organigrama. Por eso este capítulo:

- describe el problema como **análisis AS-IS preliminar** del equipo, pendiente de validación con RR. HH./Administración del colegio;
- no afirma canales, formatos ni herramientas concretas que use hoy la institución;
- vincula cada problema con los requerimientos (RF) diseñados para atenderlo.

El proceso analizado va desde que un área detecta una necesidad de personal hasta que se comunica el resultado final a los postulantes. Participan el área solicitante, Recursos Humanos, la Dirección (aprobación y decisión), los evaluadores y los postulantes.

## 2.2 Problemas identificados (AS-IS preliminar)

Los cinco problemas provienen del análisis previo del equipo. El documento fuente de ese análisis (entregable de identificación de problemas) **no está incluido en el repositorio**; ver [evidence-index.md](evidence-index.md).

| # | Problema | Descripción (AS-IS preliminar) | Efecto esperado | Validación |
|---|---|---|---|---|
| P1 | Información distribuida | Los datos del proceso (requerimiento, perfil del puesto, CV, evaluaciones y decisiones) no están centralizados en un único registro por convocatoria. | Dificultad para reconstruir el expediente y riesgo de pérdida o duplicación de información. | Pendiente con RR. HH. |
| P2 | Seguimiento manual | El avance de cada requerimiento y postulación se controla sin estados ni historial sistematizados. | Poca visibilidad del estado del proceso y de quién hizo cada cambio. | Pendiente con RR. HH. |
| P3 | Evaluaciones heterogéneas | Los candidatos no se evalúan con criterios, ponderaciones y rangos definidos de antemano y comunes a toda la convocatoria. | Comparaciones poco objetivas y difíciles de justificar. | Pendiente con RR. HH./Dirección |
| P4 | Comunicación manual | Los avisos a postulantes y participantes (recepción, cambios de etapa, convocatorias, resultado) dependen de gestiones manuales. | Demoras u omisiones en la comunicación. | Pendiente con RR. HH. |
| P5 | Indicadores limitados | No se dispone de información consolidada para comparar candidatos ni de trazabilidad de las acciones críticas. | Decisiones con menos sustento y baja capacidad de auditoría. | Pendiente con Dirección |

## 2.3 Relación problema → solución implementada

| Problema | RF que lo atienden | Qué quedó implementado |
|---|---|---|
| P1 | RF-01, RF-05, RF-06, RF-09, RF-10, RF-12 | Requerimiento, vacante con perfil y criterios, perfil del postulante con CV privado y expediente de postulación, todo por organización |
| P2 | RF-02, RF-03, RF-13, RF-14, RF-24, RF-25 | Máquinas de estado del requerimiento y de la postulación, con historial (quién, cuándo, de qué estado a cuál) |
| P3 | RF-05, RF-16 a RF-22 | Criterios con ponderación y rango por vacante, hojas de puntaje validadas, ranking ponderado explicable y comparación |
| P4 | RF-04, RF-11, RF-15, RF-17, RF-26 | Notificaciones automáticas (base de datos y correo con *driver* `log`) sin datos confidenciales |
| P5 | RF-21, RF-22, RF-23, RF-27 | Ranking y comparación como apoyo a la decisión humana, y auditoría de solo lectura para Dirección |

**Límite honesto sobre P5.** No se implementaron tableros de indicadores de gestión (tiempos del proceso, embudo de postulaciones ni estadísticas por periodo). P5 se atiende con la comparación de candidatos y la auditoría. Los indicadores de gestión quedan como recomendación (capítulo 14).

## 2.4 Objetivos del proyecto

**Objetivo general.** Analizar, diseñar, implementar y verificar una plataforma SaaS multiempresa para gestionar el reclutamiento, la evaluación y la selección de personal, tomando como caso de estudio al Colegio Andino de Huancayo, con evidencia verificable de calidad.

**Objetivos específicos y resultado alcanzado:**

| # | Objetivo específico | Resultado alcanzado |
|---|---|---|
| OE1 | Modelar el proceso AS-IS preliminar y el TO-BE propuesto | Capítulo 3 (el BPMN formal está pendiente de anexar) |
| OE2 | Definir y trazar la línea base de requerimientos | 27 RF trazados a código y pruebas ([traceability-master.md](traceability-master.md)) |
| OE3 | Implementar una arquitectura multiempresa segura y mantenible | Monolito modular con `organization_id`, Policies y auditoría (capítulos 6 y 7) |
| OE4 | Asegurar la calidad con TDD, pruebas automatizadas y gestión de defectos | 244 pruebas PHPUnit, 43 tests Cypress y 13 defectos corregidos (capítulos 11 a 13) |
| OE5 | Garantizar la portabilidad y reproducibilidad del entorno | Docker Compose validado desde un clon limpio (capítulo 10) |
