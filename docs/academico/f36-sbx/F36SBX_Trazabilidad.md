# F36-SBX — Trazabilidad

> Fase F36-SBX, versión 4 (27/10/2026): añade la trazabilidad de las auditorías AF1, AF2, AF3 y AF4 (sección 5). Candidata a una quinta auditoría independiente. F36-SBX no modifica ningún RF, CU ni RNF, ni los RF candidatos. No promueve nada al baseline.

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

## 5. Auditorías independientes y correcciones

| Auditoría | Candidato | Resultado | Corrección |
|---|---|---|---|
| AF1 | `06e933e` | No aprobado: 2 MEDIUM, más 3 defectos del oracle encontrados al corregir | [Corrección AF1](F36SBX_Correccion_AF1.md) |
| AF2 | `2a4e68c` | No aprobado: 0 BLOCKER, 0 HIGH, 3 MEDIUM y 1 LOW | [Corrección AF2](F36SBX_Correccion_AF2.md). La tercera auditoría dio por corregidos AF2-M02, AF2-M03 y AF2-L01, y no corregido de forma integral AF2-M01: su parte pendiente, la pertenencia del ADR al candidato, es AF3-M01 |
| AF3 | `ecb22cc` | No aprobado: 0 BLOCKER, 0 HIGH, 2 MEDIUM y 1 LOW | [Corrección AF3](F36SBX_Correccion_AF3.md). La cuarta auditoría reprodujo sus pruebas sin falsos PASS en esas familias y señaló AF4-M01, AF4-M02 y AF4-L01 |
| AF4 | `57efbfc` | No aprobado: 0 BLOCKER, 0 HIGH, 2 MEDIUM y 1 LOW | [Corrección AF4](F36SBX_Correccion_AF4.md). AF4-M01, AF4-M02 y AF4-L01 corregidos por implementación, junto con los defectos propios AF4-PR01..PR05, pendientes de quinta auditoría independiente |

| Hallazgo AF2 | Control | Dónde se documenta | Pruebas |
|---|---|---|---|
| AF2-M01 | Bloque canónico del informe y del ADR, coherencia exacta con el registro e identidad visible | [Gate §8.6](F36SBX_Gate_Sucesor.md#86-informe-y-adr-fuente-estructurada-canónica) | AF2-01..AF2-12, D01..D46 |
| AF2-M02 | Hashes con etiqueta por nivel y sello de test v2 | [Contrato §5 y §6](F36SBX_Contrato_Evidencia.md#5-hashes-y-procedencia) | AF2-13..AF2-24, H01..H12, P-01..P-04 |
| AF2-M03 | Autores, anotadores y referencias upstream ligados a su contexto; sin fuentes globales | [Contrato §7](F36SBX_Contrato_Evidencia.md#7-aislamiento-entre-organizaciones) | AF2-25..AF2-30, X01..X10, P-05, P-06 |
| AF2-L01 | `example_id` cerrado y cobertura mínima del ejemplo | [Contrato §9](F36SBX_Contrato_Evidencia.md#9-ejemplo-de-conformidad) | AF2-31..AF2-33, L01..L05 |

| Hallazgo AF3 | Control | Dónde se documenta | Pruebas |
|---|---|---|---|
| AF3-M01 | El ADR es el blob regular `candidate_commit:path` y sus bytes se leen de Git; la evidencia de equipo es versionable | [Gate §8.6](F36SBX_Gate_Sucesor.md#86-informe-y-adr-fuente-estructurada-canónica) y §9 | AF3-01..AF3-11; con Git real, U01..U15 y G01..G11 |
| AF3-M02 | Contexto canónico de todo output, abstenciones y outputs de ajuste incluidos (REL-15) | [Contrato §7.1](F36SBX_Contrato_Evidencia.md#71-contexto-canónico-rel-15) | AF3-12..AF3-25, P-12..P-14, C52..C54 |
| AF3-L01 | Marcadores de identidad normalizados e identidades genéricas rechazadas | [Gate §8.6](F36SBX_Gate_Sucesor.md#86-informe-y-adr-fuente-estructurada-canónica) | AF3-26..AF3-35, P-07, P-08 |

| Hallazgo AF4 | Control | Dónde se documenta | Pruebas |
|---|---|---|---|
| AF4-M01 | El árbol de trabajo se compara con el índice por sus bytes. Las marcas `assume-unchanged` y `skip-worktree`, los conflictos, los objetos ausentes y las operaciones en curso fallan cerrado | [Gate §9](F36SBX_Gate_Sucesor.md#9-vínculo-con-el-candidato-auditado) | AF4-01..AF4-09 y AF4-12; con Git real, AF4-M01-1..7, AF4-M01-A1..A13 y W01..W19 |
| AF4-M02 | Una sola vía hacia Git, sobre objetos reales: sin `refs/replace` ni variables `GIT_*` heredadas, con el SHA-1 del commit verificado; `refs/replace` e injertos fallan cerrado | [Gate §8.6 y §9](F36SBX_Gate_Sucesor.md#86-informe-y-adr-fuente-estructurada-canónica) | AF4-10 y AF4-11; con Git real, AF4-M02-1..5, AF4-M02-A1..A4 y RP01..RP07 |
| AF4-L01 | Una identidad contiene al menos una palabra distintiva, tras normalizar | [Gate §8.6](F36SBX_Gate_Sucesor.md#86-informe-y-adr-fuente-estructurada-canónica) | AF4-L01-01..29, AF4-L01-P1, AF4-L01-P2, P-07 |
| AF4-PR01..PR05 | Entradas normativas versionables, injertos, caché de stat y filtros locales, entorno de Git saneado y validador de solo lectura | [Corrección AF4 §6](F36SBX_Correccion_AF4.md#6-revisión-del-oracle-y-hallazgos-propios) | AF4-06..AF4-08, AF4-11, RP07, W06, W16, W18, AF4-M01-A5, A7, A11 y A13, AF4-M02-A1 y A3 |

Las amenazas afectadas son TEI-05, TEI-06, TEI-08, TEI-12 y TEI-22 del [threat model](F36SBX_Threat_Model.md), sin renumerar; AF4 solo afecta a TEI-22. Las pruebas están en [`test_f36sbx.py`](../tools/f36sbx/test_f36sbx.py) y en [`test_f36sbx_git.py`](../tools/f36sbx/test_f36sbx_git.py), y las metapruebas, en [`meta_f36sbx.py`](../tools/f36sbx/meta_f36sbx.py).
