"""F35-SBX-B — validador del cierre de B1 (B1-FREEZE).

Uso:  python -I docs/academico/tools/f35sbxb_freeze/validate_f35sbxb_freeze.py
      (si se invoca sin -I, se relanza aislado)

Sobre HEAD de la rama de B, de `develop` o de `main`:

  FRZ  El conjunto congelado de B1 (las cinco rutas que B1 cambió respecto de la base de B) es idéntico a su blob en
       el ancla auditada 8e94a60, con modo 100644, en el árbol de HEAD, en cada commit descendiente del ancla, en el
       índice y en el sistema de archivos. Las carpetas de B y del cierre tienen exactamente su contenido, y el
       manifiesto coincide con Git.
  B1   Las reglas del gate de B1 (CTX, AIN, HST, B0F, SBX, GOV, FSY, FLG, CNT y DEP) sobre HEAD. El gate se ejecuta
       desde los bytes ya verificados contra el ancla. SCP usa el alcance de B1 más los tres archivos del cierre.
  FCN  Los archivos del cierre no contienen PII ni afirmaciones o declaraciones de estado prohibidas.
  FDP  Este validador solo usa la biblioteca estándar autorizada.

El commit de cierre no figura en ningún archivo: es posterior al ancla y se consulta en Git. Cualquier error de Git
o de lectura, o cualquier estado no evaluable, falla cerrado.
"""
import os
import sys

# Mismo aislamiento que el gate de B1 (B1.4): python -I, relanzado con os.spawnv antes de otra importación.
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

import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
ANCHOR = '8e94a60274fe39ebda3e9961bc58036b389dfc00'      # AUDITED_B1_ANCHOR: contenido de B1 aprobado
B_BASE = '430f3f544c3542cabac8028a122c8a0c2a97390b'      # develop al iniciar F35-SBX-B
GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
MANIFEST = 'docs/academico/tools/f35sbxb_freeze/b1_freeze_manifest.json'
VALIDATOR = 'docs/academico/tools/f35sbxb_freeze/validate_f35sbxb_freeze.py'
FREEZE_DOC = 'docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md'
FREEZE_FILES = (FREEZE_DOC, MANIFEST, VALIDATOR)
FROZEN_DIRS = {
    'docs/academico/evidencia-sbx-b': ('F35SBXB_B0_Sucesion_de_Gates.md', 'F35SBXB_B1_Gate_Sucesor.md', 'README.md'),
    'docs/academico/tools/f35sbxb': ('validate_f35sbxb.py',),
    'docs/academico/evidencia-sbx-b-freeze': ('F35SBXB_B1_Freeze.md',),
    'docs/academico/tools/f35sbxb_freeze': ('b1_freeze_manifest.json', 'validate_f35sbxb_freeze.py'),
}
GATE_MODULE = 'f35sbxb_gate_congelado'


class GitError(Exception):
    pass


def must(*args):
    try:
        p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    except OSError as e:
        raise GitError(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(args[:3])} → {p.returncode}')
    return p.stdout


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def no_link(rel):
    """Ninguno de los componentes de la ruta es un enlace."""
    parts = rel.split('/')
    return not any(os.path.islink(os.path.join(ROOT, *parts[:k])) for k in range(1, len(parts) + 1))


def real_bytes(rel):
    """Bytes de un archivo regular sin enlaces en su ruta; cualquier otro caso → None (falla cerrado)."""
    full = os.path.join(ROOT, rel)
    if not no_link(rel) or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def tree_entries(commit, paths):
    """{ruta: (modo, tipo, blob)} de las rutas en un commit; sin seguir renombrados."""
    out = {}
    for entry in must('ls-tree', '-z', commit, '--', *paths).split(b'\x00'):
        if entry:
            meta, _, path = entry.partition(b'\t')
            out[path.decode('utf-8', 'replace')] = tuple(meta.decode().split())
    return out


