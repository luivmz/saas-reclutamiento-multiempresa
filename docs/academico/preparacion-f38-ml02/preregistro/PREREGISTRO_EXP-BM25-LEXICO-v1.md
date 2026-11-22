# Preregistro · EXP-BM25-LEXICO-v1 (experimental)

> **EXPERIMENTAL — rama local `exp/evidencias-ml02`.**
>
> - **Qué no es.** No es el preregistro de F37-SBX-A que pide F38 §6. Ese preregistro exige F36-SBX-GATE SUPERADO y FG-03.
> - **Estado de EI-09.** EI-09 sigue CONDITIONAL, con F36-M02 pendiente.
> - **Efecto.** No habilita ninguna capacidad ni cambia ningún estado. F37-SBX y F38-SBX siguen BLOQUEADAS.
>
> Se versiona en el mismo commit que el método, **antes** de ejecutar el método sobre `dev` o `test`.

## 1. Método que se ejecuta

Son las clases `App\Services\Ml02\TextAnalyzer`, `Bm25Retriever` y `LexicalSearch`, las mismas que usa la página de evidencias. El comando `php artisan ml02:evaluar` las ejecuta sobre el conjunto F38.

| Pieza | Definición fija |
|---|---|
| Análisis | Quita `[SINTÉTICO]`, pasa a minúsculas, quita tildes (`ñ`→`n`) y parte por lo que no es letra ni dígito. Elimina una lista fija de 51 palabras vacías y recorta sufijos de forma ligera: `-es` (5+ letras) o `-s` (4+) y después una `a`, `e` u `o` final (4+) |
| EI-09 | BM25 con k1 = 1,2 y b = 0,75, e idf = ln(1 + (N − n + 0,5) / (n + 0,5)). La consulta es el texto del criterio. Las estadísticas salen **solo de los fragmentos de la misma postulación**. Devuelve hasta k = 3 fragmentos que comparten algún término; en un empate, decide el identificador. **Se abstiene** si ninguno comparte términos |
| EI-07 | Búsqueda exacta de F38: `token_normalizado` y `subcadena` |
| Línea base de EI-09 | `EXP-LINEA-BASE-EXACTA-v1`: fragmentos con alguna palabra no vacía del criterio, sin recortar, en orden de identificador, hasta k = 3 (F38 §6.6) |
| Entrenamiento | Ninguno. No hay pesos aprendidos ni partición `train` (EI-22 BLOCKED) |

## 2. Hipótesis, umbrales y parada

- **H1.** En `dev` y en `test`, el Recall@3 medio (M-07) de BM25 es **mayor o igual** que el de la línea base.
- **H2, umbral de aceptación de M-07.** Recall@3 medio ≥ 0,5 en `test`.
- **Resto de umbrales, los de F38 §4:**
  - M-06 = 1,0;
  - abstención correcta (M-08) = 1,0;
  - M-11 = 1,0;
  - M-12 = 0.
- **Parámetros.** k = 3. Semilla del bootstrap: 2381, la del arnés. Sello de `test`: `fb7e7e13f664f93ca9e6fb7cf824a097469034d6096659e980e928d4df3eee72`.
- **Parada.**
  - `test` se abre una sola vez, con el método de este commit.
  - Cualquier cambio posterior del método lleva un `method_id` nuevo y otro preregistro.
  - Los resultados de v1 se conservan tal como salgan.

## 3. Contaminación declarada y predicción

**Contaminación.** El conjunto entero está en el repositorio, también `test` con su oro, y quien diseñó el método lo leyó antes. El análisis no se ajustó caso por caso, pero **`test` no es una evaluación ciega**.

**Predicción, escrita antes de ejecutar:**

- **Fallos esperados.** BM25 no recupera los pares de estrato `nulo` ni los `medio` que no comparten palabras con el criterio: FRG-003 y FRG-007 en `dev`, FRG-009 y FRG-010 en `test`.
- **`dev`.** Recall@3 ≈ 0,5, con una abstención falsa (APP-ML-002 / CRI-01-CLASE).
- **`test`.** Recall@3 = 0, así que H2 se rechazaría. Las abstenciones correctas serían 1,0 en las dos particiones.
- **Línea base.** Debería empatar con BM25 en este conjunto, porque cada criterio comparte como mucho una palabra con cada fragmento.

El conjunto tiene 12 fragmentos y **no sirve para estimar el rendimiento** (F38 §2). Esta ejecución comprueba el formato, la reproducibilidad y el comportamiento de abstención. No dice si el método es útil.
