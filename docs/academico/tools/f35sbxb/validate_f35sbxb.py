"""F35-SBX-B — gate sucesor sobre HEAD (incremento B1).

Valida el HEAD actual de la rama de B, de develop o de main (DH-B04). No sustituye esa validación por los gates
históricos congelados, que se ejecutan anclados como evidencia complementaria (DH-B01, DH-B02). Solo biblioteca
estándar. Primero recoge el estado real (Git, índice, sistema de archivos y documentos) y después evalúa reglas puras;
los casos negativos mutan una copia del estado en memoria.

  CTX  rama permitida, HEAD no separado; E, el cierre de B0 y la base de B como ancestros de HEAD.
  AIN  F35-SBX-A idéntica a E: bytes reales, sin archivos extra ni enlaces, árbol de HEAD sin cambios (DH-B09).
  B0F  documento de B0 idéntico a su cierre auditado.
  SBX  SBX-01..SBX-18 recalculados sobre HEAD con compute_sbx() de validate_f34e.py, importado solo tras verificar
       sus bytes y los de los módulos que carga contra E (DH-B13).
  GOV  trece estados exactos; F35-SBX-B solo INICIADA; ninguna línea añadida que desbloquee nada (DH-B11).
  SCP  delta exacto respecto de la base de B en el árbol de HEAD, el árbol de trabajo, el índice y lo no seguido.
  FSY  recorrido real de las carpetas de B: sin archivos fuera de la lista (aunque Git los ignore) ni enlaces.
  FLG  sin flags del índice: solo «H» en git ls-files -v (h = assume-unchanged, S = skip-worktree, s = ambos).
  CNT  archivos de B: UTF-8 sin NUL, CR ni BOM; sin PII; solo .md, .json y .py; claves JSON sin capacidades prohibidas.
  DEP  código de tools/f35sbxb: biblioteca estándar autorizada, sin importaciones dinámicas ni dependencias de ML.

Cualquier error de Git, de lectura o de importación, criterio no evaluable o estado desconocido: falla cerrado (DH-B10).
"""
import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

E = '61f94e23fc30b00a848a4558830b6d65f81dff87'          # commit E: cierre endurecido de F35-SBX-A
B0_CLOSE = 'cc634eb9dcc5c0cc0d77b911bb3815182b8319c2'   # cierre auditado de B0
B_BASE = '430f3f544c3542cabac8028a122c8a0c2a97390b'     # develop al iniciar F35-SBX-B (B0 integrada)
B_BRANCH = 'feature/f35-sbx-b-deterministic-pipeline'
BRANCHES = (B_BRANCH, 'develop', 'main')

A_PATHS = ('docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx',
           'docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
           'docs/academico/tools/f34/validate_f34.py', 'docs/academico/tools/f34b/validate_f34b.py',
           'docs/academico/tools/f34e/validate_f34e.py')
A_COUNT = 22
B0_DOC = 'docs/academico/evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md'
B_DIRS = ('docs/academico/evidencia-sbx-b', 'docs/academico/tools/f35sbxb')
PYCACHE_OK = ('docs/academico/tools/f35sbx/__pycache__', 'docs/academico/tools/f35sbxb/__pycache__')
GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
# Alcance exacto de B1 respecto de B_BASE: ruta -> estado esperado. Todas obligatorias.
SCOPE = {
    'CLAUDE.md': 'M',
    'docs/PROGRESS.md': 'M',
    'docs/academico/evidencia-sbx-b/README.md': 'M',
    'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md': 'A',
    GATE: 'A',
}
# Archivos reales que deben existir, exactamente, en las carpetas de B.
B_FILES = frozenset({'docs/academico/evidencia-sbx-b/README.md', B0_DOC,
                     'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md', GATE})
GOVERNANCE = ('CLAUDE.md', 'docs/PROGRESS.md')
STATES = ['- G0 real = NO APROBADA', '- G0-09 = CUMPLIDO', '- G0-14 = CUMPLIDO', '- G0-02 = PENDIENTE EXTERNO',
          '- G0-03 = PENDIENTE EXTERNO', '- G0-12 = PENDIENTE EXTERNO', '- ADR-005 = PROPUESTA',
          '- G0-SBX = APROBADA CON RESTRICCIONES', '- F35 productiva = BLOQUEADA', '- F35-SBX = HABILITADA',
          '- F36–F40 = BLOQUEADAS', '- Alcance C = BLOQUEADO', '- Datos reales = PROHIBIDOS']
