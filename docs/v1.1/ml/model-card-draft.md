# Model card — BORRADOR

**Estado del documento: `draft`. No existe modelo. Ninguna métrica ha sido medida.**

Los campos marcados `PENDIENTE DE MEDICIÓN` se completan solo con resultados de una ejecución real. Rellenarlos con metas, ejemplos o valores plausibles invalidaría el documento.

---

## Identificación

| Campo | Valor |
|---|---|
| Nombre | *(pendiente)* — propuesto: `process-delay-risk` |
| Versión del modelo | *(no existe)* |
| Estado | **`draft`** — ni `experimental` ni `no-go`: la fase previa aún no se ejecutó |
| Fecha de esta versión | 20 de septiembre de 2026 |
| Propietario académico | Equipo del proyecto: Coronacion Meza Fredy, Peña Arroyo Anthony, Vila Meza Luis Antonio |
| Curso | Pruebas y Calidad de Software, NRC 28607, Universidad Continental |
| Docente | Dr. Maglioni Arana Caparachin |
| Revisión y aprobación | **PENDIENTE** — requiere la compuerta de `phase-14-ml-definition.md` §Gate |

## Propósito

Estimar, con fines **académicos y experimentales**, la probabilidad de que un proceso de selección cierre después de su plazo operacional objetivo, a partir de señales operacionales agregadas disponibles en un checkpoint fijo.

**No** evalúa, puntúa, ordena ni clasifica personas. **No** interviene en ninguna decisión sobre candidatos.

## Unidad de análisis y checkpoint

- **Unidad:** un snapshot único de una vacante elegible. Máximo una observación por `vacancy_id`.
- **Checkpoint:** inicio del día inmediatamente posterior a `vacancies.closes_at`, en `America/Lima`.
- Detalle y justificación: [`problem-definition.md` §3](problem-definition.md).

## Target

```
delayed = 1  si  vacancies.closed_at >  target_completion_at
delayed = 0  si  vacancies.closed_at <= target_completion_at
```

**Aprobado conceptualmente** el 20/09/2026 (decisión 3). `ML-DECISION-01` quedó resuelta: `job_requests.required_by` **no** se reinterpreta y se aprueba la necesidad de un plazo operacional explícito.

**PENDIENTE para despliegue — `GAP-01`.** `target_completion_at` **no existe en Laravel**. El experimento lo obtiene del dataset sintético, que lo modela como variable operacional explícita. El modelo resultante **no es integrable** hasta que la brecha se resuelva en una fase posterior.

## Datos

| Campo | Valor |
|---|---|
| Origen | **Sintético**, generado a partir de la estructura del proceso |
| Versión | `synthetic-v1` *(no generado)* |
| Volumen | 6 000 observaciones propuestas |
| Periodo simulado | ≥ 36 meses |
| Organizaciones | 4 – 8, totalmente ficticias |
| Seed | `20260920` |
| Datos reales o PII | **Ninguno.** No se obtienen ni se usan |
| Hash del dataset | `PENDIENTE DE MEDICIÓN` |

## Features

- **Incluidas:** 14 del conjunto núcleo, más `days_remaining_to_target` condicionada a la aprobación del target. Lista completa con definiciones: [`feature-contract.md` §1](feature-contract.md).
- **Excluidas en v1:** 7 candidatas documentadas con su motivo ([§2](feature-contract.md)).
- **Prohibidas:** identidad, atributos sensibles, proxies socioeconómicos, contenido textual, puntajes, resultados de entrevista, ranking, decisión, identificadores y todo dato posterior al checkpoint ([§3](feature-contract.md)).

## Partición

Bloques temporales 70 / 15 / 15 ordenados por `checkpoint_at`. Test se usa una sola vez. Sin split aleatorio. Detalle: [`evaluation-plan.md` §1](evaluation-plan.md).

## Baselines y modelo

| Rol | Definición | Estado |
|---|---|---|
| Baseline trivial | Clase mayoritaria + predictor constante de prevalencia | No ejecutado |
| Baseline operacional | Regla de backlog y días sin actividad, con umbrales fijados en train | No ejecutado |
| Primer modelo | Logistic Regression con preprocesamiento reproducible | No entrenado |
| Comparación | Decision Tree, Random Forest; HistGradientBoosting opcional | No entrenados |

## Métricas

