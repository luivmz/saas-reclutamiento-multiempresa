#!/usr/bin/env python3
"""Pruebas con Git real del vínculo entre el ADR sucesor y el blob de su commit candidato (AF3-M01).

En memoria, test_f36sbx.py solo puede simular la resolución Git del ADR. Aquí se usa Git de verdad:

- U: un repositorio mínimo y desechable, para la resolución de objetos (blob regular, ejecutable, enlace,
  submódulo, árbol, sin versionar, ignorado, otro commit, comodines, mayúsculas y bytes del árbol de trabajo);
- G: un clon local compartido y desechable del repositorio, con el paquete del árbol de trabajo, un commit
  candidato con un ADR sintético y evidencia SINTÉTICA de FG-03 y FG-12 sin confirmar, sobre el que se ejecuta el
  validador completo: un control positivo y los ataques de AF3-M01.

Todo ocurre en el directorio temporal del sistema y se borra al terminar. Nunca escribe en el repositorio original
(se comprueba antes y después), no usa red y no registra evidencia real.

Uso: python -I -B docs/academico/tools/f36sbx/test_f36sbx_git.py
"""
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_f36sbx as v  # noqa: E402

BRANCH = 'feature/f36-sbx-authorization-design'
IDENTITY = ['-c', 'user.name=F36SBX prueba sintetica', '-c', 'user.email=f36sbx-prueba@localhost']
CDATE = '2026-10-27'
COMMIT_ENV = {'GIT_AUTHOR_DATE': f'{CDATE}T12:00:00+0000', 'GIT_COMMITTER_DATE': f'{CDATE}T12:00:00+0000'}
ADR_PATH = 'docs/academico/f36-sbx/ADR_006_prueba_git.md'
TREE_PATH = 'docs/academico/f36-sbx/adr_carpeta.md'
IGNORED_ADR = 'docs/academico/f36-sbx/htmlcov/ADR_006_ignorado.md'
UNTRACKED_ADR = 'docs/academico/f36-sbx/ADR_007_sin_versionar.md'
LATER_ADR = 'docs/academico/f36-sbx/ADR_008_posterior.md'
EV = v.GATE_EVIDENCE

results = []


def ok(cond, cid, desc, detail=''):
    results.append((bool(cond), cid, desc, detail))


def git(cwd, *args, stdin=None, env=None):
    r = subprocess.run(['git', *IDENTITY, *args], cwd=cwd, input=stdin, capture_output=True,
                       env={**os.environ, **(env or {})})
    if r.returncode:
        raise RuntimeError(f'git {" ".join(args)}: {r.stderr.decode("utf-8", "replace").strip()}')
    return r.stdout.decode('utf-8', 'replace').strip()


def commit(cwd, msg):
    git(cwd, 'commit', '-q', '-m', msg, env=COMMIT_ENV)
    return git(cwd, 'rev-parse', 'HEAD')


def write(root, rel, data):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))


