"""F34A — Validación de los prerequisitos de G0 (solo biblioteca estándar).

Comprueba que los documentos de docs/academico/g0-readiness/:
  AP  no afirman aprobaciones inexistentes (G0, ADR-005, revisión jurídica, datos reales, F35–F40);
  MG  la matriz G0 tiene los 15 criterios, estados válidos y ningún criterio externo CUMPLIDO;
  ADR el registro de decisión del ADR-005 sigue PENDIENTE y no tiene decisiones sin nombre ni fecha;
  JUR el checklist jurídico usa solo VERIFICADO / LECTURA PRELIMINAR / REQUIERE ABOGADO/RESPONSABLE LEGAL;
  PRI el análisis de privacidad cubre los temas exigidos y mantiene la prohibición de datos reales;
  NEC el instrumento de necesidad no tiene respuestas inventadas;
  TM  el modelo de amenazas cubre STRIDE y las amenazas obligatorias;
  RF  los RF candidatos no contaminan el baseline;
  GOV RF-23 humana, RF-29 experimental, F35–F40 bloqueadas;
  LNK enlaces y anclas;
  EIA una evaluación de impacto planificada no cierra G0-02 (COMPLETADA o NO APLICABILIDAD documentada);
  AUD la auditoría conserva usuario e IP: sin «sin PII» absoluto ni anonimato afirmado;
  RANK el nuevo motor no ordena personas, pero RF-21 vigente mantiene su ranking;
  TOK las rutas /v1/* del servicio ML fallan cerrado; el token no es opcional;
  ROLE ningún rol no implementado se presenta como vigente;
  XSS amenaza explícita de XSS persistente con sus controles;
y además que el baseline, ADR-005, el runtime y las dependencias no cambiaron respecto de develop.
Los casos negativos (QA) mutan los textos en memoria: cada uno debe ser detectado.
Uso: python docs/academico/tools/f34a/validate_f34a.py
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DOCS = os.path.join(ROOT, 'docs', 'academico', 'g0-readiness')
BASE = 'develop'
FILES = ['README.md', 'F34A_Matriz_G0.md', 'F34A_Paquete_Aprobacion_ADR005.md', 'F34A_Checklist_Revision_Juridica.md',
         'F34A_Analisis_Privacidad_Preliminar.md', 'F34A_Validacion_Necesidad_Institucional.md',
         'F34A_Modelo_de_Amenazas.md', 'F34A_RF_Candidatos.md', 'F34A_Decision_Readiness_G0.md']
STATES = {'CUMPLIDO', 'PARCIAL', 'PENDIENTE EXTERNO', 'BLOQUEADO', 'NO APLICA'}
EXTERNAL = {'G0-02', 'G0-03', 'G0-12', 'G0-14'}          # dependen de abogado, responsable, institución o decisión del equipo
JUR_STATES = {'VERIFICADO', 'LECTURA PRELIMINAR', 'REQUIERE ABOGADO/RESPONSABLE LEGAL'}
ADR_DECISIONS = {'PENDIENTE', 'APRUEBA', 'APRUEBA CON OBSERVACIONES', 'RECHAZA'}
NEG = re.compile(r'\b(no|ni|sin|nunca|ningún|ninguna|nada)\b', re.I)

# Afirmaciones prohibidas. «estricta»: falla siempre; «blanda»: falla salvo que la línea la niegue.
CLAIMS = [
    ('G0 aprobada', re.compile(r'G0\s*=\s*\**\s*APROBADA', re.I), True),
    ('G0 aprobada', re.compile(r'G0 (?:fue|ha sido|está|queda|quedó) aprobada', re.I), False),
    ('ADR-005 aprobado', re.compile(r'ADR-005\s*=\s*\**\s*APROBAD', re.I), True),
    ('ADR-005 aprobado', re.compile(r'ADR-005 (?:fue|ha sido|está|queda|quedó) aprobad', re.I), False),
    ('revisión jurídica aprobada', re.compile(r'revisi[oó]n jur[ií]dica (?:fue |ha sido |está |queda )?'
                                              r'(?:aprobada|favorable|completada|concluida)', re.I), False),
    ('dictamen legal emitido', re.compile(r'dictamen legal (?:emitido|favorable)', re.I), False),
    ('cumplimiento legal afirmado', re.compile(r'(?:cumple|conforme a|cumplimiento de) (?:con )?la (?:Ley|norma)',
                                               re.I), False),
    ('datos reales autorizados', re.compile(r'datos reales (?:quedan|están|son|se) (?:autorizad|permitid|habilitad)',
                                            re.I), False),
    ('candidato en baseline', re.compile(r'(?:pasa|entra|se incorpora|promovid[oa]|forma parte) (?:a|al|del) '
                                         r'baseline', re.I), False),
]


def read_all():
    return {n: open(os.path.join(DOCS, n), encoding='utf-8').read() if os.path.isfile(os.path.join(DOCS, n)) else ''
            for n in FILES}


def rows(text, first):
    """Filas de tabla markdown cuya primera celda coincide con la expresión `first`."""
    out = []
    for ln in text.splitlines():
        if ln.startswith('|'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if cells and re.fullmatch(first, cells[0]):
                out.append(cells)
    return out


def plain(cell):
    return re.sub(r'\s*\(.*?\)\s*', ' ', cell.replace('**', '')).strip()


# ---------------------------------------------------------------- reglas
def ap(D):
    out = []
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            for what, rx, strict in CLAIMS:
                if not rx.search(ln):
                    continue
                if strict or not NEG.search(ln):
                    out.append(f'{n}:{i}: afirma «{what}»: {ln.strip()[:90]}')
    return out


def mg(D):
    t = D['F34A_Matriz_G0.md']
    rs = rows(t, r'G0-\d\d')
    out = []
    ids = [r[0] for r in rs]
    if ids != [f'G0-{i:02d}' for i in range(1, 16)]:
        out.append(f'la matriz no tiene exactamente G0-01..G0-15 en orden: {ids}')
    final = {}
    for r in rs:
        if len(r) != 10:
            out.append(f'{r[0]}: {len(r)} columnas (se esperan 10)')
            continue
        st = plain(r[8])
        final[r[0]] = st
        if st not in STATES:
            out.append(f'{r[0]}: estado final «{st}» no válido')
        if r[0] in EXTERNAL and st == 'CUMPLIDO':
            out.append(f'{r[0]}: criterio que depende de terceros marcado CUMPLIDO')
        if r[5].startswith('No') and st == 'CUMPLIDO':
            out.append(f'{r[0]}: no puede cerrarse en F34A pero figura CUMPLIDO')
        if st == 'CUMPLIDO' and r[3] in ('', '—'):
            out.append(f'{r[0]}: CUMPLIDO sin evidencia disponible')
        if any(c == '' for c in r):
            out.append(f'{r[0]}: celda vacía')
    # resumen coherente con las filas
    for st in STATES:
        m = re.search(r'^\| ' + re.escape(st) + r' \| (.*?) \| (\d+) \|$', t, re.M)
        n = sum(1 for v in final.values() if v == st)
        if not m or int(m.group(2)) != n:
            out.append(f'resumen de la matriz: «{st}» no coincide con las filas ({n})')
    # G0 no puede estar aprobada si falta algún criterio obligatorio
    if any(v not in ('CUMPLIDO', 'NO APLICA') for v in final.values()):
        for n in ('README.md', 'F34A_Decision_Readiness_G0.md'):
            if 'G0 = NO APROBADA' not in D[n]:
                out.append(f'{n}: faltan criterios y no declara «G0 = NO APROBADA»')
    return out


def adr(D):
    t = D['F34A_Paquete_Aprobacion_ADR005.md']
    sec = t.split('## 9. Registro de decisión del equipo')[-1] if '## 9. Registro de decisión del equipo' in t else ''
    out = [] if sec else ['paquete sin sección 9 de registro de decisión']
    regs = [r for r in rows(sec, r'.*') if len(r) == 5 and r[0] not in ('Nombre', '---') and not r[0].startswith('-')]
    if len(regs) < 3:
        out.append('registro de decisión con menos de tres filas')
    decs = []
    for r in regs:
        d = r[3]
        decs.append(d)
        if d not in ADR_DECISIONS:
            out.append(f'decisión no admitida «{d}»')
        if d != 'PENDIENTE' and (r[0] in ('', '—') or r[2] in ('', '—')):
            out.append(f'decisión «{d}» sin nombre o sin fecha (aprobación falsificada)')
    pend = '**Estado actual: PENDIENTE.**' in t
    if all(d == 'PENDIENTE' for d in decs) != pend:
        out.append('el estado del registro no coincide con las decisiones registradas')
    for s in ('**Estado del ADR: PROPUESTA.', 'Estado de la aprobación: PENDIENTE.'):
        if s not in t:
            out.append(f'paquete sin «{s}»')
    for sec_ in ('Resumen ejecutivo', 'Decisión propuesta', 'Alcance B', 'Capacidades excluidas', 'Riesgos',
                 'Consecuencias', 'Condiciones de reversión', 'Relación con F30, F33 y F34'):
        if not re.search(r'^## \d+\. ' + sec_, t, re.M):
            out.append(f'paquete sin sección «{sec_}»')
    return out


def jur(D):
    t = D['F34A_Checklist_Revision_Juridica.md']
    out = [] if 'Esto no es un dictamen legal' in t else ['checklist sin la advertencia «no es un dictamen legal»']
    rs = rows(t, r'J-\d\d')
    ids = [r[0] for r in rs]
    if ids != [f'J-{i:02d}' for i in range(1, len(ids) + 1)] or not ids:
        out.append('puntos J-xx no consecutivos')
    cnt = {s: 0 for s in JUR_STATES}
    for r in rs:
        st = r[2] if len(r) == 4 else ''
        if st not in JUR_STATES:
            out.append(f'{r[0]}: estado «{st}» no admitido')
            continue
        cnt[st] += 1
        if st == 'VERIFICADO' and not re.search(r'\[O\d\d\]', r[3]):
            out.append(f'{r[0]}: VERIFICADO sin fuente oficial [Oxx]')
    for st, n in cnt.items():
        m = re.search(r'^\| ' + re.escape(st) + r' \| .*? \| (\d+) \|$', t, re.M)
        if not m or int(m.group(1)) != n:
            out.append(f'resumen jurídico: «{st}» no coincide con los puntos ({n})')
    for topic in ('DS 115-2025-PCM', 'Ley 29733', 'DS 016-2024-JUS', '2024/1689', 'decisiones automatizadas',
                  'riesgo alto', 'Transparencia', 'supervisión humana', 'conservación', 'transfronterizo'):
        if topic.lower() not in t.lower():
            out.append(f'checklist sin el tema «{topic}»')
    return out


def pri(D):
    t = D['F34A_Analisis_Privacidad_Preliminar.md']
    out = []
    for s in ('**Regla vigente: los datos reales siguen PROHIBIDOS.**',
              '**El consentimiento por sí solo NO levanta el bloqueo.**', '**No afirma cumplimiento legal**',
              '**No hay conclusión de cumplimiento.**'):
        if s not in t:
            out.append(f'privacidad sin «{s}»')
    for topic in ('Finalidad', 'Categorías de datos', 'Necesidad', 'proporcionalidad', 'Minimización', 'Almacenamiento',
                  'Acceso', 'Retención', 'borrado', 'Multitenencia', 'Procedencia', 'Logs', 'Datos sensibles',
                  'Datos de audio', 'Terceros y proveedores', 'Riesgos y mitigaciones'):
        if not re.search(r'^## \d+\. .*' + topic, t, re.M | re.I):
            out.append(f'privacidad sin sección «{topic}»')
    if len(rows(t, r'P-\d\d')) < 8:
        out.append('privacidad con menos de 8 riesgos')
    return out


def nec(D):
    t = D['F34A_Validacion_Necesidad_Institucional.md']
    out = [] if 'PENDIENTE VALIDACIÓN EXTERNA' in t else ['instrumento sin estado PENDIENTE VALIDACIÓN EXTERNA']
    qs = [r for r in rows(t, r'N-\d\d') if len(r) == 3]
    if len(qs) != 10:
        out.append(f'instrumento con {len(qs)} preguntas (se esperan 10)')
    ans = [r for r in rows(t, r'N-\d\d') if len(r) == 5]
    filled = [r[0] for r in ans if any(c not in ('—', '') for c in r[1:])]
    if len(ans) != 10 or filled:
        out.append(f'respuestas registradas sin evidencia real: {filled or len(ans)}')
    part = rows(t, r'Docente|RR\. HH\.|Administración|Representante institucional')
    if any(len(r) == 5 and any(c != '—' for c in r[1:]) for r in part):
        out.append('participantes con nombre, fecha o firma registrados')
    for who in ('Docente', 'RR. HH.', 'Administración', 'Representante institucional'):
        if who not in t:
            out.append(f'instrumento sin el perfil «{who}»')
    for topic in ('problema concreto', 'alcance B', 'rúbricas', 'tiempo adicional', 'riesgos', 'excluir',
                  'ayuda automática'):
        if topic.lower() not in t.lower():
            out.append(f'instrumento sin la pregunta sobre «{topic}»')
    return out


REQUIRED_THREATS = ['Fuga cross-tenant', 'Exfiltración de CV y evidencias', 'Prompt injection futura', 'Poisoning',
                    'Model tampering', 'Data tampering', 'Replay', 'Token leakage', 'Logs con PII',
                    'Manipulación de reglas', 'Abuso de privilegios', 'Disponibilidad']


def tm(D):
    t = D['F34A_Modelo_de_Amenazas.md']
    out = []
    rs = rows(t, r'T-\d\d')
    ids = [r[0] for r in rs]
    if ids != [f'T-{i:02d}' for i in range(1, len(ids) + 1)] or len(ids) < 11:
        out.append(f'amenazas T-xx no consecutivas o insuficientes ({len(ids)})')
    for r in rs:
        if len(r) != 8 or any(c == '' for c in r):
            out.append(f'{r[0]}: fila incompleta')
        elif not set(r[1].split('/')) <= set('STRIDE'):
            out.append(f'{r[0]}: categoría STRIDE inválida «{r[1]}»')
    body = ' '.join(' '.join(r) for r in rs)
    for th in REQUIRED_THREATS:
        if th.lower() not in body.lower():
            out.append(f'falta la amenaza obligatoria «{th}»')
    for sec in ('Activos', 'Actores', 'Superficies y fronteras de confianza', 'Amenazas', 'Resumen'):
        if not re.search(r'^## \d+\. ' + sec, t, re.M):
            out.append(f'modelo sin sección «{sec}»')
    if not re.search(r'STRIDE', t) or len(re.findall(r'^\| TB-\d', t, re.M)) < 5:
        out.append('modelo sin STRIDE o sin fronteras de confianza')
    m = re.search(r'(\d+) amenazas', D['README.md'])
    if not m or int(m.group(1)) != len(ids):
        out.append('el README no coincide con el número de amenazas')
    if 'Solo diseño' not in t:
        out.append('el modelo no declara que es solo diseño')
    return out


def rf(D):
    t = D['F34A_RF_Candidatos.md']
    out = []
    rs = rows(t, r'RF-CAND-\d\d')
    ids = [r[0] for r in rs]
    if ids != [f'RF-CAND-{i:02d}' for i in range(1, len(ids) + 1)] or not ids:
        out.append('RF-CAND-xx no consecutivos')
    for r in rs:
        if not r[-1].startswith('CANDIDATO'):
            out.append(f'{r[0]}: estado «{r[-1]}» (debe ser CANDIDATO)')
    for n, tx in D.items():                           # ningún RF nuevo con número productivo en F34A
        for r in rows(tx, r'RF-(?:2[89]|[3-9]\d)'):
            out.append(f'{n}: define {r[0]} como requisito en una tabla')
    if 'No son requisitos productivos ni forman parte del baseline' not in t:
        out.append('registro sin la advertencia de baseline')
    return out


def gov(D):
    out = []
    for n in ('README.md', 'F34A_Decision_Readiness_G0.md'):
        t = D[n]
        for s in ('F35–F40 = BLOQUEADAS', 'ADR-005 = PROPUESTA', 'RF-23', 'RF-29', 'datos reales siguen PROHIBIDOS'):
            if s.lower() not in t.lower():
                out.append(f'{n}: no declara «{s}»')
        if 'F34A = LISTA PARA AUDITORÍA' not in t:
            out.append(f'{n}: no declara «F34A = LISTA PARA AUDITORÍA»')
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'F3[5-9]|F40', ln) and re.search(r'\b(HABILITAD|DESBLOQUEAD|AUTORIZAD)', ln) \
                    and not re.search(r'BLOQUEAD|NO APROBADA|\b(no|solo con|si)\b', ln, re.I):
                out.append(f'{n}:{i}: declara F35–F40 habilitadas')
        if 'F34A = CERRADA' in t or 'F34A CERRADA' in t:
            out.append(f'{n}: declara F34A cerrada antes de la auditoría')
    return out


def slug(h):
    h = re.sub(r'[`*_]', '', h.strip().lower())
    return re.sub(r'[^\w\- ]', '', h).replace(' ', '-')


def lnk(D):
    out = []
    for n, t in D.items():
        for link in re.findall(r'\]\(([^)\s]+)\)', t):
            if link.startswith(('http://', 'https://')):
                continue
            path, _, anchor = link.partition('#')
            target = os.path.normpath(os.path.join(DOCS, path)) if path else os.path.join(DOCS, n)
            if not os.path.exists(target):
                out.append(f'{n}→{link}')
            elif anchor and target.endswith('.md'):
                src = D.get(os.path.basename(target)) if os.path.dirname(target) == DOCS else None
                src = src if src is not None else open(target, encoding='utf-8').read()
                if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', src, re.M)}:
                    out.append(f'{n}→{link}')
    return out


# ---------------------------------------------------------------- reglas añadidas tras la auditoría F34A
def eia(D):
    """M01: una evaluación de impacto planificada no cierra G0-02."""
    out = []
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'evaluaci[oó]n de impacto', ln, re.I) and re.search(r'planifi', ln, re.I) \
                    and not re.search(r'NO cierra|no basta', ln):
                out.append(f'{n}:{i}: admite una evaluación de impacto planificada como cierre de G0-02')
    for n, where in (('F34A_Checklist_Revision_Juridica.md', None),
                     ('F34A_Decision_Readiness_G0.md', r'^\| S-02 \|.*$'),
                     ('F34A_Matriz_G0.md', r'^\| G0-02 \|.*$')):
        t = D[n]
        if where:
            m = re.search(where, t, re.M)
            t = m.group(0) if m else ''
        for s in ('COMPLETADA', 'NO APLICABILIDAD', 'NO cierra G0-02'):
            if s not in t:
                out.append(f'{n}: la regla de cierre de G0-02 no exige «{s}»')
    if not re.search(r'^## \d+\. Regla de cierre de G0-02', D['F34A_Checklist_Revision_Juridica.md'], re.M):
        out.append('checklist sin la sección «Regla de cierre de G0-02»')
    return out


def aud(D):
    """La auditoría conserva usuario e IP: no se afirma «sin PII» absoluto ni anonimato."""
    out = []
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'audit|AuditLogger', ln, re.I):
                if re.search(r'sin PII(?! innecesaria)', ln):
                    out.append(f'{n}:{i}: afirma auditoría «sin PII» absoluta')
                if re.search(r'\banónim[oa]s?\b', ln, re.I) and not re.search(r'no es (?:un registro )?anónim', ln, re.I):
                    out.append(f'{n}:{i}: afirma anonimato de la auditoría')
    pri_t = D['F34A_Analisis_Privacidad_Preliminar.md']
    for s in ('No es un registro anónimo', 'usuario, organización, acción, objeto e IP', 'minimización y limitación de '
              'propósito'):
        if s not in pri_t:
            out.append(f'privacidad no declara «{s}» sobre la auditoría')
    return out


def rank(D):
    """El nuevo motor no ordena personas; RF-21 vigente sí mantiene su ranking determinista."""
    out = []
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'\b(?:el|del) sistema\b[^.]*\b(?:nunca|no)\b[^.]*\bordena', ln, re.I) \
                    and not re.search(r'nuevo motor|RF-21', ln):
                out.append(f'{n}:{i}: prohíbe ordenar personas al sistema entero (contradice RF-21)')
    for n in ('F34A_Validacion_Necesidad_Institucional.md', 'F34A_RF_Candidatos.md'):
        if not re.search(r'ranking vigente de RF-21[^.]*se mantiene sin cambios', D[n]):
            out.append(f'{n}: no aclara que el ranking vigente de RF-21 se mantiene')
    return out


def tok(D):
    """T-02: las rutas /v1/* fallan cerrado; el token no es opcional."""
    t = D['F34A_Modelo_de_Amenazas.md']
    out = []
    m = re.search(r'^\| T-02 \|.*$', t, re.M)
    row = m.group(0) if m else ''
    if not re.search(r'/v1/\*', row) or not re.search(r'fallan cerrado', row):
        out.append('T-02 no declara que /v1/* fallan cerrado sin credencial')
    for n, tx in D.items():
        for i, ln in enumerate(tx.splitlines(), 1):
            if re.search(r'token', ln, re.I) and re.search(r'opcional', ln, re.I):
                out.append(f'{n}:{i}: describe el token del servicio como opcional')
    return out


IMPLEMENTED_ROLES = {'Postulante', 'Evaluador', 'RR. HH.', 'Aprobador/Dirección', 'Solicitante'}
NON_ROLE_ACTORS = {'Atacante externo', 'Usuario de otro tenant', 'Desarrollador u operador', 'Servicio ML'}


def role(D):
    """Ningún rol no implementado se presenta como vigente."""
    t = D['F34A_Modelo_de_Amenazas.md']
    sec = t.split('## 3. Actores')[-1].split('## 4.')[0] if '## 3. Actores' in t else ''
    out = [] if sec else ['modelo sin sección de actores']
    for r in rows(sec, r'.*'):
        if len(r) != 3 or r[0] in ('Actor', '---') or r[0].startswith('-'):
            continue
        name = plain(r[0])
        if name not in IMPLEMENTED_ROLES | NON_ROLE_ACTORS and 'actor conceptual futuro' not in r[0]:
            out.append(f'actor «{name}» presentado como rol vigente sin estar implementado')
    for n, tx in D.items():
        for i, ln in enumerate(tx.splitlines(), 1):
            if re.search(r'Administrador', ln) and not re.search(r'conceptual futuro|no es un rol implementado', ln, re.I):
                out.append(f'{n}:{i}: menciona un administrador como rol vigente')
    return out


XSS_CONTROLS = ['escap', 'sanitiza', 'HTML arbitrario', 'validación de contenido', 'CSP', 'pruebas de renderizado seguro']


def xss(D):
    """Amenaza explícita de XSS persistente sobre citas, anotaciones y evidence_text, con sus controles."""
    t = D['F34A_Modelo_de_Amenazas.md']
    rs = [r for r in rows(t, r'T-\d\d') if 'XSS persistente' in ' '.join(r)]
    if not rs:
        return ['falta la amenaza de XSS persistente']
    row = ' '.join(rs[0])
    out = [f'XSS persistente sin el control «{c}»' for c in XSS_CONTROLS if c.lower() not in row.lower()]
    out += [f'XSS persistente no cubre «{c}»' for c in ('citas', 'evidence_text', 'anotaciones') if c not in row]
    return out


DOC_RULES = [('AP', ap), ('MG', mg), ('ADR', adr), ('JUR', jur), ('PRI', pri), ('NEC', nec), ('TM', tm), ('RF', rf),
             ('GOV', gov), ('LNK', lnk), ('EIA', eia), ('AUD', aud), ('RANK', rank), ('TOK', tok), ('ROLE', role),
             ('XSS', xss)]


def run_doc_rules(D):
    res = {}
    for rid, fn in DOC_RULES:
        try:
            res[rid] = fn(D)
        except (KeyError, IndexError, ValueError, AttributeError) as e:
            res[rid] = [f'error estructural: {type(e).__name__}: {e}']
    return res


# ---------------------------------------------------------------- casos negativos (mutaciones en memoria)
def sub(n, a, b):
    def f(D):
        assert a in D[n], (n, a)
        D = dict(D)
        D[n] = D[n].replace(a, b, 1)
        return D
    return f


def regex_sub(n, pat, rep):
    def f(D):
        D = dict(D)
        new = re.sub(pat, rep, D[n], count=1, flags=re.M)
        assert new != D[n], (n, pat)
        D[n] = new
        return D
    return f


CASES = [
    ('QA-01', 'MG', 'G0-02 (revisión jurídica) marcado CUMPLIDO',
     regex_sub('F34A_Matriz_G0.md', r'(\| G0-02 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**')),
    ('QA-02', 'MG', 'G0-14 (ADR-005) marcado CUMPLIDO',
     regex_sub('F34A_Matriz_G0.md', r'(\| G0-14 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**')),
    ('QA-03', 'MG', 'G0-12 (necesidad institucional) marcado CUMPLIDO',
     regex_sub('F34A_Matriz_G0.md', r'(\| G0-12 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**')),
    ('QA-04', 'AP', 'Se declara «G0 = APROBADA CON RESTRICCIONES»',
     sub('F34A_Decision_Readiness_G0.md', '- **G0 = NO APROBADA.**', '- **G0 = APROBADA CON RESTRICCIONES.**')),
    ('QA-05', 'AP', 'Se declara «ADR-005 = APROBADA»',
     sub('README.md', '**ADR-005 = PROPUESTA**', '**ADR-005 = APROBADA**')),
    ('QA-06', 'ADR', 'Decisión APRUEBA sin nombre ni fecha (aprobación falsificada)',
     sub('F34A_Paquete_Aprobacion_ADR005.md', '| — | Integrante del equipo | — | PENDIENTE | — |',
         '| — | Integrante del equipo | — | APRUEBA | — |')),
    ('QA-07', 'ADR', 'Estado del registro cambiado a APROBADO con decisiones pendientes',
     sub('F34A_Paquete_Aprobacion_ADR005.md', '**Estado actual: PENDIENTE.**', '**Estado actual: APROBADO.**')),
    ('QA-08', 'JUR', 'Punto jurídico J-03 marcado APROBADO',
     regex_sub('F34A_Checklist_Revision_Juridica.md', r'(\| J-03 \|.*?\| )REQUIERE ABOGADO/RESPONSABLE LEGAL', r'\1APROBADO')),
    ('QA-09', 'JUR', 'J-03 marcado VERIFICADO sin fuente oficial',
     regex_sub('F34A_Checklist_Revision_Juridica.md', r'(\| J-03 \|.*?\| )REQUIERE ABOGADO/RESPONSABLE LEGAL',
               r'\1VERIFICADO')),
    ('QA-10', 'AP', 'Se afirma que la revisión jurídica fue aprobada',
     sub('F34A_Decision_Readiness_G0.md', '## 5. Datos reales', 'La revisión jurídica fue aprobada.\n\n## 5. Datos reales')),
    ('QA-11', 'AP', 'Se afirma cumplimiento de la Ley 29733',
     sub('F34A_Analisis_Privacidad_Preliminar.md', '## 15. Conclusión preliminar',
         '## 15. Conclusión preliminar\n\nEl diseño cumple la Ley 29733.')),
    ('QA-12', 'PRI', 'Se elimina la prohibición de datos reales',
     sub('F34A_Analisis_Privacidad_Preliminar.md', '**Regla vigente: los datos reales siguen PROHIBIDOS.**',
         '**Regla vigente: los datos reales se admiten con consentimiento.**')),
    ('QA-13', 'AP', 'Se declara que los datos reales quedan autorizados',
     sub('F34A_Decision_Readiness_G0.md', '## 5. Datos reales', '## 5. Datos reales\n\nLos datos reales quedan autorizados.')),
    ('QA-14', 'NEC', 'Respuesta inventada del docente en N-01',
     regex_sub('F34A_Validacion_Necesidad_Institucional.md', r'^\| N-01 \| — \|', '| N-01 | Sí, hay demoras. |')),
    ('QA-15', 'NEC', 'Firma inventada de un participante',
     sub('F34A_Validacion_Necesidad_Institucional.md', '| Docente | — | — | — | — |',
         '| Docente | — | Docente | 2026-10-04 | Firmado |')),
    ('QA-16', 'TM', 'Se elimina la amenaza de logs con PII',
     regex_sub('F34A_Modelo_de_Amenazas.md', r'^\| T-13 \|.*\n', '')),
    ('QA-17', 'TM', 'Se elimina la amenaza de fuga cross-tenant',
     sub('F34A_Modelo_de_Amenazas.md', '**Fuga cross-tenant**', 'Fuga')),
    ('QA-18', 'RF', 'RF-CAND-01 con estado BASELINE',
     regex_sub('F34A_RF_Candidatos.md', r'(\| RF-CAND-01 \|.*\| )CANDIDATO \|$', r'\1BASELINE |')),
    ('QA-19', 'RF', 'Requisito definido como RF-32 productivo en una tabla',
     sub('F34A_RF_Candidatos.md', '| RF-CAND-02 |', '| RF-32 |')),
    ('QA-20', 'AP', 'Se afirma que un candidato pasa al baseline',
     sub('F34A_RF_Candidatos.md', '## 3. Fuera del registro', 'RF-CAND-02 pasa al baseline como RF-32.\n\n## 3. Fuera del registro')),
    ('QA-21', 'GOV', 'F35–F40 declaradas habilitadas',
     sub('F34A_Decision_Readiness_G0.md', '- **F35–F40 = BLOQUEADAS.**', '- **F35–F40 = HABILITADAS.**')),
    ('QA-22', 'GOV', 'F34A declarada CERRADA antes de la auditoría',
     sub('README.md', '**F34A = LISTA PARA AUDITORÍA.**', '**F34A = CERRADA.**')),
    ('QA-23', 'MG', 'G0 no aprobada eliminada del README con criterios pendientes',
     sub('README.md', '**G0 = NO APROBADA**', '**G0 en revisión**')),
    ('QA-24', 'MG', 'Resumen de la matriz incoherente con las filas',
     sub('F34A_Matriz_G0.md', '| PENDIENTE EXTERNO | G0-02, G0-03, G0-12, G0-14 | 4 |',
         '| PENDIENTE EXTERNO | G0-02, G0-03, G0-12, G0-14 | 2 |')),
    ('QA-25', 'LNK', 'Enlace roto a un documento inexistente',
     sub('README.md', '(F34A_Matriz_G0.md)', '(F34A_Matriz_G0_inexistente.md)')),
    # auditoría F34A
    ('QA-26', 'EIA', 'Checklist: la evaluación de impacto «se adjunta o se planifica»',
     regex_sub('F34A_Checklist_Revision_Juridica.md', r'^2\. concluya de forma documentada.*$',
               '2. indique si se requiere evaluación de impacto (J-08) y, si es así, la adjunte o la planifique;')),
    ('QA-27', 'EIA', 'S-02 acepta una evaluación de impacto planificada',
     regex_sub('F34A_Decision_Readiness_G0.md', r'(^\| S-02 \|[^|]*\| )[^|]*(\|)',
               r'\1Informe firmado y, si corresponde, la evaluación de impacto planificada \2')),
    ('QA-28', 'EIA', 'Se elimina la sección de regla de cierre de G0-02',
     sub('F34A_Checklist_Revision_Juridica.md', '## 5. Regla de cierre de G0-02', '## 5. Notas sobre G0-02')),
    ('QA-29', 'AUD', 'Privacidad vuelve a afirmar «AuditLogger sin PII»',
     regex_sub('F34A_Analisis_Privacidad_Preliminar.md', r'^- `AuditLogger` registra usuario.*$',
               '- `AuditLogger` sin PII ni secretos (contrato 6); trigger `audit_logs_append_only`.')),
    ('QA-30', 'AUD', 'RF-CAND-09 vuelve a «sin PII» absoluto',
     sub('F34A_RF_Candidatos.md', 'sin texto de evidencia ni PII innecesaria', 'sin PII ni texto de evidencia')),
    ('QA-31', 'AUD', 'Se afirma que la auditoría es anónima',
     sub('F34A_Modelo_de_Amenazas.md', '| A-06 | `audit_logs` de solo inserción |',
         '| A-06 | `audit_logs` de solo inserción y anónimos |')),
    ('QA-32', 'RANK', '«El sistema nunca ordena personas» (contradice RF-21)',
     regex_sub('F34A_Validacion_Necesidad_Institucional.md', r'\*\*El nuevo motor.*?se mantiene sin cambios\.',
               '**El sistema nunca califica, ordena, recomienda ni descarta personas.**')),
    ('QA-33', 'TOK', 'T-02 describe el token interno como opcional',
     regex_sub('F34A_Modelo_de_Amenazas.md', r'(^\| T-02 \|.*?\| E: )[^|]*(\|)',
               r'\1token interno opcional (`ML_SERVICE_TOKEN`), servicio en red interna \2')),
    ('QA-34', 'ROLE', 'Administrador presentado como rol vigente',
     sub('F34A_Modelo_de_Amenazas.md', 'Administrador de la organización (**actor conceptual futuro**)',
         'Administrador de la organización')),
    ('QA-35', 'ROLE', 'Otro rol inventado en la tabla de actores',
     sub('F34A_Modelo_de_Amenazas.md', '| Solicitante | Media |', '| Supervisor académico | Media |')),
    ('QA-36', 'XSS', 'Se elimina la amenaza de XSS persistente',
     regex_sub('F34A_Modelo_de_Amenazas.md', r'^\| T-25 \|.*\n', '')),
    ('QA-37', 'XSS', 'XSS persistente sin pruebas de renderizado seguro ni CSP',
     regex_sub('F34A_Modelo_de_Amenazas.md', r'; CSP y controles de frontend si el despliegue los adopta; pruebas de '
                                              r'renderizado seguro con', '; con')),
]


# ---------------------------------------------------------------- git: alcance, baseline, runtime y dependencias
def git(*a):
    return subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout


GOVERNANCE_FILES = frozenset({'CLAUDE.md', 'README.md', 'docs/PROGRESS.md',
                              'docs/academico/ACADEMIC_BASELINE.md'})
CLOSURE_SUBJECTS = [
    'docs(governance): register F34A readiness; G0 remains not approved',
    'docs(academic): add F34A G0 readiness package and threat model',
    'docs(academic): add F34A G0 readiness validator',
]


def closure_scope(subjects, committed, dirty):
    """Solo el commit C autorizado, tras B/A, permite su delta de gobierno limpio.

    No habilita ediciones pendientes ni una excepción permanente para fases futuras.
    """
    if subjects != CLOSURE_SUBJECTS or not committed or not committed <= GOVERNANCE_FILES or dirty:
        return frozenset()
    return frozenset(committed)


def git_checks():
    out = []
    changed = set(git('diff', '--name-only', BASE).split())
    changed |= set(git('ls-files', '--others', '--exclude-standard').split())
    allowed = ('docs/academico/g0-readiness/', 'docs/academico/tools/f34a/')
    subjects = git('log', '-3', '--format=%s').splitlines()
    committed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').splitlines())
    dirty = set(git('diff', '--name-only', 'HEAD', '--', *sorted(GOVERNANCE_FILES)).splitlines())
    governance = closure_scope(subjects, committed, dirty)
    fuera = sorted(p for p in changed if not p.startswith(allowed) and p not in governance)
    if fuera:
        out.append(f'cambios fuera del alcance de F34A: {fuera[:5]}')
    protected = ['app', 'routes', 'config', 'database', 'resources', 'tests', 'cypress', 'ml-service', 'composer.json',
                 'composer.lock', 'package.json', 'package-lock.json', 'docker-compose.yml', 'Dockerfile',
                 'docs/v1.1/scope-preliminary.md', 'docs/final-report/traceability-master.md',
                 'docs/rf-implementation-matrix.md', 'docs/assumptions.md',
                 'docs/academico/diseno-inteligente/F33_ADR_005_G0.md', 'docs/academico/datos-sinteticos']
    tocados = git('diff', '--name-only', BASE, '--', *protected).split()
    if tocados:
        out.append(f'runtime, dependencias, baseline, ADR-005 o F34 modificados: {tocados[:5]}')
    adr_text = open(os.path.join(ROOT, 'docs', 'academico', 'diseno-inteligente', 'F33_ADR_005_G0.md'),
                    encoding='utf-8').read()
    if '- **Estado:** **PROPUESTA**' not in adr_text or 'G0 = NO APROBADA' not in adr_text:
        out.append('ADR-005 ya no figura como PROPUESTA con G0 NO APROBADA')
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    for n in FILES:
        add(os.path.isfile(os.path.join(DOCS, n)), f'documento presente: {n}')
    D = read_all()

    res = run_doc_rules(D)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:2]}' if viol else ''))

    for cid, rule, what, mut in CASES:
        try:
            r = run_doc_rules(mut(D))
            add(r.get(rule), f'{cid} detectado por {rule}: {what}')
        except AssertionError as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({e})')
    add(len(CASES) >= 35, f'casos negativos: {len(CASES)}')

    gv = git_checks()
    add(not gv, f'GIT: alcance, baseline, ADR-005, runtime y dependencias sin cambios: {gv}')
    add(closure_scope(CLOSURE_SUBJECTS, {'CLAUDE.md'}, set()) == {'CLAUDE.md'},
        'cierre: admite únicamente el delta de gobierno comprometido en C tras B/A')
    add(not closure_scope(CLOSURE_SUBJECTS, {'CLAUDE.md'}, {'CLAUDE.md'}),
        'cierre: rechaza nuevas ediciones de gobierno pendientes')
    add(not closure_scope(['fase futura', *CLOSURE_SUBJECTS[1:]], {'CLAUDE.md'}, set()),
        'cierre: la excepción no habilita commits de fases futuras')
    add(not closure_scope(CLOSURE_SUBJECTS, {'app/Models/User.php'}, set()),
        'cierre: rechaza archivos fuera de los cuatro documentos de gobierno autorizados')

    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    est = {r[0]: plain(r[8]) for r in rows(D['F34A_Matriz_G0.md'], r'G0-\d\d') if len(r) == 10}
    for st in ('CUMPLIDO', 'PARCIAL', 'PENDIENTE EXTERNO', 'BLOQUEADO', 'NO APLICA'):
        print(f'INFO {st}: {[k for k, v in est.items() if v == st]}')
    print(f'validate_f34a: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
