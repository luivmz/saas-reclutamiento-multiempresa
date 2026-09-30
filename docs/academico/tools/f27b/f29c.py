"""F29C — Variables y matriz de operacionalización: Markdown, diagrama conceptual (SVG y PNG), anexo Word y registro de
la actividad de comparación de chatbots. Todo sale de m_variables.py, así que los artefactos no pueden contradecirse.

La guía E1/L1 pide documentar la matriz y el diagrama en el informe Word como «Anexo 1. Matriz de Operacionalización de
Variables» y «Anexo 2. Diseño conceptual de variables». El DOCX reutiliza el paquete de la plantilla oficial del Formato 11
solo por su cabecera institucional (logotipo y asignatura) y sus estilos; el cuerpo es propio y va en páginas horizontales.
"""
import os
import re
import zipfile
from xml.dom import minidom
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw

import diagrams as dg
import m_common as C
import m_cu as U
import m_variables as V
from docxgen import (_runs, box, image_data, image_xml, keep_image_resolution, sect_variant, split_blocks, EMU_CM,
                     TWIP_CM)

FECHA = '30/09/2026'
TITULO = 'Variables y matriz de operacionalización del proyecto (F29C)'


def cu_of(rfs):
    """CU del Formato 08 que implementan alguno de los RF (correspondencia real de m_cu.py)."""
    return sorted({c[0] for c in U.CU if set(c[4]) & set(rfs)})


def indicadores():
    for v in V.VARIABLES:
        for d in v['dimensiones']:
            for i in d['indicadores']:
                yield v, d, i


# ------------------------------------------------------------------ diagrama conceptual
W, H = 2000, 1260
COL = {'VI': ('#DCE9F7', '#2F5F8F'), 'VD': ('#E2F0D9', '#3D6B2E'), 'VIN': ('#FFF2CC', '#8A6D1F'), 'EXP': ('#EEEEEE', '#666666')}
BOXES = {
    'VIN-1': (60, 190, 560, 390), 'VIN-2': (60, 420, 560, 620), 'VIN-3': (60, 650, 560, 850),
    'VI': (680, 190, 1180, 850), 'VD': (1420, 190, 1940, 850), 'VIN-4': (1420, 930, 1940, 1130),
}


def layout():
    """Contenido de cada caja: (clave de color, encabezado, líneas de texto, discontinua)."""
    by = {v['id']: v for v in V.VARIABLES}
    out = {}
    for vid, (x0, y0, x1, y1) in BOXES.items():
        v = by[vid]
        kind = 'VI' if vid == 'VI' else 'VD' if vid == 'VD' else 'EXP' if v['estado'] == V.EXP else 'VIN'
        head = f'{vid} · Variable {v["tipo"].lower()}'
        lines = [v['nombre'], f'Estado: {v["estado"]}']
        if vid in ('VI', 'VD'):
            inds = [i for d in v['dimensiones'] for i in d['indicadores']]
            instr = [n for n in ('lista de cotejo', 'ficha de observación', 'cuestionario Likert')
                     if any(n.lower() in i['instrumento'].lower() for i in inds)]
            lines += ['', 'Dimensiones:'] + [f'{d["id"][-2:]} {d["nombre"]}' for d in v['dimensiones']]
            lines += ['', f'{len(inds)} indicadores y {sum(len(i["items"]) for i in inds)} ítems (Anexo 1).',
                      'Instrumentos: ' + '; '.join(instr) + '.']
        out[vid] = (kind, head, lines, v['estado'] == V.EXP)
    return out


ARROWS = [  # origen, destino, puntos, etiqueta, posición de la etiqueta, discontinua
    ('VIN-1', 'VI', [(560, 290), (680, 290)], 'condiciona', (620, 272), False),
    ('VIN-2', 'VI', [(560, 520), (680, 520)], 'orienta', (620, 502), False),
    ('VIN-3', 'VI', [(560, 750), (680, 750)], 'estructura', (620, 732), False),
    ('VI', 'VD', [(1180, 520), (1420, 520)], 'se propone que mejore', (1300, 490), False),
    ('VIN-4', 'VD', [(1680, 930), (1680, 850)], 'estima el riesgo de demora (experimental)', (1680, 890), True),
]


