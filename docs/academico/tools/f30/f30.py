"""F30 — Genera los documentos derivados de datos y el consolidado Word.

Generados (no se editan a mano):
  investigacion-ia/F30_Matriz_Evidencia_Cientifica.md   ← fuentes.py + m_matriz.py + datos/*.json
  investigacion-ia/REFERENCIAS.md                       ← datos/verificacion_fuentes.json
  investigacion-ia/F30_Analisis_Herramientas_Skills.md  ← datos/herramientas.json + m_herramientas.py
  investigacion-ia/F30_Investigacion_IA_Reclutamiento.docx  ← consolidado de los documentos Markdown

Uso (desde la raíz del repositorio):  python docs/academico/tools/f30/f30.py [--sin-docx]
El PDF se exporta después con Word:  docs/academico/tools/f27b/topdf_toc.ps1 <docx>
"""
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'f27b'))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'investigacion-ia'))
DATOS = os.path.join(OUT, 'datos')

from fuentes import FUENTES  # noqa: E402
from m_herramientas import ALERTAS, CLASES, CLASIFICACION, SKILLS_LOCALES  # noqa: E402
from m_matriz import MATRIZ, NIVELES, OFICIALES  # noqa: E402

# Excluidas tras la verificación (no entran en la matriz ni se citan como evidencia).
EXCLUIDAS = [
    ('10.1057/s41599-023-01787-8', 'Q', 'Artículo retractado: Crossref registra una retractación del editor '
     '(10.1057/s41599-026-06602-8, 03/02/2026) y el título empieza por «RETRACTED ARTICLE»'),
]

TIPOS = {'journal-article': 'Artículo de revista', 'proceedings-article': 'Artículo de conferencia',
         'book-chapter': 'Capítulo de libro', 'posted-content': 'Preprint', 'report': 'Informe técnico',
         'monograph': 'Libro', 'book': 'Libro', 'Text': 'Preprint o documento de trabajo', 'Preprint': 'Preprint'}


def load(name):
    with open(os.path.join(DATOS, name), encoding='utf-8') as f:
        return json.load(f)


def limpio(t):
    # DataCite entrega el apóstrofo de S42 como carácter de reemplazo (U+FFFD); se repone el apóstrofo.
    t = str(t or '').replace('�', "'")
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t)).strip()


def write(name, text):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('escrito', name)


def cell(x):
    return str(x).replace('|', '\\|').replace('\n', '<br>')


def table(headers, rows):
    L = ['| ' + ' | '.join(headers) + ' |', '|' + '---|' * len(headers)]
    return L + ['| ' + ' | '.join(cell(c) for c in r) + ' |' for r in rows] + ['']


# ------------------------------------------------------------------ referencias
def iniciales(given):
    return ' '.join(p[0] + '.' for p in re.split(r'[\s-]+', given) if p)


CONTENEDORES = {'clr': 'California Law Review'}  # abreviatura que DataCite registra como editorial


def lista_autores(r):
    """DataCite a veces entrega varios autores en una sola cadena separada por «; »."""
    out = []
    for a in r.get('autores') or []:
        out += [x.strip() for x in a.split(';') if x.strip()]
    return [(a.split(', ', 1)[0].title() + ', ' + a.split(', ', 1)[1]) if ', ' in a and a.split(', ', 1)[0].isupper()
            else a for a in out]


def autor(a):
    if ', ' in a:
        fam, giv = a.split(', ', 1)
        return f'{fam}, {iniciales(giv)}'
    return a


def autores(lista):
    xs = [autor(a) for a in lista if a]
    if not xs:
        return ''
    if len(xs) > 6:
        return ', '.join(xs[:6]) + ' et al.'
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' y ' + xs[-1]


def corta(r):
    xs = lista_autores(r)
    fam = [a.split(', ')[0] for a in xs if a]
    if not fam:
        return limpio(r.get('titulo'))[:40]
    base = fam[0] if len(fam) == 1 else (f'{fam[0]} y {fam[1]}' if len(fam) == 2 else f'{fam[0]} et al.')
    return f'{base} ({r.get("anio")})'


def tipo(r, fid):
    if fid.startswith('O') and r.get('registro') == 'HTTP':
        return 'Norma o documento oficial'
    if fid.startswith('X'):
        return 'Fuente secundaria'
    doi = (r.get('doi') or '').lower()
    if 'ssrn' in doi:
        return 'Documento de trabajo (SSRN)'
    if 'arxiv' in doi:
        return 'Preprint (arXiv)'
    if r.get('registro') == 'DataCite':
        return {'ConferencePaper': 'Artículo de conferencia', 'Text': 'Artículo de revista'}.get(r.get('tipo'),
                                                                                                r.get('tipo'))
    return TIPOS.get(r.get('tipo'), r.get('tipo') or '')


