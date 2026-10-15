"""F35-SBX-B — batería del cierre de gobierno de B2, B2-GOVERNMENT-CLOSURE (test_f35sbxb2_cierre_gobierno.py).

Uso:  python -I docs/academico/tools/f35sbxb2_cierre_gobierno/test_f35sbxb2_cierre_gobierno.py   (sin -I, se relanza)

Fija en RED el gate sucesor del incremento de gobierno que registra la integración técnica de B2: la transición única
y monotónica B2_GOVERNANCE_BLOB → B2_CLOSURE_GOVERNANCE_BLOB, la integridad de las capas congeladas desde sus anclas, la
evaluación material vigente (el gate de B2 y el cierre de la capa sucesora, intactos, con su falla de clase A
clasificada con exactitud) y el nivel B de esta capa.

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en
GC17, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta allí el gate con
python -I. Pasa si fallan exactamente las reglas esperadas y, cuando se indica, si las líneas FALLA o INFO contienen el
motivo esperado. El repositorio original no se modifica.
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
import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'          # develop al crear la rama de B2
DEVELOP_MERGE = 'eb02c2d84335347c52b81a76c1e73dc30b93e88a'    # integración de B2 en develop; base de este incremento
MAIN_MERGE = '5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33'       # integración de B2 en main
BRANCH = 'chore/f35-sbx-b2-government-closure'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md')
LAYER_TOOLS = 'docs/academico/tools/f35sbxb2_cierre_gobierno'
GATE = LAYER_TOOLS + '/validate_f35sbxb2_cierre_gobierno.py'
TESTS = LAYER_TOOLS + '/test_f35sbxb2_cierre_gobierno.py'
DOC = 'docs/academico/evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md'
LAYER_FILES = (DOC, GATE, TESTS)
STORE = 'docs/academico/tools/f35sbxb2/sbxb_store.py'
B1_GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
SF_VALIDATOR = 'docs/academico/tools/f35sbxb2_sucesor_freeze/validate_f35sbxb2_sucesor_freeze.py'
SUC_DOC = 'docs/academico/evidencia-sbx-b2-sucesor/F35SBXB_B2_Sucesor.md'
EVIDENCE = 'docs/academico/datos-sinteticos/dataset/evidence.csv'
RULES = frozenset({'ENT', 'CTX', 'ANC', 'HIS', 'SUC', 'MAT', 'INT', 'FLG', 'GOV', 'SEM', 'ALC', 'FRZ', 'DEP'})
SUMMARY = 'validate_f35sbxb2_cierre_gobierno: '
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
    path = os.path.join(base, f'f35sbxb2gc-{label}-{os.getpid()}-{_COUNTER[0]}')
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
                'GIT_AUTHOR_NAME': 'fixture-b2gc', 'GIT_AUTHOR_EMAIL': 'fixture-b2gc',
                'GIT_COMMITTER_NAME': 'fixture-b2gc', 'GIT_COMMITTER_EMAIL': 'fixture-b2gc',
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
    """Clon desechable de la base con la rama de este incremento en HEAD. Nada de lo que se hace aquí llega al
    repositorio. Con depth, el clon es superficial (copia de objetos por file://); si no, comparte los objetos."""

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
        run_git(['checkout', '-q', '-B', BRANCH, self.head], root, self.env)

    def sibling(self, label):
        """Otro clon limpio del mismo HEAD, que se borra junto con el caso."""
        root = make_temp(label)
        self.extra.append(root)
        self._clone(root)
        return root

    def cleanup(self):
        for path in [self.root] + self.extra:
            remove_tree(path)

    def git(self, *args, data=None, env=None):
        return run_git(list(args), self.root, env or self.env, data)

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

    def has(self, oid):
        return subprocess.run(['git', 'cat-file', '-e', oid + '^{commit}'], cwd=self.root, env=self.env,
                              capture_output=True).returncode == 0

    def validate(self, extra_env=None):
        """(reglas en falla, INFO por regla, líneas FALLA por regla, resumen) del gate, o (None, {}, {}, motivo) si no
        terminó con un resumen coherente."""
        RUNS[0] += 1
        try:
            p = subprocess.run([sys.executable, '-I', '-B', self.path(GATE)], cwd=self.root,
                               env=dict(self.env, **(extra_env or {})), capture_output=True, timeout=7200)
        except (OSError, subprocess.TimeoutExpired) as e:
            return None, {}, {}, f'el gate no se pudo ejecutar ({e.__class__.__name__})'
        lines = p.stdout.decode('utf-8', 'replace').splitlines()
        summary = [x for x in lines if x.startswith(SUMMARY)]
        fallas = {x.split()[1].rstrip(':'): x for x in lines if x.startswith('FALLA ') and len(x.split()) > 1}
        info = {x.split()[1].rstrip(':'): x for x in lines if x.startswith('INFO ') and len(x.split()) > 1}
        if len(summary) != 1:
            tail = ((p.stdout + p.stderr).decode('utf-8', 'replace').strip().splitlines() or [''])[-1]
            return None, {}, {}, f'el gate no terminó con su resumen (código {p.returncode}): «{tail[:200]}»'
        failing = set(fallas)
        if (p.returncode == 0) != (not failing) or not failing <= RULES:
            return None, {}, {}, f'salida incoherente (código {p.returncode}; reglas en falla {sorted(failing)})'
        return failing, info, fallas, summary[0]


def anchor(info):
    line = info.get('FRZ', '')
    marker = 'commit que completa la capa: '
    return line.split(marker, 1)[1].split(';', 1)[0].strip() if marker in line else None


def b2_rules(info):
    """Reglas del gate de B2 en falla que la línea INFO de MAT nombra."""
    line = info.get('MAT', '')
    marker = 'reglas en falla: '
    if marker not in line:
        return None
    named = line.split(marker, 1)[1].split(';', 1)[0]
    return {x.strip() for x in named.split(',') if x.strip() and x.strip() != 'ninguna'}


def probe(fx, expected, label='', mat=None, scenario=True, why='', env=None, says=None, check=None):
    """Una ejecución del gate frente a las reglas que deben fallar (vacío = PASS). mat: reglas del gate de B2 que la
    línea INFO de MAT debe nombrar; says: {regla: texto} que su línea FALLA debe contener; check: comprobación adicional
    sobre las líneas INFO, que devuelve un motivo o None."""
    if not scenario:
        return label, expected, None, f'escenario no reproducido: {why}'
    observed, info, fallas, detail = fx.validate(env)
    if observed is None:
        return label, expected, None, detail
    if observed == expected:
        if mat is not None:
            named = b2_rules(info)
            if named is None or not mat <= named:
                return label, expected, None, f'MAT no nombra {sorted(mat)} (nombra {sorted(named or [])})'
        for rule, text in (says or {}).items():
            if text not in fallas.get(rule, ''):
                return label, expected, None, f'la línea FALLA {rule} no contiene «{text}»'
        if check is not None:
            problem = check(info)
            if problem:
                return label, expected, None, problem
    return label, expected, observed, detail


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def rebuild(fx, steps, merge_step=None):
    """Historia reconstruida desde DEVELOP_MERGE con el contenido de HEAD: cada paso es un grupo de rutas que se
    confirma en un commit propio (con plumbing, sobre un índice aparte). merge_step: índice del paso que se confirma
    como merge de dos padres (el anterior y un commit lateral vacío). Devuelve el último commit."""
    index = dict(fx.env, GIT_INDEX_FILE=os.path.join(fx.root, '.git', 'indice-reconstruido'))
    run_git(['read-tree', DEVELOP_MERGE], fx.root, index)
    parent = DEVELOP_MERGE
    for k, paths in enumerate(steps):
        for rel in paths:
            oid = fx.text('rev-parse', f'HEAD:{rel}')
            run_git(['update-index', '--add', '--cacheinfo', f'100644,{oid},{rel}'], fx.root, index)
        tree = run_git(['write-tree'], fx.root, index).decode('ascii').strip()
        parents = ['-p', parent]
        if k == merge_step:
            side = fx.text('commit-tree', fx.text('rev-parse', parent + '^{tree}'), '-p', parent, '-m', 'rama lateral')
            parents += ['-p', side]
        parent = fx.text('commit-tree', tree, *parents, '-m', f'paso {k + 1} de la historia reconstruida')
    fx.git('checkout', '-q', '-f', '-B', BRANCH, parent)
    return parent


def gov_edit(fx, old, new, message):
    """Reemplaza un bloque (una vez) en cada ruta de gobierno que lo contiene, al menos una, y lo confirma."""
    edited = []
    for rel in GOV_PATHS:
        data = fx.read(rel)
        if old.encode('utf-8') in data:
            fx.write(rel, data.replace(old.encode('utf-8'), new.encode('utf-8'), 1))
            edited.append(rel)
    if not edited:
        raise Failure('el bloque a reemplazar no aparece en el gobierno')
    fx.commit(message, *edited)


# ---------------------------------------------------------------- estados legítimos
def gc01(fx, c):
    return [probe(fx, set(), check=lambda info: None if anchor(info) == c['completion'] else
                  f'ancla derivada {anchor(info)} distinta del commit que completa la capa {c["completion"]}')]


def gc02(fx, c):
    if not fx.has(MAIN_MERGE):
        return [probe(fx, set(), scenario=False, why=f'el merge de main {MAIN_MERGE[:12]} no está en los objetos')]
    fx.git('checkout', '-q', '-b', 'develop', DEVELOP_MERGE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff del cierre de gobierno en develop', BRANCH)
    out = [probe(fx, set(), label='develop (eb02c2d) tras el merge')]
    fx.git('checkout', '-q', '-b', 'main', MAIN_MERGE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    out.append(probe(fx, set(), label='main (5bf4f4e) tras el merge'))
    return out


def gc03(fx, c):
    fx.git('commit', '-q', '--allow-empty', '-m', 'commit posterior sin cambios de contenido')
    return [probe(fx, set())]


# ---------------------------------------------------------------- monotonía de la transición
def gc04(fx, c):
    fx.write('CLAUDE.md', fx.read('CLAUDE.md') + b'\nLinea fuera del delta cerrado.\n')
    fx.commit('tercer blob de gobierno', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def gc05(fx, c):
    original = fx.read('CLAUDE.md')
    fx.write('CLAUDE.md', original + b'\nLinea temporal.\n')
    fx.commit('modifica el gobierno', 'CLAUDE.md')
    fx.write('CLAUDE.md', original)
    fx.commit('lo restaura', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def gc06(fx, c):
    for rel in GOV_PATHS:
        fx.write(rel, fx.git('cat-file', 'blob', f'{DEVELOP_MERGE}:{rel}'))
    fx.commit('vuelve al blob de gobierno de B2', *GOV_PATHS)
    return [probe(fx, {'GOV', 'SEM', 'ALC'}, says={'GOV': 'regla 3'})]


def gc07(fx, c):
    top = rebuild(fx, [(DOC, TESTS), GOV_PATHS, (GATE,)])
    return [probe(fx, {'GOV'}, says={'GOV': 'registrada'},
                  check=lambda info: None if anchor(info) == top and top != c['completion'] else
                  f'el ancla derivada ({anchor(info)}) no distingue la historia reconstruida ({top[:12]})')]


def gc08(fx, c):
    rebuild(fx, [(TESTS,), GOV_PATHS + (DOC,), (GATE,)])
    return [probe(fx, {'GOV'}, says={'GOV': 'otras rutas'})]


def gc09(fx, c):
    rebuild(fx, [(DOC, TESTS), GOV_PATHS, (GATE,)], merge_step=1)
    return [probe(fx, {'GOV'}, says={'GOV': 'un solo padre'})]


def gc10(fx, c):
    rebuild(fx, [(DOC, TESTS), GOV_PATHS[:1], GOV_PATHS[1:], (GATE,)])
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 4'})]


# ---------------------------------------------------------------- integridad de las capas congeladas
def gc11(fx, c):
    fx.write(STORE, fx.read(STORE) + b'\n# alterado\n')
    fx.commit('altera el almacén de B2', STORE)
    return [probe(fx, {'INT', 'MAT', 'SUC', 'ALC'})]


def gc12(fx, c):
    fx.write(SF_VALIDATOR, fx.read(SF_VALIDATOR) + b'\n# alterado\n')
    fx.commit('altera el validador de B2-SUCCESSOR-FREEZE', SF_VALIDATOR)
    return [probe(fx, {'INT', 'SUC', 'ALC'})]


def gc13(fx, c):
    original = fx.read(SUC_DOC)
    fx.write(SUC_DOC, original + b'\nalterado\n')
    fx.commit('modifica el documento del sucesor', SUC_DOC)
    fx.write(SUC_DOC, original)
    fx.commit('lo restaura', SUC_DOC)
    return [probe(fx, {'INT', 'SUC'})]


def gc14(fx, c):
    original = fx.read(B1_GATE)
    fx.git('checkout', '-q', '-b', 'lateral')
    fx.write(B1_GATE, original + b'\n# alterado en una rama lateral\n')
    fx.commit('lateral: altera el gate de B1', B1_GATE)
    fx.write(B1_GATE, original)
    fx.commit('lateral: lo restaura', B1_GATE)
    fx.git('checkout', '-q', BRANCH)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama lateral', 'lateral')
    return [probe(fx, {'INT', 'MAT'}, scenario=fx.read(B1_GATE) == original, why='el merge no restauró el gate')]


# ---------------------------------------------------------------- evaluación material
def gc15(fx, c):
    fx.write(EVIDENCE, fx.read(EVIDENCE) + b'\n')
    return [probe(fx, {'MAT', 'SUC', 'ALC'}, mat={'SBX', 'FSY', 'PRE'})]


def gc16(fx, c):
    fx.write('public/build/assets/fixture.js', b'console.log("artefacto generado sin origen verificable");\n')
    return [probe(fx, {'MAT'}, mat={'FSY'}, scenario=fx.hidden(), why='git status muestra el archivo')]


# ---------------------------------------------------------------- entorno de Git
def gc17(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, RULES - {'FLG', 'DEP'}, scenario=shallow, why='el clon no es superficial')]


gc17.depth = 1


def gc18(fx, c):
    clean = fx.sibling('gc18-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    return [probe(fx, {'ENT'}, env=hostile)]


def gc19(fx, c):
    head, parent = fx.text('rev-parse', 'HEAD'), fx.text('rev-parse', 'HEAD^')
    grafts = fx.text('rev-parse', '--git-path', 'info/grafts')
    fx.write(grafts.replace('\\', '/'), f'{head} {parent}\n'.encode('ascii'))   # injerto sin efecto: los mismos padres
    return [probe(fx, {'ENT', 'SUC'})]


def gc20(fx, c):
    fx.git('update-index', '--skip-worktree', '--', 'CLAUDE.md')
    fx.write('CLAUDE.md', fx.read('CLAUDE.md') + b'\noculto\n')
    return [probe(fx, {'GOV', 'FLG', 'MAT', 'SUC'}, scenario=fx.hidden(), why='git status lo muestra')]


# ---------------------------------------------------------------- nivel B y contenido de esta capa
def gc21(fx, c):
    fx.write(DOC, fx.read(DOC) + b'\nTexto alterado tras completar la capa.\n')
    fx.commit('altera el documento de la capa', DOC)
    return [probe(fx, {'FRZ'})]


def gc22(fx, c):
    trusted = fx.read(GATE)
    modified = trusted + b'\n\ndef _capacidad_nueva():\n    import sqlite3\n    return sqlite3\n'
    fx.write(GATE, modified)
    fx.commit('altera el gate de la capa', GATE)
    fx.write(GATE, trusted)
    out = [probe(fx, {'FRZ'}, label='copia de confianza en el disco')]
    fx.write(GATE, modified)
    out.append(probe(fx, {'FRZ', 'DEP'}, label='copia alterada en el disco'))
    return out


def gc23(fx, c):
    address = 'persona.ficticia' + '@' + 'ejemplo-sintetico.org'      # construido aquí: no queda en ningún documento
    fx.write(DOC, fx.read(DOC) + f'\nContacto de prueba: {address}\n'.encode('utf-8'))
    fx.commit('añade un dato personal ficticio al documento de la capa', DOC)
    return [probe(fx, {'SEM', 'FRZ'})]


def gc24(fx, c):
    gov_edit(fx, 'B2 INTEGRADA TÉCNICAMENTE Y PENDIENTE DE CIERRE FORMAL', 'B2 CERRADA FORMALMENTE',
             'el gobierno declara el cierre formal anticipado')
    return [probe(fx, {'GOV', 'SEM', 'MAT'})]


def gc25(fx, c):
    gov_edit(fx, '- G0 real = NO APROBADA', '- G0 real = APROBADA', 'el gobierno cambia G0 real')
    return [probe(fx, {'GOV', 'SEM', 'MAT'})]


def gc26(fx, c):
    fx.git('checkout', '-q', '--detach', 'HEAD')
    return [probe(fx, {'CTX', 'MAT'})]


CASES = (
    ('GC01', 'estado válido', (gc01,)),
    ('GC02', 'merge --no-ff en develop y de develop en main', (gc02,)),
    ('GC03', 'commit posterior sin cambios de contenido', (gc03,)),
    ('GC04', 'tercer blob de gobierno tras la transición', (gc04,)),
    ('GC05', 'modificar → restaurar el gobierno tras la transición', (gc05,)),
    ('GC06', 'vuelta al blob de gobierno de B2', (gc06,)),
    ('GC07', 'historia reconstruida con el mismo contenido', (gc07,)),
    ('GC08', 'transición que también cambia otra ruta', (gc08,)),
    ('GC09', 'transición hecha en un merge', (gc09,)),
    ('GC10', 'transición repartida en dos commits', (gc10,)),
    ('GC11', 'almacén de B2 alterado y confirmado', (gc11,)),
    ('GC12', 'validador de B2-SUCCESSOR-FREEZE alterado y confirmado', (gc12,)),
    ('GC13', 'modificar → restaurar el documento del sucesor', (gc13,)),
    ('GC14', 'rama lateral que altera y restaura el gate de B1, integrada con merge --no-ff', (gc14,)),
    ('GC15', 'LF añadido a evidence.csv', (gc15,)),
    ('GC16', 'artefacto ignorado en una superficie del runtime', (gc16,)),
    ('GC17', 'clon superficial', (gc17,)),
    ('GC18', 'GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE presentes', (gc18,)),
    ('GC19', 'injertos sin efecto', (gc19,)),
    ('GC20', 'skip-worktree en el gobierno con un cambio que git status no ve', (gc20,)),
    ('GC21', 'documento de la capa modificado tras completarla', (gc21,)),
    ('GC22', 'gate de la capa alterado y confirmado', (gc22,)),
    ('GC23', 'dato personal ficticio en el documento de la capa', (gc23,)),
    ('GC24', 'gobierno que declara el cierre formal anticipado de B2', (gc24,)),
    ('GC25', 'gobierno que declara G0 real aprobada', (gc25,)),
    ('GC26', 'HEAD separado', (gc26,)),
)


def context(base, env):
    """HEAD probado y commit que completa la capa en su historia (el primero posterior a DEVELOP_MERGE que contiene
    sus tres archivos)."""
    head = run_git(['rev-parse', '--verify', 'HEAD^{commit}'], base, env).decode('utf-8').strip()
    completion = None
    for commit in run_git(['rev-list', '--reverse', '--ancestry-path', f'{DEVELOP_MERGE}..{head}'], base, env).decode(
            'ascii').split():
        names = set(run_git(['ls-tree', '-r', '--name-only', '-z', commit, '--', LAYER_TOOLS, DOC.rsplit('/', 1)[0]],
                            base, env).decode('utf-8').split('\x00'))
        if set(LAYER_FILES) <= names:
            completion = commit
            break
    return {'head': head, 'completion': completion}


def fmt(rules):
    return 'PASS' if not rules else 'FAIL en ' + ', '.join(sorted(rules))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    only = set(sys.argv[1:])
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
        print('test_f35sbxb2_cierre_gobierno: 0 casos correctos, 1 fallas (preparación no ejecutable)')
        if work is not None:
            remove_tree(work)
        sys.exit(1)
    print(f'INFO HEAD probado: {ctx["head"]}; commit que completa la capa: {ctx["completion"] or "ninguno"}')
    for cid, what, setups in CASES:
        if only and cid not in only:
            continue
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
            print(f'FALLA {cid} {what}: ' + '; '.join(problems), flush=True)
        else:
            good += 1
            print(f'OK    {cid} {what}: ' + '; '.join(notes), flush=True)
    try:
        remove_tree(work)
    except OSError as e:
        bad += 1
        print(f'FALLA limpieza del temporal base ({e.__class__.__name__})')
    print(f'test_f35sbxb2_cierre_gobierno: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del gate)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
