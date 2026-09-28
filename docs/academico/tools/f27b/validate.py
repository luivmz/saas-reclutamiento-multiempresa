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
    cubiertos = rf_cu | set(U.TRANSVERSAL)
    check('F8: todo RF-01..RF-27 está en algún CU o declarado transversal (RF-27)', set(BASE_RF) <= cubiertos,
          ', '.join(sorted(set(BASE_RF) - cubiertos)))
    check('F8: RF-23 solo en el CU de decisión final humana y sin RF-27',
          [c[0] for c in U.CU if 'RF-23' in c[4]] == ['CU-18'] and 'RF-27' not in rf_cu and 'humana' in dict((c[0], c[1]) for c in U.CU)['CU-18'])
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
        if rf in U.TRANSVERSAL:
            if U.TRANSVERSAL[rf]['inb'] != in9:
                div.append(f'{rf}: bloque F9 {in9} / transversal {U.TRANSVERSAL[rf]["inb"]}')
            continue
        mine = [c for c in U.CU if rf in c[4]]
        cus = {c[0] for c in mine}
        if not any(x.strip() in cus for x in re.split(r'[,y]', cu9.replace('Incluido en', ''))):
            div.append(f'{rf}: F9 {cu9} / F8 {sorted(cus)}')
        if not any(in9 in c[7] for c in mine):
            div.append(f'{rf}: bloque F9 {in9}')
    check('F8 ↔ F9: la relación RF → CU → bloque IN coincide con el F9 publicado (RF-27: solo el bloque, divergencia '
          'de CU documentada en D-CU-04)', not div, '; '.join(div))
    # Afirmaciones institucionales
    flagged = []
    patt = re.compile(r'[^.\n]*\b(validad[oa]s? (?:por|con) (?:la institución|RR\. HH\.|el Colegio)|validación institucional'
                      r'|aprobad[oa] por (?:la institución|el Colegio))[^.\n]*', re.I)
    for md in glob.glob(os.path.join(ACAD, 'practica-*', 'F*_Colegio_Andino.md')):
        for m in patt.finditer(open(md, encoding='utf-8').read()):
            frag = m.group(0)
            if not re.search(r'\b(no|sin|ninguna|ningún|nada|pendiente|sujet[oa]|falta|antes|hasta|depende|condición|confirmarán|a validar)\b', frag, re.I):
                flagged.append(f'{os.path.basename(md)}: «{frag.strip()[:120]}»')
    check('Ninguna afirmación de validación institucional sin negación o condición', not flagged, ' | '.join(flagged))
    # Nomenclatura (H-13): variantes retiradas no deben reaparecer en F2 a F5 ni en sus README/pendientes
    variantes = [r'(?<!Candidato )¿Preseleccionado\?', r'Citación recibida', r'Participa en la evaluación',
                 r'Resultado recibido', r'sin candidato elegible']
    encontradas = []
    for f in glob.glob(os.path.join(ACAD, 'practica-0[2-5]', '*.md')):
        txt = open(f, encoding='utf-8').read()
        for v in variantes:
            for m in re.finditer(v, txt):
                ctx = txt[max(0, m.start() - 40):m.end() + 10]
                if not re.search(r'(retir|no se representa|no representa|ni representa|H-13|H-04|variante)', ctx, re.I):
                    encontradas.append(f'{os.path.basename(f)}: «{m.group(0)}»')
    check('F3/F5: no quedan variantes de nombre retiradas (glosario único)', not encontradas, ' | '.join(encontradas))
    # Integridad de los DOCX
    for docx in sorted(glob.glob(os.path.join(ACAD, 'practica-*', 'F*_Colegio_Andino.docx'))):
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


# ---------------------------------------------------------------------------------------------------------------
# Fase 28 — validación de la arquitectura conceptual (F11 adaptado)
def _ids(text, prefix):
    """Extrae IDs (RF-xx, CU-xx, Cxx) de un texto; expande «RF-01..RF-27» y «C04 a C11»."""
    out = set()
    for a, b in re.findall(rf'{prefix}-?(\d+)\s*(?:\.\.|a)\s*{prefix}-?(\d+)', text):
        out |= {f'{prefix}-{i:02d}' if prefix != 'C' else f'C{i:02d}' for i in range(int(a), int(b) + 1)}
    for x in re.findall(rf'\b{prefix}-?(\d\d)\b', text):
        out.add(f'{prefix}-{x}' if prefix != 'C' else f'C{x}')
    return out


