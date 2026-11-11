# Resultados · EXP-BM25-LEXICO-v1 (experimental)

> **EXPERIMENTAL.** Rama local `exp/evidencias-ml02`. La evaluación usa el arnés F38 sin cambios.
>
> - **Qué no es.** No es la evaluación de F37-SBX-A, y EI-09 sigue CONDITIONAL.
> - **Preregistro.** [`PREREGISTRO_EXP-BM25-LEXICO-v1.md`](../preregistro/PREREGISTRO_EXP-BM25-LEXICO-v1.md), versionado en `e3f80a157af8c56e0d89bff997d3c7e26f68722a` antes de ejecutar nada. `test` se abrió una sola vez con ese commit.

## 1. Qué se ejecutó

```
php artisan ml02:evaluar --particion=<dev|test> --metodo=<bm25|exacta> --salida=storage/app/ml02/<archivo>.json
python -I -B docs/academico/preparacion-f38-ml02/evaluacion/f38_evaluar.py <salida.json> --particion <dev|test>
```

- **Código.** El comando ejecuta las mismas clases que la página de evidencias: `TextAnalyzer`, `Bm25Retriever` y `LexicalSearch`.
- **Reproducibilidad.** Dos ejecuciones sobre `dev` dieron el mismo SHA-256 de salida: `b8fa206c…a54cf6`.
- **Sello de `test`.** Coincide: `fb7e7e13…eee72`.
- **Archivos de esta carpeta.**
  - `salida_*.json`: lo que produjo cada método.
  - `resultado_*.json`: lo que calculó el arnés.

## 2. Métricas

| | `dev` BM25 | `dev` línea base | `test` BM25 | `test` línea base |
|---|---|---|---|---|
| Válida (M-11 = 1, M-12 = 0) | Sí | Sí | Sí | Sí |
| M-06, búsqueda exacta (EI-07) | 1,0 | 1,0 | 1,0 | 1,0 |
| M-07 Recall@3 | 0,5 | 0,5 | **0,0** | 0,0 |
| M-07 P@3 · MRR · nDCG@3 | 0,22 · 0,67 · 0,54 | Iguales | 0 · 0 · 0 | Iguales |
| Recall por estrato | alto 1,0 · medio 0 · nulo 0 | Igual | medio 0 · nulo 0 | Igual |
| M-08, abstención correcta · abstenciones falsas | 1,0 · 1 | 1,0 · 1 | 1,0 · 2 | 1,0 · 2 |
| Intervalo bootstrap | No informativo (1 vacante) | — | No informativo (1 vacante) | — |

**Contra el preregistro:**

- **H1 se cumple, pero solo por empate.** BM25 rinde igual que la línea base en las dos particiones: en este conjunto, cada criterio comparte como mucho una palabra con cada fragmento.
- **H2 se rechaza.** El Recall@3 de `test` es 0,0, por debajo del umbral de 0,5.
- **El resultado coincide con la predicción escrita.**
- **Criterios de aceptación de M-01 a M-05.** El arnés los marca como no cumplidos porque este método no produce EI-01 a EI-05: están fuera de su alcance.

## 3. Ejemplos

**Acertados:**

| Partición | Postulación · criterio | Devuelve | Por qué |
|---|---|---|---|
| dev | APP-ML-001 · «Planificación de la enseñanza» | FRG-002, «Elaboró la planificación anual y las unidades didácticas del área.» | Comparte «planificación» (estrato alto) |
| dev | APP-ML-001 · «Conducción de la clase» | FRG-004, «Inició la clase modelo presentando los objetivos.» | Comparte «clase» (alto) |
| dev | APP-ML-001 · «Planificación de la enseñanza» | No devuelve FRG-004 | Es el par anotado como no relevante |
| dev / test | APP-ML-002 · Planificación; APP-ML-004 · «Atención a familias» | Abstención | Son los casos sin evidencia (M-08) |
| dev / test | Q-01 a Q-04 (EI-07) | El conjunto exacto | También la consulta sin resultados (Q-03) |

**Fallidos:**

| Partición | Postulación · criterio | Relevante no recuperado | Por qué falla |
|---|---|---|---|
| dev | APP-ML-001 · Planificación | FRG-003, «Organizó la secuencia de actividades con metas por sesión.» | Estrato nulo: es relevante pero no comparte ninguna palabra |
| dev | APP-ML-002 · «Conducción de la clase» | FRG-007, «Respondió las preguntas del grupo con ejemplos cotidianos.» | Estrato medio: la relación es de sentido, no de palabras. Abstención falsa |
| test | APP-ML-003 · «Gestión documental» | FRG-009, «Ordenó y digitalizó el archivo de matrículas del colegio.» | Nulo. Abstención falsa |
| test | APP-ML-003 · «Atención a familias» | FRG-010, «Explicó con calma un trámite a un apoderado ficticio.» | Medio. Abstención falsa |

## 4. Lectura

- **Qué hace bien.** La recuperación léxica encuentra lo que comparte palabras con el criterio, muestra la fuente de cada fragmento y se abstiene cuando no hay coincidencias.
- **Qué no ve.** No ve las paráfrasis, que en este conjunto son la mitad de los pares relevantes.
- **Cómo lo dice la pantalla.** Muestra la abstención como «Eso no significa que el criterio no se cumpla». Así una ausencia de palabras no pasa por un juicio sobre la persona.
- **Siguiente paso.** Mejorar esto sin salir de lo léxico exigiría descriptores del criterio escritos por personas, un método nuevo y otro preregistro. Los métodos semánticos (embeddings) siguen fuera de la matriz F36-SBX.
- **Tamaño del conjunto.** Con 12 fragmentos y una vacante por partición, ninguna cifra estima el rendimiento: el intervalo es «no informativo» (F38 §2).
