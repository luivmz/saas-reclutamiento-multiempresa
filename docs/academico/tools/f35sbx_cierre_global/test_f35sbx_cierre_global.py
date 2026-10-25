"""F35-SBX — batería del gate sucesor del cierre global (test_f35sbx_cierre_global.py).

Uso:  python -I docs/academico/tools/f35sbx_cierre_global/test_f35sbx_cierre_global.py [GC01 ...]
      (sin -I, se relanza)

Fija en RED el gate del cierre global de F35-SBX: los estados legítimos (la rama, los merges --no-ff en develop y en
main, un commit vacío), la transición única y monotónica en las cuatro rutas de gobierno, la reapertura y la
sobredeclaración (F35-SBX, F36–F40, F36-SBX, G0 real, alcance C, datos reales y RF-29), la integridad de A y de B, el
runtime y el dataset, los archivos físicos que Git ignora en las superficies materiales (GC-AF-M01), los riesgos
registrados, el documento de la capa, el alcance, el código de la capa y el entorno de Git hostil o incompleto.

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en
GC24, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta allí el gate con
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
TC_ANCHOR = '9ebb90929f34079b42e88e21e144f80182ba7565'          # cierre terminal de F35-SBX-B
BASE = 'f082b4165ca756659b998716e2647494a3ec7be6'               # integración del cierre terminal en develop; base
MAIN_MERGE = '57eeb5329c7ef5cc3fa219918536400fcb846570'         # integración del cierre terminal en main
BRANCH = 'chore/f35-sbx-global-closure'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md', 'README.md')
LAYER_DOCS = 'docs/academico/evidencia-sbx-cierre-global'
LAYER_TOOLS = 'docs/academico/tools/f35sbx_cierre_global'
DOC = LAYER_DOCS + '/F35SBX_Cierre_Global.md'
GATE = LAYER_TOOLS + '/validate_f35sbx_cierre_global.py'
TESTS = LAYER_TOOLS + '/test_f35sbx_cierre_global.py'
FIX_DOC = LAYER_DOCS + '/F35SBX_Cierre_Global_GC-AF-M01.md'
LAYER_FILES = (DOC, GATE, TESTS, FIX_DOC)
A_FILE = 'docs/academico/evidencia-sbx/README.md'
TC_GATE = 'docs/academico/tools/f35sbxb_cierre_terminal/validate_f35sbxb_cierre_terminal.py'
RUNTIME = 'routes/web.php'
DATASET = 'docs/academico/datos-sinteticos/dataset/organizations.csv'
GC_RECORD = 'F35-SBX está CERRADA Y CONGELADA, con su cierre global registrado en '
GC_F36 = 'ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza.'
README_STATE = ('F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A y F35-SBX-B cerradas e '
                'integradas, con su cierre global registrado en [`evidencia-sbx-cierre-global`]'
                '(docs/academico/evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md).')
RF_STATE = 'RF-23 sigue humana; RF-29 sigue experimental/informativa.'
LOW_ROW = '| B3-AF-L02 | LOW |'
INFO_ROW = '| TC-AF-I01 | INFO |'
LIMIT = '- no permite la selección automática;\n'
RULES = frozenset({'ENT', 'CTX', 'ANC', 'INT', 'FLG', 'GOV', 'SEM', 'SBX', 'FSY', 'RSK', 'ALC', 'FRZ', 'DEP'})
SUMMARY = 'validate_f35sbx_cierre_global: '
STAMP = '2026-10-24T00:00:00+00:00'
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
    path = os.path.join(base, f'f35sbxgc-{label}-{os.getpid()}-{_COUNTER[0]}')
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
                'GIT_AUTHOR_NAME': 'fixture-gc', 'GIT_AUTHOR_EMAIL': 'fixture-gc',
                'GIT_COMMITTER_NAME': 'fixture-gc', 'GIT_COMMITTER_EMAIL': 'fixture-gc',
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

    def has(self, oid):
        return subprocess.run(['git', 'cat-file', '-e', oid + '^{commit}'], cwd=self.root, env=self.env,
                              capture_output=True).returncode == 0

    def validate(self, extra_env=None):
        """(reglas en falla, INFO por regla, líneas FALLA por regla, resumen) del gate, o (None, {}, {}, motivo) si no
        terminó con un resumen coherente."""
        RUNS[0] += 1
        gate = self.path(GATE)
        if not os.path.isfile(gate):
            return None, {}, {}, 'el gate del cierre global no existe en HEAD'
        try:
            p = subprocess.run([sys.executable, '-I', '-B', gate], cwd=self.root,
                               env=dict(self.env, **(extra_env or {})), capture_output=True, timeout=3600)
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
def gc01(fx, c):
    return [probe(fx, set(), check=lambda info: None if anchor(info) == c['completion'] else
                  f'ancla derivada {anchor(info)} distinta del commit que completa la capa {c["completion"]}')]


def gc02(fx, c):
    if not fx.has(MAIN_MERGE):
        return [probe(fx, set(), scenario=False, why=f'el merge de main {MAIN_MERGE[:12]} no está en los objetos')]
    fx.git('checkout', '-q', '-b', 'develop', BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff del cierre global en develop', BRANCH)
    out = [probe(fx, set(), label='develop (f082b41) tras el merge')]
    fx.git('checkout', '-q', '-b', 'main', MAIN_MERGE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    out.append(probe(fx, set(), label='main (57eeb53) tras el merge'))
    return out


def gc03(fx, c):
    fx.git('commit', '-q', '--allow-empty', '-m', 'commit posterior sin cambios de contenido')
    return [probe(fx, set())]


# ---------------------------------------------------------------- monotonía de la transición
def gc04(fx, c):
    fx.write('CLAUDE.md', fx.read('CLAUDE.md') + b'\nLinea fuera del delta cerrado.\n')
    fx.commit('otro blob de gobierno', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def gc05(fx, c):
    original = fx.read('CLAUDE.md')
    fx.write('CLAUDE.md', original + b'\nCambio temporal.\n')
    fx.commit('modifica el gobierno', 'CLAUDE.md')
    fx.write('CLAUDE.md', original)
    fx.commit('restaura el gobierno', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 4'})]


def gc06(fx, c):
    for rel in GOV_PATHS:
        fx.write(rel, fx.git('cat-file', 'blob', f'{BASE}:{rel}'))
    fx.commit('vuelve al gobierno del cierre terminal', *GOV_PATHS)
    return [probe(fx, {'GOV', 'SEM', 'ALC'})]


# ---------------------------------------------------------------- reapertura y sobredeclaración en el gobierno
ATTACKS = {
    'GC07': (GC_RECORD, 'F35-SBX está REABIERTA, con su cierre global registrado en '),
    'GC08': ('- F36–F40 = BLOQUEADAS', '- F36–F40 = HABILITADAS'),
    'GC09': (GC_F36, 'F36-SBX queda INICIADA.'),
    'GC10': ('- G0 real = NO APROBADA', '- G0 real = APROBADA'),
    'GC11': ('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO'),
    'GC12': ('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS'),
    'GC34': (README_STATE, 'F35-SBX exclusivamente sintético. F35-SBX AÚN NO INICIADA.'),
    'GC35': (RF_STATE, 'RF-23 sigue humana; RF-29 pasa a productivo.'),
}


def attack(cid):
    def run(fx, c):
        gov_replace(fx, [ATTACKS[cid]], f'gobierno alterado ({cid})')
        return [probe(fx, {'GOV', 'SEM'})]
    return run


# ---------------------------------------------------------------- integridad de A y de B, runtime y dataset
def gc13(fx, c):
    fx.write(A_FILE, fx.read(A_FILE) + b'\nalterado tras el cierre\n')
    fx.commit('altera F35-SBX-A', A_FILE)
    return [probe(fx, {'INT', 'ALC'}, says={'INT': 'capa A'})]


def gc14(fx, c):
    fx.write(TC_GATE, fx.read(TC_GATE) + b'\n# alterado tras el cierre\n')
    fx.commit('altera el gate del cierre terminal', TC_GATE)
    return [probe(fx, {'INT', 'ALC'}, says={'INT': 'capa B'})]


def gc15(fx, c):
    fx.write(RUNTIME, fx.read(RUNTIME) + b'\n// alterado\n')
    fx.commit('modifica el runtime', RUNTIME)
    return [probe(fx, {'ALC', 'SBX', 'FSY'}, says={'SBX': 'SBX-16'})]


def gc16(fx, c):
    edit(fx, DATASET, b'ORG-S2,synthetic,', b'ORG-S2,real,', 'altera el dataset sintético')
    return [probe(fx, {'ALC', 'SBX', 'FSY'})]


# ---------------------------------------------------------------- riesgos y documento de la capa
def gc17(fx, c):
    data = fx.read(DOC)
    lines = [ln for ln in data.split(b'\n') if not ln.startswith(LOW_ROW.encode('utf-8'))]
    if len(lines) != len(data.split(b'\n')) - 1:
        raise Failure('la fila de B3-AF-L02 no aparece exactamente una vez')
    fx.write(DOC, b'\n'.join(lines))
    fx.commit('elimina un riesgo LOW', DOC)
    return [probe(fx, {'RSK', 'FRZ'})]


def gc18(fx, c):
    data = fx.read(DOC).decode('utf-8')
    rows = [ln for ln in data.split('\n') if ln.startswith(INFO_ROW)]
    if len(rows) != 1 or not rows[0].endswith('| Aceptado, no bloqueante |'):
        raise Failure('la fila de TC-AF-I01 no aparece exactamente una vez con su estado')
    fx.write(DOC, data.replace(rows[0], rows[0][:-len('| Aceptado, no bloqueante |')] + '| Descartado |', 1)
             .encode('utf-8'))
    fx.commit('cambia el estado de TC-AF-I01', DOC)
    return [probe(fx, {'RSK', 'FRZ'})]


def gc19(fx, c):
    fx.write(DOC, fx.read(DOC) + 'El motor recomienda candidatos a la Dirección.\n'.encode('utf-8'))
    fx.commit('el documento afirma una capacidad prohibida', DOC)
    return [probe(fx, {'SEM', 'FRZ'})]


def gc20(fx, c):
    edit(fx, DOC, LIMIT.encode('utf-8'), b'', 'el documento pierde un límite del cierre')
    return [probe(fx, {'SEM', 'FRZ'})]


# ---------------------------------------------------------------- alcance
def gc21(fx, c):
    fx.write('docs/academico/nota_sin_seguimiento.md', b'Nota sin seguimiento.\n')
    return [probe(fx, {'ALC'})]


# ---------------------------------------------------------------- superficies físicas que Git ignora (GC-AF-M01)
def is_ignored(fx, rel):
    try:
        run_git(['check-ignore', '-q', '--', rel], fx.root, fx.env)
        return True
    except Failure:
        return False


def hide(fx, files, exclude=None):
    """Archivos físicos fuera del inventario y ocultos para Git: con exclude, la línea se añade a .git/info/exclude; si
    no, ya los ignora un .gitignore. Exige que git status no muestre nada y que Git los considere ignorados."""
    for rel, data in files:
        fx.write(rel, data)
    if exclude is not None:
        with open(fx.path('.git/info/exclude'), 'ab') as f:
            f.write(exclude.encode('utf-8') + b'\n')
    if fx.git('status', '--porcelain').strip():
        raise Failure('git status muestra el escenario: no está oculto')
    if not all(is_ignored(fx, rel) for rel, _ in files):
        raise Failure('Git no considera ignorados todos los archivos del escenario')


def gc36(fx, c):
    hide(fx, [('app/Support/Interno/registro_local.php', b'<?php\n// inerte\n')], exclude='app/Support/Interno/')
    return [probe(fx, {'FSY'})]


def gc37(fx, c):
    hide(fx, [('public/build/assets/chunk-vendor.js', b'export default 0;\n')])
    return [probe(fx, {'FSY'})]


def gc38(fx, c):
    rel = 'docs/academico/datos-sinteticos/dataset/extra_sintetico.csv'
    hide(fx, [(rel, b'organization_token,source_type,synthetic_record_id\n')], exclude=rel)
    return [probe(fx, {'FSY'})]


def gc39(fx, c):
    hide(fx, [('routes/.local/.gitignore', b'*\n'), ('routes/.local/vacio', b'')])
    return [probe(fx, {'FSY'})]


def gc40(fx, c):
    hide(fx, [('ml-service/src/recruitment_ml/__pycache__/schema.cpython-312.pyc', b'no es bytecode')])
    return [probe(fx, {'FSY'})]


# ---------------------------------------------------------------- entorno de Git, historia y contexto
def gc22(fx, c):
    fx.git('update-index', '--assume-unchanged', '--', 'CLAUDE.md')
    return [probe(fx, {'FLG'})]


def gc23(fx, c):
    clean = fx.sibling('gc23-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    return [probe(fx, {'ENT'}, env=hostile)]


def gc24(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, RULES - {'FLG', 'DEP'}, scenario=shallow, why='el clon no es superficial')]


gc24.depth = 1


def gc25(fx, c):
    readme = fx.text('rev-parse', 'HEAD:README.md')
    other = fx.git('hash-object', '-w', '--stdin', data=b'README reemplazado\n').decode('ascii').strip()
    fx.git('replace', readme, other)
    return [probe(fx, {'ENT'})]


def gc26(fx, c):
    fx.git('checkout', '-q', '--detach', 'HEAD')
    return [probe(fx, {'CTX'})]


def gc27(fx, c):
    fx.git('checkout', '-q', '-b', 'feature/otra-rama', 'HEAD')
    return [probe(fx, {'CTX'})]


def gc28(fx, c):
    rebuild(fx, [GOV_PATHS[:2], GOV_PATHS[2:], LAYER_FILES])
    return [probe(fx, {'GOV'})]


def gc29(fx, c):
    rebuild(fx, [GOV_PATHS, LAYER_FILES], merge_step=0)
    return [probe(fx, {'GOV'})]


def gc30(fx, c):
    replay(fx, closure_commits(fx), BASE, 'historia reconstruida')
    return [probe(fx, {'GOV'}, says={'GOV': 'distinta de la registrada'})]


def gc31(fx, c):
    edit(fx, TESTS, b'import subprocess  # noqa: E402\n', b'import subprocess  # noqa: E402\nimport json  # noqa: E402\n',
         'la batería importa un módulo no autorizado')
    return [probe(fx, {'DEP', 'FRZ'})]


def gc32(fx, c):
    fx.write(TESTS, fx.read(TESTS) + b'\n\ndef _dinamico():\n    return eval("1")\n')
    fx.commit('la batería ejecuta código dinámico', TESTS)
    return [probe(fx, {'DEP', 'FRZ'})]


def gc33(fx, c):
    replay(fx, closure_commits(fx), TC_ANCHOR, 'cierre sin la integración')
    return [probe(fx, {'CTX', 'ANC', 'GOV', 'FRZ'})]


CASES = (
    ('GC01', 'estado válido', (gc01,)),
    ('GC02', 'merge --no-ff en develop y de develop en main', (gc02,)),
    ('GC03', 'commit posterior sin cambios de contenido', (gc03,)),
    ('GC04', 'un blob de gobierno más tras la transición', (gc04,)),
    ('GC05', 'modificar → restaurar el gobierno tras la transición', (gc05,)),
    ('GC06', 'vuelta al gobierno del cierre terminal en las cuatro rutas', (gc06,)),
    ('GC07', 'F35-SBX reabierta en el estado vigente', (attack('GC07'),)),
    ('GC08', 'gobierno que habilita F36–F40', (attack('GC08'),)),
    ('GC09', 'gobierno que inicia F36-SBX', (attack('GC09'),)),
    ('GC10', 'gobierno que aprueba la G0 real', (attack('GC10'),)),
    ('GC11', 'gobierno que habilita el alcance C', (attack('GC11'),)),
    ('GC12', 'gobierno que permite datos reales', (attack('GC12'),)),
    ('GC13', 'F35-SBX-A alterada tras el cierre', (gc13,)),
    ('GC14', 'gate del cierre terminal alterado tras el cierre', (gc14,)),
    ('GC15', 'runtime modificado y confirmado', (gc15,)),
    ('GC16', 'dataset sintético alterado', (gc16,)),
    ('GC17', 'riesgo LOW eliminado del documento', (gc17,)),
    ('GC18', 'TC-AF-I01 con otro estado en el documento', (gc18,)),
    ('GC19', 'el documento afirma una capacidad prohibida', (gc19,)),
    ('GC20', 'el documento pierde un límite del cierre', (gc20,)),
    ('GC21', 'archivo sin seguimiento en el árbol de trabajo', (gc21,)),
    ('GC22', 'assume-unchanged en el gobierno', (gc22,)),
    ('GC23', 'GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE presentes', (gc23,)),
    ('GC24', 'clon superficial', (gc24,)),
    ('GC25', 'objeto de reemplazo en refs/replace', (gc25,)),
    ('GC26', 'HEAD separado', (gc26,)),
    ('GC27', 'rama no permitida', (gc27,)),
    ('GC28', 'transición repartida en dos commits', (gc28,)),
    ('GC29', 'transición hecha en un merge', (gc29,)),
    ('GC30', 'historia del cierre reconstruida con el mismo contenido', (gc30,)),
    ('GC31', 'la batería importa un módulo no autorizado', (gc31,)),
    ('GC32', 'la batería ejecuta código dinámico', (gc32,)),
    ('GC33', 'cierre construido sobre 9ebb909 sin su integración', (gc33,)),
    ('GC34', 'README.md devuelto a F35-SBX AÚN NO INICIADA', (attack('GC34'),)),
    ('GC35', 'gobierno que cambia RF-29', (attack('GC35'),)),
    ('GC36', 'archivo de app/ oculto por .git/info/exclude', (gc36,)),
    ('GC37', 'artefacto de public/build ignorado por .gitignore', (gc37,)),
    ('GC38', 'archivo del dataset oculto por .git/info/exclude', (gc38,)),
    ('GC39', 'carpeta anidada que se ignora a sí misma, con un archivo vacío', (gc39,)),
    ('GC40', '.pyc no derivable en una caché ignorada', (gc40,)),
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
        print('test_f35sbx_cierre_global: 0 casos correctos, 1 fallas (preparación no ejecutable)')
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
    print(f'test_f35sbx_cierre_global: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del gate)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
