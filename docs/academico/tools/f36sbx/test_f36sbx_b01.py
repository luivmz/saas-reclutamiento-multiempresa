#!/usr/bin/env python3
"""Batería del sucesor B-01 (S v2.2) — CANDIDATO EXPERIMENTAL en la rama local `exp/b01-candidato`.

No es B-01 implementado: D-02b no está emitida (AC-01) y T-01 a T-09 siguen NO EMITIDAS. Esta batería prueba el
candidato con las opciones técnicas que S propone: T-09 (a-ii), T-04 con la rama `exp/b01-candidato`, T-08 (i)
(solo la variante 3/3, `gate_version` 3), T-02 con «AUTORIZADA PARA INICIAR» y T-03 «no».

En memoria: S-T01 a S-T03, S-T09, S-T10, S-T15, S-T17, espejos E1–E7 (AC-09), REQUIRED_STATE(R) y vocabulario.
Con Git real, en un clon desechable: S-T11 a S-T14, identidad de H (H §5.6), S-T18 a S-T21 y S-T22 sobre el árbol
real de la rama. Los controles positivos (S-T11 con evidencia nula y S-T18) solo existen en el clon (AC-11).

Uso: python -I -B docs/academico/tools/f36sbx/test_f36sbx_b01.py
"""
import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_f36sbx_git as tg  # noqa: E402
import validate_f36sbx as v  # noqa: E402

H_BRANCH = 'exp/b01-candidato'
MAIN_AF5 = '55f758e013e1852de8c8daa5d6fde95e39b02b0d'
DETERMINATION = v.GATE_EVIDENCE + 'REVOCACION_DETERMINACION.md'
CURRENT = ['feature/f36-sbx-authorization-design', 'develop', 'main']
results = []


def ok(cond, cid, desc, detail=''):
    results.append((bool(cond), cid, desc, detail))


def attempt(cid, desc, fn):
    """Una prueba que no se puede ejecutar (p. ej., falta la función en el validador v3) es una falla, nunca un PASS."""
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        ok(False, cid, desc, f'no ejecutable: {e.__class__.__name__}: {e}')


def event(determination=DETERMINATION, **extra):
    rev = {'date': '2026-11-11', 'effective_from': '2026-10-28T21:05:26-05:00', 'ground': 'charter_7_3',
           'determination': determination, 'evidence': ['a' * 64]}
    rev.update(extra)
    return rev


def gate_state():
    return json.loads((v.ROOT / v.GATE_STATE).read_text(encoding='utf-8'))


def superado_state():
    """Estado en memoria que la regla de decisión daría por SUPERADO (control positivo de la función)."""
    st = gate_state()
    for c in st['criteria']:
        c['status'] = 'CUMPLE'
    st['f37_authorized_ei'] = ['EI-01']
    st['candidate_commit'] = 'b' * 40
    return st