# Referencia de normas y páginas sin DOI: emisor, año y título oficial. La URL y su verificación vienen de los datos.
REF_OFICIAL = {
    'O01': 'Parlamento Europeo y Consejo de la Unión Europea. (2024). *Reglamento (UE) 2024/1689, por el que se '
           'establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia '
           'Artificial)*. Diario Oficial de la Unión Europea.',
    'O02': 'Parlamento Europeo y Consejo de la Unión Europea. (2016). *Reglamento (UE) 2016/679, relativo a la '
           'protección de las personas físicas en lo que respecta al tratamiento de datos personales (Reglamento '
           'general de protección de datos)*. Diario Oficial de la Unión Europea.',
    'O05': 'ISO/IEC. (2023). *ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management '
           'system*.',
    'O06': 'ISO/IEC. (2023). *ISO/IEC 23894:2023 Information technology — Artificial intelligence — Guidance on risk '
           'management*.',
    'O07': 'OCDE. (s. f.). *OECD AI Principles* (Recomendación del Consejo sobre Inteligencia Artificial).',
    'O08': 'UNESCO. (2021). *Recomendación sobre la ética de la inteligencia artificial*.',
    'O09': 'Ministerio de Justicia y Derechos Humanos. (2024). *Decreto Supremo N.° 016-2024-JUS, que aprueba el '
           'Reglamento de la Ley N.° 29733, Ley de Protección de Datos Personales*.',
    'O10': 'Congreso de la República del Perú. (2023). *Ley N.° 31814, Ley que promueve el uso de la inteligencia '
           'artificial en favor del desarrollo económico y social del país*.',
    'O11': 'Estados Unidos. *29 CFR Part 1607 — Uniform Guidelines on Employee Selection Procedures (1978)*. Code of '
           'Federal Regulations, edición 2017 (govinfo).',
    'O12': 'Ciudad de Nueva York, Department of Consumer and Worker Protection. (s. f.). *Automated Employment '
           'Decision Tools (AEDT)* (Local Law 144 of 2021).',
    'O13': 'Presidencia del Consejo de Ministros. (2025). *Decreto Supremo N.° 115-2025-PCM, que aprueba el '
           'Reglamento de la Ley N.° 31814*. El Peruano, 9 de setiembre de 2025.',
    'O14': 'Ministerio de Educación del Perú. (2012). *Marco de Buen Desempeño Docente* (RM N.° 0547-2012-ED).',
    'O15': 'Congreso de la República del Perú. (2011). *Ley N.° 29733, Ley de Protección de Datos Personales* '
           '(3 de julio de 2011).',
    'O16': 'Parlamento Europeo y Consejo de la Unión Europea. (2026). *Reglamento (UE) 2026/1744, de 8 de julio de '
           '2026, por el que se modifican los Reglamentos (UE) 2024/1689, (UE) 2018/1139 y (UE) 2023/1230 en lo que '
           'respecta a la simplificación de la aplicación de normas armonizadas en materia de inteligencia artificial '
           '(Digital Omnibus on AI)*. Diario Oficial de la Unión Europea, serie L, 24 de julio de 2026.',
    'X01': 'EU Artificial Intelligence Act (sitio informativo, no oficial). (s. f.). *Annex III: High-Risk AI Systems '
           'Referred to in Article 6(2)*.',
    'X02': 'Gibson Dunn. (s. f.). *EU AI Act Omnibus Agreement — Postponed High-Risk Deadlines and Other Key '
           'Changes* (análisis de un despacho de abogados).',
}


def contenedor(r):
    c = limpio(r.get('contenedor'))
    return CONTENEDORES.get(c, c)


def referencia(fid, r):
    if r.get('doi'):
        cont = contenedor(r) or limpio(r.get('editorial'))
        return (f'{autores(lista_autores(r))} ({r.get("anio")}). {limpio(r.get("titulo")).rstrip(".")}. '
                + (f'*{cont}*. ' if cont else '') + f'https://doi.org/{r["doi"]}')
    return f'{REF_OFICIAL[fid]} {r["url"]} (consultado el {VER["fecha"]})'


