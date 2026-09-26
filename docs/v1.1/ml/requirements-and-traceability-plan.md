# Requerimientos candidatos y plan de trazabilidad

**Fase 14 · 20 de septiembre de 2026**

**[LIMITACIÓN]** Ningún requerimiento de este documento está aprobado. RF-01 a RF-27 no se tocan: conservan número, significado y condición de línea base de v1.0.

> **[APROBADA] Decisión 11 del equipo, 20 de septiembre de 2026.** Se mantienen las disposiciones: RF-28 candidato a panel operacional descriptivo; RF-29 candidato **condicionado** a que el experimento supere su compuerta; RF-30 y RF-31 fuera del alcance de ML en esta fase. **Ni RF-28 ni RF-29 se marcan todavía como RF formalmente aprobados del baseline de v1.1.**

---

## 1. Esquema de trazabilidad a construir

**[PROPUESTA]** La matriz de v1.1 no se construye todavía; se define su forma para que una fase posterior la llene sin improvisar:

```
Problema ML (ML-PROBLEM-NN)
→ RF/RNF candidato
→ actor y caso de uso
→ feature ID (ML-FEAT-NN) y su fuente temporal
→ campo y versión del dataset
→ preprocesamiento
→ baseline / modelo (ML-BASE-NN, ML-MODEL-NN)
→ métrica y criterio (ML-METRIC-NN)
→ prueba futura
→ campo de la API
→ elemento de UI
→ documento o evidencia
→ estado de aprobación
```

Cada enlace admite exactamente un estado: `verificado`, `propuesto`, `pendiente` o `no aplica`.

### Espacios de identificadores

| Prefijo | Uso | Asignados en la Fase 14 |
|---|---|---|
| `ML-PROBLEM-NN` | Problema de ML | `ML-PROBLEM-01` |
| `ML-UNIT-NN` | Unidad de análisis | `ML-UNIT-01` |
| `ML-CHECKPOINT-NN` | Definición de checkpoint | `ML-CHECKPOINT-01` |
| `ML-TARGET-NN` | Definición de target | `ML-TARGET-01` |
| `ML-DECISION-NN` | Decisión pendiente bloqueante | `ML-DECISION-01` |
| `ML-FEAT-NN` / `ML-FEAT-XNN` | Features incluidas / excluidas | `01`–`18`, `X01`–`X07` |
| `ML-SPLIT-NN` | Estrategia de partición | `ML-SPLIT-01` |
| `ML-BASE-NN` / `ML-MODEL-NN` | Baselines / modelos | `ML-BASE-01`, `ML-BASE-02`, `ML-MODEL-01` |
| `ML-ETHICS-NN` | Frontera ética | `ML-ETHICS-01` |

**[LIMITACIÓN]** Este espacio **no compite** con la numeración RF/RNF y no la sustituye.

**[PROPUESTA]** No se edita la trazabilidad histórica RF-01 a RF-27 ni el Formato 09. Cuando el equipo apruebe requerimientos, la actualización se planifica desde `documentation-update-map.md`.

---

## 2. RF candidatos

### RF-28 (candidato) — Panel operativo de seguimiento

| Campo | Contenido |
|---|---|
| **Necesidad** | RR. HH. y Dirección no disponen hoy de una vista agregada de tiempos y cuellos de botella del proceso |
| **Actores** | RR. HH. y Aprobador/Dirección de la **misma** organización |
| **Precondición** | Existir vacantes publicadas en la organización del usuario |
| **Entrada** | Selección de organización implícita por tenant; filtros de periodo y estado |
| **Salida** | Tiempos por etapa operacional, backlog de sesiones, carga concurrente y cuellos de botella, **todo agregado** |
| **Dependencias** | Ninguna respecto del ML. **Es independiente y puede aprobarse por separado** |
| **Aceptación** | No expone datos personales innecesarios; respeta aislamiento tenant con prueba cross-tenant; no muestra puntajes, ranking ni identidades salvo lo ya permitido por RF-12 |
| **Riesgos** | Que se convierta en un tablero de desempeño de personas; mitigable manteniendo todo agregado |
| **¿RF o RNF?** | **RF**: es una capacidad funcional observable |
| **Disposición** | **Conservar como candidato.** Es además el **fallback descriptivo** si RF-29 resulta NO-GO |

### RF-29 (candidato) — Estimación informativa de riesgo de demora

| Campo | Contenido |
|---|---|
| **Necesidad** | Anticipar procesos que terminarán fuera de plazo, para reasignar atención |
| **Actores** | RR. HH. y Aprobador/Dirección de la misma organización |
| **Precondición** | Vacante publicada, elegible y posterior al checkpoint; servicio de inferencia disponible |
| **Entrada** | El usuario consulta un proceso. **Laravel deriva el vector operacional**; el usuario no introduce features |
| **Salida** | Probabilidad calibrada, versión de modelo, factores operacionales y rótulo de estimación sintética. **Ninguna acción automática** |
| **Dependencias** | `ML-DECISION-01` aprobada · contrato de features aprobado · experimento aceptado según `evaluation-plan.md` §6 · fallback implementado · supervisión humana |
| **Aceptación** | La pantalla funciona sin el servicio; ninguna escritura automática; ningún dato personal en la salida; rotulado presente |
| **Riesgos** | Que se lea como juicio sobre candidatos; que la probabilidad se interprete como certeza; fatiga de alertas |
| **¿RF o RNF?** | **RF**, con RNF de resiliencia y explicabilidad asociados |
| **Disposición** | **Candidato condicionado a la compuerta científica.** Si se activa el NO-GO, **no** se presenta como predictor válido |