# ------------------------------------------------------------------------------------------------- en memoria
def memory():
    classes = v.EXPECTED_CLASSES
    none = lambda fg: []  # noqa: E731

    def st01():
        st = gate_state()
        st['revocation'] = event()
        ok(v.revocation_errors(st['revocation']) == [] and v.evaluate_gate(st, classes, none) == 'REVOCADO',
           'S-T01', 'revocation con el formato de §5.8.1: R = REVOCADO')
        st2 = superado_state()
        st2['revocation'] = event()
        ok(v.evaluate_gate(st2, classes, none) == 'REVOCADO', 'S-T01b',
           'REVOCADO prevalece aunque la evidencia daría SUPERADO (I-11)')
    attempt('S-T01', 'revocación válida', st01)

    def st02():
        bad = {'sin determination': {k: x for k, x in event().items() if k != 'determination'},
               'ground desconocido': event(ground='otro'),
               'tipo distinto': 'revocado',
               'clave adicional': event(note='x'),
               'otra ruta': event(determination=v.GATE_EVIDENCE + 'OTRA.md'),
               'evidencia vacía': event(evidence=[]),
               'fecha sin formato': event(date='11/11/2026')}
        wrong = []
        for name, rev in bad.items():
            st = gate_state()
            st['revocation'] = rev
            if v.evaluate_gate(st, classes, none) != 'NO SUPERADO' or not v.revocation_errors(rev):
                wrong.append(name)
        ok(not wrong, 'S-T02', 'revocation mal formada: NO SUPERADO y una falla (falla cerrado)', f'admitidas: {wrong}')
    attempt('S-T02', 'revocación mal formada', st02)

    def mirrors():
        texts = copy.deepcopy(v.collect(v.ROOT)['texts'])
        ok(v.mirror_errors(texts, 'NO SUPERADO') == [], 'AC-09a',
           'el árbol de la rama: E1–E7 declaran NO SUPERADO y BLOQUEADA, una vez por sujeto',
           str(v.mirror_errors(texts, 'NO SUPERADO')))
        ok(v.mirror_errors(texts, 'SUPERADO') != [], 'AC-09b', 'divergencia: R = SUPERADO con espejos en NO SUPERADO')
        st03 = copy.deepcopy(texts)
        st03[v.GATE_STATE] = json.dumps({**json.loads(st03[v.GATE_STATE]), 'revocation': event(),
                                         'declared_result': 'REVOCADO'})
        ok(v.mirror_errors(st03, 'REVOCADO') != [], 'S-T03', 'revocation válida con espejos E2–E7 en NO SUPERADO: falla')
        dup = copy.deepcopy(texts)
        dup['CLAUDE.md'] = dup['CLAUDE.md'].replace('- F37-SBX = BLOQUEADA\n',
                                                    '- F37-SBX = BLOQUEADA\n\nF36-SBX-GATE = NO SUPERADO de nuevo.\n', 1)
        ok(any('CLAUDE.md' in e for e in v.mirror_errors(dup, 'NO SUPERADO')), 'AC-09c',
           'una segunda afirmación del gate en el bloque de gobierno falla (D-07)')
        up = copy.deepcopy(texts)
        for rel in v.GOV_FILES:
            up[rel] = up[rel].replace('- F36-SBX-GATE = NO SUPERADO', '- F36-SBX-GATE = SUPERADO')
        ok(any(e for e in v.mirror_errors(up, 'NO SUPERADO')), 'AC-09d',
           'espejos en SUPERADO con R = NO SUPERADO: falla (el otro sentido)')
    attempt('AC-09', 'espejos E1–E7', mirrors)

    def required():
        sup, rev = v.required_state('SUPERADO'), v.required_state('REVOCADO')
        ok('F36-SBX-GATE = SUPERADO' in sup and 'F37-SBX = AUTORIZADA PARA INICIAR' in sup and len(sup) == 16
           and 'F36-SBX-GATE = REVOCADO' in rev and 'F37-SBX = BLOQUEADA' in rev
           and v.required_state('NO SUPERADO') == v.REQUIRED_STATE,
           'H-5.4', 'REQUIRED_STATE(R): 14 líneas fijas, el gate con R y F37-SBX derivada (T-02)')
    attempt('H-5.4', 'REQUIRED_STATE(R)', required)

    def vocabulary():
        s = v.collect(v.ROOT)
        s2 = copy.deepcopy(s)
        rel = f'{v.PKG}/F36SBX_Charter.md'
        s2['texts'][rel] = s2['texts'][rel] + '\nF36-SBX-GATE = SUPERADO\n'
        bad = [m for ok_, m in v.rule_sem(s2) if not ok_]
        ok(any('F36-SBX-GATE = SUPERADO' in m for m in bad), 'H-5.3a',
           'fuera de los espejos solo se admite el estado histórico (NO SUPERADO)')
        s3 = copy.deepcopy(s)
        for r in v.GOV_FILES:
            s3['texts'][r] = s3['texts'][r].replace('- F36-SBX-GATE = NO SUPERADO', '- F36-SBX-GATE = SUPERADO')
        sem = [m for ok_, m in v.rule_sem(s3) if not ok_]
        ok(not sem, 'H-5.3b', 'en la línea canónica de un espejo, SEM admite el vocabulario cerrado del gate', str(sem))
        s4 = copy.deepcopy(s)
        for r in v.GOV_FILES:
            s4['texts'][r] = s4['texts'][r].replace('- F36-SBX-GATE = NO SUPERADO', '- F36-SBX-GATE = CASI SUPERADO')
        ok(any(not ok_ for ok_, _ in v.rule_sem(s4)), 'H-5.3c', 'un valor fuera del vocabulario en un espejo falla')
    attempt('H-5.3', 'vocabulario cerrado', vocabulary)

    def fg12():
        st = superado_state()
        next(c for c in st['criteria'] if c['id'] == 'FG-12')['status'] = 'NO APLICA'
        ok(v.evaluate_gate(st, classes, none) == 'SUPERADO', 'S-T09',
           'FG-12 en NO APLICA con FG-03 sin EI CONDITIONAL: admitido (AC-12)')
        st['f37_authorized_ei'] = ['EI-09']
        ok(v.evaluate_gate(st, classes, none) == 'NO SUPERADO', 'S-T10',
           'FG-12 en NO APLICA con una EI CONDITIONAL autorizada: NO SUPERADO')
    attempt('S-T09', 'FG-12 en NO APLICA', fg12)

    ok(v.BASE == 'b8892af39a6492d8dd44a36290604efc602380cd', 'S-T15', 'BASE sin cambios (AC-06)')
    ok(v.BRANCHES == frozenset(CURRENT + [H_BRANCH]), 'S-T17',
       'BRANCHES: exactamente las tres vigentes y la rama de H (AC-07)', str(sorted(v.BRANCHES)))


