"""Sonda de la especificación S v2.2 (§5.9.5): un H trasplantado lleva las sondas y puede ejecutarlas. Biblioteca estándar.

PREPARACIÓN — B-01 NO ESTÁ IMPLEMENTADO. No modifica `validate_f36sbx.py` ni ninguna ref del repositorio. En un clon
temporal crea la rama de prueba de H desde el commit `55f758e` (T-09 (a-ii)), trasplanta `docs/academico/f36-sbx/` de
la revisión indicada (por defecto, HEAD de la raíz), hace un commit sintético y comprueba:

    T-1  inventario: `git diff --name-only 55f758e <H>` cabe en el perímetro de AC-05 e incluye `sondas-b01/`;
    T-2  enlaces: todo enlace relativo de S y del README de las sondas resuelve en ese árbol, dentro del paquete;
    T-3  FRZ: el validador del clon, con la rama de prueba admitida solo en memoria, da 0 fallas y R = NO SUPERADO;
    T-4  ejecución: `sondas_t09.py` y `sonda_revocacion.py`, lanzados desde el árbol trasplantado, salen con código 0.

Con `--paquete ARBOL` trasplanta los archivos del árbol de trabajo de la raíz (versionados o no ignorados), para
probar antes de un commit. El H de prueba es sintético; no es H, que sigue sin fijar (T-04 y T-09, NO EMITIDAS).

Uso, desde cualquier directorio:
    python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sonda_trasplante.py [--paquete REV|ARBOL] [--raiz RUTA]
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
MAIN_AF5 = '55f758e013e1852de8c8daa5d6fde95e39b02b0d'
PKG = 'docs/academico/f36-sbx'
TOOLS = 'docs/academico/tools/f36sbx'
GOV_FILES = ('CLAUDE.md', 'README.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md')
VALIDATOR = TOOLS + '/validate_f36sbx.py'
SONDAS = PKG + '/expediente-final/sondas-b01'
REQUIRED = [f'{SONDAS}/{n}' for n in ('README.md', 'sondas_t09.py', 'sonda_revocacion.py', 'sonda_trasplante.py')]
LINKED = [PKG + '/expediente-final/F36SBX_B01_Especificacion_S.md', SONDAS + '/README.md']
H_BRANCH = 'feature/f36-sbx-h-sonda'  # nombre de prueba: la rama real de H es T-04, NO EMITIDA
LINK = re.compile(r'\]\(([^)\s]+)\)')
DATE = '2026-11-09T12:00:00-05:00'
IDENTITY = ['-c', 'user.name=Sonda S v2.2', '-c', 'user.email=sonda.invalid']

RUNNER = r'''
import importlib.util, json, sys
path, extra = sys.argv[1:3]
spec = importlib.util.spec_from_file_location('validate_f36sbx', path)
v = importlib.util.module_from_spec(spec)
sys.modules['validate_f36sbx'] = v
spec.loader.exec_module(v)
v.BRANCHES = frozenset(set(v.BRANCHES) | {extra})
s = v.collect(v.ROOT)
results, gate = v.run(s)
print(json.dumps({'branch': s['branch'], 'gate': gate, 'ok': sum(1 for r in results if r[1]),
                  'fails': [r[2] for r in results if not r[1]]}))
'''


def run(args, cwd, check=True, env=None) -> subprocess.CompletedProcess:
    done = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                          env={**os.environ, 'PYTHONIOENCODING': 'utf-8', **(env or {})})
    if check and done.returncode != 0:
        raise RuntimeError(f'{" ".join(map(str, args))}\n{done.stderr}')
    return done


def out(args, cwd) -> str:
    return run(args, cwd).stdout.strip()


def transplant(root: pathlib.Path, clone: pathlib.Path, source: str) -> None:
    if source != 'ARBOL':
        out(['git', 'checkout', '-q', source, '--', PKG], clone)
        return
    shutil.rmtree(clone / PKG)
    for rel in out(['git', 'ls-files', '-co', '--exclude-standard', '--', PKG], root).splitlines():
        if (root / rel).is_file():
            (clone / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / rel, clone / rel)


def broken_links(clone: pathlib.Path) -> list[str]:
    bad, pkg = [], (clone / PKG).resolve()
    for rel in LINKED:
        if not (clone / rel).is_file():
            bad.append(f'{rel}: el documento no existe en el árbol')
            continue
        text = (clone / rel).read_text(encoding='utf-8')
        for target in LINK.findall(text):
            if target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            path = ((clone / rel).parent / target.split('#')[0]).resolve()
            if not path.exists():
                bad.append(f'{rel}: {target} no existe')
            elif pkg not in (path, *path.parents):
                bad.append(f'{rel}: {target} sale del paquete')
    return bad


def remove(path: pathlib.Path) -> None:
    def retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onerror=retry)


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[argv.index('--raiz') + 1]) if '--raiz' in argv else \
        pathlib.Path(out(['git', 'rev-parse', '--show-toplevel'], HERE))
    source = argv[argv.index('--paquete') + 1] if '--paquete' in argv else out(['git', 'rev-parse', 'HEAD'], root)
    common = pathlib.Path(out(['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'], root))
    workspace = pathlib.Path(tempfile.mkdtemp(prefix='sonda-trasplante-'))
    clone, bad = workspace / 'clon', 0

    def report(pid, ok, detail):
        nonlocal bad
        bad += 0 if ok else 1
        print(f'{"OK   " if ok else "FALLA"} {pid}: {detail}')

    try:
        out(['git', 'clone', '-q', '--no-hardlinks', '--no-checkout', str(common), str(clone)], workspace)
        out(['git', 'checkout', '-q', '-f', '-B', H_BRANCH, MAIN_AF5], clone)
        transplant(root, clone, source)
        out(['git', 'add', '-A', '--', PKG], clone)
        run(['git', *IDENTITY, 'commit', '-q', '-m', f'H de prueba: trasplante de {PKG} ({source[:12]})'], clone,
            env={'GIT_AUTHOR_DATE': DATE, 'GIT_COMMITTER_DATE': DATE})
        h = out(['git', 'rev-parse', 'HEAD'], clone)
        print(f'H de prueba {h[:12]} en {H_BRANCH}, desde {MAIN_AF5[:7]}, con el paquete de {source[:12]}')

        inventory = out(['git', 'diff', '--name-only', MAIN_AF5, h], clone).splitlines()
        outside = [p for p in inventory if not (p.startswith(PKG + '/') or p.startswith(TOOLS + '/') or p in GOV_FILES)]
        missing = [p for p in REQUIRED if p not in inventory]
        report('T-1 inventario', not outside and not missing,
               f'{len(inventory)} rutas; fuera de AC-05: {outside}; faltan de sondas-b01: {missing}')

        links = broken_links(clone)
        report('T-2 enlaces', not links, f'{len(LINKED)} documentos; rotos o fuera del paquete: {links}')

        result = json.loads(out([sys.executable, '-I', '-B', '-c', RUNNER, str(clone / VALIDATOR), H_BRANCH],
                                tempfile.gettempdir()).splitlines()[-1])
        report('T-3 FRZ', not result['fails'] and result['gate'] == 'NO SUPERADO',
               f'{result["ok"]}/{len(result["fails"])} · rama {result["branch"]} · gate {result["gate"]} · '
               f'{result["fails"]}')

        for name in ('sondas_t09.py', 'sonda_revocacion.py'):
            done = run([sys.executable, '-I', '-B', str(clone / SONDAS / name), '--raiz', str(clone)],
                       tempfile.gettempdir(), check=False)
            last = (done.stdout.strip().splitlines() or ['(sin salida)'])[-1]
            report(f'T-4 {name}', done.returncode == 0, f'código {done.returncode} · {last}')
    finally:
        remove(workspace)
    print(f'sonda_trasplante: {bad} discrepancias; clon temporal eliminado: {not workspace.exists()}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
