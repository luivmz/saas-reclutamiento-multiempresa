"""Validación independiente de la F29, sin PowerDesigner.

Lee los modelos guardados (XML de PowerDesigner) y las exportaciones, y los contrasta con
las fuentes versionadas del contenido:
  - F3: docs/academico/tools/f27b/m_asis.py (GLOSARIO, ACTIVIDADES)
  - F5: docs/academico/tools/f27b/m_tobe.py (ACTIVIDADES, FUTURAS, EVENTOS, COMPUERTAS)
  - F8: docs/academico/tools/f27b/m_cu.py (ACTORES, CU, INCLUDES)
  - ARQ-01: docs/academico/practica-11/COMPONENTS.md y RELATIONSHIPS.md
Comprueba además las exportaciones (PNG y SVG válidos, con su contenido), la integración
posterior a la F29 (capturas, exportaciones dentro de los DOCX y PDF de los Formatos 03, 05, 08
y 11, y manifiesto) y que la F23 no cambió (git). Complementa, no sustituye, los informes de
validation/*.txt.

Uso (raíz del repositorio): python docs/academico/powerdesigner/scripts/validate_f29.py
"""
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F29 = ROOT / 'docs' / 'academico' / 'powerdesigner'
sys.path.insert(0, str(ROOT / 'docs' / 'academico' / 'tools' / 'f27b'))
import m_asis  # noqa: E402
import m_cu  # noqa: E402
import m_tobe  # noqa: E402

NS = {'a': 'attribute', 'c': 'collection', 'o': 'object'}
fails, oks = [], []


def check(cond, msg):
    (oks if cond else fails).append(msg)


def load(path):
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'xmlns:(\w)="[^"]*"', '', text)          # simplifica los espacios de nombres
    text = re.sub(r'<(/?)(\w):', r'<\1\2_', text)
    text = re.sub(r' (\w):(\w+)=', r' \1_\2=', text)
    return ET.fromstring(text.encode('utf-8'))


def objects(root, kind):
    """Objetos (con Code) de un tipo, con el código de su paquete contenedor."""
    out = []

    def walk(el, pkg):
        for ch in el:
            tag = ch.tag
            if tag == 'o_Package' and ch.find('a_Code') is not None:
                if kind == 'Package':
                    out.append({'pkg': pkg, 'code': ch.findtext('a_Code'), 'name': ch.findtext('a_Name'),
                                'stereo': ch.findtext('a_Stereotype') or '', 'el': ch})
                walk(ch, ch.findtext('a_Code'))
                continue
            if tag == f'o_{kind}' and ch.find('a_Code') is not None:
                out.append({'pkg': pkg, 'code': ch.findtext('a_Code'), 'name': ch.findtext('a_Name'),
                            'stereo': ch.findtext('a_Stereotype') or '', 'el': ch})
            walk(ch, pkg)
    walk(root, None)
    return out


# ------------------------------------------------------------------ BPM
bpm = load(F29 / 'models' / 'F29_BPM_Academico.bpm')
nodes = objects(bpm, 'Process') + objects(bpm, 'ProcessStart') + objects(bpm, 'ProcessEnd') + objects(bpm, 'Decision')
f3 = {n['code']: n for n in nodes if n['code'].startswith('F3_')}
f5 = {n['code']: n for n in nodes if n['code'].startswith('F5_')}


def key(i, prefix):
    return prefix + i.replace('-', '_')


# F3: glosario y actividades con su nombre oficial literal.
exp3 = {g[0]: g[2] for g in m_asis.GLOSARIO}
exp3.update({a[0]: a[1] for a in m_asis.ACTIVIDADES})
for i, name in exp3.items():
    n = f3.get(key(i, 'F3_'))
    check(n is not None and n['name'] == f'{i} {name}', f'F3 {i} «{name}»')
check(len(f3) == len(exp3), f'F3: {len(f3)} nodos en el modelo, {len(exp3)} en la fuente (14 tareas, SP-01, 2 compuertas, 8 eventos)')
sp01 = f3.get('F3_SP_01')
check(sp01 is not None and 'Multi-Instance Parallel' in ET.tostring(sp01['el'], encoding='unicode'),
      'F3 SP-01 instancia múltiple paralela')

