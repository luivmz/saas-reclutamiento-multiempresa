"""F29H — Informe Final v1 sobre la plantilla oficial Plantilla_Estructura_de_proyecto_final.docx.

Se conserva el paquete de la plantilla: portada con logotipo, estilos, numeración de capítulos, tabla de contenido y
pie. Se hacen estos cambios:
- la portada recibe el título y los integrantes (el código de alumno no está en el repositorio: queda «Pendiente»);
- se eliminan todos los textos guía en rojo (FF0000) y la «Aclaración importante»;
- después de cada título se inserta el contenido de m_informe.py (títulos e introducciones negras de la plantilla se
  conservan);
- al final, los diagramas anchos (anexos A a C) van en páginas horizontales.
"""
import hashlib
import os
import re
import zipfile
from xml.dom import minidom
from xml.sax.saxutils import escape

import m_common as C
import m_informe as M
from docxgen import (_runs, image_data, image_xml, keep_image_resolution, sect_variant, split_blocks,
                     wide_image_parts, EMU_CM, TWIP_CM)

STEM = 'F29H_Informe_Final_v1_Colegio_Andino'
TEMPLATE = 'docs/academico/00-fuentes-oficiales/plantillas-proyecto/Plantilla_Estructura_de_proyecto_final.docx'
TEXT_W = 11906 - 1440 - 1440                   # A4 con márgenes de 2,54 cm (twips)
FIXED = (2026, 9, 30, 0, 0, 0)
RED = re.compile(r'<w:color w:val="FF0000"/>')
FINALES = ('CONCLUSIONES', 'RECOMENDACIONES', 'REFERENCIAS', 'ANEXOS')


def text_of(xml):
    return ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', xml)).strip()


def style_of(xml):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', xml)
    return m.group(1) if m else None


# ------------------------------------------------------------------ bloques de contenido
def _p(text, italic=False, sz=None, jc='both', after=120):
    return (f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="276" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'
            f'{_runs(text, italic=italic, sz=sz)}</w:p>')


def _bullet(text):
    return ('<w:p><w:pPr><w:spacing w:after="60" w:line="264" w:lineRule="auto"/><w:ind w:left="567" w:hanging="283"/>'
            '<w:jc w:val="both"/></w:pPr><w:r><w:t>•</w:t></w:r><w:r><w:tab/></w:r>' + _runs(text) + '</w:p>')


def _cell(text, width, sz, header=False):
    paras = ''.join(f'<w:p><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                    f'{_runs(line, bold=header, sz=sz)}</w:p>' for line in (str(text).split('\n') or ['']))
    shd = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if header else ''
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}</w:tcPr>{paras}</w:tc>'


def _table(headers, rows, fracs, sz=16):
    widths = [int(TEXT_W * f) for f in fracs[:-1]]
    widths.append(TEXT_W - sum(widths))
    out = [f'<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/><w:tblW w:w="{TEXT_W}" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
           'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>' +
           ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>',
           '<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' +
           ''.join(_cell(h, w, sz, True) for h, w in zip(headers, widths)) + '</w:tr>']
    for r in rows:
        out.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(_cell(c, w, sz) for c, w in zip(r, widths)) + '</w:tr>')
    return ''.join(out) + '</w:tbl>' + _p('', after=60)


class Media:
    def __init__(self, root):
        self.root, self.items, self.n = root, [], 300

    def add(self, rel):
        data, w, h = image_data(os.path.join(self.root, rel))
        self.n += 1
        rid, target = f'rId{self.n}', f'media/f29h_{len(self.items) + 1}.png'
        self.items.append((rid, target, data))
        return rid, self.n, w, h