def frozen_problems(manifest):
    """FRZ: conjunto congelado, historia, índice, sistema de archivos y carpetas. (problemas, bytes verificados)."""
    out, verified = [], {}
    frozen = {e['path']: e for e in manifest.get('frozen_set', [])}
    paths = sorted(frozen)
    if manifest.get('audited_b1_anchor') != ANCHOR or manifest.get('b_base') != B_BASE:
        out.append('el manifiesto no declara el ancla auditada y la base de B de este validador')
    if {d: tuple(v) for d, v in manifest.get('frozen_dirs', {}).items()} != FROZEN_DIRS or \
            tuple(sorted(manifest.get('freeze_files', []))) != tuple(sorted(FREEZE_FILES)):
        out.append('el manifiesto no coincide con las carpetas y archivos del cierre de este validador')
    # 1. Ancla, ascendencia e historia completa.
    if must('cat-file', '-t', ANCHOR).strip() != b'commit':
        return out + ['el ancla auditada no es un commit (falla cerrado)'], verified
    if must('rev-parse', '--is-shallow-repository').strip() != b'false':
        return out + ['repositorio superficial: la historia posterior al ancla no es verificable (falla cerrado)'], verified
    p = subprocess.run(['git', 'merge-base', '--is-ancestor', ANCHOR, 'HEAD'], cwd=ROOT, capture_output=True)
    if p.returncode not in (0, 1):
        raise GitError(f'merge-base → {p.returncode}')
    if p.returncode == 1:
        return out + ['el ancla auditada no es ancestro de HEAD: B1 no está contenida (falla cerrado)'], verified
    # 2. El conjunto congelado se deriva de Git: lo que B1 cambió respecto de la base de B, en el ancla.
    parts = must('diff', '--name-status', '--no-renames', '-z', B_BASE, ANCHOR).split(b'\x00')
    derived = {parts[i + 1].decode(): parts[i].decode() for i in range(0, len(parts) - 1, 2) if parts[i]}
    if {p_: e.get('status_vs_base') for p_, e in frozen.items()} != derived:
        out.append(f'el conjunto congelado del manifiesto no es el delta de B1 en el ancla: {sorted(derived)}')
    anchor = tree_entries(ANCHOR, paths)
    for path, e in frozen.items():
        expected = ('100644', 'blob', e.get('blob'))
        if anchor.get(path) != expected:
            out.append(f'{path}: el manifiesto no coincide con su entrada en el ancla ({anchor.get(path)})')
            continue
        data = must('cat-file', 'blob', expected[2])
        if hashlib.sha256(data).hexdigest() != e.get('sha256') or len(data) != e.get('bytes'):
            out.append(f'{path}: SHA-256 o tamaño del manifiesto distinto del blob del ancla')
    if out:
        return out, verified
    # 3. Árbol de HEAD y cada commit descendiente del ancla que lleva a HEAD (incluidos los merges).
    head = tree_entries('HEAD', paths)
    out += [f'HEAD: {p_} ausente, renombrado o distinto del ancla (modo, tipo o bytes)' for p_ in paths
            if head.get(p_) != anchor[p_]]
    for commit in must('rev-list', '--ancestry-path', f'{ANCHOR}..HEAD').decode().split():
        entries = tree_entries(commit, paths)
        bad = [p_ for p_ in paths if entries.get(p_) != anchor[p_]]
        if bad:
            out.append(f'el commit {commit[:12]}, descendiente del ancla, altera el conjunto congelado: {bad[:3]}')
    # 4. Índice: entrada única en etapa 0 con el modo y el blob del ancla, y ningún flag que oculte cambios.
    index = {}
    for entry in must('ls-files', '-s', '-z', '--', *paths).split(b'\x00'):
        if entry:
            meta, _, path = entry.partition(b'\t')
            index.setdefault(path.decode('utf-8', 'replace'), []).append(tuple(meta.decode().split()))
    for p_ in paths:
        if index.get(p_) != [(anchor[p_][0], anchor[p_][2], '0')]:
            out.append(f'índice: {p_} ausente, en conflicto o distinto del ancla: {index.get(p_)}')
    flags = [x.decode('utf-8', 'replace') for x in must('ls-files', '-v', '-z').split(b'\x00') if x and not x.startswith(b'H ')]
    if flags:
        out.append(f'flags del índice que ocultan cambios (assume-unchanged o skip-worktree): {flags[:5]}')
    # 5. Sistema de archivos: archivo regular, sin enlaces, con los bytes del ancla y sin bit de ejecución.
    for p_ in paths:
        data = real_bytes(p_)
        if data is None:
            out.append(f'disco: {p_} ausente, enlace, objeto especial o ilegible')
        elif blob_id(data) != anchor[p_][2]:
            out.append(f'disco: {p_} con bytes distintos del ancla')
        else:
            if os.name != 'nt' and os.stat(os.path.join(ROOT, p_)).st_mode & 0o111:
                out.append(f'disco: {p_} con permiso de ejecución (el ancla registra 100644)')
            verified[p_] = data
    # 6. Carpetas de B y del cierre con su contenido exacto (también archivos ignorados u ocultos, sin __pycache__).
    for folder, names in FROZEN_DIRS.items():
        full = os.path.join(ROOT, folder)
        if not no_link(folder) or not os.path.isdir(full):
            out.append(f'{folder}: ausente, enlace o no es un directorio')
            continue
        try:
            entries = list(os.scandir(full))
        except OSError as e:
            out.append(f'{folder}: ilegible ({e.__class__.__name__})')
            continue
        found = sorted(x.name for x in entries)
        if found != sorted(names):
            out.append(f'{folder}: contenido distinto del autorizado: extra={sorted(set(found) - set(names))[:3]} '
                       f'faltan={sorted(set(names) - set(found))[:3]}')
        out += [f'{folder}/{x.name}: no es un archivo regular' for x in entries
                if x.is_symlink() or not x.is_file(follow_symlinks=False)]
    return out, verified