def render_png(path):
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.text((W // 2, 50), 'Diseño conceptual de variables — ' + C.INSTITUCION.split(' (')[0], font=dg.font(34, True),
           fill='#1F1F1F', anchor='mm')
    d.text((W // 2, 100), 'Plataforma SaaS multiempresa de reclutamiento, evaluación y selección (F29C, guía E1/L1)',
           font=dg.font(22), fill='#444444', anchor='mm')
    for vid, (kind, head, lines, dashed_) in layout().items():
        x0, y0, x1, y1 = BOXES[vid]
        fill, ink = COL[kind]
        d.rectangle((x0, y0, x1, y1), fill=fill, outline=None)
        if dashed_:
            dg.dashed(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], ink, width=3)
        else:
            d.rectangle((x0, y0, x1, y1), outline=ink, width=3)
        d.text((x0 + 16, y0 + 14), head, font=dg.font(22, True), fill=ink)
        y = y0 + 52
        for k, line in enumerate(lines):
            f = dg.font(22, True) if k == 0 else dg.font(19)
            for wl in dg.wrap(d, line, f, x1 - x0 - 32) if line else ['']:
                d.text((x0 + 16, y), wl, font=f, fill='#1F1F1F')
                y += 27 if k == 0 else 25
            if k == 0:
                y += 4
    for src, dst, pts, label, lpos, dashed_ in ARROWS:
        color = '#555555' if dashed_ else '#1F1F1F'
        if dashed_:
            dg.dashed(d, pts, color, width=3)
        else:
            d.line(pts, fill=color, width=3)
        dg.arrowhead(d, pts[-2], pts[-1], color, size=16)
        f = dg.font(18, italic=True)
        tw = d.textlength(label, font=f)
        lx, ly = lpos
        if src in ('VI', 'VIN-4'):
            d.rectangle((lx - tw / 2 - 6, ly - 13, lx + tw / 2 + 6, ly + 13), fill='white')
        d.text((lx, ly), label, font=f, fill=color, anchor='mm')
    d.text((60, 1180), 'Relación VI → VD: hipótesis de trabajo (TO-BE PROPUESTO), sin línea base ni mediciones. '
                       'La decisión final de selección es humana (RF-23).', font=dg.font(19), fill='#333333')
    d.text((60, 1212), 'Discontinuo: EXPERIMENTAL / PROPUESTO (RF-29, fuera de la línea base).',
           font=dg.font(19), fill='#555555')
    im.save(path, optimize=False)


def render_svg(path):
    """Misma disposición que el PNG, con texto vectorial. Los cortes de línea se calculan con las mismas métricas."""
    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           'font-family="Arial, Helvetica, sans-serif">',
           '<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<text x="{W // 2}" y="62" font-size="34" font-weight="bold" text-anchor="middle" fill="#1F1F1F">'
           f'{escape("Diseño conceptual de variables — " + C.INSTITUCION.split(" (")[0])}</text>',
           f'<text x="{W // 2}" y="108" font-size="22" text-anchor="middle" fill="#444444">'
           f'{escape("Plataforma SaaS multiempresa de reclutamiento, evaluación y selección (F29C, guía E1/L1)")}</text>']
    for vid, (kind, head, lines, dashed_) in layout().items():
        x0, y0, x1, y1 = BOXES[vid]
        fill, ink = COL[kind]
        dash = ' stroke-dasharray="10 7"' if dashed_ else ''
        out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{fill}" stroke="{ink}" '
                   f'stroke-width="3"{dash}/>')
        out.append(f'<text x="{x0 + 16}" y="{y0 + 34}" font-size="22" font-weight="bold" fill="{ink}">{escape(head)}</text>')
        y = y0 + 52
        for k, line in enumerate(lines):
            f = dg.font(22, True) if k == 0 else dg.font(19)
            for wl in dg.wrap(probe, line, f, x1 - x0 - 32) if line else ['']:
                weight = ' font-weight="bold"' if k == 0 else ''
                size = 22 if k == 0 else 19
                out.append(f'<text x="{x0 + 16}" y="{y + size - 2}" font-size="{size}"{weight} fill="#1F1F1F">{escape(wl)}</text>')
                y += 27 if k == 0 else 25
            if k == 0:
                y += 4
    for src, dst, pts, label, lpos, dashed_ in ARROWS:
        color = '#555555' if dashed_ else '#1F1F1F'
        dash = ' stroke-dasharray="10 7"' if dashed_ else ''
        p = ' '.join(f'{x},{y}' for x, y in pts)
        out.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="3"{dash} marker-end="url(#a)"/>')
        lx, ly = lpos
        if src in ('VI', 'VIN-4'):
            tw = probe.textlength(label, font=dg.font(18, italic=True))
            out.append(f'<rect x="{lx - tw / 2 - 6:.0f}" y="{ly - 13}" width="{tw + 12:.0f}" height="26" fill="white"/>')
        out.append(f'<text x="{lx}" y="{ly + 6}" font-size="18" font-style="italic" text-anchor="middle" '
                   f'fill="{color}">{escape(label)}</text>')
    out.append(f'<text x="60" y="1196" font-size="19" fill="#333333">{escape("Relación VI → VD: hipótesis de trabajo (TO-BE PROPUESTO), sin línea base ni mediciones. La decisión final de selección es humana (RF-23).")}</text>')
    out.append(f'<text x="60" y="1228" font-size="19" fill="#555555">{escape("Discontinuo: EXPERIMENTAL / PROPUESTO (RF-29, fuera de la línea base).")}</text>')
    out.append('</svg>')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out) + '\n')


# ------------------------------------------------------------------ Markdown
def md_esc(x):
    return str(x).replace('|', '\\|').replace('\n', '<br>')


def md_table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)] +
                     ['| ' + ' | '.join(md_esc(c) for c in r) + ' |' for r in rows])


