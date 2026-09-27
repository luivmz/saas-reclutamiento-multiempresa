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

from docxgen import Doc, build_docx, build_md  # noqa: E402
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


def write_evidence(n, title, items):
    """evidencias/README.md: cada evidencia con ruta relativa y SHA-256 del archivo en el árbol de trabajo."""
    import hashlib
    out = os.path.join(pdir(n, 'evidencias'), 'README.md')
    lines = [f'# Evidencias — {title}', '',
             'Evidencias reales del repositorio que respaldan el formato. Rutas relativas a la raíz del repositorio. '
             'SHA-256 calculado en la Fase 27B sobre el archivo versionado. No hay capturas institucionales ni firmas: '
             'no existen en el repositorio y no se simulan.', '',
             '| Evidencia | Ruta | SHA-256 | Qué respalda |', '|---|---|---|---|']
    for path, what in items:
        full = os.path.join(ROOT, path)
        if os.path.isdir(full):
            h = '(carpeta)'
        else:
            with open(full, 'rb') as f:
                h = '`' + hashlib.sha256(f.read()).hexdigest() + '`'
        link = os.path.relpath(full, os.path.dirname(out)).replace(os.sep, '/')
        lines.append(f'| {os.path.basename(path.rstrip("/"))} | [`{path}`]({link}) | {h} | {what} |')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')


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
               'la institución y no es el modelo formal de PowerDesigner (pendiente para la Fase 29, ver '
               '`POWERDESIGNER_PENDING.md`).'])
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
    d.img(bp[0], 'Figura 1. BPMN AS-IS preliminar, parte 1 (EI-01 a AS-08).', 16)
    d.img(bp[1], 'Figura 2. BPMN AS-IS preliminar, parte 2 (AS-09 a EF-03).', 16)
    d.p('Borrador de revisión dibujado desde la especificación de este formato (corregida en la F27D tras la auditoría '
        'F27C). La versión formal se modelará en PowerDesigner en la F29.')
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
    d.instr('Marque con un aspa (X) si se cumplen los enunciados. Se aplica a la especificación y al borrador de '
            'este formato.')
    d.table(['Enunciado', 'X', 'Comprobación'], [
        ('El proceso tiene evento de inicio y fin claramente definidos.', 'X',
         'Proceso: EI-01; EF-01 y EF-03. SP-01: SI-01; EF-02 y EF-04. Postulante: EP-01; EP-02.'),
        ('Todas las actividades están conectadas correctamente.', 'X',
         'AS-01 a AS-14 tienen entrada y salida de secuencia; AS-06 → AS-08 es secuencia (AS-08 es tarea de recepción); '
         'AS-07 está entre EP-01 y EP-02; las partes 1 y 2 se unen con el enlace A.'),
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
        'Borradores: `docs/academico/practica-03/diagramas/draft/F3-bpmn-as-is-parte1.png` y `…parte2.png`.',
        'Pendiente de modelado formal: `docs/academico/practica-03/POWERDESIGNER_PENDING.md`.',
    ])
    emit(3, 'F3_Diagrama_BPM_ASIS_Colegio_Andino', 'Formato_03_Diagrama_BPM.docx', 'proceso', d,
         'Formato 03 — Diagrama BPM del proceso actual (AS-IS preliminar)')
    write_evidence(3, 'Formato 03', EVID_ASIS + [
        ('docs/academico/practica-03/diagramas/draft/F3-bpmn-as-is-parte1.png', 'Borrador BPMN AS-IS, parte 1'),
        ('docs/academico/practica-03/diagramas/draft/F3-bpmn-as-is-parte2.png', 'Borrador BPMN AS-IS, parte 2'),
        ('docs/academico/practica-02/F2_Analisis_del_Proceso_Colegio_Andino.docx', 'Formato 02 del que deriva el BPMN'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_03.docx', 'Guía oficial de la Práctica 03'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_03_Diagrama_BPM.docx',
         'Plantilla oficial del Formato 03 (solo lectura)'),
    ])


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
               '(propuesta futura no implementada). RF-29 (experimental) no forma parte del TO-BE base.'])
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
    caps = ['parte 1: nivel vacante (requerimiento y convocatoria)', 'parte 2a: SP-P por postulación (1 de 2) y pool Postulante',
            'parte 2b: SP-P por postulación (2 de 2)', 'parte 3: nivel vacante (selección y cierre)']
    for i, (pth, cap) in enumerate(zip(bp, caps), start=1):
        d.img(pth, f'Figura {i}. BPMN TO-BE propuesto, {cap}. Borrador de revisión.', 16.5)
    d.p('Borrador dibujado desde la especificación de este formato (corregida en la F27D tras la auditoría F27C). La '
        'versión formal se modelará en PowerDesigner en la F29 (`POWERDESIGNER_PENDING.md`).')
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
    d.img(ante, 'Figura 5. Antecedente: TO-BE original del equipo (anexo A del F9 v1.0, copia sin modificar). Incluye la '
                'rama «cerrar sin selección», no implementada.', 16)
    d.bullets([
        'TO-BE escrito e implementado: `docs/final-report/03-procesos-negocio.md` §3.3–3.5 y '
        '`docs/final-report/diagram-reports/02-bpmn-to-be-report.md`.',
        'Reglas: `docs/assumptions.md` (A-05, A-13, A-16, A-23 a A-31). Verificación del flujo completo: E2E-13 y la QA de la '
        'Fase 25 (`docs/v1.1/phase-25-final-qa.md`).',
        'Comportamiento implementado de referencia (no es el TO-BE institucional): AC-01 '
        '(`docs/v1.1/powerdesigner/exports/AC-01-proceso-reclutamiento.png`).',
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
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte1.png', 'Borrador BPMN TO-BE, parte 1'),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte2a.png', 'Borrador BPMN TO-BE, parte 2a (SP-P)'),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte2b.png', 'Borrador BPMN TO-BE, parte 2b (SP-P)'),
        ('docs/academico/practica-05/diagramas/draft/F5-bpmn-to-be-parte3.png', 'Borrador BPMN TO-BE, parte 3'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_05.docx', 'Guía oficial de la Práctica 05'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_05_Modelo_BPM_mejorado.docx',
         'Plantilla oficial del Formato 05 (solo lectura)'),
    ])


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
    d.sub('Nombres canónicos y alias históricos')
    d.table(['ID', 'Nombre canónico', 'Alias en el F9 (v1.0 y v1.1)', 'Alias en el informe v1.0 (cap. 4)'],
            [(k, RFD[k][1], v[0] or '—', v[1] or '—') for k, v in R.ALIAS.items()], widths=[9, 35, 28, 28], sz=16)
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
    d.table(['ID', 'Candidato', 'Estado', 'Observación'], N.CANDIDATOS, widths=[8, 37, 13, 42], sz=16)
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
    estado(d, [f'Los casos de uso representan el **{C.SI}** de la línea base RF-01 a RF-27. El diagrama académico es un '
               '**borrador**. La vista técnica formal es UC-01 de PowerDesigner (F23), que no se modifica.'])
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
    d.img(diag, 'Figura 1. Diagrama de casos de uso, vista académica (CU-01 a CU-20). Borrador de revisión.', 16.5)
    d.img(uc01, 'Figura 2. Referencia técnica: UC-01 de PowerDesigner (F23), un caso por RF. Exportación versionada, sin cambios.', 16.5)
    d.p('La adaptación formal de la vista académica en PowerDesigner está en `POWERDESIGNER_PENDING.md`. No se modificó '
        'el OOM de la F23.')
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
    d.img(ante, 'Figura 3. Antecedente superado: diagrama de CU del F9 v1.0 (anexo B, copia sin modificar). Incluye '
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
        ('docs/academico/practica-08/diagramas/draft/F8-casos-de-uso-academico.png', 'Borrador del diagrama académico'),
        ('docs/academico/tools/f27b/m_cu.py', 'Modelo de datos de los CU usado por el generador'),
        ('docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_08.docx', 'Guía oficial de la Práctica 08'),
        ('docs/academico/00-fuentes-oficiales/formatos-originales/Formato_08_Diagrama_de_casos_de_uso.docx',
         'Plantilla oficial del Formato 08 (solo lectura)'),
    ])