### RF-30 (candidato) — Exportación operativa PDF/CSV

**Disposición: fuera del alcance de la Fase 14.** Es una capacidad potencial, pero no es necesaria para definir ni entrenar el modelo, y **no debe usarse como justificación para incluir PII** en ningún dataset ni exportación. Se evalúa en otra fase, con minimización de datos y control tenant. **[LIMITACIÓN]** No se analiza aquí para no darle estatus por acumulación.

### RF-31 (candidato) — Portal público visual mejorado

**Disposición: fuera del alcance de la Fase 14.** Es funcional y experiencial, no un requisito de ML. Su aprobación **no** se vincula al experimento. No autoriza 3D ni dependencias nuevas (véase ADR-003).

**[LIMITACIÓN]** Ningún RF candidato se marca aprobado. Los números no se reasignan.

---

## 3. Brecha funcional detectada

**`GAP-01` — Plazo operacional de cierre inequívoco.** **Decisión de diseño APROBADA el 20/09/2026; brecha de implementación ABIERTA.**

**[HECHO]** El único campo temporal parecido es `job_requests.required_by`: `date` nullable (`database/migrations/2026_09_13_000005_create_job_requests_table.php:22`), validado `after_or_equal:today` (`app/Http/Requests/JobRequests/JobRequestFormRequest.php:33`) y rotulado «fecha requerida» (`:48`). Nada demuestra que signifique la fecha límite para cerrar el proceso de selección.

**[APROBADA]** *(decisión 3)*

| Aspecto | Resolución |
|---|---|
| Reutilizar `required_by` | **Rechazado.** Conserva su significado histórico y actual; RF-01 no se modifica |
| Necesidad de `target_completion_at` | **Aprobada conceptualmente**: fecha/hora objetivo máxima para completar el proceso de selección, inequívoca |
| Implementación en la Fase 14 | **Ninguna.** Sin campo, sin migración, sin RF, sin cambios en Laravel |
| Dónde se resuelve | **Fase de integración correspondiente**, con su propia autorización |
| Efecto en la Fase 15 | **No bloquea el experimento**: el dataset sintético modela `target_completion_at` como variable operacional explícita |
| Efecto en la integración | **Bloqueante.** Sin este campo, `ML-FEAT-02` no es computable en Laravel y el contrato de API no puede satisfacerse |

**[LIMITACIÓN]** Mientras `GAP-01` siga abierta, un modelo exitoso en la Fase 15 **no es desplegable**. La brecha no es un detalle pendiente: es la condición que separa el gate científico del gate de integración.

**[PENDIENTE]** Cuando el equipo aborde la implementación deberá decidir: en qué entidad vive el plazo (requerimiento o vacante), quién lo fija y cuándo, si es obligatorio u opcional, cómo se garantiza su inmutabilidad tras la publicación, y qué RF o RNF lo cubre. **Ninguna de esas decisiones se toma aquí, y no se reserva número de RF.**

---

## 4. RNF candidatos

### Existentes, revisados

| RNF | Disposición |
|---|---|
| **RNF-A · Accesibilidad** | Sigue siendo candidato y **relevante para cualquier UI futura**. **[LIMITACIÓN]** No se aprueba retroactivamente un alcance general sobre RF-01 a RF-27 sin una auditoría real. La accesibilidad futura permanece bajo este RNF; no se crea uno nuevo |
| **RNF-B · Rendimiento frontend** | Candidato. **Separado** del rendimiento de inferencia: son magnitudes distintas y no deben mezclarse en una misma métrica |
| **RNF-C · Experiencia 3D** | **Fuera de la Fase 14.** Sin relación con el experimento (ADR-003) |
| **RNF-D · Observabilidad operacional** | Candidato **relevante**. Se refina a: logs técnicos estructurados, latencia, disponibilidad y versión de modelo, **sin PII**. No se duplica en otro RNF |

### Adicionales propuestos

**[PROPUESTA]** Numeración provisional, sin aprobar:

| ID prov. | Candidato | Contenido |
|---|---|---|
| RNF-E | Resiliencia del componente opcional | La plataforma funciona completa si el servicio de inferencia no existe o está caído; fallback probado |
| RNF-F | Reproducibilidad y versionado | Dataset, código, seed, esquema, umbrales y modelo versionados y verificables por hash |
| RNF-G | Seguridad y privacidad del límite Laravel–ML | Sin PII a través del límite; autenticación servicio-a-servicio y red interna **[PENDIENTE]** |
| RNF-H | Explicabilidad, rotulado y supervisión humana | Factores operacionales legibles, rótulo de estimación sintética, decisión siempre humana |
| RNF-I | Rendimiento de inferencia | Objetivo p95 **[PENDIENTE]**, definido solo tras medir una línea base |

**[LIMITACIÓN]** No se convierten decisiones de diseño puntuales en RNF artificiales. Los cinco anteriores son transversales y verificables; si alguno resulta redundante al aprobarse, se fusiona en lugar de multiplicarse.

## Enlaces

- [Definición del problema](problem-definition.md) · [Contrato de features](feature-contract.md) · [Plan de evaluación](evaluation-plan.md) · [Alcance preliminar](../scope-preliminary.md) · [Mapa de actualización documental](../documentation-update-map.md) · [Índice de la Fase 14](../phase-14-ml-definition.md)