| Métrica | Valor |
|---|---|
| Average Precision (primaria) | `PENDIENTE DE MEDICIÓN` |
| Precision / Recall / F1 al umbral | `PENDIENTE DE MEDICIÓN` |
| F2 | `PENDIENTE DE MEDICIÓN` |
| Matriz de confusión | `PENDIENTE DE MEDICIÓN` |
| Balanced accuracy | `PENDIENTE DE MEDICIÓN` |
| ROC-AUC (contexto) | `PENDIENTE DE MEDICIÓN` |
| Brier score | `PENDIENTE DE MEDICIÓN` |
| Brier Skill Score | `PENDIENTE DE MEDICIÓN` |
| Prevalencia por bloque | `PENDIENTE DE MEDICIÓN` |
| Métricas por periodo y organización | `PENDIENTE DE MEDICIÓN` |
| Intervalo bootstrap pareado vs. baseline | `PENDIENTE DE MEDICIÓN` |

## Calibración y umbrales

| Campo | Valor |
|---|---|
| Método de calibración | `PENDIENTE` — sigmoid como primera opción; isotónica solo con muestra suficiente |
| Curva de confiabilidad | `PENDIENTE DE MEDICIÓN` |
| `t_high` | `PENDIENTE` — requiere meta de precision aprobada |
| `t_medium` | `PENDIENTE` — requiere meta de recall aprobada |
| Versión de umbrales | *(no existe)* |
| Comportamiento sin metas aprobadas | Devolver solo probabilidad; `risk_level = null` |

## Limitaciones

1. **Los datos son sintéticos.** Un buen resultado demostraría que el método es correcto, no que funcionaría en el Colegio Andino de Huancayo.
2. **Censura estructural.** Una vacante solo se cierra tras decisión y selección humanas, de modo que los procesos atascados nunca producen `closed_at` y quedan excluidos. Eso sesga la muestra hacia procesos que terminaron. La Fase 15 debe **medir** ese sesgo, no solo declararlo (decisión 10).
3. **El plazo objetivo no existe en el sistema.** Está aprobado conceptualmente, pero `GAP-01` sigue abierta: una de las quince features utilizables (`ML-FEAT-02`) **no es computable en Laravel hoy**. El modelo no es desplegable hasta resolverlo.
4. **Alcance temporal.** Una sola observación por proceso, en un único checkpoint.
5. **Sin validación externa.** Ninguna comparación contra datos reales es posible ni está prevista.

## Usos permitidos

Demostración metodológica académica: diseño de problema, generación reproducible, entrenamiento, evaluación honesta, calibración, integración técnica y documentación de un no-go.

## Usos prohibidos

Evaluar, puntuar, ordenar, recomendar, filtrar o descartar personas. Sustituir o condicionar la decisión del Aprobador/Dirección. Alimentar el ranking de RF-20 a RF-22. Presentarse como capacidad validada del producto. Cualquier uso institucional real.

## Ética y privacidad

Frontera completa en [`ethics-and-human-oversight.md`](ethics-and-human-oversight.md). Ningún atributo sensible ni proxy. Ningún dato personal cruza el límite Laravel ↔ ML.

## Supervisión humana

La decisión final pertenece siempre a una persona identificable, con justificación registrada y auditoría inalterable. El modelo no dispara acciones automáticas.

## Arquitectura y fallback

Laravel es el sistema de registro. El servicio de inferencia es opcional y sin estado. Si falla, es lento o responde algo inválido, la pantalla se muestra sin estimación y el proceso continúa completo. Detalle: [`api-contract-draft.md`](api-contract-draft.md).

## Actualización y retiro

**[PROPUESTA]** El modelo se retira si: cambia la semántica del plazo objetivo, se detecta fuga posterior, el rendimiento se degrada entre periodos, aparece cualquier uso fuera de los permitidos, o el equipo académico concluye el proyecto. No hay reentrenamiento automático.

## Linaje

| Campo | Valor |
|---|---|
| Hash del artefacto | `PENDIENTE DE MEDICIÓN` |
| Hash del dataset | `PENDIENTE DE MEDICIÓN` |
| Hash de la configuración | `PENDIENTE DE MEDICIÓN` |
| Versión del contrato de features | `feature-contract.md`, Fase 14 |
| Versiones de librerías | `PENDIENTE` |
