"""F35-SBX-B — B2: almacén efímero sintético por tenant (sbxb_store.py).

Módulo Python interno y experimental de F35-SBX-B; no es una API HTTP. Guarda los objetos de un run sintético en una
base SQLite ':memory:' propia de cada organización sintética y escenario, que solo admite inserciones de contenido F34
autorizado y se destruye cerrando la conexión.

Diseño: docs/academico/evidencia-sbx-b2/F35SBXB_B2_Diseno_Almacen.md (versión 2.1). Verificación:
F35SBXB_B2_Contrato_Verificacion.md y el gate validate_f35sbxb2.py de esta carpeta.

Código de desarrollo NO AUDITADO (Q6): un PASS del gate no equivale a confianza ni a cierre. No persiste nada de RF-29
ni ningún puntaje, ranking, recomendación o selección; RF-23 sigue siendo una decisión humana.
"""
import csv
import hashlib
import json
import os
import re
import sqlite3
import threading
import unicodedata

# ---------------------------------------------------------------- constantes del contrato (A, B0 §5.2 y diseño §5)
CONTRACT_VERSION = 'f35sbxb-contract-1.0.0'
PIPELINE_VERSION = 'f35sbxb-0'
RUN_KIND = 'ejecucion_sbx_b'
HASH_ALGORITHM = 'f35sbx-content-sha256-v1'
DATASET_VERSION = 'f34-synth-1.1.0'
ORIGIN_FILE = 'docs/academico/datos-sinteticos/dataset/evidence.csv'
GENESIS = '0' * 64
MARKER = '[SINTÉTICO] '
TENANTS = ('ORG-S1', 'ORG-S2', 'ORG-S3')
PATH = ('pendiente', 'validando', 'registrado', 'transformado', 'en_revision', 'revisado', 'completado')
TERMINAL = ('completado', 'fallido')
EVENT_STATES = PATH + ('fallido',)
AUDIT_ACTIONS = ('fixture_verificado', 'esquema_validado', 'sintetico_verificado', 'hash_calculado',
                 'provenance_registrada', 'tenant_validado', 'revision_simulada_registrada', 'ejecucion_cerrada')
EVIDENCE_KINDS = ('formulario', 'nota_entrevista', 'prueba')
VALIDATION_STATUSES = ('valido', 'rechazado')
REVIEW_STATUSES = ('conforme', 'observado')
TRANSFORMATION = ('T1-normalizacion-nfc-espacios', '1')
TENANT_FIELDS = ('synthetic_organization_id', 'tenant_kind', 'origin_dataset_version', 'simulation_actor')
EVIDENCE_FIELDS = ('origin_record_id', 'origin_file_sha256', 'criterion_ref', 'evidence_kind', 'text_synthetic',
                   'hash_before', 'content_hash', 'validation_status', 'review_status', 'created_at', 'recorded_at',
                   'reviewed_at')
# Origen autorizado (§11): las cuatro rutas fijas de F34 con el SHA-256 del manifiesto de f34-synth-1.1.0.
F34_INPUTS = (('evidence', 'docs/academico/datos-sinteticos/dataset/evidence.csv',
               'ec6aef1b297a2f5688800d883df5a681c7c4a8070af406e9532cfd785b4b0563'),
              ('criteria', 'docs/academico/datos-sinteticos/dataset/criteria.csv',
               '65898a8d9c8c431bfff48a84859647f5c69c9299485cf02e2d27ddfb52f5ee12'),
              ('vacancies', 'docs/academico/datos-sinteticos/dataset/vacancies.csv',
               '04def2e4f115c921586ba46c603c552c3a583344d54a67d69f75ca5c64f00b7a'),
              ('applications', 'docs/academico/datos-sinteticos/dataset/applications.csv',
               '15a9a125a11e6c9d14e6d5d239c1c10685786785db7ca02747c0b0230cd5ba82'))
_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))

# Columnas de cada tabla: exactamente los campos de su entidad de A, en el mismo orden (§5).
COLUMNS = {
    'tenant_context': ('synthetic_organization_id', 'tenant_kind', 'origin_dataset_version', 'simulation_actor'),
    'pipeline_run': ('pipeline_run_id', 'synthetic_organization_id', 'run_kind', 'pipeline_version', 'contract_version',
                     'hash_algorithm', 'seed', 'clock_start', 'environment', 'source_type'),
    'pipeline_event': ('event_id', 'pipeline_run_id', 'seq', 'state', 'at', 'error_code', 'prev_event_hash',
                       'event_hash'),
    'evidence_source': ('source_id', 'synthetic_organization_id', 'source_type', 'origin_dataset_version', 'origin_file',
                        'origin_file_sha256', 'origin_record_id'),
    'evidence_record': ('synthetic_id', 'synthetic_organization_id', 'pipeline_run_id', 'source_id', 'criterion_ref',
                        'evidence_kind', 'text_synthetic', 'source_type', 'environment', 'hash_algorithm',
                        'content_hash', 'validation_status', 'review_status', 'created_at'),
    'evidence_provenance': ('provenance_id', 'record_id', 'synthetic_organization_id', 'provenance_kind', 'source_id',
                            'transformation_id', 'transformation_version', 'hash_before', 'hash_after',
                            'pipeline_run_id', 'review_id', 'recorded_at', 'prev_provenance_hash', 'provenance_hash'),
    'simulated_review': ('review_id', 'record_id', 'pipeline_run_id', 'synthetic_organization_id', 'reviewer_type',
                         'simulation_actor', 'review_scope', 'review_status', 'scripted', 'reviewed_at'),
    'audit_entry': ('audit_id', 'pipeline_run_id', 'synthetic_organization_id', 'action', 'target_ref', 'at',
                    'prev_audit_hash', 'audit_hash'),
}
INTEGER_COLUMNS = ('seed', 'seq', 'scripted')
_TABLES = frozenset(COLUMNS)

_TS = re.compile(r'20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]')
_HEX = re.compile(r'[0-9a-f]{64}')
_ORIGIN_ID = re.compile(r'SYN-[0-9]{6}')
_CRITERION = re.compile(r'CRI-[0-9]{4}')
_ERROR_CODE = re.compile(r'E-[A-Z]{2,12}')
_TEXT = re.compile(r'\[SINTÉTICO\] [^<>\x00-\x1f\x7f]{1,380}')
# Defensa adicional (§11): los detectores de A §5. Heurística, no detección universal.
_PII = (re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), re.compile(r'https?://|www\.', re.I),
        re.compile(r'(?<![\w-])\d{11}(?![\w-])'), re.compile(r'(?<![\w-])\d{8}(?![\w-])'),
        re.compile(r'(?<![\w-])\+?\d[\d ]{8,}\d(?![\w-])'), re.compile(r'data:[\w.+/-]*;base64', re.I),
        re.compile(r'[A-Za-z0-9+/]{40,}={0,2}'))