# ------------------------------------------------------------------ matriz
def busqueda_md(bus):
    L = ['## 1. Estrategia de búsqueda', '',
         f'- **Base de búsqueda:** OpenAlex (API pública, {bus["fecha"]}), elegida por indexar Crossref, PubMed, arXiv '
         'y repositorios, y por devolver resúmenes; Crossref respondió con límite de tasa (HTTP 429) en búsquedas '
         'masivas, por eso se usó solo para verificar.',
         '- **Verificación:** Crossref para cada DOI (metadatos y avisos de retractación, corrección o retirada), '
         'DataCite para DOI de arXiv y SSRN, y respuesta HTTP con palabra clave esperada en el título para normas y '
         'páginas oficiales (`verificar.py`).',
         f'- **Criterio de cribado:** {bus["criterio"]}.',
         '- **Inclusión:** trabajo revisado por pares, metaanálisis, revisión sistemática, norma oficial o trabajo '
         'fundacional muy citado; relación directa con un tema A–T; resumen o texto que permita extraer los campos.',
         '- **Exclusión:** sin DOI ni URL verificable, retractado, duplicado, opinión sin método, o tema solo '
         'tangencial (p. ej., IA en reclutamiento de pacientes clínicos, que aparece mucho al buscar «recruitment»).',
         '- **Bola de nieve:** trabajos citados por los seleccionados y trabajos fundacionales que la búsqueda por '
         'relevancia no devuelve en los 25 primeros (p. ej., metaanálisis de validez de la entrevista).',
         '- **Búsqueda complementaria:** consultas dirigidas a 2021–2025 para cubrir huecos (alucinación de Whisper, '
         'sesgo de LLM en contratación, calificación automática de respuestas abiertas, entrevistas multimodales).',
         '']
    orig = collections.Counter(o for i, _, _, _, o in FUENTES if i.startswith('S'))
    otros = [(i, o) for i, _, _, _, o in FUENTES if not i.startswith('S') and o.startswith('búsqueda')]
    rows = []
    for t in bus['temas']:
        rows.append([t['codigo'], t['tema'], f'`{t["consulta"]}`', f'{t["total"]:,}'.replace(',', ' '),
                     len(t['cribados']), orig.get('búsqueda ' + t['codigo'], 0)])
    L += ['### Consultas', ''] + table(['Tema', 'Nombre', 'Consulta', 'Resultados', 'Cribados',
                                        'Trabajos seleccionados'], rows)
    L += ['Además, ' + ' y '.join(f'{i} ({o.split()[-1]})' for i, o in otros) + ' son documentos oficiales que '
          'aparecieron en el cribado; se cuentan entre las normas y no entre los trabajos.', '']
    dois = [c.get('doi') for t in bus['temas'] for c in t['cribados']]
    unicos = len({d for d in dois if d})
    n_bus = sum(v for k, v in orig.items() if k.startswith('búsqueda ') and k != 'búsqueda complementaria')
    n_s = sum(1 for f in FUENTES if f[0].startswith('S'))
    s_orig = orig
    L += ['### Flujo de selección', '',
          '```',
          f'Resultados devueltos por las 20 consultas ........ {sum(t["total"] for t in bus["temas"]):,}'.replace(',', ' '),
          f'Cribados (25 primeros por consulta) ............... {len(dois)} registros, {unicos} DOI únicos',
          f'  seleccionados desde el cribado .................. {n_bus}',
          '  excluidos del cribado ........................... resto (fuera de tema, sin método, duplicados,',
          f'                                                     {len(EXCLUIDAS)} retractado)',
          f'Búsqueda complementaria 2021–2025 ................. {s_orig.get("búsqueda complementaria", 0)}',
          f'Bola de nieve y trabajos fundacionales ............ {s_orig.get("bola de nieve", 0)}',
          f'Trabajos científicos en la matriz (S01–S{n_s}) ...... {n_s}',
          f'Normas y documentos oficiales (O01–O{sum(1 for f in FUENTES if f[0].startswith("O")):02d}) ........... '
          f'{sum(1 for f in FUENTES if f[0].startswith("O"))}',
          f'Fuentes secundarias de contraste (X01–X02) ........ {sum(1 for f in FUENTES if f[0].startswith("X"))}',
          f'Total verificado ................................... {sum(1 for v in VER["fuentes"].values() if v.get("verificado"))} de {len(FUENTES)}',
          '```', '',
          'El cribado fue por título, tipo y revista; la extracción de campos se hizo sobre el resumen publicado '
          '(OpenAlex). Los conteos «Resultados» son los que devuelve OpenAlex para la consulta y no equivalen a '
          'trabajos pertinentes: solo indican el tamaño del área.', '']
    return L


