"""Construye F29H v2 desde su Markdown y la plantilla visual de Word."""

from pathlib import Path
import hashlib
import json
import re
from urllib.parse import quote

from PIL import Image
from docx import Document
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
STEM = 'F29H_Informe_Final_v2_Colegio_Andino'
ASSETS = ROOT / 'recursos-v2'
REPO = 'https://github.com/luivmz/saas-reclutamiento-multiempresa'
TOKEN = re.compile(r'(\{\{ref:[\w-]+\}\}|\[[^\]]+\]\(https?://[^ )]+\)|\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)')
FIGURES = json.loads((ASSETS / 'figuras.json').read_text(encoding='utf-8'))
TEXT = (ROOT / (STEM + '.md')).read_text(encoding='utf-8')
KEYS = re.findall(r'^\{\{fig:([\w-]+)\}\}$', TEXT, re.M)
assert set(KEYS) == set(FIGURES) and len(KEYS) == len(set(KEYS))
FIG_NUMBERS = {key: n for n, key in enumerate(KEYS, 1)}
TABLE_CAPTIONS = iter([
    'Problemas y prioridades del caso',
    'Macroactividades y responsables',
    'Actividades del proceso AS-IS',
    'Validación del diagnóstico por responsable',
    'Mejoras propuestas y requisitos',
    'Objetivos de mejora del proceso',
    'Actores del sistema',
    'Requerimientos funcionales de la línea base',
    'Requerimientos no funcionales',
    'Casos de uso académicos',
    'Alcance incluido en la línea base',
    'Exclusiones del alcance',
    'Herramientas del proyecto',
    'Criterios del plan de pruebas F29D',
    'Relaciones y restricciones del dominio',
    'Tecnologías del frontend',
    'Tecnologías del backend',
    'Referencias del corte documental',
    'Revisiones relevantes',
    'Servicios de Docker Compose',
    'Niveles de prueba',
    'Tipos de pruebas ejecutadas',
    'Casos y reglas con evidencia',
    'Herramientas de automatización',
    'Historial de integración continua',
    'Ejecuciones por revisión y fecha',
    'Defectos y regresiones',
    'Métricas de SonarQube V3',
    'Mecanismos de monitoreo local',
    'Paquetes de evidencia y trazabilidad',
])


def xml(tag, **attrs):
    element = OxmlElement('w:' + tag)
    for key, value in attrs.items():
        element.set(qn('w:' + key), str(value))
    return element


