"""Validación de coherencia F2 → F9 (encargo F27B §17) y de integridad de los DOCX.

Uso: python docs/academico/tools/f27b/validate.py
Devuelve una lista de (regla, resultado, detalle) y sale con código 1 si alguna regla falla.
"""
import glob
import os
import re
import sys
import zipfile
import xml.dom.minidom

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
ACAD = os.path.join(ROOT, 'docs', 'academico')

import m_asis as A  # noqa: E402
import m_problems as PR  # noqa: E402
import m_tobe as T  # noqa: E402
import m_rf as R  # noqa: E402
import m_rnf as N  # noqa: E402
import m_cu as U  # noqa: E402

BASE_RF = [f'RF-{i:02d}' for i in range(1, 28)]


def f9_rf_cu():
    """RF → CU y bloque IN, leídos del F9 v1.1 publicado (tabla de la línea base funcional)."""
    path = os.path.join(ACAD, 'phase-24', 'output', 'F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx')
    doc = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
    out = {}
    for row in re.findall(r'<w:tr[ >].*?</w:tr>', doc, re.S):
        cells = [''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', c)) for c in re.findall(r'<w:tc>.*?</w:tc>', row, re.S)]
        if len(cells) == 5 and re.fullmatch(r'RF-\d\d', cells[0]) and cells[3].startswith('CU-'):
            out[cells[0]] = (cells[3], cells[4])
    return out


def checks():
    res = []

    def check(rule, ok, detail=''):
        res.append((rule, 'OK' if ok else 'FALLA', detail))

    as_ids = {a[0] for a in A.ACTIVIDADES}
    # F2 → F3: actividades con actor y ubicadas en el BPMN
    sin_actor = [a[0] for a in A.ACTIVIDADES if not any(r in ('Ejecuta', 'Valida') for _, r in a[4])]
    check('F2: toda actividad AS-IS tiene un actor que la ejecuta o valida', not sin_actor, ', '.join(sin_actor))
    # F3 → F4: problemas con actividad; coherencia bidireccional de etiquetas
    sin_act = [p['id'] for p in PR.PROBLEMAS if not p['actividades'] or not set(p['actividades']) <= as_ids]
    check('F4: todo problema tiene actividades AS-IS existentes', not sin_act, ', '.join(sin_act))
    tags = {(a[0], p) for a in A.ACTIVIDADES for p in a[5]}
    rel = {(x, p['id']) for p in PR.PROBLEMAS for x in p['actividades']}
    check('F2 ↔ F4: las etiquetas de problema de las actividades coinciden con F4', tags == rel,
          f'solo en F2: {sorted(tags - rel)}; solo en F4: {sorted(rel - tags)}' if tags != rel else '')
    obs = {o[2] for o in A.OBSERVACIONES if o[2].startswith('P') and ',' not in o[2]}
    check('F2 ↔ F4: cada problema P1–P5 tiene una observación en F2', obs >= {p['id'] for p in PR.PROBLEMAS})
    # F4 → F5
    pids = {p['id'] for p in PR.PROBLEMAS}
    sol_p = {s[0] for s in T.SOLUCIONES}
    check('F5: toda solución responde a un problema de F4', sol_p <= pids)
    check('F5: todo problema de F4 tiene solución', pids <= sol_p, ', '.join(sorted(pids - sol_p)))
    tb_ids = {t[0] for t in T.ACTIVIDADES}
    bad_tb = [s[1] for s in T.SOLUCIONES if not set(s[4]) <= tb_ids]
    check('F5: las actividades de cada solución existen en el TO-BE', not bad_tb, ', '.join(bad_tb))
    sin_actor_tb = [t[0] for t in T.ACTIVIDADES + T.FUTURAS if not t[4]]
    check('F5: toda actividad TO-BE tiene actor', not sin_actor_tb, ', '.join(sin_actor_tb))
    as_sin_tb = sorted(as_ids - {o for t in T.ACTIVIDADES for o in t[6]})
    check('F2 → F5: toda actividad AS-IS tiene continuidad en el TO-BE', not as_sin_tb, ', '.join(as_sin_tb))
    # Solución ↔ RF de la solución coherente con las actividades
    incoh = []
    for s in T.SOLUCIONES:
        rf_tb = {r for t in T.ACTIVIDADES if t[0] in s[4] for r in t[5]}
        if not set(s[5]) <= rf_tb:
            incoh.append(f'{s[1]}: {sorted(set(s[5]) - rf_tb)}')
    check('F5: los RF de cada solución están soportados por sus actividades TO-BE', not incoh, '; '.join(incoh))
    # F5 → F6
    rf_in_tb = {r for t in T.ACTIVIDADES for r in t[5]}
    check('F6: todo RF-01..RF-27 tiene actividad TO-BE', set(BASE_RF) <= rf_in_tb, ', '.join(sorted(set(BASE_RF) - rf_in_tb)))
    check('F6: el TO-BE no usa RF fuera de la línea base', rf_in_tb <= set(BASE_RF), ', '.join(sorted(rf_in_tb - set(BASE_RF))))
    check('F6: hay exactamente 27 fichas, en orden y sin duplicados', [r[0] for r in R.RF] == BASE_RF)
    ficha_tb = [r[0] for r in R.RF if not set(r[11]) <= tb_ids or
                any(r[0] not in dict((t[0], t[5]) for t in T.ACTIVIDADES)[x] for x in r[11])]
    check('F6 ↔ F5: la actividad TO-BE de cada ficha contiene ese RF', not ficha_tb, ', '.join(ficha_tb))
    check('F6: todo RF tiene actor', all(r[3] for r in R.RF))
    check('F6: RF-28 y RF-29 solo están en extensiones', {e[0] for e in R.EXTENSIONES} == {'RF-28', 'RF-29'} and
          not any(r[0] in ('RF-28', 'RF-29') for r in R.RF))
    rf23 = next(r for r in R.RF if r[0] == 'RF-23')
    check('F6: RF-23 es una decisión humana del Aprobador / Dirección', 'Aprobador / Dirección' == rf23[3] and 'humana' in rf23[2])
    # F6 → F7
    check('F7: hay 10 RNF académicos, cada uno con método de verificación y estado',
          len(N.RNF) == 10 and all(x[7] and x[8] for x in N.RNF))
    check('F7: los estados usan solo el vocabulario permitido',
          {x[8] for x in N.RNF} <= {'VERIFICADO', 'EVIDENCIA PARCIAL', 'NO VERIFICADO', 'PROPUESTO'})
    check('F7: RNF-C figura solo como propuesta', all(c[2] == 'PROPUESTO' for c in N.CANDIDATOS if c[0] == 'RNF-C'))
    # F6 → F8
    rf_cu = {r for c in U.CU for r in c[4]}
    check('F8: todo RF-01..RF-27 está en algún CU', set(BASE_RF) <= rf_cu, ', '.join(sorted(set(BASE_RF) - rf_cu)))
    check('F8: ningún CU usa RF fuera de la línea base', rf_cu <= set(BASE_RF))
    inc = {i[1] for i in U.INCLUDES}
    sin_actor_cu = [c[0] for c in U.CU if not c[3] and c[0] not in inc]
    check('F8: todo CU tiene actor directo o es un caso incluido', not sin_actor_cu, ', '.join(sin_actor_cu))
    check('F8: todo CU tiene RF', all(c[4] for c in U.CU))
    check('F8: hay 20 CU académicos (CU-01..CU-20)', [c[0] for c in U.CU] == [f'CU-{i:02d}' for i in range(1, 21)])
    # F8 → F9
    f9 = f9_rf_cu()
    check('F9: se leyó la tabla RF → CU del F9 publicado (27 filas)', len(f9) == 27, str(len(f9)))
    div = []
    for rf, (cu9, in9) in f9.items():
        mine = [c for c in U.CU if rf in c[4]]
        cus = {c[0] for c in mine}
        if not any(x.strip() in cus for x in re.split(r'[,y]', cu9.replace('Incluido en', ''))):
            div.append(f'{rf}: F9 {cu9} / F8 {sorted(cus)}')
        if not any(in9 in c[7] for c in mine):
            div.append(f'{rf}: bloque F9 {in9}')
    check('F8 ↔ F9: la relación RF → CU → bloque IN coincide con el F9 publicado', not div, '; '.join(div))
    # Afirmaciones institucionales
    flagged = []
    patt = re.compile(r'[^.\n]*\b(validad[oa]s? (?:por|con) (?:la institución|RR\. HH\.|el Colegio)|validación institucional'
                      r'|aprobad[oa] por (?:la institución|el Colegio))[^.\n]*', re.I)
    for md in glob.glob(os.path.join(ACAD, 'practica-0*', 'F*_Colegio_Andino.md')):
        for m in patt.finditer(open(md, encoding='utf-8').read()):
            frag = m.group(0)
            if not re.search(r'\b(no|sin|ninguna|ningún|nada|pendiente|sujet[oa]|falta|antes|hasta|depende|condición|confirmarán|a validar)\b', frag, re.I):
                flagged.append(f'{os.path.basename(md)}: «{frag.strip()[:120]}»')
    check('Ninguna afirmación de validación institucional sin negación o condición', not flagged, ' | '.join(flagged))
    # Integridad de los DOCX
    for docx in sorted(glob.glob(os.path.join(ACAD, 'practica-0*', 'F*_Colegio_Andino.docx'))):
        name = os.path.basename(docx)
        z = zipfile.ZipFile(docx)
        ok = z.testzip() is None
        for n in z.namelist():
            if n.endswith(('.xml', '.rels')):
                xml.dom.minidom.parseString(z.read(n))
        doc = z.read('word/document.xml').decode('utf-8')
        rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
        embeds = re.findall(r'r:embed="(rId\d+)"', doc)
        missing = [e for e in embeds if f'Id="{e}"' not in rels]
        media_ok = all(('word/' + t) in z.namelist() for t in re.findall(r'Target="(media/f27b_\d+\.png)"', rels))
        placeholders = '____' in doc
        check(f'DOCX {name}: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla',
              ok and not missing and media_ok and not placeholders,
              f'{len(embeds)} imágenes' + ('; faltan relaciones' if missing else '') + ('; quedan «____»' if placeholders else ''))
    return res


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    fails = 0
    for rule, r, det in checks():
        print(f'{r:5} {rule}' + (f' — {det}' if det else ''))
        fails += r != 'OK'
    print(f'\n{fails} fallas')
    sys.exit(1 if fails else 0)
