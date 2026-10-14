"""F35-SBX-B — cierre de la capa sucesora, B2-SUCCESSOR-FREEZE (validate_f35sbxb2_sucesor_freeze.py).

Uso:  python -I docs/academico/tools/f35sbxb2_sucesor_freeze/validate_f35sbxb2_sucesor_freeze.py   (sin -I, se relanza)

Resuelve AF-L02. Ancla desde fuera la capa sucesora auditada (9d6fb15) y conserva la evaluación material vigente: el
gate sucesor aprobado se ejecuta intacto sobre HEAD. El repositorio solo se lee; los subgates escriben únicamente sus
temporales fuera de él. Cada objeto Git que se lee se verifica recalculando su identificador, ninguna lectura sigue
objetos de reemplazo, y todo error, salida incompleta o estado no evaluable falla cerrado.

Nivel A — capa sucesora; su ancla registrada es 9d6fb15.
  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; ninguna variable de Git que redirija el
       repositorio, el índice, los objetos o las referencias; Git sobre el repositorio de este archivo, con historia
       completa y sin injertos ni objetos de reemplazo.
  ANC  el candidato 2472fd6, el freeze 9961d2d y el sucesor 9d6fb15 son commits íntegros en cadena hasta HEAD. El
       conjunto protegido es el delta de Git entre el freeze y el sucesor, igual al contrato del sucesor (leído por AST
       de su blob, sin ejecutarlo), y sus superficies son carpetas nuevas en el sucesor.
  MAN  el manifiesto es, byte a byte, la serialización canónica de lo que se deriva de esos objetos.
  HIS  en cada commit posterior al sucesor que lleva a HEAD, merges incluidos, el conjunto y las superficies son los
       del sucesor.
  ARB  árbol de HEAD.   IDX  índice en etapa 0.   FLG  sin flags en el índice.
  DSK  disco: archivos regulares sin enlaces y superficies exactas.
  VIG  evaluación material vigente: el gate sucesor, verificado contra su blob en 9d6fb15, se ejecuta sobre HEAD, y
       solo se acepta la evolución de alcance de clase A que introduce este cierre. MAT ejecuta el gate de B2 y solo
       puede fallar SCP, por las rutas enumeradas; el resto del sucesor tiene que pasar.
  ALC  alcance exacto del cierre: frente al sucesor, HEAD, el índice y el árbol de trabajo solo añaden las rutas del
       cierre, y no hay archivos sin seguimiento.
Nivel B — capa del cierre. Su ancla es el commit que la completa: se deriva de Git y se registra fuera, nunca en un
archivo.
  FRZ  un único commit posterior al sucesor completa la capa y HEAD desciende de él. Desde él, cada commit, HEAD, el
       índice y el disco tienen exactamente sus archivos.
  DEP  los archivos Python del cierre solo importan la biblioteca estándar autorizada y no ejecutan código dinámico.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación, como los gates anteriores: python -I, relanzado con os.spawnv.
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
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'      # B2_CANDIDATE
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'         # B2-FREEZE
SUCCESSOR = '9d6fb157bb818574217e3675da1849e8d1010962'      # capa sucesora auditada; registrada aquí tras existir
B2_TRANSITION = '12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa'  # transición de gobierno de B2
SUC_VALIDATOR = 'docs/academico/tools/f35sbxb2_sucesor/validate_f35sbxb2_sucesor.py'
# Contrato del sucesor que se lee por AST de su blob verificado: constantes literales y la fórmula de su alcance.
SUC_LITERALS = ('FREEZE_DIRS', 'SUCESOR_DIRS', 'ORDER', 'PLANES')
SUC_FORMULA = ("tuple(sorted(f'{folder}/{name}' for group in (FREEZE_DIRS, SUCESOR_DIRS) "
               "for folder, names in group.items() for name in names))")
# Capa del cierre (nivel B), con su contenido exacto.
CLOSURE_TOOLS = 'docs/academico/tools/f35sbxb2_sucesor_freeze'
CLOSURE_DIRS = {'docs/academico/evidencia-sbx-b2-sucesor-freeze': ('F35SBXB_B2_Sucesor_Freeze.md',),
                CLOSURE_TOOLS: ('b2_sucesor_freeze_manifest.json', 'test_f35sbxb2_sucesor_freeze.py',
                                'validate_f35sbxb2_sucesor_freeze.py')}
CLOSURE_FILES = tuple(sorted(f'{folder}/{name}' for folder, names in CLOSURE_DIRS.items() for name in names))
VALIDATOR = CLOSURE_TOOLS + '/validate_f35sbxb2_sucesor_freeze.py'
MANIFEST = CLOSURE_TOOLS + '/b2_sucesor_freeze_manifest.json'
TESTS = CLOSURE_TOOLS + '/test_f35sbxb2_sucesor_freeze.py'
DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'hashlib', 'json', 'os', 're', 'subprocess', 'sys'}),
               TESTS: frozenset({'hashlib', 'json', 'os', 'subprocess', 'sys'})}
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
ORDER = ('ENT', 'ANC', 'MAN', 'HIS', 'ARB', 'IDX', 'FLG', 'DSK', 'VIG', 'ALC', 'FRZ', 'DEP')
TIMEOUT = 3600
# Variables que cambian qué repositorio, índice, objetos, historia o rutas lee Git: con ellas el cierre falla cerrado
# (y, de todos modos, Git y los subgates se ejecutan sin ninguna variable GIT_*).
REDIRECTING = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
               'GIT_COMMON_DIR', 'GIT_NAMESPACE', 'GIT_REPLACE_REF_BASE', 'GIT_NO_REPLACE_OBJECTS', 'GIT_GRAFT_FILE',
               'GIT_SHALLOW_FILE', 'GIT_CEILING_DIRECTORIES', 'GIT_DISCOVERY_ACROSS_FILESYSTEM',
               'GIT_LITERAL_PATHSPECS', 'GIT_GLOB_PATHSPECS', 'GIT_NOGLOB_PATHSPECS', 'GIT_ICASE_PATHSPECS')
GIT_ENV = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
GIT = ('git', '--no-replace-objects', '--literal-pathspecs')
# Salida del gate sucesor: sus cuatro líneas INFO, líneas FALLA y su resumen final.
SUC_SUMMARY = re.compile(r'validate_f35sbxb2_sucesor: (\d+) comprobaciones correctas, (\d+) fallas')
SUC_INFO = {
    'ANC': re.compile(r'INFO ANC: candidato ([0-9a-f]{40}); freeze registrado ([0-9a-f]{40}); HEAD ([0-9a-f]{40})'),
    'CON': re.compile(r'INFO CON: validador del freeze: código (\d+); (\d+) correctas, (\d+) fallas; candidato '
                      r'([0-9a-f]{40}); freeze derivado ([0-9a-f]{40}) \(registrado ([0-9a-f]{40})\)'),
    'MAT': re.compile(r'INFO MAT: gate de B2 sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en falla: '
                      r'([^;]*); casos en falla: (\d+); SCP: (\d+) violaciones \(alcance del sucesor: (\d+)\)'),
    'HIS': re.compile(r'INFO HIS: gate de B2 anclado sobre ([0-9a-f]{40}): código (\d+); (\d+) correctas, (\d+) fallas; '
                      r'transición derivada ([0-9a-f]{40}), registrada ([0-9a-f]{40})')}
FALLA_LINE = re.compile(r'FALLA ([A-Z]{3}): (\d+) violaciones — (.*)')
MAT_SCP = re.compile(r'SCP con violaciones ajenas al alcance del sucesor: (\d+) \(esperadas (\d+)\)')
ALC_PLANE = re.compile(r'(HEAD|árbol|índice): alcance distinto del enumerado para el sucesor: (\[.*\])')


class GitError(Exception):
    pass


ERRORS = (GitError, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError, subprocess.TimeoutExpired)


def git(*args):
    try:
        p = subprocess.run([*GIT, *args], cwd=ROOT, env=GIT_ENV, capture_output=True, timeout=TIMEOUT)
    except OSError as e:
        raise GitError(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(args[:2])} → {p.returncode}')
    return p.stdout


def is_oid(value):
    return isinstance(value, str) and len(value) == 40 and all(c in '0123456789abcdef' for c in value)


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def name_status(raw):
    parts = raw.split(b'\x00')
    return {parts[i + 1].decode('utf-8'): parts[i].decode('ascii') for i in range(0, len(parts) - 1, 2) if parts[i]}


# ---------------------------------------------------------------- objetos Git verificados (técnica de B2-FREEZE)
class Objects:
    """git cat-file --batch: cada objeto leído se verifica recalculando su identificador antes de usarlo."""

    def __init__(self):
        self.raw, self.trees = {}, {}
        try:
            self.proc = subprocess.Popen([*GIT, 'cat-file', '--batch'], cwd=ROOT, env=GIT_ENV, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except OSError as e:
            raise GitError(f'git no ejecutable ({e.__class__.__name__})')

    def read(self, oid):
        if oid in self.raw:
            return self.raw[oid]
        if not is_oid(oid):
            raise GitError(f'identificador de objeto no válido: {oid!r}')
        try:
            self.proc.stdin.write(oid.encode('ascii') + b'\n')
            self.proc.stdin.flush()
            header = self.proc.stdout.readline().split()
            if len(header) != 3 or header[0] != oid.encode('ascii'):
                raise GitError(f'objeto {oid[:12]} ausente')
            kind, size = header[1], int(header[2])
            data, end = self.proc.stdout.read(size), self.proc.stdout.read(1)
        except (OSError, ValueError) as e:
            raise GitError(f'lectura del objeto {oid[:12]} interrumpida ({e.__class__.__name__})')
        if len(data) != size or end != b'\n' or hashlib.sha1(kind + b' %d\x00' % size + data).hexdigest() != oid:
            raise GitError(f'el objeto {oid[:12]} no corresponde a su identificador')
        self.raw[oid] = (kind.decode('ascii'), data)
        return self.raw[oid]

    def close(self):
        for stream in (self.proc.stdin, self.proc.stdout):
            try:
                stream.close()
            except OSError:
                pass
        try:
            self.proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()


def commit_parts(objs, oid):
    """(árbol, padres) de un commit verificado, leídos como los lee Git: los padres siguen a la línea del árbol."""
    kind, data = objs.read(oid)
    if kind != 'commit':
        raise GitError(f'{oid[:12]} no es un commit')
    lines = data.split(b'\n\n', 1)[0].split(b'\n')
    tree = lines[0][5:].decode('ascii') if lines[0].startswith(b'tree ') else ''
    parents = []
    for line in lines[1:]:
        if not line.startswith(b'parent '):
            break
        parents.append(line[7:].decode('ascii'))
    if not is_oid(tree) or not all(is_oid(p) for p in parents):
        raise GitError(f'commit {oid[:12]} malformado')
    return tree, parents


def tree_items(objs, oid):
    if oid not in objs.trees:
        kind, data = objs.read(oid)
        if kind != 'tree':
            raise GitError(f'{oid[:12]} no es un árbol')
        out, i = {}, 0
        while i < len(data):
            space = data.index(b' ', i)
            nul = data.index(b'\x00', space)
            mode = data[i:space].decode('ascii').zfill(6)
            name, child = data[space + 1:nul].decode('utf-8'), data[nul + 1:nul + 21].hex()
            if len(child) != 40 or not name or name in out:
                raise GitError(f'árbol {oid[:12]} malformado')
            out[name] = (mode, 'tree' if mode == '040000' else 'commit' if mode == '160000' else 'blob', child)
            i = nul + 21
        objs.trees[oid] = out
    return objs.trees[oid]


def entry(objs, tree, path):
    parts = path.split('/')
    for k, name in enumerate(parts):
        found = tree_items(objs, tree).get(name)
        if found is None or (k < len(parts) - 1 and found[1] != 'tree'):
            return None
        if k == len(parts) - 1:
            return found
        tree = found[2]
    return None


def listing(objs, tree, folder):
    top = entry(objs, tree, folder)
    if top is None or top[1] != 'tree':
        return None
    out, stack = {}, [('', top[2])]
    while stack:
        prefix, oid = stack.pop()
        for name, found in tree_items(objs, oid).items():
            if found[1] == 'tree':
                stack.append((prefix + name + '/', found[2]))
            else:
                out[prefix + name] = found
    return out


def listing_diff(folder, found, want):
    if found is None:
        return [folder + '/']
    return [f'{folder}/{rel}' for rel in sorted(set(found) | set(want)) if found.get(rel) != want.get(rel)]


def ancestry(objs, head):
    """{commit: padres} de todos los ancestros de head, incluido, desde objetos verificados."""
    parents, stack = {}, [head]
    while stack:
        commit = stack.pop()
        if commit not in parents:
            parents[commit] = commit_parts(objs, commit)[1]
            stack.extend(p for p in parents[commit] if p not in parents)
    return parents


def descendants(parents, base):
    """Commits del grafo que descienden de base, sin incluirla (lo mismo que rev-list --ancestry-path base..head)."""
    children = {}
    for commit, ps in parents.items():
        for p in ps:
            children.setdefault(p, []).append(commit)
    out, stack = set(), [base]
    while stack:
        for child in children.get(stack.pop(), ()):
            if child not in out:
                out.add(child)
                stack.append(child)
    return out


# ---------------------------------------------------------------- índice y disco
def index_problems(want, paths, label):
    expected = {p: [(e[0], e[2], '0')] for p, e in want.items()}
    found = {}
    for item in git('ls-files', '-s', '-z', '--', *paths).split(b'\x00'):
        if item:
            meta, _, path = item.partition(b'\t')
            mode, oid, stage = meta.decode('ascii').split()
            found.setdefault(path.decode('utf-8'), []).append((mode, oid, stage))
    diff = sorted(p for p in set(expected) | set(found) if expected.get(p) != found.get(p))
    return [f'índice distinto {label} (entrada ausente, extra, en conflicto o con otro modo, tipo o blob): '
            f'{diff[:5]}'] if diff else []


def linked(full):
    return os.path.islink(full) or bool(getattr(os.path, 'isjunction', lambda _: False)(full))


def disk_path(rel):
    parts = rel.split('/')
    if any(linked(os.path.join(ROOT, *parts[:k])) for k in range(1, len(parts) + 1)):
        return None
    return os.path.join(ROOT, *parts)


def disk_bytes(rel):
    full = disk_path(rel)
    if full is None or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def file_problems(rel, want):
    data = disk_bytes(rel)
    if data is None:
        return [f'{rel}: ausente, enlace, objeto especial o ilegible en el disco']
    if blob_id(data) != want[2]:
        return [f'{rel}: bytes del disco distintos del blob esperado']
    if os.name != 'nt' and os.stat(disk_path(rel)).st_mode & 0o111:
        return [f'{rel}: permiso de ejecución en el disco (se espera {want[0]})']
    return []


def disk_folder(folder, want):
    """Carpeta del disco con exactamente los archivos esperados (también ignorados, ocultos y __pycache__), regulares,
    sin enlaces y con sus blobs."""
    base = disk_path(folder)
    if base is None or not os.path.isdir(base):
        return [f'{folder}: ausente, enlace o no es un directorio']
    out, found, stack = [], set(), [('', base)]
    while stack:
        prefix, path = stack.pop()
        try:
            with os.scandir(path) as it:
                items = sorted(it, key=lambda x: x.name)
        except OSError as e:
            out.append(f'{folder}/{prefix}: ilegible ({e.__class__.__name__})')
            continue
        for item in items:
            rel = prefix + item.name
            if linked(item.path):
                out.append(f'{folder}/{rel}: enlace')
            elif item.is_dir(follow_symlinks=False):
                out.append(f'{folder}/{rel}: carpeta inesperada')
                stack.append((rel + '/', item.path))
            elif item.is_file(follow_symlinks=False):
                found.add(rel)
            else:
                out.append(f'{folder}/{rel}: objeto especial')
    extra, missing = sorted(found - set(want)), sorted(set(want) - found)
    if extra or missing:
        out.append(f'{folder}: contenido del disco distinto del esperado: extra={extra[:3]} faltan={missing[:3]}')
    for rel in sorted(found & set(want)):
        out += file_problems(f'{folder}/{rel}', want[rel])
    return out


def by_folder(files, folder):
    return {p[len(folder) + 1:]: e for p, e in files.items() if p.startswith(folder + '/')}


# ---------------------------------------------------------------- nivel A: la capa sucesora desde su ancla
def successor_contract(source):
    """Constantes del gate sucesor aprobado, leídas por AST de sus bytes verificados, sin ejecutarlo."""
    assigns = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            assigns.setdefault(node.targets[0].id, []).append(node.value)
    values = {}
    for name in SUC_LITERALS:
        if len(assigns.get(name, [])) != 1:
            raise ValueError(f'el gate sucesor no asigna {name} exactamente una vez')
        values[name] = ast.literal_eval(assigns[name][0])
    nodes = assigns.get('SUCCESSOR_FILES', [])
    if len(nodes) != 1 or ast.dump(nodes[0]) != ast.dump(ast.parse(SUC_FORMULA, mode='eval').body):
        raise ValueError('el gate sucesor no define su alcance con la fórmula auditada')
    values['SUCCESSOR_FILES'] = tuple(sorted(f'{folder}/{name}' for group in (values['FREEZE_DIRS'], values['SUCESOR_DIRS'])
                                             for folder, names in group.items() for name in names))
    return values


def successor_state(objs):
    """Anclas, conjunto protegido (Git y contrato), entradas verificadas, superficies y contrato del sucesor."""
    problems = []
    frz_tree, suc_tree = commit_parts(objs, FREEZE)[0], commit_parts(objs, SUCCESSOR)[0]
    commit_parts(objs, CANDIDATE)
    if CANDIDATE == FREEZE or CANDIDATE not in ancestry(objs, FREEZE):
        problems.append(f'el freeze {FREEZE[:12]} no desciende del candidato {CANDIDATE[:12]}')
    if FREEZE == SUCCESSOR or FREEZE not in ancestry(objs, SUCCESSOR):
        problems.append(f'el sucesor {SUCCESSOR[:12]} no desciende del freeze {FREEZE[:12]}')
    derived = name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', FREEZE, SUCCESSOR))
    gate = entry(objs, suc_tree, SUC_VALIDATOR)
    if gate is None or gate[:2] != ('100644', 'blob'):
        raise GitError('el gate sucesor no es un blob regular en el sucesor')
    contract = successor_contract(objs.read(gate[2])[1].decode('utf-8'))
    declared = {f'{folder}/{name}': 'A' for folder, names in contract['SUCESOR_DIRS'].items() for name in names}
    if derived != declared:
        problems.append(f'el delta de Git entre el freeze y el sucesor no es la capa declarada por el contrato del '
                        f'sucesor: {sorted(set(derived.items()) ^ set(declared.items()))[:3]}')
    protected, entries, blobs = dict(sorted(derived.items())), {}, {}
    for path, status in protected.items():
        found, before = entry(objs, suc_tree, path), entry(objs, frz_tree, path)
        if found is None or found[:2] != ('100644', 'blob') or objs.read(found[2])[0] != 'blob':
            problems.append(f'{path}: no es un blob regular 100644 en el sucesor')
            continue
        if status != 'A' or before is not None:
            problems.append(f'{path}: estado {status} frente al freeze no confirmado por los objetos')
        entries[path], blobs[path] = found, objs.read(found[2])[1]
    surfaces = {}
    for folder in sorted({p.rsplit('/', 1)[0] for p in protected if '/' in p}):
        found = listing(objs, suc_tree, folder)
        inside = {p[len(folder) + 1:] for p in protected if p.startswith(folder + '/')}
        if entry(objs, frz_tree, folder) is not None or found is None or set(found) != inside:
            problems.append(f'{folder}: no es una carpeta creada por el sucesor con solo el conjunto protegido')
        surfaces[folder] = found or {}
    return {'problems': problems, 'protected': protected, 'entries': entries, 'blobs': blobs, 'surfaces': surfaces,
            'contract': contract}


def derived_manifest(state):
    return {
        'manifest_version': 1,
        'phase': 'F35-SBX-B',
        'increment': 'B2-SUCCESSOR-FREEZE',
        'successor_commit': SUCCESSOR,
        'freeze_commit': FREEZE,
        'candidate_commit': CANDIDATE,
        'protected_set': [{'path': path, 'status_vs_freeze': status, 'type': state['entries'][path][1],
                           'mode': state['entries'][path][0], 'blob': state['entries'][path][2],
                           'sha256': hashlib.sha256(state['blobs'][path]).hexdigest(), 'bytes': len(state['blobs'][path])}
                          for path, status in state['protected'].items() if path in state['entries']],
        'reserved_surfaces': {folder: sorted(found) for folder, found in state['surfaces'].items()},
        'closure_layer': {folder: sorted(names) for folder, names in CLOSURE_DIRS.items()},
    }


def canonical(manifest):
    return (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def manifest_problems(state):
    want = derived_manifest(state)
    data = disk_bytes(MANIFEST)
    if data is None:
        return ['manifiesto del cierre ausente, enlace o ilegible']
    if data == canonical(want):
        return []
    try:
        found = json.loads(data.decode('utf-8'))
    except ValueError:
        return ['el manifiesto del cierre no es JSON UTF-8 válido']
    if not isinstance(found, dict):
        return ['el manifiesto del cierre no es un objeto JSON']
    out = [f'«{key}» distinto de lo que se deriva de los objetos del sucesor' for key in sorted(set(want) | set(found))
           if key != 'protected_set' and found.get(key) != want.get(key)]
    listed = found.get('protected_set') if isinstance(found.get('protected_set'), list) else []
    have = {e.get('path'): e for e in listed if isinstance(e, dict)}
    need = {e['path']: e for e in want['protected_set']}
    for path in sorted(set(have) | set(need), key=str):
        a, b = have.get(path) or {}, need.get(path) or {}
        fields = sorted(str(k) for k in set(a) | set(b) if a.get(k) != b.get(k))
        if fields:
            out.append(f'protected_set {path}: {", ".join(fields)} distinto de lo que se deriva del sucesor')
    return out or ['el manifiesto del cierre tiene el contenido derivado, pero no su serialización canónica']


def seal_diff(objs, tree, state):
    out = {p for p, want in state['entries'].items() if entry(objs, tree, p) != want}
    for folder, want in state['surfaces'].items():
        out.update(listing_diff(folder, listing(objs, tree, folder), want))
    return sorted(out)


def disk_problems(state):
    inside = lambda p: any(p.startswith(folder + '/') for folder in state['surfaces'])  # noqa: E731
    out = [x for p, e in state['entries'].items() if not inside(p) for x in file_problems(p, e)]
    for folder, want in state['surfaces'].items():
        out += disk_folder(folder, want)
    return out


# ---------------------------------------------------------------- VIG: el gate sucesor intacto sobre HEAD
def run_successor(expected):
    """Ejecuta el gate sucesor con bytes verificados antes y después, con python -I y sin variables GIT_*."""
    data = disk_bytes(SUC_VALIDATOR)
    if data is None or blob_id(data) != expected:
        raise ValueError(f'{SUC_VALIDATOR} distinto de su blob {expected[:12]} en el sucesor: no se ejecuta')
    p = subprocess.run([sys.executable, '-I', '-B', disk_path(SUC_VALIDATOR)], cwd=ROOT, env=GIT_ENV,
                       capture_output=True, timeout=TIMEOUT)
    data = disk_bytes(SUC_VALIDATOR)
    if data is None or blob_id(data) != expected:
        raise ValueError(f'{SUC_VALIDATOR} cambió durante la ejecución: resultado descartado')
    return p.returncode, p.stdout, p.stderr


def parse_successor(code, stdout, stderr):
    """Salida estricta del gate sucesor: sus líneas INFO, sus líneas FALLA (lista completa de hasta tres violaciones) y
    su resumen final, coherentes con el código de salida. ValueError si no es la esperada."""
    if stderr.strip():
        raise ValueError(f'salida de error inesperada del gate sucesor: «{stderr.decode("utf-8", "replace").strip()[:120]}»')
    lines = [x for x in stdout.decode('utf-8').splitlines() if x.strip()]
    if not lines or not SUC_SUMMARY.fullmatch(lines[-1]):
        raise ValueError('el gate sucesor no terminó con su resumen: ejecución incompleta')
    info, fallas = {}, {}
    for line in lines[:-1]:
        m = FALLA_LINE.fullmatch(line)
        if m and m.group(1) not in fallas:
            items = ast.literal_eval(m.group(3))
            if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
                raise ValueError(f'violaciones ilegibles en FALLA {m.group(1)}')
            fallas[m.group(1)] = (int(m.group(2)), items)
        elif line.startswith('INFO ') and line[5:8] in SUC_INFO and line[5:8] not in info:
            info[line[5:8]] = line
        else:
            raise ValueError(f'línea no reconocida o repetida en la salida del gate sucesor: «{line[:80]}»')
    ok, ko = (int(x) for x in SUC_SUMMARY.fullmatch(lines[-1]).groups())
    if ko != len(fallas) or code != (1 if ko else 0):
        raise ValueError(f'resumen, líneas FALLA y código de salida del gate sucesor incoherentes (código {code})')
    return ok, ko, fallas, info


def vig_problems(state, head):
    """El gate sucesor sobre HEAD solo puede fallar por la evolución de alcance de clase A de este cierre."""
    contract = state['contract']
    try:
        code, stdout, stderr = run_successor(state['entries'][SUC_VALIDATOR][2])
    except ValueError as e:
        return [str(e)], f'INFO VIG: gate sucesor sobre HEAD no ejecutado: {e}'
    ok, ko, fallas, info = parse_successor(code, stdout, stderr)
    planes, own = len(contract['PLANES']), len(contract['SUCCESSOR_FILES'])
    expected_scp, with_closure = planes * own, planes * (own + len(CLOSURE_FILES))
    out = []
    mat = SUC_INFO['MAT'].fullmatch(info.get('MAT', ''))
    b2_rules = mat.group(4) if mat else 'no disponible'
    scp = mat.group(6) if mat else 'no disponible'
    if set(fallas) != {'MAT', 'ALC'} or ok + ko != len(contract['ORDER']):
        out.append(f'el gate sucesor falla en {sorted(fallas)}: solo puede fallar MAT y ALC por el alcance del cierre')
    if not mat or mat.group(1) != '1' or mat.group(4) != 'SCP' or mat.group(5) != '0' or \
            int(mat.group(6)) != with_closure or int(mat.group(7)) != expected_scp:
        out.append(f'el gate de B2 sobre HEAD no incumple solo SCP con {with_closure} violaciones de clase A: '
                   f'reglas en falla {b2_rules}, SCP {scp}')
    count, items = fallas.get('MAT', (0, []))
    match = MAT_SCP.fullmatch(items[0]) if count == 1 and len(items) == 1 else None
    if 'MAT' in fallas and (not match or (int(match.group(1)), int(match.group(2))) != (with_closure, expected_scp)):
        out.append(f'MAT del sucesor no falla solo por el recuento de SCP del cierre: {items[:2]}')
    count, items = fallas.get('ALC', (0, []))
    seen = {}
    for item in items:
        m = ALC_PLANE.fullmatch(item)
        paths = ast.literal_eval(m.group(2)) if m else None
        if not m or m.group(1) in seen or not paths or \
                not all(isinstance(t, tuple) and len(t) == 2 and t[0] in CLOSURE_FILES and t[1] == 'A' for t in paths):
            seen = None
            break
        seen[m.group(1)] = paths
    if 'ALC' in fallas and (count != planes or seen is None or set(seen) != set(contract['PLANES'])):
        out.append(f'ALC del sucesor no falla solo por las rutas del cierre en los {planes} planos: {items[:2]}')
    anc, con, his = (SUC_INFO[k].fullmatch(info.get(k, '')) for k in ('ANC', 'CON', 'HIS'))
    if not anc or anc.groups() != (CANDIDATE, FREEZE, head):
        out.append('el gate sucesor no informa el candidato, el freeze registrado y este HEAD')
    if not con or con.group(1) != '0' or con.group(3) != '0' or con.group(4) != CANDIDATE or \
            con.group(5) != FREEZE or con.group(6) != FREEZE:
        out.append('CON del sucesor no acredita el freeze registrado con código 0 y sin fallas')
    if not his or his.group(1) != CANDIDATE or his.group(2) != '0' or his.group(4) != '0' or \
            his.groups()[4:] != (B2_TRANSITION, B2_TRANSITION):
        out.append('HIS del sucesor no acredita el gate de B2 anclado en el candidato con código 0 y sin fallas')
    line = (f'INFO VIG: gate sucesor sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas del sucesor en falla: '
            f'{", ".join(sorted(fallas)) or "ninguna"}; reglas del gate de B2 en falla: {b2_rules}; SCP: {scp} '
            f'(alcance del sucesor {expected_scp}; con el cierre {with_closure})')
    return out, line


def alc_problems():
    want, out = {p: 'A' for p in CLOSURE_FILES}, []
    for plane, args in (('HEAD', ('diff', '--name-status', '--no-renames', '-z', SUCCESSOR, 'HEAD')),
                        ('árbol', ('diff', '--name-status', '--no-renames', '-z', SUCCESSOR)),
                        ('índice', ('diff', '--cached', '--name-status', '--no-renames', '-z', SUCCESSOR))):
        found = name_status(git(*args))
        if found != want:
            out.append(f'{plane}: alcance distinto del cierre frente al sucesor: '
                       f'{sorted(set(found.items()) ^ set(want.items()))[:3]}')
    untracked = [x for x in git('ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').split('\x00') if x]
    if untracked:
        out.append(f'archivos sin seguimiento fuera del alcance: {untracked[:5]}')
    return out


# ---------------------------------------------------------------- nivel B: la capa del cierre
def freeze_problems(objs, head, parents, after, info):
    cache = {}

    def layer(commit):
        if commit not in cache:
            tree = commit_parts(objs, commit)[0]
            cache[commit] = {folder: listing(objs, tree, folder) for folder in CLOSURE_DIRS}
        return cache[commit]

    def complete(found):
        return all(found[folder] is not None and all(n in found[folder] for n in names)
                   for folder, names in CLOSURE_DIRS.items())
    seals = sorted(c for c in after if complete(layer(c)) and not any(complete(layer(p)) for p in parents[c]))
    info['completion'] = seals[0] if len(seals) == 1 else None
    if len(seals) != 1:
        return ['ningún commit posterior al sucesor completa la capa del cierre' if not seals else
                f'la capa del cierre se completa en más de un commit: {[c[:12] for c in seals]}']
    completion = seals[0]
    want, out = layer(completion), []
    for folder, names in CLOSURE_DIRS.items():
        if set(want[folder]) != set(names) or any(e[:2] != ('100644', 'blob') for e in want[folder].values()):
            out.append(f'{folder}: en el commit que completa el cierre no contiene exactamente sus archivos regulares')
    later = descendants(parents, completion)
    if head != completion and head not in later:
        out.append(f'HEAD no desciende del commit que completa el cierre {completion[:12]}')
    for commit in sorted(later):
        diff = [x for folder in CLOSURE_DIRS for x in listing_diff(folder, layer(commit)[folder], want[folder])]
        if diff:
            out.append(f'{commit[:12]}: capa del cierre distinta del commit que la completa (modificada, eliminada, '
                       f'renombrada, con otro modo o con archivos extra): {diff[:3]}')
    files = {f'{folder}/{rel}': e for folder, found in want.items() for rel, e in found.items()}
    out += index_problems(files, list(CLOSURE_DIRS), 'del commit que completa el cierre')
    for folder in CLOSURE_DIRS:
        out += disk_folder(folder, want[folder])
    return out


# ---------------------------------------------------------------- entorno y dependencias
def ent_problems():
    out = []
    if not sys.flags.isolated:
        out.append('intérprete no aislado: se exige python -I')
    out += [f'{name} definida: el intérprete podría cargar código ajeno' for name in
            ('PYTHONPATH', 'PYTHONHOME', 'PYTHONUSERBASE') if os.environ.get(name)]
    hostile = sorted(name for name in os.environ if name.upper() in REDIRECTING)
    if hostile:
        out.append(f'variables de Git que redirigen el repositorio, el índice o los objetos: {hostile}')
    if not os.path.samefile(git('rev-parse', '--show-toplevel').decode('utf-8').strip(), ROOT):
        out.append('la raíz del repositorio no es la de este validador')
    if git('rev-parse', '--is-shallow-repository').strip() != b'false':
        out.append('repositorio superficial: la historia no es completa')
    grafts = git('rev-parse', '--git-path', 'info/grafts').decode('utf-8').strip()
    if os.path.lexists(grafts if os.path.isabs(grafts) else os.path.join(ROOT, grafts)):
        out.append('injertos en info/grafts: Git mostraría otra historia')
    replaced = [x for x in git('for-each-ref', '--format=%(refname)', 'refs/replace/').decode('utf-8').splitlines() if x]
    if replaced:
        out.append(f'objetos de reemplazo en refs/replace ({len(replaced)}): Git mostraría otros objetos')
    head = git('rev-parse', '--verify', '-q', 'HEAD^{commit}').decode('ascii').strip()
    if not is_oid(head):
        raise GitError('HEAD no es un commit')
    return out, head


def flag_problems():
    flagged = [item.decode('utf-8', 'replace') for item in git('ls-files', '-v', '-z').split(b'\x00')
               if item and not item.startswith(b'H ')]
    return [f'flags en el índice (assume-unchanged, skip-worktree o conflictos): {flagged[:5]}'] if flagged else []


def dep_problems():
    out = []
    for path, allowed in DEP_ALLOWED.items():
        data = disk_bytes(path)
        if data is None:
            out.append(f'{path}: ausente o ilegible')
            continue
        modules, dynamic = set(), set()
        for node in ast.walk(ast.parse(data.decode('utf-8'), filename=path)):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.add(node.module.split('.')[0] if node.level == 0 and node.module else '(relativa)')
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_CODE:
                dynamic.add(node.func.id)
        if modules - allowed:
            out.append(f'{path}: importaciones fuera de la biblioteca estándar autorizada: {sorted(modules - allowed)}')
        if dynamic:
            out.append(f'{path}: ejecución dinámica de código: {sorted(dynamic)}')
    return out


# ---------------------------------------------------------------- evaluación con fallo cerrado
def evaluate():
    viol, info, notes = {rid: [] for rid in ORDER}, [], {'completion': None, 'after': None}

    def closed(rids, why):
        for rid in rids:
            viol[rid].append(f'no evaluable: {why} (falla cerrado)')

    def check(rid, fn, *args):
        try:
            result = fn(*args)
        except ERRORS as e:
            closed((rid,), f'{e.__class__.__name__}: {e}')
            return None
        problems, rest = (result[0], result[1:]) if isinstance(result, tuple) else (result, ())
        viol[rid] += problems
        return rest

    check('DEP', dep_problems)
    try:
        problems, head = ent_problems()
    except ERRORS as e:
        closed([r for r in ORDER if r != 'DEP'], f'repositorio Git ({e.__class__.__name__}: {e})')
        return viol, info
    viol['ENT'] += problems
    check('FLG', flag_problems)
    info.append(f'INFO ANC: candidato {CANDIDATE}; freeze {FREEZE}; sucesor registrado {SUCCESSOR}; HEAD {head}')
    objs = None
    try:
        objs = Objects()
        parents = state = after = None
        try:
            parents = ancestry(objs, head)
        except ERRORS as e:
            closed(('ANC', 'HIS', 'FRZ'), f'historia desde HEAD ({e})')
        try:
            state = successor_state(objs)
            viol['ANC'] += state['problems']
        except ERRORS as e:
            closed(('ANC', 'MAN', 'HIS', 'ARB', 'IDX', 'DSK', 'VIG'), f'sucesor ({e.__class__.__name__}: {e})')
        if parents is not None:
            if SUCCESSOR in parents:
                after = descendants(parents, SUCCESSOR)
                notes['after'] = len(after)
            else:
                viol['ANC'].append('el sucesor registrado no es HEAD ni ancestro de HEAD: la historia no corresponde')
                closed(('HIS', 'FRZ'), 'no hay historia posterior al sucesor')
        if state is not None:
            check('MAN', manifest_problems, state)
            check('ARB', lambda: [f'árbol de HEAD distinto del sucesor: {d[:5]}' for d in
                                  [seal_diff(objs, commit_parts(objs, head)[0], state)] if d])
            files = dict(state['entries'])
            files.update({f'{folder}/{rel}': e for folder, found in state['surfaces'].items() for rel, e in found.items()})
            check('IDX', index_problems, files, list(state['entries']) + list(state['surfaces']), 'del sucesor')
            check('DSK', disk_problems, state)
            vig = check('VIG', vig_problems, state, head)
            if vig:
                info.append(vig[0])
            if after is not None:
                check('HIS', lambda: [f'{c[:12]}: conjunto protegido o superficies del sucesor distintos (modificados, '
                                      f'eliminados, renombrados, con otro modo o tipo, o con archivos extra): {d[:3]}'
                                      for c in sorted(after) for d in [seal_diff(objs, commit_parts(objs, c)[0], state)]
                                      if d])
        check('ALC', alc_problems)
        if after is not None:
            check('FRZ', freeze_problems, objs, head, parents, after, notes)
    except ERRORS as e:
        closed(('ANC', 'MAN', 'HIS', 'ARB', 'IDX', 'DSK', 'VIG', 'ALC', 'FRZ'), f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        if objs is not None:
            objs.close()
    after = 'no verificable' if notes['after'] is None else notes['after']
    info.append(f'INFO FRZ: commit que completa el cierre: {notes["completion"] or "ninguno"}; commits posteriores al '
                f'sucesor: {after}')
    return viol, info


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        viol, info = evaluate()
    except Exception as e:      # cualquier fallo inesperado: todas las reglas fallan cerradas
        viol = {rid: [f'evaluación interrumpida ({e.__class__.__name__}): falla cerrado'] for rid in ORDER}
        info = []
    for line in info:
        print(line)
    fallas = [rid for rid in ORDER if viol[rid]]
    for rid in fallas:
        print(f'FALLA {rid}: {len(viol[rid])} violaciones — {viol[rid][:3]}')
    print(f'validate_f35sbxb2_sucesor_freeze: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
