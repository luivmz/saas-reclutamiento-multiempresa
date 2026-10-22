"""F35-SBX-B — B3: pipeline determinista de evidencia sintética (sbxb_pipeline.py).

Uso:  python -I docs/academico/tools/f35sbxb3/sbxb_pipeline.py [--fallo ORG-SX:N]   (sin -I, se relanza)

Recorre los doce pasos de la arquitectura de F35-SBX-A sobre sus fixtures, para ORG-S1, ORG-S2 y ORG-S3, con el
almacén efímero de B2 sin modificarlo, y escribe por la salida estándar un único informe en JSON canónico (UTF-8, LF).
Código de salida: 0 si el resultado es completado, 1 si es fallido y 2 si la invocación no es válida.

Contrato y diseño: docs/academico/evidencia-sbx-b3/F35SBXB_B3_Pipeline.md. Código de desarrollo de un sandbox
académico: no escribe archivos ni usa red, variables de entorno o nada del runtime; no persiste nada fuera del almacén
':memory:' de B2; no calcula puntajes y no ordena, sugiere, selecciona ni descarta personas. RF-23 sigue siendo una
decisión humana y RF-29, experimental.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación: python -I, relanzado con os.spawnv.
if __name__ == '__main__' and not sys.flags.isolated:
    _argv = [sys.executable, '-I', '-B'] + (['-X', 'utf8'] if sys.flags.utf8_mode else []) + \
        [os.path.abspath(__file__)] + sys.argv[1:]
    if os.name == 'nt':
        _argv = ['"' + a.replace('"', '\\"') + '"' if (' ' in a or '\t' in a) else a for a in _argv]
    sys.exit(os.spawnv(os.P_WAIT, sys.executable, _argv))

import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import types  # noqa: E402
import unicodedata  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))

# ---------------------------------------------------------------- entradas autorizadas y su raíz de confianza
STORE_REL = 'docs/academico/tools/f35sbxb2/sbxb_store.py'
STORE_SHA256 = '0f96ed8f305d649bf906970e6b3baa179df95f373a172887e25cba2a7beb8663'  # blob 09ac588 (candidato de B2)
SBX_DIR = 'docs/academico/evidencia-sbx/'
SBX_MANIFEST = SBX_DIR + 'fixtures/manifest.json'
SBX_MANIFEST_SHA256 = '2df919ebde68fdf959b169d0249141422d84dc3ae4cfc29a9d2601735c915a4b'  # congelado en E
SBX_CONTRACT = SBX_DIR + 'contrato/f35sbx_contract.json'
F34_DIR = 'docs/academico/datos-sinteticos/dataset/'
F34_MANIFEST = F34_DIR + 'manifest.json'
F34_MANIFEST_SHA256 = '079aae87916530b99fb97f22414d8c7d4938e8b7edd7d3527e5fa9db555af431'  # el que registra A
F34_FILES = ('evidence.csv', 'criteria.csv', 'vacancies.csv', 'applications.csv')
TENANTS = ('ORG-S1', 'ORG-S2', 'ORG-S3')
FIXTURES = {o: SBX_DIR + f'fixtures/{o}_evidencias.json' for o in TENANTS}
INPUTS = frozenset({STORE_REL, SBX_MANIFEST, SBX_CONTRACT, F34_MANIFEST, *FIXTURES.values(),
                    *(F34_DIR + n for n in F34_FILES)})
# Escenarios del oráculo: la semilla y el reloj lógico de cada fixture de A (run.seed y run.clock_start).
SCENARIOS = {'ORG-S1': (20261008, '2026-10-07T09:00:00'), 'ORG-S2': (20261009, '2026-10-07T09:00:00'),
             'ORG-S3': (20261010, '2026-10-07T09:00:00')}

REPORT_VERSION = 'f35sbxb3-report-1.0.0'
CONTRACT_VERSION_A = 'f35sbx-contract-1.0.0'
DATASET_VERSION = 'f34-synth-1.1.0'
HASH_ALGORITHM = 'f35sbx-content-sha256-v1'
MARKER = '[SINTÉTICO]'
GENESIS = '0' * 64
PATH = ('pendiente', 'validando', 'registrado', 'transformado', 'en_revision', 'revisado', 'completado')
ACTIONS = ('fixture_verificado', 'esquema_validado', 'sintetico_verificado', 'hash_calculado', 'provenance_registrada',
           'tenant_validado', 'revision_simulada_registrada', 'ejecucion_cerrada')
EVIDENCE_KINDS = ('formulario', 'nota_entrevista', 'prueba')
PER_TENANT = 2
STEP_NAMES = {1: 'fixture_verificado', 2: 'esquema_validado', 3: 'sintetico_verificado', 4: 'hash_calculado',
              5: 'provenance_registrada', 6: 'transformado', 7: 'tenant_validado', 8: 'revision_simulada',
              9: 'resultado_experimental', 10: 'auditoria_encadenada', 11: 'ejecucion_cerrada', 12: 'purga'}
EXTRA_STEPS = {0: 'entradas', 13: 'informe'}
INJECTED = 'E-INYECTADO'
TABLES = ('tenant_context', 'pipeline_run', 'pipeline_event', 'evidence_source', 'evidence_record',
          'evidence_provenance', 'simulated_review', 'audit_entry')
COUNTS = {'tenant_context': 1, 'pipeline_run': 1, 'pipeline_event': 7, 'evidence_source': 2, 'evidence_record': 2,
          'evidence_provenance': 2, 'simulated_review': 2, 'audit_entry': 8}
RECEIPT_KEYS = frozenset({'closure_kind', 'pipeline_run_id', 'synthetic_organization_id', 'final_state', 'failed_event',
                          'failed_event_record', 'error_code', 'last_event_hash', 'counts', 'file_backed', 'observed',
                          'connection', 'post_close_check', 'receipt_hash'})
TS_RX = re.compile(r'20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]')
CODE_RX = re.compile(r'E-[A-Z]{2,12}')


class PipelineError(Exception):
    """Error controlado de un paso: código E-[A-Z]{2,12}, paso (0 entradas, 1..12, 13 informe) y mensaje fijo."""

    def __init__(self, step, code, message):
        super().__init__(f'{code}: {message}')
        self.step, self.code, self.message = step, code, message


class PipelineFailure(Exception):
    """Fallo de un run, con el cierre del almacén ya resuelto (comprobante, diagnóstico o no_disponible)."""

    def __init__(self, org, step, code, message, closure):
        super().__init__(f'{org} paso {step}: {code}')
        self.org, self.step, self.code, self.message, self.closure = org, step, code, message, closure


# ---------------------------------------------------------------- funciones de A (validate_f35sbx.py, congelado en E)
def canon(obj):
    """JSON canónico de A: claves ordenadas, separadores sin espacios, UTF-8 sin escapar."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(obj):
    return hashlib.sha256(canon(obj)).hexdigest()


def t1(text):
    """T1, exactamente normalize_text de A: Unicode NFC y espacios colapsados."""
    return ' '.join(unicodedata.normalize('NFC', text).split())


def content_hash(org, origin, criterion, kind, text):
    return sha({'algorithm': HASH_ALGORITHM, 'synthetic_organization_id': org, 'origin_record_id': origin,
                'criterion_ref': criterion, 'evidence_kind': kind, 'text': text})


def chain_problems(items, key, prev_key, label):
    """chain_hash de A eslabón por eslabón: génesis de 64 ceros y SHA-256 del objeto sin su propio campo."""
    prev, out = GENESIS, []
    for item in items:
        if item.get(prev_key) != prev:
            out.append(f'{label}: eslabón roto')
        if item.get(key) != sha({k: v for k, v in item.items() if k != key}):
            out.append(f'{label}: hash recalculado distinto')
        prev = item.get(key)
    return out


