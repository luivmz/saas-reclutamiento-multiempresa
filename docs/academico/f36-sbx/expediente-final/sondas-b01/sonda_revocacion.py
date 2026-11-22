"""Sonda de la especificación S v2.2 (§5.8.2): el delta de revocación después de H es distinguible. Biblioteca estándar.

PREPARACIÓN — B-01 NO ESTÁ IMPLEMENTADO. Es una sonda de la especificación, no la validación funcional de AC-10:
no ejecuta ni modifica `validate_f36sbx.py`, no crea evidencia del gate en el repositorio y no mueve ninguna ref.
Clona en un directorio temporal, crea allí commits sintéticos (un H y sus sucesores) y borra el clon.

Comprueba que la definición de §5.8.2 basta para separar el delta permitido (documento de determinación en su ruta
fija, `revocation` de nulo a un evento válido, FG-14 de CUMPLE a NO CUMPLE, `declared_result` a REVOCADO y la celda
Estado de FG-14 en el documento del gate) de cualquier otro con una ruta o un campo adicional, o al que le falte una
de las tres transiciones de X2-R, que C-R.4 exige juntas. `delta_errors()` es
la definición de referencia escrita a partir de S; la comprobación real será la de B-01, con su RED y su GREEN.

Fuera de esta sonda: las líneas canónicas E2 a E7 (X3 a X5), cuyo texto depende de T-01 y D-07, y el caso de una
revocación posterior a SUPERADO, en el que el delta admitido es la unión con el de X1 y X2.

Uso, desde cualquier directorio:
    python -I -B docs/academico/f36-sbx/expediente-final/sondas-b01/sonda_revocacion.py [--raiz RUTA]
"""

from __future__ import annotations

import hashlib
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
GATE_STATE = PKG + '/gate/f36sbx_gate_state.json'
GATE_DOC = PKG + '/F36SBX_Gate_Sucesor.md'
GATE_EVIDENCE = PKG + '/gate/evidencia/'
DETERMINATION = GATE_EVIDENCE + 'REVOCACION_DETERMINACION.md'
CHARTER = PKG + '/F36SBX_Charter.md'
GROUNDS = {'charter_7_1', 'charter_7_2', 'charter_7_3', 'charter_7_4', 'gate_5_tei21', 'gate_5_retirada'}
REVOCATION_KEYS = {'date', 'effective_from', 'ground', 'determination', 'evidence'}
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
INSTANT = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
SHA256 = re.compile(r'^[0-9a-f]{64}$')
H_DATE = '2026-11-09T12:00:00-05:00'
X_DATE = '2026-11-10T12:00:00-05:00'
IDENTITY = ['-c', 'user.name=Sonda S v2.2', '-c', 'user.email=sonda.invalid']


def run(args, cwd, check=True, env=None) -> str:
    done = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                          env={**os.environ, 'PYTHONIOENCODING': 'utf-8', **(env or {})})
    if check and done.returncode != 0:
        raise RuntimeError(f'{" ".join(args)}\n{done.stderr}')
    return done.stdout.strip()


# ------------------------------------------------------------------ definición de referencia del delta (§5.8.2)
def revocation_errors(rev, h_date: str, h_paths: set[str]) -> list[str]:
    if not isinstance(rev, dict) or set(rev) != REVOCATION_KEYS:
        return [f'revocation: claves distintas de {sorted(REVOCATION_KEYS)}']
    e = []
    if not (isinstance(rev['date'], str) and DATE.match(rev['date']) and rev['date'] >= h_date):
        e.append('revocation.date: fecha inválida o anterior a H')
    if not (isinstance(rev['effective_from'], str) and INSTANT.match(rev['effective_from'])):
        e.append('revocation.effective_from: instante inválido')
    if rev['ground'] not in GROUNDS:
        e.append('revocation.ground: motivo no admitido')
    if rev['determination'] != DETERMINATION:
        e.append(f'revocation.determination: debe ser exactamente {DETERMINATION}')
    ev = rev['evidence']
    if not (isinstance(ev, list) and ev and all(isinstance(x, str) and (SHA256.match(x) or x in h_paths) for x in ev)):
        e.append('revocation.evidence: cada entrada es un SHA-256 o una ruta que ya existe en H')
    return e


