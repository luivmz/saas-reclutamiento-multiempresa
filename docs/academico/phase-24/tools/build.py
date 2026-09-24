# -*- coding: utf-8 -*-
"""F24: produce the final Formato 09 v1.1 from the historical F9 DOCX.

Edits word/document.xml as a string (no reserialization) so the original
styles, cover, headers, footers and page borders are preserved.
Usage: python3 build.py <orig.docx> <out.docx> <exports_dir> <toc.json|->
"""
import json, os, re, shutil, struct, subprocess, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docxlib import split_blocks, txt

ORIG, OUT, EXPORTS, TOCJSON = sys.argv[1:5]
WORK = os.path.join(os.path.dirname(os.path.abspath(OUT)), 'build-work')
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK)
with zipfile.ZipFile(ORIG) as z:
    for n in z.namelist():
        assert not n.startswith('/') and '..' not in n, n
    z.extractall(WORK)

DOC = os.path.join(WORK, 'word', 'document.xml')
d = open(DOC, encoding='utf8').read()
b0 = d.index('<w:body>') + len('<w:body>')
b1 = d.rindex('<w:sectPr')
head, body, tail = d[:b0], d[b0:b1], d[b1:]
items = split_blocks(body)
assert ''.join(x for _, x in items) == body
assert len(items) == 215, len(items)

# ---------------------------------------------------------------- helpers
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def t(s):
    sp = ' xml:space="preserve"' if s != s.strip() else ''
    return f'<w:t{sp}>{esc(s)}</w:t>'

RPR = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial"/>'

def run(s, bold=False, italic=False, color='000000', sz=21, code=False):
    fonts = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas"/>' if code else RPR
    return (f'<w:r><w:rPr>{fonts}{"<w:b/>" if bold else ""}{"<w:i/>" if italic else ""}'
            f'<w:color w:val="{color}"/><w:sz w:val="{sz}"/></w:rPr>{t(s)}</w:r>')

def segs(spec, **kw):
    """spec: str or list of str / (str, 'b'|'i'|'c')."""
    if isinstance(spec, str):
        return run(spec, **kw)
    out = []
    for s in spec:
        if isinstance(s, tuple):
            txt_, f = s
            out.append(run(txt_, bold='b' in f, italic='i' in f, code='c' in f, **kw))
        else:
            out.append(run(s, **kw))
    return ''.join(out)

def body_p(spec):
    return f'<w:p><w:pPr><w:keepNext w:val="0"/><w:spacing w:after="100"/></w:pPr>{segs(spec)}</w:p>'

def bullet(spec):
    if isinstance(spec, str):
        spec = '• ' + spec
    else:
        spec = ['• '] + list(spec)
    return f'<w:p><w:pPr><w:spacing w:after="40"/><w:ind w:left="202" w:hanging="144"/></w:pPr>{segs(spec)}</w:p>'

def h1(s, page_break=True):
    pb = '<w:pageBreakBefore/>' if page_break else ''
    return (f'<w:p><w:pPr><w:pStyle w:val="Ttulo1"/>{pb}</w:pPr><w:r><w:rPr>{RPR}<w:b/>'
            f'<w:color w:val="1F4E79"/><w:sz w:val="30"/></w:rPr>{t(s)}</w:r></w:p>')

def h2(s):
    return (f'<w:p><w:pPr><w:pStyle w:val="Ttulo2"/></w:pPr><w:r><w:rPr>{RPR}<w:b/>'
            f'<w:color w:val="1F4E79"/><w:sz w:val="24"/></w:rPr>{t(s)}</w:r></w:p>')

def caption(spec):
    return (f'<w:p><w:pPr><w:spacing w:before="80" w:after="80"/><w:jc w:val="center"/></w:pPr>'
            f'{segs(spec, italic=True, color="666666", sz=18)}</w:p>')

SPACER = '<w:p><w:pPr><w:spacing w:after="40"/></w:pPr></w:p>'
MAR = ('<w:tcMar><w:top w:w="70" w:type="dxa"/><w:start w:w="80" w:type="dxa"/>'
       '<w:bottom w:w="70" w:type="dxa"/><w:end w:w="80" w:type="dxa"/></w:tcMar>')

def cell(content, width, align, header=False, shade=None):
    shd = f'<w:shd w:fill="{"1F4E79" if header else shade}"/>' if (header or shade) else ''
    color = 'FFFFFF' if header else '000000'
    b = '<w:b/>' if header else '<w:b w:val="0"/>'
    jc = 'center' if header else align
    if isinstance(content, str):
        content = [content]
    runs = []
    for s in content:
        f = ''
        if isinstance(s, tuple):
            s, f = s
        font = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas"/>' if 'c' in f else RPR
        bb = '<w:b/>' if ('b' in f or header) else b
        runs.append(f'<w:r><w:rPr>{font}{bb}<w:color w:val="{color}"/><w:sz w:val="17"/></w:rPr>{t(s)}</w:r>')
    return (f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{width}"/>{shd}<w:vAlign w:val="center"/>{MAR}</w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'
            f'<w:r/>{"".join(runs)}</w:p></w:tc>')

def table(headers, rows, widths, aligns):
    assert sum(widths) == 9216, sum(widths)
    assert len(headers) == len(widths) == len(aligns)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/><w:tblW w:type="auto" w:w="0"/>'
           '<w:jc w:val="center"/><w:tblLayout w:type="fixed"/><w:tblLook w:firstColumn="1" w:firstRow="1" '
           'w:lastColumn="0" w:lastRow="0" w:noHBand="0" w:noVBand="1" w:val="04A0"/></w:tblPr>'
           f'<w:tblGrid>{grid}</w:tblGrid>']
    out.append('<w:tr><w:trPr><w:tblHeader w:val="true"/></w:trPr>' +
               ''.join(cell(h, w, 'center', header=True) for h, w in zip(headers, widths)) + '</w:tr>')
    for i, r in enumerate(rows, start=1):
        assert len(r) == len(widths), r
        shade = 'F1F4F8' if i % 2 == 0 else None
        out.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>' +
                   ''.join(cell(c, w, a, shade=shade) for c, w, a in zip(r, widths, aligns)) + '</w:tr>')
    out.append('</w:tbl>')
    return ''.join(out)