# ------------------------------------------------------------------------------------------------ con Git real
def sandbox(tmp, name, start=H_BRANCH):
    clone = tmp / name
    tg.git(tmp, 'clone', '-q', '--shared', '--branch', start, str(v.ROOT), str(clone))
    tg.sync_package(clone)
    # H sintético con fecha fija (la de los commits de prueba), para que la fecha del registro sea comparable.
    tg.git(clone, 'commit', '-q', '--allow-empty', '-m', 'H sintético de prueba', env=tg.COMMIT_ENV)
    return clone


def validate(clone):
    v.clear_caches()
    res, gate = v.run(v.collect(clone))
    return [(n, m) for n, ok_, m in res if not ok_], gate


def revoke(clone, h, *, fg14=True, declared=True, determination=True, rev=None, candidate=True):
    """Registro de una revocación posterior a H con el delta de §5.8.2 (y candidate_commit = H, DS-B01-1)."""
    state = json.loads((clone / v.GATE_STATE).read_text(encoding='utf-8'))
    state['revocation'] = event() if rev is None else rev
    if candidate:
        state['candidate_commit'] = h
    if declared:
        state['declared_result'] = 'REVOCADO'
    if fg14:
        next(c for c in state['criteria'] if c['id'] == 'FG-14')['status'] = 'NO CUMPLE'
        doc = (clone / v.GATE_DOC).read_text(encoding='utf-8').split('\n')
        doc = [ln.rsplit('| CUMPLE |', 1)[0] + '| NO CUMPLE |' if ln.startswith('| FG-14 |') else ln for ln in doc]
        tg.write(clone, v.GATE_DOC, '\n'.join(doc))
    tg.write(clone, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    mirrors_to(clone, 'REVOCADO', 'BLOQUEADA')
    if determination:
        tg.write(clone, DETERMINATION, '[SINTÉTICO] Determinación de prueba: no es un acto del equipo.\n')


def mirrors_to(clone, gate, f37):
    """Lleva las líneas canónicas de los espejos E2–E7 al valor indicado, desde cualquier valor previo."""
    for rel in [v.GATE_DOC, f'{v.PKG}/README.md', *v.GOV_FILES]:
        p = clone / rel
        text = p.read_text(encoding='utf-8')
        text = re.sub(r'^- F36-SBX-GATE = [A-ZÁÉÍÓÚÑ ]+$', f'- F36-SBX-GATE = {gate}', text, flags=re.M)
        text = re.sub(r'^- F37-SBX = [A-ZÁÉÍÓÚÑ ]+$', f'- F37-SBX = {f37}', text, flags=re.M)
        tg.write(clone, rel, text)


def check(cid, desc, fails, gate, needles=(), want_gate='NO SUPERADO'):
    if not needles:
        ok(not fails and gate == want_gate, cid, desc,
           f'gate {gate}; fallas: {[f"{n}: {m[:150]}" for n, m in fails][:4]}')
        return
    missing = [x for x in needles if not any(x[0] == n and x[1] in m for n, m in fails)]
    ok(not missing and gate != 'SUPERADO', cid, desc,
       f'gate {gate}; faltan {missing}; fallas {[f"{n}: {m[:150]}" for n, m in fails][:5]}')


def git_cases(tmp):
    clone = sandbox(tmp, 'h')
    h = tg.git(clone, 'rev-parse', 'HEAD')
    fails, gate = validate(clone)
    check('S-T11', 'rama de H desde 55f758e, admitida, con el paquete trasplantado y sin evidencia: 0 fallas, '
          'R = NO SUPERADO (AC-04)', fails, gate)

    tg.write(clone, 'app/Experimental.php', '<?php\n')
    fails, gate = validate(clone)
    check('S-T12', 'S-T11 más una ruta de app/: FRZ falla por alcance y por runtime', fails, gate,
          [('FRZ', 'app/Experimental.php')])
    (clone / 'app/Experimental.php').unlink()

    tg.git(clone, 'checkout', '-q', '-b', 'otra-rama')
    fails, gate = validate(clone)
    check('S-T13', 'el mismo árbol con una rama no admitida: FRZ falla por la rama', fails, gate,
          [('FRZ', 'rama admitida: otra-rama')])
    tg.git(clone, 'checkout', '-q', H_BRANCH)

    dev = tmp / 'dev'
    tg.git(tmp, 'clone', '-q', '--shared', '--branch', 'develop', str(v.ROOT), str(dev))
    tg.git(dev, 'checkout', '-q', '-b', H_BRANCH)
    tg.sync_package(dev)
    fails, gate = validate(dev)
    check('S-T14', 'rama con el nombre de H cortada desde develop: FRZ falla por alcance y runtime; el nombre no basta',
          fails, gate, [('FRZ', 'app/')])

    # H §5.6: un H que ya trae evidencia o espejos adelantados no vale como candidato.
    bad_h = sandbox(tmp, 'h-con-evidencia')
    tg.write(bad_h, v.GATE_EVIDENCE + 'FG-02.json', '{}\n')
    tg.git(bad_h, 'add', '-A')
    early = tg.commit(bad_h, 'H sintético que ya trae evidencia')
    revoke(bad_h, early)
    fails, gate = validate(bad_h)
    check('H-5.6', 'H con gate/evidencia/ dentro: el vínculo falla', fails, gate, [('GATE', 'identidad de H')])

    def fresh(name):
        c = sandbox(tmp, name)
        return c, tg.git(c, 'rev-parse', 'HEAD')

    c, hh = fresh('st18')
    revoke(c, hh)
    check('B01-M04a', 'determinación sin seguimiento en el árbol de trabajo: no vale como registro (S:118)',
          *validate(c), [('GATE', 'no está versionada')])
    tg.git(c, 'add', '-A')
    check('B01-M04b', 'determinación solo preparada en el índice, sin commit: tampoco vale', *validate(c),
          [('GATE', 'no está versionada')])
    tg.commit(c, 'registro sintético de la revocación')
    fails, gate = validate(c)
    check('S-T18', 'revocación después de H con exactamente el delta de §5.8.2 y C-R, versionada en un commit '
          'sucesor de H: R = REVOCADO, 0 fallas', fails, gate, want_gate='REVOCADO')

    c, hh = fresh('st02b')
    revoke(c, hh, rev=event(date='2026-10-01'))
    fails, gate = validate(c)
    ok(gate == 'NO SUPERADO' and any('revocation.date' in m for _, m in fails), 'S-T02b',
       'revocación con fecha anterior a H: falla cerrado, NO SUPERADO y una falla (§5.8.1)',
       f'gate {gate}; fallas {[m[:120] for _, m in fails][:3]}')
    c, hh = fresh('st02c')
    revoke(c, hh, rev=event(evidence=['docs/academico/f36-sbx/NO_EXISTE.md']))
    fails, gate = validate(c)
    ok(gate == 'NO SUPERADO' and any('revocation.evidence' in m for _, m in fails), 'S-T02c',
       'revocación cuya evidencia cita una ruta que no existe en H: falla cerrado',
       f'gate {gate}; fallas {[m[:120] for _, m in fails][:3]}')

    c, hh = fresh('st19a')
    revoke(c, hh)
    commit_all(c, 'registro sintético de la revocación')
    tg.write(c, v.GATE_EVIDENCE + 'OTRO.md', '[SINTÉTICO] extra\n')
    fails, gate = validate(c)
    check('S-T19a', 'S-T18 más un archivo en gate/evidencia/: falla', fails, gate, [('GATE', 'gate/evidencia')])
    ok(gate == 'REVOCADO', 'DS-B01-2', 'interpretación vigente del candidato: con una revocación válida y vinculada, una '
       'falla ajena hace fallar el validador pero R sigue REVOCADO (I-11); S §3 diría NO SUPERADO', f'gate {gate}')
    c, hh = fresh('st19b')
    revoke(c, hh)
    charter = c / f'{v.PKG}/F36SBX_Charter.md'
    tg.write(c, f'{v.PKG}/F36SBX_Charter.md', charter.read_text(encoding='utf-8') + '\nNota posterior.\n')
    check('S-T19b', 'S-T18 más un cambio en otro archivo del paquete: falla el vínculo', *validate(c),
          [('GATE', 'después del commit auditado')])

    c, hh = fresh('st20a')
    revoke(c, hh)
    st = json.loads((c / v.GATE_STATE).read_text(encoding='utf-8'))
    next(x for x in st['criteria'] if x['id'] == 'FG-13')['status'] = 'NO CUMPLE'
    tg.write(c, v.GATE_STATE, json.dumps(st, ensure_ascii=False, indent=2) + '\n')
    check('S-T20a', 'S-T18 más FG-13 en NO CUMPLE: campo fuera del delta', *validate(c), [('GATE', 'fuera del delta')])
    c, hh = fresh('st20b')
    revoke(c, hh, rev=event(note='x'))
    check('S-T20b', 'S-T18 con una clave adicional en revocation: falla el formato', *validate(c),
          [('GATE', 'revocation')])

    c, hh = fresh('st21a')
    st = json.loads((c / v.GATE_STATE).read_text(encoding='utf-8'))
    next(x for x in st['criteria'] if x['id'] == 'FG-14')['status'] = 'NO CUMPLE'
    st['candidate_commit'] = hh
    tg.write(c, v.GATE_STATE, json.dumps(st, ensure_ascii=False, indent=2) + '\n')
    check('S-T21a', 'FG-14 en NO CUMPLE sin revocación: falla', *validate(c), [('GATE', 'FG-14')])
    c, hh = fresh('st21b')
    tg.write(c, DETERMINATION, '[SINTÉTICO] determinación sin evento\n')
    check('S-T21b', 'la determinación sin evento: falla', *validate(c), [('GATE', 'gate/evidencia')])
    c, hh = fresh('st21c')
    revoke(c, hh, rev=event(determination=v.GATE_EVIDENCE + 'OTRA.md'))
    check('S-T21c', 'un evento que cita otra ruta: falla', *validate(c), [('GATE', 'revocation')])
    c, hh = fresh('st21d')
    revoke(c, hh, fg14=False)
    check('S-T21d', 'revocación sin la transición de FG-14 (C-R.4): falla', *validate(c), [('GATE', 'C-R.4')])


def commit_all(clone, msg):
    tg.git(clone, 'add', '-A')
    return tg.commit(clone, msg)


def restore_to(clone, h, keep_candidate):
    """Vuelve el estado, el documento del gate y los espejos a los de H y borra la determinación."""
    tg.git(clone, 'checkout', h, '--', v.GATE_STATE, v.GATE_DOC, v.PKG_README, *v.GOV_FILES)
    if (clone / DETERMINATION).exists():
        (clone / DETERMINATION).unlink()
    if keep_candidate:
        state = json.loads((clone / v.GATE_STATE).read_text(encoding='utf-8'))
        state['candidate_commit'] = h
        tg.write(clone, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')


def git_audit(tmp):
    """Hallazgos del informe de Codex con Git real: permanencia de la revocación (B01-H01) y formato (M01, M02)."""
    def revoked(name):
        c = sandbox(tmp, name)
        hh = tg.git(c, 'rev-parse', 'HEAD')
        revoke(c, hh)
        commit_all(c, 'registro sintético de la revocación')
        return c, hh

    c, hh = revoked('h01a')
    restore_to(c, hh, keep_candidate=True)
    commit_all(c, 'retirada sintética de la revocación, con el mismo H')
    check('B01-H01a', 'revocación válida retirada en un commit posterior con el mismo candidate_commit = H: falla '
          '(I-11, REVOCADO no se deshace)', *validate(c), [('GATE', 'I-11')])

    c, hh = revoked('h01b')
    restore_to(c, hh, keep_candidate=False)
    commit_all(c, 'restauración sintética completa del estado de H')
    check('B01-H01b', 'la misma retirada devolviendo también candidate_commit a nulo: falla', *validate(c),
          [('GATE', 'I-11')])

    c, hh = revoked('h01c')
    restore_to(c, hh, keep_candidate=True)
    check('B01-H01c', 'retirada solo en el árbol de trabajo, sin commit: falla', *validate(c), [('GATE', 'I-11')])

    c, hh = revoked('h01d')
    state = json.loads((c / v.GATE_STATE).read_text(encoding='utf-8'))
    state['revocation'] = event(ground='gate_5_retirada')
    tg.write(c, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    commit_all(c, 'sustitución sintética de la revocación por otra')
    check('B01-H01d', 'una revocación registrada sustituida por otra distinta: falla', *validate(c),
          [('GATE', 'I-11')])

    for cid, value in (('B01-M01g', '2026-99-99T99:99:99+99:99'),):
        c = sandbox(tmp, 'm01')
        hh = tg.git(c, 'rev-parse', 'HEAD')
        revoke(c, hh, rev=event(effective_from=value))
        commit_all(c, 'registro sintético con un instante imposible')
        fails, gate = validate(c)
        ok(gate == 'NO SUPERADO' and any('effective_from' in m for _, m in fails), cid,
           f'instante imposible {value} versionado: NO SUPERADO y una falla', f'gate {gate}; {[m[:100] for _, m in fails][:3]}')

    for cid, ground in (('B01-M02g', []), ('B01-M02h', {})):
        c = sandbox(tmp, f'm02-{cid[-1]}')
        hh = tg.git(c, 'rev-parse', 'HEAD')
        revoke(c, hh, rev=event(ground=ground))
        commit_all(c, 'registro sintético con ground mal tipado')
        try:
            fails, gate = validate(c)
            ok(gate == 'NO SUPERADO' and any('revocation.ground' in m for _, m in fails), cid,
               f'ground = {ground!r} en el validador completo: resultado estructurado, NO SUPERADO y una falla',
               f'gate {gate}; {[m[:100] for _, m in fails][:3]}')
        except Exception as e:  # noqa: BLE001
            ok(False, cid, f'ground = {ground!r} en el validador completo', f'excepción {e.__class__.__name__}: {e}')


def superado(clone, h):
    """Registro SINTÉTICO completo de SUPERADO: FG-02 con su informe, FG-03 (solo EI ALLOWED), FG-10 sin dependencias y
    FG-12 en NO APLICA; espejos en SUPERADO y F37-SBX derivada. No son actos del equipo: solo existen en el clon."""
    import test_f36sbx as tm
    docs = tm.evidence_docs(['EI-01'])
    for fg in ('FG-02', 'FG-03', 'FG-10'):
        docs[fg]['candidate_commit'] = h
    report = tm.doc_bytes(tm.REPORT_PROSE, 'f36sbx-audit-metadata', tm.report_meta(docs['FG-02']))
    docs['FG-02']['audit_report']['sha256'] = v.sha256(report)
    tg.write(clone, tm.REPORT, report)
    for fg in ('FG-02', 'FG-03', 'FG-10'):
        tg.write(clone, f'{v.GATE_EVIDENCE}{fg}.json', json.dumps(docs[fg], ensure_ascii=False, indent=2) + '\n')
    state = json.loads((clone / v.GATE_STATE).read_text(encoding='utf-8'))
    state['candidate_commit'] = h
    state['f37_authorized_ei'] = ['EI-01']
    state['declared_result'] = 'SUPERADO'
    for c in state['criteria']:
        if c['id'] in ('FG-02', 'FG-03', 'FG-10'):
            c['status'], c['evidence'] = 'CUMPLE', f'{v.GATE_EVIDENCE}{c["id"]}.json'
        elif c['id'] == 'FG-12':
            c['status'], c['evidence'] = 'NO APLICA', None
    tg.write(clone, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    doc = (clone / v.GATE_DOC).read_text(encoding='utf-8').split('\n')
    rows = {'FG-02': 'CUMPLE', 'FG-03': 'CUMPLE', 'FG-10': 'CUMPLE', 'FG-12': 'NO APLICA'}
    doc = [ln.rsplit('| PENDIENTE |', 1)[0] + f'| {rows[ln[2:7]]} |' if ln[2:7] in rows and ln.startswith('| FG-')
           else ln for ln in doc]
    tg.write(clone, v.GATE_DOC, '\n'.join(doc))
    mirrors_to(clone, 'SUPERADO', v.F37_ENABLED)


def superado_integral(tmp):
    """DS-B01-3: control positivo SUPERADO con Git real, divergencias de espejo en los dos sentidos y después
    SUPERADO → REVOCADO → intento de retirada."""
    c = sandbox(tmp, 'superado')
    h = tg.git(c, 'rev-parse', 'HEAD')
    superado(c, h)
    commit_all(c, 'registro sintético completo de SUPERADO')
    check('DS-B01-3a', 'SUPERADO integral con Git real: FG-02, FG-03, FG-10 y FG-12 (NO APLICA) coherentes, espejos '
          'en SUPERADO y F37-SBX = AUTORIZADA PARA INICIAR: 0 fallas', *validate(c), want_gate='SUPERADO')

    gov = c / v.GOV_FILES[0]
    tg.write(c, v.GOV_FILES[0], gov.read_text(encoding='utf-8').replace('- F36-SBX-GATE = SUPERADO\n',
                                                                        '- F36-SBX-GATE = NO SUPERADO\n'))
    fails, gate = validate(c)
    ok(any('espejos E1–E7' in m for _, m in fails), 'DS-B01-3b',
       'evidencia de SUPERADO con un espejo de gobierno en NO SUPERADO: falla', f'gate {gate}')
    tg.git(c, 'checkout', '--', v.GOV_FILES[0])

    (c / f'{v.GATE_EVIDENCE}FG-03.json').unlink()
    fails, gate = validate(c)
    ok(gate == 'NO SUPERADO' and any('espejos E1–E7' in m for _, m in fails), 'DS-B01-3c',
       'espejos en SUPERADO sin la evidencia de FG-03: NO SUPERADO y falla de espejos', f'gate {gate}')
    tg.git(c, 'checkout', '--', f'{v.GATE_EVIDENCE}FG-03.json')

    revoke(c, h)
    commit_all(c, 'revocación sintética posterior a SUPERADO')
    check('DS-B01-3d', 'SUPERADO → REVOCADO con la unión de deltas: R = REVOCADO, 0 fallas', *validate(c),
          want_gate='REVOCADO')

    state = json.loads((c / v.GATE_STATE).read_text(encoding='utf-8'))
    state['revocation'], state['declared_result'] = None, 'SUPERADO'
    next(x for x in state['criteria'] if x['id'] == 'FG-14')['status'] = 'CUMPLE'
    tg.write(c, v.GATE_STATE, json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    doc = (c / v.GATE_DOC).read_text(encoding='utf-8')
    tg.write(c, v.GATE_DOC, '\n'.join(ln.rsplit('| NO CUMPLE |', 1)[0] + '| CUMPLE |' if ln.startswith('| FG-14 |')
                                      else ln for ln in doc.split('\n')))
    (c / DETERMINATION).unlink()
    for rel in [v.GATE_DOC, v.PKG_README, *v.GOV_FILES]:
        p = c / rel
        txt = p.read_text(encoding='utf-8').replace('- F36-SBX-GATE = REVOCADO\n', '- F36-SBX-GATE = SUPERADO\n')
        tg.write(c, rel, txt.replace('- F37-SBX = BLOQUEADA\n', f'- F37-SBX = {v.F37_ENABLED}\n'))
    commit_all(c, 'intento sintético de retirar la revocación y volver a SUPERADO')
    fails, gate = validate(c)
    ok(gate != 'SUPERADO' and any('I-11' in m for _, m in fails), 'DS-B01-3e',
       'SUPERADO → REVOCADO → retirada para volver a SUPERADO: falla y no habilita F37-SBX', f'gate {gate}; '
       f'{[m[:100] for _, m in fails][:3]}')


def memory_audit():
    """Hallazgos B01-M01, B01-M02 y B01-M03 en memoria."""
    def m01():
        bad = ['2026-99-99T99:99:99+99:99', '2026-13-01T00:00:00-05:00', '2026-02-30T10:00:00-05:00',
               '2026-11-11T25:00:00-05:00', '2026-11-11T10:61:00-05:00', '2026-11-11T10:00:00+24:00']
        admitted = [x for x in bad if not any('effective_from' in e for e in v.revocation_errors(event(effective_from=x)))]
        ok(not admitted, 'B01-M01', 'effective_from con mes, día, hora, minuto u desfase imposibles: formato inválido',
           f'admitidos: {admitted}')
        ok(v.revocation_errors(event(effective_from='2020-01-01T00:00:00-05:00')) == [], 'B01-M01b',
           'un instante válido anterior al registro y a H se admite: el validador no juzga el efecto histórico')
    attempt('B01-M01', 'instantes imposibles', m01)

    def m02():
        broken = []
        for key, value in (('ground', []), ('ground', {}), ('ground', 3), ('ground', None), ('determination', []),
                           ('date', ['2026-11-11']), ('effective_from', {}), ('evidence', {'a': 1}),
                           ('evidence', [['x']])):
            try:
                errs = v.revocation_errors(event(**{key: value}))
                st = gate_state()
                st['revocation'] = event(**{key: value})
                if not any(key in e for e in errs) or v.evaluate_gate(st, v.EXPECTED_CLASSES, lambda fg: []) != 'NO SUPERADO':
                    broken.append(f'{key}={value!r}: admitido')
            except Exception as e:  # noqa: BLE001
                broken.append(f'{key}={value!r}: {e.__class__.__name__}')
        ok(not broken, 'B01-M02', 'claves de revocation con tipos compuestos, número o nulo: diagnóstico y NO SUPERADO, '
           'sin excepción', str(broken))
    attempt('B01-M02', 'tipos de revocation', m02)

    def m03():
        s = v.collect(v.ROOT)
        for state in ('SUPERADO', 'REVOCADO'):
            f37 = v.F37_ENABLED if state == 'SUPERADO' else 'BLOQUEADA'
            for rel, label in ((v.PKG_README, 'README'), (v.GATE_DOC, 'gate')):
                s2 = copy.deepcopy(s)
                for r in [v.GATE_DOC, v.PKG_README, *v.GOV_FILES]:
                    s2['texts'][r] = s2['texts'][r].replace('- F36-SBX-GATE = NO SUPERADO\n', f'- F36-SBX-GATE = {state}\n') \
                        .replace('- F37-SBX = BLOQUEADA\n', f'- F37-SBX = {f37}\n')
                inside = [m for ok_, m in v.rule_sem(s2) if not ok_]
                s2['texts'][rel] = s2['texts'][rel] + f'\n## Nota ajena al espejo\n\nF36-SBX-GATE = {state}\n'
                outside = [m for ok_, m in v.rule_sem(s2) if not ok_]
                ok(not inside and any(f'F36-SBX-GATE = {state}' in m for m in outside), f'B01-M03-{label}-{state}',
                   f'«F36-SBX-GATE = {state}»: admitida en la línea canónica del espejo y rechazada fuera de su ámbito '
                   f'({label})', f'dentro: {inside}; fuera: {outside}')
    attempt('B01-M03', 'excepción SEM por ubicación', m03)


def inventory():
    """S-T22 y AC-05 sobre el árbol real de la rama: inventario frente a 55f758e y sondas ejecutables desde H."""
    allowed = (v.PKG + '/', v.TOOLS + '/')
    out = subprocess.run(['git', 'diff', '--name-only', MAIN_AF5, 'HEAD'], cwd=v.ROOT, capture_output=True, text=True)
    paths = out.stdout.split()
    outside = [p for p in paths if not (p.startswith(allowed) or p in v.GOV_FILES)]
    probes = [p for p in paths if '/expediente-final/sondas-b01/' in p]
    ok(out.returncode == 0 and paths and not outside and len(probes) == 4, 'S-T22a',
       f'git diff --name-only 55f758e HEAD cabe en AC-05 ({len(paths)} rutas) e incluye las 4 piezas de sondas-b01/',
       f'fuera: {outside}; sondas: {len(probes)}')
    ok(not any(p.startswith(v.GATE_EVIDENCE) for p in paths) and not (v.ROOT / v.GATE_EVIDENCE).exists(), 'AC-11',
       'ningún control positivo persiste: gate/evidencia/ no existe en la rama')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    before = tuple(v.git(v.ROOT, *a)[1] for a in (('rev-parse', 'HEAD'), ('status', '--porcelain', '--ignored')))
    memory()
    memory_audit()
    tmp = Path(tempfile.mkdtemp(prefix='f36sbx-b01-'))
    try:
        attempt('GIT', 'casos con Git real', lambda: git_cases(tmp))
        attempt('GIT-AUD', 'hallazgos de la auditoría con Git real', lambda: git_audit(tmp))
        attempt('DS-B01-3', 'SUPERADO integral con Git real', lambda: superado_integral(tmp))
    finally:
        tg.remove_tree(tmp)
    attempt('S-T22', 'inventario de la rama', inventory)
    after = tuple(v.git(v.ROOT, *a)[1] for a in (('rev-parse', 'HEAD'), ('status', '--porcelain', '--ignored')))
    ok(before == after, 'R00', 'el repositorio original no cambió (HEAD y estado, también de ignorados)')
    bad = [r for r in results if not r[0]]
    for ok_, cid, desc, detail in results:
        print(f'{"OK   " if ok_ else "FALLA"} {cid} {desc}: {detail}')
    print(f'test_f36sbx_b01: {len(results) - len(bad)} casos correctos, {len(bad)} fallas')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