# --------------------------------------------------------------------------- Trazabilidad F2 → F9
@builder('trace')
def build_trace():
    import validate as V
    out_dir = os.path.join(ACAD, 'trazabilidad')
    os.makedirs(out_dir, exist_ok=True)
    tbd = {t[0]: t for t in T.ACTIVIDADES + T.FUTURAS}
    rnf_rf = lambda rf: N.RNF_POR_RF.get(rf, N.RNF_POR_RF['default'])
    cu_of = lambda rfs: [c for c in U.CU if set(c[4]) & set(rfs)]
    rows = []
    for t in T.ACTIVIDADES + T.FUTURAS:
        sols = [s for s in T.SOLUCIONES if t[0] in s[4]]
        cus = cu_of(t[5])
        rows.append((', '.join(t[6]) or '— (nueva)', ', '.join(s[0] for s in sols) or '—', ', '.join(s[1] for s in sols) or '—',
                     f'{t[0]} {t[2]}', ', '.join(t[5]) or '— (propuesta futura)',
                     ', '.join(sorted({x for r in t[5] for x in rnf_rf(r)})) or '—',
                     ', '.join(c[0] for c in cus) or '—',
                     ', '.join(sorted({p.strip() for c in cus for p in c[7].split('·')})) or 'Fuera de alcance (OUT)'))
    as_rows = [(a[0], a[1], ', '.join(a[5]) or '—', ', '.join(t[0] for t in T.ACTIVIDADES if a[0] in t[6])) for a in A.ACTIVIDADES]
    rf_rows = []
    for r in R.RF:
        cus = cu_of([r[0]])
        rf_rows.append((r[0], r[1], ', '.join(r[11]), ', '.join(c[0] for c in cus),
                        ', '.join(sorted({c[5] for c in cus})), ', '.join(sorted({c[6] for c in cus})),
                        ', '.join(rnf_rf(r[0])), ', '.join(sorted({p.strip() for c in cus for p in c[7].split('·')}))))
    val = V.checks()
    fails = sum(1 for v in val if v[1] != 'OK')
    text = f"""# Trazabilidad F2 → F9 (Fase 27B)

Cadena académica completa: actividad AS-IS → problema → solución → actividad TO-BE → RF → RNF relevantes → CU → alcance del F9.
Se genera desde los mismos modelos que los Formatos 02 a 08 (`docs/academico/tools/f27b/`), así que no puede contradecirlos.
Para regenerarla: `python docs/academico/tools/f27b/build.py trace`.

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
| RF-28, RF-29 y RNF-C | **Fuera** de la cadena de la línea base |

Un RNF no se asocia a una única actividad: son transversales, y la columna muestra los más relevantes para cada RF.

## 1. Cadena completa por actividad TO-BE

{md_table(['AS-IS', 'Problema', 'Solución', 'Actividad TO-BE', 'RF', 'RNF relevantes', 'CU', 'Alcance F9'], rows)}

## 2. Del proceso actual al TO-BE

{md_table(['AS-IS', 'Actividad actual', 'Problemas', 'Actividades TO-BE que la sustituyen'], as_rows)}

## 3. Por requerimiento funcional

{md_table(['RF', 'Nombre canónico', 'TO-BE', 'CU académico', 'CU agrupado (v1.0)', 'UC-RF', 'RNF relevantes', 'Alcance F9'], rf_rows)}

## 4. RNF transversales

{md_table(['RNF', 'Nombre', 'Estado', 'Equivalente técnico'], [(x[0], x[2], x[8], next(e[1] for e in N.EQUIVALENCIA if e[0].startswith(x[0]))) for x in N.RNF])}

## 5. Validación de coherencia (§17 del encargo)

Resultado de `docs/academico/tools/f27b/validate.py` al generar este documento: **{len(val) - fails} de {len(val)} reglas OK, {fails} fallas.**

{md_table(['Regla', 'Resultado', 'Detalle'], val)}

## 6. Rupturas y pendientes conocidos

Las reglas se cumplen. Estos puntos son **límites declarados**, no errores de trazabilidad:

| ID | Eslabón | Pendiente | Tratamiento |
|---|---|---|---|
| T-01 | AS-IS | Todo el AS-IS es **preliminar**: sin validación de RR. HH. ni de la Administración del Colegio | Mantener el rótulo hasta validarlo; no afirmar hechos institucionales |
| T-02 | AS-IS → problema | AS-01 no tiene un problema asociado | Correcto: no toda actividad es problemática |
| T-03 | Problema → solución | P5 se atiende **en parte**: los indicadores de gestión dependen de RF-28, un candidato no implementado | Declarado en F4, F5 y F6 |
| T-04 | TO-BE → RF | TB-F1 «cerrar sin selección» no tiene RF: es una propuesta futura (A-30) | Requiere un cambio de alcance aprobado |
| T-05 | TO-BE ← AS-IS | TB-30 (auditoría) no tiene actividad AS-IS de origen: es una capacidad nueva | Correcto: responde a P2 y P5 |
| T-06 | RF → CU | La consulta de auditoría (RF-27) no tiene un CU académico propio; el F9 la incluye en CU-18 | Propuesta CU-21, pendiente de decisión del equipo (O-F8-02) |
| T-07 | CU | Los nombres de CU-01 a CU-20 los asignó la F27B; el F9 solo los numeraba | Confirmación del equipo (O-F8-01) |
| T-08 | RNF | RNF-06 y RNF-07 no están verificados; RNF-05, RNF-08 y RNF-09 tienen evidencia parcial | Criterios propuestos en el F7, sin umbrales inventados |
| T-09 | RNF ↔ catálogo técnico | La equivalencia no es 1:1 (10 académicos frente a 11 técnicos) | Unificarla es una decisión del equipo (F24 L-01) |
| T-10 | Diagramas | Los BPMN de F3 y F5 y el diagrama académico de F8 son **borradores** | Se formalizan en PowerDesigner en la F29, tras la F27C ([worklist](../POWERDESIGNER_WORKLIST.md)) |
| T-11 | F9 | El F9 publicado no refleja el release, la QA de la F25 ni la resolución de los rótulos | [Adenda](../practica-09/F9_POST_RELEASE_ADDENDUM.md); el F9 no se modifica |
| T-12 | Problema → RF | RF-07 (TB-10) y RF-08 (TB-11) no responden directamente a P1–P5 en la relación de §2.3: habilitan el flujo (publicar y acceder) | Correcto; no se fuerza una relación inexistente |
"""
    write_text(os.path.join(out_dir, 'F2-F9-traceability.md'), text)
    print('OK', os.path.relpath(os.path.join(out_dir, 'F2-F9-traceability.md'), ROOT))


if __name__ == '__main__':
    keys = sys.argv[1:] or list(BUILDERS)
    for k in keys:
        BUILDERS[k]()