# F5: actividades, futura, eventos, compuertas y SP-P.
exp5 = {a[0]: a[2] for a in m_tobe.ACTIVIDADES}
exp5.update({f[0]: f[2] for f in m_tobe.FUTURAS})
exp5.update({e[0]: e[2] for e in m_tobe.EVENTOS})
exp5.update({g[0]: g[3] for g in m_tobe.COMPUERTAS})
exp5['SP-P'] = 'Gestionar la postulación'
for i, name in exp5.items():
    n = f5.get(key(i, 'F5_'))
    check(n is not None and n['name'] == f'{i} {name}', f'F5 {i} «{name}»')
check(len(f5) == len(exp5), f'F5: {len(f5)} nodos en el modelo, {len(exp5)} en la fuente (31 tareas, SP-P, 10 compuertas, 9 eventos)')
check(not any(re.search(r'RF-29|riesgo', n['name'] or '', re.I) for n in f5.values()), 'F5 sin RF-29 ni riesgo operacional')
spp = f5.get('F5_SP_P')
check(spp is not None and 'Multi-Instance Parallel' in ET.tostring(spp['el'], encoding='unicode'),
      'F5 SP-P instancia múltiple paralela')

# Unidades organizativas: pools y carriles.
ous = {o['name'] for o in objects(bpm, 'OrganizationUnit')}
for n in ['Colegio Andino de Huancayo — AS-IS preliminar', 'Postulante', 'Organización cliente (Colegio) con la plataforma — TO-BE propuesto',
          'Área solicitante', 'RR. HH.', 'Dirección', 'Evaluadores', 'Aprobador / Dirección', 'Evaluador', 'Plataforma SaaS (sistema)']:
    check(n in ous, f'BPM pool o carril «{n}»')
check(not any(n.startswith('Default') for n in ous), 'BPM sin carriles «Default» huérfanos')
check(not any('Sistemas' == n for n in ous), 'F3 sin carril «Sistemas»')

# ------------------------------------------------------------------ OOM
oom = load(F29 / 'models' / 'F29_UML_Academico.oom')
acts = {o['code']: o for o in objects(oom, 'Actor') if o['pkg'] == 'F8'}
ucs = {o['code']: o for o in objects(oom, 'UseCase') if o['pkg'] == 'F8'}
for a in m_cu.ACTORES:
    o = acts.get(key(a[0], 'F8_'))
    check(o is not None and o['name'] == f'{a[0]} {a[1]}', f'F8 {a[0]} «{a[1]}»')
check(len(acts) == 5 and not any('Sistema' in (o['name'] or '') for o in acts.values()), 'F8: 5 actores, sin «Sistema»')
for u in m_cu.CU:
    o = ucs.get(key(u[0], 'F8_'))
    check(o is not None and o['name'] == f'{u[0]} {u[1]}', f'F8 {u[0]} «{u[1]}»')
check(len(ucs) == 20 and 'F8_CU_21' not in ucs, 'F8: CU-01 a CU-20, sin CU-21')
check(ucs.get('F8_CU_18', {}).get('name') == 'CU-18 Registrar decisión final humana', 'F8 CU-18 «Registrar decisión final humana»')

comps_md = (ROOT / 'docs' / 'academico' / 'practica-11' / 'COMPONENTS.md').read_text(encoding='utf-8')
exp_c = dict(re.findall(r'^\| (C\d\d) \| ([^|]+?) \|', comps_md, re.M))
comps = {o['code']: o for o in objects(oom, 'Component') if (o['code'] or '').startswith('ARQ01_')}
for cid, name in exp_c.items():
    o = comps.get('ARQ01_' + cid)
    check(o is not None and o['name'] == f'{cid} {name}', f'ARQ-01 {cid} «{name}»')
