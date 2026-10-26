#!/usr/bin/env python3
"""Validador fail-closed del paquete F36-SBX (autorización, investigación y diseño), versión 2.

Solo biblioteca estándar. No ejecuta ML ni NLP, no usa red y no escribe archivos.

- Recalcula el F36-SBX-GATE y exige que coincida con el declarado.
- Valida la semántica de la evidencia de equipo (FG-02, FG-03, FG-10 y FG-12) y su vínculo con el commit
  candidato auditado; la existencia de un archivo no basta.
- Valida el contrato de evidencia cerrado (v2) y, con él, el ejemplo de conformidad: estructura, provenance,
  relaciones entre objetos y particiones (REL-01..REL-12).

Uso: python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py
"""
import ast
import csv
import datetime
import hashlib
import io
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

BASE = 'b8892af39a6492d8dd44a36290604efc602380cd'
BRANCHES = frozenset({'feature/f36-sbx-authorization-design', 'develop', 'main'})
PKG = 'docs/academico/f36-sbx'
TOOLS = 'docs/academico/tools/f36sbx'
GATE_EVIDENCE = PKG + '/gate/evidencia/'
CHARTER = PKG + '/F36SBX_Charter.md'
MATRIX = PKG + '/F36SBX_Matriz_Capacidades.md'
THREATS = PKG + '/F36SBX_Threat_Model.md'
PLAN = PKG + '/F36SBX_Plan_Evaluacion.md'
GATE_DOC = PKG + '/F36SBX_Gate_Sucesor.md'
CONTRACT = PKG + '/contrato/f36sbx_evidence_contract.json'
EXAMPLE = PKG + '/contrato/f36sbx_contract_example.json'
GATE_STATE = PKG + '/gate/f36sbx_gate_state.json'
TEAM_SCHEMA = PKG + '/gate/f36sbx_team_evidence_schema.json'
F33_MATRIX = 'docs/academico/diseno-inteligente/F33_Matriz_Capacidades_y_Restricciones.md'
PKG_DOCS = ['README.md', 'F36SBX_Charter.md', 'F36SBX_Matriz_Capacidades.md', 'F36SBX_Investigacion_Diseno.md',
            'F36SBX_Contrato_Evidencia.md', 'F36SBX_Threat_Model.md', 'F36SBX_Plan_Evaluacion.md',
            'F36SBX_Gate_Sucesor.md', 'F36SBX_Trazabilidad.md', 'F36SBX_Correccion_AF1.md']
PKG_DATA = [CONTRACT, EXAMPLE, GATE_STATE, TEAM_SCHEMA]
PKG_FILES = [f'{PKG}/{n}' for n in PKG_DOCS] + PKG_DATA
GOV_FILES = ['CLAUDE.md', 'README.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md']
F34 = 'docs/academico/datos-sinteticos/dataset/'
UPSTREAM_FILES = [F34 + 'applications.csv', F34 + 'criteria.csv', F34 + 'vacancies.csv', F34 + 'manifest.json']

# Integridad de los artefactos cerrados: SHA-256 de su JSON canónico. Cambiarlos exige un incremento auditado.
CONTRACT_SHA256 = 'b68cf631dce7a7141a2dc708273adfd07ae71e0c14dca869ce833b765adb754a'
TEAM_SCHEMA_SHA256 = 'b87b1cc9e8e4820cc432abf05d7370075b1b49b52a10f3d0092ac5269a510c5e'

# Estado vigente de los cuatro documentos de gobierno: exactamente estas líneas, una vez cada una.
REQUIRED_STATE = ['G0 real = NO APROBADA', 'G0-09 = CUMPLIDO', 'G0-14 = CUMPLIDO', 'G0-02 = PENDIENTE EXTERNO',
                  'G0-03 = PENDIENTE EXTERNO', 'G0-12 = PENDIENTE EXTERNO', 'ADR-005 = PROPUESTA',
                  'G0-SBX = APROBADA CON RESTRICCIONES', 'F35 productiva = BLOQUEADA',
                  'F35-SBX = CERRADA Y CONGELADA', 'F36-SBX = EN DISEÑO', 'F36-SBX-GATE = NO SUPERADO',
                  'F37-SBX = BLOQUEADA', 'F36–F40 = BLOQUEADAS', 'Alcance C = BLOQUEADO', 'Datos reales = PROHIBIDOS']
MEMBERS = ('Coronacion Meza Fredy', 'Peña Arroyo Anthony', 'Vila Meza Luis Antonio')
CLAUDE_MEMBERS = 'Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio.'

# Afirmaciones de estado que nunca pueden aparecer en el paquete ni en el gobierno.
FORBIDDEN_CLAIMS = [
    (r'\bG0 real\s*=\s*APROBADA', 'G0 real aprobada'),
    (r'\bG0\s*=\s*APROBADA', 'G0 aprobada sin sufijo'),
    (r'ADR-005(?: canónico)?\s*=\s*APROBAD', 'ADR-005 aprobado'),
    (r'(?i)alcance C\s*=\s*+(?!BLOQUEADO)', 'alcance C no bloqueado'),
    (r'(?i)datos reales\s*=\s*+(?!PROHIBIDOS)', 'datos reales no prohibidos'),
    (r'(?i)F37-SBX(?:-[A-Z])? (?:queda|está|esta) (?:habilitada|autorizada|iniciada)', 'F37-SBX habilitada'),
    (r'(?i)RF-23\s*(?:=|es)\s*autom', 'RF-23 automática'),
]
# Afirmaciones «sujeto = ESTADO» o «sujeto: ESTADO» sobre fases, puertas, ADR, alcance y datos.
CLAIM_RX = re.compile(r'(?<![\w-])(?P<subj>G0(?: real|-SBX|-\d{2})?|ADR-\d{3}(?: canónico)?'
                      r'|F\d{2}(?:-F\d{2})?(?:-SBX(?:-[A-Z0-9]+)*)?(?: productivas?)?'
                      r'|[Aa]lcance [A-Z](?: [a-záéíóúñ]+)*|[Dd]atos reales)'
                      r'\s*(?P<sep>[:=])\s*(?P<state>[A-ZÁÉÍÓÚÑ]{2}[A-ZÁÉÍÓÚÑ ]*)')
ID_CLAIM_RX = re.compile(r'(?<![\w-])(?P<subj>EI-\d{2}|RF-\d{2})\s*(?P<sep>=)\s*(?P<state>[A-ZÁÉÍÓÚÑ]{2}[A-ZÁÉÍÓÚÑ ]*)')
# Con «:» solo cuenta como afirmación si el estado empieza por una palabra de estado; con «=», siempre.
STATE_WORDS = {'ABIERTA', 'ABIERTO', 'ACTIVA', 'ACTIVO', 'APROBADA', 'APROBADO', 'AUTORIZADA', 'AUTORIZADO',
               'BLOQUEADA', 'BLOQUEADAS', 'BLOQUEADO', 'BLOQUEADOS', 'CERRADA', 'CERRADO', 'CONGELADA', 'CUMPLIDO',
               'DESBLOQUEADA', 'DESBLOQUEADO', 'EJECUTADA', 'EN', 'HABILITADA', 'HABILITADAS', 'HABILITADO',
               'IMPLEMENTADA', 'INICIADA', 'INICIADO', 'INTEGRADA', 'LISTA', 'NO', 'PENDIENTE', 'PERMITIDO',
               'PERMITIDOS', 'PROHIBIDOS', 'PROPUESTA', 'PROPUESTO', 'REVOCADA', 'REVOCADO', 'SUPERADA', 'SUPERADO',
               'VIGENTE'}
# Tabla «Estados de gobierno que el charter preserva»: el valor de cada fila empieza por su estado.
CHARTER_STATES = {'G0 real': 'NO APROBADA', 'G0-02, G0-03 y G0-12': 'PENDIENTE EXTERNO',
                  'G0-09 y G0-14': 'CUMPLIDO', 'G0-SBX': 'APROBADA CON RESTRICCIONES', 'ADR-005': 'PROPUESTA',
                  'F35 productiva': 'BLOQUEADA', 'F35-SBX': 'CERRADA Y CONGELADA',
                  'F36-F40 productivas': 'BLOQUEADAS', 'Alcance C': 'BLOQUEADO', 'Datos reales': 'PROHIBIDOS',
                  'RF-23': 'Decisión final humana', 'RF-29': 'Experimental', 'GC-AF-L01': 'LOW, ABIERTO / DIFERIDO'}

# Matriz fijada: clase y alcance de cada EI. Reclasificar exige un incremento auditado.
EXPECTED_MATRIX = {
    'EI-01': ('ALLOWED', 'B'), 'EI-02': ('ALLOWED', 'B'), 'EI-03': ('ALLOWED', 'B'), 'EI-04': ('ALLOWED', 'B'),
    'EI-05': ('ALLOWED', 'B'), 'EI-06': ('ALLOWED', 'B'), 'EI-07': ('ALLOWED', 'B'),
    'EI-08': ('CONDITIONAL', 'C'), 'EI-09': ('CONDITIONAL', 'B'), 'EI-10': ('CONDITIONAL', 'C'),
    'EI-11': ('CONDITIONAL', 'C'), 'EI-12': ('CONDITIONAL', 'C'), 'EI-24': ('CONDITIONAL', 'C'),
    'EI-13': ('BLOCKED', '—'), 'EI-14': ('BLOCKED', '—'), 'EI-15': ('BLOCKED', 'C'), 'EI-16': ('BLOCKED', '—'),
    'EI-17': ('BLOCKED', '—'), 'EI-18': ('BLOCKED', '—'), 'EI-19': ('BLOCKED', '—'), 'EI-20': ('BLOCKED', '—'),
    'EI-21': ('BLOCKED', '—'), 'EI-22': ('BLOCKED', '—'), 'EI-23': ('BLOCKED', '—'),
}
EXPECTED_CLASSES = {ei: cls for ei, (cls, _) in EXPECTED_MATRIX.items()}
SCOPE_C_CONDITIONAL = sorted(ei for ei, (cls, sc) in EXPECTED_MATRIX.items() if cls == 'CONDITIONAL' and sc == 'C')
EI_IDS = [f'EI-{i:02d}' for i in range(1, 25)]
CLASSES = ('ALLOWED', 'CONDITIONAL', 'BLOCKED')
# Temas que deben quedar en una fila BLOCKED de la matriz (columna de capacidad).
MUST_BLOCK = ['resumen', 'veredicto', 'ocr', 'llm sobre evidencia', 'llm para generar', 'entre candidatos',
              'scoring', 'ranking', 'recomendación', 'selección automática', 'emociones', 'personalidad',
              'honestidad', 'inteligencia', 'estrés', 'nerviosismo', 'biometría', 'rostro', 'voz', 'prosodia',
              'acento', 'audio', 'ajuste fino', 'datos reales', 'endpoints', 'migraciones']
# Términos que una capacidad ALLOWED no puede nombrar: son del alcance C o están bloqueados.
NOT_ALLOWED_WORDS = [r'embedding', r'sem[aá]ntic', r'\bocr\b', r'\bllm', r'\bpdf\b', r'\bdocx\b', r'\bner\b',
                     r'extracci', r'transformer', r'whisper', r'\bstt\b', r'\baudio\b']

TEI_IDS = [f'TEI-{i:02d}' for i in range(1, 23)]
THREAT_TOPICS = ['injection', 'malicioso', 'envenenamiento', 'fuga criterio', 'organizaciones', 'pii',
                 'alucinación', 'sin respaldo', 'automatización', 'ranking encubierto', 'inferencias prohibidas',
                 'procedencia', 'deriva de modelo', 'reproducibilidad', 'dependencia externa',
                 'cadena de suministro', 'agotamiento', 'adversarial', 'abstención', 'contaminación']
M_IDS = [f'M-{i:02d}' for i in range(1, 14)]
R_IDS = [f'R-{i:02d}' for i in range(1, 6)]

# Invariantes del contrato v2 que se comprueban además de su hash.
CONTRACT_KEYS = ['contract_id', 'contract_version', 'status', 'environment', 'source_type_allowed', 'generator_policy',
                 'allowed_upstream_sources', 'upstream_files', 'upstream_manifest', 'upstream_ref_bindings',
                 'content_upstream_bindings', 'forbidden_upstream_sources', 'synthetic_markers', 'identifier_patterns',
                 'enums', 'content_field_types', 'artifact_envelope_fields', 'artifact_types', 'fragment_fields',
                 'output_fields', 'output_ei', 'context_fields', 'provenance_fields', 'example_fields',
                 'partition_manifest_fields', 'partition_fields', 'threshold_fields', 'hashing', 'relations',
                 'group_marker_only_in', 'forbidden_fields', 'forbidden_field_tokens', 'splits']
ALLOWED_UPSTREAM = {'docs/academico/datos-sinteticos/dataset', 'docs/academico/evidencia-sbx/fixtures'}
REQUIRED_FORBIDDEN_SOURCES = {'docs/academico/g0-evidence', 'storage', 'database', 'http://', 'https://'}
MARKERS = {'synthetic_id_prefix': 'SBX36-', 'text_prefix': '[SINTÉTICO]', 'source_type': 'synthetic',
           'environment': 'sandbox', 'hash_algorithm': 'f36sbx-content-sha256-v1',
           'synthetic_organization_ids': ['ORG-S1', 'ORG-S2', 'ORG-S3']}