def matriz_md():
    bus = load('busqueda_openalex.json')
    L = ['# F30 — Matriz de evidencia científica', '',
         '> Documento generado por `docs/academico/tools/f30/f30.py` desde `fuentes.py`, `m_matriz.py` y los datos '
         'verificados de `datos/`. No se edita a mano.', '',
         '**Cómo leer la matriz.** Cada ficha separa cuatro tipos de afirmación:', '',
         '- **Evidencia científica:** «Resultados relevantes», tomado del resumen publicado del trabajo. Si el trabajo '
         'no tiene resumen disponible, se indica y no se dan cifras.',
         '- **Recomendación de los autores:** cuando el resultado es una propuesta o guía, se escribe como tal.',
         '- **Inferencia del equipo:** «Aplicabilidad al caso».',
         '- **Decisión de ingeniería:** «Decisión que respalda». Las decisiones finales están en '
         '[F30_Recomendaciones_F33_F40.md](F30_Recomendaciones_F33_F40.md).', '',
         '**Niveles de evidencia** (sobre el aporte de la fuente a la decisión, no sobre su prestigio):', '']
    L += table(['Nivel', 'Significado'], [
        ['FUERTE', 'Metaanálisis, revisión amplia o resultado formal o experimental robusto y replicado'],
        ['MODERADA', 'Estudio empírico sólido, revisión sistemática o guía ampliamente adoptada, con límites de '
                     'contexto'],
        ['LIMITADA', 'Estudio único, caso de aplicación o contexto muy distinto del caso'],
        ['CONFLICTIVA', 'Resultados que otras fuentes de la matriz contradicen o matizan'],
        ['INSUFICIENTE', 'No hay datos suficientes para extraer resultados (p. ej., sin resumen disponible)']])
    L += busqueda_md(bus)

    cnt = collections.Counter(m['confianza'] for m in MATRIZ.values())
    L += ['## 2. Resumen de la matriz', '', 'Distribución por nivel: ' +
          ', '.join(f'{n} {cnt.get(n, 0)}' for n in NIVELES) + '.', '']
    rows = []
    for fid, doi, url, tema, origen in FUENTES:
        if not fid.startswith('S'):
            continue
        r, m = VER['fuentes'][fid], MATRIZ[fid]
        rows.append([fid, corta(r), tema, tipo(r, fid), m['revision'], m['confianza']])
    L += table(['ID', 'Referencia', 'Tema', 'Tipo', 'Revisión por pares', 'Nivel'], rows)

    L += ['## 3. Fichas de evidencia', '']
    for fid, doi, url, tema, origen in FUENTES:
        if not fid.startswith('S'):
            continue
        r, m = VER['fuentes'][fid], MATRIZ[fid]
        avisos = ', '.join(r.get('avisos') or []) or 'ninguno'
        L += [f'### {fid} — {corta(r)}', '']
        L += table(['Campo', 'Contenido'], [
            ['Referencia', referencia(fid, r)],
            ['Año', r.get('anio')],
            ['Autores', autores(lista_autores(r))],
            ['Revista o conferencia', contenedor(r) or '—'],
            ['DOI / URL', f'https://doi.org/{doi}'],
            ['Tipo de publicación', tipo(r, fid)],
            ['Revisión por pares', m['revision']],
            ['Tema y origen', f'{tema} · {origen}'],
            ['Avisos de Crossref', avisos],
            ['Objetivo', m['objetivo']],
            ['Datos o población', m['datos']],
            ['Técnica', m['tecnica']],
            ['Variables o características', m['variables']],
            ['Métricas', m['metricas']],
            ['Resultados relevantes (evidencia)', m['resultados']],
            ['Limitaciones', m['limitaciones']],
            ['Riesgos de sesgo', m['sesgo']],
            ['Aplicabilidad al caso (inferencia del equipo)', m['aplicabilidad']],
            ['Decisión que respalda (decisión de ingeniería)', m['decision']],
            ['Nivel de confianza', m['confianza']]])

    L += ['## 4. Normas, documentos oficiales y fuentes secundarias', '',
          'Para las normas no aplican campos como métricas o población: se registra qué establecen, si aplican al '
          'caso y qué decisión motivan. Esto no es asesoría legal: la evaluación de impacto la valida una persona con '
          'competencia jurídica.', '',
          '- **Normas de la UE (O01, O02, O16):** EUR-Lex responde 202 a clientes automáticos; su texto se verificó en '
          'la versión oficial del Diario Oficial que sirve la Oficina de Publicaciones de la UE.',
          '- **DS 115-2025-PCM (O13):** la ficha oficial en gob.pe está verificada y el **art. 24.1 e) está '
          'corroborado**. El texto de los demás artículos citados (24, incluidos sus incisos b) e i); 23, 25, 28.11, 30 '
          'y 31) se leyó en la copia en PDF de la publicación en El Peruano que difunde el portal jurídico LP Derecho. '
          '**Requieren contraste artículo por artículo con la publicación normativa oficial antes de producir efectos '
          'jurídicos.**', '']
    rows = []
    for fid, doi, url, tema, origen in FUENTES:
        if fid.startswith('O'):
            nombre, establece, aplica, decision = OFICIALES[fid]
            rows.append([fid, nombre, establece, aplica, decision, 'Sí' if VER['fuentes'][fid]['verificado']
                         else 'No'])
    L += table(['ID', 'Documento', 'Qué establece (relevante)', 'Aplicabilidad', 'Decisión que motiva',
                'Verificado'], rows)
    L += ['Fuentes secundarias (solo para contrastar, nunca como única base de una afirmación):', '']
    L += table(['ID', 'Página', 'Uso'], [
        ['X01', limpio(VER['fuentes']['X01'].get('titulo_pagina')), 'Lectura del Anexo III y del art. 5 de la Ley '
         'de IA cuando EUR-Lex no entrega el texto a clientes automáticos'],
        ['X02', limpio(VER['fuentes']['X02'].get('titulo_pagina')), 'Contexto del acuerdo político del Digital '
         'Omnibus. **Sustituida** para fechas por la fuente oficial O16 (Reglamento (UE) 2026/1744), con la que '
         'coincide en el aplazamiento al 2/12/2027 de las obligaciones del Anexo III']])

    L += ['## 5. Avisos editoriales y exclusiones', '']
    avis = [[fid, corta(VER['fuentes'][fid]), ', '.join(VER['fuentes'][fid]['avisos'])]
            for fid in VER['fuentes'] if VER['fuentes'][fid].get('avisos')]
    L += ['Fuentes incluidas con avisos (corrección o errata; ninguna retractada):', '']
    L += table(['ID', 'Referencia', 'Aviso'], avis)
    L += ['Fuentes excluidas tras la verificación:', '']
    L += table(['DOI', 'Tema', 'Motivo'], [[f'https://doi.org/{d}', t, m] for d, t, m in EXCLUIDAS])
    return '\n'.join(L).rstrip() + '\n'