def render(blocks, media):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'p':
            out.append(_p(b[1]))
        elif k == 'note':
            out.append(_p(b[1], italic=True, sz=18))
        elif k == 'ul':
            out += [_bullet(x) for x in b[1]]
        elif k == 'table':
            out.append(_table(b[1], b[2], b[3], b[4] if len(b) > 4 else 16))
        elif k == 'img':
            rid, docpr, w, h = media.add(b[1])
            cx = int((TEXT_W / TWIP_CM) * EMU_CM)
            cy = int(cx * h / w)
            max_cy = int(19.0 * EMU_CM)
            if cy > max_cy:
                cy, cx = max_cy, int(max_cy * w / h)
            out.append(image_xml(rid, docpr, os.path.basename(b[1]), cx, cy).replace('<w:pPr>', '<w:pPr><w:keepNext/>', 1))
            out.append(_p(b[2], italic=True, sz=18, jc='center', after=160))
        else:
            raise ValueError(k)
    return ''.join(out)


# ------------------------------------------------------------------ portada
def _cover_table(tbl):
    rows = re.findall(r'<w:tr[ >].*?</w:tr>', tbl, re.S)
    head, tmpl = rows[0], rows[1]
    rpr = '<w:rPr><w:rFonts w:cs="Arial"/><w:lang w:val="es-ES"/></w:rPr>'
    new_rows = []
    for name in C.EQUIPO.split('; '):
        cells = re.findall(r'<w:tc>.*?</w:tc>', tmpl, re.S)
        vals = [name, 'Pendiente']
        filled = [c.replace('</w:p>', f'<w:r>{rpr}<w:t xml:space="preserve">{escape(v)}</w:t></w:r></w:p>', 1)
                  for c, v in zip(cells, vals)]
        new_rows.append(re.sub(r'<w:tc>.*</w:tc>', lambda m: ''.join(filled), tmpl, count=1, flags=re.S))
    start = tbl.index(rows[0])
    return tbl[:start] + head + ''.join(new_rows) + '</w:tbl>'