ARTIFACT_TYPES = {'cv_document': 'A', 'certificate': 'A', 'interview_transcript': 'A', 'human_observation': 'A',
                  'relevance_annotation': 'A', 'adversarial_case': 'A', 'counterfactual_pair': 'B',
                  'rendered_document': 'B'}
ENVELOPE = ['synthetic_id', 'artifact_type', 'stage', 'synthetic_organization_id', 'scenario_id', 'vacancy_token',
            'application_token', 'partition', 'template_family', 'source_type', 'environment', 'hash_algorithm',
            'content', 'content_hash', 'provenance']
CONTEXT = ['synthetic_organization_id', 'scenario_id', 'vacancy_token', 'application_token', 'partition']
FRAGMENT_FIELDS = ['fragment_id', 'artifact_id', *CONTEXT, 'text_path', 'char_start', 'char_end', 'fragment_hash']
OUTPUT_FIELDS = ['output_id', 'ei', 'method_id', 'method_version', *CONTEXT, 'query_criterion_id', 'fragment_refs',
                 'abstained', 'input_manifest_hash', 'output_hash']
PROVENANCE = ['generator_id', 'generator_version', 'template_id', 'template_family', 'seed', 'upstream_refs',
              'content_hash']
EXPECTED_SPLITS = {'partitions': ['dev', 'test'], 'forbidden_partitions': ['train'], 'train_allowed': False,
                   'group_by': ['template_family', 'vacancy_token'], 'test_sealed_before_any_run': True,
                   'seal_algorithm': 'f36sbx-test-seal-sha256-v1', 'thresholds_fit_on': 'dev',
                   'test_used_for_tuning': False, 'temporal_embargo': 'process_splits_f34',
                   'counterfactual_pairs_same_partition': True}
REQUIRED_FORBIDDEN_FIELDS = {'name', 'dni', 'email', 'phone', 'address', 'photo', 'age', 'gender', 'score', 'rank',
                             'recommendation', 'suitability', 'suggested_level', 'emotion', 'personality',
                             'honesty', 'intelligence', 'stress', 'nervousness', 'voice', 'face', 'prosody',
                             'accent', 'audio', 'video', 'biometric'}
REQUIRED_FORBIDDEN_TOKENS = {'name', 'dni', 'email', 'phone', 'gender', 'score', 'rank', 'recommendation', 'fit',
                             'verdict', 'emotion', 'personality', 'honesty', 'intelligence', 'stress',
                             'nervousness', 'voice', 'face', 'biometric', 'level', 'hire', 'select', 'discard'}
REL_IDS = [f'REL-{i:02d}' for i in range(1, 13)]

FG_IDS = [f'FG-{i:02d}' for i in range(1, 15)]
FG_TEAM = ('FG-02', 'FG-03', 'FG-10', 'FG-12')
FG_NA_ALLOWED = frozenset({'FG-12'})
AUTO_STATUSES = frozenset({'CUMPLE', 'NO CUMPLE'})
TEAM_STATUSES = frozenset({'CUMPLE', 'PENDIENTE', 'NO CUMPLE'})
STATUSES = AUTO_STATUSES | TEAM_STATUSES | {'NO APLICA'}
GATE_KEYS = {'gate_id', 'gate_version', 'authorizes', 'cannot_authorize', 'base_commit', 'candidate_commit',
             'team_evidence_schema', 'criteria', 'f37_authorized_ei', 'revocation', 'declared_result'}
CANNOT_AUTHORIZE = {'produccion', 'datos_reales', 'pii_real', 'audio_video_real', 'seleccion_automatica',
                    'scoring_ranking_recomendacion', 'cambio_rf23_rf21_rf29', 'g0_real', 'alcance_c_producto',
                    'endpoints_migraciones_ui', 'ei_blocked'}
PLACEHOLDERS = {'auditor', 'auditora', 'independiente', 'auditor independiente', 'auditoría independiente',
                'auditoria independiente', 'n/a', 'na', 'tbd', 'pendiente', 'desconocido', 'anónimo', 'anonimo',
                'none', 'null', 'x', '-', '?'}
HEX40 = re.compile(r'[0-9a-f]{40}')
HEX64 = re.compile(r'[0-9a-f]{64}')
INDEX = re.compile(r'0|[1-9][0-9]*')

STDLIB = frozenset({'ast', 'copy', 'csv', 'datetime', 'hashlib', 'importlib', 'io', 'json', 'os', 're', 'subprocess',
                    'sys', 'unicodedata', 'pathlib', 'unittest', 'tempfile'})
LOCAL_MODULES = frozenset({'validate_f36sbx'})
ML_IMPORT = re.compile(r'^\s*(?:import|from)\s+(torch|transformers|sentence_transformers|spacy|sklearn|pypdf|'
                       r'pdfplumber|docx|pytesseract|ollama|openai|anthropic|faiss|chromadb|whisper|numpy|'
                       r'pandas|requests|urllib3|httpx)\b', re.M)
PII_PATTERNS = [(re.compile(r'[\w.+-]+@[\w-]+\.[A-Za-z]{2,}'), 'correo'),
                (re.compile(r'(?<![\w])9\d{8}(?![\w])'), 'teléfono'),
                (re.compile(r'(?<![\w])\d{8}(?![\w])'), 'DNI')]
RUNTIME_PREFIXES = ('app/', 'routes/', 'config/', 'database/', 'resources/', 'ml-service/', 'bootstrap/',
                    'public/', 'tests/', 'docker/', '.github/', 'cypress/')
DEPENDENCY_FILES = frozenset({'composer.json', 'composer.lock', 'package.json', 'package-lock.json',
                              'ml-service/pyproject.toml', 'docker-compose.yml', 'Dockerfile'})
F35_FROZEN = ('docs/academico/evidencia-sbx', 'docs/academico/g0-', 'docs/academico/tools/f35sbx',
              'docs/academico/datos-sinteticos/', 'docs/academico/diseno-inteligente/',
              'docs/academico/investigacion-ia/', 'docs/academico/TECHNICAL_DEBT.md')


# ---------------------------------------------------------------- utilidades

def norm(text):
    """NFKC y guiones unificados, para que una variante tipográfica no esquive una regla."""
    text = unicodedata.normalize('NFKC', text)
    return re.sub('[‐‑‒–—―−]', '-', text)


def slug(heading):
    heading = re.sub(r'[`*]', '', heading).strip().lower()
    return re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')


def strict_json(text):
    """JSON sin claves duplicadas en ningún nivel; cualquier error devuelve None (falla cerrado)."""
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError('clave duplicada')
        return dict(pairs)
    try:
        return json.loads(text, object_pairs_hook=hook)
    except (ValueError, TypeError, RecursionError):
        return None


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def git(root, *args):
    r = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, encoding='utf-8')
    return r.returncode, r.stdout


def read(root, rel):
    try:
        return (Path(root) / rel).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None


def read_bytes(root, rel):
    try:
        p = Path(root) / rel
        return None if p.is_symlink() or not p.is_file() else p.read_bytes()
    except OSError:
        return None


def json_bytes(data):
    if not isinstance(data, bytes):
        return None
    try:
        return strict_json(data.decode('utf-8'))
    except UnicodeDecodeError:
        return None


def safe_doc_path(path):
    return (isinstance(path, str) and path.startswith('docs/') and path.endswith('.md') and '\\' not in path
            and '..' not in path.split('/') and '' not in path.split('/'))


def git_facts(root, sha):
    """Hechos Git de un commit candidato; todo lo no evaluable queda en falso o None (falla cerrado)."""
    f = {'commit': False, 'from_base': False, 'ancestor': False, 'changed': None, 'date': None, 'gate_doc': None}
    code, out = git(root, 'cat-file', '-t', sha)
    if code != 0 or out.strip() != 'commit':
        return f
    f['commit'] = True
    f['from_base'] = git(root, 'merge-base', '--is-ancestor', BASE, sha)[0] == 0
    f['ancestor'] = git(root, 'merge-base', '--is-ancestor', sha, 'HEAD')[0] == 0
    c1, diff = git(root, 'diff', '--name-only', '--no-renames', sha)
    c2, untracked = git(root, 'ls-files', '--others', '--exclude-standard')
    if c1 == 0 and c2 == 0:
        f['changed'] = sorted({ln.strip() for ln in (diff + untracked).splitlines() if ln.strip()})
    code, out = git(root, 'show', '-s', '--format=%cs', sha)
    f['date'] = out.strip() if code == 0 else None
    code, out = git(root, 'show', f'{sha}:{GATE_DOC}')
    f['gate_doc'] = out if code == 0 else None
    return f