def flatten(state: dict) -> dict:
    """Campos del estado: `criteria` por id y `revocation` como un valor atómico."""
    out = {}
    for key, value in state.items():
        if key == 'criteria' and isinstance(value, list):
            for c in value:
                for ck, cv in (c.items() if isinstance(c, dict) else ()):
                    out[f'criteria[{c.get("id")}].{ck}'] = cv
        else:
            out[key] = value
    return out


def fg_row(line: str):
    cells = [c.strip() for c in line.strip().strip('|').split(' | ')]
    return cells if line.startswith('| FG-') and len(cells) == 5 else None


def delta_errors(repo: pathlib.Path, h: str, x: str) -> list[str]:
    paths = set(run(['git', 'diff', '--no-renames', '--name-only', h, x], repo).splitlines())
    h_state = json.loads(run(['git', 'show', f'{h}:{GATE_STATE}'], repo))
    x_state = json.loads(run(['git', 'show', f'{x}:{GATE_STATE}'], repo))
    a, b = flatten(h_state), flatten(x_state)
    x2r = {'criteria[FG-14].status': ('CUMPLE', 'NO CUMPLE'), 'declared_result': ('NO SUPERADO', 'REVOCADO'),
           'revocation': (None, 'evento')}
    # C-R.1 y C-R.4: X1-R y X2-R se habilitan solo si las tres transiciones de X2-R se dan juntas. El evento (C-R.2)
    # lo comprueba revocation_errors() y el documento (C-R.3), la comprobación de la determinación.
    attempted = h_state.get('revocation') is None and x_state.get('revocation') is not None
    missing = [f for f in sorted(x2r) if f != 'revocation' and (a.get(f), b.get(f)) != x2r[f]]
    revoked = attempted and not missing
    errors = [f'C-R.4: faltan transiciones de X2-R: {missing}'] if attempted and missing else []

    allowed = {GATE_STATE, GATE_DOC} | ({DETERMINATION} if revoked else set())
    outside = sorted(paths - allowed)
    if outside:
        errors.append(f'ruta fuera del delta: {outside}')

    if revoked:
        h_paths = set(run(['git', 'ls-tree', '-r', '--name-only', h], repo).splitlines())
        h_date = run(['git', 'show', '-s', '--format=%cs', h], repo)
        errors += revocation_errors(x_state['revocation'], h_date, h_paths)
        entry = run(['git', 'ls-tree', x, '--', DETERMINATION], repo).split()
        if DETERMINATION not in paths or not entry or entry[0] != '100644' or entry[1] != 'blob':
            errors.append('determinación: falta, o no es un blob regular 100644 añadido después de H')
        elif not run(['git', 'show', f'{x}:{DETERMINATION}'], repo).startswith('[SINTÉTICO]'):
            errors.append('determinación: en esta sonda debe ser sintética')

    transitions = x2r if revoked else {}
    for field in sorted(set(a) | set(b)):
        if a.get(field, '∅') == b.get(field, '∅'):
            continue
        rule = transitions.get(field)
        ok = rule is not None and a.get(field) == rule[0] and (field == 'revocation' or b.get(field) == rule[1])
        if not ok:
            errors.append(f'campo fuera del delta: {field}')

    if GATE_DOC in paths:
        old = run(['git', 'show', f'{h}:{GATE_DOC}'], repo).split('\n')
        new = run(['git', 'show', f'{x}:{GATE_DOC}'], repo).split('\n')
        same_shape = len(old) == len(new)
        for p, q in zip(old, new) if same_shape else ():
            if p == q:
                continue
            cp, cq = fg_row(p), fg_row(q)
            if not (revoked and cp and cq and cp[0] == 'FG-14' and cp[:4] == cq[:4]
                    and (cp[4], cq[4]) == ('CUMPLE', 'NO CUMPLE')):
                errors.append(f'documento del gate: línea fuera del delta ({(cp or [p[:20]])[0]})')
        if not same_shape:
            errors.append('documento del gate: cambia el número de líneas')
    return errors