B_STATE_RX = re.compile(r'F35-SBX-B\s+(NO\s+INICIADA|[A-ZÁÉÍÓÚÑ]{2,})')
UNLOCK = [re.compile(p) for p in (
    r'\bG0 real\s*[=:]?\s*APROBADA', r'\bG0 real\s+(HABILITAD|DESBLOQUEAD)',
    r'\bADR-005\s*[=:]?\s*(APROBAD|ACEPTAD)',
    r'\bF35 productiva\s*[=:]?\s*(HABILITAD|INICIAD|DESBLOQUEAD|APROBAD)',
    r'\b(F3[6-9]|F40)\b[^.;\n]{0,40}?\b(HABILITAD|INICIAD|DESBLOQUEAD|AUTORIZAD)',
    r'\b(Alcance|Scope) C\s*[=:]?\s*(HABILITAD|DESBLOQUEAD|APROBAD)',
    r'\b[Dd]atos reales\s*[=:]?\s*(PERMITID|AUTORIZAD|HABILITAD)')]
SBX_MODULES = ('docs/academico/tools/f34e/validate_f34e.py', 'docs/academico/tools/f34/validate_f34.py',
               'docs/academico/tools/f34a/validate_f34a.py', 'docs/academico/tools/f34b/validate_f34b.py')
SBX_IDS = [f'SBX-{i:02d}' for i in range(1, 19)]
SBX_INFO = {   # ID: (fuente, comprobación aplicada), según la matriz de criterios de F34E
    'SBX-01': ('Dataset F34, validate_f34.py', 'DQ-05..DQ-07 sin violaciones y manifiesto source = synthetic'),
    'SBX-02': ('validate_f34.py', 'PII-01..PII-03 sin violaciones'),
    'SBX-03': ('Árbol de archivos, F34', 'Solo CSV, JSON o Markdown en datos-sinteticos/ y g0-sandbox/; DQ-04'),
    'SBX-04': ('Árbol de archivos', 'Ningún audio ni vídeo en datos-sinteticos/ ni g0-sandbox/'),
    'SBX-05': ('schema.json, F34', 'Sin campos de score, ranking ni selección; LK-01 y LK-08'),
    'SBX-06': ('schema.json', 'Sin campos de recomendación'),
    'SBX-07': ('schema.json, matriz de trazabilidad', 'Sin selección ni contratación; RF-23 humana'),
    'SBX-08': ('traceability-master.md, Git', 'Fila RF-23 «humana» y baseline sin cambios'),
    'SBX-09': ('Matriz de trazabilidad, validate_f34a.py', 'Fila RF-21 sin cambios y regla RANK'),
    'SBX-10': ('F34, schema.json', 'CTX-01..CTX-10 y organization_token'),
    'SBX-11': ('schema.json, F34', 'provenance en evidence y DQ-07'),
    'SBX-12': ('Registros F34C, validate_f34b.py', 'G0-09 derivado CUMPLIDO'),
    'SBX-13': ('validate_f34b.py, ADR-005', 'G0-14 CUMPLIDO y ADR-005 canónico PROPUESTA'),
    'SBX-14': ('F34, manifest.json', 'source_type = synthetic, [SINTÉTICO] y advertencia del manifiesto'),
    'SBX-15': ('Recorrido del runtime', 'Ningún archivo del runtime referencia los datos sintéticos ni G0-SBX'),
    'SBX-16': ('Git', 'Runtime, dependencias, migraciones y baseline sin cambios frente a la base fija'),
    'SBX-17': ('F34B_Decision_G0.md', 'Alcance C no habilitado'),
    'SBX-18': ('F34B_Decision_G0.md, validate_f34b.py', 'G0 = NO APROBADA y G0-02/03/12 sin cerrar'),
}
STDLIB_OK = {'ast', 'copy', 'hashlib', 'importlib', 'json', 'os', 're', 'subprocess', 'sys'}
PII = [re.compile(p) for p in (
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}',                          # correo
    r'\bDNI\b\D{0,10}\d{8}(?![0-9A-Za-z])',                                    # DNI
    r'(?<![0-9A-Za-z])(\+?51[\s-]?)?9\d{2}[\s-]?\d{3}[\s-]?\d{3}(?![0-9A-Za-z])',  # celular
    r'(?<![0-9A-Za-z])(10|20)\d{9}(?![0-9A-Za-z])')]                           # RUC
