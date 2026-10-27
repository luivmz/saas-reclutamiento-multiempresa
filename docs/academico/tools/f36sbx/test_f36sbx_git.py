#!/usr/bin/env python3
"""Pruebas con Git real del validador F36-SBX: AF3-M01, AF4-M01 y AF4-M02.

En memoria, test_f36sbx.py solo puede simular Git. Aquí se usa Git de verdad:

- U (AF3-M01): un repositorio mínimo, para la resolución de objetos (blob regular, ejecutable, enlace,
  submódulo, árbol, sin versionar, ignorado, otro commit, comodines, mayúsculas y bytes del árbol de trabajo);
- W (AF4-M01): otro repositorio mínimo, para la vista del índice y del árbol de trabajo: marcas assume-unchanged
  y skip-worktree, caché de stat engañada, fin de línea, conflictos, operaciones en curso, objetos ausentes,
  submódulos, bit de ejecución, entorno hostil, Git no ejecutable y ausencia de escrituras;
- RP (AF4-M02): otro repositorio mínimo, para los objetos reales frente a refs/replace, etiquetas e injertos;
- G (AF3-M01): un clon local compartido y desechable del repositorio, con el paquete del árbol de trabajo, un
  commit candidato con un ADR sintético y evidencia SINTÉTICA de FG-03 y FG-12 sin confirmar, sobre el que se
  ejecuta el validador completo: un control positivo y los ataques de AF3-M01;
- AF4-M01-* y AF4-M02-*: el validador completo sobre dos clones más, con las pruebas que exige la cuarta
  auditoría (numeradas como en ella) y ataques propios (sufijo A).

Todo ocurre en el directorio temporal del sistema y se borra al terminar. Nunca escribe en el repositorio original
(se comprueba antes y después, también su índice), no usa red y no registra evidencia real.

Uso: python -I -B docs/academico/tools/f36sbx/test_f36sbx_git.py
"""
import contextlib
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
OLD = 1577836800  # 2020-01-01: un stat antiguo, para que la caché de Git no lo considere «racy»
ADR_PATH = 'docs/academico/f36-sbx/ADR_006_prueba_git.md'
TREE_PATH = 'docs/academico/f36-sbx/adr_carpeta.md'
IGNORED_ADR = 'docs/academico/f36-sbx/htmlcov/ADR_006_ignorado.md'
UNTRACKED_ADR = 'docs/academico/f36-sbx/ADR_007_sin_versionar.md'
LATER_ADR = 'docs/academico/f36-sbx/ADR_008_posterior.md'
EV = v.GATE_EVIDENCE
NO_BLOB = 'no es un blob regular versionado en el commit candidato'
ABSENT = f'{NO_BLOB}: no existe en el árbol del commit'
CHANGED_AFTER = 'el paquete cambió después del commit auditado'
SHA_MISMATCH = 'no es el del blob del ADR en el commit candidato'
UNRELIABLE = ('GATE', 'estado Git no fiable')

results = []


def ok(cond, cid, desc, detail=''):
    results.append((bool(cond), cid, desc, detail))


def git(cwd, *args, stdin=None, env=None):
    r = subprocess.run(['git', *IDENTITY, *args], cwd=cwd, input=stdin, capture_output=True,
                       env={**os.environ, **(env or {})})
    if r.returncode:
        raise RuntimeError(f'git {" ".join(args)}: {r.stderr.decode("utf-8", "replace").strip()}')
    return r.stdout.decode('utf-8', 'replace').strip()


def git_code(cwd, *args):
    """Código de salida de Git consultado como lo haría cualquier persona, sin las opciones del validador."""
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True).returncode


def commit(cwd, msg):
    git(cwd, 'commit', '-q', '-m', msg, env=COMMIT_ENV)
    return git(cwd, 'rev-parse', 'HEAD')


def commit_tree(cwd, tree, parents=(), date=CDATE, msg='objeto sintético de prueba'):
    """Commit sin rama (para sustitutos, huérfanos e injertos), con fecha fija."""
    stamp = f'{date}T12:00:00+0000'
    return git(cwd, 'commit-tree', tree, *[x for p in parents for x in ('-p', p)], '-m', msg,
               env={'GIT_AUTHOR_DATE': stamp, 'GIT_COMMITTER_DATE': stamp})


def clear_replace(cwd):
    for ref in git(cwd, 'for-each-ref', '--format=%(refname)', 'refs/replace/').split():
        git(cwd, 'update-ref', '-d', ref)


def write(root, rel, data):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))


@contextlib.contextmanager
def environ(**values):
    """Variables de entorno del proceso solo durante el bloque (para el validador; no se llama a git() dentro)."""
    saved = dict(os.environ)
    os.environ.update(values)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


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

    # Ramas defensivas que Git real no produce con rutas válidas: se simula su salida y debe fallar cerrado.
    real = v.git_bytes
    obj = git(repo, 'rev-parse', f'{c1}:docs/adr/ADR_006.md').encode('ascii')

    def simulated(cid, desc, fake, needle):
        v.git_bytes = fake
        try:
            b = v.git_blob(repo, c1, 'docs/adr/ADR_006.md')
        finally:
            v.git_bytes = real
        ok('error' in b and needle in b['error'], cid, desc, b.get('error', f'sin error: {str(b)[:120]}'))
    entry = b'100644 blob ' + obj + b'\t'
    simulated('U16', 'git devuelve dos entradas para la ruta (simulado)',
              lambda root, *a, **k: entry + b'docs/adr/ADR_006.md\0' + entry + b'docs/adr/OTRO.md\0' if 'ls-tree' in a
              else real(root, *a, **k), 'no identifica exactamente una entrada')
    simulated('U17', 'git devuelve una entrada con otra ruta (simulado)',
              lambda root, *a, **k: entry + b'docs/adr/OTRO.md\0' if 'ls-tree' in a else real(root, *a, **k),
              'no identifica exactamente una entrada')
    simulated('U18', 'git no puede leer el blob después de resolverlo (simulado)',
              lambda root, *a, **k: None if 'cat-file' in a else real(root, *a, **k), 'no se pudo leer el blob')


