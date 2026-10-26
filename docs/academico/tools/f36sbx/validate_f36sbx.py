#!/usr/bin/env python3
"""Validador fail-closed del paquete F36-SBX (autorización, investigación y diseño).

Solo biblioteca estándar. No ejecuta ML ni NLP, no usa red y no escribe archivos.
Recalcula el resultado del F36-SBX-GATE y exige que coincida con el declarado.

Uso: python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py
"""
import ast
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
MATRIX = PKG + '/F36SBX_Matriz_Capacidades.md'
THREATS = PKG + '/F36SBX_Threat_Model.md'
PLAN = PKG + '/F36SBX_Plan_Evaluacion.md'
GATE_DOC = PKG + '/F36SBX_Gate_Sucesor.md'
CONTRACT = PKG + '/contrato/f36sbx_evidence_contract.json'
GATE_STATE = PKG + '/gate/f36sbx_gate_state.json'
F33_MATRIX = 'docs/academico/diseno-inteligente/F33_Matriz_Capacidades_y_Restricciones.md'
PKG_DOCS = ['README.md', 'F36SBX_Charter.md', 'F36SBX_Matriz_Capacidades.md', 'F36SBX_Investigacion_Diseno.md',
            'F36SBX_Contrato_Evidencia.md', 'F36SBX_Threat_Model.md', 'F36SBX_Plan_Evaluacion.md',
            'F36SBX_Gate_Sucesor.md', 'F36SBX_Trazabilidad.md']
PKG_FILES = [f'{PKG}/{n}' for n in PKG_DOCS] + [CONTRACT, GATE_STATE]
GOV_FILES = ['CLAUDE.md', 'README.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md']

# Estado vigente que deben declarar los cuatro documentos de gobierno, una sola vez cada uno.
REQUIRED_STATE = ['G0 real = NO APROBADA', 'G0-09 = CUMPLIDO', 'G0-14 = CUMPLIDO', 'G0-02 = PENDIENTE EXTERNO',
                  'G0-03 = PENDIENTE EXTERNO', 'G0-12 = PENDIENTE EXTERNO', 'ADR-005 = PROPUESTA',
                  'G0-SBX = APROBADA CON RESTRICCIONES', 'F35 productiva = BLOQUEADA',
                  'F35-SBX = CERRADA Y CONGELADA', 'F36-SBX = EN DISEÑO', 'F36-SBX-GATE = NO SUPERADO',
                  'F37-SBX = BLOQUEADA', 'F36–F40 = BLOQUEADAS', 'Alcance C = BLOQUEADO', 'Datos reales = PROHIBIDOS']

# Afirmaciones de estado que nunca pueden aparecer en el paquete ni en el gobierno.
FORBIDDEN_CLAIMS = [
    (r'\bG0 real\s*=\s*APROBADA', 'G0 real aprobada'),
    (r'\bG0\s*=\s*APROBADA', 'G0 aprobada sin sufijo'),
    (r'ADR-005(?: canónico)?\s*=\s*APROBAD', 'ADR-005 aprobado'),
    (r'F37-SBX\s*[:=]\s*+(?!BLOQUEADA)', 'F37-SBX en un estado distinto de BLOQUEADA'),
    (r'F36-SBX\s*[:=]\s*+(?!EN DISEÑO)', 'F36-SBX en un estado distinto de EN DISEÑO'),
    (r'F36-SBX-GATE\s*[:=]\s*+(?!NO SUPERADO)', 'F36-SBX-GATE en un estado distinto de NO SUPERADO'),
    (r'(?i)alcance C\s*=\s*+(?!BLOQUEADO)', 'alcance C no bloqueado'),
    (r'(?i)datos reales\s*=\s*+(?!PROHIBIDOS)', 'datos reales no prohibidos'),
    (r'(?i)F37-SBX (?:queda|está|esta) (?:habilitada|autorizada|iniciada)', 'F37-SBX habilitada'),
    (r'(?i)RF-23\s*(?:=|es)\s*autom', 'RF-23 automática'),
]

EI_IDS = [f'EI-{i:02d}' for i in range(1, 25)]
CLASSES = ('ALLOWED', 'CONDITIONAL', 'BLOCKED')
# Temas que deben quedar en una fila BLOCKED de la matriz (columna de capacidad).
MUST_BLOCK = ['resumen', 'veredicto', 'ocr', 'llm sobre evidencia', 'llm para generar', 'entre candidatos',
              'scoring', 'ranking', 'recomendación', 'selección automática', 'emociones', 'personalidad',
              'honestidad', 'inteligencia', 'estrés', 'nerviosismo', 'biometría', 'rostro', 'voz', 'prosodia',
              'acento', 'audio', 'ajuste fino', 'datos reales', 'endpoints', 'migraciones']
