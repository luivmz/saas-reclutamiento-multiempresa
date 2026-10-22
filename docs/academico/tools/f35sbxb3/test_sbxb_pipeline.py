"""F35-SBX-B — B3: pruebas del pipeline determinista (test_sbxb_pipeline.py).

Uso:  python -I docs/academico/tools/f35sbxb3/test_sbxb_pipeline.py   (sin -I, se relanza)

PT01..PT30: ejecución completa, doble ejecución en proceso y en procesos nuevos, conformidad de nivel 1 y nivel 2
recalculada aquí con una implementación propia, comprobantes de purga, identificadores de B, los negativos TSBB que se
prueban en el pipeline y el fallo inyectado en cada uno de los doce pasos. Nada se escribe en disco: las entradas
alteradas se pasan en memoria y cada ejecución usa almacenes ':memory:' nuevos.
"""
import os
import sys

if __name__ == '__main__' and not sys.flags.isolated:
    _argv = [sys.executable, '-I', '-B'] + (['-X', 'utf8'] if sys.flags.utf8_mode else []) + \
        [os.path.abspath(__file__)] + sys.argv[1:]
    if os.name == 'nt':
        _argv = ['"' + a.replace('"', '\\"') + '"' if (' ' in a or '\t' in a) else a for a in _argv]
    sys.exit(os.spawnv(os.P_WAIT, sys.executable, _argv))

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path[:] = [HERE] + [p for p in sys.path if not (os.path.normcase(os.path.abspath(p or os.curdir)) + os.sep)
                        .startswith(os.path.normcase(ROOT) + os.sep)]

import copy  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402

PIPELINE = os.path.join(HERE, 'sbxb_pipeline.py')
FIXTURES = {o: f'docs/academico/evidencia-sbx/fixtures/{o}_evidencias.json' for o in ('ORG-S1', 'ORG-S2', 'ORG-S3')}
STATES = ['pendiente', 'validando', 'registrado', 'transformado', 'en_revision', 'revisado', 'completado']
ACTIONS = ['fixture_verificado', 'esquema_validado', 'sintetico_verificado', 'hash_calculado', 'provenance_registrada',
           'tenant_validado', 'revision_simulada_registrada', 'ejecucion_cerrada']
COUNTS = {'tenant_context': 1, 'pipeline_run': 1, 'pipeline_event': 7, 'evidence_source': 2, 'evidence_record': 2,
          'evidence_provenance': 2, 'simulated_review': 2, 'audit_entry': 8}
GENESIS = '0' * 64
SUMMARY = 'test_sbxb_pipeline: '


class Failure(Exception):
    pass


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(obj):
    return hashlib.sha256(canon(obj)).hexdigest()


def expect(condition, why):
    if not condition:
        raise Failure(why)


def fixture(org):
    with open(os.path.join(ROOT, *FIXTURES[org].split('/')), 'rb') as f:
        return json.loads(f.read().decode('utf-8'))