# ---------------------------------------------------------------- lectura de entradas (TSBB-06) y carga del almacén
def resolve_input(rel):
    """Ruta absoluta de una entrada autorizada: relativa, sin «..» ni barras invertidas y de la lista cerrada."""
    if type(rel) is not str or rel.startswith('/') or os.path.isabs(rel) or '\\' in rel or \
            '..' in rel.split('/') or rel not in INPUTS:
        raise PipelineError(0, 'E-RUTA', 'ruta de entrada no autorizada')
    return os.path.join(ROOT, *rel.split('/'))


def read_input(rel, overrides=None):
    path = resolve_input(rel)
    if overrides and rel in overrides:
        return overrides[rel]
    try:
        with open(path, 'rb') as handle:
            return handle.read()
    except OSError:
        raise PipelineError(0, 'E-ENTRADA', 'entrada autorizada ilegible') from None


def load_store():
    """El almacén de B2 desde sus bytes verificados (SHA-256 del candidato), sin __pycache__ ni ruta de importación.
    Es la única ejecución dinámica del pipeline."""
    raw = read_input(STORE_REL)
    if hashlib.sha256(raw).hexdigest() != STORE_SHA256:
        raise PipelineError(0, 'E-ALMACEN', 'el almacén de B2 no coincide con su SHA-256 registrado')
    path = resolve_input(STORE_REL)
    module = types.ModuleType('sbxb_store')
    module.__file__ = path
    exec(compile(raw, path, 'exec', dont_inherit=True), module.__dict__)
    return module


def _json(raw, what):
    def no_duplicates(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError('clave duplicada')
        return dict(pairs)
    try:
        if b'\r' in raw or b'\x00' in raw or raw.startswith(b'\xef\xbb\xbf'):
            raise ValueError('CR, NUL o BOM')
        return json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, ValueError):
        raise PipelineError(0, 'E-ENTRADA', f'{what}: JSON no válido') from None


def _csv(raw):
    return list(csv.DictReader(re.split(r'(?<=\n)', raw.decode('utf-8'))))


def load_inputs(overrides=None):
    """Manifest F34 (SHA-256 registrado por A), sus cuatro CSV, manifest y contrato de A. Los fixtures los lee el
    paso 1 de cada tenant."""
    f34m_raw = read_input(F34_MANIFEST, overrides)
    if hashlib.sha256(f34m_raw).hexdigest() != F34_MANIFEST_SHA256:
        raise PipelineError(0, 'E-ENTRADA', 'manifest F34 distinto del registrado por A')
    f34m = _json(f34m_raw, 'manifest F34')
    if f34m.get('dataset_version') != DATASET_VERSION or f34m.get('source') != 'synthetic':
        raise PipelineError(0, 'E-ENTRADA', 'el dataset F34 no es f34-synth-1.1.0 sintético')
    files, tables = {}, {}
    for name in F34_FILES:
        raw = read_input(F34_DIR + name, overrides)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != f34m['files'][name]['sha256']:
            raise PipelineError(0, 'E-ENTRADA', f'{name} distinto de su manifest F34')
        files[name] = digest
        try:
            tables[name] = _csv(raw)
        except (UnicodeDecodeError, csv.Error):
            raise PipelineError(0, 'E-ENTRADA', f'{name} no legible como CSV UTF-8') from None
    sbx_raw = read_input(SBX_MANIFEST, overrides)
    if hashlib.sha256(sbx_raw).hexdigest() != SBX_MANIFEST_SHA256:
        raise PipelineError(0, 'E-ENTRADA', 'manifest de A distinto del congelado en E')
    sbx = _json(sbx_raw, 'manifest de A')
    if sbx['f34']['evidence_sha256'] != files['evidence.csv'] or \
            sbx['f34']['manifest_sha256'] != hashlib.sha256(f34m_raw).hexdigest():
        raise PipelineError(0, 'E-ENTRADA', 'el manifest de A no registra este dataset F34')
    contract_raw = read_input(SBX_CONTRACT, overrides)
    entry = sbx['files']['contrato/f35sbx_contract.json']
    if hashlib.sha256(contract_raw).hexdigest() != entry['sha256'] or len(contract_raw) != entry['bytes']:
        raise PipelineError(0, 'E-ENTRADA', 'contrato de A distinto de su manifest')
    try:
        apps = {r['application_token']: r['organization_token'] for r in tables['applications.csv']}
        vacs = {r['vacancy_token']: r['organization_token'] for r in tables['vacancies.csv']}
        crit = {r['criterion_id']: vacs[r['vacancy_token']] for r in tables['criteria.csv']}
        evidence = {r['synthetic_record_id']: dict(r, organization=apps[r['application_token']])
                    for r in tables['evidence.csv']}
    except KeyError:
        raise PipelineError(0, 'E-ENTRADA', 'dataset F34 con columnas o referencias distintas del contrato') from None
    return {'f34_manifest_sha256': hashlib.sha256(f34m_raw).hexdigest(), 'f34_files_sha256': files,
            'sbx_manifest_sha256': hashlib.sha256(sbx_raw).hexdigest(), 'sbx_manifest': sbx,
            'sbx_contract_sha256': entry['sha256'], 'contract': _json(contract_raw, 'contrato de A'),
            'evidence': evidence, 'criteria_org': crit, 'overrides': overrides or {}}


# ---------------------------------------------------------------- comprobaciones de A que reproducen los pasos
SCHEMA_KEYS = frozenset({'type', 'properties', 'required', 'additionalProperties', 'items', 'minItems', 'maxItems',
                         'const', 'enum', 'pattern', 'maxLength', 'minLength', 'minimum', 'maximum', '$ref'})
PY_TYPES = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool}


def check_schema(value, schema, defs, path='$'):
    """check_schema de A (SCH): JSON Schema mínimo y cerrado. Una palabra clave o un tipo desconocidos, una referencia
    inexistente o un objeto sin additionalProperties=false fallan; los patrones se aplican con fullmatch."""
    if not isinstance(schema, dict):
        return [f'{path}: esquema ilegible']
    if set(schema) - SCHEMA_KEYS:
        return [f'{path}: palabra clave de esquema desconocida {sorted(set(schema) - SCHEMA_KEYS)}']
    if '$ref' in schema:
        name = str(schema['$ref']).removeprefix('#/$defs/')
        if name not in defs:
            return [f'{path}: referencia inexistente']
        return check_schema(value, defs[name], defs, path)
    kind = schema.get('type')
    if kind is not None:
        if kind not in PY_TYPES:
            return [f'{path}: tipo de esquema desconocido']
        if not isinstance(value, PY_TYPES[kind]) or (kind == 'integer' and isinstance(value, bool)):
            return [f'{path}: tipo {type(value).__name__}, se exige {kind}']
    out = []
    if 'const' in schema and (value != schema['const'] or type(value) is not type(schema['const'])):
        out.append(f'{path}: valor distinto de la constante del contrato')
    if 'enum' in schema and value not in schema['enum']:
        out.append(f'{path}: valor fuera del enum')
    if isinstance(value, str):
        if 'pattern' in schema and not re.fullmatch(schema['pattern'], value):
            out.append(f'{path}: valor fuera del patrón')
        if len(value) > schema.get('maxLength', len(value)) or len(value) < schema.get('minLength', 0):
            out.append(f'{path}: longitud fuera de rango')
    if isinstance(value, int) and not isinstance(value, bool):
        if 'minimum' in schema and value < schema['minimum'] or 'maximum' in schema and value > schema['maximum']:
            out.append(f'{path}: entero fuera de rango')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', len(value)):
            out.append(f'{path}: número de elementos fuera de rango')
        for i, item in enumerate(value):
            out += check_schema(item, schema.get('items', {}), defs, f'{path}[{i}]')
    if isinstance(value, dict):
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is not False:
            out.append(f'{path}: objeto sin additionalProperties=false')
        if set(value) - set(props):
            out.append(f'{path}: campos no permitidos {sorted(set(value) - set(props))}')
        if set(schema.get('required', [])) - set(value):
            out.append(f'{path}: campos ausentes {sorted(set(schema.get("required", [])) - set(value))}')
        for k in props:
            if k in value:
                out += check_schema(value[k], props[k], defs, f'{path}.{k}')
    return out