def referencias_md():
    L = ['# F30 — Referencias', '',
         f'> Generado por `docs/academico/tools/f30/f30.py` desde `datos/verificacion_fuentes.json` (verificación del '
         f'{VER["fecha"]}). Autores, año, título y revista salen de Crossref o DataCite, no de memoria. Formato basado '
         'en APA 7 (más de seis autores: los seis primeros y «et al.»).', '']
    grupos = [('Trabajos científicos', 'S'), ('Normas y documentos oficiales', 'O'), ('Fuentes secundarias', 'X')]
    for titulo, pref in grupos:
        L += [f'## {titulo}', '']
        for fid, *_ in FUENTES:
            if fid.startswith(pref):
                r = VER['fuentes'][fid]
                L += [f'- **[{fid}]** {referencia(fid, r)}']
        L += ['']
    return '\n'.join(L).rstrip() + '\n'


# ------------------------------------------------------------------ herramientas
NECESIDADES = [
    ('Modelo base (si F36 lo justifica)', ['scikit-learn', 'InterpretML (EBM)', 'XGBoost', 'LightGBM', 'CatBoost']),
    ('Explicabilidad', ['SHAP', 'LIME', 'InterpretML (EBM)']),
    ('Equidad', ['Fairlearn', 'AIF360']),
    ('Registro de modelos y experimentos', ['MLflow']),
    ('Versionado y validación de datos', ['DVC', 'Pandera', 'Great Expectations']),
    ('Monitoreo y deriva', ['Evidently']),
    ('Texto, entidades y anonimización', ['spaCy', 'Microsoft Presidio', 'Hugging Face Transformers']),
    ('Similitud semántica y búsqueda vectorial', ['sentence-transformers', 'pgvector', 'FAISS', 'Qdrant']),
    ('Voz a texto y diarización', ['Whisper (OpenAI)', 'faster-whisper', 'whisper.cpp', 'Vosk', 'pyannote.audio',
                                   'FFmpeg']),
    ('Documentos (PDF, DOCX, OCR)', ['pypdf', 'pdfplumber', 'python-docx', 'PyMuPDF', 'Docling', 'Unstructured',
                                     'Apache Tika', 'Tesseract OCR']),
    ('Cuadernos y reproducibilidad', ['JupyterLab', 'nbstripout']),
    ('Seguridad de dependencias', ['pip-audit', 'OSV-Scanner']),
    ('LLM local', ['Ollama']),
    ('Bibliografía y diagramas', ['Zotero', 'Better BibTeX for Zotero', 'Mermaid']),
    ('Servidores MCP', ['MCP Reference Servers (fetch, filesystem, git)', 'GitHub MCP Server',
                        'Hugging Face MCP Server', 'arXiv MCP Server', 'Zotero MCP', 'Context7 MCP']),
]


def transferidos(por):
    xs = [f'{n} (`{h["repo"]}` → `{h["github"]["nombre"]}`)' for n, h in por.items()
          if h['github'].get('redirigido')]
    return 'GitHub redirige ' + str(len(xs)) + ' repositorios a otro propietario: ' + ', '.join(xs)


