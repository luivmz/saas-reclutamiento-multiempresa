#!/usr/bin/env python3
"""Metapruebas de validate_f36sbx.py y de sus baterías (AF4): ablaciones y mutación exhaustiva de hojas.

1. Ablación. Anula, una por una, cada regla, cada función de evidencia y cada comprobación AF2, AF3 y AF4 del
   validador (sobre su árbol sintáctico, en memoria) y ejecuta contra ese validador debilitado la batería en
   memoria y, cuando la pieza depende de Git, también la batería con Git real (test_f36sbx_git.py); las piezas
   de la vista de Git de AF4, que la batería en memoria no ejercita, solo con la de Git real. Cada ablación
   tiene que ser detectada por al menos un caso concreto que falle por su motivo: una excepción global, o un caso
   que solo falla porque su mutación ya no se puede montar, no cuenta como detección pertinente. Con un filtro,
   solo se ejecutan las ablaciones cuya etiqueta contiene alguna de sus subcadenas (ejecución focal).
2. Mutación de hojas. Cambia, de una en una, cada hoja y cada lista u objeto del ejemplo de conformidad y de la
   evidencia de equipo en memoria:
   - familia de forma (sufijo en textos, +1 en enteros, booleano invertido, clave adicional, elemento quitado o
     repetido): sin recalcular hashes, toda mutación del ejemplo tiene que fallar, salvo la nota libre; con los
     registros recalculados y sin resellar, solo pueden pasar los artefactos de dev que no usa el ajuste; con test
     resellado, lo que pasa se compara con la lista cerrada de cambios legítimos;
   - familia de sustitución (AF3): cada texto se sustituye por otro valor VÁLIDO de su dominio (el de otro
     registro del conjunto, un valor enumerado del contrato o un identificador F34 coherente) y se resella todo.
     Lo que sigue pasando tiene que ser un cambio legítimo cerrado, nunca un cambio de contexto o de partición;
   - en la evidencia, mutar o sustituir un solo lado (registro, informe o ADR) tiene que invalidarla, salvo los
     campos libres cerrados (propósito, licencia admitida y revisor de una dependencia).

No escribe archivos fuera de los directorios temporales de test_f36sbx_git.py y no usa red.
Uso: python -I -B docs/academico/tools/f36sbx/meta_f36sbx.py [ablaciones|hojas] [subcadena,subcadena…]
"""
import ast
import contextlib
import copy
import csv
import io
import json
import re
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_f36sbx as v  # noqa: E402
import test_f36sbx as t  # noqa: E402


def git_suite():
    """test_f36sbx_git.py, importado solo cuando una ablación lo necesita (la mutación de hojas no lo usa)."""
    import test_f36sbx_git
    return test_f36sbx_git

VALIDATOR = HERE / 'validate_f36sbx.py'
SRC = VALIDATOR.read_text(encoding='utf-8')
MEM, GIT, GIT_ONLY = ('mem',), ('mem', 'git'), ('git',)
# Partes de test_f36sbx_git.py: si una entera no se puede ejecutar, es una excepción, no una detección pertinente.
GIT_PARTS = {'UNIT', 'WORKTREE', 'REPLACEMENT', 'E2E', 'E2E_M01', 'E2E_M02'}

