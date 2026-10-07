"""F35-SBX-A — excepciones de alcance para los validadores históricos F30, F33 y F34.

Base inmutable: b67f644 (main tras F34E y el handoff macOS). La excepción vale solo en la rama F35-SBX y mientras
esa base sea ancestro de HEAD, así que sigue vigente tras los commits técnicos A y B hasta que C registre el gobierno.
Todo se compara contra la base, nunca contra HEAD:
  - CLAUDE.md y docs/PROGRESS.md: exactamente la apertura de F35-SBX-A (DH-09) y los 13 estados sin cambios;
  - validate_f30.py, validate_f33.py y validate_f34.py: exactamente la adaptación autorizada (import de este módulo,
    governance_ok(), sus regresiones y el ajuste mínimo del alcance Git); cualquier otro cambio funcional falla.
Rama distinta, base no ancestro, error de Git, base ilegible, binario, CR o contenido distinto: falla cerrado.
No concede permisos a ningún otro archivo.
"""
import subprocess

F35SBX_BRANCH = 'feature/f35-sbx-synthetic-evidence-pipeline'
F35SBX_BASE = 'b67f6443fb2bb71e736a60a645a15bd1fa0e7de6'
GOVERNANCE = frozenset({'CLAUDE.md', 'docs/PROGRESS.md'})
HISTORICAL_VALIDATORS = frozenset({'docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
                                   'docs/academico/tools/f34/validate_f34.py'})
STARTED = ('F35-SBX-A INICIADA — diseño, contratos, fixtures sintéticos y validación académica. '
           'Sin runtime productivo ni capacidades de alcance C.')
_NEXT = ('Próximo trabajo autorizado aquí: handoff macOS, no iniciar F35-SBX.',
         'El handoff macOS está publicado; F35-SBX-A está en curso en `feature/f35-sbx-synthetic-evidence-pipeline` '
         'y F35-SBX-B no se inicia sin autorización nueva.')
_HEADER = ('Última actualización: 2026-10-05 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
           'F35-SBX sintética HABILITADA, AÚN NO INICIADA; publicación sujeta a CI).',
           'Última actualización: 2026-10-07 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
           'F35-SBX sintética HABILITADA; F35-SBX-A INICIADA; publicación sujeta a CI).')
# Únicos reemplazos admitidos sobre el contenido de la base; cada texto original debe aparecer exactamente una vez.
OPENING = {
    'CLAUDE.md': [('F35-SBX AÚN NO INICIADA.', STARTED), _NEXT],
    'docs/PROGRESS.md': [_HEADER, ('F35-SBX AÚN NO INICIADA.', STARTED), _NEXT],
}
STATES = ['- G0 real = NO APROBADA', '- G0-09 = CUMPLIDO', '- G0-14 = CUMPLIDO', '- G0-02 = PENDIENTE EXTERNO',
          '- G0-03 = PENDIENTE EXTERNO', '- G0-12 = PENDIENTE EXTERNO', '- ADR-005 = PROPUESTA',
          '- G0-SBX = APROBADA CON RESTRICCIONES', '- F35 productiva = BLOQUEADA', '- F35-SBX = HABILITADA',
          '- F36–F40 = BLOQUEADAS', '- Alcance C = BLOQUEADO', '- Datos reales = PROHIBIDOS']
