# F34 — Modelo de datos y contrato del módulo inteligente

> Fase F34, versión 1.1 (04/10/2026), corregida tras la auditoría F34. Modelo **conceptual y lógico** para datos futuros del módulo diseñado en [F33](../diseno-inteligente/README.md). No hay migraciones, endpoints ni tablas en la base de datos: el contrato vive en [`schema.json`](../tools/f34/schema.json) y el dataset que lo cumple es **100 % sintético** ([`dataset/`](dataset/)). G0 sigue **NO APROBADA**.

## 1. Principios del contrato

- **Sin score de idoneidad ni recomendación.** El contrato no tiene ningún campo calculado por el sistema sobre una persona (F33, CAP-15 y CAP-16 BLOQUEADAS). El único puntaje es el humano: `rubric_points`, derivado de forma determinista del `human_level` que asigna el evaluador.
- **Tokens en lugar de identidades.** Organización, vacante, postulación, persona y evaluador son tokens sintéticos (`ORG-S1`, `VAC-0001`, `APP-00001`, `PER-S-00001`, `EV-S1-01`). No hay nombres, correos, teléfonos, documentos de identidad, direcciones ni fotos.
- **Rol explícito de cada campo.** `identifier`, `foreign_key`, `context`, `human_record`, `free_text_synthetic`, `feature_process`, `label_process`, `lineage`, `split` o `fairness_synthetic`. Solo los campos `feature_process` pueden entrar a un modelo, y solo sobre el **proceso** (alcance E).
- **Linaje en cada fila.** Toda fila lleva `source_type = synthetic` y un `synthetic_record_id` único en todo el dataset.
- **Tiempo explícito.** Los instantes son `YYYY-MM-DDTHH:MM:SS` en `America/Lima`, con granularidad de segundo; `closes_at` es una fecha. La observación termina en `observation_end` (`2026-09-30T23:59:59`): ningún hecho registrado es posterior.
- **Contexto coherente.** Toda fila referida pertenece a la misma organización y vacante que la fila que la refiere (reglas CTX-01 a CTX-10): no hay cruces entre tenants ni entre vacantes.

## 2. Bloques del contrato

### A. Contexto de vacante

| Tabla | Campos clave | Notas |
|---|---|---|
| `organizations` | `organization_token` | 3 organizaciones sintéticas (multiempresa) |
| `competencies` | `competency_id`, `competency_label`, `scope`, `catalog_version` | Catálogo versionado por organización; etiquetas genéricas inspiradas en el ejemplo **ilustrativo** de F30 |
| `vacancies` | `vacancy_token`, `area`, `positions_count`, `published_at`, `closes_at`, `target_completion_at`, `criteria_version`, `rubric_version` | `target_completion_at` es un plazo operacional fijado antes de publicar (como en RF-29) |
| `criteria` | `criterion_id`, `competency_id`, `stage`, `method`, `weight`, `range_min`, `range_max` | Pesos que suman 100 (A-06); ambas etapas presentes |
| `rubric_levels` | `criterion_id`, `level` (1–4), `descriptor`, `rubric_points` | Correspondencia nivel → puntaje publicada: 1→5, 2→10, 3→15, 4→20 |
| `requirements` | `requirement_type`, `min_years` | Requisitos obligatorios: título, colegiatura, experiencia mínima |

### B. Evidencia

| Tabla | Campos clave | Notas |
|---|---|---|
| `evidence` | `evidence_id`, `source_type_ev`, `source_reference`, `criterion_id`, `assessment_id`, `evidence_text`, `provenance`, `registered_by`, `registered_at`, `state` | `provenance = registro_humano` (alcance B: texto introducido por una persona); `state` es `borrador` (sesión programada) o `vinculada` (inmutable al registrar el resultado) |
| `requirement_checks` | `declared_met`, `evidence_present` | Insumo de la alerta determinista CAP-01; **nunca** filtra ni descarta |

### C. Evaluación humana

| Tabla | Campos clave | Notas |
|---|---|---|
| `sessions` | `session_token`, `stage`, `evaluator_token`, `scheduled_for`, `status`, `completed_at` | Estados vigentes `programada` → `realizada` (FF-02, `AssessmentResultRecorder`) |
| `assessments` | `human_level`, `rubric_points`, `justification`, `evidence_sufficiency`, `evaluator_token`, `recorded_at`, versiones | Un resultado por sesión y criterio; solo en sesiones `realizada`; inmutable (A-19) |
| `annotations` | `assessment_id`, `reason`, `annotation_text` | **Anotaciones complementarias** de solo inserción; no modifican el resultado |

