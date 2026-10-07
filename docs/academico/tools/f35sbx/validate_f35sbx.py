"""F35-SBX-A — Validación del diseño, el contrato y los fixtures del pipeline experimental de evidencia sintética.

Solo biblioteca estándar. F35-SBX-A no ejecuta ningún pipeline (DH-04): verifica documentos, un contrato JSON cerrado,
fixtures sintéticos pequeños derivados de F34, su manifest y sus hashes, y recalcula de forma independiente todo lo
que esos artefactos declaran. Reutiliza los analizadores de proposiciones y de estados de validate_f34e.py.

  DOC   documentos obligatorios, encabezado de fase y enlaces relativos válidos.
  TSB   threat model F35-SBX: TSB-01..TSB-17, cada amenaza con control, evidencia y casos negativos existentes.
  TRZ   plan de pruebas y criterios: todos los casos NS-xx, ACS-01..10 y REV-01..14 documentados.
  STA   estados críticos declarados una vez en el README y coherentes con la puerta G0-SBX vigente (no se asumen).
  CLM   ninguna afirmación positiva de categorías prohibidas (parser de proposiciones de F34E).
  PHS   F35 productiva, F36–F40, alcance C y G0 real nunca iniciados ni habilitados; RF-23/RF-21 sin modificar.
  CON   contrato cerrado: additionalProperties=false, exactamente los campos permitidos y restricciones clave.
  SCH   cada fixture cumple el contrato (validador JSON Schema mínimo; palabras clave desconocidas fallan).
  SYN   seis marcadores synthetic-only en cada registro.
  PII   sin PII: nombres de campo, correo, URL, DNI, RUC o teléfono.
  MED   sin media, binarios, base64 ni data URI; sin archivos ajenos en evidencia-sbx/.
  CAP   sin capacidades prohibidas: scoring, ranking, recomendación, selección, OCR, parsing, extracción,
        embeddings, vectores, búsqueda semántica, LLM ni inferencias sobre personas.
  PER   sin tokens ni campos de persona (APP-, PER-S-, EV-…; DH-06).
  ISO   aislamiento por tenant sintético ORG-S1..S3.
  HSH   hashes recalculados: contenido, antes/después y cadenas de eventos, provenance y auditoría.
  PRV   provenance completa y enlazada: fuente, transformación, run, revisión, tenant e instante.
  ORI   origen F34 verificable: registro existente, mismo texto normalizado, misma organización, selección determinista.
  RUN   run existente, eventos contiguos y en orden, auditoría completa, instantes monótonos.
  REV   SyntheticHumanReview limitada a integridad y procedencia: review_scope = integridad_y_procedencia (DH-05).
  STO   sin persistencia ni integración productiva; sin lectura de g0-evidence/adjuntos.
  MAN   manifest: archivos exactos, SHA-256, conteos y referencias F34.
  GOV   gobierno: ciclo de vida de F35-SBX-A, exactamente INICIADA o CERRADA (coherente en los tres documentos;
        CERRADA exige auditoría independiente PASS, regresión GREEN registrada y F35-SBX-B NO INICIADA) y estados
        G0 sin cambios.
  GATE  G0 real NO APROBADA y G0-SBX vigente; si la puerta cae, el trabajo SBX se detiene.
  DEP   solo biblioteca estándar autorizada en tools/f35sbx (sin sqlite3 en F35-SBX-A, DH-07).
  GIT   solo evidencia-sbx/** (md/json), tools/f35sbx/** (py), la adaptación DH-02 y el gobierno; falla cerrado.
Incluye casos negativos en memoria y un control no forzado (G0-SBX NO APROBADA y F35-SBX BLOQUEADA).
Uso: python docs/academico/tools/f35sbx/validate_f35sbx.py
"""
import ast
import copy
import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
ACAD = os.path.join(ROOT, 'docs', 'academico')
SBX = os.path.join(ACAD, 'evidencia-sbx')
REL_SBX = 'docs/academico/evidencia-sbx/'
REL_TOOLS = 'docs/academico/tools/f35sbx/'
# Base fija de F35-SBX-A: main publicado tras el cierre de F34E y el handoff macOS.
BASE = 'b67f6443fb2bb71e736a60a645a15bd1fa0e7de6'
DOCS = ['README.md', 'F35SBX_Alcance.md', 'F35SBX_Arquitectura.md', 'F35SBX_Contratos_Datos.md', 'F35SBX_Provenance.md',
        'F35SBX_Revision_Humana_Simulada.md', 'F35SBX_Aislamiento_y_Almacenamiento.md', 'F35SBX_Threat_Model.md',
        'F35SBX_Plan_Pruebas.md', 'F35SBX_Criterios_Cierre_y_Revocacion.md']
CONTRACT = 'contrato/f35sbx_contract.json'
ORGS = ['ORG-S1', 'ORG-S2', 'ORG-S3']
FIXTURES = {o: f'fixtures/{o}_evidencias.json' for o in ORGS}
MANIFEST = 'fixtures/manifest.json'
ARTIFACTS = [CONTRACT, MANIFEST, *FIXTURES.values()]
GOVERNANCE = ['CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md']
BASELINE_DOC = 'docs/academico/ACADEMIC_BASELINE.md'          # solo registra el cierre (convención F33–F34E)
STARTED = ('F35-SBX-A INICIADA — diseño, contratos, fixtures sintéticos y validación académica. '
           'Sin runtime productivo ni capacidades de alcance C.')
NOT_STARTED = 'AÚN NO INICIADA'
CLOSED = ('F35-SBX-A CERRADA — diseño, contratos, fixtures sintéticos y validador completados, tras auditoría '
          'independiente PASS. Sin runtime productivo ni capacidades de alcance C. F35-SBX-B NO INICIADA.')
LIFECYCLE_PHRASES = {'INICIADA': STARTED, 'CERRADA': CLOSED}
PHASE_STATE_RX = re.compile(r'F35-SBX-A\s+([A-ZÁÉÍÓÚÑ]{4,})\b')          # cualquier estado en mayúsculas
SBXB_STATE_RX = re.compile(r'F35-SBX-B\s+(?!NO\s+INICIADA)([A-ZÁÉÍÓÚÑ]{2,})\b')
GOV_FIXED = {'G0 real': 'NO APROBADA', 'G0-09': 'CUMPLIDO', 'G0-14': 'CUMPLIDO', 'G0-02': 'PENDIENTE EXTERNO',
             'G0-03': 'PENDIENTE EXTERNO', 'G0-12': 'PENDIENTE EXTERNO', 'ADR-005': 'PROPUESTA',
             'F35 productiva': 'BLOQUEADA', 'F36–F40': 'BLOQUEADAS', 'Alcance C': 'BLOQUEADO',
             'Datos reales': 'PROHIBIDOS'}
GATE_DECISION = os.path.join(ACAD, 'g0-sandbox', 'F34E_Decision_G0_SBX.md')
GATE_MATRIX = os.path.join(ACAD, 'g0-sandbox', 'F34E_Matriz_Criterios_G0_SBX.md')
G0_REAL_DECISION = os.path.join(ACAD, 'g0-evidence', 'F34B_Decision_G0.md')
F34_DIR = os.path.join(ACAD, 'datos-sinteticos', 'dataset')
F34_EVIDENCE = 'docs/academico/datos-sinteticos/dataset/evidence.csv'
F34_MANIFEST = 'docs/academico/datos-sinteticos/dataset/manifest.json'
F34_VERSION = 'f34-synth-1.1.0'
HASH_ALG = 'f35sbx-content-sha256-v1'
CONTRACT_VERSION = 'f35sbx-contract-1.0.0'
MANIFEST_VERSION = 'f35sbx-manifest-1.0.0'
PIPELINE_VERSION = 'f35sbx-design-0'
RUN_KIND = 'oraculo_sbx_a'
MARKER = '[SINTÉTICO]'
GENESIS = '0' * 64
PER_TENANT = 2
EVIDENCE_KINDS = ['formulario', 'nota_entrevista', 'prueba']        # sin «cv» ni «documento» (DH-06, alcance C)
TRANSFORM = ('T1-normalizacion-nfc-espacios', '1')
LIFECYCLE = ['pendiente', 'validando', 'registrado', 'transformado', 'en_revision', 'revisado', 'completado']
RUN_STATES = LIFECYCLE + ['fallido', 'purgado']
AUDIT_ACTIONS = ['fixture_verificado', 'esquema_validado', 'sintetico_verificado', 'hash_calculado',
                 'provenance_registrada', 'tenant_validado', 'revision_simulada_registrada', 'ejecucion_cerrada']
REVIEW_SCOPE = 'integridad_y_procedencia'
REVIEW_STATUSES = ['conforme', 'observado']
REVIEWER_TYPE = 'synthetic_human_simulation'
HASH_FIELDS = ['algorithm', 'criterion_ref', 'evidence_kind', 'origin_record_id', 'synthetic_organization_id', 'text']
CRITICAL = ['G0 real', 'G0-SBX', 'F35 productiva', 'F35-SBX', 'F36–F40', 'Alcance C']
TSB_IDS = [f'TSB-{i:02d}' for i in range(1, 18)]
ACS_IDS = [f'ACS-{i:02d}' for i in range(1, 11)]
REV_IDS = [f'REV-{i:02d}' for i in range(1, 15)]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(mod)
    return mod


V34E = load_module('f35sbx_f34e_policy', os.path.join(ACAD, 'tools', 'f34e', 'validate_f34e.py'))
SCOPE = load_module('f35sbx_scope', os.path.join(HERE, 'f35sbx_scope.py'))