DASHES = '‐‑‒–—―−﹘﹣－'


def fold(text):
    """fold de A en lo que afecta a sus detectores de contenido: NFKC, sin caracteres de formato (Cf), guiones Unicode
    entre caracteres visibles como «-» y espacios colapsados. Las reescrituras de RF y de «Scope C» de A se omiten:
    sirven a las proposiciones de los documentos, no a estos detectores."""
    t = unicodedata.normalize('NFKC', text or '')
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Cf')
    t = re.sub(r'(?<=\S)[' + DASHES + r'](?=\S)', '-', t)
    return re.sub(r'[ \t]+', ' ', t)


def tokens(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return set(re.split(r'[^a-z0-9]+', s)) - {''}


def walk(obj, path=''):
    """(ruta, clave, valor) de cada clave y de cada valor hoja, como walk de A."""
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


def decoded_problems(obj, path=''):
    """decoded_problems de A: ninguna clave ni texto decodificado con caracteres de formato (Cf) o que NFKC cambie."""
    out = []
    items = obj.items() if isinstance(obj, dict) else enumerate(obj) if isinstance(obj, list) else []
    for k, v in items:
        here = f'{path}.{k}' if isinstance(obj, dict) else f'{path}[{k}]'
        for x in (k, v):
            if isinstance(x, str) and (any(unicodedata.category(c) == 'Cf' for c in x)
                                       or unicodedata.normalize('NFKC', x) != x):
                out.append(f'{here}: caracteres invisibles o de compatibilidad Unicode')
        if isinstance(v, (dict, list)):
            out += decoded_problems(v, here)
    return out


# Detectores de A (PII, MED, CAP, PER y STO), con sus mismos patrones y exenciones.
F34_EVIDENCE = F34_DIR + 'evidence.csv'
HASH_KEY = re.compile(r'(_hash|_sha256|^content_hash|^hash_before|^hash_after)$')
PII_FIELD = re.compile(r'(^|_)(real|nombres?|names?|apellidos?|surname|emails?|correos?|mail|tel[eé]fonos?|phones?|'
                       r'celular|dni|ruc|pasaporte|passport|documento_identidad|direcci[oó]n|address|domicilio|'
                       r'nacimiento|birth\w*|edad|age|sexo|sex|g[eé]nero|gender|etnia|salud|health|religion|foto|photo)'
                       r'(_|$)', re.I)
PII_VALUE = (re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), re.compile(r'https?://|www\.', re.I),
             re.compile(r'(?<![\w-])\d{11}(?![\w-])'), re.compile(r'(?<![\w-])\d{8}(?![\w-])'),
             re.compile(r'(?<![\w-])\+?\d[\d ]{8,}\d(?![\w-])'))
MEDIA_FIELD = re.compile(r'(^|_)(cv|cvs|curriculum|pdf|docx?|imagen(es)?|images?|img|fotos?|photos?|audios?|videos?|'
                         r'v[ií]deos?|media|adjuntos?|attachments?|archivos?|files?|blob|binary|binario|base64)(_|$)',
                         re.I)
MEDIA_FIELD_OK = frozenset({'origin_file', 'origin_file_sha256'})
MEDIA_EXT = re.compile(r'\.(pdf|docx?|odt|rtf|png|jpe?g|gif|bmp|tiff?|webp|heic|svg|mp3|wav|m4a|ogg|flac|aac|mp4|mov|'
                       r'avi|mkv|webm|wmv|zip|rar|7z|exe|bin|sqlite3?|db)\b', re.I)
MEDIA_VALUE = (MEDIA_EXT, re.compile(r'data:[\w.+/-]*;base64', re.I), re.compile(r'[A-Za-z0-9+/]{40,}={0,2}'),
               re.compile(r'[\x00-\x08\x0b-\x1f\x7f]'), re.compile(r'\b(CVs?|curr[ií]cul\w*)\b', re.I))
CAP_TOKENS = frozenset({
    'score', 'scores', 'scoring', 'puntaje', 'puntajes', 'puntuacion', 'rank', 'ranking', 'rankings', 'ranked',
    'recommend', 'recommendation', 'recommendations', 'recommended', 'recomendacion', 'recomendado', 'recomienda',
    'best', 'mejor', 'selected', 'selection', 'seleccion', 'seleccionado', 'automatic', 'hire', 'hired', 'contratado',
    'contratar', 'ocr', 'parsing', 'parse', 'parser', 'extraction', 'extract', 'extraccion', 'embedding', 'embeddings',
    'vector', 'vectors', 'vectorial', 'semantic', 'semantica', 'semantico', 'llm', 'gpt', 'similarity', 'similitud',
    'apto', 'apta', 'aptitud', 'idoneidad', 'idoneo', 'merito', 'desempeno', 'performance', 'personalidad',
    'personality', 'emocion', 'emotion', 'honestidad', 'honesty', 'inteligencia', 'intelligence', 'estres', 'stress',
    'biometria', 'biometric', 'suitability', 'fit', 'percentile', 'percentil', 'level', 'nivel'})
PERSON_VALUE = re.compile(r'(?<![\w-])(?:APP|PER|PER-S|EV|EVA|CAND|POST|USR|USER)-[\w-]*\d', re.I)
PERSON_FIELD = re.compile(r'(^|_)(person|persona|personas|people|candidate|candidato|candidatos|applicant|application|'
                          r'postulante|postulacion|evaluator|evaluador|evaluado|user|usuario|employee|empleado|'
                          r'human_level|rubric_points)(_|$)', re.I)
PROD_FIELD = re.compile(r'(^|_)(table|tabla|db|database|connection|conexion|dsn|endpoint|url|uri|host|storage|'
                        r'persist\w*|deploy\w*|despliegue|webhook|api)(_|$)', re.I)
PROD_VALUE = re.compile(r'pgsql|postgres|mysql|mariadb|sqlite|redis|\bDB_\w+|\.env\b|storage/|database/|(?<![\w-])app/|'
                        r'routes/|config/|resources/|ml-service|ML_SERVICE|localhost|127\.0\.0\.1|0\.0\.0\.0|https?://|'
                        r'audit_logs|insert\s+into|producci[oó]n|productiv|production', re.I)
ADJUNTOS = re.compile(r'g0-evidence|adjuntos', re.I)
TEXT_RX = re.compile(r'\[SINTÉTICO\] [^<>\x00-\x1f\x7f]{1,380}')
ID_KEYS = ('fixture_id', 'pipeline_run_id', 'event_id', 'source_id', 'synthetic_id', 'provenance_id', 'record_id',
           'review_id', 'audit_id', 'target_ref', 'simulation_actor')