def cli(*args):
    p = subprocess.run([sys.executable, '-I', '-B', PIPELINE, *args], cwd=ROOT, capture_output=True, timeout=600,
                       env={k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')})
    return p.returncode, p.stdout, p.stderr


# ---------------------------------------------------------------- verificaciones propias (independientes del pipeline)
def own_chain(items, key, prev_key):
    prev, out = GENESIS, []
    for item in items:
        if item.get(prev_key) != prev:
            out.append(f'{key}: eslabón roto en {item.get(key, "?")[:12]}')
        if item.get(key) != sha({k: v for k, v in item.items() if k != key}):
            out.append(f'{key}: hash recalculado distinto en {item.get(key, "?")[:12]}')
        prev = item.get(key)
    return out


def own_level1(run, fx):
    """Proyección de nivel 1 de B0 §5.2, calculada aquí: emparejamiento por clave natural."""
    t = run['tables']
    out = []
    if [e['state'] for e in t['pipeline_event']] != [e['state'] for e in fx['events']]:
        out.append('estados de los eventos distintos del oráculo')
    if [e['error_code'] for e in t['pipeline_event']] != [e['error_code'] for e in fx['events']]:
        out.append('error_code de los eventos distintos del oráculo')
    if [e['seq'] for e in t['pipeline_event']] != list(range(1, len(t['pipeline_event']) + 1)):
        out.append('seq no contiguo')
    if [a['action'] for a in t['audit_entry']] != [a['action'] for a in fx['audit']]:
        out.append('acciones de auditoría distintas del oráculo')
    a_src = {s['source_id']: s for s in fx['sources']}
    b_src = {s['source_id']: s for s in t['evidence_source']}
    a_rev = {r['record_id']: r for r in fx['reviews']}
    b_rev = {r['record_id']: r for r in t['simulated_review']}
    a_prov = {p['record_id']: p for p in fx['provenance']}
    b_prov = {p['record_id']: p for p in t['evidence_provenance']}

    def keyed(records, src):
        return {(r['synthetic_organization_id'], src[r['source_id']]['origin_record_id']): r for r in records}
    a_rec, b_rec = keyed(fx['records'], a_src), keyed(t['evidence_record'], b_src)
    if set(a_rec) != set(b_rec):
        return out + [f'claves naturales distintas: {sorted(set(a_rec) ^ set(b_rec))[:3]}']
    for key in sorted(a_rec):
        ra, rb = a_rec[key], b_rec[key]
        for f in ('synthetic_organization_id', 'criterion_ref', 'evidence_kind', 'text_synthetic', 'hash_algorithm',
                  'content_hash', 'validation_status', 'review_status', 'source_type', 'environment'):
            if ra[f] != rb[f]:
                out.append(f'{key}: {f} distinto del oráculo')
        sa, sb = a_src[ra['source_id']], b_src[rb['source_id']]
        for f in ('origin_dataset_version', 'origin_file', 'origin_file_sha256', 'origin_record_id', 'source_type',
                  'synthetic_organization_id'):
            if sa[f] != sb[f]:
                out.append(f'{key}: fuente {f} distinta del oráculo')
        pa, pb = a_prov[ra['synthetic_id']], b_prov[rb['synthetic_id']]
        for f in ('provenance_kind', 'transformation_id', 'transformation_version', 'hash_before', 'hash_after'):
            if pa[f] != pb[f]:
                out.append(f'{key}: procedencia {f} distinta del oráculo')
        if pb['source_id'] != rb['source_id'] or b_rev[rb['synthetic_id']]['review_id'] != pb['review_id']:
            out.append(f'{key}: relación evidencia ↔ fuente ↔ revisión rota')
        va, vb = a_rev[ra['synthetic_id']], b_rev[rb['synthetic_id']]
        for f in ('review_scope', 'review_status', 'reviewer_type', 'scripted', 'simulation_actor'):
            if va[f] != vb[f]:
                out.append(f'{key}: revisión {f} distinta del oráculo')
    order_a = [(r['synthetic_organization_id'], a_src[r['source_id']]['origin_record_id'])
               for r in (next(x for x in fx['records'] if x['synthetic_id'] == p['record_id']) for p in fx['provenance'])]
    order_b = [(r['synthetic_organization_id'], b_src[r['source_id']]['origin_record_id'])
               for r in (next(x for x in t['evidence_record'] if x['synthetic_id'] == p['record_id'])
                         for p in t['evidence_provenance'])]
    if order_a != order_b:
        out.append('orden de la cadena de procedencia distinto del oráculo')
    counts = {k: len(v) for k, v in t.items()}
    if counts != COUNTS:
        out.append(f'conteos distintos: {counts}')
    return out


def own_receipt(run):
    r = run['receipt']
    t = run['tables']
    out = []
    for k, v in (('closure_kind', 'purga'), ('final_state', 'completado'), ('connection', 'CLOSED'),
                 ('post_close_check', 'ProgrammingError'), ('file_backed', False), ('error_code', '')):
        if r.get(k) != v:
            out.append(f'comprobante con {k} = {r.get(k)!r}, se exige {v!r}')
    if r.get('counts') != {k: len(v) for k, v in t.items()}:
        out.append('conteos del comprobante distintos de las tablas')
    if r.get('last_event_hash') != t['pipeline_event'][-1]['event_hash']:
        out.append('el comprobante no se encadena al evento completado')
    if r.get('receipt_hash') != sha({k: v for k, v in r.items() if k != 'receipt_hash'}):
        out.append('receipt_hash no recalculable')
    if run.get('post_purge') != 'E-PURGADO':
        out.append('el almacén se pudo usar tras la purga')
    return out


# ---------------------------------------------------------------- casos
def pt01(p):
    report, code = p.run()
    expect(code == 0 and report['result'] == 'completado', f'resultado {report.get("result")} con código {code}')
    expect(p.check_report(report) == [], f'esquema del informe: {p.check_report(report)[:2]}')
    expect([r['synthetic_organization_id'] for r in report['runs']] == ['ORG-S1', 'ORG-S2', 'ORG-S3'], 'tenants')
    for r in report['runs']:
        expect(r['final_state'] == 'completado', f'{r["synthetic_organization_id"]}: {r["final_state"]}')
        expect({k: len(v) for k, v in r['tables'].items()} == COUNTS, f'{r["synthetic_organization_id"]}: conteos')
        expect([s['step'] for s in r['steps']] == list(range(1, 13)), 'los doce pasos')
    return 'tres runs completados, doce pasos y conteos 1/1/7/2/2/2/2/8'


def pt02(p):
    a, b = p.report_bytes(p.run()[0]), p.report_bytes(p.run()[0])
    expect(a == b, 'dos ejecuciones en el mismo proceso dan bytes distintos')
    return f'{len(a)} bytes idénticos'


def pt03(p):
    (c1, o1, e1), (c2, o2, e2) = cli(), cli()
    expect(c1 == c2 == 0, f'códigos {c1} y {c2}: {(e1 or e2)[-200:]!r}')
    expect(o1 == o2, 'dos procesos dan informes distintos')
    expect(o1.endswith(b'\n') and b'\r' not in o1, 'informe sin LF final o con CR')
    report = json.loads(o1.decode('utf-8'))
    expect(o1 == p.report_bytes(report), 'la salida no es el JSON canónico del informe')
    return f'{len(o1)} bytes idénticos en dos procesos'


def pt04(p):
    report, _ = p.run()
    for r in report['runs']:
        fx = fixture(r['synthetic_organization_id'])
        diff = own_level1(r, fx)
        expect(not diff, f'{r["synthetic_organization_id"]}: {diff[:2]}')
        expect(p.level1(r, fx) == [], f'{r["synthetic_organization_id"]}: el pipeline no ve su propia conformidad')
        expect(r['conformity'] == {'level1': 'conforme', 'level2': 'integra'}, 'conformidad informada')
        expect((r['seed'], r['clock_start']) == (fx['run']['seed'], fx['run']['clock_start']), 'escenario del oráculo')
    return 'nivel 1 conforme en los tres tenants y escenarios del oráculo'


def pt05(p):
    report, _ = p.run()
    for r in report['runs']:
        t = r['tables']
        problems = own_chain(t['pipeline_event'], 'event_hash', 'prev_event_hash') + \
            own_chain(t['evidence_provenance'], 'provenance_hash', 'prev_provenance_hash') + \
            own_chain(t['audit_entry'], 'audit_hash', 'prev_audit_hash')
        expect(not problems, f'{r["synthetic_organization_id"]}: {problems[:2]}')
        expect(p.level2(r) == [], f'{r["synthetic_organization_id"]}: nivel 2 del pipeline')
    return 'cadenas de eventos, procedencia y auditoría recalculadas'


def pt06(p):
    seen = []
    report, _ = p.run(observe=lambda mod, store: seen.append((mod, store)))
    for r in report['runs']:
        problems = own_receipt(r)
        expect(not problems, f'{r["synthetic_organization_id"]}: {problems[:2]}')
        expect(p.check_receipt(r['receipt'], r) == [], 'el pipeline rechaza su propio comprobante')
    expect(len(seen) == 3, f'se observaron {len(seen)} almacenes, no 3')
    for mod, store in seen:         # observación en el proceso: un comprobante coherente no basta
        try:
            mod.list_events(store)
            raise Failure('un almacén sigue utilizable tras la purga')
        except Exception as e:
            expect(getattr(e, 'code', None) == 'E-PURGADO', f'tras la purga: {e.__class__.__name__} {e}')
    return 'comprobantes verificados; los tres almacenes, inutilizables (E-PURGADO)'


def pt07(p):
    report, _ = p.run()
    for r in report['runs']:
        o, seed = r['synthetic_organization_id'], r['seed']
        space = f'{o}-{seed:010d}'
        t = r['tables']
        ids = [t['pipeline_run'][0]['pipeline_run_id']] + [x['event_id'] for x in t['pipeline_event']] + \
            [x['audit_id'] for x in t['audit_entry']] + [x['source_id'] for x in t['evidence_source']] + \
            [x['synthetic_id'] for x in t['evidence_record']] + [x['provenance_id'] for x in t['evidence_provenance']] + \
            [x['review_id'] for x in t['simulated_review']]
        expect(all(i.startswith('SBB') and space in i for i in ids), f'{o}: identificador fuera de SBB*-{space}')
        expect(b'SBX' not in canon(t), f'{o}: identificadores de A copiados')
    return 'identificadores SBB* del espacio <org>-<semilla>'


def failed(report, code, org, step, error):
    expect(code == 1 and report['result'] == 'fallido', f'resultado {report.get("result")} con código {code}')
    expect('runs' not in report, 'resultado parcial en un informe fallido')
    f = report['failure']
    expect((f['synthetic_organization_id'], f['step'], f['error_code']) == (org, step, error),
           f'falla en {f["synthetic_organization_id"]} paso {f["step"]} {f["error_code"]}, se exige {org} paso {step} '
           f'{error}')


def pt08(p):
    raw = bytearray(open(os.path.join(ROOT, *FIXTURES['ORG-S1'].split('/')), 'rb').read())
    raw[raw.index(b'Menciona')] = ord(b'm')
    report, code = p.run(overrides={FIXTURES['ORG-S1']: bytes(raw)})
    failed(report, code, 'ORG-S1', 1, 'E-FIXTURE')
    return 'un byte del fixture alterado: fallido en el paso 1'


def pt09(p):
    rec = copy.deepcopy(fixture('ORG-S1')['records'][0])
    rec['text_synthetic'] = '[SINTÉTICO] Contacto persona.ficticia' + '@' + 'ejemplo-sintetico.org'
    expect(p.check_synthetic(rec, 'ORG-S1'), 'dato personal admitido en el paso 3')
    rec = copy.deepcopy(fixture('ORG-S1')['records'][0])
    expect(p.check_synthetic(rec, 'ORG-S2'), 'registro de otro tenant admitido en el paso 3')
    store = p.load_store()
    s = store.open_tenant_store({'synthetic_organization_id': 'ORG-S1', 'tenant_kind': 'synthetic_organization',
                                 'origin_dataset_version': 'f34-synth-1.1.0', 'simulation_actor': 'SIMREV-ORG-S1'})
    store.create_run(s, 20261008, '2026-10-07T09:00:00')
    row = fixture('ORG-S2')
    ev = p.evidence_for(row['sources'][0]['origin_record_id'], 'ORG-S2', 'conforme', '2026-10-07T09:05:00',
                        '2026-10-07T09:08:00')
    try:
        store.append_evidence(s, ev)
        raise Failure('el almacén admitió una fila de otro tenant')
    except store.SbxbStoreError as e:
        expect(e.code == 'E-ORIGEN', f'código {e.code}')
    return 'dato personal y tenant ajeno rechazados; fila de otro tenant: E-ORIGEN'


def pt10(p):
    problems = p.check_tenant_rows('ORG-S1', {'evidence_source': [{'synthetic_organization_id': 'ORG-S2',
                                                                    'source_id': 'SBBS-ORG-S2-0020261009-000001'}]})
    expect(problems, 'fila de otro tenant no detectada en el paso 7')
    other = open(os.path.join(ROOT, *FIXTURES['ORG-S2'].split('/')), 'rb').read()
    report, code = p.run(overrides={FIXTURES['ORG-S1']: other})
    failed(report, code, 'ORG-S1', 1, 'E-FIXTURE')
    return 'fixture de otro tenant: fallido en el paso 1; fila ajena detectada en el paso 7'


def pt11(p):
    report, _ = p.run()
    r = copy.deepcopy(report['runs'][0])
    r['tables']['evidence_provenance'][1]['prev_provenance_hash'] = '1' * 64
    expect(p.level2(r), 'eslabón de procedencia alterado no detectado')
    r = copy.deepcopy(report['runs'][0])
    r['tables']['evidence_provenance'][0]['hash_before'] = '2' * 64
    expect(p.level1(r, fixture('ORG-S1')), 'hash_before alterado no detectado por el nivel 1')
    return 'eslabón y hash_before alterados: nivel 2 y nivel 1 en falla'


def pt12(p):
    store = p.load_store()
    s = store.open_tenant_store({'synthetic_organization_id': 'ORG-S1', 'tenant_kind': 'synthetic_organization',
                                 'origin_dataset_version': 'f34-synth-1.1.0', 'simulation_actor': 'SIMREV-ORG-S1'})
    store.create_run(s, 20261008, '2026-10-07T09:00:00')
    ev = p.evidence_for(fixture('ORG-S1')['sources'][0]['origin_record_id'], 'ORG-S1', 'conforme',
                        '2026-10-07T09:05:00', '2026-10-07T09:08:00')
    store.append_evidence(s, ev)
    try:
        store.append_evidence(s, ev)
        raise Failure('reescritura de una evidencia ya registrada admitida')
    except store.SbxbStoreError as e:
        expect(e.code == 'E-ORIGEN', f'código {e.code}')
    d = store.diagnostic(s)
    expect(d['failed_event'] == 'FAILED_EVENT_COMMITTED' and d['final_state'] == 'fallido', f'diagnóstico {d}')
    return 'reescritura rechazada (E-ORIGEN) y run fallido confirmado'


def pt13(p):
    store = p.load_store()
    ctx = {'synthetic_organization_id': 'ORG-S1', 'tenant_kind': 'synthetic_organization',
           'origin_dataset_version': 'f34-synth-1.1.0', 'simulation_actor': 'SIMREV-ORG-S1'}
    s = store.open_tenant_store(ctx)
    store.create_run(s, 20261008, '2026-10-07T09:00:00')
    store.append_event(s, 'validando', '2026-10-07T09:02:00')
    try:
        store.append_event(s, 'validando', '2026-10-07T09:03:00')
        raise Failure('evento repetido admitido')
    except store.SbxbStoreError as e:
        expect(e.code == 'E-CICLO', f'evento repetido: {e.code}')
    store.purge(s)
    s = store.open_tenant_store(ctx)
    store.create_run(s, 20261008, '2026-10-07T09:00:00')
    try:
        store.create_run(s, 20261008, '2026-10-07T09:00:00')
        raise Failure('run repetido admitido')
    except store.SbxbStoreError as e:
        expect(e.code == 'E-CICLO', f'run repetido: {e.code}')
    store.purge(s)
    return 'evento y run repetidos: E-CICLO'


def pt14(p):
    for bad in ('../CLAUDE.md', 'docs/academico/evidencia-sbx/../../../.env', os.path.join(ROOT, 'CLAUDE.md'),
                'docs/academico/evidencia-sbx/fixtures/ORG-S4_evidencias.json'):
        try:
            p.resolve_input(bad)
            raise Failure(f'ruta admitida: {bad}')
        except p.PipelineError as e:
            expect(e.code == 'E-RUTA', f'{bad}: {e.code}')
    return 'rutas con .., absolutas o fuera de la lista: E-RUTA'


def pt15(p):
    report, _ = p.run()
    r = copy.deepcopy(report['runs'][0])
    r['receipt']['file_backed'] = True
    r['receipt']['receipt_hash'] = sha({k: v for k, v in r['receipt'].items() if k != 'receipt_hash'})
    expect(p.check_receipt(r['receipt'], r), 'comprobante con base en archivo admitido')
    return 'file_backed distinto de false: comprobante rechazado'


def pt16(p):
    rec = copy.deepcopy(fixture('ORG-S1')['records'][0])
    rec['text_synthetic'] = '[SINTÉTICO] <script>alerta</script>'
    expect(p.check_synthetic(rec, 'ORG-S1'), 'marcado HTML admitido en el paso 3')
    return 'marcado HTML rechazado'


def pt17(p):
    report, _ = p.run()
    bad = copy.deepcopy(report)
    bad['runs'][0]['score'] = 1
    expect(p.check_report(bad), 'campo de puntaje admitido en el informe')
    bad = copy.deepcopy(report)
    bad['ranking'] = []
    expect(p.check_report(bad), 'campo de orden admitido en el informe')
    return 'informe con puntaje u orden: esquema cerrado en falla'


def pt18(p):
    a = p.report_bytes(p.run()[0])
    b = p.report_bytes(p.run(minutes=2)[0])
    expect(a != b, 'un reloj lógico distinto no cambia el informe')
    expect(not p.same_report(a, b) and p.same_report(a, a), 'la comparación de informes no detecta la diferencia')
    return 'informes distintos detectados'


def fault(step):
    def case(p):
        first = cli('--fallo', f'ORG-S1:{step}')
        second = cli('--fallo', f'ORG-S1:{step}')
        expect(first[0] == 1, f'código {first[0]}: {first[2][-200:]!r}')
        expect(first[1] == second[1], 'diagnóstico no repetible')
        report = json.loads(first[1].decode('utf-8'))
        failed(report, 1, 'ORG-S1', step, 'E-INYECTADO')
        closure = report['failure']['closure']
        if step <= 11:
            expect(closure.get('final_state') == 'fallido', f'cierre con final_state {closure.get("final_state")}')
        expect(closure.get('connection') in ('CLOSED', 'CONNECTION_ABORTED'), 'conexión no cerrada')
        return f'paso {step}: fallido, sin resultado parcial y repetible'
    case.__name__ = f'pt{18 + step:02d}'
    return case


CASES = [('PT01', 'ejecución completa', pt01), ('PT02', 'doble ejecución en un proceso', pt02),
         ('PT03', 'doble ejecución en procesos nuevos', pt03), ('PT04', 'nivel 1 igual al oráculo', pt04),
         ('PT05', 'nivel 2 recalculado', pt05), ('PT06', 'comprobantes de purga', pt06),
         ('PT07', 'identificadores de B', pt07), ('PT08', 'TSBB-01: fixture alterado', pt08),
         ('PT09', 'TSBB-01 y TSBB-02: dato personal y fila ajena', pt09),
         ('PT10', 'TSBB-02: fixture de otro tenant', pt10), ('PT11', 'TSBB-03: procedencia alterada', pt11),
         ('PT12', 'TSBB-04: reescritura de una evidencia', pt12), ('PT13', 'TSBB-05: replay', pt13),
         ('PT14', 'TSBB-06: path traversal', pt14), ('PT15', 'TSBB-08: persistencia en archivo', pt15),
         ('PT16', 'TSBB-13: marcado HTML', pt16), ('PT17', 'TSBB-10: puntaje en el informe', pt17),
         ('PT18', 'TSBB-12: informes distintos', pt18)] + \
        [(f'PT{18 + k:02d}', f'TSBB-11: fallo inyectado en el paso {k}', fault(k)) for k in range(1, 13)]


def main():
    only = set(sys.argv[1:])
    good = bad = 0
    try:
        import sbxb_pipeline as p
    except Exception as e:      # pipeline ausente o no importable: todos los casos fallan
        p, why = None, f'pipeline no importable ({e.__class__.__name__}: {e})'
    for cid, what, fn in CASES:
        if only and cid not in only:
            continue
        try:
            if p is None:
                raise Failure(why)
            note = fn(p)
        except Exception as e:
            bad += 1
            print(f'FALLA {cid} {what}: {e.__class__.__name__}: {str(e)[:300]}', flush=True)
            continue
        good += 1
        print(f'OK    {cid} {what}: {note}', flush=True)
    print(f'{SUMMARY}{good} casos correctos, {bad} fallas')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