def field(p, command, cached):
    """Guarda el campo de Word con un valor visible antes de actualizarlo."""
    p.add_run()._r.append(xml('fldChar', fldCharType='begin'))
    instr = xml('instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = ' ' + command + ' '
    p.add_run()._r.append(instr)
    p.add_run()._r.append(xml('fldChar', fldCharType='separate'))
    p.add_run(cached)
    p.add_run()._r.append(xml('fldChar', fldCharType='end'))


def hyperlink(p, label, href):
    item = OxmlElement('w:hyperlink')
    item.set(qn('r:id'), p.part.relate_to(quote(href, safe=':/%#?=&@'), RELATIONSHIP_TYPE.HYPERLINK, is_external=True))
    run = xml('r')
    prop = xml('rPr')
    prop.append(xml('color', val='234A75'))
    prop.append(xml('u', val='single'))
    run.append(prop)
    t = xml('t')
    t.text = label
    run.append(t)
    item.append(run)
    p._p.append(item)


def inline(p, text):
    for token in TOKEN.split(text):
        if token.startswith('{{ref:'):
            key = token[6:-2]
            p.add_run('figura ')
            field(p, 'REF Fig_' + key.replace('-', '_') + ' \\h', str(FIG_NUMBERS[key]))
        elif token.startswith('[') and '](' in token:
            label, address = token[1:-1].split('](', 1)
            hyperlink(p, label, address)
        elif token.startswith('**') and token.endswith('**'):
            p.add_run(token[2:-2]).bold = True
        elif token.startswith('*') and token.endswith('*'):
            p.add_run(token[1:-1]).italic = True
        elif token.startswith('`') and token.endswith('`'):
            p.add_run(token[1:-1]).font.name = 'Consolas'
        elif token:
            p.add_run(token)


def replace_text(element, value):
    texts = list(element.iter(qn('w:t')))
    assert texts
    original = texts[0]
    for node in texts[1:]:
        node.text = ''
    original.text = value


def open_template():
    doc = Document(ROOT / 'plantillas' / 'PLANTILLA_INFORME_UC_PORTADA_FORMATADA.docx')
    body = doc._element.body
    elements = list(body)
    values = {
        3: 'UNIVERSIDAD CONTINENTAL',
        4: 'FACULTAD DE INGENIERÍA\nIngeniería de Sistemas e Informática',
        7: 'Pruebas y Calidad de Software',
        9: 'SaaS Reclutamiento Multiempresa\nCaso Colegio Andino de Huancayo',
        11: 'Dr. Maglioni Arana Caparachin',
        13: '28607',
        15: 'Coronacion Meza Fredy',
        16: 'Peña Arroyo Anthony',
        17: 'Vila Meza Luis Antonio',
        23: 'Huancayo, Perú · 2026',
    }
    assert 'ARQUITECTU' in ''.join(elements[7].itertext())
    for idx, value in values.items():
        if '\n' not in value:
            replace_text(elements[idx], value)
            continue
        title, subtitle = value.split('\n')
        replace_text(elements[idx], title)
        run = next(elements[idx].iter(qn('w:r')))
        node = next(run.iter(qn('w:t')))
        # El título y el caso comparten el estilo del campo TEMA.
        br = xml('br')
        node.addnext(br)
        t = xml('t')
        t.text = subtitle
        br.addnext(t)
    for idx, child in enumerate(elements):
        if idx in (18, 19, 20) or (idx >= 24 and child.tag != qn('w:sectPr')):
            body.remove(child)
    university = doc.paragraphs[3]
    university.alignment = WD_ALIGN_PARAGRAPH.CENTER
    university.paragraph_format.left_indent = Inches(0)
    university.paragraph_format.right_indent = Inches(0)
    for p in doc.sections[0].header.paragraphs:
        text = ''.join(t.text or '' for t in p._p.iter(qn('w:t')))
        if 'TEMA' in text:
            replace_text(p._p, 'RECLUTAMIENTO MULTIEMPRESA | NRC 28607')
    doc.core_properties.title = 'Informe final SaaS Reclutamiento Multiempresa'
    doc.core_properties.subject = 'Caso académico Colegio Andino de Huancayo'
    doc.core_properties.author = 'Coronacion Meza Fredy · Peña Arroyo Anthony · Vila Meza Luis Antonio'
    doc.core_properties.keywords = 'reclutamiento, arquitectura, pruebas, Universidad Continental'
    doc.core_properties.comments = ''
    doc.core_properties.category = 'Informe académico'
    update = doc.settings._element.find(qn('w:updateFields'))
    if update is None:
        doc.settings._element.append(xml('updateFields', val='true'))
    else:
        update.set(qn('w:val'), 'true')
    return doc


def configure_body(doc):
    normal = doc.styles['Normal']
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08
    normal.paragraph_format.widow_control = True
    try:
        caption = doc.styles['Caption']
    except KeyError:
        caption = doc.styles.add_style('Caption', WD_STYLE_TYPE.PARAGRAPH)
    caption.base_style = normal
    caption.font.name = 'Arial'
    caption.font.size = Pt(10)
    caption.font.bold = True
    caption.font.italic = False
    caption.font.color.rgb = RGBColor.from_string('234A75')
    caption.paragraph_format.space_before = Pt(9)
    caption.paragraph_format.space_after = Pt(5)
    caption.paragraph_format.keep_with_next = True
    for name in ('TOC 1', 'TOC 2', 'Table of Figures'):
        try:
            index_style = doc.styles[name]
        except KeyError:
            index_style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH, builtin=True)
        index_style.base_style = normal
        index_style.font.name = 'Arial'
        index_style.font.size = Pt(10)
        index_style.paragraph_format.left_indent = Inches(.16 if name == 'TOC 2' else 0)
        index_style.paragraph_format.space_before = Pt(0)
        index_style.paragraph_format.space_after = Pt(2)
        index_style.paragraph_format.line_spacing = 1

    for level in [1, 2]:
        style = doc.styles['Heading ' + str(level)]
        style.paragraph_format.space_after = Pt(5)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.keep_together = True