def set_text(xml, new):
    ts = re.findall(r'<w:t(?:\s[^>]*)?>[^<]*</w:t>', xml)
    assert len(ts) == 1, (len(ts), txt(xml)[:80])
    return xml.replace(ts[0], t(new), 1)

def expect(k, prefix):
    assert txt(items[k][1]).startswith(prefix), (k, txt(items[k][1])[:80], prefix)

# ---------------------------------------------------------------- images
MEDIA = os.path.join(WORK, 'word', 'media')
RELS = os.path.join(WORK, 'word', '_rels', 'document.xml.rels')
rels = open(RELS, encoding='utf8').read()
EMU_CM = 360000
MAX_W, MAX_H = 15.6, 20.5
next_rid = [300]
next_docpr = [900001]

def png_size(path):
    with open(path, 'rb') as f:
        hdr = f.read(24)
    assert hdr[:8] == b'\x89PNG\r\n\x1a\n', path
    return struct.unpack('>II', hdr[16:24])

def add_image(src, name, rotate=False):
    global rels
    dst = os.path.join(MEDIA, name)
    shutil.copyfile(src, dst)
    if rotate:
        subprocess.run(['sips', '-r', '270', dst], check=True, capture_output=True)
    w, h = png_size(dst)
    wcm = MAX_W
    hcm = wcm * h / w
    if hcm > MAX_H:
        hcm = MAX_H
        wcm = hcm * w / h
    rid = f'rId{next_rid[0]}'
    next_rid[0] += 1
    rels = rels.replace('</Relationships>',
                        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        f'relationships/image" Target="media/{name}"/></Relationships>')
    return rid, int(wcm * EMU_CM), int(hcm * EMU_CM), (w, h)

def image_p(rid, cx, cy, descr):
    pid = next_docpr[0]
    next_docpr[0] += 1
    return ('<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{pid}" name="Picture {pid}" descr="{esc(descr)}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
            f'<pic:nvPicPr><pic:cNvPr id="0" name="{pid}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"/></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline>'
            '</w:drawing></w:r></w:p>')

# ---------------------------------------------------------------- TOC
toc = json.load(open(TOCJSON)) if TOCJSON != '-' else {}
TOC_TITLES = [
    '1. Control del documento', '2. Resumen ejecutivo', '3. Contexto y problema',
    '4. Objetivos del sistema', '5. Alcance incluido', '6. Alcance excluido',
    '7. Límites del sistema', '8. Línea base funcional', '9. Línea base no funcional',
    '10. Restricciones', '11. Supuestos, dependencias y riesgos',
    '12. Criterios de aceptación del alcance', '13. Trazabilidad del alcance',
    '14. Control de cambios y conclusión', 'Anexos A a F. Evidencia visual de referencia',
]

def toc_line(title, template):
    page = str(toc.get(title, '0'))
    x = template
    ts = re.findall(r'<w:t(?:\s[^>]*)?>[^<]*</w:t>', x)
    assert len(ts) == 2
    x = x.replace(ts[0], t(title), 1)
    x = x.replace(ts[1], t(page), 1)
    return x

# ================================================================ CONTENT
R = {}   # index -> replacement xml (str) ; '' removes the block
A = {}   # index -> xml appended after the block

TEAM = 'Coronacion Meza Fredy; Peña Arroyo Anthony; Vila Meza Luis Antonio'
FREEZE = '9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2'
THRESHOLD = '0.1679418172266036'

# --- cover
expect(16, '30180'); R[16] = set_text(items[16][1], '28607')
expect(12, 'Caso de estudio'); A[12] = set_text(items[12][1], 'Versión 1.1 · septiembre de 2026')
R[25] = ''   # one empty spacer less, to keep the cover on one page

# --- TOC (static lines, same format as the original)
for k in range(29, 44):
    R[k] = toc_line(TOC_TITLES[k - 29], items[k][1])

# --- 1. Control del documento
expect(46, 'FechaVersión')
R[46] = table(['Fecha', 'Versión', 'Autor', 'Descripción'], [
    ['20/09/2026', '1.0', TEAM, 'Definición consolidada del alcance del proyecto software F9, coherente con la '
     'línea base implementada y la documentación vigente.'],
    ['24/09/2026', '1.1', TEAM, 'Actualización del Formato 09 al estado consolidado v1.1, incorporando trazabilidad '
     'UML/PowerDesigner y diferenciando la línea base académica de las capacidades experimentales. '
     'Corrige el NRC a 28607.'],
], [1296, 1008, 3600, 3312], ['center', 'center', 'left', 'left'])

expect(49, 'CampoDetalle')
R[49] = table(['Campo', 'Detalle'], [
    ['Nombre del proyecto', 'Análisis y Diseño de una Plataforma SaaS Multiempresa para la gestión del '
     'reclutamiento, evaluación y selección de personal'],
    ['Organización / caso de estudio', 'Colegio Andino de Huancayo'],
    ['Módulo / Sistema', 'Plataforma SaaS de Reclutamiento, Evaluación y Selección de Personal: sistema completo, '
     'organizado en ocho bloques funcionales (sección 5)'],
    ['Integrantes del equipo', TEAM],
    ['Asignatura', 'Pruebas y Calidad de Software'],
    ['NRC', '28607'],
    ['Docente', 'Dr. Maglioni Arana Caparachin'],
    ['Entregable', 'Formato 09 - Alcance del proyecto software'],
    ['Versión del documento', '1.1'],
    ['Fecha', '24 de septiembre de 2026'],
    ['Sistema de referencia', 'Línea base académica v1.0 (RF-01 a RF-27) y evolución técnica v1.1 '
     '(Fases 13 a 23), diferenciadas en todo el documento'],
], [2736, 6480], ['left', 'left'])