JSON_KEY_RX = re.compile(r'score|rank|recommend|recomend|best|mejor|select|selecci|hire|contrat|ocr|pars|extract|'
                         r'extracc|embedding|vector|semantic|semántic|llm', re.I)
MAX_BYTES = 1_000_000


class GitError(Exception):
    pass


def git(*args):
    try:
        p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    except OSError:
        return None, b''
    return p.returncode, p.stdout


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def real_bytes(rel):
    """Bytes reales de un archivo regular; enlaces, otros tipos y errores de lectura → None (falla cerrado)."""
    full = os.path.join(ROOT, rel)
    if os.path.islink(full) or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def walk(roots):
    """Archivos reales bajo las rutas, sin seguir enlaces. Solo se omiten los __pycache__ autorizados, y solo con
    archivos regulares .pyc directos. (conjunto de rutas, problemas)."""
    found, problems = set(), []

    def visit(rel):
        full = os.path.join(ROOT, rel)
        try:
            with os.scandir(full) as entries:
                for entry in entries:
                    sub = f'{rel}/{entry.name}'
                    if entry.is_symlink():
                        problems.append(f'enlace en una ruta protegida: {sub}')
                    elif entry.is_dir(follow_symlinks=False):
                        if sub in PYCACHE_OK:
                            bad = [e.name for e in os.scandir(entry.path) if not (
                                e.name.endswith('.pyc') and not e.is_symlink() and e.is_file(follow_symlinks=False))]
                            if bad:
                                problems.append(f'entradas no permitidas en {sub}: {sorted(bad)[:3]}')
                        else:
                            visit(sub)
                    elif entry.is_file(follow_symlinks=False):
                        found.add(sub)
                    else:
                        problems.append(f'objeto especial en una ruta protegida: {sub}')
        except OSError as e:
            problems.append(f'{rel} ilegible ({e.__class__.__name__}): falla cerrado')

    for rel in roots:
        full = os.path.join(ROOT, rel)
        if os.path.islink(full):
            problems.append(f'ruta protegida convertida en enlace: {rel}')
        elif os.path.isdir(full):
            visit(rel)
        elif os.path.lexists(full):
            found.add(rel)
    return found, problems


def name_status(data):
    parts = data.split(b'\x00')
    return {(parts[i].decode(), parts[i + 1].decode('utf-8', 'replace')) for i in range(0, len(parts) - 1, 2)
            if parts[i]}


def sbx_eval(must, reader=real_bytes):
    """DH-B13: verificar contra E los bytes de validate_f34e.py y de los módulos que carga; solo entonces ejecutar
    compute_sbx() con los bytes verificados. (resultados, error)."""
    try:
        verified = {}
        for rel in SBX_MODULES:
            oid = must('rev-parse', f'{E}:{rel}').decode().strip()
            data = reader(rel)
            if data is None or blob_id(data) != oid:
                return None, f'{rel}: distinto de su blob en E; no se importa (falla cerrado)'
            verified[rel] = data
        path = os.path.join(ROOT, SBX_MODULES[0])
        spec = importlib.util.spec_from_file_location('f35sbxb_validate_f34e', path)
        module = importlib.util.module_from_spec(spec)
        exec(compile(verified[SBX_MODULES[0]], path, 'exec'), module.__dict__)
        results = module.compute_sbx()[0]
        return {k: (v[0] is True, v[1]) for k, v in results.items()}, None
    except Exception as e:          # cualquier fallo de evaluación deja los criterios como no evaluables
        return None, f'compute_sbx() no evaluable ({e.__class__.__name__}: {e}): falla cerrado'


