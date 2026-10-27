#!/usr/bin/env python3
"""Pruebas negativas, mutantes y controles positivos de validate_f36sbx.py, versión 3 (AF2).

Todo ocurre en memoria, sobre copias de la fotografía del repositorio: no se escribe ningún archivo. La
evidencia de equipo válida, el informe de auditoría, la dependencia y el ADR de los controles positivos son
ficticios y solo existen en memoria. Cada mutante debe hacer fallar su regla y, cuando se indica, con un motivo
concreto; si la mutación ya no se puede aplicar, la prueba falla.

Grupos: T (control), M (gobierno, matriz, threat model, plan, alcance, dependencias, PII y enlaces),
C (contrato), R (relaciones del ejemplo), H (cadena de hashes y sello de test), X (aislamiento entre tenants y
procedencia), E (semántica de la evidencia de equipo), D (informe y ADR: bloque canónico y coherencia),
GR (registro de evidencia en el repositorio), G (regla de decisión), AUD (falsos PASS de la auditoría AF1),
AF2-01..AF2-33 (pruebas obligatorias de la auditoría AF2, que incluyen sus doce falsos PASS reconstruidos) y
P (controles positivos, incluidos los resellados).

Los mutantes del ejemplo se evalúan, salvo que se indique, con todos sus hashes recalculados y test vuelto a
sellar: así solo puede fallar la invariante semántica que se prueba (hashes válidos de contenido inválido).

Uso: python -I -B docs/academico/tools/f36sbx/test_f36sbx.py
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_f36sbx as v  # noqa: E402

M, T, R, G = v.MATRIX, v.THREATS, v.PLAN, v.GATE_DOC
C, S, CH, EX, SCH = v.CONTRACT, v.GATE_STATE, v.CHARTER, v.EXAMPLE, v.TEAM_SCHEMA
PR = v.PKG + '/README.md'
CE = v.PKG + '/F36SBX_Contrato_Evidencia.md'
EV = v.GATE_EVIDENCE
REPORT = EV + 'FG-02_informe_auditoria.md'
ADR_PATH = 'docs/academico/f36-sbx/ADR_006_prueba_en_memoria.md'
CAND = 'c' * 40
OTHER = 'd' * 40
CDATE = '2026-10-26'
RDATE = '2026-10-27'
AUTH = ['EI-01', 'EI-07', 'EI-09', 'EI-10']
F34 = 'docs/academico/datos-sinteticos/dataset/'
SEAL = 'el sello de test no coincide'

results = []


def ok(cond, cid, desc, detail):
    results.append((bool(cond), cid, desc, detail))


NOT_APPLICABLE = (AssertionError, KeyError, IndexError, TypeError, ValueError, StopIteration, AttributeError)


# ---------------------------------------------------------------- utilidades de mutación

def sub(path, old, new):
    def f(s):
        text = s['texts'][path]
        assert text is not None and old in text, f'{path}: no contiene {old!r}'
        s['texts'][path] = text.replace(old, new, 1)
    return f


def drop_line(path, prefix):
    def f(s):
        lines = s['texts'][path].split('\n')
        hit = [ln for ln in lines if ln.startswith(prefix)]
        assert len(hit) == 1, f'{path}: {len(hit)} líneas empiezan por {prefix!r}'
        s['texts'][path] = '\n'.join(ln for ln in lines if not ln.startswith(prefix))
    return f


def jmut(path, fn):
    def f(s):
        data = json.loads(s['texts'][path])
        fn(data)
        s['texts'][path] = json.dumps(data, ensure_ascii=False, indent=2)
    return f


def chain(*fns):
    def f(s):
        for fn in fns:
            fn(s)
    return f


def setkey(key, value):
    def f(s):
        s[key] = value
    return f


def add_changed(path):
    def f(s):
        s['changed'] = set(s['changed']) | {path}
    return f


def add_tool(path, src):
    def f(s):
        s['tools'][path] = src
        s['changed_py'][path] = src
    return f


def append_tool(src):
    def f(s):
        rel = v.TOOLS + '/validate_f36sbx.py'
        s['tools'][rel] = s['tools'][rel] + src
    return f


def failing(snap):
    res, _ = v.run(snap)
    return {(n, m) for n, ok_, m in res if not ok_}


def case(cid, desc, mutation, rule, needle=None):
    snap = copy.deepcopy(BASE)
    try:
        mutation(snap)
    except NOT_APPLICABLE as e:
        ok(False, cid, desc, f'mutación no aplicable: {e.__class__.__name__}: {e}')
        return
    fails = failing(snap)
    hit = [m for n, m in fails if n == rule and (needle is None or needle in m)]
    detail = f'falla {rule}' + (f' («{needle}»)' if needle else '') if hit else \
        f'esperaba FALLA {rule}' + (f' con «{needle}»' if needle else '') + f'; fallaron {sorted({n for n, _ in fails})}'
    ok(hit, cid, desc, detail)


def pos(cid, desc, mutation):
    """Control positivo: la mutación es legítima y el validador completo pasa sin fallas (gate NO SUPERADO)."""
    snap = copy.deepcopy(BASE)
    try:
        mutation(snap)
    except NOT_APPLICABLE as e:
        ok(False, cid, desc, f'mutación no aplicable: {e.__class__.__name__}: {e}')
        return
    res, gate = v.run(snap)
    fl = [f'{n}: {m[:200]}' for n, ok_, m in res if not ok_]
    ok(not fl and gate == 'NO SUPERADO', cid, desc, f'sin fallas, gate {gate}' if not fl else f'fallas: {fl}')


# ---------------------------------------------------------------- ejemplo de conformidad

def art(ex, n):
    return next(a for a in ex['artifacts'] if a['synthetic_id'] == f'SBX36-ORG-S1-ART-{n:04d}')


def frg(ex, n):
    return next(f for f in ex['fragments'] if f['fragment_id'] == f'SBX36-ORG-S1-FRG-{n:04d}')


def out(ex, n):
    return next(o for o in ex['outputs'] if o['output_id'] == f'SBX36-ORG-S1-OUT-{n:04d}')


def rehash(a):
    """Recalcula content_hash, el de la provenance y record_hash de un artefacto, y nada más."""
    a['content_hash'] = v.sha256(v.canonical(a['content']))
    a['provenance']['content_hash'] = a['content_hash']
    a['record_hash'] = v.artifact_record_hash(a)


def rehash_fragment(ex, n):
    """Recalcula text_hash y fragment_hash de un fragmento, y nada más (sus outputs quedan desactualizados)."""
    f = frg(ex, n)
    a = next(x for x in ex['artifacts'] if x['synthetic_id'] == f['artifact_id'])
    text = v.resolve_text(a['content'], f['text_path'], CONTRACT['artifact_types'][a['artifact_type']]['text_paths'])
    f['text_hash'] = v.sha256(text[f['char_start']:f['char_end']].encode('utf-8'))
    f['fragment_hash'] = v.fragment_record_hash(f)


def rehash_all(ex):
    """Recalcula toda la cadena de hashes de registro, pero conserva el sello de test: no vuelve a sellar."""
    test = ex['partition_manifest']['partitions']['test']
    seal = test['seal_sha256']
    v.seal_bundle(ex, CONTRACT)
    test['seal_sha256'] = seal


def reseal(ex):
    """Recalcula toda la cadena de hashes y vuelve a sellar test."""
    v.seal_bundle(ex, CONTRACT)


def rel(cid, desc, fn, needle, mode='reseal'):
    """Mutante del ejemplo que debe hacer fallar CTR con el motivo indicado.

    mode='reseal': hashes válidos y test resellado; 'rehash': registros recalculados sin resellar;
    'raw': sin recalcular nada."""
    def g(e):
        fn(e)
        if mode == 'reseal':
            reseal(e)
        elif mode == 'rehash':
            rehash_all(e)
    case(cid, desc, jmut(EX, g), 'CTR', needle)


def bundle_of(fn, mode):
    ex = v.strict_json(BASE['texts'][EX])
    fn(ex)
    (reseal if mode == 'reseal' else rehash_all)(ex)
    return ex, v.bundle_errors(CONTRACT, ex, BASE['upstream'])


def seal_only(cid, desc, fn):
    """Cambio coherente de test con los registros recalculados y sin resellar: el único error es el sello, y el
    validador completo FALLA en CTR."""
    try:
        _, errs = bundle_of(fn, 'rehash')
    except NOT_APPLICABLE as e:
        ok(False, cid, desc, f'mutación no aplicable: {e.__class__.__name__}: {e}')
        return
    only = len(errs) == 1 and errs[0].startswith('REL-11 ' + SEAL)
    snap = copy.deepcopy(BASE)
    jmut(EX, lambda e: (fn(e), rehash_all(e)))(snap)
    hit = [m for n, m in failing(snap) if n == 'CTR' and SEAL in m]
    ok(only and hit, cid, desc, 'solo lo detecta el sello y el validador falla' if only and hit else
       f'errores {errs[:3]}; validador {"falla" if hit else "no falla"} en CTR')


def resealed(cid, desc, fn):
    """Control positivo resellado: el mismo cambio, con test vuelto a sellar, es conforme y el validador pasa."""
    try:
        _, errs = bundle_of(fn, 'reseal')
    except NOT_APPLICABLE as e:
        ok(False, cid, desc, f'mutación no aplicable: {e.__class__.__name__}: {e}')
        return
    if errs:
        ok(False, cid, desc, f'errores {errs[:3]}')
        return
    pos(cid, desc, jmut(EX, lambda e: (fn(e), reseal(e))))


def remap(obj, table):
    """Copia de obj con cada cadena sustituida por su valor en table (valores completos, nunca subcadenas)."""
    if isinstance(obj, dict):
        return {k: remap(x, table) for k, x in obj.items()}
    if isinstance(obj, list):
        return [remap(x, table) for x in obj]
    return table.get(obj, obj) if isinstance(obj, str) else obj


def transplant(table, partition='test', ids=None):
    """Trasplante coherente de identidad: sustituye valores en todos los registros de una partición y en el
    manifiesto; ids(e) añade a la tabla los identificadores que cambian de organización."""
    def f(e):
        t = dict(table)
        if ids:
            t.update(ids(e))
        for key in ('artifacts', 'fragments', 'outputs'):
            e[key] = [remap(r, t) if r['partition'] == partition else r for r in e[key]]
        e['partition_manifest'] = remap(e['partition_manifest'], t)
    return f


def test_ids_to(org):
    def f(e):
        return {r[k]: r[k].replace('ORG-S1', org) for key, k in (('artifacts', 'synthetic_id'),
                                                                 ('fragments', 'fragment_id'), ('outputs', 'output_id'))
                for r in e[key] if r['partition'] == 'test'}
    return f


TO_APP = transplant({'APP-00013': 'APP-00015'})
TO_VAC = transplant({'VAC-0004': 'VAC-0010', 'APP-00013': 'APP-00053', 'APP-00014': 'APP-00054',
                     'CRI-0016': 'CRI-0045', 'CRI-0017': 'CRI-0046'})
TO_ORG = transplant({'ORG-S1': 'ORG-S2', 'VAC-0004': 'VAC-0002', 'APP-00013': 'APP-00003', 'APP-00014': 'APP-00004',
                     'CRI-0016': 'CRI-0007', 'CRI-0017': 'CRI-0008', 'ANT36-S1-02': 'ANT36-S2-02'},
                    ids=test_ids_to('ORG-S2'))
TO_SCENARIO = transplant({'SC36-02': 'SC36-03'})
TO_FAMILY = transplant({'TF36-BB': 'TF36-CC', 'TPL36-BB-01': 'TPL36-CC-01', 'TPL36-BB-02': 'TPL36-CC-02',
                        'TPL36-BB-03': 'TPL36-CC-03'})


def upref(e, source, ref):
    """Referencia upstream con el hash del manifiesto F34 (el que ya cita el ejemplo para esa tabla)."""
    sha = next(r['sha256'] for a in e['artifacts'] for r in a['provenance']['upstream_refs'] if r['source'] == F34 + source)
    return {'source': F34 + source, 'ref': ref, 'sha256': sha}


def add_ref(n, source, ref, sha=None):
    def f(e):
        r = upref(e, source, ref) if sha is None else {'source': source, 'ref': ref, 'sha256': sha}
        art(e, n)['provenance']['upstream_refs'].append(r)
    return f


# ---------------------------------------------------------------- evidencia de equipo en memoria

def path(fg):
    return f'{EV}{fg}.json'


def approvals(date=RDATE):
    return [{'member': m, 'vote': 'APRUEBA', 'date': date} for m in v.MEMBERS]


def common(fg, n=1):
    return {'schema': 'f36sbx-team-evidence/v2', 'criterion_id': fg, 'gate_id': 'F36-SBX-GATE',
            'gate_version': '3', 'candidate_commit': CAND, 'record_id': f'F36SBX-{fg}-{n:03d}',
            'recorded_at': RDATE}


REPORT_PROSE = (
    '# Informe de auditoría independiente de F36-SBX (prueba en memoria)\n\n'
    '## Alcance\n\n'
    'Revisión ficticia, solo en memoria, del paquete F36-SBX: contrato de evidencia, ejemplo de conformidad, '
    'validador, batería de pruebas y documentos de diseño. No existe fuera de esta prueba y no aprueba nada real.\n\n'
    '## Hallazgos\n\n'
    'Los hallazgos abiertos y su severidad constan únicamente en el bloque canónico de metadatos de este informe; '
    'el texto humano no los repite, para no crear una segunda fuente.\n\n'
    '## Conclusión\n\n'
    'La conclusión normativa es la del bloque canónico. Este texto solo describe el alcance de la revisión.\n')
ADR_PROSE = (
    '# ADR-006 · Excepción sintética de F36-SBX (prueba en memoria)\n\n'
    '## Contexto\n\n'
    'Documento ficticio, solo en memoria, que ejercita las comprobaciones de FG-12 del gate sucesor de F36-SBX. '
    'Se relaciona con ADR-005 como una excepción acotada al sandbox sintético y no existe fuera de esta prueba.\n\n'
    '## Decisión\n\n'
    'La decisión normativa, su relación con ADR-005, su alcance, las EI que cubre y la decisión sobre EI-09 constan '
    'únicamente en el bloque canónico de metadatos.\n\n'
    '## Consecuencias\n\n'
    'Ninguna fuera de la prueba: no habilita datos reales, producción ni capacidades bloqueadas.\n')


def doc_bytes(prose, info, meta, extra=''):
    return (prose + f'\n```{info}\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n```\n' + extra).encode('utf-8')


def report_meta(d):
    return {'metadata_schema': 'f36sbx-audit-report/v1', 'gate_id': 'F36-SBX-GATE', 'gate_version': '3',
            'criterion_id': 'FG-02', 'candidate_commit': d['candidate_commit'], 'auditor': copy.deepcopy(d['auditor']),
            'verdict': d['verdict'], 'findings_open': copy.deepcopy(d['findings_open']), 'report_date': RDATE}


def adr_meta(d):
    adr = d['successor_adr']
    return {'metadata_schema': 'f36sbx-adr/v1', 'gate_id': 'F36-SBX-GATE', 'gate_version': '3', 'base_commit': v.BASE,
            'adr_id': adr['id'], 'status': adr['status'], 'relation_to_adr005': adr['relation_to_adr005'],
            'scope': adr['scope'], 'covered_ei': list(d['covered_ei']), 'ei09_decision': d['ei09_decision'],
            'decided_on': CDATE}


def set_report(meta_fn=None, prose=None, extra='', raw=None):
    """Reescribe el informe de FG-02 desde el registro vigente (metadatos, texto o bytes) y actualiza su SHA-256."""
    def f(docs, ctx):
        meta = report_meta(docs['FG-02'])
        if meta_fn:
            meta_fn(meta)
        data = raw if raw is not None else doc_bytes(REPORT_PROSE if prose is None else prose,
                                                     'f36sbx-audit-metadata', meta, extra)
        ctx['evidence'][REPORT] = data
        docs['FG-02']['audit_report']['sha256'] = v.sha256(data)
    return f


def blob(data, mode='100644', kind='blob'):
    """Resolución de git_blob tal como la devuelve el validador para un blob del commit candidato."""
    return {'mode': mode, 'type': kind, 'object': v.git_blob_id(data), 'data': data}


def set_adr(meta_fn=None, prose=None, extra='', raw=None):
    """Reescribe el ADR sucesor desde el registro FG-12 vigente, como blob del commit candidato, y actualiza su SHA-256.

    En memoria, el ADR solo existe como resolución de candidate_commit:path; la resolución con Git real la prueba
    test_f36sbx_git.py."""
    def f(docs, ctx):
        meta = adr_meta(docs['FG-12'])
        if meta_fn:
            meta_fn(meta)
        data = raw if raw is not None else doc_bytes(ADR_PROSE if prose is None else prose,
                                                     'f36sbx-adr-metadata', meta, extra)
        ctx['adr_blobs'][(docs['FG-12']['candidate_commit'], ADR_PATH)] = blob(data)
        docs['FG-12']['successor_adr']['sha256'] = v.sha256(data)
    return f


def both(*fns):
    def f(docs, ctx):
        for fn in fns:
            fn(docs, ctx)
    return f


def evidence_docs(auth):
    deps = [] if not set(auth) & {'EI-10', 'EI-11', 'EI-12'} else [{
        'name': 'dependencia-ficticia-f36', 'version': '==1.0.0',
        'purpose': 'Dependencia ficticia de prueba en memoria para EI-10; no existe ni se instala.',
        'license': 'MIT', 'source': 'pypi', 'source_url': 'https://pypi.org/project/dependencia-ficticia-f36/',
        'supply_chain_review': {'osv_checked_on': RDATE, 'open_vulnerabilities': 0, 'artifact_sha256': 'e' * 64,
                                'reviewed_by': v.MEMBERS[2]},
        'related_ei': sorted(set(auth) & {'EI-10', 'EI-11', 'EI-12'}), 'approval_status': 'APROBADA'}]
    cond_c = sorted(set(auth) & set(v.SCOPE_C_CONDITIONAL))
    return {
        'FG-02': {**common('FG-02'),
                  'auditor': {'name': 'Sesión de auditoría independiente AF3 (prueba en memoria)',
                              'kind': 'sesion_de_auditoria_independiente', 'independent_of_candidate': True},
                  'audit_report': {'path': REPORT, 'sha256': None},
                  'verdict': 'APROBADO_CON_OBSERVACIONES',
                  'findings_open': {'blocker': 0, 'high': 0, 'medium_requiring_fix': 0, 'medium_accepted': 1,
                                    'low': 2}},
        'FG-03': {**common('FG-03'), 'decision': 'AUTORIZA_INICIO_F37_SBX', 'authorized_ei': list(auth),
                  'numbering_f36_m01': 'CONFIRMADA', 'approvals': approvals(), 'quorum': '3/3'},
        'FG-10': {**common('FG-10'), 'new_dependencies': bool(deps), 'dependencies': deps,
                  'approvals': approvals(), 'quorum': '3/3'},
        'FG-12': {**common('FG-12'),
                  'successor_adr': None if not cond_c else {
                      'id': 'ADR-006', 'path': ADR_PATH, 'sha256': None, 'status': 'APROBADO',
                      'relation_to_adr005': 'EXCEPCION_SANDBOX_SINTETICA_ADR005_6_4',
                      'scope': 'ALCANCE_C_SOLO_SINTETICO'},
                  'covered_ei': cond_c,
                  'ei09_decision': 'CABE_EN_ALCANCE_B' if 'EI-09' in auth else 'SIN_DECISION',
                  'approvals': approvals(), 'quorum': '3/3'},
    }


def status_doc(doc, statuses):
    """El documento del gate con la columna Estado de las filas FG indicadas cambiada (cambio de registro)."""
    lines = doc.split('\n')
    for i, ln in enumerate(lines):
        for fg, st in statuses.items():
            if ln.startswith(f'| {fg} |'):
                lines[i] = ln.rsplit('| PENDIENTE |', 1)[0] + f'| {st} |'
    return '\n'.join(lines)


def build(auth=AUTH, mutate=None, team=('FG-02', 'FG-03', 'FG-10', 'FG-12')):
    """Contexto completo de evidencia válida en memoria; mutate(docs, ctx) lo altera antes de serializar."""
    schema = v.strict_json(BASE['texts'][SCH])
    state = json.loads(BASE['texts'][S])
    state['candidate_commit'] = CAND
    state['f37_authorized_ei'] = list(auth)
    for c in state['criteria']:
        if c['id'] in team:
            c['status'], c['evidence'] = 'CUMPLE', path(c['id'])
    docs = evidence_docs(auth)
    # El ADR forma parte del commit candidato (no cambia después); el informe se registra en gate/evidencia/.
    ctx = {'state': state, 'schema': schema, 'evidence': {}, 'adr_blobs': {}, 'classes': v.EXPECTED_CLASSES,
           'gate_doc': status_doc(BASE['texts'][G], {fg: 'CUMPLE' for fg in team}),
           'facts': {CAND: {'commit': True, 'from_base': True, 'ancestor': True, 'date': CDATE,
                            'gate_doc': BASE['texts'][G],
                            'changed': sorted([S, G, REPORT, *(path(fg) for fg in team)])}}}
    set_report()(docs, ctx)
    if docs['FG-12']['successor_adr'] is not None:
        set_adr()(docs, ctx)
    if mutate:
        mutate(docs, ctx)
    for fg, doc in docs.items():
        if fg in team and doc is not None:
            ctx['evidence'][path(fg)] = doc if isinstance(doc, bytes) else \
                json.dumps(doc, ensure_ascii=False).encode('utf-8')
    return ctx


def decide(ctx):
    return v.evaluate_gate(ctx['state'], v.EXPECTED_CLASSES, lambda fg: v.team_evidence_errors(fg, ctx))


def ev_case(cid, desc, fg, mutate, needle, auth=AUTH):
    """La evidencia mutada de fg debe ser inválida por el motivo indicado, y el gate no puede quedar SUPERADO."""
    try:
        ctx = build(auth, mutate)
        errs = v.team_evidence_errors(fg, ctx)
        gate = decide(ctx)
    except NOT_APPLICABLE as e:
        ok(False, cid, desc, f'mutación no aplicable: {e.__class__.__name__}: {e}')
        return
    hit = [e for e in errs if needle in e]
    ok(hit and gate == 'NO SUPERADO', cid, desc,
       f'{fg} inválida («{needle}») y gate {gate}' if hit else f'esperaba «{needle}»; errores {errs[:3]}; gate {gate}')


def register(team=('FG-02',), mutate=None, statuses=None):
    """Mutación del repositorio: registra en memoria la evidencia de los criterios indicados, como lo haría el equipo."""
    def f(s):
        ctx = build(AUTH, mutate, team)
        state = json.loads(s['texts'][S])
        state['candidate_commit'] = CAND
        for c in state['criteria']:
            if c['id'] in team:
                c['status'], c['evidence'] = 'CUMPLE', path(c['id'])
        if 'FG-03' in team:
            state['f37_authorized_ei'] = list(AUTH)
        s['texts'][S] = json.dumps(state, ensure_ascii=False, indent=2)
        s['texts'][G] = status_doc(s['texts'][G], statuses or {fg: 'CUMPLE' for fg in team})
        s['evidence'] = {p: b for p, b in ctx['evidence'].items() if p == REPORT or p in {path(fg) for fg in team}}
        s['adr_blobs'] = dict(ctx['adr_blobs'])
        s['facts'] = ctx['facts']
        s['changed'] = set(s['changed']) | set(s['evidence'])
    return f


def af2(cid, desc, fg, mutate, needle):
    """Prueba obligatoria AF2 sobre la evidencia: inválida en memoria con el motivo indicado, gate NO SUPERADO y,
    registrada en el repositorio, el validador completo FALLA en GATE con el mismo motivo."""
    team = ('FG-02',) if fg == 'FG-02' else ('FG-02', 'FG-03', fg)
    try:
        ctx = build(AUTH, mutate)
        errs = v.team_evidence_errors(fg, ctx)
        gate = decide(ctx)
        snap = copy.deepcopy(BASE)
        register(team, mutate)(snap)
        repo = [m for n, m in failing(snap) if n == 'GATE' and needle in m]
    except NOT_APPLICABLE as e:
        ok(False, cid, desc, f'mutación no aplicable: {e.__class__.__name__}: {e}')
        return
    hit = [e for e in errs if needle in e]
    ok(hit and gate == 'NO SUPERADO' and repo, cid, desc,
       f'{fg} inválida («{needle}»), gate {gate} y validador FALLA' if hit and repo else
       f'esperaba «{needle}»; errores {errs[:3]}; gate {gate}; validador {"falla" if repo else "no falla"}')


# ---------------------------------------------------------------- batería

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    # T00 · control: el repositorio real pasa y el gate da NO SUPERADO.
    res, gate = v.run(copy.deepcopy(BASE))
    fails = [f'{n}: {m}' for n, ok_, m in res if not ok_]
    ok(not fails and gate == 'NO SUPERADO', 'T00', 'control: repositorio real sin fallas y gate NO SUPERADO',
       f'gate {gate}' if not fails else f'fallas reales: {fails}')
    ex = v.strict_json(BASE['texts'][EX])
    ok(v.bundle_errors(CONTRACT, ex, BASE['upstream']) == [], 'T01',
       'control: el ejemplo de conformidad cumple REL-01..REL-14', 'sin errores')
    again = copy.deepcopy(ex)
    reseal(again)
    ok(again == ex, 'T01b', 'control: el ejemplo ya está sellado (volver a sellarlo no cambia ningún byte)', '')
    # Robustez: con un contrato roto, la validación de registros falla cerrado y nunca lanza una excepción.
    broken = copy.deepcopy(CONTRACT)
    broken['upstream_files'].pop(F34 + 'applications.csv')
    for cid, desc, c_ in (('T02', 'contrato sin la tabla de postulaciones', broken), ('T03', 'contrato vacío', {}),
                          ('T04', 'contrato que no es un objeto', None)):
        try:
            errs = v.bundle_errors(c_, ex, BASE['upstream'])
            ok(bool(errs), cid, f'registros con {desc}: errores, sin excepción', errs[:1])
        except Exception as e:  # noqa: BLE001
            ok(False, cid, f'registros con {desc}: errores, sin excepción', f'excepción {e.__class__.__name__}')

    nbh = '‑'
    # ---------------- gobierno y afirmaciones de estado
    case('M01', 'G0 real aprobada en CLAUDE.md', sub('CLAUDE.md', '- G0 real = NO APROBADA', '- G0 real = APROBADA'), 'SEM')
    case('M02', 'falta F37-SBX = BLOQUEADA en README.md', sub('README.md', '- F37-SBX = BLOQUEADA\n', ''), 'GOV')
    case('M03', 'F37-SBX habilitada en PROGRESS', sub('docs/PROGRESS.md', '- F37-SBX = BLOQUEADA', '- F37-SBX = HABILITADA'), 'SEM')
    case('M04', 'alcance C habilitado en ACADEMIC_BASELINE',
         sub('docs/academico/ACADEMIC_BASELINE.md', '- Alcance C = BLOQUEADO', '- Alcance C = HABILITADO'), 'SEM')
    case('M05', 'datos reales permitidos en README.md',
         sub('README.md', '- Datos reales = PROHIBIDOS', '- Datos reales = PERMITIDOS'), 'SEM')
    case('M06', 'se pierde F35-SBX = CERRADA Y CONGELADA', sub('CLAUDE.md', '- F35-SBX = CERRADA Y CONGELADA\n', ''), 'GOV')
    case('M07', 'G0-12 declarado dos veces con valores distintos',
         sub('docs/PROGRESS.md', '- G0-12 = PENDIENTE EXTERNO\n', '- G0-12 = PENDIENTE EXTERNO\n- G0-12 = CUMPLIDO\n'), 'GOV')
    case('M08', 'ADR-005 aprobado en el README del paquete', sub(PR, 'ADR-005 = PROPUESTA', 'ADR-005 = APROBADA'), 'SEM')
    case('M09', 'gate declarado SUPERADO en su documento',
         sub(G, 'F36-SBX-GATE = NO SUPERADO.', 'F36-SBX-GATE = SUPERADO.'), 'SEM')
    case('M10', 'F36-SBX cerrada con guion no separable',
         sub(CH, '**F36-SBX = EN DISEÑO**', f'**F36{nbh}SBX = CERRADA**'), 'SEM')
    case('M11', 'F37-SBX habilitada escondida con negritas', sub(CH, '**F37-SBX = BLOQUEADA**', '**F37-SBX** = HABILITADA'), 'SEM')
    case('M12', 'F37-SBX habilitada con dos puntos', sub(PR, '**F37-SBX = BLOQUEADA.**', '**F37-SBX: HABILITADA.**'), 'SEM')
    case('M13', 'línea desconocida en el estado vigente (F37-SBX-A = HABILITADA)',
         sub('CLAUDE.md', '- F37-SBX = BLOQUEADA\n', '- F37-SBX = BLOQUEADA\n- F37-SBX-A = HABILITADA\n'), 'GOV', 'desconocidas')
    case('M14', 'afirmación «ADR-006 = APROBADO» en el paquete',
         sub(PR, '- RF-23 sigue', '- ADR-006 = APROBADO.\n- RF-23 sigue'), 'SEM', 'ADR-006')
    case('M15', 'afirmación «Alcance C sintético = AUTORIZADO» en el paquete',
         sub(CE, '## 1. Principios', '## 1. Principios\n\nAlcance C sintético = AUTORIZADO.'), 'SEM', 'Alcance C')
    case('M16', 'afirmación «G0-SBX = APROBADA SIN RESTRICCIONES» en el gate',
         sub(G, '## 1. Nombre y propósito', '## 1. Nombre y propósito\n\nG0-SBX = APROBADA SIN RESTRICCIONES.'), 'SEM', 'G0-SBX')
    case('M17', 'F37-SBX-B habilitada con dos puntos en la matriz',
         sub(M, '## Resumen', 'F37-SBX-B: HABILITADA.\n\n## Resumen'), 'SEM', 'F37-SBX-B')
    case('M18', 'tabla de estados del charter con G0 real aprobada',
         sub(CH, '| G0 real | NO APROBADA |', '| G0 real | APROBADA |'), 'SEM', 'charter')
    case('M19', 'CLAUDE.md con otros integrantes', sub('CLAUDE.md', 'Peña Arroyo Anthony y', 'Peña Arroyo Antonio y'), 'GOV',
         'integrantes')
    # ---------------- matriz de capacidades
    case('M20', 'EI-19 (scoring y ranking) pasa a ALLOWED',
         sub(M, '| **BLOCKED** | — | CAP-15, CAP-16, CAP-17 |', '| **ALLOWED** | B | CAP-15, CAP-16, CAP-17 |'), 'CAP')
    case('M21', 'EI-10 (embeddings) pasa a ALLOWED',
         sub(M, '| **CONDITIONAL** | C | CAP-09, CAP-20 |', '| **ALLOWED** | C | CAP-09, CAP-20 |'), 'CAP')
    case('M22', 'OCR pasa a CONDITIONAL', sub(M, '| OCR | **BLOCKED** | C |', '| OCR | **CONDITIONAL** | C |'), 'CAP')
    case('M23', 'desaparece EI-20 (inferencias prohibidas)', drop_line(M, '| EI-20 |'), 'CAP')
    case('M24', 'el resumen no coincide con las filas', sub(M, 'EI-06, EI-07 |', 'EI-06 |'), 'CAP')
    case('M25', 'EI-01 cita una CAP inexistente', sub(M, '| CAP-04, CAP-06 |', '| CAP-99, CAP-06 |'), 'CAP')
    case('M26', 'EI-04 ALLOWED cita CAP-10 BLOQUEADA', sub(M, '| CAP-13 |', '| CAP-13, CAP-10 |'), 'CAP')
    case('M27', 'capacidad ALLOWED que usa embeddings', sub(M, 'Búsqueda léxica exacta', 'Búsqueda con embeddings'), 'CAP')
    case('M28', 'EI-08 de alcance C pasa a ALLOWED',
         sub(M, '| **CONDITIONAL** | C | CAP-07 | Es extracción', '| **ALLOWED** | C | CAP-07 | Es extracción'), 'CAP')
    for i, word in enumerate(('OCR', 'LLM', 'PDF', 'DOCX', 'NER', 'audio', 'Whisper')):
        case(f'M29{chr(97 + i)}', f'capacidad ALLOWED que nombra {word}',
             sub(M, 'Búsqueda léxica exacta, por subcadena', f'{word} y búsqueda léxica exacta, por subcadena'), 'CAP',
             'capacidad ALLOWED que nombra')
    case('M30', 'EI-09 reclasificada como ALLOWED, con el resumen a juego',
         chain(sub(M, '| **CONDITIONAL** | B | CAP-08 |', '| **ALLOWED** | B | CAP-08 |'),
               sub(M, '| ALLOWED | EI-01, EI-02, EI-03, EI-04, EI-05, EI-06, EI-07 |',
                   '| ALLOWED | EI-01, EI-02, EI-03, EI-04, EI-05, EI-06, EI-07, EI-09 |'),
               sub(M, '| CONDITIONAL | EI-08, EI-09, EI-10,', '| CONDITIONAL | EI-08, EI-10,')),
         'CAP', 'reclasificadas')
    # ---------------- threat model y plan
    case('M31', 'desaparece TEI-11 (abstención)', drop_line(T, '| TEI-11 |'), 'THR')
    case('M32', 'TEI-02 sin comportamiento fail-closed', sub(T, '| Un manifiesto con texto libre es inválido |', '| — |'), 'THR')
    case('M33', 'se pierde el tema de inyección', sub(T, 'Prompt injection o document injection', 'Instrucciones incrustadas'), 'THR')
    case('M34', 'el plan inventa un resultado', sub(R, '**No hay resultados.**', 'Resultados preliminares: Recall@5 = 0,81.'), 'EVA')
    case('M35', 'desaparece M-07', drop_line(R, '| M-07 |'), 'EVA')
    case('M36', 'una EI BLOCKED recibe métrica', sub(R, '| M-11 | Toda salida |', '| M-11 | Toda salida, EI-13 |'), 'EVA')
    # ---------------- alcance Git, runtime, F35-SBX, dependencias, PII y enlaces
    case('M37', 'cambio en app/', add_changed('app/Models/Vacancy.php'), 'FRZ')
    case('M38', 'cambio en F35-SBX congelada', add_changed('docs/academico/evidencia-sbx/README.md'), 'FRZ')
    case('M39', 'cambio en composer.json', add_changed('composer.json'), 'FRZ')
    case('M40', 'cambio en las dependencias de ml-service', add_changed('ml-service/pyproject.toml'), 'FRZ')
    case('M41', 'cambio en la deuda técnica', add_changed('docs/academico/TECHNICAL_DEBT.md'), 'FRZ')
    case('M42', 'cambio en el gate congelado de F35-SBX',
         add_changed('docs/academico/tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py'), 'FRZ')
    case('M43', 'cambio en una migración', add_changed('database/migrations/2026_10_26_000000_x.php'), 'FRZ')
    case('M44', 'cambio en el dataset F34', add_changed(F34 + 'applications.csv'), 'FRZ')
    case('M45', 'rama no admitida', setkey('branch', 'feature/otra'), 'FRZ')
    case('M46', 'la base no es ancestro', setkey('base_ok', False), 'FRZ')
    case('M47', 'estado Git desconocido', setkey('changed', None), 'FRZ')
    case('M48', 'el validador importa torch', append_tool('\nimport torch\n'), 'DEP')
    case('M49', 'el validador importa requests', append_tool('\nimport requests\n'), 'DEP')
    case('M50', 'un script nuevo importa sentence_transformers',
         add_tool(v.TOOLS + '/localizador.py', 'from sentence_transformers import SentenceTransformer\n'), 'DEP')
    case('M51', 'el validador contiene un byte de retroceso (0x08)', append_tool(f'\nX = r"{chr(8)}ocr{chr(8)}"\n'),
         'DEP', '0x08')
    case('M52', 'correo en el contrato', sub(CE, '## 1. Principios', '## 1. Principios\n\nContacto: persona' + '@' + 'colegio.pe'), 'PII')
    case('M53', 'número de DNI en el charter', sub(CH, '## 3. Problema', 'DNI ' + '4' + '1234567' + '\n\n## 3. Problema'), 'PII')
    case('M54', 'enlace roto', sub(PR, '](F36SBX_Charter.md)', '](F36SBX_Charter_x.md)'), 'LNK')
    case('M55', 'ancla rota', sub(M, '(F36SBX_Charter.md#7-revocación)', '(F36SBX_Charter.md#7-revocacion)'), 'LNK')
    case('M56', 'falta el threat model', lambda s: s['texts'].update({T: None}), 'STR')
    case('M57', 'falta el ejemplo de conformidad', lambda s: s['texts'].update({EX: None}), 'STR')
    case('M58', 'el README no enlaza el esquema de evidencia',
         sub(PR, '](gate/f36sbx_team_evidence_schema.json)', '](gate/esquema.json)'), 'STR')
    case('M59', 'falta el documento de corrección AF2', lambda s: s['texts'].update({v.PKG + '/F36SBX_Correccion_AF2.md': None}),
         'STR', 'F36SBX_Correccion_AF2.md')

    # ---------------- contrato cerrado v3 (C)
    c_cases = [
        ('C01', 'source_type admite real', lambda d: d['source_type_allowed'].append('real'), 'source_type_allowed'),
        ('C02', 'tipo de artefacto desconocido (audio_recording)',
         lambda d: (d['enums']['artifact_type'].append('audio_recording'), d['artifact_types'].update(
             audio_recording={'stage': 'A', 'content_fields': ['text_synthetic'], 'list_items': {},
                              'text_paths': ['text_synthetic'], 'fragmentable': True})), 'tipos de artefacto'),
        ('C03', 'author_kind admite system', lambda d: d['enums']['author_kind'].append('system'), 'author_kind'),
        ('C04', 'partition admite train', lambda d: d['enums']['partition'].append('train'), 'partition'),
        ('C05', 'partición con valor desconocido (holdout)', lambda d: d['enums']['partition'].append('holdout'), 'partition'),
        ('C06', 'se admite train', lambda d: d['splits'].update(train_allowed=True), 'garantías de partición'),
        ('C07', 'test sin sellar antes de ejecutar', lambda d: d['splits'].update(test_sealed_before_any_run=False),
         'garantías de partición'),
        ('C08', 'umbrales ajustados en test', lambda d: d['splits'].update(thresholds_fit_on='test'), 'garantías de partición'),
        ('C09', 'partición sin familia de plantilla', lambda d: d['splits'].update(group_by=['vacancy_token']),
         'garantías de partición'),
        ('C10', 'embargo temporal eliminado', lambda d: d['splits'].update(temporal_embargo='ninguno'), 'garantías de partición'),
        ('C11', 'provenance sin upstream_refs ni seed',
         lambda d: d['provenance_fields'].update(artifact=['generator_id', 'generator_version', 'template_id',
                                                           'template_family', 'content_hash']), 'provenance'),
        ('C12', 'fragmento sin artifact_id', lambda d: d['fragment_fields'].remove('artifact_id'), 'campos del fragmento'),
        ('C13', 'output con campo score', lambda d: d['output_fields'].append('score'), 'campos del output'),
        ('C14', 'propiedad adicional peligrosa en un tipo (allow_real_data)',
         lambda d: d['artifact_types']['cv_document'].update(allow_real_data=True), 'claves distintas'),
        ('C15', 'campo sinónimo de puntaje (candidate_score)',
         lambda d: (d['content_field_types'].update(candidate_score='text'),
                    d['artifact_types']['cv_document']['content_fields'].append('candidate_score')), 'tokens prohibidos'),
        ('C16', 'transcripción sin revisar (review_status = cruda)', lambda d: d['enums'].update(review_status=['cruda']),
         'review_status'),
        ('C17', 'observation_kind con una inferencia', lambda d: d['enums']['observation_kind'].append('inferencia_emocional'),
         'observation_kind'),
        ('C18', 'fuentes prohibidas recortadas', lambda d: d.update(forbidden_upstream_sources=['docs/academico/g0-evidence']),
         'fuentes prohibidas'),
        ('C19', 'estado del contrato cambiado', lambda d: d.update(status='APROBADO'), 'identidad'),
        ('C20', 'sin la tabla de postulaciones', lambda d: d['upstream_files'].pop(F34 + 'applications.csv'),
         'archivos upstream'),
        ('C21', 'el generador admite LLM', lambda d: d['generator_policy'].update(llm_allowed=True), 'generador'),
        ('C22', 'prefijo de marcador cambiado', lambda d: d['synthetic_markers'].update(synthetic_id_prefix='SBXE-'), 'marcadores'),
        ('C23', 'patrón de artefacto abierto', lambda d: d['identifier_patterns'].update(artifact_id='^.*$'), 'artifact_id'),
        ('C24', 'formato mp4 admitido', lambda d: d['enums']['format'].append('mp4'), 'format'),
        ('C25', 'output_ei incluye una EI BLOCKED', lambda d: d['output_ei'].append('EI-19'), 'output_ei'),
        ('C26', 'marcador de grupo en una observación',
         lambda d: d['artifact_types']['human_observation']['content_fields'].append('grupo_sintetico'), 'marcador de grupo'),
        ('C27', 'fuente upstream extra (g0-evidence)',
         lambda d: d['upstream_files'].update({'docs/academico/g0-evidence/x.csv': {
             'key': 'id', 'scope': 'tenant', 'context': {}, 'cardinality': 'any_same_vacancy'}}), 'archivos upstream'),
        ('C28', 'manifiesto de particiones sin sello',
         lambda d: d['partition_fields'].update(test=['artifacts']), 'manifiesto de particiones'),
        ('C29', 'relaciones incompletas', lambda d: d['relations'].pop('REL-13'), 'relaciones'),
        # v3 (AF2): tenants, fuentes globales, cadena de hashes, configuración y cobertura.
        ('C33', 'fuente global admitida (competencies.csv)',
         lambda d: d['global_upstream_sources'].append(F34 + 'competencies.csv'), 'fuentes globales'),
        ('C34', 'annotator_token deja de estar ligado al tenant', lambda d: d['tenant_bound_tokens'].remove('annotator_token'),
         'tokens ligados al tenant'),
        ('C35', 'patrón de autor sin grupo de tenant', lambda d: d['identifier_patterns'].update(author_token='^EV-S[1-3]-[0-9]{2}$'),
         'patrones de autor y anotador'),
        ('C36', 'cardinalidad libre para la postulación',
         lambda d: d['upstream_files'][F34 + 'applications.csv'].update(cardinality='any_same_vacancy'), 'archivos upstream'),
        ('C37', 'contexto de la postulación sin la dimensión postulación',
         lambda d: d['upstream_files'][F34 + 'applications.csv']['context'].pop('application'), 'archivos upstream'),
        ('C38', 'cobertura mínima de un escenario', lambda d: d['example_coverage'].update(min_scenarios=1), 'cobertura mínima'),
        ('C39', 'identificador del ejemplo abierto', lambda d: d.update(example_id_value=None), 'identificador cerrado'),
        ('C40', 'etiqueta de record_hash cambiada', lambda d: d['hash_scheme']['record_hash'].update(tag='otra'),
         'esquema de hashes'),
        ('C41', 'sello v1 sin registros', lambda d: d['splits'].update(seal_algorithm='f36sbx-test-seal-sha256-v1'),
         'garantías de partición'),
        ('C42', 'sobre sin record_hash', lambda d: d['artifact_envelope_fields'].remove('record_hash'), 'sobre del artefacto'),
        ('C43', 'output sin fragment_ref_hashes', lambda d: d['output_fields'].remove('fragment_ref_hashes'), 'campos del output'),
        ('C44', 'fragmento sin artifact_record_hash', lambda d: d['fragment_fields'].remove('artifact_record_hash'),
         'campos del fragmento'),
        ('C45', 'configuración del método con temperature', lambda d: d['method_config_fields'].append('temperature'),
         'configuración del método'),
        ('C46', 'top_k sin límite razonable', lambda d: d.update(top_k_range=[1, 1000]), 'configuración del método'),
        ('C47', 'normalización semántica admitida', lambda d: d['enums']['normalization'].append('semantica'), 'normalization'),
        ('C48', 'identificador global personal', lambda d: d['global_identifiers']['question_id'].update(personal=True),
         'identificadores globales'),
        ('C49', 'identificador de contenido sin clase (evaluator_ref)',
         lambda d: (d['content_field_types'].update(evaluator_ref='pattern:author_token'),
                    d['artifact_types']['human_observation']['content_fields'].append('evaluator_ref')), 'sin clase única'),
        ('C50', 'identificador con dos clases (criterion_id interno y upstream)',
         lambda d: d['internal_references'].update(criterion_id='fragments'), 'sin clase única'),
        ('C51', 'identificador global nuevo sin documentar (vacancy_ref)',
         lambda d: d['global_identifiers'].update(vacancy_ref={'scope': 'global', 'personal': False,
                                                               'resolved_upstream': False, 'semantics': ''}),
         'identificadores globales'),
    ]
    for cid, desc, fn, needle in c_cases:
        case(cid, desc, jmut(C, fn), 'CTR', needle)
    case('C30', 'cambio sin efecto semántico detectado por el hash (texto de una relación)',
         jmut(C, lambda d: d['relations'].update({'REL-01': 'texto distinto'})), 'CTR', 'idéntico a la versión cerrada')
    case('C31', 'clave nueva de primer nivel', jmut(C, lambda d: d.update(real_data_allowed=False)), 'CTR',
         'claves de primer nivel distintas')
    case('C32', 'clave duplicada en el contrato',
         sub(C, '"contract_version": "3",', '"contract_version": "3",\n  "contract_version": "4",'), 'CTR', 'JSON inválido')

    # ---------------- relaciones del ejemplo de conformidad (R): hashes válidos y test resellado, salvo indicación
    def r_set(n, **kw):
        return lambda e: art(e, n).update(kw)

    def r_content(n, fn):
        return lambda e: fn(art(e, n)['content'])

    rel('R01', 'source_type desconocido', r_set(1, source_type='real'), 'source_type desconocido')
    rel('R02', 'artifact_type desconocido', r_set(1, artifact_type='audio_recording'), 'artifact_type desconocido')
    rel('R03', 'author_kind desconocido', r_content(3, lambda c: c.update(author_kind='system')), 'author_kind con valor desconocido')
    rel('R04', 'partición train', r_set(2, partition='train'), "partición 'train' prohibida")
    rel('R05', 'partición desconocida', r_set(2, partition='holdout'), "partición desconocida 'holdout'")
    rel('R06', 'provenance ausente', lambda e: art(e, 1).pop('provenance'), 'provenance ausente')
    rel('R07', 'provenance mal formada: semilla de texto', lambda e: art(e, 1)['provenance'].update(seed='3601'), 'semilla')
    rel('R08', 'provenance mal formada: upstream_refs no es lista',
        lambda e: art(e, 1)['provenance'].update(upstream_refs='VAC-0001'), 'sin referencias upstream')
    rel('R09', 'fragmento hacia un artefacto inexistente', lambda e: frg(e, 1).update(artifact_id='SBX36-ORG-S1-ART-0099'),
        'referencia un artefacto inexistente')
    rel('R10', 'output hacia un fragmento inexistente',
        lambda e: out(e, 1).update(fragment_refs=['SBX36-ORG-S1-FRG-0001', 'SBX36-ORG-S1-FRG-0099']),
        'referencia un fragmento inexistente')
    rel('R11', 'mezcla de organización en un fragmento', lambda e: frg(e, 1).update(synthetic_organization_id='ORG-S2'),
        'mezcla de synthetic_organization_id')
    rel('R12', 'mezcla de escenario en la vacante', r_set(2, scenario_id='SC36-02'),
        'vacante mezclada entre organizaciones o escenarios')
    rel('R13', 'mezcla de vacante y postulación en un output',
        lambda e: out(e, 1).update(fragment_refs=['SBX36-ORG-S1-FRG-0001', 'SBX36-ORG-S1-FRG-0004']),
        'mezcla de application_token')
    rel('R14', 'postulación de otra vacante en F34', r_set(1, application_token='APP-00013'),
        'la postulación F34 es de otra vacante')
    rel('R15', 'propiedad adicional peligrosa en un output', lambda e: out(e, 1).update(score=0.9), "sobran ['score']")
    rel('R16', 'propiedad adicional en el sobre de un artefacto', r_set(1, real_data=False), "sobran ['real_data']")
    rel('R17', 'test deja de estar sellado',
        lambda e: e['partition_manifest']['partitions']['test'].update(sealed=False), 'no está sellada')
    rel('R18', 'artefacto de test cambiado sin volver a sellar',
        r_content(6, lambda c: c.update(title_synthetic='[SINTÉTICO] Constancia sintética distinta.')), SEAL, 'rehash')
    rel('R19', 'umbrales ajustados con un output de test',
        lambda e: e['partition_manifest']['thresholds']['tuning_outputs'].append('SBX36-ORG-S1-OUT-0002'),
        'test no puede ajustar')
    rel('R20', 'test usado para ajuste', lambda e: e['partition_manifest'].update(test_used_for_tuning=True),
        'test_used_for_tuning')
    rel('R21', 'manifiesto con partición train',
        lambda e: e['partition_manifest']['partitions'].update(train={'artifacts': []}), 'partición prohibida')
    rel('R22', 'familia de plantilla en dos particiones',
        lambda e: (art(e, 6).update(template_family='TF36-AA'),
                   art(e, 6)['provenance'].update(template_family='TF36-AA', template_id='TPL36-AA-09')),
        'familia de plantilla en varias particiones')
    rel('R23', 'vacante en dos particiones',
        lambda e: (art(e, 5).update(partition='test'),
                   e['partition_manifest']['partitions']['dev']['artifacts'].remove('SBX36-ORG-S1-ART-0005'),
                   e['partition_manifest']['partitions']['test']['artifacts'].append('SBX36-ORG-S1-ART-0005')),
        'vacante en varias particiones')
    rel('R24', 'sin la referencia upstream a la postulación',
        lambda e: art(e, 1)['provenance'].update(upstream_refs=art(e, 1)['provenance']['upstream_refs'][:1]),
        'debe citar exactamente su application_token')
    rel('R25', 'referencia upstream con hash falso',
        lambda e: art(e, 1)['provenance']['upstream_refs'][0].update(sha256='0' * 64), 'distinto del manifiesto F34')
    rel('R26', 'referencia upstream a un id inexistente',
        lambda e: art(e, 1)['provenance']['upstream_refs'][1].update(ref='APP-99999'), "'APP-99999' no existe")
    rel('R27', 'content_hash que no corresponde al contenido',
        r_content(3, lambda c: c.update(text_synthetic='[SINTÉTICO] Otro texto.')), 'content_hash incorrecto', 'raw')
    rel('R28', 'fragment_hash incorrecto', lambda e: frg(e, 2).update(fragment_hash='0' * 64), 'fragment_hash incorrecto', 'raw')
    rel('R29', 'offsets fuera del texto', lambda e: frg(e, 3).update(char_end=10 ** 6), 'offsets fuera del texto')
    rel('R30', 'text_path inválido', lambda e: frg(e, 1).update(text_path='sections/9/text_synthetic'), 'text_path')
    rel('R31', 'abstención con fragmentos', lambda e: out(e, 1).update(abstained=True), 'abstención no coincide')
    rel('R32', 'output con una EI BLOCKED', lambda e: out(e, 1).update(ei='EI-19'), '(BLOCKED)')
    rel('R33', 'input_manifest_hash incorrecto', lambda e: out(e, 2).update(input_manifest_hash='0' * 64),
        'input_manifest_hash incorrecto', 'raw')
    rel('R34', 'texto sin [SINTÉTICO]', r_content(1, lambda c: c['sections'][0].update(text_synthetic='Licenciatura real.')),
        'sin el prefijo [SINTÉTICO]')
    rel('R35', 'texto con un correo', r_content(3, lambda c: c.update(
        text_synthetic='[SINTÉTICO] Contacto ' + 'evaluadora' + '@' + 'colegio.pe')), 'patrón de PII')
    rel('R36', 'texto no NFC', r_content(3, lambda c: c.update(
        text_synthetic='[SINTÉTICO] La persona evaluadora sintética anota un ejemplo.')), 'no está en NFC')
    rel('R36b', 'texto sin prefijo por descomposición Unicode', r_content(3, lambda c: c.update(
        text_synthetic='[SINTÉTICO] La persona evaluadora sintética anota un ejemplo.')), 'sin el prefijo')
    rel('R37', 'documento renderizado desde algo que no es un CV', r_content(8, lambda c: c.update(
        rendered_from='SBX36-ORG-S1-ART-0002')), 'REL-10')
    rel('R38', 'variante contrafactual de otra vacante', r_content(7, lambda c: c.update(
        variant_of='SBX36-ORG-S1-ART-0001')), 'REL-09')
    rel('R39', 'anotación con un criterio de otra vacante', r_content(4, lambda c: c.update(criterion_id='CRI-0016')),
        'REL-08')
    rel('R40', 'identificadores repetidos', lambda e: frg(e, 2).update(fragment_id='SBX36-ORG-S1-FRG-0001'), 'REL-03')
    rel('R41', 'identificador de otra organización', r_set(1, synthetic_id='SBX36-ORG-S2-ART-0001'), 'REL-03')
    rel('R42', 'transcripción sin revisar', r_content(2, lambda c: c.update(review_status='cruda')),
        'review_status con valor desconocido')
    rel('R43', 'campo de contenido adicional', r_content(1, lambda c: c.update(score=1)), 'contenido distinto del tipo')
    rel('R44', 'artefacto fuera del manifiesto',
        lambda e: e['partition_manifest']['partitions']['dev']['artifacts'].remove('SBX36-ORG-S1-ART-0003'),
        'fuera del manifiesto')
    rel('R45', 'etapa distinta de la del tipo', r_set(1, stage='B'), 'etapa')
    rel('R46', 'plantilla de otra familia', lambda e: art(e, 1)['provenance'].update(template_id='TPL36-BB-01'),
        'no pertenece a la familia')
    rel('R47', 'ejemplo que no se declara ejemplo', lambda e: e.update(example_only=False), 'solo ejemplo')
    rel('R48', 'method_config con top_k 0', lambda e: out(e, 1)['method_config'].update(top_k=0), 'method_config fuera')
    rel('R49', 'method_config con un campo adicional (temperature)',
        lambda e: out(e, 1)['method_config'].update(temperature=0.7), 'method_config fuera')
    rel('R50', 'method_config con normalización desconocida',
        lambda e: out(e, 1)['method_config'].update(normalization='semantica'), 'method_config fuera')
    rel('R51', 'method_config con top_k booleano', lambda e: out(e, 1)['method_config'].update(top_k=True),
        'method_config fuera')
    rel('R52', 'nota del ejemplo con un carácter invisible',
        lambda e: e.update(note=e['note'].replace('Ejemplo', 'Ejem​plo', 1)), 'debe declararse solo ejemplo')
    rel('R53', 'texto con un carácter invisible (U+200B)', r_content(3, lambda c: c.update(
        text_synthetic='[SINTÉTICO] La persona evaluadora​ sintética anota un ejemplo.')), 'caracteres invisibles')
    rel('R54', 'fragment_ref_hashes en otro orden', lambda e: out(e, 1).update(
        fragment_ref_hashes=list(reversed(out(e, 1)['fragment_ref_hashes']))), 'fragment_ref_hashes no coincide', 'raw')
    rel('R55', 'abstained como entero', lambda e: out(e, 2).update(abstained=1), 'abstained debe ser booleano')
    rel('R56', 'familia de plantilla con un carácter invisible',
        lambda e: (art(e, 1).update(template_family='TF36-AA​'),
                   art(e, 1)['provenance'].update(template_family='TF36-AA​')), 'template_family fuera de patrón')
    rel('R57', 'provenance con un campo adicional (llm_generated)',
        lambda e: art(e, 1)['provenance'].update(llm_generated=False), 'provenance distinta del contrato')
    rel('R58', 'fragmento con un campo adicional', lambda e: frg(e, 1).update(confidence=0.9), 'campos distintos del contrato')
    rel('R59', 'manifiesto con un campo adicional', lambda e: e['partition_manifest'].update(notes='x'),
        'manifiesto de particiones ausente o con campos distintos')
    rel('R60', 'lista de secciones vacía', r_content(1, lambda c: c.update(sections=[])), 'debe ser una lista no vacía')
    rel('R61', 'upstream_refs vacía', lambda e: art(e, 1)['provenance'].update(upstream_refs=[]), 'sin referencias upstream')
    rel('R62', 'fragment_refs con repetidos',
        lambda e: out(e, 1).update(fragment_refs=['SBX36-ORG-S1-FRG-0001', 'SBX36-ORG-S1-FRG-0001']),
        'identificadores únicos')
    rel('R63', 'artefacto repetido en la lista de una partición',
        lambda e: e['partition_manifest']['partitions']['dev']['artifacts'].append('SBX36-ORG-S1-ART-0001'),
        'lista de artefactos inválida')
    rel('R64', 'enumerado desconocido en una anotación', r_content(4, lambda c: c.update(relevance='parcial')),
        'relevance con valor desconocido')

    # ---------------- cadena de hashes y sello de test (H)
    rel('H01', 'semilla cambiada sin recalcular record_hash', lambda e: art(e, 1)['provenance'].update(seed=3611),
        'record_hash incorrecto', 'raw')
    rel('H02', 'artefacto recalculado sin actualizar su fragmento',
        lambda e: (art(e, 1)['provenance'].update(seed=3611), rehash(art(e, 1))),
        'artifact_record_hash no es el record_hash vigente', 'raw')
    rel('H03', 'record_hash sustituido por el content_hash (esquema anterior)',
        lambda e: art(e, 2).update(record_hash=art(e, 2)['content_hash']), 'record_hash incorrecto', 'raw')
    rel('H04', 'sello declarado con el algoritmo v1',
        lambda e: e['partition_manifest']['partitions']['test'].update(seal_algorithm='f36sbx-test-seal-sha256-v1'),
        'algoritmo de sello')
    rel('H05', 'sello calculado con el esquema v1 (pares [id, content_hash])',
        lambda e: e['partition_manifest']['partitions']['test'].update(seal_sha256=v.sha256(v.canonical(sorted(
            [a['synthetic_id'], a['content_hash']] for a in e['artifacts'] if a['partition'] == 'test')))), SEAL, 'raw')
    rel('H06', 'output de ajuste cambiado sin recalcular su output_hash',
        lambda e: out(e, 1)['method_config'].update(top_k=7), 'output_hash incorrecto', 'raw')
    rel('H07', 'fragmento de test sin recalcular text_hash',
        lambda e: frg(e, 4).update(char_start=frg(e, 4)['char_start'] + 1), 'text_hash incorrecto', 'raw')
    seal_only('H08', 'artefacto de dev usado por el ajuste, cambiado sin resellar (lo fija el output de ajuste)',
              r_content(3, lambda c: c.update(text_synthetic=c['text_synthetic'] + ' Sin cambios de contexto.')))
    seal_only('H09', 'output de ajuste recalculado sin resellar', lambda e: out(e, 1)['method_config'].update(top_k=7))
    seal_only('H10', 'oro de dev cambiado sin resellar (tuning_gold)', r_content(4, lambda c: c.update(overlap_stratum='alto')))
    seal_only('H11', 'output de test recalculado sin resellar (test_outputs)',
              lambda e: out(e, 3).update(query_criterion_id='CRI-0018'))
    rel('H12', 'fragmento de test sin outputs, recalculado sin resellar (test_fragments)',
        lambda e: (e.update(outputs=[o for o in e['outputs'] if o['partition'] == 'dev']), reseal(e),
                   frg(e, 4).update(char_start=frg(e, 4)['char_start'] + 1), rehash_all(e)), SEAL, 'raw')

    # ---------------- aislamiento entre tenants y procedencia (X): hashes válidos y test resellado
    rel('X01', 'criterio del contenido sin su referencia upstream', r_content(4, lambda c: c.update(criterion_id='CRI-0005')),
        'falta la referencia upstream de content.criterion_id')
    rel('X02', 'referencia upstream a la vacante repetida',
        lambda e: art(e, 1)['provenance']['upstream_refs'].append(dict(art(e, 1)['provenance']['upstream_refs'][0])),
        'repetida o inválida')
    rel('X03', 'referencia a otra postulación de la misma vacante', add_ref(1, 'applications.csv', 'APP-00002'),
        'de otra postulación')
    rel('X04', 'referencia upstream con un campo adicional',
        lambda e: art(e, 1)['provenance']['upstream_refs'][0].update(note='libre'), 'referencia upstream mal formada')
    rel('X05', 'referencia upstream a una URL', add_ref(1, 'https://example.invalid/x.csv', 'X', '0' * 64),
        'global no admitida')
    rel('X06', 'referencia upstream a g0-evidence', add_ref(1, 'docs/academico/g0-evidence/x.csv', 'X', '0' * 64),
        'global no admitida')
    rel('X07', 'autor con un tenant inexistente (EV-S4-01)', r_content(3, lambda c: c.update(author_token='EV-S4-01')),
        'author_token fuera de patrón')
    rel('X08', 'anotador de ORG-S2 en una anotación de ORG-S1', r_content(4, lambda c: c.update(annotator_token='ANT36-S2-01')),
        "annotator_token 'ANT36-S2-01' es de ORG-S2")
    rel('X09', 'segunda vacante propia citada (otra vacante de ORG-S1)', add_ref(1, 'vacancies.csv', 'VAC-0010'),
        'de otra vacante')
    rel('X10', 'trasplante de un solo artefacto de test a ORG-S2 sin sus referencias',
        lambda e: art(e, 6).update(synthetic_organization_id='ORG-S2', synthetic_id='SBX36-ORG-S2-ART-0006'), 'REL-04')

    # ---------------- pruebas obligatorias de la auditoría AF2 (AF2-01..AF2-33)
    fg02 = lambda fn: lambda docs, ctx: fn(docs['FG-02'])  # noqa: E731
    fg03 = lambda fn: lambda docs, ctx: fn(docs['FG-03'])  # noqa: E731
    fg10 = lambda fn: lambda docs, ctx: fn(docs['FG-10'])  # noqa: E731
    fg12 = lambda fn: lambda docs, ctx: fn(docs['FG-12'])  # noqa: E731

    # AF2-M01 · coherencia entre el registro y el informe o el ADR.
    af2('AF2-01', 'FG-02 APROBADO en el registro y NO_APROBADO en el informe', 'FG-02',
        set_report(lambda m: m.update(verdict='NO_APROBADO_PARA_INTEGRACION')), 'no coincide con el del registro')
    af2('AF2-02', 'FG-02 con HIGH = 0 en el registro y HIGH = 2 en el informe', 'FG-02',
        set_report(lambda m: m['findings_open'].update(high=2)), 'recuentos de hallazgos del informe no coinciden')
    af2('AF2-03', 'informe que solo contiene el SHA del candidato', 'FG-02', set_report(raw=CAND.encode('ascii')),
        'exactamente un bloque')
    af2('AF2-04', 'auditor «...» (registro e informe coherentes)', 'FG-02',
        both(fg02(lambda d: d['auditor'].update(name='...')), set_report()), 'identidad del auditor')
    af2('AF2-05', 'auditor de caracteres invisibles U+200B (registro e informe coherentes)', 'FG-02',
        both(fg02(lambda d: d['auditor'].update(name='​​​')), set_report()), 'caracteres invisibles')
    af2('AF2-06', 'metadatos del informe con otro commit', 'FG-02',
        set_report(lambda m: m.update(candidate_commit=OTHER)), 'el commit de los metadatos no es el candidato')
    af2('AF2-07', 'veredicto aprobatorio distinto en el informe', 'FG-02',
        set_report(lambda m: m.update(verdict='APROBADO_PARA_INTEGRACION')), 'no coincide con el del registro')
    af2('AF2-08', 'recuentos distintos en el informe (LOW)', 'FG-02',
        set_report(lambda m: m['findings_open'].update(low=3)), 'recuentos de hallazgos del informe no coinciden')
    af2('AF2-09', 'FG-12 APROBADO en el registro y PROPUESTO en el ADR', 'FG-12',
        set_adr(lambda m: m.update(status='PROPUESTO')), 'status de los metadatos')
    af2('AF2-10', 'metadatos del ADR de otro contexto (otro gate)', 'FG-12',
        set_adr(lambda m: m.update(gate_id='G0-SBX')), 'otro contexto')
    af2('AF2-11', 'covered_ei distinta en el ADR', 'FG-12',
        set_adr(lambda m: m.update(covered_ei=['EI-10', 'EI-11'])), 'covered_ei de los metadatos')
    af2('AF2-12', 'decisión sobre EI-09 distinta en el ADR', 'FG-12',
        set_adr(lambda m: m.update(ei09_decision='NO_CABE_EN_ALCANCE_B')), 'ei09_decision de los metadatos')

    # AF2-M02 · cadena de hashes y sello de test: cambios coherentes, registros recalculados y sin resellar.
    seal_only('AF2-13', 'application_token de test trasplantado (APP-00013 → APP-00015) sin resellar', TO_APP)
    seal_only('AF2-14', 'vacante de test trasplantada (VAC-0004 → VAC-0010, con sus postulaciones y criterios) sin resellar',
              TO_VAC)
    seal_only('AF2-15', 'organización de test trasplantada (ORG-S1 → ORG-S2, con identificadores y referencias) sin resellar',
              TO_ORG)
    seal_only('AF2-16', 'escenario de test cambiado (SC36-02 → SC36-03) sin resellar', TO_SCENARIO)
    seal_only('AF2-17', 'familia de plantilla de test cambiada (TF36-BB → TF36-CC) sin resellar', TO_FAMILY)
    seal_only('AF2-18', 'generator_version de un artefacto de test cambiada sin resellar',
              lambda e: art(e, 6)['provenance'].update(generator_version='0.2.0'))
    seal_only('AF2-19', 'semilla de un artefacto de test cambiada sin resellar',
              lambda e: art(e, 6)['provenance'].update(seed=3616))
    seal_only('AF2-20', 'provenance upstream de test cambiada (criterio legítimo añadido) sin resellar',
              add_ref(6, 'criteria.csv', 'CRI-0018'))
    rel('AF2-21', 'contexto de un fragmento de test cambiado sin recalcular su hash',
        lambda e: frg(e, 4).update(application_token='APP-00015'), 'fragment_hash incorrecto', 'raw')
    rel('AF2-22', 'contexto de un output de test cambiado sin recalcular su hash',
        lambda e: out(e, 3).update(application_token='APP-00015'), 'output_hash incorrecto', 'raw')
    rel('AF2-23', 'fragmento de entrada cambiado y recalculado, sin recalcular el output',
        lambda e: (frg(e, 4).update(char_end=frg(e, 4)['char_end'] - 1), rehash_fragment(e, 4)),
        'fragment_ref_hashes no coincide', 'raw')
    seal_only('AF2-24', 'oro de test (anotación de relevancia) cambiado sin resellar',
              r_content(9, lambda c: c.update(relevance='no_relevante')))
    resealed('P-01', 'control positivo resellado: el trasplante de postulación, con test vuelto a sellar, es conforme', TO_APP)
    resealed('P-02', 'control positivo resellado: el trasplante coherente a ORG-S2, con test vuelto a sellar, es conforme',
             TO_ORG)
    resealed('P-03', 'control positivo resellado: la semilla de test cambiada y resellada es conforme',
             lambda e: art(e, 6)['provenance'].update(seed=3616))
    resealed('P-04', 'control positivo resellado: el oro de test cambiado y resellado es conforme',
             r_content(9, lambda c: c.update(relevance='no_relevante')))

    # AF2-M03 · aislamiento entre tenants: autores y referencias upstream contextuales.
    rel('AF2-25', 'autor de ORG-S2 (EV-S2-01) en una observación de ORG-S1', r_content(3, lambda c: c.update(author_token='EV-S2-01')),
        "author_token 'EV-S2-01' es de ORG-S2")
    rel('AF2-26', 'referencia upstream adicional a una postulación de ORG-S2 (APP-00003)', add_ref(1, 'applications.csv', 'APP-00003'),
        "'APP-00003' de otra organización")
    rel('AF2-27', 'referencia upstream a un criterio de otra vacante de la misma organización (CRI-0045)',
        add_ref(1, 'criteria.csv', 'CRI-0045'), "'CRI-0045' de otra vacante")
    rel('AF2-28', 'referencia upstream a un criterio de otro escenario (CRI-0016, SC36-02)', add_ref(1, 'criteria.csv', 'CRI-0016'),
        "'CRI-0016' de otro escenario")
    rel('AF2-29', 'referencia upstream desconocida (CRI-9999)', add_ref(1, 'criteria.csv', 'CRI-9999'), "'CRI-9999' no existe")
    rel('AF2-30', 'fuente global no admitida (competencies.csv, con su hash real del manifiesto F34)',
        add_ref(1, F34 + 'competencies.csv', 'CMP-S1-01', COMPETENCIES_SHA), 'global no admitida')
    resealed('P-05', 'control positivo: referencia legítima a otro criterio de la misma vacante (CRI-0005)',
             add_ref(1, 'criteria.csv', 'CRI-0005'))
    resealed('P-06', 'control positivo: anotador y autor de su propia organización (ANT36-S1-09, EV-S1-07)',
             lambda e: (art(e, 4)['content'].update(annotator_token='ANT36-S1-09'),
                        art(e, 3)['content'].update(author_token='EV-S1-07')))

    # AF2-L01 · identificador del ejemplo cerrado y cobertura mínima.
    rel('AF2-31', 'example_id como objeto', lambda e: e.update(example_id={'id': 'f36sbx-contract-example'}),
        'example_id debe ser exactamente')
    rel('AF2-32', 'example_id con candidate_score', lambda e: e.update(example_id={'candidate_score': 1}),
        'example_id debe ser exactamente')
    rel('AF2-33', 'ejemplo vacío',
        lambda e: (e.update(artifacts=[], fragments=[], outputs=[]),
                   e['partition_manifest']['partitions']['dev'].update(artifacts=[]),
                   e['partition_manifest']['partitions']['test'].update(artifacts=[]),
                   e['partition_manifest']['thresholds'].update(tuning_outputs=[])), 'REL-14 cobertura mínima')
    rel('L01', 'ejemplo sin test', lambda e: (
        e.update(artifacts=[a for a in e['artifacts'] if a['partition'] == 'dev'],
                 fragments=[f for f in e['fragments'] if f['partition'] == 'dev'],
                 outputs=[o for o in e['outputs'] if o['partition'] == 'dev']),
        e['partition_manifest']['partitions']['test'].update(artifacts=[])), 'test sin artefactos')
    rel('L02', 'ejemplo sin abstención', lambda e: (
        e.update(outputs=[o for o in e['outputs'] if not o['abstained']])), 'sin outputs con abstención')
    rel('L03', 'ejemplo sin un tipo de artefacto (rendered_document)', lambda e: (
        e.update(artifacts=[a for a in e['artifacts'] if a['artifact_type'] != 'rendered_document']),
        e['partition_manifest']['partitions']['dev']['artifacts'].remove('SBX36-ORG-S1-ART-0008')), 'faltan tipos de artefacto')
    rel('L04', 'ejemplo con un solo escenario', TO_SCENARIO_ONE, 'menos de dos escenarios')
    rel('L05', 'ejemplo sin oro en test', lambda e: (
        e.update(artifacts=[a for a in e['artifacts'] if a['synthetic_id'] != 'SBX36-ORG-S1-ART-0009']),
        e['partition_manifest']['partitions']['test']['artifacts'].remove('SBX36-ORG-S1-ART-0009')), 'test sin anotaciones de oro')

    # ---------------- semántica de la evidencia de equipo (E)
    full = build()
    ok(all(v.team_evidence_errors(fg, full) == [] for fg in v.FG_TEAM) and decide(full) == 'SUPERADO', 'E00',
       'control positivo en memoria: las cuatro evidencias, el informe y el ADR son válidos y el gate da SUPERADO',
       str({fg: v.team_evidence_errors(fg, full)[:2] for fg in v.FG_TEAM}))
    no_c = build(['EI-01', 'EI-07'], team=('FG-02', 'FG-03', 'FG-10'))
    no_c['state']['criteria'][11]['status'] = 'NO APLICA'
    ok(decide(no_c) == 'SUPERADO', 'E00b', 'control positivo: solo EI ALLOWED, FG-10 sin dependencias nuevas y FG-12 NO APLICA',
       decide(no_c))

    def both_auth(lst):
        def f(docs, ctx):
            docs['FG-03']['authorized_ei'] = lst
            ctx['state']['f37_authorized_ei'] = lst
        return f

    # Los quince casos obligatorios del gate.
    ev_case('E01', 'FG-02 vacía', 'FG-02', lambda docs, ctx: docs.update({'FG-02': b''}), 'está vacío')
    ev_case('E02', 'FG-02 de otro commit', 'FG-02', fg02(lambda d: d.update(candidate_commit=OTHER)),
            'distinto del candidato declarado')
    ev_case('E03', 'auditoría con veredicto rechazado', 'FG-02', fg02(lambda d: d.update(verdict='NO_APROBADO_PARA_INTEGRACION')),
            'no aprueba el candidato')
    ev_case('E04', 'auditoría con BLOCKER abierto', 'FG-02', fg02(lambda d: d['findings_open'].update(blocker=1)),
            'blocker abiertos = 1')
    ev_case('E05', 'auditoría con HIGH abierto', 'FG-02', fg02(lambda d: d['findings_open'].update(high=2)), 'high abiertos = 2')
    ev_case('E06', 'auditoría con un MEDIUM que requiere corrección', 'FG-02',
            fg02(lambda d: d['findings_open'].update(medium_requiring_fix=1)), 'medium_requiring_fix abiertos = 1')
    ev_case('E07', 'FG-03 con 2/3', 'FG-03', fg03(lambda d: d['approvals'].pop()), 'quórum incompleto 2/3')
    ev_case('E08', 'FG-03 con identidad duplicada', 'FG-03',
            fg03(lambda d: d['approvals'].__setitem__(2, dict(d['approvals'][0]))), 'integrante duplicado')
    ev_case('E09', 'FG-03 con una EI BLOCKED', 'FG-03', both_auth(['EI-01', 'EI-19']), 'EI-19 es BLOCKED')
    ev_case('E10', 'FG-03 con una EI desconocida', 'FG-03', both_auth(['EI-01', 'EI-99']), 'EI desconocida')
    ev_case('E11', 'FG-03 sin lista explícita de EI', 'FG-03', fg03(lambda d: d.pop('authorized_ei')), 'campos distintos')
    ev_case('E11b', 'FG-03 con lista vacía', 'FG-03', both_auth([]), 'falta la lista explícita')
    ev_case('E12', 'FG-10 con estructura desconocida', 'FG-10', fg10(lambda d: d['dependencies'][0].pop('license')),
            'estructura desconocida o incompleta')
    ev_case('E12b', 'FG-10 con una clave adicional', 'FG-10', fg10(lambda d: d.update(notes='libre')), 'campos distintos')
    ev_case('E13', 'FG-12 con el ADR PROPUESTO', 'FG-12', fg12(lambda d: d['successor_adr'].update(status='PROPUESTO')),
            'está PROPUESTO')
    ev_case('E14', 'FG-12 de otro contexto (otro gate)', 'FG-12', fg12(lambda d: d.update(gate_id='G0-SBX')),
            'otro contexto')
    ev_case('E14b', 'FG-12 con un ADR que no cita F36-SBX ni ADR-005', 'FG-12',
            set_adr(prose=ADR_PROSE.replace('F36-SBX', 'otro proyecto').replace('ADR-005', 'otra decisión')),
            'otro contexto')
    ev_case('E15', 'FG-12 que intenta autorizar una EI BLOCKED', 'FG-12',
            fg12(lambda d: d.update(covered_ei=['EI-10', 'EI-19'])), 'EI-19, que es BLOCKED')
    # Refuerzos de las mismas invariantes.
    ev_case('E16', 'FG-02 con JSON de claves duplicadas', 'FG-02',
            lambda docs, ctx: docs.update({'FG-02': b'{"schema": "a", "schema": "b"}'}), 'no es JSON')
    ev_case('E17', 'FG-02 con informe de otro hash', 'FG-02', fg02(lambda d: d['audit_report'].update(sha256='0' * 64)),
            'SHA-256 es distinto')
    ev_case('E18', 'FG-02 con informe sin bloque canónico', 'FG-02',
            set_report(raw=REPORT_PROSE.encode('utf-8')), 'exactamente un bloque')
    ev_case('E19', 'FG-02 con auditor genérico (N/A)', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='N/A')), set_report()), 'identidad del auditor')
    ev_case('E20', 'FG-02 con auditor no independiente', 'FG-02',
            fg02(lambda d: d['auditor'].update(independent_of_candidate=False)), 'independiente')
    ev_case('E21', 'FG-02 con un recuento booleano', 'FG-02', fg02(lambda d: d['findings_open'].update(blocker=False)),
            'entero no negativo')
    ev_case('E22', 'FG-02 de un commit con cambios posteriores del paquete', 'FG-02',
            lambda docs, ctx: ctx['facts'][CAND].update(changed=ctx['facts'][CAND]['changed'] + [v.MATRIX]),
            'el paquete cambió después')
    ev_case('E23', 'FG-02 de un commit que no es ancestro de HEAD', 'FG-02',
            lambda docs, ctx: ctx['facts'][CAND].update(ancestor=False), 'no es ancestro de HEAD')
    ev_case('E24', 'FG-02 con recorded_at anterior al candidato', 'FG-02', fg02(lambda d: d.update(recorded_at='2026-10-01')),
            'anterior al commit candidato')
    ev_case('E25', 'FG-03 con un voto RECHAZA', 'FG-03', fg03(lambda d: d['approvals'][1].update(vote='RECHAZA')),
            'no aprueba')
    ev_case('E26', 'FG-03 con una identidad casi igual (homoglifo)', 'FG-03',
            fg03(lambda d: d['approvals'][1].update(member='Peña Arroyo Anthony'.replace('a', 'а', 1))),
            'integrante no reconocido')
    ev_case('E27', 'FG-03 con decisión NO_AUTORIZA', 'FG-03', fg03(lambda d: d.update(decision='NO_AUTORIZA')), 'no autoriza')
    ev_case('E28', 'FG-03 sin confirmar F36-M01', 'FG-03', fg03(lambda d: d.update(numbering_f36_m01='NO_CONFIRMADA')),
            'no confirmada')
    ev_case('E29', 'FG-03 distinta del estado del gate', 'FG-03', fg03(lambda d: d.update(authorized_ei=['EI-01'])),
            'distinta de f37_authorized_ei')
    ev_case('E30', 'FG-10 con versión en rango', 'FG-10', fg10(lambda d: d['dependencies'][0].update(version='>=1.0')),
            'versión no fijada')
    ev_case('E31', 'FG-10 con vulnerabilidades abiertas', 'FG-10',
            fg10(lambda d: d['dependencies'][0]['supply_chain_review'].update(open_vulnerabilities=1)), 'vulnerabilidades')
    ev_case('E32', 'FG-10 con licencia no admitida', 'FG-10', fg10(lambda d: d['dependencies'][0].update(license='GPL-3.0')),
            'licencia')
    ev_case('E33', 'FG-10 con dependencia solo PROPUESTA', 'FG-10',
            fg10(lambda d: d['dependencies'][0].update(approval_status='PROPUESTA')), 'no APROBADA')
    ev_case('E34', 'FG-10 sin dependencias con EI-10 autorizada', 'FG-10',
            fg10(lambda d: d.update(new_dependencies=False, dependencies=[])), 'requieren dependencias')
    ev_case('E35', 'FG-10 que relaciona una EI sin dependencias', 'FG-10',
            fg10(lambda d: d['dependencies'][0].update(related_ei=['EI-07'])), 'no justifica')
    ev_case('E36', 'FG-10 con URL de origen falsa', 'FG-10',
            fg10(lambda d: d['dependencies'][0].update(source_url='https://example.invalid/x')), 'URL de origen')
    ev_case('E37', 'FG-10 con FG-03 inválida', 'FG-10', fg03(lambda d: d.update(decision='NO_AUTORIZA')),
            'requiere una autorización FG-03 válida')
    ev_case('E38', 'FG-12 con id de ADR reservado', 'FG-12', fg12(lambda d: d['successor_adr'].update(id='ADR-005')),
            'reservado')
    ev_case('E39', 'FG-12 con un ADR sin resolver en el commit candidato', 'FG-12', lambda docs, ctx: ctx['adr_blobs'].clear(),
            'no es un blob regular versionado en el commit candidato')
    ev_case('E40', 'FG-12 sin decisión sobre EI-09 autorizada', 'FG-12',
            both(fg12(lambda d: d.update(ei09_decision='SIN_DECISION')), set_adr()), 'EI-09 autorizada sin la decisión')
    ev_case('E41', 'FG-12 que no cubre EI-10', 'FG-12', both(fg12(lambda d: d.update(covered_ei=[])), set_adr()), 'no cubre')
    ev_case('E42', 'FG-12 sin ADR con EI-10 autorizada', 'FG-12', fg12(lambda d: d.update(successor_adr=None, covered_ei=[])),
            'exigen un ADR sucesor')
    ev_case('E43', 'FG-12 que cubre una EI ALLOWED', 'FG-12', fg12(lambda d: d.update(covered_ei=['EI-10', 'EI-07'])),
            'no es una EI CONDITIONAL de alcance C')
    ev_case('E44', 'FG-12 con fecha de aprobación posterior al registro', 'FG-12',
            fg12(lambda d: d['approvals'][0].update(date='2026-12-31')), 'fecha de aprobación')
    ev_case('E45', 'record_id de otro criterio', 'FG-03', fg03(lambda d: d.update(record_id='F36SBX-FG-02-001')), 'record_id')
    ev_case('E46', 'evidencia citada por el estado en otra ruta', 'FG-02',
            lambda docs, ctx: ctx['state']['criteria'][1].update(evidence=EV + 'otra.json'), 'debe citar exactamente')
    ev_case('E47', 'FG-12 con el ADR fuera de docs/', 'FG-12', fg12(lambda d: d['successor_adr'].update(path='storage/adr.md')),
            'ruta del ADR inválida')
    ev_case('E48', 'FG-12 con el ADR cambiado después del candidato', 'FG-12',
            lambda docs, ctx: ctx['facts'][CAND].update(changed=ctx['facts'][CAND]['changed'] + [ADR_PATH]),
            'el paquete cambió después')

    # ---------------- informe y ADR: bloque canónico, texto exterior y coherencia (D)
    block = 'f36sbx-audit-metadata'
    ev_case('D01', 'informe con dos bloques canónicos', 'FG-02',
            lambda docs, ctx: set_report(extra=f'\n```{block}\n{{}}\n```\n')(docs, ctx), 'exactamente un bloque')
    ev_case('D02', 'informe con otro bloque f36sbx ambiguo', 'FG-02',
            set_report(extra='\n```F36SBX-audit-metadata-v0\n{}\n```\n'), 'otro bloque f36sbx ambiguo')
    ev_case('D03', 'bloque del informe con claves duplicadas', 'FG-02',
            set_report(raw=(REPORT_PROSE + f'\n```{block}\n{{"verdict": "a", "verdict": "b"}}\n```\n').encode('utf-8')),
            'no es un objeto JSON válido')
    ev_case('D04', 'bloque del informe con un campo adicional', 'FG-02', set_report(lambda m: m.update(notes='x')),
            'metadatos con campos distintos')
    ev_case('D05', 'bloque del informe sin report_date', 'FG-02', set_report(lambda m: m.pop('report_date')),
            'metadatos con campos distintos')
    ev_case('D06', 'informe sin la sección de hallazgos', 'FG-02',
            set_report(prose=REPORT_PROSE.replace('## Hallazgos', '## Notas')), 'faltan las secciones')
    ev_case('D07', 'informe no NFC', 'FG-02', set_report(prose=REPORT_PROSE.replace('Revisión', 'Revisión')),
            'no está en NFC')
    ev_case('D08', 'informe con un carácter de control bidireccional (U+202E)', 'FG-02',
            set_report(prose=REPORT_PROSE.replace('Revisión', 'Revisión‮')), 'caracteres invisibles')
    ev_case('D09', 'report_date anterior al candidato', 'FG-02', set_report(lambda m: m.update(report_date='2026-10-01')),
            'report_date inválida')
    ev_case('D10', 'informe de otro criterio (FG-03)', 'FG-02', set_report(lambda m: m.update(criterion_id='FG-03')),
            'otro contexto')
    ev_case('D11', 'informe de otra versión del gate', 'FG-02', set_report(lambda m: m.update(gate_version='2')),
            'otro contexto')
    ev_case('D12', 'informe que no es UTF-8', 'FG-02',
            set_report(raw=REPORT_PROSE.encode('latin-1', 'replace')), 'no es UTF-8')
    ev_case('D13', 'JSON señuelo fuera del bloque con recuentos', 'FG-02',
            set_report(extra='\n```json\n{"high": 2}\n```\n'), 'aserciones de veredicto o de recuentos')
    ev_case('D14', 'auditor distinto en el informe', 'FG-02',
            set_report(lambda m: m['auditor'].update(name='Otra sesión de auditoría ficticia')),
            'el auditor de los metadatos no coincide')
    ev_case('D15', 'tipo de auditor distinto en el informe', 'FG-02',
            set_report(lambda m: m['auditor'].update(kind='docente')), 'el auditor de los metadatos no coincide')
    ev_case('D16', 'recuento booleano en el informe (false por 0)', 'FG-02',
            set_report(lambda m: m['findings_open'].update(high=False)), 'recuentos de hallazgos del informe no coinciden')
    ev_case('D17', 'veredicto canónico fuera del bloque', 'FG-02',
            set_report(prose=REPORT_PROSE + '\nNO_APROBADO_PARA_INTEGRACION\n'), 'aparece fuera del bloque')
    ev_case('D18', 'recuento afirmado fuera del bloque (HIGH = 2)', 'FG-02',
            set_report(prose=REPORT_PROSE + '\nHIGH = 2\n'), 'aserciones de veredicto o de recuentos')
    ev_case('D19', 'veredicto afirmado fuera del bloque (Veredicto: …)', 'FG-02',
            set_report(prose=REPORT_PROSE + '\nVeredicto: rechazado.\n'), 'aserciones de veredicto o de recuentos')
    ev_case('D20', 'informe con solo el bloque', 'FG-02', set_report(prose=''), 'contenido humano insuficiente')
    ev_case('D21', 'identidad del auditor con U+200B dentro del nombre', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='Revisora​Externa Ficticia')), set_report()),
            'caracteres invisibles')
    ev_case('D22', 'identidad del auditor con espacios al inicio', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name=' Revisora Externa Ficticia')), set_report()), 'espacios')
    ev_case('D23', 'identidad del auditor genérica («Auditor independiente»)', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='Auditor independiente')), set_report()), 'marcador de posición')
    ev_case('D24', 'identidad del auditor no NFC', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='Sesión de auditoría ficticia')), set_report()), 'no está en NFC')
    ev_case('D25', 'bloque del informe que es una lista', 'FG-02',
            set_report(raw=(REPORT_PROSE + f'\n```{block}\n[]\n```\n').encode('utf-8')), 'no es un objeto JSON válido')
    ev_case('D26', 'ADR con dos bloques canónicos', 'FG-12',
            set_adr(extra='\n```f36sbx-adr-metadata\n{}\n```\n'), 'exactamente un bloque')
    ev_case('D27', 'ADR sin su id en el título', 'FG-12', set_adr(prose=ADR_PROSE.replace('# ADR-006 ·', '# ADR sucesor ·')),
            'el título no nombra su id')
    ev_case('D28', 'ADR con el estado afirmado fuera del bloque', 'FG-12',
            set_adr(prose=ADR_PROSE + '\nEstado: vigente.\n'), 'aserción o token de estado')
    ev_case('D29', 'ADR con un token de estado fuera del bloque', 'FG-12',
            set_adr(prose=ADR_PROSE + '\nEste ADR queda PROPUESTO hasta nueva revisión.\n'), 'aserción o token de estado')
    ev_case('D30', 'ADR con la relación canónica fuera del bloque', 'FG-12',
            set_adr(prose=ADR_PROSE + '\nEXCEPCION_SANDBOX_SINTETICA_ADR005_6_4\n'), 'token canónico')
    ev_case('D31', 'ADR decidido después del commit candidato que lo contiene', 'FG-12',
            set_adr(lambda m: m.update(decided_on='2026-10-27')), 'decided_on')
    ev_case('D32', 'id del ADR distinto en sus metadatos', 'FG-12', set_adr(lambda m: m.update(adr_id='ADR-007')),
            'adr_id de los metadatos')
    ev_case('D33', 'alcance distinto en los metadatos del ADR', 'FG-12', set_adr(lambda m: m.update(scope='ALCANCE_C_REAL')),
            'scope de los metadatos')
    ev_case('D34', 'covered_ei repetida en los metadatos del ADR', 'FG-12',
            set_adr(lambda m: m.update(covered_ei=['EI-10', 'EI-10'])), 'covered_ei de los metadatos')
    ev_case('D35', 'metadatos del ADR con otra base', 'FG-12', set_adr(lambda m: m.update(base_commit=OTHER)), 'otro contexto')
    ev_case('D36', 'metadatos del ADR de otra versión del gate', 'FG-12', set_adr(lambda m: m.update(gate_version='2')),
            'otro contexto')
    ev_case('D37', 'metadatos del ADR que citan el commit candidato (campo no admitido)', 'FG-12',
            set_adr(lambda m: m.update(applies_to_candidate_commit=CAND)), 'metadatos con campos distintos')
    ev_case('D38', 'ADR con un carácter invisible', 'FG-12', set_adr(prose=ADR_PROSE.replace('Contexto\n', 'Contexto⁠\n', 1)),
            'caracteres invisibles')
    ev_case('D39', 'ADR sin la sección de consecuencias', 'FG-12',
            set_adr(prose=ADR_PROSE.replace('## Consecuencias', '## Otras notas')), 'faltan las secciones')
    ev_case('D40', 'ADR con estado RECHAZADO en registro y bloque', 'FG-12',
            both(fg12(lambda d: d['successor_adr'].update(status='RECHAZADO')), set_adr()), 'está RECHAZADO')
    ev_case('D41', 'ADR con ei09_decision vacía en sus metadatos', 'FG-12', set_adr(lambda m: m.update(ei09_decision=None)),
            'ei09_decision de los metadatos')
    ev_case('D42', 'informe con el auditor del bloque como texto', 'FG-02',
            set_report(lambda m: m.update(auditor='Sesión de auditoría independiente AF3')), 'auditor con campos distintos')
    # Regresiones aisladas, añadidas tras la metaprueba de ablación: solo falla la regla indicada.
    ev_case('D43', 'identidad del auditor con menos de tres letras (Jo)', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='Jo')), set_report()), 'sin contenido visible suficiente')
    ev_case('D44', 'informe sin título de nivel 1', 'FG-02',
            set_report(prose=REPORT_PROSE.split('\n', 2)[2]), 'debe empezar con un título')

    def escaped_report(docs, ctx):
        """Bloque del informe con escapes JSON: el documento queda en ASCII, NFC y sin caracteres invisibles."""
        meta = json.dumps(report_meta(docs['FG-02']), ensure_ascii=True, indent=2)
        set_report(raw=(REPORT_PROSE + f'\n```f36sbx-audit-metadata\n{meta}\n```\n').encode('utf-8'))(docs, ctx)
    ev_case('D45', 'identidad no NFC escondida con escapes JSON en el bloque del informe', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='Sesión de auditoría ficticia')), escaped_report),
            'no está en NFC')
    ev_case('D46', 'identidad con U+200B escondida con escapes JSON en el bloque del informe', 'FG-02',
            both(fg02(lambda d: d['auditor'].update(name='Revisora​Externa Ficticia')), escaped_report),
            'caracteres invisibles')

    # ---------------- AF3-M01: el ADR es el blob de candidate_commit:path (decisión, en memoria)
    # La resolución con Git real (ignorados, sin versionar, sustituidos, tipos) la prueba test_f36sbx_git.py.
    def adr_entry(fn):
        """Mutación de la resolución Git del ADR para el commit candidato."""
        def f(docs, ctx):
            key = (docs['FG-12']['candidate_commit'], ADR_PATH)
            ctx['adr_blobs'][key] = fn(ctx['adr_blobs'][key])
        return f
    no_blob = 'no es un blob regular versionado en el commit candidato'
    af2('AF3-01', 'ADR que no existe en el árbol del commit candidato (ignorado, sin versionar o ausente)', 'FG-12',
        adr_entry(lambda b: {'error': 'no existe en el árbol del commit'}), no_blob)
    af2('AF3-02', 'ADR versionado solo en otro commit, no en el candidato', 'FG-12',
        lambda docs, ctx: ctx['adr_blobs'].update({(OTHER, ADR_PATH): ctx['adr_blobs'].pop((CAND, ADR_PATH))}), no_blob)
    af2('AF3-03', 'ruta del ADR que es un árbol (directorio) en el commit candidato', 'FG-12',
        adr_entry(lambda b: {**b, 'type': 'tree', 'mode': '040000'}), no_blob)
    af2('AF3-04', 'ADR que es un enlace simbólico (modo 120000)', 'FG-12', adr_entry(lambda b: {**b, 'mode': '120000'}), no_blob)
    af2('AF3-05', 'ADR que es un submódulo (tipo commit, modo 160000)', 'FG-12',
        adr_entry(lambda b: {**b, 'type': 'commit', 'mode': '160000'}), no_blob)
    af2('AF3-06', 'ADR ejecutable (modo 100755)', 'FG-12', adr_entry(lambda b: {**b, 'mode': '100755'}), no_blob)
    af2('AF3-07', 'resolución con bytes que no son los del objeto Git (bytes del árbol de trabajo)', 'FG-12',
        adr_entry(lambda b: {**b, 'data': b['data'] + b'\nCopia del arbol de trabajo.\n'}), 'los bytes no son los del objeto')
    af2('AF3-08', 'SHA-256 declarado de otra copia del ADR, distinta del blob del candidato', 'FG-12',
        lambda docs, ctx: docs['FG-12']['successor_adr'].update(sha256=v.sha256(b'otra copia del ADR')),
        'no es el del blob del ADR en el commit candidato')
    case('AF3-09', 'evidencia que Git ignora (nunca podría estar en un commit)',
         chain(register(), lambda s: s.update(ignored=[path('FG-02')])), 'GATE', 'Git lo ignora')
    case('AF3-10', 'no se puede comprobar con Git si la evidencia es versionable (falla cerrado)',
         chain(register(), setkey('ignored', None)), 'GATE', 'no se pudo comprobar con Git')
    ok(v.blob_problem(blob(b'# ADR\n')) is None and v.blob_problem(None) and v.blob_problem({'error': 'x'})
       and v.blob_problem({**blob(b'a'), 'object': '0' * 40}), 'AF3-11',
       'contraste: blob_problem acepta un blob regular íntegro y rechaza la ausencia, el error y un objeto que no corresponde', '')

    # ---------------- registro de evidencia en el repositorio (GR)
    snap = copy.deepcopy(BASE)
    register()(snap)
    res, gate = v.run(snap)
    fl = [f'{n}: {m[:160]}' for n, ok_, m in res if not ok_]
    ok(not fl and gate == 'NO SUPERADO', 'GR01', 'control positivo: registro parcial válido de FG-02 (el gate sigue NO SUPERADO)',
       f'gate {gate}' if not fl else f'fallas: {fl}')
    case('GR02', 'FG-02 en CUMPLE con evidencia vacía', register(mutate=lambda d, c: d.update({'FG-02': b''})), 'GATE',
         'semánticamente válida')
    case('GR03', 'FG-02 en CUMPLE con auditoría rechazada',
         register(mutate=lambda d, c: d['FG-02'].update(verdict='NO_APROBADO_PARA_INTEGRACION')), 'GATE', 'no aprueba')
    case('GR04', 'FG-02 en CUMPLE de otro commit',
         register(mutate=lambda d, c: d['FG-02'].update(candidate_commit=OTHER)), 'GATE', 'distinto del candidato')
    case('GR05', 'archivo de evidencia sin citar', chain(register(), lambda s: s['evidence'].update({EV + 'suelto.json': b'{}'})),
         'GATE', 'sin citar')
    case('GR06', 'evidencia ilegible o enlace simbólico', chain(register(), lambda s: s['evidence'].update({EV + 'enlace.json': None})),
         'GATE', 'enlaces o ilegibles')
    case('GR07', 'el paquete cambió después del candidato',
         chain(register(), lambda s: s['facts'][CAND]['changed'].append(v.MATRIX)), 'GATE', 'el paquete cambió')
    case('GR08', 'el documento del gate cambió fuera de la columna Estado',
         chain(register(), sub(G, '## 6. Lo que el gate no puede autorizar', '## 6. Lo que el gate tampoco autoriza')),
         'GATE', 'fuera de la columna Estado')
    case('GR09', 'criterios EQUIPO en CUMPLE sin candidate_commit',
         chain(register(), jmut(S, lambda d: d.update(candidate_commit=None))), 'GATE', 'sin candidate_commit')
    case('GR10', 'FG-10 en NO APLICA', chain(jmut(S, lambda d: d['criteria'][9].update(status='NO APLICA')),
                                             sub(G, 'Nunca es NO APLICA | PENDIENTE |', 'Nunca es NO APLICA | NO APLICA |')),
         'GATE', 'no admitido para este criterio')
    case('GR11', 'f37_authorized_ei sin FG-03 en CUMPLE', jmut(S, lambda d: d.update(f37_authorized_ei=['EI-01'])), 'GATE',
         'sin FG-03 en CUMPLE')
    case('GR12', 'esquema de evidencia con un veredicto rechazado como aprobatorio',
         jmut(SCH, lambda d: d['criteria']['FG-02']['passing_verdicts'].append('NO_APROBADO_PARA_INTEGRACION')), 'GATE',
         'FG-02: solo veredictos aprobatorios')
    case('GR13', 'esquema de evidencia con quórum 2/3', jmut(SCH, lambda d: d['approvals'].update(quorum='2/3')), 'GATE',
         'quórum 3/3')
    case('GR14', 'esquema de evidencia con otro integrante',
         jmut(SCH, lambda d: d.update(team_members=['Coronacion Meza Fredy', 'Persona Ficticia', 'Vila Meza Luis Antonio'])),
         'GATE', 'tres integrantes')
    case('GR15', 'evidencia PENDIENTE que cita un archivo', jmut(S, lambda d: d['criteria'][1].update(evidence=EV + 'FG-02.json')),
         'GATE', 'solo un criterio en CUMPLE cita evidencia')
    case('GR16', 'el JSON declara SUPERADO', jmut(S, lambda d: d.update(declared_result='SUPERADO')), 'GATE', 'declarado')
    case('GR17', 'el gate autoriza producción', jmut(S, lambda d: d['authorizes'].append('produccion')), 'GATE', 'solo autoriza')
    case('GR18', 'el gate deja de excluir los datos reales', jmut(S, lambda d: d['cannot_authorize'].remove('datos_reales')),
         'GATE', 'solo autoriza')
    case('GR19', 'revocación no reflejada en el resultado',
         jmut(S, lambda d: d.update(revocation={'fecha': '2026-10-26', 'motivo': 'prueba'})), 'GATE', 'recalculado')
    case('GR20', 'FG-02 se disfraza de AUTO', jmut(S, lambda d: d['criteria'][1].update(kind='auto')), 'GATE', 'claves o tipo')
    case('GR21', 'base equivocada', jmut(S, lambda d: d.update(base_commit='0' * 40)), 'GATE', 'identidad')
    case('GR22', 'FG-04 declarado distinto del recalculado', jmut(S, lambda d: d['criteria'][3].update(status='NO CUMPLE')),
         'GATE', 'AUTO declarados')
    case('GR23', 'clave duplicada en el estado del gate',
         sub(S, '"gate_version": "3",', '"gate_version": "3",\n  "gate_version": "4",'), 'GATE', 'JSON inválido')
    case('GR24', 'tabla FG del documento distinta del JSON', sub(G, '| Regla FRZ | CUMPLE |', '| Regla FRZ | PENDIENTE |'),
         'GATE', 'tabla FG')
    case('GR25', 'AUTO declarado CUMPLE con el gobierno roto', sub('CLAUDE.md', '- F36-SBX-GATE = NO SUPERADO\n', ''),
         'GATE', 'AUTO declarados')
    case('GR26', 'candidate_commit con formato inválido', jmut(S, lambda d: d.update(candidate_commit='HEAD')), 'GATE',
         'fuera de formato')
    case('GR27', 'esquema de evidencia v1 (sin bloque canónico)', jmut(SCH, lambda d: d.update(schema_tag='f36sbx-team-evidence/v1')),
         'GATE', 'idéntico a la versión cerrada')
    case('GR28', 'esquema cuyo ADR cita el commit que lo contiene',
         jmut(SCH, lambda d: d['criteria']['FG-12']['adr_metadata_fields'].append('applies_to_candidate_commit')), 'GATE',
         'nunca el commit que lo contiene')
    case('GR29', 'PII en el ADR citado por FG-12',
         register(('FG-02', 'FG-03', 'FG-12'), set_adr(prose=ADR_PROSE + '\nContacto: adr' + '@' + 'colegio.pe\n')),
         'PII', f'ADR_006_prueba_en_memoria.md ({CAND[:12]}): correo')

    # ---------------- regla de decisión (G)
    def stub(errors):
        return lambda fg: errors
    real_state = json.loads(BASE['texts'][S])
    ok(v.evaluate_gate(real_state, v.EXPECTED_CLASSES, stub([])) == 'NO SUPERADO', 'G01', 'estado real → NO SUPERADO', '')
    for fg in v.FG_TEAM:
        ctx = build()
        bad = v.evaluate_gate(ctx['state'], v.EXPECTED_CLASSES,
                              lambda x, fg=fg: ['inválida'] if x == fg else v.team_evidence_errors(x, ctx))
        ok(bad == 'NO SUPERADO', f'G02-{fg}', f'todo CUMPLE pero {fg} inválida → NO SUPERADO', bad)

    def gstate(fn):
        st = build()['state']
        fn(st)
        return v.evaluate_gate(st, v.EXPECTED_CLASSES, stub([]))
    decisions = [
        ('G03', 'FG-12 NO APLICA con una EI CONDITIONAL autorizada', lambda st: st['criteria'][11].update(status='NO APLICA'),
         'NO SUPERADO'),
        ('G04', 'FG-10 NO APLICA', lambda st: st['criteria'][9].update(status='NO APLICA'), 'NO SUPERADO'),
        ('G05', 'estado desconocido', lambda st: st['criteria'][2].update(status='APROBADO'), 'NO SUPERADO'),
        ('G06', 'revocación con todo CUMPLE', lambda st: st.update(revocation={'motivo': 'prueba'}), 'REVOCADO'),
        ('G07', 'autoriza producción', lambda st: st['authorizes'].append('produccion'), 'NO SUPERADO'),
        ('G08', 'falta FG-14', lambda st: st['criteria'].pop(), 'NO SUPERADO'),
        ('G09', 'autorización con una EI BLOCKED', lambda st: st.update(f37_authorized_ei=['EI-01', 'EI-19']), 'NO SUPERADO'),
        ('G10', 'sin candidato con todo CUMPLE', lambda st: st.update(candidate_commit=None), 'NO SUPERADO'),
        ('G11', 'sin lista de EI con todo CUMPLE', lambda st: st.update(f37_authorized_ei=None), 'NO SUPERADO'),
        ('G12', 'EI repetida en la autorización', lambda st: st.update(f37_authorized_ei=['EI-01', 'EI-01']), 'NO SUPERADO'),
        ('G13', 'AUTO en NO APLICA', lambda st: st['criteria'][0].update(status='NO APLICA'), 'NO SUPERADO'),
    ]
    for cid, desc, fn, expected in decisions:
        got = gstate(fn)
        ok(got == expected, cid, f'{desc} → {expected}', got)
    ok(v.evaluate_gate(None, v.EXPECTED_CLASSES, stub([])) == 'NO SUPERADO', 'G14', 'estado no legible → NO SUPERADO', '')

    for i, exc in enumerate((KeyError('roto'), StopIteration(), RuntimeError('roto'))):
        def boom(fg, exc=exc):
            raise exc
        ok(v.evaluate_gate(build()['state'], v.EXPECTED_CLASSES, boom) == 'NO SUPERADO', f'G15{"abc"[i]}',
           f'una excepción {exc.__class__.__name__} al validar la evidencia → NO SUPERADO (fail-closed)', '')
    ok(v.doc_status_only('a\n| FG-02 | x | EQUIPO | y | PENDIENTE |', 'a\n| FG-02 | x | EQUIPO | y | CUMPLE |')
       and not v.doc_status_only('a\n| FG-02 | x | EQUIPO | y | PENDIENTE |', 'b\n| FG-02 | x | EQUIPO | y | CUMPLE |')
       and not v.doc_status_only('| FG-02 | x | EQUIPO | y | PENDIENTE |', '| FG-02 | z | EQUIPO | y | PENDIENTE |'),
       'G16', 'el documento del gate solo admite cambios en la columna Estado', '')

    # ---------------- controles positivos adicionales (P)
    names = ['Dra. Ficticia Núñez-Ejemplo (revisora académica)', 'Sesión AF3 · revisión independiente ficticia', 'Ana']
    bad_names = {n: v.identity_errors(n, 'identidad') for n in names}
    ok(not any(bad_names.values()), 'P-07', 'control positivo: identidades visibles con tildes, guiones y puntuación son válidas',
       str({k: e for k, e in bad_names.items() if e}))
    ok(all(v.identity_errors(n, 'identidad') for n in ('', '  ', '...', 'N/A', '​​​', 'Revisora‮Externa',
                                                        'TBD', 'auditoría independiente', 'x' * 121)),
       'P-08', 'contraste: identidades vacías, invisibles, genéricas o demasiado largas son inválidas', '')
    ctx = build(mutate=set_report(extra='\n```text\nNota técnica sin valores normativos.\n```\n'))
    ok(v.team_evidence_errors('FG-02', ctx) == [], 'P-09', 'control positivo: un bloque de código ajeno, sin tokens ni '
       'aserciones, no invalida el informe', str(v.team_evidence_errors('FG-02', ctx)[:2]))
    pos('P-10', 'control positivo: registro de FG-02, FG-03 y FG-12 con informe y ADR válidos (gate NO SUPERADO: falta FG-10)',
        register(('FG-02', 'FG-03', 'FG-12')))
    pos('P-11', 'límite documentado: un artefacto de dev fuera del ajuste puede cambiar sin resellar (dev no se sella)',
        jmut(EX, lambda e: (r_content(5, lambda c: c.update(text_synthetic=c['text_synthetic'] + ' Variante.'))(e),
                            rehash_all(e))))

    # ---------------- falsos PASS de la auditoría AF1, reconstruidos sobre 06e933e (AUD)
    for i, fg in enumerate(v.FG_TEAM, 1):
        case(f'AUD-{i:02d}', f'{fg} en CUMPLE con un archivo cualquiera ({{}})',
             chain(register((fg,) if fg == 'FG-02' else ('FG-02', fg)),
                   lambda s, fg=fg: s['evidence'].update({path(fg): b'{}'})), 'GATE', 'semánticamente válida')
    aud_c = [
        ('AUD-05', 'tipo de artefacto desconocido', c_cases[1][2]),
        ('AUD-06', 'transcripción sin revisar', c_cases[15][2]),
        ('AUD-07', 'observation_kind con una inferencia', c_cases[16][2]),
        ('AUD-08', 'provenance sin upstream_refs ni seed', c_cases[10][2]),
        ('AUD-09', 'fragmento sin artifact_id', c_cases[11][2]),
        ('AUD-10', 'partición sin familia de plantilla', c_cases[8][2]),
        ('AUD-11', 'propiedad adicional peligrosa', c_cases[13][2]),
        ('AUD-12', 'campo sinónimo de puntaje', c_cases[14][2]),
        ('AUD-13', 'fuentes prohibidas recortadas', c_cases[17][2]),
        ('AUD-14', 'estado del contrato cambiado', c_cases[18][2]),
        ('AUD-15', 'embargo temporal eliminado', c_cases[9][2]),
    ]
    for cid, desc, fn in aud_c:
        case(cid, desc, jmut(C, fn), 'CTR')
    case('AUD-16', 'capacidad ALLOWED que nombra OCR', sub(M, 'Búsqueda léxica exacta, por subcadena',
                                                           'OCR y búsqueda léxica exacta, por subcadena'), 'CAP')
    case('AUD-17', 'línea desconocida en el estado vigente',
         sub('CLAUDE.md', '- F37-SBX = BLOQUEADA\n', '- F37-SBX = BLOQUEADA\n- F37-SBX-A = HABILITADA\n'), 'GOV')
    case('AUD-18', 'afirmación «ADR-006 = APROBADO» en el paquete', sub(PR, '- RF-23 sigue', '- ADR-006 = APROBADO.\n- RF-23 sigue'),
         'SEM')

    bad = [r for r in results if not r[0]]
    for ok_, cid, desc, detail in results:
        print(f'{"OK   " if ok_ else "FALLA"} {cid} {desc}: {detail}')
    print(f'test_f36sbx: {len(results) - len(bad)} casos correctos, {len(bad)} fallas')
    return 1 if bad else 0


def TO_SCENARIO_ONE(e):
    """Todo el ejemplo en un solo escenario (SC36-01)."""
    transplant({'SC36-02': 'SC36-01'})(e)


BASE = v.collect(v.ROOT)
CONTRACT = v.strict_json(BASE['texts'][C])
COMPETENCIES_SHA = ((v.json_bytes(BASE['upstream'][F34 + 'manifest.json']) or {}).get('files', {})
                    .get('competencies.csv', {}).get('sha256', 'e' * 64))

if __name__ == '__main__':
    sys.exit(main())
