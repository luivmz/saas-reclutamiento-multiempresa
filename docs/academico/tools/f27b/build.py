"""Construye los entregables F2 a F8 de la Fase 27B.

Uso (desde la raíz del repositorio):  python docs/academico/tools/f27b/build.py [f2 f3 ...]

Para cada práctica genera: el DOCX sobre la plantilla oficial, su espejo en Markdown (mismo
contenido, para revisión en Git) y los borradores PNG en diagramas/draft/. Las plantillas de
docs/academico/00-fuentes-oficiales/ solo se leen.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
ACAD = os.path.join(ROOT, 'docs', 'academico')
FMT = os.path.join(ACAD, '00-fuentes-oficiales', 'formatos-originales')

from docxgen import Doc, build_docx, build_md, build_docx_f9  # noqa: E402
import diagrams as dg  # noqa: E402
import m_common as C  # noqa: E402

BUILDERS = {}


def builder(key):
    def deco(fn):
        BUILDERS[key] = fn
        return fn
    return deco


def pdir(n, *parts):
    d = os.path.join(ACAD, f'practica-{n:02d}', *parts)
    os.makedirs(d, exist_ok=True)
    return d


# Archivos de texto que git versiona con finales de línea LF (.gitattributes: text=auto eol=lf). PowerDesigner los
# escribe con CRLF; el SHA-256 se calcula sobre el contenido versionado, igual que en el manifiesto de la F29.
TEXT_EXT = ('.md', '.svg', '.bpm', '.oom', '.py', '.ps1', '.txt', '.json', '.csv')


def sha256_versioned(full):
    import hashlib
    with open(full, 'rb') as f:
        data = f.read()
    if full.lower().endswith(TEXT_EXT):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def write_evidence(n, title, items, note=None):
    """evidencias/README.md: cada evidencia con ruta relativa y SHA-256 del contenido versionado."""
    out = os.path.join(pdir(n, 'evidencias'), 'README.md')
    lines = [f'# Evidencias — {title}', '',
             'Evidencias reales del repositorio que respaldan el formato. Rutas relativas a la raíz del repositorio. '
             'SHA-256 calculado en la Fase 27B sobre el archivo versionado. No hay capturas institucionales ni firmas: '
             'no existen en el repositorio y no se simulan.', '']
    if note:
        lines += [note, '']
    lines += ['| Evidencia | Ruta | SHA-256 | Qué respalda |', '|---|---|---|---|']
    for path, what in items:
        full = os.path.join(ROOT, path)
        if os.path.isdir(full):
            h = '(carpeta)'
        else:
            h = '`' + sha256_versioned(full) + '`'
        link = os.path.relpath(full, os.path.dirname(out)).replace(os.sep, '/')
        lines.append(f'| {os.path.basename(path.rstrip("/"))} | [`{path}`]({link}) | {h} | {what} |')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')


# --------------------------------------------------------------------------- PowerDesigner (F29, integración post-F29)
PD = 'docs/academico/powerdesigner'
SUPERSEDED = 'DRAFT / SUPERSEDED BY F29 FORMAL EXPORT'
NOTA_EVID_F29 = ('**Integración posterior a la F29 (28/09/2026):** el diagrama principal del formato es la exportación formal '
                 'de PowerDesigner, auditada en la F29 y en el hotfix F29B. Las capturas de PowerDesigner son reales: se '
                 'tomaron de la ventana de PowerDesigner 16.6 con los modelos reabiertos desde el disco, sin simulación ni '
                 'retoque. Los borradores quedan como antecedente (' + SUPERSEDED + '). SHA-256 recalculado en esta '
                 'integración; en los archivos de texto, sobre el contenido versionado (LF).')


def pd(*parts):
    return os.path.join(ROOT, *PD.split('/'), *parts)


def estado(doc, extra=()):
    doc.note('Estado de la información de este formato', C.LEYENDA + list(extra) + C.REGLAS_FIJAS)


def emit(n, stem, template, kind, doc, title, preface=''):
    out_docx = os.path.join(pdir(n), stem + '.docx')
    out_md = os.path.join(pdir(n), stem + '.md')
    datos = C.datos(kind)
    build_docx(os.path.join(FMT, template), out_docx, datos, doc, title=title)
    build_md(out_md, title, datos, doc,
             preface=preface or (f'> Espejo en Markdown de `{stem}.docx`, generado desde el mismo modelo '
                                 '(`docs/academico/tools/f27b/`). El entregable es el DOCX.'))
    print('OK', os.path.relpath(out_docx, ROOT))


# --------------------------------------------------------------------------- F2 y F3 (AS-IS)
import m_asis as A  # noqa: E402

AS = {a[0]: a for a in A.ACTIVIDADES}


def asis_flowchart():
    """Diagrama de flujo AS-IS (símbolos básicos) en dos partes, para el Formato 02."""
    kw = dict(show_lanes=False, CW=470, RH=118, TW=410, TH=84, FS=20)
    lab = lambda i: f'{i} · {AS[i][1]}\n({", ".join(a for a, r in AS[i][4] if r in ("Ejecuta", "Valida"))})'
    N_ = A.NOMBRE
    p1 = dg.Swimlanes('F2 · Flujo del proceso actual (AS-IS preliminar) — parte 1 de 2',
                      [('', ''), ('', '')], 'Sujeto a validación institucional. Actor responsable entre paréntesis.', **kw)
    p1.node('ini', 'terminator', 0, 0, f'Inicio: {N_["EI-01"].lower()}')
    for r, i in enumerate(['AS-01', 'AS-02', 'AS-03', 'AS-04'], start=1):
        p1.node(i, 'task', 0, r, lab(i))
    p1.node('g1', 'gateway', 0, 5, f'G-01 {N_["G-01"]}')
    p1.node('f1', 'terminator', 1, 5, f'Fin: {N_["EF-01"].lower()}')
    for r, i in enumerate(['AS-05', 'AS-06', 'AS-07', 'AS-08'], start=6):
        p1.node(i, 'task', 0, r, lab(i))
    p1.node('c1', 'terminator', 0, 10, 'Continúa en la parte 2 (A)')
    seq = ['ini', 'AS-01', 'AS-02', 'AS-03', 'AS-04', 'g1', 'AS-05', 'AS-06', 'AS-07', 'AS-08', 'c1']
    for a, b in zip(seq, seq[1:]):
        p1.edge(a, b, 'Sí' if a == 'g1' else '')
    p1.edge('g1', 'f1', 'No')
    path1 = os.path.join(pdir(2, 'diagramas', 'draft'), 'F2-flujo-as-is-parte1.png')
    p1.render(path1, 'Fuente: docs/final-report/03-procesos-negocio.md §3.1 (8 actividades macro), desagregadas en AS-01 a AS-14.')
    p2 = dg.Swimlanes('F2 · Flujo del proceso actual (AS-IS preliminar) — parte 2 de 2',
                      [('', ''), ('', '')], 'Sujeto a validación institucional. AS-09 a AS-11 se repiten por cada candidato.', **kw)
    p2.node('c2', 'terminator', 0, 0, 'Viene de la parte 1 (A)')
    p2.node('AS-09', 'task', 0, 1, lab('AS-09'))
    p2.node('g2', 'gateway', 0, 2, f'G-02 {N_["G-02"]}')
    p2.node('f2', 'terminator', 1, 2, f'Fin (para ese candidato): {N_["EF-02"].lower()}')
    for r, i in enumerate(['AS-10', 'AS-11', 'AS-12', 'AS-13', 'AS-14'], start=3):
        p2.node(i, 'task', 0, r, lab(i))
    p2.node('f3', 'terminator', 0, 8, f'Fin: {N_["EF-03"].lower()}')
    seq = ['c2', 'AS-09', 'g2', 'AS-10', 'AS-11', 'AS-12', 'AS-13', 'AS-14', 'f3']
    for a, b in zip(seq, seq[1:]):
        p2.edge(a, b, 'Sí' if a == 'g2' else '')
    p2.edge('g2', 'f2', 'No')
    path2 = os.path.join(pdir(2, 'diagramas', 'draft'), 'F2-flujo-as-is-parte2.png')
    p2.render(path2, 'Borrador de revisión. La formalización BPMN (con SP-01 por candidato) está en el Formato 03.')
    return [path1, path2]


def asis_bpmn(n=3, prefix='F3-bpmn-as-is', badges=None, tag='F3'):
    """BPMN AS-IS en carriles verticales, dos partes unidas por un evento de enlace (especificación F27D)."""
    badges = badges or {}
    lanes = A.LANES
    N_ = A.NOMBRE
    kw = dict(CW=310, RH=122, TW=262, TH=92, FS=19)
    sub = 'BPMN AS-IS preliminar derivado del análisis del equipo — sujeto a validación institucional'
    t = lambda i: f'{i}\n{AS[i][1]}'
    b1 = dg.Swimlanes(f'{tag} · BPMN del proceso actual (AS-IS preliminar) — parte 1 de 2', lanes, sub, **kw)
    b1.node('EI-01', 'start', 0, 0, f'EI-01 {N_["EI-01"]}')
    b1.node('AS-01', 'task', 0, 1, t('AS-01'))
    b1.node('AS-02', 'task', 0, 2, t('AS-02'))
    b1.node('AS-03', 'task', 1, 3, t('AS-03'))
    b1.node('AS-04', 'task', 2, 4, t('AS-04'))
    b1.node('G-01', 'gateway', 2, 5, f'G-01 {N_["G-01"]}', off=-70)
    b1.node('EF-01', 'end', 2, 5, f'EF-01 {N_["EF-01"]}', off=70)
    b1.node('AS-05', 'task', 1, 6, t('AS-05'))
    b1.node('AS-06', 'task', 1, 7, t('AS-06'))
    b1.node('EP-01', 'start', 4, 7, f'EP-01 {N_["EP-01"]}', off=-100)
    b1.node('AS-07', 'task', 4, 8, t('AS-07'))
    b1.node('EP-02', 'end', 4, 9, f'EP-02 {N_["EP-02"]}', off=-100)
    b1.node('AS-08', 'task', 1, 9, t('AS-08') + '\n(tarea de recepción)')
    b1.node('L-A', 'link', 1, 10, 'Enlace A → parte 2')
    for a, b_ in [('EI-01', 'AS-01'), ('AS-01', 'AS-02'), ('AS-02', 'AS-03'), ('AS-03', 'AS-04'), ('AS-04', 'G-01'),
                  ('AS-05', 'AS-06'), ('AS-06', 'AS-08'), ('AS-08', 'L-A'), ('EP-01', 'AS-07'), ('AS-07', 'EP-02')]:
        b1.edge(a, b_)
    b1.edge('G-01', 'EF-01', 'No')
    b1.edge('G-01', 'AS-05', 'Sí', side='left')
    b1.edge('AS-06', 'EP-01', 'MF-01 convocatoria', kind='msg')
    b1.edge('AS-07', 'AS-08', 'MF-02 postulación y CV', kind='msg', side='lr')
    b1.badges = {k: v for k, v in badges.items() if k in b1.nodes}
    path1 = os.path.join(pdir(n, 'diagramas', 'draft'), f'{prefix}-parte1.png')
    b1.render(path1, 'Discontinuas: flujos de mensaje (MF-01, MF-02). AS-06 → AS-08 es secuencia: AS-08 espera las postulaciones.')
    b2 = dg.Swimlanes(f'{tag} · BPMN del proceso actual (AS-IS preliminar) — parte 2 de 2', lanes, sub, **kw)
    b2.node('L-A2', 'link', 1, 0, 'Enlace A (desde parte 1)')
    b2.node('IN', 'bnd', 1, 0.62)
    b2.group(1, 3, 1, 6, f'SP-01 {N_["SP-01"]} — subproceso de instancia múltiple paralela: una instancia por candidato')
    b2.node('SI-01', 'start', 1, 1.25, f'SI-01 {N_["SI-01"]}')
    b2.node('AS-09', 'task', 1, 2.2, t('AS-09'))
    b2.node('G-02', 'gateway', 1, 3.2, f'G-02 {N_["G-02"]}', off=-70)
    b2.node('EF-02', 'end', 1, 3.2, f'EF-02 {N_["EF-02"]}', off=85)
    b2.node('AS-10', 'task', 1, 4.2, t('AS-10'))
    b2.node('AS-11', 'task', 3, 5.2, t('AS-11'))
    b2.node('EF-04', 'end', 3, 6.1, f'EF-04 {N_["EF-04"]}', off=-90)
    b2.node('OUT', 'bnd', 1, 6.52)
    b2.node('P-MF03', 'bnd', 4, 4.2, off=-155)
    b2.node('AS-12', 'task', 1, 7.3, t('AS-12'))
    b2.node('AS-13', 'task', 2, 8.3, t('AS-13'))
    b2.node('AS-14', 'task', 1, 9.3, t('AS-14'))
    b2.node('P-MF04', 'bnd', 4, 9.3, off=-155)
    b2.node('EF-03', 'end', 1, 10.3, f'EF-03 {N_["EF-03"]}')
    for a, b_ in [('L-A2', 'IN'), ('SI-01', 'AS-09'), ('AS-09', 'G-02'), ('AS-10', 'AS-11'), ('AS-11', 'EF-04'),
                  ('OUT', 'AS-12'), ('AS-12', 'AS-13'), ('AS-13', 'AS-14'), ('AS-14', 'EF-03')]:
        b2.edge(a, b_)
    b2.edge('G-02', 'EF-02', 'No')
    b2.edge('G-02', 'AS-10', 'Sí')
    b2.edge('AS-10', 'P-MF03', 'MF-03 citación', kind='msg')
    b2.edge('AS-14', 'P-MF04', 'MF-04 resultado', kind='msg')
    b2.badges = {k: v for k, v in badges.items() if k in b2.nodes}
    path2 = os.path.join(pdir(n, 'diagramas', 'draft'), f'{prefix}-parte2.png')
    b2.render(path2, 'SP-01 termina cuando todas sus instancias terminaron; entonces sigue AS-12. MF-03 y MF-04 llegan al borde del pool Postulante.')
    return [path1, path2]


EVID_ASIS = [
    ('docs/final-report/03-procesos-negocio.md', 'AS-IS preliminar (§3.1): 8 actividades macro, responsables y problemas'),
    ('docs/final-report/02-contexto-problema.md', 'Contexto sin documentación institucional verificada; P1–P5 (§2.2)'),
    ('docs/final-report/diagram-reports/01-bpmn-as-is-report.md', 'El BPMN AS-IS original del equipo no está versionado'),
    ('docs/final-report/evidence-index.md', 'Índice de evidencia de v1.0 (entregables previos ausentes)'),
    ('docs/academico/tools/f27b/m_asis.py', 'Modelo de datos del AS-IS usado por el generador'),
]


def evidencias_asis():
    return [
        'Fuente del AS-IS: `docs/final-report/03-procesos-negocio.md` §3.1 (8 actividades macro, responsables y '
        'problemas P1–P5 asociados) — rotulado como «preliminar, pendiente de validación» desde la v1.0.',
        'Contexto y problemas: `docs/final-report/02-contexto-problema.md` §2.1–2.2 (sin documentación '
        'institucional verificada en el repositorio).',
        'Informe del BPMN AS-IS v1.0: `docs/final-report/diagram-reports/01-bpmn-as-is-report.md` (el diagrama '
        'original del equipo **no está versionado**; estado «evidencia externa pendiente»).',
        'Guía oficial: `docs/academico/00-fuentes-oficiales/guias/` (Prácticas 02 y 03) y plantillas oficiales '
        'de los Formatos 02 y 03 (SHA-256 en `docs/academico/00-fuentes-oficiales/inventory.md`).',
        'Modelo de datos del documento y generador reproducible: `docs/academico/tools/f27b/` (`m_asis.py`, `build.py`).',
    ]


@builder('f2')
def build_f2():
    flow = asis_flowchart()
    d = Doc()
    estado(d, [f'Todo el contenido de proceso de este formato es **{C.ASP}**. No describe el software '
               'implementado ni el diagrama de actividad AC-01 de la v1.1, que modela el sistema ya construido.'])
    d.h('Descripción general del proceso')
    d.instr('Describir de manera clara y breve en qué consiste el proceso analizado, indicando su propósito, '
            'contexto y alcance (inicio y fin del proceso).')
    d.kv([
        ('Nombre del proceso', C.PROCESO + ' (AS-IS preliminar sujeto a validación institucional).'),
        ('Propósito', 'Cubrir las necesidades de personal del Colegio incorporando al candidato más adecuado para '
                      'cada puesto, con una decisión final tomada por la Dirección.'),
        ('Contexto', 'El Colegio Andino de Huancayo es el caso de estudio académico. Participan el área que '
                     'necesita personal, Recursos Humanos, la Dirección, los evaluadores y los postulantes. El '
                     'repositorio no contiene documentación institucional verificada (estadísticas, herramientas, '
                     'organigrama ni procedimientos), por lo que este análisis es una reconstrucción preliminar '
                     'del equipo.'),
        ('Alcance (inicio y fin)', 'Inicio: un área identifica una necesidad de personal. Fin: se comunica el '
                                   'resultado final a los postulantes (o se descarta la necesidad no aprobada).'),
        ('Estado', f'{C.ASP}. Validación pendiente con RR. HH. / Administración del Colegio: tiempos, canales, '
                   'formatos, herramientas y responsables reales.'),
    ])
    d.h('Diagrama del proceso actual (AS-IS)')
    d.instr('Inserte el diagrama de flujo del proceso actual elaborado con la herramienta seleccionada.')
    d.p('Diagrama de flujo con símbolos básicos (inicio/fin, proceso, decisión). **Borrador de revisión** generado '
        'desde el modelo del documento; el modelado BPMN formal corresponde al Formato 03.')
    d.img(flow[0], 'Figura 1. Flujo AS-IS preliminar, parte 1 (AS-01 a AS-08).', 15.5)
    d.img(flow[1], 'Figura 2. Flujo AS-IS preliminar, parte 2 (AS-09 a AS-14).', 15.5)
    d.h('Lista de actividades del proceso')
    d.table(['N°', 'Actividad', 'Descripción', 'Origen (§3.1)'],
            [(a[0], a[1], a[2], f'Actividad macro {a[3]}' + (' — desagregación F27B' if 'desagreg' in a[6] else ''))
             for a in A.ACTIVIDADES], widths=[9, 26, 45, 20], sz=18)
    d.p('La F27B desagrega las 8 actividades macro versionadas en 14 sin añadir hechos: los pasos separados (por '
        'ejemplo, revisar y aprobar) ya estaban nombrados en la actividad macro y en sus responsables.')
    d.h('Identificación de actores')
    d.table(['N°', 'Actor', 'Tipo (Interno / Externo / Sistemas)', 'Rol en el proceso'],
            [(a[0], a[1], a[2], a[3]) for a in A.ACTORES], widths=[10, 22, 18, 50])
    d.p(A.NOTA_SISTEMAS)
    d.p(A.NOTA_SUPUESTOS)
    d.h('Relación actividades-actores')
    rows, n = [], 0
    for a in A.ACTIVIDADES:
        for actor, rol in a[4]:
            n += 1
            rows.append((str(n), f'{a[0]} {a[1]}', actor, rol))
    d.table(['N°', 'Actividad', 'Actor', 'Rol (Ejecuta / Recibe / Valida)'], rows, widths=[8, 50, 24, 18])
    d.h('Observaciones del proceso')
    d.instr('Registrar observaciones relevantes sobre el proceso actual (ineficiencias, redundancias, puntos '
            'críticos, etc.), sin proponer soluciones.')
    d.table(['ID', 'Observación (AS-IS preliminar)', 'Problema', 'Actividades'],
            [o for o in A.OBSERVACIONES], widths=[8, 60, 12, 20])
    d.h('Evidencias')
    d.bullets(evidencias_asis() + [
        'Borradores: `docs/academico/practica-02/diagramas/draft/F2-flujo-as-is-parte1.png` y `…parte2.png`.',
        'No se adjuntan capturas institucionales porque no existen en el repositorio. No hay firmas ni '
        'validación de RR. HH.: esa validación es la condición para retirar el rótulo «preliminar».',
    ])
    emit(2, 'F2_Analisis_del_Proceso_Colegio_Andino', 'Formato_02_Analisis_del_proceso.docx', 'proceso', d,
         'Formato 02 — Análisis del proceso (AS-IS preliminar)')
    write_evidence(2, 'Formato 02', EVID_ASIS + [
        ('docs/academico/practica-02/diagramas/draft/F2-flujo-as-is-parte1.png', 'Borrador del flujo AS-IS, parte 1'),
        ('docs/academico/practica-02/diagramas/draft/F2-flujo-as-is-parte2.png', 'Borrador del flujo AS-IS, parte 2'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_02.docx', 'Guía oficial de la Práctica 02'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_02_Analisis_del_proceso.docx',
         'Plantilla oficial del Formato 02 (solo lectura)'),
    ])


@builder('f3')
def build_f3():
    bp = asis_bpmn()
    d = Doc()
    estado(d, ['Este BPMN es un **BPMN AS-IS preliminar derivado del análisis del equipo**. No está validado por '
               'la institución. Su modelo formal es el diagrama «F3 - BPMN AS-IS» de PowerDesigner (F29, con el hotfix '
               'F29B): formalizarlo no cambia su condición de preliminar.'])
    d.h('Descripción general del proceso')
    d.instr('Describir brevemente el proceso que será representado en el diagrama BPM, indicando su propósito, '
            'alcance (inicio y fin) y contexto.')
    d.box([f'**Proceso:** {C.PROCESO} en el {C.INSTITUCION}.',
           '**Propósito:** cubrir necesidades de personal con una decisión final de la Dirección.',
           '**Alcance:** desde que un área identifica una necesidad de personal (EI-01) hasta que se comunica el '
           'resultado a los postulantes (EF-03). Caminos alternativos: necesidad no aprobada (EF-01) y, para cada '
           'candidato dentro de SP-01, candidato no preseleccionado (EF-02).',
           '**Contexto:** representa las 14 actividades del Formato 02 (AS-01 a AS-14). Es un modelo preliminar, sin '
           'canales, herramientas ni tiempos reales verificados.'])
    d.h('Diagrama BPM del proceso actual (AS-IS)')
    d.instr('Inserte el diagrama BPM elaborado utilizando notación BPMN.')
    exp = pd('exports', 'F3_BPMN_ASIS.png')
    d.p('Diagrama formal modelado en **PowerDesigner 16.6** (Fase 29): diagrama «F3 - BPMN AS-IS» del modelo '
        '`F29_BPM_Academico.bpm`, paquete F3. La figura 1 es la exportación completa; las figuras 2 y 3 amplían sus dos '
        'mitades para leerlas mejor y no añaden contenido.')
    d.wide_img(exp, 'Figura 1. BPMN AS-IS preliminar: exportación formal de PowerDesigner (F29), diagrama «F3 - BPMN '
                    'AS-IS» (`F3_BPMN_ASIS.png`).')
    d.wide_img(exp, 'Figura 2. Ampliación de la figura 1 (franja del 0 % al 55 % del ancho): EI-01 a AS-08 y pool '
                    'Postulante. Recorte sin retoque de la exportación formal.', crop=(0.0, 0.55))
    d.wide_img(exp, 'Figura 3. Ampliación de la figura 1 (franja del 45 % al 100 % del ancho): SP-01, AS-12 a AS-14 y '
                    'EF-03. Recorte sin retoque de la exportación formal.', crop=(0.45, 1.0))
    d.p('SP-01 es un subproceso expandido de instancia múltiple paralela (marcador |||) con SI-01, AS-09, G-02, AS-10, '
        'AS-11, EF-02 y EF-04 dentro. PowerDesigner 16.6 no dibuja ese contenido en la vista principal del editor '
        '(limitación F29B-OBS-01): se consulta en el diagrama «SP-01 Evaluar al candidato — detalle», con los mismos '
        'objetos. La exportación, reproducible, es la evidencia formal.')
    d.p('El borrador de revisión de la F27B–F28 (`diagramas/draft/`) queda como antecedente: ' + SUPERSEDED + '.')
    d.h('Elementos BPMN utilizados')
    d.table(['N°', 'Elemento BPMN', 'Descripción', 'Uso en el proceso'],
            [(str(i), e, ds, u) for i, (e, ds, u) in enumerate(A.ELEMENTOS_BPMN, start=1)], widths=[7, 20, 28, 45])
    d.sub('Glosario de nombres oficiales')
    d.table(['ID', 'Tipo', 'Nombre oficial'], A.GLOSARIO, widths=[12, 50, 38], sz=17)
    d.p('Cada ID tiene **un solo nombre**, que se usa igual en el formato, el borrador, el README y el pendiente de '
        'PowerDesigner.')
    d.sub('Pool del Postulante y subproceso por candidato')
    d.p(A.POOL_POSTULANTE)
    d.p(A.SUBPROCESO)
    d.sub('Flujos de mensaje (lista cerrada, unidireccional)')
    d.table(['ID', 'Origen', 'Destino', 'Elemento receptor', 'Contenido'], A.MENSAJES, widths=[9, 33, 16, 26, 16], sz=17)
    d.h('Identificación de actores (Pools / Lanes)')
    d.table(['N°', 'Actor', 'Tipo (Interno / Externo / Sistemas)', 'Lane asignado'],
            [('1', 'Área solicitante', 'Interno', 'Lane «Área solicitante» (pool del Colegio)'),
             ('2', 'Recursos Humanos', 'Interno', 'Lane «RR. HH.» (pool del Colegio)'),
             ('3', 'Dirección', 'Interno', 'Lane «Dirección» (pool del Colegio)'),
             ('4', 'Evaluadores', 'Interno (supuesto de modelado)', 'Lane «Evaluadores» (pool del Colegio)'),
             ('5', 'Postulante', 'Externo (supuesto de modelado)',
              'Pool «Postulante»: participante visible con EP-01 → AS-07 → EP-02')],
            widths=[7, 25, 23, 45])
    d.p('No hay lane de «Sistemas»: el AS-IS preliminar no identifica ninguna herramienta informática del Colegio.')
    d.h('Descripción del flujo del proceso')
    d.instr('Describir paso a paso cómo se desarrolla el proceso según el diagrama BPM.')
    d.box([f'{i}. {t}' for i, t in enumerate(A.FLUJO, start=1)])
    d.h('Validación del modelo')
    d.instr('Marque con un aspa (X) si se cumplen los enunciados. Se aplica a la especificación y al modelo formal '
            'de PowerDesigner (F29), verificado en `docs/academico/powerdesigner/F29_VALIDATION.md`.')
    d.table(['Enunciado', 'X', 'Comprobación'], [
        ('El proceso tiene evento de inicio y fin claramente definidos.', 'X',
         'Proceso: EI-01; EF-01 y EF-03. SP-01: SI-01; EF-02 y EF-04. Postulante: EP-01; EP-02.'),
        ('Todas las actividades están conectadas correctamente.', 'X',
         'AS-01 a AS-14 tienen entrada y salida de secuencia; AS-06 → AS-08 es secuencia (AS-08 es tarea de recepción); '
         'AS-07 está entre EP-01 y EP-02; el modelo formal es un solo diagrama (el borrador unía sus dos partes con '
         'el enlace A).'),
        ('Se utilizan correctamente los elementos BPMN.', 'X',
         'Secuencia solo dentro de cada pool; MF-01 a MF-04 unidireccionales entre pools; SP-01 de instancia múltiple '
         'paralela por candidato.'),
        ('Cada actividad tiene un actor asignado.', 'X', 'Cada tarea está en el lane de su actor (tabla 5).'),
        ('El flujo es coherente y entendible.', 'X', 'Coincide con las 8 actividades macro de §3.1, con el Formato 02 y '
         'con el glosario de nombres.'),
    ], widths=[45, 6, 49])
    d.p('La validación es **interna del equipo**. Falta la validación institucional del contenido del AS-IS.')
    d.h('Evidencias')
    d.bullets(evidencias_asis() + [
        'Modelo formal: `docs/academico/powerdesigner/models/F29_BPM_Academico.bpm` (paquete F3); exportaciones '
        '`F3_BPMN_ASIS.png` y `F3_BPMN_ASIS.svg` en `docs/academico/powerdesigner/exports/`; validación en '
        '`F29_VALIDATION.md` y `F29B_HOTFIX.md`.',
        'Especificación de PowerDesigner: `docs/academico/practica-03/POWERDESIGNER_PENDING.md` (FORMALIZED / DONE).',
        'Borradores: `docs/academico/practica-03/diagramas/draft/F3-bpmn-as-is-parte1.png` y `…parte2.png` '
        '(' + SUPERSEDED + ').',
    ])
    d.p('Capturas reales de PowerDesigner, tomadas con el modelo reabierto desde el disco:')
    d.img(pd('evidencias', 'capturas', 'F3_BPMN_ASIS_PowerDesigner.png'),
          'Figura 4. Captura de PowerDesigner: diagrama «F3 - BPMN AS-IS» y paquete F3 en el Object Browser.', 16)
    d.img(pd('evidencias', 'capturas', 'F3_SP-01_detalle_PowerDesigner.png'),
          'Figura 5. Captura de PowerDesigner: diagrama «SP-01 Evaluar al candidato — detalle» (contenido de SP-01; '
          'F29B-OBS-01).', 16)
    emit(3, 'F3_Diagrama_BPM_ASIS_Colegio_Andino', 'Formato_03_Diagrama_BPM.docx', 'proceso', d,
         'Formato 03 — Diagrama BPM del proceso actual (AS-IS preliminar)')
    write_evidence(3, 'Formato 03', EVID_ASIS + [
        (f'{PD}/exports/F3_BPMN_ASIS.png', 'Exportación formal PNG del diagrama «F3 - BPMN AS-IS» (figura principal)'),
        (f'{PD}/exports/F3_BPMN_ASIS.svg', 'Exportación formal SVG (nativa de PowerDesigner)'),
        (f'{PD}/models/F29_BPM_Academico.bpm', 'Modelo fuente de PowerDesigner (paquete F3)'),
        (f'{PD}/evidencias/capturas/F3_BPMN_ASIS_PowerDesigner.png', 'Captura real de PowerDesigner: vista principal'),
        (f'{PD}/evidencias/capturas/F3_SP-01_detalle_PowerDesigner.png',
         'Captura real de PowerDesigner: detalle de SP-01 (F29B-OBS-01)'),
        (f'{PD}/F29_VALIDATION.md', 'Validación de la vista (F29)'),
        (f'{PD}/F29B_HOTFIX.md', 'Hotfix de reproducibilidad (F29B) y F29B-OBS-01'),
        ('docs/academico/practica-03/diagramas/draft/F3-bpmn-as-is-parte1.png', 'Borrador BPMN AS-IS, parte 1 — ' + SUPERSEDED),
        ('docs/academico/practica-03/diagramas/draft/F3-bpmn-as-is-parte2.png', 'Borrador BPMN AS-IS, parte 2 — ' + SUPERSEDED),
        ('docs/academico/practica-02/F2_Analisis_del_Proceso_Colegio_Andino.docx', 'Formato 02 del que deriva el BPMN'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_03.docx', 'Guía oficial de la Práctica 03'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_03_Diagrama_BPM.docx',
         'Plantilla oficial del Formato 03 (solo lectura)'),
    ], note=NOTA_EVID_F29)


# --------------------------------------------------------------------------- F4 (problemas)
import m_problems as PR  # noqa: E402
import m_tobe as T  # noqa: E402

TB = {t[0]: t for t in T.ACTIVIDADES + T.FUTURAS}


def md_table(headers, rows):
    esc = lambda x: str(x).replace('|', '\\|').replace('\n', '<br>')
    out = ['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)]
    out += ['| ' + ' | '.join(esc(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def write_text(path, text):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text.rstrip() + '\n')


@builder('f4')
def build_f4():
    badges = {}
    for p in PR.PROBLEMAS:
        for a in p['actividades']:
            badges[a] = (badges.get(a, '') + ' ' + p['id']).strip()
    ann = asis_bpmn(4, 'F4-bpmn-as-is-problemas', badges, 'F4')
    d = Doc()
    estado(d, [f'Los problemas son **{C.ASP}**. La prioridad es una **{PR.PRIORIZACION}** y las causas son hipótesis '
               'del equipo; ninguna está validada por la institución.'])
    d.h('Descripción general del proceso')
    d.instr('Describir de manera breve el proceso analizado (AS-IS), indicando su propósito, alcance (inicio y fin) '
            'y contexto organizacional.')
    d.box(['**Proceso analizado:** reclutamiento, evaluación y selección de personal (AS-IS preliminar de los Formatos '
           '02 y 03).',
           '**Propósito:** cubrir necesidades de personal con una decisión final de la Dirección.',
           '**Alcance:** desde que un área identifica una necesidad (EI-01) hasta que se comunica el resultado (EF-03).',
           '**Contexto organizacional:** Colegio Andino de Huancayo, caso de estudio académico. Intervienen el área '
           'solicitante, RR. HH., la Dirección, los evaluadores y los postulantes. No hay documentación institucional '
           'verificada.'])
    d.h('Listado de problemas identificados')
    d.table(['N°', 'Actividad del proceso', 'Problema identificado', 'Tipo de problema', 'Descripción del problema',
             'Impacto', 'Prioridad (Alta/Media/Baja)'],
            [(p['id'], ', '.join(p['actividades']), p['nombre'],
              p['tipo'] + (' (sec.: ' + ', '.join(p['tipos_sec']) + ')' if p['tipos_sec'] else ''),
              p['descripcion'], p['impacto'], f"{p['prioridad']}\n({PR.PRIORIZACION})")
             for p in PR.PROBLEMAS], widths=[6, 12, 12, 13, 22, 22, 13], sz=16)
    d.sub('Justificación de la prioridad y estado de la evidencia')
    d.table(['N°', 'Prioridad', 'Justificación (analítica)', 'Estado de la evidencia'],
            [(p['id'], p['prioridad'], p['justif'], PR.ESTADO_EVIDENCIA.format(v=p['validacion']))
             for p in PR.PROBLEMAS], widths=[7, 10, 43, 40], sz=16)
    d.h('Clasificación de problemas')
    d.instr('Clasificar los problemas según su naturaleza.')
    for k, v in PR.CLASIFICACION.items():
        d.sub(k)
        d.box([v])
    d.h('Análisis de causas')
    d.table(['N°', 'Problema identificado', 'Causa principal', 'Descripción de la causa'],
            [(p['id'], p['nombre'], p['causa'], p['causa_desc']) for p in PR.PROBLEMAS], widths=[7, 18, 25, 50], sz=17)
    d.p('Las causas son **hipótesis del equipo** derivadas del análisis. Se confirmarán o corregirán en la validación '
        'institucional.')
    d.h('Relación con el diagrama BPM')
    d.instr('Describir en qué parte del diagrama BPM se encuentra cada problema identificado.')
    d.table(['N°', 'Problema', 'Ubicación en el BPMN AS-IS (Formato 03)', 'Actividades'],
            [(p['id'], p['nombre'], p['bpmn'], ', '.join(p['actividades'])) for p in PR.PROBLEMAS],
            widths=[7, 18, 55, 20], sz=17)
    d.h('Conclusiones del análisis')
    d.box(PR.CONCLUSION)
    d.h('Evidencias')
    d.instr('Adjuntar capturas del diagrama BPM donde se evidencien los problemas identificados.')
    d.img(ann[0], 'Figura 1. BPMN AS-IS preliminar con la ubicación de los problemas (parte 1). Borrador.', 16)
    d.img(ann[1], 'Figura 2. BPMN AS-IS preliminar con la ubicación de los problemas (parte 2). Borrador.', 16)
    d.bullets([
        'Problemas P1–P5: `docs/final-report/02-contexto-problema.md` §2.2–2.3 y tabla 3.2 del F9 v1.0 '
        '(`docs/academico/phase-24/`).',
        'Matriz consolidada con todas las columnas: `docs/academico/practica-04/matriz-problemas.md`.',
        'El documento original de identificación de problemas del equipo **no está versionado** '
        '(`docs/final-report/evidence-index.md`).',
    ])
    emit(4, 'F4_Problemas_del_Proceso_Colegio_Andino', 'Formato_04_Identificacion_de_problemas.docx', 'proceso', d,
         'Formato 04 — Identificación de problemas del proceso')
    rows = [(p['id'], ', '.join(p['actividades']), p['nombre'],
             p['tipo'] + (' / ' + ', '.join(p['tipos_sec']) if p['tipos_sec'] else ''), p['descripcion'], p['impacto'],
             f"{p['prioridad']} ({PR.PRIORIZACION})", p['causa'], p['causa_desc'], p['bpmn'],
             PR.ESTADO_EVIDENCIA.format(v=p['validacion'])) for p in PR.PROBLEMAS]
    write_text(os.path.join(pdir(4), 'matriz-problemas.md'),
               '# Matriz consolidada de problemas (F4)\n\nGenerada desde `docs/academico/tools/f27b/m_problems.py`, '
               'el mismo modelo del Formato 04. Todo es **AS-IS preliminar**: prioridad analítica del equipo, causas '
               'hipotéticas y validación institucional pendiente.\n\n'
               + md_table(['ID', 'Actividad afectada', 'Problema', 'Tipo', 'Descripción', 'Impacto', 'Prioridad',
                           'Causa principal', 'Descripción de la causa', 'Ubicación en AS-IS/BPMN',
                           'Estado de evidencia'], rows))
    write_evidence(4, 'Formato 04', EVID_ASIS[:4] + [
        ('docs/academico/tools/f27b/m_problems.py', 'Modelo de datos de P1–P5 usado por el generador'),
        ('docs/academico/phase-24/F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx',
         'F9 v1.0 del equipo: tabla 3.2 «Problemas oficiales» con su impacto'),
        ('docs/academico/practica-04/diagramas/draft/F4-bpmn-as-is-problemas-parte1.png', 'BPMN anotado con P1–P5, parte 1'),
        ('docs/academico/practica-04/diagramas/draft/F4-bpmn-as-is-problemas-parte2.png', 'BPMN anotado con P1–P5, parte 2'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_04.docx', 'Guía oficial de la Práctica 04'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_04_Identificacion_de_problemas.docx',
         'Plantilla oficial del Formato 04 (solo lectura)'),
    ])


# --------------------------------------------------------------------------- F5 (TO-BE)
TOBE_LANES = [
    ('Organización cliente (Colegio) con la plataforma — TO-BE propuesto', 'Área solicitante'),
    ('Organización cliente (Colegio) con la plataforma — TO-BE propuesto', 'RR. HH.'),
    ('Organización cliente (Colegio) con la plataforma — TO-BE propuesto', 'Aprobador / Dirección'),
    ('Organización cliente (Colegio) con la plataforma — TO-BE propuesto', 'Evaluador'),
    ('Organización cliente (Colegio) con la plataforma — TO-BE propuesto', 'Plataforma SaaS (sistema)'),
    ('Postulante (externo)', 'Postulante'),
]


def tobe_bpmn():
    """BPMN TO-BE (especificación F27D): nivel vacante (partes 1 y 3) y SP-P por postulación (partes 2a y 2b)."""
    kw = dict(CW=292, RH=118, TW=240, TH=92, FS=18)
    sub = 'TO-BE propuesto por el equipo, soportado por la plataforma v1.1. Verde: tareas del sistema. Gris: propuesta futura.'
    lab = lambda i: f'{i}\n{TB[i][2]}'
    sysl = lambda i: 'system' if TB[i][4] == 'Sistema' else 'normal'
    E = {e[0]: e[2] for e in T.EVENTOS}
    G = {g[0]: g[3] for g in T.COMPUERTAS}
    out = os.path.join(pdir(5, 'diagramas', 'draft'))
    paths = []
    # Parte 1 — nivel vacante: A + B hasta SP-P
    b = dg.Swimlanes('F5 · BPMN TO-BE — parte 1: nivel vacante (requerimiento y convocatoria)', TOBE_LANES, sub, **kw)
    b.node('EI', 'start', 0, 0, E['EI'])
    for tid, lane, row in [('TB-01', 0, 1), ('TB-02', 0, 2), ('TB-03', 1, 3), ('TB-04', 0, 4.9), ('TB-05', 2, 5),
                           ('TB-06', 4, 6), ('TB-07', 1, 7), ('TB-08', 1, 8), ('TB-09', 4, 9), ('TB-10', 1, 11)]:
        b.node(tid, 'task', lane, row, lab(tid), style=sysl(tid))
    b.node('GA1', 'gateway', 1, 4, f'GA1 {G["GA1"]}', off=-70)
    b.node('GA2', 'gateway', 2, 6, f'GA2 {G["GA2"]}', off=-70)
    b.node('EFA', 'end', 4, 7, f'EFA {E["EFA"]}')
    b.node('GB1', 'gateway', 4, 10, f'GB1 {G["GB1"]}', off=-70)
    b.node('P-MT01', 'bnd', 5, 11, off=-146)
    b.node('SP-P', 'task', 1, 12.3, 'SP-P Gestionar la postulación\n(instancia múltiple |||, ver partes 2a y 2b)')
    b.node('LB', 'link', 1, 13.5, 'Enlace B → parte 3 (cuando terminaron todas las instancias)')
    for a_, c_ in [('EI', 'TB-01'), ('TB-01', 'TB-02'), ('TB-02', 'TB-03'), ('TB-03', 'GA1'), ('TB-05', 'GA2'),
                   ('TB-06', 'EFA'), ('TB-07', 'TB-08'), ('TB-08', 'TB-09'), ('TB-09', 'GB1'), ('TB-10', 'SP-P'),
                   ('SP-P', 'LB')]:
        b.edge(a_, c_)
    b.edge('GA1', 'TB-04', 'Observado', side='left')
    b.edge('TB-04', 'TB-02', 'corrige y reenvía', side='gutter')
    b.edge('GA1', 'TB-05', 'Validado', side='right')
    b.edge('GA2', 'TB-06', 'No (motivo)')
    b.edge('GA2', 'TB-07', 'Sí', side='left')
    b.edge('GB1', 'TB-08', 'No', side='gutter', lpos='vr')
    b.edge('GB1', 'TB-10', 'Sí', side='left')
    b.edge('TB-10', 'P-MT01', 'MT-01 vacante publicada (→ EP-01)', kind='msg')
    paths.append(os.path.join(out, 'F5-bpmn-to-be-parte1.png'))
    b.render(paths[-1], 'Nivel vacante. SP-P se ejecuta una vez por postulación registrada (MT-02) y se detalla en las partes 2a y 2b.')
    # Parte 2a — SP-P (1 de 2) y pool Postulante
    b = dg.Swimlanes('F5 · BPMN TO-BE — parte 2a: SP-P «Gestionar la postulación» (nivel postulación)', TOBE_LANES, sub, **kw)
    b.node('EP-01', 'start', 5, 0, f'EP-01 {E["EP-01"]}')
    for tid, row in [('TB-11', 1), ('TB-12', 2), ('TB-13', 3)]:
        b.node(tid, 'task', 5, row, lab(tid))
    b.node('EP-02', 'end', 5, 4.1, f'EP-02 {E["EP-02"]}')
    b.group(1, 4, 3.55, 11.2, 'SP-P Gestionar la postulación — subproceso de instancia múltiple paralela: una instancia por postulación (1 de 2)')
    b.node('SP-IN', 'bnd', 4, 3.62, off=60)
    b.node('SIP', 'start', 4, 4.3, f'SIP {E["SIP"]}')
    b.node('TB-14', 'task', 4, 5.2, lab('TB-14'), style='system')
    b.node('P-MT03', 'bnd', 5, 5.2, off=-146)
    b.node('TB-15', 'task', 1, 6.2, lab('TB-15'))
    b.node('TB-16', 'task', 1, 7.2, lab('TB-16'))
    b.node('TB-17', 'task', 4, 8.2, lab('TB-17'), style='system')
    b.node('P-MT04', 'bnd', 5, 8.2, off=-146)
    b.node('GD1', 'gateway', 1, 9.1, f'GD1 {G["GD1"]}', off=-70)
    b.node('EFP-01', 'end', 1, 9.1, f'EFP-01 {E["EFP-01"]}', off=85)
    b.node('GM1', 'gateway', 1, 10.3, 'GM1 unión', off=-70)
    b.node('LD2', 'link', 1, 10.3, 'Enlace D (desde GD3 «Sí»)', off=95)
    b.node('LC', 'link', 1, 11.1, 'Enlace C → parte 2b', off=-70)
    for a_, c_ in [('EP-01', 'TB-11'), ('TB-11', 'TB-12'), ('TB-12', 'TB-13'), ('TB-13', 'EP-02'), ('SIP', 'TB-14'),
                   ('TB-14', 'TB-15'), ('TB-15', 'TB-16'), ('TB-16', 'TB-17'), ('TB-17', 'GD1'), ('GM1', 'LC')]:
        b.edge(a_, c_)
    b.edge('TB-13', 'SP-IN', 'MT-02 postulación', kind='msg', side='lr')
    b.edge('TB-14', 'P-MT03', 'MT-03', kind='msg')
    b.edge('TB-17', 'P-MT04', 'MT-04', kind='msg')
    b.edge('GD1', 'EFP-01', 'No')
    b.edge('GD1', 'GM1', 'Sí')
    b.edge('LD2', 'GM1', '')
    paths.append(os.path.join(out, 'F5-bpmn-to-be-parte2a.png'))
    b.render(paths[-1], 'GM1 también recibe el retorno «¿Otra sesión? Sí» de la parte 2b. MT-03 y MT-04 llegan al borde del pool Postulante.')
    # Parte 2b — SP-P (2 de 2)
    b = dg.Swimlanes('F5 · BPMN TO-BE — parte 2b: SP-P «Gestionar la postulación» (continuación)', TOBE_LANES, sub, **kw)
    b.group(1, 4, 0.55, 12.2, 'SP-P Gestionar la postulación — subproceso de instancia múltiple paralela (2 de 2)')
    b.node('LC2', 'link', 1, 1.2, 'Enlace C (desde GM1, parte 2a)', off=-70)
    b.node('GD2', 'gateway', 1, 2.1, f'GD2 {G["GD2"]}', off=-70)
    b.node('TB-18', 'task', 1, 3.1, lab('TB-18'))
    b.node('TB-20', 'task', 1, 4.1, lab('TB-20'))
    b.node('GM2', 'gateway', 4, 5.0, 'GM2 unión', off=-70)
    b.node('TB-19', 'task', 4, 6.0, lab('TB-19'), style='system')
    b.node('P-MT05', 'bnd', 5, 6.0, off=-146)
    b.node('TB-21', 'task', 3, 7.0, lab('TB-21'))
    b.node('TB-22', 'task', 4, 8.0, lab('TB-22'), style='system')
    b.node('GV', 'gateway', 4, 8.9, f'GV {G["GV"]}', off=-70)
    b.node('GD3', 'gateway', 1, 9.7, f'GD3 {G["GD3"]}', off=-70)
    b.node('LD', 'link', 1, 9.7, 'Enlace D → GM1 (parte 2a)', off=95)
    b.node('TB-23', 'task', 1, 10.7, lab('TB-23'))
    b.node('GF', 'gateway', 1, 11.6, f'GF {G["GF"]}', off=-70)
    b.node('EFP-03', 'end', 1, 11.6, f'EFP-03 {E["EFP-03"]} (MT-07)', off=85)
    b.node('EFP-02', 'end', 3, 11.6, f'EFP-02 {E["EFP-02"]} (MT-06)', off=-60)
    for a_, c_ in [('LC2', 'GD2'), ('GM2', 'TB-19'), ('TB-19', 'TB-21'), ('TB-21', 'TB-22'), ('TB-22', 'GV'),
                   ('TB-23', 'GF')]:
        b.edge(a_, c_)
    b.edge('GD2', 'TB-18', 'Evaluación')
    b.edge('GD2', 'TB-20', 'Entrevista', side='lgutter', lpos='vl')
    b.edge('TB-18', 'GM2', '', side='right')
    b.edge('TB-20', 'GM2', '', side='right')
    b.edge('TB-19', 'P-MT05', 'MT-05 convocatoria', kind='msg')
    b.edge('GV', 'TB-21', 'No (rechazo)', side='gutter', lpos='vr')
    b.edge('GV', 'GD3', 'Sí')
    b.edge('GD3', 'TB-23', 'No')
    b.edge('GD3', 'LD', 'Sí')
    b.edge('GF', 'EFP-03', 'No')
    b.edge('GF', 'EFP-02', 'Sí')
    paths.append(os.path.join(out, 'F5-bpmn-to-be-parte2b.png'))
    b.render(paths[-1], 'GV «No»: el sistema rechaza los puntajes y el evaluador corrige y reenvía. EFP-02 y EFP-03 son fines de mensaje (aviso de etapa, RF-15).')
    # Parte 3 — nivel vacante: selección y cierre
    b = dg.Swimlanes('F5 · BPMN TO-BE — parte 3: nivel vacante (selección y cierre)', TOBE_LANES, sub, **kw)
    b.node('LB2', 'link', 1, 0, 'Enlace B (SP-P completado)')
    for tid, lane, row in [('TB-24', 4, 1), ('TB-25', 4, 2), ('TB-26', 2, 3), ('TB-27', 1, 4), ('TB-28', 1, 5),
                           ('TB-29', 4, 6)]:
        b.node(tid, 'task', lane, row, lab(tid), style=sysl(tid))
    b.node('P-MT08', 'bnd', 5, 6, off=-146)
    b.node('EFE', 'end', 4, 7, f'EFE {E["EFE"]}')
    b.group(3, 4, 8.45, 9.55, 'Transversal (no es un paso de la secuencia): se ejecuta en cada acción crítica', style='transversal')
    b.node('TB-30', 'task', 4, 9.1, lab('TB-30'), style='system')
    b.group(0, 1, 8.45, 9.55, 'Propuesta futura (A-30) — desconectada del flujo', style='future')
    b.node('TB-F1', 'task', 0, 9.1, 'TB-F1 Cerrar la convocatoria sin selección\nPROPUESTA FUTURA, no implementada', style='future', off=146)
    for a_, c_ in [('LB2', 'TB-24'), ('TB-24', 'TB-25'), ('TB-25', 'TB-26'), ('TB-26', 'TB-27'), ('TB-27', 'TB-28'),
                   ('TB-28', 'TB-29'), ('TB-29', 'EFE')]:
        b.edge(a_, c_)
    b.edge('TB-29', 'P-MT08', 'MT-08 resultado', kind='msg')
    paths.append(os.path.join(out, 'F5-bpmn-to-be-parte3.png'))
    b.render(paths[-1], 'TB-26 es la decisión HUMANA (RF-23): el ranking no elige. TB-F1 no tiene flujo de entrada ni condición del sistema.')
    return paths


def antecedente_tobe():
    """Copia a evidencias la imagen del TO-BE original del equipo (anexo A del F9 v1.0), sin modificarla."""
    import zipfile
    import re
    src = os.path.join(ACAD, 'phase-24', 'F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx')
    z = zipfile.ZipFile(src)
    doc = z.read('word/document.xml').decode('utf-8')
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read('word/_rels/document.xml.rels').decode()))
    ids = [rels[i] for i in re.findall(r'r:embed="(rId\d+)"', doc)]
    anexo_a = ids[1]  # orden: logotipo, anexo A (TO-BE), anexo B (CU), anexo C (arquitectura)
    out = os.path.join(pdir(5, 'evidencias'), 'antecedente-to-be-f9-v1.0-anexo-A.png')
    with open(out, 'wb') as f:
        f.write(z.read('word/' + anexo_a))
    return out


@builder('f5')
def build_f5():
    bp = tobe_bpmn()
    ante = antecedente_tobe()
    d = Doc()
    estado(d, [f'El proceso de este formato es **{C.TBP}**: está soportado por el **{C.SI}** v1.1, salvo TB-F1 '
               '(propuesta futura no implementada). RF-29 (experimental) no forma parte del TO-BE base. Su modelo formal '
               'es el diagrama «F5 - BPMN TO-BE» de PowerDesigner (F29, con el hotfix F29B).'])
    d.h('Descripción general del proceso')
    d.instr('Describir de manera clara el proceso mejorado.')
    d.sub('Objetivo del proceso.')
    d.box(['Gestionar el reclutamiento, la evaluación y la selección de personal de forma centralizada, trazable y '
           'multiempresa: el sistema calcula, ordena y compara, y la decisión final la toma y justifica una persona '
           'autorizada (Aprobador / Dirección).'])
    d.sub('Alcance (inicio y fin).')
    d.box(['**Inicio:** un área identifica una necesidad de personal y registra el requerimiento (TB-01).',
           '**Fin:** la convocatoria se cierra con selección y cada postulante recibe su resultado (TB-28, TB-29 y EFE). '
           'Caminos alternativos: requerimiento rechazado (TB-06 y EFA). Para cada postulación, dentro de SP-P: '
           'descartada en la preselección (EFP-01), descartada tras la evaluación (EFP-03) o finalista (EFP-02).',
           '**Dos niveles:** el nivel vacante (A, B, E y TB-30) y el nivel postulación (SP-P, de instancia múltiple, '
           'con C y D). El flujo principal supone al menos un finalista; el caso sin finalistas no tiene camino '
           'implementado (A-30).'])
    d.sub('Principales mejoras respecto al proceso actual (AS-IS).')
    d.bullets([f'{s[1]}: {s[3]} ({s[0]}).' for s in T.SOLUCIONES])
    d.sub('Reglas del TO-BE')
    d.bullets(T.REGLAS_TOBE)
    d.h('Objetivos de mejora')
    d.instr('Detallar los objetivos que se buscan con el rediseño del proceso.')
    d.table(['ID', 'Objetivo de mejora', 'Problema (F4)'], T.OBJETIVOS_MEJORA, widths=[10, 75, 15])
    d.p('Los objetivos **no se cuantifican** (por ejemplo, «reducir X % el tiempo»): no hay una línea base medida '
        'del AS-IS. Cuantificarlos exige medir el proceso real con la institución.')
    d.h('Relación Problema-Solución')
    d.table(['N°', 'Problema identificado (F4)', 'Solución propuesta', 'Mejora aplicada'],
            [(s[0], next(p['nombre'] for p in PR.PROBLEMAS if p['id'] == s[0]), s[2], s[3]) for s in T.SOLUCIONES],
            widths=[7, 18, 55, 20], sz=17)
    d.sub('Matriz problema → solución → actividad TO-BE → RF')
    d.table(['Problema (F4)', 'Solución', 'Actividades TO-BE', 'RF asociados'],
            [(s[0], s[1], ', '.join(s[4]), ', '.join(s[5])) for s in T.SOLUCIONES], widths=[14, 12, 44, 30], sz=17)
    d.h('Diagrama BPM mejorado (TO-BE)')
    d.instr('Inserte el diagrama BPM del proceso mejorado.')
    exp = pd('exports', 'F5_BPMN_TOBE.png')
    d.p('Diagrama formal modelado en **PowerDesigner 16.6** (Fase 29): diagrama «F5 - BPMN TO-BE» del modelo '
        '`F29_BPM_Academico.bpm`, paquete F5. Por su anchura, la figura 1 muestra la exportación completa en una página '
        'horizontal y las figuras 2 a 5 amplían cuatro franjas consecutivas, que se solapan para no cortar ningún '
        'elemento. Las ampliaciones son recortes sin retoque y no añaden contenido.')
    d.wide_img(exp, 'Figura 1. BPMN TO-BE propuesto: exportación formal de PowerDesigner (F29), diagrama «F5 - BPMN '
                    'TO-BE» (`F5_BPMN_TOBE.png`), completo.')
    franjas = [((0.0, 0.28), 'nivel vacante: requerimiento, aprobación y configuración (EI a GB1, TB-01 a TB-09)'),
               ((0.24, 0.52), 'publicación (TB-10), pool Postulante (EP-01, TB-11 a TB-13, EP-02) e inicio de SP-P '
                              '(SIP, TB-14 a TB-17)'),
               ((0.48, 0.76), 'SP-P, continuación: sesiones, evaluación y entrevista (TB-18 a TB-23)'),
               ((0.72, 1.0), 'fin de SP-P y nivel vacante: ranking, decisión humana, selección y cierre (TB-24 a TB-29, '
                             'EFE), TB-30 y TB-F1')]
    for i, (crop, txt) in enumerate(franjas, start=2):
        d.wide_img(exp, f'Figura {i}. Ampliación de la figura 1 (franja del {round(crop[0] * 100)} % al '
                        f'{round(crop[1] * 100)} % del ancho): {txt}. Recorte sin retoque de la exportación formal.', crop=crop)
    d.sub('Observaciones del modelo formal (Check Model de PowerDesigner)')
    d.table(['Elemento', 'Hallazgo de PowerDesigner', 'Tratamiento'], [
        ('TB-30 Registrar la auditoría de las acciones críticas', 'Proceso sin flujos de entrada ni de salida',
         'Esperado: es **transversal** (se ejecuta en cada acción crítica) y se representa desconectado a propósito'),
        ('TB-F1 Cerrar la convocatoria sin selección', 'Proceso sin flujos de entrada ni de salida',
         'Esperado: es una **propuesta futura** (A-30), no implementada y desconectada del flujo'),
        ('MT-02 Postulación', 'Advertencia de mensaje incoherente (CheckFlowIncohMsg)',
         'Advertencia **aceptada** de la herramienta: MT-02 llega al borde de SP-P con su formato de mensaje, y '
         'PowerDesigner no permite declarar un mensaje recibido en un subproceso compuesto'),
    ], widths=[26, 28, 46], sz=16)
    d.p('Ninguno de estos hallazgos es una falla funcional del TO-BE: los tres se aceptaron en la auditoría de la F29. '
        'SP-P es un subproceso expandido de instancia múltiple paralela; PowerDesigner 16.6 no dibuja su contenido en '
        'la vista principal del editor (limitación F29B-OBS-01) y se consulta en el diagrama «SP-P Gestionar la '
        'postulación — detalle», con los mismos objetos.')
    d.p('El borrador de revisión de la F27B–F28 (`diagramas/draft/`, partes 1, 2a, 2b y 3) queda como antecedente: '
        + SUPERSEDED + '.')
    d.sub('Estructura del modelo: niveles')
    d.table(['Nivel', 'Instancias', 'Contenido'], T.NIVELES, widths=[22, 33, 45], sz=17)
    d.p(T.SP_P)
    d.sub('Eventos (nombres oficiales)')
    d.table(['ID', 'Tipo', 'Nombre oficial'], T.EVENTOS, widths=[12, 45, 43], sz=17)
    d.sub('Compuertas (incluidas las uniones explícitas)')
    d.table(['ID', 'Tipo', 'Lane', 'Nombre', 'Salidas'], T.COMPUERTAS, widths=[8, 16, 16, 24, 36], sz=16)
    d.sub('Flujos de mensaje (lista cerrada, unidireccional)')
    d.table(['ID', 'Origen', 'Destino', 'Elemento receptor', 'Contenido'], T.MENSAJES, widths=[8, 32, 13, 24, 23], sz=16)
    d.h('Descripción de actividades del proceso')
    d.table(['N°', 'Actividad', 'Descripción', 'Actor responsable', 'RF'],
            [(t[0], t[2], t[3], t[4], ', '.join(t[5]) or '—') for t in T.ACTIVIDADES + T.FUTURAS],
            widths=[8, 22, 42, 15, 13], sz=16)
    d.sub('Correcciones conceptuales respecto del TO-BE original del equipo')
    d.table(['ID', 'Tema', 'Corrección'], T.CORRECCIONES, widths=[8, 20, 72], sz=17)
    d.h('Conclusiones del rediseño')
    d.box([
        '**Qué cambia respecto del AS-IS:** el TO-BE sustituye un proceso con información dispersa, seguimiento manual, '
        'evaluaciones heterogéneas y avisos manuales por un flujo con registro único, estados e historial, criterios '
        'ponderados definidos de antemano, notificaciones automáticas y auditoría.',
        '**Qué se mantiene:** la decisión sigue siendo **humana y de la Dirección**; el sistema solo aporta un ranking y '
        'una comparación explicables como apoyo.',
        '**Qué queda fuera:** el cierre sin selección es una propuesta futura, y los indicadores de gestión (P5) no se '
        'resuelven (RF-28 es un candidato).',
        '**Qué no está demostrado:** el impacto en tiempos o costos no está medido, y la adopción en el Colegio no está '
        'validada.',
    ])
    d.h('Evidencias')
    d.instr('Adjuntar capturas del diagrama BPM mejorado.')
    d.p('Capturas reales de PowerDesigner, tomadas con el modelo reabierto desde el disco. La vista principal se capturó '
        'en dos partes por su anchura.')
    d.img(pd('evidencias', 'capturas', 'F5_BPMN_TOBE_PowerDesigner_parte1.png'),
          'Figura 6. Captura de PowerDesigner: diagrama «F5 - BPMN TO-BE», parte 1 (nivel vacante hasta el inicio de SP-P).', 16)
    d.img(pd('evidencias', 'capturas', 'F5_BPMN_TOBE_PowerDesigner_parte2.png'),
          'Figura 7. Captura de PowerDesigner: diagrama «F5 - BPMN TO-BE», parte 2 (SP-P hasta el cierre, TB-30 y TB-F1).', 16)
    d.img(pd('evidencias', 'capturas', 'F5_SP-P_detalle_PowerDesigner.png'),
          'Figura 8. Captura de PowerDesigner: diagrama «SP-P Gestionar la postulación — detalle» (contenido de SP-P; '
          'F29B-OBS-01).', 16)
    d.img(ante, 'Figura 9. Antecedente: TO-BE original del equipo (anexo A del F9 v1.0, copia sin modificar). Incluye la '
                'rama «cerrar sin selección», no implementada.', 16)
    d.bullets([
        'TO-BE escrito e implementado: `docs/final-report/03-procesos-negocio.md` §3.3–3.5 y '
        '`docs/final-report/diagram-reports/02-bpmn-to-be-report.md`.',
        'Reglas: `docs/assumptions.md` (A-05, A-13, A-16, A-23 a A-31). Verificación del flujo completo: E2E-13 y la QA de la '
        'Fase 25 (`docs/v1.1/phase-25-final-qa.md`).',
        'Comportamiento implementado de referencia (no es el TO-BE institucional): AC-01 '
        '(`docs/v1.1/powerdesigner/exports/AC-01-proceso-reclutamiento.png`).',
        'Modelo formal: `docs/academico/powerdesigner/models/F29_BPM_Academico.bpm` (paquete F5); exportaciones '
        '`F5_BPMN_TOBE.png` y `F5_BPMN_TOBE.svg`; validación en `F29_VALIDATION.md` y `F29B_HOTFIX.md`.',
        'Borradores: `docs/academico/practica-05/diagramas/draft/` (' + SUPERSEDED + ').',
    ])
    emit(5, 'F5_Modelo_BPM_TOBE_Colegio_Andino', 'Formato_05_Modelo_BPM_mejorado.docx', 'proceso', d,
         'Formato 05 — Modelo BPM mejorado (proceso TO-BE)')
    write_evidence(5, 'Formato 05', [
        ('docs/final-report/03-procesos-negocio.md', 'TO-BE propuesto (§3.3), flujo implementado y reglas (§3.3–3.5)'),
        ('docs/final-report/diagram-reports/02-bpmn-to-be-report.md', 'Informe del TO-BE: el BPMN original no está versionado'),
        ('docs/assumptions.md', 'Reglas A-05, A-13, A-16 y A-23 a A-31 (cierre solo con selección: A-30)'),
        ('docs/final-report/02-contexto-problema.md', 'Relación problema → RF (§2.3)'),
        ('docs/academico/practica-05/evidencias/antecedente-to-be-f9-v1.0-anexo-A.png',
         'TO-BE original del equipo (copia del anexo A del F9 v1.0)'),
        ('docs/academico/phase-24/F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx', 'F9 v1.0, fuente del anexo A'),
        ('docs/v1.1/powerdesigner/exports/AC-01-proceso-reclutamiento.png', 'Comportamiento implementado (referencia, no TO-BE)'),
        ('docs/academico/tools/f27b/m_tobe.py', 'Modelo de datos del TO-BE usado por el generador'),
        (f'{PD}/exports/F5_BPMN_TOBE.png', 'Exportación formal PNG del diagrama «F5 - BPMN TO-BE» (figura principal)'),
        (f'{PD}/exports/F5_BPMN_TOBE.svg', 'Exportación formal SVG (nativa de PowerDesigner)'),
        (f'{PD}/models/F29_BPM_Academico.bpm', 'Modelo fuente de PowerDesigner (paquete F5)'),
        (f'{PD}/evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte1.png', 'Captura real de PowerDesigner: vista principal, parte 1'),
        (f'{PD}/evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte2.png', 'Captura real de PowerDesigner: vista principal, parte 2'),
        (f'{PD}/evidencias/capturas/F5_SP-P_detalle_PowerDesigner.png',
         'Captura real de PowerDesigner: detalle de SP-P (F29B-OBS-01)'),
        (f'{PD}/F29_VALIDATION.md', 'Validación de la vista y hallazgos aceptados (TB-30, TB-F1, MT-02)'),
        (f'{PD}/F29B_HOTFIX.md', 'Hotfix de reproducibilidad (F29B) y F29B-OBS-01'),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte1.png', 'Borrador BPMN TO-BE, parte 1 — ' + SUPERSEDED),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte2a.png', 'Borrador BPMN TO-BE, parte 2a (SP-P) — ' + SUPERSEDED),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte2b.png', 'Borrador BPMN TO-BE, parte 2b (SP-P) — ' + SUPERSEDED),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte3.png', 'Borrador BPMN TO-BE, parte 3 — ' + SUPERSEDED),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_05.docx', 'Guía oficial de la Práctica 05'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_05_Modelo_BPM_mejorado.docx',
         'Plantilla oficial del Formato 05 (solo lectura)'),
    ], note=NOTA_EVID_F29)


# --------------------------------------------------------------------------- F6 (RF)
import m_rf as R  # noqa: E402
import m_rnf as N  # noqa: E402

RFD = {r[0]: r for r in R.RF}


def sistema_desc(d, rel_rf=True):
    d.sub('Objetivo del sistema.')
    d.box(['Gestionar de forma centralizada, trazable y multiempresa el ciclo de reclutamiento, evaluación y selección de '
           'personal: desde el requerimiento hasta el cierre de la convocatoria. Los datos de cada organización quedan '
           'aislados y la decisión final de selección se reserva a una persona autorizada (Aprobador / Dirección).'])


@builder('f6')
def build_f6():
    d = Doc()
    estado(d, [f'Los RF-01 a RF-27 describen el **{C.SI}** v1.1 (27 de 27 trazados a código y pruebas). La prioridad es '
               f'una **{R.PRIORIZACION}**. RF-28 y RF-29 están en una sección aparte y **no** forman parte de la línea base.'])
    d.h('Descripción general del sistema')
    d.instr('Describir brevemente el sistema a desarrollar.')
    sistema_desc(d)
    d.sub('Usuarios principales.')
    d.table(['Actor', 'Rol en el sistema', 'Tipo'], [(a[1], f'`{a[2]}`', a[3]) for a in C.ACTORES_SISTEMA], widths=[40, 35, 25])
    d.p('El Sistema valida, calcula, notifica y audita, pero **nunca selecciona**. No existe un rol de superadministrador.')
    d.sub('Relación con el proceso TO-BE.')
    d.box(['Cada RF soporta al menos una actividad del TO-BE del Formato 05 (TB-01 a TB-30). La tabla de la sección 5 '
           'muestra la relación completa. La actividad TB-F1 («cerrar sin selección») es una propuesta futura y no '
           'tiene RF en la línea base.'])
    d.h('Lista de requerimientos funcionales')
    d.table(['ID', 'Nombre del requerimiento', 'Descripción', 'Actor', 'Entradas', 'Salidas', 'Prioridad'],
            [(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in R.RF], widths=[7, 16, 20, 11, 18, 17, 11], sz=14)
    d.p(f'La prioridad es una {R.PRIORIZACION}: **Alta** si el RF está en el camino principal del proceso y **Media** si '
        'es una notificación derivada de otra acción. Los 27 RF son de la línea base y están implementados.')
    d.sub('Nombres canónicos, fuente y alias históricos')
    d.p('**Nombre canónico:** el del catálogo técnico de la línea base. **Fuente:** ' + R.FUENTE_CANONICA + ' **Alias '
        'histórico:** el rótulo que otro documento usó para el mismo RF (abreviatura o variante). No es otro RF ni otro nombre '
        'oficial.')
    d.table(['RF', 'Nombre canónico', 'Fuente', 'Alias histórico', 'Observación'],
            [(r[0], r[1], f'UC-{r[0].replace("-", "")} (F22)',
              ' / '.join(x for x in dict.fromkeys(R.ALIAS.get(r[0], (None, None))) if x) or '—', R.obs_nombre(r[0]))
             for r in R.RF], widths=[8, 28, 13, 22, 29], sz=15)
    d.p('Los IDs no cambian. La Fase 24 registró «seis rótulos abreviados» en el Formato 09 (observación L-02). La '
        'comparación completa contra el catálogo canónico encuentra **13** rótulos distintos en el F9: 11 abreviaturas y '
        '2 variantes (RF-19 y RF-23). En el informe v1.0 hay 8. Todos quedan resueltos aquí con su alias; el F9 publicado '
        'no se modifica.')
    d.h('Detalle de requerimientos funcionales')
    for r in R.RF:
        d.sub(f'{r[0]}: {r[1]}')
        d.kv([('Descripción', r[2]), ('Actor principal', r[3]), ('Precondiciones', r[7]),
              ('Flujo principal', '\n'.join(f'{i}. {x}' for i, x in enumerate(r[8], start=1))),
              ('Flujo alternativo', '\n'.join(r[9])), ('Postcondiciones', r[10]),
              ('Actividad TO-BE', ', '.join(r[11])), ('Evidencia de implementación', r[12])], widths=(24, 76), sz=16)
    d.h('Trazabilidad con el proceso TO-BE')
    d.table(['Actividad del proceso (TO-BE)', 'Requerimiento funcional asociado'],
            [(f'{t[0]} {t[2]}', ', '.join(t[5]) or '— (propuesta futura, sin RF)') for t in T.ACTIVIDADES + T.FUTURAS],
            widths=[70, 30], sz=16)
    d.h('Extensiones posteriores al baseline')
    d.p('Estas extensiones **no** forman parte de RF-01 a RF-27, no se mezclan con la tabla principal y su promoción es '
        'una decisión pendiente del equipo (`docs/v1.1/scope-preliminary.md`, preguntas 12 y 13).')
    d.table(['ID', 'Nombre', 'Estado', 'Descripción', 'Fuente'], R.EXTENSIONES, widths=[8, 17, 17, 38, 20], sz=16)
    emit(6, 'F6_Requerimientos_Funcionales_Colegio_Andino', 'Formato_06_Requerimientos_funcionales.docx', 'clave', d,
         'Formato 06 — Requerimientos funcionales')
    write_evidence(6, 'Formato 06', [
        ('docs/final-report/04-requerimientos.md', 'RF-01 a RF-27 implementados (§4.2), actores (§4.1) y reglas críticas (§4.5)'),
        ('docs/final-report/traceability-master.md', 'Trazabilidad RF → backend, frontend, PHPUnit y Cypress (27/27)'),
        ('docs/rf-implementation-matrix.md', 'RF → archivos de implementación'),
        ('docs/assumptions.md', 'Reglas A-01 a A-36 citadas en las fichas'),
        ('docs/v1.1/uml/use-cases.md', 'Nombres canónicos de RF-01 a RF-29 (UC-RF01 a UC-RF29)'),
        ('docs/v1.1/phase-25-final-qa.md', 'QA global: PHPUnit 411 superadas, Cypress 85/85'),
        ('docs/v1.1/scope-preliminary.md', 'RF-28 y RF-29 como candidatos (decisión 11)'),
        ('app/Http/Requests', 'Campos y validaciones reales de las entradas'),
        ('docs/academico/tools/f27b/m_rf.py', 'Modelo de datos de las fichas usado por el generador'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_06.docx', 'Guía oficial de la Práctica 06'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_06_Requerimientos_funcionales.docx',
         'Plantilla oficial del Formato 06 (solo lectura)'),
    ])


# --------------------------------------------------------------------------- F7 (RNF)
@builder('f7')
def build_f7():
    d = Doc()
    estado(d, [f'La prioridad es una **{N.PRIORIZACION}**. Cada RNF declara su **estado real de validación**: '
               'verificado, evidencia parcial, no verificado o propuesto. Las pruebas exploratorias no se presentan como '
               'SLA, y RNF-C no se presenta como requisito implementado.'])
    d.h('Descripción general del sistema')
    d.instr('Describir brevemente el sistema a desarrollar.')
    sistema_desc(d)
    d.sub('Funcionalidades principales.')
    d.bullets(['Requerimientos de personal con validación y aprobación (RF-01 a RF-04).',
               'Vacantes con perfil, criterios ponderados, validación y publicación (RF-05 a RF-07).',
               'Cuenta, perfil, CV y postulación del postulante (RF-08 a RF-11).',
               'Revisión, etapas y notificaciones (RF-12 a RF-15).',
               'Evaluaciones y entrevistas con convocatoria y registro de resultados (RF-16 a RF-20).',
               'Ranking y comparación explicables, decisión humana, selección, cierre y resultado (RF-21 a RF-26).',
               'Auditoría de solo inserción (RF-27).'])
    d.sub('Relación con los requerimientos funcionales.')
    d.box(['Los RNF son **transversales**: se aplican a los 27 RF del Formato 06 y no crean módulos propios. La matriz de '
           'trazabilidad F2–F9 indica los RNF más relevantes para cada RF.'])
    d.h('Lista de requerimientos no funcionales')
    d.table(['ID', 'Categoría', 'Nombre del requerimiento', 'Descripción', 'Métrica / Criterio', 'Prioridad'],
            [(x[0], x[1], x[2], x[3], x[4], x[5]) for x in N.RNF], widths=[8, 14, 15, 21, 30, 12], sz=15)
    d.h('Detalle de requerimientos no funcionales')
    for x in N.RNF:
        d.sub(f'{x[0]}: {x[2]}')
        d.kv([('Categoría', x[1]), ('Descripción', x[3]), ('Métrica o criterio de aceptación', x[4]),
              ('Justificación', x[6]), ('Método de verificación', x[7]), ('Estado real de validación', f'**{x[8]}**'),
              ('Evidencia y límites', x[9])], widths=(26, 74), sz=16)
    d.h('Clasificación por atributos de calidad')
    d.table(['Categoría', 'Requerimientos asociados'], N.CLASIFICACION, widths=[35, 65])
    d.sub('Matriz de equivalencia: RNF académico ↔ RNF técnico ↔ evidencia ↔ estado')
    d.table(['RNF académico (F9)', 'RNF técnico (informe v1.0, cap. 4 §4.3)', 'Relación', 'Estado'],
            N.EQUIVALENCIA, widths=[28, 44, 12, 16], sz=16)
    d.p('La relación **no es 1:1**. Tres RNF académicos (RNF-06, RNF-07 y RNF-08) no tienen equivalente técnico, y dos '
        'RNF técnicos no tienen equivalente académico. Unificar los catálogos es una decisión del equipo (F24 L-01).')
    d.table(['RNF técnico sin equivalente académico', 'Requerimiento', 'Estado'], N.TECNICOS_SIN_EQUIVALENTE,
            widths=[22, 48, 30], sz=16)
    d.sub('Candidatos fuera de la línea base')
    d.table(['ID', 'Candidato', 'Estado', 'Observación'], N.CANDIDATOS, widths=[8, 32, 13, 47], sz=16)
    d.p('RNF-A a RNF-D son **propuestas separadas** de los 10 RNF académicos: no se cuentan en la línea base ni cambian su '
        'estado de verificación.')
    emit(7, 'F7_Requerimientos_No_Funcionales_Colegio_Andino', 'Formato_07_Requerimientos_no_funcionales.docx', 'modulo',
         d, 'Formato 07 — Requerimientos no funcionales')
    write_evidence(7, 'Formato 07', [
        ('docs/final-report/04-requerimientos.md', 'Catálogo técnico RNF-01 a RNF-11 (§4.3): sin SLA ni pruebas de carga'),
        ('docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx',
         'Catálogo académico RNF-01 a RNF-10 (F9 v1.1)'),
        ('docs/v1.1/phase-25-final-qa.md', 'QA global: suites, seguridad, multitenencia y rendimiento exploratorio (§21)'),
        ('docs/v1.1/phase-21-visual-qa.md', 'QA visual y de accesibilidad (usabilidad, evidencia parcial)'),
        ('docs/manual-smoke-test.md', 'Recorrido manual de usabilidad (v1.0)'),
        ('docs/defects.md', 'DEF-07, DEF-08 y DEF-09'),
        ('docs/docker.md', 'Portabilidad (RNF técnico sin equivalente académico)'),
        ('docs/v1.1/scope-preliminary.md', 'Candidatos RNF-A, RNF-B y RNF-C (propuestas)'),
        ('docs/academico/tools/f27b/m_rnf.py', 'Modelo de datos de los RNF usado por el generador'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_07.docx', 'Guía oficial de la Práctica 07'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_07_Requerimientos_no_funcionales.docx',
         'Plantilla oficial del Formato 07 (solo lectura)'),
    ])


# --------------------------------------------------------------------------- F8 (casos de uso)
import m_cu as U  # noqa: E402

CUD = {c[0]: c for c in U.CU}
ACTN = {a[0]: a[1] for a in U.ACTORES}


def f9_image(index, out_name, n):
    """Copia sin modificar una imagen del F9 v1.0 (orden: logotipo, anexo A, anexo B, anexo C)."""
    import zipfile
    import re
    src = os.path.join(ACAD, 'phase-24', 'F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx')
    z = zipfile.ZipFile(src)
    doc = z.read('word/document.xml').decode('utf-8')
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', z.read('word/_rels/document.xml.rels').decode()))
    ids = [rels[i] for i in re.findall(r'r:embed="(rId\d+)"', doc)]
    out = os.path.join(pdir(n, 'evidencias'), out_name)
    with open(out, 'wb') as f:
        f.write(z.read('word/' + ids[index]))
    return out


@builder('f8')
def build_f8():
    left = [(a, ACTN[a]) for a in ('ACT-01', 'ACT-04', 'ACT-05')]
    right = [(a, ACTN[a]) for a in ('ACT-02', 'ACT-03')]
    links = [(a, c[0]) for c in U.CU for a in c[3]]
    diag = os.path.join(pdir(8, 'diagramas', 'draft'), 'F8-casos-de-uso-academico.png')
    dg.use_case_diagram(diag, 'F8 · Diagrama de casos de uso — vista académica (CU-01 a CU-20)',
                        'Cinco actores y veinte casos de la línea base RF-01 a RF-27. Nombres de CU asignados en la F27B (O-F8-01).',
                        left, right, [(c[0], c[1], c[8], c[9]) for c in U.CU], links, U.INCLUDES,
                        'CU-16 es un caso incluido, sin actor directo. RF-28 y RF-29 no forman parte de esta vista.')
    ante = f9_image(2, 'antecedente-cu-f9-v1.0-anexo-B.png', 8)
    uc01 = os.path.join(ROOT, 'docs', 'v1.1', 'powerdesigner', 'exports', 'UC-01-casos-de-uso.png')
    d = Doc()
    estado(d, [f'Los casos de uso representan el **{C.SI}** de la línea base RF-01 a RF-27. El diagrama académico está '
               'formalizado en PowerDesigner (F29): diagrama «F8 - Casos de Uso Academicos». La vista técnica UC-01 de '
               'PowerDesigner (F23) se conserva como referencia y no se modifica.'])
    d.h('Descripción general del sistema')
    d.instr('Describir brevemente el sistema a desarrollar.')
    sistema_desc(d)
    d.sub('Funcionalidades principales.')
    d.bullets(['Requerimientos de personal (CU-01 a CU-03).', 'Vacantes (CU-04 a CU-06).',
               'Cuenta y postulación (CU-07 a CU-09).', 'Seguimiento de postulaciones (CU-10 a CU-12).',
               'Evaluación y entrevista (CU-13 a CU-15).', 'Comparación y ranking (CU-16 y CU-17).',
               'Decisión humana, selección y cierre (CU-18 a CU-20), con auditoría.'])
    d.sub('Relación con los requerimientos funcionales.')
    d.box(['Los 20 CU cubren RF-01 a RF-26 del Formato 06, sin RF adicionales. **RF-27** (auditoría) es transversal: su '
           'registro ocurre en todas las acciones críticas y su consulta es una capacidad técnica (UC-RF27), fuera del '
           'catálogo académico (decisión D-CU-04). RF-28 y RF-29 son extensiones fuera de esta vista.'])
    d.sub('Decisión del equipo sobre los casos de uso (F27D)')
    d.table(['ID', 'Decisión'], U.DECISION, widths=[14, 86])
    d.p('**Nota técnica.** ' + U.NOTA_AUDITORIA)
    d.h('Identificación de actores')
    d.table(['ID', 'Actor', 'Descripción'], U.ACTORES, widths=[10, 22, 68])
    d.p(U.NOTA_ACTORES)
    d.h('Identificación de casos de uso')
    d.table(['ID', 'Caso de uso', 'Descripción'], [(c[0], c[1], c[2]) for c in U.CU], widths=[9, 33, 58], sz=17)
    d.h('Relación actores-casos de uso')
    rows = [(f'{a[0]} {a[1]}', ', '.join(c[0] for c in U.CU if a[0] in c[3])) for a in U.ACTORES]
    rows.append(('— (caso incluido)', 'CU-16, incluido por CU-05, CU-15 y CU-17'))
    d.table(['Actor', 'Caso de uso'], rows, widths=[35, 65])
    d.h('Diagrama de casos de uso')
    d.instr('Insertar aquí el diagrama elaborado con herramienta UML.')
    exp = pd('exports', 'F8_Casos_de_Uso_Academicos.png')
    d.p('Diagrama formal modelado en **PowerDesigner 16.6** (Fase 29): diagrama «F8 - Casos de Uso Academicos» del modelo '
        '`F29_UML_Academico.oom`, paquete F8. Cinco actores, CU-01 a CU-20 en cinco áreas funcionales y CU-16 incluido '
        'desde CU-05, CU-15 y CU-17. Las figuras 2 y 3 amplían sus dos mitades y no añaden contenido.')
    d.img(exp, 'Figura 1. Diagrama de casos de uso, vista académica (CU-01 a CU-20): exportación formal de PowerDesigner '
               '(F29), `F8_Casos_de_Uso_Academicos.png`.', 15.5)
    d.img(exp, 'Figura 2. Ampliación de la figura 1 (franja del 0 % al 55 % del ancho): actores ACT-01, ACT-04 y ACT-05 '
               'y áreas A a E. Recorte sin retoque de la exportación formal.', 15.5, crop=(0.0, 0.55))
    d.img(exp, 'Figura 3. Ampliación de la figura 1 (franja del 45 % al 100 % del ancho): áreas A a E y actores ACT-02 y '
               'ACT-03. Recorte sin retoque de la exportación formal.', 15.5, crop=(0.45, 1.0))
    d.p('PowerDesigner señala CU-16 como caso sin actor directo (Check Model): es esperado, porque CU-16 es un caso '
        'incluido. CU-21 «Consultar auditoría» sigue **DIFERIDO** y no aparece en el diagrama. El borrador de la F27B–F28 '
        '(`diagramas/draft/`) queda como antecedente: ' + SUPERSEDED + '.')
    d.img(uc01, 'Figura 4. Referencia técnica: UC-01 de PowerDesigner (F23), un caso por RF. Exportación versionada, sin cambios.', 16.5)
    d.p('No se modificó el OOM de la F23. Captura real de PowerDesigner, tomada con el modelo reabierto desde el disco:')
    d.img(pd('evidencias', 'capturas', 'F8_Casos_de_Uso_PowerDesigner.png'),
          'Figura 5. Captura de PowerDesigner: diagrama «F8 - Casos de Uso Academicos» y paquete F8 en el Object Browser.', 16)
    d.h('Relación con los requerimientos y correspondencia de vistas')
    d.table(['CU académico (F9)', 'CU agrupado (v1.0)', 'UC-RF (F22/F23)', 'Actor', 'RF', 'Alcance (F9)'],
            [(f'{c[0]} {c[1]}', c[5], c[6], ', '.join(c[3]) or '— (incluido)', ', '.join(c[4]), c[7]) for c in U.CU] +
            [(t['cu'], t['agrupado'], t['uc'], t['actor'], rf, t['inb']) for rf, t in U.TRANSVERSAL.items()],
            widths=[24, 16, 20, 13, 13, 14], sz=15)
    d.p('RF-27: ' + U.TRANSVERSAL['RF-27']['f9'] + '. RF-23 queda solo en CU-18 → UC-RF23.')
    d.sub('Los 13 CU agrupados de v1.0 (se conservan)')
    d.table(['CU (v1.0)', 'Caso de uso', 'Actor', 'RF'], U.AGRUPADOS, widths=[12, 38, 25, 25], sz=16)
    d.p('Las tres vistas se conservan: 20 CU académicos (F9), 13 CU agrupados (informe v1.0) y 29 UC-RF técnicos '
        '(F22/F23, uno por RF, con UC-RF28 candidato y UC-RF29 experimental). No se renumera ninguna.')
    d.h('Observaciones')
    d.table(['ID', 'Tema', 'Observación'], U.OBSERVACIONES, widths=[11, 20, 69], sz=16)
    d.img(ante, 'Figura 6. Antecedente superado: diagrama de CU del F9 v1.0 (anexo B, copia sin modificar). Incluye '
                'actores fuera del alcance (O-F8-06).', 15)
    emit(8, 'F8_Diagrama_Casos_de_Uso_Colegio_Andino', 'Formato_08_Diagrama_de_casos_de_uso.docx', 'modulo', d,
         'Formato 08 — Diagrama de casos de uso')
    write_evidence(8, 'Formato 08', [
        ('docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx',
         'Vista A: 20 CU académicos, actores ACT-01 a ACT-05 y bloques IN (tablas 5 y 8)'),
        ('docs/final-report/04-requerimientos.md', 'Vista B: 13 CU agrupados (§4.4)'),
        ('docs/final-report/diagram-reports/03-use-case-report.md', 'Informe de CU de v1.0 y rutas reales por CU'),
        ('docs/v1.1/uml/use-cases.md', 'Vista C: 29 UC-RF, actores, include/extend y semántica crítica'),
        ('docs/v1.1/powerdesigner/exports/UC-01-casos-de-uso.png', 'UC-01 de PowerDesigner (F23), referencia técnica'),
        ('docs/academico/practica-08/evidencias/antecedente-cu-f9-v1.0-anexo-B.png', 'Antecedente superado (anexo B del F9 v1.0)'),
        (f'{PD}/exports/F8_Casos_de_Uso_Academicos.png', 'Exportación formal PNG del diagrama académico (figura principal)'),
        (f'{PD}/exports/F8_Casos_de_Uso_Academicos.svg', 'Exportación formal SVG (nativa de PowerDesigner)'),
        (f'{PD}/models/F29_UML_Academico.oom', 'Modelo fuente de PowerDesigner (paquete F8)'),
        (f'{PD}/evidencias/capturas/F8_Casos_de_Uso_PowerDesigner.png', 'Captura real de PowerDesigner: vista principal'),
        (f'{PD}/F29_VALIDATION.md', 'Validación de la vista (F29) y hallazgo aceptado de CU-16'),
        (f'{PD}/F29B_HOTFIX.md', 'Hotfix de reproducibilidad (F29B)'),
        ('docs/academico/practica-08/diagramas/draft/F8-casos-de-uso-academico.png', 'Borrador del diagrama académico — ' + SUPERSEDED),
        ('docs/academico/tools/f27b/m_cu.py', 'Modelo de datos de los CU usado por el generador'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_08.docx', 'Guía oficial de la Práctica 08'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_08_Diagrama_de_casos_de_uso.docx',
         'Plantilla oficial del Formato 08 (solo lectura)'),
    ], note=NOTA_EVID_F29)


# --------------------------------------------------------------------------- Trazabilidad F2 → F9
@builder('trace')
def build_trace():
    import validate as V
    out_dir = os.path.join(ACAD, 'trazabilidad')
    os.makedirs(out_dir, exist_ok=True)
    rnf_rf = lambda rf: N.RNF_POR_RF.get(rf, N.RNF_POR_RF['default'])
    cu_of = lambda rfs: [c for c in U.CU if set(c[4]) & set(rfs)]
    prob_of_as = lambda ids: sorted({p['id'] for p in PR.PROBLEMAS for a in ids if a in p['actividades']})

    def cu_in(rfs):
        """CU académicos e IN del F9 para un conjunto de RF; RF-27 es transversal (H-07)."""
        cus = cu_of(rfs)
        cu_txt = [c[0] for c in cus] + [f'{rf}: {U.TRANSVERSAL[rf]["cu"]}' for rf in rfs if rf in U.TRANSVERSAL]
        ins = sorted({c[7] for c in cus} | {U.TRANSVERSAL[rf]['inb'] for rf in rfs if rf in U.TRANSVERSAL})
        return ', '.join(cu_txt) or '—', ', '.join(ins) or 'Fuera de alcance (OUT)'

    rows = []
    for t in T.ACTIVIDADES + T.FUTURAS:
        sols = [s for s in T.SOLUCIONES if t[0] in s[4]]
        cu_txt, in_txt = cu_in(t[5])
        rows.append((', '.join(t[6]) or '— (nueva)', ', '.join(prob_of_as(t[6])) or '—',
                     ', '.join(s[0] for s in sols) or '—', ', '.join(s[1] for s in sols) or '—',
                     f'{t[0]} {t[2]}', ', '.join(t[5]) or '— (propuesta futura)',
                     ', '.join(sorted({x for r in t[5] for x in rnf_rf(r)})) or '—', cu_txt, in_txt))
    as_rows = [(a[0], a[1], ', '.join(a[5]) or '—', ', '.join(t[0] for t in T.ACTIVIDADES if a[0] in t[6])) for a in A.ACTIVIDADES]
    rf_rows = []
    for r in R.RF:
        cus = cu_of([r[0]])
        if r[0] in U.TRANSVERSAL:
            tr = U.TRANSVERSAL[r[0]]
            rf_rows.append((r[0], r[1], ', '.join(r[11]), tr['cu'], tr['agrupado'], tr['uc'], ', '.join(rnf_rf(r[0])), tr['inb']))
            continue
        rf_rows.append((r[0], r[1], ', '.join(r[11]), ', '.join(c[0] for c in cus),
                        ', '.join(sorted({c[5] for c in cus})), ', '.join(sorted({c[6] for c in cus})),
                        ', '.join(rnf_rf(r[0])), ', '.join(sorted({c[7] for c in cus}))))
    val = V.checks()
    fails = sum(1 for v in val if v[1] != 'OK')
    pend = [
        ('T-01', 'AS-IS', 'Todo el AS-IS es **preliminar**: sin validación de RR. HH. ni de la Administración del Colegio',
         'ACEPTADO / DOCUMENTADO', 'Se mantiene el rótulo en F2 a F4; no se afirman hechos institucionales'),
        ('T-02', 'AS-IS → problema', 'AS-01 no tiene un problema asociado', 'INFO, no bloqueante',
         'No toda actividad es problemática'),
        ('T-03', 'Problema → solución', 'P5 se atiende **en parte**: los indicadores dependen de RF-28, un candidato no implementado',
         'ACEPTADO', 'Declarado en F4, F5 y F6'),
        ('T-04', 'TO-BE → RF', 'TB-F1 «cerrar sin selección» no tiene RF', 'RESUELTO (F27D, H-04)',
         'TB-F1 desconectado del flujo como propuesta futura (A-30), sin condición del sistema'),
        ('T-05', 'TO-BE ← AS-IS', 'TB-30 (auditoría) no tiene actividad AS-IS de origen', 'INFO',
         'Capacidad nueva y transversal; atiende P5 a través de S-05 (§2.3)'),
        ('T-06', 'RF → CU', 'La consulta de auditoría (RF-27) no tiene un CU académico propio', 'RESUELTO como DIFERIDO (F27D, H-11)',
         'CU-21 diferido por decisión del equipo; RF-27 es transversal → UC-RF27, IN-08'),
        ('T-07', 'CU', 'Los nombres de CU-01 a CU-20 los asignó la F27B', 'RESUELTO por decisión del equipo (F27D, H-12)',
         '20 CU aprobados; CU-18 renombrado a «Registrar decisión final humana»'),
        ('T-08', 'RNF', 'RNF-06 y RNF-07 no verificados; RNF-05, RNF-08 y RNF-09 con evidencia parcial', 'ACEPTADO',
         'Criterios propuestos en el F7, sin umbrales inventados'),
        ('T-09', 'RNF ↔ catálogo técnico', 'La equivalencia no es 1:1 (10 académicos frente a 11 técnicos)', 'ACEPTADO',
         'Unificarla es una decisión del equipo (F24 L-01)'),
        ('T-10', 'Diagramas', 'Los BPMN de F3 y F5 y la vista académica de F8 eran borradores con ambigüedades (MEDIUM en la F27C)',
         'RESUELTO EN ESPECIFICACIÓN; pendiente de formalización en PowerDesigner',
         'Especificaciones cerradas (H-01 a H-05, H-11 a H-13): READY FOR POWERDESIGNER en la F29'),
        ('T-11', 'F9', 'El F9 publicado no refleja el release, la QA de la F25 ni la resolución de los rótulos', 'CUBIERTO POR ADENDA',
         '[Adenda post-release](../practica-09/F9_POST_RELEASE_ADDENDUM.md); el F9 no se modifica'),
        ('T-12', 'Problema → RF', 'RF-07 (TB-10) y RF-08 (TB-11) no aparecen en la relación problema → RF de §2.3',
         'RESUELTO / CONCILIADO (F27D, H-06)',
         'La columna «Problema directo» muestra los problemas que F4 asigna a su actividad AS-IS (AS-06 → P1; AS-07 → P4). '
         'La columna «vía solución» queda vacía porque §2.3 no los incluye en ninguna solución. No se inventan relaciones'),
    ]
    text = f"""# Trazabilidad F2 → F9 (Fases 27B y 27D)