# Ablaciones sobre el código del validador: (etiqueta, tipo, aguja[, baterías]). 'if' anula la condición de la
# única sentencia if/elif cuya condición contiene la aguja o, si la aguja contiene «=>», cuyo «condición => primera
# sentencia» la contiene (así no coincide el if que envuelve a la comprobación); 'assign' vacía la asignación que
# la contiene; 'dictval' vacía el valor de esa clave en el único literal de diccionario que la tiene; 'need' hace
# verdadera la condición del need() que la contiene. Si la aguja no coincide exactamente una vez, la ablación no es
# aplicable y cuenta como superviviente.
SOURCE_ABLATIONS = [
    # AF2-M01: identidad visible, documento humano y coherencia con el registro.
    ('identidad: caracteres invisibles', 'assign', 'bad = invisible_chars(value)'),
    ('identidad: mínimo de letras', 'if', "startswith('L')) < min_letters"),
    ('identidad: marcadores de posición', 'if', 'key in PLACEHOLDERS'),
    ('identidad: NFC', 'if', "is_normalized('NFC', value) => e.append"),
    ('identidad: espacios exteriores', 'if', 'value != value.strip()'),
    ('auditor: identidad completa', 'assign', "e = identity_errors(au['name']"),
    ('documento: un único bloque canónico', 'if', 'len(mine) != 1'),
    ('documento: bloques f36sbx ambiguos', 'if', "others => e.append(f'{label}: otro bloque"),
    ('documento: caracteres invisibles', 'assign', 'bad = invisible_chars(text, allow_layout=True)'),
    ('documento: NFC', 'if', "is_normalized('NFC', text)"),
    ('documento: secciones requeridas', 'if', "missing => e.append(f'{label}: faltan las secciones"),
    ('documento: contenido humano mínimo', 'if', 'letters < min_letters'),
    ('documento: título de nivel 1', 'if', "=> e.append(f'{label}: debe empezar con un título"),
    ('informe: tokens canónicos fuera del bloque', 'if', "token in outside => e.append(f'FG-02"),
    ('informe: aserciones fuera del bloque', 'if', 'COUNT_ASSERTION_RX.search(outside)'),
    ('informe: contexto de los metadatos', 'if', "=> e.append('FG-02: informe: metadatos de otro esquema"),
    ('informe: commit candidato', 'if', "meta['candidate_commit'] != ev.get('candidate_commit')"),
    ('informe: auditor coherente', 'if', "canonical(meta['auditor'])"),
    ('informe: veredicto coherente', 'if', "canonical(meta['verdict'])"),
    ('informe: recuentos coherentes', 'if', "canonical(meta['findings_open'])"),
    ('informe: fecha', 'if', "=> e.append('FG-02: informe: report_date inválida"),
    ('ADR: título y contexto textual', 'if', "=> e.append('FG-12: ADR: el título no nombra su id"),
    ('ADR: estado fuera del bloque', 'if', 'STATUS_ASSERTION_RX.search(outside)'),
    ('ADR: tokens canónicos fuera del bloque', 'if', "token in outside => e.append(f'FG-12"),
    ('ADR: contexto de los metadatos', 'if', "=> e.append('FG-12: ADR: metadatos de otro esquema"),
    ('ADR: id, estado, relación y alcance coherentes', 'if', 'canonical(meta[key]) != canonical(adr[reg])'),
    ('ADR: covered_ei coherente', 'if', "=> e.append(f'FG-12: ADR: covered_ei de los metadatos"),
    ('ADR: ei09_decision coherente', 'if', "canonical(meta['ei09_decision'])"),
    ('ADR: decided_on no posterior al candidato', 'if', 'dd is None or cdate is None or dd > cdate'),
    # AF2-M02: cadena de hashes y sello de test.
    ('hash: content_hash', 'if', "a.get('content_hash') == sha256(canonical(content))"),
    ('hash: record_hash', 'if', "a.get('record_hash') != artifact_record_hash(a)"),
    ('hash: artifact_record_hash del fragmento', 'if', "f.get('artifact_record_hash') != a.get('record_hash')"),
    ('hash: text_hash', 'if', "f.get('text_hash') != sha256("),
    ('hash: fragment_hash', 'if', "f.get('fragment_hash') != fragment_record_hash(f)"),
    ('hash: output_hash', 'if', "o.get('output_hash') != output_record_hash(o)"),
    ('hash: fragment_ref_hashes', 'if', 'ref_hashes != ['),
    ('hash: input_manifest_hash', 'if', "o.get('input_manifest_hash') != input_manifest_hash("),
    ('sello: comparación', 'if', "test['seal_sha256'] != test_seal("),
    ('sello: artefactos de test', 'dictval', 'test_artifacts'),
    ('sello: fragmentos de test', 'dictval', 'test_fragments'),
    ('sello: outputs de test', 'dictval', 'test_outputs'),
    ('sello: outputs de ajuste', 'dictval', 'tuning_outputs'),
    ('sello: oro de dev', 'dictval', 'tuning_gold'),
    # AF2-M03: aislamiento entre tenants.
    ('tenant: autor y anotador', 'if', "f'ORG-{m.group(1)}' != a.get('synthetic_organization_id')"),
    ('tenant: contexto de cada referencia upstream', 'if', 'dim in ctx and ctx[dim] != a.get(field)'),
    ('tenant: cardinalidad de la referencia propia', 'if', 'got != [own]'),
    ('tenant: fuentes globales no admitidas', 'if', "src not in c['upstream_files']"),
    ('tenant: criterio del contenido citado', 'if', 'content[field] not in per_source.get(src, [])'),
    # AF2-L01 y endurecimientos asociados.
    ('ejemplo: example_id cerrado', 'if', "ex.get('example_id') != c['example_id_value']"),
    ('ejemplo: cobertura mínima', 'if', "not cond => add(f'REL-14"),
    ('texto: caracteres invisibles', 'if', "invisible_chars(value) => add(f'REL-12"),
    ('texto: NFC', 'if', "is_normalized('NFC', value) => add(f'REL-12"),
    ('output: method_config cerrado', 'if', 'not isinstance(mc, dict)'),
    # Contrato y esquema.
    ('contrato: clase única de cada identificador', 'need', 'set().union(*classes) == pattern_fields'),
    ('contrato: identificadores globales documentados', 'need', "list(gid) == ['question_id']"),
    ('contrato: archivos upstream tipados', 'need', "c.get('upstream_files') == EXPECTED_UPSTREAM_FILES"),
    ('contrato: allowlist global vacía', 'need', "c.get('global_upstream_sources') == []"),
    ('contrato: tokens ligados al tenant', 'need', "c.get('tenant_bound_tokens') == TENANT_TOKENS"),
    ('contrato: cobertura mínima', 'need', "c.get('example_coverage') == EXPECTED_COVERAGE"),
    ('contrato: esquema de hashes', 'need', "hs.get(k), dict) and hs[k].get('tag') == tag"),
    ('esquema: el ADR no cita el commit que lo contiene', 'need', "'applies_to_candidate_commit' not in"),
    # AF3-M01: el ADR es el blob de candidate_commit:path y la evidencia es versionable.
    ('git: la ruta existe en el árbol del commit', 'if', 'not entries', GIT),
    ('git: una sola entrada, con la ruta exacta', 'if', 'len(entries) != 1 or entries[0][3] != path', GIT),
    ('git: blob regular (100644)', 'if', "kind != 'blob' or mode != GIT_REGULAR_MODE", GIT),
    ('git: blob legible', 'if', "data is None => return {'error': 'no se pudo leer el blob", GIT),
    ('blob: resolución con error', 'if', "'error' in blob", GIT),
    ('blob: tipo y modo de la resolución', 'if', "blob.get('type') != 'blob'", GIT),
    ('blob: bytes del objeto Git', 'if', 'git_blob_id(data) != obj', GIT),
    ('FG-12: el ADR es un blob del commit candidato', 'if', 'why is not None', GIT),
    ('FG-12: SHA-256 del blob del candidato', 'if', "sha256(data) != adr['sha256']", GIT),
    ('evidencia: Git no la ignora', 'assign', 'ign_err = ', GIT),
    # AF3-M02: contexto canónico de todo output.
    ('REL-15: postulación sin evidencia en el conjunto', 'if', 'not expected => return'),
    ('REL-15: contexto canónico ambiguo', 'if', 'len(expected) != 1'),
    ('REL-15: campo distinto del contexto canónico', 'if', 'rec.get(k) != val'),
    ('REL-11: partición canónica del output de ajuste', 'if', "parts_of != {c['splits']['thresholds_fit_on']}"),
    ('contrato: contexto canónico', 'need', "c.get('canonical_context') == EXPECTED_CANONICAL"),
    # AF3-L01: identidad genérica.
    ('identidad: genérica, sin nombre propio', 'if', 'set(key.split()) <= GENERIC_IDENTITY_WORDS'),
    # AF4-M01: índice y árbol de trabajo vistos sin marcas ni caché de stat.
    ('AF4-M01 · índice: marca assume-unchanged', 'if', 'tag.islower()', GIT_ONLY),
    ('AF4-M01 · índice: marca skip-worktree', 'if', "tag in 'Ss'", GIT_ONLY),
    ('AF4-M01 · índice: entradas sin fusionar', 'if', "stage != '0'", GIT_ONLY),
    ('AF4-M01 · índice: submódulos y modos no verificables', 'if', 'mode not in WORKTREE_MODES', GIT_ONLY),
    ('AF4-M01 · índice: objetos ausentes', 'if', 'out is None or unresolved', GIT_ONLY),
    ('AF4-M01 · árbol de trabajo: bytes distintos del índice', 'if', 'data is None or not same_blob(', GIT_ONLY),
    ('AF4-M01 · árbol de trabajo: bit de ejecución', 'if', "filemode and mode != '120000'", GIT_ONLY),
    ('AF4-M01 · árbol de trabajo: archivos ilegibles', 'if', 'unreadable => problems.append', GIT_ONLY),
    ('AF4-M01 · sin versionar: archivos que Git no ignora', 'assign', "st['untracked'] = ", GIT_ONLY),
    ('AF4-M01 · cambios: índice frente al commit', 'if', 'tree.get(p) != index.get(p)', GIT_ONLY),
    ('AF4-M01 · FRZ: entradas normativas versionables', 'assign', 'unversioned = '),
    ('AF4 · FRZ: estado Git fiable', 'assign', "problems = s['git_state']"),
    ('AF4 · vínculo: estado Git no fiable', 'if', 'not isinstance(gs, list) or gs'),
    # AF4-M02: objetos reales, sin refs/replace ni injertos.
    ('AF4-M02 · estado: refs/replace presentes', 'if', 'out.strip() => refs = sorted(', GIT_ONLY),
    ('AF4-M02 · estado: injertos y operaciones en curso', 'if', 'os.path.lexists(Path(root) / rel)', GIT_ONLY),
    ('AF4-M02 · commit: SHA-1 de sus bytes', 'if', 'hexdigest() != sha', GIT_ONLY),
    # AF4-L01: identidades genéricas compuestas.
    ('AF4-L01 · identidad: compuesta sin nombre propio', 'if', 'all(nondistinctive(t)'),
    ('AF4-L01 · identidad: homógrafos', 'if', 'any(mixed_script(t)'),
    ('AF4-L01 · palabra: número o inicial', 'if', 'len(letters) < 2'),
    ('AF4-L01 · palabra: rol, conector o marcador', 'if', 'form in IDENTITY_NOISE'),
    ('AF4-L01 · palabra: relleno', 'if', 'IDENTITY_FILLER.fullmatch(form)'),
    ('AF4-L01 · palabra: concatenación', 'if', 'concatenated(form)'),
    ('AF4-L01 · palabra: dígitos en lugar de letras', 'assign', 'LEET = str.maketrans'),
    ('AF4-L01 · palabra: camelCase', 'if', 'value[i - 1].islower() and c.isupper()'),
]


