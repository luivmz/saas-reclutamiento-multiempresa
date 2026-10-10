# F35-SBX-A — Contratos de datos

> Fase F35-SBX-A, versión 1 (07/10/2026). Fuente: [`contrato/f35sbx_contract.json`](contrato/f35sbx_contract.json), versión `f35sbx-contract-1.0.0`. El validador construye el mismo contrato de forma independiente y exige que el archivo coincida exactamente (doble llave): ningún campo se añade y ninguna restricción se relaja.

## 1. Reglas del contrato

- Subconjunto cerrado de JSON Schema: `type`, `properties`, `required`, `additionalProperties`, `items`, `minItems`, `maxItems`, `const`, `enum`, `pattern`, `maxLength`, `minLength`, `minimum`, `maximum` y `$ref`. Cualquier otra palabra clave falla.
- Cada entidad es un objeto con `additionalProperties: false` y `required` igual a todos sus campos.
- Ninguna cadena queda libre: cada campo de texto lleva `const`, `enum` o `pattern`.
- `text_synthetic` empieza por `[SINTÉTICO] `, mide como máximo 400 caracteres y no admite `<`, `>` ni caracteres de control (T2, prevención de XSS).

## 2. Entidades y campos

| Entidad | Campos permitidos |
|---|---|
| FixtureFile | `fixture_id`, `contract_version`, `synthetic_organization_id`, `source_type`, `environment`, `synthetic_marker`, `tenant`, `run`, `events`, `sources`, `records`, `provenance`, `reviews`, `audit` |
| SyntheticTenantContext | `synthetic_organization_id`, `tenant_kind`, `origin_dataset_version`, `simulation_actor` |
| SyntheticPipelineRun | `pipeline_run_id`, `synthetic_organization_id`, `run_kind`, `pipeline_version`, `contract_version`, `hash_algorithm`, `seed`, `clock_start`, `environment`, `source_type` |
| SyntheticPipelineEvent | `event_id`, `pipeline_run_id`, `seq`, `state`, `at`, `error_code`, `prev_event_hash`, `event_hash` |
| SyntheticEvidenceSource | `source_id`, `synthetic_organization_id`, `source_type`, `origin_dataset_version`, `origin_file`, `origin_file_sha256`, `origin_record_id` |
| SyntheticEvidenceRecord | `synthetic_id`, `synthetic_organization_id`, `pipeline_run_id`, `source_id`, `criterion_ref`, `evidence_kind`, `text_synthetic`, `source_type`, `environment`, `hash_algorithm`, `content_hash`, `validation_status`, `review_status`, `created_at` |
| SyntheticEvidenceProvenance | `provenance_id`, `record_id`, `synthetic_organization_id`, `provenance_kind`, `source_id`, `transformation_id`, `transformation_version`, `hash_before`, `hash_after`, `pipeline_run_id`, `review_id`, `recorded_at`, `prev_provenance_hash`, `provenance_hash` |
| SyntheticHumanReview | `review_id`, `record_id`, `pipeline_run_id`, `synthetic_organization_id`, `reviewer_type`, `simulation_actor`, `review_scope`, `review_status`, `scripted`, `reviewed_at` |
| SyntheticAuditEntry | `audit_id`, `pipeline_run_id`, `synthetic_organization_id`, `action`, `target_ref`, `at`, `prev_audit_hash`, `audit_hash` |

`evidence_kind` solo admite `formulario`, `nota_entrevista` o `prueba`. Quedan excluidos los tipos `cv` y `documento` de F34, para no acercarse al alcance C.

## 3. Identificadores

| Prefijo | Entidad | Patrón |
|---|---|---|
| `FXS` | Fixture | `FXS-ORG-S[1-3]` |
| `SBXR` | Run | `SBXR-ORG-S[1-3]-NNNN` |
| `SBXV` | Evento | `SBXV-ORG-S[1-3]-NNNN-NN` |
| `SBXS` | Fuente | `SBXS-ORG-S[1-3]-NNNNNN` |
| `SBXE` | Evidencia | `SBXE-ORG-S[1-3]-NNNNNN` |
| `SBXP` | Provenance | `SBXP-ORG-S[1-3]-NNNNNN` |
| `SBXH` | Revisión simulada | `SBXH-ORG-S[1-3]-NNNNNN` |
| `SBXA` | Auditoría | `SBXA-ORG-S[1-3]-NNNN-NN` |
| `SIMREV` | Actor simulado del tenant | `SIMREV-ORG-S[1-3]` |

Cada identificador lleva el tenant. `SIMREV` designa un rol simulado por tenant, nunca a un individuo (DH-06). Las únicas referencias externas son `origin_record_id` (`SYN-NNNNNN` de F34) y `criterion_ref` (`CRI-NNNN` de F34).

## 4. Marcadores synthetic-only

Cada evidencia debe llevar los seis a la vez; si falta uno, falla.

| # | Marcador |
|---|---|
| 1 | `synthetic_id` con prefijo `SBXE-` y el tenant |
| 2 | `text_synthetic` que empieza por `[SINTÉTICO]` |
| 3 | `source_type = synthetic` |
| 4 | `environment = sandbox` |
| 5 | `hash_algorithm = f35sbx-content-sha256-v1` |
| 6 | `synthetic_organization_id` en `ORG-S1..S3` |

## 5. Campos y valores prohibidos

| Prohibido en contrato y fixtures | Ejemplos de nombres o valores rechazados |
|---|---|
| Datos personales | `real_name`, `name`, `email`, `telefono`, `dni`, `ruc`, `direccion`, `edad`, `sexo`, `salud`, `foto`; correos, URL, números de 8 u 11 dígitos, teléfonos |
| Documentos o media | `cv`, `curriculum`, `pdf`, `docx`, `imagen`, `audio`, `video`, `adjunto`, `archivo`, `base64`; extensiones de documento o media, data URI, bloques base64 |
| Identificadores de persona | `person_token`, `candidato`, `postulante`, `evaluador`, `usuario`, `human_level`, `rubric_points`; valores `APP-`, `PER-S-`, `EV-` |
| Capacidades | `score`, `ranking`, `recommendation`, `best`, `selected`, `automatic`, `ocr`, `parsing`, `extraction`, `embedding`, `vector`, `semantic`, `llm`, `similarity`, `apto`, `aptitud`, `idoneidad`, `merito`, `desempeno`, `personalidad`, `emocion`, `honestidad`, `inteligencia`, `estres`, `biometria` |
| Destinos productivos | `endpoint`, `url`, `host`, `database`, `table`, `storage`, `connection`; valores con `pgsql`, `postgres`, `redis`, `sqlite`, `.env`, `audit_logs`, `app/`, `database/` o `ml-service` |

## 6. Hash de contenido (SyntheticEvidenceHash)

`f35sbx-content-sha256-v1`: SHA-256 del JSON canónico (claves ordenadas, separadores sin espacios, UTF-8 sin escapar) con `algorithm`, `synthetic_organization_id`, `origin_record_id`, `criterion_ref`, `evidence_kind` y `text`. No incluye tokens de persona. Cambiar el contenido canónico exige un nombre nuevo (`-v2`), nunca reutilizar este.

Las cadenas de eventos, provenance y auditoría usan el mismo JSON canónico: cada elemento guarda el hash del anterior (el primero, 64 ceros) y su propio hash calculado sin ese campo.