def collect(root=ROOT):
    """Fotografía de todo lo que evalúan las reglas. Las pruebas la mutan en memoria."""
    texts = {rel: read(root, rel) for rel in PKG_FILES + GOV_FILES + [F33_MATRIX]}
    upstream = {rel: read_bytes(root, rel) for rel in UPSTREAM_FILES}
    tools = {}
    tdir = Path(root) / TOOLS
    if tdir.is_dir():
        for p in sorted(tdir.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                tools[p.relative_to(root).as_posix()] = read(root, p.relative_to(root).as_posix())
    evidence = {}
    edir = Path(root) / GATE_EVIDENCE
    if edir.exists() or edir.is_symlink():
        if edir.is_symlink() or not edir.is_dir():
            evidence[GATE_EVIDENCE] = None
        else:
            for p in sorted(edir.rglob('*')):
                rel = p.relative_to(root).as_posix()
                if p.is_symlink() or (not p.is_file() and not p.is_dir()):
                    evidence[rel] = None
                elif p.is_file():
                    evidence[rel] = read_bytes(root, rel)
    code, branch = git(root, 'rev-parse', '--abbrev-ref', 'HEAD')
    branch = branch.strip() if code == 0 else None
    base_ok = git(root, 'merge-base', '--is-ancestor', BASE, 'HEAD')[0] == 0
    changed = None
    c1, diff = git(root, 'diff', '--name-only', '--no-renames', BASE)
    c2, untracked = git(root, 'ls-files', '--others', '--exclude-standard')
    if c1 == 0 and c2 == 0:
        changed = {ln.strip() for ln in (diff + untracked).splitlines() if ln.strip()}
    base_gov = {}
    for rel in GOV_FILES:
        c, out = git(root, 'show', f'{BASE}:{rel}')
        base_gov[rel] = out if c == 0 else None
    changed_py = {rel: read(root, rel) for rel in sorted(changed or ()) if rel.endswith('.py')}
    # Commits candidatos citados por el estado del gate o por la evidencia, y ADR sucesores citados por FG-12.
    shas, adr_paths = set(), set()
    state = strict_json(texts.get(GATE_STATE) or '')
    if isinstance(state, dict) and isinstance(state.get('candidate_commit'), str):
        shas.add(state['candidate_commit'])
    for data in evidence.values():
        ev = json_bytes(data)
        if isinstance(ev, dict):
            if isinstance(ev.get('candidate_commit'), str):
                shas.add(ev['candidate_commit'])
            adr = ev.get('successor_adr')
            if isinstance(adr, dict) and safe_doc_path(adr.get('path')):
                adr_paths.add(adr['path'])
    facts = {sha: git_facts(root, sha) for sha in sorted(shas) if HEX40.fullmatch(sha)}
    repo_files = {p: read_bytes(root, p) for p in sorted(adr_paths)}
    return {'root': str(root), 'texts': texts, 'upstream': upstream, 'tools': tools, 'evidence': evidence,
            'branch': branch, 'base_ok': base_ok, 'changed': changed, 'base_gov': base_gov,
            'changed_py': changed_py, 'facts': facts, 'repo_files': repo_files}


def state_block(text):
    """Bloque «Estado vigente» de un documento de gobierno, hasta el siguiente encabezado de nivel 2."""
    if text is None:
        return None
    m = re.search(r'^## Estado vigente[^\n]*\n(.*?)(?=^## )', text, re.M | re.S)
    return m.group(1) if m else None


def bullets(block):
    return [ln[2:].strip() for ln in block.splitlines() if ln.startswith('- ')]


def table_rows(text, prefix):
    rows = []
    for ln in (text or '').splitlines():
        if ln.startswith(f'| {prefix}'):
            rows.append([c.strip() for c in ln.strip().strip('|').split(' | ')])
    return rows


def section(text, heading_prefix):
    m = re.search(rf'^## {re.escape(heading_prefix)}[^\n]*\n(.*?)(?=^## |\Z)', text or '', re.M | re.S)
    return m.group(1) if m else None


# ---------------------------------------------------------------- reglas del paquete

def rule_str(s):
    out = []
    missing = [p for p in PKG_FILES if s['texts'].get(p) is None]
    out.append((not missing, f'paquete completo ({len(PKG_FILES)} archivos); faltan: {missing}'))
    readme = s['texts'].get(f'{PKG}/README.md') or ''
    unlinked = [n for n in PKG_DOCS[1:] if f']({n})' not in readme]
    unlinked += [p for p in PKG_DATA if f']({p[len(PKG) + 1:]})' not in readme]
    out.append((not unlinked, f'el README enlaza todos los artefactos; sin enlace: {unlinked}'))
    return out


def rule_lnk(s):
    root = Path(s['root'])
    broken = []
    texts_by_path = {str((root / k).resolve()): v for k, v in s['texts'].items() if v is not None}
    for rel in [p for p in PKG_FILES if p.endswith('.md')] + GOV_FILES:
        text = s['texts'].get(rel)
        if text is None:
            continue
        links = re.findall(r'\]\(([^)\s]+)\)', text)
        if rel in GOV_FILES:
            # En gobierno solo se verifican los enlaces nuevos, hacia el paquete F36-SBX.
            links = [link for link in links if 'f36-sbx' in link]
        for link in links:
            if re.match(r'^[a-z]+:', link):
                continue
            path, _, anchor = link.partition('#')
            target = (root / rel).parent / path if path else root / rel
            try:
                target = target.resolve()
            except OSError:
                broken.append(f'{rel}→{link}')
                continue
            content = texts_by_path.get(str(target))
            if content is None:
                if not target.exists():
                    broken.append(f'{rel}→{link}')
                    continue
                if anchor and target.suffix == '.md':
                    content = target.read_text(encoding='utf-8')
            if anchor and target.suffix == '.md' and content is not None:
                if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', content, re.M)}:
                    broken.append(f'{rel}→{link}')
    return [(not broken, f'enlaces y anclas resueltos; rotos: {broken}')]


def rule_gov(s):
    out = []
    required = sorted(norm(r) for r in REQUIRED_STATE)
    for rel in GOV_FILES:
        block = state_block(s['texts'].get(rel))
        if block is None:
            out.append((False, f'{rel}: sin bloque «Estado vigente» (falla cerrado)'))
            continue
        bl = [norm(b) for b in bullets(block)]
        unknown = sorted(set(bl) - set(required))
        missing = sorted(set(required) - set(bl))
        dup = sorted({b for b in bl if bl.count(b) > 1})
        out.append((not unknown and not missing and not dup,
                    f'{rel}: el estado vigente tiene exactamente las {len(required)} líneas cerradas; '
                    f'desconocidas: {unknown}, ausentes: {missing}, repetidas: {dup}'))
        base_block = state_block(s['base_gov'].get(rel))
        if base_block is None:
            out.append((False, f'{rel}: no se pudo leer el estado vigente de la base {BASE[:7]} (falla cerrado)'))
        else:
            lost = [b for b in (norm(x) for x in bullets(base_block)) if b not in bl]
            out.append((not lost, f'{rel}: conserva todos los estados de la base; perdidos: {lost}'))
    out.append((CLAUDE_MEMBERS in (s['texts'].get('CLAUDE.md') or ''),
                'CLAUDE.md declara exactamente a los tres integrantes que exige el quórum del gate'))
    return out


def allowed_states(subj):
    if subj in ('G0', 'G0 real'):
        return {'NO APROBADA'}
    fixed = {'G0-SBX': {'APROBADA CON RESTRICCIONES'}, 'G0-02': {'PENDIENTE EXTERNO'},
             'G0-03': {'PENDIENTE EXTERNO'}, 'G0-12': {'PENDIENTE EXTERNO'}, 'G0-09': {'CUMPLIDO'},
             'G0-14': {'CUMPLIDO'}, 'ADR-005': {'PROPUESTA'}, 'ADR-005 canónico': {'PROPUESTA'},
             'F35 productiva': {'BLOQUEADA'}, 'F35-SBX': {'CERRADA Y CONGELADA'}, 'F36-SBX': {'EN DISEÑO'},
             'F36-SBX-GATE': {'NO SUPERADO'}}
    if subj in fixed:
        return fixed[subj]
    m = re.match(r'F(\d{2})', subj)
    if m and (int(m.group(1)) >= 36 or '-F' in subj):
        return {'BLOQUEADA', 'BLOQUEADAS', 'BLOQUEADO'}
    if subj.lower().startswith('alcance '):
        return {'BLOQUEADO'}
    if subj.lower() == 'datos reales':
        return {'PROHIBIDOS'}
    return set()


def state_claims(text):
    t = re.sub(r'[*`_]', '', norm(text))
    for rx in (CLAIM_RX, ID_CLAIM_RX):
        for m in rx.finditer(t):
            state = m.group('state').strip()
            if m.group('sep') == '=' or state.split(' ')[0] in STATE_WORDS:
                yield m.group('subj'), state


def rule_sem(s):
    hits = []
    for rel in PKG_FILES + GOV_FILES:
        text = s['texts'].get(rel)
        if text is None:
            continue
        # Sin marcado Markdown: «**F37-SBX** = …» no esquiva la regla.
        t = re.sub(r'[*`_]', '', norm(text))
        for pattern, label in FORBIDDEN_CLAIMS:
            for m in re.finditer(norm(pattern), t):
                hits.append(f'{rel}: {label} «{t[m.start():m.start() + 40].strip()}»')
    out = [(not hits, f'sin afirmaciones de estado prohibidas; encontradas: {hits}')]
    bad = []
    scopes = {p: s['texts'].get(p) for p in PKG_FILES if p.endswith('.md')}
    scopes.update({p: state_block(s['texts'].get(p)) for p in GOV_FILES})
    for rel, text in scopes.items():
        for subj, st in state_claims(text or ''):
            if st not in allowed_states(subj):
                bad.append(f'{rel}: «{subj} = {st}»')
    out.append((not bad, f'cada afirmación «sujeto = ESTADO» usa un estado admitido para su sujeto; '
                         f'no admitidas: {bad}'))
    sec = section(s['texts'].get(CHARTER) or '', '2. Estados de gobierno')
    rows = {}
    for ln in (sec or '').splitlines():
        cells = [c.strip() for c in ln.strip().strip('|').split(' | ')] if ln.startswith('| ') else []
        if len(cells) == 2 and cells[0] not in ('Estado', '---') and not cells[0].startswith('---'):
            rows[norm(cells[0])] = norm(cells[1])
    tab = [k for k, v in CHARTER_STATES.items() if not rows.get(k, '').startswith(v)]
    extra = sorted(set(rows) - set(CHARTER_STATES))
    out.append((sec is not None and not tab and not extra,
                f'la tabla de estados del charter coincide con el gobierno; distintas: {tab}, desconocidas: {extra}'))
    return out


def f33_classes(text):
    out = {}
    for cells in table_rows(text, 'CAP-'):
        if len(cells) < 3:
            continue
        cls = cells[2].replace('*', '').strip()
        for name in ('BLOQUEADA', 'FUTURA', 'PERMITIDA CON RESTRICCIONES', 'PERMITIDA'):
            if cls.startswith(name):
                out[cells[0]] = name
                break
    return out


def matrix_rows(text):
    rows, bad = {}, []
    for cells in table_rows(text, 'EI-'):
        if len(cells) != 7:
            bad.append(f'{cells[0]}: {len(cells)} columnas')
            continue
        ei, cap_text, cls, scope, caps, cond, stage = cells
        if ei in rows:
            bad.append(ei)
        rows[ei] = {'capacity': cap_text, 'class': cls.replace('*', '').strip(), 'scope': scope,
                    'caps': re.findall(r'CAP-\d\d', caps), 'cond': cond, 'stage': stage}
    return rows, bad


def rule_cap(s):
    out = []
    f33 = f33_classes(s['texts'].get(F33_MATRIX))
    out.append((len(f33) == 37, f'matriz F33 legible: {len(f33)} de 37 CAP'))
    rows, bad = matrix_rows(s['texts'].get(MATRIX))
    out.append((not bad, f'filas EI bien formadas y sin duplicados; problemas: {bad}'))
    out.append((sorted(rows) == EI_IDS, f'EI-01..EI-24 presentes exactamente; hay {sorted(rows)}'))
    pinned = [ei for ei in EI_IDS if ei in rows and (rows[ei]['class'], rows[ei]['scope']) != EXPECTED_MATRIX[ei]]
    out.append((not pinned, f'clase y alcance de cada EI iguales a la matriz fijada; reclasificadas: {pinned}'))
    errs = []
    for ei, r in rows.items():
        if r['class'] not in CLASSES:
            errs.append(f'{ei}: clase desconocida {r["class"]!r}')
            continue
        if r['scope'] not in ('B', 'C', '—'):
            errs.append(f'{ei}: alcance desconocido {r["scope"]!r}')
        for cap in r['caps']:
            if cap not in f33:
                errs.append(f'{ei}: {cap} no existe en F33')
            elif f33[cap] == 'BLOQUEADA' and r['class'] != 'BLOCKED':
                errs.append(f'{ei}: cita {cap} BLOQUEADA en F33 y no es BLOCKED')
            elif f33[cap] == 'FUTURA' and r['class'] == 'ALLOWED':
                errs.append(f'{ei}: cita {cap} FUTURA en F33 y es ALLOWED')
        if r['class'] == 'ALLOWED':
            if r['scope'] != 'B':
                errs.append(f'{ei}: ALLOWED fuera del alcance B')
            low = r['capacity'].lower()
            words = [w for w in NOT_ALLOWED_WORDS if re.search(w, low)]
            if words:
                errs.append(f'{ei}: capacidad ALLOWED que nombra {words}')
    out.append((not errs, f'clases coherentes con F33 y con la frontera B/C; errores: {errs}'))
    blocked_text = ' '.join(r['capacity'].lower() for r in rows.values() if r['class'] == 'BLOCKED')
    unblocked = [t for t in MUST_BLOCK if t not in blocked_text]
    out.append((not unblocked, f'todo lo prohibido está en una fila BLOCKED; sin bloquear: {unblocked}'))
    text = s['texts'].get(MATRIX) or ''
    summary = {}
    for cls in CLASSES:
        m = re.search(rf'^\| {cls} \| ([^|]+) \|$', text, re.M)
        summary[cls] = sorted(re.findall(r'EI-\d\d', m.group(1))) if m else None
    expected = {cls: sorted(k for k, v in rows.items() if v['class'] == cls) for cls in CLASSES}
    out.append((summary == expected, f'el resumen coincide con las filas: {summary} frente a {expected}'))
    return out


# ---------------------------------------------------------------- contrato de evidencia v2

def field_tokens(name):
    return set(name.lower().split('_'))


def contract_semantic_errors(c, root):
    """Invariantes del contrato v2 con mensajes explícitos (el hash fija además todo lo demás)."""
    e = []

    def need(cond, msg):
        if not cond:
            e.append(msg)

    need(list(c) == CONTRACT_KEYS, f'claves de primer nivel distintas del contrato cerrado: '
                                   f'faltan {sorted(set(CONTRACT_KEYS) - set(c))}, sobran {sorted(set(c) - set(CONTRACT_KEYS))}')
    need(c.get('contract_id') == 'f36sbx-evidence-contract' and c.get('contract_version') == '2'
         and c.get('status') == 'DISENO', 'identidad: f36sbx-evidence-contract v2 en estado DISENO')
    need(c.get('environment') == 'sandbox', 'environment debe ser sandbox')
    need(c.get('source_type_allowed') == ['synthetic'], 'source_type_allowed debe ser exactamente ["synthetic"]')
    need(c.get('generator_policy') == {'llm_allowed': False, 'template_based': True, 'seed_required': True,
                                       'byte_reproducible': True}, 'política del generador distinta: sin LLM, '
                                                                   'con plantillas, semilla y bytes reproducibles')
    up = c.get('allowed_upstream_sources')
    need(isinstance(up, list) and set(up) == ALLOWED_UPSTREAM and len(up) == len(set(up))
         and all((Path(root) / u).is_dir() for u in up), 'fuentes upstream admitidas fuera de la lista cerrada')
    files = c.get('upstream_files')
    need(files == {F34 + 'applications.csv': 'application_token', F34 + 'criteria.csv': 'criterion_id',
                   F34 + 'vacancies.csv': 'vacancy_token'}, 'archivos upstream distintos de las tres tablas F34')
    need(c.get('upstream_manifest') == F34 + 'manifest.json', 'manifiesto upstream distinto del de F34')
    need(c.get('upstream_ref_bindings') == {F34 + 'applications.csv': 'application_token',
                                            F34 + 'vacancies.csv': 'vacancy_token'},
         'provenance: faltan los vínculos obligatorios con la postulación y la vacante')
    need(c.get('content_upstream_bindings') == {'criterion_id': F34 + 'criteria.csv'},
         'provenance: falta el vínculo de criterion_id con criteria.csv')
    need(isinstance(c.get('forbidden_upstream_sources'), list)
         and REQUIRED_FORBIDDEN_SOURCES <= set(c['forbidden_upstream_sources']),
         f'fuentes prohibidas incompletas: deben incluir {sorted(REQUIRED_FORBIDDEN_SOURCES)}')
    need(c.get('synthetic_markers') == MARKERS, 'marcadores synthetic-only distintos de los exigidos')
    pats = c.get('identifier_patterns') if isinstance(c.get('identifier_patterns'), dict) else {}
    for key in ('artifact_id', 'fragment_id', 'output_id'):
        need(isinstance(pats.get(key), str) and pats[key].startswith('^SBX36-(ORG-S[1-3])-'),
             f'patrón {key}: debe fijar el prefijo SBX36- y la organización sintética')
    for key, value in pats.items():
        try:
            re.compile(value)
        except (re.error, TypeError):
            e.append(f'patrón {key} no compila')
    enums = c.get('enums') if isinstance(c.get('enums'), dict) else {}
    for key, value in enums.items():
        need(isinstance(value, list) and value and all(isinstance(x, str) and x for x in value)
             and len(value) == len(set(value)), f'enumerado {key}: lista no vacía de valores únicos')
        need(not (isinstance(value, list) and 'train' in value), f'enumerado {key}: contiene train')
    need(enums.get('partition') == ['dev', 'test'], 'partition: solo dev y test')
    need(enums.get('author_kind') == ['human_synthetic'], 'author_kind: solo human_synthetic')
    need(enums.get('review_status') == ['revisada_sintetica'], 'review_status: solo revisada_sintetica')
    need(enums.get('transcript_kind') == ['texto_sintetico_revisado'], 'transcript_kind: solo texto sintético revisado')
    need(enums.get('stage') == ['A', 'B'], 'stage: solo A y B')
    need(set(enums.get('observation_kind') or []) <= {'conducta_observada', 'aclaracion'},
         'observation_kind: solo conducta observada o aclaración, nunca una inferencia')
    need(set(enums.get('format') or []) <= {'pdf', 'docx'}, 'format: solo pdf o docx')
    types = c.get('artifact_types') if isinstance(c.get('artifact_types'), dict) else {}
    need(enums.get('artifact_type') == list(ARTIFACT_TYPES) and list(types) == list(ARTIFACT_TYPES),
         f'tipos de artefacto distintos de los ocho cerrados: {list(types)}')
    cft = c.get('content_field_types') if isinstance(c.get('content_field_types'), dict) else {}
    for field, kind in cft.items():
        ok = kind in ('text', 'list') or (isinstance(kind, str) and (
            (kind.startswith('enum:') and kind[5:] in enums) or (kind.startswith('pattern:') and kind[8:] in pats)))
        need(ok, f'tipo de campo de contenido desconocido: {field} = {kind!r}')
    record_fields = []
    for name, spec in types.items():
        if not isinstance(spec, dict) or set(spec) != {'stage', 'content_fields', 'list_items', 'text_paths',
                                                       'fragmentable'}:
            e.append(f'{name}: especificación con claves distintas del contrato')
            continue
        need(spec['stage'] == ARTIFACT_TYPES.get(name), f'{name}: etapa distinta de la fijada')
        cf = spec['content_fields'] if isinstance(spec['content_fields'], list) else []
        need(bool(cf) and all(f in cft for f in cf), f'{name}: campos de contenido sin tipo declarado')
        items = spec['list_items'] if isinstance(spec['list_items'], dict) else {}
        need(all(cft.get(k) == 'list' and k in cf and all(x in cft for x in v) for k, v in items.items())
             and all(k in items for k in cf if cft.get(k) == 'list'), f'{name}: listas sin estructura cerrada')
        need(isinstance(spec['fragmentable'], bool) and spec['fragmentable'] == bool(spec['text_paths']),
             f'{name}: fragmentable incoherente con text_paths')
        need(('grupo_sintetico' in cf) == (name == 'counterfactual_pair'), f'{name}: marcador de grupo fuera de lugar')
        record_fields += cf + [x for v in items.values() for x in v]
    need(c.get('artifact_envelope_fields') == ENVELOPE, 'sobre del artefacto distinto del cerrado')
    need(c.get('fragment_fields') == FRAGMENT_FIELDS, 'campos del fragmento distintos: la cadena de provenance '
                                                      'exige artifact_id, text_path, offsets y fragment_hash')
    need(c.get('output_fields') == OUTPUT_FIELDS, 'campos del output distintos: exige fragment_refs, abstained, '
                                                  'input_manifest_hash y output_hash, sin texto ni puntaje')
    need(c.get('context_fields') == CONTEXT, 'campos de contexto distintos de organización, escenario, vacante, '
                                             'postulación y partición')
    need(c.get('output_ei') == ['EI-07', 'EI-09', 'EI-10'] and all(
        EXPECTED_CLASSES.get(x) in ('ALLOWED', 'CONDITIONAL') for x in c.get('output_ei') or []),
         'output_ei: solo las EI de localización EI-07, EI-09 y EI-10')
    prov = c.get('provenance_fields') if isinstance(c.get('provenance_fields'), dict) else {}
    need(prov == {'artifact': PROVENANCE, 'upstream_ref': ['source', 'ref', 'sha256']},
         'provenance: faltan campos obligatorios del artefacto o de la referencia upstream')
    need(c.get('example_fields') == ['example_id', 'contract_version', 'example_only', 'note', 'artifacts',
                                     'fragments', 'outputs', 'partition_manifest'], 'campos del ejemplo distintos')
    need(c.get('partition_manifest_fields') == ['partitions', 'thresholds', 'test_used_for_tuning']
         and c.get('partition_fields') == {'dev': ['artifacts'], 'test': ['artifacts', 'sealed', 'seal_sha256']}
         and c.get('threshold_fields') == ['tuning_partition', 'tuning_outputs'],
         'manifiesto de particiones distinto: test debe estar sellado y los umbrales, ajustados con dev')
    need(isinstance(c.get('relations'), dict) and sorted(c['relations']) == REL_IDS
         and all(isinstance(v, str) and v for v in c['relations'].values()), 'relaciones REL-01..REL-12 incompletas')
    need(c.get('group_marker_only_in') == ['counterfactual_pair'], 'el marcador de grupo solo va en counterfactual_pair')
    forb = c.get('forbidden_fields') if isinstance(c.get('forbidden_fields'), list) else []
    need(REQUIRED_FORBIDDEN_FIELDS <= set(forb), f'campos prohibidos incompletos: '
                                                 f'faltan {sorted(REQUIRED_FORBIDDEN_FIELDS - set(forb))}')
    toks = c.get('forbidden_field_tokens') if isinstance(c.get('forbidden_field_tokens'), list) else []
    need(REQUIRED_FORBIDDEN_TOKENS <= set(toks), f'tokens prohibidos incompletos: '
                                                 f'faltan {sorted(REQUIRED_FORBIDDEN_TOKENS - set(toks))}')
    record_fields += ENVELOPE + FRAGMENT_FIELDS + OUTPUT_FIELDS + PROVENANCE + ['source', 'ref', 'sha256',
                                                                                  'partitions', 'thresholds',
                                                                                  'tuning_partition',
                                                                                  'tuning_outputs', 'sealed',
                                                                                  'seal_sha256', 'artifacts']
    leaked = sorted({f for f in record_fields if f in forb or field_tokens(f) & set(toks)})
    need(not leaked, f'campos de registro prohibidos o con tokens prohibidos: {leaked}')
    need(c.get('splits') == EXPECTED_SPLITS, 'garantías de partición distintas: solo dev y test, train prohibido, '
                                             'separación por familia y vacante, test sellado, umbrales en dev, '
                                             'test sin ajuste, embargo temporal y pares en la misma partición')
    return e


def load_upstream(c, upstream):
    """Tablas F34 indexadas por su clave y hashes (manifiesto, archivo); None si algo no se puede leer."""
    try:
        files = json.loads(upstream[c['upstream_manifest']].decode('utf-8'))['files']
        tables, hashes = {}, {}
        for path, key in c['upstream_files'].items():
            data = upstream[path]
            declared = (files.get(path.rsplit('/', 1)[1]) or {}).get('sha256')
            hashes[path] = (declared, sha256(data))
            tables[path] = {r[key]: r for r in csv.DictReader(io.StringIO(data.decode('utf-8'))) if key in r}
        return tables, hashes
    except (KeyError, AttributeError, TypeError, ValueError, UnicodeDecodeError):
        return None


def resolve_text(content, path, patterns):
    """Texto apuntado por text_path si coincide con un patrón del tipo; None en cualquier otro caso."""
    if not isinstance(path, str) or not isinstance(content, dict):
        return None
    parts = path.split('/')
    if not any(len(p.split('/')) == len(parts) and all(x == y or (x == '*' and INDEX.fullmatch(y))
                                                       for x, y in zip(p.split('/'), parts)) for p in patterns):
        return None
    cur = content
    for part in parts:
        if isinstance(cur, list) and INDEX.fullmatch(part) and int(part) < len(cur):
            cur = cur[int(part)]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur if isinstance(cur, str) else None


def bundle_errors(c, ex, upstream):
    """Invariantes REL-01..REL-12 de un conjunto de registros frente al contrato. Lista vacía = conforme."""
    errs = []
    try:
        _bundle(c, ex, upstream, errs.append)
    except Exception as exc:  # noqa: BLE001 — cualquier error de evaluación falla cerrado
        errs.append(f'registros no evaluables: {exc.__class__.__name__} (falla cerrado)')
    return errs


def _bundle(c, ex, upstream, add):
    up = load_upstream(c, upstream)
    if up is None:
        add('REL-02 tablas o manifiesto F34 ilegibles (falla cerrado)')
        return
    tables, hashes = up
    for path, (declared, actual) in hashes.items():
        if declared != actual:
            add(f'REL-02 {path}: hash distinto del declarado en el manifiesto F34')
    app_src = next((p for p, f in c['upstream_ref_bindings'].items() if f == 'application_token'), None)
    vac_src = next((p for p, f in c['upstream_ref_bindings'].items() if f == 'vacancy_token'), None)
    cri_src = c['content_upstream_bindings'].get('criterion_id')
    if app_src not in tables or vac_src not in tables or cri_src not in tables:
        add('REL-02 el contrato no vincula la postulación, la vacante y el criterio con tablas F34 (falla cerrado)')
        return
    if not isinstance(ex, dict):
        add('REL-01 ejemplo: JSON inválido, vacío o con claves duplicadas')
        return
    if set(ex) != set(c['example_fields']):
        add(f'REL-01 ejemplo: campos distintos del contrato: {sorted(set(ex) ^ set(c["example_fields"]))}')
    prefix = c['synthetic_markers']['text_prefix']
    if ex.get('example_only') is not True or ex.get('contract_version') != c['contract_version'] \
            or not str(ex.get('note', '')).startswith(prefix):
        add('REL-01 ejemplo: debe declararse solo ejemplo, de la versión del contrato y [SINTÉTICO]')
    pats = {k: re.compile(v) for k, v in c['identifier_patterns'].items()}
    enums, types, cft = c['enums'], c['artifact_types'], c['content_field_types']
    lists = {}
    for key in ('artifacts', 'fragments', 'outputs'):
        value = ex.get(key)
        if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
            add(f'REL-01 ejemplo: {key} debe ser una lista de objetos')
            value = [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []
        lists[key] = value
    ids = [r.get(k) for key, k in (('artifacts', 'synthetic_id'), ('fragments', 'fragment_id'),
                                   ('outputs', 'output_id')) for r in lists[key]]
    dup = sorted({str(i) for i in ids if ids.count(i) > 1})
    if dup:
        add(f'REL-03 identificadores repetidos: {dup}')
    arts = {a.get('synthetic_id'): a for a in lists['artifacts'] if isinstance(a.get('synthetic_id'), str)}

    def check_org(rid, kind, org, label):
        m = pats[kind].fullmatch(rid) if isinstance(rid, str) else None
        if not m:
            add(f'REL-01 {label}: identificador {rid!r} fuera de patrón')
        elif m.group(1) != org:
            add(f'REL-03 {label}: el identificador es de {m.group(1)} y el registro de {org!r}')

    def check_context(rec, label):
        if rec.get('synthetic_organization_id') not in c['synthetic_markers']['synthetic_organization_ids']:
            add(f'REL-01 {label}: organización sintética desconocida {rec.get("synthetic_organization_id")!r}')
        for field in ('scenario_id', 'vacancy_token', 'application_token'):
            if not (isinstance(rec.get(field), str) and pats[field].fullmatch(rec[field])):
                add(f'REL-01 {label}: {field} fuera de patrón')
        part = rec.get('partition')
        if part in c['splits']['forbidden_partitions']:
            add(f'REL-11 {label}: partición {part!r} prohibida')
        elif part not in enums['partition']:
            add(f'REL-11 {label}: partición desconocida {part!r}')
        vac = tables[vac_src].get(rec.get('vacancy_token'))
        app = tables[app_src].get(rec.get('application_token'))
        if vac is None:
            add(f'REL-04 {label}: la vacante {rec.get("vacancy_token")!r} no existe en F34')
        elif vac.get('organization_token') != rec.get('synthetic_organization_id'):
            add(f'REL-04 {label}: la vacante F34 es de otra organización')
        if app is None:
            add(f'REL-04 {label}: la postulación {rec.get("application_token")!r} no existe en F34')
        elif (app.get('vacancy_token'), app.get('organization_token')) != (rec.get('vacancy_token'),
                                                                            rec.get('synthetic_organization_id')):
            add(f'REL-04 {label}: la postulación F34 es de otra vacante u organización')

    def check_value(label, field, value, spec, where):
        kind = cft.get(field)
        if kind == 'text':
            if not isinstance(value, str) or not value.startswith(prefix):
                add(f'REL-12 {label}: {where}{field} sin el prefijo [SINTÉTICO]')
            elif not unicodedata.is_normalized('NFC', value):
                add(f'REL-12 {label}: {where}{field} no está en NFC')
            elif any(p.search(value) for p, _ in PII_PATTERNS):
                add(f'REL-12 {label}: {where}{field} contiene un patrón de PII')
            elif len(value) > 4000:
                add(f'REL-12 {label}: {where}{field} supera 4000 caracteres')
        elif kind == 'list':
            item_fields = spec['list_items'].get(field)
            if not isinstance(value, list) or not value or item_fields is None:
                add(f'REL-01 {label}: {where}{field} debe ser una lista no vacía')
                return
            for i, item in enumerate(value):
                if not isinstance(item, dict) or set(item) != set(item_fields):
                    add(f'REL-01 {label}: {where}{field}/{i} con campos distintos de {item_fields}')
                    continue
                for sub in item_fields:
                    check_value(label, sub, item[sub], spec, f'{where}{field}/{i}/')
        elif isinstance(kind, str) and kind.startswith('enum:'):
            if value not in enums[kind[5:]]:
                add(f'REL-01 {label}: {where}{field} con valor desconocido {value!r}')
        elif isinstance(kind, str) and kind.startswith('pattern:'):
            if not (isinstance(value, str) and pats[kind[8:]].fullmatch(value)):
                add(f'REL-01 {label}: {where}{field} fuera de patrón')
        else:
            add(f'REL-01 {label}: campo de contenido desconocido {where}{field}')

    # REL-01, REL-02, REL-04 y REL-12: cada artefacto.
    for a in lists['artifacts']:
        aid = a.get('synthetic_id', '?')
        label = f'artefacto {aid}'
        if set(a) != set(c['artifact_envelope_fields']):
            add(f'REL-01 {label}: sobre distinto del contrato: faltan '
                f'{sorted(set(c["artifact_envelope_fields"]) - set(a))}, sobran {sorted(set(a) - set(c["artifact_envelope_fields"]))}')
        check_org(aid, 'artifact_id', a.get('synthetic_organization_id'), label)
        t = a.get('artifact_type')
        spec = types.get(t) if isinstance(t, str) else None
        if spec is None:
            add(f'REL-01 {label}: artifact_type desconocido {t!r}')
        elif a.get('stage') != spec['stage']:
            add(f'REL-01 {label}: etapa {a.get("stage")!r} distinta de la del tipo')
        check_context(a, label)
        if not (isinstance(a.get('template_family'), str) and pats['template_family'].fullmatch(a['template_family'])):
            add(f'REL-01 {label}: template_family fuera de patrón')
        if a.get('source_type') not in c['source_type_allowed']:
            add(f'REL-01 {label}: source_type desconocido {a.get("source_type")!r}')
        if a.get('environment') != c['environment']:
            add(f'REL-01 {label}: environment distinto de sandbox')
        if a.get('hash_algorithm') != c['synthetic_markers']['hash_algorithm']:
            add(f'REL-01 {label}: hash_algorithm distinto del marcador')
        content = a.get('content')
        if not isinstance(content, dict):
            add(f'REL-01 {label}: content ausente o mal formado')
        elif spec is not None:
            if set(content) != set(spec['content_fields']):
                add(f'REL-01 {label}: contenido distinto del tipo: faltan '
                    f'{sorted(set(spec["content_fields"]) - set(content))}, sobran {sorted(set(content) - set(spec["content_fields"]))}')
            for field in spec['content_fields']:
                if field in content:
                    check_value(label, field, content[field], spec, '')
        if not (isinstance(content, dict) and a.get('content_hash') == sha256(canonical(content))):
            add(f'REL-01 {label}: content_hash incorrecto')
        p = a.get('provenance')
        if not isinstance(p, dict):
            add(f'REL-02 {label}: provenance ausente o mal formada')
            continue
        if set(p) != set(c['provenance_fields']['artifact']):
            add(f'REL-02 {label}: provenance distinta del contrato: faltan '
                f'{sorted(set(c["provenance_fields"]["artifact"]) - set(p))}, sobran {sorted(set(p) - set(c["provenance_fields"]["artifact"]))}')
        if not (isinstance(p.get('generator_id'), str) and pats['generator_id'].fullmatch(p['generator_id'])
                and isinstance(p.get('generator_version'), str) and pats['semver'].fullmatch(p['generator_version'])):
            add(f'REL-02 {label}: generador o versión fuera de patrón')
        mt = pats['template_id'].fullmatch(p.get('template_id') or '') if isinstance(p.get('template_id'), str) else None
        mf = pats['template_family'].fullmatch(a.get('template_family') or '') \
            if isinstance(a.get('template_family'), str) else None
        if not mt or not mf or mt.group(1) != mf.group(1) or p.get('template_family') != a.get('template_family'):
            add(f'REL-02 {label}: la plantilla de la provenance no pertenece a la familia del artefacto')
        if type(p.get('seed')) is not int or p['seed'] < 0:
            add(f'REL-02 {label}: semilla ausente o inválida')
        if p.get('content_hash') != a.get('content_hash'):
            add(f'REL-02 {label}: el content_hash de la provenance no es el del artefacto')
        refs = p.get('upstream_refs')
        if not isinstance(refs, list) or not refs:
            add(f'REL-02 {label}: sin referencias upstream')
            refs = []
        seen = set()
        for r in refs:
            if not isinstance(r, dict) or set(r) != set(c['provenance_fields']['upstream_ref']):
                add(f'REL-02 {label}: referencia upstream mal formada')
                continue
            src, ref = r['source'], r['ref']
            if not isinstance(src, str) or not isinstance(ref, str) or (src, ref) in seen:
                add(f'REL-02 {label}: referencia upstream repetida o inválida')
                continue
            seen.add((src, ref))
            if src not in c['upstream_files']:
                add(f'REL-02 {label}: fuente upstream no admitida {src!r}')
                continue
            if r['sha256'] != hashes[src][0] or r['sha256'] != hashes[src][1]:
                add(f'REL-02 {label}: hash de {src} distinto del manifiesto F34 o del archivo')
            if ref not in tables[src]:
                add(f'REL-02 {label}: {ref!r} no existe en {src}')
        for src, field in c['upstream_ref_bindings'].items():
            if (src, a.get(field)) not in seen:
                add(f'REL-02 {label}: falta la referencia upstream a su {field} en {src}')
        if isinstance(content, dict):
            for field, src in c['content_upstream_bindings'].items():
                if field in content and (src, content[field]) not in seen:
                    add(f'REL-02 {label}: falta la referencia upstream de content.{field}')

    # REL-05: aislamiento de vacante, postulación, familia y partición.
    def unique(key, value, message):
        seen = {}
        for a in arts.values():
            seen.setdefault(key(a), set()).add(value(a))
        for k, vs in sorted(seen.items(), key=lambda kv: str(kv[0])):
            if len(vs) > 1:
                add(f'REL-05 {message} {k}: {sorted(map(str, vs))}')
    unique(lambda a: a.get('vacancy_token'), lambda a: (a.get('synthetic_organization_id'), a.get('scenario_id')),
           'vacante mezclada entre organizaciones o escenarios')
    unique(lambda a: a.get('application_token'),
           lambda a: (a.get('synthetic_organization_id'), a.get('scenario_id'), a.get('vacancy_token')),
           'postulación mezclada entre organizaciones, escenarios o vacantes')
    unique(lambda a: a.get('template_family'), lambda a: a.get('partition'), 'familia de plantilla en varias particiones')
    unique(lambda a: a.get('vacancy_token'), lambda a: a.get('partition'), 'vacante en varias particiones')

    # REL-06: fragmentos.
    frs = {}
    for f in lists['fragments']:
        fid = f.get('fragment_id', '?')
        label = f'fragmento {fid}'
        if set(f) != set(c['fragment_fields']):
            add(f'REL-06 {label}: campos distintos del contrato: faltan {sorted(set(c["fragment_fields"]) - set(f))}, '
                f'sobran {sorted(set(f) - set(c["fragment_fields"]))}')
        check_org(fid, 'fragment_id', f.get('synthetic_organization_id'), label)
        if isinstance(fid, str):
            frs[fid] = f
        a = arts.get(f.get('artifact_id'))
        if a is None:
            add(f'REL-06 {label}: referencia un artefacto inexistente {f.get("artifact_id")!r}')
            continue
        spec = types.get(a.get('artifact_type'))
        if not spec or not spec['fragmentable']:
            add(f'REL-06 {label}: su artefacto no es fragmentable')
            continue
        for k in c['context_fields']:
            if f.get(k) != a.get(k):
                add(f'REL-06 {label}: mezcla de {k} con su artefacto ({f.get(k)!r} frente a {a.get(k)!r})')
        text = resolve_text(a.get('content'), f.get('text_path'), spec['text_paths'])
        if text is None:
            add(f'REL-06 {label}: text_path {f.get("text_path")!r} no apunta a un texto del artefacto')
            continue
        s0, s1 = f.get('char_start'), f.get('char_end')
        if type(s0) is not int or type(s1) is not int or not 0 <= s0 < s1 <= len(text):
            add(f'REL-06 {label}: offsets fuera del texto')
        elif f.get('fragment_hash') != sha256(text[s0:s1].encode('utf-8')):
            add(f'REL-06 {label}: fragment_hash incorrecto')

    # REL-07: outputs.
    outs = {}
    for o in lists['outputs']:
        oid = o.get('output_id', '?')
        label = f'output {oid}'
        if set(o) != set(c['output_fields']):
            add(f'REL-07 {label}: campos distintos del contrato: faltan {sorted(set(c["output_fields"]) - set(o))}, '
                f'sobran {sorted(set(o) - set(c["output_fields"]))}')
        check_org(oid, 'output_id', o.get('synthetic_organization_id'), label)
        check_context(o, label)
        if isinstance(oid, str):
            outs[oid] = o
        ei = o.get('ei')
        if ei not in c['output_ei']:
            add(f'REL-07 {label}: EI {ei!r} no admitida para outputs'
                + (' (BLOCKED)' if EXPECTED_CLASSES.get(ei) == 'BLOCKED' else ''))
        if not (isinstance(o.get('method_id'), str) and pats['method_id'].fullmatch(o['method_id'])
                and isinstance(o.get('method_version'), str) and pats['semver'].fullmatch(o['method_version'])):
            add(f'REL-07 {label}: método o versión fuera de patrón')
        row = tables[cri_src].get(o.get('query_criterion_id'))
        if row is None or row.get('vacancy_token') != o.get('vacancy_token'):
            add(f'REL-07 {label}: el criterio de la consulta no existe en F34 o es de otra vacante')
        refs = o.get('fragment_refs')
        if not isinstance(refs, list) or not all(isinstance(r, str) for r in refs) or len(set(refs)) != len(refs):
            add(f'REL-07 {label}: fragment_refs debe ser una lista de identificadores únicos')
            refs = [r for r in refs if isinstance(r, str)] if isinstance(refs, list) else []
        for r in refs:
            f = frs.get(r)
            if f is None:
                add(f'REL-07 {label}: referencia un fragmento inexistente {r!r}')
                continue
            for k in c['context_fields']:
                if f.get(k) != o.get(k):
                    add(f'REL-07 {label}: mezcla de {k} con el fragmento {r}')
        ab = o.get('abstained')
        if type(ab) is not bool:
            add(f'REL-07 {label}: abstained debe ser booleano')
        elif ab != (len(refs) == 0):
            add(f'REL-07 {label}: la abstención no coincide con la ausencia de fragmentos')
        pool = sorted([fid, f.get('fragment_hash')] for fid, f in frs.items()
                      if (f.get('application_token'), f.get('partition')) == (o.get('application_token'),
                                                                               o.get('partition')))
        if o.get('input_manifest_hash') != sha256(canonical(pool)):
            add(f'REL-07 {label}: input_manifest_hash incorrecto')
        payload = {k: o.get(k) for k in ('abstained', 'ei', 'fragment_refs', 'method_id', 'method_version',
                                         'output_id', 'query_criterion_id')}
        if o.get('output_hash') != sha256(canonical(payload)):
            add(f'REL-07 {label}: output_hash incorrecto')

    # REL-08, REL-09 y REL-10: referencias entre artefactos.
    for aid, a in arts.items():
        content = a.get('content') if isinstance(a.get('content'), dict) else {}
        t = a.get('artifact_type')
        label = f'artefacto {aid}'
        if t == 'relevance_annotation':
            f = frs.get(content.get('fragment_id'))
            if f is None:
                add(f'REL-08 {label}: la anotación referencia un fragmento inexistente')
            else:
                for k in c['context_fields']:
                    if f.get(k) != a.get(k):
                        add(f'REL-08 {label}: mezcla de {k} con el fragmento anotado')
            row = tables[cri_src].get(content.get('criterion_id'))
            if row is None or row.get('vacancy_token') != a.get('vacancy_token'):
                add(f'REL-08 {label}: el criterio no existe en F34 o es de otra vacante')
        elif t == 'counterfactual_pair':
            b = arts.get(content.get('variant_of'))
            if b is None or b is a:
                add(f'REL-09 {label}: la variante referencia un artefacto inexistente')
            elif not types.get(b.get('artifact_type'), {}).get('fragmentable'):
                add(f'REL-09 {label}: la variante no es un artefacto fragmentable')
            else:
                for k in ('synthetic_organization_id', 'scenario_id', 'vacancy_token', 'partition', 'template_family'):
                    if b.get(k) != a.get(k):
                        add(f'REL-09 {label}: mezcla de {k} con su variante')
        elif t == 'rendered_document':
            b = arts.get(content.get('rendered_from'))
            if b is None or b.get('artifact_type') != 'cv_document':
                add(f'REL-10 {label}: el origen no existe o no es un cv_document')
            else:
                for k in c['context_fields'] + ['template_family']:
                    if b.get(k) != a.get(k):
                        add(f'REL-10 {label}: mezcla de {k} con su origen')

    # REL-11: manifiesto de particiones, sello de test y ajuste solo con dev.
    pm = ex.get('partition_manifest')
    if not isinstance(pm, dict) or set(pm) != set(c['partition_manifest_fields']):
        add('REL-11 manifiesto de particiones ausente o con campos distintos del contrato')
        return
    parts = pm['partitions']
    if not isinstance(parts, dict):
        add('REL-11 particiones mal formadas')
    else:
        for name in parts:
            if name not in c['splits']['partitions']:
                kind = 'prohibida' if name in c['splits']['forbidden_partitions'] else 'desconocida'
                add(f'REL-11 partición {kind} en el manifiesto: {name!r}')
        if set(parts) != set(c['splits']['partitions']):
            add('REL-11 el manifiesto debe declarar exactamente dev y test')
        listed = {}
        for name, spec in parts.items():
            expected = c['partition_fields'].get(name)
            if expected is None:
                continue
            if not isinstance(spec, dict) or set(spec) != set(expected):
                add(f'REL-11 partición {name}: campos distintos de {expected}')
                continue
            ids = spec['artifacts']
            if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids) or len(set(ids)) != len(ids):
                add(f'REL-11 partición {name}: lista de artefactos inválida')
                continue
            for i in ids:
                if i in listed:
                    add(f'REL-11 {i} figura en dos particiones')
                listed[i] = name
                if i not in arts:
                    add(f'REL-11 partición {name}: artefacto inexistente {i!r}')
                elif arts[i].get('partition') != name:
                    add(f'REL-11 {i} está en {name} y declara {arts[i].get("partition")!r}')
        missing = sorted(set(arts) - set(listed))
        if missing:
            add(f'REL-11 artefactos fuera del manifiesto: {missing}')
        test = parts.get('test')
        if isinstance(test, dict) and set(test) == set(c['partition_fields']['test']):
            if test['sealed'] is not True:
                add('REL-11 la partición test no está sellada')
            pairs = sorted([i, a.get('content_hash')] for i, a in arts.items() if a.get('partition') == 'test')
            if test['seal_sha256'] != sha256(canonical(pairs)):
                add('REL-11 el sello de test no coincide con sus artefactos')
    th = pm['thresholds']
    if not isinstance(th, dict) or set(th) != set(c['threshold_fields']):
        add('REL-11 umbrales mal formados')
    else:
        if th['tuning_partition'] != c['splits']['thresholds_fit_on']:
            add(f'REL-11 umbrales ajustados en {th["tuning_partition"]!r}: solo se ajusta con dev')
        tuning = th['tuning_outputs']
        if not isinstance(tuning, list):
            add('REL-11 tuning_outputs debe ser una lista')
        else:
            for x in tuning:
                if x not in outs:
                    add(f'REL-11 output de ajuste inexistente {x!r}')
                elif outs[x].get('partition') != 'dev':
                    add(f'REL-11 el output de ajuste {x} es de {outs[x].get("partition")!r}: test no puede ajustar')
    if pm['test_used_for_tuning'] is not False:
        add('REL-11 test_used_for_tuning debe ser false')


def rule_ctr(s):
    out = []
    c = strict_json(s['texts'].get(CONTRACT) or '')
    if not isinstance(c, dict):
        return [(False, 'contrato de evidencia: JSON inválido o con claves duplicadas (falla cerrado)')]
    digest = sha256(canonical(c))
    out.append((digest == CONTRACT_SHA256, f'contrato idéntico a la versión cerrada v2 (SHA-256 canónico '
                                           f'{digest[:12]}, esperado {CONTRACT_SHA256[:12]})'))
    errs = contract_semantic_errors(c, s['root'])
    out.append((not errs, f'invariantes del contrato: solo sintético, cerrado, provenance y particiones; '
                          f'errores: {errs}'))
    if errs:
        out.append((False, 'ejemplo de conformidad no evaluado: el contrato no es válido (falla cerrado)'))
        return out
    ex = strict_json(s['texts'].get(EXAMPLE) or '')
    berrs = bundle_errors(c, ex, s['upstream'])
    out.append((not berrs, f'ejemplo de conformidad conforme a REL-01..REL-12; errores: {berrs}'))
    return out


def rule_thr(s):
    rows = table_rows(s['texts'].get(THREATS), 'TEI-')
    ids = [r[0] for r in rows]
    out = [(ids == TEI_IDS, f'TEI-01..TEI-22 en orden y sin huecos; hay {ids}')]
    weak = [r[0] for r in rows if len(r) != 6 or any(not c or c in ('—', '-') for c in (r[4], r[5]))]
    out.append((not weak, f'cada amenaza tiene control y comportamiento fail-closed; incompletas: {weak}'))
    text = ' '.join(r[1].lower() for r in rows if len(r) == 6)
    missing = [t for t in THREAT_TOPICS if t not in text]
    out.append((not missing, f'el modelo cubre los temas exigidos; faltan: {missing}'))
    return out


def rule_eva(s):
    text = s['texts'].get(PLAN) or ''
    mrows = table_rows(text, 'M-')
    rrows = table_rows(text, 'R-')
    out = [([r[0] for r in mrows] == M_IDS, f'M-01..M-13 presentes; hay {[r[0] for r in mrows]}'),
           ([r[0] for r in rrows] == R_IDS, f'R-01..R-05 presentes; hay {[r[0] for r in rrows]}')]
    covered = set()
    for r in mrows:
        if len(r) > 1:
            covered |= set(re.findall(r'EI-\d\d', r[1]))
    needed = sorted(k for k, v in EXPECTED_CLASSES.items() if v in ('ALLOWED', 'CONDITIONAL'))
    uncovered = [e for e in needed if e not in covered]
    out.append((not uncovered, f'cada EI ALLOWED o CONDITIONAL tiene métrica; sin métrica: {uncovered}'))
    blocked = sorted(e for e in covered if EXPECTED_CLASSES.get(e) != 'ALLOWED' and EXPECTED_CLASSES.get(e) != 'CONDITIONAL')
    out.append((not blocked, f'ninguna EI BLOCKED o desconocida tiene métrica; con métrica: {blocked}'))
    m = re.search(r'^## 6\. Resultados\n+(.*)', text, re.M | re.S)
    out.append((bool(m) and m.group(1).strip().startswith('**No hay resultados.**'),
                'el plan declara que no hay resultados'))
    return out


def rule_frz(s):
    out = [(s['branch'] in BRANCHES, f'rama admitida: {s["branch"]}'),
           (s['base_ok'], f'la base {BASE[:7]} es ancestro de HEAD')]
    changed = s['changed']
    if changed is None:
        out.append((False, 'estado Git desconocido: no se puede verificar el alcance (falla cerrado)'))
        return out
    allowed = [p for p in changed if p.startswith(PKG + '/') or p.startswith(TOOLS + '/') or p in GOV_FILES]
    outside = sorted(set(changed) - set(allowed))
    out.append((not outside, f'cambios solo en el paquete, sus herramientas y el gobierno ({len(changed)}); '
                             f'fuera de alcance: {outside}'))
    runtime = sorted(p for p in changed if p.startswith(RUNTIME_PREFIXES) or p in DEPENDENCY_FILES)
    out.append((not runtime, f'0 cambios de runtime, producto o dependencias; encontrados: {runtime}'))
    frozen = sorted(p for p in changed if p.startswith(F35_FROZEN))
    out.append((not frozen, f'F35-SBX, G0 y los antecedentes congelados intactos; tocados: {frozen}'))
    return out


def rule_dep(s):
    errs = []
    for rel, src in sorted(s['tools'].items()):
        if not rel.endswith('.py'):
            continue
        try:
            tree = ast.parse(src or '')
        except SyntaxError:
            errs.append(f'{rel}: no se puede analizar')
            continue
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [(node.module or '').split('.')[0]]
            errs += [f'{rel}: importa {n}' for n in names if n not in STDLIB and n not in LOCAL_MODULES]
        if '\x08' in (src or ''):
            errs.append(f'{rel}: contiene bytes de retroceso (0x08), que anulan patrones como \\b')
    for rel, src in sorted(s['changed_py'].items()):
        errs += [f'{rel}: importa {m.group(1)} (ML, NLP o red)' for m in ML_IMPORT.finditer(src or '')]
    return [(not errs, f'solo biblioteca estándar y ningún import de ML, NLP o red; encontrados: {sorted(set(errs))}')]


def rule_pii(s):
    hits = []
    scope = {p: s['texts'].get(p) for p in PKG_FILES}
    scope.update({p: t for p, t in s['tools'].items() if p.endswith('.py')})
    scope.update({p: b.decode('utf-8', 'replace') for p, b in s['evidence'].items() if isinstance(b, bytes)})
    for rel, text in scope.items():
        for pattern, label in PII_PATTERNS:
            if text and pattern.search(text):
                hits.append(f'{rel}: {label}')
    return [(not hits, f'sin patrones de PII en el paquete, sus herramientas ni la evidencia; encontrados: {hits}')]


# ---------------------------------------------------------------- evidencia de equipo y gate

def team_schema_errors(sch):
    """Invariantes del esquema de evidencia de equipo (su hash fija además todo lo demás)."""
    if not isinstance(sch, dict):
        return ['esquema ilegible']
    e = []

    def need(cond, msg):
        if not cond:
            e.append(msg)
    crit = sch.get('criteria') if isinstance(sch.get('criteria'), dict) else {}
    get = lambda fg, k: (crit.get(fg) or {}).get(k)  # noqa: E731
    need(sch.get('schema_tag') == 'f36sbx-team-evidence/v1' and sch.get('gate_id') == 'F36-SBX-GATE'
         and sch.get('gate_version') == '2', 'identidad del esquema y del gate')
    need(sch.get('evidence_paths') == {fg: f'{GATE_EVIDENCE}{fg}.json' for fg in FG_TEAM},
         'rutas fijas de la evidencia de FG-02, FG-03, FG-10 y FG-12')
    need(sch.get('team_members') == list(MEMBERS), 'lista cerrada de los tres integrantes')
    need((sch.get('candidate_binding') or {}).get('descends_from') == BASE, 'el candidato desciende de la base')
    ap = sch.get('approvals') if isinstance(sch.get('approvals'), dict) else {}
    need(ap.get('required_vote') == 'APRUEBA' and ap.get('quorum') == '3/3', 'aprobación explícita con quórum 3/3')
    need(set(get('FG-02', 'passing_verdicts') or []) <= {'APROBADO_PARA_INTEGRACION', 'APROBADO_CON_OBSERVACIONES'}
         and set(get('FG-02', 'must_be_zero') or []) >= {'blocker', 'high', 'medium_requiring_fix'},
         'FG-02: solo veredictos aprobatorios y cero BLOCKER, HIGH y MEDIUM que requiere corrección')
    need(get('FG-03', 'passing_decision') == 'AUTORIZA_INICIO_F37_SBX'
         and get('FG-03', 'authorizable_classes') == ['ALLOWED', 'CONDITIONAL'],
         'FG-03: autorización explícita y solo EI ALLOWED o CONDITIONAL')
    need(get('FG-10', 'passing_approval_status') == 'APROBADA'
         and str(get('FG-10', 'version_pattern') or '').startswith('^==')
         and get('FG-10', 'dependency_ei') == ['EI-10', 'EI-11', 'EI-12'],
         'FG-10: dependencias aprobadas, con versión exacta y solo para EI-10, EI-11 y EI-12')
    need(get('FG-12', 'passing_adr_status') == 'APROBADO' and get('FG-12', 'coverable_ei') == SCOPE_C_CONDITIONAL
         and get('FG-12', 'ei09_passing_decision') == 'CABE_EN_ALCANCE_B'
         and not any(re.fullmatch(str(get('FG-12', 'adr_id_pattern') or ''), f'ADR-00{i}') for i in range(1, 6)),
         'FG-12: ADR sucesor APROBADO y distinto de ADR-001..ADR-005, cobertura solo de EI CONDITIONAL de alcance C')
    return e


def doc_status_only(old, new):
    """El documento del gate solo cambió en la columna Estado de la tabla FG."""
    if old is None or new is None:
        return False
    a, b = old.split('\n'), new.split('\n')
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x == y:
            continue
        cx = [c.strip() for c in x.strip().strip('|').split(' | ')]
        cy = [c.strip() for c in y.strip().strip('|').split(' | ')]
        if not (x.startswith('| FG-') and y.startswith('| FG-') and len(cx) == len(cy) == 5 and cx[:4] == cy[:4]
                and cy[4] in STATUSES):
            return False
    return True


def binding_errors(sha, facts, gate_doc):
    """Vínculo reproducible con el candidato: commit de la rama, ancestro de HEAD y sin cambios materiales después."""
    if not isinstance(sha, str) or not HEX40.fullmatch(sha):
        return ['candidate_commit fuera de formato (40 hexadecimales en minúscula)']
    f = facts.get(sha)
    if not isinstance(f, dict):
        return [f'sin datos Git del candidato {sha[:12]} (falla cerrado)']
    e = []
    if not f.get('commit'):
        e.append(f'{sha[:12]} no es un commit del repositorio')
    if not f.get('from_base'):
        e.append(f'{sha[:12]} no desciende de la base {BASE[:7]}')
    if not f.get('ancestor'):
        e.append(f'{sha[:12]} no es ancestro de HEAD')
    changed = f.get('changed')
    if changed is None:
        e.append('cambios posteriores al candidato no evaluables (falla cerrado)')
    else:
        outside = sorted(p for p in changed if not (p.startswith(GATE_EVIDENCE) or p in (GATE_STATE, GATE_DOC)))
        if outside:
            e.append(f'el paquete cambió después del commit auditado: {outside[:6]}')
        if GATE_DOC in changed and not doc_status_only(f.get('gate_doc'), gate_doc):
            e.append('el documento del gate cambió fuera de la columna Estado de la tabla FG')
    if parse_date(f.get('date')) is None:
        e.append('fecha del commit candidato ilegible')
    return e


def approval_errors(fg, ev, ctx, cdate, rdate):
    rule, members = ctx['schema']['approvals'], ctx['schema']['team_members']
    ap = ev.get('approvals')
    if not isinstance(ap, list):
        return [f'{fg}: approvals debe ser una lista']
    e, names = [], []
    for i, a in enumerate(ap):
        if not isinstance(a, dict) or set(a) != set(rule['fields']):
            e.append(f'{fg}: aprobación {i} con campos distintos de {rule["fields"]}')
            continue
        names.append(a['member'])
        if a['member'] not in members:
            e.append(f'{fg}: integrante no reconocido {a["member"]!r} (se exige la identidad exacta)')
        if a['vote'] not in rule['votes']:
            e.append(f'{fg}: voto desconocido {a["vote"]!r}')
        elif a['vote'] != rule['required_vote']:
            e.append(f'{fg}: {a["member"]} no aprueba ({a["vote"]})')
        d = parse_date(a['date'])
        if d is None or (cdate and d < cdate) or (rdate and d > rdate):
            e.append(f'{fg}: fecha de aprobación de {a["member"]!r} inválida o fuera del registro')
    if len(names) != len(set(names)):
        e.append(f'{fg}: integrante duplicado en las aprobaciones')
    approving = {a['member'] for a in ap if isinstance(a, dict) and a.get('member') in members
                 and a.get('vote') == rule['required_vote']}
    if approving != set(members) or len(ap) != len(members):
        e.append(f'{fg}: quórum incompleto {len(approving)}/{len(members)}')
    if ev.get('quorum') != rule['quorum']:
        e.append(f'{fg}: quorum declarado distinto de {rule["quorum"]}')
    return e


def authorized_list_errors(fg, lst, ctx):
    allowed = ctx['schema']['criteria']['FG-03']['authorizable_classes']
    if not isinstance(lst, list) or not lst:
        return [f'{fg}: falta la lista explícita y cerrada de EI autorizadas']
    e = []
    if len({str(x) for x in lst}) != len(lst):
        e.append(f'{fg}: EI repetidas')
    for x in lst:
        cls = ctx['classes'].get(x) if isinstance(x, str) else None
        if cls is None:
            e.append(f'{fg}: EI desconocida o fuera de la matriz {x!r}')
        elif cls not in allowed:
            e.append(f'{fg}: {x} es {cls}: no se puede autorizar')
    return e


def fg02_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-02'], []
    au = ev.get('auditor')
    if not isinstance(au, dict) or set(au) != set(c['auditor_fields']):
        e.append('FG-02: auditor con campos distintos del esquema')
    else:
        name = au['name']
        if not isinstance(name, str) or not 3 <= len(name.strip()) <= 120 \
                or name.strip().casefold() in PLACEHOLDERS:
            e.append('FG-02: auditor no identificado de forma inequívoca')
        if au['kind'] not in c['auditor_kinds']:
            e.append(f'FG-02: tipo de auditor desconocido {au["kind"]!r}')
        if au['independent_of_candidate'] is not True:
            e.append('FG-02: el auditor no se declara independiente del candidato')
    rep = ev.get('audit_report')
    if not isinstance(rep, dict) or set(rep) != set(c['audit_report_fields']):
        e.append('FG-02: referencia al informe de auditoría mal formada')
    else:
        p = rep['path']
        if not (isinstance(p, str) and p.startswith(GATE_EVIDENCE) and p.endswith('.md')
                and '..' not in p.split('/') and '\\' not in p):
            e.append('FG-02: el informe debe ser un .md dentro de gate/evidencia/')
        else:
            data = ctx['evidence'].get(p)
            if not isinstance(data, bytes) or not data.strip():
                e.append('FG-02: el informe de auditoría no existe o está vacío')
            elif sha256(data) != rep['sha256']:
                e.append('FG-02: SHA-256 del informe distinto del declarado')
            elif not isinstance(ev.get('candidate_commit'), str) \
                    or ev['candidate_commit'] not in data.decode('utf-8', 'replace'):
                e.append('FG-02: el informe no nombra el commit candidato completo')
    verdict = ev.get('verdict')
    if verdict not in c['verdicts']:
        e.append(f'FG-02: veredicto desconocido {verdict!r}')
    elif verdict not in c['passing_verdicts']:
        e.append(f'FG-02: veredicto {verdict}: no aprueba el candidato')
    fo = ev.get('findings_open')
    if not isinstance(fo, dict) or set(fo) != set(c['findings_fields']):
        e.append('FG-02: findings_open con campos distintos del esquema')
    else:
        for k in c['findings_fields']:
            n = fo[k]
            if type(n) is not int or n < 0:
                e.append(f'FG-02: findings_open.{k} debe ser un entero no negativo')
            elif k in c['must_be_zero'] and n:
                e.append(f'FG-02: {k} abiertos = {n}')
    return e


def fg03_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-03'], []
    if ev.get('decision') not in c['decisions']:
        e.append(f'FG-03: decisión desconocida {ev.get("decision")!r}')
    elif ev['decision'] != c['passing_decision']:
        e.append('FG-03: el equipo no autoriza el inicio de F37-SBX')
    if ev.get('numbering_f36_m01') not in c['numbering_values']:
        e.append('FG-03: falta la confirmación de la numeración F36-M01')
    elif ev['numbering_f36_m01'] != c['passing_numbering']:
        e.append('FG-03: numeración F36-M01 no confirmada')
    e += authorized_list_errors('FG-03', ev.get('authorized_ei'), ctx)
    if ev.get('authorized_ei') != ctx['state'].get('f37_authorized_ei'):
        e.append('FG-03: authorized_ei distinta de f37_authorized_ei del estado del gate')
    return e + approval_errors('FG-03', ev, ctx, cdate, rdate)


def fg03_list(ctx):
    """EI autorizadas por una FG-03 válida; None si FG-03 no tiene evidencia válida."""
    if team_evidence_errors('FG-03', ctx):
        return None
    return json_bytes(ctx['evidence'].get(ctx['schema']['evidence_paths']['FG-03']))['authorized_ei']


def fg10_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-10'], []
    auth = fg03_list(ctx)
    if auth is None:
        e.append('FG-10: requiere una autorización FG-03 válida')
        auth = []
    nd, deps = ev.get('new_dependencies'), ev.get('dependencies')
    if type(nd) is not bool:
        e.append('FG-10: new_dependencies debe ser booleano')
    if not isinstance(deps, list):
        e.append('FG-10: dependencies debe ser una lista')
        deps = []
    need = sorted(set(auth) & set(c['dependency_ei']))
    if nd is False and deps:
        e.append('FG-10: declara que no hay dependencias nuevas y lista dependencias')
    if nd is False and need:
        e.append(f'FG-10: {need} requieren dependencias registradas y aprobadas')
    if nd is True and not deps:
        e.append('FG-10: declara dependencias nuevas y no lista ninguna')
    names, covered = [], set()
    for i, d in enumerate(deps):
        if not isinstance(d, dict) or set(d) != set(c['dependency_fields']):
            e.append(f'FG-10: dependencia {i} con estructura desconocida o incompleta')
            continue
        n = d['name']
        if not (isinstance(n, str) and re.fullmatch(c['name_pattern'], n)):
            e.append(f'FG-10: dependencia {i} con nombre inválido')
            continue
        names.append(n.lower())
        if not (isinstance(d['version'], str) and re.fullmatch(c['version_pattern'], d['version'])):
            e.append(f'FG-10: {n}: versión no fijada con == exacto')
        if not (isinstance(d['purpose'], str) and 10 <= len(d['purpose'].strip()) <= 300):
            e.append(f'FG-10: {n}: propósito ausente o genérico')
        if d['license'] not in c['licenses']:
            e.append(f'FG-10: {n}: licencia fuera de la lista admitida')
        if d['source'] not in c['sources']:
            e.append(f'FG-10: {n}: origen no admitido')
        if d['source_url'] != c['source_url_template'].format(name=n):
            e.append(f'FG-10: {n}: URL de origen distinta de la canónica')
        sc = d['supply_chain_review']
        if not isinstance(sc, dict) or set(sc) != set(c['supply_chain_fields']):
            e.append(f'FG-10: {n}: revisión de cadena de suministro mal formada')
        else:
            od = parse_date(sc['osv_checked_on'])
            if od is None or (cdate and od < cdate) or (rdate and od > rdate):
                e.append(f'FG-10: {n}: fecha de la consulta OSV inválida')
            if type(sc['open_vulnerabilities']) is not int or sc['open_vulnerabilities'] != 0:
                e.append(f'FG-10: {n}: vulnerabilidades abiertas o recuento inválido')
            if not (isinstance(sc['artifact_sha256'], str) and HEX64.fullmatch(sc['artifact_sha256'])):
                e.append(f'FG-10: {n}: SHA-256 del artefacto inválido')
            if sc['reviewed_by'] not in ctx['schema']['team_members']:
                e.append(f'FG-10: {n}: revisor no reconocido')
        rel = d['related_ei']
        if not isinstance(rel, list) or not rel:
            e.append(f'FG-10: {n}: sin EI relacionadas')
        else:
            for x in rel:
                if x not in auth:
                    e.append(f'FG-10: {n}: {x!r} no está entre las EI autorizadas por FG-03')
                elif x not in c['dependency_ei']:
                    e.append(f'FG-10: {n}: {x} no justifica dependencias nuevas')
                else:
                    covered.add(x)
        if d['approval_status'] not in c['approval_statuses']:
            e.append(f'FG-10: {n}: estado de aprobación desconocido')
        elif d['approval_status'] != c['passing_approval_status']:
            e.append(f'FG-10: {n}: dependencia no APROBADA ({d["approval_status"]})')
    if len(names) != len(set(names)):
        e.append('FG-10: dependencias repetidas')
    if nd is True and set(need) - covered:
        e.append(f'FG-10: {sorted(set(need) - covered)} sin dependencia aprobada que las cubra')
    return e + approval_errors('FG-10', ev, ctx, cdate, rdate)


def fg12_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-12'], []
    auth = fg03_list(ctx)
    if auth is None:
        e.append('FG-12: requiere una autorización FG-03 válida')
        auth = []
    need = sorted(x for x in auth if x in c['coverable_ei'])
    cov = ev.get('covered_ei')
    if not isinstance(cov, list) or len({str(x) for x in cov}) != len(cov):
        e.append('FG-12: covered_ei debe ser una lista sin repetidos')
        cov = []
    for x in cov:
        cls = ctx['classes'].get(x) if isinstance(x, str) else None
        if cls is None:
            e.append(f'FG-12: EI desconocida {x!r}')
        elif cls == 'BLOCKED':
            e.append(f'FG-12: intenta autorizar {x}, que es BLOCKED')
        elif x not in c['coverable_ei']:
            e.append(f'FG-12: {x} no es una EI CONDITIONAL de alcance C')
    adr = ev.get('successor_adr')
    if adr is None:
        if need:
            e.append(f'FG-12: {need} exigen un ADR sucesor APROBADO')
        if cov:
            e.append('FG-12: covered_ei sin ADR sucesor')
    elif not isinstance(adr, dict) or set(adr) != set(c['adr_fields']):
        e.append('FG-12: successor_adr con campos distintos del esquema')
    else:
        if not (isinstance(adr['id'], str) and re.fullmatch(c['adr_id_pattern'], adr['id'])):
            e.append('FG-12: id de ADR inválido o reservado (ADR-001..ADR-005)')
        if adr['status'] not in c['adr_statuses']:
            e.append(f'FG-12: estado de ADR desconocido {adr["status"]!r}')
        elif adr['status'] != c['passing_adr_status']:
            e.append(f'FG-12: el ADR sucesor está {adr["status"]}, no {c["passing_adr_status"]}')
        if adr['relation_to_adr005'] not in c['relations_to_adr005']:
            e.append('FG-12: relación con ADR-005 no admitida')
        if adr['scope'] not in c['scopes']:
            e.append('FG-12: alcance del ADR no admitido')
        if not safe_doc_path(adr['path']):
            e.append('FG-12: ruta del ADR inválida')
        else:
            data = ctx['repo_files'].get(adr['path'])
            if not isinstance(data, bytes):
                e.append('FG-12: el ADR sucesor no existe en el repositorio')
            elif sha256(data) != adr['sha256']:
                e.append('FG-12: SHA-256 del ADR distinto del declarado')
            else:
                text = data.decode('utf-8', 'replace')
                if not (isinstance(adr['id'], str) and adr['id'] in text and 'F36-SBX' in text and 'ADR-005' in text):
                    e.append('FG-12: el ADR no corresponde a este contexto (su id, F36-SBX y ADR-005)')
        if set(need) - set(cov):
            e.append(f'FG-12: el ADR no cubre {sorted(set(need) - set(cov))}')
    d09 = ev.get('ei09_decision')
    if d09 not in c['ei09_decisions']:
        e.append('FG-12: falta la decisión explícita sobre EI-09')
    elif 'EI-09' in auth and d09 != c['ei09_passing_decision']:
        e.append(f'FG-12: EI-09 autorizada sin la decisión {c["ei09_passing_decision"]}')
    return e + approval_errors('FG-12', ev, ctx, cdate, rdate)


SPECIFIC = {'FG-02': fg02_errors, 'FG-03': fg03_errors, 'FG-10': fg10_errors, 'FG-12': fg12_errors}


def team_evidence_errors(fg, ctx):
    """Errores semánticos de la evidencia de un criterio de EQUIPO. Lista vacía = evidencia válida."""
    sch, state = ctx.get('schema'), ctx['state']
    if not isinstance(sch, dict):
        return [f'{fg}: esquema de evidencia no verificado (falla cerrado)']
    path = sch['evidence_paths'][fg]
    crit = next((c for c in state.get('criteria') or [] if isinstance(c, dict) and c.get('id') == fg), {})
    e = []
    if crit.get('evidence') != path:
        e.append(f'{fg}: el estado del gate debe citar exactamente {path}')
    ev = json_bytes(ctx['evidence'].get(path))
    if not isinstance(ev, dict) or not ev:
        return e + [f'{fg}: {path} no existe, está vacío, no es JSON o tiene claves duplicadas']
    expected = set(sch['common_fields']) | set(sch['criteria'][fg]['fields'])
    if set(ev) != expected:
        return e + [f'{fg}: campos distintos del esquema: faltan {sorted(expected - set(ev))}, '
                    f'sobran {sorted(set(ev) - expected)}']
    if ev['schema'] != sch['schema_tag'] or ev['criterion_id'] != fg or ev['gate_id'] != sch['gate_id'] \
            or ev['gate_version'] != sch['gate_version']:
        e.append(f'{fg}: esquema, criterio, gate o versión distintos (evidencia de otro contexto)')
    cand = ev['candidate_commit']
    if cand != state.get('candidate_commit'):
        e.append(f'{fg}: candidate_commit distinto del candidato declarado en el estado del gate')
    e += [f'{fg}: {x}' for x in binding_errors(cand, ctx['facts'], ctx['gate_doc'])]
    if not (isinstance(ev['record_id'], str) and re.fullmatch(sch['record_id_pattern'], ev['record_id'])
            and ev['record_id'].startswith(f'F36SBX-{fg}-')):
        e.append(f'{fg}: record_id inválido')
    cdate = parse_date((ctx['facts'].get(cand) or {}).get('date')) if isinstance(cand, str) else None
    rdate = parse_date(ev['recorded_at'])
    if rdate is None:
        e.append(f'{fg}: recorded_at no es una fecha válida')
    elif cdate is not None and rdate < cdate:
        e.append(f'{fg}: recorded_at anterior al commit candidato')
    return e + SPECIFIC[fg](ev, ctx, cdate, rdate)


def evaluate_gate(state, classes, team_errors):
    """Regla de decisión del F36-SBX-GATE. Cualquier situación no prevista devuelve NO SUPERADO."""
    no = 'NO SUPERADO'
    if not isinstance(state, dict):
        return no
    if state.get('revocation') is not None:
        return 'REVOCADO'
    if state.get('authorizes') != ['F37-SBX']:
        return no
    crit = state.get('criteria')
    if not isinstance(crit, list) or not all(isinstance(c, dict) for c in crit) \
            or [c.get('id') for c in crit] != FG_IDS:
        return no
    st = {c['id']: c.get('status') for c in crit}
    for fg, v in st.items():
        admitted = (TEAM_STATUSES | ({'NO APLICA'} if fg in FG_NA_ALLOWED else set())) if fg in FG_TEAM \
            else AUTO_STATUSES
        if v not in admitted:
            return no
    auth = state.get('f37_authorized_ei')
    if auth is not None:
        if not isinstance(auth, list) or not auth or len({str(x) for x in auth}) != len(auth):
            return no
        if any(classes.get(x) not in ('ALLOWED', 'CONDITIONAL') for x in auth):
            return no
    for fg in FG_TEAM:
        if st[fg] == 'CUMPLE':
            try:
                if team_errors(fg):
                    return no
            except Exception:  # noqa: BLE001 — una evidencia no evaluable nunca supera el gate
                return no
    conditional = auth is not None and any(classes.get(x) == 'CONDITIONAL' for x in auth)
    for fg, v in st.items():
        if v == 'NO APLICA':
            if st['FG-03'] != 'CUMPLE' or auth is None or conditional:
                return no
        elif v != 'CUMPLE':
            return no
    if auth is None or not isinstance(state.get('candidate_commit'), str):
        return no
    return 'SUPERADO'


def rule_gate(s, auto):
    out = []
    state = strict_json(s['texts'].get(GATE_STATE) or '')
    if not isinstance(state, dict):
        return [(False, 'estado del gate: JSON inválido o con claves duplicadas (falla cerrado)')], 'NO SUPERADO'
    out.append((set(state) == GATE_KEYS, f'estado del gate con esquema cerrado; diferencias: '
                                         f'{sorted(set(state) ^ GATE_KEYS)}'))
    out.append((state.get('gate_id') == 'F36-SBX-GATE' and state.get('gate_version') == '2'
                and state.get('base_commit') == BASE and state.get('team_evidence_schema') == 'f36sbx-team-evidence/v1',
                'identidad, versión, base y esquema de evidencia del gate'))
    ca = state.get('cannot_authorize')
    scope_ok = state.get('authorizes') == ['F37-SBX'] and isinstance(ca, list) and set(ca) == CANNOT_AUTHORIZE \
        and len(ca) == len(CANNOT_AUTHORIZE)
    out.append((scope_ok, 'el gate solo autoriza F37-SBX y declara la lista cerrada de lo que no puede autorizar'))
    schema = strict_json(s['texts'].get(TEAM_SCHEMA) or '')
    schema_ok = isinstance(schema, dict) and sha256(canonical(schema)) == TEAM_SCHEMA_SHA256
    out.append((schema_ok, 'esquema de evidencia EQUIPO idéntico a la versión cerrada f36sbx-team-evidence/v1'))
    serr = team_schema_errors(schema)
    out.append((not serr, f'invariantes del esquema de evidencia EQUIPO; errores: {serr}'))
    crit = state.get('criteria') if isinstance(state.get('criteria'), list) else []
    struct = []
    if [c.get('id') if isinstance(c, dict) else None for c in crit] != FG_IDS:
        struct.append('los criterios deben ser exactamente FG-01..FG-14, en orden')
    for c in crit:
        if not isinstance(c, dict):
            continue
        fg, team = c.get('id'), c.get('id') in FG_TEAM
        keys = {'id', 'kind', 'status', 'evidence'} if team else {'id', 'kind', 'status'}
        if set(c) != keys or c.get('kind') != ('team' if team else 'auto'):
            struct.append(f'{fg}: claves o tipo distintos ({"EQUIPO" if team else "AUTO"})')
        admitted = (TEAM_STATUSES | ({'NO APLICA'} if fg in FG_NA_ALLOWED else set())) if team else AUTO_STATUSES
        if c.get('status') not in admitted:
            struct.append(f'{fg}: estado {c.get("status")!r} no admitido para este criterio')
        if team and c.get('status') != 'CUMPLE' and c.get('evidence') is not None:
            struct.append(f'{fg}: solo un criterio en CUMPLE cita evidencia')
    out.append((not struct, f'criterios cerrados: tipos, claves, estados admitidos y evidencia; errores: {struct}'))
    computed_auto = {
        'FG-01': all(auto.values()), 'FG-04': auto['GOV'], 'FG-05': auto['FRZ'], 'FG-06': auto['CAP'],
        'FG-07': auto['CTR'], 'FG-08': auto['THR'], 'FG-09': auto['EVA'], 'FG-11': auto['CAP'] and auto['SEM'],
        'FG-13': scope_ok, 'FG-14': state.get('revocation') is None,
    }
    status = {c.get('id'): c.get('status') for c in crit if isinstance(c, dict)}
    mismatch = [fg for fg, ok in computed_auto.items() if status.get(fg) != ('CUMPLE' if ok else 'NO CUMPLE')]
    out.append((not mismatch, f'los criterios AUTO declarados coinciden con los recalculados; difieren: {mismatch}'))
    cand = state.get('candidate_commit')
    cumple = [fg for fg in FG_TEAM if status.get(fg) == 'CUMPLE']
    if cand is None:
        cand_err = [f'{cumple} en CUMPLE sin candidate_commit'] if cumple else []
    else:
        cand_err = binding_errors(cand, s['facts'], s['texts'].get(GATE_DOC))
    out.append((not cand_err, f'vínculo con el commit candidato auditado (nulo mientras no haya evidencia); '
                              f'errores: {cand_err}'))
    ctx = {'state': state, 'schema': schema if schema_ok and not serr else None, 'evidence': s['evidence'],
           'facts': s['facts'], 'repo_files': s['repo_files'], 'classes': EXPECTED_CLASSES,
           'gate_doc': s['texts'].get(GATE_DOC)}

    def team_errors(fg):
        return team_evidence_errors(fg, ctx)
    invalid = {}
    for fg in cumple:
        try:
            errs = team_errors(fg)
        except Exception as exc:  # noqa: BLE001 — cualquier error de evaluación falla cerrado
            errs = [f'{fg}: evidencia no evaluable ({exc.__class__.__name__}, falla cerrado)']
        if errs:
            invalid[fg] = errs
    out.append((not invalid, f'cada criterio EQUIPO en CUMPLE tiene evidencia semánticamente válida; '
                             f'inválidas: {invalid}'))
    referenced = {f'{GATE_EVIDENCE}{fg}.json' for fg in cumple}
    fg02 = json_bytes(s['evidence'].get(f'{GATE_EVIDENCE}FG-02.json'))
    if 'FG-02' in cumple and isinstance(fg02, dict) and isinstance(fg02.get('audit_report'), dict):
        referenced.add(fg02['audit_report'].get('path'))
    stray = sorted(p for p in s['evidence'] if p not in referenced)
    unreadable = sorted(p for p, b in s['evidence'].items() if not isinstance(b, bytes))
    out.append((not stray and not unreadable, f'gate/evidencia/ solo contiene evidencia citada y archivos regulares; '
                                              f'sin citar: {stray}; enlaces o ilegibles: {unreadable}'))
    auth = state.get('f37_authorized_ei')
    auth_err = []
    if auth is not None:
        if not isinstance(auth, list) or not auth or len({str(x) for x in auth}) != len(auth) \
                or any(EXPECTED_CLASSES.get(x) not in ('ALLOWED', 'CONDITIONAL') for x in auth):
            auth_err.append(f'f37_authorized_ei solo admite una lista de EI ALLOWED o CONDITIONAL: {auth}')
        if status.get('FG-03') != 'CUMPLE':
            auth_err.append('f37_authorized_ei declarada sin FG-03 en CUMPLE')
    out.append((not auth_err, f'autorización de F37-SBX coherente con la matriz y con FG-03; errores: {auth_err}'))
    result = evaluate_gate(state, EXPECTED_CLASSES, team_errors)
    if result == 'SUPERADO' and (mismatch or struct or cand_err or invalid or not schema_ok or serr):
        result = 'NO SUPERADO'
    out.append((state.get('declared_result') == result,
                f'resultado declarado {state.get("declared_result")!r} = recalculado {result!r}'))
    doc = norm(s['texts'].get(GATE_DOC) or '')
    rows = {r[0]: r for r in table_rows(doc, 'FG-')}
    doc_err = []
    for c in crit:
        if not isinstance(c, dict):
            continue
        r = rows.get(c.get('id'))
        if not r or len(r) != 5:
            doc_err.append(f'{c.get("id")}: sin fila')
        elif r[2] != ('EQUIPO' if c.get('kind') == 'team' else 'AUTO') or r[4] != c.get('status'):
            doc_err.append(f'{c.get("id")}: tipo o estado distinto del JSON')
    out.append((not doc_err and sorted(rows) == FG_IDS, f'tabla FG del documento = JSON; diferencias: {doc_err}'))
    phrase = f'F36-SBX-GATE = {result}'
    where = [rel for rel in [GATE_DOC, f'{PKG}/README.md'] if phrase not in norm(s['texts'].get(rel) or '')]
    out.append((not where, f'«{phrase}» declarado en el gate y en el README; falta en: {where}'))
    out.append((result == 'NO SUPERADO', f'el gobierno de esta versión exige F36-SBX-GATE = NO SUPERADO; '
                                         f'el gate da {result}'))
    return out, result


RULES = [('STR', rule_str), ('LNK', rule_lnk), ('GOV', rule_gov), ('SEM', rule_sem), ('CAP', rule_cap),
         ('CTR', rule_ctr), ('THR', rule_thr), ('EVA', rule_eva), ('FRZ', rule_frz), ('DEP', rule_dep),
         ('PII', rule_pii)]


def run(s):
    """Devuelve [(regla, ok, mensaje)] y el resultado del gate."""
    results, auto = [], {}
    for name, fn in RULES:
        checks = fn(s)
        auto[name] = all(ok for ok, _ in checks)
        results += [(name, ok, msg) for ok, msg in checks]
    gate_checks, gate = rule_gate(s, auto)
    results += [('GATE', ok, msg) for ok, msg in gate_checks]
    return results, gate


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    s = collect(ROOT)
    results, gate = run(s)
    fails = [r for r in results if not r[1]]
    for name, ok, msg in results:
        print(f'{"OK   " if ok else "FALLA"} {name}: {msg}')
    print(f'INFO F36-SBX-GATE = {gate} · rama {s["branch"]} · base {BASE[:7]}')
    print(f'validate_f36sbx: {len(results) - len(fails)} comprobaciones correctas, {len(fails)} fallas')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