def fs_git_blob(m):
    """Mutante del comportamiento anterior a AF3: el «blob» se lee del árbol de trabajo."""
    def f(root, sha, path):
        data = m.read_bytes(root, path)
        return {'error': 'x'} if data is None else {'mode': '100644', 'type': 'blob', 'object': m.git_blob_id(data),
                                                    'data': data}
    return f


def replace_view(m):
    """Mutante de git_run sin protección frente a refs/replace: ni --no-replace-objects ni GIT_NO_REPLACE_OBJECTS."""
    def run(root, *args, stdin=None):
        env = {k: x for k, x in m.git_env().items() if k != 'GIT_NO_REPLACE_OBJECTS'}
        try:
            r = m.subprocess.run(['git', *(o for o in m.GIT_GLOBAL if o != '--no-replace-objects'), *args], cwd=root,
                                 input=stdin, capture_output=True, env=env)
        except (OSError, ValueError):
            return None, b''
        return r.returncode, r.stdout
    return run


def legacy_commit(m):
    """Mutante de git_commit anterior a AF4: tipo con cat-file -t, padres con rev-list y fecha con git show, con la
    vista habitual de Git (refs/replace incluidas) y sin verificar el SHA-1 de los bytes."""
    def f(root, sha):
        def plain(*args):
            r = m.subprocess.run(['git', *args], cwd=root, capture_output=True)
            return r.returncode, r.stdout.decode('utf-8', 'replace').strip()
        if plain('cat-file', '-t', sha) != (0, 'commit'):
            return None
        (c1, date), (c2, tree), (c3, line) = (plain('show', '-s', '--format=%cs', sha),
                                              plain('rev-parse', f'{sha}^{{tree}}'),
                                              plain('rev-list', '--parents', '-n', '1', sha))
        return None if c1 or c2 or c3 else {'tree': tree, 'parents': line.split()[1:], 'date': date}
    return f


