"""Formato 11 oficial regularizado (F11-R): rellena la plantilla oficial en su propio paquete.

Se conserva el paquete de la plantilla (cabecera con el logotipo y la asignatura, estilos, numeración, título y tablas).
Se rellenan sus bloques en el mismo orden: la tabla de datos generales, las cajas de una celda de cada viñeta, la tabla de
componentes (CMP-xx), la tabla de relaciones, la caja del diagrama (en una página horizontal) y las viñetas de
decisiones. Se quitan las instrucciones de la plantilla («Describir brevemente:», «Insertar aquí el diagrama del
sistema.», etc.) y las líneas en blanco para completar. La plantilla oficial solo se lee.
"""
import os
import re
from xml.dom import minidom
import zipfile
from xml.sax.saxutils import escape

import m_common as C
import m_f11r as F
from docxgen import (_fill_datos, _runs, box, image_data, image_xml, keep_image_resolution, sect_variant, split_blocks,
                     with_sect, TWIP_CM, EMU_CM)

INSTRUCCIONES = ('Describir brevemente:', 'Seleccionar y justificar el estilo arquitectónico',
                 'Insertar aquí el diagrama del sistema.', 'Registrar decisiones clave tomadas:')
CAJAS_DESCRIPCION = {'Propósito del sistema.': F.PROPOSITO, 'Alcance general.': F.ALCANCE,
                     'Usuarios principales.': F.USUARIOS, 'Relación con requerimientos y casos de uso.': F.RELACION_RF_CU}
CAJAS = {**CAJAS_DESCRIPCION, **F.ESTILO, **F.RESTRICCIONES}


def text_of(xml):
    return ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', xml)).strip()


def cell_paras(lines, sz=18, jc='both', spacing=264):
    """Párrafos de una caja o celda. Cada línea es un párrafo; las líneas «• …» y «– …» llevan sangría francesa."""
    out = []
    for line in lines:
        for sub in line.split('\n'):
            s = sub.strip()
            ind = ''
            if s.startswith('• '):
                ind = '<w:ind w:left="227" w:hanging="227"/>'
            elif s.startswith('– '):
                ind = '<w:ind w:left="454" w:hanging="227"/>'
            out.append(f'<w:p><w:pPr><w:spacing w:after="60" w:line="{spacing}" w:lineRule="auto"/>{ind}<w:jc w:val="{jc}"/>'
                       f'</w:pPr>{_runs(s, sz=sz)}</w:p>')
    return ''.join(out)


def fill_box(tbl, lines):
    """Sustituye el contenido de la única celda de una caja de la plantilla, conservando su tabla y ancho."""
    return re.sub(r'(<w:tc>\s*<w:tcPr>.*?</w:tcPr>).*?(</w:tc>)', lambda m: m.group(1) + cell_paras(lines) + m.group(2),
                  tbl, count=1, flags=re.S)


