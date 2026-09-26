# Protocolo de evaluación del modelo

Aplica solo si el equipo aprueba el servicio. Mientras tanto es material de diseño.

## 1. Dataset

- **Origen**: generado sintéticamente a partir de la estructura real del proceso (vacantes, etapas, evaluaciones, entrevistas), nunca de personas reales.
- **Rotulado**: el archivo se llama `*-synthetic.*`, su documentación empieza declarando que los datos son ficticios y toda salida derivada lo repite.
- **Unidad de análisis**: la convocatoria o la etapa, **no** el postulante.
- **Volumen mínimo**: suficiente para una partición temporal con al menos 3 periodos; si no alcanza, el resultado se declara no concluyente.

## 2. Características permitidas

Conteos, duraciones, fechas relativas y estados del proceso. Por ejemplo: número de etapas configuradas, número de postulaciones recibidas, días desde la publicación, evaluaciones programadas frente a completadas, entrevistas pendientes, número de evaluadores asignados, días hábiles restantes hasta la fecha objetivo.

Cualquier característica derivada de una persona concreta está prohibida, incluidos los promedios de puntajes de candidatos.

## 3. Prevención de fuga de información

- Ninguna característica puede haber sido registrada **después** del instante que se predice.
- Partición **temporal**: entrenamiento con procesos anteriores, prueba con posteriores. Nunca partición aleatoria.
- Un mismo proceso no puede aparecer en entrenamiento y en prueba.
- El preprocesamiento se ajusta solo con los datos de entrenamiento.
- Prueba explícita: si el modelo alcanza una exactitud sospechosamente alta, asume fuga y búscala antes de celebrar.

## 4. Línea base

| Tarea | Línea base mínima |
|---|---|
| Días de demora | media o mediana histórica por tipo de vacante |
| Etapa atascada | regla fija: "sin movimiento en N días" |
| Carga esperada | promedio del mismo periodo anterior |

El modelo solo se justifica si supera la línea base de forma clara y estable en la partición temporal.

## 5. Métricas

- **Regresión**: MAE y RMSE, con intervalo de confianza por *bootstrap*; comparación directa contra la línea base.
- **Clasificación**: AUC-PR (no solo AUC-ROC), *precision* y *recall* al umbral operativo elegido, y **calibración** mediante puntaje de Brier y diagrama de confiabilidad. Un modelo mal calibrado no se despliega aunque discrimine bien.
- **Estabilidad**: las métricas se reportan por periodo, no solo agregadas.
- Nunca se reporta una métrica que no se haya calculado en una ejecución real.

## 6. Model card

Documento breve con: propósito, unidad de análisis, datos (sintéticos), características, línea base, métricas con su partición, límites conocidos, **usos prohibidos** (la lista de la frontera), fecha y responsable.

## 7. Pruebas

`pytest` para: validación del esquema de entrada, salida siempre con `model_version`, preprocesamiento determinista, casos borde (vacante sin postulaciones, fechas invertidas, campos faltantes) y ausencia de llamadas de red. En Laravel, `Http::fake()` cubre respuesta correcta, respuesta inválida, timeout y servicio caído — este último debe demostrar que la pantalla sigue funcionando.

## 8. Criterios de no-go

El servicio **no se implementa** si se cumple cualquiera de estos:

1. El modelo no supera la línea base en la partición temporal.
2. Se detecta fuga de información que no puede eliminarse.
3. El dataset sintético no representa razonablemente el proceso y no hay forma de validarlo.
4. La calibración es mala y la estimación induciría a error.
5. El esfuerzo pone en riesgo los entregables académicos comprometidos de v1.1.
6. Alguna característica necesaria obligaría a cruzar la frontera de la sección "La frontera, primero".

Un no-go es un resultado legítimo y publicable: se documenta en `docs/v1.1/ml-feasibility.md` con la evidencia que lo sustenta.