expect(54, '')
A[54] = ''.join([
    h2('1.4 Correspondencia con el Formato 09 oficial'),
    body_p('La plantilla oficial del Formato 09 exige siete apartados. La tabla indica dónde se desarrolla cada '
           'campo en este documento, que conserva además secciones complementarias de control, trazabilidad y riesgos.'),
    table(['Campo del Formato 09', 'Sección de este documento'], [
        ['1. Datos generales del proyecto', '1.2 Información del proyecto'],
        ['2. Contexto: problema que se busca resolver', '3.1 Contexto organizacional y 3.2 Problemas oficiales'],
        ['2. Contexto: objetivo general del sistema', '4.1 Objetivo general'],
        ['2. Contexto: usuarios principales', '3.4 Usuarios principales'],
        ['2. Contexto: entorno de uso (organización / tecnológico)', '3.5 Entorno de uso'],
        ['3. Objetivos del sistema: general y específicos', '4.1 Objetivo general y 4.2 Objetivos específicos'],
        ['4. Funcionalidades incluidas (IN SCOPE)', '5. Alcance incluido (IN-01 a IN-08)'],
        ['4. Funcionalidades excluidas (OUT OF SCOPE)', '6. Alcance excluido (OUT-01 a OUT-11)'],
        ['5. Límites: actores externos', '7.1 Actores externos (ACT-01 a ACT-05)'],
        ['5. Límites: entradas al sistema', '7.4 Entradas del sistema (E-01 a E-09)'],
        ['5. Límites: salidas del sistema', '7.5 Salidas del sistema (S-01 a S-09)'],
        ['6. Restricciones: tecnológicas, operativas y legales', '10.1, 10.2 y 10.3'],
        ['6. Supuestos', '11.1 Supuestos principales'],
        ['7. Criterios de aceptación del alcance', '12. Criterios de aceptación y 12.1 Correspondencia con el Formato 09'],
    ], [4320, 4896], ['left', 'left']),
    SPACER,
    h2('1.5 Convenciones de estado'),
    body_p('Para no confundir lo verificado con lo propuesto, el documento usa las siguientes categorías:'),
    table(['Categoría', 'Significado en este documento'], [
        ['Verificado', 'Comprobado en el repositorio del proyecto o en una ejecución de pruebas registrada, '
         'indicando la fase en que se verificó.'],
        ['AS-IS académico preliminar', 'Reconstrucción del proceso actual del colegio hecha por el equipo; '
         'pendiente de validación institucional por Recursos Humanos o Administración.'],
        ['TO-BE propuesto', 'Proceso mejorado que propone el equipo; no es un procedimiento aprobado por la institución.'],
        ['Implementado en el prototipo', 'Presente en el código y cubierto por pruebas; demuestra viabilidad '
         'técnica, no preparación para producción.'],
        ['Experimental o candidato (v1.1)', 'Evolución técnica posterior a la v1.0 que no forma parte de la línea '
         'base oficial: RF-28, RF-29 y RNF-C.'],
    ], [2736, 6480], ['left', 'left']),
    SPACER,
])

# --- 2. Resumen ejecutivo
expect(57, 'La línea base vigente')
R[57] = set_text(items[57][1],
    'La línea base oficial contiene 27 requerimientos funcionales, 10 requerimientos no funcionales, 20 casos de uso '
    'y cinco actores externos. Los 27 RF se implementaron y trazaron en el repositorio (v1.0 académica, verificada en '
    'el QA final de la Fase 12). Esta evidencia demuestra viabilidad técnica del prototipo académico, pero no '
    'convierte el modelado AS-IS en un procedimiento institucional validado ni acredita preparación para producción.')
expect(59, 'El servicio Python')
R[59] = set_text(items[59][1],
    'Después de la v1.0, la versión 1.1 (Fases 13 a 23) incorporó una evolución técnica: un servicio experimental de '
    'machine learning en Python y FastAPI, integrado con Laravel mediante HTTP interno autenticado, que estima el '
    'riesgo de demora del proceso de una convocatoria (RF-29, candidato); el rediseño de la interfaz, animaciones con '
    'soporte de movimiento reducido, una escena decorativa en CSS 3D en la portada, QA visual y de accesibilidad, y el '
    'UML AS-IS actualizado con su formalización en PowerDesigner. Esta evolución no amplía la línea base oficial: '
    'RF-28, RF-29 y RNF-C siguen siendo candidatos, el riesgo operacional no evalúa personas ni es productivo, y la '
    'decisión final sigue siendo humana.')
expect(64, '• Cualquier ampliación')
A[64] = bullet('La evolución técnica v1.1 se documenta aparte (secciones 5.9 y 5.10) y no modifica la línea base oficial.')

# --- 3. Contexto: usuarios y entorno (campos oficiales)
expect(72, 'El proceso TO-BE')
A[72] = ''.join([
    h2('3.4 Usuarios principales'),
    body_p('Los usuarios del sistema son los cinco actores externos de la línea base (sección 7.1). El Área '
           'solicitante, Recursos Humanos, el Aprobador o Dirección y el Evaluador pertenecen a una organización '
           'cliente y solo operan dentro de ella. El Postulante tiene una cuenta global y solo ve sus propias '
           'postulaciones. No existen usuarios de administración comercial de la plataforma, y ningún componente de '
           'inteligencia artificial actúa como usuario ni como decisor.'),
    h2('3.5 Entorno de uso'),
    table(['Dimensión', 'Descripción'], [
        ['Organizacional', 'Colegio Andino de Huancayo como organización cliente del caso de estudio. La plataforma '
         'admite varias organizaciones con datos aislados lógicamente. El uso se limita al ámbito académico: '
         'desarrollo, demostración y pruebas con datos ficticios.'],
        ['Tecnológico', 'Aplicación web para navegadores modernos de escritorio y móviles. Monolito modular Laravel 13 '
         '(PHP 8.4) con React 19, TypeScript, Inertia y Tailwind/shadcn; PostgreSQL 17 y Redis 7, ejecutados con '
         'Docker Compose. En v1.1 se suma un servicio Python/FastAPI experimental y opcional, fuera de Docker Compose.'],
    ], [2736, 6480], ['left', 'left']),
    SPACER,
])

