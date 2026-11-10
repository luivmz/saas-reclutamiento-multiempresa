# F38 · ML-02: conjunto sintético, resultados esperados y criterios de evaluación

> **PREPARACIÓN — SIN MÉTODO, SIN ENTRENAMIENTO Y SIN PROCESAR EVIDENCIA.** Documento del 08/11/2026, en la rama local `feature/continuacion-f36-f40`. Desarrolla el [plan de ML-02](../f36-sbx/prototipo-ml02/F36SBX_ML02_Plan_Entrenamiento_Evaluacion.md) y el [plan de evaluación del paquete](../f36-sbx/F36SBX_Plan_Evaluacion.md), sin sustituirlos. F37-SBX y F38-SBX siguen **BLOQUEADAS** (F36-SBX-GATE = NO SUPERADO). EI-22 (entrenar con evidencia) y EI-23 (integración productiva) están **BLOCKED**.
>
> **La decisión de selección es de Dirección** (RF-23). Ninguna ayuda de ML-02 puntúa, ordena, recomienda ni descarta personas. Las métricas miden métodos contra un oráculo sintético, nunca a personas.

## 1. Qué se evalúa

| Ayuda | Clase | Métrica | Estado de la evaluación |
|---|---|---|---|
| EI-01 y EI-06: organizar por tipo, criterio y fuente declarados | ALLOWED | M-01 | Oro y métrica listos |
| EI-02: alerta de proceso «requisito no evidenciado» | ALLOWED | M-02 | Oro y métrica listos |
| EI-03: integridad del enlace evidencia → criterio | ALLOWED | M-03 | Oro, con fallos sembrados, y métrica listos |
| EI-04: desglose con orden fijo por identificador | ALLOWED | M-04 | Oro, con permutaciones, y métrica listos |
| EI-05: guardia de PII | ALLOWED | M-05 | Oro, con PII ficticia sembrada, y métrica listos |
| EI-07: búsqueda léxica dentro de una postulación | ALLOWED | M-06 | Oro y métrica listos |
| EI-09: recuperación léxica ponderada de fragmentos | **CONDITIONAL** (F36-M02 pendiente) | M-07 y M-08 | Solo especificada: oro y métricas sin umbral |
| Toda salida | — | M-11 (atribución) y M-12 (sin texto libre) | Listas; además invalidan el resultado |

Fuera de la evaluación, porque están BLOCKED: resúmenes, veredictos o niveles sobre personas, LLM, OCR, audio, similitud entre candidatos y entrenamiento (EI-13 a EI-22).

## 2. Conjunto sintético

[`conjunto/ml02_casos_sinteticos.json`](conjunto/ml02_casos_sinteticos.json), escrito a mano, sin LLM (EI-17):

- **2 vacantes**: `VAC-ML-01` en `dev` y `VAC-ML-02` en `test`. La unidad de partición es la vacante. No hay `train` (contrato v4: `train_allowed = false`).
- **4 postulaciones** y **12 fragmentos**. Todo texto empieza por `[SINTÉTICO]`.
- **Sello de `test`:** `fb7e7e13f664f93ca9e6fb7cf824a097469034d6096659e980e928d4df3eee72`. Es el SHA-256 de la etiqueta `f38-ml02-test-seal-v1` y de la proyección canónica de `test`: vacantes, postulaciones, fragmentos, casos y el parámetro `k` de EI-09, que es compartido y cambia las métricas de `test`. El arnés se niega a evaluar `test` si el sello no coincide. Cambiar los casos de `dev` no altera el sello.

| Tarea | Casos en `dev` | Casos en `test` | Qué se sembró |
|---|---|---|---|
| EI-01 | 3 | 2 | Grupos `tipo\|criterio\|fuente` declarados |
| EI-02 | 2 alertas esperadas | 2 alertas esperadas | Un requisito sin evidencia por postulación |
| EI-03 | 4 enlaces, 2 rotos | 2 enlaces, 1 roto | Cita inexistente (`LNK-03`), versión de criterio cambiada (`LNK-04`) y fragmento de otra postulación (`LNK-06`) |
| EI-04 | 2 permutaciones | — | El orden esperado es el de los identificadores |
| EI-05 | 2 con PII, 1 limpio | 2 con PII, 1 limpio | Correo `.test`, teléfono `900000000`, documento `00000000` y URL `.test`, todos ficticios |
| EI-07 | 3 consultas | 1 consulta | Token normalizado (con mayúsculas y tilde), subcadena y una consulta sin resultados |
| EI-09 | 4 pares relevantes y 1 no relevante, en 3 consultas; 1 caso sin evidencia | 2 pares relevantes en 2 consultas; 1 caso sin evidencia | Estratos `alto`, `medio` y `nulo` |

**No sirve para estimar el rendimiento de ningún método:** es demasiado pequeño. Fija el formato, el oro, las métricas y el arnés. El tamaño real lo calcula el contrato (§3.5: unos 385 pares relevantes por estrato).