def build(root, out_dir):
    tpl = os.path.join(root, TEMPLATE)
    zin = zipfile.ZipFile(tpl)
    document = zin.read('word/document.xml').decode('utf-8')
    rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
    head, rest = document.split('<w:body>', 1)
    body, tail = rest.rsplit('</w:body>', 1)
    blocks = split_blocks(body)
    sect = blocks[-1][1]
    assert sect.startswith('<w:sectPr'), 'la última pieza del cuerpo debe ser el sectPr'
    S = M.secciones()
    media = Media(root)
    parts, usados, headings = [], set(), []
    for kind, xml in blocks[:-1]:
        txt = text_of(xml)
        if kind == 'w:tbl' and 'APELLIDOS Y NOMBRES' in txt:
            parts.append(_cover_table(xml))
            continue
        if kind != 'w:p':
            parts.append(xml)
            continue
        st = style_of(xml)
        if '[Título del proyecto del Equipo]' in xml:
            xml = xml.replace('[Título del proyecto del Equipo]', escape(M.TITULO))
        is_heading = st in ('Ttulo1', 'Ttulo2')
        if RED.search(xml) and not is_heading:
            continue                                            # texto guía de la plantilla
        if is_heading:
            xml = RED.sub('', xml)                              # títulos del capítulo 8 en rojo en la plantilla
            headings.append((st, txt))
        parts.append(xml)
        key = txt if (st == 'Ttulo2' or txt in FINALES) else None
        if key:
            if key not in S:
                raise KeyError(f'Sin contenido para la sección «{key}»')
            parts.append(render(S[key], media))
            usados.add(key)
    sobrantes = set(S) - usados
    assert not sobrantes, f'Contenido sin sección en la plantilla: {sobrantes}'
    # Anexos A a C en páginas horizontales; la última sección del documento queda horizontal.
    for i, (rel, caption) in enumerate(M.ANEXOS_IMG):
        data, w, h = image_data(os.path.join(root, rel))
        media.n += 1
        rid, target = f'rId{media.n}', f'media/f29h_{len(media.items) + 1}.png'
        media.items.append((rid, target, data))
        cap = _p(caption, italic=True, sz=18, jc='center', after=0)
        pieces = wide_image_parts(sect, False, rid, media.n, os.path.basename(rel), w, h, cap, close_prev=(i == 0))
        if i == len(M.ANEXOS_IMG) - 1:
            pieces[-1] = cap                                    # la última sección usa el sectPr final (horizontal)
        parts += pieces
    final_sect = sect_variant(sect, landscape=True)
    new_doc = head + '<w:body>' + ''.join(parts) + final_sect + '</w:body>' + tail
    minidom.parseString(new_doc.encode('utf-8'))
    for rid, target, _ in media.items:
        rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                            f'officeDocument/2006/relationships/image" Target="{target}"/></Relationships>')
    core = zin.read('docProps/core.xml').decode('utf-8')
    core = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', f'<dc:title>{escape(M.VERSION + " — " + M.TITULO)}</dc:title>', core)
    core = re.sub(r'<dc:creator>.*?</dc:creator>', f'<dc:creator>{escape(C.EQUIPO)}</dc:creator>', core)
    core = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', '<cp:lastModifiedBy>Equipo del proyecto</cp:lastModifiedBy>', core)
    core = re.sub(r'(<dcterms:(?:created|modified)[^>]*>)[^<]*', r'\g<1>2026-09-30T00:00:00Z', core)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, STEM + '.docx')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            d = zin.read(info.filename)
            if info.filename == 'word/document.xml':
                d = new_doc.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                d = rels.encode('utf-8')
            elif info.filename == 'docProps/core.xml':
                d = core.encode('utf-8')
            elif info.filename == 'word/settings.xml':
                s = keep_image_resolution(d.decode('utf-8'))
                if 'w:updateFields' not in s:
                    s = re.sub(r'(<w:settings[^>]*>)', r'\1<w:updateFields w:val="true"/>', s, count=1)
                d = s.encode('utf-8')
            zi = zipfile.ZipInfo(info.filename, date_time=FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, d)
        for _, target, data in media.items:
            zi = zipfile.ZipInfo('word/' + target, date_time=FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
    build_md(os.path.join(out_dir, STEM + '.md'), headings, S)
    return headings


# ------------------------------------------------------------------ espejo Markdown
def _md(x):
    return str(x).replace('|', '\\|').replace('\n', '<br>')


def build_md(path, headings, S):
    L = [f'# {M.VERSION} — {M.TITULO}', '',
         f'> Espejo en Markdown de [`{STEM}.docx`]({STEM}.docx) (y su [PDF]({STEM}.pdf)), generado con '
         '`python docs/academico/tools/f27b/build.py f29h`. No se edita a mano. Las figuras están en el DOCX y el PDF.', '',
         f'**Integrantes:** {C.EQUIPO} · **Asesor:** {C.DOCENTE} · **Fecha:** {M.FECHA}', '']
    cap, sec = 0, 0
    pending_cap = None
    for st, txt in headings:
        if st == 'Ttulo1' and txt.startswith('CAPÍTULO'):
            cap, sec = int(txt.split()[1]), 0
            pending_cap = txt
            continue
        if st == 'Ttulo1':
            if pending_cap:
                L += [f'## {pending_cap}. {txt}', '']
                pending_cap = None
                continue
            if txt in FINALES:
                L += [f'## {txt}', '']
                blocks = S[txt]
            else:
                continue
        else:
            sec += 1
            L += [f'### {cap}.{sec}. {txt}', '']
            blocks = S[txt]
        for b in blocks:
            if b[0] == 'p':
                L += [b[1], '']
            elif b[0] == 'note':
                L += [f'*{b[1]}*', '']
            elif b[0] == 'ul':
                L += [f'- {x}' for x in b[1]] + ['']
            elif b[0] == 'table':
                L += ['| ' + ' | '.join(b[1]) + ' |', '|' + '---|' * len(b[1])]
                L += ['| ' + ' | '.join(_md(c) for c in r) + ' |' for r in b[2]] + ['']
            elif b[0] == 'img':
                L += [f'*{b[2]} (imagen en el DOCX: `{b[1]}`)*', '']
    L += ['## Anexos gráficos (páginas horizontales del DOCX)', ''] + [f'- {c} (`{r}`)' for r, c in M.ANEXOS_IMG]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(re.sub(r'\n{3,}', '\n\n', '\n'.join(L)).rstrip() + '\n')


def sha256(path):
    with open(path, 'rb') as f:
        data = f.read()
    if path.endswith(('.md', '.py')):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


FUENTES = [
    (TEMPLATE, 'Plantilla oficial del informe final (estructura, portada, estilos y tabla de contenido)'),
    ('docs/academico/tools/f27b/m_informe.py', 'Contenido de cada sección'),
    ('docs/academico/tools/f27b/f29h.py', 'Relleno de la plantilla, anexos horizontales y espejo Markdown'),
    ('docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png', 'Figura 1 (F29)'),
    ('docs/v1.1/powerdesigner/exports/CL-01-clases-del-dominio.png', 'Figura 2 (F23)'),
    ('docs/v1.1/powerdesigner/exports/PDM-01-esquema-completo.png', 'Figura 3 (F23)'),
    ('docs/v1.1/powerdesigner/exports/DE-01-despliegue.png', 'Figura 4 (F23)'),
    ('docs/academico/powerdesigner/exports/F3_BPMN_ASIS.png', 'Anexo A (F29)'),
    ('docs/academico/powerdesigner/exports/F5_BPMN_TOBE.png', 'Anexo B (F29)'),
    ('docs/academico/powerdesigner/exports/F8_Casos_de_Uso_Academicos.png', 'Anexo C (F29)'),
]


def build_registro(path, root):
    L = ['# F29H — Registro de generación del Informe Final v1', '',
         '> Generado por `f29h.py`. Documenta las fuentes, las decisiones y los comandos del informe final.', '',
         '## Fuentes', '', '| Archivo | Uso | SHA-256 |', '|---|---|---|']
    L += [f'| `{r}` | {u} | `{sha256(os.path.join(root, r))}` |' for r, u in FUENTES]
    L += ['', '## Decisiones', '',
          '1. **Estructura oficial.** Se conservan la portada, la tabla de contenido, los 14 capítulos con sus 53 secciones '
          'y los apartados finales (conclusiones, recomendaciones, referencias y anexos) de la plantilla.',
          '2. **Texto guía.** Se eliminan todos los párrafos en rojo de la plantilla, incluida la «Aclaración importante». '
          'Los títulos del capítulo 8, que la plantilla trae en rojo, se conservan sin ese color.',
          '3. **Contenido.** Sale de `m_informe.py`:',
          '   - las tablas se generan desde los modelos académicos (F2 a F11, F29C) y desde la evidencia de la F29D a la '
          'F29G;',
          '   - los estados (HECHO VERIFICADO, AS-IS PRELIMINAR, TO-BE PROPUESTO, SOFTWARE IMPLEMENTADO y EXPERIMENTAL) se '
          'declaran;',
          '   - no se afirma validación institucional, beneficios medidos, SLA, disponibilidad, rendimiento ni '
          'escalabilidad verificados;',
          '   - las fases F30 y posteriores solo aparecen como trabajo futuro.',
          '4. **Portada.** Lleva el título del proyecto y los tres integrantes. El código de alumno no está en el repositorio '
          'y queda «Pendiente»: lo completa el equipo.',
          '5. **Figuras.** Son exportaciones formales de PowerDesigner, incrustadas sin modificar. Los diagramas anchos '
          '(anexos A a C) van en páginas horizontales.',
          '6. **Tabla de contenido y reproducibilidad.** El campo de la tabla de contenido se actualiza al exportar el PDF '
          '(`topdf_toc.ps1`). El DOCX tiene fecha de ZIP fija y es reproducible; el PDF depende de Word.',
          '', '## Comandos', '', '```',
          'python docs/academico/tools/f27b/build.py f29h',
          'powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/informe-final/' + STEM + '.docx',
          '```']
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
