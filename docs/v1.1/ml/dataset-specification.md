# Especificación del dataset sintético

**Fase 14 · 20 de septiembre de 2026**

**[LIMITACIÓN] No existe ningún dataset.** Este documento especifica cómo debe generarse en la Fase 15. En la Fase 14 no se creó ningún archivo de datos, script, notebook ni dependencia.

> **[APROBADA] Decisión 4 del equipo, 20 de septiembre de 2026.** Quedan aprobados: dataset sintético académico, 6 000 observaciones iniciales con rango de sensibilidad 5 000–10 000, al menos 36 meses sintéticos, varias organizaciones ficticias, seed `20260920`, generación *event-first*, target no determinista y datos exclusivamente ficticios. La limitación de validez sigue siendo obligatoria y explícita.

> Los datos sintéticos permiten demostrar metodología, entrenamiento, integración y evaluación técnica. No demuestran validez predictiva real sobre procesos del Colegio Andino de Huancayo ni autorizan uso institucional.

---

## 1. Escala y versionado

**[APROBADA]** *(decisión 4)*

| Parámetro | Valor por defecto | Justificación |
|---|---|---|
| Observaciones | **6 000** | Una por proceso elegible. Con prevalencia esperada de 25-40 %, el bloque de test (15 % ≈ 900 filas) contiene del orden de 225-360 positivos: suficiente para estimar precision/recall con intervalos bootstrap de ancho interpretable, sin caer en el régimen de decenas de casos donde toda métrica es ruido |
| Rango de sensibilidad | 5 000 – 10 000 | Por debajo de 5 000 el test queda demasiado fino para calibración; por encima de 10 000 el costo de generación y entrenamiento no compra precisión adicional en un trabajo académico |
| Periodo simulado | ≥ 36 meses | Permite al menos tres bloques temporales y hace observable el drift |
| Organizaciones ficticias | 4 – 8 | Simula heterogeneidad multiempresa sin que ninguna domine el dataset |
| Seed maestra | `20260920` | Centralizada, única, registrada en la configuración |
| Versión inicial | `synthetic-v1` | Toda ejecución registra versión, seed y hash de configuración |

**[LIMITACIÓN]** Ningún nombre, correo, documento ni dato del dataset puede parecerse a una persona real. Las organizaciones son ficticias y así deben rotularse en el archivo, en la documentación y en cualquier pantalla derivada.

---

## 2. Generación *event-first*

**[APROBADA]** *(decisión 4)* La generación produce **una cronología**, no una fila con una fórmula de etiqueta al final. El orden es obligatorio:

1. **Cronología base.** Fecha de solicitud → publicación → cierre de postulaciones (`closes_at`) → checkpoint. **`target_completion_at` se genera como variable operacional explícita**, fijada **antes** de la publicación y **nunca modificada** después. **[LIMITACIÓN]** Esta variable **no tiene equivalente en Laravel**: existe solo en el dataset sintético mientras `GAP-01` siga abierta. Su distribución debe ser plausible respecto de la duración típica del proceso, pero **independiente del ruido que determina el desenlace**, o el target se volvería trivial.
2. **Factores latentes**, generados y **nunca exportados**: capacidad operacional del equipo, fricción de coordinación y shock de carga del periodo. Son la causa común de que features y desenlace covaríen sin que el target sea función de las features.
3. **Dinámica del proceso.** Volumen de postulaciones, programación de evaluaciones y entrevistas, completitud, backlog y transiciones de etapa, condicionados por los latentes.
4. **Corte.** Todas las features se derivan **exclusivamente del historial truncado en `checkpoint_at`**, aplicando la regla del contrato de features.
5. **Desenlace posterior.** La duración restante hasta el cierre se genera con un proceso estocástico que depende de los latentes y del estado en el checkpoint, con ruido irreducible.
6. **Etiqueta.** `delayed` se calcula al final comparando `closed_at` contra `target_completion_at`. Nunca antes, nunca con las features.
7. **Limpieza.** Latentes, timestamps posteriores al checkpoint y cualquier columna prohibida se eliminan del dataset model-ready.

**[LIMITACIÓN]** El target no puede ser una suma determinista de las features con un umbral. Debe existir solapamiento entre clases: procesos con features casi idénticas deben terminar a veces dentro y a veces fuera de plazo. **Una exactitud casi perfecta no es un buen resultado: es la señal de que hay fuga o de que el generador es demasiado fácil**, y obliga a auditar antes de continuar.

---

## 3. Distribuciones propuestas

**[PROPUESTA]** Familias, con su razón. Los parámetros exactos se fijan en la Fase 15 y se registran en la configuración versionada.

