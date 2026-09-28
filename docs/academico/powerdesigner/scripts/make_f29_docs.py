"""Genera MANIFEST.md y la trazabilidad por elemento de la F29 a partir de los modelos.

- docs/academico/powerdesigner/MANIFEST.md: modelos, exportaciones, recursos de los SVG,
  scripts e informes, con SHA-256 del contenido versionado en git (blob de HEAD, con los
  finales de línea normalizados por git) para que el hash no dependa del checkout.
- docs/academico/trazabilidad/F29-powerdesigner-traceability.md: cada elemento de la
  especificación -> objeto del modelo (código) -> carril o agrupación -> dibujado en su
  diagrama -> RF / problema / CU -> exportación.

Uso (raíz del repositorio, después de confirmar los modelos y exportaciones):
    python docs/academico/powerdesigner/scripts/make_f29_docs.py
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F29 = ROOT / 'docs' / 'academico' / 'powerdesigner'
sys.path.insert(0, str(ROOT / 'docs' / 'academico' / 'tools' / 'f27b'))
sys.path.insert(0, str(Path(__file__).parent))
import m_asis  # noqa: E402
import m_cu  # noqa: E402
import m_tobe  # noqa: E402
from validate_f29 import load  # noqa: E402


def rel(p):
    return p.relative_to(ROOT).as_posix()


def blob_sha(path):
    # Contenido tal como lo guarda git: índice (preparado para el commit) o, si no, HEAD.
    for ref in (f':{rel(path)}', f'HEAD:{rel(path)}'):
        r = subprocess.run(['git', 'show', ref], cwd=ROOT, capture_output=True)
        if r.returncode == 0:
            return hashlib.sha256(r.stdout).hexdigest()
    return None


# ------------------------------------------------------------------ índice del modelo
def index(root):
    objs, drawn, pkg_of = {}, set(), {}

    def walk(el, pkg):
        for ch in el:
            if ch.get('Id') and ch.find('a_Code') is not None:
                objs[ch.get('Id')] = ch
                pkg_of[ch.get('Id')] = pkg
                if ch.tag == 'o_Package':
                    walk(ch, ch.findtext('a_Code'))
                    continue
            if ch.tag.endswith('Symbol'):
                o = ch.find('c_Object')
                if o is not None:
                    for r in o:
                        if r.get('Ref'):
                            drawn.add(r.get('Ref'))
            walk(ch, pkg)
    walk(root, None)
    # Un diagrama que muestra objetos de un subpaquete usa accesos directos (o_Shortcut) con el
    # mismo código: el índice por código conserva el objeto real y «dibujado» se evalúa por código.
    by_code = {}
    for i, o in objs.items():
        if o.tag != 'o_Shortcut' or o.findtext('a_Code') not in by_code:
            by_code[o.findtext('a_Code')] = (i, o)
    drawn_codes = {objs[i].findtext('a_Code') for i in drawn if i in objs}
    return objs, drawn_codes, by_code


def lane(objs, o):
    c = o.find('c_OrganizationUnit')
    if c is None:
        return ''
    for r in c:
        if r.get('Ref') in objs:
            return objs[r.get('Ref')].findtext('a_Name')
    return ''


bpm = load(F29 / 'models' / 'F29_BPM_Academico.bpm')
oom = load(F29 / 'models' / 'F29_UML_Academico.oom')
bo, bd, bc = index(bpm)
oo, od, oc = index(oom)


def row_bpm(code):
    if code not in bc:
        return ('FALTA', '', 'no')
    i, o = bc[code]
    return (o.findtext('a_Stereotype') or '', lane(bo, o) or '—', 'sí' if code in bd else 'no')


# ------------------------------------------------------------------ trazabilidad
T = []
T.append('# Trazabilidad F29 — especificación → modelo PowerDesigner → exportación\n')
T.append('Generado por [`powerdesigner/scripts/make_f29_docs.py`](../powerdesigner/scripts/make_f29_docs.py) a partir de los modelos '
         'guardados y de las fuentes del contenido (`tools/f27b/m_asis.py`, `m_tobe.py`, `m_cu.py` y `practica-11/COMPONENTS.md`). '
         'No editar a mano: volver a generarlo.\n')
T.append('**«Dibujado»** indica que el objeto tiene símbolo en el diagrama de su vista. **«Carril»** es el responsable '
         '(atributo *Organization Unit*) guardado en el modelo.\n')
T.append('## Vistas\n')
T.append('| Vista | Especificación | Modelo · paquete | Diagrama | Exportaciones | Verificación |')
T.append('|---|---|---|---|---|---|')
views = [
    ('F3', '../practica-03/POWERDESIGNER_PENDING.md', 'F29_BPM_Academico.bpm · F3', 'F3 - BPMN AS-IS', 'F3_BPMN_ASIS', 'F3_model_check.txt'),
    ('F5', '../practica-05/POWERDESIGNER_PENDING.md', 'F29_BPM_Academico.bpm · F5', 'F5 - BPMN TO-BE', 'F5_BPMN_TOBE', 'F5_model_check.txt'),
    ('F8', '../practica-08/POWERDESIGNER_PENDING.md', 'F29_UML_Academico.oom · F8', 'F8 - Casos de Uso Academicos', 'F8_Casos_de_Uso_Academicos', 'F8_model_check.txt'),
    ('F11 ARQ-01', '../practica-11/POWERDESIGNER_PENDING.md', 'F29_UML_Academico.oom · ARQ01', 'ARQ-01 - Arquitectura Conceptual', 'ARQ-01_Arquitectura_Conceptual', 'ARQ01_model_check.txt'),
]
for v in views:
    T.append(f'| {v[0]} | [`POWERDESIGNER_PENDING.md`]({v[1]}) | `{v[2]}` | «{v[3]}» | '
             f'[PNG](../powerdesigner/exports/{v[4]}.png) · [SVG](../powerdesigner/exports/{v[4]}.svg) | '
             f'[`{v[5]}`](../powerdesigner/validation/{v[5]}) |')

T.append('\n## F3 — BPMN AS-IS\n')
T.append('| ID | Nombre oficial | Tipo (estereotipo) | Carril | Dibujado | Problemas / origen |')
T.append('|---|---|---|---|---|---|')
for g in m_asis.GLOSARIO:
    s, ln, dr = row_bpm('F3_' + g[0].replace('-', '_'))
    T.append(f'| {g[0]} | {g[2]} | {s} | {ln} | {dr} | {g[1]} |')
for a in m_asis.ACTIVIDADES:
    s, ln, dr = row_bpm('F3_' + a[0].replace('-', '_'))
    T.append(f'| {a[0]} | {a[1]} | {s} | {ln} | {dr} | {", ".join(a[5]) or "—"} · {a[6]} |')
T.append('\nMensajes: MF-01 AS-06 → EP-01; MF-02 AS-07 → AS-08; MF-03 AS-10 → borde del pool Postulante; '
         'MF-04 AS-14 → borde del pool Postulante (formatos de mensaje `F3_MF_01` a `F3_MF_04`).')

T.append('\n## F5 — BPMN TO-BE\n')
T.append('| ID | Nombre oficial | Tipo (estereotipo) | Carril | Dibujado | RF | Origen AS-IS |')
T.append('|---|---|---|---|---|---|---|')
for a in m_tobe.ACTIVIDADES:
    s, ln, dr = row_bpm('F5_' + a[0].replace('-', '_'))
    T.append(f'| {a[0]} | {a[2]} | {s} | {ln} | {dr} | {", ".join(a[5]) or "—"} | {", ".join(a[6]) or "—"} |')
for f in m_tobe.FUTURAS:
    s, ln, dr = row_bpm('F5_' + f[0].replace('-', '_'))
    T.append(f'| {f[0]} | {f[2]} | {s} (propuesta futura A-30, desconectada) | {ln} | {dr} | — | — |')
for e in m_tobe.EVENTOS:
    s, ln, dr = row_bpm('F5_' + e[0].replace('-', '_'))
    T.append(f'| {e[0]} | {e[2]} | {s} | {ln} | {dr} | — | — |')
for g in m_tobe.COMPUERTAS:
    s, ln, dr = row_bpm('F5_' + g[0].replace('-', '_'))
    T.append(f'| {g[0]} | {g[3]} | {s} | {ln} | {dr} | — | — |')
s, ln, dr = row_bpm('F5_SP_P')
T.append(f'| SP-P | Gestionar la postulación | {s}, instancia múltiple paralela | {ln} | {dr} | — | — |')
T.append('\nMensajes: ' + '; '.join(f'{m[0]} {m[1].split(" (")[0]} → {m[3]}' for m in m_tobe.MENSAJES) + '.')

T.append('\n## F8 — Casos de uso (vista académica)\n')
T.append('| CU | Nombre | Actores | RF | CU del F9 v1.0 | Vista técnica | Dibujado |')
T.append('|---|---|---|---|---|---|---|')
for u in m_cu.CU:
    dr = 'sí' if 'F8_' + u[0].replace('-', '_') in od else 'no'
    T.append(f'| {u[0]} | {u[1]} | {", ".join(u[3]) or "— (inclusión)"} | {", ".join(u[4])} | {u[5]} | {u[6]} | {dr} |')
T.append('\nActores: ' + '; '.join(f'{a[0]} {a[1]}' for a in m_cu.ACTORES) + '. «include»: '
         + ', '.join(f'{x[0]} → {x[1]}' for x in m_cu.INCLUDES) + '. CU-21 diferido, no modelado. RF-27: nota técnica (UC-RF27).')

T.append('\n## F11 — ARQ-01 arquitectura conceptual\n')
T.append('| ID | Componente | Estereotipo | Agrupación (paquete) | RF | CU | Dibujado |')
T.append('|---|---|---|---|---|---|---|')
comps = (ROOT / 'docs' / 'academico' / 'practica-11' / 'COMPONENTS.md').read_text(encoding='utf-8')
for m in re.finditer(r'^\| (C\d\d) \| ([^|]+?) \| [^|]*\| ([^|]*)\| ([^|]*)\|', comps, re.M):
    i = oc.get('ARQ01_' + m.group(1))
    st = i[1].findtext('a_Stereotype') if i else 'FALTA'
    parent = ''
    if i:
        # paquete de agrupación que contiene el componente (no el paquete de la vista)
        for pid, po in oo.items():
            if po.tag == 'o_Package' and po.findtext('a_Code') != 'ARQ01' and po.find('.//o_Component[@Id="%s"]' % i[0]) is not None:
                parent = po.findtext('a_Name')
    dr = 'sí' if 'ARQ01_' + m.group(1) in od else 'no'
    T.append(f'| {m.group(1)} | {m.group(2)} | {st} | {parent} | {m.group(3).strip()} | {m.group(4).strip()} | {dr} |')
rels = (ROOT / 'docs' / 'academico' / 'practica-11' / 'RELATIONSHIPS.md').read_text(encoding='utf-8')
T.append('\nRelaciones (dependencias del paquete ARQ01): '
         + '; '.join(f'{m.group(1)} {m.group(2).strip()} → {m.group(3).strip()}' for m in re.finditer(r'^\| (R-\d\d) \| ([^|]+)\| ([^|]+)\|', rels, re.M))
         + '. R-03, R-04, R-13, R-14 y R-16 usan el paquete «Capa de negocio» como extremo, como pide la especificación.')
(ROOT / 'docs' / 'academico' / 'trazabilidad' / 'F29-powerdesigner-traceability.md').write_text('\n'.join(T) + '\n', encoding='utf-8', newline='\n')

# ------------------------------------------------------------------ manifiesto
M = []
M.append('# Manifiesto F29 — modelos y exportaciones de PowerDesigner\n')
M.append('Generado por [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py). **SHA-256 del contenido versionado** '
         '(`git show :<ruta>`, el blob que se confirma): git normaliza a LF los finales de línea de `.bpm`, `.oom` y `.svg`, así que el hash '
         'del archivo de trabajo en Windows (CRLF) puede diferir; el del blob es reproducible en cualquier checkout.\n')
M.append('**Estado:** FORMALIZADO — pendiente de la auditoría F29. Ningún formato (DOCX o PDF) se sustituyó todavía.\n')
M.append('## Modelos y exportaciones\n')
M.append('| Artefacto | Tipo | Modelo fuente | Diagrama | Formato | SHA-256 | Estado |')
M.append('|---|---|---|---|---|---|---|')
rows = [
    ('models/F29_BPM_Academico.bpm', 'Modelo BPM (BPMN 2.0 Descriptive)', '—', 'F3 - BPMN AS-IS; F5 - BPMN TO-BE', 'BPM (XML)'),
    ('models/F29_UML_Academico.oom', 'Modelo OOM (UML, Analysis)', '—', 'F8 - Casos de Uso Academicos; ARQ-01 - Arquitectura Conceptual', 'OOM (XML)'),
]
for v in views:
    mf = 'F29_BPM_Academico.bpm' if v[2].startswith('F29_BPM') else 'F29_UML_Academico.oom'
    rows.append((f'exports/{v[4]}.png', 'Exportación', mf, v[3], 'PNG (rasterizado del SVG, escala 2)'))
    rows.append((f'exports/{v[4]}.svg', 'Exportación', mf, v[3], 'SVG (exportación nativa)'))
for r in rows:
    p = F29 / r[0]
    M.append(f'| [`{r[0]}`]({r[0]}) | {r[1]} | {r[2]} | {r[3]} | {r[4]} | `{blob_sha(p) or "sin confirmar"}` | FORMALIZADO |')
M.append('\n## Recursos, scripts e informes\n')
M.append('| Archivo | Uso | SHA-256 |')
M.append('|---|---|---|')
extra = sorted((F29 / 'exports').glob('*_svg_Files/*.png')) + sorted((F29 / 'scripts').glob('*')) + sorted((F29 / 'validation').glob('*.txt'))
for p in extra:
    if p.name.startswith('__') or p.is_dir():
        continue
    use = {'svg_Files': 'Icono referenciado por el SVG (exportado por PowerDesigner)'}.get(p.parent.name.split('_')[-1] if 'svg_Files' in p.parent.name else '', '')
    if 'svg_Files' in p.parent.name:
        use = 'Icono referenciado por el SVG (exportado por PowerDesigner)'
    elif p.parent.name == 'scripts':
        use = 'Script de construcción o validación'
    else:
        use = 'Informe de verificación (salida de los scripts)'
    M.append(f'| [`{rel(p).replace("docs/academico/powerdesigner/", "")}`]({rel(p).replace("docs/academico/powerdesigner/", "")}) | {use} | `{blob_sha(p) or "sin confirmar"}` |')
M.append('\n## Capturas de PowerDesigner\n')
M.append('No se incluyen capturas: no fue posible tomarlas de forma fiable desde la sesión automatizada. Instrucciones para '
         'tomarlas a mano en [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md).')
(F29 / 'MANIFEST.md').write_text('\n'.join(M) + '\n', encoding='utf-8', newline='\n')
print('MANIFEST.md y F29-powerdesigner-traceability.md generados')