# --- 5. Alcance incluido
expect(89, 'El alcance incluido')
R[89] = set_text(items[89][1],
    'El alcance incluido se organiza en ocho bloques derivados de los 27 RF y 20 CU. Las columnas RF y CU expresan la '
    'relación con los requerimientos que pide el Formato 09. Los diez RNF se aplican transversalmente a estos bloques.')
expect(90, 'IDBloque')
x = items[90][1]
x = x.replace('<w:t>Bloque</w:t>', '<w:t>Funcionalidad</w:t>', 1).replace('<w:t>Resultado incluido</w:t>', '<w:t>Descripción</w:t>', 1)
assert 'Funcionalidad' in x and 'Descripción' in x
R[90] = x

expect(115, 'La documentación del repositorio')
R[115] = set_text(items[115][1],
    'La v1.0 académica (tag v1.0.0-academic) implementa y traza RF-01 a RF-27 a backend, frontend y pruebas '
    'automatizadas. El QA final de la Fase 12 registró 27 de 27 RF verificados, PHPUnit con 244 pruebas (236 '
    'aprobadas, 8 omitidas, 0 fallidas) y Cypress con 43 de 43 pruebas aprobadas. Esta condición respalda la '
    'viabilidad del alcance funcional, sin ampliar la línea base ni declarar infraestructura productiva definitiva.')
A[115] = ''.join([
    h2('5.9 Evolución técnica v1.1 (fuera de la línea base oficial)'),
    body_p('Tras la v1.0, el equipo desarrolló la versión 1.1 en la rama develop, en las Fases 13 a 23. Se documenta '
           'para que el alcance refleje el estado real del prototipo, pero no amplía la línea base oficial: ningún RF '
           'nuevo fue aprobado y la rama main conserva la v1.0 académica.'),
    table(['Fase', 'Contenido', 'Efecto sobre el alcance oficial'], [
        ['F13–F14.5', 'Gobierno de v1.1, definición del experimento de ML y flujo de trabajo multiagente',
         'Ninguno: los candidatos RF-28 en adelante no se aprueban (decisión 11 del equipo).'],
        ['F15', 'Servicio ML experimental: datos sintéticos, entrenamiento y API FastAPI',
         'RF-29 candidato; fuera de la línea base.'],
        ['F16', 'Integración Laravel ↔ FastAPI por HTTP interno autenticado; plazo objetivo de cierre de la vacante',
         'Experimental, opcional y desactivada por defecto; no cambia RF-01 a RF-27.'],
        ['F17', 'Validación del ML y regresión integral',
         'Evidencia técnica con datos sintéticos; sin validación institucional.'],
        ['F18', 'Rediseño del frontend', 'Solo interfaz; sin cambios de reglas ni de RF.'],
        ['F19', 'Animaciones con soporte de movimiento reducido', 'Solo interfaz.'],
        ['F20', 'Escena decorativa en CSS 3D en la portada pública',
         'Implementación puntual; RNF-C sigue siendo una propuesta.'],
        ['F21', 'QA visual, accesibilidad y diseño adaptable', 'Corrige defectos de interfaz; sin funciones nuevas.'],
        ['F22', 'Especificación UML del AS-IS del sistema implementado',
         'Documental; representa RF-01 a RF-27 y marca RF-28 y RF-29.'],
        ['F23', 'Formalización en PowerDesigner: modelos OOM y PDM y 22 diagramas exportados',
         'Documental; fuente de los anexos B a F.'],
    ], [1296, 4320, 3600], ['center', 'left', 'left']),
    SPACER,
    body_p([('Resultados de pruebas por fase. ', 'b'),
            'La última regresión funcional completa registrada es la de la Fase 21: Laravel con 408 pruebas '
            'aprobadas y 8 omitidas, Python con 532 aprobadas, 42 pruebas de componente aprobadas y Cypress con 20 '
            'especificaciones y 84 pruebas aprobadas. Las Fases 22 y 23 fueron documentales y de modelado, por lo '
            'que no requirieron reejecución. Estos resultados no se volvieron a ejecutar para este documento; la '
            'Fase 25 realizará el QA global final.']),
    h2('5.10 Candidatos de v1.1 no incorporados a la línea base'),
    table(['ID', 'Descripción', 'Estado real', 'Tratamiento en este Formato 09'], [
        ['RF-28 (candidato)', 'Panel operativo descriptivo de seguimiento de convocatorias: etapas, tiempos y cuellos '
         'de botella, sin datos de personas', 'Propuesta; no implementado',
         'Trabajo futuro (6.2); no forma parte del alcance incluido.'],
        ['RF-29 (candidato)', 'Estimación informativa del riesgo de demora del proceso de una convocatoria',
         'Implementado e integrado de forma experimental (F15 a F17); validado solo con datos sintéticos; no productivo',
         'Evolución técnica experimental (5.9 y 6.1); su uso productivo o decisorio queda excluido (OUT-11).'],
        ['RNF-C (propuesta)', 'Experiencia 3D progresiva en pantallas públicas',
         'Escena puntual en la portada (F20), decorativa y con respaldo estático',
         'Propuesta; no es un RNF aprobado.'],
    ], [1296, 3168, 2448, 2304], ['center', 'left', 'left', 'left']),
    SPACER,
    body_p('Otros candidatos de v1.1 (RF-30, RF-31, RNF-A, RNF-B y RNF-D) tampoco forman parte de la línea base. La '
           'promoción de cualquiera de ellos, incluidos RF-28, RF-29 y RNF-C, es una decisión pendiente del equipo.'),
])