def fill_grid(tbl, rows, sz=16):
    """Tabla con encabezado: conserva la fila de encabezado de la plantilla (repetida en cada página) y la cuadrícula,
    y reemplaza las filas de ejemplo por las filas de contenido."""
    widths = re.findall(r'<w:gridCol w:w="(\d+)"/>', tbl)
    trs = re.findall(r'<w:tr[ >].*?</w:tr>', tbl, re.S)
    header = re.sub(r'(<w:tr[^>]*>)', r'\1<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>', trs[0], count=1)
    body = []
    for r in rows:
        cells = ''.join(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/></w:tcPr>{cell_paras([str(v)], sz=sz, jc="left", spacing=240)}</w:tc>'
                        for v, w in zip(r, widths))
        body.append(f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{cells}</w:tr>')
    start = tbl.index(trs[0])
    end = tbl.rindex(trs[-1]) + len(trs[-1])
    return tbl[:start] + header + ''.join(body) + tbl[end:]


def bullet(text, sz=18):
    return ('<w:p><w:pPr><w:pStyle w:val="Prrafodelista"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="5"/></w:numPr>'
            f'<w:spacing w:after="80" w:line="264" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>{_runs(text, sz=sz)}</w:p>')


def plain(text, sz=18, jc='both', italic=False, after=120):
    return (f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="264" w:lineRule="auto"/><w:ind w:left="284"/>'
            f'<w:jc w:val="{jc}"/></w:pPr>{_runs(text, sz=sz, italic=italic)}</w:p>')


def build(template, arq_png, out_docx):
    zin = zipfile.ZipFile(template)
    document = zin.read('word/document.xml').decode('utf-8')
    rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
    head, rest = document.split('<w:body>', 1)
    body, tail = rest.rsplit('</w:body>', 1)
    blocks = split_blocks(body)
    sect = blocks[-1][1]
    assert 'w:sectPr' in sect
    media, rid_n, docpr = [], 100, 100

    def add_image(data):
        nonlocal rid_n, docpr, rels
        rid_n += 1
        docpr += 1
        rid, target = f'rId{rid_n}', f'media/f11r_{len(media) + 1}.png'
        media.append((target, data))
        rels = rels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                            f'officeDocument/2006/relationships/image" Target="{target}"/></Relationships>')
        return rid, docpr

    parts, label, first_tbl, decisions_done, seen = [], None, True, False, []
    for kind, xml in blocks[:-1]:
        txt = text_of(xml)
        if kind == 'w:p':
            if txt in INSTRUCCIONES:
                seen.append(txt)
                continue
            if txt and set(txt) == {'_'}:                       # líneas para completar de «Decisiones de diseño»
                if not decisions_done:
                    for d in F.DECISIONES:
                        parts.append(bullet(f'**{d[0]} {d[1]}.** Estado: **{d[2]}**. {d[3]}. Evidencia: {d[4]}.'))
                    parts.append(plain(F.NOTA_DECISIONES, sz=16, italic=True))
                    decisions_done = True
                continue
            if txt == 'Diagrama de Arquitectura conceptual':
                # Cierra la sección vertical anterior: el apartado 6 va en una página horizontal.
                parts.append('<w:p><w:pPr><w:spacing w:after="0"/>' + sect_variant(sect) + '</w:pPr></w:p>')
            if txt:
                label = txt
            if '<w:numPr>' in xml and '<w:keepNext/>' not in xml:
                # Encabezados y viñetas de la plantilla: se mantienen con la caja o tabla que les sigue.
                if '<w:pStyle' in xml:
                    xml = re.sub(r'(<w:pStyle w:val="[^"]+"/>)', lambda m: m.group(1) + '<w:keepNext/>', xml, count=1)
                else:
                    xml = xml.replace('<w:pPr>', '<w:pPr><w:keepNext/>', 1)
            parts.append(xml)
            continue
        # tablas
        if first_tbl:
            datos = C.datos('modulo')
            datos['Fecha'] = F.FECHA
            parts.append(_fill_datos(xml, datos))
            parts.append('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>')
            parts.append(box(['**Estado de la información de este formato**'] + C.LEYENDA + F.NOTA_ESTADO + C.REGLAS_FIJAS,
                             sz=18, fill='FFF2CC'))
            first_tbl = False
        elif 'Funcionalidades asociadas' in txt:
            parts.append(fill_grid(xml, F.componentes()))
            parts += [plain(x, sz=16) for x in F.NOTA_COMPONENTES]
        elif 'Tipo de interacción' in txt:
            parts.append(fill_grid(xml, F.relaciones()))
            parts += [plain(x, sz=16, after=60) for x in F.NOTA_RELACIONES]
        elif label == 'Diagrama de Arquitectura conceptual':
            # Caja del diagrama ensanchada al ancho útil de la página horizontal, con ARQ-01 dentro.
            m = re.search(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"', sect)
            mar = {k: int(v) for k, v in re.findall(r'w:(left|right|top|bottom)="(\d+)"', re.search(r'<w:pgMar[^>]*/>', sect).group(0))}
            width = int(m.group(2)) - mar['left'] - mar['right'] - 284
            data, w, h = image_data(arq_png)
            cx = int((width - 230) / TWIP_CM * EMU_CM)
            cy = int(cx * h / w)
            max_cy = int(13.2 * EMU_CM)
            if cy > max_cy:
                cy, cx = max_cy, int(max_cy * w / h)
            rid, dp = add_image(data)
            img = image_xml(rid, dp, os.path.basename(arq_png), cx, cy).replace('<w:spacing w:after="60"/>', '<w:spacing w:after="0"/>')
            t = re.sub(r'<w:gridCol w:w="\d+"/>', f'<w:gridCol w:w="{width}"/>', xml)
            t = re.sub(r'<w:tcW w:w="\d+" w:type="dxa"/>', f'<w:tcW w:w="{width}" w:type="dxa"/>', t)
            t = re.sub(r'(<w:tc>\s*<w:tcPr>.*?</w:tcPr>).*?(</w:tc>)', lambda mm: mm.group(1) + img + mm.group(2), t, count=1, flags=re.S)
            parts.append(t)
            cap = plain(F.FIGURA_1, sz=16, jc='center', italic=True, after=0)
            parts.append(with_sect(cap, sect_variant(sect, landscape=True)))
            parts.append(plain(F.DIAGRAMA_NOTA, sz=18))
            for crop, caption in (((0.0, 0.55), F.FIGURA_2), ((0.45, 1.0), F.FIGURA_3)):
                data, w, h = image_data(arq_png, crop)
                cx = int(14.8 * EMU_CM)
                cy = int(cx * h / w)
                if cy > int(21.5 * EMU_CM):
                    cy = int(21.5 * EMU_CM)
                    cx = int(cy * w / h)
                rid, dp = add_image(data)
                parts.append(image_xml(rid, dp, os.path.basename(arq_png), cx, cy))
                parts.append(plain(caption, sz=16, jc='center', italic=True, after=200))
        elif label in CAJAS:
            parts.append(fill_box(xml, CAJAS[label]))
        else:
            raise ValueError(f'Tabla de la plantilla sin contenido asignado (etiqueta «{label}»)')
    parts.append(sect)
    missing = [i for i in INSTRUCCIONES if i not in seen]
    assert not missing and decisions_done, (missing, decisions_done)
    new_doc = head + '<w:body>' + ''.join(parts) + '</w:body>' + tail
    minidom.parseString(new_doc.encode('utf-8'))   # falla aquí si el XML generado no está bien formado
    core = zin.read('docProps/core.xml').decode('utf-8')
    core = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', f'<dc:title>{escape(F.TITULO)}</dc:title>', core)
    core = re.sub(r'<dc:creator>.*?</dc:creator>', f'<dc:creator>{escape(C.EQUIPO)}</dc:creator>', core)
    core = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', '<cp:lastModifiedBy>Equipo del proyecto</cp:lastModifiedBy>', core)
    fixed = (2026, 9, 29, 0, 0, 0)
    with zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'word/document.xml':
                data = new_doc.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                data = rels.encode('utf-8')
            elif info.filename == 'docProps/core.xml':
                data = core.encode('utf-8')
            elif info.filename == 'word/settings.xml':
                data = keep_image_resolution(data.decode('utf-8')).encode('utf-8')
            zi = zipfile.ZipInfo(info.filename, date_time=fixed)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
        for target, data in media:
            zi = zipfile.ZipInfo('word/' + target, date_time=fixed)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)