def remove_tree(path):
    """Borra un directorio temporal aunque Git haya dejado objetos de solo lectura."""
    def retry(func, p, exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    shutil.rmtree(path, onexc=retry)


def adr_text(adr_id='ADR-006', decided_on=CDATE, note=''):
    meta = {'metadata_schema': 'f36sbx-adr/v1', 'gate_id': 'F36-SBX-GATE', 'gate_version': v.GATE_VERSION,
            'base_commit': v.BASE, 'adr_id': adr_id, 'status': 'APROBADO',
            'relation_to_adr005': 'EXCEPCION_SANDBOX_SINTETICA_ADR005_6_4', 'scope': 'ALCANCE_C_SOLO_SINTETICO',
            'covered_ei': ['EI-08'], 'ei09_decision': 'SIN_DECISION', 'decided_on': decided_on}
    return (f'# {adr_id} · Excepción sintética de F36-SBX (prueba con Git real)\n\n## Contexto\n\n'
            'Documento sintético de prueba que se relaciona con ADR-005 y con F36-SBX solo para ejercitar la '
            'resolución del ADR en el árbol Git del commit candidato, dentro de un clon desechable.\n\n'
            '## Decisión\n\nLa decisión normativa consta únicamente en el bloque canónico de metadatos.\n\n'
            f'## Consecuencias\n\nNinguna fuera de la prueba: el clon se borra al terminar.{note}\n\n'
            '```f36sbx-adr-metadata\n' + json.dumps(meta, ensure_ascii=False, indent=2) + '\n```\n').encode('utf-8')


# ---------------------------------------------------------------- U: resolución de objetos en un repositorio mínimo

def unit(tmp):
    repo = tmp / 'minimo'
    repo.mkdir()
    git(repo, 'init', '-q', '-b', 'main')
    write(repo, 'docs/LEEME.md', '# Repositorio mínimo de prueba\n')
    git(repo, 'add', '.')
    c0 = commit(repo, 'base')
    regular = b'# ADR regular\n\nContenido versionado.\n'
    write(repo, 'docs/adr/ADR_006.md', regular)
    write(repo, 'docs/adr/EJECUTABLE.md', b'# Ejecutable\n')
    write(repo, 'docs/adr/CARPETA.md/nota.txt', b'nota\n')
    git(repo, 'add', '.')
    git(repo, 'update-index', '--chmod=+x', 'docs/adr/EJECUTABLE.md')
    link = git(repo, 'hash-object', '-w', '--stdin', stdin=b'ADR_006.md')
    git(repo, 'update-index', '--add', '--cacheinfo', f'120000,{link},docs/adr/ENLACE.md')
    git(repo, 'update-index', '--add', '--cacheinfo', f'160000,{c0},docs/adr/SUBMODULO.md')
    c1 = commit(repo, 'candidato')
    write(repo, 'docs/adr/SIN_VERSIONAR.md', b'# Sin versionar\n')
    write(repo, '.git/info/exclude', b'docs/adr/ignorado/\n')
    write(repo, 'docs/adr/ignorado/ADR.md', b'# Ignorado\n')
    write(repo, 'docs/adr/ADR_006.md', regular + b'Cambio solo en el arbol de trabajo.\n')

    def check(cid, desc, sha, rel, needle=None):
        b = v.git_blob(repo, sha, rel)
        if needle is None:
            good = 'error' not in b and b['data'] == regular and b['mode'] == '100644' and b['type'] == 'blob' \
                and b['object'] == git(repo, 'rev-parse', f'{c1}:{rel}') and v.blob_problem(b) is None
            ok(good, cid, desc, 'blob regular con los bytes del commit' if good else str(b)[:160])
        else:
            ok('error' in b and needle in b['error'] and v.blob_problem(b), cid, desc,
               b.get('error', 'sin error')[:160])

    check('U01', 'blob regular del commit candidato (control positivo; bytes de Git, no del árbol de trabajo)',
          c1, 'docs/adr/ADR_006.md')
    check('U02', 'archivo ejecutable (100755)', c1, 'docs/adr/EJECUTABLE.md', 'modo 100755')
    check('U03', 'enlace simbólico (120000)', c1, 'docs/adr/ENLACE.md', 'modo 120000')
    check('U04', 'submódulo (160000)', c1, 'docs/adr/SUBMODULO.md', 'tipo commit')
    check('U05', 'ruta que es un árbol', c1, 'docs/adr/CARPETA.md', 'tipo tree')
    check('U06', 'archivo sin versionar', c1, 'docs/adr/SIN_VERSIONAR.md', 'no existe en el árbol')
    check('U07', 'archivo ignorado', c1, 'docs/adr/ignorado/ADR.md', 'no existe en el árbol')
    ok(v.git_ignored(repo, ['docs/adr/ignorado/ADR.md', 'docs/adr/ADR_006.md']) == ['docs/adr/ignorado/ADR.md'],
       'U08', 'git_ignored identifica el archivo ignorado y no el versionado')
    check('U09', 'archivo versionado consultado en un commit anterior a su creación', c0, 'docs/adr/ADR_006.md',
          'no existe en el árbol')
    check('U10', 'ruta inexistente', c1, 'docs/adr/NO_EXISTE.md', 'no existe en el árbol')
    check('U11', 'comodín en la ruta (se trata literalmente)', c1, 'docs/adr/*.md', 'no existe en el árbol')
    check('U12', 'ruta con otras mayúsculas', c1, 'docs/ADR/ADR_006.md', 'no existe en el árbol')
    check('U13', 'objeto que no es un commit', link, 'docs/adr/ADR_006.md', 'no se pudo leer el árbol')
    check('U14', 'ruta que sale del árbol con ..', c1, 'docs/adr/../LEEME.md', 'fuera de formato')
    check('U15', 'commit fuera de formato', 'HEAD', 'docs/adr/ADR_006.md', 'fuera de formato')


# ---------------------------------------------------------------- G: validador completo en un clon compartido

def sync_package(clone):
    """El clon recibe el paquete y las herramientas del árbol de trabajo del repositorio original."""
    changed = False
    for rel_dir in (v.PKG, v.TOOLS):
        src, dst = v.ROOT / rel_dir, clone / rel_dir
        wanted = {p.relative_to(src).as_posix() for p in src.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts}
        present = {p.relative_to(dst).as_posix() for p in dst.rglob('*')
                   if p.is_file() and '__pycache__' not in p.parts} if dst.exists() else set()
        for rel in sorted(present - wanted):
            (dst / rel).unlink()
            changed = True
        for rel in sorted(wanted):
            data = (src / rel).read_bytes()
            if not (dst / rel).is_file() or (dst / rel).read_bytes() != data:
                write(dst, rel, data)
                changed = True
    if changed:
        git(clone, 'add', '-A', v.PKG, v.TOOLS)
        commit(clone, 'sincroniza el paquete F36-SBX del árbol de trabajo (clon de prueba)')


def e2e(tmp):
    clone = tmp / 'clon'
    git(tmp, 'clone', '-q', '--shared', '--branch', BRANCH, str(v.ROOT), str(clone))
    sync_package(clone)
    base_head = git(clone, 'rev-parse', 'HEAD')
    write(clone, ADR_PATH, adr_text())
    write(clone, f'{TREE_PATH}/nota.txt', 'nota\n')
    git(clone, 'add', ADR_PATH, TREE_PATH)
    cand = commit(clone, 'candidato sintético de prueba con ADR versionado')
    blob_sha = hashlib.sha256(adr_text()).hexdigest()
    state0 = git(clone, 'show', f'{cand}:{v.GATE_STATE}')
    doc0 = git(clone, 'show', f'{cand}:{v.GATE_DOC}')

    def register(candidate, adr_path, adr_sha):
        """Evidencia SINTÉTICA de FG-03 y FG-12 sin confirmar, como la registraría el equipo tras auditar."""
        common = {'schema': v.TEAM_SCHEMA_TAG, 'gate_id': 'F36-SBX-GATE', 'gate_version': v.GATE_VERSION,
                  'candidate_commit': candidate, 'recorded_at': CDATE}
        approvals = [{'member': m, 'vote': 'APRUEBA', 'date': CDATE} for m in v.MEMBERS]
        fg03 = {**common, 'criterion_id': 'FG-03', 'record_id': 'F36SBX-FG-03-001',
                'decision': 'AUTORIZA_INICIO_F37_SBX', 'authorized_ei': ['EI-07', 'EI-08'],
                'numbering_f36_m01': 'CONFIRMADA', 'approvals': approvals, 'quorum': '3/3'}
        fg12 = {**common, 'criterion_id': 'FG-12', 'record_id': 'F36SBX-FG-12-001',
                'successor_adr': {'id': 'ADR-006', 'path': adr_path, 'sha256': adr_sha, 'status': 'APROBADO',
                                  'relation_to_adr005': 'EXCEPCION_SANDBOX_SINTETICA_ADR005_6_4',
                                  'scope': 'ALCANCE_C_SOLO_SINTETICO'},
                'covered_ei': ['EI-08'], 'ei09_decision': 'SIN_DECISION', 'approvals': approvals, 'quorum': '3/3'}
        write(clone, f'{EV}FG-03.json', json.dumps(fg03, ensure_ascii=False, indent=2))
        write(clone, f'{EV}FG-12.json', json.dumps(fg12, ensure_ascii=False, indent=2))
        state = json.loads(state0)
        state['candidate_commit'] = candidate
        state['f37_authorized_ei'] = ['EI-07', 'EI-08']
        for c in state['criteria']:
            if c['id'] in ('FG-03', 'FG-12'):
                c['status'], c['evidence'] = 'CUMPLE', f'{EV}{c["id"]}.json'
        write(clone, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        lines = doc0.split('\n')
        for i, ln in enumerate(lines):
            if ln.startswith('| FG-03 |') or ln.startswith('| FG-12 |'):
                lines[i] = ln.rsplit('| PENDIENTE |', 1)[0] + '| CUMPLE |'
        write(clone, v.GATE_DOC, '\n'.join(lines) + '\n')

    def validate():
        v.clear_caches()
        res, gate = v.run(v.collect(clone))
        return [(n, m) for n, ok_, m in res if not ok_], gate

    def scenario(cid, desc, candidate, adr_path, adr_sha, needles=(), prepare=None, undo=None):
        try:
            if prepare:
                prepare()
            register(candidate, adr_path, adr_sha)
            fails, gate = validate()
        except Exception as e:  # noqa: BLE001 — un escenario que no se puede montar es una falla de la prueba
            ok(False, cid, desc, f'escenario no ejecutable: {e.__class__.__name__}: {e}')
            return
        finally:
            if undo:
                undo()
        if not needles:
            ok(not fails and gate == 'NO SUPERADO', cid, desc,
               f'validador sin fallas, gate {gate}' if not fails else f'fallas: {[f"{n}: {m[:140]}" for n, m in fails]}')
        else:
            missing = [x for x in needles if not any(n == 'GATE' and x in m for n, m in fails)]
            ok(not missing and gate == 'NO SUPERADO', cid, desc,
               f'validador FALLA en GATE con {list(needles)}' if not missing else
               f'faltan {missing}; fallas {[f"{n}: {m[:140]}" for n, m in fails][:3]}')

    no_blob = 'no es un blob regular versionado en el commit candidato'
    changed_after = 'el paquete cambió después del commit auditado'
    scenario('G01', 'control positivo realista: ADR versionado como blob regular del commit candidato',
             cand, ADR_PATH, blob_sha)
    ignored = adr_text(note=' Copia ignorada.')
    scenario('G02', 'ADR válido solo en el sistema de archivos, bajo un directorio ignorado (htmlcov/)',
             cand, IGNORED_ADR, hashlib.sha256(ignored).hexdigest(), (no_blob,),
             lambda: write(clone, IGNORED_ADR, ignored), lambda: (clone / IGNORED_ADR).unlink())
    untracked = adr_text(note=' Copia sin versionar.')
    scenario('G03', 'ADR sin versionar en el árbol de trabajo, ausente del commit candidato',
             cand, UNTRACKED_ADR, hashlib.sha256(untracked).hexdigest(), (no_blob, changed_after),
             lambda: write(clone, UNTRACKED_ADR, untracked), lambda: (clone / UNTRACKED_ADR).unlink())
    swapped = adr_text(note=' Sustituido en el árbol de trabajo.')
    scenario('G04', 'ADR versionado y sustituido en el árbol de trabajo, con el SHA-256 de la copia sustituida',
             cand, ADR_PATH, hashlib.sha256(swapped).hexdigest(),
             ('no es el del blob del ADR en el commit candidato', changed_after),
             lambda: write(clone, ADR_PATH, swapped), lambda: write(clone, ADR_PATH, adr_text()))
    scenario('G05', 'ADR sustituido en el árbol de trabajo, aunque el registro cite el SHA-256 del blob',
             cand, ADR_PATH, blob_sha, (changed_after,),
             lambda: write(clone, ADR_PATH, swapped), lambda: write(clone, ADR_PATH, adr_text()))
    scenario('G06', 'ruta del ADR que es un árbol en el commit candidato', cand, TREE_PATH, blob_sha,
             (no_blob, 'tipo tree'))
    scenario('G07', 'ruta inexistente en el commit candidato', cand, 'docs/academico/f36-sbx/ADR_009_no_existe.md',
             blob_sha, (no_blob,))
    scenario('G08', 'candidate_commit incorrecto: commit anterior, que no contiene el ADR', base_head, ADR_PATH,
             blob_sha, (no_blob,))
    exclude = clone / '.git' / 'info' / 'exclude'
    original_exclude = exclude.read_bytes() if exclude.exists() else b''
    scenario('G09', 'evidencia de equipo que Git ignora (exclusión local): ningún commit podría contenerla',
             cand, ADR_PATH, blob_sha, ('Git lo ignora',),
             lambda: write(clone, '.git/info/exclude', original_exclude + f'\n/{EV}FG-12.json\n'.encode('utf-8')),
             lambda: write(clone, '.git/info/exclude', original_exclude))
    write(clone, ADR_PATH, swapped)
    git(clone, 'add', ADR_PATH)
    commit(clone, 'ADR sustituido en un commit posterior al candidato')
    scenario('G10', 'ADR sustituido en un commit posterior, con el SHA-256 de la versión posterior',
             cand, ADR_PATH, hashlib.sha256(swapped).hexdigest(),
             ('no es el del blob del ADR en el commit candidato', changed_after))
    later = adr_text(adr_id='ADR-008')
    write(clone, LATER_ADR, later)
    git(clone, 'add', LATER_ADR)
    commit(clone, 'ADR añadido después del candidato')
    scenario('G11', 'ADR existente en HEAD y en el árbol de trabajo pero añadido después del commit candidato',
             cand, LATER_ADR, hashlib.sha256(later).hexdigest(), (no_blob, changed_after))


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    before = (v.git(v.ROOT, 'rev-parse', 'HEAD')[1], v.git(v.ROOT, 'status', '--porcelain', '--ignored')[1])
    tmp = Path(tempfile.mkdtemp(prefix='f36sbx-git-'))
    try:
        for part in (unit, e2e):
            try:
                part(tmp)
            except Exception as e:  # noqa: BLE001 — una parte que no se puede ejecutar es una falla, nunca un PASS
                ok(False, part.__name__.upper(), f'parte {part.__name__} no ejecutable', f'{e.__class__.__name__}: {e}')
    finally:
        remove_tree(tmp)
    after = (v.git(v.ROOT, 'rev-parse', 'HEAD')[1], v.git(v.ROOT, 'status', '--porcelain', '--ignored')[1])
    ok(before == after, 'R00', 'el repositorio original no cambió: mismo HEAD y mismo estado, también de ignorados')
    ok(not tmp.exists(), 'R01', 'el directorio temporal se borró')
    bad = [r for r in results if not r[0]]
    for ok_, cid, desc, detail in results:
        print(f'{"OK   " if ok_ else "FALLA"} {cid} {desc}: {detail}')
    print(f'test_f36sbx_git: {len(results) - len(bad)} casos correctos, {len(bad)} fallas')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