def lenient_eol(m):
    """Mutante de same_blob que tolera cualquier cambio de fin de línea (CRLF parcial o CR sueltos)."""
    return lambda data, obj, eol=True: m.git_blob_id(data) == obj or (
        eol and m.git_blob_id(data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')) == obj)


# Ablaciones de función: (nombre, fábrica del reemplazo a partir del módulo, baterías[, etiqueta]).
FUNCTION_ABLATIONS = [
    ('fg02_errors', lambda m: lambda *a: [], MEM), ('fg03_errors', lambda m: lambda *a: [], MEM),
    ('fg10_errors', lambda m: lambda *a: [], MEM), ('fg12_errors', lambda m: lambda *a: [], MEM),
    ('team_evidence_errors', lambda m: lambda *a: [], MEM), ('binding_errors', lambda m: lambda *a: [], MEM),
    ('approval_errors', lambda m: lambda *a: [], MEM), ('identity_errors', lambda m: lambda *a, **k: [], MEM),
    ('bundle_errors', lambda m: lambda *a: [], MEM), ('contract_semantic_errors', lambda m: lambda *a: [], MEM),
    ('team_schema_errors', lambda m: lambda *a: [], MEM), ('state_claims', lambda m: lambda *a: iter(()), MEM),
    ('doc_status_only', lambda m: lambda *a: True, MEM), ('test_seal', lambda m: lambda *a: 'x', MEM),
    ('evaluate_gate', lambda m: lambda st, c, e: 'SUPERADO' if isinstance(st, dict) else 'NO SUPERADO', MEM),
    ('git_blob', fs_git_blob, GIT), ('git_ignored', lambda m: lambda *a: [], GIT),
    ('blob_problem', lambda m: lambda b: None, GIT),
    ('placeholder_key', lambda m: lambda value: re.sub(r'[\W_]+', ' ', value.casefold()).strip(), MEM),
    # AF4-M02 y AF4-M01: vista normativa de Git.
    ('git_run', replace_view, GIT_ONLY, 'AF4-M02 · función git_run sin --no-replace-objects ni GIT_NO_REPLACE_OBJECTS'),
    ('git_env', lambda m: lambda: {**m.os.environ, **m.GIT_ENV}, GIT_ONLY,
     'AF4-M02 · función git_env que conserva las variables GIT_* heredadas'),
    ('git_commit', legacy_commit, GIT_ONLY, 'AF4-M02 · función git_commit anterior a AF4'),
    ('git_state_problems', lambda m: lambda root: [], GIT_ONLY, 'AF4-M02 · función git_state_problems anulada'),
    ('changed_since', lambda m: lambda root, sha, wt: [], GIT_ONLY, 'AF4-M01 · función changed_since anulada'),
    ('same_blob', lenient_eol, GIT, 'AF4-M01 · función same_blob que tolera cualquier fin de línea'),
    ('same_blob', lambda m: lambda data, obj, eol=True: m.git_blob_id(data) == obj, GIT,
     'AF4-M01 · función same_blob sin la conversión LF→CRLF de un checkout'),
    # AF4-L01.
    ('nondistinctive', lambda m: lambda token: False, MEM, 'AF4-L01 · función nondistinctive anulada'),
    ('identity_tokens', lambda m: lambda value: value.split(), MEM, 'AF4-L01 · función identity_tokens sin normalizar'),
    ('concatenated', lambda m: lambda word: False, MEM, 'AF4-L01 · función concatenated anulada'),
]
EXCEPTION_MARKS = ('mutación no aplicable', 'escenario no ejecutable', 'excepción')


def ablated_tree(kind, needle):
    tree = ast.parse(SRC)
    hits = 0
    for node in ast.walk(tree):
        if kind == 'if' and isinstance(node, ast.If):
            test = ast.get_source_segment(SRC, node.test)
            key = f'{test} => {ast.get_source_segment(SRC, node.body[0])}' if '=>' in needle else test
            if needle in key:
                node.test, hits = ast.Constant(False), hits + 1
        elif kind == 'assign' and isinstance(node, ast.Assign):
            if needle in (ast.get_source_segment(SRC, node) or ''):
                node.value, hits = ast.List(elts=[], ctx=ast.Load()), hits + 1
        elif kind == 'dictval' and isinstance(node, ast.Dict):
            for i, k in enumerate(node.keys):
                if isinstance(k, ast.Constant) and k.value == needle:
                    node.values[i], hits = ast.List(elts=[], ctx=ast.Load()), hits + 1
        elif kind == 'need' and isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == 'need' and node.args:
            if needle in (ast.get_source_segment(SRC, node.args[0]) or ''):
                node.args[0], hits = ast.Constant(True), hits + 1
    return ast.fix_missing_locations(tree), hits


def load(tree):
    mod = types.ModuleType('validate_f36sbx')
    mod.__file__ = str(VALIDATOR)
    exec(compile(tree, str(VALIDATOR), 'exec'), mod.__dict__)  # noqa: S102 — el propio validador, mutado en memoria
    return mod


def run_suite(module, mod):
    """Ejecuta una batería (test_f36sbx o test_f36sbx_git) contra mod; devuelve los casos que fallan."""
    module.v = mod
    module.results.clear()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            module.main()
    except Exception as e:  # noqa: BLE001 — una batería que no termina no es una detección pertinente
        return [(module.__name__, f'excepción global {e.__class__.__name__}')]
    finally:
        module.v = v
    return [(cid, str(detail)) for ok, cid, _, detail in module.results if not ok]


def battery(mod, suites=MEM, resealed=False):
    """Casos que fallan con mod, por batería. Con resealed=True, el ejemplo de la fotografía se vuelve a sellar
    antes con el propio mod: una ablación del sello ya no la delatan los controles positivos."""
    saved = t.BASE['texts'][v.EXAMPLE]
    try:
        if resealed:
            ex = mod.strict_json(saved)
            mod.seal_bundle(ex, t.CONTRACT)
            t.BASE['texts'][v.EXAMPLE] = json.dumps(ex, ensure_ascii=False, indent=2)
        fails = run_suite(t, mod) if 'mem' in suites else []
        if 'git' in suites:
            fails += [(f'git:{cid}', d) for cid, d in run_suite(git_suite(), mod)]
    finally:
        t.BASE['texts'][v.EXAMPLE] = saved
    return fails


def classify(fails, base):
    """Separa las detecciones pertinentes (un caso concreto falla por su motivo) de las debidas a excepciones."""
    new = [(cid, d) for cid, d in fails if cid not in base]
    exc = sorted(cid for cid, d in new if d.startswith(EXCEPTION_MARKS) or cid.split(':')[-1] in GIT_PARTS)
    return sorted(cid for cid, _ in new if cid not in exc), exc


def ablations(only=None):
    """Ejecuta las ablaciones (con only, solo aquellas cuya etiqueta contiene alguna de sus subcadenas)."""
    def wanted(label):
        return not only or any(x.casefold() in label.casefold() for x in only)
    base_fails = battery(load(ast.parse(SRC)), GIT)
    base = {cid for cid, _ in base_fails}
    print(f'línea base (memoria y Git real): {len(base)} casos fallan {sorted(base)}')
    if only:
        print(f'ejecución focal: ablaciones cuya etiqueta contiene {only}')
    rows = []

    def record(label, mod, suites, resealed=False):
        rows.append((label, *classify(battery(mod, suites, resealed), base)))
    for name, _ in v.RULES:
        if not wanted(f'regla {name} anulada'):
            continue
        mod = load(ast.parse(SRC))
        mod.RULES = [(n, (lambda s: []) if n == name else fn) for n, fn in mod.RULES]
        record(f'regla {name} anulada', mod, MEM)
    for entry in FUNCTION_ABLATIONS:
        name, factory, suites = entry[:3]
        label = entry[3] if len(entry) > 3 else f'función {name} anulada'
        if not wanted(label):
            continue
        mod = load(ast.parse(SRC))
        repl = factory(mod)
        setattr(mod, name, repl)
        if name in ('fg02_errors', 'fg03_errors', 'fg10_errors', 'fg12_errors'):
            mod.SPECIFIC[f'FG-{name[2:4]}'] = repl
        record(label, mod, suites)
        if name == 'test_seal':
            record(f'{label}, con el ejemplo resellado', mod, suites, True)
    for entry in SOURCE_ABLATIONS:
        label, kind, needle = entry[:3]
        if not wanted(label):
            continue
        suites = entry[3] if len(entry) > 3 else MEM
        tree, hits = ablated_tree(kind, needle)
        if hits != 1:
            rows.append((f'{label} (no aplicable: {hits} coincidencias)', [], []))
            continue
        record(label, load(tree), suites)
        if kind == 'dictval':
            record(f'{label}, con el ejemplo resellado', load(tree), suites, True)
    bad = 0
    for label, killed, exc in rows:
        state = 'DETECTADA ' if killed else ('SOLO EXCEPCIÓN' if exc else 'SOBREVIVE ')
        bad += not killed
        print(f'{state} {label}: {len(killed)} casos {killed[:6]}{" …" if len(killed) > 6 else ""}'
              + (f' · por excepción: {exc[:4]}' if exc else ''))
    print(f'ablaciones: {len(rows)}, detectadas por casos pertinentes {len(rows) - bad}, sin detección pertinente {bad}')
    return not base and not bad


# ---------------------------------------------------------------- mutación de hojas

def nodes(obj, path=()):
    yield path, obj
    if isinstance(obj, dict):
        for k, x in obj.items():
            yield from nodes(x, path + (k,))
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            yield from nodes(x, path + (i,))


def mutations(value):
    if isinstance(value, bool):
        yield 'invertido', not value
    elif isinstance(value, int):
        yield '+1', value + 1
    elif isinstance(value, str):
        yield 'sufijo', value + 'X'
    elif value is None:
        yield 'nulo→texto', 'X'
    elif isinstance(value, dict):
        yield 'clave adicional', {**value, 'x_extra': 1}
    elif isinstance(value, list) and value:
        yield 'sin el último', value[:-1]
        yield 'primero repetido', value + [copy.deepcopy(value[0])]


def put(obj, path, value):
    if not path:
        return value
    cur = obj
    for p in path[:-1]:
        cur = cur[p]
    cur[path[-1]] = value
    return obj


def label(ex, path):
    """Ruta legible: los índices de registros se sustituyen por su identificador."""
    out, cur = [], ex
    for p in path:
        nxt = cur[p]
        if isinstance(p, int) and isinstance(nxt, dict):
            out.append(nxt.get('synthetic_id') or nxt.get('fragment_id') or nxt.get('output_id') or str(p))
        else:
            out.append(str(p))
        cur = nxt
    return '/'.join(out)


def field_of(path):
    """Nombre del campo de una hoja: su clave o, si es un elemento de lista, la clave de la lista."""
    for p in reversed(path):
        if isinstance(p, str):
            return p
    return ''


# Cambios legítimos que siguen siendo conformes tras recalcular y resellar: (sufijo de ruta, mutación).
LEGIT_RESEALED = {('text_synthetic', 'sufijo'), ('issuer_synthetic', 'sufijo'), ('title_synthetic', 'sufijo'),
                  ('seed', '+1'), ('char_start', '+1'), ('char_end', '+1'), ('top_k', '+1'), ('note', 'sufijo'),
                  ('sections', 'primero repetido'), ('turns', 'primero repetido'), ('outputs', 'sin el último'),
                  ('fragment_refs', 'sin el último')}
# Artefactos de dev que no usa el ajuste: pueden cambiar sin resellar (dev no se sella; límite documentado).
UNSEALED_DEV = {'SBX36-ORG-S1-ART-0005', 'SBX36-ORG-S1-ART-0008'}
# Familia de sustitución: valores válidos del dominio que no aparecen en el ejemplo (F34 coherente u otro tenant).
EXTRA_VALUES = {'scenario_id': ['SC36-99'], 'vacancy_token': ['VAC-0010'], 'application_token': ['APP-00015', 'APP-00053'],
                'synthetic_organization_id': ['ORG-S2'], 'author_token': ['EV-S1-07', 'EV-S2-01'],
                'annotator_token': ['ANT36-S1-09', 'ANT36-S2-01'], 'query_criterion_id': ['CRI-0018', 'CRI-0045'],
                'criterion_id': ['CRI-0005', 'CRI-0018'], 'template_family': ['TF36-CC']}
HASH_FIELDS = {'content_hash', 'record_hash', 'artifact_record_hash', 'text_hash', 'fragment_hash',
               'input_manifest_hash', 'output_hash', 'seal_sha256', 'sha256', 'fragment_ref_hashes'}
# Campos cuyo valor puede cambiar, dentro de su dominio, sin romper ninguna relación: contenido libre o enumerado.
FREE_FIELDS = {'section_kind', 'text_synthetic', 'issuer_synthetic', 'title_synthetic', 'speaker_role', 'relevance',
               'overlap_stratum', 'observation_kind', 'attack_kind', 'expected_outcome', 'format', 'grupo_sintetico',
               'note'}


def criterion_vacancies():
    data = t.BASE['upstream'][v.F34 + 'criteria.csv'].decode('utf-8')
    return {r['criterion_id']: r['vacancy_token'] for r in csv.DictReader(io.StringIO(data))}


def legit_swap(path, field, old, new, vac_of):
    """¿La sustitución, conforme tras resellar, es un cambio legítimo cerrado y no una relación rota?"""
    if field in FREE_FIELDS:
        return True
    if field == 'fragment_id' and path[0] == 'artifacts':
        # Una anotación de oro que pasa a otro fragmento: REL-08 ya exige que exista y sea de su mismo contexto.
        return True
    if field == 'application_token' and path[0] == 'outputs':
        # Un output de otra postulación con evidencia en su mismo contexto: REL-15 ya exige ese contexto canónico.
        return True
    if field in ('author_token', 'annotator_token'):
        return old.split('-')[1] == new.split('-')[1]
    if field == 'template_id':
        return old.split('-')[1] == new.split('-')[1]
    if field == 'query_criterion_id':
        return vac_of.get(old) is not None and vac_of.get(old) == vac_of.get(new)
    return False


def alternatives(ex0, contract):
    """Valores válidos alternativos de cada campo de texto: los vistos en el conjunto, los enumerados y los extra."""
    seen = {}
    for path, value in nodes(ex0):
        if isinstance(value, str) and path:
            seen.setdefault(field_of(path), set()).add(value)
    enums = contract['enums']
    for field, kind in contract['content_field_types'].items():
        if kind.startswith('enum:'):
            seen.setdefault(field, set()).update(enums[kind[5:]])
    for field in ('partition', 'stage', 'artifact_type'):
        seen.setdefault(field, set()).update(enums[field])
    for field, extra in EXTRA_VALUES.items():
        seen.setdefault(field, set()).update(extra)
    return seen


def example_leaves():
    ex0 = v.strict_json(t.BASE['texts'][v.EXAMPLE])
    up = t.BASE['upstream']
    problems, stats = [], {'raw': 0, 'borradas': 0, 'legitimas': 0, 'swaps': 0, 'swaps_legitimos': 0}
    for path, value in list(nodes(ex0)):
        if not path:
            continue
        where = label(ex0, path)
        for kind, new in mutations(value):
            results = {}
            for mode in ('raw', 'rehash', 'reseal'):
                ex = put(copy.deepcopy(ex0), path, copy.deepcopy(new))
                try:
                    if mode == 'rehash':
                        t.rehash_all(ex)
                    elif mode == 'reseal':
                        t.reseal(ex)
                except Exception:  # noqa: BLE001 — si no se puede recalcular, se evalúa tal cual
                    pass
                if ex == ex0:
                    # El recálculo restauró la hoja mutada (un hash, el sello o una lista derivada): no hay cambio.
                    results[mode] = 'borrada'
                    continue
                results[mode] = 'PASA' if not v.bundle_errors(t.CONTRACT, ex, up) else 'falla'
            stats['raw'] += 1
            if results['raw'] == 'PASA' and (path[-1], kind) != ('note', 'sufijo'):
                problems.append(f'sin recalcular pasa: {where} ({kind})')
            if results['rehash'] == 'PASA' and (path[-1], kind) != ('note', 'sufijo') \
                    and not (path[0] == 'artifacts' and ex0['artifacts'][path[1]]['synthetic_id'] in UNSEALED_DEV):
                problems.append(f'sin resellar pasa: {where} ({kind})')
            if results['reseal'] == 'borrada':
                stats['borradas'] += 1
            elif results['reseal'] == 'PASA':
                if (path[-1], kind) in LEGIT_RESEALED:
                    stats['legitimas'] += 1
                else:
                    problems.append(f'resellada pasa y no es un cambio legítimo cerrado: {where} ({kind})')
    # Familia de sustitución por valores válidos del dominio, con todo recalculado y test resellado.
    alts, vac_of = alternatives(ex0, t.CONTRACT), criterion_vacancies()
    for path, value in list(nodes(ex0)):
        field = field_of(path)
        if not path or not isinstance(value, str) or field in HASH_FIELDS:
            continue
        for new in sorted(alts.get(field, set()) - {value}):
            ex = put(copy.deepcopy(ex0), path, new)
            try:
                t.reseal(ex)
            except Exception:  # noqa: BLE001
                pass
            stats['swaps'] += 1
            if ex != ex0 and not v.bundle_errors(t.CONTRACT, ex, up):
                if legit_swap(path, field, value, new, vac_of):
                    stats['swaps_legitimos'] += 1
                else:
                    problems.append(f'sustitución válida y resellada que pasa: {label(ex0, path)}: {value} → {new}')
    print(f'ejemplo: {stats["raw"]} mutaciones de forma (resellado: {stats["legitimas"]} cambios legítimos conformes, '
          f'{stats["borradas"]} borradas por el recálculo) y {stats["swaps"]} sustituciones por valores válidos del '
          f'dominio ({stats["swaps_legitimos"]} cambios legítimos conformes)')
    return problems


def evidence_alternatives():
    schema = v.strict_json(t.BASE['texts'][v.TEAM_SCHEMA])
    crit = schema['criteria']
    return {'verdict': crit['FG-02']['verdicts'], 'kind': crit['FG-02']['auditor_kinds'],
            'decision': crit['FG-03']['decisions'], 'numbering_f36_m01': crit['FG-03']['numbering_values'],
            'license': crit['FG-10']['licenses'], 'approval_status': crit['FG-10']['approval_statuses'],
            'vote': schema['approvals']['votes'], 'member': schema['team_members'],
            'reviewed_by': schema['team_members'], 'status': crit['FG-12']['adr_statuses'],
            'ei09_decision': crit['FG-12']['ei09_decisions'], 'authorized_ei': ['EI-02', 'EI-08', 'EI-19'],
            'covered_ei': ['EI-08', 'EI-11', 'EI-19'], 'related_ei': ['EI-11', 'EI-07']}


def evidence_leaves():
    problems, count = [], 0
    sides = []
    base = t.evidence_docs(t.AUTH)
    for fg in v.FG_TEAM:
        for path, value in list(nodes(base[fg])):
            if path:
                sides.append(('registro', fg, path, value))
    ctx0 = t.build()
    for path, value in list(nodes(t.report_meta(json.loads(ctx0['evidence'][t.path('FG-02')])))):
        if path:
            sides.append(('informe', 'FG-02', path, value))
    for path, value in list(nodes(t.adr_meta(json.loads(ctx0['evidence'][t.path('FG-12')])))):
        if path:
            sides.append(('ADR', 'FG-12', path, value))
    alts = evidence_alternatives()
    legit_free = {('FG-10', 'purpose', 'sufijo'), ('FG-10', 'license', 'sustitución'), ('FG-10', 'reviewed_by', 'sustitución')}
    for side, fg, path, value in sides:
        candidates = list(mutations(value))
        if isinstance(value, str):
            candidates += [('sustitución', x) for x in alts.get(field_of(path), []) if x != value]
        for kind, new in candidates:
            count += 1
            if side == 'registro':
                def mutate(docs, ctx, fg=fg, path=path, new=new):
                    put(docs[fg], path, copy.deepcopy(new))
            elif side == 'informe':
                mutate = t.set_report(lambda m, path=path, new=new: put(m, path, copy.deepcopy(new)))
            else:
                mutate = t.set_adr(lambda m, path=path, new=new: put(m, path, copy.deepcopy(new)))
            try:
                errs = v.team_evidence_errors(fg, t.build(t.AUTH, mutate))
            except Exception as e:  # noqa: BLE001
                errs = [f'excepción {e.__class__.__name__}']
            legit = side == 'registro' and (fg, field_of(path), kind) in legit_free
            if not errs and not legit:
                problems.append(f'{side} {fg}: {"/".join(map(str, path))} ({kind} → {new!r}) sigue siendo válido')
    print(f'evidencia: {count} mutaciones y sustituciones de un solo lado (registro, informe o ADR)')
    return problems


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    what = sys.argv[1] if len(sys.argv) > 1 else 'todo'
    only = [x for x in sys.argv[2].split(',') if x] if len(sys.argv) > 2 else None
    ok = True
    if what in ('todo', 'hojas'):
        problems = example_leaves() + evidence_leaves()
        for p in problems:
            print(f'FALSO PASS {p}')
        print(f'mutación de hojas: {len(problems)} falsos PASS')
        ok = ok and not problems
    if what in ('todo', 'ablaciones'):
        ok = ablations(only) and ok
    print(f'meta_f36sbx: {"sin supervivientes ni falsos PASS" if ok else "HAY SUPERVIVIENTES O FALSOS PASS"}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