# ---------------------------------------------------------------- hashes y normalización (contrato f35sbx)
def canon(obj):
    """JSON canónico: claves ordenadas, separadores sin espacios, UTF-8 sin escapar."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(obj):
    return hashlib.sha256(canon(obj)).hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def normalize_text(text):
    """T1 (única transformación permitida): Unicode NFC y espacios colapsados. Pura, determinista e idempotente."""
    return ' '.join(unicodedata.normalize('NFC', text).split())


def content_hash(org, origin, criterion, kind, text):
    """SyntheticEvidenceHash, algoritmo f35sbx-content-sha256-v1 (sin tokens de persona)."""
    return sha({'algorithm': HASH_ALG, 'synthetic_organization_id': org, 'origin_record_id': origin,
                'criterion_ref': criterion, 'evidence_kind': kind, 'text': text})


def chain_hash(item, key):
    return sha({k: v for k, v in item.items() if k != key})


# ---------------------------------------------------------------- contrato esperado (doble llave con el archivo)
ORG_RX = '^ORG-S[1-3]$'
TS_RX = '^20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$'
HASH_RX = '^[0-9a-f]{64}$'


def _id(prefix, digits, suffix=''):
    return {'type': 'string', 'pattern': f'^{prefix}-ORG-S[1-3]-[0-9]{{{digits}}}{suffix}$'}


EXPECTED_FIELDS = {
    'FixtureFile': ['fixture_id', 'contract_version', 'synthetic_organization_id', 'source_type', 'environment',
                    'synthetic_marker', 'tenant', 'run', 'events', 'sources', 'records', 'provenance', 'reviews',
                    'audit'],
    'SyntheticTenantContext': ['synthetic_organization_id', 'tenant_kind', 'origin_dataset_version', 'simulation_actor'],
    'SyntheticPipelineRun': ['pipeline_run_id', 'synthetic_organization_id', 'run_kind', 'pipeline_version',
                             'contract_version', 'hash_algorithm', 'seed', 'clock_start', 'environment', 'source_type'],
    'SyntheticPipelineEvent': ['event_id', 'pipeline_run_id', 'seq', 'state', 'at', 'error_code', 'prev_event_hash',
                               'event_hash'],
    'SyntheticEvidenceSource': ['source_id', 'synthetic_organization_id', 'source_type', 'origin_dataset_version',
                                'origin_file', 'origin_file_sha256', 'origin_record_id'],
    'SyntheticEvidenceRecord': ['synthetic_id', 'synthetic_organization_id', 'pipeline_run_id', 'source_id',
                                'criterion_ref', 'evidence_kind', 'text_synthetic', 'source_type', 'environment',
                                'hash_algorithm', 'content_hash', 'validation_status', 'review_status', 'created_at'],
    'SyntheticEvidenceProvenance': ['provenance_id', 'record_id', 'synthetic_organization_id', 'provenance_kind',
                                    'source_id', 'transformation_id', 'transformation_version', 'hash_before',
                                    'hash_after', 'pipeline_run_id', 'review_id', 'recorded_at',
                                    'prev_provenance_hash', 'provenance_hash'],
    'SyntheticHumanReview': ['review_id', 'record_id', 'pipeline_run_id', 'synthetic_organization_id', 'reviewer_type',
                             'simulation_actor', 'review_scope', 'review_status', 'scripted', 'reviewed_at'],
    'SyntheticAuditEntry': ['audit_id', 'pipeline_run_id', 'synthetic_organization_id', 'action', 'target_ref', 'at',
                            'prev_audit_hash', 'audit_hash'],
}


def _props():
    s = lambda **kw: dict(kw)
    org = s(type='string', pattern=ORG_RX)
    ts = s(type='string', pattern=TS_RX)
    hx = s(type='string', pattern=HASH_RX)
    run_id = _id('SBXR', 4)
    arr = lambda name, lo, hi: s(type='array', items={'$ref': f'#/$defs/{name}'}, minItems=lo, maxItems=hi)
    return {
        'FixtureFile': {
            'fixture_id': s(type='string', pattern='^FXS-ORG-S[1-3]$'),
            'contract_version': s(const=CONTRACT_VERSION), 'synthetic_organization_id': org,
            'source_type': s(const='synthetic'), 'environment': s(const='sandbox'), 'synthetic_marker': s(const=MARKER),
            'tenant': {'$ref': '#/$defs/SyntheticTenantContext'}, 'run': {'$ref': '#/$defs/SyntheticPipelineRun'},
            'events': arr('SyntheticPipelineEvent', len(LIFECYCLE), len(RUN_STATES)),
            'sources': arr('SyntheticEvidenceSource', 1, 10), 'records': arr('SyntheticEvidenceRecord', 1, 10),
            'provenance': arr('SyntheticEvidenceProvenance', 1, 10), 'reviews': arr('SyntheticHumanReview', 1, 10),
            'audit': arr('SyntheticAuditEntry', 1, len(AUDIT_ACTIONS)),
        },
        'SyntheticTenantContext': {
            'synthetic_organization_id': org, 'tenant_kind': s(const='synthetic_organization'),
            'origin_dataset_version': s(const=F34_VERSION),
            'simulation_actor': s(type='string', pattern='^SIMREV-ORG-S[1-3]$'),
        },
        'SyntheticPipelineRun': {
            'pipeline_run_id': run_id, 'synthetic_organization_id': org, 'run_kind': s(const=RUN_KIND),
            'pipeline_version': s(const=PIPELINE_VERSION), 'contract_version': s(const=CONTRACT_VERSION),
            'hash_algorithm': s(const=HASH_ALG), 'seed': s(type='integer', minimum=0, maximum=2 ** 31 - 1),
            'clock_start': ts, 'environment': s(const='sandbox'), 'source_type': s(const='synthetic'),
        },
        'SyntheticPipelineEvent': {
            'event_id': _id('SBXV', 4, '-[0-9]{2}'), 'pipeline_run_id': run_id,
            'seq': s(type='integer', minimum=1, maximum=len(RUN_STATES)), 'state': s(enum=RUN_STATES), 'at': ts,
            'error_code': s(type='string', pattern='^(|E-[A-Z]{2,12})$'), 'prev_event_hash': hx, 'event_hash': hx,
        },
        'SyntheticEvidenceSource': {
            'source_id': _id('SBXS', 6), 'synthetic_organization_id': org, 'source_type': s(const='synthetic'),
            'origin_dataset_version': s(const=F34_VERSION), 'origin_file': s(const=F34_EVIDENCE),
            'origin_file_sha256': hx, 'origin_record_id': s(type='string', pattern='^SYN-[0-9]{6}$'),
        },
        'SyntheticEvidenceRecord': {
            'synthetic_id': _id('SBXE', 6), 'synthetic_organization_id': org, 'pipeline_run_id': run_id,
            'source_id': _id('SBXS', 6), 'criterion_ref': s(type='string', pattern='^CRI-[0-9]{4}$'),
            'evidence_kind': s(enum=EVIDENCE_KINDS),
            # T2: texto plano; sin marcado HTML ni caracteres de control (T-25 de F34A).
            'text_synthetic': s(type='string', pattern='^\\[SINTÉTICO\\] [^<>\\x00-\\x1f\\x7f]{1,380}$',
                                maxLength=400),
            'source_type': s(const='synthetic'), 'environment': s(const='sandbox'), 'hash_algorithm': s(const=HASH_ALG),
            'content_hash': hx, 'validation_status': s(enum=['valido', 'rechazado']),
            'review_status': s(enum=REVIEW_STATUSES), 'created_at': ts,
        },
        'SyntheticEvidenceProvenance': {
            'provenance_id': _id('SBXP', 6), 'record_id': _id('SBXE', 6), 'synthetic_organization_id': org,
            'provenance_kind': s(const='synthetic_fixture'), 'source_id': _id('SBXS', 6),
            'transformation_id': s(const=TRANSFORM[0]), 'transformation_version': s(const=TRANSFORM[1]),
            'hash_before': hx, 'hash_after': hx, 'pipeline_run_id': run_id, 'review_id': _id('SBXH', 6),
            'recorded_at': ts, 'prev_provenance_hash': hx, 'provenance_hash': hx,
        },
        'SyntheticHumanReview': {
            'review_id': _id('SBXH', 6), 'record_id': _id('SBXE', 6), 'pipeline_run_id': run_id,
            'synthetic_organization_id': org, 'reviewer_type': s(const=REVIEWER_TYPE),
            'simulation_actor': s(type='string', pattern='^SIMREV-ORG-S[1-3]$'), 'review_scope': s(const=REVIEW_SCOPE),
            'review_status': s(enum=REVIEW_STATUSES), 'scripted': s(type='boolean', const=True), 'reviewed_at': ts,
        },
        'SyntheticAuditEntry': {
            'audit_id': _id('SBXA', 4, '-[0-9]{2}'), 'pipeline_run_id': run_id, 'synthetic_organization_id': org,
            'action': s(enum=AUDIT_ACTIONS), 'target_ref': run_id, 'at': ts, 'prev_audit_hash': hx, 'audit_hash': hx,
        },
    }


def build_contract():
    """Contrato esperado. El archivo publicado debe coincidir exactamente: ningún campo se añade ni se relaja."""
    props = _props()
    defs = {name: {'type': 'object', 'additionalProperties': False, 'required': list(EXPECTED_FIELDS[name]),
                   'properties': {f: props[name][f] for f in EXPECTED_FIELDS[name]}} for name in EXPECTED_FIELDS}
    return {
        'contract_id': 'f35sbx-contract', 'contract_version': CONTRACT_VERSION,
        'contract_format': 'json-schema-subconjunto-cerrado-f35sbx', 'closed': True, 'synthetic_marker': MARKER,
        'root': 'FixtureFile',
        'hash_definition': {'id': HASH_ALG, 'digest': 'sha256',
                            'serialization': 'json-canonico-claves-ordenadas-sin-espacios-utf8',
                            'canonical_fields': HASH_FIELDS, 'chain_genesis': GENESIS,
                            'transformation': {'id': TRANSFORM[0], 'version': TRANSFORM[1]}},
        '$defs': defs,
    }


SCHEMA_KEYS = {'type', 'properties', 'required', 'additionalProperties', 'items', 'minItems', 'maxItems', 'const',
               'enum', 'pattern', 'maxLength', 'minLength', 'minimum', 'maximum', '$ref'}
PY_TYPES = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool}


def check_schema(v, s, defs, path, out):
    """Validador JSON Schema mínimo y cerrado: una palabra clave desconocida falla (no se ignora)."""
    if not isinstance(s, dict):
        out.append(f'{path}: esquema ilegible')
        return
    unknown = set(s) - SCHEMA_KEYS
    if unknown:
        out.append(f'{path}: palabra clave de esquema desconocida {sorted(unknown)} (falla cerrado)')
        return
    if '$ref' in s:
        name = str(s['$ref']).removeprefix('#/$defs/')
        if name not in defs:
            out.append(f'{path}: referencia inexistente {s["$ref"]}')
            return
        return check_schema(v, defs[name], defs, path, out)
    t = s.get('type')
    if t is not None:
        if t not in PY_TYPES:
            out.append(f'{path}: tipo de esquema desconocido {t}')
            return
        if not isinstance(v, PY_TYPES[t]) or (t == 'integer' and isinstance(v, bool)):
            out.append(f'{path}: tipo {type(v).__name__}, se exige {t}')
            return
    if 'const' in s and (v != s['const'] or type(v) is not type(s['const'])):
        out.append(f'{path}: valor «{str(v)[:40]}» distinto de la constante «{s["const"]}»')
    if 'enum' in s and v not in s['enum']:
        out.append(f'{path}: valor «{str(v)[:40]}» fuera de {s["enum"]}')
    if isinstance(v, str):
        if 'pattern' in s and not re.fullmatch(s['pattern'], v):
            out.append(f'{path}: «{v[:50]}» no cumple el patrón')
        if 'maxLength' in s and len(v) > s['maxLength']:
            out.append(f'{path}: longitud {len(v)} > {s["maxLength"]}')
        if 'minLength' in s and len(v) < s['minLength']:
            out.append(f'{path}: longitud {len(v)} < {s["minLength"]}')
    if isinstance(v, int) and not isinstance(v, bool):
        if 'minimum' in s and v < s['minimum'] or 'maximum' in s and v > s['maximum']:
            out.append(f'{path}: {v} fuera de rango')
    if isinstance(v, list):
        if len(v) < s.get('minItems', 0) or len(v) > s.get('maxItems', len(v)):
            out.append(f'{path}: {len(v)} elementos fuera de [{s.get("minItems")}, {s.get("maxItems")}]')
        for i, x in enumerate(v):
            check_schema(x, s.get('items', {}), defs, f'{path}[{i}]', out)
    if isinstance(v, dict):
        props = s.get('properties', {})
        if s.get('additionalProperties') is not False:
            out.append(f'{path}: objeto sin additionalProperties=false (falla cerrado)')
        extra = sorted(set(v) - set(props))
        missing = sorted(set(s.get('required', [])) - set(v))
        if extra:
            out.append(f'{path}: campos no permitidos {extra}')
        if missing:
            out.append(f'{path}: faltan campos {missing}')
        for k in props:
            if k in v:
                check_schema(v[k], props[k], defs, f'{path}.{k}', out)


# ---------------------------------------------------------------- referencia F34 (solo lectura)
def load_f34():
    """Índices del dataset F34. Cualquier fallo deja la referencia vacía: ORI, ISO y HSH fallan cerrado."""
    try:
        def rows(n):
            with open(os.path.join(F34_DIR, n), encoding='utf-8', newline='') as f:
                return list(csv.DictReader(f))
        apps = {r['application_token']: r['organization_token'] for r in rows('applications.csv')}
        vac = {r['vacancy_token']: r['organization_token'] for r in rows('vacancies.csv')}
        crit_org = {r['criterion_id']: vac[r['vacancy_token']] for r in rows('criteria.csv')}
        evidence = {}
        for r in rows('evidence.csv'):
            evidence[r['synthetic_record_id']] = dict(r, organization=apps[r['application_token']])
        with open(os.path.join(F34_DIR, 'manifest.json'), 'rb') as f:
            mraw = f.read()
        with open(os.path.join(F34_DIR, 'evidence.csv'), 'rb') as f:
            eraw = f.read()
        manifest = json.loads(mraw)
        return {'ok': True, 'evidence': evidence, 'crit_org': crit_org, 'manifest': manifest,
                'manifest_sha': sha_bytes(mraw), 'evidence_sha': sha_bytes(eraw)}
    except (OSError, KeyError, ValueError) as e:
        return {'ok': False, 'error': str(e), 'evidence': {}, 'crit_org': {}, 'manifest': {}, 'manifest_sha': '',
                'evidence_sha': ''}


REF = load_f34()


def expected_selection(org, ref=None):
    """Regla de selección determinista: las PER_TENANT primeras evidencias F34 «vinculada» de la organización, de tipo
    formulario, nota_entrevista o prueba, ordenadas por evidence_id."""
    ref = ref or REF
    rows = sorted((r for r in ref['evidence'].values() if r['organization'] == org and r['state'] == 'vinculada'
                   and r['source_type_ev'] in EVIDENCE_KINDS and r['source_type'] == 'synthetic'),
                  key=lambda r: r['evidence_id'])
    return [r['synthetic_record_id'] for r in rows[:PER_TENANT]]


# ---------------------------------------------------------------- carga del estado (en memoria)
def read_bytes(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except OSError:
        return None


def read_text(path):
    data = read_bytes(path)
    if data is None:
        return None
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None


def listing(base):
    out = []
    for d, dirs, files in os.walk(base):
        dirs[:] = [x for x in dirs if x != '__pycache__']
        out += [os.path.relpath(os.path.join(d, f), base).replace(os.sep, '/') for f in files]
    return sorted(out)


class GitError(Exception):
    pass


def git_rc(*args):
    try:
        p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    except OSError:
        return None, ''
    return p.returncode, p.stdout.strip()


def lines(text):
    return {x.strip() for x in text.splitlines() if x.strip()}


def f35_path_ok(p):
    """DH-02: solo Markdown/JSON en evidencia-sbx/ y Python en tools/f35sbx/; rutas normalizadas."""
    if '\\' in p or any(part in ('', '.', '..') for part in p.split('/')):
        return False
    if p.startswith(REL_SBX):
        return p.endswith(('.md', '.json'))
    if p.startswith(REL_TOOLS):
        return p.endswith('.py')
    return False


F35_EXACT = {'docs/academico/tools/f34b/validate_f34b.py', 'docs/academico/tools/f34e/validate_f34e.py'}
# El gobierno (CLAUDE.md, PROGRESS.md, ACADEMIC_BASELINE.md) no es una ruta libre: su contenido debe ser exactamente
# la apertura o el cierre autorizados sobre la base (f35sbx_scope.lifecycle).
# Validadores históricos adaptados en F35-SBX-A: rutas exactas; su contenido se compara con la base (f35sbx_scope).
F35_HISTORICAL = frozenset({'docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
                            'docs/academico/tools/f34/validate_f34.py'})


def git_state(runner=git_rc, scope=None):
    """Estado Git real. Cualquier código inesperado, Git ausente o base no ancestral: error (falla cerrado)."""
    empty = {'changed': set(), 'deleted': set(), 'contents': {}, 'historical': {}, 'governance': {},
             'v34b': ([], 'unknown')}
    try:
        if runner('rev-parse', '--is-inside-work-tree') != (0, 'true'):
            raise GitError('repositorio inválido o Git no disponible')
        rc, out = runner('rev-parse', '--verify', '--quiet', BASE + '^{commit}')
        if rc != 0 or out != BASE:
            raise GitError('base F35-SBX-A no resuelta')
        if runner('merge-base', '--is-ancestor', BASE, 'HEAD')[0] != 0:
            raise GitError('la base no es ancestro de HEAD')
        rc1, diff = runner('diff', '--name-only', BASE)
        rc2, untracked = runner('ls-files', '--others', '--exclude-standard')
        rc3, deleted = runner('diff', '--name-only', '--diff-filter=D', BASE)
        if (rc1, rc2, rc3) != (0, 0, 0):
            raise GitError(f'consulta Git fallida ({rc1}, {rc2}, {rc3})')
        changed = lines(diff) | lines(untracked)
        contents = {p: read_bytes(os.path.join(ROOT, p)) for p in changed if f35_path_ok(p)}
        historical = {}
        for p in sorted(changed & F35_HISTORICAL):
            rc, base = SCOPE.git(ROOT, 'show', f'{BASE}:{p}')   # sin recortar: el contenido se compara exacto
            historical[p] = {'text': read_text(os.path.join(ROOT, p)), 'base': base if rc == 0 and base else None}
        governance = {}
        for p in sorted(changed & set(GOVERNANCE)):
            rc, base = SCOPE.git(ROOT, 'show', f'{BASE}:{p}')
            governance[p] = {'text': read_text(os.path.join(ROOT, p)), 'base': base if rc == 0 and base else None}
        if scope is None:
            V34B = load_module('f35sbx_f34b_scope', os.path.join(ACAD, 'tools', 'f34b', 'validate_f34b.py'))
            scope = V34B.git_scope()
        return {'error': None, 'changed': changed, 'deleted': lines(deleted), 'contents': contents,
                'historical': historical, 'governance': governance, 'v34b': scope}
    except (GitError, OSError) as e:
        return dict(empty, error=str(e))


def load_state():
    return {
        'docs': {n: read_text(os.path.join(SBX, n)) for n in DOCS},
        'raw': {n: read_bytes(os.path.join(SBX, n)) for n in ARTIFACTS},
        'files': listing(SBX),
        'gov': {p: read_text(os.path.join(ROOT, p)) for p in GOVERNANCE},
        'gate': {'decision': read_text(GATE_DECISION) or '', 'matrix': read_text(GATE_MATRIX) or '',
                 'g0_real': read_text(G0_REAL_DECISION) or ''},
        'sources': {f: read_text(os.path.join(ACAD, 'tools', 'f35sbx', f)) for f in listing(os.path.join(ACAD, 'tools', 'f35sbx'))},
        'git': git_state(),
    }


class DuplicateKey(ValueError):
    pass


def no_duplicates(pairs):
    """object_pairs_hook: cualquier clave repetida en un mismo objeto, en cualquier nivel, invalida el JSON."""
    keys = [k for k, _ in pairs]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        raise DuplicateKey(f'claves duplicadas {dup}')
    return dict(pairs)


def load_json(raw):
    return json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates)


def parse(D):
    """Artefactos JSON interpretados. Un archivo ausente, binario, mal formado o con claves duplicadas queda como
    error (falla cerrado): no llega a ningún análisis."""
    P = {'json': {}, 'err': {}}
    for n in ARTIFACTS:
        raw = D['raw'].get(n)
        if raw is None:
            P['err'][n] = 'ausente'
            continue
        try:
            P['json'][n] = load_json(raw)
        except (UnicodeDecodeError, ValueError) as e:
            P['err'][n] = f'JSON ilegible: {str(e)[:60]}'
    P['fixtures'] = {o: P['json'].get(FIXTURES[o]) for o in ORGS}
    return P


def decoded_problems(obj, path=''):
    """Claves y textos DECODIFICADOS de un JSON (incluidos los escapes \\uXXXX): ningún carácter de formato
    invisible (Unicode Cf) ni texto que NFKC cambie. Se comprueba antes de cualquier normalización."""
    out = []
    items = obj.items() if isinstance(obj, dict) else enumerate(obj) if isinstance(obj, list) else []
    for k, v in items:
        here = f'{path}.{k}' if isinstance(obj, dict) else f'{path}[{k}]'
        for label, x in (('clave', k), ('valor', v)):
            if isinstance(x, str) and (any(unicodedata.category(c) == 'Cf' for c in x)
                                       or unicodedata.normalize('NFKC', x) != x):
                out.append(f'{here}: {label} con caracteres invisibles o de compatibilidad Unicode (escape JSON '
                           f'incluido)')
        if isinstance(v, (dict, list)):
            out += decoded_problems(v, here)
    return out


def walk(obj, path=''):
    """(ruta, clave, valor) de cada clave y de cada valor hoja; los contenedores se informan con valor None."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{path}.{k}' if path else str(k)
            if isinstance(v, (dict, list)):
                yield p, k, None
                yield from walk(v, p)
            else:
                yield p, k, fold(v) if isinstance(v, str) else v
    elif isinstance(obj, list):
        parent = path.rsplit('.', 1)[-1].split('[')[0] if path else ''
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                yield from walk(v, f'{path}[{i}]')
            else:
                yield f'{path}[{i}]', parent, fold(v) if isinstance(v, str) else v


def fixture_items(P):
    for o in ORGS:
        fx = P['fixtures'].get(o)
        if isinstance(fx, dict):
            yield o, fx


