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


def pdf_literal_text(data):
    """Extrae literales Tj/TJ del PDF de Word para el check minimo de cabecera H-14.

    Lee operadores de texto BT/ET, incluidos fragmentos con kerning. No busca
    cadenas en metadata ni cuenta imagenes como texto. No es un extractor PDF
    general: una fuente CID/hexadecimal no compatible hace fallar este check.
    """
    import zlib
    lines = []
    literal = re.compile(rb'\(((?:\\.|[^()\\])*)\)')

    def unescape(value):
        def replace(m):
            token = m.group(1)
            if token[:1] in b'01234567':
                return bytes([int(token, 8)])
            return {b'n': b'\n', b'r': b'\r', b't': b'\t', b'b': b'\b',
                    b'f': b'\f'}.get(token, token)
        return re.sub(rb'\\([0-7]{1,3}|[^\r\n])', replace, value).decode('cp1252', errors='replace')

    for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
        try:
            stream = zlib.decompress(stream)
        except zlib.error:
            pass
        for block in re.findall(rb'\bBT\b(.*?)\bET\b', stream, re.S):
            fragments = []
            for operand in re.findall(rb'(\[(?:[^\]]*)\])\s*TJ', block, re.S):
                fragments.extend(unescape(v) for v in literal.findall(operand))
            for value in re.findall(rb'\(((?:\\.|[^()\\])*)\)\s*Tj', block):
                fragments.append(unescape(value))
            if fragments:
                lines.append(''.join(fragments))
    return ' '.join(' '.join(lines).split())


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
    f4_pdf = os.path.join(ACAD, 'practica-04', 'F4_Problemas_del_Proceso_Colegio_Andino.pdf')
    with open(f4_pdf, 'rb') as f:
        header_text = pdf_literal_text(f.read())
    check('H-14 F4 PDF: cabecera presente como texto extraible (Tj/TJ)',
          'Asignatura: Pruebas y Calidad de Software' in header_text)
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


