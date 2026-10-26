#!/usr/bin/env python3
"""Pruebas negativas y mutantes de validate_f36sbx.py.

Todo ocurre en memoria, sobre una copia de la fotografía del repositorio: no se escribe ningún archivo.
Cada mutante debe hacer fallar la regla indicada; si la mutación ya no se puede aplicar, la prueba falla.

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
C, S, CH = v.CONTRACT, v.GATE_STATE, v.PKG + '/F36SBX_Charter.md'
PR = v.PKG + '/README.md'
CE = v.PKG + '/F36SBX_Contrato_Evidencia.md'

results = []


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


def case(cid, desc, mutation, rule):
    snap = copy.deepcopy(BASE)
    try:
        mutation(snap)
    except AssertionError as e:
        results.append((False, cid, desc, f'mutación no aplicable: {e}'))
        return
    res, _ = v.run(snap)
    fails = sorted({n for n, ok, _ in res if not ok})
    ok = rule in fails
    results.append((ok, cid, desc, f'falla {rule}' if ok else f'esperaba FALLA {rule}; fallaron {fails}'))


def gate_case(cid, desc, state_fn, expected, classes=None, exists=lambda p: True):
    state = json.loads(BASE['texts'][S])
    state_fn(state)
    got = v.evaluate_gate(state, classes or CLASSES, exists)
    results.append((got == expected, cid, desc, f'{got}' if got == expected else f'esperaba {expected}; dio {got}'))


def all_cumple(state, auth=('EI-01', 'EI-07')):
    for c in state['criteria']:
        c['status'] = 'CUMPLE'
        if c['kind'] == 'team':
            c['evidence'] = v.GATE_EVIDENCE + c['id'] + '.md'
    state['f37_authorized_ei'] = list(auth)


def crit(state, fg):
    return next(c for c in state['criteria'] if c['id'] == fg)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    # T00 · control: el repositorio real pasa y el gate da NO SUPERADO.
    res, gate = v.run(copy.deepcopy(BASE))
    fails = [f'{n}: {m}' for n, ok, m in res if not ok]
    results.append((not fails and gate == 'NO SUPERADO', 'T00', 'control: repositorio real sin fallas y gate NO SUPERADO',
                    f'gate {gate}' if not fails else f'fallas reales: {fails}'))

    nbh = '‑'  # guion no separable: variante tipográfica
    # Gobierno y afirmaciones de estado.
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
    case('M11', 'F37-SBX habilitada escondida con negritas',
         sub(CH, '**F37-SBX = BLOQUEADA**', '**F37-SBX** = HABILITADA'), 'SEM')
    case('M12', 'F37-SBX habilitada con dos puntos', sub(PR, '**F37-SBX = BLOQUEADA.**', '**F37-SBX: HABILITADA.**'), 'SEM')
    # Matriz de capacidades.
    case('M13', 'EI-19 (scoring y ranking) pasa a ALLOWED',
         sub(M, '| **BLOCKED** | — | CAP-15, CAP-16, CAP-17 |', '| **ALLOWED** | B | CAP-15, CAP-16, CAP-17 |'), 'CAP')
    case('M14', 'EI-10 (embeddings) pasa a ALLOWED',
         sub(M, '| **CONDITIONAL** | C | CAP-09, CAP-20 |', '| **ALLOWED** | C | CAP-09, CAP-20 |'), 'CAP')
    case('M15', 'OCR pasa a CONDITIONAL', sub(M, '| OCR | **BLOCKED** | C |', '| OCR | **CONDITIONAL** | C |'), 'CAP')
    case('M16', 'desaparece EI-20 (inferencias prohibidas)', drop_line(M, '| EI-20 |'), 'CAP')
    case('M17', 'el resumen no coincide con las filas', sub(M, 'EI-06, EI-07 |', 'EI-06 |'), 'CAP')
    case('M18', 'EI-01 cita una CAP inexistente', sub(M, '| CAP-04, CAP-06 |', '| CAP-99, CAP-06 |'), 'CAP')
    case('M19', 'EI-04 ALLOWED cita CAP-10 BLOQUEADA', sub(M, '| CAP-13 |', '| CAP-13, CAP-10 |'), 'CAP')
    case('M20', 'capacidad ALLOWED que usa embeddings', sub(M, 'Búsqueda léxica exacta', 'Búsqueda con embeddings'), 'CAP')
    case('M21', 'EI-08 de alcance C pasa a ALLOWED',
         sub(M, '| **CONDITIONAL** | C | CAP-07 | Es extracción', '| **ALLOWED** | C | CAP-07 | Es extracción'), 'CAP')
    # Contrato de evidencia.
    case('M22', 'el generador admite LLM', jmut(C, lambda d: d['generator_policy'].update(llm_allowed=True)), 'CTR')
    case('M23', 'se admite source_type real', jmut(C, lambda d: d['source_type_allowed'].append('real')), 'CTR')
    case('M24', 'gender deja de estar prohibido', jmut(C, lambda d: d['forbidden_fields'].remove('gender')), 'CTR')
    case('M25', 'un CV declara un campo score',
         jmut(C, lambda d: d['artifact_types']['cv_document']['fields'].append('score')), 'CTR')
    case('M26', 'grupo_sintetico dentro de una observación',
         jmut(C, lambda d: d['artifact_types']['human_observation']['fields'].append('grupo_sintetico')), 'CTR')
    case('M27', 'se admite un conjunto de entrenamiento', jmut(C, lambda d: d['splits'].update(train_allowed=True)), 'CTR')
    case('M28', 'clave duplicada en el contrato',
         sub(C, '"contract_version": "1",', '"contract_version": "1",\n  "contract_version": "2",'), 'CTR')
    case('M29', 'clave nueva fuera del esquema cerrado', jmut(C, lambda d: d.update(real_data_allowed=False)), 'CTR')
    case('M30', 'los adjuntos de gobierno como fuente admitida',
         jmut(C, lambda d: d['allowed_upstream_sources'].append('docs/academico/g0-evidence')), 'CTR')
    case('M31', 'prefijo de marcador cambiado',
         jmut(C, lambda d: d['synthetic_markers'].update(synthetic_id_prefix='SBXE-')), 'CTR')
    case('M32', 'una observación puede tener autor sistema',
         jmut(C, lambda d: d['closed_values']['author_kind'].append('system')), 'CTR')
    # Threat model y plan de evaluación.
    case('M33', 'desaparece TEI-11 (abstención)', drop_line(T, '| TEI-11 |'), 'THR')
    case('M34', 'TEI-02 sin comportamiento fail-closed', sub(T, '| Un manifiesto con texto libre es inválido |', '| — |'), 'THR')
    case('M35', 'se pierde el tema de inyección',
         sub(T, 'Prompt injection o document injection', 'Instrucciones incrustadas'), 'THR')
    case('M36', 'el plan inventa un resultado',
         sub(R, '**No hay resultados.**', 'Resultados preliminares: Recall@5 = 0,81.'), 'EVA')
    case('M37', 'desaparece M-07', drop_line(R, '| M-07 |'), 'EVA')
    case('M38', 'una EI BLOCKED recibe métrica', sub(R, '| M-11 | Toda salida |', '| M-11 | Toda salida, EI-13 |'), 'EVA')
    # Estado del gate.
    case('M39', 'el JSON declara SUPERADO', jmut(S, lambda d: d.update(declared_result='SUPERADO')), 'GATE')
    case('M40', 'FG-02 en CUMPLE sin evidencia',
         jmut(S, lambda d: crit(d, 'FG-02').update(status='CUMPLE')), 'GATE')
    case('M41', 'el gate autoriza producción', jmut(S, lambda d: d['authorizes'].append('produccion')), 'GATE')
    case('M42', 'el gate deja de excluir los datos reales',
         jmut(S, lambda d: d['cannot_authorize'].remove('datos_reales')), 'GATE')
    case('M43', 'revocación no reflejada en el resultado',
         jmut(S, lambda d: d.update(revocation={'fecha': '2026-10-26', 'motivo': 'prueba'})), 'GATE')
    case('M44', 'FG-02 se disfraza de AUTO', jmut(S, lambda d: crit(d, 'FG-02').update(kind='auto')), 'GATE')
    case('M45', 'base equivocada', jmut(S, lambda d: d.update(base_commit='0' * 40)), 'GATE')
    case('M46', 'FG-04 declarado distinto del recalculado',
         jmut(S, lambda d: crit(d, 'FG-04').update(status='NO CUMPLE')), 'GATE')
    case('M47', 'clave duplicada en el estado del gate',
         sub(S, '"gate_version": "1",', '"gate_version": "1",\n  "gate_version": "2",'), 'GATE')
    case('M48', 'la autorización de F37-SBX lista una EI BLOCKED',
         jmut(S, lambda d: d.update(f37_authorized_ei=['EI-01', 'EI-19'])), 'GATE')
    case('M49', 'tabla FG del documento distinta del JSON',
         sub(G, '| Regla FRZ | CUMPLE |', '| Regla FRZ | PENDIENTE |'), 'GATE')
    case('M50', 'AUTO declarado CUMPLE con el gobierno roto',
         sub('CLAUDE.md', '- F36-SBX-GATE = NO SUPERADO\n', ''), 'GATE')
    # Alcance Git, runtime, F35-SBX y dependencias.
    case('M51', 'cambio en app/', add_changed('app/Models/Vacancy.php'), 'FRZ')
    case('M52', 'cambio en F35-SBX congelada', add_changed('docs/academico/evidencia-sbx/README.md'), 'FRZ')
    case('M53', 'cambio en composer.json', add_changed('composer.json'), 'FRZ')
    case('M54', 'cambio en las dependencias de ml-service', add_changed('ml-service/pyproject.toml'), 'FRZ')
    case('M55', 'cambio en la deuda técnica', add_changed('docs/academico/TECHNICAL_DEBT.md'), 'FRZ')
    case('M56', 'cambio en el gate congelado de F35-SBX',
         add_changed('docs/academico/tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py'), 'FRZ')
    case('M57', 'cambio en una migración', add_changed('database/migrations/2026_10_26_000000_x.php'), 'FRZ')
    case('M58', 'rama no admitida', setkey('branch', 'feature/otra'), 'FRZ')
    case('M59', 'la base no es ancestro', setkey('base_ok', False), 'FRZ')
    case('M60', 'estado Git desconocido', setkey('changed', None), 'FRZ')
    case('M61', 'el validador importa torch', append_tool('\nimport torch\n'), 'DEP')
    case('M62', 'el validador importa requests', append_tool('\nimport requests\n'), 'DEP')
    case('M63', 'un script nuevo importa sentence_transformers',
         add_tool(v.TOOLS + '/localizador.py', 'from sentence_transformers import SentenceTransformer\n'), 'DEP')
    # PII, enlaces y estructura.
    case('M64', 'correo en el contrato', sub(CE, '## 1. Principios', '## 1. Principios\n\nContacto: persona' + '@' + 'colegio.pe'), 'PII')
    case('M65', 'número de DNI en el charter', sub(CH, '## 3. Problema', 'DNI ' + '4' + '1234567' + '\n\n## 3. Problema'), 'PII')
    case('M66', 'enlace roto', sub(PR, '](F36SBX_Charter.md)', '](F36SBX_Charter_x.md)'), 'LNK')
    case('M67', 'ancla rota', sub(M, '(F36SBX_Charter.md#7-revocación)', '(F36SBX_Charter.md#7-revocacion)'), 'LNK')
    case('M68', 'falta el threat model', lambda s: s['texts'].update({T: None}), 'STR')

    # Regla de decisión del gate, con estados en memoria. Ningún estado positivo se escribe en disco.
    gate_case('G01', 'estado real → NO SUPERADO', lambda s: None, 'NO SUPERADO')
    gate_case('G02', 'control positivo en memoria: todo CUMPLE y solo EI ALLOWED → SUPERADO', all_cumple, 'SUPERADO')
    gate_case('G03', 'autoriza EI-19 BLOCKED → NO SUPERADO', lambda s: all_cumple(s, ('EI-01', 'EI-19')), 'NO SUPERADO')
    gate_case('G04', 'autoriza una EI inexistente → NO SUPERADO', lambda s: all_cumple(s, ('EI-99',)), 'NO SUPERADO')

    def na_with_conditional(s):
        all_cumple(s, ('EI-01', 'EI-10'))
        crit(s, 'FG-12')['status'] = 'NO APLICA'
    gate_case('G05', 'EI-10 CONDITIONAL con FG-12 NO APLICA → NO SUPERADO', na_with_conditional, 'NO SUPERADO')

    def na_allowed_only(s):
        all_cumple(s)
        crit(s, 'FG-10')['status'] = 'NO APLICA'
        crit(s, 'FG-12')['status'] = 'NO APLICA'
    gate_case('G06', 'solo EI ALLOWED con FG-10 y FG-12 NO APLICA → SUPERADO', na_allowed_only, 'SUPERADO')

    def na_on_audit(s):
        all_cumple(s)
        crit(s, 'FG-02')['status'] = 'NO APLICA'
    gate_case('G07', 'NO APLICA en la auditoría FG-02 → NO SUPERADO', na_on_audit, 'NO SUPERADO')

    def unknown_status(s):
        all_cumple(s)
        crit(s, 'FG-03')['status'] = 'APROBADO'
    gate_case('G08', 'estado desconocido → NO SUPERADO', unknown_status, 'NO SUPERADO')
    gate_case('G09', 'evidencia inexistente → NO SUPERADO', all_cumple, 'NO SUPERADO', exists=lambda p: False)
    results.append((not v.evidence_ok(BASE['root'], '../../../CLAUDE.md')
                    and not v.evidence_ok(BASE['root'], v.GATE_EVIDENCE + '../../README.md')
                    and not v.evidence_ok(BASE['root'], None), 'G18',
                    'evidence_ok rechaza rutas fuera de gate/evidencia, con salida de directorio o nulas', 'fail-closed'))
    gate_case('G10', 'evidencia fuera de gate/evidencia → NO SUPERADO', all_cumple, 'NO SUPERADO',
              exists=lambda p: v.evidence_ok(BASE['root'], '../../../CLAUDE.md'))

    def revoked(s):
        all_cumple(s)
        s['revocation'] = {'fecha': '2026-10-26', 'motivo': 'prueba'}
    gate_case('G11', 'revocación con todo CUMPLE → REVOCADO', revoked, 'REVOCADO')

    def no_auth(s):
        all_cumple(s)
        s['f37_authorized_ei'] = None
    gate_case('G12', 'FG-03 CUMPLE sin lista de EI → NO SUPERADO', no_auth, 'NO SUPERADO')

    def prod(s):
        all_cumple(s)
        s['authorizes'] = ['F37-SBX', 'produccion']
    gate_case('G13', 'autoriza producción → NO SUPERADO', prod, 'NO SUPERADO')

    def missing_fg(s):
        all_cumple(s)
        s['criteria'] = s['criteria'][:-1]
    gate_case('G14', 'falta FG-14 → NO SUPERADO', missing_fg, 'NO SUPERADO')
    results.append((v.evaluate_gate(None, CLASSES, lambda p: True) == 'NO SUPERADO', 'G15',
                    'estado no legible → NO SUPERADO', 'fail-closed'))

    def dup_auth(s):
        all_cumple(s, ('EI-01', 'EI-01'))
    gate_case('G16', 'EI repetida en la autorización → NO SUPERADO', dup_auth, 'NO SUPERADO')
    gate_case('G17', 'evidencia con salida de directorio → rechazada', all_cumple, 'NO SUPERADO',
              exists=lambda p: v.evidence_ok(BASE['root'], v.GATE_EVIDENCE + '../gate/../../README.md'))

    bad = [r for r in results if not r[0]]
    for ok, cid, desc, detail in results:
        print(f'{"OK   " if ok else "FALLA"} {cid} {desc}: {detail}')
    print(f'test_f36sbx: {len(results) - len(bad)} casos correctos, {len(bad)} fallas')
    return 1 if bad else 0


BASE = v.collect(v.ROOT)
CLASSES = v.matrix_classes(BASE)

if __name__ == '__main__':
    sys.exit(main())