def tokens(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return set(re.split(r'[^a-z0-9]+', s)) - {''}


HASH_KEY = re.compile(r'(_hash|_sha256|^content_hash|^hash_before|^hash_after)$')


# ---------------------------------------------------------------- reglas documentales
def doc_props(text):
    """(línea, proposición, polaridad) con el contexto de tabla «Permitido/Prohibido» de F34E. Usa el contexto
    Markdown compartido: el código (fences y código indentado) no genera proposiciones; lo demás sí."""
    rows = [(ln.strip(), kind) for ln, kind in join_rf_lines(scan_markdown(text))]
    ctx = None
    for i, (ln, kind) in enumerate(rows, 1):
        if kind in CODE_KINDS or kind == BLANK:
            continue
        body = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', ln)
        body = unmark(body)
        if kind == TABLE:
            if set(ln.replace('|', '').strip()) <= set('-: '):
                continue
            cells = [c.strip() for c in body.strip().strip('|').split('|')]
            if (i < len(rows) and rows[i][1] == TABLE
                    and set(rows[i][0].replace('|', '').strip()) <= set('-: ')):
                ctx = V34E.table_context(cells[0])
                continue
            for j, c in enumerate(cells):
                for s in re.split(r'(?<=[.!?])\s+', c):
                    for prop, pol in V34E.claim_props(s, ctx if j == 0 else None):
                        yield i, prop, pol
        else:
            ctx = None
            for s in re.split(r'(?<=[.!?])\s+', body):
                for prop, pol in V34E.claim_props(s):
                    yield i, prop, pol


def r_doc(D, P):
    out = []
    for n in DOCS:
        t = D['docs'].get(n)
        if not t or not t.strip():
            out.append(f'documento ausente o vacío: {n}')
            continue
        if unclosed_fence(t):
            out.append(f'{n}: bloque de código (``` o ~~~) sin cerrar (falla cerrado)')
        if not t.lstrip().startswith('# F35-SBX-A'):
            out.append(f'{n}: el encabezado debe empezar por «# F35-SBX-A»')
    readme = D['docs'].get('README.md') or ''
    for n in DOCS[1:] + [CONTRACT, MANIFEST, *FIXTURES.values()]:
        if f']({n})' not in readme:
            out.append(f'README no enlaza {n}')

    def slug(h):
        h = re.sub(r'[`*_]', '', h.strip().lower())
        return re.sub(r'[^\w\- ]', '', h).replace(' ', '-')
    for n, t in D['docs'].items():
        for link in re.findall(r'\]\(([^)\s]+)\)', t or ''):
            if link.startswith(('http://', 'https://')):
                out.append(f'{n}: enlace externo no permitido {link}')
                continue
            path, _, anchor = link.partition('#')
            target = os.path.normpath(os.path.join(SBX, path)) if path else os.path.join(SBX, n)
            local = os.path.dirname(target) == os.path.normpath(SBX) and os.path.basename(target) in D['docs']
            if not (local and D['docs'][os.path.basename(target)]) and not os.path.exists(target):
                out.append(f'{n}: enlace roto {link}')
            elif anchor and target.endswith('.md'):
                src = D['docs'].get(os.path.basename(target)) if local else read_text(target)
                if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', src or '', re.M)}:
                    out.append(f'{n}: ancla rota {link}')
    return out


def r_tsb(D, P):
    t = D['docs'].get('F35SBX_Threat_Model.md') or ''
    rows = [[c.strip() for c in ln.strip().strip('|').split('|')] for ln, kind in scan_markdown(t)
            if kind == TABLE and re.match(r'^\|\s*TSB-\d+\s*\|', ln.strip())]
    out = []
    ids = [r[0] for r in rows]
    if sorted(ids) != TSB_IDS or len(ids) != len(set(ids)):
        out.append(f'threat model: se exigen exactamente {TSB_IDS[0]}..{TSB_IDS[-1]} sin duplicados (hay {ids})')
    known = {c[0] for c in CASES} | {c[0] for c in JOIN_CASES}
    for r in rows:
        if len(r) != 7 or any(not c for c in r):
            out.append(f'{r[0]}: fila incompleta (amenaza, riesgo, control, evidencia, negativo, fail-closed)')
            continue
        refs = re.findall(r'NS-\d{2,3}', r[5])
        if not refs or not set(refs) <= known:
            out.append(f'{r[0]}: casos negativos inexistentes o ausentes {sorted(set(refs) - known) or "—"}')
    return out


def r_trz(D, P):
    out = []
    plan = '\n'.join(ln for ln, kind in scan_markdown(D['docs'].get('F35SBX_Plan_Pruebas.md') or '') if kind == TABLE)
    listed = set(re.findall(r'^\|\s*(NS-\d{2,3})\s*\|', plan, re.M))
    known = {c[0] for c in CASES} | {c[0] for c in JOIN_CASES}
    if listed != known:
        out.append(f'plan de pruebas y validador no coinciden: faltan {sorted(known - listed)[:5]}, '
                   f'sobran {sorted(listed - known)[:5]}')
    crit = '\n'.join(ln for ln, kind in scan_markdown(D['docs'].get('F35SBX_Criterios_Cierre_y_Revocacion.md') or '')
                     if kind == TABLE)
    for i in ACS_IDS + REV_IDS:
        if len(re.findall(rf'^\|\s*{i}\s*\|', crit, re.M)) != 1:
            out.append(f'criterios: {i} ausente o duplicado')
    return out


def gate_states(D):
    return V34E.decision_states(D['gate']['decision'])


def expected_states(D):
    g, f = gate_states(D)
    return {'G0 real': 'NO APROBADA', 'G0-SBX': g, 'F35 productiva': 'BLOQUEADA', 'F35-SBX': f,
            'F36–F40': 'BLOQUEADAS', 'Alcance C': 'BLOQUEADO'}


def r_sta(D, P):
    out = []
    exp = expected_states(D)
    readme = D['docs'].get('README.md') or ''
    decls, _ = V34E.parse_declarations(fold(readme))
    for k in CRITICAL:
        vals = [v for kk, v in decls if kk == k]
        if exp[k] is None or vals != [exp[k]]:
            out.append(f'README: «{k}» debe declararse una vez como {exp[k]} (declarado {vals})')
    for n, t in D['docs'].items():
        d, problems = V34E.parse_declarations(fold(t))
        out += [f'{n}: {p}' for p in problems]
        for k, v in d:
            if v != exp.get(k):
                out.append(f'{n}: «{k} = {v}» incoherente con el estado vigente ({exp.get(k)})')
    plain = unmark(readme)
    for need in ('ADR-005 = PROPUESTA', 'Datos reales = PROHIBIDOS'):
        if need not in plain:
            out.append(f'README: falta «{need}»')
    words = set(PHASE_STATE_RX.findall(plain))
    if len(words) != 1 or not words <= set(LIFECYCLE_PHRASES):
        out.append(f'README: estado de F35-SBX-A ausente, contradictorio o desconocido {sorted(words)}')
    elif words == {'CERRADA'} and gov_lifecycle(D)[0] != 'CERRADA':
        out.append('README: F35-SBX-A figura cerrada sin cierre registrado en el gobierno')
    if SBXB_STATE_RX.search(plain):
        out.append('README: F35-SBX-B no puede figurar iniciada')
    return out


# Guiones Unicode que pueden separar «RF» del número: hyphen, non-breaking hyphen, figure dash, en/em dash,
# horizontal bar, minus, small/fullwidth hyphen-minus.
DASHES = '\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe58\ufe63\uff0d'
RF_RX = re.compile(r'\bRF\s*[-_' + DASHES + r']?\s*(\d{1,3})\b', re.I)
# RF seguido de un separador razonable y su predicado («RF-23: automática», «RF 23 — automática», «RF23 = …»,
# «RF-23 -> …»): el separador se retira para que identificador y predicado queden en la misma proposición.
RF_SEP_RX = re.compile(r'\b(RF-\d{2,3})[ \t]*(?:->|→|[:=' + DASHES + r'-])[ \t]*')
# Predicado de RF-21/RF-23 envuelto en paréntesis: se retiran hasta MAX_RF_WRAPPERS capas que lo envuelvan por
# completo («RF-23: (((automática)))» → «RF-23 automática»). Una estructura que no se puede verificar (paréntesis
# desbalanceados, más capas que la cota, envoltorio vacío o ambiguo) se sustituye por RF_INVALID: falla cerrado.
MAX_RF_WRAPPERS = 8
RF_INVALID = 'PREDICADO_RF_NO_VERIFICABLE'
RF_PRED_RX = re.compile(r'\bRF-2[13]\b')


def _closing(text, i):
    """Índice del paréntesis que cierra el abierto en i, o -1."""
    level = 0
    for x in range(i, len(text)):
        level += (text[x] == '(') - (text[x] == ')')
        if level == 0:
            return x
    return -1


def unwrap_rf_predicates(t):
    """Solo el predicado inmediato de RF-21/RF-23 (hasta «.», «;» o fin de línea); otros paréntesis no se tocan."""
    out, pos = [], 0
    for m in RF_PRED_RX.finditer(t):
        if m.start() < pos:
            continue
        out.append(t[pos:m.end()])
        j = m.end()
        while j < len(t) and t[j] in ' \t':
            j += 1
        end = min([k for k in (t.find(c, j) for c in '.;\n') if k != -1] + [len(t)])
        region, level, balanced = t[j:end], 0, True
        for ch in region:
            level += (ch == '(') - (ch == ')')
            balanced = balanced and level >= 0
        if not balanced or level != 0:                    # solo apertura, solo cierre o desbalanceado
            out.append(f' {RF_INVALID} {region}')
        elif region.startswith('('):
            close = _closing(region, 0)
            seg, layers = region[:close + 1].strip(), 0
            while seg.startswith('(') and _closing(seg, 0) == len(seg) - 1 and layers <= MAX_RF_WRAPPERS:
                seg, layers = seg[1:-1].strip(), layers + 1
            if layers > MAX_RF_WRAPPERS or not seg or '(' in seg or ')' in seg:
                out.append(f' {RF_INVALID} {region}')      # cota superada, vacío o ambiguo
            else:
                out.append(f' {seg}{region[close + 1:]}')
        else:
            out.append(t[m.end():j])                    # sin envoltorio: el siguiente RF también cuenta
            pos = j
            continue
        pos = end
    out.append(t[pos:])
    return ''.join(out)
SCOPE_C_RX = re.compile(r'\bscope\s+c\b', re.I)


def fold(text):
    """Normalización previa común y determinista (segunda reauditoría):
    1. Unicode NFKC (ｓｃｏｒｉｎｇ → scoring); 2. sin caracteres de formato invisibles (categoría Cf: U+200B,
    U+200C, U+200D, U+2060, U+FEFF, U+00AD…); 3. guiones Unicode entre caracteres visibles → «-» (los guiones
    con espacios siguen separando proposiciones); 4. RF23, RF 23, rf-23, RF–23 o RF—23 → RF-23;
    5. «Scope C» → «alcance C». No es un analizador general: solo cierra las clases de bypass verificadas."""
    t = unicodedata.normalize('NFKC', text or '')
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Cf')
    t = re.sub(r'(?<=\S)[' + DASHES + r'](?=\S)', '-', t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = RF_RX.sub(lambda m: f'RF-{int(m.group(1)):02d}', t)
    t = RF_SEP_RX.sub(r'\1 ', t)
    t = unwrap_rf_predicates(t)
    return SCOPE_C_RX.sub('alcance C', t)


RF_TAIL_RX = re.compile(r'\bRF-2[13][ \t]*$')

# ---------------------------------------------------------------- contexto Markdown compartido (fuente única)
# scan_markdown() clasifica cada línea una sola vez; join_rf_breaks(), doc_props(), el CLM, las tablas TSB/TRZ, DOC
# (fence sin cerrar) y los metadatos usan esa misma clasificación. Ningún otro código detecta fences ni bloques.
PLAIN, BLANK, FENCE, FENCED_CODE, INDENTED_CODE = 'PLAIN', 'BLANK', 'FENCE', 'FENCED_CODE', 'INDENTED_CODE'
HEADING, BLOCKQUOTE, LIST, TABLE, OTHER_STRUCTURAL = 'HEADING', 'BLOCKQUOTE', 'LIST', 'TABLE', 'OTHER_STRUCTURAL'
HTML_BLOCK = 'HTML_BLOCK'
CODE_KINDS = frozenset({FENCE, FENCED_CODE, INDENTED_CODE})          # nunca son proposiciones del documento
MD_START = {'fence': None, 'html': None, 'ctx': None, 'prev': None}
FENCE_OPEN_RX = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
HEADING_RX = re.compile(r'^ {0,3}#{1,6}(?:[ \t]|$)')
HR_RX = re.compile(r'^ {0,3}(?:([-*_])(?:[ \t]*\1){2,}|=+)[ \t]*$')
SETEXT_RX = re.compile(r'^ {0,3}(?:=+|-+)[ \t]*$')
QUOTE_RX = re.compile(r'^ {0,3}>')
LIST_RX = re.compile(r'^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:[ \t]|$)')
TABLE_RX = re.compile(r'^\s*\||^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$')
HTML_OPEN_RX = re.compile(r'^ {0,3}<(?:(!--)|(/?)([A-Za-z][A-Za-z0-9-]*)(?=[\s/>]|$))?')
HTML_BLOCK_TAGS = frozenset({
    'address', 'article', 'aside', 'blockquote', 'center', 'details', 'dialog', 'dd', 'div', 'dl', 'dt', 'fieldset',
    'figcaption', 'figure', 'footer', 'form', 'header', 'iframe', 'li', 'main', 'nav', 'ol', 'p', 'pre', 'script',
    'section', 'style', 'summary', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'tr', 'ul'})


def classify_markdown_line(line, state):
    """(tipo, estado siguiente) de una línea según el estado acumulado:
    - fence: (carácter, longitud). Solo lo cierra una línea del mismo carácter y longitud igual o mayor, sin texto
      detrás: «```» no cierra «````» y «~~~» no cierra «```». Sin cierre, todo hasta el final es código.
    - html: marcador de cierre de un bloque HTML (</div>, </pre>, -->…). Sin cierre, el resto sigue siendo HTML.
    - ctx: lista, cita o tabla, para sus líneas de continuación.
    - prev: tipo de la línea anterior. El código indentado no puede interrumpir un párrafo (CommonMark): una línea
      indentada tras prosa es continuación de esa prosa."""
    fence, html, ctx, prev = state['fence'], state['html'], state['ctx'], state['prev']
    if fence:
        ch, n = fence
        if re.fullmatch(r' {0,3}' + re.escape(ch) + '{' + str(n) + r',}[ \t]*', line):
            return FENCE, dict(MD_START)
        return FENCED_CODE, state
    if html:
        return HTML_BLOCK, dict(state, html=None) if html in line.lower() else state
    m = FENCE_OPEN_RX.match(line)
    if m and not (m.group(1)[0] == '`' and '`' in m.group(2)):
        return FENCE, dict(MD_START, fence=(m.group(1)[0], len(m.group(1))))
    if not line.strip():
        return BLANK, dict(MD_START)
    if line.startswith(('\t', '    ')):
        if ctx == 'list':
            return LIST, state
        return (PLAIN, state) if prev == PLAIN else (INDENTED_CODE, dict(MD_START))
    m = HTML_OPEN_RX.match(line)
    if m and (m.group(1) or (m.group(3) or '').lower() in HTML_BLOCK_TAGS):
        end = '-->' if m.group(1) else f'</{m.group(3).lower()}>'
        rest = line.lower()[m.end():]
        opened = not m.group(2) and end not in rest
        return HTML_BLOCK, dict(MD_START, html=end if opened else None)
    if HEADING_RX.match(line):
        return HEADING, dict(MD_START)
    if HR_RX.match(line):
        return OTHER_STRUCTURAL, dict(MD_START)
    if QUOTE_RX.match(line):
        return BLOCKQUOTE, dict(MD_START, ctx='quote')
    if LIST_RX.match(line):
        return LIST, dict(MD_START, ctx='list')
    if TABLE_RX.match(line) or (ctx == 'table' and '|' in line):
        return TABLE, dict(MD_START, ctx='table')
    if m:                                                     # otra etiqueta HTML en su propia línea
        return OTHER_STRUCTURAL, dict(MD_START)
    if ctx in ('list', 'quote'):                              # continuación perezosa de la lista o la cita
        return (LIST if ctx == 'list' else BLOCKQUOTE), state
    return PLAIN, dict(MD_START)


def _scan(text):
    rows, state = [], dict(MD_START)
    for ln in (text or '').split('\n'):
        kind, state = classify_markdown_line(ln, state)
        state = dict(state, prev=kind)
        rows.append([ln, kind])
    # Títulos setext: un párrafo seguido de «===» o «---» es un título. Se reconoce aquí, antes de cualquier unión.
    for i, (ln, kind) in enumerate(rows):
        if i and SETEXT_RX.match(ln) and rows[i - 1][1] == PLAIN:
            rows[i][1] = HEADING
            j = i - 1
            while j >= 0 and rows[j][1] == PLAIN:
                rows[j][1] = HEADING
                j -= 1
    return [tuple(r) for r in rows], state


def scan_markdown(text):
    """[(línea, tipo)] del documento completo: la fuente única de contexto Markdown de F35-SBX."""
    return _scan(text)[0]


def unclosed_fence(text):
    """True si un fence (``` o ~~~) se abre y no se cierra: su resto es código, y DOC falla cerrado."""
    return _scan(text)[1]['fence'] is not None


def join_rf_lines(rows):
    """Une una línea PLAIN que termina en RF-21/RF-23 (tras normalizar y quitar su separador) con la línea PLAIN
    contigua: en Markdown forman la misma frase. Ningún otro tipo se une, ni a través de una línea en blanco."""
    out = []
    for ln, kind in rows:
        if (kind == PLAIN and out and out[-1][1] == PLAIN
                and RF_TAIL_RX.search(fold(V34E.strip_md(fold(out[-1][0]))))):
            out[-1] = (out[-1][0].rstrip() + ' ' + ln.strip(), PLAIN)
        else:
            out.append((ln, kind))
    return out


def join_rf_breaks(text):
    return '\n'.join(ln for ln, _ in join_rf_lines(scan_markdown(text)))


def prose_text(text):
    """Texto del documento tal como lo analiza la semántica: uniones de RF aplicadas y líneas de código en blanco
    (se conservan los números de línea de lo demás)."""
    return '\n'.join('' if kind in CODE_KINDS else ln for ln, kind in join_rf_lines(scan_markdown(text)))


def unmark(text):
    """M01: quita solo los delimitadores Markdown (`x`, **x**, *x*, _x_, ~~x~~ y combinaciones), nunca el
    contenido: «`scoring`» se analiza como «scoring». Los guiones bajos internos se conservan.
    Orden: fold → quitar delimitadores → fold de nuevo, para que «`RF` 23», «**RF**23» o «**Scope** C» se
    normalicen igual que su forma sin Markdown."""
    return fold(V34E.strip_md(fold(text)))


def r_clm(D, P):
    # Se analiza el texto sin delimitadores: el CLM de F34E descarta los spans de código y eso era un bypass.
    # Las líneas de código (contexto Markdown compartido) no son proposiciones del documento.
    return V34E.clm({n: unmark(prose_text(t)) for n, t in D['docs'].items() if t}, {})


PHASE_SUBJ = re.compile(r'\bF35\b(?!-SBX)|\bF3[6-9]\b|\bF40\b|\balcance\s+C\b|\bG0\s+real\b|\bG0\b(?![-\w])', re.I)
PHASE_VERB = re.compile(r'\b(inici\w*|arranc\w*|comienz\w*|comenz\w*|abiert\w*|abre|habilit\w*|desbloque\w*|activ\w*|'
                        r'aprob\w*|ejecut\w*|en\s+curso)\b', re.I)
RF_SUBJ = re.compile(r'\bRF-2[13]\b', re.I)
RF_VERB = re.compile(r'\b(modific\w*|cambi\w*|reemplaz\w*|sustitu\w*|automatiz\w*|autom[aá]tic\w*|elimin\w*|'
                     r'reinterpret\w*|renumer\w*|redefin\w*)\b', re.I)


def r_phs(D, P):
    out = []
    for n, t in D['docs'].items():
        for i, prop, pol in doc_props(t):
            if RF_INVALID in prop:
                out.append(f'{n}:{i}: predicado de RF-21/RF-23 con paréntesis no verificables (falla cerrado)')
            if pol == 'neg':
                continue
            if PHASE_SUBJ.search(prop) and PHASE_VERB.search(prop):
                out.append(f'{n}:{i}: fase o puerta bloqueada afirmada como iniciada/habilitada: {prop[:80]}')
            if RF_SUBJ.search(prop) and RF_VERB.search(prop):
                out.append(f'{n}:{i}: modificación de RF-21/RF-23: {prop[:80]}')
    return out


# ---------------------------------------------------------------- contrato y fixtures
def r_con(D, P):
    c = P['json'].get(CONTRACT)
    if not isinstance(c, dict):
        return [f'contrato ilegible: {P["err"].get(CONTRACT, "no es un objeto")} (falla cerrado)']
    exp = build_contract()
    out = []
    if set(c) != set(exp):
        out.append(f'claves de primer nivel distintas: {sorted(set(c) ^ set(exp))}')
    for k in ('contract_id', 'contract_version', 'contract_format', 'closed', 'synthetic_marker', 'root',
              'hash_definition'):
        if c.get(k) != exp[k]:
            out.append(f'«{k}» distinto del contrato esperado')
    defs = c.get('$defs') if isinstance(c.get('$defs'), dict) else {}
    if set(defs) != set(EXPECTED_FIELDS):
        out.append(f'entidades distintas: {sorted(set(defs) ^ set(EXPECTED_FIELDS))}')
    for name, fields in EXPECTED_FIELDS.items():
        s = defs.get(name) if isinstance(defs.get(name), dict) else {}
        if s.get('type') != 'object' or s.get('additionalProperties') is not False:
            out.append(f'{name}: no es un objeto cerrado (additionalProperties=false)')
        props = s.get('properties') if isinstance(s.get('properties'), dict) else {}
        if set(props) != set(fields):
            out.append(f'{name}: campos distintos de los permitidos {sorted(set(props) ^ set(fields))}')
        if sorted(s.get('required') or []) != sorted(fields):
            out.append(f'{name}: «required» debe contener exactamente los campos permitidos')
        for f, sub in props.items():
            if tokens(f) & CAP_TOKENS or PII_FIELD.search(f) or PERSON_FIELD.search(f):
                out.append(f'{name}.{f}: nombre de campo prohibido')
            if not isinstance(sub, dict):
                continue
            if sub.get('type') == 'string' and not ({'const', 'enum', 'pattern'} & set(sub)):
                out.append(f'{name}.{f}: cadena libre sin const, enum ni pattern')
            if f in exp['$defs'].get(name, {}).get('properties', {}) and sub != exp['$defs'][name]['properties'][f]:
                out.append(f'{name}.{f}: restricción distinta de la esperada (relajada o alterada)')
    bad = []

    def keywords(x, path):
        if isinstance(x, dict):
            if path.count('.') >= 2 and not path.endswith('.properties'):
                for k in set(x) - SCHEMA_KEYS:
                    bad.append(f'{path}.{k}')
            for k, v in x.items():
                keywords(v, f'{path}.{k}')
        elif isinstance(x, list):
            for v in x:
                keywords(v, path)
    for name, s in defs.items():
        keywords(s, f'$defs.{name}')
    if bad:
        out.append(f'palabras clave de esquema desconocidas: {sorted(bad)[:4]}')
    return out


def r_sch(D, P):
    exp = build_contract()
    out = []
    for o in ORGS:
        fx = P['fixtures'].get(o)
        if fx is None:
            out.append(f'{FIXTURES[o]}: {P["err"].get(FIXTURES[o], "ausente")} (falla cerrado)')
            continue
        errs = []
        check_schema(fx, exp['$defs']['FixtureFile'], exp['$defs'], o, errs)
        out += errs
    return out


def r_syn(D, P):
    out = []
    for o, fx in fixture_items(P):
        if fx.get('synthetic_marker') != MARKER or fx.get('source_type') != 'synthetic' or fx.get('environment') != 'sandbox':
            out.append(f'{o}: cabecera del fixture sin marcadores sintéticos')
        run = fx.get('run') if isinstance(fx.get('run'), dict) else {}
        for k, v in (('source_type', 'synthetic'), ('environment', 'sandbox'), ('hash_algorithm', HASH_ALG)):
            if run.get(k) != v:
                out.append(f'{o}: run con {k} ≠ {v}')
        for s in fx.get('sources') or []:
            if isinstance(s, dict) and s.get('source_type') != 'synthetic':
                out.append(f'{o}: fuente {s.get("source_id")} con source_type ≠ synthetic')
        for r in fx.get('records') or []:
            if not isinstance(r, dict):
                out.append(f'{o}: registro ilegible')
                continue
            rid = str(r.get('synthetic_id'))
            checks = [
                (rid.startswith(f'SBXE-{o}-'), '1 identificador SBXE- del tenant'),
                (str(r.get('text_synthetic', '')).startswith(MARKER + ' '), '2 texto con [SINTÉTICO]'),
                (r.get('source_type') == 'synthetic', '3 source_type = synthetic'),
                (r.get('environment') == 'sandbox', '4 environment = sandbox'),
                (r.get('hash_algorithm') == HASH_ALG, f'5 hash_algorithm = {HASH_ALG}'),
                (r.get('synthetic_organization_id') == o and re.fullmatch(ORG_RX, str(r.get('synthetic_organization_id'))),
                 '6 tenant sintético ORG-S*'),
            ]
            for ok, what in checks:
                if not ok:
                    out.append(f'{o}:{rid}: marcador synthetic-only ausente: {what}')
    return out


PII_FIELD = re.compile(r'(^|_)(real|nombres?|names?|apellidos?|surname|emails?|correos?|mail|tel[eé]fonos?|phones?|'
                       r'celular|dni|ruc|pasaporte|passport|documento_identidad|direcci[oó]n|address|domicilio|'
                       r'nacimiento|birth\w*|edad|age|sexo|sex|g[eé]nero|gender|etnia|salud|health|religion|foto|photo)'
                       r'(_|$)', re.I)
PII_VALUE = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), 'correo'), (re.compile(r'https?://|www\.', re.I), 'URL'),
             (re.compile(r'(?<![\w-])\d{11}(?![\w-])'), 'RUC'), (re.compile(r'(?<![\w-])\d{8}(?![\w-])'), 'DNI'),
             (re.compile(r'(?<![\w-])\+?\d[\d ]{8,}\d(?![\w-])'), 'teléfono')]


def r_pii(D, P):
    out = []
    for o, fx in fixture_items(P):
        for path, k, v in walk(fx):
            if PII_FIELD.search(str(k)):
                out.append(f'{o}:{path}: campo de dato personal')
            if isinstance(v, str) and not HASH_KEY.search(str(k)):
                for rx, what in PII_VALUE:
                    if rx.search(v):
                        out.append(f'{o}:{path}: posible {what} en el valor')
    return out


MEDIA_FIELD = re.compile(r'(^|_)(cv|cvs|curriculum|pdf|docx?|imagen(es)?|images?|img|fotos?|photos?|audios?|videos?|'
                         r'v[ií]deos?|media|adjuntos?|attachments?|archivos?|files?|blob|binary|binario|base64)(_|$)',
                         re.I)
MEDIA_FIELD_OK = {'origin_file', 'origin_file_sha256'}
MEDIA_EXT = re.compile(r'\.(pdf|docx?|odt|rtf|png|jpe?g|gif|bmp|tiff?|webp|heic|svg|mp3|wav|m4a|ogg|flac|aac|mp4|mov|'
                       r'avi|mkv|webm|wmv|zip|rar|7z|exe|bin|sqlite3?|db)\b', re.I)
DATA_URI = re.compile(r'data:[\w.+/-]*;base64', re.I)
BASE64 = re.compile(r'[A-Za-z0-9+/]{40,}={0,2}')
CONTROL = re.compile(r'[\x00-\x08\x0b-\x1f\x7f]')
CV_VALUE = re.compile(r'\b(CVs?|curr[ií]cul\w*)\b', re.I)