Cadena académica completa: actividad AS-IS → problema → solución → actividad TO-BE → RF → RNF relevantes → CU → alcance del F9.
Se genera desde los mismos modelos que los Formatos 02 a 08 (`docs/academico/tools/f27b/`), así que no puede contradecirlos.
Para regenerarla: `python docs/academico/tools/f27b/build.py trace`.

Alcance de la validación automática: [`README.md`](README.md). `validate.py` comprueba la coherencia **estructural**, no la semántica completa.

| Formato | Entregable |
|---|---|
| F2 | [`practica-02`](../practica-02/README.md) |
| F3 | [`practica-03`](../practica-03/README.md) |
| F4 | [`practica-04`](../practica-04/README.md) |
| F5 | [`practica-05`](../practica-05/README.md) |
| F6 | [`practica-06`](../practica-06/README.md) |
| F7 | [`practica-07`](../practica-07/README.md) |
| F8 | [`practica-08`](../practica-08/README.md) |
| F9 | [`phase-24/output`](../phase-24/README.md) (publicado, sin cambios) y [`practica-09`](../practica-09/F9_POST_RELEASE_ADDENDUM.md) (adenda) |

**Estado de cada eslabón:**

| Eslabón | Estado |
|---|---|
| AS-IS (F2 a F4) | **Preliminar**, sujeto a validación institucional |
| TO-BE (F5) | **Propuesto** |
| RF (F6) y CU (F8) | Describen el **software implementado** v1.1 |
| RNF (F7) | Cada uno con su estado de verificación |
| RF-28, RF-29 y RNF-A a RNF-D | **Fuera** de la cadena de la línea base |