# ------------------------------------------------------------------------------------------- escenarios
def write(repo: pathlib.Path, rel: str, data: bytes) -> None:
    target = repo / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def replace(repo: pathlib.Path, rel: str, old: bytes, new: bytes) -> None:
    data = (repo / rel).read_bytes()
    if data.count(old) != 1:
        raise RuntimeError(f'{rel}: el fragmento a sustituir no aparece una sola vez: {old[:60]!r}')
    (repo / rel).write_bytes(data.replace(old, new))


def revocation_event(determination: str = DETERMINATION, extra: dict | None = None) -> dict:
    return {'date': '2026-11-10', 'effective_from': '2026-11-10T09:00:00-05:00', 'ground': 'gate_5_retirada',
            'determination': determination,
            'evidence': [CHARTER, hashlib.sha256(b'[SINTETICO] determinacion').hexdigest()], **(extra or {})}


def set_revocation(repo, event) -> None:
    replace(repo, GATE_STATE, b'"revocation": null', b'"revocation": ' + json.dumps(event, ensure_ascii=False).encode())


def set_fg14(repo) -> None:
    replace(repo, GATE_STATE, b'{"id": "FG-14", "kind": "auto", "status": "CUMPLE"}',
            b'{"id": "FG-14", "kind": "auto", "status": "NO CUMPLE"}')
    data = (repo / GATE_DOC).read_bytes()
    lines = data.split(b'\n')
    idx = [i for i, ln in enumerate(lines) if ln.startswith(b'| FG-14 |')]
    if len(idx) != 1 or not lines[idx[0]].rstrip(b'\r').endswith(b'| CUMPLE |'):
        raise RuntimeError('documento del gate: fila FG-14 no encontrada')
    lines[idx[0]] = lines[idx[0]].replace(b'| CUMPLE |', b'| NO CUMPLE |')
    (repo / GATE_DOC).write_bytes(b'\n'.join(lines))


def set_declared(repo) -> None:
    replace(repo, GATE_STATE, b'"declared_result": "NO SUPERADO"', b'"declared_result": "REVOCADO"')


def determination(repo, rel=DETERMINATION) -> None:
    write(repo, rel, '[SINTÉTICO] Documento de determinación de la sonda S v2.2. No es un acto del equipo.\n'.encode())


def permitted(repo, event=None) -> None:
    determination(repo)
    set_revocation(repo, event or revocation_event())
    set_fg14(repo)
    set_declared(repo)