def r_med(D, P):
    out = []
    for n in ARTIFACTS:
        raw = D['raw'].get(n)
        if raw is not None and (b'\x00' in raw or b'\r' in raw or raw.startswith(b'\xef\xbb\xbf')):
            out.append(f'{n}: contenido binario, CR o BOM (solo texto UTF-8 con LF)')
        text = raw.decode('utf-8', 'replace') if raw is not None else ''
        if any(unicodedata.category(ch) == 'Cf' for ch in text) or unicodedata.normalize('NFKC', text) != text:
            out.append(f'{n}: caracteres invisibles de formato o de compatibilidad Unicode (NFKC)')
        if n != MANIFEST and n in P['json']:               # el manifest lo revisa MAN tras su esquema
            out += [f'{n}{x}' for x in decoded_problems(P['json'][n])]
    expected = set(DOCS) | set(ARTIFACTS)
    for f in D['files']:
        if f not in expected:
            out.append(f'archivo no autorizado en evidencia-sbx/: {f}')
        if MEDIA_EXT.search(f):
            out.append(f'media o binario en evidencia-sbx/: {f}')
    for o, fx in fixture_items(P):
        for path, k, v in walk(fx):
            if MEDIA_FIELD.search(str(k)) and k not in MEDIA_FIELD_OK:
                out.append(f'{o}:{path}: campo de media, documento o adjunto')
            if isinstance(v, str) and not HASH_KEY.search(str(k)):
                for rx, what in ((MEDIA_EXT, 'archivo de media o documento'), (DATA_URI, 'data URI'),
                                 (BASE64, 'bloque base64'), (CONTROL, 'carácter de control'), (CV_VALUE, 'CV')):
                    if rx.search(v) and not (rx is MEDIA_EXT and v == F34_EVIDENCE):
                        out.append(f'{o}:{path}: {what}')
    return out


CAP_TOKENS = {'score', 'scores', 'scoring', 'puntaje', 'puntajes', 'puntuacion', 'rank', 'ranking', 'rankings', 'ranked',
              'recommend', 'recommendation', 'recommendations', 'recommended', 'recomendacion', 'recomendado',
              'recomienda', 'best', 'mejor', 'selected', 'selection', 'seleccion', 'seleccionado', 'automatic',
              'hire', 'hired', 'contratado', 'contratar', 'ocr', 'parsing', 'parse', 'parser', 'extraction', 'extract',
              'extraccion', 'embedding', 'embeddings', 'vector', 'vectors', 'vectorial', 'semantic', 'semantica',
              'semantico', 'llm', 'gpt', 'similarity', 'similitud', 'apto', 'apta', 'aptitud', 'idoneidad', 'idoneo',
              'merito', 'desempeno', 'performance', 'personalidad', 'personality', 'emocion', 'emotion', 'honestidad',
              'honesty', 'inteligencia', 'intelligence', 'estres', 'stress', 'biometria', 'biometric', 'suitability',
              'fit', 'percentile', 'percentil', 'level', 'nivel'}


def r_cap(D, P):
    out = []
    for o, fx in fixture_items(P):
        for path, k, v in walk(fx):
            hit = tokens(k) & CAP_TOKENS
            if isinstance(v, str) and not HASH_KEY.search(str(k)):
                hit |= tokens(v) & CAP_TOKENS
            if hit:
                out.append(f'{o}:{path}: capacidad prohibida {sorted(hit)}')
    m = P['json'].get(MANIFEST)
    if isinstance(m, dict):
        for path, k, v in walk(m):
            if tokens(k) & CAP_TOKENS:
                out.append(f'manifest:{path}: capacidad prohibida')
    return out


PERSON_VALUE = re.compile(r'(?<![\w-])(?:APP|PER|PER-S|EV|EVA|CAND|POST|USR|USER)-[\w-]*\d', re.I)
PERSON_FIELD = re.compile(r'(^|_)(person|persona|personas|people|candidate|candidato|candidatos|applicant|application|'
                          r'postulante|postulacion|evaluator|evaluador|evaluado|user|usuario|employee|empleado|'
                          r'human_level|rubric_points)(_|$)', re.I)


def r_per(D, P):
    out = []
    for o, fx in fixture_items(P):
        for path, k, v in walk(fx):
            if PERSON_FIELD.search(str(k)):
                out.append(f'{o}:{path}: campo de persona (DH-06)')
            if isinstance(v, str) and PERSON_VALUE.search(v):
                out.append(f'{o}:{path}: token de persona en el valor (DH-06)')
    return out


ID_KEYS = ('fixture_id', 'pipeline_run_id', 'event_id', 'source_id', 'synthetic_id', 'provenance_id', 'record_id',
           'review_id', 'audit_id', 'target_ref', 'simulation_actor')


def r_iso(D, P):
    out = []
    seen = {}
    for o in ORGS:
        fx = P['fixtures'].get(o)
        if not isinstance(fx, dict):
            out.append(f'{o}: fixture ilegible; aislamiento no verificable (falla cerrado)')
            continue
        for path, k, v in walk(fx):
            if k == 'synthetic_organization_id' and v != o:
                out.append(f'{o}:{path}: organización cruzada {v}')
            if k in ID_KEYS and isinstance(v, str) and not v.endswith(o) and f'-{o}-' not in v:
                out.append(f'{o}:{path}: identificador de otro tenant {v}')
            if k in ('synthetic_id', 'origin_record_id', 'source_id') and isinstance(v, str):
                if seen.setdefault((k, v), o) != o:
                    out.append(f'{o}:{path}: {v} compartido con {seen[(k, v)]}')
        for s in fx.get('sources') or []:
            row = REF['evidence'].get(s.get('origin_record_id')) if isinstance(s, dict) else None
            if row and row['organization'] != o:
                out.append(f'{o}: origen F34 {s.get("origin_record_id")} pertenece a {row["organization"]}')
        for r in fx.get('records') or []:
            if isinstance(r, dict) and REF['crit_org'].get(r.get('criterion_ref'), o) != o:
                out.append(f'{o}: criterio {r.get("criterion_ref")} de otra organización')
    return out


def by(items, key):
    return {x.get(key): x for x in items or [] if isinstance(x, dict)}


def check_chain(items, key, prev_key, label, out):
    prev = GENESIS
    for x in items or []:
        if not isinstance(x, dict):
            continue
        if x.get(prev_key) != prev:
            out.append(f'{label}: cadena rota en {x.get(key.replace("_hash", "_id"), "?")}')
        if x.get(key) != chain_hash(x, key):
            out.append(f'{label}: hash recalculado distinto en {x.get(key.replace("_hash", "_id"), "?")}')
        prev = x.get(key)


def r_hsh(D, P):
    out = []
    if not REF['ok']:
        return [f'referencia F34 ilegible: {REF.get("error")} (falla cerrado)']
    for o, fx in fixture_items(P):
        src = by(fx.get('sources'), 'source_id')
        prov = by(fx.get('provenance'), 'record_id')
        for r in fx.get('records') or []:
            if not isinstance(r, dict):
                continue
            s = src.get(r.get('source_id')) or {}
            origin = s.get('origin_record_id')
            h = content_hash(o, origin, r.get('criterion_ref'), r.get('evidence_kind'), r.get('text_synthetic'))
            if r.get('content_hash') != h:
                out.append(f'{o}:{r.get("synthetic_id")}: content_hash alterado')
            p = prov.get(r.get('synthetic_id')) or {}
            if p and p.get('hash_after') != r.get('content_hash'):
                out.append(f'{o}:{r.get("synthetic_id")}: hash_after ≠ content_hash')
            row = REF['evidence'].get(origin)
            if p and row:
                before = content_hash(o, origin, row['criterion_id'], row['source_type_ev'], row['evidence_text'])
                if p.get('hash_before') != before:
                    out.append(f'{o}:{r.get("synthetic_id")}: hash_before distinto del contenido F34 de origen')
        for s in fx.get('sources') or []:
            if isinstance(s, dict) and s.get('origin_file_sha256') != REF['evidence_sha']:
                out.append(f'{o}:{s.get("source_id")}: SHA-256 de evidence.csv distinto del archivo F34')
        events = sorted((e for e in fx.get('events') or [] if isinstance(e, dict)), key=lambda e: e.get('seq', 0))
        check_chain(events, 'event_hash', 'prev_event_hash', f'{o}: eventos', out)
        check_chain(fx.get('provenance'), 'provenance_hash', 'prev_provenance_hash', f'{o}: provenance', out)
        check_chain(fx.get('audit'), 'audit_hash', 'prev_audit_hash', f'{o}: auditoría', out)
    if REF['manifest'].get('files', {}).get('evidence.csv', {}).get('sha256') != REF['evidence_sha']:
        out.append('evidence.csv de F34 no coincide con su manifiesto (dataset alterado)')
    return out


def r_prv(D, P):
    out = []
    for o, fx in fixture_items(P):
        run = fx.get('run') if isinstance(fx.get('run'), dict) else {}
        recs = by(fx.get('records'), 'synthetic_id')
        src = by(fx.get('sources'), 'source_id')
        revs = by(fx.get('reviews'), 'review_id')
        provs = [p for p in fx.get('provenance') or [] if isinstance(p, dict)]
        counts = {}
        for p in provs:
            counts[p.get('record_id')] = counts.get(p.get('record_id'), 0) + 1
        for rid, r in recs.items():
            if counts.get(rid) != 1:
                out.append(f'{o}:{rid}: se exige exactamente una provenance (hay {counts.get(rid, 0)})')
        for p in provs:
            rid = p.get('record_id')
            r = recs.get(rid)
            if r is None:
                out.append(f'{o}:{p.get("provenance_id")}: provenance de un registro inexistente')
                continue
            if p.get('source_id') != r.get('source_id') or p.get('source_id') not in src:
                out.append(f'{o}:{rid}: provenance sin fuente coherente')
            if (p.get('transformation_id'), p.get('transformation_version')) != TRANSFORM:
                out.append(f'{o}:{rid}: transformación no registrada')
            if p.get('provenance_kind') != 'synthetic_fixture':
                out.append(f'{o}:{rid}: provenance_kind ≠ synthetic_fixture')
            if p.get('pipeline_run_id') != run.get('pipeline_run_id'):
                out.append(f'{o}:{rid}: provenance de otro run')
            rv = revs.get(p.get('review_id'))
            if rv is None or rv.get('record_id') != rid:
                out.append(f'{o}:{rid}: provenance sin revisión simulada coherente')
            if str(p.get('recorded_at', '')) < str(r.get('created_at', '~')):
                out.append(f'{o}:{rid}: provenance registrada antes que el registro')
        used = {r.get('source_id') for r in recs.values()}
        for sid in set(src) - used:
            out.append(f'{o}: fuente huérfana {sid}')
    return out


def r_ori(D, P):
    if not REF['ok']:
        return [f'referencia F34 ilegible: {REF.get("error")} (falla cerrado)']
    out = []
    if REF['manifest'].get('dataset_version') != F34_VERSION or REF['manifest'].get('source') != 'synthetic':
        out.append('dataset F34 de origen no es f34-synth-1.1.0 sintético')
    for o, fx in fixture_items(P):
        src = by(fx.get('sources'), 'source_id')
        origins = []
        for r in fx.get('records') or []:
            if not isinstance(r, dict):
                continue
            s = src.get(r.get('source_id')) or {}
            origin = s.get('origin_record_id')
            origins.append(origin)
            row = REF['evidence'].get(origin)
            if row is None:
                out.append(f'{o}:{r.get("synthetic_id")}: origen F34 inexistente {origin}')
                continue
            if row['state'] != 'vinculada' or row['source_type'] != 'synthetic' or row['source_type_ev'] not in EVIDENCE_KINDS:
                out.append(f'{o}:{origin}: registro F34 no elegible')
            if r.get('text_synthetic') != normalize_text(row['evidence_text']):
                out.append(f'{o}:{origin}: el texto no es T1(texto F34)')
            if r.get('criterion_ref') != row['criterion_id'] or r.get('evidence_kind') != row['source_type_ev']:
                out.append(f'{o}:{origin}: criterio o tipo distintos del origen F34')
            if s.get('origin_file') != F34_EVIDENCE or s.get('origin_dataset_version') != F34_VERSION:
                out.append(f'{o}:{origin}: archivo o versión de origen distintos de F34')
        if origins != expected_selection(o):
            out.append(f'{o}: selección no determinista: {origins} ≠ {expected_selection(o)}')
    return out


def r_run(D, P):
    out = []
    for o, fx in fixture_items(P):
        run = fx.get('run') if isinstance(fx.get('run'), dict) else {}
        rid = run.get('pipeline_run_id')
        if run.get('run_kind') != RUN_KIND:
            out.append(f'{o}: run_kind ≠ {RUN_KIND} (F35-SBX-A no ejecuta ningún pipeline)')
        start = str(run.get('clock_start', ''))
        for part in ('records', 'events', 'provenance', 'reviews', 'audit'):
            for x in fx.get(part) or []:
                if isinstance(x, dict) and x.get('pipeline_run_id') != rid:
                    out.append(f'{o}:{part}: referencia a un run inexistente {x.get("pipeline_run_id")}')
        events = [e for e in fx.get('events') or [] if isinstance(e, dict)]
        if [e.get('seq') for e in events] != list(range(1, len(events) + 1)):
            out.append(f'{o}: secuencia de eventos con huecos o desordenada')
        if [e.get('state') for e in events] != LIFECYCLE:
            out.append(f'{o}: ciclo de vida distinto de {LIFECYCLE}')
        audit = [a for a in fx.get('audit') or [] if isinstance(a, dict)]
        if [a.get('action') for a in audit] != AUDIT_ACTIONS:
            out.append(f'{o}: auditoría incompleta o desordenada')
        stamps = [str(e.get('at', '')) for e in events] + [str(a.get('at', '')) for a in audit]
        for part, key in (('records', 'created_at'), ('provenance', 'recorded_at'), ('reviews', 'reviewed_at')):
            stamps += [str(x.get(key, '')) for x in fx.get(part) or [] if isinstance(x, dict)]
        if any(s < start for s in stamps):
            out.append(f'{o}: instantes anteriores al reloj lógico del run')
        for seq in ([str(e.get('at', '')) for e in events], [str(a.get('at', '')) for a in audit]):
            if seq != sorted(seq):
                out.append(f'{o}: instantes no monótonos')
    return out


REVIEW_FORBIDDEN = CAP_TOKENS | {'merit', 'apt', 'idoneo', 'contratable', 'aprobado', 'rechazado', 'recomendable'}


LEGACY_REVIEW_SCOPE = 'integridad_procedencia_' + 'coherencia'     # valor anterior, nunca admitido (M03)


def r_rev(D, P):
    out = []
    for n, t in list(D['docs'].items()) + [(k, (v or b'').decode('utf-8', 'replace')) for k, v in D['raw'].items()]:
        if LEGACY_REVIEW_SCOPE in (t or ''):
            out.append(f'{n}: valor anterior de review_scope; el único admitido es {REVIEW_SCOPE}')
    for o, fx in fixture_items(P):
        recs = by(fx.get('records'), 'synthetic_id')
        revs = [x for x in fx.get('reviews') or [] if isinstance(x, dict)]
        per = {}
        for rv in revs:
            per.setdefault(rv.get('record_id'), []).append(rv)
        for rid, r in recs.items():
            got = per.get(rid, [])
            if len(got) != 1:
                out.append(f'{o}:{rid}: se exige exactamente una revisión humana simulada (hay {len(got)})')
                continue
            rv = got[0]
            if r.get('review_status') != rv.get('review_status'):
                out.append(f'{o}:{rid}: review_status del registro ≠ revisión')
        for rv in revs:
            rid = rv.get('review_id')
            if rv.get('record_id') not in recs:
                out.append(f'{o}:{rid}: revisión de un registro inexistente')
            if rv.get('reviewer_type') != REVIEWER_TYPE:
                out.append(f'{o}:{rid}: reviewer_type ≠ {REVIEWER_TYPE}')
            if rv.get('review_scope') != REVIEW_SCOPE:
                out.append(f'{o}:{rid}: review_scope distinto de {REVIEW_SCOPE}: la revisión solo cubre integridad '
                           f'y procedencia (DH-05)')
            if rv.get('review_status') not in REVIEW_STATUSES:
                out.append(f'{o}:{rid}: review_status «{rv.get("review_status")}» no admitido (solo {REVIEW_STATUSES})')
            if rv.get('scripted') is not True:
                out.append(f'{o}:{rid}: la decisión simulada debe venir declarada en el fixture (scripted=true)')
            if rv.get('simulation_actor') != f'SIMREV-{o}':
                out.append(f'{o}:{rid}: actor simulado de otro tenant')
            if set(rv) != set(EXPECTED_FIELDS['SyntheticHumanReview']):
                out.append(f'{o}:{rid}: campos de revisión fuera de integridad/procedencia {sorted(set(rv) ^ set(EXPECTED_FIELDS["SyntheticHumanReview"]))}')
            for path, k, v in walk(rv):
                if tokens(k) & REVIEW_FORBIDDEN or (isinstance(v, str) and tokens(v) & REVIEW_FORBIDDEN):
                    out.append(f'{o}:{rid}.{path}: la revisión evalúa a una persona (DH-05)')
    return out


PROD_VALUE = re.compile(r'pgsql|postgres|mysql|mariadb|sqlite|redis|\bDB_\w+|\.env\b|storage/|database/|(?<![\w-])app/|'
                        r'routes/|config/|resources/|ml-service|ML_SERVICE|localhost|127\.0\.0\.1|0\.0\.0\.0|https?://|'
                        r'audit_logs|insert\s+into|producci[oó]n|productiv|production', re.I)
PROD_FIELD = re.compile(r'(^|_)(table|tabla|db|database|connection|conexion|dsn|endpoint|url|uri|host|storage|'
                        r'persist\w*|deploy\w*|despliegue|webhook|api)(_|$)', re.I)
ADJUNTOS = re.compile(r'g0-evidence|adjuntos', re.I)
PERSIST_VERB = re.compile(r'\b(persist\w*|almacen\w*|guard\w*|escrib\w*|insert\w*|conect\w*|integr[ae]\w*|promuev\w*|'
                          r'promocion\w*|migr\w*|desplieg\w*|env[ií]\w*|alimenta\w*)\b', re.I)
PROD_TARGET = re.compile(r'producci[oó]n|productiv|audit_logs|runtime|laravel|postgre', re.I)


def r_sto(D, P):
    out = []
    for o, fx in fixture_items(P):
        for path, k, v in walk(fx):
            if PROD_FIELD.search(str(k)):
                out.append(f'{o}:{path}: campo de persistencia o integración productiva')
            if isinstance(v, str) and not HASH_KEY.search(str(k)):
                if PROD_VALUE.search(v):
                    out.append(f'{o}:{path}: referencia productiva «{v[:50]}»')
                if ADJUNTOS.search(v):
                    out.append(f'{o}:{path}: lectura desde g0-evidence/adjuntos')
        for s in fx.get('sources') or []:
            if isinstance(s, dict) and s.get('origin_file') != F34_EVIDENCE:
                out.append(f'{o}:{s.get("source_id")}: origen fuera del dataset F34 autorizado')
    for n, t in D['docs'].items():
        for i, prop, pol in doc_props(t):
            if pol != 'neg' and PERSIST_VERB.search(prop) and PROD_TARGET.search(prop):
                out.append(f'{n}:{i}: persistencia o conexión productiva afirmada: {prop[:80]}')
    return out


def manifest_schema():
    """Esquema estructural exacto del manifest: tipo exacto por clave y claves exactas en cada objeto.
    El manifest no define listas: una lista, un objeto bajo un campo de texto, null, un número o un booleano
    donde se espera otro tipo fallan antes de cualquier análisis semántico."""
    fixture = {'sha256': str, 'bytes': int, 'records': int, 'synthetic_organization_id': str}
    return {'manifest_version': str, 'contract_version': str, 'file_hash': str, 'source_type': str,
            'environment': str, 'note': str, 'derivation_rule': str,
            'f34': {'dataset_version': str, 'manifest_path': str, 'manifest_sha256': str, 'evidence_path': str,
                    'evidence_sha256': str},
            'files': {CONTRACT: {'sha256': str, 'bytes': int}, **{FIXTURES[o]: dict(fixture) for o in ORGS}}}


