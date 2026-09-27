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
    out = []
    kw = dict(show_lanes=False, CW=470, RH=118, TW=410, TH=84, FS=20)
    lab = lambda i: f'{i} · {AS[i][1]}\n({", ".join(a for a, r in AS[i][4] if r in ("Ejecuta", "Valida"))})'
    p1 = dg.Swimlanes('F2 · Flujo del proceso actual (AS-IS preliminar) — parte 1 de 2',
                      [('', ''), ('', '')], 'Sujeto a validación institucional. Actor responsable entre paréntesis.', **kw)
    p1.node('ini', 'terminator', 0, 0, 'Inicio: necesidad de personal identificada')
    for r, i in enumerate(['AS-01', 'AS-02', 'AS-03', 'AS-04'], start=1):
        p1.node(i, 'task', 0, r, lab(i))
    p1.node('g1', 'gateway', 0, 5, '¿Necesidad aprobada?')
    p1.node('f1', 'terminator', 1, 5, 'Fin: necesidad no aprobada')
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
                      [('', ''), ('', '')], 'Sujeto a validación institucional. Actor responsable entre paréntesis.', **kw)
    p2.node('c2', 'terminator', 0, 0, 'Viene de la parte 1 (A)')
    p2.node('AS-09', 'task', 0, 1, lab('AS-09'))
    p2.node('g2', 'gateway', 0, 2, '¿Candidato preseleccionado? (por candidato)')
    p2.node('f2', 'terminator', 1, 2, 'Fin: el candidato no continúa')
    for r, i in enumerate(['AS-10', 'AS-11', 'AS-12', 'AS-13', 'AS-14'], start=3):
        p2.node(i, 'task', 0, r, lab(i))
    p2.node('f3', 'terminator', 0, 8, 'Fin: resultado comunicado')
    seq = ['c2', 'AS-09', 'g2', 'AS-10', 'AS-11', 'AS-12', 'AS-13', 'AS-14', 'f3']
    for a, b in zip(seq, seq[1:]):
        p2.edge(a, b, 'Sí' if a == 'g2' else '')
    p2.edge('g2', 'f2', 'No')
    path2 = os.path.join(pdir(2, 'diagramas', 'draft'), 'F2-flujo-as-is-parte2.png')
    p2.render(path2, 'Borrador de revisión (F27B). La formalización BPMN está en el Formato 03.')
    return [path1, path2]


