"""Validación independiente de la F29, sin PowerDesigner.

Lee los modelos guardados (XML de PowerDesigner) y las exportaciones, y los contrasta con
las fuentes versionadas del contenido:
  - F3: docs/academico/tools/f27b/m_asis.py (GLOSARIO, ACTIVIDADES)
  - F5: docs/academico/tools/f27b/m_tobe.py (ACTIVIDADES, FUTURAS, EVENTOS, COMPUERTAS)
  - F8: docs/academico/tools/f27b/m_cu.py (ACTORES, CU, INCLUDES)
  - ARQ-01: docs/academico/practica-11/COMPONENTS.md y RELATIONSHIPS.md
Comprueba además las exportaciones (PNG y SVG válidos, con su contenido) y que la F23 no
cambió (git). Complementa, no sustituye, los informes de validation/*.txt.

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

# ------------------------------------------------------------------ F23 intacta
r = subprocess.run(['git', 'status', '--porcelain', '--', 'docs/v1.1/powerdesigner'], cwd=ROOT, capture_output=True, text=True)
check(r.returncode == 0 and r.stdout.strip() == '', 'F23 (docs/v1.1/powerdesigner) sin cambios en git')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for m in fails:
        print('FALLA', m)
    print(f'validate_f29: {len(oks)} comprobaciones correctas, {len(fails)} fallas')
    sys.exit(1 if fails else 0)