### D. Proceso

| Tabla | Campos clave | Notas |
|---|---|---|
| `process_events` | `event_type`, `event_at`, `ref_token` | Línea de tiempo: publicación, postulaciones, sesiones programadas y realizadas, cambios de etapa (incluido el historial inicial de cada postulación) y cierre; el cierre solo existe si se observó |
| `process_snapshots` | 15 variables RF-29 + `delayed` + `observation_status` | Snapshot en el checkpoint (inicio del día siguiente a `closes_at`, ADR-004); variables calculadas con la semántica exacta de RF-29 (`t <= checkpoint_at`); `delayed` vacío y `censored` si el cierre no se observó |
| `process_splits` | `label_known_at`, `split`, `split_reason` | Partición temporal agrupada por vacante con purga por madurez de la etiqueta (ver [calidad y leakage](F34_Data_Leakage_y_Calidad.md#5-particiones)); `label_known_at` nunca es feature |
| `analysis_runs` + `analysis_run_events` | versiones, `input_hash_algorithm`, `input_snapshot_hash`, estados | Registro principal inmutable + eventos de solo inserción (F33); hash canónico del contenido de entrada (`f34-input-sha256-v1`) |
| `expected_alerts` | `alert_type`, referencias | Oráculo de prueba de las reglas deterministas de F33 |

### Archivo separado

| Archivo | Contenido | Regla |
|---|---|---|
| `fairness_sintetico/synthetic_group_attributes.csv` | `person_token`, `grupo_sintetico` (`GS-A`, `GS-B`) | Etiqueta abstracta asignada al azar; **no** representa sexo, edad ni ninguna categoría real; fuera de todo feature set |

## 3. Relaciones

```
organizations ─┬─< competencies ─< criteria >─ vacancies >─ organizations
               └─< vacancies ─┬─< criteria ─< rubric_levels
                              ├─< requirements ─< requirement_checks >─ applications
                              ├─< applications ─< sessions ─< assessments ─< annotations
                              │                         └─< evidence >─ assessments (si vinculada)
                              ├─< process_events
                              ├── process_snapshots ── process_splits
                              └─< analysis_runs ─< analysis_run_events
```

Todas las claves foráneas están declaradas en `schema.json` y se comprueban (regla DQ-06).

## 4. Correspondencia con el diseño de F33

| Entidad de F33 | Tabla de F34 |
|---|---|
| Competencia, criterio de vacante, rúbrica BARS | `competencies`, `criteria`, `rubric_levels` |
| Evidencia (cita y fuente introducidas por una persona) | `evidence` |
| Valoración humana (nivel, justificación, suficiencia) | `assessments` |
| Anotación complementaria | `annotations` |
| Alerta de proceso | `expected_alerts` (oráculo; las alertas reales se calcularían en F35) |
| `analysis_run` + `analysis_run_events` | Tablas homónimas |
| ML del proceso (RF-29) | `process_snapshots` (nombres del contrato RF-29, sin modificarlo) |

## 5. Lo que el contrato excluye a propósito

- Cualquier score, ranking o recomendación calculado por el sistema sobre personas.
- Etiquetas «contratado», «seleccionado», decisión RF-23 o posición en el ranking.
- `closed_at`, `decided_at` y cualquier otra columna posterior al checkpoint dentro de la tabla de features.
- Atributos sensibles reales o sus *proxies* (edad, sexo, etnia, discapacidad, salud, dirección, colegio o universidad de procedencia).
- Embeddings, similitud semántica o texto extraído automáticamente de PDF o DOCX (alcance C).

## 6. Lectura por fases futuras

`schema.json` sigue la convención de Frictionless Table Schema (campos, restricciones, `primaryKey`, `foreignKeys`) para que F35/F36 puedan leerlo sin herramientas nuevas. El detalle de qué podrá consumir cada fase, y bajo qué condición de G0, está en [F34_Preparacion_F35_F36.md](F34_Preparacion_F35_F36.md).
