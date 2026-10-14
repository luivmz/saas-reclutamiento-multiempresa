"""F35-SBX-B — validador de B2-FREEZE (validate_f35sbxb2_freeze.py).

Uso:  python -I docs/academico/tools/f35sbxb2_freeze/validate_f35sbxb2_freeze.py   (sin -I, se relanza aislado)

Herramienta de integridad Git de solo lectura: no ejecuta el almacén ni el gate de B2, no abre SQLite, no usa la red y
no escribe nada. Todo error o estado no evaluable falla cerrado. Cada objeto Git que lee se verifica recalculando su
identificador con el formato de objetos de Git, y ninguna lectura sigue objetos de reemplazo. La historia se recorre
sobre esos objetos verificados, no con rev-list.

Nivel A — candidato de B2, ancla 2472fd6. La fuente de verdad es el commit candidato, no el manifiesto.
  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; Git sin variables GIT_* heredadas y sobre el
       repositorio de este archivo; historia completa, sin injertos ni objetos de reemplazo.
  CAN  el candidato es un commit íntegro y ancestro de HEAD, y la base de B2 y las anclas previas son ancestros suyos.
       El conjunto congelado es el delta de Git entre 72e86c5 y el candidato, igual al alcance del contrato que fija el
       gate aprobado (leído por AST del blob del candidato, sin ejecutarlo). Cada ruta es un blob regular 100644.
  MAN  el manifiesto es, byte a byte, la serialización canónica de lo que se deriva del candidato.
  HIS  en cada commit posterior al candidato que lleva a HEAD, merges incluidos, las rutas congeladas y las superficies
       reservadas de B2 (las carpetas que B2 creó) son idénticas al candidato: detecta modificar, eliminar, renombrar o
       cambiar el modo y restaurar después.
  ARB  árbol de HEAD idéntico al candidato.
  IDX  índice: una entrada en etapa 0 por archivo, con el modo y el blob del candidato, y nada más en las superficies.
  FLG  ningún flag en el índice del repositorio (solo H): ni assume-unchanged, ni skip-worktree, ni conflictos.
  DSK  disco: archivos regulares sin enlaces, con los bytes del candidato; superficies con su contenido exacto,
       incluidos archivos ignorados, ocultos y __pycache__.
Nivel B — capa del freeze. Su ancla es el commit que la completa, que se deriva de Git: ningún archivo registra su hash.
  FRZ  un único commit posterior al candidato completa la capa y HEAD desciende de él. Desde él, cada commit, HEAD, el
       índice y el disco tienen exactamente sus archivos, y sus carpetas no contienen nada más.
  DEP  los archivos Python de la capa solo importan la biblioteca estándar autorizada y no ejecutan código dinámico.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación, como en los gates de B1 y B2: python -I, relanzado con os.spawnv.
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
import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'   # B2_CANDIDATE: B2 reauditada y aprobada para freeze
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'      # develop al crear la rama de B2
PRIOR_ANCHORS = (('b1_audited_anchor', '8e94a60274fe39ebda3e9961bc58036b389dfc00'),
                 ('b1_freeze_closure', '3d9b78307684a0dfb093e31d28fde290b2b1cb4a'),
                 ('b2_governance_transition', '12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa'))
# Alcance de B2 tal como lo fija el gate aprobado (contrato §2.5): constantes literales y fórmulas exactas.
B2_GATE = 'docs/academico/tools/f35sbxb2/validate_f35sbxb2.py'
GATE_LITERALS = ('STORE', 'GATE2', 'GOV_PATHS', 'B2_DOCS')
GATE_FORMULAS = {'B2_FILES': 'B2_DOCS + (STORE, GATE2)',
                 'SCOPE2': "{**{p: 'A' for p in B2_FILES}, **{p: 'M' for p in GOV_PATHS}}"}
# Capa del freeze (nivel B): carpetas propias con su contenido exacto.
FREEZE_TOOLS = 'docs/academico/tools/f35sbxb2_freeze'
FREEZE_EVIDENCE = 'docs/academico/evidencia-sbx-b2-freeze'
VALIDATOR = FREEZE_TOOLS + '/validate_f35sbxb2_freeze.py'
MANIFEST = FREEZE_TOOLS + '/b2_freeze_manifest.json'
TESTS = FREEZE_TOOLS + '/test_f35sbxb2_freeze.py'
FREEZE_DIRS = {FREEZE_EVIDENCE: ('F35SBXB_B2_Freeze.md',),
               FREEZE_TOOLS: ('b2_freeze_manifest.json', 'test_f35sbxb2_freeze.py', 'validate_f35sbxb2_freeze.py')}
DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'hashlib', 'json', 'os', 'subprocess', 'sys'}),
               TESTS: frozenset({'hashlib', 'json', 'os', 'subprocess', 'sys'})}
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
ORDER = ('ENT', 'CAN', 'MAN', 'HIS', 'ARB', 'IDX', 'FLG', 'DSK', 'FRZ', 'DEP')
# Git sin variables heredadas (GIT_DIR, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_REPLACE_REF_BASE...), sin objetos de
# reemplazo y con rutas literales.
GIT_ENV = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
GIT = ('git', '--no-replace-objects', '--literal-pathspecs')


class GitError(Exception):
    pass


ERRORS = (GitError, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError)


def git(*args):
    try:
        p = subprocess.run([*GIT, *args], cwd=ROOT, env=GIT_ENV, capture_output=True)
    except OSError as e:
        raise GitError(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(args[:2])} → {p.returncode}')
    return p.stdout


def is_oid(value):
    return isinstance(value, str) and len(value) == 40 and all(c in '0123456789abcdef' for c in value)


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


# ---------------------------------------------------------------- objetos Git verificados
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
        """(tipo, contenido) de un objeto cuyo identificador coincide con su contenido."""
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
    """{nombre: (modo, tipo, oid)} de un árbol verificado."""
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
    """(modo, tipo, oid) de una ruta dentro de un árbol, o None si no existe."""
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
    """{ruta relativa: (modo, tipo, oid)} de todo lo que cuelga de una carpeta, o None si no es una carpeta."""
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
    """Commits del grafo que descienden de base, sin incluirla: lo mismo que rev-list --ancestry-path base..head."""
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


# ---------------------------------------------------------------- nivel A: raíz de confianza en el candidato
def gate_scope(source):
    """Alcance de B2 {ruta: estado} según el gate aprobado, leído por AST de sus bytes verificados, sin ejecutarlo."""
    assigns = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            assigns.setdefault(node.targets[0].id, []).append(node.value)
    values = {}
    for name in GATE_LITERALS:
        if len(assigns.get(name, [])) != 1:
            raise ValueError(f'el gate aprobado no asigna {name} exactamente una vez')
        values[name] = ast.literal_eval(assigns[name][0])
    for name, formula in GATE_FORMULAS.items():
        nodes = assigns.get(name, [])
        if len(nodes) != 1 or ast.dump(nodes[0]) != ast.dump(ast.parse(formula, mode='eval').body):
            raise ValueError(f'el gate aprobado no define {name} con la fórmula del contrato')
    files = tuple(values['B2_DOCS']) + (values['STORE'], values['GATE2'])
    scope = {**{p: 'A' for p in files}, **{p: 'M' for p in values['GOV_PATHS']}}
    if len(scope) != len(files) + len(values['GOV_PATHS']) or not all(isinstance(p, str) for p in scope):
        raise ValueError('alcance del gate aprobado no válido')
    return scope


def candidate_state(objs):
    """Conjunto congelado (Git y contrato), entradas verificadas y superficies reservadas, todo desde el candidato."""
    problems = []
    cand_tree, base_tree = commit_parts(objs, CANDIDATE)[0], commit_parts(objs, B2_BASE)[0]
    lineage = ancestry(objs, CANDIDATE)
    for name, oid in (('b2_base', B2_BASE),) + PRIOR_ANCHORS:
        if oid not in lineage or oid == CANDIDATE:
            problems.append(f'{name} ({oid[:12]}) no es ancestro del candidato')
    raw = git('diff-tree', '-r', '--no-renames', '--name-status', '-z', B2_BASE, CANDIDATE).split(b'\x00')
    derived = {raw[i + 1].decode('utf-8'): raw[i].decode('ascii') for i in range(0, len(raw) - 1, 2) if raw[i]}
    gate = entry(objs, cand_tree, B2_GATE)
    if gate is None or gate[:2] != ('100644', 'blob'):
        raise GitError('el gate aprobado no es un blob regular en el candidato')
    contract = gate_scope(objs.read(gate[2])[1].decode('utf-8'))
    if derived != contract:
        problems.append(f'el delta de Git entre la base de B2 y el candidato no es el alcance del contrato: '
                        f'{sorted(set(derived.items()) ^ set(contract.items()))[:3]}')
    frozen, entries, blobs = dict(sorted(derived.items())), {}, {}
    for path, status in frozen.items():
        found, before = entry(objs, cand_tree, path), entry(objs, base_tree, path)
        if found is None or found[:2] != ('100644', 'blob') or objs.read(found[2])[0] != 'blob':
            problems.append(f'{path}: no es un blob regular 100644 en el candidato')
            continue
        if (status, before is None) not in (('A', True), ('M', False)) or before == found:
            problems.append(f'{path}: estado {status} frente a la base no confirmado por los objetos')
        entries[path], blobs[path] = found, objs.read(found[2])[1]
    surfaces = {}
    for folder in sorted({p.rsplit('/', 1)[0] for p, status in frozen.items() if status == 'A' and '/' in p}):
        found = listing(objs, cand_tree, folder)
        inside = {p[len(folder) + 1:] for p in frozen if p.startswith(folder + '/')}
        if entry(objs, base_tree, folder) is not None or found is None or set(found) != inside:
            problems.append(f'{folder}: no es una carpeta creada por B2 que contenga solo el conjunto congelado')
        surfaces[folder] = found or {}
    return {'problems': problems, 'frozen': frozen, 'entries': entries, 'blobs': blobs, 'surfaces': surfaces}


def derived_manifest(cand):
    return {
        'manifest_version': 1,
        'phase': 'F35-SBX-B',
        'increment': 'B2-FREEZE',
        'candidate_commit': CANDIDATE,
        'b2_base': B2_BASE,
        'prior_anchors': dict(PRIOR_ANCHORS),
        'frozen_set': [{'path': path, 'status_vs_base': status, 'type': cand['entries'][path][1],
                        'mode': cand['entries'][path][0], 'blob': cand['entries'][path][2],
                        'sha256': hashlib.sha256(cand['blobs'][path]).hexdigest(), 'bytes': len(cand['blobs'][path])}
                       for path, status in cand['frozen'].items() if path in cand['entries']],
        'reserved_surfaces': {folder: sorted(found) for folder, found in cand['surfaces'].items()},
        'freeze_layer': {folder: sorted(names) for folder, names in FREEZE_DIRS.items()},
    }


def canonical(manifest):
    return (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def manifest_problems(cand):
    want = derived_manifest(cand)
    data = disk_bytes(MANIFEST)
    if data is None:
        return ['manifiesto ausente, enlace o ilegible']
    if data == canonical(want):
        return []
    try:
        found = json.loads(data.decode('utf-8'))
    except ValueError:
        return ['el manifiesto no es JSON UTF-8 válido']
    if not isinstance(found, dict):
        return ['el manifiesto no es un objeto JSON']
    out = [f'«{key}» distinto de lo que se deriva del candidato' for key in sorted(set(want) | set(found))
           if key != 'frozen_set' and found.get(key) != want.get(key)]
    listed = found.get('frozen_set') if isinstance(found.get('frozen_set'), list) else []
    have = {e.get('path'): e for e in listed if isinstance(e, dict)}
    need = {e['path']: e for e in want['frozen_set']}
    for path in sorted(set(have) | set(need), key=str):
        a, b = have.get(path) or {}, need.get(path) or {}
        fields = sorted(str(k) for k in set(a) | set(b) if a.get(k) != b.get(k))
        if fields:
            out.append(f'frozen_set {path}: {", ".join(fields)} distinto de lo que se deriva del candidato')
    return out or ['el manifiesto tiene el contenido derivado, pero no su serialización canónica']


def seal_diff(objs, tree, cand):
    """Rutas congeladas y superficies reservadas de un árbol que difieren del candidato."""
    out = {p for p, want in cand['entries'].items() if entry(objs, tree, p) != want}
    for folder, want in cand['surfaces'].items():
        out.update(listing_diff(folder, listing(objs, tree, folder), want))
    return sorted(out)


# ---------------------------------------------------------------- índice y disco
def index_entries(paths):
    """{ruta: [(modo, oid, etapa)]} del índice para las rutas y carpetas pedidas."""
    out = {}
    for item in git('ls-files', '-s', '-z', '--', *paths).split(b'\x00'):
        if item:
            meta, _, path = item.partition(b'\t')
            mode, oid, stage = meta.decode('ascii').split()
            out.setdefault(path.decode('utf-8'), []).append((mode, oid, stage))
    return out


def index_problems(want, paths, label):
    """want: {ruta: (modo, tipo, oid)} esperado en etapa 0; cualquier otra entrada bajo paths es una diferencia."""
    expected = {p: [(e[0], e[2], '0')] for p, e in want.items()}
    found = index_entries(paths)
    diff = sorted(p for p in set(expected) | set(found) if expected.get(p) != found.get(p))
    return [f'índice distinto {label} (entrada ausente, extra, en conflicto o con otro modo, tipo o blob): '
            f'{diff[:5]}'] if diff else []


def linked(full):
    return os.path.islink(full) or bool(getattr(os.path, 'isjunction', lambda _: False)(full))


def disk_path(rel):
    """Ruta absoluta si ningún componente bajo la raíz es un enlace ni una unión de Windows; None en otro caso."""
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
    """Carpeta del disco frente a su listado esperado: contenido exacto (también ignorados, ocultos y __pycache__),
    sin enlaces ni objetos especiales, y cada archivo con su blob."""
    base = disk_path(folder)
    if base is None or not os.path.isdir(base):
        return [f'{folder}: ausente, enlace o no es un directorio']
    dirs = {'/'.join(rel.split('/')[:k]) for rel in want for k in range(1, rel.count('/') + 1)}
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
                if rel not in dirs:
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


def disk_problems(cand):
    inside = lambda p: any(p.startswith(folder + '/') for folder in cand['surfaces'])  # noqa: E731
    out = [x for p, e in cand['entries'].items() if not inside(p) for x in file_problems(p, e)]
    for folder, want in cand['surfaces'].items():
        out += disk_folder(folder, want)
    return out


# ---------------------------------------------------------------- nivel B: capa del freeze
def freeze_problems(objs, head, parents, after, info):
    cache = {}

    def layer(commit):
        if commit not in cache:
            tree = commit_parts(objs, commit)[0]
            cache[commit] = {folder: listing(objs, tree, folder) for folder in FREEZE_DIRS}
        return cache[commit]

    def complete(found):
        return all(found[folder] is not None and all(n in found[folder] for n in names)
                   for folder, names in FREEZE_DIRS.items())
    seals = sorted(c for c in after if complete(layer(c)) and not any(complete(layer(p)) for p in parents[c]))
    if len(seals) != 1:
        return ['ningún commit posterior al candidato completa la capa del freeze' if not seals else
                f'la capa del freeze se completa en más de un commit: {[c[:12] for c in seals]}']
    freeze = info['freeze'] = seals[0]
    want, out = layer(freeze), []
    for folder, names in FREEZE_DIRS.items():
        if set(want[folder]) != set(names) or any(e[:2] != ('100644', 'blob') for e in want[folder].values()):
            out.append(f'{folder}: en el commit de freeze no contiene exactamente sus archivos regulares 100644')
    later = descendants(parents, freeze)
    if head != freeze and head not in later:
        out.append(f'HEAD no desciende del commit de freeze {freeze[:12]}')
    for commit in sorted(later):
        diff = [x for folder in FREEZE_DIRS for x in listing_diff(folder, layer(commit)[folder], want[folder])]
        if diff:
            out.append(f'{commit[:12]}: capa del freeze distinta del commit de freeze (modificada, eliminada, '
                       f'renombrada, con otro modo o con archivos extra): {diff[:3]}')
    files = {f'{folder}/{rel}': e for folder, found in want.items() for rel, e in found.items()}
    out += index_problems(files, list(FREEZE_DIRS), 'del commit de freeze')
    for folder in FREEZE_DIRS:
        out += disk_folder(folder, want[folder])
    return out


# ---------------------------------------------------------------- entorno y dependencias
def ent_problems():
    out = []
    if not sys.flags.isolated:
        out.append('intérprete no aislado: se exige python -I')
    out += [f'{name} definida: el intérprete podría cargar código ajeno' for name in
            ('PYTHONPATH', 'PYTHONHOME', 'PYTHONUSERBASE') if os.environ.get(name)]
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
    viol = {rid: [] for rid in ORDER}
    info = {'head': None, 'after': None, 'freeze': None}

    def closed(rids, why):
        for rid in rids:
            viol[rid].append(f'no evaluable: {why} (falla cerrado)')

    def check(rid, fn, *args):
        try:
            viol[rid] += fn(*args)
        except ERRORS as e:
            closed((rid,), f'{e.__class__.__name__}: {e}')

    check('DEP', dep_problems)
    try:
        problems, head = ent_problems()
    except ERRORS as e:
        closed([r for r in ORDER if r != 'DEP'], f'repositorio Git ({e.__class__.__name__}: {e})')
        return viol, info
    viol['ENT'] += problems
    info['head'] = head
    check('FLG', flag_problems)
    objs = None
    try:
        objs = Objects()
        parents = cand = after = None
        try:
            parents = ancestry(objs, head)
        except ERRORS as e:
            closed(('CAN', 'HIS', 'FRZ'), f'historia desde HEAD ({e})')
        try:
            cand = candidate_state(objs)
            viol['CAN'] += cand['problems']
        except ERRORS as e:
            closed(('CAN', 'MAN', 'HIS', 'ARB', 'IDX', 'DSK'), f'candidato ({e.__class__.__name__}: {e})')
        if parents is not None:
            if CANDIDATE in parents:
                after = descendants(parents, CANDIDATE)
                info['after'] = len(after)
            else:
                viol['CAN'].append('el candidato no es ancestro de HEAD: la historia no corresponde')
                closed(('HIS', 'FRZ'), 'no hay historia posterior al candidato')
        if cand is not None:
            check('MAN', manifest_problems, cand)
            check('ARB', lambda: [f'árbol de HEAD distinto del candidato: {d[:5]}' for d in
                                  [seal_diff(objs, commit_parts(objs, head)[0], cand)] if d])
            files = dict(cand['entries'])
            files.update({f'{folder}/{rel}': e for folder, found in cand['surfaces'].items() for rel, e in found.items()})
            check('IDX', index_problems, files, list(cand['entries']) + list(cand['surfaces']), 'del candidato')
            check('DSK', disk_problems, cand)
            if after is not None:
                check('HIS', lambda: [f'{c[:12]}: rutas congeladas o superficies reservadas distintas del candidato '
                                      f'(modificadas, eliminadas, renombradas, con otro modo o con archivos extra): '
                                      f'{d[:3]}' for c in sorted(after)
                                      for d in [seal_diff(objs, commit_parts(objs, c)[0], cand)] if d])
        if after is not None:
            check('FRZ', freeze_problems, objs, head, parents, after, info)
    except ERRORS as e:
        closed(('CAN', 'MAN', 'HIS', 'ARB', 'IDX', 'DSK', 'FRZ'), f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        if objs is not None:
            objs.close()
    return viol, info


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        viol, info = evaluate()
    except Exception as e:      # cualquier fallo inesperado: todas las reglas fallan cerradas
        viol = {rid: [f'evaluación interrumpida ({e.__class__.__name__}): falla cerrado'] for rid in ORDER}
        info = {'head': None, 'after': None, 'freeze': None}
    after = 'no verificable' if info['after'] is None else info['after']
    print(f'INFO candidato {CANDIDATE}; HEAD {info["head"] or "no verificable"}; commits posteriores al candidato: '
          f'{after}; commit de freeze derivado: {info["freeze"] or "ninguno"}')
    fallas = [rid for rid in ORDER if viol[rid]]
    for rid in fallas:
        print(f'FALLA {rid}: {len(viol[rid])} violaciones — {viol[rid][:3]}')
    print(f'validate_f35sbxb2_freeze: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