def check_synthetic(record, org):
    """Paso 3 sobre una evidencia: los seis marcadores synthetic-only de A (SYN) y el texto en el patrón del contrato,
    sin datos personales, media, tokens de persona ni capacidades prohibidas."""
    if type(record) is not dict:
        return ['registro ilegible']
    rid, text = str(record.get('synthetic_id')), record.get('text_synthetic')
    out = [what for ok, what in (
        (rid.startswith(f'SBXE-{org}-'), 'marcador 1: identificador SBXE- del tenant'),
        (isinstance(text, str) and text.startswith(MARKER + ' '), 'marcador 2: texto con [SINTÉTICO]'),
        (record.get('source_type') == 'synthetic', 'marcador 3: source_type = synthetic'),
        (record.get('environment') == 'sandbox', 'marcador 4: environment = sandbox'),
        (record.get('hash_algorithm') == HASH_ALGORITHM, f'marcador 5: hash_algorithm = {HASH_ALGORITHM}'),
        (record.get('synthetic_organization_id') == org, 'marcador 6: tenant sintético')) if not ok]
    if not isinstance(text, str) or not TEXT_RX.fullmatch(text):
        return out + ['texto con marcado, caracteres de control o fuera del patrón']
    folded = fold(text)
    out += [f'posible dato personal en el texto ({i})' for i, rx in enumerate(PII_VALUE) if rx.search(folded)]
    out += [f'media o documento en el texto ({i})' for i, rx in enumerate(MEDIA_VALUE) if rx.search(folded)]
    if PERSON_VALUE.search(folded):
        out.append('token de persona en el texto')
    if tokens(folded) & CAP_TOKENS:
        out.append(f'capacidad prohibida en el texto {sorted(tokens(folded) & CAP_TOKENS)}')
    return out


def check_fixture_content(fixture):
    """Paso 3 sobre el fixture completo, como PII, MED, CAP, PER y STO de A más su decoded_problems: campos y valores
    de datos personales, media, capacidades, personas y destinos productivos, con las exenciones de A (claves de hash
    y origin_file del dataset F34)."""
    out = decoded_problems(fixture)
    for path, k, v in walk(fixture):
        key = str(k)
        if PII_FIELD.search(key) or PERSON_FIELD.search(key) or PROD_FIELD.search(key) or \
                (MEDIA_FIELD.search(key) and key not in MEDIA_FIELD_OK) or tokens(key) & CAP_TOKENS:
            out.append(f'{path}: campo no permitido')
        if isinstance(v, str) and PERSON_VALUE.search(v):
            out.append(f'{path}: token de persona')
        if isinstance(v, str) and not HASH_KEY.search(key):
            if any(rx.search(v) for rx in PII_VALUE) or tokens(v) & CAP_TOKENS or PROD_VALUE.search(v) or \
                    ADJUNTOS.search(v) or any(rx.search(v) and not (rx is MEDIA_EXT and v == F34_EVIDENCE)
                                              for rx in MEDIA_VALUE):
                out.append(f'{path}: valor no permitido')
    for source in fixture['sources']:
        if source.get('origin_file') != F34_EVIDENCE:
            out.append('origen fuera del dataset F34 autorizado')
    return out


def check_fixture_tenant(org, fixture, inputs):
    """Paso 7 sobre el oráculo, como ISO de A: organización e identificadores del tenant, y filas F34 y criterios de
    su organización."""
    out = []
    for path, k, v in walk(fixture):
        if k == 'synthetic_organization_id' and v != org:
            out.append(f'{path}: organización cruzada')
        if k in ID_KEYS and isinstance(v, str) and not v.endswith(org) and f'-{org}-' not in v:
            out.append(f'{path}: identificador de otro tenant')
    for source in fixture['sources']:
        row = inputs['evidence'].get(source.get('origin_record_id'))
        if row is None or row['organization'] != org:
            out.append('origen F34 de otra organización')
    for record in fixture['records']:
        if inputs['criteria_org'].get(record.get('criterion_ref'), org) != org:
            out.append('criterio de otra organización')
    return out


def check_scenario(org, fixture):
    """El escenario del run de B es el del oráculo del tenant: su semilla y su reloj lógico."""
    run = fixture.get('run') if isinstance(fixture, dict) else None
    if not isinstance(run, dict) or (run.get('seed'), run.get('clock_start')) != SCENARIOS[org]:
        return ['escenario distinto del oráculo del tenant']
    return []


def select_rows(inputs, org):
    """Regla de selección determinista de A: las dos primeras filas F34 vinculadas, sintéticas y de un tipo admitido
    de la organización, ordenadas por evidence_id."""
    rows = sorted((r for r in inputs['evidence'].values() if r['organization'] == org and r['state'] == 'vinculada'
                   and r['source_type_ev'] in EVIDENCE_KINDS and r['source_type'] == 'synthetic'),
                  key=lambda r: r['evidence_id'])
    return [r['synthetic_record_id'] for r in rows[:PER_TENANT]]


NAMESPACED = frozenset({'pipeline_run_id', 'event_id', 'audit_id', 'source_id', 'synthetic_id', 'record_id',
                        'provenance_id', 'review_id', 'target_ref'})


def check_tenant_rows(org, tables):
    """Paso 7: toda fila es del tenant y todo identificador de B lleva su espacio de nombres SBB*-<org>-<semilla>."""
    space = re.compile(r'SBB[RVASEPH]-' + re.escape(org) + r'-[0-9]{10}(-[0-9]{2}|-[0-9]{6})?')
    out = []
    for table, rows in tables.items():
        for row in rows:
            for k, v in row.items():
                if k == 'synthetic_organization_id' and v != org:
                    out.append(f'{table}: fila de otro tenant')
                elif k == 'simulation_actor' and v != f'SIMREV-{org}':
                    out.append(f'{table}: actor simulado de otro tenant')
                elif k in NAMESPACED and (type(v) is not str or not space.fullmatch(v)):
                    out.append(f'{table}: identificador fuera del espacio del tenant en {k}')
    return out


def check_run(events, audit, start, complete):
    """RUN de A sobre el estado del almacén: estados y acciones en el orden del oráculo (completos o como prefijo),
    seq contiguo e instantes monótonos y no anteriores al reloj lógico."""
    out = []
    states, actions = [e['state'] for e in events], [a['action'] for a in audit]
    want_s, want_a = (list(PATH), list(ACTIONS)) if complete else \
        (list(PATH[:len(states)]), list(ACTIONS[:len(actions)]))
    if states != want_s or (complete and len(states) != len(PATH)):
        out.append('estados de los eventos distintos del camino del oráculo')
    if actions != want_a or (complete and len(actions) != len(ACTIONS)):
        out.append('acciones de auditoría distintas del oráculo')
    if [e['seq'] for e in events] != list(range(1, len(events) + 1)):
        out.append('seq no contiguo')
    for stamps in ([e['at'] for e in events], [a['at'] for a in audit]):
        if stamps != sorted(stamps) or any(s < start for s in stamps):
            out.append('instantes no monótonos o anteriores al reloj lógico')
    return out


# ---------------------------------------------------------------- conformidad (B0 §5.2) y comprobante (B0 §5.3)
def level1(run, fixture, inputs=None):
    """Nivel 1 (B0 §5.2): proyección semántica A↔B por tenant, emparejada por clave natural (organización, fila F34 de
    origen), sin identificadores, instantes ni cadenas dependientes del run. Recalcula además, desde evidence.csv, la
    selección, T1, hash_before y content_hash. Falla cerrado: lo no evaluable es una diferencia."""
    inputs = inputs or _cached_inputs()
    try:
        return _level1(run, fixture, inputs)
    except (KeyError, TypeError, AttributeError, StopIteration, ValueError):
        return ['run no evaluable contra el oráculo']