# --- 6. Alcance excluido
expect(118, 'IDElemento excluido')
R[118] = table(['ID', 'Funcionalidad excluida', 'Justificación'], [
    ['OUT-01', 'Facturación SaaS', 'No pertenece al proceso cubierto por RF-01 a RF-27.'],
    ['OUT-02', 'Planes y suscripciones', 'No existe requerimiento comercial aprobado.'],
    ['OUT-03', 'Superadministración comercial SaaS', 'No existen actores ni CU aprobados para gestión comercial global.'],
    ['OUT-04', 'Selección automática por IA o ML', 'Contradice la decisión humana obligatoria de RF-23.'],
    ['OUT-05', 'Inferencia de personalidad o idoneidad', 'No está autorizada y no existe base de datos real o legal para ello.'],
    ['OUT-06', 'Banco de talentos', 'No forma parte de los 27 RF vigentes.'],
    ['OUT-07', 'Dashboards e indicadores avanzados', 'Requieren nuevos RF y definición de métricas. El panel '
     'descriptivo RF-28 es solo un candidato de v1.1 y no está implementado.'],
    ['OUT-08', 'Proveedores externos definitivos', 'Correo, SMS u otros canales no tienen proveedor contratado o aprobado.'],
    ['OUT-09', 'Infraestructura productiva y nube', 'Docker cubre desarrollo, demostración y pruebas locales.'],
    ['OUT-10', 'Integraciones externas no especificadas', 'No hay contratos con ERP, firma, identidad o bolsas de empleo.'],
    ['OUT-11', 'Uso productivo o decisorio del riesgo operacional ML (RF-29)', 'Es una integración experimental '
     'validada solo con datos sintéticos, sin validación institucional ni autorización de producción. No evalúa '
     'personas ni interviene en el ranking, la comparación o la decisión.'],
], [936, 3096, 5184], ['center', 'left', 'left'])

expect(121, 'El servicio experimental solo')
R[121] = ''.join([
    body_p('Estado vigente en v1.1: Laravel consume el servicio FastAPI mediante HTTP interno autenticado cuando la '
           'integración está habilitada por configuración; por defecto está desactivada y, sin el servicio, la '
           'aplicación funciona igual. La estimación se muestra a Recursos Humanos y al Aprobador de la misma '
           'organización como una tarjeta rotulada «Experimental». No se guarda en la base de datos y no llega al '
           'ranking, a la comparación ni a la decisión final.'),
    table(['Elemento', 'Contenido'], [
        ['Frontera', 'Laravel → HTTP interno autenticado (token interno) → FastAPI'],
        ['Petición', 'Exactamente 15 variables operacionales del proceso; sin identificadores, datos personales, '
         'atributos sensibles ni texto libre'],
        ['Respuesta', ['risk_score, risk_flag, threshold, model_version, freeze_fingerprint y status. No existe un '
                       'campo independiente de incertidumbre']],
        ['Modelo', 'Logistic Regression, C = 10, class_weight = None, StandardScaler, sin calibración'],
        ['Contrato congelado', [('Freeze: ', 'b'), (FREEZE, 'c'), ('  ·  Threshold: ', 'b'), (THRESHOLD, 'c')]],
        ['Estado', 'Experimental, opcional, no productivo y no persistido; RF-29 sigue siendo candidato'],
    ], [2304, 6912], ['left', 'left']),
    SPACER,
    body_p('El servicio estima el riesgo de demora del proceso de una convocatoria, no de las personas: no recibe ni '
           'produce puntuaciones de candidatos, no accede a la base de datos principal, no escribe estados y no '
           'modifica el ranking. El detalle científico y de validación está en la documentación técnica de v1.1 '
           '(Fases 14 a 17).'),
])
for k, s in zip(range(123, 128), [
        'Panel operativo descriptivo del proceso (RF-28, candidato) y reportes exportables (RF-30, candidato).',
        'Indicadores medibles con definiciones institucionales aprobadas.',
        'Validación institucional del riesgo operacional (RF-29) y decisión formal sobre su promoción; nunca aplicado a personas.',
        'Accesibilidad verificada con lector de pantalla real, presupuestos de rendimiento medidos y observabilidad '
        'formal (RNF-A, RNF-B y RNF-D, candidatos).',
        'Despliegue productivo, continuidad operativa y acuerdos con proveedores externos.']):
    assert txt(items[k][1]).startswith('• ')
    R[k] = set_text(items[k][1], '• ' + s)

# --- 7. Límites del sistema
expect(131, '')
A[131] = body_p('El servicio de riesgo operacional aparece en el UML técnico v1.1 como actor secundario '
                '«external service, experimental» (Anexo B). No es un usuario del negocio ni toma decisiones; por eso '
                'no figura entre los actores externos del alcance.')
expect(133, 'Los controladores')
R[133] = ''.join([
    set_text(items[133][1],
        'Los controladores, servicios, políticas, colas, base de datos, auditoría, notificaciones y validadores son '
        'componentes internos y no actores. Laravel constituye el sistema de registro; PostgreSQL conserva los datos '
        'de negocio y Redis soporta sesiones, caché y procesamiento asíncrono. La arquitectura es un monolito modular '
        'y la multitenencia es lógica: organization_id, un scope global y Policies que comparan rol y organización. '
        'No se usa Row Level Security de PostgreSQL ni microservicios generales.'),
    body_p([('Frontera técnica experimental (v1.1). ', 'b'),
            'El servicio FastAPI es un proceso externo al monolito y a Docker Compose. Recibe de Laravel 15 variables '
            'operacionales y devuelve una estimación de riesgo del proceso; no accede a la base de datos principal ni '
            'escribe estados. Si está deshabilitado o no responde, la tarjeta muestra un estado descriptivo o no '
            'disponible y el resto del sistema no cambia.']),
])
expect(140, 'IDSalida')
R[140] = table(['ID', 'Salida', 'Destino'], [
    ['S-01', 'Estado y notificación del requerimiento', 'Área solicitante (notificación de rechazo); RR. HH. y Aprobador (estado)'],
    ['S-02', 'Vacante publicada', 'Postulantes y público (portal de empleos)'],
    ['S-03', 'Confirmación y estado de postulación', 'Postulante'],
    ['S-04', 'Historial de etapas y notificaciones', 'Recursos Humanos (historial); Postulante (notificación)'],
    ['S-05', 'Convocatorias de evaluación y entrevista', 'Postulante convocado y Evaluador asignado'],
    ['S-06', 'Resultados registrados', 'Recursos Humanos y Aprobador o Dirección'],
    ['S-07', 'Ranking y comparación explicable', 'Recursos Humanos y Aprobador o Dirección'],
    ['S-08', 'Decisión, selección, cierre y resultado individual', 'Aprobador o Dirección y RR. HH. (registro); '
     'Postulante (resultado individual)'],
    ['S-09', 'Registro de auditoría', 'Aprobador o Dirección (consulta)'],
], [1008, 4320, 3888], ['center', 'left', 'left'])

