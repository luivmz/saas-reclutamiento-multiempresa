#!/usr/bin/env python3
"""Metapruebas de validate_f36sbx.py y de su batería (AF2): ablaciones y mutación exhaustiva de hojas.

1. Ablación. Anula, una por una, cada regla, cada función de evidencia y cada comprobación AF2 del validador
   (sobre su árbol sintáctico, en memoria) y ejecuta la batería completa contra ese validador debilitado. Cada
   ablación tiene que ser detectada por al menos un caso; si alguna sobrevive, la batería no prueba esa pieza.
2. Mutación de hojas. Cambia, de una en una, cada hoja y cada lista u objeto del ejemplo de conformidad y de la
   evidencia de equipo en memoria (sufijo en textos, +1 en enteros, booleano invertido, clave adicional,
   elemento quitado o repetido):
   - sin recalcular hashes, toda mutación del ejemplo tiene que fallar, salvo la nota libre del ejemplo;
   - con los registros recalculados y sin resellar, solo pueden pasar los artefactos de dev que no usa el ajuste;
   - con todo recalculado y test resellado, lo que pasa se compara con la lista cerrada de cambios legítimos;
   - en la evidencia, mutar un solo lado (registro, informe o ADR) tiene que invalidarla, salvo el propósito
     libre de una dependencia.

No escribe archivos ni usa red. Uso: python -I -B docs/academico/tools/f36sbx/meta_f36sbx.py [ablaciones|hojas]
"""
import ast
import contextlib
import copy
import io
import json
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_f36sbx as v  # noqa: E402
import test_f36sbx as t  # noqa: E402

VALIDATOR = HERE / 'validate_f36sbx.py'
SRC = VALIDATOR.read_text(encoding='utf-8')

# Ablaciones sobre el código del validador: (etiqueta, tipo, aguja). 'if' anula la condición de la única sentencia
# if/elif cuya condición contiene la aguja o, si la aguja contiene «=>», cuyo «condición => primera sentencia» la
# contiene (así no coincide el if que envuelve a la comprobación); 'assign' vacía la asignación que la contiene;
# 'dictval' vacía el valor de esa clave en el único literal de diccionario que la tiene; 'need' hace verdadera la
# condición del need() que la contiene. Si la aguja no coincide exactamente una vez, la ablación no es aplicable y
# cuenta como superviviente.
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
    # Contrato v3 y esquema v2.
    ('contrato: clase única de cada identificador', 'need', 'set().union(*classes) == pattern_fields'),
    ('contrato: identificadores globales documentados', 'need', "list(gid) == ['question_id']"),
    ('contrato: archivos upstream tipados', 'need', "c.get('upstream_files') == EXPECTED_UPSTREAM_FILES"),
    ('contrato: allowlist global vacía', 'need', "c.get('global_upstream_sources') == []"),
    ('contrato: tokens ligados al tenant', 'need', "c.get('tenant_bound_tokens') == TENANT_TOKENS"),
    ('contrato: cobertura mínima', 'need', "c.get('example_coverage') == EXPECTED_COVERAGE"),
    ('contrato: esquema de hashes', 'need', "hs.get(k), dict) and hs[k].get('tag') == tag"),
    ('esquema: el ADR no cita el commit que lo contiene', 'need', "'applies_to_candidate_commit' not in"),
]

FUNCTION_ABLATIONS = [
    ('fg02_errors', lambda *a: []), ('fg03_errors', lambda *a: []), ('fg10_errors', lambda *a: []),
    ('fg12_errors', lambda *a: []), ('team_evidence_errors', lambda *a: []), ('binding_errors', lambda *a: []),
    ('approval_errors', lambda *a: []), ('identity_errors', lambda *a, **k: []), ('bundle_errors', lambda *a: []),
    ('contract_semantic_errors', lambda *a: []), ('team_schema_errors', lambda *a: []),
    ('state_claims', lambda *a: iter(())), ('doc_status_only', lambda *a: True), ('test_seal', lambda *a: 'x'),
    ('evaluate_gate', lambda st, c, e: 'SUPERADO' if isinstance(st, dict) else 'NO SUPERADO'),
]


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


def battery(mod, resealed=False):
    """Ejecuta la batería completa contra mod y devuelve los casos que fallan.

    Con resealed=True, el ejemplo de la fotografía se vuelve a sellar antes con el propio mod: una ablación del
    sello ya no la delatan los controles positivos, y solo la detectan los casos negativos."""
    t.v = mod
    t.results.clear()
    saved = t.BASE['texts'][v.EXAMPLE]
    try:
        if resealed:
            ex = mod.strict_json(saved)
            mod.seal_bundle(ex, t.CONTRACT)
            t.BASE['texts'][v.EXAMPLE] = json.dumps(ex, ensure_ascii=False, indent=2)
        with contextlib.redirect_stdout(io.StringIO()):
            t.main()
    except Exception as e:  # noqa: BLE001 — una batería que no termina cuenta como detección
        return [f'excepción {e.__class__.__name__}']
    finally:
        t.v = v
        t.BASE['texts'][v.EXAMPLE] = saved
    return sorted(cid for ok, cid, _, _ in t.results if not ok)