def matrix_rows():
    """Filas de la matriz (una por indicador). La variable, sus definiciones y la dimensión se escriben en la primera
    fila de su grupo; en el DOCX esas celdas se combinan verticalmente."""
    rows = []
    for v in V.VARIABLES:
        first_v = True
        for d in v['dimensiones']:
            first_d = True
            for i in d['indicadores']:
                rows.append(dict(
                    variable=f'{v["id"]} — {v["nombre"]}' if first_v else '',
                    conceptual=v['conceptual'] if first_v else '', operacional=v['operacional'] if first_v else '',
                    dimension=f'{d["id"]} {d["nombre"]}' if first_d else '',
                    indicador=f'{i["id"]} {i["nombre"]}', items='\n'.join(f'• {x}' for x in i['items']),
                    instrumento=i['instrumento'], escala=i['escala'], vid=v['id'], did=d['id'],
                    first_v=first_v, first_d=first_d))
                first_v = first_d = False
    return rows


MATRIX_HEAD = ['Variable', 'Definición conceptual', 'Definición operacional', 'Dimensión', 'Indicador', 'Ítem',
               'Instrumento', 'Escala']


def trace_rows():
    rows = []
    for v, d, i in indicadores():
        rows.append((i['id'], ', '.join(i['rf']) or '—', ', '.join(cu_of(i['rf'])) or '—', ', '.join(i['rnf']) or '—',
                     ', '.join(i['ml']) or '—', i['estado'], i['fuente'] or '—'))
    return rows


TRACE_HEAD = ['Indicador', 'RF', 'CU (derivados de los RF, F8)', 'RNF', 'Variables RF-29', 'Estado', 'Fuente']