def _level1(run, fixture, inputs):
    t, org = run['tables'], run['synthetic_organization_id']
    out = []
    if [(e['state'], e['error_code']) for e in t['pipeline_event']] != \
            [(e['state'], e['error_code']) for e in fixture['events']]:
        out.append('eventos distintos del camino del oráculo')
    if [e['seq'] for e in t['pipeline_event']] != list(range(1, len(t['pipeline_event']) + 1)):
        out.append('seq no contiguo')
    if [a['action'] for a in t['audit_entry']] != [a['action'] for a in fixture['audit']]:
        out.append('acciones de auditoría distintas del oráculo')
    sa = {s['source_id']: s for s in fixture['sources']}
    sb = {s['source_id']: s for s in t['evidence_source']}
    ra = {(r['synthetic_organization_id'], sa[r['source_id']]['origin_record_id']): r for r in fixture['records']}
    rb = {(r['synthetic_organization_id'], sb[r['source_id']]['origin_record_id']): r for r in t['evidence_record']}
    if set(ra) != set(rb) or len(rb) != len(t['evidence_record']):
        return out + ['claves naturales distintas del oráculo']
    pa = {p['record_id']: p for p in fixture['provenance']}
    pb = {p['record_id']: p for p in t['evidence_provenance']}
    va = {v['record_id']: v for v in fixture['reviews']}
    vb = {v['record_id']: v for v in t['simulated_review']}
    for key in sorted(ra):
        a, b = ra[key], rb[key]
        pairs = ((('synthetic_organization_id', 'criterion_ref', 'evidence_kind', 'text_synthetic', 'hash_algorithm',
                   'content_hash', 'validation_status', 'review_status', 'source_type', 'environment'), a, b,
                  'evidencia'),
                 (('origin_dataset_version', 'origin_file', 'origin_file_sha256', 'origin_record_id', 'source_type',
                   'synthetic_organization_id'), sa[a['source_id']], sb[b['source_id']], 'fuente'),
                 (('provenance_kind', 'transformation_id', 'transformation_version', 'hash_before', 'hash_after'),
                  pa[a['synthetic_id']], pb[b['synthetic_id']], 'procedencia'),
                 (('review_scope', 'review_status', 'reviewer_type', 'scripted', 'simulation_actor'),
                  va[a['synthetic_id']], vb[b['synthetic_id']], 'revisión'))
        for names, x, y, what in pairs:
            for f in names:
                if x[f] != y[f] or type(x[f]) is not type(y[f]):
                    out.append(f'{key[1]}: {what} con {f} distinto del oráculo')
        p, s = pb[b['synthetic_id']], sb[b['source_id']]
        if p['source_id'] != b['source_id'] or vb[b['synthetic_id']]['review_id'] != p['review_id']:
            out.append(f'{key[1]}: relación evidencia ↔ fuente ↔ revisión rota')
        # Recalculado desde la fila F34: nunca se acepta un valor precargado.
        row = inputs['evidence'][key[1]]
        args = (org, key[1], row['criterion_id'], row['source_type_ev'])
        if row['organization'] != org or (b['criterion_ref'], b['evidence_kind']) != args[2:] or \
                b['text_synthetic'] != t1(row['evidence_text']) or \
                p['hash_before'] != content_hash(*args, row['evidence_text']) or \
                b['content_hash'] != content_hash(*args, t1(row['evidence_text'])) or \
                p['hash_after'] != b['content_hash'] or \
                s['origin_file_sha256'] != inputs['f34_files_sha256']['evidence.csv']:
            out.append(f'{key[1]}: evidencia distinta de la recalculada desde su fila F34')
    chain_a = [sa[next(r for r in fixture['records'] if r['synthetic_id'] == p['record_id'])['source_id']]
               ['origin_record_id'] for p in fixture['provenance']]
    chain_b = [sb[next(r for r in t['evidence_record'] if r['synthetic_id'] == p['record_id'])['source_id']]
               ['origin_record_id'] for p in t['evidence_provenance']]
    if chain_a != chain_b:
        out.append('orden de la cadena de procedencia distinto del oráculo')
    if chain_b != select_rows(inputs, org):
        out.append('selección distinta de la regla determinista de A sobre F34')
    if {k: len(v) for k, v in t.items()} != COUNTS or run['counts'] != COUNTS:
        out.append('conteos distintos del oráculo')
    return out


def level2(run):
    """Nivel 2 (B0 §5.2): integridad nativa de B. Cadenas de eventos, procedencia y auditoría recalculadas eslabón por
    eslabón, identificadores SBB* del espacio <org>-<semilla> y relaciones entre las filas del run. Falla cerrado."""
    try:
        return _level2(run)
    except (KeyError, TypeError, AttributeError, ValueError):
        return ['run no evaluable en su integridad nativa']


def _level2(run):
    t = run['tables']
    out = chain_problems(t['pipeline_event'], 'event_hash', 'prev_event_hash', 'eventos') + \
        chain_problems(t['evidence_provenance'], 'provenance_hash', 'prev_provenance_hash', 'procedencia') + \
        chain_problems(t['audit_entry'], 'audit_hash', 'prev_audit_hash', 'auditoría')
    org, seed = run['synthetic_organization_id'], run['seed']
    space = f'{org}-{seed:010d}'
    run_id = f'SBBR-{space}'
    if [r['pipeline_run_id'] for r in t['pipeline_run']] != [run_id]:
        out.append('identificador del run distinto del espacio <org>-<semilla>')
    for table, key, prefix in (('pipeline_event', 'event_id', 'SBBV'), ('audit_entry', 'audit_id', 'SBBA'),
                               ('evidence_source', 'source_id', 'SBBS'), ('evidence_record', 'synthetic_id', 'SBBE'),
                               ('evidence_provenance', 'provenance_id', 'SBBP'),
                               ('simulated_review', 'review_id', 'SBBH')):
        if any(not str(r[key]).startswith(f'{prefix}-{space}-') for r in t[table]):
            out.append(f'{table}: identificador fuera de {prefix}-{space}')
    for table, rows in t.items():
        if any(r.get('pipeline_run_id', run_id) != run_id or r.get('synthetic_organization_id', org) != org or
               r.get('target_ref', run_id) != run_id for r in rows):
            out.append(f'{table}: fila de otro run o de otro tenant')
    sources = {s['source_id'] for s in t['evidence_source']}
    records = {r['synthetic_id']: r for r in t['evidence_record']}
    reviews = {v['record_id']: v for v in t['simulated_review']}
    for p in t['evidence_provenance']:
        r = records.get(p['record_id'])
        if r is None or r['source_id'] not in sources or p['source_id'] != r['source_id'] or \
                reviews.get(p['record_id'], {}).get('review_id') != p['review_id']:
            out.append('procedencia sin su evidencia, su fuente o su revisión')
    if len(records) != len(t['evidence_provenance']) or set(reviews) != set(records):
        out.append('evidencias sin una procedencia y una revisión cada una')
    return out