## 1. Cadena completa por actividad TO-BE

**Dos columnas de problema (H-06):**

- **«Problema directo (F4)»:** solo los problemas que el Formato 04 asigna a la actividad AS-IS de origen.
- **«Problema vía solución»:** el problema que atiende la solución (F5, relación de §2.3) donde participa esa actividad TO-BE.

Una columna no se deduce de la otra, y no se atribuye a ninguna actividad un problema que F4 no le asignó.

{md_table(['AS-IS', 'Problema directo (F4)', 'Problema vía solución', 'Solución', 'Actividad TO-BE', 'RF', 'RNF relevantes', 'CU', 'Alcance F9'], rows)}

## 2. Del proceso actual al TO-BE

{md_table(['AS-IS', 'Actividad actual', 'Problemas (F4)', 'Actividades TO-BE que la sustituyen'], as_rows)}

## 3. Por requerimiento funcional

RF-23 va a CU-18 «Registrar decisión final humana» → UC-RF23 (IN-07). RF-27 es transversal → UC-RF27 (IN-08) y no se mezcla con RF-23 (H-07).

{md_table(['RF', 'Nombre canónico', 'TO-BE', 'CU académico', 'CU agrupado (v1.0)', 'UC-RF', 'RNF relevantes', 'Alcance F9'], rf_rows)}