# Palabras que una capacidad ALLOWED no puede nombrar: son del alcance C o están bloqueadas.
NOT_ALLOWED_WORDS = [r'embedding', r'semántic', r'ocr', r'llm', r'pdf', r'docx', r'ner',
                     r'extracci']

TEI_IDS = [f'TEI-{i:02d}' for i in range(1, 23)]
THREAT_TOPICS = ['injection', 'malicioso', 'envenenamiento', 'fuga criterio', 'organizaciones', 'pii',
                 'alucinación', 'sin respaldo', 'automatización', 'ranking encubierto', 'inferencias prohibidas',
                 'procedencia', 'deriva de modelo', 'reproducibilidad', 'dependencia externa',
                 'cadena de suministro', 'agotamiento', 'adversarial', 'abstención', 'contaminación']
M_IDS = [f'M-{i:02d}' for i in range(1, 14)]
R_IDS = [f'R-{i:02d}' for i in range(1, 6)]

CONTRACT_KEYS = {'contract_id', 'contract_version', 'status', 'environment', 'source_type_allowed',
                 'generator_policy', 'allowed_upstream_sources', 'forbidden_upstream_sources', 'synthetic_markers',
                 'provenance_required', 'artifact_types', 'closed_values', 'group_marker_only_in',
                 'forbidden_fields', 'splits'}
ALLOWED_UPSTREAM = {'docs/academico/datos-sinteticos/dataset', 'docs/academico/evidencia-sbx/fixtures'}
REQUIRED_FORBIDDEN_FIELDS = {'name', 'dni', 'email', 'phone', 'address', 'photo', 'age', 'gender', 'score', 'rank',
                             'recommendation', 'suitability', 'suggested_level', 'emotion', 'personality',
                             'honesty', 'intelligence', 'stress', 'nervousness', 'voice', 'face', 'prosody',
                             'accent', 'audio', 'video', 'biometric'}
MARKERS = {'synthetic_id_prefix': 'SBX36-', 'text_prefix': '[SINTÉTICO]', 'source_type': 'synthetic',
           'environment': 'sandbox', 'hash_algorithm': 'f36sbx-content-sha256-v1',
           'synthetic_organization_ids': ['ORG-S1', 'ORG-S2', 'ORG-S3']}

FG_IDS = [f'FG-{i:02d}' for i in range(1, 15)]
FG_TEAM = frozenset({'FG-02', 'FG-03', 'FG-10', 'FG-12'})
FG_NA_ALLOWED = frozenset({'FG-10', 'FG-12'})
STATUSES = frozenset({'CUMPLE', 'PENDIENTE', 'NO CUMPLE', 'NO APLICA'})
RESULTS = ('NO SUPERADO', 'SUPERADO', 'REVOCADO')
GATE_KEYS = {'gate_id', 'gate_version', 'authorizes', 'cannot_authorize', 'base_commit', 'criteria',
             'f37_authorized_ei', 'revocation', 'declared_result'}
CANNOT_AUTHORIZE = {'produccion', 'datos_reales', 'pii_real', 'audio_video_real', 'seleccion_automatica',
                    'scoring_ranking_recomendacion', 'cambio_rf23_rf21_rf29', 'g0_real', 'alcance_c_producto',
                    'endpoints_migraciones_ui', 'ei_blocked'}

STDLIB = frozenset({'ast', 'copy', 'json', 'os', 're', 'subprocess', 'sys', 'unicodedata', 'pathlib', 'unittest',
                    'tempfile'})
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
    except (ValueError, TypeError):
        return None


def git(root, *args):
    r = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, encoding='utf-8')
    return r.returncode, r.stdout


def read(root, rel):
    try:
        return (Path(root) / rel).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None