# ---------------------------------------------------------------- W: índice y árbol de trabajo sin marcas ni caché

def worktree(tmp):
    repo = tmp / 'estado'
    repo.mkdir()
    git(repo, 'init', '-q', '-b', 'main')
    files = {'docs/a.md': b'# A\n\nUna linea.\nOtra linea.\n', 'app/b.php': b'<?php\n// b sintetico\n',
             'docs/c.md': b'# C sintetico\n', 'tools/run.sh': b'#!/bin/sh\necho ok\n'}
    for rel, data in files.items():
        write(repo, rel, data)
    git(repo, 'add', '.')
    git(repo, 'update-index', '--chmod=+x', 'tools/run.sh')
    os.chmod(repo / 'tools/run.sh', 0o755)
    link = git(repo, 'hash-object', '-w', '--stdin', stdin=b'a.md')
    git(repo, 'update-index', '--add', '--cacheinfo', f'120000,{link},docs/enlace.md')
    c1 = commit(repo, 'base')
    git(repo, 'checkout', '--', 'docs/enlace.md')
    idx = repo / '.git' / 'index'

    def view():
        st = v.worktree_state(repo)
        return st, v.git_state_problems(repo) + st['problems']

    def hidden(rel):
        """¿git status, como lo usaría cualquier persona, no muestra el cambio de rel?"""
        return git(repo, 'status', '--porcelain', '--', rel) == ''

    def has(problems, needle):
        return any(needle in p for p in problems)

    st, problems = view()
    ok(not problems and st['dirty'] == set() and st['untracked'] == set() and len(st['index'] or {}) == 5, 'W01',
       'control positivo: checkout normal sin marcas ni cambios (con un ejecutable y un enlace simbólico)',
       f'problemas {problems}, cambiados {sorted(st["dirty"] or [])}, índice {len(st["index"] or {})}')

    git(repo, 'update-index', '--assume-unchanged', 'docs/a.md')
    st, problems = view()
    ok(has(problems, 'assume-unchanged') and not st['dirty'], 'W02',
       'marca assume-unchanged sin cambios: la marca sola hace la vista no fiable', str(problems))
    write(repo, 'docs/a.md', files['docs/a.md'] + b'Cambio oculto.\n')
    plain = hidden('docs/a.md')
    st, problems = view()
    ok(has(problems, 'assume-unchanged') and 'docs/a.md' in st['dirty']
       and 'docs/a.md' in (v.changed_since(repo, c1, st) or []), 'W03',
       'cambio bajo assume-unchanged: el validador lo ve por sus bytes', f'git status lo oculta: {plain}')
    git(repo, 'update-index', '--no-assume-unchanged', 'docs/a.md')
    write(repo, 'docs/a.md', files['docs/a.md'])

    git(repo, 'update-index', '--skip-worktree', 'app/b.php')
    write(repo, 'app/b.php', files['app/b.php'] + b'// cambio oculto\n')
    plain = hidden('app/b.php')
    st, problems = view()
    ok(has(problems, 'skip-worktree') and 'app/b.php' in st['dirty'], 'W04',
       'cambio bajo skip-worktree: el validador lo ve por sus bytes', f'git status lo oculta: {plain}')
    (repo / 'app/b.php').unlink()
    plain = hidden('app/b.php')
    st, problems = view()
    ok(has(problems, 'skip-worktree') and 'app/b.php' in st['dirty'], 'W05',
       'archivo marcado skip-worktree y borrado del árbol de trabajo', f'git status lo oculta: {plain}')
    git(repo, 'update-index', '--no-skip-worktree', 'app/b.php')
    write(repo, 'app/b.php', files['app/b.php'])

    p = repo / 'docs/c.md'
    os.utime(p, (OLD, OLD))
    git(repo, 'update-index', '-q', '--refresh')
    p.write_bytes(files['docs/c.md'].replace(b'C', b'D'))
    os.utime(p, (OLD, OLD))
    plain = hidden('docs/c.md')
    st, problems = view()
    ok('docs/c.md' in st['dirty'] and not problems, 'W06',
       'cambio del mismo tamaño con la fecha restaurada, sin marcas (caché de stat engañada)',
       f'git status lo oculta: {plain}')
    p.write_bytes(files['docs/c.md'])

    eol = [('W07', 'control positivo: conversión LF→CRLF completa de un checkout', files['docs/a.md'].replace(b'\n', b'\r\n'),
            False),
           ('W08', 'un solo fin de línea CRLF: solo se tolera la conversión completa',
            files['docs/a.md'].replace(b'\n', b'\r\n', 1), True),
           ('W09', 'fines de línea CR sueltos', files['docs/a.md'].replace(b'\n', b'\r'), True)]
    for cid, desc, data, dirty in eol:
        write(repo, 'docs/a.md', data)
        st, problems = view()
        ok(('docs/a.md' in st['dirty']) == dirty and not problems, cid, desc, sorted(st['dirty']))
    write(repo, 'docs/a.md', files['docs/a.md'])

    saved = idx.read_bytes()
    oid = git(repo, 'rev-parse', ':docs/c.md')
    info = f'0 {"0" * 40}\tdocs/c.md\n' + ''.join(f'100644 {oid} {n}\tdocs/c.md\n' for n in (1, 2, 3))
    git(repo, 'update-index', '--index-info', stdin=info.encode('utf-8'))
    _, problems = view()
    ok(has(problems, 'sin fusionar'), 'W10', 'estado no resoluble: entradas del índice sin fusionar (conflicto)',
       str(problems))
    idx.write_bytes(saved)
    for cid, name, make in (('W11', 'MERGE_HEAD', lambda q: q.write_text(c1 + '\n')),
                            ('W12', 'rebase-merge', lambda q: q.mkdir())):
        q = repo / '.git' / name
        make(q)
        _, problems = view()
        ok(has(problems, name), cid, f'estado ambiguo: operación de Git en curso ({name})', str(problems))
        q.rmdir() if q.is_dir() else q.unlink()
    git(repo, 'update-index', '--add', '--cacheinfo', f'100644,{"1" * 40},docs/fantasma.md')
    _, problems = view()
    ok(has(problems, 'sin su objeto blob'), 'W13', 'entrada del índice cuyo objeto no existe en el repositorio',
       str(problems))
    idx.write_bytes(saved)
    git(repo, 'update-index', '--add', '--cacheinfo', f'160000,{c1},docs/sub')
    _, problems = view()
    ok(has(problems, 'submódulo'), 'W14', 'entrada de submódulo, que el validador no puede comparar', str(problems))
    idx.write_bytes(saved)

    real_mode = v.git_filemode
    os.chmod(repo / 'tools/run.sh', 0o644)
    try:
        v.git_filemode = lambda root: True
        on = v.worktree_state(repo)['dirty']
        v.git_filemode = lambda root: False
        off = v.worktree_state(repo)['dirty']
    finally:
        v.git_filemode = real_mode
        os.chmod(repo / 'tools/run.sh', 0o755)
    ok('tools/run.sh' in on and 'tools/run.sh' not in off, 'W15',
       'bit de ejecución distinto del índice: es un cambio solo si Git lo compara (core.fileMode, fuera de Windows)',
       f'con core.fileMode {sorted(on)}, sin él {sorted(off)}')

    with environ(GIT_DIR=str(tmp / 'minimo' / '.git'), GIT_WORK_TREE=str(tmp / 'minimo'),
                 GIT_INDEX_FILE=str(tmp / 'no-existe'), GIT_OBJECT_DIRECTORY=str(tmp / 'no-existe'),
                 GIT_NO_REPLACE_OBJECTS=''):
        head = v.git(repo, 'rev-parse', 'HEAD')[1].strip()
        st, problems = view()
    ok(head == c1 and not problems and st['dirty'] == set(), 'W16',
       'entorno hostil (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE y GIT_OBJECT_DIRECTORY de otro sitio): se ignora',
       f'HEAD {head[:12]}, problemas {problems}')

    real_run = v.subprocess.run

    def boom(*a, **k):
        raise OSError('git no disponible (simulado)')
    v.subprocess.run = boom
    try:
        st = v.worktree_state(repo)
        problems = v.git_state_problems(repo)
        out = (v.git_commit(repo, c1), v.changed_since(repo, c1, st), v.git_ignored(repo, ['docs/a.md']),
               v.git(repo, 'rev-parse', 'HEAD')[0])
    finally:
        v.subprocess.run = real_run
    ok(st['index'] is None and problems and out == (None, None, None, -1), 'W17',
       'Git no ejecutable (simulado): nada queda evaluado y todo falla cerrado', f'{problems[:1]} {out}')

    os.utime(repo / 'docs/a.md', None)
    before = idx.read_bytes()
    st, _ = view()
    v.changed_since(repo, c1, st)
    v.git_ignored(repo, ['docs/a.md'])
    ok(idx.read_bytes() == before, 'W18', 'el validador no escribe el índice, ni para refrescar un stat desactualizado')

    real_read = Path.read_bytes

    def denied(self):
        if self.name == 'c.md':
            raise PermissionError('lectura denegada (simulado)')
        return real_read(self)
    Path.read_bytes = denied
    try:
        st, problems = view()
    finally:
        Path.read_bytes = real_read
    ok(has(problems, 'ilegibles'), 'W19', 'archivo versionado que no se puede leer (simulado): la vista no es fiable',
       str(problems))