## 4. RNF transversales

{md_table(['RNF', 'Nombre', 'Estado', 'Equivalente técnico'], [(x[0], x[2], x[8], next(e[1] for e in N.EQUIVALENCIA if e[0].startswith(x[0]))) for x in N.RNF])}

## 5. Validación de coherencia estructural (§17 del encargo)

Resultado de `docs/academico/tools/f27b/validate.py` al generar este documento: **{len(val) - fails} de {len(val)} reglas OK, {fails} fallas.**

Es una validación **estructural**. En la F27D, además, se revisaron a mano F3, F5, F8 y esta trazabilidad (ver [`README.md`](README.md)).

{md_table(['Regla', 'Resultado', 'Detalle'], val)}

## 6. Rupturas y pendientes conocidos (historial y resolución)

La descripción original de la F27B se conserva y la resolución de la F27D se añade al lado.

{md_table(['ID', 'Eslabón', 'Pendiente (F27B)', 'Estado (F27D)', 'Resolución'], pend)}
"""
    write_text(os.path.join(out_dir, 'F2-F9-traceability.md'), text)
    print('OK', os.path.relpath(os.path.join(out_dir, 'F2-F9-traceability.md'), ROOT))


# --------------------------------------------------------------------------- F11 adaptado (Fase 28)
import m_arch as AR  # noqa: E402

F9_BASE = os.path.join(ACAD, 'phase-24', 'output', 'F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx')
F11_STEM = 'F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino'


def arch_diagram():
    path = os.path.join(pdir(11, 'diagramas', 'draft'), 'F11-arquitectura-conceptual.png')
    L = lambda c: next(x for x in AR.COMPONENTES if x[0] == c)
    t = lambda c, extra='': f'{c} {L(c)[1]}' + (f'\n{extra}' if extra else '')
    groups = [
        (60, 105, 1420, 90, 'Actores', 'actors'),
        (60, 240, 1420, 110, 'Capa de presentación', 'layer'),
        (60, 375, 1420, 135, 'Capa de acceso y seguridad', 'layer'),
        (60, 535, 1430, 470, 'Capa de negocio (módulos del monolito)', 'business'),
        (1530, 375, 330, 630, 'Servicios transversales', 'transversal'),
        (60, 1040, 1430, 160, 'Persistencia e infraestructura', 'infra'),
        (1530, 1040, 330, 250, 'Experimental (opcional)', 'experimental'),
    ]
    bw, bh = 290, 90
    xs = [90, 450, 810, 1170]
    boxes = {
        'ACT': (90, 135, 1360, 50, 'Área solicitante · Recursos Humanos · Aprobador / Dirección · Evaluador · Postulante', 'actor'),
        'C01': (90, 272, 1360, 64, t('C01', 'páginas por rol · portal público de empleos · notificaciones propias'), 'normal'),
        'C02': (90, 410, 650, 80, t('C02', 'registro, inicio de sesión, 2FA'), 'normal'),
        'C03': (800, 410, 650, 80, t('C03', 'rol + organización · organization_id'), 'transversal'),
        'C04': (xs[0], 580, bw, bh, t('C04'), 'normal'),
        'C05': (xs[1], 580, bw, bh, t('C05'), 'normal'),
        'C07': (xs[2], 580, bw, bh, t('C07'), 'normal'),
        'C06': (xs[3], 580, bw, bh, t('C06'), 'normal'),
        'C10': (xs[0], 740, bw, bh, t('C10', 'Aprobador / Dirección'), 'human'),
        'C09': (xs[1], 740, bw, bh, t('C09', 'apoyo: no selecciona'), 'normal'),
        'C08': (xs[2], 740, bw, bh, t('C08'), 'normal'),
        'C11': (xs[0], 895, bw, bh, t('C11'), 'normal'),
        'C12': (1560, 430, 270, 140, t('C12', 'se encolan tras el commit'), 'transversal'),
        'C13': (1560, 640, 270, 140, t('C13', 'solo inserción'), 'transversal'),
        'C14': (90, 1090, 430, 80, t('C14'), 'infra'),
        'C15': (560, 1090, 430, 80, t('C15'), 'infra'),
        'C16': (1030, 1090, 430, 80, t('C16'), 'infra'),
        'C17': (1560, 1090, 270, 170, t('C17', 'solo el proceso; no evalúa personas'), 'experimental'),
    }
    anchors = {'BUS': (60, 535, 1430, 470), 'INFRA': (60, 1040, 1430, 160), 'TRV': (1530, 375, 330, 630)}
    arrows = [
        ('ACT', 'C01', 'usan', 'solid'), ('C01', 'C02', 'R-01', 'solid'), ('C02', 'C03', 'R-02', 'solid'),
        ('C03', 'BUS', 'R-03', 'solid'),
        ('C04', 'C05', 'R-05', 'solid'), ('C05', 'C07', 'R-06', 'solid'), ('C06', 'C07', 'R-07', 'solid'),
        ('C08', 'C07', 'R-08', 'solid'), ('C08', 'C09', 'R-09', 'solid'), ('C09', 'C10', 'R-10', 'solid'),
        ('C10', 'C11', 'R-11', 'solid'),
        ('BUS', 'TRV', 'R-13/14', 'solid'), ('BUS', 'INFRA', 'R-16/17', 'solid'),
        ('C05', 'C17', 'R-19', 'dashed', [(595, 580), (595, 555), (1510, 555), (1510, 1175), (1560, 1175)]),
        ('C17', 'C01', 'R-20', 'dashed', [(1830, 1175), (1880, 1175), (1880, 304), (1450, 304)]),
    ]
    notes = [
        (60, 1320, 900, 'C10 es la decisión HUMANA (RF-23): la registra el Aprobador / Dirección. C09 calcula y compara, '
                        'pero no selecciona ni cambia estados.'),
        (60, 1395, 900, 'C11 aplica las transiciones de C07 (R-12). C12 usa la cola de C16 (R-15). C02 usa sesiones de C16 '
                        '(R-18). C01 invoca los módulos a través de C03 (R-04).'),
        (1000, 1320, 860, 'C17 (RF-29) es experimental y opcional: no se relaciona con C09, C10 ni C11. RF-28 (panel '
                          'operativo) es un candidato NO IMPLEMENTADO y no forma parte de la arquitectura.'),
    ]
    dg.block_diagram(path, 'F11 · Arquitectura conceptual del sistema (adaptación académica, Guía 11)',
                     '17 componentes conceptuales en capas. Flechas numeradas = relaciones R-xx de RELATIONSHIPS.md.',
                     groups, boxes, arrows, notes, size=(1900, 1490), anchors=anchors)
    return path


def rnf_of_comp(c):
    return [r[0] for r in AR.RNF_ARQ if c in r[3] or r[3].startswith('Todos')]


def f11_trace_rows():
    import validate as V
    _, comp, rf_of, cu_of, _ = V.f11_model()
    rows = []
    for c in AR.COMPONENTES:
        cus = sorted(cu_of[c[0]])
        ins = sorted({x.strip() for u in U.CU if u[0] in cus for x in u[7].split('·')})
        if 'RF-27' in rf_of[c[0]]:
            ins = sorted(set(ins) | {'IN-08'})
        rfs = ', '.join(sorted(rf_of[c[0]])) or ('; '.join(c[4]))
        rows.append((f'{c[0]} {c[1]}', rfs, ', '.join(cus) or c[5], ', '.join(rnf_of_comp(c[0])) or '—',
                     ', '.join(ins) or ('Fuera de la línea base (RF-29)' if c[0] == 'C17' else 'Transversal / soporte'), c[8]))
    return rows


@builder('f11')
def build_f11():
    import validate as V
    diag = arch_diagram()
    checks = V.f11_checks()
    d = Doc()
    d.note('Formato 11 – Arquitectura del sistema. Adaptación académica', [
        AR.NOTA_ADAPTACION + ' Formato oficial no publicado / no disponible.',
        'Estructura derivada de las actividades y entregables de la Guía 11: lista de componentes, relación entre '
        'componentes, diagrama de arquitectura conceptual y arquitectura validada.',
        f'Estados usados: **{C.SI}** (componentes IMPLEMENTADOS), TRANSVERSAL, **EXPERIMENTAL** (RF-29), NO IMPLEMENTADO '
        '(RF-28). La decisión final de selección es **humana** (RF-23).'])
    d.h('Datos generales')
    d.kv([('Proyecto', C.PROYECTO), ('Curso', 'Pruebas y Calidad de Software'), ('NRC', '28607'), ('Docente', C.DOCENTE),
          ('Equipo', C.EQUIPO), ('Formato', 'Formato 11 – Arquitectura del sistema (adaptación académica; sin plantilla oficial)'),
          ('Fuente normativa', 'Guía de Práctica N.° 11 (docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx)'),
          ('Fecha', '28/09/2026'),
          ('Estado', 'Versión 1.1: integra la vista formal ARQ-01 de PowerDesigner (F29, con el hotfix F29B). La versión '
                     '1.0 se auditó en la Fase 28. Sin aprobación institucional')],
         widths=(26, 74), sz=17)
    d.sub('Correspondencia con la Guía 11')
    d.table(['ID', 'Exigencia de la guía', 'Apartado de la guía', 'Sección de este documento'],
            [(g[0], g[1], g[2], s) for g, s in zip(AR.GUIA, ['2', '3', '4 y 5', '6 y 7', '8', '10'])], widths=[8, 50, 20, 22])
    d.h('Contexto y alcance arquitectónico')
    d.p('Síntesis del Formato 09 v1.1 útil para la arquitectura; el F9 publicado no se modifica.')
    d.kv(AR.CONTEXTO, widths=(22, 78), sz=16)
    d.h('Casos de uso que condicionan la arquitectura')
    d.p('Agrupados por responsabilidad arquitectónica a partir del catálogo aprobado del Formato 08 (CU-01 a CU-20). '
        'CU-18 es «Registrar decisión final humana». CU-21 «Consultar auditoría» está **DIFERIDO** y no forma parte del catálogo.')
    d.table(['Responsabilidad', 'Casos de uso', 'Qué condiciona en la arquitectura', 'Componentes'], AR.CU_GRUPOS,
            widths=[18, 28, 38, 16], sz=16)
    d.h('Componentes principales')
    d.table(['ID', 'Componente', 'Capa conceptual', 'Estado'], [(c[0], c[1], c[2], c[7]) for c in AR.COMPONENTES],
            widths=[8, 42, 30, 20], sz=16)
    d.p('Son **17 componentes conceptuales**: agrupan responsabilidades, no son clases ni carpetas. Evaluaciones y '
        'entrevistas forman un solo componente porque comparten programación y registro (un único módulo en el código). '
        'La decisión (C10) se separa de la selección y el cierre (C11) para dejar visible la frontera de RF-23.')
    d.sub('Elementos no incluidos como componentes')
    d.table(['ID', 'Elemento', 'Estado', 'Motivo'], AR.EXCLUIDOS, widths=[8, 26, 22, 44], sz=16)
    d.h('Responsabilidades')
    d.table(['ID', 'Componente', 'Responsabilidad', 'RF', 'CU', 'Actores', 'Fuente'],
            [(c[0], c[1], c[3], ', '.join(c[4]), c[5], c[6], c[8]) for c in AR.COMPONENTES],
            widths=[6, 13, 27, 12, 12, 13, 17], sz=14)
    d.h('Relaciones entre componentes')
    d.table(['ID', 'Origen', 'Destino', 'Tipo', 'Información intercambiada', 'RF/CU'],
            [(r[0], r[1], r[2], r[3], r[4], r[6]) for r in AR.RELACIONES], widths=[7, 12, 13, 13, 38, 17], sz=15)
    d.p('La dependencia y la observación de cada relación están en `RELATIONSHIPS.md`. No hay dependencias circulares '
        'entre los módulos de negocio: C07 (postulaciones) no depende de ningún otro módulo de negocio.')
    d.h('Flujo de información')
    d.box([f'{i}. {x}' for i, x in enumerate(AR.FLUJO, start=1)])
    d.p(AR.NOTA_FLUJO)
    d.sub('Flujo separado de RF-29 (experimental)')
    d.box([f'{i}. {x}' for i, x in enumerate(AR.FLUJO_RF29, start=1)])
    d.h('Arquitectura conceptual')
    d.table(['Capa conceptual', 'Componentes'], AR.CAPAS, widths=[45, 55])
    d.p(AR.NOTA_CAPAS)
    exp = pd('exports', 'ARQ-01_Arquitectura_Conceptual.png')
    d.p('Vista formal **ARQ-01** modelada en **PowerDesigner 16.6** (Fase 29): diagrama «ARQ-01 - Arquitectura '
        'Conceptual» del modelo `F29_UML_Academico.oom`, paquete ARQ01. Muestra los 17 componentes dentro de sus 6 '
        'agrupaciones y las relaciones R-01 a R-20. La figura 1 va en una página horizontal; las figuras 2 y 3 amplían '
        'sus dos mitades y no añaden contenido.')
    d.wide_img(exp, 'Figura 1. Arquitectura conceptual del sistema: vista formal ARQ-01, exportación de PowerDesigner '
                    '(F29), `ARQ-01_Arquitectura_Conceptual.png`.')
    d.img(exp, 'Figura 2. Ampliación de la figura 1 (franja del 0 % al 55 % del ancho). Recorte sin retoque de la '
               'exportación formal.', 16.5, crop=(0.0, 0.55))
    d.img(exp, 'Figura 3. Ampliación de la figura 1 (franja del 45 % al 100 % del ancho), con C17 (RF-29, experimental) '
               'y las notas del diagrama. Recorte sin retoque de la exportación formal.', 16.5, crop=(0.45, 1.0))
    d.p('C10 es la decisión **humana** (RF-23); C09 calcula, ordena y compara, sin seleccionar. RF-28 no se implementó y '
        'no es un componente. C17 (RF-29) es experimental y no se relaciona con C09, C10 ni C11. El borrador de la F28 '
        '(`diagramas/draft/`) queda como antecedente: ' + SUPERSEDED + '.')
    d.sub('Arquitectura técnica de referencia (implementación actual)')
    d.p('Esta sección documenta cómo está construido el sistema. **No es la vista conceptual principal** ni un despliegue.')
    d.kv(AR.TECNICA, widths=(24, 76), sz=16)
    d.h('Decisiones arquitectónicas')
    d.table(['ID', 'Decisión', 'Motivo', 'Fuente', 'Impacto'], AR.DECISIONES, widths=[8, 20, 30, 20, 22], sz=15)
    d.sub('RNF académicos → decisiones y componentes')
    d.table(['RNF', 'Nombre', 'Decisión', 'Componentes / soporte', 'Estado (F7)'], AR.RNF_ARQ, widths=[9, 20, 12, 43, 16], sz=15)
    d.p('RNF-06 y RNF-07 siguen **NO VERIFICADOS**: la arquitectura indica qué decisiones los soportan, pero no hay '
        'medición ni prueba de respaldo y restauración.')
    d.h('Validación')
    npass = sum(1 for c in checks if c[2] == 'PASS')
    d.p(f'Validación estructural y académica de la arquitectura ({len(checks)} criterios): **{npass} PASS**, '
        f'{sum(1 for c in checks if c[2] == "PASS CON OBSERVACIÓN")} PASS CON OBSERVACIÓN, '
        f'{sum(1 for c in checks if c[2] == "NO VERIFICADO")} NO VERIFICADO y '
        f'{sum(1 for c in checks if c[2] == "FALLA")} fallas. El detalle está en `VALIDATION.md`. No hay aprobación institucional.')
    d.table(['Criterio', 'Resultado', 'Evidencia'], [(c[0], c[2], c[3]) for c in checks], widths=[46, 16, 38], sz=14)
    d.h('Limitaciones y observaciones')
    d.bullets(AR.LIMITACIONES)
    d.h('Conclusiones')
    d.box(AR.CONCLUSIONES)
    d.h('Evidencias')
    d.bullets([
        'Guía oficial: `docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx`.',
        'Alcance: F9 v1.1 (`docs/academico/phase-24/output/`) y su adenda (`docs/academico/practica-09/`).',
        'Casos de uso, RF y RNF: Formatos 06, 07 y 08 (`docs/academico/practica-06` a `practica-08`).',
        'Referencias técnicas sin modificar: CO-01 y PK-01 (`docs/v1.1/uml/component-model.md`), DE-01 '
        '(`deployment-model.md`), UC-01, SEQ-07 y SEQ-08 (`docs/v1.1/uml/`); exportaciones de la F23.',
        'Manifiesto con SHA-256: `docs/academico/practica-11/evidencias/README.md`.',
        'Vista formal ARQ-01: modelo `docs/academico/powerdesigner/models/F29_UML_Academico.oom` (paquete ARQ01), '
        'exportaciones `ARQ-01_Arquitectura_Conceptual.png` y `.svg`; validación en `F29_VALIDATION.md` y `F29B_HOTFIX.md`.',
        'Borrador de la F28: `docs/academico/practica-11/diagramas/draft/F11-arquitectura-conceptual.png` (' + SUPERSEDED + ').',
    ])
    d.p('Captura real de PowerDesigner, tomada con el modelo reabierto desde el disco:')
    d.img(pd('evidencias', 'capturas', 'ARQ01_Arquitectura_Conceptual_PowerDesigner.png'),
          'Figura 4. Captura de PowerDesigner: diagrama «ARQ-01 - Arquitectura Conceptual» y paquete ARQ01 en el Object '
          'Browser.', 16)
    d.h('Trazabilidad')
    d.table(['Componente', 'RF', 'CU', 'RNF', 'Alcance F9', 'Artefacto técnico'], f11_trace_rows(),
            widths=[18, 17, 15, 14, 12, 24], sz=14)
    contents = ['Nota de adaptación'] + [f'{i}. {it[1]}' for i, it in enumerate([x for x in d.items if x[0] == 'h'], start=1)]
    title = 'Formato 11 — Arquitectura del sistema (adaptación académica)'
    out_docx = os.path.join(pdir(11), F11_STEM + '.docx')
    build_docx_f9(F9_BASE, out_docx,
                  cover=[('ALCANCE DEL PROYECTO SOFTWARE F9', 'ARQUITECTURA DEL SISTEMA — FORMATO 11 (ADAPTACIÓN ACADÉMICA)'),
                         ('Versión 1.1 · septiembre de 2026', 'Versión 1.1 · septiembre de 2026')],
                  cover_note=AR.NOTA_ADAPTACION,
                  header_text='F11 ADAPTADO | PRUEBAS Y CALIDAD DE SOFTWARE',
                  doc=d, props={'dc:title': title, 'dc:subject': 'Arquitectura conceptual — adaptación académica de la Guía 11',
                                'dc:description': 'NRC 28607 · Formato 11 adaptado (no oficial) · Fase 28',
                                'dc:creator': C.EQUIPO, 'cp:lastModifiedBy': 'Equipo del proyecto'},
                  contents=contents)
    build_md(os.path.join(pdir(11), F11_STEM + '.md'), title, None, d, start=1,
             preface=f'> Espejo en Markdown de `{F11_STEM}.docx`. **{AR.NOTA_ADAPTACION}**')
    print('OK', os.path.relpath(out_docx, ROOT))
    # Archivos de trabajo
    comp_rows = [(c[0], c[1], c[3], ', '.join(c[4]), c[5], c[6], c[7], c[8]) for c in AR.COMPONENTES]
    write_text(os.path.join(pdir(11), 'COMPONENTS.md'),
               '# Componentes de la arquitectura conceptual (F11)\n\nGenerado desde `docs/academico/tools/f27b/m_arch.py`. '
               'Estados: IMPLEMENTADO · TRANSVERSAL · EXPERIMENTAL · PROPUESTO · NO IMPLEMENTADO.\n\n'
               + md_table(['ID', 'Componente', 'Responsabilidad', 'RF asociados', 'CU asociados', 'Actores', 'Estado', 'Fuente'], comp_rows)
               + '\n\n## Elementos no incluidos como componentes\n\n' + md_table(['ID', 'Elemento', 'Estado', 'Motivo'], AR.EXCLUIDOS)
               + '\n\n## Capas conceptuales\n\n' + md_table(['Capa', 'Componentes'], AR.CAPAS) + '\n\n' + AR.NOTA_CAPAS)
    write_text(os.path.join(pdir(11), 'RELATIONSHIPS.md'),
               '# Relaciones entre componentes (F11)\n\nGenerado desde `m_arch.py`. «C04 a C11» significa cada componente '
               'de ese rango. Las flechas del borrador llevan estos IDs.\n\n'
               + md_table(['ID', 'Origen', 'Destino', 'Tipo de relación', 'Información intercambiada', 'Dependencia',
                           'RF/CU relacionados', 'Observación'], AR.RELACIONES)
               + '\n\n## Flujo de información\n\n' + '\n'.join(f'{i}. {x}' for i, x in enumerate(AR.FLUJO, start=1))
               + '\n\n' + AR.NOTA_FLUJO + '\n\n### Flujo separado de RF-29 (experimental)\n\n'
               + '\n'.join(f'{i}. {x}' for i, x in enumerate(AR.FLUJO_RF29, start=1)))
    _, comp, rf_of, cu_of, _ = V.f11_model()
    comp_val = [(f'{c[0]} {c[1]}', 'Sí — ' + (', '.join(sorted(rf_of[c[0]])) or ', '.join(sorted(cu_of[c[0]])) or
                                            ('transversal' if c[7] == 'TRANSVERSAL' else 'soporte de infraestructura / interfaz')),
                 c[7], 'RF-29 fuera de la línea base' if c[0] == 'C17' else '') for c in AR.COMPONENTES]
    write_text(os.path.join(pdir(11), 'VALIDATION.md'),
               '# Validación de la arquitectura conceptual (F11)\n\nResultados: PASS · PASS CON OBSERVACIÓN · NO VERIFICADO · '
               'NO APLICA. Generado por `validate.py` (`f11_checks`) sobre el modelo `m_arch.py`. Es una validación '
               '**estructural y académica, interna del equipo**: no hay aprobación institucional. `validate.py` no juzga '
               'la calidad semántica del diseño (ver `docs/academico/trazabilidad/README.md`).\n\n## Matriz de validación\n\n'
               + md_table(['Criterio', 'Fuente', 'Resultado', 'Evidencia', 'Observación'], checks)
               + '\n\n## Validación de componentes\n\n'
               + md_table(['Componente', 'Tiene RF/CU/justificación transversal', 'Estado', 'Observación'], comp_val)
               + '\n\n## Validación de relaciones\n\n- Relaciones necesarias: R-01 a R-20 (todas las pedidas por el encargo, '
               'con la dirección de dependencia real).\n- Dependencias circulares entre módulos de negocio: ninguna (C07 no '
               'depende de otro módulo de negocio; C08 y C11 dependen de C07).\n- Componentes aislados: ninguno.\n- Flujo '
               'completo: R-05 → R-06/R-07 → R-08 → R-09 → R-10 → R-11 → R-12.\n- RF-29: C17 solo se relaciona con C05 '
               '(lectura de datos operativos) y C01 (presentación); **sin relación** con C09, C10 ni C11.')
    guia_rows = [
        ('Revisar el alcance', 'Sección 2 (síntesis del F9: IN, OUT, límites y restricciones)', 'PASS'),
        ('Analizar los casos de uso', 'Sección 3 (CU-01..CU-20 agrupados; CU-18 y CU-21 tratados)', 'PASS'),
        ('Identificar los componentes', 'Secciones 4 y 5; COMPONENTS.md (17 componentes y 4 exclusiones)', 'PASS'),
        ('Definir las relaciones', 'Secciones 6 y 7; RELATIONSHIPS.md (20 relaciones y flujo)', 'PASS'),
        ('Diagrama conceptual', 'Sección 8; diagramas/draft/F11-arquitectura-conceptual.png (borrador; formal en F29)', 'PASS'),
        ('Arquitectura validada', f'Sección 10; VALIDATION.md ({npass} PASS, sin fallas; RNF-06 y RNF-07 NO VERIFICADOS; '
                                  'validación interna, no institucional)', 'PASS CON OBSERVACIONES'),
    ]
    write_text(os.path.join(pdir(11), 'F28_VALIDATION.md'),
               '# Validación de la Fase 28 frente a la Guía 11\n\nCada exigencia de la Guía de Práctica N.° 11 y su evidencia '
               'en este entregable. No se agregan exigencias no oficiales.\n\n'
               + md_table(['Requisito de la Guía 11', 'Evidencia', 'Estado'], guia_rows)
               + '\n\n**Observaciones:** el formato es una adaptación académica (no hay Formato 11 oficial); RNF-06 y '
               'RNF-07 no verificados; H-14 (PDF del F4) pendiente para la F31; sin aprobación institucional.')
    tr = f11_trace_rows()
    write_text(os.path.join(ACAD, 'trazabilidad', 'F11-architecture-traceability.md'),
               '# Trazabilidad de la arquitectura (F11)\n\nComponente → RF → CU → RNF → alcance F9 → artefacto técnico. '
               'Generado desde `m_arch.py`, `m_cu.py` y `validate.py`; no se inventan correspondencias: los RF y CU salen '
               'de la tabla de componentes, el alcance IN sale de los CU (F8/F9) y el artefacto técnico es la fuente '
               'citada (CO-01, PK-01, SEQ, ADR).\n\n'
               + md_table(['Componente', 'RF', 'CU', 'RNF', 'Alcance F9', 'Artefacto técnico'], tr)
               + '\n\nNotas: C01, C03, C14 y C16 soportan todos los RF (interfaz, autorización y persistencia) y no se '
               'listan RF por separado. C13 es transversal (RF-27 → UC-RF27, IN-08). C17 es experimental (RF-29, fuera de '
               'la línea base). Relación con la cadena académica: [F2-F9-traceability.md](F2-F9-traceability.md).')
    write_evidence(11, 'Formato 11 (adaptado)', [
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx', 'Fuente normativa (Guía 11)'),
        ('docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx',
         'Alcance (F9) y base visual del documento (solo lectura)'),
        ('docs/academico/practica-09/F9_POST_RELEASE_ADDENDUM.md', 'Estado post-release del alcance'),
        ('docs/academico/practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.md', 'Casos de uso aprobados (CU-01..CU-20)'),
        ('docs/academico/practica-06/F6_Requerimientos_Funcionales_Colegio_Andino.md', 'RF-01..RF-27'),
        ('docs/academico/practica-07/F7_Requerimientos_No_Funcionales_Colegio_Andino.md', 'RNF académicos y su estado'),
        ('docs/academico/trazabilidad/F2-F9-traceability.md', 'Cadena académica F2 → F9'),
        ('docs/v1.1/uml/component-model.md', 'CO-01 y PK-01: componentes y paquetes reales (referencia)'),
        ('docs/v1.1/uml/deployment-model.md', 'DE-01: despliegue (referencia; no se mezcla con la vista conceptual)'),
        ('docs/v1.1/uml/use-cases.md', 'UC-01: vista técnica de casos de uso (UC-RF27, UC-RF29)'),
        ('docs/v1.1/uml/sequence-diagrams.md', 'SEQ-07 (decisión humana) y SEQ-08 (riesgo operacional)'),
        ('docs/v1.1/powerdesigner/exports/CO-01-componentes.png', 'Exportación CO-01 (F23), sin modificar'),
        ('docs/v1.1/powerdesigner/exports/PK-01-paquetes.png', 'Exportación PK-01 (F23), sin modificar'),
        ('docs/v1.1/powerdesigner/exports/DE-01-despliegue.png', 'Exportación DE-01 (F23), sin modificar'),
        ('docs/v1.1/powerdesigner/exports/UC-01-casos-de-uso.png', 'Exportación UC-01 (F23), sin modificar'),
        ('docs/final-report/07-arquitectura-tecnologica.md', 'Estilo, multitenencia, PostgreSQL y Redis (decisiones)'),
        ('docs/v1.1/architecture-decisions/ADR-001-ml-boundary.md', 'Frontera del ML (DA-07)'),
        ('docs/v1.1/architecture-decisions/ADR-002-human-oversight.md', 'Decisión humana (DA-03)'),
        ('docs/academico/tools/f27b/m_arch.py', 'Modelo de datos de la arquitectura'),
        (f'{PD}/exports/ARQ-01_Arquitectura_Conceptual.png', 'Exportación formal PNG de ARQ-01 (figura principal)'),
        (f'{PD}/exports/ARQ-01_Arquitectura_Conceptual.svg', 'Exportación formal SVG (nativa de PowerDesigner)'),
        (f'{PD}/models/F29_UML_Academico.oom', 'Modelo fuente de PowerDesigner (paquete ARQ01)'),
        (f'{PD}/evidencias/capturas/ARQ01_Arquitectura_Conceptual_PowerDesigner.png',
         'Captura real de PowerDesigner: vista ARQ-01 con sus 6 agrupaciones'),
        (f'{PD}/F29_VALIDATION.md', 'Validación de la vista (F29)'),
        (f'{PD}/F29B_HOTFIX.md', 'Hotfix de reproducibilidad (F29B): geometría de las agrupaciones'),
        ('docs/academico/practica-11/diagramas/draft/F11-arquitectura-conceptual.png',
         'Borrador del diagrama conceptual — ' + SUPERSEDED),
    ], note=NOTA_EVID_F29)


# --------------------------------------------------------------------------- F11 oficial regularizado (fase F11-R)
F11R_STEM = 'F11_Arquitectura_del_Sistema_Colegio_Andino'
# Fuentes del registro de la regularización (F11R_REGULARIZACION.md), con su SHA-256.
F11R_SOURCES = [
    ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_11_Arquitectura_del_sistema.docx',
     'Plantilla oficial del Formato 11 (fuente formal principal, solo lectura)'),
    ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx', 'Guía de Práctica 11 (fuente complementaria)'),
    ('docs/academico/practica-11/COMPONENTS.md', 'Componentes C01 a C17 (F28)'),
    ('docs/academico/practica-11/RELATIONSHIPS.md', 'Relaciones R-01 a R-20 (F28)'),
    ('docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png', 'Diagrama ARQ-01 (F29 y F29B)'),
    ('docs/academico/powerdesigner/models/F29_UML_Academico.oom', 'Modelo fuente de ARQ-01 (sin cambios)'),
    ('docs/academico/practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx', 'F11 adaptado histórico (sin cambios)'),
    ('docs/academico/practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf', 'PDF del F11 adaptado histórico (sin cambios)'),
    ('docs/academico/tools/f27b/m_arch.py', 'Modelo de datos de la arquitectura (sin cambios)'),
    ('docs/academico/tools/f27b/m_f11r.py', 'Contenido del F11 oficial: CMP-xx, estilo, decisiones y restricciones'),
    ('docs/academico/tools/f27b/f11r.py', 'Relleno de la plantilla oficial y espejo en Markdown'),
    ('docs/final-report/07-arquitectura-tecnologica.md', 'Estilo, multitenencia, seguridad, PostgreSQL, Redis y despliegue'),
    ('docs/academico/practica-07/F7_Requerimientos_No_Funcionales_Colegio_Andino.md', 'Estado de los RNF (RNF-06 y RNF-07 no verificados; RNF-D propuesto)'),
]


@builder('f11r')
def build_f11r():
    """Formato 11 oficial sobre la plantilla recibida después de la F28. No toca el F11 adaptado (builder «f11»)."""
    import f11r
    out_docx = os.path.join(pdir(11), F11R_STEM + '.docx')
    arq = pd('exports', 'ARQ-01_Arquitectura_Conceptual.png')
    f11r.build(os.path.join(FMT, 'Formato_11_Arquitectura_del_sistema.docx'), arq, out_docx)
    out_md = os.path.join(pdir(11), F11R_STEM + '.md')
    f11r.build_md(out_md, F11R_STEM + '.docx', os.path.relpath(arq, pdir(11)).replace(os.sep, '/'))
    f11r.build_registro(os.path.join(pdir(11), 'F11R_REGULARIZACION.md'), ROOT, F11R_SOURCES)
    print('OK', os.path.relpath(out_docx, ROOT))


# --------------------------------------------------------------------------- F29C variables y operacionalización
F29C_DIR = os.path.join(ACAD, 'operacionalizacion')
F29C_STEM = 'F29C_Operacionalizacion_Variables'
F29C_DIAG = 'F29C_diagrama_conceptual_variables'


@builder('f29c')
def build_f29c():
    """Variables, matriz de operacionalización y diagrama conceptual (guía E1/L1), desde m_variables.py."""
    import f29c
    ddir = os.path.join(F29C_DIR, 'diagramas')
    os.makedirs(ddir, exist_ok=True)
    png = os.path.join(ddir, F29C_DIAG + '.png')
    f29c.render_png(png)
    f29c.render_svg(os.path.join(ddir, F29C_DIAG + '.svg'))
    f29c.build_md(os.path.join(F29C_DIR, F29C_STEM + '.md'), f'diagramas/{F29C_DIAG}.png', f'diagramas/{F29C_DIAG}.svg',
                  'ACTIVIDAD_IA_COMPARACION.md')
    f29c.build_activity(os.path.join(F29C_DIR, 'ACTIVIDAD_IA_COMPARACION.md'))
    if f29c.build_registro(os.path.join(F29C_DIR, f29c.V.REGISTRO)):   # solo si no existe: es evidencia del equipo
        print('OK registro de ejecuciones creado (vacío)')
    out_docx = os.path.join(F29C_DIR, F29C_STEM + '.docx')
    f29c.build_docx(os.path.join(FMT, 'Formato_11_Arquitectura_del_sistema.docx'), png, out_docx)
    print('OK', os.path.relpath(out_docx, ROOT))


# --------------------------------------------------------------------------- F29D plan de pruebas
F29D_DIR = os.path.join(ACAD, 'plan-pruebas')


@builder('f29d')
def build_f29d():
    """Plan de Pruebas sobre la plantilla del curso (PDF): DOCX generado, espejo Markdown y registro."""
    import f29d
    f29d.build(F29D_DIR)
    f29d.build_registro(os.path.join(F29D_DIR, 'F29D_REGISTRO.md'), ROOT)
    print('OK', os.path.relpath(os.path.join(F29D_DIR, f29d.STEM + '.docx'), ROOT))


# --------------------------------------------------------------------------- F29E, F29F y F29G
@builder('f29e')
def build_f29e():
    """Casos de prueba y matriz de trazabilidad, derivados del código de pruebas y de la evidencia F29F."""
    import f29e
    cs = f29e.build(os.path.join(ACAD, 'casos-prueba'))
    print('OK casos-prueba:', len(cs), 'CP')


@builder('f29f')
def build_f29f():
    """Resumen de la ejecución QA final, criterios de aceptación y matriz CP → resultado."""
    import f29f
    crit = f29f.build(os.path.join(ACAD, 'qa-final'))
    print('OK qa-final:', sum(1 for c in crit if c[2]), 'de', len(crit), 'criterios cumplidos')


@builder('f29g')
def build_f29g():
    """Registro final de defectos y métricas calculadas con datos reales."""
    import f29g
    defs = f29g.build(os.path.join(ACAD, 'metricas-calidad'))
    print('OK metricas-calidad:', len(defs), 'registros de defectos')


# --------------------------------------------------------------------------- F29H informe final v1
@builder('f29h')
def build_f29h():
    """Informe Final v1 sobre la plantilla oficial del proyecto final, con espejo Markdown y registro."""
    import f29h
    out_dir = os.path.join(ACAD, 'informe-final')
    heads = f29h.build(ROOT, out_dir)
    f29h.build_registro(os.path.join(out_dir, 'F29H_REGISTRO.md'), ROOT)
    print('OK', os.path.relpath(os.path.join(out_dir, f29h.STEM + '.docx'), ROOT), '—', len(heads), 'títulos')


if __name__ == '__main__':
    keys = sys.argv[1:] or list(BUILDERS)
    for k in keys:
        BUILDERS[k]()