# Adaptación autorizada de los tres validadores históricos, como reemplazos exactos sobre la base.
VALIDATOR_PATCHES = {
    'docs/academico/tools/f30/validate_f30.py': [
        ('import f32_scope  # noqa: E402\n',
         "import f32_scope  # noqa: E402\nsys.path.append(os.path.join(HERE, '..', 'f35sbx'))\nimport f35sbx_scope  # noqa: E402\n"),
        ('    gobierno_f32 = f32_scope.GOVERNANCE if f32_scope.active(ROOT) else set()\n',
         '    gobierno_f32 = f32_scope.GOVERNANCE if f32_scope.active(ROOT) else set()\n    # F35-SBX-A (DH-09): CLAUDE.md y docs/PROGRESS.md solo con exactamente la apertura, en rama y base propias.\n'),
        ('             and ln[3:].strip(\'"\').replace(\'\\\\\', \'/\') not in (gobierno_f31 | gobierno_f32)]\n',
         '             and ln[3:].strip(\'"\').replace(\'\\\\\', \'/\') not in (gobierno_f31 | gobierno_f32)\n             and not f35sbx_scope.governance_ok(ln[3:], ROOT)]\n'),
        ("        err(f'cambios fuera de docs/academico/: {fuera}')\n",
         "        err(f'cambios fuera de docs/academico/: {fuera}')\n    for ok, m in f35sbx_scope.regressions(ROOT):\n        if not ok:\n            err(m)\n"),
    ],
    'docs/academico/tools/f33/validate_f33.py': [
        ("    check(all(p.startswith('docs/academico/') for p in rutas), f'cambios solo en docs/academico ({len(rutas)})')\n",
         "    # Excepción F35-SBX-A (DH-09): solo CLAUDE.md y docs/PROGRESS.md con exactamente la apertura; si no, falla.\n    sys.path.append(os.path.join(ROOT, 'docs', 'academico', 'tools', 'f35sbx'))\n    import f35sbx_scope\n    check(all(p.startswith('docs/academico/') or f35sbx_scope.governance_ok(p, ROOT) for p in rutas),\n          f'cambios solo en docs/academico ({len(rutas)})')\n    for ok, m in f35sbx_scope.regressions(ROOT):\n        check(ok, m)\n"),
    ],
    'docs/academico/tools/f34/validate_f34.py': [
        ("    add(all(p.startswith('docs/academico/') for p in rutas), f'cambios solo en docs/academico ({len(rutas)})')\n",
         "    # Excepción F35-SBX-A (DH-09): solo CLAUDE.md y docs/PROGRESS.md con exactamente la apertura; si no, falla.\n    sys.path.append(os.path.join(ROOT, 'docs', 'academico', 'tools', 'f35sbx'))\n    import f35sbx_scope\n    add(all(p.startswith('docs/academico/') or f35sbx_scope.governance_ok(p, ROOT) for p in rutas),\n        f'cambios solo en docs/academico ({len(rutas)})')\n    checks.extend(f35sbx_scope.regressions(ROOT))\n"),
    ],
}


def git(root, *args):
    try:
        p = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, encoding='utf-8')
    except OSError:
        return None, ''
    return p.returncode, p.stdout


def active(root, runner=git):
    """Rama F35-SBX exacta y base ancestro de HEAD (rc 0). Rama distinta, rc 1 o cualquier error: inactiva."""
    rc, branch = runner(root, 'branch', '--show-current')
    if rc != 0 or branch.strip() != F35SBX_BRANCH:
        return False
    return runner(root, 'merge-base', '--is-ancestor', F35SBX_BASE, 'HEAD')[0] == 0


def apply(base_text, patches):
    text = base_text
    for old, new in patches:
        if text.count(old) != 1:
            return None
        text = text.replace(old, new)
    return text


def expected(path, base_text):
    """Contenido de la base con la apertura de F35-SBX-A aplicada; None si la base no la admite."""
    return apply(base_text, OPENING[path]) if path in OPENING else None


def expected_validator(path, base_text):
    """Validador histórico de la base con la adaptación autorizada; None si la base no la admite."""
    return apply(base_text, VALIDATOR_PATCHES[path]) if path in VALIDATOR_PATCHES else None


def opening_problems(path, text, base_text):
    if path not in GOVERNANCE:
        return [f'{path}: no es gobierno F35-SBX-A']
    out = []
    exp = expected(path, base_text)
    if exp is None:
        out.append(f'{path}: la base no admite la apertura de F35-SBX-A')
    elif text != exp:
        out.append(f'{path}: cambios distintos de la apertura de F35-SBX-A')
    if STARTED not in text:
        out.append(f'{path}: falta el registro de apertura de F35-SBX-A')
    for line in STATES:
        if ('\n' + line + '\n') not in text:
            out.append(f'{path}: estado ausente o alterado: {line}')
    return out


