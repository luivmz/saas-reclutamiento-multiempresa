"""F35-SBX-B — batería del gate sucesor vigente tras B2-FREEZE (test_f35sbxb2_sucesor.py).

Uso:  python -I docs/academico/tools/f35sbxb2_sucesor/test_f35sbxb2_sucesor.py   (sin -I, se relanza aislado)

Fija en RED la corrección de AF-M01. Sobre HEAD, el gate vigente compone cuatro piezas:

  HIS  el gate de B2 anclado en el candidato;
  CON  la integridad del freeze registrado;
  MAT  la evaluación material del gate de B2, intacto, sobre el estado actual;
  ALC  el alcance exacto del sucesor.

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en AF13,
un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta el gate sucesor con
python -I. Pasa si fallan exactamente las reglas esperadas y, en los casos materiales, si la línea INFO de MAT nombra
las reglas del gate de B2 que detectan el incumplimiento. Las rutas congeladas se derivan de Git. El repositorio
original no se modifica.
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
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'      # B2-FREEZE auditado (AF-M01)
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'      # develop al crear la rama de B2
B1_MAIN = '3fdfdcecdec47b08d99e96968dd915e0e1b9010b'      # main tras integrar B1, con el mismo árbol que 72e86c5
B2_BRANCH = 'feature/f35-sbx-b2-ephemeral-store'
SUCESOR = 'docs/academico/tools/f35sbxb2_sucesor/validate_f35sbxb2_sucesor.py'
B2_GATE = 'docs/academico/tools/f35sbxb2/validate_f35sbxb2.py'
FREEZE_VALIDATOR = 'docs/academico/tools/f35sbxb2_freeze/validate_f35sbxb2_freeze.py'
FREEZE_MANIFEST = 'docs/academico/tools/f35sbxb2_freeze/b2_freeze_manifest.json'
EVIDENCE = 'docs/academico/datos-sinteticos/dataset/evidence.csv'
F34_MANIFEST = 'docs/academico/datos-sinteticos/dataset/manifest.json'
RULES = frozenset({'ENT', 'ANC', 'HIS', 'CON', 'MAT', 'ALC', 'DEP'})
SUMMARY = 'validate_f35sbxb2_sucesor: '
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
    path = os.path.join(base, f'f35sbxb2suc-{label}-{os.getpid()}-{_COUNTER[0]}')
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
                'GIT_AUTHOR_NAME': 'fixture-b2suc', 'GIT_AUTHOR_EMAIL': 'fixture-b2suc',
                'GIT_COMMITTER_NAME': 'fixture-b2suc', 'GIT_COMMITTER_EMAIL': 'fixture-b2suc',
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


def lines_of(stdout):
    return stdout.decode('utf-8', 'replace').splitlines()


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

    def python(self, rel, extra_env=None):
        """Ejecuta un script del clon con python -I y devuelve el proceso terminado."""
        return subprocess.run([sys.executable, '-I', '-B', self.path(rel)], cwd=self.root,
                              env=dict(self.env, **(extra_env or {})), capture_output=True, timeout=3600)

    def validate(self, extra_env=None):
        """(reglas en falla, líneas INFO, resumen) del gate sucesor del clon, o (None, {}, motivo) si no terminó con un
        resumen coherente."""
        RUNS[0] += 1
        try:
            p = self.python(SUCESOR, extra_env)
        except (OSError, subprocess.TimeoutExpired) as e:
            return None, {}, f'el gate sucesor no se pudo ejecutar ({e.__class__.__name__})'
        lines = lines_of(p.stdout)
        summary = [x for x in lines if x.startswith(SUMMARY)]
        failing = {x.split()[1].rstrip(':') for x in lines if x.startswith('FALLA ') and len(x.split()) > 1}
        info = {x.split()[1].rstrip(':'): x for x in lines if x.startswith('INFO ') and len(x.split()) > 1}
        if len(summary) != 1:
            tail = ((p.stdout + p.stderr).decode('utf-8', 'replace').strip().splitlines() or [''])[-1]
            return None, {}, f'el gate sucesor no terminó con su resumen (código {p.returncode}): «{tail[:200]}»'
        if (p.returncode == 0) != (not failing) or not failing <= RULES:
            return None, {}, f'salida incoherente (código {p.returncode}; reglas en falla {sorted(failing)})'
        return failing, info, summary[0]


def mat_rules(info):
    """Reglas del gate de B2 que la línea INFO de MAT nombra en falla."""
    line = info.get('MAT', '')
    if 'reglas en falla: ' not in line:
        return None
    named = line.split('reglas en falla: ', 1)[1].split(';', 1)[0]
    return {x.strip() for x in named.split(',') if x.strip() and x.strip() != 'ninguna'}


def probe(fx, expected, label='', mat=None, scenario=True, why='', env=None, check=None):
    """Una ejecución del gate sucesor frente a las reglas que deben fallar (vacío = PASS). mat: reglas del gate de B2
    que MAT debe nombrar; check: comprobación adicional sobre las líneas INFO, que devuelve un motivo o None."""
    if not scenario:
        return label, expected, None, f'escenario no reproducido: {why}'
    observed, info, detail = fx.validate(env)
    if observed is None:
        return label, expected, None, detail
    if mat is not None and observed == expected:
        named = mat_rules(info)
        if named is None or not mat <= named:
            return label, expected, None, f'MAT no nombra {sorted(mat)} (nombra {sorted(named or [])})'
    if check is not None and observed == expected:
        problem = check(info)
        if problem:
            return label, expected, None, problem
    return label, expected, observed, detail


def b2_gate_direct(fx):
    """El gate de B2 ejecutado directamente sobre el clon: (código, comprobaciones en falla, resumen)."""
    p = fx.python(B2_GATE)
    lines = lines_of(p.stdout)
    failing = [x.split()[1].rstrip(':') for x in lines if x.startswith('FALLA ') and len(x.split()) > 1]
    summary = [x for x in lines if x.startswith('validate_f35sbxb2: ')]
    return p.returncode, failing, summary[0] if len(summary) == 1 else ''


# ---------------------------------------------------------------- casos
def af01(fx, c):
    return [probe(fx, set())]


def af02(fx, c):
    fx.write(EVIDENCE, fx.read(EVIDENCE) + b'\n')
    return [probe(fx, {'MAT', 'ALC'}, mat={'SBX', 'FSY', 'PRE'})]


def _manifest_hash(fx, new_hash=None):
    """Sustituye el SHA-256 de evidence.csv en el manifiesto F34 (una sola aparición) y devuelve el anterior."""
    data = fx.read(F34_MANIFEST)
    old = json.loads(data.decode('utf-8'))['files']['evidence.csv']['sha256']
    new = new_hash or old[:-1] + ('1' if old[-1] != '1' else '2')
    if data.count(old.encode('ascii')) != 1:
        raise Failure('el SHA-256 de evidence.csv no aparece exactamente una vez en el manifiesto F34')
    fx.write(F34_MANIFEST, data.replace(old.encode('ascii'), new.encode('ascii'), 1))
    return old


def af03_hash(fx, c):
    _manifest_hash(fx)
    return [probe(fx, {'MAT', 'ALC'}, label='solo el SHA-256 del manifiesto F34', mat={'SBX', 'FSY', 'STA'})]


def af03_coherent(fx, c):
    data = fx.read(EVIDENCE) + b'\n'
    fx.write(EVIDENCE, data)
    _manifest_hash(fx, hashlib.sha256(data).hexdigest())
    return [probe(fx, {'MAT', 'ALC'}, label='CSV y manifiesto coherentes entre sí', mat={'SBX', 'FSY', 'STA'})]


def af04_store(fx, c):
    path = c['py'][0]   # primer módulo congelado por orden: el almacén
    fx.write(path, fx.read(path) + b'# alterado\n')
    fx.commit('altera el almacén congelado', path)
    return [probe(fx, {'CON', 'ALC'}, label='almacén alterado y confirmado')]


def af04_gate(fx, c):
    fx.write(B2_GATE, fx.read(B2_GATE) + b'# alterado\n')
    return [probe(fx, {'CON', 'MAT', 'ALC'}, label='gate de B2 alterado en el disco',
                  check=lambda info: None if 'no ejecutado' in info.get('MAT', '') else
                  'MAT no declara que el gate alterado quedó sin ejecutar')]


def af05_validator(fx, c):
    fx.write(FREEZE_VALIDATOR, fx.read(FREEZE_VALIDATOR) + b'\n# alterado\n')
    fx.commit('altera el validador del freeze', FREEZE_VALIDATOR)
    return [probe(fx, {'CON'}, label='validador del freeze alterado y confirmado',
                  check=lambda info: None if 'no ejecutado' in info.get('CON', '') else
                  'CON no declara que el validador alterado quedó sin ejecutar')]


def af05_manifest(fx, c):
    data = fx.read(FREEZE_MANIFEST)
    fx.write(FREEZE_MANIFEST, data.replace(b'"B2-FREEZE"', b'"B2-FREEZE-ALTERADO"', 1))
    return [probe(fx, {'CON'}, label='manifiesto del freeze alterado en el disco', scenario=fx.read(FREEZE_MANIFEST) != data,
                  why='el manifiesto no cambió')]


def af06(fx, c):
    path = c['md'][0]
    original = fx.read(path)
    fx.write(path, original + b'\nalterado\n')
    fx.commit('modifica un archivo congelado', path)
    fx.write(path, original)
    fx.commit('lo restaura', path)
    return [probe(fx, {'CON'})]


def af07(fx, c):
    out = []
    fx.git('checkout', '-q', '-b', 'develop', B2_BASE)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama de B2 en develop', B2_BRANCH)
    out.append(probe(fx, set(), label='develop (72e86c5) tras el merge'))
    fx.git('checkout', '-q', '-b', 'main', B1_MAIN)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de develop en main', 'develop')
    out.append(probe(fx, set(), label='main (3fdfdce) tras el merge'))
    return out


def af08(fx, c):
    path = c['md'][1]
    original = fx.read(path)
    fx.git('checkout', '-q', '-b', 'lateral')
    fx.write(path, original + b'\nalterado en una rama lateral\n')
    fx.commit('lateral: altera un archivo congelado', path)
    fx.write(path, original)
    fx.commit('lateral: lo restaura', path)
    fx.git('checkout', '-q', B2_BRANCH)
    fx.git('merge', '-q', '--no-ff', '-m', 'merge --no-ff de la rama lateral', 'lateral')
    return [probe(fx, {'CON'}, scenario=fx.read(path) == original, why='el resultado del merge no parece correcto')]


def af09(fx, c):
    code, failing, summary = b2_gate_direct(fx)
    ok = code == 1 and failing == ['SCP'] and summary.endswith(' 1 fallas')
    first = ('gate de B2 directo', set(), set() if ok else None,
             summary if ok else f'el gate de B2 sobre HEAD limpio no da solo SCP: código {code}, {failing[:5]}')
    return [first, probe(fx, set(), label='gate sucesor')]


def af10(fx, c):
    def check(info):
        his, mat = info.get('HIS', ''), info.get('MAT', '')
        if CANDIDATE not in his or 'código 0;' not in his or ' 0 fallas' not in his:
            return f'HIS no acredita el candidato con código 0 y sin fallas: «{his[:160]}»'
        try:
            total_his = int(his.split('código 0; ', 1)[1].split(' correctas', 1)[0])
            ok_mat = int(mat.split('código 1; ', 1)[1].split(' correctas', 1)[0])
            fail_mat = int(mat.split(' correctas, ', 1)[1].split(' fallas', 1)[0])
        except (IndexError, ValueError):
            return 'totales de HIS y MAT no legibles'
        return None if total_his == ok_mat + fail_mat else f'total histórico {total_his} distinto del de MAT'
    return [probe(fx, set(), check=check)]


def af11(fx, c):
    parent = fx.text('rev-parse', FREEZE + '^')   # el commit RED del freeze: la capa aún no está completa
    top = fx.text('commit-tree', fx.text('rev-parse', 'HEAD^{tree}'), '-p', parent,
                  '-m', 'freeze reconstruido con los mismos bytes en otra historia')
    fx.git('checkout', '-q', '-B', B2_BRANCH, top)
    p = fx.python(FREEZE_VALIDATOR)
    lines = lines_of(p.stdout)
    accepted = p.returncode == 0 and any(f'commit de freeze derivado: {top}' in x for x in lines)
    return [probe(fx, {'ANC', 'CON'}, scenario=accepted, why='el validador del freeze no aprueba la historia reconstruida')]


def af12(fx, c):
    fx.write(EVIDENCE, fx.read(EVIDENCE) + b'\n')
    clean = fx.sibling('af12-limpio')
    hostile = {'GIT_DIR': os.path.join(clean, '.git'), 'GIT_WORK_TREE': clean,
               'GIT_INDEX_FILE': os.path.join(clean, '.git', 'index')}
    steered = subprocess.run(['git', 'diff', '--quiet'], cwd=fx.root, env=dict(fx.env, **hostile),
                             capture_output=True).returncode == 0      # con esas variables, Git no ve el cambio
    return [probe(fx, {'MAT', 'ALC'}, mat={'SBX', 'FSY', 'PRE'}, env=hostile, scenario=steered,
                  why='con esas variables Git sigue viendo el cambio')]


def af13(fx, c):
    shallow = fx.text('rev-parse', '--is-shallow-repository') == 'true'
    return [probe(fx, {'ENT', 'ANC', 'HIS', 'CON', 'MAT', 'ALC'}, scenario=shallow, why='el clon no es superficial')]


af13.depth = 1


def af14(fx, c):
    fx.write('public/build/assets/fixture.js', b'console.log("artefacto generado sin origen verificable");\n')
    hidden = fx.git('status', '--porcelain').strip() == b''         # ignorado: ni git status ni ALC lo ven
    return [probe(fx, {'MAT'}, mat={'FSY'}, scenario=hidden, why='git status muestra el archivo')]

CASES = (
    ('AF01', 'HEAD con el freeze intacto y estado material válido', (af01,)),
    ('AF02', 'LF añadido a evidence.csv', (af02,)),
    ('AF03', 'origen sintético alterado de forma equivalente', (af03_hash, af03_coherent)),
    ('AF04', 'artefacto congelado de B2 alterado', (af04_store, af04_gate)),
    ('AF05', 'capa del freeze alterada', (af05_validator, af05_manifest)),
    ('AF06', 'modificar → restaurar un archivo congelado', (af06,)),
    ('AF07', 'merges --no-ff legítimos en develop y main', (af07,)),
    ('AF08', 'rama lateral que altera y restaura, integrada con merge --no-ff', (af08,)),
    ('AF09', 'estado limpio: el gate de B2 sigue en solo SCP y el sucesor pasa', (af09,)),
    ('AF10', 'el candidato se sigue acreditando con el gate de B2 anclado', (af10,)),
    ('AF11', 'freeze reconstruido con los mismos bytes en otra historia', (af11,)),
    ('AF12', 'evidence.csv alterado con GIT_DIR, GIT_WORK_TREE y GIT_INDEX_FILE hacia un clon limpio', (af12,)),
    ('AF13', 'clon superficial', (af13,)),
    ('AF14', 'artefacto ignorado en una superficie del runtime, invisible para git status y para ALC', (af14,)),
)


def context(base, env):
    """HEAD probado y rutas congeladas derivadas de Git (delta de B2 entre su base y el candidato), por papel."""
    head = run_git(['rev-parse', '--verify', 'HEAD^{commit}'], base, env).decode('utf-8').strip()
    raw = run_git(['diff-tree', '-r', '--no-renames', '--name-status', '-z', B2_BASE, CANDIDATE], base, env).split(b'\x00')
    frozen = {raw[i + 1].decode('utf-8'): raw[i].decode('ascii') for i in range(0, len(raw) - 1, 2) if raw[i]}
    ctx = {'head': head, 'frozen': frozen,
           'md': sorted(p for p, s in frozen.items() if s == 'A' and p.endswith('.md')),
           'py': sorted(p for p, s in frozen.items() if s == 'A' and p.endswith('.py'))}
    if (len(frozen), len(ctx['md']), len(ctx['py'])) != (7, 3, 2) or ctx['py'][1] != B2_GATE:
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
        print('test_f35sbxb2_sucesor: 0 casos correctos, 1 fallas (preparación no ejecutable)')
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
    print(f'test_f35sbxb2_sucesor: {good} casos correctos, {bad} fallas ({RUNS[0]} ejecuciones del gate sucesor)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