def check_receipt(receipt, run):
    """Paso 12: el comprobante del almacén (diseño de B2, §9) es el de una purga completa de este run."""
    out = []
    if type(receipt) is not dict or set(receipt) != RECEIPT_KEYS:
        return ['comprobante con campos distintos de los del almacén']
    t = run['tables']
    for k, v in (('closure_kind', 'purga'), ('final_state', 'completado'), ('failed_event', 'no_aplica'),
                 ('failed_event_record', 'no_aplica'), ('error_code', ''), ('connection', 'CLOSED'),
                 ('post_close_check', 'ProgrammingError'), ('file_backed', False),
                 ('synthetic_organization_id', run['synthetic_organization_id']),
                 ('pipeline_run_id', t['pipeline_run'][0]['pipeline_run_id']),
                 ('counts', {k2: len(v2) for k2, v2 in t.items()}),
                 ('last_event_hash', t['pipeline_event'][-1]['event_hash'])):
        if receipt.get(k) != v or type(receipt.get(k)) is not type(v):
            out.append(f'comprobante con {k} distinto del de una purga completa')
    if receipt.get('observed') != {'counts': receipt.get('counts'), 'last_event_hash': receipt.get('last_event_hash'),
                                   'final_state': 'completado', 'file_backed': False}:
        out.append('hechos observados del comprobante distintos de los informados')
    if receipt.get('receipt_hash') != sha({k: v for k, v in receipt.items() if k != 'receipt_hash'}):
        out.append('receipt_hash no recalculable')
    return out


# ---------------------------------------------------------------- reloj lógico, inyección de fallo y contexto
def instant(start, k, minutes):
    """Instante lógico del paso k: clock_start + k·minutes minutos, en el mismo día del escenario."""
    if not TS_RX.fullmatch(start):
        raise PipelineError(0, 'E-RELOJ', 'reloj lógico no válido')
    hh, mm, ss = int(start[11:13]), int(start[14:16]), int(start[17:19])
    total = hh * 60 + mm + k * minutes
    if not 0 <= total < 24 * 60:
        raise PipelineError(0, 'E-RELOJ', 'instante lógico fuera del día del escenario')
    return f'{start[:11]}{total // 60:02d}:{total % 60:02d}:{ss:02d}'


def inject(fault, org, k):
    if fault == (org, k):
        raise PipelineError(k, INJECTED, 'fallo inyectado')


class Ctx:
    """Estado de un run: el almacén y lo que cada paso deja para los siguientes."""

    def __init__(self, mod, store, org, inputs, minutes):
        self.mod, self.store, self.org, self.inputs, self.minutes = mod, store, org, inputs, minutes
        self.seed, self.clock_start = SCENARIOS[org]
        self.fixture = self.raw = self.tables = self.receipt = self.post_purge = self.run_id = None
        self.evidence, self.k = [], 0

    def at(self, k):
        return instant(self.clock_start, k, self.minutes)

    def now(self):
        """Instante de la posición en la que corre el paso (§4.4)."""
        return self.at(self.k)


def tenant_context(org):
    return {'synthetic_organization_id': org, 'tenant_kind': 'synthetic_organization',
            'origin_dataset_version': DATASET_VERSION, 'simulation_actor': f'SIMREV-{org}'}


def evidence_for(origin, org, review_status, at_registered, at_reviewed, inputs=None):
    """La evidencia que el paso 5 entrega al almacén, calculada desde su fila F34: T1, hash_before y content_hash."""
    inputs = inputs or _cached_inputs()
    row = inputs['evidence'][origin]
    criterion, kind, text = row['criterion_id'], row['source_type_ev'], row['evidence_text']
    return {'origin_record_id': origin, 'origin_file_sha256': inputs['f34_files_sha256']['evidence.csv'],
            'criterion_ref': criterion, 'evidence_kind': kind, 'text_synthetic': t1(text),
            'hash_before': content_hash(org, origin, criterion, kind, text),
            'content_hash': content_hash(org, origin, criterion, kind, t1(text)), 'validation_status': 'valido',
            'review_status': review_status, 'created_at': at_registered, 'recorded_at': at_registered,
            'reviewed_at': at_reviewed}


_INPUTS = []           # entradas verificadas del run vigente (run las fija); si no hay, se cargan del disco


def _cached_inputs():
    if not _INPUTS:
        _INPUTS.append(load_inputs())
    return _INPUTS[0]


# ---------------------------------------------------------------- los doce pasos
def step1(ctx):
    """Fixture verificado contra el manifest de A (MAN): SHA-256, tamaño, JSON sin claves duplicadas y cabecera."""
    rel = FIXTURES[ctx.org]
    raw = read_input(rel, ctx.inputs['overrides'])
    entry = ctx.inputs['sbx_manifest']['files'][rel[len(SBX_DIR):]]
    if hashlib.sha256(raw).hexdigest() != entry['sha256'] or len(raw) != entry['bytes'] or \
            entry['synthetic_organization_id'] != ctx.org or entry['records'] != PER_TENANT:
        raise PipelineError(1, 'E-FIXTURE', 'el fixture no coincide con el manifest de A')
    try:
        fixture = _json(raw, 'fixture')
    except PipelineError:
        raise PipelineError(1, 'E-FIXTURE', 'fixture no legible como JSON sin claves duplicadas') from None
    head = {k: fixture.get(k) for k in ('fixture_id', 'contract_version', 'synthetic_organization_id', 'source_type',
                                        'environment', 'synthetic_marker')}
    if head != {'fixture_id': f'FXS-{ctx.org}', 'contract_version': CONTRACT_VERSION_A,
                'synthetic_organization_id': ctx.org, 'source_type': 'synthetic', 'environment': 'sandbox',
                'synthetic_marker': MARKER}:
        raise PipelineError(1, 'E-FIXTURE', 'cabecera del fixture distinta de la del tenant')
    ctx.fixture, ctx.raw = fixture, raw
    ctx.mod.append_audit(ctx.store, 'fixture_verificado', ctx.now())


def step2(ctx):
    """Esquema cerrado del contrato publicado de A (SCH, CON), contexto del tenant y escenario del oráculo."""
    contract = ctx.inputs['contract']
    if check_schema(ctx.fixture, contract['$defs'][contract['root']], contract['$defs']):
        raise PipelineError(2, 'E-ESQUEMA', 'el fixture no cumple el contrato cerrado de A')
    if ctx.fixture['tenant'] != tenant_context(ctx.org):
        raise PipelineError(2, 'E-ESQUEMA', 'contexto del tenant distinto del contrato')
    if check_scenario(ctx.org, ctx.fixture):
        raise PipelineError(2, 'E-ESCENARIO', 'escenario distinto del oráculo del tenant')
    ctx.mod.append_event(ctx.store, 'validando', ctx.now(), audit_action='esquema_validado')


def step3(ctx):
    """Synthetic-only: seis marcadores por evidencia y ningún dato personal, media, persona ni capacidad prohibida."""
    if any(check_synthetic(r, ctx.org) for r in ctx.fixture['records']) or check_fixture_content(ctx.fixture):
        raise PipelineError(3, 'E-SINTETICO', 'el fixture no supera las reglas synthetic-only de A')
    ctx.mod.append_audit(ctx.store, 'sintetico_verificado', ctx.now())


def step4(ctx):
    """Hash de contenido: selección determinista desde F34, T1, hash_before y content_hash calculados aquí."""
    fx = ctx.fixture
    sources = {s['source_id']: s for s in fx['sources']}
    declared = [sources.get(r['source_id'], {}).get('origin_record_id') for r in fx['records']]
    selection = select_rows(ctx.inputs, ctx.org)
    if declared != selection:
        raise PipelineError(4, 'E-ORIGEN', 'selección distinta de la regla determinista de A')
    reviews = {v['record_id']: v['review_status'] for v in fx['reviews']}
    ctx.evidence = []
    for record in fx['records']:
        origin = sources[record['source_id']]['origin_record_id']
        ev = evidence_for(origin, ctx.org, reviews.get(record['synthetic_id']), ctx.at(5), ctx.at(8), ctx.inputs)
        if ev['review_status'] not in ('conforme', 'observado'):
            raise PipelineError(4, 'E-HASH', 'evidencia sin revisión declarada')
        ctx.evidence.append(ev)
    ctx.mod.append_audit(ctx.store, 'hash_calculado', ctx.now())