def validator_problems(path, text, base_text):
    if path not in HISTORICAL_VALIDATORS:
        return [f'{path}: validador no autorizado para F35-SBX-A']
    exp = expected_validator(path, base_text)
    if exp is None:
        return [f'{path}: la base no admite la adaptación autorizada']
    if text != exp:
        return [f'{path}: cambios distintos de la adaptación autorizada (falla cerrado)']
    return []


def read(root, path):
    try:
        with open(f'{root}/{path}', 'rb') as f:
            return f.read()
    except OSError:
        return None


def _load(path, root, runner, reader):
    """(texto de trabajo, texto de la base) o None si algo no se puede verificar."""
    if not active(root, runner):
        return None
    rc, base = runner(root, 'show', f'{F35SBX_BASE}:{path}')
    data = reader(root, path)
    if rc != 0 or not base or data is None or b'\x00' in data or b'\r' in data:
        return None
    try:
        return data.decode('utf-8'), base
    except UnicodeDecodeError:
        return None


def governance_ok(path, root, runner=git, reader=read):
    """True solo para CLAUDE.md o docs/PROGRESS.md con exactamente la apertura de F35-SBX-A (falla cerrado)."""
    path = path.strip().strip('"').replace('\\', '/')
    if path not in GOVERNANCE:
        return False
    loaded = _load(path, root, runner, reader)
    return loaded is not None and not opening_problems(path, *loaded)


def validator_ok(path, root, runner=git, reader=read):
    """True solo para los tres validadores históricos con exactamente la adaptación autorizada (falla cerrado)."""
    path = path.strip().strip('"').replace('\\', '/')
    if path not in HISTORICAL_VALIDATORS:
        return False
    loaded = _load(path, root, runner, reader)
    return loaded is not None and not validator_problems(path, *loaded)


