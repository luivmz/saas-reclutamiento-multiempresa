"""F33 — Consolidado Word del diseño funcional del motor inteligente (con diagramas).

Reutiliza el conversor Markdown → bloques de F30 y el paquete Word de F27B. Las imágenes Markdown
(`![texto](diagramas/x.png)`) se incrustan como imágenes reales en el DOCX.

Salida: docs/academico/diseno-inteligente/F33_Diseno_Motor_Inteligente.docx
El PDF se exporta después con Word: docs/academico/tools/f27b/topdf_toc.ps1 <docx>
Uso: python docs/academico/tools/f33/f33.py
"""
import os
import re
import struct
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'f27b'))
sys.path.insert(0, os.path.join(HERE, '..', 'f30'))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'diseno-inteligente'))
DOCX = os.path.join(OUT, 'F33_Diseno_Motor_Inteligente.docx')

from docxgen import image_xml  # noqa: E402
from docxpkg import FIXED_DATE, TEXT_W, write_docx  # noqa: E402
from f30 import md_blocks  # noqa: E402

ORDEN = ['README.md', 'F33_ADR_005_G0.md', 'F33_Diseno_Funcional_Motor_Inteligente.md',
         'F33_Matriz_Capacidades_y_Restricciones.md', 'F33_Flujos_Funcionales.md', 'F33_Mapa_F34_F40.md']
WP_NS = 'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"'
IMG = re.compile(r'^!\[([^\]]*)\]\(([^)]+\.png)\)\s*$')


def png_size(path):
    with open(path, 'rb') as f:
        return struct.unpack('>II', f.read(24)[16:24])


def blocks_with_images(md, images):
    """Sustituye cada imagen por un marcador de párrafo y luego por el dibujo incrustado."""
    lines = []
    for ln in md.split('\n'):
        m = IMG.match(ln.strip())
        if m:
            images.append(os.path.normpath(os.path.join(OUT, m.group(2))))
            lines += ['', f'@@IMG{len(images) - 1}@@', '']
        else:
            lines.append(ln)
    out = []
    for b in md_blocks('\n'.join(lines)):
        mk = re.fullmatch(r'@@IMG(\d+)@@', b[1]) if b[0] == 'p' else None
        if mk:
            i = int(mk.group(1))
            w, h = png_size(images[i])
            cx = TEXT_W * 635                       # ancho útil en EMU (1 twip = 635 EMU)
            cy = int(cx * h / w)
            max_cy = int(21.5 / 2.54 * 914400)      # límite de alto de página útil
            if cy > max_cy:
                cx, cy = int(cx * max_cy / cy), max_cy
            xml = image_xml(f'rIdImg{i}', 100 + i, os.path.basename(images[i]), cx, cy)
            out.append(('raw', xml.replace('<wp:inline ', f'<wp:inline {WP_NS} ', 1)))
        else:
            out.append(b)
    return out


def add_images(path, images):
    """Añade las imágenes al paquete: partes media, relaciones y tipo de contenido PNG."""
    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
    ct = files['[Content_Types].xml'].decode('utf-8')
    if 'Extension="png"' not in ct:
        ct = ct.replace('<Default Extension="xml"', '<Default Extension="png" ContentType="image/png"/>'
                        '<Default Extension="xml"', 1)
    files['[Content_Types].xml'] = ct.encode('utf-8')
    rels = files['word/_rels/document.xml.rels'].decode('utf-8')
    extra = ''.join(f'<Relationship Id="rIdImg{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                    f'relationships/image" Target="media/f33_img{i}.png"/>' for i in range(len(images)))
    files['word/_rels/document.xml.rels'] = rels.replace('</Relationships>', extra + '</Relationships>').encode('utf-8')
    for i, p in enumerate(images):
        with open(p, 'rb') as f:
            files[f'word/media/f33_img{i}.png'] = f.read()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            zi = zipfile.ZipInfo(name, date_time=FIXED_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    images = []
    blocks = [('h1', 'Contenido'), ('toc',), ('pagebreak',)]
    for i, name in enumerate(ORDEN):
        with open(os.path.join(OUT, name), encoding='utf-8') as f:
            b = blocks_with_images(f.read(), images)
        if i:
            blocks.append(('pagebreak',))
        blocks += b
    write_docx(DOCX, blocks, 'F33 — Diseño funcional del motor inteligente y ADR-005 / G0',
               'Coronacion Meza, Peña Arroyo, Vila Meza',
               header=('Área Informática', 'Pruebas y Calidad de Software — NRC 28607'),
               cover=('F33 — Diseño funcional del motor inteligente y ADR-005 / G0',
                      'SaaS Reclutamiento Multiempresa · Caso Colegio Andino de Huancayo',
                      'Versión 1 · 04/10/2026 · G0 = NO APROBADA · pendiente de auditoría'),
               footer_extra='F33 — Diseño motor inteligente')
    add_images(DOCX, images)
    print('escrito', os.path.basename(DOCX), 'con', len(images), 'imágenes')


if __name__ == '__main__':
    main()