def asis_bpmn():
    """BPMN AS-IS en carriles verticales, dos partes unidas por un evento de enlace."""
    lanes = A.LANES
    kw = dict(CW=310, RH=122, TW=262, TH=92, FS=19)
    sub = 'BPMN AS-IS preliminar derivado del análisis del equipo — sujeto a validación institucional'
    b1 = dg.Swimlanes('F3 · BPMN del proceso actual (AS-IS preliminar) — parte 1 de 2', lanes, sub, **kw)
    t = lambda i: f'{i}\n{AS[i][1]}'
    b1.node('EI-01', 'start', 0, 0, 'EI-01 Necesidad de personal identificada')
    b1.node('AS-01', 'task', 0, 1, t('AS-01'))
    b1.node('AS-02', 'task', 0, 2, t('AS-02'))
    b1.node('AS-03', 'task', 1, 3, t('AS-03'))
    b1.node('AS-04', 'task', 2, 4, t('AS-04'))
    b1.node('G-01', 'gateway', 2, 5, 'G-01 ¿Necesidad aprobada?', off=-70)
    b1.node('EF-01', 'end', 2, 5, 'EF-01 Necesidad no aprobada', off=70)
    b1.node('AS-05', 'task', 1, 6, t('AS-05'))
    b1.node('AS-06', 'task', 1, 7, t('AS-06'))
    b1.node('AS-07', 'task', 4, 8, t('AS-07'))
    b1.node('AS-08', 'task', 1, 9, t('AS-08'))
    b1.node('L-A', 'link', 1, 10, 'Enlace A → parte 2')
    for a, b_ in [('EI-01', 'AS-01'), ('AS-01', 'AS-02'), ('AS-02', 'AS-03'), ('AS-03', 'AS-04'), ('AS-04', 'G-01'),
                  ('AS-08', 'L-A')]:
        b1.edge(a, b_)
    b1.edge('G-01', 'EF-01', 'No')
    b1.edge('G-01', 'AS-05', 'Sí', side='left')
    b1.edge('AS-05', 'AS-06')
    b1.edge('AS-06', 'AS-07', 'convocatoria', kind='msg')
    b1.edge('AS-07', 'AS-08', 'postulación y CV', kind='msg')
    path1 = os.path.join(pdir(3, 'diagramas', 'draft'), 'F3-bpmn-as-is-parte1.png')
    b1.render(path1, 'Líneas discontinuas: flujos de mensaje entre pools. Fuente: F2 (AS-01 a AS-14) y §3.1 del informe v1.0.')
    b2 = dg.Swimlanes('F3 · BPMN del proceso actual (AS-IS preliminar) — parte 2 de 2', lanes, sub, **kw)
    b2.node('L-A2', 'link', 1, 0, 'Enlace A (desde parte 1)')
    b2.node('AS-09', 'task', 1, 1, t('AS-09'))
    b2.node('G-02', 'gateway', 1, 2, 'G-02 ¿Preseleccionado? (por candidato)', off=-70)
    b2.node('EF-02', 'end', 1, 2, 'EF-02 El candidato no continúa', off=80)
    b2.node('AS-10', 'task', 1, 3, t('AS-10'))
    b2.node('M-01', 'inter', 4, 3, 'Citación recibida')
    b2.node('AS-11', 'task', 3, 4, t('AS-11'))
    b2.node('M-02', 'inter', 4, 4, 'Participa en la evaluación o entrevista')
    b2.node('AS-12', 'task', 1, 5, t('AS-12'))
    b2.node('AS-13', 'task', 2, 6, t('AS-13'))
    b2.node('AS-14', 'task', 1, 7, t('AS-14'))
    b2.node('M-03', 'inter', 4, 7, 'Resultado recibido')
    b2.node('EF-03', 'end', 1, 8, 'EF-03 Resultado comunicado')
    for a, b_ in [('L-A2', 'AS-09'), ('AS-09', 'G-02'), ('AS-10', 'AS-11'), ('AS-11', 'AS-12'), ('AS-12', 'AS-13'),
                  ('AS-13', 'AS-14'), ('AS-14', 'EF-03')]:
        b2.edge(a, b_)
    b2.edge('G-02', 'EF-02', 'No')
    b2.edge('G-02', 'AS-10', 'Sí')
    b2.edge('AS-10', 'M-01', 'citación', kind='msg')
    b2.edge('AS-11', 'M-02', '', kind='msg')
    b2.edge('AS-14', 'M-03', 'resultado', kind='msg')
    path2 = os.path.join(pdir(3, 'diagramas', 'draft'), 'F3-bpmn-as-is-parte2.png')
    b2.render(path2, 'G-02 se evalúa por candidato (a detallar como instancia múltiple en PowerDesigner, F29).')
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
           'resultado a los postulantes (EF-03). Caminos alternativos: necesidad no aprobada (EF-01) y candidato '
           'no preseleccionado (EF-02).',
           '**Contexto:** representa las 14 actividades del Formato 02 (AS-01 a AS-14). Es un modelo preliminar, sin '
           'canales, herramientas ni tiempos reales verificados.'])
    d.h('Diagrama BPM del proceso actual (AS-IS)')
    d.instr('Inserte el diagrama BPM elaborado utilizando notación BPMN.')
    d.img(bp[0], 'Figura 1. BPMN AS-IS preliminar, parte 1 (EI-01 a AS-08).', 16)
    d.img(bp[1], 'Figura 2. BPMN AS-IS preliminar, parte 2 (AS-09 a EF-03).', 16)
    d.p('Borrador de revisión dibujado desde la especificación de este formato. La versión formal se modelará en '
        'PowerDesigner cuando la auditoría F27C apruebe el contenido.')
    d.h('Elementos BPMN utilizados')
    d.table(['N°', 'Elemento BPMN', 'Descripción', 'Uso en el proceso'],
            [(str(i), e, ds, u) for i, (e, ds, u) in enumerate(A.ELEMENTOS_BPMN, start=1)], widths=[7, 20, 28, 45])
    d.h('Identificación de actores (Pools / Lanes)')
    d.table(['N°', 'Actor', 'Tipo (Interno / Externo / Sistemas)', 'Lane asignado'],
            [('1', 'Área solicitante', 'Interno', 'Lane «Área solicitante» (pool del Colegio)'),
             ('2', 'Recursos Humanos', 'Interno', 'Lane «RR. HH.» (pool del Colegio)'),
             ('3', 'Dirección', 'Interno', 'Lane «Dirección» (pool del Colegio)'),
             ('4', 'Evaluadores', 'Interno', 'Lane «Evaluadores» (pool del Colegio)'),
             ('5', 'Postulante', 'Externo', 'Pool «Postulante» (externo), comunicado por flujos de mensaje')],
            widths=[7, 25, 23, 45])
    d.p('No hay lane de «Sistemas»: el AS-IS preliminar no identifica ninguna herramienta informática del Colegio.')
    d.h('Descripción del flujo del proceso')
    d.instr('Describir paso a paso cómo se desarrolla el proceso según el diagrama BPM.')
    d.box([f'{i}. {t}' for i, t in enumerate(A.FLUJO, start=1)])
    d.h('Validación del modelo')
    d.instr('Marque con un aspa (X) si se cumplen los enunciados. Se aplica a la especificación y al borrador de '
            'este formato.')
    d.table(['Enunciado', 'X', 'Comprobación'], [
        ('El proceso tiene evento de inicio y fin claramente definidos.', 'X', 'EI-01; EF-01, EF-02 y EF-03.'),
        ('Todas las actividades están conectadas correctamente.', 'X',
         'AS-01 a AS-14 tienen entrada y salida; las partes 1 y 2 se unen con el enlace A.'),
        ('Se utilizan correctamente los elementos BPMN.', 'X',
         'Secuencia dentro del pool y mensajes entre pools. G-02 por candidato queda anotada para modelarse como '
         'instancia múltiple en PowerDesigner.'),
        ('Cada actividad tiene un actor asignado.', 'X', 'Cada tarea está en el lane de su actor (tabla 5).'),
        ('El flujo es coherente y entendible.', 'X', 'Coincide con las 8 actividades macro de §3.1 y con el Formato 02.'),
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


if __name__ == '__main__':
    keys = sys.argv[1:] or list(BUILDERS)
    for k in keys:
        BUILDERS[k]()