SCENARIOS = [
    ('S-T18', 'delta permitido', lambda r: permitted(r), None),
    ('S-T19 evidencia', 'S-T18 más un archivo en gate/evidencia/',
     lambda r: (permitted(r), write(r, GATE_EVIDENCE + 'NOTA.md', b'[SINTETICO] nota\n')), 'ruta fuera del delta'),
    ('S-T19 paquete', 'S-T18 más un archivo del paquete',
     lambda r: (permitted(r), write(r, PKG + '/NOTA_REVOCACION.md', b'[SINTETICO] nota\n')), 'ruta fuera del delta'),
    ('S-T20 campo', 'S-T18 más `f37_authorized_ei` cambiado',
     lambda r: (permitted(r), replace(r, GATE_STATE, b'"f37_authorized_ei": null', b'"f37_authorized_ei": []')),
     'campo fuera del delta: f37_authorized_ei'),
    ('S-T20 criterio', 'S-T18 más FG-13 en NO CUMPLE',
     lambda r: (permitted(r), replace(r, GATE_STATE, b'{"id": "FG-13", "kind": "auto", "status": "CUMPLE"}',
                                      b'{"id": "FG-13", "kind": "auto", "status": "NO CUMPLE"}')),
     'campo fuera del delta: criteria[FG-13].status'),
    ('S-T20 revocation', 'S-T18 con una clave adicional en `revocation`',
     lambda r: permitted(r, revocation_event(extra={'note': 'x'})), 'revocation: claves distintas'),
    ('S-T21 FG-14', 'FG-14 en NO CUMPLE sin revocación',
     lambda r: set_fg14(r), 'campo fuera del delta: criteria[FG-14].status'),
    ('S-T21 determinación', 'documento de determinación sin revocación',
     lambda r: determination(r), 'ruta fuera del delta'),
    ('S-T21 ruta citada', 'revocación que cita y añade otra ruta de determinación',
     lambda r: (determination(r, GATE_EVIDENCE + 'OTRA.md'), set_revocation(r, revocation_event(GATE_EVIDENCE + 'OTRA.md')),
                set_fg14(r), set_declared(r)), 'revocation.determination'),
    # C-R.4: con la determinación y el evento, falta una de las tres transiciones de X2-R o faltan ambas.
    ('S-T21 sin FG-14', 'determinación y evento; FG-14 sigue en CUMPLE',
     lambda r: (determination(r), set_revocation(r, revocation_event()), set_declared(r)),
     "C-R.4: faltan transiciones de X2-R: ['criteria[FG-14].status']"),
    ('S-T21 sin declared_result', 'determinación y evento; declared_result sigue en NO SUPERADO',
     lambda r: (determination(r), set_revocation(r, revocation_event()), set_fg14(r)),
     "C-R.4: faltan transiciones de X2-R: ['declared_result']"),
    ('S-T21 sin ambas', 'determinación y evento; FG-14 y declared_result conservan su valor de H',
     lambda r: (determination(r), set_revocation(r, revocation_event())),
     "C-R.4: faltan transiciones de X2-R: ['criteria[FG-14].status', 'declared_result']"),
]


def commit(repo, message, date) -> str:
    run(['git', 'add', '-A'], repo)
    run(['git', *IDENTITY, 'commit', '-q', '--allow-empty', '-m', message], repo,
        env={'GIT_AUTHOR_DATE': date, 'GIT_COMMITTER_DATE': date})
    return run(['git', 'rev-parse', 'HEAD'], repo)


def remove(path: pathlib.Path) -> None:
    def retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onerror=retry)


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[argv.index('--raiz') + 1]) if '--raiz' in argv else \
        pathlib.Path(run(['git', 'rev-parse', '--show-toplevel'], HERE))
    common = pathlib.Path(run(['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'], root))
    workspace = pathlib.Path(tempfile.mkdtemp(prefix='sonda-revocacion-'))
    clone, bad = workspace / 'clon', 0
    try:
        run(['git', 'clone', '-q', '--no-hardlinks', '--no-checkout', str(common), str(clone)], workspace)
        run(['git', 'checkout', '-q', '-f', '-B', 'sonda/h-sintetico', MAIN_AF5], clone)
        h = commit(clone, 'H sintético de la sonda S v2.2 (sin evidencia)', H_DATE)
        for pid, label, apply, expected in SCENARIOS:
            run(['git', 'checkout', '-q', '-f', '-B', 'sonda/x', h], clone)
            run(['git', 'clean', '-qfdx'], clone)
            apply(clone)
            x = commit(clone, f'{pid} (sintético)', X_DATE)
            errors = delta_errors(clone, h, x)
            ok = errors == [] if expected is None else any(expected in err for err in errors)
            bad += 0 if ok else 1
            verdict = 'admitido' if not errors else 'rechazado'
            print(f'{"OK   " if ok else "FALLA"} {pid}: {label} -> {verdict}'
                  + (f' · {errors}' if errors else '') + ('' if ok else f' · esperado: {expected or "admitido"}'))
    finally:
        remove(workspace)
    print(f'sonda_revocacion: {bad} discrepancias; clon temporal eliminado: {not workspace.exists()}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