def ablations():
    base = battery(load(ast.parse(SRC)))
    print(f'línea base: {len(base)} casos fallan {base}')
    rows = []
    for name, _ in v.RULES:
        mod = load(ast.parse(SRC))
        mod.RULES = [(n, (lambda s: []) if n == name else fn) for n, fn in mod.RULES]
        rows.append((f'regla {name} anulada', sorted(set(battery(mod)) - set(base))))
    for name, repl in FUNCTION_ABLATIONS:
        mod = load(ast.parse(SRC))
        setattr(mod, name, repl)
        if name in ('fg02_errors', 'fg03_errors', 'fg10_errors', 'fg12_errors'):
            mod.SPECIFIC[f'FG-{name[2:4]}'] = repl
        rows.append((f'función {name} anulada', sorted(set(battery(mod)) - set(base))))
        if name == 'test_seal':
            rows.append((f'función {name} anulada, con el ejemplo resellado', sorted(set(battery(mod, True)) - set(base))))
    for label, kind, needle in SOURCE_ABLATIONS:
        tree, hits = ablated_tree(kind, needle)
        if hits != 1:
            rows.append((f'{label} (no aplicable: {hits} coincidencias)', []))
            continue
        rows.append((label, sorted(set(battery(load(tree))) - set(base))))
        if kind == 'dictval':
            rows.append((f'{label}, con el ejemplo resellado', sorted(set(battery(load(tree), True)) - set(base))))
    survivors = [label for label, killed in rows if not killed]
    for label, killed in rows:
        print(f'{"DETECTADA " if killed else "SOBREVIVE "} {label}: {len(killed)} casos {killed[:6]}'
              f'{" …" if len(killed) > 6 else ""}')
    print(f'ablaciones: {len(rows)}, detectadas {len(rows) - len(survivors)}, sobreviven {len(survivors)}')
    return not base and not survivors


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


# Cambios legítimos que siguen siendo conformes tras recalcular y resellar: (sufijo de ruta, mutación).
LEGIT_RESEALED = {('text_synthetic', 'sufijo'), ('issuer_synthetic', 'sufijo'), ('title_synthetic', 'sufijo'),
                  ('seed', '+1'), ('char_start', '+1'), ('char_end', '+1'), ('top_k', '+1'), ('note', 'sufijo'),
                  ('sections', 'primero repetido'), ('turns', 'primero repetido'), ('outputs', 'sin el último'),
                  ('fragment_refs', 'sin el último')}
# Artefactos de dev que no usa el ajuste: pueden cambiar sin resellar (dev no se sella; límite documentado).
UNSEALED_DEV = {'SBX36-ORG-S1-ART-0005', 'SBX36-ORG-S1-ART-0008'}


def example_leaves():
    ex0 = v.strict_json(t.BASE['texts'][v.EXAMPLE])
    up = t.BASE['upstream']
    problems, stats = [], {'raw': 0, 'rehash': 0, 'reseal': 0, 'borradas': 0, 'legitimas': 0}
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
    print(f'ejemplo: {stats["raw"]} mutaciones de hoja; resellado: {stats["legitimas"]} cambios legítimos conformes, '
          f'{stats["borradas"]} borradas por el recálculo (hashes y sello)')
    return problems


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
    for side, fg, path, value in sides:
        for kind, new in mutations(value):
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
            legit = side == 'registro' and fg == 'FG-10' and path[-1] == 'purpose' and kind == 'sufijo'
            if not errs and not legit:
                problems.append(f'{side} {fg}: {"/".join(map(str, path))} ({kind}) sigue siendo válido')
    print(f'evidencia: {count} mutaciones de un solo lado (registro, informe o ADR)')
    return problems


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    what = sys.argv[1] if len(sys.argv) > 1 else 'todo'
    ok = True
    if what in ('todo', 'hojas'):
        problems = example_leaves() + evidence_leaves()
        for p in problems:
            print(f'FALSO PASS {p}')
        print(f'mutación de hojas: {len(problems)} falsos PASS')
        ok = ok and not problems
    if what in ('todo', 'ablaciones'):
        ok = ablations() and ok
    print(f'meta_f36sbx: {"sin supervivientes ni falsos PASS" if ok else "HAY SUPERVIVIENTES O FALSOS PASS"}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