check(len(comps) == 17 and 'ARQ01_C18' not in comps, 'ARQ-01: 17 componentes, sin C18')
check('experimental' in comps.get('ARQ01_C17', {}).get('stereo', ''), 'ARQ-01 C17 <<experimental>>')
check('human decision' in comps.get('ARQ01_C10', {}).get('stereo', ''), 'ARQ-01 C10 <<human decision>>')
groups = {o['name'] for o in objects(oom, 'Package') if (o['code'] or '').startswith('ARQ01_') and o['code'] != 'ARQ01_ACT'}
check(groups == {'Capa de presentación', 'Capa de acceso y seguridad', 'Capa de negocio', 'Servicios transversales',
                 'Persistencia e infraestructura', 'Experimental (opcional)'}, f'ARQ-01: 6 agrupaciones ({len(groups)})')
deps = [o for o in objects(oom, 'Dependency') if (o['code'] or '').startswith('ARQ01_')]
rids = sorted({re.sub(r'b$', '', o['code'].replace('ARQ01_', '').replace('_', '-')) for o in deps} - {'U'})
check(rids == [f'R-{i:02d}' for i in range(1, 21)], f'ARQ-01: R-01 a R-20 ({len(rids)})')
check(not any(re.search(r'factur|suscrip|superadmin|talent|kubernetes|meilisearch|microservic|motor de selecci', (o['name'] or ''), re.I)
              for o in comps.values()), 'ARQ-01 sin elementos fuera de alcance')

# ------------------------------------------------------------------ exportaciones
try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
except ImportError:
    Image = None
expected = {
    'F3_BPMN_ASIS': ['AS-14', 'SP-01', 'MF-04'], 'F5_BPMN_TOBE': ['TB-30', 'TB-F1', 'MT-08', 'SP-P'],
    'F8_Casos_de_Uso_Academicos': ['CU-20', 'CU-18', 'ACT-05'], 'ARQ-01_Arquitectura_Conceptual': ['C17', 'R-20', 'C10'],
}
for base, words in expected.items():
    svg, png = F29 / 'exports' / f'{base}.svg', F29 / 'exports' / f'{base}.png'
    ok_svg = svg.exists() and svg.stat().st_size > 0
    if ok_svg:
        text = svg.read_text(encoding='utf-8')
        try:
            ET.fromstring(text.encode('utf-8')); parsed = True
        except ET.ParseError:
            parsed = False
        check(parsed and all(w in text for w in words), f'{base}.svg válido y con {", ".join(words)}')
        refs = re.findall(r'xlink:href="([^"#][^"]*)"', text)
        check(all((svg.parent / r).exists() for r in refs), f'{base}.svg: {len(refs)} recursos referenciados presentes')
    else:
        check(False, f'{base}.svg existe')
    if Image and png.exists():
        with Image.open(png) as im:
            im.verify()
        with Image.open(png) as im:
            check(im.size[0] > 1000 and im.size[1] > 500, f'{base}.png válido ({im.size[0]} x {im.size[1]})')
    else:
        check(png.exists() and png.stat().st_size > 0, f'{base}.png existe')

# ------------------------------------------------------------------ F29B: reproducibilidad
# 1) Ajuste automático al texto desactivado en todo símbolo de nodo: con él activado,
#    PowerDesigner vuelve a dimensionar el símbolo al abrir el modelo.
LINKS = {'o_FlowSymbol', 'o_DependencySymbol', 'o_UseCaseAssociationSymbol', 'o_SwimlaneSubGroupSymbol', 'o_SwimpoolSymbol'}
for name, root in (('BPM', bpm), ('OOM', oom)):
    bad = [el.tag for el in root.iter() if el.tag.endswith('Symbol') and el.tag not in LINKS
           and el.find('a_Rect') is not None and el.findtext('a_AutoAdjustToText') != '0']
    check(not bad, f'{name}: ajuste automático al texto desactivado en todos los símbolos de nodo ({len(bad)} activos)')

# 2) ARQ-01: cada agrupación conserva en el XML la geometría que declara el script.
arq_script = (F29 / 'scripts' / 'f29-arq01-arquitectura.ps1').read_text(encoding='utf-8-sig')
declared = {c: tuple(int(x) for x in v) for c, v in
            ((m.group(1), m.group(2, 3, 4, 5)) for m in re.finditer(r"@\('(\w+)', '[^']+', (-?\d+), (-?\d+), (-?\d+), (-?\d+)\)", arq_script))}