def check_structure(value, schema, path, out, strings):
    if isinstance(schema, dict):
        if type(value) is not dict:
            out.append(f'{path}: se exige un objeto, hay {type(value).__name__}')
            return
        extra, missing = sorted(set(value) - set(schema)), sorted(set(schema) - set(value))
        if extra or missing:
            out.append(f'{path}: claves no permitidas {extra} o ausentes {missing}')
        for k, sub in schema.items():
            if k in value:
                check_structure(value[k], sub, f'{path}.{k}', out, strings)
    elif type(value) is not schema:                       # exacto: bool no vale como int, None no vale nada
        out.append(f'{path}: tipo {type(value).__name__}, se exige {schema.__name__}')
    elif schema is str:
        strings.append((path, value))


def r_man(D, P):
    m = P['json'].get(MANIFEST)
    if m is None:
        return [f'manifest ilegible: {P["err"].get(MANIFEST, "ausente")} (falla cerrado)']
    struct, strings = [], []
    check_structure(m, manifest_schema(), 'manifest', struct, strings)
    if struct:
        return struct + ['manifest: estructura o tipos no admitidos; su contenido no se analiza (falla cerrado)']
    out = []
    for k, v in (('manifest_version', MANIFEST_VERSION), ('contract_version', CONTRACT_VERSION),
                 ('file_hash', 'sha256-bytes'), ('source_type', 'synthetic'), ('environment', 'sandbox')):
        if m[k] != v:
            out.append(f'manifest: {k} ≠ {v}')
    if 'NO representan datos reales' not in m['note']:
        out.append('manifest: falta la advertencia de datos no reales')
    exp34 = {'dataset_version': F34_VERSION, 'manifest_path': F34_MANIFEST, 'manifest_sha256': REF['manifest_sha'],
             'evidence_path': F34_EVIDENCE, 'evidence_sha256': REF['evidence_sha']}
    if m['f34'] != exp34 or not REF['ok']:
        out.append('manifest: referencias F34 distintas del dataset real')
    for n, e in m['files'].items():
        raw = D['raw'].get(n)
        if raw is None or e['sha256'] != sha_bytes(raw) or e['bytes'] != len(raw):
            out.append(f'manifest: SHA-256 o tamaño de {n} distinto del archivo')
    for o in ORGS:
        e, fx = m['files'][FIXTURES[o]], P['fixtures'].get(o)
        n = len(fx.get('records') or []) if isinstance(fx, dict) else -1
        if e['records'] != n or n != PER_TENANT or e['synthetic_organization_id'] != o:
            out.append(f'manifest: conteo u organización de {FIXTURES[o]} incoherentes')
    if 'evidence_id' not in m['derivation_rule']:
        out.append('manifest: falta la regla de selección determinista')
    out += [f'manifest{x}' for x in decoded_problems(m)]    # strings decodificados, antes de fold()
    for path, v in strings:                               # todos los textos permitidos por el esquema
        if path.endswith(('.sha256', '_sha256')):
            if not re.fullmatch(HASH_RX, v):
                out.append(f'{path}: no es un SHA-256')
        else:
            out += [f'{path}: {x}' for x in meta_problems(v)]
    return out


def meta_problems(text):
    """M02: un valor de metadatos no puede afirmar nada prohibido. Más estricto que los documentos: en un
    metadato, una categoría prohibida cuenta salvo que su proposición esté negada (la neutralidad no basta)."""
    # Un metadato es texto plano: cualquier estructura Markdown de bloque (código, HTML, lista, título…) podría ocultar
    # contenido al análisis, así que falla cerrado (contexto Markdown compartido).
    blocks = sorted({kind for _, kind in scan_markdown(text)} - {PLAIN, BLANK})
    out = [f'estructura Markdown de bloque no admitida en un metadato: {blocks}'] if blocks else []
    t = unmark(join_rf_breaks(text))
    out += [x.split(': ', 1)[-1] for x in V34E.clm({'v': t}, {})]
    decls, problems = V34E.parse_declarations(t)
    out += problems
    out += [f'declaración de estado en un metadato: {k} = {v}' for k, v in decls]
    for _, prop, pol in doc_props(t):
        if RF_INVALID in prop:
            out.append('predicado de RF-21/RF-23 con paréntesis no verificables (falla cerrado)')
        if pol == 'neg':
            continue
        for cat, rx in V34E.CLAIM_CATEGORIES.items():
            if rx.search(prop):
                out.append(f'afirma «{cat}»: {prop[:70]}')
        if V34E.G0_SUBJECT.search(prop) and V34E.G0_APPROVED.search(prop):
            out.append(f'afirma G0 real aprobada: {prop[:70]}')
        if PHASE_SUBJ.search(prop) and PHASE_VERB.search(prop) or RF_SUBJ.search(prop) and RF_VERB.search(prop):
            out.append(f'afirma una fase, puerta o RF alterada: {prop[:70]}')
        if PERSIST_VERB.search(prop) and PROD_TARGET.search(prop):
            out.append(f'afirma persistencia o integración productiva: {prop[:70]}')
        if tokens(prop) & CAP_TOKENS - {'level', 'nivel'}:
            out.append(f'capacidad prohibida {sorted(tokens(prop) & CAP_TOKENS)}: {prop[:70]}')
    return sorted(set(out))


def gov_section(t):
    sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', t or '', re.M | re.S)
    return sections[0] if len(sections) == 1 else None


def gov_lifecycle(D):
    """(estado, problemas) del ciclo de vida de F35-SBX-A según CLAUDE.md y docs/PROGRESS.md: INICIADA o CERRADA."""
    states, out = [], []
    for path in GOVERNANCE[:2]:
        sec = gov_section(D['gov'].get(path))
        if sec is None:
            out.append(f'{path}: se exige una sección única «Estado vigente F34E»')
            continue
        found = [st for st, phrase in LIFECYCLE_PHRASES.items() if phrase in sec]
        words = set(PHASE_STATE_RX.findall(sec))
        if len(found) != 1 or not words <= set(LIFECYCLE_PHRASES) or len(words) != 1:
            out.append(f'{path}: estado de F35-SBX-A ausente, contradictorio o desconocido {sorted(words)}')
        else:
            states.append(found[0])
    if len(set(states)) > 1:
        out.append(f'CLAUDE.md y docs/PROGRESS.md con estados distintos de F35-SBX-A: {states}')
    state = states[0] if len(states) == 2 and len(set(states)) == 1 else None
    return state, out


def r_gov(D, P):
    out = []
    g, f = gate_states(D)
    exp = dict(GOV_FIXED, **{'G0-SBX': g, 'F35-SBX': f})
    state, out = gov_lifecycle(D)
    for path in GOVERNANCE:
        t = D['gov'].get(path)
        if t is None:
            out.append(f'{path}: ilegible (falla cerrado)')
            continue
        sec = gov_section(t)
        if sec is None:
            out.append(f'{path}: se exige una sección única «Estado vigente F34E»')
            continue
        head = t.split('\n## ', 1)[0]
        if path == BASELINE_DOC:
            # ACADEMIC_BASELINE no registra la apertura (sigue en el texto de la base) y sí el cierre.
            words = set(PHASE_STATE_RX.findall(sec))
            if state == 'CERRADA' and (CLOSED not in sec or words != {'CERRADA'}):
                out.append(f'{path}: el cierre de F35-SBX-A debe registrarse también aquí, y solo el cierre')
            if state == 'INICIADA' and (words or NOT_STARTED not in sec):
                out.append(f'{path}: antes del cierre conserva el texto de la base')
        elif NOT_STARTED in sec or NOT_STARTED in head:
            out.append(f'{path}: el estado vigente sigue diciendo «{NOT_STARTED}»')
        if SBXB_STATE_RX.search(sec + head):
            out.append(f'{path}: F35-SBX-B no puede figurar iniciada')
        if state == 'CERRADA':
            if 'F35-SBX-B NO INICIADA' not in sec or 'Sin runtime productivo' not in sec:
                out.append(f'{path}: el cierre exige F35-SBX-B NO INICIADA y sin runtime productivo')
            if 'auditoría independiente PASS' not in sec or re.search(r'auditor[ií]a[^.;]*\bFAIL\b', sec, re.I):
                out.append(f'{path}: el cierre exige auditoría independiente PASS')
        declared = {}
        for ln in sec.splitlines():
            plain = V34E.strip_md(ln).strip().removeprefix('- ').strip()
            if '=' in plain:
                k, v = plain.split('=', 1)
                declared.setdefault(V34E.norm_key(k), []).append(' '.join(v.upper().split()))
        for k, v in exp.items():
            if declared.get(V34E.norm_key(k)) != [v]:
                out.append(f'{path}: «{k}» debe declararse una vez como {v}')
    if state == 'CERRADA':
        # Regresión final GREEN registrada en el plan de pruebas (fila GREEN con 0 fallas, sin «pendiente»).
        plan = D['docs'].get('F35SBX_Plan_Pruebas.md') or ''
        green = [ln for ln in plan.splitlines() if ln.startswith('| GREEN |')]
        if (len(green) != 1 or re.search(r'\bpendiente\b', green[0], re.I)
                or not green[0].rstrip(' |').endswith('0 fallas, código de salida 0')):
            out.append('cierre sin regresión final GREEN registrada en el plan de pruebas')
    return out


def r_gate(D, P):
    out = []
    g, f = gate_states(D)
    st = V34E.matrix_states({'F34E_Matriz_Criterios_G0_SBX.md': D['gate']['matrix']})
    if g != 'APROBADA CON RESTRICCIONES' or f != 'HABILITADA':
        out.append(f'G0-SBX = {g}, F35-SBX = {f}: F35-SBX bloqueada; el trabajo SBX se detiene')
    if len(st) != 18 or any(v != 'CUMPLE' for v in st.values()):
        out.append('la matriz G0-SBX no está 18/18 en CUMPLE')
    if '- **G0 = NO APROBADA.**' not in D['gate']['g0_real']:
        out.append('la decisión G0 real ya no declara «G0 = NO APROBADA»')
    return out


STDLIB_OK = {'ast', 'copy', 'csv', 'hashlib', 'importlib', 'json', 'os', 're', 'subprocess', 'sys', 'unicodedata'}