# --- 8. Línea base funcional
expect(143, 'Los 27 requerimientos')
R[143] = set_text(items[143][1],
    'Los 27 requerimientos funcionales forman la línea base oficial y conservan su número, nombre y significado. No '
    'se agregan RF experimentales o comerciales: RF-28 y RF-29 son candidatos de v1.1 (sección 5.10) y no forman '
    'parte de esta tabla.')

# --- 9. RNF
expect(150, 'Los RNF son transversales')
R[150] = set_text(items[150][1], txt(items[150][1]).rstrip() +
    ' Los RNF candidatos de v1.1 (RNF-A a RNF-D) no modifican esta línea base; en particular, RNF-C (experiencia 3D '
    'progresiva) sigue siendo una propuesta aunque la Fase 20 implementó una escena puntual en la portada.')

# --- 10. Restricciones
expect(153, '• Monolito modular')
R[153] = set_text(items[153][1], '• Monolito modular con Laravel 13 y PHP 8.4; frontend React 19, TypeScript, '
                  'Inertia 3, Tailwind 4 y componentes shadcn/ui.')
expect(156, '• La imagen actual')
A[156] = bullet('Multitenencia lógica con organization_id, scope global y Policies; sin Row Level Security de '
                'PostgreSQL ni microservicios generales.') + \
         bullet('El servicio FastAPI (Python y scikit-learn) es experimental, opcional y externo a Docker Compose; '
                'solo se habilita por configuración.')
expect(162, '• Una vacante cerrada')
A[162] = bullet('El riesgo operacional (RF-29) es informativo: no cambia estados, no modifica el ranking y no '
                'participa en la decisión final.')
expect(167, '• El prototipo no acredita')
A[167] = bullet('El servicio de riesgo operacional recibe solo 15 variables operacionales del proceso, sin '
                'identificadores, datos personales, atributos sensibles ni texto libre, y se entrenó con datos sintéticos.')

# --- 11. Supuestos, dependencias y riesgos
expect(174, '• La decisión final')
A[174] = bullet('RF-28, RF-29 y RNF-C permanecen como candidatos hasta una decisión explícita del equipo; '
                'implementar una capacidad no la promueve a la línea base.') + \
         bullet('El catálogo CU-01 a CU-20 procede del análisis académico del equipo; el repositorio conserva otras '
                'vistas de los mismos RF (sección 13.2).')
expect(176, 'DependenciaEfecto')
R[176] = table(['Dependencia', 'Efecto en el alcance'], [
    ['Validación de RR. HH. o Administración', 'Confirma o corrige el AS-IS, roles y prioridades institucionales.'],
    ['Entorno Docker', 'Permite reproducir la aplicación y las pruebas localmente.'],
    ['Servicios PostgreSQL y Redis', 'Soportan persistencia, integridad, sesiones, caché y colas.'],
    ['Proveedores de comunicación', 'Se simulan o se usan canales de desarrollo hasta seleccionar un proveedor.'],
    ['Gobierno de ML', 'Mantiene el riesgo operacional como experimental y desactivado por defecto; su uso productivo '
     'exige validación institucional y la promoción formal de RF-29.'],
    ['Modelos UML v1.1 (PowerDesigner)', 'Los anexos usan las exportaciones versionadas de la Fase 23; editar los '
     'modelos requiere PowerDesigner y autorización del equipo.'],
], [3168, 6048], ['left', 'left'])
expect(179, 'RiesgoImpacto')
R[179] = table(['Riesgo', 'Impacto', 'Mitigación'], [
    ['Cambios en RF o CU', 'Alto', 'Control formal de cambios y actualización de trazabilidad.'],
    ['Confundir prototipo con producción', 'Alto', 'Mantener exclusiones y criterios de preparación productiva separados.'],
    ['Usar ML para evaluar personas', 'Crítico', 'Aplicar ADR-001 y ADR-002; contrato de 15 variables operacionales '
     'sin identificadores ni PII; prohibición explícita y pruebas.'],
    ['Pérdida de aislamiento multiempresa', 'Alto', 'Políticas, contexto organizacional y pruebas de acceso cruzado.'],
    ['Confundir la evolución v1.1 con una ampliación del alcance', 'Alto', 'Separar línea base, evolución técnica y '
     'candidatos (secciones 5.9 y 5.10); promover solo por decisión explícita del equipo.'],
], [3456, 1152, 4608], ['left', 'center', 'left'])