# ---------------------------------------------------------------- catálogo cerrado de sentencias (§4.1)
# DDL constante: ocho tablas STRICT y sus triggers. Solo lo ejecuta el preflight, con executescript.
SQL_SCHEMA = """
CREATE TABLE tenant_context (
    synthetic_organization_id TEXT NOT NULL PRIMARY KEY CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    tenant_kind TEXT NOT NULL CHECK (tenant_kind = 'synthetic_organization'),
    origin_dataset_version TEXT NOT NULL CHECK (origin_dataset_version = 'f34-synth-1.1.0'),
    simulation_actor TEXT NOT NULL CHECK (simulation_actor = 'SIMREV-' || synthetic_organization_id)
) STRICT;
CREATE TABLE pipeline_run (
    pipeline_run_id TEXT NOT NULL PRIMARY KEY
        CHECK (pipeline_run_id GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    synthetic_organization_id TEXT NOT NULL REFERENCES tenant_context (synthetic_organization_id)
        CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    run_kind TEXT NOT NULL CHECK (run_kind = 'ejecucion_sbx_b'),
    pipeline_version TEXT NOT NULL CHECK (pipeline_version = 'f35sbxb-0'),
    contract_version TEXT NOT NULL CHECK (contract_version = 'f35sbxb-contract-1.0.0'),
    hash_algorithm TEXT NOT NULL CHECK (hash_algorithm = 'f35sbx-content-sha256-v1'),
    seed INTEGER NOT NULL CHECK (seed BETWEEN 0 AND 2147483647),
    clock_start TEXT NOT NULL CHECK (clock_start GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'),
    environment TEXT NOT NULL CHECK (environment = 'sandbox'),
    source_type TEXT NOT NULL CHECK (source_type = 'synthetic')
) STRICT;
CREATE TABLE pipeline_event (
    event_id TEXT NOT NULL PRIMARY KEY
        CHECK (event_id GLOB 'SBBV-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-0[1-7]'),
    pipeline_run_id TEXT NOT NULL REFERENCES pipeline_run (pipeline_run_id)
        CHECK (pipeline_run_id GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    seq INTEGER NOT NULL CHECK (seq BETWEEN 1 AND 7),
    state TEXT NOT NULL CHECK (state IN ('pendiente', 'validando', 'registrado', 'transformado', 'en_revision',
                                         'revisado', 'completado', 'fallido')),
    at TEXT NOT NULL CHECK (at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'),
    error_code TEXT NOT NULL CHECK (error_code = '' OR (error_code GLOB 'E-[A-Z][A-Z]*'
        AND error_code NOT GLOB 'E-*[^A-Z]*' AND length(error_code) <= 14)),
    prev_event_hash TEXT NOT NULL CHECK (length(prev_event_hash) = 64 AND prev_event_hash NOT GLOB '*[^0-9a-f]*'),
    event_hash TEXT NOT NULL CHECK (length(event_hash) = 64 AND event_hash NOT GLOB '*[^0-9a-f]*'),
    CHECK (event_id GLOB ('*-0' || seq)),
    CHECK ((state = 'fallido') = (error_code <> ''))
) STRICT;
CREATE TABLE evidence_source (
    source_id TEXT NOT NULL PRIMARY KEY
        CHECK (source_id GLOB 'SBBS-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    synthetic_organization_id TEXT NOT NULL REFERENCES tenant_context (synthetic_organization_id)
        CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    source_type TEXT NOT NULL CHECK (source_type = 'synthetic'),
    origin_dataset_version TEXT NOT NULL CHECK (origin_dataset_version = 'f34-synth-1.1.0'),
    origin_file TEXT NOT NULL CHECK (origin_file = 'docs/academico/datos-sinteticos/dataset/evidence.csv'),
    origin_file_sha256 TEXT NOT NULL
        CHECK (length(origin_file_sha256) = 64 AND origin_file_sha256 NOT GLOB '*[^0-9a-f]*'),
    origin_record_id TEXT NOT NULL UNIQUE CHECK (origin_record_id GLOB 'SYN-[0-9][0-9][0-9][0-9][0-9][0-9]')
) STRICT;
CREATE TABLE evidence_record (
    synthetic_id TEXT NOT NULL PRIMARY KEY
        CHECK (synthetic_id GLOB 'SBBE-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    synthetic_organization_id TEXT NOT NULL REFERENCES tenant_context (synthetic_organization_id)
        CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    pipeline_run_id TEXT NOT NULL REFERENCES pipeline_run (pipeline_run_id)
        CHECK (pipeline_run_id GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    source_id TEXT NOT NULL UNIQUE REFERENCES evidence_source (source_id)
        CHECK (source_id GLOB 'SBBS-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    criterion_ref TEXT NOT NULL CHECK (criterion_ref GLOB 'CRI-[0-9][0-9][0-9][0-9]'),
    evidence_kind TEXT NOT NULL CHECK (evidence_kind IN ('formulario', 'nota_entrevista', 'prueba')),
    text_synthetic TEXT NOT NULL CHECK (text_synthetic GLOB '[[]SINTÉTICO] *'
        AND length(text_synthetic) BETWEEN 13 AND 392 AND text_synthetic NOT GLOB '*[<>]*'),
    source_type TEXT NOT NULL CHECK (source_type = 'synthetic'),
    environment TEXT NOT NULL CHECK (environment = 'sandbox'),
    hash_algorithm TEXT NOT NULL CHECK (hash_algorithm = 'f35sbx-content-sha256-v1'),
    content_hash TEXT NOT NULL CHECK (length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    validation_status TEXT NOT NULL CHECK (validation_status IN ('valido', 'rechazado')),
    review_status TEXT NOT NULL CHECK (review_status IN ('conforme', 'observado')),
    created_at TEXT NOT NULL CHECK (created_at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]')
) STRICT;
CREATE TABLE evidence_provenance (
    provenance_id TEXT NOT NULL PRIMARY KEY
        CHECK (provenance_id GLOB 'SBBP-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    record_id TEXT NOT NULL UNIQUE REFERENCES evidence_record (synthetic_id)
        CHECK (record_id GLOB 'SBBE-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    synthetic_organization_id TEXT NOT NULL REFERENCES tenant_context (synthetic_organization_id)
        CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    provenance_kind TEXT NOT NULL CHECK (provenance_kind = 'synthetic_fixture'),
    source_id TEXT NOT NULL REFERENCES evidence_source (source_id)
        CHECK (source_id GLOB 'SBBS-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    transformation_id TEXT NOT NULL CHECK (transformation_id = 'T1-normalizacion-nfc-espacios'),
    transformation_version TEXT NOT NULL CHECK (transformation_version = '1'),
    hash_before TEXT NOT NULL CHECK (length(hash_before) = 64 AND hash_before NOT GLOB '*[^0-9a-f]*'),
    hash_after TEXT NOT NULL CHECK (length(hash_after) = 64 AND hash_after NOT GLOB '*[^0-9a-f]*'),
    pipeline_run_id TEXT NOT NULL REFERENCES pipeline_run (pipeline_run_id)
        CHECK (pipeline_run_id GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    review_id TEXT NOT NULL UNIQUE REFERENCES simulated_review (review_id)
        CHECK (review_id GLOB 'SBBH-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    recorded_at TEXT NOT NULL CHECK (recorded_at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'),
    prev_provenance_hash TEXT NOT NULL
        CHECK (length(prev_provenance_hash) = 64 AND prev_provenance_hash NOT GLOB '*[^0-9a-f]*'),
    provenance_hash TEXT NOT NULL CHECK (length(provenance_hash) = 64 AND provenance_hash NOT GLOB '*[^0-9a-f]*')
) STRICT;
CREATE TABLE simulated_review (
    review_id TEXT NOT NULL PRIMARY KEY
        CHECK (review_id GLOB 'SBBH-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    record_id TEXT NOT NULL UNIQUE REFERENCES evidence_record (synthetic_id)
        CHECK (record_id GLOB 'SBBE-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]'),
    pipeline_run_id TEXT NOT NULL REFERENCES pipeline_run (pipeline_run_id)
        CHECK (pipeline_run_id GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    synthetic_organization_id TEXT NOT NULL REFERENCES tenant_context (synthetic_organization_id)
        CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    reviewer_type TEXT NOT NULL CHECK (reviewer_type = 'synthetic_human_simulation'),
    simulation_actor TEXT NOT NULL CHECK (simulation_actor = 'SIMREV-' || synthetic_organization_id),
    review_scope TEXT NOT NULL CHECK (review_scope = 'integridad_y_procedencia'),
    review_status TEXT NOT NULL CHECK (review_status IN ('conforme', 'observado')),
    scripted INTEGER NOT NULL CHECK (scripted = 1),
    reviewed_at TEXT NOT NULL CHECK (reviewed_at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]')
) STRICT;
CREATE TABLE audit_entry (
    audit_id TEXT NOT NULL PRIMARY KEY
        CHECK (audit_id GLOB 'SBBA-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-0[1-8]'),
    pipeline_run_id TEXT NOT NULL REFERENCES pipeline_run (pipeline_run_id)
        CHECK (pipeline_run_id GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    synthetic_organization_id TEXT NOT NULL REFERENCES tenant_context (synthetic_organization_id)
        CHECK (synthetic_organization_id GLOB 'ORG-S[1-3]'),
    action TEXT NOT NULL CHECK (action IN ('fixture_verificado', 'esquema_validado', 'sintetico_verificado',
        'hash_calculado', 'provenance_registrada', 'tenant_validado', 'revision_simulada_registrada',
        'ejecucion_cerrada')),
    target_ref TEXT NOT NULL REFERENCES pipeline_run (pipeline_run_id)
        CHECK (target_ref GLOB 'SBBR-ORG-S[1-3]-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    at TEXT NOT NULL CHECK (at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'),
    prev_audit_hash TEXT NOT NULL CHECK (length(prev_audit_hash) = 64 AND prev_audit_hash NOT GLOB '*[^0-9a-f]*'),
    audit_hash TEXT NOT NULL CHECK (length(audit_hash) = 64 AND audit_hash NOT GLOB '*[^0-9a-f]*'),
    CHECK (target_ref = pipeline_run_id)
) STRICT;
CREATE TRIGGER tenant_context_no_update BEFORE UPDATE ON tenant_context
BEGIN SELECT RAISE(ABORT, 'tenant_context: solo inserción'); END;
CREATE TRIGGER tenant_context_no_delete BEFORE DELETE ON tenant_context
BEGIN SELECT RAISE(ABORT, 'tenant_context: solo inserción'); END;
CREATE TRIGGER pipeline_run_no_update BEFORE UPDATE ON pipeline_run
BEGIN SELECT RAISE(ABORT, 'pipeline_run: solo inserción'); END;
CREATE TRIGGER pipeline_run_no_delete BEFORE DELETE ON pipeline_run
BEGIN SELECT RAISE(ABORT, 'pipeline_run: solo inserción'); END;
CREATE TRIGGER pipeline_event_no_update BEFORE UPDATE ON pipeline_event
BEGIN SELECT RAISE(ABORT, 'pipeline_event: solo inserción'); END;
CREATE TRIGGER pipeline_event_no_delete BEFORE DELETE ON pipeline_event
BEGIN SELECT RAISE(ABORT, 'pipeline_event: solo inserción'); END;
CREATE TRIGGER evidence_source_no_update BEFORE UPDATE ON evidence_source
BEGIN SELECT RAISE(ABORT, 'evidence_source: solo inserción'); END;
CREATE TRIGGER evidence_source_no_delete BEFORE DELETE ON evidence_source
BEGIN SELECT RAISE(ABORT, 'evidence_source: solo inserción'); END;
CREATE TRIGGER evidence_record_no_update BEFORE UPDATE ON evidence_record
BEGIN SELECT RAISE(ABORT, 'evidence_record: solo inserción'); END;
CREATE TRIGGER evidence_record_no_delete BEFORE DELETE ON evidence_record
BEGIN SELECT RAISE(ABORT, 'evidence_record: solo inserción'); END;
CREATE TRIGGER evidence_provenance_no_update BEFORE UPDATE ON evidence_provenance
BEGIN SELECT RAISE(ABORT, 'evidence_provenance: solo inserción'); END;
CREATE TRIGGER evidence_provenance_no_delete BEFORE DELETE ON evidence_provenance
BEGIN SELECT RAISE(ABORT, 'evidence_provenance: solo inserción'); END;
CREATE TRIGGER simulated_review_no_update BEFORE UPDATE ON simulated_review
BEGIN SELECT RAISE(ABORT, 'simulated_review: solo inserción'); END;
CREATE TRIGGER simulated_review_no_delete BEFORE DELETE ON simulated_review
BEGIN SELECT RAISE(ABORT, 'simulated_review: solo inserción'); END;
CREATE TRIGGER audit_entry_no_update BEFORE UPDATE ON audit_entry
BEGIN SELECT RAISE(ABORT, 'audit_entry: solo inserción'); END;
CREATE TRIGGER audit_entry_no_delete BEFORE DELETE ON audit_entry
BEGIN SELECT RAISE(ABORT, 'audit_entry: solo inserción'); END;
CREATE TRIGGER tenant_context_single BEFORE INSERT ON tenant_context
WHEN EXISTS (SELECT 1 FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'tenant_context: fila única'); END;
CREATE TRIGGER pipeline_run_single BEFORE INSERT ON pipeline_run
WHEN EXISTS (SELECT 1 FROM pipeline_run)
BEGIN SELECT RAISE(ABORT, 'pipeline_run: principal único'); END;
CREATE TRIGGER pipeline_run_tenant BEFORE INSERT ON pipeline_run
WHEN NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'pipeline_run: tenant ajeno'); END;
CREATE TRIGGER evidence_source_tenant BEFORE INSERT ON evidence_source
WHEN NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'evidence_source: tenant ajeno'); END;
CREATE TRIGGER evidence_record_tenant BEFORE INSERT ON evidence_record
WHEN NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'evidence_record: tenant ajeno'); END;
CREATE TRIGGER evidence_provenance_tenant BEFORE INSERT ON evidence_provenance
WHEN NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'evidence_provenance: tenant ajeno'); END;
CREATE TRIGGER simulated_review_tenant BEFORE INSERT ON simulated_review
WHEN NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'simulated_review: tenant ajeno'); END;
CREATE TRIGGER audit_entry_tenant BEFORE INSERT ON audit_entry
WHEN NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM tenant_context)
BEGIN SELECT RAISE(ABORT, 'audit_entry: tenant ajeno'); END;
CREATE TRIGGER pipeline_event_order BEFORE INSERT ON pipeline_event
WHEN EXISTS (SELECT 1 FROM pipeline_event WHERE seq >= NEW.seq)
    OR (NEW.seq = 1 AND NEW.state <> 'pendiente')
    OR (NEW.seq > 1 AND NOT EXISTS (SELECT 1 FROM pipeline_event WHERE seq = NEW.seq - 1))
    OR NEW.at < (SELECT clock_start FROM pipeline_run)
    OR NEW.at < (SELECT at FROM pipeline_event WHERE seq = NEW.seq - 1)
BEGIN SELECT RAISE(ABORT, 'pipeline_event: secuencia, estado inicial o instante no admitidos'); END;
CREATE TRIGGER pipeline_event_chain BEFORE INSERT ON pipeline_event
WHEN NEW.prev_event_hash IS NOT CASE WHEN NEW.seq = 1
    THEN '0000000000000000000000000000000000000000000000000000000000000000'
    ELSE (SELECT event_hash FROM pipeline_event WHERE seq = NEW.seq - 1) END
BEGIN SELECT RAISE(ABORT, 'pipeline_event: cadena rota'); END;
CREATE TRIGGER pipeline_event_terminal BEFORE INSERT ON pipeline_event
WHEN EXISTS (SELECT 1 FROM pipeline_event WHERE state IN ('completado', 'fallido'))
BEGIN SELECT RAISE(ABORT, 'pipeline_event: el run ya terminó'); END;
CREATE TRIGGER evidence_provenance_chain BEFORE INSERT ON evidence_provenance
WHEN EXISTS (SELECT 1 FROM evidence_provenance WHERE provenance_id >= NEW.provenance_id)
    OR NEW.prev_provenance_hash IS NOT CASE WHEN EXISTS (SELECT 1 FROM evidence_provenance)
        THEN (SELECT provenance_hash FROM evidence_provenance ORDER BY provenance_id DESC LIMIT 1)
        ELSE '0000000000000000000000000000000000000000000000000000000000000000' END
BEGIN SELECT RAISE(ABORT, 'evidence_provenance: cadena rota'); END;
CREATE TRIGGER audit_entry_chain BEFORE INSERT ON audit_entry
WHEN EXISTS (SELECT 1 FROM audit_entry WHERE audit_id >= NEW.audit_id)
    OR NEW.prev_audit_hash IS NOT CASE WHEN EXISTS (SELECT 1 FROM audit_entry)
        THEN (SELECT audit_hash FROM audit_entry ORDER BY audit_id DESC LIMIT 1)
        ELSE '0000000000000000000000000000000000000000000000000000000000000000' END
BEGIN SELECT RAISE(ABORT, 'audit_entry: cadena rota'); END;
"""