# ---------------------------------------------------------------- RP: objetos reales frente a refs/replace e injertos

def replacement(tmp):
    repo = tmp / 'reemplazos'
    repo.mkdir()
    git(repo, 'init', '-q', '-b', 'main')
    write(repo, 'docs/a.md', b'# A real\n')
    git(repo, 'add', '.')
    c0 = commit(repo, 'base')
    write(repo, 'docs/b.md', b'# B real\n')
    git(repo, 'add', '.')
    c1 = commit(repo, 'hijo')
    real_tree = git(repo, 'rev-parse', f'{c1}^{{tree}}')
    real_a = git(repo, 'rev-parse', f'{c1}:docs/a.md')
    fake_blob = git(repo, 'hash-object', '-w', '--stdin', stdin=b'# A falso\n')
    idx_env = {'GIT_INDEX_FILE': str(tmp / 'indice-reemplazos')}
    git(repo, 'read-tree', c1, env=idx_env)
    git(repo, 'update-index', '--add', '--cacheinfo', f'100644,{fake_blob},docs/a.md', env=idx_env)
    fake_tree = git(repo, 'write-tree', env=idx_env)
    orphan = commit_tree(repo, fake_tree, (), '2026-10-20', 'huérfano')
    fake = commit_tree(repo, fake_tree, (orphan,), '2030-01-01', 'sustituto')

    git(repo, 'replace', c1, fake)
    plain = (git(repo, 'show', '-s', '--format=%cs', c1), git(repo, 'show', f'{c1}:docs/a.md'),
             git_code(repo, 'merge-base', '--is-ancestor', c0, c1), git_code(repo, 'merge-base', '--is-ancestor', orphan, c1))
    info = v.git_commit(repo, c1)
    blob = v.git_blob(repo, c1, 'docs/a.md')
    tree = v.git_tree(repo, c1) or {}
    real = (info, blob.get('data'), tree.get('docs/a.md'), v.git_run(repo, 'merge-base', '--is-ancestor', c0, c1)[0],
            v.git_run(repo, 'merge-base', '--is-ancestor', orphan, c1)[0])
    ok(plain == ('2030-01-01', '# A falso', 1, 0)
       and real == ({'tree': real_tree, 'parents': [c0], 'date': CDATE}, b'# A real\n', ('100644', real_a), 0, 1),
       'RP01', 'commit sustituido por refs/replace: fecha, padres, árbol, blob y ancestros son los del objeto real',
       f'Git sin opciones ve {plain}; el validador ve fecha {info and info["date"]} y ancestros {real[3:]}')
    problems = v.git_state_problems(repo)
    ok(any('refs/replace' in p for p in problems), 'RP02', 'la presencia de refs/replace hace la vista ambigua',
       str(problems))
    git(repo, 'replace', '-d', c1)

    git(repo, 'replace', real_a, fake_blob)
    plain = git(repo, 'show', f'{c1}:docs/a.md')
    blob = v.git_blob(repo, c1, 'docs/a.md')
    ok(plain == '# A falso' and blob.get('data') == b'# A real\n' and v.blob_problem(blob) is None, 'RP03',
       'blob sustituido por refs/replace: el validador lee los bytes del blob real', f'Git sin opciones ve {plain!r}')
    git(repo, 'replace', '-d', real_a)

    ghost = '2' * 40
    git(repo, 'update-ref', f'refs/replace/{ghost}', c1)
    plain = git_code(repo, 'cat-file', '-t', ghost)
    ok(plain == 0 and v.git_commit(repo, ghost) is None and v.git_run(repo, 'cat-file', '-e', ghost)[0] != 0, 'RP04',
       'SHA inexistente con una ref de reemplazo a su nombre: no es un commit real (falla cerrado)',
       f'git cat-file -t sin opciones: {plain}')
    clear_replace(repo)

    git(repo, 'tag', '-a', '-m', 'etiqueta sintética', 'etiqueta', c0)
    tag = git(repo, 'rev-parse', 'etiqueta')
    ok(git_code(repo, 'cat-file', 'commit', tag) == 0 and v.git_commit(repo, tag) is None
       and v.git_commit(repo, real_tree) is None and v.git_commit(repo, real_a) is None and v.git_commit(repo, c0),
       'RP05', 'solo un commit cuyo SHA-1 es el de sus bytes: una etiqueta (que Git desreferencia), un árbol o un '
       'blob no lo son')

    dates = {}
    for stamp in ('2026-10-26T23:30:00-0500', '2026-10-27T01:30:00+0900', '2026-10-27T12:00:00+0000'):
        sha = git(repo, 'commit-tree', real_tree, '-m', 'fecha', env={'GIT_AUTHOR_DATE': stamp, 'GIT_COMMITTER_DATE': stamp})
        dates[stamp] = ((v.git_commit(repo, sha) or {}).get('date'), git(repo, 'show', '-s', '--format=%cs', sha))
    ok(all(a == b for a, b in dates.values()), 'RP06',
       'la fecha del candidato es la de «git show --format=%cs», en la zona horaria del committer', str(dates))

    write(repo, '.git/info/grafts', f'{c0} {orphan}\n')
    plain = (git_code(repo, 'merge-base', '--is-ancestor', orphan, c0),
             git_code(repo, '--no-replace-objects', 'merge-base', '--is-ancestor', orphan, c0))
    problems = v.git_state_problems(repo)
    ok(plain == (0, 0) and any('injertos' in p for p in problems), 'RP07',
       'injertos (info/grafts): Git los aplica también sin reemplazos, así que su presencia falla cerrado',
       f'merge-base con y sin reemplazos: {plain}')
    (repo / '.git' / 'info' / 'grafts').unlink()