def md_table(headers, rows):
    esc = lambda x: str(x).replace('|', '\\|').replace('\n', '<br>')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)] +
                     ['| ' + ' | '.join(esc(c) for c in r) + ' |' for r in rows])


def build_md(out_md, docx_name, arq_rel):
    L = [f'# {F.TITULO}', '',
         f'> Espejo en Markdown de `{docx_name}`, generado desde el mismo contenido (`docs/academico/tools/f27b/m_f11r.py` '
         'y `f11r.py`) sobre la plantilla oficial `Formato_11_Arquitectura_del_sistema.docx`. El entregable es el DOCX.', '',
         '## 1. Datos generales del proyecto', '', '| Campo | Valor |', '|---|---|']
    datos = C.datos('modulo')
    datos['Fecha'] = F.FECHA
    L += [f'| {k} | {v} |' for k, v in datos.items()] + ['']
    L += ['> **Estado de la información de este formato**', '>'] + [f'> {x}\n>' for x in C.LEYENDA + F.NOTA_ESTADO + C.REGLAS_FIJAS]
    L += ['', '## 2. Descripción general del sistema', '']
    for k, v in CAJAS_DESCRIPCION.items():
        L += [f'**{k}**', ''] + [x for x in v] + ['']
    L += ['## 3. Estilo arquitectónico propuesto', '']
    for k, v in F.ESTILO.items():
        L += [f'**{k}**', ''] + [x for x in v] + ['']
    L += ['## 4. Identificación de componentes', '', md_table(['ID', 'Componente', 'Descripción', 'Funcionalidades asociadas'],
                                                            F.componentes()), ''] + F.NOTA_COMPONENTES + ['']
    L += ['## 5. Relación entre componentes', '', md_table(['Componente origen', 'Componente destino', 'Tipo de interacción',
                                                          'Descripción'], F.relaciones()), ''] + F.NOTA_RELACIONES + ['']
    L += ['## 6. Diagrama de Arquitectura conceptual', '', f'![{F.FIGURA_1}]({arq_rel})', '', f'*{F.FIGURA_1}*', '',
          F.DIAGRAMA_NOTA, '', f'*{F.FIGURA_2}* (en el DOCX)', '', f'*{F.FIGURA_3}* (en el DOCX)', '']
    L += ['## 7. Decisiones de diseño', ''] + [f'- **{d[0]} {d[1]}.** Estado: **{d[2]}**. {d[3]}. Evidencia: {d[4]}.'
                                               for d in F.DECISIONES] + ['', F.NOTA_DECISIONES, '']
    L += ['## 8. Restricciones y consideraciones', '']
    for k, v in F.RESTRICCIONES.items():
        L += [f'**{k}**', ''] + [x.replace('\n', '\n') for x in v] + ['']
    text = '\n'.join(L)
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n'
    with open(out_md, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def sha256_versioned(path):
    """SHA-256 del contenido versionado (LF en los archivos de texto), el mismo criterio que build.py y el manifiesto F29."""
    import hashlib
    with open(path, 'rb') as f:
        data = f.read()
    if path.lower().endswith(('.md', '.svg', '.bpm', '.oom', '.py', '.ps1', '.txt')):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def build_registro(out_md, root, sources):
    """Registro de la regularización: qué cambió y qué no, matriz de correspondencia, equivalencia CMP ↔ C, relaciones
    R-01 a R-20, diferencias con el F11 adaptado y fuentes con su SHA-256. sources: [(ruta relativa a root, qué es)]."""
    import m_arch as AR
    rel = lambda path: os.path.relpath(os.path.join(root, path), os.path.dirname(out_md)).replace(os.sep, '/')
    L = ['# Regularización F11-R — Formato 11 oficial', '',
         '**Estado:** implementada el 29/09/2026 en la rama `feature/f11-r-official-format` (creada desde `develop` `f7017c1`). '
         'Pendiente de auditoría independiente. No se hizo *push* ni *merge*.', '',
         '## Qué es', '',
         'El Formato 11 oficial «Arquitectura del sistema» llegó después de la Fase 28. Hasta entonces no estaba disponible, así '
         'que el F11 se hizo como **adaptación académica** de la Guía 11 sobre la base visual del F9. La F11-R **regulariza** '
         'ese entregable:', '',
         '- **Qué hace:** vuelve a presentar la misma arquitectura conceptual sobre la plantilla oficial, con su estructura de 8 '
         'secciones y sus identificadores CMP-xx.',
         '- **Qué no cambia:** la arquitectura. Los componentes, las relaciones, las capas, las decisiones, los estados y el '
         'diagrama ARQ-01 son los mismos.',
         '- **Versión anterior:** el F11 adaptado se conserva como **versión histórica**. Fue una adaptación académica válida '
         'en las condiciones de ese momento, no un error.', '',
         '| Versión | Archivos | Estado |', '|---|---|---|',
         '| **Definitiva** (F11-R) | [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_Colegio_Andino.docx) · '
         '[PDF](F11_Arquitectura_del_Sistema_Colegio_Andino.pdf) · [espejo `.md`](F11_Arquitectura_del_Sistema_Colegio_Andino.md) | '
         'Sobre la plantilla oficial. Pendiente de auditoría |',
         '| **Histórica** (F28, F29) | [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) · '
         '[PDF](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) · [espejo `.md`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.md) | '
         'Adaptación académica anterior. Se conserva **sin cambios** |', '',
         '## Estructura real de la plantilla oficial', '',
         'Cabecera con el logotipo de la Universidad Continental y «Asignatura: Pruebas y Calidad de Software». Título «Formato 11: '
         'Arquitectura del sistema». Ocho secciones numeradas:', '',
         '1. **Datos generales del proyecto:** tabla con los campos Nombre del proyecto, Integrantes del equipo, Módulo / '
         'Sistema, Docente y Fecha.',
         '2. **Descripción general del sistema:** instrucción «Describir brevemente:» y cuatro viñetas, cada una con una caja: '
         'Propósito del sistema, Alcance general, Usuarios principales y Relación con requerimientos y casos de uso.',
         '3. **Estilo arquitectónico propuesto:** instrucción «Seleccionar y justificar el estilo arquitectónico» y seis '
         'viñetas con caja: Cliente-Servidor, Capas (N-tier), Microservicios, Monolítico, Otros y Justificación.',
         '4. **Identificación de componentes:** tabla con las columnas ID · Componente · Descripción · Funcionalidades '
         'asociadas, y las filas de ejemplo CMP-01, CMP-02 y «…».',
         '5. **Relación entre componentes:** tabla con las columnas Componente origen · Componente destino · Tipo de '
         'interacción · Descripción.',
         '6. **Diagrama de Arquitectura conceptual:** instrucción «Insertar aquí el diagrama del sistema.» y una caja.',
         '7. **Decisiones de diseño:** instrucción «Registrar decisiones clave tomadas:» y tres viñetas de líneas en blanco.',
         '8. **Restricciones y consideraciones:** cuatro viñetas con caja: Tecnológicas, De rendimiento, De seguridad y De '
         'escalabilidad.', '',
         'Tratamiento de la plantilla en el entregable:', '',
         '- **Se conservan** la cabecera, los estilos, la numeración, los títulos, las viñetas, las cajas y las tablas, con sus '
         'columnas.',
         '- **Se retiran** las instrucciones y las líneas en blanco.',
         '- **Único añadido** fuera de la estructura: el recuadro «Estado de la información» tras los datos generales, igual '
         'que en los Formatos 02 a 08.', '',
         '## Matriz de correspondencia', '',
         md_table(['Sección oficial', 'Fuente en el F11 adaptado', 'Evidencia', 'Acción de regularización'], F.CORRESPONDENCIA), '',
         'Las secciones del F11 adaptado sin equivalente en la plantilla oficial **no se pierden**: siguen en el F11 adaptado '
         'histórico y en sus archivos de trabajo, que no cambian.', '',
         '| Sección del F11 adaptado | Dónde sigue |', '|---|---|',
         '| Correspondencia con la Guía 11 | F11 adaptado; [`F28_VALIDATION.md`](F28_VALIDATION.md) |',
         '| Flujo de información y flujo de RF-29 | F11 adaptado; [`RELATIONSHIPS.md`](RELATIONSHIPS.md) |',
         '| Arquitectura técnica de referencia | F11 adaptado. En el oficial, resumida en las secciones 3 y 8 |',
         '| RNF académicos → decisiones y componentes | F11 adaptado. En el oficial, dentro de las secciones 7 y 8 |',
         '| Validación (22 criterios) | [`VALIDATION.md`](VALIDATION.md) y `validate.py` (`f11_checks`) |',
         '| Trazabilidad por componente | [`../trazabilidad/F11-architecture-traceability.md`](../trazabilidad/F11-architecture-traceability.md) |', '',
         '## Equivalencia de identificadores CMP ↔ C', '',
         'Es uno a uno: no se combinan, dividen ni añaden componentes.', '',
         '- **CMP-xx:** identificador del Formato 11 oficial.',
         '- **Cxx:** identificador histórico. Lo conservan el F11 adaptado, `COMPONENTS.md`, `RELATIONSHIPS.md` y el diagrama '
         'ARQ-01.', '',
         md_table(['Formato 11 oficial', 'Histórico', 'Componente (nombre canónico)', 'Capa conceptual', 'Estado'],
                  [(F.CMP[c[0]], c[0], c[1], c[2], F.ESTADO_COMPONENTE[c[7]]) for c in AR.COMPONENTES]), '',
         '## Relaciones R-01 a R-20', '',
         'Se conservan tal como están en [`RELATIONSHIPS.md`](RELATIONSHIPS.md): mismo identificador con guion, mismo origen, '
         'destino y tipo, sin desdoblar las relaciones múltiples y sin R-21.', '',
         md_table(['ID', 'Origen', 'Destino', 'Tipo'], [(r[0], F.cmp_ref(r[1]), F.cmp_ref(r[2]), r[3]) for r in AR.RELACIONES]), '',
         '## ARQ-01', '',
         'Se reutiliza la exportación formal auditada en la F29 y el hotfix F29B ([`ARQ-01_Arquitectura_Conceptual.png`]('
         + rel('docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png') + ')), **sin rediseñarla ni '
         'retocarla**. Conserva los identificadores C01 a C17; el documento oficial aporta la equivalencia con CMP-xx. En el '
         'DOCX:', '',
         '- va dentro de la caja de la sección 6, en una página horizontal;',
         '- le siguen dos ampliaciones, que son recortes sin retoque.', '',
         'No se modificaron los modelos de PowerDesigner de la F29 ni los de la F23.', '',
         '## Diferencias entre el F11 adaptado y el Formato 11 oficial', '',
         '| Aspecto | F11 adaptado (F28) | F11 oficial (F11-R) |', '|---|---|---|',
         '| Base del documento | Paquete del F9 publicado (portada, cabecera «F11 ADAPTADO», pie de página y borde) | Plantilla oficial del Formato 11 (cabecera con logotipo y asignatura) |',
         '| Estructura | 14 secciones propias, derivadas de la Guía 11 | 8 secciones oficiales, con sus viñetas, cajas y tablas |',
         '| Identificadores | C01 a C17 | CMP-01 a CMP-17, con el histórico Cxx al lado |',
         '| Estilo arquitectónico | Descrito en la arquitectura técnica y en DA-01 | Respondido opción por opción del formato: monolito modular adoptado; cliente-servidor y capas como características complementarias; microservicios no adoptado |',
         '| Decisiones | Tabla DA-01 a DA-10 | Viñetas con estado (ADOPTADA, IMPLEMENTADA, PROPUESTA, EXPERIMENTAL). Se añade DA-11 (Docker Compose), una decisión ya aplicada |',
         '| Restricciones | Limitaciones y RNF → decisiones | Cuatro categorías oficiales, sin SLA ni métricas inventadas |',
         '| Arquitectura | 17 componentes, R-01 a R-20, 6 capas y ARQ-01 | **Sin cambios** |', '',
         '## Fuentes', '',
         'SHA-256 del contenido versionado. En los archivos de texto se calcula con finales de línea LF.', '',
         '| Fuente | Ruta | SHA-256 | Qué aporta |', '|---|---|---|---|']
    for path, what in sources:
        L.append(f'| {os.path.basename(path)} | [`{path}`]({rel(path)}) | `{sha256_versioned(os.path.join(root, path))}` | {what} |')
    L += ['', '## Validación', '',
          '`python docs/academico/tools/f27b/validate.py` incluye el bloque «F11-R». Comprueba:', '',
          '- que la plantilla está registrada y que el documento deriva de ella: cabecera, estilos y numeración idénticos;',
          '- la estructura oficial completa y la ausencia de instrucciones y líneas en blanco;',
          '- los datos generales;',
          '- CMP-01 a CMP-17 = C01 a C17 y R-01 a R-20 sin cambios;',
          '- ARQ-01 incrustado sin modificar;',
          '- el estilo, las decisiones con estado y las restricciones sin métricas inventadas;',
          '- la cobertura de RF-01 a RF-27 y CU-01 a CU-20;',
          '- el PDF;',
          '- que el F11 adaptado no cambió.', '',
          'La revisión visual de todas las páginas del PDF se registra en el informe de la fase.', '',
          '**Recuento de evidencias** (observación F11R-O01 de la auditoría):', '',
          '- Las tablas `evidencias/README.md` de las prácticas 02 a 11 suman **121 referencias** con SHA-256 a **91 archivos '
          'distintos**, con 0 ausentes, 0 discrepancias y 0 conflictos de hash. Es el recuento general vigente.',
          '- El «81» del primer informe de la F11-R era un subconjunto: solo las prácticas 03, 05, 08 y 11, las cuatro con '
          'integración de PowerDesigner, que suman 81 referencias a 68 archivos. No debe usarse como recuento general.', '',
          '## Limitaciones', '',
          '- **Sin validación institucional.** La validación es interna y académica, sin aprobación ni firma de la institución.',
          '- **RNF sin verificar.** RNF-06 (rendimiento) y RNF-07 (disponibilidad y recuperabilidad) siguen **NO VERIFICADOS**. '
          'La escalabilidad es una consideración, no una propiedad validada.',
          '- **Imágenes del PDF.** Microsoft Word reduce las imágenes del PDF a unos 200 ppp; el DOCX conserva la resolución de '
          'la exportación.',
          '- **LOW para la F31:** H-14, F28-L01, F29-L01, F29-L02 y F29B-OBS-01, sin cambios.']
    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(L)).rstrip() + '\n'
    with open(out_md, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