def herramientas_md():
    H = load('herramientas.json')
    por = {h['nombre']: h for h in H['herramientas']}
    faltan = sorted(set(CLASIFICACION) ^ set(por))
    assert not faltan, faltan
    pend = [n for n, h in por.items() if not h['github'].get('existe')]
    L = ['# F30 — Análisis de herramientas, skills y servidores MCP', '',
         '> Datos generados por `docs/academico/tools/f30/f30.py` desde `datos/herramientas.json` (consultas a la API '
         'de GitHub, PyPI, npm y OSV con `herramientas.py`) y la clasificación de `m_herramientas.py`. **En F30 no '
         'se instaló nada**: ni paquetes, ni skills, ni servidores MCP.', '',
         '## 1. Método', '',
         '- **Datos objetivos por herramienta:** existencia y propietario del repositorio, licencia, archivado, última '
         'actividad, estrellas; versión y fecha en el registro del paquete; avisos de seguridad en OSV, tanto el total '
         'histórico como los que afectan a la última versión publicada.',
         '- **Clasificación:** RECOMENDADO, EVALUAR EN SANDBOX, NO NECESARIO o EVITAR, según necesidad real en '
         'F33–F40, evidencia de la matriz, licencia, mantenimiento, avisos y superficie de ataque.',
         '- **Un aviso histórico no es una vulnerabilidad actual:** indica cuánta superficie de ataque ha tenido el '
         'proyecto (p. ej., lectores de PDF frente a archivos malformados). Lo que bloquea es un aviso en la versión '
         'que se instalaría.',
         '- **Skills y MCP locales:** inventario de solo lectura de `.claude/skills/`, `~/.claude/skills`, plugins y '
         'conectores visibles en la sesión, revisando archivos, scripts, *hooks*, `allowed-tools` e instrucciones.',
         '']
    if pend:
        L += [f'> **Datos incompletos:** la API de GitHub sin autenticación limita a 60 consultas por hora; faltan los '
              f'datos de repositorio de {len(pend)} herramienta{"s" if len(pend) > 1 else ""} ({", ".join(pend)}). Se completan con '
              '`python docs/academico/tools/f30/herramientas.py --completar`.', '']
    cnt = collections.Counter(c[0] for c in CLASIFICACION.values())
    L += ['## 2. Resultado', '', 'Herramientas evaluadas: ' + str(len(CLASIFICACION)) + '. ' +
          ', '.join(f'{c}: {cnt.get(c, 0)}' for c in CLASES) + '.', '']
    for c in CLASES:
        L += [f'- **{c}:** ' + ', '.join(n for n, v in CLASIFICACION.items() if v[0] == c) + '.']
    L += ['']

    L += ['## 3. Comparación por necesidad', '']
    for nec, nombres in NECESIDADES:
        L += [f'### {nec}', '']
        rows = []
        for n in nombres:
            cl, fase, just, riesgo = CLASIFICACION[n]
            rows.append([n, cl, fase, just, riesgo])
        L += table(['Herramienta', 'Clasificación', 'Fase', 'Justificación', 'Condición o riesgo'], rows)

    L += ['## 4. Datos verificados por herramienta', '',
          f'Consulta del {H["fecha"]} (cada herramienta registra su fecha en `datos/herramientas.json`).', '']
    rows = []
    for nombre, (cl, *_rest) in CLASIFICACION.items():
        h = por[nombre]
        g, reg = h['github'], h.get('registro') or {}
        hist = h.get('osv_historico')
        ult = h.get('osv_ultima_version')
        repo = (g['nombre'] + (' (transferido)' if g.get('redirigido') else '')) if g.get('existe') else h['repo']
        rows.append([nombre, repo,
                     (g.get('licencia') or reg.get('licencia') or '—') if g.get('existe') else 'pendiente',
                     g.get('ultima_actividad', 'pendiente'), g.get('estrellas', 'pendiente'),
                     ('sí' if g.get('archivado') else 'no') if g.get('existe') else 'pendiente',
                     reg.get('version', '—'), '—' if hist is None else len(hist),
                     '—' if ult is None else len(ult), cl])
    L += table(['Herramienta', 'Repositorio', 'Licencia (GitHub)', 'Última actividad', 'Estrellas', 'Archivado',
                'Versión', 'Avisos OSV históricos', 'Avisos en última versión', 'Clasificación'], rows)
    L += ['«—» en avisos: la herramienta no se publica en un ecosistema que OSV indexe con ese nombre (p. ej., '
          'binarios o extensiones); no significa cero avisos. «NOASSERTION» o «Other»: GitHub no reconoce la licencia '
          'automáticamente; se revisa el archivo de licencia antes de adoptar.', '']

    L += ['## 5. Skills, plugins y conectores del entorno local', '',
          'Inventario de solo lectura del 30/09/2026. Las skills del proyecto son Markdown sin scripts, *hooks* ni '
          'acceso de red; las tres externas tienen `PROVENANCE.md` con origen, commit fijado, licencia y auditoría. '
          'No hay *hooks* configurados en `.claude/settings.local.json` ni en la configuración de usuario.', '']
    L += table(['Skill o plugin', 'Origen', 'Contenido', 'Clasificación', 'Uso o motivo'],
               [list(s) for s in SKILLS_LOCALES])
    L += ['Conectores MCP visibles en la sesión: Claude Docs, Canva y Google Drive (claude.ai), y los del plugin '
          '*engineering* (Asana, Atlassian, Datadog, GitHub, Linear, Notion, PagerDuty, Slack) sin autenticar. '
          'Ninguno es necesario para F33–F40 y **ninguno debe recibir datos de postulantes**, ni siquiera ficticios '
          'que imiten datos reales. Clasificación: NO NECESARIO.', '',
          '**Hallazgos de la revisión de skills:**', '',
          '- Ninguna skill del proyecto contiene scripts, binarios, *hooks* ni instrucciones de leer `.env`, enviar '
          'datos o saltar confirmaciones.',
          '- `reviewing-a11y` declara en `allowed-tools` WebFetch y herramientas de un MCP de Playwright que no está '
          'instalado. No es malicioso, pero instalar ese MCP ampliaría lo que la skill puede hacer sin confirmación: '
          'requiere autorización del equipo.',
          '- Las skills sincronizadas `docx`, `pdf`, `pptx` y `xlsx` incluyen scripts Python que se ejecutan en local; '
          'su origen es Anthropic. Se revisan antes de ejecutarlos sobre documentos con datos.',
          '- No se detectaron skills sospechosas. La sección siguiente fija los criterios para las que se propongan '
          'después.', '']

    L += ['## 6. Señales de alerta de cadena de suministro', '',
          'Toda skill, plugin, servidor MCP o paquete que se proponga en F33–F40 se revisa con estas señales antes de '
          'instalarse. Una sola señal grave basta para EVITAR.', '']
    L += table(['Señal', 'Cómo se comprueba'], [list(a) for a in ALERTAS])
    L += ['**Riesgos concretos encontrados en esta evaluación:**', '',
          '- **Licencia:** PyMuPDF es AGPL-3.0: requiere revisión de compatibilidad AGPL o licencia comercial '
          '(EVITAR por prudencia). '
          'FFmpeg es LGPL con componentes GPL opcionales.',
          '- **Superficie de ataque:** los lectores de PDF (pypdf, PyMuPDF) y las plataformas con servidor (MLflow, '
          'JupyterLab) acumulan muchos avisos históricos: si se usan, en proceso aislado con límites.',
          '- **Pesos de modelos:** Transformers, sentence-transformers y Whisper descargan pesos de terceros; solo '
          'formatos sin ejecución (*safetensors*) y revisiones fijadas.',
          '- **Datos biométricos:** la diarización con embeddings de voz (pyannote.audio) trata datos biométricos '
          '(EVITAR).',
          '- **Mantenimiento:** LIME sin actividad desde julio de 2024 (EVITAR).',
          '- **Cambio de propietario:** ' + transferidos(por) + '. Puede ser un cambio legítimo (reorganización o '
          'adquisición), pero es justo la señal que explota un ataque de cadena de suministro: antes de adoptar '
          'cualquiera de ellos se comprueba en el registro del paquete quién publica las versiones y desde qué '
          'repositorio.',
          '- **Credenciales y envío a terceros:** Zotero MCP (clave de API y acceso a la biblioteca) y Context7 '
          '(consultas a un servicio externo).',
          '- **Inyección de prompt:** cualquier MCP que traiga contenido externo (fetch, arXiv, Hugging Face) puede '
          'incluir instrucciones; ese contenido es dato, nunca orden.', '',
          '## 7. Reglas de adopción para F33–F40', '',
          '1. Regla G0 ([F30_Recomendaciones_F33_F40.md](F30_Recomendaciones_F33_F40.md#2-puerta-g0)): en F35–F40 '
          'ninguna herramienta se instala sin G0 aprobado; en F33–F34, solo en sandbox, con datos sintéticos y '
          'autorización explícita.',
          '2. Toda dependencia nueva de producción requiere autorización explícita del equipo (skill '
          '`project-guardian`).',
          '3. Versión fijada, licencia revisada, `pip-audit` u OSV-Scanner sin avisos en esa versión.',
          '4. Primero en un entorno aislado con datos ficticios; sin red de producción ni credenciales reales.',
          '5. Ninguna herramienta de terceros recibe datos de postulantes reales.', '']
    return '\n'.join(L).rstrip() + '\n'


