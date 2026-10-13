"""F35-SBX-B — batería de pruebas de B2-FREEZE (test_f35sbxb2_freeze.py).

Uso:  python -I docs/academico/tools/f35sbxb2_freeze/test_f35sbxb2_freeze.py   (sin -I, se relanza aislado)

Diseño que estas pruebas fijan antes de implementar el validador (RED):

  Nivel A  protege el candidato aprobado 2472fd6. La raíz de confianza es el commit candidato y sus objetos Git, no el
           manifiesto. El conjunto congelado es el delta de B2 respecto de 72e86c5. Después del candidato, ninguna ruta
           congelada ni superficie reservada de B2 cambia: ni en la historia (merges incluidos), ni en HEAD, ni en el
           índice, ni en el disco.
  Nivel B  protege la capa del freeze (validador, manifiesto, esta batería y su evidencia) desde el commit que la
           completa. Ese commit se deriva de Git: ningún archivo registra su propio hash.

El validador informa diez reglas: ENT, CAN, MAN, HIS, ARB, IDX, FLG, DSK, FRZ y DEP. Cada caso trabaja en un clon
desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (F20, con un clon superficial),
configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta allí el validador con python -I. El caso pasa
si el validador termina con su resumen y fallan exactamente las reglas esperadas (ninguna, si se espera PASS). Las rutas
congeladas se derivan de Git, no del manifiesto. El repositorio original no se modifica.

Salvo en la segunda sonda de B01, el validador que se ejecuta tiene los bytes del commit de freeze: los casos que lo
alteran recuperan esos bytes en el disco antes de validar, como hará la auditoría con el commit registrado.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación, como el validador: python -I, relanzado con os.spawnv.
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
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'      # develop al crear la rama de B2
B2_BRANCH = 'feature/f35-sbx-b2-ephemeral-store'
VALIDATOR = 'docs/academico/tools/f35sbxb2_freeze/validate_f35sbxb2_freeze.py'
MANIFEST = 'docs/academico/tools/f35sbxb2_freeze/b2_freeze_manifest.json'
TESTS = 'docs/academico/tools/f35sbxb2_freeze/test_f35sbxb2_freeze.py'
FREEZE_DOC = 'docs/academico/evidencia-sbx-b2-freeze/F35SBXB_B2_Freeze.md'
RULES = frozenset({'ENT', 'CAN', 'MAN', 'HIS', 'ARB', 'IDX', 'FLG', 'DSK', 'FRZ', 'DEP'})
SUMMARY = 'validate_f35sbxb2_freeze: '
STAMP = '2026-10-13T00:00:00+00:00'
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
    path = os.path.join(base, f'f35sbxb2frz-{label}-{os.getpid()}-{_COUNTER[0]}')
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
                'GIT_AUTHOR_NAME': 'fixture-b2frz', 'GIT_AUTHOR_EMAIL': 'fixture-b2frz',
                'GIT_COMMITTER_NAME': 'fixture-b2frz', 'GIT_COMMITTER_EMAIL': 'fixture-b2frz',
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
        """(reglas en falla, resumen) del validador del clon, o (None, motivo) si no terminó con un resumen coherente."""
        RUNS[0] += 1
        try:
            p = subprocess.run([sys.executable, '-I', '-B', self.path(VALIDATOR)], cwd=self.root,
                               env=dict(self.env, **(extra_env or {})), capture_output=True, timeout=900)
        except (OSError, subprocess.TimeoutExpired) as e:
            return None, f'el validador no se pudo ejecutar ({e.__class__.__name__})'
        lines = p.stdout.decode('utf-8', 'replace').splitlines()
        summary = [x for x in lines if x.startswith(SUMMARY)]
        failing = {x.split()[1].rstrip(':') for x in lines if x.startswith('FALLA ') and len(x.split()) > 1}
        if len(summary) != 1:
            tail = ((p.stdout + p.stderr).decode('utf-8', 'replace').strip().splitlines() or [''])[-1]
            return None, f'el validador no terminó con su resumen (código {p.returncode}): «{tail[:200]}»'
        if (p.returncode == 0) != (not failing) or not failing <= RULES:
            return None, f'salida incoherente del validador (código {p.returncode}; reglas en falla {sorted(failing)})'
        return failing, summary[0]


def probe(fx, expected, label='', scenario=True, why='', env=None):
    """Una ejecución del validador frente a las reglas que deben fallar (vacío = PASS)."""
    if not scenario:
        return label, expected, None, f'escenario no reproducido: {why}'
    observed, detail = fx.validate(env)
    return label, expected, observed, detail


def load_manifest(fx):
    return json.loads(fx.read(MANIFEST).decode('utf-8'))


def save_manifest(fx, manifest):
    fx.write(MANIFEST, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def frozen_entry(manifest, path):
    found = [e for e in manifest['frozen_set'] if e.get('path') == path]
    if len(found) != 1:
        raise Failure(f'el manifiesto no tiene una entrada única para {path}')
    return found[0]


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


# ---------------------------------------------------------------- nivel A: candidato
def f01(fx, c):
    return [probe(fx, set())]


def f02(fx, c):
    path = c['py'][0]
    fx.write(path, fx.read(path) + b'# alterado\n')
    fx.commit('altera un archivo congelado', path)
    return [probe(fx, {'HIS', 'ARB', 'IDX', 'DSK'})]


def f03(fx, c):
    path = c['md'][0]
    original = fx.read(path)
    fx.write(path, original + b'\nalterado\n')
    fx.commit('modifica un archivo congelado', path)
    fx.write(path, original)
    fx.commit('lo restaura', path)
    return [probe(fx, {'HIS'})]


def f04(fx, c):
    path = c['py'][1]
    fx.git('rm', '-q', '--', path)
    fx.commit('elimina un archivo congelado')
    fx.git('checkout', '-q', 'HEAD~1', '--', path)
    fx.commit('lo restaura')
    return [probe(fx, {'HIS'})]


def f05(fx, c):
    path = c['py'][0]
    moved = path.rsplit('/', 1)[0] + '/renombrado.py'
    fx.git('mv', path, moved)
    fx.commit('renombra un archivo congelado')
    fx.git('mv', moved, path)
    fx.commit('restaura su nombre')
    return [probe(fx, {'HIS'})]


def f06(fx, c):
    path = c['py'][1]
    fx.git('update-index', '--chmod=+x', '--', path)
    fx.commit('cambia el modo a 100755')
    fx.git('update-index', '--chmod=-x', '--', path)
    fx.commit('restaura el modo 100644')
    return [probe(fx, {'HIS'})]


def f07(fx, c):
    path = c['gov'][0]
    fx.write(path, fx.read(path) + b'\n')
    return [probe(fx, {'DSK'})]


def f08(fx, c):
    path = c['gov'][1]
    original = fx.read(path)
    fx.write(path, original + b'\nsolo en el indice\n')
    fx.git('add', '--', path)
    fx.write(path, original)
    return [probe(fx, {'IDX'})]


def f09(fx, c):
    path = c['py'][0]
    fx.git('update-index', '--assume-unchanged', '--', path)
    fx.write(path, fx.read(path) + b'# oculto\n')
    return [probe(fx, {'FLG', 'DSK'}, scenario=fx.hidden(), why='git status muestra el cambio')]


def f10(fx, c):
    path = c['md'][2]
    fx.git('update-index', '--skip-worktree', '--', path)
    fx.write(path, fx.read(path) + b'\noculto\n')
    return [probe(fx, {'FLG', 'DSK'}, scenario=fx.hidden(), why='git status muestra el cambio')]


def f11(fx, c):
    manifest = load_manifest(fx)
    manifest['frozen_set'] = [e for e in manifest['frozen_set'] if e.get('path') != c['gov'][1]]
    save_manifest(fx, manifest)
    fx.commit('excluye una ruta del conjunto congelado', MANIFEST)
    return [probe(fx, {'MAN', 'FRZ'})]


def f12_blob(fx, c):
    manifest = load_manifest(fx)
    frozen_entry(manifest, c['gov'][0])['blob'] = fx.text('rev-parse', f'{B2_BASE}:{c["gov"][0]}')
    save_manifest(fx, manifest)
    fx.commit('blob histórico en el manifiesto', MANIFEST)
    return [probe(fx, {'MAN', 'FRZ'}, label='blob')]


def f12_sha(fx, c):
    manifest = load_manifest(fx)
    entry = frozen_entry(manifest, c['py'][1])
    entry['sha256'] = entry['sha256'][:-1] + ('1' if entry['sha256'].endswith('0') else '0')
    save_manifest(fx, manifest)
    fx.commit('SHA-256 alterado en el manifiesto', MANIFEST)
    return [probe(fx, {'MAN', 'FRZ'}, label='SHA-256')]


def f12_size(fx, c):
    manifest = load_manifest(fx)
    frozen_entry(manifest, c['md'][1])['bytes'] += 1
    save_manifest(fx, manifest)
    fx.commit('tamaño alterado en el manifiesto', MANIFEST)
    return [probe(fx, {'MAN', 'FRZ'}, label='tamaño')]


def f13(fx, c):
    folder = c['py'][0].rsplit('/', 1)[0]
    fx.write(folder + '/__pycache__/modulo.cpython-312.pyc', b'\x00artefacto')
    return [probe(fx, {'DSK'}, scenario=fx.hidden(), why='git status muestra el archivo')]


def f14(fx, c):
    other = fx.text('rev-parse', CANDIDATE + '^')
    manifest = load_manifest(fx)
    manifest['candidate_commit'] = other
    for entry in manifest['frozen_set']:
        oid = fx.text('rev-parse', f'{other}:{entry["path"]}')
        data = fx.git('cat-file', 'blob', oid)
        entry.update(blob=oid, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    save_manifest(fx, manifest)
    fx.commit('manifiesto reanclado al padre del candidato', MANIFEST)
    return [probe(fx, {'MAN', 'FRZ'})]


def f15(fx, c):
    note, out = 'docs/fixture-integracion.md', []
    fx.git('checkout', '-q', '-b', 'develop', B2_BASE)
    fx.write(note, b'# Cambio ajeno a B2\n')
    fx.commit('develop: cambio ajeno', note)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama de B2 en develop', B2_BRANCH)
    out.append(probe(fx, set(), label='develop tras el merge'))
    fx.write(note, b'# Cambio ajeno a B2\n\nPosterior al merge.\n')
    fx.commit('develop: cambio posterior', note)
    out.append(probe(fx, set(), label='develop con un commit posterior'))
    fx.git('checkout', '-q', '-b', 'main', B2_BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    out.append(probe(fx, set(), label='main tras el merge'))
    return out


def f16(fx, c):
    path = c['md'][1]
    original = fx.read(path)
    fx.git('checkout', '-q', '-b', 'lateral')
    fx.write(path, original + b'\nalterado en una rama lateral\n')
    fx.commit('lateral: altera un archivo congelado', path)
    fx.write(path, original)
    fx.commit('lateral: lo restaura', path)
    fx.git('checkout', '-q', B2_BRANCH)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama lateral', 'lateral')
    return [probe(fx, {'HIS'}, scenario=fx.read(path) == original and fx.hidden(),
                  why='el resultado del merge no parece correcto')]


def f17_gitlink(fx, c):
    fx.git('update-index', '--cacheinfo', f'160000,{CANDIDATE},{c["py"][1]}')
    return [probe(fx, {'IDX'}, label='gitlink en el índice')]


def f17_symlink(fx, c):
    path = c['py'][0]
    original = fx.read(path)
    copy = fx.path('copia-fuera-de-la-superficie.py')
    with open(copy, 'wb') as f:
        f.write(original)
    os.remove(fx.path(path))
    try:
        os.symlink(copy, fx.path(path))
    except OSError as e:
        return [probe(fx, {'DSK'}, label='enlace simbólico en el disco', scenario=False,
                      why=f'el sistema no permite crear enlaces simbólicos ({e.__class__.__name__})')]
    return [probe(fx, {'DSK'}, label='enlace simbólico en el disco',
                  scenario=os.path.islink(fx.path(path)) and fx.read(path) == original,
                  why='el enlace no entrega los bytes del candidato')]


def f18(fx, c):
    parent = fx.text('rev-parse', CANDIDATE + '^')
    rewritten = fx.text('commit-tree', fx.text('rev-parse', CANDIDATE + '^{tree}'), '-p', parent,
                        '-m', 'candidato reescrito')
    top = fx.text('commit-tree', fx.text('rev-parse', 'HEAD^{tree}'), '-p', rewritten,
                  '-m', 'capa del freeze sobre la historia reescrita')
    fx.git('checkout', '-q', '-B', 'reescrita', top)
    return [probe(fx, {'CAN', 'HIS', 'FRZ'}, scenario=rewritten != CANDIDATE, why='la reescritura reprodujo el candidato')]


def f19(fx, c):
    path = c['py'][0]
    fx.write(path, fx.read(path) + b'# alterado\n')
    fx.commit('altera un archivo congelado', path)
    blob = fx.text('rev-parse', 'HEAD:' + path)
    index = dict(fx.env, GIT_INDEX_FILE=os.path.join(fx.root, '.git', 'indice-falso'))
    run_git(['read-tree', CANDIDATE], fx.root, index)
    run_git(['update-index', '--cacheinfo', f'100644,{blob},{path}'], fx.root, index)
    tree = run_git(['write-tree'], fx.root, index).decode('utf-8').strip()
    parents = [arg for p in fx.text('rev-parse', CANDIDATE + '^@').split() for arg in ('-p', p)]
    forged = fx.text('commit-tree', tree, *parents, '-m', 'candidato falsificado')
    fx.git('replace', CANDIDATE, forged)
    seen = fx.text('rev-parse', f'{CANDIDATE}:{path}') == blob   # Git ya muestra el candidato falsificado
    return [probe(fx, {'ENT', 'HIS', 'ARB', 'IDX', 'DSK'}, scenario=seen, why='git replace no sustituyó el candidato')]


def f20(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, {'ENT', 'CAN', 'MAN', 'HIS', 'ARB', 'IDX', 'DSK', 'FRZ'}, scenario=shallow,
                  why='el clon no es superficial')]


f20.depth = 1


def f21(fx, c):
    path = c['gov'][1]
    original = fx.read(path)
    fx.write(path, original + b'\nsolo en el indice\n')
    fx.git('add', '--', path)
    fx.write(path, original)
    clean = fx.sibling('f21-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    steered = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=fx.root, env=dict(fx.env, **hostile),
                             capture_output=True).returncode == 0      # con esas variables, Git no ve el cambio
    return [probe(fx, {'IDX'}, scenario=steered, why='con esas variables Git sigue viendo el cambio', env=hostile)]


def r01(fx, c):
    path = c['py'][0]
    data = fx.read(path) + b'# alterado con un manifiesto coherente\n'
    fx.write(path, data)
    manifest = load_manifest(fx)
    frozen_entry(manifest, path).update(blob=blob_id(data), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    save_manifest(fx, manifest)
    fx.commit('altera un archivo congelado y ajusta el manifiesto para que coincida', path, MANIFEST)
    coherent = fx.text('rev-parse', 'HEAD:' + path) == frozen_entry(load_manifest(fx), path)['blob']
    return [probe(fx, {'MAN', 'HIS', 'ARB', 'IDX', 'DSK', 'FRZ'}, scenario=coherent,
                  why='el manifiesto no coincide con el archivo alterado')]


# ---------------------------------------------------------------- nivel B: capa del freeze
def b01(fx, c):
    trusted = fx.read(VALIDATOR)
    modified = trusted + b'\n\ndef _capacidad_nueva():\n    import sqlite3\n    return sqlite3\n'
    fx.write(VALIDATOR, modified)
    fx.commit('modifica el validador del freeze', VALIDATOR)
    fx.write(VALIDATOR, trusted)
    out = [probe(fx, {'FRZ'}, label='copia de confianza en el disco')]
    fx.write(VALIDATOR, modified)
    out.append(probe(fx, {'FRZ', 'DEP'}, label='copia modificada en el disco'))
    return out


def b02(fx, c):
    data = fx.read(MANIFEST)
    fx.write(MANIFEST, data.replace(b'"B2-FREEZE"', b'"B2-FREEZE-ALTERADO"', 1))
    return [probe(fx, {'MAN', 'FRZ'}, scenario=fx.read(MANIFEST) != data, why='el manifiesto no cambió')]


def b03(fx, c):
    original = fx.read(FREEZE_DOC)
    fx.write(FREEZE_DOC, original + b'\nalterado\n')
    fx.git('add', '--', FREEZE_DOC)
    fx.write(FREEZE_DOC, original)
    return [probe(fx, {'FRZ'})]


def b04(fx, c):
    original = fx.read(VALIDATOR)
    fx.write(VALIDATOR, original + b'\n# modificado\n')
    fx.commit('modifica el validador del freeze', VALIDATOR)
    fx.write(VALIDATOR, original)
    fx.commit('lo restaura', VALIDATOR)
    return [probe(fx, {'FRZ'})]


def b05(fx, c):
    layer = {path: fx.read(path) for path in (VALIDATOR, MANIFEST, TESTS, FREEZE_DOC)}
    fx.git('checkout', '-q', '-b', 'alternativa', CANDIDATE)
    for path, data in layer.items():
        fx.write(path, data + (b'\n# capa alternativa\n' if path == VALIDATOR else b''))
    fx.commit('capa del freeze alternativa en una rama lateral', *layer)
    fx.git('checkout', '-q', B2_BRANCH)
    fx.git('merge', '-q', '--no-ff', '-s', 'ours', '-m', 'merge que conserva la capa del freeze', 'alternativa')
    kept = all(fx.read(path) == data for path, data in layer.items()) and fx.hidden()
    return [probe(fx, {'FRZ'}, scenario=kept, why='el merge no conserva la capa del freeze')]


CASES = (
    ('F01', 'candidato intacto con la capa del freeze', (f01,)),
    ('F02', 'archivo congelado modificado y confirmado', (f02,)),
    ('F03', 'modificar → restaurar un archivo congelado', (f03,)),
    ('F04', 'eliminar → restaurar un archivo congelado', (f04,)),
    ('F05', 'renombrar → restaurar un archivo congelado', (f05,)),
    ('F06', 'cambio de modo → restauración', (f06,)),
    ('F07', 'modificación solo en el árbol de trabajo', (f07,)),
    ('F08', 'modificación solo en el índice (staged)', (f08,)),
    ('F09', 'assume-unchanged con un cambio que git status no ve', (f09,)),
    ('F10', 'skip-worktree con un cambio que git status no ve', (f10,)),
    ('F11', 'manifiesto manipulado: excluye una ruta congelada', (f11,)),
    ('F12', 'blob, SHA-256 o tamaño incorrectos en el manifiesto', (f12_blob, f12_sha, f12_size)),
    ('F13', 'archivo ignorado inesperado en una superficie reservada', (f13,)),
    ('F14', 'manifiesto reanclado a otro commit candidato', (f14,)),
    ('F15', 'merges --no-ff legítimos en develop y main, y un commit posterior', (f15,)),
    ('F16', 'rama lateral que altera y restaura, integrada con merge --no-ff', (f16,)),
    ('F17', 'objeto inesperado en una ruta congelada', (f17_gitlink, f17_symlink)),
    ('F18', 'historia reescrita: el candidato no es ancestro de HEAD', (f18,)),
    ('F19', 'candidato sustituido con git replace para ocultar una alteración', (f19,)),
    ('F20', 'clon superficial: la historia no es completa', (f20,)),
    ('F21', 'GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE apuntan a un clon limpio', (f21,)),
    ('R01', 'raíz de confianza: archivo congelado y manifiesto alterados de forma coherente', (r01,)),
    ('B01', 'validador del freeze modificado y confirmado', (b01,)),
    ('B02', 'manifiesto del freeze modificado en el disco', (b02,)),
    ('B03', 'evidencia del freeze modificada solo en el índice', (b03,)),
    ('B04', 'modificar → restaurar el validador del freeze', (b04,)),
    ('B05', 'segunda capa del freeze en una rama lateral, integrada con un merge que conserva la original', (b05,)),
)


def context(base, env):
    """HEAD probado y rutas congeladas derivadas de Git (delta de B2 entre su base y el candidato), por papel."""
    head = run_git(['rev-parse', '--verify', 'HEAD^{commit}'], base, env).decode('utf-8').strip()
    raw = run_git(['diff-tree', '-r', '--no-renames', '--name-status', '-z', B2_BASE, CANDIDATE], base, env).split(b'\x00')
    frozen = {raw[i + 1].decode('utf-8'): raw[i].decode('ascii') for i in range(0, len(raw) - 1, 2) if raw[i]}
    ctx = {'head': head, 'frozen': frozen,
           'gov': sorted(p for p, s in frozen.items() if s == 'M'),
           'md': sorted(p for p, s in frozen.items() if s == 'A' and p.endswith('.md')),
           'py': sorted(p for p, s in frozen.items() if s == 'A' and p.endswith('.py'))}
    if (len(frozen), len(ctx['gov']), len(ctx['md']), len(ctx['py'])) != (7, 2, 3, 2):
        raise Failure(f'precondición: el delta de B2 no tiene la forma del contrato: {sorted(frozen.items())}')
    return ctx


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
        print('test_f35sbxb2_freeze: 0 casos correctos, 1 fallas (preparación no ejecutable)')
        if work is not None:
            remove_tree(work)
        sys.exit(1)
    print(f'INFO HEAD probado: {ctx["head"]}; rutas congeladas derivadas de Git: {len(ctx["frozen"])}')
    for cid, what, setups in CASES:
        problems, notes = [], []
        for setup in setups:
            fx = None
            try:
                fx = Fixture(base, cid.lower(), env, ctx['head'], getattr(setup, 'depth', None))
                probes = setup(fx, ctx)
            except (Failure, OSError, ValueError, KeyError, TypeError) as e:
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
    print(f'test_f35sbxb2_freeze: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del validador)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
