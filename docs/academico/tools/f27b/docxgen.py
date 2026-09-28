"""Relleno de las plantillas oficiales (Formatos 02 a 08) y espejo en Markdown.

Se conserva el paquete de la plantilla (estilos, numeración, cabecera con el logotipo,
márgenes y página). Del cuerpo se reutilizan el título, el encabezado «Datos generales»
y su tabla, que se rellena. El resto del cuerpo se genera con el mismo estilo de
encabezado numerado (Prrafodelista, numId 1) y el estilo de tabla de la plantilla
(Tablaconcuadrcula, sangría 284). Las plantillas originales no se modifican: se lee una
copia en memoria y se escribe un DOCX nuevo.
"""
import os
import re
import struct
import sys
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'phase-24', 'tools'))
from docxlib import split_blocks  # noqa: E402  (reutiliza el separador de bloques de la F24)

W_TEXT = 8216  # ancho útil de las tablas de la plantilla, en twips


def _runs(text, bold=False, italic=False, sz=None, color=None):
    """Convierte texto con **negrita** en runs de WordprocessingML."""
    out = []
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    for part in parts:
        if not part:
            continue
        b = bold
        mono = False
        if part.startswith('**') and part.endswith('**'):
            part, b = part[2:-2], True
        elif part.startswith('`') and part.endswith('`') and len(part) > 1:
            part, mono = part[1:-1], True
        rpr = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if mono else ''
        if b:
            rpr += '<w:b/><w:bCs/>'
        if italic:
            rpr += '<w:i/><w:iCs/>'
        if color:
            rpr += f'<w:color w:val="{color}"/>'
        if sz:
            rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        rpr = f'<w:rPr>{rpr}</w:rPr>' if rpr else ''
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return ''.join(out)


def para(text='', bold=False, italic=False, sz=None, ind=284, jc=None, after=None,
         keep_next=False, color=None, shade=None):
    ppr = ''
    if keep_next:
        ppr += '<w:keepNext/>'
    if shade:
        ppr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    if after is not None:
        ppr += f'<w:spacing w:after="{after}"/>'
    if ind:
        ppr += f'<w:ind w:left="{ind}"/>'
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    return f'<w:p><w:pPr>{ppr}</w:pPr>{_runs(text, bold, italic, sz, color)}</w:p>'


def heading(text):
    """Encabezado numerado con el mismo formato que los de la plantilla."""
    return ('<w:p><w:pPr><w:pStyle w:val="Prrafodelista"/><w:keepNext/><w:numPr><w:ilvl w:val="0"/>'
            '<w:numId w:val="1"/></w:numPr><w:ind w:left="284" w:hanging="284"/><w:rPr><w:b/><w:bCs/></w:rPr>'
            f'</w:pPr>{_runs(text, bold=True)}</w:p>')


def _cell(text, width, sz, bold=False, jc=None, fill=None):
    paras = []
    for line in str(text).split('\n'):
        ppr = f'<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="{jc or "left"}"/>'
        paras.append(f'<w:p><w:pPr>{ppr}</w:pPr>{_runs(line, bold=bold, sz=sz)}</w:p>')
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}</w:tcPr>{"".join(paras)}</w:tc>'


