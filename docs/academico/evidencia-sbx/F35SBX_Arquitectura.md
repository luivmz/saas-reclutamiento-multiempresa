# F35-SBX-A — Arquitectura lógica experimental

> Fase F35-SBX-A, versión 1 (07/10/2026). Arquitectura **conceptual**: en esta fase no hay código de pipeline, servicio, endpoint ni migración. Los fixtures describen el resultado esperado de cada paso (un oráculo declarativo, `run_kind = oraculo_sbx_a`) para que F35-SBX-B lo reproduzca.

## 1. Frontera

Todo vive en `docs/academico/evidencia-sbx/` y `docs/academico/tools/f35sbx/`. La única entrada es el `evidence.csv` sintético de F34, leído sin modificarlo y verificado contra su manifiesto. Nada cruza hacia `app/`, `routes/`, `database/`, `ml-service/`, la base de datos ni la red.

```
dataset F34 (solo lectura, SHA-256 del manifiesto F34)
        |
        |  regla de selección determinista (dos filas por organización)
        v
fixtures/ORG-S*_evidencias.json  [SINTÉTICO], versionados
        |
        v
SyntheticPipelineRun (un run por tenant, reloj lógico, semilla)
        |
        +-- SyntheticEvidenceSource --- SyntheticEvidenceRecord --- SyntheticEvidenceHash
        |                                      |
        |                          SyntheticEvidenceProvenance (encadenada)
        |                                      |
        |                          SyntheticHumanReview (integridad y procedencia)
        |
        +-- SyntheticPipelineEvent (encadenados) + SyntheticAuditEntry (sin contenido)
        |
        v
manifest.json (SHA-256 y tamaño) <--- validate_f35sbx.py recalcula todo
```

## 2. Componentes

| Componente | Representación en F35-SBX-A | Equivalente en F34 | En F35-SBX-B |
|---|---|---|---|
| SyntheticTenantContext | Objeto `tenant` de cada fixture | `organizations` (`ORG-S1..S3`) | Igual |
| SyntheticEvidenceSource | Lista `sources`: fila F34 de origen y SHA-256 de `evidence.csv` | `evidence.synthetic_record_id` | Igual |
| SyntheticEvidenceRecord | Lista `records`, sin tokens de persona | `evidence`, sin `application_token` | Tabla SQLite en memoria |
| SyntheticEvidenceHash | `hash_definition` del contrato; algoritmo `f35sbx-content-sha256-v1` | Patrón de `f34-input-sha256-v1` | Igual |
| SyntheticEvidenceProvenance | Lista `provenance`, encadenada por `prev_provenance_hash` | `evidence.provenance` | Solo inserción |
| SyntheticPipelineRun | Objeto `run`, `run_kind = oraculo_sbx_a` | `analysis_runs` | Ejecución real en sandbox |
| SyntheticPipelineEvent | Lista `events`, siete estados encadenados | `analysis_run_events` | Solo inserción con triggers |
| SyntheticHumanReview | Lista `reviews`, declarada en el fixture | — | Igual |
| SyntheticAuditEntry | Lista `audit`, solo identificadores y hashes | Separada de `audit_logs` | Solo inserción |
| Manifest | `fixtures/manifest.json` | `dataset/manifest.json` | Más el informe de cada run |

Mecanismo de almacenamiento: **solo JSON versionado** (DH-07). No hay SQLite, ni almacenamiento temporal, ni archivos fuera de las dos carpetas autorizadas.

## 3. Flujo del pipeline

Estados del run: `pendiente`, `validando`, `registrado`, `transformado`, `en_revision`, `revisado` y `completado`; `fallido` y `purgado` quedan reservados para F35-SBX-B. Cualquier error deja el run en `fallido`, con código y sin resultado parcial.

| Paso | Qué hace | Estado o auditoría | Comprobación en F35-SBX-A |
|---|---|---|---|
| 1 | Fixture sintético verificado contra el manifest | `fixture_verificado` | MAN |
| 2 | Validación del esquema cerrado | `validando`, `esquema_validado` | SCH, CON |
| 3 | Validación synthetic-only: seis marcadores | `sintetico_verificado` | SYN, PII, MED, PER |
| 4 | Cálculo del hash de contenido | `hash_calculado` | HSH |
| 5 | Registro de provenance | `registrado`, `provenance_registrada` | PRV, ORI |
| 6 | Transformación T1: Unicode NFC y espacios colapsados | `transformado` | HSH (`hash_before`, `hash_after`) |
| 7 | Validación del tenant | `tenant_validado` | ISO |
| 8 | Revisión humana simulada | `en_revision`, `revisado`, `revision_simulada_registrada` | REV |
| 9 | Resultado experimental: estado de validación de cada evidencia | Campo `validation_status` | SCH |
| 10 | Auditoría experimental encadenada | Lista `audit` | RUN, HSH |
| 11 | Cierre e inmutabilidad del run | `completado`, `ejecucion_cerrada` | HSH (cadenas) |
| 12 | Purga o retención | Sin almacenamiento temporal en F35-SBX-A | STO, DEP |

Ningún paso clasifica ni puntúa ni recomienda ni decide sobre personas, ni consulta un LLM. El resultado de cada evidencia solo dice si el artefacto es íntegro y procedente (`valido` o `rechazado`), nunca nada sobre la persona sintética.