def collect(runner=git, reader=real_bytes):
    """Estado real de HEAD. Cualquier error de Git queda en S['errors'] y hace fallar CTX."""
    S = {'errors': []}

    def must(*args):
        rc, out = runner(*args)
        if rc != 0:
            raise GitError(f'git {" ".join(args[:3])} → {rc}')
        return out
    try:
        S['inside'] = must('rev-parse', '--is-inside-work-tree').strip() == b'true'
        S['branch'] = must('branch', '--show-current').decode().strip()
        S['head'] = must('rev-parse', '--verify', 'HEAD^{commit}').decode().strip()
        S['ancestors'] = {}
        for name, commit in (('E', E), ('B0', B0_CLOSE), ('base de B', B_BASE)):
            rc, _ = runner('merge-base', '--is-ancestor', commit, 'HEAD')
            if rc not in (0, 1):
                raise GitError(f'merge-base {name} → {rc}')
            S['ancestors'][name] = rc == 0
        S['flags'] = [x.decode('utf-8', 'replace') for x in must('ls-files', '-v', '-z').split(b'\x00')
                      if x and not x.startswith(b'H ')]
        expected = {}
        for entry in must('ls-tree', '-r', '-z', '--full-tree', E, '--', *A_PATHS).split(b'\x00'):
            if entry:
                meta, _, path = entry.partition(b'\t')
                expected[path.decode()] = tuple(meta.decode().split())
        S['a_expected'] = expected
        S['a_real'] = {p: (None if (d := reader(p)) is None else blob_id(d)) for p in expected}
        S['a_fs'], S['a_walk'] = walk(A_PATHS)
        S['a_head_diff'] = [x for x in must('diff', '--name-only', '-z', E, 'HEAD', '--', *A_PATHS).decode().split('\x00') if x]
        S['b0_blob'] = must('rev-parse', f'{B0_CLOSE}:{B0_DOC}').decode().strip()
        S['b0_real'] = None if (d := reader(B0_DOC)) is None else blob_id(d)
        S['delta'] = {
            'HEAD': name_status(must('diff', '--name-status', '--no-renames', '-z', B_BASE, 'HEAD')),
            'árbol': name_status(must('diff', '--name-status', '--no-renames', '-z', B_BASE)),
            'índice': name_status(must('diff', '--cached', '--name-status', '--no-renames', '-z', B_BASE)),
        }
        S['untracked'] = {x for x in must('ls-files', '--others', '--exclude-standard', '-z').decode().split('\x00') if x}
        S['b_fs'], S['b_walk'] = walk(B_DIRS)
        S['links'] = sorted(p for p in set(SCOPE) | B_FILES if os.path.islink(os.path.join(ROOT, p)))
        S['files'] = {p: reader(p) for p in sorted(B_FILES)}
        S['gov'] = {p: reader(p) for p in GOVERNANCE}
        S['gov_base'] = {p: must('show', f'{B_BASE}:{p}') for p in GOVERNANCE}
        S['sbx'], S['sbx_error'] = sbx_eval(must, reader)
    except (GitError, OSError, ValueError) as e:
        S['errors'].append(f'estado Git o de archivos no verificable: {e}')
    return S


# ---------------------------------------------------------------- reglas puras sobre el estado
def text_of(data):
    if data is None:
        return None
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None


def r_ctx(S):
    out = list(S['errors'])
    if out:
        return out
    if not S.get('inside'):
        out.append('no es un árbol de trabajo Git')
    if S.get('branch') not in BRANCHES:
        out.append(f'rama no permitida o HEAD separado: «{S.get("branch")}»')
    out += [f'{name} no es ancestro de HEAD' for name, ok in S.get('ancestors', {}).items() if not ok]
    if len(S.get('ancestors', {})) != 3:
        out.append('ascendencia no verificable')
    return out


