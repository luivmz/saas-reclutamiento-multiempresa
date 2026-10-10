"""F35-SBX-A — excepciones de alcance para los validadores históricos F30, F33 y F34.

Base inmutable: b67f644 (main tras F34E y el handoff macOS). Tres contextos explícitos (context()):
  - FEATURE: rama F35-SBX y la base como ancestro de HEAD (commits A, B, C, D y posteriores de la rama);
  - INTEGRATION: rama develop o main, el commit D auditado (ba139c1) como ancestro de HEAD, evidencia POST-E del
    adaptador, el gobierno exactamente en el cierre (CERRADA) y los artefactos del cierre idénticos a E: gobierno,
    evidencia-sbx/**, tools/f35sbx/** (incluido este módulo) y las adaptaciones f30/f33/f34/f34b/f34e. No depende
    del hash de ningún merge ni del de E;
  - cualquier otra rama, HEAD separado, error de Git o condición incumplida: sin contexto (falla cerrado).
Todo se compara contra la base, nunca contra HEAD:
  - gobierno: exactamente uno de los dos estados de ciclo de vida autorizados de F35-SBX-A, con los 13 estados
    sin cambios: INICIADA (apertura, DH-09: CLAUDE.md y docs/PROGRESS.md) o CERRADA (cierre, commit C: CLAUDE.md,
    docs/PROGRESS.md y docs/academico/ACADEMIC_BASELINE.md, según la convención de cierres F33–F34E);
  - validate_f30.py, validate_f33.py y validate_f34.py: exactamente la adaptación autorizada (import de este módulo,
    governance_ok(), sus regresiones y el ajuste mínimo del alcance Git); cualquier otro cambio funcional falla.
Adaptador (adapter_state()): este módulo y validate_f35sbx.py se anclan mutuamente sin autorreferencia:
  - validate_f35sbx.ADAPTER_SHA256 = SHA-256 de este archivo (ancla externa; este archivo no guarda su propio hash);
  - VALIDATOR_SHA256 = SHA-256 de validate_f35sbx.py sin exactamente la línea de su ancla;
  - PRE-E: ningún commit posterior a D toca los dos archivos y su contenido es exactamente el auditado;
  - POST-E: en la historia completa de D..HEAD (sin simplificar, cada commit contra cada padre) un único commit E
    toca los dos archivos: hijo directo y único de D, cambia solo esos dos archivos con el contenido auditado, y el
    árbol de trabajo es idéntico a E. Cualquier otro commit que los toque (aunque un revert o un merge posterior
    restaure E), una eliminación, la versión de D o un ancla distinta fallan. validate_f35sbx.py repite la
    comprobación de forma independiente y además exige en PRE-E el delta exacto de esos dos archivos.
Rama distinta, base no ancestro, error de Git, base ilegible, binario, CR o contenido distinto: falla cerrado.
No concede permisos a ningún otro archivo.
"""
import hashlib
import os
import re
import subprocess

F35SBX_BRANCH = 'feature/f35-sbx-synthetic-evidence-pipeline'
F35SBX_BASE = 'b67f6443fb2bb71e736a60a645a15bd1fa0e7de6'
GOVERNANCE = frozenset({'CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md'})
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
CLOSED = ('F35-SBX-A CERRADA — diseño, contratos, fixtures sintéticos y validador completados, tras auditoría '
          'independiente PASS. Sin runtime productivo ni capacidades de alcance C. F35-SBX-B NO INICIADA.')
_NEXT_CLOSED = (_NEXT[0], 'El handoff macOS está publicado; F35-SBX-A queda cerrada documentalmente en '
                '`feature/f35-sbx-synthetic-evidence-pipeline`, con publicación pendiente de regresión post-commits y '
                'CI. F35-SBX-B NO INICIADA; requiere autorización nueva.')
_HEADER_CLOSED = (_HEADER[0], 'Última actualización: 2026-10-07 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA '
                  'CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA; F35-SBX-B NO INICIADA; '
                  'publicación pendiente de regresión post-commits y CI).')
# Cierre (commit C): únicos reemplazos admitidos sobre la base; ACADEMIC_BASELINE solo registra el cierre.
CLOSING = {
    'CLAUDE.md': [('F35-SBX AÚN NO INICIADA.', CLOSED), _NEXT_CLOSED],
    'docs/PROGRESS.md': [_HEADER_CLOSED, ('F35-SBX AÚN NO INICIADA.', CLOSED), _NEXT_CLOSED],
    'docs/academico/ACADEMIC_BASELINE.md': [('F35-SBX AÚN NO INICIADA.', CLOSED), _NEXT_CLOSED],
}
# Ciclo de vida: los dos únicos estados autorizados, nunca ambos ni otro.
LIFECYCLE = {'INICIADA': (OPENING, STARTED), 'CERRADA': (CLOSING, CLOSED)}
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


# Integración: identidad estable de la entrega auditada = commit D (y sus ancestros A, B y C).
AUDITED_CLOSURE = 'ba139c1f0e4a16c15126ff1e34ae280620234db7'
INTEGRATION_BRANCHES = frozenset({'develop', 'main'})
FEATURE, INTEGRATION = 'FEATURE', 'INTEGRATION'
# Artefactos que en develop/main deben ser idénticos a E, sin exclusiones: gobierno, evidencia-sbx/**,
# tools/f35sbx/** (incluidos este módulo y validate_f35sbx.py) y las adaptaciones f30/f33/f34/f34b/f34e.
FROZEN_AFTER_CLOSURE = ('CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md',
                        'docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx', *sorted(HISTORICAL_VALIDATORS),
                        'docs/academico/tools/f34b/validate_f34b.py', 'docs/academico/tools/f34e/validate_f34e.py')