def step5(ctx):
    """Registro: fuente, evidencia, revisión declarada y procedencia de cada evidencia, en una transacción (Q7)."""
    for ev in ctx.evidence:
        ctx.mod.append_evidence(ctx.store, ev)
    ctx.mod.append_event(ctx.store, 'registrado', ctx.now(), audit_action='provenance_registrada')


def step6(ctx):
    """T1 verificada sobre lo persistido: texto = T1(texto F34), hash_before y hash_after recalculados."""
    for bundle in ctx.mod.list_evidence(ctx.store):
        rec, prov, src = bundle['record'], bundle['provenance'], bundle['source']
        row = ctx.inputs['evidence'][src['origin_record_id']]
        args = (ctx.org, src['origin_record_id'], row['criterion_id'], row['source_type_ev'])
        if rec['text_synthetic'] != t1(row['evidence_text']) or \
                prov['hash_before'] != content_hash(*args, row['evidence_text']) or \
                prov['hash_after'] != rec['content_hash'] or \
                rec['content_hash'] != content_hash(*args, t1(row['evidence_text'])) or \
                (prov['transformation_id'], prov['transformation_version']) != ('T1-normalizacion-nfc-espacios', '1'):
            raise PipelineError(6, 'E-TRANSFORMA', 'transformación T1 no verificable sobre lo persistido')
    ctx.mod.append_event(ctx.store, 'transformado', ctx.now())


def step7(ctx):
    """Tenant: toda fila y todo identificador del tenant, en el almacén y en el oráculo (ISO de A); filas F34 y
    criterios de su organización."""
    bundles = ctx.mod.list_evidence(ctx.store)
    problems = check_tenant_rows(ctx.org, json.loads(ctx.mod.snapshot(ctx.store).decode('utf-8'))) + \
        check_fixture_tenant(ctx.org, ctx.fixture, ctx.inputs)
    for b in bundles:
        row = ctx.inputs['evidence'][b['source']['origin_record_id']]
        if row['organization'] != ctx.org or ctx.inputs['criteria_org'].get(b['record']['criterion_ref']) != ctx.org:
            problems.append('fila F34 o criterio de otra organización')
    if problems:
        raise PipelineError(7, 'E-TENANT', 'aislamiento por tenant no verificable')
    ctx.mod.append_audit(ctx.store, 'tenant_validado', ctx.now())


def step8(ctx):
    """Revisión humana simulada: solo integridad y procedencia, declarada en el fixture (REV de A)."""
    ctx.mod.append_event(ctx.store, 'en_revision', ctx.now())
    bundles = ctx.mod.list_evidence(ctx.store)
    declared = {v['record_id']: v for v in ctx.fixture['reviews']}
    by_origin = {s['origin_record_id']: r['synthetic_id'] for s, r in
                 ((({x['source_id']: x for x in ctx.fixture['sources']})[r['source_id']], r)
                  for r in ctx.fixture['records'])}
    for b in bundles:
        v, rec = b['review'], b['record']
        want = declared.get(by_origin.get(b['source']['origin_record_id']), {})
        if v['review_scope'] != 'integridad_y_procedencia' or v['reviewer_type'] != 'synthetic_human_simulation' or \
                v['simulation_actor'] != f'SIMREV-{ctx.org}' or v['scripted'] is not True or \
                v['review_status'] not in ('conforme', 'observado') or v['review_status'] != rec['review_status'] or \
                v['review_status'] != want.get('review_status') or v['record_id'] != rec['synthetic_id']:
            raise PipelineError(8, 'E-REVISION', 'revisión simulada fuera de integridad y procedencia')
    if len(bundles) != PER_TENANT:
        raise PipelineError(8, 'E-REVISION', 'una revisión por evidencia')
    ctx.mod.append_event(ctx.store, 'revisado', ctx.now(), audit_action='revision_simulada_registrada')


def step9(ctx):
    """Resultado experimental: cada evidencia íntegra y procedente (valido); nunca nada sobre la persona."""
    if [b['record']['validation_status'] for b in ctx.mod.list_evidence(ctx.store)] != ['valido'] * PER_TENANT:
        raise PipelineError(9, 'E-RESULTADO', 'resultado experimental distinto de valido')


def step10(ctx):
    """Auditoría encadenada: cadena recalculada y RUN de A como prefijo del camino del oráculo."""
    audit, events = list(ctx.mod.list_audit(ctx.store)), list(ctx.mod.list_events(ctx.store))
    if chain_problems(audit, 'audit_hash', 'prev_audit_hash', 'auditoría') or \
            check_run(events, audit, ctx.clock_start, False):
        raise PipelineError(10, 'E-AUDITORIA', 'auditoría encadenada no verificable')


def step11(ctx):
    """Cierre e inmutabilidad: evento completado con su auditoría, instantánea de las ocho tablas y conformidad."""
    ctx.mod.append_event(ctx.store, 'completado', ctx.now(), audit_action='ejecucion_cerrada')
    ctx.tables = json.loads(ctx.mod.snapshot(ctx.store).decode('utf-8'))
    ctx.run_id = ctx.tables['pipeline_run'][0]['pipeline_run_id']
    if check_run(ctx.tables['pipeline_event'], ctx.tables['audit_entry'], ctx.clock_start, True):
        raise PipelineError(11, 'E-CIERRE', 'run cerrado fuera del camino del oráculo')
    partial = {'synthetic_organization_id': ctx.org, 'seed': ctx.seed, 'tables': ctx.tables,
               'counts': {k: len(v) for k, v in ctx.tables.items()}}
    if level1(partial, ctx.fixture) or level2(partial):
        raise PipelineError(11, 'E-CONFORMIDAD', 'run no conforme con el oráculo de A')


def step12(ctx):
    """Purga: conexión cerrada y comprobante; una llamada posterior debe fallar con E-PURGADO."""
    ctx.receipt = ctx.mod.purge(ctx.store)
    try:
        ctx.mod.list_events(ctx.store)
        ctx.post_purge = 'utilizable'
    except ctx.mod.SbxbStoreError as e:
        ctx.post_purge = e.code


STEP_FUNCTIONS = {1: step1, 2: step2, 3: step3, 4: step4, 5: step5, 6: step6, 7: step7, 8: step8, 9: step9,
                  10: step10, 11: step11, 12: step12}


# ---------------------------------------------------------------- ejecución con fallo cerrado
def _close(mod, store, ctx, step, code):
    """Cierre tras un fallo: fallido con su código si el run sigue activo y purga; si el almacén quedó bloqueado, su
    diagnóstico. Lo que no se pueda establecer queda no_disponible."""
    if store is None:
        return 'no_disponible'
    try:
        mod.append_event(store, 'fallido', ctx.at(max(step, 1)) if ctx else '', error_code=code)
    except Exception as e:                  # terminado, bloqueado o purgado: lo decide el estado del almacén
        if getattr(e, 'code', None) == 'E-BLOQUEADO':
            return _safe(lambda: mod.diagnostic(store))
        if getattr(e, 'code', None) == 'E-PURGADO':
            return ctx.receipt if ctx and ctx.receipt is not None else 'no_disponible'
    try:
        return mod.purge(store)
    except Exception as e:
        if getattr(e, 'code', None) in ('E-BLOQUEADO', 'E-SQLITE'):
            return _safe(lambda: mod.diagnostic(store))
        return 'no_disponible'


def _safe(fn):
    try:
        return fn()
    except Exception:
        return 'no_disponible'


