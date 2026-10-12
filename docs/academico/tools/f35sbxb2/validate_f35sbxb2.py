"""F35-SBX-B — B2: gate sucesor sobre HEAD (validate_f35sbxb2.py).

Uso:  python -I docs/academico/tools/f35sbxb2/validate_f35sbxb2.py      (si se invoca sin -I, se relanza aislado)

Contrato: docs/academico/evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md (versión 2.1) y el diseño
F35SBXB_B2_Diseno_Almacen.md. Código de desarrollo NO AUDITADO (Q6): un PASS de desarrollo no equivale a confianza
ni a cierre; lo acredita la auditoría independiente.

  CTX  rama de B2, develop o main; aislado (python -I) y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; E, el cierre de
       B0, el ancla y el cierre de B1 y la base de B2 como ancestros de HEAD; historia no superficial.
  B1F  conjunto auditado de B1 desde 8e94a60 y del cierre desde 3d9b783, en cada commit de la ascendencia; transición
       única y monotónica de gobierno (reglas 1 a 4 de §2.3); estado efectivo en árbol, índice y disco (P25, P32, P33,
       con historias en repositorios desechables).
  AIN, B0F, HST, SBX, FLG   reglas del gate de B1, cargado desde los bytes verificados contra su ancla (Q5).
  SCP  delta exacto respecto de 72e86c5 (§2.5) en HEAD, árbol de trabajo, índice y archivos sin seguimiento.
  FSY  FSY de B1 (runtime, dataset y evidencia byte a byte; carpetas de B1), carpetas de B1-FREEZE y de B2 exactas,
       ningún archivo de base de datos SQLite en el repositorio y ningún enlace.
  DEP  almacén: sqlite3, csv, hashlib, json, re, unicodedata y os.path; gate: las del gate de B1; nadie más usa el almacén.
  PRE  entorno del preflight (SQLite 3.37 o posterior realmente cargado, API y PRAGMA efectivos) antes de DYN.
  STA  el almacén antes de ejecutarlo: catálogo, DDL con doble llave frente al contrato de A, origen frente al
       manifiesto F34, conexión, API, módulo y referencias (§2.4).
  DYN  P01..P33 en proceso desde los mismos bytes analizados, bajo la guarda de B1.4 y en un directorio temporal.
  DET, ISO, PUR, DAT   agrupaciones de casos de §2.2.
  CAP  P17 y P18, más el contenido de los archivos de B2 con la semántica de B1.
  GOV  trece estados exactos y gobierno igual al blob histórico de B1 o al nuevo de B2, sin declaraciones
       contradictorias ni afirmaciones que habiliten capacidades.
  NB2  negativos: mutaciones del almacén y del estado del repositorio que el gate debe detectar.

Todo error o estado no evaluable falla cerrado. El repositorio real nunca se modifica: los casos de historia usan
repositorios desechables fuera de él.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación, como en B1.4: python -I, relanzado con os.spawnv.
if __name__ == '__main__' and not sys.flags.isolated:
    _argv = [sys.executable, '-I', '-B'] + (['-X', 'utf8'] if sys.flags.utf8_mode else []) + \
        [os.path.abspath(__file__)] + sys.argv[1:]
    if os.name == 'nt':
        _argv = ['"' + a.replace('"', '\\"') + '"' if (' ' in a or '\t' in a) else a for a in _argv]
    sys.exit(os.spawnv(os.P_WAIT, sys.executable, _argv))

_REPO = os.path.normcase(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..')))
sys.path[:] = [p for p in sys.path if not (os.path.normcase(os.path.abspath(p or os.curdir)) + os.sep).startswith(
    _REPO + os.sep)]
sys.dont_write_bytecode = True
sys.pycache_prefix = os.path.join(os.path.abspath(__file__), 'sin-pyc')

import ast  # noqa: E402
import copy  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import unicodedata  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
B1_ANCHOR = '8e94a60274fe39ebda3e9961bc58036b389dfc00'     # AUDITED_B1_ANCHOR
B1_GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
B1_GATE_MODULE = 'f35sbxb_gate_b1_verificado'
STORE = 'docs/academico/tools/f35sbxb2/sbxb_store.py'
GATE2 = 'docs/academico/tools/f35sbxb2/validate_f35sbxb2.py'
A_CONTRACT = 'docs/academico/evidencia-sbx/contrato/f35sbx_contract.json'
A_FIXTURES = {org: f'docs/academico/evidencia-sbx/fixtures/{org}_evidencias.json' for org in ('ORG-S1', 'ORG-S2', 'ORG-S3')}
F34_DIR = 'docs/academico/datos-sinteticos/dataset'
F34_MANIFEST = F34_DIR + '/manifest.json'
F34_NAMES = ('evidence', 'criteria', 'vacancies', 'applications')
TENANTS = ('ORG-S1', 'ORG-S2', 'ORG-S3')

# ---------------------------------------------------------------- historia, alcance y gobierno (§2.2, §2.3 y §2.5)
E = '61f94e23fc30b00a848a4558830b6d65f81dff87'            # cierre endurecido de F35-SBX-A
B0_CLOSE = 'cc634eb9dcc5c0cc0d77b911bb3815182b8319c2'     # cierre auditado de B0
B1_CLOSURE = '3d9b78307684a0dfb093e31d28fde290b2b1cb4a'   # cierre de B1-FREEZE
B1_BASE = '430f3f544c3542cabac8028a122c8a0c2a97390b'      # base de B1 (superficies del runtime de referencia del gate de B1)
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'      # develop al crear la rama de B2 (B1-FREEZE integrada)
B2_BRANCH = 'feature/f35-sbx-b2-ephemeral-store'
BRANCHES = (B2_BRANCH, 'develop', 'main')
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md')
SET_A = GOV_PATHS + ('docs/academico/evidencia-sbx-b/README.md', 'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md',
                     B1_GATE)
SET_B = ('docs/academico/tools/f35sbxb_freeze/validate_f35sbxb_freeze.py',
         'docs/academico/tools/f35sbxb_freeze/b1_freeze_manifest.json',
         'docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md')
B2_DOCS = ('docs/academico/evidencia-sbx-b2/README.md', 'docs/academico/evidencia-sbx-b2/F35SBXB_B2_Diseno_Almacen.md',
           'docs/academico/evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md')
B2_FILES = B2_DOCS + (STORE, GATE2)
# Carpetas con su contenido exacto: las de B1 y B1-FREEZE (B1F, C) y las de B2 (Q2, DH-B2-01).
FOLDERS = {'docs/academico/evidencia-sbx-b': {'docs/academico/evidencia-sbx-b/README.md',
                                              'docs/academico/evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md',
                                              'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md'},
           'docs/academico/tools/f35sbxb': {B1_GATE},
           'docs/academico/evidencia-sbx-b-freeze': {SET_B[2]},
           'docs/academico/tools/f35sbxb_freeze': {SET_B[0], SET_B[1]},
           'docs/academico/evidencia-sbx-b2': set(B2_DOCS),
           'docs/academico/tools/f35sbxb2': {STORE, GATE2}}
# Delta exacto respecto de la base de B2 (§2.5). El gobierno solo cambia mediante la transición única de §2.3.
SCOPE2 = {**{p: 'A' for p in B2_FILES}, **{p: 'M' for p in GOV_PATHS}}
# Delta de gobierno de B2 (Q1, DH-B2-07): lista cerrada de reemplazos literales sobre el blob de cada ruta en el ancla
# de B1. Cada bloque antiguo aparece exactamente una vez; el gate calcula así los bytes del blob nuevo.
_B2_SENTENCE_1 = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E '
                  'INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, sin '
                  'pipeline funcional ni ML.')
_B2_SENTENCE_2 = ('F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en '
                  '`develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre '
                  '`3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`]'
                  '({root}evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está '
                  'IMPLEMENTADO y es CANDIDATO A AUDITORÍA INDEPENDIENTE, en `feature/f35-sbx-b2-ephemeral-store` y '
                  'registrado en [`evidencia-sbx-b2`]({root}evidencia-sbx-b2/README.md). Su integración y su publicación '
                  'requieren autorización explícita del equipo.')
_B1_SENTENCE_1 = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) en desarrollo, sin '
                  'pipeline funcional, SQLite ni ML.')
_B1_SENTENCE_2 = ('F35-SBX-B INICIADA en `feature/f35-sbx-b-deterministic-pipeline`; su incremento B1 (gate sucesor '
                  'sobre HEAD) se entrega PENDIENTE DE AUDITORÍA.')
GOVERNANCE_DELTA = {
    'CLAUDE.md': [(_B1_SENTENCE_1, _B2_SENTENCE_1),
                  (_B1_SENTENCE_2, _B2_SENTENCE_2.format(root='docs/academico/'))],
    'docs/PROGRESS.md': [
        ('Última actualización: 2026-10-09 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
         'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA, B1 '
         'en desarrollo).',
         'Última actualización: 2026-10-12 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
         'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: '
         'B1 CERRADA E INTEGRADA, B2 IMPLEMENTADA Y CANDIDATA A AUDITORÍA INDEPENDIENTE).'),
        ('el mismo día, al inicio de F35-SBX-B con B0 cerrada e integrada.',
         'el mismo día, al inicio de F35-SBX-B con B0 cerrada e integrada. El 12/10/2026 pasó de «B1 en desarrollo» '
         'a B1 cerrada e integrada y B2 implementada, candidata a auditoría independiente.'),
        (_B1_SENTENCE_1, _B2_SENTENCE_1),
        (_B1_SENTENCE_2, _B2_SENTENCE_2.format(root='academico/'))]}
# Commit de la transición de gobierno. Se registra después de que exista, nunca en el propio commit (§2.3).
B2_GOVERNANCE_TRANSITION = None

# ---------------------------------------------------------------- esquema esperado, derivado por el gate (doble llave)
TABLE_ENTITY = (('tenant_context', 'SyntheticTenantContext', 'synthetic_organization_id'),
                ('pipeline_run', 'SyntheticPipelineRun', 'pipeline_run_id'),
                ('pipeline_event', 'SyntheticPipelineEvent', 'event_id'),
                ('evidence_source', 'SyntheticEvidenceSource', 'source_id'),
                ('evidence_record', 'SyntheticEvidenceRecord', 'synthetic_id'),
                ('evidence_provenance', 'SyntheticEvidenceProvenance', 'provenance_id'),
                ('simulated_review', 'SyntheticHumanReview', 'review_id'),
                ('audit_entry', 'SyntheticAuditEntry', 'audit_id'))
ORG_TABLES = ('pipeline_run', 'evidence_source', 'evidence_record', 'evidence_provenance', 'simulated_review',
              'audit_entry')
# Valores propios de B (diseño §5) y límites que salen de los contratos de entrada (Q9).
B_CONST = {'run_kind': 'ejecucion_sbx_b', 'pipeline_version': 'f35sbxb-0', 'contract_version': 'f35sbxb-contract-1.0.0'}
B_LIMITS = {'seq': 7}
B_ORDINAL = {'V': '-0[1-7]', 'A': '-0[1-8]'}
FOREIGN = {('pipeline_run', 'synthetic_organization_id'): ('tenant_context', 'synthetic_organization_id'),
           ('pipeline_event', 'pipeline_run_id'): ('pipeline_run', 'pipeline_run_id'),
           ('evidence_source', 'synthetic_organization_id'): ('tenant_context', 'synthetic_organization_id'),
           ('evidence_record', 'synthetic_organization_id'): ('tenant_context', 'synthetic_organization_id'),
           ('evidence_record', 'pipeline_run_id'): ('pipeline_run', 'pipeline_run_id'),
           ('evidence_record', 'source_id'): ('evidence_source', 'source_id'),
           ('evidence_provenance', 'record_id'): ('evidence_record', 'synthetic_id'),
           ('evidence_provenance', 'synthetic_organization_id'): ('tenant_context', 'synthetic_organization_id'),
           ('evidence_provenance', 'source_id'): ('evidence_source', 'source_id'),
           ('evidence_provenance', 'pipeline_run_id'): ('pipeline_run', 'pipeline_run_id'),
           ('evidence_provenance', 'review_id'): ('simulated_review', 'review_id'),
           ('simulated_review', 'record_id'): ('evidence_record', 'synthetic_id'),
           ('simulated_review', 'pipeline_run_id'): ('pipeline_run', 'pipeline_run_id'),
           ('simulated_review', 'synthetic_organization_id'): ('tenant_context', 'synthetic_organization_id'),
           ('audit_entry', 'pipeline_run_id'): ('pipeline_run', 'pipeline_run_id'),
           ('audit_entry', 'synthetic_organization_id'): ('tenant_context', 'synthetic_organization_id'),
           ('audit_entry', 'target_ref'): ('pipeline_run', 'pipeline_run_id')}
UNIQUE = {('evidence_source', 'origin_record_id'), ('evidence_record', 'source_id'),
          ('evidence_provenance', 'record_id'), ('evidence_provenance', 'review_id'), ('simulated_review', 'record_id')}
TABLE_CHECKS = {'pipeline_event': ["CHECK (event_id GLOB ('*-0' || seq))", "CHECK ((state = 'fallido') = (error_code <> ''))"],
                'audit_entry': ['CHECK (target_ref = pipeline_run_id)']}
TS_RX = '^20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$'
TS_GLOB = '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
TEXT_MARKER = '[SINTÉTICO] '
TRIGGERS = sorted([f'{t}_no_update' for t, _, _ in TABLE_ENTITY] + [f'{t}_no_delete' for t, _, _ in TABLE_ENTITY] +
                  [f'{t}_tenant' for t in ORG_TABLES] +
                  ['tenant_context_single', 'pipeline_run_single', 'pipeline_event_order', 'pipeline_event_chain',
                   'pipeline_event_terminal', 'evidence_provenance_chain', 'audit_entry_chain'])
API = {'open_tenant_store': ('tenant',), 'create_run': ('store', 'seed', 'clock_start'),
       'append_event': ('store', 'state', 'at', 'error_code', 'audit_action'), 'append_evidence': ('store', 'evidence'),
       'append_audit': ('store', 'action', 'at'), 'read_run': ('store',), 'list_events': ('store',),
       'list_audit': ('store',), 'list_evidence': ('store',), 'current_state': ('store',), 'snapshot': ('store',),
       'preflight_report': ('store',), 'diagnostic': ('store',), 'purge': ('store',)}
API_CLASSES = frozenset({'TenantRunStore', 'SbxbStoreError'})
STORE_IMPORTS = frozenset({'csv', 'hashlib', 'json', 'os', 're', 'sqlite3', 'unicodedata'})
GATE_IMPORTS = frozenset({'ast', 'copy', 'hashlib', 'importlib', 'json', 'os', 're', 'subprocess', 'sys', 'unicodedata'})
OS_ALLOWED = frozenset({'os.path.join', 'os.path.dirname', 'os.path.abspath'})
FORBIDDEN_ATTRS = frozenset({'backup', 'serialize', 'deserialize', 'iterdump', 'enable_load_extension', 'load_extension',
                             'enable_shared_cache', 'create_function', 'create_aggregate', 'create_collation',
                             'create_window_function', 'set_progress_handler', 'set_trace_callback', 'blobopen'})
FORBIDDEN_BUILTINS = frozenset({'getattr', 'setattr', 'delattr', 'globals', 'locals', 'vars', '__import__', 'exec',
                                'eval', 'compile', 'breakpoint', 'input', 'memoryview', '__builtins__'})
FORBIDDEN_MODULE_NAMES = frozenset({'time', 'datetime', 'random', 'uuid', 'secrets', 'socket', 'urllib', 'http',
                                    'subprocess', 'importlib', 'io', 'pathlib', 'shutil', 'tempfile', 'sys'})
PREFLIGHT_SQL = frozenset({'PRAGMA foreign_keys = ON', 'PRAGMA foreign_keys', 'PRAGMA recursive_triggers = ON',
                           'PRAGMA recursive_triggers', 'PRAGMA temp_store = MEMORY', 'PRAGMA temp_store',
                           'PRAGMA trusted_schema = OFF', 'PRAGMA trusted_schema', 'PRAGMA journal_mode',
                           "SELECT name FROM sqlite_schema WHERE type = 'trigger' ORDER BY name"} |
                          {f'PRAGMA table_info({t})' for t, _, _ in TABLE_ENTITY})
RUNTIME_FORBIDDEN = re.compile(r'\b(REPLACE|IGNORE|CONFLICT|UPDATE|DELETE|ATTACH|DETACH|VACUUM|ALTER|DROP|CREATE|ROWID|'
                               r'UPSERT|PRAGMA|RANDOM|DATETIME|JULIANDAY|STRFTIME|CURRENT_\w+)\b', re.I)
DDL_FORBIDDEN = re.compile(r'\b(ATTACH|DETACH|PRAGMA|VACUUM|ALTER|DROP|INSERT|REPLACE|CONFLICT|IGNORE|TEMP|TEMPORARY|'
                           r'VIRTUAL|AUTOINCREMENT|ROWID|VIEW|INDEX|load_extension|random|datetime|CURRENT_\w+)\b', re.I)
SQL_WORDS = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|PRAGMA|ATTACH|DETACH|CREATE|DROP|REPLACE|VACUUM)\b')
FORBIDDEN_REFS = re.compile(r'(app/|database/|routes/|artisan|\.env\b|pgsql|postgres|redis|mysql)', re.I)
PROHIBITED_NAMES = re.compile(r'score|rank|recommend|recomend|best|mejor|select|selecci|hire|contrat|ocr|pars|extract|'
                              r'embedding|vector|semantic|llm|personal|emoci|emotion|biometr|risk|riesgo|predict', re.I)
# Detectores de A §5 (copia propia del gate): defensa adicional del contenido, no la garantía.
PII = (re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), re.compile(r'https?://|www\.', re.I),
       re.compile(r'(?<![\w-])\d{11}(?![\w-])'), re.compile(r'(?<![\w-])\d{8}(?![\w-])'),
       re.compile(r'(?<![\w-])\+?\d[\d ]{8,}\d(?![\w-])'), re.compile(r'data:[\w.+/-]*;base64', re.I),
       re.compile(r'[A-Za-z0-9+/]{40,}={0,2}'))


class CaseFail(Exception):
    pass


class GitError(Exception):
    pass


def git(*args, cwd=None):
    try:
        p = subprocess.run(['git', *args], cwd=cwd or ROOT, capture_output=True)
    except OSError as e:
        raise GitError(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(args[:3])} → {p.returncode}: {p.stderr.decode("utf-8", "replace").strip()[:120]}')
    return p.stdout


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def no_link(rel, root=None):
    parts = rel.split('/')
    return not any(os.path.islink(os.path.join(root or ROOT, *parts[:k])) for k in range(1, len(parts) + 1))


def real_bytes(rel, root=None):
    full = os.path.join(root or ROOT, *rel.split('/'))
    if not no_link(rel, root) or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def read_json(rel):
    data = real_bytes(rel)
    if data is None:
        raise ValueError(f'{rel}: ilegible')
    return json.loads(data.decode('utf-8'))


# ---------------------------------------------------------------- carga verificada del gate de B1 (principio F de B0)
def load_b1_gate():
    """Gate de B1 desde los bytes del ancla, sin releer el archivo; None si no coincide (falla cerrado)."""
    meta = git('ls-tree', B1_ANCHOR, '--', B1_GATE).decode().split('\t')[0].split()
    data = real_bytes(B1_GATE)
    if len(meta) != 3 or meta[:2] != ['100644', 'blob'] or data is None or blob_id(data) != meta[2]:
        return None
    path = os.path.join(ROOT, *B1_GATE.split('/'))
    spec = importlib.util.spec_from_file_location(B1_GATE_MODULE, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[B1_GATE_MODULE] = module
    exec(compile(data, path, 'exec', dont_inherit=True), module.__dict__)
    return module


# ---------------------------------------------------------------- B1F: historia de B1 y transición de gobierno (§2.3)
class Repo:
    """Lectura de un repositorio Git, el real o uno desechable, con caché por commit. No escribe en el real."""

    def __init__(self, cwd, env=None):
        self.cwd, self.env, self.cache = cwd, env, {}

    def call(self, *args, data=None):
        try:
            p = subprocess.run(['git', *args], cwd=self.cwd, capture_output=True, env=self.env, input=data)
        except OSError as e:
            raise GitError(f'git no ejecutable ({e.__class__.__name__})')
        return p.returncode, p.stdout

    def run(self, *args, data=None):
        rc, out = self.call(*args, data=data)
        if rc != 0:
            raise GitError(f'git {" ".join(args[:3])} → {rc}')
        return out

    def entries(self, commit, paths):
        """{ruta: (modo, tipo, blob)} de las rutas pedidas en un commit (identificado por su hash)."""
        key = ('ls-tree', commit, paths)
        if key not in self.cache:
            found = {}
            for entry in self.run('ls-tree', '-z', commit, '--', *paths).split(b'\x00'):
                if entry:
                    meta, _, path = entry.partition(b'\t')
                    found[path.decode('utf-8', 'replace')] = tuple(meta.decode().split())
            self.cache[key] = found
        return self.cache[key]

    def is_ancestor(self, older, newer):
        key = ('ancestor', older, newer)
        if key not in self.cache:
            rc, _ = self.call('merge-base', '--is-ancestor', older, newer)
            if rc not in (0, 1):
                raise GitError(f'merge-base --is-ancestor → {rc}')
            self.cache[key] = rc == 0
        return self.cache[key]

    def graph(self, base, head):
        """{commit: [padres]} de git rev-list --ancestry-path base..head, merges incluidos, en orden topológico."""
        out = {}
        for line in self.run('rev-list', '--topo-order', '--parents', '--ancestry-path', f'{base}..{head}').decode().splitlines():
            ids = line.split()
            if not ids or not all(re.fullmatch(r'[0-9a-f]{40}', x) for x in ids):
                raise GitError('historia no verificable')
            out[ids[0]] = ids[1:]
        return out


def governance_new(repo, anchor, delta):
    """Bytes del blob nuevo de B2 en cada ruta de gobierno: el delta cerrado aplicado al blob histórico del ancla, con
    cada bloque antiguo presente exactamente una vez. ({ruta: bytes}, problemas)."""
    found, problems = {}, []
    old = repo.entries(anchor, GOV_PATHS)
    for path in GOV_PATHS:
        meta = old.get(path)
        if meta is None or meta[:2] != ('100644', 'blob'):
            problems.append(f'{path}: sin blob histórico regular en el ancla')
            continue
        text = repo.run('cat-file', 'blob', meta[2]).decode('utf-8')
        blocks = delta.get(path) or []
        if not blocks or any(text.count(before) != 1 for before, _ in blocks):
            problems.append(f'{path}: delta vacío o con un bloque antiguo que no aparece exactamente una vez')
            continue
        for before, after in blocks:
            text = text.replace(before, after, 1)
        found[path] = text.encode('utf-8')
    return found, problems


def effective_state(repo, root, expected):
    """Árbol de HEAD, índice (etapa 0, sin flags) y disco (archivo regular, sin enlaces) con el blob admitido."""
    out, paths = [], tuple(expected)
    tree = repo.entries(repo.run('rev-parse', '--verify', 'HEAD^{commit}').decode().strip(), paths)
    index = {}
    for entry in repo.run('ls-files', '-s', '-v', '-z', '--', *paths).split(b'\x00'):
        if entry:
            meta, _, path = entry.partition(b'\t')
            index.setdefault(path.decode('utf-8', 'replace'), []).append(tuple(meta.decode().split()))
    for path, want in expected.items():
        if tree.get(path) != want:
            out.append(f'{path}: árbol de HEAD distinto del blob admitido')
        if index.get(path) != [('H', want[0], want[2], '0')]:
            out.append(f'{path}: índice distinto del blob admitido, con flags o en conflicto')
        data = real_bytes(path, root)
        if data is None or blob_id(data) != want[2]:
            out.append(f'{path}: disco distinto del blob admitido, enlace o ausente')
    return out


def b1f_check(repo, anchor, closure, delta, registered, head='HEAD', root=None):
    """B1F (§2.3): conjunto auditado de B1 desde su ancla, conjunto del cierre desde el suyo y transición única y
    monotónica de gobierno, en cada commit de la ascendencia (merges incluidos). Con head = HEAD comprueba además el
    estado efectivo en root. Devuelve (problemas, transición derivada o None, commits revisados)."""
    out = []
    want_a, want_b = repo.entries(anchor, SET_A), repo.entries(closure, SET_B)
    for label, want, paths in (('auditado de B1', want_a, SET_A), ('del cierre de B1-FREEZE', want_b, SET_B)):
        if set(want) != set(paths) or any(m[:2] != ('100644', 'blob') for m in want.values()):
            out.append(f'conjunto {label} incompleto o con modo o tipo inesperado en su ancla')
    new_bytes, problems = governance_new(repo, anchor, delta)
    out += problems
    if out:
        return out, None, 0
    old = {p: want_a[p] for p in GOV_PATHS}
    new = {p: ('100644', 'blob', blob_id(new_bytes[p])) for p in GOV_PATHS}
    graph = repo.graph(anchor, head)

    def gov(commit):
        found = repo.entries(commit, SET_A)
        return {p: found.get(p) for p in GOV_PATHS}
    # Regla 4: un único commit introduce el blob nuevo, es decir, lo contiene sin que lo contenga ninguno de sus padres.
    introduced = {}
    for commit in reversed(list(graph)):            # de los más antiguos a los más recientes
        for p in GOV_PATHS:
            if gov(commit)[p] == new[p] and not any(gov(q)[p] == new[p] for q in graph[commit]):
                introduced.setdefault(commit, set()).add(p)
    full = [c for c, paths in introduced.items() if paths == set(GOV_PATHS)]
    transition = full[0] if full else None
    others = [c[:12] for c in introduced if c != transition]
    if others:
        out.append(f'regla 4: introducción del blob nuevo de gobierno fuera de la transición única: {others}')
    # Regla 2: la transición tiene un solo padre, con el blob histórico, y solo cambia las dos rutas de gobierno.
    if transition is not None:
        parents = graph[transition]
        if len(parents) != 1:
            out.append(f'regla 2: la transición {transition[:12]} no tiene un solo padre')
        elif gov(parents[0]) != old:
            out.append(f'regla 2: el padre de la transición {transition[:12]} no contiene el blob histórico')
        else:
            changed = {x for x in repo.run('diff-tree', '-r', '--no-renames', '--name-only', '-z', parents[0], transition)
                       .decode('utf-8', 'replace').split('\x00') if x}
            if changed != set(GOV_PATHS):
                out.append(f'la transición {transition[:12]} cambia otras rutas además del gobierno: '
                           f'{sorted(changed ^ set(GOV_PATHS))[:3]}')
    if registered is not None and transition != registered:
        out.append(f'transición derivada ({transition[:12] if transition else "ninguna"}) distinta de la registrada '
                   f'({registered[:12]})')
    # Reglas 1 y 3 y el resto del conjunto auditado, en cada commit: lo admitido depende de su ascendencia.
    for commit in graph:
        found = repo.entries(commit, SET_A)
        moved = [p for p in SET_A if p not in GOV_PATHS and found.get(p) != want_a[p]]
        if moved:
            out.append(f'{commit[:12]}: conjunto auditado de B1 distinto del ancla (modificado, eliminado, renombrado '
                       f'o con otro modo): {moved[:2]}')
        after = transition is not None and (commit == transition or repo.is_ancestor(transition, commit))
        bad = [p for p in GOV_PATHS if found.get(p) != (new if after else old)[p]]
        if bad:
            rule = ('regla 3: descendiente de la transición sin el blob nuevo de B2' if after else
                    'regla 1: commit previo o ajeno a la transición sin el blob histórico de B1')
            out.append(f'{commit[:12]}: {rule}: {bad}')
    # Conjunto del cierre de B1-FREEZE, desde su introducción.
    for commit in repo.graph(closure, head):
        found = repo.entries(commit, SET_B)
        bad = [p for p in SET_B if found.get(p) != want_b[p]]
        if bad:
            out.append(f'{commit[:12]}: conjunto del cierre de B1-FREEZE distinto de {closure[:12]}: {bad[:2]}')
    if head == 'HEAD':
        out += effective_state(repo, root, {**want_a, **(new if transition is not None else old), **want_b})
    return out, transition, len(graph)


# ---------------------------------------------------------------- doble llave: DDL y catálogo esperados desde A
def q(value):
    return "'" + value.replace("'", "''") + "'"


def column_check(name, spec):
    """Restricción del motor que corresponde a la especificación de A del campo, con los valores propios de B."""
    if 'const' in spec:
        value = B_CONST.get(name, spec['const'])
        return f'{name} = 1' if value is True else f'{name} = {q(value)}'
    if 'enum' in spec:
        return f"{name} IN ({', '.join(q(v) for v in spec['enum'] if v != 'purgado')})"
    if spec.get('type') == 'integer':
        return f"{name} BETWEEN {spec['minimum']} AND {B_LIMITS.get(name, spec['maximum'])}"
    pattern = spec.get('pattern') or ''
    if pattern == '^ORG-S[1-3]$':
        return f"{name} GLOB 'ORG-S[1-3]'"
    if pattern == '^SIMREV-ORG-S[1-3]$':
        return f"{name} = 'SIMREV-' || synthetic_organization_id"
    if pattern == TS_RX:
        return f"{name} GLOB '{TS_GLOB}'"
    if pattern == '^[0-9a-f]{64}$':
        return f"length({name}) = 64 AND {name} NOT GLOB '*[^0-9a-f]*'"
    if pattern == '^(|E-[A-Z]{2,12})$':
        return f"{name} = '' OR ({name} GLOB 'E-[A-Z][A-Z]*' AND {name} NOT GLOB 'E-*[^A-Z]*' AND length({name}) <= 14)"
    m = re.fullmatch(r'\^\\\[SINTÉTICO\\\] \[\^<>\\x00-\\x1f\\x7f\]\{(\d+),(\d+)\}\$', pattern)
    if m:
        low, high = len(TEXT_MARKER) + int(m[1]), len(TEXT_MARKER) + int(m[2])
        return f"{name} GLOB '[[]SINTÉTICO] *' AND length({name}) BETWEEN {low} AND {high} AND {name} NOT GLOB '*[<>]*'"
    m = re.fullmatch(r'\^(SYN|CRI)-\[0-9\]\{(\d)\}\$', pattern)
    if m:
        return f"{name} GLOB '{m[1]}-{'[0-9]' * int(m[2])}'"
    m = re.fullmatch(r'\^SBX([RVSEPHA])-ORG-S\[1-3\]-\[0-9\]\{(\d)\}(-\[0-9\]\{2\})?\$', pattern)
    if m:
        glob = f'SBB{m[1]}-ORG-S[1-3]-' + '[0-9]' * 10
        if m[3]:
            glob += B_ORDINAL[m[1]]
        elif m[2] == '6':
            glob += '-' + '[0-9]' * 6
        return f"{name} GLOB '{glob}'"
    raise ValueError(f'{name}: patrón de A sin traducción al esquema de B2')


def expected_tables(contract):
    """CREATE TABLE normalizado de cada tabla, construido solo desde el contrato de A y las decisiones de B2."""
    out = {}
    for table, entity, pk in TABLE_ENTITY:
        lines = []
        for name, spec in contract['$defs'][entity]['properties'].items():
            parts = [name, 'INTEGER' if spec.get('type') in ('integer', 'boolean') else 'TEXT', 'NOT NULL']
            parts += ['PRIMARY KEY'] if name == pk else []
            parts += ['UNIQUE'] if (table, name) in UNIQUE else []
            parts += ['REFERENCES {} ({})'.format(*FOREIGN[(table, name)])] if (table, name) in FOREIGN else []
            lines.append(' '.join(parts + [f'CHECK ({column_check(name, spec)})']))
        out[table] = ' '.join(f'CREATE TABLE {table} ( {", ".join(lines + TABLE_CHECKS.get(table, []))} ) STRICT;'.split())
    return out


def expected_simple_triggers():
    """Texto normalizado de los triggers de solo inserción, de tenant y de fila única (los de cadena y orden se
    comprueban por nombre y por su efecto en P10 y P29)."""
    out = {}
    for table, _, _ in TABLE_ENTITY:
        for when, verb in (('no_update', 'UPDATE'), ('no_delete', 'DELETE')):
            out[f'{table}_{when}'] = (f"CREATE TRIGGER {table}_{when} BEFORE {verb} ON {table} "
                                      f"BEGIN SELECT RAISE(ABORT, '{table}: solo inserción'); END;")
    for table in ORG_TABLES:
        out[f'{table}_tenant'] = (f'CREATE TRIGGER {table}_tenant BEFORE INSERT ON {table} WHEN '
                                  f'NEW.synthetic_organization_id IS NOT (SELECT synthetic_organization_id FROM '
                                  f"tenant_context) BEGIN SELECT RAISE(ABORT, '{table}: tenant ajeno'); END;")
    for table, label in (('tenant_context', 'fila única'), ('pipeline_run', 'principal único')):
        out[f'{table}_single'] = (f'CREATE TRIGGER {table}_single BEFORE INSERT ON {table} WHEN EXISTS (SELECT 1 FROM '
                                  f"{table}) BEGIN SELECT RAISE(ABORT, '{table}: {label}'); END;")
    return out


def expected_schema(contract):
    """table_info esperado de cada tabla: [nombre, tipo, notnull, pk], solo desde el contrato de A."""
    out = {}
    for table, entity, pk in TABLE_ENTITY:
        props = contract['$defs'][entity]['properties']
        out[table] = [[name, 'INTEGER' if spec.get('type') in ('integer', 'boolean') else 'TEXT', 1, 1 if name == pk else 0]
                      for name, spec in props.items()]
    return out


def expected_origin():
    """Las cuatro rutas fijas de F34 con el SHA-256 de su manifiesto (llave independiente de las constantes del almacén)."""
    manifest = read_json(F34_MANIFEST)
    if manifest.get('dataset_version') != 'f34-synth-1.1.0' or manifest.get('source') != 'synthetic':
        raise ValueError('manifiesto F34 distinto de f34-synth-1.1.0 sintético')
    return tuple((name, f'{F34_DIR}/{name}.csv', manifest['files'][f'{name}.csv']['sha256']) for name in F34_NAMES)


# ---------------------------------------------------------------- STA: análisis estático del almacén
def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f'{base}.{node.attr}' if base else None
    return None


def _expr(source):
    return ast.dump(ast.parse(source, mode='eval').body)


def store_static(source, contract, origin):
    """Problemas estáticos del almacén por tema, sobre los mismos bytes que luego se ejecutarán."""
    P = {k: [] for k in ('imports', 'os', 'connect', 'execute', 'catalog', 'ddl', 'postcondition', 'files', 'attrs',
                         'module_state', 'api', 'refs', 'strings', 'time', 'origin')}
    try:
        tree = ast.parse(source.decode('utf-8'), filename=STORE)
    except (SyntaxError, ValueError, UnicodeDecodeError) as e:
        return {'parse': [f'almacén no analizable ({e.__class__.__name__})']}
    parent = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[child] = node

    def enclosing(node, kinds):
        while node in parent:
            node = parent[node]
            if isinstance(node, kinds):
                return node
        return None

    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and node.body and \
                isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
            docstrings.add(node.body[0].value)
    # Catálogo: solo constantes de texto literales a nivel de módulo, asignadas una vez.
    catalog, module_names = {}, {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            module_names[name] = module_names.get(name, 0) + 1
            if name.startswith('SQL_'):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    catalog[name] = node.value.value
                else:
                    P['catalog'].append(f'{name}: no es una constante literal')
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            P['module_state'].append('asignación aumentada o anotada a nivel de módulo')
    P['catalog'] += [f'{n}: asignado {k} veces' for n, k in module_names.items() if k > 1]
    sql_values = {n.value for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and
                  isinstance(n.targets[0], ast.Name) and n.targets[0].id.startswith('SQL_')}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and node.id.startswith('SQL_') and \
                enclosing(node, (ast.FunctionDef, ast.ClassDef, ast.Lambda)) is not None:
            P['catalog'].append(f'{node.id}: reasignado fuera del nivel de módulo')
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            P['module_state'].append(f'sentencia global/nonlocal (línea {node.lineno})')
    # DDL: doble llave contra el esquema que el gate deriva de A.
    ddl = catalog.get('SQL_SCHEMA')
    if ddl is None:
        P['ddl'].append('falta SQL_SCHEMA')
    else:
        bare = re.sub(r'BEFORE (INSERT|UPDATE|DELETE) ON', ' ', ddl)
        if DDL_FORBIDDEN.search(bare) or re.search(r'\b(UPDATE|DELETE)\b', bare):
            P['ddl'].append('el DDL contiene sentencias o palabras no autorizadas')
        tables = {m[1]: ' '.join(m[0].split()) for m in re.finditer(r'CREATE TABLE (\w+) \(.*?\n\) STRICT;', ddl, re.S)}
        try:
            want = expected_tables(contract)
        except (KeyError, ValueError) as e:
            want = {}
            P['ddl'].append(f'esquema esperado no derivable del contrato de A ({e})')
        for table in sorted(set(want) | set(tables)):
            if tables.get(table) != want.get(table):
                P['ddl'].append(f'{table}: CREATE TABLE distinto del derivado del contrato de A')
        triggers = {m[1]: ' '.join(m[0].split()) for m in re.finditer(r'CREATE TRIGGER (\w+) .*?END;', ddl, re.S)}
        if sorted(triggers) != TRIGGERS or len(re.findall(r'CREATE TRIGGER', ddl)) != len(TRIGGERS):
            P['ddl'].append(f'triggers distintos del contrato: {sorted(set(triggers) ^ set(TRIGGERS))[:4]}')
        for name, text in expected_simple_triggers().items():
            if triggers.get(name) != text:
                P['ddl'].append(f'{name}: trigger distinto del esperado')
        if len(re.findall(r'\bCREATE\b', ddl)) != len(TABLE_ENTITY) + len(TRIGGERS):
            P['ddl'].append('el DDL crea objetos distintos de las ocho tablas y sus triggers')
    columns = {table: [c[0] for c in cols] for table, cols in expected_schema(contract).items()}
    pk = {table: key for table, _, key in TABLE_ENTITY}
    inserts, selects = {}, {}
    for name, sql in catalog.items():
        if name == 'SQL_SCHEMA':
            continue
        if name.startswith('SQL_PRE_'):
            if sql not in PREFLIGHT_SQL:
                P['catalog'].append(f'{name}: sentencia de preflight fuera de la lista enumerada')
            continue
        if sql == 'PRAGMA database_list':
            continue
        if RUNTIME_FORBIDDEN.search(sql):
            P['catalog'].append(f'{name}: forma prohibida en el catálogo de ejecución')
        if not re.match(r'(INSERT INTO|SELECT|BEGIN|COMMIT|ROLLBACK)\b', sql):
            P['catalog'].append(f'{name}: sentencia no admitida en ejecución')
        m = re.fullmatch(r'INSERT INTO (\w+) \(([\w, ]+)\) VALUES \((\?(?:, \?)*)\)', sql)
        if sql.startswith('INSERT'):
            if not m or m[2].split(', ') != columns.get(m[1]) or m[3].count('?') != len(columns.get(m[1], [])):
                P['catalog'].append(f'{name}: INSERT distinto de la inserción simple con las columnas de A')
            else:
                inserts[m[1]] = inserts.get(m[1], 0) + 1
        m = re.fullmatch(r'SELECT ([\w, ]+) FROM (\w+) ORDER BY (\w+)', sql)
        if sql.startswith('SELECT') and ' FROM ' in sql:
            order = ('seq',) if m and m[2] == 'pipeline_event' else (pk.get(m[2]) if m else None,)
            if not m or m[1].split(', ') != columns.get(m[2]) or m[3] not in order:
                P['catalog'].append(f'{name}: SELECT distinto de la lectura ordenada con las columnas de A')
            else:
                selects[m[2]] = selects.get(m[2], 0) + 1
        elif sql.startswith('SELECT') and sql != 'SELECT 1':
            P['catalog'].append(f'{name}: SELECT sin tabla distinto de la sonda de cierre')
    for table in columns:
        if inserts.get(table) != 1 or selects.get(table) != 1:
            P['catalog'].append(f'{table}: se exige exactamente una inserción y una lectura en el catálogo')
    inserts_names = {n for n, s in catalog.items() if s.startswith('INSERT')}
    connects, opens = 0, 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name not in STORE_IMPORTS or a.asname:
                    P['imports'].append(f'importación no autorizada: {a.name}')
        elif isinstance(node, ast.ImportFrom):
            P['imports'].append(f'importación «from» no autorizada: {node.module}')
        elif isinstance(node, ast.Attribute):
            if node.attr in FORBIDDEN_ATTRS:
                P['attrs'].append(f'atributo prohibido: {node.attr}')
            dotted = _dotted(node)
            if dotted and dotted.startswith('os.') and not isinstance(parent.get(node), ast.Attribute) and \
                    dotted not in OS_ALLOWED:
                P['os'].append(f'uso de os no autorizado: {dotted}')
        elif isinstance(node, ast.Name):
            if node.id in FORBIDDEN_BUILTINS:
                P['attrs'].append(f'referencia prohibida: {node.id}')
            if node.id == 'open' and not (isinstance(parent.get(node), ast.Call) and parent[node].func is node):
                P['attrs'].append('referencia indirecta a open')
            if node.id in FORBIDDEN_MODULE_NAMES:
                P['time'].append(f'referencia a {node.id}')
        elif isinstance(node, ast.Call):
            name = _dotted(node.func) or ''
            if name == 'sqlite3.connect':
                connects += 1
                ok = (len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == ':memory:'
                      and all(k.arg == 'isolation_level' and isinstance(k.value, ast.Constant) and k.value.value is None
                              for k in node.keywords))
                if not ok:
                    P['connect'].append('sqlite3.connect distinto de la constante literal \':memory:\' sin uri')
            if isinstance(node.func, ast.Attribute) and node.func.attr in ('execute', 'executemany'):
                arg = node.args[0] if node.args else None
                if not (isinstance(arg, ast.Name) and arg.id in catalog and arg.id != 'SQL_SCHEMA') or \
                        node.keywords or len(node.args) > 2:
                    P['execute'].append(f'execute sin una constante del catálogo (línea {node.lineno})')
                elif node.func.attr == 'executemany':
                    P['execute'].append(f'executemany no admitido (línea {node.lineno})')
                elif arg.id in inserts_names and not (isinstance(parent.get(node), ast.Call) and
                                                      _dotted(parent[node].func) == '_one'):
                    P['postcondition'].append(f'INSERT sin la postcondición _one (línea {node.lineno})')
                elif not arg.id.startswith(('SQL_PRE_', 'SQL_DATABASE_LIST')) and \
                        enclosing(node, (ast.FunctionDef,)) is not None and \
                        enclosing(node, (ast.FunctionDef,)).name == '_preflight' and \
                        arg.id not in ('SQL_DATABASE_LIST',):
                    P['execute'].append(f'el preflight ejecuta una sentencia fuera de su lista (línea {node.lineno})')
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'executescript':
                arg = node.args[0] if node.args else None
                fn = enclosing(node, (ast.FunctionDef,))
                if not (isinstance(arg, ast.Name) and arg.id == 'SQL_SCHEMA') or fn is None or fn.name != '_preflight':
                    P['ddl'].append('executescript fuera del DDL constante del preflight')
            if isinstance(node.func, ast.Name) and node.func.id == 'open':
                opens += 1
                mode = node.args[1] if len(node.args) > 1 else None
                fn = enclosing(node, (ast.FunctionDef,))
                loop = enclosing(node, (ast.For,))
                fixed = (loop is not None and ast.dump(loop.iter) == _expr('F34_INPUTS') and
                         ast.dump(loop.target) == ast.dump(ast.parse('name, rel, digest = x').body[0].targets[0]) and
                         len(node.args) == 2 and ast.dump(node.args[0]) == _expr("os.path.join(_ROOT, *rel.split('/'))"))
                if not (isinstance(mode, ast.Constant) and mode.value == 'rb') or node.keywords or fn is None or \
                        fn.name != '_load_origin' or not fixed:
                    P['files'].append(f'open no autorizado (línea {node.lineno})')
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if FORBIDDEN_REFS.search(node.value):
                P['refs'].append(f'referencia prohibida: {node.value[:40]!r}')
            if node not in docstrings and node not in sql_values and SQL_WORDS.search(node.value):
                P['strings'].append(f'SQL fuera del catálogo: {node.value[:40]!r}')
    if connects != 1:
        P['connect'].append(f'sqlite3.connect aparece {connects} veces (se exige una)')
    if opens != 1:
        P['files'].append(f'open aparece {opens} veces (se exige una, en _load_origin)')
    # Origen: las cuatro rutas fijas con el SHA-256 del manifiesto F34 y la raíz derivada de __file__.
    values = {n.targets[0].id: n.value for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and
              isinstance(n.targets[0], ast.Name)}
    try:
        if ast.literal_eval(values['F34_INPUTS']) != origin:
            P['origin'].append('F34_INPUTS distinto de las rutas y hashes del manifiesto F34')
    except (KeyError, ValueError, SyntaxError):
        P['origin'].append('F34_INPUTS ausente o no literal')
    expected_root = "os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))"
    if '_ROOT' not in values or ast.dump(values['_ROOT']) != _expr(expected_root):
        P['origin'].append('_ROOT distinto de la raíz derivada de __file__')
    # Estado a nivel de módulo: sin conexiones, almacenes ni registros.
    for node in tree.body:
        targets = [t.id for t in getattr(node, 'targets', []) if isinstance(t, ast.Name)]
        for t in targets:
            if not t.startswith('SQL_') and re.search(r'conn|store|registry|cache|pool', t, re.I):
                P['module_state'].append(f'nombre de estado a nivel de módulo: {t}')
        if isinstance(node, ast.Assign):
            for call in [n for n in ast.walk(node.value) if isinstance(n, ast.Call)]:
                if (_dotted(call.func) or '') not in ('re.compile', 'frozenset', 'os.path.abspath', 'os.path.join',
                                                      'os.path.dirname'):
                    P['module_state'].append(f'llamada a nivel de módulo: {_dotted(call.func)}')
        elif not isinstance(node, (ast.Import, ast.FunctionDef, ast.ClassDef)) and \
                not (isinstance(node, ast.Expr) and node.value in docstrings):
            P['module_state'].append(f'sentencia a nivel de módulo no admitida (línea {node.lineno})')
    # API cerrada.
    public_funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')}
    public_classes = {n.name for n in tree.body if isinstance(n, ast.ClassDef) and not n.name.startswith('_')}
    if set(public_funcs) != set(API):
        P['api'].append(f'API pública distinta del contrato: {sorted(set(public_funcs) ^ set(API))}')
    for name, fn in public_funcs.items():
        params = tuple(a.arg for a in fn.args.args)
        if API.get(name) != params or fn.args.vararg or fn.args.kwarg or fn.args.kwonlyargs or fn.args.posonlyargs:
            P['api'].append(f'{name}: parámetros {params} distintos del contrato')
    if public_classes != API_CLASSES:
        P['api'].append(f'clases públicas distintas del contrato: {sorted(public_classes ^ API_CLASSES)}')
    names = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))] + \
            [a.arg for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) for a in n.args.args]
    P['api'] += [f'nombre con capacidad prohibida: {n}' for n in names if PROHIBITED_NAMES.search(n)]
    return P


# ---------------------------------------------------------------- funciones independientes del almacén (P29)
def g_canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def g_sha(obj):
    return hashlib.sha256(g_canon(obj)).hexdigest()


def g_t1(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


def g_content_hash(org, origin, criterion, kind, text):
    return g_sha({'algorithm': 'f35sbx-content-sha256-v1', 'synthetic_organization_id': org, 'origin_record_id': origin,
                  'criterion_ref': criterion, 'evidence_kind': kind, 'text': text})


def g_chain_ok(items, key, prev_key):
    prev = '0' * 64
    for item in items:
        if item[prev_key] != prev or g_sha({k: v for k, v in item.items() if k != key}) != item[key]:
            return False
        prev = item[key]
    return True


def identity_conflicts(principals):
    """B2-M03: dos runs con el mismo identificador y principales distintos violan «una semilla, un escenario»."""
    seen, out = {}, []
    for p in principals:
        other = seen.setdefault(p['pipeline_run_id'], p)
        if other != p:
            out.append(p['pipeline_run_id'])
    return out


def authorized_rows(csv_module, origin):
    """Filas F34 autorizadas por tenant, calculadas por el gate como A (criterio y postulación), desde bytes con el
    SHA-256 del manifiesto. Usa el módulo csv estándar ya cargado por el almacén: el gate no lo importa (DEP)."""
    tables = {}
    for name, rel, digest in origin:
        raw = real_bytes(rel)
        if raw is None or hashlib.sha256(raw).hexdigest() != digest:
            return None
        tables[name] = list(csv_module.DictReader(re.split(r'(?<=\n)', raw.decode('utf-8'))))
    apps = {r['application_token']: r['organization_token'] for r in tables['applications']}
    vac = {r['vacancy_token']: r['organization_token'] for r in tables['vacancies']}
    crit = {r['criterion_id']: vac[r['vacancy_token']] for r in tables['criteria']}
    out = {org: {} for org in TENANTS}
    for r in tables['evidence']:
        org = apps.get(r['application_token'])
        if org in out and crit.get(r['criterion_id']) == org and r['state'] == 'vinculada' and \
                r['source_type'] == 'synthetic' and r['source_type_ev'] in ('formulario', 'nota_entrevista', 'prueba'):
            out[org][r['synthetic_record_id']] = (r['criterion_id'], r['source_type_ev'], r['evidence_text'])
    return out


# ---------------------------------------------------------------- temporales sin dependencias nuevas
_TEMP_COUNTER = [0]


def make_temp(label):
    base = os.environ.get('TEMP') or os.environ.get('TMP') or os.environ.get('TMPDIR') or '/tmp'
    base = os.path.abspath(base)
    if (os.path.normcase(base) + os.sep).startswith(_REPO + os.sep) or not os.path.isdir(base):
        raise GitError('directorio temporal no disponible fuera del repositorio')
    _TEMP_COUNTER[0] += 1
    path = os.path.join(base, f'f35sbxb2-{label}-{os.getpid()}-{_TEMP_COUNTER[0]}')
    os.mkdir(path)
    return path


def remove_tree(path):
    if not os.path.isdir(path):
        return
    for d, dirs, files in os.walk(path, topdown=False):
        for name in files:
            full = os.path.join(d, name)
            try:
                os.chmod(full, 0o600)
            except OSError:
                pass
            os.remove(full)
        for name in dirs:
            full = os.path.join(d, name)
            if os.path.islink(full):
                os.remove(full)
            else:
                os.rmdir(full)
    os.rmdir(path)


def listing(path, skip=('.git',)):
    out = set()
    for d, dirs, files in os.walk(path):
        dirs[:] = [x for x in dirs if not (d == path and x in skip)]
        for name in files:
            out.add(os.path.relpath(os.path.join(d, name), path).replace(os.sep, '/'))
    return out


# ---------------------------------------------------------------- B1F sobre historias desechables (P25, P32 y P33)
class FixtureRepo:
    """Repositorio desechable para B1F, fuera del original: configuración de Git aislada, identidad ficticia y commits
    construidos con plumbing sobre un índice propio. El repositorio real nunca se toca."""

    def __init__(self):
        self.base = make_temp('b1f')
        try:
            self.root = os.path.join(self.base, 'repo')
            os.mkdir(self.root)
            config = os.path.join(self.base, 'gitconfig')
            with open(config, 'wb'):
                pass
            env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
            env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': config, 'GIT_AUTHOR_NAME': 'fixture-b2',
                        'GIT_AUTHOR_EMAIL': 'fixture-b2@example.invalid', 'GIT_COMMITTER_NAME': 'fixture-b2',
                        'GIT_COMMITTER_EMAIL': 'fixture-b2@example.invalid',
                        'GIT_AUTHOR_DATE': '2026-10-12T00:00:00+00:00', 'GIT_COMMITTER_DATE': '2026-10-12T00:00:00+00:00'})
            self.repo = Repo(self.root, env)
            self.repo.run('init', '-q')
            self.repo.run('config', 'core.autocrlf', 'false')
            self.plumbing = Repo(self.root, dict(env, GIT_INDEX_FILE=os.path.join(self.base, 'indice-plumbing')))
            self.count = 0
        except BaseException:
            remove_tree(self.base)
            raise

    def commit(self, parents, changes):
        """Commit cuyo árbol es el del primer padre con los cambios indicados (bytes, (modo, bytes) o None)."""
        self.plumbing.run('read-tree', *(parents[:1] or ['--empty']))
        for path, value in changes.items():
            if value is None:
                self.plumbing.run('update-index', '--force-remove', '--', path)
                continue
            mode, data = value if isinstance(value, tuple) else ('100644', value)
            blob = self.plumbing.run('hash-object', '-w', '--stdin', data=data).decode().strip()
            self.plumbing.run('update-index', '--add', '--cacheinfo', f'{mode},{blob},{path}')
        tree = self.plumbing.run('write-tree').decode().strip()
        self.count += 1
        return self.plumbing.run('commit-tree', tree, '-m', f'fixture {self.count}',
                                 *[arg for p in parents for arg in ('-p', p)]).decode().strip()


FX_OLD = {'CLAUDE.md': b'# Gobierno\n\nEstado: B1 en desarrollo.\n', 'docs/PROGRESS.md': b'# Progreso\n\nEstado: B1 en desarrollo.\n'}
FX_DELTA = {p: [('Estado: B1 en desarrollo.', 'Estado: B1 cerrada; B2 implementada.')] for p in GOV_PATHS}


def b1f_fixtures():
    """Escenarios de B1F en un repositorio desechable. {id: (ok, descripción, detalle)}; el ok compara el resultado
    con lo esperado (pasa o falla con la regla indicada)."""
    fx, results = None, {}
    try:
        fx = FixtureRepo()
        R, c = fx.repo, fx.commit
        new = {p: FX_OLD[p].replace(b'B1 en desarrollo.', 'B1 cerrada; B2 implementada.'.encode()) for p in GOV_PATHS}
        rest = {SET_A[2]: b'readme de B\n', SET_A[3]: b'documento de B1\n', SET_A[4]: b'# gate de B1\n'}
        closing = {SET_B[0]: b'# validador del cierre\n', SET_B[1]: b'{"manifiesto": 1}\n', SET_B[2]: b'cierre de B1\n'}
        anchor = c([], {**FX_OLD, **rest, 'otro.txt': b'0\n'})
        close = c([anchor], closing)
        dev = c([close], {'otro.txt': b'1\n'})
        trans = c([dev], new)
        post = c([trans], {'otro.txt': b'2\n'})
        side, side2, d1 = c([close], {'otro2.txt': b'x\n'}), c([dev], {'otro3.txt': b'x\n'}), c([close], {'otro4.txt': b'x\n'})
        d2 = c([d1, post], {**new, 'otro.txt': b'2\n'})                                  # --no-ff en develop
        main_merge = c([close, d2], {**new, 'otro.txt': b'2\n', 'otro4.txt': b'x\n'})     # y de develop en main
        back = c([trans], FX_OLD)
        again = c([back], new)
        scenarios = [   # (id, descripción, head, registrada, debe pasar, fragmentos exigidos en los problemas)
            ('F01', 'historia legítima antes de la transición', dev, None, True, ()),
            ('F02', 'transición legítima y un descendiente', post, None, True, ()),
            ('F03', 'transición registrada que coincide con la derivada', post, trans, True, ()),
            ('F04', 'transición registrada distinta de la derivada', post, dev, False, ('distinta de la registrada',)),
            ('F05', 'manifiesto del cierre modificado y restaurado (P32)',
             c([c([dev], {SET_B[1]: b'{"manifiesto": 2}\n'})], {SET_B[1]: closing[SET_B[1]]}), None, False,
             ('conjunto del cierre',)),
            ('F06', 'gate de B1 modificado y restaurado',
             c([c([dev], {SET_A[4]: b'# gate alterado\n'})], {SET_A[4]: rest[SET_A[4]]}), None, False, ('conjunto auditado',)),
            ('F07', 'documento de B1 eliminado', c([dev], {SET_A[3]: None}), None, False, ('conjunto auditado',)),
            ('F08', 'documento de B1 renombrado', c([dev], {SET_A[3]: None, SET_A[3][:-3] + '_v2.md': rest[SET_A[3]]}),
             None, False, ('conjunto auditado',)),
            ('F09', 'gate de B1 con cambio de modo', c([dev], {SET_A[4]: ('100755', rest[SET_A[4]])}), None, False,
             ('conjunto auditado',)),
            ('F10', 'histórico, nuevo, histórico y nuevo otra vez (P33)', again, None, False, ('regla 3', 'regla 4')),
            ('F11', 'histórico, nuevo e histórico otra vez', back, None, False, ('regla 3',)),
            ('F12', 'tercer blob en el gobierno', c([dev], {'CLAUDE.md': b'# Gobierno\n\nEstado: otro.\n'}), None, False,
             ('regla 1',)),
            ('F13', 'transición hecha en un merge', c([dev, side], {**new, 'otro2.txt': b'x\n'}), None, False, ('regla 2',)),
            ('F14', 'transición en una sola ruta', c([dev], {'CLAUDE.md': new['CLAUDE.md']}), None, False,
             ('regla 1', 'regla 4')),
            ('F15', 'transición que cambia otras rutas', c([dev], {**new, 'otro.txt': b'9\n'}), None, False, ('otras rutas',)),
            ('F16', 'rama previa a la transición fusionada con el blob nuevo', c([post, side2], {'otro3.txt': b'x\n'}), None,
             True, ()),
            ('F17', 'merge que reintroduce el blob histórico', c([post, side2], {**FX_OLD, 'otro3.txt': b'x\n'}), None,
             False, ('regla 3',)),
            ('F18', 'integración --no-ff en develop y después en main', main_merge, trans, True, ()),
        ]
        for cid, what, head, registered, should_pass, fragments in scenarios:
            problems, derived, _ = b1f_check(R, anchor, close, FX_DELTA, registered, head=head)
            text = ' | '.join(problems)
            ok = (not problems) if should_pass else (bool(problems) and all(f in text for f in fragments))
            if ok and cid in ('F02', 'F03', 'F18'):
                ok = derived == trans
            results[cid] = (ok, what, f'{"pasa" if not problems else text[:160]}')
        # Estado efectivo sobre una copia de trabajo del escenario legítimo: limpio, disco alterado e índice con flag.
        R.run('checkout', '-q', '--detach', post)
        problems, _, _ = b1f_check(R, anchor, close, FX_DELTA, None, root=fx.root)
        results['F19'] = (not problems, 'estado efectivo limpio tras la transición', '; '.join(problems)[:160] or 'pasa')
        with open(os.path.join(fx.root, 'CLAUDE.md'), 'wb') as f:
            f.write(FX_OLD['CLAUDE.md'])
        problems, _, _ = b1f_check(R, anchor, close, FX_DELTA, None, root=fx.root)
        results['F20'] = (any('disco' in p for p in problems), 'disco con el blob histórico tras la transición',
                          '; '.join(problems)[:160])
        R.run('checkout', '-q', '--', 'CLAUDE.md')
        R.run('update-index', '--skip-worktree', 'CLAUDE.md')
        problems, _, _ = b1f_check(R, anchor, close, FX_DELTA, None, root=fx.root)
        results['F21'] = (any('índice' in p for p in problems), 'índice con flag skip-worktree', '; '.join(problems)[:160])
        R.run('update-index', '--no-skip-worktree', 'CLAUDE.md')
    except (GitError, OSError, ValueError) as e:
        results['F00'] = (False, 'repositorio desechable de B1F', f'no evaluable ({e}): falla cerrado')
    finally:
        if fx is not None:
            remove_tree(fx.base)
    return results


# ---------------------------------------------------------------- DYN: casos P01..P31 sobre el almacén
def load_store(data):
    """Ejecuta el almacén desde los bytes ya analizados; no se registra en sys.modules."""
    path = os.path.join(ROOT, *STORE.split('/'))
    spec = importlib.util.spec_from_file_location('f35sbxb2_store_verificado', path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(data, path, 'exec', dont_inherit=True), module.__dict__)
    return module


class FailConn:
    """Vía interna del arnés: conexión envuelta que falla en las sentencias indicadas (las primeras `times` veces, o
    siempre) y, si se pide, no cierra de verdad. No forma parte de la API."""

    def __init__(self, real, error, fail, times=None, closes=True):
        self._real, self._error, self._fail, self._left, self._closes = real, error, fail, times, closes

    def execute(self, sql, params=()):
        if self._fail(sql) and (self._left is None or self._left > 0):
            if self._left is not None:
                self._left -= 1
            raise self._error('fallo inyectado por el arnés')
        return self._real.execute(sql, params)

    @property
    def in_transaction(self):
        return self._real.in_transaction

    def close(self):
        if self._closes:
            self._real.close()


def make_cases(ST, fixtures, rows, schema):
    """Casos P01..P31 (salvo P06, P19, P20, P25 y P28 en su parte estática, que son de STA o de la historia Git)."""
    sq = ST.sqlite3

    def expect(cond, msg):
        if not cond:
            raise CaseFail(msg)

    def expect_error(codes, fn, *a, **k):
        codes = (codes,) if isinstance(codes, str) else codes
        try:
            fn(*a, **k)
        except ST.SbxbStoreError as e:
            if e.code not in codes:
                raise CaseFail(f'código {e.code}, se esperaba {"/".join(codes)} ({e})')
            return e
        raise CaseFail(f'no falló; se esperaba {"/".join(codes)}')

    def refused(conn, stmt, params=()):
        try:
            conn.execute(stmt, params)
        except sq.Error:
            return True
        return False

    def probe_closed(conn):
        try:
            conn.execute(ST.SQL_POST_CLOSE_PROBE)
        except sq.ProgrammingError:
            return True
        return False

    def tenant(org):
        return {'synthetic_organization_id': org, 'tenant_kind': 'synthetic_organization',
                'origin_dataset_version': 'f34-synth-1.1.0', 'simulation_actor': f'SIMREV-{org}'}

    def scenario(org):
        run = fixtures[org]['run']
        return run['seed'], run['clock_start']

    def payload(org, i):
        fx = fixtures[org]
        r, s, p, v = fx['records'][i], fx['sources'][i], fx['provenance'][i], fx['reviews'][i]
        expect(r['source_id'] == s['source_id'] == p['source_id'] and v['record_id'] == r['synthetic_id'] ==
               p['record_id'], 'fixture de A desalineado')
        return {'origin_record_id': s['origin_record_id'], 'origin_file_sha256': s['origin_file_sha256'],
                'criterion_ref': r['criterion_ref'], 'evidence_kind': r['evidence_kind'],
                'text_synthetic': r['text_synthetic'], 'hash_before': p['hash_before'], 'content_hash': r['content_hash'],
                'validation_status': r['validation_status'], 'review_status': r['review_status'],
                'created_at': r['created_at'], 'recorded_at': p['recorded_at'], 'reviewed_at': v['reviewed_at']}

    def started(org='ORG-S1', seed=None, clock=None):
        s, c = scenario(org)
        st = ST.open_tenant_store(tenant(org))
        ST.create_run(st, s if seed is None else seed, c if clock is None else clock)
        return st

    def full(org='ORG-S1', seed=None):
        """Camino del oráculo de A: sus siete estados con sus instantes, sus ocho acciones y sus evidencias."""
        fx = fixtures[org]
        st = started(org, seed)
        at = {e['state']: e['at'] for e in fx['events']}
        ST.append_audit(st, 'fixture_verificado', at['pendiente'])
        ST.append_event(st, 'validando', at['validando'], audit_action='esquema_validado')
        ST.append_audit(st, 'sintetico_verificado', at['validando'])
        ST.append_audit(st, 'hash_calculado', at['validando'])
        for i in range(len(fx['records'])):
            ST.append_evidence(st, payload(org, i))
        ST.append_event(st, 'registrado', at['registrado'], audit_action='provenance_registrada')
        ST.append_event(st, 'transformado', at['transformado'])
        ST.append_event(st, 'en_revision', at['en_revision'], audit_action='tenant_validado')
        ST.append_event(st, 'revisado', at['revisado'], audit_action='revision_simulada_registrada')
        ST.append_event(st, 'completado', at['completado'], audit_action='ejecucion_cerrada')
        return st

    def internal(st, stmt, table, row):
        """Vía interna: una inserción fuera de la API, dentro de la unidad de escritura del almacén."""
        def unit(conn):
            conn.execute(ST.SQL_BEGIN)
            ST._one(conn.execute(stmt, ST._params(table, row)))
            conn.execute(ST.SQL_COMMIT)
        return ST._guarded(st, ('activo',), unit)

    def without_authorizer(st, action):
        """Vía interna: retira el autorizador para observar solo los triggers y el límite, y lo restituye."""
        st._conn.set_authorizer(None)
        try:
            return action(st._conn)
        finally:
            st._conn.set_authorizer(ST._authorize)

    def counts(st):
        observed = ST.diagnostic(st)['observed']
        return observed['counts'] if isinstance(observed, dict) else None

    def p01():
        st = ST.open_tenant_store(tenant('ORG-S1'))
        rep = ST.preflight_report(st)
        expect(rep['database_list'] and all(row[2] == '' for row in rep['database_list']),
               f'database_list con ruta: {rep["database_list"]}')
        expect(ST.purge(st)['file_backed'] is False, 'el comprobante no acredita file_backed = false')

    def p02():
        st = started()
        expect(ST.preflight_report(st)['foreign_keys'] == 1, 'foreign_keys distinto de 1')
        run = ST.read_run(st)
        ns = run['pipeline_run_id'][5:]
        row = {'synthetic_id': f'SBBE-{ns}-000009', 'synthetic_organization_id': 'ORG-S1',
               'pipeline_run_id': run['pipeline_run_id'], 'source_id': f'SBBS-{ns}-000009', 'criterion_ref': 'CRI-0004',
               'evidence_kind': 'nota_entrevista', 'text_synthetic': '[SINTÉTICO] fila sin fuente',
               'source_type': 'synthetic', 'environment': 'sandbox', 'hash_algorithm': 'f35sbx-content-sha256-v1',
               'content_hash': '0' * 64, 'validation_status': 'valido', 'review_status': 'conforme',
               'created_at': run['clock_start']}
        e = expect_error('E-SQLITE', internal, st, ST.SQL_INSERT_EVIDENCE_RECORD, 'evidence_record', row)
        expect('FOREIGN KEY' in str(e).upper(), f'no es un fallo de FK: {e}')
        d = ST.diagnostic(st)
        expect(st._state == 'bloqueado' and d['failed_event'] == 'FAILED_EVENT_COMMITTED' and
               d['connection'] == 'CONNECTION_ABORTED', f'sin cierre excepcional: {d}')

    def p03():
        a, b = full('ORG-S1'), full('ORG-S2')
        for st, own, other in ((a, 'ORG-S1', 'ORG-S2'), (b, 'ORG-S2', 'ORG-S1')):
            data = ST.snapshot(st).decode('utf-8')
            expect(other not in data, f'{own} contiene datos de {other}')
            ids = [x['record']['synthetic_id'] for x in ST.list_evidence(st)] + [x['event_id'] for x in ST.list_events(st)]
            expect(ids and all(f'-{own}-' in i for i in ids), f'identificadores ajenos en {own}')
            expect({x['source']['origin_record_id'] for x in ST.list_evidence(st)} <= set(rows[own]),
                   f'{own}: evidencia de una fila de otro tenant')
        ST.purge(a)
        ST.purge(b)

    def p04():
        a, b = started('ORG-S1'), started('ORG-S2')
        expect(a._conn is not b._conn, 'conexión compartida')
        ST.purge(a)
        expect(len(ST.list_events(b)) == 1 and ST.current_state(b) == 'pendiente', 'el otro almacén quedó afectado')
        ST.purge(b)

    def p05():
        expect_error('E-TENANT', ST.open_tenant_store, None)
        for field, value in (('synthetic_organization_id', 'ORG-S9'), ('simulation_actor', 'SIMREV-ORG-S2')):
            expect_error('E-TENANT', ST.open_tenant_store, dict(tenant('ORG-S1'), **{field: value}))
        st = started('ORG-S1')
        expect_error('E-ORIGEN', ST.append_evidence, st, payload('ORG-S2', 0))
        expect(st._state == 'bloqueado' and counts(st)['evidence_record'] == 0, 'evidencia ajena admitida')
        st = started('ORG-S1')
        ns = ST.read_run(st)['pipeline_run_id'][5:]
        src = {'source_id': f'SBBS-{ns}-000001', 'synthetic_organization_id': 'ORG-S2', 'source_type': 'synthetic',
               'origin_dataset_version': 'f34-synth-1.1.0',
               'origin_file': 'docs/academico/datos-sinteticos/dataset/evidence.csv',
               'origin_file_sha256': payload('ORG-S2', 0)['origin_file_sha256'], 'origin_record_id': 'SYN-006218'}
        e = expect_error('E-SQLITE', internal, st, ST.SQL_INSERT_EVIDENCE_SOURCE, 'evidence_source', src)
        expect('tenant ajeno' in str(e), f'el trigger de tenant no rechazó: {e}')

    def p07():
        st = started()
        expect(st._conn.getlimit(sq.SQLITE_LIMIT_ATTACHED) == 0, 'límite de bases adjuntas distinto de 0')
        expect(refused(st._conn, "ATTACH DATABASE ':memory:' AS otra"), 'ATTACH admitido con el autorizador')
        expect(without_authorizer(st, lambda c: refused(c, "ATTACH DATABASE ':memory:' AS otra")),
               'ATTACH admitido sin autorizador: el límite no actúa')
        ST.purge(st)

    def p09():
        st = started()
        before = ST.read_run(st)
        expect_error('E-CICLO', ST.create_run, st, *scenario('ORG-S1'))
        expect(st._state == 'activo', 'un error de ciclo bloqueó el almacén')
        stmts = ('UPDATE pipeline_run SET seed = 1', 'DELETE FROM pipeline_run')
        expect(all(refused(st._conn, s) for s in stmts), 'el autorizador admitió UPDATE o DELETE del principal')
        expect(without_authorizer(st, lambda c: all(refused(c, s) for s in stmts)),
               'los triggers admitieron UPDATE o DELETE del principal')
        expect(ST.read_run(st) == before, 'el principal cambió')
        ST.purge(st)

    def p10():
        st = started()
        expect_error('E-CICLO', ST.append_event, st, 'registrado', '2026-10-07T09:01:00')
        expect(len(ST.list_events(st)) == 1 and st._state == 'activo', 'la secuencia cambió tras E-CICLO')
        first = ST.list_events(st)[0]
        gap = dict(first, event_id=first['event_id'][:-2] + '03', seq=3, state='registrado')
        stmts = (('UPDATE pipeline_event SET state = ?', ('fallido',)), ('DELETE FROM pipeline_event', ()))
        expect(all(refused(st._conn, s, p) for s, p in stmts), 'el autorizador admitió UPDATE o DELETE de eventos')
        expect(without_authorizer(st, lambda c: all(refused(c, s, p) for s, p in stmts) and
                                  refused(c, ST.SQL_INSERT_PIPELINE_EVENT, ST._params('pipeline_event', gap))),
               'los triggers admitieron UPDATE, DELETE o un seq no contiguo')
        expect(ST.list_events(st) == (first,), 'la secuencia cambió')
        ST.purge(st)
        st = full()
        expect_error('E-CICLO', ST.append_event, st, 'fallido', '2026-10-07T09:07:00', 'E-CONTRATO')
        expect(len(ST.list_events(st)) == 7, 'evento admitido tras un estado terminal')
        ST.purge(st)

    def p11():
        a = full()
        seqs = [e['seq'] for e in ST.list_events(a)]
        ords = [x['record']['synthetic_id'] for x in ST.list_evidence(a)]
        expect(seqs == list(range(1, 8)) and ords == sorted(ords), 'orden no determinista')
        b = full()
        expect(ST.snapshot(a) == ST.snapshot(b), 'snapshot distinto en dos ejecuciones del mismo guion')
        ST.purge(a)
        ST.purge(b)

    def p12():
        st = ST.open_tenant_store(tenant('ORG-S1'))
        r = ST.purge(st)
        expect(r['closure_kind'] == 'purga' and r['pipeline_run_id'] == 'sin_run' and r['connection'] == 'CLOSED' and
               r['file_backed'] is False and r['post_close_check'] == 'ProgrammingError', f'purga en abierto: {r}')
        st = started()
        r = ST.purge(st)
        expect(r['closure_kind'] == 'aborto' and r['error_code'] == 'E-ABORTADO' and
               r['failed_event'] == 'FAILED_EVENT_COMMITTED' and r['final_state'] == 'fallido' and
               r['connection'] == 'CONNECTION_ABORTED' and r['file_backed'] is False, f'purga en activo: {r}')
        st = full()
        r = ST.purge(st)
        expect(r['closure_kind'] == 'purga' and r['final_state'] == 'completado' and r['connection'] == 'CLOSED' and
               r['counts']['evidence_record'] == 2 and r['file_backed'] is False and
               r['receipt_hash'] == g_sha({k: v for k, v in r.items() if k != 'receipt_hash'}), f'purga en finalizado: {r}')
        st = full()
        original = ST._observe

        def broken(conn):
            raise sq.OperationalError('fallo inyectado al leer los conteos')
        ST._observe = broken
        try:
            r = ST.purge(st)
        finally:
            ST._observe = original
        expect(r['counts'] == 'no_disponible' and r['connection'] == 'CLOSED', f'purga con fallo inyectado: {r}')
        st = full()
        real = st._conn
        st._conn = FailConn(real, sq.OperationalError, lambda s: False, closes=False)
        try:
            expect_error('E-SQLITE', ST.purge, st)
            d = ST.diagnostic(st)
            expect(st._state == 'bloqueado' and d['connection'] == 'CLOSE_UNVERIFIED' and
                   d['post_close_check'] == 'no_verificado', f'cierre no verificable aceptado: {d}')
        finally:
            real.close()

    def p13():
        st = full()
        conn = st._conn
        ST.purge(st)
        s, c = scenario('ORG-S1')
        calls = [(ST.create_run, (st, s, c)), (ST.append_event, (st, 'validando', c)),
                 (ST.append_evidence, (st, payload('ORG-S1', 0))), (ST.append_audit, (st, 'hash_calculado', c)),
                 (ST.read_run, (st,)), (ST.list_events, (st,)), (ST.list_audit, (st,)), (ST.list_evidence, (st,)),
                 (ST.current_state, (st,)), (ST.snapshot, (st,)), (ST.diagnostic, (st,)), (ST.purge, (st,))]
        for fn, args in calls:
            expect_error('E-PURGADO', fn, *args)
        expect(probe_closed(conn), 'la conexión purgada sigue utilizable')

    def p14():
        a, b = started('ORG-S1'), started('ORG-S2')
        ST.purge(a)
        for i in (0, 1):
            ST.append_evidence(b, payload('ORG-S2', i))
        expect(len(ST.list_evidence(b)) == 2 and ST.current_state(b) == 'pendiente', 'ORG-S2 afectado por la purga')
        ST.purge(b)

    def p15():
        for org in TENANTS:
            st = full(org)
            got = ST.list_evidence(st)
            expect(len(got) == len(fixtures[org]['records']), f'{org}: evidencias no registradas')
            for i, x in enumerate(got):
                r, p = fixtures[org]['records'][i], fixtures[org]['provenance'][i]
                expect(x['record']['content_hash'] == r['content_hash'] and x['provenance']['hash_before'] ==
                       p['hash_before'] and x['record']['text_synthetic'] == r['text_synthetic'],
                       f'{org}: hashes distintos de A')
            ST.purge(st)

    def p16():
        hits = [(org, origin) for org in TENANTS for origin, (_, _, text) in rows[org].items()
                if any(rx.search(g_t1(text)) for rx in PII)]
        expect(not hits, f'heurísticas de PII activadas por filas autorizadas: {hits[:3]}')
        base = payload('ORG-S1', 0)
        text = base['text_synthetic']
        variants = [('correo', dict(base, text_synthetic=text + ' Contacto: ana.torres@correo.example')),
                    ('DNI', dict(base, text_synthetic=text + ' DNI 45871236.')),
                    ('URL', dict(base, text_synthetic=text + ' https://example.org/x')),
                    ('base64', dict(base, text_synthetic=text + ' ' + 'QUJD' * 12)),
                    ('marcado', dict(base, text_synthetic=text + ' <b>x</b>')),
                    ('sin marcador', dict(base, text_synthetic=text[len(TEXT_MARKER):])),
                    ('tipo cv', dict(base, evidence_kind='cv'))]
        for what, p in variants:
            st = started()
            expect_error(('E-ORIGEN', 'E-PROHIBIDO'), ST.append_evidence, st, p)
            expect(st._state == 'bloqueado' and (counts(st) or {}).get('evidence_record') == 0,
                   f'{what}: evidencia persistida o sin cierre excepcional')

    def p17():
        st = ST.open_tenant_store(tenant('ORG-S1'))
        names = [c[0] for cols in ST.preflight_report(st)['table_info'].values() for c in cols]
        ST.purge(st)
        expect(not [n for n in names if PROHIBITED_NAMES.search(n)], 'columnas de puntaje, ranking o selección')
        for extra in ('score', 'selected'):
            st = started()
            expect_error('E-CONTRATO', ST.append_evidence, st, dict(payload('ORG-S1', 0), **{extra: 1}))
            expect(st._state == 'bloqueado', f'{extra}: sin cierre excepcional')

    def p18():
        st = started()
        expect_error(('E-ORIGEN', 'E-PROHIBIDO'), ST.append_evidence, st, dict(payload('ORG-S1', 0),
                                                                            evidence_kind='documento'))
        expect(st._state == 'bloqueado' and counts(st)['evidence_record'] == 0, 'documento admitido')

    def p21():
        cases = []

        def inject(st, fail, times=None):
            real = st._conn
            st._conn = FailConn(real, sq.OperationalError, fail, times)
            return real
        st = ST.open_tenant_store(tenant('ORG-S1'))
        real = inject(st, lambda s: s == ST.SQL_INSERT_PIPELINE_RUN)
        expect_error('E-SQLITE', ST.create_run, st, *scenario('ORG-S1'))
        cases.append(('create_run', st, real, 'FAILED_EVENT_UNAVAILABLE', {'pipeline_run': 0, 'pipeline_event': 0}))
        empty = {'pipeline_event': 2, 'evidence_source': 0, 'evidence_record': 0, 'simulated_review': 0,
                 'evidence_provenance': 0, 'audit_entry': 0}
        c = scenario('ORG-S1')[1]
        for stmt, op in ((ST.SQL_INSERT_EVIDENCE_SOURCE, 'evidencia'), (ST.SQL_INSERT_EVIDENCE_RECORD, 'evidencia'),
                         (ST.SQL_INSERT_SIMULATED_REVIEW, 'evidencia'), (ST.SQL_INSERT_EVIDENCE_PROVENANCE, 'evidencia'),
                         (ST.SQL_INSERT_PIPELINE_EVENT, 'evento'), (ST.SQL_INSERT_AUDIT_ENTRY, 'evento+auditoría'),
                         (ST.SQL_INSERT_AUDIT_ENTRY, 'auditoría')):
            st = started()
            real = inject(st, lambda s, stmt=stmt: s == stmt, times=1)
            if op == 'evidencia':
                expect_error('E-SQLITE', ST.append_evidence, st, payload('ORG-S1', 0))
            elif op == 'evento':
                expect_error('E-SQLITE', ST.append_event, st, 'validando', c)
            elif op == 'evento+auditoría':
                expect_error('E-SQLITE', ST.append_event, st, 'validando', c, audit_action='esquema_validado')
            else:
                expect_error('E-SQLITE', ST.append_audit, st, 'fixture_verificado', c)
            cases.append((f'{op} ({stmt.split()[2]})', st, real, 'FAILED_EVENT_COMMITTED', empty))
        st = started()
        real = inject(st, lambda s: s in (ST.SQL_INSERT_SIMULATED_REVIEW, ST.SQL_ROLLBACK))
        expect_error('E-SQLITE', ST.append_evidence, st, payload('ORG-S1', 0))
        cases.append(('fallo del ROLLBACK', st, real, 'FAILED_EVENT_UNAVAILABLE', None))
        st = started()
        real = inject(st, lambda s: s in (ST.SQL_INSERT_EVIDENCE_RECORD, ST.SQL_INSERT_PIPELINE_EVENT))
        expect_error('E-SQLITE', ST.append_evidence, st, payload('ORG-S1', 0))
        cases.append(('fallo al registrar fallido', st, real, 'FAILED_EVENT_UNAVAILABLE',
                      {'pipeline_event': 1, 'evidence_source': 0, 'evidence_record': 0}))
        for what, st, real, failed, expected in cases:
            d = ST.diagnostic(st)
            expect(st._state == 'bloqueado', f'{what}: objeto no bloqueado')
            expect(d['failed_event'] == failed, f'{what}: failed_event = {d["failed_event"]}, se esperaba {failed}')
            expect(d['connection'] == 'CONNECTION_ABORTED' and probe_closed(real), f'{what}: conexión no cerrada')
            if expected is None:
                expect(d['observed'] == 'no_disponible', f'{what}: hechos inventados tras fallar el ROLLBACK')
            else:
                got = d['observed']['counts'] if isinstance(d['observed'], dict) else {}
                expect(all(got.get(t) == n for t, n in expected.items()), f'{what}: conteos {got}')
            if failed == 'FAILED_EVENT_COMMITTED':
                record = d['failed_event_record']
                expect(d['final_state'] == 'fallido' and record['state'] == 'fallido' and
                       record['error_code'] == 'E-SQLITE' and record['event_hash'] == d['last_event_hash'],
                       f'{what}: evento fallido no releído')
            else:
                expect(d['failed_event_record'] == 'no_disponible', f'{what}: se afirma un fallido no confirmado')

    def p22():
        a, b = full('ORG-S1'), full('ORG-S1')
        seed, clock = scenario('ORG-S1')
        ra, rb = ST.read_run(a), ST.read_run(b)
        expect(ra['pipeline_run_id'] == f'SBBR-ORG-S1-{seed:010d}' and ra == rb and ST.snapshot(a) == ST.snapshot(b),
               'el mismo escenario no da la misma identidad')
        expect(ST.purge(a) == ST.purge(b), 'comprobantes distintos para el mismo escenario')
        c, d = full('ORG-S1', seed=seed + 1), started('ORG-S2', seed=seed)
        expect(ST.read_run(c)['pipeline_run_id'] == f'SBBR-ORG-S1-{seed + 1:010d}' and
               ST.read_run(d)['pipeline_run_id'] == f'SBBR-ORG-S2-{seed:010d}', 'espacios de nombres no distintos')
        e = started('ORG-S1', clock=clock[:8] + '%02d' % (int(clock[8:10]) + 1) + clock[10:])
        principals = [ra, ST.read_run(c), ST.read_run(d), ST.read_run(e)]
        expect(identity_conflicts(principals) == [ra['pipeline_run_id']],
               'no se detectó el mismo identificador con otro principal')
        expect(not identity_conflicts([ra, rb]), 'conflicto falso para el mismo escenario')
        for st in (c, d, e):
            ST.purge(st)
        st = started()
        expect_error('E-CONTRATO', ST.append_event, st, 'validando', clock[:11] + '08:59:00')

    def p23():
        a, b = started('ORG-S1'), started('ORG-S1')
        expect(a._conn is not b._conn, 'conexión compartida entre almacenes')
        ST.purge(a)
        expect(ST.current_state(b) == 'pendiente', 'purgar un almacén afectó a otro del mismo tenant')
        ST.purge(b)

    def p24():
        st = full()
        conn = st._conn
        ST.purge(st)
        expect(probe_closed(conn), 'tras purgar, la conexión sigue abierta')

    def p26():
        st = full()
        before = ST.snapshot(st)
        params = ST._params('evidence_source', ST.list_evidence(st)[0]['source'])
        marks = ', '.join('?' * len(params))
        forms = (('OR REPLACE', f'INSERT OR REPLACE INTO evidence_source VALUES ({marks})'),
                 ('REPLACE', f'REPLACE INTO evidence_source VALUES ({marks})'),
                 ('OR IGNORE', f'INSERT OR IGNORE INTO evidence_source VALUES ({marks})'),
                 ('DO NOTHING', f'INSERT INTO evidence_source VALUES ({marks}) ON CONFLICT DO NOTHING'),
                 ('DO UPDATE', f'INSERT INTO evidence_source VALUES ({marks}) ON CONFLICT(source_id) '
                               f'DO UPDATE SET source_type = excluded.source_type'))

        def attempt(conn):
            seen = {}
            for label, stmt in forms:
                try:
                    seen[label] = f'sin error, rowcount={conn.execute(stmt, params).rowcount}'
                except sq.Error as e:
                    seen[label] = e.__class__.__name__
            return seen
        # Motor con el autorizador (como queda tras abrir) y, por la vía interna, solo con los triggers (§16 del diseño).
        observed = {'con autorizador': attempt(st._conn), 'solo triggers': without_authorizer(st, attempt)}
        expect(ST.snapshot(st) == before, f'una fila cambió o desapareció: {observed}')
        for mode, seen in observed.items():
            expect(seen['OR IGNORE'] == seen['DO NOTHING'] == 'sin error, rowcount=0',
                   f'{mode}: OR IGNORE o DO NOTHING no se comportan como documenta el diseño: {seen}')
            expect(all(seen[k] in ('IntegrityError', 'DatabaseError') for k in ('OR REPLACE', 'REPLACE', 'DO UPDATE')),
                   f'{mode}: una forma que debía fallar no falló: {seen}')
        expect(observed['solo triggers']['DO UPDATE'] == 'IntegrityError' and
               observed['con autorizador']['DO UPDATE'] == 'DatabaseError',
               f'DO UPDATE: el trigger o el autorizador no actúan como se documenta: {observed}')
        ST.purge(st)
        st = started()
        ST.append_evidence(st, payload('ORG-S1', 0))
        params = ST._params('evidence_source', ST.list_evidence(st)[0]['source'])

        def silent(conn):
            conn.execute(ST.SQL_BEGIN)
            ST._one(conn.execute(f'INSERT OR IGNORE INTO evidence_source VALUES ({marks})', params))
            conn.execute(ST.SQL_COMMIT)
        expect_error('E-SQLITE', ST._guarded, st, ('activo',), silent)
        expect(st._state == 'bloqueado' and counts(st)['evidence_source'] == 1,
               'la postcondición no falló cerrada ante una inserción silenciosa')
        return observed

    def p27():
        st = started()
        for stmt in ('PRAGMA foreign_keys = OFF', 'DROP TRIGGER pipeline_run_no_update', 'CREATE TABLE extra (x TEXT)',
                     "SELECT load_extension('x')", 'SELECT random()', "SELECT datetime('now')"):
            expect(refused(st._conn, stmt), f'el autorizador permitió: {stmt}')
        ST.purge(st)

    def p28():
        st = ST.open_tenant_store(tenant('ORG-S1'))
        rep = ST.preflight_report(st)
        ST.purge(st)
        expect(rep['table_info'] == schema, 'table_info distinto de la lista derivada del contrato de A')
        expect(rep['triggers'] == TRIGGERS, f'triggers distintos: {sorted(set(rep["triggers"]) ^ set(TRIGGERS))[:4]}')

    def p29():
        for org in TENANTS:
            st = full(org)
            ev, au, bundles = ST.list_events(st), ST.list_audit(st), ST.list_evidence(st)
            expect(g_chain_ok(ev, 'event_hash', 'prev_event_hash') and g_chain_ok(au, 'audit_hash', 'prev_audit_hash') and
                   g_chain_ok([b['provenance'] for b in bundles], 'provenance_hash', 'prev_provenance_hash'),
                   f'{org}: cadenas no verificables con una implementación independiente')
            fx = fixtures[org]
            for i, b in enumerate(bundles):
                s, r, p, v = b['source'], b['record'], b['provenance'], b['review']
                row = rows[org].get(s['origin_record_id'])
                expect(row is not None, f'{org}: fila F34 de origen no autorizada para el tenant')
                criterion, kind, text = row
                expect(r['text_synthetic'] == g_t1(text) and r['criterion_ref'] == criterion and
                       r['evidence_kind'] == kind, f'{org}: evidencia distinta de su fila F34')
                expect(p['hash_before'] == g_content_hash(org, s['origin_record_id'], criterion, kind, text) and
                       r['content_hash'] == p['hash_after'] ==
                       g_content_hash(org, s['origin_record_id'], criterion, kind, g_t1(text)),
                       f'{org}: hashes no recalculables desde la fila F34')
                expect(r['source_id'] == s['source_id'] == p['source_id'] and p['record_id'] == r['synthetic_id'] ==
                       v['record_id'] and p['review_id'] == v['review_id'], f'{org}: relaciones rotas')
                a_rec, a_src, a_prov, a_rev = fx['records'][i], fx['sources'][i], fx['provenance'][i], fx['reviews'][i]
                for got, want, keys in ((r, a_rec, ('synthetic_organization_id', 'criterion_ref', 'evidence_kind',
                                                    'text_synthetic', 'hash_algorithm', 'content_hash',
                                                    'validation_status', 'review_status', 'source_type', 'environment')),
                                        (s, a_src, ('origin_dataset_version', 'origin_file', 'origin_file_sha256',
                                                    'origin_record_id', 'source_type', 'synthetic_organization_id')),
                                        (p, a_prov, ('provenance_kind', 'transformation_id', 'transformation_version',
                                                     'hash_before', 'hash_after')),
                                        (v, a_rev, ('review_scope', 'review_status', 'reviewer_type', 'scripted',
                                                    'simulation_actor'))):
                    bad = [k for k in keys if got[k] != want[k] or type(got[k]) is not type(want[k])]
                    expect(not bad, f'{org}: nivel 1 distinto de A en {bad}')
            expect([e['state'] for e in ev] == [e['state'] for e in fx['events']] and
                   [a['action'] for a in au] == [a['action'] for a in fx['audit']], f'{org}: nivel 1 de ciclo y auditoría')
            tampered = copy.deepcopy(list(ev))
            tampered[2]['state'] = 'fallido'
            expect(not g_chain_ok(tampered, 'event_hash', 'prev_event_hash'), 'la alteración de un eslabón no se detecta')
            ST.purge(st)
        # Texto correcto con un hash alterado: el almacén recalcula y rechaza (E-HASH), sin filas.
        st = started()
        wrong = payload('ORG-S1', 0)
        wrong['hash_before'] = ('1' if wrong['hash_before'][0] == '0' else '0') + wrong['hash_before'][1:]
        expect_error('E-HASH', ST.append_evidence, st, wrong)
        expect(st._state == 'bloqueado' and counts(st)['evidence_record'] == 0, 'hash alterado admitido')

    def p30():
        seed, clock = scenario('ORG-S1')

        def fresh(state):
            if state == 'abierto':
                return ST.open_tenant_store(tenant('ORG-S1'))
            if state == 'activo':
                return started()
            if state == 'completado':
                return full()
            if state == 'fallido':
                st = started()
                ST.append_event(st, 'fallido', clock, 'E-CONTRATO')
                return st
            if state == 'bloqueado':
                st = started()
                try:
                    ST.append_evidence(st, dict(payload('ORG-S1', 0), text_synthetic=TEXT_MARKER + 'texto ajeno'))
                except ST.SbxbStoreError:
                    pass
                return st
            st = ST.open_tenant_store(tenant('ORG-S1'))
            ST.purge(st)
            return st
        ops = {'create_run': lambda st: ST.create_run(st, seed, clock),
               'append_event': lambda st: ST.append_event(st, 'validando', clock),
               'append_evidence': lambda st: ST.append_evidence(st, payload('ORG-S1', 0)),
               'append_audit': lambda st: ST.append_audit(st, 'hash_calculado', clock),
               'read_run': ST.read_run, 'list_events': ST.list_events, 'current_state': ST.current_state,
               'list_evidence': ST.list_evidence, 'list_audit': ST.list_audit, 'snapshot': ST.snapshot,
               'preflight_report': ST.preflight_report, 'diagnostic': ST.diagnostic, 'purge': ST.purge}
        allowed = {'abierto': {'create_run', 'preflight_report', 'purge'},
                   'activo': {'append_event', 'append_evidence', 'append_audit', 'read_run', 'list_events',
                              'current_state', 'list_evidence', 'list_audit', 'snapshot', 'preflight_report', 'purge'},
                   'completado': {'read_run', 'list_events', 'current_state', 'list_evidence', 'list_audit', 'snapshot',
                                  'preflight_report', 'purge'},
                   'fallido': {'read_run', 'list_events', 'current_state', 'preflight_report', 'purge'},
                   'bloqueado': {'preflight_report', 'diagnostic'},
                   'purgado': {'preflight_report'}}
        refused_code = {'abierto': 'E-CICLO', 'activo': 'E-CICLO', 'completado': 'E-CICLO', 'fallido': 'E-CICLO',
                        'bloqueado': 'E-BLOQUEADO', 'purgado': 'E-PURGADO'}
        for state, ok_ops in allowed.items():
            for op, fn in ops.items():
                st = fresh(state)
                expect(st._state == {'completado': 'finalizado', 'fallido': 'finalizado'}.get(state, state),
                       f'{state}: el almacén de partida está en {st._state}')
                if op in ok_ops:
                    try:
                        fn(st)
                    except ST.SbxbStoreError as e:
                        raise CaseFail(f'{state}: {op} debía admitirse y dio {e.code}')
                else:
                    expect_error(refused_code[state], fn, st)
                if st._state not in ('purgado', 'bloqueado'):
                    ST.purge(st)
        st = started()
        real = st._conn
        st._conn = FailConn(real, sq.OperationalError, lambda s: s in (ST.SQL_INSERT_EVIDENCE_RECORD, ST.SQL_ROLLBACK))
        expect_error('E-SQLITE', ST.append_evidence, st, payload('ORG-S1', 0))
        expect(probe_closed(real), 'la conexión quedó abierta tras fallar el ROLLBACK')
        expect(set(ST.diagnostic(st)) >= {'failed_event', 'connection', 'error_code', 'observed'}, 'diagnóstico incompleto')

    def p31():
        a, b = payload('ORG-S1', 0), payload('ORG-S1', 1)
        org, origin, criterion, kind = 'ORG-S1', a['origin_record_id'], a['criterion_ref'], a['evidence_kind']
        altered = a['text_synthetic'][:-1] + ('X' if a['text_synthetic'][-1] != 'X' else 'Y')
        for what, text in (('texto de otra fila', b['text_synthetic']), ('texto alterado tras T1', altered)):
            p = dict(a, text_synthetic=text, hash_before=g_content_hash(org, origin, criterion, kind, text),
                     content_hash=g_content_hash(org, origin, criterion, kind, text))
            st = started()
            expect_error('E-ORIGEN', ST.append_evidence, st, p)
            expect(st._state == 'bloqueado' and counts(st)['evidence_record'] == 0, f'{what}: evidencia persistida')

    return [('P01', p01), ('P02', p02), ('P03', p03), ('P04', p04), ('P05', p05), ('P07', p07), ('P09', p09),
            ('P10', p10), ('P11', p11), ('P12', p12), ('P13', p13), ('P14', p14), ('P15', p15), ('P16', p16),
            ('P17', p17), ('P18', p18), ('P21', p21), ('P22', p22), ('P23', p23), ('P24', p24), ('P26', p26),
            ('P27', p27), ('P28', p28), ('P29', p29), ('P30', p30), ('P31', p31)]


STATIC_FOR = {'P01': ('connect',), 'P06': ('execute', 'strings', 'catalog'), 'P07': ('catalog',), 'P11': ('catalog',),
              'P17': ('api',), 'P18': ('api',), 'P19': ('imports',), 'P20': ('refs',), 'P22': ('time', 'imports'),
              'P23': ('module_state',), 'P24': ('catalog',), 'P26': ('catalog', 'postcondition', 'api'),
              'P28': ('ddl', 'catalog')}
GROUPS = {'DET': ('P11', 'P22'), 'ISO': ('P03', 'P04', 'P05', 'P14', 'P23'), 'PUR': ('P12', 'P13', 'P24'),
          'DAT': ('P15', 'P16', 'P28', 'P29', 'P31')}
STORE_CASES = tuple(f'P{i:02d}' for i in range(1, 32) if i != 25)

# ---------------------------------------------------------------- NB2: negativos del almacén (bytes mutados en memoria)
# (caso, regla, descripción, (texto original, texto mutado) o ('', texto añadido al final), detector). El detector es un
# tema de STA o, para una mutación invisible al análisis estático, el caso DYN que debe fallar con ella.
NB2_STORE = [
    ('NB2-01', 'STA', 'conexión a un archivo con URI',
     ("conn = sqlite3.connect(':memory:', isolation_level=None)",
      "conn = sqlite3.connect('file:almacen.db', uri=True, isolation_level=None)"), 'connect'),
    ('NB2-02', 'STA', 'INSERT OR REPLACE en el catálogo',
     ("SQL_INSERT_EVIDENCE_RECORD = ('INSERT INTO evidence_record", "SQL_INSERT_EVIDENCE_RECORD = ('INSERT OR REPLACE INTO "
                                                                    "evidence_record"), 'catalog'),
    ('NB2-03', 'STA', 'DELETE en el catálogo', ('', "\nSQL_DELETE_RUN = 'DELETE FROM pipeline_run'\n"), 'catalog'),
    ('NB2-04', 'DEP', 'el almacén importa time', ('import sqlite3\n', 'import sqlite3\nimport time\n'), 'imports'),
    ('NB2-05', 'STA', 'inserción sin la postcondición de una fila',
     ('_one(conn.execute(SQL_INSERT_AUDIT_ENTRY,', '(conn.execute(SQL_INSERT_AUDIT_ENTRY,'), 'postcondition'),
    ('NB2-06', 'STA', 'SQL construido fuera del catálogo',
     ('        conn.execute(SQL_BEGIN)\n        _one(conn.execute(SQL_INSERT_PIPELINE_RUN,',
      "        conn.execute('BEGIN ' + 'IMMEDIATE')\n        _one(conn.execute(SQL_INSERT_PIPELINE_RUN,"), 'execute'),
    ('NB2-07', 'STA', 'API que acepta SQL del llamador',
     ('', '\n\ndef execute_sql(store, sql):\n    return store._conn.execute(sql)\n'), 'api'),
    ('NB2-08', 'STA', 'columna de puntaje fuera del contrato de A',
     ("    created_at TEXT NOT NULL CHECK (created_at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:"
      "[0-5][0-9]')\n) STRICT;",
      "    created_at TEXT NOT NULL CHECK (created_at GLOB '20[0-9][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:"
      "[0-5][0-9]'),\n    score INTEGER NOT NULL CHECK (score >= 0)\n) STRICT;"), 'ddl'),
    ('NB2-09', 'STA', 'conexión a nivel de módulo', ('', "\n_CONN = sqlite3.connect(':memory:')\n"), 'module_state'),
    ('NB2-10', 'STA', 'apertura del origen en modo de escritura',
     ("with open(os.path.join(_ROOT, *rel.split('/')), 'rb') as handle:",
      "with open(os.path.join(_ROOT, *rel.split('/')), 'rb+') as handle:"), 'files'),
    ('NB2-11', 'DYN', 'texto ajeno admitido sin compararlo con T1 de su fila',
     ("    if record['text_synthetic'] != _t1(text):", '    if False:'), 'P31'),
    ('NB2-12', 'DYN', 'autorizador que todo lo admite',
     ('    return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY', '    return sqlite3.SQLITE_OK'), 'P27'),
    ('NB2-13', 'DYN', 'cierre excepcional sin cerrar la conexión',
     ("        verified = _close(conn)\n        store._conn = None\n        store._closure = _closure(store, 'aborto'",
      "        verified = True\n        store._conn = None\n        store._closure = _closure(store, 'aborto'"), 'P21'),
    ('NB2-14', 'DYN', 'filas F34 de otra organización en el índice del tenant',
     ("and criteria.get(r['criterion_id']) == org and applications.get(r['application_token']) == org:",
      'and True:'), 'P05'),
    ('NB2-15', 'DYN', 'purga sin cerrar la conexión',
     ("            verified = _close(conn)\n            store._conn = None\n            store._closure = _closure(store, "
      "'purga'", "            verified = True\n            store._conn = None\n            store._closure = "
                 "_closure(store, 'purga'"), 'P24'),
    ('NB2-16', 'DYN', 'evento fallido afirmado sin confirmarlo',
     ("            if failed_record != 'no_disponible':\n                failed = 'FAILED_EVENT_COMMITTED'",
      "            failed = 'FAILED_EVENT_COMMITTED'"), 'P21'),
    ('NB2-17', 'DYN', 'hashes aceptados sin recalcularlos',
     ("    if evidence['hash_before'] != _content_hash(org, origin, criterion, kind, text) or \\\n"
      "            evidence['content_hash'] != _content_hash(org, origin, criterion, kind, _t1(text)):",
      '    if False:'), 'P29'),
]


def mutate_bytes(data, change):
    old, new = change
    text = data.decode('utf-8')
    if not old:
        return (text + new).encode('utf-8')
    if old not in text:
        raise ValueError(f'mutación no aplicable: {old[:50]!r}')
    return text.replace(old, new, 1).encode('utf-8')


def run_nb2_store(b1, store_bytes, ctx):
    """Cada mutación del almacén debe detectarse: por STA en su tema o, si STA no la ve, por el caso DYN indicado,
    ejecutado con los bytes mutados bajo la misma guarda. {caso: (detectada, detalle)}."""
    results = {}
    for cid, rule, what, change, detector in NB2_STORE:
        try:
            mutated = mutate_bytes(store_bytes, change)
        except ValueError as e:
            results[cid] = (False, f'{e} (falla cerrado)')
            continue
        static = store_static(mutated, ctx['contract'], ctx['origin'])
        if not detector.startswith('P'):
            hits = static.get(detector, [])
            results[cid] = (bool(hits), f'STA ({detector}): {hits[:1]}' if hits else f'STA no lo detecta en {detector}')
            continue
        found = [p for items in static.values() for p in items]
        if found:
            results[cid] = (False, f'la mutación ya la detecta STA ({found[:1]}): no prueba {detector}')
            continue
        tmp, cwd = make_temp('nb2'), os.getcwd()
        try:
            os.chdir(tmp)
            with b1.ExecGuard({}):
                try:
                    ST = load_store(mutated)
                    case = dict(make_cases(ST, ctx['fixtures'], ctx['rows'], ctx['schema']))[detector]
                except Exception as e:      # mutación no ejecutable: el negativo no demuestra nada
                    results[cid] = (False, f'almacén mutado no ejecutable ({e.__class__.__name__})')
                    continue
                try:
                    case()
                    results[cid] = (False, f'{detector} no detecta la mutación')
                except Exception as e:      # el caso falla con el almacén mutado: la mutación se detecta
                    results[cid] = (True, f'{detector}: {e.__class__.__name__}: {str(e)[:90]}')
        finally:
            os.chdir(cwd)
            remove_tree(tmp)
    return results


def run_store_rules(b1, store_bytes, baseline=None):
    """STA, DEP, PRE y DYN (P01..P31) con sus agrupaciones. Devuelve ({regla: [problemas]}, {caso: (ok, detalle)},
    contexto de las pruebas para los negativos NB2)."""
    out = {'STA': [], 'DEP': [], 'PRE': [], 'DYN': []}
    cases, ctx = {}, None
    try:
        contract, origin = read_json(A_CONTRACT), expected_origin()
        fixtures = {org: read_json(p) for org, p in A_FIXTURES.items()}
    except (ValueError, KeyError, UnicodeDecodeError) as e:
        for rid in out:
            out[rid].append(f'contrato de A, fixtures o manifiesto F34 ilegibles ({e}): falla cerrado')
        return out, cases, ctx
    if store_bytes is None:
        for rid in out:
            out[rid].append('almacén ausente o ilegible (falla cerrado)')
        return out, cases, ctx
    static = store_static(store_bytes, contract, origin)
    if 'parse' in static:
        for rid in out:
            out[rid] += static['parse']
        return out, cases, ctx
    out['DEP'] += static['imports']
    out['STA'] += [p for topic, items in static.items() if topic != 'imports' for p in items]
    try:
        gate_tree = ast.parse((real_bytes(GATE2) or b'').decode('utf-8'))
        mods = {a.name.split('.')[0] for n in ast.walk(gate_tree) if isinstance(n, ast.Import) for a in n.names}
        mods |= {(n.module or '').split('.')[0] for n in ast.walk(gate_tree) if isinstance(n, ast.ImportFrom)}
        out['DEP'] += [f'gate: importación no autorizada «{m}»' for m in sorted(mods - GATE_IMPORTS)]
    except (SyntaxError, ValueError) as e:
        out['DEP'].append(f'gate no analizable ({e.__class__.__name__})')
    for pid, topics in STATIC_FOR.items():
        problems = [p for t in topics for p in static.get(t, [])]
        cases[pid] = (not problems, f'estático: {problems[:2]}' if problems else 'estático: correcto')
    if out['STA'] or out['DEP']:
        out['DYN'].append('el almacén no supera STA/DEP: no se ejecuta (falla cerrado)')
        return out, cases, ctx
    schema, rows = expected_schema(contract), None
    tmp = make_temp('dyn')
    repo_before, cwd = (listing(ROOT) if baseline is None else baseline), os.getcwd()
    try:
        os.chdir(tmp)
        with b1.ExecGuard({}) as guard:
            ST = load_store(store_bytes)
            try:
                version = tuple(int(x) for x in ST.sqlite3.sqlite_version.split('.'))
                api = all(hasattr(ST.sqlite3.Connection, m) for m in ('setlimit', 'getlimit', 'set_authorizer')) and \
                    all(hasattr(ST.sqlite3, c) for c in ('SQLITE_LIMIT_ATTACHED', 'SQLITE_DENY', 'SQLITE_OK'))
                ST._require_api()
                probe = ST.open_tenant_store({'synthetic_organization_id': 'ORG-S1', 'tenant_kind': 'synthetic_organization',
                                              'origin_dataset_version': 'f34-synth-1.1.0',
                                              'simulation_actor': 'SIMREV-ORG-S1'})
                rep = ST.preflight_report(probe)
                ST.purge(probe)
                pre = {'SQLite cargado >= 3.37.0': version >= (3, 37, 0), 'API de sqlite3': api,
                       'foreign_keys': rep['foreign_keys'] == 1, 'recursive_triggers': rep['recursive_triggers'] == 1,
                       'temp_store': rep['temp_store'] == 2, 'trusted_schema': rep['trusted_schema'] == 0,
                       'journal_mode': rep['journal_mode'] == 'memory', 'attached_limit': rep['attached_limit'] == 0,
                       'database_list': bool(rep['database_list']) and all(r[2] == '' for r in rep['database_list'])}
                out['PRE'] += [f'requisito no cumplido: {k}' for k, ok in pre.items() if not ok]
            except Exception as e:      # entorno incompatible o almacén inutilizable: falla cerrado
                out['PRE'].append(f'preflight no superado ({e.__class__.__name__}: {e})')
            rows = authorized_rows(ST.csv, origin) if not out['PRE'] else None
            if out['PRE']:
                out['DYN'].append('PRE no superado: no se ejecuta DYN (falla cerrado)')
            elif rows is None:
                out['DYN'].append('origen F34 no verificable para las pruebas (falla cerrado)')
            else:
                for pid, fn in make_cases(ST, fixtures, rows, schema):
                    ok, detail = cases.get(pid, (True, ''))
                    try:
                        result = fn()
                        cases[pid] = (ok, (detail + '; ' if detail else '') + 'dinámico: correcto' +
                                      (f' {result}' if result else ''))
                    except CaseFail as e:
                        cases[pid] = (False, f'dinámico: {e}')
                    except Exception as e:      # un error inesperado de la prueba cuenta como fallo
                        cases[pid] = (False, f'dinámico: {e.__class__.__name__}: {e}')
            if guard.refused:
                out['DYN'].append(f'código del repositorio rechazado por la guarda: {guard.refused[:2]}')
    finally:
        os.chdir(cwd)
        created = listing(tmp)
        remove_tree(tmp)
    p08 = sorted(created | (listing(ROOT) - repo_before))
    cases['P08'] = (not p08 and not out['PRE'] and not out['DYN'],
                    f'archivos nuevos: {p08[:5]}' if p08 else 'sin archivos nuevos en el repositorio ni en el directorio '
                    'de trabajo; database_list sin ruta (garantía acotada a esas ubicaciones)')
    out['DYN'] += [f'{pid}: {cases.get(pid, (False, "no ejecutado"))[1]}' for pid in STORE_CASES
                   if not cases.get(pid, (False, ''))[0] and pid not in ('P19', 'P20')]
    for gid, pids in GROUPS.items():
        out[gid] = [f'{pid}: {cases.get(pid, (False, "no ejecutado"))[1]}' for pid in pids
                    if not cases.get(pid, (False, ''))[0]]
    if rows is not None:
        ctx = {'contract': contract, 'origin': origin, 'fixtures': fixtures, 'rows': rows, 'schema': schema,
               'static': static}
    return out, cases, ctx


# ---------------------------------------------------------------- estado del repositorio para las reglas propias de B2
SQLITE_ARTIFACT = re.compile(r'(\.(db|sqlite|sqlite3)|-(journal|wal|shm))$', re.I)


def collect2(b1):
    """Estado de HEAD para CTX, SCP, FSY, DEP, GOV, CAP y B1F. Cualquier error de Git o de lectura queda en
    S2['errors'] y hace fallar esas reglas (falla cerrado)."""
    S2, repo = {'errors': []}, Repo(ROOT)
    try:
        S2['inside'] = repo.run('rev-parse', '--is-inside-work-tree').strip() == b'true'
        S2['branch'] = repo.run('branch', '--show-current').decode().strip()
        S2['shallow'] = repo.run('rev-parse', '--is-shallow-repository').strip() != b'false'
        S2['ancestors'] = {name: repo.is_ancestor(commit, 'HEAD') for name, commit in (
            ('E', E), ('el cierre de B0', B0_CLOSE), ('el ancla de B1', B1_ANCHOR), ('el cierre de B1', B1_CLOSURE),
            ('la base de B2', B2_BASE))}
        S2['delta'] = {
            'HEAD': b1.name_status(repo.run('diff', '--name-status', '--no-renames', '-z', B2_BASE, 'HEAD')),
            'árbol': b1.name_status(repo.run('diff', '--name-status', '--no-renames', '-z', B2_BASE)),
            'índice': b1.name_status(repo.run('diff', '--cached', '--name-status', '--no-renames', '-z', B2_BASE))}
        S2['untracked'] = {x for x in repo.run('ls-files', '--others', '--exclude-standard', '-z')
                           .decode('utf-8', 'replace').split('\x00') if x}
        S2['surfaces'] = {ref: repo.run('ls-tree', '-r', '-z', ref, '--', *b1.RUNTIME_SURFACES) for ref in (B1_BASE, B2_BASE)}
        S2['folders'] = {}
        for folder in FOLDERS:
            disk, problems = b1.walk((folder,), pycache_roots=(folder + '/',) if folder.endswith('/f35sbxb2') else ())
            tree = {x for x in repo.run('ls-tree', '-r', '--name-only', '-z', 'HEAD', '--', folder)
                    .decode('utf-8', 'replace').split('\x00') if x}
            S2['folders'][folder] = (disk, problems, tree)
        S2['files'] = {p: real_bytes(p) for p in B2_FILES}
        S2['gov'] = {p: real_bytes(p) for p in GOV_PATHS}
        S2['gov_old'] = {p: repo.run('show', f'{B1_ANCHOR}:{p}') for p in GOV_PATHS}
        S2['gov_new'], S2['gov_new_problems'] = governance_new(repo, B1_ANCHOR, GOVERNANCE_DELTA)
        S2['b1f'], S2['transition'], S2['b1f_commits'] = b1f_check(repo, B1_ANCHOR, B1_CLOSURE, GOVERNANCE_DELTA,
                                                                   B2_GOVERNANCE_TRANSITION, root=ROOT)
        S2['listing'] = listing(ROOT)
        S2['py_refs'] = sorted(p for p in repo.run('ls-files', '-z', '--', '*.py').decode('utf-8', 'replace').split('\x00')
                               if p and p not in (STORE, GATE2) and b'sbxb_store' in (real_bytes(p) or b''))
    except (GitError, OSError, ValueError, UnicodeDecodeError) as e:
        S2['errors'].append(f'estado Git o de archivos no verificable: {e}')
    return S2


# ---------------------------------------------------------------- semántica de B1 con los estados de B2 (GOV y CAP)
B2_FORBIDDEN_RX = re.compile(r'(?<![\w-])b2(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*(cerrad\w*|integrad\w*|'
                             r'productiv\w*|congelad\w*|aprobad\w*|publicad\w*|desplegad\w*)\b')


def semantics(b1):
    """Declaraciones de estado de B1 (cerrada) y de B2 (implementada), construidas con las piezas verificadas del gate
    de B1; el resto de entidades conserva sus valores. El gate de B1 no se modifica."""
    declared = [(s, a) for s, a in b1.DECLARED if s != 'b1'] + [
        ('b1', ('cerrad', 'congelad', 'implementad') + b1.LOCKED),
        ('b2', ('implementad', 'no cerrad', 'no congelad', 'no aprobad') + b1.LOCKED)]
    decl_rx = [(re.compile(r'(?<![\w-])(' + subj + r')(?![\w-])(?:\s*(?::=|==|=|:|->|→)\s*|\s+(no\s+)?(?:se\s+)?'
                           + b1.DECL_COPULA + r'\s+(?:[a-z]+mente\s+)?|\s+)' + b1.STATE_VALUE), allowed)
               for subj, allowed in declared]
    verb_rx = [(re.compile(r'(?<![\w-])' + b1.DECL_NEG + r'(?:se\s+)?(?:(?:lo|la|los|las)\s+)?(?<![\w-])(?:' + b1.DECL_VERB +
                           r')(?![\w-])\s+(?:[a-z]+mente\s+)?(?:(?:el|la|los|las|al|a|the)\s+)?(?P<subj>' + subj +
                           r')(?![\w-])'), allowed, rx) for (subj, allowed), (rx, _) in zip(declared, decl_rx)] + \
              [(re.compile(r'(?<![\w-])(?P<subj>' + subj + r')(?![\w-])\s+' + b1.DECL_NEG + r'se\s+(?:[a-z]+mente\s+)?(?:' +
                           b1.DECL_VERB + r')(?![\w-])'), allowed, rx) for (subj, allowed), (rx, _) in zip(declared, decl_rx)]
    return decl_rx, verb_rx


def contradictions2(b1, sem, text, exempt=lambda row: False):
    """contradictions() de B1 con las declaraciones de B2, más B2 cerrada, integrada, productiva o publicada."""
    decl_rx, verb_rx = sem
    out = []
    for body in b1.sentences(text, cite=True, exempt=exempt):
        if b1.EXAMPLE_PREFIX_RX.match(body.strip(' |-')):
            continue
        found = []
        for rx, allowed in decl_rx:
            for m in rx.finditer(body):
                found.append((m, allowed, b1.state_value(bool(m.group(2) or m.group(3)), m.group(4), body[m.end():])))
        for rx, allowed, decl in verb_rx:
            for m in rx.finditer(body):
                if decl.match(body, m.start('subj')):
                    continue
                k = next(int(g[1:]) for g, v in m.groupdict().items() if v and g.startswith('v'))
                found.append((m, allowed, b1.state_value(bool(m.group('neg')), b1.DECL_VERBS[k][1], body[m.end():])))
        for m in B2_FORBIDDEN_RX.finditer(body):
            if any(t in b1.NEG_WORDS or t.startswith(b1.NEG_PREFIXES) for t in m.group(1).split()):
                continue
            found.append((m, ('implementad',), m.group(2)))
        for m, allowed, value in found:
            if b1.admitted(value, allowed):
                continue
            if b1.DECL_NEG_RX.search(re.split(r'[.,;:!?|]', body[:m.start()])[-1]):
                continue
            out.append(f'«{m.group(0).strip()}»')
        out += b1.g0sbx_unrestricted(body) + b1.approval_grants(body)
    return out


def case_rows2(b1):
    """Filas «| NB2-xx | REGLA | descripción |» de los documentos que describen un negativo del gate: no son
    afirmaciones (como los casos NB de B1)."""
    rows = {tuple(b1.row_cell(x) for x in (cid, rule, what)) for cid, rule, what, *_ in
            NB2_STORE + NB2_REPO + NB2_REPO_EXTRA}

    def exempt(sentence):
        cells = tuple(b1.row_cell(c) for c in sentence.strip().strip('|').split('|'))
        return len(cells) == 3 and cells in rows
    return exempt


# ---------------------------------------------------------------- reglas propias de B2 sobre el repositorio
def r2_ctx(S, S2):
    out = list(S2['errors'])
    if out:
        return out
    out += list(S.get('env', ['entorno de Python no verificable (falla cerrado)']))
    if not S2['inside']:
        out.append('no es un árbol de trabajo Git')
    if S2['branch'] not in BRANCHES:
        out.append(f'rama no permitida o HEAD separado: «{S2["branch"]}»')
    out += [f'{name} no es ancestro de HEAD' for name, ok in S2['ancestors'].items() if not ok]
    if S2['shallow']:
        out.append('repositorio superficial: la historia no es completa (falla cerrado)')
    return out


def r2_scp(S2):
    if S2['errors']:
        return ['alcance no verificable (falla cerrado)']
    out = []
    for where, delta in S2['delta'].items():
        for status, path in sorted(delta):
            if SCOPE2.get(path) != status:
                out.append(f'{where}: cambio fuera del delta autorizado de B2 o con estado inesperado: {status} {path}')
    present = {p for _, p in S2['delta']['HEAD'] | S2['delta']['árbol']} | {p for p in S2['untracked'] if SCOPE2.get(p) == 'A'}
    missing = sorted(p for p, status in SCOPE2.items() if status == 'A' and p not in present)
    if missing:
        out.append(f'rutas obligatorias de B2 ausentes del delta: {missing}')
    stray = sorted(p for p in S2['untracked'] if SCOPE2.get(p) != 'A')
    if stray:
        out.append(f'archivos sin seguimiento fuera del delta de B2: {stray[:5]}')
    return out


def r2_fsy(b1, S, S2):
    if S2['errors']:
        return ['sistema de archivos no verificable (falla cerrado)']
    out = list(b1.r_fsy(S))      # runtime, dataset y evidencia frente a la base; carpetas de B1; enlaces (gate de B1)
    if S2['surfaces'][B1_BASE] != S2['surfaces'][B2_BASE]:
        out.append('las superficies del runtime difieren entre la base de B1 y la de B2: comparación no válida')
    for folder, (disk, problems, tree) in S2['folders'].items():
        out += problems
        want = FOLDERS[folder]
        for where, found in (('disco', disk), ('árbol de HEAD', tree)):
            if found != want:
                out.append(f'{folder}: contenido en {where} distinto de la lista exacta: extra={sorted(found - want)[:3]} '
                           f'faltan={sorted(want - found)[:3]}')
    artifacts = sorted(p for p in S2['listing'] if SQLITE_ARTIFACT.search(p))
    if artifacts:
        out.append(f'archivos de base de datos SQLite en el repositorio: {artifacts[:5]}')
    links = sorted(p for p in B2_FILES + GOV_PATHS + SET_B if not no_link(p))
    if links:
        out.append(f'enlaces en rutas de B2, de B1-FREEZE o de gobierno: {links[:3]}')
    return out


def r2_dep(S2):
    if S2['errors']:
        return ['código no verificable (falla cerrado)']
    return [f'{p}: código fuera de B2 que usa el almacén o sus nombres internos' for p in S2['py_refs']]


def r2_gov(b1, S2, sem):
    """Trece estados exactos, F35-SBX-B solo INICIADA, contenido igual al blob histórico de B1 o al nuevo de B2 (cuál
    rige lo decide B1F por la ascendencia) y ninguna declaración contradictoria ni afirmación que habilite capacidades."""
    if S2['errors']:
        return ['gobierno no verificable (falla cerrado)']
    out = list(S2['gov_new_problems'])
    for path in GOV_PATHS:
        data, old, new = S2['gov'][path], S2['gov_old'][path], S2['gov_new'].get(path)
        if data is None or new is None:
            out.append(f'{path}: ilegible o sin blob nuevo calculable (falla cerrado)')
            continue
        if data not in (old, new):
            out.append(f'{path}: contenido distinto del blob histórico de B1 y del blob nuevo de B2')
        text = data.decode('utf-8', 'replace')
        sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != b1.STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        header = '\n'.join(ln for ln in text.splitlines() if ln.startswith('Última actualización:'))
        b_states = {' '.join(m.split()) for m in b1.B_STATE_RX.findall(section + '\n' + header)}
        if b_states != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(b_states)}')
        before = set(old.decode('utf-8', 'replace').splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        bad = contradictions2(b1, sem, section + '\n' + header + '\n' + added)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    return out


def r2_cap(b1, S2, sem, exempt, cases):
    """P17 y P18, más el contenido de los archivos de B2 con las reglas de B1 (UTF-8 sin NUL, CR ni BOM; en los
    documentos, sin datos personales, afirmaciones positivas ni declaraciones contradictorias)."""
    out = [f'{pid}: {cases.get(pid, (False, "no ejecutado"))[1]}' for pid in ('P17', 'P18')
           if not cases.get(pid, (False, ''))[0]]
    if S2['errors']:
        return out + ['contenido no verificable (falla cerrado)']
    for path in B2_FILES:
        data = S2['files'].get(path)
        if data is None or len(data) > b1.MAX_BYTES or b'\x00' in data or b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
            out.append(f'{path}: ilegible, binario, CR, BOM o tamaño excesivo')
            continue
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            out.append(f'{path}: no es UTF-8')
            continue
        if not path.endswith('.md'):
            continue
        hits = [m.group(0) for rx in b1.PII for m in [rx.search(text)] if m]
        if hits:
            out.append(f'{path}: posible dato personal: {hits[:2]}')
        claims = b1.positive_claims(text, exempt=exempt)
        if claims:
            out.append(f'{path}: afirmación positiva que habilita una capacidad prohibida: {claims[:2]}')
        bad = contradictions2(b1, sem, text, exempt=exempt)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:2]}')
    return out


# ---------------------------------------------------------------- NB2: negativos del repositorio (estado mutado)
def _gov_edit(old, new):
    def apply(S, S2):
        for p in GOV_PATHS:
            S2['gov'][p] = S2['gov'][p].replace(old.encode('utf-8'), new.encode('utf-8'), 1)
    return apply


def _doc_add(path, line):
    def apply(S, S2):
        S2['files'][path] = S2['files'][path] + f'\n{line}\n'.encode('utf-8')
    return apply


def _add_db(S, S2):
    S2['listing'].add('docs/academico/tools/f35sbxb2/almacen.db')
    S2['folders']['docs/academico/tools/f35sbxb2'][0].add('docs/academico/tools/f35sbxb2/almacen.db')


# (caso, regla, descripción, mutación del estado, fragmento exigido en las violaciones de la regla)
NB2_REPO = [
    ('NB2-18', 'SCP', 'archivo del runtime en el delta de B2',
     lambda S, S2: S2['delta']['HEAD'].add(('A', 'app/Models/Extra.php')), 'fuera del delta autorizado'),
    ('NB2-19', 'SCP', 'gobierno eliminado en el árbol de trabajo',
     lambda S, S2: S2['delta']['árbol'].add(('D', 'CLAUDE.md')), 'fuera del delta autorizado'),
    ('NB2-20', 'FSY', 'base de datos en archivo junto al almacén', _add_db, 'SQLite'),
    ('NB2-21', 'DEP', 'otro módulo del repositorio usa el almacén',
     lambda S, S2: S2['py_refs'].append('docs/academico/tools/f34/validate_f34.py'), 'usa el almacén'),
    ('NB2-22', 'GOV', 'G0 real declarada APROBADA', _gov_edit('- G0 real = NO APROBADA', '- G0 real = APROBADA'),
     'trece estados'),
    ('NB2-23', 'GOV', 'B2 declarada cerrada e integrada en el gobierno',
     _gov_edit('- Datos reales = PROHIBIDOS\n', '- Datos reales = PROHIBIDOS\n\nB2 = CERRADA E INTEGRADA.\n'),
     'declaraciones de estado'),
    ('NB2-24', 'CTX', 'rama no permitida', lambda S, S2: S2.__setitem__('branch', 'feature/otra'), 'rama no permitida'),
    ('NB2-25', 'CAP', 'un documento de B2 afirma que el motor recomienda quién continúa',
     _doc_add(B2_DOCS[0], 'El motor recomendará quién debe continuar.'), 'afirmación positiva'),
    ('NB2-26', 'CAP', 'dato personal en un documento de B2',
     _doc_add(B2_DOCS[0], 'Contacto: ana.torres@correo.pe'), 'dato personal'),
    ('NB2-27', 'GOV', 'F35-SBX-B declarada cerrada en el gobierno',
     _gov_edit('F35-SBX-B INICIADA solo como sandbox', 'F35-SBX-B CERRADA solo como sandbox'), 'solo INICIADA'),
]


def run_nb2_repo(b1, S, S2, sem, exempt, cases):
    """Cada negativo muta en memoria una copia del estado y la regla correspondiente debe detectarlo."""
    rules = {'SCP': lambda T, T2: r2_scp(T2), 'FSY': lambda T, T2: r2_fsy(b1, T, T2), 'DEP': lambda T, T2: r2_dep(T2),
             'GOV': lambda T, T2: r2_gov(b1, T2, sem), 'CTX': r2_ctx,
             'CAP': lambda T, T2: r2_cap(b1, T2, sem, exempt, cases)}
    results = {}
    for cid, rule, what, mutate, fragment in NB2_REPO:
        try:
            T, T2 = copy.deepcopy(S), copy.deepcopy(S2)
            mutate(T, T2)
            found = rules[rule](T, T2)
        except Exception as e:      # mutación no aplicable o estado incompleto: el negativo no demuestra nada
            results[cid] = (False, f'no evaluable ({e.__class__.__name__}: {e})')
            continue
        hit = [p for p in found if fragment in p]
        results[cid] = (bool(hit), f'{rule}: {hit[0][:110]}' if hit else f'{rule} no lo detecta')
    try:
        problems, _, _ = b1f_check(Repo(ROOT), B1_ANCHOR, B1_CLOSURE, GOVERNANCE_DELTA, '0' * 40, root=ROOT)
        hit = [p for p in problems if 'distinta de la registrada' in p]
        results['NB2-28'] = (bool(hit), f'B1F: {hit[0][:110]}' if hit else 'B1F no lo detecta')
    except (GitError, OSError, ValueError) as e:
        results['NB2-28'] = (False, f'no evaluable ({e})')
    return results


NB2_REPO_EXTRA = [('NB2-28', 'B1F', 'transición registrada distinta de la derivada')]


def report(checks):
    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    print(f'validate_f35sbxb2: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


RULE_ORDER = ('CTX', 'B1F', 'AIN', 'B0F', 'HST', 'SBX', 'SCP', 'FSY', 'FLG', 'DEP', 'PRE', 'STA', 'DYN', 'DET', 'ISO',
              'PUR', 'DAT', 'CAP', 'GOV')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    try:
        b1 = load_b1_gate()
    except (GitError, OSError) as e:
        b1 = None
        add(False, f'gate de B1 no verificable ({e}): falla cerrado')
    if b1 is None:
        add(False, 'gate de B1 distinto de su blob en el ancla o ilegible: no se ejecuta nada (falla cerrado)')
        report(checks)
    # collect() de B1 sin __main__ registrado: su control de módulos del repositorio ya cargados (DH-B13) no debe
    # tomar este gate por código no verificado. El almacén todavía no se ha cargado.
    running = sys.modules.pop('__main__', None)
    try:
        S = b1.collect()
    finally:
        if running is not None:
            sys.modules['__main__'] = running
    S2 = collect2(b1)
    sem, exempt = semantics(b1), case_rows2(b1)
    fixtures = b1f_fixtures()
    store_bytes = real_bytes(STORE)
    store_rules, cases, ctx = run_store_rules(b1, store_bytes, baseline=None if S2['errors'] else S2['listing'])
    nb2 = run_nb2_store(b1, store_bytes, ctx) if ctx is not None else {}
    nb2.update(run_nb2_repo(b1, S, S2, sem, exempt, cases))
    # P25, P32 y P33: B1F sobre la historia real y sobre las historias desechables.
    real_b1f = ['B1F no evaluable (falla cerrado)'] if S2['errors'] else list(S2['b1f'])
    fixture_fail = [f'{cid} ({what}): {detail}' for cid, (ok, what, detail) in sorted(fixtures.items()) if not ok]
    p25 = real_b1f + [x for x in fixture_fail if not x.startswith(('F05', 'F10'))]
    cases['P25'] = (not p25 and len(fixtures) >= 21, f'{p25[:2]}' if p25 else
                    f'historia real íntegra ({S2.get("b1f_commits", 0)} commits desde el ancla; transición derivada: '
                    f'{S2.get("transition") or "aún no materializada"}); escenarios F01–F04, F06–F09 y F11–F21 correctos')
    for pid, cid in (('P32', 'F05'), ('P33', 'F10')):
        ok, what, detail = fixtures.get(cid, (False, '', 'no ejecutado'))
        cases[pid] = (ok, f'{cid} ({what}): {detail}')
    rules = {'CTX': r2_ctx(S, S2), 'B1F': real_b1f + fixture_fail,
             'AIN': b1.r_ain(S), 'B0F': b1.r_b0f(S), 'HST': b1.r_hst(S), 'SBX': b1.r_sbx(S),
             'SCP': r2_scp(S2), 'FSY': r2_fsy(b1, S, S2), 'FLG': b1.r_flg(S),
             'DEP': store_rules['DEP'] + r2_dep(S2), 'PRE': store_rules['PRE'], 'STA': store_rules['STA'],
             'DYN': store_rules['DYN'] + [f'{pid}: {cases[pid][1]}' for pid in ('P25', 'P32', 'P33') if not cases[pid][0]],
             'CAP': r2_cap(b1, S2, sem, exempt, cases), 'GOV': r2_gov(b1, S2, sem)}
    for gid in GROUPS:
        rules[gid] = store_rules.get(gid, [f'{gid} no evaluado: el almacén no llegó a ejecutarse (falla cerrado)'])
    for rid in RULE_ORDER:
        viol = rules[rid]
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:3]}' if viol else ''))
    for pid in sorted(set(STORE_CASES) | {'P25', 'P32', 'P33'}):
        ok, detail = cases.get(pid, (False, 'no ejecutado'))
        add(ok, f'{pid}: {detail}')
    for cid in sorted(fixtures):
        ok, what, detail = fixtures[cid]
        add(ok, f'{cid} [B1F] {what}: {detail}')
    for cid, rule, what, *_ in NB2_STORE + NB2_REPO + NB2_REPO_EXTRA:
        ok, detail = nb2.get(cid, (False, 'no ejecutado'))
        add(ok, f'{cid} [{rule}] {what}: {detail}')
    print(f'INFO transición de gobierno de B2 derivada: {S2.get("transition") or "ninguna (aún no materializada)"}; '
          f'registrada: {B2_GOVERNANCE_TRANSITION or "ninguna"}')
    report(checks)


if __name__ == '__main__':
    main()