# Transición del adaptador: los dos únicos archivos que E puede cambiar respecto de D.
ADAPTER = 'docs/academico/tools/f35sbx/f35sbx_scope.py'
ADAPTER_VALIDATOR = 'docs/academico/tools/f35sbx/validate_f35sbx.py'
ADAPTED_IN_E = (ADAPTER, ADAPTER_VALIDATOR)
ANCHOR_RX = re.compile(r"^ADAPTER_SHA256 = '([0-9a-f]{64})'\n", re.M)
VALIDATOR_SHA256 = '0db50264db3447e99637a239850842e0d444586b0d0ff342976f83ab32e9e05c'
PRE_E, POST_E = 'PRE-E', 'POST-E'


def _sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _text(data):
    if data is None or b'\x00' in data or b'\r' in data:
        return None
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None


def anchor_problems(adapter_text, validator_text):
    """Anclas cruzadas del adaptador auditado: externa (en validate_f35sbx.py) y del validador sin su línea de ancla."""
    if adapter_text is None or validator_text is None:
        return ['adaptador o validador ilegibles (falla cerrado)']
    anchors = ANCHOR_RX.findall(validator_text)
    if len(anchors) != 1:
        return ['ancla externa ADAPTER_SHA256 ausente o duplicada en validate_f35sbx.py (falla cerrado)']
    out = []
    if _sha(adapter_text) != anchors[0]:
        out.append('f35sbx_scope.py distinto del adaptador auditado (ancla externa ADAPTER_SHA256)')
    if _sha(ANCHOR_RX.sub('', validator_text, count=1)) != VALIDATOR_SHA256:
        out.append('validate_f35sbx.py distinto del validador auditado (VALIDATOR_SHA256)')
    return out


def adapter_history(root, runner=git):
    """Commits de D..HEAD que tocan el adaptador o el validador, con historia completa y sin simplificar: `git log` sin
    rutas enumera todos los commits alcanzables (también los de ramas laterales ya fusionadas) y cada uno se compara
    contra cada uno de sus padres. Un commit normal los toca si cambia alguno frente a su padre; un merge, si su versión
    difiere de la de todos sus padres. Un cambio en una rama lateral sigue siendo su propio commit aunque un merge o un
    revert posterior restaure E. (lista de (commit, padres, rutas tocadas), error)."""
    rc, log = runner(root, 'log', '--format=%H %P', f'{AUDITED_CLOSURE}..HEAD')
    if rc != 0:
        return None, f'historia del adaptador no verificable ({rc}): falla cerrado'
    touching = []
    for line in log.splitlines():
        ids = line.split()
        if not ids:
            continue
        if len(ids) < 2 or not all(re.fullmatch(r'[0-9a-f]{40}', x) for x in ids):
            return None, 'commit sin padres o no verificable en la historia posterior a D (falla cerrado)'
        commit, parents = ids[0], ids[1:]
        diffs = []
        for parent in parents:
            rc, names = runner(root, 'diff-tree', '-r', '--name-only', '--no-renames', parent, commit, '--',
                               *ADAPTED_IN_E)
            if rc != 0:
                return None, f'diff de {commit[:7]} no verificable ({rc}): falla cerrado'
            diffs.append(set(names.split()))
        touched = set.intersection(*diffs)
        if touched:
            touching.append((commit, parents, sorted(touched)))
    return touching, None


def adapter_state(root, runner=git, reader=None):
    """(PRE-E | POST-E | None, E, problemas) del adaptador. Sin hashes de merge ni de E: E es el único commit posterior a
    D que toca el adaptador o el validador, según la historia completa (adapter_history)."""
    reader = reader or read
    adapter, validator = (_text(reader(root, path)) for path in ADAPTED_IN_E)
    problems = anchor_problems(adapter, validator)
    touching, error = adapter_history(root, runner)
    if error:
        return None, None, problems + [error]
    if not touching:
        return PRE_E, None, problems
    if len(touching) > 1:
        return None, None, problems + [f'adaptador o validador modificados después de D por {len(touching)} commits '
                                       f'(historia completa): {[c[:7] for c, _, _ in touching][:5]}']
    e, parents, _ = touching[0]
    rc2, names = runner(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', '--no-renames', e)
    shown = [runner(root, 'show', f'{e}:{path}') for path in ADAPTED_IN_E]
    if rc2 != 0 or any(r != 0 for r, _ in shown):
        return None, e, problems + ['contenido de E no verificable (falla cerrado)']
    if parents != [AUDITED_CLOSURE]:
        problems.append('E no es hijo directo y único del commit D (ni merge)')
    if sorted(names.split()) != sorted(ADAPTED_IN_E):
        problems.append(f'E cambia archivos distintos de los dos adaptados: {sorted(names.split())[:5]}')
    if anchor_problems(shown[0][1], shown[1][1]):
        problems.append('E no contiene exactamente el adaptador y el validador auditados')
    if (adapter, validator) != (shown[0][1], shown[1][1]):
        problems.append('árbol de trabajo del adaptador distinto de E')
    return POST_E, e, problems


def context(root, runner=git, reader=None, adapter_reader=None):
    """FEATURE, INTEGRATION o None (falla cerrado). Nunca basta el nombre de la rama."""
    rc, branch = runner(root, 'branch', '--show-current')
    if rc != 0:
        return None
    branch = branch.strip()
    if branch == F35SBX_BRANCH:
        if runner(root, 'merge-base', '--is-ancestor', F35SBX_BASE, 'HEAD')[0] != 0:
            return None
        phase, e, problems = adapter_state(root, runner, adapter_reader)
        if phase == POST_E and not problems:
            problems = frozen_problems(root, runner, e)             # misma congelación que develop/main
        return FEATURE if phase is not None and not problems else None
    if branch in INTEGRATION_BRANCHES:
        if runner(root, 'merge-base', '--is-ancestor', AUDITED_CLOSURE, 'HEAD')[0] != 0:
            return None
        return INTEGRATION if not integration_problems(root, runner, reader or read, adapter_reader) else None
    return None


PYCACHE_OK = 'docs/academico/tools/f35sbx/__pycache__'      # único directorio ignorado por la política del repo


def blob_id(data):
    """Identificador Git del blob calculado localmente sobre los bytes reales (sin índice ni filtros)."""
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def real_bytes(root, rel):
    full = os.path.join(root, rel)
    return None if os.path.islink(full) or not os.path.isfile(full) else read(root, rel)


def cache_problems(path, sub):
    """Excepción __pycache__: solo archivos regulares *.pyc directos. DirEntry.is_file(follow_symlinks=False) no sigue
    enlaces: un nombre o sufijo .pyc nunca convierte un directorio, enlace, unión u objeto especial en permitido.
    Directorio o entrada ilegible: falla cerrado."""
    bad = []
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                try:
                    ok = entry.name.endswith('.pyc') and not entry.is_symlink() and entry.is_file(follow_symlinks=False)
                except OSError:
                    ok = False
                if not ok:
                    bad.append(entry.name)
    except OSError:
        return [f'{sub} ilegible (falla cerrado)']
    return [f'entradas no permitidas en {sub} (solo archivos regulares .pyc): {sorted(bad)[:3]}'] if bad else []


def _remove_tree(top):
    """Borrado sin seguir enlaces (solo os): archivos y enlaces se desvinculan; directorios, de abajo arriba."""
    if not os.path.lexists(top):
        return
    for d, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(d, name))
        for name in dirs:
            p = os.path.join(d, name)
            try:
                os.unlink(p) if os.path.islink(p) else os.rmdir(p)
            except OSError:
                os.rmdir(p)
    os.rmdir(top)