# --- 12. Criterios de aceptación
expect(182, 'IDCriterio')
R[182] = table(['ID', 'Criterio', 'Condición verificable'], [
    ['CA-01', 'Línea base funcional', 'Los 27 RF están vinculados con bloques IN y casos de uso.'],
    ['CA-02', 'Línea base no funcional', 'Los 10 RNF se aplican transversalmente y tienen condición verificable.'],
    ['CA-03', 'Casos de uso', 'Los 20 CU representan la línea base sin funciones huérfanas.'],
    ['CA-04', 'Actores', 'Los cinco actores externos tienen responsabilidad, entradas y salidas definidas.'],
    ['CA-05', 'Problema', 'Los cinco problemas oficiales se presentan como diagnóstico académico preliminar.'],
    ['CA-06', 'Claridad IN/OUT', 'Ocho bloques incluidos y once exclusiones están identificados y justificados.'],
    ['CA-07', 'Decisión humana', 'El ranking es apoyo y no cambia por sí solo el estado de una postulación; la '
     'decisión final corresponde al Aprobador o Dirección (RF-23).'],
    ['CA-08', 'ML experimental', 'El riesgo operacional (RF-29) queda fuera de la línea base, es experimental y no '
     'productivo, no evalúa personas y no interviene en el ranking ni en la decisión.'],
    ['CA-09', 'Multitenencia', 'Lecturas y escrituras empresariales respetan el contexto de organización.'],
    ['CA-10', 'Viabilidad', 'La implementación existente respalda el alcance sin afirmar producción.'],
    ['CA-11', 'Consistencia documental', 'El entregable utiliza el NRC 28607 y terminología coherente con el Informe '
     'Final y la documentación de v1.1.'],
    ['CA-12', 'Cambio controlado', 'Toda ampliación exige RF/RNF, trazabilidad, aprobación y pruebas actualizadas.'],
    ['CA-13', 'Evolución v1.1', 'Las capacidades de las Fases 13 a 23 se identifican como evolución técnica; RF-28, '
     'RF-29 y RNF-C figuran como candidatos no promovidos.'],
    ['CA-14', 'Evidencia de modelado', 'Los anexos UML proceden de las exportaciones de PowerDesigner de la Fase 23 y '
     'se identifican como UML AS-IS v1.1.'],
], [1008, 2592, 5616], ['center', 'left', 'left'])
expect(183, '')
A[183] = ''.join([
    h2('12.1 Correspondencia con los criterios del Formato 09'),
    table(['Criterio del Formato 09', 'Criterios', 'Cómo se cumple'], [
        ['Coherencia con los requerimientos y casos de uso', 'CA-01 a CA-04',
         'Cada bloque IN se vincula con RF y CU; los 27 RF y los 20 CU quedan cubiertos sin funciones huérfanas '
         '(secciones 5, 8 y 13).'],
        ['Claridad en IN/OUT of scope', 'CA-06, CA-08, CA-13',
         'Ocho bloques incluidos y once exclusiones justificadas; los candidatos de v1.1 se separan de la línea base.'],
        ['Viabilidad del proyecto', 'CA-09, CA-10',
         'La v1.0 implementada y probada respalda el alcance, sin afirmar preparación para producción.'],
        ['Ausencia de ambigüedades', 'CA-05, CA-07, CA-11, CA-12, CA-14',
         'Categorías de estado explícitas (1.5), decisión humana inequívoca, NRC y terminología únicos, y control '
         'formal de cambios.'],
    ], [2880, 1728, 4608], ['left', 'center', 'left']),
    SPACER,
])

# --- 13. Trazabilidad: UML AS-IS v1.1
expect(189, '')
A[189] = ''.join([
    h2('13.2 Correspondencia con el UML AS-IS v1.1'),
    body_p('Los diagramas de PowerDesigner de la Fase 23 usan un caso de uso por RF, incluidos RF-28 como '
           '«propuesto v1.1» y RF-29 como «experimental». El Informe Final del repositorio agrupa los mismos RF en 13 '
           'casos de uso (CU-01 a CU-13) y este Formato conserva el catálogo académico CU-01 a CU-20. Las tres vistas '
           'cubren RF-01 a RF-27; la conciliación de la numeración de los CU queda registrada como observación para el '
           'equipo.'),
    table(['RF', 'Diagramas de PowerDesigner (Fase 23)'], [
        ['RF-01 a RF-04', 'UC-01, PK-01, CO-01, CL-01, PDM, SEQ-02, AC-01, ST-01'],
        ['RF-05 a RF-07', 'UC-01, PK-01, CO-01, CL-01, PDM, AC-01, ST-02'],
        ['RF-08 a RF-11', 'UC-01, PK-01, CL-01, PDM, SEQ-01, AC-01, ST-03 (RF-10)'],
        ['RF-12 a RF-15', 'UC-01, PK-01, CL-01, PDM, SEQ-03, AC-01, ST-03'],
        ['RF-16 a RF-20', 'UC-01, PK-01, CL-01, PDM, SEQ-04, SEQ-05, SEQ-06 (RF-20), AC-01, ST-03, ST-04'],
        ['RF-21 y RF-22', 'UC-01, PK-01, CO-01, SEQ-06, AC-01'],
        ['RF-23', 'UC-01 «human decision», CL-01 (SelectionDecision), SEQ-07 «human decision», AC-01; ningún mensaje al ML'],
        ['RF-24 a RF-26', 'UC-01, PK-01, CL-01, PDM (índice parcial), AC-01, ST-02, ST-03'],
        ['RF-27', 'UC-01, PK-01, CO-01, CL-01 (AuditLog), PDM (trigger de solo inserción), AuditLogger en las secuencias'],
        ['RF-28 (candidato)', 'Solo UC-01, «propuesto v1.1», sin asociaciones'],
        ['RF-29 (candidato)', 'UC-01, PK-01, CO-01, DE-01, CL-01/PDM (target_completion_at), SEQ-08 y AC-02, siempre «experimental»'],
    ], [2304, 6912], ['center', 'left']),
    SPACER,
])

# --- 14. Conclusión y referencias
expect(199, 'El ranking y la comparación')
R[199] = set_text(items[199][1],
    'El ranking y la comparación permanecen como apoyo explicable. La decisión final es humana, autorizada y auditable '
    '(RF-23). La versión 1.1 integró de forma experimental un servicio de riesgo operacional del proceso (RF-29, '
    'candidato) mediante HTTP interno autenticado; no evalúa personas, no se persiste, no interviene en el ranking ni '
    'en la decisión y no está autorizado para producción. Esa evolución, junto con el rediseño de la interfaz, el UML '
    'AS-IS actualizado y su formalización en PowerDesigner, se reconoce como trabajo técnico que no amplía la línea '
    'base oficial.')