def r_ain(S):
    if S['errors']:
        return ['integridad de A no verificable (falla cerrado)']
    out = []
    exp = S['a_expected']
    if len(exp) != A_COUNT:
        out.append(f'F35-SBX-A en E debería tener {A_COUNT} archivos protegidos y tiene {len(exp)}')
    bad = [p for p, meta in exp.items() if meta[:2] != ('100644', 'blob') or S['a_real'].get(p) != meta[2]]
    if bad:
        out.append(f'F35-SBX-A distinta de E, eliminada o ilegible: {sorted(bad)[:5]}')
    extra = sorted(S['a_fs'] - set(exp))
    if extra:
        out.append(f'archivos extra en F35-SBX-A: {extra[:5]}')
    out += S['a_walk']
    if S['a_head_diff']:
        out.append(f'árbol de HEAD cambia F35-SBX-A respecto de E: {S["a_head_diff"][:5]}')
    return out


def r_b0f(S):
    if S['errors']:
        return ['B0 no verificable (falla cerrado)']
    return [] if S['b0_real'] == S['b0_blob'] else [f'{B0_DOC}: distinto de su cierre auditado']


def r_sbx(S):
    if S['errors']:
        return ['SBX-01..SBX-18 no evaluables (falla cerrado)']
    if S['sbx'] is None:
        return [S['sbx_error'] or 'SBX-01..SBX-18 no evaluables (falla cerrado)']
    out = []
    if set(S['sbx']) != set(SBX_IDS):
        out.append(f'criterios no evaluables o desconocidos: {sorted(set(SBX_IDS) ^ set(S["sbx"]))}')
    out += [f'{k} incumplido (clase B): {S["sbx"][k][1]}' for k in SBX_IDS if k in S['sbx'] and not S['sbx'][k][0]]
    return out


def r_gov(S):
    if S['errors']:
        return ['gobierno no verificable (falla cerrado)']
    out = []
    for path in GOVERNANCE:
        text, base = text_of(S['gov'][path]), text_of(S['gov_base'][path])
        if text is None or base is None:
            out.append(f'{path}: ilegible (falla cerrado)')
            continue
        sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        states = [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)]
        if states != STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        vigente = section + '\n' + '\n'.join(ln for ln in text.splitlines() if ln.startswith('Última actualización:'))
        b_states = [' '.join(m.split()) for m in B_STATE_RX.findall(vigente)]
        if not b_states or set(b_states) != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(set(b_states))}')
        added = [ln for ln in text.splitlines() if ln not in set(base.splitlines())]
        hits = [ln[:90] for ln in added for rx in UNLOCK if rx.search(ln)]
        if hits:
            out.append(f'{path}: líneas añadidas que desbloquean un estado prohibido: {hits[:2]}')
    return out


def r_scp(S):
    if S['errors']:
        return ['alcance no verificable (falla cerrado)']
    out = []
    for where, delta in S['delta'].items():
        for status, path in sorted(delta):
            if SCOPE.get(path) != status:
                out.append(f'{where}: cambio fuera del alcance de B1 o con estado inesperado: {status} {path}')
    present = {p for st, p in S['delta']['HEAD'] | S['delta']['árbol']} | {p for p in S['untracked'] if SCOPE.get(p) == 'A'}
    missing = sorted(set(SCOPE) - present)
    if missing:
        out.append(f'rutas obligatorias de B1 ausentes del delta: {missing}')
    stray = sorted(p for p in S['untracked'] if SCOPE.get(p) != 'A')
    if stray:
        out.append(f'archivos sin seguimiento fuera del alcance de B1: {stray[:5]}')
    return out


def r_fsy(S):
    if S['errors']:
        return ['sistema de archivos no verificable (falla cerrado)']
    out = list(S['b_walk'])
    if S['b_fs'] != B_FILES:
        out.append(f'carpetas de B distintas de la lista exacta: extra={sorted(S["b_fs"] - B_FILES)[:3]} '
                   f'faltan={sorted(B_FILES - S["b_fs"])[:3]}')
    if S['links']:
        out.append(f'enlaces en rutas de B o de gobierno: {S["links"][:3]}')
    return out


def r_flg(S):
    if S['errors']:
        return ['índice no verificable (falla cerrado)']
    return [f'flags del índice que ocultan cambios: {S["flags"][:5]}'] if S['flags'] else []