def cache_regressions(disk):
    """Excepción __pycache__ con sistema de archivos real en un directorio temporal fuera del repositorio."""
    base = os.environ.get('TMPDIR') or os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp'
    tmp = os.path.join(base, f'f35sbx-cache-{os.getpid()}')
    _remove_tree(tmp)
    cache = os.path.join(tmp, *PYCACHE_OK.split('/'))
    out = []

    def touch(p, data=b'x'):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as f:
            f.write(data)

    def case(label, build, ok, needs_link=False):
        _remove_tree(os.path.join(tmp, 'docs'))
        os.makedirs(cache)
        outside = os.path.join(tmp, 'fuera.txt')
        touch(outside)
        try:
            build(cache, outside)
        except OSError as e:
            if not needs_link:
                raise
            out.append((True, f'__pycache__: {label} — enlace no creable en esta plataforma ({e.__class__.__name__})'))
            return
        _, problems = disk(tmp)
        out.append(((not problems) == ok, f'__pycache__: {label} → {"PASS" if not problems else "FAIL"} {problems[:1]}'))
    try:
        case('vacío', lambda c, o: None, True)
        case('normal.pyc archivo regular', lambda c, o: touch(os.path.join(c, 'normal.pyc')), True)
        case('directorio not-a-file.pyc con descendiente',
             lambda c, o: touch(os.path.join(c, 'not-a-file.pyc', 'hidden-extra.md')), False)
        case('directorio directory.pyc vacío', lambda c, o: os.makedirs(os.path.join(c, 'directory.pyc')), False)
        case('enlace link.pyc a un archivo', lambda c, o: os.symlink(o, os.path.join(c, 'link.pyc')), False, True)
        case('enlace dir.pyc a un directorio', lambda c, o: os.symlink(os.path.dirname(o), os.path.join(c, 'dir.pyc'),
                                                                    target_is_directory=True), False, True)
        case('subdirectorio subdir/hidden.pyc', lambda c, o: touch(os.path.join(c, 'subdir', 'hidden.pyc')), False)
        case('archivo evil.txt', lambda c, o: touch(os.path.join(c, 'evil.txt')), False)
        case('normal.pyc + archivo extra oculto',
             lambda c, o: (touch(os.path.join(c, 'normal.pyc')), touch(os.path.join(c, 'oculto.md'))), False)
    finally:
        _remove_tree(tmp)
    return out


def disk_files(root):
    """Archivos reales bajo los artefactos congelados (sistema de archivos, sin Git ni índice)."""
    found, problems = set(), []
    for rel in FROZEN_AFTER_CLOSURE:
        full = os.path.join(root, rel)
        if os.path.islink(full):
            problems.append(f'ruta protegida convertida en enlace: {rel}')
        elif os.path.isdir(full):
            for d, dirs, files in os.walk(full):
                here = os.path.relpath(d, root).replace(os.sep, '/')
                for x in list(dirs):
                    sub = f'{here}/{x}'
                    if os.path.islink(os.path.join(d, x)):
                        problems.append(f'directorio protegido como enlace: {sub}')
                        dirs.remove(x)
                    elif sub == PYCACHE_OK:
                        dirs.remove(x)
                        problems += cache_problems(os.path.join(d, x), sub)
                found |= {f'{here}/{f}' for f in files}
        elif os.path.lexists(full):
            found.add(rel)
    return found, problems


def integrity_problems(root, runner, ref):
    """Sin depender de git diff: ningún flag del índice en los congelados (`ls-files -v`: solo «H»; h =
    assume-unchanged, S = skip-worktree, s = ambos), y los bytes reales del sistema de archivos con el blob-id y el
    modo 100644 de ref, sin archivos de más ni de menos."""
    rc1, flags = runner(root, 'ls-files', '-v', '-z', '--', *FROZEN_AFTER_CLOSURE)
    rc2, tree = runner(root, 'ls-tree', '-r', '-z', '--full-tree', ref, '--', *FROZEN_AFTER_CLOSURE)
    if rc1 != 0 or rc2 != 0:
        return [f'índice o árbol de E no verificables ({rc1}, {rc2}): falla cerrado']
    out = []
    flagged = [x[2:] for x in flags.split('\x00') if x and x[:2] != 'H ']
    if flagged:
        out.append(f'flags del índice que ocultan cambios en artefactos congelados: {flagged[:5]}')
    expected = {}
    for entry in tree.split('\x00'):
        if entry:
            meta, _, path = entry.partition('\t')
            parts = meta.split()
            if len(parts) != 3:
                return out + ['árbol de E ilegible (falla cerrado)']
            expected[path] = tuple(parts)
    if not expected:
        return out + ['árbol de E vacío para los artefactos congelados (falla cerrado)']
    found, walk_problems = disk_files(root)
    out += walk_problems
    differ = [path for path, (mode, kind, oid) in sorted(expected.items())
              if kind != 'blob' or mode != '100644' or (data := real_bytes(root, path)) is None or blob_id(data) != oid]
    if differ:
        out.append(f'bytes reales distintos de E, eliminados o ilegibles: {differ[:5]}')
    extra = sorted(found - set(expected))
    if extra:
        out.append(f'artefactos congelados que no existen en E: {extra[:5]}')
    return out