def f11_model():
    import m_arch as AR
    comp = {c[0]: c for c in AR.COMPONENTES}
    rf_of = {c[0]: (_ids(' '.join(c[4]), 'RF') if not any('RF-01..RF-27' in r for r in c[4]) else set()) for c in AR.COMPONENTES}
    cu_of = {c[0]: _ids(c[5], 'CU') for c in AR.COMPONENTES}
    edges = []
    for r in AR.RELACIONES:
        for s in sorted(_ids(r[1], 'C')):
            for t in sorted(_ids(r[2], 'C')):
                if s != t:
                    edges.append((s, t, r[0]))
    return AR, comp, rf_of, cu_of, edges


def f11_checks():
    """Devuelve (criterio, fuente, resultado, evidencia, observación)."""
    AR, comp, rf_of, cu_of, edges = f11_model()
    res = []
    add = lambda *r: res.append(r)
    # A) RF
    cubiertos = set().union(*rf_of.values())
    faltan = sorted(set(BASE_RF) - cubiertos)
    add('A. Cobertura funcional RF-01..RF-27', 'F6; COMPONENTS.md', 'PASS' if not faltan else 'FALLA',
        f'{len(set(BASE_RF) & cubiertos)}/27 RF asignados a componentes de negocio o transversales', ', '.join(faltan))
    extra = sorted(r for r in cubiertos if r not in BASE_RF and r != 'RF-29')
    add('A. Ningún RF fuera de la línea base (salvo RF-29 experimental en C17)', 'F6; scope-preliminary.md',
        'PASS' if not extra else 'FALLA', 'RF-29 solo en C17', ', '.join(extra))
    # B) CU
    cus = set().union(*cu_of.values())
    cat = {f'CU-{i:02d}' for i in range(1, 21)}
    add('B. Cobertura CU-01..CU-20', 'F8', 'PASS' if cat <= cus else 'FALLA', f'{len(cat & cus)}/20 CU',
        ', '.join(sorted(cat - cus)))
    add('B. Ningún CU nuevo; CU-21 sigue DIFERIDO', 'F8 (D-CU-03)', 'PASS' if not (cus - cat) else 'FALLA',
        'Sin CU-21 ni otros', ', '.join(sorted(cus - cat)))
    # C) Alcance
    ins = {c[7] for c in U.CU} | {t['inb'] for t in U.TRANSVERSAL.values()}
    ins = {x.strip() for i in ins for x in i.split('·')}
    add('C. Alcance incluido IN-01..IN-08 representado', 'F9 §5', 'PASS' if {f'IN-0{i}' for i in range(1, 9)} <= ins else 'FALLA',
        'Todos los bloques IN tienen componente (vía CU/RF)', '')
    prohibidos = re.compile(r'(factura|suscrip|superadmin|banco de talentos|kubernetes|meilisearch|microservicio|nube|recomendador)', re.I)
    malos = [c[0] for c in AR.COMPONENTES if prohibidos.search(c[1] + ' ' + c[3]) and 'No hay' not in c[3] and 'sin microservicios' not in c[3]]
    add('C. Ningún componente fuera de alcance (OUT-01..OUT-11)', 'F9 §6', 'PASS' if not malos else 'FALLA',
        'Exclusiones listadas aparte (X-01..X-04), no como componentes', ', '.join(malos))
    # D) RNF
    rnf_ok = len(AR.RNF_ARQ) == 10 and all(r[2] and r[3] for r in AR.RNF_ARQ)
    add('D. Los 10 RNF académicos relacionados con decisiones y componentes', 'F7', 'PASS' if rnf_ok else 'FALLA',
        '10/10 con decisión (DA) y componente', '')
    for r in AR.RNF_ARQ:
        if r[4] == 'NO VERIFICADO':
            add(f'D. {r[0]} {r[1]}', 'F7', 'NO VERIFICADO', f'Soporte arquitectónico: {r[2]}; {r[3].split(".")[0]}',
                'Sin evidencia de medición; no se afirma validado')
        elif r[4] == 'EVIDENCIA PARCIAL':
            add(f'D. {r[0]} {r[1]}', 'F7', 'PASS CON OBSERVACIÓN', f'{r[2]}; {r[3]}', 'Evidencia parcial según F7')
    # E) Fronteras
    rf23 = [c for c, s in rf_of.items() if 'RF-23' in s]
    add('E. RF-23: decisión final humana en un componente propio (C10), distinto del ranking',
        'ADR-002; F6 RF-23; F8 CU-18', 'PASS' if rf23 == ['C10'] and 'humana' in comp['C10'][1].lower() else 'FALLA',
        'C10 «Decisión final humana»; R-10: el ranking no elige', '')
    c17_rel = {t for s, t, _ in edges if s == 'C17'} | {s for s, t, _ in edges if t == 'C17'}
    add('E. RF-29 experimental y separado de ranking, decisión y selección', 'ADR-001; ADR-004; OUT-11',
        'PASS' if comp['C17'][7] == 'EXPERIMENTAL' and not (c17_rel & {'C09', 'C10', 'C11'}) else 'FALLA',
        f'C17 EXPERIMENTAL; relaciones solo con {", ".join(sorted(c17_rel))}', '')
    rf28 = [c for c in AR.COMPONENTES if 'RF-28' in ' '.join(c[4])]
    add('E. RF-28 no implementado: sin componente productivo', 'scope-preliminary.md; OUT-07',
        'PASS' if not rf28 and any('RF-28' in x[2] for x in AR.EXCLUIDOS) else 'FALLA', 'X-01 lo registra como NO IMPLEMENTADO', '')
    # F, G, H
    r03 = {t for s, t, rid in edges if rid == 'R-03'}
    add('F. Multitenencia: C03 autoriza y filtra todos los módulos de negocio', 'cap. 7 §7.3; RNF-02',
        'PASS' if {f'C{i:02d}' for i in range(4, 12)} <= r03 else 'FALLA', 'R-03 C03 → C04..C11, C13', 'Sin RLS (DA-02)')
    r13 = {s for s, t, rid in edges if rid == 'R-13'}
    add('G. Auditoría transversal de las acciones críticas', 'RF-27; A-33, A-34', 'PASS' if {f'C{i:02d}' for i in range(4, 12)} <= r13 else 'FALLA',
        'R-13 C04..C11 → C13; trigger de solo inserción', 'Consulta: capacidad técnica (CU-21 diferido)')
    add('H. Privacidad del CV: almacenamiento privado y descarga autorizada', 'A-12, A-15; RNF-04',
        'PASS' if any(rid == 'R-17' and t == 'C15' for s, t, rid in edges) else 'FALLA', 'C15; R-17; DA-05', '')
    # Componentes
    sin_just = [c[0] for c in AR.COMPONENTES if not (rf_of[c[0]] or cu_of[c[0]] or c[7] in ('TRANSVERSAL',) or 'Soporte' in ' '.join(c[4]) or c[0] in ('C01',))]
    add('Componentes: todos con RF/CU o justificación transversal o de soporte', 'COMPONENTS.md', 'PASS' if not sin_just else 'FALLA',
        f'{len(AR.COMPONENTES)} componentes', ', '.join(sin_just))
    # Relaciones: aislados y ciclos entre módulos de negocio
    tocados = {s for s, t, _ in edges} | {t for s, t, _ in edges}
    aislados = sorted(set(comp) - tocados)
    add('Relaciones: ningún componente aislado', 'RELATIONSHIPS.md', 'PASS' if not aislados else 'FALLA',
        f'{len(AR.RELACIONES)} relaciones', ', '.join(aislados))
    neg = {f'C{i:02d}' for i in range(4, 12)}
    g = {}
    for s, t, _ in edges:
        if s in neg and t in neg:
            g.setdefault(s, set()).add(t)
    ciclo = []

    def dfs(n, path):
        for m in g.get(n, ()):
            if m in path:
                ciclo.append(path[path.index(m):] + [m])
            elif not ciclo:
                dfs(m, path + [m])
    for n in sorted(g):
        if not ciclo:
            dfs(n, [n])
    add('Relaciones: sin dependencias circulares entre módulos de negocio', 'RELATIONSHIPS.md', 'PASS' if not ciclo else 'FALLA',
        'Grafo C04..C11 acíclico', ' → '.join(ciclo[0]) if ciclo else '')
    cadena = [('C04', 'C05'), ('C05', 'C07'), ('C06', 'C07'), ('C08', 'C07'), ('C08', 'C09'), ('C09', 'C10'), ('C10', 'C11'), ('C11', 'C07')]
    falt = [f'{a}→{b}' for a, b in cadena if (a, b) not in {(s, t) for s, t, _ in edges}]
    add('Relaciones: flujo completo requerimiento → vacante → postulación → evaluación → ranking → decisión → selección',
        'F5 (TO-BE); RELATIONSHIPS.md', 'PASS' if not falt else 'FALLA', 'R-05..R-12', ', '.join(falt))
    return res


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    fails = 0
    for rule, r, det in checks():
        print(f'{r:5} {rule}' + (f' — {det}' if det else ''))
        fails += r != 'OK'
    print()
    print('--- F11 (Fase 28): arquitectura conceptual')
    for crit, fuente, r, ev, obs in f11_checks():
        print(f'{r:21} {crit} — {ev}' + (f' ({obs})' if obs else ''))
        fails += r == 'FALLA'
    print(f'\n{fails} fallas')
    sys.exit(1 if fails else 0)