pkg_ids = {el.get('Id'): el.findtext('a_Code') for el in oom.iter('o_Package') if el.get('Id')}
saved = {}
for el in oom.iter('o_PackageSymbol'):
    ref = el.find('c_Object/o_Package')
    code = pkg_ids.get(ref.get('Ref')) if ref is not None else None
    if code and code.startswith('ARQ01_'):
        nums = [int(x) for x in re.findall(r'-?\d+', el.findtext('a_Rect'))]   # ((L,B),(R,T))
        saved[code.replace('ARQ01_', '')] = (nums[0], nums[3], nums[2], nums[1])
for g in ('PRE', 'ACC', 'EXP', 'NEG', 'TRA', 'INF'):
    check(declared.get(g) is not None and saved.get(g) == declared.get(g),
          f'ARQ-01 agrupación {g}: geometría guardada {saved.get(g)} = declarada {declared.get(g)}')

# 3) Subprocesos expandidos (F29B-OBS-01): el diagrama de detalle del proceso compuesto
#    representa todos sus hijos (mismos objetos, sin duplicarlos) y los demás diagramas del
#    proceso (el de la vista compuesta) quedan vacíos; así la exportación no duplica nada.
for code, tasks in (('F3_SP_01', ['AS-09', 'AS-10', 'AS-11']),
                    ('F5_SP_P', ['TB-14', 'TB-15', 'TB-16', 'TB-17', 'TB-18', 'TB-19', 'TB-20', 'TB-21', 'TB-22', 'TB-23'])):
    sp = next(el for el in bpm.iter('o_Process') if el.findtext('a_Code') == code)
    kids = {el.get('Id') for coll in ('c_Processes', 'c_ProcessStarts', 'c_ProcessEnds', 'c_ProcessDecisions', 'c_Flows')
            for el in sp.findall(f'{coll}/*') if el.get('Id')}
    diagrams = sp.findall('c_BusinessProcessDiagrams/o_BusinessProcessDiagram')
    detail = [dg for dg in diagrams if (dg.findtext('a_Name') or '').endswith('— detalle')]
    others = [dg for dg in diagrams if dg not in detail]
    refs = {r.get('Ref') for r in detail[0].iter() if r.get('Ref')} if detail else set()
    check(len(detail) == 1 and bool(kids) and kids <= refs,
          f'{code}: diagrama de detalle con los {len(kids)} hijos representados ({len(kids & refs)})')
    check(all(dg.find('c_Symbols') is None or len(dg.find('c_Symbols')) == 0 for dg in others),
          f'{code}: diagrama de la vista compuesta vacío ({len(others)})')
    names = [el.findtext('a_Name') for el in sp.iter('o_Process') if el.get('Id')]   # definiciones, no referencias
    check(len(names) == len(set(names)), f'{code}: sin objetos duplicados en el subproceso')
    svg = (F29 / 'exports' / ('F3_BPMN_ASIS.svg' if code.startswith('F3') else 'F5_BPMN_TOBE.svg')).read_text(encoding='utf-8')
    counts = {t: len(re.findall(rf'>{t} ', svg)) for t in tasks}
    check(all(c == 1 for c in counts.values()), f'{code}: la exportación dibuja cada tarea del subproceso una sola vez {counts}')

# 4) Publicación reproducible registrada en los informes de las cuatro vistas.
for rep in ('F3_model_check.txt', 'F5_model_check.txt', 'F8_model_check.txt', 'ARQ01_model_check.txt'):
    t = (F29 / 'validation' / rep).read_text(encoding='utf-8')
    recs = re.findall(r'Recarga «[^»]+»: (\d+) símbolos antes de guardar, (\d+) tras reabrir; cambiados: (\d+); ausentes: (\d+)', t)
    ok = bool(recs) and all(a == b and c == '0' and d == '0' for a, b, c, d in recs)
    check(ok and 'reproduce el mismo SVG' in t and ': True' in t.split('reproduce el mismo SVG')[1][:80] and 'RESULTADO: PASS' in t,
          f'{rep}: recarga sin cambios ({len(recs)} diagramas) y exportación reproducible')

