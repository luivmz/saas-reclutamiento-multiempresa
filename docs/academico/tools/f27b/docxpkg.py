"""Paquete Word generado desde cero (F29D): documento con cabecera y pie propios, estilos de título para la tabla de
contenido y un modelo de bloques que produce a la vez el DOCX y su espejo Markdown.

Se usa cuando la plantilla oficial solo existe en PDF (Plan de Pruebas del curso): la estructura y los títulos salen
de la plantilla, y la cabecera replica la suya. La fecha del ZIP es fija para que la salida sea reproducible.

Bloques: ('h1', texto) · ('h2', texto) · ('p', texto) · ('note', texto) · ('ul', [textos]) ·
         ('table', cabeceras, filas, fracciones_de_ancho) · ('pagebreak',) · ('toc',)
El texto admite **negrita** y `código`.
"""
import re
import zipfile
from xml.dom import minidom
from xml.sax.saxutils import escape

from docxgen import _runs

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
BLUE = '365F91'
FIXED_DATE = (2026, 9, 30, 0, 0, 0)
PAGE_W, PAGE_H = 12240, 15840                     # carta, como la plantilla del curso
MARGIN = dict(top=1985, right=1701, bottom=1418, left=1701, header=709, footer=709)
TEXT_W = PAGE_W - MARGIN['left'] - MARGIN['right']

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W_NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial" w:cs="Arial"/>
<w:sz w:val="20"/><w:szCs w:val="20"/><w:lang w:val="es-PE"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="360" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:bCs/><w:color w:val="{BLUE}"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:b/><w:bCs/><w:color w:val="{BLUE}"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W}"/></w:tabs><w:spacing w:after="60"/></w:pPr>
<w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W}"/></w:tabs><w:spacing w:after="40"/><w:ind w:left="284"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0"/></w:pPr></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>
<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/><w:tblPr><w:tblBorders>
<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
</w:tblBorders></w:tblPr></w:style>
</w:styles>'''


def header_xml(left, right):
    """Cabecera de la plantilla del curso: área a la izquierda, docente a la derecha y barra azul debajo."""
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {W_NS}>'
            '<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            f'<w:b/><w:sz w:val="26"/></w:rPr><w:t>{escape(left)}</w:t></w:r></w:p>'
            '<w:p><w:pPr><w:pStyle w:val="Header"/><w:pBdr><w:bottom w:val="single" w:sz="36" w:space="4" '
            'w:color="4F81BD"/></w:pBdr><w:jc w:val="right"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Calibri" '
            f'w:hAnsi="Calibri"/><w:b/><w:i/><w:color w:val="{BLUE}"/><w:sz w:val="18"/></w:rPr><w:t>{escape(right)}'
            '</w:t></w:r></w:p></w:hdr>')


def footer_xml(extra=''):
    extra_run = (f'<w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t xml:space="preserve">{escape(extra)}</w:t></w:r><w:r><w:tab/></w:r>'
                 if extra else '')
    jc = '' if extra else '<w:jc w:val="right"/>'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {W_NS}><w:p><w:pPr><w:pStyle w:val="Footer"/>'
            f'<w:tabs><w:tab w:val="right" w:pos="{TEXT_W}"/></w:tabs>{jc}</w:pPr>'
            f'{extra_run}<w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="18"/></w:rPr>'
            '<w:t xml:space="preserve">Página </w:t></w:r><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r>'
            '<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            '<w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')


def _p(text, style=None, sz=None, bold=False, italic=False, jc=None, after=None, before=None, color=None, keep=False):
    ppr = ''
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if keep:
        ppr += '<w:keepNext/>'
    if after is not None or before is not None:
        ppr += '<w:spacing' + (f' w:before="{before}"' if before is not None else '') + \
               (f' w:after="{after}"' if after is not None else '') + '/>'
    if jc:
        ppr += f'<w:jc w:val="{jc}"/>'
    return f'<w:p><w:pPr>{ppr}</w:pPr>{_runs(text, bold=bold, italic=italic, sz=sz, color=color)}</w:p>'


def _cell(text, width, header=False, sz=16, fill=None):
    paras = ''.join(f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/></w:pPr>'
                    f'{_runs(line, bold=header, sz=sz)}</w:p>' for line in (str(text).split('\n') or ['']))
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}</w:tcPr>{paras}</w:tc>'


def _table(headers, rows, fracs, sz=16):
    widths = [int(TEXT_W * f) for f in fracs[:-1]]
    widths.append(TEXT_W - sum(widths))
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = [f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="{TEXT_W}" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
           f'</w:tblPr><w:tblGrid>{grid}</w:tblGrid>',
           '<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' +
           ''.join(_cell(h, w, True, sz, 'D9D9D9') for h, w in zip(headers, widths)) + '</w:tr>']
    for r in rows:
        out.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(_cell(c, w, False, sz) for c, w in zip(r, widths)) + '</w:tr>')
    out.append('</w:tbl>')
    return ''.join(out) + '<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>'


def _toc(blocks):
    """Campo TOC con las entradas ya escritas (sin número de página): Word lo actualiza al abrir o exportar."""
    entries = ''.join(
        f'<w:p><w:pPr><w:pStyle w:val="{"TOC1" if b[0] == "h1" else "TOC2"}"/></w:pPr>{_runs(b[1])}</w:p>'
        for b in blocks if b[0] in ('h1', 'h2'))
    return ('<w:p><w:pPr><w:pStyle w:val="TOC1"/></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r></w:p>' + entries +
            '<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')


def body_xml(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'h1':
            out.append(_p(b[1], 'Heading1'))
        elif k == 'h2':
            out.append(_p(b[1], 'Heading2'))
        elif k == 'p':
            out.append(_p(b[1]))
        elif k == 'note':
            out.append(_p(b[1], italic=True, sz=18, color='404040'))
        elif k == 'ul':
            for item in b[1]:
                out.append('<w:p><w:pPr><w:spacing w:after="60"/><w:ind w:left="567" w:hanging="283"/></w:pPr>'
                           '<w:r><w:t>•</w:t></w:r><w:r><w:tab/></w:r>' + _runs(item) + '</w:p>')
        elif k == 'table':
            out.append(_table(b[1], b[2], b[3], sz=b[4] if len(b) > 4 else 16))
        elif k == 'pagebreak':
            out.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        elif k == 'toc':
            out.append(_toc(blocks))
        elif k == 'raw':
            out.append(b[1])
        else:
            raise ValueError(k)
    return ''.join(out)


def cover_xml(title, subtitle, date_label):
    """Portada con la disposición de la plantilla: título grande alineado a la derecha, proyecto y fecha."""
    return ('<w:p><w:pPr><w:spacing w:before="4200" w:after="360"/><w:jc w:val="right"/></w:pPr>'
            f'{_runs(title, bold=True, sz=48)}</w:p>'
            f'<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="right"/></w:pPr>{_runs(subtitle, bold=True, italic=True, sz=26, color="00B050")}</w:p>'
            f'<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="right"/></w:pPr>{_runs(date_label, bold=True, italic=True, sz=28)}</w:p>'
            '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')


def write_docx(path, blocks, title, creator, header=('Área Informática', 'Mg. Maglioni Arana Caparachin'),
               cover=None, footer_extra=''):
    sect = (f'<w:sectPr><w:headerReference w:type="default" r:id="rId3"/><w:footerReference w:type="default" r:id="rId4"/>'
            f'<w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/><w:pgMar w:top="{MARGIN["top"]}" w:right="{MARGIN["right"]}" '
            f'w:bottom="{MARGIN["bottom"]}" w:left="{MARGIN["left"]}" w:header="{MARGIN["header"]}" '
            f'w:footer="{MARGIN["footer"]}" w:gutter="0"/></w:sectPr>')
    body = (cover_xml(*cover) if cover else '') + body_xml(blocks)
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W_NS}><w:body>{body}{sect}'
                '</w:body></w:document>')
    files = {
        '[Content_Types].xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
        '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
        '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>',
        '_rels/.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>',
        'word/_rels/document.xml.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
        '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
        '</Relationships>',
        'word/document.xml': document,
        'word/styles.xml': STYLES,
        'word/settings.xml': f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {W_NS}><w:updateFields w:val="true"/>'
        '<w:defaultTabStop w:val="708"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting '
        'w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>',
        'word/header1.xml': header_xml(*header),
        'word/footer1.xml': footer_xml(footer_extra),
        'docProps/core.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f'<dc:title>{escape(title)}</dc:title><dc:creator>{escape(creator)}</dc:creator><cp:lastModifiedBy>Equipo del proyecto</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-09-30T00:00:00Z</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-09-30T00:00:00Z</dcterms:modified></cp:coreProperties>',
        'docProps/app.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties '
        'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>f27b docxpkg</Application></Properties>',
    }
    for name, data in files.items():
        if name.endswith('.xml') or name.endswith('.rels'):
            minidom.parseString(data.encode('utf-8'))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            zi = zipfile.ZipInfo(name, date_time=FIXED_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data.encode('utf-8'))


# ------------------------------------------------------------------ espejo Markdown
def _md_cell(x):
    return str(x).replace('|', '\\|').replace('\n', '<br>')


def to_md(blocks, title, preface=()):
    L = [f'# {title}', ''] + list(preface)
    for b in blocks:
        k = b[0]
        if k == 'h1':
            L += [f'## {b[1]}', '']
        elif k == 'h2':
            L += [f'### {b[1]}', '']
        elif k == 'p':
            L += [b[1], '']
        elif k == 'note':
            L += [f'*{b[1]}*', '']
        elif k == 'ul':
            L += [f'- {x}' for x in b[1]] + ['']
        elif k == 'table':
            L += ['| ' + ' | '.join(b[1]) + ' |', '|' + '---|' * len(b[1])]
            L += ['| ' + ' | '.join(_md_cell(c) for c in r) + ' |' for r in b[2]] + ['']
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(L)).rstrip() + '\n'