# Preflight (§4.3): conjunto cerrado y enumerado; se ejecuta antes de instalar el autorizador.
SQL_PRE_FOREIGN_KEYS_ON = 'PRAGMA foreign_keys = ON'
SQL_PRE_FOREIGN_KEYS = 'PRAGMA foreign_keys'
SQL_PRE_RECURSIVE_TRIGGERS_ON = 'PRAGMA recursive_triggers = ON'
SQL_PRE_RECURSIVE_TRIGGERS = 'PRAGMA recursive_triggers'
SQL_PRE_TEMP_STORE_ON = 'PRAGMA temp_store = MEMORY'
SQL_PRE_TEMP_STORE = 'PRAGMA temp_store'
SQL_PRE_TRUSTED_SCHEMA_OFF = 'PRAGMA trusted_schema = OFF'
SQL_PRE_TRUSTED_SCHEMA = 'PRAGMA trusted_schema'
SQL_PRE_JOURNAL_MODE = 'PRAGMA journal_mode'
SQL_PRE_TABLE_INFO_TENANT_CONTEXT = 'PRAGMA table_info(tenant_context)'
SQL_PRE_TABLE_INFO_PIPELINE_RUN = 'PRAGMA table_info(pipeline_run)'
SQL_PRE_TABLE_INFO_PIPELINE_EVENT = 'PRAGMA table_info(pipeline_event)'
SQL_PRE_TABLE_INFO_EVIDENCE_SOURCE = 'PRAGMA table_info(evidence_source)'
SQL_PRE_TABLE_INFO_EVIDENCE_RECORD = 'PRAGMA table_info(evidence_record)'
SQL_PRE_TABLE_INFO_EVIDENCE_PROVENANCE = 'PRAGMA table_info(evidence_provenance)'
SQL_PRE_TABLE_INFO_SIMULATED_REVIEW = 'PRAGMA table_info(simulated_review)'
SQL_PRE_TABLE_INFO_AUDIT_ENTRY = 'PRAGMA table_info(audit_entry)'
SQL_PRE_TRIGGERS = "SELECT name FROM sqlite_schema WHERE type = 'trigger' ORDER BY name"

