# F34 — Matriz de features y labels

> Fase F34, versión 1.1 (04/10/2026), corregida tras la auditoría F34. Clasifica qué variables y etiquetas serían **metodológicamente válidas** si algún día se aprueba G0. **Hoy nada se usa para entrenar:** G0 = NO APROBADA y F35–F40 siguen bloqueadas. Las fuentes [Sxx] y [Oxx] remiten a la [matriz de F30](../investigacion-ia/F30_Matriz_Evidencia_Cientifica.md).

## 1. Clasificación

| Clasificación | Significado |
|---|---|
| **PERMITIDA** | Puede usarse en reglas deterministas (alcance B) o como feature de modelos **del proceso** (alcance E) |
| **CONDICIONADA** | Solo con la condición indicada (agregada, como umbral de una regla o en un archivo separado); nunca como feature de un modelo sobre personas |
| **BLOQUEADA** | No se genera ni se usa en este ciclo |

La regla de fondo es la de F33: **ningún modelo trata a personas**. Una variable sobre una persona solo puede alimentar una regla determinista del proceso, nunca un modelo.

## 2. Features

| ID | Feature | Definición | Tipo / rango | Origen | Finalidad | Riesgo | Riesgo de leakage | Clasificación | Fase futura |
|---|---|---|---|---|---|---|---|---|---|
| FT-01 | Cumplimiento de requisito | `declared_met` y `evidence_present` por requisito | booleano (con vacíos) | Registro humano (`requirement_checks`) | Alerta CAP-01 «requisito no evidenciado» | Usarlo para filtrar o descartar (ADR-001) | Bajo | **CONDICIONADA**: solo para la alerta determinista; nunca filtra ni puntúa | F35 (B) |
| FT-02 | Años de experiencia declarados | `years_experience_declared` | entero 0–20, 8 % vacío | Declaración sintética | Comprobar el requisito de experiencia mínima | **Proxy de edad** [S42, S47] | Bajo | **CONDICIONADA**: solo la comparación con `min_years`; el valor crudo no entra a ningún modelo | F35 (B) |
| FT-03 | Número de evidencias por criterio | Conteo de evidencias `vinculada` | entero ≥ 0 | Derivado de `evidence` | Completitud (alerta de evidencia faltante) | Bajo | Bajo | **PERMITIDA** (regla de proceso) | F35 |
| FT-04 | Suficiencia documental | `evidence_sufficiency` | suficiente, parcial o insuficiente | Registro humano | Completitud y explicación | Que se lea como juicio sobre la persona | Bajo | **PERMITIDA** solo como auxiliar de QA y análisis del proceso; nunca feature de ML | F35, F37 |
| FT-05 | Niveles humanos por criterio | `human_level` | entero 1–4 | Registro humano (evaluador) | Insumo de RF-21 (existente) y del ICC | Convertirlo en etiqueta o feature de un modelo sobre personas | Alto si se usa como etiqueta | **CONDICIONADA**: solo RF-21 y ICC; prohibido en modelos | F35, F39 |
| FT-06 | Puntaje humano derivado | `rubric_points` | entero 5–20 | Rúbrica (determinista) | Fórmula A-24 del ranking | Ídem FT-05 | Alto si se usa como etiqueta | **CONDICIONADA**: solo RF-21 | — |
| FT-07 | Pesos de rúbrica | `weight` | entero 1–100; suma 100 | Configuración de RR. HH. | RF-20, RF-21 | Bajo | Ninguno | **PERMITIDA** | F35 |
| FT-08 | Tiempos del proceso | Días desde la publicación, ventana, días hasta el plazo, días sin actividad | entero | Hechos con `t <= checkpoint_at` | RF-29 (proceso) | Bajo | **Temporal** si se usan eventos posteriores (LK-02) | **PERMITIDA** (proceso) | F36 (E) |
| FT-09 | Cambios de etapa | `stage_transition_count` agregado por vacante | entero ≥ 0 | Hechos con `t <= checkpoint_at` | RF-29 | Bajo | Temporal (LK-02) | **PERMITIDA** (proceso) | F36 |
| FT-10 | Carga del proceso | Sesiones programadas, realizadas y vencidas; vacantes abiertas simultáneas | entero ≥ 0 | Hechos con `t <= checkpoint_at` | RF-29 | Bajo | Temporal (LK-02) | **PERMITIDA** (proceso) | F36 |
| FT-11 | Carga del evaluador | Sesiones abiertas por `evaluator_token` | entero ≥ 0 | Derivado de `sessions` | Planificación del proceso | Evaluar el desempeño del evaluador o identificarlo | Medio | **CONDICIONADA**: solo agregada por vacante u organización; sin identificar evaluadores | F36 |
| FT-12 | Discrepancia entre evaluadores | \|Δ nivel\| en doble calificación | entero 0–3 | Derivado de `assessments` | Alerta y calidad del proceso (ICC) | Que se lea como juicio sobre el evaluador o la persona | Bajo | **PERMITIDA** solo como auxiliar de QA, alerta e ICC; nunca feature de ML | F35, F39 |
| FT-13 | Las 15 variables RF-29 | Contrato congelado de RF-29 | enteros | `process_snapshots` | Riesgo de demora del **proceso** | Bajo | Temporal (LK-02, LK-03) | **PERMITIDA** (proceso), sin cambiar el contrato congelado | F36 |
| FT-14 | Alertas por vacante | Conteo de alertas deterministas | entero ≥ 0 | Reglas F33 | Panel del proceso | Bajo | Bajo | **PERMITIDA** (proceso) | F40 |
| FT-15 | Texto de evidencia y justificación | Texto libre | texto | Registro humano (aquí plantillas) | Explicación humana y procedencia | Dato personal en uso real; NLP es alcance C | Medio | **CONDICIONADA**: se muestra a humanos; no es feature | F35 |
| FT-16 | Fechas por persona | `submitted_at` y fechas de sesión por postulación | fecha | Sintético | Orden del proceso | *Proxy* indirecto; temporal | Medio | **CONDICIONADA**: solo agregadas por vacante | F36 |
| FT-17 | Similitud semántica | Similitud entre texto y criterio | real | — | — | Sesgo por nombre y género [S11] | — | **BLOQUEADA** (alcance C, futuro) | — |
| FT-18 | Embeddings | Vectores de texto | vector | — | — | Ídem; dato personal | — | **BLOQUEADA** | — |
| FT-19 | Atributos demográficos | Edad, sexo, etnia, nacionalidad, estado civil, discapacidad, salud | — | — | — | Discriminación; datos sensibles [O15, O09] | — | **BLOQUEADA**: no se recolectan | — |
| FT-20 | *Proxies* sensibles | Nombre, foto, dirección o distrito, colegio o universidad de procedencia, año de egreso | — | — | — | *Proxy* de atributos protegidos [S42, S48] | — | **BLOQUEADA** | — |
| FT-21 | Variables posteriores a la decisión | Seleccionado, `decided_at`, `closed_at` (y `label_known_at`), posición en el ranking | — | — | — | Leakage y reproducción de decisiones | **Target leakage** | **BLOQUEADA** como feature | — |
| FT-22 | Grupo sintético de equidad | `grupo_sintetico` (`GS-A`, `GS-B`) | categórica | Archivo separado | Pruebas metodológicas de equidad | Usarlo como feature o para decidir | — | **CONDICIONADA**: separado del feature set; nunca para scoring | F37 (método sintético) |

