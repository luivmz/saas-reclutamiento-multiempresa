"""F35-SBX-B — batería del gate sucesor de B3 (test_f35sbxb3.py).

Uso:  python -I docs/academico/tools/f35sbxb3/test_f35sbxb3.py [CB01 ...]   (sin -I, se relanza)

Fija en RED el gate de B3: los estados legítimos (la rama, los merges --no-ff en develop y en main, un commit vacío), la
transición única y monotónica en cinco etapas, la integridad de las capas congeladas, los ataques al pipeline (un paso
omitido, reordenado o alterado, procedencia, hash o conteo incorrectos, tenant o escenario cruzados, informe no
determinista, purga falsa, resultado parcial presentado como completo, campo de puntaje, importación no autorizada), el
alcance, la sobredeclaración en el gobierno y el entorno de Git hostil o incompleto.

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en
CB43, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta allí el gate con
python -I. Pasa si fallan exactamente las reglas esperadas y, cuando se indica, si las líneas FALLA o INFO contienen el
motivo esperado. Los ataques al pipeline insertan su código justo antes de la guarda __main__ del pipeline. El
repositorio original no se modifica.
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
R2A_COMPLETION = 'ad193f9565bf23246fadb9f85fc0ceddf8ddf698'       # registro del cierre formal de B2: ancla aprobada
BASE = 'ca36875938eca035c97205921ec5f9633381c571'                 # su integración en develop; base de B3
MAIN_MERGE = '8a00505c8a8adc6ebd125f3b30d3cf97dc03b475'           # su integración en main
BRANCH = 'feature/f35-sbx-b3-deterministic-pipeline'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md')
LAYER_TOOLS = 'docs/academico/tools/f35sbxb3'
DOC = 'docs/academico/evidencia-sbx-b3/F35SBXB_B3_Pipeline.md'
PIPELINE = LAYER_TOOLS + '/sbxb_pipeline.py'
PIPELINE_TESTS = LAYER_TOOLS + '/test_sbxb_pipeline.py'
GATE = LAYER_TOOLS + '/validate_f35sbxb3.py'
TESTS = LAYER_TOOLS + '/test_f35sbxb3.py'
LAYER_FILES = (DOC, PIPELINE, PIPELINE_TESTS, GATE, TESTS)
B2_TOOLS = 'docs/academico/tools/f35sbxb2'        # el almacén se deriva de Git: ningún .py ajeno nombra el módulo
R2A_GATE = 'docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py'
GC_DOC = 'docs/academico/evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md'
A_FIXTURE = 'docs/academico/evidencia-sbx/fixtures/ORG-S1_evidencias.json'
DEPENDENCY = 'composer.json'
RUNTIME = 'routes/web.php'
B3_STATE = 'B3 (pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA'
B3_HEADER = 'B3 IMPLEMENTADA).'
MAIN_GUARD = "if __name__ == '__main__':\n"
PIPE_RULES = frozenset({'PIP', 'DET', 'CNF', 'PUR', 'TSB', 'FAL'})
RULES = frozenset({'ENT', 'CTX', 'ANC', 'HIS', 'R2A', 'MAT', 'INT', 'FLG', 'GOV', 'SEM', 'ALC', 'FRZ', 'DEP'}) | PIPE_RULES
SUMMARY = 'validate_f35sbxb3: '
STAMP = '2026-10-19T00:00:00+00:00'
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
    path = os.path.join(base, f'f35sbxb3cb-{label}-{os.getpid()}-{_COUNTER[0]}')
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
                'GIT_AUTHOR_NAME': 'fixture-b3', 'GIT_AUTHOR_EMAIL': 'fixture-b3',
                'GIT_COMMITTER_NAME': 'fixture-b3', 'GIT_COMMITTER_EMAIL': 'fixture-b3',
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
        parents = ['-p', parent]
        if k == merge_step:
            side = fx.text('commit-tree', fx.text('rev-parse', parent + '^{tree}'), '-p', parent, '-m', 'rama lateral')
            parents += ['-p', side]
        parent = fx.text('commit-tree', tree, *parents, '-m', f'paso {k + 1} de la historia reconstruida')
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


def patch_pipeline(fx, code, message=None):
    """Inserta código justo antes de la guarda __main__ del pipeline; con message, lo confirma."""
    data = fx.read(PIPELINE).decode('utf-8')
    if data.count(MAIN_GUARD) != 1:
        raise Failure('el pipeline no tiene exactamente una guarda __main__')
    fx.write(PIPELINE, data.replace(MAIN_GUARD, code.strip('\n') + '\n\n\n' + MAIN_GUARD).encode('utf-8'))
    if message:
        fx.commit(message, PIPELINE)


# ---------------------------------------------------------------- estados legítimos
def cb01(fx, c):
    return [probe(fx, set(), check=lambda info: None if anchor(info) == c['completion'] else
                  f'ancla derivada {anchor(info)} distinta del commit que completa la capa {c["completion"]}')]


def cb02(fx, c):
    if not fx.has(MAIN_MERGE):
        return [probe(fx, set(), scenario=False, why=f'el merge de main {MAIN_MERGE[:12]} no está en los objetos')]
    fx.git('checkout', '-q', '-b', 'develop', BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de B3 en develop', BRANCH)
    out = [probe(fx, set(), label='develop (ca36875) tras el merge')]
    fx.git('checkout', '-q', '-b', 'main', MAIN_MERGE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    out.append(probe(fx, set(), label='main (8a00505) tras el merge'))
    return out


def cb03(fx, c):
    fx.git('commit', '-q', '--allow-empty', '-m', 'commit posterior sin cambios de contenido')
    return [probe(fx, set())]


# ---------------------------------------------------------------- monotonía de la transición
def cb04(fx, c):
    fx.write('CLAUDE.md', fx.read('CLAUDE.md') + b'\nLinea fuera del delta cerrado.\n')
    fx.commit('sexto blob de gobierno', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def cb05(fx, c):
    original = fx.read('CLAUDE.md')
    fx.write('CLAUDE.md', original + b'\nLinea temporal.\n')
    fx.commit('modifica el gobierno', 'CLAUDE.md')
    fx.write('CLAUDE.md', original)
    fx.commit('lo restaura', 'CLAUDE.md')
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 3'})]


def cb06(fx, c):
    for rel in GOV_PATHS:
        fx.write(rel, fx.git('cat-file', 'blob', f'{BASE}:{rel}'))
    fx.commit('vuelve al gobierno del cierre formal: sin B3', *GOV_PATHS)
    return [probe(fx, {'GOV', 'SEM', 'ALC'}, says={'GOV': 'regla 3', 'SEM': 'B3'})]


def cb07(fx, c):
    gov_replace(fx, [(B3_STATE, B3_STATE.replace('IMPLEMENTADA', 'CERRADA')),
                     (B3_HEADER, B3_HEADER.replace('IMPLEMENTADA', 'CERRADA'))], 'el gobierno declara B3 cerrada')
    return [probe(fx, {'GOV', 'SEM'}, says={'SEM': 'B3'})]


def cb08(fx, c):
    top = rebuild(fx, [(DOC, PIPELINE_TESTS, TESTS), GOV_PATHS, (PIPELINE, GATE)])
    return [probe(fx, {'GOV'}, says={'GOV': 'registrada'},
                  check=lambda info: None if anchor(info) == top and top != c['completion'] else
                  f'el ancla derivada ({anchor(info)}) no distingue la historia reconstruida ({top[:12]})')]


def cb09(fx, c):
    rebuild(fx, [(PIPELINE_TESTS, TESTS), GOV_PATHS + (DOC,), (PIPELINE, GATE)])
    return [probe(fx, {'GOV'}, says={'GOV': 'otras rutas'})]


def cb10(fx, c):
    rebuild(fx, [(DOC, PIPELINE_TESTS, TESTS), GOV_PATHS, (PIPELINE, GATE)], merge_step=1)
    return [probe(fx, {'GOV'}, says={'GOV': 'un solo padre'})]


def cb11(fx, c):
    rebuild(fx, [(DOC, PIPELINE_TESTS, TESTS), GOV_PATHS[:1], GOV_PATHS[1:], (PIPELINE, GATE)])
    return [probe(fx, {'GOV'}, says={'GOV': 'regla 4'})]


# ---------------------------------------------------------------- integridad de las capas congeladas
def cb12(fx, c):
    fx.write(R2A_GATE, fx.read(R2A_GATE) + b'\n# alterado\n')
    fx.commit('altera el gate de R2-A', R2A_GATE)
    return [probe(fx, {'INT', 'ALC', 'R2A'}, says={'INT': 'capa R2-A'})]


def cb13(fx, c):
    fx.write(c['store'], fx.read(c['store']) + b'\n# alterado\n')
    fx.commit('altera el almacén de B2', c['store'])
    return [probe(fx, {'INT', 'ALC', 'MAT', 'R2A'} | PIPE_RULES, says={'INT': 'capa B2 '})]


def cb14(fx, c):
    original = fx.read(GC_DOC)
    fx.write(GC_DOC, original + b'\nalterado\n')
    fx.commit('modifica el documento del cierre de gobierno', GC_DOC)
    fx.write(GC_DOC, original)
    fx.commit('lo restaura', GC_DOC)
    return [probe(fx, {'INT', 'R2A'})]


def cb15(fx, c):
    raw = fx.read(A_FIXTURE)
    fx.write(A_FIXTURE, raw.replace(b'Menciona', b'menciona', 1))
    return [probe(fx, {'INT', 'ALC', 'MAT', 'R2A'} | PIPE_RULES, says={'INT': 'capa A'})]


# ---------------------------------------------------------------- ataques al pipeline (en el disco, sin confirmar)
# Cada ataque desactiva además las comprobaciones propias del pipeline que lo detendrían (check_run, level1, level2,
# check_report, check_scenario, check_receipt o inject): así se prueba que el gate lo rechaza por su cuenta.
PIPELINE_ATTACKS = {
    'CB16': ('STEP_FUNCTIONS[3] = lambda ctx: None\ncheck_run = lambda *a, **k: []\nlevel1 = lambda run, fx: []\n',
             {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB17': ('STEP_FUNCTIONS[3], STEP_FUNCTIONS[4] = STEP_FUNCTIONS[4], STEP_FUNCTIONS[3]\n'
             'check_run = lambda *a, **k: []\nlevel1 = lambda run, fx: []\n', {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB18': ('def _paso7_alterado(ctx):\n'
             "    ctx.mod.append_audit(ctx.store, 'esquema_validado', ctx.at(7))\n"
             'STEP_FUNCTIONS[7] = _paso7_alterado\ncheck_run = lambda *a, **k: []\nlevel1 = lambda run, fx: []\n',
             {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB19': ('_run_tenant_original = run_tenant\n'
             'def run_tenant(*a, **k):\n'
             '    r = _run_tenant_original(*a, **k)\n'
             "    r['tables']['evidence_provenance'][0]['hash_before'] = '0' * 64\n"
             '    return r\n'
             'level1 = lambda run, fx: []\nlevel2 = lambda run: []\n', {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB20': ('_run_tenant_original = run_tenant\n'
             'def run_tenant(*a, **k):\n'
             '    r = _run_tenant_original(*a, **k)\n'
             "    r['tables']['audit_entry'][3]['audit_hash'] = 'f' * 64\n"
             '    return r\n'
             'level2 = lambda run: []\n', {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB21': ('_run_tenant_original = run_tenant\n'
             'def run_tenant(*a, **k):\n'
             '    r = _run_tenant_original(*a, **k)\n'
             "    r['counts']['audit_entry'] = 7\n"
             '    return r\n'
             'level1 = lambda run, fx: []\n', {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB22': ('_run_tenant_original = run_tenant\n'
             'def run_tenant(*a, **k):\n'
             '    r = _run_tenant_original(*a, **k)\n'
             "    if r['synthetic_organization_id'] == 'ORG-S1':\n"
             "        r['synthetic_organization_id'] = 'ORG-S2'\n"
             '    return r\n'
             'level1 = lambda run, fx: []\ncheck_report = lambda report: []\n',
             {'ALC', 'FRZ', 'PIP', 'CNF', 'PUR', 'TSB'}),
    'CB23': ("SCENARIOS['ORG-S1'], SCENARIOS['ORG-S2'] = SCENARIOS['ORG-S2'], SCENARIOS['ORG-S1']\n"
             'check_scenario = lambda org, fx: []\n', {'ALC', 'FRZ', 'CNF', 'TSB'}),
    'CB24': ('_instant_original = instant\n'
             'def instant(start, k, minutes):\n'
             '    return _instant_original(start, k + os.getpid() % 500, minutes)\n', {'ALC', 'FRZ', 'DET', 'FAL', 'TSB'}),
    'CB25': ('def _paso12_falso(ctx):\n'
             "    events = ctx.tables['pipeline_event']\n"
             "    receipt = {'closure_kind': 'purga', 'pipeline_run_id': ctx.run_id,\n"
             "               'synthetic_organization_id': ctx.org, 'final_state': 'completado',\n"
             "               'failed_event': 'no_aplica', 'failed_event_record': 'no_aplica', 'error_code': '',\n"
             "               'last_event_hash': events[-1]['event_hash'],\n"
             "               'counts': {k: len(v) for k, v in ctx.tables.items()}, 'file_backed': False,\n"
             "               'connection': 'CLOSED', 'post_close_check': 'ProgrammingError'}\n"
             "    receipt['observed'] = {'counts': receipt['counts'], 'last_event_hash': receipt['last_event_hash'],\n"
             "                           'final_state': 'completado', 'file_backed': False}\n"
             "    receipt['receipt_hash'] = hashlib.sha256(canon(receipt)).hexdigest()\n"
             '    ctx.receipt = receipt\n'
             "    ctx.post_purge = 'E-PURGADO'\n"
             'STEP_FUNCTIONS[12] = _paso12_falso\n', {'ALC', 'FRZ', 'TSB'}),
    'CB26': ('inject = lambda fault, org, k: None\n', {'ALC', 'FRZ', 'FAL', 'TSB'}),
    'CB27': ('_run_tenant_original = run_tenant\n'
             'def run_tenant(*a, **k):\n'
             '    r = _run_tenant_original(*a, **k)\n'
             "    r['score'] = 0\n"
             '    return r\n'
             'check_report = lambda report: []\n', {'ALC', 'FRZ', 'PIP', 'TSB'}),
}


def pipeline_attack(cid):
    def setup(fx, c):
        code, expected = PIPELINE_ATTACKS[cid]
        patch_pipeline(fx, code)
        return [probe(fx, set(expected))]
    setup.__name__ = cid.lower()
    return setup


def cb28(fx, c):
    patch_pipeline(fx, 'import socket\n', 'el pipeline importa un módulo no autorizado')
    return [probe(fx, {'FRZ', 'DEP'})]


# ---------------------------------------------------------------- alcance
def cb29(fx, c):
    name = c['store'].rsplit('/', 1)[1][:-3]
    fx.write('docs/academico/tools/f34/usa_almacen.py', f'import {name}\n'.encode('utf-8'))
    fx.commit('otro módulo del repositorio nombra el almacén', 'docs/academico/tools/f34/usa_almacen.py')
    return [probe(fx, {'ALC', 'DEP', 'MAT', 'R2A'})]


def cb30(fx, c):
    fx.write(DEPENDENCY, fx.read(DEPENDENCY) + b'\n')
    fx.commit('modifica una dependencia', DEPENDENCY)
    return [probe(fx, {'ALC', 'MAT', 'R2A'})]


def cb31(fx, c):
    fx.write(RUNTIME, fx.read(RUNTIME) + b'\n// alterado\n')
    fx.commit('modifica el runtime', RUNTIME)
    return [probe(fx, {'ALC', 'MAT', 'R2A'})]


def cb32(fx, c):
    fx.write(LAYER_TOOLS + '/almacen.sqlite', b'SQLite format 3\x00')
    return [probe(fx, {'ALC', 'FRZ', 'MAT', 'R2A'})]


def cb33(fx, c):
    fx.write(LAYER_TOOLS + '/__pycache__/sbxb_pipeline.cpython-312.pyc', b'\x00artefacto ignorado\x00')
    return [probe(fx, {'ALC', 'FRZ'}, scenario=fx.hidden(), why='git status muestra el artefacto')]


# ---------------------------------------------------------------- sobredeclaración en el gobierno
GOVERNANCE_ATTACKS = {
    'CB34': ('- G0 real = NO APROBADA', '- G0 real = APROBADA'),
    'CB35': ('- G0-SBX = APROBADA CON RESTRICCIONES', '- G0-SBX = APROBADA SIN RESTRICCIONES'),
    'CB36': ('- ADR-005 = PROPUESTA', '- ADR-005 = APROBADA'),
    'CB37': ('- F36–F40 = BLOQUEADAS', '- F36–F40 = DESBLOQUEADAS'),
    'CB38': ('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO'),
    'CB39': ('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS'),
    'CB40': ('Sin scoring, recomendación ni selección automática;',
             'Se habilita el scoring de personas, la recomendación y la selección automática;'),
    'CB41': ('F35-SBX-B INICIADA solo como sandbox sintético', 'F35-SBX-B CERRADA solo como sandbox sintético'),
    'CB42': ('- F35-SBX = HABILITADA', '- F35-SBX = CERRADA'),
}


def attack(cid):
    def setup(fx, c):
        old, new = GOVERNANCE_ATTACKS[cid]
        gov_replace(fx, [(old, new)], f'{cid}: el gobierno sobredeclara un estado que B3 no cambia')
        return [probe(fx, {'GOV', 'SEM', 'MAT', 'R2A'})]
    setup.__name__ = cid.lower()
    return setup


# ---------------------------------------------------------------- entorno de Git, historia y contexto
def cb43(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, RULES - {'FLG', 'DEP'}, scenario=shallow, why='el clon no es superficial')]


cb43.depth = 1


def cb44(fx, c):
    clean = fx.sibling('cb44-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    return [probe(fx, {'ENT'}, env=hostile)]


def cb45(fx, c):
    fx.git('update-index', '--skip-worktree', '--', 'CLAUDE.md')
    fx.write('CLAUDE.md', fx.read('CLAUDE.md') + b'\noculto\n')
    return [probe(fx, {'GOV', 'FLG', 'MAT', 'R2A'}, scenario=fx.hidden(), why='git status lo muestra')]


def cb46(fx, c):
    fx.git('checkout', '-q', '--detach', 'HEAD')
    return [probe(fx, {'CTX', 'MAT', 'R2A'})]


def cb47(fx, c):
    tree = fx.text('rev-parse', 'HEAD^{tree}')
    top = fx.text('commit-tree', tree, '-p', R2A_COMPLETION, '-m', 'B3 sin la integración de R2-A')
    fx.git('checkout', '-q', '-f', '-B', BRANCH, top)
    return [probe(fx, {'CTX', 'GOV', 'FRZ'}, says={'CTX': BASE[:12]})]


CASES = (
    ('CB01', 'estado válido', (cb01,)),
    ('CB02', 'merge --no-ff en develop y de develop en main', (cb02,)),
    ('CB03', 'commit posterior sin cambios de contenido', (cb03,)),
    ('CB04', 'sexto blob de gobierno tras la transición', (cb04,)),
    ('CB05', 'modificar → restaurar el gobierno tras la transición', (cb05,)),
    ('CB06', 'vuelta al gobierno del cierre formal', (cb06,)),
    ('CB07', 'gobierno que declara B3 cerrada', (cb07,)),
    ('CB08', 'historia reconstruida con el mismo contenido', (cb08,)),
    ('CB09', 'transición que también cambia otra ruta', (cb09,)),
    ('CB10', 'transición hecha en un merge', (cb10,)),
    ('CB11', 'transición repartida en dos commits', (cb11,)),
    ('CB12', 'gate de R2-A alterado y confirmado', (cb12,)),
    ('CB13', 'almacén de B2 alterado y confirmado', (cb13,)),
    ('CB14', 'modificar → restaurar el documento del cierre de gobierno', (cb14,)),
    ('CB15', 'fixture de A alterado en el árbol de trabajo', (cb15,)),
    ('CB16', 'pipeline que omite un paso', (pipeline_attack('CB16'),)),
    ('CB17', 'pipeline que reordena dos pasos', (pipeline_attack('CB17'),)),
    ('CB18', 'pipeline que altera la auditoría de un paso', (pipeline_attack('CB18'),)),
    ('CB19', 'pipeline que informa una procedencia incorrecta', (pipeline_attack('CB19'),)),
    ('CB20', 'pipeline que altera la cadena de auditoría', (pipeline_attack('CB20'),)),
    ('CB21', 'pipeline que informa un conteo incorrecto', (pipeline_attack('CB21'),)),
    ('CB22', 'pipeline que cruza tenants', (pipeline_attack('CB22'),)),
    ('CB23', 'pipeline que cruza escenarios', (pipeline_attack('CB23'),)),
    ('CB24', 'pipeline no determinista', (pipeline_attack('CB24'),)),
    ('CB25', 'pipeline con purga falsa', (pipeline_attack('CB25'),)),
    ('CB26', 'pipeline que presenta un resultado parcial como completo', (pipeline_attack('CB26'),)),
    ('CB27', 'pipeline con un campo de puntaje en el informe', (pipeline_attack('CB27'),)),
    ('CB28', 'pipeline que importa un módulo no autorizado, confirmado', (cb28,)),
    ('CB29', 'otro módulo del repositorio nombra el almacén', (cb29,)),
    ('CB30', 'dependencia modificada y confirmada', (cb30,)),
    ('CB31', 'runtime modificado y confirmado', (cb31,)),
    ('CB32', 'base SQLite sin seguimiento en la carpeta de B3', (cb32,)),
    ('CB33', 'artefacto ignorado en la carpeta de B3', (cb33,)),
    ('CB34', 'gobierno que declara G0 real aprobada', (attack('CB34'),)),
    ('CB35', 'gobierno que quita las restricciones de G0-SBX', (attack('CB35'),)),
    ('CB36', 'gobierno que aprueba ADR-005', (attack('CB36'),)),
    ('CB37', 'gobierno que desbloquea F36–F40', (attack('CB37'),)),
    ('CB38', 'gobierno que habilita el alcance C', (attack('CB38'),)),
    ('CB39', 'gobierno que permite datos reales', (attack('CB39'),)),
    ('CB40', 'gobierno que admite puntajes y selección automática de personas', (attack('CB40'),)),
    ('CB41', 'gobierno que declara F35-SBX-B cerrada', (attack('CB41'),)),
    ('CB42', 'gobierno que declara F35-SBX cerrada', (attack('CB42'),)),
    ('CB43', 'clon superficial', (cb43,)),
    ('CB44', 'GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE presentes', (cb44,)),
    ('CB45', 'skip-worktree en el gobierno con un cambio que git status no ve', (cb45,)),
    ('CB46', 'HEAD separado', (cb46,)),
    ('CB47', 'B3 sin el merge de integración de R2-A', (cb47,)),
)


def context(base, env):
    """HEAD probado, módulo del almacén de B2 (el único .py de su carpeta que no es el gate), derivado de Git, y commit
    que completa la capa en su historia (el primero posterior a BASE que contiene sus cinco archivos)."""
    head = run_git(['rev-parse', '--verify', 'HEAD^{commit}'], base, env).decode('utf-8').strip()
    names = [x for x in run_git(['ls-tree', '--name-only', '-z', head, B2_TOOLS + '/'], base, env).decode(
        'utf-8').split('\x00') if x]
    store = [x for x in names if x.endswith('.py') and not x.rsplit('/', 1)[1].startswith('validate_')]
    if len(names) != 2 or len(store) != 1:
        raise Failure(f'precondición: la carpeta de herramientas de B2 no tiene la forma auditada: {names}')
    completion = None
    for commit in run_git(['rev-list', '--reverse', '--ancestry-path', f'{BASE}..{head}'], base,
                          env).decode('ascii').split():
        names = set(run_git(['ls-tree', '-r', '--name-only', '-z', commit, '--', LAYER_TOOLS, DOC.rsplit('/', 1)[0]],
                            base, env).decode('utf-8').split('\x00'))
        if set(LAYER_FILES) <= names:
            completion = commit
            break
    return {'head': head, 'completion': completion, 'store': store[0]}


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
        print('test_f35sbxb3: 0 casos correctos, 1 fallas (preparación no ejecutable)')
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
    print(f'test_f35sbxb3: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del gate)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