# ------------------------------------------------------------------ integración posterior a la F29
# Capturas reales, exportaciones formales dentro de los DOCX y PDF de los Formatos 03, 05, 08 y 11, y manifiesto.
import hashlib  # noqa: E402
import zipfile  # noqa: E402

ACAD = ROOT / 'docs' / 'academico'
BASE_REF = 'e49b313'   # último commit antes de la integración (F29B)
CAPS = {
    'F3': ['F3_BPMN_ASIS_PowerDesigner.png', 'F3_SP-01_detalle_PowerDesigner.png'],
    'F5': ['F5_BPMN_TOBE_PowerDesigner_parte1.png', 'F5_BPMN_TOBE_PowerDesigner_parte2.png', 'F5_SP-P_detalle_PowerDesigner.png'],
    'F8': ['F8_Casos_de_Uso_PowerDesigner.png'],
    'F11': ['ARQ01_Arquitectura_Conceptual_PowerDesigner.png'],
}
FORMATS = {   # formato: (DOCX sin extensión, exportación formal, borradores sustituidos, páginas horizontales)
    'F3': ('practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino', 'F3_BPMN_ASIS.png',
           ['practica-03/diagramas/draft/F3-bpmn-as-is-parte1.png', 'practica-03/diagramas/draft/F3-bpmn-as-is-parte2.png'], True),
    'F5': ('practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino', 'F5_BPMN_TOBE.png',
           [f'practica-05/diagramas/draft/F5-bpmn-to-be-parte{x}.png' for x in ('1', '2a', '2b', '3')], True),
    'F8': ('practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino', 'F8_Casos_de_Uso_Academicos.png',
           ['practica-08/diagramas/draft/F8-casos-de-uso-academico.png'], False),
    'F11': ('practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino', 'ARQ-01_Arquitectura_Conceptual.png',
            ['practica-11/diagramas/draft/F11-arquitectura-conceptual.png'], True),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def png_dims(data):
    return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')


export_sha = {e.name: sha(e.read_bytes()) for e in (F29 / 'exports').glob('*.png')}

# 1) Las 7 capturas: PNG válidos del tamaño de una ventana, distintos de cualquier exportación.
for fmt, caps in CAPS.items():
    for cap in caps:
        f = F29 / 'evidencias' / 'capturas' / cap
        data = f.read_bytes() if f.exists() else b''
        w, h = png_dims(data) if data[:8] == b'\x89PNG\r\n\x1a\n' else (0, 0)
        check(w >= 1000 and h >= 600 and sha(data) not in export_sha.values(),
              f'Captura {cap}: PNG válido de ventana ({w}x{h}), distinto de las exportaciones')
check('STATUS: COMPLETED' in (F29 / 'evidencias' / 'capturas' / 'CAPTURAS_PENDIENTES.md').read_text(encoding='utf-8'),
      'CAPTURAS_PENDIENTES.md: STATUS: COMPLETED')

# 2) DOCX: exportación formal y capturas incrustadas, sin borradores, con tablas y encabezados conservados.
for fmt, (stem, exp, drafts, landscape) in FORMATS.items():
    path = ACAD / f'{stem}.docx'
    z = zipfile.ZipFile(path)
    okzip = z.testzip() is None
    try:
        for n in z.namelist():
            if n.endswith(('.xml', '.rels')):
                ET.fromstring(z.read(n))
        okxml = True
    except ET.ParseError:
        okxml = False
    doc = z.read('word/document.xml').decode('utf-8')
    rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
    embeds = re.findall(r'r:embed="(rId\d+)"', doc)
    targets = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    media = {t: z.read('word/' + t) for t in (targets.get(e) for e in embeds) if t and ('word/' + t) in z.namelist()}
    media_sha = {sha(b) for b in media.values()}
    check(okzip and okxml and len(media) == len(set(targets.get(e) for e in embeds)),
          f'{fmt} DOCX: ZIP y XML válidos, {len(embeds)} imágenes con su relación')
    check(export_sha[exp] in media_sha, f'{fmt} DOCX: incrusta la exportación formal {exp} sin modificar')
    draft_sha = {sha((ACAD / d).read_bytes()) for d in drafts}
    check(not (draft_sha & media_sha), f'{fmt} DOCX: ningún borrador (diagramas/draft) incrustado')
    cap_sha = {sha((F29 / 'evidencias' / 'capturas' / c).read_bytes()) for c in CAPS[fmt]}
    check(cap_sha <= media_sha, f'{fmt} DOCX: incrusta sus {len(cap_sha)} capturas de PowerDesigner')
    core = z.read('docProps/core.xml').decode('utf-8')
    check(bool(re.search(r'<dc:title>Formato \d+', core)) and '____' not in doc, f'{fmt} DOCX: título y sin campos vacíos')
    old = subprocess.run(['git', 'show', f'{BASE_REF}:docs/academico/{stem}.docx'], cwd=ROOT, capture_output=True).stdout
    old_doc = zipfile.ZipFile(__import__('io').BytesIO(old)).read('word/document.xml').decode('utf-8')
    head_pat = r'<w:numId w:val="1"/>' if fmt != 'F11' else r'w:val="Ttulo1"'
    check(doc.count('<w:tbl>') >= old_doc.count('<w:tbl>') and doc.count(head_pat) == old_doc.count(head_pat),
          f'{fmt} DOCX: tablas ({old_doc.count("<w:tbl>")} → {doc.count("<w:tbl>")}) y encabezados numerados '
          f'({doc.count(head_pat)}) conservados')
    n_land = doc.count('w:orient="landscape"')
    check(n_land > 0 if landscape else n_land == 0, f'{fmt} DOCX: {n_land} páginas horizontales para diagramas anchos')

    # 3) PDF: válido, con la exportación (misma proporción) y las páginas horizontales.
    pdf = (ACAD / f'{stem}.pdf').read_bytes()
    pages = re.findall(rb'/Type\s*/Page[^s]', pdf)
    boxes = re.findall(rb'/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]', pdf)
    land = sum(1 for w, h in boxes if float(w) > float(h))
    ew, eh = png_dims((F29 / 'exports' / exp).read_bytes())
    imgs = [(int(a), int(b)) for a, b in re.findall(rb'/Subtype\s*/Image[^>]*?/Width\s+(\d+)\s*/Height\s+(\d+)', pdf)]
    has_exp = any(abs(w / h - ew / eh) < 0.01 * ew / eh for w, h in imgs if h)
    check(pdf[:5] == b'%PDF-' and b'%%EOF' in pdf[-1024:] and len(pages) > 0 and has_exp and (land > 0) == landscape,
          f'{fmt} PDF: válido, {len(pages)} páginas ({land} horizontales), exportación formal presente')

# 4) Manifiesto: capturas VALID con el SHA-256 del archivo, y formatos UPDATED.
man = (F29 / 'MANIFEST.md').read_text(encoding='utf-8')
for caps in CAPS.values():
    for cap in caps:
        h = sha((F29 / 'evidencias' / 'capturas' / cap).read_bytes())
        check(re.search(rf'{re.escape(cap)}`\]\([^)]*\) \| Captura PNG \|[^\n]*`{h}` \| VALID \|', man) is not None,
              f'MANIFEST: {cap} VALID con su SHA-256')
check(man.count('| UPDATED |') == 8, 'MANIFEST: 8 entregables (DOCX y PDF de F3, F5, F8 y F11) UPDATED')

# ------------------------------------------------------------------ F23 intacta
r = subprocess.run(['git', 'status', '--porcelain', '--', 'docs/v1.1/powerdesigner'], cwd=ROOT, capture_output=True, text=True)
check(r.returncode == 0 and r.stdout.strip() == '', 'F23 (docs/v1.1/powerdesigner) sin cambios en git')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for m in fails:
        print('FALLA', m)
    print(f'validate_f29: {len(oks)} comprobaciones correctas, {len(fails)} fallas')
    sys.exit(1 if fails else 0)