def r_dep(D, P):
    out = []
    if not D['sources']:
        return ['tools/f35sbx/ sin código legible (falla cerrado)']
    for rel, src in D['sources'].items():
        if not rel.endswith('.py'):
            out.append(f'tools/f35sbx/{rel}: solo se admite código Python')
            continue
        try:
            tree = ast.parse(src or '')
        except (SyntaxError, ValueError) as e:
            out.append(f'tools/f35sbx/{rel}: código ilegible ({e})')
            continue
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods |= {a.name.split('.')[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    out.append(f'tools/f35sbx/{rel}: importación relativa')
                mods.add((node.module or '').split('.')[0])
            elif isinstance(node, ast.Call):
                fn = node.func
                name = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else ''
                if name in ('__import__', 'import_module'):
                    out.append(f'tools/f35sbx/{rel}: importación dinámica')
        for mname in sorted(mods - STDLIB_OK):
            out.append(f'tools/f35sbx/{rel}: dependencia no autorizada «{mname}» (solo biblioteca estándar; sin sqlite3)')
    return out


def content_problems(p, data):
    if data is None:
        return [f'{p}: ausente o ilegible (falla cerrado)']
    out = []
    if len(data) > 262144:
        out.append(f'{p}: tamaño {len(data)} > 256 KiB')
    if b'\x00' in data or b'\r' in data:
        out.append(f'{p}: binario o CR')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return out + [f'{p}: no es UTF-8']
    if p.endswith('.json'):
        try:
            json.loads(text)
        except ValueError:
            out.append(f'{p}: JSON inválido')
    return out


def r_git(D, P):
    g = D['git']
    if g.get('error'):
        return [f'estado Git desconocido (falla cerrado): {g["error"]}']
    out = [f'eliminación no autorizada: {p}' for p in sorted(g['deleted'])]
    for p in sorted(g['changed']):
        if p in F35_EXACT:
            continue
        if p in GOVERNANCE:
            h = g.get('governance', {}).get(p) or {}
            state = SCOPE.lifecycle(p, h['text'], h['base']) if h.get('text') and h.get('base') else None
            if state is None:
                out.append(f'{p}: gobierno distinto de la apertura o del cierre autorizados de F35-SBX-A (falla cerrado)')
            continue
        if p in F35_HISTORICAL:
            h = g['historical'].get(p) or {}
            if not h.get('text') or not h.get('base'):
                out.append(f'{p}: validador histórico o su base ilegibles (falla cerrado)')
            else:
                out += SCOPE.validator_problems(p, h['text'], h['base'])
            continue
        if f35_path_ok(p):
            out += content_problems(p, g['contents'].get(p))
            continue
        out.append(f'cambio fuera del alcance de F35-SBX-A: {p}')
    states = {SCOPE.lifecycle(p, h['text'], h['base']) for p, h in (g.get('governance') or {}).items()
              if p in g['changed'] and h.get('text') and h.get('base')}
    if len(states - {None}) > 1:
        out.append(f'gobierno con estados de ciclo de vida distintos entre documentos: {sorted(states - {None})}')
    if 'CERRADA' in states and not all(p in g['changed'] for p in GOVERNANCE):
        out.append('cierre de F35-SBX-A sin registrar en los tres documentos de gobierno')
    if 'INICIADA' in states and BASELINE_DOC in g['changed']:
        out.append(f'{BASELINE_DOC}: solo puede cambiar para registrar el cierre')
    v, mode = g['v34b']
    if v or mode != 'post':
        out.append(f'validate_f34b.git_scope debe ser post sin violaciones: {mode} {v[:2]}')
    return out


RULES = [('DOC', r_doc), ('TSB', r_tsb), ('TRZ', r_trz), ('STA', r_sta), ('CLM', r_clm), ('PHS', r_phs),
         ('CON', r_con), ('SCH', r_sch), ('SYN', r_syn), ('PII', r_pii), ('MED', r_med), ('CAP', r_cap),
         ('PER', r_per), ('ISO', r_iso), ('HSH', r_hsh), ('PRV', r_prv), ('ORI', r_ori), ('RUN', r_run),
         ('REV', r_rev), ('STO', r_sto), ('MAN', r_man), ('GOV', r_gov), ('GATE', r_gate), ('DEP', r_dep),
         ('GIT', r_git)]


def run_rules(D):
    P = parse(D)
    out = {}
    for rid, fn in RULES:
        try:
            out[rid] = fn(D, P)
        except Exception as e:                     # cualquier excepción inesperada: falla cerrado, nunca «pasa»
            out[rid] = [f'excepción {type(e).__name__}: {e} (falla cerrado)']
    return out


# ---------------------------------------------------------------- casos negativos (en memoria)
def mutate(fn):
    def f(D):
        D = copy.deepcopy(D)
        fn(D)
        return D
    return f


def fx(org, fn):
    """Aplica fn al fixture interpretado y lo vuelve a serializar (el manifest no se actualiza)."""
    def apply(D):
        obj = json.loads(D['raw'][FIXTURES[org]].decode('utf-8'))
        fn(obj)
        D['raw'][FIXTURES[org]] = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return mutate(apply)


def rec(field, value, org='ORG-S1', part='records', i=0):
    def fn(obj):
        obj[part][i][field] = value
    return fx(org, fn)


def text_add(extra, org='ORG-S1'):
    def fn(obj):
        obj['records'][0]['text_synthetic'] += extra
    return fx(org, fn)


def doc_add(text, n='F35SBX_Alcance.md'):
    def fn(D):
        D['docs'][n] = (D['docs'][n] or '') + '\n\n' + text + '\n'
    return mutate(fn)


def doc_sub(n, a, b):
    def fn(D):
        assert a in (D['docs'][n] or ''), (n, a)
        D['docs'][n] = D['docs'][n].replace(a, b, 1)
    return mutate(fn)


def raw_set(name, data):
    def fn(D):
        D['raw'][name] = data
    return mutate(fn)


def contract(fn):
    def apply(D):
        obj = json.loads(D['raw'][CONTRACT].decode('utf-8'))
        fn(obj)
        D['raw'][CONTRACT] = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return mutate(apply)


def git_with(changed=(), contents=None, deleted=(), error=None, v34b=None):
    def fn(D):
        g = D['git']
        if error:
            g['error'] = error
            return
        g['changed'] = set(g['changed']) | set(changed)
        g['deleted'] = set(g['deleted']) | set(deleted)
        g['contents'] = dict(g['contents'], **(contents or {}))
        if v34b is not None:
            g['v34b'] = v34b
    return mutate(fn)


def gov_phase(fn, path='CLAUDE.md'):
    """Reemplaza la frase canónica del estado vigente (INICIADA o CERRADA) del documento de gobierno."""
    def apply(D):
        t = D['gov'][path] or ''
        phrase = next(ph for ph in (CLOSED, STARTED) if ph in t)
        D['gov'][path] = t.replace(phrase, fn(phrase), 1)
    return mutate(apply)


def gov_all(a, b):
    """Mismo cambio en los tres documentos de gobierno."""
    def apply(D):
        for p in GOVERNANCE:
            assert a in (D['gov'][p] or ''), (p, a)
            D['gov'][p] = D['gov'][p].replace(a, b, 1)
    return mutate(apply)


def gov_git(path, fn):
    """Contenido de gobierno distinto en el estado Git (el delta exacto se compara con la base)."""
    def apply(D):
        h = dict((D['git'].get('governance') or {}).get(path) or {})
        if not h.get('base'):
            h['base'] = SCOPE.git(ROOT, 'show', f'{BASE}:{path}')[1]
        h['text'] = fn(h.get('text') or h['base'])
        D['git']['governance'] = dict(D['git'].get('governance') or {}, **{path: h})
        D['git']['changed'] = set(D['git']['changed']) | {path}
    return mutate(apply)


def gov_sub(a, b, path='CLAUDE.md'):
    def fn(D):
        assert a in (D['gov'][path] or ''), (path, a)
        D['gov'][path] = D['gov'][path].replace(a, b, 1)
    return mutate(fn)


def swap_origin(obj):
    """Usa como origen una evidencia F34 de ORG-S2 en el fixture de ORG-S1 (texto y hashes coherentes)."""
    other = expected_selection('ORG-S2')[0]
    row = REF['evidence'][other]
    obj['sources'][0]['origin_record_id'] = other
    obj['records'][0]['text_synthetic'] = normalize_text(row['evidence_text'])


def later_origin(obj):
    """Evidencia F34 válida de ORG-S1 pero fuera de la regla de selección determinista."""
    rows = sorted((r for r in REF['evidence'].values() if r['organization'] == 'ORG-S1' and r['state'] == 'vinculada'
                   and r['source_type_ev'] in EVIDENCE_KINDS), key=lambda r: r['evidence_id'])
    row = rows[PER_TENANT + 3]
    obj['sources'][0]['origin_record_id'] = row['synthetic_record_id']
    obj['records'][0].update(text_synthetic=normalize_text(row['evidence_text']), criterion_ref=row['criterion_id'],
                             evidence_kind=row['source_type_ev'])


def drop(part, i=0, org='ORG-S1'):
    def fn(obj):
        del obj[part][i]
    return fx(org, fn)


def historical_extra(path, base=''):
    """Validador histórico adaptado con un cambio funcional adicional (o con la base ilegible si base=None)."""
    def fn(D):
        rc, real_base = SCOPE.git(ROOT, 'show', f'{BASE}:{path}')
        good = SCOPE.expected_validator(path, real_base) if rc == 0 else None
        D['git']['changed'] = set(D['git']['changed']) | {path}
        D['git']['historical'] = dict(D['git'].get('historical') or {}, **{path: {
            'text': (good or '') + "\nprint('cambio no autorizado')\n",
            'base': real_base if base is not None else None}})
    return mutate(fn)


GOOD_PY = b'import json\n'
CASES = [
    # ---- datos personales y media
    ('NS-01', 'PII', 'PII real: número de DNI en el texto', text_add(' DNI 45871236.')),
    ('NS-02', 'PII', 'Campo real_name', rec('real_name', 'Ana Torres Quispe')),
    ('NS-03', 'PII', 'Correo en el texto', text_add(' Contacto: ana.torres@correo.pe')),
    ('NS-04', 'PII', 'Campo dni', rec('dni', '45871236')),
    ('NS-05', 'MED', 'CV: campo cv con un archivo', rec('cv', 'curriculum_postulante.pdf')),
    ('NS-06', 'MED', 'PDF o DOCX citado en el texto', text_add(' Ver anexo informe_entrevista.docx')),
    ('NS-07', 'MED', 'Audio: campo audio_ref', rec('audio_ref', 'entrevista_01.mp3')),
    ('NS-08', 'MED', 'Vídeo citado en el texto', text_add(' Grabación sesion.mp4')),
    ('NS-09', 'MED', 'Imagen guardada en evidencia-sbx/', mutate(lambda D: D['files'].append('fixtures/foto.png'))),
    ('NS-10', 'MED', 'Bloque base64 en el texto', text_add(' ' + 'QUJDREVGR0hJSktMTU5PUFFSU1RVVldY' * 2)),
    ('NS-11', 'MED', 'Data URI en el texto', text_add(' data:image/png;base64,iVBORw0KGgo')),
    ('NS-12', 'MED', 'Fixture binario (bytes NUL)', raw_set(FIXTURES['ORG-S2'], b'{"a":\x00}')),
    # ---- marcadores synthetic-only y esquema
    ('NS-13', 'SYN', 'source_type distinto de synthetic', rec('source_type', 'real')),
    ('NS-14', 'SYN', 'Marcador [SINTÉTICO] ausente',
     fx('ORG-S1', lambda o: o['records'][0].update(text_synthetic=o['records'][0]['text_synthetic'].replace(MARKER + ' ', '')))),
    ('NS-15', 'SYN', 'environment distinto de sandbox', rec('environment', 'production')),
    ('NS-16', 'SCH', 'Campo desconocido en un registro (contrato cerrado)', rec('comentario_libre', 'texto')),
    ('NS-17', 'SCH', 'Fixture con JSON inválido (falla cerrado)', raw_set(FIXTURES['ORG-S3'], b'{"records": [')),
    ('NS-18', 'SCH', 'evidence_kind «cv» fuera del enum', rec('evidence_kind', 'cv')),
    ('NS-19', 'SCH', 'Marcado HTML en el texto (T2, XSS)', text_add(' <script>alert(1)</script>')),
    # ---- aislamiento, hashes, provenance, origen y run
    ('NS-20', 'ISO', 'Organización cruzada en un registro', rec('synthetic_organization_id', 'ORG-S2')),
    ('NS-21', 'ISO', 'Origen F34 de otra organización', fx('ORG-S1', swap_origin)),
    ('NS-22', 'HSH', 'content_hash alterado', rec('content_hash', 'f' * 64)),
    ('NS-23', 'HSH', 'hash_before alterado', rec('hash_before', 'e' * 64, part='provenance')),
    ('NS-24', 'HSH', 'Cadena de eventos rota', rec('prev_event_hash', 'a' * 64, part='events', i=2)),
    ('NS-25', 'HSH', 'Cadena de provenance rota', rec('prev_provenance_hash', 'b' * 64, part='provenance', i=1)),
    ('NS-26', 'PRV', 'Provenance ausente', drop('provenance')),
    ('NS-27', 'PRV', 'Transformación no registrada', rec('transformation_id', 'T9-reescritura', part='provenance')),
    ('NS-28', 'ORI', 'Origen F34 inexistente', rec('origin_record_id', 'SYN-999999', part='sources')),
    ('NS-29', 'ORI', 'Texto distinto del origen F34', fx('ORG-S2', lambda o: o['records'][1].update(
        text_synthetic=MARKER + ' Texto reescrito sin relación con el origen.'))),
    ('NS-30', 'ORI', 'Selección no determinista (evidencia elegida a mano)', fx('ORG-S1', later_origin)),
    ('NS-31', 'RUN', 'Run inexistente', rec('pipeline_run_id', 'SBXR-ORG-S1-9999')),
    ('NS-32', 'RUN', 'Eventos con huecos', fx('ORG-S3', lambda o: o['events'].pop(3))),
    ('NS-33', 'RUN', 'Instante anterior al reloj lógico', rec('created_at', '2020-01-01T00:00:00')),
    # ---- revisión humana simulada
    ('NS-34', 'REV', 'Revisión ausente', drop('reviews')),
    ('NS-35', 'REV', 'reviewer_type incorrecto', rec('reviewer_type', 'system_auto', part='reviews')),
    ('NS-36', 'REV', 'review_status «apto»', rec('review_status', 'apto', part='reviews')),
    ('NS-37', 'REV', 'Revisión que evalúa aptitud', rec('aptitud', 'alta', part='reviews')),
    ('NS-38', 'REV', 'Revisión no declarada en el fixture (scripted=false)', rec('scripted', False, part='reviews')),
    # ---- capacidades prohibidas
    ('NS-39', 'CAP', 'scoring: campo score', rec('score', 0.87)),
    ('NS-40', 'CAP', 'ranking: campo ranking_position', rec('ranking_position', 1)),
    ('NS-41', 'CAP', 'recommendation', rec('recommendation', 'contratar')),
    ('NS-42', 'CAP', 'best_candidate', rec('best_candidate', True)),
    ('NS-43', 'CAP', 'automatic_selection', rec('automatic_selection', True)),
    ('NS-44', 'CAP', 'OCR como transformación', rec('transformation_id', 'ocr-pdf-v1', part='provenance')),
    ('NS-45', 'CAP', 'parsing', rec('parsing_engine', 'pdfminer')),
    ('NS-46', 'CAP', 'extraction', rec('extraction_method', 'automatica')),
    ('NS-47', 'CAP', 'embeddings', rec('embedding', [0.12, 0.33, 0.91])),
    ('NS-48', 'CAP', 'vector', rec('vector_ref', 'idx-0001')),
    ('NS-49', 'CAP', 'semantic_search', rec('semantic_search', 'enabled')),
    ('NS-50', 'PER', 'Token de persona APP- en el texto', text_add(' Ref. APP-00001')),
    ('NS-51', 'PER', 'Campo person_token', rec('person_token', 'PER-S-00001')),
    # ---- producción, almacenamiento y adjuntos
    ('NS-52', 'STO', 'Integración productiva: endpoint en el run',
     fx('ORG-S1', lambda o: o['run'].update(endpoint='https://colegio.example/api'))),
    ('NS-53', 'STO', 'Persistencia productiva: destino pgsql/audit_logs',
     fx('ORG-S1', lambda o: o['run'].update(storage_target='pgsql://db/audit_logs'))),
    ('NS-54', 'STO', 'Lectura desde g0-evidence/adjuntos',
     rec('origin_file', 'docs/academico/g0-evidence/adjuntos/README.md', part='sources')),
    ('NS-55', 'STO', 'Documento que afirma persistencia en producción',
     doc_add('Los registros SBX se persisten en las tablas productivas de Laravel.')),
    ('NS-56', 'CLM', 'Documento que afirma integración productiva', doc_add('F35-SBX-A habilita la integración con producción.')),
    # ---- dependencias, runtime y Git
    ('NS-57', 'DEP', 'Nueva dependencia (numpy)', mutate(lambda D: D['sources'].__setitem__('extra.py', 'import numpy as np\n'))),
    ('NS-58', 'DEP', 'sqlite3 en F35-SBX-A (DH-07)', mutate(lambda D: D['sources'].__setitem__('extra.py', 'import sqlite3\n'))),
    ('NS-59', 'GIT', 'Archivo runtime (app/)', git_with(changed={'app/Models/SyntheticEvidence.php'})),
    ('NS-60', 'GIT', 'Migración productiva (database/)', git_with(changed={'database/migrations/2026_10_07_create_sbx.php'})),
    ('NS-61', 'GIT', 'Prueba en tests/ (ruta protegida)', git_with(changed={'tests/Feature/SbxTest.php'})),
    ('NS-62', 'GIT', 'Modificación de RF-21/RF-23 en la matriz de trazabilidad',
     git_with(changed={'docs/final-report/traceability-master.md'})),
    ('NS-63', 'GIT', 'Evidencia F34B/C/D modificada', git_with(changed={'docs/academico/g0-evidence/F34B_Decision_G0.md'})),
    ('NS-64', 'GIT', 'Binario con extensión permitida en evidencia-sbx/',
     git_with(changed={REL_SBX + 'fixtures/extra.json'}, contents={REL_SBX + 'fixtures/extra.json': b'\x89PNG\x00'})),
    ('NS-65', 'GIT', 'Imagen en evidencia-sbx/', git_with(changed={REL_SBX + 'fixtures/foto.png'})),
    ('NS-66', 'GIT', 'JSON en tools/f35sbx/ (solo Python)', git_with(changed={REL_TOOLS + 'datos.json'},
                                                                    contents={REL_TOOLS + 'datos.json': b'{}'})),
    ('NS-67', 'GIT', 'Prefijo confundible evidencia-sbx-otro/', git_with(changed={'docs/academico/evidencia-sbx-otro/a.md'})),
    ('NS-68', 'GIT', 'Git desconocido o con error (falla cerrado)', git_with(error='git no disponible')),
    ('NS-69', 'GIT', 'Eliminación de un archivo', git_with(deleted={'docs/academico/g0-sandbox/README.md'})),
    ('NS-70', 'GIT', 'Alcance de validate_f34b no válido', git_with(v34b=(['UNKNOWN'], 'unknown'))),
    # ---- estados, fases y gobierno
    ('NS-71', 'CLM', 'G0 real aprobada', doc_add('Con F35-SBX-A la G0 real quedó aprobada.')),
    ('NS-72', 'STA', '«G0 real = APROBADA» en el README',
     doc_sub('README.md', '**G0 real = NO APROBADA**', '**G0 real = APROBADA**')),
    ('NS-73', 'CLM', 'F35 productiva habilitada', doc_add('La F35 productiva queda habilitada.')),
    ('NS-74', 'PHS', 'F36 iniciada', doc_add('F36 queda iniciada en paralelo.')),
    ('NS-75', 'PHS', 'Modificación de RF-23', doc_add('F35-SBX-A modifica RF-23 para que la decisión sea automática.')),
    ('NS-76', 'PHS', 'Modificación de RF-21', doc_add('Se reemplaza RF-21 por un orden calculado.')),
    ('NS-77', 'CLM', 'Alcance C por conector concesivo', doc_add('No hay scoring; sin embargo OCR sobre documentos.')),
    ('NS-78', 'STA', 'Alias desconocido de un estado crítico', doc_add('- G0 productiva = NO APROBADA', 'README.md')),
    ('NS-79', 'STA', 'F35-SBX BLOQUEADA en el README con la puerta vigente',
     doc_sub('README.md', '**F35-SBX = HABILITADA**', '**F35-SBX = BLOQUEADA**')),
    ('NS-80', 'GOV', 'Gobierno sigue «AÚN NO INICIADA»', gov_phase(lambda ph: 'F35-SBX AÚN NO INICIADA.')),
    ('NS-81', 'GOV', 'INICIADA y CERRADA a la vez', gov_phase(lambda ph: STARTED + ' ' + CLOSED, 'docs/PROGRESS.md')),
    ('NS-82', 'GATE', 'Decisión G0 real alterada', mutate(lambda D: D['gate'].__setitem__('g0_real', '- **G0 = APROBADA.**'))),
    # ---- contrato, manifest y documentos
    ('NS-83', 'CON', 'additionalProperties=true en el registro',
     contract(lambda c: c['$defs']['SyntheticEvidenceRecord'].update(additionalProperties=True))),
    ('NS-84', 'CON', 'Campo score añadido al contrato',
     contract(lambda c: (c['$defs']['SyntheticEvidenceRecord']['properties'].update(score={'type': 'integer'}),
                         c['$defs']['SyntheticEvidenceRecord']['required'].append('score')))),
    ('NS-85', 'CON', 'reviewer_type relajado a cadena libre',
     contract(lambda c: c['$defs']['SyntheticHumanReview']['properties'].update(reviewer_type={'type': 'string'}))),
    ('NS-86', 'CON', 'Palabra clave de esquema desconocida',
     contract(lambda c: c['$defs']['SyntheticEvidenceSource'].update(patternProperties={'.*': {}}))),
    ('NS-87', 'MAN', 'SHA-256 de un fixture distinto del manifest', text_add(' ', org='ORG-S3')),
    ('NS-88', 'MAN', 'Manifest ausente', raw_set(MANIFEST, None)),
    ('NS-89', 'DOC', 'Documento obligatorio ausente', mutate(lambda D: D['docs'].__setitem__('F35SBX_Provenance.md', None))),
    ('NS-90', 'DOC', 'Enlace roto', doc_add('[detalle](F35SBX_Inexistente.md)')),
    # ---- validadores históricos adaptados (rutas exactas, contenido comparado con la base)
    ('NS-91', 'GIT', 'Cuarto validador no autorizado (validate_f34a.py)',
     git_with(changed={'docs/academico/tools/f34a/validate_f34a.py'})),
    ('NS-92', 'GIT', 'Cambio funcional extra en validate_f30.py', historical_extra('docs/academico/tools/f30/validate_f30.py')),
    ('NS-93', 'GIT', 'Cambio funcional extra en validate_f33.py', historical_extra('docs/academico/tools/f33/validate_f33.py')),
    ('NS-94', 'GIT', 'Cambio funcional extra en validate_f34.py', historical_extra('docs/academico/tools/f34/validate_f34.py')),
    ('NS-95', 'GIT', 'Base del validador histórico ilegible',
     historical_extra('docs/academico/tools/f34/validate_f34.py', base=None)),
]


def man_set(key, value, sub=None):
    """Cambia (o añade) un valor del manifest; con sub, dentro de files[sub]."""
    def fn(D):
        m = json.loads(D['raw'][MANIFEST].decode('utf-8'))
        target = m['files'][sub] if sub else m
        target[key] = value(target.get(key)) if callable(value) else value
        D['raw'][MANIFEST] = (json.dumps(m, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return mutate(fn)


def raw_sub(name, old, new):
    """Edita el texto JSON tal cual (para claves duplicadas, que json.dumps nunca produce)."""
    def fn(D):
        t = D['raw'][name].decode('utf-8')
        assert old in t, (name, old)
        D['raw'][name] = t.replace(old, new, 1).encode('utf-8')
    return mutate(fn)


def man_escaped(key, value):
    """Manifest serializado con escapes \\uXXXX (ensure_ascii): el archivo no contiene el carácter literal."""
    def fn(D):
        m = json.loads(D['raw'][MANIFEST].decode('utf-8'))
        m[key] = value(m[key]) if callable(value) else value
        D['raw'][MANIFEST] = (json.dumps(m, ensure_ascii=True, indent=2) + '\n').encode('utf-8')
    return mutate(fn)


def fx_escaped(org, extra):
    def fn(D):
        obj = json.loads(D['raw'][FIXTURES[org]].decode('utf-8'))
        obj['records'][0]['text_synthetic'] += extra
        D['raw'][FIXTURES[org]] = (json.dumps(obj, ensure_ascii=True, indent=2) + '\n').encode('utf-8')
    return mutate(fn)


def review_scope(value):
    return fx('ORG-S2', lambda o: o['reviews'][0].update(review_scope=value))


CASES += [
    # ---- M01: el Markdown no oculta contenido semántico
    ('NS-96', 'CLM', 'scoring entre backticks', doc_add('Se habilita `scoring` de candidatos.')),
    ('NS-97', 'CLM', 'OCR entre backticks', doc_add('Se habilita `OCR` sobre documentos.')),
    ('NS-98', 'PHS', 'RF-23 entre backticks', doc_add('Se reemplaza `RF-23` por decisión automática.')),
    ('NS-99', 'PHS', 'rf-23 en minúsculas', doc_add('Se reemplaza rf-23 por una decisión automática.')),
    ('NS-100', 'CLM', 'scoring en negrita', doc_add('Se habilita **scoring** de candidatos.')),
    ('NS-101', 'CLM', 'scoring en cursiva con asterisco', doc_add('Se habilita *scoring* de candidatos.')),
    ('NS-102', 'CLM', 'scoring en cursiva con guion bajo', doc_add('Se habilita _scoring_ de candidatos.')),
    ('NS-103', 'CLM', 'scoring tachado', doc_add('Se habilita ~~scoring~~ de candidatos.')),
    ('NS-104', 'CLM', 'OCR en negrita y backticks', doc_add('Se habilita **`OCR`** sobre documentos.')),
    ('NS-105', 'CLM', 'Mayúsculas con backticks', doc_add('SE HABILITA `SCORING` DE CANDIDATOS.')),
    ('NS-106', 'PHS', 'rf-21 entre backticks', doc_add('Se modifica `rf-21` para otro orden.')),
    # ---- M02: ningún valor del manifest es un canal de bypass
    ('NS-107', 'MAN', 'note = «Se recomienda al mejor candidato»', man_set('note', 'Se recomienda al mejor candidato')),
    ('NS-108', 'MAN', 'note = «G0 real = APROBADA»', man_set('note', 'G0 real = APROBADA')),
    ('NS-109', 'MAN', 'derivation_rule con scoring',
     man_set('derivation_rule', 'Las filas se ordenan por scoring de evidence_id.')),
    ('NS-110', 'MAN', 'note válida con recomendación añadida',
     man_set('note', lambda v: v + ' Se recomienda al mejor candidato.')),
    ('NS-111', 'MAN', 'note con OCR en negrita y backticks', man_set('note', lambda v: v + ' Se habilita **`OCR`** sobre documentos.')),
    ('NS-112', 'MAN', 'note en mayúsculas', man_set('note', lambda v: v + ' SE RECOMIENDA AL MEJOR CANDIDATO.')),
    ('NS-113', 'MAN', 'note con negación mixta',
     man_set('note', lambda v: v + ' No usa datos reales, pero sí recomendación automática.')),
    ('NS-114', 'MAN', 'derivation_rule que reemplaza RF-23', man_set('derivation_rule', lambda v: v + ' Se reemplaza RF-23.')),
    ('NS-115', 'MAN', 'note con F35 productiva habilitada', man_set('note', lambda v: v + ' F35 productiva = HABILITADA.')),
    ('NS-116', 'MAN', 'Clave desconocida en el manifest', man_set('comentario', 'texto libre')),
    ('NS-117', 'MAN', 'Clave desconocida en files[]', man_set('nota', 'texto libre', sub=FIXTURES['ORG-S1'])),
    ('NS-118', 'MAN', 'note con alcance C habilitado', man_set('note', lambda v: v + ' Alcance C = HABILITADO.')),
    ('NS-119', 'MAN', 'note con datos reales permitidos', man_set('note', lambda v: v + ' Se permiten datos reales.')),
    # ---- M03: review_scope tiene un único valor admitido
    ('NS-120', 'REV', 'review_scope anterior (tres términos)', review_scope(LEGACY_REVIEW_SCOPE)),
    ('NS-121', 'REV', 'review_scope = seleccion', review_scope('seleccion')),
    ('NS-122', 'REV', 'review_scope = evaluacion_candidato', review_scope('evaluacion_candidato')),
    ('NS-123', 'REV', 'review_scope = idoneidad', review_scope('idoneidad')),
    ('NS-124', 'REV', 'review_scope = aptitud', review_scope('aptitud')),
    ('NS-125', 'REV', 'review_scope = recomendacion', review_scope('recomendacion')),
    ('NS-126', 'REV', 'review_scope vacío', review_scope('')),
    ('NS-127', 'CON', 'Contrato con el review_scope anterior',
     contract(lambda c: c['$defs']['SyntheticHumanReview']['properties'].update(review_scope={'const': LEGACY_REVIEW_SCOPE}))),
    ('NS-128', 'REV', 'Valor anterior de review_scope citado en un documento',
     doc_add('La revisión usa ' + LEGACY_REVIEW_SCOPE + '.')),
    # ---- segunda reauditoría: normalización RF, Unicode y Scope C
    ('NS-129', 'PHS', 'RF23 sin guion', doc_add('RF23 pasa a ser automática.')),
    ('NS-130', 'PHS', 'RF 23 con espacio', doc_add('Se automatiza RF 23.')),
    ('NS-131', 'PHS', 'RF–23 con raya corta', doc_add('Se automatiza RF\u201323.')),
    ('NS-132', 'PHS', 'RF—23 con raya larga', doc_add('Se automatiza RF\u201423.')),
    ('NS-133', 'PHS', 'RF21 sin guion', doc_add('RF21 pasa a ser automática.')),
    ('NS-134', 'PHS', 'rf‑21 con guion no separable', doc_add('Se modifica rf\u201121.')),
    ('NS-135', 'CLM', 'scoring en ancho completo', doc_add('Se habilita \uff53\uff43\uff4f\uff52\uff49\uff4e\uff47 de candidatos.')),
    ('NS-136', 'CLM', 'scoring con U+200B', doc_add('Se habilita s\u200bcoring de candidatos.')),
    ('NS-137', 'CLM', 'scoring con U+2060 y U+FEFF', doc_add('Se habilita sc\u2060or\ufeffing de candidatos.')),
    ('NS-138', 'CLM', 'Scope C habilitado', doc_add('Scope C habilitado.')),
    ('NS-139', 'CLM', 'Se habilita Scope C', doc_add('Se habilita Scope C.')),
    ('NS-140', 'CLM', 'Se activa alcance C', doc_add('Se activa alcance C.')),
    ('NS-141', 'PHS', 'scope c en minúsculas', doc_add('Queda activado scope c.')),
    # ---- segunda reauditoría: manifest cerrado por estructura y tipos exactos
    ('NS-142', 'MAN', 'note como lista', man_set('note', lambda v: [v])),
    ('NS-143', 'MAN', 'note como objeto', man_set('note', lambda v: {'texto': v})),
    ('NS-144', 'MAN', 'note null', man_set('note', None)),
    ('NS-145', 'MAN', 'note numérica', man_set('note', 7)),
    ('NS-146', 'MAN', 'derivation_rule como lista', man_set('derivation_rule', lambda v: [v])),
    ('NS-147', 'MAN', 'Objeto adicional en el primer nivel', man_set('extra', {'texto': 'libre'})),
    ('NS-148', 'MAN', 'Clave desconocida en files del contrato', man_set('nota', 'libre', sub=CONTRACT)),
    ('NS-149', 'MAN', 'Clave desconocida en files de un fixture', man_set('comentario', 'libre', sub=FIXTURES['ORG-S2'])),
    ('NS-150', 'MAN', 'Frase partida en parte1/parte2', man_set('note', {'parte1': 'G0 real', 'parte2': 'APROBADA'})),
    ('NS-151', 'MAN', 'note con scoring en ancho completo', man_set('note', lambda v: v + ' Se habilita \uff53\uff43\uff4f\uff52\uff49\uff4e\uff47.')),
    ('NS-152', 'MAN', 'note con scoring y U+200B', man_set('note', lambda v: v + ' Se habilita s\u200bcoring.')),
    ('NS-153', 'MAN', 'note con RF23', man_set('note', lambda v: v + ' RF23 pasa a ser automática.')),
    ('NS-154', 'MAN', 'derivation_rule con Scope C', man_set('derivation_rule', lambda v: v + ' Se habilita Scope C.')),
    ('NS-155', 'MAN', 'bytes booleano en files', man_set('bytes', True, sub=CONTRACT)),
    ('NS-156', 'MED', 'Carácter invisible U+200B en un fixture', text_add(' s\u200b')),
    # ---- tercera reauditoría: Markdown + normalización posterior
    ('NS-157', 'PHS', '`RF` 23', doc_add('Se automatiza `RF` 23.')),
    ('NS-158', 'PHS', '**RF**23', doc_add('Se automatiza **RF**23.')),
    ('NS-159', 'PHS', '*RF* 23', doc_add('Se automatiza *RF* 23.')),
    ('NS-160', 'PHS', '_RF_23', doc_add('Se automatiza _RF_23.')),
    ('NS-161', 'CLM', '**Scope** C', doc_add('Se habilita **Scope** C.')),
    ('NS-162', 'CLM', '`Scope` C', doc_add('Se habilita `Scope` C.')),
    ('NS-163', 'CLM', '*alcance* C', doc_add('Se activa *alcance* C.')),
    ('NS-164', 'PHS', '`RF` 23 automática', doc_add('`RF` 23 automática.')),
    ('NS-165', 'PHS', '**RF**23 automática', doc_add('**RF**23 automática.')),
    ('NS-166', 'PHS', '*RF* 23 automática', doc_add('*RF* 23 automática.')),
    ('NS-167', 'CLM', '**Scope** C habilitado', doc_add('**Scope** C habilitado.')),
    ('NS-168', 'CLM', '`Scope` C habilitado', doc_add('`Scope` C habilitado.')),
    # ---- RF + separador + predicado
    ('NS-169', 'PHS', 'RF-23: automática', doc_add('RF-23: automática.')),
    ('NS-170', 'PHS', 'RF-21: automática', doc_add('RF-21: automática.')),
    ('NS-171', 'PHS', 'RF 23 — automática', doc_add('RF 23 \u2014 automática.')),
    ('NS-172', 'PHS', 'RF23 = automática', doc_add('RF23 = automática.')),
    ('NS-173', 'PHS', 'RF-23 -> automática', doc_add('RF-23 -> automática.')),
    ('NS-174', 'PHS', 'RF23: selección automática', doc_add('RF23: selección automática.')),
    ('NS-175', 'PHS', 'RF-21: automatizada', doc_add('RF-21: automatizada.')),
    ('NS-176', 'PHS', 'RF-23 → decisión automática', doc_add('RF-23 \u2192 decisión automática.')),
    ('NS-177', 'MAN', 'note con RF-23: automática', man_set('note', lambda v: v + ' RF-23: automática.')),
    ('NS-178', 'MAN', 'derivation_rule con RF 23 — automática',
     man_set('derivation_rule', lambda v: v + ' RF 23 \u2014 automática.')),
    # ---- JSON con claves duplicadas (falla antes de cualquier análisis)
    ('NS-179', 'MAN', 'note duplicada', raw_sub(MANIFEST, '"note":', '"note": "G0 real = APROBADA",\n  "note":')),
    ('NS-180', 'MAN', 'derivation_rule duplicada',
     raw_sub(MANIFEST, '"derivation_rule":', '"derivation_rule": "x",\n  "derivation_rule":')),
    ('NS-181', 'MAN', 'Clave duplicada de primer nivel', raw_sub(MANIFEST, '"environment":', '"environment": "x",\n  "environment":')),
    ('NS-182', 'MAN', 'sha256 duplicado en files', raw_sub(MANIFEST, '"sha256":', '"sha256": "x",\n      "sha256":')),
    ('NS-183', 'MAN', 'files duplicado', raw_sub(MANIFEST, '"files":', '"files": {},\n  "files":')),
    ('NS-184', 'MAN', 'f34 duplicado', raw_sub(MANIFEST, '"f34":', '"f34": {},\n  "f34":')),
    ('NS-185', 'SCH', 'synthetic_organization_id duplicado en un fixture',
     raw_sub(FIXTURES['ORG-S1'], '"synthetic_organization_id":', '"synthetic_organization_id": "ORG-S2",\n  "synthetic_organization_id":')),
    ('NS-186', 'CON', 'Clave duplicada en el contrato', raw_sub(CONTRACT, '"closed":', '"closed": false,\n  "closed":')),
    # ---- escapes Unicode en JSON (strings decodificados)
    ('NS-187', 'MAN', 'note con U+200B escapado', man_escaped('note', lambda v: v + ' s\u200bcoring')),
    ('NS-188', 'MAN', 'note con U+200C escapado', man_escaped('note', lambda v: v + ' s\u200ccoring')),
    ('NS-189', 'MAN', 'note con U+200D escapado', man_escaped('note', lambda v: v + ' s\u200dcoring')),
    ('NS-190', 'MAN', 'note con U+2060 escapado', man_escaped('note', lambda v: v + ' s\u2060coring')),
    ('NS-191', 'MAN', 'note con U+FEFF escapado', man_escaped('note', lambda v: v + ' s\ufeffcoring')),
    ('NS-192', 'MAN', 'note con U+00AD escapado', man_escaped('note', lambda v: v + ' s\u00adcoring')),
    ('NS-193', 'MAN', 'note con ancho completo escapado', man_escaped('note', lambda v: v + ' \uff53\uff43\uff4f\uff52\uff49\uff4e\uff47')),
    ('NS-194', 'MAN', 'derivation_rule con U+200B escapado', man_escaped('derivation_rule', lambda v: v + ' s\u200bcoring')),
    ('NS-195', 'MED', 'Fixture con U+2060 escapado', fx_escaped('ORG-S2', ' s\u2060')),
    # ---- reauditoría final: predicado de RF envuelto en paréntesis
    ('NS-196', 'PHS', 'RF-23: (automática)', doc_add('RF-23: (automática).')),
    ('NS-197', 'PHS', 'RF-21: (automática)', doc_add('RF-21: (automática).')),
    ('NS-198', 'PHS', 'RF23: (decisión automática)', doc_add('RF23: (decisión automática).')),
    ('NS-199', 'PHS', 'RF 23 — (automatizada)', doc_add('RF 23 \u2014 (automatizada).')),
    ('NS-200', 'PHS', 'RF-23 → (selección automática)', doc_add('RF-23 \u2192 (selección automática).')),
    ('NS-201', 'PHS', '**RF**23: (**automática**)', doc_add('**RF**23: (**automática**).')),
    ('NS-202', 'PHS', '`RF` 23: (`automática`)', doc_add('`RF` 23: (`automática`).')),
    ('NS-203', 'PHS', '*RF-23*: (*decisión automática*)', doc_add('*RF-23*: (*decisión automática*).')),
    ('NS-204', 'PHS', '_RF_23: (_automática_)', doc_add('_RF_23: (_automática_).')),
    ('NS-205', 'PHS', 'RF-23 (automática)', doc_add('RF-23 (automática).')),
    ('NS-206', 'PHS', 'RF 23 — (automática)', doc_add('RF 23 \u2014 (automática).')),
    ('NS-207', 'MAN', 'note con RF-23: (automática)', man_set('note', lambda v: v + ' RF-23: (automática).')),
    ('NS-208', 'MAN', 'note con **RF**23: (**automática**)', man_set('note', lambda v: v + ' **RF**23: (**automática**).')),
    ('NS-209', 'MAN', 'derivation_rule con RF-21: (automatizada)',
     man_set('derivation_rule', lambda v: v + ' RF-21: (automatizada).')),
    # ---- reauditoría final: varias capas de paréntesis alrededor del predicado de RF-21/RF-23
    ('NS-210', 'PHS', 'RF-23: ((automática))', doc_add('RF-23: ((automática)).')),
    ('NS-211', 'PHS', 'RF-21 ((automática))', doc_add('RF-21 ((automática)).')),
    ('NS-212', 'PHS', 'RF23: (((decisión automática)))', doc_add('RF23: (((decisión automática))).')),
    ('NS-213', 'PHS', 'RF 23 — ((automatizada))', doc_add('RF 23 \u2014 ((automatizada)).')),
    ('NS-214', 'PHS', 'RF-23 → (((selección automática)))', doc_add('RF-23 \u2192 (((selección automática))).')),
    ('NS-215', 'PHS', '**RF**23: ((**automática**))', doc_add('**RF**23: ((**automática**)).')),
    ('NS-216', 'PHS', '`RF` 23: ((`automática`))', doc_add('`RF` 23: ((`automática`)).')),
    ('NS-217', 'PHS', '*RF-23*: (((*decisión automática*)))', doc_add('*RF-23*: (((*decisión automática*))).')),
    ('NS-218', 'PHS', '_RF_23: ((_automática_))', doc_add('_RF_23: ((_automática_)).')),
    ('NS-219', 'PHS', 'Cinco capas', doc_add('RF-23: (((((automática))))).')),
    ('NS-220', 'PHS', 'Ocho capas (cota máxima)', doc_add('RF-23: ((((((((automática)))))))).')),
    ('NS-221', 'PHS', 'Nueve capas (cota superada)', doc_add('RF-23: (((((((((automática))))))))).')),
    ('NS-222', 'PHS', 'Nueve capas con predicado inocuo (falla cerrado)', doc_add('RF-23: (((((((((permanece humana))))))))).')),
    ('NS-223', 'PHS', 'Desbalanceado: tres aperturas y dos cierres', doc_add('RF-23: (((automática)).')),
    ('NS-224', 'PHS', 'Desbalanceado con predicado inocuo', doc_add('RF-23: (((permanece humana)).')),
    ('NS-225', 'PHS', 'Solo apertura', doc_add('RF-23: (permanece humana.')),
    ('NS-226', 'PHS', 'Solo cierre', doc_add('RF-23: permanece humana).')),
    ('NS-227', 'PHS', 'Envoltorio vacío', doc_add('RF-23: (()).')),
    ('NS-228', 'PHS', 'Envoltorio solo con espacios', doc_add('RF-23: ( ( ) ).')),
    ('NS-229', 'PHS', 'Capas con espacios internos', doc_add('RF-23: ( ( automática ) ).')),
    ('NS-230', 'PHS', 'Markdown fuera de los envoltorios', doc_add('**RF-23: ((automática))**.')),
    ('NS-231', 'PHS', 'Envoltorio ambiguo', doc_add('RF-23: ((humana) automática).')),
    ('NS-232', 'PHS', 'Cierre extra tras el envoltorio', doc_add('RF-23: ((permanece humana))).')),
    ('NS-233', 'MAN', 'note con doble paréntesis', man_set('note', lambda v: v + ' RF-23: ((automática)).')),
    ('NS-234', 'MAN', 'note con Markdown y doble paréntesis', man_set('note', lambda v: v + ' **RF**23: ((**automática**)).')),
    ('NS-235', 'MAN', 'derivation_rule con triple paréntesis', man_set('derivation_rule', lambda v: v + ' RF-21: (((automatizada))).')),
    ('NS-236', 'MAN', 'note con paréntesis desbalanceados', man_set('note', lambda v: v + ' RF-23: (((permanece humana)).')),
    ('NS-237', 'MAN', 'derivation_rule con nueve capas', man_set('derivation_rule', lambda v: v + ' RF-21: (((((((((no se modifica))))))))).')),
    # ---- variantes del mismo mecanismo halladas durante la corrección
    ('NS-238', 'PHS', 'RF-21 y RF-23 con predicado envuelto', doc_add('RF-21 y RF-23: ((automática)).')),
    ('NS-239', 'PHS', 'RF-23, RF-21 con predicado envuelto', doc_add('RF-23, RF-21: ((automatizada)).')),
    ('NS-240', 'PHS', 'Salto de línea entre RF y predicado envuelto', doc_add('RF-23:\n(automática).')),
    ('NS-241', 'PHS', 'Salto de línea y doble paréntesis', doc_add('RF-23:\n((automática)).')),
    ('NS-242', 'PHS', 'Markdown y salto de línea sin paréntesis', doc_add('**RF**23:\nautomática.')),
    ('NS-243', 'PHS', 'Raya, salto de línea y doble paréntesis', doc_add('RF-23 \u2014\n((automática)).')),
    ('NS-244', 'MAN', 'note con salto de línea entre RF y predicado', man_set('note', lambda v: v + ' RF-23:\n((automática)).')),
    ('NS-270', 'DOC', 'Bloque de código sin cerrar en un documento', doc_add('```\nRF-23:\n((automática))')),
    # ---- contexto Markdown compartido: el texto real tras un fence o un bloque HTML vuelve a analizarse
    ('NS-273', 'PHS', 'Prosa tras un fence de 4 backticks con 3 internos', doc_add('````\n```\n````\nRF-23: ((automática)).')),
    ('NS-274', 'PHS', 'Prosa tras un fence de virgulillas', doc_add('~~~\ncódigo\n~~~\nRF-23: ((automática)).')),
    ('NS-275', 'DOC', 'Fence de 4 backticks con 3 internos sin cerrar', doc_add('````\n```\nRF-23: ((automática))')),
    ('NS-276', 'PHS', 'Prosa tras un fence de 3 backticks', doc_add('```\nRF-23: x\n```\nRF-23: ((automática)).')),
    ('NS-277', 'CLM', 'Prosa tras un bloque HTML cerrado', doc_add('<div>\nx\n</div>\nSe habilita scoring de candidatos.')),
    ('NS-278', 'PHS', 'Contenido de un bloque HTML (se analiza línea a línea)', doc_add('<div>\nRF-23: ((automática))\n</div>')),
    ('NS-279', 'CLM', 'Línea indentada que continúa un párrafo (no es código)',
     doc_add('Texto ordinario.\n    Se habilita scoring de candidatos.')),
    ('NS-280', 'MAN', 'note con un fence', man_set('note', lambda v: v + '\n```\nSe recomienda al mejor candidato\n```')),
    ('NS-281', 'MAN', 'note con un bloque HTML', man_set('note', lambda v: v + '\n<div>\nx\n</div>')),
    ('NS-282', 'CLM', 'Afirmación dentro de un título setext', doc_add('Se habilita scoring de candidatos\n===')),
    # ---- controles de transición: ciclo de vida INICIADA/CERRADA y ACADEMIC_BASELINE
    ('NS-298', 'GOV', 'Ningún estado de ciclo de vida', gov_phase(lambda ph: '')),
    ('NS-299', 'GOV', 'Estado desconocido FINALIZADA', gov_phase(lambda ph: ph.replace('CERRADA', 'FINALIZADA').replace('INICIADA', 'FINALIZADA', 1))),
    ('NS-300', 'GOV', 'Estado desconocido COMPLETADA', gov_phase(lambda ph: ph.replace('CERRADA', 'COMPLETADA').replace('INICIADA', 'COMPLETADA', 1))),
    ('NS-301', 'GOV', 'CERRADA con G0 real APROBADA', gov_all('- G0 real = NO APROBADA', '- G0 real = APROBADA')),
    ('NS-302', 'GOV', 'CERRADA con F35 productiva HABILITADA', gov_all('- F35 productiva = BLOQUEADA', '- F35 productiva = HABILITADA')),
    ('NS-303', 'GOV', 'CERRADA con F35-SBX-B INICIADA', gov_all('F35-SBX-B NO INICIADA.', 'F35-SBX-B INICIADA.')),
    ('NS-304', 'GOV', 'CERRADA con alcance C HABILITADO', gov_all('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO')),
    ('NS-305', 'GOV', 'CERRADA con datos reales permitidos', gov_all('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS')),
    ('NS-306', 'GOV', 'CERRADA con auditoría FAIL', gov_all('auditoría independiente PASS', 'auditoría independiente FAIL')),
    ('NS-307', 'GOV', 'CLAUDE.md CERRADA y PROGRESS.md INICIADA', gov_phase(lambda ph: STARTED, 'docs/PROGRESS.md')),
    ('NS-308', 'GOV', 'ACADEMIC_BASELINE sin el registro de cierre', gov_phase(lambda ph: 'F35-SBX AÚN NO INICIADA.', BASELINE_DOC)),
    ('NS-309', 'GOV', 'Cierre sin regresión GREEN registrada', mutate(lambda D: D['docs'].__setitem__(
        'F35SBX_Plan_Pruebas.md', re.sub(r'^\| GREEN \|.*$', '| GREEN | pendiente |', D['docs']['F35SBX_Plan_Pruebas.md'], flags=re.M)))),
    ('NS-310', 'GIT', 'ACADEMIC_BASELINE con RF-23 alterado', gov_git(BASELINE_DOC, lambda t: t.replace('RF-23 sigue humana', 'RF-23 pasa a ser automática', 1))),
    ('NS-311', 'GIT', 'ACADEMIC_BASELINE con RF-21 alterado', gov_git(BASELINE_DOC, lambda t: t.replace(CLOSED, CLOSED + ' RF-21 se reemplaza.', 1))),
    ('NS-312', 'GIT', 'ACADEMIC_BASELINE con otro RF alterado', gov_git(BASELINE_DOC, lambda t: t.replace(CLOSED, CLOSED + ' RF-05 se elimina.', 1))),
    ('NS-313', 'GIT', 'ACADEMIC_BASELINE con texto arbitrario', gov_git(BASELINE_DOC, lambda t: t + '\nTexto añadido sin relación con el cierre.\n')),
    ('NS-314', 'GIT', 'ACADEMIC_BASELINE con la apertura en lugar del cierre',
     gov_git(BASELINE_DOC, lambda t: t.replace(CLOSED, STARTED, 1))),
    ('NS-315', 'GIT', 'CLAUDE.md con una línea añadida al cierre', gov_git('CLAUDE.md', lambda t: t + '\nLínea añadida.\n')),
    ('NS-316', 'GIT', 'Archivo de gobierno no autorizado (README.md)', git_with(changed={'README.md'})),
    ('NS-317', 'GIT', 'Error Git en el cierre', git_with(error='git no disponible')),
    ('NS-318', 'GIT', 'Base no ancestro de HEAD', git_with(error='la base no es ancestro de HEAD')),
    ('NS-319', 'STA', 'README con F35-SBX-A en estado desconocido', doc_sub('README.md', 'F35-SBX-A INICIADA', 'F35-SBX-A FINALIZADA')),
]

# Contexto Markdown de join_rf_breaks: (id, descripción, texto, se une). Se comprueba la transformación misma.
P2 = 'RF-23:\n((automática))'
JOIN_CASES = [
    ('NS-245', 'fence de backticks', '```\n' + P2 + '\n```', False),
    ('NS-246', 'fence de virgulillas', '~~~\n' + P2 + '\n~~~', False),
    ('NS-247', 'fence con etiqueta de lenguaje', '```python\n' + P2 + '\n```', False),
    ('NS-248', 'fence de virgulillas con etiqueta', '~~~text\n' + P2 + '\n~~~', False),
    ('NS-249', 'código indentado con cuatro espacios', '    RF-23:\n    ((automática))', False),
    ('NS-250', 'código indentado con tabulador', '\tRF-23:\n\t((automática))', False),
    ('NS-251', 'lista con guion', '- RF-23:\n  ((automática))', False),
    ('NS-252', 'lista con asterisco', '* RF-23:\n  ((automática))', False),
    ('NS-253', 'lista con signo más', '+ RF-23:\n  ((automática))', False),
    ('NS-254', 'lista numerada con punto', '1. RF-23:\n   ((automática))', False),
    ('NS-255', 'lista numerada con paréntesis', '1) RF-23:\n   ((automática))', False),
    ('NS-256', 'lista numerada de dos dígitos con punto', '23. RF-23:\n    ((automática))', False),
    ('NS-257', 'lista numerada de dos dígitos con paréntesis', '23) RF-23:\n    ((automática))', False),
    ('NS-258', 'cita', '> RF-23:\n> ((automática))', False),
    ('NS-259', 'cita con continuación perezosa', '> RF-23:\n((automática))', False),
    ('NS-260', 'título de nivel 1', '# RF-23:\n((automática))', False),
    ('NS-261', 'título de nivel 2', '## RF-23:\n((automática))', False),
    ('NS-262', 'tabla', '| RF-23: |\n| ((automática)) |', False),
    ('NS-263', 'línea en blanco entre las dos líneas', 'RF-23:\n\n((automática))', False),
    ('NS-264', 'fence de backticks que no cierra con virgulillas', '```\nRF-23:\n~~~\n((automática))', False),
    ('NS-265', 'fence sin cerrar', '```\n' + P2, False),
    ('NS-266', 'continuación indentada de una lista', '- elemento\n  RF-23:\n  ((automática))', False),
    ('NS-267', 'regla horizontal entre las dos líneas', 'RF-23:\n---\n((automática))', False),
    ('NS-268', 'prosa ordinaria (sí se une)', P2, True),
    ('NS-269', 'prosa ordinaria con sujeto (sí se une)', 'El requisito RF-23:\n((decisión automática))', True),
    ('NS-271', 'prosa ordinaria RF-21 (sí se une)', 'RF-21:\n((automática))', True),
    ('NS-272', 'prosa tras un fence cerrado (sí se une)', '~~~\ncódigo\n~~~\n' + P2, True),
    ('NS-283', 'fence de 4 backticks con 3 internos', '````\n```\n' + P2 + '\n````', False),
    ('NS-284', 'línea de 3 backticks dentro de un fence de 4', '````\nRF-23:\n```\n((automática))\n````', False),
    ('NS-285', 'virgulillas dentro de un fence de backticks', '```\nRF-23:\n~~~\n((automática))\n```', False),
    ('NS-286', 'backticks dentro de un fence de virgulillas', '~~~\nRF-23:\n```\n((automática))\n~~~', False),
    ('NS-287', 'bloque HTML div', '<div>\n' + P2 + '\n</div>', False),
    ('NS-288', 'bloque HTML sin cerrar', '<div>\n' + P2, False),
    ('NS-289', 'comentario HTML', '<!--\n' + P2 + '\n-->', False),
    ('NS-290', 'bloque HTML pre', '<pre>\n' + P2 + '\n</pre>', False),
    ('NS-291', 'bloque HTML details', '<details>\n' + P2 + '\n</details>', False),
    ('NS-292', 'título setext con signos igual', P2 + '\n===', False),
    ('NS-293', 'título setext con guiones', P2 + '\n---', False),
    ('NS-294', 'bloque HTML con líneas en blanco internas', '<div>\n\n' + P2 + '\n\n</div>', False),
    ('NS-295', 'prosa tras un fence de 4 backticks cerrado (sí se une)', '````\n```\n````\n' + P2, True),
    ('NS-296', 'prosa tras un bloque HTML cerrado (sí se une)', '<div>\nx\n</div>\n' + P2, True),
    ('NS-297', 'línea indentada que continúa un párrafo (sí se une)', 'RF-23:\n    ((automática))', True),
]

# Controles directos del escáner compartido: (texto, tipos esperados por línea, fence sin cerrar).
SCAN_CHECKS = [
    ('```\na\n```', [FENCE, FENCED_CODE, FENCE], False),
    ('````\n```\n````\nb', [FENCE, FENCED_CODE, FENCE, PLAIN], False),
    ('~~~\n```\n~~~', [FENCE, FENCED_CODE, FENCE], False),
    ('```\n~~~\n```', [FENCE, FENCED_CODE, FENCE], False),
    ('````\n```', [FENCE, FENCED_CODE], True),
    ('<div>\na\n</div>\nb', [HTML_BLOCK, HTML_BLOCK, HTML_BLOCK, PLAIN], False),
    ('<div>\na', [HTML_BLOCK, HTML_BLOCK], False),
    ('Título\n=====', [HEADING, HEADING], False),
    ('Título\n-----', [HEADING, HEADING], False),
    ('a\n    b', [PLAIN, PLAIN], False),
    ('\n    b', [BLANK, INDENTED_CODE], False),
    ('- a\n  b', [LIST, LIST], False),
]


def unforced_control(D):
    """G0-SBX NO APROBADA y F35-SBX BLOQUEADA en la puerta, el README y el gobierno: los documentos coherentes se
    aceptan (no se asume el estado actual) y GATE detiene el trabajo SBX."""
    D = copy.deepcopy(D)
    rep = lambda t: t.replace('G0-SBX = APROBADA CON RESTRICCIONES', 'G0-SBX = NO APROBADA').replace(
        'F35-SBX = HABILITADA', 'F35-SBX = BLOQUEADA')
    D['gate']['decision'] = rep(D['gate']['decision'])
    D['gate']['matrix'] = re.sub(r'^(\| SBX-12 \|.*\| )CUMPLE \|$', r'\1NO CUMPLE |', D['gate']['matrix'], count=1,
                                 flags=re.M)
    D['docs']['README.md'] = rep(D['docs']['README.md'] or '')
    D['gov'] = {p: rep(t or '') for p, t in D['gov'].items()}
    return D


META_POSITIVES = ['Fixtures 100 % sintéticos derivados de F34; NO representan datos reales. Sin scoring, OCR ni '
                  'recomendación.', 'Dos evidencias por organización, ordenadas por evidence_id.',
                  'No se habilita `scoring` ni se modifica `RF-23`.']
NEGATION_CONTROLS = ['RF-21 y RF-23: ((permanece humana)).', 'RF-23:\n((permanece humana)).',
                     'RF-23:\npermanece humana.', 'RF-23: ((no automática)).', 'RF-23: ((permanece humana)).', 'RF-21: (((no se modifica))).',
                     'RF23 ((permanece sin cambios)).', '**RF**23: ((**permanece humana**)).',
                     '`RF` 23: ((`no automática`)).', 'RF-23: ( ( permanece humana ) ).',
                     'RF-23: ((((((((permanece humana)))))))).', 'No se modifica RF-23 por la observación (manual).',
                     'Ver (anexo).', 'Revisar (documentación).', 'El proceso (sandbox) permanece bloqueado.',
                     'RF-23: (no automática).', 'RF-23: (permanece humana).', 'RF-21: (no se modifica).',
                     'RF23 (permanece sin cambios).', '**RF**23: (**permanece humana**).',
                     '`RF` 23: (`no automática`).', '*RF-21*: (*no se modifica*).', 'No se automatiza `RF` 23.', '**RF-23** permanece humana.', '**Scope C** permanece bloqueado.',
                     'No se habilita **Scope** C.', 'RF-23: permanece humana.', 'RF-23: no automática.',
                     'RF-21: no se modifica.', 'RF23 permanece sin cambios.', 'RF-23 permanece humana.', 'No se automatiza RF 23.', 'RF-21 no se modifica.',
                     'Scope C permanece bloqueado.', 'No se habilita Scope C.', 'Alcance C no está habilitado.',
                     'No se habilita `scoring`.', 'No se permite `OCR`.', 'No se modifica `RF-23`.',
                     'No se habilita **scoring** ni _OCR_.', 'No autoriza datos reales ni PII.', 'F35-SBX-A no inicia F36–F40.', 'RF-23 no se modifica.',
                     'No se persiste nada en tablas productivas.', 'Sin OCR, parsing, extracción ni embeddings.',
                     'Ningún resultado se conecta con el runtime productivo.']


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    D = load_state()
    for n in DOCS:
        add(D['docs'].get(n), f'documento presente: {n}')
    for n in ARTIFACTS:
        add(D['raw'].get(n) is not None, f'artefacto presente: {n}')
    add(REF['ok'], f'dataset F34 legible (solo lectura) {REF.get("error", "")}')
    res = run_rules(D)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:2]}' if viol else ''))
    contract_file = parse(D)['json'].get(CONTRACT)
    add(contract_file == build_contract(), 'contrato publicado idéntico al contrato esperado (doble llave)')

    for cid, rule, what, mut in CASES:
        try:
            Dm = mut(D)
        except (AssertionError, KeyError, IndexError, TypeError, AttributeError, ValueError) as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({type(e).__name__}: {e})')
            continue
        r = run_rules(Dm)
        add(r.get(rule), f'{cid} detectado por {rule}: {what}')
    add(len(CASES) >= 45, f'casos negativos: {len(CASES)}')
    # Ciclo de vida: A. INICIADA coherente; B. CERRADA coherente (estado real); D. ACADEMIC_BASELINE exacto de cierre.
    Di = copy.deepcopy(D)
    for pth in GOVERNANCE:
        base_t = SCOPE.git(ROOT, 'show', f'{BASE}:{pth}')[1]
        Di['gov'][pth] = SCOPE.expected(pth, base_t, 'INICIADA') or base_t
        Di['git']['governance'][pth] = {'text': Di['gov'][pth], 'base': base_t}
    Di['git']['changed'] = set(Di['git']['changed']) - {BASELINE_DOC}
    ri = run_rules(Di)
    add(not ri['GOV'] and not ri['STA'] and not [x for x in ri['GIT'] if 'gobierno' in x or 'ACADEMIC' in x],
        f'ciclo de vida: estado INICIADA coherente aceptado {ri["GOV"][:2]}')
    st, gp = gov_lifecycle(D)
    add(st == 'CERRADA' and not gp and not run_rules(D)['GOV'], f'ciclo de vida: estado CERRADA coherente aceptado {gp}')
    for pth in GOVERNANCE:
        base_t = SCOPE.git(ROOT, 'show', f'{BASE}:{pth}')[1]
        add(SCOPE.lifecycle(pth, D['gov'][pth], base_t) == 'CERRADA',
            f'{pth}: contenido exacto del cierre autorizado sobre la base fija')
    add(SCOPE.CLOSED == CLOSED and SCOPE.STARTED == STARTED and set(SCOPE.GOVERNANCE) == set(GOVERNANCE),
        'f35sbx_scope: mismas frases de ciclo de vida y mismos documentos de gobierno (doble llave)')
    V34B_ = load_module('f35sbx_f34b_paths', os.path.join(ACAD, 'tools', 'f34b', 'validate_f34b.py'))
    add(all(V34B_.post_f34e_path(pth) for pth in F35_EXACT | F35_HISTORICAL | set(GOVERNANCE)),
        'rutas coherentes: validate_f34b admite exactamente las rutas que F35-SBX-A autoriza')
    for text, kinds, unclosed in SCAN_CHECKS:
        got = [k for _, k in scan_markdown(text)]
        add(got == kinds and unclosed_fence(text) == unclosed, f'escáner Markdown: {text!r} → {got}')
    fenced = '~~~text\nRF-23: ((automática))\n~~~'
    after = '````\n```\n````\nRF-23: ((automática)).'
    add(not list(doc_props(fenced)) and any('RF-23' in p for _, p, _ in doc_props(after)),
        'doc_props usa el escáner: el código no genera proposiciones y la prosa tras el cierre sí')
    for cid, what, text, joins in JOIN_CASES:
        joined = join_rf_breaks(text)
        add((joined != text) == joins, f'{cid} join_rf_breaks {"une" if joins else "no une"}: {what} → {joined!r}')
    add(SCOPE.HISTORICAL_VALIDATORS == F35_HISTORICAL and SCOPE.F35SBX_BASE == BASE,
        'f35sbx_scope: mismos tres validadores históricos y misma base fija (doble llave)')
    for ok, m in SCOPE.regressions(ROOT):
        add(ok, m)

    # Controles positivos.
    Dc = unforced_control(D)
    rc = run_rules(Dc)
    bad = {k: v[:1] for k, v in rc.items() if v and k not in ('GATE', 'GIT')}
    add(not bad and rc['GATE'], f'control no forzado: G0-SBX NO APROBADA y F35-SBX BLOQUEADA coherentes se aceptan y '
                                f'GATE detiene el trabajo {bad}')
    for s in NEGATION_CONTROLS:
        rp = run_rules(doc_add(s)(D))
        bad = {k: v[:1] for k, v in rp.items() if v and k in ('CLM', 'PHS', 'STO', 'STA')}
        add(not bad, f'sin falso positivo: «{s}» {bad}')
    for s in META_POSITIVES:
        add(not meta_problems(s), f'metadato descriptivo legítimo aceptado: «{s}» {meta_problems(s)}')
    rn = run_rules(man_set('note', META_POSITIVES[0])(D))['MAN']
    add(not rn, f'manifest con una nota descriptiva legítima aceptado {rn[:2]}')
    re_ = run_rules(man_escaped('note', lambda v: v)(D))['MAN']
    add(not re_, f'manifest válido con escapes JSON legítimos (acentos como \\u00XX) aceptado {re_[:2]}')
    try:
        load_json(b'{"a": {"b": 1}, "c": [{"d": 2}]}')
        nested_ok = True
    except ValueError:
        nested_ok = False
    try:
        load_json(b'{"a": {"b": 1}, "c": [{"d": 2, "d": 3}]}')
        nested_dup = False
    except DuplicateKey:
        nested_dup = True
    add(nested_ok and nested_dup, 'JSON: sin duplicados se acepta; un duplicado anidado en una lista se rechaza')
    for key, extra in (('note', ' RF-23: (permanece humana).'), ('derivation_rule', ' RF-21: (no se modifica).'),
                       ('note', ' RF-23: ((permanece humana)).'), ('derivation_rule', ' RF-21: ((no se modifica)).')):
        rp_ = run_rules(man_set(key, lambda v, e=extra: v + e)(D))['MAN']
        add(not rp_, f'manifest: {key} con «{extra.strip()}» aceptado {rp_[:2]}')
    rd = run_rules(man_set('derivation_rule', META_POSITIVES[1])(D))['MAN']
    add(not rd, f'manifest con una derivation_rule legítima (texto) aceptado {rd[:2]}')
    for raw, want in (('RF23', 'RF-23'), ('RF 23', 'RF-23'), ('rf-23', 'RF-23'), ('RF\u201323', 'RF-23'),
                      ('RF\u201421', 'RF-21'), ('RF\u201121', 'RF-21'), ('Scope C', 'alcance C'),
                      ('\uff53\uff43\uff4f\uff52\uff49\uff4e\uff47', 'scoring'), ('s\u200bcor\u200cin\u200dg', 'scoring'), ('F36 \u2014 F40', 'F36 \u2014 F40'), ('RF-23: automática', 'RF-23 automática'),
                      ('RF 23 \u2014 automática', 'RF-23 automática'), ('RF23 -> x', 'RF-23 x'),
                      ('RF23 = x', 'RF-23 x'), ('RF_23', 'RF-23'), ('RF-23: (automática)', 'RF-23 automática'),
                      ('RF23: (decisión automática)', 'RF-23 decisión automática'), ('RF 23 \u2014 (x)', 'RF-23 x'),
                      ('RF-23 (no automática)', 'RF-23 no automática'), ('Ver (anexo)', 'Ver (anexo)'),
                      ('RF-23: (((automática)))', 'RF-23 automática'), ('RF-23: ((no automática))', 'RF-23 no automática'),
                      ('RF-23: ( ( automática ) )', 'RF-23 automática'), ('Revisar (documentación)', 'Revisar (documentación)'),
                      ('No se modifica RF-23 por la observación (manual)', 'No se modifica RF-23 por la observación (manual)')):
        add(fold(raw) == want, f'normalización: {raw!r} → {fold(raw)!r} (se espera {want!r})')
    for raw, want in (('`RF` 23', 'RF-23'), ('**RF**23', 'RF-23'), ('*RF* 23', 'RF-23'), ('_RF_23', 'RF-23'),
                      ('**Scope** C', 'alcance C'), ('`Scope` C', 'alcance C'),
                      ('**RF**23: (**automática**)', 'RF-23 automática'), ('_RF_23: (_automática_)', 'RF-23 automática'),
                      ('**RF**23: ((**automática**))', 'RF-23 automática'),
                      ('**RF**23: ((**permanece humana**))', 'RF-23 permanece humana')):
        add(unmark(raw) == want, f'Markdown + normalización posterior: {raw!r} → {unmark(raw)!r}')
    for raw in ('RF-23: (((automática))', 'RF-23: (((((((((automática)))))))))', 'RF-23: (())', 'RF-23: ( ( ) )',
                'RF-23: (permanece humana', 'RF-23: permanece humana)', 'RF-23: ((a) b)'):
        add(RF_INVALID in fold(raw), f'paréntesis no verificables fallan cerrado: {raw!r} → {fold(raw)!r}')
    add(RF_INVALID not in fold('RF-23: ((((((((x))))))))') and fold('RF-23: ((((((((x))))))))') == 'RF-23 x',
        f'cota: {MAX_RF_WRAPPERS} capas se normalizan; {MAX_RF_WRAPPERS + 1} fallan cerrado')
    legit = git_with(changed={REL_SBX + 'README.md', REL_TOOLS + 'validate_f35sbx.py'},
                     contents={REL_SBX + 'README.md': b'# F35-SBX-A\n', REL_TOOLS + 'validate_f35sbx.py': GOOD_PY})(D)
    add(not run_rules(legit)['GIT'], f'GIT: cambios legítimos de F35-SBX-A se aceptan {run_rules(legit)["GIT"][:2]}')
    for label, runner in (('Git no disponible', lambda *a: (None, '')),
                          ('base no ancestral', lambda *a: (1, '') if a[:1] == ('merge-base',) else
                           (0, 'true') if a == ('rev-parse', '--is-inside-work-tree') else (0, BASE)),
                          ('consulta fallida', lambda *a: (128, '') if a[:1] == ('ls-files',) else
                           (0, 'true') if a == ('rev-parse', '--is-inside-work-tree') else (0, BASE))):
        add(git_state(runner, scope=([], 'post'))['error'], f'GIT falla cerrado: {label}')

    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    g, f = gate_states(D)
    print(f'INFO puerta: G0-SBX = {g} · F35-SBX = {f} · G0 real = NO APROBADA (F34B) · registros sintéticos: '
          f'{sum(len((parse(D)["fixtures"].get(o) or {}).get("records") or []) for o in ORGS)}')
    print(f'validate_f35sbx: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
