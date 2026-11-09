"""Sondas reproducibles de T-09 y pruebas S-T11 a S-T17 de la especificación S (B-01). Biblioteca estándar.

PREPARACIÓN — B-01 NO ESTÁ IMPLEMENTADO. Este script no modifica `validate_f36sbx.py`, no crea evidencia del gate
y no mueve ninguna ref del repositorio: clona en un directorio temporal, prueba allí y borra el clon.

Las sondas V-1 a V-7 y S-T04 miden el validador v3 tal como está. Las marcadas «admitida» cargan el validador del
clon y, solo en memoria y solo en ese proceso, añaden la rama de H a `BRANCHES` (lo que haría T-04) o cambian `BASE`
(T-09 (b)). Así se observa hoy qué haría FRZ con cada elección, sin escribir B-01. Lo que depende de la lógica nueva
de B-01 (S-T01 a S-T03 y S-T05 a S-T10) no se puede observar aquí.

Uso, desde cualquier directorio:
    python -I -B docs/academico/preparacion-f36-b01/sondas_t09.py [--solo ID] [--raiz RUTA_DEL_REPOSITORIO]
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
VALIDATOR = 'docs/academico/tools/f36sbx/validate_f36sbx.py'
PACKAGE = 'docs/academico/f36-sbx'

MAIN_AF5 = '55f758e013e1852de8c8daa5d6fde95e39b02b0d'
DEVELOP_SEG = '9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9'
H_PRELIMINAR = '1d5d6aa'
EXPEDIENTE = 'f5003c967e0caa19f4236bae0705de08f33fae12'
BASE_V3 = 'b8892af39a6492d8dd44a36290604efc602380cd'
BRANCHES_V3 = ['develop', 'feature/f36-sbx-authorization-design', 'main']
H_BRANCH = 'feature/f36-sbx-h-sonda'  # nombre de prueba: la rama real de H es T-04, NO EMITIDA

# Identifican cada comprobación del validador por un fragmento estable de su mensaje.
RAMA = 'rama admitida'
ANCESTRO = 'es ancestro de HEAD'
ALCANCE = 'cambios solo en el paquete'
RUNTIME = '0 cambios de runtime'
AUTO = 'los criterios AUTO'

RUNNER = r'''
import importlib.util, json, sys
path, extra, base = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('validate_f36sbx', path)
v = importlib.util.module_from_spec(spec)
sys.modules['validate_f36sbx'] = v
spec.loader.exec_module(v)
if extra:
    v.BRANCHES = frozenset(set(v.BRANCHES) | {extra})
if base:
    v.BASE = base
s = v.collect(v.ROOT)
results, gate = v.run(s)
print(json.dumps({'branch': s['branch'], 'gate': gate, 'ok': sum(1 for r in results if r[1]),
                  'fails': [r[2] for r in results if not r[1]], 'base': v.BASE, 'branches': sorted(v.BRANCHES)}))
'''


def probe(pid, start, branch, fails, total=None, overlay=None, extra=None, admit=False, base=None, at_least=False):
    return {'id': pid, 'start': start, 'branch': branch, 'fails': set(fails), 'total': total, 'overlay': overlay,
            'extra': extra, 'admit': admit, 'base': base, 'at_least': at_least}


def probes(head: str) -> list[dict]:
    h = {'start': MAIN_AF5, 'branch': H_BRANCH, 'overlay': EXPEDIENTE}
    return [
        probe('V-1', MAIN_AF5, 'main', [], 59),
        probe('V-2', DEVELOP_SEG, 'develop', [ALCANCE, RUNTIME, AUTO], 59),
        probe('V-3', MAIN_AF5, 'main', [], 59, overlay=H_PRELIMINAR),
        probe('V-4', DEVELOP_SEG, 'develop', [ALCANCE, RUNTIME, AUTO], 59, overlay=H_PRELIMINAR),
        probe('V-5', MAIN_AF5, 'main', [], 59, overlay=EXPEDIENTE),
        probe('V-6', MAIN_AF5, None, [RAMA, AUTO], 59, overlay=H_PRELIMINAR),
        probe('V-7', head, 'feature/continuacion-f36-f40', [RAMA, ALCANCE, RUNTIME, AUTO], 59),
        probe('S-T04', DEVELOP_SEG, 'develop', [ALCANCE, RUNTIME, AUTO], 59),
        probe('S-T11 RED', fails=[RAMA, AUTO], total=59, **h),
        probe('S-T11', fails=[], total=59, admit=True, **h),
        probe('S-T12 app', fails=[ALCANCE, RUNTIME, AUTO], total=59, admit=True, extra='app/SondaT09.php', **h),
        probe('S-T12 tests', fails=[ALCANCE, RUNTIME, AUTO], total=59, admit=True, extra='tests/SondaT09.php', **h),
        probe('S-T12 dependencias', fails=[ALCANCE, RUNTIME, AUTO], total=59, admit=True, extra='composer.json', **h),
        probe('S-T13', MAIN_AF5, 'feature/otra-rama', [RAMA, AUTO], 59, overlay=EXPEDIENTE, admit=True),
        probe('S-T14', DEVELOP_SEG, H_BRANCH, [ALCANCE, RUNTIME, AUTO], 59, admit=True),
        probe('S-T16', MAIN_AF5, 'main', [ANCESTRO], base=DEVELOP_SEG, at_least=True),
    ]


def run(args, cwd, check=True) -> str:
    done = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                          env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    if check and done.returncode != 0:
        raise RuntimeError(f'{" ".join(args)}\n{done.stderr}')
    return done.stdout.strip()


def execute(clone: pathlib.Path, p: dict) -> dict:
    run(['git', 'reset', '-q', '--hard'], clone)
    run(['git', 'clean', '-qfdx'], clone)
    if p['branch']:
        run(['git', 'checkout', '-q', '-f', '-B', p['branch'], p['start']], clone)
    else:
        run(['git', 'checkout', '-q', '-f', '--detach', p['start']], clone)
    if p['overlay']:
        run(['git', 'checkout', '-q', p['overlay'], '--', PACKAGE], clone)
    if p['extra']:
        target = clone / p['extra']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'{"sonda": "T-09"}\n')
    out = run([sys.executable, '-I', '-B', '-c', RUNNER, str(clone / VALIDATOR), H_BRANCH if p['admit'] else '',
               p['base'] or ''], tempfile.gettempdir())
    return json.loads(out.splitlines()[-1])


def failed_checks(result: dict) -> set[str]:
    known = (RAMA, ANCESTRO, ALCANCE, RUNTIME, AUTO)
    found = set()
    for message in result['fails']:
        found.add(next((k for k in known if k in message), message))
    return found


def compare(p: dict, r: dict) -> str | None:
    got = failed_checks(r)
    if p['at_least']:
        return None if p['fails'] <= got else f'faltan {sorted(p["fails"] - got)}'
    if got != p['fails']:
        return f'esperadas {sorted(p["fails"])}, obtenidas {sorted(got)}'
    total = r['ok'] + len(r['fails'])
    if p['total'] is not None and total != p['total']:
        return f'total {total}, esperado {p["total"]}'
    return None if r['gate'] == 'NO SUPERADO' else f'gate {r["gate"]}'


def remove(path: pathlib.Path) -> None:
    def retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onerror=retry)


def main(argv: list[str]) -> int:
    only = argv[argv.index('--solo') + 1] if '--solo' in argv else None
    root = pathlib.Path(argv[argv.index('--raiz') + 1]) if '--raiz' in argv else ROOT
    common = pathlib.Path(run(['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'], root))
    head = run(['git', 'rev-parse', 'HEAD'], root)
    workspace = pathlib.Path(tempfile.mkdtemp(prefix='sondas-t09-'))
    clone = workspace / 'clon'
    bad = 0
    try:
        run(['git', 'clone', '-q', '--no-hardlinks', '--no-checkout', str(common), str(clone)], workspace)
        run(['git', 'checkout', '-q', '-f', '--detach', MAIN_AF5], clone)
        constants = execute(clone, probe('S-T15', MAIN_AF5, 'main', []))
        checks = [('S-T15', constants['base'] == BASE_V3, f'BASE = {constants["base"][:7]}'),
                  ('S-T17', constants['branches'] == BRANCHES_V3, f'BRANCHES = {constants["branches"]}')]
        for pid, ok, detail in checks:
            if only in (None, pid):
                print(f'{"OK   " if ok else "FALLA"} {pid}: {detail}')
                bad += 0 if ok else 1
        for p in probes(head):
            if only not in (None, p['id']):
                continue
            result = execute(clone, p)
            problem = compare(p, result)
            print(f'{"OK   " if problem is None else "FALLA"} {p["id"]}: {result["ok"]}/{len(result["fails"])} · '
                  f'rama {result["branch"]} · gate {result["gate"]} · {sorted(failed_checks(result))}'
                  + (f' · {problem}' if problem else ''))
            bad += 1 if problem else 0
    finally:
        remove(workspace)
    print(f'sondas_t09: {bad} discrepancias; clon temporal eliminado: {not workspace.exists()}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