def frozen_problems(root, runner, e):
    """POST-E (feature, develop y main): los artefactos congelados idénticos a E en el árbol de trabajo, en el índice
    y sin archivos nuevos sin seguimiento; sin detección de renombrados (un rename es eliminación + alta)."""
    rc1, tree = runner(root, 'diff', '--name-only', '--no-renames', e, '--', *FROZEN_AFTER_CLOSURE)
    rc2, index = runner(root, 'diff', '--cached', '--name-only', '--no-renames', e, '--', *FROZEN_AFTER_CLOSURE)
    rc3, untracked = runner(root, 'ls-files', '--others', '--exclude-standard', '--', *FROZEN_AFTER_CLOSURE)
    if (rc1, rc2, rc3) != (0, 0, 0):
        return [f'Git no verificable en la congelación POST-E ({rc1}, {rc2}, {rc3}): falla cerrado']
    changed = sorted({ln.strip() for ln in (tree + '\n' + index + '\n' + untracked).splitlines() if ln.strip()})
    out = [f'artefactos del cierre modificados después de E: {changed[:5]}'] if changed else []
    return out + integrity_problems(root, runner, e)        # bytes reales y flags, independiente de git diff


def integration_problems(root, runner=git, reader=None, adapter_reader=None):
    """En develop/main: evidencia POST-E del adaptador, artefactos del cierre idénticos a E (incluido el árbol de
    trabajo y sin exclusiones) y gobierno exactamente CERRADA sobre la base, con los 13 estados aprobados."""
    reader = reader or read
    phase, e, problems = adapter_state(root, runner, adapter_reader)
    if phase != POST_E:
        return problems + ['develop/main sin evidencia POST-E del adaptador auditado (falla cerrado)']
    if problems:
        return problems
    out = frozen_problems(root, runner, e)
    if out and 'falla cerrado' in out[0]:
        return out
    for path in sorted(GOVERNANCE):
        rc, base = runner(root, 'show', f'{F35SBX_BASE}:{path}')
        data = reader(root, path)
        try:
            text = data.decode('utf-8') if data is not None else None
        except UnicodeDecodeError:
            text = None
        if rc != 0 or not base or text is None or lifecycle(path, text, base) != 'CERRADA' \
                or governance_problems(path, text, base):
            out.append(f'{path}: la integración exige exactamente el cierre auditado de F35-SBX-A')
    return out


def active(root, runner=git, reader=None, adapter_reader=None):
    """Contexto FEATURE o INTEGRATION válido; cualquier otra situación: inactiva (falla cerrado)."""
    return context(root, runner, reader, adapter_reader) is not None


def apply(base_text, patches):
    text = base_text
    for old, new in patches:
        if text.count(old) != 1:
            return None
        text = text.replace(old, new)
    return text


def expected(path, base_text, state='INICIADA'):
    """Contenido de la base con el estado de ciclo de vida aplicado; None si no está autorizado para esa ruta."""
    patches = LIFECYCLE[state][0]
    return apply(base_text, patches[path]) if path in patches else None


def lifecycle(path, text, base_text):
    """'INICIADA' o 'CERRADA' si el texto es exactamente ese estado autorizado sobre la base; None en otro caso."""
    found = [st for st in LIFECYCLE if expected(path, base_text, st) == text]
    return found[0] if len(found) == 1 else None


def expected_validator(path, base_text):
    """Validador histórico de la base con la adaptación autorizada; None si la base no la admite."""
    return apply(base_text, VALIDATOR_PATCHES[path]) if path in VALIDATOR_PATCHES else None


def governance_problems(path, text, base_text):
    """El gobierno debe ser exactamente la apertura o el cierre autorizados, con su frase canónica y sin la otra."""
    if path not in GOVERNANCE:
        return [f'{path}: no es gobierno F35-SBX-A']
    out = []
    state = lifecycle(path, text, base_text)
    if state is None:
        out.append(f'{path}: contenido distinto de la apertura o del cierre autorizados de F35-SBX-A')
    elif (STARTED in text) == (CLOSED in text):
        out.append(f'{path}: estado de F35-SBX-A ambiguo (INICIADA y CERRADA o ninguno)')
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
    """(texto de trabajo, texto de la base, contexto) o None si algo no se puede verificar."""
    ctx = context(root, runner, reader)
    if ctx is None:
        return None
    rc, base = runner(root, 'show', f'{F35SBX_BASE}:{path}')
    data = reader(root, path)
    if rc != 0 or not base or data is None or b'\x00' in data or b'\r' in data:
        return None
    try:
        return data.decode('utf-8'), base, ctx
    except UnicodeDecodeError:
        return None


def governance_ok(path, root, runner=git, reader=read):
    """True solo para el gobierno F35-SBX-A con exactamente la apertura o el cierre autorizados (falla cerrado)."""
    path = path.strip().strip('"').replace('\\', '/')
    if path not in GOVERNANCE:
        return False
    loaded = _load(path, root, runner, reader)
    if loaded is None:
        return False
    text, base, ctx = loaded
    if ctx == INTEGRATION and lifecycle(path, text, base) != 'CERRADA':
        return False                                        # en develop/main solo el cierre auditado
    return not governance_problems(path, text, base)