## 3. Resultados esperados

El oro de cada tarea está en el JSON: `expected_group`, `expected_alerts`, `expected_broken`, `expected_order`, `expected` (`rechazo` o `admision`), `expected_fragments` y las anotaciones de relevancia. Las etiquetas de EI-09 son de **pares fragmento-criterio** (`relevante` o `no_relevante`), nunca de personas.

## 4. Métricas y criterios de aceptación

| ID | Fórmula | Umbral (plan §2) |
|---|---|---|
| M-01 | Aciertos de grupo ÷ casos | 1,0 |
| M-02 | Precisión y exhaustividad del conjunto de alertas | 1,0 y 1,0 |
| M-03 | Enlaces rotos detectados ÷ rotos sembrados, y falsos positivos | 1,0 y 0 |
| M-04 | Todas las permutaciones dan el orden esperado | Sí (1,0) |
| M-05 | Casos con PII rechazados ÷ casos con PII; además, rechazos de casos limpios | 1,0; los rechazos de casos limpios se informan |
| M-06 | Consultas con el conjunto exacto de fragmentos ÷ consultas | 1,0 |
| M-07 | Recall@k, Precision@k, MRR y nDCG@k (k = 3), con media por consulta; recall por estrato; intervalo bootstrap al 95 % por vacante (semilla 2381, 2000 réplicas) | **Sin umbral**: se fija en el preregistro, antes de abrir `test` |
| M-08 | Abstenciones correctas ÷ casos sin evidencia; además, abstenciones falsas | 1,0 |
| M-11 | Citas cuyo fragmento existe y es de la misma postulación ÷ citas | 1,0; un fallo invalida el resultado |
| M-12 | Valores de texto libre o claves no admitidas en la salida | 0; uno solo invalida el resultado |

**Invalidan el resultado entero:** una clave con un token prohibido del contrato v4 (`score`, `rank`, `select`…), también en camelCase; texto libre o un valor numérico; una cita sin atribución válida; una salida de otro conjunto; un sello de `test` que no coincide. **Se rechazan sin calcular métricas:** una tarea fuera del catálogo (EI-01 a EI-05, EI-07 y EI-09), una salida mal formada (también una raíz JSON que no sea un objeto), una lista de recuperación con identificadores repetidos y cualquier partición distinta de `dev` y `test`, incluida `train`.

## 5. Salidas de referencia y valores calculados a mano

Ninguna de las dos salidas la produce un método: están escritas a mano para comprobar el arnés.

- [`salida_perfecta.json`](conjunto/salidas_de_referencia/salida_perfecta.json) cumple todos los umbrales en `dev` y en `test`.
- [`salida_degradada.json`](conjunto/salidas_de_referencia/salida_degradada.json) siembra un error por tarea, solo en `dev`.

Estos son los valores de la salida degradada en `dev`, calculados antes de ejecutar el arnés. Las pruebas los fijan.

| Métrica | Valor | Por qué |
|---|---|---|
| M-01 | 2/3 | `FRG-004` con el criterio cambiado |
| M-02 | precisión 0,5 y exhaustividad 0,5 | Una alerta falsa (`APP-ML-001`, `REQ-01-TIT`) y una omitida |
| M-03 | detección 0,5 y 1 falso positivo | Marca `LNK-02`, que está bien, y omite `LNK-04` |
| M-04 | 0 | La permutación `P-2` sale invertida |
| M-05 | 0,5 y 1 rechazo falso | Admite `PII-02` y rechaza `PII-05` |
| M-06 | 2/3 | `Q-01` devuelve un fragmento de más |
| M-07 | Recall@3 = 0,5; P@3 = 2/9; MRR = 0,5; nDCG@3 = (0,3869 + 1 + 0) ÷ 3; recall por estrato: `alto` 1, `medio` 0, `nulo` 0; intervalo «no informativo», con 1 vacante | Una consulta con el relevante en la posición 2, otra perfecta y otra sin salida |
| M-08 | 0 | No se abstiene en el caso sin evidencia |
| M-11 y M-12 | 1,0 y 0 | La salida es válida: el arnés no la rechaza, solo no la acepta |

## 6. Cómo se comprobarían los resultados de un método

Este protocolo se aplicará cuando exista un método autorizado, en F37-SBX-A:

1. **Preregistro** en el repositorio, antes de ejecutar nada: hipótesis, umbral de M-07, `k`, semilla, sello de `test` y criterios de parada. El sello de esta versión ya está fijado.
2. **RED:** el arnés rechaza una salida vacía.
3. **Ejecución en `dev`**, con el arnés, tantas veces como haga falta. **`test` se abre una sola vez**, y el arnés comprueba el sello.
4. **Validez:** una sola invalidación anula el resultado (§4).
5. **Reproducibilidad (R-04):** dos ejecuciones con el mismo SHA-256 de salida.
6. **Línea base:** EI-09 se compara con la regla más simple, la búsqueda exacta de EI-07 (plan §1.3).
7. **Robustez, latencia, memoria e inyección (R-01, R-02, R-03 y R-05):** fuera del arnés, en la PC declarada.
8. **Auditoría independiente** y gate sucesor propio de F37-SBX.