def collect(root=ROOT):
    """Fotografía de todo lo que evalúan las reglas. Las pruebas la mutan en memoria."""
    texts = {rel: read(root, rel) for rel in PKG_FILES + GOV_FILES + [F33_MATRIX]}
    tools = {}
    tdir = Path(root) / TOOLS
    if tdir.is_dir():
        for p in sorted(tdir.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                tools[p.relative_to(root).as_posix()] = read(root, p.relative_to(root).as_posix())
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
    changed_py = {}
    for rel in sorted(changed or ()):
        if rel.endswith('.py'):
            changed_py[rel] = read(root, rel)
    return {'root': str(root), 'texts': texts, 'tools': tools, 'branch': branch, 'base_ok': base_ok,
            'changed': changed, 'base_gov': base_gov, 'changed_py': changed_py}


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
            cells = [c.strip() for c in ln.strip().strip('|').split(' | ')]
            rows.append(cells)
    return rows


# ---------------------------------------------------------------- reglas

def rule_str(s):
    out = []
    missing = [p for p in PKG_FILES if s['texts'].get(p) is None]
    out.append((not missing, f'paquete completo ({len(PKG_FILES)} archivos); faltan: {missing}'))
    readme = s['texts'].get(f'{PKG}/README.md') or ''
    unlinked = [n for n in PKG_DOCS[1:] if f']({n})' not in readme]
    unlinked += [p for p in (CONTRACT, GATE_STATE) if f']({p[len(PKG) + 1:]})' not in readme]
    out.append((not unlinked, f'el README enlaza todos los artefactos; sin enlace: {unlinked}'))
    return out


def rule_lnk(s):
    root = Path(s['root'])
    broken = []
    texts_by_path = {str((root / k).resolve()): v for k, v in s['texts'].items() if v is not None}
    sources = [p for p in PKG_FILES if p.endswith('.md')] + GOV_FILES
    for rel in sources:
        text = s['texts'].get(rel)
        if text is None:
            continue
        if rel in GOV_FILES:
            # En gobierno solo se verifican los enlaces nuevos, hacia el paquete F36-SBX.
            links = [l for l in re.findall(r'\]\(([^)\s]+)\)', text) if 'f36-sbx' in l]
        else:
            links = re.findall(r'\]\(([^)\s]+)\)', text)
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
    required = [norm(r) for r in REQUIRED_STATE]
    for rel in GOV_FILES:
        block = state_block(s['texts'].get(rel))
        if block is None:
            out.append((False, f'{rel}: sin bloque «Estado vigente» (falla cerrado)'))
            continue
        bl = [norm(b) for b in bullets(block)]
        missing = [r for r in required if bl.count(r) != 1]
        out.append((not missing, f'{rel}: estado vigente completo y sin duplicados; ausentes o repetidos: {missing}'))
        keys = [b.split(' = ', 1)[0] for b in bl if ' = ' in b]
        dup = sorted({k for k in keys if keys.count(k) > 1})
        out.append((not dup, f'{rel}: ninguna clave de estado declarada dos veces; repetidas: {dup}'))
        base_block = state_block(s['base_gov'].get(rel))
        if base_block is None:
            out.append((False, f'{rel}: no se pudo leer el estado vigente de la base {BASE[:7]} (falla cerrado)'))
        else:
            lost = [b for b in (norm(x) for x in bullets(base_block)) if b not in bl]
            out.append((not lost, f'{rel}: conserva todos los estados de la base; perdidos: {lost}'))
    return out


def rule_sem(s):
    hits = []
    scope = {p: s['texts'].get(p) for p in PKG_FILES + GOV_FILES}
    for rel, text in scope.items():
        if text is None:
            continue
        # Sin marcado Markdown: «**F37-SBX** = …» no esquiva la regla.
        t = re.sub(r'[*`_]', '', norm(text))
        for pattern, label in FORBIDDEN_CLAIMS:
            for m in re.finditer(norm(pattern), t):
                hits.append(f'{rel}: {label} «{t[m.start():m.start() + 40].strip()}»')
    return [(not hits, f'sin afirmaciones de estado prohibidas; encontradas: {hits}')]


def f33_classes(text):
    out = {}
    for cells in table_rows(text, 'CAP-'):
        if len(cells) < 3:
            continue
        cls = cells[2].replace('*', '').strip()
        if cls.startswith('BLOQUEADA'):
            out[cells[0]] = 'BLOQUEADA'
        elif cls.startswith('FUTURA'):
            out[cells[0]] = 'FUTURA'
        elif cls.startswith('PERMITIDA CON RESTRICCIONES'):
            out[cells[0]] = 'PERMITIDA CON RESTRICCIONES'
        elif cls.startswith('PERMITIDA'):
            out[cells[0]] = 'PERMITIDA'
    return out


def matrix_rows(text):
    rows = {}
    dup = []
    for cells in table_rows(text, 'EI-'):
        if len(cells) != 7:
            dup.append(f'{cells[0]}: {len(cells)} columnas')
            continue
        ei, cap_text, cls, scope, caps, cond, stage = cells
        cls = cls.replace('*', '').strip()
        if ei in rows:
            dup.append(ei)
        rows[ei] = {'capacity': cap_text, 'class': cls, 'scope': scope, 'caps': re.findall(r'CAP-\d\d', caps),
                    'cond': cond, 'stage': stage}
    return rows, dup


def matrix_classes(s):
    rows, _ = matrix_rows(s['texts'].get(MATRIX))
    return {k: v['class'] for k, v in rows.items()}


def rule_cap(s):
    out = []
    f33 = f33_classes(s['texts'].get(F33_MATRIX))
    out.append((len(f33) == 37, f'matriz F33 legible: {len(f33)} de 37 CAP'))
    rows, bad = matrix_rows(s['texts'].get(MATRIX))
    out.append((not bad, f'filas EI bien formadas y sin duplicados; problemas: {bad}'))
    out.append((sorted(rows) == EI_IDS, f'EI-01..EI-24 presentes exactamente; hay {sorted(rows)}'))
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
            bad_words = [w for w in NOT_ALLOWED_WORDS if re.search(w, low)]
            if bad_words:
                errs.append(f'{ei}: capacidad ALLOWED que nombra {bad_words}')
        if r['scope'] == 'C' and r['class'] == 'ALLOWED':
            errs.append(f'{ei}: alcance C ALLOWED')
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


def rule_ctr(s):
    c = strict_json(s['texts'].get(CONTRACT) or '')
    if not isinstance(c, dict):
        return [(False, 'contrato de evidencia: JSON inválido o con claves duplicadas (falla cerrado)')]
    errs = []
    if set(c) != CONTRACT_KEYS:
        errs.append(f'claves de primer nivel distintas del esquema cerrado: {sorted(set(c) ^ CONTRACT_KEYS)}')
    if c.get('source_type_allowed') != ['synthetic']:
        errs.append('source_type_allowed debe ser exactamente ["synthetic"]')
    if c.get('environment') != 'sandbox':
        errs.append('environment debe ser sandbox')
    gp = c.get('generator_policy')
    if gp != {'llm_allowed': False, 'template_based': True, 'seed_required': True, 'byte_reproducible': True}:
        errs.append(f'generator_policy no admitida: {gp}')
    up = c.get('allowed_upstream_sources')
    if not isinstance(up, list) or not up or not set(up) <= ALLOWED_UPSTREAM:
        errs.append(f'fuentes admitidas fuera de la lista cerrada: {up}')
    elif not all((Path(s['root']) / u).is_dir() for u in up):
        errs.append('una fuente admitida no existe')
    fup = c.get('forbidden_upstream_sources')
    if not isinstance(fup, list) or 'docs/academico/g0-evidence' not in fup:
        errs.append('los adjuntos de gobierno deben figurar como fuente prohibida')
    if c.get('synthetic_markers') != MARKERS:
        errs.append('marcadores synthetic-only distintos de los exigidos')
    prov = c.get('provenance_required')
    if not isinstance(prov, dict) or set(prov) != {'artifact', 'fragment', 'output'} or \
            not all(isinstance(v, list) and v for v in prov.values()):
        errs.append('provenance_required incompleta')
    forb = c.get('forbidden_fields')
    if not isinstance(forb, list) or not REQUIRED_FORBIDDEN_FIELDS <= set(forb):
        missing = sorted(REQUIRED_FORBIDDEN_FIELDS - set(forb or []))
        errs.append(f'faltan campos prohibidos obligatorios: {missing}')
        forb = forb if isinstance(forb, list) else []
    types = c.get('artifact_types')
    group_types = c.get('group_marker_only_in')
    if not isinstance(types, dict) or not types:
        errs.append('artifact_types vacío o inválido')
        types = {}
    for name, spec in types.items():
        fields = spec.get('fields') if isinstance(spec, dict) else None
        if not isinstance(fields, list):
            errs.append(f'{name}: sin lista de campos')
            continue
        bad = sorted(set(fields) & set(forb))
        if bad:
            errs.append(f'{name}: declara campos prohibidos {bad}')
        for req in ('synthetic_id', 'synthetic_organization_id', 'source_type', 'environment'):
            if req not in fields:
                errs.append(f'{name}: falta {req}')
        if name != 'relevance_annotation' and 'content_hash' not in fields:
            errs.append(f'{name}: falta content_hash')
        if 'grupo_sintetico' in fields and name not in (group_types or []):
            errs.append(f'{name}: grupo_sintetico fuera de los tipos contrafactuales')
        if spec.get('stage') not in ('A', 'B'):
            errs.append(f'{name}: etapa desconocida')
    if group_types != ['counterfactual_pair']:
        errs.append('group_marker_only_in debe ser exactamente ["counterfactual_pair"]')
    cv = c.get('closed_values')
    if not isinstance(cv, dict) or cv.get('author_kind') != ['human_synthetic']:
        errs.append('author_kind debe ser exactamente ["human_synthetic"]')
    sp = c.get('splits')
    if not isinstance(sp, dict) or sp.get('partitions') != ['dev', 'test'] or sp.get('train_allowed') is not False \
            or sp.get('test_sealed_before_any_run') is not True or sp.get('thresholds_fit_on') != 'dev' \
            or sp.get('counterfactual_pairs_same_partition') is not True:
        errs.append(f'reglas de partición no admitidas: {sp}')
    return [(not errs, f'contrato de evidencia cerrado y solo sintético; errores: {errs}')]


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
    classes = matrix_classes(s)
    needed = sorted(k for k, v in classes.items() if v in ('ALLOWED', 'CONDITIONAL'))
    uncovered = [e for e in needed if e not in covered]
    out.append((bool(needed) and not uncovered, f'cada EI ALLOWED o CONDITIONAL tiene métrica; sin métrica: {uncovered}'))
    blocked_measured = sorted(e for e in covered if classes.get(e) == 'BLOCKED')
    out.append((not blocked_measured, f'ninguna EI BLOCKED tiene métrica; con métrica: {blocked_measured}'))
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
            for n in names:
                if n not in STDLIB and n not in LOCAL_MODULES:
                    errs.append(f'{rel}: importa {n}')
    for rel, src in sorted(s['changed_py'].items()):
        for m in ML_IMPORT.finditer(src or ''):
            errs.append(f'{rel}: importa {m.group(1)} (ML, NLP o red)')
    return [(not errs, f'solo biblioteca estándar y ningún import de ML, NLP o red; encontrados: {sorted(set(errs))}')]


def rule_pii(s):
    hits = []
    scope = {p: s['texts'].get(p) for p in PKG_FILES}
    scope.update({p: t for p, t in s['tools'].items() if p.endswith('.py')})
    for rel, text in scope.items():
        for pattern, label in PII_PATTERNS:
            if text and pattern.search(text):
                hits.append(f'{rel}: {label}')
    return [(not hits, f'sin patrones de PII en el paquete ni en sus herramientas; encontrados: {hits}')]


# ---------------------------------------------------------------- gate

def evidence_ok(root, path):
    if not isinstance(path, str) or not path.startswith(GATE_EVIDENCE) or '..' in Path(path).parts:
        return False
    p = (Path(root) / path)
    try:
        return p.resolve().is_relative_to((Path(root) / GATE_EVIDENCE).resolve()) and p.is_file() \
            and p.stat().st_size > 0
    except OSError:
        return False


def evaluate_gate(state, classes, exists):
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
    if any(v not in STATUSES for v in st.values()):
        return no
    for c in crit:
        if c['id'] in FG_TEAM and c.get('status') == 'CUMPLE' and not exists(c.get('evidence')):
            return no
    auth = state.get('f37_authorized_ei')
    if auth is not None:
        if not isinstance(auth, list) or not auth or len(set(auth)) != len(auth):
            return no
        if any(classes.get(ei) not in ('ALLOWED', 'CONDITIONAL') for ei in auth):
            return no
    conditional = auth is not None and any(classes.get(ei) == 'CONDITIONAL' for ei in auth)
    for fg, v in st.items():
        if v == 'NO APLICA':
            if fg not in FG_NA_ALLOWED or st['FG-03'] != 'CUMPLE' or auth is None or conditional:
                return no
        elif v != 'CUMPLE':
            return no
    if auth is None:
        return no
    return 'SUPERADO'


def rule_gate(s, auto):
    out = []
    state = strict_json(s['texts'].get(GATE_STATE) or '')
    if not isinstance(state, dict):
        return [(False, 'estado del gate: JSON inválido o con claves duplicadas (falla cerrado)')], None
    out.append((set(state) == GATE_KEYS, f'estado del gate con esquema cerrado; diferencias: '
                                         f'{sorted(set(state) ^ GATE_KEYS)}'))
    out.append((state.get('gate_id') == 'F36-SBX-GATE' and state.get('base_commit') == BASE,
                'identidad del gate y base declaradas'))
    out.append((state.get('authorizes') == ['F37-SBX'], f'el gate solo autoriza F37-SBX: {state.get("authorizes")}'))
    ca = state.get('cannot_authorize')
    out.append((isinstance(ca, list) and set(ca) == CANNOT_AUTHORIZE and len(ca) == len(CANNOT_AUTHORIZE),
                'lista cerrada de lo que el gate no puede autorizar'))
    crit = state.get('criteria') if isinstance(state.get('criteria'), list) else []
    kinds = {c.get('id'): c.get('kind') for c in crit if isinstance(c, dict)}
    expected_kinds = {fg: ('team' if fg in FG_TEAM else 'auto') for fg in FG_IDS}
    out.append((kinds == expected_kinds, 'tipos de criterio fijos (AUTO o EQUIPO)'))
    computed_auto = {
        'FG-01': all(auto.values()), 'FG-04': auto['GOV'], 'FG-05': auto['FRZ'], 'FG-06': auto['CAP'],
        'FG-07': auto['CTR'], 'FG-08': auto['THR'], 'FG-09': auto['EVA'], 'FG-11': auto['CAP'] and auto['SEM'],
        'FG-13': state.get('authorizes') == ['F37-SBX'] and isinstance(ca, list) and set(ca) == CANNOT_AUTHORIZE,
        'FG-14': state.get('revocation') is None,
    }
    declared = {c.get('id'): c.get('status') for c in crit if isinstance(c, dict)}
    mismatch = [fg for fg, ok in computed_auto.items() if declared.get(fg) != ('CUMPLE' if ok else 'NO CUMPLE')]
    out.append((not mismatch, f'los criterios AUTO declarados coinciden con los recalculados; difieren: {mismatch}'))
    unbacked = [c.get('id') for c in crit if isinstance(c, dict) and c.get('id') in FG_TEAM
                and c.get('status') == 'CUMPLE' and not evidence_ok(s['root'], c.get('evidence'))]
    out.append((not unbacked, f'cada criterio de EQUIPO en CUMPLE tiene evidencia archivada; sin evidencia: {unbacked}'))
    auth = state.get('f37_authorized_ei')
    classes = matrix_classes(s)
    auth_ok = auth is None or (isinstance(auth, list) and bool(auth) and len(set(auth)) == len(auth)
                               and all(classes.get(e) in ('ALLOWED', 'CONDITIONAL') for e in auth))
    out.append((auth_ok, f'la autorización de F37-SBX solo lista EI ALLOWED o CONDITIONAL: {auth}'))
    result = evaluate_gate(state, classes, lambda p: evidence_ok(s['root'], p))
    if mismatch and result == 'SUPERADO':
        result = 'NO SUPERADO'
    out.append((state.get('declared_result') == result,
                f'resultado declarado {state.get("declared_result")!r} = recalculado {result!r}'))
    doc = norm(s['texts'].get(GATE_DOC) or '')
    rows = {r[0]: r for r in table_rows(doc, 'FG-')}
    doc_err = []
    for c in crit:
        r = rows.get(c.get('id'))
        if not r or len(r) != 5:
            doc_err.append(f'{c.get("id")}: sin fila')
            continue
        if r[2] != ('EQUIPO' if c.get('kind') == 'team' else 'AUTO') or r[4] != c.get('status'):
            doc_err.append(f'{c.get("id")}: tipo o estado distinto del JSON')
    out.append((not doc_err and sorted(rows) == FG_IDS, f'tabla FG del documento = JSON; diferencias: {doc_err}'))
    phrase = f'F36-SBX-GATE = {result}'
    where = [rel for rel in [GATE_DOC, f'{PKG}/README.md'] if phrase not in norm(s['texts'].get(rel) or '')]
    out.append((not where, f'«{phrase}» declarado en el gate y en el README; falta en: {where}'))
    if result != 'NO SUPERADO':
        out.append((False, f'el gobierno declara F36-SBX-GATE = NO SUPERADO y el gate da {result}'))
    return out, result


RULES = [('STR', rule_str), ('LNK', rule_lnk), ('GOV', rule_gov), ('SEM', rule_sem), ('CAP', rule_cap),
         ('CTR', rule_ctr), ('THR', rule_thr), ('EVA', rule_eva), ('FRZ', rule_frz), ('DEP', rule_dep),
         ('PII', rule_pii)]


def run(s):
    """Devuelve [(regla, ok, mensaje)] y el resultado del gate."""
    results = []
    auto = {}
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