def build_md(out_md, png_rel, svg_rel, activity_rel):
    L = [f'# {TITULO}', '',
         '> Generado por `docs/academico/tools/f27b/f29c.py` desde `m_variables.py`. No editar a mano: '
         '`python docs/academico/tools/f27b/build.py f29c`. El anexo Word equivalente es '
         '[`F29C_Operacionalizacion_Variables.docx`](F29C_Operacionalizacion_Variables.docx).', '',
         '## Fuente normativa', '',
         'Guía de laboratorio **E1 «Desarrollo de Software con Inteligencia Artificial»** (Pruebas y Calidad de Software, '
         'Dr. Maglioni Arana Caparachin) y su versión **L1** (Taller de Investigación 2), con el mismo contenido '
         '(`00-fuentes-oficiales/guias-ia/`). Reglas que se aplican:', '',
         '- **Variables:**',
         '  - la solución es la variable independiente;',
         '  - el problema es la variable dependiente;',
         '  - la metodología, los principios y las herramientas de apoyo son las variables intermedias.',
         '- **Columnas de la matriz:** variables, dimensiones, indicadores, ítems de medición, instrumentos de recolección '
         'de datos y escala de medición.',
         '  - Cada variable tiene varias dimensiones, cada dimensión varios indicadores y cada indicador varios ítems.',
         '  - Instrumentos: ficha de observación, lista de cotejo o cuestionario Likert.',
         '- **Machine learning:** los indicadores de la variable dependiente son los que usa la predicción.',
         '- **Informe:** la matriz y el diagrama se documentan como **Anexo 1** y **Anexo 2**, junto con la definición '
         'conceptual.', '',
         'Esta matriz añade las columnas «Definición conceptual» y «Definición operacional», pedidas para el proyecto.', '',
         '> **Estado de la información:**',
         '>',
         '> - La matriz define **qué se mide y con qué**; no trae valores medidos.',
         '> - No hay línea base del AS-IS, y los cuestionarios Likert no se han aplicado.',
         '> - No se afirma validación institucional ni beneficios medidos.',
         '> - Cada indicador lleva su estado: HECHO VERIFICADO, AS-IS PRELIMINAR, TO-BE PROPUESTO, SOFTWARE IMPLEMENTADO '
         'o EXPERIMENTAL / PROPUESTO.', '',
         '## 1. Variables del proyecto', '',
         md_table(['ID', 'Tipo', 'Rol (guía E1/L1)', 'Variable', 'Estado'],
                  [(v['id'], v['tipo'], v['rol'], v['nombre'], v['estado']) for v in V.VARIABLES]), '',
         '**Definición conceptual y operacional:**', '']
    for v in V.VARIABLES:
        L += [f'- **{v["id"]} — {v["nombre"]}**',
              f'  - *Conceptual:* {v["conceptual"]}',
              f'  - *Operacional:* {v["operacional"]}']
    L += ['', '**Justificación de la selección:**', '',
          '- **VI:** es la solución que el proyecto construye. Sus dimensiones son las cinco soluciones S-01 a S-05 del '
          'TO-BE (Formato 05), implementadas en la plataforma v1.1.',
          '- **VD:** es el problema. Sus dimensiones son los problemas P1 a P5 (Formato 04) y los objetivos de mejora '
          'OM-01 a OM-05 (Formato 05).',
          '- **Intermedias:** solo se incluyen la metodología, las normas y las herramientas con evidencia en el '
          'repositorio.',
          '  - Con evidencia: TDD y pruebas automatizadas (`docs/tdd-evidence.md`); ISO/IEC 25010 como marco de referencia '
          '(capítulo 5); la arquitectura modular multiempresa con Docker (capítulo 7 y F11); el machine learning '
          'experimental de RF-29 (`docs/v1.1/ml/`).',
          '  - **Sin evidencia, no se incluyen:** Scrum, DevOps y SOLID, que la guía usa como ejemplo.', '',
          '## 2. Relaciones entre variables', '',
          md_table(['Origen', 'Destino', 'Relación', 'Estado'], V.RELACIONES), '', V.NOTA_RELACION, '',
          '## 3. Anexo 1. Matriz de Operacionalización de Variables', '',
          md_table(MATRIX_HEAD, [(r['variable'], r['conceptual'], r['operacional'], r['dimension'], r['indicador'],
                                  r['items'], r['instrumento'], r['escala']) for r in matrix_rows()]), '',
          '## 4. Trazabilidad de los indicadores', '',
          '- **RF, RNF y variables de RF-29:** se indican solo cuando hay correspondencia real.',
          '- **CU:** se derivan de los RF con la tabla del Formato 08, no a mano.',
          '- **Variables de RF-29:** son las del contrato de features del componente experimental.', '',
          md_table(TRACE_HEAD, trace_rows()), '',
          '## 5. Anexo 2. Diseño conceptual de variables', '',
          f'![Diseño conceptual de variables]({png_rel})', '',
          f'Versión vectorial: [`{os.path.basename(svg_rel)}`]({svg_rel}). La guía propone generar el diagrama con '
          'código Python; aquí lo genera `f29c.py` con Pillow, de forma reproducible.', '',
          '## 6. Actividad de la guía E1/L1 con IA', '',
          V.ESTADO_ACTIVIDAD, '',
          f'- **Criterio de alcance:** {V.CRITERIO_DOCENTE}',
          f'- **Requisitos de la guía, alcance, prompts y protocolo:** [`ACTIVIDAD_IA_COMPARACION.md`]({activity_rel}).',
          f'- **Evidencia ejecutada:** [`{V.REGISTRO}`]({V.REGISTRO}).', '',
          V.NOTA_ELABORACION, '']
    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(L)).rstrip() + '\n'
    with open(out_md, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


CATEGORIAS = [
    ('REQUISITO DE LA GUÍA', 'Lo que propone la guía E1/L1 (enunciados 1 a 4). Se conserva tal cual, aunque no todo se '
                             'exija en este entregable.'),
    ('ALCANCE EFECTIVO DEL ENTREGABLE', 'Lo que se exige para cerrar la F29C según el criterio docente informado por el '
                                        'equipo.'),
    ('EVIDENCIA EJECUTADA', 'Solo las filas del registro con estado `Completo` y la respuesta pegada.'),
    ('NO REQUERIDO', 'Fuera del alcance efectivo. No se ejecuta ni se presenta como ejecutado.'),
]


def build_activity(out_md):
    """Paquete de ejecución de la actividad E1/L1: requisito de la guía, alcance efectivo, prompts listos para copiar y
    evidencia mínima. Se genera desde m_variables.py; los resultados van en el registro, que es del equipo."""
    reg = V.REGISTRO
    L = ['# Actividad E1/L1 — paquete de ejecución', '',
         '> Generado por `docs/academico/tools/f27b/f29c.py` desde `m_variables.py`: no se edita a mano. La evidencia '
         f'se registra en [`{reg}`]({reg}), que completa el equipo.', '',
         f'**Estado:** {V.ESTADO_ACTIVIDAD}', '',
         '**Categorías que usa este paquete:**', '',
         md_table(['Categoría', 'Significado'], [(f'**{a}**', b) for a, b in CATEGORIAS]), '',
         '## 1. REQUISITO DE LA GUÍA', '',
         'Texto de la guía E1 («Actividades para la sesión»). La L1 propone lo mismo.', '',
         md_table(['Enunciado', 'Pedido de la guía E1', 'Entrega que implica'], V.ENUNCIADOS), '',
         f'Chat compartido por el docente en la guía (enunciado 3): {V.CHAT_DOCENTE}', '',
         '## 2. ALCANCE EFECTIVO DEL ENTREGABLE', '',
         f'**{V.CRITERIO_DOCENTE}**', '',
         V.NOTA_E3, '',
         md_table(['ID', 'Enunciado', 'Requisito de la guía', 'Alcance en este entregable', 'Dónde consta'],
                  V.REQUISITOS), '',
         '## 3. EVIDENCIA EJECUTADA', '',
         f'- **Dónde está:** en el [registro]({reg}). Solo cuenta como evidencia ejecutada una fila con estado '
         '`Completo`, sus datos y la respuesta completa pegada.',
         '- **Cuántas ejecuciones exige el alcance efectivo:** '
         + ', '.join(f'{e[0]} ({e[2]})' for e in V.EJECUCIONES_REQUERIDAS) + ', todas en ChatGPT.',
         '- **Estado actual:** lo informa `python docs/academico/tools/f27b/validate.py --cierre-f29c`.',
         '- **Capítulos 1 y 2:** P-05 y P-06 son evidencia de la actividad, no reemplazan los capítulos. La fuente canónica '
         'es la documentación del repositorio:']
    L += [f'  - [`{c[1]}`](../../../{c[1]}).' for c in V.CAPITULOS]
    L += ['- **Diferencias:** las que haya entre una respuesta y la fuente canónica se anotan en el registro, sin '
          'sobrescribir el contenido validado.', '',
          '## 4. NO REQUERIDO', '',
          md_table(['ID', 'Requisito de la guía', 'Estado'], [(r[0], f'{r[1]}: {r[2]}', r[3]) for r in V.REQUISITOS
                                                             if r[3] == V.NO_REQUERIDO]), '',
          '**Qué implica:**', '',
          '- Las filas R-05 a R-16 (Gemini, DeepSeek y Copilot) y T-01 (chat del docente) se conservan en el registro como '
          'constancia histórica de lo que propone la guía, con ese estado.',
          '- Nunca se marcan `Completo` ni se citan como ejecutadas.',
          '- Si el equipo decide ejecutarlas, se cambia su alcance en `m_variables.py` y se registran como evidencia.', '',
          '## 5. Protocolo de ejecución (alcance efectivo)', '',
          '1. **Una conversación nueva de ChatGPT.** La guía pide la versión gratuita: anota el plan que se usó.',
          '2. **Prompts en orden y sin editar.** Pega P-01 a P-06 en esa misma conversación, uno por mensaje, y espera a '
          'que cada respuesta termine antes del siguiente.',
          '3. **Una respuesta por prompt.** Si regeneraste alguna, registra la que usaste.',
          '4. **Cada respuesta se pega completa y sin editar** en su sección del registro.',
          '5. **Enlace y captura.** Guarda el enlace compartido o una captura si puedes. Si no hay ninguno, escribe «No '
          'disponible»: la evidencia queda como texto aportado por el equipo, y así se declara.',
          '6. **P-03:** anota si el código Python se ejecutó en Google Colab sin corregirlo.',
          '7. **P-05 y P-06:** completa la sección «Integración con los capítulos 1 y 2» del registro. Anota coincidencias y '
          'diferencias con la fuente canónica y cómo se tratan; los capítulos del repositorio no se sobrescriben.',
          '8. **No pegues datos personales reales:** el caso de estudio es ficticio.',
          '9. **Comprueba el cierre:** `python docs/academico/tools/f27b/validate.py --cierre-f29c`.', '',
          '## 6. Prompts listos para copiar', '']
    for pid, uso, enun, texto in V.PROMPTS:
        L += [f'### {pid} — {uso} ({enun})', '', '```text', texto, '```', '']
    L += ['## 7. Evidencia mínima por ejecución', '',
          md_table(['Campo', 'Qué se registra'], [
              ('Chatbot y modelo', 'Nombre del chatbot y modelo o versión que muestra la interfaz'),
              ('Plan', 'Gratuito u otro; «No informado» si no se registró'),
              ('Fecha', 'Día de la ejecución, en formato DD/MM/AAAA'),
              ('Prompt usado', '«Sin cambios», o «Modificado» con el prompt real y el motivo'),
              ('Respuesta', 'Texto completo, sin editar, entre `~~~~text` y `~~~~`'),
              ('Enlace', 'Enlace compartido o «No disponible»; nunca uno inventado'),
              ('Captura', 'Ruta en `evidencias-ia/capturas/`, «No disponible», o «No aplica» si hay enlace'),
          ]), '',
          '## Qué no se hace', '',
          '- No se escribe ninguna respuesta, cifra ni conclusión sin la ejecución real que la respalde.',
          '- No se presenta como ejecutado nada NO REQUERIDO, ni como texto de la guía el criterio docente informado por el '
          'equipo.',
          '- ' + V.NOTA_ELABORACION]
    text = '\n'.join(L).rstrip() + '\n'
    with open(out_md, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


# ------------------------------------------------------------------ registro de ejecuciones (lo completa el equipo)
PEND = 'Pendiente'
RUN_HEAD = ['ID', 'Chatbot', 'Prompt', 'Modelo / versión', 'Plan', 'Fecha', 'Prompt usado', 'Enlace', 'Captura', 'Estado']
INT_HEAD = ['Capítulo', 'Fuente canónica', 'Evidencia', 'Coincidencias', 'Diferencias con la fuente canónica',
            'Tratamiento']
S1, S2, S3, S4, S5 = ('## 1. ALCANCE EFECTIVO — evidencia de ChatGPT (P-01 a P-06)',
                      '## 2. ALCANCE EFECTIVO — integración con los capítulos 1 y 2',
                      '## 3. NO REQUERIDO — Gemini, DeepSeek y Copilot (enunciado 2)',
                      '## 4. NO REQUERIDO — comparaciones (enunciados 2 y 3)',
                      '## 5. Respuestas completas (evidencia ejecutada)')
NO_REQ_ITEMS = [
    ('Cuadro comparativo de los 4 chatbots y diferencias cruciales (enunciado 2)', 'REQ-04'),
    (f'T-01: revisión del chat compartido por el docente ({V.CHAT_DOCENTE}) (enunciado 3)', 'REQ-05'),
    ('Cuadro comparativo con el chat del docente y respuesta a sus dos preguntas (enunciado 3)', 'REQ-05'),
]


def registro_template():
    L = ['# Registro de ejecuciones de la actividad E1/L1 (F29C)', '',
         '> **Lo completa el equipo con evidencia real.**',
         '>',
         '> - `build.py f29c` crea este archivo solo si no existe; **nunca lo sobrescribe**.',
         '> - Requisitos, alcance y prompts: [`../ACTIVIDAD_IA_COMPARACION.md`](../ACTIVIDAD_IA_COMPARACION.md).', '',
         '**Categorías:**', ''] + [f'- **{a}:** {b}' for a, b in CATEGORIAS] + [
         '', f'**{V.CRITERIO_DOCENTE}**', '',
         '**Valores admitidos:**', '',
         '- **Fecha:** DD/MM/AAAA.',
         '- **Prompt usado:** `Sin cambios` o `Modificado`. Si es `Modificado`, en la sección de la respuesta se añade el '
         'prompt real entre `~~~~prompt` y `~~~~`, y una línea `Motivo del cambio: …`.',
         '- **Enlace:** una URL `https://` o `No disponible`.',
         '- **Captura:** rutas relativas a esta carpeta (`capturas/R-01.png`) separadas por `;`, o `No disponible`. `No '
         'aplica` solo vale si hay enlace.',
         '- **Sin enlace ni captura:** la evidencia es el texto de la respuesta aportado por el equipo, y se declara así.',
         '- **Estado:** `Pendiente` o `Completo`. `Completo` exige todos los campos y la respuesta pegada.',
         '- **Respuestas:** se pegan completas entre `~~~~text` y `~~~~`. Así el código Python de P-03 no rompe el '
         'registro.',
         '- **Columnas fijas:** no se modifican las columnas ID, Chatbot ni Prompt.', '',
         S1, '', md_table(RUN_HEAD, [e + (PEND,) * 7 for e in V.EJECUCIONES_REQUERIDAS]), '',
         S2, '',
         '- **Fuente canónica:** los capítulos del repositorio, que no se sobrescriben.',
         '- **P-05 y P-06:** son evidencia de la actividad.',
         '- **Qué se anota:** qué coincide, qué difiere y cómo se trata cada diferencia (por ejemplo, «se descarta: dato no '
         'validado»).', '',
         md_table(INT_HEAD, [(c[0], c[1], c[2], PEND, PEND, PEND) for c in V.CAPITULOS]), '',
         S3, '',
         'Nota histórica: la guía E1/L1 propone ejecutar P-01 a P-04 también en Gemini, DeepSeek y Copilot. Por el criterio '
         'docente informado por el equipo, no se exigen en este entregable. **No se ejecutaron** y no se presentan como '
         'ejecutados.', '',
         md_table(RUN_HEAD, [e + ('—',) * 6 + (V.NO_REQUERIDO,) for e in V.EJECUCIONES_NO_REQUERIDAS]), '',
         S4, '',
         'Nota histórica: la guía propone estas comparaciones. ' + V.NOTA_E3, ''] + [
         f'- {t}: **{V.NO_REQUERIDO}**' for t, _ in NO_REQ_ITEMS] + ['', S5, '']
    for rid, bot, pid in V.EJECUCIONES_REQUERIDAS:
        L += [f'### {rid} · {bot} · {pid}', '', 'Respuesta completa, sin editar, entre las dos líneas `~~~~`:', '',
              '~~~~text', PEND, '~~~~', '']
    return '\n'.join(L).rstrip() + '\n'


def build_registro(path):
    """Crea el registro vacío si no existe. Si existe, no lo toca: sus datos son evidencia del equipo."""
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(registro_template())
    return True


def _section(text, start, end=None):
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i + len(start)) if end else -1
    return text[i + len(start):j if j >= 0 else len(text)]


def _rows(block):
    out = []
    for line in (block or '').splitlines():
        line = line.strip()
        if line.startswith('|') and not line.startswith('|---'):
            out.append([c.strip() for c in line.strip('|').split('|')])
    return out[1:] if out else []


def leer_registro(path):
    """Lee el registro: ejecuciones requeridas y no requeridas, integración con los capítulos, elementos NO REQUERIDO
    de las comparaciones y las respuestas pegadas."""
    text = open(path, encoding='utf-8').read()

    def runs(sec):
        return {c[0]: dict(zip(RUN_HEAD, c)) for c in _rows(sec) if len(c) == len(RUN_HEAD)}
    s4 = _section(text, S4, S5) or ''
    no_req = [l[2:].strip() for l in s4.splitlines() if l.startswith('- ')]
    answers = {}
    s5 = _section(text, S5) or ''
    for m in re.finditer(r'^### (R-\d\d) · ([^·\n]+) · (P-\d\d)\s*$', s5, re.M):
        nxt = re.search(r'^### R-\d\d ', s5[m.end():], re.M)
        body = s5[m.end():m.end() + nxt.start()] if nxt else s5[m.end():]
        resp = re.search(r'^~~~~text\n(.*?)\n~~~~[ \t]*$', body, re.S | re.M)
        prompt = re.search(r'^~~~~prompt\n(.*?)\n~~~~[ \t]*$', body, re.S | re.M)
        motivo = re.search(r'Motivo del cambio:[ \t]*(.+)', body)
        answers[m.group(1)] = dict(bot=m.group(2).strip(), prompt_id=m.group(3),
                                   respuesta=resp.group(1).strip() if resp else None,
                                   prompt=prompt.group(1).strip() if prompt else None,
                                   motivo=motivo.group(1).strip() if motivo else None)
    return dict(runs=runs(_section(text, S1, S2)), no_req_runs=runs(_section(text, S3, S4)),
                integracion=[c for c in _rows(_section(text, S2, S3)) if len(c) == len(INT_HEAD)],
                no_req=no_req, answers=answers, text=text)


# ------------------------------------------------------------------ anexo Word
def _p(text, sz=18, bold=False, italic=False, jc='left', after=100, keep=False):
    kn = '<w:keepNext/>' if keep else ''
    return (f'<w:p><w:pPr>{kn}<w:spacing w:after="{after}" w:line="252" w:lineRule="auto"/><w:jc w:val="{jc}"/>'
            f'</w:pPr>{_runs(text, bold=bold, italic=italic, sz=sz)}</w:p>')


def _cell(text, width, sz=14, bold=False, fill=None, merge=None):
    paras = ''.join(f'<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/></w:pPr>'
                    f'{_runs(line, bold=bold, sz=sz)}</w:p>' for line in (str(text).split('\n') or ['']))
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
    vm = {'start': '<w:vMerge w:val="restart"/>', 'cont': '<w:vMerge/>'}.get(merge, '')
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{vm}{shd}</w:tcPr>{paras}</w:tc>'


def _table(headers, rows, widths, sz=14, merges=None):
    """Tabla con encabezado repetido. merges[i][j] = 'start' | 'cont' | None para combinar celdas verticalmente."""
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    xml = [f'<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/><w:tblW w:w="{sum(widths)}" w:type="dxa"/>'
           '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
           f'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>',
           '<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' +
           ''.join(_cell(h, w, sz, True, 'D9E2F3') for h, w in zip(headers, widths)) + '</w:tr>']
    for k, r in enumerate(rows):
        m = merges[k] if merges else [None] * len(r)
        xml.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>' +
                   ''.join(_cell(c if mm != 'cont' else '', w, sz, merge=mm) for c, w, mm in zip(r, widths, m)) + '</w:tr>')
    xml.append('</w:tbl>')
    return ''.join(xml) + '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'