def frontmatter(doc):
    title = doc.add_paragraph('Contenido general')
    title.paragraph_format.page_break_before = True
    title.runs[0].bold = True
    title.runs[0].font.size = Pt(17)
    title.paragraph_format.keep_with_next = True
    field(doc.add_paragraph(), r'TOC \o "1-2" \h \z \u', 'Índice del informe')
    title = doc.add_paragraph('Índice de figuras')
    title.paragraph_format.page_break_before = True
    title.runs[0].bold = True
    title.runs[0].font.size = Pt(17)
    title.paragraph_format.keep_with_next = True
    field(doc.add_paragraph(), r'TOC \h \z \c "Figura"', 'Índice de figuras')
    title = doc.add_paragraph('Índice de tablas')
    title.paragraph_format.page_break_before = True
    title.runs[0].bold = True
    title.runs[0].font.size = Pt(17)
    title.paragraph_format.keep_with_next = True
    field(doc.add_paragraph(), r'TOC \h \z \c "Tabla"', 'Índice de tablas')


def caption(doc, category, number, title, key=None):
    p = doc.add_paragraph(style='Caption')
    p.add_run(category + ' ')
    if key:
        ident = number + 500
        p._p.append(xml('bookmarkStart', id=ident, name='Fig_' + key.replace('-', '_')))
    field(p, 'SEQ ' + category + ' \\* ARABIC', str(number))
    if key:
        p._p.append(xml('bookmarkEnd', id=ident))
    p.add_run('. ' + title)
    return p


def figure(doc, key):
    figure = FIGURES[key]
    file = ASSETS / figure['file']
    assert figure['sha256'] == hashlib.sha256(file.read_bytes()).hexdigest()
    caption(doc, 'Figura', FIG_NUMBERS[key], figure['title'], key)
    # Las láminas reúnen título, imagen y procedencia en un bloque.
    section = doc.sections[-1]
    usable = (section.page_width - section.left_margin - section.right_margin) / Inches(1)
    with Image.open(file) as im:
        width, height = im.size
    max_height = 5.55 if key == 'datos' else 6.0
    if key in ('asis', 'tobe'):
        max_height = 6.9
    display = min(usable, max_height * width / height)
    imgp = doc.add_paragraph()
    imgp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    imgp.paragraph_format.keep_with_next = True
    imgp.paragraph_format.space_after = Pt(4)
    shape = imgp.add_run().add_picture(str(file), width=Inches(display))
    shape._inline.docPr.set('descr', figure['description'])
    p = doc.add_paragraph()
    p.paragraph_format.keep_together = True
    p.paragraph_format.space_after = Pt(9)
    run = p.add_run(figure['description'] + ' ')
    run.font.size = Pt(9)
    run = p.add_run('Procedencia ' + figure['commit'][:7] + '. ')
    run.font.size = Pt(9)
    source = figure['source']
    if source.startswith('docs/'):
        hyperlink(p, 'Archivo de origen', f"{REPO}/blob/{figure['commit']}/{source}")
    else:
        run = p.add_run('Captura local inventariada en el registro v2.')
        run.font.size = Pt(9)


def cell_contents(cell, text, head):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.02
    inline(p, text)
    for r in p.runs:
        r.font.size = Pt(9)
        if head:
            r.bold = True