# ------------------------------------------------------------------ consolidado Word
ORDEN = ['README.md', 'F30_Estado_del_Arte_IA_Reclutamiento.md', 'F30_Analisis_Modelos_y_Tecnicas.md',
         'F30_Explainability_Fairness_Gobernanza.md', 'F30_Analisis_Herramientas_Skills.md',
         'F30_Recomendaciones_F33_F40.md', 'F30_Matriz_Evidencia_Cientifica.md', 'REFERENCIAS.md']


def inline(t):
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1 (\2)', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'(?<![*\w])\*([^*\n]+)\*(?![*\w])', r'\1', t)
    return t.replace('<br>', '\n')


def codigo_xml(lines):
    """Bloque de código: una línea por párrafo, en monoespaciada y sin espacio entre líneas."""
    from xml.sax.saxutils import escape
    return ''.join('<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:rPr>'
                   '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="15"/></w:rPr>'
                   f'<w:t xml:space="preserve">{escape(ln)}</w:t></w:r></w:p>' for ln in lines) + \
        '<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>'


def md_blocks(md):
    """Markdown sencillo → bloques de docxpkg. # = capítulo (h1); ## = h2; ### = párrafo en negrita."""
    blocks, para, lst, tbl, code = [], [], [], [], None
    def flush():
        nonlocal para, lst, tbl
        if para:
            blocks.append(('p', inline(' '.join(para))))
        if lst:
            blocks.append(('ul', [inline(x) for x in lst]))
        if tbl:
            hdr, rows = tbl[0], tbl[2:]
            n = len(hdr)
            fr = [1 / n] * n
            if n == 2:
                fr = [0.28, 0.72]
            blocks.append(('table', [inline(h) for h in hdr], [[inline(c) for c in r] for r in rows], fr,
                           16 if n <= 4 else 13))
        para, lst, tbl = [], [], []

    def cells(line):
        return [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]

    for line in md.split('\n'):
        if line.startswith('```'):
            flush()
            if code is None:
                code = []
            else:
                blocks.append(('raw', codigo_xml(code)))
                code = None
            continue
        if code is not None:
            code.append(line)
            continue
        s = line.strip()
        if not s:
            flush()
        elif s.startswith('|'):
            if para or lst:
                p, l2 = para, lst
                para, lst = [], []
                if p:
                    blocks.append(('p', inline(' '.join(p))))
                if l2:
                    blocks.append(('ul', [inline(x) for x in l2]))
            tbl.append(cells(s))
        elif s.startswith('# '):
            flush()
            blocks.append(('h1', inline(s[2:])))
        elif s.startswith('## '):
            flush()
            blocks.append(('h2', inline(s[3:])))
        elif s.startswith('### ') or s.startswith('#### '):
            flush()
            blocks.append(('p', '**' + inline(s.lstrip('#').strip()) + '**'))
        elif s.startswith('> '):
            flush()
            blocks.append(('note', inline(s[2:])))
        elif re.match(r'^(-|\d+\.) ', s):
            if para:
                blocks.append(('p', inline(' '.join(para))))
                para = []
            lst.append(re.sub(r'^(-|\d+\.) ', '', s))
        elif lst and line.startswith('  '):
            lst[-1] += ' ' + s
        else:
            para.append(s)
    flush()
    return blocks