def build_docx(template, png, out_docx):
    zin = zipfile.ZipFile(template)
    document = zin.read('word/document.xml').decode('utf-8')
    rels = zin.read('word/_rels/document.xml.rels').decode('utf-8')
    head, rest = document.split('<w:body>', 1)
    body, tail = rest.rsplit('</w:body>', 1)
    sect = split_blocks(body)[-1][1]
    land = sect_variant(sect, landscape=True)
    m = re.search(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"', land)
    mar = {k: int(v) for k, v in re.findall(r'w:(left|right|top|bottom)="(\d+)"', re.search(r'<w:pgMar[^>]*/>', land).group(0))}
    TW = int(m.group(1)) - mar['left'] - mar['right']            # ancho útil de la página horizontal (twips)
    P = []
    P.append(_p(TITULO, sz=30, bold=True, jc='center', after=60))
    P.append(_p('Anexos del proyecto según la guía de laboratorio E1/L1 «Desarrollo de Software con Inteligencia '
                'Artificial»', sz=20, italic=True, jc='center', after=160))
    P.append(_table(['Campo', 'Valor'], [
        ('Nombre del proyecto', C.PROYECTO), ('Integrantes del equipo', C.EQUIPO),
        ('Asignatura', 'Pruebas y Calidad de Software (NRC 28607)'), ('Docente', C.DOCENTE), ('Fecha', FECHA)],
        [int(TW * 0.22), TW - int(TW * 0.22)], sz=16))
    P.append(box(['**Estado de la información de este documento**'] + C.LEYENDA +
                 ['La matriz define qué se mide y con qué instrumento; **no contiene valores medidos**. No hay línea base '
                  'del AS-IS y los cuestionarios Likert no se han aplicado. No se afirma validación institucional ni '
                  'beneficios medidos.'] + C.REGLAS_FIJAS, sz=16, fill='FFF2CC').replace(
        '<w:tblInd w:w="284" w:type="dxa"/>', '').replace('w:w="8216"', f'w:w="{TW}"'))
    P.append(_p('1. Variables del proyecto', sz=24, bold=True, keep=True, after=80))
    P.append(_p('Regla de la guía: la solución es la variable independiente; el problema, la dependiente; la metodología, '
                'los principios y las herramientas de apoyo, las intermedias. Solo se incluyen intermedias con evidencia '
                'en el repositorio: Scrum, DevOps y SOLID (ejemplos de la guía) no se incluyen porque el proyecto no los '
                'documenta.', sz=16, after=80))
    w5 = [int(TW * f) for f in (0.07, 0.19, 0.33, 0.29)]
    w5.append(TW - sum(w5))
    P.append(_table(['ID', 'Variable (tipo)', 'Definición conceptual', 'Definición operacional', 'Estado'],
                    [(v['id'], f'{v["nombre"]}\n({v["tipo"]}: {v["rol"].split(" (")[0].lower()})', v['conceptual'],
                      v['operacional'], v['estado']) for v in V.VARIABLES], w5, sz=15))
    P.append(_p('2. Relaciones entre variables', sz=24, bold=True, keep=True, after=80))
    w4 = [int(TW * f) for f in (0.12, 0.12, 0.52)]
    w4.append(TW - sum(w4))
    P.append(_table(['Origen', 'Destino', 'Relación', 'Estado'], V.RELACIONES, w4, sz=15))
    P.append(_p(V.NOTA_RELACION, sz=16, italic=True, after=160))
    P.append(_p('Anexo 1. Matriz de Operacionalización de Variables', sz=24, bold=True, keep=True, after=80))
    fr = (0.10, 0.13, 0.13, 0.10, 0.11, 0.24, 0.10)
    w8 = [int(TW * f) for f in fr]
    w8.append(TW - sum(w8))
    rows, merges = [], []
    mr = matrix_rows()
    for r in mr:
        rows.append((r['variable'], r['conceptual'], r['operacional'], r['dimension'], r['indicador'], r['items'],
                     r['instrumento'], r['escala']))
        mv = 'start' if r['first_v'] else 'cont'
        md = 'start' if r['first_d'] else 'cont'
        merges.append([mv, mv, mv, md, None, None, None, None])
    P.append(_table(MATRIX_HEAD, rows, w8, sz=13, merges=merges))
    P.append(_p('Trazabilidad de los indicadores', sz=24, bold=True, keep=True, after=80))
    P.append(_p('RF, RNF y variables de RF-29 solo cuando hay correspondencia real; los CU se derivan de los RF con la '
                'tabla del Formato 08.', sz=16, after=80))
    w7 = [int(TW * f) for f in (0.10, 0.15, 0.17, 0.10, 0.15, 0.13)]
    w7.append(TW - sum(w7))
    P.append(_table(TRACE_HEAD, trace_rows(), w7, sz=13))
    P.append(_p('Actividad de la guía E1/L1 con IA (enunciados 1 a 4): ' + V.ESTADO_ACTIVIDAD, sz=16, after=60))
    P.append(_p(V.CRITERIO_DOCENTE + ' Requisitos, alcance y prompts: docs/academico/operacionalizacion/'
                'ACTIVIDAD_IA_COMPARACION.md; evidencia: docs/academico/operacionalizacion/' + V.REGISTRO + '.',
                sz=16, after=80))
    P.append(_p(V.NOTA_ELABORACION, sz=16, italic=True, after=160))
    P.append(_p('Anexo 2. Diseño conceptual de variables', sz=24, bold=True, keep=True, after=80))
    data, w, h = image_data(png)
    cx = int((TW / TWIP_CM - 0.5) * EMU_CM)
    cy = int(cx * h / w)
    max_cy = int(13.0 * EMU_CM)
    if cy > max_cy:
        cy, cx = max_cy, int(max_cy * w / h)
    rels = rels.replace('</Relationships>', '<Relationship Id="rId201" Type="http://schemas.openxmlformats.org/'
                        'officeDocument/2006/relationships/image" Target="media/f29c_1.png"/></Relationships>')
    P.append(image_xml('rId201', 201, os.path.basename(png), cx, cy))
    P.append(_p('Figura 1. Diseño conceptual de variables: VI, VD y variables intermedias. Generado con Python '
                '(f29c.py) desde m_variables.py.', sz=16, italic=True, jc='center', after=120))
    P.append(land)
    new_doc = head + '<w:body>' + ''.join(P) + '</w:body>' + tail
    minidom.parseString(new_doc.encode('utf-8'))
    core = zin.read('docProps/core.xml').decode('utf-8')
    core = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>', f'<dc:title>{escape(TITULO)}</dc:title>', core)
    core = re.sub(r'<dc:creator>.*?</dc:creator>', f'<dc:creator>{escape(C.EQUIPO)}</dc:creator>', core)
    core = re.sub(r'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', '<cp:lastModifiedBy>Equipo del proyecto</cp:lastModifiedBy>', core)
    fixed = (2026, 9, 30, 0, 0, 0)
    with zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            d = zin.read(info.filename)
            if info.filename == 'word/document.xml':
                d = new_doc.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                d = rels.encode('utf-8')
            elif info.filename == 'docProps/core.xml':
                d = core.encode('utf-8')
            elif info.filename == 'word/settings.xml':
                d = keep_image_resolution(d.decode('utf-8')).encode('utf-8')
            zi = zipfile.ZipInfo(info.filename, date_time=fixed)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, d)
        zi = zipfile.ZipInfo('word/media/f29c_1.png', date_time=fixed)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zout.writestr(zi, data)