def run_tenant(mod, inputs, org, fault, minutes, observe=None):
    """Los doce pasos de un tenant. Devuelve su run; cualquier error lo deja fallido sin resultado parcial."""
    store = ctx = None
    step = 0
    try:
        store = mod.open_tenant_store(tenant_context(org))
        ctx = Ctx(mod, store, org, inputs, minutes)
        mod.create_run(store, ctx.seed, ctx.clock_start)
        steps = []
        for step in range(1, 13):
            ctx.k = step
            inject(fault, org, step)
            STEP_FUNCTIONS[step](ctx)
            steps.append({'step': step, 'name': STEP_NAMES[step], 'result': 'ok', 'at': ctx.at(step)})
        if observe is not None:
            observe(mod, store)
        run = {'synthetic_organization_id': org, 'seed': ctx.seed, 'clock_start': ctx.clock_start,
               'final_state': 'completado', 'steps': steps, 'tables': ctx.tables,
               'counts': {k: len(v) for k, v in ctx.tables.items()},
               'conformity': {'level1': 'conforme', 'level2': 'integra'}, 'receipt': ctx.receipt,
               'post_purge': ctx.post_purge}
        if check_receipt(ctx.receipt, run) or ctx.post_purge != 'E-PURGADO':
            raise PipelineError(12, 'E-PURGA', 'purga no verificada')
        return run
    except PipelineError as e:
        code, message, failed_step = e.code, e.message, e.step if e.step else step
    except Exception as e:                  # error del almacén u otro: el código del almacén si lo tiene
        code = getattr(e, 'code', None)
        code = code if isinstance(code, str) and CODE_RX.fullmatch(code) else 'E-INTERNO'
        message, failed_step = 'error del almacén o del pipeline', step
    closure = _close(mod, store, ctx, failed_step, code)
    raise PipelineFailure(org, failed_step, code, message, closure)


def base_report(inputs, mod):
    return {'report_version': REPORT_VERSION,
            'pipeline_version': getattr(mod, 'PIPELINE_VERSION', 'no_disponible') if mod else 'no_disponible',
            'contract_version': getattr(mod, 'CONTRACT_VERSION', 'no_disponible') if mod else 'no_disponible',
            'run_kind': getattr(mod, 'RUN_KIND', 'no_disponible') if mod else 'no_disponible',
            'environment': 'sandbox', 'source_type': 'synthetic',
            'inputs': {} if inputs is None else {
                'dataset_version': DATASET_VERSION, 'f34_manifest_sha256': inputs['f34_manifest_sha256'],
                'f34_files_sha256': inputs['f34_files_sha256'], 'sbx_manifest_sha256': inputs['sbx_manifest_sha256'],
                'sbx_contract_sha256': inputs['sbx_contract_sha256'], 'store_sha256': STORE_SHA256,
                'fixtures_sha256': {o: inputs['sbx_manifest']['files'][FIXTURES[o][len(SBX_DIR):]]['sha256']
                                    for o in TENANTS}}}


def run(fault=None, overrides=None, minutes=1, observe=None):
    """Ejecución completa: (informe, código de salida). Sin escritura de archivos."""
    inputs = mod = None
    try:
        inputs = load_inputs(overrides)
        _INPUTS[:] = [inputs]
        mod = load_store()
        runs = [run_tenant(mod, inputs, org, fault, minutes, observe) for org in TENANTS]
        report = dict(base_report(inputs, mod), result='completado', runs=runs)
        if check_report(report):
            raise PipelineError(13, 'E-INFORME', 'informe fuera de su esquema cerrado')
        return report, 0
    except PipelineFailure as f:
        failure = {'synthetic_organization_id': f.org, 'step': f.step, 'step_name': STEP_NAMES.get(f.step,
                   EXTRA_STEPS.get(f.step, 'no_disponible')), 'error_code': f.code, 'message': f.message,
                   'closure': f.closure}
    except PipelineError as e:
        failure = {'synthetic_organization_id': 'ninguna', 'step': e.step, 'step_name': STEP_NAMES.get(
            e.step, EXTRA_STEPS.get(e.step, 'no_disponible')), 'error_code': e.code, 'message': e.message,
            'closure': 'no_disponible'}
    return dict(base_report(inputs, mod), result='fallido', failure=failure), 1


# ---------------------------------------------------------------- informe canónico (TSBB-10)
def check_report(report):
    """Esquema cerrado del informe: claves y tipos exactos; ningún campo ajeno, como un puntaje o un orden."""
    out = []
    top = {'report_version', 'result', 'pipeline_version', 'contract_version', 'run_kind', 'environment',
           'source_type', 'inputs'}
    if type(report) is not dict:
        return ['informe ilegible']
    result = report.get('result')
    want = top | ({'runs'} if result == 'completado' else {'failure'} if result == 'fallido' else set())
    if set(report) != want:
        out.append(f'claves del informe distintas del esquema: {sorted(set(report) ^ want)}')
    if report.get('report_version') != REPORT_VERSION or report.get('environment') != 'sandbox' or \
            report.get('source_type') != 'synthetic':
        out.append('cabecera del informe distinta del esquema')
    if result == 'completado':
        runs = report.get('runs')
        if type(runs) is not list or [r.get('synthetic_organization_id') for r in runs] != list(TENANTS):
            return out + ['runs distintos de los tres tenants en orden']
        run_keys = {'synthetic_organization_id', 'seed', 'clock_start', 'final_state', 'steps', 'tables', 'counts',
                    'conformity', 'receipt', 'post_purge'}
        for r in runs:
            if set(r) != run_keys:
                out.append(f'claves del run distintas del esquema: {sorted(set(r) ^ run_keys)}')
                continue
            if r['final_state'] != 'completado' or r['post_purge'] != 'E-PURGADO' or \
                    r['conformity'] != {'level1': 'conforme', 'level2': 'integra'}:
                out.append('run no completado, sin purga verificada o no conforme')
            if [(s.get('step'), s.get('name'), s.get('result')) for s in r['steps']] != \
                    [(k, STEP_NAMES[k], 'ok') for k in range(1, 13)] or any(set(s) != {'step', 'name', 'result', 'at'}
                                                                         for s in r['steps']):
                out.append('pasos distintos de los doce del contrato')
            if type(r['tables']) is not dict or set(r['tables']) != set(TABLES) or set(r['counts']) != set(TABLES):
                out.append('tablas o conteos distintos de las ocho del almacén')
            if type(r['receipt']) is not dict or set(r['receipt']) != RECEIPT_KEYS:
                out.append('comprobante con campos distintos de los del almacén')
    elif result == 'fallido':
        f = report.get('failure')
        if type(f) is not dict or set(f) != {'synthetic_organization_id', 'step', 'step_name', 'error_code',
                                              'message', 'closure'} or not CODE_RX.fullmatch(str(f.get('error_code'))):
            out.append('falla con campos distintos del esquema')
    else:
        out.append('resultado distinto de completado o fallido')
    for path, k, v in walk(report):
        if tokens(k) & CAP_TOKENS:
            out.append(f'{path}: campo de capacidad prohibida')
    return out


def report_bytes(report):
    return canon(report) + b'\n'


def same_report(a, b):
    return a == b


def main(argv):
    fault = None
    if argv:
        m = re.fullmatch(r'(ORG-S[1-3]):([0-9]{1,2})', argv[1]) if len(argv) == 2 and argv[0] == '--fallo' else None
        if m is None or not 1 <= int(m.group(2)) <= 12:
            sys.stderr.write('uso: sbxb_pipeline.py [--fallo ORG-SX:N], con N de 1 a 12\n')
            return 2
        fault = (m.group(1), int(m.group(2)))
    report, code = run(fault=fault)
    sys.stdout.buffer.write(report_bytes(report))
    sys.stdout.buffer.flush()
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