for k, s in zip(range(201, 206), [
        'Informe Final SaaS Reclutamiento Colegio Andino hasta el Capítulo 5 (documento histórico del equipo, '
        'referenciado en la versión 1.0 de este Formato con el NRC anterior).',
        'Informe final del repositorio (14 capítulos), matriz de implementación de RF y matriz maestra de trazabilidad.',
        'Supuestos y decisiones documentadas A-01 a A-36.',
        'ADR-001 Frontera del machine learning, ADR-002 Supervisión humana de la decisión y ADR-003 Experiencia 3D '
        'progresiva y acotada.',
        'Documentación de v1.1: alcance preliminar y candidatos, Fases 15 a 17 (servicio ML, integración y '
        'validación), Fase 22 (UML AS-IS) y Fase 23 (PowerDesigner).']):
    assert txt(items[k][1]).startswith('• ')
    R[k] = set_text(items[k][1], '• ' + s)

# --- Anexos
expect(206, 'Anexo A'); expect(209, 'Anexo B'); expect(212, 'Anexo C')
R[208] = caption('Proceso TO-BE propuesto por el equipo (BPMN). Es una propuesta académica, no un procedimiento '
                 'validado por la institución. La rama «cerrar sin selección» no está implementada en el prototipo: '
                 'RF-25 cubre solo el cierre con selección.')
EXP = EXPORTS
def annex(title, png, name, descr, cap, rotate=False):
    rid, cx, cy, _ = add_image(os.path.join(EXP, png), name, rotate)
    return h1(title) + image_p(rid, cx, cy, descr) + caption(cap)

R[209] = ''
R[210] = ''
R[211] = annex('Anexo B. Casos de uso — UML AS-IS v1.1 (UC-01)', 'UC-01-casos-de-uso.png',
    'f24-uc-01.png', 'Diagrama de casos de uso UC-01, UML AS-IS v1.1',
    'UC-01 exportado de PowerDesigner (Fase 23), girado 90° para ganar tamaño. Representa el sistema implementado: '
    'cinco actores de negocio y el servicio de riesgo operacional como actor técnico secundario «external service, '
    'experimental»; un caso por RF, con RF-23 «human decision», RF-28 «propuesto v1.1» sin asociaciones y RF-29 '
    '«experimental». Sustituye la vista de casos de uso usada como antecedente visual en la versión 1.0, que incluía '
    'actores y funciones fuera del alcance.', rotate=True)
R[212] = ''
R[213] = ''
R[214] = ''.join([
    annex('Anexo C. Componentes — UML AS-IS v1.1 (CO-01)', 'CO-01-componentes.png', 'f24-co-01.png',
          'Diagrama de componentes CO-01, UML AS-IS v1.1',
          'CO-01 (Fase 23). Monolito modular Laravel con frontend React/Inertia, PostgreSQL 17, Redis 7 y auditoría; '
          'el servicio FastAPI figura como componente externo «experimental». Sustituye la arquitectura conceptual de '
          'la versión 1.0, que mostraba servicios fuera del alcance, como suscripciones y planes o superadministración.'),
    annex('Anexo D. Despliegue — UML AS-IS v1.1 (DE-01)', 'DE-01-despliegue.png', 'f24-de-01.png',
          'Diagrama de despliegue DE-01, UML AS-IS v1.1',
          'DE-01 (Fase 23), girado 90°. Contenedores app, queue, postgres y redis en Docker Compose; el proceso Python '
          'del servicio experimental corre en el equipo anfitrión, fuera de Compose, y solo se usa con '
          'ML_SERVICE_ENABLED=true. Es un entorno de desarrollo, demostración y pruebas, no una infraestructura productiva.',
          rotate=True),
    annex('Anexo E. Actividad del proceso de reclutamiento — UML AS-IS v1.1 (AC-01)', 'AC-01-proceso-reclutamiento.png',
          'f24-ac-01.png', 'Diagrama de actividad AC-01, UML AS-IS v1.1',
          'AC-01 (Fase 23). Describe, por carriles de actor, el comportamiento verificado del sistema implementado. '
          'Complementa el TO-BE del Anexo A; no constituye una validación institucional del AS-IS del colegio.'),
    annex('Anexo F. Clases del dominio — UML AS-IS v1.1 (CL-01)', 'CL-01-clases-del-dominio.png', 'f24-cl-01.png',
          'Diagrama de clases del dominio CL-01, UML AS-IS v1.1',
          'CL-01 (Fase 23). 17 clases del dominio y 37 asociaciones derivadas de los modelos Eloquent; las '
          'enumeraciones están en la vista auxiliar CL-01b. Los diagramas en SVG y los modelos nativos (.oom y .pdm) '
          'están en docs/v1.1/powerdesigner/ del repositorio.'),
])

# ================================================================ assemble
out = []
for k, (tag, xml) in enumerate(items):
    out.append(R.get(k, xml))
    if k in A:
        out.append(A[k])
new_body = ''.join(out)
open(DOC, 'w', encoding='utf8').write(head + new_body + tail)
open(RELS, 'w', encoding='utf8').write(rels)

core = os.path.join(WORK, 'docProps', 'core.xml')
c = open(core, encoding='utf8').read()
assert '<dc:description>NRC 30180</dc:description>' in c
c = c.replace('<dc:description>NRC 30180</dc:description>',
              '<dc:description>NRC 28607 · Versión 1.1 (Fase 24)</dc:description>')
c = re.sub(r'<dcterms:modified xsi:type="dcterms:W3CDTF">[^<]*</dcterms:modified>',
           '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-09-24T12:00:00Z</dcterms:modified>', c)
c = c.replace('<cp:revision>2</cp:revision>', '<cp:revision>3</cp:revision>')
open(core, 'w', encoding='utf8').write(c)

# well-formedness of every XML part
import xml.dom.minidom
for root, _, files in os.walk(WORK):
    for f in files:
        if f.endswith('.xml') or f.endswith('.rels'):
            xml.dom.minidom.parse(os.path.join(root, f))

# zip: [Content_Types].xml first, same order as the original
with zipfile.ZipFile(ORIG) as z:
    order = z.namelist()
new_files = []
for root, _, files in os.walk(WORK):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), WORK)
        if rel not in order:
            new_files.append(rel)
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in order + sorted(new_files):
        z.write(os.path.join(WORK, n), n)
print('OK', OUT, 'blocks', len(items), 'new media', sorted(new_files))