def validator_ok(path, root, runner=git, reader=read):
    """True solo para los tres validadores históricos con exactamente la adaptación autorizada (falla cerrado)."""
    path = path.strip().strip('"').replace('\\', '/')
    if path not in HISTORICAL_VALIDATORS:
        return False
    loaded = _load(path, root, runner, reader)
    return loaded is not None and not validator_problems(path, *loaded[:2])


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
            if a[:1] in (('diff',), ('ls-files',), ('log',)):
                return 0, ''
            if a[:1] == ('show',) and a[1].split(':', 1)[0] == F35SBX_BASE:
                return 0, bases.get(a[1].split(':', 1)[1], '')
            return 128, ''
        return run
    at_base, advanced = runner(), runner(head='c' * 40)
    text = lambda t: (lambda r, p: None if t is None else t.encode('utf-8'))
    out = []
    for path in sorted(GOVERNANCE):
        for state, (_, marker) in LIFECYCLE.items():
            good = expected(path, bases[path], state)
            if good is None:                                       # p. ej. ACADEMIC_BASELINE en la apertura
                opening = expected(path, bases[path], 'INICIADA')
                out.append((opening is None and not governance_ok(path, root, at_base, text(bases[path])),
                            f'F35-SBX: {path} no admite el estado {state}'))
                continue
            out.append((marker in good and governance_ok(path, root, at_base, text(good)),
                        f'F35-SBX: {state} exacta aceptada en {path} (HEAD = base)'))
            out.append((governance_ok(path, root, advanced, text(good)),
                        f'F35-SBX: {state} exacta aceptada en {path} con HEAD posterior (base ancestro)'))
            other = CLOSED if state == 'INICIADA' else STARTED
            bad = {
                'modificación arbitraria': good + '\nLínea añadida sin relación con el ciclo de vida.\n',
                'G0 real = APROBADA': good.replace('- G0 real = NO APROBADA', '- G0 real = APROBADA', 1),
                'F35 productiva = HABILITADA': good.replace('- F35 productiva = BLOQUEADA', '- F35 productiva = HABILITADA', 1),
                'F36 iniciada': good.replace(marker, marker + ' F36 INICIADA.', 1),
                'alcance C habilitado': good.replace('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO', 1),
                'RF-21 modificada': good.replace(marker, marker + ' RF-21 se reemplaza por un orden nuevo.', 1),
                'RF-23 modificada': good.replace('RF-23 sigue humana', 'RF-23 pasa a ser automática', 1),
                'otro RF modificado': good.replace(marker, marker + ' RF-05 se elimina del baseline.', 1),
                'datos reales permitidos': good.replace('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS', 1),
                'INICIADA y CERRADA a la vez': good.replace(marker, marker + ' ' + other, 1),
                'estado desconocido FINALIZADA': good.replace(marker, marker.replace(state, 'FINALIZADA'), 1),
                'F35-SBX-B INICIADA': good.replace(marker, marker + ' F35-SBX-B INICIADA.', 1),
                'auditoría FAIL': good.replace(marker, marker + ' Auditoría independiente FAIL.', 1),
                'sin registro de ciclo de vida': bases[path],
            }
            for label, t in bad.items():
                out.append((t != good and not governance_ok(path, root, at_base, text(t)),
                            f'F35-SBX: {state} con {label} rechazado en {path}'))
            out.append((not governance_ok(path, root, advanced, text(bad['G0 real = APROBADA'])),
                        f'F35-SBX: HEAD posterior con gobierno {state} incorrecto rechazado en {path}'))
            for label, data in (('binario', good.encode('utf-8') + b'\x00'),
                                ('CR', good.replace('\n', '\r\n').encode('utf-8')), ('no UTF-8', b'\xff\xfe'),
                                ('ilegible', None)):
                out.append((not governance_ok(path, root, at_base, lambda r, p, d=data: d),
                            f'F35-SBX: {path} {state} {label} rechazado'))
            for label, run in (('otra rama', runner(branch='main')), ('base no ancestro', runner(ancestor=1)),
                               ('error de git merge-base', runner(ancestor=128)), ('Git no disponible', lambda r, *a: (None, ''))):
                out.append((not governance_ok(path, root, run, text(good)), f'F35-SBX: {state} con {label} rechazado en {path}'))
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
    return out + integration_regressions(root, bases) + cache_regressions(disk_files)