| Magnitud | Familia | Razón |
|---|---|---|
| Duraciones (ventana de postulaciones, tiempo hasta el cierre) | Lognormal o Gamma | Positivas y asimétricas a la derecha: muchos procesos normales, algunos muy largos |
| Postulaciones recibidas | Binomial negativa | Conteo con **sobredispersión**; Poisson subestimaría la varianza real de la demanda |
| Sesiones programadas por postulación | Poisson truncada | Conteos pequeños con techo operacional |
| Plazas (`positions`) | Discreta concentrada en 1-2 | **[HECHO]** `CHECK (positions >= 1)` (`database/migrations/2026_09_13_000006_create_vacancies_table.php:39`) |
| Criterios configurados | Discreta 3-8 | Rango operacional plausible |
| Carga concurrente por organización | Proceso de llegada por periodo | Genera correlación entre procesos de la misma organización y del mismo mes |
| Días sin actividad | Mezcla: masa en valores bajos + cola larga | Distingue procesos activos de procesos estancados |
| Efecto de periodo y de organización | Efectos aleatorios de media cero | Producen drift moderado y heterogeneidad sin determinismo |
| Shocks | Evento raro (p ≈ 0.02-0.05) con impacto grande | Cola larga realista |

**[LIMITACIÓN]** Las correlaciones son **plausibles por construcción**, no causalidad institucional observada. Mayor carga concurrente puede aumentar la demora esperada; nunca debe determinarla.

---

## 4. Balance, ruido, faltantes y extremos

**[APROBADA]** *(decisión 4: target no determinista)* · **[PROPUESTA]** en los parámetros concretos

- **Prevalencia objetivo: 25 – 40 %** de `delayed = 1`. Es una decisión de simulación, **no** una estadística institucional, y así debe declararse en toda tabla que la reporte.
- **No** se fuerza 50/50 por estética. **No** se rebalancea validation ni test bajo ninguna circunstancia.
- **No** se usa SMOTE por defecto. Si alguna fase futura lo estudia, solo dentro de train, con justificación y comparación contra el modelo sin remuestreo.
- **Ruido y solapamiento** explícitos, como exige la sección 2.
- **Casos extremos obligatorios:** cero postulaciones; volumen muy alto; ninguna sesión programada; sesiones vencidas sin completar; carga concurrente máxima; periodo largo sin actividad; ventana de postulaciones mínima; `opens_at` nulo (**[HECHO]** la columna es nullable, `…000006…:22`) para ejercitar la regla de respaldo de ML-FEAT-03.
- **Faltantes:** las features del contrato **no faltan** en el dataset model-ready. Si se simulan faltantes, se hace en una capa *raw* y las reglas de exclusión o imputación se ajustan **solo con train**.

---

## 5. Validaciones que el generador deberá pasar

**[PROPUESTA]** Ninguna existe todavía. En la Fase 15 serán pruebas automatizadas, no comprobaciones manuales.

**Reproducibilidad**
1. Determinismo: misma seed y misma configuración ⇒ dataset idéntico por hash.
2. Registro de versión, seed, hash de configuración y versión del esquema en cada ejecución.

**Estructura**
3. Unicidad: un `vacancy_id` y un `checkpoint_at` por fila; sin duplicados.
4. Tipos y rangos conformes al contrato de features.
5. Ausencia total de columnas prohibidas (lista de `feature-contract.md` §3), comprobada por nombre y por contenido.

**Coherencia temporal**
6. Orden cronológico: `published_at ≤ closes_at < checkpoint_at`.
7. `target_completion_at > checkpoint_at`, fijado antes de `published_at` e **inmutable**: una prueba comprueba que el valor no cambia en ningún punto de la cronología.
8. Cero eventos posteriores al checkpoint incorporados a cualquier feature.
9. El target se calcula solo al final del pipeline.

**Invariantes de conteo**
10. `completed ≤ scheduled` en evaluaciones y entrevistas.
11. `pending = scheduled − completed`, exacta.
12. `overdue_pending ≤ pending`.

**Distribución**
13. Prevalencia dentro de la tolerancia documentada.
14. Sin correlación sospechosa feature-target (|r| por encima de un umbral declarado dispara revisión manual de fuga).
15. Cada caso extremo de §4 aparece al menos una vez.

**Censura** *(decisión 10)*
16. Los procesos sin `closed_at` al final de la ventana observacional se marcan como **censurados** y se excluyen del conjunto etiquetado. **Nunca** se les asigna `delayed = 0` ni `delayed = 1`.
17. Se reporta el número y la proporción de censurados, y se comparan sus features contra las de los incluidos: si difieren sistemáticamente, el sesgo de selección es material y debe declararse en las conclusiones.

---

## 6. Linaje

**[PROPUESTA]** Cada dataset generado produce un manifiesto con: versión, seed, hash de configuración, hash del archivo, número de filas, prevalencia por bloque temporal, versión del contrato de features, fecha y herramienta. Sin manifiesto, un resultado no es reproducible y no puede citarse en el informe académico.

## Enlaces

- [Definición del problema](problem-definition.md)
- [Contrato de features](feature-contract.md)
- [Plan de evaluación](evaluation-plan.md)
- [Índice de la Fase 14](../phase-14-ml-definition.md)