def r_cnt(S):
    if S['errors']:
        return ['contenido no verificable (falla cerrado)']
    out = []
    for path, data in S['files'].items():
        if not path.endswith(('.md', '.json', '.py')):
            out.append(f'{path}: tipo de archivo no autorizado')
            continue
        if data is None or len(data) > MAX_BYTES or b'\x00' in data or b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
            out.append(f'{path}: ilegible, binario, CR, BOM o tamaño excesivo')
            continue
        text = text_of(data)
        if text is None:
            out.append(f'{path}: no es UTF-8')
            continue
        if not path.endswith('.py'):
            hits = [m.group(0) for rx in PII for m in [rx.search(text)] if m]
            if hits:
                out.append(f'{path}: posible dato personal: {hits[:2]}')
        if path.endswith('.json'):
            try:
                keys = []

                def walk_keys(o):
                    if isinstance(o, dict):
                        for k, v in o.items():
                            keys.append(k)
                            walk_keys(v)
                    elif isinstance(o, list):
                        for v in o:
                            walk_keys(v)
                walk_keys(json.loads(text))
                bad = [k for k in keys if JSON_KEY_RX.search(k)]
                if bad:
                    out.append(f'{path}: claves con capacidades prohibidas: {bad[:3]}')
            except ValueError:
                out.append(f'{path}: JSON inválido')
    return out