WIDTHS = {
    1: [.065, .155, .245, .17, .265, .10],
    6: [.16, .72, .12],
    12: [.23, .77],
    15: [.30, .70],
    19: [.26, .74],
    22: [.27, .73],
    23: [.32, .68],
    27: [.19, .16, .48, .17],
    28: [.27, .23, .50],
    29: [.29, .71],
    3: [.10, .34, .56],
    5: [.09, .24, .55, .12],
    8: [.09, .25, .46, .20],
    9: [.09, .19, .17, .39, .16],
    10: [.09, .28, .47, .16],
    26: [.14, .17, .13, .10, .29, .17],
}


def table(doc, rows, number):
    title = next(TABLE_CAPTIONS)
    caption(doc, 'Tabla', number, title)
    count = len(rows[0])
    assert all(len(row) == count for row in rows), (title, rows[0], [r for r in rows if len(r) != count])
    weights = WIDTHS.get(number, [1 / count] * count)
    assert len(weights) == count, (number, title, count)
    tbl = doc.add_table(rows=len(rows), cols=count)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    section = doc.sections[-1]
    width = section.page_width - section.left_margin - section.right_margin
    for col, weight in zip(tbl.columns, weights):
        col.width = int(width * weight)
    border = xml('tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        border.append(xml(side, val='single', sz='5', color='D4DCE5'))
    tbl._tbl.tblPr.append(border)
    margin = xml('tblCellMar')
    for side, value in [('top', 65), ('left', 83), ('bottom', 65), ('right', 83)]:
        margin.append(xml(side, w=value, type='dxa'))
    tbl._tbl.tblPr.append(margin)
    for idx, values in enumerate(rows):
        row = tbl.rows[idx]
        trprop = row._tr.get_or_add_trPr()
        trprop.append(xml('cantSplit'))
        if idx == 0:
            trprop.append(xml('tblHeader', val='true'))
        shade = 'DCE9F4' if idx == 0 else ('F4F7FA' if idx % 2 == 0 else 'FFFFFF')
        for cell, text, weight in zip(row.cells, values, weights):
            cell.width = int(width * weight)
            cell._tc.get_or_add_tcPr().append(xml('shd', val='clear', fill=shade))
            cell_contents(cell, text, idx == 0)


def new_orientation(doc, landscape):
    sect = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sect.different_first_page_header_footer = False
    sect.orientation = WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    dims = [11906, 16838] if not landscape else [16838, 11906]
    sect.page_width, sect.page_height = (int(dim * 635) for dim in dims)


def build():
    doc = open_template()
    configure_body(doc)
    frontmatter(doc)
    lines = TEXT.splitlines()[1:]
    table_number = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line.startswith('## '):
            p = doc.add_heading(line[3:], level=1)
            if line.startswith(('## CAPÍTULO 1.', '## ANEXOS')):
                p.paragraph_format.page_break_before = True
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=2)
        elif line.startswith('|'):
            rows = [line.strip('|').strip().split('|')]
            i += 1  # Separador de encabezado Markdown.
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i].strip().strip('|').split('|'))
                i += 1
            table_number += 1
            table(doc, [[col.strip() for col in row] for row in rows], table_number)
        elif line.startswith('{{fig:'):
            key = line[6:-2]
            if key == 'datos':
                new_orientation(doc, True)
            figure(doc, key)
            if key == 'datos':
                new_orientation(doc, False)
        elif line.startswith('- '):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(.20)
            p.paragraph_format.first_line_indent = Inches(-.16)
            p.add_run('•  ')
            inline(p, line[2:])
        else:
            inline(doc.add_paragraph(), line)
    assert next(TABLE_CAPTIONS, None) is None, table_number
    output = ROOT / (STEM + '.docx')
    doc.save(output)
    print(f'{output.name} | {len(FIG_NUMBERS)} figuras | {table_number} tablas')


if __name__ == '__main__':
    build()