```
python -I -B docs/academico/preparacion-f38-ml02/evaluacion/f38_evaluar.py <salida.json> --particion dev
python -I -B docs/academico/preparacion-f38-ml02/evaluacion/f38_evaluar.py --sello
python -I -B -m unittest discover -s docs/academico/preparacion-f38-ml02/evaluacion -v
```

## 7. Datos, etiquetas y particiones que exigiría un entrenamiento

**Hoy no se puede entrenar.** EI-22 está BLOCKED, y la matriz dice que «una autorización sandbox sucesora no tiene autoridad para habilitarla». El contrato v4 prohíbe la partición `train` (`train_allowed = false`). Ninguna ayuda ALLOWED (EI-01 a EI-07) necesita entrenamiento, y EI-09 (BM25) tampoco: sus estadísticos se calculan, no se aprenden con etiquetas.

Si algún día se planteara entrenar, por ejemplo un reordenador de fragmentos o el ajuste de un modelo local de EI-10, esto es lo mínimo que exigiría. Se especifica para que la decisión sea informada, **no para anticiparla**:

| Elemento | Especificación |
|---|---|
| Unidad de dato | Par (fragmento, criterio) de una postulación sintética. **Nunca** una persona, una postulación entera ni un resultado del proceso |
| Etiqueta | Relevancia binaria del fragmento para el criterio, sin puntaje ni nivel. **Prohibidas** las etiquetas de idoneidad, contratación, ranking o resultado de RF-21, RF-23 o RF-29 |
| Anotación | Dos anotadores independientes de la misma organización sintética. Acuerdo medido antes de usar el oro (kappa de Cohen ≥ 0,8 como propuesta) y adjudicación documentada |
| Generación | Plantillas con semilla y estratos `alto`, `medio` y `nulo` de solapamiento léxico (contrato §3.5); sin LLM (EI-17) |
| Particiones | `train`, `dev` y `test` por (`template_family`, `vacancy_token`): ninguna familia ni vacante en dos particiones. Embargo temporal de F34 (`process_splits`). `test` sellado antes de cualquier ejecución |
| Tamaño | `test`: unos 385 pares relevantes por estrato, para una semiamplitud de 0,05. `train`: a justificar en el preregistro, con una curva de aprendizaje en `dev` |
| Fugas | Mismas comprobaciones que REL-05 y REL-11 del contrato, más la prohibición de que un fragmento o su variante contrafactual crucen particiones |
| Equidad | Pares contrafactuales (EI-24) con marcadores de grupo sintéticos, solo para auditar. El grupo nunca es feature |
| Comprobación | Este arnés, sobre `test` sellado, contra la línea base sin entrenamiento: el modelo entrenado solo se acepta si la supera por un margen preregistrado, con el intervalo bootstrap por vacante |

**Requisito exacto para habilitarlo:**

1. Reclasificar EI-22 mediante un incremento auditado del validador, porque la regla CAP fija la clase de cada EI.
2. Una versión 5 del contrato que admita `train`.
3. Un ADR sucesor aprobado por los tres integrantes.
4. Como la matriz excluye esta capacidad de cualquier autorización sandbox, una decisión fuera del sandbox: la G0 real y el nivel N5 del roadmap.

Hoy no hay una vía para hacerlo dentro de F37-SBX.

## 8. Estado por pieza

| Pieza | Estado | Requisito de lo pendiente |
|---|---|---|
| Conjunto sintético, oro y sello | **Preparado** y probado | — |
| Arnés de métricas (M-01 a M-08, M-11 y M-12), con sus invalidaciones | **Implementado** fuera del SaaS. 28 pruebas; 5 ablaciones detectadas el 08/11/2026 | — |
| Salidas de referencia escritas a mano | **Preparadas** | — |
| Métodos de EI-01 a EI-07 | **Pendientes** | F36-SBX-GATE SUPERADO anclado en H, con FG-03 que liste esas EI (S §7) |
| EI-09 y su umbral de M-07 | **Pendientes** | F36-M02 confirmada por actos auténticos, FG-12 y el preregistro |
| Entrenamiento | **Bloqueado** | §7 |
| Integración en el SaaS | **Bloqueada** (EI-23) | La G0 real y la decisión N5 |

## 9. Puntos para la auditoría

1. Que el arnés no contenga ningún método. Solo compara una salida dada con el oro.
2. Que los valores de §5 se puedan recalcular a mano a partir del JSON.
3. Que el sello cubra todo `test` y nada de `dev`.
4. Que §7 especifique sin habilitar, y que su requisito sea el exacto.
5. Que ninguna etiqueta, métrica o salida se refiera a personas.