def load_gate(data):
    """Carga el gate de B1 desde los bytes ya verificados contra el ancla, sin releer el archivo."""
    path = os.path.join(ROOT, GATE)
    spec = importlib.util.spec_from_file_location(GATE_MODULE, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[GATE_MODULE] = module
    exec(compile(data, path, 'exec', dont_inherit=True), module.__dict__)
    return module


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    try:
        manifest = json.loads((real_bytes(MANIFEST) or b'').decode('utf-8'))
        frz, verified = frozen_problems(manifest)
    except (GitError, OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        manifest, frz, verified = None, [f'cierre no verificable ({e.__class__.__name__}: {e}): falla cerrado'], {}
    add(not frz, f'FRZ: {len(frz)} violaciones' + (f' — {frz[:3]}' if frz else ''))
    if frz or GATE not in verified:
        add(False, 'B1: reglas del gate de B1 no evaluables sin el gate verificado contra el ancla (falla cerrado)')
    else:
        try:
            gate = load_gate(verified[GATE])
            if [f'- {s}' for s in manifest['governance_states']] != gate.STATES:
                add(False, 'FRZ: los estados de gobierno del manifiesto no son los del gate congelado')
            gate.SCOPE.update({p: 'A' for p in FREEZE_FILES})      # alcance de B1 más los tres archivos del cierre
            running = sys.modules.pop('__main__', None)            # este validador no entra en DH-B13 (§ del cierre)
            try:
                S = gate.collect()
            finally:
                if running is not None:
                    sys.modules['__main__'] = running
            for rid, fn in gate.RULES.items():
                viol = fn(S)
                add(not viol, f'B1 {rid}: {len(viol)} violaciones' + (f' — {viol[:3]}' if viol else ''))
            sbx = S.get('sbx') or {}
            passed = sum(1 for k in gate.SBX_IDS if sbx.get(k, (False,))[0])
            print(f'SBX-01..SBX-18 sobre HEAD (DH-B13): {passed}/18 PASS' + ('' if sbx else f' — {S.get("sbx_error")}'))
            files = {p: real_bytes(p) for p in FREEZE_FILES}
            fcn = gate.r_cnt({'errors': [], 'files': files})
            add(not fcn, f'FCN: {len(fcn)} violaciones' + (f' — {fcn[:3]}' if fcn else ''))
            fdp = gate.r_dep({'errors': [], 'files': {VALIDATOR: files[VALIDATOR]}})
            add(not fdp, f'FDP: {len(fdp)} violaciones' + (f' — {fdp[:3]}' if fdp else ''))
        except Exception as e:      # cualquier fallo al evaluar las reglas reutilizadas: falla cerrado
            add(False, f'B1: evaluación no completada ({e.__class__.__name__}: {e}): falla cerrado')
    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    print(f'validate_f35sbxb_freeze: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