def table(headers, rows, widths=None, sz=18, header_fill='D9E2F3'):
    n = len(headers) if headers else len(rows[0])
    if not widths:
        widths = [W_TEXT // n] * n
    scale = W_TEXT / sum(widths)
    widths = [int(w * scale) for w in widths]
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    xml = [('<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/>'
            f'<w:tblW w:w="{W_TEXT}" w:type="dxa"/><w:tblInd w:w="284" w:type="dxa"/>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
            'w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>')]
    if headers:
        cells = ''.join(_cell(h, w, sz, bold=True, jc='center', fill=header_fill) for h, w in zip(headers, widths))
        xml.append(f'<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{cells}</w:tr>')
    for row in rows:
        cells = ''.join(_cell(c, w, sz) for c, w in zip(row, widths))
        xml.append(f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{cells}</w:tr>')
    xml.append('</w:tbl>')
    return ''.join(xml) + para('', after=0)


def box(lines, sz=None, fill=None):
    """Recuadro de una celda, como los recuadros de respuesta de la plantilla."""
    paras = ''.join(f'<w:p><w:pPr><w:spacing w:after="60" w:line="252" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                    f'{_runs(l, sz=sz)}</w:p>' for l in lines)
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
    return ('<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/>'
            f'<w:tblW w:w="{W_TEXT}" w:type="dxa"/><w:tblInd w:w="284" w:type="dxa"/>'
            '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" '
            f'w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid><w:gridCol w:w="{W_TEXT}"/></w:tblGrid>'
            f'<w:tr><w:tc><w:tcPr><w:tcW w:w="{W_TEXT}" w:type="dxa"/>{shd}</w:tcPr>{paras}</w:tc></w:tr></w:tbl>'
            + para('', after=0))


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    return struct.unpack('>II', head[16:24])


def image_xml(rid, docpr_id, name, cx, cy):
    return ('<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{docpr_id}" name="{escape(name)}"/><wp:cNvGraphicFramePr>'
            '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
            '</wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="{escape(name)}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r></w:p>')


PAGEBREAK = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

EMU_CM = 914400 / 2.54
TWIP_CM = 1440 / 2.54


def image_data(path, crop=None):
    """Bytes y tamaño en píxeles de un PNG; con crop=(x0, x1), la franja horizontal indicada (recorte sin retoque)."""
    if not crop:
        w, h = png_size(path)
        with open(path, 'rb') as f:
            return f.read(), w, h
    import io
    from PIL import Image
    im = Image.open(path)
    part = im.crop((int(im.width * crop[0]), 0, int(im.width * crop[1]), im.height))
    buf = io.BytesIO()
    part.save(buf, 'PNG')
    return buf.getvalue(), part.width, part.height


def sect_variant(sect, landscape=False, keep_first=True):
    """Copia de las propiedades de sección de la plantilla: apaisada (ancho y alto intercambiados) o sin la
    cabecera y el pie de primera página (para que no se repitan al empezar cada sección nueva)."""
    s = sect
    if not keep_first:
        s = s.replace('<w:titlePg/>', '')
        s = re.sub(r'<w:(?:header|footer)Reference w:type="first" r:id="rId\d+"/>', '', s)
    if landscape:
        m = re.search(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"\s*/>', s)
        s = s.replace(m.group(0), f'<w:pgSz w:w="{m.group(2)}" w:h="{m.group(1)}" w:orient="landscape"/>')
    return s


def landscape_size_cm(sect):
    """Ancho y alto útiles (cm) de la página apaisada que resulta de las propiedades de sección."""
    w = int(re.search(r'<w:pgSz w:w="(\d+)"', sect).group(1))
    h = int(re.search(r'<w:pgSz w:w="\d+" w:h="(\d+)"', sect).group(1))
    mar = {k: int(v) for k, v in re.findall(r'w:(top|right|bottom|left)="(\d+)"', re.search(r'<w:pgMar[^>]*/>', sect).group(0))}
    return (h - mar['left'] - mar['right']) / TWIP_CM, (w - mar['top'] - mar['bottom']) / TWIP_CM


def with_sect(paragraph, sect):
    """Añade propiedades de sección a un párrafo: la sección termina en él."""
    return paragraph.replace('</w:pPr>', sect + '</w:pPr>', 1)


def wide_image_parts(sect, first, rid, docpr, name, w, h, caption_xml, close_prev=True):
    """Página horizontal con una imagen: cierra la sección anterior (vertical), dibuja la imagen al ancho útil y
    termina la sección apaisada en el pie de figura. Si la anterior ya era una página horizontal (close_prev=False),
    no hay sección vertical que cerrar."""
    tw, th = landscape_size_cm(sect)
    cx = int(tw * 0.99 * EMU_CM)
    cy = int(cx * h / w)
    max_cy = int((th - 2.2) * EMU_CM)
    if cy > max_cy:
        cy = max_cy
        cx = int(cy * w / h)
    close = ['<w:p><w:pPr><w:spacing w:after="0"/>' + sect_variant(sect, keep_first=first) + '</w:pPr></w:p>'] if close_prev else []
    return close + [image_xml(rid, docpr, name, cx, cy),
            with_sect(caption_xml, sect_variant(sect, landscape=True, keep_first=False))]


def keep_image_resolution(settings):
    """Marca «No comprimir las imágenes del archivo» para que las exportaciones conserven su resolución."""
    if 'w:doNotAutoCompressPictures' in settings:
        return settings
    for anchor in ('<w:forceUpgrade', '<w:captions', '<w:shapeDefaults', '<w:decimalSymbol', '<w:listSeparator',
                   '</w:settings>'):
        if anchor in settings:
            return settings.replace(anchor, '<w:doNotAutoCompressPictures/>' + anchor, 1)
    return settings


def _fill_datos(tbl, values):
    """Rellena la tercera celda de cada fila de la tabla «Datos generales»."""
    def fill_row(m):
        row = m.group(0)
        label = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', row)).split(':')[0].strip()
        val = values.get(label)
        if val is None:
            raise KeyError(f'Sin valor para el campo «{label}» de Datos generales')
        cells = re.findall(r'<w:tc>.*?</w:tc>', row, re.S)
        last = cells[-1]
        new_last = re.sub(r'<w:p [^>]*/>', f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{_runs(val)}</w:p>', last, count=1)
        return row.replace(last, new_last)
    return re.sub(r'<w:tr[ >].*?</w:tr>', fill_row, tbl, flags=re.S)


class Doc:
    """Documento compuesto por elementos que se emiten a DOCX y a Markdown."""

    def __init__(self):
        self.items = []

    def h(self, t): self.items.append(('h', t)); return self
    def instr(self, t): self.items.append(('instr', t)); return self
    def sub(self, t): self.items.append(('sub', t)); return self
    def p(self, t): self.items.append(('p', t)); return self
    def bullets(self, xs): self.items.append(('bullets', list(xs))); return self
    def table(self, headers, rows, widths=None, sz=18): self.items.append(('table', headers, rows, widths, sz)); return self
    def kv(self, rows, widths=(28, 72), sz=18): self.items.append(('kv', rows, widths, sz)); return self
    def box(self, lines): self.items.append(('box', list(lines))); return self
    def note(self, title, lines): self.items.append(('note', title, list(lines))); return self
    def img(self, path, caption, width_cm=16.0, crop=None):
        """Imagen en la página vertical. crop=(x0, x1): ampliación de esa franja del ancho, sin retoque."""
        self.items.append(('img', path, caption, width_cm) + ((crop,) if crop else ()))
        return self

    def wide_img(self, path, caption, crop=None):
        """Imagen en su propia página horizontal (sección apaisada), al ancho útil de la página. crop=(x0, x1),
        fracciones del ancho: ampliación de esa franja de la imagen, sin retoque (recorte en memoria)."""
        self.items.append(('wimg', path, caption, crop))
        return self
    def pagebreak(self): self.items.append(('pb',)); return self


def build_docx(template, out_path, datos, doc, title=None):
    zin = zipfile.ZipFile(template)
    document = zin.read('word/document.xml').decode('utf-8')
    rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
    head, rest = document.split('<w:body>', 1)
    body, tail = rest.rsplit('</w:body>', 1)
    blocks = split_blocks(body)
    first_tbl = next(i for i, b in enumerate(blocks) if b[0] == 'w:tbl')
    sect = blocks[-1][1]
    assert 'w:sectPr' in sect
    parts = [b[1] for b in blocks[:first_tbl]]
    parts.append(_fill_datos(blocks[first_tbl][1], datos))
    parts.append(para('', after=0))
    media = []
    rid_n = 100
    docpr = 100
    wide = 0
    for i, it in enumerate(doc.items):
        k = it[0]
        prev = doc.items[i - 1][0] if i else None
        if k == 'h':
            parts.append(heading(it[1]))
        elif k == 'instr':
            parts.append(para(it[1], italic=True, sz=18, color='595959', after=80, keep_next=True))
        elif k == 'sub':
            parts.append(para(it[1], bold=True, after=60, keep_next=True))
        elif k == 'p':
            parts.append(para(it[1], after=100))
        elif k == 'bullets':
            for x in it[1]:
                parts.append(para('• ' + x, after=40, ind=567))
            parts.append(para('', after=0))
        elif k == 'table':
            parts.append(table(it[1], it[2], it[3], it[4]))
        elif k == 'kv':
            parts.append(table(None, it[1], list(it[2]), it[3]))
        elif k == 'box':
            parts.append(box(it[1]))
        elif k == 'note':
            parts.append(box([f'**{it[1]}**'] + it[2], sz=18, fill='FFF2CC'))
        elif k in ('img', 'wimg'):
            path, caption = it[1], it[2]
            data, w, h = image_data(path, it[3] if k == 'wimg' else (it[4] if len(it) > 4 else None))
            rid_n += 1
            docpr += 1
            rid = f'rId{rid_n}'
            target = f'media/f27b_{len(media) + 1}.png'
            media.append((target, data))
            rels = rels.replace('</Relationships>',
                                f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                                f'relationships/image" Target="{target}"/></Relationships>')
            cap = para(caption, italic=True, sz=18, jc='center', after=160)
            if k == 'wimg':
                parts += wide_image_parts(sect, not wide, rid, docpr, os.path.basename(path), w, h, cap,
                                          close_prev=prev != 'wimg')
                wide += 1
                continue
            width_cm = it[3]
            cx = int(width_cm / 2.54 * 914400)
            cy = int(cx * h / w)
            max_cy = int(22.5 / 2.54 * 914400)
            if cy > max_cy:
                cy = max_cy
                cx = int(cy * w / h)
            parts.append(image_xml(rid, docpr, os.path.basename(path), cx, cy))
            parts.append(cap)
        elif k == 'pb':
            parts.append(PAGEBREAK)
    parts.append(sect_variant(sect, keep_first=not wide))
    new_doc = head + '<w:body>' + ''.join(parts) + '</w:body>' + tail
    core = zin.read('docProps/core.xml').decode('utf-8')
    if title:
        core = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', f'<dc:title>{escape(title)}</dc:title>', core)
    core = re.sub(r'<dc:creator>.*?</dc:creator>', '<dc:creator>Coronacion Meza Fredy; Peña Arroyo Anthony; '
                  'Vila Meza Luis Antonio</dc:creator>', core)
    core = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', '<cp:lastModifiedBy>Equipo del proyecto'
                  '</cp:lastModifiedBy>', core)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'word/document.xml':
                data = new_doc.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                data = rels.encode('utf-8')
            elif info.filename == 'docProps/core.xml':
                data = core.encode('utf-8')
            elif info.filename == 'word/settings.xml' and wide:
                data = keep_image_resolution(data.decode('utf-8')).encode('utf-8')
            zout.writestr(info, data)
        for target, data in media:
            info = zipfile.ZipInfo('word/' + target, date_time=(2026, 9, 26, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(info, data)


def _md_cell(x):
    return str(x).replace('|', '\\|').replace('\n', '<br>')


def build_md(out_path, title, datos, doc, preface='', start=None):
    rel = lambda p: os.path.relpath(p, os.path.dirname(out_path)).replace(os.sep, '/')
    lines = [f'# {title}', '']
    if preface:
        lines += [preface, '']
    if datos:
        lines += ['## 1. Datos generales del proyecto', '', '| Campo | Valor |', '|---|---|']
        lines += [f'| {k} | {_md_cell(v)} |' for k, v in datos.items()]
        lines.append('')
    n = start if start is not None else 2  # la plantilla numera «Datos generales del proyecto» como 1
    for it in doc.items:
        k = it[0]
        if k == 'h':
            lines += [f'## {n}. {it[1]}', '']
            n += 1
        elif k == 'instr':
            lines += [f'*{it[1]}*', '']
        elif k == 'sub':
            lines += [f'**{it[1]}**', '']
        elif k == 'p':
            lines += [it[1], '']
        elif k == 'bullets':
            lines += [f'- {x}' for x in it[1]] + ['']
        elif k in ('table', 'kv'):
            headers = it[1] if k == 'table' else ['Campo', 'Detalle']
            rows = it[2] if k == 'table' else it[1]
            lines += ['| ' + ' | '.join(_md_cell(h) for h in headers) + ' |',
                      '|' + '---|' * len(headers)]
            lines += ['| ' + ' | '.join(_md_cell(c) for c in r) + ' |' for r in rows]
            lines.append('')
        elif k == 'box':
            for l in it[1]:
                lines += [f'> {l}', '>']
            lines[-1] = ''
        elif k == 'note':
            lines += [f'> **{it[1]}**', '>']
            for l in it[2]:
                lines += [f'> {l}', '>']
            lines[-1] = ''
        elif (k == 'img' and len(it) < 5) or (k == 'wimg' and not it[3]):
            lines += [f'![{it[2]}]({rel(it[1])})', '', f'*{it[2]}*', '']
        elif k in ('img', 'wimg'):
            crop = it[3] if k == 'wimg' else it[4]
            lines += [f'*{it[2]}* (En el DOCX: ampliación de la franja del {round(crop[0] * 100)} % al '
                      f'{round(crop[1] * 100)} % del ancho de [`{os.path.basename(it[1])}`]({rel(it[1])}).)', '']
    text = '\n'.join(lines).rstrip() + '\n'
    text = re.sub(r'\n{3,}', '\n\n', text)
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


# ---------------------------------------------------------------------------------------------------------------
# Constructor sobre el paquete del F9 final (estilo visual académico del F9), usado por el F11 adaptado (Fase 28).
# El F9 se lee en memoria y nunca se modifica.
F9_BLUE = '1F4E79'
ARIAL = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial"/>'


def _f9_heading(text, level=1, page_break=False):
    size = 30 if level == 1 else 24
    pb = '<w:pageBreakBefore/>' if page_break else ''
    return (f'<w:p><w:pPr><w:pStyle w:val="Ttulo{level}"/><w:keepNext/>{pb}</w:pPr><w:r><w:rPr>{ARIAL}<w:b/>'
            f'<w:color w:val="{F9_BLUE}"/><w:sz w:val="{size}"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def _arial(runs):
    runs = runs.replace('<w:rPr>', '<w:rPr>' + ARIAL)
    return runs.replace('<w:r><w:t', f'<w:r><w:rPr>{ARIAL}</w:rPr><w:t')


def _f9_cell(text, width, header=False, sz=16):
    paras = []
    for line in str(text).split('\n'):
        runs = _arial(_runs(line, bold=header, sz=sz, color='FFFFFF' if header else None))
        jc = 'center' if header else 'left'
        paras.append(f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>{runs}</w:p>')
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{F9_BLUE}"/>' if header else ''
    mar = ('<w:tcMar><w:top w:w="60" w:type="dxa"/><w:start w:w="70" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/>'
           '<w:end w:w="70" w:type="dxa"/></w:tcMar>')
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}{mar}<w:vAlign w:val="center"/></w:tcPr>{"".join(paras)}</w:tc>'


def _f9_table(headers, rows, widths=None, sz=16, total=9380):
    n = len(headers) if headers else len(rows[0])
    widths = widths or [1] * n
    widths = [int(w * total / sum(widths)) for w in widths]
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    xml = [('<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
            'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>') % (total, grid)]
    if headers:
        xml.append('<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' +
                   ''.join(_f9_cell(h, w, True, sz) for h, w in zip(headers, widths)) + '</w:tr>')
    for r in rows:
        xml.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(_f9_cell(c, w, False, sz) for c, w in zip(r, widths)) + '</w:tr>')
    xml.append('</w:tbl>')
    return ''.join(xml) + '<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>'


def _replace_text(xml, old, new):
    if f'>{old}<' not in xml:
        raise ValueError('Texto de portada no encontrado: ' + old)
    return xml.replace(f'>{old}<', f'>{escape(new)}<', 1)


def build_docx_f9(base, out_path, cover, cover_note, header_text, doc, props, contents):
    """base: DOCX del F9 final (solo lectura). cover: [(texto_antiguo, texto_nuevo)] de la portada.
    cover_note: nota visible añadida en la portada. contents: títulos de la página «Contenido» (estática)."""
    zin = zipfile.ZipFile(base)
    document = zin.read('word/document.xml').decode('utf-8')
    rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
    head, rest = document.split('<w:body>', 1)
    body, tail = rest.rsplit('</w:body>', 1)
    blocks = split_blocks(body)
    toc_i = next(i for i, b in enumerate(blocks) if 'Tabla de contenido' in b[1])
    ver_i = next(i for i, b in enumerate(blocks) if 'Versión 1.1' in b[1])
    sect = blocks[-1][1]
    assert 'w:sectPr' in sect
    cover_blocks = [b[1] for b in blocks[:toc_i]]
    cover_blocks.insert(ver_i + 1, para(cover_note, italic=True, sz=18, jc='center', ind=0, after=60, color=F9_BLUE))
    cover_xml = ''.join(cover_blocks)
    for old, new in cover:
        cover_xml = _replace_text(cover_xml, old, new)
    parts = [cover_xml, _f9_heading('Contenido', 1, page_break=True)]
    for c in contents:
        parts.append(para(c, ind=0, after=40))
    media, rid_n, docpr, n, wide = [], 900, 900, 0, 0
    for i, it in enumerate(doc.items):
        k = it[0]
        prev = doc.items[i - 1][0] if i else None
        if k == 'h':
            n += 1
            parts.append(_f9_heading(f'{n}. {it[1]}', 1, page_break=(n == 1)))
        elif k == 'sub':
            parts.append(_f9_heading(it[1], 2))
        elif k == 'instr':
            parts.append(para(it[1], italic=True, sz=18, color='595959', after=80, ind=0, keep_next=True))
        elif k == 'p':
            parts.append(para(it[1], after=100, ind=0))
        elif k == 'bullets':
            for x in it[1]:
                parts.append(para('• ' + x, after=40, ind=284))
            parts.append(para('', after=0, ind=0))
        elif k == 'table':
            parts.append(_f9_table(it[1], it[2], it[3], it[4] or 16))
        elif k == 'kv':
            parts.append(_f9_table(None, it[1], list(it[2]), it[3]))
        elif k == 'box':
            parts.append(box(it[1]).replace('<w:tblInd w:w="284" w:type="dxa"/>', ''))
        elif k == 'note':
            parts.append(box([f'**{it[1]}**'] + it[2], sz=18, fill='FFF2CC').replace('<w:tblInd w:w="284" w:type="dxa"/>', ''))
        elif k in ('img', 'wimg'):
            path, caption = it[1], it[2]
            data, w, h = image_data(path, it[3] if k == 'wimg' else (it[4] if len(it) > 4 else None))
            rid_n += 1
            docpr += 1
            rid = f'rId{rid_n}'
            target = f'media/f28_{len(media) + 1}.png'
            media.append((target, data))
            rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                                f'officeDocument/2006/relationships/image" Target="{target}"/></Relationships>')
            cap = para(caption, italic=True, sz=18, jc='center', after=160, ind=0)
            if k == 'wimg':
                parts += wide_image_parts(sect, not wide, rid, docpr, os.path.basename(path), w, h, cap,
                                          close_prev=prev != 'wimg')
                wide += 1
                continue
            width_cm = it[3]
            cx = int(width_cm / 2.54 * 914400)
            cy = int(cx * h / w)
            max_cy = int(22.0 / 2.54 * 914400)
            if cy > max_cy:
                cy = max_cy
                cx = int(cy * w / h)
            parts.append(image_xml(rid, docpr, os.path.basename(path), cx, cy))
            parts.append(cap)
        elif k == 'pb':
            parts.append(PAGEBREAK)
    parts.append(sect_variant(sect, keep_first=not wide))
    new_doc = head + '<w:body>' + ''.join(parts) + '</w:body>' + tail
    used = set(re.findall(r'r:(?:embed|id|link|pict)="(rId\d+)"', new_doc))
    drop = set()

    def keep_rel(m):
        rid, typ, target = m.group(1), m.group(2), m.group(3)
        if typ.endswith('/image') and rid not in used:
            drop.add('word/' + target)
            return ''
        return m.group(0)
    rels = re.sub(r'<Relationship Id="(rId\d+)" Type="([^"]+)" Target="([^"]+)"/>', keep_rel, rels)
    header = zin.read('word/header1.xml').decode('utf-8')
    header = _replace_text(header, 'ALCANCE F9 | PRUEBAS Y CALIDAD DE SOFTWARE', header_text)
    core = zin.read('docProps/core.xml').decode('utf-8')
    for tag, val in props.items():
        pat = '<' + tag + '>.*?</' + tag + '>|<' + tag + '/>'
        core = re.sub(pat, lambda m, t=tag, v=val: '<' + t + '>' + escape(v) + '</' + t + '>', core, flags=re.S)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fixed = (2026, 9, 27, 0, 0, 0)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.filename in drop:
                continue
            data = zin.read(info.filename)
            if info.filename == 'word/document.xml':
                data = new_doc.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                data = rels.encode('utf-8')
            elif info.filename == 'word/header1.xml':
                data = header.encode('utf-8')
            elif info.filename == 'docProps/core.xml':
                data = core.encode('utf-8')
            elif info.filename == 'word/settings.xml' and wide:
                data = keep_image_resolution(data.decode('utf-8')).encode('utf-8')
            zi = zipfile.ZipInfo(info.filename, date_time=fixed)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
        for target, data in media:
            zi = zipfile.ZipInfo('word/' + target, date_time=fixed)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