def r_dep(S):
    if S['errors']:
        return ['código no verificable (falla cerrado)']
    out = []
    for path, data in S['files'].items():
        if not path.endswith('.py'):
            continue
        try:
            tree = ast.parse(text_of(data) or '')
        except (SyntaxError, ValueError) as e:
            out.append(f'{path}: código ilegible ({e.__class__.__name__})')
            continue
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods |= {a.name.split('.')[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    out.append(f'{path}: importación relativa')
                mods.add((node.module or '').split('.')[0])
            elif isinstance(node, ast.Call):
                fn = node.func
                name = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else ''
                if name in ('__import__', 'import_module'):
                    out.append(f'{path}: importación dinámica')
        out += [f'{path}: dependencia no autorizada «{m}»' for m in sorted(mods - STDLIB_OK)]
    return out


RULES = {'CTX': r_ctx, 'AIN': r_ain, 'B0F': r_b0f, 'SBX': r_sbx, 'GOV': r_gov, 'SCP': r_scp, 'FSY': r_fsy,
         'FLG': r_flg, 'CNT': r_cnt, 'DEP': r_dep}


def run_rules(S):
    return {rid: fn(S) for rid, fn in RULES.items()}


# ---------------------------------------------------------------- casos negativos (estado mutado en memoria)
def mutate(fn):
    def apply(S):
        T = copy.deepcopy(S)
        fn(T)
        return T
    return apply


def gov_sub(old, new):
    def fn(T):
        for p in GOVERNANCE:
            text = T['gov'][p].decode('utf-8')
            assert old in text, old
            T['gov'][p] = text.replace(old, new, 1).encode('utf-8')
    return mutate(fn)


def gov_add(line):
    return mutate(lambda T: T['gov'].__setitem__('CLAUDE.md', T['gov']['CLAUDE.md'] + f'\n{line}\n'.encode('utf-8')))


B1_DOC = 'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md'
README_B = 'docs/academico/evidencia-sbx-b/README.md'
CASES = [
    ('NB-01', 'SBX', 'SBX-05 incumplido (campo de puntaje en schema.json)',
     mutate(lambda T: T['sbx'].__setitem__('SBX-05', (False, ['applications.score'])))),
    ('NB-02', 'GOV', 'G0 real declarada APROBADA', gov_sub('- G0 real = NO APROBADA', '- G0 real = APROBADA')),
    ('NB-03', 'CNT', 'dato personal real en un documento de B',
     mutate(lambda T: T['files'].__setitem__(B1_DOC, T['files'][B1_DOC] + b'\nContacto: maria.quispe@colegio.edu.pe\n'))),
    ('NB-04', 'AIN', 'archivo protegido de F35-SBX-A alterado',
     mutate(lambda T: T['a_real'].__setitem__(sorted(T['a_real'])[0], '0' * 40))),
    ('NB-05', 'SCP', 'cambio productivo fuera del alcance (app/)',
     mutate(lambda T: T['delta']['árbol'].add(('M', 'app/Models/User.php')))),
    ('NB-06', 'FSY', 'archivo extra no autorizado en evidencia-sbx-b (ignorado por Git)',
     mutate(lambda T: T['b_fs'].add('docs/academico/evidencia-sbx-b/oculto.md'))),
    ('NB-07', 'FSY', 'enlace simbólico en una ruta de B', mutate(lambda T: T['links'].append(README_B))),
    ('NB-08', 'FLG', 'assume-unchanged en CLAUDE.md', mutate(lambda T: T['flags'].append('h CLAUDE.md'))),
    ('NB-09', 'FLG', 'skip-worktree en el documento de B0', mutate(lambda T: T['flags'].append(f'S {B0_DOC}'))),
    ('NB-10', 'CTX', 'error de Git', lambda S: collect(runner=lambda *a: (128, b''))),
    ('NB-11', 'CTX', 'estado desconocido: HEAD separado', mutate(lambda T: T.__setitem__('branch', ''))),
    ('NB-12', 'SBX', 'estado desconocido: criterio SBX-18 no evaluable',
     mutate(lambda T: T['sbx'].pop('SBX-18'))),
    ('NB-13', 'GOV', 'intento de habilitar F36–F40', gov_sub('- F36–F40 = BLOQUEADAS', '- F36–F40 = HABILITADAS')),
    ('NB-14', 'GOV', 'línea añadida que habilita el alcance C', gov_add('Alcance C = HABILITADO para F35-SBX-B.')),
    ('NB-15', 'GOV', 'F35-SBX-B declarada CERRADA en el estado vigente',
     gov_sub('F35-SBX-B INICIADA solo como sandbox', 'F35-SBX-B CERRADA solo como sandbox')),
    ('NB-16', 'B0F', 'documento de B0 modificado', mutate(lambda T: T.__setitem__('b0_real', '1' * 40))),
    ('NB-17', 'DEP', 'dependencia de ML en el código de B',
     mutate(lambda T: T['files'].__setitem__(GATE, T['files'][GATE] + b'\nimport sklearn\n'))),
    ('NB-18', 'CNT', 'JSON de B con un campo de puntaje',
     mutate(lambda T: T['files'].__setitem__('docs/academico/evidencia-sbx-b/x.json', b'{"candidate_score": 1}'))),
]


def integrity_cases(S):
    """DH-B13: un módulo de compute_sbx() alterado no se importa (lectura simulada, sin tocar archivos)."""
    def must(*args):
        rc, out = git(*args)
        if rc != 0:
            raise GitError(str(rc))
        return out
    tampered = lambda rel: (real_bytes(rel) or b'') + (b'\n# alterado\n' if rel == SBX_MODULES[1] else b'')
    res, err = sbx_eval(must, tampered)
    return [(res is None and bool(err) and 'no se importa' in err,
             f'NB-19 SBX: módulo de compute_sbx() alterado no se importa (falla cerrado) — {err}')]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    S = collect()
    res = run_rules(S)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:3]}' if viol else ''))
    print('SBX-01..SBX-18 sobre HEAD (DH-B13):')
    for k in SBX_IDS:
        ok, detail = (S.get('sbx') or {}).get(k, (False, S.get('sbx_error') or 'no evaluable'))
        fuente, comprobacion = SBX_INFO[k]
        motivo = '' if ok else f' | motivo: {str(detail)[:120]}'
        print(f'  {k} | {"PASS" if ok else "FAIL"} | fuente: {fuente} | comprobación: {comprobacion}{motivo}')
    for cid, rule, what, mut in CASES:
        try:
            T = mut(S)
        except (AssertionError, KeyError, IndexError, TypeError, AttributeError, ValueError) as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({e.__class__.__name__}: {e})')
            continue
        add(run_rules(T)[rule], f'{cid} detectado por {rule}: {what}')
    for ok, msg in integrity_cases(S):
        add(ok, msg)
    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    print(f'validate_f35sbxb: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