# Catálogo de ejecución: INSERT simple con parámetros, SELECT con ORDER BY explícito y control de transacción.
# El único PRAGMA fuera del preflight es la lectura de database_list (purga y cierre excepcional).
SQL_DATABASE_LIST = 'PRAGMA database_list'
SQL_BEGIN = 'BEGIN'
SQL_COMMIT = 'COMMIT'
SQL_ROLLBACK = 'ROLLBACK'
SQL_POST_CLOSE_PROBE = 'SELECT 1'
SQL_INSERT_TENANT_CONTEXT = ('INSERT INTO tenant_context (synthetic_organization_id, tenant_kind, '
                             'origin_dataset_version, simulation_actor) VALUES (?, ?, ?, ?)')
SQL_INSERT_PIPELINE_RUN = ('INSERT INTO pipeline_run (pipeline_run_id, synthetic_organization_id, run_kind, '
                           'pipeline_version, contract_version, hash_algorithm, seed, clock_start, environment, '
                           'source_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
SQL_INSERT_PIPELINE_EVENT = ('INSERT INTO pipeline_event (event_id, pipeline_run_id, seq, state, at, error_code, '
                             'prev_event_hash, event_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
SQL_INSERT_EVIDENCE_SOURCE = ('INSERT INTO evidence_source (source_id, synthetic_organization_id, source_type, '
                              'origin_dataset_version, origin_file, origin_file_sha256, origin_record_id) '
                              'VALUES (?, ?, ?, ?, ?, ?, ?)')
SQL_INSERT_EVIDENCE_RECORD = ('INSERT INTO evidence_record (synthetic_id, synthetic_organization_id, pipeline_run_id, '
                              'source_id, criterion_ref, evidence_kind, text_synthetic, source_type, environment, '
                              'hash_algorithm, content_hash, validation_status, review_status, created_at) '
                              'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
SQL_INSERT_EVIDENCE_PROVENANCE = ('INSERT INTO evidence_provenance (provenance_id, record_id, '
                                  'synthetic_organization_id, provenance_kind, source_id, transformation_id, '
                                  'transformation_version, hash_before, hash_after, pipeline_run_id, review_id, '
                                  'recorded_at, prev_provenance_hash, provenance_hash) '
                                  'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
SQL_INSERT_SIMULATED_REVIEW = ('INSERT INTO simulated_review (review_id, record_id, pipeline_run_id, '
                               'synthetic_organization_id, reviewer_type, simulation_actor, review_scope, '
                               'review_status, scripted, reviewed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
SQL_INSERT_AUDIT_ENTRY = ('INSERT INTO audit_entry (audit_id, pipeline_run_id, synthetic_organization_id, action, '
                          'target_ref, at, prev_audit_hash, audit_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
SQL_SELECT_TENANT_CONTEXT = ('SELECT synthetic_organization_id, tenant_kind, origin_dataset_version, simulation_actor '
                             'FROM tenant_context ORDER BY synthetic_organization_id')
SQL_SELECT_PIPELINE_RUN = ('SELECT pipeline_run_id, synthetic_organization_id, run_kind, pipeline_version, '
                           'contract_version, hash_algorithm, seed, clock_start, environment, source_type '
                           'FROM pipeline_run ORDER BY pipeline_run_id')
SQL_SELECT_PIPELINE_EVENT = ('SELECT event_id, pipeline_run_id, seq, state, at, error_code, prev_event_hash, '
                             'event_hash FROM pipeline_event ORDER BY seq')
SQL_SELECT_EVIDENCE_SOURCE = ('SELECT source_id, synthetic_organization_id, source_type, origin_dataset_version, '
                              'origin_file, origin_file_sha256, origin_record_id FROM evidence_source '
                              'ORDER BY source_id')
SQL_SELECT_EVIDENCE_RECORD = ('SELECT synthetic_id, synthetic_organization_id, pipeline_run_id, source_id, '
                              'criterion_ref, evidence_kind, text_synthetic, source_type, environment, hash_algorithm, '
                              'content_hash, validation_status, review_status, created_at FROM evidence_record '
                              'ORDER BY synthetic_id')
SQL_SELECT_EVIDENCE_PROVENANCE = ('SELECT provenance_id, record_id, synthetic_organization_id, provenance_kind, '
                                  'source_id, transformation_id, transformation_version, hash_before, hash_after, '
                                  'pipeline_run_id, review_id, recorded_at, prev_provenance_hash, provenance_hash '
                                  'FROM evidence_provenance ORDER BY provenance_id')
SQL_SELECT_SIMULATED_REVIEW = ('SELECT review_id, record_id, pipeline_run_id, synthetic_organization_id, '
                               'reviewer_type, simulation_actor, review_scope, review_status, scripted, reviewed_at '
                               'FROM simulated_review ORDER BY review_id')
SQL_SELECT_AUDIT_ENTRY = ('SELECT audit_id, pipeline_run_id, synthetic_organization_id, action, target_ref, at, '
                          'prev_audit_hash, audit_hash FROM audit_entry ORDER BY audit_id')


# ---------------------------------------------------------------- errores y objeto del almacén
class SbxbStoreError(Exception):
    """Única excepción del almacén. code cumple el patrón de A ^E-[A-Z]{2,12}$."""

    def __init__(self, code, message):
        super().__init__(f'{code}: {message}')
        self.code = code
        self.message = message


class TenantRunStore:
    """Almacén de un tenant y un escenario (§3). Se opera solo con las funciones del módulo: no expone la conexión,
    los cursores, el catálogo ni el índice de origen. No hay registro global de almacenes. Pertenece al hilo que lo
    abre (M01): desde otro hilo ninguna operación toca SQLite."""
    __slots__ = ('_tenant', '_origin', '_conn', '_report', '_owner', '_state', '_outcome', '_run', '_events', '_audit',
                 '_evidence', '_closure')

    def __init__(self, tenant, origin, conn, report, owner):
        self._tenant, self._origin, self._conn, self._report, self._owner = tenant, origin, conn, report, owner
        self._state, self._outcome, self._closure = 'abierto', None, None
        self._run, self._events, self._audit, self._evidence = None, [], [], []

    def __repr__(self):
        return f'<TenantRunStore {self._tenant["synthetic_organization_id"]} {self._state}>'


# ---------------------------------------------------------------- funciones de A (validate_f35sbx.py, congelado en E)
def _canon(obj):
    """JSON canónico de A: claves ordenadas, separadores sin espacios, UTF-8 sin escapar."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def _sha(obj):
    return hashlib.sha256(_canon(obj)).hexdigest()


def _t1(text):
    """T1, exactamente normalize_text de A: Unicode NFC y espacios colapsados."""
    return ' '.join(unicodedata.normalize('NFC', text).split())


def _content_hash(org, origin, criterion, kind, text):
    return _sha({'algorithm': HASH_ALGORITHM, 'synthetic_organization_id': org, 'origin_record_id': origin,
                 'criterion_ref': criterion, 'evidence_kind': kind, 'text': text})


def _chained(item, key):
    """Completa item con su hash de cadena (chain_hash de A: SHA-256 del JSON canónico sin el propio campo)."""
    item[key] = _sha({k: v for k, v in item.items() if k != key})
    return item


# ---------------------------------------------------------------- origen autorizado (§11)
def _load_origin(org):
    """Índice en memoria de las filas F34 autorizadas del tenant: {origin_record_id: (criterio, tipo, texto)}.
    Sin tokens de persona. Lee los cuatro CSV fijos en binario y exige su SHA-256."""
    tables = {}
    for name, rel, digest in F34_INPUTS:
        try:
            with open(os.path.join(_ROOT, *rel.split('/')), 'rb') as handle:
                raw = handle.read()
        except OSError:
            raise SbxbStoreError('E-ORIGEN', f'origen F34 ilegible: {rel}') from None
        if hashlib.sha256(raw).hexdigest() != digest:
            raise SbxbStoreError('E-ORIGEN', f'origen F34 alterado (SHA-256 distinto del manifiesto): {rel}')
        try:
            tables[name] = list(csv.DictReader(re.split(r'(?<=\n)', raw.decode('utf-8'))))
        except (UnicodeDecodeError, csv.Error):
            raise SbxbStoreError('E-ORIGEN', f'origen F34 no legible como CSV UTF-8: {rel}') from None
    try:
        applications = {r['application_token']: r['organization_token'] for r in tables['applications']}
        vacancies = {r['vacancy_token']: r['organization_token'] for r in tables['vacancies']}
        criteria = {r['criterion_id']: vacancies[r['vacancy_token']] for r in tables['criteria']}
        index = {}
        for r in tables['evidence']:
            # La organización se comprueba por el criterio y por la postulación, como hace A.
            if r['state'] == 'vinculada' and r['source_type'] == 'synthetic' and r['source_type_ev'] in EVIDENCE_KINDS \
                    and criteria.get(r['criterion_id']) == org and applications.get(r['application_token']) == org:
                index[r['synthetic_record_id']] = (r['criterion_id'], r['source_type_ev'], r['evidence_text'])
    except KeyError:
        raise SbxbStoreError('E-ORIGEN', 'origen F34 con columnas o referencias distintas del contrato') from None
    if not index:
        raise SbxbStoreError('E-ORIGEN', f'sin filas F34 autorizadas para {org}')
    return index


# ---------------------------------------------------------------- preflight y autorizador (§4.2 y §4.3)
def _require_api():
    """Comprueba la API de sqlite3 directamente, no por la versión de Python."""
    try:
        needed = (sqlite3.Connection.setlimit, sqlite3.Connection.getlimit, sqlite3.Connection.set_authorizer,
                  sqlite3.SQLITE_LIMIT_ATTACHED, sqlite3.SQLITE_OK, sqlite3.SQLITE_DENY, sqlite3.SQLITE_INSERT,
                  sqlite3.SQLITE_READ, sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION, sqlite3.SQLITE_FUNCTION,
                  sqlite3.SQLITE_PRAGMA, sqlite3.ProgrammingError, sqlite3.sqlite_version)
    except AttributeError as e:
        raise SbxbStoreError('E-PREFLIGHT', f'API de sqlite3 ausente ({e})') from None
    return len(needed)


def _columns(rows):
    """[nombre, tipo, notnull, pk] de cada fila de table_info."""
    return [[row[1], row[2], row[3], row[5]] for row in rows]


def _preflight(conn):
    """Fase interna cerrada: versión, PRAGMA efectivos, base sin archivo, límite de adjuntas y esquema fijo.
    Devuelve el informe de solo lectura; cualquier discrepancia es E-PREFLIGHT, sin respaldo silencioso."""
    try:
        version = tuple(int(part) for part in sqlite3.sqlite_version.split('.'))
    except ValueError:
        raise SbxbStoreError('E-PREFLIGHT', 'versión de SQLite no interpretable') from None
    if version < (3, 37, 0):
        raise SbxbStoreError('E-PREFLIGHT', f'SQLite {sqlite3.sqlite_version} sin tablas STRICT (se exige 3.37.0)')
    conn.setlimit(sqlite3.SQLITE_LIMIT_ATTACHED, 0)
    conn.execute(SQL_PRE_FOREIGN_KEYS_ON)
    conn.execute(SQL_PRE_RECURSIVE_TRIGGERS_ON)
    conn.execute(SQL_PRE_TEMP_STORE_ON)
    conn.execute(SQL_PRE_TRUSTED_SCHEMA_OFF)
    conn.executescript(SQL_SCHEMA)
    report = {
        'sqlite_version': sqlite3.sqlite_version,
        'foreign_keys': conn.execute(SQL_PRE_FOREIGN_KEYS).fetchone()[0],
        'recursive_triggers': conn.execute(SQL_PRE_RECURSIVE_TRIGGERS).fetchone()[0],
        'temp_store': conn.execute(SQL_PRE_TEMP_STORE).fetchone()[0],
        'trusted_schema': conn.execute(SQL_PRE_TRUSTED_SCHEMA).fetchone()[0],
        'journal_mode': conn.execute(SQL_PRE_JOURNAL_MODE).fetchone()[0],
        'database_list': [list(row) for row in conn.execute(SQL_DATABASE_LIST).fetchall()],
        'attached_limit': conn.getlimit(sqlite3.SQLITE_LIMIT_ATTACHED),
        'table_info': {
            'tenant_context': _columns(conn.execute(SQL_PRE_TABLE_INFO_TENANT_CONTEXT).fetchall()),
            'pipeline_run': _columns(conn.execute(SQL_PRE_TABLE_INFO_PIPELINE_RUN).fetchall()),
            'pipeline_event': _columns(conn.execute(SQL_PRE_TABLE_INFO_PIPELINE_EVENT).fetchall()),
            'evidence_source': _columns(conn.execute(SQL_PRE_TABLE_INFO_EVIDENCE_SOURCE).fetchall()),
            'evidence_record': _columns(conn.execute(SQL_PRE_TABLE_INFO_EVIDENCE_RECORD).fetchall()),
            'evidence_provenance': _columns(conn.execute(SQL_PRE_TABLE_INFO_EVIDENCE_PROVENANCE).fetchall()),
            'simulated_review': _columns(conn.execute(SQL_PRE_TABLE_INFO_SIMULATED_REVIEW).fetchall()),
            'audit_entry': _columns(conn.execute(SQL_PRE_TABLE_INFO_AUDIT_ENTRY).fetchall()),
        },
        'triggers': [row[0] for row in conn.execute(SQL_PRE_TRIGGERS).fetchall()],
    }
    expected = {table: [[name, 'INTEGER' if name in INTEGER_COLUMNS else 'TEXT', 1, 1 if i == 0 else 0]
                        for i, name in enumerate(names)] for table, names in COLUMNS.items()}
    problems = [name for name, ok in (
        ('foreign_keys', report['foreign_keys'] == 1), ('recursive_triggers', report['recursive_triggers'] == 1),
        ('temp_store', report['temp_store'] == 2), ('trusted_schema', report['trusted_schema'] == 0),
        ('journal_mode', report['journal_mode'] == 'memory'),
        ('database_list', bool(report['database_list']) and all(row[2] == '' for row in report['database_list'])),
        ('attached_limit', report['attached_limit'] == 0), ('esquema', report['table_info'] == expected)) if not ok]
    if problems:
        raise SbxbStoreError('E-PREFLIGHT', f'requisitos no cumplidos: {", ".join(problems)}')
    return report


def _authorize(action, arg1, arg2, database, trigger):
    """Autorizador por lista blanca, instalado tras el preflight. Defensa adicional: la frontera primaria es la API
    cerrada con el catálogo fijo (§4.1)."""
    if action in (sqlite3.SQLITE_INSERT, sqlite3.SQLITE_READ):
        # Un EXISTS (SELECT 1 FROM tabla) de un trigger se notifica como lectura sin columna y sin base (None).
        allowed = arg1 in _TABLES and database in ('main', None)
    elif action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION):
        allowed = True
    elif action == sqlite3.SQLITE_FUNCTION:
        allowed = arg2 in ('raise', 'glob', 'length')
    elif action == sqlite3.SQLITE_PRAGMA:
        allowed = arg1 == 'database_list' and arg2 is None
    else:
        allowed = False
    return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY


# ---------------------------------------------------------------- filas, lecturas y postcondición
def _params(table, row):
    return tuple(row[column] for column in COLUMNS[table])


def _row(table, values):
    item = dict(zip(COLUMNS[table], values))
    if table == 'simulated_review':
        item['scripted'] = item['scripted'] == 1      # booleano del contrato de A, guardado como INTEGER 1
    return item


def _one(cursor):
    """Postcondición de cada escritura (§4.1): exactamente una fila."""
    if cursor.rowcount != 1:
        raise SbxbStoreError('E-SQLITE', f'la escritura afectó {cursor.rowcount} filas; se exige exactamente una')
    return cursor


def _read_tables(conn):
    """Las ocho tablas como listas de dict, con ORDER BY explícito: nunca rowid ni orden implícito."""
    raw = (('tenant_context', conn.execute(SQL_SELECT_TENANT_CONTEXT).fetchall()),
           ('pipeline_run', conn.execute(SQL_SELECT_PIPELINE_RUN).fetchall()),
           ('pipeline_event', conn.execute(SQL_SELECT_PIPELINE_EVENT).fetchall()),
           ('evidence_source', conn.execute(SQL_SELECT_EVIDENCE_SOURCE).fetchall()),
           ('evidence_record', conn.execute(SQL_SELECT_EVIDENCE_RECORD).fetchall()),
           ('evidence_provenance', conn.execute(SQL_SELECT_EVIDENCE_PROVENANCE).fetchall()),
           ('simulated_review', conn.execute(SQL_SELECT_SIMULATED_REVIEW).fetchall()),
           ('audit_entry', conn.execute(SQL_SELECT_AUDIT_ENTRY).fetchall()))
    return {table: [_row(table, values) for values in rows] for table, rows in raw}


def _bundles(tables):
    sources = {s['source_id']: s for s in tables['evidence_source']}
    reviews = {r['record_id']: r for r in tables['simulated_review']}
    provenance = {p['record_id']: p for p in tables['evidence_provenance']}
    return tuple({'source': sources[r['source_id']], 'record': r, 'provenance': provenance[r['synthetic_id']],
                  'review': reviews[r['synthetic_id']]} for r in tables['evidence_record'])


def _observe(conn):
    """Hechos observables para el comprobante y el diagnóstico: conteos, último evento y database_list."""
    tables = _read_tables(conn)
    events = tables['pipeline_event']
    last = events[-1] if events else None
    return {'counts': {table: len(rows) for table, rows in tables.items()},
            'last_event_hash': last['event_hash'] if last else 'no_disponible',
            'final_state': last['state'] if last and last['state'] in TERMINAL else 'no_disponible',
            'file_backed': any(row[2] != '' for row in conn.execute(SQL_DATABASE_LIST).fetchall())}


# ---------------------------------------------------------------- ciclo de vida y cierre excepcional (§6)
def _phase(store):
    return store._outcome if store._state == 'finalizado' else store._state


def _require(store, allowed, connection=True):
    """Matriz de §6.1 y propiedad del hilo (M01). Un error de ciclo o de hilo no cierra el almacén: la operación no
    llega a tocar SQLite ni a cambiar el estado. connection=False para las operaciones que no usan la conexión."""
    if type(store) is not TenantRunStore:
        raise SbxbStoreError('E-CONTRATO', 'se esperaba un almacén abierto con open_tenant_store')
    phase = _phase(store)
    if phase not in allowed:
        if phase == 'purgado':
            raise SbxbStoreError('E-PURGADO', 'el almacén está purgado')
        if phase == 'bloqueado':
            raise SbxbStoreError('E-BLOQUEADO', 'el almacén quedó bloqueado tras un cierre excepcional; solo diagnostic')
        raise SbxbStoreError('E-CICLO', f'operación no admitida con el almacén en {phase}')
    if connection and store._owner != threading.get_ident():
        raise SbxbStoreError('E-HILO', 'el almacén pertenece al hilo que lo abrió: desde otro hilo no se toca SQLite '
                                       'ni cambia su estado')


def _guarded(store, allowed, action):
    """Ejecuta action(conexión) con el almacén en un estado admitido y desde su hilo. Cualquier fallo, incluido un
    sqlite3.Error, activa el cierre excepcional y se propaga como SbxbStoreError (fallo cerrado, §13)."""
    _require(store, allowed)
    try:
        return action(store._conn)
    except SbxbStoreError as e:
        failure = e
    except sqlite3.Error as e:
        failure = SbxbStoreError('E-SQLITE', f'{e.__class__.__name__}: {e}')
    except Exception as e:
        failure = SbxbStoreError('E-CONTRATO', f'entrada no evaluable ({e.__class__.__name__})')
    try:
        _abort(store, failure.code)
    except Exception:           # _abort no lanza; si lo hiciera, el objeto sigue bloqueado y se conserva la causa
        store._state = 'bloqueado'
    raise failure


def _rollback(conn):
    """ROLLBACK de la unidad actual. False si falla: la conexión queda contaminada."""
    try:
        if conn.in_transaction:
            conn.execute(SQL_ROLLBACK)
        return True
    except Exception:
        return False


def _close(conn, owner):
    """Cierra siempre y acredita el cierre solo desde el hilo propietario (M01). Allí, que una consulta posterior lance
    ProgrammingError significa conexión cerrada: el error de hilo ajeno no puede darse. Desde otro hilo, sin acreditar."""
    try:
        conn.close()
    except Exception:
        pass
    if owner != threading.get_ident():
        return False
    try:
        conn.execute(SQL_POST_CLOSE_PROBE)
    except sqlite3.ProgrammingError:
        return True
    except Exception:
        return False
    return False


def _event(run, events, state, at, error_code):
    seq = len(events) + 1
    return _chained({'event_id': f'SBBV-{run["pipeline_run_id"][5:]}-{seq:02d}', 'pipeline_run_id': run['pipeline_run_id'],
                     'seq': seq, 'state': state, 'at': at, 'error_code': error_code,
                     'prev_event_hash': events[-1]['event_hash'] if events else GENESIS}, 'event_hash')


def _commit_failed(store, conn, code):
    """Registra fallido en su propia transacción. Devuelve (conexión utilizable, evento releído o no_disponible):
    solo se afirma el evento si se confirmó y se releyó igual."""
    event = _event(store._run, store._events, 'fallido', store._events[-1]['at'], code)
    try:
        conn.execute(SQL_BEGIN)
        _one(conn.execute(SQL_INSERT_PIPELINE_EVENT, _params('pipeline_event', event)))
        conn.execute(SQL_COMMIT)
    except Exception:
        return _rollback(conn), 'no_disponible'
    try:
        stored = _read_tables(conn)['pipeline_event']
    except Exception:
        return False, 'no_disponible'
    if not stored or stored[-1] != event:
        return True, 'no_disponible'
    store._events.append(event)
    return True, dict(event)


def _closure(store, kind, code, failed, failed_record, observed, verified):
    """Comprobante (§9) o diagnóstico (§6.2): solo hechos observados, encadenado al último evento."""
    facts = observed if type(observed) is dict else {}
    record = {'closure_kind': kind,
              'pipeline_run_id': store._run['pipeline_run_id'] if store._run else 'sin_run',
              'synthetic_organization_id': store._tenant['synthetic_organization_id'],
              'final_state': facts.get('final_state', 'no_disponible'),
              'failed_event': failed,
              'failed_event_record': failed_record,
              'error_code': code,
              'last_event_hash': facts.get('last_event_hash', 'no_disponible'),
              'counts': facts.get('counts', 'no_disponible'),
              'file_backed': facts.get('file_backed', 'no_disponible'),
              'observed': observed,
              'connection': ('CONNECTION_ABORTED' if kind == 'aborto' else 'CLOSED') if verified else 'CLOSE_UNVERIFIED',
              'post_close_check': 'ProgrammingError' if verified else 'no_verificado'}
    record['receipt_hash'] = _sha(record)
    return record


def _receipt(store, kind, code, failed, failed_record, observed, verified):
    """Construcción falible del comprobante o del diagnóstico (M02). Si _closure falla, se degrada a un mínimo veraz:
    los hechos ya establecidos (tipo de cierre, código del fallo original, evento fallido y estado de la conexión), lo
    disponible del run y del tenant, y no_disponible en lo demás, con la causa en receipt_error. No inventa hashes,
    conteos, FAILED ni CLOSED. Nunca lanza."""
    try:
        return _closure(store, kind, code, failed, failed_record, observed, verified)
    except Exception as e:
        reason = e.__class__.__name__
    record = {'closure_kind': kind, 'pipeline_run_id': 'no_disponible', 'synthetic_organization_id': 'no_disponible',
              'final_state': 'no_disponible', 'failed_event': failed, 'failed_event_record': 'no_disponible',
              'error_code': code, 'last_event_hash': 'no_disponible', 'counts': 'no_disponible',
              'file_backed': 'no_disponible', 'observed': 'no_disponible',
              'connection': ('CONNECTION_ABORTED' if kind == 'aborto' else 'CLOSED') if verified else 'CLOSE_UNVERIFIED',
              'post_close_check': 'ProgrammingError' if verified else 'no_verificado', 'receipt_error': reason}
    try:
        run_id = store._run['pipeline_run_id'] if store._run is not None else 'sin_run'
        record['pipeline_run_id'] = run_id if type(run_id) is str else 'no_disponible'
    except Exception:
        pass
    try:
        org = store._tenant['synthetic_organization_id']
        record['synthetic_organization_id'] = org if type(org) is str else 'no_disponible'
    except Exception:
        pass
    try:
        record['receipt_hash'] = _sha(record)
    except Exception:
        record['receipt_hash'] = 'no_disponible'
    return record


def _abort(store, code, purge_requested=False):
    """Cierre excepcional (§6.2). El objeto queda bloqueado antes de tocar la conexión; ROLLBACK; fallido solo si es
    válido y se confirma; hechos observados; cierre en finally; comprobante falible con respaldo veraz (M02). Nunca
    lanza: lo que no se pueda leer queda como no_disponible y se conserva el código del fallo original."""
    conn, store._state = store._conn, 'bloqueado'
    failed, failed_record, observed, verified = 'FAILED_EVENT_UNAVAILABLE', 'no_disponible', 'no_disponible', False
    try:
        usable = _rollback(conn)
        if usable and store._run is not None and store._events and store._events[-1]['state'] not in TERMINAL:
            usable, failed_record = _commit_failed(store, conn, code)
            if failed_record != 'no_disponible':
                failed = 'FAILED_EVENT_COMMITTED'
        if usable:
            observed = _observe(conn)
    except Exception:           # un fallo inesperado no impide el cierre: lo no observado queda no_disponible
        pass
    finally:
        verified = _close(conn, store._owner)
        store._conn = None
    store._closure = _receipt(store, 'aborto', code, failed, failed_record, observed, verified)
    store._state = 'purgado' if purge_requested and verified else 'bloqueado'
    return store._closure


def _copy(value):
    return json.loads(json.dumps(value))


def _safe_copy(record):
    """Copia del comprobante para el llamador; si la copia profunda falla, una copia superficial, nunca la interna."""
    try:
        return _copy(record)
    except Exception:
        return dict(record)


# ---------------------------------------------------------------- validación de entradas (§8, §11 y §13)
def _instant(value, floor, what):
    if type(value) is not str or not _TS.fullmatch(value):
        raise SbxbStoreError('E-CONTRATO', f'{what}: se exige un instante lógico AAAA-MM-DDTHH:MM:SS')
    if value < floor:
        raise SbxbStoreError('E-CONTRATO', f'{what}: anterior a {floor}')


def _check_tenant(tenant):
    if type(tenant) is not dict or 'synthetic_organization_id' not in tenant:
        raise SbxbStoreError('E-TENANT', 'se exige el contexto SyntheticTenantContext del tenant')
    if set(tenant) != set(TENANT_FIELDS):
        raise SbxbStoreError('E-CONTRATO', 'el contexto del tenant debe traer exactamente sus cuatro campos')
    org = tenant['synthetic_organization_id']
    if type(org) is not str or org not in TENANTS:
        raise SbxbStoreError('E-TENANT', 'organización sintética fuera de ORG-S1..ORG-S3')
    if tenant['simulation_actor'] != f'SIMREV-{org}':
        raise SbxbStoreError('E-TENANT', 'simulation_actor de otro tenant')
    if tenant['tenant_kind'] != 'synthetic_organization' or tenant['origin_dataset_version'] != DATASET_VERSION:
        raise SbxbStoreError('E-CONTRATO', 'tenant_kind u origin_dataset_version distintos del contrato')
    return {field: tenant[field] for field in TENANT_FIELDS}


def _new_audit(store, action, at):
    if action not in AUDIT_ACTIONS:
        raise SbxbStoreError('E-CONTRATO', 'acción de auditoría fuera del enum de A')
    if len(store._audit) >= len(AUDIT_ACTIONS):
        raise SbxbStoreError('E-CONTRATO', 'auditoría completa: como máximo ocho entradas (Q9)')
    _instant(at, store._audit[-1]['at'] if store._audit else store._run['clock_start'], 'at')
    run_id = store._run['pipeline_run_id']
    seq = len(store._audit) + 1
    return _chained({'audit_id': f'SBBA-{run_id[5:]}-{seq:02d}', 'pipeline_run_id': run_id,
                     'synthetic_organization_id': store._tenant['synthetic_organization_id'], 'action': action,
                     'target_ref': run_id, 'at': at,
                     'prev_audit_hash': store._audit[-1]['audit_hash'] if store._audit else GENESIS}, 'audit_hash')


def _evidence_bundle(store, evidence):
    """Comprobaciones de §11, en su orden, antes de persistir. Devuelve las cuatro filas con identificadores y
    cadena asignados. El contenido persistido es exactamente una fila F34 autorizada transformada solo por T1."""
    if type(evidence) is not dict or set(evidence) != set(EVIDENCE_FIELDS) or \
            any(type(evidence[field]) is not str for field in EVIDENCE_FIELDS):
        raise SbxbStoreError('E-CONTRATO', 'la evidencia debe traer exactamente los doce campos del contrato, como texto')
    if evidence['evidence_kind'] not in EVIDENCE_KINDS:
        raise SbxbStoreError('E-PROHIBIDO', 'tipo de evidencia excluido: solo formulario, nota_entrevista o prueba')
    for field, pattern in (('origin_record_id', _ORIGIN_ID), ('origin_file_sha256', _HEX), ('criterion_ref', _CRITERION),
                           ('hash_before', _HEX), ('content_hash', _HEX)):
        if not pattern.fullmatch(evidence[field]):
            raise SbxbStoreError('E-CONTRATO', f'{field}: formato distinto del contrato')
    if evidence['validation_status'] not in VALIDATION_STATUSES or evidence['review_status'] not in REVIEW_STATUSES:
        raise SbxbStoreError('E-CONTRATO', 'validation_status o review_status fuera del enum de A')
    for field in ('created_at', 'recorded_at', 'reviewed_at'):
        _instant(evidence[field], store._run['clock_start'], field)
    if evidence['recorded_at'] < evidence['created_at']:
        raise SbxbStoreError('E-CONTRATO', 'procedencia registrada antes que la evidencia')
    org, origin = store._tenant['synthetic_organization_id'], evidence['origin_record_id']
    # 1. Fila F34 autorizada del tenant (referencia, origen permitido y tenant coherente), una vez por run.
    row = store._origin.get(origin)
    if row is None:
        raise SbxbStoreError('E-ORIGEN', 'origin_record_id no es una fila F34 autorizada de este tenant')
    if any(bundle['source']['origin_record_id'] == origin for bundle in store._evidence):
        raise SbxbStoreError('E-ORIGEN', 'la fila F34 ya se usó en este run')
    criterion, kind, text = row
    # 2. SHA-256 del archivo de origen.
    if evidence['origin_file_sha256'] != F34_INPUTS[0][2]:
        raise SbxbStoreError('E-ORIGEN', 'origin_file_sha256 distinto del de evidence.csv')
    # 3. Criterio y tipo de la propia fila.
    if evidence['criterion_ref'] != criterion or evidence['evidence_kind'] != kind:
        raise SbxbStoreError('E-ORIGEN', 'criterion_ref o evidence_kind distintos de su fila F34')
    ordinal = len(store._evidence) + 1
    run_id = store._run['pipeline_run_id']
    namespace = run_id[5:]
    source = {'source_id': f'SBBS-{namespace}-{ordinal:06d}', 'synthetic_organization_id': org,
              'source_type': 'synthetic', 'origin_dataset_version': DATASET_VERSION, 'origin_file': ORIGIN_FILE,
              'origin_file_sha256': evidence['origin_file_sha256'], 'origin_record_id': origin}
    record = {'synthetic_id': f'SBBE-{namespace}-{ordinal:06d}', 'synthetic_organization_id': org,
              'pipeline_run_id': run_id, 'source_id': source['source_id'], 'criterion_ref': criterion,
              'evidence_kind': kind, 'text_synthetic': evidence['text_synthetic'], 'source_type': 'synthetic',
              'environment': 'sandbox', 'hash_algorithm': HASH_ALGORITHM, 'content_hash': evidence['content_hash'],
              'validation_status': evidence['validation_status'], 'review_status': evidence['review_status'],
              'created_at': evidence['created_at']}
    # 4. Los seis marcadores synthetic-only de A, con el texto sin marcado ni caracteres de control.
    markers = (record['synthetic_id'].startswith(f'SBBE-{org}-'), _TEXT.fullmatch(record['text_synthetic']) is not None,
               record['source_type'] == 'synthetic', record['environment'] == 'sandbox',
               record['hash_algorithm'] == HASH_ALGORITHM, record['synthetic_organization_id'] in TENANTS)
    if not all(markers):
        raise SbxbStoreError('E-PROHIBIDO', 'marcador synthetic-only ausente o texto con marcado')
    # 5. El texto es, carácter a carácter, T1 del texto de su fila.
    if record['text_synthetic'] != _t1(text):
        raise SbxbStoreError('E-ORIGEN', 'el texto no es T1 del texto de su fila F34')
    # 6. Hashes recalculados con la función de A sobre el texto original y el transformado.
    if evidence['hash_before'] != _content_hash(org, origin, criterion, kind, text) or \
            evidence['content_hash'] != _content_hash(org, origin, criterion, kind, _t1(text)):
        raise SbxbStoreError('E-HASH', 'hash_before o content_hash no coinciden con los recalculados')
    # Defensa adicional: heurísticas de PII de A sobre el texto.
    if any(pattern.search(record['text_synthetic']) for pattern in _PII):
        raise SbxbStoreError('E-PROHIBIDO', 'el texto activa una heurística de datos personales')
    review = {'review_id': f'SBBH-{namespace}-{ordinal:06d}', 'record_id': record['synthetic_id'],
              'pipeline_run_id': run_id, 'synthetic_organization_id': org,
              'reviewer_type': 'synthetic_human_simulation', 'simulation_actor': store._tenant['simulation_actor'],
              'review_scope': 'integridad_y_procedencia', 'review_status': evidence['review_status'], 'scripted': True,
              'reviewed_at': evidence['reviewed_at']}
    provenance = _chained({'provenance_id': f'SBBP-{namespace}-{ordinal:06d}', 'record_id': record['synthetic_id'],
                           'synthetic_organization_id': org, 'provenance_kind': 'synthetic_fixture',
                           'source_id': source['source_id'], 'transformation_id': TRANSFORMATION[0],
                           'transformation_version': TRANSFORMATION[1], 'hash_before': evidence['hash_before'],
                           'hash_after': evidence['content_hash'], 'pipeline_run_id': run_id,
                           'review_id': review['review_id'], 'recorded_at': evidence['recorded_at'],
                           'prev_provenance_hash': store._evidence[-1]['provenance']['provenance_hash']
                           if store._evidence else GENESIS}, 'provenance_hash')
    return {'source': source, 'record': record, 'provenance': provenance, 'review': review}


# ---------------------------------------------------------------- API interna (§13)
def open_tenant_store(tenant):
    """Abre el almacén de un tenant: origen autorizado, preflight, esquema, autorizador y fila tenant_context."""
    row = _check_tenant(tenant)
    origin = _load_origin(row['synthetic_organization_id'])
    _require_api()
    owner = threading.get_ident()
    conn = sqlite3.connect(':memory:', isolation_level=None)
    try:
        report = _preflight(conn)
        conn.set_authorizer(_authorize)
        conn.execute(SQL_BEGIN)
        _one(conn.execute(SQL_INSERT_TENANT_CONTEXT, _params('tenant_context', row)))
        conn.execute(SQL_COMMIT)
    except Exception as e:
        _close(conn, owner)
        if type(e) is SbxbStoreError and e.code == 'E-PREFLIGHT':
            raise
        raise SbxbStoreError('E-PREFLIGHT', f'el almacén no se abre ({e.__class__.__name__}: {e})') from None
    return TenantRunStore(row, origin, conn, report, owner)


def create_run(store, seed, clock_start):
    """Crea el principal inmutable y el evento pendiente en una transacción. Una vez por almacén."""
    def unit(conn):
        if type(seed) is not int or not 0 <= seed <= 2147483647:
            raise SbxbStoreError('E-CONTRATO', 'seed: entero de 0 a 2147483647')
        _instant(clock_start, '', 'clock_start')
        org = store._tenant['synthetic_organization_id']
        run = {'pipeline_run_id': f'SBBR-{org}-{seed:010d}', 'synthetic_organization_id': org, 'run_kind': RUN_KIND,
               'pipeline_version': PIPELINE_VERSION, 'contract_version': CONTRACT_VERSION,
               'hash_algorithm': HASH_ALGORITHM, 'seed': seed, 'clock_start': clock_start, 'environment': 'sandbox',
               'source_type': 'synthetic'}
        event = _event(run, [], 'pendiente', clock_start, '')
        conn.execute(SQL_BEGIN)
        _one(conn.execute(SQL_INSERT_PIPELINE_RUN, _params('pipeline_run', run)))
        _one(conn.execute(SQL_INSERT_PIPELINE_EVENT, _params('pipeline_event', event)))
        conn.execute(SQL_COMMIT)
        store._run, store._events, store._state = run, [event], 'activo'
        return dict(run)
    return _guarded(store, ('abierto',), unit)


def append_event(store, state, at, error_code='', audit_action=None):
    """Añade el siguiente evento del camino de A (o fallido), atómico con su auditoría si se indica (Q7)."""
    _require(store, ('activo',))
    current = store._events[-1]['state']
    if state in EVENT_STATES and state not in (PATH[PATH.index(current) + 1], 'fallido'):
        raise SbxbStoreError('E-CICLO', f'transición no admitida: {current} → {state}')

    def unit(conn):
        if state not in EVENT_STATES:
            raise SbxbStoreError('E-CONTRATO', 'estado fuera del contrato')
        _instant(at, store._events[-1]['at'], 'at')
        if state == 'fallido':
            if type(error_code) is not str or not _ERROR_CODE.fullmatch(error_code):
                raise SbxbStoreError('E-CONTRATO', 'fallido exige un código E-[A-Z]{2,12}')
        elif error_code != '':
            raise SbxbStoreError('E-CONTRATO', 'error_code solo se admite con fallido')
        event = _event(store._run, store._events, state, at, error_code)
        entry = _new_audit(store, audit_action, at) if audit_action is not None else None
        conn.execute(SQL_BEGIN)
        _one(conn.execute(SQL_INSERT_PIPELINE_EVENT, _params('pipeline_event', event)))
        if entry is not None:
            _one(conn.execute(SQL_INSERT_AUDIT_ENTRY, _params('audit_entry', entry)))
        conn.execute(SQL_COMMIT)
        store._events.append(event)
        if entry is not None:
            store._audit.append(entry)
        if state in TERMINAL:
            store._state, store._outcome = 'finalizado', state
        return {'event': dict(event), 'audit': dict(entry) if entry is not None else None}
    return _guarded(store, ('activo',), unit)


def append_evidence(store, evidence):
    """Registra fuente, evidencia, revisión simulada y procedencia en una transacción, en orden FK (Q7)."""
    def unit(conn):
        bundle = _evidence_bundle(store, evidence)
        conn.execute(SQL_BEGIN)
        _one(conn.execute(SQL_INSERT_EVIDENCE_SOURCE, _params('evidence_source', bundle['source'])))
        _one(conn.execute(SQL_INSERT_EVIDENCE_RECORD, _params('evidence_record', bundle['record'])))
        _one(conn.execute(SQL_INSERT_SIMULATED_REVIEW, _params('simulated_review', bundle['review'])))
        _one(conn.execute(SQL_INSERT_EVIDENCE_PROVENANCE, _params('evidence_provenance', bundle['provenance'])))
        conn.execute(SQL_COMMIT)
        store._evidence.append(bundle)
        return _copy(bundle)
    return _guarded(store, ('activo',), unit)


def append_audit(store, action, at):
    """Añade una entrada de auditoría encadenada, con una acción del enum de A."""
    def unit(conn):
        entry = _new_audit(store, action, at)
        conn.execute(SQL_BEGIN)
        _one(conn.execute(SQL_INSERT_AUDIT_ENTRY, _params('audit_entry', entry)))
        conn.execute(SQL_COMMIT)
        store._audit.append(entry)
        return dict(entry)
    return _guarded(store, ('activo',), unit)


def read_run(store):
    """Principal del run."""
    return _guarded(store, ('activo', 'completado', 'fallido'), lambda conn: _read_tables(conn)['pipeline_run'][0])


def list_events(store):
    """Eventos en orden de seq."""
    return _guarded(store, ('activo', 'completado', 'fallido'),
                    lambda conn: tuple(_read_tables(conn)['pipeline_event']))


def current_state(store):
    """Estado del último evento confirmado."""
    return _guarded(store, ('activo', 'completado', 'fallido'),
                    lambda conn: _read_tables(conn)['pipeline_event'][-1]['state'])


def list_audit(store):
    """Auditoría en orden de ordinal."""
    return _guarded(store, ('activo', 'completado'), lambda conn: tuple(_read_tables(conn)['audit_entry']))


def list_evidence(store):
    """Evidencias con su fuente, procedencia y revisión, en orden de ordinal."""
    return _guarded(store, ('activo', 'completado'), lambda conn: _bundles(_read_tables(conn)))


def snapshot(store):
    """Bytes del JSON canónico de las ocho tablas. Sin resultado parcial tras fallido (DH-B10)."""
    return _guarded(store, ('activo', 'completado'), lambda conn: _canon(_read_tables(conn)))


def preflight_report(store):
    """Copia de solo lectura de los hechos del preflight. No hay API de PRAGMA ni acceso a la conexión."""
    _require(store, ('abierto', 'activo', 'completado', 'fallido', 'bloqueado', 'purgado'), connection=False)
    return _copy(store._report)


def diagnostic(store):
    """Diagnóstico del cierre excepcional; solo en bloqueado. No usa la conexión."""
    _require(store, ('bloqueado',), connection=False)
    return _safe_copy(store._closure)


def purge(store):
    """Cierra la conexión y devuelve el comprobante en memoria (§9). Con el run activo, cierre excepcional
    E-ABORTADO. La purga nunca es un borrado de filas: no existe ninguna sentencia de borrado. El objeto queda
    bloqueado antes de tocar la conexión y el comprobante es falible con respaldo veraz (M02)."""
    _require(store, ('abierto', 'activo', 'completado', 'fallido'))
    if store._state == 'activo':
        record = _abort(store, 'E-ABORTADO', purge_requested=True)
    else:
        conn, observed, verified, store._state = store._conn, 'no_disponible', False, 'bloqueado'
        try:
            observed = _observe(conn)
        except Exception:       # lo no observado queda no_disponible; el cierre sigue
            pass
        finally:
            verified = _close(conn, store._owner)
            store._conn = None
        store._closure = record = _receipt(store, 'purga', '', 'no_aplica', 'no_aplica', observed, verified)
        store._state = 'purgado' if verified else 'bloqueado'
    if record['connection'] == 'CLOSE_UNVERIFIED':
        raise SbxbStoreError('E-SQLITE', 'no se pudo comprobar el cierre de la conexión; ver diagnostic')
    return _safe_copy(record)