# ---------------------------------------------------------------------------------------------------------------
# Fase F11-R — Formato 11 oficial regularizado sobre la plantilla recibida después de la F28
def f11r_checks():
    """Devuelve (criterio, resultado, detalle). Comprueba que el F11 oficial deriva de la plantilla, conserva la
    arquitectura del F11 adaptado (C01..C17 ↔ CMP-01..CMP-17, R-01..R-20, ARQ-01) y no deja texto de plantilla."""
    import hashlib
    import subprocess
    import m_arch as AR
    import m_f11r as F
    res = []
    add = lambda crit, ok, det='': res.append((crit, 'PASS' if ok else 'FALLA', det))
    tpl_path = os.path.join(ACAD, '00-fuentes-oficiales', 'formatos-originales', 'Formato_11_Arquitectura_del_sistema.docx')
    out = os.path.join(ACAD, 'practica-11', 'F11_Arquitectura_del_Sistema_Colegio_Andino')
    tpl_sha = hashlib.sha256(open(tpl_path, 'rb').read()).hexdigest()
    inv = open(os.path.join(ACAD, '00-fuentes-oficiales', 'inventory.md'), encoding='utf-8').read()
    add('Plantilla oficial del Formato 11 presente y registrada en el inventario (OFICIAL)',
        tpl_sha in inv and 'Formato_11_Arquitectura_del_sistema.docx' in inv, tpl_sha[:16])
    tpl, z = zipfile.ZipFile(tpl_path), zipfile.ZipFile(out + '.docx')
    ok = z.testzip() is None
    for n in z.namelist():
        if n.endswith(('.xml', '.rels')):
            xml.dom.minidom.parseString(z.read(n))
    doc = z.read('word/document.xml').decode('utf-8')
    rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
    embeds = re.findall(r'r:embed="(rId\d+)"', doc)
    targets = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    add('DOCX: ZIP y XML válidos; toda imagen tiene relación y archivo',
        ok and all(e in targets and ('word/' + targets[e]) in z.namelist() for e in embeds), f'{len(embeds)} imágenes')
    same = [n for n in ('word/header1.xml', 'word/styles.xml', 'word/numbering.xml', 'word/media/image1.png')
            if tpl.read(n) == z.read(n)]
    add('Deriva de la plantilla: cabecera (logotipo y asignatura), estilos y numeración idénticos', len(same) == 4,
        ', '.join(same))

    def numbered(d):
        out_ = []
        for par in re.findall(r'<w:p[ >](?:(?!</w:p>).)*?<w:numPr>.*?</w:p>', d, re.S):
            num = (re.findall(r'w:numId w:val="(\d+)"', par) or ['-'])[0]
            out_.append(num + '|' + ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', par)).strip())
        return out_
    tpl_doc = tpl.read('word/document.xml').decode('utf-8')
    tpl_heads = [t for t in numbered(tpl_doc) if not set(t.split('|', 1)[1]) <= {'_'}]
    new_heads = [t for t in numbered(doc) if t.startswith(('1|', '5|')) and not t.split('|', 1)[1].startswith('DA-')]
    add('Estructura oficial: las 8 secciones y sus viñetas, en el mismo orden y con los mismos títulos',
        tpl_heads == new_heads,
        f'{sum(1 for t in new_heads if t.startswith("1|"))} secciones, {sum(1 for t in new_heads if t.startswith("5|"))} viñetas')
    plain = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', doc))
    leftovers = [x for x in ('Describir brevemente', 'Seleccionar y justificar', 'Insertar aquí',
                             'Registrar decisiones clave', '____', '[', '…') if x in plain]
    add('Sin instrucciones, líneas para completar ni marcadores de la plantilla', not leftovers, ', '.join(leftovers))
    tbls = re.findall(r'<w:tbl>.*?</w:tbl>', doc, re.S)

    def cell_rows(t):
        return [[''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', c)) for c in re.findall(r'<w:tc>.*?</w:tc>', r, re.S)]
                for r in re.findall(r'<w:tr[ >].*?</w:tr>', t, re.S)]

    def table_with(word):
        return next(cell_rows(t) for t in tbls if word in ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', t)))
    datos = cell_rows(tbls[0])
    add('Datos generales: los 5 campos oficiales completos', len(datos) == 5 and all(r[-1].strip() for r in datos),
        '; '.join(r[0] for r in datos))
    comp = table_with('Funcionalidades asociadas')
    exp = [(F.CMP[c[0]] + f'({c[0]})', c[1]) for c in AR.COMPONENTES]
    got = [(r[0], r[1]) for r in comp[1:]]
    add('Componentes: CMP-01..CMP-17 = C01..C17, con los nombres canónicos y las columnas oficiales',
        comp[0] == ['ID', 'Componente', 'Descripción', 'Funcionalidades asociadas'] and len(got) == 17 and
        all(g[0] == e[0] and g[1].startswith(e[1]) for g, e in zip(got, exp)), f'{len(got)} filas')
    rel = table_with('Tipo de interacción')
    ids = [m.group(1) if (m := re.match(r'(R-\d\d)\.', r[3])) else '?' for r in rel[1:]]
    same_ends = all(r[0] == F.cmp_ref(x[1]) and r[1] == F.cmp_ref(x[2]) and r[2] == x[3]
                    for r, x in zip(rel[1:], AR.RELACIONES))
    add('Relaciones: R-01..R-20 sin renumerar ni añadir, con el origen, el destino y el tipo de RELATIONSHIPS.md',
        ids == [f'R-{i:02d}' for i in range(1, 21)] and same_ends and
        rel[0] == ['Componente origen', 'Componente destino', 'Tipo de interacción', 'Descripción'], f'{len(ids)} relaciones')
    arq = open(os.path.join(ACAD, 'powerdesigner', 'exports', 'ARQ-01_Arquitectura_Conceptual.png'), 'rb').read()
    media = [z.read('word/' + targets[e]) for e in embeds if e in targets]
    add('ARQ-01: la exportación formal F29/F29B está incrustada sin modificar, en una página horizontal',
        arq in media and 'w:orient="landscape"' in doc)
    add('Estilo: monolito modular adoptado; microservicios no adoptados; sin RLS',
        'MONOLITO MODULAR' in plain and 'No adoptado.' in plain and 'RLS no está implementado' in plain)
    add('Decisiones de diseño con su estado (DA-01 a DA-11)',
        all(re.search(re.escape(d[0]) + r' [^\n]*?Estado:', plain) for d in F.DECISIONES), f'{len(F.DECISIONES)} decisiones')
    no_metric = not re.search(r'\d+(?:[.,]\d+)?\s*(?:ms\b|segundos|usuarios concurrentes|% de disponibilidad)', plain)
    add('Restricciones: RNF-06 y RNF-07 NO VERIFICADOS, RNF-D propuesto, sin SLA ni métricas afirmadas',
        'RNF-06 Rendimiento: NO VERIFICADO' in plain and 'RNF-07 Disponibilidad y recuperabilidad: NO VERIFICADO' in plain
        and 'RNF-D Observabilidad:' in plain and no_metric)
    rfs = {f'RF-{i:02d}' for i in range(1, 28)}
    _, _, rf_of, _, _ = f11_model()
    covered = set().union(*rf_of.values())
    cus = {f'CU-{i:02d}' for i in range(1, 21)}
    add('Trazabilidad: RF-01..RF-27 y CU-01..CU-20 cubiertos por CMP-01..CMP-17 y presentes en el documento',
        covered >= rfs and all(r in plain for r in rfs) and all(c in plain for c in cus),
        f'RF {len(covered & rfs)}/27, CU {sum(c in plain for c in cus)}/20')
    add('RF-23 humano, ranking como apoyo, RF-28 no implementado y RF-29 experimental',
        'Decisión final humana' in plain and 'no selecciona' in plain and 'NO IMPLEMENTADO' in plain
        and 'EXPERIMENTAL / PROPUESTO' in plain)
    pdf = open(out + '.pdf', 'rb').read()
    boxes = re.findall(rb'/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]', pdf)
    pages = len(re.findall(rb'/Type\s*/Page[^s]', pdf))
    add('PDF: válido y con una página horizontal',
        pdf[:5] == b'%PDF-' and b'%%EOF' in pdf[-1024:] and any(float(w) > float(h) for w, h in boxes), f'{pages} páginas')
    adapted = ['docs/academico/practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.' + e for e in ('docx', 'pdf', 'md')]
    r = subprocess.run(['git', 'status', '--porcelain', '--'] + adapted, cwd=ROOT, capture_output=True, text=True)
    add('F11 adaptado histórico intacto (DOCX, PDF y Markdown sin cambios en git)', r.returncode == 0 and not r.stdout.strip())
    return res


# ---------------------------------------------------------------------------------------------------------------
# Fase F29C — variables y matriz de operacionalización (guía E1/L1)
def f29c_checks():
    """Devuelve (criterio, resultado, detalle). Comprueba las reglas de la guía E1/L1 sobre m_variables.py, la
    correspondencia con RF, CU, RNF y variables de RF-29, y que los artefactos generados coinciden con una
    regeneración (DOCX, Markdown, diagramas) sin afirmar resultados de chatbots."""
    import hashlib
    import subprocess
    import tempfile
    import m_common as C
    import m_variables as V
    import f29c
    res = []
    add = lambda crit, ok, det='': res.append((crit, 'PASS' if ok else 'FALLA', det))
    src = os.path.join(ACAD, '00-fuentes-oficiales')
    inv = open(os.path.join(src, 'inventory.md'), encoding='utf-8').read()
    guias = ['L1_Definicion_de_proyecto_software_con_IA.pdf', 'E1_Desarrollo_de_software_con_IA.pdf']
    hashes = {g: hashlib.sha256(open(os.path.join(src, 'guias-ia', g), 'rb').read()).hexdigest() for g in guias}
    add('Guías E1 y L1 presentes y registradas en el inventario con su SHA-256',
        all(h in inv and g in inv for g, h in hashes.items()), ', '.join(h[:12] for h in hashes.values()))
    tipos = [v['tipo'] for v in V.VARIABLES]
    add('Una variable independiente (la solución), una dependiente (el problema) y variables intermedias',
        tipos.count('Independiente') == 1 and tipos.count('Dependiente') == 1 and tipos.count('Intermedia') >= 1,
        f'{len(tipos)} variables')
    add('Cada variable con definición conceptual y operacional',
        all(v['conceptual'].strip() and v['operacional'].strip() for v in V.VARIABLES))
    dims = [(v['id'], len(v['dimensiones'])) for v in V.VARIABLES]
    add('Cada variable tiene varias dimensiones (≥ 2)', all(n >= 2 for _, n in dims),
        ', '.join(f'{i}: {n}' for i, n in dims))
    pocas = [d['id'] for v in V.VARIABLES for d in v['dimensiones'] if len(d['indicadores']) < 2]
    add('Cada dimensión tiene varios indicadores (≥ 2)', not pocas, ', '.join(pocas))
    inds = [(v, d, i) for v in V.VARIABLES for d in v['dimensiones'] for i in d['indicadores']]
    pocos = [i['id'] for _, _, i in inds if len(i['items']) < 2]
    add('Cada indicador tiene varios ítems de medición (≥ 2)', not pocos,
        f'{len(inds)} indicadores, {sum(len(i["items"]) for _, _, i in inds)} ítems' + (': ' + ', '.join(pocos) if pocos else ''))
    ids = [x['id'] for v in V.VARIABLES for x in [v] + v['dimensiones'] + [i for d in v['dimensiones'] for i in d['indicadores']]]
    add('Identificadores únicos de variables, dimensiones e indicadores', len(ids) == len(set(ids)), f'{len(ids)} IDs')
    def partes(instr):  # «Lista de cotejo y Cuestionario Likert (RR. HH.)» → dos instrumentos, sin el paréntesis
        return re.split(r' y | / ', re.sub(r'\s*\([^)]*\)', '', instr))
    malos = [i['id'] for _, _, i in inds
             if not all(any(p.lower() == g.lower() for g in V.INSTRUMENTOS_GUIA) for p in partes(i['instrumento']))]
    add('Instrumentos de la guía: ficha de observación, lista de cotejo o cuestionario Likert', not malos, ', '.join(malos))
    add('Cada indicador tiene escala de medición', all(i['escala'].strip() for _, _, i in inds))
    estados = {C.HV, C.ASP, C.TBP, C.SI, C.EXP}
    fuera = [x for x in [v['estado'] for v in V.VARIABLES] + [i['estado'] for _, _, i in inds]
             if not all(p.replace('uso predictivo ', '') in estados for p in x.split(' · '))]
    add('Estados solo de la leyenda (HV, AS-IS PRELIMINAR, TO-BE PROPUESTO, SOFTWARE IMPLEMENTADO, EXPERIMENTAL)',
        not fuera, ', '.join(sorted(set(fuera))))
    likert_hv = [i['id'] for _, _, i in inds if 'Likert' in i['instrumento'] and C.HV in i['estado']]
    add('Sin mediciones afirmadas: todo indicador con cuestionario Likert es TO-BE PROPUESTO (no aplicado)',
        not likert_hv and all(C.TBP in i['estado'] for _, _, i in inds if 'Likert' in i['instrumento']), ', '.join(likert_hv))
    vd = next(v for v in V.VARIABLES if v['tipo'] == 'Dependiente')
    add('La variable dependiente sigue siendo AS-IS PRELIMINAR y sus indicadores TO-BE PROPUESTO',
        vd['estado'] == C.ASP and all(i['estado'].startswith(C.TBP) for d in vd['dimensiones'] for i in d['indicadores']))
    rf_ok = {f'RF-{i:02d}' for i in range(1, 28)}
    rnf_ok = {x[0] for x in N.RNF}
    contrato = open(os.path.join(ROOT, 'docs', 'v1.1', 'ml', 'feature-contract.md'), encoding='utf-8').read()
    ml_ok = set(re.findall(r'ML-FEAT-\d\d', contrato))
    rfs = set().union(*[i['rf'] for _, _, i in inds])
    rnfs = set().union(*[i['rnf'] for _, _, i in inds])
    mls = set().union(*[i['ml'] for _, _, i in inds])
    add('Los RF citados existen en la línea base RF-01..RF-27', rfs <= rf_ok, f'{len(rfs)} RF; fuera: {sorted(rfs - rf_ok)}')
    add('Los RNF citados existen en el F7 (RNF-01..RNF-10)', rnfs <= rnf_ok, f'{len(rnfs)} RNF; fuera: {sorted(rnfs - rnf_ok)}')
    add('Las variables de RF-29 citadas existen en el contrato de features', mls <= ml_ok,
        f'{len(mls)} citadas de {len(ml_ok)} del contrato; fuera: {sorted(mls - ml_ok)}')
    exp = next(v for v in V.VARIABLES if v['estado'] == C.EXP)
    usados = set().union(*[i['ml'] for d in exp['dimensiones'] for i in d['indicadores']])
    vd_ml = set().union(*[i['ml'] for d in vd['dimensiones'] for i in d['indicadores']])
    add('Guía: los indicadores de la variable dependiente contienen todas las variables que usa el modelo RF-29',
        usados and usados <= vd_ml and len(usados) == 15, f'{len(usados & vd_ml)}/{len(usados)}')
    cus = set().union(*[f29c.cu_of(i['rf']) for _, _, i in inds])
    todos_cu = {f'CU-{i:02d}' for i in range(1, 21)}
    add('Cobertura: RF-01..RF-27 y CU-01..CU-20 (CU derivados de los RF con la tabla del F8, sin CU nuevos)',
        rfs == rf_ok and cus == todos_cu, f'RF {len(rfs & rf_ok)}/27, CU {len(cus & todos_cu)}/20')
    rel = {(a, b) for a, b, _, _ in V.RELACIONES}
    vi = next(v for v in V.VARIABLES if v['tipo'] == 'Independiente')
    add('Relaciones del diagrama: intermedias → VI, VI → VD (TO-BE PROPUESTO, no medida), RF-29 → VD (EXPERIMENTAL)',
        (vi['id'], vd['id']) in rel and all(r[3] == C.TBP for r in V.RELACIONES if r[:2] == (vi['id'], vd['id']))
        and all(r[3] == C.EXP for r in V.RELACIONES if r[0] == exp['id']), f'{len(rel)} relaciones')
    texto = ' '.join(str(x) for v in V.VARIABLES for x in [v['conceptual'], v['operacional']] +
                     [it for d in v['dimensiones'] for i in d['indicadores'] for it in i['items']])
    add('Sin Scrum, DevOps ni SOLID como variables (sin evidencia en el repositorio)',
        not re.search(r'\b(Scrum|DevOps|SOLID)\b', ' '.join(v['nombre'] for v in V.VARIABLES)))
    add('Salvaguardas explícitas: el ranking no cambia estados y RF-29 no toca personas, ranking ni decisión',
        'no evalúa, puntúa, ordena ni selecciona personas' in texto
        and '¿El ranking cambia el estado de alguna postulación? (esperado: No)' in texto
        and '¿El resultado modifica el ranking, la decisión o la selección? (esperado: No)' in texto)
    out = os.path.join(ACAD, 'operacionalizacion')
    tmp = tempfile.mkdtemp()
    stem, diag = 'F29C_Operacionalizacion_Variables', 'F29C_diagrama_conceptual_variables'
    tmp_png = os.path.join(tmp, diag + '.png')    # mismo nombre: el DOCX guarda el nombre de la imagen
    f29c.render_png(tmp_png)
    f29c.render_svg(os.path.join(tmp, 'd.svg'))
    f29c.build_md(os.path.join(tmp, 'm.md'), f'diagramas/{diag}.png', f'diagramas/{diag}.svg', 'ACTIVIDAD_IA_COMPARACION.md')
    f29c.build_activity(os.path.join(tmp, 'a.md'))
    f29c.build_docx(os.path.join(src, 'formatos-originales', 'Formato_11_Arquitectura_del_sistema.docx'),
                    tmp_png, os.path.join(tmp, 'x.docx'))
    pares = [(diag + '.png', f'diagramas/{diag}.png'), ('d.svg', f'diagramas/{diag}.svg'), ('m.md', stem + '.md'),
             ('a.md', 'ACTIVIDAD_IA_COMPARACION.md'), ('x.docx', stem + '.docx')]
    distintos = [b for a, b in pares if open(os.path.join(tmp, a), 'rb').read() != open(os.path.join(out, b), 'rb').read()]
    add('Reproducible: la regeneración produce los mismos bytes (PNG, SVG, Markdown y DOCX)', not distintos, ', '.join(distintos))
    svg = open(os.path.join(out, 'diagramas', diag + '.svg'), encoding='utf-8').read()
    xml.dom.minidom.parseString(svg.encode('utf-8'))
    add('Diagrama conceptual: SVG válido con todas las variables', all(f'>{v["id"]} ·' in svg for v in V.VARIABLES))
    z = zipfile.ZipFile(os.path.join(out, stem + '.docx'))
    tpl = zipfile.ZipFile(os.path.join(src, 'formatos-originales', 'Formato_11_Arquitectura_del_sistema.docx'))
    for n in z.namelist():
        if n.endswith(('.xml', '.rels')):
            xml.dom.minidom.parseString(z.read(n))
    doc = z.read('word/document.xml').decode('utf-8')
    plain = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', doc))
    add('DOCX: ZIP y XML válidos, cabecera institucional de la plantilla y página horizontal',
        z.testzip() is None and z.read('word/header1.xml') == tpl.read('word/header1.xml') and 'w:orient="landscape"' in doc)
    heads = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', re.search(r'<w:tblHeader/>.*?</w:tr>', doc[doc.index('Anexo 1.'):], re.S).group(0)))
    add('Anexo 1: matriz con las 8 columnas pedidas y todas las filas', heads == ''.join(f29c.MATRIX_HEAD) and
        all(i['id'] in plain for _, _, i in inds), f'{len(inds)} indicadores')
    png = open(os.path.join(out, 'diagramas', diag + '.png'), 'rb').read()
    add('Anexo 2: el diagrama incrustado es el PNG generado', 'Anexo 2. Diseño conceptual de variables' in plain
        and png in [z.read(n) for n in z.namelist() if n.startswith('word/media/')])
    pdf = open(os.path.join(out, stem + '.pdf'), 'rb').read()
    boxes = re.findall(rb'/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]', pdf)
    npag = len(re.findall(rb'/Type\s*/Page[^s]', pdf))
    add('PDF: válido y en páginas horizontales', pdf[:5] == b'%PDF-' and b'%%EOF' in pdf[-1024:] and boxes
        and all(float(w) > float(h) for w, h in boxes), f'{npag} páginas')
    protegidos = ['app', 'resources', 'routes', 'database', 'tests', 'ml-service', 'docs/v1.1', 'docs/final-report',
                  'docs/academico/phase-24/output', 'docs/academico/practica-11', 'docs/academico/powerdesigner']
    r = subprocess.run(['git', 'status', '--porcelain', '--'] + protegidos, cwd=ROOT, capture_output=True, text=True)
    add('Alcance: sin cambios en runtime, ML, F9 publicado, F11, F23/F29 ni en el informe v1.0', r.returncode == 0
        and not r.stdout.strip(), r.stdout.strip()[:120])
    return res


def f29c_actividad_checks():
    """Actividad E1/L1 según el ALCANCE EFECTIVO del entregable (m_variables.REQUISITOS). Devuelve (criterio, resultado,
    detalle) con resultado:
      PASS / FALLA  — integridad: paquete, registro, datos escritos, elementos NO REQUERIDO nunca presentados como
                      ejecutados, integración sin evidencia;
      PENDIENTE     — requisito del alcance efectivo sin evidencia completa: estado de trabajo, no falla, pero impide
                      el cierre (`--cierre-f29c`);
      NO REQ        — requisito de la guía fuera del alcance efectivo: se informa, no se valida como ejecutado ni
                      cuenta para el cierre."""
    import datetime
    import subprocess
    import m_common as C
    import m_variables as V
    import f29c
    res = []
    add = lambda crit, st, det='': res.append((crit, st, det))
    ok = lambda b: 'PASS' if b else 'FALLA'
    out = os.path.join(ACAD, 'operacionalizacion')
    act = open(os.path.join(out, 'ACTIVIDAD_IA_COMPARACION.md'), encoding='utf-8').read()
    bloques = re.findall(r'```text\n(.*?)\n```', act, re.S)
    cats = all(f'## {n}. {c}' in act for n, (c, _) in enumerate(f29c.CATEGORIAS, 1))
    no_req = [r for r in V.REQUISITOS if r[3] == V.NO_REQUERIDO]
    add('Paquete: requisito de la guía, alcance efectivo, evidencia ejecutada y NO REQUERIDO distinguidos; P-01 a P-06 '
        'listos para copiar',
        ok([p[3] for p in V.PROMPTS] == bloques and cats and V.CRITERIO_DOCENTE in act and V.CHAT_DOCENTE in act
           and all(e[0] in act for e in V.ENUNCIADOS) and all(r[0] in act and r[2] in act for r in V.REQUISITOS)
           and 'informado por el equipo' in V.CRITERIO_DOCENTE and 'No es contenido de la guía' in V.CRITERIO_DOCENTE
           and V.TITULO_BASE == C.PROYECTO and V.TITULO_BASE in V.PROMPTS[1][3]),
        f'{len(bloques)} prompts; {len(V.REQUISITOS)} requisitos de la guía, {len(no_req)} NO REQUERIDO')
    reg_path = os.path.join(out, V.REGISTRO)
    if not os.path.exists(reg_path):
        add('Registro de ejecuciones presente', 'FALLA', V.REGISTRO + ' no existe (build.py f29c lo crea vacío)')
        return res
    R = f29c.leer_registro(reg_path)
    reg_dir = os.path.dirname(reg_path)
    P = f29c.PEND
    requeridas, no_requeridas = V.EJECUCIONES_REQUERIDAS, V.EJECUCIONES_NO_REQUERIDAS
    estructura = ([(k, r['Chatbot'], r['Prompt']) for k, r in R['runs'].items()] == requeridas
                  and [(k, r['Chatbot'], r['Prompt']) for k, r in R['no_req_runs'].items()] == no_requeridas
                  and [(k, a['bot'], a['prompt_id']) for k, a in R['answers'].items()] == requeridas
                  and [(c[0], c[1], c[2]) for c in R['integracion']] == V.CAPITULOS
                  and len(R['no_req']) == len(f29c.NO_REQ_ITEMS))
    add('Registro: estructura intacta (alcance efectivo, integración, NO REQUERIDO y respuestas)', ok(estructura),
        f'{len(R["runs"])} ejecuciones requeridas, {len(R["no_req_runs"])} NO REQUERIDO')
    if not estructura:
        return res
    hoy = datetime.date.today()
    prompts = {p[0]: p[3] for p in V.PROMPTS}

    def fecha_ok(v):
        m = re.fullmatch(r'(\d\d)/(\d\d)/(\d{4})', v)
        try:
            return bool(m) and datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) <= hoy
        except ValueError:
            return False

    def capturas_ok(v):
        rutas = [x.strip() for x in v.split(';') if x.strip()]
        return rutas and all(re.search(r'\.(png|jpe?g|pdf)$', x, re.I) and os.path.isfile(os.path.join(reg_dir, x))
                             for x in rutas)

    completas, errores, solo_texto = set(), [], []
    for rid, bot, pid in requeridas:
        r, a = R['runs'][rid], R['answers'][rid]
        e = []
        if r['Fecha'] != P and not fecha_ok(r['Fecha']):
            e.append(f'fecha «{r["Fecha"]}» no es DD/MM/AAAA o es futura')
        if r['Enlace'] not in (P, 'No disponible') and not re.fullmatch(r'https://\S+', r['Enlace']):
            e.append(f'enlace «{r["Enlace"]}» no es https:// ni «No disponible»')
        if r['Captura'] not in (P, 'No disponible', 'No aplica') and not capturas_ok(r['Captura']):
            e.append(f'captura inexistente o de formato no admitido: {r["Captura"]}')
        if r['Captura'] == 'No aplica' and not r['Enlace'].startswith('https://'):
            e.append('«No aplica» en captura solo vale con enlace')
        if r['Prompt usado'] not in (P, 'Sin cambios', 'Modificado'):
            e.append(f'«Prompt usado» = «{r["Prompt usado"]}»')
        if r['Prompt usado'] == 'Modificado' and (not a['prompt'] or not a['motivo'] or a['prompt'] == prompts[pid]):
            e.append('prompt «Modificado» sin el prompt real distinto del oficial o sin «Motivo del cambio»')
        if r['Estado'] not in (P, 'Completo'):
            e.append(f'estado «{r["Estado"]}» no admitido en el alcance efectivo')
        if r['Estado'] == 'Completo':
            faltan = [k for k in ('Modelo / versión', 'Plan', 'Fecha', 'Prompt usado', 'Enlace', 'Captura')
                      if r[k] in ('', P, '—')]
            if faltan:
                e.append('marcada Completo con campos pendientes: ' + ', '.join(faltan))
            if not a['respuesta'] or a['respuesta'] == P or len(a['respuesta']) < 20:
                e.append('marcada Completo sin la respuesta pegada')
        if e:
            errores.append(f'{rid}: ' + '; '.join(e))
        elif r['Estado'] == 'Completo':
            completas.add(rid)
            if r['Enlace'] == 'No disponible' and r['Captura'] == 'No disponible':
                solo_texto.append(rid)
    add('Registro: los datos escritos son coherentes (fechas, enlaces, capturas, estados, prompts)', ok(not errores),
        ' | '.join(errores)[:400])

    # NO REQUERIDO: nunca ejecutado ni citado como ejecutado.
    campos = ['Modelo / versión', 'Plan', 'Fecha', 'Prompt usado', 'Enlace', 'Captura']
    mal_nr = [rid for rid, _, _ in no_requeridas
              if R['no_req_runs'][rid]['Estado'] != V.NO_REQUERIDO or any(R['no_req_runs'][rid][k] != '—' for k in campos)]
    mal_nr += [t[:40] for t in R['no_req'] if not t.endswith(f'**{V.NO_REQUERIDO}**')]
    mal_nr += [rid for rid, _, _ in no_requeridas if f'### {rid} ' in R['text']]
    citados = set(re.findall(r'\b(R-(?:0[5-9]|1[0-6])|T-01)\b', ' '.join(' '.join(c[3:]) for c in R['integracion'])))
    mal_nr += sorted(citados)
    mal_nr += [rid for rid, _, _ in requeridas if R['runs'][rid]['Estado'] == V.NO_REQUERIDO]
    add('NO REQUERIDO: R-05 a R-16 y las comparaciones sin datos ni respuestas, nunca citados ni marcados como ejecutados',
        ok(not mal_nr and not (completas & {e[0] for e in no_requeridas})), ', '.join(mal_nr))

    # Integración de P-05 y P-06 con los capítulos 1 y 2: la fuente canónica no se sustituye.
    int_pend, int_mal = 0, []
    for cap, fuente, rid, *resto in R['integracion']:
        if not os.path.isfile(os.path.join(ROOT, fuente)):
            int_mal.append(f'{fuente} no existe')
        if all(x == P for x in resto):
            int_pend += 1
        elif any(x == P for x in resto) or rid not in completas:
            int_mal.append(f'{cap[:10]}: escrita sin {rid} completa o con celdas pendientes')
    fuentes_intactas = subprocess.run(['git', 'status', '--porcelain', '--'] + [c[1] for c in V.CAPITULOS], cwd=ROOT,
                                      capture_output=True, text=True).stdout.strip() == ''
    add('Integración con los capítulos 1 y 2: sin evidencia no se escribe; la fuente canónica no se modifica',
        ok(not int_mal and fuentes_intactas), '; '.join(int_mal) + ('' if fuentes_intactas else ' capítulo canónico modificado'))

    def estado(completo, falla=False):
        return 'FALLA' if falla else ('PASS' if completo else 'PENDIENTE')
    e1 = {'R-01', 'R-02', 'R-03', 'R-04'}
    e4 = {'R-17', 'R-18'}
    def obs(ids):
        t = sorted(set(solo_texto) & ids)
        return f'; evidencia solo textual (sin enlace ni captura): {", ".join(t)}' if t else ''
    add('REQ-01 · Enunciado 1: evidencia de ChatGPT P-01 a P-04 (R-01 a R-04)', estado(e1 <= completas),
        f'{len(e1 & completas)}/4 completas' + obs(e1))
    doc_md = open(os.path.join(out, 'F29C_Operacionalizacion_Variables.md'), encoding='utf-8').read()
    add('REQ-02 · Enunciado 1: matriz y definición conceptual documentadas en el informe (F29C)',
        ok('Anexo 1. Matriz de Operacionalización de Variables' in doc_md and '*Conceptual:*' in doc_md
           and os.path.isfile(os.path.join(out, 'F29C_Operacionalizacion_Variables.docx'))))
    add('REQ-06 · Enunciado 4: evidencia de ChatGPT P-05 y P-06 (R-17, R-18)', estado(e4 <= completas),
        f'{len(e4 & completas)}/2 completas' + obs(e4))
    add('REQ-07 · Enunciado 4: P-05 y P-06 integradas frente a los capítulos 1 y 2 canónicos',
        estado(int_pend == 0 and not int_mal, bool(int_mal)), f'{len(V.CAPITULOS) - int_pend}/{len(V.CAPITULOS)} capítulos')
    for r in no_req:
        add(f'{r[0]} · {r[1]}: {r[2]}', 'NO REQ', 'fuera del alcance efectivo (criterio docente informado por el equipo); '
                                                  'no ejecutado')
    return res


# ---------------------------------------------------------------------------------------------------------------
# F29D a F29H — plan de pruebas, casos, ejecución QA, defectos y métricas, informe final
def f29dh_checks():
    """Devuelve (fase, criterio, resultado, detalle) con resultado PASS, FALLA, PENDIENTE u OBS. OBS informa una
    deuda registrada que no bloquea (la CI de main); PENDIENTE y FALLA impiden el cierre (`--cierre-f29`)."""
    import hashlib
    import shutil
    import tempfile
    import m_common as C
    import m_plan as MP
    import qa_data as Q
    res = []
    add = lambda fase, crit, ok, det='': res.append((fase, crit, 'PASS' if ok else 'FALLA', det))
    tmp = tempfile.mkdtemp()
    txt = lambda x: ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', x))

    def exists(fase, rels):
        falt = [r for r in rels if not os.path.isfile(os.path.join(ACAD, r))]
        add(fase, 'Entregables presentes', not falt, 'faltan: ' + ', '.join(falt) if falt else f'{len(rels)} archivos')
        return not falt

    def pdf_ok(path, min_pages=1):
        pdf = open(path, 'rb').read()
        n = len(re.findall(rb'/Type\s*/Page[^s]', pdf))
        return pdf[:5] == b'%PDF-' and b'%%EOF' in pdf[-1024:] and n >= min_pages, n

    def docx_xml_ok(path):
        z = zipfile.ZipFile(path)
        for n in z.namelist():
            if n.endswith(('.xml', '.rels')):
                xml.dom.minidom.parseString(z.read(n))
        return z.testzip() is None, z

    def same(a, b):
        return open(a, 'rb').read() == open(b, 'rb').read()

    # ------------------------------------------------------------------ F29D
    import f29d
    d_dir = 'plan-pruebas/'
    if exists('F29D', [d_dir + f29d.STEM + e for e in ('.docx', '.pdf', '.md')] + [d_dir + 'F29D_REGISTRO.md', d_dir + 'README.md']):
        ok, z = docx_xml_ok(os.path.join(ACAD, d_dir, f29d.STEM + '.docx'))
        doc = z.read('word/document.xml').decode('utf-8')
        heads = [(1 if s == 'Heading1' else 2, txt(x)) for s, x in re.findall(
            r'<w:p><w:pPr><w:pStyle w:val="(Heading[12])"/></w:pPr>(.*?)</w:p>', doc)]
        add('F29D', 'Estructura de la plantilla del curso: los 29 títulos en orden', ok and heads == MP.SECCIONES, f'{len(heads)} títulos')
        hdr = txt(z.read('word/header1.xml').decode('utf-8'))
        add('F29D', 'Cabecera de la plantilla del curso (Área Informática, docente)',
            'Área Informática' in hdr and 'Maglioni Arana Caparachin' in hdr)
        plain = txt(doc)
        add('F29D', 'Sin aprobación simulada: aprobaciones «Pendiente — sin firma», sin validación institucional',
            plain.count(MP.SIN_APROBACION) >= 2 and 'no está aprobado ni firmado' in plain and 'Firmado' not in plain)
        add('F29D', 'Criterios de aceptación CA-01 a CA-07, riesgos con probabilidad, impacto, mitigación y contingencia',
            all(f'CA-0{i}' in plain for i in range(1, 8)) and all(f'R-0{i}' in plain for i in range(1, 8)) and 'Contingencia' in plain)
        inv = open(os.path.join(ACAD, '00-fuentes-oficiales', 'inventory.md'), encoding='utf-8').read()
        tpl = os.path.join(ACAD, '00-fuentes-oficiales', 'plan-pruebas', 'Plantilla_de_Plan_de_Pruebas_de_Software.pdf')
        add('F29D', 'Plantilla del curso registrada en el inventario con su SHA-256',
            hashlib.sha256(open(tpl, 'rb').read()).hexdigest() in inv)
        f29d.build(os.path.join(tmp, 'd'))
        add('F29D', 'Reproducible: DOCX y Markdown regenerados con los mismos bytes',
            all(same(os.path.join(tmp, 'd', f29d.STEM + e), os.path.join(ACAD, d_dir, f29d.STEM + e)) for e in ('.docx', '.md')))
        ok, n = pdf_ok(os.path.join(ACAD, d_dir, f29d.STEM + '.pdf'), 8)
        add('F29D', 'PDF válido', ok, f'{n} páginas')

    # ------------------------------------------------------------------ F29E
    import f29e
    e_dir = 'casos-prueba/'
    if exists('F29E', [e_dir + x for x in ('F29E_Casos_de_Prueba.md', 'F29E_Matriz_Trazabilidad.md', 'F29E_Casos_de_Prueba.csv', 'README.md')]):
        cs = f29e.casos()
        ids = [c['id'] for c in cs]
        add('F29E', 'IDs CP-001… consecutivos y únicos', ids == [f'CP-{i:03d}' for i in range(1, len(cs) + 1)], f'{len(cs)} CP')
        cov = f29e.cobertura_rf(cs)
        sin = [rf for rf, v in cov.items() if not v[0]]
        add('F29E', 'Cobertura: RF-01 a RF-27 con al menos un CP automatizado aprobado', not sin, f'{27 - len(sin)}/27' + (f'; sin: {sin}' if sin else ''))
        cus = {cu for rf, v in cov.items() if v[0] for cu in f29e.cu_of([rf])}
        add('F29E', 'CU-01 a CU-20 cubiertos a través de sus RF', len(cus) == 20, f'{len(cus)}/20')
        falt = [c['id'] for c in cs if c['auto'] == f29e.AUTO and c['suite'] not in ('Estática', 'CI')
                and not os.path.exists(os.path.join(ROOT, c['prueba'].split(' (')[0]))]
        add('F29E', 'Automatización real: cada CP AUTOMATIZADA apunta a una prueba que existe', not falt, ', '.join(falt))
        manual_mal = [c['id'] for c in cs if c['auto'] != f29e.AUTO and (c['n'] or c['estado'].startswith('APROBADO'))]
        add('F29E', 'Casos manuales sin resultados atribuidos (ejecución histórica o NO EJECUTADO)', not manual_mal, ', '.join(manual_mal))
        junit = Q.phpunit_junit()
        tot = lambda s: sum(c['n'] for c in cs if c['suite'] == s)
        cy = Q.cypress_results()[1]
        add('F29E', 'Cada prueba ejecutada pertenece a un CP: los totales cuadran con la ejecución',
            tot('PHPUnit') == sum(v['n'] for v in junit.values()) and str(tot('Cypress')) == cy.group(3)
            and str(tot('Vitest')) == Q.vitest_results()[1].group(2) and tot('pytest') == sum(v['n'] for v in Q.pytest_results().values()),
            f'PHPUnit {tot("PHPUnit")}, Cypress {tot("Cypress")}, Vitest {tot("Vitest")}, pytest {tot("pytest")}')
        f29e.build(os.path.join(tmp, 'e'))
        add('F29E', 'Reproducible: catálogo, matriz y CSV regenerados con los mismos bytes',
            all(same(os.path.join(tmp, 'e', x), os.path.join(ACAD, e_dir, x)) for x in
                ('F29E_Casos_de_Prueba.md', 'F29E_Matriz_Trazabilidad.md', 'F29E_Casos_de_Prueba.csv')))

    # ------------------------------------------------------------------ F29F
    import f29f
    f_dir = 'qa-final/'
    logs = ['01-git', '02-entorno', '03-compose-config', '04-phpunit', '04b-phpunit-junit', '05-tsc', '06-build',
            '07-vitest', '08-pytest', '08b-pytest', '09-cypress', '10-git-post', '11-pint', '12-vp-check']
    if exists('F29F', [f_dir + 'F29F_Ejecucion_QA.md', f_dir + 'README.md'] + [f_dir + 'evidencias/' + l + '.log' for l in logs]
              + [f_dir + 'evidencias/' + x for x in ('phpunit-junit.xml', 'pytest-junit.xml', 'ci-github-actions.json', '00-resumen.tsv')]):
        sin_rc = [l for l in logs if not re.search(r'# código de salida: \d+', Q.log(l + '.log'))]
        add('F29F', 'Cada registro trae comando, horas y código de salida', not sin_rc, ', '.join(sin_rc))
        g = Q.log('01-git.log').split('\n')
        add('F29F', 'Commit probado registrado y árbol limpio al iniciar', g[4].startswith('bc44303') and g[5].startswith('bc44303 '),
            g[4].strip()[:12])
        crit = f29f.criterios(f29e.casos(), f29f.resultados()[2])
        add('F29F', 'Criterios de aceptación CA-01 a CA-07 cumplidos', all(c[2] for c in crit),
            ', '.join(c[0] for c in crit if not c[2]))
        evid = ''.join(open(os.path.join(Q.EVID, f), encoding='utf-8', errors='replace').read() for f in os.listdir(Q.EVID))
        fuga = [p for p in (r'APP_KEY=base64', r'E2E_TOKEN=\S', r'DESKTOP-[A-Z0-9]+', r'jobs[\\/]61b97500') if re.search(p, evid)]
        add('F29F', 'Evidencia sin secretos, nombre del equipo ni rutas temporales', not fuga, ', '.join(fuga))
        f29f.build(os.path.join(tmp, 'f'))
        add('F29F', 'Reproducible: el resumen regenerado desde la evidencia da los mismos bytes',
            same(os.path.join(tmp, 'f', 'F29F_Ejecucion_QA.md'), os.path.join(ACAD, f_dir, 'F29F_Ejecucion_QA.md')))
        dev, _ = Q.ci_estado('develop')
        add('F29F', 'CI en verde en develop (commit probado)', bool(dev) and dev['conclusion'] == 'success')
        main, main_sha = Q.ci_estado('main')
        res.append(('F29F', 'CI de main', 'OBS' if not main else ('PASS' if main['conclusion'] == 'success' else 'FALLA'),
                    'CI main F29C pendiente de ejecución manual (OBS-F29F-04; deuda registrada, no bloquea)' if not main
                    else main['conclusion']))

    # ------------------------------------------------------------------ F29G
    import f29g
    import m_defectos as MD
    g_dir = 'metricas-calidad/'
    if exists('F29G', [g_dir + 'F29G_Defectos_y_Metricas.md', g_dir + 'README.md']):
        defs = MD.registro()
        campos = ('id', 'descripcion', 'severidad', 'prioridad', 'origen', 'estado', 'version', 'evidencia', 'resolucion', 'regresion')
        add('F29G', 'Cada defecto con los diez campos exigidos', all(all(d.get(k) for k in campos) for d in defs), f'{len(defs)} registros')
        add('F29G', 'Defectos v1.0 = docs/defects.md (DEF-01 a DEF-13), sin defectos inventados',
            [d['id'] for d in defs if d['id'].startswith('DEF-')] == [f'DEF-{i:02d}' for i in range(1, 14)])
        altos = [d['id'] for d in defs if d['severidad'] in ('Crítica', 'Alta') and not d['estado'].startswith('Cerrado')]
        add('F29G', 'Sin defectos Críticos o Altos abiertos', not altos, ', '.join(altos))
        md = open(os.path.join(ACAD, g_dir, 'F29G_Defectos_y_Metricas.md'), encoding='utf-8').read()
        add('F29G', 'Cobertura de código declarada NO MEDIDA y sin certificación ISO/IEC 25010',
            'Cobertura de código (líneas o ramas) | **NO MEDIDA**' in md and 'no se declara certificación' in md)
        f29g.build(os.path.join(tmp, 'g'))
        add('F29G', 'Reproducible: el documento regenerado da los mismos bytes',
            same(os.path.join(tmp, 'g', 'F29G_Defectos_y_Metricas.md'), os.path.join(ACAD, g_dir, 'F29G_Defectos_y_Metricas.md')))

    # ------------------------------------------------------------------ F29H
    import f29h
    h_dir = 'informe-final/'
    if exists('F29H', [h_dir + f29h.STEM + e for e in ('.docx', '.pdf', '.md')] + [h_dir + 'F29H_REGISTRO.md', h_dir + 'README.md']):
        ok, z = docx_xml_ok(os.path.join(ACAD, h_dir, f29h.STEM + '.docx'))
        doc = z.read('word/document.xml').decode('utf-8')
        tz = zipfile.ZipFile(os.path.join(ROOT, f29h.TEMPLATE))
        tdoc = tz.read('word/document.xml').decode('utf-8')

        def heads(d):
            return [(s, txt(p).strip()) for p in re.findall(r'<w:p[ >](?:(?!</w:p>).)*?</w:p>', d, re.S)
                    for s in re.findall(r'<w:pStyle w:val="(Ttulo[12])"/>', p)]
        add('F29H', 'Estructura oficial: los 87 títulos de la plantilla (14 capítulos, 53 secciones y apartados finales)',
            ok and heads(doc) == heads(tdoc), f'{len(heads(doc))} títulos')
        add('F29H', 'Sin texto guía (rojo) ni marcadores de la plantilla',
            'w:val="FF0000"' not in doc and '[Título del proyecto del Equipo]' not in doc and 'Aclaración Importante' not in doc)
        plain = txt(doc)
        add('F29H', 'Portada con el título del proyecto y los tres integrantes',
            C.PROYECTO.replace('–', '–') in plain and all(n in plain for n in C.EQUIPO.split('; ')))
        # Cada sección (Título 2 y apartados finales) tiene contenido propio antes del siguiente título.
        vacias = []
        partes = re.split(r'(<w:p[ >](?:(?!</w:p>).)*?<w:pStyle w:val="Ttulo[12]"/>.*?</w:p>)', doc, flags=re.S)
        for k in range(1, len(partes) - 1, 2):
            h = txt(partes[k]).strip()
            if 'Ttulo2' in partes[k] or h in f29h.FINALES:
                if len(txt(partes[k + 1]).strip()) < 40 and '<w:drawing' not in partes[k + 1]:
                    vacias.append(h)
        add('F29H', 'Cada sección tiene contenido', not vacias, ', '.join(vacias))
        add('F29H', 'Logotipo, figuras de PowerDesigner y anexos A a C en páginas horizontales',
            'word/media/image1.png' in z.namelist() and sum(1 for n in z.namelist() if n.startswith('word/media/f29h_')) == 7
            and doc.count('w:orient="landscape"') >= 3)
        fut = re.findall(r'\bF(?:3\d|4[0-3])\b', plain)
        faltan = [x for x in ('no evalúa', 'decisión final', 'NO MEDIDA', 'sin certificación', 'EXPERIMENTAL',
                              'no hay beneficios medidos', 'Trabajo futuro') if x.lower() not in plain.lower()]
        add('F29H', 'Límites declarados: RF-23 humano, RF-29 experimental, sin beneficios medidos, sin certificación, '
                    'cobertura no medida, trabajo futuro', not faltan and not fut, ', '.join(faltan + fut))
        f29h.build(ROOT, os.path.join(tmp, 'h'))
        add('F29H', 'Reproducible: DOCX y Markdown regenerados con los mismos bytes',
            all(same(os.path.join(tmp, 'h', f29h.STEM + e), os.path.join(ACAD, h_dir, f29h.STEM + e)) for e in ('.docx', '.md')))
        ok, n = pdf_ok(os.path.join(ACAD, h_dir, f29h.STEM + '.pdf'), 20)
        add('F29H', 'PDF válido', ok, f'{n} páginas')
    shutil.rmtree(tmp, ignore_errors=True)
    return res


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    cierre = '--cierre-f29c' in sys.argv[1:] or '--cierre-f29' in sys.argv[1:]
    cierre_f29 = '--cierre-f29' in sys.argv[1:]
    fails = 0
    for rule, r, det in checks():
        print(f'{r:5} {rule}' + (f' — {det}' if det else ''))
        fails += r != 'OK'
    print()
    print('--- F11 (Fase 28): arquitectura conceptual')
    for crit, fuente, r, ev, obs in f11_checks():
        print(f'{r:21} {crit} — {ev}' + (f' ({obs})' if obs else ''))
        fails += r == 'FALLA'
    print()
    print('--- F11-R: Formato 11 oficial regularizado')
    for crit, r, det in f11r_checks():
        print(f'{r:5} {crit}' + (f' — {det}' if det else ''))
        fails += r == 'FALLA'
    print()
    print('--- F29C: variables y matriz de operacionalización (guía E1/L1)')
    for crit, r, det in f29c_checks():
        print(f'{r:5} {crit}' + (f' — {det}' if det else ''))
        fails += r == 'FALLA'
    print()
    print('--- F29C: actividad E1/L1 según el alcance efectivo del entregable')
    pendientes = 0
    for crit, r, det in f29c_actividad_checks():
        print(f'{r:9} {crit}' + (f' — {det}' if det else ''))
        fails += r == 'FALLA'
        pendientes += r == 'PENDIENTE'
    if pendientes:
        print(f'\nF29C ABIERTA: {pendientes} comprobaciones PENDIENTES. Es un estado de trabajo válido, '
              'pero la F29C no puede cerrarse hasta completarlas con evidencia real.')
    else:
        print('\nF29C: actividad completa; se puede auditar para el cierre.')
    if cierre:
        print(f'Modo --cierre-f29c: las pendientes cuentan como fallas → cierre {"RECHAZADO" if pendientes or fails else "ADMITIDO"}.')
        fails += pendientes
    print()
    print('--- F29D a F29H: plan, casos, ejecución QA, defectos y métricas, informe final')
    for fase, crit, r, det in f29dh_checks():
        print(f'{r:5} {fase} · {crit}' + (f' — {det}' if det else ''))
        fails += r == 'FALLA'
        if cierre_f29 and r == 'PENDIENTE':
            fails += 1
    if cierre_f29:
        print(f'\nModo --cierre-f29: cierre de F29 completo {"RECHAZADO" if fails else "ADMITIDO"} '
              '(la CI de main se informa como OBS: deuda registrada, no bloquea).')
    print(f'\n{fails} fallas')
    sys.exit(1 if fails else 0)
