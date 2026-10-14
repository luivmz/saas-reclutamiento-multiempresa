"""F35-SBX-B — batería del cierre de la capa sucesora, B2-SUCCESSOR-FREEZE (test_f35sbxb2_sucesor_freeze.py).

Uso:  python -I docs/academico/tools/f35sbxb2_sucesor_freeze/test_f35sbxb2_sucesor_freeze.py   (sin -I, se relanza)

Fija en RED el cierre que resuelve AF-L02, en dos niveles:

  Nivel A  la capa sucesora auditada en 9d6fb15: bytes, modos, tipos e historia, en HEAD, el índice y el disco.
  Nivel B  la capa del cierre, desde el commit que la completa, que se deriva de Git y se registra fuera.

La evaluación material vigente (VIG) ejecuta el gate sucesor aprobado sobre HEAD y solo acepta la evolución de alcance
de clase A que introduce el cierre.

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en
SF13, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta allí el
validador del cierre con python -I. Pasa si fallan exactamente las reglas esperadas y, en los casos materiales, si la
línea INFO de VIG nombra las reglas del gate de B2 que detectan el incumplimiento. Las rutas del sucesor se derivan de
Git. El repositorio original no se modifica.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación, como los gates: python -I, relanzado con os.spawnv.
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

import hashlib  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'   # B2_CANDIDATE
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'      # B2-FREEZE
SUCCESSOR = '9d6fb157bb818574217e3675da1849e8d1010962'   # capa sucesora auditada (AF-M01 resuelto)
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'      # develop al crear la rama de B2
B1_MAIN = '3fdfdcecdec47b08d99e96968dd915e0e1b9010b'      # main tras integrar B1, con el mismo árbol que 72e86c5
B2_BRANCH = 'feature/f35-sbx-b2-ephemeral-store'
CLOSURE_TOOLS = 'docs/academico/tools/f35sbxb2_sucesor_freeze'
CLOSURE = CLOSURE_TOOLS + '/validate_f35sbxb2_sucesor_freeze.py'
CLOSURE_MANIFEST = CLOSURE_TOOLS + '/b2_sucesor_freeze_manifest.json'
CLOSURE_FILES = (CLOSURE, CLOSURE_MANIFEST, CLOSURE_TOOLS + '/test_f35sbxb2_sucesor_freeze.py',
                 'docs/academico/evidencia-sbx-b2-sucesor-freeze/F35SBXB_B2_Sucesor_Freeze.md')
EVIDENCE = 'docs/academico/datos-sinteticos/dataset/evidence.csv'
F34_MANIFEST = 'docs/academico/datos-sinteticos/dataset/manifest.json'
RULES = frozenset({'ENT', 'ANC', 'MAN', 'HIS', 'ARB', 'IDX', 'FLG', 'DSK', 'VIG', 'ALC', 'FRZ', 'DEP'})
SUMMARY = 'validate_f35sbxb2_sucesor_freeze: '
STAMP = '2026-10-14T00:00:00+00:00'
RUNS = [0]


class Failure(Exception):
    pass


# ---------------------------------------------------------------- temporales y Git aislado
_COUNTER = [0]


def make_temp(label):
    base = os.path.abspath(os.environ.get('TEMP') or os.environ.get('TMP') or os.environ.get('TMPDIR') or '/tmp')
    if (os.path.normcase(base) + os.sep).startswith(_REPO + os.sep) or not os.path.isdir(base):
        raise Failure('directorio temporal no disponible fuera del repositorio')
    _COUNTER[0] += 1
    path = os.path.join(base, f'f35sbxb2scf-{label}-{os.getpid()}-{_COUNTER[0]}')
    os.mkdir(path)
    return path


def remove_tree(path):
    """Borra un temporal: los objetos de Git son de solo lectura en Windows y los enlaces se borran sin seguirlos."""
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


def git_env(config):
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': config,
                'GIT_AUTHOR_NAME': 'fixture-b2scf', 'GIT_AUTHOR_EMAIL': 'fixture-b2scf',
                'GIT_COMMITTER_NAME': 'fixture-b2scf', 'GIT_COMMITTER_EMAIL': 'fixture-b2scf',
                'GIT_AUTHOR_DATE': STAMP, 'GIT_COMMITTER_DATE': STAMP})
    return env


def run_git(args, cwd, env, data=None):
    try:
        p = subprocess.run(['git', *args], cwd=cwd, env=env, input=data, capture_output=True)
    except OSError as e:
        raise Failure(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise Failure(f'git {" ".join(args[:2])} → {p.returncode}: {p.stderr.decode("utf-8", "replace").strip()[:160]}')
    return p.stdout


def file_url(path):
    path = os.path.abspath(path).replace(os.sep, '/')
    return 'file://' + ('' if path.startswith('/') else '/') + path


class Fixture:
    """Clon desechable de la base con la rama de B2 en HEAD. Nada de lo que se hace aquí llega al repositorio. Con
    depth, el clon es superficial (copia de objetos por file://); si no, comparte los objetos de la base."""

    def __init__(self, base, label, env, head, depth=None):
        self.env, self.base, self.head, self.extra = env, base, head, []
        self.root = make_temp(label)
        try:
            self._clone(self.root, depth)
        except BaseException:
            remove_tree(self.root)
            raise

    def _clone(self, root, depth=None):
        source = ['--shared', self.base] if depth is None else ['--depth', str(depth), file_url(self.base)]
        run_git(['clone', '-q', '--no-checkout', '-c', 'core.autocrlf=false', *source, root], os.path.dirname(root),
                self.env)
        run_git(['remote', 'remove', 'origin'], root, self.env)
        run_git(['checkout', '-q', '-B', B2_BRANCH, self.head], root, self.env)

    def sibling(self, label):
        """Otro clon limpio del mismo HEAD, que se borra junto con el caso."""
        root = make_temp(label)
        self.extra.append(root)
        self._clone(root)
        return root

    def cleanup(self):
        for path in [self.root] + self.extra:
            remove_tree(path)

    def git(self, *args, data=None):
        return run_git(list(args), self.root, self.env, data)

    def text(self, *args):
        return self.git(*args).decode('utf-8').strip()

    def path(self, rel):
        return os.path.join(self.root, *rel.split('/'))

    def read(self, rel):
        with open(self.path(rel), 'rb') as f:
            return f.read()

    def write(self, rel, data):
        full = self.path(rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as f:
            f.write(data)

    def commit(self, message, *paths):
        if paths:
            self.git('add', '--', *paths)
        self.git('commit', '-q', '-m', message)

    def hidden(self):
        """git status no muestra ningún cambio: el escenario es invisible para él."""
        return self.git('status', '--porcelain').strip() == b''

    def validate(self, extra_env=None):
        """(reglas en falla, líneas INFO, resumen) del validador del cierre, o (None, {}, motivo) si no terminó con un
        resumen coherente."""
        RUNS[0] += 1
        try:
            p = subprocess.run([sys.executable, '-I', '-B', self.path(CLOSURE)], cwd=self.root,
                               env=dict(self.env, **(extra_env or {})), capture_output=True, timeout=3600)
        except (OSError, subprocess.TimeoutExpired) as e:
            return None, {}, f'el validador del cierre no se pudo ejecutar ({e.__class__.__name__})'
        lines = p.stdout.decode('utf-8', 'replace').splitlines()
        summary = [x for x in lines if x.startswith(SUMMARY)]
        failing = {x.split()[1].rstrip(':') for x in lines if x.startswith('FALLA ') and len(x.split()) > 1}
        info = {x.split()[1].rstrip(':'): x for x in lines if x.startswith('INFO ') and len(x.split()) > 1}
        if len(summary) != 1:
            tail = ((p.stdout + p.stderr).decode('utf-8', 'replace').strip().splitlines() or [''])[-1]
            return None, {}, f'el validador del cierre no terminó con su resumen (código {p.returncode}): «{tail[:200]}»'
        if (p.returncode == 0) != (not failing) or not failing <= RULES:
            return None, {}, f'salida incoherente (código {p.returncode}; reglas en falla {sorted(failing)})'
        return failing, info, summary[0]


def b2_rules(info):
    """Reglas del gate de B2 en falla que la línea INFO de VIG nombra."""
    line = info.get('VIG', '')
    marker = 'reglas del gate de B2 en falla: '
    if marker not in line:
        return None
    named = line.split(marker, 1)[1].split(';', 1)[0]
    return {x.strip() for x in named.split(',') if x.strip() and x.strip() != 'ninguna'}


def anchor(info):
    line = info.get('FRZ', '')
    marker = 'commit que completa el cierre: '
    return line.split(marker, 1)[1].split(';', 1)[0].strip() if marker in line else None


def probe(fx, expected, label='', mat=None, scenario=True, why='', env=None, check=None):
    """Una ejecución del validador del cierre frente a las reglas que deben fallar (vacío = PASS). mat: reglas del gate
    de B2 que VIG debe nombrar; check: comprobación adicional sobre las líneas INFO, que devuelve un motivo o None."""
    if not scenario:
        return label, expected, None, f'escenario no reproducido: {why}'
    observed, info, detail = fx.validate(env)
    if observed is None:
        return label, expected, None, detail
    if mat is not None and observed == expected:
        named = b2_rules(info)
        if named is None or not mat <= named:
            return label, expected, None, f'VIG no nombra {sorted(mat)} (nombra {sorted(named or [])})'
    if check is not None and observed == expected:
        problem = check(info)
        if problem:
            return label, expected, None, problem
    return label, expected, observed, detail


def not_run(rule):
    return lambda info: None if 'no ejecutado' in info.get(rule, '') else f'{rule} no declara que el gate alterado quedó sin ejecutar'


def _manifest_hash(fx, new_hash=None):
    """Sustituye el SHA-256 de evidence.csv en el manifiesto F34 (una sola aparición)."""
    data = fx.read(F34_MANIFEST)
    old = json.loads(data.decode('utf-8'))['files']['evidence.csv']['sha256']
    new = new_hash or old[:-1] + ('1' if old[-1] != '1' else '2')
    if data.count(old.encode('ascii')) != 1:
        raise Failure('el SHA-256 de evidence.csv no aparece exactamente una vez en el manifiesto F34')
    fx.write(F34_MANIFEST, data.replace(old.encode('ascii'), new.encode('ascii'), 1))


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


# ---------------------------------------------------------------- nivel A: la capa sucesora auditada
def sf01(fx, c):
    return [probe(fx, set(), check=lambda info: None if anchor(info) == c['completion'] else
                  f'ancla derivada {anchor(info)} distinta del commit que completa el cierre {c["completion"]}')]


def sf02(fx, c):
    fx.write(c['validator'], fx.read(c['validator']) + b'\n# alterado\n')
    fx.commit('altera el gate sucesor', c['validator'])
    return [probe(fx, {'HIS', 'ARB', 'IDX', 'DSK', 'VIG', 'ALC'}, check=not_run('VIG'))]


def sf03(fx, c):
    fx.write(c['tests'], fx.read(c['tests']) + b'\n# alterado\n')
    fx.commit('altera la batería del sucesor', c['tests'])
    return [probe(fx, {'HIS', 'ARB', 'IDX', 'DSK', 'ALC'})]


def sf04(fx, c):
    fx.write(c['doc'], fx.read(c['doc']) + b'\nalterado\n')
    fx.commit('altera el documento del sucesor', c['doc'])
    return [probe(fx, {'HIS', 'ARB', 'IDX', 'DSK', 'ALC'})]


def sf05(fx, c):
    original = fx.read(c['tests'])
    fx.write(c['tests'], original + b'\n# alterado\n')
    fx.commit('modifica la batería del sucesor', c['tests'])
    fx.write(c['tests'], original)
    fx.commit('la restaura', c['tests'])
    return [probe(fx, {'HIS'})]


def sf06_rename(fx, c):
    moved = c['tests'].rsplit('/', 1)[0] + '/renombrado.py'
    fx.git('mv', c['tests'], moved)
    fx.commit('renombra la batería del sucesor')
    fx.git('mv', moved, c['tests'])
    fx.commit('restaura su nombre')
    return [probe(fx, {'HIS'}, label='renombrar')]


def sf06_delete(fx, c):
    fx.git('rm', '-q', '--', c['doc'])
    fx.commit('elimina el documento del sucesor')
    fx.git('checkout', '-q', 'HEAD~1', '--', c['doc'])
    fx.commit('lo restaura')
    return [probe(fx, {'HIS'}, label='eliminar')]


def sf06_mode(fx, c):
    fx.git('update-index', '--chmod=+x', '--', c['tests'])
    fx.commit('modo 100755')
    fx.git('update-index', '--chmod=-x', '--', c['tests'])
    fx.commit('restaura el modo 100644')
    return [probe(fx, {'HIS'}, label='modo')]


def sf06_type(fx, c):
    target = fx.git('hash-object', '-w', '--stdin', data=b'F35SBXB_B2_Sucesor_real.md').decode('ascii').strip()
    fx.git('update-index', '--cacheinfo', f'120000,{target},{c["doc"]}')
    fx.commit('cambia el documento del sucesor por un enlace simbólico')
    fx.git('checkout', '-q', 'HEAD~1', '--', c['doc'])
    fx.commit('restaura el archivo regular')
    return [probe(fx, {'HIS'}, label='tipo', scenario=fx.hidden(), why='la restauración no deja el árbol limpio')]


def sf09(fx, c):
    original = fx.read(c['doc'])
    fx.git('checkout', '-q', '-b', 'lateral')
    fx.write(c['doc'], original + b'\nalterado en una rama lateral\n')
    fx.commit('lateral: altera el documento del sucesor', c['doc'])
    fx.write(c['doc'], original)
    fx.commit('lateral: lo restaura', c['doc'])
    fx.git('checkout', '-q', B2_BRANCH)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama lateral', 'lateral')
    return [probe(fx, {'HIS'}, scenario=fx.read(c['doc']) == original, why='el resultado del merge no parece correcto')]


def sf10(fx, c):
    fx.git('checkout', '-q', '-b', 'develop', B2_BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama de B2 en develop', B2_BRANCH)
    return [probe(fx, set(), label='develop (72e86c5) tras el merge')]


def sf11(fx, c):
    fx.git('commit', '-q', '--allow-empty', '-m', 'commit posterior sin cambios de contenido')
    return [probe(fx, set())]


def sf12(fx, c):
    fx.git('checkout', '-q', '-b', 'develop', B2_BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama de B2 en develop', B2_BRANCH)
    fx.git('checkout', '-q', '-b', 'main', B1_MAIN)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    return [probe(fx, set(), label='main (3fdfdce) tras el merge')]


def sf13(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, RULES - {'FLG', 'DEP'}, scenario=shallow, why='el clon no es superficial')]


sf13.depth = 1


def sf14_replace(fx, c):
    fx.write(c['validator'], fx.read(c['validator']) + b'\n# alterado\n')
    fx.commit('altera el gate sucesor', c['validator'])
    blob = fx.text('rev-parse', 'HEAD:' + c['validator'])
    index = dict(fx.env, GIT_INDEX_FILE=os.path.join(fx.root, '.git', 'indice-falso'))
    run_git(['read-tree', SUCCESSOR], fx.root, index)
    run_git(['update-index', '--cacheinfo', f'100644,{blob},{c["validator"]}'], fx.root, index)
    tree = run_git(['write-tree'], fx.root, index).decode('utf-8').strip()
    parents = [arg for p in fx.text('rev-parse', SUCCESSOR + '^@').split() for arg in ('-p', p)]
    forged = fx.text('commit-tree', tree, *parents, '-m', 'sucesor falsificado')
    fx.git('replace', SUCCESSOR, forged)
    seen = fx.text('rev-parse', f'{SUCCESSOR}:{c["validator"]}') == blob      # Git ya muestra el sucesor falsificado
    return [probe(fx, {'ENT', 'HIS', 'ARB', 'IDX', 'DSK', 'VIG', 'ALC'}, label='git replace', scenario=seen,
                  why='git replace no sustituyó el sucesor')]


def sf14_graft(fx, c):
    head, parent = fx.text('rev-parse', 'HEAD'), fx.text('rev-parse', 'HEAD^')
    grafts = fx.text('rev-parse', '--git-path', 'info/grafts')
    fx.write(grafts.replace('\\', '/'), f'{head} {parent}\n'.encode('ascii'))   # injerto sin efecto: los mismos padres
    return [probe(fx, {'ENT', 'VIG'}, label='injertos')]


def sf15(fx, c):
    clean = fx.sibling('sf15-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    return [probe(fx, {'ENT'}, env=hostile)]


def sf16_assume(fx, c):
    fx.git('update-index', '--assume-unchanged', '--', c['doc'])
    fx.write(c['doc'], fx.read(c['doc']) + b'\noculto\n')
    return [probe(fx, {'FLG', 'DSK', 'VIG'}, label='assume-unchanged', scenario=fx.hidden(), why='git status lo muestra')]


def sf16_skip(fx, c):
    fx.git('update-index', '--skip-worktree', '--', c['tests'])
    fx.write(c['tests'], fx.read(c['tests']) + b'\n# oculto\n')
    return [probe(fx, {'FLG', 'DSK', 'VIG'}, label='skip-worktree', scenario=fx.hidden(), why='git status lo muestra')]


def sf17(fx, c):
    original = fx.read(c['doc'])
    fx.write(c['doc'], original + b'\nsolo en el indice\n')
    fx.git('add', '--', c['doc'])
    fx.write(c['doc'], original)
    return [probe(fx, {'IDX', 'ALC', 'VIG'})]


def sf18_ignored(fx, c):
    folder = c['validator'].rsplit('/', 1)[0]
    fx.write(folder + '/__pycache__/modulo.cpython-312.pyc', b'\x00artefacto')
    return [probe(fx, {'DSK', 'VIG'}, label='archivo ignorado', scenario=fx.hidden(), why='git status lo muestra')]


def sf18_symlink(fx, c):
    folder = c['validator'].rsplit('/', 1)[0]
    try:
        os.symlink(fx.path(c['validator']), fx.path(folder + '/enlace.py'))
    except OSError as e:
        return [probe(fx, {'DSK', 'ALC', 'VIG'}, label='enlace simbólico nuevo', scenario=False,
                      why=f'el sistema no permite crear enlaces simbólicos ({e.__class__.__name__})')]
    return [probe(fx, {'DSK', 'ALC', 'VIG'}, label='enlace simbólico nuevo')]


def sf18_gitlink(fx, c):
    fx.git('update-index', '--cacheinfo', f'160000,{CANDIDATE},{c["doc"]}')
    return [probe(fx, {'IDX', 'ALC', 'VIG'}, label='gitlink en el índice')]


def sf19(fx, c):
    top = fx.text('commit-tree', fx.text('rev-parse', 'HEAD^{tree}'), '-p', FREEZE,
                  '-m', 'capa sucesora y cierre reconstruidos con los mismos bytes en otra historia')
    fx.git('checkout', '-q', '-B', B2_BRANCH, top)
    return [probe(fx, {'ANC', 'HIS', 'FRZ'})]


def sf20(fx, c):
    data = fx.read(c['validator'])
    weak = data.replace(b"        mat = check('MAT', mat_problems, gate_blob) if gate_blob is not None else None\n",
                        b'        mat = None\n', 1)
    fx.write(c['validator'], weak)
    return [probe(fx, {'DSK', 'VIG', 'ALC'}, scenario=weak != data, why='la evaluación material no se pudo retirar',
                  check=not_run('VIG'))]


def sf21(fx, c):
    fx.write(EVIDENCE, fx.read(EVIDENCE) + b'\n')
    return [probe(fx, {'VIG', 'ALC'}, mat={'SBX', 'FSY', 'PRE'})]


def sf22(fx, c):
    _manifest_hash(fx)
    return [probe(fx, {'VIG', 'ALC'}, mat={'SBX', 'FSY', 'STA'})]


def sf23(fx, c):
    data = fx.read(EVIDENCE) + b'\n'
    fx.write(EVIDENCE, data)
    _manifest_hash(fx, hashlib.sha256(data).hexdigest())
    return [probe(fx, {'VIG', 'ALC'}, mat={'SBX', 'FSY', 'STA'})]


def sf24(fx, c):
    fx.write('public/build/assets/fixture.js', b'console.log("artefacto generado sin origen verificable");\n')
    return [probe(fx, {'VIG'}, mat={'FSY'}, scenario=fx.hidden(), why='git status muestra el archivo')]


def sf25(fx, c):
    data = fx.read(c['doc']) + b'\nalterado con un manifiesto coherente\n'
    fx.write(c['doc'], data)
    manifest = json.loads(fx.read(CLOSURE_MANIFEST).decode('utf-8'))
    found = [e for e in manifest['protected_set'] if e.get('path') == c['doc']]
    if len(found) != 1:
        raise Failure('el manifiesto del cierre no tiene una entrada única para el documento del sucesor')
    found[0].update(blob=blob_id(data), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    fx.write(CLOSURE_MANIFEST, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    fx.commit('altera el documento del sucesor y ajusta el manifiesto del cierre', c['doc'], CLOSURE_MANIFEST)
    return [probe(fx, {'MAN', 'HIS', 'ARB', 'IDX', 'DSK', 'ALC', 'FRZ'})]


# ---------------------------------------------------------------- nivel B: la capa del cierre
def sf07(fx, c):
    data = fx.read(CLOSURE_MANIFEST)
    fx.write(CLOSURE_MANIFEST, data.replace(b'"B2-SUCCESSOR-FREEZE"', b'"B2-SUCCESSOR-FREEZE-ALTERADO"', 1))
    fx.commit('altera el manifiesto del cierre', CLOSURE_MANIFEST)
    return [probe(fx, {'MAN', 'FRZ'}, scenario=fx.read(CLOSURE_MANIFEST) != data, why='el manifiesto no cambió')]


def sf08(fx, c):
    trusted = fx.read(CLOSURE)
    modified = trusted + b'\n\ndef _capacidad_nueva():\n    import sqlite3\n    return sqlite3\n'
    fx.write(CLOSURE, modified)
    fx.commit('altera el validador del cierre', CLOSURE)
    fx.write(CLOSURE, trusted)
    out = [probe(fx, {'FRZ'}, label='copia de confianza en el disco')]
    fx.write(CLOSURE, modified)
    out.append(probe(fx, {'FRZ', 'DEP'}, label='copia alterada en el disco'))
    return out


def sf26(fx, c):
    top = fx.text('commit-tree', fx.text('rev-parse', 'HEAD^{tree}'), '-p', SUCCESSOR,
                  '-m', 'cierre reconstruido con los mismos bytes en otra historia')
    fx.git('checkout', '-q', '-B', B2_BRANCH, top)
    return [probe(fx, set(), check=lambda info: None if anchor(info) == top and top != c['completion'] else
                  f'el ancla derivada ({anchor(info)}) no distingue el cierre reconstruido ({top[:12]})')]


CASES = (
    ('SF01', 'estado válido del cierre', (sf01,)),
    ('SF02', 'gate sucesor modificado y confirmado', (sf02,)),
    ('SF03', 'batería del sucesor modificada y confirmada', (sf03,)),
    ('SF04', 'documento del sucesor modificado y confirmado', (sf04,)),
    ('SF05', 'modificar → restaurar un artefacto del sucesor', (sf05,)),
    ('SF06', 'renombrar, eliminar, cambiar el modo o el tipo, y restaurar', (sf06_rename, sf06_delete, sf06_mode,
                                                                            sf06_type)),
    ('SF07', 'manifiesto del cierre alterado y confirmado', (sf07,)),
    ('SF08', 'validador del cierre alterado y confirmado', (sf08,)),
    ('SF09', 'rama lateral que altera y restaura el sucesor, integrada con merge --no-ff', (sf09,)),
    ('SF10', 'merge --no-ff legítimo en develop', (sf10,)),
    ('SF11', 'commit posterior sin cambios de contenido', (sf11,)),
    ('SF12', 'merge --no-ff legítimo de develop en main', (sf12,)),
    ('SF13', 'clon superficial', (sf13,)),
    ('SF14', 'sustitución de objetos e injertos', (sf14_replace, sf14_graft)),
    ('SF15', 'GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE presentes', (sf15,)),
    ('SF16', 'assume-unchanged y skip-worktree con un cambio que git status no ve', (sf16_assume, sf16_skip)),
    ('SF17', 'índice distinto con el disco correcto', (sf17,)),
    ('SF18', 'objeto inesperado en una superficie reservada', (sf18_ignored, sf18_symlink, sf18_gitlink)),
    ('SF19', 'sucesor reconstruido con los mismos bytes en otra historia', (sf19,)),
    ('SF20', 'gate sucesor debilitado sin evaluación material', (sf20,)),
    ('SF21', 'LF añadido a evidence.csv', (sf21,)),
    ('SF22', 'SHA-256 de evidence.csv alterado en el manifiesto F34', (sf22,)),
    ('SF23', 'CSV y manifiesto F34 alterados de forma coherente', (sf23,)),
    ('SF24', 'artefacto ignorado en una superficie del runtime', (sf24,)),
    ('SF25', 'archivo del sucesor y manifiesto del cierre alterados de forma coherente', (sf25,)),
    ('SF26', 'cierre reconstruido con los mismos bytes en otra historia', (sf26,)),
)


def context(base, env):
    """HEAD probado, rutas del sucesor derivadas de Git (delta entre el freeze y el sucesor) y commit que completa el
    cierre en la historia de HEAD (el primero que contiene sus cuatro archivos)."""
    head = run_git(['rev-parse', '--verify', 'HEAD^{commit}'], base, env).decode('utf-8').strip()
    raw = run_git(['diff-tree', '-r', '--no-renames', '--name-status', '-z', FREEZE, SUCCESSOR], base, env).split(b'\x00')
    added = {raw[i + 1].decode('utf-8'): raw[i].decode('ascii') for i in range(0, len(raw) - 1, 2) if raw[i]}
    py = sorted(p for p, s in added.items() if s == 'A' and p.endswith('.py'))
    md = sorted(p for p, s in added.items() if s == 'A' and p.endswith('.md'))
    if len(added) != 3 or len(py) != 2 or len(md) != 1 or not py[1].rsplit('/', 1)[1].startswith('validate_'):
        raise Failure(f'precondición: el delta del sucesor no tiene la forma auditada: {sorted(added.items())}')
    completion = None
    for commit in run_git(['rev-list', '--reverse', '--ancestry-path', f'{SUCCESSOR}..{head}'], base, env).decode(
            'ascii').split():
        names = set(run_git(['ls-tree', '-r', '--name-only', '-z', commit, '--',
                             CLOSURE_TOOLS, CLOSURE_FILES[3].rsplit('/', 1)[0]], base, env).decode('utf-8').split('\x00'))
        if set(CLOSURE_FILES) <= names:
            completion = commit
            break
    return {'head': head, 'validator': py[1], 'tests': py[0], 'doc': md[0], 'completion': completion}


def fmt(rules):
    return 'PASS' if not rules else 'FAIL en ' + ', '.join(sorted(rules))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    work, good, bad = None, 0, 0
    try:
        work = make_temp('base')
        config = os.path.join(work, 'gitconfig')
        with open(config, 'wb'):
            pass
        env = git_env(config)
        base = os.path.join(work, 'base')
        run_git(['clone', '-q', '--shared', '--no-checkout', ROOT, base], work, env)
        ctx = context(base, env)
    except (Failure, OSError, ValueError) as e:
        print(f'FALLA preparación: {e.__class__.__name__}: {e}')
        print('test_f35sbxb2_sucesor_freeze: 0 casos correctos, 1 fallas (preparación no ejecutable)')
        if work is not None:
            remove_tree(work)
        sys.exit(1)
    print(f'INFO HEAD probado: {ctx["head"]}; commit que completa el cierre: {ctx["completion"] or "ninguno"}')
    for cid, what, setups in CASES:
        problems, notes = [], []
        for setup in setups:
            fx = None
            try:
                fx = Fixture(base, cid.lower(), env, ctx['head'], getattr(setup, 'depth', None))
                probes = setup(fx, ctx)
            except (Failure, OSError, ValueError, KeyError, TypeError, IndexError, subprocess.TimeoutExpired) as e:
                probes = [('', None, None, f'preparación no ejecutable ({e.__class__.__name__}: {e})')]
            finally:
                if fx is not None:
                    try:
                        fx.cleanup()
                    except OSError as e:
                        problems.append(f'limpieza incompleta del clon ({e.__class__.__name__})')
            for label, expected, observed, detail in probes:
                tag = f'{label}: ' if label else ''
                if expected is not None and observed == expected:
                    notes.append(tag + fmt(observed))
                elif expected is None:
                    problems.append(tag + detail)
                else:
                    problems.append(f'{tag}esperado {fmt(expected)}, observado ' +
                                    (fmt(observed) if observed is not None else detail))
        if problems:
            bad += 1
            print(f'FALLA {cid} {what}: ' + '; '.join(problems))
        else:
            good += 1
            print(f'OK    {cid} {what}: ' + '; '.join(notes))
    try:
        remove_tree(work)
    except OSError as e:
        bad += 1
        print(f'FALLA limpieza del temporal base ({e.__class__.__name__})')
    print(f'test_f35sbxb2_sucesor_freeze: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del validador)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
