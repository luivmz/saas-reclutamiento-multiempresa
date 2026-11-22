# ML-02 — Plan de entrenamiento y evaluación

> **PROPUESTA — NO VIGENTE.** Documento del 07/11/2026, en la rama local `feature/entrega-academica-demo`. Es preparación de F37-SBX y F38-SBX, que siguen **BLOQUEADAS** (F36-SBX-GATE = NO SUPERADO). No entrena, no implementa y no ejecuta nada. Desarrolla el [plan de evaluación](../F36SBX_Plan_Evaluacion.md) del paquete, sin sustituirlo.

## 1. Qué es ML-02 y qué no es

ML-02 es la línea de **ayudas sobre la evidencia** de un expediente sintético para un evaluador humano: organizar, localizar y trazar evidencia frente a criterios explícitos (charter §3). No es un modelo sobre personas.

| Sí (diseño hoy; F37-SBX-A, si se autoriza) | Nunca, en ningún ciclo de este proyecto |
|---|---|
| EI-01 a EI-07: deterministas, sin modelo, alcance B | Puntuar, ordenar, recomendar o seleccionar personas (EI-19) |
| EI-09, recuperación léxica BM25 de fragmentos, solo si se confirma F36-M02 | Resumir o juzgar a un postulante, ni sugerir niveles (EI-13, EI-14) |
| — | LLM sobre la evidencia, OCR, similitud entre candidatos (EI-15, EI-16, EI-18) |
| — | Audio, vídeo o voz, también sintéticos; emociones o personalidad (EI-20, EI-21) |
| — | **Entrenar o ajustar modelos con evidencia (EI-22)** |
| — | Datos reales, UI productiva o salidas hacia RF-21, RF-23 o RF-29 (EI-23) |

## 2. Entrenamiento: no hay en este ciclo

**ML-02 no se entrena.** EI-22 está BLOCKED: no hay etiquetas válidas y el resultado sería un modelo sobre personas. No hay, por tanto, ni conjunto de entrenamiento, ni ajuste, ni *checkpoint*.

| Capacidad | ¿Necesita entrenamiento? | Qué la sustituye |
|---|---|---|
| EI-01 a EI-07 | No: reglas deterministas | Pruebas con oráculo exacto (M-01 a M-06) |
| EI-09 (BM25) | No: los estadísticos del corpus se calculan, no se aprenden con etiquetas | Parámetros `k1` y `b` fijados en el preregistro, sin ajustarlos sobre `test` |
| EI-10 (embeddings, alcance C) | No se entrenaría: modelo local preentrenado, fijado por hash | Exige un ADR sucesor APROBADO por los tres integrantes y la auditoría contrafactual EI-24 |

Si algún día se planteara entrenar algo, haría falta lo mismo que en ML-01 para un experimento nuevo: una decisión expresa del equipo, un protocolo, un preregistro y una auditoría. Además, EI-22 tendría que dejar de estar BLOCKED mediante un ADR propio. Este plan no lo anticipa.

## 3. Datos de evaluación (solo sintéticos)

- **Corpus.** Lo genera un generador determinista con plantillas y semilla, según el [contrato de evidencia](../F36SBX_Contrato_Evidencia.md). No se usa un LLM (EI-17).
- **Particiones.** `dev` y `test` sellado, con su SHA-256 publicado en el preregistro antes de abrir `test`.
- **Casos sembrados.**
  - Requisitos sin evidencia, para M-02.
  - Enlaces rotos y versiones de criterio cambiadas, para M-03.
  - PII ficticia evidente, para M-05.
  - Casos adversariales e inyecciones, para R-01 y R-05.
- **Guardia de entrada (EI-05).** Ningún artefacto con un patrón de PII entra al corpus.

## 4. Métricas y umbrales

| Fase | Capacidades | Métricas | Umbral de aceptación |
|---|---|---|---|
| F37-SBX-A, etapa 1 | EI-01 a EI-07 | M-01 a M-06, M-11 y M-12 | 100 %: son deterministas, y cualquier diferencia es un defecto |
| F37-SBX-A, etapa 2 (con F36-M02) | EI-09 | M-07 por estrato, M-08, M-11, M-12, R-01 a R-05 | Se fijan en el preregistro, antes de ver `test` |
| F37-SBX-B (alcance C, ADR aprobado) | EI-08, EI-10 a EI-12, EI-24 | M-07 a M-10 y M-13 | EI-10 solo se acepta si supera a BM25 por el margen declarado |
| Siempre | Toda salida | Ninguna puntuación sobre personas, ninguna salida hacia RF-21 o RF-23 | Una sola violación invalida el resultado |

## 5. Protocolo

1. Preregistro: hipótesis, métricas, umbrales, semilla, SHA-256 de `test` y criterios de parada.
2. RED: pruebas con oráculo que fallan sin la implementación.
3. Implementación mínima, sin dependencias nuevas en alcance B.
4. Evaluación en `dev`; `test` se abre una sola vez.
5. Manifiesto con los hashes de entrada y salida, y dos ejecuciones idénticas (R-04).
6. Auditoría independiente y gate sucesor propio de F37-SBX.

## 6. Qué demuestra hoy el prototipo

El [prototipo navegable](index.html) muestra **cómo se vería** cada ayuda de EI-01 a EI-07 sobre un expediente sintético, con resultados escritos a mano como ejemplos de diseño. No calcula nada, no tiene modelo y no está conectado al SaaS. Sirve para discutir el diseño y la experiencia del evaluador, no para medir métricas.
