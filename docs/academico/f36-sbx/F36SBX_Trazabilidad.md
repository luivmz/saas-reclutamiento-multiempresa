# F36-SBX — Trazabilidad

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. F36-SBX no modifica ningún RF, CU ni RNF, ni los RF candidatos. No promueve nada al baseline.

## 1. Requisitos relacionados (sin cambios)

| RF | Significado vigente ([traceability-master](../../final-report/traceability-master.md)) | Relación con F36-SBX |
|---|---|---|
| RF-13 | Registrar preselección o descarte (RR. HH.) | EI-02 solo alerta; nunca preselecciona ni descarta |
| RF-19 | Registrar entrevista y resultado (evaluador) | La evidencia de EI-01 y EI-03 es la que registra el evaluador; la ayuda llega después de la calificación (TEI-13) |
| RF-20 | Validar rangos y ponderaciones | Sin relación directa; EI-04 no crea pesos ni totales |
| RF-21 | Calcular ranking configurable | Ninguna salida F36-SBX ni F37-SBX lo alimenta (EI-19 y EI-23 BLOCKED) |
| RF-22 | Presentar comparación de candidatos | EI-04 estudia un desglose por criterio, sin orden ni insignias. No sustituye RF-22 |
| RF-23 | Registrar la decisión final de selección (**humana**) | Intacta. Ninguna capacidad la sustituye ni la informa |
| RF-29 (candidato) | Riesgo operacional del proceso, experimental | Intacto. F36-SBX no es la F36 «ML baseline» del mapa F33 |

## 2. Antecedentes y cómo se usan

| Fuente | Qué toma F36-SBX |
|---|---|
| F30 · [Investigación IA](../investigacion-ia/README.md) | Evidencia científica [Sxx, Oxx], la cadena de procedencia, las métricas por tarea y el catálogo de herramientas |
| F33 · [ADR-005](../diseno-inteligente/F33_ADR_005_G0.md), [matriz CAP](../diseno-inteligente/F33_Matriz_Capacidades_y_Restricciones.md) y [mapa](../diseno-inteligente/F33_Mapa_F34_F40.md) | La frontera B/C, la clasificación CAP (que F36-SBX no relaja), las prohibiciones §6.7 y la regla de datos §6.10 |
| F34 · [Datos sintéticos](../datos-sinteticos/README.md) | Las tablas reutilizables y la partición con purga (`process_splits`) |
| F34A · [Threat model](../g0-readiness/F34A_Modelo_de_Amenazas.md) | T-01..T-25, que TEI-xx extiende |
| F34E · [G0-SBX](../g0-sandbox/README.md) | Las prohibiciones, la separación entre la G0 real y SBX y los criterios de salida SAL-01..SAL-05 |
| F35-SBX · [Contrato](../evidencia-sbx/README.md) y [cierre global](../evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md) | Los marcadores synthetic-only, la provenance, TSB-xx y la regla de que F36-SBX exige una autorización sucesora |

## 3. Matriz EI → CAP → amenaza → métrica → gate

| EI | CAP F33 | Amenazas principales | Métricas | Criterios del gate |
|---|---|---|---|---|
| EI-01 | CAP-04, CAP-06 | TEI-12 | M-01 | FG-03, FG-06 |
| EI-02 | CAP-01, CAP-34 | TEI-14 | M-02 | FG-03, FG-06 |
| EI-03 | CAP-04, CAP-29 | TEI-10, TEI-12 | M-03, M-11 | FG-03, FG-06 |
| EI-04 | CAP-13 | TEI-14 | M-04 | FG-03, FG-06, FG-11 |
| EI-05 | — | TEI-01, TEI-02 | M-05 | FG-03, FG-07 |
| EI-06 | CAP-06 | TEI-12 | M-01 | FG-03, FG-06 |
| EI-07 | CAP-08 | TEI-05 | M-06 | FG-03, FG-06 |
| EI-08 | CAP-07 | TEI-15, TEI-17 | M-09 | FG-10, FG-12 |
| EI-09 | CAP-08 | TEI-07, TEI-11, TEI-13, TEI-20 | M-07, M-08, R-01 | FG-12 (F36-M02) |
| EI-10 | CAP-09, CAP-20 | TEI-06, TEI-16, TEI-17, TEI-21 | M-07, M-08, M-13, R-02, R-03 | FG-10, FG-12 |
| EI-11 | CAP-07 | TEI-03, TEI-04, TEI-19 | M-10 | FG-10, FG-12 |
| EI-12 | CAP-07 | TEI-15 | M-09 | FG-10, FG-12 |
| EI-24 | CAP-32 | TEI-14, TEI-15 | M-13 | FG-12 |
| EI-13..EI-23 | Ver la [matriz](F36SBX_Matriz_Capacidades.md) | TEI-09, TEI-14, TEI-15, TEI-22 | — (BLOCKED) | FG-06, FG-11, FG-13 |

## 4. Estado de G0 y de las puertas

G0 real = NO APROBADA; G0-02, G0-03 y G0-12 = PENDIENTE EXTERNO; G0-09 y G0-14 = CUMPLIDO; G0-SBX = APROBADA CON RESTRICCIONES, con alcance solo en F35-SBX; ADR-005 = PROPUESTA; F36-SBX-GATE = NO SUPERADO. F36-SBX no cambia ninguno de estos estados de la G0 real ni de G0-SBX.