**Features auxiliares (FT-04 y FT-12).** `evidence_sufficiency`, `evaluator_disagreement` y sus agregados (proporción de evidencia suficiente, número o media de discrepancias por vacante, criterio o evaluador) **no alimentan ML de personas ni el modelo del proceso**. Solo sirven para control de calidad (QA), análisis del proceso, alertas deterministas y el procedimiento de ICC. No están en `process_snapshots` ni en el feature set del manifiesto (`excluded_from_features`), y la regla LK-08 lo comprueba (casos QA-43 y QA-44).

**Resumen:**

- **PERMITIDAS (9):** FT-03, FT-04, FT-07, FT-08, FT-09, FT-10, FT-12, FT-13, FT-14.
- **CONDICIONADAS (8):** FT-01, FT-02, FT-05, FT-06, FT-11, FT-15, FT-16, FT-22.
- **BLOQUEADAS (5):** FT-17 a FT-21.

## 3. Labels / targets

| ID | Label | Definición | Clasificación | Motivo |
|---|---|---|---|---|
| LB-01 | `delayed` | El cierre real supera el plazo operacional fijado antes de publicar | **VÁLIDO PARA PROCESO** | Es el target de RF-29 (ADR-004); la unidad es la vacante, no la persona |
| LB-02 | Resultado esperado de cada regla (`expected_alerts`) | Alertas que una regla determinista debe producir | **VÁLIDO PARA PROCESO** (oráculo de prueba) | Verifica reglas; no es un target de aprendizaje |
| LB-03 | Días hasta el cierre | Duración del proceso | **VÁLIDO SOLO EXPERIMENTALMENTE** | Proceso, pero no aprobado en ADR-004; riesgo de leakage temporal |
| LB-04 | Etapa atascada | Una etapa sin avance en N días | **VÁLIDO SOLO EXPERIMENTALMENTE** | Permitido por ADR-001 (proceso); sin definición formal aprobada |
| LB-05 | Acuerdo entre evaluadores (ICC) | Métrica de calidad del proceso | **VÁLIDO SOLO EXPERIMENTALMENTE** | Mide el proceso, no a la persona [S20, S21] |
| LB-06 | Contratado | — | **NO VÁLIDO** | Reproduce decisiones históricas y su sesgo [S01, S42, S48] |
| LB-07 | Seleccionado | — | **NO VÁLIDO** | Ídem; contradice RF-23 y ADR-001 |
| LB-08 | Decisión humana histórica (RF-23) | — | **NO VÁLIDO** | Aprender la decisión es automatizarla (ADR-002) |
| LB-09 | «Mejor candidato» | — | **NO VÁLIDO** | No es observable; es un juicio |
| LB-10 | Score final humano o posición en el ranking | — | **NO VÁLIDO** | Equivale a predecir el ranking: scoring de personas |
| LB-11 | `human_level` como objetivo de predicción | — | **NO VÁLIDO** | Sugerir niveles está bloqueado (F33, CAP-05) |
| LB-12 | Desempeño o permanencia posterior | — | **NO VÁLIDO** | Validez predictiva baja en docentes [S22]; datos inexistentes |
| LB-13 | Resultado de entrevista «recomendado» (A-20) | — | **NO VÁLIDO** | Es un juicio humano sobre la persona |

**Regla:** RF-29 puede usar targets **del proceso** (LB-01), nunca de idoneidad personal. Cualquier otro label de proceso (LB-03 a LB-05) exige una decisión documentada, al estilo de ADR-004, antes de usarse.