def integration_regressions(root, bases):
    """Contextos FEATURE/DEVELOP/MAIN y transición PRE-E/POST-E con Git simulado en memoria (no crea ramas, commits,
    merges ni archivos)."""
    closed = {p: expected(p, bases[p], 'CERRADA') for p in GOVERNANCE}
    opened = {p: expected(p, bases[p], 'INICIADA') or bases[p] for p in GOVERNANCE}
    good = dict(closed, **{p: expected_validator(p, bases[p]) for p in HISTORICAL_VALIDATORS})
    real = {p: _text(read(root, p)) for p in ADAPTED_IN_E}
    rc_d, adapter_d = git(root, 'show', f'{AUDITED_CLOSURE}:{ADAPTER}')
    if None in real.values() or rc_d != 0 or not adapter_d:
        return [(False, 'adaptador, validador o versión D ilegibles (falla cerrado)')]
    e_hash = 'e' * 40
    sc, va = ADAPTED_IN_E
    both = [sc, va]
    # Historia simulada D..HEAD: (commit, padres, {padre: rutas del adaptador cambiadas frente a ese padre}).
    clean_e = [('9' * 40, ['8' * 40, e_hash], {'8' * 40: both, e_hash: []}),
               (e_hash, [AUDITED_CLOSURE], {AUDITED_CLOSURE: both})]

    disk, _ = disk_files(root)
    disk_tree = ''.join(f'100644 blob {blob_id(real_bytes(root, q))}\t{q}\x00' for q in sorted(disk))
    readme = 'docs/academico/evidencia-sbx/README.md'

    def runner(branch='develop', closure=0, base=0, diff='', diff_rc=0, branch_rc=0, history=None, history_rc=0,
               raw_log=None, pair_rc=0, names=None, names_rc=0, e_files=None, show_rc=0, flags='', ref_tree=None,
               ls_tree_rc=0):
        history = clean_e if history is None else history
        names = '\n'.join(ADAPTED_IN_E) if names is None else names
        e_files = real if e_files is None else e_files
        pairs = {(p, c): t for c, _, per in history for p, t in per.items()}
        log = raw_log if raw_log is not None else ''.join(f'{c} {" ".join(ps)}\n' for c, ps, _ in history)

        def run(root_, *a):
            if a[:1] == ('branch',):
                return branch_rc, branch + '\n'
            if a[:2] == ('merge-base', '--is-ancestor'):
                return (closure if a[2] == AUDITED_CLOSURE else base), ''
            if a[:2] == ('log', '--format=%H %P'):
                return history_rc, log
            if a[:2] == ('diff-tree', '-r'):
                return pair_rc, '\n'.join(pairs.get((a[4], a[5]), [])) + '\n'
            if a[:2] == ('diff-tree', '--no-commit-id'):
                return names_rc, names + '\n'
            if a[:1] == ('diff',):
                return diff_rc, diff
            if a[:2] == ('ls-files', '-v'):
                return 0, flags
            if a[:1] == ('ls-tree',):
                return ls_tree_rc, disk_tree if ref_tree is None else ref_tree
            if a[:1] == ('ls-files',):
                return 0, ''
            if a[:1] == ('show',) and a[1].split(':', 1)[0] == e_hash:
                content = e_files.get(a[1].split(':', 1)[1])
                return (show_rc, content) if content is not None else (128, '')
            if a[:1] == ('show',) and a[1].split(':', 1)[0] == F35SBX_BASE:
                return 0, bases.get(a[1].split(':', 1)[1], '')
            return 128, ''
        return run

    def reader(files):
        return lambda r, p: None if files.get(p) is None else files[p].encode('utf-8')

    def gov_with(old, new):
        mutated = {p: closed[p].replace(old, new, 1) for p in GOVERNANCE}
        assert all(mutated[p] != closed[p] for p in GOVERNANCE), old   # la mutación debe existir
        return dict(good, **mutated)

    def adapter_with(**files):
        return reader(dict(real, **{ADAPTER if k == 'adapter' else ADAPTER_VALIDATOR: v for k, v in files.items()}))
    ok_reader = reader(good)
    f30 = 'docs/academico/tools/f30/validate_f30.py'
    validator_anchor = ANCHOR_RX.search(real[ADAPTER_VALIDATOR]).group(0)
    wrong_anchor = real[ADAPTER_VALIDATOR].replace(validator_anchor, f"ADAPTER_SHA256 = '{'0' * 64}'\n", 1)
    extra_adapter = real[ADAPTER] + '# línea añadida\n'
    extra_validator = real[ADAPTER_VALIDATOR] + '# línea añadida\n'
    pre_e = runner(branch=F35SBX_BRANCH, history=[])
    x, y, z, lat, m2 = '1' * 40, '2' * 40, '3' * 40, '4' * 40, '5' * 40

    def after_e(*commits):
        return list(commits) + clean_e
    clean_merge = after_e((m2, [e_hash, z], {e_hash: [], z: both}))
    out = [
        (context(root, pre_e, ok_reader) == FEATURE and adapter_state(root, pre_e)[0] == PRE_E,
         'adaptador 1: PRE-E exacto en feature → FEATURE (PASS)'),
        (context(root, runner(branch=F35SBX_BRANCH, history=clean_e[1:]), ok_reader) == FEATURE
         and adapter_state(root, runner(branch=F35SBX_BRANCH, history=clean_e[1:]))[:2] == (POST_E, e_hash),
         'adaptador B: POST-E exacto en feature (HEAD = E) → FEATURE (PASS)'),
        (adapter_state(root, runner(history=clean_merge))[0] == POST_E
         and not adapter_state(root, runner(history=clean_merge))[2]
         and context(root, runner(branch='main', history=clean_merge), ok_reader) == INTEGRATION,
         'adaptador 15/E: merge limpio posterior a E que no toca los archivos congelados → PASS'),
        (all(f'(exclude)' not in x for x in FROZEN_AFTER_CLOSURE) and ADAPTER.startswith('docs/academico/tools/f35sbx/')
         and 'docs/academico/tools/f35sbx' in FROZEN_AFTER_CLOSURE,
         'adaptador: congelado tras E sin exclusiones (tools/f35sbx/** incluye f35sbx_scope.py)'),
        (adapter_d != real[ADAPTER] and ANCHOR_RX.sub('', real[ADAPTER_VALIDATOR], count=1) != real[ADAPTER_VALIDATOR],
         'adaptador: la versión D es distinta y el ancla externa existe en validate_f35sbx.py'),
    ]
    for branch in sorted(INTEGRATION_BRANCHES):
        run = runner(branch=branch)
        out.append((context(root, run, ok_reader) == INTEGRATION and validator_ok(f30, root, run, ok_reader)
                    and all(governance_ok(p, root, run, ok_reader) for p in GOVERNANCE),
                    f'contexto {branch}: commit D ancestro, POST-E exacto y cierre exacto → INTEGRATION'))
    out.append((context(root, runner(branch='develop'), ok_reader) == INTEGRATION,
                'contexto D: otro merge cualquiera con el commit D como ancestro → INTEGRATION (sin hash de merge ni de E)'))
    negatives = [
        ('develop sin el commit D como ancestro', runner(branch='develop', closure=1), ok_reader, None),
        ('main sin el commit D como ancestro', runner(branch='main', closure=1), ok_reader, None),
        ('rama desconocida', runner(branch='feature/otra'), ok_reader, None),
        ('HEAD separado (sin rama)', runner(branch=''), ok_reader, None),
        ('error de Git al leer la rama', runner(branch_rc=128), ok_reader, None),
        ('error de Git en merge-base', runner(closure=128), ok_reader, None),
        ('error de Git en diff', runner(diff_rc=128), ok_reader, None),
        ('develop con F35-SBX-B INICIADA', runner(branch='develop', diff='CLAUDE.md'),
         reader(gov_with('F35-SBX-B NO INICIADA.', 'F35-SBX-B INICIADA.')), None),
        ('main con G0 real APROBADA', runner(branch='main', diff='CLAUDE.md'),
         reader(gov_with('- G0 real = NO APROBADA', '- G0 real = APROBADA')), None),
        ('develop con F35 productiva HABILITADA', runner(branch='develop', diff='CLAUDE.md'),
         reader(gov_with('- F35 productiva = BLOQUEADA', '- F35 productiva = HABILITADA')), None),
        ('main con alcance C HABILITADO', runner(branch='main', diff='CLAUDE.md'),
         reader(gov_with('- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO')), None),
        ('develop con datos reales PERMITIDOS', runner(branch='develop', diff='CLAUDE.md'),
         reader(gov_with('- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS')), None),
        ('develop con una modificación arbitraria del gobierno', runner(branch='develop', diff='docs/PROGRESS.md'),
         reader(dict(good, **{'docs/PROGRESS.md': closed['docs/PROGRESS.md'] + '\nLínea añadida.\n'})), None),
        ('develop con gobierno alterado aunque Git no lo informe', runner(branch='develop'),
         reader(gov_with('- G0 real = NO APROBADA', '- G0 real = APROBADA')), None),
        ('develop con el gobierno de la apertura (INICIADA)', runner(branch='develop'), reader(dict(good, **opened)), None),
        ('main con una modificación posterior de evidencia-sbx', runner(branch='main',
         diff='docs/academico/evidencia-sbx/fixtures/manifest.json'), ok_reader, None),
        ('main con una modificación posterior de un validador histórico', runner(branch='main', diff=f30), ok_reader, None),
        ('develop con una modificación posterior de validate_f34b', runner(branch='develop',
         diff='docs/academico/tools/f34b/validate_f34b.py'), ok_reader, None),
        ('main con una modificación posterior de validate_f35sbx', runner(branch='main', diff=ADAPTER_VALIDATOR),
         ok_reader, None),
        # FEATURE POST-E: misma congelación que develop/main respecto de E (árbol, índice y sin seguimiento).
        *[(f'feature POST-E con {p} modificado respecto de E', runner(branch=F35SBX_BRANCH, history=clean_e[1:], diff=p),
           ok_reader, None)
          for p in ('docs/academico/evidencia-sbx/README.md', 'docs/academico/evidencia-sbx/fixtures/manifest.json',
                    'CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md', f30,
                    'docs/academico/tools/f34b/validate_f34b.py', 'docs/academico/tools/f34e/validate_f34e.py',
                    ADAPTER, ADAPTER_VALIDATOR)],
        ('feature POST-E con error de Git en la congelación', runner(branch=F35SBX_BRANCH, history=clean_e[1:],
                                                                    diff_rc=128), ok_reader, None),
        # Flags del índice y bytes reales frente a E (git diff no ve nada en estos casos).
        *[(f'{b} POST-E con flag «{t}» en README', runner(branch=b, history=hist, flags=f'{t} {readme}\x00'),
           ok_reader, None)
          for b, hist in ((F35SBX_BRANCH, clean_e[1:]), ('develop', None), ('main', None)) for t in ('h', 'S', 's')],
        ('feature POST-E con bytes reales de README distintos de E', runner(branch=F35SBX_BRANCH, history=clean_e[1:],
         ref_tree=disk_tree.replace(f'\t{readme}', f'\t{readme}', 1).replace(
             disk_tree.split(f'\t{readme}')[0][-40:], '0' * 40, 1)), ok_reader, None),
        ('main POST-E con un protegido de E ausente del sistema de archivos', runner(branch='main',
         ref_tree=disk_tree + f'100644 blob {"1" * 40}\tdocs/academico/evidencia-sbx/borrado.md\x00'), ok_reader, None),
        ('develop POST-E con un archivo real que no existe en E', runner(ref_tree=''.join(
            x + '\x00' for x in disk_tree.split('\x00') if x and not x.endswith(readme))), ok_reader, None),
        ('feature POST-E con modo distinto de 100644 en E', runner(branch=F35SBX_BRANCH, history=clean_e[1:],
         ref_tree=disk_tree.replace('100644 blob', '100755 blob', 1)), ok_reader, None),
        ('main POST-E con árbol de E vacío', runner(branch='main', ref_tree=''), ok_reader, None),
        ('develop POST-E con error de Git en ls-tree', runner(ls_tree_rc=128), ok_reader, None),
        # Transición del adaptador (negativos obligatorios 2 y 4–10).
        ('2 PRE-E con una línea extra en f35sbx_scope.py', pre_e, ok_reader, adapter_with(adapter=extra_adapter)),
        ('2 PRE-E con una línea extra en validate_f35sbx.py', pre_e, ok_reader, adapter_with(validator=extra_validator)),
        ('4 develop POST-E con f35sbx_scope.py modificado en el árbol', runner(branch='develop'), ok_reader,
         adapter_with(adapter=extra_adapter)),
        ('4 main POST-E con f35sbx_scope.py modificado y committeado tras E', runner(branch='main',
         history=after_e((x, [e_hash], {e_hash: [sc]})), diff=ADAPTER), ok_reader, adapter_with(adapter=extra_adapter)),
        ('8 main POST-E: scope modificado y revertido (contenido final = E)', runner(branch='main', history=after_e(
            (y, [x], {x: [sc]}), (x, [e_hash], {e_hash: [sc]}))), ok_reader, None),
        ('9 develop POST-E: validador modificado y revertido', runner(history=after_e(
            (y, [x], {x: [va]}), (x, [e_hash], {e_hash: [va]}))), ok_reader, None),
        ('10 main POST-E: ambos modificados con anclas recalculadas y revertidos (ataque coordinado)', runner(
            branch='main', history=after_e((y, [x], {x: both}), (x, [e_hash], {e_hash: both}))), ok_reader, None),
        ('11 develop POST-E: rama lateral modifica scope y el merge restaura E', runner(history=after_e(
            (m2, [e_hash, lat], {e_hash: [], lat: [sc]}), (lat, [e_hash], {e_hash: [sc]}))), ok_reader, None),
        ('12 main POST-E: rama lateral modifica el validador y el merge restaura E', runner(branch='main', history=after_e(
            (m2, [e_hash, lat], {e_hash: [], lat: [va]}), (lat, [e_hash], {e_hash: [va]}))), ok_reader, None),
        ('11b develop: rama lateral nacida en D modifica scope y se fusiona tras E', runner(history=after_e(
            (m2, [e_hash, lat], {e_hash: [sc], lat: both}), (lat, [AUDITED_CLOSURE], {AUDITED_CLOSURE: [sc]}))),
         ok_reader, None),
        ('13 main POST-E: merge commit que toca scope directamente', runner(branch='main', history=after_e(
            (m2, [e_hash, z], {e_hash: [sc], z: both}))), ok_reader, None),
        ('14 develop POST-E: merge commit que toca el validador directamente', runner(history=after_e(
            (m2, [e_hash, z], {e_hash: [va], z: both}))), ok_reader, None),
        ('10b main POST-E: revert de E seguido de un cherry-pick equivalente de E', runner(branch='main', history=after_e(
            (y, [x], {x: both}), (x, [e_hash], {e_hash: both}))), ok_reader, None),
        ('5 develop POST-E con f35sbx_scope.py eliminado', runner(branch='develop', diff=ADAPTER), ok_reader,
         adapter_with(adapter=None)),
        ('6 main POST-E con f35sbx_scope.py reemplazado por la versión D', runner(branch='main', diff=ADAPTER), ok_reader,
         adapter_with(adapter=adapter_d)),
        ('6 develop con E que contiene la versión D del adaptador', runner(branch='develop',
         e_files=dict(real, **{ADAPTER: adapter_d})), ok_reader, adapter_with(adapter=adapter_d)),
        ('7 main POST-E con ancla incorrecta en el árbol', runner(branch='main', diff=ADAPTER_VALIDATOR), ok_reader,
         adapter_with(validator=wrong_anchor)),
        ('7 develop con E de ancla incorrecta', runner(branch='develop', e_files=dict(real, **{ADAPTER_VALIDATOR:
         wrong_anchor})), ok_reader, adapter_with(validator=wrong_anchor)),
        ('7 develop con ancla duplicada', runner(branch='develop'), ok_reader,
         adapter_with(validator=real[ADAPTER_VALIDATOR] + validator_anchor)),
        ('develop sin evidencia de E (PRE-E)', runner(branch='develop', history=[]), ok_reader, None),
        ('main sin evidencia de E (PRE-E)', runner(branch='main', history=[]), ok_reader, None),
        ('error de Git en la historia del adaptador', runner(branch='main', history_rc=128), ok_reader, None),
        ('error de Git en la historia del adaptador (feature)', runner(branch=F35SBX_BRANCH, history=[], history_rc=128),
         ok_reader, None),
        ('error de Git en el diff de un commit de la historia', runner(branch='develop', pair_rc=128), ok_reader, None),
        ('error de Git en diff-tree de E', runner(branch='main', names_rc=128), ok_reader, None),
        ('error de Git al leer el contenido de E', runner(branch='develop', show_rc=128), ok_reader, None),
        ('commit sin padres en la historia', runner(branch='main', raw_log=f'{"a" * 40}\n'), ok_reader, None),
        ('E que no es hijo directo de D', runner(branch='main', history=[(e_hash, ['a' * 40], {'a' * 40: both})]),
         ok_reader, None),
        ('E como merge (dos padres)', runner(branch='develop', history=[
            (e_hash, [AUDITED_CLOSURE, 'a' * 40], {AUDITED_CLOSURE: both, 'a' * 40: both})]), ok_reader, None),
        ('E que cambia otro archivo', runner(branch='main', names='\n'.join(ADAPTED_IN_E + ('CLAUDE.md',))),
         ok_reader, None),
        ('E que solo cambia el adaptador', runner(branch='develop', names=ADAPTER), ok_reader, None),
        ('identificador de E no verificable', runner(branch='main', raw_log='HEAD~1 HEAD~2\n'), ok_reader, None),
        ('adaptador binario', runner(branch='develop'), ok_reader, lambda r, p: real[p].encode('utf-8') + b'\x00'),
        ('adaptador con CR', runner(branch='main'), ok_reader,
         lambda r, p: real[p].replace('\n', '\r\n').encode('utf-8')),
    ]
    for label, run, rd, ard in negatives:
        out.append((context(root, run, rd, ard) is None
                    and (ard is not None or (not validator_ok(f30, root, run, rd)
                                             and not governance_ok('CLAUDE.md', root, run, rd))),
                    f'rechazado (falla cerrado): {label}'))
    required = {'CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md', 'docs/academico/evidencia-sbx',
                'docs/academico/tools/f35sbx', 'docs/academico/tools/f34b/validate_f34b.py',
                'docs/academico/tools/f34e/validate_f34e.py', *HISTORICAL_VALIDATORS}
    out.append((required <= set(FROZEN_AFTER_CLOSURE) and not [x for x in FROZEN_AFTER_CLOSURE if x.startswith(':(')],
                'integración: artefactos congelados tras E completos y sin ninguna exclusión'))
    # Los estados de gobierno se rechazan por contenido, aunque Git no informe ningún cambio posterior a E.
    for label, old_, new_ in (('F35-SBX-B INICIADA', 'F35-SBX-B NO INICIADA.', 'F35-SBX-B INICIADA.'),
                              ('G0 real APROBADA', '- G0 real = NO APROBADA', '- G0 real = APROBADA'),
                              ('F35 productiva HABILITADA', '- F35 productiva = BLOQUEADA', '- F35 productiva = HABILITADA'),
                              ('alcance C HABILITADO', '- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO'),
                              ('datos reales PERMITIDOS', '- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS'),
                              ('ADR-005 APROBADO', '- ADR-005 = PROPUESTA', '- ADR-005 = APROBADO'),
                              ('F36–F40 HABILITADAS', '- F36–F40 = BLOQUEADAS', '- F36–F40 = HABILITADAS')):
        rd = reader(gov_with(old_, new_))
        out.append((all(context(root, runner(branch=b), rd) is None for b in sorted(INTEGRATION_BRANCHES)),
                    f'integración rechazada por contenido (sin diff de Git): {label}'))
    return out