# ---------------------------------------------------------------- validador completo en clones compartidos

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


class Sandbox:
    """Clon local compartido y desechable con un commit candidato que versiona un ADR sintético."""

    def __init__(self, tmp, name, tree_path=False):
        self.clone = tmp / name
        git(tmp, 'clone', '-q', '--shared', '--branch', BRANCH, str(v.ROOT), str(self.clone))
        sync_package(self.clone)
        self.base_head = git(self.clone, 'rev-parse', 'HEAD')
        write(self.clone, ADR_PATH, adr_text())
        paths = [ADR_PATH]
        if tree_path:
            write(self.clone, f'{TREE_PATH}/nota.txt', 'nota\n')
            paths.append(TREE_PATH)
        git(self.clone, 'add', *paths)
        self.cand = commit(self.clone, 'candidato sintético de prueba con ADR versionado')
        self.blob_sha = hashlib.sha256(adr_text()).hexdigest()
        self.state0 = git(self.clone, 'show', f'{self.cand}:{v.GATE_STATE}')
        self.doc0 = git(self.clone, 'show', f'{self.cand}:{v.GATE_DOC}')

    def register(self, candidate, adr_path, adr_sha):
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
        write(self.clone, f'{EV}FG-03.json', json.dumps(fg03, ensure_ascii=False, indent=2))
        write(self.clone, f'{EV}FG-12.json', json.dumps(fg12, ensure_ascii=False, indent=2))
        state = json.loads(self.state0)
        state['candidate_commit'] = candidate
        state['f37_authorized_ei'] = ['EI-07', 'EI-08']
        for c in state['criteria']:
            if c['id'] in ('FG-03', 'FG-12'):
                c['status'], c['evidence'] = 'CUMPLE', f'{EV}{c["id"]}.json'
        write(self.clone, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
        lines = self.doc0.split('\n')
        for i, ln in enumerate(lines):
            if ln.startswith('| FG-03 |') or ln.startswith('| FG-12 |'):
                lines[i] = ln.rsplit('| PENDIENTE |', 1)[0] + '| CUMPLE |'
        write(self.clone, v.GATE_DOC, '\n'.join(lines) + '\n')

    def validate(self):
        v.clear_caches()
        res, gate = v.run(v.collect(self.clone))
        return [(n, m) for n, ok_, m in res if not ok_], gate

    def scenario(self, cid, desc, needles=(), prepare=None, undo=None, candidate=None, adr_path=ADR_PATH,
                 adr_sha=None, note=None):
        """Registra la evidencia sobre el clon preparado y ejecuta el validador completo. Sin agujas, control
        positivo (sin fallas); con ellas, cada aguja tiene que aparecer en una falla de su regla: un texto es de
        GATE y una tupla (regla, texto), de esa regla."""
        try:
            if prepare:
                prepare()
            self.register(candidate or self.cand, adr_path, adr_sha or self.blob_sha)
            fails, gate = self.validate()
        except Exception as e:  # noqa: BLE001 — un escenario que no se puede montar es una falla de la prueba
            ok(False, cid, desc, f'escenario no ejecutable: {e.__class__.__name__}: {e}')
            return
        finally:
            if undo:
                undo()
        extra = f' · {note()}' if note else ''
        if not needles:
            ok(not fails and gate == 'NO SUPERADO', cid, desc,
               (f'validador sin fallas, gate {gate}' if not fails else
                f'fallas: {[f"{n}: {m[:140]}" for n, m in fails]}') + extra)
            return
        wanted = [('GATE', x) if isinstance(x, str) else x for x in needles]
        missing = [x for x in wanted if not any(n == x[0] and x[1] in m for n, m in fails)]
        ok(not missing and gate == 'NO SUPERADO', cid, desc,
           (f'validador FALLA con {wanted}' if not missing else
            f'faltan {missing}; fallas {[f"{n}: {m[:140]}" for n, m in fails][:4]}') + extra)


def e2e(tmp):
    """AF3-M01: el ADR es el blob de candidate_commit:path."""
    sb = Sandbox(tmp, 'clon', tree_path=True)
    clone = sb.clone
    sb.scenario('G01', 'control positivo realista: ADR versionado como blob regular del commit candidato')
    ignored = adr_text(note=' Copia ignorada.')
    sb.scenario('G02', 'ADR válido solo en el sistema de archivos, bajo un directorio ignorado (htmlcov/)', (ABSENT,),
                lambda: write(clone, IGNORED_ADR, ignored), lambda: (clone / IGNORED_ADR).unlink(),
                adr_path=IGNORED_ADR, adr_sha=hashlib.sha256(ignored).hexdigest())
    untracked = adr_text(note=' Copia sin versionar.')
    sb.scenario('G03', 'ADR sin versionar en el árbol de trabajo, ausente del commit candidato', (ABSENT, CHANGED_AFTER),
                lambda: write(clone, UNTRACKED_ADR, untracked), lambda: (clone / UNTRACKED_ADR).unlink(),
                adr_path=UNTRACKED_ADR, adr_sha=hashlib.sha256(untracked).hexdigest())
    swapped = adr_text(note=' Sustituido en el árbol de trabajo.')
    sb.scenario('G04', 'ADR versionado y sustituido en el árbol de trabajo, con el SHA-256 de la copia sustituida',
                (SHA_MISMATCH, CHANGED_AFTER), lambda: write(clone, ADR_PATH, swapped),
                lambda: write(clone, ADR_PATH, adr_text()), adr_sha=hashlib.sha256(swapped).hexdigest())
    sb.scenario('G05', 'ADR sustituido en el árbol de trabajo, aunque el registro cite el SHA-256 del blob',
                (CHANGED_AFTER,), lambda: write(clone, ADR_PATH, swapped), lambda: write(clone, ADR_PATH, adr_text()))
    sb.scenario('G06', 'ruta del ADR que es un árbol en el commit candidato', (NO_BLOB, 'tipo tree'), adr_path=TREE_PATH)
    sb.scenario('G07', 'ruta inexistente en el commit candidato', (ABSENT,),
                adr_path='docs/academico/f36-sbx/ADR_009_no_existe.md')
    sb.scenario('G08', 'candidate_commit incorrecto: commit anterior, que no contiene el ADR', (ABSENT,),
                candidate=sb.base_head)
    exclude = clone / '.git' / 'info' / 'exclude'
    original_exclude = exclude.read_bytes() if exclude.exists() else b''
    sb.scenario('G09', 'evidencia de equipo que Git ignora (exclusión local): ningún commit podría contenerla',
                ('Git lo ignora',),
                lambda: write(clone, '.git/info/exclude', original_exclude + f'\n/{EV}FG-12.json\n'.encode('utf-8')),
                lambda: write(clone, '.git/info/exclude', original_exclude))
    write(clone, ADR_PATH, swapped)
    git(clone, 'add', ADR_PATH)
    commit(clone, 'ADR sustituido en un commit posterior al candidato')
    sb.scenario('G10', 'ADR sustituido en un commit posterior, con el SHA-256 de la versión posterior',
                (SHA_MISMATCH, CHANGED_AFTER), adr_sha=hashlib.sha256(swapped).hexdigest())
    later = adr_text(adr_id='ADR-008')
    write(clone, LATER_ADR, later)
    git(clone, 'add', LATER_ADR)
    commit(clone, 'ADR añadido después del candidato')
    sb.scenario('G11', 'ADR existente en HEAD y en el árbol de trabajo pero añadido después del commit candidato',
                (ABSENT, CHANGED_AFTER), adr_path=LATER_ADR, adr_sha=hashlib.sha256(later).hexdigest())


def e2e_m01(tmp):
    """AF4-M01: las marcas del índice y la caché de stat no pueden ocultar cambios del ADR, de la evidencia, del
    paquete ni de las superficies protegidas."""
    sb = Sandbox(tmp, 'clon-m01')
    clone = sb.clone
    idx = clone / '.git' / 'index'
    orig = adr_text()
    other = adr_text(note=' Modificado después del candidato.')
    web = (clone / 'routes/web.php').read_bytes()
    composer = (clone / 'composer.json').read_bytes()
    matrix = (clone / v.MATRIX).read_bytes()
    saved = {}

    def marked(rel, kind, data=None):
        def f():
            git(clone, 'update-index', f'--{kind}', rel)
            if data is not None:
                write(clone, rel, data)
        return f

    def unmarked(rel, kind, data):
        def f():
            git(clone, 'update-index', f'--no-{kind}', rel)
            write(clone, rel, data)
        return f

    def save_index():
        saved['index'] = idx.read_bytes()

    def restore_index():
        idx.write_bytes(saved['index'])

    sb.scenario('AF4-M01-1', 'ADR versionado en el candidato, checkout normal: control positivo')
    sb.scenario('AF4-M01-2', 'ADR modificado normalmente en el árbol de trabajo', (CHANGED_AFTER,),
                lambda: write(clone, ADR_PATH, other), lambda: write(clone, ADR_PATH, orig))
    for cid, kind in (('AF4-M01-3', 'assume-unchanged'), ('AF4-M01-4', 'skip-worktree')):
        sb.scenario(cid, f'reproducción de la cuarta auditoría: ADR modificado y marcado {kind} (git status no lo '
                    'muestra)', (('FRZ', kind), UNRELIABLE, CHANGED_AFTER),
                    marked(ADR_PATH, kind, other), unmarked(ADR_PATH, kind, orig))
    sb.scenario('AF4-M01-5', 'reproducción de la cuarta auditoría: superficie productiva (routes/web.php) modificada '
                'y marcada assume-unchanged', (('FRZ', 'routes/web.php'), ('FRZ', 'assume-unchanged')),
                marked('routes/web.php', 'assume-unchanged', web + b'\n// cambio productivo oculto\n'),
                unmarked('routes/web.php', 'assume-unchanged', web))
    sb.scenario('AF4-M01-6', 'dependencias (composer.json) modificadas y marcadas skip-worktree',
                (('FRZ', 'composer.json'), ('FRZ', 'skip-worktree')),
                marked('composer.json', 'skip-worktree', composer.replace(b'{', b'{\n    "x-oculto": true,', 1)),
                unmarked('composer.json', 'skip-worktree', composer))

    def conflict():
        save_index()
        oid = git(clone, 'rev-parse', f':{v.PLAN}')
        info = f'0 {"0" * 40}\t{v.PLAN}\n' + ''.join(f'100644 {oid} {n}\t{v.PLAN}\n' for n in (1, 2, 3))
        git(clone, 'update-index', '--index-info', stdin=info.encode('utf-8'))
    sb.scenario('AF4-M01-7', 'estado no resoluble: entradas del índice sin fusionar (conflicto)',
                (('FRZ', 'sin fusionar'), UNRELIABLE), conflict, restore_index)

    sb.scenario('AF4-M01-A1', 'estado ambiguo: fusión en curso (MERGE_HEAD)', (('FRZ', 'MERGE_HEAD'), UNRELIABLE),
                lambda: write(clone, '.git/MERGE_HEAD', sb.base_head + '\n'),
                lambda: (clone / '.git' / 'MERGE_HEAD').unlink())

    def corrupt():
        save_index()
        idx.write_bytes(b'DIRC' + b'\0' * 24)
    sb.scenario('AF4-M01-A2', 'estado no resoluble: índice de Git ilegible',
                (('FRZ', 'no se pudo leer el índice'), UNRELIABLE), corrupt, restore_index)
    sb.scenario('AF4-M01-A3', 'ADR intacto pero marcado assume-unchanged: la marca sola ya hace la vista no fiable',
                (('FRZ', 'assume-unchanged'), UNRELIABLE), marked(ADR_PATH, 'assume-unchanged'),
                unmarked(ADR_PATH, 'assume-unchanged', orig))
    sb.scenario('AF4-M01-A4', 'documento del paquete (matriz) modificado después del candidato y marcado skip-worktree',
                (('FRZ', 'skip-worktree'), CHANGED_AFTER),
                marked(v.MATRIX, 'skip-worktree', matrix + b'\nCambio oculto.\n'),
                unmarked(v.MATRIX, 'skip-worktree', matrix))

    def stale_stat():
        p = clone / 'routes/web.php'
        os.utime(p, (OLD, OLD))
        git(clone, 'update-index', '-q', '--refresh')
        p.write_bytes(web[:-1] + (b'#' if web[-1:] != b'#' else b'%'))
        os.utime(p, (OLD, OLD))
        saved['hidden'] = git(clone, 'status', '--porcelain', '--', 'routes/web.php') == ''
    sb.scenario('AF4-M01-A5', 'superficie productiva cambiada con el mismo tamaño y la fecha restaurada, sin marcas',
                (('FRZ', 'routes/web.php'),), stale_stat, lambda: write(clone, 'routes/web.php', web),
                note=lambda: f'git status lo oculta: {saved.get("hidden")}')

    def deleted():
        git(clone, 'update-index', '--skip-worktree', 'routes/web.php')
        (clone / 'routes/web.php').unlink()
        saved['hidden'] = git(clone, 'status', '--porcelain', '--', 'routes/web.php') == ''
    sb.scenario('AF4-M01-A6', 'superficie productiva marcada skip-worktree y borrada del árbol de trabajo',
                (('FRZ', 'routes/web.php'), ('FRZ', 'skip-worktree')), deleted,
                unmarked('routes/web.php', 'skip-worktree', web), note=lambda: f'git status lo oculta: {saved.get("hidden")}')

    def filtered():
        # El filtro devuelve siempre el blob de HEAD; con un cambio del mismo tamaño, Git solo compara a través de él.
        write(clone, '.git/info/attributes', 'routes/web.php filter=oculta\n')
        git(clone, 'config', 'filter.oculta.clean', 'cat >/dev/null; git show HEAD:routes/web.php')
        write(clone, 'routes/web.php', web[:-1] + (b'#' if web[-1:] != b'#' else b'%'))
        saved['hidden'] = git(clone, 'status', '--porcelain', '--', 'routes/web.php') == ''

    def unfiltered():
        (clone / '.git' / 'info' / 'attributes').unlink()
        git(clone, 'config', '--unset', 'filter.oculta.clean')
        write(clone, 'routes/web.php', web)
    sb.scenario('AF4-M01-A7', 'filtro clean local (.git/info/attributes) que oculta a Git un cambio productivo',
                (('FRZ', 'routes/web.php'),), filtered, unfiltered,
                note=lambda: f'git status lo oculta: {saved.get("hidden")}')

    def round_trip():
        for kind in ('assume-unchanged', 'skip-worktree'):
            git(clone, 'update-index', f'--{kind}', ADR_PATH)
            git(clone, 'update-index', f'--no-{kind}', ADR_PATH)
    sb.scenario('AF4-M01-A8', 'control positivo: marcas puestas y retiradas, con el contenido intacto', (), round_trip)
    sb.scenario('AF4-M01-A9', 'control positivo: ADR con la conversión LF→CRLF completa de un checkout', (),
                lambda: write(clone, ADR_PATH, orig.replace(b'\n', b'\r\n')), lambda: write(clone, ADR_PATH, orig))
    sb.scenario('AF4-M01-A10', 'ADR con un solo fin de línea CRLF: solo se tolera la conversión completa',
                (CHANGED_AFTER,), lambda: write(clone, ADR_PATH, orig.replace(b'\n', b'\r\n', 1)),
                lambda: write(clone, ADR_PATH, orig))
    exclude = clone / '.git' / 'info' / 'exclude'
    exclude0 = exclude.read_bytes() if exclude.exists() else b''

    def unversioned():
        git(clone, 'rm', '-q', '--cached', v.MATRIX)
        write(clone, '.git/info/exclude', exclude0 + f'\n/{v.MATRIX}\n'.encode('utf-8'))

    def versioned():
        write(clone, '.git/info/exclude', exclude0)
        git(clone, 'add', v.MATRIX)
    sb.scenario('AF4-M01-A11', 'documento del paquete sacado del índice e ignorado localmente: el validador lo leería '
                'sin que ningún commit lo contenga', (('FRZ', 'versionables'), CHANGED_AFTER), unversioned, versioned)

    def committed_evidence():
        git(clone, 'add', EV, v.GATE_STATE, v.GATE_DOC)
        commit(clone, 'evidencia sintética registrada (clon de prueba)')
        git(clone, 'update-index', '--assume-unchanged', f'{EV}FG-03.json')
        write(clone, f'{EV}FG-03.json', (clone / f'{EV}FG-03.json').read_bytes() + b'\n')
        saved['hidden'] = git(clone, 'status', '--porcelain', '--', EV) == ''
    try:
        sb.register(sb.cand, ADR_PATH, sb.blob_sha)
        committed_evidence()
        fails, gate = sb.validate()
        git(clone, 'update-index', '--no-assume-unchanged', f'{EV}FG-03.json')
        hit = [m for n, m in fails if n == 'FRZ' and 'assume-unchanged' in m]
        ok(hit and gate == 'NO SUPERADO', 'AF4-M01-A12', 'evidencia ya registrada en un commit y cambiada bajo '
           'assume-unchanged: lo validado no sería lo versionado', f'git status lo oculta: {saved.get("hidden")}')
    except Exception as e:  # noqa: BLE001
        ok(False, 'AF4-M01-A12', 'evidencia registrada y cambiada bajo assume-unchanged',
           f'escenario no ejecutable: {e.__class__.__name__}: {e}')

    os.utime(clone / ADR_PATH, None)
    before = idx.read_bytes()
    sb.validate()
    ok(idx.read_bytes() == before, 'AF4-M01-A13', 'el validador completo no escribe el índice del clon, aunque haya '
       'entradas con el stat desactualizado')


def e2e_m02(tmp):
    """AF4-M02: refs/replace (e injertos) no pueden dar contenido, ancestros ni fechas a un commit candidato."""
    sb = Sandbox(tmp, 'clon-m02')
    clone, cand, pre = sb.clone, sb.cand, sb.base_head
    v2 = adr_text(note=' Versión sustituta, solo visible a través de refs/replace.')
    cand_tree = git(clone, 'rev-parse', f'{cand}^{{tree}}')
    pre_tree = git(clone, 'rev-parse', f'{pre}^{{tree}}')
    pre_parent = git(clone, 'rev-parse', f'{pre}^')
    adr_blob = git(clone, 'rev-parse', f'{cand}:{ADR_PATH}')
    blob2 = git(clone, 'hash-object', '-w', '--stdin', stdin=v2)
    idx_env = {'GIT_INDEX_FILE': str(tmp / 'indice-m02')}
    git(clone, 'read-tree', cand, env=idx_env)
    git(clone, 'update-index', '--add', '--cacheinfo', f'100644,{blob2},{ADR_PATH}', env=idx_env)
    tree2 = git(clone, 'write-tree', env=idx_env)
    sha2 = hashlib.sha256(v2).hexdigest()
    plain = {}

    def replaced(original, replacement):
        return lambda: git(clone, 'replace', original, replacement)

    def unreplaced():
        clear_replace(clone)

    sb.scenario('AF4-M02-1', 'candidato normal, sin refs/replace: control positivo')

    fake = commit_tree(clone, cand_tree, (pre_parent,), CDATE, 'sustituto que contiene el ADR')

    def reproduce():
        git(clone, 'replace', pre, fake)
        plain['e'] = (git_code(clone, 'cat-file', '-e', f'{pre}:{ADR_PATH}'),
                      git_code(clone, '--no-replace-objects', 'cat-file', '-e', f'{pre}:{ADR_PATH}'))
    sb.scenario('AF4-M02-2', 'reproducción de la cuarta auditoría: refs/replace hace que un commit sin ADR parezca '
                'contenerlo', (ABSENT, CHANGED_AFTER, ('FRZ', 'refs/replace'), UNRELIABLE), reproduce, unreplaced,
                candidate=pre, note=lambda: f'git cat-file -e candidato:ADR con y sin reemplazos: {plain.get("e")}')
    fake2 = commit_tree(clone, tree2, (pre,), CDATE, 'sustituto con otro ADR')
    sb.scenario('AF4-M02-3', 'refs/replace altera un commit existente: el candidato muestra otro ADR, citado por su '
                'SHA-256', (SHA_MISMATCH, ('FRZ', 'refs/replace')), replaced(cand, fake2), unreplaced, adr_sha=sha2)
    sb.scenario('AF4-M02-3b', 'refs/replace altera el blob del ADR del candidato, citado por su SHA-256',
                (SHA_MISMATCH, ('FRZ', 'refs/replace')), replaced(adr_blob, blob2), unreplaced, adr_sha=sha2)

    # AF4-M02-4: los helpers normativos (commit, ancestros, fecha, cambios y blob) ignoran los objetos sustituidos.
    sb.register(cand, ADR_PATH, sb.blob_sha)
    wt = v.worktree_state(clone)
    keys = ('commit', 'from_base', 'ancestor', 'date', 'changed', 'gate_doc')
    before = {k: v.git_facts(clone, cand, wt, [])[k] for k in keys}
    fake_cand = commit_tree(clone, pre_tree, (pre,), '2030-01-01', 'sustituto sin el ADR')
    git(clone, 'replace', cand, fake_cand)
    seen = (git_code(clone, 'cat-file', '-e', f'{cand}:{ADR_PATH}'), git(clone, 'show', '-s', '--format=%cs', cand))
    after = {k: v.git_facts(clone, cand, wt, [])[k] for k in keys}
    blob = v.git_blob(clone, cand, ADR_PATH)
    clear_replace(clone)
    ok(seen == (128, '2030-01-01') and after == before and before['commit'] and before['from_base']
       and before['ancestor'] and blob.get('data') == adr_text(), 'AF4-M02-4a',
       'candidato sustituido por un commit sin el ADR: commit, ancestros, fecha, cambios, documento del gate y blob son '
       'los reales', f'Git sin opciones ve {seen}; el validador ve fecha {after.get("date")}')
    orphan = commit_tree(clone, cand_tree, (), CDATE, 'huérfano con el ADR')
    git(clone, 'replace', orphan, commit_tree(clone, cand_tree, (v.BASE,), '2030-01-02', 'aparenta descender de la base'))
    git(clone, 'replace', cand, commit_tree(clone, cand_tree, (pre, orphan), CDATE, 'aparenta contener al huérfano'))
    seen = (git_code(clone, 'merge-base', '--is-ancestor', v.BASE, orphan),
            git_code(clone, 'merge-base', '--is-ancestor', orphan, 'HEAD'), git(clone, 'show', '-s', '--format=%cs', orphan))
    facts = v.git_facts(clone, orphan, wt, [])
    ok(seen == (0, 0, '2030-01-02') and facts['commit'] and not facts['from_base'] and not facts['ancestor']
       and facts['date'] == CDATE, 'AF4-M02-4b', 'huérfano al que refs/replace da la base como ancestro, a HEAD como '
       'descendiente y otra fecha: los ancestros y la fecha son los reales',
       f'Git sin opciones ve {seen}; el validador ve {[facts[k] for k in ("from_base", "ancestor", "date")]}')
    sb.scenario('AF4-M02-4c', 'el validador completo con ese huérfano como candidato',
                ('no desciende de la base', 'no es ancestro de HEAD', ('FRZ', 'refs/replace')), None, unreplaced,
                candidate=orphan)

    ghost = '3' * 40

    def ghost_ref():
        git(clone, 'update-ref', f'refs/replace/{ghost}', cand)
        plain['t'] = git_code(clone, 'cat-file', '-t', ghost)
    sb.scenario('AF4-M02-5', 'error al resolver el objeto real: el candidato citado no existe, solo una ref de '
                'reemplazo con su nombre', ('no es un commit del repositorio', ('FRZ', 'refs/replace')), ghost_ref,
                unreplaced, candidate=ghost, note=lambda: f'git cat-file -t sin opciones: {plain.get("t")}')

    grafts = clone / '.git' / 'info' / 'grafts'

    def grafted():
        write(clone, '.git/info/grafts', f'{orphan} {v.BASE}\n{cand} {pre} {orphan}\n')
        plain['g'] = git_code(clone, '--no-replace-objects', 'merge-base', '--is-ancestor', orphan, 'HEAD')
    sb.scenario('AF4-M02-A1', 'injertos (info/grafts): un commit ajeno aparenta descender de la base y ser ancestro '
                'de HEAD, también sin reemplazos', (('FRZ', 'injertos'), UNRELIABLE), grafted, grafts.unlink,
                candidate=orphan, note=lambda: f'merge-base sin reemplazos: {plain.get("g")}')
    readme = git(clone, 'rev-parse', 'HEAD:README.md')
    other = git(clone, 'hash-object', '-w', '--stdin', stdin=b'# README sustituto\n')
    sb.scenario('AF4-M02-A2', 'ref de reemplazo ajena al candidato (blob de README.md): la ambigüedad falla cerrado',
                (('FRZ', 'refs/replace'), UNRELIABLE), replaced(readme, other), unreplaced)
    sb.register(cand, ADR_PATH, sb.blob_sha)
    with environ(GIT_DIR=str(tmp / 'minimo' / '.git'), GIT_WORK_TREE=str(tmp / 'minimo'),
                 GIT_INDEX_FILE=str(tmp / 'no-existe'), GIT_OBJECT_DIRECTORY=str(tmp / 'no-existe'),
                 GIT_REPLACE_REF_BASE='refs/heads/', GIT_NO_REPLACE_OBJECTS=''):
        fails, gate = sb.validate()
    ok(not fails and gate == 'NO SUPERADO', 'AF4-M02-A3', 'control positivo con un entorno hostil (GIT_DIR, '
       'GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY y GIT_REPLACE_REF_BASE): el validador lo ignora',
       f'gate {gate}' if not fails else f'fallas: {[f"{n}: {m[:140]}" for n, m in fails][:3]}')
    sb.scenario('AF4-M02-A4', 'control positivo: sin refs/replace ni injertos, el mismo candidato vuelve a ser válido')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    def snapshot():
        """HEAD, estado (también de ignorados) y entradas del índice del repositorio original."""
        return tuple(v.git(v.ROOT, *args)[1] for args in (('rev-parse', 'HEAD'), ('status', '--porcelain', '--ignored'),
                                                          ('ls-files', '-s', '-v')))
    before = snapshot()
    tmp = Path(tempfile.mkdtemp(prefix='f36sbx-git-'))
    try:
        for part in (unit, worktree, replacement, e2e, e2e_m01, e2e_m02):
            try:
                part(tmp)
            except Exception as e:  # noqa: BLE001 — una parte que no se puede ejecutar es una falla, nunca un PASS
                ok(False, part.__name__.upper(), f'parte {part.__name__} no ejecutable',
                   f'excepción {e.__class__.__name__}: {e}')
    finally:
        remove_tree(tmp)
    after = snapshot()
    ok(before == after, 'R00', 'el repositorio original no cambió: mismo HEAD, mismo estado (también de ignorados) y '
       'mismas entradas del índice')
    ok(not tmp.exists(), 'R01', 'el directorio temporal se borró')
    bad = [r for r in results if not r[0]]
    for ok_, cid, desc, detail in results:
        print(f'{"OK   " if ok_ else "FALLA"} {cid} {desc}: {detail}')
    print(f'test_f36sbx_git: {len(results) - len(bad)} casos correctos, {len(bad)} fallas')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