def docx():
    from docxpkg import write_docx
    blocks = [('h1', 'Contenido'), ('toc',), ('pagebreak',)]
    for i, name in enumerate(ORDEN):
        with open(os.path.join(OUT, name), encoding='utf-8') as f:
            b = md_blocks(f.read())
        if i:
            blocks.append(('pagebreak',))
        blocks += b
    # La tabla de contenido no lista su propio título.
    path = os.path.join(OUT, 'F30_Investigacion_IA_Reclutamiento.docx')
    write_docx(path, blocks, 'F30 — Investigación científica y tecnológica para el motor inteligente de '
               'reclutamiento', 'Coronacion Meza, Peña Arroyo, Vila Meza',
               header=('Área Informática', 'Pruebas y Calidad de Software — NRC 28607'),
               cover=('F30 — Investigación científica y tecnológica para el motor inteligente de reclutamiento',
                      'SaaS Reclutamiento Multiempresa · Caso Colegio Andino de Huancayo',
                      'Versión 1 · 30/09/2026 · auditada e integrada'),
               footer_extra='F30 — Investigación IA reclutamiento')
    print('escrito', os.path.basename(path))


VER = load('verificacion_fuentes.json')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    write('F30_Matriz_Evidencia_Cientifica.md', matriz_md())
    write('REFERENCIAS.md', referencias_md())
    write('F30_Analisis_Herramientas_Skills.md', herramientas_md())
    if '--sin-docx' not in sys.argv:
        docx()