def regressions(root):
    """Negativos y controles en memoria: leen la base fija con Git y no escriben nada."""
    bases = {}
    for path in sorted(GOVERNANCE | HISTORICAL_VALIDATORS):
        rc, base = git(root, 'show', f'{F35SBX_BASE}:{path}')
        bases[path] = base if rc == 0 and base else None
    if None in bases.values():
        return [(False, 'F35-SBX: base fija ilegible (falla cerrado)')]

    def runner(branch=F35SBX_BRANCH, ancestor=0, head=F35SBX_BASE):
        def run(root_, *a):
            if a[:1] == ('branch',):
                return 0, branch + '\n'
            if a[:1] == ('merge-base',):
                return ancestor, ''
            if a[:1] == ('rev-parse',):
                return 0, head + '\n'
            if a[:1] == ('show',) and a[1].split(':', 1)[0] == F35SBX_BASE:
                return 0, bases.get(a[1].split(':', 1)[1], '')
            return 128, ''
        return run
    at_base, advanced = runner(), runner(head='c' * 40)
    text = lambda t: (lambda r, p: None if t is None else t.encode('utf-8'))
    out = []
    for path in sorted(GOVERNANCE):
        good = expected(path, bases[path])
        out.append((good is not None and STARTED in good and governance_ok(path, root, at_base, text(good)),
                    f'F35-SBX: A, HEAD = base con la apertura exacta aceptada en {path}'))
        out.append((governance_ok(path, root, advanced, text(good)),
                    f'F35-SBX: B/C, HEAD posterior con la base como ancestro y gobierno sin commit aceptado en {path}'))
        bad = {
            'modificación arbitraria': good + '\nLínea añadida sin relación con la apertura.\n',
            'G0 real = APROBADA': good.replace('- G0 real = NO APROBADA', '- G0 real = APROBADA', 1),
            'F35 productiva = HABILITADA': good.replace('- F35 productiva = BLOQUEADA', '- F35 productiva = HABILITADA', 1),
            'F36 iniciada': good.replace(STARTED, STARTED + ' F36 INICIADA.', 1),
            'alcance C habilitado': good.replace('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO', 1),
            'RF-21 modificada': good.replace(STARTED, STARTED + ' RF-21 se reemplaza por un orden nuevo.', 1),
            'RF-23 modificada': good.replace('RF-23 sigue humana', 'RF-23 pasa a ser automática', 1),
            'datos reales permitidos': good.replace('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS', 1),
            'sin registro de apertura': bases[path],
        }
        for label, t in bad.items():
            out.append((t != good and not governance_ok(path, root, at_base, text(t)),
                        f'F35-SBX: {label} rechazada en {path}'))
        out.append((not governance_ok(path, root, advanced, text(bad['G0 real = APROBADA'])),
                    f'F35-SBX: HEAD posterior con gobierno incorrecto rechazado en {path}'))
        for label, data in (('binario', good.encode('utf-8') + b'\x00'), ('CR', good.replace('\n', '\r\n').encode('utf-8')),
                            ('no UTF-8', b'\xff\xfe'), ('ilegible', None)):
            out.append((not governance_ok(path, root, at_base, lambda r, p, d=data: d), f'F35-SBX: {path} {label} rechazado'))
        for label, run in (('otra rama', runner(branch='main')), ('base no ancestro', runner(ancestor=1)),
                           ('error de git merge-base', runner(ancestor=128)), ('Git no disponible', lambda r, *a: (None, ''))):
            out.append((not governance_ok(path, root, run, text(good)), f'F35-SBX: {label} rechazado en {path}'))
    for path in sorted(HISTORICAL_VALIDATORS):
        good = expected_validator(path, bases[path])
        out.append((good is not None and validator_ok(path, root, at_base, text(good))
                    and validator_ok(path, root, advanced, text(good)),
                    f'F35-SBX: adaptación autorizada aceptada en {path} (HEAD = base y HEAD posterior)'))
        for label, t in (('cambio funcional extra', good + "\nprint('cambio no autorizado')\n"),
                         ('comprobación relajada', good.replace("startswith('docs/academico/')", "startswith('docs/')", 1)),
                         ('sin la adaptación', bases[path])):
            out.append((t != good and not validator_ok(path, root, at_base, text(t)),
                        f'F35-SBX: {label} rechazado en {path}'))
        out.append((not validator_ok(path, root, runner(ancestor=1), text(good)), f'F35-SBX: base no ancestro rechazada en {path}'))
    any_reader = lambda r, p: b'# texto\n'
    for path in ('README.md', 'docs/README.md', 'docs/academico/ACADEMIC_BASELINE.md', 'CLAUDE.md.bak', 'otro.md',
                 'app/Models/X.php', 'routes/web.php', 'config/app.php', 'database/migrations/x.php',
                 'resources/js/app.tsx', 'tests/Feature/X.php', 'cypress/e2e/x.cy.ts', 'ml-service/src/x.py',
                 'composer.json', 'composer.lock', 'package.json', 'package-lock.json', 'requirements.txt', '.env',
                 'docs/v1.1/scope-preliminary.md', 'docs/academico/g0-evidence/F34B_Decision_G0.md', 'logo.png',
                 'docs/academico/evidencia-sbx/foto.png'):
        out.append((not governance_ok(path, root, at_base, any_reader) and not validator_ok(path, root, at_base, any_reader),
                    f'F35-SBX: ruta rechazada {path}'))
    for path in ('docs/academico/tools/f34a/validate_f34a.py', 'docs/academico/tools/f30/f30.py',
                 'docs/academico/tools/f27b/validate.py', 'docs/academico/powerdesigner/scripts/validate_f29.py',
                 'docs/academico/tools/f34b/validate_f34b.py'):
        out.append((not validator_ok(path, root, at_base, any_reader), f'F35-SBX: cuarto validador no autorizado {path}'))
    return out
