"""F35-SBX-B — batería del gate sucesor del cierre terminal (test_f35sbxb_cierre_terminal.py).

Uso:  python -I docs/academico/tools/f35sbxb_cierre_terminal/test_f35sbxb_cierre_terminal.py [CT01 ...]
      (sin -I, se relanza)

Fija en RED el gate del cierre terminal de F35-SBX-B: los estados legítimos (la rama, los merges --no-ff en develop y en
main, un commit vacío), la transición única y monotónica en seis etapas, la integridad de las capas congeladas y de B3,
la sustitución de B3 o de la historia del cierre por contenido equivalente, los riesgos LOW registrados, la
sobredeclaración en el gobierno (F36, F35-SBX, G0 real, alcance C, datos reales, RF-23 y RF-29), el alcance, el código de
la capa y el entorno de Git hostil o incompleto.

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en
CT24, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta allí el gate con
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

import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
B3_ANCHOR = '8d39d0e547821f7d6f63dc12b9c01803f985d797'           # B3: ancla aprobada
B3_TRANSITION = 'fa5664a0a3660519744a32b320822ecc396b1619'       # transición de gobierno de B3
B3_BASE = 'ca36875938eca035c97205921ec5f9633381c571'             # integración de R2-A en develop; base de B3
BASE = '53c0eb55a8f64f5576c43c2bfb5dccf095e30412'                # integración de B3 en develop; base del cierre
MAIN_MERGE = '9424f1ea2a1e25dd29e8cfc0b9f446b3118b7a9a'          # integración de B3 en main
BRANCH = 'chore/f35-sbx-b-terminal-closure'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md')
LAYER_DOCS = 'docs/academico/evidencia-sbx-b-cierre-terminal'
LAYER_TOOLS = 'docs/academico/tools/f35sbxb_cierre_terminal'
DOC = LAYER_DOCS + '/F35SBXB_Cierre_Terminal.md'
GATE = LAYER_TOOLS + '/validate_f35sbxb_cierre_terminal.py'
TESTS = LAYER_TOOLS + '/test_f35sbxb_cierre_terminal.py'
LAYER_FILES = (DOC, GATE, TESTS)
B3_DIRS = ('docs/academico/evidencia-sbx-b3', 'docs/academico/tools/f35sbxb3')
PIPELINE = 'docs/academico/tools/f35sbxb3/sbxb_pipeline.py'
B2_DOC = 'docs/academico/evidencia-sbx-b2/README.md'
TRACEABILITY = 'docs/final-report/traceability-master.md'
RUNTIME = 'routes/web.php'
TC_STATE = ('F35-SBX-B CERRADA, CONGELADA E INTEGRADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) '
            'CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, '
            'CONGELADA E INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) CERRADA, CONGELADA '
            'E INTEGRADA, sin ML.')
B3_CLOSED = 'B3 (pipeline determinista de doce pasos sobre el almacén de B2) CERRADA, CONGELADA E INTEGRADA, sin ML.'
B3_OPEN = 'B3 (pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA, sin ML.'
LOW_ROW = '| B3-AF-L02 | LOW |'
LIMIT = '- no permite la selección automática;\n'
RULES = frozenset({'ENT', 'CTX', 'ANC', 'HIS', 'B3G', 'R2A', 'MAT', 'INT', 'FLG', 'GOV', 'SEM', 'LOW', 'ALC', 'FRZ',
                   'DEP'})
FROZEN_GATES = frozenset({'B3G', 'R2A', 'MAT'})
SUMMARY = 'validate_f35sbxb_cierre_terminal: '
STAMP = '2026-10-21T00:00:00+00:00'
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
    path = os.path.join(base, f'f35sbxbtc-{label}-{os.getpid()}-{_COUNTER[0]}')
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
                'GIT_AUTHOR_NAME': 'fixture-tc', 'GIT_AUTHOR_EMAIL': 'fixture-tc',
                'GIT_COMMITTER_NAME': 'fixture-tc', 'GIT_COMMITTER_EMAIL': 'fixture-tc',
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
        gate = self.path(GATE)
        if not os.path.isfile(gate):
            return None, {}, {}, 'el gate del cierre no existe en HEAD'
        try:
            p = subprocess.run([sys.executable, '-I', '-B', gate], cwd=self.root,
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


def probe(fx, expected, label='', scenario=True, why='', env=None, says=None, check=None):
    """Una ejecución del gate frente a las reglas que deben fallar (vacío = PASS). says: {regla: texto} que su línea
    FALLA debe contener; check: comprobación adicional sobre las líneas INFO, que devuelve un motivo o None."""
    if not scenario:
        return label, expected, None, f'escenario no reproducido: {why}'
    observed, info, fallas, detail = fx.validate(env)
    if observed is None:
        return label, expected, None, detail
    if observed == expected:
        for rule, text in (says or {}).items():
            if text not in fallas.get(rule, ''):
                return label, expected, None, f'la línea FALLA {rule} no contiene «{text}»'
        if check is not None:
            problem = check(info)
            if problem:
                return label, expected, None, problem
    return label, expected, observed, detail


def commit_tree(fx, tree, parents, message):
    args = [x for p in parents for x in ('-p', p)]
    return fx.text('commit-tree', tree, *args, '-m', message)


def closure_commits(fx):
    """Los commits del cierre, del más antiguo al más reciente: los posteriores a BASE en la historia de HEAD."""
    return fx.text('rev-list', '--reverse', '--ancestry-path', f'{BASE}..HEAD').split()


def replay(fx, commits, onto, label):
    """Los mismos árboles, uno tras otro sobre onto, con otros metadatos. Devuelve el último commit."""
    parent = onto
    for k, commit in enumerate(commits):
        parent = commit_tree(fx, fx.text('rev-parse', commit + '^{tree}'), [parent], f'{label} {k + 1}')
    fx.git('checkout', '-q', '-f', '-B', BRANCH, parent)
    return parent


def rebuild(fx, steps, merge_step=None, base=BASE):
    """Historia reconstruida desde base con el contenido de HEAD: cada paso es un grupo de rutas que se confirma en un
    commit propio (con plumbing, sobre un índice aparte). merge_step: índice del paso que se confirma como merge de dos
    padres (el anterior y un commit lateral vacío). Devuelve el último commit."""
    index = dict(fx.env, GIT_INDEX_FILE=os.path.join(fx.root, '.git', 'indice-reconstruido'))
    run_git(['read-tree', base], fx.root, index)
    parent = base
    for k, paths in enumerate(steps):
        for rel in paths:
            oid = fx.text('rev-parse', f'HEAD:{rel}')
            run_git(['update-index', '--add', '--cacheinfo', f'100644,{oid},{rel}'], fx.root, index)
        tree = run_git(['write-tree'], fx.root, index).decode('ascii').strip()
        parents = [parent]
        if k == merge_step:
            parents.append(commit_tree(fx, fx.text('rev-parse', parent + '^{tree}'), [parent], 'rama lateral'))
        parent = commit_tree(fx, tree, parents, f'paso {k + 1} de la historia reconstruida')
    fx.git('checkout', '-q', '-f', '-B', BRANCH, parent)
    return parent


def gov_replace(fx, pairs, message):
    """Aplica cada reemplazo (una vez por archivo) en las rutas de gobierno que contienen su bloque, al menos una por
    reemplazo, y lo confirma."""
    edited = set()
    for old, new in pairs:
        hit = False
        for rel in GOV_PATHS:
            data = fx.read(rel)
            if old.encode('utf-8') in data:
                fx.write(rel, data.replace(old.encode('utf-8'), new.encode('utf-8'), 1))
                edited.add(rel)
                hit = True
        if not hit:
            raise Failure(f'el bloque a reemplazar no aparece en el gobierno: «{old[:60]}»')
    fx.commit(message, *sorted(edited))


def edit(fx, rel, old, new, message):
    data = fx.read(rel)
    if data.count(old) != 1:
        raise Failure(f'{rel}: el fragmento a reemplazar no aparece exactamente una vez')
    fx.write(rel, data.replace(old, new, 1))
    fx.commit(message, rel)


# ---------------------------------------------------------------- estados legítimos
def ct01(fx, c):
    return [probe(fx, set(), check=lambda info: None if anchor(info) == c['completion'] else
                  f'ancla derivada {anchor(info)} distinta del commit que completa la capa {c["completion"]}')]


def ct02(fx, c):
    if not fx.has(MAIN_MERGE):
        return [probe(fx, set(), scenario=False, why=f'el merge de main {MAIN_MERGE[:12]} no está en los objetos')]
    fx.git('checkout', '-q', '-b', 'develop', BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff del cierre terminal en develop', BRANCH)
    out = [probe(fx, set(), label='develop (53c0eb5) tras el merge')]
    fx.git('checkout', '-q', '-b', 'main', MAIN_MERGE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    out.append(probe(fx, set(), label='main (9424f1e) tras el merge'))
    return out


def ct03(fx, c):
    fx.git('commit', '-q', '--allow-empty', '-m', 'commit posterior sin cambios de contenido')
    return [probe(fx, set())]


# ---------------------------------------------------------------- monotonía de la transición
def ct04(fx, c):
    fx.write('CLAUDE.md', fx.read('CLAUDE.md') + b'\nLinea fuera del delta cerrado.\n')
    fx.commit('séptimo blob de gobierno', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def ct05(fx, c):
    original = fx.read('CLAUDE.md')
    fx.write('CLAUDE.md', original + b'\nLinea temporal.\n')
    fx.commit('modifica el gobierno', 'CLAUDE.md')
    fx.write('CLAUDE.md', original)
    fx.commit('lo restaura', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def ct06(fx, c):
    for rel in GOV_PATHS:
        fx.write(rel, fx.git('cat-file', 'blob', f'{BASE}:{rel}'))
    fx.commit('vuelve al gobierno de B3', *GOV_PATHS)
    return [probe(fx, {'GOV', 'SEM', 'ALC'} | FROZEN_GATES, says={'GOV': 'regla 4'})]


def ct07(fx, c):
    gov_replace(fx, [(TC_STATE, TC_STATE + ' F35-SBX-B queda reabierta.')], 'el gobierno reabre F35-SBX-B')
    return [probe(fx, {'GOV', 'SEM'}, says={'SEM': 'reapertura'})]


def ct25(fx, c):
    rebuild(fx, [(DOC, TESTS), GOV_PATHS[:1], GOV_PATHS[1:], (GATE,)])
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 4'})]


def ct26(fx, c):
    rebuild(fx, [(DOC, TESTS), GOV_PATHS, (GATE,)], merge_step=1)
    return [probe(fx, {'GOV'}, says={'GOV': 'un solo padre'})]


def ct35(fx, c):
    gov_replace(fx, [(B3_CLOSED, B3_OPEN)], 'el gobierno cierra F35-SBX-B con B3 aún implementada')
    return [probe(fx, {'GOV', 'SEM'})]


def ct36(fx, c):
    rel = GOV_PATHS[2]
    fx.write(rel, fx.git('cat-file', 'blob', f'{BASE}:{rel}'))
    fx.commit('ACADEMIC_BASELINE.md vuelve a F35-SBX-B no iniciada', rel)
    return [probe(fx, {'GOV', 'SEM', 'ALC'} | FROZEN_GATES)]


# ---------------------------------------------------------------- B3, capas congeladas e historia
def ct08(fx, c):
    fx.git('rm', '-q', '-r', '--', *B3_DIRS)
    fx.commit('B cerrada sin la capa de B3')
    return [probe(fx, {'INT', 'ALC'} | FROZEN_GATES, says={'INT': 'capa B3'})]


def ct09(fx, c):
    tree = fx.text('rev-parse', B3_ANCHOR + '^{tree}')
    substitute = commit_tree(fx, tree, [B3_TRANSITION], 'B3 sustituida por otro commit con el mismo árbol')
    merge = commit_tree(fx, fx.text('rev-parse', BASE + '^{tree}'), [B3_BASE, substitute], 'integración reconstruida')
    replay(fx, closure_commits(fx), merge, 'cierre reconstruido sobre otra B3')
    return [probe(fx, {'CTX', 'INT', 'FRZ', 'GOV', 'B3G'}, says={'CTX': BASE[:12], 'INT': B3_ANCHOR[:12]})]


def ct10(fx, c):
    top = replay(fx, closure_commits(fx), BASE, 'historia del cierre reconstruida')
    return [probe(fx, {'GOV'}, says={'GOV': 'registrada'},
                  check=lambda info: None if anchor(info) == top and top != c['completion'] else
                  f'el ancla derivada ({anchor(info)}) no distingue la historia reconstruida ({top[:12]})')]


def ct11(fx, c):
    fx.write(B2_DOC, fx.read(B2_DOC) + b'\nalterado tras el cierre\n')
    fx.commit('altera una capa congelada de B2', B2_DOC)
    return [probe(fx, {'INT', 'ALC', 'B3G', 'R2A'}, says={'INT': 'capa B2 '})]


def ct29(fx, c):
    fx.write(PIPELINE, fx.read(PIPELINE) + b'\n# alterado tras el cierre\n')
    fx.commit('altera el pipeline de B3', PIPELINE)
    return [probe(fx, {'INT', 'B3G', 'ALC'}, says={'INT': 'capa B3'})]


# ---------------------------------------------------------------- riesgos LOW y documento de la capa
def ct12(fx, c):
    lines = fx.read(DOC).decode('utf-8').split('\n')
    kept = [ln for ln in lines if not ln.startswith(LOW_ROW)]
    if len(kept) != len(lines) - 1:
        raise Failure('la fila del riesgo B3-AF-L02 no aparece exactamente una vez')
    fx.write(DOC, '\n'.join(kept).encode('utf-8'))
    fx.commit('elimina un riesgo LOW registrado', DOC)
    return [probe(fx, {'LOW', 'FRZ'}, says={'LOW': 'B3-AF-L02'})]


def ct30(fx, c):
    fx.write(DOC, fx.read(DOC) + 'El motor recomendará qué candidatos continúan.\n'.encode('utf-8'))
    fx.commit('el documento afirma una capacidad prohibida', DOC)
    return [probe(fx, {'SEM', 'FRZ'})]


def ct31(fx, c):
    edit(fx, DOC, LIMIT.encode('utf-8'), b'', 'el documento pierde un límite del cierre')
    return [probe(fx, {'SEM', 'FRZ'})]


def ct27(fx, c):
    fx.write(TESTS, fx.read(TESTS) + b'\nimport sqlite3  # noqa: E402\n')
    fx.commit('la batería importa un módulo no autorizado', TESTS)
    return [probe(fx, {'DEP', 'FRZ'})]


def ct28(fx, c):
    fx.write(TESTS, fx.read(TESTS) + b"\n_SIN_USO = eval('1')\n")
    fx.commit('la batería ejecuta código dinámico', TESTS)
    return [probe(fx, {'DEP', 'FRZ'})]


# ---------------------------------------------------------------- sobredeclaración en el gobierno
GOVERNANCE_ATTACKS = {
    'CT13': ('- F36–F40 = BLOQUEADAS', '- F36–F40 = HABILITADAS'),
    'CT14': ('- F35-SBX = HABILITADA', '- F35-SBX = CERRADA'),
    'CT15': ('- G0 real = NO APROBADA', '- G0 real = APROBADA'),
    'CT16': ('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO'),
    'CT17': ('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS'),
}


def attack(cid):
    def setup(fx, c):
        old, new = GOVERNANCE_ATTACKS[cid]
        gov_replace(fx, [(old, new)], f'{cid}: el gobierno sobredeclara un estado que el cierre no cambia')
        return [probe(fx, {'GOV', 'SEM'} | FROZEN_GATES)]
    setup.__name__ = cid.lower()
    return setup


def ct18(fx, c):
    edit(fx, TRACEABILITY, '(**humana**)'.encode('utf-8'), '(**automática**)'.encode('utf-8'),
         'la matriz de trazabilidad cambia RF-23')
    return [probe(fx, {'MAT', 'ALC', 'B3G', 'R2A'})]


def ct19(fx, c):
    gov_replace(fx, [('RF-29 sigue experimental/informativa', 'RF-29 deja de ser experimental')],
                'el gobierno cambia RF-29')
    return [probe(fx, {'GOV', 'SEM'}, says={'SEM': 'RF-29'})]


# ---------------------------------------------------------------- alcance
def ct20(fx, c):
    fx.write(RUNTIME, fx.read(RUNTIME) + b'\n// alterado\n')
    fx.commit('modifica el runtime', RUNTIME)
    return [probe(fx, {'ALC', 'MAT', 'B3G', 'R2A'})]


def ct21(fx, c):
    fx.write('docs/academico/nota_sin_seguimiento.md', b'Nota sin seguimiento.\n')
    return [probe(fx, {'ALC', 'B3G', 'R2A', 'MAT'})]


# ---------------------------------------------------------------- entorno de Git, historia y contexto
def ct22(fx, c):
    fx.git('update-index', '--assume-unchanged', '--', 'CLAUDE.md')
    return [probe(fx, {'FLG'} | FROZEN_GATES)]


def ct23(fx, c):
    clean = fx.sibling('ct23-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    return [probe(fx, {'ENT'}, env=hostile)]


def ct24(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, RULES - {'FLG', 'DEP'}, scenario=shallow, why='el clon no es superficial')]


ct24.depth = 1


def ct32(fx, c):
    readme = fx.text('rev-parse', 'HEAD:README.md')
    other = fx.git('hash-object', '-w', '--stdin', data=b'README reemplazado\n').decode('ascii').strip()
    fx.git('replace', readme, other)
    return [probe(fx, {'ENT', 'B3G', 'R2A'})]


def ct33(fx, c):
    fx.git('checkout', '-q', '--detach', 'HEAD')
    return [probe(fx, {'CTX'} | FROZEN_GATES)]


def ct34(fx, c):
    fx.git('checkout', '-q', '-b', 'feature/otra-rama', 'HEAD')
    return [probe(fx, {'CTX'} | FROZEN_GATES)]


CASES = (
    ('CT01', 'estado válido', (ct01,)),
    ('CT02', 'merge --no-ff en develop y de develop en main', (ct02,)),
    ('CT03', 'commit posterior sin cambios de contenido', (ct03,)),
    ('CT04', 'séptimo blob de gobierno tras la transición', (ct04,)),
    ('CT05', 'modificar → restaurar el gobierno tras la transición', (ct05,)),
    ('CT06', 'vuelta al gobierno de B3 en las tres rutas', (ct06,)),
    ('CT07', 'reapertura de F35-SBX-B en el estado vigente', (ct07,)),
    ('CT08', 'B declarada cerrada sin la capa de B3', (ct08,)),
    ('CT09', 'B3 sustituida por otro commit con el mismo árbol', (ct09,)),
    ('CT10', 'historia del cierre reconstruida con el mismo contenido', (ct10,)),
    ('CT11', 'capa congelada de B2 alterada tras el cierre', (ct11,)),
    ('CT12', 'riesgo LOW eliminado del documento', (ct12,)),
    ('CT13', 'gobierno que habilita F36–F40', (attack('CT13'),)),
    ('CT14', 'gobierno que cierra F35-SBX', (attack('CT14'),)),
    ('CT15', 'gobierno que aprueba la G0 real', (attack('CT15'),)),
    ('CT16', 'gobierno que habilita el alcance C', (attack('CT16'),)),
    ('CT17', 'gobierno que permite datos reales', (attack('CT17'),)),
    ('CT18', 'matriz de trazabilidad con RF-23 alterado', (ct18,)),
    ('CT19', 'gobierno que cambia RF-29', (ct19,)),
    ('CT20', 'runtime modificado y confirmado', (ct20,)),
    ('CT21', 'archivo sin seguimiento en el árbol de trabajo', (ct21,)),
    ('CT22', 'assume-unchanged en el gobierno', (ct22,)),
    ('CT23', 'GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE presentes', (ct23,)),
    ('CT24', 'clon superficial', (ct24,)),
    ('CT25', 'transición repartida en dos commits', (ct25,)),
    ('CT26', 'transición hecha en un merge', (ct26,)),
    ('CT27', 'la batería importa un módulo no autorizado', (ct27,)),
    ('CT28', 'la batería ejecuta código dinámico', (ct28,)),
    ('CT29', 'pipeline de B3 alterado tras el cierre', (ct29,)),
    ('CT30', 'el documento afirma una capacidad prohibida', (ct30,)),
    ('CT31', 'el documento pierde un límite del cierre', (ct31,)),
    ('CT32', 'objeto de reemplazo en refs/replace', (ct32,)),
    ('CT33', 'HEAD separado', (ct33,)),
    ('CT34', 'rama no permitida', (ct34,)),
    ('CT35', 'F35-SBX-B cerrada con B3 aún implementada', (ct35,)),
    ('CT36', 'ACADEMIC_BASELINE.md devuelto a F35-SBX-B no iniciada', (ct36,)),
)


def context(base, env):
    """HEAD probado y commit que completa la capa en su historia (el primero posterior a BASE que contiene sus tres
    archivos)."""
    head = run_git(['rev-parse', '--verify', 'HEAD^{commit}'], base, env).decode('utf-8').strip()
    completion = None
    for commit in run_git(['rev-list', '--reverse', '--ancestry-path', f'{BASE}..{head}'], base,
                          env).decode('ascii').split():
        names = set(run_git(['ls-tree', '-r', '--name-only', '-z', commit, '--', LAYER_DOCS, LAYER_TOOLS],
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
        print('test_f35sbxb_cierre_terminal: 0 casos correctos, 1 fallas (preparación no ejecutable)')
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
    print(f'test_f35sbxb_cierre_terminal: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del gate)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
