"""F35-SBX-B — gate sucesor vigente tras B2-FREEZE (validate_f35sbxb2_sucesor.py).

Uso:  python -I docs/academico/tools/f35sbxb2_sucesor/validate_f35sbxb2_sucesor.py   (sin -I, se relanza aislado)

Corrige AF-M01. Sobre HEAD no basta el resultado histórico del gate de B2 (119/0 sobre el candidato) más la integridad
del freeze (10/0). Por B0 (§2.2, principios B y C) y DH-B13 (puntos 6 y 7), la falla de alcance del gate congelado
(clase A) no se ignora: obliga a ejecutar la evaluación sucesora completa sobre HEAD. Este gate la compone sin modificar
ningún gate congelado. Cada subgate se ejecuta intacto, como proceso propio, desde bytes verificados contra su ancla y
con las variables GIT_* descartadas:

  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; Git sobre el repositorio de este archivo, con
       historia completa y sin injertos ni objetos de reemplazo.
  ANC  anclas registradas: el candidato 2472fd6 y el freeze 9961d2d son commits íntegros; el freeze desciende del
       candidato y HEAD del freeze.
  HIS  gate histórico: el gate de B2, con los bytes del candidato, anclado sobre 2472fd6 en un clon temporal sin remoto:
       código 0, ninguna falla y la transición de gobierno derivada igual a la registrada.
  CON  freeze: la capa del freeze tiene en HEAD, el índice y el disco los blobs del freeze registrado. Su validador,
       verificado antes de ejecutarlo, termina con código 0 y sin fallas, y deriva este candidato y exactamente este
       freeze.
  MAT  evaluación material vigente: el gate de B2, verificado contra el candidato, se ejecuta sobre HEAD. Toda
       comprobación pasa salvo SCP, y SCP solo falla por clase A: cada ruta enumerada del sucesor en el árbol de HEAD,
       el árbol de trabajo y el índice, y nada más. Su total de comprobaciones es el de la ejecución histórica.
  ALC  alcance exacto del sucesor: frente al candidato, HEAD, el índice y el árbol de trabajo añaden exactamente las
       rutas enumeradas, no hay archivos sin seguimiento y las rutas de esta capa están confirmadas y sin extras.
  DEP  esta capa solo importa la biblioteca estándar autorizada y no ejecuta código dinámico.

El repositorio solo se lee: lo único que se escribe es un clon temporal fuera de él, que se borra al terminar. Todo error,
salida incompleta o inesperada o estado no evaluable falla cerrado. Cada objeto Git que se lee se verifica recalculando
su identificador con el formato de objetos de Git.
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
import re  # noqa: E402
import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'      # B2_CANDIDATE: B2 reauditada y aprobada para freeze
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'         # B2-FREEZE auditado (AF-M01); registrado tras existir
B2_TRANSITION = '12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa'  # transición de gobierno de B2, registrada por B2
B2_BRANCH = 'feature/f35-sbx-b2-ephemeral-store'
B2_GATE = 'docs/academico/tools/f35sbxb2/validate_f35sbxb2.py'
FREEZE_VALIDATOR = 'docs/academico/tools/f35sbxb2_freeze/validate_f35sbxb2_freeze.py'
FREEZE_DIRS = {'docs/academico/evidencia-sbx-b2-freeze': ('F35SBXB_B2_Freeze.md',),
               'docs/academico/tools/f35sbxb2_freeze': ('b2_freeze_manifest.json', 'test_f35sbxb2_freeze.py',
                                                        'validate_f35sbxb2_freeze.py')}
SUCESOR_DIRS = {'docs/academico/evidencia-sbx-b2-sucesor': ('F35SBXB_B2_Sucesor.md',),
                'docs/academico/tools/f35sbxb2_sucesor': ('test_f35sbxb2_sucesor.py', 'validate_f35sbxb2_sucesor.py')}
# Alcance exacto del sucesor frente al candidato (principio D de B0): las rutas de la capa del freeze y las de esta capa.
SUCCESSOR_FILES = tuple(sorted(f'{folder}/{name}' for group in (FREEZE_DIRS, SUCESOR_DIRS)
                               for folder, names in group.items() for name in names))
VALIDATOR = 'docs/academico/tools/f35sbxb2_sucesor/validate_f35sbxb2_sucesor.py'
TESTS = 'docs/academico/tools/f35sbxb2_sucesor/test_f35sbxb2_sucesor.py'
DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'hashlib', 'os', 're', 'subprocess', 'sys'}),
               TESTS: frozenset({'hashlib', 'json', 'os', 'subprocess', 'sys'})}
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
ORDER = ('ENT', 'ANC', 'HIS', 'CON', 'MAT', 'ALC', 'DEP')
PLANES = ('HEAD', 'árbol', 'índice')          # planos de SCP del gate de B2
TIMEOUT = 3600
# Git y subgates sin variables heredadas (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE...): el entorno no puede redirigirlos.
GIT_ENV = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
GIT = ('git', '--no-replace-objects', '--literal-pathspecs')
# Salida de los subgates: solo su línea INFO, líneas FALLA y su resumen final.
B2_SUMMARY = re.compile(r'validate_f35sbxb2: (\d+) comprobaciones correctas, (\d+) fallas')
B2_INFO = re.compile(r'INFO transición de gobierno de B2 derivada: ([0-9a-f]{40}); registrada: ([0-9a-f]{40})')
FRZ_SUMMARY = re.compile(r'validate_f35sbxb2_freeze: (\d+) comprobaciones correctas, (\d+) fallas')
FRZ_INFO = re.compile(r'INFO candidato ([0-9a-f]{40}); HEAD ([0-9a-f]{40}); commits posteriores al candidato: (\d+); '
                      r'commit de freeze derivado: ([0-9a-f]{40})')
SCP_LINE = re.compile(r'FALLA SCP: (\d+) violaciones — (.*)')
SCP_ITEM = re.compile(r"'(HEAD|árbol|índice): cambio fuera del delta autorizado de B2 o con estado inesperado: A ([^']+)'")
RULE_ID = re.compile(r'[A-Z][A-Z0-9]{2}')
CASE_ID = re.compile(r'[PF]\d{2}')


class GitError(Exception):
    pass


ERRORS = (GitError, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError, subprocess.TimeoutExpired)


def git(*args, cwd=None, env=None):
    try:
        p = subprocess.run([*GIT, *args], cwd=cwd or ROOT, env=env or GIT_ENV, capture_output=True, timeout=TIMEOUT)
    except OSError as e:
        raise GitError(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(args[:2])} → {p.returncode}')
    return p.stdout


def is_oid(value):
    return isinstance(value, str) and len(value) == 40 and all(c in '0123456789abcdef' for c in value)


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


# ---------------------------------------------------------------- objetos Git verificados (técnica del freeze)
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


def ancestry(objs, head):
    """Todos los ancestros de head, incluido, desde objetos verificados."""
    seen, stack = set(), [head]
    while stack:
        commit = stack.pop()
        if commit not in seen:
            seen.add(commit)
            stack.extend(p for p in commit_parts(objs, commit)[1] if p not in seen)
    return seen


def layer_entries(objs, tree, dirs):
    """{ruta: (modo, tipo, oid)} de unas carpetas con su contenido exacto en un árbol, o None si no lo tienen."""
    out = {}
    for folder, names in dirs.items():
        found = listing(objs, tree, folder)
        if found is None or set(found) != set(names) or any(e[:2] != ('100644', 'blob') for e in found.values()):
            return None
        out.update({f'{folder}/{rel}': e for rel, e in found.items()})
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
    return [f'índice distinto {label}: {diff[:5]}'] if diff else []


def linked(full):
    return os.path.islink(full) or bool(getattr(os.path, 'isjunction', lambda _: False)(full))


def disk_path(rel, root=None):
    parts = rel.split('/')
    if any(linked(os.path.join(root or ROOT, *parts[:k])) for k in range(1, len(parts) + 1)):
        return None
    return os.path.join(root or ROOT, *parts)


def disk_bytes(rel, root=None):
    full = disk_path(rel, root)
    if full is None or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def disk_folder(folder, want):
    """Carpeta del disco con exactamente los archivos esperados (también ignorados y ocultos), regulares, sin enlaces
    y con sus blobs."""
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
        data = disk_bytes(f'{folder}/{rel}')
        if data is None or blob_id(data) != want[rel][2]:
            out.append(f'{folder}/{rel}: bytes del disco distintos del blob esperado')
    return out


def by_folder(files, folder):
    return {p[len(folder) + 1:]: e for p, e in files.items() if p.startswith(folder + '/')}


# ---------------------------------------------------------------- ejecución estricta de los subgates congelados
def parse_run(code, stdout, stderr, summary_rx, info_rx):
    """Salida de un subgate: (correctas, fallas, ids en falla, líneas FALLA, INFO). ValueError si no es la esperada."""
    if stderr.strip():
        raise ValueError(f'salida de error inesperada: «{stderr.decode("utf-8", "replace").strip()[:120]}»')
    lines = [x for x in stdout.decode('utf-8').splitlines() if x.strip()]
    if not lines or not summary_rx.fullmatch(lines[-1]):
        raise ValueError('sin su resumen final: ejecución incompleta')
    info = [m for m in (info_rx.fullmatch(x) for x in lines[:-1]) if m]
    fallas = [x for x in lines[:-1] if x.startswith('FALLA ')]
    if len(info) != 1 or len(info) + len(fallas) != len(lines) - 1:
        raise ValueError('líneas no reconocidas o sin su línea INFO')
    ok, ko = (int(x) for x in summary_rx.fullmatch(lines[-1]).groups())
    if ko != len(fallas) or code != (1 if ko else 0):
        raise ValueError(f'resumen, líneas FALLA y código de salida incoherentes (código {code})')
    return ok, ko, [x.split()[1].rstrip(':') for x in fallas], fallas, info[0]


def verified_script(rel, expected, root=None):
    data = disk_bytes(rel, root)
    if data is None or blob_id(data) != expected:
        raise ValueError(f'{rel} distinto de su blob {expected[:12]}: no se ejecuta')
    return disk_path(rel, root)


def run_script(rel, expected, cwd):
    """Ejecuta un subgate con bytes verificados antes y después, con python -I y sin variables GIT_*."""
    path = verified_script(rel, expected, cwd)
    p = subprocess.run([sys.executable, '-I', '-B', path], cwd=cwd, env=GIT_ENV, capture_output=True, timeout=TIMEOUT)
    verified_script(rel, expected, cwd)
    return p.returncode, p.stdout, p.stderr


_COUNTER = [0]


def make_temp(label):
    base = os.path.abspath(os.environ.get('TEMP') or os.environ.get('TMP') or os.environ.get('TMPDIR') or '/tmp')
    if (os.path.normcase(base) + os.sep).startswith(_REPO + os.sep) or not os.path.isdir(base):
        raise GitError('directorio temporal no disponible fuera del repositorio')
    _COUNTER[0] += 1
    path = os.path.join(base, f'f35sbxb2-sucesor-{label}-{os.getpid()}-{_COUNTER[0]}')
    os.mkdir(path)
    return path


def remove_tree(path):
    if not os.path.lexists(path):
        return
    for d, dirs, files in os.walk(path, topdown=False):
        for name in files:
            full = os.path.join(d, name)
            if not os.path.islink(full):
                os.chmod(full, 0o600)
            os.remove(full)
        for name in dirs:
            full = os.path.join(d, name)
            if os.path.islink(full) and os.name != 'nt':
                os.remove(full)
            else:
                os.rmdir(full)
    os.rmdir(path)


class Historic:
    """HIS: el gate de B2 anclado sobre el candidato, en un clon temporal sin remoto, en paralelo con el resto."""

    def __init__(self, gate_blob):
        self.tmp, self.proc, self.files, self.gate_blob = make_temp('historico'), None, [], gate_blob
        try:
            config = os.path.join(self.tmp, 'gitconfig')
            with open(config, 'wb'):
                pass
            env = dict(GIT_ENV, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=config)
            self.repo = os.path.join(self.tmp, 'repo')
            git('clone', '-q', '--shared', '--no-checkout', '-c', 'core.autocrlf=false', ROOT, self.repo,
                cwd=self.tmp, env=env)
            git('remote', 'remove', 'origin', cwd=self.repo, env=env)
            git('checkout', '-q', '-B', B2_BRANCH, CANDIDATE, cwd=self.repo, env=env)
            if git('rev-parse', '--verify', 'HEAD^{commit}', cwd=self.repo).decode('ascii').strip() != CANDIDATE:
                raise GitError('el clon temporal no está en el candidato')
            path = verified_script(B2_GATE, gate_blob, self.repo)
            self.files = [open(os.path.join(self.tmp, name), 'wb') for name in ('salida', 'errores')]
            self.proc = subprocess.Popen([sys.executable, '-I', '-B', path], cwd=self.repo, env=GIT_ENV,
                                         stdout=self.files[0], stderr=self.files[1])
        except BaseException:
            self.close()
            raise

    def result(self):
        try:
            code = self.proc.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
            raise
        for f in self.files:
            f.close()
        verified_script(B2_GATE, self.gate_blob, self.repo)
        with open(os.path.join(self.tmp, 'salida'), 'rb') as f:
            out = f.read()
        with open(os.path.join(self.tmp, 'errores'), 'rb') as f:
            err = f.read()
        return code, out, err

    def close(self):
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()
            self.proc.wait()
        for f in self.files:
            f.close()
        remove_tree(self.tmp)


# ---------------------------------------------------------------- reglas
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


def anc_problems(objs, head):
    commit_parts(objs, CANDIDATE)
    commit_parts(objs, FREEZE)
    out = []
    if FREEZE not in ancestry(objs, head):
        out.append(f'el freeze registrado {FREEZE[:12]} no es HEAD ni ancestro de HEAD')
    if CANDIDATE == FREEZE or CANDIDATE not in ancestry(objs, FREEZE):
        out.append(f'el freeze registrado {FREEZE[:12]} no desciende del candidato')
    return out


def his_problems(code, out, err):
    ok, ko, ids, _, info = parse_run(code, out, err, B2_SUMMARY, B2_INFO)
    problems = [] if not ids else [f'el gate de B2 anclado sobre el candidato falla: {ids[:5]}']
    if info.groups() != (B2_TRANSITION, B2_TRANSITION):
        problems.append(f'transición derivada o registrada distinta de {B2_TRANSITION[:12]}')
    line = (f'INFO HIS: gate de B2 anclado sobre {CANDIDATE}: código {code}; {ok} correctas, {ko} fallas; transición '
            f'derivada {info.group(1)}, registrada {info.group(2)}')
    return problems, line, ok + ko


def con_problems(objs, head):
    want = layer_entries(objs, commit_parts(objs, FREEZE)[0], FREEZE_DIRS)
    if want is None:
        raise GitError(f'el freeze registrado {FREEZE[:12]} no contiene exactamente su capa')
    out = []
    here = layer_entries(objs, commit_parts(objs, head)[0], FREEZE_DIRS)
    if here != want:
        out.append(f'árbol de HEAD: capa del freeze distinta de {FREEZE[:12]}')
    out += index_problems(want, list(FREEZE_DIRS), f'del freeze {FREEZE[:12]} en la capa del freeze')
    for folder in FREEZE_DIRS:
        out += disk_folder(folder, by_folder(want, folder))
    try:
        code, stdout, stderr = run_script(FREEZE_VALIDATOR, want[FREEZE_VALIDATOR][2], ROOT)
    except ValueError as e:
        return out + [str(e)], f'INFO CON: validador del freeze no ejecutado: {e}'
    ok, ko, ids, _, info = parse_run(code, stdout, stderr, FRZ_SUMMARY, FRZ_INFO)
    if ids:
        out.append(f'el validador del freeze falla: {ids}')
    if info.group(1) != CANDIDATE or info.group(2) != head:
        out.append('el validador del freeze informa otro candidato u otro HEAD')
    if info.group(4) != FREEZE:
        out.append(f'freeze derivado {info.group(4)[:12]} distinto del registrado {FREEZE[:12]}: ancla no autenticada')
    line = (f'INFO CON: validador del freeze: código {code}; {ok} correctas, {ko} fallas; candidato {info.group(1)}; '
            f'freeze derivado {info.group(4)} (registrado {FREEZE})')
    return out, line


def mat_problems(gate_blob):
    try:
        code, stdout, stderr = run_script(B2_GATE, gate_blob, ROOT)
    except ValueError as e:
        return [str(e)], f'INFO MAT: gate de B2 sobre HEAD no ejecutado: {e}', None
    ok, ko, ids, fallas, info = parse_run(code, stdout, stderr, B2_SUMMARY, B2_INFO)
    rules = sorted(i for i in ids if RULE_ID.fullmatch(i) and not CASE_ID.fullmatch(i))
    cases = len(ids) - len(rules)
    expected = len(PLANES) * len(SUCCESSOR_FILES)
    scp = [m for m in (SCP_LINE.fullmatch(x) for x in fallas) if m]
    count = int(scp[0].group(1)) if scp else 0
    out = []
    if info.groups() != (B2_TRANSITION, B2_TRANSITION):
        out.append(f'transición derivada o registrada distinta de {B2_TRANSITION[:12]}')
    material = [i for i in ids if i != 'SCP']
    if material:
        out.append(f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas {[r for r in rules if r != "SCP"]}'
                   f', {cases} casos')
    if 'SCP' not in ids:
        out.append('SCP no falla: falta la evolución autorizada del sucesor')
    else:
        shown = SCP_ITEM.findall(scp[0].group(2)) if scp else []
        if count != expected or not shown or any(path not in SUCCESSOR_FILES for _, path in shown):
            out.append(f'SCP con violaciones ajenas al alcance del sucesor: {count} (esperadas {expected})')
    line = (f'INFO MAT: gate de B2 sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas en falla: '
            f'{", ".join(rules) or "ninguna"}; casos en falla: {cases}; SCP: {count} violaciones (alcance del sucesor: '
            f'{expected})')
    return out, line, ok + ko


def name_status(raw):
    parts = raw.split(b'\x00')
    return {parts[i + 1].decode('utf-8'): parts[i].decode('ascii') for i in range(0, len(parts) - 1, 2) if parts[i]}


def alc_problems(objs, head):
    want, out = {p: 'A' for p in SUCCESSOR_FILES}, []
    for plane, args in (('HEAD', ('diff', '--name-status', '--no-renames', '-z', CANDIDATE, 'HEAD')),
                        ('árbol', ('diff', '--name-status', '--no-renames', '-z', CANDIDATE)),
                        ('índice', ('diff', '--cached', '--name-status', '--no-renames', '-z', CANDIDATE))):
        found = name_status(git(*args))
        if found != want:
            out.append(f'{plane}: alcance distinto del enumerado para el sucesor: '
                       f'{sorted(set(found.items()) ^ set(want.items()))[:3]}')
    untracked = [x for x in git('ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').split('\x00') if x]
    if untracked:
        out.append(f'archivos sin seguimiento fuera del alcance: {untracked[:5]}')
    own = layer_entries(objs, commit_parts(objs, head)[0], SUCESOR_DIRS)
    if own is None:
        return out + ['las carpetas de esta capa no tienen en HEAD exactamente sus archivos regulares']
    out += index_problems(own, list(SUCESOR_DIRS), 'de HEAD en esta capa')
    for folder in SUCESOR_DIRS:
        out += disk_folder(folder, by_folder(own, folder))
    return out


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


# ---------------------------------------------------------------- composición con fallo cerrado
def evaluate():
    viol, info = {rid: [] for rid in ORDER}, []

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
    info.append(f'INFO ANC: candidato {CANDIDATE}; freeze registrado {FREEZE}; HEAD {head}')
    objs, historic = None, None
    try:
        objs = Objects()
        check('ANC', anc_problems, objs, head)
        gate_blob = None
        try:
            gate = entry(objs, commit_parts(objs, CANDIDATE)[0], B2_GATE)
            if gate is None or gate[:2] != ('100644', 'blob'):
                raise GitError('el gate de B2 no es un blob regular en el candidato')
            gate_blob = gate[2]
        except ERRORS as e:
            closed(('HIS', 'MAT'), f'gate de B2 en el candidato ({e.__class__.__name__}: {e})')
        if gate_blob is not None:
            try:
                historic = Historic(gate_blob)
            except ERRORS as e:
                closed(('HIS',), f'clon temporal del candidato ({e.__class__.__name__}: {e})')
                info.append(f'INFO HIS: gate de B2 anclado no ejecutado: {e}')
        con = check('CON', con_problems, objs, head)
        if con:
            info.append(con[0])
        mat = check('MAT', mat_problems, gate_blob) if gate_blob is not None else None
        if mat:
            info.append(mat[0])
        check('ALC', alc_problems, objs, head)
        if historic is not None:
            his = check('HIS', lambda: his_problems(*historic.result()))
            if his:
                info.append(his[0])
                if mat and mat[1] is not None and his[1] != mat[1]:
                    viol['MAT'].append(f'total de comprobaciones sobre HEAD ({mat[1]}) distinto del histórico ({his[1]})')
    except ERRORS as e:
        closed(('ANC', 'HIS', 'CON', 'MAT', 'ALC'), f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        if historic is not None:
            try:
                historic.close()
            except OSError as e:
                viol['HIS'].append(f'limpieza incompleta del clon temporal ({e.__class__.__name__}): falla cerrado')
        if objs is not None:
            objs.close()
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
    print(f'validate_f35sbxb2_sucesor: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
